# Keresések — minden lefuttatott lekérdezés szó szerint

Kampány: `kereses-indexeles` · 2026-09-08

> Al-kérdésenként bontva, ahogy a kereső ügynökök rögzítették.


---

## SQ-01 — Hol szűrjön a jogosultság a keresésben

# SQ-01 — Lefuttatott keresések

Keresőmotor: WebSearch (US-only index) + WebFetch (oldal-tartalom kinyerés kis modellel).
Dátum: 2026-09-08.

## Előszűrés / utószűrés alapfogalmak
1. `pre-filtering vs post-filtering vector search hybrid definition`
2. `HNSW pre-filtering recall degradation benchmark "filtered vector search"`
3. `post-filtering top-k fewer results oversampling over-fetch vector database`
4. `Qdrant documentation "exact" pre-filtering default HNSW payload index filterable`

## Top-k probléma, over-fetch, iteratív újrakérés
5. `Pinecone metadata filter "fewer than top_k" OR "fewer results than requested" documentation`
6. `langchain fetch_k oversampling filter vectorstore documentation`
7. `oversampling factor vector search recall documentation Vertex AI OR Azure "oversample"`
8. `pgvector 0.8.0 iterative index scan filtered search release notes`
9. `pgvector iterative scan HNSW filter "strict_order" OR "relaxed_order" documentation`
10. `Milvus iterative filtering pass rate documentation measured`

## Előszűrés ára (HNSW/IVF recall)
11. (ua. mint 2.) — Qdrant ACORN cikk, Weaviate cikk, SIEVE paper, Compass paper találatai
12. `arxiv.org/pdf/2510.27141` közvetlen lekérés (Compass paper)
13. `arxiv.org/abs/2401.07119v1` közvetlen lekérés (Curator — multi-tenant vector DB paper)

## SQLite FTS5 + jogosultsági JOIN
14. `SQLite FTS5 join external table permission filtering documentation`
15. `sqlite fts5 "join" slow "query plan" tenant permission table site:sqlite.org OR site:news.ycombinator.com OR site:stackoverflow.com`
16. `SQLite FTS5 "external content" table join filter WHERE clause slow query plan blog`
17. Közvetlen lekérés: `sqlite.org/fts5.html` (JOIN/planner szó szerinti keresés a szövegben)
18. Közvetlen lekérés: SQLite fórum — „JOINs with FTS5 virtual tables are very slow”
19. Közvetlen lekérés: SQLite fórum — „FTS5: `join as` doesn't interoperate with `tablename MATCH`”
20. Közvetlen lekérés: SQLite fórum — „Bad query plans from FTS5”

## Szivárgás (darabszám, időzítés, lapozás, „did you mean”)
21. `search result count leakage side channel access control information disclosure paper`
22. `"count" side channel authorization leak "does not exist" total hits`
23. `autocomplete suggestion leak private data search "did you mean" information disclosure`
24. `"pagination" leak hidden results total count access control search API design`
25. `"row level security" search index timing attack enumeration vulnerability disclosure blog`
26. Közvetlen lekérés: Microsoft Research — „Side-Channel Leaks in Web Applications” PDF
27. Közvetlen lekérés: PostgreSQL levelezőlista — RLS leakproofness szál

## Valós rendszerek (Elasticsearch, OpenSearch, Vespa, Qdrant, Weaviate, Milvus, Typesense, Meilisearch)
28. `Elasticsearch document level security DLS official documentation`
29. `OpenSearch document level security field level security documentation`
30. `Vespa document access control filtering query documentation`
31. `Qdrant payload filtering pre-filter HNSW documentation`
32. `Weaviate multi-tenancy filtering permissions documentation`
33. `Milvus scalar filtering search documentation pre-filter`
34. `Typesense filter_by documentation access control`
35. `Meilisearch filter security API key documentation tenant token`
36. `document level security performance overhead benchmark Elasticsearch OpenSearch`
37. `Elasticsearch document level security knn vector search interaction`
38. `Elasticsearch document level security automatically combined knn query filter role query merge`
39. `Weaviate RBAC roles documentation OR Qdrant RBAC roles documentation 2026`
40. `Weaviate multi-tenancy tenant isolation guarantee no cross-tenant leakage documentation`
41. Közvetlen lekérések: `docs.weaviate.io/weaviate/concepts/filtering`, `.../configuration/rbac`, `.../manage-collections/multi-tenancy`
42. Közvetlen lekérések: `docs.opensearch.org/2.11/security/access-control/document-level-security/` (a `/latest/` verzió nem adott vissza tartalmat, csak navigációt)
43. Közvetlen lekérés: `eliatra.com` — OpenSearch access-control teljesítmény blog
44. Közvetlen lekérések: `qdrant.tech/articles/filtered-vector-search-acorn/`, `qdrant.tech/blog/pre-filtering-vs-post-filtering/`, `qdrant.tech/documentation/concepts/filtering/`, `qdrant.tech/articles/data-privacy/`
45. Közvetlen lekérés: `milvus.io/docs/filtered-search.md`
46. Közvetlen lekérések: `typesense.org/docs/guide/data-access-control.html`, `typesense.org/docs/30.2/api/joins.html`
47. Közvetlen lekérés: `meilisearch.com/docs/capabilities/security/overview`
48. Közvetlen lekérés: `docs.vespa.ai/en/securing-your-vespa-installation.html`
49. Közvetlen lekérés (AST Consulting, T3-jellegű harmadik fél blog): `astconsulting.in/database/implement-access-control-vespa`
50. `Vespa YQL where clause ACL group filter application-level access control search`
51. `Vespa "visibility" OR "access control" per document field permission filtering search results`

## Hol szűrjön a hibrid (lexikai+vektoros) keresés
52. `hybrid search RRF reciprocal rank fusion apply filter before or after fusion`
53. `RAG access control retrieval permission filter before fusion recommendation architecture blog`
54. Közvetlen lekérések: `pinecone.io/learn/rag-access-control/`, `aws.amazon.com/blogs/security/authorizing-access-to-data-with-rag-implementations/`, `tianpan.co/blog/2026-05-04-permission-aware-retrieval-enterprise-rag-access-control`
55. `Azure AI Search security trimming filters permissions best practice`
56. `"security trimming" search index access control documentation`
57. Közvetlen lekérések: `learn.microsoft.com/.../vector-search-filters`, `.../search-document-level-access-overview`

## Egyéb / kiegészítő
58. `row level security PostgreSQL full text search join performance query planner`
59. `vector database multi-tenancy metadata filter tenant_id best practice recommendation blog`
60. `Meilisearch roaring bitmap filter implementation engineering blog`

Megjegyzés: több kereséssel nem sikerült T1-forrást találni bizonyos konkrét részkérdésekhez (ld. `gaps.md`) — ezeket nem pótoltam kitalált adattal.


---

## SQ-02 — Index és lemez elcsúszásának észlelése és javítása

# SQ-02 — Lefuttatott keresések

Módszertan: `deep-web-research` skill, `search-playbook.md` — széles → szűk lekérdezések,
elsődleges forrásra közvetlen irányítás (hivatalos doksi, man page, repó), majd a
gyártói/vélemény-jellegű találatok kiszűrése a T1/T2/T3 tierelés szerint.

## 1. Elcsúszás-észlelés módszerei (mtime, hash, inode)

| # | Query (eszköz) | Miért | Eredmény |
|---|---|---|---|
| 1 | `SQLite FTS5 integrity-check rebuild command` (WebSearch) | Konkrét parancsnevek megtalálása | fts5.html azonosítva |
| 2 | `mtime unreliable file change detection checksum` (WebSearch) | Az mtime gyengeségeinek szakirodalma | apenwarr blog, restic issue |
| 3 | `git status how does git detect file changes mtime racy git` (WebSearch) | Git saját mechanizmusa | racy-git hivatalos doksi |
| 4 | `rsync --checksum vs mtime size quick check documentation` (WebSearch) | A kétlépcsős minta hivatalos leírása | rsync man page |
| 5 | `Borgbackup file unchanged mtime size ctime cache detection` (WebSearch) | Backup-eszköz konkrét mezői | borg create.html |
| 6 | `"NFS" OR "network file system" mount mtime clock skew stale unreliable` (WebSearch) | Hálózati fájlrendszer eset | nfs(5) man page |

## 2. Valós rendszerek gyakorlata

| # | Query | Miért | Eredmény |
|---|---|---|---|
| 7 | `FSCrawler Elasticsearch detect file changes checksum "sha1" OR "mtime" indexing` (WebSearch) | ES-fájlkonnektor mechanikája | fscrawler docs, issue #531 |
| 8 | `FSCrawler checksum config file changes indexed again "checksum"` (WebSearch) | Konkrét config-mezők | local-fs.html |
| 9 | `Apache Solr DataImportHandler delta import lastModified` (WebSearch) | Solr DIH delta-mechanizmus | cwiki DataImportHandler |
| 10 | `Recoll omindex Xapian incremental indexing mtime` (WebSearch) | Recoll/Xapian gyakorlat | recollindex man, monitor doksi |
| 11 | `Meilisearch document indexing consistency crash recovery snapshot` (WebSearch) | Meilisearch konzisztencia | csak issue-k, nincs tervezési doksi (gap) |
| 12 | `Typesense reindex "out of sync" OR "consistency" file source` (WebSearch) | Typesense konzisztencia | nincs releváns hivatalos doksi (gap) |
| 13 | `Obsidian search index rebuild cache out of date` (WebSearch) | Obsidian gyakorlat | fórum-szálak, hivatalos súgó |
| 14 | `Zoekt code search index rebuild git commit detection` (WebSearch) | Zoekt staleness-detektálás | design.md (nem részletezi) |
| 15 | `obsidian.md help search "full-text index" cache mtime` (WebSearch) | Obsidian hivatalos doksi keresése | obsidian.md/help/plugins/search |
| 16 | `tantivy IndexReader reload consistency segment merge documentation` (WebSearch) | tantivy olvasó-frissítési modell | docs.rs IndexReader |

## 3. A teljes átvizsgálás ára

| # | Query | Miért | Eredmény |
|---|---|---|---|
| 17 | `SHA-256 hashing throughput GB/s benchmark BLAKE3` (WebSearch) | Hash-elés sebessége | csak marketing oldalak (gap) |
| 18 | `openssl speed sha256 MB/s benchmark modern CPU` (WebSearch) | Konkrét mért adat keresése | nem talált T1/T2 forrást (gap) |
| 19 | `walking million files filesystem stat time benchmark seconds` (WebSearch) | Fájlfa-bejárás költsége | csak régi kernel-listás anekdota (gap) |
| 20 | `SHA-256 vs BLAKE3 ... hashing algorithms on commodity hardware` → `arxiv.org/html/2407.08284v1` (WebFetch) | Mért hash-sebesség konkrét számmal | hashes/sec táblázat (erős fenntartással) |

## 4. Mit szabad automatikusan javítani

| # | Query | Miért | Eredmény |
|---|---|---|---|
| 21 | `"auto-heal" OR "self-healing" search index bug deleted data incident` (WebSearch) | Dokumentált önjavítási incidens keresése | Atlassian index auto-healing találat |
| 22 | `rclone --max-delete safety check "empty" source prevent mass deletion documentation` (WebSearch) | Automatikus törlés elleni védőkorlát mintája | rclone sync doksi |
| 23 | `rsync unmounted directory looks empty deletes everything --delete danger` (WebSearch) | Klasszikus "üresnek látszó forrás" veszély | csak fórum-anekdoták (gap, nem citálva) |
| 24 | `FSCrawler remove_deleted incorrectly removed files from index bug` (WebSearch) | Konkrét önjavítási hiba keresés-index kontextusban | issue #531 (nem megerősített gyökérok) |

## 5. Konzisztencia-ellenőrzés mint ütemezett feladat

| # | Query | Miért | Eredmény |
|---|---|---|---|
| 25 | `ZFS scrub documentation how often silent data corruption` (WebSearch) | Scrub minta és gyakoriság | zpool-scrub.8 |
| 26 | `Cassandra anti-entropy repair Merkle tree documentation` (WebSearch) | Anti-entropy minta | DataStax repair doksi |
| 27 | `Cassandra deleted data reappears tombstone resurrection repair not run` (WebSearch) | Mi történik, ha a konzisztencia-feladat elmarad | opsRepairNodesWhen |
| 28 | `Kubernetes controller reconciliation loop desired state actual state documentation` (WebSearch) | "Reconciliation" mint elnevezett minta | k8s controller doksi |

## 6. SQLite FTS5 integritás

| # | Query | Miért | Eredmény |
|---|---|---|---|
| 29 | `SQLite PRAGMA integrity_check quick_check documentation cost` (WebSearch) | Komplexitás-adat keresése | pragma.html — O(N) vs O(N log N) |

## 7. Részleges vs teljes újraépítés

| # | Query | Miért | Eredmény |
|---|---|---|---|
| 30 | `"partial reindex" vs "full reindex" threshold when rebuild entire index` (WebSearch) | Fordulópont keresése | Hawksearch doksi (nincs számszerű küszöb) |
| 31 | `Elasticsearch reindex API full reindex cost large index downtime documentation` (WebSearch) | ES saját mintája | docs-reindex.html |

## WebFetch-el ténylegesen letöltött és elemzett oldalak (verbatim tartalom kérve)

fts5.html, apenwarr.ca/log/20181113, restic issue #2179, git-scm racy-git, lesbonscomptes/recoll perfs (redirect →
recoll.org/pages/perfs.html), recoll RCL.INDEXING.MONITOR, fscrawler elasticsearch.rst, Solr DIH cwiki,
fscrawler local-fs.html, IBM Sterling IndexSynchronizationConcepts, Atlassian index-auto-healing, zpool-scrub.8,
DataStax opsRepairNodesManualRepair, opsRepairNodesWhen, borg create.html, zoekt design.md, rsync man page,
sqlite pragma.html, BLAKE3 GitHub README, Hawksearch full-vs-partial-indexing, Elastic docs-reindex 8.19,
k8s controller doksi, nfs(5) man page, fscrawler issue #531, docs.rs tantivy IndexReader, obsidian.md/help/plugins/search,
arxiv.org/html/2407.08284v1, rclone.org/commands/rclone_sync.

**Összesen kb. 31 keresés + kb. 27 verbatim fetch**, a `search-playbook.md` kb. 30 hívásos irányértékének
megfelelő nagyságrendben egyetlen kérdésre (SQ-02) vonatkozóan.


---

## SQ-03 — Ha a beágyazó nem elérhető lekérdezéskor

# SQ-03 — Lefuttatott keresések

Eszközök: WebSearch (US-only index) + WebFetch (oldal-tartalom kinyerés kis modellel).
Dátum: 2026-09-08.

## 1. Named patterns — fail-fast / graceful degradation / stale / queue
1. `graceful degradation vs fail-fast pattern distributed systems dependency failure design`
2. `hybrid search embedding service unavailable fallback to lexical search pattern`
3. Közvetlen lekérés: `docs.aws.amazon.com/wellarchitected/.../rel_mitigate_interaction_failure_graceful_degradation.html`
4. Közvetlen lekérés: `sre.google/sre-book/addressing-cascading-failures/`
5. Közvetlen lekérés: `sre.google/sre-book/handling-overload/`
6. `Azure architecture center "Queue-Based Load Leveling pattern" official documentation`
7. Közvetlen lekérés: `learn.microsoft.com/.../patterns/queue-based-load-leveling`
8. `Azure architecture center "Bulkhead pattern" isolate resources failure documentation`
9. Közvetlen lekérés: `learn.microsoft.com/.../patterns/bulkhead`
10. `"stale-if-error" OR "stale-while-revalidate" cache header serve stale response when backend down RFC`
11. Közvetlen lekérés: `rfc-editor.org/rfc/rfc5861.txt`
12. Közvetlen lekérés: `developer.mozilla.org/.../Headers/Warning`
13. `"circuit breaker" open state "fail fast" better than waiting long timeout queue backlog`
14. `"circuit breaker" "half-open" vs "waiting" queue backlog worse latency spike explanation article`

## 2. Mért adat — BM25-only vs hibrid (BEIR/MTEB/TREC)
15. `BEIR benchmark BM25 vs hybrid dense sparse nDCG@10 results table`
16. Közvetlen lekérés: `datasets-benchmarks-proceedings.neurips.cc/.../BEIR-Paper-round2.pdf`
17. Közvetlen lekérés: `elastic.co/search-labs/blog/improving-information-retrieval-elastic-stack-hybrid`
18. `TREC deep learning track BM25 baseline vs neural dense retrieval nDCG comparison table`
19. Közvetlen lekérés: `trec.nist.gov/pubs/trec30/papers/Overview-DL.pdf` (TREC 2021 DL Track Overview)
20. `MTEB retrieval leaderboard BM25 baseline score compared to embedding models`
21. `hybrid search benchmark measured recall drop when disabling one retriever leg ablation study`
22. Közvetlen lekérés: `arxiv.org/html/2604.01733v1` („From BM25 to Corrective RAG")
23. `Anthropic contextual retrieval BM25 embeddings failure rate reduction 49% 35%`
24. Közvetlen lekérés: `anthropic.com/engineering/contextual-retrieval` (kétszer, részletesebb promttal is)
25. `Anthropic contextual retrieval "Appendix I" table embeddings only BM25 recall numbers pdf`
26. Közvetlen lekérés: Anthropic Appendix II PDF (`www-cdn.anthropic.com/...pdf`) — táblázat-kinyerés sikertelen, ld. `gaps.md`

## 3. Mért adat fordítva — szemantikus-only gyengeségei (exact ID, hibakód, ritka szó)
27. `dense retrieval fails exact match rare term out-of-vocabulary BM25 outperforms semantic search`
28. Közvetlen lekérés: `tianpan.co/blog/2026-04-12-hybrid-search-production-bm25-dense-embeddings`
29. Közvetlen lekérés: `zenodo.org/records/18807773` (sparse/dense/hibrid StackOverflow tanulmány)
30. `Pinecone hybrid search alpha BM25 dense benchmark measured nDCG recall numbers blog`
31. `"embeddings only" vs "hybrid" BM25 recall table RAG retrieval benchmark exact numbers comparison paper`

## 4. Csendes romlás — jelölés a válaszban
32. `"X-Degraded" header OR "degraded response" API design partial response indicate client`
33. `"partial results" OR "partial_results" search API response field meta indicate incomplete degraded Elasticsearch timeout`
34. `Elasticsearch _shards.failed timed_out response field partial results search API documentation`
35. Közvetlen lekérés: `elastic.co/docs/solutions/search/the-search-api`
36. `API design guideline "degraded" field response metadata partial availability status indicate consumer Google API design guide OR Microsoft REST API guidelines`
37. Közvetlen lekérés: `google.aip.dev/193` (AIP-193: Errors)
38. `GraphQL "errors" array "extensions" partial data resolver failure specification official`
39. Közvetlen lekérés: `docs.vespa.ai/en/graceful-degradation.html`
40. `RFC 7234 Warning header "110 Response is stale" HTTP semantics stale response indicator`

## 5. Circuit breaker / timeout
41. `circuit breaker pattern states closed open half-open Martin Fowler microservices`
42. `Martin Fowler CircuitBreaker pattern original article "fail fast" remote call timeout`
43. `Michael Nygard "Release It" circuit breaker pattern definition fail fast`
44. `Netflix Hystrix circuit breaker states closed open half-open wiki documentation`
45. Közvetlen lekérés: `github.com/netflix/hystrix/wiki/how-it-works`
46. Közvetlen lekérés: `docs.aws.amazon.com/prescriptive-guidance/.../circuit-breaker.html`
47. `AWS builders library timeouts retries backoff choosing timeout value client`
48. Közvetlen lekérés: AWS Builders' Library PDF (timeouts-retries-and-backoff-with-jitter)
49. `Google SRE book handling overload circuit breaking cascading failure waiting worse than fail fast`
50. `"circuit breaker" "bulkhead" embedding model microservice ML inference resilience pattern timeout recommendation`

## 6. Valós hibrid keresők viselkedése lekérdezéskor
51. `Elasticsearch semantic_text inference endpoint unavailable query error behavior`
52. Közvetlen lekérés: `github.com/elastic/elasticsearch/issues/115692` (kétszer, részletesebb promttal is)
53. Közvetlen lekérés: `elastic.co/docs/reference/elasticsearch/mapping-reference/semantic-text-reference`
54. Közvetlen lekérés: `elastic.co/docs/reference/query-languages/query-dsl/query-dsl-semantic-query`
55. `Elasticsearch retriever RRF fallback if one sub-retriever fails hybrid search error whole request`
56. Közvetlen lekérés: `github.com/elastic/elasticsearch/pull/136732`
57. `OpenSearch neural search model not deployed error query time ml-commons`
58. `OpenSearch official documentation hybrid search neural query model not ready timeout error response`
59. Közvetlen lekérés: `docs.opensearch.org/latest/query-dsl/compound/hybrid/`
60. `OpenSearch neural query documentation "model_id" error "not found" OR "not ready" response format`
61. Közvetlen lekérés: `opensearch.org/blog/cold-start-search/` (nem releváns tartalom, ld. `gaps.md`)
62. `Vespa embedder unavailable timeout query fail documentation`
63. Közvetlen lekérés: `docs.vespa.ai/en/embedding.html`
64. `Weaviate vectorizer module unavailable query time error hybrid search behavior`
65. `Qdrant Milvus embedding inference service down at query time behavior documentation`
66. `Typesense embedding model remote API down search error documentation`
67. Közvetlen lekérés: `typesense.org/docs/30.2/api/vector-search.html`
68. `"cold start" OR "circuit breaker" search engine embedding service degraded mode return lexical results only header flag`

## 7. Indexelési oldal — mit csinálnak írás közben
69. `Elasticsearch semantic_text ingest failure inference unavailable indexing document rejected OR queued`
70. Közvetlen lekérés: `elastic.co/docs/troubleshoot/elasticsearch/troubleshoot-ingest-pipelines`
71. Közvetlen lekérés: `elastic.co/docs/manage-data/ingest/transform-enrich/error-handling`
72. Közvetlen lekérés: `elastic.co/guide/.../handling-failure-in-pipelines.html`
73. `"ignore_failure" OR "on_failure" inference processor elasticsearch ingest pipeline embedding error handling`
74. Közvetlen lekérés: `elastic.co/docs/reference/enrich-processor/inference-processor`
75. `OpenSearch text_embedding processor ingest pipeline failure ml model unavailable index document`
76. Közvetlen lekérés: `docs.opensearch.org/latest/ingest-pipelines/processors/text-embedding/`
77. Közvetlen lekérés: `docs.opensearch.org/latest/ingest-pipelines/pipeline-failures/` (redirekt, üres tartalom)
78. `Weaviate import object vectorization failure reject object OR store without vector`
79. `Weaviate async vectorization queue object stored not yet vectorized documentation official`
80. Közvetlen lekérés: `weaviate.io/blog/weaviate-1-22-release`
81. `Milvus function embedding provider error insert search documentation behavior`
82. Közvetlen lekérés: `milvus.io/docs/embedding-function-overview.md`
83. `Qdrant cloud inference upsert failure embedding provider down write behavior documentation`
84. `vector database async embedding backfill write text now embed later architecture pattern`
85. Közvetlen lekérés: `supabase.com/blog/automatic-embeddings`
86. Közvetlen lekérés: `docs.cloud.google.com/spanner/docs/backfill-embeddings`

Megjegyzés: több hivatalos dokumentációs oldal (OpenSearch text-embedding processor, OpenSearch
pipeline-failures, Vespa embedding.html, Milvus embedding-function-overview.md, opensearch.org
cold-start-search) lekérésekor a WebFetch csak navigációs vázat / töredékes vagy nem releváns
tartalmat adott vissza — ezeket NEM használtam fel konkrét állítás alátámasztására, csak a
`gaps.md`-ben jelöltem hiányosságként. Egyik esetben sem kaptam vissza az instrukcióban leírt
„## Issue Summary" jellegű, láthatóan hallucinált AI-összefoglalót — a kisegítő modell minden
esetben explicit jelezte, hogy nem találja a kért információt a lekért tartalomban.


---

## SQ-04 — Törlésre jelölt bejegyzés az indexben

# SQ-04 — Lefuttatott keresések

Sorrendben, ahogy futottak. Minden sor: keresőmotor-lekérdezés → mire vezetett.

1. `SQLite FTS5 documentation delete-all command contentless rebuild` (WebSearch) →
   elvezetett a hivatalos `sqlite.org/fts5.html`-hez.
2. `SQLite FTS5 "special commands" delete rebuild content=''` (WebSearch) → megerősítette,
   hogy a hivatalos oldal a releváns forrás; egyéb találatok (harmadik féltől származó
   tükrök, blogok) nem kellettek.
3. `inverted index tombstone deletion merge segment Lucene` (WebSearch) → elvezetett az
   Elastic hivatalos blogjához („Lucene's Handling of Deleted Documents").
4. `HNSW index deletion soft delete recall degradation` (WebSearch) → elvezetett két
   releváns arXiv archív cikkhez (Ghost Vectors; Enhancing HNSW Index for Real-Time
   Updates) és egy OpenReview/arXiv archív cikkhez (data deletion evaluation).
5. `WebFetch: sqlite.org/fts5.html` — deletion + bm25() szakaszok kinyerése (1. kör).
6. `WebFetch: elastic.co/blog/lucenes-handling-of-deleted-documents` — tombstone/bitset
   mechanizmus, mért 18–46%-os lekérdezés-lassulás 50%-os töröltarány mellett.
7. `WebFetch: arxiv.org/html/2606.18497v1` (Ghost Vectors) — HNSW soft-delete
   rekonstruálhatóság, ChromaDB/FAISS/Weaviate viselkedés.
8. `WebFetch: arxiv.org/html/2407.07871v2` (Enhancing HNSW Index) — „unreachable points"
   formális definíció, markDelete mechanizmus.
9. `Elasticsearch soft deletes Lucene _delete_by_query merge policy tombstone official documentation`
   (WebSearch) → elvezetett a hivatalos „History retention settings" oldalhoz és a
   forcemerge API dokumentációhoz.
10. `Qdrant delete points official documentation storage segment optimizer` (WebSearch) →
    elvezetett a hivatalos Qdrant Optimizer oldalhoz.
11. `Weaviate delete object tombstone async cleanup documentation` (WebSearch) → elvezetett
    a hivatalos delete.mdx oldalhoz és a `cleanupIntervalSeconds` GitHub PR-hoz.
12. `Milvus delete entity documentation compaction reclaim disk space` (WebSearch) →
    elvezetett a hivatalos delete-entities.md-hez és a Milvus saját blogjához.
13. `Meilisearch delete documents task documentation index` (WebSearch) → elvezetett a
    hivatalos „Documents Soft Deletion" specifikációhoz (specs.meilisearch.dev).
14. `Typesense delete document soft delete documentation` (WebSearch) → elvezetett a
    hivatalos Documents API oldalhoz (nem tartalmazott belső mechanizmust — ld. gaps.md).
15. `WebFetch: elastic.co/docs/reference/elasticsearch/index-settings/history-retention` —
    soft delete retenció, `retention.lease` alapértelmezett 12h.
16. `WebFetch: qdrant.tech/documentation/ops-optimization/optimizer` — `deleted_threshold`
    (0.2) és `vacuum_min_vector_number` (1000) pontos értékek.
17. `WebFetch: docs.weaviate.io/weaviate/manage-objects/delete` — csak a művelet API-szintű
    leírását adta, belső mechanizmust nem (ld. gaps.md), ezért továbbkeresés kellett (18).
18. `WebFetch: milvus.io/docs/delete-entities.md` — szintén csak API-szint, belső
    mechanizmust nem tartalmazott → továbbkeresés (Milvus blog) kellett.
19. `WebFetch: specs.meilisearch.dev/specifications/text/0136-documents-soft-deletion.html`
    — pontos purge-feltételek (arányküszöb, lemezküszöb).
20. `WebFetch: typesense.org/docs/30.2/api/documents.html` — nem tartalmazott belső
    mechanizmust (ld. gaps.md).
21. `Weaviate documentation cleanupIntervalSeconds tombstone HNSW vector index config`
    (WebSearch) → elvezetett a hivatalos vector-index config-refs oldalhoz.
22. `Milvus documentation "delete and compaction" mechanism deleted entities segment`
    (WebSearch) → elvezetett a Milvus saját 2022-es blogbejegyzéséhez a streaming delete
    mechanizmusról.
23. `OpenSearch soft delete Lucene documentation index-time deletion` (WebSearch) →
    elvezetett a hivatalos Delete by Query API oldalhoz (kevés belső részlet, ld. gaps.md).
24. `bun oven-sh 31247 FTS5 macOS "database disk image is malformed"` (WebSearch) →
    közvetlenül megtalálta a GitHub issue-t (ismert csapda, a feladat kérése szerint
    rögzítve, nem részletezve tovább).
25. `WebFetch: github.com/oven-sh/bun/issues/31247` — pontos hibaszöveg és verziószám
    kinyerése.
26. `WebFetch: docs.weaviate.io/weaviate/config-refs/indexing/vector-index` —
    `cleanupIntervalSeconds` (alapértelmezett 300s), `TOMBSTONE_DELETION_MIN/MAX_PER_CYCLE`.
27. `WebFetch: milvus.io/blog/2022-02-07-how-milvus-deletes-streaming-data-in-distributed-cluster.md`
    — bitset + bloom filter mechanizmus, logikai vs fizikai törlés megkülönböztetése.
28. `WebFetch: docs.opensearch.org/latest/api-reference/document-apis/delete-by-query`
    — csak API-szintű leírás, belső Lucene-mechanizmust nem részletez (ld. gaps.md).
29. `Faiss IVF index remove_ids deletion documentation official` (WebSearch) → elvezetett a
    hivatalos Faiss wiki „Special operations on indexes" oldalhoz.
30. `WebFetch: openreview.net/pdf?id=lnaC19Pd30` — **sikertelen, 403 hiba** → újrapróbálva
    arXiv-változattal (31).
31. `"How Should We Evaluate Data Deletion" graph-based ANN indexes arxiv` (WebSearch) →
    megtalálta az arXiv-azonosítót (2512.06200) és a HTML-változat elérhető URL-jét.
32. `"soft delete" search index anti-pattern relevance BM25 stale document frequency`
    (WebSearch) → nem hozott releváns, kifejezetten a kérdésre szabott forrást (általános
    BM25-ismertetők jöttek fel) — ld. gaps.md.
33. `WebFetch: github.com/facebookresearch/faiss/wiki/Special-operations-on-indexes` —
    `remove_ids`, `IndexIVFFlat` támogatott, szekvenciális indexeknél id-eltolódás.
34. `WebFetch: arxiv.org/html/2512.06200` — mért recall-stabilizáció fizikai törlésnél
    (~0.81 SIFT1B-n), logikai törlésnél romló pontosság, hibrid „Deletion Control"
    stratégia.
35. `Manning Raghavan Schütze "Introduction to Information Retrieval" dynamic indexing
    invalidation bit deletion auxiliary index` (WebSearch) → elvezetett az ingyenes
    hivatalos online kiadáshoz (nlp.stanford.edu/IR-book).
36. `WebFetch: nlp.stanford.edu/IR-book/html/htmledition/dynamic-indexing-1.html` —
    „invalidation bit vector", „the correct number of hits for a term is no longer a
    simple lookup" idézetek.
37. `Qdrant Weaviate "undelete" restore deleted point vector re-insert without re-embedding`
    (WebSearch) → nem hozott közvetlen hivatalos forrást a „visszavonás" API-ra (ld.
    gaps.md); a Qdrant GitHub issue-k (#6556, #2550) közvetetten megerősítik, hogy a
    vektor-nélküli/törölt pontok kezelése esetről esetre eltérő, nincs dedikált „undelete".
38. `WebFetch: elastic.co/docs/api/doc/elasticsearch/operation/operation-delete-by-query`
    — verziókonfliktus-kezelés, refresh-viselkedés; segment-merge-ről nem szól (ld. gaps.md).
39. `WebFetch: sqlite.org/fts5.html` (2. kör, célzottan a 4.4.3 „External Content Tables"
    szakaszra) — a normál (nem-external) FTS5 tábla automatikus DELETE-kezelése, és a
    hivatalos trigger-példa (`t1_ad`) az external content tábla szinkronban tartására.
