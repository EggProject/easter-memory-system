# Linkek — sq01 (CJK / szóköz nélküli írásrendszerek a szöveges keresésben)

Minden T1-forrás nyers HTML/PDF-lekéréssel lett ellenőrizve (`curl`, nem WebFetch-összefoglaló), a `sqlite.org`-tippnek megfelelően és általánosítva minden hivatalos domainre, ahol a WebFetch AI-összefoglalója gyanúsnak tűnt.

## T1 — hivatalos dokumentáció / forráskód / peer-reviewed

| # | Cím | URL | Lekérés módja |
|---|---|---|---|
| 1 | SQLite FTS5 Extension (hivatalos doksi) | https://www.sqlite.org/fts5.html | nyers `curl` |
| 2 | SQLite FTS3/FTS4 Extension (hivatalos doksi, ICU tokenizáló innen) | https://www.sqlite.org/fts3.html | nyers `curl` |
| 3 | SQLite hivatalos GitHub-tükör, ICU extension README | https://raw.githubusercontent.com/sqlite/sqlite/master/ext/icu/README.txt | nyers `curl` |
| 4 | SQLite Release 3.34.0 (trigram bekerülésének dátuma) | https://www.sqlite.org/releaselog/3_34_0.html | nyers `curl` |
| 5 | PostgreSQL hivatalos doksi — Text Search Limitations | https://www.postgresql.org/docs/current/textsearch-limitations.html | WebFetch |
| 6 | PostgreSQL hivatalos doksi — Text Search Parsers | https://www.postgresql.org/docs/current/textsearch-parsers.html | nyers `curl` (WebFetch is ellenőrizve, egyezett) |
| 7 | PostgreSQL hivatalos doksi — pg_trgm | https://www.postgresql.org/docs/current/pgtrgm.html | nyers `curl` |
| 8 | OpenSearch hivatalos doksi — CJK analyzer | https://docs.opensearch.org/latest/analyzers/language-analyzers/cjk/ | nyers `curl` (első WebFetch-próbálkozás hiányos tartalmat adott vissza — ld. `gaps.md`) |
| 9 | Elastic hivatalos doksi — kuromoji analyzer | https://www.elastic.co/docs/reference/elasticsearch/plugins/analysis-kuromoji-analyzer | nyers `curl` |
| 10 | Elastic hivatalos doksi — kuromoji plugin (fő oldal) | https://www.elastic.co/docs/reference/elasticsearch/plugins/analysis-kuromoji | nyers `curl` |
| 11 | Elastic hivatalos doksi — Smart Chinese analysis plugin | https://www.elastic.co/docs/reference/elasticsearch/plugins/analysis-smartcn | nyers `curl` |
| 12 | Elastic hivatalos blog — Nori (koreai) plugin bejelentés | https://www.elastic.co/blog/nori-the-official-elasticsearch-plugin-for-korean-language-analysis | nyers `curl` |
| 13 | Meilisearch hivatalos doksi — Tokenization | https://www.meilisearch.com/docs/learn/advanced/tokenization | WebFetch |
| 14 | Meilisearch hivatalos GitHub — charabia tokenizáló könyvtár | https://github.com/meilisearch/charabia | (hivatkozva, tartalom a #13-ból) |
| 15 | Typesense hivatalos doksi — Locale | https://typesense.org/docs/guide/locale.html | WebFetch |
| 16 | arXiv — M3-Embedding (BGE-M3) cikk, absztrakt oldal | https://arxiv.org/abs/2402.03216 | nyers `curl` |
| 17 | arXiv — M3-Embedding (BGE-M3) teljes szöveg (HTML), MIRACL táblázat forrása | https://arxiv.org/html/2402.03216v2 | nyers `curl` |
| 18 | ACL Anthology — M3-Embedding (peer-reviewed publikáció, Findings of ACL 2024) | https://aclanthology.org/2024.findings-acl.137/ | csak hivatkozva (a tartalmat az arXiv-verzióból dolgoztuk fel) |
| 19 | arXiv — Multilingual E5 Text Embeddings: A Technical Report | https://arxiv.org/abs/2402.05672 | nyers `curl` (csak absztrakt-szintig dolgozva fel, ld. gaps) |
| 20 | Springer — McNamee & Mayfield, "Character N-Gram Tokenization for European Language Text Retrieval" | https://link.springer.com/article/10.1023/B:INRT.0000009441.78971.be | WebFetch (csak absztrakt, teljes szöveg fizetőfal mögött) |
| 21 | ICU hivatalos oldal — ICU4C Footprint | https://icu.unicode.org/charts/icu4c-footprint | nyers `curl` (megjegyzés: régi, ICU~3.0-hoz tartozó adatok) |

## T2 — megbízható másodlagos / konkrét technikai tartalommal bíró projekt-dokumentáció

| # | Cím | URL | Megjegyzés |
|---|---|---|---|
| 22 | GitHub — pg_bigm hivatalos repó (NTT eredetű PostgreSQL-kiegészítő) | https://github.com/pgbigm/pg_bigm | README |
| 23 | GitHub — pg_bigm hivatalos dokumentáció (angol), pg_trgm-összehasonlító táblázat | https://raw.githubusercontent.com/pgbigm/pg_bigm/REL1_2_STABLE/docs/pg_bigm_en.md | nyers `curl` |
| 24 | GitHub — streetwriters/sqlite-better-trigram | https://github.com/streetwriters/sqlite-better-trigram | README, CJK-specifikus indoklás |
| 25 | andrewmara.com blog — "Faster SQLite LIKE Queries Using FTS5 Trigram Indexes" | https://andrewmara.com/blog/faster-sqlite-like-queries-using-fts5-trigram-indexes/ | konkrét méret/sebesség-mérés, 18,2M soros adathalmaz |

## T3 — fórum, blog, egyedi anekdota (NEM tekintendő elsődleges bizonyítéknak)

| # | Cím | URL | Megjegyzés |
|---|---|---|---|
| 26 | SQLite hivatalos fórum — "Trigram indexes for SQLite" (2020) | https://sqlite.org/forum/forumpost/c230760fdf?t=h | Hivatalos domain, de fórumbejegyzés → T3 a szabály szerint. A trigram tokenizáló eredettörténete (Simon Willison kérése, Dan Kennedy megvalósítása). |
| 27 | GitHub — simonw/sqlite-fts5-trigram (ma már elavult repó) | https://github.com/simonw/sqlite-fts5-trigram | Megerősíti, hogy a trigram funkció a 3.34.0-ban lett hivatalos |
| 28 | dev.to — "SQLite FTS5 won't tokenize Chinese — here's the 7-line bigram fix that did" | https://dev.to/foxck016077/sqlite-fts5-wont-tokenize-chinese-heres-the-7-line-bigram-fix-that-did-4fcc | Gyakorlati anekdota, kb. 2×-es DB-méretnövekedés egyedi bigram-megoldással |
| 29 | GitHub issue — NousResearch/hermes-agent #43690 ("FTS5 Trigram Index Bloat") | https://github.com/NousResearch/hermes-agent/issues/43690 | Egyedi eset, 18,3×-os méretnövekedés strukturált JSON-adaton — a szerző maga jelzi, hogy ez torzított/szélsőséges eset |

## Keresett, de fel nem használt / nem elérhető források

- `courses.cs.umbc.edu/graduate/CMSC676/umbconly/McNameeMayfield.pdf` — 403 Forbidden, nem sikerült elérni a teljes cikket.
- Academia.edu / ResearchGate tükrök a McNamee & Mayfield cikkhez — nem próbáltuk ki (idő-/tool-korlát), a Springer-absztrakt elegendőnek bizonyult a fő állítás idézéséhez.
