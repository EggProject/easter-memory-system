# Szintézis — skálázás: egy app vagy több

Írta: Opus (fő szál) · Keresés: 6 Sonnet ügynök · Ellenőrzés: 4 Sonnet verifikáló
Dátum: 2026-09-05 · Bizonyíték: 67 forrás, 105 állítás, minden hivatkozás él
Verdikt: 88 megerősítve, 17 gyengítve, 0 megdöntve · 66 **Magas**, 28 Közepes, 11 Alacsony

Ez a kampány a tulajdonos kérdésére válaszol: *„mi van ha 100 user egyszerre használja?"* — és arra,
hogy a karbantartó meg a fájlírás legyen-e külön alkalmazás.

---

## 1. A kiinduló elemzésem — és amit a kutatás módosított rajta

A kör előtt ezt gondoltam: a szabály nem „egy folyamat", hanem „egy **író**"; az olvasó oldal zár
nélkül szaporítható; a felső határ egy gép; és az igazi szűk keresztmetszet a beágyazás-számítás.

**Ebből mi állt meg:** a beágyazás-hipotézis megerősítést kapott, és erősebbet, mint reméltem.
Az egy-gép-plafon is áll.

**Amit a kutatás megcáfolt bennem:** azt hittem, az „egy írós" minta modul-szintű elv, és a
folyamatra bontás külön indoklást kíván. Martin Thompson eredeti szövege **kifejezetten kiterjeszti
folyamat- és hálózati határokon át**: *„The same patterns apply if the processing node is a server
and the communication system is a local network."* Két verifikáló egymástól függetlenül élőben
ellenőrizte ezt, mert az egyik kereső a szűkebb olvasatot rögzítette. Vagyis a szétvágásnak van
elvi támogatása — nem csak megtűrt kompromisszum.

**És egy dolog, amire nem számítottam:** az igazi korlát nem a zár és nem is a lemez, hanem
**az eseményhurok**, és rosszabb formában, mint gondoltam. Lásd a következő szakaszt.

---

## 2. Az eseményhurok — a kampány legfontosabb találata

Három egymást erősítő tény, mind a gyártók saját dokumentációjából:

- **A `bun:sqlite` szinkron.** Bun saját szava: *„The API is synchronous and fast."* A `.all()`,
  `.get()`, `.run()` értéket ad vissza, nem Promise-t. **[Magas]**
- **A Bun `Worker` API-ja a saját dokumentációja szerint kísérleti**: *„The Worker API is still
  experimental (particularly for terminating workers)."* Ez az egyetlen dokumentált mód arra, hogy
  processzoridő-igényes munkát a kérés útjából kivegyünk — és nem termelésre kész. **[Magas]**
- **A folyamaton belül futtatható beágyazó könyvtárak mind blokkolnak.** A `transformers.js`
  Node alatt saját doksija szerint az `onnxruntime-node`-ot használja; az ONNX Runtime pedig
  annyi szálat indít, ahány fizikai mag van, **és a hívó szál maga is számol** — tehát végig
  blokkol. Ugyanez a `fastembed-js`. **[Közepes]**

Ebből következik, hogy **egyetlen Bun folyamatban minden keresés blokkolja az összes többit**
a beágyazás + FTS5-lekérdezés + összefésülés idejére. Nem részlegesen: teljesen.

Ez az, ami a „100 felhasználó" kérdést eldönti — nem a fájlzár, és nem a lemez.

---

## 3. Mennyibe kerül egy beágyazás? — és mit nem tudunk

**Az egyetlen mérés, ami minden feltételét megadja** (AMD EPYC 7702P 6 mag, llama.cpp-szerver,
`wrk -t1 -c1`, GGUF Q8_0):

| Modell | Rövid lekérdezés (~5 szó) | Bekezdésnyi szöveg |
|---|---|---|
| granite-embedding-107m többnyelvű, Q8_0 | **p50 2,9 ms · p99 4,2 ms** | p50 24,4 ms · p99 32,7 ms |
| granite-embedding-278m többnyelvű, Q5_K_M | p50 12,9 ms · p99 17,3 ms | p50 198,9 ms · p99 259 ms |

*[Alacsony — személyes blog saját mérése, de minden feltételt megad, és élőben ellenőrizve.]*

A tanulság nem a konkrét szám, hanem az **arány**: a modellméret négyszerezése a rövid lekérdezésnél
4-5x-ös, bekezdésnyi szövegnél **8x-os** lassulást hozott. Egy keresőmezőbe írt kérdés rövid, tehát
a kedvező tartományban vagyunk — de a modellválasztás itt nem ízlés kérdése.

**Amit nem tudunk, és ez „bizonyított hiány", nem hiányos kutatás:** a szóba jövő modellekre
(multilingual-E5, MiniLM, BGE-M3) **senki nem publikál batch=1 CPU-késleltetést**. A közzétett
számok mind nagy kötegekre vonatkoznak, ami nem írja le az élő lekérdezési utat. **Ezt nekünk kell
lemérnünk**, nem kikeresnünk.

**Egy licenc-csapda, élőben ellenőrizve:** a **jina-embeddings-v3 CC BY-NC 4.0** — nem kereskedelmi.
Kereskedelmi használathoz a gyártót kell megkeresni. **Ezzel a modell kiesik.** A multilingual-E5
(MIT) és a BGE-M3 (MIT) marad. **[Magas]**

**A magyarról nincs adat.** Egyik modellkártya sem sorolja fel a magyart a kiemelt nyelvek közt, és
az MTEB magyar alcsoportját ez a kör nem érte el. Ez „hiányzó bizonyíték", nem bizonyított hiány —
de a saját mérésünk (`90-meresek.html`) itt többet ér, mint bármelyik leaderboard.

---

## 4. Olvasók: az SQLite oldal olcsó, ha jól állítjuk be

- **WAL módban** a doksi szó szerint: *„readers do not block writers and a writer does not block
  readers."* De ugyanaz az oldal relativizálja is: *„This is mostly true. But there are some obscure
  cases…"* — dokumentált alapelv, nem feltétel nélküli garancia. **[Magas, fenntartással]**
- **Egy író egyszerre.** A második írási próbálkozás `SQLITE_BUSY`. A `BEGIN IMMEDIATE` elkerüli az
  „olvasok, aztán írni akarok" csapdát. **[Magas]**
- **A `busy_timeout` nem mindig segít**: ha a kezelő meghívása holtponthoz vezetne, az SQLite
  **nem hívja meg**, azonnal hibát ad. Ez tudatos szabály, nem hiba. **[Magas]**
- **Checkpoint-kiéheztetés** valós: folyamatosan átfedő olvasók mellett a WAL sosem tud
  visszaíródni, és korlátlanul nő. Richard Hipp (az SQLite szerzője) szerint a leggyakoribb ok
  **egy elfelejtett, nem lezárt lekérdezés**. A `journal_size_limit` **alapértéke -1, azaz nincs
  korlát** — ezt be kell állítani. **[Magas]**
- **Egy kapcsolat nem ad párhuzamosságot.** Az alapértelmezett „serialized" szálkezelési módban egy
  kapcsolat hívásai mutexszel **sorosítva** futnak. Valódi olvasási párhuzamossághoz több kapcsolat
  kell. **[Magas]**
- **`locking_mode=EXCLUSIVE` — amit korábban fontolgattunk — itt kifejezetten káros lenne**, mert
  pont az olvasói párhuzamosságot öli meg. *(Árnyalat: egy csak-olvasó kapcsolat csak SHARED zárat
  vesz fel, ami másokat nem zár ki; a kizárás akkor lép be, amikor a kapcsolat ír is.)*

---

## 5. Az egy-írós szétválasztás mint minta

**Van neve, és valós rendszerek használják.**

- **Thompson, Single Writer Principle**: *„for any item of data, or resource, that item of data
  should be owned by a single execution context for all mutations."* És — ez a döntő —
  kifejezetten kiterjeszti szerverekre és helyi hálózatra. **[Magas]**
- **rqlite**: egyetlen vezető, a Raft-log az egyetlen hiteles írási út. **[Magas]**
- **dqlite**: *„At any time at most one write transaction can be started."* **[Magas]**
- **Litestream**: *„It runs as a separate background process…"* — tényleges külön folyamat SQLite
  mellett. **[Közepes]**

**A folyamathatár ára mérve** (1 bájtos üzenet, 1 000 000 mérés, kétmagos gép — a CPU típusa nincs
megadva, ezért ez irányszám):

| Csatorna | medián | 99. percentilis |
|---|---|---|
| Unix domain socket | 1 439 ns | 1 898 ns |
| pipe | 4 255 ns | 5 352 ns |
| TCP loopback | 7 287 ns | 8 573 ns |

**Ez a döntő arány:** a leggyorsabb folyamatközi hívás **~1,4 mikroszekundum**, a beágyazás
**~3 000 mikroszekundum**. A folyamathatár ára **a munka ezredrésze**. Vagyis a szétvágás
teljesítmény-szempontból ingyen van — az ára máshol jelentkezik.

**Ahol az ára jelentkezik — az új hibamódok:**

- **Legalább-egyszeri kézbesítés → idempotencia kell.** Az AWS SQS saját szava: *„Design your
  applications to be idempotent (they should not be affected adversely when processing the same
  message more than once)."* **[Magas]**
- **A dqlite retry-protokollja — ami pont ezt oldaná meg — a saját dokumentációja szerint
  „in progress, not released yet".** Vagyis még egy éles, komoly rendszer sem fejezte be ezt.
  **[Alacsony]** Ez józanító.

**Az ellenérv, amit külön kerestettem** — Martin Fowler, *MonolithFirst*: *„you shouldn't start a
new project with microservices, even if you're sure your application will be big enough to make it
worthwhile."* Két indok: nem tudod még, megéri-e; és a jó határokat korán szinte lehetetlen
eltalálni. Ugyanő figyelmeztet: *„Most systems acquire too many dependencies between their modules,
and thus can't be sensibly broken apart"* — vagyis **a későbbi szétvágás csak akkor olcsó, ha a
határt a monolitban is szigorúan tartod.** *(Az ellenérvnek magának is van ellenérve — a
verifikáló talált élő vitát Fowler állításáról; ezt a teljesség kedvéért írom ide.)* **[Közepes]**

---

## 6. Index-frissesség — a D-19 kérdés

**Amit a valódi keresők csinálnak: alapból NEM látszik azonnal, és ezt tudatosan vállalják.**

- **Elasticsearch**: alapértelmezett frissítési időköz **1 másodperc**. Saját szavuk: *„Unless you
  have a good reason to wait for the change to become visible, always use refresh=false (the default
  setting)."* A kényszerített frissítés áráról: *„the cost of true is paid at index time to create
  the tiny segment, at search time to search the tiny segment, and at merge time to make the larger
  segments."* **[Magas]**
- **Solr**: puha commit 10 mp / kemény commit 60 mp az ajánlott példakonfiguráció. **[Magas]**

**De ez a figyelmeztetés nagy írási forgalomra szól, nem ránk.** Nálunk az írás ritka. És az FTS5
másképp működik: minden tranzakció egy kis b-fát hoz létre, amit az `automerge` (alap 4) a háttérben
olvaszt össze — **a per-írás beszúrás olcsó**. A veszély a **`crisismerge`** (alap 16): ha túl sok
azonos szintű b-fa gyűlik össze, azonnali, **blokkoló** teljes összeolvasztás indul. Ezért a
karbantartó a `merge` paranccsal, kis lépésekben tartsa karban az indexet, ne az `optimize`-zal,
ami a doksi szerint *„Can take long time"*.

**A hibrid keresés viselkedése hiányzó lábnál:** az összefésülés nem ejti ki a dokumentumot, csak
nem kap pontot abból a lábból. **De a mi kapuzott tervünkben** a jelentés-láb az elsődleges — tehát
egy beágyazás nélküli bejegyzés **gyakorlatilag láthatatlan**, hacsak nem pont a benne szereplő
szóra keresnek. *(Ezt a következtetést a kutató vonta le a képletből; az Elastic és az Azure doksija
nem mondja ki külön mondatban — de a képletből valóban következik.)*

**Precedens fájl-alapú jegyzetrendszerekben — és ez tanulságos:**
- **Khoj**: a beágyazás **szinkronizáláskor** készül, nem mentéskor.
- **Smart Connections** (Obsidian): késleltetés beállítható („Re-import wait time"), utána háttér-
  újraszámítás, plusz kézi „Embed now" gomb és explicit **„kész / nem kész" állapotjelzés**.

**Egyik sem ígér azonnali láthatóságot mentés után.** Ez nem azt jelenti, hogy mi se tegyük — azt
jelenti, hogy ha megtesszük, jobbat adunk, mint amit ezek adnak, és tudnunk kell, mit vállalunk.

---

## 7. Docker

- **Bun saját dokumentált Dockerfile-ja** többlépcsős, `bun install --frozen-lockfile`-t használ, és
  **`USER bun`**-nal nem rootként futtat. Sorról sorra egyezik a hivatalos forrással. **[Magas]**
- **Az Alpine nem ingyen kisebb**: a Bun hivatalos Alpine Dockerfile-ja maga futtat
  `apk add libgcc libstdc++`-t, mert a bináris C++ futtatókörnyezetet igényel. *(Pontosítás egy
  verifikálótól: ezek az Alpine saját, musl-linkelt csomagjai, nem glibc — a korábbi megfogalmazás
  pontatlan volt.)* **[Közepes]**
- **A Compose `stop_grace_period` alapértéke 10 másodperc**, utána SIGKILL. Ennyi idő alatt kell a
  szervernek lezárnia az SQLite kapcsolatot és lezárnia a naplófájlt. **[Magas]**
- **Az SQLite tiltja a nyitott kapcsolat használatát `fork()` után.** *(A „worker/cluster mintákra"
  általánosítás a kutatóé; a forrás csak `fork()`-ról beszél.)* **[Magas]**
- **Hálózati fájlrendszer**: az SQLite saját figyelmeztetése áll. Docker Desktop macOS-en a
  bind mount VM-en és fájlmegosztási rétegen megy át — **konkrét dokumentált korrupciós esetet erre
  nem találtunk**, ez architekturális érv, nem incidens. Fejlesztésre elég, éles üzemre Linux.

**Egy korábbi saját állításunk megdőlt.** A `easter-decisions.md`-ben ez állt: *„az alapértelmezett
natív illesztő Bun alatt dokumentáltan törik — több független hibajegy, konténerben különösen."*
A valóság gyengébb: a konténeres hibajegyet a karbantartók **duplikátumként lezárták**, és a valódi
ok **nem adatbázis-driver hiba**, hanem CLI-félreértés: a slim/distroless kép belépési pontja már
`bun`, így egy `bun`-nal kezdődő parancs `bun bun index.js`-sé válik, amit a CLI csendben
`bun build`-ként értelmez. **Ez bármelyik beépített importot elrontja, nem csak az SQLite-ot** — és
a rendes Debian-alapú képen nem jelentkezik. **A tiltást pontosítani kell.**

---

## 8. A javaslatom

**Most: egy alkalmazás-konténer + egy beágyazó-konténer. A karbantartó és az írás nem külön app.**

Az indoklás nem az egyszerűség, hanem hogy **a szétvágást ott kell kezdeni, ahol a fal van** — és a
fal a beágyazás, nem a fájlírás. A beágyazó szolgáltatás kiemelése:

- **pontosan a szűk keresztmetszetet szünteti meg** — az eseményhurok többé nem áll meg 3-25 ms-ra
  minden keresésnél;
- **nem hoz új hibamódot**, mert a beágyazás **tiszta függvény**: nincs állapota, nincs írása, az
  újrapróbálkozás ingyen van, idempotencia-probléma nincs;
- **készen kapható** (Ollama, Infinity, text-embeddings-inference, llama.cpp-szerver) — nem mi
  írjuk;
- **egy sor a compose fájlban.**

Ezzel szemben a fájlíró kiemelése **most** minden költséget behozna (idempotencia, újrapróbálkozás,
indulási sorrend, a leállt író kezelése) azért a nyereségért, amit még nem tudunk kimutatni.

**Az írás határa viszont most kerül a helyére**, egyetlen modul mögé (`ir(utvonal, tartalom,
vartLenyomat)`), amiben a fájlonkénti sor él. Ma függvényhívás. Ha egyszer több olvasó folyamat kell
(`reusePort`, Linuxon), akkor **és csak akkor** ugyanez a hívás Unix socketen megy át a kijelölt
íróhoz — mérten a munka ezredrészének áráért. Fowler figyelmeztetése pontosan erről szól: a későbbi
szétvágás akkor olcsó, ha a határt már most is szigorúan tartjuk.

**Amit mérnünk kell, mielőtt bármit szétvágunk**, mert a szakirodalom nem adja meg:
1. a választott beágyazó modell batch=1 késleltetése a mi gépünkön, magyar lekérdezésekkel;
2. hány egyidejű keresésnél romlik el a válaszidő egy folyamaton;
3. a `reusePort` melletti olvasói skálázódás.

**A plafon egy gép**, és ezt ki kell mondani: a fájlok és az SQLite egy lemezen vannak, a WAL osztott
memóriát igényel, tehát minden folyamatnak ugyanazon a gépen kell lennie. Több gépre szétteríteni
csak az alapmodell átírásával lehetne.
