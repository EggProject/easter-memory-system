# Ellentmondások — ahol a források nem egyeznek

Kampány: `kereses-indexeles` · 2026-09-08

> Al-kérdésenként bontva, ahogy a kereső ügynökök rögzítették.


---

## SQ-01 — Hol szűrjön a jogosultság a keresésben

# SQ-01 — Ellentmondások a forrásokban

## 1. Hol legyen a jogosultság-ellenőrzés RAG-visszakeresésben: a vektor-rétegben (előszűrés) vagy a visszakeresés UTÁN, a forrásrendszernél?

**A oldal — AWS hivatalos biztonsági blogja: post-retrieval ellenőrzés a forrásnál**

> „This makes metadata filtering insufficient for organizations that require stronger
> authorization controls." és „To implement robust authorization for knowledge base data
> access, verify permissions directly at the data source rather than relying on intermediate
> systems."

Indoklás: „vector databases only sync periodically, meaning permission changes in the source
data aren't immediately reflected." Az ajánlott architektúra: (1) chunkok visszakeresése a
tudásbázisból, (2) jogosultság-ellenőrzés a forrásrendszernél (pl. S3 Access Grants), (3)
csak az engedélyezett chunkok kerülnek az LLM-hez.
— https://aws.amazon.com/blogs/security/authorizing-access-to-data-with-rag-implementations/

**B oldal — független mérnöki blog + a nagy vektor-DB gyártók saját mintája: előszűrés a vektor-rétegben**

> „If the application logic has a bug, makes a wrong assumption, or is circumvented by a
> prompt injection attack, the documents flow through anyway." és „The vector store never
> returns an unauthorized document in the first place; the model never processes it."
— https://tianpan.co/blog/2026-05-04-permission-aware-retrieval-enterprise-rag-access-control

Ezt támasztja alá közvetve minden olyan hivatalos gyártói dokumentáció, ahol a szűrés a
lekérdezésbe van beégetve (Typesense scoped key, Meilisearch tenant token, Elasticsearch kNN
pre-filter, Weaviate multi-tenancy fizikai particionálás) — ezek mind azt sugallják, hogy a
*helyes* hely a lekérdezés/index szintje, nem egy utólagos alkalmazás-rétegbeli szűrés.

**Miért van ez az eltérés — a források saját magyarázata alapján:** az AWS-cikk kifejezetten
azzal érvel, hogy a vektoros index **metaadata elavulhat** a forrásrendszerhez képest (a
szinkronizáció késleltetése miatt), ezért a vektor-DB-beli előszűrés önmagában
*nem elég friss* garancia — de ez nem azt jelenti, hogy az AWS a post-filtert (a
rangsorolás utáni szűrést a *találati listán*) ajánlaná; ők egy **harmadik, dedikált
jogosultság-ellenőrző lépést** iktatnak be a visszakeresés és az LLM-kontextusba-helyezés
közé, ami *nem azonos* a kérdésben vizsgált „post-filtering" hibrid-keresési technikával
(ahol a szűrés a keresőmotoron belül, a rangsorolás után történik). A két forrás tehát
részben **más réteget** véd (friss-e a jogosultsági adat vs. hol fut le a szűrés
algoritmikusan), de a gyakorlati tanácsuk így is szemben áll: az AWS explicit **nem bízik**
a vektor-DB-beli (pre-)szűrésben mint egyedüli védelemben, míg a B-oldal források szerint a
vektor-réteg az egyetlen hely, ahol garantálható, hogy „a modell sosem látja" a
dokumentumot.

**Relevancia a mi tervünkhöz:** mivel nálunk a jogosultság-forrás (projekt-tagság) és az
index ugyanabban a rendszerben, feltehetően szinkron módon frissül (nem külső, aszinkron
szinkronizált forrásrendszerről van szó, mint az AWS-cikk „knowledge base" esetében), az
AWS-érvelés fő indoka (elavult metaadat) nálunk kevésbé releváns — de az elv (ne bízz egyetlen
rétegben) érdemes megfontolásra a K-01/K-02 (index-lemez elcsúszás) SQ-02 kérdés
kontextusában is.

---

## 2. Ront-e az előszűrés a HNSW recall-on? — látszólagos, de feloldható ellentmondás

**A oldal — a szűrés tönkreteszi a gráfbejárást (Qdrant saját mérése, „plain graph"):**

> „Filter out 96% of the points and fewer than one link per node survives on average, so
> traversal can get stranded before it reaches the true nearest matches." Mért szám 1%-os
> szelektivitásnál: „Plain graph: 0.1% @ 1.6ms" recall/latencia.
— https://qdrant.tech/articles/filtered-vector-search-acorn/

**B oldal — a szűrés nem rontja érdemben a recall-t (Weaviate saját mérése):**

> „as filters get more restrictive (less than 20% of the dataset contained) the recall is
> perfect (100%)" — 250k objektumon, Weaviate v1.8.0-n mérve.
— https://towardsdatascience.com/effects-of-filtered-hnsw-searches-on-recall-and-latency-434becf8041c/

**Feloldás:** a két mérés **nem ugyanazt a mechanizmust** méri. A Qdrant „plain graph" egy
*módosítatlan*, extra élek/ACORN nélküli HNSW-gráfon futtatott naiv előszűrést jelent — ez a
worst-case forgatókönyv, amit a Qdrant-cikk kifejezetten azért mutat be, hogy demonstrálja,
miért kellett az ACORN-t/filterable-HNSW-t kifejleszteni. A Weaviate-mérés viszont már a
Weaviate saját, **beépített** hibrid mechanizmusát méri (inverz index allow-list + automatikus
flat-search-cutoff szigorú szűrőknél) — ami pontosan az a fajta „engineered fix", amit a
Qdrant-cikk is leír megoldásként. **A két adat tehát nem mond ellent egymásnak**, csak azt
mutatja, hogy a „naiv HNSW + szűrő" és a „kereskedelmi vektor-DB beépített szűrő-motorja"
két különböző dolog — de ezt egyetlen forrás sem mondja ki ilyen direktben egymás mellé
állítva, ez az én szintézisem a két adatsorból. Emiatt soroltam ide, ellentmondásként
jelölve, nem a `megallapitasok.md` fő szövegébe rejtve.

---

## 3. Pre-filter mindig lassabb vagy mindig gyorsabb?

**Azure AI Search:** „Prefiltering is almost always slower than postfiltering, except on
small indexes where performance is approximately equal." — mégis ezt ajánlja
alapértelmezettként, mert „Prefilter is the default mode because it favors recall and
quality over latency."
— https://learn.microsoft.com/en-us/azure/search/vector-search-filters

**Qdrant:** a saját (nem naiv) előszűrő mechanizmusuk (filterable HNSW) a mért adatok szerint
(3. pont a `megallapitasok.md`-ben) **gyorsabb is, pontosabb is** lehet, mint egy „plain
graph + ACORN" utólagos javítás (pl. „Filterable HNSW: 99.8% @ 1.0ms" vs „Plain graph +
ACORN: 67.7% @ 4.7ms" ugyanannál a szűrőnél).

**Feloldás:** nincs valódi ellentmondás — az Azure-állítás az **általános, algoritmus-
agnosztikus** pre- vs post-filter összehasonlításra vonatkozik (amikor a pre-filter egy
külön maszk-számítást jelent az egész indexen), míg a Qdrant saját, index-idejű extra-éllel
kiegészített („filterable") HNSW-je egy **más algoritmus**, aminél a szűrés-vs-sebesség
kompromisszum másképp fest. Ez megerősíti az 1. és 3. pontban leírt fő tanulságot: a
„pre-filter" szó két, jelentősen eltérő teljesítményű implementációt takarhat, és ezt a
tervezésnél explicit külön kell választani.


---

## SQ-02 — Index és lemez elcsúszásának észlelése és javítása

# SQ-02 — Ellentmondások a forrásokban

## 1. A "racy" (ugyanabban a másodpercben történő) módosítás ma inkább ritkább vagy inkább gyakoribb probléma?

**A Git hivatalos állásfoglalása (2006-os empirikus megfigyelésre alapozva) — a probléma
gyakorlatban ritka nagy projekteknél:**

> „In a large project where raciness avoidance cost really matters, however, the initial
> computation of all object names in the index takes more than one second, and the index
> file is written out after all that happens. Therefore the timestamp of the index file
> will be more than one second later than the youngest file in the working tree. This means
> that in these cases there actually will not be any racily clean entry in the resulting
> index." — https://git-scm.com/docs/racy-git (Runtime penalty / Avoiding runtime penalty
> szakasz)

Emiatt a Git 2006 óta **nem** tartalmaz külön védekező kódot a runtime-büntetés
elkerülésére, mert a szerzők úgy ítélték meg, hogy a helyzet a gyakorlatban nem fordul elő.

**Apenwarr (2018) ezzel szemben kifejezetten azt állítja, hogy a modern, gyors gépek és
eszközök MIATT a helyzet gyakoribbá vált:**

> „Computers are now so fast that you can save foo.c in your editor, and then produce foo.o,
> and then compile foo, all in the same one-second time period. If you do this and, say,
> save foo.c twice in the same second (and you have one-second granularity mtimes), then
> make can't tell if foo.o and foo are up to date or not." — https://apenwarr.ca/log/20181113
>
> „This often happens if you're using one of those fancy new inotify-based tools that fires
> off a compile immediately, every time you hit save in your editor... Symptom: needing to
> save your source file twice before the autocompiler catches it." — uo.

**Mi magyarázza az eltérést:** a két állítás **különböző munkaterhelésről** szól. A Git
saját érve a *saját indexének felépítési idejére* vonatkozik (nagy projektnél az `add`/
`checkout` maga is >1 másodpercig tart, ami "elhúzza" az index-fájl időbélyegét a
fájlokétól). Apenwarr érve viszont **kis, gyakori, esemény-vezérelt** műveletekre
vonatkozik (egyetlen fájl mentése + azonnali build inotify-triggerrel), ahol nincs
"lassú, nagy fa-bejárás", ami elhúzná az időbélyeget. **A projekt kontextusára nézve ez
azt jelenti, hogy a kockázat a művelet méretétől függ**: egyetlen fájl gyors, célzott
újraolvasása (K-01, "újraolvasás kérése egy fájlra") pontosan az a kis, gyors művelet-
típus, amelyre apenwarr figyelmeztetése vonatkozik, míg egy teljes fa bejárás (a napi
konzisztencia-futás) inkább a Git által leírt, magától védett esethez hasonlít.

## 2. Az automatikus törlés az indexből — rutinszerűen biztonságos, vagy alapból veszélyesnek tekintendő?

**Az Atlassian index auto-healing rendszere rutinszerű, automatikus törlést végez az
"index orphan" kategóriára, ütemezett, felügyelet nélküli futásban:**

> „Index orphans: Issues existing only in the index, not in the database" ... „[the process]
> deindexes missing issues and reindexes absent or outdated items" —
> https://confluence.atlassian.com/enterprise/fix-indexing-issues-with-index-auto-healing-1540234564.html

**Az rclone (és általában a szinkronizáló/backup-eszközök kultúrája) az automatikus törlést
alapból veszélyesnek tekinti, és explicit védőkorlátot épít be ellene:**

> „Since this can cause data loss, test first with the --dry-run or the --interactive/i
> flag." és „Files in the destination won't be deleted if there were any errors at any
> point." — https://rclone.org/commands/rclone_sync/

**Mi magyarázza az eltérést (nem valódi, feloldatlan ellentmondás, hanem eltérő
kockázati profil):** az Atlassian-mechanizmus **tételesen**, egyenként, egy megbízható,
élő adatbázis-lekérdezés eredménye alapján dönt arról, hogy egy adott index-bejegyzés
valóban árva-e ("existing only in the index, not in the database") — azaz a "forrás"
(az adatbázis) elérhetősége és válasza minden egyes törlési döntés előtt megerősítést
nyer. Az rclone-féle veszély ezzel szemben abból fakad, hogy a *teljes forrás*
(pl. egy le nem csatolt hálózati meghajtó) tűnhet tévesen üresnek/hibásnak, és emiatt egy
naiv "ami nincs a forrásban, azt töröld a célból" logika **tömegesen**, hibás
előfeltevés alapján törölne mindent. **A tanulság a projektre nézve:** az automatikus
törlés önmagában nem probléma, ha (a) egyedi, megerősített tételekre vonatkozik, és (b)
van egy explicit "ha a bejárás/forrás-elérés hibával tér vissza, ne törölj semmit"
védőkorlát a *tömeges* törlés ellen — a két forrás nem mond ellent egymásnak, hanem együtt
pontosan kirajzolja, hol a határ a biztonságos és a veszélyes automatikus törlés között.

## 3. Van-e valódi, fel nem oldott ellentmondás a mért adatokban?

**Nem találtam** két forrást, amelyek ugyanarra a mért mennyiségre (pl. ugyanarra a
konkrét indexelési sebességre, hash-throughput-ra vagy konzisztencia-futási időre)
egymásnak ellentmondó számot adtak volna. A `megallapitasok.md`-ben szereplő mért adatok
(Recoll sebesség, SQLite komplexitás-osztály, arXiv hash-szám) mindegyike **egyedi forrásból
származik**, nincs velük szemben álló, eltérő számot közlő második mérés — ez nem azt
jelenti, hogy a számok biztosan helytállóak, hanem hogy **nem volt mit összevetni**
(ld. `gaps.md` a hiányzó második mérésekről).


---

## SQ-03 — Ha a beágyazó nem elérhető lekérdezéskor

# SQ-03 — Ellentmondások a forrásokban

## 1. Circuit breaker: ajánlott bevált minta VAGY kerülendő, kockázatos komplexitás?

**A oldal — AWS Well-Architected: a circuit breaker a fail-fast bevált eszköze**

> „The circuit breaker pattern can be utilized here, which monitors failing calls to a
> downstream system. If a high number of calls are failing, it will stop sending more
> requests to the downstream system and only occasionally let calls through to test whether
> the downstream system is available again."
— https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_mitigate_interaction_failure_graceful_degradation.html

Ugyanezt erősíti meg az AWS Prescriptive Guidance saját, dedikált circuit-breaker mintaoldala,
a Netflix Hystrix (a legelterjedtebb nyílt forráskódú implementáció) és az Azure Architecture
Center is — mindannyian a circuit breaker-t sorolják a standard, ajánlott eszközök közé
folyamathatáron túli, hibázó függőségekhez.

**B oldal — AWS Builders' Library (szintén hivatalos AWS-tartalom!): a circuit breaker
kockázatos, komplex, nehezen tesztelhető**

> „widely promoted to solve this problem" [de] „introduce modal behavior into systems that
> can be difficult to test, and can introduce significant addition time to recovery."
— https://d1.awsstatic.com/builderslibrary/pdfs/timeouts-retries-and-backoff-with-jitter.pdf

Ugyanez a dokumentum alternatívát is javasol: „limiting retries locally using a token
bucket" — vagyis nem a downstream-hívást blokkolja globálisan (mint egy klasszikus circuit
breaker), hanem kliens-oldali, helyi token-bucket-tel korlátozza az újrapróbálkozások
számát.

**Ez egy valódi, forrásokkal alátámasztott ellentmondás — és nem külső-belső forrás közötti,
hanem UGYANAZON gyártó (AWS) két különböző hivatalos dokumentuma között.** A Well-Architected
Framework (átfogó, magas szintű architektúra-ajánlások) és a Builders' Library (Amazon belső
mérnöki csapatainak saját, gyakorlati tapasztalatokból származó ajánlásai) nyilvánvalóan nem
egyeztették össze ezen a ponton az álláspontjukat, vagy a Builders' Library egy szándékosan
kontrariánus, tapasztalat-alapú finomítás a Well-Architected általánosabb ajánlásához képest.

**Miért lehet ez így — a forrás saját magyarázata alapján:** a Builders' Library kifejezetten
azt emeli ki, hogy a circuit breaker **állapotgép-jellegű, modális viselkedést** visz be a
rendszerbe („introduce modal behavior... difficult to test"), ami a tesztelést és a
helyreállítási időt nehezíti — ez egy tapasztalati, üzemeltetési érv, nem elméleti. A
Well-Architected-oldal viszont a **tervezési** szempontból (mikor ne folytass hiába
próbálkozást) érvel, és nem tér ki a circuit breaker üzemeltetési komplexitására.

**Relevancia a mi tervünkhöz:** mindkét minta megvalósítható egy külön-folyamatban futó
beágyazó szolgáltatás elé — a döntés végső soron azon múlik, hogy a csapat vállalja-e a
circuit breaker állapotgépének tesztelési/üzemeltetési többletköltségét, vagy inkább egy
egyszerűbb, helyi timeout+retry-korlátozó mechanizmust választ. Egyik forrás sem mondja ki,
hogy univerzálisan melyik a jobb — mindkettő kontextusfüggő ajánlás, nem mérés.

---

## 2. BM25 vs dense/szemantikus — melyik a jobb egyedül? (látszólagos, feloldható ellentmondás)

**A oldal — BM25 veri a dense-t egyedül (BEIR, Corrective-RAG paper, tianpan.co):**

> „Dense retrievers are observed to underperform on datasets with a large domain shift...
> like in BioASQ, or task-shifts like in Touché-2020." — BEIR paper (arXiv/NeurIPS).
> Konkrét szám: ArguAna nDCG@10 — BM25 0,315 vs DPR 0,175.

> „BM25 outperforms dense retrieval (text-embedding-3-large) on all metrics except
> Recall@20" — „From BM25 to Corrective RAG" paper, pénzügyi dokumentumokon (nDCG@10: BM25
> 0,515 vs Dense 0,466).

**B oldal — Dense veri a sparse-t egyedül (StackOverflow-tanulmány):**

> „Dense retrieval achieves Recall@5 = 0.779 and MRR = 0.670" vs „sparse baseline (Recall@5 =
> 0.394, MRR = 0.292)" — https://zenodo.org/records/18807773

**Feloldás — nem valódi ellentmondás, hanem két, jelentősen eltérő feltétel:**

1. **A „sparse baseline" a StackOverflow-tanulmányban TF-IDF, nem teljes BM25.** A TF-IDF
   nem tartalmazza a BM25 dokumentumhossz-normalizálását és a telítési (saturation)
   függvényt, ami gyakorlatban jelentősen gyengébb lexikai alapmódszerré teszi. A BEIR és a
   Corrective-RAG mérések viszont valódi, hangolt BM25-tel mérnek. Ez önmagában
   megmagyarázhatja a nagyságrendi különbséget.
2. **A lekérdezés-típus is eltér.** A StackOverflow Q&A jellemzően **parafrázis-jellegű,
   természetes nyelvi** kérdés-válasz párokból áll (pl. „hogyan tudom X-et csinálni Y
   nyelven"), ahol a szemantikus hasonlóság jól működik. A BEIR domain-shifthez kötött
   feladatai (ArguAna, Climate-FEVER, NFCorpus) és a pénzügyi dokumentumok (Corrective-RAG
   paper) viszont pontos terminológiát, számokat, entitásokat igénylő lekérdezések — pont
   az a fajta lekérdezés, ahol a lexikai egyezés kritikus (ld. `megallapitasok.md` 3.
   pont, tianpan.co konkrét példái: hibakódok, SKU-k).

**Ez tehát megerősíti — nem cáfolja — a fő tanulságot**: a kérdés nem az, hogy „BM25 vagy
dense jobb általában", hanem hogy **melyik lekérdezés-típusnál melyik esik ki drámaian** —
ez pontosan az az árnyalat, amit a kérdés (SQ-03, 3. pont) explicit keresett, és amit egyik
forrás sem mond ki ilyen direktben egymás mellé állítva — ez az én szintézisem a két
adatsorból.

---

## 3. Stale/degradált válasz jelzése — élő gyakorlat vs visszavont szabvány

**A oldal — a gyakorlatban élő és aktívan implementált minta:**

CDN-szolgáltatók (Fastly, KeyCDN) ma is implementálják és dokumentálják a
`stale-if-error`/Warning-fejléc mechanizmust production-környezetben.

**B oldal — a formális szabvány visszavonta a hozzá tartozó jelző-mechanizmust:**

> „The header was deprecated because it is not widely generated or surfaced to users (see
> RFC9111)." — https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Warning

**Feloldás:** nem ellentmondás a gyakorlat és az RFC 5861 `stale-if-error` *funkciója*
között (az továbbra is érvényes, aktív specifikáció) — az ellentmondás abban van, hogy a
funkcióhoz eredetileg társított **jelző-mechanizmus** (Warning fejléc) mára elavult, és a
HTTP-szabványvilág explicit indoka erre az, hogy a fejlécet „nem widely generated or
surfaced to users" — vagyis a valóságban **soha nem terjedt el eléggé ahhoz, hogy megérje
fenntartani a szabványban**. Ez önmagában egy releváns adatpont a SQ-03 4. pontjára: még a
HTTP-világ dedikált „ezt jelezd stale-nek" mechanizmusa is elhalt a gyakorlati elterjedtség
hiánya miatt — ez óvatosságra int azzal a feltételezéssel szemben, hogy egy hasonló, saját
kitalált „X-Degraded" jelző magától elterjedne vagy hasznosulna, ha a hívó oldalak nem
építik be kifejezetten a kezelését.


---

## SQ-04 — Törlésre jelölt bejegyzés az indexben

# SQ-04 — Ellentmondások a forrásokban

## 1. Weaviate tombstone-takarítás: „megoldja" a problémát, vagy csak a gráf-bejárást javítja, a lemezt nem?

**A oldal — Weaviate hivatalos dokumentációja szerint a periodikus takarítás megoldja a
felhalmozódást:**

> „Tombstones are records that mark deleted objects. In an HNSW index, tombstones are
> regularly cleaned up, triggered periodically by the cleanupIntervalSeconds parameter." —
> https://docs.weaviate.io/weaviate/config-refs/indexing/vector-index

Ez azt sugallja, hogy a `cleanupIntervalSeconds` ciklus után a törölt objektum ténylegesen
eltűnik a rendszerből.

**B oldal — a Ghost Vectors kutatás szerint a Weaviate takarítás után is helyben hagyja a
nyers vektort a lemezen:**

> „Weaviate appends deletion metadata without reclaiming HNSW slots." — arXiv 2606.18497v1

> „Soft-deleted HNSW vectors remain physically recoverable by accessing raw index files at
> the storage layer, bypassing API access." — ugyanott

> „a backup snapshot can be used for attack with identical reconstruction quality" —
> ugyanott, ami azt sugallja, hogy a rekonstruálhatóság **hosszú távon, a takarítási ciklus
> lezajlása után is** fennállhat.

**Az ellentmondás feloldása (saját elemzés, nem forrás állítása):** a két állítás nem
feltétlenül zárja ki egymást, mert **különböző rétegről beszélnek**. A Weaviate hivatalos
dokumentációja a **gráf-bejárási/logikai** takarításról szól (a tombstone-jelölésű
csomópont linkjeinek eltávolítása a HNSW-gráfból, hogy a keresés ne akadjon el rajta és ne
lassuljon a felhalmozódástól). A Ghost Vectors paper a **lemez-szintű, byte-pontos**
törlésről beszél (vajon a nyers vektor bájtjai fizikailag felül vannak-e írva, vagy csak a
mutató/index-bejegyzés szűnt meg — hasonlóan ahhoz, ahogy egy fájlrendszerben a
„törölt" fájl tartalma gyakran a lemezen marad, amíg felül nem írják). **A projekt D-21
harmadik állapota („véglegesen törölt — a fájl és minden korábbi változata eltűnik")
szempontjából ez releváns kockázat**: a Weaviate-szerű „tombstone cleanup" dokumentáltan
megoldja a keresési teljesítmény-problémát, de **nincs forrás arra, hogy garantáltan
byte-szinten felülírja a lemezt** — ezt egyik vizsgált vektor-DB hivatalos dokumentációja
sem állítja kifejezetten egyik irányban sem (se azt, hogy felülírja, se azt, hogy nem).

## 2. HNSW logikai törlés hatása a recall-ra: „csak fokozatosan romlik" vagy „drámaian, mérhetően rossz"?

**A oldal — az arXiv 2512.06200 paper szerint a logikai törlés (tombstoning) romlást
okoz, de ez kezelhető, kontrollált mértékű:**

> „search accuracy of logical deletion deteriorates" [ismételt frissítéseknél], és a
> szerzők egy „Deletion Control" stratégiával (időnkénti rebuild beiktatásával) „almost
> satisfies the required search accuracy" — azaz a romlás **kordában tartható**, nem
> katasztrofális, ha megfelelő ütemben rebuildelnek.

**B oldal — az arXiv 2407.07871v2 paper szerint a probléma sokkal súlyosabb, mert
strukturális, nem csak fokozatos pontosság-csökkenés:**

> „the performance of HNSW and most graph-based indices become unacceptable when faced
> with a large number of real-time deletions, insertions, and updates." — arXiv
> 2407.07871v2

> Az „unreachable points" jelenség **nem fokozatos romlás, hanem bizonyos pontok teljes
> elérhetetlenné válása** — „unless the node v serves as the entry point... it will remain
> unvisited in subsequent search operations." — ugyanott

**Az ellentmondás jellege:** ez **nem közvetlen cáfolat**, hanem hangsúlykülönbség — a
2407.07871 paper kifejezetten a **replace/update** műveletre (törlés+újrabeszúrás
kombinációja) fókuszál és ennek szerkezeti mellékhatását (elérhetetlen pontok) írja le,
míg a 2512.06200 paper a **tiszta törlés** (nincs egyidejű beszúrás) hatását méri
recall-számokban, és arra ad ütemezési stratégiát. Mindkettő igaz lehet egyszerre a saját
kontextusában, de **a két paper különböző súlyosságú képet fest** ugyanarról az
alapjelenségről (HNSW logikai törlés), ezért fontos, hogy a projekt ne csak az egyiket
vegye figyelembe: ha a törlésre-jelölt állapot **gyakori insert/update-tel is jár együtt**
(pl. egy fájl újra szerkesztésre kerül visszavonás után), a 2407.07871 által leírt,
súlyosabb strukturális probléma is releváns lehet, nem csak a fokozatos recall-romlás.

## 3. Van-e teljesítmény-előny a soft delete-nek, vagy csak kényelmi/biztonsági kompromisszum?

**A oldal — a Meilisearch hivatalos specifikációja kifejezetten a sebesség érdekében
vezette be a soft delete-et, tehát tisztán előnyként állítja be:**

> „Deleting documents is extremely slow... Making deletion almost instantaneous by not
> deleting the document when asked." — https://specs.meilisearch.dev/specifications/text/0136-documents-soft-deletion.html

**B oldal — a Qdrant és Weaviate dokumentációja szerint a soft delete önmagában
hosszú távon PROBLÉMÁT okoz, amit külön mechanizmussal (Vacuum Optimizer, tombstone
cleanup) kell ellensúlyozni:**

> „over time, these marked records can build up, wasting memory and slowing down the
> system." — https://qdrant.tech/documentation/ops-optimization/optimizer/

**Az ellentmondás feloldása:** nem valódi ellentmondás, hanem **időtávlat-különbség** — a
soft delete rövid távon (a törlés pillanatában) mindig gyorsabb, mint a fizikai törlés,
de hosszú távon (ha nincs takarítás) mindig degradálódáshoz vezet. Minden forrás
egyetért abban, hogy **mindkét hatás egyszerre igaz** — ez azért szerepel itt
ellentmondásként, mert felületesen olvasva úgy tűnhet, mintha az egyik forrás
(Meilisearch) a soft delete-et tisztán jóként, a másik kettő (Qdrant, Weaviate) tisztán
problémaként mutatná be, holott mindhárom rendszer **mindkét mechanizmust együtt
alkalmazza** (gyors jelölés + kötelező, ütemezett takarítás) — tehát a látszólagos
ellentmondás valójában ugyanannak az érem két oldalának eltérő hangsúlyozása.
