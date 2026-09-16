# Hiányok — tartalom-kapu



---

# sq01 — Titok- és kulcsfelismerés írás előtt

# sq01 — Hiányok (amit nem sikerült megtudni)

Minden tétel jelöli, hogy **"nincs ilyen"** (feltehetően nem létezik publikált anyag erre) vagy **"nem találtuk meg"** (létezhet, de a rendelkezésre álló idő/eszközök alatt nem került elő).

## 1. Magyar nyelvű szöveg és magyar azonosítók entrópia-viselkedése secret-scanning kontextusban

**Nincs ilyen** (nagy valószínűséggel) — az összes talált eszközdokumentáció, forráskód-kommentár és a lektorált ESEM 2023 tanulmány kizárólag angol nyelvű szöveggel és angol/ASCII-alapú kódmintákkal illusztrál. Nem találtunk sem lektorált, sem gyártói publikációt, amely kifejezetten:
- magyar (vagy bármilyen nem-angol, ékezetes) nyelvű szöveg karakterenkénti/bájtonkénti Shannon-entrópiáját mérné a secret-scanning eszközök küszöbértékeihez viszonyítva,
- vagy azt vizsgálná, hogy a UTF-8 többbájtos kódolású ékezetes karakterek (á, é, í, ó, ö, ő, ú, ü, ű) hogyan torzítják a bájt-szintű entrópiaszámítást a tisztán karakter-szintű számításhoz képest.

Pótlásképp közöltünk egy **saját, illusztratív számítást** (`megallapitasok.md` 3.4. pont), amely nem publikált forrás, csak irányjelző: egyetlen mintamondaton mérve a magyar szöveg entrópiája a valódi véletlen kulcsokéhoz hasonló tartományba (4.0–4.5 bit/karakter) esett. Ez **nem helyettesíti a hiányzó korpusz-alapú mérést**.

## 2. GitHub push protection független (nem gyártói), lektorált fals pozitív/negatív mérése

**Nem találtuk meg** — az egyetlen lektorált mérés (ESEM 2023, Basak et al.) a "GitHub Secret Scanner"-t vizsgálta, ami az **alert-alapú, utólagos** szkennelést jelenti (75% precizitás, 6% recall), **nem magát a push protection mechanizmust**, és 2023-as, jelenleg már elavult mintakészlet-állapotra (a jelenlegi 522 mintás katalógusnál valószínűleg szűkebb) vonatkozik. Nincs publikált, független adat arra, hogy a push protection éles blokkolása milyen arányban állít meg valódi titkot vs. hány legitim push-t akaszt meg fals riasztással.

## 3. GitHub "validity checks" (ellenőrzött titok mód) saját, elkülönített fals pozitív aránya

**Nem találtuk meg.** A hivatalos dokumentáció csak kvalitatívan írja le a validity checks működését (active/inactive/unknown állapotok), számszerű pontossági/FP-adatot nem közöl rá. A TruffleHogra viszont **van** ilyen szám (6% vs. 90% precizitás, 10% maradék FP verifikált módban — lásd `megallapitasok.md` 4.3) — ez az egyetlen konkrét, lektorált szám, ami a "verified vs unverified" kettősséget méri, de csak egy eszközre (TruffleHog), nem a GitHube-ra.

## 4. GitHub AI-alapú generikus (jelszó-) felismerés abszolút pontossági/FP száma

**Nem találtuk meg** abszolút számként. A GitHub 2026-os blogbejegyzése csak **relatív** csökkenést közöl ("75.76% reduction", "hundreds of customer-confirmed false positive alerts" alapon) — nincs megadva sem az előtte, sem az utána mért abszolút fals pozitív arány, sem a pontos mintaszám. Ezt a `megallapitasok.md` 2.4 pontja explicit gyártói állításként kezeli, nem mérésként — a feladat kikötése szerint.

## 5. A lektorált ESEM 2023 tanulmány teljes III. táblázata (mind a 9 eszköz nyers TP/FP/FN/ST/PS száma)

**Nem találtuk meg** géppel olvasható formában. Az ar5iv HTML-render a táblázat feliratát és az azt kísérő szöveges bekezdéseket (bullet point összegzések) helyesen adta vissza, de magát a táblázat celláinak nyers számsorát nem sikerült kinyerni a HTML-ből (feltehetően képként vagy komplex LaTeX-táblaként van beágyazva, amit az egyszerű tag-stripelő szkriptünk nem tudott lineáris szöveggé alakítani). A hiányzó pontos számokat (pl. Whispers, ggshield, git-secrets, Repo-Supervisor, SpectralOps, Commercial X konkrét TP/FP/FN értékei) a cikk szöveges bekezdéseiből idézett összefoglaló számokkal (top-3 lista) és a különálló FPSecretBench README FP-táblázatával pótoltuk — ez utóbbi minden eszközre lefedi a nyers FP-számot.

## 6. GitHub secret scanning partnerprogram jelenlegi (2026-os) pontos partnerszáma

**Nem találtuk meg** egy helyen kimondva. A 2023-as ESEM-tanulmány közli, hogy akkor "only 66 API vendors" vett részt a partnerprogramban; a jelenlegi (2026-09-15-i) hivatalos "Supported secret scanning patterns" oldal 522 mintát sorol fel, de ez minta-szám, nem partner-szám (egy partner több mintával/tokentípussal is szerepelhet), és a partnerprogram-bemutató oldal (`secret-scanning-partner-program`) csatlakozási útmutató, nem statisztikai összegzés — nem tartalmaz aktuális partnerszámot.

## 7. Formális, statisztikai levezetés az entrópia-küszöbökre

**Nincs ilyen** (a fellelt források szerint). Mind a gitleaks (3.5), mind a detect-secrets (4.5/3.0) küszöbei a fejlesztői dokumentáció szerint tapasztalati/közösségi próbálgatás eredményei ("trial and error and feedback from the Gitleaks community"), nem formális ROC-görbe-optimalizálás vagy hasonló statisztikai eljárás publikált eredménye. Ha létezik ilyen belső vizsgálat a gyártóknál, az nem publikus.

## 8. Az `easter-memory-system`-re (vagy bármilyen agent-memória-írási kapura) kifejezetten alkalmazott secret-detection publikáció

**Nincs ilyen** — ez várható volt, mivel ez egy konkrét, egyedi rendszer, nem publikus eszköz. A kutatás ezért kizárólag az általános, jól dokumentált iparági eszközök (gitleaks, TruffleHog, detect-secrets, GitHub) adataira támaszkodhatott, amelyek relevanciáját a kampány-feladat maga is feltételezte.

## 9. TruffleHog Driftwood adatbázis pontos találati/hamis arányszáma

**Nem találtuk meg** számszerűsítve. A 2022-es bejelentő blogbejegyzés csak esettanulmány-szerű, konkrét szervezetekre (Twitter, Netflix) vonatkozó anekdotikus számokat közöl ("about 25", "about 4811" privát kulcs), nem ad meg általános precizitás/recall-számot magára a Driftwood-adatbázis-egyeztetésre. Ezt a `megallapitasok.md`-ben T2/T3 anekdotaként, nem mérésként kezeltük.



---

# sq02 — Mit szűrnek a valódi agent-memória rendszerek íráskor

# sq02 — Hiányok

Két kategóriában: **"nincs ilyen"** (aktívan megnéztük ott, ahol lennie kellene, idézettel/hivatkozással alátámasztva, hogy a dolog ténylegesen hiányzik), és **"nem találtuk meg"** (a dolog valószínűleg létezik vagy nem zárható ki, de a kutatás során nem sikerült elérni/igazolni).

---

## A) "Nincs ilyen" — aktívan ellenőrzött, dokumentált hiányok

1. **Determinisztikus, LLM-mentes tartalom-kapu íráskor egyik vizsgált memória-rendszer saját, beépített funkciójaként sem létezik.** Mind a hat rendszernél (basic-memory, mem0, Zep/Graphiti, Letta, Anthropic memory tool, Claude Code auto-memory, OpenAI memória) kifejezetten kerestük ezt, és vagy semmilyen szűrés nincs (basic-memory, Graphiti OSS, Letta — csak méretkorlát), vagy a meglévő szűrés modell-alapú/valószínűségi (mem0 Custom Instructions, Anthropic "usually refuses", OpenAI "steer away"). Lásd `megallapitasok.md` 1. és az összegző táblázat.

2. **basic-memory-nál nincs PII-, titok- vagy tartalom-osztályozó modul** — a SECURITY.md kifejezetten és kizárólag útvonal-bejárás és parancsinjektálás elleni védelemről szól, a "Out Of Scope" szakasz explicit módon kizárja a hozzáférés-vezérlést az OS-felhasználók között.

3. **Letta-nál nincs memória-mérgezés elleni beépített védelem** — ezt nem csak a dokumentáció hiánya, hanem a projekt saját, nyitott GitHub issue-ja (#3342) is kifejezetten kimondja: "Letta presently lacks built-in defenses against memory poisoning as defined by OWASP ASI06 standards."

4. **Nincs mért adat arra, hogyan hat egy blokkoló memória-írási kapu az agent vagy az ügyfél viselkedésére** (6. kérdés). Kifejezetten kerestük DLP-gyártói blogokban, guardrail-keretrendszerek dokumentációjában és az OWASP Agent Memory Guard saját közléseiben — egyik forrás sem tartalmaz ilyen viselkedési/üzleti hatás-mérést. Ez a hatodik kérdésre adott végleges válasz: a hiány maga az eredmény.

5. **Nincs kifejezett "nem vagyunk biztonsági határ" jellegű nyilatkozat mem0, Zep/Graphiti vagy Letta hivatalos dokumentációjában/jogi oldalain** — célzottan kerestük ("security boundary", "not responsible", "your responsibility" kulcsszavakkal), és nem találtunk ilyet egyik rendszernél sem (szemben az Anthropic memory tool és a Microsoft Presidio explicit nyilatkozataival).

---

## B) "Nem találtuk meg" — létezhet, de nem sikerült igazolni

1. **A basic-memory szó szerinti "It is NOT a security boundary" állítása.** A kutatási feladat kiindulópontként idézi ezt a mondatot. Közvetlenül átvizsgáltuk a README.md-t, a SECURITY.md-t és a docs.basicmemory.com technikai-információ oldalát (mindhármat nyers formában) — egyikben sem szerepel ez a pontos szöveg. Lehetséges, hogy (a) egy korábbi vagy későbbi dokumentáció-verzióban szerepelt/szerepelni fog, (b) egy Discord-beszélgetésben vagy egy nem indexelt oldalon van, vagy (c) a feladatleírás egy hasonló, de nem pontosan idézett állítást általánosít. Lásd `ellentmondasok.md`.

2. **Az OWASP ASI06 hivatalos, teljes katalógus-szövege** (a definíció + támadási vektorok + ajánlott kontrollok hivatalos, "törzsszöveg" formája). Több valószínű URL-mintát próbáltunk a genai.owasp.org-on, mind 404-et adott. A tétel léte és tartalma számos független, egymással konzisztens másodlagos forrásból (Modulos, DeepTeam, Vectorize) rekonstruálható, de a szó szerinti hivatalos szöveget nem sikerült elérni.

3. **Az AgentPoison ">80%" és a MINJA ">95%/70%"** pontos számadatainak elsődleges (arXiv-absztrakt szintű) megerősítése. Az absztraktok megerősítik a támadások hatékonyságát kvalitatívan ("high probability", "minimal requirements... enables any user to influence agent memory"), de a konkrét százalékokat csak másodlagos forrás (mem0 blog) tulajdonítja nekik. Nem zárható ki, hogy a számok a teljes cikktörzsben (nem az absztraktban) szerepelnek — ezt nem ellenőriztük a teljes PDF/HTML letöltésével, idő/token-korlát miatt.

4. **Az "Agent Security Bench" (84,30%-os legmagasabb átlagos sikerességi arány) és az "A-MemGuard" (66%-os detekció-elmulasztás) tanulmányok elsődleges forrása.** Mindkettő egyetlen másodlagos hivatkozásból (Vectorize.io, illetve mem0 blog) származik ebben a kutatásban; az elsődleges publikációt nem azonosítottuk és nem kerestük meg külön.

5. **Van-e a memória-mérgezés kategóriájában kifejezetten kiadott CVE-azonosító.** A kutatás során talált CVE-k (EchoLeak, GitHub Copilot RCE, Cursor-lánc, Reprompt) mind a tágabb "prompt injection" kategóriába tartoznak, egyik sem kifejezetten "memory poisoning" címkével. Nem zárható ki, hogy létezik ilyen CVE, amit nem találtunk meg — de a kifejezetten erre irányuló keresés (`"CVE agent memory poisoning..."`) nem hozott ilyet.

6. **A Zep kereskedelmi platform "biztonsági garanciái"** konkrét tartalma. A nyilvános README egy összehasonlító táblázatban megemlíti ("Enterprise features: SLAs, support, security guarantees"), de nem specifikálja, mit takar ez — lehet, hogy létezik tartalom-szintű védelem a fizetős platformon, csak nyilvánosan nem dokumentált; ezt nem tudtuk sem megerősíteni, sem cáfolni.

7. **PraisonAI Issue #5028** ("Memory subsystem has no provenance/trust boundary...") tartalmának részletes elemzése elmaradt — csak a címét és a keresési index-előnézetét láttuk, a teljes issue-szöveget idő/token-korlát miatt nem kértük le. Címe alapján valószínűleg egy további, konkrét megerősítő példa lenne a hiányra egy negyedik keretrendszerben, de ezt nem igazoltuk közvetlenül.

8. **A "MemoryGraft" (Srivastava és He, 2025) és az "A-MemGuard" (2025) tanulmányok pontos bibliográfiai adatai** (folyóirat/konferencia, DOI, arXiv-szám) — ezeket csak a mem0 blog említése alapján ismerjük, elsődleges forrást nem azonosítottunk hozzájuk.
