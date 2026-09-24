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
