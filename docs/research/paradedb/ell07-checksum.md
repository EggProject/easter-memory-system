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
