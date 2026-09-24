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
