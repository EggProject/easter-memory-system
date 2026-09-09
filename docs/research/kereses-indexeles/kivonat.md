# Kivonat — keresés és indexelés: négy nyitott kérdés

Forrás: `00-plan.md`, valamint `sq01`–`sq04` mappák (`megallapitasok.md`, `links.md`,
`gaps.md`, `contradictions.md`, `searches.md`). Ez a dokumentum a kutatók megállapításainak
összefoglalása — nem tartalmaz új kutatást, és nem tartalmaz tervezési következtetést vagy
ajánlást (azt a szintézis írja külön).

---

## 1. Mire kerestünk választ

A `30-kereses.html` dokumentum egy olyan rendszert ír le, amelyben a markdown fájlok az
igazságforrás, és belőlük épül fel — indexelési lépésként — egy eldobható SQLite adatbázis.
Ez az adatbázis két, párhuzamosan futó keresési mechanizmust szolgál ki: egy FTS5 alapú,
BM25-pontszámmal rangsorolt szöveges (lexikai) indexet, és egy beágyazás-alapú (embedding),
jelentés szerinti keresést, amely egy külön folyamatban (más konténerben) futó beágyazó
szolgáltatáson keresztül számol vektorokat. A két láb találatait helyezés-alapú egyesítéssel
(Reciprocal Rank Fusion, RRF) kombinálja a rendszer — ennek a képlete és a csillapító
paramétere korábbi kutatási körben (`router-rangsor`) már lezárt kérdés, ebben a körben nem
vizsgáltuk újra. Ugyanígy lezártnak számít az FTS5+Drizzle technikai megvalósítás (virtuális
tábla, öt árnyéktábla, `bm25()` szerinti rendezés, automerge/crisismerge), a Bun/SQLite/
beágyazás teljesítmény-jellemzői, és a kategória-prompt költségvetés.

A rendszer jogosultsági modellje projekt-szintű: egy felhasználó egy adott projekthez vagy
hozzáfér, vagy nem. A tervezett viselkedési elv (D-13) szigorú: amihez valakinek nincs joga,
az a számára ne csak láthatatlan legyen, hanem *ne is létezzen* — se találat nem jelenhet
meg róla, se a találatok száma nem árulkodhat a jelenlétéről, se semmilyen közvetett jelzés
(időzítés, rangsor-pozíció, javaslat) nem utalhat rá. Egy másik korábbi döntés (D-21) szerint
egy törlésre jelölt bejegyzés azonnal eltűnik a keresésből mindenki számára, de a fájl maga
megmarad, és aki jogosult rá, a böngésző felületen továbbra is látja (halványítva, „jelölt”
címkével) — vagyis a keresési indexből való eltűnés és a tényleges, végleges törlés két
különböző esemény.

Ez a kutatási kör négy, korábban nyitva hagyott al-kérdésre keresett választ: (1) hol
kell érvényesíteni a jogosultsági szűrést egy két lábon álló, RRF-fel egyesített hibrid
keresésben ahhoz, hogy a „nem létezik” garancia tartható legyen; (2) miből derül ki, hogy
az eldobható SQLite index már nem egyezik a markdown-lemezzel, és mit szabad ebből
automatikusan javítani; (3) mi történjen, ha a lekérdezés pillanatában a külön konténerben
futó beágyazó szolgáltatás nem elérhető; és (4) egy törlésre jelölt bejegyzést ki kell-e
azonnal venni a keresési indexből, vagy elég lekérdezéskor kiszűrni. Mind a négy kérdésnél
a kutatók élesen elválasztották a **mért adatot** a **tervezési ajánlástól/véleménytől** —
utóbbi sosem mérés, hanem egy gyártó, mérnök vagy szerző álláspontja.

---

## 2. SQ-01 — Hol szűrjön a jogosultság a hibrid keresésben

### Fogalmak és alapproblémák

Az **előszűrés** (pre-filtering) a szűrőfeltételt a keresés előtt vagy közben alkalmazza,
mielőtt a rangsorolt találati halmaz kialakulna — a Compass akadémiai dolgozat (arXiv
2510.27141) megfogalmazásában „it applies all relational predicates to the dataset first
and then performs vector search on the resulting filtered subset”. Az **utószűrés**
(post-filtering) előbb lefuttatja a keresést a teljes, szűretlen indexen, és a szűrőt csak
utólag, az eredménylistára alkalmazza: „a set of k′ candidate records is retrieved using
vector search as the first step, and then this set is filtered according to the attribute
predicate” (ugyanaz a forrás). Mindkét megközelítésnek dokumentált, saját törése van. Az
előszűrés ára naiv esetben a teljes (brute-force) átvizsgálásig nőhet: „The cost grows
fast: the mask touches every point, every match becomes a scoring candidate, and a broad
filter degrades into brute force” (Qdrant, T2, qdrant.tech/blog/pre-filtering-vs-post-filtering).
Az utószűrés ára az, hogy szelektív szűrőnél a kért `k` darab találatból csak töredék
marad életben, és „more selective predicates can actually increase query latency, contrary
to the typical database expectation” (Compass paper).

### A top-k alákerülés — van mért adat

Az Elasticsearch hivatalos dokumentációja explicit kimondja a különbséget a kNN pre-filter
és a hagyományos post-filter szűrők között: a kNN `filter` „is applied **during** the
approximate kNN search to ensure that `num_candidates` matching documents are returned”,
míg más szűrők „results in fewer than k results, even when there are enough matching
documents” (elastic.co, T1). Konkrét, mért szám az AWS saját (T2) méréséből, pgvector
0.8.0-n, Aurora PostgreSQL-en, iteratív szkennelés be- és kikapcsolásával összevetve:
„Category-filtered search: improved from 10% recall to 100% recall” és „Complex filtered
search: improved from 1% recall to 100% recall”. Vagyis naiv, nem-iteratív utószűrésnél a
mért recall ugyanazon szűrt lekérdezéseknél 1–10% volt — konkrét, dokumentált eset, nem
becslés, bár erősen lekérdezés/adatbázis-függő szám. A pgvector hivatalos közleménye
szerint az iteratív mód addig folytatja a keresést, „until it hits a configurable
threshold (`hnsw.max_scan_tuples`...)” — vagyis a garancia még ekkor is csak feltételes,
nem abszolút.

### Az előszűrés ára a HNSW/IVF gráfbejárásnál

Itt a legdrámaibb, egymást megerősítő mérés a Qdrant saját ACORN-cikkéből (T2) származik.
1%-os szelektivitású szűrőnél: „Plain graph: 0.1% @ 1.6ms” recall/latencia egy módosítatlan
HNSW-gráfon, ACORN-nal „67.7% @ 4.7ms”, index-idejű extra élekkel épített („filterable”)
HNSW-vel pedig „99.8% @ 1.0ms” (qdrant.tech/articles/filtered-vector-search-acorn). Az ok
a cikk saját magyarázata szerint: „Filter out 96% of the points and fewer than one link per
node survives on average, so traversal can get stranded before it reaches the true nearest
matches.” Ezzel látszólag szemben áll egy Weaviate-mérnök (Etienne Dilocker) saját mérése
(T2, 250k objektum, 256 dimenzió, Weaviate v1.8.0, 100 különböző szűrő 0–99%-os
szelektivitási tartományban): „as filters get more restrictive (less than 20% of the
dataset contained) the recall is perfect (100%)” és „Regardless of filter, searches
typically don't take longer than 30ms” (towardsdatascience.com). A kutatók szerint ez nem
valódi ellentmondás, hanem ugyanannak a jelenségnek két oldala (részletesen a 6. pontban).

### SQLite FTS5 konkrétan — JOIN egy jogosultsági táblával

A hivatalos `sqlite.org/fts5.html` dokumentáció **nem tárgyalja a JOIN-t** — a kutató szó
szerinti kereséssel ellenőrizte, hogy a „JOIN” szó egyszer sem fordul elő az oldalon. A
gyakorlati viselkedést csak a hivatalos SQLite fórumon (T3, de a projekt fő fejlesztőitől,
Dan Kennedy-től és Richard Hipp-től) sikerült megtalálni, három konkrét problémával: (1)
„FTS5 uses static cost estimates”, ezért JOIN-nál a tervező rosszul dönthet a bejárási
sorrendről; (2) egy konkrét, mért esetben „running ANALYZE reduced query execution from
170 seconds to 0.259 seconds” — kb. 656-szoros gyorsulás; (3) a `MATCH` operátor nem
működik aliasszal JOIN-olt FTS5 táblánál, a fórum ajánlása szerint „Don't join with the
fts tables, rather, join with their search result set.” A gyakorlati következtetés (nem
hivatalos SQLite-ajánlás, mert a hivatalos doksi nem tér ki erre): a jogosultsági szűrést
vagy egy előre kiszámolt rowid allow-listtel kell a MATCH-lekérdezésbe injektálni, vagy a
MATCH eredményét kell alkérdésként JOIN-olni a jogosultsági táblával — és mindkét esetben
kötelező az `ANALYZE`/`PRAGMA optimize` lefuttatása.

### Szivárgás darabszámon és időzítésen keresztül

Ez a legjobban dokumentált pont, hivatalos gyártói figyelmeztetéssel. Az Elasticsearch DLS
dokumentációja kimondja: „it's still possible to write search requests that return
aggregate information about the entire index. A user whose access is restricted to
specific documents in an index could still learn about field names and terms that only
exist in inaccessible documents, and count how many inaccessible documents contain a given
term.” Ugyanez a dokumentum egy rangsorolási csatornát is megnevez: „Document level
security doesn't affect global index statistics that relevancy scoring uses. This means
that scores are computed without taking the role query into account.” — vagyis egy
jogosultság nélküli dokumentum jelenléte torzíthatja mások pontszámát, ami közvetett jelzés
a létezésére. Az időzítés-alapú szivárgásra egy Microsoft Research + Indiana University
technikai jelentés (T1) általános webalkalmazás-kontextusban mutatja ki, hogy „packet
sizes and timings, can still give away the information about the user's selection” HTTPS
alatt is. A PostgreSQL RLS közösség saját fejlesztői vitájában (T3, de a projekt hackerei)
kimondja, hogy „a lot of the PostgreSQL functions are not marked as leakproof”, és emiatt
a legnagyobb kockázatnak kifejezetten az IDOR-t (jogosulatlan hozzáférés objektum-
azonosítón keresztül) tekintik. A lapozás és a „did you mean”/autocomplete csatornákra
kereső-index-ACL-specifikus dokumentált esetet a kutató **nem talált** — ez explicit gap.

### Mit csinálnak a valós rendszerek

Mind a nyolc vizsgált rendszer (Elasticsearch, OpenSearch, Vespa, Qdrant, Weaviate, Milvus,
Typesense, Meilisearch) a szűrést **a lekérdezésbe ágyazva**, előszűrésként valósítja meg —
egyik sem futtat külön, a rangsorolás utáni ACL-motort. Az Elasticsearch kNN `filter`-je
explicit pre-filter; a Qdrant payload-szűrése a gráfbejárásba van építve; a Weaviate
multi-tenancy-je fizikai shard-per-tenant izolációt is ad („Each tenant is stored on a
separate shard. Data stored in one tenant is not visible to another tenant.”); a
Typesense scoped API key-je és a Meilisearch tenant tokenje kriptográfiailag beégetett,
felülírhatatlan szűrő. Az egyetlen kivétel a Vespa: hivatalos biztonsági dokumentációja
kizárólag hálózati/cluster-szintű védelmet ír le, dokumentum-szintű ACL-ről nem szól — ott
a fejlesztőnek kell a szűrést a lekérdezésbe (YQL `where`) építenie. Fontos árnyalat: az
„előszűrés” ezeknél a rendszereknél nem a naiv „vedd a HNSW-gráfot és hagyd figyelmen
kívül a nem-egyező pontokat” — mindegyik vektoros rendszer külön mérnöki munkát fektetett
a szűrt-gráfbejárás problémájának megoldásába (ACORN, extra élek, allow-list, adaptive mód).

Az explicit „a fúzió elé vagy mögé tegyük a szűrést” RRF-specifikus ajánlást a kutatók
**nem találták meg** egyetlen forrásban sem — ez a kutatási kör egyik legvilágosabban
rögzített hiánya (ld. 7. pont).

---

## 3. SQ-02 — Index és lemez elcsúszásának észlelése és javítása

### Az mtime gyengeségei

Az mtime a tartalom utolsó módosítási ideje, nem a fájl azonosítója — és több, egymástól
független módon hazudhat. A `redo` build-eszköz szerzőjének technikai blogja (T2) sorolja
fel a konkrét eseteket: másodperc-granularitás („almost no filesystems provide that level
of precision”), a `touch` paranccsal tetszőlegesen beállítható időbélyeg, óraátállítás,
hálózati fájlrendszerek óra-eltolódása, valamint konténer-mountok/virtuális fájlrendszerek,
amelyek gyakran egyáltalán nem állítják be az mtime-ot. A restic saját hibajegyén (T3)
dokumentált konkrét eset: egy csomagkezelő lecseréli a fájl tartalmát, de visszaállítja az
eredeti időbélyeget, „with mtime it can skip backing up a file.” A Git hivatalos
dokumentációja írja le a „racy git” jelenséget: ha egy fájl kétszer módosul ugyanabban a
másodpercben, „the cached stat information the index entry records still exactly match
what you would see in the filesystem, even though the file foo is now different” —
vagyis a Git tévesen tisztának hiheti a fájlt. A Git védekezése: ha a cache-elt mtime
egyenlő vagy újabb, mint az index-fájl saját időbélyege, tartalom-összehasonlítást is
végez, nem bízik pusztán az mtime-ban. A BorgBackup dokumentációja élesen szembeállítja a
ctime-ot („cannot be set from user space”) az mtime-mal („can be arbitrarily set from user
space”), és megjegyzi, hogy az inode-szám „often unstable on network file systems”. Az NFS
man page hivatalosan leírja az attribútum-gyorsítótár mechanizmusát: „Every few seconds,
an NFS client checks the server's version of each file's attributes for updates. Changes
that occur on the server in those small intervals remain undetected until the client
checks the server again.”

### A kétlépcsős minta mint iparági alapminta

Két, egymástól független hivatalos forrás dokumentálja ugyanazt a mintát. Az rsync
alapból méret+mtime „quick check”-et használ, és csak explicit `--checksum` kapcsolóval
tér át tartalom-hash-re. A Git a hash-alapú összevetést csak a „racily clean” (gyanús,
azonos időbélyegű) bejegyzésekre futtatja, nem az egész fára. A kutatók tervezési
következtetése (nem mérés, hanem két forrás tervezői döntéséből levont minta): a bevett
gyakorlat nem „hash mindent mindig”, hanem olcsó metaadat-összevetés a teljes fán, és
drága tartalom-hash csak a gyanús/határeseti fájlokra.

### Elnevezés és gyakoriság

A napi/heti konzisztencia-ellenőrző futásra több, egymástól független eredetű elnevezés
létezik: **reconciliation** (Kubernetes control loop: „The controller continuously works
to make the current state match the desired state... This is also known as the
reconciliation pattern”), **anti-entropy/repair** (Cassandra: „a process of comparing the
data of all replicas and updating each replica to the newest version”), **scrub**
(ZFS/OpenZFS: „A standard scrub verifies each block's checksum by examining all data”), és
termékspecifikus nevek: **index auto-healing** (Atlassian) és **index synchronization/
InSync flag** (IBM Sterling OMS). A klasszikus „fsck” elnevezést a kutató **nem** találta
keresőindex-kontextusban használva. Gyakoriság tekintetében minden talált konkrét rendszer
napi-heti tartományban futtatja a teljes ellenőrzést: az Atlassian index auto-healing
„daily at 1 a.m. local instance time”, a Cassandra hivatalos ajánlása „Run incremental
repair daily, run full repairs weekly to month”, a ZFS scrub-hoz pedig kész heti és havi
systemd-timer egységek vannak (mind tervezési ajánlás, nem mért optimalizációs eredmény).

### Mit szabad automatikusan javítani, és mit csak jelenteni

Az Atlassian Jira/Confluence „index auto-healing” funkciója pontosan a kérdésben felvetett
mintát valósítja meg: három kategóriát különböztet meg — „Index orphans: Issues existing
only in the index, not in the database. Database orphans: Issues existing only in the
database, not in the index. Outdated issues: Mismatches between indexed data and database
data.” Automatikusan javítja a talált eltéréseket, de van egy explicit korlát: ha az index
állapota „Unhealthy”, a dokumentáció kézi beavatkozást kér: „we recommend performing a
manual re-index.” Az IBM Sterling OMS hasonlóan explicit kézi vészkijáratot biztosít
(„manually mark enterprises not-synchronized... for exceptional circumstances like index
corruption requiring full rebuilds”). Az rclone `sync` parancsa explicit védőkorlátot
épít be a katasztrofális automatikus törlés ellen: „Files in the destination won't be
deleted if there were any errors at any point”, plusz egy `--max-delete` limit. A
Cassandra dokumentációja arra is figyelmeztet, hogy ha a konzisztencia-javító feladat
**elmarad**, az rosszabb, mintha sosem futna: törölt adat „feltámadhat” (`gc_grace_seconds`
küszöb átlépésekor). Egy konkrét, megerősített esetet arra, hogy egy önjavító mechanizmus
*tévesen* törölt volna élő adatot, a kutató **nem talált** — az FSCrawler egy dokumentált
hibajegye (#531) az ellenkező irányba mutat (nem törölt olyat, amit kellett volna).

### SQLite FTS5 konkrétan

Az `integrity-check` parancs a hivatalos dokumentáció szerint „is used to verify that the
full-text index is internally consistent, and, optionally, that it is consistent with any
external content table” — de külső content-táblás FTS5-nél (ami a projekt architektúrája)
ez csak akkor ellenőrzi a content táblával való egyezést is, ha „the value specified for
the rank column is 1”. A `rebuild` parancs a teljes indexet törli és újraépíti: „This
command first deletes the entire full-text index, then rebuilds it based on the contents
of the table or content table.” **Nincs** részleges FTS5-szintű javítási mechanizmus —
a hivatalos dokumentáció szerint az egyetlen javasolt út elcsúszás esetén a `rebuild`,
nem valamiféle célzott javítás; egyetlen fájl esetében a javítás az alkalmazási rétegre
hárul (törölj-és-szúrj-be-újra ezt az egy `file_id`-t a content táblában, a triggerek
intézik a shadow-táblákat). Az általános SQLite `PRAGMA quick_check` „does not verify...
that index content matches table content” és O(N) időben fut, míg a `PRAGMA
integrity_check` O(N log N) időben — ez az egyetlen algoritmikus komplexitás-adat, amit a
kutatók találtak, bár ez nem FTS5-specifikus.

### A teljes átvizsgálás ára

A Recoll szerzőjének saját mérése (T2, 2016-os közepes hardveren) konkrét indexelési
sebességet ad: „The indexer can process 1000 typical PDF files per minute, or 500
Wikipedia HTML pages per second on medium-range hardware.” Egy konkrét teszt 18000 PDF-en
(30 GB) helyi SSD-n 11m40s, ugyanazon adaton NFS-en 24m40s alatt futott le — mért,
kb. kétszeres szorzó a tárolási réteg (helyi vs hálózati) hatására. **Fontos korlátozás**:
ez teljes tartalom-kinyerést és indexelést mér, nem pusztán egy stat()+hash bejárást,
tehát felső becslés, nem közvetlenül alkalmazható a „csak nézzük meg, változott-e”
művelet költségére. A hash-elési sebességre talált egyetlen arXiv-szám bizonytalan
bemenet-méret miatt csak erős fenntartással idézhető, és **nincs** T1/T2 forrás konkrét
GB/s-re modern CPU-n. Mikor válik a teljes hash-elés vállalhatatlanná — erre **nincs**
mért fordulópont, csak minőségi állítás („Checksumming every input file before building is
very slow... for large projects, this sucks a lot”, apenwarr).

---

## 4. SQ-03 — Ha a beágyazó nem elérhető lekérdezéskor

### A négy elnevezett minta

A kutatás négy, forrásokkal alátámasztott, egymást kiegészítő (nem versengő) mintát
azonosított. **Fail-fast**: az AWS Well-Architected keretrendszer downstream-hiba esetén
kifejezetten circuit breaker-t ajánl: „If requests to a downstream system are consistently
failing, it does not make sense to continue retrying.” A Google SRE könyv ugyanezt a
válaszidő/erőforrás oldaláról indokolja: „it is usually better to have small queue lengths
relative to the thread pool size... which results in the server rejecting requests early.”
**Graceful degradation**: az AWS Well-Architected definíciója szerint „Application
components should continue to perform their core function even if dependencies become
unavailable. They might be serving slightly stale data, alternate data, or even no data.”
A Google SRE könyv maga is figyelmeztet, hogy ez nem ingyenes: „Complex load shedding and
graceful degradation can cause problems themselves.” **Stale/cached válasz**: az IETF RFC
5861 `stale-if-error` kiterjesztése kifejezetten backend-kiesésre való, és eredetileg
kötelezővé tette a jelölést (Warning fejléc) — ezt a mechanizmust azóta az RFC 9111
elavulttá nyilvánította, dedikált utód nélkül. **Sorbaállítás/várakozás**: az Azure
Architecture Center „Queue-Based Load Leveling” mintája explicit kimondja, mikor NEM
alkalmazható: „The caller requires a low-latency, synchronous response” — vagyis ez a
minta elsősorban az írási (indexelési), nem a lekérdezési oldalra való.

### Mért adat: mennyivel romlik a minőség csak BM25-tel

Több, egymástól független forrás mér, de **egymástól jelentősen eltérő nagyságrendekkel**,
a benchmark tartományától függően. Az Elastic saját BEIR-alapú mérése (T2) szerint az
RRF-fúzió „achieved... 18% over BM25 alone” nDCG@10-ben, egy jobban hangolt súlyozott
kombináció pedig „24% improvement over BM25 alone”. A „From BM25 to Corrective RAG” arXiv
dolgozat pénzügyi dokumentumokon: nDCG@10 — BM25 0,515, Dense 0,466, Hybrid 0,551 (itt a
BM25 önmagában *jobb* is, mint a dense-only). A TREC 2021 Deep Learning Track hivatalos
NIST-jelentése egy más módszertani összevetésben (legjobb tisztán neurális vs legjobb
tisztán BM25 rendszer, nem hibrid-vs-BM25) sokkal nagyobb rést mutat: „the best BM25
baseline achieved an NDCG@10 of 0.5116” dokumentum-rangsorolásnál a legjobb neurális
0,7437-hez képest, passage-rangsorolásnál 0,4458 vs 0,7494. Az Anthropic Contextual
Retrieval (T2, saját technikáról) szerint a BM25 hozzáadása egy már kontextualizált
beágyazáshoz a kudarc-arányt 5,7%-ról 3,7%-ra (csak kontextuális embedding), majd 2,9%-ra
(kontextuális embedding + BM25) viszi le. A kutatók összegzése: a talált mérések 6,5%-tól
kb. 40%-ig terjedő romlást mutatnak, ha a szemantikus láb kiesik — a konkrét szám erősen
feladat- és mérőszám-függő, nincs egyetlen univerzálisan idézhető szám.

### Mért adat fordítva: mennyivel romlik, ha csak a szemantikus láb megy

A BEIR paper (T1, NeurIPS 2021) a domain-shift jelenséget nevezi meg okként: „Dense
retrievers are observed to underperform on datasets with a large domain shift compared
from what they have been trained on.” Konkrét számok: ArguAna nDCG@10 — BM25 0,315 vs
DPR 0,175; Climate-FEVER — BM25 0,213 vs DPR 0,148; NFCorpus — BM25 0,325 vs DPR 0,189. Egy
független mérnöki blog (T2, tianpan.co) nevesíti a konkrét lekérdezés-mintázatokat, ahol a
szemantikus láb egyedül elbukik: „Error codes and identifiers”, „Product SKUs and model
numbers”, „Function names and library identifiers”, „Domain jargon with controlled
vocabulary” — pontosan azok a kategóriák, amelyeket a kutatási kérdés is megnevezett
(pontos azonosító, hibakód, ritka szó). Ezzel szemben egy StackOverflow Q&A tanulmány
(T2, Zenodo self-deposit) fordított eredményt mutat: „Dense retrieval achieves Recall@5 =
0.779 and MRR = 0.670” a „sparse baseline (Recall@5 = 0.394, MRR = 0.292)”-hez képest —
itt azonban a „sparse baseline” TF-IDF, nem teljes BM25 (ld. 6. pont).

### A degradált válasz jelölése

Van élő, hivatalos gyártói precedens, de nincs egységes iparági szabvány. A Vespa hivatalos
dokumentációja szerint a válasz JSON-ban explicit jelzés van: „a coverage element below the
root element, which has a degraded element if the query execution was degraded in some
way” — konkrét okokat is megnevez (`timeout`, `adaptive-timeout`, `match-phase`,
`anntimeout`), de a beágyazó-komponens explicit hibájára a dokumentáció **nem tér ki**. Az
Elasticsearch `_search` API-ja shard-szintű időtúllépésre/hibára ad hasonló jelzőket
(`timed_out`, `_shards.failed/skipped`) — de amikor kifejezetten a beágyazó (inference
endpoint) hiányzik, a `semantic_text` mezőt használó lekérdezés a hivatalos dokumentáció
szerint **egyáltalán nem jut el eddig a pontig**: kemény hibával bukik el már a
kérés-értelmezés szintjén. A Google API Improvement Proposals (AIP-193, hivatalos Google
tervezési szabvány) kifejezetten ellenzi a részleges hibákat: „APIs should not support
partial errors. Partial errors add significant complexity for users.” Nevesített,
elterjedt „X-Degraded” HTTP-fejléc konvenciót a kutató **sehol nem talált**.

### Circuit breaker és időkorlát

A Hystrix (Netflix) hivatalos wiki-dokumentációja írja le a három klasszikus állapotot:
CLOSED (normál), OPEN („it short-circuits all requests”), HALF-OPEN (egy próba-kérés
átengedése bizonyos idő után). Az AWS Builders' Library konkrét, számszerű timeout-
választási módszertant ad: „start with the latency metrics of the downstream service...
choose an acceptable rate of false timeouts (such as 0.1%). Then... look at the
corresponding latency percentile on the downstream service (p99.9 in this example).” Az
Azure Architecture Center „Bulkhead” mintája dedikált kapcsolat-/szálkeretet javasol
minden külső függőséghez, hogy egy elakadó szolgáltatás ne vigye magával a másik lábat
kiszolgáló erőforrásokat.

### Mit csinálnak a valós hibrid keresők — és az indexelési oldal

A hét vizsgált rendszer közül **csak az Elasticsearch** hivatalos dokumentációja mond ki
explicit állítást a lekérdezés-kori beágyazó-kiesésről, és az állítás fail-fast: „Removing
an inference endpoint will cause ingestion of documents and semantic queries to fail on
indices that define semantic_text fields with that inference endpoint as their
inference_id.” OpenSearch, Weaviate, Qdrant, Milvus, Typesense esetében **nem** talált a
kutató hivatalos állásfoglalást erre a pontos esetre — csak közösségi issue-alapú, közvetett
bizonyíték (T3) van. Az indexelési (írási) oldalon két, egymástól élesen elváló, mindkettő
hivatalos forrással alátámasztható minta van: (A) elutasítás/pipeline-megállás —
alapértelmezetten (Elasticsearch: „By default, pipeline processing stops when one of these
processors fails”, `ignore_failure` alapértelmezetten `false`); (B) azonnali commit +
aszinkron, idempotens utólagos beágyazás — a Supabase saját architektúrája (pgvector+pgmq+
pg_cron) szerint a trigger „fire off 'embedding jobs' that run asynchronously instead of
blocking the write path”, a Google Cloud Spanner hivatalos dokumentációja pedig kifejezetten
a hibakezelést is leírja: „Using SAFE.ML.PREDICT returns NULL for failed requests”, majd
„a WHERE embedding_column IS NULL filter to rerun your query.” A kutatók megjegyzik, hogy
a tervezett architektúra (fájl = commit pont, index utólag épül) a B mintát követi, és ez
bevett, hivatalos forrásokkal alátámasztott gyakorlat, nem egyedi megoldás.

---

## 5. SQ-04 — Törlésre jelölt bejegyzés az indexben

### FTS5 delete/rebuild mechanika

A hivatalos FTS5 dokumentáció három tábla-fajtát különböztet meg eltérő DELETE-
viselkedéssel. Normál táblánál egy `DELETE` automatikusan karbantartja az indexet. Külső
(external) content táblánál — ez a projekt architektúrája — a szöveg egy másik táblában
van, és „It is still the responsibility of the user to ensure that the contents of an
external content FTS5 table are kept up to date with the content table. One way to do
this is with triggers.” A hivatalos ajánlott minta egy trigger, amely törléskor egy
speciális `'delete'` parancsot ad ki a régi oszlopértékekkel. Kritikus feltétel: „If the
values 'inserted' into the text columns as part of a 'delete' command are not the same as
those currently stored within the table, the results may be unpredictable.” Contentless
táblánál egyáltalán nincs `UPDATE`/`DELETE` támogatás. A `delete-all` az egész indexet
üríti, a `rebuild` pedig „first deletes the entire full-text index, then rebuilds it based
on the contents of the table or content table” — ez mindig a **teljes** indexre vonatkozik,
nincs „csak ezt az egy dokumentumot építsd újra” parancs.

### Tombstone-ok, relevancia-torzítás, sebesség — a Lucene/Elasticsearch mért adatai

A Lucene mechanizmusa: „Lucene simply marks a bit in a per-segment bitset to record that
the document is deleted”, és „It is not until segments are merged that the bytes consumed
by deleted documents are reclaimed” (Elastic saját blogja, T2). A relevancia-torzítás
**hivatalos, explicit gyártói kijelentés**, nem következtetés: „Aggregate term statistics,
used for query scoring, will still reflect deleted terms and documents. When a merge
completes, the term statistics will suddenly jump closer to their true values, changing
hit scores.” Mért teljesítmény-hatás: „In testing with 50% deleted documents, query
performance declined between 18-46% depending on query type, with range queries dropping
from 1.2 to 0.6 QPS (46% reduction)” — gyártói saját mérés (T2). Az Elasticsearch soft
delete retenciós ideje alapértelmezetten „12h” (`retention.lease`), és célja explicit nem a
felhasználói „papírkosár”, hanem a replika-helyreállítás.

### Vektoros indexek: HNSW nem töröl valóban, IVF (Faiss) igen

A HNSW-ben nincs valódi törlés, csak `markDelete`: „for a delete operation concerning a
label x_d, HNSW employs the markDelete algorithm to flag and transfer it to a designated
deleted set” (arXiv 2407.07871v2). A csomópont fizikailag a gráfban marad éleivel együtt:
„the greedy walk still visits ghost nodes during search—they are filtered from output but
not from traversal” (arXiv 2606.18497v1, „Ghost Vectors”). Mért hatás: „unreachable
points” — olyan pontok, amelyeknek van kimenő, de nincs bejövő élük, és ezért „unless the
node v serves as the entry point... it will remain unvisited in subsequent search
operations.” Mért lassulás ismételt törlés+beszúrásnál: „the insertion speed using the
replaced_update method is notably slower by a factor of 5 to 10.” A Ghost Vectors kutatás
konkrét divergencia-mérése: „query latency differed by 4.3% between soft-delete and true
deletion, and 95% of top-K neighbor sets diverged between conditions.” A legfrissebb
(2026-os) dedikált kutatás (arXiv 2512.06200) szerint fizikai törléssel a keresési
pontosság stabilizálódik (~0,81 recall SIFT1B-n), logikai törléssel viszont „search
accuracy of logical deletion deteriorates” ismételt frissítéseknél — ugyanez a paper egy
saját, nem általánosítható hibrid stratégiát is javasol (logikai törlés egy küszöbig,
utána rebuild). A Faiss (IVF) hivatalos wiki-je szerint az IVF **valódi** eltávolítást
támogat („Supported by IndexFlat, IndexIVFFlat, IDMap”), de „efficient only when a
significant number of vectors needs to be removed” — egyesével nem hatékony itt sem.

### A soft delete + lekérdezési szűrő minta problémái és a takarítási küszöbök

Minden vizsgált rendszer explicit megnevezi, hogy a jelölt-de-nem-törölt bejegyzések
helyet foglalnak takarításig: „over time, these marked records can build up, wasting
memory and slowing down the system” (Qdrant). A Stanford IR-tankönyv (Manning/Raghavan/
Schütze) kimondja, hogy egy invalidation bitvektoros rendszerben „the correct number of
hits for a term is no longer a simple lookup” — vagyis a találatszám könnyen eltérhet a
ténylegesen látható eredményektől, ha a számlálás nem veszi figyelembe a szűrést.
Konkrét, dokumentált takarítási küszöbök: **Qdrant** — `deleted_threshold: 0.2` (a
töröltarány, ami fölött szegmens-optimalizáció indul) és `vacuum_min_vector_number: 1000`;
**Weaviate** — `cleanupIntervalSeconds` alapértelmezetten 300 másodperc; **Meilisearch** —
két feltétel bármelyike (törölt dokumentumok száma meghaladja az élőkét, vagy egy
lemez-méret küszöböt); **Elasticsearch** — retenciós lease alapértelmezetten 12 óra.

### bm25() torzítás — hivatalos képlet, saját levezetés

Az FTS5 `bm25()` képlete hivatalosan függ `N`-től (a sorok teljes száma), `avgdl`-től
(átlagos dokumentumhossz) és `n(qi)`-től (a kifejezést tartalmazó sorok száma). Ha egy
törlésre jelölt sor bent marad a táblában, mindhárom komponenst torzítja, amíg fizikailag
el nem tűnik. **Fontos**: a hivatalos FTS5 dokumentáció ezt **nem mondja ki explicit**
figyelmeztetésként — ez a képlet szerkezetéből fakadó, logikailag levezetett állítás, amit
az Elastic/Lucene explicit, analóg kijelentése (fent) más motorra vonatkozóan alátámaszt.

### Visszaállíthatóság

FTS5 oldalon olcsó: a `delete` parancs csak az FTS-indexből távolítja el a bejegyzést, nem
a content táblából — vagyis a visszavonás egy egyszerű újra-`INSERT`, ha a content tábla
sora megmaradt. Vektoros oldalon a Ghost Vectors kutatás mért bizonyítékot ad arra, hogy a
gyakorlatban használt rendszerek nem dobják el azonnal a nyers vektort: „When a user
requests data deletion, the systems typically only mark the record as deleted, leaving
the embedding on disk physically unchanged”, konkrétan „ChromaDB marks records in SQLite
metadata while leaving index.bin unchanged... Weaviate appends deletion metadata without
reclaiming HNSW slots.” Dedikált „undelete” API-t egyik vizsgált rendszer (Qdrant,
Weaviate, Milvus, Meilisearch, Typesense, Elasticsearch/Lucene) hivatalos dokumentációjában
sem talált a kutató.

### Mit csinálnak a valós rendszerek

Hét a nyolc vizsgált rendszer közül (SQLite FTS5, Lucene/Elasticsearch/OpenSearch, Qdrant,
Weaviate, Milvus, Meilisearch) a „jelöld meg most, takarítsd később tömegesen” mintát
követi — egyik sem távolítja el azonnal, soronként fizikailag a törölt adatot a fő
indexből. Az egyetlen dokumentált kivétel a Faiss `IndexIVFFlat` `remove_ids`, ami valódi,
azonnali eltávolítást végez, de architekturálisan más (explicit id-tárolás), és a
dokumentáció maga figyelmezteti, hogy soronkénti törlésre nem hatékony. A Typesense belső
mechanizmusát a hivatalos dokumentáció nem részletezi — ez nyitva marad.

---

## 6. Ellentmondások a forrásokban

### SQ-01: hol legyen a jogosultság-ellenőrzés RAG-visszakeresésben?

**AWS hivatalos biztonsági blogja** post-retrieval ellenőrzést ajánl a forrásrendszernél:
„This makes metadata filtering insufficient for organizations that require stronger
authorization controls”, mert „vector databases only sync periodically, meaning
permission changes in the source data aren't immediately reflected”
(aws.amazon.com/blogs/security/authorizing-access-to-data-with-rag-implementations/).
**Ezzel szemben** egy független mérnöki blog és a nagy vektor-DB gyártók saját mintája
előszűrést javasol a vektor-rétegben: „The vector store never returns an unauthorized
document in the first place; the model never processes it.”
(tianpan.co/blog/2026-05-04-permission-aware-retrieval-enterprise-rag-access-control). A
kutató feloldása: a két forrás **más réteget** véd — az AWS-érv arra vonatkozik, hogy a
jogosultsági *adat* elavulhat egy külső, aszinkron szinkronizált forrásrendszerhez képest,
nem azt állítja, hogy a keresőmotoron belüli post-filtert (a rangsorolás utáni szűrést)
ajánlaná; egy harmadik, dedikált ellenőrzési lépést iktat be. A projekt kontextusában
(ahol a jogosultság-forrás és az index ugyanabban a rendszerben, feltehetően szinkron
frissül) az AWS fő indoka kevésbé releváns, de az elv — ne bízz egyetlen rétegben —
átgondolásra érdemes.

### SQ-01: ront-e az előszűrés a HNSW recall-on?

Qdrant saját mérése szerint egy módosítatlan („plain”) HNSW-gráfon 1%-os szelektivitásnál
a recall 0,1%-ra zuhan; egy Weaviate-mérnök saját mérése szerint ugyanilyen szelektivitási
tartományban „the recall is perfect (100%)”. A kutató szerint ez **nem valódi
ellentmondás**: a Qdrant-mérés a worst-case, engineering nélküli HNSW-t mutatja be pont
azért, hogy indokolja, miért kellett az ACORN-t kifejleszteni; a Weaviate-mérés már a
Weaviate saját, beépített hibrid mechanizmusát méri (allow-list + automatikus flat-search
átváltás) — vagyis a „naiv HNSW + szűrő” és a „kereskedelmi vektor-DB beépített
szűrő-motorja” két különböző dolog, amit egyetlen forrás sem mond ki ilyen direktben
egymás mellé állítva.

### SQ-02: a „racy” módosítás ma ritkább vagy gyakoribb probléma?

A Git hivatalos állásfoglalása (2006-os megfigyelésre alapozva) szerint nagy projekteknél a
probléma a gyakorlatban ritka, mert „the initial computation of all object names in the
index takes more than one second”, ezért nincs racily clean bejegyzés. Apenwarr (2018)
ezzel szemben azt állítja, hogy a modern, gyors gépek és eszközök **miatt** a helyzet
gyakoribbá vált: „Computers are now so fast that you can save foo.c in your editor, and
then produce foo.o, and then compile foo, all in the same one-second time period.” A
kutató feloldása: a két állítás különböző munkaterhelésről szól — a Git érve nagy,
lassú fa-bejárásra vonatkozik, Apenwarr érve kis, gyors, esemény-vezérelt (egyetlen fájl
mentése + azonnali build) műveletekre. A projekt kontextusában ez azt jelenti, hogy a
kockázat a művelet méretétől függ: egy célzott, egyetlen fájlra vonatkozó újraolvasás
inkább az Apenwarr által leírt kockázati körbe esik, egy teljes fa-bejárás inkább a Git
által védett esethez hasonlít.

### SQ-03: circuit breaker — bevált minta vagy kerülendő komplexitás?

Ez egy valódi ellentmondás **ugyanazon gyártó két hivatalos dokumentuma között**. Az AWS
Well-Architected Framework a circuit breaker-t ajánlja: „The circuit breaker pattern can
be utilized here, which monitors failing calls to a downstream system.” Az AWS Builders'
Library (szintén hivatalos AWS-tartalom) viszont szkeptikus: a minta „widely promoted to
solve this problem” de „introduce modal behavior into systems that can be difficult to
test, and can introduce significant addition time to recovery”, és alternatívaként helyi
token-bucket-alapú retry-korlátozást javasol. A kutató szerint ez a Well-Architected
(magas szintű architektúra-ajánlás) és a Builders' Library (Amazon belső csapatainak
gyakorlati tapasztalata) közötti, nyilvánvalóan nem összehangolt nézőpont-különbség — az
egyik tervezési, a másik üzemeltetési szempontból érvel, és egyik forrás sem mondja ki,
hogy univerzálisan melyik a jobb.

### SQ-03: BM25 vagy dense — melyik jobb egyedül?

A BEIR paper és a „From BM25 to Corrective RAG” dolgozat szerint a BM25 gyakran veri a
dense-t egyedül (pl. ArguAna nDCG@10: BM25 0,315 vs DPR 0,175). Egy StackOverflow-tanulmány
(Zenodo) viszont a dense fölényét mutatja: „Dense retrieval achieves Recall@5 = 0.779 and
MRR = 0.670” a „sparse baseline (Recall@5 = 0.394, MRR = 0.292)”-hez képest. A kutató
feloldása: nem ellentmondás, hanem eltérő feltételek — a StackOverflow-tanulmány „sparse
baseline”-ja **TF-IDF, nem teljes BM25** (gyengébb lexikai alapmódszer, hiányzik belőle a
dokumentumhossz-normalizálás és a telítési függvény), és a lekérdezés-típus is eltér
(parafrázis-jellegű természetes nyelvi kérdés a domain-shiftelt, pontos terminológiát
igénylő BEIR/pénzügyi feladatokhoz képest).

### SQ-03: a stale/degradált válasz jelzése — élő gyakorlat vs visszavont szabvány

A CDN-szolgáltatók (Fastly, KeyCDN) ma is implementálják a `stale-if-error` mechanizmust,
de a hozzá eredetileg társított jelző-mechanizmus (HTTP Warning fejléc) elavult: „The
header was deprecated because it is not widely generated or surfaced to users (see
RFC9111).” A kutató szerint ez nem a funkció, hanem a jelző-mechanizmus visszavonása —
és óvatosságra int azzal a feltételezéssel szemben, hogy egy saját kitalált „X-Degraded”
jelző magától elterjedne, ha a hívó oldalak nem építik be kifejezetten a kezelését.

### SQ-04: a Weaviate tombstone-takarítás megoldja a problémát, vagy csak a gráf-bejárást javítja?

A Weaviate hivatalos dokumentációja szerint „tombstones are regularly cleaned up,
triggered periodically by the cleanupIntervalSeconds parameter” — ez azt sugallja, hogy a
törölt objektum ténylegesen eltűnik. A Ghost Vectors kutatás szerint azonban „Weaviate
appends deletion metadata without reclaiming HNSW slots”, és „Soft-deleted HNSW vectors
remain physically recoverable by accessing raw index files at the storage layer, bypassing
API access.” A kutató feloldása: a két állítás más rétegről szól — a hivatalos
dokumentáció a gráf-bejárási/logikai takarításról (a keresés ne akadjon el a tombstone-on),
a Ghost Vectors paper a lemez-szintű, byte-pontos törlésről. Egyik vizsgált vektor-DB
hivatalos dokumentációja sem állítja kifejezetten egyik irányban sem, hogy a takarítás
garantáltan felülírja-e a lemezt.

### SQ-04: a HNSW logikai törlés hatása — fokozatos vagy drámai romlás?

Az arXiv 2512.06200 paper szerint a logikai törlés romlása kordában tartható megfelelő
ütemű rebuilddel. Az arXiv 2407.07871v2 paper szerint viszont a probléma strukturális,
nem fokozatos: „the performance of HNSW and most graph-based indices become unacceptable
when faced with a large number of real-time deletions, insertions, and updates”, és az
„unreachable points” jelenség egyes pontok teljes elérhetetlenné válását okozza, nem
csak pontszám-csökkenést. A kutató szerint ez hangsúlykülönbség, nem cáfolat: az egyik
paper a tiszta törlést, a másik a törlés+beszúrás (replace) kombinációját vizsgálja — ha
a törlésre-jelölt állapot gyakori újra-szerkesztéssel is jár, a súlyosabb, strukturális
probléma is releváns lehet.

### SQ-04: van-e teljesítmény-előnye a soft delete-nek, vagy csak kompromisszum?

A Meilisearch hivatalos specifikációja tisztán előnyként állítja be: „Deleting documents
is extremely slow... Making deletion almost instantaneous by not deleting the document
when asked.” A Qdrant és Weaviate dokumentációja szerint viszont a felhalmozódó jelölt
rekordok problémát okoznak: „over time, these marked records can build up, wasting memory
and slowing down the system.” A kutató szerint ez nem ellentmondás, hanem időtávlat-
különbség — mindhárom rendszer mindkét mechanizmust együtt alkalmazza (gyors jelölés +
kötelező, ütemezett takarítás), csak a forrásaik más-más felét hangsúlyozzák.

---

## 7. Hiányok — amire nincs válasz

**SQ-01.** Nincs olyan forrás (sem hivatalos dokumentáció, sem tudományos publikáció),
amely kifejezetten az RRF-fúzió kontextusában mondaná ki, hogy a jogosultsági szűrésnek a
két láb egyesítése előtt vagy után kell történnie — ez a jelentésben szereplő
következtetés a kutató saját szintézise, nem idézet. Nincs kereső-index/ACL-specifikus
dokumentált eset a lapozás vagy a „did you mean”/autocomplete mint szivárgási csatorna
esetére. Nincs hivatalos (T1) SQLite-ajánlás a jogosultsági JOIN mintára, csak fórum-
alapú (T3) gyakorlati tapasztalat. Nem világos, hogy az Elasticsearch DLS role-query-je
automatikusan bekerül-e a kNN `filter`-be valódi pre-filterként, vagy más útvonalon fut. A
Typesense/Meilisearch beégetett szűrőinek pontos, motor-szintű pre-/post-filter jellegét
egyik hivatalos dokumentáció sem mondja ki technikai kifejezésekkel. Nincs számszerű,
publikált mérés az OpenSearch DLS önmagában vett latencia-overhead-jéről.

**SQ-02.** Nincs mért fordulópont arra, hány fájlnál/GB-nál válik a teljes tartalom-
hash-elés vállalhatatlanná egy napi konzisztencia-futásban. Nincs megbízható, konkrét
hash-throughput szám (GB/s) modern CPU-n T1/T2 forrásból. Meilisearch és Typesense esetén
nem található dokumentált konzisztencia-ellenőrző minta (index vs forrás-adat elcsúszás
kezelésére) — ez lehet *evidence of absence*, de nem zárható ki teljesen, hogy csak nem
került elő a keresési ablakban. A Zoekt és a tantivy pontos staleness-detektálási
mechanizmusát nem sikerült elsődleges forrásból megerősíteni. Nincs megerősített, konkrét
incidens arra, hogy egy automatikus index-javítás tévesen törölt volna élő adatot (csak
közvetett bizonyíték van arra, hogy az iparág ismeri és komolyan veszi ezt a kockázatot).
Nem egyértelmű, hogy a Solr DataImportHandler jelenleg is a Solr törzsének része-e.

**SQ-03.** Nincs egyetlen, univerzálisan idézhető szám a BM25-only vs hibrid romlásra —
a mért adatok (6,5%–40%) különböző benchmarkokból, különböző módszertannal származnak, és
nincs olyan kontrollált tanulmány, amely lekérdezés-típusonként (pontos azonosító vs
természetes nyelvi kérdés) bontva mérné ugyanazon a korpuszon a romlást. Az Anthropic
Contextual Retrieval Appendix PDF-jéből nem volt kinyerhető a nyers (nem-kontextualizált)
embeddings-only vs embeddings+BM25 táblázat. OpenSearch, Weaviate, Qdrant, Milvus
hivatalos dokumentációjában nincs explicit állásfoglalás arra, mi történik lekérdezéskor,
ha a beágyazó/modell szolgáltatás nem elérhető — csak közösségi issue-alapú (T3) közvetett
bizonyíték van. Nincs nevesített, elterjedt „X-Degraded” HTTP-fejléc konvenció sehol. Nem
egyértelmű, hogy egy Elasticsearch ingest-pipeline hiba a teljes bulk-kérést vagy csak az
érintett dokumentumot utasítja-e el. Nem világos, hogy a Vespa `coverage.degraded`
mechanizmusa kiterjed-e a beágyazó-kiesés esetére.

**SQ-04.** Nincs hivatalos FTS5-dokumentációs forrás, amely explicit kimondaná, hogy a
törölt-de-bent-hagyott sorok torzítják a `bm25()`-öt — ez a képlet szerkezetéből vett
logikai levezetés, nem idézett FTS5-állítás. Egyetlen vizsgált rendszer (Qdrant, Weaviate,
Milvus, Meilisearch, Typesense, Elasticsearch/Lucene) dokumentációjában sincs dedikált
„undelete”/visszaállítás API. Nincs SQLite FTS5-specifikus, publikált mérés arra, hogy egy
`WHERE fts MATCH ? AND status != 'törölt'` post-filter lekérdezés mennyivel lassabb egy
előre kitakarított indexnél — csak analóg (Lucene, HNSW) mérések vannak. A Typesense
belső (memóriabeli) törlés-mechanizmusát a hivatalos dokumentáció nem részletezi. Az
OpenSearch `_delete_by_query` és a Lucene-merge kapcsolatát hivatalos OpenSearch-forrás
nem tárgyalja explicit (csak a közös Lucene-eredetből levezetve feltételezhető).

---

## 8. Minden meglátogatott link

Tier-kulcs a forrásanyag szerint: **T1** = hivatalos dokumentáció/spec/forráskód/
peer-reviewed vagy arXiv publikáció. **T2** = megbízható másodlagos forrás VAGY gyártó
saját termékére vonatkozó teljesítményállítása. **T3** = fórum, levelezőlista, issue
tracker vita, vélemény, marketing (hivatalos domainen is, ha fórum/vélemény jellegű). Az
`[SQ01/02/03/04]` jelölés mutatja, melyik al-kérdés kutatásában szerepelt a link.

### T1 — Hivatalos dokumentáció, specifikáció, forráskód, tudományos/arXiv publikáció

| URL | SQ | Mire volt jó |
|---|---|---|
| https://www.sqlite.org/fts5.html | SQ01, SQ02, SQ04 | FTS5 hivatalos spec — nincs benne „JOIN”; `integrity-check`/`rebuild`/`delete`/`delete-all` parancsok; contentless/external content táblák DELETE-viselkedése; `bm25()` képlet. |
| https://sqlite.org/pragma.html | SQ02 | `PRAGMA integrity_check` (O(N log N)) vs `quick_check` (O(N)). |
| https://learn.microsoft.com/en-us/azure/search/vector-search-filters | SQ01 | Azure preFilter/postFilter definíció, mért lassulási arány. |
| https://learn.microsoft.com/en-us/azure/search/search-document-level-access-overview | SQ01 | Dokumentum-szintű hozzáférés-vezérlés, Entra ID. |
| https://docs.weaviate.io/weaviate/concepts/filtering | SQ01 | Pre/post-filter definíció, ACORN, sweeping. |
| https://docs.weaviate.io/weaviate/configuration/rbac | SQ01 | RBAC granularitás — kollekció-szint. |
| https://docs.weaviate.io/weaviate/manage-collections/multi-tenancy | SQ01 | Fizikai shard-per-tenant izoláció. |
| https://www.elastic.co/docs/deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level | SQ01 | DLS mechanizmus, count/aggregáció és pontszám-szivárgás hivatalos figyelmeztetése. |
| https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-knn-query | SQ01 | kNN `filter` = explicit pre-filter. |
| https://docs.opensearch.org/2.11/security/access-control/document-level-security/ | SQ01, SQ04 (kontextus) | Lucene-level/filter-level/adaptive DLS módok. |
| https://milvus.io/docs/filtered-search.md | SQ01 | Alapértelmezett = előszűrés, iteratív szűrés alternatíva. |
| https://typesense.org/docs/guide/data-access-control.html | SQ01 | Scoped API key — beégetett, felülírhatatlan `filter_by`. |
| https://typesense.org/docs/30.2/api/joins.html | SQ01 | Collection-join, `!$deny_list(...)` minta. |
| https://www.meilisearch.com/docs/capabilities/security/overview | SQ01 | Tenant token — beágyazott szűrő minden kereséshez. |
| https://docs.pinecone.io/guides/data/understanding-metadata | SQ01 | top_k alákerülés csak sparse vektoroknál dokumentált. |
| https://qdrant.tech/documentation/concepts/filtering/ | SQ01 | Szűrés-konstrukció, payload index — végrehajtási sorrendről nem nyilatkozik. |
| https://arxiv.org/pdf/2510.27141 (Compass paper) | SQ01 | Formális pre/post-filter definíciók, <0,1% küszöb, post-filter „több körre” bomlása. |
| https://arxiv.org/abs/2401.07119v1 (Curator paper) | SQ01 | Többbérlős vektor-DB index-stratégiák. |
| https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/WebAppSideChannel-final.pdf | SQ01 | Oldalcsatorna-szivárgás titkosított forgalomban is (csomagméret, időzítés). |
| https://www.postgresql.org/about/news/pgvector-080-released-2952 | SQ01 | pgvector 0.8.0 iteratív bejárás, overfiltering elleni mechanizmus. |
| https://docs.vespa.ai/en/securing-your-vespa-installation.html | SQ01 | Csak hálózati/cluster-szintű védelem — nincs dokumentum-szintű ACL. |
| https://git-scm.com/docs/racy-git | SQ02 | „Racy git” jelenség, stat-cache mezők, futásidő-teszt. |
| https://man7.org/linux/man-pages/man1/rsync.1.html | SQ02 | `--checksum` vs alapértelmezett méret+mtime „quick check”. |
| https://borgbackup.readthedocs.io/en/stable/usage/create.html | SQ02 | Files-cache módok (ctime/mtime/inode/size) kompromisszumai. |
| https://fscrawler.readthedocs.io/en/latest/admin/fs/local-fs.html | SQ02 | `checksum`, `update_rate`, `remove_deleted` opciók. |
| https://cwiki.apache.org/confluence/display/solr/DataImportHandler | SQ02 | Solr DIH `deltaQuery`, `deletedPkQuery`, `last_index_time`. |
| https://www.recoll.org/usermanual/webhelp/docs/RCL.INDEXING.MONITOR.html | SQ02 | inotify valós idejű figyelés, terhelési figyelmeztetés, „trigger incremental pass”. |
| https://github.com/sourcegraph/zoekt/blob/main/doc/design.md | SQ02 | „Reindex any changed repositories” — mechanizmus nem részletezve (negatív találat). |
| https://openzfs.github.io/openzfs-docs/man/master/8/zpool-scrub.8.html | SQ02 | ZFS scrub, heti/havi systemd-timer minta. |
| https://docs.datastax.com/en/cassandra-oss/3.x/cassandra/operations/opsRepairNodesManualRepair.html | SQ02 | Anti-entropy repair, Merkle-fa. |
| https://docs.datastax.com/en/cassandra-oss/3.x/cassandra/operations/opsRepairNodesWhen.html | SQ02 | Repair gyakorisági ajánlás (napi/heti-havi). |
| https://kubernetes.io/docs/concepts/architecture/controller/ | SQ02 | „Reconciliation pattern” elnevezés. |
| https://rclone.org/commands/rclone_sync/ | SQ02 | `--max-delete`, hiba esetén nem törlő védőkorlát. |
| https://man7.org/linux/man-pages/man5/nfs.5.html | SQ02 | NFS attribútum-gyorsítótár, `noac` korlátai. |
| https://obsidian.md/help/plugins/search | SQ02 | Nincs dokumentált külön perzisztens FTS-index (negatív találat). |
| https://www.elastic.co/guide/en/elasticsearch/reference/8.19/docs-reindex.html | SQ02 | Reindex API — teljes vs részleges (`op_type: create`). |
| https://docs.rs/tantivy/latest/tantivy/struct.IndexReader.html | SQ02 | `ReloadPolicy::OnCommitWithDelay` — más réteg (író→olvasó láthatóság). |
| https://arxiv.org/html/2407.08284v1 | SQ02 | Hash-algoritmus sebesség (hashes/sec) — bizonytalan bemenet-méret, erős fenntartással. |
| https://github.com/BLAKE3-team/BLAKE3 | SQ02 | Benchmark-diagram — kép formátumú, nem kinyerhető (nem hasznosítva). |
| https://github.com/dadoonet/fscrawler/blob/fscrawler-2.9/docs/source/admin/fs/elasticsearch.rst | SQ02 | Csak mezőneveket sorol fel — negatív találat. |
| https://www.ibm.com/docs/SS4QMC_10.0.0/installation/c_IndexSynchronizationConcepts.html | SQ02 | IBM Sterling OMS — kézi „not-synchronized” jelölés. |
| https://confluence.atlassian.com/enterprise/fix-indexing-issues-with-index-auto-healing-1540234564.html | SQ02 | Index auto-healing — napi cron, index-árva/DB-árva/elavult kategóriák, „Unhealthy” → kézi. |
| https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_mitigate_interaction_failure_graceful_degradation.html | SQ03 | Graceful degradation definíció, circuit breaker ajánlás. |
| https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/design-interactions-in-a-distributed-system-to-mitigate-or-withstand-failures.html | SQ03 | Kontextus, nem idézve közvetlenül. |
| https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/circuit-breaker.html | SQ03 | Closed/Open/Half-open (név nélkül) állapotok. |
| https://learn.microsoft.com/en-us/azure/architecture/patterns/queue-based-load-leveling | SQ03 | „Nem javasolt alacsony-latenciájú szinkron válaszra” korlátozás. |
| https://learn.microsoft.com/en-us/azure/architecture/patterns/bulkhead | SQ03 | Bulkhead — erőforrás-izoláció függőségenként. |
| https://sre.google/sre-book/addressing-cascading-failures/ | SQ03 | Korai elutasítás (kis várólista), HTTP 503 minta. |
| https://sre.google/sre-book/handling-overload/ | SQ03 | Degradált válasz definíció, komplexitás kockázata. |
| https://docs.vespa.ai/en/graceful-degradation.html | SQ03 | `coverage.degraded` mező — élő minta a degradáció-jelzésre. |
| https://docs.vespa.ai/en/embedding.html | SQ03 | Embedder-hiba esetéről nincs infó (negatív találat). |
| https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/semantic-text-reference | SQ03 | Inference endpoint hiánya → hiba ingestnél ÉS lekérdezésnél is. |
| https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-semantic-query | SQ03 | Hibakezelésről nincs infó (negatív találat). |
| https://www.elastic.co/docs/reference/enrich-processor/inference-processor | SQ03 | `ignore_failure` alapértelmezetten `false`. |
| https://www.elastic.co/guide/en/elasticsearch/reference/master/handling-failure-in-pipelines.html | SQ03 | „Pipeline processing stops when one of these processors fails.” |
| https://www.elastic.co/docs/manage-data/ingest/transform-enrich/error-handling | SQ03 | `on_failure`/`ignore_failure` általános leírás. |
| https://www.elastic.co/docs/solutions/search/the-search-api | SQ03 | `timed_out`, `_shards.failed/skipped`, `allow_partial_search_results`. |
| https://milvus.io/docs/embedding-function-overview.md | SQ03 | Beágyazó-hibáról nincs infó (negatív találat). |
| https://typesense.org/docs/30.2/api/vector-search.html | SQ03 | Retry-mechanizmus (`remote_embedding_timeout_ms`/`num_tries`) — kimerülés utáni viselkedés nincs dokumentálva. |
| https://docs.opensearch.org/latest/ingest-pipelines/processors/text-embedding/ | SQ03 | Modell-elérhetetlenségről nincs infó (negatív találat). |
| https://docs.opensearch.org/latest/ingest-pipelines/pipeline-failures/ | SQ03 | Csak navigációs váz (negatív találat). |
| https://docs.opensearch.org/latest/query-dsl/compound/hybrid/ | SQ03 | Hibakezelésről nincs infó (negatív találat). |
| https://docs.cloud.google.com/spanner/docs/backfill-embeddings | SQ03 | `SAFE.ML.PREDICT` → `NULL`, idempotens `WHERE ... IS NULL` újrafuttatás. |
| https://google.aip.dev/193 | SQ03 | „APIs should not support partial errors” — tervezési ajánlás. |
| https://www.rfc-editor.org/rfc/rfc5861.txt | SQ03 | `stale-if-error` Cache-Control kiterjesztés. |
| https://github.com/netflix/hystrix/wiki/how-it-works | SQ03 | CLOSED/OPEN/HALF-OPEN állapotok. |
| https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/file/65b9eea6e1cc6bb9f0cd2a47751a186f-Paper-round2.pdf (BEIR) | SQ03 | BM25 vs DPR/ANCE/TAS-B nDCG@10, domain-shift magyarázat. |
| https://trec.nist.gov/pubs/trec30/papers/Overview-DL.pdf | SQ03 | TREC 2021 DL — BM25 vs neurális nDCG@10. |
| https://arxiv.org/html/2604.01733v1 (From BM25 to Corrective RAG) | SQ03 | BM25/dense/hybrid nDCG@10 táblázat pénzügyi dokumentumokon. |
| https://d1.awsstatic.com/builderslibrary/pdfs/timeouts-retries-and-backoff-with-jitter.pdf | SQ03 | Timeout-választási módszertan (p99.9), circuit breaker kritikája. |
| https://arxiv.org/html/2606.18497v1 (Ghost Vectors) | SQ04 | Soft-delete rekonstruálhatóság, 4,3% latencia-eltérés, 95% top-K divergencia. |
| https://arxiv.org/html/2407.07871v2 (Enhancing HNSW Index for Real-Time Updates) | SQ04 | `markDelete`, „unreachable points”, 5–10x lassabb `replaced_update`. |
| https://arxiv.org/html/2512.06200 (How Should We Evaluate Data Deletion in Graph-Based ANN Indexes?) | SQ04 | Fizikai törlés recall-stabilizáció (~0,81 SIFT1B), logikai törlés romlása, „Deletion Control” stratégia. |
| https://openreview.net/pdf?id=lnaC19Pd30 | SQ04 | Fetch sikertelen (403) — arXiv-változat használva helyette. |
| https://github.com/facebookresearch/faiss/wiki/Special-operations-on-indexes | SQ04 | `remove_ids` — valódi törlés IVF-nél, id-eltolódás szekvenciális indexeknél. |
| https://github.com/oven-sh/bun/issues/31247 | SQ04 | Ismert csapda: Bun macOS arm64 SQLite 3.43.2, FTS5 UPDATE/DELETE → korrupció. |
| https://www.elastic.co/docs/reference/elasticsearch/index-settings/history-retention | SQ04 | Soft delete retenciós lease (alapért. 12h). |
| https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-delete-by-query | SQ04 | Snapshot-alapú működés, verziókonfliktus — segment-merge-ről nem szól. |
| https://qdrant.tech/documentation/ops-optimization/optimizer/ | SQ04 | `deleted_threshold: 0.2`, `vacuum_min_vector_number: 1000`. |
| https://docs.weaviate.io/weaviate/manage-objects/delete | SQ04 | Csak API-szintű leírás, belső mechanizmus nélkül. |
| https://docs.weaviate.io/weaviate/config-refs/indexing/vector-index | SQ04 | `cleanupIntervalSeconds` (300s), tombstone-definíció. |
| https://github.com/weaviate/weaviate/pull/5700 | SQ04 | Tombstone-takarítás késleltethető/konfigurálható (fejlesztői PR). |
| https://milvus.io/docs/delete-entities.md | SQ04 | Csak API-szintű leírás. |
| https://milvus.io/blog/2022-02-07-how-milvus-deletes-streaming-data-in-distributed-cluster.md | SQ04 | Logikai törlés bitset+bloom filter, fizikai törlés csak Compaction-kor. |
| https://specs.meilisearch.dev/specifications/text/0136-documents-soft-deletion.html | SQ04 | Pontos purge-feltételek (törölt>élő VAGY lemez-küszöb). |
| https://typesense.org/docs/30.2/api/documents.html | SQ04 | Csak végpontok, belső mechanizmus nélkül (negatív találat). |
| https://docs.opensearch.org/latest/api-reference/document-apis/delete-by-query/ | SQ04 | Csak funkcionális leírás, belső Lucene-mechanizmus nélkül. |
| https://nlp.stanford.edu/IR-book/html/htmledition/dynamic-indexing-1.html (Manning/Raghavan/Schütze) | SQ04 | Invalidation bit vector, találatszám-torzulás dinamikus indexelésnél. |

### T2 — Megbízható másodlagos forrás / gyártó saját teljesítményállítása

| URL | SQ | Mire volt jó |
|---|---|---|
| https://towardsdatascience.com/effects-of-filtered-hnsw-searches-on-recall-and-latency-434becf8041c/ | SQ01 | Weaviate-mérnök saját mérése — szigorú szűrőnél is 100% recall. |
| https://qdrant.tech/articles/filtered-vector-search-acorn/ | SQ01 | ACORN — konkrét recall/latencia számok 1%-os szelektivitásnál. |
| https://qdrant.tech/blog/pre-filtering-vs-post-filtering/ | SQ01 | „Why Qdrant Does Neither” — hibrid mechanizmus. |
| https://qdrant.tech/articles/data-privacy/ | SQ01 | RBAC — kulcs-szintű, kollekció-granularitású. |
| https://weaviate.io/blog/speed-up-filtered-vector-search | SQ01 | ACORN „akár 10x” gyorsulás (grafikonban). |
| https://eliatra.com/blog/performance-improvements-for-the-access-control-layer-of-opensearch/ | SQ01 | Saját optimalizáció mérése — 58%/542% javulás. |
| https://www.elastic.co/search-labs/blog/vector-search-filtering | SQ01 | Pre/post-filter HNSW-interakció, ACORN-1 mérés. |
| https://www.pinecone.io/learn/rag-access-control/ | SQ01 | Hit-rate alapú döntés elő/utószűrés között. |
| https://aws.amazon.com/blogs/security/authorizing-access-to-data-with-rag-implementations/ | SQ01 | Post-retrieval jogosultság-ellenőrzés ajánlása (ellentmondás-forrás). |
| https://aws.amazon.com/blogs/database/supercharging-vector-search-performance-and-relevance-with-pgvector-0-8-0-on-amazon-aurora-postgresql | SQ01 | pgvector 0.8.0 mérés — recall 10%→100%, 1%→100%. |
| https://tianpan.co/blog/2026-05-04-permission-aware-retrieval-enterprise-rag-access-control | SQ01 | Előszűrés melletti érvelés, gyártói minták megnevezése. |
| https://apenwarr.ca/log/20181113 | SQ02 | mtime minden gyengesége, `redo` build-rendszer 6-mezős minta. |
| https://www.recoll.org/pages/perfs.html | SQ02 | Mért indexelési sebesség (PDF/HTML, SSD vs NFS). |
| https://developerdocs.hawksearch.com/docs/full-vs-partial-indexing | SQ02 | Teljes vs részleges rebuild döntési szabály (változás típusa). |
| https://www.elastic.co/search-labs/blog/improving-information-retrieval-elastic-stack-hybrid | SQ03 | RRF +18%/+24% nDCG@10 BM25-höz képest (BEIR). |
| https://www.anthropic.com/engineering/contextual-retrieval | SQ03 | 35%/49%-os failure-rate csökkenés BM25+embedding kombinációval. |
| https://www-cdn.anthropic.com/5722e7658c9302d8b97a3238de1bb8e6afdf04b9.pdf | SQ03 | Appendix — konkrét sorok nem kinyerhetők (részleges gap). |
| https://supabase.com/blog/automatic-embeddings | SQ03 | Aszinkron beágyazás-generálás — sor azonnal commitolódik. |
| https://tianpan.co/blog/2026-04-12-hybrid-search-production-bm25-dense-embeddings | SQ03 | Konkrét lekérdezés-típusok, ahol BM25 nyer (hibakódok, SKU-k). |
| https://weaviate.io/blog/weaviate-1-22-release | SQ03 | Async vector index building — brute-force amíg az index épül. |
| https://zenodo.org/records/18807773 | SQ03 | StackOverflow tanulmány — dense veri a (TF-IDF) sparse-t (ellentmondás-forrás). |
| https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Warning | SQ03 | HTTP Warning fejléc elavulása (RFC 9111). |
| https://www.elastic.co/blog/lucenes-handling-of-deleted-documents | SQ04 | Tombstone-bitset, „term statistics jump”, mért 18–46% lassulás. |

### T3 — Fórum, levelezőlista, issue tracker, harmadik féltől származó tartalom, vélemény

| URL | SQ | Mire volt jó |
|---|---|---|
| https://sqlite.org/forum/info/509bdbe534f58f20 | SQ01 | „JOINs with FTS5 virtual tables are very slow” — ANALYZE 170s→0,259s. |
| https://sqlite.org/forum/forumpost/5b303ab003f91660 | SQ01 | `MATCH` nem működik JOIN-alias mellett. |
| https://sqlite.org/forum/info/e0e30e9eb1998e3c9305aea26957bec804615283969d11c1f9326a6b787526eb | SQ01 | „Bad query plans from FTS5” — statikus költségbecslés. |
| https://www.postgresql.org/message-id/1985636.6fXRgaOMqv%40peanuts2 | SQ01 | RLS leakproof-függvények hiánya, IDOR mint fő fenyegetés. |
| https://astconsulting.in/database/implement-access-control-vespa | SQ01 | Nem tudta tisztázni, natív-e a Vespa ACL — alacsony evidenciaérték. |
| https://github.com/restic/restic/issues/2179 | SQ02 | mtime-alapú hibás változás-észlelés csomagkezelőnél. |
| https://github.com/dadoonet/fscrawler/issues/531 | SQ02 | „remove deleted” funkció megbízhatatlansága (ellenkező irányú hiba). |
| https://forum.obsidian.md/t/stuck-index-cache-bases-unaware-of-new-notes-outline-heading-link-suggestions-empty-rebuild-cache-button-inert/108785 | SQ02 | Felhasználói panasz — a cache/index „beragad”. |
| https://github.com/elastic/elasticsearch/issues/115692 | SQ03 | Konkrét hibaüzenet hiányzó inference endpointnál. |
| https://github.com/elastic/elasticsearch/pull/136732 | SQ03 | Compound retriever (RRF) shard-szintű hibakezelése — mérnöki vita. |
| https://github.com/weaviate/weaviate/issues/2892 | SQ03 | „Hybrid search expose errors from underlying vectorizer.” |
| https://github.com/weaviate/weaviate/issues/4346, #6873, #7681, #6695, #8366, #10424 | SQ03 | Háttér-kontextus, konkrét idézet nélkül. |
| https://github.com/weaviate/weaviate/issues/7156 | SQ03 | Aszinkron vectorizáció írási hibái. |
| https://github.com/weaviate/weaviate/issues/4587 | SQ03 | „Async Vectorizer Modules” feature-kérés. |
| https://forum.weaviate.io/t/hybrid-search-giving-errors-about-missing-vectorizer-but-objects-are-vectorized-correctly/2092 | SQ03 | Közösségi tapasztalat vectorizer-hibáról. |
| https://github.com/opensearch-project/ml-commons/issues/2838, #2823, #3582, #2808, #2981 | SQ03 | Modell-deploy hibák megerősítése, hivatalos állásfoglalás nélkül. |
| https://forum.opensearch.org/t/ml-model-has-to-be-re-deployed-each-time-ml-node-is-restarted/21120 | SQ03 | Modell-újratelepítési probléma csomópont-újraindításkor. |
| https://sqlite.org/forum/forumpost/dde862dbb3 | SQ04 | „FTS5 Error database disk image is malformed after 'delete'” — rokon tünet. |
| https://github.com/qdrant/qdrant/issues/6556 | SQ04 | Nincs dedikált „undelete” API — közvetett bizonyíték. |
| https://github.com/qdrant/qdrant/issues/2550 | SQ04 | Törölt pontok vektor-adata nem tűnik el azonnal. |
| https://github.com/weaviate/weaviate/issues/5732 | SQ04 | Tombstone-ok takarítás után is megmaradhatnak (kontextus). |

### Megtalált, de nem (vagy csak háttérként) felhasznált linkek

- `opendistro.github.io/for-elasticsearch-docs/...` [SQ01] — elavult (Open Distro), nem idézve.
- `docs.opensearch.org/latest/security/access-control/document-level-security/` [SQ01] — csak navigációs váz, a `2.11` verziót használták helyette.
- `darksi.de/13.sqlite-fts5-structure/`, `medium.com/@johnidouglasmarangon/...`, `sql-easy.com/...` [SQ01] — általános FTS5-bevezetők, nem válaszoltak a JOIN/ACL kérdésre.
- `ieeexplore.ieee.org/document/6558424` [SQ01] — paywall mögött, nem elérhető.
- `scylladb.com/2022/06/30/preventing-data-resurrection-with-repair-based-tombstone-garbage-collection/` [SQ02] — csak cím, nem lekérve.
- Marketing/összehasonlító oldalak (ssojet.com, mojoauth.com, devtoolspro.org, guptadeepak.com) [SQ02] — forrás nélküli, „content farm” jellegű, nem használva.
- `opensearch.org/blog/cold-start-search/` [SQ03] — más témáról (shard-refresh) szól.
- `qdrant.tech/documentation/inference/cloud-inference/`, `.../inference-api/` [SQ03] — funkció-leírás, hibaviselkedés nélkül.
- `accelate.ai/...`, `sesen.ai/...`, `denser.ai/...`, `supermemory.ai/...` [SQ03] — marketing-jellegű, módszertan nélküli blogok.
- `github.com/elastic/elasticsearch/issues/29530`, `pull/30226`, `pull/34953` [SQ04] — Elasticsearch saját fejlesztési vitái, a hivatalos retenciós doksi pontosabb volt.
- `github.com/milvus-io/milvus/discussions/28565`, `/26828`, `/24875`, `/19259` [SQ04] — felhasználói kérdések, a hivatalos blog pontosabb forrás volt.
- Általános „soft delete search index anti-pattern” keresési találatok (GeeksforGeeks, Spice AI, DataAspirant) [SQ04] — nem T1/T2 minőségű, nem specifikus a törlési torzításra.
