# Hiányok — amire nem találtunk választ

Kampány: `kereses-indexeles` · 2026-09-08

> Al-kérdésenként bontva, ahogy a kereső ügynökök rögzítették.


---

## SQ-01 — Hol szűrjön a jogosultság a keresésben

# SQ-01 — Hiányosságok (amire nem találtam választ)

## 1. RRF-specifikus szűrési sorrend
Nem találtam olyan forrást (sem hivatalos dokumentációt, sem tudományos publikációt), amely
kifejezetten a **Reciprocal Rank Fusion** kontextusában mondaná ki, hogy a jogosultsági
szűrésnek a két láb (lexikai, vektoros) egyesítése előtt vagy után kell történnie.

Amit próbáltam: `hybrid search RRF reciprocal rank fusion apply filter before or after
fusion`, az OpenSearch RRF-bevezető blog elolvasása, az Azure „Hybrid Search Scoring (RRF)"
oldal célzott lekérdezése. Ezek a fúziós képletet és a súlyozást tárgyalják, a
jogosultság-szűrés helyét nem.

**Miért lehet ez így:** valószínűleg azért, mert a gyakorlatban minden vizsgált rendszer
(6. pont a `megallapitasok.md`-ben) mindkét lábban *saját maga* szűr a lekérdezés szintjén,
így a kérdés a gyakorlatban fel sem merül — nincs olyan éles termék, ami a fúzió *utáni*
közös eredménylistán szűrne. Ez viszont az én következtetésem, nem egy forrás állítása.

## 2. Lapozás mint szivárgási csatorna kereső-ACL kontextusban
A kérdésben felsorolt csatornák közül a „lapozás" (pagination) esetére nem találtam
kereső-index/ACL-specifikus dokumentált esetet vagy szakirodalmat. A keresések
(„pagination" leak hidden results total count access control search API design) általános
API-tervezési cikkeket adtak vissza (Elasticsearch Labs pagination tutorial, Azure
page-layout dokumentáció), amelyek a lapozás *mechanikáját* írják le, nem a jogosultsági
szivárgás szempontjából.

## 3. „Did you mean" / autocomplete szivárgás kereső-ACL kontextusban
Hasonlóan, a keresés („autocomplete suggestion leak private data search 'did you mean'
information disclosure") nem hozott kereső-index-ACL-specifikus találatot. A releváns
találatok (Mastodon actor-index bug, böngésző-autofill phishing, Google Docs
megosztási hiba) más problémakörre vonatkoznak. Nem találtam publikált esetet arra, hogy egy
dokumentum-szintű ACL-lel védett keresőmotor „did you mean" vagy autocomplete javaslata
konkrétan felfedte volna egy jogosulatlan dokumentum létezését.

**Mit próbáltam még nem:** nem kerestem rá kifejezetten Elasticsearch/OpenSearch
"completion suggester" + DLS kombinációra dedikáltan — ez egy nyitva hagyott irány, ha a
téma később élesebbre kerül.

## 4. SQLite FTS5 — nincs hivatalos (T1) ajánlás a jogosultsági JOIN-ra
A hivatalos `fts5.html` specifikáció (ellenőrizve szó szerinti kereséssel) nem tárgyalja a
JOIN-t, a query planner FTS5-specifikus viselkedését, sem az ACL-mintát. Amit találtam,
kizárólag a hivatalos SQLite fórumból (T3) származik — hiteles (a projekt fő fejlesztőitől),
de nem hivatalos dokumentáció. Nem találtam olyan blogot vagy esettanulmányt sem, amely
kifejezetten „FTS5 + jogosultsági tábla JOIN" mintát írna le performancia-számokkal.

## 5. OpenSearch DLS önálló teljesítmény-overhead
Az Eliatra blog (T2) a saját access-control-réteg *optimalizációjának* előtte/utána
összehasonlítását adja (58%/542% javulás), de nem közöl abszolút, „mennyivel lassabb a
sima keresés a DLS bekapcsolása nélkül vs vele" jellegű alapmérést. A hivatalos OpenSearch
dokumentáció is csak annyit mond, hogy „keep [DLS queries] simple to minimize the
performance impact" — konkrét szám nélkül.

## 6. Elasticsearch DLS + kNN integráció mélysége
Megtaláltam, hogy a kNN `filter` paraméter pre-filter, és hogy a DLS role-query is egy
query-alapú mechanizmus — de nem találtam olyan hivatalos forrást, amely kifejezetten
kimondaná, hogy a DLS role-query automatikusan bekerül-e a kNN `filter`-be (azaz valódi
pre-filterként viselkedik-e kNN esetén is), vagy csak a hagyományos (BM25) lábban garantált
ez, a kNN lábban esetleg más (post-filter jellegű) útvonalon fut. Két dedikált Elastic
blogbejegyzést (`vector-search-filtering`, `dls-internal-knowledge-search`) is megnéztem,
egyik sem kötötte össze explicit a két mechanizmust.

## 7. Meilisearch/Typesense — pre- vagy post-filter technikailag?
Mindkét rendszernél megvan a *funkcionális* garancia (a kliens nem kerülheti meg a beégetett
szűrőt), de egyik hivatalos dokumentáció sem mondja ki explicit technikai kifejezésekkel,
hogy ez a rangsoroláshoz/pontozáshoz képest elő- vagy utószűrésként van-e implementálva
motor-szinten. (A Meilisearch esetében találtam utalást a "roaring bitmap" alapú szűrő
implementációra a Kerollmops-blogban, de ez a keresésem idején nem adott vissza közvetlenül
idézhető, a pre/post kérdésre válaszoló szöveget — nem forszíroztam tovább, mert a
funkcionális garancia a design szempontjából elegendő volt.)

## 8. AI-összefoglaló / fetch-hiba esetek
- Az `opensearch.org/docs/latest/security/access-control/document-level-security/` oldal
  lekérésekor a WebFetch csak navigációs vázat adott vissza, valódi tartalom nélkül — ezt
  NEM használtam fel forrásként, helyette a verzió-specifikus (`2.11`) URL-t kértem le, ami
  működött.
- A `docs.vespa.ai/en/operations-selfhosted/securing-your-vespa-installation.html` oldal
  első lekérése egy „redirect message"-et adott vissza tartalom nélkül; a második,
  közvetlenül a redirect-cél URL-re (`docs.vespa.ai/en/securing-your-vespa-installation.html`)
  irányuló lekérés már valódi tartalmat adott — ez utóbbit használtam forrásként.
- Az `astconsulting.in/database/implement-access-control-vespa` (T3, harmadik fél tutorial)
  önmagában nem tudta megválaszolni, hogy a Vespa ACL natív vagy alkalmazás-szintű — ezt
  kifejezetten jeleztem, és nem használtam fel állítás alátámasztására.

Egyik fetch sem adott vissza az instrukcióban leírt „## Issue Summary" mintájú, láthatóan
hallucinált AI-összefoglalót — de a fenti három esetnél a visszakapott tartalom
információhiányos volt, ezt a `megallapitasok.md`-ben és itt is jelöltem, nem töltöttem ki
kitalált adattal.


---

## SQ-02 — Index és lemez elcsúszásának észlelése és javítása

# SQ-02 — Amire nem találtam választ (gaps)

## 1. Nincs mért fordulópont a teljes hash-elés költségére

Kerestem konkrét, mért adatot arra, hogy hány fájlnál / hány GB-nál válik a teljes
tartalom-hash-elés (SHA-256, BLAKE3 stb.) "vállalhatatlanná" egy napi konzisztencia-
futásban. **Nem találtam** ilyen mérést semmilyen tier forrásban. Amit találtam:

- Az apenwarr-blog (T2) csak minőségi állítást tesz ("thousands, or tens of thousands of
  files... sucks a lot"), szám nélkül.
- A Recoll teljesítmény-oldal (T2) mért adatot ad, de **teljes tartalom-kinyerésre és
  indexelésre**, nem pusztán stat()+hash bejárásra — a két művelet költsége nem
  helyettesíthető egymással.

**Minősítés:** valószínűleg *absence of evidence*, nem *evidence of absence* — plauzibilis,
hogy létezik ilyen benchmark valahol (pl. deduplikációs rendszerek, borgbackup/restic saját
teljesítmény-tesztjei), de a rendelkezésre álló keresési ablakban nem került elő.

## 2. Nincs megbízható, konkrét hash-throughput szám (GB/s) modern CPU-n

Több keresést futtattam SHA-256/BLAKE3 GB/s-re. A találatok túlnyomó többsége marketing-
jellegű összehasonlító oldal (ssojet.com, mojoauth.com, devtoolspro.org, guptadeepak.com) —
ezeket **szándékosan nem használtam fel**, mert nincs bennük elsődleges mérés-forrás, csak
egymást idéző számok (klasszikus "content farm" minta a `search-playbook.md` 5. pontja
szerint). Az egyetlen arXiv-forrás (2407.08284v1) "hashes/sec" mértékegységet használ
tisztázatlan bemenet-mérettel, ezért csak erős fenntartással idézhető (ld.
`megallapitasok.md` 3.2). A BLAKE3 hivatalos GitHub repója hivatkozik saját benchmark-
diagramra, de az kép formátumú, a WebFetch szöveges kinyerése nem tudta reprodukálni a
számokat.

## 3. Meilisearch és Typesense — nincs dokumentált konzisztencia-ellenőrző minta

Mindkét terméknél kerestem hivatalos tervezési dokumentumot vagy funkciót, ami a forrás-
adat és az index közötti elcsúszást kezelné (crash közbeni indexelés, "resync" parancs).
Csak elszórt hibajegyeket találtam (Meilisearch #3313 — crash naplózás nélkül; #4438 —
csendes indexelési hiba), nem tervezési dokumentumot. **Nem zárható ki**, hogy létezik
ilyen funkció, amit a keresési ablakban nem találtam meg (pl. mélyebben a dokumentáció
struktúrájában, vagy csak a forráskódban).

## 4. Zoekt és tantivy — a staleness-detektálás pontos mechanizmusa

A Zoekt hivatalos tervezési dokumentuma (design.md) csak annyit mond, hogy "reindex any
changed repositories", de nem részletezi, *miből* dönti el, hogy egy repó megváltozott
(commit SHA összevetés a legvalószínűbb, de ezt nem sikerült elsődleges forrással
megerősíteni). A tantivy hivatalos doksija a reader-frissítést írja le (`ReloadPolicy`),
ami egy **másik réteg** problémája (író→olvasó láthatóság), nem a fájlrendszer↔index
elcsúszás — ez utóbbira a tantivy dokumentációjában nem találtam releváns szakaszt.

## 5. Nincs konkrét, megerősített incidens arra, hogy automatikus index-javítás élő adatot törölt volna tévesen

Kerestem kifejezetten dokumentált esetet, ahol egy "önjavító" keresőindex-mechanizmus
*tévesen* (hamis pozitív irányban) törölt vagy sérült meg élő, még létező tartalmat. A
talált FSCrawler-hibajegy (#531) az **ellenkező** irányú hibáról szól (nem törölt olyat,
amit kellett volna). Az rclone `--max-delete`/hibakezelési védőkorlátjának létezése erős
**közvetett** jelzés arra, hogy az iparág ismeri ezt a kockázatot, de ez nem helyettesít
egy konkrét, forrásolható incidens-leírást. Ezt a kutatási kört lezárva **nem találtam**
ilyen konkrét esetet — lehet, hogy létezik (pl. adott cégek postmortem-blogjaiban), de a
felhasznált keresési idő alatt nem került elő.

## 6. A Solr DataImportHandler jelenlegi státusza a Solr törzsében

A DIH hivatalos wiki-oldala (cwiki.apache.org) élő, funkcionális leírást ad, de **nem
ellenőriztem külön forrással**, hogy a DIH jelenleg is támogatott/elérhető komponens-e a
legújabb Solr-verziókban, vagy már törölték/kiszervezték. Ezt a bizonytalanságot a
`megallapitasok.md`-ben jeleztem, de nem zártam le.

## 7. `gc_grace_seconds` konkrét alapértelmezett értéke

A Cassandra repair-gyakoriság kontextusában szerettem volna megerősíteni a
`gc_grace_seconds` paraméter alapértelmezett értékét (a köztudatban elterjedt "10 nap"),
de a ténylegesen lefetchelt oldal szövegében ez a konkrét szám **nem szerepelt** — ezért
**nem** vettem fel számként a megállapítások közé, annak ellenére, hogy valószínűleg
igaz. Ez a szabály szigorú betartása: "ne találj ki számot", ha a lefetchelt idézet nem
tartalmazza.

## 8. AI-összefoglaló / üres tartalom problémája

Több WebFetch-hívás olyan válasszal tért vissza, hogy "a megadott tartalom nem tárgyalja
ezt a témát" (pl. FSCrawler `elasticsearch.rst`, Zoekt `design.md` a staleness-
detektálásra, Obsidian súgó a perzisztens indexre). Ezekben az esetekben **nem
találtam ki** tartalmat — a hiányt explicit negatív találatként rögzítettem a
`megallapitasok.md`-ben és itt. Egyetlen esetben sem tapasztaltam, hogy a WebFetch a
valódi oldal helyett egyértelműen félrevezető, kitalált AI-összefoglalót adott volna
vissza — de a fenti "nem talált releváns szakaszt" válaszok is korlátozzák a lefedettséget,
mert a kisebb, gyors modell által végzett kinyerés esetleg átugrott releváns, de nem
kulcsszó-egyező szövegrészeket.

## 9. Magyar nyelvű forrás nem került elő

A `search-playbook.md` 4. pontja szerint geográfiailag/intézményileg kötött témáknál
érdemes natív nyelvű keresést is futtatni. Ez a téma (fájlrendszer/keresőindex
konzisztencia) nem magyar-specifikus, ezért **nem futtattam** külön magyar nyelvű
keresési kört — ezt tudatos döntésként, nem mulasztásként rögzítem.


---

## SQ-03 — Ha a beágyazó nem elérhető lekérdezéskor

# SQ-03 — Hiányosságok (amire nem találtam választ)

## 1. Nincs egyetlen, univerzális szám a BM25-only vs hibrid romlásra
A mért adatok (Elastic Labs BEIR: 18–24%; From BM25 to Corrective RAG: ~6,5%; TREC DL 2021:
~31–40%) különböző benchmarkokból, különböző módszertannal, különböző mérőszámmal (nDCG@10
vs failure-rate) származnak. Nem találtam olyan egységes, kontrollált tanulmányt, amely
ugyanazon a korpuszon, ugyanazzal a módszertannal mérné a BM25-only vs hibrid romlást
**lekérdezés-típusonként** lebontva (pl. külön az „exact ID" és külön a „természetes nyelvi
kérdés" alkategóriára) — ahogy a kérdés kérte. Amit próbáltam: `hybrid search benchmark
measured recall drop when disabling one retriever leg ablation study`, több MTEB/BEIR
leaderboard-keresés — ezek vagy nem bontják lekérdezés-típusra az eredményt, vagy csak
task/dataset-szinten (pl. „ArguAna", „NFCorpus"), nem konkrét lekérdezés-mintázat szinten.

## 2. Anthropic Contextual Retrieval — a nyers (nem-kontextualizált) embeddings-only vs
## embeddings+BM25 táblázat nem volt kinyerhető
A blogbejegyzés explicit hivatkozik egy „Appendix I"/„Appendix II" PDF-re, amely „a
breakdown of results across datasets, embedding providers, use of BM25 in addition to
embeddings" — vagyis pontosan a keresett bontás létezik. Megtaláltam és lekértem a PDF-et
(https://www-cdn.anthropic.com/5722e7658c9302d8b97a3238de1bb8e6afdf04b9.pdf), de a
WebFetch-eszköz (kis segédmodell) nem tudta kinyerni a konkrét táblázat-sorokat/számokat a
PDF-ből — csak azt erősítette meg, hogy a táblázat témái léteznek a dokumentumban. Ez **nem**
a instrukcióban leírt „AI-összefoglaló a valódi tartalom helyett" hibamód (nem kaptam vissza
hallucinált, kitalált „## Issue Summary" jellegű szöveget) — a segédmodell explicit,
őszintén jelezte, hogy nem találja a kért konkrét adatokat a kinyert tartalomban. Ennek
ellenére forrásként nem használtam fel konkrét számot ebből a PDF-ből, mert nem tudtam
ellenőrizni egyetlen konkrét állítást sem szó szerinti idézettel.

## 3. OpenSearch, Weaviate, Qdrant, Milvus — nincs hivatalos (T1) állásfoglalás a lekérdezés-
## kori beágyazó-kiesésről
Mind a négy rendszernél megpróbáltam közvetlenül lekérni a releváns hivatalos
dokumentációs oldalakat:
- OpenSearch: `docs.opensearch.org/latest/ingest-pipelines/processors/text-embedding/`,
  `.../ingest-pipelines/pipeline-failures/` (redirekt után is csak navigációs váz jött
  vissza), `.../query-dsl/compound/hybrid/` — egyik sem tartalmazott explicit állítást a
  modell-elérhetetlenség esetére.
- Weaviate: a vectorizer/hibrid keresés hivatalos koncepcionális oldalait (`concepts/
  filtering`, `concepts/vector-index`) átnéztem korábbi (SQ-01) kutatásból is, de a
  „mi történik, ha a vectorizer API nem válaszol" kérdésre explicit hivatalos választ nem
  találtam — csak közösségi issue-kat (T3).
- Qdrant: a „Cloud Inference" hivatalos oldalai (`documentation/inference/cloud-inference/`,
  `.../inference-api/`) a funkció beállítását írják le, a hibaesetet nem.
- Milvus: az „Embedding Function Overview" hivatalos oldal (`milvus.io/docs/
  embedding-function-overview.md`) sem tér ki a szolgáltató-hiba esetére.

**Mit próbálnék még, ha folytatnám:** az egyes projektek GitHub-repóiban közvetlenül a
forráskódot (nem az issue-kat) keresném meg a hibakezelő ág(ak)ra — pl. Milvus
`embedding_function` Python-kliens forráskódjában a try/except blokkokat, vagy az OpenSearch
`neural-search` plugin Java forráskódjában a modell-hívás hibakezelését. Ez explicit T1
forrás (forráskód) lenne, de ehhez mélyebb, kódszintű keresés kellett volna, ami túlment
volna a rendelkezésre álló kereten.

## 4. Nincs nevesített, elterjedt „X-Degraded" HTTP-fejléc konvenció
Kifejezetten kerestem rá (`"X-Degraded" header OR "degraded response" API design partial
response indicate client`), és nem találtam ilyen elterjedt konvenciót — sem hivatalos
specifikációként, sem de facto iparági gyakorlatként. A legközelebbi formális minta (HTTP
Warning fejléc, RFC 7234/9111) elavult (ld. `contradictions.md` 3. pont). Ez azt jelenti,
hogy ha a projekt bevezetne egy saját degradációs jelzőt, az **nem egy már létező,
felismerhető konvenciót követne**, hanem saját tervezésű mezőt kellene definiálni — ezt
explicit ki kell mondani, nem szabad úgy tenni, mintha lenne rá bevett minta.

## 5. Elasticsearch ingest-pipeline hiba — dokumentum-szintű vs bulk-kérés-szintű elutasítás
A hivatalos dokumentáció kimondja, hogy alapértelmezetten „pipeline processing stops when
one of these processors fails" — de nem találtam olyan mondatot, ami 100%-osan explicit
módon tisztázná, hogy egy bulk-indexelési kérésen belül **csak az érintett dokumentum**
bukik-e el (és a többi a batch-ben sikeresen indexelődik), vagy a **teljes bulk-kérés**
elutasításra kerül. A gyakorlati Elasticsearch-ismeret (bulk API item-szintű
sikeresség/hiba-jelentése) erősen az előbbi felé mutat, de ezt nem tudtam szó szerinti
idézettel alátámasztani a lekért oldalakról, ezért nem állítottam ezt tényként a
`megallapitasok.md`-ben.

## 6. Vespa — a `coverage.degraded` mechanizmus kiterjed-e a beágyazó-kiesésre?
A hivatalos Vespa dokumentáció (`graceful-degradation.html`) csak időtúllépésre/lefedettségre
(`timeout`, `adaptive-timeout`, `match-phase`, `anntimeout`) sorol fel konkrét okokat a
`degraded` objektumban. A `embedding.html` oldal nem tárgyalja az embedder-hiba esetét
egyáltalán. Nem tudtam megállapítani, hogy egy lassú/elakadt embedder a `anntimeout` alá
esne-e (mivel az ANN-keresés maga is az embedder kimenetétől függ), vagy egy teljesen kemény
hibát váltana ki. Ez nyitva maradt kérdés.

## 7. AI-összefoglaló / fetch-hiba esetek — explicit jelzés
Egyik lekérés sem adott vissza az instrukcióban leírt „## Issue Summary" mintájú, láthatóan
hallucinált AI-összefoglalót a valódi oldaltartalom helyett. Több esetben azonban a
WebFetch kis segédmodellje explicit jelezte, hogy a kapott tartalom navigációs vázra vagy
töredékes/redirekt-üzenetre korlátozódott, és nem tud konkrét állítást idézni belőle. Ezeket
NEM használtam fel forrásként konkrét állítás alátámasztására, csak a hiányosság tényét
rögzítettem:
- `docs.opensearch.org/latest/ingest-pipelines/pipeline-failures/` — redirekt után is csak
  navigációs váz.
- `milvus.io/docs/embedding-function-overview.md` — a modell szerint a tartalom nem
  tárgyalja a hibaesetet.
- `docs.vespa.ai/en/embedding.html` — hasonlóan, a hibaeset nincs a lekért tartalomban.
- `opensearch.org/blog/cold-start-search/` — a tartalom más témáról (shard-refresh
  késleltetés) szól, nem a beágyazó-szolgáltatás elérhetőségéről.
- `docs.opensearch.org/latest/query-dsl/compound/hybrid/` — a lekért tartalom nem
  tartalmazott hibakezelési részt.

## 8. TREC/MTEB — nem találtam friss (2026-os), explicit BM25-only vs hibrid összehasonlítást
egy hivatalos TREC-jelentésben
A TREC 2021 Deep Learning Track jelentése BM25 vs neurális összehasonlítást ad, de nem
„hibrid" (fúziós) futtatást állít szembe BM25-tel egy dedikált sorban. A TREC 2023-as
jelentést (`trec.nist.gov/pubs/trec32/papers/Overview_deep.pdf`) megtaláltam a keresésben,
de nem kértem le részletesen — ha a kutatás folytatódna, érdemes lenne ezt is átnézni
hasonló bontásért. Az MTEB retrieval leaderboard-ot csak másodkézből (blogokon keresztül)
találtam, magát a hivatalos MTEB leaderboardot (huggingface.co/spaces/mteb/leaderboard) nem
kértem le közvetlenül BM25-baseline-sorért — ez egy nyitva hagyott irány.


---

## SQ-04 — Törlésre jelölt bejegyzés az indexben

# SQ-04 — Amire nem találtam választ (gaps)

## 1. Explicit FTS5-specifikus figyelmeztetés a bm25() torzításról törölt sorok esetén

A hivatalos `sqlite.org/fts5.html` dokumentálja a `bm25()` képlet N/avgdl/n(qi)
függőségét, és külön dokumentálja a `delete`/`delete-all`/`rebuild` parancsokat — de
**sehol nem mondja ki explicit módon**, hogy „ha egy sort törölsz-jelölés után bent
hagysz és csak WHERE-rel szűrsz ki, a bm25() pontszám torzulni fog". Ez a `megallapitasok.md`
5. pontjában szereplő állítás **saját logikai levezetés** a képlet szerkezetéből, nem
idézett FTS5-állítás. Ha a projektnek szüksége van hivatalos SQLite-forrásra pont erre az
állításra, ilyen nem létezik — csak az Elastic/Lucene analóg, explicit kijelentése (más
motorra vonatkozóan).

## 2. Dedikált „undelete" / visszaállítás API

Egyik vizsgált rendszer (Qdrant, Weaviate, Milvus, Meilisearch, Typesense,
Elasticsearch/Lucene) hivatalos dokumentációjában sem találtam kifejezett „undelete" vagy
„restore deleted point/document" API-t vagy funkciót. A Qdrant GitHub issue-k (#6556,
#2550) közvetve megerősítik, hogy a törölt pontok vektor-adatának kezelése implementációs
részletkérdés, nem dokumentált, garantált API-felület. **Ez azt jelenti, hogy a
visszaállíthatóság ára minden vizsgált rendszerben implicit, nem hivatalosan garantált
viselkedésen múlik** — a `megallapitasok.md` 6. pontjában közölt következtetés emiatt
tervezési szintézis, nem forrás-alapú tény.

## 3. Típus-specifikus mért benchmark a soft-delete-and-filter mintára FTS5-ben

Van általános Lucene-mérés (18–46% lassulás 50% töröltaránynál — Elastic saját blogja),
és van HNSW-specifikus mérés (Ghost Vectors: 4,3% latencia-eltérés, 95% top-K
divergencia). **Nincs SQLite FTS5-specifikus, publikált mérés** arra, hogy egy
`WHERE fts MATCH ? AND status != 'törölt'` jellegű post-filter lekérdezés mennyivel
lassabb, vagy hogyan torzítja a rangsort egy előre kitakarított (fizikailag eltávolított)
indexhez képest. Ez azt jelenti, hogy a projekt saját döntéséhez **nincs kész,
átvehető szám** — csak analóg rendszerek mért adatai.

## 4. Typesense belső törlés-mechanizmusa

A hivatalos Typesense Documents API dokumentáció (https://typesense.org/docs/30.2/api/documents.html)
kizárólag a végpontokat írja le (egyedi törlés, `filter_by`-alapú tömeges törlés,
truncate), de **nem tárgyalja**, hogy a belső (memóriabeli) adatstruktúra jelölést vagy
azonnali fizikai eltávolítást alkalmaz-e. Nem találtam más hivatalos Typesense-forrást
sem, ami ezt tisztázná — ehhez a forráskód vizsgálata kellene, ami nem célja ennek a
kutatásnak.

## 5. OpenSearch `_delete_by_query` és a Lucene-merge kapcsolata hivatalos dokumentációban

A hivatalos OpenSearch „Delete by Query API" oldal (https://docs.opensearch.org/latest/api-reference/document-apis/delete-by-query/)
csak funkcionális szinten írja le a műveletet, nem tárgyalja explicit a mögöttes
Lucene-szegmens-jelölést vagy merge-folyamatot. Feltételezhető (az OpenSearch a
Lucene-re épül, mint az Elasticsearch), hogy ugyanaz a bitset-mechanizmus érvényes, de ezt
**nem hivatalos OpenSearch-forrásból**, hanem az Elasticsearch/Lucene közös eredetéből
vezetem le — ezt a `megallapitasok.md`-ben nem állítottam külön OpenSearch-tényként.

## 6. Elasticsearch hivatalos API-dokumentáció a `_delete_by_query`-ról nem tárgyalja a segment-merge-et

A hivatalos `operation-delete-by-query` API-referencia (https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-delete-by-query)
a verziókonfliktus-kezelést és a `refresh` paramétert írja le, de nem szól arról, hogy a
törlés triggerel-e (vagy sem) azonnali szegmens-merge-t. Ezt a „History retention
settings" és a Lucene-blog általánosabb, nem `_delete_by_query`-specifikus állításaiból
vezettem le.

## 7. Az OpenReview PDF nem volt elérhető

Az `https://openreview.net/pdf?id=lnaC19Pd30` URL **403-as hibát** adott vissza
(fetch-hiba, nem AI-összefoglaló-probléma — a hívás egyértelmű kliens-oldali hibát
jelzett). Az azonos tartalmú arXiv-változatot (https://arxiv.org/html/2512.06200)
sikerült lekérni és idézni, így tartalmi adatvesztés nem történt, de magát az
OpenReview-oldalt nem tudtam közvetlenül ellenőrizni/idézni.

## 8. Általános „soft delete anti-pattern keresőindexben" célzott szakirodalom

A kifejezetten erre a mintára (nem ACL-re, hanem törlési állapotra) fókuszáló, célzott
keresés („soft delete search index anti-pattern relevance BM25 stale document frequency")
kizárólag általános BM25-ismertető cikkeket hozott (GeeksforGeeks, Spice AI, DataAspirant),
amik nem T1/T2 minőségűek és nem foglalkoznak kifejezetten a törlés okozta torzítással.
Emiatt a 4. pont (`megallapitasok.md`) állításait a Lucene/Meilisearch/Qdrant-specifikus,
rendszerenkénti forrásokból építettem fel, nem egy általános „best practice" cikkből.

## 9. Nem volt AI-összefoglaló-probléma ebben a kutatásban

A feladat kérte, hogy jelezzem, ha egy fetch AI-összefoglalót ad vissza a valódi oldal
helyett. Ebben a kutatásban **nem találkoztam** ezzel a jelenséggel — minden WebFetch
válasz tartalmi kivonatot adott a ténylegesen lekért oldalról (bár néhány esetben — pl.
Weaviate delete.mdx, Milvus delete-entities.md, Typesense documents.html — a lekért oldal
maga nem tartalmazta a keresett belső mechanizmust, ami különbözik az AI-összefoglaló
problémától: itt a forrás oldal ténylegesen nem tárgyalta a kérdést, nem a fetch-eszköz
hibázott).
