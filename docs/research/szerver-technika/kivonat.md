# Szerver-technika kutatás — kivonat

A kutatás négy témát járt körül egy Bun + TypeScript szerverhez, amely a tartalmát markdown
fájlokban tartja: (A) írási sorbaállítás fájlokra, (B) Better Auth jogosultságkezelés és
Drizzle + SQLite FTS5, (C) audit napló tárolása — ami menet közben SQLite táblából
JSON Lines fájl-alapú tervvé alakult —, és (D) a Bun/SQLite platformkérdés. 84 forrás, 148
állítás; ebből az ellenőrzés 108-at megerősített, 33-at gyengített (`partial`/`unsupported`
minősítéssel), 2-t tartalmilag megdöntött. Ez a fájl a 122 archivált oldal helyett marad meg:
a lenti idézetek mind a mentett pillanatképekből származnak, nem a szintézisből.

## A) Írási sorbaállítás fájlokra

**Amit tudunk.** Az atomikus fájlírás két, egymástól független garanciából áll össze, és
egyik sem helyettesíti a másikat. A `rename(2)` Linux man page szerint a célfájl-csere
atomikus:

> "If newpath already exists, it will be atomically replaced, so that there is no point at
> which another process attempting to access newpath will find it missing."

Ez viszont csak egy mountponton belül él — más fájlrendszerre `EXDEV` hibát ad —, és NFS-en
a man page saját BUGS szakasza figyelmeztet: ha a szerver rename közben omlik össze, az
újraküldött RPC hamis hibát adhat vissza, "you cannot assume that if the operation failed,
the file was not renamed."

A `rename` önmagában nem tartósság. Az `fsync(2)` man page (man7.org) kimondja a rést:

> "Calling fsync() does not necessarily ensure that the entry in the directory containing
> the file has also reached disk. For that an explicit fsync() on a file descriptor for the
> directory is also needed."

Ez nem elméleti hiba. Theodore Ts'o, az ext4 karbantartója, saját blogján írta le a 2009-es
esetet: az ext4 késleltetett blokk-allokálása miatt egy `rename`-nel felülírt fájl helyén
egy összeomlás után nulla hosszúságú fájl maradt. Ts'o szerint hosszú távon "application
writers who are worried about files getting lost on an unclean shutdown really should use
fsync" — de a hibát magát a 2.6.30-as kernel három patch-csel javította: rename vagy
truncate esetén a blokkallokálás azonnal megtörténik. A hiba tehát javítva van, csak a
tanulság maradt érvényes. Ugyanezt mondta ki a 2019-es LSFMM kernelfejlesztői vita (LWN
tudósítása szerint): a temp+rename "the applications often do not use fsync() correctly, so
they lose their data anyway".

macOS-en külön csapda van. Az Apple `fsync(2)` man page-ének egy tükre (nem az Apple saját
oldala) szerint:

> "While fsync() flushes data from the host to the drive, the drive itself may delay
> physically writing data to platters or write it out-of-order. ... For applications
> requiring stricter data integrity guarantees, Mac OS X provides the F_FULLFSYNC fcntl
> option."

Kész csomag mindkét réteget lefedi: az npm `write-file-atomic` README-je szerint egyedi
ideiglenes fájlnevet használ (`filename + "." + murmurhex(...)`), alapból fsync fut a
rename előtt (`fsync: Boolean, default = true`), és emellett saját, folyamaton belüli
Promise-sorral szerializálja az ugyanarra a fájlnévre irányuló írásokat: "If multiple writes
are concurrently issued to the same file, the write operations are put into a queue and
serialized in the order they were called, using Promises."

**Fájlonkénti zár, konkrét eszközök.** Az `async-mutex` README egyértelmű figyelmeztetést ad:
"Failure to call `release` will hold the mutex locked and will likely deadlock the
application." A `p-limit` README: "Avoid calling the same `limit` function inside a function
that is already limited by it. This can create a deadlock." A `mutexify` README FIFO-sorrendet
garantál: "mutexify guarantees that the order that a mutex was requested in is the order that
access will be given." Az `async-lock` `maxPending` opciója sormélység-korlátot ad a
kulcsonkénti várakozási sorra.

**A garancia határa.** A Node hivatalos `cluster` dokumentációja kimondja, hogy a workerek
külön OS-folyamatok (`child_process.fork()`), és "Node.js does not provide routing logic. It
is therefore important to design an application such that it does not rely too heavily on
in-memory data objects." A Bun `reusePort` dokumentációja ugyanezt mondja Linuxra:
"`reusePort` uses the Linux `SO_REUSEPORT` and `SO_REUSEADDR` socket options to ensure fair
load balancing across processes" — és Windows/macOS-en nincs hatása. Ebből az következik,
hogy egy folyamaton belüli mutex semmit nem ér több folyamat esetén — ez azonban **a
kutatás saját következtetése**, nem a dokumentáció állítása, amit az ellenőrzés helyesen
"partial"-ra minősített: a forrás a folyamat-szeparációt mondja ki, a mutex-érvénytelenség
levezetése tőlünk származik.

Fájlrendszerek közötti zárhoz a `proper-lockfile` tudatosan `mkdir`-alapú, mert (saját
README) "O_EXCL is broken on NFS file systems; programs which rely on it for performing
locking tasks will contain a race condition." Alapértelmezett `stale` küszöb 10 000 ms,
SIGKILL vagy VM-összeomlás után a zár nem szabadul fel automatikusan.

**Mit csinálnak a valódi rendszerek — semmit.** A Logseq egyik közreműködője (cnrpman) a
#8074 discussion-ben szó szerint leírta a mechanizmust: "This is the limitation of file
sync. It's not designed for concurrent editing. It has 20 sec of update interval." A
Logseq fórumon egy felhasználó "3-4 cases of data loss" -t jelentett egy hét alatt; egy
másik hozzászóló szerint "data loss may be way more common when using third party sync."
Egy külön GitHub-issue (#1332) szerint a Logseq oldal-létrehozáskor felülírt egy meglévő
.md fájlt ütközés-ellenőrzés nélkül — ezt az ellenőrzés T6-ra (megerősítetlen, elemző-stílusú
összefoglaló) minősítette vissza a manifest T1-es besorolásáról, mert karbantartói
megerősítés nincs a mentett szövegben.

**Ami gyengült.** A cluster/reusePort → mutex-érvénytelenség láncolat és a "before hook az
objektum-szintű ellenőrzés primitívje" jellegű mondatok mind a kutatás saját következtetései,
amiket a szöveg forrásidézetnek álcázott. Egy pillanatkép (a Logseq #7197/#8074 discussion)
eltért a rögzítéskori hash-től — ami idézhető belőle, az a fenti karbantartói válasz, ami
stílusában nem AI-összefoglaló, tehát valószínűleg valódi.

## B) Better Auth jogosultság és Drizzle + FTS5

**A határ éles.** A Better Auth `hooks` doksija kimondja: "We highly recommend using hooks if
you need to make custom adjustments to an endpoint rather than making another endpoint
outside of Better Auth" — vagyis a hookok a Better Auth saját végpontjaihoz készültek. A
`plugins` doksi ezt élesen le is zárja:

> "Unlike hooks, middleware only runs on `api` requests from a client. If the endpoint is
> invoked directly, the middleware will not run."

Az összes dokumentált hook-példa `ctx.path`-on ágazik el (`/sign-up/email`, `/reset-password`
stb.) — saját Better Auth útvonalakon. A saját forráskód (`authorization.ts`,
`better-auth/better-auth` repo) megerősíti, hogy a `requireResourceOwnership` middleware egy
darab sort tölt be és egyetlen oszlop-egyenlőséget ellenőriz:

```
const resource = await ctx.context.adapter.findOne({ model: config.model, where: [{ field: "id", value: resourceId }] });
if ((resource as Record<string, unknown>)[ownerField] !== session.user.id) { ... }
```

Nincs benne se összetett feltétel, se erőforrás-tábla, se projekt-jogosultsági modell — csak
`resource[ownerField] === session.user.id`. A Next.js integrációs oldal a saját útvonalak
védelmére `auth.api.getSession({ headers })`-t ajánl, explicit figyelmeztetéssel: "You must
always validate the session on your server for any protected actions or pages."

A szervezet-plugin `hasPermission`-je erőforrás-**típus** → akció leképezés, nem
erőforrás-**példány**. A saját doksi kódpéldája ezt mutatja:

```
await auth.api.hasPermission({ headers: await headers(), body: { permissions: { project: ["create"] } } });
```

Nincs `projectId` vagy hasonló paraméter sehol a hívásban. A `createAccessControl` statement
objektuma is típus-kulcsos (`{ project: ["create", "share", ...] }`), nem példány-kulcsos.

**Session-cache és jogosultság.** A `customSession` mezői nem kerülnek a cache-be — a saját
doksi szerint: "Session caching, including secondary storage or cookie cache, does not
include custom fields. Custom session function is called each time the session is fetched."
A cookie-cache bekapcsolt állapotában a visszavonás késik: "revoked sessions may remain
active on other devices until the cookie cache expires" — az alapértelmezett `maxAge` 5 perc
(`5 * 60` másodperc a doksi példakódjában). Egy megerősítetlen GitHub-issue (#4697, T6) szerint
a kompakt cookie-stratégia a böngésző kb. 4 KB-os cookie-korlátjába ütközik, és ekkor a Better
Auth hibát dob, nem csonkol: "Session data is too large to store in the cookie." Az issue
saját adata szerint egy tipikus ID-token ~1,5 KB, egy access token ~2 KB — vagyis a
4 KB-os plafon reálisan elérhető, ha a `customSession` sokat ad hozzá.

**Drizzle + FTS5: kézzel.** A `drizzle-orm` GitHub feature request-je (#2046, 2024. március
20., **ma is Open**, "Development: No branches or pull requests") kimondja, hogy a séma-DSL
nem tud `CREATE VIRTUAL TABLE`-t. A hivatalos SQLite FTS5-doksi (sqlite.org/fts5.html) pontosan
három triggert ír elő a külső-tartalmú szinkronizációhoz, és a törléshez különleges szintaxist:

```
CREATE TRIGGER t1_ad AFTER DELETE ON t1 BEGIN
  INSERT INTO fts_idx(fts_idx, rowid, b, c) VALUES('delete', old.a, old.b, old.c);
END;
```

Egy sqlite.org fórumbejegyzés (2022, Mark/marcardar) leírja, hogy a természetesnek tűnő, de
hibás minta (`DELETE FROM my_fts WHERE id=old.id` sima `id`-vel, `rowid` helyett) "randomly
(maybe 10% of the time) a corrupt database" eredményt adott. **Ezt a számot nem szabad
tényként kezelni**: a válaszoló SQLite-fejlesztő, Dan Kennedy, csak annyit írt, hogy "both
versions look like they should have worked to me", és több séma-részletet kért — nem
erősítette meg sem az okot, sem a 10%-ot. A `bm25()` hivatalos leírása: "numerically lower
values representing better matches" — tehát `ORDER BY bm25(tbl)` növekvő sorrendben helyes,
csökkenőben hibás lenne.

**A Bun-kockázat.** Lásd a D) pontot — ez a két téma összefonódik.

## C) Audit napló tárolása — SQLite táblából JSON Lines tervvé

**Méret nem gond, tempó igen.** A SQLite hivatalos korlát-doksija (`limits.html`): "this
gives a maximum database size of about 17.5 terabytes" (4096 bájtos lapnál), illetve "about
281 terabytes" (65536 bájtos lapnál). A fizikai plafon az fsync sebessége. A Percona
(adatbázis-gyártó) mért, néven nevezett meghajtókon:

| Eszköz | Mért ütem | Latencia |
|---|---|---|
| 7200 rpm SATA (WD2502ABYS) | 56/mp | 18 ms |
| Fogyasztói SATA SSD (Crucial) | 108/mp | 9,3 ms |
| Fogyasztói SATA SSD (Intel 520) | 2031/mp | 0,49 ms |
| Csúcs NVMe (Intel PC-3700) | 7380/mp | 0,14 ms |
| RAID + BBU (Dell Perc) | 23 000/mp | 0,04 ms |

Következtetésük: "A 7.2k RPM drive limits fully ACID transactions to ~56/second with single
connection." Ez a 2018-as mérés, de a nagyságrendi sorrend (HDD ≪ SSD ≪ NVMe ≪ BBU-RAID) fizikai
okokból ma is áll.

**WAL erre a terhelésre nem segít.** Egy 2025 végi, néven nevezett hardveren (2,4 GHz 8-magos
i9 MacBook, 32 GB RAM, Node.js + Piscina) mért benchmark szerint 1 egyidejű írónál a
DELETE-journal 496 írás/mp-et adott, WAL módban 223-at; a szerző szövege szerint "At 1 and 2
concurrent connections, writing to WAL reduces throughput by 43% and 17% respectively" — WAL
csak 4 worker fölött nyer (1510 vs. 1021 írás/mp 4 workernél). A hivatalos SQLite fórumon egy
hozzászóló (Warren Young) fizikai indoklást ad: "7200 RPM divided by 60 seconds per minute
divided by 2 rotations per transaction yields 60 transactions per second, absolute max, hard-
limited by physics." Ez a forrás T5/T6 (személyes blog, fórum), de az irányt két független,
néven nevezett hardveren mért adat is alátámasztja — nálunk egy író van, tehát a WAL nem
hoz nyereséget, csak a hálózati fájlrendszeres korlátozását.

**Sorméret-benchmark, amit nem szabad ránk vetíteni.** A `better-sqlite3` saját, hivatalos
benchmarkja (2020.03.29, "MacBook Pro (Retina, 15-inch, Mid 2014, OSX 10.11.6), using nodejs
v12.16.1", WAL módban): 62 554 egysoros beszúrás/mp, illetve "inserting 100 rows in a single
transaction: better-sqlite3 x 4,141 ops/sec". Ez a szám élőben stimmel, de **más binding**
(Node N-API addon, nem `bun:sqlite`), **más gép**, **hat éve EOL Node-verzió** — nagyságrendi
tájékozódásra jó, tervezési alapnak nem.

**Particionálás: ne.** A SQLite `ATTACH` korlátja alapból 10, kemény maximum 125 (ezt a
hivatalos `limits.html` mondja ki — a mentett pillanatkép ugyan csonka ezen a ponton, hiányzik
belőle a szakasz, de a verifikáló élőben ellenőrizte az élő oldalon). Egy harmadik féltől
származó útmutató (mako.ai, T5) szerint egy `UNION ALL` nézet nem szűri le a nem érintett
ágakat: "SQLite does not prune the `UNION ALL` branches the way a partitioned planner would" —
és ugyanez a forrás mondja ki, hogy több `ATTACH`-elt fájlra kiterjedő tranzakció WAL módban
nem garantáltan atomi. Ez utóbbit egy verifikáló élőben megtalálta a hivatalos
`sqlite.org/lang_attach.html` oldalon is, tehát a mondat áll, csak a forrás gyengébb tier-ű,
mint amit egy állítás alátámasztásához szeretnénk.

**Index és lapozás.** A hivatalos `EXPLAIN QUERY PLAN` doksi definiálja a `SCAN` (teljes
bejárás) és `SEARCH` (részhalmaz) különbséget, és a fedő index jelzését: "SEARCH t1 USING
COVERING INDEX i2 (a=?)". A `USE TEMP B-TREE FOR ORDER BY` sor a hiányzó rendező indexet
jelzi. A lapozás témában a *Use The Index, Luke* (Markus Winand, T3) mondja ki a
determinisztikus rendezés szükségességét: "Paging requires a deterministic sort order", és
adja a sor-érték szintaxist a döntetlen-feloldáshoz (`WHERE (SALE_DATE, SALE_ID) < (?, ?)`).
Az ehhez tartozó teljesítmény-ábra a forrásban **kvalitatív**, hardver és sorszám nélkül — a
mechanizmus (OFFSET lineárisan drágul, seek nem) áll, a konkrét szám nem forrásolható.

**Törlés, tömörítés.** A hivatalos SQLite VACUUM-doksi: "as much as twice the size of the
original database file is required in free disk space", és az `auto_vacuum` ára "extra
database file fragmentation". A `zstd` saját README-je (Core i7-9700K, Ubuntu 24.04,
lzbench, Silesia korpusz): zstd -1 2,896:1 arány 510 MB/s tömörítéssel, zlib -1 2,743:1 arány
105 MB/s-mal — ez általános szöveges korpuszon mért szám, nem ismétlődő JSON naplón, a valós
audit-naplón az arány valószínűleg jobb, de ezt a kutatás nem mérte.

**Megőrzési idő — nincs szám, ami minket kötelezne.** Az ISO 27001:2022 A.8.15 kontroll teljes
szövege ennyi: "Logs that record activities, exceptions, faults and other relevant events
should be produced, stored, protected and analysed." Nincs benne szám. A gyakran idézett
"12 hónap" egyetlen tanácsadói FAQ saját válasza (hightable.io): "There is no single mandated
period, but 12 months is the industry standard 'rule of thumb'" — ezt a mondatot az
ellenőrzés **lefokozta**, mert a "több forrás egybehangzó" framing helytelen: csak ez az egy,
hivatkozás nélküli oldal mondja. A NIS2 rendelet (CIR 2024/2690, 3.2.5. szakasz) saját szövege
szintén nem ad számot: "CIR Section 3.2.5 does not specify a minimum retention duration.
Neither does the NIS2 Directive itself" — a gyakran hallott "12 hónap (6+6)" és "18 hónap"
egy megfelelőségi tanácsadó cég saját ajánlása, nem jogszabályszöveg. A SOC 2 kritériumok nem
írnak elő időtartamot, csak azt, hogy a szervezet definiálja a sajátját. Egyedül a PCI DSS
ad tényleges számot: "the audit history should be kept for at least one year and at least
three months immediately available for analysis." A GDPR 5. cikk (1)(e) a másik irányba
korlátoz: a személyt azonosító adat "no longer than is necessary for the purposes."

**Referencia egy valódi rendszerre.** A HashiCorp Vault saját doksija szerint az audit
alrendszer fail-closed: "Vault sends the audit log entry of every API request and response
to all enabled audit devices and guarantees that it saves to at least one of the enabled
devices" — és ha minden eszköz elérhetetlen, "Vault effectively becomes unavailable." A
fájl-alapú eszköz szándékosan minimális: "This is a very simple audit device: it appends logs
to a file", nincs beépített rotáció — "we recommend using existing tools" —, és `SIGHUP`
zárja-nyitja újra a fájlt rotációhoz.

**A JSON Lines-fordulat konkrét technikai anyaga.** A hivatalos JSON Lines specifikáció:
egy sor egy JSON érték, UTF-8, záró sortörés ajánlott, de nem kötelező. Az NDJSON spec (v1.0.0)
szigorúbb: "The JSON texts MUST NOT contain newlines or carriage returns", és kötelező
UTF-8-at ír elő — de ez a különbség csak az NDJSON saját szövegéből adódik, a JSON Lines-
specifikációval való összevetést a kutatás maga tette hozzá, nem forrásolt idézet. A
Kubernetes saját audit-doksija JSON Lines formátumú fájlba ír, a jsonlines.org-ra hivatkozva
mint formátum-tekintélyre. A Bun `Bun.write`/`FileSink` API-ja nem dokumentál `O_APPEND`
módot, `fsync`/`O_DSYNC` opciót; a `.flush()` a doksi szövege szerint "write buffer to disk"
— ez a doksi saját szóhasználata, ami erősebb garanciát sugall, mint amit egy sima OS-puffer
flush ténylegesen ad; ezt a részletet a doksi nem hedgeli, tehát a "csak az OS-puffort éri
el, nem a lemezt" olvasat **ütközik** a forrás szó szerinti szövegével, és emiatt bizonytalan
marad, mit garantál valójában a `.flush()`. A hivatalos POSIX write(2) szöveg (IEEE Std
1003.1-2017) az `O_APPEND` atomicitását írja le: "the file offset shall be set to the end of
the file prior to each write and no intervening file modification operation shall occur" — ez
a garancia egy géprendszeren belül él, NFS-en a kliens kernel csak szimulálja. A PostgreSQL
hivatalos doksija a fsync-kikapcsolás kockázatát mondja ki: "this can result in unrecoverable
data corruption in the event of a power failure or system crash", míg a
`synchronous_commit=off` enyhébb: "does not create any risk of database inconsistency... some
recent allegedly-committed transactions being lost."

Sok-fájlos (egy fájl/nap vagy egy fájl/felhasználó) elrendezésnél két konkrét korlát merül
fel. A Linux `auditd.conf(5)` man page a `flush`/`freq` és `max_log_file`/`num_logs`
paraméterekkel írja le az fsync-ütemezést és a rotációt. Az ext4 hivatalos kernel.org
dokumentációja szerint a könyvtár hasított b-fája (htree) mélysége kemény korlátos: "Cannot
be larger than 3 if the INCOMPAT_LARGEDIR feature is set; cannot be larger than 2 otherwise"
— ez korlátozza, hány bejegyzést tud egy könyvtár hatékonyan indexelni, mielőtt
alkönyvtárakra kellene bontani. A systemd-journald man page konkrét számot ad egy
sok-streames tervhez: "the number of parallel log streams systemd-journald will accept is
limited to 4096." Egy sidecar-index minta (zindex projekt saját README-je) szerint egy
egyszerű numerikus index mérete "typically about 10% of the compressed file's size."

## D) Bun/SQLite platformkérdés (és a Docker-hiány)

**Ez a kampány legkellemetlenebb találata.** A Bun hivatalos `bun:sqlite` doksija kimondja:

> "macOS: Bun uses the system-provided SQLite, which Apple builds with persistent WAL
> enabled. ... Linux and Windows: Bun statically links its own SQLite build, which follows
> upstream defaults."

Ugyanez a doksi mondja ki, hogy Apple saját SQLite-buildje nem tölt be kiterjesztéseket
("macOS ships with Apple's proprietary build of SQLite, which doesn't support extensions"),
és a `Database.setCustomSQLite(path)` a dokumentált kerülőút — de "on other operating
systems, this is a no-op", és a `.dylib` fájlra kell mutatnia, nem a futtatható állományra.

Egy nyitott, felhasználó által bejelentett hibajegy (#31247, 2026. május 23., macOS 15.5
arm64, Bun 1.3.14 és 1.4.0-canary) saját reprodukciós kóddal dokumentálja, hogy a
`sqlite_version()` 3.43.2-t ad vissza a blogban ígért 3.53.0 helyett, és ez a régi verzió az
FTS5-nél korrupciót okoz:

```
db.run('UPDATE docs SET content = ? WHERE id = ?', ['c', 1]);
// Throws: database disk image is malformed, errno: 267
```

Az issue élő állapota (2026-09-05-i élő lekérdezéssel ellenőrizve): Open, nulla komment,
nincs karbantartói válasz, nincs csatolt PR — "The 'Development' section explicitly states
'No branches or pull requests.'" Ez tehát **megerősítetlen** felhasználói bejelentés (helyes
tier: T6, nem a manifestbe eredetileg került T1), de a reprodukciós kód konkrét és
ellenőrizhető.

**Hogy az FTS5 egyáltalán be van-e fordítva** — erre a Bun dokumentációja sehol nem felel:
végignézve a `sqlite`-doksi teljes szövegét, az "FTS5" kifejezés egyszer sem fordul elő a
törzsszövegben. Ez "evidence of absence": kerestük, nincs ott. Ugyanakkor egy karbantartói
PR (#37045, 2026.08.06, szerző: robobun, egy másik nyitott hiba — a `close()`-kori
use-after-free — javítására) a leírásában FTS5-specifikus kódra hivatkozik
(`sqlite3Fts5IndexClose`, `fts5DisconnectMethod`), ami közvetett, de karbantartói szintű
bizonyíték arra, hogy az FTS5 ténylegesen be van fordítva és tesztelve Bun oldalán — csak a
doksi hallgat róla.

**A "Docker" kérdésről.** A feladatleírás e témát "Docker és a Bun/SQLite platformkérdés"
címkével adta, de **a vault-ban egyetlen Docker-releváns forrás sincs** — sem a
`02-sources/manifest.jsonl`-ben, sem egyetlen kereséssorban a `01-search-log/queries.jsonl`-
ben. Amit a kutatás ténylegesen körüljárt, az a Bun/SQLite operációs rendszer szerinti
eltérése (macOS rendszer-SQLite vs. Linux saját build), nem a konténerizáció mint olyan. A
"szerver Linuxon fusson" javaslat (SZINTEZIS 2.5/3) implicit módon konténerizációval is
elérhető, de ezt egyetlen forrás sem mondja ki — ez tiszta hiány, nem a kutatás
elmulasztása, hanem olyasmi, amit soha nem kerestek.

## Amire ez a kutatás nem ad választ

**Bizonyított hiány (kerestük, nincs ott):**
- Hivatalos állítás arról, hogy az FTS5 be van-e fordítva a Bun SQLite-jába — nincs, sem a
  renderelt, sem a nyers doksiforrásban.
- Egyetlen vizsgált markdown-rendszer (Logseq, Joplin, Obsidian, Outline, Decap CMS,
  SilverBullet) sem használ tartalom-lenyomatos írási előfeltételt.
- Better Auth sehol nem mondja ki explicit módon, hogy a jogosultságkezelés nem az ő
  felelőssége — ez a dokumentált minta hiányából (nincs "Protecting Resources" oldal, minden
  hook `ctx.path`-hoz kötött) következik, nem egy kimondott mondatból.

**Kifutott a kutatási keretből (lehetne még keresni):**
- A Docker/konténerizáció mint téma — soha nem indult el rá keresés.
- A stabil Bun 1.4 (2026.08.20) tartalmazza-e a 2026.08.06-i FTS5-segfault javítást — a PR
  aznap mergelt, de a release-hez kötést nem ellenőriztük.
- Mért többletköltség hash-láncolt (tamper-evident) audit naplóra — az immudb "milliós
  tranzakció/mp" állítása gyártói marketingszöveg, hardver és konfiguráció nélkül.
- Kemény, hardverrel dokumentált OFFSET vs. keyset lapozás-benchmark SQLite-on — a mechanizmus
  forrásolt, a szám nem.
- Konkrét bájt/sor becslés a tényleges audit-sémára indexekkel együtt — a szerkezeti alapadat
  (varint fejléc + oszloponkénti típuskód) megvan, magát a számítást a kutatás nem végezte el.
- A TiddlyWiki MultiWikiServer ETag/If-Match írási előfeltétele nem lett megerősítve — ha
  létezik, ez lenne az egyetlen talált precedens a tartalom-lenyomatos írásra.
- Dendron, Zettlr, Foam konkurenciakezelése — egyetlen kör sem jutott rá.

## Amit a kutatás önmagáról derített ki

A záró minőségellenőrzés (`finalize.py`, 2026-09-05) szerint: **143/148 idézet pontos (97%),
4 összefűzött, 1 nem található**; ellenőrzési lefedettség 86% (21 állítás a záró hullám után
született gap-körből, ellenőrizetlen maradt); minden hivatkozott link élt a záráskor.

**Két állítás elvesztette a valódi forrását rögzítési hiba miatt.** A mentő eszköz két
GitHub-issue-nál nem az oldalt mentette el, hanem egy AI-generált összefoglalót róla —
felismerhető jelekkel: `## Issue Summary`, `## Critical Impact`, harmadik személyű elbeszélés
("The reporter encountered..."). Az egyik érintett a Bun FTS5-hibajegy volt (#31247) — ezt
szigorúbb, összefoglalás-ellenes prompttal újra rögzítették, és a második változat már valódi
oldalszöveg (lásd fent, teljes reprodukciós kóddal). A másik érintett, egy Better Auth
`hasPermission`-hibajegy, rögzítetlen maradt, mert a döntés nem múlott rajta.

**Rendszeres, egyirányú forrásminősítési hiba.** A tekintélyesnek látszó, de nem lektorált
források rendre túl magas tiert kaptak:

| Forrás típusa | Kapott | Helyes | Ok |
|---|---|---|---|
| Apple man page GitHub Pages-tükre | T2 | T5–T6 | magánszemély tükre, a tartalom hű, de nem elsődleges |
| use-the-index-luke.com | T3 | T4 | egyszemélyes szakmai oldal |
| sqlite.org fórumbejegyzések | T1 | T6 | a domain hivatalos, a tartalom egy felhasználó anekdotája |
| GitHub hibajegyek (több, pl. #1332, #3235, #7822) | T1 | T6 | bejelentő ≠ karbantartó, megerősítés nélkül |
| better-sqlite3, zstd, sqlite.org saját benchmarkjai | T1 | T4 | gyártó a saját termékéről |

Ez az az aszimmetria, amire a kutatási protokoll figyelmeztet: a domain neve (`sqlite.org`,
`github.com`) nem minősítés, a tartalom típusa igen.

**Egy konkrét vault-hiba, amit érdemes tudni:** az `sqlite.org/limits.html` mentett
pillanatképe csonka — hiányzik belőle az `ATTACH`-korlátokról szóló szakasz (10 alapból, 125
kemény maximum). Az élő oldalon megvan, egy verifikáló élőben ellenőrizte, ezért az állítás a
szintézisben állva maradt — de ha valaki csak a pillanatképre hagyatkozna, hamis
"unsupported" eredményt kapna.

**Számok, amiket nem szabad tényként idézni a jövőben:**
- "Az FTS5 hibás trigger-minta 10%-ban okoz korrupciót" — a bejelentő saját, hedgelt becslése,
  a válaszoló SQLite-fejlesztő ("both versions look like they should have worked to me") nem
  erősítette meg sem az okot, sem a számot.
- "12 hónap az ISO 27001 ipari szabványa" — egyetlen, hivatkozás nélküli tanácsadói FAQ-mondat.
- "NIS2: 12 vagy 18 hónap" — tanácsadó cégek saját ajánlása, nem a rendelet szövege (a
  rendelet és az irányelv saját szövege nem ad számot).
- A `better-sqlite3` 4 141 tranzakció/mp — valódi szám, de 2020-as, más binding, más gépen mérve.

Összesen 148 állításból 108 áll megerősítve, 33 gyengült ("partial" vagy "unsupported"
minősítést kapott — ezek közül egyik sem volt puszta rögzítési hiba, hanem valódi
túlállítás: a forrás kevesebbet mond, mint amit az eredeti megfogalmazás sugallt), 2 dőlt meg
tartalmilag. A jelen kivonat mindenütt jelezte, melyik állítás melyik kategóriába esik.
