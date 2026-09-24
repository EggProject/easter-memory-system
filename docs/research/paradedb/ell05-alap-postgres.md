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
