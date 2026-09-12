# Hiányok — amire nem találtunk választ

Kampány: `adatbazis-illeszto` · 2026-09-09


---

## SQ-01 — Melyik illesztési minta, és hol a varrat

# SQ-01 — Hiányok (gaps)

A módszertan szerint minden hiánynál jelezve van, hogy **"absence of evidence"** (még
nem találtuk meg, más szögből érdemes keresni) vagy **"evidence of absence"** (megnéztük
ott, ahol szükségszerűen lennie kellene, és nincs ott — ez maga egy eredmény).

---

## 1. Eric Evans DDD-könyvének szó szerinti Repository-szövege — **absence of evidence
(eszköz-korlát, nem tartalmi hiány)**

Két elsődleges forrásból (a hivatalos, ingyenes DDD Reference PDF a domainlanguage.com-on,
illetve a teljes könyv egy harmadik féltől hosztolt PDF-je) próbáltuk kinyerni Evans
saját, szó szerinti Repository-definícióját. **Mindkét esetben a WebFetch-eszköz
megtagadta a szó szerinti reprodukálást**, szerzői jogi okra hivatkozva (a PDF-eket
feldolgozó kis modell saját döntése, nem a forrás blokkolása vagy elérhetetlensége — a
tartalom technikailag elérhető volt, csak a modell nem volt hajlandó szó szerint
visszaadni).

**Ez nem azt jelenti, hogy a tartalom nem létezik vagy nem érhető el** — csak azt, hogy
*ennek az ügynöknek, ezzel az eszközkészlettel, ebben a körben* nem sikerült hozzáférnie
szó szerint. Amit tudunk helyette: egy másodlagos blog (mikehadlow.blogspot.com)
állítólagosan szó szerint idéz négy pontot és egy tranzakciós elvet a könyvből — ezt
`Kozepes` bizonyossággal, forrás-kettős-áttétellel kezeltük.

**Javasolt következő lépés:** (a) próbálja meg egy másik ügynök/eszköz (pl. böngésző-
alapú fetch, vagy a könyv nyomtatott/legális e-könyv példányának közvetlen idézése emberi
felügyelettel); (b) az InfoQ Eric Evans-interjú (https://www.infoq.com/interviews/eric-
evans-ddd-interview) potenciálisan tartalmaz Evans saját szavaival megfogalmazott
Repository-magyarázatot, szerkesztett interjú formában, ami kevésbé eshet szerzői jogi
akadályba — ezt ebben a körben nem próbáltuk ki.

---

## 2. Greg Young "DDD: The Generic Repository" (2009) — **absence of evidence
(hozzáférési akadály)**

Az eredeti codebetter.com-os bejegyzés ma már nem érhető el közvetlenül (a blog
platformja megszűnt/átalakult). A Wayback Machine-en át próbált elérés
**`SITE_BLOCKED`** hibát adott — ezt log-oltuk (`01-search-log/blocked.jsonl`), és a
módszertan előírása szerint **nem kerültük meg** curl-lal vagy más eszközzel.

Ez az egyik leggyakrabban hivatkozott korai (2009-es) kritika kifejezetten a
**generikus** (`IRepository<T>`) Repository-implementáció ellen — a mai vita nagy része
erre az írásra vezethető vissza, de a szöveget magát nem sikerült ellenőriznünk.
`megallapitasok.md`-ben ezért csak *másodlagos* hivatkozásként (mikehadlow blogja
linkeli) szerepel, nem önálló, ellenőrzött forrásként.

**Javasolt következő lépés:** másik Wayback-pillanatkép (más év/hónap), vagy a
Google cache, vagy azonosítani egy olyan másodlagos forrást, amely hosszabban,
idézőjelesen idézi Young eredeti szövegét.

---

## 3. AI-átfogalmazás mint visszatérő kockázat ebben a körben — **módszertani
megfigyelés, nem tartalmi hiány, de befolyásolja a bizonyossági szinteket**

Ebben a kutatási körben **ismételten** előfordult, hogy a WebFetch-eszköz nem a valódi
oldalszöveget adta vissza szó szerint, hanem egy kitalált fejezetcímekkel
("Overview", "Key Problems", "Core Principle" stb.) tagolt, AI-átfogalmazott verziót —
annak ellenére, hogy a prompt kifejezetten szó szerinti, nem összefoglalt szöveget kért.

**Érintett fetchek, ahol ez megtörtént (első próbálkozásra):**
- `martinfowler.com/eaaCatalog/tableDataGateway.html` — **javítva**, második,
  szigorúbb prompttal kereszt-ellenőrzött, végül megbízható.
- `www.domainlanguage.com/ddd/reference/` — **nem javítva**, nem használtuk fel
  forrásként a szigorú szabály szerint ("ha egy fetch AI-összefoglalót ad vissza, ne
  használd forrásként — jelöld a gaps.md-ben").
- `www.odbms.org/.../Neward...pdf` (Vietnam of Computer Science) — **javítva**,
  második, célzottabb prompttal kereszt-ellenőrzött, végül megbízható és szó szerinti.
- `docs.nestjs.com/techniques/sql` — valószínűleg **nem** érintett (a hosszú, részletes,
  kódblokkokkal teli válasz jellege arra utal, hogy ez a lekérés ténylegesen a valódi
  oldalszöveget adta vissza), de nem lett kereszt-ellenőrizve második lekéréssel.
- `codeopinion.com/avoiding-the-repository-pattern-with-an-orm/`,
  `codeopinion.com/do-you-really-need-that-abstraction-or-generic-code-yagni/`,
  `www.oracle.com/java/technologies/dataaccessobject.html`,
  `refactoring.guru/smells/speculative-generality`,
  `martinfowler.com/bliki/Yagni.html`,
  `www.thereformedprogrammer.net/is-the-repository-pattern-useful-with-entity-framework/`
  — mindegyik AI-átstrukturált választ adott. Ezeket **felhasználtuk**, de:
  - csak az idézőjelbe tett mondatokat kezeltük lehetséges szó szerinti idézetként
    (`[VERBATIM-BIZONYTALAN, Kozepes]`),
  - minden más állítást parafrázisnak jelöltünk, a forrás szerzőjéhez kötve, nem szó
    szerinti forrásszövegként.

**Ez fontos jelzés a szintézis-fázis számára**: ezekben az esetekben a `Magas`
bizonyossági szint nem indokolt pusztán a forrás T1-es tier-je alapján — a
*fetch-módszer* korlátozza a bizonyosságot, függetlenül a forrás presztízsétől. Két
T1-es forrás (Oracle DAO-oldal, Fowler Yagni-oldal) is csak `Kozepes` szintre kerülhet
emiatt, amíg második, kereszt-ellenőrző lekérés nem történik.

---

## 4. "Repository vs DAO vs Data Mapper vs Gateway" — nincs egyetlen dedikált,
egyértelmű forrás — **absence of evidence**

Ez a kör nem talált olyan T1-T2 forrást, amely egy helyen, explicit módon
szembeállítaná mind a négy fogalmat. A `megallapitasok.md` 2. szakaszában bemutatott
különbségtétel **a mi rekonstrukciónk** a Fowler-katalógus egymás mellé olvasásából és az
Oracle DAO-leírásból, nem egyetlen forrás kimondott állítása.

**Javasolt következő lépés:** Vaughn Vernon "Implementing Domain-Driven Design" könyve
(gyakran hivatkozzák mint a DDD tactical patterns legrészletesebb, gyakorlatorientált
tárgyalását) potenciálisan tartalmaz ilyen explicit összehasonlítást — ezt a kört nem
sikerült elérnie.

---

## 5. A 7. alkérdés (egy vagy két port a keresési index és az adattár számára) —
**evidence of absence**

Két célzottan megfogalmazott keresés (`searches.md` 17. tétele, és rokon
próbálkozások a keresési eredmények átolvasásakor) nem hozott olyan forrást, amely
kifejezetten erről a konkrét szituációról (eldobható keresési index vs. nem eldobható
adattár, közös vagy külön port) szólna. Ez azok közé a helyek közé tartozik, ahol egy
ilyen forrásnak — ha létezne — tipikusan elő kellett volna kerülnie (hexagonal
architecture gyakorlati útmutatók, "how many ports" jellegű cikkek), ezért ezt
**evidence of absence**-ként, nem "még nem kerestük eléggé"-ként rögzítjük.

A `megallapitasok.md` 7. szakaszában bemutatott válasz Cockburn általános elvének
(portok célja szerint, nem technológia szerint particionálandók) **extrapolációja** erre
a konkrét esetre — ez a mi következtetésünk, `Vitatott` jelöléssel, nem egy forrás
kimondott állítása.

---

## 6. Drizzle / Kysely saját állásfoglalása a repository/data-access mintázásról —
**nem kutatott, hatókör-döntés**

A feladatkiírás 6. pontja kifejezetten a NestJS/Drizzle/Prisma/Kysely "környékét" kérte.
Ebben a körben **csak NestJS hivatalos dokumentációját** kerestük meg és fetcheltük;
Drizzle és Kysely saját dokumentációját **nem néztük meg célzottan** a repository-
mintázás kérdésében, mivel a szülő-terv (`00-plan.md`) "Hatókörön kívül" szakasza
kizárja "Konkrét ORM kiválasztása (a Drizzle a D-12-vel eldőlt)" tárgykört. Utólag
átgondolva ez **túl szigorú értelmezés** lehetett — a D-34 ténylegesen Drizzle-lel
valósul meg, tehát releváns lehet, mit *mond* a Drizzle dokumentáció a rétegződésről
(nem melyik ORM-et válasszuk, hanem hogyan rétegezzünk rá egy már eldöntött ORM esetén).
**Javasolt következő lépésként rögzítve**, nem pótoltuk utólag ebben a körben a
tool-budget miatt.

---

## 7. Az N+1/lusta-betöltés-szivárgás mért, számszerűsített dokumentálása —
**absence of evidence**

A kérdés kifejezetten kérte a "leaky abstraction" és N+1 probléma dokumentált eseteit.
Amit találtunk (Comartin cikke), az gyakorlói *állítás* a jelenség létezéséről, nem mért
benchmark vagy esettanulmány számokkal. Ebben a körben nem kerestünk kifejezetten
"N+1 query benchmark measurement" vagy hasonló, számszerűsítést ígérő kifejezéssel — ez
**absence of evidence**, nyitott maradt egy következő körnek.

---

## 8. Fowler 2021-es, bővített Gateway-cikke — **alacsony prioritású, nem pótolt hiány**

A PoEAA Gateway-oldal saját maga jelzi, hogy 2021-ben Fowler írt egy jobb, részletesebb
magyarázatot (`martinfowler.com/articles/gateway-pattern.html`). Ezt nem fetcheltük,
mert az alapdefiníció a kérdés megválaszolásához elegendőnek bizonyult, és a
tool-budget nagy részét más, kritikusabb hiányok zárására fordítottuk.


---

## SQ-02 — Párhuzamosság és tranzakciók motorok között

# SQ-02 — Hiányok (gaps)

A módszertan szerint minden hiánynál jelezve van, hogy **"absence of evidence"** (még
nem találtuk meg, más szögből érdemes keresni) vagy **"evidence of absence"** (megnéztük
ott, ahol szükségszerűen lennie kellene, és nincs ott — ez maga egy eredmény).

---

## 1. Drizzle ORM SQLite-specifikus tranzakció-konfigurációs felülete — **absence of
evidence, magas prioritású, mert ez a rendszer saját ORM-je**

A hivatalos `orm.drizzle.team/docs/transactions` oldal fetchje csak egy Postgres-specifikus
`PgTransactionConfig` interfészt hozott vissza (`isolationLevel`, `accessMode`,
`deferrable`). A fetch-eszköz saját megjegyzése szerint a lekért tartalom **nem
tartalmazott** SQLite-specifikus tranzakciós viselkedést vagy motorok közti
összehasonlítást.

**Ez nem azt jelenti, hogy Drizzle-nek nincs SQLite-specifikus tranzakció-kezelése** —
csak azt, hogy *ez a fetch* nem hozta felszínre. A Drizzle SQLite-adaptere (better-sqlite3
és libsql driverek felett) valószínűleg maga is dönt DEFERRED/IMMEDIATE kérdésben (ahogy a
Prisma is, dokumentáltan, 3.2 pont) — ez **kritikus, megválaszolatlan kérdés a D-34
tervezéshez**, mert a rendszer ténylegesen Drizzle-t fog használni.

**Javasolt következő lépés**: közvetlenül a Drizzle SQLite-specifikus doksi-oldalát
(`orm.drizzle.team/docs/get-started/sqlite-new`, vagy a `drizzle-orm/src/sqlite-core/
README.md` a GitHub-on) kellene megnézni, célzottan a `db.transaction()` SQLite-driver
melletti viselkedésére és arra, van-e mód a BEGIN módjának (DEFERRED/IMMEDIATE/EXCLUSIVE)
explicit beállítására a Drizzle API-n keresztül.

---

## 2. Berenson et al. (1995) — csak egyetlen, nem-kanonikus forrás, nincs kereszt-
ellenőrzés — **módszertani hiány, nem tartalmi**

Az alapmű pontos szövegét csak egy CMU-kurzus által hosztolt PDF-másolatból sikerült
lekérni (`cs.cmu.edu/~15721-f24/papers/Critique_of_ANSI_Isolation_Levels.pdf`), nem a
kanonikus Microsoft Research vagy ACM SIGMOD Record oldalról (mindkettő valószínűleg
paywall/absztrakt-only). A fetch emellett **[FETCH-ÓVATOSSÁG]**-jelöléssel bír, mert a
visszaadott tartalom láthatóan át volt strukturálva (a cikk eredeti szakaszcímei helyett
olyan címekkel, mint "Discussion of Ambiguity in P1", amik nem a cikk saját szerkezete).

A megkapott idézetek tartalma **konzisztens** azzal, ahogy ezt a klasszikus cikket az
adatbázis-szakirodalom széles körben, gyakran idézi (a P0-P3 jelenség-definíciók jól
ismertek), de **ebben a körben nem történt független, második-forrású kereszt-
ellenőrzés**.

**Javasolt következő lépés**: egy második fetch a `researchgate.net` vagy
`semanticscholar.org` verzióról, vagy — még jobb — a `dl.acm.org/doi/abs/10.1145/
568271.223785` oldalról (ha elérhető a teljes szöveg), a P0-P3 definíciók szó szerinti
összevetésére.

---

## 3. Jakarta Persistence (JPA) hivatalos specifikáció-szövege — **absence of evidence,
tudatos hatókör-döntés a tool-budget miatt**

A JPA specifikáció saját szavaival (nem a Hibernate mint egy konkrét implementáció
doksijával) mondhatná ki a legpontosabban, mit NEM szabványosít az izolációs szintekről —
ez erősebb bizonyíték lenne, mint egy implementáció doksija, mert a *szabvány*
hallgatásáról szólna, nem egy gyártó döntéséről. A keresés megtalálta a spec URL-jét
(`jakarta.ee/specifications/persistence/3.0/jakarta-persistence-spec-3.0.html`), de a
tool-budget nagy részét más, konkrétabb hiányok (Django ticket, Ecto, Hibernate Locking
fejezet) pótlására fordítottuk.

**Javasolt következő lépés**: a spec `javax.persistence.EntityManager`/tranzakció-kezelés
fejezetének fetchelése, célzottan arra, mond-e bármit az izolációs szintről (a szerzők
várakozásunk szerint valószínűleg egyáltalán nem tesznek ilyen normatív állítást, ami
maga is fontos "evidence of absence" lenne, de ezt nem ellenőriztük).

---

## 4. Kysely issue #877 karbantartói válasza — **absence of evidence, technikai
akadály**

A fetch csak az issue címét, az eredeti posztot és a címkéket (`postgres` is köztük) adta
vissza — a tényleges karbantartói diszkussziót (miért nem/hogyan valósítható meg
READ ONLY/DEFERRABLE motorfüggetlenül) a fetch-eszköz nem szolgáltatta, feltehetően mert a
GitHub-oldal renderelt tartalma (kommentek) JavaScript-tal töltődik be, amit az egyszerű
markdown-konverzió nem követ le teljesen.

**Javasolt következő lépés**: a GitHub API-n keresztüli lekérdezés
(`api.github.com/repos/kysely-org/kysely/issues/877/comments`), ami nyers JSON-t adna
vissza a kommentekkel együtt, megkerülve a renderelési problémát.

---

## 5. Konkrét, számszerűsített teljesítmény-összehasonlítás (DEFERRED vs IMMEDIATE
tranzakciók, mennyi az "elrejtés ára") — **absence of evidence**

A megállapítások (3.2, 7. pont) kvalitatívan leírják, hogy a Prisma "mindig IMMEDIATE"
döntése egy teljesítmény-kompromisszum, de **egyetlen forrás sem ad számot** arra, mekkora
ez a kompromisszum (pl. hány százalékkal csökken az egyidejű, csak-olvasó tranzakciók
áteresztőképessége, ha minden tranzakció IMMEDIATE-tel indul DEFERRED helyett). A
tenthousandmeters.com blog ad informális számokat (70k-100k tranzakció/mp), de nem
DEFERRED-vs-IMMEDIATE összehasonlításra, hanem általános írási áteresztőképességre.

**Javasolt következő lépés**: célzott keresés "SQLite BEGIN IMMEDIATE vs DEFERRED
benchmark performance" jellegű kifejezésekkel, vagy a Fly.io / Turso (SQLite-alapú
felhő-szolgáltatók, akik pont ezzel a problémával foglalkoznak üzemi léptékben) saját
mérnöki blogjainak átnézése.

---

## 6. Rokon Django-ticketek (#29062, #9409) — **absence of evidence, nem fetchelve**

Két másik Django hivatalos ticket cím alapján ugyanerre a jelenség-családra utal
("database table locked errors" LiveServerTestCase-szel; korai "OperationalError:
database is locked" multiprocessing-gel), de egyiket sem fetcheltük ebben a körben, mert a
#29280-as ticket már önmagában elég erős, részletes bizonyítékot adott a 6. pontra, és a
tool-budgetet inkább a szélesség (több különböző ORM/adatréteg lefedése) felé irányítottuk
a mélység helyett ugyanazon egy jelenségen belül.

---

## 7. AI-átfogalmazás mint ismétlődő kockázat ebben a körben is — **módszertani
megfigyelés, befolyásolja a bizonyossági szinteket**

Ahogy az SQ-01 kör `gaps.md`-je is jelezte, ebben a körben is **több alkalommal**
előfordult, hogy a WebFetch-eszköz nem a valódi oldalszöveget adta vissza szó szerint,
hanem egy kitalált fejezetcímekkel tagolt, átstrukturált verziót, annak ellenére, hogy a
prompt kifejezetten szó szerinti, teljes szöveget kért.

**Érintett fetchek ebben a körben** (mindegyiknél `[FETCH-ÓVATOSSÁG]` jelölés a
`megallapitasok.md`-ben):
- `martinfowler.com/eaaCatalog/unitOfWork.html`
- `cs.cmu.edu/~15721-f24/papers/Critique_of_ANSI_Isolation_Levels.pdf`
- `sqlite.org/whentouse.html` (részben — "Key Content" digest formában jött vissza)
- `docs.sqlalchemy.org/en/20/core/connections.html`
- `docs.sqlalchemy.org/en/20/dialects/sqlite.html`
- `knexjs.org/guide/transactions.html`
- `docs.hibernate.org/orm/5.2/userguide/html_single/chapters/portability/Portability.html`
  (ez a legszélsőségesebb eset — a fetch egyáltalán nem adott vissza tartalmat, csak egy
  "ez nincs benne" jelentést; NEM tudjuk biztosan, hogy az oldal tényleg nem tartalmazza a
  keresett anyagot, vagy a fetch-eszköz kis modellje egyszerűen nem találta meg/foglalta
  össze hibásan. **Evidence of absence helyett inkább absence-of-evidence-nek kezelendő.**)
- `orm.drizzle.team/docs/transactions` (a Drizzle-gap forrása, ld. 1. pont fent)

**Nem érintett (a válasz jellege — hosszú, tagolt, sok pontos idézőjeles mondat — arra
utal, hogy valószínűleg valódi szó szerinti tartalmat kaptunk, bár második, kereszt-
ellenőrző fetch nem történt)**:
- `www.sqlite.org/lang_transaction.html` — teljes, jól tagolt, a hivatalos oldal ismert
  szerkezetét pontosan követő válasz.
- `www.sqlite.org/wal.html` — ugyanígy, plusz a válasz explicit idézte a saját magát
  ("Key Excerpt on Single Writer Restriction" záró szakasz), ami arra utal, hogy a
  fetch-modell tudatosan kiemelte, nem csak parafrazálta a forrást.
- `www.sqlite.org/lockingv3.html`, `www.sqlite.org/isolation.html` — hosszú,
  részletgazdag, a hivatalos oldal ismert tartalmával egyező válaszok.
- `www.prisma.io/docs/orm/prisma-client/queries/transactions` — rendkívül hosszú,
  kódblokkokkal, táblázatokkal teli válasz, ami a valódi oldal ismert szerkezetét pontosan
  követi (nincs kitalált átcímkézés).
- `docs.djangoproject.com/en/6.1/ref/databases/` — ugyanígy, a Django doksi ismert
  szerkezetét pontosan követő, hosszú válasz.
- `code.djangoproject.com/ticket/29280` — a Trac-ticket jellegzetes formátumát követi,
  konkrét névvel azonosított hozzászólókkal.
- `www.doctrine-project.org/.../transactions.html`, `api.rubyonrails.org/.../
  Optimistic.html`, `docs.hibernate.org/orm/5.2/.../Locking.html` — mind rövidebb, de
  konkrét, ellenőrizhető idézetekkel.

**Ez fontos jelzés a szintézis-fázis számára**: a `[FETCH-ÓVATOSSÁG]`-gal jelölt
forrásoknál a `Magas` bizonyossági szint nem indokolt pusztán a forrás T1-es tier-je
alapján, ahogy az SQ-01 gaps.md is megállapította ugyanezt a saját körére.


---

## SQ-03 — Szöveges és vektoros keresés hordozható felület mögött

# SQ-03 — Hiányok és le nem zárt szálak

## AI-összefoglalót / üres vázat visszaadó fetch-ek (nem használtuk forrásként)

A skill szabálya szerint ha egy fetch a valódi oldal helyett AI-összefoglalót vagy üres
navigációs vázat ad vissza, azt nem szabad forrásként felhasználni. Ez a kör a következő
oldalaknál futott bele ebbe, és egyiket sem vettük fel a `links.md`/evidence table-be:

- **`https://qdrant.tech/documentation/concepts/search/`** — a WebFetch üres tartalmat
  jelzett ("the webpage content provided is empty"). Helyette a
  `qdrant.tech/documentation/search/search/` URL-t találtuk meg (WebSearch-ből), ami már
  tartalmat adott — ez lett a forrás.
- **`https://qdrant.tech/documentation/concepts/filtering/`** — a WebFetch azt jelezte,
  hogy az oldal nem tárgyalja explicit a pre/post-filtering kérdést, csak a szűrő-
  szintaxist. Helyette a `qdrant.tech/articles/vector-search-filtering/` cikket
  használtuk (T2, vendor-cikk, nem a core docs).
- **`https://docs.opensearch.org/latest/vector-search/ai-search/hybrid-search/index/`**
  (kétszer is, redirect után is) — a WebFetch csak navigációs menüt/meta-leírást adott
  vissza, a tényleges dokumentáció-szöveget nem. **Ez konkrét hiány**: az OpenSearch
  hibrid keresés normalizáló logikájának (min-max, L2, RRF-kombináció) saját
  dokumentációját nem sikerült elolvasni ebben a körben, pedig ez közvetlen,
  elsődleges bizonyíték lett volna a 7. kérdésre (a pontszám-alapú fúzió miért igényel
  motoronkénti normalizálást, szemben az RRF-fel).
- **`https://docs.opensearch.org/latest/vector-search/ai-search/hybrid-search/
  normalization-processor/`** — 404-oldal jött vissza.
- **`https://weaviate.io/developers/weaviate/config-refs/distances`** — csak a
  redirect-információt adta vissza a WebFetch, a tényleges tartalmat nem; a
  redirect célját (`docs.weaviate.io/...`) külön kellett lekérni, ami már sikerült.
- **`https://typesense.org/docs/latest/api/documents.html#ranking-and-relevance`** és
  **`https://typesense.org/docs/latest/api/search.html#ranking-and-relevance`** —
  mindkétszer a Typesense doksi-honlap navigációs váza jött vissza, nem a horgonyzott
  szekció tartalma. A helyes URL-t (`typesense.org/docs/guide/ranking-and-relevance.html`)
  WebSearch-csel találtuk meg, az már sikeres volt.
- **`https://www.elastic.co/guide/en/elasticsearch/guide/current/scoring-theory.html`**
  (Elasticsearch: The Definitive Guide, "Theory Behind Relevance Scoring" fejezet) —
  ezt sikeresen lekértük, DE (a) a WebFetch nem a szó szerinti oldalszöveget, hanem egy
  átstrukturált összefoglalót adott vissza, és (b) tartalmilag a Lucene *klasszikus*
  TF/IDF-modelljét írja le (a BM25 előtti alapértelmezettet) — emiatt **szándékosan nem
  vettük fel forrásként**: elavult lenne, és a kért explicit "a pontszám nem abszolút/nem
  összemérhető" mondat nem volt benne a kapott kivonatban.

## Explicit hiányzó bizonyítékok (a forrás nem mondta ki, amit kerestünk)

- **SQLite FTS5 `bm25()` — nincs explicit mondat az összemérhetetlenségről.** A hivatalos
  sqlite.org/fts5.html oldal kimondja a pontszám *irányát* (kisebb = jobb) és a formula
  változóit (korpusz- és lekérdezés-függő IDF, átlaghossz), de nem tartalmaz egyetlen
  mondatot sem arról, hogy a kapott érték más lekérdezésekhez/táblákhoz nem hasonlítható.
  Ez **hiányzó explicit forrás**, a `megallapitasok.md` 2.3 pontjában a kutatás saját,
  formulából levezetett következtetéseként van jelölve, nem idézetként.
- **MySQL InnoDB pontos relevancia-képlete.** A lekért `fulltext-search.html` oldal nem
  tartalmazta, hogy az InnoDB BM25-variánst vagy klasszikus TF/IDF-et használ-e — ez a
  `fulltext-fine-tuning.html` aloldalon lehet, amit ez a kör nem nyitott meg.
- **Weaviate exact-vs-approximate nyilatkozata.** Csak a távolságmértékek oldalát kértük
  le sikeresen; a Weaviate saját "brute force vs. HNSW" vagy hasonló doksioldalát nem
  találtuk/nyitottuk meg ebben a körben, így a Weaviate hiányzik az 5.1 pont
  pontos/közelítő táblázatából.
- **sqlite-vec pontos-vs-közelítő nyilatkozata.** A raw README fetch nem hozott elő
  explicit "brute-force" vagy "exact search" mondatot (a projekt más ismert
  jellemzője — hogy nincs ANN-indexe, csak lineáris keresés — közismert a
  közösségben, de ebben a körben elsődleges forrásból nem sikerült megerősíteni).
- **Milvus és Qdrant konkrét távolságmérték-listája** (a lekért oldalak az
  index-típusokra, ill. az exact/approximate paraméterre fókuszáltak, nem a
  metrika-listára) — az 5.3 táblázatban üresen maradt cellák jelzik.
- **SQL:2023 vektor-típus hiányának megerősítése T1/T2 forrásból.** Csak Wikipedia-
  összefoglalót (T5) sikerült felhasználni; egy hivatalos ISO-dokumentumot vagy
  adatbázis-szakértői (pl. modern-sql.com, Markus Winand) elemzést, amely
  kifejezetten megerősítené a vektor-típus hiányát, nem sikerült elérni (az ISO
  katalógusoldalak fizetősek).

## Absence of evidence vs. evidence of absence

- **"Gyakorlói bukás-beszámoló egy keresés-absztrakcióról"** — ez `absence of evidence`:
  három különböző kereséssel (leaky abstraction ES/Solr, Haystack abandoned, Spring Data
  Elasticsearch leaky) sem került elő dedikált beszámoló. Lehet, hogy a műfaj tényleg
  ritka (a fejlesztők inkább a hivatalos doksiban dokumentálják a korlátokat, nem külön
  posztban panaszkodnak róla — ez maga is érdekes megfigyelés), vagy más
  keresési szavakkal/nyelven elő lehetne keríteni. **Nem kezeljük evidence of absence-
  ként**, mert nem jártuk körbe kimerítően (pl. Hacker News/Reddit közvetlen keresését
  nem futtattuk le ebben a körben, csak generikus WebSearch-öt).
- **"Közös vektor-kliens API-szabvány"** — ez inkább `evidence of absence`-hez közelít:
  a keresés (ann-benchmarks, SQL:2023, gyártói vektor-kiterjesztések) konzisztensen azt
  mutatta, hogy a terület jelenleg gyártónkénti szigetekből áll, és nem került elő
  semmilyen jel arra, hogy létezne egy komolyan vett, több gyártó által elfogadott
  közös felület-kísérlet. Ezt a `megallapitasok.md` 6. pontja evidence-of-absence-ként
  kezeli, de fenntartással (l. "Mi az, amiben nem" szakasz).

## Amit egy következő kör érdemes lenne megnyitnia

- OpenSearch normalization-processor doksi (más útvonalon vagy később, amikor a
  WebFetch/oldal already-cache-elt verziója esetleg jobban renderelődik).
- MySQL `fulltext-fine-tuning.html` (InnoDB relevancia-képlet részletei).
- Weaviate saját "exact search" / "brute force vs ANN" doksioldala.
- sqlite-vec dokumentációs honlapja (`alexgarcia.xyz/sqlite-vec/`), nem csak a GitHub
  README, a pontos/közelítő kérdés tisztázásához.
- Hacker News / Reddit közvetlen keresése "search abstraction" bukás-történetekre.
- Milvus/Qdrant saját metrika-lista oldalai (`milvus.io/docs/metric.md`, ill. Qdrant
  megfelelő doksioldala).


---

## SQ-04 — Hogyan tartható őszinte egy illesztő

# SQ-04 — Hiányok és le nem zárt szálak

## Blokkolt/nem használható fetch-ek

- **`https://github.com/rails/rails/tree/main/activerecord/test/cases`** —
  `ROBOTS_DISALLOWED`. A GitHub könyvtárlistázó ("tree") nézetei robots.txt által
  blokkoltak, míg az egyes fájlok ("blob"/"raw" nézet) ugyanazon a domainen sikeresen
  lekérhetők voltak (l. `README.dialects.rst` és `test_case.rb` sikeres lekérése).
  **Konkrét hiány**: nem tudtuk megnézni, van-e az ActiveRecord `test/cases`
  könyvtárban egy explicit, névvel ellátott "shared examples"/"adapter conformance"
  almodul a fő `test_case.rb`-n túl — csak azt tudjuk, hogy a fő alaposztály és az öt
  adapter-scope-olt alosztály hogyan néz ki.
- **`https://wiki.c2.com/?SubclassToTestAntiPattern=`** — a WebFetch nem a valódi
  tartalmat adta vissza, hanem egy üres, JavaScript-igényről szóló vázat
  ("JavaScript required to view this site"). A skill szabálya szerint ez **nem**
  használható forrásként. **Konkrét hiány**: ez lett volna a felhasználó által kért
  "subclass-to-test-interface" fogalom legközvetlenebb, kanonikus tárgyalása — csak a
  *létezését* tudjuk dokumentálni (a keresési találat címéből és Rainsberger válasz-
  jellegű előadás-címéből), a benne foglalt érvelést nem.
- **`https://online-training.jbrains.ca/courses/36224/lectures/2957384`** ("Why I Don't
  Consider Subclass to Test An Anti-Pattern") — fizetős kurzus-tartalom, a kör nem
  próbálta megnyitni (feltételezhetően authentikációt igényel, ami a WebFetch
  korlátain kívül esik). Csak a cím és a téma ismert, az érvelés nem.

## Tartalmi hiányok — amit kifejezetten kerestünk, de nem találtunk

- **Nincs konkrét, névvel azonosítható nyílt forráskódú esettanulmány** arra, hogy egy
  *formális, több-implementációs, közös szerződés-tesztkészlet* (SQLAlchemy-, Ecto- vagy
  ActiveRecord-stílusú dialect/adapter compliance suite) **konkrétan elfedett volna egy
  motorkülönbséget, ami éles környezetben eltört**. A talált legjobb bizonyíték (Neon
  vendor-blog, dev.to postmortem) egy szorosan rokon, de nem azonos mintára vonatkozik:
  "teszt-motor (SQLite) vs. éles-motor (PostgreSQL)" eltérés, nem "N regisztrált adapter
  közös kontraktus-tesztje ellen lefuttatva". Ez **evidence of absence** a kör keresési
  költségvetésén belül, nem feltétlenül azt jelenti, hogy ilyen eset sosem történt —
  csak azt, hogy nyilvánosan, könnyen kereshető formában nem dokumentálták így.
- **Nincs empirikus (mért) anyag** arra, hogy megtérül-e egy port/adapter-réteg előre
  történő megépítése egyetlen jelenlegi implementációhoz. A specifikusan erre irányuló
  keresés (`empirical study cost of abstraction layer...`) kizárólag véleményblogokat
  hozott (Medium, személyes blogok, T0/T6 szint), amiket nem vettünk fel forrásként. Ezt
  a `megallapitasok.md` 6.1 pontja explicit, "nem szépítve" rögzíti.
- **A Kohavi et al. tanulmány** (amit Fowler saját YAGNI-esszéjében idéz, "csak 1/3-a a
  Microsoft-funkcióknak javította a célzott metrikát") **nem lett elsődleges forrásból
  ellenőrizve** ebben a körben — a Fowler-oldalon lévő link
  (`ai.stanford.edu/~ronnyk/ExPThinkWeek2009Public.pdf`) létezik és lett linkként
  rögzítve (`05-links.jsonl`-ben, a ContractTest/Yagni capture automatikus link-
  kinyerésén keresztül), de a PDF tartalmát nem nyitottuk meg — ez a kör másodkézből,
  Fowler összefoglalásán keresztül idézi az adatot. Ha a szintézis ezt az adatot
  Magas bizonyossággal akarja használni, a PDF-et külön ellenőrizni kellene.
- **Az Ecto belső adapter-szerződés tesztkészlete** (pl. van-e olyan, hogy
  `Ecto.Adapter.Behaviour` viselkedési kontraktusához tartozó, motoronként lefuttatott
  közös tesztsor, hasonlóan a SQLAlchemy `testing.suite`-hoz) **nem lett feltárva**. Csak
  a felhasználói szintű `Ecto.Adapters.SQL.Sandbox` (tranzakciós izoláció valódi motor
  ellen) dokumentációja került elő, ami más kérdésre válaszol (izoláció, nem
  motor-agnosztikus megfelelőség).
- **Prisma, Django ORM, Hibernate** adapter/dialect-tesztelési architektúrája
  **egyáltalán nem lett feltárva** ebben a körben — a kérdésben javasolt példák közül a
  kör kapacitása (kb. 30-40 hívás) csak a SQLAlchemy, Ecto és ActiveRecord hármasra
  futotta.
- **A tranzakciós szemantika és a konkurrenciakezelés explicit kimaradása a
  szerződés-tesztekből** — nem találtunk Fowlertől vagy Rainsbergertől kifejezett,
  normatív, "a szerződés-teszt sosem ellenőrzi X-et" jellegű kijelentést kifejezetten
  ezekre a két területre. A `megallapitasok.md` 7.3 pontja csak közvetve (egy T4
  vendor-blog technikai állításán és Rainsberger általánosabb, "teljesítmény = integrált
  teszt szerepe" megjegyzésén keresztül) tudja alátámasztani ezt a részt.

## AI-összefoglalót vagy üres vázat visszaadó fetch-ek (nem használtuk forrásként)

- `https://wiki.c2.com/?SubclassToTestAntiPattern=` — l. fent, "Blokkolt/nem használható
  fetch-ek" szekció.

## Nyelvi lefedettség

Ez a kör kizárólag angol nyelvű forrásokat használt. A téma (Fowler/Rainsberger bliki,
nyílt forráskódú tesztelési architektúrák, Pact dokumentáció) nemzetközi, angol nyelvű
szakmai közegben él, nincs magyar intézményi kötődése — ezért ezt nem tekintjük
lefedettségi hiánynak a skill nyelvi szabálya értelmében.
