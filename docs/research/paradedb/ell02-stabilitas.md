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
