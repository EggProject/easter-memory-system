# Szintézis — szerver-oldali technikai kérdések

Írta: Opus (fő szál) · Keresés: 8 + 2 Sonnet ügynök · Ellenőrzés: 6 Sonnet verifikáló
Dátum: 2026-09-05 · Bizonyíték: 84 forrás, 148 állítás, minden hivatkozás él

Ez a jelentés a **#13 (írási sorbaállítás)**, **#14 (Better Auth jogosultság, Drizzle+FTS5)**
és **#15 (audit napló tárolása)** feladatokat zárja le. Minden szám és mechanizmus mögött
ott van a forrásazonosító a `06-evidence-table.csv`-ben; amit az ellenőrzés megdöntött vagy
gyengített, azt a 4. szakasz sorolja fel.

Megbízhatósági jelölés: **Magas** / **Közepes** / **Alacsony** / **Vitatott** /
**Ellenőrizetlen**. Ebben a kampányban **egyetlen állítás sem kapott Magas minősítést** —
nem azért, mert gyenge a bizonyíték, hanem mert szinte minden állítás pontosan egy
elsődleges forrásra (hivatalos dokumentáció, man page, spec) támaszkodik, és a protokoll a
Magashoz két független forrást kér. Egy man page nem lesz igazabb attól, hogy valaki
idézi — de a szabályt nem hajlítom meg, inkább leírom, hogy miért így néz ki a kép.

---

## 1. Írási sorbaállítás — #13

### 1.1 A kérdés két külön kérdés

Az eddigi döntés (D-07) szerint minden írás viszi az olvasott tartalom lenyomatát, és
eltérésnél megáll. Ez **észleli** az ütközést. A megelőzés viszont két, egymástól független
rétegen múlik, és a kettőt nem szabad összekeverni:

- **Fájlrendszer-réteg**: hogy egy fájl soha ne legyen félig kiírva vagy elveszve.
- **Folyamaton belüli réteg**: hogy egy fájlra egyszerre tényleg egy feladat írjon.

Az egyik nem helyettesíti a másikat.

### 1.2 Fájlrendszer-réteg: ideiglenes fájl + átnevezés, két fsync-kel

A POSIX `rename()` atomikusan cseréli a célfájlt — a cél soha nem látszik hiányzónak —, de
csak **ugyanazon a mountponton belül** (`EXDEV` egyébként). *[Közepes]*

Az `fsync()` a fájl tartalmát viszi lemezre, **a szülőkönyvtár bejegyzését nem** — ahhoz
külön `fsync()` kell a könyvtár leíróján. *[Közepes]* Ezt a hiányt nem elméleti: a 2009-es
ext4 „nullhosszúságú fájl" ügy (Ted Ts'o, az ext4 karbantartója, saját blogján) pontosan
ezen bukott el, és a kernelfejlesztők 2019-es LSFMM-vitájában is az hangzott el, hogy a
temp+rename az iparági szabvány, de „the applications often do not use fsync() correctly,
so they lose their data anyway". *[Közepes]*

> **Kiegészítés a korábbi állításhoz.** A 2009-es eset 17 éves, és a 2.6.30-as kernel óta a
> rename/truncate azonnali blokk-allokálást vált ki. Az ellenőrzés ezért a jelen időben
> megfogalmazott változatot gyengítette: a hiba maga javítva van, a **tanulság** (a rename
> önmagában nem tartósság) áll.

macOS-en van egy külön csapda: a sima `fsync()` az Apple dokumentációja szerint nem
garantálja, hogy az adat a lemezmédiumra került; ehhez `F_FULLFSYNC` kell. *[Alacsony] —
lásd 4. szakasz, forrásminősítési hiba*

**Kész csomag erre**: az npm `write-file-atomic` pontosan ezt a mintát valósítja meg
(egyedi ideiglenes fájlnév, alapból fsync a rename előtt), **és** saját belső
Promise-sorral szerializálja az ugyanarra a fájlnévre irányuló egyidejű írásokat egy
folyamaton belül. *[Közepes]* Vagyis egyetlen csomag mindkét réteget lefedi.

`Bun.write`-ról nincs hivatalos állítás, hogy atomikus lenne, és van nyitott hibajegy
(#31682), amely szerint az S3-streamelő útvonala nem truncate-eli a célfájlt. *[Alacsony] —
felhasználói bejelentés* Ez nem a mi útvonalunk, de elég ok arra, hogy ne feltételezzük az
atomicitást.

### 1.3 Folyamaton belüli réteg: fájlonkénti zár

A minta: kulcsonként (fájlútvonalanként) egy Promise-lánc vagy mutex, más kulcs
párhuzamosan fut. Konkrét, dokumentált eszközök:

| Csomag | Amit ad | Amire figyelni |
|---|---|---|
| `async-lock` | kulcsos zár, `maxPending` (sormélység-korlát), `timeout`, `maxOccupationTime` | ez adja készen a „várjon vagy utasítsa vissza" döntést |
| `async-mutex` | `runExclusive`, `withTimeout` (E_TIMEOUT), `tryAcquire` (azonnali E_ALREADY_LOCKED) | ha a `release` elmarad, a README szerint „will likely deadlock the application" |
| `mutexify` | **dokumentált FIFO-sorrend** — kiéheztetés ellen | callback- és promise-API |
| `p-queue` | globális sor, `concurrency: 1` = teljes szerializáció | egy elbukott feladat nem állítja meg a többit |
| `p-limit` | konkurrencia-korlát | a README maga figyelmeztet: rekurzív hívás ugyanazon a limiteren holtpont |

Mind *[Közepes]*, a csomagok saját dokumentációjából.

### 1.4 A garancia határa — és ez tervezési következmény, nem részlet

**Egy folyamaton belüli zár abban a pillanatban semmit nem ér, amikor több folyamat van.**
A Node `cluster` minden workere külön OS-folyamat, külön memóriával; a Bun `reusePort`
szintén külön folyamatokat indít, amelyek `SO_REUSEPORT`-tal osztoznak egy porton. *(Közepes
— a dokumentáció a folyamat-szeparációt mondja ki; hogy ebből következik a mutex
érvénytelensége, az az én következtetésem, és az ellenőrzés ezt helyesen meg is jelölte.)*

Ebből két dolog következik a mi rendszerünkre:

1. **A kiszolgáló egyetlen folyamatként fut.** Nincs cluster, nincs `reusePort`. Ez amúgy is
   egybevág azzal, amit az SQLite-ról már tudunk (egy kapcsolat, `locking_mode=EXCLUSIVE`),
   és a D-14-gyel (központi szerver, nincs közvetlen fájlhozzáférés).
2. **A napi karbantartó (D-16 `karbantart` mód) viszont a folyamaton kívül van.** Ha külön
   folyamatként indul, a fájlonkénti mutex rá nem vonatkozik. Erre két tiszta megoldás van:
   vagy a karbantartó a kiszolgáló folyamatán belül fut ütemezetten (akkor ugyanaz a mutex
   védi), vagy külön folyamat, és akkor kell egy folyamatközi zár — `proper-lockfile`, amely
   tudatosan `mkdir`-alapú, mert a README szerint az `O_EXCL` „broken on NFS file systems".
   *[Közepes]* Ugyanez a README mondja ki, hogy SIGKILL vagy VM-összeomlás után a zár nem
   szabadul fel magától, csak a 10 másodperces mtime-heartbeat alapján évül el.

### 1.5 Mit csinálnak a valódi markdown-rendszerek? Semmit.

Ez a szakasz a legfontosabb megerősítés a D-07 mellett, mert azt mutatja, hogy a mi
megoldásunk **jobb, mint bármelyik vizsgált terméké**:

- **Logseq** (fájl-alapú sync): nincs zárolás, nincs merge, ~20 mp-es intervallum,
  utolsó-nyert. Dokumentált hibajegy (#7197): két eszközön szerkesztett dokumentumból az
  egyik verzió nyomtalanul elvész. Egy másik (#1332, „priority-A / data-stability"):
  oldallétrehozáskor felülírt egy létező .md fájlt ütközés-ellenőrzés nélkül. *[Alacsony] —
  megerősítetlen hibajegyek, de éppen ez a lényeg: ezek a valós panaszok*
- **Joplin**: a vesztes verziót külön „Conflict" jegyzetfüzetbe másolja, a távoli felülírja
  a helyit. *[Közepes]*
- **Obsidian Sync**: markdownnál diff-match-patch automatikus merge; v1.9.7-től választható
  „conflict file" mód; nem-markdownnál utolsó-módosítás-nyer. *[Közepes]*
- **SilverBullet**: van sync-motorja, de **konfliktuskezelésről semmit nem dokumentál**.
  *(Az eredeti, erősebb állítást — „nincs is sync" — az ellenőrzés megdöntötte.)*
- **Decap CMS** (git-alapú): a „konfliktus feloldása a felületről" kérés **2018 óta
  nyitott**. Vagyis nem old fel semmit. *[Közepes]*

**Egyik vizsgált rendszer sem használ tartalom-lenyomatos írási előfeltételt.** Ez „evidence
of absence", nem hiányos kutatás: hét rendszer dokumentációját néztük át. A D-07 tehát
szokatlan — és a felsorolt adatvesztések pontosan azok, amiket megelőz.

### 1.6 Javaslat a #13-ra

Három réteg, egymásra épülve:

1. **Írás**: ideiglenes fájl ugyanabban a könyvtárban → `fsync` a fájlra → `rename` →
   `fsync` a könyvtárra. Kész csomaggal (`write-file-atomic`) vagy kézzel.
2. **Sorbaállítás**: fájlútvonal szerinti kulcsos zár, sormélység-korláttal és időtúllépéssel
   (`async-lock` adja készen). A kiszolgáló egyetlen folyamat.
3. **Előfeltétel**: marad a D-07 tartalom-lenyomat. Ez fogja el azt, amit az első kettő nem:
   a felhasználót, aki elavult tartalom fölé ír.

A karbantartó módról külön kell dönteni (1.4/2. pont) — ez a kérdés eddig nem volt kimondva.

---

## 2. Better Auth és Drizzle — #14

### 2.1 A Better Auth-kérdés eldőlt, és tisztább a válasz, mint amire számítottunk

A D-12-ben nyitva hagyott figyelmeztetés — „a projekt-jogosultságot nem a Better Auth
adja" — nemcsak igaz, hanem **erősebben igaz**, mint gondoltuk. A gap-körben ez derült ki:

**A Better Auth hookjai kizárólag a Better Auth saját végpontjain futnak.** A plugin-doksi
szó szerint: *„Unlike hooks, middleware only runs on `api` requests from a client. If the
endpoint is invoked directly, the middleware will not run."* Minden dokumentált hook-példa
`ctx.path`-on ágazik el, és minden útvonal a Better Auth sajátja (`/sign-up/email`,
`/sign-in/email`, `/reset-password`). *[Közepes]*

Vagyis a mi MCP-végpontjainkra és admin felületünkre a Better Auth hook **rá sem fut**. Egy
projekt-jogosultság-ellenőrzést oda tenni nemcsak felesleges — nem is működne.

**Amit a dokumentáció a saját végpontokra ajánl**: `auth.api.getSession({ headers })` hívása
szerver oldalon, a saját route-ban. A Next.js integrációs oldal explicit figyelmeztetést ad:
*„You must always validate the session on your server for any protected actions or pages."*
*[Közepes]*

A `requireResourceOwnership` létező, importálható middleware (`better-auth/api`), de csak
Better Auth **plugin-végpontokon** használható, és egyetlen konfigurálható tulajdonos-oszlopot
ellenőriz — nem tetszőleges feltételt, nem jogosultság-táblát. *[Közepes]* A mi
modellünkhöz (projekt → személy → olvas/ír/töröl) nem illik.

Az `organization` plugin `createAccessControl` / `hasPermission` rendszere erőforrás-**típus**
→ akció leképezés, nem erőforrás-**példány**; a `hasPermission` nem is vesz át
objektum-azonosítót. *[Közepes]* A „Dynamic Access Control" is szerepkör-szintű marad.

**A határ tehát éles és kimondható:**

> A Better Auth azt válaszolja meg, hogy **ki ez az ember**. Azt, hogy **mit szabad neki
> ebben a projektben**, teljes egészében a mi kódunk dönti el, a mi tábláinkból, a mi
> kérés-rétegünkben.

Ez a D-12 figyelmeztetését nem eltünteti, hanem **döntéssé alakítja** — ami sokkal jobb,
mint egy nyitva hagyott aggály.

### 2.2 Amiért a jogosultságot nem tesszük a session-be

Csábító lenne a felhasználó jogosultság-halmazát a session-be tenni, hogy ne kelljen
kérésenként lekérdezni. A dokumentáció három külön okot ad arra, hogy ne tegyük:

1. A `customSession` extra mezői **nem kerülnek a session-cache-be**, és a callback minden
   egyes session-lekérdezéskor újra lefut. *[Közepes]* Tehát a spórolás nem is valósul meg.
2. A cookie-cache ~4 KB-os böngésző-korlátnál futásidejű hibát dob („Session data is too
   large to store in the cookie"), **chunkolás nélkül**. *[Alacsony] — hibajegy*
3. A cookie-cache bekapcsolt állapotában **a visszavont jogosultság a TTL lejártáig érvényben
   marad** — ezt maga a hivatalos doksi mondja ki. *[Közepes]*

A harmadik a döntő: ha az admin elvesz egy projektjogot, annak azonnal hatnia kell.
Kérésenkénti lekérdezés a saját táblánkból ezt ingyen megadja, és egy SQLite indexelt
lekérdezés ára ehhez képest nem számít.

### 2.3 Drizzle + FTS5: működik, de kézzel

- Drizzle séma-DSL-je **nem tud virtuális táblát**. A feature request 2024. március 20-án
  nyílt, **ma is nyitott**, PR és branch nélkül (élőben ellenőrizve, 2026-09-04). *[Közepes]*
- A kikerülő út dokumentált: `drizzle-kit generate --custom` üres migrációs fájl, kézzel
  megírt DDL; lekérdezéshez az `sql` tagged-template (`sql`, `sql<T>` csak fordítási idejű
  típus-tipp, `sql.raw()`, `db.execute()`). *[Közepes]*
- **Veszély**: ha az FTS5 táblát sima `sqliteTable`-ként deklaráljuk, a `drizzle-kit push`
  újra létrehozza és eltöri. *[Alacsony] — Discord-beszámoló* A Drizzle Studio szintén hibát
  dob az FTS5 `_config` árnyéktábláján. *[Alacsony]* Következtetés: az index-adatbázis sémáját
  **ne** a Drizzle séma-DSL kezelje.
- A hivatalos `drizzle-orm/bun-sqlite` driver létezik és dokumentált; meglévő `bun:sqlite`
  `Database` becsomagolható (`drizzle({ client: sqlite })`) — élőben ellenőrizve. *[Közepes]*
- Az FTS5 külső-tartalmú (`content=`) szinkronizáció **pontosan három triggert** ír elő, és a
  törléshez a speciális `INSERT INTO fts(fts, rowid, ...) VALUES('delete', ...)` alakot — sima
  `DELETE FROM fts` **nem** ez. *[Közepes]* Aki ezt elrontotta, adatbázis-korrupciót kapott.
  *[Alacsony] — egy fórumeset; a „10%-ban korrupt" szám a bejelentő saját becslése, az SQLite
  fejlesztő nem erősítette meg — lásd 4. szakasz.*
- **`bm25()` alacsonyabb érték = jobb találat**, tehát `ORDER BY bm25(tbl)` **növekvő**.
  *[Közepes]* Ezt könnyű fordítva megírni, és csendben rossz sorrendet ad.

### 2.4 A Bun-kockázat — ez a kampány legkellemetlenebb találata

A Bun dokumentációja szerint **macOS-en az Apple rendszer-SQLite-ját használja**, Linuxon és
Windowson a saját, statikusan linkelt buildjét. *[Közepes]*

Nyitott hibajegy (oven-sh/bun#31247, 2026-05-23, Bun 1.3.14 és 1.4.0-canary, macOS 15.5
arm64): a `sqlite_version()` **3.43.2**-t ad vissza a blogban ígért 3.53.0 helyett, és ezen
a buildon **bármely UPDATE vagy DELETE egy FTS5 táblán „database disk image is malformed"
(errno 267) hibát dob**. Az ügy ma is nyitott, karbantartói válasz és linkelt PR nélkül.
*[Alacsony] — megerősítetlen felhasználói bejelentés, de élőben ellenőrizve, hogy létezik és
nyitott.*

Egy másik FTS5-hiba (#37044, segfault `close()`-nál) **nem** verzióprobléma volt, hanem
Bun-oldali use-after-free, és aznap javították (#37045). *[Közepes]*

**És a legkellemetlenebb rész**: sehol nincs hivatalos állítás arról, hogy az FTS5 egyáltalán
be van-e fordítva a Bun SQLite-jába. A gap-ügynök átnézte a renderelt doksit és a nyers
`sqlite.mdx` forrást is — nulla találat „FTS5"-re. Ez „evidence of absence": a dokumentáció
tényleg hallgat. Hogy a gyakorlatban működik, azt csak hibajegyek reprodukciós kódjából
tudjuk.

### 2.5 Az én válaszom a Bun-kockázatra

Nem kell emiatt elhagyni sem a Bunt, sem az FTS5-öt. Három lépés, és a kockázat kezelhető:

1. **Induláskor önteszt.** A kiszolgáló indulásnál létrehoz egy eldobható FTS5 táblát,
   beszúr, frissít, töröl, keres, és kiírja a `sqlite_version()`-t. Ha bármelyik lépés elbukik,
   nem indul el, hanem megmondja, mi a baj. Ez öt sor, és **egy nem ellenőrizhető
   dokumentációs hiányt futásidejű ténnyé alakít**. Ezt azért javaslom, mert a bizonyíték
   hiánya itt nem múlik el attól, hogy tovább keresünk.
2. **Ne frissítsünk FTS5 sort helyben.** A jelentett korrupciót az UPDATE/DELETE váltja ki. A
   keresési index **eldobható** (D-03, D-12) — ez pont most fizet ki. A karbantartó
   újraépítheti az érintett részt, ahelyett hogy módosítanánk.
3. **A kiszolgáló Linuxon fusson.** Ott a Bun a saját buildjét viszi, nem az Apple-ét, és a
   jelentett verzió-eltérés fel sem merül. Ha a fejlesztés Macen folyik, a `setCustomSQLite`
   dokumentált kerülőút — de csak macOS-en működik, más rendszeren no-op, és a doksi
   kifejezetten extension-betöltésre ajánlja, nem erre. *[Közepes]*

---

## 3. Audit napló — #15

### 3.1 A méret nem probléma, a tempó lehet az

- SQLite maximális adatbázisméret ~17,5 TB (4 KB-os lap) illetve ~281 TB (64 KB). *[Közepes]*
  A soronkénti tárolási többlet szerkezetileg kicsi: egy varint fejlécméret + oszloponként
  általában 1 bájt típuskód, TEXT/BLOB-nál nincs fix szélességű kitöltés. *[Közepes]*
  **A „többgigás fájl" félelme nem a sorok számából jön, hanem a beszúrási tempóból.**
- Fizikai plafon: az fsync sebessége. Mért értékek megnevezett meghajtókon: 7200-as HDD ~56
  fsync/mp, SATA SSD 108–2031/mp, csúcs NVMe 7380/mp, BBU-s RAID 23 000/mp. *[Alacsony] —
  2018-as konzultánscég-blog, de a fizika áll*
- Beszúrási tempó: a `better-sqlite3` hivatalos benchmarkja 62 554 egysoros beszúrás/mp és
  4 141 db 100-soros tranzakció/mp — **2014-es MacBook Pro-n, Node 12-vel, 2020-ban, és nem a
  Bun SQLite-jával**. *[Alacsony] — a szám élőben stimmel, de a mérés se nem friss, se nem a mi
  környezetünk.* Nagyságrendnek jó, tervezési alapnak nem.

**Következtetés**: egy audit-esemény = egy tranzakció = egy fsync. Ha egy művelet több
eseményt ír, egy tranzakcióba kell tenni őket.

### 3.2 WAL-t az audit adatbázisra nem kell — és ez most egybevág mindennel

Mért adat: **1 egyidejű írónál a WAL 43%-kal, 2 írónál 17%-kal lassabb**, mint az
alapértelmezett DELETE journal; a WAL csak 4+ írótól kezdve nyer. *[Alacsony] — egyéni blog,
de megnevezett hardverrel* Az SQLite saját fórumán is elhangzik, hogy a WAL előnye a
konkurrencia, nem a nyers írási sebesség. *[Alacsony] — fórumvélemény*

Nálunk **egy író van** (1.4). Vagyis a WAL nem hozna sebességet, viszont hozná a már ismert
hátrányát: hálózati fájlrendszeren nem működik. Három független megfontolás mutat ugyanarra:
maradjunk a sima journalnál.

### 3.3 Particionálás: ne

- Az `ATTACH`-elt adatbázisok száma alapból 10, kemény korlát 125. *[Közepes]* Havi külön
  fájlokkal ez ~10 év alatt elfogy.
- Egy fájlon belüli havi táblák + `UNION ALL` nézet működik, de a nézet nem írható, és
  **az SQLite nem metszi le a nem érintett ágakat** — a WHERE-nek indexszel kell kizárnia
  őket. *[Alacsony] — harmadik féltől származó blog*
- Több ATTACH-elt fájlra kiterjedő tranzakció **WAL módban nem garantáltan atomi**. *(Alacsony;
  megjegyzés: az egyik verifikáló élőben megtalálta ugyanezt az `sqlite.org/lang_attach.html`
  hivatalos oldalán is — érdemes lenne felvenni a bizonyítéktárba.)*

**Javaslat**: egy tábla, particionálás nélkül. A két olvasási nézetet index oldja meg, nem
particionálás. Ha valaha tényleg megnő, az archiválás akkor is elvégezhető — de ne építsünk
ma bonyolultságot egy holnapután sem biztos problémára.

### 3.4 A két nézet: index és lapozás

- Oszlopsorrend: az SQLite csak az index bal oldali, megszakítás nélküli prefixét használja
  egyenlőségre, és a jobb szélső használt oszlop kaphat egyenlőtlenséget vagy rendezést.
  *[Közepes]* Ebből: a felhasználói nézethez `(user_id, ts DESC)`, a rendszernézethez
  `(ts DESC)`.
- A DESC index nem trükk, hanem fizikai tárolási forma (schema format 4), az SQLite 3.3.0
  óta érti, 3.7.10 óta alapértelmezett. *[Közepes]* Az `ORDER BY ts DESC` így a B-fát
  visszafelé olvassa, rendezés nélkül. *[Közepes]*
- **Fedő index nagyjából duplájára gyorsít**, mert elmarad a második keresés az alaptáblán;
  az `EXPLAIN QUERY PLAN` ezt „USING COVERING INDEX"-ként jelzi. *[Közepes] — élőben
  ellenőrizve*
- Terv olvasása: `SCAN` = teljes bejárás, `SEARCH` = részhalmaz, **`USE TEMP B-TREE FOR
  ORDER BY` = nincs index a rendezéshez** — ez az a sor, amit nem szabad látni. *[Közepes]*
- **Lapozás keyset-tel, nem OFFSET-tel.** Az OFFSET a lapmélységgel arányosan olvas és dob el
  sorokat. Nem egyedi rendezőkulcsnál kell egy döntetlen-feloldó:
  `WHERE (ts, rowid) < (?, ?) ORDER BY ts DESC, rowid DESC`. *(Közepes; a hozzá tartozó ábra a
  forrásban kvalitatív, hardver és sorszám nélkül — a mechanizmus áll, a konkrét szám nem.)*
- Az `ANALYZE` / `sqlite_stat1` **statikus pillanatkép**, nem frissül magától. *[Közepes]*
  Növekvő audit táblánál a napi karbantartó futtasson `PRAGMA optimize`-t. *(Ez az én
  javaslatom; a hivatkozott doksi-részlet magát a `PRAGMA optimize`-t nem említi — az
  ellenőrzés ezt jogosan jelezte.)*

### 3.5 Törlés, tömörítés, megőrzés

- **A `DELETE` nem zsugorítja a fájlt** — a hely szabad lapként marad. A `VACUUM` újraírja az
  egészet, de futás közben **a fájl méretének kétszeresét** kéri szabad helyként. Az
  `auto_vacuum` automatikusan zsugorít, de többlet-fragmentációt okoz. *[Közepes]*
- Tömörítés: zstd -1 = 2,896-szoros arány 510 MB/s mellett; gzip -1 = 2,743-szoros 105 MB/s
  mellett. *[Alacsony] — a gyártó saját README-benchmarkja, és a Silesia korpusz vegyes, nem
  JSON-napló; ismétlődő JSON-on a valós arány feltehetően jobb.*
- **Megőrzési idő: nincs szabvány, ami számot írna elő ránk.** Ez a szakasz megdőlt
  állításokból épül újra:
  - **NIS2 / CIR 2024/2690** — a naplózási szakasz **nem ír elő számot**. A „12 hónap (6+6)" és
    a „18 hónap" a hivatkozott tanácsadói oldal saját ajánlása. *(Az eredeti állítást az
    ellenőrzés lefokozta.)*
  - **SOC 2** — nem ír elő időtartamot; azt követeli, hogy a szervezet **saját szabályzatot**
    definiáljon és tartson be. *[Alacsony]*
  - **ISO/IEC 27001:2022 A.8.15** — a szöveg annyit mond, hogy a naplókat elő kell állítani,
    tárolni, védeni és elemezni; **szám nincs benne**. A „12 hónap az ipari szabvány" egyetlen,
    hivatkozás nélküli tanácsadói mondat. *(Alacsony, és az ellenőrzés külön kifogásolta, hogy
    az eredeti állítás több forrás egyetértését sugallta.)*
  - **GDPR 5. cikk (1)(e)** — a tárolási korlátozás **a másik irányba** szorít: a személyt
    azonosító naplóbejegyzés nem tartható tovább, mint amit a cél indokol. *[Közepes]*

**Javaslat**: mivel semmi nem ír elő számot, mi döntünk — és leírjuk, miért. Az audit napló
értelme épp az, hogy semmi ne tűnjön el csendben, a mérete pedig (3.1) nem probléma. Tehát:
**automatikus törlés nincs**, van viszont dokumentált archiválási eljárás arra az esetre, ha
valaha kelleni fog. Ha a GDPR-oldalt komolyan akarjuk venni, az a személyes adatok
minimalizálásán múlik a naplóban, nem a törlési határidőn.

- Hamisítás-észlelés (hash-lánc): **egyetlen forrás sem ad mért többletköltséget**. Az immudb
  „milliós tranzakció/mp" állítása gyártói marketing, hardver és konfiguráció megnevezése
  nélkül. *[Alacsony]* Ha kell, meg lehet csinálni, de a költségét mi fogjuk megmérni, nem
  találunk rá irodalmat.
- Referencia arra, hogy más hogyan csinálja: a HashiCorp Vault audit alrendszere
  **fail-closed** — ha minden audit-eszköz elérhetetlen, maga a Vault válik használhatatlanná;
  a fájl-alapú eszköz pedig „nagyon egyszerű: fájlhoz fűzi a logokat", rotáció nélkül.
  *[Közepes]* Ez a szigor a mi rendszerünkben túlzás lenne, de a kérdést fel kell tenni: ha az
  audit írása elbukik, a művelet menjen tovább vagy álljon meg?

---

## 4. Mi dőlt meg vagy gyengült az ellenőrzésben

Ezt a szakaszt azért írom ki külön, mert a kutatás akkor ér valamit, ha a hibái is látszanak.
148 állításból **108 megerősítve, 17 gyengítve, 2 megdöntve**, minden hivatkozás él.

**Két állítás elvesztette a hivatkozását — rögzítési hiba miatt.** A mentő eszköz nem az
oldalt mentette el, hanem egy AI-összefoglalót róla („## Issue Summary", „The reporter
encountered…"), így az idézet valójában a mentő ügynököt idézte, nem a forrást. Két állítást
érintett: a Bun FTS5-korrupciós hibajegyet és egy Better Auth `hasPermission` hibajegyet. A
Bun-osat a gap-körben **szigorúbb prompttal újra rögzítettük**, most áll a lábán; a Better
Auth-osat elejtettem, mert a döntés nem múlik rajta.

**Forrásminősítési hibák — mind ugyanabba az irányba.** A tekintélyesnek látszó, de valójában
nem lektorált források kaptak túl magas besorolást:

| Forrás | Kapott | Helyes | Miért |
|---|---|---|---|
| keith.github.io (Apple man page tükör) | T2 | T5–T6 | magánszemély GitHub Pages-tükre, nincs szerkesztés (a tartalom viszont hű az Apple eredetihez) |
| use-the-index-luke.com | T3 | T4 | egyszemélyes szakmai oldal, nincs szerkesztőségi folyamat |
| sqlite.org fórumbejegyzések | T1 | T6 | a domain hivatalos, a tartalom egyetlen felhasználó anekdotája |
| GitHub hibajegyek (több) | T1 | T6 | bejelentő ≠ karbantartó; megerősítés nélkül |
| better-sqlite3, zstd, sqlite.org saját benchmarkjai | T1 | T4 | gyártó a saját termékéről |

Ez pontosan az az aszimmetria, amire a protokoll figyelmeztet, és amit magamnak is fel kell
írnom: a domain neve nem minősítés.

**Számok, amiket nem szabad használni:**

- „Az FTS5 rossz trigger-minta az esetek 10%-ában korrupciót okoz" — ez a **bejelentő saját
  becslése**; az SQLite fejlesztő (Dan Kennedy) csak annyit mondott, hogy „mindkét verziónak
  működnie kellett volna". A mechanizmus áll, a szám nem.
- „12 hónap az ISO 27001 ipari szabványa" — egyetlen, hivatkozás nélküli tanácsadói mondat.
- „NIS2 12/18 hónap" — a tanácsadó saját ajánlása, nem a rendelet.
- A `better-sqlite3` beszúrási számok: 2020, Node 12, 2014-es MacBook, más binding, mint a mienk.

**Egy vault-hiba, amit érdemes tudni**: az `sqlite.org/limits.html` mentett pillanatképe
**csonka** — hiányzik belőle az ATTACH-korlátokról szóló szakasz. Az élő oldalon megvan, és a
verifikáló élőben ellenőrizte, így az állítás áll. De ez pont az a hiba, ami miatt a
protokoll a számokat élőben is ellenőrizteti: a pillanatkép-alapú ellenőrzés itt hamis
„unsupported"-ot adott volna.

**Következtetések, amiket ügynökök forrásnak álcáztak** (helyesek, de a mieink, nem a
forráséi): hogy a cluster/reusePort érvényteleníti a mutexet; hogy a `before` hook az
objektum-szintű ellenőrzés primitívje; hogy az Outline a konkurenciát CRDT-vel oldja meg;
hogy a `(user_id, ts)` sorrend következik az optimalizáló szabályából. Mindegyiket
következtetésként jelöltem meg a fenti szövegben.

---

## 5. Amit nem sikerült megtudni

- **Hivatalos állítás arról, hogy az FTS5 be van-e fordítva a Bun SQLite-jába — nincs.**
  „Evidence of absence": a renderelt doksi és a nyers forrás is átnézve, nulla találat. Ezt
  már nem kutatással kell zárni, hanem az induláskori önteszttel (2.5/1).
- Nincs megerősítve, hogy a stabil Bun 1.4 (2026-08-20) tartalmazza-e a 2026-08-06-i
  FTS5-segfault javítást. Valószínű, de nem forrásolt.
- macOS Intelre nincs közvetlen FTS5-korrupciós reprodukció, csak analóg verzió-eltérés.
- Nincs mért többletköltség hash-láncolt naplóra sehol, csak gyártói állítás.
- Nincs publikált bájt/sor számítás valós audit-sémára indexekkel; a szerkezeti alapadatok
  megvannak, a becslést nekünk kell elvégezni.
- Nincs kemény, hardverrel és sorszámmal dokumentált OFFSET vs keyset benchmark SQLite-on.
- Dendron, Zettlr, Foam konkurenciakezelése nem lett vizsgálva (nem jutott rá kör) — ez
  „nem kutatott", nem „nincs mechanizmus".
- A TiddlyWiki MultiWikiServer ETag/If-Match írási előfeltétele nem lett megerősítve. Ha
  létezik, ez lenne az egyetlen precedens a D-07-re — érdemes lehet még egy körre.

---

## 6. Amit ebből a három feladatra javaslok

**#13 — írási sorbaállítás**: temp+rename két fsync-kel, fájlonkénti kulcsos zár
sormélység-korláttal, egyetlen kiszolgáló-folyamat, és marad a D-07 tartalom-lenyomat. Új,
eddig ki nem mondott kérdés: a napi karbantartó a kiszolgáló folyamatán belül fusson-e.

**#14 — Better Auth és Drizzle**: a D-12 figyelmeztetése döntéssé alakul — a Better Auth a
személyazonosságot adja, a projekt-jogosultságot a mi kérés-rétegünk dönti el, kérésenkénti
lekérdezéssel, nem a session-ből. Az FTS5 séma nem a Drizzle DSL-jében él, hanem kézzel írt
migrációban; induláskor öntesztet futtatunk; a kiszolgáló Linuxon fut.

**#15 — audit napló**: egy SQLite tábla, particionálás nélkül, sima journal (nem WAL), két
index (`(ts DESC)` és `(user_id, ts DESC)`), keyset-lapozás, `PRAGMA optimize` a napi
karbantartóban, automatikus törlés nincs. Egy nyitott kérdés marad: mi történjen, ha az audit
írása elbukik.
