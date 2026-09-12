# Kivonat — Adatbázis-illesztő mintakutatás

Forrás: `/home/claude/work/.research/adatbazis-illeszto/` (00-plan.md, sq01–sq04).
Készült: 2026-09-09. Ez a dokumentum a négy Sonnet-kör tényanyagát foglalja össze
összefüggő magyar szövegben — nem tartalmaz következtetést vagy ajánlást, azt a
szintézis-kör (Opus) írja külön.

---

## 1. Mire kerestünk választ

A tulajdonos kimondta: az adatbázis-hozzáférést **illesztő vagy más illesztési
programozási mintát** használva kell megoldani, mert később más adatbázis-típusokat is be
akar vezetni, és az újonnan bevezetett motoroknál nem szabad, hogy megjelenjenek azok az
SQLite-specifikus fogások, amiket a jelenlegi tervezés közben fedeztek fel. A rendszer,
amihez a mintát keressük, két különálló tárból áll: egy **eldobható keresési index**-ből
(SQLite FTS5 szöveges index plusz beágyazás-vektorok) és egy **nem eldobható adattár**-ból
(felhasználók, projektek, jogosultságok), utóbbi Drizzle-lel kezelve, a bejelentkezés
Better Authtal. Mindkettő egy gépen, két konténerben, egyetlen szerverfolyamatban fut. A
keresés hibrid — szöveges és jelentés-láb (embedding) keresés kombinációja —,
**helyezés-alapú** egyesítéssel (Reciprocal Rank Fusion, RRF), és a jogosultsági
előszűrés ma azért "ingyenes", mert a jelentés-láb keresés pontos, tehát nem közelítő,
végigolvasás.

A konkrét kiváltó ok, hogy ez a kutatási kör egyáltalán elindult: a rendszer tervezése
során egyetlen körben négy, kifejezetten **SQLite-specifikus fogás** derült ki, amit
valahogy el kell szigetelni a jövőbeli motorváltástól — a `MATCH` operátor nem működik
JOIN-aliasszal; `ANALYZE` nélkül nagyságrendekkel lassabb a JOIN-os lekérdezés; a Drizzle
séma-feltöltésének kizáró listára van szüksége az FTS5 öt árnyéktáblájához; és macOS-en a
rendszer-SQLite FTS5-implementációja hibás. Ezek konkrét, dokumentált okot adtak arra,
hogy a hozzáférési réteg ne az alkalmazáskódba szórva, hanem egy illesztő mögé kerüljön.

A dokumentum korábbi (kutatás nélküli) változata emellett egy tárgyi tévedést is
tartalmazott: az "egy írós" SQLite-korlátot alkalmazás-szintű feltevésként írta le,
holott — ahogy ez a kutatási kör megerősítette — ez az SQLite motor saját, dokumentált
tulajdonsága, tehát elvben pontosan az illesztő feladata lenne elnyelni. Ezt a kört négy
al-kérdésre bontották: (SQ-01) melyik illesztési minta illik ide, és hol vágjuk a
varratot; (SQ-02) hogyan fejezhető ki motor-függetlenül a párhuzamosság és a
tranzakció — ez volt a kör legfontosabbnak jelölt kérdése; (SQ-03) hogyan tehető
hordozhatóvá a szöveges és vektoros keresés felülete; (SQ-04) hogyan tartható őszinte,
azaz nem hamis biztonságérzetet adó, egy ilyen illesztő. A kutatás kifejezetten nem
foglalkozott a konkrét ORM kiválasztásával (a Drizzle már korábban eldőlt) és a keresés
algoritmusának magával (csak a felület alakja érdekelte).

---

## 2. SQ-01 — Melyik minta, és hol a varrat

### Az elsődleges források saját szavaikkal

**Alistair Cockburn** saját, 2005-ös cikke (alistair.cockburn.us, T1, ellenőrzött szó
szerinti forrás) a mintát **Ports and Adapters**-nek nevezi, alternatív néven Hexagonal
Architecture-nek. A cél saját megfogalmazásában:

> "Allow an application to equally be driven by users, programs, automated test or batch
> scripts, and to be developed and tested in isolation from its eventual run-time devices
> and databases." (https://alistair.cockburn.us/hexagonal-architecture)

A lényegi szabály nála nem a bal-jobb, hanem a **belső/külső** aszimmetria: "The rule to
obey is that code pertaining to the *inside* part should not leak into the *outside*
part." Cockburn a portokat *primary/driving* (az alkalmazást hajtó) és *secondary/driven*
(az alkalmazás által hajtott) típusra osztja, és saját, explicit normatív állítása
szerint a portok számát **cél szerint**, nem technológia szerint kell particionálni:
"It doesn't appear that there is any particular damage in choosing the "wrong" number of
ports... My selection tends to favor a small number, two, three or four ports."

**Martin Fowler PoEAA-katalógusa** (martinfowler.com, T1) öt mintát ad meg pontos
definícióval. Fontos, a kutatás által tisztázott tényállás: a **Repository** mintaleírás
szerzősége a katalógus saját oldala szerint **nem Fowleré**, hanem "Edward Hieatt and Rob
Mee, 05 March 2003" — miközben a Data Mapper, Gateway, Table Data Gateway és Row Data
Gateway oldalak szerzője kifejezetten "Martin Fowler". A Repository definíciója:

> "A Repository mediates between the domain and data mapping layers, acting like an
> in-memory domain object collection... Repository also supports the objective of
> achieving a clean separation and one-way dependency between the domain and data mapping
> layers." (https://martinfowler.com/eaaCatalog/repository.html)

A Fowler-oldal saját maga mondja ki, hogy a Repository egy **második, opcionális**
absztrakciós réteg a Data Mapper fölött, ami csak akkor éri meg, ha "a large number of
domain classes or heavy querying" van jelen — tehát a Repository a katalógus saját
állítása szerint sem alapszintű, mindig kötelező minta. A Data Mapper a legalsó szint:
"the in-memory objects needn't know even that there's a database present." A Gateway a
legáltalánosabb fogalom ("An object that encapsulates access to an external system or
resource"), a Table Data Gateway és a Row Data Gateway pedig ennek tábla-, illetve
sor-orientált specializációja.

Az **Eric Evans DDD-könyvének** szó szerinti Repository-szövegéhez ebben a körben nem
sikerült hozzáférni: a WebFetch-eszköz mindkét megpróbált forrásból (a hivatalos, ingyenes
DDD Reference PDF és egy harmadik féltől hosztolt teljes könyv-PDF) megtagadta a szó
szerinti idézést, szerzői jogi okra hivatkozva. Amit helyette tudunk: egy másodlagos blog
(Mike Hadlow, T3) állítólag szó szerint idéz négy előnyt és egy tranzakciós elvet Evans
könyvéből ("Leave transaction control to the client"), és azt is közli, hogy Evans a
Repositoryt kizárólag aggregate root-okhoz rendeli — ezt csak **közepes bizonyossággal**
kezeljük, mert másodkézből, blogon át idézett szöveg.

Az **Oracle hivatalos DAO-oldala** (Core J2EE Patterns, T1, de a fetch AI-átfogalmazott
volt, ezért csak közepes bizonyosságú) szerint a DAO célja "abstract and encapsulate all
access to the data source" — technikai, tábla/entitás-központú minta, domain-fogalmak
bevonása nélkül.

### A tényleges különbség a minták között — a kutatás saját rekonstrukciója

**Fontos módszertani megjegyzés: nem található egyetlen T1–T2 forrás sem, amely egy
helyen, explicit módon szembeállítaná mind a négy fogalmat** (Repository, DAO, Data
Mapper, Gateway). Az alábbi különbségtétel a Fowler-katalógus egymás mellé olvasásából és
az Oracle DAO-leírásból rekonstruált **saját szintézis**, nem egyetlen forrás kimondott
állítása: a Data Mapper a *hogyan* (objektum↔sor mozgatás, a domain semmit nem tud a
perzisztenciáról); a Repository a domain-központú, aggregátumhoz kötött, deklaratív
lekérdezéseket kínáló, opcionális felső réteg; a Gateway technológia-agnosztikus,
általános "csomagold be a speciális API-t" minta; a DAO pedig a Gateway-hagyománytól
független, Java EE-eredetű, technikai, tábla/entitás-központú minta, ami a gyakorlatban
gyakran szinonimaként keveredik a Repository-val, de a mintakatalógusok szintjén nem
szinonima. Ezt a gyakorlatban Jon P Smith (thereformedprogrammer.net, T2, "Entity
Framework Core in Action" könyv szerzője) is megerősíti: a jól tervezett Repository
"domain-specific database views"-t ad, ahol egy metódusnév ("GetAllMembersInLayer")
"communicate[s] intent more clearly than complex LINQ expressions" — szemben egy nyers
DAO-val vagy DbSet-tel.

### Hol vágják a varratot a gyakorlatban

A forrásokból három, egymással versengő vágási elv rajzolódik ki, és a kutatás
kifejezetten hangsúlyozza: **egyik forrás sem állítja, hogy a másik kettő téved a saját
kontextusában** — ez kontextus-függés, nem valódi forrás-ellentmondás.

- **Aggregátumonként** (a DDD-hagyomány, Evans másodkézből idézve): a Repository csak
  aggregate root-okra készül. Derek Comartin (codeopinion.com, T3, gyakorlói vélemény) ő
  maga is csak aggregátumokra használ Repositoryt, "typically contain[ing] only Get(id)
  and Save(aggregateRoot) methods".
- **Táblánként/entitásonként** (a DAO- és Table Data Gateway-hagyomány) — ezt valósítja
  meg a NestJS/TypeORM `@InjectRepository(User)` mintázata is (ld. lent).
- **Use case-enként** (query object / CQRS-hagyomány) — a Repository-kritika fő
  ellenjavaslata: minden olvasási igényhez saját, önálló query objektum, közvetlenül az
  ORM ellen.

### A dokumentált bukások — mindkét oldal, mert ez valódi, éles szakmai vita

A legélesebb, ténylegesen egymásnak ellentmondó véleménypár ebben a körben a
**Repository ORM mellett hasznos-e vagy káros**. Ez **gyakorlói vélemény szintjén zajló**
vita, nem a minta eredeti szerzőinek állítása.

A háttérben ott áll **Ted Neward** "The Vietnam of Computer Science" esszéje (2006,
odbms.org, T1, elsődleges, két lekéréssel ellenőrizve) — nem kifejezetten a
Repository-ról, hanem az ORM-ről általában, a legtöbbet idézett kritikai szöveg:

> "Object/Relational Mapping is the Vietnam of Computer Science. It represents a quagmire
> which starts well, gets more complicated as time passes, and before long entraps its
> users in a commitment that has no clear demarcation point, no clear win conditions, and
> no clear exit strategy." (odbms.org, Neward 2006)

Neward hat lehetséges választ ad (Abandonment, Wholehearted acceptance, Manual mapping,
Acceptance of O/R-M limitations, Integration of relational concepts into the languages,
Integration of relational concepts into frameworks) — nem elutasítja az ORM-et, hanem
strukturált alternatívákat sorol.

**A kontra oldalon** (mind gyakorló mérnökök, nem a minta eredeti szerzői): Derek
Comartin szerint az `IQueryable<T>`/`DbSet<T>` kiadása a repository-ból "leaky
abstraction" — a hívó fél nem tudja, mikor fut le a lekérdezés, és pont ez az a
mechanizmus, amiben az N+1/lusta-betöltés-szivárgás gyökerezik. Jon P Smith cikke további
kritikusokat is nevesít: Rob Conery ("Repositories On Top UnitOfWork Are Not a Good
Idea"), Isaac Abraham ("Why Entity Framework renders the Repository pattern obsolete" —
"Repositories are no easier to mock than IDbSet"), Jimmy Bogard ("Favor query objects
over repositories"). Egy korai (2009), gyakran hivatkozott kritika, Greg Young "DDD: The
Generic Repository" c. bejegyzése ebben a körben **nem volt elérhető** — a Wayback
Machine-en át próbált lekérést a WebFetch-eszköz `SITE_BLOCKED` hibával utasította el.

**A pro/árnyaltabb oldalon** Jon P Smith konkrét előnyöket sorol fel — nem veti el a
mintát: domain-specifikus nézetek, aggregáció, adatbiztonság (tracked/untracked
kontroll), komplex SQL egy helyre gyűjtése. Comartin saját kivétele is jelzi, hogy a
kritika **nem magát a Repository mintát**, hanem a *lekérdezésekre is kiterjesztett,
generikus* változatot (`IRepository<T>` `IQueryable`-lel) támadja.

A kutatás **nem szentel egyik oldalnak sem győzelmet** — ehelyett azt találja, hogy a
vita résztvevői eltérő méretű/stílusú rendszerekről beszélnek: Comartin
vertical-slice/CQRS-architektúrát favorizál (ahol a query object természetes
illeszkedés), Jon P Smith egy nagyobb, réteges rendszert elemez, ahol az aggregáció maga a
fő érték.

### A TypeScript/Node ökoszisztéma — NestJS hivatalos állásfoglalása

A NestJS hivatalos dokumentációja (docs.nestjs.com, T1) **nem foglal állást**
Repository-vs-DAO-vs-Data-Mapper kérdésben, és nincs keretrendszer-szintű "repository
ajánlása": "Nest maintains database agnosticism, enabling seamless integration with any
SQL or NoSQL database." A dokumentumban szereplő "Repository" a **TypeORM saját**
`Repository<T>` osztálya, amit a Nest a DI-n keresztül injektál — ez entitásonkénti,
tábla-központú minta, nem aggregátum-alapú DDD-repository. **A Drizzle és a Kysely saját
állásfoglalása erről a kérdésről ebben a körben nem került elő** — a hatókör kizárta a
konkrét ORM kiválasztását, ezért nem kerestek célzottan Drizzle-dokumentációt a
repository-mintázásról; a kutatás ezt utólag túl szigorú értelmezésnek minősíti, és
következő körre javasolja.

### Az "egy megvalósítás" kérdés — YAGNI vs. port a jövőnek

**Martin Fowler** saját bliki-bejegyzése (Yagni, T1) négy költségkategóriát nevez meg
korai absztrakció építésekor: Cost of Build, Cost of Delay, Cost of Carry, Cost of
Repair — ez **normatív állítás** a minta szerzőjétől. Egy hivatkozott statisztika:
"even with careful up-front analysis, only [1/3] of [features] improved the metrics they
were designed to improve" — ezt Fowler idézi, a mögöttes forrást (Kohavi et al.) ez a
kör nem ellenőrizte elsődlegesen.

A kérdésre legpontosabban válaszoló forrás **Derek Comartin** cikke (gyakorlói vélemény,
T3): "When you define an interface, you base it on your current knowledge, which is
often limited to your single implementation." — vagyis egyetlen implementációra épített
port a *jelenlegi* megvalósítás alakját tükrözi, nem a jövőbeli, még ismeretlen második
implementációét.

**Fontos megkülönböztetés, amit a kutatás explicit kiemel**: Cockburn saját cikke *nem*
foglalkozik az "egy implementáció esetén is építsek-e portot" YAGNI-kérdéssel — az ő
motivációja a tesztelhetőség és a UI/DB-független fejlesztés, **nem** a jövőbeli
adatbázis-csere. Ha valaki Cockburnre hivatkozva indokolná a portot "hátha kell más DB"
alapon, az félreértené Cockburn saját érvelését.

### A hetedik kérdés — egy vagy két port a két tárnak? (Vitatott, extrapoláció)

Erre a konkrét kérdésre — hogy az eldobható keresési index és a nem eldobható adattár
külön vagy közös felület mögé kerüljön-e — **egyetlen forrás sem beszél közvetlenül**; ez
a kutatás szerint **evidence of absence**, nem "még nem találtuk meg". Amit Cockburn saját
"hány portot nyissunk" elvéből extrapolálni lehet: mivel a két tár különböző *célt*
szolgál, nem csak különböző technológiát, Cockburn saját logikája ("architect the
system's interfaces *by purpose* rather than by technology") szerint ez két külön
secondary portot indokolna. **Ez a kutatás saját, Cockburn elvéből levezetett
következtetése, nem Cockburn vagy bárki más kimondott állítása erre a konkrét
helyzetre** — `Vitatott` jelöléssel rögzítve.

---

## 3. SQ-02 — Párhuzamosság és tranzakciók

Ez volt a kör kijelölt legfontosabb kérdése, és 22 forrást archivált (16 T1 hivatalos
dokumentáció, 4 T2 gyártói issue tracker, 1 T3 gyakorlói blog).

### Az SQLite írási modellje pontosan

A hivatalos SQLite-dokumentáció (sqlite.org, T1) kertelés nélkül mondja ki az "egy író"
korlátot **tervezési döntésként, nem hibaként**:

> "SQLite supports multiple simultaneous read transactions coming from separate database
> connections, possibly in separate threads or processes, but only one simultaneous write
> transaction." (sqlite.org/lang_transaction.html)

A WAL-doksi ugyanezt a fájlszerkezetből vezeti le: "since there is only one WAL file,
there can only be one writer at a time" (sqlite.org/wal.html). A hivatalos "Appropriate
Uses For SQLite" oldal explicit döntési kritériumként fogalmazza: "If there are many
client programs sending SQL to the same database over a network, then use a
client/server database engine instead of SQLite." **Ez tehát nem alkalmazás-szintű
feltevés, hanem az SQLite motor dokumentált, szándékos tervezési tulajdonsága** — a D-34
korábbi tárgyi tévedését ez a forrás közvetlenül megcáfolja.

A zárolási állapotgép (UNLOCKED→SHARED→RESERVED→PENDING→EXCLUSIVE) öt fokozatból áll, a
PENDING állapot célja kifejezetten az író-éhezés (writer starvation) elkerülése. A három
tranzakció-mód (DEFERRED/IMMEDIATE/EXCLUSIVE) közül az alapértelmezett DEFERRED nem
azonnal zárol, hanem csak az első tényleges írás pillanatában próbál write-zárat
szerezni — és **ekkor** bukhat el `SQLITE_BUSY`-val, akkor is, ha SELECT-tel indult a
tranzakció. Egy különösen fontos versenyhelyzet, amit a hivatalos "Isolation In SQLite"
oldal ír le: amikor egy olvasás-tranzakció írásra próbál frissülni, de közben más már
írt, `SQLITE_BUSY_SNAPSHOT` hibát kap — és ez a hiba **nem old fel egyszerű
várakozással** (`busy_timeout`-tal), mert két, egymással logikailag ütköző "múlt-
pillanatkép" ütközése, nem egyszerű zárolási torlódás. A hivatalos javasolt minta erre:
ha egy tranzakció tudja előre, hogy írni is fog, kezdje `BEGIN IMMEDIATE`-tel.

Az izoláció kérdésében az SQLite hivatalos állítása az egyik legélesebb az egész
korpuszban: "all transactions in SQLite show 'serializable' isolation. SQLite implements
serializable transactions by actually serializing the writes." Ez azt jelenti, hogy
SQLite-ban a SERIALIZABLE **nem választható szint a több közül** (mint Postgres-en vagy
MySQL-en), hanem az egyetlen elérhető — és nem bonyolult konfliktus-detektálással
(mint Postgres SSI-je), hanem azzal kapja "ingyen", hogy fizikailag nem enged két írót
egyszerre.

### A Unit of Work minta — mit old meg, és mit nem

Fowler saját PoEAA-definíciója (T1, de a fetch átstrukturált volt, ezért csak az
idézőjeles mondatok kezelendők szó szerintinek): "Maintains a list of objects affected by
a business transaction and coordinates the writing out of changes and the resolution of
concurrency problems." A definíció maga is nevesíti a "resolution of concurrency
problems"-t mint a minta feladatát — de a kutatás értelmezése szerint ez a **koordinálás**
ígérete, nem annak garantálása, hogy minden motoron ugyanaz a konfliktus-feloldási
mechanizmus fusson le. A UoW keretet ad a változások összegyűjtésére, de a "mit jelent az,
hogy egy tranzakció sikeres/ütközik" kérdést a mögöttes motorra hárítja.

### Mit csinálnak a valós, több motort támogató rétegek — táblázatos áttekintés

A kutatás kilenc adatréteget vizsgált meg (SQLAlchemy, Prisma, Knex, Kysely, Doctrine
DBAL, Hibernate/JPA, ActiveRecord, Ecto, Drizzle). **A minta egyértelmű és minden
vizsgált rétegnél konzisztens: egyik sem állítja, hogy az izolációs szint vagy a
zárolási képesség egyenértékű lenne minden motoron — mind dokumentálják a különbséget,**
nem hamisan egyenlővé teszik.

| Réteg | Mit ígér | Mit mond arról, amit NEM tud elrejteni |
|---|---|---|
| SQLAlchemy | Motoronkénti külön doksi-oldalak | "Not every DBAPI supports every value; if an unsupported value is used... an error is raised." |
| Prisma | Táblázatos, motoronkénti izolációs-szint mátrix | "CockroachDB and SQLite only support the Serializable isolation level." |
| Knex | Nincs szimulálás | "Not supported by oracle and sqlite." |
| Kysely | Közös enum, de nyitott, motorspecifikus funkciókérés | (maintainer-válasz nem volt elérhető) |
| Doctrine DBAL | Csak alsó korlátot ígér | "guaranteed to be at least READ_COMMITTED" |
| Hibernate/JPA | Nem próbálja egységesíteni | "let the database handle locking issues"; csendes degradáció hiányzó lock mode-nál |
| ActiveRecord | Motor-független SQL-minta (optimista út) | pesszimista út külön API, motorfüggő |
| Ecto | Nyíltan dokumentált funkció-kiesés | "does not support async tests... due to SQLite only allowing up one write transaction" |
| Drizzle | Csak Postgres-specifikus konfigurációs felület volt látható | SQLite-specifikus felület **nem került elő ebben a körben — fontos hiány, mert ez a rendszer saját ORM-je** |

A **Prisma saját issue trackere** (T2, github.com/prisma/prisma/issues/25587) az
egyetlen legjobb konkrét bizonyíték arra, hogy a DEFERRED/IMMEDIATE döntés *elrejthető*:
"Right now we always start transactions on SQLite as IMMEDIATE... it would be better to
open it as DEFERRED to be able to have concurrent transactions" — a Prisma tehát
**motor-specifikus, teljesítmény-kompromisszummal járó, de helyesség-kompromisszum
nélküli** alapértelmezést választ az alkalmazáskód elől elrejtve.

### Izolációs szintek — Berenson és társai kritikája

A kért alapmű, Berenson, Bernstein, Hamilton, Newson, O'Neil, O'Neil "A Critique of ANSI
SQL Isolation Levels" (1995, T1, csak egyetlen, nem-kanonikus CMU-hosztolt PDF-másolatból
ellenőrizve, kereszt-ellenőrzés nélkül) kimutatja, hogy maga az ANSI SQL-92 szöveg
**kétértelmű**, és bevezet egy negyedik jelenséget (P0, "Dirty Write") a szabvány három
jelensége (Dirty Read, Non-repeatable Read, Phantom) mellé. A cikk fő tanulsága a
kutatás értelmezésében: **a "SERIALIZABLE" elnevezés önmagában nem garantálja az azonos
viselkedést** két motor között, mert a szabvány szövege eleve alulspecifikált. Ez
elméleti alátámasztása annak, amit a gyakorlatban látunk: minden vizsgált réteg egyszerűen
**átdirigálja** az izolációs szint nevét a motorra, nem próbálja garantálni az azonos
szemantikát a név mögött.

### Zárolás és sorosítás motor-független kifejezése — három megfigyelt felület-alak

A Django hivatalos dokumentációja egyszerűen kimondja: "SQLite does not support the
SELECT ... FOR UPDATE syntax. Calling it will have no effect." — ez **hiányzó
képesség**, nem eltérő szintaxis. A kutatás három, dokumentáltan alkalmazott
felület-alakot azonosít arra, hogyan kezelik a rétegek a hiányzó/eltérő motor-
képességeket:

1. **Explicit "nincs hatása" jelzés** (Django `select_for_update` SQLite-on) — a hívás
   nem hibázik, de dokumentáltan semmit nem csinál.
2. **Motor-független alapminta-helyettesítés** — az **optimista, verziószám-alapú
   zárolás**, amit két, egymástól független hivatalos forrás (Rails ActiveRecord:
   `lock_version` oszlop + `StaleObjectError`; Prisma: `version` mező + feltételes
   `updateMany`) is leír, motorfüggetlenül. Ez a legerősebb bizonyíték arra, hogy
   **létezik olyan felület-alak, ami tényleg elrejti a motor-különbséget**, mert a
   mögöttes mechanizmus sosem támaszkodott motor-specifikus zárolásra.
3. **Csendes degradáció a legközelebbi elérhető garanciára** — Hibernate hivatalos
   dokumentációja: "If the requested lock mode is not supported by the database,
   Hibernate uses an appropriate alternate mode instead of throwing an exception."

### Konkrétan: elrejthető-e az "egy író" korlát? — a Django-esettanulmány

**Ez a kutatási kör talán legfontosabb egyetlen bizonyítéka.** A Django hivatalos
issue-trackerében (ticket #29280, T2, többéves, dokumentált vita) Ove Kåven pontosan
leírja a törés mechanizmusát: egy `update_or_create()`-szerű "upsert" két egyidejű
szálon fut, mindkettő SELECT-tel kezdi (mert SQLite-on nincs `SELECT FOR UPDATE`), mindkét
SELECT sikeres, majd amikor mindkettő írni próbál, csak az egyik kapja meg a write-zárat:
"The thread that didn't get the write lock immediately gets a 'database is locked' error.
Its transaction is aborted." És a kritikus megjegyzés: "The timeout mentioned in the
Django documentation will have absolutely no effect on this."

A Django-karbantartó (Aymeric Augustin) **elutasította** azt a javaslatot, hogy Django
mindenhol IMMEDIATE-re váltson (ami eltüntette volna a hibát minden alkalmazáskód-
változtatás nélkül): "the performance hit of removing the possibility of concurrent
database reads — and web workflows tend to be read-heavy — seems too high to implement
this in Django." A végleges megoldás, három évvel később, **nem** egy csendes,
motor-független viselkedésváltoztatás lett, hanem egy **SQLite-specifikus, opt-in
konfigurációs kapcsoló** (`OPTIONS["transaction_mode"]`). **A Django ORM — egy 20+ éves,
rendkívül érett, több motort támogató adatréteg — nem tudta transzparensen elrejteni ezt
a korlátot úgy, hogy az alkalmazásfejlesztőnek ne kelljen SQLite-specifikus tudást
szereznie.** A "megoldás" a probléma *motorra korlátozott, dokumentált szivárgása* a
konfigurációs felületre, nem annak eltüntetése. A hivatalos Django-dokumentáció
elsőként felsorolt tanácsa a probléma tartós előfordulására: "Switching to another
database backend. At a certain point SQLite becomes too 'lite' for real-world
applications."

Egy második, egymástól teljesen független ökoszisztémából (Elixir) érkező, megerősítő
esettanulmány: az Ecto SQLite3 adapter hivatalos dokumentációja explicit kimondja, hogy
**egy konkrét funkció** (párhuzamos, sandboxolt tesztfuttatás) **dokumentáltan nem
támogatott** SQLite alatt, "due to SQLite only allowing up one write transaction at a
time" — más motorokon (Postgres) elérhető.

### Mit lehet és mit nem lehet elrejteni — a kutatás összegzése erre a konkrét kérdésre

A bizonyítékok alapján a kutatás a következő, több, egymástól független forrásból
konzisztensen alátámasztott állítást fogalmazza meg: **az "egy egyidejű író" korlát
valóban nem rejthető el teljesen és ingyen egy réteg mögé, valahányszor az alkalmazás
olyan versenyhelyzet-érzékeny logikát futtat, ami más motorokon `SELECT ... FOR
UPDATE`-re (vagy ezzel egyenértékű pesszimista sor-zárolásra) támaszkodna.** Ennek négy
támasza: (1) a hivatalos SQLite-dokumentáció maga mondja ki tervezési döntésként; (2)
minden vizsgált réteg dokumentálja, nem eltünteti a különbséget; (3) a Django-csapat két,
egymást kizáró jó megoldás közül kellett válasszon, és nem volt harmadik, mindkettőt
kielégítő út; (4) a hivatalos Django-doksi maga ajánlja a motorváltást végső
megoldásként.

**Amit viszont valóban el lehet és el is szoktak rejteni** — ez fontos ellenpélda, hogy
az állítás ne legyen túlzó: a konfliktus-mentes, hozzáadó írások zöme simán fut egy
szigorúan sorosított modellen is (a korlát csak ütköző, egyidejű írásoknál jelentkezik);
az optimista, verziószám-alapú zárolás valóban motor-független felület-alak; és a
DEFERRED/IMMEDIATE döntés **csendben, teljesítmény-kompromisszum árán, de helyesség-
kompromisszum nélkül** eldönthető az illesztő rétegben, ahogy a Prisma dokumentáltan
teszi.

---

## 4. SQ-03 — Keresés hordozható felület mögött

### Mi tér el motoronként a szöveges keresésben

Minden vizsgált motor saját, eltérő lekérdezési szintaxist és rangsorolási módszertant
használ. Az **SQLite FTS5** `bm25()` rangsorolása fordított irányú a legtöbb
implementációhoz képest: "The better the match, the numerically smaller the value
returned" (sqlite.org/fts5.html) — ezt a dokumentáció szándékos tervezési döntésként
indokolja. A **PostgreSQL** `ts_rank`/`ts_rank_cd` függvényei külön dokumentálják, hogy
"csak példák": "The built-in ranking functions are only examples. You can write your own
ranking functions." A **MySQL** háromféle módot ismer, a query expansion kétlépéses,
"vak visszacsatolásos" mechanizmus. Az **Elasticsearch** Query DSL-je élesen elválasztja
a pontozó *query context*-et a nem pontozó *filter context*-től. A **Meilisearch** és a
**Typesense** a legélesebb eltérés: mindkettő **explicit nem BM25-öt** használ, hanem
saját, több lépcsős, tie-breaking bucket-sort rangsorolást — a "pontszám" itt több,
egymást felülíró kritérium lexikografikus sorrendje, nem egyetlen súlyozott összeg.

### A rangsor-pontszámok összemérhetetlensége — a kör egyik kulcspontja

**Több hivatalos dokumentáció explicit kimondja, hogy a pontszám nem abszolút mérték.**
Az Elasticsearch saját "Getting consistent scoring" oldala szerint **két egymást követő,
azonos lekérdezés is eltérő sorrendű találatokat adhat**, mert a replika-shardok
index-statisztikái eltérhetnek: "if you run the same query twice in a row that it will go
to different copies of the same shard" — a pontszám tehát (a) különböző lekérdezések
között biztosan nem, (b) ugyanazon lekérdezés ismételt futtatásai között sem garantáltan
összemérhető. A PostgreSQL dokumentációja ugyanezt még élesebben mondja ki: "It is
important to note that the ranking functions do not use any global information, so it is
impossible to produce a fair normalization to 1% or 100% as sometimes desired." Ezzel
szemben az **SQLite FTS5 dokumentációja nem tartalmaz explicit mondatot** az
összemérhetetlenségről — ez a formula szerkezetéből (korpusz- és lekérdezés-függő IDF)
matematikailag következik, de a kutatás ezt **saját levezetett következtetésként**, nem
idézett tényként jelöli meg — fontos elhatárolni Elasticsearch/PostgreSQL explicit
állításától.

Ez a megállapítás közvetlenül alátámasztja azt a tervezési döntést, hogy **a helyezés
(rank), nem a pontszám (score) az, amit egy motor-független illesztő felületen érdemes
átadni**.

### Léteznek-e valódi keresés-absztrakciós rétegek, és mit fednek le

A **Searchkick** (Ruby) saját README-je szerint kizárólag Elasticsearch/OpenSearch fölött
működik — ez tehát egyetlen motorcsalád fölötti kényelmi réteg, nem valódi
motorosztályok-közötti absztrakció. Ezzel szemben a **Django Haystack**, a **Laravel
Scout** és a **Hibernate Search** valódi, több motorcsaládot átfogó absztrakciók, és
mindegyik **saját dokumentációjában ismeri el** a határait:

- A Haystack saját support-mátrixa kimondja, hogy a PostgreSQL FTS backend **nem** tudja
  a "More Like This" funkciót, amit a Lucene-alapú backendek (Solr, ES, Whoosh, Xapian)
  igen.
- A Laravel Scout dokumentációja explicit: "The `searchableAs` method has no effect when
  using the database engine" és "Since search engines are not aware of your Eloquent
  model's global scope definitions, you should not utilize global scopes."
- A Hibernate Search a "backend" fogalmát az absztrakciós rétegként definiálja ("where
  'things get done'"), de rögtön hozzáteszi: "Each backend exposes its own APIs to
  define analyzers and normalizers" — és dedikált, motor-specifikus kiszökő ajtókat ad
  (`fromLuceneQuery`, `fromJson`) azokra az esetekre, amikor az absztrakció nem elég.

**Ismétlődő, négy réteg, amit a keretrendszerek saját maguk vallanak be nem
elrejthetőnek**: a szöveg elemzése/tövezése/tokenizálása (motor-specifikus logika); a
séma/mapping/attribútum-deklaráció (Meilisearch/Typesense előre kell deklaráltassa); a
motoronként eltérő funkció-készlet (Haystack support-mátrixa); és az
ORM-integrációs mellékhatások szivárgása (Laravel Scout globális scope-figyelmeztetése).
A kutatás nem talált dedikált gyakorlói "hogyan bukott meg egy keresés-absztrakció"
blogbejegyzést — ami erősebb bizonyíték ennél, hogy maguk a keretrendszerek dokumentumai
vallják be ugyanazokat a réteg-határokat, tervezési szinten, nem elégedetlen felhasználói
panaszként.

### A vektoros oldal

**Minden vizsgált vektor-motor saját dokumentációjában explicit kimondja, hogy az adott
index/mód pontos-e vagy közelítő.** A pgvector alapból pontos keresést végez ("By
default, pgvector performs exact nearest neighbor search, which provides perfect
recall"), közelítő indexet (HNSW/IVFFlat) csak explicit létrehozással kap a felhasználó.
A Qdrant explicit `exact` kapcsolóval rendelkezik. A Milvus kimondja, hogy a FLAT index az
egyetlen, ami garantáltan pontos ("the only index that can guarantee exact search
results"). A Faiss saját wikije táblázatban jelöli, mely index "Exhaustive". A **Weaviate**
és a **sqlite-vec** esetében ezt a kör nem tudta elsődleges forrásból megerősíteni
(hiány).

A szűrés helye (pre- vs. post-filtering) minden ANN-motornál dokumentált probléma, és
**közvetlenül befolyásolja a recall-t** — nem elrejthető technikai részlet. A pgvector
konkrét számpéldával mutatja: "If a condition matches 10% of rows, with HNSW and the
default `hnsw.ef_search` of 40, only 4 rows will match on average." A Qdrant saját,
"filterable HNSW" nevű megoldást épített erre.

A távolságmértékek is eltérnek motoronként (pgvector hat mértéket ad — L2, inner product,
cosine, L1, Hamming, Jaccard —, Weaviate ötöt, Faiss saját listát). Fontos technikai
részlet, amit a Faiss wiki explicit kimond: az inner product metrika "differs from cosine
similarity unless vectors are normalized to unit hypersphere surfaces" — a "koszinusz-
távolság" tehát nem natív elsődleges metrika minden motorban.

**Nincs SQL-szabvány a vektoros keresésre.** A SQL:2023 (ISO/IEC 9075:2023) property
graph lekérdezéseket, bővített JSON-t hozott, de vektor- vagy embedding-adattípust nem
(Wikipedia-összefoglaló alapján, T5, csak orientációra — a kutatás nem talált T1/T2
forrást, ami ezt közvetlenül megerősítené vagy cáfolná). Amit a kutatás talált, azok
gyártónkénti kiterjesztések (Oracle 23ai VECTOR típusa, Microsoft/Azure SQL vektor-
előzetes funkciói) — **a vektoros keresés jelenleg "minden gyártó a saját útját járja"
állapotban van**, és a kutatás nem talált semmilyen, hivatalos testület vagy több gyártó
által elfogadott, közös vektor-kliens API-specifikációt sem — ez a kutatás értelmezése
szerint evidence of absence.

### A hibrid keresés hordozhatósága — RRF mint motor-független egyesítő módszer

Ez a kör második kulcskérdése, és a bizonyítékok itt nagyon egyértelműek. Az RRF-et
bevezető eredeti tudományos cikk (Cormack, Clarke, Buettcher, SIGIR 2009, T1) saját
szavaival:

> "Reciprocal Rank Fusion (RRF)... combines ranks without regard to the arbitrary scores
> returned by particular ranking methods... requires no special voting algorithm or
> global information; ranks may be computed and summed one system at a time."
> (cormack.uwaterloo.ca/cormacksigir09-rrf.pdf)

A szerzők már 2009-ben explicit "arbitrary" (önkényes) jelzővel illetik a rendszerek
pontszámait — vagyis az alapfeltevés, hogy a pontszámok rendszerek között nem
összemérhetők, és pont ezt kerüli meg az RRF azzal, hogy csak a helyezést nézi. Az
**Elasticsearch saját RRF-dokumentációja** ugyanezt az indoklást adja gyártói szinten:
"RRF requires no tuning, and the different relevance indicators do not have to be related
to each other to achieve high-quality results." A kutatás összegzése: mivel a rangsor-
pozíció (1., 2., 3. helyezett) motorfüggetlenül definiált fogalom, míg a nyers pontszám
motoronként, sőt lekérdezésenként más jelentésű és Elasticsearch esetén dokumentáltan
instabil is, **a helyezés-alapú egyesítés elvi okokból hordozhatóbb, mint a
pontszám-alapú egyesítés** — ez a rendszer tervezési döntését (RRF) közvetlenül
alátámasztó, hivatalos forrásokból származó tény, nem csak kényelmi érv.

---

## 5. SQ-04 — Hogyan tartható őszinte egy illesztő

### Mi a szerződés-teszt pontosan

**Martin Fowler** saját bliki-bejegyzése (2011, T1) a szerződés-tesztet (Contract Test)
kifejezetten **külső szolgáltatások** test double-jainak hitelesítésére vezeti be: "These
check that all the calls against your test doubles return the same results as a call to
the external service would." Fontos, hogy Fowler ezt **nem** a build-pipeline ritmusához
köti, hanem a külső szolgáltatás saját változási ritmusához ("Often running just once a
day is plenty"). A felhasználó által kifejezetten megkérdezett `IntegrationContractTest`
oldal **ma már nem létezik önállóan** — Fowler saját revíziós jegyzete szerint 2018-ban
összevonta a `ContractTest` néven: "the term 'contract test' has become widely used for
these, so I changed the bliki entry." Fowler egy fontos korlátozást is rögzít: a
szerződés-teszt **nem feltétlenül az adatot**, hanem a formátumot ellenőrzi.

Az "abstract test case" fogalom közvetlenül **J. B. Rainsbergerhez** köthető, aki
1999–2001 körül alkotta meg, majd 2021-ben saját visszatekintő bejegyzésében explicit
összeköti a "contract test" fogalmával: "I called them *abstract test cases* at the
time, but today we know them as *contract tests*." Rainsberger a szerződés-tesztet
kifejezetten a **Liskov Substitution Principle**-hez köti: "we must be able to freely
replace a supplier module with another supplier that claims to act as the same type." **A
Rainsberger-féle definíció szélesebb, mint Fowleré**: nem csak külső szolgáltatásra,
hanem bármely, több osztály által implementálható interfészre vonatkozik — beleértve
explicit a Repository mintát is: "I generally introduce a Repository interface to hide
the database... I pull up the general 'push and pull data' tests up as Contract Tests
for Repository." **Ez pontosan a D-34 illesztő esete.** A kutatás megjegyzi, hogy ez nem
ellentmondás a két forrás között, hanem szűkebb/tágabb olvasat — Fowler eredeti esete a
Rainsberger-féle tágabb definíció speciális esete, és a D-34 kontextusában a tágabb
olvasat a releváns, mert az adatbázis-illesztő saját kódbázison belüli, két (jelenleg
egy) implementációval rendelkező interfész, nem külső szolgáltatás.

### Közös tesztkészlet több megvalósításra — nevesített minták és valós projektek

Rainsberger saját 2021-es összefoglalója **két strukturális mintát** ír le, amelyek
között ő maga 20 év alatt váltott: (A) a hagyományos, absztrakt ős + template method
minta ("The concrete test subclass inherits the tests from the abstract test
superclass"); (B) az újabb, kompozíció-alapú minta, paraméterezett gyárakkal ("favors
composition over inheritance... an abstract factory object that creates instances of the
objects to test"). A felhasználó által megjelölt "subclass-to-test-interface" kifejezés
nem egyezik pontosan egyetlen forrás szóhasználatával sem, de a legközelebbi, ténylegesen
**vitatott** minta a "Subclass to Test" (c2-wiki `SubclassToTestAntiPattern`) — ennek
tartalmát a kör nem tudta elolvasni (JavaScript-védett oldal), de Rainsbergernek van egy
külön, "Why I Don't Consider Subclass to Test An Anti-Pattern" című előadása, ami
**megerősíti a vita tényét**, csak a tartalmát nem sikerült feltárni.

Rainsberger explicit, önmaga által megnevezett kockázata a **szemantikai drift**: a
kollaborációs tesztek és a szerződés-tesztek szétcsúszhatnak, és erre 20 év alatt sem
talált automatizált megoldást: "Even after 20 years, I still don't have a better answer
than to rely on the human to pay attention and check."

Három valós projekt architektúrája:

- **SQLAlchemy** (T1, a legkifejtettebb, hivatalosan dokumentált minta): egy közös,
  motorfüggetlen `sqlalchemy.testing.suite` teszthalmaz, amit egy dialektus egyetlen
  sorral importál be ("There's no need for a third party dialect to run through
  SQLAlchemy's full testing suite"), és egy **explicit `Requirements` osztály**, ami nem
  motornevet, hanem *képesség*-zászlókat ad meg ("specific database and DBAPI names are
  mentioned less and less, in favor of @requires directives which state a particular
  capability"). Ha egy teszt mégsem fedhető le zászlóval, a dialektus közvetlenül
  felülírhatja/kihagyhatja (`@testing.skip("access")`). **Ez közvetlenül alkalmazható
  mintaként a D-34-re**: az SQLite-specifikus fogások nem "if sqlite" ágakként, hanem
  képesség-zászlóként fejezhetők ki egy jövőbeli második motorra nézve.
- **Ecto** (Elixir, T1): a hivatalos dokumentáció **nem** egy motor-agnosztikus
  megfelelőségi tesztkészletről szól, hanem az **Ecto SQL Sandbox** mintáról — minden
  teszt a valódi, konfigurált adatbázis ellen fut, tranzakcióba csomagolva, teszt végén
  visszagörgetve. Ez fontos ellenpélda: nem old meg semmit a motorok közti
  viselkedés-eltérésből, csak az izolációt oldja meg gyorsan futó tesztekhez.
- **Rails ActiveRecord** (a forráskódból, `test_case.rb`, szó szerint): egy közös
  `ActiveRecord::TestCase` alaposztály + öt adapter-hatókörű alosztály, amiknek
  `self.run` metódusa **futásidejű őrfeltétellel** csak akkor engedi lefutni a teszteket,
  ha a ténylegesen konfigurált adapter egyezik. Ez egy harmadik, olcsóbb, de gyengébb
  garanciájú minta, mint a SQLAlchemy CI-mátrixa: egy adott futás csak egy motor ellen
  fut, a több motor lefedettségét a CI-mátrix (több párhuzamos job) adja.

### Testcontainers — mit ad hozzá, mi az ára

A hivatalos dokumentáció (T1) kifejezetten a hamis-biztonság problémájára válaszként
pozicionálja magát: "In-memory services may not have all the features of your production
service and behave slightly differently." Az ára: Docker-függőség (a D-34 kontextusában,
egy gépen, két konténerben futó szolgáltatásnál ez nem jelent plusz réteget, mert a
Docker már adott, de a fejlesztői gépeken/CI-ban lassabb tesztfuttatást jelent egy
in-process SQLite-fájlhoz képest), a GenericContainer-réteg tanulási költsége, és egy
automatikus takarító Ryuk sidecar konténer, ami működő Docker-daemon jelenlétét
feltételezi.

### A hamis biztonság kockázata — a legfontosabb kérdés, konkrét esettel

**Fontos pontosítás**: a kutatás **nem talált** olyan konkrét, nyilvánosan dokumentált
esetet, ahol kifejezetten egy *több-implementációs, formális szerződés-tesztkészlet*
lett volna zöld, miközben egy adott motor másképp viselkedett éles környezetben. Amit
talált, egy szorosan rokon, ugyanazt a mögöttes kockázatot dokumentáló jelenség: amikor
a **teszt-motor** (SQLite) és az **éles motor** (PostgreSQL) eltérése miatt egy zöld
tesztfuttatás valós hibát rejtett el — ez a D-34 jelenlegi helyzetére (SQLite ma,
esetleg más motor később) közvetlenül alkalmazható analógia.

Egy gyakorlói post-mortem (dev.to, T6, egyetlen, nem ellenőrizhető szerző, de rendkívül
konkrét, technikailag koherens leírás) a legélesebb, konkrét eset:

> "We were making a schema change, so we ran the suite against a real Postgres instance
> for once. Two tests failed. On SQLite the same commit was 1241/1241 green."

A cikk három konkrét, valós hibát dokumentál: (1) idegenkulcs-kényszer nem érvényesült
SQLite-on alapértelmezetten (a szerző szerint ez okozta a fenti két hibát); (2) a
migrációs eszközt (Alembic) a tesztkészlet **soha nem futtatta**, tehát a migrációs kód
"was the least tested code in the repository. Not under-tested. Zero lines executed."; (3)
törölt sorok "feltámadtak" idegenkulcs-kényszer hiányában és azonosító-újrafelhasználás
miatt. A szerző összefoglalása a kockázat lényegére: "for three weeks our tests were
measuring a different database than the one our users touch. They were not lying. We
were reading them as if they said more than they did." **Fontos, hogy a javítás sem
oldott meg mindent** — a cikk explicit leszögezi: "It does not make SQLite run your
migrations... It does not make the two engines equivalent. It closes one specific gap."
Ez közvetlenül alátámasztja: egyetlen "kapcsold be a szigorúbb módot" trükk nem szünteti
meg, csak csökkenti a motor-eltérés kockázatát.

Egy Postgres-as-a-service gyártó blogja (Neon, T4 — a technikai állítások
ellenőrizhetők, a végkövetkeztetés, saját termék ajánlása, marketing) hasonló jelenségre
mutat rá: "inserting a float (3.14) into an INTEGER column succeeds silently [SQLite-on].
PostgreSQL enforces strict type checking and would raise an error."

### Megéri-e portot építeni egy megvalósításhoz? — Ez a kör kifejezett, nem szépített válasza: nincs empirikus adat

**Ez explicit, "nem szépített" megállapítás**: a kör kifejezetten keresett empirikus
(mért, nem véleményalapú) anyagot arra, hogy megéri-e előre megépíteni egy nem-használt
absztrakciós réteget. A célzott keresés (`"empirical study cost of abstraction layer
unused interface software engineering research"`) **kizárólag véleményblogokat és
Medium-cikkeket hozott** (T0/T6 szint, számadat vagy módszertan nélkül) — ezeket **nem**
vették fel forrásként. Ez a kutatás szerint evidence of absence a kör keresési
költségvetésén belül: nem került elő specifikusan a "port/adapter előre megépítése vs.
YAGNI" kérdésre szabott, mért, publikált tanulmány.

Az egyetlen talált, számszerű adatpont — a Fowler-féle YAGNI-esszében idézett Kohavi et
al.-hivatkozás ("only ⅓ of [features] improved the metrics they were designed to
improve") — **nem port/adapter-specifikus**: Microsoft-termékek általános
funkció-fejlesztéseiről szól, nem adatbázis-illesztőkről. Analógiaként használható, de a
kutatás explicit figyelmeztet: "nem szabad úgy idézni, mintha kifejezetten
portokra/illesztőkre mért adat lenne." A mögöttes Kohavi-tanulmányt maga ezt a kört sem
ellenőrizte elsődleges forrásból, csak Fowler másodkézből idéző szövegén keresztül.

Fowler saját YAGNI-esszéje **normatív állításként** explicit az absztrakciókra
vonatkoztatja az elvet: "any abstraction that makes it harder to understand the code for
current requirements is presumed guilty" — de explicit **kizárja** a hatálya alól a
kód-karbantarthatóságot növelő munkát: "Yagni only applies to capabilities built into the
software to support a presumptive feature, it does not apply to effort to make the
software easier to modify." Fowler maga is elismeri, hogy a YAGNI néha téved, de ezt
**saját, bevallott véleményként**, nem mért adatként: "My sense is that yagni-failures
are relatively rare."

**A kutatás kiemel egy fontos elhatárolást**: a forrásanyag legerősebb, ténylegesen
támogatható érve a port mellett **nem** a hordozhatósági (jövőbeli motorváltás) érv,
hanem Rainsberger **tesztelhetőségi** érve — egy Repository-interfész és a mögé tartozó
szerződés-teszt **ma is** javítja az üzleti logika izolált tesztelhetőségét, függetlenül
attól, lesz-e valaha második motor. A D-34 indoklása ("mert később más adatbázis-
típusokat is be akar vezetni") a Fowler-féle, jövő-orientált érvet idézi, miközben a
forrásanyag erősebb, empirikusan is jobban alátámasztható érve a jelen-orientált
tesztelhetőségi érv lenne.

### Mit nem tud ellenőrizni egy szerződés-teszt

A **Pact** hivatalos dokumentációja (T1, a legelterjedtebb consumer-driven contract
testing eszköz) explicit, kanonikus választ ad: "A contract test does not check for side
effects." Egy explicit felelősség-táblázatban a mellékhatásokat (perzisztálás,
állapotváltozás) kifejezetten a szolgáltató saját funkcionális tesztjeinek feladataként
jelöli meg — **ez direkt válasz arra, hogy egy adatbázis-illesztő valódi
adattárolási mellékhatását a szerződés-teszt önmagában nem fedi le**. A Pact-dokumentáció
egy második figyelmeztetést is ad a túlspecifikálás kockázatáról: ha a szerződés-teszt
üzleti validációs szabályokat is lefed, "over-specifying our scenarios" a szolgáltató
legitim, nem-törő változtatásait is eltöri.

A **teljesítmény** kimaradását Rainsberger explicit kimondja saját tesztfilozófiájában:
"I tend to limit integrated tests to the roles of checking performance... and blunder
checking my contracts" — vagyis a teljesítmény nem a szerződés-teszt, hanem egy külön,
integrált teszt feladata. **A tranzakciós szemantika és a konkurrenciakezelés kimaradására
nem talált a kör kifejezett, elsődleges, normatív forrást** Fowlertől vagy
Rainsbergertől — ez csak közvetve, a Neon-blog technikai állításán (a zárolási modell
motoronként eltér, ami csak konkurrens terhelés alatt derül ki) és Rainsberger fenti,
általánosabb megjegyzésén keresztül támasztható alá. Ez explicit hiányként van rögzítve.

---

## 6. Ellentmondások

Az alábbiak a négy kör `contradictions.md` fájljaiban rögzített, valódi vagy látszólagos
feszültségek — a források saját szavaival, mindkét oldalról.

**1. Repository ORM mellett: hasznos vagy káros? (SQ-01, valódi szakmai
véleménykülönbség.)** Kontra: Comartin, Conery, Abraham, Bogard, Sapiens Works — mind
gyakorló mérnökök — szerint a Repository ORM fölé építve vagy leaky abstraction, vagy
felesleges burkolat. Pro/árnyalt: Jon P Smith és Comartin saját kivétele szerint jól
tervezve (szűk felülettel, csak aggregátum-gyökérre) valódi értéket ad. **Mindkét oldal
egyetért abban**, hogy a *generikus*, minden entitásra ráhúzott, lekérdezés-visszaadó
Repository (`IRepository<T>` `IQueryable`-lel) problémás — a vita a szűkebb kérdésben
van: egyáltalán érdemes-e Repository-t használni ORM mellett, vagy csak query object-eket
kell írni. A kutatás magyarázata: eltérő architektúra-stílus (vertical-slice/CQRS vs.
nagyobb, réteges rendszer) áll a háttérben — kontextus-függő ajánlás, nem egymást kizáró
igazság.

**2. Elrejthető-e az egy-író korlát ingyen? (SQ-02, nem valódi ellentmondás, hanem két
réteg.)** "El lehet rejteni"-oldal: Prisma mindig `BEGIN IMMEDIATE`-et választ SQLite-on
alkalmazáskód-változtatás nélkül; Doctrine SAVEPOINT-tal sikeresen emulálja a beágyazott
tranzakciókat; az optimista zárolás motor-független. "Nem lehet elrejteni ingyen"-oldal: a
Django-vita opt-in konfigurációs kapcsolóban végződött; a hivatalos Django-doksi "válts
motort" tanácsot ad; az Ecto dokumentáltan kikapcsol egy funkciót. A megkülönböztetés: A)
azokra az esetekre igaz, ahol a réteg **saját maga, egyszer, tervezési időben** dönthet a
viselkedésről; B) azokra, ahol az **alkalmazás konkrét, futásidejű logikája** ütközik a
motor korlátjával — ott a döntésnek alkalmazás-specifikus ára van, amit csak a
fejlesztő ismerhet.

**3. "SERIALIZABLE" SQLite-ban vs. a Berenson-kritika (SQ-02, látszólagos feszültség, ami
valójában megerősítés.)** SQLite magabiztosan állítja: minden tranzakció SERIALIZABLE.
Berenson et al. bizonyítja, hogy az izolációs szint-nevek kétértelműek. Nem
ellentmondás: az SQLite-nál a SERIALIZABLE szokatlanul "erős" és "olcsó", mert nem
lock-alapú konfliktus-detektálással, hanem az egyidejű írás fizikai kizárásával éri el —
más motorokon (Postgres SSI) ugyanaz a név bonyolultabb mechanizmussal valósul meg. A
névazonosság nem garantálja a mechanizmus-azonosságot.

**4. "Nincs egyetlen abszolút módszer" vs. "mindenki mégis BM25-szerű alapértelmezést ad"
(SQ-03, filozófia-különbség, nem forráskonfliktus.)** PostgreSQL retorikája:
rangsoroló-függvényei "csak példák", szabadon cserélhetők. SQLite FTS5/Elasticsearch/
Meilisearch/Typesense: beépített, nehezen lecserélhető alapértelmezés. Ez a motorok
tervezési filozófiájának eltérése, nem logikai ellentmondás.

**5. RRF "nem igényel hangolást" vs. a `rank_constant` paraméter létezése (SQ-03, enyhe
feszültség, nem valódi ellentmondás.)** Elasticsearch: "RRF requires no tuning" — mégis
van egy állítható `rank_constant`. Az eredeti Cormack-cikk ugyanezt a mintát mutatja: a
`k=60`-at egy pilot-vizsgálatban rögzítették, és utána nem hangolták tovább. Mindkét
forrás konzisztensen azt állítja: van hangolható paraméter, de a módszer szándéka szerint
nem érdemes rajta módszeresen hangolni.

**6. A "szerződés-teszt" hatóköre Fowlernél szűkebb, Rainsbergernél tágabb (SQ-04, nem
valódi ellentmondás, hanem szűkebb/tágabb olvasat.)** Fowler kifejezetten külső
szolgáltatásra szabja a definíciót. Rainsberger bármely, több osztály által
implementálható interfészre alkalmazza, saját kódbázison belülre is (Repository). Fowler
esete a Rainsberger-féle tágabb definíció speciális esete — a D-34 kontextusában a
tágabb olvasat a releváns.

**7. "Subclass to Test" — antipattern vagy sem? (SQ-04, Vitatott, a tartalom nem
feltárt.)** Létezik egy c2-wiki oldal "SubclassToTestAntiPattern" néven, és van egy
Rainsberger-előadás "Why I Don't Consider Subclass to Test An Anti-Pattern" címmel — a
cím önmagában megerősíti a vita tényét. A kutatás nem tudta feltárni az érvelést
egyik oldalról sem (a c2-wiki JavaScript-védett, az előadás fizetős), csak a vita
**létezését** dokumentálja. Összecseng azzal, hogy Rainsberger saját 2021-es
visszatekintésében explicit áttért az öröklés-alapú mintáról a kompozíció-alapúra — ez
erősen sugallja, de nem bizonyítja, hogy a szakmai konszenzus elmozdult.

**8. YAGNI mint normatív állítás vs. Rainsberger tesztelhetőségi érve (SQ-04, nem
ellentmondás, hanem két külön kérdésre adott válasz, amit könnyű összekeverni.)** Fowler:
egy jövőbeli, bizonytalan igényre épített absztrakció rossz befektetés. Rainsberger: egy
Repository-mögötti szerződés-teszt javítja a *mai* tesztelhetőséget. A kutatás explicit
kiemeli a kockázatot: a D-34 indoklása a gyengébb (jövő-bizonytalan) érvre hivatkozik,
miközben az erősebb, létező érv a jelen-orientált tesztelhetőségi érv lenne.

---

## 7. Hiányok

Ez a szakasz a négy kör `gaps.md` fájljainak összesítése — ideértve azt is, ahol a
lekérés AI-összefoglalót adott a valódi oldal helyett, ahogy a feladat kéri, szépítés
nélkül.

**Visszatérő módszertani probléma mind a négy körben: a WebFetch-eszköz gyakran nem a
valódi oldalszöveget adta vissza szó szerint, hanem kitalált fejezetcímekkel tagolt,
AI-átfogalmazott verziót — annak ellenére, hogy a prompt kifejezetten szó szerinti
szöveget kért.** Ez T1-es forrásoknál is előfordult (pl. Oracle DAO-oldal, Fowler
Yagni-oldal, Fowler Unit of Work-oldal, Berenson et al. PDF, SQLAlchemy izolációs-szint
oldalak, Knex doksi). Ahol volt idő második, kereszt-ellenőrző lekérésre (pl. Table Data
Gateway, Neward Vietnam-esszé), ott a bizonyosság Magas maradt; ahol nem, ott csak az
idézőjelbe tett mondatok kezelendők szó szerintinek, minden más parafrázisnak — ez
minden SQ-körben explicit csökkentette a bizonyossági szintet, **függetlenül a forrás
presztízsétől**.

**Konkrét, tartalmi hiányok, SQ-onként:**

- **Eric Evans DDD-könyvének szó szerinti Repository-szövege (SQ-01).** A WebFetch-eszköz
  **megtagadta** a szó szerinti idézést mindkét próbált forrásból (hivatalos DDD
  Reference PDF, harmadik féltől hosztolt teljes könyv), szerzői jogi okra hivatkozva —
  ez eszközkorlát, nem a tartalom elérhetetlensége.
- **Greg Young "DDD: The Generic Repository" (2009) (SQ-01).** A Wayback Machine-en át
  próbált elérést a WebFetch `SITE_BLOCKED` hibával utasította el; a módszertan szerint
  ezt nem kerülték meg.
- **"Repository vs DAO vs Data Mapper vs Gateway" — nincs egyetlen dedikált forrás
  (SQ-01).** A megkülönböztetés a kutatás saját rekonstrukciója, nem egy forrás kimondott
  állítása.
- **Drizzle SQLite-specifikus tranzakció-konfigurációs felülete (SQ-02) — magas
  prioritású hiány, mert ez a rendszer saját ORM-je.** A hivatalos oldal fetchje csak
  Postgres-specifikus interfészt hozott vissza; a SQLite-adapter tényleges
  DEFERRED/IMMEDIATE-viselkedése ismeretlen maradt ebben a körben.
- **Berenson et al. (1995) csak egyetlen, nem-kanonikus forrásból, kereszt-ellenőrzés
  nélkül (SQ-02).**
- **A Kysely issue #877 karbantartói válasza (SQ-02)** — a GitHub-oldal renderelt
  kommentjeit a fetch-eszköz nem szolgáltatta.
- **DEFERRED vs. IMMEDIATE tranzakciók konkrét, számszerűsített teljesítmény-
  összehasonlítása (SQ-02)** — nem került elő; csak kvalitatív leírás van arra, hogy ez
  kompromisszum.
- **SQLite FTS5 `bm25()` explicit összemérhetetlenségi nyilatkozata (SQ-03)** — a
  hivatalos oldal nem mondja ki explicit egy mondatban; a kutatás saját, formulából
  levezetett következtetése, nem idézett tény.
- **OpenSearch hibrid keresés normalizáló-processzorának dokumentációja (SQ-03)** —
  ismételt kísérlet (404/üres navigációs váz) sem hozott valódi tartalmat; ez közvetlen
  bizonyíték lett volna arra, miért igényel a pontszám-alapú fúzió motoronkénti
  normalizálást.
- **Gyakorlói "beszámoló egy megbukott keresés-absztrakcióról" (SQ-03)** — több
  kereséssel sem került elő dedikált beszámoló; lehet, hogy a fejlesztők inkább a
  hivatalos doksiban dokumentálják a korlátokat, nem külön posztban panaszkodnak.
- **Weaviate és sqlite-vec pontos-vs-közelítő nyilatkozata elsődleges forrásból (SQ-03)**
  — nem sikerült megerősíteni.
- **Közös vektor-kliens API-szabvány (SQ-03)** — nem került elő; ez inkább evidence of
  absence, mint absence of evidence (a terület gyártónkénti szigetekből áll).
- **Konkrét, formális, több-implementációs szerződés-tesztkészlet konkrét elbukása
  (SQ-04)** — nem került elő ilyen, névvel azonosítható nyílt forráskódú esettanulmány;
  a talált legjobb bizonyíték (Neon, dev.to) "teszt-motor vs. éles-motor" mintára
  vonatkozik, nem "N adapter közös suite-ja" mintára.
- **Empirikus adat arra, hogy megtérül-e egy port/adapter-réteg előre megépítése egyetlen
  implementációhoz (SQ-04) — nincs.** A célzott keresés kizárólag véleményblogokat
  hozott; ezt a kutatás explicit, szépítés nélkül evidence of absence-ként rögzíti.
- **"Subclass to Test" vita tartalma (SQ-04)** — a c2-wiki oldal JavaScript-védett, a
  Rainsberger-előadás fizetős; csak a vita létezése dokumentált, az érvelés nem.
- **A tranzakciós szemantika és konkurrenciakezelés kimaradása a szerződés-tesztekből
  (SQ-04)** — nincs erre kifejezett, elsődleges, normatív forrás Fowlertől vagy
  Rainsbergertől; csak közvetve támasztható alá.
- **GitHub könyvtárlistázó (`tree`) nézetek (SQ-04)** — robots.txt blokkolta (pl. Rails
  `activerecord/test/cases` teljes tartalma); az egyes fájlok (`blob`/`raw`) viszont
  elérhetők voltak ugyanazon a domainen.
- **Prisma, Django ORM, Hibernate adapter/dialect-tesztelési architektúrája (SQ-04)** —
  a kör kapacitása csak SQLAlchemy, Ecto és ActiveRecord vizsgálatára futotta.

---

## 8. Minden meglátogatott link

A négy kör `links.md` fájljainak uniója. **T1** = elsődleges forrás (a minta szerzőjének
saját írása, hivatalos dokumentáció, peer-reviewed); **T2** = megbízható másodlagos vagy
gyártó saját terméke/issue trackere; **T3–T6** = fórum, blog, vélemény, aggregátor,
marketing (finomabb belső skála, ahol a forrásanyag jelezte). "Archiválva" = ténylegesen
letöltött és forrásként használt; "csak link" = megtalált, keresési találatként látott,
de nem (vagy nem forrásként) megnyitott; "AI-összefoglaló/üres" = megnyitva, de nem
használt, mert a lekérés nem a valódi szöveget adta vissza.

### SQ-01 — Melyik minta, és hol a varrat

| URL | Tier | Státusz | Megjegyzés |
|---|---|---|---|
| alistair.cockburn.us/hexagonal-architecture | T1 | Archiválva | Cockburn saját cikke, szó szerint ellenőrzött |
| martinfowler.com/eaaCatalog/repository.html | T1 | Archiválva | Szerző: Hieatt & Mee, nem Fowler |
| martinfowler.com/eaaCatalog/dataMapper.html | T1 | Archiválva | Fowler |
| martinfowler.com/eaaCatalog/gateway.html | T1 | Archiválva | Fowler |
| martinfowler.com/eaaCatalog/tableDataGateway.html | T1 | Archiválva | 2 lekéréssel kereszt-ellenőrizve |
| martinfowler.com/eaaCatalog/rowDataGateway.html | T1 | Archiválva | Fowler |
| odbms.org (Neward, "Vietnam of Computer Science" PDF) | T1 | Archiválva | 2 lekéréssel kereszt-ellenőrizve |
| mikehadlow.blogspot.com/2009/01/eric-evans-on-repositories.html | T3 | Archiválva | Másodlagos, állítólag szó szerint idézi Evanst |
| docs.nestjs.com/techniques/sql | T1 | Archiválva | Hivatalos NestJS doksi |
| codeopinion.com/avoiding-the-repository-pattern-with-an-orm/ | T3 | Archiválva | Comartin, AI-átstrukturált fetch |
| oracle.com/java/technologies/dataaccessobject.html | T1 | Archiválva | Oracle DAO, AI-átfogalmazott fetch |
| refactoring.guru/smells/speculative-generality | T3 | Archiválva | Speculative Generality smell |
| codeopinion.com/do-you-really-need-that-abstraction-or-generic-code-yagni/ | T3 | Archiválva | Comartin, egy implementációra épített interfész |
| martinfowler.com/bliki/Yagni.html | T1 | Archiválva | Fowler saját bliki |
| thereformedprogrammer.net/is-the-repository-pattern-useful-with-entity-framework/ | T2 | Archiválva | Jon P Smith, kiegyensúlyozott elemzés |
| codebetter.com/.../ddd-the-generic-repository (+ Wayback) | T3 | Csak link | **BLOKKOLVA**, SITE_BLOCKED a Wayback-en |
| lostechies.com/.../favor-query-objects-over-repositories | T3 | Csak link | Jimmy Bogard, nem fetchelve |
| rob.conery.io/.../repositories-on-top-unitofwork | T3 | Csak link | Rob Conery, nem fetchelve |
| cockneycoder.wordpress.com/.../why-entity-framework-renders-the-repository-pattern-obsolete | T3 | Csak link | Isaac Abraham, nem fetchelve |
| tech.pro/blog/1191/say-no-to-the-repository-pattern-in-your-dal | T3 | Csak link | Nem fetchelve |
| blog.sapiensworks.com/.../The-Generic-Repository-Is-An-Anti-Pattern.aspx | T3 | Csak link | Nem fetchelve |
| domainlanguage.com/ddd/reference/ | T1 | AI-összefoglaló | Nem archiválva forrásként |
| domainlanguage.com/.../DDD_Reference_2015-03.pdf | T1 | Megtagadva | WebFetch szerzői jogi okból megtagadta a szó szerinti idézést |
| fabiofumarola.github.io/nosql/readingMaterial/Evans03.pdf | T4 | Megtagadva | Ugyanígy megtagadva |
| martinfowler.com/articles/gateway-pattern.html | T1 | Csak link | Fowler 2021-es bővített Gateway-cikke, nem fetchelve |
| en.wikipedia.org/wiki/Hexagonal_architecture_(software) | T5 | Csak link | Aggregátor, nem fetchelve |
| en.wikipedia.org/wiki/Table_data_gateway, .../Row_data_gateway, .../Data_mapper_pattern | T5 | Csak link | Aggregátorok, nem fetchelve |
| grokipedia.com/page/table_data_gateway | T0/T5 | Kerülve | AI-generált aggregátor-gyanús, tudatosan kerülve |
| informit.com/articles/article.aspx?p=1398618 | T2 | Csak link | Nem fetchelve |
| learn.microsoft.com/.../infrastructure-persistence-layer-design | T2 | Csak link | Más ökoszisztéma (.NET), nem fetchelve |
| blog.elmah.io/the-repository-pattern-is-simple-yet-misunderstood/ | T3 | Csak link | Nem fetchelve |
| infoq.com/interviews/eric-evans-ddd-interview | T2 | Csak link | Potenciális Evans-elsőkéz-forrás, nem fetchelve |
| infoworld.com/.../design-patterns-that-i-often-avoid-repository-pattern.html | T2/T3 | Csak link | Nem fetchelve |

### SQ-02 — Párhuzamosság és tranzakciók

| URL | Tier | Státusz | Megjegyzés |
|---|---|---|---|
| sqlite.org/lang_transaction.html | T1 | Archiválva | DEFERRED/IMMEDIATE/EXCLUSIVE, SQLITE_BUSY |
| sqlite.org/wal.html | T1 | Archiválva | "only one writer at a time" |
| sqlite.org/lockingv3.html | T1 | Archiválva | Zárolási állapotgép |
| sqlite.org/isolation.html | T1 | Archiválva | SERIALIZABLE, SQLITE_BUSY_SNAPSHOT — a kör legfontosabb SQLite-forrása |
| sqlite.org/whentouse.html | T1 | Archiválva | "mikor NE használj SQLite-ot" |
| martinfowler.com/eaaCatalog/unitOfWork.html | T1 | Archiválva | AI-átstrukturált fetch |
| cs.cmu.edu/~15721-f24/papers/Critique_of_ANSI_Isolation_Levels.pdf | T1 | Archiválva | Berenson et al. 1995, nem-kanonikus másolat, kereszt-ellenőrzés nélkül |
| prisma.io/docs/orm/prisma-client/queries/transactions | T1 | Archiválva | Izolációs szint táblázat motoronként |
| github.com/prisma/prisma/issues/25587 | T2 | Archiválva | Kulcsbizonyíték: SQLite-on mindig BEGIN IMMEDIATE |
| knexjs.org/guide/transactions.html | T1 | Archiválva | "Not supported by oracle and sqlite" |
| docs.djangoproject.com/en/6.1/ref/databases/ | T1 | Archiválva | transaction_mode OPTIONS, "válts motort" ajánlás |
| code.djangoproject.com/ticket/29280 | T2 | Archiválva | A kör legfontosabb esettanulmánya |
| orm.drizzle.team/docs/transactions | T1 | Archiválva | Csak Postgres-specifikus interfész — SQLite-rész hiányzik |
| kysely-org.github.io/.../TRANSACTION_ISOLATION_LEVELS.html | T1 | Archiválva | 5 izolációs szint konstans |
| github.com/kysely-org/kysely/issues/877 | T2 | Archiválva | Maintainer-válasz nem elérhető |
| doctrine-project.org/.../transactions.html | T1 | Archiválva | "guaranteed to be at least READ_COMMITTED" |
| api.rubyonrails.org/.../Optimistic.html | T1 | Archiválva | lock_version, StaleObjectError |
| docs.hibernate.org/orm/5.2/.../Locking.html | T1 | Archiválva | Csendes lock-mode degradáció |
| docs.sqlalchemy.org/en/20/core/connections.html | T1 | Archiválva | Motoronkénti doksi-oldalak |
| docs.sqlalchemy.org/en/20/dialects/sqlite.html | T1 | Archiválva | sqlite3 legacy mód megtörheti a SERIALIZABLE-t |
| tenthousandmeters.com/blog/sqlite-concurrent-writes... | T3 | Archiválva | Informális benchmark, kiegészítő |
| ecto-sqlite3.hexdocs.pm/0.5.2/Ecto.Adapters.SQLite3.html | T1 | Archiválva | Async sandbox tesztelés dokumentáltan nem támogatott |
| docs.hibernate.org/.../Portability.html | T1 | Fetchelve, nem releváns | Nem tartalmazta a keresett tartalmat |
| jakarta.ee/specifications/persistence/3.0/... | T1 | Csak link | JPA spec, nem fetchelve (tool-budget) |
| vladmihalcea.com/a-beginners-guide-to-transaction-isolation-levels... | T2 | Csak link | Nem fetchelve |
| render.com/articles/how-to-migrate-from-sqlite-to-postgresql | T3 | Csak link | Nem fetchelve |
| code.djangoproject.com/ticket/29062 | T2 | Csak link | Rokon ticket, nem fetchelve |
| code.djangoproject.com/ticket/9409 | T2 | Csak link | Korai (2008) ticket, nem fetchelve |
| sqlite.org/forum/info/722e181400b0ae09ea64446c614fe29ee3e313139fbc1c96e054913197a4a95b | T3 | Csak link | Fórumbejegyzés, alacsony prioritás |

### SQ-03 — Keresés hordozható felület mögött

| URL | Tier | Státusz | Megjegyzés |
|---|---|---|---|
| sqlite.org/fts5.html | T1 | Archiválva | bm25() irány, tokenizálók |
| postgresql.org/docs/current/textsearch-controls.html | T1 | Archiválva | ts_rank, "only examples" |
| postgresql.org/docs/current/textsearch-intro.html | T1 | Archiválva | Bevezető |
| dev.mysql.com/doc/refman/8.4/en/fulltext-search.html | T1 | Archiválva | MATCH/AGAINST, query expansion |
| elastic.co/.../query-filter-context.html | T1 | Archiválva | query vs. filter context |
| elastic.co/.../consistent-scoring | T1 | Archiválva | _score nem stabil ismételt futtatásnál sem |
| meilisearch.com/docs/learn/relevancy/relevancy | T1 | Archiválva | Bucket-sort, nem BM25 |
| typesense.org/docs/guide/ranking-and-relevance.html | T1 | Archiválva | text_match_type |
| elastic.co/.../rrf.html | T1 | Archiválva | "RRF requires no tuning" |
| cormack.uwaterloo.ca/cormacksigir09-rrf.pdf | T1 | Archiválva | Eredeti RRF-cikk, SIGIR 2009 |
| github.com/pgvector/pgvector | T1 | Archiválva | Exact by default, HNSW/IVFFlat |
| raw.githubusercontent.com/asg017/sqlite-vec/main/README.md | T1 | Archiválva | Pre-v1, exact/approx nem explicit |
| qdrant.tech/documentation/search/search/ | T1 | Archiválva | exact flag |
| qdrant.tech/articles/vector-search-filtering/ | T2 | Archiválva | Vendor-cikk, filterable HNSW |
| docs.weaviate.io/weaviate/config-refs/distances | T1 | Archiválva | Távolságmértékek |
| milvus.io/docs/index.md | T1 | Archiválva | FLAT = egyetlen garantáltan pontos |
| github.com/facebookresearch/faiss/wiki/Faiss-indexes | T1 | Archiválva | Exhaustive/approx táblázat |
| github.com/facebookresearch/faiss/wiki/MetricType-and-distances | T1 | Archiválva | Inner product ≠ cosine normalizálás nélkül |
| github.com/ankane/searchkick | T1 | Archiválva | Kizárólag ES/OpenSearch |
| django-haystack.readthedocs.io/en/latest/ | T1 | Archiválva | "unified API" |
| django-haystack.readthedocs.io/en/latest/backend_support.html | T1 | Archiválva | Support-mátrix, "More Like This" hiánya |
| laravel.com/docs/12.x/scout | T1 | Archiválva | database/collection/harmadik fél motorok |
| docs.hibernate.org/search/7.2/reference/en-US/html_single/ | T1 | Archiválva | Backend-fogalom, kiszökő ajtók |
| en.wikipedia.org/wiki/SQL:2023 | T5 | Archiválva | Csak orientációra, nincs vektor-típus említve |
| docs.opensearch.org/.../normalization-processor/ | T1 | AI-összefoglaló/üres | 404/redirect-váz, nem sikerült elolvasni |
| github.com/erikbern/ann-benchmarks | T2 | Csak link | De facto benchmark-protokoll, nem API-szabvány |
| db-engines.com/en/system/Elasticsearch... | T3 | Csak link | Összehasonlító oldal |
| postgresql.org/docs/current/textsearch-indexes.html | T1 | Csak link | GIN/GiST index-struktúra |
| typesense.org/docs/30.2/api/vector-search.html | T1 | Csak link | Follow-up téma |
| qdrant.tech/documentation/concepts/search/ | T1 | AI-összefoglaló/üres | Üres tartalom |
| qdrant.tech/documentation/concepts/filtering/ | T1 | AI-összefoglaló/üres | Nem tárgyalta a pre/post-filtering kérdést |
| docs.opensearch.org/.../hybrid-search/index/ | T1 | AI-összefoglaló/üres | Csak navigációs menü |
| weaviate.io/developers/weaviate/config-refs/distances | T1 | AI-összefoglaló/üres | Csak redirect-infó |
| typesense.org/docs/latest/api/{documents,search}.html#ranking-and-relevance | T1 | AI-összefoglaló/üres | Navigációs váz |
| elastic.co/guide/.../scoring-theory.html (Definitive Guide) | T2 | Fetchelve, nem használt | Elavult (BM25 előtti) modell, AI-átstrukturált |

### SQ-04 — Hogyan tartható őszinte egy illesztő

| URL | Tier | Státusz | Megjegyzés |
|---|---|---|---|
| martinfowler.com/bliki/ContractTest.html | T1 | Archiválva | Fowler saját definíciója |
| martinfowler.com/bliki/Yagni.html | T1 | Archiválva | Költségkategóriák, Kohavi-idézet |
| blog.thecodewhisperer.com/permalink/abstract-test-cases-20-years-later | T1 | Archiválva | Rainsberger, c2-wiki vita újraközlése |
| testcontainers.com/getting-started/ | T1 | Archiválva | "real services... without mocks" |
| github.com/sqlalchemy/sqlalchemy/blob/main/README.dialects.rst | T1 | Archiválva | testing.suite + Requirements zászlók |
| ecto.hexdocs.pm/testing-with-ecto.html | T1 | Archiválva | SQL Sandbox minta |
| docs.pact.io/consumer/contract_tests_not_functional_tests | T1 | Archiválva | "does not check for side effects" |
| raw.githubusercontent.com/rails/rails/main/activerecord/test/cases/test_case.rb | T1 | Archiválva | Közös TestCase + adapter-alosztályok, forráskód |
| neon.com/blog/testing-sqlite-postgres | T4 | Archiválva | Vendor-blog, technikai állítások ellenőrizhetők |
| dev.to/enderyentar/sqlite-doesnt-enforce-foreign-keys... | T6 | Archiválva | 1241/1241 zöld teszt, három valós hiba |
| github.com/rails/rails/tree/main/activerecord/test/cases | — | Blokkolva | robots.txt (GitHub tree-nézet) |
| wiki.c2.com/?SubclassToTestAntiPattern= | — | AI-összefoglaló/üres | JavaScript-védett, üres váz |
| online-training.jbrains.ca/courses/36224/lectures/2957384 | — | Csak link | Fizetős kurzus, nem nyitva |
| beware-the-integrated-tests-scam.jbrains.ca | T1 | Csak link | Rainsberger fő esszéje, lead más körnek |
| wiki.c2.com/?AbstractTestCases | T3 | Csak link | Eredeti c2-wiki, Rainsberger újraközli |

---

**Szó szerinti idézetek forrása**: minden idézet a fenti szakaszokban a hivatkozott
forrás-URL-ről származik, a kutatási körök `megallapitasok.md` fájljaiban rögzített
kimásolás szerint. A bizonyossági szintek (Magas/Közepes/Alacsony) és a `[VERBATIM-
BIZONYTALAN]`/`[FETCH-ÓVATOSSÁG]` jelölések a forrásanyagban jelzett módon lettek
kezelve — ahol a forrásanyag közepes vagy alacsony bizonyosságot jelzett egy idézetre,
azt ez a kivonat is jelezte a szövegkörnyezetben.
