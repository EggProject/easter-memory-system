# Skálázás — kutatási kivonat

Forrás: 67 archivált weboldal-pillanatkép, 105 idézett állítás, teljes verifikáció
(`04-citations/verdicts.jsonl`). A kérdés: mi történik 100 egyidejű felhasználónál, és szét kell-e
választani a fájlírót a karbantartótól. A rendszer: Bun + TypeScript, egy cég egy példány, Docker,
egy gép; markdown a forrás igazság; eldobható SQLite index (FTS5 + embedding); tartós SQLite a
jogosultságoknak; fájl-alapú JSONL audit log.

Ez a dokumentum a nyers forrásokra megy vissza, nem a szintézis átfogalmazása. Ahol egy állítást a
verifikáció gyengített (`partial`), az itt is gyengítve szerepel.

---

## 1. Bun eseményhurka és HTTP-konkurencia

A `Bun.serve` elfogadja a párhuzamos kapcsolatokat, de a kérdés az, mi történik a kérés
*feldolgozása* alatt. Három hivatalos dokumentációs tény együtt dönti el a sorsát.

**A `bun:sqlite` szinkron.** Bun saját szava:

> „The API is synchronous and fast."

A `Statement` osztály `all()`, `get()`, `run()`, `values()` metódusai sima értéket adnak vissza, nem
Promise-t — tehát a hívás a hívó szálon, azaz az egyetlen kérés-feldolgozó eseményhurkon fut le, és
addig blokkolja azt.

**A `Worker` API kísérleti.** Bun saját dokumentációja:

> „The Worker API is still experimental (particularly for terminating workers). We are actively
> working on improving this."

Ez az egyetlen dokumentált mód processzoridő-igényes munka kiszervezésére a kérés útjából — és a
gyártó saját szava szerint nem termelésre kész.

**A folyamaton belüli beágyazó könyvtárak blokkolnak.** A `transformers.js` saját doksija:

> „When running in node, we use `onnxruntime-node`."

Az ONNX Runtime saját dokumentációja pedig:

> „By default with intra_op_num_threads=0 or not set, each session will start with the main thread
> on the 1st core (not affinitized). Then extra threads per additional physical core are created…"

— és pár sorral lejjebb: „along with the main calling thread, there will be three threads in total
to participate in intra-op computation." A szál-készlet tehát felgyorsítja az *egy* számítást, de a
hívó nem kap vissza irányítást, amíg az véget nem ér. Ugyanez igaz a `fastembed-js`-re: natív ONNX
Runtime kötéseket használ, folyamaton belül, szinkron módon.

**Következmény:** egyetlen Bun folyamatban a beágyazás-számítás + FTS5-lekérdezés + összefésülés
idejére minden más keresés vár — nem részlegesen, teljesen. Ez a kampány fő találata: nem a
fájlzár és nem a lemez a szűk keresztmetszet, hanem az eseményhurok.

**Ami erről nem áll rendelkezésre feltételekkel:** Bun saját reklám-táblázata („roughly 2.5x more
requests per second than Node.js on Linux") hardver és konkurencia-szint nélkül közölt szám — a
verifikáció T1-ről T4-re minősítette vissza, mert ez a gyártó saját, ellenőrizetlen mérése önmagáról.
Egy független, teljes feltétellel megadott benchmark (AMD 5900X, `hey`, Node 22.9 vs Bun 1.0.28,
DB-hátterű terheléssel) elhanyagolható különbséget talált — Bun előnye csak triviális „hello world"
végponton jelenik meg. A `reusePort`, Bun dokumentált módja több folyamat indítására egy gépen,
**csak Linuxon működik** — Windows és macOS figyelmen kívül hagyja az `SO_REUSEPORT` opciót
(man7.org, operációs rendszeri korlát).

---

## 2. SQLite olvasási konkurencia és WAL

**Az alapelv igaz, de feltétellel.** A WAL dokumentáció fő állítása:

> „WAL provides more concurrency as readers do not block writers and a writer does not block
> readers."

Ugyanaz az oldal, néhány szakasszal lejjebb, relativizálja:

> „This is mostly true. But there are some obscure cases where a query against a WAL-mode database
> can return SQLITE_BUSY, so applications should be prepared for that happenstance."

Ez nem ellentmondás, hanem elhallgatott feltétel — tervezési elvnek jó, feltétlen garanciának nem.

**Egy író egyszerre — WAL módban is.** „However, since there is only one WAL file, there can only
be one writer at a time." A második írási kísérlet `SQLITE_BUSY`-t kap. Az `SQLITE_BUSY`
dokumentáció szerint ez „az esettel, amikor mindkét folyamat írni próbál" foglalkozik, és a
`BEGIN IMMEDIATE` áthelyezi ezt a kockázatot a tranzakció elejére: onnantól a `COMMIT`-ig nem jön
többé `SQLITE_BUSY`.

**A `busy_timeout` nem old meg mindent.** A callback-dokumentáció:

> „If SQLite determines that invoking the busy handler could result in a deadlock, it will go
> ahead and return SQLITE_BUSY to the application instead of invoking the busy handler."

Ez tudatos tervezési döntés, nem hiba.

**Checkpoint-kiéheztetés valós kockázat.** „if a database has many concurrent overlapping readers
and there is always at least one active reader, then no checkpoints will be able to complete and
hence the WAL file will grow without bound." Egy valós SQLite-fórum bejegyzésben Richard Hipp (a
projekt vezető karbantartója) tisztázta, hogy „COMMIT does not cancel a pending read transaction -
it merely downgrades a write transaction into a read transaction" — egy el nem engedett,
`sqlite3_reset()`-tel le nem zárt prepared statement önmagában is kiéheztetheti a checkpointot
(ez az idézet degradált, fórum-paraprafázis-környezetű pillanatkép). A `journal_size_limit`
alapértéke „-1 (no limit)" — ezt explicit be kell állítani, különben a napló korlátlanul nőhet.

**Egy kapcsolat nem ad valódi párhuzamosságot.** Az alapértelmezett szálkezelési mód „serialized":
„The name 'serialized' arises from the fact that SQLite uses mutexes to serialize access to each
object" — valódi olvasói párhuzamossághoz több kapcsolat kell.

**`locking_mode=EXCLUSIVE` — árnyalattal.** A verifikáció pontosított egy korábbi állítást: a
`PRAGMA` dokumentáció szerint EXCLUSIVE módban a kapcsolat „never releases file-locks", de a teljes
kizárás **csak az első írástól** lép életbe (EXCLUSIVE zár). Egy csak-olvasó kapcsolat EXCLUSIVE
módban is csak SHARED zárat vesz fel, ami **nem zár ki más olvasókat** — „multiple SHARED locks can
coexist". A korábbi, „ez mindenkit kizár" megfogalmazás túl erős volt az olvasó-only esetre.

---

## 3. A beágyazás valódi ára — és amit nem tudunk

**Az egyetlen mérés minden feltétellel megadva** (paulw.tokyo, személyes blog, 2025-09-14; AMD EPYC
7702P, 6 mag; llama.cpp szerver; `wrk -t1 -c1`, azaz gyakorlatilag sorosított, batch=1-szerű
terhelés; GGUF Q8_0/Q5_K_M kvantálás):

| Modell | „short" (~5 szó) p50 / p99 | „paragraph" p50 / p99 |
|---|---|---|
| granite-embedding-107m többnyelvű, Q8_0 | 2,9 ms / 4,2 ms | 24,4 ms / 32,7 ms |
| granite-embedding-278m többnyelvű, Q5_K_M | 12,9 ms / 17,3 ms | 198,9 ms / 259,0 ms |

A szerző saját szava: „The larger models can only handle a small load on this machine, but the
100M parameters one can already run at about 50 rps/core on short queries and 6 rps/core on more
substantial chunks of text." Fontos: ez **T5-ös** forrás (személyes blog), és **nem** a kutatás
célmodelljeire (multilingual-E5, MiniLM, BGE-M3) vonatkozik, hanem hasonló méretű IBM granite /
Google EmbeddingGemma modellekre, llama.cpp/GGUF alatt, nem `transformers.js`/ONNX-ben.

**Elvetett számok — és miért.** Két mérést a kampány tudatosan nem használt fel. Egy 2024-es
Hugging Face/Intel blogbejegyzés „under 1% accuracy loss" és „up to 4.5x latency speedup, under
20ms" számokat közöl kvantált BGE-modellekre Intel Xeonon, de a befogás nem őrizte meg, melyik
BGE-mérethez, CPU-hoz, szálszámhoz, szekvenciahosszhoz és kötegmérethez tartoznak — **eldobva,
feltétel nélkül nem idézhető.** A Hugging Face Infinity 2022-es „1-4ms latency for sequences up to
64 tokens" száma DistilBERT **osztályozásra** vonatkozik (nem beágyazásra), és a termék „no longer
offered as a commercial inference solution" 2022 decembere óta — csak nagyságrendi tájékozódásra
tartható meg.

**A bizonyított hiány: senki nem publikál batch=1 CPU-késleltetést a szóba jövő modellekre.** A
multilingual-E5, MiniLM és BGE-M3 modellkártyák (Hugging Face) méretet, dimenziót, licencet és
nyelvi lefedettséget adnak meg, de éles, egyesével érkező lekérdezésre vonatkozó látenciát egyik sem.
A `fastembed-js` olvasónaplója például kötegelt API-t dokumentál 256-os alapértelmezett
kötegmérettel — ez nem írja le az élő keresőmezőbe írt, egyesével érkező lekérdezést. **Ezt saját
méréssel kell pótolni**, nem tovább keresni.

**Egy licenc-csapda.** A jina-embeddings-v3 modellkártya:

> „The model operates under CC BY-NC 4.0 licensing, with commercial usage requiring contact with
> Jina AI."

Ezt élő újralekérdezéssel is megerősítették — a modell kereskedelmi használatra emiatt kiesik. A
multilingual-e5-small/base és a BGE-M3 kártyák szerint a licenc MIT — ezek maradnak versenyben.
(Az e5-kártyák dimenzió/paraméterszám adatai a verifikáció szerint csak a befogó ügynök
táblázat-átfogalmazásából származnak, nem szó szerinti README-idézetből — valószínűek, de nem
igazoltak; a nyelvi lefedettség és az 512 tokenes csonkítási határ viszont szó szerint idézett.)

**A magyar nyelvről nincs adat.** Egyik modellkártya sem sorolja fel a magyart kiemelt nyelvként; az
e5-base kártya csak annyit mond, hogy „100 languages from xlm-roberta, but low-resource languages
may see performance degradation" — a magyar besorolása ebbe a kategóriába nem tisztázott a
forrásokból.

---

## 4. Egy-írós minta és a folyamathatár ára

**A döntő önkorrekció.** Az egyik kereső ügynök azt rögzítette, hogy Thompson „Single Writer
Principle"-e szálakra/végrehajtási kontextusokra vonatkozik, és a nyeresége folyamathatáron nem
érhető el, mert memóriabarrierre (nem kölcsönös kizárásra) épül. Ez a szűkebb olvasat a
szétválasztás ellen szólt volna. **Két verifikáló egymástól függetlenül, élő szövegellenőrzéssel**
megcáfolta ezt. Thompson eredeti szövege, a „The Principle at Scale" szakaszból:

> „This principle works at all levels of scale. […] CPU cores are just nodes of execution and the
> cache system provides message passing for communication. **The same patterns apply if the
> processing node is a server and the communication system is a local network.** If a service, in
> SOA architecture parlance, is the only service that can write to its data store it can be made to
> scale and perform much better. […] Encapsulation has just been broken at a more macro level when
> multiple different services write to the same data store."

A feloldás: a szűkebb állítás **az LMAX Disruptor konkrét, lock-free, megosztott memóriás
technikájára** igaz (ahol tényleg memóriabarrier helyettesíti a zárat), nem magára az elvre, amit
Thompson kifejezetten kiterjeszt szerver- és hálózati határokra. A kereső a kettőt összemosta. A
tanulság: a szétvágásnak van elvi, nem csak megtűrt, támogatása.

**Valós rendszerek ugyanezt teszik.** rqlite: „Only one node can bootstrap a cluster, so any other
node that attempts to do so later will fail, and instead become a Follower in the new cluster" —
a Raft-log az egyetlen hiteles írási út. dqlite: „At any time at most one write transaction can be
started"; egy második próbálkozás `SQLITE_BUSY`-val bukik. Litestream: „It runs as a separate
background process and continuously copies write-ahead log pages from disk to a replica" — valódi
külön folyamat SQLite mellett.

**A folyamathatár ára mérve** (kamalmarhubi.com, 2015, saját kétmagos/4-szálas géppel — a CPU
pontos típusa nincs megadva, ezért ez csak irányszám, nem géptől független abszolút érték; 1 bájtos
üzenet, `clock_gettime`/`CLOCK_MONOTONIC`, 1 000 000 mérés):

| Csatorna | medián (ns) | 99. percentilis (ns) |
|---|---|---|
| Unix domain socket (`af_unix`) | 1439 | 1898 |
| pipe | 4255 | 5352 |
| TCP loopback (`af_inet_loopback`) | 7287 | 8573 |

A szerző saját szava: „the biggest surprise was how much faster UNIX domain sockets were than
anything else." A döntő arány: a leggyorsabb IPC-hívás ~1,4 mikroszekundum, a beágyazás fentebb
mért 2,9–25 ezredmásodperc — a beágyazás ezerszer drágább, mint a folyamathatár átlépése. A
szétvágás teljesítmény-szempontból gyakorlatilag ingyen van.

**Az ára máshol jelentkezik — a hibamódokban.** AWS SQS saját dokumentációja: „Design your
applications to be idempotent (they should not be affected adversely when processing the same
message more than once)" — a legalább-egyszeri kézbesítés idempotenciát követel. A dqlite
retry-protokollja, ami pont ezt oldaná meg vezetőváltáskor, saját dokumentációjában a szakaszcím
szerint „Client sessions (in progress, not released yet)" — egy éles, forgalomban lévő elosztott
SQLite-rendszer sem fejezte még be ezt.

**Az ellenérv.** Martin Fowler, *MonolithFirst*: „you shouldn't start a new project with
microservices, even if you're sure your application will be big enough to make it worthwhile" —
és lábjegyzetben: „Most systems acquire too many dependencies between their modules, and thus
can't be sensibly broken apart." Fowler nem azt mondja, *hogyan* válaszd szét (arról Thompson
beszél), hanem *mikor*: korán nem tudod, megéri-e, és a jó határokat korán nehéz eltalálni. A
későbbi szétvágás csak akkor olcsó, ha a határt a monolitban is szigorúan tartod. (Fowler
állításának van dokumentált élő vitája is — nem egyhangú álláspont, de ezt a kör nem dolgozta fel.)

---

## 5. Index-frissesség

**A nagy keresőmotorok tudatosan nem ígérnek azonnali láthatóságot.** Elasticsearch: „Unless you
have a good reason to wait for the change to become visible, always use refresh=false (the default
setting)" — alapértelmezett frissítési időköz 1 másodperc. A kényszerített frissítés ára
háromszorosan jelentkezik: „the cost of true is paid at index time to create the tiny segment, at
search time to search the tiny segment, and at merge time to make the larger segments." Solr
hasonlóan: puha commit ajánlott intervalluma „often 15-60 seconds is reasonable."

**Ez a figyelmeztetés nagy írási forgalomra szól, nem a mi esetünkre.** Az FTS5 másképp épül fel:
minden tranzakció egy kis b-fát hoz létre, amit az `automerge` (alapérték 4, max 16) a háttérben
összeolvaszt. A veszély a `crisismerge` (alap 16): ha túl sok azonos szintű b-fa gyűlik össze,
azonnali, blokkoló teljes összeolvasztás indul. Az `optimize` parancs dokumentált figyelmeztetése:
„the optimize command can take a long time to run" — ezért ajánlott helyette a `merge` parancsot kis
lépésekben futtatni. (Mindkét FTS5-pillanatkép degradált befogás: a folyó szöveg átfogalmazott, csak
a számszerű alapértékek és a kódrészletek megbízhatóak szó szerint.)

**Precedens fájl-alapú rendszerekben.** Khoj: „When you sync you documents with Khoj, it uses the
bi-encoder model to create and store meaning vectors of (chunks of) your documents" — a beágyazás
szinkronizáláskor készül, nem mentéskor. Smart Connections (Obsidian-bővítmény): „Time in seconds
to wait before re-importing a file after modification", majd kézi „Embed now" gomb és explicit
változás-számláló. Egyik sem ígér azonnali láthatóságot mentés után; ha a tervezett rendszer ezt
megteszi, jobbat ad, mint a bevett gyakorlat, de vállalnia kell a `crisismerge` blokkoló kockázatát.

---

## 6. Docker, Bun, SQLite

**A hivatalos Dockerfile-ok jónak bizonyultak.** A Bun saját dokumentált többlépcsős Dockerfile-ja
`bun install --frozen-lockfile`-t futtat és nem rootként fut. Az Alpine-alapú hivatalos image maga
is muszáj hogy telepítse a C++ futtatókörnyezetet: `apk add libgcc libstdc++` a végső fázisban — az
Alpine tehát **nem ingyen kisebb**. A Debian-alapú image dedikált, nem-root felhasználót hoz létre
(`useradd bun --uid 1000`).

**Pontosítás egy külön hibajegyről (#29681):** egy nyitott, „needs triage" jegy szerint a Bun
musl-címkéjű bináris ténylegesen dinamikusan linkeli a `libstdc++`/`libgcc`-t, és csupasz Alpine-on
„Error loading shared library libstdc++.so.6" hibával fut el, amíg ezeket apk-val fel nem
telepítik — ugyanaz a lépés, amit az oven-sh hivatalos Alpine Dockerfile-ja már tartalmaz. A
verifikáció pontosított egy megfogalmazást: ezek **Alpine saját, musl-hoz linkelt** csomagjai, nem
glibc — a „glibc-függőség" a befogó ügynök saját, pontatlan értelmezése volt.

**Egy korábbi saját feljegyzés megdőlt.** A projekt korábbi jegyzete szerint „az alapértelmezett
natív illesztő Bun alatt dokumentáltan törik — több független hibajegy, konténerben különösen." A
valóság gyengébb. A konkrét konténeres hibajegy (#26228) a distroless image-en „Browser build
cannot import Bun builtin: 'bun:sqlite'" hibát mutatott, és a karbantartók **duplikátumként
lezárták** a #25925 jegy javára. A gyökér-ok CLI-félreértés: a slim/distroless image belépési
pontja már `bun`, így egy `CMD ["bun", "index.js"]` ténylegesen `bun bun index.js`-ként fut le,
amit a CLI csendben `bun build`-ként (böngésző-célú csomagolásként) értelmez — a jelentő szava
szerint ez „just cost me half a day". **A gyökér-jegy (#25925) maga továbbra is nyitott**, „needs
triage" címkével: a duplikátumot lezárták, de a mögöttes CLI-viselkedést nem javították. A hiba
bármelyik beépített importot elrontja, nem kizárólag a `bun:sqlite`-ot, és a rendes (nem
slim/distroless) Debian-alapú képen nem jelentkezik.

**Leállási határidő.** A Compose specifikáció `stop_grace_period` alapértéke dokumentáltan 10
másodperc, utána SIGKILL jön: „The default value is 10s." Ennyi idő alatt kell a szervernek
lezárnia az SQLite-kapcsolatot és flush-olnia az audit-naplót.

**Fork és hálózati fájlrendszer.** Az SQLite hivatalos korrupciós-okok dokumentuma kifejezetten
tiltja: „Do not open an SQLite database connection, then fork(), then try to use that database
connection in the child process" (a worker/cluster-mintákra való általánosítás a kutatóé, a forrás
csak a `fork()`-ról beszél), és külön nevesíti az NFS-t mint gyakori törött-zárolás forrást.
**Konkrét, dokumentált korrupciós esetet Docker Desktop macOS fájlmegosztására nem találtunk** —
ez architekturális érv (VM + fájlmegosztási réteg közbeiktatása), nem incidens-bizonyíték.

---

## Amire ez a kutatás nem ad választ

**Bizonyított hiány — mérni kell, nem tovább keresni:**

1. **Batch=1 CPU-késleltetés a szóba jövő beágyazó modellekre** (multilingual-E5, MiniLM, BGE-M3).
   Minden publikált szám kötegelt feldolgozásra vonatkozik (a fastembed-js alap kötegmérete 256),
   ami nem írja le az egyesével érkező élő lekérdezést. Ez a kampány legnagyobb, tudatosan nyitva
   hagyott hiánya.
2. **Magyar nyelvű visszakeresési minőség** ezekre a modellekre — egyik modellkártya sem sorolja
   fel a magyart, az MTEB magyar alcsoportját ez a kör nem érte el.
3. **Dokumentált SQLite-korrupciós incidens Docker Desktop macOS fájlmegosztásán** — nem található,
   csak architekturális érv.
4. **`text-embeddings-inference` és a `llama.cpp`-szerver saját konkurencia-dokumentációja** — ez
   dönti el, melyik kész beágyazó szolgáltatást érdemes választani; ezt a kör nem dolgozta fel.
5. Egy teljes FTS5-újraépítés ideje a saját korpuszon, ami megmutatná, mennyire súlyos egy
   index-hiba — nem mérték.

**Amit a következő körben mérni kell:** a választott modell batch=1 késleltetése a célgépen magyar
rövid lekérdezésekkel; hány egyidejű keresésnél romlik el a válaszidő egy Bun-folyamaton; az olvasói
skálázódás `reusePort` mellett.

## Amit a kutatás önmagáról derített ki

A minőségellenőrzés (QA.md) szerint mind a 105 állítás idézete szó szerint visszakereshető volt a
pillanatképekben (100%), és minden hivatkozás élőnek bizonyult újralekérdezéskor. Ugyanakkor:

- **17 állítást a verifikáció gyengített** (`partial`): a befogó ügynök szó szerinti idézet mellé
  saját értelmezést vagy táblázat-átfogalmazást fűzött, amit utólag nem lehetett igazolni (pl. az
  e5-modellek dimenziószáma, a fastembed-js „in-process" jellege). A tényanyag többsége igaz
  élő újraellenőrzéssel, de a megfogalmazás pontossága sérült.
- **Tier-inflálás 6 esetben**: az automatizált befogás T1-nek minősített olyan tartalmat, ami
  valójában T4 (gyártó ellenőrizetlen önreklámja, pl. a Bun rps-szám) vagy T5 (személyes blog,
  pl. Thompson bejegyzése).
- **Egyetlen forrásra támaszkodó, load-bearing állítások**: a beágyazás-költség egyetlen teljes
  feltétellel megadott mérése (paulw.tokyo) és a Thompson-idézet is egyetlen T5-ös blogból
  származik — élőben megerősítve, de független második forrás nélkül.
- Két FTS5-pillanatkép **degradált befogású**: a számértékek megbízhatóak, a folyó szöveg csak
  valószínűsítve az.
