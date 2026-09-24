# Kivonat — ParadeDB

Kutatási egységenként, szó szerinti idézetekkel. SQ01–SQ07: első kör; ELL01–ELL05: ellenőrző kör az Exa keresővel; ELL06–ELL07: második ellenőrző kör a leírások átírása előtt (mentés és migráció, adatlap-ellenőrzőösszeg), szintén Exa. A linkek a `linkek.md`-ben.



---

# SQ01 — Mi a ParadeDB pontosan, és mennyire érett?

> **Módszertani megjegyzés (kötelező bejegyzés a `_kozos.txt` szerint):** A feladatot a `anthropic-skills:deep-web-research` skill elindította, de a skill többágenses (Sonnet-kereső-subagentek + Opus-szintézis) fan-out architektúrája ebben a futtatási környezetben nem érhető el — nincs önálló „Agent" eszköz subagent-indításra, és nincs interaktív felhasználó, aki a scope-kérdésekre válaszolna (a skill Phase 0 `AskUserQuestion` lépése). Ezért a skill saját instrukciója szerinti **degradált módban** dolgoztam: egyetlen szálon, szekvenciálisan, magam végeztem a keresést (`WebSearch`/`WebFetch`/`curl`), a forrásmegbízhatósági elveket (elsődleges forrás előny, idézetkényszer, kétforrásos megerősítés, ellentmondások kiírása) viszont követtem. A kimenet formátuma a `_kozos.txt`-ben előírt SQ-sablont követi, nem a skill saját `SZINTEZIS.md` vault-formátumát, mert a feladat kifejezetten egyetlen `sq01.md` fájlt kért.

## Rövid válasz

A „paradb" néven két, a ParadeDB-től teljesen független termék is létezik (egy paranormális jelentéseket gyűjtő SourceForge-adatbázis és egy gombagenomikai adatbázis), így a felhasználó feltehetően a **ParadeDB**-re gondolt. A ParadeDB nem önálló adatbázis-disztribúció, hanem — saját megfogalmazása szerint — „vanilla Postgres with an extension installed, not a Postgres fork or sidecar process": a fő komponens a Rust nyelven (pgrx + Tantivy + Apache DataFusion felett) írt **pg_search** kiterjesztés, amely BM25 szöveges keresést, hibrid keresést, szűrést/aggregációt és — 2026 nyara óta, a `pgvector`-ra kötelezően ráépülve — vektoros keresést ad Postgreshez. A korábbi `pg_lakehouse` nevű analitikai kiterjesztést átnevezték `pg_analytics`-ra, majd 2025. március 19-én archiválták, funkcióit a `pg_search`-be olvasztották. A projekt gyors ütemben, még 0.x verziószámon fejlődik (legfrissebb stabil kiadás: **v0.25.9**, 2026. szeptember 11.), AGPL-3.0 licenc alatt, mellette fizetős „ParadeDB Enterprise" réteggel (HA, read replica, support). A céget (ParadeDB, Inc., alapítók: Philippe Noël és Ming Ying) 2023-ban alapították, 2025 júliusában 12 millió dolláros Series A-t zárt (Craft Ventures vezetésével, összesen 14 millió dollár bevont tőke). Futtatható Dockerben, Debian/Ubuntu/RHEL csomagként és natív macOS binárisként, de nincs Homebrew formula; a „ParadeDB Cloud" felhős szolgáltatás 2026 szeptemberében még csak várólistás „Coming soon" státuszban van. A menedzselt Postgres-szolgáltatók képe vegyes és **időben instabil**: a Neon 2025 márciusában hivatalos partnerségben vezette be a `pg_search`-öt, majd 2026 márciusában bejelentette a kivezetését, és 2026. szeptember 21-től (azaz gyakorlatilag a kutatás idejére) teljesen megszünteti; a Supabase csak „partner katalógusban" szerepelteti, saját hivatalos deploy-dokumentációja pedig az AWS RDS-t, Supabase-t és Neon-t név szerint egyáltalán nem említi támogatott célként.

## 1. Egyértelműsítés — létezik-e más „paradb" termék?

Igen, létezik legalább két, a ParadeDB-től teljesen független termék, amely „ParaDB" néven fut:

1. **ParaDB — Paranormal Reporting Database** (SourceForge-projekt): „ParaDB -- Paranormal Reporting Database" — ez egy paranormális jelenségek bejelentésére szolgáló, a Postgres-témától teljesen független alkalmazás. Forrás: [paradb.sourceforge.net](https://paradb.sourceforge.net/).
2. **ParaDB — genomikai adatbázis**: „ParaDB: A manually curated database containing genomic annotation for the human pathogenic fungi *Paracoccidioides* spp." — egy tudományos, gomba-genomikai annotációs adatbázis, publikálva a *PLOS Neglected Tropical Diseases* folyóiratban. Forrás: [journals.plos.org/plosntds/article?id=10.1371/journal.pntd.0007576](https://journals.plos.org/plosntds/article?id=10.1371%2Fjournal.pntd.0007576), másodforrás: [pmc.ncbi.nlm.nih.gov/articles/PMC6658007](https://pmc.ncbi.nlm.nih.gov/articles/PMC6658007/).

Egyik sincs kapcsolatban a Postgres-alapú ParadeDB-vel. A kutatás további része feltételezi, hogy a felhasználó a **ParadeDB**-re (paradedb.com, github.com/paradedb) gondolt.

## 2. Mi a ParadeDB, összetevőnként

### 2.1 Bővítmény, nem disztribúció

A hivatalos dokumentáció explicit állítása: „vanilla Postgres with an extension installed, not a Postgres fork or sidecar process." Forrás: [paradedb.com/docs/start/introduction](https://www.paradedb.com/docs/start/introduction).

A GitHub repó leírása is ezt erősíti meg: „One Postgres for your application data, full-text search, vector retrieval, and aggregations. Home of the pg_search extension." Forrás: [github.com/paradedb/paradedb](https://github.com/paradedb/paradedb).

### 2.2 pg_search — a fő komponens (BM25, Tantivy)

A `pg_search/README.md` (a fejlesztői dokumentum a fő monorepóban) szerint: „pg_search is supported on official PostgreSQL Global Development Group Postgres versions, starting at PostgreSQL 15." Forrás: [raw.githubusercontent.com/paradedb/paradedb/main/pg_search/README.md](https://raw.githubusercontent.com/paradedb/paradedb/main/pg_search/README.md).

Az architektúráról a bevezető oldal: „One ParadeDB Index combines an inverted index for text, a clustered index for vectors, and columnar storage for filters and aggregates." — azaz egy „ParadeDB Index" szöveges inverz indexet, vektoros klaszterezett indexet és oszlopalapú tárolást egyesít. Az alap Rust-könyvtárak: **pgrx** (Postgres–Rust híd), **Tantivy** (keresőmotor), **Apache DataFusion** (OLAP-feldolgozás). Forrás: [paradedb.com/docs/start/introduction](https://www.paradedb.com/docs/start/introduction).

### 2.3 Vektoros keresés — a `pgvector`-ra épül, nem saját implementáció

Ez a legfontosabb, közvetlen forrásból megerősített tény: a `pg_search/README.md` kimondja: „`pg_search` uses `pgvector`'s types to index vector fields alongside text and other fields in ParadeDB indexes, so `pgvector` must be available before `pg_search` can be created." Ugyanitt telepítési példa: „`CREATE EXTENSION pg_search CASCADE` (`CASCADE` also creates `pgvector`, which `pg_search` requires)." Forrás: [raw.githubusercontent.com/paradedb/paradedb/main/pg_search/README.md](https://raw.githubusercontent.com/paradedb/paradedb/main/pg_search/README.md).

Ezt egy **második, független forrás is megerősíti**: a v0.25.0 kiadási jegyzék „Breaking change" bejegyzése: „As of `0.25.0`, [`pgvector`](https://github.com/pgvector/pgvector) is a required extension of `pg_search`." Forrás: [paradedb.com/docs/project/changelog/0.25.0](https://www.paradedb.com/docs/project/changelog/0.25.0).

Tehát: a vektor-**típus** és -tárolás a `pgvector`-ra épül (kötelező függőség 0.25.0 óta), de a tényleges vektoros **index** ("clustered index for vectors") a ParadeDB saját indexstruktúrájának része, nem a `pgvector` saját HNSW/IVFFlat indexét használja újra közvetlenül — ez utóbbi pontos technikai részletére (index-algoritmus szint) nem találtam elsődleges dokumentációt („Indexing Vectors"/„Tuning" aloldalak tartalmát nem sikerült teljes egészében lekérni).

### 2.4 pg_analytics / pg_lakehouse sorsa

Egyértelmű láncolat, két lépésben:

- **Átnevezés:** a `pg_analytics` fejlesztői README-je szerint: „`pg_analytics` (formerly named `pg_lakehouse`) puts DuckDB inside Postgres." „`pg_analytics` uses DuckDB v1.1.0 and is supported on Postgres 13+." Forrás: [raw.githubusercontent.com/paradedb/pg_analytics/dev/README.md](https://raw.githubusercontent.com/paradedb/pg_analytics/dev/README.md). Ezt megerősíti a korábbi, `pg_lakehouse` nevű alkönyvtár egy régi commitban: „`pg_lakehouse` is an extension that transforms Postgres into an analytical query engine over object stores like S3 and table formats like Apache Iceberg." Forrás: [github.com/paradedb/paradedb/blob/ea729db.../pg_lakehouse/README.md](https://github.com/paradedb/paradedb/blob/ea729db69722aaacf9071086978fecf358d4340f/pg_lakehouse/README.md).
- **Archiválás:** a `pg_analytics` repó jelenlegi README-je: „The `paradedb/pg_analytics` extension has been discontinued and is archived. This decision was made because ParadeDB's work on Postgres analytics is now being done in our primary extension, `pg_search`." „The code in this repository is no longer maintained." GitHub-fejléc: „This repository was archived by the owner on Mar 19, 2025. It is now read-only." Forrás: [github.com/paradedb/pg_analytics](https://github.com/paradedb/pg_analytics).

### 2.5 Licenc

A fő monorepó `LICENSE` fájlja: „GNU AFFERO GENERAL PUBLIC LICENSE, Version 3, 19 November 2007." Forrás: [raw.githubusercontent.com/paradedb/paradedb/main/LICENSE](https://raw.githubusercontent.com/paradedb/paradedb/main/LICENSE).

A saját blogbejegyzésük a licencválasztásról: az AGPL volt „the only license that met all our criteria" (ismertség, jövőállóság, közösségi jelleg); az alapítók egy korábbi projektje Elastic License 2.0 alatt futott, ami időközben „has since been deprecated" — ez motiválta az AGPL melletti döntést „from day one". Forrás: [paradedb.com/blog/agpl](https://www.paradedb.com/blog/agpl) (publikálva 2024.08.03., tehát kb. 1 évvel a cég alapítása után íródott vissza).

Emellett létezik egy **fizetős „ParadeDB Enterprise"** réteg, más licenccel: „ParadeDB Enterprise adds commercial licensing, support, and physical replication for ParadeDB indexes", szemben a „ParadeDB Community — the AGPL-3.0 open source product" jelöléssel. Az Enterprise pluszfunkciói: „High Availability for ParadeDB indexes" (a Community 1 node-ra korlátozott), „Read replicas for ParadeDB queries", fizikai replikáció. Ár nincs közölve, csak „contact sales" (sales@paradedb.com), nonprofit/nyílt forráskódú projekteknek „complimentary access on a case-by-case basis". Forrás: [paradedb.com/docs/operate/deploy/enterprise](https://www.paradedb.com/docs/operate/deploy/enterprise).

## 3. Verziók és ütem

### 3.1 Legfrissebb verzió

**Három egymástól független forrás** erősíti meg ugyanazt az adatot:

1. GitHub „latest release" oldal: verziócímke **„v0.25.9"**, „Release Date/Time: September 11" (2026), közzétéve a `github-actions` bot által. Forrás: [github.com/paradedb/paradedb/releases/latest](https://github.com/paradedb/paradedb/releases/latest).
2. Docker Hub hivatalos image (`paradedb/paradedb` szervezeti fiók), a tag-lista API-ján keresztül: `v0.25.9` tag, `tag_last_pushed: "2026-09-11T18:28:54.209419Z"`. Forrás: `https://hub.docker.com/v2/repositories/paradedb/paradedb/tags` (Docker Hub hivatalos REST API).
3. PGXN (PostgreSQL Extension Network) csomagbejegyzés: „pg_search 0.25.9 — 2026-09-11 (Stable)". Forrás: [pgxn.org/dist/pg_search](https://pgxn.org/dist/pg_search/).

Ugyanaznap (2026-09-11) egy **release candidate is megjelent**: Docker Hub tag `v0.26.0-rc.1`, `tag_last_pushed: "2026-09-11T22:24:39Z"` — ez a következő minor verzió előzetese, nem stabil kiadás.

**Módszertani megjegyzés:** a GitHub `/releases` HTML-listaoldalát (nem a `/releases/latest` végpontot) többször lekérve a `WebFetch` eszköz **egymásnak ellentmondó** „legfrissebb" verziót adott vissza (egyszer `v0.25.0`/júl. 28., egyszer `v0.24.3`/júl. 15. „Latest" jelöléssel) — ez valószínűleg a JS-alapú GitHub-oldal nem megbízható feldolgozásából (kis segédmodell által összegzett, csonkolt tartalom) ered, nem valós adatellentmondás. A Docker Hub API és a PGXN strukturált, nem-scrapelt adata alapján a fenti (v0.25.9, 2026-09-11) tekinthető megbízhatónak.

### 3.2 Kiadási gyakoriság (kb. utolsó 12 hónap)

A Docker Hub hivatalos tag-előzményei (anonim API-lekérdezéssel kb. 2025-10-29-ig visszamenőleg elérhető, azon túl „pagination offset too large for anonymous requests" hibát ad) alapján **69 db szemver-formátumú kiadási tag** (`vX.Y.Z` és `vX.Y.Z-rc.N`) született 2025-10-29 és 2026-09-11 között (~10,5 hónap alatt) — ez átlagosan **kb. heti 1,5 kiadás**. Néhány konkrét dátum-adatpont ugyanebből a forrásból: v0.20.0 → 2025-11-21, v0.21.0 → 2026-01-07, v0.22.0 → 2026-03-16, v0.23.0 → 2026-04-16, v0.24.0 → 2026-06-03, v0.25.0 → 2026-07-28, v0.25.9 → 2026-09-11. Ezt a PGXN registry (2. független forrás) is megerősíti közel azonos dátumokkal (0.24.0: 2026-06-03, 0.23.0: 2026-04-16, 0.22.0: 2026-03-16, 0.21.0: 2026-01-07, 0.20.0: 2025-11-21 — a kettő szó szerint egyezik).

### 3.3 Támogatott Postgres főverziók

A `pg_search/README.md`: „`pg_search` is supported on official PostgreSQL Global Development Group Postgres versions, starting at PostgreSQL 15." és: „`cargo pgrx init` builds every supported Postgres version this project targets (currently 15–18)." Forrás: [raw.githubusercontent.com/paradedb/paradedb/main/pg_search/README.md](https://raw.githubusercontent.com/paradedb/paradedb/main/pg_search/README.md). Azaz jelenleg **PG 15, 16, 17, 18** a támogatott sáv.

### 3.4 1.0 / stabilitási ígéret, API-stabilitási politika

A projekt **2026 szeptemberében is 0.x verziószámon** áll (legfrissebb: 0.25.9, a következő pedig 0.26.0-rc.1 előzetesként) — formális, külön dokumentált „API stabilitási politikát" vagy „1.0 ígéretet" tartalmazó hivatalos oldalt **nem találtam** (lásd „Amire NINCS forrás").

### 3.5 Törő változások („breaking") a kiadási jegyzékekben

Igen, vannak, explicit „Breaking Changes" jelöléssel — két konkrét, dátumozott példa:

- **v0.25.0 (2026-07-28, friss):** „**Breaking change:** As of `0.25.0`, [`pgvector`](https://github.com/pgvector/pgvector) is a required extension of `pg_search`." — az index access method neve is megváltozott `USING bm25`-ről `USING paradedb`-re (a régi szintaxis visszafelé kompatibilis alias marad). Forrás: [paradedb.com/docs/project/changelog/0.25.0](https://www.paradedb.com/docs/project/changelog/0.25.0).
- **v0.10.0 (korábbi, korai verzió):** „**Breaking Changes 🚨**" szakasz: „New File Paths - ...a big breaking change is that we now store index files in a different location on disk." „Compact Internal IDs - This is a breaking change as v0.10.0's understanding of this field is not compatible with prior versions." „Neither of these changes are backwards compatible." „This will be the last release causing on-disk breaking changes." Forrás: [docs.paradedb.com/changelog/0.10.0](https://docs.paradedb.com/changelog/0.10.0).

## 4. A cég és a projekt egészsége

### 4.1 Ki fejleszti, finanszírozás

Hivatalos bejelentés: „$12M Series A fundraising round" amely „brings our total capital raised to $14M"; vezető befektető: **Craft Ventures**, résztvevő: **Y Combinator** (korábbi befektető). Bejelentés dátuma: 2025. július 14. Forrás: [paradedb.com/blog/series-a-announcement](https://www.paradedb.com/blog/series-a-announcement).

Ezt egy **független, második forrás** is megerősíti: a TechCrunch cikke (2025.07.15.) szerint a társalapítók **Philippe Noël** (CEO) és **Ming Ying** (CTO), az ötlet egy korábbi vállalkozásuk (Whist, felhőalapú böngésző) „Postgres search woes" tapasztalataiból született; a cég 2023-ban alakult, első nyílt forráskódú kiadás 2023 végén; csapatméret a cikk idején („legalább négy fős, tíz fősre bővülő" csapat); ismert ügyfelek: **Alibaba** (első ügyfél, 2024 május), **Modern Treasury**, **Bilt Rewards**, **TCDI**. Forrás: [techcrunch.com/2025/07/15/paradedb-takes-on-elasticsearch...](https://techcrunch.com/2025/07/15/paradedb-takes-on-elasticsearch-as-interest-in-postgres-explodes-amid-ai-boom/). **Figyelem: a csapatlétszám-adat 2025 közepéről származik, 2026-os frissítést nem találtam.**

### 4.2 GitHub-repó aktivitása

A `github.com/paradedb/paradedb` repó-oldal (két egymástól független, ugyanazon a napon végzett lekérésben egyező adatok): **9,2k csillag, 445 fork, 46 watcher, 167 nyitott issue, 38 nyitott pull request**. Forrás: [github.com/paradedb/paradedb](https://github.com/paradedb/paradedb). A pontos **közreműködő- (contributor-) számot és a teljes commit-számot NEM sikerült megbízhatóan megszerezni** — a GitHub `/graphs/contributors` aloldalt a `robots.txt` blokkolja a lekérő eszköz számára, a `api.github.com` REST API pedig ebben a kutatási környezetben szervezetpolitika miatt egyáltalán nem elérhető (403-as hibát ad, „GitHub access to this repository is not enabled for this session"). Lásd „Amire NINCS forrás".

Közvetett aktivitásjelző: a hivatalos Docker image (`paradedb/paradedb`, `paradedb` szervezeti fiók) összesített letöltésszáma **3 112 101 pull** (Docker Hub API, lekérés időpontja: kutatás ideje). Forrás: `https://hub.docker.com/v2/repositories/paradedb/paradedb`.

### 4.3 Ismert éles felhasználók — hivatalos esettanulmányok

A `paradedb.com/customers` oldal **hét, névvel és idézettel ellátott, hivatalos esettanulmányt** listáz:

- „Cofactr replaced MongoDB Atlas Search with ParadeDB to unify its search and primary data stores on Postgres in AWS GovCloud." ([case-study-cofactr](https://www.paradedb.com/customers/case-study-cofactr))
- „Terrapin Finance replaced pg_trgm with ParadeDB to power sub-200ms full-text search across 1.1 billion rows of fixed-income data." ([case-study-terrapin-finance](https://www.paradedb.com/customers/case-study-terrapin-finance))
- „Modern Treasury replaced legacy indexes and roll-up tables with ParadeDB, eliminating query timeouts and increasing write speeds by 2-3x." ([case-study-modern-treasury](https://www.paradedb.com/customers/case-study-modern-treasury))
- „Bilt improved their Postgres performance with ParadeDB, reducing query timeouts by 95%." ([case-study-bilt](https://www.paradedb.com/customers/case-study-bilt))
- „Alibaba Cloud integrated ParadeDB for full text search in their Postgres-based data warehouse." ([case-study-alibaba](https://www.paradedb.com/customers/case-study-alibaba))
- „INSA replaced Elasticsearch with ParadeDB for better performance and simplicity." — részletesen: 1,5 TB, 66 millió dokumentum, „sub-100ms query speeds", integráció on-prem Kubernetes-klaszterre „a matter of days" alatt történt. ([case-study-insa](https://www.paradedb.com/customers/case-study-insa))
- „SweetSpot leveraged ParadeDB for their search infrastructure." ([case-study-sweetspot](https://www.paradedb.com/customers/case-study-sweetspot))

Ezek a cég saját oldalán közölt, tehát **T1-es, de nem független** állítások (a cég maga választja és fogalmazza meg őket) — harmadik féltől származó, tőle független megerősítést (pl. az ügyfél saját nyilatkozata) ezekhez a konkrét számokhoz nem találtam, a TechCrunch-cikk viszont függetlenül is megnevezi az Alibaba, Modern Treasury, Bilt Rewards ügyfélkapcsolatot, ami részleges megerősítés.

## 5. Hogyan futtatható

### 5.1 Docker, Linux, macOS

A hivatalos „self-hosted extension" telepítési dokumentáció szerint elérhető előre fordított csomag: **Debian 12 (Bookworm) és 13 (Trixie)**, **Ubuntu 24.04 (Noble) és 26.04 (Resolute)** (`.deb`), **Red Hat Enterprise Linux 9 és 10** (`.rpm`), valamint **macOS 15 (Sequoia) és 26 (Tahoe)**, plusz „macOS via Postgres.app (PostgreSQL 18)". **Homebrew-formulát a dokumentáció nem említ.** Forrás: [paradedb.com/docs/deploy/self-hosted/extension](https://www.paradedb.com/docs/deploy/self-hosted/extension).

Hivatalos Docker image: `paradedb/paradedb` a Docker Hub-on, a `paradedb` szervezeti fiók alatt publikálva (aktív, napi szintű frissítésekkel — lásd 3.1/3.2 pont).

A hivatalos „Deploy overview" oldal további, név szerint támogatott „Cloud Platform" célok Docker-alapon: **Railway, Render, Fly.io, DigitalOcean, Dokku**; önhosztolt opciók: Postgres-be telepíthető „extension", illetve Kubernetes Helm chart (CloudNativePG-alapon); vállalati opció: **ParadeDB BYOC** (AWS vagy GCP felhőben, „bring your own cloud"). Forrás: [paradedb.com/docs/deploy/overview](https://www.paradedb.com/docs/deploy/overview). Ezt megerősítik a cég saját blogbejegyzései is: „ParadeDB is Officially on Render" és „ParadeDB is Officially on Railway" (paradedb.com/blog/render, paradedb.com/blog/railway).

**Fontos:** ez a hivatalos lista **nem említ név szerint sem AWS RDS-t, sem Supabase-t, sem Neont** támogatott célként — l. lentebb, „Ellentmondások".

### 5.2 ParadeDB Cloud

A `paradedb.com/cloud` oldal jelenlegi (kutatás idejei) tartalma: „We're building a fully managed ParadeDB: one Postgres for your application data, full-text search, vector retrieval, and aggregations. Waitlist open now." Az oldal fejléce: „Coming soon". Ár és pontos elérhetőségi dátum nincs megadva, csak e-mail-várólistára lehet feliratkozni. Forrás: [paradedb.com/cloud](https://www.paradedb.com/cloud). **Tehát a ParadeDB saját, teljesen felügyelt felhős szolgáltatása 2026 szeptemberében még NEM elérhető, csak várólistás.**

### 5.3 Menedzselt Postgres-szolgáltatók — vegyes és időben instabil kép

**Neon:** eredeti hivatalos bejelentés (2025-03-18): „We've teamed up with ParadeDB to bring pg_search to all Neon users, making full-text search in Postgres faster and more powerful." Forrás: [neon.com/blog/pgsearch-on-neon](https://neon.com/blog/pgsearch-on-neon). Ezt **egy évvel később a Neon saját maga vonta vissza**: „Neon support for the `pg_search` extension is deprecated. As of **March 19, 2026**, it is not available for **new** Neon projects." „If you already use `pg_search`: you will continue to have access to the extension on your existing projects." Forrás: [neon.com/docs/changelog/2026-04-03](https://neon.com/docs/changelog/2026-04-03). A migrációs útmutató szerint a **teljes megszüntetés dátuma 2026. szeptember 21.** — azaz a meglévő projektekről is eltávolítják: „pg_search (ParadeDB) is deprecated on Neon: new installs are blocked, and existing installs will be removed"; utódmegoldás: `lakebase_text` (`lakebase_bm25` index, `tsvector` oszlopok alapján, más lekérdezési szintaxissal: `@@@` helyett `@@` + `<@>`). Forrás: [neon.com/docs/extensions/migrate-pg-search-to-lakebase-text](https://neon.com/docs/extensions/migrate-pg-search-to-lakebase-text). Ezt egy független adatpont is alátámasztja: egy nyilvános GitHub-issue címe „Migrate member search from pg_search to lakebase_text (pg_search removed by Neon today)" (forrás: [github.com/msocietyhq/community-os/issues/57](https://github.com/msocietyhq/community-os/issues/57)).

**Supabase:** a Supabase saját oldalán „ParadeDB | Works With Supabase" cím alatt, a hivatalos partnerkatalógusban szerepel. Forrás: [supabase.com/partners/paradedb](https://supabase.com/partners/paradedb). A pontos technikai integráció módját (natívan telepíthető `CREATE EXTENSION pg_search` egy sima Supabase-projekten, vagy csak külön futtatott/párhuzamos infrastruktúráról van szó) a lekérhető oldaltartalomból **nem sikerült egyértelműen megállapítani** — l. „Amire NINCS forrás".

**AWS RDS:** a ParadeDB saját hivatalos dokumentációja ([paradedb.com/docs/deploy/third-party-extensions](https://www.paradedb.com/docs/deploy/third-party-extensions)) **nem tesz említést** az AWS RDS-ről, csak a Citus-ról (elosztott Postgres) egyéb harmadik féltől származó kiterjesztésekkel kapcsolatban. Az **AWS hivatalos dokumentációja** (két aloldal) szerint a `pg_search`/`paradedb` **nem szerepel** a támogatott PostgreSQL-kiterjesztések listáján: sem a [docs.aws.amazon.com/.../PostgreSQL.Concepts.General.FeatureSupport.Extensions.html](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Appendix.PostgreSQL.CommonDBATasks.Extensions.html), sem a [docs.aws.amazon.com/.../postgresql-extensions.html](https://docs.aws.amazon.com/AmazonRDS/latest/PostgreSQLReleaseNotes/postgresql-extensions.html) (PostgreSQL 19/18/17 stb. verziónkénti kiterjesztés-táblázatok) nem tartalmazza egyik nevet sem. Ezzel szemben **egy harmadlagos (T3) blogbejegyzés** azt állítja, az AWS RDS/Aurora „natívan" futtatja: „Running it on Amazon RDS or Aurora gives you managed backups and scaling while keeping vectors close to transactional data", telepítési lépésként: „Create a custom parameter group that adds paradedb to shared_preload_libraries, reboot, then run CREATE EXTENSION paradedb." Forrás: [getgalaxy.io/learn/glossary/how-to-use-paradedb-on-aws-in-postgresql](https://www.getgalaxy.io/learn/glossary/how-to-use-paradedb-on-aws-in-postgresql). **Ez a T3-forrás ellentmond a hivatalos AWS-dokumentációnak** — l. „Ellentmondások".

## Ellentmondások

1. **AWS RDS támogatottsága.** Egy T3 blog (getgalaxy.io) szerint az AWS RDS/Aurora „natívan" futtatja a ParadeDB-t, sima `CREATE EXTENSION paradedb` paranccsal. Ezzel szemben **két hivatalos AWS-dokumentációs oldal** (a kiterjesztés-listák) **nem tartalmazza** sem a `pg_search`, sem a `paradedb` nevet egyetlen támogatott Postgres-verziónál sem. A ParadeDB saját hivatalos dokumentációja (third-party-extensions oldal) sem említi az AWS RDS-t. Nem tudtam feloldani, hogy a blogcikk téved, elavult, vagy az AWS „RDS Custom for PostgreSQL" (OS-szintű hozzáférést adó, nem a sztenderd menedzselt RDS) változatára gondol-e valójában — ez utóbbira nem találtam sem megerősítést, sem cáfolatot.
2. **Neon-támogatottság — időbeli ellentmondás.** 2025 elejéről (és egész 2025-ből) sok forrás (Neon saját blogja, X/Twitter-bejegyzés) azt állítja, hogy a Neon hivatalosan, minden felhasználó számára támogatja a `pg_search`-öt. A Neon 2026-os saját dokumentációja szerint ez **deprecated**, új projekteken 2026. március 19. óta nem elérhető, meglévő projekteken pedig 2026. szeptember 21-ig (azaz gyakorlatilag a kutatás idejére) teljesen megszűnik. A két állítás nem mond ellent egymásnak ha figyelembe vesszük a dátumokat, de **aki csak a 2025-ös forrásokat olvassa, téves képet kap** a 2026 őszi állapotról — ezt a `_kozos.txt` külön is kéri jelezni.
3. **GitHub `/releases` oldal megbízhatatlan scrape-elhetősége.** A `WebFetch` eszközzel többször lekért `github.com/paradedb/paradedb/releases` HTML-oldal egymásnak ellentmondó „legfrissebb verzió" adatokat adott vissza (lásd 3.1 pont) — ez feltehetően a JS-renderelt oldal kis segédmodell általi, hibás/csonkolt összegzéséből ered, nem valódi forrás-ellentmondás. A Docker Hub API és a PGXN strukturált adatai (mindkettő géppel olvasható, nem HTML-scrape) egymással konzisztensek, ezekre támaszkodtam.
4. **Supabase-integráció jellege bizonytalan.** A Supabase „Works With Supabase" partnerkatalógusban listázza a ParadeDB-t, ami mély integrációt sugallhat, miközben a ParadeDB saját hivatalos deploy-dokumentációja **egyáltalán nem** nevesíti a Supabase-t támogatott célként. A két forrás nem cáfolja egymást explicit módon, de egymásnak ellentmondó benyomást kelt a támogatottság szintjéről.

## Amire NINCS forrás

- **A `pg_search` pontos vektoros indexelési algoritmusa** (hogy a „clustered index for vectors" ParadeDB-saját implementáció-e teljes egészében, vagy valamilyen szinten a `pgvector` HNSW/IVFFlat indexét hívja meg) — a részletes „Indexing Vectors"/„Tuning" aloldalak tartalmát nem sikerült teljes egészében lekérni. NINCS FORRÁS a pontos algoritmusszintű válaszra.
- **Formális, külön dokumentált API-stabilitási politika vagy 1.0-ígéret.** Nem találtam olyan hivatalos oldalt vagy nyilatkozatot, amely kimondottan „API stability policy" vagy „path to 1.0" címen ígéretet tenne. NINCS FORRÁS.
- **Pontos GitHub-közreműködő- (contributor-) szám és teljes commit-szám.** A `/graphs/contributors` oldalt a lekérő eszköz `robots.txt`-je blokkolta, az `api.github.com` REST API pedig ebben a kutatási környezetben szervezetpolitika miatt nem elérhető. NINCS FORRÁS.
- **Aktuális (2026-os) alkalmazottlétszám.** Az egyetlen fellelt adat (TechCrunch, 2025.07.15.) „legalább négy fős, tíz fősre törekvő" csapatról beszél — ennél frissebb, 2026-os létszámadatot nem találtam. NINCS FORRÁS.
- **Pontos seed-kör összege a Series A előtt.** A Series A-bejelentésből csak annyi derül ki, hogy az új kör „total capital raised to $14M"-re emeli a bevont tőkét (azaz a 12M-en felül kb. 2M korábbi tőke), de a seed-kör pontos összegét, dátumát és befektetőit külön nem közlik. NINCS FORRÁS.
- **Supabase technikai integrációjának pontos módja** (natív `CREATE EXTENSION` egy sima projektben vs. csak partneri/marketing-szintű kapcsolat). NINCS FORRÁS az egyértelmű megválaszoláshoz.
- **ParadeDB Cloud pontos elindulási dátuma vagy árazása.** Csak „Coming soon" / várólista státusz ismert. NINCS FORRÁS.
- **A Galaxy-blog AWS RDS-állításának technikai pontossága** (RDS Custom vs. sztenderd RDS kérdése — l. Ellentmondások 1. pont). NINCS FORRÁS a feloldáshoz.



---

# SQ02 — Licenc és függőségi kockázat

> **Módszertani megjegyzés (kötelező bevezető).** A `_kozos.txt` előírja az `anthropic-skills:deep-web-research` skill használatát. A skill betöltődött, de a skill Fázis 2 („Search fan-out") és Fázis 6 („Synthesis") párhuzamos Sonnet/Opus alügynökök indítását írja elő (Agent tool). Ebben a munkakörnyezetben **nem állt rendelkezésre subagent-indító eszköz** (nincs `Agent`/`Task`-spawn tool a session eszköztárában), ezért a skill saját leírása szerinti **degradált módban** dolgoztam: egyetlen kontextusban, szekvenciális kereséssel (WebSearch/WebFetch/`curl`), elsődleges források közvetlen (nyers fájl-) lekérésével, majd kézi kereszt-ellenőrzéssel több független forrás között. A Sonnet/Opus modellszétválasztás és a párhuzamos alügynök-fan-out emiatt **nem valósult meg**; ez korlátozza a lefedettség szélességét (kevesebb egyidejű keresési irány), de a forrás-elsődlegesség és az idézet-ellenőrzés elve érvényesült. Emellett ebben a környezetben a `github.com` és `api.github.com` közvetlen böngészése/API-elérése session-szinten korlátozott volt (lásd „Amire NINCS forrás"), és a `web.archive.org` elérése a hálózati szabályzat miatt teljesen blokkolva volt.

## Rövid válasz

A ParadeDB fő terméke — a monorepóban élő `pg_search` kiterjesztés és a teljes `paradedb/paradedb` workspace — ma **AGPL-3.0** licenc alatt áll (repó `LICENSE` fájl, `Cargo.toml` `license = "AGPL-3.0"` mező, dokumentáció, jelenlegi verzió: v0.25.9, 2026-09-11-i kiadás, lekérve 2026-09-22-én). Emellett létezik egy **kereskedelmi/Enterprise** verzió is: a hivatalos összehasonlító oldal szerint a Community és Enterprise funkcionálisan (kereső/index API) azonos, a különbség a licencelésben, a support-ban és a fizikai replikációban (klaszterméret, HA, olvasási replikák) van. A cég saját közlése szerint a licenc „a nap egy óta" (from day one) AGPL, licencváltásra utaló elsődleges forrást nem találtam — viszont egy korábbi, ma már megszűnt komponens, a `pg_analytics` (korábban `pg_lakehouse`), **PostgreSQL License** alatt futott, és csak 2025. március 19-én archiválták, funkcióit a `pg_search`-be (AGPL) olvasztva. Az AGPL 13. szakasza szó szerint a „módosított" verzió hálózaton keresztüli elérésére vonatkozik; az FSF hivatalos GYIK-je szerint a kötelezettség a **módosított** AGPL-programot futtató félre hárul, egy azt **változatlanul** használó, hálózaton kommunikáló kliens saját forráskódjára nem terjed ki explicit módon — de sem az FSF, sem a ParadeDB nem nyilatkozik kifejezetten az „egy be-process Postgres-kiterjesztéssel SQL/MCP protokollon kommunikáló, azt nem módosító alkalmazás" konkrét esetéről, ez értelmezési rés. A pgvector licence a repó `LICENSE` fájla alapján a klasszikus, OSI-jóváhagyott **PostgreSQL License** (BSD/MIT-jellegű, nem copyleft). Függőségi kockázat szempontjából a ParadeDB Inc. egy VC-finanszírozott (2025 júliusában 12 M USD Series A, összesen 14 M USD tőke, Craft Ventures + Y Combinator), 2025 közepén kb. 4 fős csapat által irányított, „lean team" projekt, amely minden közreműködőtől CLA-t (Contributor License Agreement) kér — ez a szerződés a beküldött kódra AGPL **és** kereskedelmi licencelést egyaránt biztosít a cégnek. A pontos „bus factor" számot (contributor-eloszlás) nem sikerült lekérni (lásd lentebb). Ismert, eltérő licencű alternatíva létezik: a Timescale/TigerData `pg_textsearch` kiterjesztése PostgreSQL License alatt fut, míg a TensorChord `VectorChord-bm25` szintén dupla AGPLv3/kereskedelmi modellt használ, tehát a „szigorú copyleft" mintázat nem csak a ParadeDB sajátja az ökoszisztémában.

---

## 1. A ParadeDB pontos licence ma, összetevőnként

### 1.1 A repó `LICENSE` fájlja (szó szerint)

A `paradedb/paradedb` monorepó gyökerében lévő `LICENSE` fájl (lekérve: `https://raw.githubusercontent.com/paradedb/paradedb/main/LICENSE`, 2026-09-22) a teljes, standard AGPL-3.0 licencszöveg. Az első sorai:

> „GNU AFFERO GENERAL PUBLIC LICENSE
> Version 3, 19 November 2007
>
> Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
> Everyone is permitted to copy and distribute verbatim copies
> of this license document, but changing it is not allowed.
>
> Preamble
>
> The GNU Affero General Public License is a free, copyleft license for
> software and other kinds of works, specifically designed to ensure
> cooperation with the community in the case of network server software."

A fájl a szabvány AGPL-3.0-sablon szöveg, egyedi „Copyright (C) \<year> \<name of author>" kitöltés nélkül (a záró rész is a generikus AGPL-sablon mintaszöveget tartalmazza, nem egy kitöltött, ParadeDB-specifikus copyright-fejlécet).

### 1.2 Cargo.toml — workspace-szintű megerősítés

A repó gyökér `Cargo.toml` fájlja (`https://raw.githubusercontent.com/paradedb/paradedb/main/Cargo.toml`, lekérve 2026-09-22) explicit módon deklarálja:

> „[workspace.package]
> version = "0.25.6"
> edition = "2024"
> license = "AGPL-3.0""

A `pg_search/Cargo.toml` a `license = { workspace = true }` mezővel örökli ezt — tehát a `pg_search` (a fő kereső-kiterjesztés) külön `LICENSE` fájl nélkül, a workspace AGPL-3.0 licencét használja. (Megjegyzés: a Cargo.toml itt 0.25.6-ot mutatott, míg a dokumentációs oldal és a PGXN aznap 0.25.9-et — ez a projekt gyors kiadási ütemét tükrözi, ld. „Ellentmondások".)

### 1.3 Hivatalos dokumentáció — licencoldal / Enterprise összehasonlító oldal

A `https://docs.paradedb.com/deploy/enterprise` oldal (lekérve 2026-09-22, dokumentáció verziója a navigációban: „v0.25.9") szó szerint:

> „ParadeDB ships in two versions: ParadeDB Community and ParadeDB Enterprise. Both editions expose the same SQL APIs for search, filtering, sorting, joins, and analytics. ParadeDB Community is the AGPL-3.0 open source product. It supports single-node deployments. ParadeDB Enterprise adds commercial licensing, support, and physical replication for ParadeDB indexes. Use Enterprise when the ParadeDB index itself needs high availability, failover, or read replicas that can serve ParadeDB queries. For access to ParadeDB Enterprise, please contact sales."

Az oldal explicit „Feature Comparison" táblázatot közöl (idézve, tömörítve):

> „Feature Comparison | ParadeDB Community | ParadeDB Enterprise
> Index Configuration — Support for most Postgres types ✅ ✅; Custom tokenizers and filters ✅ ✅; Multiple tokenizers per field ✅ ✅
> Search — Full-text search with BM25 ✅ ✅; Vector search ✅ ✅; Hybrid search ✅ ✅; Sorting and Top K ✅ ✅; Filtering ✅ ✅; Join pushdown ✅ ✅; Aggregates and facets ✅ ✅
> Concurrency and Consistency — Postgres MVCC-safe ✅ ✅; Concurrent, non-blocking writes ✅ ✅; Block storage integration ✅ ✅; Buffer cache integration ✅ ✅
> Deployment — Maximum ParadeDB index nodes: **1** vs. **Unlimited**; Crash Recovery ✅ ✅; Point in Time Recovery ✅ ✅; High Availability for ParadeDB indexes **❌ / ✅**; Read replicas for ParadeDB queries **❌ / ✅**"

Vagyis a hivatalos forrás szerint az egyetlen **funkcionális** (nem licencelési) eltérés a Community és Enterprise között a ParadeDB-index csomópontszáma, a magas rendelkezésre állás és az olvasási replikák támogatása — minden keresési/lekérdezési/aggregációs funkció (BM25, vektoros keresés, hibrid keresés, join pushdown, facetting stb.) azonos mindkét verzióban. Az oldal azt is jelzi, hogy nonprofit/nem-kereskedelmi nyílt forráskódú projektek esetenkénti ingyenes hozzáférést kaphatnak: „If you're a non-profit or a non-commercial open source project and are interested in ParadeDB Enterprise, please contact sales. We provide complimentary access on a case-by-case basis."

Az „adds commercial licensing" fordulat azt jelzi, hogy az Enterprise verzióhoz **külön kereskedelmi (nem-AGPL) licencszerződés** tartozik, de a jelenlegi oldal-szövegben nem szerepel szó szerint olyan mondat, hogy a kereskedelmi licenc „waives the copyleft provision" (ezt egy korábbi, automatikus összefoglaló-lekérés állította, de a nyers HTML-ből kinyert, teljes oldal-szöveg — 2026-09-22-i friss lekérés — nem tartalmazza sem a „waive", sem a „copyleft" szót; ld. „Ellentmondások").

### 1.4 „Why We Picked AGPL" — saját nyilatkozat a komponensek köréről

A hivatalos blogbejegyzés (`https://www.paradedb.com/blog/agpl`, szerző: Philippe Noël, dátum: 2024. augusztus 3., lekérve 2026-09-22) szerint:

> „ParadeDB has been licensed under the GNU Affero General Public License 3.0 — also known as AGPL — from day one."

és a monetizációról:

> „Monetization. We have monetized through support contracts and issuing commercial, non-AGPL licenses, which also contain a few closed-source enterprise features."

Ez megerősíti, hogy létezik **külön, nem-AGPL kereskedelmi licenc**, és hogy ehhez **néhány zárt forráskódú Enterprise-funkció** is tartozik — bár a jelenlegi (2026-09-22-i) hivatalos Enterprise-összehasonlító táblázat szerint ez ma konkrétan a HA/read-replica/csomópontszám-korlátra redukálódik (ld. 1.3).

### 1.5 Egy korábbi ParadeDB-komponens MÁS licenc alatt: `pg_analytics` — PostgreSQL License

A `paradedb/pg_analytics` (korábbi nevén `pg_lakehouse`, DuckDB-alapú Postgres-analitika) **külön repó**, és **nem** AGPL, hanem PostgreSQL License alatt futott. A repó `LICENSE` fájlja (`https://raw.githubusercontent.com/paradedb/pg_analytics/dev/LICENSE`, lekérve 2026-09-22):

> „The PostgreSQL License
>
> Copyright (c) 2025, ParadeDB
>
> Permission to use, copy, modify, and distribute this software and its documentation for any purpose, without fee, and without a written agreement is hereby granted, provided that the above copyright notice and this paragraph and the following two paragraphs appear in all copies."

A repó `README.md`-je (ugyanonnan lekérve) és a GitHub archív-banner (`https://github.com/paradedb/pg_analytics`, WebFetch, 2026-09-22, két külön lekérdezéssel megerősítve) szerint:

> „The `paradedb/pg_analytics` extension has been discontinued and is archived. This decision was made because ParadeDB's work on Postgres analytics is now being done in our primary extension, `pg_search`."

> „This repository was archived by the owner on Mar 19, 2025. It is now read-only."

Tehát: **nem minden „ParadeDB extension" volt/AGPL** — a `pg_analytics` PostgreSQL License alatt állt, majd 2025. március 19-én megszűnt, funkcióit a (AGPL alatt álló) `pg_search`-be integrálták. Ez ellentmond a lentebb (2. és 5. pont) idézett, 2024. májusi HN-kommentnek, mely szerint „All ParadeDB extensions are released under AGPL-3.0" — ld. „Ellentmondások".

### 1.6 ParadeDB GitHub-szervezet — a többi repó licencelése (áttekintés)

A `https://github.com/orgs/paradedb/repositories` (WebFetch, 2026-09-22) szerint a szervezet egyéb, kapcsolódó repói vegyes licencűek, jellemzően permisszívek:

- `tantivy` (a `pg_search` alap keresőmotor-könyvtára, Postgres-optimalizált fork) — MIT
- `pgrx` (a Rust-Postgres-kiterjesztés keretrendszer, amivel a `pg_search` épül) — a GitHub UI „Other"-ként jelzi (nem AGPL)
- ORM-integrációk (`drizzle-paradedb`, `django-paradedb`, `sqlalchemy-paradedb`, `rails-paradedb`, `efcore-paradedb`, `prisma-paradedb`) — MIT
- `website`, `charts` (Helm chart), `docker-official-images` — Apache 2.0
- `pg_analytics` (archivált) — PostgreSQL License

Vagyis a szigorú AGPL-3.0 copyleft **kifejezetten a fő adatbázis-motorra/kiterjesztésre** (a `paradedb/paradedb` repóra, benne a `pg_search`-re) koncentrálódik; a kliens-oldali/ökoszisztéma-integrációk (ORM-csomagok stb.) megengedőbb (MIT/Apache) licenc alatt állnak.

---

## 2. Licenctörténet

**Elsődleges (saját) állítás — nincs licencváltás.** A „Why We Picked AGPL" bejegyzés (2024-08-03) kifejezetten azt állítja, hogy a licenc „from day one" AGPL volt, azaz a szerző szerint sosem volt más a fő projekt licence.

**Korábbi közvetett megerősítés (HN, 2024. május).** A Hacker News-on (`https://news.ycombinator.com/item?id=40348443`) egy, a fő poszt szerint ParadeDB-alapító („philippemnoel") által írt komment (2024. május 13.) így fogalmaz:

> „All ParadeDB extensions are released under AGPL-3.0. We've found that it strikes the right balance between being open-source and enabling the community…"

Ez időben **megelőzi** az augusztusi blogbejegyzést, és azt sugallja, hogy már 2024 közepén is AGPL volt érvényben — de (ld. 1.5. pont) ez az állítás pontatlan volt, mert a `pg_analytics` akkor még létező, aktív komponens PostgreSQL License alatt futott, nem AGPL alatt.

**Az induló, 2023-as állapot közvetlen ellenőrzése nem sikerült.** A projekt első blogbejegyzése („Introducing ParadeDB", `https://www.paradedb.com/blog/introducing-paradedb`, szerző: Ming Ying, dátum: 2023. augusztus 31.) **nem tartalmaz explicit licenc-utalást** (WebFetch-es ellenőrzés, 2026-09-22). A `pg_bm25 → pg_search` átnevezésről szóló bejegyzés („Introducing ParadeDB pg_search: Elastic-Quality Full Text Search Inside Postgres", `https://www.paradedb.com/blog/introducing-search`, szerző: Ming Ying, 2023. november 15., v0.6.0-hoz kötve) szintén **nem említ licencet**:

> „With the release of v0.6.0, which marks the first stable release of the ParadeDB full-text search extension, we have renamed pg_bm25 to pg_search."

A CMU Database Group „Database of Databases" bejegyzése (`https://dbdb.io/db/paradedb`, T2/T3 harmadik fél forrás, WebFetch, 2026-09-22) függetlenül megerősíti a jelenlegi „AGPL v3" licencet, és az első commit dátumát 2023. június 30-ra teszi, de **nem tartalmaz** információt korábbi licencváltásról.

Az internetes archívum (Wayback Machine, `web.archive.org`) közvetlen ellenőrzése — ami a 2023-as `LICENSE`-fájl tényleges, archivált állapotát mutathatta volna — ebben a munkakörnyezetben **hálózati szabályzat miatt teljesen blokkolva volt** (mind `curl`, mind a `WebFetch` eszköz „Blocked by egress policy" / „SITE_BLOCKED" hibát adott). Emiatt a „licenc sosem változott" állítást **kizárólag a ParadeDB saját, utólagos (2024-es) nyilatkozata és közvetett korabeli jelek (2023 novemberi rebrand-poszt licenc-említés nélkül, a mai LICENSE-fájl formátuma) támasztják alá — független, korabeli (2023-as) elsődleges forrmargóval nem sikerült megerősíteni.**

**Összegzés:** a fő motor (pg_bm25 → pg_search, ma a `paradedb/paradedb` repó) licencére vonatkozóan **nem található elsődleges forrás arra, hogy valaha PostgreSQL License vagy más engedékenyebb licenc alatt állt volna**; a projekt saját állítása szerint mindig AGPL volt. Ezzel párhuzamosan viszont **igazolt tény**, hogy a projekt ökoszisztémáján belül **létezett és létezik** PostgreSQL License / MIT / Apache 2.0 alatt álló komponens is (`pg_analytics`, `tantivy`, ORM-adapterek stb.), ami finomítja azt az egyszerűsítő állítást, hogy „a ParadeDB AGPL".

---

## 3. Mit jelent az AGPL-3.0 ebben a helyzetben — elsődleges források

### 3.1 Az AGPL-3.0 13. szakasza szó szerint

Forrás: a hivatalos GNU szöveg (`https://www.gnu.org/licenses/agpl-3.0.txt`, letöltve 2026-09-22) és — ezzel szóról szóra megegyezően — a ParadeDB repó `LICENSE` fájlja:

> „13. Remote Network Interaction; Use with the GNU General Public License.
>
> Notwithstanding any other provision of this License, if you modify the Program, your modified version must prominently offer all users interacting with it remotely through a computer network (if your version supports such interaction) an opportunity to receive the Corresponding Source of your version by providing access to the Corresponding Source from a network server at no charge, through some standard or customary means of facilitating copying of software. This Corresponding Source shall include the Corresponding Source for any work covered by version 3 of the GNU General Public License that is incorporated pursuant to the following paragraph.
>
> Notwithstanding any other provision of this License, you have permission to link or combine any covered work with a work licensed under version 3 of the GNU General Public License into a single combined work, and to convey the resulting work. The terms of this License will continue to apply to the part which is the covered work, but the work with which it is combined will remain governed by version 3 of the GNU General Public License."

Fontos: a kötelezettség kifejezetten akkor áll be, ha **„you modify the Program"** — azaz a „Program" (itt: ParadeDB/pg_search) módosításához kötött, nem magához a hálózati eléréshez általában.

### 3.2 FSF/GNU hivatalos GYIK — a releváns kérdések szó szerint

Forrás: `https://www.gnu.org/licenses/gpl-faq.html` (letöltve 2026-09-22, HTML-ből kinyerve, anchor-azonosítókkal).

**„UnreleasedModsAGPL"** — mit kell tennie egy AGPL-programot futtató, azt módosító cégnek:

> „A company is running a modified version of a program licensed under the GNU Affero GPL (AGPL) on a web site. Does the AGPL say they must release their modified sources? […] The GNU Affero GPL requires that modified versions of the software offer all users interacting with it over a computer network an opportunity to receive the source. What the company is doing falls under that meaning, so the company must release the modified source code."

**„AGPLv3InteractingRemotely"** — mi számít „hálózaton keresztüli távoli interakciónak":

> „In AGPLv3, what counts as 'interacting with [the software] remotely through a computer network?' […] If the program is expressly designed to accept user requests and send responses over a network, then it meets these criteria. Common examples of programs that would fall into this category include web and mail servers, interactive web-based applications, and servers for games that are played online. If a program is not expressly designed to interact with a user through a network, but is being run in an environment where it happens to do so, then it does not fall into this category. For example, an application is not required to provide source merely because the user is running it over SSH, or a remote X session."

**„AGPLv3ServerAsUser"** — kliens-szoftverre vonatkozó kérdés (a kérdés maga is releváns, mert a „kliens vs. szerver" megkülönböztetést tárgyalja):

> „If some network client software is released under AGPLv3, does it have to be able to provide source to the servers it interacts with? […] AGPLv3 requires a program to offer source code to 'all users interacting with it remotely through a computer network.' It doesn't matter if you call the program a 'client' or a 'server,' the question you need to ask is whether or not there is a reasonable expectation that a person will be interacting with the program remotely over a network."

Megjegyzés: ez a konkrét GYIK-pont arról szól, hogy **ha egy kliens szoftver maga AGPLv3 alatt van kiadva**, annak kell-e forrást adnia a szerverének — ami **más eset**, mint a mi kérdésünk (egy **nem**-AGPL alkalmazás beszél egy AGPL adatbázis-szerverrel).

**„AGPLv3CorrespondingSource"** — mit kell pontosan kiadni módosítás esetén:

> „Under AGPLv3, when I modify the Program under section 13, what Corresponding Source does it have to offer? […] 'Corresponding Source' is defined in section 1 of the license, and you should provide what it lists. So, if your modified version depends on libraries under other licenses, such as the Expat license or GPLv3, the Corresponding Source should include those libraries (unless they are System Libraries). If you have modified those libraries, you must provide your modified source code for them."

**„SeparateAffero"** — miért külön licenc az AGPL (kontextus, miért nem GPLv3 egy klauzulával):

> „Why did you decide to write the GNU Affero GPLv3 as a separate license? […] By publishing the GNU Affero GPLv3 as a separate license, with provisions in it and GPLv3 to allow code under these licenses to link to each other, we accomplish all of our original goals while making it easier to determine which code has the source publication requirement."

### 3.3 Kapcsolódó (általános GPL-családi, nem AGPL-specifikus) FSF-elvek a „különálló program vs. kombinált mű" kérdésről

Ezek **nem AGPL-specifikus** GYIK-pontok, hanem az általános GPL-keretrendszer „hol a határ két külön program és egy kombinált program között" elvét fejtik ki — ugyanabból a hivatalos FSF GYIK-ből (`gpl-faq.html`), és tartalmilag relevánsak lehetnek annak megítélésekor, hogy egy külön folyamatban futó, hálózaton (socket/wire protocol) kommunikáló kliens „önálló programnak" számít-e:

**„MereAggregation":**

> „Where's the line between two separate programs, and one program with two parts? […] We believe that a proper criterion depends both on the mechanism of communication (exec, pipes, rpc, function calls within a shared address space, etc.) and the semantics of the communication (what kinds of information are interchanged). […] By contrast, pipes, sockets and command-line arguments are communication mechanisms normally used between two separate programs. So when they are used for communication, the modules normally are separate programs."

**„GPLInProprietarySystem":**

> „[…] in many cases you can distribute the GPL-covered software alongside your proprietary system. To do this validly, you must make sure that the free and nonfree programs communicate at arms length, that they are not combined in a way that would make them effectively a single program."

**Értelmezési bizonytalanság (nem jogi következtetés, csak a rés megjelölése):** a fenti idézetek két, elméletileg releváns, de **különálló** FSF-forrásból származnak: (a) az AGPL 13. szakasz és a hozzá tartozó AGPL-specifikus GYIK, amely a **módosított** AGPL-program hálózati elérésére vonatkozik; (b) az általános GPL „mere aggregation"/„arm's length" elve, amely azt tárgyalja, mikor számít két, socket/pipe-on kommunikáló program „különállónak". **Sem az FSF hivatalos GYIK-je, sem a ParadeDB semmilyen fellelt hivatalos nyilatkozata nem alkalmazza expliciten ezt a két elvet együtt** arra a konkrét architektúrára, amikor (i) egy Postgres-kiterjesztés (a `pg_search`, amely dinamikusan linkelt `.so`-ként töltődik be magába a PostgreSQL szerverfolyamatba) AGPL alatt fut, és (ii) egy **különálló folyamatként futó** kliens/MCP-szerver a szabványos PostgreSQL wire protokollon (hálózati socketen) keresztül, **a `pg_search`-öt nem módosítva** küld neki SQL-lekérdezéseket. Nincs olyan elsődleges forrás — sem FSF, sem ParadeDB —, amely kimondottan ezt az esetet (Postgres-kiterjesztés + attól különálló, network-protokollon kommunikáló, változatlan kliens) minősítené. Ez explicit értelmezési rés; jogi következtetést ehhez a kutatás nem fűz.

### 3.4 ParadeDB saját nyilatkozata a hálózati kliensek AGPL-relevanciájáról

A „Why We Picked AGPL" bejegyzés (ld. 1.4) **nem tér ki explicit módon** arra, hogy a ParadeDB-vel (mint adatbázis-szerverrel) hálózaton kommunikáló, azt nem módosító alkalmazásra mi vonatkozik. A ParadeDB dokumentáció-indexében (`https://docs.paradedb.com/llms.txt`, teljes oldaltérkép, 2026-09-22) **nem szerepel** külön „License FAQ" vagy hasonló oldal. **Nem található ParadeDB-saját GYIK vagy nyilatkozat erről a konkrét kérdésről** — ld. „Amire NINCS forrás".

---

## 4. A pgvector licence

A `pgvector/pgvector` repó `LICENSE` fájlja (`https://raw.githubusercontent.com/pgvector/pgvector/master/LICENSE`, lekérve 2026-09-22, teljes egészében idézve):

> „Portions Copyright (c) 1996-2026, PostgreSQL Global Development Group
>
> Portions Copyright (c) 1994, The Regents of the University of California
>
> Permission to use, copy, modify, and distribute this software and its documentation for any purpose, without fee, and without a written agreement is hereby granted, provided that the above copyright notice and this paragraph and the following two paragraphs appear in all copies.
>
> IN NO EVENT SHALL THE UNIVERSITY OF CALIFORNIA BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF THE UNIVERSITY OF CALIFORNIA HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
>
> THE UNIVERSITY OF CALIFORNIA SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE SOFTWARE PROVIDED HEREUNDER IS ON AN 'AS IS' BASIS, AND THE UNIVERSITY OF CALIFORNIA HAS NO OBLIGATIONS TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS."

Ez a szöveg a szabványos **„PostgreSQL License"** (OSI-jóváhagyott, BSD/MIT-jellegű, nem copyleft, engedékeny licenc — vö. `https://opensource.org/license/postgresql`, T1/T2 kiegészítő forrás a licenctípus azonosításához, tartalmilag megegyezik a fenti idézett szöveggel). A pgvector tehát **nem** AGPL, nem copyleft, és semmilyen forrás-kiadási vagy hálózati kötelezettséget nem ró a felhasználóra.

**Kereszt-ellenőrzés / megjegyzés:** egy automatikus (nem elsődleges, összefoglaló jellegű) lekérdezési kísérlet tévesen „Apache 2.0"-t jelzett a pgvector licenceként; ezt a nyers `LICENSE`-fájl közvetlen, kétszeri ellenőrzésével cáfoltam — a fájl tartalma egyértelműen és következetesen a fenti PostgreSQL License szöveg. Ld. „Ellentmondások".

---

## 5. Függőségi kockázat

### 5.1 Jelek arra, hogy funkciók a fizetős verzióba vándorolnak / a licenc szigorodhat

- A saját blogbejegyzés (2024-08-03) szerint már akkor is léteztek „a few closed-source enterprise features" — tehát a zárt Enterprise-funkciók **nem újkeletűek**, a modell kezdettől „open core"-szerű.
- A jelenlegi (2026-09-22-i) hivatalos Enterprise-összehasonlító oldal (ld. 1.3) szerint az Enterprise-kizárólagos funkciók köre ma **konkrétan**: korlátlan ParadeDB-index csomópontszám, magas rendelkezésre állás, olvasási replikák. Minden más (keresési, indexelési, aggregációs) funkció azonos a két kiadásban.
- **Nem találtam** elsődleges forrást (hivatalos bejelentés, changelog-bejegyzés, GitHub issue/discussion) arra, hogy egy **korábban Community-ben elérhető** funkciót utólag Enterprise-ba mozgattak volna át (azaz konkrét „downgrade" eseményt). A `https://github.com/orgs/paradedb/discussions/3521` című vita címe („BM25 reads on streaming replication standbys worked in 0.18.10, blocked in 0.19.5?") **felveti** egy ilyen funkcióváltozás gyanúját (BM25-olvasás streaming standby-okon, ami 0.18.10-ben működött, 0.19.5-ben blokkolva), de a vita **tartalmát nem sikerült elolvasni** (a GitHub Discussions-oldalak elérése ebben a munkakörnyezetben korlátozott volt) — ezért ezt csak **címként**, nem megerősített tartalmi állításként rögzítem; önmagában nem tekinthető megerősített bizonyítéknak funkció-elvonásra.
- Nem találtam elsődleges forrást arra, hogy a ParadeDB az AGPL-t egy még szigorúbb licencre (pl. SSPL, BSL, saját forrás-elérhetőségi licenc) kívánná váltani. A blogbejegyzés kifejezetten a hosszú távú stabilitást ígéri: „Future-Proof: […] Our users should trust that our project will stand the test of time."

### 5.2 „Bus factor" — közreműködők eloszlása

**A pontos szám nem állapítható meg ebben a kutatásban.** A GitHub natív „Contributors" grafikonja (`https://github.com/paradedb/paradedb/graphs/contributors`) és a GitHub `robots.txt`-je explicit módon tiltja ennek automatikus lekérését (`Disallow: /*/*/graphs`, `Disallow: /*/*/contributors`, `Disallow: /*/*/commits/`) — ezt közvetlenül ellenőriztem a `https://github.com/robots.txt` fájlban. A `github.com` és `api.github.com` REST API közvetlen (session-szintű) elérése ebben a környezetben szintén korlátozott volt (a proxy „GitHub access to this repository is not enabled for this session" hibát adott vissza). Harmadik féltől származó, számszerű contributor-statisztikát tartalmazó oldalt (pl. OSS Insight-jellegű elemző szolgáltatást) a keresés nem talált a ParadeDB-hez.

**Közvetett, minőségi jelek a kormányzási/bus-factor kockázatról:**

- A `CONTRIBUTING.md` (`https://raw.githubusercontent.com/paradedb/paradedb/main/CONTRIBUTING.md`, lekérve 2026-09-22) szerint minden külső hozzájárulónak alá kell írnia egy CLA-t:

  > „In order for us, ParadeDB, Inc., to accept patches and other contributions from you, you need to adopt our ParadeDB Contributor License Agreement (the 'CLA'). […] By contributing to ParadeDB, you agree that your contributions will be licensed under the GNU Affero General Public License v3.0 and as commercial software."

  Ez azt jelenti, hogy minden beküldött kód **egyszerre** kerül AGPL **és** kereskedelmi licenc alá — azaz a ParadeDB Inc. jogilag szabadon beépítheti a közösségi hozzájárulásokat a zárt forráskódú Enterprise-termékbe is.

- A CLA saját szövege (`https://gist.github.com/philippemnoel/5ba3a20230bc1c3c0ae89caeb0597f4a`, „ParadeDB Individual Contributor License Agreement", WebFetch-en keresztül idézve) tartalmaz egy tág, visszavonhatatlan jogátadási klauzulát:

  > „perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable copyright license to reproduce, prepare derivative works of, publicly display, publicly perform, sublicense, and distribute Your Contributions"

  (Megjegyzés: ez a CLA-idézet egy WebFetch-alapú, összefoglaló jellegű lekérésből származik, nem nyers fájlból — a szöveg tartalmilag konzisztens a CONTRIBUTING.md közvetlenül idézett, nyersen ellenőrzött állításával, de a szó szerinti pontosságot csak a CONTRIBUTING.md-idézetre garantálom teljes bizonyossággal.)

- A projekt egyetlen cég (ParadeDB, Inc.) irányítása alatt áll, nem alapítványi/többszereplős kormányzású (nincs pl. Apache Software Foundation-szerű semleges felügyelet). A TechCrunch cikke (`https://techcrunch.com/2025/07/15/paradedb-takes-on-elasticsearch-as-interest-in-postgres-explodes-amid-ai-boom`, 2025-07-15, T2 forrás) szerint:

  > „The startup was founded in 2023 and released the first open source version of the product later that year." — és a cikk a csapatot ekkor (2025 közepén) **„a team of four"**-ként írja le, azzal, hogy legalább 10 főre kívánnak nőni.

  A ParadeDB saját Roadmap-oldala (`https://www.paradedb.com/docs/project/roadmap.md`, lekérve 2026-09-22) ezt megerősíti: „We're a lean team that likes to ship at incredibly high velocity."

- Finanszírozás (kettős, egymástól független forrással alátámasztva): a ParadeDB saját blogja (`https://www.paradedb.com/blog/series-a-announcement`, szerző: Ming Ying, 2025-07-14) és a TechCrunch cikke egyaránt megerősíti:

  > „We're excited to announce our $12M Series A fundraising round, led by Craft Ventures and joined by existing investors including Y Combinator. This brings our total capital raised to $14M."

  Ez azt jelzi, hogy a projekt jövője, ütemterve és licencpolitikája erősen egyetlen, kockázati tőke által finanszírozott cég üzleti döntéseitől függ — ami klasszikus „bus factor"/vendor-lock kockázat vállalati szempontból, függetlenül a nyers contributor-számtól.

- Növekedési adatok (két időpontból, ugyanattól a forrás-családtól): a 2024-08-03-i blogbejegyzés szerint „ParadeDB has gained 5K stars in the past year" és „ParadeDB has been deployed 40K times"; a jelenlegi (2026-09-22) GitHub-oldal szerint a csillagok száma **9.2k**, forkok száma **445**, nyitott issue-k száma **167**, nyitott PR-ek száma **38**, commit-ok száma (main ágon) **3 491**. Ez lassuló, de folyamatos növekedést jelez, exponenciális helyett inkább lineáris ütemben (5K → 9,2K csillag kb. két év alatt).

### 5.3 Fork vagy közösségi alternatíva

- **Nem található fork** a `paradedb/paradedb` főrepóból (a keresés több, egyértelműen személyes/tükröző klón GitHub-repót talált — pl. `wangkhc/paradedb`, `thebhavye/paradedb`, `sahilchug/paradedb` — de ezek leírásuk alapján egyszerű forkok/tükrök, nem önálló, elágazó közösségi projektek saját irányvonallal; ezt nem tekintem „independens fork"-nak a kérdés értelmében).
- **Léteznek funkcionálisan versengő, más licencű Postgres BM25/full-text-search kiterjesztések:**
  - **`pg_textsearch`** (Timescale / TigerData) — a repó `LICENSE` fájlja (`https://raw.githubusercontent.com/timescale/pg_textsearch/main/LICENSE`, lekérve 2026-09-22) szintén a PostgreSQL License szövegét tartalmazza:

    > „The PostgreSQL License
    >
    > Permission to use, copy, modify, and distribute this software and its documentation for any purpose, without fee, and without a written agreement is hereby granted, provided that the above copyright notice and this paragraph…"

    Ez egy **engedékenyebb licencű, közvetlen funkcionális alternatíva** BM25-kereséshez Postgres-ben (hivatalos bejelentés: `https://www.postgresql.org/about/news/pg_textsearch-v10-3264`, PostgreSQL.org hírportál, T1/T2 forrás).
  - **`VectorChord-bm25`** (TensorChord) — a repó `LICENSE` fájlja (`https://raw.githubusercontent.com/tensorchord/VectorChord-bm25/main/LICENSE`, lekérve 2026-09-22) szerint:

    > „# Dual License Notice
    >
    > This software is licensed under a dual license model. You may choose to use this software under one of the following licenses:
    >
    > 1. GNU Affero General Public License v3 (AGPLv3)"

    Vagyis ez az „alternatíva" **maga is AGPL/kereskedelmi dupla licencmodellt** használ — tehát az AGPL mintázat nem kizárólag a ParadeDB sajátja a Postgres BM25-ökoszisztémában.
  - **ZomboDB** (a `pg_search` egyik elismert szellemi elődje, amely külső Elasticsearch-motorra épít) — a ParadeDB saját blogbejegyzése (`introducing-search`, 2023-11-15) nevesíti mint előzményt, de a ZomboDB `LICENSE`-fájlját ebben a kutatásban **nem sikerült elérni** (a `master`/`main` ág `raw.githubusercontent.com`-os lekérése 404-et adott — valószínűleg más az alapértelmezett ág neve vagy a fájl elérési útja), így a ZomboDB pontos jelenlegi licence ebből a kutatásból **NINCS FORRÁS**.

---

## Ellentmondások

1. **„Waives the copyleft provision" kontra a nyers oldal-szöveg.** Egy első, automatikus (összefoglaló-alapú) lekérdezés azt állította, hogy a `docs.paradedb.com/deploy/enterprise` oldal szó szerint tartalmazza, hogy a kereskedelmi licenc „waives the copyleft provision of AGPL-3.0". Egy közvetlen, nyers HTML-ből kinyert, teljes oldal-szöveg (kétszer ellenőrizve, 2026-09-22) **nem tartalmazza** sem a „waive", sem a „copyleft" szót. A tényleges, ellenőrzött szöveg csak annyit mond: „ParadeDB Enterprise adds commercial licensing, support, and physical replication for ParadeDB indexes." Ezt eszköz-generált hibaként kezelem, nem hivatalos forrás-ellentmondásként, de jelzem, mert a kutatás során ez felmerült.

2. **„All ParadeDB extensions are released under AGPL-3.0" (HN, 2024-05) kontra a `pg_analytics` PostgreSQL License.** A 2024. májusi HN-kommentben (feltételezett ParadeDB-alapítói szerzőség) az áll, hogy „minden" ParadeDB-kiterjesztés AGPL-3.0. Ugyanakkor a `pg_analytics` (2025 márciusáig aktív, hivatalos ParadeDB-repó) végig **PostgreSQL License** alatt futott. A két elsődleges/közel-elsődleges forrás tehát ellentmond egymásnak — nem simítottam el, mindkettőt idéztem.

3. **Verzió-eltérés (nem valódi ellentmondás, csak időzítési jelenség).** A repó gyökér `Cargo.toml`-ja 0.25.6-ot mutatott, míg a dokumentációs navigáció és a PGXN aznap (2026-09-22) 0.25.9-et — ez a projekt gyakori kiadási ciklusának (napi/heti kiadások) tudható be, nem tényleges ellentmondás, csak lekérdezés-időzítési különbség; mindkét számot rögzítettem dátummal.

4. **pgvector licence: egy automatikus lekérdezés „Apache 2.0"-t állított**, míg a nyers `LICENSE`-fájl (kétszer ellenőrizve) egyértelműen és következetesen PostgreSQL License szöveget tartalmaz. Az „Apache 2.0" állítást eszköz-hibaként (nem hiteles forrásként) kezelem, és nem szerepeltetem tényként.

---

## Amire NINCS forrás

- **Pontos contributor-szám / commit-eloszlás (bus factor számszerűsítve) a `paradedb/paradedb` repóhoz.** A GitHub `graphs/contributors` oldala a `robots.txt` szerint tiltott (`Disallow: /*/*/graphs`, `/*/*/contributors`, `/*/*/commits/`), a GitHub API session-szinten nem volt elérhető ebben a környezetben, és harmadik féltől származó, számszerű elemző oldalt nem találtam a ParadeDB-hez. **NINCS FORRÁS.**
- **A 2023-as (induláskori) `LICENSE`-fájl független, korabeli (nem utólagos) igazolása.** A Wayback Machine (`web.archive.org`) elérése ebben a munkakörnyezetben hálózati szabályzat miatt teljesen blokkolva volt. Csak a ParadeDB saját, 2024-es utólagos nyilatkozata áll rendelkezésre arra, hogy a licenc „from day one" AGPL volt. **NINCS FORRÁS** egy 2023-as, független pillanatfelvételre.
- **ParadeDB saját, kifejezett állásfoglalása/GYIK-je arról, hogy egy vele hálózaton (Postgres wire protocol / MCP-n keresztül) kommunikáló, őt nem módosító kliensalkalmazásra vonatkozik-e az AGPL.** A hivatalos dokumentáció-index (`llms.txt`) nem listáz ilyen oldalt, a blogbejegyzés nem tér ki rá. **NINCS FORRÁS.**
- **Konkrét, megerősített eset arra, hogy egy korábban Community-ben elérhető funkciót utólag Enterprise-ba helyeztek volna át** (a `paradedb/discussions/3521` cím felveti a gyanút BM25-olvasásra streaming standby-okon 0.18.10→0.19.5 között, de a vita tartalmát nem sikerült elérni/elolvasni ebben a kutatásban). **NINCS FORRÁS** a tartalmi megerősítésre.
- **A ZomboDB jelenlegi pontos licence** (a `raw.githubusercontent.com/zombodb/zombodb/{master,main}/LICENSE` lekérése 404-et adott). **NINCS FORRÁS.**
- **Hivatalos, elsődleges forrás arra, hogy a ParadeDB licencpolitikája a jövőben szigorodna** (pl. AGPL → SSPL/BSL váltás terve). Nem találtam ilyet; ennek hiánya önmagában nem bizonyítja, hogy ilyen terv nincs, csak azt, hogy nyilvánosan bejelentett terv **NINCS FORRÁS** alapján.

---



---

# SQ03 — Szöveges keresés a ParadeDB-ben, különös tekintettel a magyarra

> **Módszertani megjegyzés (kötelező feltüntetés).** A `_kozos.txt` előírja az
> `anthropic-skills:deep-web-research` skill használatát. A skillt betöltöttem, de ez a
> kutatás egy már futó al-ügynök (subagent) környezetben zajlik, amelyben nincs `Agent`/`Task`
> eszköz újabb al-ügynökök indítására, és nincs interaktív felhasználó a scope-kérdések
> megválaszolására. A skill saját leírása ezt a helyzetet előre kezeli: *"If the Agent tool is
> not available — you are already running inside a subagent, or the environment doesn't expose
> it — the skill still works, degraded. Run phases 2, 5, 6 and 7 as separate sequential passes
> in your own context... Record in 00-plan.md and in the report's limitations section that the
> model separation did not happen."* Ennek megfelelően **degradált módban**, egyetlen ügynökként
> dolgoztam: nem Sonnet-kereső-ügynökök + Opus-szintéziző, hanem egyetlen folyamatos kutatási
> munkamenet, közvetlen `WebSearch`/`WebFetch`/`curl` lekérésekkel, elsődleges forrásokra
> fókuszálva. Nem építettem ki a skill teljes `.research/` bizonyítéktárát (vault, shard-index,
> automatikus linkellenőrző szkriptek); ehelyett a `_kozos.txt`-ben előírt kimeneti formátumot
> követtem, minden állításnál szó szerinti idézettel és URL-lel. A modell-szétválasztás (Sonnet
> keresés / Opus szintézis) tehát **nem** valósult meg — ezt a skill kifejezetten kéri jelezni.

## Rövid válasz

A ParadeDB `pg_search` bővítménye a `CREATE INDEX ... USING paradedb (...)` szintaxissal hoz
létre egyetlen, táblánkénti "borító" (covering) indexet — a hivatalos dokumentáció szerint
**"Only one ParadeDB index can exist per table"** —, amely egyszerre tárol szöveges (fordított
index), oszlopos (columnar) és vektoros struktúrákat; az írások a Postgres-tranzakció részeként
azonnal láthatók. A magyar nyelvhez **van hivatalos Snowball-alapú tövező** (`stemmer=hungarian`)
és kapcsolható ASCII-folding (`ascii_folding=true`); az ő/ű betűket az alapul szolgáló Tantivy
könyvtár forráskódja kifejezetten `o`, illetve `u` karakterre képezi le ASCII-foldingnál. Az
azonosítók (pl. `PROJ-4412`, `RATE_LIMIT_URL`) tokenizálása tokenizáló-függő: az alapértelmezett
`unicode_words`/`simple` tokenizáló szétvágja őket írásjeleknél, de van dedikált `literal`/
`literal_normalized` (kulcsszó-jellegű, pontos egyezés), `whitespace` (írásjeleket megtartó),
`source_code` (camelCase/snake_case-tudatos), `ngram`/`edge_ngram` (részszó/prefix) tokenizáló,
valamint `===` (term), `###` (phrase), `|||`/`&&&` (match diszjunkció/konjunkció) operátor és
`fuzzy(n)` (Levenshtein, max. távolság 2, prefix-móddal). A beépített Postgres `ts_rank`
hivatalos dokumentációja **sehol nem említi a "BM25" kifejezést**, és kifejezetten azt írja,
hogy **"The built-in ranking functions are only examples"**, és hogy nem használnak globális
(korpuszszintű) információt — ez funkcionálisan eltér a BM25 IDF-alapú számításától, de a
dokumentáció ezt nem "nem BM25" megfogalmazással mondja ki. A Postgres forráskódja
(`dict_snowball.c`) igazolja a magyar Snowball-tövező meglétét. Az SQLite FTS5 hivatalos
dokumentációja saját, valódi BM25-képletet ír le (`k1=1.2`, `b=0.75`, **fixen** a kódba égetve,
csak oszlopsúlyok állíthatók), és az `unicode61` tokenizáló alapból eltávolítja az ékezeteket,
de nyelvspecifikus (pl. magyar) tövezőt nem tartalmaz. Független (nem ParadeDB általi)
teljesítmény-összehasonlítást találtam ParadeDB vs. natív Postgres FTS között (Vineeth
Pothulapati blogja), de közvetlen, független ParadeDB-vs-SQLite-FTS5 összehasonlítást nem.

---

## 1. A `pg_search` BM25 (ParadeDB) indexe

**Verzió/dátum:** a lenti idézetek a ParadeDB hivatalos dokumentációjának 2026-09-22-i,
élő állapotából származnak (`www.paradedb.com/docs/...`). A `pg_search` bővítmény aktuális
stabil verziója a PGXN csomagregiszter szerint **0.25.9** (kiadva: 2026-09-11T17:58:47Z), a
Docker Hub `paradedb/paradedb` image ugyanezt a verziót és egy `0.26.0-rc.1` release
candidate-et is listáz (mindkettő 2026-09-11-i push).

### Létrehozás szintaxisa

```sql
CREATE INDEX search_idx ON mock_items
USING paradedb (id, description, category)
WITH (key_field='id');
```

> „`USING bm25` remains supported as a backwards-compatible alias for `USING paradedb`."
> — a 0.25.0 verziótól kezdve az index access method neve `paradedb`-re változott (a `bm25`
> visszamenőlegesen kompatibilis alias maradt).
> Forrás: [Create an Index](https://www.paradedb.com/docs/reference/indexing/create-index.md)

> „In version `0.25.0`, the BM25 index was renamed to the ParadeDB index, and `paradedb` was
> added as the index access method name. The rename reflects the fact that the index is now
> much more than BM25 scoring — it also powers vector search, aggregates, top K, and filtering."
> Forrás: uo.

### Mit indexel (oszlopok, JSON)

> „Most ordinary scalar columns can be added directly to a ParadeDB index."
> Forrás: [Create an Index](https://www.paradedb.com/docs/reference/indexing/create-index.md)

JSON/JSONB oszlopok indexelése automatikus, minden aloszlót külön szöveges mezőként kezel:

> „When indexing JSON, ParadeDB automatically indexes all sub-fields of the JSON object. The
> type of each sub-field is also inferred automatically... ParadeDB will automatically index
> both `metadata.color` and `metadata.location` as text."
> Forrás: [Indexing JSON](https://www.paradedb.com/docs/reference/indexing/indexing-json.md)

A JSON aloszlók külön-külön is konfigurálhatók saját tokenizálóval:

```sql
CREATE INDEX search_idx ON mock_items
USING paradedb (id, ((metadata->>'color')::pdb.ngram(2,3)))
WITH (key_field='id');
```
Forrás: uo.

### Kulcsmező (`key_field`)

> „Every ParadeDB index needs a `key_field`... The `key_field` must: 1. Have a `UNIQUE`
> constraint. Usually this means the table's `PRIMARY KEY`. 2. Be the first column in the
> column list. 3. Be untokenized, if it is a text field."
> Forrás: [Create an Index](https://www.paradedb.com/docs/reference/indexing/create-index.md)

### Hány index lehet egy táblán

> „Only one ParadeDB index can exist per table. We recommend indexing all columns in a table
> that may be present in a search query, including columns used for sorting, grouping,
> filtering, and aggregations."
> Forrás: [Create an Index](https://www.paradedb.com/docs/reference/indexing/create-index.md)

Ezt egy **második, független dokumentumoldal** is megerősíti (ugyanaz a kiadó, de más oldal,
más megfogalmazás, a tervezési indoklással együtt):

> „The ParadeDB index is a covering index, which means it stores all indexed columns inside a
> single index per table. This decision is intentional -- by colocating all the relevant data,
> ParadeDB optimizes for fast reads and boolean conditions. However, this means that all
> columns must be defined up front at index creation time. Adding or removing columns requires
> a `REINDEX`."
> Forrás: [Limitations & Tradeoffs](https://www.paradedb.com/docs/welcome/limitations.md)

### Lekérdező operátorok

| Operátor | Jelentés | Forrás |
|---|---|---|
| `@@@` | Általános "matchel-e a query builder függvénnyel" operátor; jobb oldalán `pdb.parse()`, `pdb.term()`, `pdb.phrase()`, `pdb.fuzzy_term()`, `pdb.range()`, `pdb.regex()`, `pdb.all()` stb. állhat | [Advanced Query Functions](https://www.paradedb.com/docs/reference/full-text/query-builder.md) |
| `\|\|\|` | Match diszjunkció (OR a tokenek között) | [Match](https://www.paradedb.com/docs/reference/full-text/match.md) |
| `&&&` | Match konjunkció (AND a tokenek között) | uo. |
| `###` | Phrase (sorrend- és pozíció-érzékeny) | [Phrase](https://www.paradedb.com/docs/reference/full-text/phrase.md) |
| `===` | Term (pontos token-egyezés, kis-nagybetű érzékeny) | [Term](https://www.paradedb.com/docs/reference/full-text/term.md) |

> „Query builder functions use the `@@@` operator. `@@@` takes a column on the left-hand side
> and a query builder function on the right-hand side. It means 'find all rows where the column
> matches the given query.'"
> Forrás: [Advanced Query Functions](https://www.paradedb.com/docs/reference/full-text/query-builder.md)

> „Match disjunction uses the `\|\|\|` operator and means 'find all documents that contain one
> or more of the terms tokenized from this text input.'" / „`&&&` means 'find all documents that
> contain all terms tokenized from this text input.'"
> Forrás: [Match](https://www.paradedb.com/docs/reference/full-text/match.md)

> „Term queries use the `===` operator... the query string is taken as-is, without any further
> tokenization or filtering."
> Forrás: [Term](https://www.paradedb.com/docs/reference/full-text/term.md)

A `pdb.parse()` a Tantivy natív lekérdezés-string szintaxisát fogadja el:

> „The parse query accepts a Tantivy query string... The intended use case is for accepting raw
> query strings provided by the end user."
> Forrás: [Query Parser](https://www.paradedb.com/docs/reference/full-text/query-parser.md)

### BM25 paraméterek (k1, b)

> „BM25 uses two parameters, `k1` and `b`, to control how term frequency and field length
> affect relevance scores. You can configure them independently for each field when creating
> an index." A táblázat szerint `k1` alapértéke `1.2` (tartomány `0`–`100`), `b` alapértéke
> `0.75` (tartomány `0`–`1`).
> Forrás: [Create an Index — BM25 Parameters](https://www.paradedb.com/docs/reference/indexing/create-index.md)

### Frissül-e tranzakción belül (írás után azonnal kereshető-e)

Három **egymástól függetlenül megfogalmazott**, de ugyanazon hivatalos dokumentáción belüli hely
mondja ki ugyanazt:

> „When a table row is inserted or updated, the ParadeDB index is immediately notified. These
> changes are recorded as part of the current transaction, ensuring that index updates are
> real-time."
> Forrás: [Architecture](https://www.paradedb.com/docs/welcome/architecture.md)

> „Incoming writes are added to a mutable segment as part of the current Postgres transaction."
> Forrás: [How the ParadeDB Index Works](https://www.paradedb.com/docs/concepts/how-the-paradedb-index-works.md)

> Az architektúra-ábra `aria-label`-je (kép-helyettesítő szöveg, tehát önálló, explicit
> mondat): „Your application connects to Postgres through SQL. Inside Postgres, your tables are
> indexed by the pg_search extension, **with index updates in the same transaction as table
> writes**."
> Forrás: [Welcome to ParadeDB](https://www.paradedb.com/docs/welcome/introduction.md)

Fontos árnyalat: a BM25 pontszámot befolyásolhatják a `VACUUM`-mal még nem takarított "halott"
sorok:

> „The scores generated by the ParadeDB index may be influenced by dead rows that have not
> been cleaned up by the `VACUUM` process. Running `VACUUM` on the underlying table will remove
> all dead rows from the index and ensures that only rows visible to the current transaction
> are factored into the BM25 score."
> Forrás: [BM25 Scoring — Score Refresh](https://www.paradedb.com/docs/reference/full-text/score.md)

Az index technikai alapja LSM-fa (log-structured merge tree), a fő függőségek:

> „The three main dependencies of `pg_search` are: pgrx — the library for writing Postgres
> extensions in Rust; Tantivy — a Rust-based full-text search library inspired by Lucene; Apache
> DataFusion — an extensible query execution framework for OLAP processing."
> Forrás: [Architecture](https://www.paradedb.com/docs/welcome/architecture.md)

Ezt a PGXN csomagmetaadat is megerősíti (**második, gépileg generált, független forrás**
ugyanahhoz az állításhoz):

> „ParadeDB pg_search is a Postgres extension that enables fast full-text, faceted and hybrid
> search over Postgres tables using the BM25 algorithm. It is built on top of Tantivy, the
> Rust-based alternative to Apache Lucene, using pgrx."
> Forrás: [pg_search @ PGXN, v0.25.9 metaadat](https://api.pgxn.org/dist/pg_search.json)

---

## 2. Tokenizálók és nyelvek

**Verzió/dátum:** ParadeDB hivatalos dokumentáció, 2026-09-22-i állapot, v0.25.9-hez tartozó
oldalak.

### Teljes tokenizáló-lista (hivatalos index)

A dokumentáció `llms.txt` indexoldala szerint az elérhető tokenizálók:

> „Unicode... Literal... Literal Normalized... Whitespace... Ngram... Edge Ngram... Simple...
> Regex Patterns... Chinese Compatible... Lindera... ICU... Jieba... Source Code"
> Forrás: [ParadeDB docs index](https://www.paradedb.com/docs/llms.txt)

Az egyes tokenizálók hivatalos leírása (mind saját aloldalról):

| Tokenizáló | Leírás (idézet) | Forrás |
|---|---|---|
| `unicode_words` (alapértelmezett) | „splits text according to word boundaries defined by the Unicode Standard Annex #29 rules. All characters are lowercased by default." | [Unicode](https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/unicode.md) |
| `simple` | „splits on any non-alphanumeric character (e.g. whitespace, punctuation, symbols). All characters are lowercased by default." | [Simple](https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/simple.md) |
| `whitespace` | „splits only on whitespace. It also lowercases characters by default." | [Whitespace](https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/whitespace.md) |
| `literal` | „applies no tokenization to the text, preserving it as-is. It is the default for `uuid` fields... useful for doing exact string matching." | [Literal](https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/literal.md) |
| `literal_normalized` | „similar to the literal tokenizer... All text is treated as a single token... unlike the literal tokenizer, this tokenizer allows token filters to be applied. By default... also lowercases the text." | [Literal Normalized](https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/literal-normalized.md) |
| `ngram(min,max)` | „splits text into 'grams,' where each 'gram' is of a certain length." | [Ngram](https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/ngrams.md) |
| `edge_ngram(min,max)` | „first splits text into words at character-class boundaries, then generates n-grams anchored to the beginning of each word." | [Edge Ngram](https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/edge-ngrams.md) |
| `regex_pattern(pattern)` | „tokenizes text using a regular expression... uses the Rust `regex` crate." | [Regex Patterns](https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/regex.md) |
| `chinese_compatible` | „like the simple tokenizer -- it lowercases non-CJK characters and splits on any non-alphanumeric character. Additionally, it treats each CJK character as its own token." | [Chinese Compatible](https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/chinese-compatible.md) |
| `lindera(chinese\|japanese\|korean)` | „uses prebuilt Chinese, Japanese, or Korean dictionaries to break text into meaningful tokens (words or phrases) rather than on individual characters. Chinese Lindera uses the CC-CEDICT dictionary, Korean Lindera uses the KoDic dictionary, and Japanese Lindera uses the IPADIC dictionary." | [Lindera](https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/lindera.md) |
| `icu` | „breaks down text according to the Unicode standard. It can be used to tokenize most languages and recognizes the nuances in word boundaries across different languages." | [ICU](https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/icu.md) |
| `jieba` | „a tokenizer for Chinese text that leverages both a dictionary and statistical models. It is generally considered to be better at identifying ambiguous Chinese word boundaries compared to... Lindera and... Chinese compatible... but the tradeoff is that it is slower." | [Jieba](https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/jieba.md) |
| `source_code` | „intended for tokenizing code. In addition to splitting on whitespace, punctuation, and symbols, it also splits on common casing conventions like camel case and snake case." | [Source Code](https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/source-code.md) |

### Magyar: van-e tövező (stemmer)?

**Igen.** A `pdb.simple('stemmer=hungarian')` (vagy bármely más tokenizáló + `stemmer=`
argumentum) formában kapcsolható:

> „Stemmers in ParadeDB are based on stemming algorithms obtained from the official Snowball
> website... Valid languages are `arabic`, `czech`, `danish`, `dutch`, `english`, `finnish`,
> `french`, `german`, `greek`, `hungarian`, `italian`, `norwegian`, `polish`, `portuguese`,
> `romanian`, `russian`, `spanish`, `swedish`, `tamil`, and `turkish`."
> Forrás: [Stemmer](https://www.paradedb.com/docs/reference/token-filters/stemming.md)
> (**20 nyelv**, benne magyarral)

**Két független megerősítés** ugyanerre az állításra:

1. A hivatkozott hivatalos upstream projekt, a Snowball (`snowballstem.org`) saját algoritmus-
   listája külön-külön felsorolja: „Czech", „Polish", „Arabic", „Hungarian" mint önálló
   stemming-algoritmusokat.
   Forrás: [snowballstem.org/algorithms](https://snowballstem.org/algorithms/)
2. A Rust `rust-stemmers` csomag (amelyet a Rust ökoszisztémában tipikusan Snowball-tövezők
   elérésére használnak) `Algorithm` enumja is tartalmazza a „Hungarian" variánst, a többi 17
   nyelv mellett.
   Forrás: [docs.rs/rust-stemmers 1.2.0, `Algorithm` enum](https://docs.rs/rust-stemmers/latest/rust_stemmers/enum.Algorithm.html)
   — **Megjegyzés (lásd Ellentmondások):** ez a konkrét crate-verzió csak 18 nyelvet listáz
   (nincs benne Czech és Polish), tehát a pg_search stemmelője nem feltétlenül pontosan ezt a
   crate-et/verziót használja — de a magyar mindkettőben szerepel.

### Van-e ékezet-lehagyás (ASCII folding)?

**Igen, kapcsolható**, de nem alapértelmezett:

> „The ASCII folding filter strips away diacritical marks (accents, umlauts, tildes, etc.)
> while leaving the base character intact. It is supported for all tokenizers besides the
> literal tokenizer. To enable, append `ascii_folding=true` to the tokenizer's arguments."
>
> Példa: `SELECT 'Café naïve coöperate'::pdb.simple('ascii_folding=true')::text[];` →
> `{cafe,naive,cooperate}`
> Forrás: [ASCII Folding](https://www.paradedb.com/docs/reference/token-filters/ascii-folding.md)

### Hogyan kezeli az ő, ű betűket?

A hivatalos pg_search-dokumentáció **nem ad külön, magyar-specifikus példát** az `ascii_folding`
viselkedésére ő/ű esetén (csak a fenti café/naïve/coöperate példát). Mivel a ParadeDB
architektúra-dokumentációja szerint a Tantivy a szövegfeldolgozás alapkönyvtára, megnéztem a
Tantivy saját forráskódját (**T1, elsődleges forrás, más karbantartók**, mint a ParadeDB):

> Tantivy `AsciiFoldingFilter` forráskódja (`ascii_folding_filter.rs`, `tantivy` crate v0.26.2,
> a docs.rs "latest" build-je 2026-09-22-én): a `match` blokkban szó szerint szerepel:
> ```
> '\u{0150}' | // Ő  [LATIN CAPITAL LETTER O WITH DOUBLE ACUTE]
> ...
> '\u{0151}' | // ő  [LATIN SMALL LETTER O WITH DOUBLE ACUTE]
> ...
> => Some("o"),
> ```
> és hasonlóan `'\u{0170}'` (Ű) / `'\u{0171}'` (ű) → `"u"` ágban.
> Forrás: [docs.rs/tantivy — src/tantivy/tokenizer/ascii_folding_filter.rs.html](https://docs.rs/tantivy/latest/src/tantivy/tokenizer/ascii_folding_filter.rs.html)

**Fontos korlát:** ez azt igazolja, hogy *a Tantivy könyvtár* explicit módon `o`-ra, ill.
`u`-ra képezi le az ő/ű karaktereket az ASCII-foldingnál. Azt, hogy a pg_search konkrétan ezt a
Tantivy-osztályt hívja-e az `ascii_folding=true` opciónál (nem egy saját implementációt), a
pg_search saját forráskódjából **nem tudtam közvetlenül ellenőrizni**, mert a
`github.com/paradedb/paradedb` repóhoz ebben a kutatási környezetben nincs hozzáférés (lásd
lent, "Amire NINCS forrás"). Ez tehát erős közvetett bizonyíték, nem közvetlen megerősítés.

### CJK: Lindera, jieba, ICU — mi érhető el ténylegesen?

A dokumentáció szerint mindhárom (és a `chinese_compatible` is) **dokumentált, használatra kész
tokenizálóként** szerepel a jelenlegi (0.25.9) referencia-dokumentációban, build-flag-említés
nélkül (lásd fenti táblázat). Egy **korábbi** verzió (0.15.13) hivatalos README-je viszont
kifejezetten megemlítette, hogy az ICU tokenizáló natív/rendszerfüggőséget (`libicu`) igényel,
és fejlesztői build esetén explicit Cargo feature-flaget:

> „Our prebuilt binaries come with the ICU tokenizer enabled, which requires the `libicu`
> library... Or, you can compile the extension from source without `--features icu` to build
> without the ICU tokenizer." / „The ICU tokenizer, which enables tokenization for Arabic,
> Amharic, Czech and Greek, is not enabled by default in development due to the additional
> dependencies it requires... to enable the ICU tokenizer in development, pass `--features icu`
> to the `cargo pgrx run` and `cargo pgrx test` commands."
> Forrás: [pg_search README @ PGXN, v0.15.13](https://api.pgxn.org/src/pg_search/pg_search-0.15.13/pg_search/README.md)

A jelenlegi (0.25.9) README **rövidebb** és **nem tér ki** tokenizáló-specifikus build-
flagekre; a hivatalos self-hosted telepítési útmutató sem említ ilyet:

> „Install the `pg_search` extension, which powers ParadeDB's search features." (nincs
> tokenizáló-specifikus feature-flag megjegyzés)
> Forrás: [Extension (self-hosted telepítés)](https://www.paradedb.com/docs/operate/deploy/self-hosted/extension.md)

**Ez tehát nyitott kérdés:** nem sikerült egyértelműen megerősítenem, hogy a jelenlegi (0.25.9)
előre buildelt (Docker/csomag) binárisokban a Lindera és a Jieba tokenizáló alapból, mindenféle
extra kapcsoló nélkül elérhető-e, vagy — mint korábban az ICU esetén — külön compile-time
feature-flaget igényelnek forrásból építésnél. Lásd "Amire NINCS forrás".

### Egy indexen belül lehet-e több nyelv?

**Igen, kétféleképpen is:**

1. **Oszloponként eltérő tokenizáló/nyelv** — a `CREATE INDEX` minden oszlopot külön
   castolhat saját tokenizálóra:
   ```sql
   CREATE INDEX search_idx ON mock_items
   USING paradedb (id, (description::pdb.icu), category)
   WITH (key_field='id');
   ```
   Forrás: [Create an Index](https://www.paradedb.com/docs/reference/indexing/create-index.md)

2. **Ugyanaz az oszlop többféleképp is tokenizálható**, alias-szal megkülönböztetve (pl. egy
   mező egyszerre `literal` és `simple('stemmer=hungarian')` tokenizálású is lehet):
   > „In many cases, a text field needs to be tokenized multiple ways... To tokenize a field in
   > more than one way, append an `alias=<alias_name>` argument to the additional tokenizer
   > configurations... two distinct fields are created in the index."
   > Forrás: [Multiple Tokenizers Per Field](https://www.paradedb.com/docs/reference/tokenizers/multiple-per-field.md)

---

## 3. Azonosítók és kódrészletek tokenizálása

A hivatalos dokumentáció nem ad kifejezett, kész példát pontosan a `PROJ-4412`,
`RATE_LIMIT_URL`, `ECONNREFUSED` és `bun run release` sztringekre, de a **dokumentált
tokenizáló-szabályokból közvetlenül levezethető**, mi történne velük — ezt lentebb minden
esetben jelzem, ha levezetés, nem közvetlen dokumentált példa.

| Bemenet | `unicode_words`/`simple` (alapértelmezett) | `whitespace` | `source_code` | `literal`/`literal_normalized` |
|---|---|---|---|---|
| `PROJ-4412` | „splits on any non-alphanumeric character" → két token: `proj`, `4412` (a kötőjel nem alfanumerikus) *(levezetve)* | „splits only on whitespace" → **egy** token: `proj-4412` (a kötőjel megmarad, mert nem szóköz) *(levezetve)* | „splits on whitespace, punctuation, and symbols" → a kötőjel írásjel, így valószínűleg szintén `proj`, `4412` *(levezetve — nincs pontosan erre a mintára hivatalos példa)* | egész mezőérték = 1 token (csak akkor hasznos, ha a mező *csak* az azonosítót tartalmazza) |
| `RATE_LIMIT_URL` | alulvonás nem alfanumerikus → `rate`, `limit`, `url` *(levezetve a „splits on any non-alphanumeric character" szabályból)* | egy token: `rate_limit_url` *(levezetve)* | dokumentált példa **hasonló** mintára: „`my_variable`... would get split into `my` and `variable`" → itt: `rate`, `limit`, `url` | egész mező = 1 token |
| `ECONNREFUSED` | egy token: `econnrefused` (nincs elválasztó karakter, csak kisbetűsítés történik) *(levezetve)* | egy token: `econnrefused` | egy token: `econnrefused` (nincs camelCase-váltás, mert az egész csupa nagybetű) *(levezetve)* | egész mező = 1 token |
| `bun run release` | 3 token: `bun`, `run`, `release` (szóközök mentén, ez triviális minden tokenizálónál) | 3 token: `bun`, `run`, `release` | 3 token: `bun`, `run`, `release` | egész mező = 1 token (`bun run release`) |

Forrásidézetek a fenti szabályokhoz:
- „The simple tokenizer splits on any non-alphanumeric character (e.g. whitespace, punctuation,
  symbols)." — [Simple](https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/simple.md)
- „The whitespace tokenizer splits only on whitespace." — [Whitespace](https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/whitespace.md)
- „The source code tokenizer is intended for tokenizing code. In addition to splitting on
  whitespace, punctuation, and symbols, it also splits on common casing conventions like camel
  case and snake case. For instance, text like `my_variable` or `myVariable` would get split
  into `my` and `variable`." — [Source Code](https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/source-code.md)
- „The literal tokenizer applies no tokenization to the text, preserving it as-is... useful for
  doing exact string matching over text fields." — [Literal](https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/literal.md)

### Van-e pontos-egyezés/kulcsszó mező?

**Igen** — a `literal` (case-sensitive, semmilyen token filter nem alkalmazható rá) és a
`literal_normalized` (kisbetűsít, de token filtert enged, és oszlopos tárolásra is alkalmas
`Top K`/aggregátumokhoz) tokenizáló pontosan ezt a célt szolgálja:

> „Text fields used as a sort field in a Top K query, or as part of an aggregate, must use
> either this tokenizer or `literal_normalized`."
> Forrás: [Literal](https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/literal.md)

### Frázis-keresés

**Igen**, a `###` operátorral, sorrend- és pozíció-érzékenyen:

> „Phrase queries work exactly like match conjunction..., but are more strict in that they
> require the order and position of tokens to be the same." Emellett `slop(n)` argumentummal
> lazítható a sorrendkövetelmény.
> Forrás: [Phrase](https://www.paradedb.com/docs/reference/full-text/phrase.md)

### Prefix keresés

Nincs önálló "prefix" query-builder függvény, de két mechanizmus is megvalósítja:

1. **`fuzzy(n, true)`** — a második argumentum `true`/`t` értéke a query stringet prefixként
   kezeli (0 távolsággal = pontos prefix):
   > „`fuzzy` also supports prefix matching... To treat the query string as a prefix, set the
   > second argument of `fuzzy` to either `t` or `'true'`."
   > Forrás: [Fuzzy](https://www.paradedb.com/docs/reference/full-text/fuzzy.md)
2. **`edge_ngram(min,max)`** tokenizáló — indexidejű prefix-generálás "search-as-you-type"
   célra: „generates n-grams anchored to the **beginning** of each word."
   Forrás: [Edge Ngram](https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/edge-ngrams.md)

### Fuzzy (Levenshtein) keresés

**Igen**, `match`/`term` lekérdezésekre alkalmazható `::pdb.fuzzy(n)` cast formában:

> „When a query is cast to `fuzzy(n)`, this requirement is relaxed -- tokens are matched if
> their Levenshtein distance, or edit distance, is less than or equal to `n`."... „For
> performance reasons, the maximum allowed edit distance is `2`." A transzpozíció (két
> szomszédos karakter felcserélése) alapból 2 költségű, `transposition_cost_one=true`-val 1-re
> csökkenthető.
> Forrás: [Fuzzy](https://www.paradedb.com/docs/reference/full-text/fuzzy.md)

Figyelmeztetés nem-latin (pl. CJK) karakterekre:

> „While fuzzy matching will work for non-Latin characters (Chinese, Japanese, Korean, etc.),
> it may not give expected results (with large result sets returned) as Levenshtein distance
> relies on individual character difference."
> Forrás: uo.

### Részszó (n-gram) keresés

**Igen**, két tokenizáló is: `ngram(min,max)` (a szó eleji és belseji részszavakra is illeszkedő,
szabad hosszúságú n-gram) és `edge_ngram(min,max)` (csak szóprefixekre). Az `ngram`-nál
`positions=true`-val (csak akkor, ha `min==max`) pontos részsztring-egyezés is elérhető
`###` frázis-lekérdezéssel:

> „With `positions=true`, phrase queries over ngram fields perform exact substring matching...
> A phrase query uses a single positional intersection instead [of `Must` clause per token]."
> Forrás: [Ngram](https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/ngrams.md)

---

## 4. Összevetés a Postgres beépített szöveges keresésével (`tsvector`/`tsquery`)

**Verzió/dátum:** PostgreSQL hivatalos dokumentáció, "current" ág = PostgreSQL 18-hoz tartozó
oldalak; a dokumentáció fejléce szerint a legutóbbi kiadási dátum „August 13, 2026: PostgreSQL
18.6, 17.11, 16.15, 15.19...". Lekérve: 2026-09-22.

### Van-e magyar snowball szótár?

**A jelenlegi hivatalos PostgreSQL-dokumentáció (12.6. Dictionaries és 12.1. Introduction
fejezetek, `postgresql.org/docs/current/`) NEM sorolja fel név szerint a beépített Snowball-
nyelveket** — csak egy angol példát mutat be (`CREATE TEXT SEARCH DICTIONARY english_stem
(TEMPLATE = snowball, Language = english, ...)`), és általánosságban ír „predefined
dictionaries for many languages"-ről. Ez saját magában nem bizonyítja vagy cáfolja a magyar
elérhetőségét, ezért a forráskódhoz fordultam (**T1, elsődleges, más jellegű forrás**):

> A PostgreSQL forráskódjának `src/backend/snowball/dict_snowball.c` fájljában (a hivatalos
> Doxygen-alapú forráskód-böngészőben) szó szerint szerepel:
> ```
> #include "snowball/libstemmer/stem_ISO_8859_2_hungarian.h"
> ...
> #include "snowball/libstemmer/stem_UTF_8_hungarian.h"
> ...
> STEMMER_MODULE(hungarian, PG_LATIN2, ISO_8859_2),
> ...
> STEMMER_MODULE(hungarian, PG_UTF8, UTF_8),
> ```
> Forrás: [doxygen.postgresql.org — dict_snowball.c forráskód](https://doxygen.postgresql.org/dict__snowball_8c_source.html)

Ez **közvetlenül igazolja**, hogy a Postgres beépített (`contrib`-en kívüli, `pg_catalog`-beli)
Snowball-implementációja tartalmaz magyar tövezőt (`hungarian_stem` konfigurációként érhető el
`CREATE TEXT SEARCH DICTIONARY ... (TEMPLATE = snowball, Language = hungarian)` formában, a fenti
angol példa mintájára — ez utóbbi konkrét SQL-példa a magyarra nem szerepel a dokban, de a
sablon és a forráskódban talált nyelvmodul együtt egyértelműen ezt teszi lehetővé).

### Mit mond a hivatalos Postgres-dokumentáció a `ts_rank`-ről (BM25 vs. ts_rank)

**Fontos, pontosított megállapítás:** a hivatalos PostgreSQL-dokumentáció "Ranking Search
Results" (12.3.3) fejezete **egyszer sem használja a "BM25" kifejezést** — sem "nem BM25",
sem semmilyen más formában. Ez ellentétben áll a kutatási kérdés megfogalmazásának
feltételezésével ("A hivatalos Postgres-dokumentáció szerint a ts_rank nem BM25"); a
dokumentáció nem tesz explicit összehasonlítást a BM25-tel, ezért ilyen szó szerinti idézet
**nem létezik**. Amit a dokumentáció ehelyett kimond, az a `ts_rank`/`ts_rank_cd` funkciók
korlátozott, "csak példa" jellegéről és a globális (korpuszszintű) statisztika hiányáról szól:

> „Ranking attempts to measure how relevant documents are to a particular query... However, the
> concept of relevancy is vague and very application-specific. Different applications might
> require additional information for ranking, e.g., document modification time. **The built-in
> ranking functions are only examples.** You can write your own ranking functions and/or
> combine their results with additional factors to fit your specific needs."
> Forrás: [12.3.3. Ranking Search Results](https://www.postgresql.org/docs/current/textsearch-controls.html)

> „It is important to note that **the ranking functions do not use any global information**, so
> it is impossible to produce a fair normalization to 1% or 100% as sometimes desired."
> Forrás: uo.

A BM25-képlet (lásd lentebb, SQLite FTS5 hivatalos leírásában) definíció szerint tartalmaz egy
korpuszszintű **IDF** (inverse document frequency) tagot, amely az adott terminust tartalmazó
dokumentumok arányából számol — ez az, amit a Postgres saját dokumentációja szerint a
`ts_rank`/`ts_rank_cd` **nem** használ ("do not use any global information"). Ez **funkcionális,
nem szó szerinti** bizonyíték arra, hogy a `ts_rank` nem BM25-algoritmus.

Független (nem ParadeDB, nem Postgres-projekt) T2/T3 források **expliciten** kimondják a
különbséget, bár nem idézik a Postgres-dokumentációt "nem BM25" megfogalmazással:

> „Postgres uses term frequency without the saturation function. It either allows users to rank
> documents purely based on the term frequency (`ts_rank`) or based on the term frequency and
> the distance between the query terms" — és a szerző Postgres megközelítését „simpler and less
> powerful than BM25"-nek nevezi.
> Forrás: Evan Schwartz, [Comparing full text search algorithms: BM25, TF-IDF, and Postgres](https://emschwartz.me/comparing-full-text-search-algorithms-bm25-tf-idf-and-postgres/) (2024-11-19, független technikai blog, T2)

> „Postgres FTS does not do *all* of the things a purpose-built search engine can do, but
> Postgres can produce very good results with decent performance." — a hiányzó képességek közt:
> „Lemmatization and stemming... Advanced result ranking configuration... Edit distance
> matching..."
> Forrás: Supabase blog, [Postgres Full Text Search vs the rest](https://supabase.com/blog/postgres-full-text-search-vs-the-rest) (2022-10, független, ParadeDB-hez nem köthető, T2/T3)

### Mit ad a ParadeDB, amit a beépített Postgres FTS nem?

A ParadeDB saját dokumentációja (**T2, gyártói forrás**) szerint:

> „ParadeDB accelerates these queries inside Postgres with a custom index... You've outgrown
> Postgres full-text search or pgvector and are frustrated with performance bottlenecks, missing
> features, or a clunky developer experience."
> Forrás: [Welcome to ParadeDB](https://www.paradedb.com/docs/welcome/introduction.md)

Ezt két, ParadeDB-től **független** T2 forrás is alátámasztja konkrét mérésekkel, illetve
funkciólistával:

> Vineeth Pothulapati (független blog, 2025-08-15, 1,6M Amazon-termék adathalmazon mérve):
> teljes szöveges keresésnél „ParadeDB 4.4x faster (92ms vs 401ms)", fuzzy keresésnél „164x
> faster (139ms vs 22,838ms)", mezőspecifikus keresésnél „48x faster (90ms vs 4,399ms)";
> ugyanakkor pontos frázis-keresésnél „PostgreSQL 14x faster (6ms vs 89ms)", és egyedi
> beszúrásoknál is a natív Postgres volt gyorsabb. A szerző szó szerint: „For search workloads,
> ParadeDB destroys PostgreSQL", de „PostgreSQL remains superior for single-row transactional
> operations and exact phrase matching."
> Forrás: [vineeth.fyi — PostgreSQL vs ParadeDB: A Search Comparison](https://www.vineeth.fyi/blog/pg-vs-pg-search/)

> Rishi Raj Jain / Neon (Postgres-felhőszolgáltató, nem ParadeDB, de üzleti partnerségben áll a
> ParadeDB-vel, ezért csak részben független — **T3**): a natív `tsvector` „limited relevance
> ranking"-gel rendelkezik és nem kezel jól „complex queries like fuzzy matching or phrase
> proximity"-t; a `pg_search` „BM25 ranking"-et és „typo tolerance"-t ad hozzá.
> Forrás: [dev.to/neon-postgres — Comparing Text Search Strategies](https://dev.to/neon-postgres/comparing-text-search-strategies-pgsearch-vs-tsvector-vs-external-engines-54f0) (2025-05-08, szerkesztve 2025-06-23)

**A ParadeDB saját (T2, gyártói) benchmarkja** — ahogy a módszertan kéri, itt T2-ként kezelve,
és a fentiekkel (Vineeth Pothulapati, Neon) igyekeztem alátámasztani — a
[„Same Query, Three Results" blogbejegyzésben](https://www.paradedb.com/blog/benchmarker-iteration)
és a [ParadeDB vs. PostgreSQL összehasonlító oldalon](https://www.paradedb.com/vs/postgresql)
érhető el; ezeket nem dolgoztam fel részletesen idézetszinten, mivel a kérdés kifejezetten
független forrást kért elsődlegesnek, és a fenti két független forrás (Pothulapati, illetve
részben Neon) már lefedi a lényegi állítást (ParadeDB gyorsabb tipikus szöveges keresési
workloadokon, cserébe egyedi tranzakciós írásoknál és pontos frázis-keresésnél a natív Postgres
verhet gyorsabb lehet).

Egy **harmadik, versenytárs által készített**, de nyílt forráskódú módszertannal közölt
benchmark (SereneDB, T2/T3, saját érdekeltséggel, mivel konkurens terméket kínál) 2026-09-07-i
dátummal 1 milliárd sornyi OpenTelemetry-log adaton, natív Postgres 18, ParadeDB (pg_search) és
TigerData (pg_textsearch) összevetésével:

> 1 milliárd sornál, medián válaszidő: SereneDB 35,5 ms (92/92 lekérdezés lefutott), ParadeDB
> 413,0 ms (77/92 lefutott), TigerData és natív Postgres 60 másodperces timeout-limitbe
> ütközött a lekérdezések nagy részénél (TigerData 33/92, Postgres csak 12/92 futott le).
> „Postgres: `to_tsvector('simple', body)` with GIN; uses `ts_rank_cd` (not BM25)."
> Forrás: [serenedb.com/blog/searchbench-postgres](https://serenedb.com/blog/searchbench-postgres) — nyílt forráskódú benchmark-kód: `github.com/serenedb/searchbench`

---

## 5. Összevetés az SQLite FTS5-tel (`unicode61`, `bm25()`)

**Verzió/dátum:** a hivatalos SQLite FTS5-dokumentáció (`sqlite.org/fts5.html`) élő állapota,
lekérve 2026-09-22-én; a `sqlite.org/download.html` szerint az aktuális stabil SQLite-verzió
ekkor **3.53.4**.

### `unicode61` tokenizáló

> „The unicode tokenizer classifies all unicode characters as either 'separator' or 'token'
> characters. By default all space and punctuation characters, as defined by Unicode 6.1, are
> considered separators... By default, diacritics are removed from all Latin script characters.
> This means, for example, that 'A', 'a', 'À', 'à', 'Â' and 'â' are all considered to be
> equivalent."
> Forrás: [SQLite FTS5 Extension — 4.3.1. Unicode61 Tokenizer](https://sqlite.org/fts5.html)

Az ékezet-eltávolítás (`remove_diacritics`) kapcsolható (`0`/`1`/`2`, alapértelmezett `1`):

> „This option should be set to '0', '1' or '2'. The default value is '1'... if it is set to
> '1', then diacritics are not removed in the fairly uncommon case where a single unicode
> codepoint is used to represent a character with more that one diacritic... This is technically
> a bug... If this option is set to '2', then diacritics are correctly removed from all Latin
> characters."
> Forrás: uo.

Ez alátámasztja a `_kozos.txt`-ben leírt jelenlegi tervet (`unicode61 remove_diacritics 2`).

**Nyelvspecifikus tövező FTS5-ben nincs magyarhoz** — az FTS5 négy beépített tokenizálója
(`unicode61`, `ascii`, `porter`, `trigram`) közül csak a `porter` végez tövezést, és az is
kizárólag angolra:

> „FTS5 features four built-in tokenizer modules... The porter tokenizer, which implements the
> porter stemming algorithm... The porter stemmer algorithm is designed for use with English
> language terms only - using it with other languages may or may not improve search utility."
> Forrás: [SQLite FTS5 Extension — 4.3.3. Porter Tokenizer](https://sqlite.org/fts5.html)

Ez megegyezik a `_kozos.txt` kiinduló feltevésével ("tövező nélkül").

### `bm25()` függvény

Az FTS5 saját, valódi BM25-implementációt tartalmaz, **fix** `k1`/`b` konstansokkal:

> „The built-in auxiliary function `bm25()` returns a real value indicating how well the current
> row matches the full-text query. The better the match, the numerically smaller the value
> returned... `k1` and `b` are both constants, hard-coded at `1.2` and `0.75` respectively."
> Forrás: [SQLite FTS5 Extension — 5.1.1. The bm25() function](https://sqlite.org/fts5.html)

> „The '-1' term at the start of the formula is not found in most implementations of the BM25
> algorithm... the FTS5 implementation of BM25 multiplies the result by -1 before returning it,
> ensuring that better matches are assigned numerically lower scores."
> Forrás: uo.

Csak **oszlopsúlyok** (nem `k1`/`b`) állíthatók lekérdezés-időben:

> „by passing extra real value arguments to the `bm25()` SQL function, each column of the table
> may be assigned a different weight... The first argument passed to `bm25()` following the
> table name is the weight assigned to the leftmost column..."
> Forrás: uo.

**Ellentét a ParadeDB-vel:** a ParadeDB `k1`/`b` paraméterei indexdefiníció-időben,
mezőnként konfigurálhatók (lásd 1. szakasz), míg az FTS5-ben `k1`/`b` fixen a kódba van égetve,
csak az oszlopsúlyok módosíthatók lekérdezés-időben.

### Prefix, phrase, NEAR, fuzzy

> „`3.3. FTS5 Prefix Queries` ... a token extracted from the string is marked as a prefix token.
> As you might expect, a prefix token matches any document token of which it is a prefix."
> Forrás: [SQLite FTS5 Extension](https://sqlite.org/fts5.html)

> „Two or more phrases may be grouped into a NEAR group... `NEAR('one two' 'three four', 10)`
> ... If no N parameter is supplied, it defaults to 10."
> Forrás: uo.

**Fuzzy/Levenshtein keresés az FTS5 hivatalos dokumentációjában sehol nem szerepel** — a
„fuzzy", „levenshtein" és „edit distance" kifejezések egyike sem fordul elő a teljes
`fts5.html` oldalon (ellenőrizve). Ez megerősíti, hogy az FTS5-nek nincs beépített fuzzy
keresése (ellentétben a ParadeDB `fuzzy(n)`-jével).

**Részszó/n-gram keresés** az FTS5-ben a `trigram` tokenizálóval érhető el, de az **fix,
3 karakteres** ablakmérettel (a ParadeDB `ngram(min,max)`-jával szemben, amely tetszőleges
mérettartományt enged):

> „The trigram tokenizer extends FTS5 to support substring matching in general, instead of the
> usual token matching... treats each contiguous sequence of three characters as a token."
> Forrás: uo.

### Van-e független összehasonlítás?

**Nem találtam szigorú, mérőszámokkal alátámasztott, FTS5-öt közvetlenül más motorral (BM25-
minőség vagy sebesség szempontjából) összevető, ParadeDB-től és a SQLite-projekttől egyaránt
független forrást.** Amit találtam, az inkább minőségi/kritikai jellegű, versenytárs
(Turso, a SQLite-ra épülő TursoDB gyártója) által írt bejegyzés:

> „SQLite's FTS5 extension is also full of caveats and shortcomings."
> Forrás: Preston Thorpe / Turso, [Beyond FTS5: Building Transactional Full-Text Search in TursoDB](https://turso.tech/blog/beyond-fts5) (2026-01-27) — **T3**, mert a Turso saját, FTS5-öt helyettesítő terméket (Tantivy-alapú) reklámoz, konkrét benchmark-számot nem közöl.

Közvetlen **ParadeDB vs. SQLite FTS5** összehasonlítást (sem független, sem gyártói forrásból)
**nem találtam** — ez érthető, mivel a két rendszer eltérő platformra épül (Postgres-kiterjesztés
vs. beágyazott motor), így nincs tipikus "versus" tartalom róluk.

---

## Ellentmondások

1. **A kutatási kérdés feltevése vs. a talált elsődleges forrás.** A feladat azt kérte:
   „A hivatalos Postgres-dokumentáció szerint a ts_rank nem BM25 – idézd." A hivatalos
   PostgreSQL-dokumentáció (`textsearch-controls.html`, 12.3.3. fejezet) **sehol nem használja
   a "BM25" szót**, tehát ilyen szó szerinti kijelentés nem létezik benne. A dokumentáció
   helyette a `ts_rank`/`ts_rank_cd` korlátozott, "csak példa" jellegét és a globális
   (korpuszszintű) statisztika hiányát mondja ki — ez tartalmilag konzisztens a BM25-től való
   eltéréssel, de nem azonos állítás. Nem simítottam el: a fenti 4. szakaszban mindkét szintet
   (közvetlen hiány / közvetett funkcionális bizonyíték) külön jelöltem.

2. **A magyar Snowball-nyelvlista mérete a ParadeDB dokumentáció és a `rust-stemmers` Rust
   crate között eltér.** A ParadeDB hivatalos `stemming.md` oldala 20 nyelvet sorol fel
   (beleértve `czech`-et és `polish`-t is). A `rust-stemmers` v1.2.0 crate `Algorithm` enumja
   csak 18 variánst listáz, **Czech és Polish nélkül** — tehát vagy nem ez a konkrét crate/
   verzió áll a pg_search stemmelője mögött, vagy egy újabb/eltérő verziót/binding-ot használ.
   A magyar mindkét listában szerepel, ez az állítás nem kérdéses; az eltérés csak a lista
   teljes hosszát/összetételét érinti, és jelzi, hogy a pg_search Snowball-integrációjának
   pontos alsó rétegét (melyik konkrét Rust-csomagot/verziót) nem sikerült 100%-osan
   azonosítani a pg_search saját forráskódja nélkül.

3. **Egy index vs. "hány index lehet egy táblán" kérdés lehetséges félreértése.** A kutatási
   kérdés megfogalmazása ("hány ilyen index lehet egy táblán") nyitva hagyta a lehetőségét,
   hogy több BM25-index is létezhet egy táblán (mint pl. a Postgres GIN-indexeknél). A
   hivatalos dokumentáció ezt egyértelműen kizárja ("Only one ParadeDB index can exist per
   table"), és ezt két különböző hivatalos dokumentum-oldal is megerősíti (lásd 1. szakasz) —
   nincs itt tényleges forrásellentmondás, csak a kérdésfeltevés és a valóság közötti eltérést
   emelem ki.

---

## Amire NINCS forrás

- **A pg_search saját (nem Tantivy-, hanem konkrétan a pg_search Rust-kódjában lévő)
  implementációja** az `ascii_folding` és `stemmer` token filterekhez — a
  `github.com/paradedb/paradedb` repóhoz ebben a kutatási környezetben nincs hozzáférés
  (a proxy explicit hibaüzenete: „GitHub access to this repository is not enabled for this
  session"), így nem tudtam közvetlenül igazolni, hogy a pg_search ténylegesen a fentebb
  idézett Tantivy `AsciiFoldingFilter`-t hívja-e, vagy attól eltérő saját kódot használ.
- **Hogy a Lindera és a Jieba CJK-tokenizáló a jelenlegi (0.25.9) előre buildelt ParadeDB
  Docker-image/csomagokban alapból, kapcsoló nélkül elérhető-e**, vagy — az ICU 0.15.13-as
  README-jében dokumentált mintához hasonlóan — külön compile-time feature-flaget igényel
  forrásból építésnél. A jelenlegi dokumentáció erről nem nyilatkozik explicit módon.
  NINCS FORRÁS.
- **Konkrét, hivatalos SQL-példa arra, hogy `CREATE TEXT SEARCH DICTIONARY hungarian_stem
  (TEMPLATE = snowball, Language = hungarian, ...)`** ténylegesen szerepel-e a PostgreSQL
  dokumentációjában — nem találtam ilyen konkrét, magyar nyelvre vonatkozó SQL-példát a
  hivatalos dokumentációban (csak az angol mintapélda van dokumentálva); a magyar elérhetőségét
  kizárólag a forráskód (`dict_snowball.c`) igazolja, SQL-szintű hivatalos példa nélkül.
  NINCS FORRÁS (dokumentációs szintű SQL-példára).
- **Van-e a PostgreSQL disztribúcióban ténylegesen telepített `hungarian.stop` stopword-fájl**
  (a `share/tsearch_data/` alatt) — ezt nem ellenőriztem közvetlenül (pl. forráskód-repó
  fájllistázásával), csak a stemmer-modul meglétét. NINCS FORRÁS.
- **Szigorú, mérőszámokkal dokumentált, ParadeDB-től és a SQLite-projekttől egyaránt független
  benchmark vagy minőségi tanulmány, amely kifejezetten az SQLite FTS5 `bm25()`-öt más
  motorokkal (Lucene/Tantivy/Postgres) veti össze** — csak minőségi, benchmark-szám nélküli
  kritikai megjegyzést találtam (Turso blog), és közvetlen ParadeDB-vs-SQLite-FTS5
  összehasonlítást egyáltalán nem találtam. NINCS FORRÁS.
- **A ParadeDB saját benchmark-módszertanának (`benchmarker-iteration` blog, `paradedb/
  benchmarks` GitHub-mappa) részletes, idézetszintű feldolgozása** — a GitHub-repóhoz való
  hozzáférés hiánya, illetve a kutatási idő-/terjedelemkorlát miatt ezt csak érintőlegesen,
  T2-ként jelöltem, nem dolgoztam fel tételesen.

---



---

# SQ04 — Vektoros és hibrid keresés, jogosultsági szűréssel

> **Módszertani megjegyzés (kötelező bejegyzés a `_kozos.txt` szerint):** ehhez a feladathoz nem indítottam el a `anthropic-skills:deep-web-research` skill teljes, több-ügynökös fan-out pipeline-ját. A skill saját kimenete (`.research/` evidence-vault + önálló szintézis-riport formátum) nem illeszkedik ahhoz, hogy a kötelező kimenet egyetlen, a `_kozos.txt`-ben előírt fix szerkezetű `sq04.md` fájl legyen, és ebben a futtatási környezetben nincs elérhető önálló "Agent" eszköz további keresőalügynökök indítására. Ezért a `_kozos.txt` "degradált mód" utasítása szerint jártam el: egyetlen szálon, magam végeztem a forráskutatást (`WebSearch`, `WebFetch`, valamint `curl` a nyers HTML/JSON/forráskód közvetlen lekéréséhez — a ParadeDB dokumentációs oldalai React Server Components streaming-formátumban szolgálják ki a tartalmat, ezért a tényleges szöveget a `self.__next_f.push([...])` szkript-darabokból, szó szerinti idézetek szintjén, kézzel kellett kibontanom), és követtem a forrásmegbízhatósági elveket (elsődleges forrás előny, szó szerinti idézet + URL minden állításhoz, kétforrásos megerősítés, ellentmondások kiírása, verzió+dátum minden számnál).

## Rövid válasz

A ParadeDB **nem** a `pgvector` HNSW/IVFFlat indexére épít vektoros keresésre: a `pg_search` kiterjesztés a `0.25.0` kiadás (2026 nyara) óta egy **saját, SPANN-stílusú vektorindexet** épít a ParadeDB-indexen belül, és a `pgvector`-t kizárólag a `vector` **adattípus** és a távolság-operátorok (`<->`, `<=>`, `<#>`) miatt kényszeríti ki függőségként — ez négy, egymástól független elsődleges forrásból (docs.paradedb.com, GitHub `pg_search/README.md`, GitHub-alapú kiadási napló, és a hivatalos Docker-image build-fájljai) is szó szerint megerősíthető. A hivatalos `paradedb/paradedb` Docker image-ben (stabil `v0.25.9`, 2026-09-11) a `pgvector` **0.8.4** van APT-csomagként rögzítve minden támogatott PG-verzióhoz (15–18); a következő, még release candidate státuszú `v0.26.0-rc.1` build már `pgvector` **0.8.6**-ra vált. A `pgvector` saját (index nélküli) keresése pontos, "perfect recall"-lal; a HNSW/IVFFlat viszont közelítő, és a `0.8.0` verzió (2024-10-30) óta létező `hnsw.iterative_scan`/`ivfflat.iterative_scan` (alapértéken **kikapcsolva**) csak *addig* olvas be több jelöltet, amíg elég találat nem gyűlik össze vagy el nem éri a `max_scan_tuples`/`max_probes` korlátot — ez **nem** formális recall-garancia, csak egy "addig próbálkozik" heurisztika két módban (`strict_order` — pontos sorrend; `relaxed_order` — jobb recall, közelítő sorrend). A HNSW/IVFFlat indexelhető dimenziószáma `vector` típusnál **legfeljebb 2000**, `halfvec`-nél **legfeljebb 4000** — vagyis a projekt tervezett 768–4096 dimenziós beágyazási tartományának felső vége (pl. 3072–4096 dim modellek) **nem indexelhető** pgvector HNSW/IVFFlat-tal, csak pontos (index nélküli) kereséssel vagy bináris kvantálással. Egy AWS Aurora PostgreSQL blogbejegyzés (Shayon Sanyal, 2025-05-28) pontosan azt a táblázatot közli, amelyre a feladat háttere hivatkozik: naiv utószűrésnél 10%/1% recall, iteratív bejárással 100%; ezt egy 2026 februári, független UC Merced-kutatás (arXiv:2602.11443) is idézi és kvalitatívan megerősíti a `pgvector 0.8.1`-en végzett saját méréseivel, bár konkrét recall-számokat nem közöl szövegesen (csak ábrán). A ParadeDB dokumentációja explicit "Filter Pushdown" fejezetet szentel a témának: a `pg_search` a WHERE-feltételeket (numerikus, dátum, bool, `uuid`, illetve `IN`/`ANY`/`ALL` tömbös feltételek, tehát pl. `project_id IN (...)`) **magába az indexszkennelésbe tolja be**, ha az érintett oszlop is része a ParadeDB-indexnek — ellenkező esetben Postgres utólag, soronként ellenőrzi őket ("forcing Postgres to recheck them afterward"). Hibrid keresésre a hivatalos minta a **Reciprocal Rank Fusion** (`weight / (k + rank)`, `k=60` alapérték), amely a BM25- és vektor-ágat **rangsor**, nem nyers pontszám alapján egyesíti, és mindkét ág WHERE-ágába — a dokumentáció kifejezett ajánlása szerint — ugyanazok a jogosultsági szűrők tehetők be, hogy mindkét ág ugyanabból a jogosult sorhalmazból merítsen.

---

## 1. Vektorkeresés a ParadeDB-ben: saját megoldás vagy `pgvector`-ra épül?

### 1.1 A hivatalos dokumentáció négyszeresen megerősített állítása

A `docs.paradedb.com/concepts/vector/overview` ("How Vector Search Works") oldal:

> „Today, many Postgres applications use the [pgvector](https://github.com/pgvector/pgvector) extension for similarity search. pgvector works well for many use cases, but separate vector indexes can struggle when a query also needs selective filters, text predicates, or frequent updates."
>
> „The ParadeDB index supports pgvector's `vector` type inside the same index that stores text and columnar data. […] ParadeDB vectors use ParadeDB-built index structures designed for fast nearest-neighbor retrieval at scale. They are independent from pgvector's HNSW and IVFFlat indexes, while still using pgvector's `vector` type."

Forrás: [paradedb.com/docs/concepts/vector/overview](https://www.paradedb.com/docs/concepts/vector/overview) (T1, letöltve közvetlenül; a valós szöveg a React Server Components streaming-válasz egy külön szkript-darabjában van, nem a fő HTML body-ban).

Ugyanezt, technikai részletekkel kiegészítve, a `docs.paradedb.com/reference/indexing/indexing-vectors` oldal mondja ki (a szöveg szintén csak az RSC-streaming egyik `T`-jelű darabjából bontható ki, ASCII-visszafejtéssel):

> „Make sure the [pgvector](https://github.com/pgvector/pgvector) extension is installed first. ParadeDB uses pgvector's vector types, but not its HNSW or IVF indexes."
>
> „ParadeDB uses a SPANN-style vector index, which is similar to an IVF index but with additional structures to improve recall and latency, especially over large datasets."
>
> „Only pgvector's `vector` type is supported. The `halfvec`, `sparsevec`, and `bit` types are not yet indexable."

Forrás: [paradedb.com/docs/reference/indexing/indexing-vectors](https://www.paradedb.com/docs/reference/indexing/indexing-vectors) (T1).

**Harmadik, dátumhoz kötött megerősítés** — a `0.25.0` kiadási napló (ez az a kiadás, amely bevezette a natív vektoros keresést), szintén szó szerint:

> „**Breaking change**: As of `0.25.0`, [pgvector](https://github.com/pgvector/pgvector) is a required extension of `pg_search`. Before upgrading or installing the extension, please ensure that pgvector is installed on the same database. The reason is because 0.25.0 brings native vector search support to the ParadeDB index and relies on pgvector's vector type and distance operators."
>
> „**Native Vector Search (Beta)**: The ParadeDB index can now index the `vector` type. This index is completely separate from pgvector's HNSW/IVF indexes: Vectors are backed by a SPANN-style index, the state-of-the-art in vector search designed for datasets that are far larger than available memory. […] While vector search is marked as beta, future releases may change the vector storage format and require a reindex."

Forrás: [paradedb.com/docs/project/changelog/0.25.0](https://www.paradedb.com/docs/project/changelog/0.25.0) (T1).

**Negyedik, forráskód-szintű megerősítés** — a monorepó `pg_search/README.md` fejlesztői dokumentuma:

> „`pg_search` uses `pgvector`'s types to index vector fields alongside text and other fields in ParadeDB indexes, so `pgvector` must be available before `pg_search` can be created."
>
> build-utasítás: „`git clone --branch v0.8.6 https://github.com/pgvector/pgvector.git`"
>
> „Inside Postgres, create the extension (`CASCADE` also creates `pgvector`, which `pg_search` requires): `CREATE EXTENSION pg_search CASCADE;`"

Forrás: [raw.githubusercontent.com/paradedb/paradedb/main/pg_search/README.md](https://raw.githubusercontent.com/paradedb/paradedb/main/pg_search/README.md) (T1, GitHub `main` ág, lekérve 2026-09-22).

**Összegzés:** a `vector` **típus** (tárolási formátum, `<->`/`<=>`/`<#>` operátorok) `pgvector`-tól jön és kötelező függőség 0.25.0 óta; a tényleges **keresőindex-algoritmus** viszont a ParadeDB saját, SPANN-stílusú (klaszter-alapú, IVF-rokon, de attól bővített) struktúrája, amely a szöveges/BM25 és numerikus/szűrő adatokkal egy közös indexben él. A beta-státusz jelenleg is fennáll: a legfrissebb stabil kiadásban (`v0.25.9`, 2026-09-11) és a release candidate `v0.26.0-rc.1`-ben is a `reference/vector/querying` oldal így nyilatkozik: „This is a beta feature available in versions `0.25.0` and above."

### 1.2 SPANN-index paraméterei (amit a dokumentáció közöl)

Az index-létrehozási `WITH`-opciók (`reference/indexing/indexing-vectors`):

> „`centroid_ratio` (default `.01`): Vectors are clustered by proximity, and a centroid is a cluster's representative vector. This setting controls the number of centroids to build, as a fraction of the number of indexed vectors (`num_centroids = centroid_ratio * num_vectors`). More centroids produce smaller clusters, improving recall at the cost of a slower, more memory-intensive build. Must be between `0.000001` and `1.0`."
>
> „`training_sample_ratio` (default `.32`): The fraction of indexed vectors sampled to train the k-means clustering at build time. […] The default samples `0.32 * num_vectors`."
>
> „`cluster_replication` (default `1`): Accepted for compatibility. Vectors are currently assigned to their single nearest cluster regardless of this value."

Forrás: [paradedb.com/docs/reference/indexing/indexing-vectors](https://www.paradedb.com/docs/reference/indexing/indexing-vectors) (T1).

Fontos, hogy a `cluster_replication` paraméter **jelenleg nem csinál semmit** ("Accepted for compatibility") — azaz a SPANN-index (a névadó algoritmustól eltérően, amely tipikusan több klaszterbe is replikálja a határon lévő vektorokat a recall javítására) ma **csak egyetlen legközelebbi klaszterbe** sorolja be a vektorokat. Ez a szűréssel kombinált keresés recalljára nézve releváns, de erre vonatkozó konkrét recall-számot a dokumentáció nem közöl (lásd „Amire NINCS forrás").

### 1.3 `pgvector`-verzió a hivatalos Docker image-ben

A `paradedb/paradedb` szervezeti Docker Hub-fiók API-ja (`hub.docker.com/v2/repositories/paradedb/paradedb/tags`, lekérve 2026-09-22) szerint a **`latest`** címke jelenleg (`tag_last_pushed: 2026-09-11T18:29:05Z`) a **`0.25.9`** verzióra és a **PG 18** alapú build-re mutat (`latest` és `pg18` időbélyege másodpercre egyezik). A GitHub repó forrásából (jsdelivr GitHub-tükrön keresztül lekérve, mert a `raw.githubusercontent.com` közvetlen elérése a `docker/` alkönyvtárnál 404-et adott, a fájlok valójában a repó gyökerében vannak) a **`docker/Dockerfile.paradedb-{15,16,17,18}`** fájlok (per-PG-verzió build) mindegyike, a `v0.25.9` GitHub-tagen:

> „`postgresql-17-pgvector=0.8.4-1.pgdg13+1`" (és ugyanez `postgresql-{15,16,18}-pgvector=0.8.4-1.pgdg13+1` alakban a többi PG-verzióhoz, valamint a `Dockerfile.official-17`-ben is)

Forrás: [github.com/paradedb/paradedb](https://github.com/paradedb/paradedb) repó `docker/Dockerfile.paradedb-17` fájlja, `v0.25.9` tag, jsdelivr GitHub-tükrön keresztül lekérve: `cdn.jsdelivr.net/gh/paradedb/paradedb@0.25.9/docker/Dockerfile.paradedb-17` (T1, forráskód, 2026-09-22-i lekérés).

A `shared_preload_libraries` sor ugyanitt: `shared_preload_libraries = 'pg_search,pg_cron,pg_stat_statements'` — a `pgvector` **nincs** a preload-listán, csak APT-csomagként települ, `CREATE EXTENSION`-nel aktiválható; ez konzisztens az 1.1 pontban leírt "csak típus, nem index" viszonnyal.

A még nem stabil **`v0.26.0-rc.1`** tag (Docker Hub: `tag_last_pushed: 2026-09-11T22:24:41Z`) ugyanezen Dockerfile-jában már:

> „`postgresql-17-pgvector=0.8.6-1.pgdg13+1`"

Forrás: `cdn.jsdelivr.net/gh/paradedb/paradedb@0.26.0-rc.1/docker/Dockerfile.paradedb-17` (T1). Ez egybevág a `pg_search/README.md` fejlesztői build-utasításával, amely a `pgvector`-t forrásból `v0.8.6`-ra fixálva kéri klónozni (lásd 1.1).

**Összegzés — pgvector-verzió a hivatalos image-ben:** stabil csatorna (`v0.25.9`, 2026-09-11): **pgvector 0.8.4**. Release candidate csatorna (`v0.26.0-rc.1`, 2026-09-11): **pgvector 0.8.6**.

---

## 2. `pgvector` pontos és közelítő keresése

### 2.1 Index nélküli (pontos) keresés

A `pgvector` hivatalos README-je (`github.com/pgvector/pgvector`, `master` ág, lekérve közvetlenül `raw.githubusercontent.com`-ról):

> „By default, pgvector performs exact nearest neighbor search, which provides perfect recall."
>
> „#### Exact Search — To speed up queries without an index, increase `max_parallel_workers_per_gather`."
>
> „If vectors are normalized to length 1 (like [OpenAI embeddings](https://platform.openai.com/docs/guides/embeddings#which-distance-function-should-i-use)), use inner product for best performance."

Forrás: [github.com/pgvector/pgvector/blob/master/README.md](https://github.com/pgvector/pgvector/blob/master/README.md) (T1). Vagyis a "költség" index nélkül egyszerűen egy teljes szekvenciális (esetleg párhuzamosított) táblaolvasás + távolságszámítás minden sorra — a README nem ad Big-O-t vagy konkrét költségbecslést, csak a `max_parallel_workers_per_gather` tuningot ajánlja.

### 2.2 HNSW és IVFFlat

> „## HNSW — An HNSW index creates a multilayer graph. It has better query performance than IVFFlat (in terms of speed-recall tradeoff), but has slower build times and uses more memory. Also, an index can be created without any data in the table since there isn't a training step like IVFFlat."
>
> „### Query Options — Specify the size of the dynamic candidate list for search (40 by default)" — `SET hnsw.ef_search = 100;`
>
> „## IVFFlat — An IVFFlat index divides vectors into lists, and then searches a subset of those lists that are closest to the query vector. It has faster build times and uses less memory than HNSW, but has lower query performance (in terms of speed-recall tradeoff)."
>
> „### Query Options — Specify the number of probes (1 by default)" — `SET ivfflat.probes = 10;`

Alapértékek forráskód-szinten is megerősítve (`m=16`, `ef_construction=64` HNSW-nél; `ef_search` alapérték 40; `probes` alapérték 1). Forrás: [github.com/pgvector/pgvector/blob/master/README.md](https://github.com/pgvector/pgvector/blob/master/README.md) (T1).

### 2.3 Iteratív indexbejárás (`hnsw.iterative_scan`, 0.8.0)

A `CHANGELOG.md` szerint az iteratív indexbejárás a **`0.8.0`** kiadásban (**2024-10-30**) jelent meg: „## 0.8.0 (2024-10-30) — Added support for iterative index scans […] Improved cost estimation for better index selection when filtering". Forrás: [github.com/pgvector/pgvector/blob/master/CHANGELOG.md](https://github.com/pgvector/pgvector/blob/master/CHANGELOG.md) (T1). A jelenlegi (2026-09-22-i) legfrissebb stabil verzió a changelog szerint **0.8.6** (2026-07-29), a **0.8.7** pedig "unreleased" státuszban van.

A README pontos leírása a működésről:

> „With approximate indexes, queries with filtering can return less results since filtering is applied *after* the index is scanned. Starting with 0.8.0, you can enable iterative index scans, which will automatically scan more of the index until enough results are found (or it reaches `hnsw.max_scan_tuples` or `ivfflat.max_probes`)."
>
> „Iterative scans can use strict or relaxed ordering. Strict ensures results are in the exact order by distance" — `SET hnsw.iterative_scan = strict_order;` — „Relaxed allows results to be slightly out of order by distance, but provides better recall" — `SET hnsw.iterative_scan = relaxed_order;` / `SET ivfflat.iterative_scan = relaxed_order;`
>
> „#### HNSW — Specify the max number of tuples to visit (20,000 by default)" — `SET hnsw.max_scan_tuples = 20000;` (megjegyzés: „This is approximate and does not affect the initial scan") — „Specify the max amount of memory to use, as a multiple of `work_mem` (1 by default)" — `SET hnsw.scan_mem_multiplier = 2;`
>
> „#### IVFFlat — Specify the max number of probes" — `SET ivfflat.max_probes = 100;` („If this is lower than `ivfflat.probes`, `ivfflat.probes` will be used")

Forrás: [github.com/pgvector/pgvector/blob/master/README.md](https://github.com/pgvector/pgvector/blob/master/README.md) (T1).

**Mit garantál és mit nem?** A mechanizmus **nem** ad formális recall-garanciát — csak addig olvas be újabb jelölteket ("automatically scan more of the index"), amíg (a) elég találat össze nem gyűlik, VAGY (b) el nem éri a `hnsw.max_scan_tuples`/`ivfflat.max_probes` felső korlátot, amelynél a bejárás megáll, akárhány találat is van addig. `strict_order` a távolság szerinti **pontos sorrendet** garantálja (de nem a teljes recallt); `relaxed_order` a sorrendet **nem** garantálja pontosan, cserébe jobb recallt ad ugyanannyi munkával. Az alapértékek forráskód-szinten (nem csak a READMÉ-ben, hanem a tényleges GUC-regisztrációban) is ellenőrizve:

> `src/hnsw.c`: „`DefineCustomEnumVariable("hnsw.iterative_scan", …, HNSW_ITERATIVE_SCAN_OFF, hnsw_iterative_scan_options, …)`" — azaz a **`hnsw.iterative_scan` alapértéke `off`**, a lehetséges értékek `off`/`relaxed_order`/`strict_order`.
>
> `src/ivfflat.c`: „`DefineCustomEnumVariable("ivfflat.iterative_scan", …, IVFFLAT_ITERATIVE_SCAN_OFF, ivfflat_iterative_scan_options, …)`", és az enum-lista csak `{"off", …}, {"relaxed_order", …}` — **`strict_order` nem létezik IVFFlat-nál**, csak `off`/`relaxed_order`.

Forrás: [github.com/pgvector/pgvector/blob/master/src/hnsw.c](https://github.com/pgvector/pgvector/blob/master/src/hnsw.c) és [github.com/pgvector/pgvector/blob/master/src/ivfflat.c](https://github.com/pgvector/pgvector/blob/master/src/ivfflat.c) (T1, `master` ág, közvetlen forráskód-lekérés).

### 2.4 Dimenziókorlátok — pontos számok a README-ből

A README két, **egymástól élesen elkülönülő** korlátot ad: az **adattípus tárolási** korlátját és az **indexelhető** korlátot.

Tárolási korlát (bármilyen index nélkül is érvényes):

> „Each vector takes `4 * dimensions + 8` bytes of storage. […] Vectors can have up to **16,000 dimensions**." (`vector` típus)
>
> „Each half vector takes `2 * dimensions + 8` bytes of storage. […] Half vectors can have up to **16,000 dimensions**." (`halfvec` típus)

Indexelhető (HNSW **és** IVFFlat) korlát — mindkét index-szakasz szó szerint ugyanazt a táblázatot közli:

> „Supported types are: — `vector` - up to **2,000 dimensions** — `halfvec` - up to **4,000 dimensions** — `bit` - up to **64,000 dimensions** — `sparsevec` - up to **1,000 non-zero elements**"

A GYIK-részben ugyanez, megoldási javaslattal együtt:

> „#### What if I want to index vectors with more than 2,000 dimensions? — You can use [half-precision vectors](#half-precision-vectors) or [half-precision indexing](#half-precision-indexing) to index up to 4,000 dimensions or [binary quantization](#binary-quantization) to index up to 64,000 dimensions."

Forrás mindhárom idézethez: [github.com/pgvector/pgvector/blob/master/README.md](https://github.com/pgvector/pgvector/blob/master/README.md) (T1).

**Relevancia a projekt 768–4096 dimenziós tartományára:** a `vector` típus HNSW/IVFFlat-indexelhetősége **2000 dimenziónál megáll**; a `halfvec`-es út **4000 dimenzióig** tolja ki a határt. A tartomány felső vége (**4096 dimenzió**, pl. bizonyos nagyobb beágyazó modellek) tehát **egyik indexelhető típussal sem fér el** — csak index nélküli (pontos) kereséssel, vagy `bit`/bináris kvantálással (ami lossy, más reprezentáció) kezelhető pgvectorral. Ezt egy **második, független forrás** — a ParadeDB saját "pgvector Limitations" cikke — is ugyanezekkel a számokkal erősíti meg: „The indexable vector type tops out at 2,000 dimensions. The halfvec type (16-bit floats) extends this to 4,000 dimensions and roughly halves storage, bit vectors extend to 64,000 dimensions through binary quantization, and sparsevec stores up to 1,000 nonzero elements." Forrás: [paradedb.com/learn/postgresql/pgvector-limitations](https://www.paradedb.com/learn/postgresql/pgvector-limitations) (T3 — ParadeDB saját marketing/„learn" blogja, nem a `/docs/` referencia, de számszerűen egybevág a README-vel).

---

## 3. Szűrés jogosultságra (pgvector oldalán)

### 3.1 Hivatalos ajánlások

A README „Filtering" és „Multitenancy" szakasza pontosan a projekt D-32 forgatókönyvét írja le:

> „## Filtering — There are a few ways to index nearest neighbor queries with a `WHERE` clause. […] A good place to start is creating an index on the filter column. This can provide fast, exact nearest neighbor search in many cases. […] Exact indexes work well for conditions that match a low percentage of rows. Otherwise, [approximate indexes](#indexing) can work better."
>
> „With approximate indexes, filtering is applied *after* the index is scanned. If a condition matches 10% of rows, with HNSW and the default `hnsw.ef_search` of 40, only 4 rows will match on average. For more rows, enable [iterative index scans](#iterative-index-scans), which will automatically scan more of the index when needed."
>
> „If filtering by only a few distinct values, consider [partial indexing](https://www.postgresql.org/docs/current/indexes-partial.html)." — `CREATE INDEX ON items USING hnsw (embedding vector_l2_ops) WHERE (category_id = 123);`
>
> „If filtering by many different values, consider [partitioning](https://www.postgresql.org/docs/current/ddl-partitioning.html)." — `CREATE TABLE items (embedding vector(3), category_id int) PARTITION BY LIST(category_id);`
>
> „## Multitenancy — For applications with multiple tenants, sharing an approximate index between tenants means vectors from one tenant can affect recall (and speed) for other tenants. For tenant isolation, use [list partitioning](https://www.postgresql.org/docs/current/ddl-partitioning.html) or separate tables." — `CREATE TABLE items (customer_id int, embedding vector(3)) PARTITION BY LIST(customer_id);`

Forrás: [github.com/pgvector/pgvector/blob/master/README.md](https://github.com/pgvector/pgvector/blob/master/README.md) (T1). Ez utóbbi bekezdés — bár "tenant", nem "project"/"jogosultság" szóhasználattal — architekturálisan pontosan a jelen projekt "project-ek szeparáltak legyenek" célkitűzésére vonatkozik: a hivatalos ajánlás a **közös index kerülése** (listapartícionálás vagy külön tábla projektenként), mert egyetlen megosztott approximate indexben "vectors from one tenant can affect recall (and speed) for other tenants".

### 3.2 Független mérés a szűrt HNSW recalljáról a 0.8.0 óta

**Első forrás (T2, felhő-szolgáltató, a pgvector projekttől független cég):** az AWS Database Blog cikke ("Supercharging vector search performance and relevance with pgvector 0.8.0 on Amazon Aurora PostgreSQL", szerző: Shayon Sanyal, közzététel: **2025-05-28**) pontosan azt a táblázatot közli, amelyre a feladat háttere hivatkozik ("naiv utószűrésnél 10%/1%, iteratív bejárással 100%"):

> „Remember that recall means we return X out of Y expected results, with 100% being perfect recall:"
>
> | Query | 0.7.4 baseline (ef_search=40) | 0.7.4 (ef_search=200) | 0.8.0 with strict_order | 0.8.0 with relaxed_order |
> |---|---|---|---|---|
> | Category-filtered search | **10%** | 0% | **100%** | **100%** |
> | Complex filtered search | **1%** | 0% | **100%** | **100%** |
> | Very large result set | 5% | 5% | 100% | 100% |
>
> „For highly selective queries (products in a specific category), pgvector 0.7.4 returned only a fraction of requested results. With iterative scanning enabled in 0.8.0, we saw up to **100 times improvement** in result completeness, substantially enhancing the user experience."

A cikk teszt-konfigurációi is dokumentáltak: „0.7.4 baseline: ef_search=40 — 0.7.4: ef_search=200 — 0.8.0 baseline: ef_search=40, iterative_scan=off — 0.8.0: ef_search=40, iterative_scan=strict_order — 0.8.0: ef_search=40, iterative_scan=relaxed_order — 0.8.0: ef_search=200, iterative_scan=strict_order — 0.8.0: ef_search=200, iterative_scan=relaxed_order." Forrás: [aws.amazon.com/blogs/database/supercharging-vector-search-performance-and-relevance-with-pgvector-0-8-0-on-amazon-aurora-postgresql](https://aws.amazon.com/blogs/database/supercharging-vector-search-performance-and-relevance-with-pgvector-0-8-0-on-amazon-aurora-postgresql/) (T2, nyers HTML-ből kigrepelve, 2026-09-22-i lekérés).

**Második, valóban független forrás (T1, akadémiai preprint):** Amanbayev, Tsan, Dang és Rusu (University of California, Merced), *"Filtered Approximate Nearest Neighbor Search in Vector Databases: System Design and Performance Analysis"*, **arXiv:2602.11443**, **2026. február**. A dolgozat kifejezetten a `pgvector 0.8.1`-et (Postgres 16 alatt, "git main" build) méri, más rendszerekkel (FAISS, Milvus) összevetve, és **maga is idézi az AWS-blogot** forrásként (46. hivatkozás). Releváns, szó szerinti idézetek:

> „Post-filtering […] is commonly implemented in relational DBMS systems, such as pgvector in PostgreSQL […] It often performs well in terms of search latency but may suffer from reduced recall. […] In graph-based indexes, filtering occurs only on the limited set of vectors in the candidate priority queue (e.g., in HNSW, a larger queue size increases traversal latency). For low selectivity predicates uncorrelated with vector similarities, this can lead to incomplete top-k results (fewer than k survivors)."
>
> „We identify that pgvector's cost-based optimizer frequently misjudges execution costs, favoring approximate index scans even when exact sequential scans would yield perfect recall at comparable latency."
>
> „**Optimizer Fragility**: We exposed some limitations in pgvector's cost-based optimizer, which frequently fails to switch to sequential scans or attribute-index scans when they would provide perfect recall at competitive latencies."
>
> Gyakorlati ajánlásaik között (7.4. szakasz), kifejezetten a jelen kutatási kérdéshez illő tanáccsal: „**Index metadata attributes aggressively (pgvector)**. In relational vector extensions, metadata indexes unlock execution plans that the optimizer can exploit for filtered queries. Without them, the system often commits to recall-degrading post-filtering strategies."

A dolgozat egy külön ábrán (17. ábra) közli is a mérést: „Figure 17: QPS–Recall curves for HNSW and IVFFlat in pgvector with and without index on the filter attribute" — de a **konkrét számszerű recall-értékeket** (pl. hány % adott szelektivitásnál) a kinyert szöveges tartalom nem tartalmazza, csak az ábra-referenciát (lásd „Amire NINCS forrás"). Forrás: [arxiv.org/html/2602.11443v1](https://arxiv.org/html/2602.11443v1) (T1, nyers HTML-ből kigrepelve, 2026-09-22-i lekérés).

**Kiegészítő, első-fél (nem független) adatpont a ParadeDB saját CI-benchmark-jából:** a `paradedb/paradedb` GitHub-repó `benchmarks/datasets/cohere/` alatt egy Cohere Wikipedia-beágyazásos (1024 dim) benchmark-csomagot tartalmaz, amely a `pg_search`-öt HNSW-vel, IVFFlat-tal és a VectorChord (vchordrq) kiterjesztéssel veti össze 0%/10%/1% szűrési szelektivitásnál. A `config.toml` explicit dokumentálja a "tisztességes" összevetéshez szükséges — meglepően magas — HNSW-paramétereket 1%-os szelektivitásnál:

> „`ef_search_1pct = "1000"`" · „`max_scan_tuples_1pct = "CASE … WHEN 10000000 THEN 5000000 …"`" · „`scan_mem_multiplier_1pct = "16"`" — megjegyzés a fájlban: „tuned for 95% recall"

és a tényleges lekérdezés (`queries/knn_top10_1pct.sql`) `hnsw.iterative_scan=relaxed_order`-t állít be. Vagyis a ParadeDB saját mérési protokollja szerint 1%-os szelektivitásnál egy 10 milliós adathalmazon `hnsw.max_scan_tuples`-t **5 millióra** (a tábla feléig!) és `ef_search`-öt **1000**-re kell emelni ahhoz, hogy a HNSW ~95%-os recallt tartson — ez kvalitatívan megerősíti a fenti két forrás által leírt jelenséget, de a `pg_search`/HNSW ágakra vonatkozó **konkrét mért recall-számot** a lekérdezhető fájlokban nem közöl (csak a VectorChord-ágra van explicit mért szám, lásd lent). Forrás: [github.com/paradedb/paradedb](https://github.com/paradedb/paradedb) repó `benchmarks/datasets/cohere/config.toml` és `queries/knn_top10_1pct.sql`, `v0.25.9` tag (T1, forráskód, első-fél/gyártói forrás).

---

## 4. Hibrid keresés (BM25 + vektor) a ParadeDB-ben

### 4.1 Van hivatalos minta, és Reciprocal Rank Fusion

> „Hybrid search combines the strengths of text search and vector search. […] Because those signals fail in different ways, combining them often produces a better result set than either one alone."
>
> „BM25 scores and vector distances operate on different scales, so they cannot be added together directly. ParadeDB's hybrid examples use Reciprocal Rank Fusion, which discards raw scores and uses only each row's position, or rank, in each result list. With rank fusion, a row that ranks first contributes the same amount whether its BM25 score was 1 or 100."

Forrás: [paradedb.com/docs/concepts/hybrid/overview](https://www.paradedb.com/docs/concepts/hybrid/overview) (T1). Tehát a válasz egyértelmű: **RRF**, nem nyers pontszám-összegzés (a BM25-pontszám és a koszinusz-/L2-távolság közvetlenül nem összeadható, mert más skálán mozognak).

### 4.2 A fúziós képlet és a konkrét SQL-példa

> „Each branch contributes `weight / (k + rank)`, and the contributions are added. — `rank` is the row's position in that branch's list, starting at 1. — `weight` scales how much that branch contributes […] — `k` is the rank constant. It softens the difference between adjacent positions […] `60` is the conventional value and the one used throughout this page."

A teljes, szó szerint idézett SQL-minta (`reference/hybrid/rrf` oldal):

```sql
WITH text AS (
    SELECT id, RANK() OVER (ORDER BY pdb.score(id) DESC, id) AS rank
    FROM mock_items
    WHERE description ||| 'running shoes'
    ORDER BY pdb.score(id) DESC, id
    LIMIT 20
),
vector AS (
    SELECT id, RANK() OVER (ORDER BY embedding <=> '[1,2,3,4,5,6,7,8]', id) AS rank
    FROM mock_items
    WHERE id @@@ pdb.all()
    ORDER BY embedding <=> '[1,2,3,4,5,6,7,8]', id
    LIMIT 20
),
fused AS (
    SELECT id, sum(weight) AS score
    FROM (
        SELECT id, 1.0 / (60 + rank) AS weight FROM text
        UNION ALL
        SELECT id, 0.7 / (60 + rank) AS weight FROM vector
    ) u
    GROUP BY id
)
SELECT m.id, m.description, f.score
FROM fused f
JOIN mock_items m USING (id)
ORDER BY f.score DESC, m.id
LIMIT 5;
```

Forrás: [paradedb.com/docs/reference/hybrid/rrf](https://www.paradedb.com/docs/reference/hybrid/rrf) (T1, a fenti SQL a React-streaming válasz nyers `T`-darabjából szó szerint kibontva).

### 4.3 Szűrhető-e mindkét ág jogosultságra ugyanabban a lekérdezésben?

Igen — a dokumentáció ezt kifejezetten megmagyarázza és ajánlja:

> „The two `WHERE` clauses differ because each branch retrieves by its own method. `description ||| 'running shoes'` is the text branch's query. The vector branch's query is the query vector in its `ORDER BY`, so its `WHERE` is `pdb.all()`, meaning every row is eligible. **To narrow either branch, add filters to both, so that each is drawing from the same set of eligible rows.**"

Forrás: [paradedb.com/docs/reference/hybrid/rrf](https://www.paradedb.com/docs/reference/hybrid/rrf) (T1). Vagyis a D-32-höz illő minta az lenne, hogy a `text` CTE `WHERE`-jébe **és** a `vector` CTE `WHERE`-jébe (a `pdb.all()` helyére) is bekerül ugyanaz a jogosultsági predikátum (pl. `project_id @@@ pdb.term(...)` vagy — a 3. fejezetben tárgyalt indexelt oszlopos út esetén — sima `project_id IN (...)`), hogy mindkét ág ugyanabból a jogosult sorhalmazból dolgozzon.

### 4.4 Előszűrés vagy utószűrés a BM25-ágban?

A dokumentáció a "Verifying Pushdown" szakaszban explicit ellenőrzési módszert ad, és a `Custom Scan`/`TopKScanExecState` jelenléte a **pushdown-olt (index-be tolt, tehát gyakorlatilag előszűrt)** végrehajtást jelzi:

> „To verify that the hybrid query is being accelerated by ParadeDB, inspect the query plan by running `EXPLAIN`: […] If the query is accelerated, there should be a `TopKScanExecState` printed for each branch." — példa terv-részlet: „`-> WindowAgg … -> Custom Scan (ParadeDB Base Scan) on mock_items — Exec Method: TopKScanExecState — TopK Order By: pdb.score() desc, id asc — TopK Limit: 20`" — „If you do not see `TopKScanExecState`, the branch is not taking the optimized path."

Forrás: [paradedb.com/docs/reference/hybrid/rrf](https://www.paradedb.com/docs/reference/hybrid/rrf) (T1). Ez összhangban van az 5. fejezetben tárgyalt "Filter Pushdown" mechanizmussal: ha a szűrt oszlop (pl. `project_id`) az indexben van és a típus/operátor a pushdown-táblázatban szerepel, a szűrés az indexszkennelésen belül (tehát *előszűrésként*) történik; ha nem, Postgres a `TopKScanExecState`helyett mást mutat, és a szűrés utólagos, soronkénti "recheck"-ké válik (lásd 5.2).

---

## 5. A `pg_search` és a szűrés: WHERE az indexen belül, vagy utólagos Postgres-szűrés?

### 5.1 „Filter Pushdown" — a dokumentáció szó szerint ezt a kifejezést használja

A `reference/filtering/indexed` oldal fejezetcíme és bevezetője:

> „Indexed columns are columns or expressions included in the ParadeDB index. For filters over built-in scalar types and literal text columns, this is the most efficient path because the filter can be pushed directly into the ParadeDB scan."
>
> „## Filter Pushdown — ### Non-Text Columns — While not required, filtering performance over non-text columns can be improved by including them in the ParadeDB index. **When these columns are part of the index, WHERE clauses that reference them can be pushed down into the index scan itself.** This can result in faster query execution over large datasets."

Forrás: [paradedb.com/docs/reference/filtering/indexed](https://www.paradedb.com/docs/reference/filtering/indexed) (T1; a `docs.paradedb.com/documentation/filtering/indexed` és `www.paradedb.com/docs/documentation/filtering/indexed` URL-ek 308-cal ugyanide irányítanak át).

### 5.2 Konkrét típus/operátor-táblázat — `project_id IN (…)` pushdown-képes-e?

A dokumentáció egy explicit táblázatot közöl arról, mely típus/operátor-kombinációk tolhatók be az indexbe:

> „Filter pushdown is currently supported for the following combinations of types and operators: — `=, <, >, <=, >=, <>, BETWEEN`: int2, int4, int8, float4, float8, numeric, date, time, timetz, timestamp, timestamptz, uuid (azonos-azonos típuspárok) — `=`: bool–bool (pl. `WHERE in_stock = true`) — **`IN, ANY, ALL`: bool–bool[], int2/int4/int8–saját és egymás tömbváltozatai, float4/float8–saját és egymás tömbváltozatai, date–date[], timetz–timetz[], timestamp–timestamp[], timestamptz–timestamptz[], `uuid`–`uuid[]`** (pl. `WHERE rating IN (1,2,3)`) — `IS, IS NOT`: bool–bool (pl. `WHERE in_stock IS true`) — `IS NULL, IS NOT NULL`: a fenti skalár típusokra."

Forrás: [paradedb.com/docs/reference/filtering/indexed](https://www.paradedb.com/docs/reference/filtering/indexed) (T1). **Ez direkt választ ad a kérdésre:** ha a jogosultsági oszlop (pl. `project_id`) `int4`/`int8`/`uuid` típusú **és** része a ParadeDB-indexnek, akkor a `project_id IN (…)` forma kifejezetten a támogatott pushdown-kombinációk között szerepel (`uuid`–`uuid[]`, illetve az egész típusok saját/kereszt-tömbváltozatai).

Szöveges oszlopoknál (pl. ha a jogosultsági kulcs `text`) a pushdown külön feltételhez kötött:

> „To push down the `category = 'Footwear'` filter, `category` must be indexed using the [literal tokenizer](/reference/tokenizers/available-tokenizers/literal): `CREATE INDEX search_idx ON mock_items USING paradedb (id, description, (category::pdb.literal)) WITH (key_field = 'id');`"
>
> „**Pushdown of set filters over text columns also requires the literal tokenizer**" — azaz `category IN ('Footwear', 'Apparel')` is csak `literal` tokenizerrel indexelt oszlopnál kerül be az indexbe.

Forrás: [paradedb.com/docs/reference/filtering/indexed](https://www.paradedb.com/docs/reference/filtering/indexed) (T1).

### 5.3 Mi történik, ha a szűrt oszlop NEM indexelt — a dokumentáció explicit kimondja: utólagos, soronkénti Postgres-ellenőrzés

Az általánosabb `reference/filtering/overview` oldal (rövid, de tartalmilag lényegi) a jelenséget általános adatbázis-elméleti keretbe helyezi:

> „In many databases, an index can speed up one part of a query while the remaining filters are checked later, one row at a time. That is correct, but it can be expensive when the search condition matches many rows. **ParadeDB avoids that pattern where possible.** It can apply many filters directly during the ParadeDB index scan, including numeric comparisons, boolean checks, **set membership**, null checks, etc. When a filter is better served by a different index, ParadeDB can also combine its own results with the candidates from that index before returning rows."
>
> „## Choosing a Filtering Path — The fastest option is to put frequently-filtered columns in the ParadeDB index when their type can be represented by ParadeDB. This is the right path for most built-in scalar column types, including numbers, booleans, dates, UUIDs, and literal text."

Forrás: [paradedb.com/docs/reference/filtering/overview](https://www.paradedb.com/docs/reference/filtering/overview) (T1).

A vektoros keresés oldala (`reference/vector/querying`) ugyanezt vektor+szűrő kombinációra explicit ki is mondja — ez a legpontosabb, közvetlen forrás arra, hogy nem-indexelt szűrőoszlop esetén **valóban utólagos, Postgres-oldali "recheck"** történik, nem index-szintű pushdown:

> „**Every column you filter on (e.g. `category` above) must also be part of the ParadeDB index. Filters on unindexed columns cannot be evaluated by the ParadeDB index, forcing Postgres to recheck them afterward and eliminating the benefit of combining vector search with filtering.**"

Forrás: [paradedb.com/docs/reference/vector/querying](https://www.paradedb.com/docs/reference/vector/querying) (T1).

**Összegzés Q5-re:** a `pg_search` BM25/ParadeDB-index **igen**, tud WHERE-feltételt (beleértve `IN`/halmaztagsági feltételt is, tehát tipikusan egy `project_id IN (...)` jogosultsági szűrőt) az indexen belül, előszűrésként érvényesíteni — de **csak akkor**, ha (a) az érintett oszlop maga is szerepel a ParadeDB `USING paradedb (...)` index-definíciójában, (b) szöveges oszlopnál a `literal` tokenizerrel van indexelve, és (c) a típus/operátor-pár szerepel az 5.2-ben idézett hivatalos pushdown-táblázatban. Ha ezek bármelyike hiányzik, a dokumentáció szó szerint "recheck"-nek nevezi az utólagos, Postgres-oldali, soronkénti ellenőrzést — ez felel meg a kérdésben említett "filter pushdown" vs. utószűrés megkülönböztetésnek, és a dokumentáció maga is a **"Filter Pushdown"** kifejezést használja fejezetcímként.

---

## Ellentmondások

- **Nem találtam tartalmi ellentmondást** a fő állítások között (ParadeDB saját SPANN-index vs. `pgvector`-tól csak a típus; pgvector iteratív bejárás működése; filter pushdown mechanizmusa) — a négy különböző ParadeDB-forrás (két `/docs/` oldal, egy changelog-bejegyzés, egy GitHub `README.md`) és a `pgvector` README + forráskód (`hnsw.c`/`ivfflat.c`) egymással teljesen konzisztensek.
- **Forrás-minőségi árnyalat, nem valódi ellentmondás:** a feladat háttere "gyártói mérés"-nek nevezi a 10%/1% → 100% recall-táblázatot. Ez **nem a `pgvector` projekt** (Andrew Kane) saját, hivatalos mérése — nem található ilyen táblázat a `pgvector` GitHub repóban vagy a `postgresql.org` hivatalos `0.8.0` bejelentésében —, hanem az **Amazon Aurora PostgreSQL csapatának** (AWS Database Blog, Shayon Sanyal, 2025-05-28) saját, Aurora-specifikus tesztkörnyezetben futtatott mérése. A "gyártó" itt tehát pontosabban "egy nagy felhő-szolgáltató, aki a pgvectort disztribúcióként kínálja", nem a `pgvector` upstream projekt maga.
- **Hiányos lefedettség, nem ellentmondás:** a független UC Merced-tanulmány (arXiv:2602.11443, 2026 február) `pgvector 0.8.1`-en méri a szűrt HNSW/IVFFlat recallt, és **explicit idézi is** az AWS-blogot forrásként — de a saját kísérleti protokollja (7.1–7.2. szakasz) **nem teszteli a `hnsw.iterative_scan`/`ivfflat.iterative_scan` funkciót külön** (a "iterative_scan" kifejezés az egész dolgozatban nem fordul elő a kinyert szövegben) — a méréseik "post-filtering" vs. "pre-filtering" stratégiákat hasonlítanak össze, nem az `iterative_scan` be/kikapcsolt állapotát. Ez azt jelenti, hogy a két forrás (AWS és UC Merced) **különböző dimenziót** mér, még ha ugyanarra a mögöttes jelenségre (szűrt HNSW recall-esés) is vonatkoznak — nem cáfolják, de nem is azonos kísérleti beállítást erősítenek meg egymás mellett.
- A ParadeDB saját `docs.paradedb.com/reference/indexing/indexing-vectors` oldala szerint `cluster_replication` paraméter létezik, de "Accepted for compatibility. Vectors are currently assigned to their single nearest cluster regardless of this value." — ez arra utal, hogy a SPANN-index **jelenlegi** implementációja **nem** valósítja meg a SPANN-algoritmus névadó jellemzőjét (határon lévő vektorok több klaszterbe replikálása a recall javítására), noha a paraméter már létezik az API-ban "kompatibilitás" céljából (feltehetően egy jövőbeli verzióra készülve). Ez nem forrás-ellentmondás, inkább a dokumentáció önmagában jelzett korlátozása.

## Amire NINCS forrás

- **NINCS FORRÁS** a feladat hátterében említett konkrét "1%-os szelektivitásnál 0,1%-ra" recall-esés számára — sem az AWS-blogban, sem a kigrepelt arXiv-szövegben, sem a `pgvector` README-ben/changelogban nem találtam ezzel a pontos számpárral (1% szelektivitás → 0,1% recall) egyező, szó szerint idézhető állítást. Az arXiv-dolgozat 6. ábrája ("QPS–Recall curves at different selectivity levels") vizuálisan tartalmazhatja ezt az adatpontot, de a kinyert szöveges tartalom nem közöl belőle számszerű értéket.
- **NINCS FORRÁS** arra, hogy a ParadeDB saját SPANN-stílusú vektorindexének **konkrétan mekkora az indexelhető maximális dimenziószáma** — a dokumentáció csak azt mondja ki, hogy "Only pgvector's `vector` type is supported", implicit módon örökölve a `pgvector` `vector`-típus tárolási korlátját (16 000 dim), de nem világos, hogy a ParadeDB saját SPANN-index maga is korlátozott-e (és ha igen, mennyire) a `pgvector` HNSW/IVFFlat 2000-dimenziós indexelhetőségi korlátjához hasonlóan, vagy attól függetlenül más a helyzet.
- **NINCS FORRÁS** a ParadeDB saját SPANN-indexének **recall-viselkedésére erős jogosultsági szűrés (pl. 1%-os szelektivitás) mellett** — a hivatalos dokumentáció csak azt írja le, hogy a szűrt oszlopnak indexeltnek kell lennie a pushdown-hoz, és hogy `EXPLAIN`-nel `TopKScanExecState`-tel ellenőrizhető a gyorsítás, de **konkrét recall-számot vagy -garanciát erős szelektivitásnál nem közöl** (szemben a `pgvector`/HNSW-re vonatkozó, AWS által mért 10%/1%/100%-os adatokkal). A ParadeDB saját `benchmarks/` CI-csomagjában van egy `recall.sql` és Cohere-alapú tesztkeret, amely ezt módszertanilag megalapozná, de a lekérdezhető fájlokból (config, index-, query-SQL-ek) csak a *tuning-célértékeket* ("tuned for 95% recall") és a VectorChord-ágra vonatkozó mért számokat ("unfiltered 60 -> 0.961, 10pct 80 -> 0.953, 1pct 420 -> 0.959") sikerült kinyerni — a `pg_search`/SPANN-ágra vonatkozó tényleges mért recall-eredmény nem szerepel ezekben a fájlokban (feltehetően csak a CI futtatás eredményeként, nyilvánosan nem publikált formában létezik).
- **NINCS FORRÁS** független (nem ParadeDB által írt) mérésre vagy elemzésre a ParadeDB saját vektorindexéről — minden, a ParadeDB SPANN-indexére vonatkozó technikai állítás ParadeDB saját forrásaiból (docs.paradedb.com, GitHub-repó) származik; harmadik féltől (pl. Tiger Data/Timescale blogja, amelyet ellenőriztem) nem találtam olyan cikket, amely külön kitérne a ParadeDB saját index-algoritmusára vagy annak recalljára.
- **NINCS FORRÁS** arra, hogy a `paradedb.vector_cluster_max_probe` GUC-paraméter (amelyet csak a `benchmarks/datasets/cohere/queries/pg_search/knn_top10_1pct.sql` fájlban találtam meg, `SET paradedb.vector_cluster_max_probe={{ pg_search_max_probe }};` formában) szerepelne-e egyáltalán a nyilvános `/docs/` referenciaoldalakon — a hivatalos "Querying Vectors"/"Indexing Vectors" oldalakon nem találtam rá utalást, így nem tudom megerősíteni, hogy ez egy dokumentált, stabil, éles használatra ajánlott beállítás-e, vagy csak belső/kísérleti tuning-kapcsoló.



---

# SQ05 — Üzemeltetés egy gépen: mentés, frissítés, erőforrás

> **Módszertani megjegyzés (degradált mód):** A `anthropic-skills:deep-web-research` skillt a `_kozos.txt` előírása szerint próbáltam használni, de ebben a környezetben nem érhető el alügynök-indító (Agent/Task) eszköz, és a feladatleírás kifejezetten tiltja, hogy a teljes kutatást egyetlen újabb alügynökre delegáljam. Ezért a skill saját "degradált módja" szerint jártam el: a fázisokat (tervezés → keresés → hézagpótló körök → ellenőrzés → szintézis) egyetlen, saját kontextusban, szekvenciálisan futtattam, Sonnet/Opus-elkülönítés és automatikus evidence-vault (`.research/`) build nélkül. A kötelező módszertani elemeket (elsődleges forrás előny, szó szerinti idézetek, URL-ek, kereszthivatkozás-kísérlet minden lényeges állításnál, verzió+dátum jelölése, „NINCS FORRÁS" jelölés) manuálisan tartottam be `WebSearch`/`WebFetch` eszközökkel.

## Rövid válasz

Hivatalos RAM-minimumot (tétlen vagy terhelt állapotra) a ParadeDB dokumentációja sehol nem ad meg; csak index-építési memóriaszabályokat közöl (`maintenance_work_mem` ≈ RAM/16, workerenként min. 15 MB). A `pg_dump`/`pg_restore` a BM25 indexet — mint minden Postgres-indexet — csak *definícióként* (CREATE INDEX) menti, tehát visszaállításkor újraépül, de erre nincs ParadeDB-specifikus hivatalos megerősítés, csak az általános Postgres pg_dump-viselkedés. A `pg_basebackup`/PITR csak 2025 eleje óta ("Block Storage" migráció) működik elvileg a BM25 indexszel, mert azelőtt az index Postgres blokktárolón *kívül* élt; egy 2025. novemberi hivatalos GitHub-vitában a ParadeDB fejlesztője viszont kimondja, hogy a standby-ról való olvasás WAL-integrációja kizárólag Enterprise-kiadásban elérhető, Community-ban nem — ez ellentmond a blogbejegyzés általánosabb megfogalmazásának, a forrás ezt nem oldja fel egyértelműen. Törölt sorok ("holt" tuple-ök) a hivatalos Postgres-dokumentáció szerint fizikailag a fájlokban maradnak VACUUM előtt, így egy fájlszintű (`pg_basebackup`) mentés is tartalmazza őket. Az `ALTER EXTENSION pg_search UPDATE` lépést a hivatalos frissítési útmutató kötelezőnek mondja minden környezetben, de a REINDEX szükségességéről és a Postgres-főverzió-váltásról (`pg_upgrade`) a ParadeDB dokumentációja teljesen hallgat. Karbantartás terén a hivatalos doksi kimondja, hogy autovacuum hiányában a BM25 index korlátlanul nő, VACUUM önmagában nem csökkenti a méretet, csak REINDEX vagy törlés-újraépítés; a korrupció-észlelésre saját, "amcheck-stílusú" `pdb.verify_index`/`bt_index_check`-analóg függvényt kínálnak, mert a natív Postgres `amcheck` csak B-Tree és GIN indexeket támogat. Telepítés terén Linuxra (.deb/.rpm, Debian/Ubuntu/RHEL) és macOS-re (.pkg, csak Apple Silicon/arm64, Sequoia/Tahoe) is van hivatalos csomag, Docker-image is van (amd64+arm64), de Homebrew-csomag még nincs — ez egy 2024 óta nyitott GitHub-issue tárgya. Beágyazott/egyfájlos mód nincs: a hivatalos doksi kifejezetten "vanilla Postgres kiterjesztésként" írja le, nem önálló adatbázis-fájlként.

## 1. Erőforrásigény (RAM)

### 1.1 Hivatalos minimum-ajánlás tétlen/terhelt állapotra

Széles körű keresés (ParadeDB hivatalos doksi, "Go to Production" oldal, "Introduction" oldal, konfigurációs referencia) ellenére **nem találtam hivatalos, számszerű RAM-minimum ajánlást** sem tétlen, sem terhelt kis (néhány tízezer soros) ParadeDB/Postgres példányra. A `paradedb.com/docs/start/go-to-production` oldal csak általánosságban fogalmaz:

> "give Postgres enough room to do the work" — (a WebFetch-összegzés szerint, az oldal explicit RAM-számot nem közöl)

**→ NINCS FORRÁS** konkrét RAM-minimumra (sem tétlen, sem terhelt esetre).

### 1.2 A `pg_search` saját memória-beállításai (hivatalos doksi)

Az `Index Creation` (index-építés) hivatalos oldal (`paradedb.com/docs/operate/performance-tuning/create-index`) szerint:

> "The default Postgres `maintenance_work_mem` value of `64MB` is quite conservative and can slow down parallel index builds."
>
> "A good starting value is `RAM / 16` and at least `64MB` per parallel indexing worker."
>
> "Each worker is required to have at least `15MB` memory. If `maintenance_work_mem` is set too low, an error will be returned."

A `Write Throughput` (írási teljesítmény) hivatalos oldal (`paradedb.com/docs/operate/performance-tuning/writes`) szerint:

> `work_mem` — "controls how much memory to allocate to a single `INSERT`/`UPDATE`/`COPY` statement" — minimum 15 MB szükséges a ParadeDB index-írásokhoz, ajánlott kiindulási érték: `(RAM - shared_buffers) / (3 * max_connections)`.

Ugyanez az oldal említi a `paradedb.global_mutable_segment_rows` beállítást (globális "mutable segment" sorpuffer-méret; alapértéke `-1`, ami azt jelenti, hogy a globális beállítást figyelmen kívül hagyja, és a per-index alapértelmezés (`1000`) érvényesül) — ez befolyásolja az olvasás közbeni memóriahasználatot.

A `Configuration Reference` hivatalos oldal (`paradedb.com/docs/reference/configuration`) az alábbi, memóriához köthető beállítást sorolja fel:

> `paradedb.mpp_queue_size` — alapérték `8MB` — "Per-inbox ring size for MPP shuffles. Accepts Postgres byte units."

és megerősíti az általános Postgres-paramétereket:

> `maintenance_work_mem` — "Index builds and index maintenance. Each parallel worker needs at least 15MB."
> `work_mem` — "Query execution memory; ParadeDB clamps the effective Tantivy budget internally."

**Ellentmondó/eltérő adat (nem hivatalos ParadeDB-forrás):** a Neon (harmadik fél, felhő-Postgres szolgáltató) saját `pg_search`-dokumentációja (`neon.com/docs/extensions/pg_search`, T2) más GUC-neveket ad meg, amelyeket a fenti hivatalos ParadeDB oldalakon nem találtam:

> `paradedb.create_index_memory_budget` — "per indexing thread before writing index segments to disk" — alapérték `1024 MB`.
> `paradedb.create_index_parallelism` — "Controls the number of threads used during CREATE INDEX" — alapérték `0` (automatikus).
> `paradedb.statement_memory_budget` — "memory per indexing thread before writing to disk" — alapérték `1024 MB`, egysoros frissítésekhez 15 MB ajánlott.

Ezt a három GUC-ot **két független ParadeDB-hivatalos oldalon sem sikerült megerősítenem** (sem a `writes`, sem a `reference/configuration` oldalon nem szerepelnek) — lásd az Ellentmondások szakaszt.

## 2. Mentés és visszaállítás

### 2.1 `pg_dump`/`pg_restore` és a BM25 index

A hivatalos Postgres-dokumentáció (`postgresql.org/docs/current/app-pgdump.html`) szerint az indexek a dump "post-data" szakaszába kerülnek, **definícióként**, nem adatként:

> "Post-data items include definitions of indexes, triggers, rules, statistics for indexes, and constraints other than validated check and not-null constraints."

Ez azt jelenti, hogy — mint minden Postgres-indexnél — a `CREATE INDEX ... USING bm25 ...` parancs kerül a dumpba, amit visszaállításkor a szerver újra lefuttat, azaz az indexet a táblaadatokból **újraépíti**, nem az index bináris tartalmát tölti vissza. A restore-oldali indexépítés általános ajánlása (`postgresql.org/docs/current/backup-dump.html`):

> "After restoring a backup, it is wise to run ANALYZE on each database so the query optimizer has useful statistics"

**Fontos korlát:** ezt a mechanizmust **nem találtam ParadeDB-specifikusan, hivatalosan megerősítve** — sem a `pg_search` doksijában, sem a GitHub repóban nem szerepel kifejezett állítás arra, hogy "pg_dump/pg_restore a BM25 indexet újraépíti". Amit fentebb leírtam, az az általános Postgres-index-dump-mechanizmusból következik (minden egyéni access method, így a `bm25` is ezt az utat követi, mert a dump SQL-szintű, nem storage-szintű), de ez **levezetés, nem szó szerinti ParadeDB-forrás** → erre nézve **részleges NINCS FORRÁS** (a mechanizmus általános Postgres-szinten dokumentált, ParadeDB-specifikusan nem).

### 2.2 `pg_basebackup`, PITR és a WAL-naplózás kérdése

A hivatalos Postgres-dokumentáció (`postgresql.org/docs/current/app-pgbasebackup.html`) szerint:

> "When used to take a full backup, it makes an exact copy of the database cluster's files."
>
> "The backup will include all files in the data directory and tablespaces, including the configuration files and any additional files placed in the directory by third parties, except certain temporary files managed by PostgreSQL and operating system files."
>
> "Backups are always taken of the entire database cluster; it is not possible to back up individual databases or database objects."
>
> a mentés "can be used both for point-in-time recovery (see Section 25.3) and as the starting point for a log-shipping or streaming-replication standby server."

Ez a mechanizmus tehát **fájlszintű**, és csak azt menti el, ami az adatkönyvtárban ténylegesen ott van a Postgres saját blokktárolójában (ún. "managed" fájlok). A kérdés emiatt az, hogy a BM25 index **a Postgres blokktárolójának része-e**.

**Ez időben változott, és a ParadeDB blogja ezt kifejezetten dokumentálja.** A "A New Postgres Block Storage Layout for Full Text Search" c. hivatalos blogbejegyzés (`paradedb.com/blog/block-storage-part-one`, dátum: 2025. január 16.) szerint korábban:

> "[pg_search] operated outside of block storage. This means that the extension created files which were not managed by Postgres."

A blokktárolóra való átállás — a bejegyzés szerint — az alábbiakat tette lehetővé:

> "Postgres write-ahead log (WAL) integration, which is necessary for physical replication" és "Crash and point-in-time recovery."

Ezt megerősíti a GitHub-os `v0.24.0` kiadási jegyzék (`github.com/paradedb/paradedb/releases/tag/v0.24.0`, dátum a release-oldalon "03 Jun", az év a lekérésben nem jelent meg egyértelműen, feltehetően 2024 — **erre nézve NINCS pontos, megerősített forrásom**):

> "feat: Crash recovery via WAL by @rebasedming in #4901"
> "docs: remove WAL/durability caveats by @rebasedming in #5091"

Vagyis: **a `v0.24.0` előtti verziókban a BM25 index dokumentáltan NEM volt WAL-naplózott**, és a hivatalos doksi maga is korábbi "WAL/durability caveats"-ekről (WAL/tartóssági fenntartásokról) beszél, amelyeket ez a kiadás távolított el.

**Ugyanakkor egy 2025. novemberi hivatalos GitHub-vita ezt élesen árnyalja / ellentmond neki.** A `github.com/orgs/paradedb/discussions/3521` vitában a ParadeDB fejlesztője, philippemnoel, 2025. november 11-én ezt írja:

> "The usage of streaming/read replicas has always been enterprise-only, as per: https://docs.paradedb.com/deploy/enterprise."

A vita szerint a Community-kiadásban a standby-ról történő BM25-olvasás hibaüzenete kifejezetten ezt mondja:

> "Serving reads from a standby requires write-ahead log (WAL) integration, which is supported on ParadeDB Enterprise, not ParadeDB Community."

Ezt a hivatalos `docs.paradedb.com/deploy/enterprise` feature-táblázat is alátámasztja: ott a "Read Replica Support" és a "High Availability Support" sorok Community-nál ❌, Enterprise-nál ✅ jelölést kapnak. A táblázat lábjegyzete ugyanakkor ezt írja:

> "ParadeDB Community supports physical/logical replication, crash recovery, etc. for heap tables and other Postgres indexes like B-Tree."

Vagyis a lábjegyzet kifejezetten a *heap táblákra és más (pl. B-Tree) Postgres-indexekre* korlátozza a Community fizikai replikáció / crash recovery garanciáját — a BM25 indexre nézve nem ad kifejezett, azonos erősségű állítást. **→ Ez lásd az Ellentmondások szakaszban.**

A hivatalos self-hosted HA-konfigurációs oldal (`docs.paradedb.com/deploy/self-hosted/high-availability/configuration`) szerint:

> "ParadeDB supports backups to cloud object stores (e.g. S3, GCS, etc.) and point-in-time-recovery via Barman."

Ez az oldal **nem jelzi**, hogy ez a képesség Community vagy Enterprise kiadáshoz kötött-e — ami újabb ellentmondás-forrás a fenti Enterprise-only táblázattal szemben.

**Két független forrás megerősítve** arra, hogy a BM25 index WAL-integrációja/PITR-kompatibilitása verzió- és kiadás-függő, korlátozott kérdés: (1) a hivatalos blog (block-storage-part-one) és (2) a hivatalos GitHub-vita (#3521) + a hivatalos Enterprise-oldal együtt. Az, hogy pontosan *melyik* funkció (naplózás vs. standby-olvasás) melyik kiadásban érhető el, a forrásokból **nem old fel egyértelműen** — lásd Ellentmondások.

### 2.3 Törölt adat a fizikai mentésben (holt tuple-ök) — hivatalos Postgres-forrás

A hivatalos Postgres-dokumentáció (`postgresql.org/docs/current/routine-vacuuming.html`) szerint:

> "In PostgreSQL, an UPDATE or DELETE of a row does not immediately remove the old version of the row. This approach is necessary to gain the benefits of multiversion concurrency control (MVCC, see Chapter 13): the row version must not be deleted while it is still potentially visible to other transactions. But eventually, an outdated or deleted row version is no longer of interest to any transaction. The space it occupies must then be reclaimed for reuse by new rows, to avoid unbounded growth of disk space requirements. This is done by running VACUUM."
>
> "The standard form of VACUUM removes dead row versions in tables and indexes and marks the space available for future reuse. However, it will not return the space to the operating system, except in the special case where one or more pages at the end of a table become entirely free and an exclusive table lock can be easily obtained."

Mivel a `pg_basebackup` — mint fentebb idézve — a fájlrendszer szintjén, "exact copy"-ként másolja a klasztert, és a holt tuple-ök VACUUM előtt **fizikailag a fájlokban maradnak**, ebből következik (általános Postgres-logika, nem ParadeDB-specifikus), hogy egy VACUUM előtt készült fizikai mentés a holt tuple-öket is tartalmazza. Ezt közvetetten támasztja alá a `continuous-archiving.html` oldal is:

> "We do not need a perfectly consistent file system backup as the starting point. Any internal inconsistency in the backup will be corrected by log replay (this is not significantly different from what happens during crash recovery)."

## 3. Verziófrissítés

### 3.1 `ALTER EXTENSION ... UPDATE` és a REINDEX kérdése

A hivatalos `Upgrading ParadeDB` oldal (`docs.paradedb.com/deploy/upgrading`) szerint a frissítés után minden adatbázisban, ahol a `pg_search` telepítve van, le kell futtatni:

> `ALTER EXTENSION pg_search UPDATE TO '0.25.3';`

és ez a lépés

> "required regardless of the environment that ParadeDB is installed in (Helm, Docker, or self-managed Postgres)."

Az oldal a verzióellenőrzésre két parancsot ad meg:
- `SELECT extversion FROM pg_extension WHERE extname = 'pg_search';`
- `SELECT * FROM paradedb.version_info();`

**Az oldal a REINDEX szükségességéről egyáltalán nem tesz említést** — sem pozitív, sem negatív irányban. **→ NINCS FORRÁS** arra nézve, hogy `ALTER EXTENSION pg_search UPDATE` után szükséges-e REINDEX.

### 3.2 Postgres-főverzió-váltás (`pg_upgrade`) a `pg_search` bővítménnyel

A ParadeDB hivatalos frissítési dokumentációja **nem tárgyalja** a `pg_upgrade`-et vagy a Postgres-főverzió-váltást a `pg_search` vonatkozásában — ezt közvetlen oldal-lekéréssel is megerősítettem (az oldal kizárólag a kiterjesztés-verzió frissítéséről szól, Postgres-verzióváltásról nem). Több célzott keresés (GitHub, hivatalos doksi) sem hozott ParadeDB-specifikus `pg_upgrade`-útmutatót vagy figyelmeztetést.

**→ NINCS FORRÁS** ParadeDB-specifikus `pg_upgrade` útmutatóra.

Háttérként (nem ParadeDB-specifikus, csak általános Postgres-kontextus) a hivatalos `pg_upgrade` dokumentáció (`postgresql.org/docs/current/pgupgrade.html`) az 5. lépésben (Install extension shared object files) általánosan kimondja:

> "Many extensions and custom modules, whether from contrib or another source, use shared object files (or DLLs)... If the old cluster used these, shared object files matching the new server binary must be installed in the new cluster, usually via operating system commands. Do not load the schema definitions, e.g., CREATE EXTENSION pgcrypto, because these will be duplicated from the old cluster. If extension updates are available, pg_upgrade will report this and create a script that can be run later to update them."

Ez a szöveg minden bővítményre (így elvileg a `pg_search`-re is) érvényes lenne, de a `bm25` egyéni index access method `pg_upgrade` alatti viselkedéséről (pl. automatikus REINDEX-szkript generálásáról) a Postgres-doksi **kifejezetten csak "reindex cases"-t említ általánosságban**, custom AM-específikusan nem részletezi.

### 3.3 Ismert frissítési buktatók (GitHub issue-k)

Több, a témához kapcsolódó GitHub-issue címét megtaláltam keresésben (`#1407` "pg_search index recreation not working properly", `#713` "bm25 index is not getting deleted properly", `#1047` beszúrási hiba indexelt táblán, `#1207` "Slow degradation of index"), **de mind a négy issue oldala a lekéréskor "This issue has been deleted" üzenetet adott vissza** — tartalmuk emiatt **nem idézhető és nem ellenőrizhető**. Ezt jelzem, nem pótlom.

Egy hozzáférhető, lezárt issue (`github.com/paradedb/paradedb/issues/2211`, "BM25 index creation stuck") arról számol be, hogy egy ~2,3 GB / ~130 000 soros táblán az indexépítés több mint 3 órán át lefagyott, miközben egy hasonló, kisebb (~500 MB / 31 000 sor) adatbázison 1 percen belül lefutott; a felhasználó korábban a `v0.10.0` verzióban lockolási problémákról számolt be, amelyeket a `v0.15.2`-re való frissítés nem oldott meg teljesen.

Két friss (2026. szeptember 17-én nyitott, ugyanaznap zárt), hivatalos GitHub-issue VACUUM-hoz kapcsolódó, index-integritást érintő hibát dokumentál:

- `#6375` — "Join scan drops one user's rows after a HOT update and VACUUM on a churned heap": "After a handful of updates and VACUUMs on the qgen tables, the join scan drops every row of one users id that PostgreSQL returns." (Postgres 15.15, ParadeDB main branch, commit `85d6ca06b`, bejelentő: mdashti)
- `#6374` — "Parallel top-k scan segfaults after two updates of one row in a mutable segment": "A NOT IN subquery that the planner runs as a parallel top-k scan crashes the backend with SIGSEGV" — három együttes feltétel mellett (parallel worker, heap filter, egy sor kétszeri frissítése egy "mutable segment"-ben). Ugyanaz a verzió/commit, ugyanaz a bejelentő.

Mindkettő CLOSED állapotú, gyors javítást jelez, de egyúttal azt is mutatja, hogy a VACUUM/HOT-update és a BM25 belső szegmensszerkezete közötti interakció aktívan hibalehetőség-forrás — legalábbis a "main" fejlesztői ágon, 2026 szeptemberében.

## 4. Karbantartás

### 4.1 VACUUM/autovacuum hatása a BM25 indexre

A hivatalos `Index Size` oldal (`docs.paradedb.com/documentation/configuration/index_size`) szerint:

> "if a table were never vacuumed, the BM25 index size would grow unbounded as rows are updated or additional rows are inserted."
>
> "Vacuums on their own do not decrease the index size — they only mark space for reuse."
>
> "If the index has already grown too large as a result of failure to vacuum, the only way to shrink the index size is to drop the index or REINDEX."

Az oldal javaslata a méret kordában tartására: az autovacuum-beállítások finomhangolása, vagy nagy írási műveletek közötti manuális `VACUUM`.

### 4.2 Szegmensek összefésülése (merge)

A hivatalos `Architecture` oldal (`docs.paradedb.com/welcome/architecture`) LSM-fa-jellegű felépítést ír le:

> "data is gradually pushed down into lower levels through a process called merging or compaction"

és megerősíti, hogy a szegmensek egyszer lemezre írva **immutábilisak** ("immutable once flushed to disk"). Ezt közvetve megerősíti a hivatalos blogbejegyzés is (`paradedb.com/blog/lsm-trees-in-postgres`), amely az írási útvonalat LSM-faként írja le, és kifejezetten tárgyalja, hogy a VACUUM/olvasási konzisztencia miatt egy standby-on "a tuple is VACUUMed from the standby prematurely" probléma léphet fel, amit a `hot_standby_feedback` beállítással (a standby elküldi a legkisebb `xmin`-t a primary felé, hogy az okosabb döntést hozhasson a takarításról) kezelnek.

**Dedikált, felhasználó által kézzel indítható "merge" parancsot vagy önálló doksi-fejezetet nem találtam** — a rendelkezésre álló hivatalos leírás szerint a szegmens-összefésülés a háttérben, automatikusan zajlik, a VACUUM/autovacuum és az írási útvonal (LSM-szerű "compaction") részeként. **→ NINCS FORRÁS** külön, kézi merge-parancsra vagy annak ütemezhetőségére.

### 4.3 Index-korrupció észlelése és javítása

A hivatalos `Verify Index Integrity` oldal (két elérési úton is megtalálva: `paradedb.com/docs/operate/index-maintenance/verify-index` és a régebbi `paradedb.com/docs/documentation/indexing/verify-index`, tartalmuk konzisztens) szerint:

> "ParadeDB provides amcheck-style index verification functions to detect corruption and validate the structural integrity of ParadeDB indexes."

A `pdb.verify_index` függvény egy táblát ad vissza (`check_name`, `passed`, `details` oszlopokkal), és az alábbiakat ellenőrzi: index-séma érvényessége, index olvashatósága, szegmens-ellenőrzőösszegek (checksums), szegmens-metaadatok, valamint — opcionálisan (`heapallindexed`) — heap-referencia integritás. A dokumentáció szerint ez hasznos:

> "useful for proactive corruption detection before issues become critical" és "validating index health after hardware failures."

**Javítási (repair) eljárást a dokumentáció nem ír le** — kizárólag detekcióról/validációról szól, arról nem, hogy talált korrupció esetén mi a hivatalosan javasolt lépés (feltételezhető, hogy REINDEX, de erre a `verify-index` oldal **nem hivatkozik kifejezetten** — → NINCS FORRÁS a korrupció-javítás hivatalos lépésére).

**Miért kellett saját "amcheck-stílusú" függvényt írniuk:** a hivatalos Postgres `amcheck` dokumentáció (`postgresql.org/docs/current/amcheck.html`) csak az alábbi function-öket sorolja fel:

> `bt_index_check(...)` és `bt_index_parent_check(...)` — B-Tree indexekhez
> `gin_index_check(...)` — GIN indexekhez

Egyéni (harmadik féltől származó) index access method-okra (mint a `bm25`) vonatkozó natív `amcheck`-támogatást a dokumentáció **nem említ** — ez megmagyarázza, miért kellett a ParadeDB-nek saját, "amcheck-stílusú" ellenőrző függvényt implementálnia a natív `amcheck` kiterjesztése/használata helyett.

## 5. Telepítés macOS-en és Linuxon

### 5.1 Hivatalos telepítési utak

A hivatalos `Extension` (self-hosted telepítési) oldal (`docs.paradedb.com/deploy/self-hosted/extension`) szerint előre fordított binárisok érhetők el:

- **Debian**: 12 (Bookworm), 13 (Trixie)
- **Ubuntu**: 24.04 (Noble), 26.04 (Resolute)
- **macOS**: 15 (Sequoia), 26 (Tahoe), valamint macOS Postgres.app-on keresztül (PostgreSQL 18)
- **Red Hat Enterprise Linux**: 9, 10

Csomagformátumok: ".deb" (Debian/Ubuntu), ".rpm" (RHEL), ".pkg" (macOS). Architektúrák: "amd64, arm64" (Debian/Ubuntu), "x86_64, aarch64" (RHEL), **kizárólag "arm64" macOS-en** (azaz Apple Silicon — Intel Mac-re nincs hivatalos csomag ezen az oldalon).

Példa telepítőparancs (Ubuntu 26.04-hez):

```
curl -L "https://github.com/paradedb/paradedb/releases/download/v0.25.3/postgresql-18-pg-search_0.25.3-1PARADEDB-resolute_amd64.deb" -o /tmp/pg_search.deb
sudo apt-get install -y /tmp/*.deb
```

### 5.2 Docker

A hivatalos gyorsindítási oldal (`docs.paradedb.com/documentation/getting-started/install`) szerint:

> "The fastest way to install ParadeDB is by pulling the ParadeDB Docker image and running it locally."

A hivatalos Docker Hub oldal (`hub.docker.com/r/paradedb/paradedb/tags`) szerint a képek **mindkét architektúrában** elérhetők, minden verzió-tag alatt:

> "linux/amd64" és "linux/arm64" (pl. a legfrissebb tagnél kb. 350 MB / 339 MB méretben), beleértve a Postgres-verzió-specifikus variánsokat (pg15, pg16, pg17, pg18) is.

Ez megerősíti, hogy a Docker-út **Apple Silicon (arm64) Mac-en natívan** működik.

### 5.3 Homebrew

**Hivatalos Homebrew-csomagot (tap/formula) nem találtam.** A `docs.paradedb.com/deploy/self-hosted/extension` oldal kifejezetten csak .deb/.rpm/.pkg formátumokat sorol fel, Homebrew-t nem. Ezt megerősíti a nyitott, hivatalos GitHub-issue (`github.com/paradedb/paradedb/issues/1019`, cím: "Publish ParadeDB extensions to APT, Homebrew, PGXN, and Yum"), amely **jelenleg is OPEN** státuszú. A vitában philippemnoel (ParadeDB) az APT/YUM-terjesztést azzal indokolta elhalasztottnak, hogy

> a szolgáltatók "don't have the ability to retain a meaningful history of packages"

és PGDG-integrációra várnak (Christoph Berg munkája a `pgrx`/Debian buildfarm-kompatibilitáson). A Homebrew-specifikus státuszra/ütemtervre **nem találtam konkrét, dátumozott hivatalos nyilatkozatot** a hozzáférhető issue-tartalomban. **→ NINCS FORRÁS** hivatalos Homebrew-csomagra vagy annak határidejére.

### 5.4 Beágyazott / egyfájlos mód

Explicit, negatív hivatalos állítást ("nem támogatjuk az egyfájlos/beágyazott módot") **nem találtam**, de a hivatalos "Introduction" oldal (`paradedb.com/docs/start/introduction`) egyértelműen, pozitív állításként ezt írja le, amiből ez következik:

> "This means ParadeDB is vanilla Postgres with an extension installed, not a Postgres fork or sidecar process."
>
> "The index ships as pg_search, a standard Postgres extension."

Ez azt jelenti, hogy a `pg_search`/ParadeDB **mindig egy futó, teljes Postgres-szerver-folyamatot** igényel (megosztott memóriával, WAL-al, saját adatkönyvtárral) — nincs olyan hivatalosan dokumentált mód, amelyben a motor SQLite-hoz hasonlóan egyetlen fájlként, szerverfolyamat nélkül, egy alkalmazásba beágyazva futna. **A tiltás explicit kimondása helyett ez csak levezetés a pozitív leírásból** → részben **NINCS FORRÁS** a kifejezett negatív állításra, csak közvetett bizonyíték.

## Ellentmondások

1. **WAL-integráció / standby-olvasás Community vs. Enterprise.** A hivatalos blog (`block-storage-part-one`, 2025.01.16.) általánosságban azt állítja, hogy a blokktárolóra váltás WAL-integrációt és "Crash and point-in-time recovery"-t hozott a `pg_search` számára. Egy hivatalos GitHub-vita (`discussions/3521`, 2025.11.11., philippemnoel) viszont kimondja, hogy a "streaming/read replicas" használata "always been enterprise-only", és a Community-kiadás hibaüzenete szerint a standby-ról való olvasáshoz szükséges WAL-integráció "is supported on ParadeDB Enterprise, not ParadeDB Community." A hivatalos Enterprise-táblázat lábjegyzete pedig a Community fizikai replikáció/crash recovery garanciáját kifejezetten "heap tables and other Postgres indexes like B-Tree"-re korlátozza, a BM25-re nem tesz azonos erősségű állítást. A három forrás nem old fel egyértelmű, konzisztens képet: nem világos a dokumentációból, hogy pontosan mely WAL-képesség (naplózás vs. naplóból való visszajátszás/olvasás standby-on) melyik kiadásban (Community/Enterprise) érhető el.

2. **Self-hosted HA/backup-doksi vs. Enterprise-only táblázat.** A `docs.paradedb.com/deploy/self-hosted/high-availability/configuration` oldal Community/Enterprise megkötés nélkül írja le a Barman-alapú felhő-mentést és PITR-t, miközben a hivatalos Enterprise-összehasonlító táblázat a "High Availability Support"-ot Community-nál ❌-nak jelöli. A két hivatalos oldal nincs egymással explicit módon összekötve/tisztázva.

3. **`pg_search` memória-GUC-nevek.** A Neon (harmadik fél) `pg_search`-dokumentációja (T2) a `paradedb.statement_memory_budget`, `paradedb.create_index_memory_budget` és `paradedb.create_index_parallelism` GUC-okat írja le konkrét alapértékekkel (1024 MB, 1024 MB, 0). A ParadeDB saját, jelenlegi hivatalos "Write Throughput" és "Configuration Reference" oldalai ezeket a GUC-neveket **nem tartalmazzák**, helyettük `work_mem`-et és `paradedb.global_mutable_segment_rows`-t dokumentálnak. Nem tudtam eldönteni (és nem is feladatom eldönteni), hogy ez verzió-eltérés, elnevezés-változás vagy a Neon-doksi elavultsága miatt van-e — a forrásokat ütköztetve hagyom.

## Amire NINCS forrás

- Hivatalos, számszerű RAM-minimum (tétlen vagy terhelt) egy kis (néhány tízezer soros) ParadeDB/Postgres példányra.
- ParadeDB-specifikus, explicit megerősítés arra, hogy `pg_dump`/`pg_restore` a BM25 indexet ténylegesen újraépíti (csak az általános Postgres pg_dump/index-definíció-mechanizmusból vezethető le).
- Hivatalos állásfoglalás arról, hogy `ALTER EXTENSION pg_search UPDATE` után szükséges-e REINDEX.
- ParadeDB-specifikus `pg_upgrade` (Postgres-főverzió-váltás) útmutató vagy figyelmeztetés.
- Négy GitHub-issue (#1407, #713, #1047, #1207) tartalma — az oldalak törölve lettek, nem idézhetők.
- Dedikált, kézzel indítható "merge" (szegmens-összefésülés) parancs vagy annak ütemezési dokumentációja — csak automatikus, háttérben zajló "merging or compaction" leírás van.
- Hivatalos, kifejezett javítási (repair) lépés BM25-index-korrupció észlelése (`pdb.verify_index`) után.
- Hivatalos Homebrew-csomag (tap/formula) létezése vagy határideje — a téma egy 2024 óta nyitott GitHub-issue tárgya, konkrét dátum/ígéret nélkül.
- Kifejezett, negatív hivatalos állítás arra, hogy a ParadeDB/`pg_search` NEM támogat beágyazott/egyfájlos üzemmódot (csak közvetett, pozitív leírásból következik).
- A `v0.24.0` GitHub-kiadás pontos éve (a release-oldal "03 Jun" dátumot mutatott, évszám nélkül a lekérésben).



---

# SQ06 — Integráció a TypeScript / Bun / Drizzle / Better Auth stackkel

> **Módszertani megjegyzés (degradált mód).** A `anthropic-skills:deep-web-research` skillt betöltöttem, de ebben a futtatási környezetben nincs `Agent`/`Task` eszköz Sonnet-alügynökök indítására (a `ToolSearch("Agent subagent Task dispatch...")` hívás nem talált ilyen eszközt). A `_kozos.txt` előírása szerint ezért a skill "saját degradált módja szerint" dolgoztam: egyetlen szálon, szekvenciálisan végeztem a keresést (`WebSearch`/`WebFetch`, illetve `curl` a `raw.githubusercontent.com`-on és az `registry.npmjs.org`-on keresztül nyers forráskódért/verzióadatért), nem futott le a skill Opus-szintézis és Sonnet-verifikáció fázisa, és nem készült `.research/` evidence-vault. Minden állítást a jelen fájlban közvetlenül, forrás-idézettel dokumentálok; ahol nem sikerült második független forrást találni, azt kiírtam.

## Rövid válasz

A Drizzle ORM-nek van **hivatalos, ParadeDB által karbantartott** csomagja (`@paradedb/drizzle-paradedb`, MIT licenc), amely a `bm25`/`paradedb` indexet és a `@@@` (és rokon `&&&`, `|||`, `###`, `===`) operátorokat Drizzle `sql` sablon-literálokba csomagolt, típusos helper-függvényekként adja vissza — tehát technikailag nyers SQL-t generál, csak típusbiztos burkolattal; natív, beépített Drizzle-operátor nincs rá. Ez a csomag a Drizzle ORM és a drizzle-kit **1.0.0-rc.4** verzióját írja elő peer-dependencyként, miközben az npm registry szerint 2026. szeptember 21-én a Drizzle "latest" taggel jelölt stabil verziója még mindig **0.45.3** (drizzle-kit: 0.31.11) — a ParadeDB-integráció tehát csak a Drizzle 1.0 release candidate ágán működik. A Drizzle `index().using()` metódusa forráskód szerint tetszőleges string indexmetódust elfogad ("*You can always specify any string you want in the method*"), és a ParadeDB saját teszt-csomagja bizonyítottan helyesen generál `USING paradedb` migrációt a `drizzle-kit/api-postgres` `generateMigration` függvényével. Prisma-hoz csak egy hivatalos, de kifejezetten **"Not ready for public consumption"** WIP-repó létezik, Kysely-hez semmilyen hivatalos ParadeDB-anyagot nem találtam. A Drizzle natívan támogatja a `vector` oszloptípust és hat távolságfüggvényt (`l2Distance`, `l1Distance`, `innerProduct`, `cosineDistance`, `hammingDistance`, `jaccardDistance`), valamint a HNSW/ivfflat indexet `index().using('hnsw', col.op('vector_cosine_ops'))` formában. Bun beépített `Bun.sql`-je élő fejlesztés alatt álló, nyílt tracking issue-val rendelkező Postgres-kliens, amelynek hivatalos dokumentációjában **egyetlen említés sincs** pgvectorra vagy vektor-típusra; a Drizzle `bun sql` integrációja is még RC-csomagokat (`drizzle-orm@rc`) igényel. A Better Auth Drizzle adapterének van `provider: "pg"` Postgres-módja, de a Drizzle 1.0 RC-kompatibilitást csak a Better Auth **1.7 RC**-je oldotta meg (PR #9489), és külön, lezáratlan hibaosztály a Bun alatti CLI-generálás, ahol a `better-sqlite3` natív binding-je (amit a CLI providertől függetlenül behúz) Bunon nem töltődik be. Konkurens írásokra a ParadeDB "Guarantees" oldala azt állítja, hogy minden írás "respect Postgres' isolation levels", ám egy 2026. szeptemberi, még **nyitott** ParadeDB-issue és a hozzá tartozó, még **nem mergelt** PR bizonyítja, hogy a `pg_search` alap- és aggregált-scanjei nem vesznek SIREAD-zárat, ezért SERIALIZABLE izoláció mellett phantom write skew fordulhat elő — ez közvetlen ellentmondás a hivatalos garancia-oldallal. Integrációs teszteléshez a ParadeDB saját hivatalos Drizzle-csomagja **nem** testcontainers-t használ, hanem egy saját bash-szkripttel indított `paradedb/paradedb:<verzió>-pg<verzió>` Docker image-et; önálló, hivatalos ParadeDB testcontainers-modult nem találtam, de a Testcontainers hivatalos `pgvector` modulja (Node.js-ben is) bizonyítja, hogy a generikus `PostgreSQLContainer`/`PostgreSqlContainer` osztály tetszőleges Postgres-kompatibilis image-dzsel (image-tag string, ill. Java alatt `asCompatibleSubstituteFor("postgres")`) használható — ez analóg mintaként alkalmazható lenne a ParadeDB image-re is, de erre magára nincs hivatalos forrás.

---

## 1. Drizzle ORM és a `pg_search`

### 1.1 Hivatalos csomag létezik

A `@paradedb/drizzle-paradedb` GitHub-repó README-je (nyers, `raw.githubusercontent.com`-ról lekérve):

> „The official [Drizzle](https://orm.drizzle.team/) integration for [ParadeDB](https://paradedb.com) (powered by the [`pg_search`](https://github.com/paradedb/paradedb) Postgres extension). Follow the [getting started guide](https://www.paradedb.com/docs/start/connect-your-app#drizzle) to begin.”
(https://github.com/paradedb/drizzle-paradedb, ill. https://raw.githubusercontent.com/paradedb/drizzle-paradedb/main/README.md)

Az npm `package.json` (nyersen lekérve) szerint:

> `"name": "@paradedb/drizzle-paradedb"`, `"version": "0.5.0"`, `"description": "Official ParadeDB integration for Drizzle"`, `"license": "MIT"`, `"author": "ParadeDB, Inc."`
(https://raw.githubusercontent.com/paradedb/drizzle-paradedb/main/package.json)

Kompatibilitási táblázat a README-ből:

> „| Component | Supported | | Node | 22.12+ | | Drizzle | 1.0+ | | ParadeDB | 0.25.0+ | | PostgreSQL | 15+ (with the ParadeDB pg_search extension) | | pgvector | Required for vector search (included in the ParadeDB Docker image) |”
(uo.)

A hivatalos ParadeDB indexelési dokumentáció (`docs.paradedb.com/documentation/indexing/create-index`) az ORM-ek közül **csak** ezeket sorolja fel: Drizzle, Django, SQLAlchemy, Rails, EF Core. **Prisma és Kysely nem szerepel** ezen az oldalon.

**Prisma:** külön kereséssel találtam egy `paradedb/prisma-paradedb` GitHub-repót. Annak README-je:

> „WIP - Starter code from the Prisma team for integrating ParadeDB with Prisma Next. Not ready for public consumption.”
(https://github.com/paradedb/prisma-paradedb)

Tehát létezik hivatalos, de kifejezetten kísérleti/nem-publikus státuszú kezdemény — ez **nem** hasonlítható a Drizzle-csomag érettségéhez.

**Kysely:** semmilyen hivatalos ParadeDB-Kysely anyagot (repó, doksi-oldal, blogbejegyzés) nem találtam a keresés során. **NINCS FORRÁS.**

### 1.2 `USING bm25` vs. `USING paradedb`, és a `@@@` operátor

A hivatalos „Create an Index” oldal szerint:

> „USING bm25 remains supported as a backwards-compatible alias for USING paradedb.”
(https://docs.paradedb.com/documentation/indexing/create-index)

A hivatalos operátor-referencia oldal (`paradedb.com/docs/reference/operators-and-functions`) a `@@@` operátort így írja le:

> „`@@@` — General ParadeDB predicate” — `pdb.parse(...)`, `pdb.all()` vagy „builder” függvényekkel használva, ahol „text is parsed with ParadeDB's query parser. Query builders return `pdb.query`.”

Ugyanez az oldal a rokon operátorokat is definiálja: `|||` = „Tokenized text match, any token” (`pdb.match_disjunction`), `&&&` = „Tokenized text match, all tokens” (`pdb.match_conjunction`), `===` = „Exact token match or token set” (`pdb.term`/`pdb.term_set`), `###` = „Phrase match” (`pdb.phrase`/`pdb.phrase_array`).
(https://www.paradedb.com/docs/reference/operators-and-functions)

A `@paradedb/drizzle-paradedb` csomag `src/search.ts` forrásfájlja (nyersen lekérve, elsődleges forrás: a tényleges kiadott forráskód) **konkrétan megmutatja**, hogyan implementálja ezeket Drizzle-lel — mind `sql` sablon-literállal, típusos wrapperbe csomagolva, NEM natív Drizzle-operátorként:

```ts
export function matchAll(column: SQLWrapper, value: SearchValue): SQL<boolean> {
  return sql<boolean>`${column} &&& ${renderSearchValue(value)}`;
}
export function matchAny(column: SQLWrapper, value: SearchValue): SQL<boolean> {
  return sql<boolean>`${column} ||| ${renderSearchValue(value)}`;
}
export function phrase(column: SQLWrapper, value: SearchValue): SQL<boolean> {
  return sql<boolean>`${column} ### ${renderSearchValue(value)}`;
}
export function term(column: SQLWrapper, value: SearchValue): SQL<boolean> {
  return sql<boolean>`${column} === ${renderSearchValue(value)}`;
}
export function proximity(column: SQLWrapper, value: ProximityValue): SQL<boolean> {
  return sql<boolean>`${column} @@@ ${value}`;
}
export function parse(column: SQLWrapper, query: string, options: ParseOptions = {}): SQL<boolean> {
  ...
  return sql<boolean>`${column} @@@ pdb.parse(${sql.join(args, sql`, `)})`;
}
```
(https://raw.githubusercontent.com/paradedb/drizzle-paradedb/main/src/search.ts — teljes fájl letöltve és ellenőrizve)

Vagyis: **a `@@@` (és társai) nincs beépítve a Drizzle ORM magjába**; a ParadeDB hivatalos csomagja adja a típusos wrappert `sql` template literál fölé — funkcionálisan ez "nyers SQL, típusos burokban", nem natív Drizzle query-builder operátor.

Ugyanez a fájl azt is megmutatja, hogy a `cosineDistance`, `innerProduct`, `l2Distance` függvényeket egyszerűen **újraexportálja** a `drizzle-orm` csomagból:

> `export { cosineDistance, innerProduct, l2Distance } from "drizzle-orm";`
(uo.)

### 1.3 Index-definíció Drizzle-sémában (`paradedbIndex`)

A csomag `src/indexing.ts` forrása (nyersen lekérve):

```ts
export function paradedbIndex(
  name?: string,
  options: ParadedbIndexOptions = {},
): { on(keyField: PgColumn, ...fields: IndexField[]): IndexBuilder } {
  return {
    on(keyField, ...fields) {
      const withOptions: Record<string, string> = { key_field: keyField.name };
      ...
      return index(name)
        .using("paradedb", keyField, ...fields)
        .with(withOptions);
    },
  };
}
```
(https://raw.githubusercontent.com/paradedb/drizzle-paradedb/main/src/indexing.ts)

Ez bizonyítja, hogy a `paradedbIndex(...).on(...)` **a Drizzle natív `index()` builder `.using("paradedb", ...)` hívására épül** — azaz a ParadeDB-csomag maga is a Drizzle core generikus index-mechanizmusát használja, nem egy külön API-t.

### 1.4 Drizzle core: tetszőleges index-metódus (nem csak GIN/GIST)

A Drizzle ORM saját forráskódjában (`drizzle-orm/src/pg-core/indexes.ts`, nyersen lekérve a hivatalos GitHub repóból):

```ts
export type PgIndexMethod = 'btree' | 'hash' | 'gist' | 'spgist' | 'gin' | 'brin' | 'hnsw' | 'ivfflat' | (string & {});
...
/**
 * Specify what index method to use. Choices are `btree`, `hash`, `gist`, `spgist`, `gin`, `brin`, or user-installed access methods like `bloom`. The default method is `btree.
 *
 * If you have the `pg_vector` extension installed in your database, you can use the `hnsw` and `ivfflat` options, which are predefined types.
 *
 * **You can always specify any string you want in the method, in case Drizzle doesn't have it natively in its types**
 */
using(method: PgIndexMethod, ...columns): IndexBuilder { ... }
```
(https://raw.githubusercontent.com/drizzle-team/drizzle-orm/main/drizzle-orm/src/pg-core/indexes.ts)

A hivatalos dokumentáció (`orm.drizzle.team/docs/indexes-constraints`) is mutat `.using()`-példát, bár ott csak a `'btree'` metódusra van kódpélda:

```
index('name').using('btree', table.column1.asc(), sql`lower(${table.column2})`, table.column1.op('text_ops'))
```
(https://orm.drizzle.team/docs/indexes-constraints)

**Tehát: a Drizzle ORM natívan, TypeScript-szinten is elfogad tetszőleges string index-metódust** (a `(string & {})` union-tag pontosan ezt a "engedd meg bármelyik stringet, de listázd ki az ismerteket IDE-autocomplete-hez" mintát valósítja meg) — ez közvetlen, elsődleges forrásból (a tényleges TypeScript definíció) igazolt válasz arra, hogy a `USING bm25`/`USING paradedb` szintaktikailag elfogadott-e Drizzle-sémában: **igen**.

### 1.5 drizzle-kit: hogyan kezeli a migrációkat egyedi index-metódussal — bizonyított teszt

A `@paradedb/drizzle-paradedb` saját `tests/indexing.test.ts` fájlja (nyersen lekérve, a csomag hivatalos, futtatott vitest-tesztje) közvetlenül a `drizzle-kit/api-postgres` (`generateDrizzleJson`, `generateMigration`) hívásával generál migrációt egy `paradedbIndex(...)`-et tartalmazó táblára, és a várt SQL-t assert-eli:

```ts
import { generateDrizzleJson, generateMigration } from "drizzle-kit/api-postgres";
...
const prev = await generateDrizzleJson({});
const cur = await generateDrizzleJson({ products });
const statements = await generateMigration(prev, cur);

expect(statements[1]).toStrictEqual(
  `CREATE INDEX "indexing_test_products_idx" ON "indexing_test_products" USING paradedb ("id",(("description")::pdb.ngram(3,3,'positions=true')),...) WITH (key_field=id) WHERE "rating" > 0;`,
);
```
(https://raw.githubusercontent.com/paradedb/drizzle-paradedb/main/tests/indexing.test.ts)

Ez **egyetlen, de közvetlen, futtatható forrásból** (a hivatalos csomag saját tesztkódja) igazolja, hogy a `drizzle-kit@1.0.0-rc.4` `generateMigration` API-ja helyesen, `WITH`-opciókkal és operátor-osztályokkal együtt generálja a `USING paradedb` SQL-t. **Második, független forrást erre a konkrét viselkedésre (nem a saját tesztkódjukon kívül) nem találtam** — ezt itt jelzem, a módszertan előírása szerint.

### 1.6 Korábbi drizzle-kit hiba egyedi index-operátorokkal (`generate` vs `push`)

A `drizzle-team/drizzle-orm` GitHub repóban:

> **Cím:** „[BUG]: `drizzle-kit generate` ignores index operators” — **bejelentve:** 2024. szeptember 9. — **állapot:** Closed (Issue #2935)
> „`index().using('gin', table.name.op('gin_trgm_ops'))`” esetén a várt SQL `CREATE INDEX ... USING gin ("name" gin_trgm_ops);`, a tényleges viszont `CREATE INDEX ... USING gin ("name");` (az operátor-osztály lemarad). A `drizzle-kit push` viszont helyesen működik — csak a `generate` hibás volt.
(https://github.com/drizzle-team/drizzle-orm/issues/2935)

Ez a bug **operátor-osztályra** (`.op(...)`) vonatkozott, nem magára a `USING <metódus>` névre, és 2024-es, lezárt issue — a fenti 1.5 pontban idézett, 2026-os saját ParadeDB-teszt szerint a `paradedb` metódus és a hozzá tartozó `WITH`-opciók már helyesen generálódnak a jelenlegi (RC) drizzle-kit verzióval. **Második, független megerősítést a #2935 hiba pontos javítási verziójára nem találtam** (a lezárás dátuma/verziója a lekért tartalomban nem szerepelt egyértelműen).

### 1.7 Verzió-státusz: a ParadeDB-integráció csak Drizzle/drizzle-kit *release candidate* ágon fut

Az npm registry API közvetlen lekérdezése (`registry.npmjs.org/drizzle-orm`, `registry.npmjs.org/drizzle-kit`), amely elsődleges, gépileg generált forrás:

```
drizzle-orm dist-tags: "latest": "0.45.3", "rc": "1.0.0-rc.4", "rc5": "1.0.0-rc.5-5935859"
  time["0.45.3"] (a "latest" publikálási ideje) = 2026-09-21T10:06:39.969Z
drizzle-kit dist-tags: "latest": "0.31.11", "rc": "1.0.0-rc.4", "rc5": "1.0.0-rc.5-5935859"
  time["0.31.11"] = 2026-09-21T10:06:58.727Z
```
(https://registry.npmjs.org/drizzle-orm és https://registry.npmjs.org/drizzle-kit, lekérve 2026-09-22)

A `@paradedb/drizzle-paradedb` `package.json`-ja pedig:

> `"peerDependencies": { "drizzle-orm": "1.0.0-rc.4" }`, `"devDependencies": { ..., "drizzle-kit": "1.0.0-rc.4", ... }`
(https://raw.githubusercontent.com/paradedb/drizzle-paradedb/main/package.json)

**Tehát a ParadeDB hivatalos Drizzle-integrációja 2026. szeptember 22-i állapot szerint a Drizzle ORM/drizzle-kit 1.0 *release candidate* ágát követeli meg, miközben az npm "latest" (stabil) tag még a 0.45.x / 0.31.x sorozatra mutat.** Ezt két, egymástól független elsődleges forrás (npm registry + a csomag saját `package.json`-ja) is megerősíti.

---

## 2. Drizzle és a `pgvector`

A hivatalos „PostgreSQL extensions” oldal (`orm.drizzle.team/docs/extensions/pg`):

```ts
const table = pgTable('table', {
	embedding: vector({ dimensions: 3 }),
	embedding2: vector({ dimensions: 3 }).default([0, -2, 3])
})
```

```ts
import { l2Distance, l1Distance, innerProduct,
          cosineDistance, hammingDistance, jaccardDistance } from 'drizzle-orm'

l2Distance(table.column, [3, 1, 2])
l1Distance(table.column, [3, 1, 2])
innerProduct(table.column, [3, 1, 2])
cosineDistance(table.column, [3, 1, 2])
hammingDistance(table.column, '101')
jaccardDistance(table.column, '101')
```

HNSW-index:
```ts
export const table = pgTable('items', {
    embedding: vector({ dimensions: 3 })
}, (table) => [
  index('l2_index').using('hnsw', table.embedding.op('vector_l2_ops')),
  index('ip_index').using('hnsw', table.embedding.op('vector_ip_ops')),
  index('cosine_index').using('hnsw', table.embedding.op('vector_cosine_ops'))
])
```
(https://orm.drizzle.team/docs/extensions/pg)

A „Vector similarity search with pgvector extension” guide (külön oldal) ugyanezt a `vector()` oszlop-mintát és a `cosineDistance`-t mutatja be, konkrét RAG-példán:

> „`drizzle-orm@0.31.0 and drizzle-kit@0.22.0 or higher`” — ez a **régebbi, stabil (0.3x) Drizzle-ágra** vonatkozó minimumkövetelmény (nem az 1.0 RC-re).
(https://orm.drizzle.team/docs/guides/vector-similarity-search)

Ezt két, egymástól független Drizzle-dokumentációs oldal (extensions/pg és a guides/vector-similarity-search) is megerősíti; harmadik megerősítésként a ParadeDB-csomag `src/search.ts`/`src/indexing.ts` forrása is ugyanezeket a Drizzle-natív azonosítókat (`vector`, `cosineDistance`, `innerProduct`, `l2Distance`) exportálja tovább (ld. 1.2–1.3 pont).

A Drizzle `PgIndexOpClass` típusdefiníciója (ugyanaz a forrásfájl, mint 1.4-ben) explicit pgvector-opclass-okat listáz:

> „`// pg_vector types` `| 'vector_l2_ops' | 'vector_ip_ops' | 'vector_cosine_ops' | 'vector_l1_ops' | 'bit_hamming_ops' | 'bit_jaccard_ops' | 'halfvec_l2_ops' | 'sparsevec_l2_op'`”
(https://raw.githubusercontent.com/drizzle-team/drizzle-orm/main/drizzle-orm/src/pg-core/indexes.ts)

---

## 3. Driverek Bun alatt

### 3.1 `Bun.sql`

A hivatalos Bun-dokumentáció (`bun.com/docs/runtime/sql`, 506 935 bájt HTML, teljes egészében letöltve és géppel átvizsgálva kulcsszavakra) — a „vector” és „pgvector” szó **egyszer sem** fordul elő a teljes oldalon (0 találat), miközben „Postgres”/„PostgreSQL” összesen 461-szer. **Tehát a hivatalos Bun SQL-dokumentáció nem tárgyal semmilyen vektor-típus- vagy pgvector-támogatást.**

A hivatalos GitHub tracking issue:

> **Cím:** „`Bun.sql` tracking issue (Postgres client)” — **állapot:** nyitva (#15088) — „`Bun.sql` is Bun's builtin postgres, mysql and sqlite client”
Kész funkciók (idézve az issue-ból): automatikus prepared statement, primitív és objektum típusok, SQL tömb beszúrás, query pipelining, SCRAM-SHA-256/MD5 auth, TLS/sslmode, kapcsolat-timeout, RDS/Neon/Supabase kompatibilitás, round-robin kapcsolatok, point/geo típusok, `--sql-preconnect` CLI flag, tranzakció API (`sql.begin(callback)`), `sql.array()`.
Függőben lévő funkciók: COPY protokoll, async iterátorok, query instrumentáció/logolás.
(https://github.com/oven-sh/bun/issues/15088)

**Vektor/pgvector típus egyik forrásban sem szerepel** — ez két, egymástól független elsődleges forrás (hivatalos doksi + hivatalos tracking issue) egybehangzó *hiánya*, amit "evidence of absence"-ként kezelek, nem csupán "nem találtam"-ként.

### 3.2 Drizzle és Bun SQL

A hivatalos „Bun SQL” Drizzle-oldal:

> „Drizzle ORM natively supports `bun sql` module and it's crazy fast 🚀”

Telepítési utasítás **RC-csomagokkal**:
> `drizzle-orm@rc` és `drizzle-kit@rc` telepítése javasolt, majd:
```ts
const db = drizzle(process.env.DATABASE_URL);
// vagy
const client = new SQL(process.env.DATABASE_URL!);
const db = drizzle({ client });
```
(https://orm.drizzle.team/docs/connect-bun-sql)

Ez összecseng a 2. és 1.7 pontban idézett npm registry-adattal: a Bun SQL Drizzle-integráció is a `@rc` (1.0.0-rc.4) ágon van dokumentálva, nem a "latest" stabil 0.45.3-on. Két független forrás (a Drizzle Bun-SQL doksi oldal + az npm dist-tags) erősíti meg ezt.

### 3.3 `postgres.js` és `node-postgres` (`pg`) Bun alatt

A hivatalos Drizzle „Get Started – PostgreSQL” oldal a támogatott driverek/kliensek közt sorolja fel: „node-postgres” (pg csomag), „postgres.js”, valamint (külön blokkban) „Bun SQL”, Neon, Vercel Postgres, Supabase, PGLite, Nile, stb.
(https://orm.drizzle.team/docs/get-started-postgresql)

A `postgres.js` Bun alatti működéséről a hivatalos `oven-sh/bun` GitHub repóban több, egymástól független hibajegy is van:

> **Cím:** „postgres-js queries hang indefinitely on Bun 1.1.35+” — **állapot:** Closed (javító PR: #15543) — **bejelentve:** 2024. november 27. — „queries fail to resolve and hang indefinitely” Bun 1.1.35–1.1.37 alatt (1.1.34 alatt működött), Drizzle ORM + RDS Postgres + SSL kombinációban. Maintainer hozzárendelve, „bug” címkével.
(https://github.com/oven-sh/bun/issues/15438)

További, hasonló témájú, de külön hibajegyek (csak cím szintjén ellenőrizve, tartalmi idézet nélkül — ezt itt jelzem): „SQL: loses connection after timeout” (#17178), „Postgres connection leak” (#23215), „Bun fails to terminate running query with `postgres`” (#15443).
(https://github.com/oven-sh/bun/issues)

A `node-postgres` (`pg`) csomag saját GitHub repójában:

> **Cím:** „pg-native not wotks on Bun (same code works on Node.js)” — **állapot:** Closed — **bejelentve:** 2024. április 29. — a `pg-native` (opcionális, C++ bővítményt használó) csatlakozó nem tölti be a natív `addon.node` binárist Bunon, míg Node.js alatt ugyanaz a kód működik. A tiszta JavaScript `pg` mag (native addon nélkül) állapotáról ez az issue nem nyilatkozik.
(https://github.com/brianc/node-postgres/issues/3201)

**Melyiket "támogatja hivatalosan" a Drizzle Bunnal?** A Drizzle dokumentációja külön, dedikált oldalt ad **csak** a Bun SQL-nek (`connect-bun-sql`); a `get-started-postgresql` oldal a `node-postgres`/`postgres.js`-t driver-specifikus, de nem Bun-specifikus útmutatóként listázza. **Explicit, egy mondatos hivatalos ajánlást arra, hogy "Bun alatt melyik driver a hivatalosan javasolt", nem találtam** — ezt NINCS FORRÁS-ként jelzem.

---

## 4. Better Auth Postgres-szel

### 4.1 Hivatalos adapter

A hivatalos Better Auth dokumentáció:

> „`provider: "pg"`” — ez a Postgres-dialektus beállítása a Drizzle adapteren belül; „If you're using PostgreSQL and you want to generate the schema with a custom schema namespace, you can pass the `schemaName` option to the Drizzle adapter.”
(https://better-auth.com/docs/adapters/drizzle)

### 4.2 Drizzle 1.0 RC-kompatibilitási probléma és javítása

> **Issue #7691** — „fix: Handle drizzle 1.0rc in drizzle-adapter” — **bejelentve:** 2026. január 29. — **állapot:** Closed as duplicate of #6766. „Better Auth still uses old (now unsupported) query syntax” → „Unknown relational filter field: decoder” hiba drizzle-orm 1.0.0-beta.12 alatt, Better Auth 1.4.18, Node v24.13.0 mellett.
(https://github.com/better-auth/better-auth/issues/7691)

> **Issue #6766** (a fő tracking issue) — cím: „Update Drizzle ORM Adapter to support the new Drizzle ORM query syntax (drizzle-orm v1.0.0)” — **állapot:** Resolved. Maintainer-idézet: „This is already done and released in v1.7 RC from PR https://github.com/better-auth/better-auth/pull/9489” — a javaslat a `@rc` Better Auth csomagokra váltás.
(https://github.com/better-auth/better-auth/issues/6766)

Két, egymástól független, egymásra hivatkozó GitHub-issue (#7691 és #6766) is megerősíti: **a Better Auth Drizzle adapter csak a Better Auth 1.7 *release candidate* verziójában kompatibilis a Drizzle ORM 1.0 RC-ágával** — ami közvetlenül releváns, mivel az 1.7 pontban idézett `@paradedb/drizzle-paradedb` is a Drizzle 1.0.0-rc.4-et írja elő. Ez azt jelenti, hogy egy ParadeDB+Drizzle+Better Auth kombináció jelenleg **mindkét** RC-ágat igényelné.

### 4.3 Bun-specifikus CLI-problémák (providertől függetlenül)

> **Issue #2283** — „Failed to generate with Bun, Drizzle and PostgreSQL” — **bejelentve:** 2025. április 14. — **állapot:** Closed, címkék: `bug`, `wontfix`. A `bunx --bun @better-auth/cli@latest generate` PostgreSQL + `provider: 'pg'` beállítás mellett is megpróbálja betölteni a `better-sqlite3` csomagot, ami szegmentálási hibával (`Segmentation fault`) összeomlik Bun alatt.
(https://github.com/better-auth/better-auth/issues/2283)

> **Issue #7987** — „Bun on Docker fails due to Better-Auth using better-sqlite3” — **bejelentve:** 2026. február 16. — **állapot:** Closed. „It installs a whole ton amount of unnecessary deps, like drizzle, svelte, sqlite, mysql” — az adott felhasználó MongoDB+Prisma providert használt, mégis a `better-sqlite3` telepítése hibázott: „Bun does not yet support 'better-sqlite3'” (hivatkozva a `oven-sh/bun` #4290 tracking issue-ra).
(https://github.com/better-auth/better-auth/issues/7987)

Két, egymástól független Better Auth-hibajegy (#2283 és #7987, más-más bejelentő, más-más dátum, más adatbázis-provider) egyaránt megerősíti, hogy **a Better Auth CLI (és/vagy a csomag függőségi fája) a választott adatbázis-providertől függetlenül behúzza a `better-sqlite3`-at, ami Bun alatt natív-binding problémákat okoz.** Mindkettő "wontfix"/"closed" — nincs jele hivatalos, végleges javításnak a lekért tartalom szerint.

---

## 5. Tranzakciók és egyidejűség

### 5.1 Postgres alapértelmezett izolációs szint

A hivatalos PostgreSQL dokumentáció:

> „*Read Committed* is the default isolation level in PostgreSQL.”
(https://www.postgresql.org/docs/current/transaction-iso.html)

Serializable mód esetén konkurens tranzakció-ütközésnél:
> „ERROR: could not serialize access due to read/write dependencies among transactions”
(uo.)

### 5.2 ParadeDB hivatalos garancia-állítása

A ParadeDB „Guarantees” oldala:

> „All reads and writes go through Postgres' transaction engine. This means that inserts, updates, and deletes to indexed columns are atomic, consistent, and respect Postgres' isolation levels.”

> „By default, ParadeDB favors correctness, even when it comes at the cost of slower query execution.”

> A Community-kiadás 0.24.0-tól write-ahead loggal biztosít crash-safe tartósságot; logikai replikációt támogat, de **fizikai replikációt (HA-hoz) csak az Enterprise-kiadás.**
(https://www.paradedb.com/docs/welcome/guarantees)

### 5.3 Ezt cáfoló, nyitott hivatalos hibajegy — ld. „Ellentmondások”

### 5.4 Konkurens `CREATE INDEX CONCURRENTLY USING bm25` hiba

> **Issue #5449** — „CREATE INDEX CONCURRENTLY USING bm25 fails with missing "pg_tblspc/..." file under concurrent writes” — **állapot:** nyitva. Érintett verziók: **v0.21.6 és v0.24.1**. Reprodukció: 300 000 soros tábla, ~2 percnyi párhuzamos insert/update, majd `CREATE INDEX CONCURRENTLY ... USING bm25` → hiba. A maintainer (Rohan-Singla) megerősítette a reprodukciót, javítást ígért, de a lekért tartalomban konkrét workaround nem szerepel.
(https://github.com/paradedb/paradedb/issues/5449)

**Ehhez második, független megerősítést nem találtam** — csak ez az egy issue dokumentálja ezt a konkrét hibát.

### 5.5 Szegmensek és zárolás — architektúra

A ParadeDB hivatalos blogja („A New Postgres Block Storage Layout for Full Text Search”):

> „Rather than being written to a file, segments are serialized and written to blocks. Large segments that spill past a single block are stored in a linked list of blocks.”

> „every DML statement in Tantivy creates at least one new segment” — ezért vezették be a `merge_on_insert` mechanizmust.

> „It is critical that only one merge process runs concurrently. If two merge processes run at the same time, they could both see the same segments, merge them together, and create duplicate segments.” Ennek elkerülésére „every merge process atomically writes its transaction ID to a metadata block. Subsequent merge attempts first read this transaction ID, and are only allowed to proceed if the effects of that transaction ID are MVCC-visible.”

> „Tantivy's lock files are no longer needed since Postgres provides buffer-level, interprocess locking mechanisms.”

> „Postgres MVCC visibility information is stored alongside each segment UUID. At query time, the extension uses MVCC visibility rules to construct a snapshot of the list of all visible segments.”

> A cikk explicit jelzi, hogy egy második rész („Part 2”) fogja tárgyalni, „how we designed and tested `pg_search` to be MVCC-safe in update-heavy scenarios” — vagyis a szerzők szerint is **folyamatban lévő** terület.
(https://www.paradedb.com/blog/block-storage-part-one)

Ezt a technikai leírást **csak ez az egy (hivatalos vállalati blog-) forrás dokumentálja**; a `pg_search/README.md` GitHub-fájlban nem találtam kiegészítő/megerősítő részletet a szegmens-zárolásról (csak verziókompatibilitási infót: „`pg_search` is supported on official PostgreSQL Global Development Group Postgres versions, starting at PostgreSQL 15.”, https://github.com/paradedb/paradedb/blob/main/pg_search/README.md). **Második független forrást a szegmens-zárolás technikai részleteire nem találtam.**

### 5.6 `REINDEX` és konkurens írás

A hivatalos ParadeDB reindexing-dokumentáció (redirekttel: `docs.paradedb.com/documentation/indexing/reindexing` → `www.paradedb.com/docs/operate/index-maintenance/reindexing.md`):

> Plain `REINDEX`: „takes an exclusive lock on the table, which blocks incoming writes (but not reads) while the new index is being built.”

> „To allow for concurrent writes during a reindex, use `REINDEX CONCURRENTLY`”, de „the tradeoff is that `REINDEX CONCURRENTLY` is slower than a plain `REINDEX`.”

> Fontos korlát: „Although `CREATE INDEX CONCURRENTLY` and `REINDEX CONCURRENTLY` run in the background, Postgres requires that the session that is executing the command remain open.” Ha a munkamenet megszakad (pl. connection pooler idle-timeoutja miatt), a művelet megszakad, és „an invalid transient index will be left behind that must be dropped manually”.
(https://www.paradedb.com/docs/operate/index-maintenance/reindexing.md)

---

## 6. Tesztelés

### 6.1 Hivatalos ParadeDB Docker image

> `docker run --name paradedb -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=mydatabase -v paradedb_data:/var/lib/postgresql/ -p 5432:5432 -d paradedb/paradedb:latest`
> „ParadeDB supports Postgres 15+”; a `latest` tag Postgres 18-at tartalmaz.
(https://docs.paradedb.com/documentation/getting-started/install)

A GitHub Releases oldal szerint a legutóbbi név szerinti release **v0.25.0 (2026. július 28.)**, előtte v0.24.3 (2026.07.15.) és v0.24.2 (2026.07.10.) — ld. „Ellentmondások” a verziószám-eltérésről.
(https://github.com/paradedb/paradedb/releases)

### 6.2 Hivatalos CI-útmutató (GitHub Actions), nem testcontainers

> „How to run ParadeDB in GitHub Actions CI” — a workflow a `paradedb/paradedb` image-et Docker service-ként indítja, `--health-cmd="pg_isready -U postgres"`, `--health-interval=10s`, `--health-timeout=5s`, `--health-retries=5` health-check paraméterekkel; a tag-lista helyét a doksi a `https://hub.docker.com/r/paradedb/paradedb/tags` címre mutatja. A minta workflow `paradedb.create_bm25_test_table()`-lel hoz létre teszttáblát, BM25-indexet épít, és `@@@` operátorral futtat lekérdezést.
(https://www.paradedb.com/docs/deploy/ci/github-actions)

**Ez a hivatalos oldal nem említ testcontainers-t.**

### 6.3 A hivatalos Drizzle-csomag saját tesztelési módszere — szintén nem testcontainers

A `@paradedb/drizzle-paradedb` saját `scripts/run_paradedb.sh` (nyersen lekért, teljes forrás):

```bash
PARADEDB_VERSION="${PARADEDB_VERSION:-0.25.0}"
PARADEDB_POSTGRES_VERSION="${PARADEDB_POSTGRES_VERSION:-18}"
IMAGE="${PARADEDB_IMAGE:-paradedb/paradedb:${PARADEDB_VERSION}-pg${PARADEDB_POSTGRES_VERSION}}"
...
docker run -d --name "$CONTAINER_NAME" -e "POSTGRES_USER=$USER" -e "POSTGRES_PASSWORD=$PASSWORD" \
  -e "POSTGRES_DB=$DB" -p "$PORT:5432" "$IMAGE"
...
docker exec "$CONTAINER_NAME" pg_isready -h 127.0.0.1 -U "$USER" -d "$DB"
```
(https://raw.githubusercontent.com/paradedb/drizzle-paradedb/main/scripts/run_paradedb.sh)

A `CONTRIBUTING.md` szerint:
> „`pnpm db:setup` starts a ParadeDB container via Docker and exports `DATABASE_URL`... Run the tests to verify every change: `bash scripts/run_tests.sh`... Some integration tests require newer pg_search versions and are skipped automatically if the feature is not available.”
(https://raw.githubusercontent.com/paradedb/drizzle-paradedb/main/CONTRIBUTING.md)

**Tehát a hivatalos ParadeDB Drizzle-csomag saját CI/integrációs tesztjei nem a Testcontainers könyvtárat használják, hanem közvetlen `docker run`-t egy bash-szkriptben, `vitest` tesztfuttatóval.** Ezt két egymástól független, saját (első-kézből) forrás támogatja (a szkript és a CONTRIBUTING.md), de mindkettő ugyanabból a repóból származik — külső, harmadik fél általi megerősítést erre nem kerestem/találtam, mert ez magának a szkriptnek/repónak a ténye, nem külső állítás.

### 6.4 Testcontainers és egyedi (extension-es) Postgres image — általános minta, NEM ParadeDB-specifikus

Önálló, hivatalos **ParadeDB testcontainers-modult nem találtam** (sem `testcontainers.com/modules/`, sem GitHub-keresés nem hozott ilyet). **NINCS FORRÁS.**

Van viszont hivatalos, analóg minta a Testcontainers projekttől magától a `pgvector` extension image-re, ami **Node.js-t is tartalmaz**:

> „pgvector, open-source vector similarity search for Postgres.” Nyelvek: Java, Go, .NET, **Node.js**. Alapértelmezett image minden nyelvi példában: `pgvector/pgvector:pg16`.
> Node.js kód: `const container = await new PostgreSqlContainer("pgvector/pgvector:pg16").start();`
> Java kód: `DockerImageName.parse("pgvector/pgvector:pg16").asCompatibleSubstituteFor("postgres")`
(https://testcontainers.com/modules/pgvector/)

Ezt megerősíti a hivatalos Java Testcontainers Postgres-modul dokumentációja is, amely explicit PostGIS-példával ugyanezt az `asCompatibleSubstituteFor("postgres")` mintát mutatja, és megjegyzi, hogy „This same pattern applies to other extensions like TimescaleDB and pgvector.”
(https://java.testcontainers.org/modules/databases/postgres/)

**Két, egymástól független, hivatalos Testcontainers-forrás** (a `pgvector` modul oldala és a Java Postgres-modul oldala) igazolja, hogy a generikus `PostgreSqlContainer`/`PostgreSQLContainer` osztály **image-tag cserével** (Node.js-ben egyszerűen a konstruktor string-argumentumában) tetszőleges Postgres-kompatibilis, extension-es image-dzsel (pl. elvben a `paradedb/paradedb`-vel is) használható. **Ez azonban csak analógia — konkrét, ParadeDB-re vonatkozó hivatalos vagy közösségi Testcontainers-példát nem találtam**, ezt a korlátot itt explicit jelzem.

---

## Ellentmondások

1. **ParadeDB "Guarantees" oldal vs. nyitott konkurenciahiba.** A hivatalos garancia-oldal kijelenti: „inserts, updates, and deletes to indexed columns are atomic, consistent, and respect Postgres' isolation levels” (https://www.paradedb.com/docs/welcome/guarantees). Ezzel szemben egy **nyitott** hivatalos GitHub-issue (#6390, bejelentve 2026. szeptember 17.) kimutatja, hogy SERIALIZABLE izoláció alatt a `pg_search` alap- és aggregált-scanjei **nem** vesznek SIREAD-zárat, ezért „two `SERIALIZABLE` transactions could each count the rows matching a search, then each insert a row the other would have counted, and both commit” — azaz phantom write skew történhet, amit a natív Postgres-tervek megelőznének. A javítást célzó PR (#6392) a kutatás idején (2026. szeptember 22.) **még nyitott, nem mergelt** állapotban van. (https://github.com/paradedb/paradedb/issues/6390, https://github.com/paradedb/paradedb/pull/6392) Ez közvetlen ellentmondás a hivatalos garancia-szöveg és a jelenlegi, dokumentált, javítatlan viselkedés között.

2. **ParadeDB legfrissebb verziószáma: forrásfüggő eltérés.** A hivatalos GitHub Releases oldal (WebFetch-lekérdezéssel) a legfrissebb, név szerint listázott kiadásnak a **v0.25.0**-t (2026.07.28.) mutatta, míg egy harmadik fél release-követő szolgáltatás (newreleases.io, csak keresési találatként, nem közvetlenül lekérve/idézve) egy **v0.25.6** verziót is említett. Mivel a GitHub Releases-oldal lekérdezése HTML-összefoglalón (WebFetch) keresztül történt, és lehetséges, hogy a lapozás/JS-renderelés nem adta vissza a legfrissebb patch-kiadásokat, ezt az ellentmondást **nem oldottam fel** — a `paradedb/paradedb` GitHub repó Releases oldalának közvetlen, teljes böngészőn keresztüli ellenőrzése szükséges a pontos legfrissebb verzióhoz.

---

## Amire NINCS forrás

- Hivatalos ParadeDB–Kysely integráció, dokumentáció vagy csomag — semmilyen keresési eredmény nem hozott ilyet.
- Explicit hivatalos Drizzle-állásfoglalás arról, hogy Bun alatt a `node-postgres`, a `postgres.js` vagy a `Bun.sql` a "hivatalosan ajánlott" driver — a Drizzle doksi mindhármat dokumentálja, de rangsorolást/ajánlást nem tettem közzé belőle idézhető formában.
- Önálló, hivatalos (ParadeDB vagy Testcontainers által karbantartott) Testcontainers-modul kifejezetten a `paradedb/paradedb` image-hez.
- Második, független forrás a `drizzle-kit generate` #2935 hibájának pontos javítási verziójára/dátumára.
- Második, független forrás a ParadeDB #5449 (`CREATE INDEX CONCURRENTLY USING bm25` konkurens-írási hiba) létezésére — csak az egy GitHub-issue dokumentálja.
- Második, független (nem a ParadeDB blogján kívüli) technikai forrás a `pg_search` szegmens-szintű zárolási/merge-mechanizmusának részleteire (5.5 pont) — a hivatalos `pg_search/README.md` ezt nem részletezi, és a bejelentett „Part 2” blogbejegyzést a keresés nem hozta fel/nem találtam meg.
- Konkrét, mért adat arra, hogy a `pg_search` index hogyan viselkedik teljesítmény/áteresztőképesség szempontjából sok egyidejű író alatt (csak kvalitatív, architekturális leírás áll rendelkezésre, mért számok nélkül).

---



---

# SQ07 — Valós tapasztalatok, mérések és hibamódok

> **Módszertani megjegyzés (kötelező, ld. `_kozos.txt`):** a kutatás az `anthropic-skills:deep-web-research` skill *irányelveit* követi (elsődleges forrás előny, T1/T2/T3 rétegzés, minden állításnál idézet+URL, kontradikciók jelölése), de **degradált módban**, mert ebben a futtatási környezetben nem érhető el az `Agent`/subagent-indító eszköz (ezt az ágenst magát is egy másik ágens indította alfeladatként, és nem tud saját Sonnet/Opus alügynököket indítani). Emiatt nem készült teljes `.research/` bizonyítéktár (manifest, shardolás, `finalize.py` audit) — helyette egyetlen kutató (én) végezte sorban a keresést, a forrásolvasást és az írást, ugyanazon minőségi szabályok (idézet+URL, kettős megerősítés, "NINCS FORRÁS" jelölés) betartásával. GitHub API-hozzáférés (gh CLI, api.github.com) ehhez a repóhoz nem volt elérhető a proxyn keresztül ("GitHub access to this repository is not enabled for this session"), ezért a GitHub-issue kutatás `WebSearch` + egyedi issue-oldalak `WebFetch`-elésével történt (a `github.com/.../issues?q=...` kereső URL-eket a robots.txt tiltja a fetch-elő eszköznek). A `web.archive.org` a munkakörnyezet egress-szabálya miatt teljesen blokkolva volt ("Blocked by egress policy" / "Access to this website has been blocked"), így archív mentésekkel nem lehetett második csatornán megerősíteni azokat az oldalakat, amelyek időközben megváltoztak. A Hacker News szálak tartalmát a `WebFetch` 429-es hibával (rate limit) visszautasította, ezért csak a keresési index/cím-szintű adatok álltak rendelkezésre, a hozzászólások szövege nem.
>
> **Rétegzés ebben a dokumentumban:** **T1** = hivatalos ParadeDB-dokumentáció, forráskód-repó (GitHub issue/PR/release/changelog). **T2** = mérésalapú forrás konkrét módszertannal (ide tartozik a ParadeDB saját blogján közölt benchmark **is**, ahogy a feladat kéri, külön jelölve — és a független, de módszertannal dokumentált harmadik féltől származó benchmark is). **T3** = közösségi vélemény, anekdota, marketing-jellegű összehasonlító oldal, mérési adat nélkül.

## Rövid válasz

A ParadeDB `pg_search` BM25-indexéről három, egymástól független, konkrét módszertannal dokumentált mérés is található (Elasticsearch, natív Postgres FTS és egy versenytárs — SereneDB — saját benchmarkja ellenében), és ezek **egymásnak ellentmondó képet** adnak: van, ahol ParadeDB nyer nagy különbséggel (pl. fuzzy/field-specific keresés egy 1,6M soros teszten), van, ahol veszít (natív Postgres gyorsabb pontos frázis-keresésnél ugyanabban a tesztben; Elasticsearch gyorsabb tiszta lekérdezés-átbocsátásban nagy egyidejűség mellett), és van, ahol 1 milliárd soros terhelésnél a ParadeDB-lekérdezések 92-ből csak 77-et fejeztek be időn belül. A GitHub issue-kban **valódi, dokumentált "helytelen találati eredmény" hibák** vannak, a legrégebbi (#1929, 2024.11.12., v0.12.0→javítva v0.12.1-ben) mellett egy egészen friss, 2026.09.17-i kötegben (#6375, #6394, #6108), amelyek pontosan a JOIN-eket és a UPDATE/VACUUM utáni állapotot érintik — ez utóbbiak a fő ág (`main`) commitjain jelentkeztek, ismeretlen, hogy hivatalos release-be kerültek-e valaha hibásan. Az írási költség dokumentáltan komoly volt: a ParadeDB saját blogja szerint v0.18.0-ban 120 UPDATE/mp volt a limit, ami v0.19.0-ra 1857-re, v0.20.0-ra 2016-ra nőtt — miközben a hivatalos dokumentáció kifejezetten használja a "write amplification" kifejezést a szegmens-összefésülésre. Kritikus, 2025.06.03-ig (v0.24.0-ig) fennálló tény: a hivatalos "Guarantees" oldal szerint **a ParadeDB Community tranzakciói csak v0.24.0-tól "durable"-ök (WAL-logoltak, crash-safe-ek)** — ez azt jelenti, hogy korábban a Community-kiadás indexadatai összeomláskor nem feltétlenül voltak helyreállíthatók. A hivatalos korlátok között kiemelendő, hogy a fizikai streaming replikáció / olvasó replikák kizárólag Enterprise-ban működnek ("Serving reads from a standby requires... ParadeDB Enterprise, not ParadeDB Community"), a Community egyetlen csomóponton fut, a fedő-index (covering index) miatt minden oszlopot előre meg kell adni létrehozáskor, és a natív Postgres 32-oszlopos index-korlát ParadeDB alatt is érvényes (kerülő megoldás: kompozit típusok, v0.22.0-tól). Közösségi (Reddit/HN) tapasztalatból **nem sikerült két egymástól független, tartalmilag egyező beszámolót** találni — a Reddit-keresés gyakorlatilag nulla releváns találatot adott, a Hacker News-szálak tartalmát pedig a lekérő eszköz rate-limitje miatt nem sikerült elolvasni, ezért ezen a ponton NINCS FORRÁS.

---

## 1. Független mérések: ParadeDB vs. Elasticsearch/OpenSearch, natív Postgres FTS, SQLite FTS5

### 1.1. ParadeDB saját benchmarkjai (T2 — nem független, a kért külön kategorizálás szerint)

**a) ParadeDB vs. natív Postgres FTS (tsvector/GIN)** — ParadeDB saját blogja, *"Same Query, Three Results: Benchmarking ParadeDB and Postgres FTS"*, szerző James Blackwood-Sewell, közzététel: **2026.06.02.**
URL: https://www.paradedb.com/blog/benchmarker-iteration

Módszertan (idézet a lekérésből): adat — *"one million rows in a single `hn_items` table, keeping only the `id` and `text`"* (Hacker News archívumból), hardver — *"four cores and eight gigabytes of memory"* konténerenként, lekérdezés-típus: **TopK relevancia-keresés, 10 találat**, azonos lekérdezés-struktúra mindkét rendszeren.

Eredmények:
| Menet | Terhelés | Végrehajtás | ParadeDB | Postgres FTS | Különbség |
|---|---|---|---|---|---|
| 1 | egy kifejezés ("inverted") | closed-loop, 16 VU | 3646 QPS | 3290 QPS | ~10% |
| 2 | 40 kifejezés rotálva | closed-loop, 16 VU | 3373 QPS | 115 QPS | **29×** |
| 3 | 40 kifejezés rotálva | open-loop, 50 QPS | P99 5,11 ms | P99 238 ms | **47×** |

A cikk üzenete maga is az, hogy a terhelés jellege és a mérési modell (closed- vs. open-loop) drasztikusan megváltoztatja az eredményt — ezt a saját forrás mondja ki, nem én értékelem.

**b) ParadeDB írási teljesítmény — saját blog**, *"Postgres as a Search Engine: The Write Performance Problem"*, szerzők Ming Ying és James Blackwood-Sewell, közzététel: **2025.12.15.**
URL: https://www.paradedb.com/blog/increased-write-performance
Lásd részletesen a 3. szakaszban (írási költség).

### 1.2. Független mérések (T2)

**c) ParadeDB vs. Elasticsearch — `inevolin/ParadeDB-vs-ElasticSearch` GitHub repó** (nem ParadeDB-alkalmazott, közösségi repó).
URL: https://github.com/inevolin/ParadeDB-vs-ElasticSearch

Módszertan (idézet): hardver — *"MacBook Pro M1"*, *"Local Kubernetes cluster running in Docker (configured with 8 CPUs and 12GB RAM)"*, mindkét rendszer egyenként *"4 CPU, 8GB RAM"*-ra korlátozva. Adatméretek: 1000+1000, 100 000+100 000, 1 000 000+1 000 000 szülő-gyermek dokumentum (1:1 kapcsolat). Hat lekérdezés-típus: egy kifejezéses full-text, pontos frázis, két kifejezés OR, egy kifejezés LIMIT-tel (N=50), három feltételes bool query, JOIN szülő→gyermek.

Eredmény (1M dokumentum, 50 kliens): Elasticsearch átlag **837 TPS**, ParadeDB átlag **444 TPS** — azaz itt Elasticsearch kb. **1,9×** gyorsabb lekérdezés-átbocsátásban. Ezzel szemben betöltés/indexelés: ParadeDB **123 mp**, Elasticsearch **380 mp** — itt ParadeDB kb. **3×** gyorsabb. A repó megjegyzi: *"Elasticsearch leads at 1/10 clients"* — azaz kis egyidejűségnél is ES vezet lekérdezésben. Dátum a repóban nem szerepel explicit publikálási dátumként — **NINCS FORRÁS** a pontos mérési dátumra.

**d) ParadeDB vs. natív Postgres — Vineeth Pothulapati személyes blogja**, *"PostgreSQL vs ParadeDB: A Search Comparison"*, közzététel: **2025.08.15.**
URL: https://www.vineeth.fyi/blog/pg-vs-pg-search/
A lekérés szerint a szerzőnek nincs feltüntetett ParadeDB- vagy versenytárs-affiliációja (személyes blog, GitHub-kóddal).

Adat: **1,6 millió Amazon-termék**. Hardver: **NINCS FORRÁS** (a cikk nem közli a CPU/RAM/tárolót). Öt lekérdezés-kategória:
| Típus | PostgreSQL | ParadeDB | Arány |
|---|---|---|---|
| Full-text | 401 ms | 92 ms | ParadeDB 4,4× gyorsabb |
| Fuzzy (elgépelés-tűrés) | 22 838 ms | 139 ms | ParadeDB 164× gyorsabb |
| Mező-specifikus | 4399 ms | 90 ms | ParadeDB 48× gyorsabb |
| Bool-lekérdezés | 7 ms | 2 ms | ParadeDB 3,5× gyorsabb |
| Pontos frázis | 6 ms | 89 ms | **Postgres 14× gyorsabb** |

Írási teljesítmény (1000 soros kötegek): *"ParadeDB is 5.4x faster (11,028 vs 2,056 rows/sec)"*.

Ez a forrás **ellentmond** a "ParadeDB mindig gyorsabb" narratívának: pontos frázis-keresésnél a natív Postgres FTS volt gyorsabb — ld. Ellentmondások.

**e) ParadeDB vs. SereneDB / TigerData / natív Postgres 18 — SereneDB blog** (versenytárs saját méréseként közölve — **összeférhetetlenség jelölve**).
Szerző: Andrey Abramov, a SereneDB CTO-ja, közzététel: **2026.09.07.**
URL: https://serenedb.com/blog/searchbench-postgres

Hardver (idézet): *"One GCP `n2-standard-32`, so 32 vCPUs of Intel Ice Lake at 2.6 GHz and 128 GB of RAM, running Ubuntu 24.04.4 LTS on a 3.9 TB `pd-ssd`."* Adat: 100 millió és 1 milliárd OpenTelemetry log sor, 15 oszloppal. Lekérdezések: *"92 of them, in five families: `count`, `top_k (bm25)`, `group_by`, `top_k (time)`, `join`"*, kombinálva egy-kifejezéses, konjunkció, diszjunkció, minimum-should-match, frázis, közelség, prefix, regexp, wildcard, fuzzy, negáció és időablak variánsokkal.

Eredmény (1 milliárd sor, hot median):
| Motor | Latencia | Végrehajtott lekérdezés |
|---|---|---|
| SereneDB | 35,5 ms | 92/92 |
| ParadeDB | 413,0 ms | **77/92** |
| TigerData | időkorlát felett | 33/92 |
| Postgres 18 | időkorlát felett | 12/92 |

Fontos: mivel a mérést egy közvetlen versenytárs CTO-ja publikálta saját termékéről, ez a forrás eleve elfogultsági kockázatot hordoz — ennek ellenére a nyers módszertan (hardver, adatméret, lekérdezés-lista) elég részletes ahhoz, hogy T2-ként szerepeltessem, a COI explicit jelölésével. Második független megerősítést erre a konkrét mérésre **nem találtam** — NINCS FORRÁS második, tőle független megerősítésre.

### 1.3. SQLite FTS5

Célzott keresés ("paradedb vs sqlite fts5 benchmark comparison") nem hozott olyan találatot, amely ParadeDB-t és SQLite FTS5-öt közvetlenül, azonos módszertannal hasonlítaná össze. **NINCS FORRÁS** közvetlen ParadeDB-vs-SQLite-FTS5 mérésre.

### 1.4. OpenSearch

Külön OpenSearch-specifikus, ParadeDB-vel közvetlenül összevető független mérést nem találtam (az (c) forrás Elasticsearch-et, nem OpenSearch-öt hasonlít). **NINCS FORRÁS** ParadeDB-vs-OpenSearch független mérésre.

---

## 2. Hibamódok a GitHub issue-kban (paradedb/paradedb)

### 2.1. Megerősített "helytelen találati eredmény" hibák

**Issue #1929** — *"Inconsistent search query results when joining tables with parallel processing"*
URL: https://github.com/paradedb/paradedb/issues/1929 — **Zárva**, nyitva: **2024.11.12.**, érintett verzió: **v0.12.0**, PostgreSQL 16.4 (Debian), Docker.
Idézet a hibaleírásból: *"Index Scan using search_product_idx_bm25_index on public.product p"* párhuzamos workerekkel **329 sort** adott vissza 3 loop alatt, míg `max_parallel_workers = 0` mellett **986 sort** egy loopban.
**Megerősítve két további, egymástól független T1-forrással:**
1. GitHub release notes (v0.12.1, közzétéve **2024.11.12.**): *"fix: index scans now work correctly under a parallel path (issue #1929)"* — https://github.com/paradedb/paradedb/releases/tag/v0.12.1
2. Hivatalos changelog (v0.12.1): *"Fixed a bug where parallel index scans could return incorrect results."* — https://docs.paradedb.com/changelog/0.12.1 (a WebFetch-eszköz élő oldalról nyerte ki 2026.09.22-én; utólagos közvetlen `curl` már 404-et adott erre az URL-re — a Mintlify-oldal láthatóan kliensoldali útvonalkezelést használ történeti verzióoldalakhoz, a `web.archive.org` pedig ebben a környezetben teljesen blokkolva van, így egy **harmadik, teljesen független csatornán nem sikerült újra-ellenőrizni** ezt a pontos szöveget — ezt jelzem, nem simítom el.)

**Issue #6375** — *"Join scan drops one user's rows after a HOT update and VACUUM on a churned heap"*
URL: https://github.com/paradedb/paradedb/issues/6375 — **Zárva** (PR #6378-hoz kapcsolva), nyitva: **2026.09.17.**, érintett: `main` ág, commit `85d6ca06b`, PostgreSQL 15.15.
Idézet: *"PostgreSQL returns 9 rows, four for users.id = 11 and five for users.id = 5. The join scan returns only the five rows of user 5"*, illetve *"window aggregates agree on both sides (COUNT(*) OVER () = 40), so the rows are lost after the join"*. A hiba nem determinisztikus (4, 8, vagy 1 sor a várt 9 helyett, futtatásonként változóan).

**Issue #6394** — *"Join scan drops the whole row when an outer join's nullable side cannot be fetched"*
URL: https://github.com/paradedb/paradedb/issues/6394 — **Zárva** (PR #6395), nyitva: **2026.09.17.**
Idézet: *"When the join scan cannot fetch the heap tuple of a source on an outer join's nullable side, it drops the whole joined row. The correct result keeps the preserved side's row and fills the nullable side with NULLs."* A gyökérok a maintainer szerint a `VisibilityChecker` blokkszám-cache-elésében van, ami hibás láthatóság-ellenőrzést okozhat, ha a heap nő egy rögzített snapshot alatt.

**Issue #6108** — *"Sequential scan fallback returns no rows for NUMERIC key fields"*
URL: https://github.com/paradedb/paradedb/issues/6108 — **Nyitva** (a lekérés időpontjában nem volt zárva, javítási verzió **NINCS FORRÁS**).
Ok: a szekvenciális-scan tartalék útvonal a heap `NUMERIC` kulcsokat séma-tudatosság nélkül alakítja stringgé, míg az index-kulcsok `I64`/`Bytes` fizikai reprezentációban vannak — a `KeySet` egzakt összehasonlítása így sosem talál egyezést.

**Issue #6101** — *"BM25 indexes reject valid NUMERIC typmods with \|scale\| > 18"*
URL: https://github.com/paradedb/paradedb/issues/6101 — **Nyitva**, érintett verzió: **0.25.4** (standalone pg_search, PostgreSQL 17, macOS arm64). Ez formálisan nem "hibás eredmény", hanem érvényes NUMERIC oszlopok indexelésének elutasítása — funkcionális korlát/hiba határeset, ide sorolva mert érintheti az adatmodellezést.

### 2.2. Crash / panic hibák

**Issue #6374** — *"Parallel top-k scan segfaults after two updates of one row in a mutable segment"*
URL: https://github.com/paradedb/paradedb/issues/6374 — **Zárva**, nyitva: **2026.09.17.**, `main` ág, commit `85d6ca06b`, PostgreSQL 15.15.
Idézet: *"server process (PID 40140) was terminated by signal 11: Segmentation fault."* Három egyidejű feltétel váltja ki: párhuzamos worker, heap-szűrő a scanben, és egy sor kétszeri UPDATE-je a mutable szegmensbe.

**Issue #806** — *"pg_analytics causes Citus to crash"* — csak cím-szinten azonosítva keresésből, tartalmát nem kérdeztem le részletesen. URL: https://github.com/paradedb/paradedb/issues/806

### 2.3. "Index out of sync" jellegű hibák

**Issue #6384** — *"Parallel top-K scan in a hashed SubPlan fails with `segment ... should exist` on a churned index"*
URL: https://github.com/paradedb/paradedb/issues/6384 — **Zárva**, nyitva: **2026.09.17.** Idézet: hibaüzenet *"segment Seg("cd90c1a3") should exist"*; a `SearchIndexReader::segment_readers_in_segments` olyan szegmens-azonosítót kapott, amit a saját readere nem tartalmazott. A maintainer megjegyzése szerint nem sikerült megbízhatóan reprodukálni ("heap states varied between replay attempts").

**Issue #702** — *"TRUNCATE is broken, tries to recreate the index"*
URL: https://github.com/paradedb/paradedb/issues/702 — **Zárva**, nyitva: **2024.01.19.**, érintett verzió **v0.4.4**. Leírás: tábla DROP után a hozzá tartozó BM25-index életben maradt. Kapcsolódó PR: #902.

**Issue #713** — *"bm25 index is not getting deleted properly"* — csak cím-szinten azonosítva, tartalom nem lekérve. URL: https://github.com/paradedb/paradedb/issues/713

**Issue #2575** — *"Unable to delete from a table with a BM25 index"*
URL: https://github.com/paradedb/paradedb/issues/2575 — **Zárva**, nyitva: **2025.05.15.**, érintett verzió **v0.15.19**, PostgreSQL 17.5 arm64. Hiba: DELETE parancsra `function "paradedb.snippet_positions(anyelement)" does not exist` — az index eltávolítása megkerülte a hibát. Javítási verzió a lekért tartalomban **NINCS FORRÁS**.

**Issue #2211** — *"BM25 index creation stuck"*
URL: https://github.com/paradedb/paradedb/issues/2211 — **Zárva**, nyitva: **2025.02.21.**, érintett verzió **v0.15.2**. Egy 130 000 soros/~2,3 GB táblán az index-építés >3 órán át lógva maradt maxolt CPU mellett, míg egy hasonló, kisebb (31 000 sor/~500 MB) tábla <1 perc alatt lefutott.

### 2.4. Törölt issue-k (nem tudtam tartalmat megerősíteni)

A keresés több, "wrong results"/"index recreation"/"score" jellegű issue-t is felszínre hozott, amelyek élő GitHub-oldala a lekérés idején **"This issue has been deleted"** üzenetet adott vissza — tartalmuk tehát **nem hozzáférhető és nem ellenőrizhető**, csak a keresési index címe utal rájuk:
- **#1406** — *"pg_search term search for text\[\] fields not working properly"* — https://github.com/paradedb/paradedb/issues/1406 (törölve)
- **#1407** — *"pg_search index recreation not working properly"* — https://github.com/paradedb/paradedb/issues/1407 (törölve)
- **#1631** — *"Issue with BM25 scoring in score_bm25"* — https://github.com/paradedb/paradedb/issues/1631 (törölve)
- **#1895** — *"Score returns NULL when joining 3 or more tables"* — https://github.com/paradedb/paradedb/issues/1895 (törölve)
- **#1207** — *"Slow degradation of index"* — https://github.com/paradedb/paradedb/issues/1207 (törölve)

**NINCS FORRÁS** arra, hogy ezek miért törlődtek (duplikátum-összevonás, spam, vagy egyéb ok) — ezt nem találtam ki, csak jelzem a tényt.

### 2.5. Egyéb, kapcsolódó hibák

- **#2038** — *"Filtering by `paradedb.score(id)` leads to no results"* — Zárva, nyitva **2024.12.30.**, `bug`/`priority-high`/`user-request` címkékkel. https://github.com/paradedb/paradedb/issues/2038
- **#1685** — *"Locking issue in `v0.8.6`"* — Zárva, nyitva **2024.09.19.** >3M soros táblánál UPDATE/SELECT lockolt és lefagyott; a felhasználó szerint *"updating and selecting rows to see the updated data is very important"*, és a 0.9.3/0.9.4-re váltás *"created additional problems with data volume persistence"*. Maintainer-megerősítés a lekért tartalomban **NINCS FORRÁS**. https://github.com/paradedb/paradedb/issues/1685
- **#5449** — *"CREATE INDEX CONCURRENTLY USING bm25 fails with missing \"pg_tblspc/...\" file under concurrent writes"* — érintett verziók **0.21.6 és 0.24.1**; a maintainer (Rohan-Singla) megerősítette a reprodukálást, javítási határidő nincs megadva. https://github.com/paradedb/paradedb/issues/5449
- **#6208** — *"CREATE INDEX CONCURRENTLY leaks buffer pins and fails on PG 15 and 16 when the table is being written"* — gyökérok: egy PG15/16-os polyfill (`fake_aminsertcleanup.rs`); PostgreSQL 17+ natív `index_insert_cleanup` funkciója miatt ott nem jelentkezik. https://github.com/paradedb/paradedb/issues/6208
- **#5999** — *"JoinScan anti-joins regress from PostgreSQL parallel execution in 0.24.3 to MPP in 0.25.3"* — teljesítmény-regresszió (35-36 ms → 67 ms, azaz 1,47–1,89×), amit a maintainer úgy zárt le, hogy *"the user upgraded to 0.25.x, so things seem to be fine here"* — ez **nem** a gyökérok igazolt javítása, csak a bejelentő elégedettségének regisztrálása. https://github.com/paradedb/paradedb/issues/5999

### 2.6. Upgrade / migrációs hiba

**Issue #2436** — *"Can't migrate 0.15.11 > 0.15.16 due to missing file `pg_analytics`"*
URL: https://github.com/paradedb/paradedb/issues/2436 — **Zárva**, nyitva: **2025.04.16.**, WSL2 (Ubuntu 20.04.6), Docker 20.10.22, ParadeDB Docker image. A felhasználó több korábbi migráción átment (0.9.3→0.10.0→0.15.2→0.15.3→0.15.11), majd a 0.15.16-ra frissítés az `pg_analytics` fájl hiánya miatt elakadt, és a felhasználó a hibajegy szövege szerint a régi verzión ragadt.

---

## 3. Írási költség: BM25 index frissítése, write amplification, szegmens-összefésülés

**Hivatalos dokumentáció — "Write Throughput"** (aktuális, v0.25.9-korabeli állapot):
URL: https://docs.paradedb.com/documentation/performance-tuning/writes

Szó szerinti idézetek:
- *"During every `INSERT`/`UPDATE`/`COPY`/`VACUUM`, the ParadeDB index runs a compaction process that looks for opportunities to merge segments together."*
- Alapértelmezett háttér-réteg méretek: *"The default background layer sizes are `100KB`, `1MB`, `10MB`, `100MB`, `1GB`, and `10GB` but can be configured."*
- Előtér vs. háttér összefésülés: *"By default, merging happens in the background so that writes are not blocked. The `layer_sizes` option allows merging to happen in the foreground. This is not typically recommended because it slows down writes, but can be used to apply back pressure to writes if segments are being created faster than they can be merged down."*
- Memóriaigény: *"Each statement that writes to a ParadeDB index is required to have at least `15MB` memory."*
- `mutable_segment_rows` (alapértelmezett **1000**): *"A higher value generally improves write throughput at the expense of read performance, since the mutable data structure is slower to search. Additionally, the mutable data structure is read into memory, so higher values cause reads to consume more RAM."*

Megjegyzés: a jelenlegi hivatalos oldalak szövegében a **"write amplification" kifejezés szó szerint NEM szerepel** (ellenőrizve `grep`-pel a teljes dokumentáció-dumpon, `docs.paradedb.com/llms-full.txt`) — ez a fogalom a blogbejegyzésben (ld. lent) jelenik meg explicit módon.

**Hivatalos blog — "Postgres as a Search Engine: The Write Performance Problem"** (T2, ParadeDB saját mérése), szerzők **Ming Ying és James Blackwood-Sewell**, közzététel: **2025.12.15.**
URL: https://www.paradedb.com/blog/increased-write-performance

Idézetek:
- *"updating a single field requires reindexing and serializing all fields which are stored alongside it, and merging these data structures during compaction adds significant write overhead."*
- *"Each write operation touches multiple data structures, and the periodic merge operations can create significant write amplification as thousands of tiny segments get rolled up into bigger ones."*
- Történeti (önjelentett) mérési adatok update-áteresztésről: **v0.18.0: 120 update/mp**, **v0.19.0: 1857 update/mp**, **v0.20.0: 2016 update/mp** — a cikk ezt *"more than a 10x improvement in write throughput"*-ként jellemzi (a nyers számok kb. 16×-os javulást mutatnak a legrégebbi és legújabb verzió között).
- Megoldásként bevezetett háttér-workerek: *"foreground writes never block on merge operations"*, és *"multiple workers to handle different merge operations concurrently"*.

**Kapcsolódó GitHub-issue-bizonyíték az írási költség valós hatásáról:**
- **#1685** (2024.09.19., v0.8.6): >3M soros táblánál UPDATE/SELECT lockolt, lefagyott tranzakciók — ez a korai (2024 közepi, még az optimalizálás előtti) verziókra jellemző súlyos írási teljesítményproblémát dokumentál. https://github.com/paradedb/paradedb/issues/1685
- **#6374** (2026.09.17.): egyetlen sor **két egymást követő UPDATE**-je egy mutable szegmensbe SIGSEGV-t okozott párhuzamos top-k scan mellett — azaz az írási útvonal (mutable segment) és az olvasási útvonal interakciójában **jelenleg (2026 szeptemberében) is** van feltárt, súlyos hiba. https://github.com/paradedb/paradedb/issues/6374
- **#6375** (2026.09.17.): HOT UPDATE + VACUUM után JOIN-eredmények vesztek el — szintén az írási/karbantartási művelet (VACUUM) és az olvasás interakciójában. https://github.com/paradedb/paradedb/issues/6375

---

## 4. Ismert korlátok a hivatalos dokumentációból

**Forrás — "Limitations & Tradeoffs"** (aktuális, v0.25.9-korabeli állapot):
URL: https://docs.paradedb.com/welcome/limitations

- **Elosztott terhelés / méret:** *"ParadeDB is designed to scale vertically on a single Postgres primary, and many production deployments comfortably operate in the 1–10TB range. Enterprise deployments can add read replicas for ParadeDB queries. The largest single ParadeDB database we've seen in production is 10TB."* Nagyobb adathalmazhoz: *"ParadeDB supports partitioned tables and can be deployed in sharded Postgres configurations... fully compatible with Citus for distributed search workloads."*
- **Fedő-index (covering index) korlát:** *"The ParadeDB index is a covering index, which means it stores all indexed columns inside a single index per table... this means that all columns must be defined up front at index creation time. Adding or removing columns requires a `REINDEX`."*
- **DDL replikáció:** *"A well-known limitation of Postgres logical replication is that DDL (Data Definition Language) statements are not replicated... If ParadeDB is running as a logical replica of a primary Postgres, DDL statements from the primary must be executed manually on the replica."*

**Forrás — "ParadeDB Enterprise" (Community vs. Enterprise táblázat):**
URL: https://www.paradedb.com/docs/operate/deploy/enterprise

- *"[ParadeDB Community](https://github.com/paradedb/paradedb) is the AGPL-3.0 open source product. It supports single-node deployments."*
- Táblázat-sorok szó szerint: **"Maximum ParadeDB index nodes"**: Community = **1**, Enterprise = **Unlimited**. **"High Availability for ParadeDB indexes"**: Community ❌, Enterprise ✅. **"Read replicas for ParadeDB queries"**: Community ❌, Enterprise ✅. **"Crash Recovery"**: mindkettő ✅. **"Point in Time Recovery"**: mindkettő ✅.
- Lábjegyzet: *"In a primary-replica topology, ParadeDB indexes in ParadeDB Community are only available on the primary because Community does not physically replicate the ParadeDB index."* Ugyanakkor: *"ParadeDB Community can still use standard Postgres replication, crash recovery, and point-in-time recovery for heap tables and other Postgres indexes like B-tree indexes."*

**Fizikai (streaming) replikáció olvasása — megerősítve GitHub Discussion-ből is:**
URL: https://github.com/orgs/paradedb/discussions/3521 (kérdés: hjaber, 2025.11.10.; válasz: philippemnoel, maintainer, 2025.11.11.)
Idézett hibaüzenet (v0.19.5 Community): *"Serving reads from a standby requires write-ahead log (WAL) integration, which is supported on ParadeDB Enterprise, not ParadeDB Community."* Maintainer megerősítése: *"streaming/read replicas has always been enterprise-only."* Ugyanakkor v0.18.10-en még hibátlanul működött ugyanez a felhasználói setup — azaz a hibaüzenet explicitté tétele (nem az alapvető korlát) v0.19.0 körül történt.

**Oszlop/index-korlátok — natív Postgres 32-oszlopos limit ParadeDB alatt:**
URL: https://www.paradedb.com/docs/reference/indexing/indexing-composite
*"Postgres allows a maximum of 32 columns in an index definition, but because ParadeDB benefits from pushing filters and ranking signals into the ParadeDB index this can become a limitation."* Megoldás **v0.22.0-tól**: kompozit típusok `ROW()`-ba csomagolva. Korlátok a kompozit megoldásra: *"Anonymous ROW expressions... not allowed."*, *"Nested composites: A composite type cannot contain another composite type as a field."*, *"Duplicate field names: Field names must be unique within a single ParadeDB index."*

**JOIN-támogatás (aktuális dokumentáció):**
URL: https://www.paradedb.com/docs/reference/joins/overview
*"ParadeDB supports all standard Postgres `JOIN` types, including: `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, `FULL JOIN`, `SEMI JOIN`, `ANTI JOIN`, `CROSS JOIN`."* A join pushdown (index-be tolt JOIN-végrehajtás) csak akkor aktiválódik, ha minden résztáblának van ParadeDB indexe, van search-operátor a lekérdezésben, minden JOIN-kulcs/szűrő/ORDER BY oszlop indexelt (szöveg/JSON esetén columnar), és van LIMIT — egyébként *"ParadeDB will emit a `NOTICE` explaining why and fall back to Postgres' native join execution."`

**Támogatott oszloptípusok / filter pushdown (részlet):**
URL: https://www.paradedb.com/docs/reference/filtering/indexed
Táblázatban dokumentált típus-operátor kombinációk: `int2/int4/int8`, `float4/float8`, `numeric`, `date`, `time`, `timetz`, `timestamp`, `timestamptz`, `uuid` (összehasonlító operátorokhoz), `bool` (egyenlőség), valamint `IN`/`ANY`/`ALL` tömb-operátorok ugyanezekhez a típusokhoz.

**Particionált táblák:** a fenti Limitations-oldal állítása szerint támogatottak, kiegészítő extension-ként a `pg_partman` is tesztelt és kompatibilis (*"ParadeDB has been tested with and supports the following popular extensions: ... `pg_partman` — Automated partition management"*, https://www.paradedb.com/docs/operate/deploy — llms-full.txt 16962. sor környéke). **Konkrét számszerű korlát** (pl. max. partíciószám egy index alatt) a dokumentációban **NINCS FORRÁS**.

**Kritikus, verzióhoz köthető durability-tény:**
URL: https://www.paradedb.com/docs/concepts/guarantees
*"As of `0.24.0`, transactions in ParadeDB Community are also durable, meaning they are write-ahead (WAL) logged and will survive crashes."*
Megerősítve a v0.24.0 release note-okból (**2025.06.03.**): https://github.com/paradedb/paradedb/releases/tag/v0.24.0 — *"feat: Crash recovery via WAL by @rebasedming in #4901"*, illetve *"docs: remove WAL/durability caveats by @rebasedming in #5091"*.
Ez azt jelenti, hogy **2025.06.03. előtt** a ParadeDB Community BM25-indexének adatai a hivatalos dokumentáció korábbi állapota szerint feltehetően **nem voltak garantáltan crash-safe-ek** (a "caveat" eltávolítása maga is bizonyíték arra, hogy korábban létezett ilyen figyelmeztetés) — magát a korábbi figyelmeztető szöveget nem sikerült szó szerint lekérni (**NINCS FORRÁS** a pontos, eredeti caveat-szövegre), csak a törléséről szóló commit-üzenetre.

**Egy további, korábbi (2024.10.14., v0.19.0-ás) release-note-sor, amely önmagában érdemel figyelmet, de nem sikerült a teljes eredeti szöveget megtalálni:**
URL: https://github.com/paradedb/paradedb/releases/tag/v0.19.0
*"docs: Caution that ParadeDB Community should not be run in production by @rebasedming in #3269"* — ez egy commit-üzenet/PR-cím, nem a tényleges dokumentációs szöveg; a pontos, akkori figyelmeztetés-szöveg **NINCS FORRÁS**-ként kezelendő, mert nem sikerült elérni a #3269 PR tartalmát vagy az akkori doksi-verziót.

**CVE / biztonsági rés:** célzott keresés nem hozott felszínre nyilvántartott CVE-azonosítót a ParadeDB/pg_search-höz. **NINCS FORRÁS** konkrét CVE-re (ez nem jelenti azt, hogy nincs ilyen, csak hogy a keresés nem talált).

---

## 5. Közösségi tapasztalat (T3)

A feladat kifejezetten előírja, hogy Hacker News / Reddit / blog-alapú állítást **csak akkor** szabad idézni, ha **legalább két, egymástól független beszámoló egyezik**. Ez alapján:

- **Reddit:** több célzott keresés (`site:reddit.com paradedb`, `reddit.com/r/PostgreSQL paradedb`, `reddit paradedb "pg_search" experience`) **gyakorlatilag nulla releváns találatot** adott (csak "Parade" szóra illeszkedő, teljesen irreleváns Wikipédia-szócikkek jöttek vissza). **NINCS FORRÁS** Reddit-alapú éles-használati tapasztalatra.
- **Hacker News:** léteznek releváns szálak (pl. *"ParadeDB – PostgreSQL for Search"*, https://news.ycombinator.com/item?id=38847571, 2024; *"One of the ParadeDB maintainers here..."*, https://news.ycombinator.com/item?id=44637543, 2025), és a keresési index néhány rövid, önmagában is szó szerinti töredéket adott vissza (pl. egy hozzászólás-cím: *"AWS RDS support is key IMO, I have done a lot of consulting on infrastructure an..."*, https://news.ycombinator.com/item?id=41180134 — csonkolt). A teljes szálak elolvasását a `WebFetch`-eszköz **429-es rate-limit-tel elutasította**, és kifejezetten arra utasított, hogy ne próbálkozzak újra ("Do not fetch this page again, even after waiting"). Mivel csak cím-töredékeket kaptam, nem a tényleges hozzászólás-szövegeket, és nincs második, tőlük független beszámoló, amivel egyeztetni tudnám őket, ezen a ponton **NINCS FORRÁS** megbízható, két forrással alátámasztott közösségi tapasztalatra.
- A talált blogok/benchmarkok (Vineeth Pothulapati, inevolin GitHub repó) inkább technikai mérések, mint "éles használat/elvetés" jellegű beszámolók — ezeket az 1. szakaszban T2-ként már szerepeltettem, itt nem duplikálom T3-ként.

**Összegzés erre a pontra: a kötelező kettős-megerősítési szabály miatt konkrét, névvel/dátummal azonosítható közösségi éles-tapasztalat állítást ehhez a kutatáshoz NEM tudok megbízhatóan idézni.**

---

## Ellentmondások

1. **Ki a gyorsabb — nincs egyértelmű válasz, kontextusfüggő:** a saját ParadeDB-benchmark (T2) szerint 40 kifejezéses rotáló terhelésnél ParadeDB **29×–47×** gyorsabb a natív Postgres FTS-nél; a Vineeth Pothulapati független teszt (T2) szerint viszont **pontos frázis-keresésnél a natív Postgres volt 14× gyorsabb** ParadeDB-nél ugyanabban a tesztben, míg fuzzy/mező-specifikus keresésnél ParadeDB volt drámaian (48×–164×) gyorsabb. A két forrás nem egymást cáfolja, hanem azt mutatja, hogy **a lekérdezés típusa dönti el a győztest** — ezt egyik forrás sem tagadja, de a "ParadeDB gyorsabb" vagy "Postgres elég" leegyszerűsítő állítás egyik forrással sem támasztható alá általánosan.
2. **ParadeDB vs. Elasticsearch nyers lekérdezés-átbocsátás:** az inevolin-féle független benchmark (T2) szerint nagy egyidejűségnél (50 kliens, 1M dok) **Elasticsearch ~1,9×-szer gyorsabb** tiszta lekérdezés-átbocsátásban, miközben ParadeDB ~3×-szor gyorsabban tölti be/indexeli ugyanazt az adatot. Ez ellentmond a marketing-jellegű "ParadeDB = gyorsabb Elasticsearch-alternatíva" narratívának, amit maga a ParadeDB is hirdet (pl. https://www.paradedb.com/blog/introducing-search — ezt az oldalt nem kérdeztem le részletesen, mert marketing-jellegű, T1/T2 mérési adat nélkül).
3. **A JOIN-támogatás dokumentált terjedelme verziónként változott:** a jelenlegi (v0.25.9-korabeli) hivatalos oldal szerint ParadeDB **minden** standard Postgres JOIN-típust támogat natív Postgres-fallback-kel, és a join pushdown csak optimalizáció. Egy korábbi keresési találat (nem kérdeztem le mélységben, csak a keresési index szintjén jelent meg) v0.22.0-hoz "beta" join pushdownt említett kizárólag INNER/SEMI/ANTI-ra. Ez inkább **időbeli fejlődés**, mint valódi ellentmondás, de mivel a korábbi állítás pontos forrását nem ellenőriztem le, itt csak a jelenlegi, verifikált (curl-lel is ellenőrzött) állapotot tekintem megbízhatónak, és jelzem a bizonytalanságot.
4. **A #5999 teljesítmény-regresszió "lezárása" nem valódi javítás-igazolás:** a maintainer azzal zárta le a hibajegyet, hogy a bejelentő időközben frissített és "úgy tűnik, minden rendben" — ez nem azonos a gyökérok igazolt kijavításával, tehát nyitva marad a kérdés, hogy a 0.24.3→0.25.3 MPP-regresszió strukturálisan megoldódott-e, vagy csak az adott felhasználó konfigurációjában tűnt el.

## Amire NINCS forrás

- Pontos, számszerű limit particionált táblák/partíciók számára egy ParadeDB index alatt.
- A v0.24.0 előtti időszak eredeti, szó szerinti "WAL/durability caveat" szövege a dokumentációból (csak a törlést jelző commit-üzenetet találtam).
- A v0.19.0-ás "ParadeDB Community should not be run in production" caution eredeti, teljes szövege (csak a release-note commit-cím ismert).
- Közvetlen, azonos módszertanú ParadeDB-vs-SQLite-FTS5 és ParadeDB-vs-OpenSearch független mérés.
- Két egymástól független, tartalmilag egyező Reddit- vagy Hacker News-alapú éles-használati beszámoló (a HN-tartalom rate-limit miatt nem volt olvasható, a Reddit-keresés releváns találat nélkül tért vissza).
- Nyilvántartott CVE-azonosító a ParadeDB/pg_search-re.
- A törölt GitHub issue-k (#1406, #1407, #1631, #1895, #1207) eredeti tartalma és törlésük oka.
- Javítási verziószám a #2575 (DELETE-hiba) és #5449 (CONCURRENTLY-hiba) esetére.
- Pontos dátum az inevolin/ParadeDB-vs-ElasticSearch benchmark közzétételére.
- Második, a SereneDB-től teljesen független megerősítés a SereneDB-benchmark 1 milliárd soros eredményeire.

---



---

# ELL01 — Licenc, kiadás és a cég helyzete

> **Módszertani megjegyzés.** Ez adverzariális ellenőrzés: a cél az sq01/sq02 korábbi állításainak megdöntése, nem megerősítése. A kötelező kereső­eszköz az **Exa** volt (`mcp__Exa__web_search_exa`, `mcp__Exa__web_fetch_exa`) — mindkettő elérhető volt és kizárólagosan ezekkel kerestem/olvastam oldalakat; beépített `WebSearch`/`WebFetch` egyszer sem futott. `curl`-t kizárólag nyers, verbatim ellenőrzésre használtam: GitHub raw fájlok (`LICENSE`, `Cargo.toml`, `CONTRIBUTING.md`, `README.md`), a Docker Hub és PGXN gépi API-i (kiadási jegyzékek), valamint a hivatalos GNU AGPL-3.0/FAQ szövegek nyers `.txt`/`.html` verziói. Egy esetben (`docs.paradedb.com/deploy/enterprise`) a `curl`-lal lekért nyers HTML kliensoldalon renderelt (JS-alapú) oldalnak bizonyult, üres tartalommal — ezért a tényleges szöveget Exa-fetch-csel szereztem be, ez az egyetlen pont, ahol a `curl`-teszt önmagában félrevezető lett volna (l. 2. állítás). Alügynök-fan-out (Sonnet-kereső / Opus-szintézis) ebben a környezetben nem indítható, ezért egyetlen szálon, szekvenciálisan dolgoztam — ez a `_ell_kozos.txt` szerinti degradált mód. Minden verdiktet igyekeztem két, egymástól független forrással alátámasztani; ahol ez nem sikerült, jelzem.

## Verdikt-összefoglaló

| # | Állítás | Verdikt | Egy mondat |
|---|---|---|---|
| 1 | `paradedb/paradedb` (pg_search) licence ma AGPL-3.0; legfrissebb stabil kiadás v0.25.9 (2026-09-11) | **RÉSZBEN IGAZOLVA** | A licenc (AGPL-3.0) tökéletesen igazolt; a v0.25.9/2026-09-11 verziót két független, géppel olvasható registry (Docker Hub API, PGXN) is megerősíti, de a GitHub saját „latest release" oldala (Exa-fetch) ellentmondóan v0.25.6-ot (2026-08-27) mutatott. |
| 2 | Van fizetős Enterprise; hivatalos összehasonlítás szerint a keresési funkciók azonosak, a különbség replikáció/HA/olvasó replikák (standby-olvasás csak Enterprise-ban) | **RÉSZBEN IGAZOLVA** | A funkcionális összehasonlítás (keresés/index azonos, HA+Read Replica csak Enterprise-ban, standby-olvasás Community-n technikailag tiltott) szó szerint stimmel, de az állítás hiányos: a hivatalos oldal szerint az Enterprise emellett **licencben is más** ("waives the copyleft provision of AGPL-3.0") és tartalmaz nem specifikált zárt forráskódú funkciókat is. |
| 3 | A cég minden közreműködőtől CLA-t kér, amely AGPL **és** kereskedelmi licencelést is lehetővé tesz | **IGAZOLVA** | A `CONTRIBUTING.md` szó szerint kimondja, hogy a hozzájárulás egyszerre AGPL-3.0 **és** kereskedelmi szoftver licence alá kerül, amit a CLA saját, tág szerzői jogi engedmény-szövege is alátámaszt. |
| 4 | A licenc „a kezdetektől" AGPL; a korábbi `pg_analytics` PostgreSQL License alatt futott, 2025-03-19-én archiválták | **IGAZOLVA** (a „from day one" rész a cég saját, nem független állítása) | A `pg_analytics` PostgreSQL License-e és 2025-03-19-i archiválása közvetlenül, két forrásból igazolt; az „AGPL a kezdetektől" kizárólag a cég 2024-es utólagos blogbejegyzésén nyugszik, 2023-as független forrás erre nem található. |
| 5 | A Neon 2026 márciusában bejelentette a `pg_search` kivezetését, teljes megszűnés 2026-09-21 | **IGAZOLVA** | A Neon két hivatalos, egymástól különböző dokumentációs oldala szó szerint megerősíti: új projekteken 2026. március 19. óta nem elérhető, meglévő telepítéseket 2026. szeptember 21-én távolítják el. |
| 6 | Létezik a Timescale/TigerData `pg_textsearch` BM25-bővítménye PostgreSQL License alatt — érettség, verzió, támogatott Postgres, magyar nyelv, BM25 | **IGAZOLVA** | PostgreSQL License megerősítve; jelenlegi verzió v1.4.0 (2026-08-18), csak PG 17–18-at támogat (19 béta best-effort), valódi BM25-rangsorolást ad, és a magyar ("hungarian") szerepel a támogatott 29 Postgres text-search-konfiguráció között — de a projekt előzetes kiadása csak 2025-10-23-i, tehát kevesebb, mint egy éve fejlesztik. |
| 7 | AGPL-3.0 13. § a módosított program hálózati elérésére vonatkozik (szó szerint); van-e ParadeDB-saját nyilatkozat a csak SQL-en beszélő, változatlan klienshasználatra | **RÉSZBEN IGAZOLVA** | A 13. § szó szerinti szövege pontosan igazolt és megegyezik a ParadeDB saját `LICENSE` fájljával; ugyanakkor semmilyen hivatalos ParadeDB-oldal, FAQ vagy blogbejegyzés nem foglalkozik kifejezetten azzal az esettel, amikor egy külön folyamatban futó alkalmazás csupán SQL-en (Postgres wire protocol-on) keresztül, a `pg_search`-öt nem módosítva használja azt — ilyen nyilatkozat nem található. |

---

## Állításonként

### 1. Licenc és legfrissebb stabil kiadás

**Licenc — teljesen igazolva.** A `paradedb/paradedb` monorepó gyökér `LICENSE` fájlja (nyers fájl, `curl`, 2026-09-22, HTTP 200):

> „GNU AFFERO GENERAL PUBLIC LICENSE
> Version 3, 19 November 2007"

Forrás: https://raw.githubusercontent.com/paradedb/paradedb/main/LICENSE

A `Cargo.toml` workspace-szekciója megerősíti:

> „[workspace.package]
> version = \"0.25.6\"
> edition = \"2024\"
> license = \"AGPL-3.0\""

Forrás: https://raw.githubusercontent.com/paradedb/paradedb/main/Cargo.toml (curl, 2026-09-22)

**Verzió/dátum — két független, géppel olvasható forrás egyezik, a GitHub saját oldala viszont nem.**

Docker Hub hivatalos API (`paradedb/paradedb` szervezeti fiók, `curl`, közvetlen JSON, 2026-09-22):

```
v0.25.9   2026-09-11T18:28:54.209419Z
0.25.9    2026-09-11T18:28:57.099286Z
```

Forrás: https://hub.docker.com/v2/repositories/paradedb/paradedb/tags?page_size=20&ordering=last_updated

PGXN (PostgreSQL Extension Network), önálló, verziószámozott URL (Exa-fetch, 2026-09-22):

> „# pg_search 0.25.9
> pg_search 0.25.9: Full text search for PostgreSQL using BM25 / PostgreSQL Extension Network"

Forrás: https://pgxn.org/dist/pg_search/0.25.9/ (a `https://pgxn.org/dist/pg_search/0.25.9/META.json` közvetlen géppel-olvasható változata 404-et adott ezen a napon, de a HTML-oldal maga létezik és verzió-specifikus).

**Ellentmondás:** a GitHub saját „latest release" oldala (Exa-fetch, 2026-09-22) ugyanekkor ezt adta vissza:

> „# v0.25.6
> - Tag: v0.25.6
> - Published: 2026-08-27T21:44:47Z"

Forrás: https://github.com/paradedb/paradedb/releases/latest

Ez logikailag ellentmond a Docker Hub-adatnak (a v0.25.9 tag később, 2026-09-11-én jelent meg, mint a v0.25.6 2026-08-27-i dátuma, tehát ha létezik, a GitHub „latest"-nek is azt kellene mutatnia). A `curl`-lal indított közvetlen GitHub API-hívás (`api.github.com/repos/paradedb/paradedb/releases/latest`) ebben a környezetben HTTP 403-at adott („GitHub access to this repository is not enabled for this session"), így ezt nem lehetett közvetlenül feloldani; a legvalószínűbb magyarázat egy elavult Exa-crawler-cache a GitHub dinamikus oldalán, nem valódi adatellentmondás — de ezt nem sikerült bizonyítani, csak valószínűsíteni.

### 2. Enterprise vs. Community — funkciók és licenc

A hivatalos oldal aktuális, teljes szövege (Exa-fetch, kétszer lekérve különböző URL-eken — `docs.paradedb.com/deploy/enterprise` és a canonicalizált `www.paradedb.com/docs/operate/deploy/enterprise`, mindkettő ugyanazt a tartalmat adta, 2026-09-22):

> „ParadeDB Community is our open source product, licensed under AGPL-3.0. This license permits free use, modification, and distribution of the software, provided that distributed, derivative works of the software are released under the same license (copyleft provision).
>
> In addition to all of the features of ParadeDB Community, ParadeDB Enterprise:
> 1. Waives the copyleft provision of AGPL-3.0
> 2. Contains several closed-source features that are recommended for ParadeDB to service enterprise, production workloads"

A „Feature Comparison" táblázat szó szerint (kivonat):

> „| | ParadeDB Community | ParadeDB Enterprise |
> | BM25 scoring | ✅ | ✅ |
> | Hybrid search | ✅ | ✅ |
> | Query builder API | ✅ | ✅ |
> | Highlighting | ✅ | ✅ |
> | Maximum cluster size | 1 | Unlimited |
> | Logical Replication | ✅ | ✅ |
> | High Availability Support | ❌ | ✅ |
> | Read Replica Support | ❌ | ✅ |"

Forrás: https://docs.paradedb.com/deploy/enterprise

Tehát a keresési/index funkciók (BM25, hibrid keresés, highlighting, aggregátumok stb.) valóban azonosak — de az Enterprise **nem csak** funkcionálisan más: saját megfogalmazásuk szerint a kereskedelmi verzió a copyleft-kötelezettséget is feloldja, plusz „several closed-source features"-t tartalmaz, amit a táblázat nem sorol fel tételesen.

**„Standby-ról olvasás csak Enterprise-ban" — közvetlenül igazolva**, mégpedig egy éles GitHub-hibaüzenet szó szerinti szövegével (2026, nyitott issue):

> „replicas are not supported on community and require paradedb enterprise, which guarantees physical replication safety on standbys."

Forrás: https://github.com/paradedb/paradedb/issues/6007 („Community ParadeDB index creation stops all PostgreSQL physical replication")

Ezt megerősíti a hivatalos „Guarantees" oldal is:

> „ParadeDB Community supports logical replication, but not physical replication: […] The ParadeDB index does not get physically replicated and won't be available on other nodes in a high availability setup.
> ParadeDB Enterprise supports both: […] It supports physical replication and high availability, ensuring that the ParadeDB index remains consistent and crash-safe across nodes."

Forrás: https://docs.paradedb.com/welcome/guarantees

### 3. CLA — AGPL és kereskedelmi licencelés egyszerre

A `CONTRIBUTING.md` (nyers fájl, `curl`, 2026-09-22, HTTP 200) „Legal Info" szakasza szó szerint:

> „In order for us, ParadeDB, Inc., to accept patches and other contributions from you, you need to adopt our ParadeDB Contributor License Agreement (the \"CLA\"). […]
>
> ### License
> By contributing to ParadeDB, you agree that your contributions will be licensed under the [GNU Affero General Public License v3.0](LICENSE) **and as commercial software**."

Forrás: https://raw.githubusercontent.com/paradedb/paradedb/main/CONTRIBUTING.md

Második, független forrás — maga a CLA-dokumentum (a társalapító, philippemnoel publikus gist-je, 2024-01-25), amely a tág szerzői jogi engedményt adja meg, ami a fenti kettős licencelést jogilag lehetővé teszi:

> „Grant of Copyright License. […] You hereby grant to the Company and to recipients of software distributed by the Company a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable copyright license to reproduce, prepare derivative works of, publicly display, publicly perform, sublicense, and distribute Your Contributions and such derivative works."

Forrás: https://gist.github.com/philippemnoel/5ba3a20230bc1c3c0ae89caeb0597f4a (hivatkozva a `CONTRIBUTING.md`-ben is, mint „CLA Assistant website": https://cla-assistant.io/paradedb/paradedb)

### 4. Licenctörténet: „AGPL a kezdetektől" és a `pg_analytics` PostgreSQL License

A `pg_analytics` (korábban `pg_lakehouse`) repó `LICENSE` fájlja (nyers fájl, `curl`, 2026-09-22, HTTP 200):

> „The PostgreSQL License
>
> Copyright (c) 2025, ParadeDB
>
> Permission to use, copy, modify, and distribute this software and its documentation for any purpose, without fee, and without a written agreement is hereby granted…"

Forrás: https://raw.githubusercontent.com/paradedb/pg_analytics/dev/LICENSE

Az archiválás dátuma két, egymástól független módon igazolt:

1. GitHub repó-metaadat (Exa-fetch, 2026-09-22): „Status: ARCHIVED", „This repository was archived by the owner on Mar 19, 2025. It is now read-only." — forrás: https://github.com/paradedb/pg_analytics és https://github.com/paradedb/pg_analytics/releases
2. Az utolsó kiadási tag időbélyege pontosan egybevág: „v0.3.7 — Published: 2025-03-19T19:27:38Z — feat: Final release" — forrás: https://github.com/paradedb/pg_analytics/releases/tag/v0.3.7

Egy harmadik, tartalmilag konzisztens (bár azonos cégtől, más aldomainről származó) forrás a döntés indoklását is adja:

> „On April 2, 2025, we will be deprecating `pg_analytics` […] The `pg_analytics` repository will be archived and will no longer be maintained. […] This decision was made because our work on Postgres analytics is being done in our primary extension, `pg_search`."

Forrás: https://paradedb-dev.mintlify.site/changelog/0.15.9

Az „AGPL a kezdetektől" állítás forrása a cég saját, 2024. augusztusi blogbejegyzése:

> „ParadeDB has been licensed under the GNU Affero General Public License 3.0 — also known as AGPL — from day one."

Forrás: https://www.paradedb.com/blog/agpl

Ez **nem független, utólagos (kb. 1 évvel az alapítás után írt) önbevallás** — 2023-as, a céghez nem köthető, korabeli forrás nem található rá (a Wayback Machine ebben a környezetben blokkolva volt, és az Exa-találatok között sem szerepelt ilyen). A `pg_analytics` esete ugyanakkor bizonyítja, hogy **nem minden ParadeDB-komponens** volt/és AGPL — csak a fő motor.

### 5. Neon — `pg_search` kivezetése

Neon hivatalos changelog-bejegyzés (2026-04-03, Exa-fetch):

> „### pg_search deprecation
> Neon support for the `pg_search` extension is deprecated. As of **March 19, 2026**, it is not available for **new** Neon projects.
> If you already use `pg_search`: you will continue to have access to the extension on your existing projects."

Forrás: https://neon.com/docs/changelog/2026-04-03

A migrációs útmutató a teljes megszűnés dátumát adja meg:

> „`pg_search` (ParadeDB) is deprecated on Neon: new installs are blocked, and **existing installs will be removed on September 21, 2026**."
>
> „Once your queries run on `lakebase_text` […], drop `pg_search` ahead of the September 21, 2026 removal."

Forrás: https://neon.com/docs/extensions/migrate-pg-search-to-lakebase-text

Egy harmadik, tőle független forrás (felhasználói GitHub-vita) megerősíti a piaci hatást is:

> „Neon has stopped allowing new `pg_search` installations and says existing installations will be removed in September 2026. This has already caused some new self-hosted deployments to fail during database migration."

Forrás: https://github.com/lobehub/lobehub/issues/18303

### 6. `pg_textsearch` (Timescale/TigerData) érettsége

Licenc — nyers fájl (`curl`, 2026-09-22, HTTP 200):

> „The PostgreSQL License
> Permission to use, copy, modify, and distribute this software and its documentation for any purpose, without fee, and without a written agreement is hereby granted…"

Forrás: https://raw.githubusercontent.com/timescale/pg_textsearch/main/LICENSE

Verzió és dátum (Exa-fetch, GitHub release-oldal, közvetlen, 2026-09-22):

> „# v1.4.0
> Published: 2026-08-18T17:05:02Z
> * Optimizations for top-K queries with a WHERE filter (aka faceted search) yielding significant (up to 5X) speedups […]
> * Chinese-language support via zhparser
> * Robustness improvements for large corpuses"

Forrás: https://github.com/timescale/pg_textsearch/releases/tag/v1.4.0

Támogatott Postgres-verziók (README, Exa-fetch):

> „pg_textsearch supports PostgreSQL 17 and 18. PostgreSQL 19 (beta) is supported on a best-effort basis while it is in beta; its CI is allowed to fail and prebuilt binaries are not published for it yet."

Forrás: https://github.com/timescale/pg_textsearch/blob/main/README.md — ez **szűkebb** támogatott sáv, mint a `pg_search` PG 15–18 tartománya.

BM25: valódi, konfigurálható BM25-rangsorolás (`k1`, `b` paraméterek, Block-Max WAND gyorsítás):

> „BM25 ranking with configurable `k1` and `b`", „Fast top-k queries with Block-Max WAND"

Forrás: https://github.com/timescale/pg_textsearch (README)

**Magyar nyelv — igazolva.** A README saját, explicit felsorolása a támogatott Postgres text-search-konfigurációkról tartalmazza a magyart:

> „### Text Search Configurations
> Available configurations depend on your Postgres installation:
> ```
> # SELECT cfgname FROM pg_ts_config;
>   cfgname
> ------------
>  simple
>  arabic
>  armenian
>  …
>  hungarian
>  …
>  yiddish
> (29 rows)
> ```
> Further language support is available via extensions such as [zhparser]."

Forrás: https://github.com/timescale/pg_textsearch/blob/main/README.md

Érettség/kor: a Tiger Data (korábban TimescaleDB) saját blogja szerint az előzetes (preview) kiadás 2025-10-23-án jelent meg:

> „We're announcing the preview release of a PostgreSQL extension built specifically for this third epoch…"

Forrás: https://www.tigerdata.com/blog/introducing-pg_textsearch-true-bm25-ranking-hybrid-retrieval-postgres (2025-10-23)

Vagyis a projekt a kutatás időpontjában (2026-09-22) **kevesebb, mint 11 hónapja** létezik nyilvánosan, jelenlegi verziója v1.4.0 — a v1.0.0-tól v1.4.0-ig gyors, havi-kéthavi kiadási ütemben fejlesztik (a releases-lista szerint v1.0.0, v1.1.0, v1.2.0, v1.3.0, v1.3.1, v1.4.0 egymást követik néhány hetes-hónapos távolságokban), de érettségben (támogatott PG-verziók száma, kiadások kora) egyértelműen fiatalabb, mint a `pg_search`.

### 7. AGPL-3.0 13. szakasz és a ParadeDB saját nyilatkozata

A hivatalos GNU-szöveg (`curl`, https://www.gnu.org/licenses/agpl-3.0.txt, 2026-09-22, HTTP 200), szó szerint:

> „13. Remote Network Interaction; Use with the GNU General Public License.
>
> Notwithstanding any other provision of this License, if you modify the Program, your modified version must prominently offer all users interacting with it remotely through a computer network (if your version supports such interaction) an opportunity to receive the Corresponding Source of your version by providing access to the Corresponding Source from a network server at no charge, through some standard or customary means of facilitating copying of software. This Corresponding Source shall include the Corresponding Source for any work covered by version 3 of the GNU General Public License that is incorporated pursuant to the following paragraph.
>
> Notwithstanding any other provision of this License, you have permission to link or combine any covered work with a work licensed under version 3 of the GNU General Public License into a single combined work, and to convey the resulting work. The terms of this License will continue to apply to the part which is the covered work, but the work with which it is combined will remain governed by version 3 of the GNU General Public License."

Ez **szóról szóra megegyezik** a ParadeDB repó saját `LICENSE` fájljával (`curl`, https://raw.githubusercontent.com/paradedb/paradedb/main/LICENSE, ugyanaz a szövegrész, sorindex 540–559) — tehát a ParadeDB nem módosította a szabvány AGPL-3.0-szöveget.

**ParadeDB-saját nyilatkozat a témában — nem található.** Sem a „Why We Picked AGPL" blogbejegyzés (https://www.paradedb.com/blog/agpl), sem a hivatalos dokumentáció-index (`llms.txt`), sem az Enterprise-oldal nem tér ki kifejezetten arra, hogy egy különálló folyamatként futó, a `pg_search`-öt nem módosító, csak SQL-en/wire protocol-on kommunikáló alkalmazásra mi vonatkozik. Célzott Exa-keresések (pl. „ParadeDB does not require open source your application AGPL SQL wire protocol") sem hoztak fel ilyen hivatalos állásfoglalást.

Az egyetlen, témába vágó — de **nem hivatalos dokumentáció, csupán fórum-hozzászólás** — forrás egy 2024-es Hacker News-komment, amelyet a poszt szerzője a ParadeDB társalapítójaként azonosít:

> „We don't believe AGPL should prevent you from self-hosting for your own internal usage. […] We spent a lot of time evaluating which license to use, and decided to follow the footsteps of Citus Data and go with a standard OSS license while ensuring that we can't be hosted on public clouds without a partnership."

Forrás: https://news.ycombinator.com/item?id=38849928

Ez a komment a **saját-hosztolásról és a felhő-szolgáltatók kizárásáról** szól, nem kifejezetten a „csak SQL-en beszélő, változatlan kliens" esetről — így nem tekinthető az állításban feltett kérdésre adott közvetlen válasznak. A kérdés tehát nyitott marad: **nincs ParadeDB-saját, hivatalos nyilatkozat** erre a konkrét forgatókönyvre.

Kiegészítésül, a GNU hivatalos FAQ-ja (`curl`, https://www.gnu.org/licenses/gpl-faq.html, 2026-09-22) két, elméletileg releváns, de egymástól különálló pontot tartalmaz:

> „AGPLv3ServerAsUser: […] AGPLv3 requires a program to offer source code to 'all users interacting with it remotely through a computer network.' It doesn't matter if you call the program a 'client' or a 'server,' the question you need to ask is whether or not there is a reasonable expectation that a person will be interacting with the program remotely over a network."

> „MereAggregation: […] Where's the line between two separate programs, and one program with two parts? This is a legal question, which ultimately judges will decide. We believe that a proper criterion depends both on the mechanism of communication (exec, pipes, rpc, function calls within a shared address space, etc.) and the semantics of the communication…"

Ezek az FSF általános GPL-családi elvei, nem ParadeDB-specifikus és nem is kifejezetten az „adatbázis-kiterjesztés + tőle különálló, wire protocol-on kommunikáló kliens" esetre szabott állásfoglalások.

---

## Amit ez a döntésre jelent

- A licenc-alapállítás (AGPL-3.0, ma is érvényes, szó szerint megegyezik a hivatalos GNU-szöveggel) minden vizsgált forrásban konzisztens és megkérdőjelezhetetlen.
- A „legfrissebb stabil kiadás" pontos száma és dátuma forrásfüggő: a strukturált, géppel olvasható registry-k (Docker Hub API, PGXN) egyöntetűen v0.25.9-et (2026-09-11) mutatnak, míg a GitHub saját „latest release" felülete (a lekérés időpontjában) egy korábbi, v0.25.6 (2026-08-27) címkét adott vissza — ez vagy crawler-cache-probléma, vagy a GitHub „latest" jelölésének valamilyen sajátossága (pl. pre-release/draft-jelölés), de nem sikerült egyértelműen tisztázni.
- Az Enterprise-Community különbség a keresési funkciók szintjén valóban nulla (BM25, hibrid keresés, highlighting stb. mindkettőben ✅), a tényleges különbség pontosan a replikáció/HA/olvasó-replika kérdésére szűkül — ezt egy éles GitHub-hibaüzenet is alátámasztja szó szerint. Ugyanakkor az Enterprise emellett licenc-váltást (copyleft feloldása) és nem részletezett zárt forráskódú funkciókat is tartalmaz, amit egy tisztán funkcionális összehasonlítás elfed.
- A `pg_analytics` PostgreSQL License alatti működése és 2025-03-19-i archiválása egyértelműen, több, egymást megerősítő ponttal (repó-státusz, utolsó release időbélyege, changelog-bejegyzés) igazolt tény; az „AGPL a kezdetektől" állítás viszont kizárólag a cég saját, utólagos (2024-es) retrospektív nyilatkozatán nyugszik, független 2023-as forrás nélkül.
- A Neon-kivezetés pontos dátumai (2026-03-19 új projektekre, 2026-09-21 teljes megszűnés) két különböző Neon-dokumentációs oldalon és egy független, harmadik fél (felhasználói GitHub-vita) által is megerősítve — ez a legerősebben alátámasztott állítás a hét közül.
- A `pg_textsearch` valódi, aktívan fejlesztett, PostgreSQL License alatti BM25-alternatíva, amely kimutathatóan támogatja a magyar nyelvet (a Postgres 29 beépített `text search configuration`-je között), de PG 17–18-ra korlátozódik (pg_search PG 15–18-hoz képest szűkebb) és kevesebb mint egy éve létezik nyilvánosan.
- A ParadeDB semmilyen hivatalos csatornán nem foglal állást abban a konkrét kérdésben, hogy egy tőle különálló folyamatként futó, csak SQL/wire protocol-on kommunikáló, a `pg_search`-öt nem módosító alkalmazásra vonatkozik-e az AGPL 13. §-a — ez nyitott értelmezési kérdés marad, amit sem az FSF általános FAQ-ja, sem a ParadeDB dokumentációja nem old fel expliciten erre a konkrét architektúrára.

---



---

# ELL02 — Helyesség, tartósság, egyidejűség

> **Módszertani megjegyzés.** A kutatás kizárólag az Exa eszközökkel (`mcp__Exa__web_search_exa`, `mcp__Exa__web_fetch_exa`) történt, a `_ell_kozos.txt` előírása szerint; beépített `WebSearch`/`WebFetch` nem lett használva. Az Exa elérhető volt, nem kellett degradálni. A GitHub-issue/PR-oldalakat az Exa `web_fetch_exa` közvetlenül, elsődleges (T1) forrásként adta vissza (issue állapot, dátum, szerző, idézett szöveg, timeline). Ahol a hivatalos doksi-oldal közvetlen fetch-elése `CRAWL_NOT_FOUND` hibát adott (pl. `docs.paradedb.com/welcome/guarantees`, `.../verify-index`), ott a keresőindex (`web_search_exa`) adta vissza a lapról vett, gépi kivonatolt, de szó szerinti idézeteket — ezeket a tényleges URL-lel együtt idézem, jelezve a lekérés módját.

## Verdikt-összefoglaló

| # | Állítás | Verdikt | Egy mondat |
|---|---|---|---|
| 1 | #1929 (2024-11, jav. v0.12.1) és #6375/#6394/#6108 (2026-09-17 köteg) valódi „helytelen találat” hibák | **IGAZOLVA** | Mind a négy hiba valódi, elsődleges GitHub-forrásból igazolt; #1929 egy kiadott verziót (v0.12.0→javítva v0.12.1) érintett, #6375/#6394 kizárólag a `main` ágon léteztek és ott is javították őket (soha nem kerültek ki hibásan kiadott verzióba), #6108 viszont ténylegesen jelen volt egy kiadott verzióban (v0.25.9) és csak a `0.26` (RC) ágon lett javítva. |
| 2 | Community-tranzakciók csak v0.24.0-tól WAL-naplózottak; két korábbi forrás 2025-01-16-ot és 2025-06-03-at adott | **RÉSZBEN MEGDŐLT** | A blokktárolóra váltás (WAL-integráció alapjának lerakása) valóban 2025-01-16-i, de a Guarantees oldalon hivatkozott, ténylegesen kiadott v0.24.0 verzió — amely a Community-durability-t ténylegesen bevezette — nem 2025-06-03-án, hanem **2026-06-03-án** jelent meg; a „2025-06-03” dátum tehát év-tévesztés volt, két független forrással (GitHub release-oldal + a WAL-PR összevonási dátuma) megcáfolva. |
| 3 | Nyitott #6390: `pg_search` scanek nem vesznek SIREAD-zárat, SERIALIZABLE phantom write skew, miközben a Guarantees oldal „respect isolation levels”-t ígér | **IGAZOLVA** | Az issue valódi, jelenleg is **NYITOTT** (a javító PR #6392 is még nyitott, nem mergelt), és szó szerint idézi a Guarantees oldal ígéretét mint azt, aminek ellentmond; READ COMMITTED alatt a hiba strukturálisan nem releváns, mert a hivatalos PostgreSQL-dokumentáció szerint SIREAD-zárat kizárólag SERIALIZABLE tranzakciók használnak. |
| 4 | SIGSEGV #6374 egyidejű frissítéseknél | **IGAZOLVA** | Az issue valódi, `main` ágon (commit `85d6ca06b`), PG 15.15 debug build alatt reprodukált, 5/5 futtatásban lefagyott a szerver; **zárva** 2026-09-19-én, a hivatalos issue-szöveg szerint egy PR javította — kiadott (stabil) verziót nem érintett, mert a hiba a legutóbbi release (v0.25.9, 2026-09-11) után, csak a fejlesztői ágon jelentkezett. |
| 5 | `pg_dump` a BM25 indexet csak definícióként menti; `pdb.verify_index` létezik | **RÉSZBEN** | A `pdb.verify_index` létezése és funkciója **teljesen igazolt**, hivatalos dokumentációval és a bevezető PR-ral; a `pg_dump`-viselkedésre nézve viszont továbbra sincs kifejezett, hivatalos ParadeDB-nyilatkozat — csak egy harmadik fél (VPS-üzemeltetési útmutató) mondja ki explicit módon, hogy „BM25 indexes are NOT included in pg_dump; they're rebuilt on restore”. |
| 6 | Kell-e REINDEX `ALTER EXTENSION pg_search UPDATE` után vagy Postgres-főverzió-váltásnál | **RÉSZBEN MEGDŐLT** | Az „erre nincs forrás” korábbi következtetés részben megdőlt: a hivatalos changelogok **több konkrét verziónál is kimondottan előírják** a REINDEX-et (v0.15.0, v0.22.0, v0.25.1), tehát nem *minden* frissítés, hanem *egyes, változónként dokumentált* frissítések igénylik; Postgres-főverzió-váltásra (`pg_upgrade`) nézve továbbra sincs ParadeDB-specifikus hivatalos útmutató. |

---

## Állításonként

### 1. „Helytelen találati eredmény” hibák — #1929, #6375, #6394, #6108

**#1929 — valódi, v0.12.0-t érintette, javítva v0.12.1-ben (mindkettő kiadott verzió).**

Az issue elsődleges szövege (Exa `web_fetch_exa`, https://github.com/paradedb/paradedb/issues/1929):
> „When joining tables, querying using a search index and the '@@@' operator produces inconsistent results with 'max_parallel_workers' > 0” — State: closed, Created: 2024-11-12, ParadeDB Version: 0.12.0, PostgreSQL 16.4.

A hibás terv 329 sort adott vissza 3 loop alatt, a nem-párhuzamos terv 986-ot egy loopban — a query-analyze kimenet szó szerint tartalmazza mindkét tervet.

Második, független forrás — a v0.12.1 release oldal (https://github.com/paradedb/paradedb/releases/tag/v0.12.1, Published: 2024-11-12):
> „fix: index scans now work correctly under a parallel path (issue #1929) by @eeeebbbbrrrr in https://github.com/paradedb/paradedb/pull/1930”

**Tehát: valódi hiba, egy ténylegesen kiadott verziót (v0.12.0) érintett, és egy másik, ugyanaznap kiadott verzióban (v0.12.1) javították — mindkettő stabil release, nem csak `main`.**

**#6375 — valódi, kizárólag a `main` ágon létezett és ott is javult, kiadott verziót nem érintett.**

Elsődleges forrás (https://github.com/paradedb/paradedb/issues/6375, Author: mdashti, Created: 2026-09-17, State: closed):
> „PostgreSQL returns 9 rows, four for `users.id = 11` and five for `users.id = 5`. The join scan returns only the five rows of user 5... `main` at `85d6ca06b`, PG 15.15, debug build.”

A timeline szerint a hiba javítása: „Referenced by PR #6378: fix: follow HOT redirects in the join scan's final heap fetch” — ugyanaznap (2026-09-17) zárva.

**#6394 — valódi, szintén csak `main`-en, egy nappal később.**

(https://github.com/paradedb/paradedb/issues/6394, Created: 2026-09-17, closed: 2026-09-18):
> „When the join scan cannot fetch the heap tuple of a source on an outer join's nullable side, it drops the whole joined row. The correct result keeps the preserved side's row and fills the nullable side with NULLs.”

Javítás: „Referenced by PR #6395: fix: assert the join scan's heap fetch finds its tuple.”

**#6108 — valódi, és ez az egyetlen a négy közül, amely ténylegesen jelen volt egy *kiadott* verzióban.**

(https://github.com/paradedb/paradedb/issues/6108, Author: mithuncy, Created: 2026-08-26, labels: bug, priority-high):
> „The sequential-scan fallback returns no matches when a PostgreSQL `NUMERIC` column is the ParadeDB `key_field`... Both fixed-precision and arbitrary-precision `NUMERIC` key fields are affected.”

A maintainer (philippemnoel) zárókommentje (2026-09-19):
> „Verified locally using published Docker images on PostgreSQL 18.6, for both numeric(10,2) and numeric(30,2): paradedb/paradedb:0.25.9: indexed searches return the expected two rows, but forced sequential scans return zero rows, reproducing the reported bug. paradedb/paradedb:0.26.0-rc.1: both indexed searches and forced sequential scans return the expected rows... Closing as fixed in the 0.26 release line; the bug remains reproducible in 0.25.9.”

**Tehát #6108 ténylegesen benne volt a legutóbbi stabil kiadásban (v0.25.9, ld. lent), és a kutatás időpontjában (2026-09-22) a javítás még csak release-candidate (0.26.0-rc.1) állapotban érhető el, stabil 0.26.0 release nem található** (a https://github.com/paradedb/paradedb/releases/tag/v0.26.0 lekérése „CRAWL_NOT_FOUND” hibát adott).

**A kiadási státusz összegzése (a GitHub Releases-lista és egyedi tag-oldalak alapján, lekérve 2026-09-22):** a legutóbbi stabil release **v0.25.9** (Published: 2026-09-11), előtte v0.25.7 (2026-09-09). Mivel #6374/#6375/#6390/#6394 mindegyike 2026-09-17 után nyílt, egyik sem érinthetett kiadott verziót — mind kizárólag a `main` fejlesztői ágon léteztek.

---

### 2. Tartósság: v0.24.0, WAL-naplózás, és a két vitatott dátum

A hivatalos Guarantees oldal szövege (Exa `web_search_exa` kivonat, https://docs.paradedb.com/welcome/guarantees, ill. tükörként https://www.paradedb.com/docs/welcome/guarantees):
> „All reads and writes go through Postgres' transaction engine. This means that inserts, updates, and deletes to indexed columns are atomic, consistent, and respect Postgres' isolation levels.”
> „As of `0.24.0`, transactions are also durable, meaning they are write-ahead (WAL) logged and will survive crashes.”

**A blokktárolóra váltás dátuma (2025-01-16) — igazolt, valódi.**

A hivatalos blogbejegyzés fejléce (https://www.paradedb.com/blog/block-storage-part-one):
> „Published: 2025-01-16 · Author: Ming Ying”
> „block storage has enabled `pg_search` to simultaneously achieve: 1. Postgres write-ahead log (WAL) integration, which is necessary for physical replication of the index 2. Crash and point-in-time recovery...”

Ez az infrastrukturális alap (a blokktárolóra való átállás) tehát valóban 2025-01-16-án jelent meg — ez a dátum helyes.

**A v0.24.0 kiadás tényleges dátuma — MEGDŐL a „2025-06-03” állítás, a helyes év 2026.**

A GitHub release-tag oldal elsődleges adatai (https://github.com/paradedb/paradedb/releases/tag/v0.24.0):
> „Tag: v0.24.0 — Published: 2026-06-03T18:27:00Z — Author: github-actions[bot]”

Ugyanez, második, független forrásból (harmadik fél release-tükör, https://newreleases.io/project/github/paradedb/paradedb/release/v0.24.0):
> „Published: 2026-06-03T00:00:00.000Z” — „latest releases: v0.25.0, v0.24.3, v0.24.2...”

Harmadik megerősítés: a durability-t hozó PR saját adatai (https://github.com/paradedb/paradedb/pull/4901, „feat: Crash recovery via WAL”):
> „Created: 2026-04-27T21:35:16Z... Merged: 2026-05-14T21:59:54Z” — azaz a WAL-crash-recovery kód 2026-05-14-én olvadt be, majd a v0.24.0 release 2026-06-03-án jelent meg, ezzel konzisztensen.

A hivatalos changelog-kivonat (https://docs.paradedb.com/changelog/0.24.0.md, Exa-keresésből):
> „`pg_search` will now write WAL entries for its buffers, allowing for crash recovery.”

**Összegzés: a két korábbi forrás által adott dátumok (2025-01-16 és 2025-06-03) közül csak az első (a blokktárolóra váltás) helyes; a v0.24.0-s, ténylegesen a Community WAL-naplózást bevezető kiadás dátuma nem 2025-06-03, hanem 2026-06-03 — egy évnyi eltérés, amit három, egymástól független elsődleges forrás (GitHub release-oldal, harmadik fél release-tükör, a WAL-PR saját metaadatai) egybehangzóan cáfol.** Ez azt is jelenti, hogy a blokktárolóra váltás (2025-01-16, az infrastruktúra alapja) és a tényleges Community-durability bevezetése (v0.24.0, 2026-06-03) között **kb. 17 hónap** telt el — a két esemény nem azonos, és nem azonos évben történt.

---

### 3. SERIALIZABLE — nyitott #6390, phantom write skew

Elsődleges forrás (https://github.com/paradedb/paradedb/issues/6390, Author: mdashti, Created: 2026-09-17, **State: open** — a lekérés időpontjában, 2026-09-22, még mindig nyitott):
> „Under `SERIALIZABLE`, the base scan and the aggregate scan take no SIREAD locks. So when two transactions each count the matching rows and then each insert a new matching row, both commit. PostgreSQL's own plans for the same read abort one of them.”
> „`pg_search` has no `PredicateLock*` calls... The Guarantees page says writes respect Postgres' isolation levels.”

A reprodukció szó szerint bemutatja, hogy egy `Custom Scan`-t használó tervnél mindkét SERIALIZABLE tranzakció commit-ol (4 sor lesz `'oncall'` a várt 2 helyett), míg a natív `Index Scan` tervnél a második `COMMIT` hibával elutasításra kerül:
> „ERROR: could not serialize access due to read/write dependencies among transactions”

**A javító PR állapota — szintén nyitott, nem mergelt** (https://github.com/paradedb/paradedb/pull/6392, Created: 2026-09-17, **State: open**):
> „Closes #6390... Our scans call neither [`index_beginscan` nor `heap_beginscan`], so two transactions could each count the rows matching a search, then each insert a row the other would have counted, and both commit.”
> „`docs/concepts/guarantees` now says so.” — azaz a PR maga is elismeri, hogy a jelenlegi Guarantees-szöveg pontatlan, és a javítás része a dokumentáció frissítése is.

**Két, egymástól független T1-forrás** (maga az issue és a rá hivatkozó, azt megoldó PR szövege) erősíti meg egymást: a hiba valódi, jelenleg (2026-09-22) is fennáll, nyitott állapotban.

**READ COMMITTED hatása.** A hivatalos PostgreSQL-dokumentáció (https://www.postgresql.org/docs/current/transaction-iso.html):
> „Predicate locks in PostgreSQL... will show up in the `pg_locks` system view with a `mode` of `SIReadLock`.”

A PostgreSQL forráskód-szintű belső dokumentáció (`README-SSI`, https://github.com/postgres/postgres/blob/master/src/backend/storage/lmgr/README-SSI) még explicitebb:
> „The only transactions which create SIREAD locks or check for conflicts with them are serializable transactions.”

**Tehát a #6390 hiba strukturálisan kizárólag SERIALIZABLE izolációt érint; READ COMMITTED (a Postgres alapértelmezett szintje) alatt a SIREAD-mechanizmus egyáltalán nem aktiválódik, így ott ez a konkrét hiba nem releváns** — ez nem ParadeDB-specifikus tény, hanem a PostgreSQL SSI-implementációjának alapvető tervezési jellemzője, amit a hivatalos PostgreSQL-forrás mond ki.

---

### 4. SIGSEGV #6374 egyidejű frissítéseknél

Elsődleges forrás (https://github.com/paradedb/paradedb/issues/6374, Author: mdashti, Created: 2026-09-17, **State: closed**):
> „A `NOT IN` subquery that the planner runs as a parallel top-k scan crashes the backend with `SIGSEGV` when the scanned table has one row that was updated twice while `paradedb.global_mutable_segment_rows` was set. The postmaster then restarts, so every other connection to the server drops as well.”
> „The script below crashes 5 of 5 runs on `main` at `85d6ca06b`, PG 15.15, debug build.”

Szerver-log idézet:
> „LOG: server process (PID 40140) was terminated by signal 11: Segmentation fault: 11”

Három együttes feltétel: párhuzamos worker, heap-szűrő a scanben, és egy sor kétszeri UPDATE-je egy mutable szegmensbe (bármelyik hiányában a hiba nem jön elő).

**Javítás:** a maintainer záró kommentje (2026-09-19T00:57:56Z):
> „Fixed by https://github.com/paradedb/paradedb/pull/6348.”

A hivatkozott PR (https://github.com/paradedb/paradedb/pull/6348, „test: property-test partitioned joins”, State: merged, Merged: 2026-09-17T02:33:54Z) tartalma elsődlegesen tesztlefedettséget ad hozzá (property-test a particionált JOIN-okhoz); a leírása nem említi kifejezetten a #6374-et mint lezárt ticketet, de az issue hivatalos szövege ezt a PR-t nevezi meg javításként — ezt a kisebb következetlenséget (a hivatkozott PR száma alacsonyabb, mint magáé az issue-é, és a PR leírása nem hivatkozik vissza rá) jelzem, nem simítom el.

**Verzió-érintettség:** mivel a hiba 2026-09-17-én került elő és 2026-09-19-én zárult, a legutóbbi stabil kiadás (v0.25.9, 2026-09-11) **nem tartalmazhatta** — kizárólag a `main` fejlesztői ágat érintette.

---

### 5. Mentés: `pg_dump`/BM25 és a `pdb.verify_index` függvény

**`pdb.verify_index` — teljesen igazolt, létezik, és pontosan meghatározható, mit ellenőriz.**

Hivatalos dokumentáció (Exa-kivonat, https://docs.paradedb.com/documentation/indexing/verify-index, szerző: ParadeDB):
> „ParadeDB provides `amcheck`-style index verification functions to detect corruption and validate the structural integrity of BM25 indexes.”
> „The `pdb.verify_index` function performs structural integrity checks on a BM25 index... This returns a table with three columns: `check_name` (text), `passed` (boolean), `details` (text).”
> „To verify that all indexed entries still exist in the heap table, use the `heapallindexed` option... This adds an additional check that validates every indexed `ctid`... references a valid row in the table.”

Paraméterei a dokumentáció szerint: `index` (kötelező, regclass), `heapallindexed` (bool, alapért. false), `sample_rate` (float, részleges mintavételes ellenőrzéshez), `report_progress`, `verbose`, `on_error_stop` (a `pg_amcheck --on-error-stop`-hoz hasonlóan), `segment_ids` (kézi párhuzamosításhoz). Létezik emellett `pdb.verify_all_indexes` (adatbázis-szintű, minta/séma-szűrős) is.

Második, független T1-forrás — a funkciót bevezető PR (https://github.com/paradedb/paradedb/pull/3907, „feat: added amcheck-style index verification for BM25 indexes”):
> „Adds `pdb.verify_index()` and related functions to detect corruption and validate the structural integrity of BM25 indexes, similar to PostgreSQL's `amcheck` extension.”
> „New functions in the `pdb` schema: `pdb.verify_index(index)` — ...checks for schema validity, readability, segment checksums, metadata consistency, and optionally heap reference validation... `pdb.verify_all_indexes()`... `pdb.index_segments(index)`... `pdb.indexes()`.”

**Tehát a függvény létezése, paraméterezése és ellenőrzési köre (séma-érvényesség, olvashatóság, szegmens-checksumok, metaadat-konzisztencia, opcionális heap-referencia-ellenőrzés) két, egymástól független hivatalos forrással (doksi-oldal + a funkciót bevezető PR) igazolt.**

**`pg_dump` és a BM25 index — nincs kifejezett hivatalos ParadeDB-megerősítés, csak harmadik féltől.**

A hivatalos „Load Data from Postgres” oldal (https://docs.paradedb.com/documentation/getting-started/load) `pg_dump`/`pg_restore` parancsokat ad meg adatbetöltéshez, de **nem tartalmaz kifejezett állítást arra, hogy a BM25 index csak definícióként kerül a dumpba és visszaállításkor újraépül**.

Amit találtam, az egy harmadik fél (VPS-szolgáltató) hivatalos ParadeDB-hez köthető, de nem ParadeDB által írt üzemeltetési útmutatója (https://www.ramnode.com/guides/paradedb):
> „BM25 indexes are NOT included in `pg_dump`; they're rebuilt on restore. For large datasets use pgBackRest for physical backups (index files included, faster restore).”

Ez **explicit, konkrét állítás**, de **nem ParadeDB hivatalos forrása** — így a szigorú „ParadeDB-specifikus hivatalos megerősítés” kritériumnak nem felel meg, csak közvetett (harmadik féltől származó, T3) megerősítést ad. A mechanizmus maga (indexek `CREATE INDEX`-definícióként, „post-data” szakaszban dumpolva) a hivatalos PostgreSQL-dokumentációból (`pg_dump`) általánosan levezethető, de ParadeDB-specifikus, elsődleges forrású megerősítést erre a kutatás sem talált.

---

### 6. Frissítés: kell-e REINDEX `ALTER EXTENSION pg_search UPDATE` után vagy Postgres-főverzió-váltásnál

**Az „ALTER EXTENSION UPDATE után sosem esik szó REINDEX-ről” korábbi következtetés RÉSZBEN MEGDŐL: a changelogok konkrét verzióknál kifejezetten előírják.**

A hivatalos „Upgrading ParadeDB” oldal (https://docs.paradedb.com/deploy/upgrading) valóban nem tárgyalja a REINDEX kérdését általánosan, és az `ALTER EXTENSION pg_search UPDATE TO '<verzió>';` lépést mondja kötelezőnek:
> „This step is required regardless of the environment that ParadeDB is installed in (Helm, Docker, or self-managed Postgres).”

Ugyanakkor a **változat-specifikus changelogok** (Exa-keresés, `api.pgxn.org` tükrözött changelog-fájlokból, valamint a hivatalos `docs.paradedb.com/documentation/indexing/reindexing` oldal) **több konkrét esetben kimondottan előírják** a REINDEX-et:

- **0.15.0** (https://api.pgxn.org/src/pg_search/pg_search-0.25.9/docs/changelog/0.15.0.mdx):
  > „`0.15.0` contains breaking changes. After upgrading, all BM25 indexes must be recreated with `REINDEX`.”
  > „Modified the block storage layout for faster reads. This breaking change necessitates existing indexes to be recreated.”

- **0.22.0** (https://api.pgxn.org/src/pg_search/pg_search-0.25.9/docs/changelog/0.22.0.mdx):
  > „Support for pushdown of queries on NUMERIC columns to the index. NOTE: Pushdown for NUMERIC columns requires [a reindex](/documentation/indexing/reindexing).”

- **0.25.1** (https://api.pgxn.org/src/pg_search/pg_search-0.25.2/docs/changelog/0.25.1.mdx):
  > „**Breaking change:** `0.25.1` replaces the vector search engine's epsilon recall knob with a proof-based bounds gate... vector indexes built with `0.25.0` must be rebuilt with `REINDEX` after upgrading.”

- Kiegészítésképp a **0.25.0** changelog is jelzi a jövőbeli kockázatot (https://api.pgxn.org/src/pg_search/pg_search-0.25.2/docs/changelog/0.25.0.mdx):
  > „While vector search is marked as beta, future releases may change the vector storage format and require a reindex.”

**Tehát a REINDEX szükségessége nem univerzális szabály minden `ALTER EXTENSION ... UPDATE` után, hanem verzió-specifikus, breaking-change-jellegű kiadásoknál kifejezetten, a szó szerinti „reindex”/„recreate” kifejezéssel dokumentált** — ez cáfolja azt a korábbi következtetést, hogy a ParadeDB dokumentációja „teljesen hallgat” erről a kérdésről. A hivatalos „Upgrading” oldal maga nem tér ki rá, de a per-verzió changelogok igen, és ezekre a hivatalos „Upgrading” oldal is figyelmeztet áttételesen a release notes átolvasására.

**Postgres-főverzió-váltás (`pg_upgrade`) — továbbra sincs ParadeDB-specifikus hivatalos forrás.** A jelen kutatási kör sem talált a `pg_upgrade`/Postgres-főverzió-váltás és a `pg_search`/BM25-index viszonyáról szóló, ParadeDB által írt, kifejezett hivatalos útmutatót vagy figyelmeztetést — ezen a ponton a korábbi „NINCS FORRÁS” megállapítás **fennáll, megerősítve**.

---

## Amit ez a döntésre jelent

- Mind a négy „helytelen találat”-hiba (#1929, #6375, #6394, #6108) valódi, elsődleges GitHub-forrásból igazolt jelenség, nem félreértés vagy kitalált állítás — de eltérő súlyú: #1929 és #6108 ténylegesen kiadott (stabil) verziót érintett, #6375 és #6394 kizárólag a fejlesztői `main` ágon léteztek, oda is javították még aznap/másnap.
- A kutatás időpontjában (2026-09-22) a legutóbbi stabil kiadás **v0.25.9** (2026-09-11); a 2026-09-17 utáni négy hiba (#6374, #6375, #6390, #6394) egyike sem érinthetett kiadott verziót, mert mindegyik a v0.25.9 megjelenése után nyílt; egy `0.26.0` **stabil** release nem található, csak `0.26.0-rc.1`.
- A tartósság-dátum kérdésében egyik korábban idézett forrás sem volt pontos: a blokktárolóra váltás (a WAL-integráció infrastrukturális alapja) valóban 2025-01-16-i, de a ténylegesen Community-durability-t hozó v0.24.0 kiadás dátuma **2026-06-03**, nem 2025-06-03 — ez három egymástól független forrással megerősített, egy évnyi eltérés a korábbi kutatásban szereplő dátumhoz képest.
- A SERIALIZABLE/SIREAD-hiány probléma (#6390) valódi és **jelenleg is nyitott** (a javító PR #6392 is nyitott, nem mergelt) — azaz a hivatalos Guarantees oldal „respect Postgres' isolation levels” állítása és a tényleges, dokumentált viselkedés között a kutatás idején fennálló, el nem hárított ellentmondás van; ez a hiba READ COMMITTED alatt szerkezetileg nem releváns, mert a PostgreSQL SIREAD-zárolást kizárólag SERIALIZABLE tranzakciók használják.
- A `pdb.verify_index` (és a hozzá tartozó `pdb.verify_all_indexes`) funkció létezése, paraméterezése és pontos ellenőrzési köre két, egymástól független hivatalos forrással teljesen igazolt; a `pg_dump`+BM25-index kapcsolat viszont továbbra sincs kifejezett hivatalos ParadeDB-nyilatkozattal alátámasztva, csak egy harmadik féltől.
- A REINDEX-szükségesség `ALTER EXTENSION ... UPDATE` után nem hiánycikk a dokumentációban, ahogy egy korábbi kutatási kör állította: a hivatalos per-verzió changelogok (0.15.0, 0.22.0, 0.25.1) kifejezetten, a „reindex”/„recreate” szóval dokumentálják, mikor szükséges — de ez verzió-specifikus, nem univerzális szabály; a Postgres-főverzió-váltásra (`pg_upgrade`) vonatkozó ParadeDB-specifikus útmutató hiánya viszont megerősítést nyert.

---



---

# ELL03 — Szöveges és vektoros keresés, szűréssel (adverzariális ellenőrzés)

> **Módszertani megjegyzés.** Az `_ell_kozos.txt` előírása szerint kizárólag az **Exa**
> eszközökkel (`mcp__Exa__web_search_exa`, `mcp__Exa__web_fetch_exa`) végeztem webes keresést és
> oldalolvasást; ezek elérhetők voltak, nem kellett leállni. A `curl`-t kizárólag a szabály által
> engedélyezett esetben használtam: két **nyers fájl** (GitHub `raw.githubusercontent.com`
> forráskód-fájl) szó szerinti, sortartó ellenőrzésére (`grep`/`sed`), amikor az Exa
> `web_fetch_exa` válasza egy nagyon hosszú Rust forrásfájlnál a releváns sorok előtt megszakadt.
> Ez a kör egy korábbi (nem adverzariális) kutatási kör két dokumentumának (`sq03.md`, `sq04.md`)
> állításait ellenőrizte **megdöntési szándékkal**, önálló, friss keresésekkel — nem a korábbi
> dokumentumok idézeteit vettem át változtatás nélkül, hanem minden állítást újra, a hivatalos
> elsődleges forrásból (vagy egy attól eltérő elsődleges forrásból) kerestem elő. Al-ügynök
> indítására (a `deep-web-research` skill többügynökös fan-outjára) ebben a környezetben nem volt
> mód; egyetlen folyamatos szálon dolgoztam, ahogy a korábbi kör is.

## Verdikt-összefoglaló

| # | Állítás | Verdikt | Egy mondat |
|---|---|---|---|
| 1 | Egy tábla — egy ParadeDB-index; `USING paradedb` szintaxis, `USING bm25` visszafelé kompatibilis alias 0.25.0 óta | **IGAZOLVA** | A hivatalos dokumentáció két különböző oldala is szó szerint kimondja mindkét felet; a 0.25.0-s changelog szerint az alias **deprecated**, de máig működik. |
| 2 | Magyar `stemmer=hungarian` (Snowball) + kapcsolható `ascii_folding`; ő/ű → o/u; oszloponként eltérő tokenizáló egy indexen belül | **IGAZOLVA** | Mindkét szűrő és az oszloponkénti tokenizáló-választás a hivatalos pg_search-dokumentációból szó szerint igazolható; az ő/ű→o/u leképezést most **közvetlenül a pg_search saját, Cargo.toml-ban rögzített Tantivy-fork forráskódjában** (nem csak az upstream Tantivyben) ellenőriztem és megerősítettem. |
| 3 | 0.25.0 óta saját SPANN-stílusú vektorindex, "completely separate" a pgvector HNSW/IVF-jétől; pgvector csak típus miatt kell; recall-mérés szűréssel; pontos (index nélküli) keresés kérhető | **RÉSZBEN IGAZOLVA** | A "saját, elkülönült index" és "pgvector csak típusként kötelező" állítás szó szerint igazolt (2026-07-28-i, tehát kb. 8 hetes kiadás); **ÚJ TALÁLAT**: létezik szűrt recall-mérés a saját SPANN-indexre (ParadeDB saját CI-je, GitHub PR, nem hivatalos dokumentációban), ami pontosítja/részben megdönti a korábbi kör "nincs forrás" megállapítását; a pontos keresés csak tartalék-útvonalként ("brute force sort"), nem külön hirdetett módként érhető el. |
| 4 | pgvector HNSW/IVFFlat: `vector` ≤2000, `halfvec` ≤4000 dim indexelhető; van-e a ParadeDB saját vektorindexének dimenziókorlátja | **RÉSZBEN IGAZOLVA / NEM ELDÖNTHETŐ** | A pgvector-számok szó szerint igazoltak a hivatalos README-ből; a ParadeDB **jelenlegi** (0.25.x, SPANN-alapú) saját vektorindexére nem találtam explicit dimenziókorlátot — a korábbi, mára elavult, saját (nem pgvector-alapú) "vector" típusnak volt egy 2000-es korlátja, de ez már nem a jelenlegi architektúra része. |
| 5 | Filter Pushdown: `project_id IN (…)` az indexszkennelésbe kerül, ha indexelt, különben Postgres utólag szűr; hibrid (RRF, k=60) mintában mindkét ágba tehető ugyanaz a szűrő | **IGAZOLVA** | Mindkét részállítás szó szerint igazolt a hivatalos `reference/filtering/indexed` és `reference/hybrid/rrf` oldalakról, két, egymástól elkülönült dokumentumból. |
| 6 | Postgres beépített `tsvector`: van `hungarian` Snowball szótár (melyik verziótól); `ts_rank` doksi pontos szövege | **IGAZOLVA** | A `hungarian_stem` szótár a `\dFd` listában PostgreSQL **8.3** (2008, az első beépített FTS-verzió) óta kimutatható a mai (18-as) verzióig; a `ts_rank`/`ts_rank_cd` idézetek szó szerint egyeznek a jelenlegi hivatalos dokumentációval. |

---

## Állításonként

### 1. Egy tábla — egy ParadeDB-index; `USING paradedb`/`USING bm25`

Közvetlenül, frissen lekérve (2026-09-22):

> "Only one ParadeDB index can exist per table. We recommend indexing all columns in a table that
> may be present in a search query, including columns used for sorting, grouping, filtering, and
> aggregations."
> Forrás: [Create an Index](https://www.paradedb.com/docs/reference/indexing/create-index.md)

Második, elkülönült dokumentumoldal, más megfogalmazással, a tervezési indoklással:

> "The ParadeDB index is a covering index, which means it stores all indexed columns inside a
> single index per table. This decision is intentional -- by colocating all the relevant data,
> ParadeDB optimizes for fast reads and boolean conditions. However, this means that all columns
> must be defined up front at index creation time. Adding or removing columns requires a
> `REINDEX`."
> Forrás: [Limitations & Tradeoffs](https://www.paradedb.com/docs/welcome/limitations.md)

A szintaxis és az alias-viszony a `create-index.md` oldalról:

> "`USING bm25` remains supported as a backwards-compatible alias for `USING paradedb`."
> Forrás: uo.

**Pontosítás/árnyalat a korábbi körhöz képest** — a 0.25.0-s kiadási jegyzék élesebben fogalmaz,
mint a `create-index.md`: az alias hivatalosan **deprecated**, csak "tovább is működik":

> "`paradedb` is now the primary index access method name. […] This rename reflects the fact that
> the index drives much more than BM25 scoring — vector search, Top K, composable filtering,
> aggregates, etc. `USING bm25` has been deprecated but continues to work as a backwards-compatible
> alias."
> Forrás: [Changelog 0.25.0](https://www.paradedb.com/docs/project/changelog/0.25.0.md)

Ez nem dönti meg az eredeti állítást (a `USING bm25` valóban működik, visszafelé kompatibilis), de
pontosítja: a hivatalos ajánlás nem az alias, hanem a `USING paradedb` használata.

---

### 2. Magyar tövező, ASCII-folding, ő/ű, oszloponkénti tokenizáló

**Stemmer:**

> "Stemmers in ParadeDB are based on stemming algorithms obtained from the official Snowball
> website. […] Valid languages are `arabic`, `czech`, `danish`, `dutch`, `english`, `finnish`,
> `french`, `german`, `greek`, `hungarian`, `italian`, `norwegian`, `polish`, `portuguese`,
> `romanian`, `russian`, `spanish`, `swedish`, `tamil`, and `turkish`."
> Forrás: [Stemmer](https://www.paradedb.com/docs/reference/token-filters/stemming.md)

**ASCII folding:**

> "The ASCII folding filter strips away diacritical marks (accents, umlauts, tildes, etc.) while
> leaving the base character intact. It is supported for all tokenizers besides the literal
> tokenizer. To enable, append `ascii_folding=true` to the tokenizer's arguments."
> Forrás: [ASCII Folding](https://www.paradedb.com/docs/reference/token-filters/ascii-folding.md)

**Ő/ű → o/u leképezés — most közvetlenül pg_search SAJÁT függőségi forrásából, nem csak az
upstream Tantivyből.** A pg_search `Cargo.toml` (a `paradedb/paradedb` repó gyökér-workspace-e)
nem az upstream `quickwit-oss/tantivy`-t, hanem a ParadeDB **saját fork-ját** rögzíti:

> `tantivy = { git = "https://github.com/paradedb/tantivy.git", package = "tantivy", rev =
> "dcbfce29c74b5d6c6653f3e36471aa2f37a9a79b", features = [...], default-features = false }`
> Forrás: [github.com/paradedb/paradedb — `Cargo.toml`](https://github.com/paradedb/paradedb/blob/main/Cargo.toml)

Ezt a pontos, rögzített revíziót (`dcbfce2…`) lekérve, a fork saját
`src/tokenizer/ascii_folding_filter.rs` fájljában — `curl`-lal, nyers fájlként, sortartóan
ellenőrizve — szó szerint megtalálható mind a nagy-, mind a kisbetűs magyar ő/ű leképezés, a
`match`-ágban **és** a fájl saját unit tesztjeiben is:

> ```
> '\u{0150}' | // Ő  [LATIN CAPITAL LETTER O WITH DOUBLE ACUTE]
> ...
> => Some("O"),
> '\u{0151}' | // ő  [LATIN SMALL LETTER O WITH DOUBLE ACUTE]
> ...
> => Some("o"),
> '\u{0170}' | // Ű  [LATIN CAPITAL LETTER U WITH DOUBLE ACUTE]
> ...
> => Some("U"),
> '\u{0171}' | // ű  [LATIN SMALL LETTER U WITH DOUBLE ACUTE]
> ...
> => Some("u"),
> ```
> Forrás: [raw.githubusercontent.com/paradedb/tantivy@dcbfce2…/src/tokenizer/ascii_folding_filter.rs](https://raw.githubusercontent.com/paradedb/tantivy/dcbfce29c74b5d6c6653f3e36471aa2f37a9a79b/src/tokenizer/ascii_folding_filter.rs)
> (T1, `curl` nyers fájl, közvetlenül a pg_search által Cargo.toml-ban rögzített revízióról,
> 2026-09-22-i lekérés)

Ugyanez a leképezés szerepel a fájl unit tesztjeiben is ("Ő", "ő", "Ű", "ű" a bemeneti tesztlisták
tagjai), tehát nemcsak deklarált, hanem tesztelt viselkedés. Ez erősebb bizonyíték, mint a korábbi
kör "csak az upstream Tantivy docs.rs-en" alapuló közvetett igazolása: ez a fájl a pg_search
**saját, ténylegesen felhasznált** függőségi forrása.

**Oszloponként eltérő tokenizáló egy indexen belül — igen**, közvetlenül igazolva:

> ```sql
> CREATE INDEX search_idx ON mock_items
> USING paradedb (id, (description::pdb.icu), category)
> WITH (key_field='id');
> ```
> "By default, text columns are tokenized using the unicode tokenizer... For instance, if a column
> contains multiple languages, the ICU tokenizer may be more appropriate."
> Forrás: [Create an Index](https://www.paradedb.com/docs/reference/indexing/create-index.md)

A mechanizmus (oszloponkénti cast `pdb.<tokenizer>`-re) közvetlenül megengedi, hogy egy törzsmező
`pdb.simple('stemmer=hungarian')`, egy azonosító-mező pedig `pdb.literal` legyen ugyanabban a
`CREATE INDEX` utasításban — konkrét, kész "hungarian stemmer + literal id" munkapéldát a
dokumentáció nem ad, de a szintaktikai mechanizmus (mezőnkénti cast) egyértelműen ezt teszi
lehetővé, és ezt a `key_field` szabály is alátámasztja ("Be untokenized, if it is a text field" —
tehát az azonosító mezőnek éppen `literal`-nak kell lennie).

---

### 3. Vektor: saját SPANN-index, "completely separate", pgvector csak típusként, recall szűréssel, pontos keresés

**"Completely separate from pgvector's HNSW/IVF indexes" — szó szerint igazolva:**

> "**Native Vector Search (Beta)**: The ParadeDB index can now index the `vector` type. This index
> is completely separate from `pgvector`'s HNSW/IVF indexes: Vectors are backed by a SPANN-style
> index, the state-of-the-art in vector search designed for datasets that are far larger than
> available memory."
> Forrás: [Changelog 0.25.0](https://www.paradedb.com/docs/project/changelog/0.25.0.md)

**pgvector csak a típus/operátorok miatt kötelező, nem az indexért:**

> "Make sure the pgvector extension is installed first. ParadeDB uses pgvector's vector types, but
> not its HNSW or IVF indexes."
> Forrás: [Indexing Vectors](https://www.paradedb.com/docs/reference/indexing/indexing-vectors.md)

> "Breaking change: As of `0.25.0`, `pgvector` is a required extension of `pg_search`. […] The
> reason is because `0.25.0` brings native vector search support to the ParadeDB index and relies
> on `pgvector`'s `vector` type and distance operators."
> Forrás: [Changelog 0.25.0](https://www.paradedb.com/docs/project/changelog/0.25.0.md)

**Mennyire új — pontosított dátum.** A `v0.25.0` GitHub-release ténylegesen:

> Tag: `v0.25.0` — Published: **2026-07-28T21:46:40Z**
> Forrás: [github.com/paradedb/paradedb/releases/tag/v0.25.0](https://github.com/paradedb/paradedb/releases/tag/v0.25.0)

Ez a mai naphoz (2026-09-22) képest kb. **8 hetes** funkció — pontosabb, mint a korábbi kör "2026
nyara" megfogalmazása.

**ÚJ TALÁLAT — recall-mérés szűréssel a ParadeDB saját SPANN-indexére.** A korábbi kör azt
állította, nincs erre forrás. Ezzel szemben találtam ParadeDB **saját CI-jéből** (nem hivatalos
`/docs/` oldal, hanem egy GitHub Pull Request automatikus botkommentje) konkrét, számszerű
recall@10 adatokat a `pg_search` SPANN-indexére, Cohere-embeddingeken (1M és 10M soros korpusz),
szűrt (1%, 10% szelektivitás) és szűretlen lekérdezésekre:

> "### Cohere recall — `pg_search` index
> | query | 1m | 10m |
> |-------|----|----|
> | `knn_top10_10pct` | 0.9510 | 0.9390 |
> | `knn_top10_1pct` | 0.9590 | 0.9420 |
> | `knn_top10_unfiltered` | 0.9680 | 0.9540 |
> recall@10 of the ANN index vs exact nearest neighbors over a held-out query set, at the same
> probes/ef_search as the latency benchmark. Probes are tuned per query+size for ~95% recall"
> Forrás: [github.com/paradedb/paradedb/pull/5613](https://github.com/paradedb/paradedb/pull/5613)
> — `github-actions[bot]` kommentje, 2026-07-22 (T1, ParadeDB saját CI-adata; a PR maga
> 2026-07-27-én lett mergelve)

Ugyanezen PR-en belül, más futásokban a számok kissé ingadoztak (pl. egy másik futásban 1%-nál
0.9420/0.9350, egy harmadikban 0.9420/0.9350 vs. szűretlen 0.9260/0.8750) — ez arra utal, hogy a
mérés maga is még instabil/finomítás alatt álló CI-folyamat, nem egy lezárt, hivatalosan közölt
benchmark. **Fontos módszertani pontosítás a korábbi körhöz képest:** ez **nem hivatalos,
dokumentált** ("published" a `/docs/` értelemben) recall-szám, hanem nyilvánosan látható, de
gyártói (first-party) CI-artefaktum egy GitHub PR-en. Független (nem ParadeDB által mért)
recall-adatot a ParadeDB saját SPANN-indexére továbbra sem találtam — ezt megerősíti, hogy célzott
kereséssel sem került elő harmadik féltől származó mérés.

Fontos, hogy a szűrt (1%) recall itt **nem esik látványosan** a szűretlenhez képest (pl. 0.959 vs.
0.968 az első táblázatban) — ez élesen eltér a pgvector natív post-filtering viselkedésétől (ahol
1%-os szelektivitásnál a natív HNSW recall drasztikusan, akár 1%-ra is leeshet iteratív scan
nélkül — lásd a korábbi kör AWS-forrását), és összhangban van azzal a dokumentált tervezési céllal,
hogy a ParadeDB a szűrőket **magába az index-scan-be** tolja be, nem utólagos post-filterként
alkalmazza.

**Pontos (index nélküli) vektorkeresés — igen, de tartalék-útvonalként, nem külön hirdetett
módként:**

> "This operator must match the distance metric used by the index. Otherwise, ParadeDB cannot use
> the index to order results and falls back to a slower brute force sort."
> Forrás: [Querying Vectors](https://www.paradedb.com/docs/reference/vector/querying.md)

Ez azt igazolja, hogy egy nem-indexelt vagy operátor-eltérő `ORDER BY embedding <-> ...` lekérdezés
esetén ParadeDB ténylegesen egy brute-force (tehát pontos, index nélküli) rendezésre esik vissza —
ugyanaz a funkcionális garancia, mint a pgvector "exact search"-je, csak a ParadeDB dokumentációja
ezt fallback-ként, nem önálló, deliberáltan kérhető "exact search" módként nevezi meg (szemben a
pgvector saját READMÉ-jével, amely direkt kimondja: "By default, pgvector performs exact nearest
neighbor search, which provides perfect recall." — Forrás:
[github.com/pgvector/pgvector/blob/master/README.md](https://raw.githubusercontent.com/pgvector/pgvector/master/README.md)).

---

### 4. Dimenziókorlátok

**pgvector — szó szerint igazolva, közvetlenül a hivatalos READMÉ-ből:**

> "Supported types are: — `vector` - up to **2,000 dimensions** — `halfvec` - up to **4,000
> dimensions** — `bit` - up to 64,000 dimensions — `sparsevec` - up to 1,000 non-zero elements"
> Forrás: [github.com/pgvector/pgvector/blob/master/README.md](https://raw.githubusercontent.com/pgvector/pgvector/master/README.md)

(Ez az indexelhetőségi korlát; a puszta *tárolási* korlát mindkét típusnál 16 000 dimenzió, index
nélkül.)

**ParadeDB saját (SPANN) vektorindexének dimenziókorlátja — NEM ELDÖNTHETŐ a jelenlegi
dokumentációból.** A jelenlegi (0.25.x, SPANN-alapú) `Indexing Vectors` oldal csak ennyit mond:

> "Only pgvector's `vector` type is supported. The `halfvec`, `sparsevec`, and `bit` types are not
> yet indexable."
> Forrás: [Indexing Vectors](https://www.paradedb.com/docs/reference/indexing/indexing-vectors.md)

— vagyis nem ad külön, a SPANN-indexre vonatkozó dimenziószámot. Célzott kereséssel találtam egy
**elavult, mára irreleváns** adatpontot: a pg_search **0.17.3**-as (SPANN előtti, saját,
nem-pgvector-alapú `vector` típusú) dokumentációja explicit 2000-es korlátot adott meg:

> "The `vector` data type is used to store vectors in ParadeDB. `vector` has a maximum dimension
> (i.e. length) of `2,000` entries."
> Forrás: [pg_search 0.17.3 `similarity/overview.mdx` @ PGXN](https://api.pgxn.org/src/pg_search/pg_search-0.17.3/docs/documentation/similarity/overview.mdx)

Ez azonban a 0.25.0 előtti, saját (nem pgvector-típusú) `vector` mezőre vonatkozott, amelyet a
0.25.0-s architektúraváltás óta a pgvector típusa váltott fel — tehát ez a szám **nem** vihető át
egyértelműen a jelenlegi SPANN-indexre. Sem a hivatalos `/docs/` oldalakon, sem a
`github.com/paradedb/paradedb` releváns dokumentum-fájljaiban nem találtam a jelenlegi SPANN-index
saját, explicit dimenziókorlátját megadó mondatot — ez nyitott kérdés marad.

---

### 5. Filter Pushdown és RRF hibrid keresés szűréssel

**`project_id IN (…)` pushdown-képessége — szó szerint igazolva, típus/operátor-táblázattal:**

> "## Filter Pushdown ### Non-Text Columns […] When these columns are part of the index, `WHERE`
> clauses that reference them can be pushed down into the index scan itself."
>
> Táblázat-sor: `IN, ANY, ALL` | `uuid` | `uuid[]` — és ugyanígy `int2`/`int4`/`int8` saját és
> egymás tömbváltozataira.
> Forrás: [Indexed Columns (Filter Pushdown)](https://www.paradedb.com/docs/reference/filtering/indexed.md)

**Nem-indexelt oszlopon utólagos Postgres-szűrés — szó szerint igazolva:**

> "Every column you filter on (e.g. `category` above) must also be part of the ParadeDB index.
> Filters on unindexed columns cannot be evaluated by the ParadeDB index, forcing Postgres to
> recheck them afterward and eliminating the benefit of combining vector search with filtering."
> Forrás: [Querying Vectors](https://www.paradedb.com/docs/reference/vector/querying.md)

**RRF, k=60, mindkét ágba tehető ugyanaz a szűrő — szó szerint igazolva, a teljes SQL-mintával
együtt:**

> "`k` is the rank constant. […] `60` is the conventional value and the one used throughout this
> page."
>
> ```sql
> WITH text AS (
>     SELECT id, RANK() OVER (ORDER BY pdb.score(id) DESC, id) AS rank
>     FROM mock_items
>     WHERE description ||| 'running shoes'
>     ORDER BY pdb.score(id) DESC, id
>     LIMIT 20
> ),
> vector AS (
>     SELECT id, RANK() OVER (ORDER BY embedding <=> '[1,2,3,4,5,6,7,8]', id) AS rank
>     FROM mock_items
>     WHERE id @@@ pdb.all()
>     ORDER BY embedding <=> '[1,2,3,4,5,6,7,8]', id
>     LIMIT 20
> ),
> fused AS (
>     SELECT id, sum(weight) AS score
>     FROM (
>         SELECT id, 1.0 / (60 + rank) AS weight FROM text
>         UNION ALL
>         SELECT id, 0.7 / (60 + rank) AS weight FROM vector
>     ) u
>     GROUP BY id
> )
> SELECT m.id, m.description, f.score
> FROM fused f
> JOIN mock_items m USING (id)
> ORDER BY f.score DESC, m.id
> LIMIT 5;
> ```
>
> "The two `WHERE` clauses differ because each branch retrieves by its own method. […] **To narrow
> either branch, add filters to both, so that each is drawing from the same set of eligible
> rows.**"
> Forrás: [Reciprocal Rank Fusion](https://www.paradedb.com/docs/reference/hybrid/rrf.md)

Tehát igen: a hivatalos minta explicit ajánlása szerint ugyanaz a (pl. jogosultsági) szűrő mindkét
CTE `WHERE`-jébe betehető — a `text` ág `|||`/`&&&`/`===` operátorába, a `vector` ág `pdb.all()`-ja
helyére.

---

### 6. Postgres beépített `tsvector`: magyar Snowball szótár és `ts_rank`

**Van-e `hungarian_stem`, és melyik verziótól — igen, PostgreSQL 8.3 óta (az első beépített
full-text-search verzió, 2008).** Első, elsődleges forrás — a **legkorábbi**, még élő hivatalos
verziódokumentáció (8.3), amely már tartalmazza:

> ```
> => \dFd
>                             List of text search dictionaries
>    Schema   |      Name       |                        Description
> ------------+-----------------+-----------------------------------------------------------
>  pg_catalog | danish_stem     | snowball stemmer for danish language
>  ...
>  pg_catalog | hungarian_stem  | snowball stemmer for hungarian language
>  ...
> ```
> Forrás: [PostgreSQL 8.3 — psql Support](https://www.postgresql.org/docs/8.3/textsearch-psql.html)

Ugyanez a sor a **jelenlegi** (18-as) dokumentációban is megvan — második, független (más
verziójú) forrás:

> "`pg_catalog | hungarian_stem  | snowball stemmer for hungarian language`"
> Forrás: [PostgreSQL 18 — psql Support](https://www.postgresql.org/docs/18/textsearch-psql.html)

Harmadik, forráskód-szintű megerősítés (más jellegű forrás, közvetlenül a `postgres/postgres`
GitHub-tükörről):

> ```
> #include "snowball/libstemmer/stem_UTF_8_hungarian.h"
> ...
> STEMMER_MODULE(hungarian, PG_LATIN2, ISO_8859_2),
> ...
> STEMMER_MODULE(hungarian, PG_UTF8, UTF_8),
> ```
> Forrás: [github.com/postgres/postgres/blob/master/src/backend/snowball/dict_snowball.c](https://github.com/postgres/postgres/blob/master/src/backend/snowball/dict_snowball.c)

Az egyetlen árnyalat: a `12.6. Dictionaries` fő tartalmi fejezet szövege maga **nem** sorolja fel
név szerint a nyelveket (csak angol példát ad, "predefined dictionaries for many languages"
általánossággal) — a nyelvlistát a `\dFd` psql-parancs kimenete és a forráskód adja meg
explicit módon, nem a leíró próza.

**`ts_rank` — a doksi pontos szövege, szó szerint egyezik a korábbi kör idézetével:**

> "Ranking attempts to measure how relevant documents are to a particular query, so that when
> there are many matches the most relevant ones can be shown first. […] However, the concept of
> relevancy is vague and very application-specific. […] **The built-in ranking functions are only
> examples.** You can write your own ranking functions and/or combine their results with
> additional factors to fit your specific needs."
>
> "It is important to note that **the ranking functions do not use any global information**, so it
> is impossible to produce a fair normalization to 1% or 100% as sometimes desired."
> Forrás: [PostgreSQL — 12.3.3. Ranking Search Results](https://www.postgresql.org/docs/current/textsearch-controls.html)

A "BM25" kifejezés ezen az oldalon (frissen ellenőrizve) továbbra sem fordul elő — ez megerősíti a
korábbi kör azon pontosítását, hogy a Postgres dokumentációja nem "nem BM25" megfogalmazással
állítja szembe magát a BM25-tel, hanem a globális (korpuszszintű) információ hiányát mondja ki
funkcionális jellemzőként.

---

## Amit ez a döntésre jelent

1. Mind a hat állítás fő magja **igazolt** vagy **részben igazolt** volt; **egyik állítás sem dőlt
   meg teljesen** — az adverzariális ellenőrzés inkább pontosításokat és egy tényleges
   kiegészítést hozott, nem cáfolatot.
2. A magyar ő/ű ASCII-folding-leképezés bizonyítéka **megerősödött**: a korábbi kör csak az
   upstream (`quickwit-oss/tantivy`) forrást tudta ellenőrizni; most közvetlenül a pg_search
   `Cargo.toml`-jában rögzített **saját ParadeDB-tantivy-fork** pontos revíziójából, `curl`-lal
   olvasott nyers forrásfájlból igazolható a leképezés (mind a nagy-, mind a kisbetűs alakra, a
   kódban és a unit tesztekben is).
3. **Új, korábban nem talált adat**: létezik ParadeDB-saját (first-party CI, nem hivatalos
   `/docs/` oldal) szűrt recall-mérés a saját SPANN-vektorindexére (recall@10, Cohere-korpusz,
   1%/10%/szűretlen szelektivitás, 1M/10M sor) — ez pontosítja a korábbi kör "nincs forrás"
   megállapítását, de nem minősül hivatalosan publikált vagy független benchmarknak, és a
   futásonkénti ingadozás (kb. 0.87–0.98 között) arra utal, hogy a mérés maga is még
   finomítás/stabilizálás alatt áll.
4. A ParadeDB saját SPANN-vektorindexének **dimenziókorlátja továbbra sem állapítható meg**
   egyértelműen a jelenlegi hivatalos dokumentációból; az egyetlen fellelt konkrét szám (2000
   dimenzió) egy **elavult**, 0.25.0 előtti, nem pgvector-alapú saját típusra vonatkozott, ezért
   nem vihető át kritika nélkül a jelenlegi architektúrára.
5. A `USING bm25` alias ténylegesen működik, de a 0.25.0-s changelog explicit **deprecated**
   státuszt ad neki — ez egy apró, de dokumentált pontosítás a korábbi kör megfogalmazásához
   képest, amely ezt nem emelte ki.
6. A magyar Snowball-tövező jelenléte a Postgres core-ban most **konkrét verzióhoz köthető**: a
   `\dFd` lista PostgreSQL 8.3-tól (2008, az első beépített FTS-kiadástól) kezdve tartalmazza a
   `hungarian_stem`-et, egészen a jelenlegi (18-as) verzióig — ez pontosítja a korábbi kör
   "melyik verziótól" nyitott kérdését.

---



---

# ELL04 — TypeScript / Bun / Drizzle / Better Auth ellenőrzés

> **Módszertani megjegyzés.** A keresést kizárólag az Exa eszközökkel (`mcp__Exa__web_search_exa`, `mcp__Exa__web_fetch_exa`) végeztem, a `_ell_kozos.txt` előírása szerint. `curl`-t kizárólag nyers fájlok (npm registry JSON, GitHub raw `package.json`/`CHANGELOG.md`) szó szerinti, gépi lekérdezésére használtam. A `anthropic-skills:deep-web-research` skill alügynök-indítási képessége ebben a környezetben sem érhető el (nincs `Agent`/`Task` eszköz), ezért — a `sq06.md`-hez hasonlóan — degradált módban, egyetlen szálon dolgoztam; nem készült `.research/` evidence-vault, nem futott Opus-szintézis/Sonnet-verifikáció. Minden verdikthez törekedtem két, egymástól független elsődleges forrásra (npm registry + GitHub, vagy két különböző hivatalos doksi-oldal); ahol ez nem sikerült, azt külön jelzem.

---

## Verdikt-összefoglaló

| # | Állítás | Verdikt | Egy mondat |
|---|---|---|---|
| 1 | Létezik hivatalos `@paradedb/drizzle-paradedb` (MIT), peer: `drizzle-orm@1.0.0-rc.4`; legfrissebb verzió/dátum | **IGAZOLVA** | Az npm registry és a GitHub `CHANGELOG.md` egybehangzóan: legfrissebb **0.5.0**, publikálva **2026-08-21**, MIT licenc, peer `drizzle-orm: "1.0.0-rc.4"`. |
| 2a | A Drizzle stabil „latest" 2026-09 közepén **0.45.3** (kit **0.31.11**), az 1.0 még RC | **IGAZOLVA** | Az npm registry `dist-tags` szerint `latest`=0.45.3 / 0.31.11 (publikálva 2026-09-21), `rc`=1.0.0-rc.4, `rc5`=1.0.0-rc.5 (2026-09-09) — a friss RC-ág is még RC, nem stabil. |
| 2b | Mikorra ígérik a Drizzle 1.0-t (hivatalos forrás) | **NEM ELDÖNTHETŐ** | Nincs friss, konkrét hivatalos dátum; a Drizzle-alapító egy 2025 végi becslése („v1 beta ősszel, a stabil ugyanolyan idősávban") azóta bő egy éve nem teljesült, a hivatalos Roadmap-oldal és a nyitott „when will we have v1.0.0?" issue sem ad dátumot. |
| 2c | Van-e mód a ParadeDB-t a stabil Drizzle-lel, hivatalos csomag nélkül használni (`index().using('paradedb', …)` + nyers `sql`) | **IGAZOLVA** | A `PgIndexMethod` típus és a `.using()` metódus, amely tetszőleges stringet elfogad, már egy 2024/2025-ös (stabil ág előtti) commitban is jelen volt változatlan formában, és a nyers `sql` sablon-literál a Drizzle mag része — technikailag megvalósítható a hivatalos RC-csomag nélkül is, bár típusbiztonság és a csomag saját teszt-lefedettsége nélkül. |
| 3 | Drizzle natívan támogatja a `vector` oszlopot, távolságfüggvényeket, HNSW-indexet — stabil verzióban is, nem csak RC-ben | **IGAZOLVA** | A hivatalos „Vector similarity search" útmutató explicit minimumverziót ad: „You should have `drizzle-orm@0.31.0` and `drizzle-kit@0.22.0` or higher" — ez a jelenlegi 0.45.3/0.31.11 stabil ág messze fölötti régi minimum, tehát a funkció a stabil ágban is megvan, nem RC-exkluzív. |
| 4a | Better Auth Drizzle-adapter: Drizzle 1.0 RC-vel csak Better Auth 1.7 RC kompatibilis (PR #9489) | **RÉSZBEN (elavult állítás)** | A PR #9489 valóban a Better Auth 1.7-es vonalán (először `1.7.0-beta.10`-ben) vezette be a Drizzle v1-kompatibilis `relations-v2` adaptert — de mára (2026-09-22) a Better Auth 1.7 **stabil** kiadás (npm „latest" = 1.7.5, 2026-09-14), tehát az állítás „csak RC" korlátozása ma már nem igaz. |
| 4b | Stabil Better Auth + stabil Drizzle (0.45) + Postgres működik-e | **IGAZOLVA** | A Better Auth 1.7.5 npm `package.json` `peerDependencies` mezője explicit: `"drizzle-orm": "^0.45.2 \|\| >=1.0.0-rc.1 <2.0.0"` — azaz a stabil 0.45.x ág hivatalosan, változatlanul támogatott (ez volt az egyetlen támogatott sáv is a korábbi 1.6.x vonalon). |
| 5a | `Bun.sql` Postgres-kliens érett-e, hivatalos státusz | **RÉSZBEN** | Hivatalosan promózott, benchmarkolt, „production" címkével kommunikált funkció, de a saját GitHub tracking issue-ja (#15088) még **nyitva** van, és 2026 június–július folyamán (a kutatás időpontjához képest 2-3 hónapja) is kerültek elő és javultak konkurenciafüggő adatvesztési/leállási hibák (pl. #32004, a hozzá tartozó #32772 javítás, #33665). |
| 5b | Mely Drizzle Postgres-driverek támogatottak Bun alatt stabilan (postgres.js, node-postgres, bun-sql) | **RÉSZBEN** | A hivatalos Bun-doksi FAQ-ja mindhármat jóváhagyja („You can use npm packages like postgres.js … pg, and node-postgres in Bun … They're great options"), és a Drizzle mindhármat dokumentálja — de explicit, egy mondatos „ez a hivatalosan ajánlott" rangsorolást egyik forrás sem ad, és a `postgres.js`/Bun kombinációnak korábban (2024 végén) volt már lezárt regressziós hibája. |
| 6 | macOS-en a `bun:sqlite` a rendszer SQLite-ját használja, bővítmény nem tölthető be; igaz-e ma (Bun 1.4), és van-e dokumentált kerülőút (`Database.setCustomSQLite`) | **IGAZOLVA** | A hivatalos, ma lekért Bun-dokumentáció szó szerint ezt írja, és két 2026 augusztusi GitHub-issue (#38647, #38772) kifejezetten Bun **1.3.14 / 1.4.0-canary** alatt reprodukálja a hibát; a `Database.setCustomSQLite(path)` a hivatalosan dokumentált és több független (Bun-doksi, `sqlite-vec` repó) forrásban is megerősített kerülőút. |

---

## Állításonként

### 1. `@paradedb/drizzle-paradedb` — hivatalos csomag, MIT, peer `drizzle-orm@1.0.0-rc.4`, legfrissebb verzió

Az npm registry API közvetlen lekérdezése (`registry.npmjs.org/@paradedb/drizzle-paradedb`):

> `"dist-tags":{"latest":"0.5.0"}` … a `0.5.0` verzió `"modified"` időbélyege: `2026-08-21T14:10:27.851Z`.
(https://registry.npmjs.org/@paradedb/drizzle-paradedb)

A publikált `0.5.0` verzió saját metaadata (`registry.npmjs.org/@paradedb/drizzle-paradedb/0.5.0`):

> `"license":"MIT"`, `"peerDependencies":{"drizzle-orm":"1.0.0-rc.4"}`
(https://registry.npmjs.org/@paradedb/drizzle-paradedb/0.5.0)

Ezt független forrásként megerősíti a repó saját `CHANGELOG.md`-je (nyersen lekérve):

> „## [0.5.0] - 2026-08-21 ### Changed - Upgraded to Drizzle 1.0.0-rc.4."
(https://raw.githubusercontent.com/paradedb/drizzle-paradedb/main/CHANGELOG.md)

**Verdikt: IGAZOLVA.** Két, technikailag különböző lekérési útvonalon (npm registry JSON API, illetve a repó saját, verziózott changelog fájlja) egybehangzó adat: a csomag hivatalos, MIT licencű, legfrissebb verziója **0.5.0** (**2026-08-21**), amely a Drizzle **1.0.0-rc.4**-et írja elő peer-dependencyként. (A `sq06.md` korábbi kutatása ugyanezt találta a fő ágon; itt függetlenül, a publikált npm-verzión is megerősítettem.)

---

### 2a. Drizzle stabil „latest" 2026-09 közepén 0.45.3 (kit 0.31.11), az 1.0 még RC

Az npm registry API friss (a mai napon végzett) lekérdezése:

> `drizzle-orm` dist-tags: `"latest":"0.45.3"`, időbélyeg `2026-09-21T10:06:39.969Z`; `"rc":"1.0.0-rc.4"`; `"rc5":"1.0.0-rc.5-5935859"` (2026-09-09).
> `drizzle-kit` dist-tags: `"latest":"0.31.11"`, időbélyeg `2026-09-21T10:06:58.727Z`; `"rc":"1.0.0-rc.4"`.
(https://registry.npmjs.org/drizzle-orm, https://registry.npmjs.org/drizzle-kit)

**Verdikt: IGAZOLVA.** Az állítás pontos: a „latest" npm-tag 2026-09-21-i publikálással is a 0.45.3/0.31.11 stabil sorozatra mutat, míg az 1.0-s ág — még a legújabb `rc5` build is — release candidate státuszú.

### 2b. Mikorra ígérik a Drizzle 1.0-t (hivatalos forrás)

A hivatalos Roadmap-oldal (`orm.drizzle.team/roadmap`) felsorolja a hátralévő funkciókat („MSSQL support", „🎉 V1 RELEASE STREAM 🎉", „Down migrations, better rollbacks…", „MariaDB support" stb.), de **egyetlen konkrét dátumot sem** tartalmaz.
(https://orm.drizzle.team/roadmap)

A `drizzle-team/drizzle-orm` GitHub repóban nyitott kérdés:

> **[QUESTION] when will we have v1.0.0?** (#5660, nyitva, 2026-04-18 óta) — a közösségi válaszokban (nem maintainer) blokkoló hiányként a „down migrations" és a „Full RLS production ready support" szerepel; maintainer-válasz/dátum **nincs** a szálban.
(https://github.com/drizzle-team/drizzle-orm/issues/5660)

Egy korábbi, hivatalos maintainer-bejelentés (AndriiSherman, a Drizzle Team alapítója, tömeges issue-frissítő üzenetben, kb. 2025 vége):

> „We are hoping to get v1 for drizzle in beta this fall and same timeline for latest." … „Where it brings us: We are getting drizzle-orm into a new good shape where we can call it `drizzle-orm@1.0.0`!"
(https://github.com/drizzle-team/drizzle-orm/issues/1869, ugyanez megismételve: https://github.com/drizzle-team/drizzle-orm/issues/4760)

Ez a becslés (2025 ősz) **nem teljesült**: a `beta` tag csak 2026 elején vált release candidate-té (AndriiSherman, 2026-01-03: „This issue has been fixed in the `beta` tag, which serves as the release candidate for Drizzle v1"), és 2026-09-22-i állapot szerint (ld. 2a) még mindig RC-ben van, immár `rc.5`-nél.

**Verdikt: NEM ELDÖNTHETŐ.** Volt hivatalos, konkrét (ha nem is dátumszerű, hanem évszakos) ígéret — de az egy éve elavult, és azóta sem a Roadmap-oldal, sem a nyitott GitHub-kérdés nem tartalmaz újabb, hivatalos időbecslést. Harmadik, frissebb hivatalos nyilatkozatot (blog, X/Twitter) nem találtam a keresés során.

### 2c. Használható-e ParadeDB stabil Drizzle-lel, hivatalos csomag nélkül (`index().using('paradedb', …)` + nyers `sql`)

A Drizzle ORM `pg-core/indexes.ts` forrása egy, a jelenlegi 1.0 RC-ág előtti (stabil-korabeli) commit-változatban (`273c7807`) **szó szerint ugyanazt** a kódot tartalmazza, mint a jelenlegi `main`:

> „`export type PgIndexMethod = 'btree' | 'hash' | 'gist' | 'spgist' | 'gin' | 'brin' | 'hnsw' | 'ivfflat' | (string & {});`" … „**You can always specify any string you want in the method, in case Drizzle doesn't have it natively in its types**"
(https://github.com/drizzle-team/drizzle-orm/blob/273c7807/drizzle-orm/src/pg-core/indexes.ts, összevetve: https://raw.githubusercontent.com/drizzle-team/drizzle-orm/main/drizzle-orm/src/pg-core/indexes.ts)

A hivatalos Drizzle-dokumentáció (mintlify tükör, jelenlegi doksi-tartalom) is mutat `.using()`-mintát tetszőleges metódusnévvel (`gin`, `brin` stb.), külön RC-megjegyzés nélkül.
(https://drizzle-team-drizzle-orm.mintlify.app/schema/indexes)

**Verdikt: IGAZOLVA (technikai lehetőség).** Mivel az `.using(method, …)` API — amely a ParadeDB saját `paradedbIndex()` helperének is az alapja (ld. `sq06.md` 1.3 pontja) — már a stabil (RC előtti) Drizzle-ágban is jelen volt, és a nyers `sql` sablon-literál mindig elérhető volt/van, technikailag lehetséges `USING paradedb`/`bm25` indexet és `@@@`-lekérdezést stabil Drizzle-lel, a hivatalos `@paradedb/drizzle-paradedb` csomag nélkül is megvalósítani. **Korlát:** ezt konkrétan, végponttól végpontig (stabil `drizzle-kit@0.31.11` `generate`/`push` és tényleges ParadeDB migráció) senki hivatalos vagy közösségi forrás nem dokumentálja/tesztelte — a hivatalos csomag saját tesztje (ld. `sq06.md` 1.5 pont) kizárólag az RC `drizzle-kit/api-postgres`-t használja.

---

### 3. Drizzle natívan támogatja a `vector` oszlopot, távolságfüggvényeket, HNSW-indexet — stabil verzióban is?

A hivatalos „Vector similarity search with pgvector extension" útmutató (frissen lekérve):

> „You should have `drizzle-orm@0.31.0` and `drizzle-kit@0.22.0` or higher."
(https://orm.drizzle.team/docs/guides/vector-similarity-search)

Ugyanez az oldal a teljes mintát mutatja: `vector()` oszlop, `index('embeddingIndex').using('hnsw', table.embedding.op('vector_cosine_ops'))`, valamint `cosineDistance` a lekérdezésben — mindezt kifejezetten a fenti (0.31.0+) minimumverzió mellett.

A „PostgreSQL extensions" oldal (frissen lekérve) ugyanezt, kibővítve `halfvec`/`sparsevec`/`bit` típusokra és mind a hat távolságfüggvényre (`l2Distance`, `l1Distance`, `innerProduct`, `cosineDistance`, `hammingDistance`, `jaccardDistance`), valamint `hnsw`/`ivfflat` indexmintákra.
(https://orm.drizzle.team/docs/extensions/pg)

**Verdikt: IGAZOLVA.** Két, egymástól független hivatalos doksi-oldal egybehangzóan, RC-specifikus megjegyzés nélkül mutatja be a funkciót, és az explicit minimumverzió (0.31.0/0.22.0) jóval a jelenlegi stabil `latest` (0.45.3/0.31.11) alatt van — tehát a pgvector-integráció **régóta a stabil ág natív, beépített része**, nem RC-kizárólagos újdonság.

---

### 4a. Better Auth Drizzle-adapter Postgres-szel: Drizzle 1.0 RC-vel csak Better Auth 1.7 RC kompatibilis (PR #9489)?

A Better Auth `packages/drizzle-adapter/CHANGELOG.md` (1.7.0 bejegyzés):

> „#9489 `ea06c5a` Thanks @ping-maxwell! - Add a new `@better-auth/drizzle-adapter/relations-v2` entry point for projects using Drizzle Relations v2."
(https://github.com/better-auth/better-auth/blob/main/packages/drizzle-adapter/CHANGELOG.md, ill. konkrét commit: https://github.com/better-auth/better-auth/blob/c3688ba/packages/drizzle-adapter/CHANGELOG.md)

Harmadik fél (Dosu/Devin) összefoglalója, amely a hivatalos changelogra és a PR-re hivatkozik:

> „Better Auth added native support in `@better-auth/drizzle-adapter@1.7.0-beta.10` (via PR #9489, included in the v1.7 release)." … táblázat: „≥ 1.7.0 (RC+) | ✅ Default adapter | ✅ Use `/relations-v2` entry point"
(https://app.dosu.dev/cdda13d9-dd27-4d31-b09a-5d8bec92de21/documents/d44cb4d1-c83b-43d5-998a-c0a6dec2b641 — **T3, csak tájékozódásra**, a tényt az alábbi elsődleges forrásokkal ellenőriztem)

**Ám az npm registry szerint a Better Auth 1.7-es vonal mára stabil kiadás:**

> `better-auth` dist-tags: `"latest":"1.7.5"` (publikálva **2026-09-14**), `"rc":"1.7.0-rc.6"` (2026-08-14, „befagyott", a `latest` már elhagyta), `"release-1.6":"1.6.33"`.
(https://registry.npmjs.org/better-auth)

> `better-auth@1.7.0` publikálási időbélyege: `2026-08-18T00:10:16.757Z`.
(https://registry.npmjs.org/better-auth, `time` mező)

A hivatalos Better Auth blog is 1.7-et stabil kiadásként kommunikálja:

> „Better Auth 1.7" — publikálva **2026-08-17**. „We introduced the first part of this work in [the] 1.7 release candidate. … Follow the 1.7 upgrade guide for the migration steps."
(https://better-auth.com/blog/1-7)

**Verdikt: RÉSZBEN (elavult állítás).** Az eredeti állítás ténye — hogy a PR #9489 és a Drizzle-v1-kompatibilitás először a Better Auth **1.7 release candidate**-jében jelent meg — igaz volt a maga idejében (a fejlesztés `1.7.0-beta.10`-ben kezdődött, majd RC-ken át futott). **De 2026-09-22-i állapot szerint a Better Auth 1.7 már nem RC, hanem stabil, „latest"-tagelt kiadás** (jelenleg 1.7.5, 2026-09-14), tehát az „csak RC-vel kompatibilis" korlátozás **ma már nem helytálló**.

### 4b. Stabil Better Auth + stabil Drizzle (0.45) + Postgres működik-e?

A Better Auth **1.7.5** (jelenlegi „latest") npm-csomagjának `peerDependencies` mezője (közvetlen npm registry lekérdezés):

> `"drizzle-orm": "^0.45.2 || >=1.0.0-rc.1 <2.0.0"`, `"drizzle-kit": ">=0.31.4 || >=1.0.0-beta.1"`, `"pg": "^8.0.0"`
(https://registry.npmjs.org/better-auth/1.7.5)

Ezt megerősíti a PR, amely ezt a tartományt bevezette:

> „Expand `drizzle-orm` peer range in `packages/better-auth/package.json` to `^0.45.2 || >=1.0.0-rc.1 <2.0.0` and align `pnpm-lock.yaml` specifier to support 1.0 RCs and avoid peer conflicts; installs still resolve to `0.45.2` unless a 1.0 RC is present." (#10501, mergelve, review: „Thank you! I'm merging this 🫡")
(https://github.com/better-auth/better-auth/pull/10501)

Második, független megerősítés: a korábbi, **1.6.33** (`release-1.6` tag) `peerDependencies`-je is `"drizzle-orm": "^0.45.2"`-t ír elő — azaz a stabil 0.45.x sáv már a Drizzle-v1-támogatás bevezetése **előtt** is az egyetlen, hivatalosan deklarált, támogatott verzió volt.
(https://registry.npmjs.org/better-auth/1.6.33)

A Drizzle-adapter dokumentációja (`provider: "pg"`) a Postgres-módot már korábban is (RC-től függetlenül) leírta:
(https://better-auth.com/docs/adapters/drizzle — idézve `sq06.md` 4.1 pontjában)

**Verdikt: IGAZOLVA.** Két, egymástól független npm-lekérdezés (1.7.5 és a párhuzamosan karbantartott 1.6.33 branch) és a hivatalos PR-leírás egybehangzóan igazolja: a **stabil** Better Auth (akár a jelenlegi 1.7.x, akár a korábbi 1.6.x vonal) + **stabil** Drizzle (`^0.45.2`) + Postgres (`pg` provider) kombináció **hivatalosan, explicit peer-dependency szinten támogatott és működő** — ez volt/maradt az alapértelmezett, „biztonságos" konfiguráció.

---

### 5a. `Bun.sql` Postgres-kliens érettsége, hivatalos státusz

A Bun hivatalos főoldala (`bun.com`, frissen lekérve) marketing-szinten éretten kommunikálja:

> „## Bun in production … `bun run dev` for `bun run dev` and keep shipping" … „`Bun.sql` Postgres, MySQL, SQLite" … benchmark-táblázat: „Bun v1.4 | 20,243 queries/s | 80 MB" (vs. Node.js 10,000 queries/s, Deno 10,406 queries/s).
(https://bun.com/)

Ugyanakkor a hivatalos GitHub tracking issue jelenleg is **nyitva** van:

> **„`Bun.sql` tracking issue (Postgres client)"** (#15088) — State: **open**, utolsó frissítés 2026-01-05 (majd további issue-k hivatkoznak rá 2026 áprilisban, májusában).
(https://github.com/oven-sh/bun/issues/15088)

2026 június–júliusban (a kutatás időpontjához, 2026-09-22-höz képest **2–3 hónapja**) több, konkurenciafüggő, adatvesztést/leállást okozó hibát találtak és javítottak:

> **#32004** „SQL: connection pool stalls under concurrent begin() + parameterized queries" — bejelentve 2026-06-09, javítás-ellenőrzés: „Verified on main … the issue's repro script … completed 40/40 consecutive runs with no hang. The same script against a build predating both PRs (1.4.0-canary.1+1498d7b77) hung 2/10."
(https://github.com/oven-sh/bun/issues/32004)

> **#32772** „sql(postgres): stop sending a redundant Sync after a simple Query" — mergelve 2026-06-26. „`Bun.SQL` (Postgres) silently delivers another query's rows to the wrong query, with no error, when a simple-protocol query runs concurrently with a not-yet-prepared parameterized query on the same connection."
(https://github.com/oven-sh/bun/pull/32772)

> **#33665** „Bun SQL prepared statement cache causes intermittent Postgres decode/protocol errors under concurrency" — bejelentve 2026-07-07, Bun 1.3.14 ellen, root cause megerősítve és más PR-hez kapcsolva javításra.
(https://github.com/oven-sh/bun/issues/33665)

**Verdikt: RÉSZBEN.** A `Bun.sql` hivatalosan promózott, benchmarkolt, aktívan fejlesztett Postgres-kliens, alapszintű használatra funkcionális és gyors — de a saját tracking issue-ja nyitva van, és a kutatás időpontjához képest néhány hónapon belül is kerültek elő és javultak **helyességi** (nem csak teljesítmény-) hibák konkurens/pooling forgatókönyvekben. Ez arra utal, hogy 2026-09-22-i állapotában **aktívan érő, de még nem lezárt/nem "kőbe vésett" stabilitású** komponens — explicit „production-ready" vagy „stabil API" hivatalos minősítést egyik forrásban sem találtam, csak implicit (marketing-szintű) promóciót.

### 5b. Mely Drizzle Postgres-driverek támogatottak Bun alatt stabilan (postgres.js, node-postgres, bun-sql)?

A hivatalos Bun SQL-dokumentáció FAQ-szekciója (frissen lekérve, `docs/runtime/sql.mdx`):

> „## Frequently Asked Questions … You can use npm packages like postgres.js, pg, and node-postgres in Bun … They're great options."
(https://github.com/oven-sh/bun/blob/88a63988/docs/runtime/sql.mdx)

A Drizzle hivatalos „Bun SQL" oldala:

> „Drizzle ORM natively supports `bun sql` module and it's crazy fast 🚀" — telepítés `drizzle-orm@rc`/`drizzle-kit@rc` csomagokkal.
(https://orm.drizzle.team/docs/connect-bun-sql — idézve `sq06.md` 3.2 pontjában)

A Drizzle „Get Started – PostgreSQL" oldala mindhárom drivert (`node-postgres`, `postgres.js`, „Bun SQL") felsorolja, rangsorolás nélkül.
(https://orm.drizzle.team/docs/get-started-postgresql — idézve `sq06.md` 3.3 pontjában)

Korábbi (2024 végi), már lezárt regresszió a `postgres.js`/Bun kombinációra:

> „postgres-js queries hang indefinitely on Bun 1.1.35+" (#15438) — Closed, javítás: PR #15543.
(https://github.com/oven-sh/bun/issues/15438)

**Verdikt: RÉSZBEN.** Mindhárom driver (`postgres.js`, `node-postgres`/`pg`, `Bun.sql`/`bun-sql`) hivatalosan dokumentált és a Bun saját FAQ-ja explicit jóváhagyja mindhármat („great options") — de **egyik forrás sem mond ki explicit, egyértelmű rangsorolást** arra, melyik a Bun alatt „hivatalosan javasolt" választás; a `bun-sql` Drizzle-integrációja emellett (ld. 2a/5a) még RC-csomagokhoz kötött, míg a `postgres.js`/`pg` a stabil Drizzle-lel is használható, saját (részben már javított) Bun-specifikus hibatörténettel.

---

### 6. macOS-en a `bun:sqlite` a rendszer SQLite-ját használja → bővítmény (pl. `sqlite-vec`) nem tölthető be; igaz-e ma (Bun 1.4), és van-e dokumentált kerülőút?

A hivatalos, **ma lekért** Bun SQLite-dokumentáció:

> „macOS users By default, macOS ships with Apple's proprietary build of SQLite, which doesn't support extensions. To use extensions, install a vanilla build of SQLite." … „To point `bun:sqlite` to the new build, call `Database.setCustomSQLite(path)` before creating any `Database` instances. (On other operating systems, this is a no-op.) Pass a path to the SQLite `.dylib` file, not the executable."
(https://bun.com/docs/runtime/sqlite.md)

Ugyanezt egy másik, önálló hivatalos API-referencia oldal is megerősíti:

> „On macOS, this requires linking a custom SQLite3 library because the Apple build of SQLite disables loading extensions. See `Database.setCustomSQLite`." … „Bun chooses the Apple build of SQLite on macOS because it brings a ~50% performance improvement."
(https://bun.com/reference/bun/sqlite/Database/loadExtension)

**Két friss (2026 augusztusi), a hiba jelenlegi fennállását igazoló GitHub-issue**, kifejezetten a kutatáshoz közeli Bun-verziókon reprodukálva:

> **#38647** „bun:sqlite: statically link Bun's bundled SQLite on macOS too" — „What version of Bun is running? **1.3.14 (also reproduces on 1.4.0-canary)**." … „The only documented workaround … requires every end user to `brew install sqlite` and call `Database.setCustomSQLite(path)`."
(https://github.com/oven-sh/bun/issues/38647, bejelentve 2026-08-14)

> **#38772** (ugyanaz a hiba, más bejelentő) — „What version of Bun is running? **1.3.14**." Mindkettőt a fenntartó-bot **#16717**-tel duplikátumként zárta le, amely maga **nyitva van** (state: open, utolsó frissítés 2026-08-16).
(https://github.com/oven-sh/bun/issues/38772, https://github.com/oven-sh/bun/issues/16717)

A dokumentált kerülőutat harmadik fél (a `sqlite-vec` hivatalos repója) is megerősíti, gyakorlati kóddal:

> „MacOS *might* have to do this, as the builtin SQLite library on MacOS doesn't allow extensions: `Database.setCustomSQLite('/usr/local/opt/sqlite3/lib/libsqlite3.dylib');`"
(https://github.com/asg017/sqlite-vec/issues/78, ill. https://github.com/asg017/sqlite-vec/blob/main/site/using/js.md)

**Ellentmondás/árnyalat, amit a keresés feltárt:** volt egy 2026 májusában **mergelt** hivatalos PR (#31293, „build: enable static SQLite by default on macOS"), amely a `staticSqlite` build-flag alapértékét `true`-ra állította macOS-en, és a hozzá tartozó issue-kommentár szerint ennek „side benefit"-je lett volna, hogy a `loadExtension()` „out of the box" működjön. **Ennek ellenére** a fent idézett #38647/#38772 issue-k **három hónappal később (2026 augusztus)**, kifejezetten Bun **1.3.14 és 1.4.0-canary** alatt **továbbra is reprodukálják** az eredeti hibát, és a **ma lekért** hivatalos dokumentáció is változatlanul az Apple-féle rendszer-SQLite-ot és a `setCustomSQLite` kerülőutat írja le. Ennek pontos okát (a build-flag nem került éles kiadásba, vagy más regresszió történt) a rendelkezésre álló források nem magyarázzák meg egyértelműen — ezt NEM ELDÖNTHETŐ részletként jelzem.

**Verdikt: IGAZOLVA.** A leírt probléma (macOS rendszer-SQLite → bővítmény nem tölthető be) a mai napig (Bun 1.4 vonal, beleértve a `1.4.0-canary`-t is) fennáll, hivatalos forrásból és két független, 2026 augusztusi GitHub-issue-ból is megerősítve; a dokumentált kerülőút (`Database.setCustomSQLite(path)`, Homebrew-SQLite `.dylib`-re mutatva) ma is a hivatalos és a közösségi (pl. `sqlite-vec`) dokumentáció szerint is érvényes és működő megoldás.

---

## Amit ez a döntésre jelent

1. A ParadeDB hivatalos Drizzle-csomagja (0.5.0, 2026-08-21, MIT) és a Drizzle 1.0 közötti kötés **ma is fennáll**: a csomag peer-dependencyje mereven `1.0.0-rc.4`-hez van kötve, miközben az npm „latest" stabil Drizzle 0.45.3/0.31.11.
2. Nincs friss, hivatalos, konkrét dátum a Drizzle 1.0 stabil megjelenésére; az egyetlen fellelhető hivatalos időbecslés (2025 ősz) régen lejárt, és a fejlesztés azóta is RC-fázisban van (jelenleg `rc.5`).
3. Technikailag lehetséges ParadeDB-indexet és `@@@`-lekérdezést a **stabil** Drizzle-lel, a hivatalos RC-kötött csomag nélkül megvalósítani (`index().using('paradedb', …)` + nyers `sql`), mert ez az API már a stabil ágban is jelen van — de ennek konkrét, gyakorlati (migrációgenerálási) működését senki nem dokumentálta/tesztelte nyilvánosan.
4. A pgvector-alapú vektoros keresés (oszloptípus, távolságfüggvények, HNSW/IVFFlat index) **régóta, a stabil Drizzle-ágban is** natívan elérhető (min. 0.31.0/0.22.0 óta) — ez nem függ a Drizzle 1.0 RC-ágtól.
5. A Better Auth + Drizzle + Postgres kompatibilitási kép **időközben megváltozott** azóta, hogy a „csak 1.7 RC" megállapítás született: a Better Auth 1.7 mára stabil kiadás, és explicit peer-dependency-szinten egyszerre támogatja mind a stabil Drizzle 0.45.x-et, mind a Drizzle 1.0 RC-t.
6. A Bun-oldali kockázatok (a `Bun.sql` még nyitott tracking issue-ja és friss konkurenciahibái, illetve a macOS `bun:sqlite`/bővítmény-probléma) továbbra is fennállnak a kutatás időpontjában (Bun 1.4 vonal) — utóbbira van hivatalosan dokumentált, működő kerülőút, előbbire (a Bun.sql érettsége) nincs hivatalos „production-ready" minősítés, csak marketing-szintű promóció és aktív hibajavítási történet.

---



---

# ELL05 — Összevetési alap: sima Postgres + pgvector, ParadeDB nélkül

**Módszer:** Kizárólag az Exa eszközökkel kerestem (`mcp__Exa__web_search_exa`, `mcp__Exa__web_fetch_exa`), a `_ell_kozos.txt` utasítása szerint — az Exa elérhető volt, nem kellett leállni. A beépített WebSearch/WebFetch-et nem használtam. `curl`-t nem kellett bevetni, minden nyers forrás (GitHub release, postgresql.org hír) Exa-val is elérhető volt. Az `anthropic-skills:deep-web-research` alügynök-indítást nem hívtam meg (ez egy fókuszált adverzariális ellenőrző kör, nem teljes kutatási kampány), helyette degradált módban, közvetlen Exa-kereséssel/-olvasással dolgoztam, minden állítást két független forrással igyekezve alátámasztani.

## Verdikt-összefoglaló

| # | Állítás | Verdikt | Egy mondat |
|---|---|---|---|
| 1 | Van (legalább részben) független minőségi értékelés a Snowball `hungarian` tövezőről, és az kedvező képet fest róla | RÉSZBEN | Van tudományos értékelés, de az egyik fő forrás maga a Snowball-magyar szerzőitől származik, és a ténylegesen független korpusz-alapú vizsgálat (Endrédy 2015) kifejezetten *gyengének* minősíti az algoritmikus (Snowball) tövezést a morfológiai elemzőkhöz (Humor, Hunmorph) képest. |
| 2 | Az `unaccent` bővítmény hivatalos dokumentációja szerint egy mezőn belül kombinálható tövezéssel (pl. `hungarian_stem`) | IGAZOLVA | A hivatalos `unaccent` doksi konkrét SQL-mintát ad erre (francia példával), ami nyelv-függetlenül ugyanúgy működik `hungarian_stem`-mel is. |
| 3 | A sima Postgresben nincs beépített BM25, csak `ts_rank`/`ts_rank_cd` | IGAZOLVA | A hivatalos doksi kimondja: „PostgreSQL provides two predefined ranking functions” — ez a kettő az egyetlen beépített rangsoroló, BM25 nincs közöttük. |
| 4 | Van érett, engedékeny licencű (PostgreSQL License) BM25-bővítmény sima Postgreshez, amely production-ready állapotban van | IGAZOLVA | A Timescale `pg_textsearch` v1.0 GA 2026.04.03-án jelent meg „Postgres license” alatt, jelenlegi kiadása v1.4.0 (2026.08.18), a repó „Production ready” státuszt hirdet. |
| 5 | A `tsvector` alapértelmezett parsere egységesen, „hword_numpart”-ként kezeli az olyan kódokat, mint a `PROJ-4412` (betű + kötőjel + szám) | MEGDŐLT | A hivatalos doksi táblázatának mintapéldája (`postgresql-beta1`) félrevezető erre az esetre: kötőjel + *csak számjegyekből álló* rész esetén a parser a kötőjelet mínuszjelnek értelmezi, és a végeredmény egy külön `asciiword` + egy `int` (előjeles egész) token, nem egy összetartozó hword. |
| 6 | Az aláhúzásos azonosítókat (pl. `RATE_LIMIT_URL`) a parser egyben, egyetlen tokenként kezeli | MEGDŐLT | Az aláhúzás nem szóalkotó karakter a parser számára: `RATE_LIMIT_URL` három külön lexémára esik szét (`rate`, `limit`, `url`), amit két egymástól független, empirikusan reprodukált forrás is megerősít. |
| 7 | A `pg_trgm` a `tsvector` pontos lexéma-egyezésétől eltérően valódi rész-szó/elgépelés-tűrő keresést biztosít | IGAZOLVA | A hivatalos `pg_trgm` doksi explicit kimondja, hogy a keresőkifejezésnek nem kell „left-anchored”-nak lennie, és index is támogatja a `LIKE`/hasonlósági kereséseket. |
| 8 | Van dokumentált minta a `tsvector` + `pgvector` RRF-alapú hibrid keresésére hivatalos/közösségi Postgres-anyagban | IGAZOLVA | A `pgvector` hivatalos README explicit RRF-et javasol a `tsvector`+`pgvector` kombinációhoz, és ezt több független (Supabase, Jonathan Katz/AWS) forrás is részletes SQL-mintával dokumentálja. |
| 9 | A korábbi kör (SQ03/SQ07) pontosan idézte a vineeth.fyi blog számait és módszertanát (14×/48×/164×, 1,6M Amazon-termék, nincs hardver-adat) | IGAZOLVA | A blog közvetlen lekérésével minden szám (401ms/92ms, 22838ms/139ms, 4399ms/90ms, 7ms/2ms, 6ms/89ms) és a hardver-adat hiánya szó szerint egyezik a korábbi kör idézetével. |
| 10 | A vineeth.fyi blog egy tőle és a ParadeDB-től **független** mérés | MEGDŐLT | A blog szerzője, Vineeth Pothulapati a publikálás idején (2025.08.) a Timescale/TigerData (a ParadeDB-vel közvetlenül versengő Postgres-bővítmény-gyártó, saját BM25-motorral, a `pg_textsearch`-csel) alkalmazottja volt — ezt a blogbejegyzés nem tünteti fel, és ez alapjaiban kérdőjelezi meg a „független” minősítést. |

## Állításonként

### 1–2. Magyar szöveges keresés `tsvector`-ral: `hungarian` minőség, `unaccent`, kombinálhatóság

**A `hungarian_stem` a hivatalos Snowball-tövezők listáján szerepel** (PostgreSQL 18 dokumentáció, `\dFd` psql-parancs kimenete):
> „pg_catalog | hungarian_stem | snowball stemmer for hungarian language”
Forrás: https://www.postgresql.org/docs/18/textsearch-psql.html (PostgreSQL Global Development Group, hivatalos doksi, T1)

A `hungarian` mint **teljes konfiguráció** (nem csak szótár) létezik és használatban is van éles rendszereken (`default_text_search_config = 'pg_catalog.hungarian'`), amit több egymástól független, valós szerverkonfigurációt idéző forrás mutat:
> „default_text_search_config = 'pg_catalog.hungarian'”
Forrás 1: https://gist.github.com/1883375 (2011, Mahara bugjelentéshez csatolt valós `SHOW ALL` kimenet, T3)
Forrás 2: https://postgrespro.ru/list/thread-id/2062481 (2011, postgresql.org levelezőlista-archívum tükrözése, T2)

**Független minőségi értékelés — de nem egyértelműen kedvező.** A CLEF 2005 hivatalos magyar ad-hoc feladatához készült tanulmány („Four Stemmers and a Funeral: Stemming in Hungarian at CLEF 2005”, Anna Tordai & Maarten de Rijke) Paice-módszerrel (understemming/overstemming/ERRT) és visszakeresési (MAP, R-precision) méréssel hasonlított össze négy általuk fejlesztett algoritmikus (Snowball-alapú) tövezőt:
> „The experiments on which we report in this paper confirm that stemming in Hungarian greatly improves retrieval effectiveness. […] The 4-gram had the highest average scores of all the runs, but for this data, it was not significantly higher than the scores of the best stemmer.”
Forrás: https://staff.fnwi.uva.nl/m.derijke/wp-content/papercite-data/pdf/tordai-four-2006.pdf (LNCS 4022, T2 — **fontos**: Tordai és de Rijke maguk a Snowball magyar tövező szerzői is, tehát ez az értékelés nem tekinthető a szótártól teljesen független külső auditnak).

Egy **ténylegesen harmadik féltől** származó, korpusz-alapú összehasonlítás (Endrédy István, 2015, Szegedi Treebank, 10 tövező/lemmatizáló 3 nyelven) viszont kifejezetten a Snowball-t találja a leggyengébbnek magyarra:
> „Since this language is heavily agglutinative, stemming improves the F-score significantly, even with the weakest stemmer (more than 50% difference comparing to the results without any stemmer). The best scores belong to the Humor stemmer in both methods. Algorithmic stemming is not appropriate for this language.”
Forrás: https://real.mtak.hu/34378/1/ei_corpus_eval_of_stemmers_ltc_u.pdf (Endrédy 2015, LTC konferencia, T2, a szerző nem kötődik a Snowball-magyarhoz)

Egy informális, de konkrét számot közlő közösségi projekt ugyanezt támasztja alá:
> „{:hunspell 32,91%, :snowball 47,41%, :hunspell-mdb 32,91%} […] This means Hunspell is 27% more accurate than Snowball.”
Forrás: https://github.com/damesek/hustem (T3, hibaarány-mérés a Snowball `.sbl` konfiguráción)

**Ékezet-lehagyás `unaccent`-tel — hivatalos doksi, és igen, kombinálható tövezéssel egy mezőn belül.** A hivatalos `unaccent` fejezet konkrét, futtatható SQL-mintát ad a kombinációra (francia nyelvre, de a mechanizmus nyelvfüggetlen — a `french_stem` helyére bármelyik Snowball-szótár, így `hungarian_stem` is írható):
> „Here is an example showing how to insert the unaccent dictionary into a text search configuration: […] `CREATE TEXT SEARCH CONFIGURATION fr ( COPY = french );` `ALTER TEXT SEARCH CONFIGURATION fr ALTER MAPPING FOR hword, hword_part, word WITH unaccent, french_stem;` […] `unaccent` is a text search dictionary that removes accents (diacritic signs) from lexemes. It's a filtering dictionary, which means its output is always passed to the next dictionary (if any)”
Forrás: https://www.postgresql.org/docs/current/unaccent.html (T1, hivatalos)

Ugyanezt a mintát egy második, függetlenül karbantartott extension-katalógus is megismétli, megerősítve, hogy ez a bevett, dokumentált munkamenet:
> „-- Create an accent-insensitive French text search config […] ALTER TEXT SEARCH CONFIGURATION fr ALTER MAPPING FOR hword, hword_part, word WITH unaccent, french_stem;”
Forrás: https://github.com/pgsty/pgext/blob/dd1d49ca8606fd0962ccd602ea1ed59cbdba1b6a/content/e/unaccent.md (T2/T3, közösségi katalógus)

**Magyar-specifikus, hivatalos, kész példa nem került elő** — csak az általános, nyelvfüggetlen minta létezik hivatalosan dokumentálva; a `hungarian_stem`-mel való konkrét kombináció felhasználói/közösségi alkalmazás, nem hivatalos doksi-tétel.

### 3. Rangsorolás: van-e BM25 a sima Postgresben?

**Nincs — csak `ts_rank`/`ts_rank_cd`, szó szerint a hivatalos doksiból:**
> „PostgreSQL provides two predefined ranking functions, which take into account lexical, proximity, and structural information […] The two ranking functions currently available are: `ts_rank(...)` […] `ts_rank_cd(...)` […] This function computes the cover density ranking for the given document vector and query, as described in Clarke, Cormack, and Tudhope's ‘Relevance Ranking for One to Three Term Queries' in the journal ‘Information Processing and Management', 1999.”
Forrás: https://www.postgresql.org/docs/current/textsearch-controls.html (T1, hivatalos, 12.3.3. szakasz)

A hivatalos C forráskód is megerősíti, hogy csak ez a két rangsoroló-család (és azok normalizálási bitmaszk-változatai) léteznek a `tsearch` motorban, BM25-specifikus komponens (IDF, dokumentumhossz-korpusz-statisztika) nélkül:
Forrás: https://github.com/postgres/postgres/blob/92268b35d04c2de416279f187d12f264afa22614/src/backend/utils/adt/tsrank.c (T1, hivatalos forráskód)

Egy független, technikai blog pontosan megfogalmazza, mi hiányzik ehhez BM25-höz képest:
> „Postgres full-text search does not implement it [BM25]. `ts_rank_cd` weighs term frequency and proximity but has no corpus-wide IDF term.”
Forrás: https://learnbackend.com/guides/hybrid-search-postgres-bm25-pgvector/ (T3, blog, 2026.07.29)

**Érett, permisszív licencű BM25-bővítmény létezik: Timescale `pg_textsearch`.** Hivatalos GA-bejelentés a postgresql.org hírfolyamán:
> „I'm delighted to announce the general availability of pg_textsearch v1.0. This is an open source extension (Postgres license) supporting modern BM25 ranked keyword search with fast indexing and state-of-the-art query performance […] https://github.com/timescale/pg_textsearch”
Forrás: https://www.postgresql.org/about/news/pg_textsearch-v10-3264/ (T1, hivatalos postgresql.org hír, 2026.04.03)

A GitHub repó jelenlegi állapota (lekérés dátuma: 2026.09.22):
> „🚀 **Status**: v1.4.0-dev - Production ready. […] pg_textsearch supports PostgreSQL 17 and 18.”
> „License: PostgreSQL License […] Created: 2025-07-06T17:45:50Z”
Forrás: https://github.com/timescale/pg_textsearch (T1, hivatalos repó)

Legfrissebb kiadás: **v1.4.0, közzétéve 2026.08.18** (a `v0.6.0` release-jegyzék szerint már akkor is „On MS-MARCO v2 (133M documents, 47GB base data), query throughput is now 3.5X higher than the leading Postgres-based BM25 extension” — ez a Timescale saját, nem független állítása, itt csak verzió/dátum-igazolásra idézve):
Forrás: https://github.com/timescale/pg_textsearch/releases/tag/v1.4.0 és https://github.com/timescale/pg_textsearch/releases (T1, hivatalos)

Megjegyzés függetlenségről: maga a GA-bejelentés is versenytárs-összehasonlítást tartalmaz — „substantial performance advantages vs ParadeDB, which has a much more restrictive license (AGPL…)” — ez a Timescale saját (nem semleges) marketingállítása, nem ellenőriztem tovább, mert a feladat 2. pontja csak a `pg_textsearch` állapotára/licencére/verziójára kérdez.

Van egy másik, kevésbé érett (0.2.0-s, kísérleti) alternatíva is, `pg_fts` néven, amely szintén saját BM25/BM25F-motort épít, de ez explicit önmagát „nem termelésre kész”-ként pozicionálja a saját összehasonlító anyagában (nem részleteztem tovább, mert a kérdés a „legalább egy érett, engedékeny licencű” esetre kérdez, amit a `pg_textsearch` már megválaszol).
Forrás: https://pgxn.org/dist/pg_fts/0.2.0/ (T3, PGXN-bejegyzés)

### 4. Azonosítók a `tsvector`-ban: `PROJ-4412`, `RATE_LIMIT_URL`, `bun run release`

**A hivatalos parser-táblázat (23 tokentípus) szerint** létezik `hword_numpart` („Hyphenated word part, letters and digits”), és a dokumentáció mintapéldája (`postgresql-beta1` → `hword_asciipart` „postgresql” + `hword_numpart` „beta1”) *azt sugallja*, hogy egy betű+szám kötőjeles kód (mint `PROJ-4412`) hasonlóan viselkedne:
> „`numhword` | Hyphenated word, letters and digits | `postgresql-beta1` […] `hword_numpart` | Hyphenated word part, letters and digits | `beta1` in the context `postgresql-beta1`”
Forrás: https://www.postgresql.org/docs/current/textsearch-parsers.html (T1, hivatalos, 12.5. szakasz)

**Ez a várakozás azonban MEGDŐL, ha a kötőjel utáni rész kizárólag számjegyekből áll** (mint a `4412` a `PROJ-4412`-ben) — a parser ekkor a kötőjelet **mínuszjelnek** értelmezi, nem szóösszekötő kötőjelnek. Egy Stack Overflow-válasz konkrét `ts_debug()`-kimenettel demonstrálja:
> „`SELECT * FROM ts_debug('english', 'abc-001');` […] `asciiword | Word, all ASCII | abc | {simple} | simple | {abc}` `int | Signed integer | -001 | {simple} | simple | {-001}`”
Forrás: https://stackoverflow.com/questions/57795085/postgres-full-text-search-with-hyphen-and-numerals (T3, de reprodukálható SQL-lel alátámasztva)

Ugyanezt **egy második, egymástól teljesen független forrás** — a hivatalos PostgreSQL `pgsql-general` levelezőlista — is megerősíti, ráadásul pont a kérdésben szereplőhöz nagyon hasonló, betű-kód mintázatra (`UVW-789-XYZ`):
> „to_tsvector('simple', 'UVW-789-XYZ') is 'uvw':1 '-789':2 'xyz':3 because -789 is a negative integer. If we turn the query '789-XYZ' into the tsquery as before, we get to_tsquery('simple', '789 <-> xyz') which doesn't match it.”
Forrás: https://www.postgresql.org/message-id/CAAmRUjt8XNGWKUiPA3uQ6%2B7UaPTNOsrfQVF-gPcS9zZnM5PW3Q%40mail.gmail.com (T2, hivatalos postgresql.org levelezőlista-archívum, 2019.10.14)

A postgresql.org lista egy másik válasza megerősíti a jelenség fennállását és a hivatalos kerülő megoldást (`dict-int` bővítmény `absval` paramétere, PG13+):
> „As an ad-hoc solution, you could add a dictionary that turns a negative integer into its positive counterpart. There's a dictionary in contrib that can be used as a starting point: https://www.postgresql.org/docs/current/dict-int.html”
Forrás: https://postgrespro.com/list/id/abf85423-ce4b-45ec-97a4-2789a400ed55@manitou-mail.org (T2)

**Gyakorlati következmény:** egy `PROJ-4412`-szerű azonosító a `tsvector`-ban **nem** egyetlen összetartozó „proj-4412” hword-ként és nem is tiszta `proj`+`4412` párként jelenik meg alapból, hanem `proj` (szó) + `-4412` (előjeles egész, a mínuszjellel együtt tárolt lexémaként) formában — emiatt a `4412`-re (előjel nélkül) való keresés alapértelmezésben **nem** találja meg a `PROJ-4412`-t tartalmazó sort, workaround (kötőjel cseréje, egyedi `dict-int absval` szótár, vagy tsquery utólagos regex-átalakítása) nélkül. Egy 2007-es hivatalos commit-üzenet és egy azonos évi fejlesztői vita is jelzi, hogy a kötőjel+szám-kombinációk kezelése régóta ismert, nem teljesen konzisztens sarokeset a parserben:
> „Change text search parsing rules for hyphenated words so that digit strings containing decimal points aren't considered part of a hyphenated word.”
Forrás: https://www.postgresql.org/message-id/20071027190345.A5D1E754229%40cvs.postgresql.org (T1, hivatalos commit-log)

**Az aláhúzásos azonosítók (`RATE_LIMIT_URL`) sem maradnak egyben.** Az aláhúzás nem számít szóalkotó karakternek a parser állapotgépében, ezért a token szétesik komponensekre, amit két, egymástól független, valós rendszeren reprodukált forrás mutat:
> „`select to_tsquery('english', '("test_with_underscore")');` → `'test' & 'underscor'`”
Forrás: https://stackoverflow.com/questions/59727819/how-to-escape-underscores-in-while-preparing-tsquery-for-postgresql-full-text-se (T3)
> „to_tsquery for a word with an underscore is splitting that word into multiple parts: `select to_tsquery('english', '("test_with_underscore")');` → `'test' & 'underscor'`”
Forrás: https://github.com/mattermost/mattermost-server/issues/14436 (T3, Mattermost hivatalos GitHub-issue-ja, 2020.04.30)

(A hivatalos parsertáblázat maga nem tárgyalja explicit módon az aláhúzás sorsát a `word`/`asciiword` típusokban — ez a viselkedés csak a két empirikus, egymástól független reprodukción alapul, nem közvetlen hivatalos doksi-idézeten.)

**`bun run release`** — ez három különálló, szóköz-elválasztott ASCII-szó, amit a parser egyszerűen három külön `asciiword` tokenként dolgoz fel (nincs kötőjel/aláhúzás, nincs speciális eset); a konfigurációtól függően mindegyik saját tövezésen megy át (pl. `english` konfiguráció esetén a `release`→`releas` stemmelődne). Ez a hivatalos `to_tsvector`/`ts_debug` alapmechanizmusból következik, külön empirikus igazolást nem igényelt:
Forrás: https://www.postgresql.org/docs/current/textsearch-controls.html és https://www.postgresql.org/docs/18/textsearch-debugging.html (T1)

**A pontos egyezés vs. rész-szó kérdésre**: a `tsvector`/`tsquery` alapból **lexéma-egyezést** csinál (a `@@` operátor), nincs beépített rész-szó/substring keresés; erre a **`pg_trgm`** bővítmény ad megoldást:
> „`pg_trgm` ignores non-word characters (non-alphanumerics) when extracting trigrams from a string. […] Unlike B-tree based searches, the search string need not be left-anchored.”
Forrás: https://www.postgresql.org/docs/current/pgtrgm.html (T1, hivatalos)
Ezt egy második, verzió-független forrás (a PostgreSQL forráskód SGML-dokumentációja) is megerősíti, benne a trigram-index (GiST/GIN) LIKE/ILIKE/regex-támogatásának leírásával:
Forrás: https://github.com/postgres/postgres/blob/master/doc/src/sgml/pgtrgm.sgml (T1, hivatalos forráskód-doksi)

### 5. Hibrid keresés sima Postgresben: van-e dokumentált RRF-minta?

**Igen, a `pgvector` hivatalos README-je explicit RRF-et javasol:**
> „## Hybrid Search — Use together with Postgres full-text search for hybrid search. `SELECT id, content FROM items, plainto_tsquery('hello search') query WHERE textsearch @@ query ORDER BY ts_rank_cd(textsearch, query) DESC LIMIT 5;` You can use Reciprocal Rank Fusion or a cross-encoder to combine results.”
Forrás: https://github.com/pgvector/pgvector/blob/master/README.md (T1, hivatalos)

Ez a mintát részletes, futtatható SQL-formában két, egymástól független, elismert forrás is kidolgozza:
> „## Hybrid search in Postgres — Implement hybrid search in Postgres using `tsvector` (keyword search) and `pgvector` (semantic search). […] `create or replace function hybrid_search(...) ... order by coalesce(1.0 / (rrf_k + full_text.rank_ix), 0.0) * full_text_weight + coalesce(1.0 / (rrf_k + semantic.rank_ix), 0.0) * semantic_weight desc”
Forrás: https://supabase.com/docs/guides/ai/hybrid-search (T2, hivatalos Supabase-dokumentáció)

> „There are a variety of methods used to score the results, with reciprocal ranked fusion (RRF) being very popular. […] PostgreSQL includes several full-text search methods, including tsearch2 and pg_trgm.”
Forrás: https://jkatz.github.io/post/postgres/hybrid-search-postgres-pgvector/ (Jonathan Katz, T2 — a szerző a PostgreSQL core fejlesztői/AWS közösség ismert tagja, technikailag semleges forrás)

Fontos, hogy a `ts_rank_cd`-alapú RRF **nem BM25-alapú** — a Supabase-minta kódkommentje is jelzi ezt a korlátot:
> „-- Note: ts_rank_cd is not indexable but will only rank matches of the where clause -- which shouldn't be too big”
Forrás: https://supabase.com/docs/guides/ai/hybrid-search (T2)

### Kiegészítő pont: a korábbi kör független mérésének (vineeth.fyi) ellenőrzése

A blog közvetlen lekérése után **minden szám pontosan egyezik** a korábbi kör (SQ03/SQ07) idézetével:
> „### Full-Text Search — PostgreSQL: 401ms average — ParadeDB: 92ms average — ParadeDB is 4.4x faster […] ### Fuzzy Search (Handling typos) — PostgreSQL: 22,838ms average — ParadeDB: 139ms average — ParadeDB is 164x faster ### Field-Specific Search — PostgreSQL: 4,399ms average — ParadeDB: 90ms average — ParadeDB is 48x faster ### Boolean Queries — PostgreSQL: 7ms average — ParadeDB: 2ms average — ParadeDB is 3.5x faster ### Exact Phrase — PostgreSQL: 6ms average — ParadeDB: 89ms average — PostgreSQL is 14x faster”
> „Both running PostgreSQL 17. Vanilla PG needed 11 indexes (GIN for full-text, pg_trgm for fuzzy). ParadeDB uses one BM25 index.”
Forrás: https://www.vineeth.fyi/blog/pg-vs-pg-search/ (közzététel: 2025.08.15, közvetlen lekérés dátuma: 2026.09.22)

A hardver-adat hiánya is megerősíthető: a teljes cikkben **egyetlen CPU/RAM/lemez-specifikáció sem szerepel** — ez alátámasztja a korábbi kör „NINCS FORRÁS” megjegyzését a hardverre.

**Az „független mérés” minősítés viszont MEGDŐL.** A szerző, Vineeth Pothulapati, a blogbejegyzés közzétételének idején (2025 augusztusa) a **Timescale / TigerData** (a TimescaleDB készítője, és — mint a 3. pontban látható — a ParadeDB-vel közvetlenül versengő saját BM25-Postgres-bővítmény, a `pg_textsearch` gyártója) alkalmazottja volt:
> „Vineeth Pothulapati: Senior Product Manager at TigerData (creators of TimescaleDB) for 1 year 5 months with 9 years 5 months of total professional experience. Previous roles include Product Manager at TigerData (creators of TimescaleDB), Associate Product Manager at TigerData (creators of TimescaleDB), and Software Engineer at TigerData (creators of TimescaleDB).”
Forrás: https://www.linkedin.com/posts/vineeth-pothulapati_speed-without-sacrifice-building-the-modern-activity-7341450784372310016-ZLEI (LinkedIn, 2025.06.19-i poszt, tehát ~2 hónappal a blogbejegyzés előtt már TigerData-alkalmazott)

> „**Currently, my focus is on improving user onboarding and paid conversions for Timescale's SaaS offering.** […] Software Engineer, Timescale [Nov, 2020 - Nov, 2021]”
Forrás: https://www.vineeth.fyi/about/ (a szerző saját „About me” oldala, T3, önbevallott)

Ezt a blogbejegyzés (`pg-vs-pg-search`) maga **sehol nem tünteti fel** — nincs affiliáció-nyilatkozat, nincs disclosure a Timescale/TigerData-kötődésről, holott a Timescale saját BM25-terméke (`pg_textsearch`) a bejegyzés írásakor még nem volt kész (GA csak 2026.04.03-án), és a Timescale hivatalos GA-bejelentése kifejezetten a ParadeDB-vel versenyezve pozicionálja a terméket. Ez alapvető, be nem jelentett érdekütközés egy „PostgreSQL vs ParadeDB” összehasonlításban, amelyet a korábbi kutatási kör (SQ03, SQ07) „független blog”-ként, illetve „nincs feltüntetett ParadeDB- vagy versenytárs-affiliációja” megjegyzéssel idézett.

## Amit ez a döntésre jelent

1. **A magyar szöveges keresés Snowball-alapon (a beépített `hungarian` konfigurációval) a legjobban dokumentált, ténylegesen független tudományos mérés szerint a leggyengébb kategóriájú tövező magyar nyelvre** — a Humor/Hunmorph-féle morfológiai elemzők jobban teljesítenek, de azok nem részei a sima Postgresnek.
2. **Ékezet-érzéketlen keresés `hungarian_stem`-mel kombinálva hivatalosan dokumentált, általános mintával megoldható** — nincs technikai akadálya, csak nincs kész, magyar-specifikus hivatalos példa.
3. **BM25-minőségű rangsorolás sima Postgresben csak külön bővítménnyel érhető el.** A `ts_rank`/`ts_rank_cd` dokumentáltan nem tartalmaz korpusz-szintű IDF-et. A Timescale `pg_textsearch` (PostgreSQL License, GA 2026.04, jelenlegi verzió v1.4.0/2026.08.18) az egyetlen azonosított, production-ready, engedékeny licencű BM25-bővítmény ebben a körben.
4. **Kód-szerű azonosítók (`PROJ-4412` mintázat) megbízhatóan törhetnek a `tsvector`-ban**: a betű+kötőjel+csak-számjegy minta a kötőjelet mínuszjelnek értelmezteti a parserrel, ami elrontja a számrész önálló kereshetőségét explicit workaround nélkül. Aláhúzásos azonosítók pedig szóhatárként törnek szét. Mindkettő dokumentált, régóta ismert, nem edge-case-számba menő viselkedés.
5. **A `pg_trgm` szükséges kiegészítő a rész-szó/elgépelés-tűrő kereséshez**, mivel a `tsvector` önmagában csak lexéma-egyezést tud.
6. **A hibrid (szöveges + vektoros) keresés RRF-mintája jól dokumentált és több független forrásból is elérhető** sima Postgres + `pgvector` kombinációra, tehát ez nem hiányzik a ParadeDB nélküli megoldásból — csak alkalmazás-oldali (SQL-függvény/kliens) implementációt igényel, nincs egy natív operátor mögé rejtve.
7. **A korábbi kör fő „független mérés” hivatkozása (vineeth.fyi) számszerűen pontosan idézett, de a „független” jelző maga megdőlt**: a szerző a mérés idején a ParadeDB egyik közvetlen versenytársának (Timescale/TigerData) alkalmazottja volt, ezt a cikk nem közli. Ez nem teszi hamissá a mért számokat, de az elfogulatlanság-minősítést átértékelendővé teszi minden olyan döntési anyagban, amely erre a forrásra hivatkozik.

---

# ELL06 — Mentés és migráció Postgres + ParadeDB alatt

**Módszer:** Kizárólag az Exa eszközzel (`mcp__Exa__web_search_exa`, `mcp__Exa__web_fetch_exa`) kerestem és olvastam — az Exa elérhető volt, nem kellett degradált módba váltani. A beépített WebSearch/WebFetch-et nem használtam. `curl`-t nem kellett bevetni. Alügynököket ez a futtatási környezet nem tudott indítani, ezért egyetlen, soros kutatóként dolgoztam (degradált mód a `deep-web-research` skill elvei szerint: elsődleges forrás, szó szerinti idézet, ellenőrzött hivatkozás).

## Verdikt-összefoglaló

| # | Állítás | Verdikt | Egy mondat |
|---|---|---|---|
| 1a | `pg_dump` konzisztens (snapshot-alapú) mentést ad, és nem blokkolja a többi felhasználót | **IGAZOLVA** | Szó szerint így írja a hivatalos Postgres-doksi két különböző oldalon (25.1 SQL Dump és a `pg_dump` referencia). |
| 1b | A logikai mentés csak a láthatatlan (törölt/dead) sorokat hagyja ki, azaz MVCC szerint csak az élő sorokat viszi | **RÉSZBEN** | A `pg_dump` doksi nem mondja ki szó szerint ezt a mondatot; ez a "konzisztens pillanatkép" + Postgres MVCC-láthatósági szabályok (forráskód-szintű) logikus, de nem explicit dokumentált következménye. |
| 2a | A legtöbb Postgres DDL tranzakciós (visszagörgethető), kivéve adatbázis/tablespace létrehozás-törlés | **IGAZOLVA** | Szó szerinti idézet a PostgreSQL wiki "Transactional DDL" oldaláról. |
| 2b | `CREATE INDEX CONCURRENTLY` nem futhat tranzakciós blokkban | **IGAZOLVA** | Szó szerinti idézet a hivatalos `CREATE INDEX` doksiból (5 verzión át azonos szöveg). |
| 2c | `CREATE DATABASE` nem futhat tranzakciós blokkban | **IGAZOLVA** | Szó szerinti, egysoros idézet a hivatalos `CREATE DATABASE` doksiból. |
| 2d | `ALTER TYPE … ADD VALUE` nem futhat tranzakciós blokkban régebbi verziókban | **RÉSZBEN / PONTOSÍTVA** | Csak PG ≤11-ig igaz szó szerint ("cannot run inside a transaction block"); PG12-től MÁR FUT tranzakcióban, csak az új érték nem használható a commit előtt (más hibaüzenet: "unsafe use of new value"). |
| 3 | A Drizzle Postgres-migrátora egy tranzakcióban futtatja az összes függő migrációt, hiba esetén minden visszagörgetődik ugyanabban a futásban | **IGAZOLVA** | Közvetlen forráskód-idézet: `PgDialect.migrate()` az összes függő migrációt egyetlen `session.transaction(async (tx) => {...})` hívásban futtatja. |
| 4a | Van hivatalos ParadeDB-workflow `pg_dump`/`pg_restore`-ra a ParadeDB-be történő adatmigrációhoz | **IGAZOLVA** | Hivatalos ParadeDB-doksi (`docs.paradedb.com/documentation/getting-started/load`) lépésről lépésre leírja. |
| 4b | A `pg_search`/ParadeDB-index a visszaállításkor újraépül, nem a fizikai index kerül mentésre | **RÉSZBEN** | Nincs erről *explicit* ParadeDB-nyilatkozat; a hivatalos Postgres `pg_dump` doksi szerint az indexek *definíciója* (DDL, "post-data" szakasz) kerül mentésre, nem a fizikai adat — ebből logikusan következik az újraépülés. Egy nem hivatalos (harmadik fél) útmutató ezt szó szerint ki is mondja. |
| 4c | Volt hiba/probléma a visszaállítással, a bővítmény hiányával vagy verzióeltéréssel kapcsolatban | **IGAZOLVA** | Több hivatalos GitHub-jegy/PR igazolja (extension-átnevezés miatti index-újraépítési kényszer; hiányos `ALTER EXTENSION UPDATE` migrációk; `pgvector` előfeltétel hiánya esetén explicit hibaüzenet). |
| 5a | `CREATE INDEX … USING paradedb`/`bm25 CONCURRENTLY` támogatott | **IGAZOLVA** | Hivatalos ParadeDB-doksi két oldalon (reindexing + legacy create-index) is dokumentálja, kóddal együtt. |
| 5b | A `CONCURRENTLY` nélküli (normál) `CREATE INDEX … USING paradedb` tranzakciós blokkban futtatható | **NEM ELDÖNTHETŐ (ParadeDB-specifikusan)** | Nincs olyan ParadeDB-forrás, ami ezt kifejezetten kimondaná vagy tiltaná; a ParadeDB doksi sehol nem dokumentál kivételt az általános Postgres-szabály (2b) alól, de ez csak közvetett következtetés, nem elsődleges forrásból igazolt tény. |
| 6a | Egy táblán csak egy ParadeDB-index létezhet | **IGAZOLVA** | Két független hivatalos hely (docs.paradedb.com és a GitHub-forrás) is szó szerint kimondja. |
| 6b | Ha a vektoroszlop NEM része a ParadeDB-indexnek, a pontos (index nélküli) `pgvector` `ORDER BY … <=>` keresés zavartalanul működik ugyanazon a táblán | **IGAZOLVA** | Hivatalos doksi szerint a ParadeDB-index csak akkor lép működésbe, ha a lekérdezésben ParadeDB-operátor (`@@@`, `\|\|\|`, `&&&`, `===`, `###`) szerepel — anélkül a lekérdezés a normál Postgres-tervezőn/`pgvector`-on megy át. |

---

## Állításonként

### 1. `pg_dump` konzisztencia és MVCC-láthatóság

**1a — konzisztens, nem blokkoló mentés.** A hivatalos Postgres 18 dokumentáció (25.1. SQL Dump fejezet) szó szerint:

> "Dumps created by pg_dump are internally consistent, meaning, the dump represents a snapshot of the database at the time pg_dump began running. pg_dump does not block other operations on the database while it is working. (Exceptions are those operations that need to operate with an exclusive lock, such as most forms of `ALTER TABLE`.)"
— https://www.postgresql.org/docs/current/backup-dump.html (megegyezik a PG16-os doksin is: https://www.postgresql.org/docs/16/backup-dump.html)

A `pg_dump` parancs-referencia oldala (második, független helyen ugyanazt állítja):

> "pg_dump is a utility for exporting a PostgreSQL database. It makes consistent exports even if the database is being used concurrently. pg_dump does not block other users accessing the database (readers or writers)."
— https://www.postgresql.org/docs/18/app-pgdump.html (PG15 doksi: "makes consistent backups… does not block other users" — https://www.postgresql.org/docs/15/app-pgdump.html)

**Verdikt 1a: IGAZOLVA**, két, egymástól független hivatalos doksioldallal alátámasztva.

**1b — csak a látható (élő) sorokat viszi MVCC szerint.** Ezt a `pg_dump` doksi *nem* mondja ki szó szerint ilyen formában. A mechanizmus viszont dokumentált máshol:

- A `pg_dump` egy tranzakción belül fut (lásd fent: "represents a snapshot… at the time pg_dump began running"), a snapshot pedig a Postgres MVCC-mechanizmusának tárgya.
- A hivatalos Postgres-forráskód (`heapam_visibility.c`, `HeapTupleSatisfiesMVCC`) explicit módon úgy dönt egy sorverzió láthatóságáról, hogy megnézi az `xmin`/`xmax` tranzakció-azonosítókat a snapshothoz képest; egy törölt (és a snapshot indítása előtt committált törlésű) sor `xmax`-a miatt láthatatlan lesz:

> "HeapTupleSatisfiesMVCC — True iff heap tuple is valid for the given MVCC snapshot."
— https://github.com/postgres/postgres/blob/e18b0cb7/src/backend/access/heap/heapam_visibility.c

- Ezt támasztja alá a 24.1. Routine Vacuuming fejezet is, amely kimondja, hogy egy `UPDATE`/`DELETE` nem törli azonnal a régi sorverziót, az csak a hivatkozó snapshotok eltűnése (pl. `VACUUM`) után szabadul fel — vagyis a *fizikai* fájlban/WAL-ban megmaradhat, miközben egy új snapshot (mint a `pg_dump` snapshotja) már nem látja:

> "In PostgreSQL, an UPDATE or DELETE of a row does not immediately remove the old version of the row. This approach is necessary to gain the benefits of multiversion concurrency control (MVCC, see Chapter 13): the row version must not be deleted while it is still potentially visible to other transactions."
— https://www.postgresql.org/docs/19/routine-vacuuming.html

**Verdikt 1b: RÉSZBEN.** A jelenség (pg_dump csak élő sorokat exportál) technikailag helyes és két különböző hivatalos forrásból (MVCC forráskód + vacuum-fejezet) levezethető, de nincs egyetlen hivatalos doksi-mondat sem, ami *szó szerint* kimondaná "a pg_dump csak a látható sorokat exportálja".

---

### 2. Tranzakciós DDL a Postgresben

**2a — a PostgreSQL wiki állítása.** A "Transactional DDL in PostgreSQL: A Competitive Analysis" wiki-oldal szó szerint:

> "Like several of its commercial competitors, one of the more advanced features of PostgreSQL is its ability to perform transactional DDL via its Write-Ahead Log design. This design supports backing out even large changes to DDL, such as table creation. You can't recover from an add/drop on a database or tablespace, but all other catalog operations are reversible."
— https://wiki.postgresql.org/wiki/Transactional_DDL_in_PostgreSQL:_A_Competitive_Analysis

Ugyanezt mondja a "Why PostgreSQL Instead of MySQL" wiki-oldal is, más szavakkal, függetlenül:

> "In PostgreSQL, when you are inside a transaction almost any operation can be undone. There are some irreversible operations (like creating or destroying a database or tablespace), but normal table modifications can be backed out by issuing a ROLLBACK via its Write-Ahead Log design."
— https://wiki.postgresql.org/wiki/Why_PostgreSQL_Instead_of_MySQL_2009

**Verdikt 2a: IGAZOLVA**, két független PostgreSQL wiki-oldallal.

**2b — `CREATE INDEX CONCURRENTLY` nem futhat tranzakcióban.** A hivatalos `CREATE INDEX` doksi (azonos szöveggel PG15, 17, 18, 19-en is):

> "Regular index builds permit other regular index builds on the same table to occur simultaneously, but only one concurrent index build can occur on a table at a time. In either case, schema modification of the table is not allowed while the index is being built. Another difference is that a regular `CREATE INDEX` command can be performed within a transaction block, but `CREATE INDEX CONCURRENTLY` cannot."
— https://www.postgresql.org/docs/current/sql-createindex.html

Ezt gyakorlati hibaként is megerősíti egy közösségi jegy (Marten projekt), amely idézi is a fenti doksit, és bemutatja a valós hibaüzenetet éles tranzakciós migrációs szkriptben:

> „`DROP INDEX CONCURRENTLY cannot be executed from a function or multi-command string`" — és a felhasználó rámutat: „a regular CREATE INDEX command can be performed within a transaction block, but CREATE INDEX CONCURRENTLY cannot."
— https://github.com/JasperFx/marten/issues/1042

**Verdikt 2b: IGAZOLVA.**

**2c — `CREATE DATABASE` nem futhat tranzakcióban.** Hivatalos doksi, azonos szöveggel PG17/18/19-en:

> "`CREATE DATABASE` cannot be executed inside a transaction block."
— https://www.postgresql.org/docs/current/sql-createdatabase.html

**Verdikt 2c: IGAZOLVA.**

**2d — `ALTER TYPE … ADD VALUE`, verziófüggő.** A hivatalos PostgreSQL Git-repó commitja (amely magát a dokumentáció-szöveget diffeli) mutatja a pontos váltást:

> Régi (≤PG11) szöveg: "`ALTER TYPE ... ADD VALUE` (the form that adds a new value to an enum type) cannot be executed inside a transaction block."
> Új (PG12+) szöveg: "If `ALTER TYPE ... ADD VALUE` (the form that adds a new value to an enum type) is executed inside a transaction block, the new value cannot be used until after the transaction has been committed, except in the case that the enum type itself was created earlier in the same transaction."
— https://git.postgresql.org/pg/commitdiff/15bc038f9bcd1a9af3f625caffafc7c20322202d

Ezt egy Stack Overflow-válasz is megerősíti, közvetlenül a Postgres-forráskód kommentjét idézve:

> "Note that this restriction has been removed in commit 212fab99… So you might want to upgrade to PostgreSQL v12 some time soon."
— https://stackoverflow.com/questions/53149484/error-alter-type-add-cannot-run-inside-a-transaction-block

**Verdikt 2d: RÉSZBEN / PONTOSÍTVA.** Az eredeti állítás ("régebbi verziókban NEM futhat tranzakcióban") igaz PG≤11-re, de PG12 óta *fut* tranzakcióban — csak az újonnan hozzáadott érték nem használható fel a commit előtt ugyanabban a tranzakcióban, más hibaüzenettel ("unsafe use of new value…").

---

### 3. A Drizzle ORM Postgres-migrátora

A `drizzle-orm` forráskódjában (`drizzle-orm/src/pg-core/dialect.ts`, `PgDialect.migrate`) az összes még le nem futtatott migráció egyetlen `session.transaction(...)` hívás belsejében fut:

```ts
await session.transaction(async (tx) => {
    for await (const migration of migrations) {
        if (
            !lastDbMigration
            || Number(lastDbMigration.created_at) < migration.folderMillis
        ) {
            for (const stmt of migration.sql) {
                await tx.execute(sql.raw(stmt));
            }
            await tx.execute(
                sql`insert into ... values(${migration.hash}, ${migration.folderMillis})`,
            );
        }
    }
});
```
— https://github.com/drizzle-team/drizzle-orm/blob/6276f5c9a94b1bb6d109b990982243d2b13e5f88/drizzle-orm/src/pg-core/dialect.ts

A konkrét driver-migrátorok (`node-postgres`, `postgres-js`) mind ugyanezt a `dialect.migrate(...)` metódust hívják meg:

> "export async function migrate(db, config) { const migrations = readMigrationFiles(config); await db.dialect.migrate(migrations, db.session, config); }"
— https://github.com/drizzle-team/drizzle-orm/blob/48e54060/drizzle-orm/src/node-postgres/migrator.ts és https://github.com/drizzle-team/drizzle-orm/blob/48e54060/drizzle-orm/src/postgres-js/migrator.ts

**Megjegyzés a rollback-viselkedésről:** a forráskód maga nem tartalmaz explicit `try/catch`+`ROLLBACK`-ot a `migrate()` függvényben — ez a `session.transaction()` wrapper (driverenként a `node-postgres`/`postgres-js` session implementációja) felelőssége, amely a szokásos JS async/await mintát követi: ha bármelyik `tx.execute()` hibát dob, a `session.transaction` Promise-a elutasítódik, és a wrapper (dokumentáltan minden Drizzle Postgres-session implementációban) ilyenkor `ROLLBACK`-et ad ki a mögöttes Postgres-tranzakción. Ezt a viselkedést közvetlenül a `session.transaction` implementációjának forráskódjában (nem csak a `dialect.ts`-ben) lehetne tovább igazolni, de a `dialect.migrate` kódja önmagában egyértelműen igazolja, hogy **az összes függő migráció egyetlen tranzakcióban fut**, és a Drizzle Postgres-fejlesztésre a projekt maga sehol nem dokumentál "commit statement-enként" viselkedést a migrátorra.

**Verdikt 3: IGAZOLVA** a "minden függő migráció egy tranzakcióban fut" részre (közvetlen forráskód-idézet), és a rollback-viselkedés a JS Promise-elutasítás + a Drizzle session-wrapperek szokásos `try{BEGIN…COMMIT}catch{ROLLBACK}` mintája alapján logikusan következik, bár ezt maga a `dialect.ts` fájl nem mondja ki explicit kommentben.

---

### 4. ParadeDB + `pg_dump`/`pg_restore`

**4a — hivatalos workflow.** A ParadeDB hivatalos "Load Data from Postgres" oldala:

> "The easiest way to copy data from another Postgres into ParadeDB is with the `pg_dump` and `pg_restore` utilities… Below, we use the 'custom' format (`-Fc`) for both `pg_dump` and `pg_restore`."
> ```
> pg_dump -Fc --no-acl --no-owner -h <host> -U <username> <dbname> > old_db.dump
> pg_restore --verbose --clean --no-acl --no-owner -h <host> -U <username> -d <dbname> -Fc old_db.dump
> ```
— https://docs.paradedb.com/documentation/getting-started/load

**Verdikt 4a: IGAZOLVA.**

**4b — az index újraépül-e visszaállításkor.** Erről *nincs* explicit kijelentés a ParadeDB hivatalos doksiban. Amit találtam:

- A hivatalos Postgres `pg_dump` referencia szerint az indexek *definíciója* (DDL) kerül mentésre, nem a fizikai index-adat:
> "Post-data items include definitions of indexes, triggers, rules, statistics for indexes, and constraints other than validated check and not-null constraints."
— https://www.postgresql.org/docs/current/app-pgdump.html

Ez a mechanizmus (index DDL `CREATE INDEX`-ként megy a dumpba, majd a restore újra lefuttatja) a Postgres-ben *access method-független* — vagyis logikusan a `USING paradedb`/`bm25` indexre is vonatkozik, hiszen a ParadeDB egy sima Postgres index access method-ot regisztrál.

- Egy nem hivatalos (harmadik fél) telepítési útmutató ezt szó szerint ki is mondja:
> "BM25 indexes are NOT included in `pg_dump`; they're rebuilt on restore. For large datasets use pgBackRest for physical backups (index files included, faster restore)."
— https://ramnode.com/guides/paradedb (NEM ParadeDB hivatalos forrás — harmadik féltől származó telepítési útmutató)

**Verdikt 4b: RÉSZBEN.** A mechanizmus (index DDL-ként mentve, restore-kor újraépítve) logikailag alátámasztott az általános Postgres `pg_dump` szemantikából, és egy nem hivatalos forrás explicit is kimondja, de **ParadeDB saját, hivatalos dokumentációja ezt sehol nem mondja ki közvetlenül** — a hivatalos ParadeDB-doksi csak azt írja le, *hogyan* kell `pg_dump`/`pg_restore`-t használni, az index-viselkedésről nem nyilatkozik.

**4c — hiba a visszaállítás/verzió/bővítmény körül.** Több hivatalos ParadeDB GitHub-jegy igazolja, hogy voltak ilyen problémák:

- Extension-átnevezés miatti kompatibilitási törés (`pg_bm25` → `pg_search`), amely az indexek teljes újralétrehozását igényelte:
> "Hey @34code, this is because we renamed the extension from `pg_bm25` to `pg_search` in `v0.6.0`… This means you will need to uninstall pg_bm25 and install pg_search, and recreate your indexes."
— https://github.com/paradedb/paradedb/issues/1076

- Hiányos `ALTER EXTENSION UPDATE` migrációk (verzióváltáskor a séma nem lett teljes, csak teljes `DROP`+`CREATE EXTENSION` oldotta meg):
> "A user upgrading prod from `0.23.1` → `0.24.0` via `ALTER EXTENSION pg_search UPDATE;` reported that `verify_index` was missing from the schema, and only a full `DROP EXTENSION` + `CREATE EXTENSION` fixed it… | Fresh CREATE EXTENSION | ✅ | | DROP + CREATE (workaround) | ✅ | | ALTER EXTENSION UPDATE from ≥0.21.5 | ❌ |"
— https://github.com/paradedb/paradedb/pull/5310

- Bővítmény-előfeltétel hiánya explicit hibaüzenettel (0.25.0 óta `pgvector` szükséges a `pg_search`-höz):
> "Without `CASCADE`, `CREATE EXTENSION pg_search` fails with `required extension \"vector\" is not installed`."
— https://api.pgxn.org/src/pg_search/pg_search-0.25.6/docs/deploy/self-hosted/extension.mdx

- Fizikai tantivy-fájlok elhelyezési hibája (két adatbázis ugyanazt az OID-t kaphatta, ami index-ütközéshez/hibás betöltéshez vezetett):
> "`pg_search` stores the tantivy index to `$PGDATA/pg_search/${index_oid}/`. This is not unique enough as two databases in the same cluster could end up with the same OID… ERROR: error loading index from directory: could not read from file to load index…"
— https://github.com/paradedb/paradedb/issues/1579

**Verdikt 4c: IGAZOLVA**, négy, egymástól független hivatalos ParadeDB GitHub-forrással.

---

### 5. ParadeDB index tranzakcióban / `CONCURRENTLY`

**5a — `CONCURRENTLY` támogatott.** Két hivatalos ParadeDB doksi-oldal is:

> "First, use `CREATE INDEX CONCURRENTLY` to build a new index in the background… The `CONCURRENTLY` clause is required. `CONCURRENTLY` allows the existing index to continue serving queries while the new index is being built."
— https://docs.paradedb.com/documentation/indexing/reindexing

> "To create a new index without blocking writes to your table, use the `CONCURRENTLY` keyword: `CREATE INDEX CONCURRENTLY search_idx_v2 ON mock_items USING bm25 (…) WITH (key_field='id');`"
— https://docs.paradedb.com/legacy/indexing/create-index

A `0.13.0` changelog is megerősíti, hogy ez a `CREATE INDEX` szintaxisra állás (a régi `paradedb.create_bm25()` helyett) egyik konkrét hozadéka volt:

> "`CREATE INDEX` conforms with PostgreSQL dialect and unlocks several new features: - Support for `CREATE INDEX CONCURRENTLY` - Support for indexing partitioned tables"
— https://paradedb-dev.mintlify.app/changelog/0.13.0

**Verdikt 5a: IGAZOLVA**, három független hivatalos ParadeDB forrással.

**5b — sima (nem `CONCURRENTLY`) `CREATE INDEX` tranzakcióban.** Ezt a ParadeDB doksi **sehol nem mondja ki explicit módon** — sem megerősítve, sem tiltva. Amit találtam, közvetett jelek:

- A ParadeDB `CREATE INDEX` munkát a háttérben egy külön "bgwriter" (background writer) folyamatra mozgatták (`PR #1413`), ami az indexépítés *belső* implementációs részlete, de nem befolyásolja azt, hogy a kliens által kiadott `CREATE INDEX` SQL-utasítás maga hogyan viselkedik tranzakció-blokk szempontjából (ez Postgres-szinten dől el, ahogy a 2b pontban igazoltuk).
- Nem találtam olyan GitHub-jegyet, amely arról szólna, hogy egy sima (nem concurrent) `USING paradedb`/`bm25` `CREATE INDEX` BEGIN…COMMIT között hibát dobna.
- Egy általános (nem ParadeDB-specifikus) Stack Overflow-válasz megerősíti az alap-Postgres szabályt bármely index access method-ra: "Yes, you can create an index inside a transaction (unless you are using CONCURRENTLY)." — https://stackoverflow.com/questions/76323576/create-and-use-an-index-inside-a-transaction

**Verdikt 5b: NEM ELDÖNTHETŐ (ParadeDB-specifikus elsődleges forrásból).** Az általános Postgres-szabály (2b) alapján valószínűsíthető, hogy igen, de erre nincs ParadeDB-specifikus hivatalos megerősítés vagy cáfolat.

---

### 6. ParadeDB-index + pontos `pgvector`-keresés ugyanazon a táblán

**6a — csak egy ParadeDB-index/tábla.** Két, egymástól technikailag független hivatalos hely (a renderelt doksi-oldal és a GitHub nyers `.mdx` forrás) ugyanazt mondja:

> "Only one ParadeDB index can exist per table. We recommend indexing all columns in a table that may be present in a search query, including columns used for sorting, grouping, filtering, and aggregations."
— https://docs.paradedb.com/documentation/indexing/create-index.md és https://github.com/paradedb/paradedb/blob/v0.25.2/docs/documentation/indexing/create-index.mdx

Ez a szabály nem új: a `v0.10.0` release notes (2024) is dokumentálja a bevezetését:

> "### One Index per Table — Until now, `pg_search` has allowed creating multiple BM25 indexes on a table. However, when searching it wasn't always guaranteed the specified index would actually be used. As of v0.10.0, only one BM25 index can be created per table."
— https://github.com/paradedb/paradedb/releases/tag/v0.10.0

**Verdikt 6a: IGAZOLVA.**

**6b — a vektoroszlopra vonatkozó pontos keresés zavartalansága, ha az nincs az indexben.** A hivatalos "Filtering" doksi kimondja az aktiválási feltételt:

> "In order for the ParadeDB index to be used, at least one ParadeDB operator must be present in the query. Any of the following search operators qualify: `@@@`, `\|\|\|`, `&&&`, `===`, `###`… For queries that do not require text search, add `pdb.all` to force the ParadeDB index without changing the query output."
— https://docs.paradedb.com/documentation/filtering

Ez azt jelenti, hogy egy sima `SELECT … ORDER BY embedding <=> $1 LIMIT k` lekérdezés — amely nem tartalmaz ParadeDB-operátort — **nem** hívja meg a ParadeDB egyedi index-scant, tehát a Postgres normál tervezője (és a `pgvector` normál, index nélküli szekvenciális-scan alapú pontos távolságszámítása) fut le, függetlenül attól, hogy a vektoroszlop szerepel-e a ParadeDB-indexben vagy sem.

Ezt közvetve megerősíti a vektor-indexelési doksi is, amely leszögezi, hogy a ParadeDB *nem* a `pgvector` saját HNSW/IVF indexeit használja, hanem egy különálló SPANN-stílusú struktúrát:

> "Make sure the pgvector extension is installed first. ParadeDB uses pgvector's `vector` type, but not its HNSW or IVF indexes."
— https://github.com/paradedb/paradedb/blob/v0.25.2/docs/documentation/indexing/indexing-vectors.mdx

— vagyis a `pgvector` saját (akár indexelt, akár index nélküli) útja a ParadeDB-indextől teljesen független alrendszer marad.

**Verdikt 6b: IGAZOLVA**, két hivatalos ParadeDB doksi-oldallal.

---

## Amit ez a döntésre jelent

1. A `pg_dump` konzisztencia- és nem-blokkoló-viselkedés hivatalosan dokumentált, szó szerint idézhető tény — erre biztonságosan lehet hivatkozni. Az "csak élő sorokat exportál" állítás technikailag igaz és két különböző hivatalos forrásból (MVCC-forráskód, vacuum-fejezet) levezethető, de nincs rá egyetlen kerek, hivatalos mondat; ha ez kritikus pont egy döntésben, érdemes jelezni, hogy ez levezetett, nem szó szerint dokumentált tény.
2. A tranzakciós DDL-korlátok (`CREATE INDEX CONCURRENTLY`, `CREATE DATABASE`) egyértelműen és stabilan dokumentáltak több Postgres-verzión át. Az `ALTER TYPE … ADD VALUE` esetében az eredeti kutatási kör állítása ("régebbi verziókban nem futhat tranzakcióban") **pontosításra szorul**: PG12 óta *fut* tranzakcióban, csak más hibát dob, ha ugyanabban a tranzakcióban használni is próbálják az új értéket — ez migrációtervezés szempontjából releváns különbség (a hiba oka és elkerülési módja más PG12+ alatt, mint PG11-en).
3. A Drizzle Postgres-migrátor "minden függő migráció egy tranzakcióban" viselkedése forráskód-szinten igazolt, közvetlenül a hivatalos `drizzle-orm` repóból. A hiba esetén bekövetkező teljes rollback a kódmintából (egyetlen `session.transaction` hívás) logikusan következik, de ezt a `dialect.ts` fájl nem mondja ki kommentben — ha ez kritikus, érdemes lenne a driver-specifikus `session.transaction()` implementációt (pl. `node-postgres/session.ts`) is közvetlenül megnézni.
4. A ParadeDB hivatalos `pg_dump`/`pg_restore`-workflow létezik és dokumentált, de **a ParadeDB saját dokumentációja nem nyilatkozik közvetlenül arról, hogy a keresési index visszaállításkor újraépül** — ez csak a Postgres általános `pg_dump` szemantikájából (index = DDL, nem fizikai adat) és egy harmadik féltől származó útmutatóból vezethető le. Ismert, dokumentált hibaosztályok viszont vannak: extension-átnevezés/verzióváltás miatti inkompatibilitás, hiányos `ALTER EXTENSION UPDATE` migrációk, és hiányzó előfeltétel-bővítmény (`pgvector`) esetén explicit hibaüzenet.
5. A `CREATE INDEX … USING paradedb/bm25 CONCURRENTLY` támogatása egyértelműen dokumentált. A nem-concurrent változat tranzakción belüli futtathatósága viszont **nincs ParadeDB-specifikusan dokumentálva** — csak az általános Postgres-szabályból következtethető ki, konkrét ParadeDB-forrás vagy -ellenpélda nélkül.
6. Az "egy tábla = egy ParadeDB-index" szabály és a ParadeDB-operátor-aktiválási mechanizmus egyaránt jól dokumentált, és együtt egyértelműen alátámasztják, hogy egy nem-indexelt vektoroszlopon végzett sima (operátor nélküli) `pgvector`-keresés a ParadeDB-indextől függetlenül, zavartalanul működik ugyanazon a táblán.

---

---

# ELL07 — Adatlap-ellenőrzőösszeg (data checksums) Postgresben és a ParadeDB képein

*Keresőeszköz: kizárólag Exa (`mcp__Exa__web_search_exa`, `mcp__Exa__web_fetch_exa`) — a beépített WebSearch/WebFetch nem került használatra. Az Exa elérhető volt, nem kellett degradált módba váltani.*

## Verdikt-összefoglaló

| # | Állítás | Verdikt | Egy mondat |
|---|---|---|---|
| 1 | A PostgreSQL 18 az `initdb`-ben alapból bekapcsolja az adatlap-ellenőrzőösszeget | **IGAZOLVA** | A hivatalos PG18 kiadási jegyzék és az `initdb` doksi is kimondja: PG18-tól `-k/--data-checksums` az alapértelmezés, PG15–17-ben ez explicit `-k` kapcsolót igényelt (nem volt alapértelmezett). |
| 2a | `pg_checksums --enable` csak leállított fürtön futtatható | **IGAZOLVA** | A hivatalos doksi és a forráskód is kimondja: „The server must be shut down cleanly before running pg_checksums", a forrás `pg_fatal("cluster must be shut down")`-ot dob futó fürtön. |
| 2b | A doksi mond valamit az időtartamról | **IGAZOLVA (minőségi, nem számszerű)** | A doksi csak annyit mond: „Enabling checksums in a large cluster can potentially take a long time" — konkrét szám/becslés nincs. |
| 3 | Van hivatalos állítás a teljesítményköltségről, szó szerint „may incur a noticeable performance penalty" | **RÉSZBEN / PONTOSÍTVA** | PG15–17 `initdb` doksija pontosan ezt a mondatot tartalmazza, de a PG18 (jelenlegi stabil) doksi már finomított szöveget használ: „might incur a **small** performance penalty" — a szó szerinti „noticeable" kifejezés a PG18-as/jelenlegi dokumentációból már eltűnt. |
| 4a | A ParadeDB hivatalos `paradedb/paradedb` Docker képe pg15–pg18 címkéket kínál | **IGAZOLVA** | A Docker Hub cimke-lista `pg15`, `pg16`, `pg17`, `pg18` (és verziózott változataik) címkéket listáz; a ParadeDB doksi explicit kimondja: „Docker images are available for Postgres 15+", és a `latest` alapból PG18-at használ. |
| 4b | Az image a hivatalos `postgres` image-re épül, így megy a `POSTGRES_INITDB_ARGS` | **RÉSZBEN (architektúrából levezetve, nem külön dokumentálva)** | A GitHub Dockerfile (`docker/Dockerfile.paradedb-18`) bizonyítottan `FROM postgres:18-trixie`, és a fájl explicit megjegyzése szerint a ParadeDB szándékosan **nem** írja felül a hivatalos image `entrypoint.sh`-ját — ez architekturálisan alátámasztja, hogy a hivatalos `postgres` image `POSTGRES_INITDB_ARGS` mechanizmusa működne, de a ParadeDB saját doksija ezt a konkrét környezeti változót nem említi és nem tesztelte/dokumentálta explicit. |
| 5 | A `pg_search` v0.25.x támogatja a PostgreSQL 18-at | **IGAZOLVA** | A hivatalos `pg_search` README (v0.25.2 tag) kimondja: „currently 15–18"; ezt független forrásként a Docker Hub is megerősíti `0.25.6-pg18` / `v0.25.6-pg18` címkékkel. |
| 6a | A `pg_amcheck` csak heap-et és B-tree indexet ellenőriz, más relációtípusokat nem | **IGAZOLVA** | Hivatalos doksi szó szerint: „Only ordinary and toast table relations, materialized views, sequences, and btree indexes are currently supported. Other relation types are silently skipped." |
| 6b | A ParadeDB `pdb.verify_index` külön, saját eszköz a BM25 indexekhez, mert a `pg_amcheck` nem fedi le őket | **IGAZOLVA** | A ParadeDB hivatalos doksija saját, „amcheck-style" függvényt ír le kifejezetten a BM25 indexekhez (séma-érvényesség, olvashatóság, szegmens-checksumok, metaadat-konzisztencia, opcionális `heapallindexed` heap-referencia ellenőrzés). |

## Állításonként

### 1. PostgreSQL 18 — alapból bekapcsolt data checksums

**PG18.0 hivatalos kiadási jegyzék** (postgresql.org/docs/release/18.0/):
> "Change initdb default to enable data checksums (Greg Sabino Mullane) […] Checksums can be disabled with the new initdb option `--no-data-checksums`. pg_upgrade requires matching cluster checksum settings, so this new option can be useful to upgrade non-checksum old clusters."
URL: https://www.postgresql.org/docs/release/18.0/

**PG18 hivatalos `initdb` doksi** (aktuális, „current" = PG18):
> "-k --data-checksums# Use checksums on data pages to help detect corruption by the I/O system that would otherwise be silent. **This is enabled by default; use --no-data-checksums to disable checksums.** Enabling checksums might incur a small performance penalty."
URL: https://www.postgresql.org/docs/18/app-initdb.html (azonos szöveg: https://www.postgresql.org/docs/current/app-initdb.html)

**„PostgreSQL 18 Released!" hivatalos hír:**
> "Databases initialized with PostgreSQL 18 `initdb` now have page checksums enabled by default. This can affect upgrades from non-checksum enabled clusters, which would require you to create a new PostgreSQL 18 cluster with the `--no-data-checksums` option when using `pg_upgrade`."
URL: https://www.postgresql.org/about/news/postgresql-18-released-3142/

**PG17 (és PG16, PG15) `initdb` doksi — nincs „enabled by default" kitétel, nincs `--no-data-checksums` opció:**
> PG17: "-k --data-checksums# Use checksums on data pages to help detect corruption by the I/O system that would otherwise be silent. Enabling checksums may incur a noticeable performance penalty. If set, checksums are calculated for all objects, in all databases."
URL: https://www.postgresql.org/docs/17/app-initdb.html

> PG16: "-k --data-checksums# Use checksums on data pages to help detect corruption by the I/O system that would otherwise be silent. Enabling checksums may incur a noticeable performance penalty. If set, checksums are calculated for all objects, in all databases. All checksum failures will be reported in the pg_stat_database view. See Section 30.2 for details."
URL: https://www.postgresql.org/docs/16/app-initdb.html

A PG16/17 szövegben nincs „enabled by default" mondat és nincs `--no-data-checksums` ellenpár-opció sem (ez csak PG18-tól létezik) — ez maga is bizonyíték arra, hogy PG15–17-ben a checksum **kikapcsolt** alapállapot volt, explicit `-k` kapcsolót igényelt.

**Verdikt: IGAZOLVA.** PostgreSQL 18-tól (2025-09-25, stabil kiadás) az `initdb` alapból bekapcsolja a data checksumot; PG15/16/17 alapértéke kikapcsolt volt.

### 2. Utólagos bekapcsolás — `pg_checksums --enable`

**Hivatalos `pg_checksums` doksi (PG18, azonos szöveg PG "current"-en is):**
> "pg_checksums checks, enables or disables data checksums in a PostgreSQL cluster. **The server must be shut down cleanly before running pg_checksums.** […] -e --enable: Enables checksums. […] **Enabling checksums in a large cluster can potentially take a long time.** During this operation, the cluster or other programs that write to the data directory must not be started or else data loss may occur."
URL: https://www.postgresql.org/docs/18/app-pgchecksums.html (és https://www.postgresql.org/docs/current/app-pgchecksums.html)

**PostgreSQL forráskód (`pg_checksums.c`), a leállítási kényszer implementációja:**
> "/* Check if cluster is running. A clean shutdown is required to avoid random checksum failures caused […] guard against someone starting the cluster concurrently. */ if (ControlFile->state != DB_SHUTDOWNED && ControlFile->state != DB_SHUTDOWNED_IN_RECOVERY) pg_fatal("cluster must be shut down");"
URL: https://doxygen.postgresql.org/pg__checksums_8c_source.html

**Megjegyzés a jövőre nézve (PostgreSQL 19, fejlesztői ág, MÉG NEM stabil kiadás):** a `devel`/19-es doksi már egy „Online Enabling of Checksums" funkcióról beszél, amely futó fürtön is engedélyezné a checksumot — ez PG15–18-on (a ParadeDB által jelenleg támogatott verziókon) **nem** elérhető, csak a leállított-fürtös `pg_checksums --enable` út.
URL: https://www.postgresql.org/docs/19/checksums.html, https://www.postgresql.org/docs/devel/checksums.html

**Verdikt: IGAZOLVA.** Offline (leállított fürtön) művelet; a doksi konkrét időtartamot **nem** ad meg, csak annyit mond, hogy nagy fürtön sokáig tarthat.

### 3. Teljesítményköltség — szó szerinti idézet és verziófüggés

**PG15/16/17 `initdb` doksi (szó szerint):**
> "Enabling checksums **may incur a noticeable performance penalty**."
URL: https://www.postgresql.org/docs/17/app-initdb.html, https://www.postgresql.org/docs/16/app-initdb.html

**PG18 (jelenlegi stabil) `initdb` doksi — a szöveg megváltozott:**
> "Enabling checksums **might incur a small performance penalty**."
URL: https://www.postgresql.org/docs/18/app-initdb.html

A kettő nem ugyanaz a mondat: a „noticeable" (észrevehető) jelző PG15–17-ben szerepelt, PG18-ban „small"-ra (kicsi) finomodott — ez összhangban van azzal a fejlesztői listás vitával is, ahol a konszenzus a checksum overhead alacsony voltáról szólt:
> "I think the last time we discussed this the consensus was that computational overhead of computing the checksums is pretty small for most systems […] turning on wal_compression also turns on wal_log_hints, which can increase WAL by quite a lot."
URL: https://www.postgresql.org/message-id/20210107211433.GS27507%40tamriel.snowman.net (hivatalos pgsql-hackers levelezőlista)

**Verdikt: RÉSZBEN / PONTOSÍTVA.** A pontosan idézett „may incur a noticeable performance penalty" mondat valóban létezik/létezett a hivatalos doksiban, de csak a PG15–17-es (és korábbi) `initdb` oldalakon; a jelenlegi (PG18) hivatalos doksi már „small performance penalty"-t ír, tehát a mai éles dokumentációból ez a konkrét jelző ("noticeable") már nem idézhető.

### 4. ParadeDB hivatalos Docker-képe

**Docker Hub címke-lista (`paradedb/paradedb`):** a tag-lista tartalmaz `pg15`, `pg16`, `pg17`, `pg18`, valamint verziózott (`latest-pg15…pg18`, `0.25.6-pg15…pg18`, `v0.25.6-pg15…pg18` stb.) változatokat.
URL: https://hub.docker.com/r/paradedb/paradedb/tags

**ParadeDB hivatalos Docker doksi — alapértelmezett verzió:**
> "```bash\ndocker run … paradedb/paradedb:latest\n```\n…\nThe `paradedb/paradedb:latest` tag uses Postgres 18. Docker images are available for Postgres 15+. To specify a different Postgres version, please refer to the available tags on Docker Hub."
URL: https://docs.paradedb.com/deploy/self-hosted/docker

**Alapja: hivatalos `postgres` image, PR bizonyítékkal az áttérésről (Bitnami → hivatalos postgres):**
> "This PR switches us away from the Bitnami Dockerfile to the Postgres Dockerfile. […] realized that our Docker image should just be Postgres and our production deployments will be via CloudNativePG. This requires using the Postgres image."
URL: https://github.com/paradedb/paradedb/pull/1436

**Jelenlegi (main ág) Dockerfile — `Dockerfile.paradedb-18`, szó szerint:**
> "# Note: Debian Trixie = Debian 13\nFROM postgres:18-trixie AS paradedb\n…\n# Copy ParadeDB bootstrap script to install extensions and configure postgresql.conf\nCOPY ./bootstrap.sh /docker-entrypoint-initdb.d/10_bootstrap_paradedb.sh\n\n# The upstream `postgres` Docker image comes with its own `entrypoint.sh` script which\n# starts as `root` and then switches to the `postgres` user after running chown and chmod\n# on the PostgreSQL data directory. To maintain compatibility with the upstream image and\n# ensure that the `postgres` user has the correct permissions on the data directory, we let\n# the upstream `entrypoint.sh` script run as the entrypoint and don't specify a custom user."
URL: https://raw.githubusercontent.com/paradedb/paradedb/main/docker/Dockerfile.paradedb-18 (forrás: https://github.com/paradedb/paradedb/blob/main/docker/Dockerfile.paradedb-18)

**Hivatalos `postgres` Docker image doksi — `POSTGRES_INITDB_ARGS`:**
> "This optional environment variable can be used to send arguments to `postgres initdb`. The value is a space separated string of arguments as `postgres initdb` would expect them. This is useful for adding functionality like data page checksums: `-e POSTGRES_INITDB_ARGS="--data-checksums"`."
URL: https://hub.docker.com/_/postgres (azonos szöveg: https://github.com/docker-library/docs/blob/master/postgres/README.md)

**Verdikt: RÉSZBEN.** A tag-lefedettség (pg15–pg18) és az alapértelmezett verzió (PG18) hivatalosan dokumentált és megerősített. Az, hogy a ParadeDB image ténylegesen a hivatalos `postgres` image-re épül és nem írja felül annak entrypoint-ját, a Dockerfile forráskódjából (elsődleges forrás) közvetlenül igazolható — ez architekturálisan alátámasztja, hogy a `POSTGRES_INITDB_ARGS` (pl. `--data-checksums`) működne rajta. Azonban a ParadeDB saját dokumentációja ezt a konkrét környezeti változót **nem említi és nem dokumentálja** explicit módon (a Docker doksi oldaluk csak `POSTGRES_USER`/`POSTGRES_PASSWORD`/`POSTGRES_DB`-t sorol fel) — ez a rész tehát levezetett, nem közvetlenül kimondott állítás.

### 5. `pg_search` v0.25.x — PostgreSQL 18 támogatás

**Hivatalos `pg_search` README (v0.25.2 tag, GitHub):**
> "`pg_search` is supported on official PostgreSQL Global Development Group Postgres versions, starting at PostgreSQL 15. […] `cargo pgrx init` builds every supported Postgres version this project targets (**currently 15–18**) into `~/.pgrx/…/pgrx-install/`…"
URL: https://github.com/paradedb/paradedb/blob/v0.25.2/pg_search/README.md

**Független megerősítés — Docker Hub címkék konkrét 0.25.x verzióval PG18-hoz:**
> Tag-lista tartalmazza: `0.25.6-pg18`, `v0.25.6-pg18` (és korábban `0.24.1-pg18`, `latest-pg18`).
URL: https://hub.docker.com/r/paradedb/paradedb/tags

**Harmadik megerősítés — self-hosted extension telepítési doksi (pg_search 0.25.6/0.25.8/0.25.9 tükrözött doksi), amely PG18-hoz konkrét `.deb`/`.rpm` csomagot ad:**
> "curl -L "https://github.com/paradedb/paradedb/releases/download/v{version}/postgresql-18-pg-search_{version}-1PARADEDB-noble_amd64.deb" …"
URL: https://api.pgxn.org/src/pg_search/pg_search-0.25.6/docs/deploy/self-hosted/extension.mdx

**Történeti kontextus (mikor jelent meg a PG18-támogatás):**
> "We just released PG18 with v0.21.0. Thank you all for your patience!"
URL: https://github.com/paradedb/paradedb/issues/2723

**Verdikt: IGAZOLVA.** A PG18-támogatás v0.21.0-tól létezik, és a 0.25.x sorozat (README + Docker Hub + csomag-doksi, három egymástól független elsődleges/hivatalos forrás) folyamatosan tartalmazza a PG18 build-eket.

### 6. `pg_amcheck` lefedettsége és a ParadeDB `pdb.verify_index`

**Hivatalos `pg_amcheck` doksi — mit ellenőriz:**
> "pg_amcheck supports running amcheck's corruption checking functions against one or more databases… **Only ordinary and toast table relations, materialized views, sequences, and btree indexes are currently supported. Other relation types are silently skipped.**"
URL: https://www.postgresql.org/docs/current/app-pgamcheck.html (azonos: https://www.postgresql.org/docs/19/app-pgamcheck.html, https://www.postgresql.org/docs/17/app-pgamcheck.html)

**Hivatalos `amcheck` modul doksi — heap és B-tree függvények:**
> "The B-Tree checking functions verify various invariants in the structure of the representation of particular relations… Unlike the B-Tree checking functions which report corruption by raising errors, the heap checking function `verify_heapam` checks a table and attempts to return a set of rows, one row per corruption detected."
URL: https://www.postgresql.org/docs/current/amcheck.html

Ebből következik: a `pg_amcheck`/`amcheck` **kizárólag** heap relációkat (tábla, TOAST, materializált nézet, szekvencia) és **B-tree** indexeket ellenőriz; más access method-ú indexeket (GIN, GiST, BRIN, hash, vagy egy egyedi AM, mint a ParadeDB BM25 indexe) **nem** — ezeket „silently skipped"-ként (csendben kihagyja).

**ParadeDB `pdb.verify_index` — hivatalos doksi:**
> "ParadeDB provides `amcheck`-style index verification functions to detect corruption and validate the structural integrity of BM25 indexes… The `pdb.verify_index` function performs structural integrity checks on a BM25 index… This returns a table with three columns: `check_name`, `passed`, `details`… To verify that all indexed entries still exist in the heap table, use the `heapallindexed` option… This adds an additional check that validates every indexed `ctid` (tuple identifier) references a valid row in the table."
URL: https://docs.paradedb.com/documentation/indexing/verify-index

**A funkciót bevezető ParadeDB PR leírása (mit csekkol pontosan):**
> "New functions in the `pdb` schema: **`pdb.verify_index(index)`** - Verifies a single index with checks for schema validity, readability, segment checksums, metadata consistency, and optionally heap reference validation (`heapallindexed := true`) […] `on_error_stop` - Stop on first error (like `pg_amcheck`)"
URL: https://github.com/paradedb/paradedb/pull/3907

**Verdikt: IGAZOLVA.** A `pg_amcheck` doksija explicit kimondja, hogy csak heap + B-tree relációkat támogat, minden mást csendben kihagy — tehát nem ellenőrzi a ParadeDB BM25 indexét. A ParadeDB ezért épített egy saját, „amcheck-style" `pdb.verify_index`/`pdb.verify_all_indexes` eszközt, amely a BM25 index szegmens-szintű checksumjait, séma-érvényességét, metaadat-konzisztenciáját és (opcionálisan) a heap-referenciákat ellenőrzi.

## Amit ez a döntésre jelent

- A helyi próba tünete (elrontott bájtokat semmi nem vett észre alap Postgres 16-on, de `initdb --data-checksums` azonnal jelezte) technikailag konzisztens a hivatalos doksival: PG16-ban a checksum nem alapértelmezett, tehát egy alap `initdb`-vel létrehozott PG16 fürtön a `pg_amcheck`/`pg_dump`/`SELECT` valóban nem tud checksum-hibát jelezni, mert nincs mit ellenőriznie (nincs tárolt checksum).
- PostgreSQL 18-tól (a ParadeDB egyik támogatott, és a Docker image-en alapértelmezett verziójától) az `initdb` már alapból bekapcsolja a checksumot — így egy PG18-alapú ParadeDB telepítésen a leírt hiba-osztály (néma bitsérülés) alapból detektálható lenne, külön kapcsoló nélkül is.
- A `pg_checksums --enable` utólagos bekapcsolás **kizárólag leállított** fürtön lehetséges (PG15–18-on; PG19 fejlesztői ágban jelenik meg majd az online változat), és a hivatalos doksi csak annyit ígér, hogy nagy fürtön „sokáig tarthat" — konkrét időbecslést nem ad, tervezéskor ezt mérni kell, nem a doksiból kiolvasni.
- A teljesítményköltségre vonatkozó, gyakran idézett „noticeable performance penalty" mondat a jelenlegi (PG18) hivatalos dokumentációban már nem szerepel szó szerint; a friss szöveg „small performance penalty"-t mond — érdemes a forrást verzióhoz kötve idézni, nem generikusan „a Postgres doksi szerint".
- A ParadeDB Docker image-e (pg15–pg18 címkékkel, `latest` = PG18) igazoltan a hivatalos `postgres` image-re épül és nem írja felül annak entrypoint-ját — ez erős jel arra, hogy a `POSTGRES_INITDB_ARGS=--data-checksums` működne rajta, de ezt a ParadeDB saját doksija nem mondja ki, nem is tesztelt/dokumentált forgatókönyv az ő oldalukon.
- A `pg_search` 0.25.x sorozat PG18-kompatibilitása több egymástól független hivatalos forrásból (README, Docker Hub címkék, csomag-telepítési doksi) is megerősített; a PG18-támogatás eredetileg v0.21.0-ban jelent meg.
- A `pg_amcheck` szerkezetileg nem képes ellenőrizni a ParadeDB BM25 (nem B-tree) indexét — ez a doksi explicit „silently skipped" kitétele alapján egyértelmű; a BM25-index-integritás ellenőrzésére a ParadeDB egy különálló, saját `pdb.verify_index`/`pdb.verify_all_indexes` eszközt fejlesztett, amely funkcionálisan az `amcheck`-et mintázza, de nem azzal azonos kódúton fut.
