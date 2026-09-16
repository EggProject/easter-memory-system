# Ellentmondások — tartalom-kapu



---

# sq01 — Titok- és kulcsfelismerés írás előtt

# sq01 — Ellentmondások és feloldásuk

## 1. "Törölni elég" vs. "törölni és cserélni is kell" — GitHub vs. HashiCorp/NIST-alapú ajánlás

**A látszólagos ellentmondás:** A GitHub két, egymástól független dokumentuma szerint a hitelesítő adat rotálása/visszavonása **önmagában elégséges** lehet, a history-átírás opcionális, "gyakran szükségtelen":

> "this is time-intensive and often unnecessary if you've already revoked the credential" — [T1, docs.github.com, secret-scanning concept oldal]

> "Going through the extra steps to rewrite the history and remove the secret may not be warranted." — [T1, docs.github.com, removing-sensitive-data oldal]

Ezzel szemben a HashiCorp Well-Architected Framework (NIST-hivatkozással) **mindkét lépést** előírja:

> "Leaked secrets in source code require immediate rotation **followed by systematic removal** from version control history. Simply deleting the file or line does not remove the secret." — [T2, developer.hashicorp.com]

**Feloldás:** Nem valódi, tartalmi ellentmondás — mindkét forrás egyetért abban, hogy a **rotálás az elsődleges, azonnali, nem-elhagyható lépés**. A különbség csak a **második lépés (history-purge) kötelező jellegében** van: a GitHub kockázat-alapú, megengedő álláspontot képvisel ("ha már rotáltál, a history-átírás extra munka lehet, ami nem feltétlenül éri meg"), míg a HashiCorp/NIST-alapú megközelítés defense-in-depth elvet követ (mindkét lépést megköveteli, függetlenül a kockázat-becsléstől). A gyakorlati ok valószínűleg az, hogy a GitHub dokumentuma explicit módon felsorolja a history-átírás **költségeit** is (commit-hash-ek megváltozása, megszakadt PR-diffek, elveszett aláírások, együttműködési kényszer más klónok tulajdonosaival) — tehát költség-haszon mérlegelést javasol, nem azt állítja, hogy a history-ban maradt titok ártalmatlan.

**Relevancia a mi rendszerünkre:** Az `easter-memory-system` **fájl-alapú verziózást** használ, nem gitet, tehát a GitHub-érvelés egy kulcseleme (más fejlesztők helyi klónjai, forkjai, amikbe "bele van égve" a régi történet) **nem áll fenn** ugyanúgy — nincsenek elosztott klónok. Ez azt sugallja, hogy a mi kontextusunkban a history-ból/verziótörténetből való törlés **relatíve olcsóbb és megbízhatóbb** lehet, mint egy git-repóban, DE ez nem változtat az alapvető tanulságon: **egyik forrás sem állítja, hogy a puszta törlés (csere nélkül) elegendő volna.** A csere (rotálás) minden forrás szerint kötelező, függetlenül attól, hogy utána törlik-e a régi verziót is.

## 2. Az entrópia-küszöbök közötti eltérés (3.0 / 3.5 / 4.5) — látszólagos ellentmondás, karakterkészlet-függő magyarázattal

**A látszólagos ellentmondás:** Három különböző, konkrét számot találtunk "a bevett Shannon-entrópia küszöbre":
- detect-secrets, Base64 charset: **4.5**
- detect-secrets, Hex charset: **3.0**
- Gitleaks, `generic-api-key` szabály: **3.5**
- TruffleHog, csak nem-ellenőrzött találatokra, ajánlott kezdőérték: **3.0**

**Feloldás:** Ez nem azt jelenti, hogy a fejlesztők nem értenek egyet abban, "mi számít gyanúsnak" — a küszöb **karakterkészlet-függő**, mert a maximális elméleti entrópia karakterkészletenként eltér: egy hexadecimális string (16 lehetséges karakter) elméleti maximuma log2(16) = **4 bit/karakter**, egy Base64-string (64 lehetséges karakter) elméleti maximuma log2(64) = **6 bit/karakter**. Ezért logikus, hogy a Base64-küszöb (4.5) magasabb, mint a Hex-küszöb (3.0) — mindkettő kb. a saját elméleti maximumuk 75%-a körül van. A gitleaks 3.5-ös értéke egy vegyes karakterkészletű ("generic") mintára vonatkozik, saját elméleti maximuma a szabály szerint 5.83 (lásd `megallapitasok.md` 3.2) — ehhez viszonyítva a 3.5 kb. 60%-os arányt jelent, valamivel megengedőbb, mint a detect-secrets Base64-küszöbe. A TruffleHog 3.0-s "kezdőértéke" pedig kifejezetten óvatos, alacsony küszöb, mert **csak kiegészítő szűrő** a nem-ellenőrzött találatokra — nem az elsődleges detekciós mechanizmus (az az élő API-ellenőrzés).

**Következtetés:** Az eltérő számok nem forrásvita jelei, hanem különböző karakterkészletekre és különböző szerepkörre (elsődleges vs. kiegészítő szűrő) kalibrált, egymással konzisztens értékek.

## 3. "GitHub Secret Scanner 75% precizitás — a legjobb eszköz" — értelmezési csapda, nem forrásellentmondás

**A csapda:** Az ESEM 2023 tanulmány szerint a GitHub Secret Scanner a legjobb precizitású eszköz (75%), ami felületesen "a legmegbízhatóbb eszköznek" tűnhet.

**Feloldás — ugyanaz a forrás mondja ki:** A recall ugyanennél az eszköznél mindössze **6%**:

> "Though GitHub Secret Scanner is the top tool based on precision, the recall score is low (6%), indicating the tool misses many secrets." — [T1, ESEM 2023]

Ez nem ellentmondás a forrásban, hanem egy fontos árnyalat, amit a nyers "75%" szám önmagában elfed: a magas precizitás azért érhető el, mert az eszköz **szűk körben, csak jól ismert, szolgáltatóhoz kötött formátumokra** keres (2023-as állapot szerint) — kevesebb találat, arányaiban kevesebb tévedés, de a valódi titkok **94%-át elszalasztja**. Egy szélesebb lefedettségű, de zajosabb eszköz (pl. Gitleaks: 46% precizitás, 88% recall) a gyakorlatban **több valódi titkot fog meg**, cserébe több fals riasztással. **Ez az egyik legfontosabb tanulság a `tartalom-kapu` kampány szempontjából: a puszta precizitás-szám félrevezető lehet lefedettségi (recall) adat nélkül.**

## 4. A GitHub 522 minta (2026) és a "csak 66 partner" (2023-as tanulmányból idézve) — időbeli, nem tartalmi ellentmondás

Nem valódi ellentmondás, csak **időbeli eltérés**: a 66 partneres szám egy 2023-as lektorált tanulmányból származik, a jelenlegi (2026-09-15-i lekérésű) hivatalos GitHub-oldal 522 mintát sorol fel. A két szám nem közvetlenül összevethető (partner-szám vs. minta-szám), és három év alatt mindkettő nőhetett. Ezt a `hianyok.md` 6. pontjában gap-ként rögzítettük, itt csak azért említjük, hogy egyértelmű legyen: ez nem forrásvita, hanem a rendszer idővel bővülő lefedettségének jele.



---

# sq02 — Mit szűrnek a valódi agent-memória rendszerek íráskor

# sq02 — Ellentmondások és feloldásuk

## 1. A basic-memory "It is NOT a security boundary" idézete — feltételezett vs. igazolt

**Az ellentmondás:** a kutatási feladat kiindulópontként állítja, hogy a basic-memory kimondja magáról: *"It is NOT a security boundary."* A közvetlen forráskutatás (README.md, SECURITY.md, docs.basicmemory.com technikai-információ oldal — mindhárom nyersen lekérve és átvizsgálva) **nem találta meg ezt a pontos szöveget** egyik hivatalos helyen sem.

**Feloldás:** a basic-memory SECURITY.md-je **tartalmilag ugyanazt állítja**, csak más megfogalmazásban és szűkebb keretben:
- "Basic Memory is designed for single-user local knowledge bases and does not implement access controls between operating-system users."
- "Basic Memory does not execute note content as code. Notes are returned as data to the LLM."

Ez funkcionálisan egyenértékű azzal, hogy "a tár nem biztonsági határ" — de a SECURITY.md kifejezetten a *fájlrendszer-/OS-szintű* hozzáférésre korlátozza ezt az állítást, nem a *tartalom* hitelesítésére vagy szűrésére. Két plauzibilis magyarázat marad nyitva (lásd `hianyok.md` B/1): vagy a feladatleírás egy korábbi/eltérő dokumentáció-verzióra, vagy egy nem indexelt forrásra (pl. Discord, README egy régebbi commitja) hivatkozik, vagy a feladatleírás általánosított/parafrazált egy hasonló, de nem szó szerinti állítást. **A gyakorlati következtetés ugyanaz marad**: basic-memory-ban nincs tartalom-szintű kapu, és a projekt saját dokumentációja szerint sem vállal ilyet — csak a pontos idézet forrását nem sikerült azonosítani.

## 2. "Memória-mérgezés gyakori/sikeres" (80-99%) vs. "nincs valós, in-the-wild incidens dokumentálva"

**Az ellentmondás látszata:** a 2. kérdésre kapott akadémiai adatok szerint a memória-mérgezés kísérleti környezetben rendkívül magas sikerességi arányú (MINJA: ">95%/70%", AgentPoison: ">80%"), miközben a 3. kérdésre talált konkrét esetek (Gemini, Amazon Bedrock PoC) mindegyike **kutatói/gyártói proof-of-concept**, nem megerősített, valós áldozattal járó incidens (az OECD.AI kifejezetten "AI Hazard"-nak, nem "aktív incidens"-nek minősítette a Gemini-esetet; a Unit 42 saját maga nevezi PoC-nak a Bedrock-esetet).

**Feloldás — ez nem valódi ellentmondás, hanem két különböző mérési szint:**
- A magas százalékok **kontrollált, laboratóriumi red-teaming kísérletekből** származnak (a kutatók maguk hozzák létre a támadó promptot és mérik a sikerarányt egy adott modellen/ágensen).
- A "valós incidens" kérdés arra vonatkozik, hogy **dokumentált-e olyan eset, ahol egy tényleges, nem-kutatói támadó, nem-teszt környezetben, ismeretlen áldozat kárára** hajtotta végre a támadást.
- Az egyetlen eset, ami ehhez a legközelebb áll, a **Cisco MemoryTrap** (Claude Code) — de ez is **Cisco kutatói által, kontrollált PoC-ként** végrehajtott demonstráció volt, amit felelősségteljesen jelentettek be, mielőtt bárki más kihasználhatta volna.
- **Következtetés:** a magas laboratóriumi sikerességi arányok és a kifejezetten "in-the-wild" (valódi támadó által, termelési környezetben kihasznált) esetek hiánya **egyszerre igaz** — a technika bizonyítottan működik, de a nyilvánosan dokumentált esetek mind felelős közzététel (responsible disclosure) keretében, kutatók által lettek demonstrálva, nem elkapott valós támadásként. Ez önmagában fontos megállapítás, nem ellentmondás.

## 3. Két különböző "motiváló példa" ugyanahhoz az OWASP ASI06 tételhez

**A látszólagos ellentmondás:** az OWASP hivatalos, 2025.12.09-i bejelentő blogja a **Gemini Memory Attack**-ot nevezi meg ASI06 példájaként, míg az OWASP hivatalos, 2026.05.13-i, az ASI06-tétel feleőse (Idan Habler) által írt blogja a **Cisco MemoryTrap (Claude Code)** esetet állítja a középpontba, meg sem említve a Gemini-esetet.

**Feloldás:** nincs valódi ellentmondás — a két blogbejegyzés más időpontban íródott (a MemoryTrap-kutatást 2026 áprilisában tette közzé a Cisco, tehát az később keletkezett, mint a 2025 decemberi bejelentés). A szerző egyszerűen egy frissebb, saját maga által vezetett kutatást emelt ki motiváló példaként a második blogposztban. A két eset **egymást kiegészíti**, nem mond ellent egymásnak — mindkettő ugyanazt az ASI06-mintázatot illusztrálja, csak más terméken (Gemini vs. Claude Code) és más kutatói csapattól (Rehberger/Embrace The Red vs. Cisco AI Security Research).

## 4. "A vizsgált rendszerek nem gátolják a rossz tartalmat" vs. "az OWASP Agent Memory Guard 92,5%-ban felismeri, 100%-ban precíz"

**A látszólagos ellentmondás:** a jelentés fő megállapítása szerint egyik natív memória-rendszer sem old meg determinisztikus tartalom-szűrést, ugyanakkor bemutatunk egy konkrét eszközt (OWASP Agent Memory Guard), ami állítólag 92,5%-os detekciós rátával, 100%-os precizitással működik.

**Feloldás:** nincs ellentmondás, mert az Agent Memory Guard **kifejezetten nem a vizsgált memória-rendszerek (mem0, Letta stb.) saját, beépített funkciója**, hanem egy különálló, rájuk kívülről rátehető köztes réteg (middleware) — a README saját integrációs példái (LangChain, mem0, AutoGen, CrewAI) éppen azt bizonyítják, hogy ezek a rendszerek **maguktól nem tartalmazzák** ezt a védelmet, ezért kell külön csomagként hozzáadni. A 92,5%/100% szám is **egy kis, saját összeállítású, 55 elemes benchmarkra** vonatkozik (nem független, nagy léptékű validáció), és még ezen a kedvező benchmarkon is 17-20%-os hiányosságot mutat két kategóriában (érzékeny adat szivárgás, méret-anomália) — tehát még ez a legjobb talált példa sem tökéletes, csak a legjobb rendelkezésre álló, kifejezetten erre épített, determinisztikus megoldás.

## 5. Unit 42 két cikke — "csak elméleti" vs. "már nem elméleti, hanem a vadonban megfigyelt"

**A látszólagos ellentmondás:** a Unit 42 2025 októberi cikke (Bedrock Memory PoC) kifejezetten laboratóriumi demonstrációként mutatja be magát, míg a 2026 márciusi cikke azt állítja: "our analysis of large-scale real-world telemetry shows that IDPI is no longer merely theoretical but is being actively weaponized."

**Feloldás:** nincs ellentmondás, mert **a két cikk más támadási osztályról szól**. A 2026 márciusi cikk (amit ellenőriztünk: 0 "memory" előfordulás a szövegben) az **általános, web-alapú indirekt prompt injectionről** szól (reklám-átverés, SEO-manipuláció, adatpusztítás stb.), **nem kifejezetten a memória-mérgezésről**. A memória-specifikus alkategória (amit a 2025 októberi cikk mutat be) továbbra is csak PoC-szinten dokumentált a talált forrásokban; az "already weaponized in the wild" állítás a tágabb IDPI-kategóriára vonatkozik, nem szűkíthető le memória-mérgezésre anélkül, hogy ezt a forrás maga állítaná — amit nem tesz.
