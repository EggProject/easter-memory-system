# Ellentmondások — korai-korok-ujra



---

# sq01 — A fa mint jogosultsági modell, és a kategóriák

# Ellentmondások — ahol a források nem egyeznek, és a feloldás (sq01 újramérés)

## 1. A korábbi (2026-08-23-i) kör forrás nélküli kategóriaszám/F1-állítása vs. e kör mérései

**Ez a legfontosabb tétel ebben a fájlban**, mert ez volt az újramérés kiváltó oka.

A feladatmegbízás szerint a 2026-08-23-i körben szerepelt egy kategóriaszám és egy
F1-érték, amit forrás nélkül vettek fel, és két héttel ezelőtt derült ki, hogy "a
tényleges mérés éppen az ellenkezőjét mondta" — ezért ki kellett venni a
specifikációból. **Ennek a kutatási körnek nem állt rendelkezésére a korábbi,
eltávolított állítás pontos szövege vagy száma** (ez nem volt elérhető forrás
ebben a munkamenetben), ezért nem tudunk sor-szintű összehasonlítást végezni
"a régi szám X volt, az új Y" formában. Ami helyette elmondható, és amit ez a
kör ténylegesen, forrással alátámasztva megállapított:

- Egy lektorált (T2, Scientific Reports/Nature Portfolio) mérés kis, on-device
  LLM-eken (BERT/RoBERTa/ALBERT/XLNet család) **egyértelmű, monoton romlást**
  mért a kategóriák számának növekedésével: 3 kategóriás feladatnál 83-84%
  balanced accuracy, 13 kategóriás feladatnál a legjobb modell is csak 62.8%-ot
  ért el (forrás: `allitasok.csv` SQ-05-C003).
- Egy nem lektorált (T4, arXiv) mérés nagy/frontier LLM-eken (Llama-3.1-70B,
  Gemma-2-27B, Qwen2.5-72B, Claude-3.5-Sonnet) szintén azt találta, hogy a
  kategóriatér (címketér) **csökkentése** minden modellnél átlagosan javította
  a macro-F1-et (3.3%-tól 7.0%-ig modellenként), azaz a **nagyobb kategóriatér
  rontja** a pontosságot (SQ-05-C004, SQ-05-C005).
- Mindkét, egymástól teljesen független forrás (eltérő módszertan, eltérő
  modellméret-tartomány, eltérő feladat) **ugyanabba az irányba mutat**: több
  kategória → rosszabb besorolási pontosság/F1. Ha a 2026-08-23-i, eltávolított
  állítás ezzel ellentétes irányt sugallt (pl. hogy a kategóriaszám növelése
  nem rontja, vagy javítja a pontosságot), akkor **ez az újramérés megerősíti,
  hogy a korábbi állítás valószínűleg téves volt**, összhangban azzal, amit a
  megbízó már két héttel ezelőtt, más úton megállapított. Ezt a feloldást csak
  óvatos, feltételes formában lehet kimondani, mert a korábbi állítás pontos
  tartalma nem áll rendelkezésre ennek az ügynöknek — ez explicit módszertani
  korlátozás, nem lezárt cáfolat.
- **Fontos árnyalat, amit a korábbi kör feltehetően nem vett figyelembe**:
  mindkét forrás azt is méri, hogy a hatás **nem egyenletes modellméret
  szerint**. A nagy/képes modellek (Qwen2.5-72B, Claude-3.5-Sonnet) sokkal
  kevésbé érzékenyek a nagy kategóriaterekre (3.3-4.9% javulás
  szűkítéskor), mint a kisebb/kevésbé képes modellek (Llama-3.1-70B: 7.0%
  javulás, illetve a kis, on-device modellek drasztikus romlása 13
  kategóriánál). **Ha a specifikáció egyetlen, modellmérettől független
  "ideális kategóriaszámot" akart rögzíteni, az a mérési adatok szerint
  fogalmilag hibás volt** — a helyes kategóriaszám modellfüggő. Lásd
  `megallapitasok.md` SQ-05 szakasza.

## 2. Kategóriaszámra vonatkozó "ideális szám" — a valódi rendszerek egymásnak ellentmondanak

A négy vizsgált, valós gyakorlatban használt rendszer **nem egyeztethető össze
egyetlen közös számban**:

| Rendszer | Előírt kategóriaszám | Forrás tier |
|---|---|---|
| PARA (Tiago Forte) | pontosan 4 | T1 (elsődleges) |
| Johnny.Decimal | legfeljebb 10 terület × legfeljebb 10 kategória (=legfeljebb 100) | T1 (elsődleges) |
| Zettelkasten Method | 0 — szándékosan nincs előre definiált kategória | T2 |
| mem0 (agent-memória rendszer) | 15 alapértelmezett (felülírható) | T1 (elsődleges) |

**Feloldás: ez nem valódi ellentmondás, hanem eltérő tervezési filozófiák
egymás mellett élése**, amit a kategóriák eltérő rendeltetése magyaráz: a PARA
és Johnny.Decimal *emberi* keresési/döntési terhelést optimalizál (kevés,
fejben tartható kategória), a Zettelkasten kifejezetten *elutasítja* az
előre rögzített struktúrát, mert az szerinte gátolja a szerves asszociációt,
a mem0 pedig egy *gépi* (embedding/LLM-alapú) címkézési rendszer, ahol a
15-ös szám gyakorlati tapasztalati kompromisszum, nem elméleti optimum.
**Egyetlen forrás sem állítja, hogy létezne egy tudományosan levezetett,
univerzálisan helyes kategóriaszám** — ezt a hiányt a `hianyok.md` is rögzíti.
Ez önmagában releváns megállapítás az `easter-memory-system` öt kategóriájára
nézve: az öt (decisions/mistakes/procedures/facts/preferences) szám a Johnny.Decimal
"legfeljebb 10" elvének megfelel, a PARA "pontosan 4" elvét enyhén meghaladja,
és nincs olyan talált forrás, ami ezt vagy cáfolná, vagy megerősítené — mert
egyik vizsgált rendszer sem *fajta szerinti* (episztemikus típus), hanem mind
*téma szerinti* kategorizálást ír le.

## 3. Namespace/prefix mint "csak szervezés" (SQ-01) vs. namespace mint "valódi izoláció" (SQ-02) — látszólagos, de feloldott ellentmondás

Első ránézésre ellentmondásnak tűnhet, hogy az SQ-01 forrásai (Anthropic memory
tool, Claude Code, Obsidian) azt hangsúlyozzák, hogy az útvonal/prefix
**önmagában nem biztonsági határ**, míg az SQ-02 forrásai (Kubernetes, Vault,
S3) olyan rendszereket mutatnak be, ahol névtér/prefix **ténylegesen működő
izolációt** ad.

**Feloldás: nincs valódi ellentmondás, a két megállapítás ugyanazt az elvet
támasztja alá két oldalról.** A Kubernetes saját hivatalos dokumentációja
kimondja, hogy "a control plane legfontosabb izolációs típusa az
authorization" (RBAC), és az objektumnevek névtereken átívelő átfedése
"hasonló a mappákban lévő fájlokhoz" — azaz maga a névtér itt is csak
*szervezési* eszköz, a *kikényszerítést* egy külön, aktívan érvényesített
szabályzat-motor (RBAC, IAM policy, Vault namespace-API) végzi. Az S3-nál ez
even explicitebb: "Amazon S3-nak nincs fizikai könyvtárhierarchiája", a
"mappa" csak kulcs-prefixből következtetett fogalom, és a tényleges
korlátozást az IAM `s3:prefix` feltétel + explicit Deny adja. Vagyis: **minden
vizsgált rendszerben — akár állítja magáról biztonsági határnak a névteret/
útvonalat, akár nem — a tényleges izolációt egy, a fastruktúrától elkülönült,
aktívan kikényszerített szabályzat-réteg adja, nem maga a fa.** Ez a kör
legmagasabb megbízhatóságú ("Magas"), 10 forrásból (7× SQ-01 + 3× SQ-02, két
teljesen különböző terület: agent-memória eszközök és általános
infrastruktúra) konvergáló megállapítása — lásd `megallapitasok.md`.

## 4. Azonosító-elnevezés emberi (Lawrie 2007) vs. LLM (When Names Disappear 2025) hatása — nem ellentmondás, hanem eltérő alany

A Lawrie et al. (2007) humán kísérlet szerint a **teljes szavas és a
rövidített** azonosítók között *nincs* szignifikáns különbség a leírási
pontosságban (csak az egybetűs azonosítókhoz képest van mindkettő
szignifikánsan jobb). Ezzel szemben a "When Names Disappear" (2025) LLM-mérés
szerint **már a névelhomályosítás (obfuscation) bármely formája** — ami
tipikusan nem egybetűsre, hanem more szisztematikus, de még "ésszerű" alakra
cseréli a neveket — jelentős (10-30+ pontos) teljesítményromlást okoz LLM-eknél.

**Feloldás: ez nem közvetlen ellentmondás, mert más az alany (ember vs. LLM) és
más a manipuláció mértéke/módja** (rövidítés vs. szemantikai elhomályosítás/
alpha-renaming). A két mérés együtt olvasva viszont figyelemre méltó
aszimmetriát jelez: az emberi megértés viszonylag robusztus az *ésszerű*
rövidítésre, míg az LLM-ek — legalábbis a vizsgált feladatokon (kódösszefoglalás,
kódvégrehajtás) — sokkal érzékenyebbnek tűnnek bármilyen névperturbációra. Ez
óvatosságra int azzal a feltevéssel szemben, hogy "amit egy embernek elég
informatívnak találunk, az egy LLM-ügynöknek is elég lesz" — de mivel egyik
forrás sem vizsgált kifejezetten *mappaneveket*, ez csak analógiás következtetés,
nem közvetlenül mért tény (ld. `hianyok.md` SQ-06 szakasza).

## 5. Tier-különbség a SQ-05 és SQ-06 legfontosabb számai mögött

Az SQ-05 két fő forrása közül csak az egyik (Scientific Reports, T2) lektorált;
a nagy modellekre vonatkozó számok (arXiv Haystack-to-Needle, T4) nem
lektoráltak. Hasonlóképpen az SQ-06-nál a klasszikus Lawrie-tanulmány
lektorált (T2), a "When Names Disappear" nem (T4). **Ez nem ellentmondás a
két pár forrás között** (az irányuk megegyezik/kiegészíti egymást), de fontos
a bizalmi szint helyes beállításához: az `allitasok.csv`-ben minden T4-forrású
állítás "Alacsony" megbízhatósági jelölést kapott, függetlenül attól, hogy
alátámasztja-e a T2-forrású mérést vagy sem — a lektoráltság hiánya önmagában
csökkenti a megbízhatóságot, akkor is, ha a végkövetkeztetés stabilnak tűnik.



---

# sq02 — A markdown fájl mint memória-egység, és a fejléc

# Ellentmondások — sq02

## E1. "A Norway-hiba a YAML 1.2 specifikáció szerint szándékos" — ELLENTMOND az elsődleges forrásnak

**Az állítás, ahogy egy másodlagos forrás megfogalmazza:**

> "The most tragic aspect of this bug, however, is that it is intended behavior according to the YAML 1.2 specification."
> — HitchDev / StrictYAML, https://hitchdev.com/strictyaml/why/implicit-typing-removed/ (T3, blog, a StrictYAML szerzőjének véleménycikke)

**Amit az elsődleges forrás (a YAML 1.2.2 specifikáció szövege) ténylegesen mond:**

> "true | True | TRUE | false | False | FALSE tag:yaml.org,2002:bool"
> (a Core Schema Tag Resolution táblázatából, 10.3.2. szakasz)
> — https://yaml.org/spec/1.2.2/ (T1)

és:

> "The Core schema is an extension of the JSON schema, allowing for more human-readable presentation of the same types. This is the recommended default schema that YAML processor should use unless instructed otherwise."
> — ugyanott (T1)

**A feloldás:** A YAML 1.2.2 spec Core Schema-ja — amely a specifikáció saját szövege szerint az *ajánlott alapértelmezett séma* — kifejezetten **kizárja** a `yes`/`no`/`on`/`off`/`y`/`n` alakokat a logikai típus feloldásából, csak a `true`/`True`/`TRUE`/`false`/`False`/`FALSE` alakokat ismeri el. Ez pontosan az ellenkezője annak, amit a HitchDev-bejegyzés állít. A blogbejegyzés állítása feltehetően két dolgot kever össze:

1. A YAML 1.1 Type Repository (`yaml.org/type/bool.html`) *valóban* tartalmazza a `no`/`yes`/`on`/`off` alakokat — de ez az **1.1-es**, nem az 1.2-es dokumentum.
2. A gyakorlatban sok, magát "YAML 1.2-kompatibilisnek" hirdető parser (pl. PyYAML, SnakeYAML — lásd A34–A37 az `allitasok.csv`-ben) a mai napig az 1.1-es stílusú, tág boolean-regexet használja alapértelmezésként, függetlenül attól, hogy a spec szövege mit mond. Így a **gyakorlati tapasztalat** (a bug ténylegesen előfordul a legelterjedtebb parsereknél) valós, csak az **okát** írja le pontatlanul a blogbejegyzés, amikor a specifikációra hárítja a felelősséget.

**Következtetés a kutatáshoz:** Ha az `easter-memory-system` specifikációja bármikor azt állítaná, hogy "a YAML 1.2 spec szerint a Norway-probléma szándékos/elfogadott viselkedés", az pontatlan lenne. A pontos állítás: *a Norway-probléma a YAML 1.2 Core Schema szintjén meg van oldva, de a gyakorlatban használt legnépszerűbb parserek egy része (PyYAML, SnakeYAML) nem ezt a sémát követi alapértelmezésben, hanem az 1.1-es viselkedést, így a hiba ott továbbra is előfordul.*

---

## E2. "Nincs olyan valódi rendszer, amely markdown fájlban tárol tény-szintű egységet" — ehhez képest a basic-memory árnyalja a képet

A feladatleírás kifejezetten kiemeli ezt kulcskérdésként, feltételezve (bár nem állítva biztosan), hogy a korábbi kör esetleg úgy zárult, hogy "nincs ilyen rendszer" vagy hogy a markdown-fájl-mint-tárolóegység ötlete elszigetelt/szokatlan. **Ez a kutatási kör azt találta, hogy létezik legalább egy éles, karbantartott, nyílt forráskódú rendszer (basic-memory), amely architektúrája nagyon hasonlít az `easter-memory-system` alapfeltevéséhez**, ugyanakkor nem azonos vele:

- basic-memory: a markdown **fájl** az elsődleges tároló ("file-first architecture... database serves as a secondary index" — T1), DE a fájlon belüli "Observations" (tény-szintű egységek) saját permalinkkel, önálló indexbejegyzésként élnek egy SQLite-alapú másodlagos indexben (teljes szöveges + vektoros kereséssel).
- Ez **nem** azonos azzal, hogy "a fájl a tárolás egysége, a fájlon belüli tények az indexelés egységei" (az `easter-memory-system` megfogalmazása) — a basic-memore-ban a tény-szintű egységek **is** perzisztálnak egy adatbázisban (bár az az adatbázis újraépíthető a fájlokból, tehát "másodlagos" / nem az igazság elsődleges forrása).

**Nincs éles ellentmondás**, csak fontos árnyalat: a valós, legközelebbi analóg rendszer (basic-memory) NEM tisztán fájl-only, hanem fájl-elsődleges + adatbázis-index hibrid, ahol a tény-szintű granularitás magában az adatbázisban jelenik meg, nem kizárólag a markdown fájl parse-olásával minden lekérdezéskor. Ha az `easter-memory-system` tervez bármilyen tény-szintű indexet (akár csak egy SQLite táblát), az a basic-memory mintázatával konzisztens; ha viszont kizárólag a nyers fájlok soronkénti/blokkonkénti parse-olására támaszkodna futásidőben adatbázis nélkül, az **nincs** ismert, éles analógja a vizsgált rendszerek között.

---

## E3. A Zep saját mérési számai (94.8% vs 93.4%, +18.5%, -90% latencia) — gyártói önértékelés, nem független validáció

Ez technikailag nem "ellentmondás" két forrás között, hanem egy **megbízhatósági figyelmeztetés**: a `arxiv.org/abs/2501.13956` cikk szerzői a Zep saját munkatársai, a benchmarkot (Deep Memory Retrieval, LongMemEval) saját maguk futtatták a saját termékükön. Nem találtunk független, harmadik féltől származó megerősítést ezekre a konkrét számokra. Ezt a CSV-ben és a megállapításokban "Alacsony" megbízhatósággal, T4-es tierrel jelöltük, és nem tekintjük semleges bizonyítéknak — csak azt dokumentáljuk, hogy *a gyártó ezt állítja magáról*.

---

## E4. Jekyll "title" mező hivatalossága — belső ellentmondás magán a Jekyll dokumentáción belül

A Jekyll hivatalos `front-matter.md` referenciaoldala a bevezető példában `title: Blogging Like a Hacker`-t használ, ami azt sugallja, hogy a `title` egy alapvető, elvárt mező — ugyanakkor a lejjebb található "Predefined Global Variables" és "Predefined Variables for Posts" táblázatokban a `title` **nincs** felsorolva (csak `layout`, `permalink`, `published`, `date`, `category`/`categories`, `tags`). Ez nem két külső forrás közötti ellentmondás, hanem a hivatalos dokumentum belső following pontatlansága/hiánya. A feloldás: a `title` a gyakorlatban univerzálisan használt konvenció (szinte minden Jekyll-téma `page.title`-t vár), de a Jekyll motor magja formálisan nem "foglalja le" ezt a nevet — bármilyen egyéni (custom) változóként működik, amit a témák konvencionálisan title-ként kezelnek. Ezt "Közepes" megbízhatósággal jelöltük az `allitasok.csv`-ben (A59), pontosan emiatt az árnyalat miatt.



---

# sq03 — Beágyazás magyarra/többnyelvűre, és az integrációs felületek

# Ellentmondások és feloldásuk — sq03

## 1. [FŐ ELLENTMONDÁS] Claude Code hook-kimeneti méretkorlát: a 2026-09-01-i ellenőrzés "megdöntötte", a mai (2026-09-15) élő dokumentáció visszaigazolja

**Az ellentmondó állítások:**

- **A kampány jelenleg érvényes döntése (D-15/5, `00-dontesek.html`)** és a rá hivatkozó mérési dokumentum (`90-meresek.html`, 07. szakasz, "Az ellenőrzés — mi dőlt meg") kimondja:
  > „Kikerült: a 10 000 karakteres hook-limit. Egy korábbi kutatás azt hozta, hogy a Claude Code session-indulási hookja 10 000 karaktert fogad. **Ez nem dokumentált.** Négy hivatalos oldal átkeresve — a hook-referencia, az útmutató, az SDK-oldal és a hibakeresés —, egyikben sincs karakter- vagy tokenlimit. A szám csak hibajegyekben szerepel, felhasználói állításként."
  > „A többi vizsgált kliensnél (Claude Code, Gemini CLI, Cursor) **nincs dokumentált limit**."
  Ez a 2026-09-01-i adverzariális ellenőrzésen alapul, és a jelenlegi specifikáció ez alapján NEM hivatkozik a 10 000-es számra Claude Code esetén.

- **A mai (2026-09-15-i) saját kutatásunk** a hivatalos `https://code.claude.com/docs/en/hooks` oldal nyers letöltésével **explicit, kétszer megismételt** 10 000 karakteres korlátot talált:
  > „Hook output strings, including `additionalContext`, `systemMessage`, and plain stdout, are capped at 10,000 characters."
  > „If a value exceeds 10,000 characters, Claude Code writes the text to a file in the session directory and passes Claude the file path with a short preview instead."

**Feloldás:** ez **nem** azt jelenti, hogy a 2026-09-01-i ellenőrzés hibázott — abban a pillanatban, amikor ellenőriztek, valóban nem volt dokumentálva (ez plauzibilis: Anthropic gyakran utólag egészíti ki a dokumentációt egy korábban csak a viselkedésben létező szabállyal). **A legvalószínűbb magyarázat: a hivatalos dokumentáció 2026-09-01 és 2026-09-15 között frissült**, és pontosan azt a számot rögzítette hivatalosan, ami korábban csak egy GitHub-hibajegyben (felhasználói megfigyelésként) szerepelt.

**Amit NEM sikerült megállapítani:** a pontos dátumot, amikor ez a dokumentáció-változás megtörtént. Megpróbáltuk ellenőrizni a Wayback Machine-en (`web.archive.org`) keresztül, de minden kísérlet (CDX API, `available` API, `WebFetch`) meghiúsult ebben a környezetben (kapcsolat-megszakadás, illetve `SITE_BLOCKED` hiba). Ezt dokumentáljuk hiányként is (`hianyok.md`).

**Javasolt döntés a kampány számára:** a **D-15/5-öt frissíteni kell** — a Claude Code oszlopban a "nincs dokumentált limit" helyett most már **"10 000 karakter (dokumentálva 2026-09-15-től, korábban, legalább 2026-09-01-ig nem volt dokumentálva)"** kell szerepeljen, a `90-meresek.html` 07. szakaszába pedig egy új bejegyzés kívánkozik, ami rögzíti, hogy **a korábban megdöntött állítás időközben ismét igazzá vált** — ez önmagában tanulságos a kampány számára: egy "megdöntött" külső állítás nem feltétlenül marad megdöntve, mert a valóság (itt: mások dokumentációja) változhat.

**Mellékszál, amit érdemes megkülönböztetni:** a GitHub-hibajegy (#44086, Claude Code v2.1.92, WebFetch-összefoglalón keresztül idézve) szerint a gyakorlatban a modellhez érkező **előnézet** csak 2000 karakter (2KB), még akkor is, ha a teljes szöveg elfér a dokumentált 10 000-es korlát alatt fájlba mentve. Ez **valószínűleg nem ellentmond** a mai hivatalos szövegnek — a dokumentáció maga is mondja, hogy a limit fölötti tartalom "egy előnézettel és fájlúttal" kerül helyettesítésre, ami implikálja, hogy MAGA a limit alatti tartalom is csak akkor jut el változatlanul, ha ELFÉR a 10 000 karakterben; efölött csak egy rövidebb előnézet látszik. A hibajegy bejelentője feltehetően azt várta, hogy a teljes 10 000 karakter mindig eljusson a modellhez, ami téves elvárás volt. Ezt a részletet **nem sikerült nyers forrásból megerősíteni** (csak WebFetch-összefoglalóból), ezért alacsonyabb megbízhatósággal kezelendő.

---

## 2. MMTEB "12 taszk" (2025-ös cikk) vs. "28 taszk" (élő 2026-09-15-i adatbázis) — nem valódi ellentmondás, hanem időbeli növekedés

Az MMTEB tudományos cikk (arXiv 2502.13595, ICLR 2025) D. függelékének 8. táblázata szerint a magyar nyelv összesen **12** taszkon szerepelt a cikk megjelenésekor (2025 eleje). Ezzel szemben a kampány saját mérési dokumentuma és a mi mai, nyers adatbázison futtatott lekérdezésünk is **28**-at mutat.

**Feloldás: nincs valódi ellentmondás.** Az MMTEB egy **élő, folyamatosan bővülő** benchmark (ezt a kampány saját dokumentuma is jelzi: "élő, folyamatosan bővülő rangsor"). A tudományos cikk egy **statikus pillanatkép** volt kb. másfél évvel ezelőttről; azóta új taszktípusok kerültek be (elsősorban vizuális dokumentum-visszakeresés és hang-visszakeresés — `JinaVDR*`, `CommonVoice*`, `Fleurs*` sorozatok), amik a magyar nyelvre is kiterjednek. A "28" a jelenleg érvényes, helyes szám; a "12" történelmi érdekesség, és jó példa arra, hogy **minden benchmark-számhoz kötelező a lekérdezés dátuma** (ahogy a feladat is előírja) — enélkül egy régi és egy új szám összemosható lenne tévesen ellentmondásként.

---

## 3. sqlite-vec "32×" térmegtakarítás vs. Qdrant "~7×" — más mérési szint, nem ellentmondás

A sqlite-vec dokumentáció bináris kvantálásra 32×-es térmegtakarítást ír (float32 → 1 bit, nyers vektorbájtok szintjén). A Qdrant hivatalos benchmarkja ezzel szemben csak kb. 7×-es RAM-csökkenést mér egy teljes, működő index szintjén (900 MB → 128 MB, 100 ezer OpenAI-vektornál).

**Feloldás:** a két szám **különböző dolgot mér**. A sqlite-vec állítása a **nyers vektor bájtjaira** vonatkozik önmagában (elméleti, tiszta tárolási arány). A Qdrant mérése egy **teljes, produkciós index** memória-lábnyomát méri, ahol az eredeti (nem kvantált) vektorokat is meg kell őrizni valahol a re-scoring (újra-pontozás) lépéshez, és a HNSW-gráf overheadje is beleszámít. Ez nem ellentmondás, hanem két **eltérő, egyaránt érvényes** mérési feltétel — mindkettőt feltétellel közöltük a `megallapitasok.md`-ben és az `allitasok.csv`-ben.

---

## 4. Amit ellenőriztünk és NEM találtunk ellentmondást — a kampány D-15/D-16 döntéseinek egyéb részei stabilak

A `90-meresek.html` 07. szakaszában felsorolt egyéb, 2026-09-01-én megdöntött vagy megerősített állítások közül (pl. "minden kliens mohón kapcsolódik" — megdőlt Claude Code-ra; "senki nem lát fölfelé" — megdőlt a GitLab-kivétel miatt; "a szerver megszünteti a korrupciós kockázatot" — túl erős volt) egyiket sem vizsgáltuk újra ebben a körben, mert nem tartoztak az sq03 hatókörébe (ezek Spec 30/D-16 más részei, nem az embedding/vektorkeresés/integrációs felület témakör). Ezt tudatosan hagytuk ki — nem azért, mert megbízhatónak ítéltük őket ellenőrzés nélkül, hanem mert kívül estek a jelen feladat kérdésein.
