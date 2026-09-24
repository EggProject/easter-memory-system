# Linkek — ParadeDB



---

# SQ01 — Mi a ParadeDB pontosan, és mennyire érett?
## Meglátogatott és felderített linkek

| Cím | URL | Tier | Lekérés módja | Megjegyzés |
|---|---|---|---|---|
| ParaDB — Paranormal Reporting Database | https://paradb.sourceforge.net/ | T1 | WebSearch találat | Egyértelműsítés: független termék |
| ParaDB genomikai adatbázis (PLOS NTD) | https://journals.plos.org/plosntds/article?id=10.1371%2Fjournal.pntd.0007576 | T1 | WebSearch találat | Egyértelműsítés: független termék, peer-reviewed |
| ParaDB genomikai adatbázis (PMC másodpéldány) | https://pmc.ncbi.nlm.nih.gov/articles/PMC6658007/ | T1 | WebSearch találat | Ua. cikk, PMC-tükrözés |
| Introduction to ParadeDB and pg_search | https://www.paradedb.com/docs/start/introduction | T1 | WebFetch | Alapdefiníció, architektúra, GitHub-statisztikák |
| GitHub — paradedb/paradedb | https://github.com/paradedb/paradedb | T1 | WebFetch (2×) | Repó-leírás, csillag/fork/issue-szám |
| pg_search/README.md (main ág, raw) | https://raw.githubusercontent.com/paradedb/paradedb/main/pg_search/README.md | T1 | curl (raw.githubusercontent.com) | Támogatott PG-verziók, pgvector-függőség szó szerint |
| LICENSE (main ág, raw) | https://raw.githubusercontent.com/paradedb/paradedb/main/LICENSE | T1 | curl (raw.githubusercontent.com) | AGPLv3 szövege |
| pg_analytics README (dev ág, raw) | https://raw.githubusercontent.com/paradedb/pg_analytics/dev/README.md | T1 | curl (raw.githubusercontent.com) | Archiválási közlemény, pg_lakehouse→pg_analytics átnevezés |
| pg_lakehouse README (történeti commit) | https://github.com/paradedb/paradedb/blob/ea729db69722aaacf9071086978fecf358d4340f/pg_lakehouse/README.md | T1 | WebSearch találat / hivatkozás | A pg_lakehouse eredeti leírása |
| GitHub — paradedb/pg_analytics | https://github.com/paradedb/pg_analytics | T1 | WebFetch | „Archived by the owner on Mar 19, 2025" |
| GitHub Releases — latest | https://github.com/paradedb/paradedb/releases/latest | T1 | WebFetch | v0.25.9, 2026-09-11 (megerősítő 1. forrás) |
| GitHub Releases — lista (több lekérés) | https://github.com/paradedb/paradedb/releases | T1 | WebFetch (több oldal, ?page=) | Ellentmondó eredmények — l. Ellentmondások 3. pont |
| Docker Hub API — tags | https://hub.docker.com/v2/repositories/paradedb/paradedb/tags | T1 | curl (közvetlen API) | Kiadási ütem, dátumok, v0.25.9 (megerősítő 2. forrás) |
| Docker Hub API — repo info | https://hub.docker.com/v2/repositories/paradedb/paradedb | T1 | curl (közvetlen API) | Összes letöltés: 3 112 101 pull |
| PGXN — pg_search | https://pgxn.org/dist/pg_search/ | T2 | WebFetch | v0.25.9, 2026-09-11 (megerősítő 3. forrás), AGPL+Enterprise megjegyzés |
| ParadeDB changelog — 0.25.0 | https://www.paradedb.com/docs/project/changelog/0.25.0 | T1 | WebFetch | „Breaking change": pgvector kötelező függőség |
| ParadeDB changelog — 0.10.0 | https://docs.paradedb.com/changelog/0.10.0 | T1 | WebFetch | Korai „Breaking Changes 🚨" példa |
| ParadeDB changelog — 0.25.9 | https://www.paradedb.com/docs/project/changelog/0.25.9.md | T1 | WebFetch | Legfrissebb kiadás tartalmi kivonata |
| ParadeDB changelog — index oldal | https://www.paradedb.com/docs/project/changelog.md | T1 | WebFetch | Navigációs oldal, kevés konkrét adat |
| ParadeDB sitemap (docs) | https://www.paradedb.com/docs/sitemap.xml | T1 | WebFetch | Changelog-URL-ek felderítése |
| Series A announcement | https://www.paradedb.com/blog/series-a-announcement | T1 | WebFetch | 12M USD Series A, Craft Ventures, YC, 2025.07.14 |
| Why We Picked AGPL | https://www.paradedb.com/blog/agpl | T1 | WebFetch | Licencválasztás indoklása, korábbi ELv2-tapasztalat |
| ParadeDB Enterprise | https://www.paradedb.com/docs/operate/deploy/enterprise | T1 | WebFetch | Enterprise vs Community funkciók, licenc |
| Deploy — self-hosted extension | https://www.paradedb.com/docs/deploy/self-hosted/extension | T1 | WebFetch | Linux/macOS csomagok, PG-verziók |
| Deploy — overview | https://www.paradedb.com/docs/deploy/overview | T1 | WebFetch | Railway/Render/Fly.io/DO/Dokku/BYOC/Cloud |
| Deploy — third-party extensions | https://www.paradedb.com/docs/deploy/third-party-extensions | T1 | WebFetch | Managed providerek NEM említve |
| ParadeDB Cloud | https://www.paradedb.com/cloud | T1 | WebFetch | „Coming soon" / várólista |
| Vector search overview | https://www.paradedb.com/docs/documentation/vector/overview | T1 | WebFetch | Vektoros keresés beta-státusza 0.25.0 fölött |
| Customers | https://www.paradedb.com/customers | T1 | WebFetch | 7 hivatalos esettanulmány listája |
| Case study — INSA Strasbourg | https://www.paradedb.com/customers/case-study-insa | T1 | WebFetch | 1,5 TB, 66M dokumentum, sub-100ms |
| TechCrunch cikk (2025.07.15.) | https://techcrunch.com/2025/07/15/paradedb-takes-on-elasticsearch-as-interest-in-postgres-explodes-amid-ai-boom/ | T2 | WebFetch | Független megerősítés: alapítók, csapatméret, ügyfelek |
| Neon blog — pg_search bejelentés | https://neon.com/blog/pgsearch-on-neon | T1 | WebFetch | 2025.03.18., eredeti Neon–ParadeDB partnerség |
| Neon changelog 2026-04-03 | https://neon.com/docs/changelog/2026-04-03 | T1 | WebFetch | pg_search deprecation, 2026.03.19-i határnap |
| Neon — migrate pg_search to lakebase_text | https://neon.com/docs/extensions/migrate-pg-search-to-lakebase-text | T1 | WebFetch | Teljes kivezetés 2026.09.21-ig, utódmegoldás |
| Neon extensions — pg_search doksi | https://neon.com/docs/extensions/pg_search | T1 | WebFetch | Verziókövetelmények, régió-korlátozás (AWS-only) |
| GitHub issue — Neon pg_search removal | https://github.com/msocietyhq/community-os/issues/57 | T2 | WebSearch találat | Független megerősítés a Neon-kivezetésről |
| Supabase — ParadeDB partneroldal | https://supabase.com/partners/paradedb | T1 | WebFetch | „Works With Supabase" katalógusbejegyzés |
| AWS RDS — kiterjesztés-lista (UserGuide) | https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Appendix.PostgreSQL.CommonDBATasks.Extensions.html | T1 | WebFetch | pg_search/paradedb NEM szerepel |
| AWS RDS — kiterjesztésverziók (ReleaseNotes) | https://docs.aws.amazon.com/AmazonRDS/latest/PostgreSQLReleaseNotes/postgresql-extensions.html | T1 | WebFetch | pg_search/paradedb NEM szerepel egyik PG-verziónál sem |
| Galaxy blog — ParadeDB AWS RDS-en | https://www.getgalaxy.io/learn/glossary/how-to-use-paradedb-on-aws-in-postgresql | T3 | WebFetch | Ellentmond az AWS hivatalos dokumentációnak |



---

# SQ02 — Licenc és függőségi kockázat
## Meglátogatott és felderített linkek

| Cím | URL | Tier | Lekérés módja | Megjegyzés |
|---|---|---|---|---|
| paradedb/paradedb — LICENSE (nyers fájl) | https://raw.githubusercontent.com/paradedb/paradedb/main/LICENSE | T1 | `curl` (nyers fájl) | Teljes AGPL-3.0 szöveg, generikus sablon |
| paradedb/paradedb — LICENSE (GitHub UI) | https://github.com/paradedb/paradedb/blob/main/LICENSE | T1 | WebFetch | Megerősíti: AGPLv3, FSF copyright fejléc |
| paradedb/paradedb — Cargo.toml (nyers fájl) | https://raw.githubusercontent.com/paradedb/paradedb/main/Cargo.toml | T1 | `curl` (nyers fájl) | `license = "AGPL-3.0"`, version 0.25.6 |
| paradedb/paradedb — pg_search/Cargo.toml | https://raw.githubusercontent.com/paradedb/paradedb/main/pg_search/Cargo.toml | T1 | `curl` (nyers fájl) | `license = { workspace = true }` |
| paradedb/paradedb — CONTRIBUTING.md | https://raw.githubusercontent.com/paradedb/paradedb/main/CONTRIBUTING.md | T1 | `curl` (nyers fájl) | CLA-kötelezettség, AGPL + kereskedelmi dupla licencelés a hozzájárulásokra |
| paradedb/paradedb — CHANGELOG.md | https://raw.githubusercontent.com/paradedb/paradedb/main/CHANGELOG.md | T1 | `curl` (nyers fájl) | Csak a docs changelog oldalára mutat, nincs saját tartalom |
| ParadeDB Enterprise (dokumentáció) | https://docs.paradedb.com/deploy/enterprise | T1 | `curl` (nyers HTML, szöveg kinyerve) | Feature Comparison táblázat, „adds commercial licensing" |
| ParadeDB Enterprise (kanonikus doksi-link) | https://www.paradedb.com/docs/operate/deploy/enterprise | T1 | csak URL azonosítás (llms.txt-ből) | Ugyanaz a tartalom más URL-en, nem külön lekérve |
| ParadeDB docs — teljes oldaltérkép | https://docs.paradedb.com/llms.txt | T1 | `curl` (nyers fájl) | Nincs külön „License FAQ" oldal |
| „Why We Picked AGPL" (blog) | https://www.paradedb.com/blog/agpl | T1 | `curl` (nyers HTML, szöveg kinyerve) | Philippe Noël, 2024-08-03; „from day one" AGPL |
| „Introducing ParadeDB pg_search" (blog) | https://www.paradedb.com/blog/introducing-search | T1 | `curl` (nyers HTML, szöveg kinyerve) | Ming Ying, 2023-11-15; pg_bm25→pg_search átnevezés, v0.6.0 |
| „Introducing ParadeDB" (első blogbejegyzés) | https://www.paradedb.com/blog/introducing-paradedb | T1 | WebFetch | Ming Ying, 2023-08-31; nincs licenc-említés |
| „Announcing Our $12M Series A" (blog) | https://www.paradedb.com/blog/series-a-announcement | T1 | `curl` (nyers HTML, szöveg kinyerve) | Ming Ying, 2025-07-14; $12M/$14M, Craft Ventures + YC |
| ParadeDB Roadmap | https://www.paradedb.com/docs/project/roadmap.md | T1 | `curl` (nyers fájl) | „lean team", vektoros keresés fejlesztés alatt |
| ParadeDB vs. Alternatives | https://www.paradedb.com/docs/start/alternatives.md | T1 | `curl` (nyers fájl) | pgvector-relációt írja le (ParadeDB saját indexet használ) |
| pg_analytics — LICENSE (nyers fájl) | https://raw.githubusercontent.com/paradedb/pg_analytics/dev/LICENSE | T1 | `curl` (nyers fájl) | PostgreSQL License, Copyright (c) 2025, ParadeDB |
| pg_analytics — README.md (nyers fájl) | https://raw.githubusercontent.com/paradedb/pg_analytics/dev/README.md | T1 | `curl` (nyers fájl) | Megszűnés-értesítés, pg_search-be olvasztva |
| pg_analytics (GitHub, archív banner) | https://github.com/paradedb/pg_analytics | T1 | WebFetch (2×, konzisztens eredmény) | „archived… on Mar 19, 2025" |
| paradedb GitHub szervezet — repólista | https://github.com/orgs/paradedb/repositories | T1 | WebFetch | Vegyes licencek: MIT, Apache-2.0, PostgreSQL License, AGPL |
| paradedb/paradedb (GitHub fő oldal) | https://github.com/paradedb/paradedb | T1 | WebFetch | Csillagok (9.2k), forkok (445), issue-k, PR-ek, commit-szám |
| ParadeDB CLA (gist) | https://gist.github.com/philippemnoel/5ba3a20230bc1c3c0ae89caeb0597f4a | T1 | WebFetch (összefoglaló) | Copyright/patent grant szövege, összefoglalva idézve |
| GNU AGPL-3.0 hivatalos szöveg | https://www.gnu.org/licenses/agpl-3.0.txt | T1 | `curl` (nyers fájl) | 13. szakasz szó szerint, megegyezik a repó LICENSE-ével |
| GNU GPL FAQ (AGPL-releváns szakaszok) | https://www.gnu.org/licenses/gpl-faq.html | T1 | `curl` (nyers HTML, anchor-alapú kinyerés) | UnreleasedModsAGPL, AGPLv3InteractingRemotely, AGPLv3ServerAsUser, AGPLv3CorrespondingSource, AGPLProxy, SeparateAffero, MereAggregation, GPLInProprietarySystem |
| pgvector — LICENSE (nyers fájl) | https://raw.githubusercontent.com/pgvector/pgvector/master/LICENSE | T1 | `curl` (nyers fájl) | PostgreSQL License szó szerint |
| pgvector (GitHub fő oldal) | https://github.com/pgvector/pgvector | T1 | WebFetch | 23.1k csillag; egy összefoglaló téves „Apache 2.0"-t is állított (elvetve) |
| PostgreSQL License (OSI) | https://opensource.org/license/postgresql | T2 | csak keresési találat, nem külön lekérve | Licenctípus azonosításhoz kiegészítő forrás |
| pg_textsearch — LICENSE (nyers fájl) | https://raw.githubusercontent.com/timescale/pg_textsearch/main/LICENSE | T1 | `curl` (nyers fájl) | PostgreSQL License — engedékenyebb alternatíva |
| pg_textsearch v1.0 bejelentés | https://www.postgresql.org/about/news/pg_textsearch-v10-3264 | T1/T2 | csak keresési találat, nem külön lekérve | PostgreSQL.org hivatalos hírportál |
| VectorChord-bm25 — LICENSE (nyers fájl) | https://raw.githubusercontent.com/tensorchord/VectorChord-bm25/main/LICENSE | T1 | `curl` (nyers fájl) | Dupla AGPLv3/kereskedelmi licenc |
| ZomboDB LICENSE (nyers fájl, master ág) | https://raw.githubusercontent.com/zombodb/zombodb/master/LICENSE | — | `curl` (nyers fájl) | 404 — nem sikerült elérni, NINCS FORRÁS |
| ZomboDB LICENSE (nyers fájl, main ág) | https://raw.githubusercontent.com/zombodb/zombodb/main/LICENSE | — | `curl` (nyers fájl) | 404 — nem sikerült elérni, NINCS FORRÁS |
| Hacker News — „All ParadeDB extensions…" szál | https://news.ycombinator.com/item?id=40348443 | T2/T3 | WebFetch (összefoglaló) | philippemnoel komment, 2024-05-13; ellentmond a pg_analytics-ténynek |
| Hacker News — ParadeDB maintainer szál | https://news.ycombinator.com/item?id=44637543 | T3 | csak keresési találat, nem elemezve | Wire-protocol kompatibilitásról, nem közvetlenül licencrelevancia |
| TechCrunch — ParadeDB Series A cikk | https://techcrunch.com/2025/07/15/paradedb-takes-on-elasticsearch-as-interest-in-postgres-explodes-amid-ai-boom | T2 | WebFetch (összefoglaló) | Csapatméret („team of four"), alapítás 2023, $12M Series A |
| dbdb.io — ParadeDB bejegyzés | https://dbdb.io/db/paradedb | T2/T3 | WebFetch (összefoglaló) | Független megerősítés: AGPL v3, első commit 2023-06-30 |
| paradedb/paradedb GitHub Discussion #3521 | https://github.com/orgs/paradedb/discussions/3521 | T3 | csak cím a keresési találatból, tartalom nem elérve | Lehetséges funkció-visszavonás gyanúja BM25/standby témában — nem megerősített |
| GitHub robots.txt | https://github.com/robots.txt | — | WebFetch | Igazolja a /graphs, /contributors, /commits tiltását |
| Wayback Machine — availability API | https://archive.org/wayback/available | — | `curl` (JSON API, sikeres) | Csak metaadat (van-e pillanatfelvétel), maga a snapshot nem elérhető |
| Wayback Machine — snapshot (2023-09-21) | http://web.archive.org/web/20230921184337/https://github.com/paradedb/paradedb | — | `curl` és WebFetch is | Mindkettő blokkolva („Blocked by egress policy" / „SITE_BLOCKED") |
| GitHub API — repo info | https://api.github.com/repos/paradedb/paradedb | — | `curl` | Session-szinten nem elérhető ebben a környezetben („add_repo" szükséges, nem állt rendelkezésre) |



---

# SQ03 — Szöveges keresés a ParadeDB-ben, különös tekintettel a magyarra
## Meglátogatott és felderített linkek

| Cím | URL | Tier | Lekérés módja | Megjegyzés |
|---|---|---|---|---|
| Create an Index (ParadeDB) | https://www.paradedb.com/docs/reference/indexing/create-index.md | T1 | curl (raw markdown) | CREATE INDEX szintaxis, key_field, egy index/tábla, BM25 paraméterek |
| Limitations & Tradeoffs (ParadeDB) | https://www.paradedb.com/docs/welcome/limitations.md | T1 | curl | Covering index / egy index per tábla, 2. megerősítés |
| Architecture (ParadeDB) | https://www.paradedb.com/docs/welcome/architecture.md | T1 | curl + WebFetch | Tranzakciós írásviselkedés, LSM-fa, Tantivy/pgrx/DataFusion függőség |
| How the ParadeDB Index Works | https://www.paradedb.com/docs/concepts/how-the-paradedb-index-works.md | T1 | curl | Tranzakciós írásviselkedés, 2. megerősítés |
| Welcome to ParadeDB | https://www.paradedb.com/docs/welcome/introduction.md | T1 | curl | Bevezető, "same transaction" ábra-felirat |
| Stemmer (ParadeDB) | https://www.paradedb.com/docs/reference/token-filters/stemming.md | T1 | curl | Magyar tövező megléte, 20 nyelv listája |
| ASCII Folding (ParadeDB) | https://www.paradedb.com/docs/reference/token-filters/ascii-folding.md | T1 | curl | Ékezet-lehagyás, café/naïve/coöperate példa |
| Token Filters Overview (ParadeDB) | https://www.paradedb.com/docs/reference/token-filters/overview.md | T1 | curl | Token filter általános leírás |
| Tokenizers Overview (ParadeDB) | https://www.paradedb.com/docs/reference/tokenizers/overview.md | T1 | curl | Teljes tokenizáló-lista, per-oszlop konfiguráció |
| Unicode tokenizer | https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/unicode.md | T1 | curl | Alapértelmezett tokenizáló leírása |
| Simple tokenizer | https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/simple.md | T1 | curl | Nem-alfanumerikus elválasztás |
| Whitespace tokenizer | https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/whitespace.md | T1 | curl | Csak szóköz-elválasztás |
| Literal tokenizer | https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/literal.md | T1 | curl | Pontos-egyezés / kulcsszó mező |
| Literal Normalized tokenizer | https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/literal-normalized.md | T1 | curl | Kisbetűsített pontos-egyezés |
| Source Code tokenizer | https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/source-code.md | T1 | curl | camelCase/snake_case splitting, azonosítók |
| Ngram tokenizer | https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/ngrams.md | T1 | curl | Részszó-keresés, positions=true |
| Edge Ngram tokenizer | https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/edge-ngrams.md | T1 | curl | Prefix-keresés / search-as-you-type |
| Regex Patterns tokenizer | https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/regex.md | T1 | curl | Regex-alapú tokenizálás |
| Chinese Compatible tokenizer | https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/chinese-compatible.md | T1 | curl | CJK karakterenkénti tokenizálás |
| Lindera tokenizer | https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/lindera.md | T1 | curl | CC-CEDICT/IPADIC/KoDic szótárak |
| ICU tokenizer | https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/icu.md | T1 | curl | Unicode-alapú többnyelvű tokenizálás |
| Jieba tokenizer | https://www.paradedb.com/docs/reference/tokenizers/available-tokenizers/jieba.md | T1 | curl | Kínai statisztikai tokenizálás |
| Multiple Tokenizers Per Field | https://www.paradedb.com/docs/reference/tokenizers/multiple-per-field.md | T1 | curl | Több nyelv/tokenizáló egy mezőn |
| Full-Text / Lexical Search Overview | https://www.paradedb.com/docs/reference/full-text/overview.md | T1 | curl | @@@ operátor áttekintés |
| Term | https://www.paradedb.com/docs/reference/full-text/term.md | T1 | curl | === operátor, term set |
| Fuzzy | https://www.paradedb.com/docs/reference/full-text/fuzzy.md | T1 | curl | Levenshtein, max. távolság 2, prefix mód |
| Match | https://www.paradedb.com/docs/reference/full-text/match.md | T1 | curl | \|\|\| és &&& operátorok |
| Phrase | https://www.paradedb.com/docs/reference/full-text/phrase.md | T1 | curl | ### operátor, slop |
| Query Parser | https://www.paradedb.com/docs/reference/full-text/query-parser.md | T1 | curl | pdb.parse(), Tantivy query string |
| Advanced Query Functions (query-builder) | https://www.paradedb.com/docs/reference/full-text/query-builder.md | T1 | curl | @@@ operátor általános leírása |
| BM25 Scoring (score) | https://www.paradedb.com/docs/reference/full-text/score.md | T1 | curl | pdb.score(), VACUUM hatása |
| Indexing JSON | https://www.paradedb.com/docs/reference/indexing/indexing-json.md | T1 | curl | JSON/JSONB automatikus indexelése |
| Changelog (ParadeDB) | https://www.paradedb.com/docs/project/changelog.md | T1 | curl | Nem tartalmazott közvetlen verziólistát |
| Self-hosted Extension install | https://www.paradedb.com/docs/operate/deploy/self-hosted/extension.md | T1 | curl | Nincs tokenizáló-specifikus feature-flag említés |
| pg_search README (PGXN, v0.15.13) | https://api.pgxn.org/src/pg_search/pg_search-0.15.13/pg_search/README.md | T1 | curl | ICU --features flag, korábbi verzió |
| pg_search README (PGXN, v0.25.9) | https://api.pgxn.org/src/pg_search/pg_search-0.25.9/pg_search/README.md | T1 | curl | Jelenlegi README, rövidebb, nincs feature-flag infó |
| pg_search csomagmetaadat (PGXN) | https://api.pgxn.org/dist/pg_search.json | T1 | curl | Verzió (0.25.9), dátum, Tantivy/pgrx leírás |
| paradedb/paradedb Docker Hub tag-ek | https://hub.docker.com/v2/repositories/paradedb/paradedb/tags | T1 | curl (API) | Verzió- és dátumellenőrzés (v0.25.9, 2026-09-11) |
| llms.txt dokumentáció-index (ParadeDB) | https://www.paradedb.com/docs/llms.txt | T1 | curl | Teljes tokenizáló/query lista feltérképezése |
| PostgreSQL 12.3. Controlling Text Search | https://www.postgresql.org/docs/current/textsearch-controls.html | T1 | curl + HTML-tisztítás | ts_rank/ts_rank_cd leírása, "only examples" idézet |
| PostgreSQL 12.6. Dictionaries | https://www.postgresql.org/docs/current/textsearch-dictionaries.html | T1 | curl + HTML-tisztítás | Snowball sablon leírása, nyelvlista NEM szerepel rajta |
| PostgreSQL 12.1. Introduction | https://www.postgresql.org/docs/current/textsearch-intro.html | T1 | curl + HTML-tisztítás | Ellenőrizve: nyelvlista itt sem szerepel |
| PostgreSQL forráskód — dict_snowball.c | https://doxygen.postgresql.org/dict__snowball_8c_source.html | T1 | curl + HTML-tisztítás | Magyar Snowball-tövező forráskódi bizonyítéka |
| SQLite FTS5 Extension (hivatalos doksi) | https://sqlite.org/fts5.html | T1 | curl + HTML-tisztítás | unicode61, bm25(), prefix/NEAR/phrase, nincs fuzzy |
| SQLite letöltési oldal (verzió) | https://sqlite.org/download.html | T1 | curl | Aktuális SQLite-verzió (3.53.4) |
| Tantivy AsciiFoldingFilter forráskód (docs.rs) | https://docs.rs/tantivy/latest/src/tantivy/tokenizer/ascii_folding_filter.rs.html | T1 | curl + HTML-tisztítás | ő/ű → o/u leképezés forráskódi bizonyítéka, tantivy v0.26.2 |
| rust-stemmers Algorithm enum (docs.rs) | https://docs.rs/rust-stemmers/latest/rust_stemmers/enum.Algorithm.html | T1 | curl + HTML-tisztítás | Független megerősítés: Hungarian variáns (v1.2.0, 18 nyelv) |
| Snowball hivatalos algoritmus-lista | https://snowballstem.org/algorithms/ | T1 | curl | Független megerősítés: Hungarian/Czech/Polish upstream lista |
| PostgreSQL vs ParadeDB: A Search Comparison (Vineeth Pothulapati) | https://www.vineeth.fyi/blog/pg-vs-pg-search/ | T2 | WebFetch | Független benchmark, konkrét ms-értékek, 2025-08-15 |
| Comparing Text Search Strategies (Neon/dev.to) | https://dev.to/neon-postgres/comparing-text-search-strategies-pgsearch-vs-tsvector-vs-external-engines-54f0 | T3 | WebFetch | Neon üzleti partner ParadeDB-vel, csak részben független |
| Comparing full text search algorithms: BM25, TF-IDF, and Postgres (Evan Schwartz) | https://emschwartz.me/comparing-full-text-search-algorithms-bm25-tf-idf-and-postgres/ | T2 | WebFetch | Független technikai elemzés, ts_rank vs BM25 |
| Postgres Full Text Search vs the rest (Supabase) | https://supabase.com/blog/postgres-full-text-search-vs-the-rest | T2/T3 | WebFetch | Független, 2022-10, ts_rank korlátok |
| SereneDB vs ParadeDB vs TigerData vs Postgres (searchbench) | https://serenedb.com/blog/searchbench-postgres | T2/T3 | WebFetch | Versenytárs által készített, nyílt forráskódú benchmark, 2026-09-07 |
| Beyond FTS5: Building Transactional Full-Text Search in TursoDB | https://turso.tech/blog/beyond-fts5 | T3 | WebFetch | Versenytárs kritikai megjegyzése FTS5-ről, benchmark nélkül |
| ParadeDB GitHub Discussion #1220 | https://github.com/orgs/paradedb/discussions/1220 | T3 | WebFetch | Közösségi visszajelzés hiányzó funkciókról (nem közvetlen forrás a fő állításokhoz) |



---

# SQ04 — Vektoros és hibrid keresés, jogosultsági szűréssel
## Meglátogatott és felderített linkek

| Cím | URL | Tier | Lekérés módja | Megjegyzés |
|---|---|---|---|---|
| pgvector README (master) | https://github.com/pgvector/pgvector/blob/master/README.md | T1 | `curl` a `raw.githubusercontent.com` végpontról, teljes fájl letöltve és `grep`/`sed`-del átfésülve | Exact search, HNSW, IVFFlat, iteratív bejárás, dimenziókorlátok — a válasz gerince |
| pgvector `src/hnsw.c` | https://github.com/pgvector/pgvector/blob/master/src/hnsw.c | T1 | `curl` raw, `grep` az enum/GUC-regisztrációra | `hnsw.iterative_scan` alapértéke `off` (forráskód-szintű megerősítés) |
| pgvector `src/ivfflat.c` | https://github.com/pgvector/pgvector/blob/master/src/ivfflat.c | T1 | `curl` raw, `grep` az enum/GUC-regisztrációra | `ivfflat.iterative_scan` alapértéke `off`; nincs `strict_order` opció IVFFlat-nál |
| pgvector `CHANGELOG.md` | https://github.com/pgvector/pgvector/blob/master/CHANGELOG.md | T1 | `curl` raw | 0.8.0 dátuma (2024-10-30), legfrissebb verzió (0.8.6, 2026-07-29; 0.8.7 unreleased) |
| pgvector GitHub Issue #678 (iteratív scan tervezés) | https://github.com/pgvector/pgvector/issues/678 | T1 | `WebFetch` (a `api.github.com` közvetlen elérése ebben a környezetben repó-szinten tiltva van) | Andrew Kane (ankane) eredeti terve, "streaming" munkanév; nem tartalmaz konkrét recall-számokat |
| ParadeDB — How Vector Search Works | https://www.paradedb.com/docs/concepts/vector/overview | T1 | `curl` + kézi RSC-streaming kibontás (`self.__next_f.push` darabok) | "independent from pgvector's HNSW and IVFFlat indexes" |
| ParadeDB — Indexing Vectors | https://www.paradedb.com/docs/reference/indexing/indexing-vectors | T1 | `curl` + kézi RSC-streaming kibontás | SPANN-stílusú index, `centroid_ratio`/`training_sample_ratio`/`cluster_replication`, csak `vector` típus indexelhető |
| ParadeDB — Querying Vectors | https://www.paradedb.com/docs/reference/vector/querying | T1 | `curl` + kézi RSC-streaming kibontás | Szűrt NN-keresés szintaxisa; nem-indexelt oszlop → Postgres "recheck"; `TopKScanExecState` ellenőrzés |
| ParadeDB — Filtering Overview | https://www.paradedb.com/docs/reference/filtering/overview | T1 | `curl` (308-redirect a `docs.paradedb.com/documentation/filtering`-ről) + kézi RSC-kibontás | Általános elv: ParadeDB elkerüli az "egy sor egyszerre" utólagos szűrést, ahol lehet |
| ParadeDB — Indexed Columns (Filter Pushdown) | https://www.paradedb.com/docs/reference/filtering/indexed | T1 | `curl` (308-redirect a `www.paradedb.com/docs/documentation/filtering/indexed`-ről) + kézi RSC-kibontás | Explicit "Filter Pushdown" fejezet, típus/operátor-táblázat, `literal` tokenizer szövegnél |
| ParadeDB — Reciprocal Rank Fusion | https://www.paradedb.com/docs/reference/hybrid/rrf | T1 | `curl` + kézi RSC-streaming kibontás | Teljes SQL-minta, `weight/(k+rank)` képlet, "add filters to both" ajánlás, pushdown-ellenőrzés |
| ParadeDB — How Hybrid Search Works | https://www.paradedb.com/docs/concepts/hybrid/overview | T1 | `curl` + kézi RSC-streaming kibontás | "cannot be added together directly" — miért RRF és nem súlyozott pontszám-összeg |
| ParadeDB — Changelog 0.25.0 | https://www.paradedb.com/docs/project/changelog/0.25.0 | T1 | `curl` + kézi RSC-streaming kibontás | "Breaking change: pgvector required"; "Native Vector Search (Beta)"; SPANN-index bejelentése dátummal/verzióval |
| ParadeDB `pg_search/README.md` (GitHub, `main`) | https://raw.githubusercontent.com/paradedb/paradedb/main/pg_search/README.md | T1 | `curl` raw | "uses pgvector's types… not its HNSW or IVF indexes" (forráskód-repó szintű megerősítés); build: `pgvector v0.8.6` |
| ParadeDB Docker build — `docker/Dockerfile.paradedb-17` (@0.25.9) | https://cdn.jsdelivr.net/gh/paradedb/paradedb@0.25.9/docker/Dockerfile.paradedb-17 | T1 | `curl` a jsdelivr GitHub-tükrön (a `raw.githubusercontent.com` közvetlen `docker/`-elérése 404-et adott, a helyes útvonalat a jsdelivr fájllista-API-val derítettem ki) | `postgresql-17-pgvector=0.8.4-1.pgdg13+1`; ugyanígy 15/16/18 és `Dockerfile.official-17` |
| ParadeDB Docker build — `docker/Dockerfile.paradedb-17` (@0.26.0-rc.1) | https://cdn.jsdelivr.net/gh/paradedb/paradedb@0.26.0-rc.1/docker/Dockerfile.paradedb-17 | T1 | `curl` a jsdelivr GitHub-tükrön | `postgresql-17-pgvector=0.8.6-1.pgdg13+1` (RC csatorna) |
| jsdelivr package/verzió- és fájllista API (`paradedb/paradedb`) | https://data.jsdelivr.com/v1/packages/gh/paradedb/paradedb és …@0.25.9 | T1/T2 | `curl` JSON API | Verziólista (0.26.0-rc.1, 0.25.9, …); a repó fájlfa feltérképezése, benne a `benchmarks/` mappa felfedezése |
| Docker Hub API — `paradedb/paradedb` tag-lista | https://hub.docker.com/v2/repositories/paradedb/paradedb/tags | T1 | `curl` hivatalos Docker Hub REST API | `latest`=`0.25.9` (2026-09-11), PG18-alapú; `0.26.0-rc.1` időbélyege |
| ParadeDB benchmark-csomag — `benchmarks/README.md` | https://cdn.jsdelivr.net/gh/paradedb/paradedb@0.25.9/benchmarks/README.md | T1 | `curl` a jsdelivr GitHub-tükrön | CI-benchmark módszertan (hot/cold mérés, `pg_stat_statements`) |
| ParadeDB benchmark — `datasets/cohere/config.toml` | https://cdn.jsdelivr.net/gh/paradedb/paradedb@0.25.9/benchmarks/datasets/cohere/config.toml | T1 | `curl` a jsdelivr GitHub-tükrön | 1%/10%/unfiltered HNSW/IVFFlat/VectorChord tuning-célértékek; VectorChord mért recall-számok |
| ParadeDB benchmark — `indexes/hnsw.sql`, `indexes/pg_search.sql`, `queries/knn_top10_1pct.sql`, `queries/pg_search/knn_top10_1pct.sql`, `recall.sql` | https://cdn.jsdelivr.net/gh/paradedb/paradedb@0.25.9/benchmarks/datasets/cohere/… | T1 | `curl` a jsdelivr GitHub-tükrön | Extrém HNSW-paraméterezés 1%-os szelektivitásnál (`ef_search=1000`, `max_scan_tuples` 5M-ig); `relaxed_order` használata; `pg_search` saját `paradedb.vector_cluster_max_probe` GUC-ja |
| AWS Database Blog — pgvector 0.8.0 Aurora-mérés | https://aws.amazon.com/blogs/database/supercharging-vector-search-performance-and-relevance-with-pgvector-0-8-0-on-amazon-aurora-postgresql/ | T2 | `curl` nyers HTML + tag-eltávolítás, `grep` a táblázatra | A feladat hátterében hivatkozott 10%/1%→100% recall-táblázat elsődleges forrása; szerző: Shayon Sanyal, 2025-05-28 |
| arXiv 2602.11443 — Filtered ANN Search in Vector Databases (UC Merced) | https://arxiv.org/html/2602.11443v1 | T1 | `curl` nyers HTML + tag-eltávolítás, `grep` | Független, 2026 februári akadémiai mérés `pgvector 0.8.1`-en; idézi az AWS-blogot; nem teszteli az `iterative_scan`-t explicit |
| ParadeDB — pgvector Limitations (learn/blog) | https://www.paradedb.com/learn/postgresql/pgvector-limitations | T3 | `curl` nyers HTML + tag-eltávolítás | ParadeDB marketing-tartalom; dimenziókorlátok (2000/4000/64000/1000) és szűrt keresés gyengeségének leírása — kiegészítő megerősítés, nem elsődleges referencia |
| Crunchy Data Blog — Hybrid Vector Search | https://www.crunchydata.com/blog/hybrid-vector-search | T3 | `WebFetch` (célzottan ellenőrizve, van-e benne mért recall-szám) | **Negatív találat**: nincs benne empirikus recall-mérés, csak fogalmi/architekturális útmutató (szerző: Christopher Winslett, 2026-07-30) |
| Tiger Data Blog — Postgres Developer's Guide to Vector Index Tradeoffs | https://www.tigerdata.com/blog/the-postgres-developers-guide-to-vector-index-tradeoffs | T3 | `WebFetch` (célzottan ellenőrizve, van-e benne ParadeDB SPANN-specifikus vagy HNSW-szűrés-recall infó) | **Negatív találat**: nem erősíti meg és nem cáfolja a ParadeDB SPANN-index állítást; nem versenytárs-független megerősítés |
| ParadeDB Docker Hub oldal (áttekintés) | https://hub.docker.com/r/paradedb/paradedb | T1 | Csak `WebSearch`-ben felbukkant, tartalma a Docker Hub API-n (fenti sor) keresztül lett ellenőrizve | Nem közvetlenül idézve, a hivatalos API-eredmény pontosabb |
| ParadeDB roadmap | https://docs.paradedb.com/welcome/roadmap | — | Csak `WebSearch` találati listában szerepelt, nem nyitottam meg | Nem használt találat |



---

# SQ05 — Üzemeltetés egy gépen: mentés, frissítés, erőforrás
## Meglátogatott és felderített linkek

| Cím | URL | Tier | Lekérés módja | Megjegyzés |
|---|---|---|---|---|
| Upgrading ParadeDB | https://docs.paradedb.com/deploy/upgrading | T1 | WebFetch | ALTER EXTENSION UPDATE kötelező, REINDEX-ről és pg_upgrade-ről hallgat |
| Reindexing | https://www.paradedb.com/docs/documentation/indexing/reindexing | T1 | WebFetch | REINDEX = séma nélküli újraépítés; CONCURRENTLY opció |
| Index Size | https://docs.paradedb.com/documentation/configuration/index_size | T1 | WebFetch | VACUUM nem csökkenti a méretet, csak jelöli az újrafelhasználható helyet |
| Configuration Reference | https://www.paradedb.com/docs/reference/configuration | T1 | WebFetch | mpp_queue_size, maintenance_work_mem, work_mem leírás |
| Install ParadeDB (getting-started) | https://docs.paradedb.com/documentation/getting-started/install | T1 | WebFetch | Csak Docker-példa, deploy-doksira mutat tovább |
| pg_search README | https://github.com/paradedb/paradedb/blob/main/pg_search/README.md | T1 | WebFetch | Csak fejlesztői/build infó, üzemeltetési infó nincs benne |
| GitHub Discussion #3521 (BM25 standby reads) | https://github.com/orgs/paradedb/discussions/3521 | T1 | WebFetch | Standby-olvasás WAL-integrációja Enterprise-only (2025.11.11., philippemnoel) |
| Enterprise vs Community | https://docs.paradedb.com/deploy/enterprise | T1 | WebFetch | HA/Read Replica Enterprise-only táblázat; lábjegyzet: Community crash recovery csak heap/B-Tree-re |
| Blog: LSM-fák és a replikáció | https://www.paradedb.com/blog/lsm-trees-in-postgres | T1 | WebFetch | VACUUM+standby konzisztencia probléma, hot_standby_feedback |
| Verify Index Integrity (operate) | https://www.paradedb.com/docs/operate/index-maintenance/verify-index | T1 | WebFetch | pdb.verify_index = amcheck-stílusú ellenőrzés, repair nincs leírva |
| Extension (self-hosted install) | https://docs.paradedb.com/deploy/self-hosted/extension | T1 | WebFetch | Deb/RPM/PKG platformlista, macOS csak arm64 |
| GitHub Issue #1019 (APT/Homebrew/Yum) | https://github.com/paradedb/paradedb/issues/1019 | T1 | WebFetch | OPEN; Homebrew-ra nincs konkrét dátum |
| Blog: Block Storage Layout | https://www.paradedb.com/blog/block-storage-part-one | T1 | WebFetch | 2025.01.16.; WAL-integráció és PITR a blokktárolóra váltás előnye |
| Go to Production | https://www.paradedb.com/docs/start/go-to-production | T1 | WebFetch | Csak checklist-szintű backup/RAM említés, konkrét szám nélkül |
| Index Creation (performance tuning) | https://www.paradedb.com/docs/operate/performance-tuning/create-index | T1 | WebFetch | maintenance_work_mem ≈ RAM/16, min. 15 MB/worker |
| Configuring High Availability | https://docs.paradedb.com/deploy/self-hosted/high-availability/configuration | T1 | WebFetch | Barman-alapú backup+PITR, Community/Enterprise megkötés nélkül említve |
| PostgreSQL: Routine Vacuuming | https://www.postgresql.org/docs/current/routine-vacuuming.html | T1 | WebFetch | Holt tuple-ök fizikai helye VACUUM előtt |
| PostgreSQL: Continuous Archiving / PITR | https://www.postgresql.org/docs/current/continuous-archiving.html | T1 | WebFetch | Base backup nem kell konzisztens legyen, WAL-replay javítja |
| PostgreSQL: pg_dump | https://www.postgresql.org/docs/current/app-pgdump.html | T1 | WebFetch | Indexek "post-data" definícióként dumpolva |
| PostgreSQL: pg_basebackup | https://www.postgresql.org/docs/current/app-pgbasebackup.html | T1 | WebFetch | Fájlszintű, teljes klaszter-másolat, PITR/standby induló pontja |
| PostgreSQL: SQL Dump (backup-dump) | https://www.postgresql.org/docs/current/backup-dump.html | T1 | WebFetch | ANALYZE ajánlás restore után |
| GitHub Release v0.24.0 | https://github.com/paradedb/paradedb/releases/tag/v0.24.0 | T1 | WebFetch | "feat: Crash recovery via WAL" (#4901); dátum "03 Jun", év bizonytalan |
| Docker Hub: paradedb/paradedb tags | https://hub.docker.com/r/paradedb/paradedb/tags | T1 | WebFetch | linux/amd64 + linux/arm64 minden tagnél |
| Introduction (start) | https://www.paradedb.com/docs/start/introduction.md | T1 | WebFetch | "vanilla Postgres with an extension installed, not a fork or sidecar" |
| Write Throughput (performance tuning) | https://www.paradedb.com/docs/operate/performance-tuning/writes | T1 | WebFetch | work_mem, paradedb.global_mutable_segment_rows |
| Configuration Overview | https://docs.paradedb.com/documentation/configuration/overview | T1 | WebFetch | Csak maintenance_work_mem példa, kevés tartalom |
| Verify Index Integrity (legacy path) | https://www.paradedb.com/docs/documentation/indexing/verify-index | T1 | WebFetch | Ugyanaz a tartalom, mint az operate/ útvonalon — konzisztens |
| GitHub Issue #2211 (index creation stuck) | https://github.com/paradedb/paradedb/issues/2211 | T1 | WebFetch | CLOSED; nagy táblán 3+ órás index-build-fagyás, v0.10.0→v0.15.2 |
| GitHub Issue #6375 (VACUUM+join scan bug) | https://github.com/paradedb/paradedb/issues/6375 | T1 | WebFetch | CLOSED; HOT update+VACUUM után sorok eltűnése join scan-ben (2026.09.17.) |
| GitHub Issue #6374 (mutable segment segfault) | https://github.com/paradedb/paradedb/issues/6374 | T1 | WebFetch | CLOSED; SIGSEGV parallel top-k scan + mutable segment update (2026.09.17.) |
| Architecture | https://docs.paradedb.com/welcome/architecture | T1 | WebFetch | "merging or compaction", szegmensek immutábilisak flush után |
| PostgreSQL: pg_upgrade | https://www.postgresql.org/docs/current/pgupgrade.html | T1 | WebFetch | Extension shared object fájlokat újra kell telepíteni főverzió-váltáskor |
| PostgreSQL: amcheck | https://www.postgresql.org/docs/current/amcheck.html | T1 | WebFetch | Csak B-Tree és GIN indexekre van natív amcheck-támogatás |
| GitHub Issue #1407 (törölve) | https://github.com/paradedb/paradedb/issues/1407 | T1 | WebFetch | Oldal törölve ("This issue has been deleted") |
| GitHub Issue #713 (törölve) | https://github.com/paradedb/paradedb/issues/713 | T1 | WebFetch | Oldal törölve |
| GitHub Issue #1047 (törölve) | https://github.com/paradedb/paradedb/issues/1047 | T1 | WebFetch | Oldal törölve |
| GitHub Issue #1207 (törölve) | https://github.com/paradedb/paradedb/issues/1207 | T1 | WebFetch | Oldal törölve |
| Neon Docs: pg_search extension | https://neon.com/docs/extensions/pg_search | T2 | WebFetch | Harmadik fél (Neon) doksija; eltérő GUC-nevek a hivatalos ParadeDB doksihoz képest |
| newreleases.io (v0.24.0 mirror) | https://newreleases.io/project/github/paradedb/paradedb/release/v0.24.0 | T3 | WebFetch | Csak relatív dátumot ("3 months ago") adott, nem használható |
| Comprehensive Guide to Backup ParadeDB with pg_dump (Galaxy) | https://www.getgalaxy.io/learn/glossary/how-to-backup-paradedb-in-postgresql | T3 | WebSearch (nem nyitva meg) | Harmadik fél blog, találatként azonosítva, nem idézve |
| Install ParadeDB CLI on macOS/Linux/Windows (Galaxy) | https://www.getgalaxy.io/learn/glossary/how-to-install-paradedb-cli-in-postgresql | T3 | WebSearch (nem nyitva meg) | Harmadik fél blog, nem idézve |
| How to Fix "max memory exceeded" Error (Galaxy) | https://www.getgalaxy.io/learn/glossary/how-to-fix-the-max-memory-exceeded-error-in-paradedb | T3 | WebSearch (nem nyitva meg) | Harmadik fél blog, nem idézve |
| Achieve Faster Search in ParadeDB (RisingWave blog) | https://risingwave.com/blog/achieve-faster-search-in-paradedb-with-these-tips/ | T3 | WebSearch (nem nyitva meg) | Harmadik fél blog, nem idézve |
| pg_search | PIGSTY | https://pigsty.io/ext/e/pg_search/ | T3 | WebSearch (nem nyitva meg) | Harmadik fél csomagolás-doksi, nem idézve |
| Deploy ParadeDB (pg_search) on a VPS (RamNode) | https://ramnode.com/guides/paradedb | T3 | WebSearch (nem nyitva meg) | Harmadik fél guide, nem idézve |



---

# SQ06 — Integráció a TypeScript / Bun / Drizzle / Better Auth stackkel
## Meglátogatott és felderített linkek

| Cím | URL | Tier | Lekérés módja | Megjegyzés |
|---|---|---|---|---|
| ParadeDB for Drizzle — GitHub README | https://github.com/paradedb/drizzle-paradedb | T1 | WebFetch + nyers `curl` (raw.githubusercontent.com) | Hivatalos, MIT licenc, kompatibilitási táblázat |
| drizzle-paradedb `src/search.ts` (forráskód) | https://raw.githubusercontent.com/paradedb/drizzle-paradedb/main/src/search.ts | T1 | `curl` nyers fájl | `@@@`/`&&&`/`###`/`===` implementáció, cosineDistance/l2Distance re-export |
| drizzle-paradedb `src/indexing.ts` (forráskód) | https://raw.githubusercontent.com/paradedb/drizzle-paradedb/main/src/indexing.ts | T1 | `curl` nyers fájl | `paradedbIndex()` implementáció Drizzle `index().using()`-ra épülve |
| drizzle-paradedb `src/index.ts` | https://raw.githubusercontent.com/paradedb/drizzle-paradedb/main/src/index.ts | T1 | `curl` nyers fájl | Modul-export-lista |
| drizzle-paradedb `package.json` | https://raw.githubusercontent.com/paradedb/drizzle-paradedb/main/package.json | T1 | `curl` nyers fájl | Verzió 0.5.0, peerDependency drizzle-orm 1.0.0-rc.4 |
| drizzle-paradedb `tests/indexing.test.ts` | https://raw.githubusercontent.com/paradedb/drizzle-paradedb/main/tests/indexing.test.ts | T1 | `curl` nyers fájl | Bizonyítja a `drizzle-kit generateMigration` helyes `USING paradedb` kimenetét |
| drizzle-paradedb `scripts/run_paradedb.sh` | https://raw.githubusercontent.com/paradedb/drizzle-paradedb/main/scripts/run_paradedb.sh | T1 | `curl` nyers fájl | Saját tesztkörnyezet: `docker run paradedb/paradedb`, NEM testcontainers |
| drizzle-paradedb `CONTRIBUTING.md` | https://raw.githubusercontent.com/paradedb/drizzle-paradedb/main/CONTRIBUTING.md | T1 | `curl` nyers fájl | Teszt-workflow leírása (`pnpm db:setup`, `vitest`) |
| ParadeDB — Create an Index | https://docs.paradedb.com/documentation/indexing/create-index | T1 | WebFetch | ORM-lista (Drizzle, Django, SQLAlchemy, Rails, EF Core); `USING bm25` alias |
| ParadeDB — Operator Reference | https://www.paradedb.com/docs/reference/operators-and-functions | T1 | WebFetch | `@@@`, `&&&`, `\|\|\|`, `===`, `###` hivatalos definíciói |
| ParadeDB — Guarantees | https://www.paradedb.com/docs/welcome/guarantees | T1 | WebFetch | Tranzakció/izoláció-garancia állítás (ld. Ellentmondások) |
| ParadeDB — Getting Started / Install | https://docs.paradedb.com/documentation/getting-started/install | T1 | WebFetch | Hivatalos Docker image / `docker run` parancs |
| ParadeDB — GitHub Actions CI doksi | https://www.paradedb.com/docs/deploy/ci/github-actions | T1 | WebFetch | Hivatalos CI-minta, nem testcontainers |
| ParadeDB — Reindexing | https://www.paradedb.com/docs/operate/index-maintenance/reindexing.md | T1 | WebFetch (redirekt után) | `REINDEX` vs `REINDEX CONCURRENTLY` zárolási viselkedés |
| ParadeDB blog — Block Storage Part One | https://www.paradedb.com/blog/block-storage-part-one | T1 | WebFetch | Szegmens-tárolás, merge_on_insert, zárolás architektúrája |
| `pg_search/README.md` (paradedb/paradedb repó) | https://github.com/paradedb/paradedb/blob/main/pg_search/README.md | T1 | WebFetch | Verzió/kompatibilitási infó, konkurenciáról nincs benne részlet |
| ParadeDB GitHub Releases | https://github.com/paradedb/paradedb/releases | T1 | WebFetch | Legfrissebb release-lista (ld. Ellentmondások) |
| ParadeDB issue #6390 (SIREAD lock hiány) | https://github.com/paradedb/paradedb/issues/6390 | T1 | WebFetch | Nyitva, 2026.09.17., SERIALIZABLE phantom write skew |
| ParadeDB PR #6392 (SIREAD lock javítás) | https://github.com/paradedb/paradedb/pull/6392 | T1 | WebFetch | Nyitva, még nem mergelt, a #6390 javítására |
| ParadeDB issue #5449 (CONCURRENTLY + bm25 hiba) | https://github.com/paradedb/paradedb/issues/5449 | T1 | WebFetch | Nyitva, v0.21.6/v0.24.1 érintett |
| paradedb/prisma-paradedb README | https://github.com/paradedb/prisma-paradedb | T1 | WebFetch | „WIP... Not ready for public consumption” |
| Drizzle ORM — Vector similarity search guide | https://orm.drizzle.team/docs/guides/vector-similarity-search | T1 | WebFetch | `vector()`, `cosineDistance`, min. verzió 0.31.0/kit 0.22.0 |
| Drizzle ORM — PostgreSQL extensions | https://orm.drizzle.team/docs/extensions/pg | T1 | WebFetch | Mind a 6 távolságfüggvény, HNSW-index minta |
| Drizzle ORM — Indexes & Constraints | https://orm.drizzle.team/docs/indexes-constraints | T1 | WebFetch | `.using('btree', ...)` példa |
| drizzle-orm `pg-core/indexes.ts` forráskód | https://raw.githubusercontent.com/drizzle-team/drizzle-orm/main/drizzle-orm/src/pg-core/indexes.ts | T1 | `curl` nyers fájl | `PgIndexMethod` típus, „you can always specify any string” JSDoc |
| Drizzle ORM — Bun SQL | https://orm.drizzle.team/docs/connect-bun-sql | T1 | WebFetch | „natively supports bun sql”, `@rc` csomagok |
| Drizzle ORM — Get Started PostgreSQL | https://orm.drizzle.team/docs/get-started-postgresql | T1 | WebFetch | Támogatott driverek listája |
| npm registry — drizzle-orm | https://registry.npmjs.org/drizzle-orm | T1 | `curl` (JSON API) | dist-tags: latest=0.45.3, rc=1.0.0-rc.4 |
| npm registry — drizzle-kit | https://registry.npmjs.org/drizzle-kit | T1 | `curl` (JSON API) | dist-tags: latest=0.31.11, rc=1.0.0-rc.4 |
| Bun docs — SQL | https://bun.com/docs/runtime/sql | T1 | WebFetch + `curl` (teljes HTML, kulcsszó-keresés) | 0 találat "vector"/"pgvector"-ra |
| Bun GitHub issue #15088 (Bun.sql tracking) | https://github.com/oven-sh/bun/issues/15088 | T1 | WebFetch | Kész/függőben lévő funkciók listája, nincs vector-említés |
| Bun GitHub issue #15438 (postgres-js hang) | https://github.com/oven-sh/bun/issues/15438 | T1 | WebFetch | Closed, PR #15543, Bun 1.1.35+ regresszió |
| node-postgres GitHub issue #3201 (pg-native Bunon) | https://github.com/brianc/node-postgres/issues/3201 | T1 | WebFetch | pg-native natív binding nem töltődik be Bun alatt |
| Better Auth — Drizzle ORM Adapter | https://better-auth.com/docs/adapters/drizzle | T1 | WebFetch | `provider: "pg"`, `schemaName` opció |
| Better Auth issue #7691 (drizzle 1.0rc) | https://github.com/better-auth/better-auth/issues/7691 | T1 | WebFetch | Closed as duplicate of #6766 |
| Better Auth issue #6766 (drizzle v1.0 syntax) | https://github.com/better-auth/better-auth/issues/6766 | T1 | WebFetch | Resolved, better-auth 1.7 RC / PR #9489 |
| Better Auth issue #2283 (Bun+Drizzle+PG CLI crash) | https://github.com/better-auth/better-auth/issues/2283 | T1 | WebFetch | Closed/wontfix, better-sqlite3 segfault Bunon |
| Better Auth issue #7987 (Bun+Docker, better-sqlite3) | https://github.com/better-auth/better-auth/issues/7987 | T1 | WebFetch | Closed, 2026.02.16., providertől független sqlite-függőség |
| PostgreSQL hivatalos doksi — Transaction Isolation | https://www.postgresql.org/docs/current/transaction-iso.html | T1 | WebFetch | Read Committed az alapértelmezett izolációs szint |
| Testcontainers — pgvector modul | https://testcontainers.com/modules/pgvector/ | T1 | WebFetch | Node.js is támogatott, `pgvector/pgvector:pg16` |
| Testcontainers (Java) — Postgres modul | https://java.testcontainers.org/modules/databases/postgres/ | T1 | WebFetch | `asCompatibleSubstituteFor("postgres")` minta, PostGIS/pgvector megemlítve |
| drizzle-team/drizzle-orm issue #2935 (`generate` ignores operators) | https://github.com/drizzle-team/drizzle-orm/issues/2935 | T1 | WebFetch | Closed, 2024.09.09., csak `.op()`-ra vonatkozott |
| deepwiki.com/paradedb/drizzle-paradedb | https://deepwiki.com/paradedb/drizzle-paradedb | T3 | WebFetch | AI-generált wiki; csak tájékozódásra használtam, a tényleges API-t a nyers forráskódból (T1) ellenőriztem |
| newreleases.io — paradedb/paradedb v0.25.6 | https://newreleases.io/project/github/paradedb/paradedb/release/v0.25.6 | T3 | csak keresési találat (nem közvetlenül lekérve/idézve) | Ellentmond a GitHub Releases oldal v0.25.0 legfrissebb-jelzésének (ld. Ellentmondások) |



---

# SQ07 — Valós tapasztalatok, mérések és hibamódok
## Meglátogatott és felderített linkek

| Cím | URL | Tier | Lekérés módja | Megjegyzés |
|---|---|---|---|---|
| Same Query, Three Results: Benchmarking ParadeDB and Postgres FTS | https://www.paradedb.com/blog/benchmarker-iteration | T2 | WebFetch | ParadeDB saját mérése, 2026.06.02., HN 1M sor |
| Postgres as a Search Engine: The Write Performance Problem | https://www.paradedb.com/blog/increased-write-performance | T2 | WebFetch | ParadeDB saját mérése, 2025.12.15., write amplification kifejezés forrása |
| inevolin/ParadeDB-vs-ElasticSearch (GitHub repo) | https://github.com/inevolin/ParadeDB-vs-ElasticSearch | T2 | WebFetch | Független, M1 Mac + lokális k8s, 1M/1M dok |
| PostgreSQL vs ParadeDB: A Search Comparison (Vineeth Pothulapati) | https://www.vineeth.fyi/blog/pg-vs-pg-search/ | T2 | WebFetch | Független, 1,6M Amazon termék, 2025.08.15. |
| SereneDB vs ParadeDB vs TigerData vs Postgres (SereneDB blog) | https://serenedb.com/blog/searchbench-postgres | T2 | WebFetch | Versenytárs CTO-ja írta — COI jelölve, 2026.09.07. |
| Tembo blog — Benchmarking ParadeDB's pg_search | https://tembo.io/blog/paradedb-search/ | — | curl (sikertelen tartalom-kinyerés, JS-renderelt) | Tartalmat nem sikerült kinyerni, NEM használtam fel állítást belőle |
| Issue #1929 — Inconsistent search query results when joining tables with parallel processing | https://github.com/paradedb/paradedb/issues/1929 | T1 | WebFetch | "Wrong results" hiba, 2024.11.12., v0.12.0 |
| Release v0.12.1 | https://github.com/paradedb/paradedb/releases/tag/v0.12.1 | T1 | WebFetch | #1929 javítása, 2024.11.12. |
| Changelog 0.12.1 | https://docs.paradedb.com/changelog/0.12.1 | T1 | WebFetch (élő oldal); utólagos curl 404 | "incorrect results" szó szerinti említés |
| Issue #6375 — Join scan drops one user's rows after HOT update+VACUUM | https://github.com/paradedb/paradedb/issues/6375 | T1 | WebFetch | Wrong results, 2026.09.17., main ág |
| Issue #6394 — Join scan drops the whole row (outer join nullable side) | https://github.com/paradedb/paradedb/issues/6394 | T1 | WebFetch | Wrong results, 2026.09.17. |
| Issue #6108 — Sequential scan fallback returns no rows for NUMERIC key fields | https://github.com/paradedb/paradedb/issues/6108 | T1 | WebFetch | Nyitott hiba (fetch időpontjában) |
| Issue #6101 — BM25 indexes reject valid NUMERIC typmods | https://github.com/paradedb/paradedb/issues/6101 | T1 | WebFetch | Nyitott, v0.25.4 |
| Issue #6374 — Parallel top-k scan segfaults after two updates | https://github.com/paradedb/paradedb/issues/6374 | T1 | WebFetch | Crash, 2026.09.17. |
| Issue #6384 — Parallel top-K scan fails with "segment ... should exist" | https://github.com/paradedb/paradedb/issues/6384 | T1 | WebFetch | Index-out-of-sync jellegű, 2026.09.17. |
| Issue #702 — TRUNCATE is broken, tries to recreate the index | https://github.com/paradedb/paradedb/issues/702 | T1 | WebFetch | 2024.01.19., v0.4.4 |
| Issue #2575 — Unable to delete from a table with a BM25 index | https://github.com/paradedb/paradedb/issues/2575 | T1 | WebFetch | 2025.05.15., v0.15.19 |
| Issue #2211 — BM25 index creation stuck | https://github.com/paradedb/paradedb/issues/2211 | T1 | WebFetch | 2025.02.21., v0.15.2 |
| Issue #2038 — Filtering by paradedb.score(id) leads to no results | https://github.com/paradedb/paradedb/issues/2038 | T1 | WebFetch | 2024.12.30. |
| Issue #1685 — Locking issue in v0.8.6 | https://github.com/paradedb/paradedb/issues/1685 | T1 | WebFetch | 2024.09.19., >3M sor |
| Issue #5449 — CREATE INDEX CONCURRENTLY fails with missing pg_tblspc file | https://github.com/paradedb/paradedb/issues/5449 | T1 | WebFetch | v0.21.6, v0.24.1 |
| Issue #6208 — CREATE INDEX CONCURRENTLY leaks buffer pins (PG15/16) | https://github.com/paradedb/paradedb/issues/6208 | T1 | WebFetch | Root cause azonosítva |
| Issue #5999 — JoinScan anti-joins regress 0.24.3→0.25.3 | https://github.com/paradedb/paradedb/issues/5999 | T1 | WebFetch | Teljesítmény-regresszió, nem véglegesen javítva |
| Issue #2436 — Can't migrate 0.15.11 > 0.15.16 (missing pg_analytics) | https://github.com/paradedb/paradedb/issues/2436 | T1 | WebFetch | Upgrade-hiba, 2025.04.16. |
| Issue #1406 (törölve) | https://github.com/paradedb/paradedb/issues/1406 | T1 | WebFetch | Tartalom nem elérhető |
| Issue #1407 (törölve) | https://github.com/paradedb/paradedb/issues/1407 | T1 | WebFetch | Tartalom nem elérhető |
| Issue #1631 (törölve) | https://github.com/paradedb/paradedb/issues/1631 | T1 | WebFetch | Tartalom nem elérhető |
| Issue #1895 (törölve) | https://github.com/paradedb/paradedb/issues/1895 | T1 | WebFetch | Tartalom nem elérhető |
| Issue #1207 (törölve) | https://github.com/paradedb/paradedb/issues/1207 | T1 | WebFetch | Tartalom nem elérhető |
| Limitations & Tradeoffs | https://docs.paradedb.com/welcome/limitations | T1 | curl (nyers HTML-ből szöveg kinyerve) | Aktuális, v0.25.9 |
| Write Throughput | https://docs.paradedb.com/documentation/performance-tuning/writes | T1 | curl (nyers HTML-ből szöveg kinyerve) | Aktuális, v0.25.9 |
| ParadeDB Enterprise (feature comparison) | https://www.paradedb.com/docs/operate/deploy/enterprise | T1 | llms-full.txt (curl) | Community vs Enterprise táblázat |
| Guarantees | https://www.paradedb.com/docs/concepts/guarantees | T1 | llms-full.txt (curl) | "As of 0.24.0 ... durable" idézet forrása |
| Supported Join Types | https://www.paradedb.com/docs/reference/joins/overview | T1 | llms-full.txt (curl) | Aktuális JOIN-támogatás |
| Indexed Columns (filter pushdown típusok) | https://www.paradedb.com/docs/reference/filtering/indexed | T1 | llms-full.txt (curl) | Típus/operátor táblázat |
| Indexing 32+ Columns | https://www.paradedb.com/docs/reference/indexing/indexing-composite | T1 | llms-full.txt (curl) | 32-oszlopos Postgres-limit és kerülőút |
| docs.paradedb.com/llms-full.txt (teljes doksi-dump) | https://docs.paradedb.com/llms-full.txt | T1 | curl | Grep-elve kulcsszavakra (corrupt, crash, amplif, stb.) |
| Discussion #3521 — BM25 reads on streaming replication standbys | https://github.com/orgs/paradedb/discussions/3521 | T1 | WebFetch | Enterprise-only fizikai replikáció megerősítése |
| Release v0.24.0 | https://github.com/paradedb/paradedb/releases/tag/v0.24.0 | T1 | WebFetch | "Crash recovery via WAL" — durability-váltás dátuma (2025.06.03.) |
| Release v0.19.0 | https://github.com/paradedb/paradedb/releases/tag/v0.19.0 | T1 | WebFetch | Logikai replikáció Community-ben, 2024.10.14. |
| HN — ParadeDB – PostgreSQL for Search | https://news.ycombinator.com/item?id=38847571 | T3 | WebFetch (429, tartalom nem elérhető) | Csak cím/index szinten |
| HN — One of the ParadeDB maintainers here | https://news.ycombinator.com/item?id=44637543 | T3 | WebFetch (429, tartalom nem elérhető) | Csak cím/index szinten |
| Reddit-keresések (több lekérdezés) | — | T3 | WebSearch | Nem hozott releváns találatot |
| GitHub API (api.github.com), repo-scoped | https://api.github.com/repos/paradedb/paradedb | — | curl | "GitHub access to this repository is not enabled for this session" — nem használható |
| web.archive.org (több URL) | — | — | curl / WebFetch | Teljesen blokkolva ebben a környezetben ("Blocked by egress policy" / "Access to this website has been blocked") |



---

# ELL01 — Licenc, kiadás és a cég helyzete
## Meglátogatott linkek

| Cím | URL | Tier | Eszköz |
|---|---|---|---|
| paradedb/paradedb — LICENSE (nyers) | https://raw.githubusercontent.com/paradedb/paradedb/main/LICENSE | T1 | curl |
| paradedb/paradedb — Cargo.toml (nyers) | https://raw.githubusercontent.com/paradedb/paradedb/main/Cargo.toml | T1 | curl |
| paradedb/paradedb — CONTRIBUTING.md (nyers) | https://raw.githubusercontent.com/paradedb/paradedb/main/CONTRIBUTING.md | T1 | curl |
| pg_analytics — LICENSE (nyers) | https://raw.githubusercontent.com/paradedb/pg_analytics/dev/LICENSE | T1 | curl |
| pg_textsearch — LICENSE (nyers) | https://raw.githubusercontent.com/timescale/pg_textsearch/main/LICENSE | T1 | curl |
| pg_textsearch — README.md (nyers) | https://raw.githubusercontent.com/timescale/pg_textsearch/main/README.md | T1 | curl |
| GNU AGPL-3.0 hivatalos szöveg | https://www.gnu.org/licenses/agpl-3.0.txt | T1 | curl |
| GNU GPL FAQ | https://www.gnu.org/licenses/gpl-faq.html | T1 | curl |
| Docker Hub API — paradedb/paradedb tags | https://hub.docker.com/v2/repositories/paradedb/paradedb/tags | T1 | curl (API) |
| GitHub API — releases/latest (403, nem elérhető) | https://api.github.com/repos/paradedb/paradedb/releases/latest | — | curl (sikertelen) |
| GitHub — releases/latest | https://github.com/paradedb/paradedb/releases/latest | T1 | Exa fetch |
| GitHub — paradedb/paradedb főoldal | https://github.com/paradedb/paradedb | T1 | Exa search |
| GitHub — paradedb/pg_analytics | https://github.com/paradedb/pg_analytics | T1 | Exa search |
| GitHub — pg_analytics releases | https://github.com/paradedb/pg_analytics/releases | T1 | Exa search |
| GitHub — pg_analytics v0.3.7 tag | https://github.com/paradedb/pg_analytics/releases/tag/v0.3.7 | T1 | Exa search |
| GitHub — pg_textsearch releases | https://github.com/timescale/pg_textsearch/releases | T1 | Exa fetch |
| GitHub — pg_textsearch v1.4.0 tag | https://github.com/timescale/pg_textsearch/releases/tag/v1.4.0 | T1 | Exa fetch |
| GitHub — pg_textsearch README | https://github.com/timescale/pg_textsearch/blob/main/README.md | T1 | Exa search |
| GitHub issue #6007 — replikáció/standby hiba | https://github.com/paradedb/paradedb/issues/6007 | T1 | Exa search |
| ParadeDB — Enterprise doksi | https://docs.paradedb.com/deploy/enterprise | T1 | Exa fetch |
| ParadeDB — Guarantees doksi | https://docs.paradedb.com/welcome/guarantees | T1 | Exa fetch |
| ParadeDB — Deploy overview | https://www.paradedb.com/docs/deploy/overview | T1 | Exa search |
| ParadeDB — „Why We Picked AGPL" blog | https://www.paradedb.com/blog/agpl | T1 | Exa search |
| ParadeDB — CLA gist (philippemnoel) | https://gist.github.com/philippemnoel/5ba3a20230bc1c3c0ae89caeb0597f4a | T1 | Exa fetch |
| ParadeDB — CLA Assistant oldal | https://cla-assistant.io/paradedb/paradedb | T2 | Exa fetch |
| ParadeDB-dev changelog 0.15.9 (pg_analytics deprecation) | https://paradedb-dev.mintlify.site/changelog/0.15.9 | T2 | Exa search |
| PGXN — pg_search 0.25.9 | https://pgxn.org/dist/pg_search/0.25.9/ | T1/T2 | Exa fetch |
| PGXN — pg_search (index) | https://pgxn.org/dist/pg_search/ | T1/T2 | Exa fetch |
| Neon — changelog 2026-04-03 | https://neon.com/docs/changelog/2026-04-03 | T1 | Exa search |
| Neon — migrate pg_search → lakebase_text | https://neon.com/docs/extensions/migrate-pg-search-to-lakebase-text | T1 | Exa search |
| Neon — pg_search extension doksi | https://neon.com/docs/extensions/pg_search | T1 | Exa search |
| Neon website repo — pg_search.md | https://github.com/neondatabase/website/blob/main/content/docs/extensions/pg_search.md | T1 | Exa search |
| LobeHub GitHub issue — Neon pg_search removal hatása | https://github.com/lobehub/lobehub/issues/18303 | T2 | Exa search |
| Tiger Data — pg_textsearch bejelentő blog | https://www.tigerdata.com/blog/introducing-pg_textsearch-true-bm25-ranking-hybrid-retrieval-postgres | T1 | Exa search |
| Tiger Data — pg_textsearch doksi | https://www.tigerdata.com/docs/use-timescale/latest/extensions/pg-textsearch | T1 | Exa search |
| Hacker News — ParadeDB alapítói komment (AGPL/self-hosting) | https://news.ycombinator.com/item?id=38849928 | T2 | Exa search |
| api-evangelist/paradedb (nem hivatalos, harmadik fél) | https://github.com/api-evangelist/paradedb | T3 (nem használt bizonyítékként) | Exa search |



---

# ELL02 — Helyesség, tartósság, egyidejűség
## Meglátogatott linkek

| Cím | URL | Tier | Eszköz |
|---|---|---|---|
| Issue #1929 — Inconsistent search query results when joining tables | https://github.com/paradedb/paradedb/issues/1929 | T1 | Exa web_fetch_exa |
| Release v0.12.1 | https://github.com/paradedb/paradedb/releases/tag/v0.12.1 | T1 | Exa web_fetch_exa |
| Issue #6375 — Join scan drops one user's rows after HOT update+VACUUM | https://github.com/paradedb/paradedb/issues/6375 | T1 | Exa web_fetch_exa |
| Issue #6394 — Join scan drops the whole row (outer join nullable side) | https://github.com/paradedb/paradedb/issues/6394 | T1 | Exa web_fetch_exa |
| Issue #6108 — Sequential scan fallback returns no rows for NUMERIC key fields | https://github.com/paradedb/paradedb/issues/6108 | T1 | Exa web_fetch_exa |
| Issue #6390 — Base and aggregate scans take no SIREAD locks | https://github.com/paradedb/paradedb/issues/6390 | T1 | Exa web_fetch_exa |
| Issue #6374 — Parallel top-k scan segfaults after two updates | https://github.com/paradedb/paradedb/issues/6374 | T1 | Exa web_fetch_exa |
| PR #6392 — feat: take the read's SIREAD lock in the ParadeDB scans | https://github.com/paradedb/paradedb/pull/6392 | T1 | Exa web_fetch_exa |
| PR #6348 — test: property-test partitioned joins | https://github.com/paradedb/paradedb/pull/6348 | T1 | Exa web_fetch_exa |
| Release v0.24.0 | https://github.com/paradedb/paradedb/releases/tag/v0.24.0 | T1 | Exa web_fetch_exa |
| newreleases.io — v0.24.0 tükör | https://newreleases.io/project/github/paradedb/paradedb/release/v0.24.0 | T3 | Exa web_search_exa |
| PR #4901 — feat: Crash recovery via WAL | https://github.com/paradedb/paradedb/pull/4901 | T1 | Exa web_search_exa |
| Changelog 0.24.0 (Mintlify tükör) | https://docs.paradedb.com/changelog/0.24.0.md | T1 | Exa web_search_exa |
| Upgrading ParadeDB | https://docs.paradedb.com/deploy/upgrading | T1 | Exa web_fetch_exa |
| Blog: A New Postgres Block Storage Layout | https://www.paradedb.com/blog/block-storage-part-one | T1 | Exa web_fetch_exa |
| Guarantees | https://docs.paradedb.com/welcome/guarantees (ill. www.paradedb.com/docs/welcome/guarantees) | T1 | Exa web_search_exa |
| Verify Index Integrity | https://docs.paradedb.com/documentation/indexing/verify-index | T1 | Exa web_search_exa |
| PR #3907 — feat: added amcheck-style index verification for BM25 indexes | https://github.com/paradedb/paradedb/pull/3907 | T1 | Exa web_search_exa |
| PR #4733 — fix: replace deprecated validate_checksum with pdb.verify_index | https://github.com/paradedb/paradedb/pull/4733 | T1 | Exa web_search_exa |
| Load Data from Postgres (pg_dump/pg_restore) | https://docs.paradedb.com/documentation/getting-started/load | T1 | Exa web_search_exa |
| Deploy ParadeDB (pg_search) on a VPS — RamNode | https://www.ramnode.com/guides/paradedb | T3 | Exa web_search_exa |
| PostgreSQL: pg_dump | https://www.postgresql.org/docs/current/app-pgdump.html | T1 | Exa web_search_exa |
| Reindexing | https://docs.paradedb.com/documentation/indexing/reindexing | T1 | Exa web_search_exa |
| Changelog 0.15.0 (pgxn tükör) | https://api.pgxn.org/src/pg_search/pg_search-0.25.9/docs/changelog/0.15.0.mdx | T1 | Exa web_search_exa |
| Changelog 0.22.0 (pgxn tükör) | https://api.pgxn.org/src/pg_search/pg_search-0.25.9/docs/changelog/0.22.0.mdx | T1 | Exa web_search_exa |
| Changelog 0.25.0 (pgxn tükör) | https://api.pgxn.org/src/pg_search/pg_search-0.25.2/docs/changelog/0.25.0.mdx | T1 | Exa web_search_exa |
| Changelog 0.25.1 (pgxn tükör) | https://api.pgxn.org/src/pg_search/pg_search-0.25.2/docs/changelog/0.25.1.mdx | T1 | Exa web_search_exa |
| Release v0.25.9 | https://github.com/paradedb/paradedb/releases/tag/v0.25.9 | T1 | Exa web_fetch_exa |
| Release v0.25.7 | https://github.com/paradedb/paradedb/releases/tag/v0.25.7 | T1 | Exa web_fetch_exa |
| Release v0.26.0 (nem található) | https://github.com/paradedb/paradedb/releases/tag/v0.26.0 | T1 | Exa web_fetch_exa (CRAWL_NOT_FOUND) |
| GitHub Releases lista | https://github.com/paradedb/paradedb/releases | T1 | Exa web_fetch_exa |
| PostgreSQL: Transaction Isolation (13.2, SIREAD) | https://www.postgresql.org/docs/current/transaction-iso.html | T1 | Exa web_search_exa |
| PostgreSQL forráskód — README-SSI | https://github.com/postgres/postgres/blob/master/src/backend/storage/lmgr/README-SSI | T1 | Exa web_search_exa |



---

# ELL03 — Szöveges és vektoros keresés, szűréssel (adverzariális ellenőrzés)
## Meglátogatott linkek

| Cím | URL | Tier | Eszköz |
|---|---|---|---|
| Create an Index | https://www.paradedb.com/docs/reference/indexing/create-index.md | T1 | Exa web_fetch_exa |
| Stemmer | https://www.paradedb.com/docs/reference/token-filters/stemming.md | T1 | Exa web_fetch_exa |
| ASCII Folding | https://www.paradedb.com/docs/reference/token-filters/ascii-folding.md | T1 | Exa web_fetch_exa |
| How Vector Search Works | https://www.paradedb.com/docs/concepts/vector/overview.md | T1 | Exa web_fetch_exa |
| Indexing Vectors | https://www.paradedb.com/docs/reference/indexing/indexing-vectors.md | T1 | Exa web_fetch_exa |
| Limitations & Tradeoffs | https://www.paradedb.com/docs/welcome/limitations.md | T1 | Exa web_fetch_exa |
| Indexed Columns (Filter Pushdown) | https://www.paradedb.com/docs/reference/filtering/indexed.md | T1 | Exa web_fetch_exa |
| Reciprocal Rank Fusion | https://www.paradedb.com/docs/reference/hybrid/rrf.md | T1 | Exa web_fetch_exa |
| Querying Vectors | https://www.paradedb.com/docs/reference/vector/querying.md | T1 | Exa web_fetch_exa |
| Changelog 0.25.0 | https://www.paradedb.com/docs/project/changelog/0.25.0.md | T1 | Exa web_fetch_exa |
| PostgreSQL 18 — 12.3. Controlling Text Search (ts_rank) | https://www.postgresql.org/docs/current/textsearch-controls.html | T1 | Exa web_fetch_exa |
| PostgreSQL 18 — 12.6. Dictionaries | https://www.postgresql.org/docs/current/textsearch-dictionaries.html | T1 | Exa web_fetch_exa |
| PostgreSQL 18 — 12.10. psql Support (\dFd lista) | https://www.postgresql.org/docs/18/textsearch-psql.html | T1 | Exa web_search_exa |
| PostgreSQL 8.3 — psql Support (\dFd lista, 2008) | https://www.postgresql.org/docs/8.3/textsearch-psql.html | T1 | Exa web_search_exa |
| PostgreSQL 8.3 — Release 8.3 (FTS core-ba kerülése) | https://www.postgresql.org/docs/8.3/release-8-3.html | T1 | Exa web_search_exa |
| postgres/postgres — dict_snowball.c | https://github.com/postgres/postgres/blob/master/src/backend/snowball/dict_snowball.c | T1 | Exa web_search_exa |
| pgvector README (master) | https://raw.githubusercontent.com/pgvector/pgvector/master/README.md | T1 | Exa web_fetch_exa |
| paradedb/paradedb — Cargo.toml (tantivy fork pin) | https://github.com/paradedb/paradedb/blob/main/Cargo.toml | T1 | Exa web_search_exa |
| paradedb/tantivy fork — ascii_folding_filter.rs (Ő/ő/Ű/ű, pontos rev) | https://raw.githubusercontent.com/paradedb/tantivy/dcbfce29c74b5d6c6653f3e36471aa2f37a9a79b/src/tokenizer/ascii_folding_filter.rs | T1 | `curl` (nyers fájl, engedélyezett) |
| GitHub — v0.25.0 release (pontos dátum) | https://github.com/paradedb/paradedb/releases/tag/v0.25.0 | T1 | Exa web_search_exa |
| GitHub PR #5613 — pg_search vektor-recall CI-adatok | https://github.com/paradedb/paradedb/pull/5613 | T1 (first-party CI) | Exa web_fetch_exa + web_search_exa |
| GitHub PR #5393 — Cohere recall mérés (ivfflat/hnsw) | https://github.com/paradedb/paradedb/pull/5393 | T1 (first-party CI) | Exa web_search_exa |
| pg_search 0.17.3 similarity/overview.mdx (elavult, saját "vector" típus, 2000 dim) | https://api.pgxn.org/src/pg_search/pg_search-0.17.3/docs/documentation/similarity/overview.mdx | T1 (elavult forrás) | Exa web_search_exa |
| ParadeDB — pgvector Limitations (learn/blog) | https://www.paradedb.com/learn/postgresql/pgvector-limitations | T3 | Exa web_search_exa |
| GitHub issue #892 — pgvector dimenziókorlát dokumentáció-hiány | https://github.com/paradedb/paradedb/issues/892 | T1 | Exa web_search_exa |



---

# ELL04 — TypeScript / Bun / Drizzle / Better Auth ellenőrzés
## Meglátogatott linkek

| Cím | URL | Tier | Eszköz |
|---|---|---|---|
| npm registry — @paradedb/drizzle-paradedb | https://registry.npmjs.org/@paradedb/drizzle-paradedb | T1 | curl (JSON API) |
| npm registry — @paradedb/drizzle-paradedb@0.5.0 | https://registry.npmjs.org/@paradedb/drizzle-paradedb/0.5.0 | T1 | curl (JSON API) |
| drizzle-paradedb CHANGELOG.md | https://raw.githubusercontent.com/paradedb/drizzle-paradedb/main/CHANGELOG.md | T1 | curl (nyers fájl) |
| drizzle-paradedb package.json (main) | https://raw.githubusercontent.com/paradedb/drizzle-paradedb/main/package.json | T1 | curl (nyers fájl) |
| GitHub — paradedb/drizzle-paradedb tags/releases | https://api.github.com/repos/paradedb/drizzle-paradedb/tags | — | curl (hozzáférés megtagadva ebben a sessionben, nem használt forrás) |
| npm registry — drizzle-orm | https://registry.npmjs.org/drizzle-orm | T1 | curl (JSON API) |
| npm registry — drizzle-kit | https://registry.npmjs.org/drizzle-kit | T1 | curl (JSON API) |
| npm registry — better-auth | https://registry.npmjs.org/better-auth | T1 | curl (JSON API) |
| npm registry — better-auth@1.7.5 | https://registry.npmjs.org/better-auth/1.7.5 | T1 | curl (JSON API) |
| npm registry — better-auth@1.6.33 | https://registry.npmjs.org/better-auth/1.6.33 | T1 | curl (JSON API) |
| Drizzle ORM — v1 Roadmap | https://orm.drizzle.team/roadmap | T1 | Exa fetch |
| GitHub issue — drizzle-orm #5660 „when will we have v1.0.0?" | https://github.com/drizzle-team/drizzle-orm/issues/5660 | T1 | Exa fetch |
| GitHub issue — drizzle-orm #1869 (AndriiSherman timeline-üzenete) | https://github.com/drizzle-team/drizzle-orm/issues/1869 | T1 | Exa search |
| GitHub issue — drizzle-orm #4760 (ugyanaz az üzenet, más issue) | https://github.com/drizzle-team/drizzle-orm/issues/4760 | T1 | Exa search |
| drizzle-orm indexes.ts (main) | https://github.com/drizzle-team/drizzle-orm/blob/main/drizzle-orm/src/pg-core/indexes.ts | T1 | Exa search |
| drizzle-orm indexes.ts (korábbi, stabil-korabeli commit) | https://github.com/drizzle-team/drizzle-orm/blob/273c7807/drizzle-orm/src/pg-core/indexes.ts | T1 | Exa search |
| Drizzle ORM — Indexes (mintlify tükördoksi) | https://drizzle-team-drizzle-orm.mintlify.app/schema/indexes | T2 | Exa search |
| Drizzle ORM — PostgreSQL extensions | https://orm.drizzle.team/docs/extensions/pg | T1 | Exa fetch |
| Drizzle ORM — Vector similarity search guide | https://orm.drizzle.team/docs/guides/vector-similarity-search | T1 | Exa fetch |
| GitHub issue — drizzle-orm #2935 „generate ignores index operators" | https://github.com/drizzle-team/drizzle-orm/issues/2935 | T1 | Exa fetch |
| Better Auth — Drizzle adapter changelog | https://github.com/better-auth/better-auth/blob/main/packages/better-auth/CHANGELOG.md | T1 | Exa search |
| Better Auth — drizzle-adapter changelog (1.7.0) | https://github.com/better-auth/better-auth/blob/c3688ba/packages/drizzle-adapter/CHANGELOG.md | T1 | Exa search |
| Better Auth — PR #10501 (peer-range igazítás) | https://github.com/better-auth/better-auth/pull/10501 | T1 | Exa search |
| Better Auth — v1.7.0 release | https://github.com/better-auth/better-auth/releases/tag/v1.7.0 | T1 | Exa search |
| Better Auth blog — „Better Auth 1.7" | https://better-auth.com/blog/1-7 | T1 | Exa search |
| Dosu/Devin — „Drizzle ORM v1 Compatibility" összefoglaló | https://app.dosu.dev/cdda13d9-dd27-4d31-b09a-5d8bec92de21/documents/d44cb4d1-c83b-43d5-998a-c0a6dec2b641 | T3 | Exa search (csak tájékozódásra, elsődleges forrásokkal ellenőrizve) |
| Bun — főoldal (benchmark, „Bun in production") | https://bun.com/ | T1 | Exa search |
| Bun — SQL dokumentáció (docs/runtime/sql.mdx) | https://github.com/oven-sh/bun/blob/88a63988/docs/runtime/sql.mdx | T1 | Exa search |
| GitHub issue — oven-sh/bun #15088 „Bun.sql tracking issue" | https://github.com/oven-sh/bun/issues/15088 | T1 | Exa search |
| GitHub issue — oven-sh/bun #32004 (pool stall) | https://github.com/oven-sh/bun/issues/32004 | T1 | Exa search |
| GitHub PR — oven-sh/bun #32772 (redundant Sync javítás) | https://github.com/oven-sh/bun/pull/32772 | T1 | Exa search |
| GitHub issue — oven-sh/bun #33665 (prepared statement cache hiba) | https://github.com/oven-sh/bun/issues/33665 | T1 | Exa search |
| GitHub issue — oven-sh/bun #15438 (postgres-js hang, lezárt) | https://github.com/oven-sh/bun/issues/15438 | T1 | (idézve `sq06.md`-ből, nem újra-olvasva) |
| Bun — SQLite dokumentáció | https://bun.com/docs/runtime/sqlite.md | T1 | Exa search |
| Bun — Database.loadExtension referencia | https://bun.com/reference/bun/sqlite/Database/loadExtension | T1 | Exa search |
| GitHub issue — oven-sh/bun #38647 (macOS statikus SQLite kérés) | https://github.com/oven-sh/bun/issues/38647 | T1 | Exa fetch |
| GitHub issue — oven-sh/bun #38772 (ua., duplikátum) | https://github.com/oven-sh/bun/issues/38772 | T1 | Exa fetch |
| GitHub issue — oven-sh/bun #16717 (SQLite version is incorrect, nyitva) | https://github.com/oven-sh/bun/issues/16717 | T1 | Exa fetch |
| GitHub issue — oven-sh/bun #31247 (macOS SQLite 3.43.2 vs 3.53.0) | https://github.com/oven-sh/bun/issues/31247 | T1 | Exa fetch |
| GitHub PR — oven-sh/bun #31249 („ai slop", lezárt, nem mergelt) | https://github.com/oven-sh/bun/pull/31249 | T1 | Exa fetch |
| GitHub PR — oven-sh/bun #31293 (static SQLite alapérték, mergelve) | https://github.com/oven-sh/bun/pull/31293 | T1 | Exa fetch |
| GitHub issue — asg017/sqlite-vec #78 (macOS kerülőút) | https://github.com/asg017/sqlite-vec/issues/78 | T1 | Exa search |
| sqlite-vec — site/using/js.md (hivatalos használati doksi) | https://github.com/asg017/sqlite-vec/blob/main/site/using/js.md | T1 | Exa search |



---

# ELL05 — Összevetési alap: sima Postgres + pgvector, ParadeDB nélkül
## Meglátogatott linkek

| Cím | URL | Tier | Eszköz |
|---|---|---|---|
| PostgreSQL 18 Docs — 12.6. Dictionaries (Snowball) | https://www.postgresql.org/docs/current/textsearch-dictionaries.html | T1 | web_search_exa |
| PostgreSQL 18 Docs — 12.10. psql Support (`\dFd` hungarian_stem lista) | https://www.postgresql.org/docs/18/textsearch-psql.html | T1 | web_search_exa |
| PostgreSQL Docs — F.48. unaccent | https://www.postgresql.org/docs/current/unaccent.html | T1 | web_search_exa |
| pgsty/pgext — unaccent.md (közösségi extension-katalógus) | https://github.com/pgsty/pgext/blob/dd1d49ca8606fd0962ccd602ea1ed59cbdba1b6a/content/e/unaccent.md | T2/T3 | web_search_exa |
| PostgreSQL Docs — 12.3. Controlling Text Search (ts_rank/ts_rank_cd) | https://www.postgresql.org/docs/current/textsearch-controls.html | T1 | web_search_exa |
| PostgreSQL Docs — 9.13. Text Search Functions and Operators | https://www.postgresql.org/docs/18/functions-textsearch.html | T1 | web_search_exa |
| postgres/postgres — src/backend/utils/adt/tsrank.c | https://github.com/postgres/postgres/blob/92268b35d04c2de416279f187d12f264afa22614/src/backend/utils/adt/tsrank.c | T1 | web_search_exa |
| pg_fts 0.2.0 (PGXN) | https://pgxn.org/dist/pg_fts/0.2.0/ | T3 | web_search_exa |
| Tigerdata blog — From ts_rank to BM25. Introducing pg_textsearch | https://www.tigerdata.com/blog/introducing-pg_textsearch-true-bm25-ranking-hybrid-retrieval-postgres | T2 (gyártói) | web_search_exa |
| postgresql.org hír — pg_textsearch v1.0 GA | https://www.postgresql.org/about/news/pg_textsearch-v10-3264/ | T1 | web_search_exa |
| timescale/pg_textsearch (GitHub repó, README/státusz/licenc) | https://github.com/timescale/pg_textsearch | T1 | web_search_exa |
| timescale/pg_textsearch — Releases lista | https://github.com/timescale/pg_textsearch/releases | T1 | web_search_exa |
| timescale/pg_textsearch — v1.4.0 release | https://github.com/timescale/pg_textsearch/releases/tag/v1.4.0 | T1 | web_search_exa |
| timescale/pg_textsearch — v0.6.0 release (MS-MARCO benchmark) | https://github.com/timescale/pg_textsearch/releases/tag/v0.6.0 | T1 | web_search_exa |
| timescale docs — use-timescale/extensions/pg-textsearch.md | https://github.com/timescale/docs/blob/latest/use-timescale/extensions/pg-textsearch.md | T2 | web_search_exa |
| PostgreSQL Docs — 12.5. Parsers (token-típusok táblázata) | https://www.postgresql.org/docs/current/textsearch-parsers.html | T1 | web_search_exa |
| PostgreSQL Docs — 12.8. Testing and Debugging Text Search (ts_token_type) | https://www.postgresql.org/docs/18/textsearch-debugging.html | T1 | web_search_exa |
| Stack Overflow — Postgres FTS with Hyphen and Numerals (`abc-001` ts_debug) | https://stackoverflow.com/questions/57795085/postgres-full-text-search-with-hyphen-and-numerals | T3 | web_search_exa |
| postgresql.org levelezőlista — Text search lexer's handling of hyphens and negatives | https://www.postgresql.org/message-id/CAAmRUjt8XNGWKUiPA3uQ6%2B7UaPTNOsrfQVF-gPcS9zZnM5PW3Q%40mail.gmail.com | T2 | web_search_exa |
| postgrespro.com — ua. levelezőlista-tükör, dict-int válasz | https://postgrespro.com/list/id/abf85423-ce4b-45ec-97a4-2789a400ed55@manitou-mail.org | T2 | web_search_exa |
| postgresql.org — pgsql commit log: hyphenated word parsing change (2007) | https://www.postgresql.org/message-id/20071027190345.A5D1E754229%40cvs.postgresql.org | T1 | web_search_exa |
| postgresql.org — wparser misbehavior for hyphenated words (Tom Lane, 2007) | https://www.postgresql.org/message-id/6269.1193184058%40sss.pgh.pa.us | T1 | web_search_exa |
| postgresql.org — BUG #17562: Strange behavior of to_tsquery() with `-` | https://www.postgresql.org/message-id/17562-7c786bed7effbace%40postgresql.org | T1 | web_search_exa |
| dba.stackexchange — hyphen in tsquery not found (PG14 fix) | https://dba.stackexchange.com/questions/302750/why-tsquery-containing-a-hyphen-isnt-found-in-full-text-search | T3 | web_search_exa |
| Stack Overflow — escaping underscores in tsquery | https://stackoverflow.com/questions/59727819/how-to-escape-underscores-in-while-preparing-tsquery-for-postgresql-full-text-se | T3 | web_search_exa |
| mattermost-server GitHub issue #14436 — underscore search | https://github.com/mattermost/mattermost-server/issues/14436 | T3 | web_search_exa |
| PostgreSQL Docs — F.35. pg_trgm | https://www.postgresql.org/docs/current/pgtrgm.html | T1 | web_search_exa |
| postgres/postgres — doc/src/sgml/pgtrgm.sgml | https://github.com/postgres/postgres/blob/master/doc/src/sgml/pgtrgm.sgml | T1 | web_search_exa |
| pgvector/pgvector — README.md (Hybrid Search, RRF) | https://github.com/pgvector/pgvector/blob/master/README.md | T1 | web_search_exa |
| Supabase Docs — Hybrid search (RRF SQL-minta) | https://supabase.com/docs/guides/ai/hybrid-search | T2 | web_search_exa |
| Jonathan Katz — Hybrid search with PostgreSQL and pgvector | https://jkatz.github.io/post/postgres/hybrid-search-postgres-pgvector/ | T2 | web_search_exa |
| learnbackend.com — Hybrid Search in Postgres: pgvector + Full-Text | https://learnbackend.com/guides/hybrid-search-postgres-bm25-pgvector/ | T3 | web_search_exa |
| Vineeth Pothulapati — PostgreSQL vs ParadeDB: A Search Comparison (teljes cikk lekérve) | https://www.vineeth.fyi/blog/pg-vs-pg-search/ | T2/T3 (l. függetlenségi megjegyzés) | web_fetch_exa |
| Vineeth Pothulapati — About me | https://www.vineeth.fyi/about/ | T3 (önbevallott) | web_search_exa |
| LinkedIn — Vineeth Pothulapati poszt (TigerData munkaviszony, 2025.06.19) | https://www.linkedin.com/posts/vineeth-pothulapati_speed-without-sacrifice-building-the-modern-activity-7341450784372310016-ZLEI | T3 | web_search_exa |
| Tordai & de Rijke — Four Stemmers and a Funeral (CLEF 2005, LNCS 4022) | https://staff.fnwi.uva.nl/m.derijke/wp-content/papercite-data/pdf/tordai-four-2006.pdf | T2 | web_search_exa |
| Endrédy István — Corpus based evaluation of stemmers (2015) | https://real.mtak.hu/34378/1/ei_corpus_eval_of_stemmers_ltc_u.pdf | T2 | web_search_exa |
| damesek/hustem GitHub repó (Hunspell vs Snowball hibaarány) | https://github.com/damesek/hustem | T3 | web_search_exa |
| Szabó & Kovács — Benchmarking morphological analyzers for Hungarian | https://scispace.com/pdf/benchmarking-morphological-analyzers-for-the-hungarian-l9mpaewmno.pdf | T2 | web_search_exa |
| gist.github.com/1883375 — valós Postgres `SHOW ALL` (hu_HU, hungarian config) | https://gist.github.com/1883375 | T3 | web_search_exa |
| postgrespro.ru levelezőlista-tükör — hu_HU szerverkonfiguráció | https://postgrespro.ru/list/thread-id/2062481 | T2 | web_search_exa |
| postgres/postgres — src/backend/tsearch/wparser_def.c (token-kategória konstansok) | https://github.com/postgres/postgres/blob/master/src/backend/tsearch/wparser_def.c | T1 | web_fetch_exa |

---

# ELL06 — Mentés és migráció Postgres + ParadeDB alatt
## Meglátogatott linkek

| Cím | URL | Tier | Eszköz |
|---|---|---|---|
| PostgreSQL Documentation: 18: 25.1. SQL Dump | https://www.postgresql.org/docs/current/backup-dump.html | 1 (hivatalos) | web_search_exa |
| PostgreSQL Documentation: 18: pg_dump | https://www.postgresql.org/docs/18/app-pgdump.html | 1 (hivatalos) | web_search_exa |
| PostgreSQL Documentation: 15: pg_dump | https://www.postgresql.org/docs/15/app-pgdump.html | 1 (hivatalos) | web_search_exa |
| PostgreSQL Documentation: 16: 26.1. SQL Dump | https://www.postgresql.org/docs/16/backup-dump.html | 1 (hivatalos) | web_search_exa |
| PostgreSQL Documentation: current: CREATE INDEX | https://www.postgresql.org/docs/current/sql-createindex.html | 1 (hivatalos) | web_search_exa |
| PostgreSQL Documentation: current: CREATE DATABASE | https://www.postgresql.org/docs/current/sql-createdatabase.html | 1 (hivatalos) | web_search_exa |
| PostgreSQL Documentation: 19: Routine Vacuuming | https://www.postgresql.org/docs/19/routine-vacuuming.html | 1 (hivatalos) | web_search_exa |
| Transactional DDL in PostgreSQL: A Competitive Analysis (PG wiki) | https://wiki.postgresql.org/wiki/Transactional_DDL_in_PostgreSQL:_A_Competitive_Analysis | 1 (hivatalos wiki) | web_search_exa |
| Why PostgreSQL Instead of MySQL 2009 (PG wiki) | https://wiki.postgresql.org/wiki/Why_PostgreSQL_Instead_of_MySQL_2009 | 1 (hivatalos wiki) | web_search_exa |
| git.postgresql.org commitdiff (ALTER TYPE ADD VALUE doksi-változás) | http://git.postgresql.org/pg/commitdiff/15bc038f9bcd1a9af3f625caffafc7c20322202d | 1 (hivatalos forráskód/doksi-diff) | web_search_exa |
| Stack Overflow: ALTER TYPE … ADD cannot run inside a transaction block | https://stackoverflow.com/questions/53149484/error-alter-type-add-cannot-run-inside-a-transaction-block | 2 (közösségi, forráskódot idéz) | web_search_exa |
| postgres/postgres heapam_visibility.c (GitHub) | https://github.com/postgres/postgres/blob/e18b0cb7/src/backend/access/heap/heapam_visibility.c | 1 (hivatalos forráskód) | web_search_exa |
| drizzle-orm pg-core/dialect.ts (GitHub) | https://github.com/drizzle-team/drizzle-orm/blob/6276f5c9a94b1bb6d109b990982243d2b13e5f88/drizzle-orm/src/pg-core/dialect.ts | 1 (hivatalos forráskód) | web_search_exa |
| drizzle-orm node-postgres/migrator.ts (GitHub) | https://github.com/drizzle-team/drizzle-orm/blob/48e54060/drizzle-orm/src/node-postgres/migrator.ts | 1 (hivatalos forráskód) | web_search_exa |
| drizzle-orm postgres-js/migrator.ts (GitHub) | https://github.com/drizzle-team/drizzle-orm/blob/48e54060/drizzle-orm/src/postgres-js/migrator.ts | 1 (hivatalos forráskód) | web_search_exa |
| ParadeDB: Load Data from Postgres | https://docs.paradedb.com/documentation/getting-started/load | 1 (hivatalos) | web_search_exa |
| ParadeDB: Create an Index | https://docs.paradedb.com/documentation/indexing/create-index.md | 1 (hivatalos) | web_fetch_exa |
| ParadeDB create-index.mdx (GitHub, v0.25.2) | https://github.com/paradedb/paradedb/blob/v0.25.2/docs/documentation/indexing/create-index.mdx | 1 (hivatalos forrás) | web_search_exa |
| ParadeDB: Filtering | https://docs.paradedb.com/documentation/filtering | 1 (hivatalos) | web_fetch_exa |
| ParadeDB indexing-vectors.mdx (GitHub, v0.25.2) | https://github.com/paradedb/paradedb/blob/v0.25.2/docs/documentation/indexing/indexing-vectors.mdx | 1 (hivatalos forrás) | web_search_exa |
| ParadeDB vector/overview | https://docs.paradedb.com/documentation/vector/overview | 1 (hivatalos) | web_search_exa |
| ParadeDB vector/querying.mdx (GitHub, v0.25.2) | https://github.com/paradedb/paradedb/blob/v0.25.2/docs/documentation/vector/querying.mdx | 1 (hivatalos forrás) | web_search_exa |
| ParadeDB: Reindexing | https://docs.paradedb.com/documentation/indexing/reindexing | 1 (hivatalos) | web_search_exa |
| ParadeDB legacy: Create an Index | https://docs.paradedb.com/legacy/indexing/create-index | 1 (hivatalos) | web_search_exa |
| ParadeDB changelog 0.13.0 | https://paradedb-dev.mintlify.app/changelog/0.13.0 | 1 (hivatalos) | web_search_exa |
| ParadeDB v0.10.0 release notes (GitHub) | https://github.com/paradedb/paradedb/releases/tag/v0.10.0 | 1 (hivatalos) | web_search_exa |
| ParadeDB deploy/self-hosted/extension | https://docs.paradedb.com/deploy/self-hosted/extension | 1 (hivatalos) | web_search_exa |
| pg_search-0.25.6 extension.mdx (pgxn tükör) | https://api.pgxn.org/src/pg_search/pg_search-0.25.6/docs/deploy/self-hosted/extension.mdx | 1 (hivatalos tartalom, tükrözve) | web_search_exa |
| ParadeDB deploy/self-hosted/high-availability | https://docs.paradedb.com/deploy/self-hosted/high-availability | 1 (hivatalos) | web_search_exa |
| ParadeDB deploy/logical-replication/getting-started | https://docs.paradedb.com/deploy/logical-replication/getting-started | 1 (hivatalos) | web_search_exa |
| GitHub issue #1076 (extension átnevezés pg_bm25→pg_search) | https://github.com/paradedb/paradedb/issues/1076 | 1 (hivatalos GitHub) | web_search_exa |
| GitHub PR #5310 (hiányos ALTER EXTENSION UPDATE migrációk) | https://github.com/paradedb/paradedb/pull/5310 | 1 (hivatalos GitHub) | web_search_exa |
| GitHub issue #1579 (tantivy index path OID-ütközés) | https://github.com/paradedb/paradedb/issues/1579 | 1 (hivatalos GitHub) | web_search_exa |
| GitHub PR #1651 (tantivy fájlok törlése DROP INDEX-en) | https://github.com/paradedb/paradedb/pull/1651 | 1 (hivatalos GitHub) | web_search_exa |
| GitHub PR #1413 (CREATE INDEX művelet bgwriterre mozgatása) | https://github.com/paradedb/paradedb/pull/1413 | 1 (hivatalos GitHub) | web_search_exa |
| GitHub issue #1407 (bm25 index újralétrehozási hiba) | https://github.com/paradedb/paradedb/issues/1407 | 1 (hivatalos GitHub) | web_search_exa |
| GitHub issue #2091 (VACUUM hiba BM25 index mellett) | https://github.com/paradedb/paradedb/issues/2091 | 1 (hivatalos GitHub) | web_search_exa |
| GitHub issue #2195 (pg_dump hiba, pg_analytics miatt) | https://github.com/paradedb/paradedb/issues/2195 | 1 (hivatalos GitHub) | web_search_exa |
| GitHub pg_search/README.md (main) | https://github.com/paradedb/paradedb/blob/main/pg_search/README.md | 1 (hivatalos GitHub) | web_search_exa |
| RamNode: Deploy ParadeDB (pg_search) on a VPS | https://ramnode.com/guides/paradedb | 2 (harmadik fél, nem hivatalos) | web_search_exa |
| RamNode: Postgres Superstack — ParadeDB pg_search | https://ramnode.com/guides/series/postgres-superstack/paradedb | 2 (harmadik fél, nem hivatalos) | web_search_exa |
| Stack Overflow: Create and use an index inside a transaction | https://stackoverflow.com/questions/76323576/create-and-use-an-index-inside-a-transaction | 2 (közösségi) | web_search_exa |
| migrationpilot.dev: ALTER TYPE … ADD VALUE in a transaction | https://migrationpilot.dev/handbook/enum-add-value-in-transaction | 2 (harmadik fél, technikai kézikönyv) | web_search_exa |
| Hacker News: Don't rely on IF NOT EXISTS for concurrent index creation | https://news.ycombinator.com/item?id=41228022 | 3 (fórum, kontextusnak) | web_search_exa |
| JasperFx/marten issue #1042 (CONCURRENTLY tranzakcióban hiba) | https://github.com/JasperFx/marten/issues/1042 | 2 (közösségi, valós hibaüzenettel) | web_search_exa |

---

# ELL07 — Adatlap-ellenőrzőösszeg (data checksums) Postgresben és a ParadeDB képein
## Meglátogatott linkek

| Cím | URL | Tier | Eszköz |
|---|---|---|---|
| PostgreSQL 18.0 Release Notes | https://www.postgresql.org/docs/release/18.0/ | 1 (hivatalos PG doksi) | web_search_exa |
| PostgreSQL 18 Released! (hivatalos hír) | https://www.postgresql.org/about/news/postgresql-18-released-3142/ | 1 | web_search_exa |
| PostgreSQL 18 Beta 1 Released! | https://www.postgresql.org/about/news/postgresql-18-beta-1-released-3070/ | 1 | web_search_exa |
| initdb — Documentation: 18 | https://www.postgresql.org/docs/18/app-initdb.html | 1 | web_search_exa |
| 28.2. Data Checksums — Documentation: 18 | https://www.postgresql.org/docs/18/checksums.html | 1 | web_search_exa |
| initdb — Documentation: 17 | https://www.postgresql.org/docs/17/app-initdb.html | 1 | web_search_exa |
| initdb — Documentation: 16 | https://www.postgresql.org/docs/16/app-initdb.html | 1 | web_search_exa + web_fetch_exa |
| initdb — Documentation: 15 | https://www.postgresql.org/docs/15/app-initdb.html | 1 | web_fetch_exa |
| pg_checksums — Documentation: 18 | https://www.postgresql.org/docs/18/app-pgchecksums.html | 1 | web_search_exa |
| pg_checksums — Documentation: 19 (devel funkció) | https://www.postgresql.org/docs/19/app-pgchecksums.html | 1 | web_search_exa |
| 28.2. Data Checksums — Documentation: 19 | https://www.postgresql.org/docs/19/checksums.html | 1 | web_search_exa |
| pg_checksums — Documentation: devel | https://www.postgresql.org/docs/devel/app-pgchecksums.html | 1 | web_search_exa |
| pg_checksums.c forráskód (doxygen) | https://doxygen.postgresql.org/pg__checksums_8c_source.html | 1 (PG forráskód) | web_search_exa |
| pg_amcheck — Documentation: current | https://www.postgresql.org/docs/current/app-pgamcheck.html | 1 | web_search_exa |
| F.1. amcheck — Documentation: current | https://www.postgresql.org/docs/current/amcheck.html | 1 | web_search_exa |
| pgsql-hackers levelezőlista: data_checksums enabled by default | https://www.postgresql.org/message-id/20210107211433.GS27507%40tamriel.snowman.net | 1 (hivatalos PG levlista) | web_search_exa |
| paradedb/paradedb Docker Hub cimkelista | https://hub.docker.com/r/paradedb/paradedb/tags | 1 (gyártói Docker Hub) | web_search_exa |
| paradedb/paradedb Docker Hub főoldal | https://hub.docker.com/r/paradedb/paradedb | 1 | web_search_exa |
| ParadeDB Docker doksi (latest = PG18) | https://docs.paradedb.com/deploy/self-hosted/docker | 1 (gyártói doksi) | web_fetch_exa |
| ParadeDB Docker Upgrading doksi | https://docs.paradedb.com/deploy/upgrading | 1 | web_search_exa |
| Dockerfile.paradedb-18 (main ág, nyers) | https://raw.githubusercontent.com/paradedb/paradedb/main/docker/Dockerfile.paradedb-18 | 1 (forráskód) | web_fetch_exa |
| Dockerfile.paradedb-18 (GitHub blob) | https://github.com/paradedb/paradedb/blob/main/docker/Dockerfile.paradedb-18 | 1 | web_fetch_exa |
| Régi docker/Dockerfile (Bitnami korszak) | https://github.com/paradedb/paradedb/blob/149f66db5cf691431797f59946343c15ab042850/docker/Dockerfile | 1 | web_search_exa |
| PR #1436: Bitnami → hivatalos postgres image váltás | https://github.com/paradedb/paradedb/pull/1436 | 1 | web_search_exa |
| PR #4225: bookworm → trixie alapkép váltás | https://github.com/paradedb/paradedb/pull/4225 | 1 | web_search_exa |
| Issue #429: PG16 alapértelmezetté tétele | https://github.com/paradedb/paradedb/issues/429 | 1 | web_search_exa |
| postgres hivatalos Docker image doksi (POSTGRES_INITDB_ARGS) | https://hub.docker.com/_/postgres | 1 (Docker Official Image doksi) | web_search_exa |
| docker-library/docs postgres README (POSTGRES_INITDB_ARGS) | https://github.com/docker-library/docs/blob/master/postgres/README.md | 1 | web_search_exa |
| pg_search README (main ág) | https://github.com/paradedb/paradedb/blob/main/pg_search/README.md | 1 (gyártói repo) | web_search_exa |
| pg_search README (v0.25.2 tag) | https://github.com/paradedb/paradedb/blob/v0.25.2/pg_search/README.md | 1 | web_search_exa |
| ParadeDB self-hosted extension telepítési doksi | https://docs.paradedb.com/deploy/self-hosted/extension | 1 | web_search_exa |
| pg_search-0.25.6 extension.mdx (tükrözött doksi) | https://api.pgxn.org/src/pg_search/pg_search-0.25.6/docs/deploy/self-hosted/extension.mdx | 2 (mirror a hivatalos doksiról) | web_search_exa |
| Issue #2723: PG18 támogatás bevezetése (v0.21.0) | https://github.com/paradedb/paradedb/issues/2723 | 1 | web_search_exa |
| ParadeDB verify-index doksi (pdb.verify_index) | https://docs.paradedb.com/documentation/indexing/verify-index | 1 (gyártói doksi) | web_search_exa |
| PR #3907: pdb.verify_index bevezetése | https://github.com/paradedb/paradedb/pull/3907 | 1 | web_search_exa |
| paradedb/charts (Helm chart, PG18 alapértelmezett) | https://github.com/paradedb/charts | 1 | web_search_exa |
| dba.stackexchange: miért nincs alapból checksum | https://dba.stackexchange.com/questions/328050/why-is-postgresql-data-checksums-not-enabled-by-default | 3 (közösségi, csak kontextusnak) | web_search_exa |
| openbsd ports README-server | https://github.com/openbsd/ports/blob/master/databases/postgresql/pkg/README-server | 2 (harmadik féltől, megerősítő) | web_search_exa |
