# Keresések — minden lefuttatott lekérdezés

Kampány: `adatbazis-illeszto` · 2026-09-09


---

## SQ-01 — Melyik illesztési minta, és hol a varrat

# SQ-01 — Elvégzett keresések

Minden WebSearch-lekérdezés, amit ez a kör futtatott, időrendben. (A gépi napló
`01-search-log/queries.jsonl`-ben is szerepel; ez a fájl az olvasható, kommentált
változat.)

## 1. kör — tájékozódás (a mintanevek és a terep megismerése)

1. `Alistair Cockburn hexagonal architecture ports and adapters cockburn.us` — cél: a
   Cockburn-oldal megtalálása. Eredmény: közvetlenül megtaláltuk
   `alistair.cockburn.us/hexagonal-architecture`-t.
2. `Martin Fowler Repository pattern PoEAA martinfowler.com` — cél: a Fowler-katalógus
   Repository-oldalának megtalálása.
3. `Martin Fowler Data Mapper Gateway Table Data Gateway Row Data Gateway pattern` — cél:
   a másik négy PoEAA-minta oldalainak megtalálása egy lekérdezéssel.
4. `"repository is a dumpster fire" OR "don't use repository pattern with an ORM"` — cél:
   a kritikai irányzat feltérképezése, a feladatban kiemelt cím nyomán.

## 2. kör — célzott, elsődleges forrásra irányuló és kritikai keresések

5. `"Repository is a Dumpster Fire"` — pontos cím-keresés. **Nem hozott releváns
   találatot** — ez a konkrét cím / cikk nem azonosítható ebben a formában (lásd
   `gaps.md`). Lehet, hogy a feladatleírásban szereplő cím parafrázis egy másik,
   hasonló hangvételű cikkre (pl. Sapiens Works "The Generic Repository Is An
   Anti-Pattern"), nem szó szerinti cím.
6. `Eric Evans Domain-Driven Design Repository pattern definition aggregate` — Evans
   elsődleges szövegének felkutatására.
7. `generic repository anti-pattern Jimmy Bogard query objects` — a "generikus
   repository" vita szereplőinek azonosítására.
8. `NestJS documentation database techniques repository recommendation` — TS/Node
   ökoszisztéma vizsgálatához.
9. `"leaky abstraction" repository pattern N+1 query ORM` — a dokumentált bukások
   (SQ-01 4. pont) feltérképezésére.
10. `Ted Neward "Vietnam of Computer Science" object relational mapping` — az ORM-kritika
    klasszikus szövegének megtalálására.

## 3. kör — elsődleges forrás finomítás és gap-zárás

11. `domainlanguage.com DDD reference Evans repository pdf` — az Evans-féle hivatalos DDD
    Reference PDF felkutatása.
12. `docs.nestjs.com database sql typeorm official documentation` — a pontos NestJS
    dokumentáció-URL megtalálására.
13. `"generic repository" anti-pattern criticism Jimmy Bogard blog` — Bogard eredeti
    cikkének felkutatására (a cikk maga nem lett direkt fetchelve, csak linkként került
    elő egy másik forráson keresztül).
14. `mikehadlow "Eric Evans on Repositories" quote QCon` — az Evans-idézetek másodlagos
    forrásának pontosítására.
15. `Oracle Core J2EE Patterns "Data Access Object" definition catalog` — a DAO minta
    hivatalos definíciójának megtalálására, hogy a Repository/DAO-különbséget
    forrás-alapon lehessen felépíteni.

## 4. kör — az 5. és 7. alkérdésre célzott keresés

16. `should you create an interface for a single implementation speculative generality
    YAGNI abstraction` — az "egy megvalósítás, épüljön-e port" kérdéshez (SQ-01 5. pont).
17. `hexagonal architecture separate port per data store search index vs repository
    different interfaces` — a "két port vagy egy" kérdéshez (SQ-01 7. pont). **Nem hozott
    releváns, dedikált találatot** — ez evidence of absence-ként van rögzítve
    `megallapitasok.md` 7. szakaszában és `gaps.md`-ben.

## Nyelvi lefedettség

Ez a kör **kizárólag angol nyelvű** keresést futtatott. A téma (szoftverarchitektúra-
minták, elsődleges források mind angolul publikálva: Cockburn USA, Fowler UK/Thoughtworks,
Evans USA, NestJS nemzetközi angol dokumentáció) nem magyar-specifikus, ezért magyar nyelvű
keresési kört nem indítottunk. Ezt explicit rögzítjük, ahogy a módszertan kéri: nem
találtunk arra utaló jelet, hogy bármelyik elsődleges forrásnak lenne magyar nyelvű
megfelelője vagy hogy a magyar szakirodalom bármi újat tenne hozzá ehhez a konkrét,
angolszász eredetű mintakatalógushoz.

## Nem futtatott, de érdemes lenne (jövőbeli kör számára)

- `Vaughn Vernon "Implementing Domain-Driven Design" repository aggregate` — a
  Repository-DAO-Data-Mapper különbségtétel dedikált forrásához.
- `Drizzle ORM repository pattern recommendation` / `Kysely repository pattern` — a
  ténylegesen használt ORM saját állásfoglalásához.
- `Jimmy Bogard "favor query objects over repositories" lostechies` — a query-object
  irányzat elsődleges cikkének közvetlen eléréséhez (eddig csak linkként került elő).
- `Greg Young generic repository codebetter wayback` — más Wayback-pillanatkép vagy
  tükör-forrás keresése, mivel az első próbálkozás blokkolva volt.


---

## SQ-02 — Párhuzamosság és tranzakciók motorok között

# SQ-02 — Elvégzett keresések

Minden WebSearch-lekérdezés, amit ez a kör futtatott, időrendben. (A gépi napló
`01-search-log/queries.jsonl`-ben is szerepel; ez a fájl az olvasható, kommentált
változat.)

## 1. kör — tájékozódás (5 kérdéskör egyszerre indítva)

1. `SQLite WAL mode busy_timeout BEGIN IMMEDIATE site:sqlite.org` — cél: a hivatalos
   SQLite tranzakció/WAL-doksi megtalálása. Eredmény: közvetlenül a SQLite fórum és
   `rescode.html` jelentek meg elsőként, de a `lang_transaction.html` és `wal.html`
   URL-eket már ismertük a domain-tudásból, közvetlenül fetcheltük.
2. `Martin Fowler Unit of Work pattern martinfowler.com eaaCatalog` — cél: a Fowler UoW
   oldal megtalálása. Eredmény: közvetlenül megtaláltuk `martinfowler.com/eaaCatalog/
   unitOfWork.html`-t.
3. `Berenson "A Critique of ANSI SQL Isolation Levels" pdf Microsoft Research` — cél: az
   alapmű elérhető PDF-másolatának megtalálása. Eredmény: a hivatalos Microsoft Research
   oldal és az ACM SIGMOD Record oldal is megjelent, de mindkettő valószínűleg
   paywall/absztrakt-only; a CMU kurzus-oldal (`cs.cmu.edu/~15721-f24/...`) adott
   közvetlenül elérhető PDF-et.
4. `Django documentation SQLite notes transactions "database is locked" single writer` —
   cél: a Django hivatalos SQLite-jegyzetek és kapcsolódó ticketek megtalálása. Eredmény:
   megtalálta a `tenthousandmeters.com` blogot és a Django ticket #29280-at (bár a cím
   akkor még nem volt látható, ezt egy második kereséssel erősítettük meg).
5. `SQLAlchemy documentation isolation level portability across backends` — cél: a
   SQLAlchemy izolációs szint doksi megtalálása. Eredmény: `docs.sqlalchemy.org/en/20/
   core/connections.html` és egy releváns GitHub Discussion (#8252) is megjelent (utóbbi
   nem lett fetchelve).

## 2. kör — célzott, hivatalos forrásra irányuló keresések (5 kérdéskör egyszerre)

6. `SQLite "Appropriate Uses For SQLite" whentouse.html server client concurrency writer`
   — cél: a hivatalos "mikor NE használj SQLite-ot" oldal. Közvetlen találat.
7. `Prisma documentation transactions isolation level "SQLite" concurrent write` — cél: a
   Prisma hivatalos tranzakció-doksi és kapcsolódó issue-k. Közvetlen találat mindkettőre
   (a hivatalos doksi és a #25587-es issue).
8. `Knex.js documentation transaction isolation level per database` — cél: a Knex
   hivatalos tranzakció-doksi. Közvetlen találat.
9. `Rails ActiveRecord isolation level documentation "differs" database adapter` — cél:
   Rails izolációs szint doksi. Eredmény: főleg forráskód-linkeket és API-oldalakat hozott,
   ezért egy külön, célzottabb keresést indítottunk (17. tétel) az optimista zárolásra.
10. `Hibernate JPA documentation isolation level portability not all databases` — cél:
    Hibernate portabilitási doksi. Eredmény: a `Portability.html` oldalt találta meg
    elsőként, ami — kiderült a fetch után — NEM tartalmazta a keresett tartalmat (lásd
    `links.md`, "Fetchelt, de nem archivált" szakasz).

## 3. kör — a hiányok pótlása (5 kérdéskör egyszerre)

11. `Jakarta Persistence JPA specification transaction isolation level not specified
    vendor-specific` — cél: a JPA hivatalos spec-szövege. **Nem lett fetchelve ebben a
    körben** (ld. `gaps.md`) — a keresés maga megtalálta a spec URL-jét
    (`jakarta.ee/specifications/persistence/3.0/...`), de a tool-budget más, magasabb
    prioritású hiányok pótlására lett fordítva.
12. `Django "Notes on transactions" OR "SQLite notes" docs.djangoproject.com database
    locked isolation` — cél: a Django hivatalos SQLite-szakasz pontos URL-je és a ticket
    #29280 megerősítése. **Sikeres** — mindkettő közvetlenül megjelent, plusz két rokon
    ticket (#29062, #9409), amiket leadként rögzítettünk.
13. `Ecto DBConnection pool_size 1 SQLite Elixir documentation single connection` — cél:
    az Ecto SQLite3 adapter hivatalos doksija. **Sikeres** — közvetlen találat
    (`hexdocs.pm/ecto_sqlite3/...`, ami átirányított `ecto-sqlite3.hexdocs.pm`-re).
14. `Drizzle ORM documentation transactions SQLite better-sqlite3 isolation` — cél: a
    Drizzle hivatalos tranzakció-doksi. **Részben sikeres** — megtaláltuk az oldalt, de a
    fetchelt tartalom csak Postgres-specifikus interfészt tartalmazott, SQLite-specifikus
    rész nem volt látható (gap).
15. `"SELECT FOR UPDATE" SQLite not supported alternative optimistic locking version
    column pattern` — cél: a zárolási felület-alakok (5. pont) irodalmának feltérképezése.
    Nem hozott közvetlenül újat a már megtalált Django-idézeten felül, de megerősítette,
    hogy ez egy jól ismert, gyakran tárgyalt mintázat (pl. peewee ORM "Hacks" oldala,
    CockroachDB blog).

## 4. kör — a 6. és a maradék ORM-lefedettség pótlása (5 kérdéskör egyszerre)

16. `SQLite to PostgreSQL migration lessons learned "database is locked" concurrent
    writes experience report` — cél: konkrét migrációs esettanulmányok. Eredmény: több
    T3-as blogcikk (render.com, sesamedisk, aimadetools stb.) — ezeket **szándékosan nem
    fetcheltük**, mert a Django ticket #29280 (2. körben megtalálva) sokkal erősebb,
    T2-es, elsődleges forrású esettanulmányt adott ugyanarra a jelenségre.
17. `Rails ActiveRecord optimistic locking lock_version guide api.rubyonrails.org
    documentation` — cél: a Rails optimista zárolás hivatalos doksija. **Sikeres**,
    közvetlen találat.
18. `Kysely documentation transactions isolation level setIsolationLevel` — cél: Kysely
    izolációs szint API. **Sikeres**, közvetlen találat (`TRANSACTION_ISOLATION_LEVELS`
    apidoc-oldal) plusz egy releváns issue (#877).
19. `Doctrine DBAL documentation transaction isolation level TRANSACTION_SERIALIZABLE
    setTransactionIsolation` — cél: Doctrine DBAL hivatalos tranzakció-doksi. **Sikeres**,
    közvetlen találat a legfrissebb (4.4) verzióra.
20. `Hibernate ORM documentation "Locking" chapter pessimistic optimistic LockMode
    isolation level database specific` — cél: a Hibernate 10. körben elmulasztott
    tartalmának pótlása egy más oldalról. **Sikeres** — a `Locking.html` (5.2-es verzió)
    oldal adta a kulcsidézetet a csendes lock-mode degradációról.

## Összegzés — kör-effektivitás

- **20 keresés** összesen (WebSearch), **22 fetch** (WebFetch, ebből 21 vezetett
  archivált forráshoz, 1 — a Hibernate Portability.html — nem tartalmazott releváns
  anyagot).
- A második körtől kezdve minden keresés **konkrét, névvel megnevezett rendszer** (Prisma,
  Knex, Django stb.) hivatalos doksijára vagy issue trackerére irányult, nem általános
  kifejezésekre — ez összhangban van a search-playbook "routing to primary sources"
  elvével.
- A legmagasabb hozamú egyetlen keresés a 12. tétel volt (Django SQLite notes) — ez adta
  a kutatási kérdés legfontosabb bizonyítékát (ticket #29280).


---

## SQ-03 — Szöveges és vektoros keresés hordozható felület mögött

# SQ-03 — Elvégzett keresések

Minden WebSearch-lekérdezés, amit ez a kör futtatott, időrendben. (A gépi napló
`01-search-log/queries.jsonl`-ben is szerepel; ez a fájl az olvasható, kommentált
változat.) Emellett számos oldalt közvetlen WebFetch-hívással értünk el (ismert hivatalos
doksi-URL-ek: sqlite.org, postgresql.org, dev.mysql.com, elastic.co, github.com repók,
qdrant.tech, docs.weaviate.io, milvus.io, laravel.com, docs.hibernate.org stb.) — ezeket
nem WebSearch előzte meg, mert a domain és az aloldal neve a témaismeretből következett.

## 1. kör — tájékozódás és a legfontosabb pontok (2. és 7. kérdés) lefedése

1. `Elasticsearch documentation _score not comparable across queries or indices` — cél:
   hivatalos ES-forrás a pontszám-összemérhetetlenségről. Eredmény: a "Getting consistent
   scoring" hivatalos oldal (elastic.co) jelent meg elsőként, ez lett a fő forrás a 2.
   ponthoz.
2. `SQLite FTS5 bm25 not meaningful OR cannot be compared across queries` — cél: explicit
   SQLite-nyilatkozat az összemérhetetlenségről. Eredmény: nem került elő ilyen explicit
   mondat a sqlite.org oldalon (l. `gaps.md`); a találatok inkább harmadik féltől
   származó FTS5-wrapperekre mutattak.
3. `Cormack Clarke Buettcher 2009 Reciprocal Rank Fusion outperforms Condorcet` — cél: az
   eredeti RRF-cikk elérhető PDF-je. Eredmény: közvetlenül megtaláltuk a szerző saját
   (uwaterloo.ca) PDF-jét.
4. `OpenSearch hybrid search normalization processor min-max L2 RRF documentation` — cél:
   OpenSearch saját normalizáló-dokumentációja. Eredmény: a linkek helyesek voltak, de a
   WebFetch a tényleges oldalakon (redirect, 404) nem adott vissza tartalmat — 2. kísérlet
   is sikertelen maradt (l. lent, 2. kör 4. tétel és `gaps.md`).
5. `Qdrant exact search parameter documentation payload filtering HNSW` — cél: Qdrant
   saját exact/approximate keresési paraméter-doksija. Eredmény: a `qdrant.tech/
   documentation/search/search/` URL azonosítva, első fetch üres volt, második
   sikeres (l. 2. kör).
6. `Faiss wiki exact search vs approximate IndexFlat IndexIVF distance metrics` — cél: a
   Faiss saját GitHub-wikijének index- és metrika-oldalai. Eredmény: közvetlenül
   megtaláltuk mindkét releváns wiki-oldalt (`Faiss-indexes`, `MetricType-and-distances`).

## 2. kör — hiányok zárása (SQL-szabvány, absztrakciók bukása, Typesense/Qdrant pontosítás)

7. `SQL:2023 standard vector data type ISO/IEC 9075 array vector` — cél: hivatalos
   ISO-forrás a szabvány tartalmáról. Eredmény: csak fizetős ISO-katalógusoldalak és
   Wikipedia; a Wikipedia-összefoglalót használtuk fel (T5, csak orientációra).
8. `ANN-Benchmarks common interface vector database standard client API` — cél: közös
   vektor-kliens-felület létezésének ellenőrzése. Eredmény: nem került elő ilyen
   szabvány/közös API; csak gyártói termék-összehasonlító cikkek és az ann-benchmarks
   projekt (benchmark-protokoll, nem API-szabvány) — evidence-of-absence, `links.md`-ben
   leadként rögzítve.
9. `"SQL:2023" does not include vector type embedding standardization database` — cél:
   explicit megerősítés a vektor-típus hiányáról. Eredmény: a találatok inkább
   motorspecifikus (Oracle 23ai, Azure SQL, SQL Server) vektor-kiterjesztésekről
   szóltak — ez maga is releváns adat (l. `megallapitasok.md` 6. pont).
10. `OpenSearch hybrid search normalization processor min-max L2 RRF documentation`
    (2. kísérlet, a redirect célját célozva) — eredmény: továbbra sem sikerült valódi
    tartalmat kapni, `gaps.md`-ben jelölve.
11. `"leaky abstraction" full text search engine ORM ElasticSearch vs Solr practitioner
    experience` — cél: gyakorlói beszámoló egy keresés-absztrakció szivárgásáról.
    Eredmény: csak generikus "Elasticsearch vs Solr" összehasonlító cikkek, nem
    dedikált bukás-beszámoló (l. `megallapitasok.md` 4. pont, `gaps.md`).
12. `Elasticsearch "theory behind relevance scoring" _score meaning practical relevance
    not absolute` — cél: a klasszikus Definitive Guide fejezet és/vagy explicit
    összemérhetetlenségi nyilatkozat. Eredmény: megtaláltuk az elastic.co-n hosztolt
    fejezetet, de az a régi (BM25 előtti) TF/IDF modellt írja le, és nem tartalmazza az
    explicit összemérhetetlenségi mondatot a lekért kivonatban — nem használtuk fel
    forrásként (`gaps.md`).
13. `"Django Haystack" abandoned OR deprecated OR "stopped using" practitioner experience
    search abstraction` — cél: gyakorlói bukás-beszámoló Haystackről. Eredmény: csak
    Haystack saját changelog/issue-oldalai, nem dedikált "miért hagytuk abba" beszámoló.
14. `Spring Data Elasticsearch vs Spring Data JPA "leaky abstraction" repository query
    limitations` — cél: gyakorlói/dokumentált korlát Spring Data Elasticsearch körül.
    Eredmény: nem került elő releváns, közvetlenül idézhető forrás; Spring Data
    Elasticsearch/Hibernate Search-nél maradtunk a Hibernate Search saját doksijánál,
    ami explicit és erős forrásnak bizonyult (l. `megallapitasok.md` 3.2 pont).
15. `Typesense text_match_score formula BM25 documentation site:typesense.org` — cél: a
    helyes Typesense ranking-doksi URL megtalálása (a `/api/documents.html` és
    `/api/search.html` anchor-ök nem adtak találatot). Eredmény: a keresés kiadta a
    `typesense.org/docs/guide/ranking-and-relevance.html` URL-t, ami sikeres fetch lett.
16. `Qdrant "exact" search parameter documentation payload filtering HNSW` (2. kísérlet,
    a helyes doksi-URL megtalálására) — eredmény: `qdrant.tech/documentation/search/
    search/`, sikeres fetch, ez lett a fő forrás az exact-flaghez.

## Direkt WebFetch-navigációk (nem WebSearch-ből, ismert URL-ek)

sqlite.org/fts5.html · postgresql.org/docs/current/textsearch-{controls,intro}.html ·
dev.mysql.com/doc/refman/8.4/en/fulltext-search.html · elastic.co/guide/.../
query-filter-context.html · elastic.co/docs/.../consistent-scoring ·
elastic.co/guide/.../rrf.html · github.com/pgvector/pgvector ·
raw.githubusercontent.com/asg017/sqlite-vec/main/README.md ·
docs.weaviate.io/weaviate/config-refs/distances (redirectelt a weaviate.io/... URL-ről) ·
milvus.io/docs/index.md · github.com/facebookresearch/faiss/wiki/{Faiss-indexes,
MetricType-and-distances} · github.com/ankane/searchkick ·
django-haystack.readthedocs.io/en/latest/{,backend_support.html} ·
laravel.com/docs/12.x/scout · docs.hibernate.org/search/7.2/reference/en-US/html_single/
(redirectelve docs.jboss.org-ról) · qdrant.tech/documentation/search/search/ ·
qdrant.tech/articles/vector-search-filtering/ · en.wikipedia.org/wiki/SQL:2023 ·
meilisearch.com/docs/learn/relevancy/relevancy ·
typesense.org/docs/guide/ranking-and-relevance.html.

Sikertelen/üres-tartalmú fetch-kísérletek (nem használtuk forrásként, `gaps.md`):
qdrant.tech/documentation/concepts/search/ · qdrant.tech/documentation/concepts/
filtering/ · docs.opensearch.org/latest/vector-search/ai-search/hybrid-search/index/ ·
docs.opensearch.org/latest/vector-search/ai-search/hybrid-search/
normalization-processor/ · weaviate.io/developers/weaviate/config-refs/distances
(redirect-only válasz, a célt külön kértük le) · typesense.org/docs/latest/api/
{documents,search}.html#ranking-and-relevance (navigációs váz, nem a tartalom).


---

## SQ-04 — Hogyan tartható őszinte egy illesztő

# SQ-04 — Elvégzett keresések

Minden WebSearch-lekérdezés, amit ez a kör futtatott, időrendben. (A gépi napló
`01-search-log/queries.jsonl`-ben is szerepel; ez a fájl az olvasható, kommentált
változat.) Ezen kívül számos oldalt közvetlen WebFetch-hívással értünk el (hivatalos
doksi-URL-ek: martinfowler.com, testcontainers.com, github.com, docs.pact.io,
ecto.hexdocs.pm) — ezeket a domain és aloldal neve alapján, WebSearch nélkül, közvetlenül
nyitottuk meg, mert a témaismeretből (Fowler bliki-URL-konvenció, GitHub repo-elrendezés)
következtek.

## 1. kör — tájékozódás (1., 2., 4. kérdés)

1. `Martin Fowler ContractTest bliki` — cél: Fowler saját ContractTest-oldalának
   megtalálása. Eredmény: közvetlenül előkerült (martinfowler.com/bliki/ContractTest.html).
2. `Martin Fowler IntegrationContractTest` — cél: a felhasználó által kifejezetten kért,
   külön nevezett oldal megtalálása. Eredmény: **nem talált külön oldalt** — csak a
   ContractTest és IntegrationTest oldalak jöttek fel; ez később megerősítést nyert:
   az IntegrationContractTest URL a ContractTest oldalra vezet (2018-as összevonás,
   Fowler saját revíziós jegyzete).
3. `"abstract test case" pattern shared test suite multiple implementations testing` —
   cél: a felhasználó által kért "abstract test case" minta elsődleges forrása. Eredmény:
   megtalálta J. B. Rainsberger 2021-es visszatekintő bejegyzését, ami a legjobb, egyben
   elsődleges forrásnak bizonyult (a szerző saját írása, ráadásul újraközli az eredeti
   1999–2001-es c2-wiki vitát is).
4. `Testcontainers documentation what is testcontainers` — cél: hivatalos Testcontainers
   dokumentáció. Eredmény: közvetlenül előkerült a `testcontainers.com/getting-started/`
   hivatalos oldal.
5. `SQLAlchemy dialect test suite requirements.py` — cél: a SQLAlchemy dialektus-tesztelési
   architektúra hivatalos leírása. Eredmény: közvetlenül előkerült a
   `README.dialects.rst` a SQLAlchemy saját repójából.

## 2. kör — valós projektek (3. pont) és a hamis-biztonság kockázat (5. pont), YAGNI (6. pont)

6. `Ecto adapter test suite Ecto.Adapter.Migration shared tests Postgres MySQL` — cél:
   az Ecto (Elixir ORM) saját adapter-szerződés tesztkészletének feltárása. Eredmény:
   **részleges** — csak a felhasználói szintű "Testing with Ecto" (Sandbox-minta)
   dokumentáció került elő, az adapter-belső (`Ecto.Adapter`, `Ecto.Adapter.Migration`)
   viselkedési szerződés tesztkészlete nem — l. `gaps.md`.
7. `Rails ActiveRecord adapter shared test cases SharedTestCase database adapters` —
   cél: az ActiveRecord adapter-tesztelési mintája. Eredmény: megtalálta a
   `rails/activerecord/test/cases` könyvtárat és az `AbstractAdapter` forrásfájlokat;
   a könyvtár-nézet (tree) később robots.txt miatt nem volt megnyitható, de az egyes
   fájlok (blob/raw) igen.
8. `Fowler YAGNI speculative generality premature abstraction` — cél: Fowler saját YAGNI
   esszéje. Eredmény: közvetlenül előkerült a `martinfowler.com/bliki/Yagni.html`.
9. `tests passed in CI but broke in production different database engine behavior
   difference` — cél: konkrét esettanulmány a hamis-biztonság kockázatára. Eredmény:
   inkább általános "miért fail-el CI-ban" cikkeket hozott, nem DB-motor-specifikusat —
   ezért finomítottuk a következő kereséssel.
10. `SQLite vs PostgreSQL behavior difference bug tests passed production different` —
    cél: kifejezetten SQLite/PostgreSQL eltérésre szabott találat. Eredmény: **ez hozta
    a kör két legfontosabb forrását** — a Neon vendor-blogot és a dev.to postmortemet.

## 3. kör — hiányok zárása (2. kérdés pontos terminusa, 6. és 7. kérdés)

11. `rails activerecord test cases adapter_test.rb shared tests abstract adapter` — cél:
    megtalálni a konkrét, adapter-specifikus felülbírálásokat mutató fájlokat. Eredmény:
    megerősítette a `test_case.rb` és `abstract_adapter.rb` fájlok helyét; a `test_case.rb`
    nyers tartalmát sikeresen lekértük raw.githubusercontent.com-ról.
12. `contract tests do not verify performance concurrency transaction semantics` — cél:
    közvetlen forrás a 7. kérdésre. Eredmény: gyenge, általános marketing-cikkeket hozott,
    nem elsődleges forrást — ezért Pact-specifikus kereséssel folytattuk.
13. `Pact contract testing limitations what it does not test non-functional` — cél: a
    Pact hivatalos dokumentációjának a témára szabott oldala. Eredmény: **közvetlenül
    előkerült** a `docs.pact.io/consumer/contract_tests_not_functional_tests` — ez lett
    a 7. kérdés fő elsődleges forrása.
14. `empirical study cost of abstraction layer unused interface software engineering
    research` — cél: a 6. kérdésre kifejezetten mért (nem véleményalapú) anyag
    keresése. Eredmény: **kizárólag véleményblogokat/Medium-cikkeket** hozott (pl. "The
    Rising Cost of Abstraction"), egyiket sem vettük fel forrásként — ez explicit,
    dokumentált hiány (l. `gaps.md` és `megallapitasok.md` 6.1 pont).
15. `"subclass-to-test-interface" OR "subclass to test" pattern testing` — cél: a
    felhasználó által kifejezetten megjelölt terminus pontos forrásának azonosítása.
    Eredmény: megtalálta a c2-wiki `SubclassToTestAntiPattern` oldalt (tartalma nem volt
    elérhető, JS-védett) és Rainsberger saját, e vitára reagáló előadás-anyagát
    ("Why I Don't Consider Subclass to Test An Anti-Pattern") — ez megerősíti, hogy a
    minta **vitatott**, de a részletes érvelést nem sikerült feltárni.

## Megjegyzés a keresési stratégiáról

A kör tudatosan **nem** futtatott külön magyar nyelvű keresést — a téma (szoftvertesztelési
minták, Fowler/Rainsberger bliki, nyílt forráskódú projektek) kizárólag angol nyelvű,
nemzetközi szakmai közegben él, nincs magyar intézményi/jogi kötődése, így a skill
nyelvi-lefedettségi szabálya szerint ez nem számít hiánynak.
