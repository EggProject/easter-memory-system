# Szóköz nélküli írásrendszerek (CJK) a szöveges keresésben — megállapítások

Kutatási egység: **sq01**. Tier-jelölés: **T1** = hivatalos dokumentáció / forráskód / peer-reviewed; **T2** = megbízható másodlagos vagy gyártói termékleírás konkrét, ellenőrizhető technikai tartalommal; **T3** = fórum, blog, vélemény, egyedi anekdota.

---

## 1. SQLite FTS5 tokenizálók és a CJK kérdés

**Forrás:** SQLite hivatalos dokumentáció, `fts5.html`, nyers HTML-ként lekérve (`curl`, nem WebFetch-összefoglaló). **[T1]**

FTS5 négy beépített tokenizálót kínál:

- **`unicode61`** (alapértelmezett): Unicode 6.1 szerint minden "L*"/"N*"/"Co" kategóriájú karaktert token-karakternek tekint, a többit elválasztónak; alapból **ékezet-hajtogatást** végez a latin karaktereken ("A", "a", "À", "à", "Â", "â" egyenértékű). Egy CJK-mondat, amelyben nincs elválasztó karakter (szóköz/írásjel), **egyetlen tokenné** olvad össze — a dokumentáció ezt nem mondja ki explicit módon CJK-ra vonatkozóan, de a szabály (elválasztó = írásjel/szóköz Unicode szerint) logikailag ezt eredményezi.
- **`ascii`**: mint `unicode61`, de minden 127 fölötti kódpontot mindig token-karakternek tekint, és nem támogatja a `remove_diacritics` opciót. CJK szempontjából ugyanaz a szóhatár-probléma áll fenn, mint `unicode61`-nél (nincs beépített szegmentálás).
- **`porter`**: wrapper tokenizáló, ami az alatta futó tokenizáló (alapból `unicode61`) kimenetére Porter-szótövezést alkalmaz. A dokumentáció szó szerint kimondja: *"The porter stemmer algorithm is designed for use with English language terms only - using it with other languages may or may not improve search utility."* Kínaira/japánra nem releváns (nincs mit tövezni token szinten, ha maga a tokenizálás sem működik).
- **`trigram`**: *"The trigram tokenizer, which treats each contiguous sequence of three characters as a token, allowing FTS5 to support more general substring matching."* Ez a nyelvfüggetlen megoldás a szóhatár-probléma megkerülésére.

### A `trigram` tokenizáló — szó szerinti dokumentáció

> "The trigram tokenizer extends FTS5 to support substring matching in general, instead of the usual token matching. When using the trigram tokenizer, a query or phrase token may match any sequence of characters within a row, not just a complete token."

Példa a dokumentációból: `CREATE VIRTUAL TABLE tri USING fts5(a, tokenize="trigram")`; a `'"hij klm" NOT stuv'` lekérdezés a `'abcdefghij KLMNOPQRST uvwxyz'` sorra illeszkedik — vagyis **a trigram tokenizáló a szóközön is átnyúló karakter-hármasokat képez**, nem csak szavakon belülieket. Ez fontos különbség a PostgreSQL `pg_trgm`-jéhez képest (ld. 4. pont).

Opciók: `case_sensitive` (0/1, alap 0), `remove_diacritics` (0/1, alap 0; csak akkor állítható 1-re, ha `case_sensitive=0`).

**Korlátok — szó szerint a dokumentációból:**

> "Substrings consisting of fewer than 3 unicode characters do not match any rows when used with a full-text query. If a LIKE or GLOB pattern does not contain at least one sequence of non-wildcard unicode characters, FTS5 falls back to a linear scan of the entire table."

> "If the FTS5 table is created with the detail=none or detail=column option specified, full-text queries may not contain any tokens longer than 3 unicode characters. LIKE and GLOB pattern matching may be slightly slower, but still works. If the index is to be used only for LIKE and/or GLOB pattern matching, these options are worth experimenting with to reduce the index size."

> "The index cannot be used to optimize LIKE patterns if the LIKE operator has an ESCAPE clause."

**LIKE/GLOB támogatás:** *"Unless the remove_diacritics option is set, FTS5 tables that use the trigram tokenizer also support indexed GLOB and LIKE pattern matching."* Ha `case_sensitive=1`, csak GLOB indexelhető, LIKE nem.

**Minimum lekérdezés-hossz:** gyakorlatilag **3 unicode karakter** — ez alatt a MATCH-lekérdezés nem ad találatot. Ez Hungary-releváns is: két-három betűs magyar szavak (pl. "de", "és", "ha") trigram-indexben nem találhatók meg MATCH-csal, csak LIKE/GLOB-bal (és akkor is csak akkor gyors, ha a mintában van legalább egy 3+ karakteres nem-wildcard szakasz).

**Nincs explicit CJK-említés:** a `fts5.html` teljes szövegében **nincs egyetlen "Chinese", "Japanese" vagy "CJK" szó sem** (ellenőrizve grep-pel a teljes nyers dokumentumon). Ez önmagában is fontos negatív eredmény: a hivatalos dokumentáció **nem tárgyalja explicit módon** a CJK-esetet, sem ajánlást, sem figyelmeztetést nem ad hozzá. **[T1 — hiány/negatív találat]**

### Történeti kontextus — mikor és miért került be a trigram tokenizáló

**[T1]** SQLite hivatalos release log, `releaselog/3_34_0.html` (2020-12-01): *"Enhanced FTS5 to support trigram indexes."* — nyers HTML-lekéréssel ellenőrizve.

**[T3 — fórum, csak kontextusnak]** A hivatalos SQLite fórum szála ("Trigram indexes for SQLite", 2020, `sqlite.org/forum/forumpost/c230760fdf`) szerint az igény eredetileg Simon Willison-től jött (PostgreSQL trigram-indexéhez hasonló substring-keresés hiánya miatt), a működő megvalósítást (`ftstri`) Dan Kennedy (SQLite core fejlesztő) írta meg napokon belül, ez került be hivatalosan a 3.34.0-ba. A motiváció **substring-keresés (LIKE-szerű minták)** volt, nem kifejezetten CJK — a CJK-alkalmazhatóság a mechanizmus mellékhatása, nem tervezési cél.

---

## 2. ICU-alapú lehetőség SQLite-ban

**[T1 — kritikus, szó szerinti idézet]** A `fts5.html` "Appendix A: Comparison with FTS3/4" szakasza kimondja:

> "The ICU tokenizer is not available." *(FTS5-re vonatkozóan, a FTS3/4-ből örökölt funkciók listájában, mint ami NEM érhető el FTS5-ben)*

Ez azt jelenti: **az FTS5-nek nincs beépített ICU tokenizálója**. Az ICU-alapú tokenizálás csak a régebbi **FTS3/FTS4** modulban létezik.

**[T1]** `fts3.html` (nyers HTML): az ICU tokenizáló FTS3/4-ben fordítási opció:

> "If the C version of the ICU library is available, then FTS may also be compiled with the SQLITE_ENABLE_ICU pre-processor macro defined. Compiling with this macro enables an FTS tokenizer that uses the ICU library to split a document into terms (words) using the conventions for a specified language and locale."

> "If this extension is compiled with the SQLITE_ENABLE_ICU pre-processor symbol defined, then there exists a built-in tokenizer named 'icu' implemented using the ICU library. [...] CREATE VIRTUAL TABLE thai_text USING fts3(text, tokenize=icu th_TH) [...] The ICU tokenizer implementation is very simple. It splits the input text according to the ICU rules for finding word boundaries and discards any tokens that consist entirely of white-space."

Tehát az FTS3/4 ICU-tokenizálója:
- **Fordítás-idejű függőség**: `-DSQLITE_ENABLE_ICU`, és a rendszernek linkelnie kell a C-s ICU könyvtárral ("if the C version of the ICU library is available").
- Locale-paraméterezhető (pl. `icu th_TH`), de a dokumentáció maga mondja: *"very simple"* — csak ICU szóhatár-keresést végez, nem morfológiai elemzést.
- **FTS5-ben nem elérhető** — ez azt jelenti, hogy egy FTS5-alapú rendszer az ICU-t **csak úgy** tudná igénybe venni, ha (a) visszaáll FTS3/4-re, vagy (b) saját egyedi FTS5-tokenizálót ír C-ben, ami maga hívja az ICU `BreakIterator`-t (ilyen közösségi projektet nem találtunk hivatalos SQLite-forrásban; a kutatás nem talált hivatalos "fts5_icu" modult).

**Az ár (méret/függőség) — [T1, de elavult adat]:** Az ICU projekt saját hivatalos oldala (`icu.unicode.org/charts/icu4c-footprint`) ad méretszámokat, de ezek egy **régi ICU-verzióra** (icudt30.dll, kb. ICU 3.0 körüli) vonatkoznak:

> "8.17 MB normal / 7.98 MB ...trnsfiles.mk / 7.00 MB ...ucmebcdic.mk / 5.43 MB ...ucmfiles.mk / 4.38 MB ...ucmcore.mk / 2.88 MB ...resfiles.mk / 1.18 MB ...colfiles.mk / 1.06 MB ...miscfiles.mk"

Ez a legkisebb konfiguráció is (~1 MB) tartalmazza a BiDi-t, normalizációt, IDNA-t, egyszerű Unicode-konverziót, UnicodeSet-et, sima UCA-kollációt és break iteration-t — vagyis a **teljes csomag méretmentes verziója sem triviálisan kicsi**, és ez egy 15+ éve nem frissített hivatalos oldal, modern ICU-verziókra vonatkozó friss, hivatalos méretszámot **nem találtunk** ebben a kutatásban (gap — ld. `gaps.md`).

**Tervezési következtetés (nem mért adat, hanem a fentiekből levezetett ajánlás):** Az SQLite ICU-útvonal FTS5 mellett **nem opció** dokumentáció szerint; FTS3/4-re váltás + C-fordítási ICU-függőség + a bináris méretének növekedése (build-specifikus, több MB-tól akár 10+ MB-ig, ICU-verziótól és modularizációtól függően) egy beágyazott/eldobható-index rendszernél valószínűleg aránytalanul nagy ár egy olyan tokenizálóért, ami a dokumentáció saját szavaival is "very simple".

---

## 3. Index-méret növekedés trigram tokenizálóval

**Hivatalos (T1) adat nincs közvetlenül a trigram tokenizálóra.** A `fts5.html` egyetlen konkrét méret-összehasonlítása a `detail=` opcióra vonatkozik (nem a tokenizáló-választásra), és ott is egy **nem-trigram**, általános e-mail-korpuszra:

> "In one test that indexed a large set of emails (1636 MiB on disk), the FTS index was 743 MiB on disk with detail=full, 340 MiB with detail=column and 134 MiB with detail=none."

Ez azt mutatja, hogy a `detail=none`/`detail=column` opciók (amelyeket a dokumentáció kifejezetten **trigram-táblák méretcsökkentésére is ajánl**, ld. 1. pont fenti idézete) 5,5×-ös (743→134 MiB) csökkenést hozhatnak — de ez nem trigram-specifikus mérés.

**Közösségi (T2/T3) mérések trigram-specifikusan — nagy szórással, tehát tartalomfüggő:**

1. **[T2, gyakorlati blogbenchmark]** `andrewmara.com` blogbejegyzés, 18,2 millió soros adathalmazon: az alap tábla **1,3 GiB**; teljes FTS5 trigram index hozzáadása után az adatbázis **3,7 GiB**-ra nőtt (tehát az index maga kb. **2,4 GiB**, azaz nagyjából a forrásadat **185%-a**); `detail='none'`-nal az adatbázis **2,8 GiB**-ra csökkent (index-rész kb. **1,5 GiB**, a teljes trigram-index kb. felére csökkentve). Cserébe LIKE-lekérdezés 1,75 mp → 10-30 ms (50-100×-os gyorsulás).
2. **[T3, GitHub issue, egyedi eset]** `NousResearch/hermes-agent` #43690 issue: 27,45 MB forrásszöveg (60 776 üzenet) esetén a **normál FTS5 index 50 MB (1,8×)**, a **trigram FTS5 index 502 MB (18,3×)** — de a szerző maga jelzi, hogy ezt a szélsőséges arányt **strukturált JSON-mezők** (ismétlődő kulcsnevek) trigram-indexelése torzítja, tehát természetes nyelvi szövegre **nem** általánosítható közvetlenül. `detail='none'`-nal kb. 37,5%-os (~187 MB) méretcsökkenést mértek.
3. **[T3, gyakorlati anekdota]** Egy dev.to cikk szerint egy egyedi (nem beépített, JavaScript-oldali) bigram-előfeldolgozásos megoldás kínai szövegre kb. **2×-es** adatbázisméret-növekedést okozott 8,3 MB forrásszövegen (15 119 chunk), 0-3 ms lekérdezési idővel.

**Összegzés — mért adat vs. hiány:** A hivatalos SQLite-dokumentáció **nem közöl trigram-specifikus méretszorzót**. A talált közösségi mérések 1,85×-től 18,3×-ig terjednek, ami azt mutatja, hogy **a szorzó erősen tartalomfüggő** (természetes nyelv vs. strukturált/ismétlődő adat), és **nincs egységes, megbízható "X×-es" szám**, amit egy tervezési dokumentumban idézni lehetne mértékadó adatként. Ha a rendszer tervezésénél konkrét méretbecslés kell, azt **a saját korpuszon empirikusan kell megmérni** — ez tervezési ajánlás, nem mért tény.

---

## 4. Mások megoldásai: PostgreSQL, Meilisearch, Typesense, Elasticsearch/OpenSearch

### PostgreSQL

**[T1]** A hivatalos `textsearch-parsers.html` dokumentáció szerint az alapértelmezett szövegkereső-parser "szóhatár"-fogalma a `lc_ctype` locale-beállítástól függ, és a dokumentáció **nem tesz külön említést** a CJK-ról vagy szóköz nélküli írásrendszerekről — csak annyit mond: *"In most European languages, token types word and asciiword should be treated alike."* Ez negatív találat: a hivatalos parser-dokumentáció **hallgat** a CJK-esetről.

**[T1]** A hivatalos `pg_trgm` (trigram hasonlósági keresés) modul dokumentációja: *"pg_trgm ignores non-word characters (non-alphanumerics) when extracting trigrams from a string. Each word is considered to have two spaces prefixed and one space suffixed."* — vagyis a PostgreSQL trigramja **szóhatár-tudatos**: nem képez szóközön átnyúló trigramot, ellentétben az SQLite trigram tokenizálójával (ld. 1. pont).

**[T2, projekt-dokumentáció]** A `pg_bigm` (NTT eredetű, PostgreSQL-kiegészítő) hivatalos dokumentációja explicit összehasonlító táblázatot közöl a `pg_trgm`-mel:

> "Full text search for non-alphabetic language (e.g., Japanese): pg_trgm = Not supported (*1); pg_bigm = Supported."
> "(*1) You can use full text search for non-alphabetic language by commenting out KEEPONLYALNUM macro variable in contrib/pg_trgm/pg_trgm.h and rebuilding pg_trgm module. But pg_bigm provides faster non-alphabetic search than such a modified pg_trgm."
> "Full text search with 1-2 characters keyword: pg_trgm = Slow (*2, csak sequential/full index scan); pg_bigm = Fast."

Ez kulcsfontosságú, eddig nem várt eredmény: **a PostgreSQL hivatalos trigram-modulja (`pg_trgm`) alapértelmezett fordítással KIZÁRJA a nem-alfanumerikus (pl. japán) karaktereket** (a `KEEPONLYALNUM` makró miatt), és csak forráskód-módosítás + újrafordítás után használható CJK-ra. Emiatt jött létre külön a `pg_bigm` **2-gram** (nem 3-gram!) modul kifejezetten CJK célra. Más CJK-specifikus PostgreSQL-megoldások: `zhparser` (kínai, szótár-alapú szegmentálás), `pg_jieba` (kínai, jieba-alapú), `pg_cjk_parser` (CJK karaktereket 2-gramra bontó egyedi parser).

**Következtetés:** PostgreSQL-ökoszisztémában **nincs egységes, univerzális megoldás** — a beépített trigram alapból nem CJK-kompatibilis, és a közösség több, egymástól független, **nyelv-specifikus** kiterjesztéssel (bigram vagy szótár-alapú szegmentáló) oldja meg a problémát.

### Elasticsearch / OpenSearch

**[T1, OpenSearch hivatalos dokumentáció, nyers HTML]**

> "The built-in cjk analyzer is designed for Chinese, Japanese, and Korean (CJK) text. It uses bigram tokenization to break down CJK text into overlapping two-character sequences, which is effective for languages that don't use spaces to separate words. You may find that the icu_analyzer in the ICU analysis plugin works better for CJK text than the cjk analyzer."

A `cjk` analizátor belső felépítése: `standard` tokenizáló → `cjk_width` → `lowercase` → `cjk_bigram` → `stop` szűrő. Tehát a Lucene-alapú motorok **beépített, nyelv-agnosztikus fallback-ja is 2-gram (bigram), nem 3-gram (trigram)** CJK-ra.

**[T1, Elastic hivatalos dokumentáció]** Emellett léteznek **nyelv-specifikus, dictionary-alapú** analizátor-pluginok:
- **`smartcn`** (kínai): *"provides an analyzer for Chinese or mixed Chinese-English text. This analyzer uses probabilistic knowledge to find the optimal word segmentation for Simplified Chinese text."* — fontos: **explicit módon kezel kevert kínai-angol szöveget egyetlen analizátorral**, nyelvfelismerés nélkül.
- **`kuromoji`** (japán): a `kuromoji_tokenizer` a **MeCab-IPADIC szótárt** használja morfológiai szegmentáláshoz (analízis-lánc: `CJKWidthCharFilter` → `kuromoji_tokenizer` → `kuromoji_baseform` → `kuromoji_part_of_speech` → `ja_stop` → `kuromoji_stemmer` → `lowercase`).
- **`nori`** (koreai, hivatalos Elastic blogbejegyzés, 2018): a **mecab-ko-dic** szótárat használja, amely a MeCab motorra épül (ugyanaz a technológia, mint a japán elemzésnél, csak más szótárral). Az Elastic blog konkrét méretadatot közöl: *"The mecab-ko-dic dictionary [...] The total size on disk after decompression of the latest distribution is 219MB."* A Nori-modul ezt bináris formátumra fordítja, mert *"we don't want to distribute 200MB of dictionary in a Lucene's module."* **[T1, mért adat: 219 MB nyers szótárméret]**

**Összegzés Elasticsearch/OpenSearch-re:** **Háromféle stratégia párhuzamosan létezik** ugyanabban az ökoszisztémában: (1) nyelv-agnosztikus bigram (`cjk` analizátor, gyors, kis függőség, gyengébb pontosság), (2) valószínűségi szegmentálás egy adott nyelvre (`smartcn`, kevert nyelvű szöveget is kezel), (3) szótár-alapú morfológiai elemzés (`kuromoji`, `nori`, nagy [~200 MB nyers] szótár-függőség, legpontosabb). **Nincs egyetlen "helyes" válasz** — a választás a pontosság/méret/komplexitás háromszögében történik, és ezt maga a hivatalos OpenSearch-dokumentáció is elismeri, amikor a `cjk` analizátornál explicit ajánlja az `icu_analyzer` kipróbálását alternatívaként.

### Meilisearch

**[T1, hivatalos dokumentáció + hivatalos GitHub-repó, `charabia`]**

> "Chinese, Japanese, and Korean do not use whitespace between words. Meilisearch's dedicated pipelines handle segmentation for these languages automatically."

A tokenizálás kétlépéses: (1) a dokumentumot **írásrendszer (script) szerint** szegmentálja (latin ábécé, kínai hanzi stb.), (2) minden szegmensre a megfelelő nyelv-specifikus pipeline-t futtatja (kínai, japán, héber, thai, khmer külön kezelést kap). **Ez nem dokumentum-szintű nyelvfelismerés, hanem karakter-szintű írásrendszer-detektálás** — közvetlenül releváns az 5. kérdésre (ld. lent).

### Typesense

**[T1, hivatalos dokumentáció]** A `locale` mezőparaméterrel (pl. `"locale": "zh"`, `"ja"`, `"ko"`, `"th"`) engedélyezhető a nyelv-specifikus szegmentálás; emellett van `pre_segmented_query` opció, amivel a kliens saját (pl. ML-alapú) szegmentálást adhat át kínai lekérdezésekhez, ha a beépített heurisztika nem elég pontos. Ez azt jelenti, hogy Typesense-nél **a fejlesztőnek explicit módon meg kell mondania a mező nyelvét** (nem automatikus script-detektálás, mint Meilisearch-nél).

---

## 5. Kell-e nyelvfelismerés vegyes nyelvű tartalomhoz?

Nincs egységes válasz a forrásokban, de **konvergáló minta rajzolódik ki**:

- **Meilisearch**: **nem** dokumentum-szintű nyelvazonosítást (language ID) használ, hanem **Unicode írásrendszer (script) szerinti szegmentálást** karakterfutamokra, majd script-enkénti pipeline-t alkalmaz ugyanazon a dokumentumon/mezőn belül is. Ez **egyetlen indexben, egyetlen mezőben** kezeli a kevert nyelvű tartalmat, nyelv-tag nélkül.
- **Elasticsearch `smartcn`**: explicit kimondja, hogy **egyetlen analizátor** kezeli a "Chinese or mixed Chinese-English text" esetet — tehát legalább egy dictionary-alapú, nyelv-specifikus analizátor is képes vegyes tartalmat kezelni **külön mező/index nélkül**, ha az egyik nyelv (kínai) a domináns, karakterkészlet alapján megkülönböztethető komponens.
- **Elasticsearch/OpenSearch általános gyakorlat viszont**: a `kuromoji`, `nori`, `smartcn` mind **mező-szintű, explicit konfigurációjú** analizátorok (a mappingben be kell állítani, melyik mezőhöz melyik analizátor tartozik) — ez facto **per-nyelv mező vagy per-nyelv index** mintát feltételez, ha több, egymástól morfológiailag távoli nyelvet (pl. magyar + kínai) kell egyszerre, jó minőségben kezelni ugyanabban a rendszerben.
- **Trigram/n-gram megoldások (SQLite trigram, Postgres `pg_trgm`, Lucene `cjk` bigram)**: ezek **explicit módon nyelv-agnosztikusak** — nem igényelnek sem nyelvfelismerést, sem script-detektálást, mert karakter-szinten, egységesen dolgoznak. Ez az egyetlen kategória, ahol **egyetlen tokenizáló, egyetlen indexszel, nyelvfüggetlenül** lefedhető a kevert tartalom — cserébe a pontosság/relevancia (BM25-minőség) alacsonyabb, mint egy nyelv-specifikus morfológiai elemzőé (ld. 7. pont).

**Következtetés (részben mért adat [Meilisearch/ES dokumentáció ténye], részben tervezési levezetés):** **Nem szükséges teljes dokumentum-szintű nyelvazonosítás** egy vegyes nyelvű (magyar+angol+kínai) index kezeléséhez, ha script-alapú (Unicode-blokk szerinti) detektálásra vagy nyelv-agnosztikus n-gram tokenizálásra épül a rendszer. Teljes nyelvazonosítás (langid/cld3-szerű) csak akkor válik szükségessé, ha **dictionary-alapú, nyelv-specifikus morfológiai elemzőt** (kuromoji/nori-szerű) akarunk **automatikusan, kézi konfiguráció nélkül** kiválasztani soronként/mezőnként — ezt a forrásokban **egyik vizsgált rendszer sem** old meg tisztán automatikus, teljes nyelvazonosítással; mind kézi mező-konfigurációra vagy script-detektálásra épít.

---

## 6. Többnyelvű beágyazó modellek CJK-teljesítménye — mért adat

**Forrás:** M3-Embedding (BGE-M3) cikk, Chen et al., 2024, ACL Findings + arXiv:2402.03216 (peer-reviewed, **[T1]**). A cikk 2. táblázata a **MIRACL fejlesztői halmazon** (18 nyelv, közte `zh`, `ja`, `ko`), nDCG@10 metrikával hasonlítja össze a modelleket, Pyserini hivatalos benchmark-eljárással.

A nyers táblázatot magunk rekonstruáltuk a HTML-kivonatból (oszlopsorrend: Avg, ar, bn, en, es, fa, fi, fr, hi, id, **ja, ko**, ru, sw, te, th, **zh**, de, yo):

| Modell | zh (kínai) | ja (japán) | ko (koreai) | Átlag (18 nyelv) |
|---|---|---|---|---|
| BM25 (lexikai, kontroll) | 56,1 | 31,2 | 37,1 | 31,9 |
| **mE5-large** (multilingual-e5-large) | 56,0 | 70,6 | 66,5 | 65,4 |
| **BGE-M3 — csak Dense** | 61,7 | 72,8 | 69,9 | 67,8 |
| **BGE-M3 — All** (dense+sparse+multi-vec) | **63,9** | **75,2** | **72,2** | **70,0** |

*(Az mE5-large sorokat a BGE-M3 szerzői mérték saját, azonos Pyserini-protokollal, tehát ez egy harmadik fél által, azonos módszertannal futtatott összehasonlítás, nem a BGE-M3 saját marketinganyaga — ez erősíti a megbízhatóságát.)*

**Mért megállapítás:** BGE-M3 minden CJK nyelven felülmúlja a multilingual-E5-large-ot ezen a benchmarkon (zh: +7,9 pont, ja: +4,6 pont, ko: +5,7 pont, kombinált módban), és mindkét modell **jelentősen jobb**, mint a tiszta BM25-lexikai keresés (zh: 56,1 → 63,9; ja: 31,2 → 75,2; ko: 37,1 → 72,2 — utóbbi kettőnél a BM25 kirívóan gyenge, ami maga is releváns adat: **japán és koreai nyelven a lexikai/BM25-keresés önmagában nagyon gyenge** ezen a benchmarkon, alátámasztva a kérdésben leírt aggodalmat, hogy embedding-kiesés esetén a japán/koreai keresés minősége drasztikusan romlana).

**Fontos módszertani megjegyzés:** A BGE-M3 cikk absztraktja azt állítja, hogy a modell *"more than 100 working languages"*-t támogat "uniform"-módon, és *"new state-of-the-art results"*-t ér el több benchmarkon — ez **általános állítás**, a fenti konkrét számok viszont **mért, tábla-szintű adatok** ugyanabból a cikkből. A multilingual-E5 saját eredeti cikkét (arXiv:2402.05672, Wang et al.) nem dolgoztuk fel részletesen táblázat-szinten ebben a körben (időkorlát) — a fenti mE5-large-számok a **BGE-M3 szerzőinek saját futtatásából** származnak, nem az E5-cikk saját publikált számaiból; ha a két forrás számai eltérnének, azt nem tudjuk ellenőrizni ebben a körben (**gap**, ld. `gaps.md`).

---

## 7. Van-e tokenizáló, ami magyarra ÉS kínaira is elfogadható? A trigram ára európai nyelveken

Ez a legkényesebb pont — itt a forrásokban talált bizonyíték **áttételes**, nem közvetlen mérés az SQLite FTS5 trigram + magyar + BM25 kombinációra.

### Amit T1 forrás valóban mér: karakter-n-gram és európai nyelvi visszakeresés

**[T1, peer-reviewed]** McNamee & Mayfield: *"Character N-Gram Tokenization for European Language Text Retrieval"* (Information Retrieval journal, Springer; CLEF 2002 adatokon). Az absztrakt szerint:

> A kutatók megvizsgálták, hogy "language-neutral methods can achieve accuracy comparable to language-specific methods with less concomitant software complexity". A **4-gram** karaktertokenizálást találták optimálisnak európai nyelvekre ("n = 4 is a good choice for those languages"). Legfontosabb konklúziójuk: *"accuracy using n-gram indexing rivals or exceeds accuracy using unnormalized words, for both monolingual and bilingual retrieval."* Kompromisszumként megnövekedett tárolási és feldolgozási igényt ("increased storage and time requirements") jegyeztek fel.

**Ennek a résznek a korlátai, amit fontos kimondani:**
- Ez **4-gram**-ra vonatkozik, nem 3-gramra (SQLite FTS5 trigramja fixen n=3). A cikk (csak az absztraktból elérhető, a teljes szöveg fizetőfal mögött van) szerint több n-értéket teszteltek, és n=4-et találták jobbnak — ami közvetve arra utal, hogy **n=3 valamivel gyengébb** lehetett, mint n=4, de ezt a konkrét számot **nem sikerült megszerezni** (a teljes cikk nem volt elérhető ebben a kutatási körben — **gap**).
- Az összevetés "unnormalized words" (nem tövezett szóalapú keresés) ellen történt, **nem** egy jól hangolt, nyelv-specifikus stemmelt/lemmatizált kereséssel szemben. Vagyis az eredmény azt mondja: *"n-gram jobb vagy egyenlő, mint a puszta szóalapú keresés"*, nem azt, hogy *"n-gram jobb, mint egy jó magyar sztemmer"*.
- Ez **klasszikus IR-relevancia** mérés (nDCG/precision-recall jellegű CLEF-metrikák), **nem** SQLite FTS5 BM25 + kapu-mechanizmus kombinációra vonatkozik, és nem magyar nyelvre specifikusan (a CLEF 2002 korpusz elsősorban francia, olasz, spanyol, holland, német, finn nyelveket tartalmazott — magyar nem szerepelt benne, agglutináló nyelvre viszont a finn igen, ami morfológiailag rokon jellegű a magyarral, tehát **indikatív, de nem közvetlen bizonyíték magyarra**).

### Amit a tervezői/gyakorlati forrásokból (T2/T3) tudunk

- **A SQLite trigram tokenizáló szóközön is átnyúló trigramokat képez** (ld. 1. pont — a hivatalos példa `"hij klm"` mintát ad vissza, ami két szót összekötő szóközt tartalmaz). Ez elméletileg **több véletlen substring-egyezést (fals pozitívot)** okozhat szóhatáron átnyúlva, mint egy szóhatár-tudatos trigram (mint a PostgreSQL `pg_trgm`-je, amely **explicit módon kizárja** a szóközön átnyúló trigramokat: *"Each word is considered to have two spaces prefixed and one space suffixed"*). **Ez logikai következtetés a dokumentációk eltéréséből, nem mért precíziós adat.**
- **[T3, közösségi projekt]** A `streetwriters/sqlite-better-trigram` projekt kifejezetten azért készült, mert az eredeti SQLite trigram nem ismeri fel a szóhatárokat (`"i am a bird"` → `['i a', ' am', 'm a', ' a ', ' bi', 'bir', 'ird']` helyett `['i', 'am', 'a', 'bir', 'ird']`-t akar), és ezt "1,6×-szer gyorsabb"-nak mérték (saját, nem független benchmark, egyetlen 289 KB-os mintán) — ez **sebesség-mérés, nem relevancia/pontosság-mérés**, tehát nem válaszolja meg közvetlenül, hogy "romlik-e a magyar keresés minősége".
- **Kis szavak problémája mindkét nyelvcsoportnál jelentkezik, csak más okból**: CJK-nál azért, mert a szavak natívan 1-2 karakteresek (és a trigram minimum 3 karaktert igényel MATCH-hoz); magyarnál a rövid kötőszavaknál/névelőknél ("de", "és", "ha", "a", "az") jelentkezik ugyanez a korlát. A `pg_bigm` dokumentáció külön kiemeli ezt problémaként a trigram (`pg_trgm`) kapcsán: *"Full text search with 1-2 characters keyword: pg_trgm = Slow"*.

### Mi az egyenes válasz a kérdésre

**Nem találtunk sem T1, sem megbízható T2 forrást, amely közvetlenül megmérte volna, hogy az SQLite FTS5 trigram tokenizáló (n=3, szóköz-áthatoló) mennyivel rontja (vagy nem rontja) a magyar nyelvű BM25-alapú keresési relevanciát egy szóalapú (`unicode61`) tokenizálóhoz képest.** A legközelebbi releváns bizonyíték (McNamee & Mayfield, n=4, más nyelvekre, "unnormalized words" ellen mérve) **azt sugallja, hogy a károsodás valószínűleg nem drámai**, sőt karakter-n-gram módszerek történelmileg **versenyképesek voltak** európai nyelveken egy tövezés-mentes alapvonallal szemben — de ez **nem egyenértékű bizonyíték** a konkrét SQLite-implementációra, konkrét n=3-ra, vagy konkrét magyar nyelvre. **Ezt explicit hiányként rögzítjük** (ld. `gaps.md`), a feladat utasításának megfelelően.

---

# Mért adat vs. tervezési ajánlás — összefoglalva

## Mért adatok (forrással, számmal)
- FTS5 trigram minimum 3 unicode karakteres substring-egyezés; ez alatt MATCH nem talál semmit. **[T1]**
- SQLite trigram tokenizáló 3.34.0-ban jelent meg (2020-12-01). **[T1]**
- `detail=full/column/none` egy 1636 MiB e-mail-korpuszon: 743/340/134 MiB (nem trigram-specifikus). **[T1]**
- Nori (koreai) szótár: 219 MB nyers méret lemezen tömörítetlenül. **[T1]**
- ICU4C adatfájl-méretek (elavult, ICU~3.0-hoz): 8,17 MB (teljes) → 1,06 MB (minimál konfiguráció). **[T1, dated]**
- BGE-M3 vs. multilingual-E5-large MIRACL nDCG@10: zh 63,9 vs 56,0; ja 75,2 vs 70,6; ko 72,2 vs 66,5 (BGE-M3 mindenhol jobb). **[T1]**
- BM25-kontroll MIRACL-on: zh 56,1; ja 31,2; ko 37,1 (feltűnően gyenge ja/ko-n). **[T1]**
- Trigram-index méretnövekedés közösségi mérésekben: 1,85× (185%, természetes szöveg, andrewmara.com) — 18,3× (szélsőséges, strukturált JSON, hermes-agent issue). **[T2/T3, nagy szórás, nem általánosítható egyetlen számra]**
- Karakter-4-gram európai nyelvi visszakeresésben "rivals or exceeds" a tövezetlen szóalapú keresést (McNamee & Mayfield, CLEF 2002). **[T1, csak absztrakt]**

## Tervezési ajánlások (levezetett, NEM mért állítás)
- Ha a szöveges láb nem eshet ki teljesen CJK-nál, egy `trigram` tokenizálós FTS5-tábla (esetleg `detail=none`-nal méretoptimalizálva) reális, dokumentált, beépített megoldás — ár: index-méret növekedés (mértéke korpuszfüggő, empirikusan mérendő), és rövid (1-2 karakteres) kulcsszavak nem találhatók MATCH-csal.
- Az ICU-útvonal FTS5 alatt **nem járható** dokumentáció szerint; ha ICU-minőségű szegmentálás kell, az vagy FTS3/4-re visszaállást, vagy egyedi C-tokenizáló írását igényelné — mindkettő jelentős többletmunka egy "kapu" mechanizmushoz képest.
- Vegyes nyelvű tartalomhoz nem feltétlenül kell teljes nyelvfelismerés; Unicode-script-alapú detektálás (mint a Meilisearch `charabia`-ja) elegendő lehet a tokenizáló-útvonal kiválasztásához.
- A "kapu" (minden szó együtt kell hogy előforduljon) explicit CJK-kezelést igényel, mert szóhatár nélkül a "szavakra bontás" fogalma maga értelmezhetetlen — egy trigram-alapú kapu-logika (pl. "minden 3-karakteres szegmens előfordul") lenne a nyelv-agnosztikus megfelelője, de ennek tervezését/mérését ez a kutatási kör nem vizsgálta (a kérdés nem is kérte).

---

# Mi az, amiben biztos vagyok / Mi az, amiben nem

**Biztos vagyok benne (közvetlen, ellenőrzött, elsődleges forrásból):**
- Az FTS5 négy beépített tokenizálója pontosan azok, amiket a dokumentáció leír; az ICU tokenizáló FTS5-ben nem elérhető, csak FTS3/4-ben, fordítási opcióként.
- A trigram tokenizáló szóközön átnyúló, 3 unicode-karakteres, nyelv-agnosztikus n-gramokat képez, minimum 3 karakteres egyezési korláttal.
- A hivatalos SQLite FTS5/FTS3 dokumentáció sehol nem említi explicit módon a kínai/japán/CJK esetet.
- A BGE-M3 (peer-reviewed) mérése szerint CJK nyelveken (zh/ja/ko) felülmúlja a multilingual-E5-large-ot a MIRACL benchmarkon, és a BM25-kontrollhoz képest mindkét embedding-modell nagy előnyben van, különösen japán/koreai nyelven.
- Az Elasticsearch/OpenSearch/Lucene-ökoszisztéma a CJK-t háromféle, egymástól eltérő stratégiával kezeli (bigram, valószínűségi szegmentálás, szótár-alapú morfológia), és a PostgreSQL beépített trigram-modulja (`pg_trgm`) alapból **nem** támogatja a nem-alfanumerikus (CJK) karaktereket.

**Nem vagyok biztos benne / a kutatás nem tudta lezárni:**
- Nincs megbízható, közvetlen mérés arra, hogy az SQLite FTS5 trigram tokenizáló mennyivel (ha egyáltalán) rontja a magyar nyelvű keresési relevanciát egy szóalapú tokenizáláshoz képest — ez a legfontosabb nyitott kérdés a 7. pontban, és a feladat kifejezett kérésének megfelelően ezt hiányként, nem becsléssel zárjuk.
- Nincs friss (2020-as évek), hivatalos ICU4C méretadat — csak egy ~15+ éves hivatalos oldal régi számai álltak rendelkezésre.
- A trigram-index méretnövekedésére nincs egységes, megbízható szorzó — a talált közösségi mérések 1,85×-től 18,3×-ig szórnak, erősen tartalomfüggően.
- Nem sikerült elérni a McNamee & Mayfield cikk teljes szövegét (fizetőfal), csak az absztraktot — a pontos n=3 vs. n=4 összehasonlító számok nem ellenőrizhetők.
- A multilingual-E5 saját publikált benchmark-számait (nem a BGE-M3 cikk általi újramérést) nem dolgoztuk fel közvetlenül ebben a körben.
