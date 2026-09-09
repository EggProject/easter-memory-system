# Linkek — minden meglátogatott és felderített forrás

Kampány: `kereses-indexeles` · 2026-09-08

> Al-kérdésenként bontva, ahogy a kereső ügynökök rögzítették.


---

## SQ-01 — Hol szűrjön a jogosultság a keresésben

# SQ-01 — Meglátogatott linkek, tier-besorolással

Tier-kulcs: **T1** = hivatalos dokumentáció/spec/forráskód/peer-reviewed vagy arXiv paper.
**T2** = megbízható másodlagos (mérnöki blog, konferencia-előadás) VAGY gyártó saját
termékére vonatkozó teljesítményállítása. **T3** = fórum, levelezőlista, vélemény, marketing
(hivatalos domainen is, ha fórum/levelezőlista).

## T1 — Hivatalos dokumentáció, spec, forráskód, tudományos publikáció

| URL | Mit adott |
|---|---|
| https://www.sqlite.org/fts5.html | Hivatalos FTS5 spec. `rank` oszlop, bm25(), external content — de **nincs benne a szó "JOIN"** (ellenőrizve szó szerinti kereséssel). |
| https://sqlite.org/forum/info/509bdbe534f58f20 | *(ld. T3 is)* SQLite fórum, de a Richard Hipp / Dan Kennedy válaszok a projekt fő fejlesztőitől származnak — technikai tartalma megbízható, de a szabály szerint fórum=T3, nem T1. |
| https://learn.microsoft.com/en-us/azure/search/vector-search-filters | Hivatalos Azure AI Search dok. preFilter/postFilter definíció, mért %-os lassulás saját benchmarkból (ld. T2 megjegyzés a szövegben). |
| https://learn.microsoft.com/en-us/azure/search/search-document-level-access-overview | Hivatalos dok. dokumentum-szintű hozzáférés-vezérlés, Entra ID integráció. |
| https://docs.weaviate.io/weaviate/concepts/filtering | Hivatalos Weaviate dok. Pre/post-filter definíció, ACORN, sweeping mechanizmus. |
| https://docs.weaviate.io/weaviate/configuration/rbac | Hivatalos dok. RBAC granularitás (kollekció-szint, nem objektum-szint). |
| https://docs.weaviate.io/weaviate/manage-collections/multi-tenancy | Hivatalos dok. „Each tenant is stored on a separate shard” — fizikai izoláció. |
| https://www.elastic.co/docs/deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level | Hivatalos Elastic dok. DLS mechanizmus + a kritikus szivárgási figyelmeztetés (count/aggregáció/pontszám). |
| https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-knn-query | Hivatalos Elastic dok. A knn `filter` paraméter kifejezetten pre-filter; a Query DSL többi szűrője post-filter és kevesebb mint k találatot adhat. |
| https://docs.opensearch.org/2.11/security/access-control/document-level-security/ | Hivatalos OpenSearch dok. Lucene-level / filter-level / adaptive DLS módok. |
| https://milvus.io/docs/filtered-search.md | Hivatalos Milvus dok. Alapértelmezett szűrés = pre-filter (előbb szűr, utána ANN a szűrt halmazon belül). Iteratív szűrés mint alternatíva. |
| https://typesense.org/docs/guide/data-access-control.html | Hivatalos Typesense dok. Scoped API key — kriptográfiailag beágyazott `filter_by`, felülírhatatlan. |
| https://typesense.org/docs/30.2/api/joins.html | Hivatalos dok. Collection-join szintaxis, `!$deny_list(...)` minta ACL-szerű szűréshez. |
| https://www.meilisearch.com/docs/capabilities/security/overview | Hivatalos Meilisearch dok. Tenant token = API key-ből származtatott, beágyazott szűrő minden kereséshez. |
| https://docs.pinecone.io/guides/data/understanding-metadata | Hivatalos Pinecone dok. (Pinecone nem volt az eredeti listán, kiegészítésként.) Csak sparse vektoroknál dokumentált explicit a top_k alákerülés. |
| https://qdrant.tech/documentation/concepts/filtering/ | Hivatalos Qdrant dok. Szűrés-konstrukció, payload index ajánlás — de a végrehajtási sorrendről (elő/utó) nem nyilatkozik explicit ezen az oldalon. |
| https://arxiv.org/pdf/2510.27141 | **Compass** paper (Ye, Yan, Lo) — formális definíciók pre/post-filterre, a post-filter „több körre” bomlásának és a pre-filter <0,1% küszöbének leírása. |
| https://arxiv.org/abs/2401.07119v1 | **Curator** paper — többbérlős vektor-DB index-stratégiák (megosztott index metaadat-szűréssel vs. bérlőnkénti index). |
| https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/WebAppSideChannel-final.pdf | Chen/Wang/Wang/Zhang (Microsoft Research + Indiana University) — oldalcsatorna-szivárgás titkosított forgalomban is (csomagméret, időzítés). |
| https://www.postgresql.org/about/news/pgvector-080-released-2952 | Hivatalos PostgreSQL.org közlemény — pgvector 0.8.0 iteratív index-bejárás, „overfiltering” elleni mechanizmus. |
| https://docs.vespa.ai/en/securing-your-vespa-installation.html | Hivatalos Vespa dok. — **kizárólag** hálózati/cluster-szintű biztonságot ír le, dokumentum-szintű hozzáférés-vezérlésről nincs benne szó. |

## T2 — Megbízható másodlagos / gyártói saját teljesítményállítás

| URL | Mit adott |
|---|---|
| https://towardsdatascience.com/effects-of-filtered-hnsw-searches-on-recall-and-latency-434becf8041c/ | Weaviate-mérnök (Etienne Dilocker) saját mérése — 250k objektum, 256-dim, Weaviate v1.8.0. |
| https://qdrant.tech/articles/filtered-vector-search-acorn/ | Qdrant saját cikke, ACORN — konkrét recall/latencia számok (1% szelektivitásnál). |
| https://qdrant.tech/blog/pre-filtering-vs-post-filtering/ | Qdrant saját cikke — „Why Qdrant Does Neither” — hibrid mechanizmus leírása. |
| https://qdrant.tech/articles/data-privacy/ | Qdrant saját blog — RBAC kulcs-szintű, kollekció-granularitású. |
| https://weaviate.io/blog/speed-up-filtered-vector-search | Weaviate saját blog — ACORN „akár 10x” gyorsulás (grafikonban, szöveges szám nélkül). |
| https://eliatra.com/blog/performance-improvements-for-the-access-control-layer-of-opensearch/ | Eliatra (OpenSearch security plugin gyártó) saját optimalizációjának mérése — 58% / 542% átviteli sebesség javulás fürtméret-függően. |
| https://www.elastic.co/search-labs/blog/vector-search-filtering | Elastic saját mérnöki blogja — pre/post-filter HNSW-interakció, ACORN-1 mérés (55%-ra csökkenő latencia 2%-os szelektivitásnál). |
| https://www.pinecone.io/learn/rag-access-control/ | Pinecone saját ajánlása — „It Depends™️”, hit-rate alapú döntés elő/utószűrés között. |
| https://aws.amazon.com/blogs/security/authorizing-access-to-data-with-rag-implementations/ | Hivatalos AWS blog, saját ajánlás: post-retrieval jogosultság-ellenőrzés a forrásrendszernél (S3 Access Grants), mert a vektor-DB metaadat elavulhat. |
| https://aws.amazon.com/blogs/database/supercharging-vector-search-performance-and-relevance-with-pgvector-0-8-0-on-amazon-aurora-postgresql | AWS saját mérése pgvector 0.8.0-ról — recall 10%→100% és 1%→100%, latencia 9x. |
| https://tianpan.co/blog/2026-05-04-permission-aware-retrieval-enterprise-rag-access-control | Független mérnöki blog — érvel a vektor-rétegbeli előszűrés mellett, megnevezi pgvector 0.8.0, Weaviate, Pinecone, Qdrant, Milvus RBAC/namespace-izolációit. |

## T3 — Fórum, levelezőlista, harmadik féltől származó tutorial, vélemény

| URL | Mit adott |
|---|---|
| https://sqlite.org/forum/info/509bdbe534f58f20 | SQLite fórum: „JOINs with FTS5 virtual tables are very slow” — ok: hiányzó `ANALYZE` statisztika; ANALYZE után 170s → 0,259s. |
| https://sqlite.org/forum/forumpost/5b303ab003f91660 | SQLite fórum: FTS5 `MATCH` nem működik JOIN-alias mellett; megoldás: táblafüggvény-szintaxis vagy CTE/subquery. |
| https://sqlite.org/forum/info/e0e30e9eb1998e3c9305aea26957bec804615283969d11c1f9326a6b787526eb | SQLite fórum: „Bad query plans from FTS5” — FTS5 statikus költségbecslést használ, ami rossz tervet eredményezhet JOIN-nál. |
| https://www.postgresql.org/message-id/1985636.6fXRgaOMqv%40peanuts2 | pgsql-hackers levelezőlista — RLS leakproof-függvények hiánya lassulást okoz (index nem használható), IDOR a fő fenyegetési modell. |
| https://astconsulting.in/database/implement-access-control-vespa | Harmadik féltől származó tutorial-blog Vespa hozzáférés-vezérlésről — nem tudta konkrétan megmondani, natív-e vagy alkalmazás-szintű. Alacsony evidenciaérték, nem használtam fel állítás alátámasztására. |

## Megtalált, de nem (vagy csak felületesen) felhasznált linkek

- https://opendistro.github.io/for-elasticsearch-docs/... — elavult (Open Distro), nem az aktuális Elastic/OpenSearch dokumentáció, nem idéztem belőle.
- https://docs.opensearch.org/latest/security/access-control/document-level-security/ — a „latest” verzió lekérésekor csak navigációs vázat kaptam vissza (nem valódi tartalmat) → a `2.11` verziót használtam helyette, ami működött.
- https://darksi.de/13.sqlite-fts5-structure/, https://medium.com/@johnidouglasmarangon/..., https://www.sql-easy.com/... — általános FTS5 bevezető blogok, nem tartalmaztak a JOIN/ACL kérdésre választ, nem idéztem.
- https://ieeexplore.ieee.org/document/6558424 — paywall mögötti IEEE cikk (multi-tenant cloud izoláció), címét láttam, tartalmát nem tudtam lekérni — nem idéztem.


---

## SQ-02 — Index és lemez elcsúszásának észlelése és javítása

# SQ-02 — Meglátogatott linkek, tier-besorolással

Tierelés a megbízó (parent agent) definíciója szerint:
- **T1** = hivatalos dokumentáció, specifikáció, forráskód, peer-reviewed/arXiv paper
- **T2** = megbízható másodlagos VAGY gyártó/szerző saját termékéről szóló teljesítményállítás
- **T3** = fórum, vélemény, marketing (hivatalos domainen lévő fórum/issue is T3)

---

## T1 — Hivatalos dokumentáció / specifikáció / forráskód / arXiv

| URL | Mit tartalmaz | Felhasználva |
|---|---|---|
| https://www.sqlite.org/fts5.html | FTS5 hivatalos doksi: `integrity-check`, `rebuild`, external content táblák, pitfalls | Igen, 6. kérdés |
| https://sqlite.org/pragma.html | `PRAGMA integrity_check` vs `PRAGMA quick_check` — O(N log N) vs O(N) | Igen, 6. kérdés |
| https://git-scm.com/docs/racy-git | Git hivatalos doksi a "racy git" jelenségről, stat-cache mezők, futásidő-teszt | Igen, 1. kérdés |
| https://man7.org/linux/man-pages/man1/rsync.1.html | rsync man page: `--checksum` vs alapértelmezett "quick check" (méret+mtime) | Igen, 3. kérdés |
| https://borgbackup.readthedocs.io/en/stable/usage/create.html | BorgBackup hivatalos doksi: files cache módok (ctime/mtime/inode/size), kompromisszumok | Igen, 1. és 3. kérdés |
| https://fscrawler.readthedocs.io/en/latest/admin/fs/local-fs.html | FSCrawler hivatalos doksi: `checksum`, `update_rate`, `remove_deleted` | Igen, 2. kérdés |
| https://cwiki.apache.org/confluence/display/solr/DataImportHandler | Apache Solr hivatalos wiki: DIH `deltaQuery`, `deletedPkQuery`, `last_index_time` | Igen, 2. kérdés |
| https://www.recoll.org/usermanual/webhelp/docs/RCL.INDEXING.MONITOR.html | Recoll hivatalos kézikönyv: valós idejű indexelés (inotify), terhelési figyelmeztetés | Igen, 2. kérdés |
| https://github.com/sourcegraph/zoekt/blob/main/doc/design.md | Zoekt hivatalos tervezési dokumentum (repó újraindexelés említése, staleness-detektálás NEM részletezett) | Igen, 2. kérdés (negatív találat) |
| https://openzfs.github.io/openzfs-docs/man/master/8/zpool-scrub.8.html | OpenZFS hivatalos man page: `zpool scrub`, ütemezett timer egységek | Igen, 5. kérdés |
| https://docs.datastax.com/en/cassandra-oss/3.x/cassandra/operations/opsRepairNodesManualRepair.html | Cassandra hivatalos üzemeltetési doksi: anti-entropy repair, Merkle-fa | Igen, 5. kérdés |
| https://docs.datastax.com/en/cassandra-oss/3.x/cassandra/operations/opsRepairNodesWhen.html | Cassandra hivatalos doksi: repair gyakorisági ajánlás, `gc_grace_seconds` | Igen, 5. kérdés |
| https://kubernetes.io/docs/concepts/architecture/controller/ | Kubernetes hivatalos doksi: control loop / "reconciliation pattern" elnevezés | Igen, 5. kérdés |
| https://rclone.org/commands/rclone_sync/ | rclone hivatalos doksi: `--max-delete`, "won't delete if there were any errors" biztonsági korlát | Igen, 4. kérdés |
| https://man7.org/linux/man-pages/man5/nfs.5.html | NFS man page: attribútum-gyorsítótár (acregmin/acdirmax/actimeo/noac), staleness oka | Igen, 1. kérdés |
| https://obsidian.md/help/plugins/search | Obsidian hivatalos súgó: Search plugin működése (fájlokon élőben keres, nincs dokumentált külön perzisztens FTS-index leírás) | Igen, 2. kérdés (negatív találat) |
| https://www.elastic.co/guide/en/elasticsearch/reference/8.19/docs-reindex.html | Elasticsearch hivatalos Reindex API doksi: teljes vs részleges (query/op_type) újraindexelés | Igen, 7. kérdés |
| https://docs.rs/tantivy/latest/tantivy/struct.IndexReader.html | tantivy hivatalos Rust doksi: `reload()`, `ReloadPolicy::OnCommitWithDelay` | Igen, 2. kérdés |
| https://arxiv.org/html/2407.08284v1 | arXiv preprint: hash-algoritmusok teljesítmény-mérése (hashes/sec, EPYC szerver) | Igen, 3. kérdés (erős fenntartással) |
| https://github.com/BLAKE3-team/BLAKE3 | BLAKE3 hivatalos repó: hivatkozás a benchmark-diagramra, konkrét szám nem volt kinyerhető szövegként | Nem hasznosítva (kép-alapú diagram) |

## T1 — meglátogatott, de a kérdéshez érdemben nem hozzájáruló / negatív találat

| URL | Megjegyzés |
|---|---|
| https://github.com/dadoonet/fscrawler/blob/fscrawler-2.9/docs/source/admin/fs/elasticsearch.rst | Csak mezőneveket sorol fel (`file.checksum` stb.), a detektálás mechanizmusát nem írja le |

---

## T2 — Megbízható másodlagos / gyártó-szerző saját teljesítményállítása

| URL | Mit tartalmaz | Miért T2 |
|---|---|---|
| https://apenwarr.ca/log/20181113 ("mtime comparison considered harmful") | Mélyreható technikai elemzés az mtime minden gyengeségéről, a `redo` build-rendszer szerzőjétől | Személyes blog, szerkesztői kontroll nélkül — de a `redo` saját rendszeréről beszél, ami elfogadható "szerző a saját rendszeréről" jellegű forrás |
| https://www.recoll.org/pages/perfs.html | Konkrét mért indexelési sebesség-számok (PDF/HTML, fájlszám, idő) | A Recoll saját szerzőjének mérése a saját szoftveréről |
| https://developerdocs.hawksearch.com/docs/full-vs-partial-indexing | Teljes vs részleges index-újraépítés lépései, mikor melyiket ajánlják | Gyártói (Hawksearch) dokumentáció saját termékről |

---

## T3 — Fórum / issue / vélemény / marketing (hivatalos domainen is T3)

| URL | Mit tartalmaz | Miért T3 |
|---|---|---|
| https://github.com/restic/restic/issues/2179 | restic: mtime alapú változás-észlelés hibája, csomagkezelő visszaállítja a régi mtime-ot | GitHub issue — fórum-jellegű vita, még ha a hivatalos repóban is van |
| https://github.com/dadoonet/fscrawler/issues/531 | "Issues with remove deleted" — töröltnek hitt, valójában létező fájlok problémája | GitHub issue, megoldatlan, nincs megerősített gyökérok |
| https://forum.obsidian.md/t/stuck-index-cache-bases-unaware-of-new-notes-outline-heading-link-suggestions-empty-rebuild-cache-button-inert/108785 | Felhasználói panasz: a cache/index "beragad", a Rebuild Cache gomb nem reagál | Fórumbejegyzés, hivatalos Obsidian fórum-domainen, de nem hivatalos dokumentáció |

---

## Egyéb — érintőlegesen látott, nem idézett linkek (leadek, nem citálva)

- https://www.ibm.com/docs/SS4QMC_10.0.0/installation/c_IndexSynchronizationConcepts.html — IBM Sterling OMS "Index Synchronization Concepts": InSync flag, `YFS_Awaiting_Index` újrapróbálkozási tábla, kézi "not-synchronized" jelölés. **T1** (gyártói hivatalos termékdoksi), felhasznált az 5. kérdésnél.
- https://confluence.atlassian.com/enterprise/fix-indexing-issues-with-index-auto-healing-1540234564.html — Atlassian (Jira/Confluence) "Index auto-healing": napi cron, index-árva / DB-árva / elavult tétel kategóriák, "Unhealthy" esetén kézi újraindexelés javasolt. **T1** (hivatalos gyártói termékdoksi), felhasznált az 5. kérdésnél.
- https://scylladb.com/2022/06/30/preventing-data-resurrection-with-repair-based-tombstone-garbage-collection/ — csak címként látva, nem fetch-elve.
- Számos marketing/összehasonlító oldal (ssojet.com, mojoauth.com, devtoolspro.org stb.) a BLAKE3/SHA-256 sebesség-összehasonlításra — **nem használva**, mert forrás nélküli, AI-farm jellegű oldalak (ld. gaps.md).

---

## Keresőmotor AI-összefoglaló probléma

Egyetlen esetben sem adott vissza a WebFetch a valódi oldal helyett tisztán AI-generált összefoglalót olyan módon, hogy az megtévesztő lett volna — de több WebFetch-hívás "nem talált releváns szakaszt" jelzéssel tért vissza (pl. FSCrawler elasticsearch.rst, Zoekt design.md, Obsidian search súgó), ezeket a `gaps.md` rögzíti negatív találatként, nem pedig kitalált tartalommal töltöttem ki.


---

## SQ-03 — Ha a beágyazó nem elérhető lekérdezéskor

# SQ-03 — Meglátogatott linkek, tier-besorolással

Tier-kulcs: **T1** = hivatalos dokumentáció/spec/forráskód/peer-reviewed vagy arXiv paper.
**T2** = megbízható másodlagos VAGY gyártó saját termékére vonatkozó teljesítményállítása.
**T3** = fórum, issue tracker vita, vélemény, marketing (hivatalos domainen is, ha
fórum/issue/vélemény jellegű).

## T1 — Hivatalos dokumentáció, spec, forráskód, tudományos/arXiv publikáció

| URL | Mit adott |
|---|---|
| https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_mitigate_interaction_failure_graceful_degradation.html | Hivatalos AWS Well-Architected dok. Graceful degradation definíció, soft/hard dependency, circuit breaker ajánlás fail-fast helyzetre. |
| https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/design-interactions-in-a-distributed-system-to-mitigate-or-withstand-failures.html | Hivatalos AWS Well-Architected dok. (kontextus, nem idéztem közvetlenül belőle). |
| https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/circuit-breaker.html | Hivatalos AWS Prescriptive Guidance. Circuit breaker closed/open állapotok, half-open viselkedés (név nélkül), használati esetek. |
| https://learn.microsoft.com/en-us/azure/architecture/patterns/queue-based-load-leveling | Hivatalos Azure Architecture Center. Queue-based load leveling definíció + explicit „nem javasolt, ha alacsony-latenciájú szinkron válasz kell" korlátozás. |
| https://learn.microsoft.com/en-us/azure/architecture/patterns/bulkhead | Hivatalos Azure Architecture Center. Bulkhead-minta definíció, erőforrás-izoláció kaszkádhiba ellen. |
| https://sre.google/sre-book/addressing-cascading-failures/ | Hivatalos, publikált Google SRE könyv fejezet. Korai elutasítás (kis várólista-hossz), graceful degradation definíció, a komplexitás kockázata. |
| https://sre.google/sre-book/handling-overload/ | Hivatalos Google SRE könyv fejezet. Degradált válasz vs hiba prioritási sorrend, kritikusság-alapú terheléselhárítás. |
| https://docs.vespa.ai/en/graceful-degradation.html | Hivatalos Vespa dok. `coverage.degraded` mező a válaszban — konkrét, élő minta a „jelöld a válasz metaadatában" mintára. |
| https://docs.vespa.ai/en/embedding.html | Hivatalos Vespa dok. — embedder-hiba/időtúllépés viselkedéséről **nincs benne infó** (ld. `gaps.md`). |
| https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/semantic-text-reference | Hivatalos Elastic dok. Kulcsidézet: inference endpoint eltávolítása/hiánya **hibát dob** ingestnél ÉS lekérdezésnél is. |
| https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-semantic-query | Hivatalos Elastic dok. — a `semantic` query hibakezeléséről explicit infó **nem található** ezen az oldalon (ld. `gaps.md`). |
| https://www.elastic.co/docs/reference/enrich-processor/inference-processor | Hivatalos Elastic dok. `ignore_failure`/`on_failure` paraméterek, alapértelmezett `false`. |
| https://www.elastic.co/guide/en/elasticsearch/reference/master/handling-failure-in-pipelines.html | Hivatalos Elastic dok. „By default, pipeline processing stops when one of these processors fails or encounters an error." |
| https://www.elastic.co/docs/manage-data/ingest/transform-enrich/error-handling | Hivatalos Elastic dok. `on_failure`/`ignore_failure` mechanizmus általános leírása. |
| https://www.elastic.co/docs/solutions/search/the-search-api | Hivatalos Elastic dok. `timed_out`, `_shards.failed/skipped`, `allow_partial_search_results` — konkrét, élő minta a degradált válasz jelölésére. |
| https://milvus.io/docs/embedding-function-overview.md | Hivatalos Milvus dok. — a beágyazó-szolgáltatás hibájáról írás/lekérdezés közben **nincs infó** (ld. `gaps.md`). |
| https://typesense.org/docs/30.2/api/vector-search.html | Hivatalos Typesense dok. `remote_embedding_timeout_ms` és `remote_embedding_num_tries` — retry-mechanizmus dokumentálva, a kimerülés utáni viselkedés **nincs** dokumentálva. |
| https://docs.opensearch.org/latest/ingest-pipelines/processors/text-embedding/ | Hivatalos OpenSearch dok. — modell-elérhetetlenség viselkedéséről a lekért tartalom **nem adott** infót (ld. `gaps.md`). |
| https://docs.opensearch.org/latest/ingest-pipelines/pipeline-failures/ | Hivatalos OpenSearch dok. — a lekérés csak navigációs vázat adott vissza (ld. `gaps.md`). |
| https://docs.opensearch.org/latest/query-dsl/compound/hybrid/ | Hivatalos OpenSearch dok. — sub-query hiba/modell-elérhetetlenség hibakezeléséről **nincs infó** ezen az oldalon (ld. `gaps.md`). |
| https://docs.cloud.google.com/spanner/docs/backfill-embeddings | Hivatalos Google Cloud Spanner dok. `SAFE.ML.PREDICT` → `NULL` hibás sorokra, `WHERE embedding_column IS NULL` idempotens újrafuttatás, aszinkron utólagos backfill minta. |
| https://google.aip.dev/193 | Hivatalos Google API Improvement Proposal. „APIs should not support partial errors" — tervezési ajánlás a részleges hibák ellen. |
| https://www.rfc-editor.org/rfc/rfc5861.txt | Hivatalos IETF RFC. `stale-if-error` Cache-Control kiterjesztés — stale válasz hiba esetén, kötelező Age+Warning fejléc. |
| https://github.com/netflix/hystrix/wiki/how-it-works | A Hystrix projekt saját hivatalos wiki-dokumentációja. Closed/Open/Half-Open állapotok, trip-küszöbök, sleep window. |
| https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/file/65b9eea6e1cc6bb9f0cd2a47751a186f-Paper-round2.pdf | BEIR paper (NeurIPS 2021 Datasets & Benchmarks track, peer-reviewed). BM25 vs DPR/ANCE/TAS-B nDCG@10 táblázat, domain-shift magyarázat. |
| https://trec.nist.gov/pubs/trec30/papers/Overview-DL.pdf | Hivatalos NIST TREC 2021 Deep Learning Track Overview. Konkrét nDCG@10: BM25 legjobb 0,5116 (doc)/0,4458 (passage) vs neurális legjobb 0,7437/0,7494. |
| https://arxiv.org/html/2604.01733v1 | arXiv paper („From BM25 to Corrective RAG"). BM25/dense/hybrid nDCG@10 és Recall@5 táblázat pénzügyi dokumentumokon. |
| https://d1.awsstatic.com/builderslibrary/pdfs/timeouts-retries-and-backoff-with-jitter.pdf | Hivatalos AWS Builders' Library. Timeout-választás módszertana (p99.9 alapú), a circuit breaker **kritikája** (token bucket alternatíva). |

## T2 — Megbízható másodlagos / gyártói saját teljesítményállítás vagy saját termékleírás

| URL | Mit adott |
|---|---|
| https://www.elastic.co/search-labs/blog/improving-information-retrieval-elastic-stack-hybrid | Elastic saját mérnöki blogja, saját termékéről. RRF: +18% nDCG@10 BM25-höz képest (BEIR-en); súlyozott: +24%. |
| https://www.anthropic.com/engineering/contextual-retrieval | Anthropic saját mérnöki blogja, saját technikájáról. 35%/49%/67%-os failure-rate csökkenés BM25+embedding kombinációkkal (kontextus-függő, ld. `gaps.md` a nem-kontextuális bontás hiányáról). |
| https://www-cdn.anthropic.com/5722e7658c9302d8b97a3238de1bb8e6afdf04b9.pdf | Anthropic saját Appendix II PDF-je — létezik benne a kért táblázat, de a WebFetch nem tudta kinyerni a konkrét sorokat (ld. `gaps.md`). |
| https://supabase.com/blog/automatic-embeddings | Supabase saját blogja, saját (pgvector+pgmq+pg_cron) architektúrájáról. Aszinkron beágyazás-generálás mintája — sor azonnal commitolódik, embedding utólag, várólistán. |
| https://tianpan.co/blog/2026-04-12-hybrid-search-production-bm25-dense-embeddings | Független mérnöki blog (nem gyártó). Konkrét lekérdezés-típusok, ahol BM25 nyer: hibakódok, SKU-k, függvénynevek, ritka entitások. |
| https://weaviate.io/blog/weaviate-1-22-release | Weaviate saját blogja, saját termékéről. Async vector index building — objektum azonnal kereshető (brute-force, max 100k objektumig), amíg az index épül; vektorizáció-hibáról nincs benne infó. |
| https://zenodo.org/records/18807773 | StackOverflow sparse/dense/hibrid tanulmány (nem egyértelműen peer-reviewed, Zenodo self-deposit). TF-IDF (nem teljes BM25!) vs dense vs hibrid Recall@5/MRR számok — itt a dense nyer. |
| https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Warning | MDN — a HTTP `Warning` fejléc leírása és explicit elavulási jelzése (RFC 9111). |

## T3 — Issue tracker vita, fórum, harmadik féltől származó tutorial, vélemény

| URL | Mit adott |
|---|---|
| https://github.com/elastic/elasticsearch/issues/115692 | Felhasználói bug report (nem Elastic-alkalmazott). Konkrét, valós hibaüzenet: „Unable to find model deployment task... please stop and start the deployment" — 404-es hiba, nem degradált válasz. Elastic-alkalmazotti megerősítés nem található a threadben. |
| https://github.com/elastic/elasticsearch/pull/136732 | Elastic saját repo PR-vita a compound retriever (RRF) shard-szintű hibakezeléséről — `allow_partial_results`-tól függ, hogy a teljes kérés elbukik-e vagy csak a hiba kerül jelentésre. Mérnöki vita, nem hivatalos dokumentáció. |
| https://github.com/weaviate/weaviate/issues/2892 | „Hybrid search expose errors from underlying vectorizer" — a cím maga is azt sugallja, hogy a hibrid keresés alapból hibát dob, ha a vectorizer elbukik. |
| https://github.com/weaviate/weaviate/issues/4346, #6873, #7681, #6695, #8366, #10424 | Weaviate hibrid keresési hibák különböző okokból (dimenzió-eltérés, szűrés, kliensverzió) — háttérként néztem át, konkrét idézetre nem használtam. |
| https://github.com/weaviate/weaviate/issues/7156 | „Objects may fail to be added when using batch import + vectorizer + async indexing" — jelzi, hogy az aszinkron vectorizáció írási hibákkal járhat, de hivatalos doksi ezt nem tárgyalja. |
| https://github.com/weaviate/weaviate/issues/4587 | „Async Vectorizer Modules" feature-kérés — jelzi, hogy 2024-ben ez még nyitott fejlesztési irány volt. |
| https://forum.weaviate.io/t/hybrid-search-giving-errors-about-missing-vectorizer-but-objects-are-vectorized-correctly/2092 | Közösségi fórum — vectorizer-hiba hibrid keresésnél, gyakorlati tapasztalat. |
| https://github.com/opensearch-project/ml-commons/issues/2838, #2823, #3582, #2808, #2981 | OpenSearch ml-commons bug reportok modell-deploy hibákról — a keresési hiba ténye megerősítést nyer, de hivatalos dokumentációs állásfoglalás nem. |
| https://forum.opensearch.org/t/ml-model-has-to-be-re-deployed-each-time-ml-node-is-restarted/21120 | Közösségi fórum — modell-újratelepítési probléma csomópont-újraindításkor. |

## Megtalált, de nem (vagy csak háttérként) felhasznált linkek

- https://opensearch.org/blog/cold-start-search/ — a cím alapján ígéretesnek tűnt, de a tartalom kizárólag a shard-refresh/indexelési késleltetésről szól, nem a beágyazó-szolgáltatás elérhetőségéről — nem idéztem belőle.
- https://milvus.io/docs/filtered-search.md, https://milvus.io/docs/search-with-embedding-lists.md — más témára (szűrés) vonatkoznak, csak tájékozódásra használtam.
- https://qdrant.tech/documentation/inference/cloud-inference/, .../inference-api/ — a Qdrant Cloud Inference funkció leírását adják, de a hibaviselkedésről (mi történik, ha az inference szolgáltatás nem elérhető) nem nyilatkoznak — nem idéztem belőlük konkrét állítást.
- https://accelate.ai/case-studies/bm25-vs-dense-vs-hybrid-retrieval-benchmark, https://sesen.ai/blog/bm25-vs-embeddings-hybrid-retrieval, https://denser.ai/blog/hybrid-search-for-rag/, https://supermemory.ai/blog/hybrid-search-guide/ — marketing-jellegű, forrás nélküli összefoglaló blogok (T3/marketing) — konkrét számot nem idéztem belőlük, mert nem közölték a mérési módszertant.
- https://www.pinecone.io/learn/... — a keresés nem hozott új, a témára specifikus (embedding-szolgáltatás-kiesés) tartalmat Pinecone-tól ebben a körben.


---

## SQ-04 — Törlésre jelölt bejegyzés az indexben

# SQ-04 — Meglátogatott linkek, tier-besorolással

Tier-kulcs: **T1** = hivatalos dokumentáció/spec/forráskód/peer-reviewed vagy arXiv paper.
**T2** = megbízható másodlagos VAGY gyártó saját termékére vonatkozó teljesítményállítás.
**T3** = fórum, levelezőlista, vélemény, marketing (hivatalos domainen is, ha fórum).

## T1 — Hivatalos dokumentáció, spec, forráskód, tudományos publikáció

| URL | Mit adott |
|---|---|
| https://www.sqlite.org/fts5.html | Hivatalos FTS5 spec. `delete`, `delete-all`, `rebuild` parancsok pontos definíciója; contentless vs. contentless-delete vs. normál/external content táblák DELETE-viselkedése; `bm25()` képlet N/avgdl/IDF függősége; a `t1_ad` trigger-példa external content táblához. |
| https://arxiv.org/html/2606.18497v1 (= Ghost Vectors: Soft-Deleted Embeddings Remain Reconstructible in HNSW Vector Databases) | ChromaDB/FAISS/Weaviate soft-delete mechanizmusa, mért 4,3%-os latencia-eltérés és 95%-os top-K divergencia soft- vs. valódi törlés között, embedding-rekonstrukció Vec2Text-tel. |
| https://arxiv.org/html/2407.07871v2 (Enhancing HNSW Index for Real-Time Updates) | „unreachable points" formális definíciója, `markDelete` mechanizmus, mért 5–10x lassabb beszúrás `replaced_update`-nél. |
| https://arxiv.org/html/2512.06200 (How Should We Evaluate Data Deletion in Graph-Based ANN Indexes?) | Mért recall-stabilizáció fizikai törlésnél (~0,81 SIFT1B-n), logikai törlés (tombstoning) romló pontossága ismételt frissítéseknél, hibrid „Deletion Control" stratégia. |
| https://openreview.net/pdf?id=lnaC19Pd30 | Ugyanaz a paper OpenReview-tükre — **fetch sikertelen (403)**, az arXiv-változatot használtam helyette. |
| https://github.com/facebookresearch/faiss/wiki/Special-operations-on-indexes | Hivatalos Faiss projekt wiki (a `remove_ids` API dokumentációja a forráskód-repóban). `IndexFlat`, `IndexIVFFlat`, `IDMap` támogatja; szekvenciális indexeknél id-eltolódás törléskor; `DirectMap` Hashtable-lel hatékony részleges törlés. |
| https://github.com/oven-sh/bun/issues/31247 | Hivatalos Bun GitHub repó — ismert csapda: macOS arm64-en SQLite 3.43.2-t linkel, FTS5 UPDATE/DELETE → `SQLITE_CORRUPT_VTAB` / „database disk image is malformed". |
| https://www.elastic.co/docs/reference/elasticsearch/index-settings/history-retention | Hivatalos Elastic dok. Lucene soft delete retenciós beállítások (`retention.lease`, alapértelmezett 12h), a soft delete célja (peer recovery replay). |
| https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-delete-by-query | Hivatalos Elastic API-referencia. Snapshot-alapú működés, verziókonfliktus-kezelés (`conflicts=proceed`), refresh-viselkedés. Segment-merge-ről nem szól (ld. gaps.md). |
| https://qdrant.tech/documentation/ops-optimization/optimizer/ | Hivatalos Qdrant dok. Pontos küszöbértékek: `deleted_threshold: 0.2`, `vacuum_min_vector_number: 1000`; proxy-mechanizmus a szegmens újraírása alatt. |
| https://docs.weaviate.io/weaviate/manage-objects/delete | Hivatalos Weaviate dok. Csak API-szintű leírás (id/kritérium szerinti törlés, `dryRun`, TTL) — belső tombstone-mechanizmust nem részletez ezen az oldalon. |
| https://docs.weaviate.io/weaviate/config-refs/indexing/vector-index | Hivatalos Weaviate dok. `cleanupIntervalSeconds` (alapértelmezett 300s), tombstone-definíció, `TOMBSTONE_DELETION_MIN_PER_CYCLE`/`MAX_PER_CYCLE` környezeti változók. |
| https://github.com/weaviate/weaviate/pull/5700 | Hivatalos Weaviate forráskód-repó (PR cím: „DO NOT MERGE: delay tombstone cleanup by 12h") — megerősíti, hogy a tombstone-takarítás késleltethető/konfigurálható, gyakorlati fejlesztői kontextusban. |
| https://milvus.io/docs/delete-entities.md | Hivatalos Milvus dok. Csak a törlés API-szintű használatát írja le (szűrő/elsődleges kulcs szerint) — belső mechanizmust nem részletez ezen az oldalon. |
| https://milvus.io/blog/2022-02-07-how-milvus-deletes-streaming-data-in-distributed-cluster.md | Hivatalos Milvus blog (a projekt saját csapatától, mérnöki mélységű, forráskód-szintű magyarázat) — logikai törlés bitset+bloom filter mechanizmussal, fizikai törlés csak Compaction-kor. |
| https://specs.meilisearch.dev/specifications/text/0136-documents-soft-deletion.html | Hivatalos Meilisearch tervezési specifikáció (a projekt saját specs-repója). Pontos purge-feltételek: (1) törölt > élő dokumentum, vagy (2) törölt dokumentumok mérete meghalad egy lemez-küszöböt. |
| https://typesense.org/docs/30.2/api/documents.html | Hivatalos Typesense API-dok. Csak a törlés végpontjait írja le, belső (memóriakezelési) mechanizmust nem (ld. gaps.md). |
| https://docs.opensearch.org/latest/api-reference/document-apis/delete-by-query/ | Hivatalos OpenSearch API-dok. Csak rövid funkcionális leírás, belső Lucene-mechanizmust nem részletez (ld. gaps.md). |
| https://nlp.stanford.edu/IR-book/html/htmledition/dynamic-indexing-1.html | Manning/Raghavan/Schütze „Introduction to Information Retrieval" — a szerzők saját, ingyenesen közzétett hivatalos online kiadása (nlp.stanford.edu). Invalidation bit vector, „a correct number of hits for a term is no longer a simple lookup", auxiliary index + periodikus merge stratégia. |

## T2 — Megbízható másodlagos / gyártói saját teljesítményállítás

| URL | Mit adott |
|---|---|
| https://www.elastic.co/blog/lucenes-handling-of-deleted-documents | Elastic saját mérnöki blogja (nem hivatalos spec, hanem magyarázó cikk). Tombstone-bitset mechanizmus, „term statistics will suddenly jump" torzítás, **mért** 18–46%-os lekérdezés-lassulás 50%-os töröltarány mellett (range query: 1,2→0,6 QPS). |

## T3 — Fórum, levelezőlista, harmadik féltől származó tartalom, GitHub issue-vita

| URL | Mit adott |
|---|---|
| https://sqlite.org/forum/forumpost/dde862dbb3 | SQLite hivatalos fórum — „FTS5 Error database disk image is malformed after 'delete'" — kontextus a törlési hibaosztályhoz (nem a Bun-specifikus esethez, de rokon tünet). |
| https://github.com/qdrant/qdrant/issues/6556 | Qdrant GitHub issue — vektor nélküli pontok viselkedése törlés után, közvetett bizonyíték arra, hogy nincs dedikált „undelete" API. |
| https://github.com/qdrant/qdrant/issues/2550 | Qdrant GitHub issue — „Delete vectors for deleted points" — megerősíti, hogy a törölt pontok vektor-adata nem feltétlenül tűnik el azonnal a tárolóból. |
| https://github.com/weaviate/weaviate/issues/5732 | Weaviate GitHub issue — teszt, ami azt jelzi, hogy tombstone-ok a takarítás után is megmaradhatnak bizonyos esetekben (implementációs részletprobléma, nem dokumentációs állítás — csak kontextusnak használtam, nem idéztem belőle állítást). |

## Megtalált, de nem (vagy csak áttételesen) felhasznált linkek

- https://github.com/elastic/elasticsearch/issues/29530, https://github.com/elastic/elasticsearch/pull/30226,
  https://github.com/elastic/elasticsearch/pull/34953 — Elasticsearch saját GitHub-fejlesztési
  vitái a soft delete/tombstone bevezetéséről; nem idéztem belőlük közvetlenül, mert a
  hivatalos „History retention settings" dokumentáció ugyanazt (és megbízhatóbban) mondja ki.
- https://github.com/milvus-io/milvus/discussions/28565, /26828, /24875, /19259 — Milvus
  GitHub Discussions, felhasználói kérdések a compaction/delete viselkedésről; a hivatalos
  blogbejegyzés (2022-02-07) pontosabb és hivatalosabb forrás volt ugyanarra, ezért ezeket
  nem idéztem.
- https://docs.opensearch.org/2.11/security/access-control/document-level-security/ — az
  SQ-01 kutatásban már felhasznált oldal, itt csak kontextusként néztem át (Lucene-level DLS
  módok), nem ide vonatkozó új idézetet nem vettem belőle.
- https://openreview.net/pdf?id=lnaC19Pd30 — **fetch sikertelen, 403-as hiba.** A tartalom
  ugyanaz, mint az arXiv-változat (arxiv.org/html/2512.06200), amit sikerült lekérni és
  idézni — ezért nem jelent adatvesztést, csak jelzem a hibát átláthatóság kedvéért.
- „soft delete" search index anti-pattern témában futtatott általános keresés (33. keresés a
  `searches.md`-ben) kizárólag általános BM25-ismertető cikkeket hozott (GeeksforGeeks,
  Spice AI, DataAspirant stb.) — ezek nem T1/T2 minőségűek és nem szóltak kifejezetten a
  törlés okozta torzításról, ezért egyiket sem idéztem forrásként.
