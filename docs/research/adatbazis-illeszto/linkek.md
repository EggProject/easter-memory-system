# Linkek — minden meglátogatott forrás

Kampány: `adatbazis-illeszto` · 2026-09-09


---

## SQ-01 — Melyik illesztési minta, és hol a varrat

# SQ-01 — Minden meglátogatott / megtalált link, tier-besorolással

Tier-jelölés a feladatkiírás szerint: **T1** = elsődleges forrás (a minta szerzőjének
saját írása, hivatalos dokumentáció, peer-reviewed/arXiv); **T2** = megbízható másodlagos
(jó mérnöki blog, konferencia-előadás, könyvrészlet) VAGY gyártó saját termékéről szóló
állítás; **T3** = fórum, vélemény, marketing.

(Megjegyzés: az itt használt vault-infrastruktúra T0–T6 skálát is ismer — ahol
finomabb besorolás indokolt, azt zárójelben jelezzük, de a fő oszlop a feladat T1/T2/T3
rendszerét követi.)

## Ténylegesen archivált (letöltött, `02-sources/_agent/SQ-01/clean/`-ba mentett) források

| # | URL | Tier | Megjegyzés |
|---|---|---|---|
| 1 | https://alistair.cockburn.us/hexagonal-architecture | **T1** | Cockburn saját oldala, az eredeti 2005-ös cikk. Szó szerint ellenőrzött. |
| 2 | https://martinfowler.com/eaaCatalog/repository.html | **T1** | martinfowler.com hivatalos katalógus. Szerző: Edward Hieatt & Rob Mee (nem Fowler!). |
| 3 | https://martinfowler.com/eaaCatalog/dataMapper.html | **T1** | martinfowler.com, szerző: Martin Fowler. |
| 4 | https://martinfowler.com/eaaCatalog/gateway.html | **T1** | martinfowler.com, szerző: Martin Fowler. |
| 5 | https://martinfowler.com/eaaCatalog/tableDataGateway.html | **T1** | martinfowler.com. Első fetch AI-átfogalmazott volt, második (kereszt-ellenőrző) fetch adta a végleges, megbízható szöveget. |
| 6 | https://martinfowler.com/eaaCatalog/rowDataGateway.html | **T1** | martinfowler.com, szerző: Martin Fowler. |
| 7 | https://www.odbms.org/wp-content/uploads/2013/11/031.01-Neward-The-Vietnam-of-Computer-Science-June-2006.pdf | **T1** | Neward eredeti esszéje, PDF-újraközlés engedéllyel. Első fetch AI-összefoglalt, második szó szerintit adott. |
| 8 | http://mikehadlow.blogspot.com/2009/01/eric-evans-on-repositories.html | **T3** (belső skálán T3) | Másodlagos blog, állítólag szó szerint idézi Evans könyvét. |
| 9 | https://docs.nestjs.com/techniques/sql | **T1** | Hivatalos NestJS dokumentáció (gyártó saját dokumentációja a saját termékéről). |
| 10 | https://codeopinion.com/avoiding-the-repository-pattern-with-an-orm/ | **T3** | Derek Comartin (ismert .NET/CQRS gyakorlati blogger) véleménycikke. AI-átstrukturált fetch, csak parafrázisként kezelve. |
| 11 | https://www.oracle.com/java/technologies/dataaccessobject.html | **T1** | Oracle hivatalos oldal, Core J2EE Patterns DAO-fejezet alapján. |
| 12 | https://refactoring.guru/smells/speculative-generality | **T3** | Másodlagos katalógus-oldal (nem martinfowler.com), Fowler & Beck "Refactoring" könyvének "Speculative Generality" smelljét ismerteti újra. |
| 13 | https://codeopinion.com/do-you-really-need-that-abstraction-or-generic-code-yagni/ | **T3** | Derek Comartin, kifejezetten az "egy implementációra épített interfész" kérdésről. |
| 14 | https://martinfowler.com/bliki/Yagni.html | **T1** | Fowler saját bliki-bejegyzése. |
| 15 | https://www.thereformedprogrammer.net/is-the-repository-pattern-useful-with-entity-framework/ | **T2** | Jon P Smith (könyvszerző, "Entity Framework Core in Action"), kiegyensúlyozott, mindkét oldalt bemutató elemzés. |

## Megtalált, de nem (vagy csak linkként) archivált források

| URL | Tier (becsült) | Miért releváns | Státusz |
|---|---|---|---|
| http://codebetter.com/blogs/gregyoung/archive/2009/01/16/ddd-the-generic-repository.aspx (Wayback: https://web.archive.org/web/2015/http://codebetter.com/gregyoung/2009/01/16/ddd-the-generic-repository/) | T3 | Greg Young korai (2009), gyakran hivatkozott kritikája a generikus Repository ellen | **BLOKKOLVA** — a WebFetch `SITE_BLOCKED` hibát adott a Wayback Machine-lekérésre. Nem próbálkoztunk curl/más eszközzel megkerülni (a módszertan tiltja). |
| http://lostechies.com/jimmybogard/2012/10/08/favor-query-objects-over-repositories/ | T3 | Jimmy Bogard "Favor query objects over repositories" — a query-object irányzat egyik alapszövege | Nem fetchelve ebben a körben, csak linkként került elő a Reformed Programmer cikkből. |
| http://rob.conery.io/2014/03/04/repositories-on-top-unitofwork-are-not-a-good-idea/ | T3 | Rob Conery kritikája | Nem fetchelve, csak linkként. |
| http://cockneycoder.wordpress.com/2013/04/07/why-entity-framework-renders-the-repository-pattern-obsolete/ | T3 | Isaac Abraham kritikája | Nem fetchelve, csak linkként. |
| http://tech.pro/blog/1191/say-no-to-the-repository-pattern-in-your-dal | T3 | "Say No to the Repository Pattern in your DAL" | Nem fetchelve, csak linkként. |
| https://blog.sapiensworks.com/post/2012/03/05/The-Generic-Repository-Is-An-Anti-Pattern.aspx | T3 | Explicit "generikus repository anti-minta" vita | Csak keresési találatként került elő, nem fetchelve. |
| https://www.domainlanguage.com/ddd/reference/ | T1 (a forrás maga hivatalos) | Eric Evans hivatalos DDD Reference oldala | Fetchelve, de a válasz AI-összefoglaló volt, **nem archiváltuk forrásként** a szigorú szabály szerint ("ha egy fetch AI-összefoglalót ad vissza, ne használd forrásként"). Ld. `gaps.md`. |
| https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf | T1 | Evans hivatalos DDD Reference PDF-je | Fetchelve, de a WebFetch-eszköz megtagadta a szó szerinti idézést szerzői jogi okra hivatkozva. Nem archiváltuk forrásként a Repository-szakasz idézetére nézve. Ld. `gaps.md`. |
| https://fabiofumarola.github.io/nosql/readingMaterial/Evans03.pdf | T4 (harmadik féltől hosztolt könyv-PDF, kérdéses jogszerűség) | Evans teljes könyve | Fetchelve, ugyanúgy megtagadva. Nem archiváltuk. |
| https://martinfowler.com/articles/gateway-pattern.html | T1 | Fowler 2021-es, bővített Gateway-cikke, amit a PoEAA Gateway-oldal saját maga ajánl jobbnak | Nem fetchelve ebben a körben (alacsony prioritású hiány, mivel az alapdefiníció már megvan). |
| https://en.wikipedia.org/wiki/Hexagonal_architecture_(software) | T5 | Tájékozódási találat | Nem fetchelve (aggregátor, csak keresési listában szerepelt). |
| https://en.wikipedia.org/wiki/Table_data_gateway , .../Row_data_gateway , .../Data_mapper_pattern | T5 | Tájékozódási találatok | Nem fetchelve — a hivatalos martinfowler.com oldalakat használtuk helyettük. |
| https://grokipedia.com/page/table_data_gateway | T0/T5 (AI-generált aggregátor, bizonytalan eredetiség) | Keresési találat | Nem fetchelve — tudatosan kerülve, AI-generált aggregátor-gyanús. |
| https://www.informit.com/articles/article.aspx?p=1398618 | T2 (InformIT, Pearson-kiadó, könyvrészlet-újraközlés) | "Framework Design Guidelines" — Table/Row Data Gateway, Data Mapper könyvrészlet | Nem fetchelve ebben a körben. |
| https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-design | T2 (gyártó saját arch. útmutatója) | Microsoft saját Repository-ajánlása .NET-hez | Nem fetchelve — más ökoszisztéma (.NET), a feladat TS/Node-ra kérdezett rá elsősorban. |
| https://blog.elmah.io/the-repository-pattern-is-simple-yet-misunderstood/ | T3 | Gyakorlói blog | Nem fetchelve, csak keresési találat. |
| https://www.infoq.com/interviews/eric-evans-ddd-interview | T2 (InfoQ, szerkesztett interjú, Evans saját szavai) | Potenciális Evans-elsőkéz-idézet forrás | Nem fetchelve ebben a körben — érdemes lenne egy következő körben, mert szerkesztett interjúban Evans saját szavai idézhetők lennének szerzői jogi aggály nélkül. |
| https://www.infoworld.com/article/2248622/design-patterns-that-i-often-avoid-repository-pattern.html | T2/T3 (InfoWorld, szerkesztett) | "Design patterns that I often avoid: Repository pattern" | Nem fetchelve, csak keresési találat. |

## Nem-releváns / kerülendő találatok (SEO-farm / véletlen egyezés gyanú)

| URL | Miért kerültük |
|---|---|
| https://github.com/dumpsterfire , https://en.wikipedia.org/wiki/Dumpster_fire , https://dictionary.cambridge.org/... | A `"Repository is a Dumpster Fire"` pontos cím-keresés szó szerinti egyezés hiányában irreleváns, szótári/GitHub-szervezet-találatokat hozott. Nem forrás. |
| https://grokipedia.com/page/table_data_gateway | AI-generált aggregátor-gyanús (a "Grokipedia" márkanév és a jellegzetes, forrás nélküli összefoglaló-stílus alapján) — tudatosan nem használtuk forrásként. |


---

## SQ-02 — Párhuzamosság és tranzakciók motorok között

# SQ-02 — Minden meglátogatott / megtalált link, tier-besorolással

Tier-jelölés a feladatkiírás szerint: **T1** = hivatalos dokumentáció, specifikáció,
forráskód, peer-reviewed/arXiv; **T2** = megbízható másodlagos VAGY gyártó saját
termékéről szóló állítás (pl. a gyártó saját issue trackere); **T3** = fórum, vélemény,
marketing.

(Megjegyzés, ahogy SQ-01-ben is: az itt használt vault-infrastruktúra T0–T6 skálát is
ismer — ahol finomabb besorolás indokolt, azt zárójelben jelezzük, de a fő oszlop a
feladat T1/T2/T3 rendszerét követi.)

## Ténylegesen archivált (letöltött, `02-sources/_agent/SQ-02/clean/`-ba mentett) források

| # | URL | Tier | Megjegyzés |
|---|---|---|---|
| 1 | https://www.sqlite.org/lang_transaction.html | **T1** | Hivatalos SQLite doksi: BEGIN DEFERRED/IMMEDIATE/EXCLUSIVE, SQLITE_BUSY. Utolsó frissítés 2026-02-18. |
| 2 | https://www.sqlite.org/wal.html | **T1** | Hivatalos WAL-doksi: "only one writer at a time", SQLITE_BUSY WAL módban is. |
| 3 | https://www.sqlite.org/lockingv3.html | **T1** | Hivatalos zárolási állapotgép: UNLOCKED/SHARED/RESERVED/PENDING/EXCLUSIVE, writer starvation. |
| 4 | https://www.sqlite.org/isolation.html | **T1** | Hivatalos izoláció-doksi: minden tranzakció SERIALIZABLE, SQLITE_BUSY_SNAPSHOT, BEGIN IMMEDIATE javaslat. A legfontosabb egyetlen SQLite-forrás ebben a körben. |
| 5 | https://sqlite.org/whentouse.html | **T1** | Hivatalos "mikor NE használj SQLite-ot" doksi. Fetch részben átstrukturált volt. |
| 6 | https://martinfowler.com/eaaCatalog/unitOfWork.html | **T1** | Fowler saját katalógusa. Fetch AI-átstrukturált volt, csak az idézőjeles mondatok kezelendők idézetként. |
| 7 | https://www.cs.cmu.edu/~15721-f24/papers/Critique_of_ANSI_Isolation_Levels.pdf | **T1** | Berenson et al. 1995 alapmű, CMU-hosztolt PDF-másolat (nem az eredeti ACM/MSR oldal, ami paywalled). Fetch részben átstrukturált; egyetlen forrás, nincs kereszt-ellenőrzés. |
| 8 | https://www.prisma.io/docs/orm/prisma-client/queries/transactions | **T1** | Hivatalos Prisma doksi: izolációs szint táblázat motoronként, optimista concurrency minta. A legrészletesebb ORM-forrás ebben a körben. |
| 9 | https://github.com/prisma/prisma/issues/25587 | **T2** | Prisma saját issue trackere saját termékéről: SQLite-on mindig BEGIN IMMEDIATE. Kulcsbizonyíték a 6. ponthoz. |
| 10 | https://knexjs.org/guide/transactions.html | **T1** | Hivatalos Knex doksi: izolációs szint "not supported by oracle and sqlite". |
| 11 | https://docs.djangoproject.com/en/6.1/ref/databases/ | **T1** | Hivatalos Django doksi: "database is locked", transaction_mode OPTIONS, select_for_update nincs hatása SQLite-on, explicit "válts motort" ajánlás. |
| 12 | https://code.djangoproject.com/ticket/29280 | **T2** | Django saját ticket-trackere: többéves, dokumentált esettanulmány az "egy író" korlát Django ORM-en való átszivárgásáról. A legfontosabb egyetlen forrás a 6. ponthoz. |
| 13 | https://orm.drizzle.team/docs/transactions | **T1** | Hivatalos Drizzle doksi. Csak Postgres-specifikus izolációs szint interfész volt látható a fetchben — gap. |
| 14 | https://kysely-org.github.io/kysely-apidoc/variables/TRANSACTION_ISOLATION_LEVELS.html | **T1** | Hivatalos Kysely API-doksi: 5 izolációs szint string konstans. |
| 15 | https://github.com/kysely-org/kysely/issues/877 | **T2** | Kysely saját issue trackere: Postgres-specifikus tranzakciós funkció (READ ONLY/DEFERRABLE) kérése motorfüggetlen query builderben; maintainer-válasz nem volt elérhető a fetchben. |
| 16 | https://www.doctrine-project.org/projects/doctrine-dbal/en/4.4/reference/transactions.html | **T1** | Hivatalos Doctrine DBAL doksi: "guaranteed to be at least READ_COMMITTED" — csak alsó korlátot ígér. |
| 17 | https://api.rubyonrails.org/classes/ActiveRecord/Locking/Optimistic.html | **T1** | Hivatalos Rails API-doksi: lock_version, StaleObjectError — motor-független optimista zárolás. |
| 18 | https://docs.hibernate.org/orm/5.2/userguide/html_single/chapters/locking/Locking.html | **T1** | Hivatalos Hibernate 5.2 doksi: csendes degradáció, ha egy lock mode nincs támogatva — kulcsidézet az 5. ponthoz. |
| 19 | https://docs.sqlalchemy.org/en/20/core/connections.html | **T1** | Hivatalos SQLAlchemy doksi: DBAPI-nkénti izolációs szint támogatás, motoronkénti külön doksi-oldalak. Fetch részben átstrukturált. |
| 20 | https://docs.sqlalchemy.org/en/20/dialects/sqlite.html | **T1** | Hivatalos SQLAlchemy SQLite-dialektus doksi: a Python sqlite3 driver legacy módja megtörheti a SERIALIZABLE garanciát. Fetch részben átstrukturált. |
| 21 | https://tenthousandmeters.com/blog/sqlite-concurrent-writes-and-database-is-locked-errors/ | **T3** | Gyakorlói blog, informális benchmark-számokkal. Csak kiegészítő, nem normatív forrásként használva. |
| 22 | https://ecto-sqlite3.hexdocs.pm/0.5.2/Ecto.Adapters.SQLite3.html | **T1** | Hivatalos Ecto SQLite3 adapter doksi: async sandbox tesztelés dokumentáltan NEM támogatott az egy-író korlát miatt — második, Django-tól független ökoszisztémából érkező megerősítő esettanulmány. |

**Összesen archiválva: 22 forrás** (16 T1, 4 T2, 1 T3, plusz a Hibernate `Portability.html`
oldal, amit fetcheltünk, de nem tartalmazott releváns anyagot — lásd alább, "Fetchelt, de
nem archivált" szakasz).

## Fetchelt, de NEM archivált (mert nem tartalmazott releváns/felhasználható anyagot)

| URL | Tier | Miért nem került archiválásra |
|---|---|---|
| https://docs.hibernate.org/orm/5.2/userguide/html_single/chapters/portability/Portability.html | T1 | A fetch szerint ez az oldal NEM tartalmaz izolációs szint / zárolási / absztrakciós-korlát tárgyú szakaszt — a "Database Portability Considerations" oldal más témákról szól (dialektus-feloldás, azonosító-generálás). Helyette a `Locking.html` oldal (18. sor fent) adta a releváns Hibernate-tartalmat. |

## Megtalált, de meg NEM nyitott linkek (leadek, `05-links.jsonl`-be és `log_link`-kel rögzítve)

| URL | Miért releváns | Miért nem lett megnyitva |
|---|---|---|
| https://jakarta.ee/specifications/persistence/3.0/jakarta-persistence-spec-3.0.html | A JPA hivatalos specifikáció-szövege saját szavaival mondhatná ki, mit NEM szabványosít az izolációs szintekről | Idő/eszközkeret-korlát ebben a körben — `gaps.md` |
| https://vladmihalcea.com/a-beginners-guide-to-transaction-isolation-levels-in-enterprise-java/ | Ismert, megbízható JPA/Hibernate-szakértő gyakorlói cikke, kereszt-ellenőrzésre alkalmas lenne | Idő/eszközkeret-korlát |
| https://render.com/articles/how-to-migrate-from-sqlite-to-postgresql | Gyakorlati SQLite→Postgres migrációs útmutató (6. pont) | Idő/eszközkeret-korlát — a Django ticket #29280 elegendő elsődleges bizonyítékot adott |
| https://code.djangoproject.com/ticket/29062 | Rokon Django SQLite locking ticket (LiveServerTestCase, in-memory db) | Idő/eszközkeret-korlát |
| https://code.djangoproject.com/ticket/9409 | Korai (2008) Django SQLite multiprocessing "database is locked" ticket | Idő/eszközkeret-korlát |
| https://sqlite.org/forum/info/722e181400b0ae09ea64446c614fe29ee3e313139fbc1c96e054913197a4a95b | SQLite hivatalos fórum: BEGIN IMMEDIATE + busy_timeout együttes viselkedése | Fórumbejegyzés — a feladatkiírás szerint hivatalos domainen sem T1, alacsony prioritás |

## Blokkolt domainek

Ebben a körben nem volt blokkolt domain (`01-search-log/blocked.jsonl`-ben SQ-02-höz nincs
bejegyzés).


---

## SQ-03 — Szöveges és vektoros keresés hordozható felület mögött

# SQ-03 — Források és tier-besorolás

Minden forrás archiválva a `02-sources/_agent/SQ-03/clean/` alatt (WebFetch-lekérésből
mentve `capture_source.py`-jal). A `source_id` a manifestben és az evidence table-ben
használt azonosító.

## Szöveges keresés — motorok hivatalos dokumentációi

| # | Cím | URL | Tier | source_id |
|---|---|---|---|---|
| 1 | SQLite FTS5 Extension | https://sqlite.org/fts5.html | T1 | src_2026-09-09_sqlite-org_sqlite-fts5-extension |
| 2 | PostgreSQL 12.3. Controlling Text Search | https://www.postgresql.org/docs/current/textsearch-controls.html | T1 | src_2026-09-09_postgresql-org_postgresql-12-3-controlling-text-search |
| 3 | PostgreSQL 12.1. Introduction (Full Text Search) | https://www.postgresql.org/docs/current/textsearch-intro.html | T1 | src_2026-09-09_postgresql-org_postgresql-12-1-introduction-full-text-search |
| 4 | MySQL 8.4 Full-Text Search Functions | https://dev.mysql.com/doc/refman/8.4/en/fulltext-search.html | T1 | src_2026-09-09_dev-mysql-com_mysql-8-4-full-text-search-functions |
| 5 | Elasticsearch Query DSL: Query and filter context | https://www.elastic.co/guide/en/elasticsearch/reference/current/query-filter-context.html | T1 | src_2026-09-09_elastic-co_elasticsearch-query-dsl-query-and-filter-context |
| 6 | Elasticsearch: Getting consistent scoring | https://www.elastic.co/docs/solutions/search/full-text/search-relevance/consistent-scoring | T1 | src_2026-09-09_elastic-co_elasticsearch-getting-consistent-scoring |
| 7 | Meilisearch: Relevancy | https://www.meilisearch.com/docs/learn/relevancy/relevancy | T1 | src_2026-09-09_meilisearch-com_meilisearch-relevancy |
| 8 | Typesense: Ranking and Relevance | https://typesense.org/docs/guide/ranking-and-relevance.html | T1 | src_2026-09-09_typesense-org_typesense-ranking-and-relevance |

## Hibrid keresés / RRF

| # | Cím | URL | Tier | source_id |
|---|---|---|---|---|
| 9 | Elasticsearch: Reciprocal rank fusion (RRF) | https://www.elastic.co/guide/en/elasticsearch/reference/current/rrf.html | T1 | src_2026-09-09_elastic-co_elasticsearch-reciprocal-rank-fusion-rrf |
| 10 | Reciprocal Rank Fusion outperforms Condorcet... (Cormack, Clarke, Buettcher, SIGIR 2009) | https://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf | T1 | src_2026-09-09_cormack-uwaterloo-ca_reciprocal-rank-fusion-outperforms-condorcet-and-individual |

## Vektoros keresés — motorok hivatalos dokumentációi

| # | Cím | URL | Tier | source_id |
|---|---|---|---|---|
| 11 | pgvector README | https://github.com/pgvector/pgvector | T1 | src_2026-09-09_github-com_pgvector-readme |
| 12 | sqlite-vec README (raw) | https://raw.githubusercontent.com/asg017/sqlite-vec/main/README.md | T1 | src_2026-09-09_raw-githubusercontent-com_sqlite-vec-readme |
| 13 | Qdrant Documentation: Search | https://qdrant.tech/documentation/search/search/ | T1 | src_2026-09-09_qdrant-tech_qdrant-documentation-search |
| 14 | A Complete Guide to Filtering in Vector Search (Qdrant) | https://qdrant.tech/articles/vector-search-filtering/ | T2 (vendor blog/article, nem a core docs) | src_2026-09-09_qdrant-tech_a-complete-guide-to-filtering-in-vector-search-qdrant |
| 15 | Weaviate: Distance metrics | https://docs.weaviate.io/weaviate/config-refs/distances | T1 | src_2026-09-09_docs-weaviate-io_weaviate-distance-metrics |
| 16 | Milvus: In-memory Index | https://milvus.io/docs/index.md | T1 | src_2026-09-09_milvus-io_milvus-in-memory-index |
| 17 | Faiss wiki: Faiss indexes | https://github.com/facebookresearch/faiss/wiki/Faiss-indexes | T1 | src_2026-09-09_github-com_faiss-wiki-faiss-indexes |
| 18 | Faiss wiki: MetricType and distances | https://github.com/facebookresearch/faiss/wiki/MetricType-and-distances | T1 | src_2026-09-09_github-com_faiss-wiki-metrictype-and-distances |

## Keresés-absztrakciós rétegek

| # | Cím | URL | Tier | source_id |
|---|---|---|---|---|
| 19 | Searchkick README | https://github.com/ankane/searchkick | T1 | src_2026-09-09_github-com_searchkick-readme |
| 20 | Django Haystack documentation (index) | https://django-haystack.readthedocs.io/en/latest/ | T1 | src_2026-09-09_django-haystack-readthedocs-io_django-haystack-documentation-index |
| 21 | Django Haystack: Backend Support | https://django-haystack.readthedocs.io/en/latest/backend_support.html | T1 | src_2026-09-09_django-haystack-readthedocs-io_django-haystack-backend-support |
| 22 | Laravel Scout documentation | https://laravel.com/docs/12.x/scout | T1 | src_2026-09-09_laravel-com_laravel-scout-documentation |
| 23 | Hibernate Search 7.2 Reference: Architecture | https://docs.hibernate.org/search/7.2/reference/en-US/html_single/ | T1 | src_2026-09-09_docs-hibernate-org_hibernate-search-7-2-reference-architecture |

## Szabványosítás

| # | Cím | URL | Tier | source_id |
|---|---|---|---|---|
| 24 | SQL:2023 (Wikipedia) | https://en.wikipedia.org/wiki/SQL:2023 | T5 (aggregátor; csak orientációra/hiány-jelzésre használva, nem önálló alátámasztásra) | src_2026-09-09_en-wikipedia-org_sql-2023-wikipedia |

## Rögzített, de meg nem nyitott linkek (leadek a következő körhöz)

Ezek `log_link.py`-jal rögzítve `05-links.jsonl`-ben, `status: not_opened`:

- https://docs.opensearch.org/latest/search-plugins/search-pipelines/normalization-processor/
  — OpenSearch normalizáló processzor (min-max/L2 pontszám-normalizálás hibrid
  kereséshez); a WebFetch ismételten 404/redirect-vázat adott vissza.
- https://github.com/erikbern/ann-benchmarks — a vektor-keresési könyvtárak közötti
  de facto közös benchmark-protokoll (nem API-szabvány).
- https://db-engines.com/en/system/Elasticsearch%3BManticore+Search%3BOracle%3BSolr —
  DB-Engines összehasonlítás, Manticore Search-csel (nem vizsgált BM25-alapú motor).
- https://www.postgresql.org/docs/current/textsearch-indexes.html — PostgreSQL
  GIN/GiST full text index dokumentáció (index-struktúra, másodlagos a rangsoroláshoz
  képest).
- https://docs.jboss.org/hibernate/search/7.2/reference/en-US/html_single/ — a
  docs.hibernate.org-ra redirectelő régi tükör; a cél oldal (#23) archiválva.
- https://typesense.org/docs/30.2/api/vector-search.html — Typesense vektoros/hibrid
  keresés dokumentációja (5/7. pont továbbfejlesztéséhez releváns follow-up).

## Megnyitott, de forrásként NEM felhasznált oldalak (AI-összefoglalót/üres vázat adtak)

Ld. részletesen `gaps.md`. Röviden: OpenSearch hybrid-search index oldal (2x), OpenSearch
normalization-processor oldal, Qdrant `concepts/search/` és `concepts/filtering/`
oldalak, Weaviate `config-refs/distances` első (nem-redirectelt) URL-je, Typesense
`text_match_type` régi URL-ek — ezek helyett vagy a redirect célját, vagy más URL-t
kerestünk meg sikeresen.


---

## SQ-04 — Hogyan tartható őszinte egy illesztő

# SQ-04 — Források és tier-besorolás

Minden forrás archiválva a `02-sources/_agent/SQ-04/clean/` alatt (WebFetch-lekérésből
mentve `capture_source.py`-jal). A `source_id` a manifestben és az evidence table-ben
(`02-sources/_agent/SQ-04/claims.jsonl`) használt azonosító.

## Elsődleges forrás a minta szerzőjétől (Fowler, Rainsberger)

| # | Cím | URL | Tier | source_id |
|---|---|---|---|---|
| 1 | bliki: Contract Test | https://martinfowler.com/bliki/ContractTest.html | T1 | src_2026-09-09_martinfowler-com_bliki-contract-test |
| 2 | bliki: Yagni | https://martinfowler.com/bliki/Yagni.html | T1 | src_2026-09-09_martinfowler-com_bliki-yagni |
| 3 | Abstract Test Cases, 20 Years Later (J. B. Rainsberger, blog.thecodewhisperer.com) — újraközli az eredeti 1999–2001-es c2-wiki vitát is (Channing Walton, James Abley) | https://blog.thecodewhisperer.com/permalink/abstract-test-cases-20-years-later | T1 | src_2026-09-09_blog-thecodewhisperer-com_abstract-test-cases-20-years-later |

Megjegyzés: `https://martinfowler.com/bliki/IntegrationContractTest.html` ugyanarra a
`ContractTest.html` tartalomra mutat/redirectel — Fowler saját revíziós jegyzete szerint
2018-ban összevonta a két bliki-bejegyzést (l. `megallapitasok.md` 1.1). Nincs önálló
`IntegrationContractTest` tartalom többé.

## Hivatalos eszköz-/keretrendszer-dokumentáció és forráskód

| # | Cím | URL | Tier | source_id |
|---|---|---|---|---|
| 4 | Getting Started — Testcontainers | https://testcontainers.com/getting-started/ | T1 | src_2026-09-09_testcontainers-com_getting-started-testcontainers |
| 5 | README.dialects.rst — SQLAlchemy Dialect Development Guide | https://github.com/sqlalchemy/sqlalchemy/blob/main/README.dialects.rst | T1 | src_2026-09-09_github-com_readme-dialects-rst-sqlalchemy-dialect-development-guide |
| 6 | Testing with Ecto | https://ecto.hexdocs.pm/testing-with-ecto.html | T1 | src_2026-09-09_ecto-hexdocs-pm_testing-with-ecto |
| 7 | Contract Tests vs Functional Tests — Pact Docs | https://docs.pact.io/consumer/contract_tests_not_functional_tests | T1 | src_2026-09-09_docs-pact-io_contract-tests-vs-functional-tests |
| 8 | rails/activerecord/test/cases/test_case.rb (nyers forráskód, main branch) | https://raw.githubusercontent.com/rails/rails/main/activerecord/test/cases/test_case.rb | T1 | src_2026-09-09_raw-githubusercontent-com_rails-activerecord-test-cases-test-case-rb-raw |

## Gyártói blog és gyakorlói beszámoló (a hamis-biztonság kockázatához, 5. kérdés)

| # | Cím | URL | Tier | source_id | Megjegyzés |
|---|---|---|---|---|---|
| 9 | The Dangers of Testing in SQLite as a Postgres User (Neon) | https://neon.com/blog/testing-sqlite-postgres | T4 | src_2026-09-09_neon-com_the-dangers-of-testing-in-sqlite-as-a-postgres-user | Postgres-as-a-service gyártó saját blogja; a technikai ténymegállapítások ellenőrizhetők, a végkövetkeztetés (saját termék ajánlása) marketing |
| 10 | SQLite doesn't enforce foreign keys by default, and it cost us three bugs | https://dev.to/enderyentar/sqlite-doesnt-enforce-foreign-keys-by-default-and-it-cost-us-three-bugs-1ii9 | T6 | src_2026-09-09_dev-to_sqlite-doesn-t-enforce-foreign-keys-by-default-and-it-cost-u | Egyetlen szerző, nem ellenőrizhető azonosítás, de rendkívül konkrét, technikailag koherens, önmagában hiteles postmortem |

## Nem forrásként felhasznált, de dokumentált találatok (l. `gaps.md`)

| URL | Miért nem lett forrás |
|---|---|
| https://github.com/rails/rails/tree/main/activerecord/test/cases | robots.txt blokkolta (könyvtárlistázó GitHub `tree` nézet) |
| https://wiki.c2.com/?SubclassToTestAntiPattern= | JavaScript-alapú oldal, a WebFetch üres vázat adott vissza ("JavaScript required to view this site") |
| https://online-training.jbrains.ca/courses/36224/lectures/2957384 ("Why I Don't Consider Subclass to Test An Anti-Pattern") | Fizetős kurzus-tartalom, a kör nem nyitotta meg — csak a létezését dokumentáljuk |

## Kapcsolódó, de nem megnyitott (csak keresési találatként látott) linkek — lead más
körnek/kérdésnek

- https://beware-the-integrated-tests-scam.jbrains.ca — Rainsberger fő esszéje az
  "integrated tests scam"-ről, amire az abstract-test-cases cikk többször hivatkozik;
  releváns lehet SQ-01/SQ-02-höz is (tesztelési stratégia általában).
- https://wiki.c2.com/?AbstractTestCases — az eredeti c2-wiki oldal, amit Rainsberger
  cikke nagyrészt szó szerint újraközöl; nem lett külön megnyitva, mert a tartalma már
  megjelenik elsődleges forrásból (Rainsberger saját újraközlése).
- https://cormack.uwaterloo.ca (SQ-03-ban már szerepel, nem SQ-04 tárgya).
