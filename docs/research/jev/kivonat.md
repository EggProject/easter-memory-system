# Kivonat — Jev (TypeSafe AI döntési modell)

Kutatási egységenként, szó szerinti idézetekkel. SQ00: azonosítás; SQ01–SQ06: kutatási kör; ELL01–ELL03: adverzariális
ellenőrzés. Minden keresés az Exa eszközzel. A linkek a `linkek.md`-ben, a szintézis a `SZINTEZIS.md`-ben.

**Javítások az ellenőrzés után:** (1) a bejelentés dátuma a cég saját blogján 2026-09-14, a sajtóközleményben és a sajtóban
09-15; (2) az SQ00 szerint nincs hivatalos kredit-rendszer — téves: a Master Customer Agreement 8.2 szerint kredit-alapú
(SQ03, ELL01/8); (3) a „50 dolláros felelősségkorlát, bármikor felfüggeszthető" csak az ingyenes preview-feltételekre igaz,
fizetős ügyfélnél a 12 havi díj vagy 50 dollár közül a nagyobb, és a felfüggesztés felsorolt okokhoz kötött (ELL01/10);
(4) az SQ02-ben idézett független kalibrációs számhármas forrása belsőleg ellentmondásos, nem igazolt — a
számokat nem vesszük át (ELL02/2); (5) a „frontier dönt, gyors modell ellenőriz" mintára léteznek eszközök, csak számszerű haszon nincs
(ELL02/9).

---

# SQ00 — Mi az a „Jev"?

*Kutatási eszköz: kizárólag Exa (`web_search_exa`, `web_fetch_exa`) a beépített WebSearch/WebFetch helyett, az utasításnak megfelelően. Alügynök-indítás (deep-web-research skill teljes pipeline-ja) nem történt — ez egy egyszeri azonosító kör, ezért degradált, de Exa-only módban, elsődleges forrásokra támaszkodva dolgoztam.*

## Rövid válasz

A „Jev" a **TypeSafe AI** nevű San Franciscó-i startup 2026. szeptember 15-én bemutatott modellje, egy ún. **„System One model"**: nem szöveget generál, hanem előre definiált „állapot" (state) és tipizált „kérdések" alapján kalibrált valószínűségekkel ellátott strukturált döntéseket ad vissza (igen/nem, választás egy listából, vagy pontszám). A cég ezt „döntéstámogató" modellként pozicionálja, és a válaszidő 70–500 ezredmásodperc — ez 40–200-szor gyorsabb, mint egy hagyományos nagy nyelvi modell (LLM) egy hasonló feladaton, ami pontosan illik a felhasználó „döntést támogató, baromi gyors model" leírására. A modellt Diogo Almeida (a ChatGPT/RLHF egyik korábbi OpenAI-kutatója) alapította cége adja ki, 40 millió dolláros (DCVC vezette) magvető körrel a háttérben. A Jev jelenleg kizárólag felhős API-ként érhető el (nincs önállóan futtatható/letölthető verzió, a súlyokat nem publikálták), díjazása bemeneti tokenenkénti mérés ($0,042/millió token, kimenet ingyenes), és a hivatalos adatvédelmi szabályzat szerint a beküldött adatot nem használják modell-tanításra. Más, azonos nevű, de más gyártótól származó „döntéstámogató gyors AI modell" jelöltet nem találtam — az összes talált forrás ugyanerre a TypeSafe-féle Jevre mutat (bár számos harmadik fél üzemeltet nem hivatalos „Jev AI" márkázású wrapper/viszonteladó oldalt ugyanerre a modellre építve).

## Jelöltek

| Név | Kiadó | Megjelenés | Mit csinál | Illik-e a leírásra | Forrás |
|---|---|---|---|---|---|
| **Jev** (más néven `jev-1.13.0`, System One Model) | TypeSafe AI, Inc. (San Francisco; alapítók: Diogo Almeida, Erik Gafni, Sasha Sheng) | 2026-09-15, korlátozott „early access" | Nem generál szöveget; „state" + tipizált kérdések (Choice / Score / Noul) alapján kalibrált valószínűségű strukturált döntést ad vissza | **Igen, erősen illik**: kifejezetten „döntés"-modellként (decision model / System One model) hirdetik, és a válaszidő (70–500 ms) 40–200×, saját munkafolyamatokon akár 193,6× gyorsabb, mint egy frontier LLM | typesafe.ai/blog/introducing-system-one-models-and-jev; techcrunch.com (2026-09-18); en.wikipedia.org/wiki/Jev_(AI_model) |
| „Jev AI" / „Jev Agent" / „thejevai.com" / „jevai.net" / „jevaimodel.net" / „jev-ai.pro" stb. — **nem önálló modellek**, hanem harmadik felek által üzemeltetett wrapper-, viszonteladó- vagy tartalom-oldalak, amelyek a fenti TypeSafe Jev modellre építenek | Különböző, TypeSafe-hez nem köthető cégek (pl. a jevtypesafeai.com üzemeltetője saját vallomása szerint „CODEFASHION TECH LTD", és explicit kimondja: „not affiliated with or endorsed by TypeSafe AI") | 2026 szeptember (a Jev-launch utáni napokban/hetekben) | Ugyanazt az API-t/modellt hívják meg (`api.typesafe.ai/v1/systemone` vagy egy gateway), saját fizetős „credit"/„balance" réteggel a tetején | Nem önálló jelölt — ugyanaz a mögöttes modell, csak közvetítőn/viszonteladón keresztül, gyakran saját (nem hivatalos) előre feltöltött egyenleg-rendszerrel | jevtypesafeai.com/privacy; jev-ai.pro/pricing; jev-agent.com/plans; lovableapp.org ([]„We are not the official developer of Jev AI Model") |
| Más iparági/más cégtől származó, azonos nevű AI modell | — | — | — | **NINCS ilyen jelölt** — nem találtam a Jev névhez kötődő, TypeSafe-től független, más gyártótól származó AI-modellt vagy -terméket | (lásd „Amire NINCS forrás") |

**Megjegyzés:** a keresés során nem került elő olyan másik, TypeSafe-től független „Jev" nevű AI-modell vagy -cég, amellyel a névazonosság miatt össze lehetne téveszteni a fentit. Az egyetlen valós jelölt a TypeSafe AI Jev modellje; a többi „Jev AI"-branded oldal ugyanarra a mögöttes technológiára épülő, nem hivatalos harmadik fél.

## A legvalószínűbb jelölt részletei

### 1. Kiadó, megjelenés, pontos név/verzió

- Kiadó: **TypeSafe AI, Inc.**, 2024-ben alapítva, székhelye San Francisco. Alapítók: **Diogo Almeida** (korábban kb. 4 évig OpenAI-nál dolgozott az RLHF, InstructGPT, ChatGPT és GPT-4 fejlesztésén), **Erik Gafni** és **Sasha Sheng**. (Forrás: en.wikipedia.org/wiki/Jev_(AI_model), a Forbes és TechCrunch cikkeire hivatkozva.)
- Bejelentés dátuma: **2026. szeptember 15.**, a hivatalos blogbejegyzés címe: *„Introducing System One Models & Jev"*, szerzője Diogo Almeida. Idézet a bejegyzésből: *„After two years in stealth, countless technical challenges, and research breakthroughs… I am beyond excited to announce that today, TypeSafe AI is releasing our first System One Model… Our first public model is Jev, available today in early access."* (typesafe.ai/blog/introducing-system-one-models-and-jev)
- Egyidejűleg bejelentett **40 millió dolláros seed-kör**, vezető befektető a **DCVC**; a Forbes szerint a kör 200 millió dolláros értékelésen történt. (en.wikipedia.org/wiki/Jev_(AI_model), Forbes-idézettel)
- Pontos modellnév/verzió: **`jev-1.13.0`**, az alias `jev-latest` (és `jev-preview`) erre mutat. Ezt legalább négy egymástól független forrás egyezően állítja: atomicbot.ai, mrjev.com, learnjev.com, meetcody.ai — a TypeSafe hivatalos „Models" oldalára hivatkozva (ezt az oldalt közvetlenül nem sikerült lekérnem, `CRAWL_NOT_FOUND` hibát adott, de a Wikipédia is „Models" TypeSafe AI oldalt jelöl meg forrásként).
- Névválasztás: a modell névadója **William Stanley Jevons**, a 19. századi közgazdász, akiről a Jevons-paradoxont nevezték el (olcsóbb erőforrás → nagyobb felhasználás). Almeida szerint ez a várakozásukat tükrözi, hogy az olcsóbb gépi intelligencia sokkal szélesebb körű elterjedéshez vezet. (techcrunch.com; en.wikipedia.org/wiki/Jev_(AI_model))

### 2. Mit csinál — bemenet/kimenet

- **Nem nagy nyelvi modell (LLM)**, nem generál szabad szöveget. A hivatalos blog szerint: *„Think of Jev as a frontier-intelligence function call: unstructured state in, typed probabilistic decisions out."* (typesafe.ai/blog/introducing-system-one-models-and-jev)
- Bemenet: egy **„state"** blokk (string, JSON objektum vagy szöveges tömb) + egy vagy több tipizált **„question"**.
- Három kérdéstípus (a Wikipédia táblázata szerint, TechSpot cikke is megerősíti):
  - **Choice** — egy opció kiválasztása egy előre megadott (max. 255 elemű) listából, opciónkénti valószínűségekkel és konfidenciával.
  - **Score** — rendezett szintek szerinti pontozás, szintenkénti valószínűségekkel és konfidenciával.
  - **Noul** — igen/nem jellegű állítás értékelése, 0 és 1 közti valószínűséggel.
- A modell minden kérdést **egyetlen párhuzamos lépésben** értékel ki (nem szekvenciális tokenenkénti generálás), ezért új kérdések hozzáadása alig növeli a válaszidőt.
- Mivel a lehetséges válaszok előre rögzítettek, a modell — a cég állítása szerint — architektúrájából adódóan **nem tud a megadott sémán kívüli értéket visszaadni** („zero hallucinations" a kimenet formátumára nézve, de téves választás a megadott opciók közül még lehetséges — ezt a TechSpot cikk is hangsúlyozza: *„'Can't hallucinate' is a narrow claim. […] it can still confidently pick the wrong option."*).
- Az architektúra részletei (pontos felépítés, súlyok, paraméterszám) **nincsenek publikálva**; a cég csak annyit közöl, hogy transzformer-alapú, és kizárólag szintetikus adaton, egy általuk „Reinforcement Learning for Calibrated Decisions" (RLCD) nevű módszerrel tanított. Külső megfigyelők (pl. a TechCrunch által idézett Armin Ronacher) feltételezik, hogy egy nyílt súlyú LLM-re épülhet, de ez nem megerősített. (techcrunch.com; en.wikipedia.org/wiki/Jev_(AI_model))

### 3. Sebesség — gyártói állítás és független mérés

- Gyártói állítás (típusos, végpontig mért válaszidő): **70–500 ezredmásodperc**, szemben a frontier LLM-ek 3–329 másodperces végpontig mért válaszidejével. Ez a hivatalos blog saját táblázatában szerepel: *„End-to-end response time is 70ms-500ms for TypeSafe. This can range from 40x-200x faster."* (typesafe.ai/blog/introducing-system-one-models-and-jev)
- A cég saját, négy munkafolyamatra épülő tesztjein a csúcsérték **193,6× gyorsabb és 444,6× olcsóbb** — ezt maga a TypeSafe is jelzi, hogy valószínűleg a valós felhasználási tartomány felső határát képviseli, és a teszteket a saját „model capabilities" csapata készítette (elismert torzítási kockázat). (en.wikipedia.org/wiki/Jev_(AI_model), a TypeSafe „technical notes"-ára hivatkozva)
- **Független/harmadik fél mérések** (nem hivatalos, de konkrét, reprodukálható számokkal):
  - Vercel mérnöke (Pranit Sharma) egy biztonsági parancs-osztályozó feladatnál OpenAI Luna 5.6-ról Jevre váltva **5–18-szor gyorsabb** eredményt kapott, nagyobb pontossággal. (techcrunch.com)
  - jev-agent.com saját, élő API-hívásokon mért (nem gyártói) adatai: egy 3 opciós Choice-hívás 342 input tokennel **$0,0000144**-be került; egy Choice+Score+Noul kombinált hívás 539 tokennel **$0,0000226**. (jev-agent.com/pricing, dátum: 2026-09-18)
  - madewithjev.com 15, egymástól független, publikált (blog/közösségi) futtatás mediánját aggregálva: **$0,000068/döntés** (~14 727 döntés/dollár).
  - Egy 26 lapos építési tervkészlet-osztályozásnál: Jev 2,9 másodperc alatt, $0,0052-ért, GPT-4.1-es saját pipeline-jukhoz képest **17–21×olcsóbban és 5× gyorsabban**, 100%-os egyezéssel. (madewithjev.com)
- **Ellenpélda / korlát**: a TechSpot cikk szerint a TypeSafe saját négy-munkafolyamatos tesztjén Jev összesített egyezése (agreement) a referenciamodellekkel **67,8%**, szemben a GPT-5.6 Sol **74,1%**-ával — számla-feldolgozásnál kifejezetten lemaradva (61,8% vs. 79,1%). Ez azt jelzi, hogy a sebesség/ár előny pontossági kompromisszummal járhat feladattípustól függően. (techspot.com, 2026-09-20)

### 4. Elérhetőség — csak felhős API, vagy önállóan futtatható? Licenc?

- **Kizárólag hosztolt (felhős) API**, TypeSafe saját szerverein fut; **a súlyokat nem publikálták**, nincs hivatalos self-hosting opció. Ezt több, egymástól független forrás megegyezően állítja:
  - systemonemodels.org: *„Weights are not released, so there is no self-hosted option."*
  - jevtypesafeai.com FAQ: *„No — Jev is a hosted model from TypeSafe AI, called over an API. […] The model itself runs on TypeSafe's servers."*
  - modemguides.com összehasonlító táblázata: „Weights: Closed; no self-host option published" — szemben a nyílt súlyú helyi alternatívákkal.
- Hivatalos hozzáférési út: regisztráció várólistával a `console.typesafe.ai`-on, API-kulcs, végpont **`POST https://api.typesafe.ai/v1/systemone`**, Bearer-tokenes hitelesítéssel. Nem OpenAI-kompatibilis (nincs `/chat/completions`, nincs `messages` tömb). (opentweet.io/jev/api-access)
- Harmadik fél gateway-eken keresztül is elérhető, várólista nélkül: **OpenRouter** (`typesafe/jev-1.13`), **Vercel AI Gateway** (`typesafe-ai/jev`), **Cloudflare AI Gateway** (`typesafe/jev`) — mindegyik ugyanazt a hivatalos árat számlázza tovább (esetleg felárral). (openrouter.ai/typesafe/jev-1.13; vercel.com/ai-gateway/models/jev; madewithjev.com/jev-pricing)
- Licenc: **zárt forráskódú, proprietary** szoftver — ezt a Wikipédia kategóriabesorolása is megerősíti („Proprietary software"). Nincs nyílt forráskódú vagy letölthető változat.

### 5. Árazás és elszámolás

- Hivatalos (TypeSafe első feles) árazás: **$0,042 / millió bemeneti token** ($42/milliárd token), **a kimeneti tokenek ingyenesek** („too cheap to meter"). Ez a hivatalos blogból közvetlenül idézhető: *„Input tokens: $0.042 / MTok ($42 per billion tokens). Output tokens: FREE (too cheap to meter)."* (typesafe.ai/blog/introducing-system-one-models-and-jev)
- **Nincs hivatalos, publikált előre-feltöltött „balance"/kredit rendszer és nincs publikált ingyenes csomag** a TypeSafe saját API-jánál — ezt három egymástól független forrás is kifejezetten megerősíti:
  - learnjev.com FAQ: *„There is no published free tier, trial credit or plan structure — `typesafe.ai/pricing` returns a 404, and the Models page is the only pricing artefact that exists."*
  - eesel.ai: *„TypeSafe does not have a dedicated pricing page… Not a self-serve free tier. Access is through an early-access waitlist…"*
  - opentweet.io/jev/api-access: *„There is no free tier. TypeSafe has not published a free allowance, a trial credit or a hobby plan…"*
  - Sebességkorlátok (rate limit) igen vannak: 250 000 token/másodperc és 1200 kérés/perc, de a TypeSafe explicit jelzi, hogy ezek előzetes értesítés nélkül változhatnak („early access" szakaszban). (jevaiguide.com/faq; mrjev.com/pricing)
- **FONTOS MEGKÜLÖNBÖZTETÉS**: az „előre feltöltött egyenleg / kredit" (balance/credit) modellt **nem a hivatalos TypeSafe API kínálja**, hanem **harmadik fél viszonteladó/wrapper oldalak** (pl. `jev-ai.pro`, `jev-agent.com`), amelyek a TypeSafe API-t hívják meg a háttérben, és saját fizetős kredit-rendszert (pl. „1 kredit = 1000 input token", ingyenes napi „check-in" kreditek, soha le nem járó vásárolt kreditcsomagok) építenek rá. Ezek az oldalak explicit kimondják, hogy nem a TypeSafe hivatalos szolgáltatásai — pl. jevtypesafeai.com/privacy: *„It is an independent developer platform and is not affiliated with or endorsed by TypeSafe AI."* Ha a felhasználó egy „előre feltöltött egyenleg" rendszerről hallott a Jevvel kapcsolatban, az valószínűleg egy ilyen **nem hivatalos, harmadik feles** szolgáltatásra vonatkozik, nem magára a TypeSafe API-ra.
- Mi történik, ha elfogy az egyenleg/kredit: a hivatalos TypeSafe API-nál ez a kérdés nem releváns (nincs előre feltöltött egyenleg, tokenenkénti utólagos/folyamatos elszámolás történik, sikertelen kérésekért nincs terhelés — ezt több forrás is jelzi rate-limit `429` válaszkóddal kapcsolatban). A nem hivatalos harmadik fél oldalaknál (pl. jev-ai.pro) `402` hibakód jelzi a hitel/token hiányát („no credits").

### 6. Nyelvek: angol, magyar támogatás

- **Nem találtam hivatalos forrást** arra vonatkozóan, hogy a TypeSafe kifejezetten mely nyelveket (pl. magyar) támogatja a bemeneti „state"/kérdés mezőkben. A dokumentáció csak annyit rögzít, hogy a bemenet „szöveg" (string, JSON objektum vagy szöveges tömb), nyelvi korlátozás vagy nyelvlista nélkül. (atomicbot.ai táblázata: *„Input: Text only… No images, audio, or video"* — de konkrét nyelvekről nem esik szó.)
- Mivel külső megfigyelők szerint a Jev valószínűleg egy meglévő (feltehetően többnyelvű) nyílt súlyú LLM-re épül (techcrunch.com, Armin Ronacher idézete), **elméletileg** kezelhet más nyelveket is, de ezt a TypeSafe nem állítja és nem is dokumentálja — ez egy feltételezés, nem megerősített tény.
- A Jev híre magyar nyelvű technológiai médiában is megjelent: a **Mobilissimo.hu** 2026-09-19-én cikket közölt róla („A következő AI talán egy szót sem szól hozzád: mit tud a Jev, és miért érdemes figyelni rá?"), de ez a modell **magyar nyelvi képességéről**, nem annak *ismertségéről* szól — a cikk maga is angol nyelvű forrásokra (TechCrunch) hivatkozva mutatja be a modellt, a magyar nyelvi támogatásról nem nyilatkozik.
- **Következtetés: NINCS FORRÁS** arra, hogy a Jev hivatalosan támogatja-e (vagy sem) a magyar nyelvet.

### 7. Adatkezelés: megőrzés, tanítás, régió

- Hivatalos adatvédelmi szabályzat (typesafe.ai/legal/privacy, utolsó frissítés: 2025-11-19) — **szó szerinti idézet**: *„We collect the personal data you provide when you use the Services, including your prompts, data, instructions, and other input ('Input'). We will not train or fine tune any artificial intelligence or machine learning models on your prompts or other Input."*
- Ezt két független másodlagos forrás is megerősíti:
  - jevaiguide.com/faq: *„According to TypeSafe, no: Jev is not trained on customer requests or responses, and every customer uses the same model weights. TypeSafe offers zero data retention (ZDR) to enterprise customers."*
  - modemguides.com: *„TypeSafe's privacy policy… states that the company will not train or fine-tune models on customer input and will not disclose input to third parties other than its service providers."*
- **Megőrzési idő**: a hivatalos szabályzat nem ad konkrét, fix megőrzési határidőt („as long as necessary" jellegű megfogalmazás — DPA szerint: *„Customer Personal Data will be retained for as long as necessary taking into account the purpose of the Processing…"*, typesafe.ai/legal/data-processing). **Nulla adatmegőrzés (ZDR)** csak vállalati (enterprise) ügyfeleknek elérhető, külön megkereséssel (privacy@typesafe.ai) — alapértelmezésben tehát NEM garantált a nulla megőrzés. (jevaiguide.com/faq)
- **Régió/hosztolás**: a szolgáltatás **az Egyesült Államokban** fut. Egy harmadik fél jogi elemzés (wunderlandmedia.com) szerint az alvállalkozók (subprocessor-ok) mind amerikai cégek (AWS — tárolás/feldolgozás; Modal — az inferencia futtatása, promptok tárolása nélkül; Slack és Google Workspace — ügyfélszolgálat), és a TypeSafe **nincs tanúsítva az EU–US Data Privacy Framework alatt** (ezt a szerző saját ellenőrzése alapján állítja, mivel a hivatalos DPF-listán nem találta a céget). Nincs bejelentett EU-s régió/hosztolási opció. Ezt egy másik független forrás (learnjev.com FAQ) is megerősíti: *„US servers only at launch; no EU region has been announced."*
- **Fontos árnyalat / kockázat, amit egy jogi elemzés (wunderlandmedia.com) kiemel**: a hivatalos Privacy Policy „nem tréníroz" ígérete és a Master Customer Agreement (MCA) szűkebb, „hozzájárulással felülírható" tanítási kikötése (4.1. klauzula) között ellentmondás/feszültség van — ez azonban egy harmadik fél (nem TypeSafe-hivatalos, ügyvédi jellegű) elemzés értelmezése a szerződéses dokumentumokról, amit önmagában, elsődleges forrás nélkül nem lehet 100%-ig megerősíteni. Lásd „Ellentmondások".

## Ellentmondások

1. **Cégnév-tévesztés egyes másodlagos forrásokban**: egy YouTube-összefoglaló alapú cikk (gist.ly) a TypeSafe AI-t tévesen **„Typeface"**-ként, illetve **„System 1"**-ként nevezi meg cégnévként, és az alapítót „Diego Almeida"-ként írja (a helyes név **Diogo Almeida**, ahogy azt a TechCrunch, a Wikipédia és a hivatalos TypeSafe blog is következetesen írja). Ez egy alacsonyabb megbízhatóságú (automatikusan generált) forrás hibája, nem tényleges névváltozat.
2. **„Balance"/kredit-rendszer eredete**: több nem hivatalos, harmadik feles oldal (jev-ai.pro, jev-agent.com) kínál előre feltöltött, soha le nem járó kredit-csomagokat és napi ingyenes „check-in" krediteket — ezt könnyű összetéveszteni a TypeSafe hivatalos, tisztán tokenenkénti (nem előre feltöltött egyenlegű) elszámolásával. A kettő **nem ugyanaz**; lásd az „5. Árazás" pontot.
3. **Adatvédelmi szabályzat vs. szerződéses feltételek feszültsége**: a wunderlandmedia.com jogi elemzése szerint a nyilvános Privacy Policy („nem tréníroz semmilyen modellt az Input-on") és a Master Customer Agreement 4.1. klauzulája (amely ügyfél-hozzájárulással megengedné a tréningadatba való bevonást) között eltérés lehet. Ez egy harmadik fél jogi értelmezése, amit közvetlenül a TypeSafe MCA-jából nem tudtam ellenőrizni (a teljes MCA szövegét nem kerestem/olvastam külön), ezért ezt fenntartással, „állítólagos ellentmondásként" közlöm.
4. **A gyártói benchmark-számok (193,6× gyorsabb, 444,6× olcsóbb) vs. független eredmények**: a TypeSafe saját, legjobb esetre optimalizált munkafolyamat-teszteken mért csúcsértékeit maga a cég is a „valószínűleg a felső határ" kategóriába sorolja; a független/felhasználói mérések (5–200× tartományban) ez alatt maradnak, illetve pontosság tekintetében (67,8% vs. 74,1–79,1% versenytárs modellekhez képest) helyenként gyengébb eredményt mutatnak. Ez nem cáfolat, inkább a marketing-számok és a valós terhelés közti általános eltérés.

## Amire NINCS forrás

- **Magyar nyelvi támogatás** (input/output nyelve, minőség magyar szövegen) — nincs hivatalos vagy független forrás, csak feltételezés arról, hogy a mögöttes (feltehetően többnyelvű) LLM-alap miatt elméletileg működhet.
- **Pontos architektúra, paraméterszám, súlyok** — a TypeSafe kifejezetten nem publikálta; minden erre vonatkozó állítás (pl. „egy nyílt súlyú LLM-re épül") külső megfigyelők feltételezése, nem megerősített tény.
- **Független, harmadik fél által végzett, publikált, szigorúan kontrollált benchmark** (pl. akadémiai vagy elismert AI-benchmark szervezettől) — csak vállalati saját tesztek és elszórt fejlesztői/blogger mérések találhatók, ezek nem tekinthetők szigorú, módszertanilag auditált független validációnak.
- **Konkrét, fix adatmegőrzési határidő** a standard (nem-enterprise) API-hozzáférésre — a szabályzat csak „szükséges ideig" jellegű megfogalmazást ad.
- **EU/egyéb nem amerikai adatközponti régió elérhetősége** — jelenleg nincs bejelentve, több forrás szerint is kizárólag USA-hosztolás van.

## Meglátogatott linkek

| Cím | URL | Tier | Eszköz | Megjegyzés |
|---|---|---|---|---|
| Introducing System One Models & Jev (TypeSafe AI blog) | https://typesafe.ai/blog/introducing-system-one-models-and-jev | T1 | Exa web_fetch_exa | Hivatalos bejelentés, elsődleges forrás — árazás, sebesség, architektúra-táblázat |
| TypeSafe AI: Home | https://typesafe.ai/ | T1 | Exa web_search_exa (highlight) | Hivatalos honlap, cégleírás |
| Privacy policy — TypeSafe AI | https://typesafe.ai/legal/privacy | T1 | Exa web_fetch_exa | Hivatalos adatvédelmi szabályzat, „nem tréníroz Input-on" idézet forrása |
| Data processing addendum — TypeSafe AI | https://typesafe.ai/legal/data-processing | T1 | Exa web_search_exa (highlight) | Hivatalos DPA — adatmegőrzés, EU-transzfer feltételek |
| Jev (AI model) — Wikipédia | https://en.wikipedia.org/wiki/Jev_(AI_model) | T2 | Exa web_fetch_exa | Tercier/enciklopédikus, de jól hivatkozott (Forbes, TechCrunch, The Register stb.) |
| A new kind of AI model from a ChatGPT inventor is thrilling developers — TechCrunch | https://techcrunch.com/2026/09/18/a-new-kind-of-ai-model-from-a-chatgpt-inventor-is-thrilling-developers/ | T1 | Exa web_fetch_exa | Elsődleges újságírói forrás, közvetlen Almeida-idézetekkel |
| What Is Jev? — LangChain blog | https://www.langchain.com/blog/building-a-harness-with-jev | T2 | Exa web_search_exa (highlight) | Hivatalos integrációs partner (LangChain) blogja |
| Jev 1.13 — API Pricing & Providers — OpenRouter | https://openrouter.ai/typesafe/jev-1.13 | T2 | Exa web_search_exa (highlight) | Gateway-szolgáltató hivatalos ártáblázata |
| Jev — Vercel AI Gateway | https://vercel.com/ai-gateway/models/jev | T2 | Exa web_search_exa (highlight) | Gateway-szolgáltató hivatalos modell-oldala |
| Meet Jev: A New AI Model From One of ChatGPT's Co-Creators — TechSpot | https://www.techspot.com/article/3172-meet-jev/ | T2 | Exa web_search_exa (highlight) | Részletes újságírói elemzés, benchmark-kritikával |
| TypeSafe Releases Decision Model Jev — METAL | https://metallab.ai/en/2026/9/typesafe-jev-decision-model | T2 | Exa web_search_exa (highlight) | Elemző cikk, Vercel-adaptációs adatokkal |
| Jev Explained — tao.media | https://www.tao.media/jev-explained-the-ai-model-that-makes-decisions-instead-of-writing-answers/ | T2 | Exa web_search_exa (highlight) | Magyarázó cikk, kérdéstípusok táblázata |
| What Is Jev? — atomicbot.ai | https://atomicbot.ai/blog/what-is-jev | T2/T3 | Exa web_search_exa (highlight) | Technikai összefoglaló, verziószám és limitek táblázata |
| TypeSafe AI's Decision Model Jev Becomes Vercel's Fastest Adopted Launch — Startup Fortune | https://startupfortune.com/typesafe-ais-decision-model-jev-becomes-vercels-fastest-adopted-launch/ | T2 | Exa web_search_exa (highlight) | Adopciós statisztikák (Vercel) |
| Jev rate limits, context window and pricing — OpenTweet | https://opentweet.io/jev/limits | T3 | Exa web_search_exa (highlight) | Harmadik fél technikai elemzés, számítási példákkal |
| Jev pricing, latency, and benchmarks — Refix | https://www.refix.ai/news/jev-pricing-latency-benchmarks/ | T3 | Exa web_search_exa (highlight) | Óvatosságra intő elemzés a gyártói benchmarkokról |
| Jev API — jev-ai.pro | https://jev-ai.pro/jev-api | T3 | Exa web_search_exa (highlight) | **Nem hivatalos** harmadik fél viszonteladó/wrapper API, saját kredit-rendszerrel |
| Jev cost & billing — Jev Agent | https://jev-agent.com/pricing | T3 | Exa web_search_exa (highlight) | Nem hivatalos, de saját mért adatokat közöl API-hívásokról |
| Pricing — Jev AI (jev-ai.pro) | https://jev-ai.pro/pricing | T3 | Exa web_search_exa (highlight) | Nem hivatalos előfizetéses/kredit csomagok |
| Jev Pricing Explained — MrJev | https://mrjev.com/pricing/ | T3 | Exa web_search_exa (highlight) | Harmadik fél összefoglaló, hivatalos árra hivatkozva |
| Jev by TypeSafe AI — jevtypesafeai.com | https://www.jevtypesafeai.com/ | T3 | Exa web_search_exa (highlight) | Nem hivatalos fejlesztői portál |
| Jev API credits — Jev Agent | https://jev-agent.com/plans | T3 | Exa web_search_exa (highlight) | Nem hivatalos kredit-csomagok, egyértelműen jelzi, hogy „not TypeSafe" |
| Jev pricing — madewithjev.com | https://madewithjev.com/jev-pricing | T3 | Exa web_search_exa (highlight) | Aggregált közösségi/blog költség-adatok (15 publikált futtatás) |
| TypeSafe Jev pricing 2026 — eesel AI | https://www.eesel.ai/blog/typesafe-jev-pricing | T3 | Exa web_search_exa (highlight) | Megerősíti: nincs hivatalos pricing-oldal, 404-es typesafe.ai/pricing |
| Jev — Vercel AI Gateway (2. hivatkozás) | https://vercel.com/ai-gateway/models/jev | T2 | — | (ismételt hivatkozás) |
| Jev API key and access without the waitlist — OpenTweet | https://opentweet.io/jev/api-access | T3 | Exa web_search_exa (highlight) | Hozzáférési útvonalak, endpoint-részletek |
| Jev FAQ — Learn Jev | https://learnjev.com/faq | T3 | Exa web_search_exa (highlight) | Megerősíti: nincs EU régió, nincs ingyenes csomag |
| How to get Jev API access — System One Models | https://systemonemodels.org/guides/how-to-get-jev-access/ | T3 | Exa web_search_exa (highlight) | Megerősíti: nincs self-hosting, súlyok nem publikusak |
| Get Jev Access — jevmodel.org | https://jevmodel.org/get-jev/ | T3 | Exa web_search_exa (highlight) | Hozzáférési útmutató |
| Does Jev Train on Your Data? — jevaiguide.com | https://jevaiguide.com/faq/does-jev-train-on-your-data/ | T3 | Exa web_search_exa (highlight) | Adatvédelmi FAQ, ZDR-részletekkel |
| TypeSafe AI: Jev 1.13 — Opper | https://opper.ai/typesafe/jev-1-13-0 | T3 | Exa web_search_exa (highlight) | Gateway-aggregátor, régió/ZDR-státusz táblázat |
| Jev AI Reality Check — modemguides.com | https://www.modemguides.com/blogs/ai-news/jev-typesafe-reality-check-run-locally | T3 | Exa web_search_exa (highlight) | Self-hosting vs. hivatalos API összehasonlítás |
| Jev 1.13: Price, API, Specs & Data Policy — meetcody.ai | https://meetcody.ai/models/jev-1-13/ | T3 | Exa web_search_exa (highlight) | Adatkezelési összefoglaló |
| Privacy Policy — jevtypesafeai.com | https://jevtypesafeai.com/privacy | T3 | Exa web_search_exa (highlight) | Explicit kimondja: „not affiliated with… TypeSafe AI” |
| TypeSafe AI Jev Terms of Service: EU Read — Wunderlandmedia | https://wunderlandmedia.com/typesafe-ai-jev-terms-of-service-gdpr | T3 | Exa web_search_exa (highlight) | Jogi (nem hivatalos) szerződéselemzés, MCA/DPA feszültségek |
| Jev AI — jevai.net | https://jevai.net/ | T3 | Exa web_search_exa (highlight) | Nem hivatalos/fan landing oldal |
| Jev AI — thejevai.com | https://thejevai.com/ | T3 | Exa web_search_exa (highlight) | Nem hivatalos playground/wrapper |
| Jev: The Lightning Fast AI Model for Decisions — gist.ly | https://gist.ly/youtube-summarizer/jev-the-lightning-fast-ai-model-for-decisions | T3 | Exa web_search_exa (highlight) | Alacsony megbízhatóságú, cégnév-tévesztést tartalmaz („Typeface”) |
| Jev AI Model — Lovable App | https://lovableapp.org/products/jevaimodel-net | T3 | Exa web_search_exa (highlight) | App-directory, explicit jelzi: nem hivatalos |
| How to Use the Jev AI Model — huggingface.co/blog | https://huggingface.co/blog/sora-2/how-to-use-the-jev-ai-model-a-step-by-step-develop | T3 | Exa web_search_exa (highlight) | Gyanúsan generált/SEO jellegű, huggingface.co aldomainen |
| Jev API & Hub — jevai.org | https://www.jevai.org/jev-api | T3 | Exa web_search_exa (highlight) | Nem hivatalos közösségi hub |
| Jev vs. LLMs — Refix | https://www.refix.ai/news/jev-vs-llms/ | T2/T3 | Exa web_search_exa (highlight) | Kontextusba helyező elemzés |
| My Early Thoughts on Jev — danielmiessler.com | https://danielmiessler.com/blog/early-thoughts-on-jev | T3 | Exa web_search_exa (highlight) | Egyéni szakértői blogvélemény |
| What is Jev? — Vesper | https://www.vespernews.com/en/articles/tech/66c1fee4-4a3a-4328-98e1-40c800fd947e | T2 | Exa web_search_exa (highlight) | Hírportál összefoglaló |
| TypeSafe (Jev) — Pydantic AI docs | https://pydantic.dev/docs/ai/models/typesafe/ | T2 | Exa web_search_exa (highlight) | Hivatalos SDK-integrációs dokumentáció (Pydantic AI) |
| typesafe_jev — Rust crate docs | https://docs.rs/typesafe-jev/latest/typesafe_jev/ | T2/T3 | Exa web_search_exa (highlight) | Közösségi/nem-hivatalos Rust kliens dokumentációja |
| Model · Experiential | https://platform.experientiallabs.ai/models/jev-latest | T3 | Exa web_search_exa (highlight) | Gateway-szolgáltató modell-oldala |
| A következő AI talán egy szót sem szól hozzád — Mobilissimo.hu | https://www.mobilissimo.hu/a-kovetkezo-ai-talan-egy-szot-sem-szol-hozzad-mit-tud-a-jev-es-miert-erdemes-figyelni-ra/ | T2 | Exa web_search_exa (highlight) | Magyar nyelvű hírportál, a TechCrunch-cikkre hivatkozva |
| typesafe.ai/models (hivatalos Models oldal) | https://typesafe.ai/models | — | Exa web_fetch_exa | **Sikertelen lekérés** (`CRAWL_NOT_FOUND`) — csak közvetett (más forrásokon keresztüli) hivatkozás áll rendelkezésre erre az oldalra |

---

# SQ01 — Mit tud a Jev pontosan: API, bemenet, kimenet, korlátok, elérhetőség

*Módszer: kizárólag Exa (`web_search_exa`, `web_fetch_exa`) eszközzel kutatva, a `_kozos.txt` és az `anthropic-skills:deep-web-research` elvei szerint. Alügynök-indítás ezúttal sem történt (egyetlen, célzott SQ-kör), ezért ez is degradált, de Exa-only, elsődleges forrásokra épülő munkamenet — a sq00-hoz hasonlóan. A TypeSafe hivatalos dokumentációs oldala (`docs.typesafe.ai`) egy `llms.txt`/`llms-full.txt` gépi-olvasható indexet is publikál, ez tette lehetővé, hogy a legtöbb API-részletet közvetlenül, szó szerint, a hivatalos doksiból idézzem.*

## Rövid válasz

A Jev API-ja egyetlen HTTP-végpont — `POST https://api.typesafe.ai/v1/systemone`, Bearer-tokenes hitelesítéssel —, amely egy `state` mezőt (szöveg, JSON objektum vagy tömb) és egy `questions` map-et vár, típusonként Choice (max. 255 opció), Score (2–10 szint) vagy Noul (yes/no) kérdésekkel; egy hívásban tetszőleges számú kérdés fut párhuzamosan, ugyanarra a state-re. A válasz kérdésenként egy típusos „answer"-t ad vissza valószínűség-eloszlással (Choice, Score) és `confidence`-szel (Choice, Score), plusz `usage` token-számlálást; nincs sem `temperature`, sem `seed`, sem `stream` mező — a hivatalos doksi ezeket nem is sorolja fel a kérésmezők közt. A kontextusméret hivatalosan **64 000 token/kérés, ezen belül 32 000 token a `state` + a leghosszabb kérdés** — de két hivatalos gateway-oldal (Cloudflare, OpenRouter) csak 32 000 tokenes kontextusablakot hirdet, ami ellentmond a TypeSafe saját 64k-s számának (lásd Ellentmondások). Determinizmust a gyártó nem ígér 100%-osan, de a saját dokumentációja és egy saját cookbookja szerint a Jev „stabil válaszokat ad ismételt kiértékelésre", mérve ~0,01 szórással (LLM-ekhez képest alacsonyabb, de nem nulla) — nincs kitett seed/temperature paraméter. A gyártói késleltetés-állítás 70–500 ms végponttól végpontig, saját bevallásuk szerint „nyugati parti laptopokról" mérve; ezt sem a gyártó, sem független fél nem publikálta szigorúan kontrollált módszertannal. Rate limit hivatalosan 250 000 token/mp és 1200 kérés/perc, de a TypeSafe kifejezetten jelzi, hogy ezek az early access alatt előzetes értesítés nélkül változhatnak. Hivatalos hibakód-tábla csak négy kódot sorol (401, 422, 429, 529), de a saját JavaScript SDK-ja emellett 400/403/404/500-hoz is definiál kivétel-osztályt — ez dokumentációs rés, nem ellentmondás. A Jev 2026-09-14/15-én indult zárt várólistával, majd **2026-09-20-án a TypeSafe hivatalosan megszüntette a várólistát** („Jev is now available to everyone. No waitlist.") — ezt ma (2026-09-25) a `console.typesafe.ai` közvetlen, várólista nélküli bejelentkezési képernyője is megerősíti. Van hivatalos, publikus státuszoldal (`status.typesafe.ai`) kiesés-történettel, de nincs publikált SLA-számadat: a Master Customer Agreement kifejezetten kimondja, hogy a szolgáltatás megszakítás-mentessége nincs garantálva. Hivatalos SDK Python (`typesafe-sdk`, PyPI) és JavaScript/TypeScript (`@typesafe-ai/sdk`, npm) nyelven létezik; más nyelvekhez (Rust stb.) csak nem hivatalos, közösségi kliensek találhatók.

## 1. Modellnév, verzió, álnevek, elérhetőség státusza (ma: 2026-09-25)

- Hivatalos bejelentés a TypeSafe blogján, dátumozás a blogoldalon **„Sep 14, 2026"**, szerzője Diogo Almeida: *„Our first public model is Jev, available today in early access."* (https://typesafe.ai/blog/introducing-system-one-models-and-jev) — megjegyzendő, hogy a sq00-ban idézett, ugyanerről a bejegyzésről készült másodlagos leírások (pl. Wikipédia, TechCrunch) szept. 15-öt írnak dátumként; ez a blogoldal saját dátumbélyege és a hírek dátuma közti egy napos eltérés, l. Ellentmondások.
- Pontos, versionált modellnév: `jev-1.13.0`. Aliasok, a hivatalos Models oldalról szó szerint: *„`jev-latest` | `jev-1.13.0` | The most recent stable, official release... `jev-preview` | `jev-1.13.0` | The most recent release, whether or not it is an official one."* (https://docs.typesafe.ai/models — `llms-full.txt`/`models.md` lekérésből)
- **Várólista-státusz változása** (fontos, mert a felhasználói kérdés releváns eleme, hogy „elfogy-e a balance / elérhető-e"): indításkor zárt, meghívásos early access volt. A TypeSafe hivatalos X-fiókja (@typesafeai) 2026-09-20-án posztolta: *„Jev is now available to everyone. No waitlist."* — ezt egy harmadik fél archívum-szolgáltatás (unrollnow.com, bittide.aicompass.dev) mentette el, közvetlen X-elérést az Exa nem tudott adni (`SOURCE_NOT_AVAILABLE`). **Közvetlenül ellenőriztem magán a `console.typesafe.ai` oldalon is** (ma, 2026-09-25): a bejelentkezési képernyő önkiszolgáló „Welcome back / Continue with Google / Continue with email" — nincs várólista-űrlap. Ez maga is elsődleges (első feles) megerősítés. Emellett **két, egymástól független harmadik fél cikk** is ugyanezt írja: *„TypeSafe posted on September 20 that Jev is available to everyone, with no waitlist... Every account starts with $5 of credit"* (jevainews.com, https://jevainews.com/news/jev-no-waitlist/, 2026-09-20) és *„The Jev waiting list no longer exists — TypeSafe AI removed it on 21 September 2026"* (https://bestaiagentcommunity.com/blog/jev-waiting-list/, 2026-09-22; és egy szinte azonos szövegű másik cikk ugyanazon szerzőtől, Julian Goldie, más domainen — ez utóbbi kettő ugyanattól a szerzőtől való, tehát ténylegesen csak fél-független megerősítés, óvatosan kezelendő).
- Licenc/hozzáférés: kizárólag felhős API, a súlyok nem publikusak — ezt a jelen kör nem cáfolta, és a hivatalos MCA license-klauzulája (2.3.c) kifejezetten tiltja a reverse engineeringet és a „source code or underlying data" elérését: *„reverse engineer, decompile, disassemble, or attempt to access or derive the source code or underlying data with respect to the Services"* (https://typesafe.ai/legal/mca, utolsó frissítés: 2026-08-27).
- Fontos MCA-klauzula, ami a kutatásra/benchmarkolásra magára is vonatkozhat: a licenc-korlátozások közt szerepel *„(f) publish benchmarks or performance information about the Services"* tiltása (https://typesafe.ai/legal/mca) — azaz a TypeSafe szerződési feltételei szerint ügyfélként saját méréseket közzétenni a szolgáltatásról szerződésszegésnek minősülhet. Ez a rendszer-tervezés szempontjából releváns megkötés, ha valaki saját benchmarkot akarna publikálni a Jev-ről.

## 2. Az API: végpont, hitelesítés, kérés/válasz szerkezet, kérdéstípusok

Hivatalos API-referencia, szó szerint (https://docs.typesafe.ai/api):

```
POST https://api.typesafe.ai/v1/systemone
Authorization: Bearer <API_KEY>
Content-Type: application/json
```

- **Kérés mezői**: `state` (szöveg vagy strukturált JSON), `model` (pl. `"jev-latest"`), `questions` (map, kulcsonként egy típusos Question). Idézet: *„A map of typed Question objects. You choose each key; answers come back under the same keys."* (uo.) A kérdés-kulcs nem kerül a modellhez: *„The key is not sent to the underlying model and is not used in inference."*
- **Nincs más dokumentált top-level mező** — a hivatalos doksi request body-ja csak `state`/`model`/`questions`-t sorol, `temperature`, `seed`, `stream`, `system`, `max_tokens` nem szerepel egyikben sem (megerősítve az Introduction, Quick start és API reference oldalak mindegyikén, https://docs.typesafe.ai/introduction, /introduction/quickstart, /api).
- **Kérdéstípusok**, a hivatalos „Primitives" táblázatból szó szerint: *„Choice | Choose an option from a list | choice, probabilities, confidence” / „Score | Score the state on a rubric | score, probabilities, confidence” / „Noul | Is this statement true? | noul (0–1)"* (https://docs.typesafe.ai/introduction, „TypeSafe primitives" táblázat).
  - **Choice**: `criteria` — *„A map of option to rubric description; use null when an option needs no extra detail. You can have a maximum of 255 options per Choice."* (https://docs.typesafe.ai/api)
  - **Score**: `criteria` — *„An ordered array of level descriptions... A Score should have at least two levels; the API accepts up to 10."* (uo.)
  - **Noul**: nincs kötelező `criteria`, csak opcionális `{"true": ..., "false": ...}` leírás a yes/no jelentéséről (uo.)
  - `instructions` (és Choice/Score esetén az opció-/szintleírások) lehetnek string, JSON objektum vagy tömb is — strukturált kérdésmegfogalmazásra (https://docs.typesafe.ai/primitives/advanced).
- **Több kérdés egy hívásban**: igen, tetszőleges számú, vegyesen Choice/Score/Noul, egy state-re, párhuzamosan kiértékelve. Idézet: *„All three question types can be mixed in a single API call. Every question is evaluated in parallel and in isolation against the same state in one go. Adding questions barely changes the response time."* (https://docs.typesafe.ai/introduction)
- **Válasz szerkezete** — egy konkrét, hivatalos példa (Quick start oldal):
```json
{
  "model": "jev-1.13.0",
  "answers": {
    "department": {"type":"choice","choice":"technical","confidence":0.78,
       "probabilities":{"technical":0.85,"sales":0.0,"billing":0.15}},
    "frustration": {"type":"score","score":1.0,"confidence":1.0,
       "legend":{"0":"Calm...","1":"Frustrated...","2":"Very angry..."},
       "probabilities":{"0":0.0,"1":1.0,"2":0.0}},
    "is_urgent": {"type":"noul","noul":1.0}
  },
  "usage": {"input_tokens": 392, "output_tokens": 65}
}
```
(https://docs.typesafe.ai/introduction/quickstart) — Noul-válasznak **nincs** `confidence` mezője (csak Choice és Score kap): *„Every answer carries a type matching its question. Choice and Score answers also carry a confidence between 0 to 1... (Noul answers don't carry one.)"* (https://docs.typesafe.ai/api, https://docs.typesafe.ai/confidence).
- **Modell-lista végpont**: `GET https://api.typesafe.ai/v1/models` — *„returns the names your account can send in the model field, with a description and release date for each. It currently lists the aliases. Versioned IDs such as jev-1.13.0 are accepted... whether or not they appear in the list."* (https://docs.typesafe.ai/models)
- **Nincs dokumentált streaming, batch vagy async endpoint.** Ezt a TypeSafe saját doksija sem közli explicit tiltásként, de az API reference egyáltalán nem sorol fel ilyen mezőt/végpontot; egy harmadik fél API-referencia-oldal (learnjev.com/reference, T3) ezt ki is mondja: *„There is no streaming, batch or async job endpoint."* — ezt a hivatalos doksik hallgatólagosan megerősítik (nincs ellenkező adat), de mivel maga a TypeSafe sosem mondja ki „nincs streaming" formában, ezt csak közvetve, egy T3 forrás explicit állításával tudom alátámasztani.

## 3. Kontextusméret (a „state" maximális hossza)

Hivatalos Models oldal, szó szerint: *„Context length: 64k tokens per request; 32k tokens for `state` plus the longest question."* (https://docs.typesafe.ai/models) — azaz a teljes kérés (state + minden kérdés összesen) 64 000 tokenig mehet, de magának a state-nek és az egyetlen leghosszabb kérdésnek együtt 32 000 tokenen belül kell maradnia.

**Egy memóriabejegyzés + 5–20 kategórialeírás elfér-e?** A hivatalos dokumentáció nem ad konkrét token-számot egy „átlagos" memóriabejegyzésre vagy kategórialeírásra, tehát ez számszerűen **NINCS FORRÁS**; de a 64k/32k-s keret nagyságrendileg (kb. 45 000–50 000 angol szónyi szöveg 64k tokenben) bőven elég egyetlen memóriabejegyzés + 20, néhány mondatos kategórialeírás befogadására, feltéve hogy a kategóriák Choice `criteria` mezőjébe kerülnek (max. 255 opció is belefér a Choice-limitbe).

**Ellentmondás a gateway-ekkel**: A Cloudflare hivatalos Workers AI modell-oldala szerint *„Context Window ↗ | 32,000 tokens"* (https://developers.cloudflare.com/ai/models/typesafe/jev/), az OpenRouter hivatalos modell-oldala szerint *„Context | 32K"* (https://openrouter.ai/typesafe/jev-1.13) — mindkettő csak 32k-t hirdet, szemben a TypeSafe saját 64k-s számával. Egy harmadik fél összehasonlító oldal (jevaiguide.com/channels/, T3) ezt így magyarázza és teszi próbára: *„OpenRouter and Cloudflare both list a 32,000-token context window. TypeSafe documents 64k per request, with the same 32k cap on the state plus the longest question. In our tests, TypeSafe rejected a state of about 33,600 tokens with `max_tokens_exceeded`, so in practice the usable state size is similar everywhere."* — ez arra utal, hogy a gyakorlati korlát ténylegesen ~32k lehet, és a TypeSafe „64k" száma talán csak elméleti/ritkán elérhető felső határ, de ezt két T1 gateway-oldal és egy T3 teszt állítja, maga a TypeSafe sosem ismeri el a diszkrepanciát — lásd Ellentmondások.

## 4. Determinizmus

A hivatalos doksi nem ígér szigorú determinizmust, de „stabilitást" igen. Idézet a „How to build with TypeSafe" oldalról: *„System One is designed to return stable answers across repeated evaluations. See the self-consistency cookbook."* (https://docs.typesafe.ai/concepts/how-to-build-with-system-one)

A hivatkozott, szintén hivatalos cookbook (Self-consistency: nouls, https://docs.typesafe.ai/cookbooks/consistency_noul_cookbook) egy 14 Noul-kérdéses rubrikát futtat 15-ször ugyanarra az állapotra, `jev-latest` modellel, és ezt írja: *„TypeSafe: one `system_one` call over the 14 Noul questions, with a fresh `uid` field (a throwaway unique value) on each call... TypeSafe's mean per-question probability standard deviation is 0.0102, below all LLM probability conditions here. Its `covered` answers span 0.43 to 0.53, crossing a 0.5 decision threshold."* Ez két dolgot jelent: (1) a Jev valószínűségei **nem tökéletesen determinisztikusak** (van szórás, és van olyan eset, ahol a szórás át is lép egy döntési küszöböt), (2) de a szórás mértéke a hivatalos teszt szerint kisebb, mint a hasonlított LLM-eké (Claude Haiku 4.5, GPT-5.4-mini, GPT-5.5, Claude Opus 4.8), akár `temperature=0` beállítás mellett is.

**Nincs kitett `seed` vagy `temperature` paraméter** a hivatalos API-ban — ez maga is közvetett bizonyíték arra, hogy a gyártó nem kínál felhasználói szintű determinizmus-vezérlést; erről explicit tiltó/magyarázó mondatot a hivatalos doksiban nem találtam, tehát a „miért nincs seed" kérdésre **NINCS FORRÁS** (csak az figyelhető meg, hogy a mező hiányzik a sémából).

## 5. Késleltetés

Gyártói állítás, szó szerint a bejelentő blogból: *„End-to-end response time is 70ms-500ms for TypeSafe. This can range from 40x-200x faster for the same levels of frontier intelligence for System One shaped queries."* (https://typesafe.ai/blog/introducing-system-one-models-and-jev)

Mérési feltétel, amit a TypeSafe maga is önkritikusan megjegyez: *„Speed per call: We truly are that fast, though our published evals are generally run from our laptops on the West Coast (this is where our service is currently based)."* (uo., „Evidence / Technical Results" szakasz) — azaz a saját publikált méréseik földrajzilag torzítottak (közel a szerverekhez), és ezt a cég maga is elismeri.

A „workflow evals" (a 193,6×/444,6× szám eredete) szintén saját, belső csapat által készített teszt: *„This is where the claims of 193.6x faster, 444.6x cheaper on our home page comes from... These content of these workflows were not deliberately chosen nor constructed to make our model look good... however, they were made by individuals on our model capabilities team, so some bias could exist."* (uo.) — ez a gyártó saját torzítás-beismerése.

**Független, gateway-en át mért, publikált latency-szám**: az OpenRouter modell-oldalán a „Latency" oszlop kitöltetlen (`--`) a Jev egyetlen providerénél: *„| TypeSafe | $0.042 | Free | -- | 100.00% |"* (https://openrouter.ai/typesafe/jev-1.13) — vagyis OpenRouternek **nincs** publikált, mért latency-adata erre a modellre; a Vercel AI Gateway providerek-táblájában is üres a „Latency" és „Throughput" oszlop a `typesafe-ai/jev` sorban (https://vercel.com/ai-gateway/models/providers/typesafe-ai). **NINCS FORRÁS** tehát egyetlen gateway hivatalos, mért (nem gyártói) latency-számára sem. Az egyetlen konkrét, nem-TypeSafe említésű gyorsulási adat egy Vercel-mérnök egyedi, nem kontrollált felhasználói tapasztalata (5–18×, sq00-ban már idézve, TechCrunch, 2026-09-18) — ez nem szigorú benchmark, csak egyetlen fejlesztő egyetlen use case-e.

## 6. Korlátok: rate limit, egyidejűség, kvóták, hibakódok

**Rate limit / kvóta**, hivatalos Models oldal: *„Rate limits | 250,000 tokens per second / 1,200 requests per minute"* és *„Rate limits are adjusting dynamically. We are serving a very large volume of demand, and the limits above can change without notice while we do... Higher limits are available on custom and enterprise plans."* (https://docs.typesafe.ai/models) — tehát a limitek explicit módon **instabilak/ideiglenesek** az early access alatt, vállalati tervben magasabbak elérhetők.

**Egyidejűség (concurrency)**: külön, konkrét egyidejű-kapcsolat-limitre **NINCS FORRÁS** a hivatalos doksiban — csak a fenti token/mp és kérés/perc szám van dokumentálva, explicit „concurrent requests" mező nélkül.

**Hibakódok**, hivatalos API reference, teljes tábla, szó szerint (https://docs.typesafe.ai/api):

| Kód | Jelentés (hivatalos szöveg) |
|---|---|
| `401 Unauthorized` | „Missing or invalid API key. Check the Authorization header." |
| `422 Unprocessable Entity` | „The request body failed validation — for example a missing required field or a malformed question. The body details the offending field." |
| `429 Too Many Requests` | „You have exceeded your rate limit. Back off and retry after a short delay." |
| `529 Overloaded` | „TypeSafe is temporarily overloaded. Retry after a short delay." |

Retry-ajánlás, szintén hivatalos: *„When you receive a 429 Too Many Requests or 529 Overloaded response, retry the request with exponential backoff instead of retrying immediately. Our client SDKs handle this automatically."* (uo.)

**Dokumentációs rés / belső feszültség**: a hivatalos JavaScript SDK saját API-referenciája (https://docs.typesafe.ai/sdk/javascript/api, `llms.txt` indexből) ennél több hibaosztályt definiál: `APIConnectionError`, `APIError`, `APITimeoutError`, `APIUserAbortError`, `AuthenticationError`, `BadRequestError` (HTTP 400), `InternalServerError` (HTTP 500), `NotFoundError` (HTTP 404), `PermissionDeniedError` (HTTP 403), `RateLimitError` (HTTP 429), `UnprocessableEntityError` (HTTP 422) — azaz a kliens-oldali kód négynél több HTTP-státuszra készül fel, jóllehet az API-referencia csak négyet dokumentál. Ez tehát **jogosultság** (401 `AuthenticationError`, 403 `PermissionDeniedError`), **kvóta/rate limit** (429 `RateLimitError`), **túlterhelés** (529, HTTP API-referenciában) és **szerverhiba** (500 `InternalServerError`, csak az SDK-ban dokumentált) kategóriákra is ad valamilyen szintű támpontot — de a szerverhiba (500) és a 400/403/404 hivatalosan, az API-referencia szintjén nincs dokumentálva, csak az SDK forráskódjában/típusaiban jelenik meg. Ezt egy T3 forrás (learnjev.com/reference) is megerősíti: *„The SDKs also define 400, 403 and 404 errors, which do not appear in the HTTP API's documented table."*

## 7. Rendelkezésre állás: státuszoldal, SLA, kiesés-történet

**Van hivatalos, publikus státuszoldal**: https://status.typesafe.ai — 2026-09-16-i állapotban (ez volt a legutolsó frissítés, amit az Exa le tudott kérni) két szolgáltatást követ:
- `api.typesafe.ai` (TypeSafe API Availability): **99,858% uptime**, a megjelenített napi sávban (2026-06-19 – 2026-09-16) tucatnyi rövid (2–59 perces) kieséssel dokumentálva (pl. „Down for 59 minutes" 2026-08-03-án, „Down for 18 minutes" 2026-07-10-én).
- `console.typesafe.ai` (fejlesztői konzol): **99,985% uptime**, hasonlóan részletezett kiesés-naplóval.

**Nincs publikált, számszerű SLA-ígéret.** A hivatalos Master Customer Agreement „Service Warranty" pontja csak annyit ígér, hogy a szolgáltatás „materially" a dokumentáció szerint fog működni, és kifejezetten kizárja a megszakítás-mentesség garantálását: *„TYPESAFE DOES NOT WARRANT THAT CUSTOMER'S USE OF THE SERVICES WILL BE UNINTERRUPTED OR ERROR-FREE... TYPESAFE IS NOT LIABLE FOR DELAYS, FAILURES, OUTAGES, DECREASED FUNCTIONALITY, NON-PERFORMANCE, UNAVAILABILITY OF THE SERVICES..."* (https://typesafe.ai/legal/mca, 9. szakasz). A preview/early-access felhasználói feltételek (Terms of Service) még explicitebbek: *„the Interfaces are not designed for use in connection with business-critical infrastructure"* és *„TYPESAFE DOES NOT GUARANTEE THAT USER'S ACCESS TO THE INTERFACES WILL BE UNINTERRUPTED."* (https://typesafe.ai/terms-and-conditions) — ugyanitt egy 50 dolláros felelősségi felső korlát is szerepel a preview-hozzáférésre: *„AGGREGATE TOTAL DAMAGES OR LIABILITY OF ANY KIND IN EXCESS OF $50 USD."*

Egy független (nem hivatalos) jogi elemzés ugyanerre a következtetésre jut, és ezt tömören össze is foglalja: *„No SLA. Support is commercially reasonable efforts by email. That is the whole commitment."* (https://wunderlandmedia.com/typesafe-ai-jev-terms-of-service-gdpr, T3, de közvetlenül a hivatalos MCA/ToS szövegére hivatkozva, és ezt magam is megerősítettem a fenti T1-idézetekkel).

**Adatmegőrzés / ZDR**: hivatalos Models oldal: *„Jev is not trained on customer requests or responses. See Legal for the Data Processing Agreement, the Privacy Policy, and details on zero data retention (ZDR) for enterprise customers."* (https://docs.typesafe.ai/models) — a nulla adatmegőrzés csak vállalati ügyfeleknek elérhető, külön szerződéssel; ezt a hivatalos Privacy Policy nem ismétli meg explicit ZDR-formában, csak a betanítás-tilalmat: *„We will not train or fine tune any artificial intelligence or machine learning models on your prompts or other Input."* (https://typesafe.ai/legal/privacy-policy, utolsó frissítés: 2025-11-19).

**Trust Center** (https://trust.typesafe.ai/) létezik, de az oldal tartalma JavaScript-renderelt, az Exa `web_fetch_exa` eszköze üres törzset adott vissza — SOC 2 vagy egyéb tanúsítvány-státuszra emiatt **NINCS FORRÁS** ebben a körben.

## 8. SDK-k

Hivatalosan **két nyelven** van elsőfeles kliens:

- **Python**: `typesafe-sdk` csomag, PyPI-n publikálva, hivatalos szerző/karbantartó „TypeSafe AI" (support@typesafe.ai) és „Daniel Gafni" néven, repó: `github.com/typesafe-ai/typesafe-sdk-python` (https://pypi.org/project/typesafe-sdk/, https://pypi.org/project/typesafe-sdk/0.5.7/). Python ≥3.10 szükséges (https://docs.typesafe.ai/sdk/python). Változásnapló szerint az első nyilvános kiadás **v0.5.7 (2026-09-14)** volt: *„This is the initial public release of TypeSafe Python SDK."* (https://docs.typesafe.ai/sdk/python/changelog); azóta v0.6.0 (2026-09-15), v0.7.0 (2026-09-18, a szerializáló `msgspec`-ről `pydantic`-ra váltott — ez törő változás), v0.7.1 (2026-09-21) jelent meg.
- **JavaScript/TypeScript**: `@typesafe-ai/sdk` csomag, npm-en, Node.js ≥20 szükséges, ESM+CJS+TS deklarációkkal (https://docs.typesafe.ai/sdk/javascript). Changelog szerint az első nyilvános kiadás **v0.5.7 (2026-09-11)**, majd **v0.6.0 (2026-09-15)** egy törő változással (`Score.criteria` tömbként, nem objektumként) (https://docs.typesafe.ai/sdk/javascript/changelog). A hivatalos GitHub-repó neve `typesafe-ai/typesafe-sdk-js`, önleírása: *„The official TypeScript/JavaScript library for the TypeSafe API"* (elérve egy tükör-domainen keresztül: https://github.laiyagushi.com/typesafe-ai/typesafe-sdk-js — maga a github.com közvetlenül nem volt Exa-val elérhető, ezért ez csak T2-ként kezelendő, bár a tartalma megegyezik az npm-csomag leírásával).
- **Defenzív névfoglalás**: létezik egy `typesafe-ai` nevű PyPI-csomag is, de ez csak egy „redirect shim", saját leírása szerint: *„Redirect shim: the TypeSafe AI Python SDK is published as 'typesafe-sdk'. This package depends on it and re-exports its public API... This package was registered defensively so that name cannot be taken over."* (https://pypi.org/project/typesafe-ai/, nem TypeSafe által regisztrálva, hanem egy külső fejlesztő, Gerome Dexheimer által) — ez fontos, mert könnyen összetéveszthető a hivatalos csomaggal, de nem hivatalos.
- **Más nyelvek**: a hivatalos dokumentáció-index (`docs.typesafe.ai/llms.txt`) kizárólag Python és JavaScript SDK-fejezeteket sorol fel; **nincs hivatalos Go, Rust, Java stb. kliens**. Találtam több, kifejezetten **nem hivatalos** (közösségi) Rust klienst: `jev-sdk` (docs.rs/jev-sdk), `typesafe-jev` (docs.rs/typesafe-jev, saját magát is „unofficial”-ként... pontosabban nem állítja magáról hivatalosnak, csak a TypeSafe API-referenciájára hivatkozik mezőről mezőre) és `jevapi` (explicit: *„An unofficial asynchronous Rust binding for the TypeSafe AI HTTP API"*, https://docs.rs/crate/jevapi/latest/source/README.en.md) — egyik sem a TypeSafe saját GitHub-szervezete alatt van.
- **Agent-skill Claude Code / Codex / más agentekhez**: a TypeSafe hivatalosan publikál egy „agent skill"-t, ami a projekt szempontjából (Codex/Claude támogatás) direkt releváns: *„claude plugin marketplace add typesafe-ai/skills"* + *„claude plugin install typesafe@typesafe-ai"*, illetve más agentekhez *„npx skills add typesafe-ai/skills --skill typesafe-ai"* (https://docs.typesafe.ai/agent-skill). Ez nem egy „modell-SDK" a szó szigorú értelmében, hanem egy promptolási/dokumentációs csomag, amit az agent (pl. Claude Code) tölt be, hogy helyesen írja meg a Jev-hívásokat.

## Ellentmondások

1. **Bejelentés dátuma**: a typesafe.ai blogoldal saját, látható dátumbélyege **„Sep 14, 2026"** (https://typesafe.ai/blog/introducing-system-one-models-and-jev), miközben a sq00-ban idézett több másodlagos forrás (Wikipédia, TechCrunch-idézet, jev.page: „Announced September 15, 2026") egységesen szeptember 15-öt ír. Ezt nem tudtam elsődleges forrásból feloldani — lehet időzóna-eltérés (pl. PT vs. UTC) vagy a blog utólagos dátum-módosítása.
2. **Kontextusablak mérete**: a TypeSafe saját hivatalos Models oldala 64 000 tokent ad meg (state+kérdések összesen), 32 000-et a state+leghosszabb kérdésre — ezzel szemben **két hivatalos gateway-oldal** (Cloudflare Workers AI modell-katalógus és OpenRouter modell-oldal) kizárólag **32 000 tokenes** kontextusablakot hirdet, a 64k-s felső korlátot nem is említve. Ez lehet, hogy a gateway-ek csak a szigorúbb (state+1 kérdés) számot vették át mint „context window", de ezt egyik gateway-dokumentáció sem magyarázza meg explicit módon.
3. **Rendelkezésre állás jellege**: a TypeSafe saját marketingje és blogja „early access"-ként, majd (harmadik felek szerint) „no waitlist"-ként írja le a jelenlegi állapotot, de több független, egymástól részben független forrás (jevmodel.org, jevaiguide.com) is megjegyzi, hogy *„TypeSafe has not clarified whether removing the waiting list means full general availability or an open beta"* — azaz maga a TypeSafe hivatalosan sosem jelentette be a „General Availability" (GA) állapotot, csak azt, hogy a várólista megszűnt. A „korlátlanul elérhető" és a „még mindig early access, csak épp önkiszolgáló regisztrációval" közötti különbség hivatalos forrásból nem dönthető el egyértelműen.
4. **Hivatalos hibakód-lista teljessége**: az API-referencia négy hibakódot dokumentál (401/422/429/529), miközben a hivatalos JS SDK saját típusdefiníciói további státuszokra (400/403/404/500) is kivétel-osztályt adnak — ez inkonzisztencia a TypeSafe két saját dokumentum-halmaza között (HTTP API-referencia vs. SDK-referencia), nem egy külső fél állítása.
5. **Gyártói sebesség-/pontosság-állítás vs. saját beismert torzítás**: a TypeSafe blog maga is elismeri, hogy a 193,6×/444,6×-os csúcsszámok „valószínűleg a valós tartomány felső határát" képviselik, saját („model capabilities") csapat által összeállított workflow-kon mérve — ez már a sq00-ban is szerepelt, itt csak megerősítést nyert az elsődleges forrás teljes szövegéből.

## Amire NINCS forrás

- Konkrét token-szám arra, hogy „egy tipikus memóriabejegyzés + 5–20 kategórialeírás" pontosan hány tokent tesz ki a Jev state-jében — a TypeSafe nem ad ilyen konkrét számítást vagy példát.
- Miért nincs kitéve `seed`/`temperature` paraméter az API-ban — a hivatalos doksi ezt nem indokolja, csak a mező hiánya figyelhető meg.
- Egyetlen gateway (OpenRouter, Vercel, Cloudflare) hivatalos, mért, publikált latency-száma a Jev-re — az OpenRouter és Vercel saját latency-oszlopai üresek/kitöltetlenek a Jev sorában.
- Explicit, dokumentált egyidejű kapcsolat- (concurrency-) limit a rate limiten felül.
- SOC 2 vagy egyéb biztonsági tanúsítvány-státusz a TypeSafe Trust Centeréből (az oldal JS-renderelt, tartalma nem volt lekérhető ezzel az eszközkészlettel).
- Hivatalos, TypeSafe általi „General Availability" bejelentés — csak a várólista megszűnése van megerősítve, a hozzáférési szint (early access / open beta / GA) pontos jogi-marketing besorolása nincs tisztázva elsődleges forrásból.
- Pontos ok/magyarázat arra, miért ad meg a TypeSafe 64k-s, a Cloudflare/OpenRouter pedig csak 32k-s kontextusablakot ugyanarra a modellre.

## Meglátogatott és felderített linkek

| Cím | URL | Tier | Eszköz | Megjegyzés |
|---|---|---|---|---|
| Introducing System One Models and Jev (TypeSafe blog) | https://typesafe.ai/blog/introducing-system-one-models-and-jev | T1 | Exa web_fetch_exa | Fő elsődleges forrás: sebesség, ár, evidence/technical results, FAQ, várólista-nyitás szövege |
| Introduction (docs) | https://docs.typesafe.ai (introduction.md) | T1 | Exa web_fetch_exa | Primitívák táblázata, alap architektúra-ábra |
| Quick start (docs) | https://docs.typesafe.ai/introduction/quickstart | T1 | Exa web_fetch_exa | Teljes kérés/válasz JSON-példa, curl, Python SDK, agent-skill telepítés |
| API reference (docs) | https://docs.typesafe.ai/api | T1 | Exa web_fetch_exa (llms-full.txt) | Teljes kérés/válasz séma, hibakód-tábla |
| Models (docs) | https://docs.typesafe.ai/models | T1 | Exa web_fetch_exa | Kontextushossz, rate limit, ár, aliasok, nyelvtámogatás, ZDR-utalás |
| State (docs) | https://docs.typesafe.ai/concepts/state | T1 | Exa web_fetch_exa | State formátumok, nyelvi pontosság-megjegyzés |
| System One (docs) | https://docs.typesafe.ai/concepts/system-one | T1 | Exa web_fetch_exa | Fogalmi keret, Kahneman-hivatkozás |
| Confidence (docs) | https://docs.typesafe.ai/confidence | T1 | Exa web_fetch_exa | Confidence számítás, Noul kivétel |
| How to build with TypeSafe (docs) | https://docs.typesafe.ai/concepts/how-to-build-with-system-one | T1 | Exa web_fetch_exa (llms-full.txt) | Determinizmus-állítás, teljes triage-kód példa |
| Self-consistency: nouls (cookbook) | https://docs.typesafe.ai/cookbooks/consistency_noul_cookbook | T1 | Exa web_fetch_exa | Determinizmus empirikus mérése (szórás 0,0102) |
| JavaScript SDK (docs) | https://docs.typesafe.ai/sdk/javascript | T1 | Exa web_fetch_exa | Hivatalos npm-csomag, kód-példa |
| JS SDK changelog | https://docs.typesafe.ai/sdk/javascript/changelog | T1 | Exa web_fetch_exa | Verziótörténet, v0.5.7 első kiadás dátuma |
| Python SDK changelog | https://docs.typesafe.ai/sdk/python/changelog | T1 | Exa web_fetch_exa | Verziótörténet, v0.5.7 első kiadás dátuma |
| RateLimitError osztály (JS SDK ref) | https://docs.typesafe.ai/sdk/javascript/api/classes/RateLimitError | T1 | Exa web_fetch_exa | SDK hibaosztály-részletek |
| Agent skill (docs) | https://docs.typesafe.ai/agent-skill (llms-full.txt) | T1 | Exa web_fetch_exa | Claude Code / más agentek hivatalos skillje |
| Documentation index | https://docs.typesafe.ai/llms.txt | T1 | Exa web_fetch_exa | Teljes doksi-térkép (gépi olvasható) |
| Full documentation dump | https://docs.typesafe.ai/llms-full.txt | T1 | Exa web_fetch_exa | Több oldal teljes szövege egy fájlban |
| Typesafe AI status | https://status.typesafe.ai | T1 | Exa web_fetch_exa | Uptime %, kiesés-napló mindkét szolgáltatásra |
| TypeSafe console (bejelentkezés) | https://console.typesafe.ai | T1 | Exa web_fetch_exa | Ma (2026-09-25) önkiszolgáló login, várólista-űrlap nélkül |
| Master customer agreement | https://typesafe.ai/legal/mca | T1 | Exa web_fetch_exa / web_search_exa | Service Warranty, SLA hiánya, license-korlátozások, benchmark-tiltás |
| Privacy policy | https://typesafe.ai/legal/privacy-policy | T1 | Exa web_fetch_exa | „nem tréníroz Input-on" idézet, adatgyűjtés részletei |
| Data processing addendum | https://typesafe.ai/legal/data-processing | T1 | Exa web_search_exa (highlight) | Megőrzési idő megfogalmazása, biztonsági incidens 72 órás bejelentés |
| Terms of Service (preview) | https://typesafe.ai/terms-and-conditions | T1 | Exa web_search_exa (highlight) | $50-os felelősségi korlát, „not... business-critical infrastructure" |
| Trust Center | https://trust.typesafe.ai/ | T1 | Exa web_fetch_exa | Tartalom nem volt kinyerhető (JS-renderelt), csak a cím jött le |
| Jev 1.13 — OpenRouter modell-oldal | https://openrouter.ai/typesafe/jev-1.13 | T2 | Exa web_fetch_exa | Kontextus 32K, ár, üres latency-oszlop, release dátum Sep 18 |
| Jev Documentation — OpenRouter | https://openrouter.ai/docs/guides/community/jev | T2 | Exa web_search_exa (highlight) | Decisions API + System One API surface, FAQ |
| Jev — Vercel AI Gateway modell-oldal | https://vercel.com/ai-gateway/models/jev | T2 | Exa web_fetch_exa | „Context window: Not applicable”, ár |
| TypeSafe AI's Jev now available on AI Gateway (Vercel changelog) | https://vercel.com/changelog/typesafe-ai-jev-now-available-on-ai-gateway | T2 | Exa web_fetch_exa | AI SDK 7 evaluate API, ZDR/No Training providerOptions |
| TypeSafe API with AI Gateway (Vercel docs) | https://vercel.com/docs/ai-gateway/sdks-and-apis/typesafe | T2 | Exa web_search_exa (highlight) | Hivatalos SDK-t hogyan kell gateway-re irányítani |
| TypeSafe AI models (Vercel provider oldal) | https://vercel.com/ai-gateway/models/providers/typesafe-ai | T2 | Exa web_search_exa (highlight) | Üres latency/throughput oszlopok, release dátum 09/15/2026 |
| Jev (typesafe) — Cloudflare Workers AI | https://developers.cloudflare.com/ai/models/typesafe/jev/ | T2 | Exa web_search_exa (highlight) | Kontextusablak 32 000 token |
| Cloudflare AI Gateway overview | https://developers.cloudflare.com/ai-gateway/ | T2 | Exa web_fetch_exa | Általános gateway-funkciók (rate limiting, caching stb.) |
| typesafe-sdk — PyPI | https://pypi.org/project/typesafe-sdk/ | T2 | Exa web_search_exa (highlight) | Hivatalos csomag, GitHub-repó, licenc |
| typesafe-sdk v0.5.7 — PyPI | https://pypi.org/project/typesafe-sdk/0.5.7/ | T2 | Exa web_search_exa (highlight) | Első kiadás metaadatai |
| typesafe-ai — PyPI (shim) | https://pypi.org/project/typesafe-ai/ | T2 | Exa web_search_exa (highlight) | Nem hivatalos, defenzív névfoglalás-csomag |
| typesafe-sdk-js — GitHub (tükör) | https://github.laiyagushi.com/typesafe-ai/typesafe-sdk-js | T2 | Exa web_search_exa (highlight) | „official... library” önleírás, tükrözött github.com tartalom |
| Jev API reference — Learn Jev | https://learnjev.com/reference | T3 | Exa web_search_exa (highlight) | Kiegészítő részletek (nincs streaming/batch endpoint, SDK-konstansok) |
| Jev API: Endpoint, Request Format and Responses — jevaiguide.com | https://jevaiguide.com/jev-api/ | T3 | Exa web_search_exa (highlight) | Konkrét hibaüzenet-példák (400/401/403/422 body) |
| How to use the Jev API — jevtypesafeai.com | https://www.jevtypesafeai.com/how-to-use | T3 | Exa web_search_exa (highlight) | Nem hivatalos, de a hivatalos sémát követő példakód |
| Jev Channels Compared — jevaiguide.com | https://jevaiguide.com/channels/ | T3 | Exa web_search_exa (highlight) | Csatorna-összehasonlító tábla, saját teszt a 32k/64k eltérésről |
| Jev on Cloudflare Workers AI — jevaiguide.com | https://jevaiguide.com/channels/cloudflare-workers-ai/ | T3 | Exa web_search_exa (highlight) | Cloudflare-specifikus hívási mód |
| Does Jev Train on Your Data? — jevaiguide.com | https://jevaiguide.com/faq/does-jev-train-on-your-data/ | T3 | Exa web_search_exa (highlight) | ZDR-összefoglaló, csatornánkénti adatkezelés-tábla |
| TypeSafe AI: The Company Behind Jev — jevaiguide.com | https://jevaiguide.com/typesafe-ai/ | T3 | Exa web_search_exa (highlight) | Legal-oldalak összefoglalása |
| TypeSafe AI Jev Terms of Service: EU Read — Wunderlandmedia | https://wunderlandmedia.com/typesafe-ai-jev-terms-of-service-gdpr | T3 | Exa web_search_exa (highlight) | Jogi (nem hivatalos) elemzés: SLA hiánya, felelősségi korlátok táblázata |
| TypeSafe drops the Jev waitlist — Jev News | https://jevainews.com/news/jev-no-waitlist/ | T3 | Exa web_search_exa (highlight) | @typesafeai 09-20 poszt idézése, $5 kredit |
| Jev Waiting List Is Gone — AI Profit Boardroom / bestaiagentcommunity | https://bestaiagentcommunity.com/blog/jev-waiting-list/ | T3 | Exa web_search_exa (highlight) | Várólista-idővonal (2026-09-15 → 09-21) |
| Jev Waiting List: Every Question Answered — Julian Goldie | https://juliangoldieaiautomation.com/blog/jev-waiting-list/ | T3 | Exa web_search_exa (highlight) | Ugyanattól a szerzőtől, mint az előző — csak részlegesen független |
| How I Skipped The Jev Waiting List — AI Profit Boardroom | https://aiprofitboardroom.com/blog/jev-waiting-list/ | T3 | Exa web_search_exa (highlight) | Csatorna-hozzáférési tábla (TypeSafe/OpenRouter/Vercel/Cloudflare) |
| Get Jev Access — jevmodel.org | https://jevmodel.org/get-jev/ | T3 | Exa web_search_exa (highlight) | „TypeSafe has not clarified... GA or open beta” megjegyzés |
| Thread By @typesafeai — unrollnow.com (X-archívum) | https://www.unrollnow.com/status/2101786156572823624 | T1 (archívumon át) | Exa web_search_exa (highlight) | Az official @typesafeai poszt szövege archiválva |
| @typesafeai poszt — bittide.aicompass.dev (cache) | https://bittide.aicompass.dev/article/deb4ee1f-54b0-45b3-b37f-aeb49e18eb12 | T1 (archívumon át) | Exa web_search_exa (highlight) | Ugyanaz a poszt, más cache-szolgáltatótól |
| Jev 101 — jev.page | https://jev.page/ | T3 | Exa web_search_exa (highlight) | „Official X, Sep 20: no waitlist” összegzés |
| Jev pricing, providers, and specs — Models.dev | https://models.dev/models/typesafe/jev-latest/ | T3 | Exa web_search_exa (highlight) | Csatornánkénti kontextus/ár összehasonlító tábla |
| Jev pricing, providers, and specs — models.opencode.ai | https://models.opencode.ai/models/typesafe/jev-latest/ | T3 | Exa web_search_exa (highlight) | Ugyanaz az adatbázis, tükör |
| ChatGPT Co-Creator Launches Jev — VKTR | https://www.vktr.com/ai-platforms/chatgpt-cocreator-launches-typesafe-ai-with-jev/ | T2 | Exa web_search_exa (highlight) | @typesafeai 09-15 launch-poszt idézése |
| TypeSafe's Jev hits 13% of Vercel paid teams — AI Weekly | https://aiweekly.co/alerts/typesafes-jev-hits-13-of-vercel-paid-teams-in-24-hours | T2 | Exa web_search_exa (highlight) | Vercel adopciós statisztika, Forbes-hivatkozással |
| jev_sdk — Rust (docs.rs) | https://docs.rs/jev-sdk/latest/jev_sdk/ | T3 | Exa web_search_exa (highlight) | Nem hivatalos Rust kliens |
| typesafe_jev — Rust (docs.rs) | https://docs.rs/typesafe-jev/latest/typesafe_jev/ | T3 | Exa web_search_exa (highlight) | Nem hivatalos Rust kliens, mezőnként a hivatalos referenciát követi |
| jevapi — Rust (docs.rs) | https://docs.rs/crate/jevapi/latest/source/README.en.md | T3 | Exa web_search_exa (highlight) | Explicit „unofficial” Rust kliens |

---

# SQ02 — Mennyire pontos és megbízható a Jev döntése

*Módszer: kizárólag Exa (`web_search_exa`, `web_fetch_exa`), a `_kozos.txt` és a `deep-web-research` skill elvei szerint. Alügynök-indítás (a skill teljes, több-ügynökös pipeline-ja) ebben a körben sem történt — egyszemélyes, de Exa-only, elsődleges forrásokra törekvő kutatás, a `sq00-azonositas.md` kontextusára építve. Minden számot a forrás nyelvén, szó szerint idézek; ahol a szám csak másod-/harmadkézből érhető el, azt jelzem.*

## Rövid válasz

A TypeSafe egyetlen saját mérést tett közzé induláskor (2026-09-15): egy 4 munkafolyamatos ("workflow eval") tesztet, ahol a referenciaválasz **két másik modell (GPT-6 Astra és Claude Fable 5.1, „high thinking") átlaga**, nem emberi igazság — ezen a mércén a Jev összesített egyezése 67,8%, szemben a GPT-5.6 Sol 74,1%-ával, számlafeldolgozásnál pedig 61,8% a 79,1%-hoz képest; ezt a négy számot legalább hat egymástól független forrás (TechSpot és öt másik elemzés) egyezően idézi. Kalibrációra (ECE, Brier, reliability diagram) a TypeSafe **nem tett közzé semmilyen saját mérőszámot** — ezt egy független elemzés kifejezetten hiányként nevesíti —, a közösségi mérések pedig adatfüggően hol jól, hol rosszul kalibráltnak találták a modellt, és legalább egy 16-modelles összevetésben egy általános célú frontier-LLM (Claude Sonnet 5) jobban kalibrált volt nála ugyanazon a feladaton. Többosztályos (5–20 címkés) besorolásra van adat: 7 osztályon 97,9%, 9 osztályos japán hírtéma-besoroláson 76,8% (egy kis, 250 mintán tanított enkóder itt 12 ponttal jobb volt), 6 kategórián 87,5%; a tartományon kívüli, de releváns Banking77 (77 osztály) feladaton 76–80,3% között mozgott, és több kis, illetve frontier LLM is megelőzte. Angol nyelvű mérés bőven van, **magyarra nincs forrás** — egyetlen Jev-specifikus magyar nyelvi tesztet vagy akár csak említést sem találtam; más nyelvekre (orosz, spanyol, kínai, koreai, japán, német) szórt adatok egyöntetűen nyelvváltáskor bekövetkező pontosságesést mutatnak. Ismert hibamódokra sok adat van: a TypeSafe saját dokumentációja kilenc hibamódot sorol fel (szó szerinti értelmezés, aritmetika, dátumösszehasonlítás, indirekció, irreleváns adattal túlterhelt állapot, ellenséges tartalom, ellentmondó instrukció/kritérium, strukturális következetlenség, generálásigény), és független mérések is dokumentáltak magabiztos, de téves választásokat (≥90%-os konfidencia mellett is), hosszú bemenetnél/elmosódott címkéknél bekövetkező pontosságesést, valamint hasonló/átfedő opciók közti szisztematikus tévesztést. Kifejezett „ellentmondó állítás Noul-lal" tesztet nem találtam, de a TypeSafe saját, publikált példája mutatja, hogy ugyanaz a tény Noul-ként és Choice-ként kérdezve homlokegyenest ellentétes választ ad, és két, egymás logikai tagadásának szánt Noul-válasz összege nem ad ki 1-et. Frontier LLM-hez képest a Jev jellemzően „középkategóriás" modellekkel egy szinten van és 6,5–11,5 ponttal lemarad a csúcsmodellektől; kis, saját adaton tanított helyi osztályozóhoz (BERT-típusú enkóder) képest 200–300 címkézett példa felett a helyi modell rendszeresen jobb és gyorsabb; tiszta, tanítás nélküli koszinusz-hasonlóságú beágyazás-osztályozóval való számszerű összevetést nem találtam — csak minőségi állításokat arról, hogy ez „kategóriahiba", mert az embedding önmagában nem válaszol kérdésre.

## 1. Pontossági mérések: gyártói teszt és a TechSpot-számok eredete

### 1.1 A TypeSafe saját („workflow eval") mérése

A hivatalos bejelentő blogposztban (typesafe.ai, 2026-09-15, szerző Diogo Almeida) a cég maga írja le a módszertant:

> „We made a new type of evaluation to measure how well AI works within code. We don't optimize for a ground truth classification […] Instead, we assume there is a correct compute graph (a 'workflow' represented in code) and use the predictions of the largest, smartest, and most expensive external models as reference probabilities. Rephrased: every model gets the same workflow. We test how they compare to the average of the smartest models (in this case, Astra and Fable)."
(https://typesafe.ai/blog/introducing-system-one-models-and-jev, T1)

Vagyis a „pontosság" itt **nem emberi/objektív igazsághoz**, hanem **két másik modell (GPT-6 Astra és Claude Fable 5.1, „high thinking" módban) válaszainak átlagához** viszonyított egyezés. A blog saját maga is jelzi a torzítást:

> „We use the average of GPT-6 Astra and Fable 5.1 as the reference answer, which biases answers towards OpenAI and Anthropic's models. We likely underestimate the relative performance of our model and DeepSeek's models." (uo., T1)

A blog a konkrét számtáblát nem az oldal szövegében, hanem egy külön „workflow evals site"-on közli (erre a blog hivatkozik: „See our workflow evals site for all the details"), amit Exa-val nem sikerült közvetlenül lekérni (a `typesafe.ai/evals` és a `typesafe.ai/models` URL is `CRAWL_NOT_FOUND` hibát adott — ugyanaz a probléma, mint a `sq00-azonositas.md`-ben dokumentált `typesafe.ai/models` esetén).

### 1.2 A „67,8% vs. 74,1%" és „61,8% vs. 79,1%" szám eredete és jelentése

A TechSpot cikke (2026-09-20, Julio Franco) közvetlenül idézi ezt a táblázatot:

> „The benchmarks are TypeSafe's own. The company skipped public leaderboards. Its workflow tests score models by agreement with the averaged answers of GPT-6 Astra and Fable 5.1, not against verified ground truth. By that measure, Jev reached about 67.8% agreement overall versus 74.1% for GPT-5.6 Sol. It came close on customer service (76% versus 78.3%) and fell well behind on invoice processing (61.8% versus 79.1%)."
(https://www.techspot.com/article/3172-meet-jev/, T2)

Tehát a szám pontos jelentése: **egyezés (agreement) a GPT-6 Astra + Claude Fable 5.1 átlagával, mint referenciaválasszal**, nem külső, emberi igazsághoz mért pontosság. A négy szám (67,8% / 74,1% / 61,8% / 79,1%) legalább öt további, egymástól független forrásban is megjelenik, azonos értékekkel:

- **dev.to (aws-builders, 2026-09-24)**: „Eval accuracy. Reference labels are 'an average of the responses of GPT-6 Astra and Claude Fable 5.1, both at high thinking', so accuracy there means agreement with two LLMs. Jev scores 67.8%, equal to Sonnet 5, with GPT-5.6 Sol leading at 74.1%. On invoice processing Jev scores 61.8% against Sol's 79.1%." (T2)
- **benchlm.ai**: „Its workflow evaluations, scored against the average of GPT-6 Astra and Claude Fable 5.1 at high thinking, put Jev at 67.8 percent agreement and GPT-5.6 Sol at 74.1, averaging four workflows with equal weight. These are agreements with model-generated labels, not human-scored accuracy." (T2)
- **agenccy.ai**: „Averaged across four workflows, Jev scores 67.8%. That places it behind Sol at 74.1% and Opus 5 at 73.1%, level with Terra at 67.9% and tied with Sonnet 5, also 67.8%. […] The reference labels were 'generated via an average of the responses of GPT-6 Astra and Claude Fable 5.1, both at high thinking' — so accuracy here measures agreement with two frontier models, which are also the models Jev is marketed against." (T2)
- **bug.hr (horvát, 2026-09-22)** táblázatban közli ugyanezt (Jev 67,8%, GPT-5.6 Luna 66,8%, GPT-5.6 Terra 67,9%, Claude Sonnet 5 67,8%, Claude Opus 5 73,1%, GPT-5.6 Sol 74,1%) és hozzáteszi: „Test je izradio TypeSafeov tim, a 'točan odgovor' je prosjek odgovora GPT-6 Astre i Fablea 5.1. Jev se dakle ne mjeri prema stvarno točnim odgovorima, nego prema tome koliko se slaže s velikim modelima." (T3, de a tartalom megegyezik a T1/T2 forrásokéval)
- **datasciocean.com (kínai, 2026-09-22)**: „這張表裡 67.8% 一致率的『參考答案』不是人工標註的真值（ground truth），而是用 GPT-6 Astra 跟 Fable 5.1 兩個模型的平均答案當標準答案。" (T2/T3)

**Fontos árnyalat**, amit az agenccy.ai és a benchlm.ai is kiemel: a TypeSafe táblázatában minden más modell **kétszer** szerepel (egyszer „workflow" — lebontott, kód-vezérelt — módban, egyszer „prompt" módban, ahol egy generált promptban maga végzi a láncolt logikát, és ez utóbbiban lényegesen rosszabbul teljesít), miközben a Jevnek nincs „prompt" sora, mert szerkezetileg nem futtatható úgy. A horvát cikk saját számítást is közöl arra, hogy a lebontás (a workflow-formátum) önmagában mennyit javít: „Svaki model u prosjeku je točniji kad je zadatak rastavljen, a najveća je razlika kod Claude Haikua 4.5 (53,6 prema 18,1 posto)." — vagyis a nyereség jó része nem a Jev modellből, hanem a feladat lebontásából ered.

### 1.3 Független mérések listája (fő pontossági eredmények)

| Forrás | Módszer | Fő eredmény |
|---|---|---|
| Aman Kumar blogja (amankumar.ai, 2026-09-18, T2) | ~16 000 API-hívás, 4 nyilvános adathalmaz (Enron spam, SST-2, AG News, Banking77) + 1005 valós dokumentumoldal + 800 e-mail, kimenet valós üzleti eredményhez mérve | „On short-text classification it is level with or ahead of gpt-5.4-mini and gpt-5.6-luna on three of four public sets... It is best on short input with crisp labels. […] On a whole-document read it is worse than the small model we run today." |
| WotAI (wotai.co, Alex Kim, 2026-09-18, T2) | 16 modell, 150 passzázs, Noul-kérdés (kalibráció) + 2 Choice-feladat | „Was Jev more accurate? Not consistently… Across three tasks it lost one, won one and tied one: 79.9% against 83.2% on business categories, 50.0% against 42.0% on commit types, 66.0% each on prose voice." |
| TrueStandard (truestandard.ai, 2026-09-18, T2) | 108 kézzel címkézett állítás, 6 domain, 3 modell (Jev, Gemini 3.1 Flash Lite, Claude Haiku 4.5) | „Jev finished 1.9 points ahead of Gemini 3.1 Flash Lite and 2.8 ahead of Claude Haiku 4.5 on raw accuracy" — 96,3% vs. 94,4% vs. 93,5% |
| AY Automate (ayautomate.com, 2026-09-20, T2) | 791 címkézett döntés, Banking77 (8- és 77-utas) + prompt-injekció-detekció, McNemar-teszt | „Not more accurate than GPT-5.6 Terra: on 77-way intent routing Terra was 5 points ahead… Jev behaved like a good small model, not like a frontier model." |
| primeline.cc (2026-09-18, T2) | pre-regisztrált, 3600+ tétel (film-, hír-, hangulat-, Banking77-adat) + 798 saját commit + 450 tudásbázis-tétel, Jev vs. Claude Haiku 4.5 | „Jev won the commit-message job clearly: 65.7% accuracy against Haiku's 54.8%… Jev lost the knowledge-category job just as clearly." |
| dev.to/aitejiu (2026-09-21, T2) | 10 nyilvános/félig-szintetikus adathalmaz ágens-eszközökre (InjecAgent, BEIR SciFact, SNIPS, Banking77, MetaTool, BFCL, SkillRetBench, RouterBench, Who&When) | vegyes: nagyon jó prompt-injekció-detekción és rerankeren, gyenge modell-routingon (51,3%, „no signal") és trajektória-hibaazonosításon (AUROC 0,560, véletlenszintű) |
| wpnews.pro (2026-09-21, T2) | 3 japán osztályozási feladat, 250 címkézett sor/feladat, 6 rendszer | 9-osztályos témabesorolás: Jev 76,8%, egy 310M-paraméteres tanított enkóder 88,8% (McNemar p=0,00007) |

## 2. Kalibráció: van-e mérés arra, hogy a valószínűség tényleg megfelel-e a találati aránynak?

A TypeSafe hivatalos állítása (a blogban): „Always communicates confidence and uncertainty with every output. Calibrated: higher confidence means higher accuracy." (typesafe.ai/blog/introducing-system-one-models-and-jev, T1) — de ehhez **maga a cég semmilyen ECE/Brier/reliability-diagram számot nem publikált**. Egy Jev-dokumentációs oldal (nem hivatalos, de nem is marketing-célú, technikai jellegű) ezt kifejezetten kritizálja:

> „Calibration is a specific, testable property with a precise definition and a standard metric. TypeSafe built a company on it and published neither a number nor a curve. […] TypeSafe has published no calibration metric of its own — no ECE, no Brier score, no reliability diagram. For a company whose entire differentiator is calibration, and for the single easiest property in machine learning to measure, that remains the most conspicuous omission of the launch."
(https://learnjev.com/concepts/calibration, T3 — nem hivatalos Jev-oldal, de a `_kozos.txt` szerint jelölve, önmagában nem elegendő forrás, ezért az alábbi független mérésekkel erősítve)

Ugyanez az oldal összefoglal több független mérést egy táblázatban:

| Független mérés | Eredmény |
|---|---|
| Pre-regisztrált vizsgálat, 8576 válasz | „Calibrated on CLINC150 (ECE 0.0204). Not calibrated on Banking77 (ECE 0.0936, systematically overconfident). Same model, same method, two datasets, opposite verdicts." |
| Konfidencia-sáv ellenőrzés | „On the 126 rows where Jev reported confidence ≥ 0.9, it was 72.2% accurate. That is the failure mode calibration is supposed to prevent." |
| Küszöbérték-átvihetőségi teszt | „The optimal threshold moved from 0.67 to 0.37 between two datasets… 'nothing measured on the first dataset predicted the second.'" |

Ezt más, önálló mérések is megerősítik és árnyalják:

- **WotAI (16 modell, 150 sor, Noul-kérdés, 2026-09-18, T2)**: „Sonnet 5 posted an ECE of 0.062, roughly half Jev's 0.121, with better accuracy and more willingness to sit in the middle. On the metric TypeSafe's entire pitch rests on, a general-purpose frontier model won." Ugyanakkor a sub-second (1 másodperc alatti) modellek közt „Jev had the best calibration error of the three models that qualified" (0,121 vs. Haiku 0,122 vs. gpt-5.4-mini 0,192).
- **TrueStandard (108 állítás, 2026-09-18, T2)**: „Expected calibration error came out at 0.066 for Jev, 0.061 for Gemini 3.1 Flash Lite and 0.067 for Claude Haiku 4.5. At 108 items those are one number… A cheap frontier-lab model, asked properly for a probability, calibrates about as well as the model built to produce calibrated probabilities." Fontos módszertani megjegyzés a cikkből: első (22 tételes) futtatásukban a Jev „nyert" a kalibráción, de ez a prompt hibája volt (nem kérték a chat-modelleket a teljes 0–1 skála használatára); a hibát javítva a különbség eltűnt.
- **dev.to (aws-builders, aggregált áttekintés, 2026-09-24, T2)**: „On Bespoke Labs' 13-subset public suite, Jev's median ECE is 0.071, lower than Nimble-9B's on 11 of 13 subsets… Against LLMs that write their confidence as a number, Jev's own probabilities usually win. Its median ECE of 0.157 on the social-science tasks beats 16 of 19 LLMs. Once every model gets one fitted temperature, 15 of those LLMs beat it." Ugyanez a cikk azt is jelzi, hogy az irány (túlzott vagy alulzott magabiztosság) adatfüggő: „On public multi-class sets Jev is overconfident: on GoEmotions, labels it scored between 0.80 and 0.95 matched the human label 15% of the time. On crash narratives and synthetic items it is under-confident."
- **jevkit-calibrate és jevcal (közösségi Python-csomagok, PyPI, T3/community eszköz)**: mindkettő kifejezetten azért készült, mert a felhasználóknak saját maguknak kell mérniük az ECE-t/Brier-t/reliability-diagramot — vagyis a piac maga is elismeri, hogy erre nincs gyártói szám: „Verify TypeSafe Jev's calibration on your own data. […] TypeSafe measures this across groups of predictions and says plainly that it does not guarantee any individual answer. This package checks the claim on your data, which is the part nobody else can do for you." (jevkit-calibrate, PyPI, T3)
- **Bernoulli.app elemzés (2026-09-18, T2)**, amely a `confidence` mező (nem az alap valószínűség) matematikai eredetét vizsgálta 1 millió hívás alapján: „Across one million tests, Choice confidence closely follows a normalized top probability within just a rounding error… The practical truth, however, is that neither result establishes that Jev's confidence value relates to the probability of being right, that is model uncertainty in general." Ez azt jelenti, hogy a `confidence` mező egy egyszerű, a válasz-eloszlásból levezetett újraskálázás, nem egy külön, tanult bizonytalanság-becslés.

**Összefoglalva**: van mérés (több is), de a kép kevert és erősen adatfüggő — a kalibrációs hiba (ECE) nagyságrendileg 0,02-től (CLINC150) 0,35-ig (6-osztályos emóció-adathalmaz) terjed a különböző tesztekben, és legalább egy közvetlen összevetésben egy általános célú LLM (Claude Sonnet 5) jobban kalibrált volt a Jevnél ugyanazon a feladaton.

## 3. Többosztályos besorolás (5–20 címke) mérése

Több forrás pontosan ebbe a tartományba eső osztályszámmal tesztelt:

| Adathalmaz | Osztályszám | Jev pontosság | Összevetés |
|---|---|---|---|
| SNIPS (dev.to/aitejiu, 2026-09-21) | 7 | 97,9% | „conf≥0.90: 93.6% coverage, 99.1% acc" |
| AG News (Aman Kumar, 2026-09-18) | 4 (a tartomány alján) | 91,3% | gpt-5.4-mini 88,3%, gpt-5.6-luna 89,7% — Jev nyer |
| livedoor hírtéma (wpnews.pro, 2026-09-21, japán) | 9 | 76,8% | egy 310M-paraméteres, 250 mintán tanított ModernBERT-ja enkóder 88,8% (McNemar p=0,00007); GLiClass zero-shot 62,8% |
| TweetTopic (OpenRouter cookbook, 2026-09-21, T1 — gateway hivatalos dokumentációja) | 6 | „got 350 of 400 correct" = 87,5% | kalibrációs bontás: „Confidence splits here are at 0.8 or above: 114 of 122 matched; at 0.5 to below 0.8: 9 of 18; below 0.5: 4 of 10." |
| Banking77 8-utas alcsoport (AY Automate, 2026-09-20) | 8 (a tartomány alján) | 83,8% | gpt-5.4-nano 90,0%, GPT-5.6 Terra 89,4% — mindkettő megelőzi |
| Banking77 teljes (több forrás) | 77 (a tartományon kívül, de releváns szélső eset) | 76,0–80,3% (forrásonként eltérő mintavétel) | Aman Kumar: gpt-5.4-mini 78,7%, gpt-5.6-luna 81,7% — mindkét kis LLM megelőzi; AY Automate 77-utas altesztjén GPT-5.6 Terra 84,0% vs. Jev 78,8% |
| MetaTool eszközkatalógus (dev.to/aitejiu) | 199 (a tartományon kívül) | 96,5% „similar distractors (k=5)" mellett | „the paper reports 69.1% for ChatGPT on the same 'similar choices' subtask" |

A mintázat több forrásban is megegyezik: **kevés, jól elkülönülő osztálynál (≤10) a Jev jellemzően erős vagy vezet**, míg **sok, egymást átfedő, finomszemcsés osztálynál (77-es Banking77) mind kis, mind frontier LLM-ek megelőzik**. Aman Kumar ezt így fogalmazza meg: „In our interpretation, when classification spaces exhibit dense semantic overlap across dozens of labels, Jev's discriminative certainty degrades alongside its underlying classification precision." (amankumar.ai, T2, megerősítve a braindetox.kr másodforrás által, T2/T3)

## 4. Nyelvek: angol és magyar

**Angol**: a fenti mérések túlnyomó többsége angol nyelvű szövegen történt, ez a fő nyelv, amin adat van.

**Magyar**: a jelen kutatás során **egyetlen forrást sem találtam**, amely kifejezetten magyar nyelvű bemeneten mérte volna a Jev pontosságát, kalibrációját vagy bármilyen teljesítménymutatóját. A magyar nyelvű technológiai média (Mobilissimo.hu, 2026-09-19; nerdgeek.hu, 2026-09-23) beszámolt a Jev indulásáról, de ezek a cikkek a modell általános leírására szorítkoznak, angol nyelvű elsődleges forrásokra (elsősorban TechCrunch) hivatkozva, és nem foglalkoznak a magyar nyelvi teljesítménnyel:

> „Szövegenerálás helyett villámgyors döntésekre tervezték a TypeSafe AI legújabb mesterséges intelligenciáját, a Jev modellt…" (nerdgeek.hu, 2026-09-23, T2 — de nem tartalmaz nyelvi teljesítményadatot)

**Következtetés: NINCS FORRÁS** a magyar nyelvi teljesítményre.

Más, nem angol nyelvekre viszont van szórt (bár nem magyar) adat, amely egy általánosabb mintázatot mutat — a teljesítmény nyelvváltáskor csökken:

- **Orosz**: „Russian XNLI dropped from 88.3% to 77.3% with ECE tripling" (dev.to/aws-builders, 2026-09-24, T2)
- **Spanyol**: „Spanish cost 3 to 6 points" (uo.)
- **Német**: „German cost 0.5 points on MASSIVE" (uo.)
- **Kínai vs. angol** (modell-nehézség-útválasztás, RouterBench): „Chinese subset 14.6% vs English 57.7%." (dev.to/aitejiu, 2026-09-21, T2)
- **Koreai vs. angol** (SkillRetBench): „Non-English tasks: KO R@1 48.9% vs EN 61.5%." (uo.)
- **Japán**: 3 feladaton 65,2–76,8% közötti zero-shot pontosság (wpnews.pro, 2026-09-21, T2), ahol egy kis, saját nyelvre tanított enkóder egy feladaton lényegesen jobb volt.

Egy horvát nyelvű elemzés (bug.hr, 2026-09-22, T3, de tartalma összhangban a fentiekkel) kifejezetten figyelmezteti a nem angol nyelvű felhasználókat:

> „Prema dokumentaciji engleski je glavni jezik treninga, a ostale jezike model obrađuje, ali ne jednako dobro, pa hrvatske tekstove treba testirati na vlastitim podacima."
(„A dokumentáció szerint az angol a fő betanítási nyelv, a többi nyelvet a modell kezeli, de nem egyenlő eséllyel, ezért a [nem angol] szövegeket saját adaton kell tesztelni.")

Ez közvetve megerősíti, hogy a hivatalos TypeSafe-dokumentáció is jelzi az angol elsődlegességét, de ehhez konkrét magyar (vagy akár horvát) számot ez a forrás sem közöl — csak azt tanácsolja, hogy magának a felhasználónak kell megmérnie.

## 5. Ismert hibamódok

### 5.1 A TypeSafe saját, dokumentált hibamód-listája

Egy Jev-dokumentációs oldal (learnjev.com/tutorials/failure-modes, T3, de a TypeSafe hivatalos dokumentációjára hivatkozva és azt idézve) 9 pontban sorolja fel a `jev-1.13` ismert gyengeségeit, TypeSafe-idézetekkel alátámasztva:

| # | Hibamód | TypeSafe ajánlása |
|---|---|---|
| 1 | Szó szerinti értelmezés | „Write the exact condition, criteria for each available option" |
| 2 | Matematika és számok | „Keep the arithmetic in code" |
| 3 | Dátum- és időösszehasonlítás | „Extract components; compare in code" |
| 4 | Indirekció (közvetett hivatkozás) | „Reduce hops; point to the relevant state" |
| 5 | Irreleváns részlettel túlterhelt állapot („context rot") | „Filter first; send only what the question needs" |
| 6 | Ellenséges/manipulatív tartalom | „Write precise prompts, and test edge cases before deploying" |
| 7 | Ellentmondó instrukció és kritérium | „Align the criteria and instruction" |
| 8 | Köznapi strukturális invariánsok megsértése | „Ask each decision one way; enforce identities in code" |
| 9 | Generálásigény (a modell nem tud szöveget írni) | „Use a generative model" |

A horvát bug.hr cikk (2026-09-22) függetlenül is megerősíti ugyanezt a listát: „dokumentacija ima stranicu o devet tipičnih slabosti verzije jev-1.13. Model griješi u računanju, usporedbi datuma i praćenju neizravnih upućivanja, upute čita previše doslovno, zbunjuju ga proturječne upute i zlonamjeran sadržaj, a točnost mu pada kad je stanje pretrpano nevažnim detaljima (context rot)."

### 5.2 Rossz választás magabiztosan (confident wrong answer)

- **TechSpot**: „'Can't hallucinate' is a narrow claim. Jev can't return an answer outside the list it was given… But it can still confidently pick the wrong option." (T2)
- **AY Automate (791 döntés, McNemar-teszt, 2026-09-20, T2)**: „Confident answers were still sometimes wrong: 5 of 112 on 8-way routing and 12 of 153 on 77-way routing at 0.90 or above." A konkrét hibapélda: „The five confident 8-way errors were all the same mistake. Each was labeled 'direct debit payment not recognised' and Jev called it 'card payment not recognised' at 0.93 to 0.99 confidence. GPT-5.6 Terra made the same call on all five, which points at the two labels overlapping, not at a Jev quirk."
- **learnjev.com konfidencia-sáv-elemzés** (a fenti, kalibrációs táblázatból): „On the 126 rows where Jev reported confidence ≥ 0.9, it was 72.2% accurate." (T3, önmagában nem elég, de az AY Automate és a TechSpot fenti megállapításával összhangban)
- **primeline.cc (2026-09-18)** hasonlót talált a saját tudásbázis-teszten: „letting Jev abstain below 0.8 confidence would close the gap — it reaches 98.6% accuracy on the 79% of items it feels confident about," de „on the exact same 356 items Jev chooses to keep, Haiku still wins (98.9% against Jev's 98.6%)" — vagyis a magas magabiztosság nem garantálja, hogy jobb lenne egy alternatívánál.

### 5.3 Hosszú bemenet

- **Aman Kumar**: „It is best on short input with crisp labels. The longer the input and the fuzzier the labels, or the more business logic the question carries, the more its accuracy and its confidence fall together. On a whole-document read it is worse than the small model we run today, and no prompt fixed that." Konkrét számpélda: „A 2,000-email phishing bench had Jev at 62.6% against 81.3% for Claude Haiku 4.5, with worse calibration."
- **learnjev.com (writing-state oldal)**, TypeSafe-idézettel: „Jev suffers from context rot, so unrelated material in the state costs you accuracy." (T3, de a fenti Aman Kumar-eredménnyel és a bug.hr-rel összhangban)
- **navinpai.github.io** (T2): „Long option lists squeeze the descriptions; the repository recommends staying below about 20 choices. Its benchmark report also says the shipped probabilities are overconfident and that temperature fitting helps."

### 5.4 Hasonló/átfedő opciók

- Lásd fent (5.2): a „direct debit payment not recognised" vs. „card payment not recognised" tévesztés az AY Automate tesztben, amit a GPT-5.6 Terra is ugyanúgy elhibázott — az elemzés szerint ez a **címkekészlet átfedésének**, nem kifejezetten a Jev hibájának tudható be.
- **dev.to/aitejiu (MetaTool teszt)**: „MetaTool comparison: the paper reports 69.1% for ChatGPT on the same 'similar choices' subtask (different exact setup — treat as magnitude reference). Errors cluster on near-duplicate tools: descriptions need explicit `not_for` boundaries." — 96,5% pontosság hasonló disztraktorok mellett (k=5), de a hibák szisztematikusan a majdnem-azonos eszközökön csoportosulnak.
- **Banking77** (76 vs. 77 finom, átfedő banki szándék-kategória) minden korábban idézett forrásban a leggyengébb pontja a Jevnek a rövid szövegű tesztek közül.

### 5.5 Ellentmondó állítások felismerése / Noul-kérdéssel kapcsolatos következetlenség

Kifejezett „ellentmondó állítás felismerése" tesztet (pl. két egymásnak ellentmondó mondatot tartalmazó bemeneten Noul-kérdéssel) nem találtam. Amit találtam, az a **modell saját belső következetlensége** azonos tény különböző kérdezési módokon (Noul vs. Choice), amit maga a TypeSafe dokumentál nyilvánosan, „jaggedness" néven:

> „On the ticket 'I'm not happy with the fit. What are my options here?', asked as 'Is the customer asking for a refund?': Noul 0.22 | Choice yes 0.01 | Choice no 0.99 | Choice confidence 0.97. Same question, same ticket, two primitives. Published on TypeSafe's jev-1.13 jaggedness page."
(https://learnjev.com/tutorials/three-primitives, T3, TypeSafe hivatalos „jaggedness" oldalára hivatkozva, amit közvetlenül nem sikerült Exa-val lekérni — `typesafe.ai/blog/jev-1-13-jaggedness` CRAWL_NOT_FOUND hibát adott)

Ugyanez az oldal egy másik, logikai ellentmondást is dokumentál: két, egymás tagadásának szánt Noul-kérdés összege nem 1:

> „On 'I was charged twice for the same order. Can someone look into this?': `refund` 0,72, `not_refund` 0,47, összeg 1,19."

A jevaiguide.com (T3) is megerősíti ugyanezt a jelenséget, saját méréssel:

> „In our own test, 'Is the customer asking for money back?' scored 0.50 on a message that complained about a charge but never mentioned a refund, while 'Does the customer say a charge might be wrong?' scored 0.97. Neither is wrong; the first question was ambiguous."

Ez a jelenség közvetlenül a `_kozos.txt`-ben említett **D-20 (duplikátum-/hasonlóság-ellenőrzés) és D-22/D-26 (kategória-választó prompt)** döntésekhez kapcsolódóan releváns kockázat: ha egy jövőbeli integráció ellentmondó állítások felismerésére Noul-kérdést használna, a fenti adatok azt jelzik, hogy (a) a Noul és az ezzel logikailag ekvivalens Choice-kérdés eltérő választ adhat, és (b) egy állítás és tagadásának Nouljai nem feltétlenül összegződnek 1-re — vagyis a modell nem konzisztens logikai értelemben a kérdezési primitívek között. Erre a TypeSafe hivatalos ajánlása: „Never carry a threshold tuned on a Noul across to a Choice. Never assume complementary questions sum to 1." (learnjev.com, TypeSafe-idézet nyomán, T3)

## 6. Összevetés: frontier LLM, kis helyi osztályozó, beágyazás/koszinusz-alapú osztályozás

### 6.1 Frontier LLM-mel

| Forrás | Eredmény |
|---|---|
| WotAI (16 modell, 2026-09-18) | „Claude Sonnet 5, on calibration error (0.062) and accuracy (71.3%)… If your budget allows a 1.7-second gate, Sonnet 5 is the better instrument." Jev accuracy 66,0% (holtverseny Claude Haiku 4.5-tel), de leggyorsabb (455ms). |
| AY Automate (2026-09-20) | „Not more accurate than GPT-5.6 Terra: on 77-way intent routing Terra was 5 points ahead, and a paired test says that gap is real (p=0.029)." |
| dev.to/aws-builders (aggregált, 2026-09-24, egy nagy pre-regisztrált tanulmány, Ibrahim & Zaki replikáció, ~7977 emberi válasz alapján) | „On accuracy, Jev sits level with mid-price LLMs and 6.5 to 11.5 points behind the frontier in the cleanest comparison." Táblázat: Claude Fable 5.1 84,0% (ECE 0,064), GPT-6 Astra 79,0%, DeepSeek V4.1 Flash 76,0%, MiniMax M3 75,5%, Kimi K3 74,5%, **Jev 72,5%** (ECE 0,161) — Jev az utolsó helyen pontosságban ebben az összevetésben. |
| TrueStandard (108 állítás) | Jev 96,3% vs. Gemini 3.1 Flash Lite 94,4% vs. Claude Haiku 4.5 93,5% — itt a Jev vezet, elsősorban a nehéz („adversarial near-miss") kategórián: 91,7% vs. 83,3%/80,6%. |

Tehát **a kép vegyes és feladatfüggő**: van olyan teszt, ahol a Jev veri a kisebb/olcsóbb LLM-eket, és van, ahol egy csúcsmodell (Sonnet 5, GPT-5.6 Terra, Claude Fable 5.1/GPT-6 Astra) egyértelműen jobb nála pontosságban és/vagy kalibrációban.

### 6.2 Kis, helyben futó (saját adaton tanított) osztályozóval

- **wpnews.pro (2026-09-21)**: egy 310M-paraméteres japán ModernBERT-enkóder, 250 címkézett sorral tanítva, 5-szörös keresztvalidációval: „beat TypeSafe's Jev decision API by 12.0 points on 9-class livedoor topic classification (McNemar p=0.00007) while running 4–20× faster, but only tied Jev on the two polarity tasks." A cikk explicit szabálya: „if the label is visible in the words, train something small; if the label is a judgement about the words, use a decision API."
- **dev.to/aws-builders** (Bespoke Nimble-9B, egy LoRA-alapú, Qwen 3.5 9B-re épülő „klón" modell összevetése): „Kev-9B vs. Jev, out of domain | Accuracy 82–85% vs 85.7%. ECE 0.042 vs 0.049. Coverage at ≤ 5% error: 0.45–0.57 vs 0.70" — itt a nyílt, kis, tanított modell hasonló pontosságú és kalibrációjú, de **lényegesen rosszabb „coverage"-t** (mennyi döntést lehet automatizálni adott hibaköltség mellett) ér el, mint a Jev, mert bár a kalibrációs hiba (ECE) hasonló, a Jev jobban **rangsorolja** saját helyes válaszait a hibás fölé.
- **jev-agent.com (T3, nem hivatalos, de technikai összevetés)** táblázata szerint: „Is Jev more accurate than a fine-tuned BERT classifier? Not on a single fixed task where you have plenty of clean labels — a small trained model will usually beat a general decision model on both accuracy and inference cost. Jev wins when the labels do not exist yet, when the taxonomy moves, or when you need many different judgements rather than one."
- **jevaiguide.com (T3)** hasonló következtetésre jut egy összehasonlító táblázatban: fix, nagy volumenű, sok címkével rendelkező feladatnál a finomhangolt (fine-tuned) osztályozót ajánlja, új/változó taxonómiájú, kevés vagy semennyi címkével rendelkező feladatnál a Jevet.

### 6.3 Beágyazás-alapú (koszinusz) osztályozással

**Konkrét, számszerű összevetést tiszta koszinusz-hasonlóságú (tanítás nélküli, pl. sentence-transformer + legközelebbi centroid) osztályozóval nem találtam.** A fellelt (nem hivatalos, T3) elemzések csak minőségi állításokat tesznek:

> „'Jev vs embeddings' is a category error worth untangling. An embedding model turns text into a vector so you can measure similarity. It does not answer a question. The comparable approach is embeddings plus a k-nearest-neighbour lookup over labelled examples, which is a legitimate and very cheap classifier — but it still needs labelled neighbours, and it can only answer questions that similarity happens to encode."
(https://jev-agent.com/jev-vs-classifier, T3)

> „Is Jev the same as an embedding model? No. Embeddings give you a vector so you can measure similarity; Jev gives you a decision over options you named, with a probability for each. Embeddings plus kNN is a real alternative for classification, but it needs labelled neighbours and it cannot answer a question the vectors were not built for."
(uo.)

A jevaiguide.com egy táblázatban helyezi el az „Embeddings + small model" oszlopot a Jev és a finomhangolt osztályozó között, de konkrét pontossági számot nem közöl hozzá, csak minőségi jellemzőket („Labeled data needed: Dozens to hundreds", „Probabilities: Depends on the model you fit"). Egy kapcsolódó, de **nem azonos** módszer — a nulla-mintás (zero-shot), NLI-alapú **GLiClass** osztályozó (amely span-alapú entailment-modellt használ, nem tiszta koszinusz-hasonlóságot) — viszont szerepel egy számszerű összevetésben:

> „Zero-shot, it scored 62.8 / 87.2 / 44.8: it lost to Jev [76,8/94,4/74,0] on all three tasks, and on the 3-class polarity task it was barely above chance (44.8% against 33.3%)."
(wpnews.pro, 2026-09-21, T2)

Ez azonban **nem koszinusz-alapú beágyazás-osztályozó**, hanem egy tanítás nélküli NLI-osztályozó, ezért csak közvetve releváns a kérdésre — a `_kozos.txt` D-20 pontjában említett, beágyazással végzett hasonlóság-ellenőrzéshez (duplikátum-keresés) közelebb álló, tiszta koszinusz-alapú *osztályozási* összevetésre **nincs forrás**.

## Ellentmondások

1. **A kalibráció minősége forrásonként ellentétes verdiktet kap.** A WotAI 16-modelles teszt szerint a Jev ECE-je (0,121) rosszabb egy frontier LLM-énél (Claude Sonnet 5, 0,062) ugyanazon a feladaton — „On the metric TypeSafe's entire pitch rests on, a general-purpose frontier model won." Ezzel szemben a dev.to/aws-builders aggregált áttekintése szerint a Jev medián ECE-je (0,071) a 13 adathalmazos Bespoke Labs-csomagon jobb, mint a tesztelt 19 LLM közül 16-é, és „Jev's own probabilities usually win" az LLM-ekkel szemben. A TrueStandard-teszt szerint pedig, ha egy olcsó LLM-et megfelelően (a teljes 0–1 skála használatára) kérnek, a kalibrációs különbség gyakorlatilag eltűnik (ECE 0,061–0,069 mindhárom modellre). A három forrás nem feltétlenül zárja ki egymást (más-más feladat, más-más LLM-ek), de együtt azt mutatják, hogy **nincs egységes, minden helyzetben érvényes kalibrációs előny** — erősen adat- és összevetés-függő.
2. **A „0% hallucináció" állítás és a tényleges pontossági rangsor feszültsége.** A TypeSafe maga írja: „Our number is not empirical. Schema matching is guaranteed, thus we can confidently add 0% into the plots." (typesafe.ai blog, T1) — vagyis ez csak azt garantálja, hogy a válasz szintaktikailag érvényes, nem azt, hogy helyes. Az agenccy.ai és az opentweet.io külön is felhívja a figyelmet arra, hogy ezt a marketingszám a sajtóban gyakran összemosódik a tényleges helyességgel: „A guaranteed-valid output is being marketed on the same chart as measured error rates, and a buyer reading it will conclude the model cannot be wrong. The company's own evals say otherwise — fourth on accuracy." (agenccy.ai)
3. **Ellentétes megállapítás arról, hogy több osztály rontja-e a kalibrációt/pontosságot.** Az általános elvárás (és a legtöbb forrás mintázata, pl. Banking77) az, hogy sok, átfedő osztály nehezebb. Ugyanakkor a primeline.cc pre-regisztrált tesztje explicit ennek ellenkezőjét találta az ő adatukon: „having more answer options does not make calibration worse either: the 5-level sentiment scale was harder to calibrate than the 77-option classifier, because the 5 levels are neighbours on a scale and Jev would confidently pick the level right next to the correct one, while the 77 categories are mostly unrelated to each other." Ez nem feltétlenül mond ellent a Banking77-es eredményeknek (ott más volt a mérőszám: pontosság, nem kalibráció), de érdemes jelezni, hogy „sok osztály = rosszabb" nem egyetemes szabály, a kérdéstípus (kategorikus vs. ordinális skála) legalább annyira számít.
4. **A gyorsulási szorzó (193,6x / 444,6x) és a független mérések közötti eltérés** közvetve érinti a megbízhatóság kérdését is: a WotAI ezt írja: „TypeSafe's landing page claims 20 to 200x, and I did not find the workload where that appears" — mérése 1,4–3,7x-es gyorsulást talált. A TrueStandard külön cikkben (2026-09-19) ezt árnyalja: „When we reproduced that shape [6 szekvenciális LLM-hívás egy batch Jev-hívással szemben], we measured 100.7x faster… When we compared a single classification call instead, we measured 1.7x. Both are correct measurements of different things." Ez nem pontossági, hanem sebességi ellentmondás, de mivel a felhasználói kérdés a Jev általános megbízhatóságára vonatkozik, érdemes jelezni: a fejenkénti szorzószámok nagyban függenek attól, mihez hasonlítjuk.

## Amire NINCS forrás

- **Magyar nyelvű teljesítménymérés** — sem pontosságra, sem kalibrációra, sem semmilyen más mérőszámra nem található közvetlen adat magyar nyelvű bemeneten. A magyar nyelvű médiamegjelenések (Mobilissimo.hu, nerdgeek.hu) csak a modell általános bemutatására szorítkoznak.
- **Tiszta, tanítás nélküli koszinusz-hasonlóságú beágyazás-osztályozóval (pl. sentence-transformer + centroid/kNN, kifejezetten mint önálló osztályozási módszer) végzett, számszerű összevetés a Jevvel** — csak minőségi állítások vannak arról, hogy ez „kategóriahiba", konkrét pontossági/ECE-szám nem található hozzá. A talált „embedding-szerű" összevetés (GLiClass) valójában egy NLI-alapú zero-shot modell, nem tiszta koszinusz-osztályozó.
- **Kifejezett, kontrollált teszt „ellentmondó állítások felismerésére" Noul-kérdéssel** (pl. két, egymásnak ellentmondó mondatot tartalmazó bemeneten explicit „van-e ellentmondás" kérdés) — csak közvetett adat van: a modell saját belső következetlensége (Noul vs. Choice eltérés, tagadás-összeg ≠ 1) ugyanarra a tényre, amit maga a TypeSafe dokumentál, de ez más jelenség, mint egy bemeneten belüli, két állítás közötti ellentmondás felismerése.
- **A TypeSafe „workflow evals" oldalának (a nyers számokat és a teljes módszertant tartalmazó oldal) közvetlen, elsőkézből való tartalma** — az oldal (`typesafe.ai/evals` és a blogban hivatkozott „workflow evals site") Exa-val nem volt lekérhető (`CRAWL_NOT_FOUND`), ezért a 67,8%/74,1%/61,8%/79,1% számokat csak másod-/harmadkézből (TechSpot és az őt megerősítő öt további forrás) sikerült megerősíteni, nem a gyártó saját oldaláról közvetlenül.
- **Pontos ECE/Brier-szám magára a TypeSafe hivatalos, saját méréséből** — ilyen, mint fent részletezve, nem létezik; minden számadat független, harmadik féltől származik.

## Meglátogatott és felderített linkek

| Cím | URL | Tier | Eszköz | Megjegyzés |
|---|---|---|---|---|
| Introducing System One Models and Jev (TypeSafe hivatalos blog) | https://typesafe.ai/blog/introducing-system-one-models-and-jev | T1 | Exa web_fetch_exa | Elsődleges forrás; leírja a „workflow eval" módszertant, de a konkrét számtáblát nem tartalmazza a lekért szövegben |
| typesafe.ai/evals | https://typesafe.ai/evals | — | Exa web_fetch_exa | Sikertelen lekérés (CRAWL_NOT_FOUND) |
| typesafe.ai/blog/jev-1-13-jaggedness | https://typesafe.ai/blog/jev-1-13-jaggedness | — | Exa web_fetch_exa | Sikertelen lekérés (CRAWL_NOT_FOUND) — a Noul/Choice-eltérés hivatalos „jaggedness" oldala, csak másodkézből (learnjev.com) idézhető |
| typesafe.ai/models | https://typesafe.ai/models | — | Exa web_fetch_exa | Sikertelen lekérés (CRAWL_NOT_FOUND), lásd sq00 is |
| Meet Jev: A New AI Model From One of ChatGPT's Co-Creators — TechSpot | https://www.techspot.com/article/3172-meet-jev/ | T2 | Exa web_fetch_exa | A 67,8%/74,1%/61,8%/79,1% szám elsődleges újságírói közlése |
| Is Jev actually calibrated? — Learn Jev | https://learnjev.com/concepts/calibration | T3 | Exa web_search_exa | Nem hivatalos, de technikai jellegű; ECE-hiány kritikája és független mérések összefoglalása |
| Jev topics — benchmarks — jevtypesafeai.com | https://jevtypesafeai.com/jev | T3 | Exa web_search_exa | Nem hivatalos; „every Jev benchmark you will see today is about speed, cost and calibration — not a public accuracy leaderboard" |
| TypeSafe Jev vs 15 other models, measured — WotAI | https://wotai.co/blog/typesafe-jev-vs-claude-haiku-tested | T2 | Exa web_search_exa | Független, 16 modelles, reprodukálható ECE/pontosság-teszt |
| Jev Accuracy Tested: 108 Claims Across Three Models — TrueStandard | https://truestandard.ai/blog/jev-accuracy-tested | T2 | Exa web_search_exa | Független, 108 kézzel címkézett állítás, ECE/Brier-számítással |
| jevkit-calibrate v0.1.0 — PyPI | https://pypi.org/project/jevkit-calibrate/ | T3 | Exa web_search_exa | Közösségi eszköz saját kalibráció-méréshez, jelzi a gyártói szám hiányát |
| jevcal v0.2.0 — PyPI | (jevcal PyPI oldal) | T3 | Exa web_search_exa | Hasonló közösségi kalibráció-mérő eszköz |
| Jev AI: the typed, calibrated decision model — jevtypesafeai.com | https://jevtypesafeai.com/jev-ai | T3 | Exa web_search_exa | Nem hivatalos termékbemutató oldal |
| Jev and RLCD: A Decision Model... — Saulius blog | https://saulius.io/blog/jev-rlcd-decision-model-calibrated-probabilities | T2 | Exa web_search_exa | RLCD-elemzés, Kev-9B/Nimble/Bespoke Labs eredmények aggregálása |
| Jev After Eight Days of Independent Tests — DEV Community (aws-builders) | https://dev.to/aws-builders/jev-after-eight-days-of-independent-tests-level-with-mid-price-llms-behind-the-frontier-1c60 | T2 | Exa web_search_exa | Legátfogóbb aggregáló cikk, sok elsődleges mérést újraszámol |
| Testing Jev on public and private data — Aman Kumar | https://amankumar.ai/blogs/jev-measured | T2 | Exa web_search_exa | ~16 000 hívás, 4 nyilvános + valós üzleti adat, „trust the ends, not the middle" |
| Measuring Jev — braindetox.kr | https://braindetox.kr/en/posts/jev_typesafe_classifier_filter_evaluation_2026.html | T2/T3 | Exa web_search_exa | Aman Kumar eredményeinek másodforrásos összefoglalása |
| Jev vs GPT and Claude: Independent Benchmark — AY Automate | https://www.ayautomate.com/blog/jev-vs-llm-benchmark | T2 | Exa web_search_exa | 791 döntés, McNemar-teszt, Wilson-intervallumok, AUROC |
| Is Jev Really 193x Faster? — TrueStandard | https://truestandard.ai/blog/is-jev-really-193x-faster | T2 | Exa web_search_exa | Sebesség-szorzó módszertani kritikája |
| TypeSafe Jev vs Claude Code: 4 Models, 2 Real Jobs — primeline.cc | https://primeline.cc/blog/typesafe-jev-pre-registered-test | T2 | Exa web_search_exa | Pre-regisztrált teszt, kérdéstípusonkénti kalibráció (Noul/Choice/Score) |
| Jev's 0% Hallucination Sits Beside a 67.8% Accuracy Score — agenccy.ai | https://agenccy.ai/news/jevs-0-percent-hallucination-sits-beside-a-678-percent-accuracy-score/ | T2 | Exa web_search_exa | A „0% hallucináció" és a pontossági rangsor közti feszültség elemzése |
| Benchmarking Jev: what a decision model can (and can't) do — DEV Community (aitejiu) | https://dev.to/aitejiu/benchmarking-jev-what-a-decision-model-can-and-cant-do-in-an-agent-harness-20po | T2 | Exa web_search_exa | 10 nyilvános adathalmaz, SNIPS/Banking77/MetaTool/RouterBench eredmények |
| TypeSafe AI 的 Jev 號稱快 193.6 倍？— DataSci Ocean | https://datasciocean.com/ai-concept/jev-overview/ | T2/T3 | Exa web_search_exa | Kínai nyelvű, több független forrást összesítő elemzés |
| Jev: AI koji ne priča, nego radi — Bug.hr | https://www.bug.hr/softver/jev-ai-koji-ne-prica-nego-radi-63035 | T3 (horvát tech média, de tartalma T1/T2-vel egyező) | Exa web_search_exa | 9 hibamód és nyelvi figyelmeztetés horvátul |
| Jev cannot write. That is the feature and the limit. — benchlm.ai | https://benchlm.ai/blog/posts/what-is-jev | T2 | Exa web_search_exa | Módszertani összefoglaló, saját (korlátozott) smoke teszttel |
| Jev vs a fine-tuned classifier — BERT, embeddings & cost — Jev Agent | https://jev-agent.com/jev-vs-classifier | T3 | Exa web_search_exa | Nem hivatalos, de technikai összevetés Jev / klasszikus osztályozó / embedding között |
| Jev vs Classifiers and Embeddings: Which to Use — jevaiguide.com | https://jevaiguide.com/compare/jev-vs-classifiers/ | T3 | Exa web_search_exa | Táblázatos összevetés Jev / fine-tuned / embeddings+kNN / zero-shot |
| Jev vs a 310M encoder I trained myself — Web Pulse | https://wpnews.pro/news/jev-vs-a-310m-encoder-i-trained-myself-750-rows-three-tasks-two-different | T2 | Exa web_search_exa | 3 japán feladat, McNemar-teszttel igazolt eredmények, GLiClass zero-shot összevetés |
| jevbench: Jev vs GPT-5-mini, Claude Sonnet 5, DistilBERT, BART NLI és Laya — madewithlaya.com | https://www.madewithlaya.com/builds/jevbench-classifiers | T3 (saját termék promóciója is) | Exa web_search_exa | Reprodukálható benchmark-keret, de a Laya (saját termék) javára is érdekelt lehet |
| Jev failure modes: 9 documented weaknesses — Learn Jev | https://learnjev.com/tutorials/failure-modes | T3 | Exa web_search_exa | A TypeSafe 9 hibamódjának részletes, TypeSafe-idézetekkel alátámasztott bemutatása |
| Jev Limitations: Known Weak Spots and Workarounds — jevaiguide.com | https://jevaiguide.com/jev-limitations/ | T3 | Exa web_search_exa | Ugyanaz a hibamód-lista, más megfogalmazásban |
| Jev primitives: Noul, Choice and Score — Learn Jev | https://learnjev.com/tutorials/three-primitives | T3 | Exa web_search_exa | A TypeSafe „jaggedness" oldaláról idézett Noul/Choice-eltérés és tagadás-összeg példák |
| Noul: Jev's Yes/No Question Type Explained — Jev AI Guide | https://jevaiguide.com/concepts/noul/ | T3 | Exa web_search_exa | Noul-viselkedés és következetlenség megerősítése saját teszttel |
| Jev Confidence and Calibration Explained — Jev AI Guide | https://jevaiguide.com/concepts/confidence/ | T3 | Exa web_search_exa | `confidence` mező vs. kalibráció fogalmi tisztázása |
| Is Jev confident? — Bernoulli.app | https://bernoulli.app/articles/is-jev-confident | T2 | Exa web_search_exa | 1 millió hívás alapján a `confidence` mező matematikai eredetének feltárása |
| Designing state for Jev — Learn Jev | https://learnjev.com/tutorials/writing-state | T3 | Exa web_search_exa | „Context rot" (hosszú/irreleváns bemenet) hivatalos TypeSafe-idézettel |
| Classify and Tag Text at Scale with Jev — OpenRouter cookbook | https://openrouter.ai/docs/cookbook/evaluate-and-optimize/jev-classification | T1 (gateway hivatalos dokumentációja) | Exa web_search_exa | TweetTopic 6-kategóriás teszt, 350/400 pontosság, kalibrációs bontás |
| Jev Confidence Thresholds: How to Choose Them — MrJev | https://mrjev.com/guides/confidence-thresholds/ | T3 | Exa web_search_exa | Noul-küszöbérték gyakorlati útmutató |
| Decoding Jev — Architecture, inference, and RLCD — navinpai.github.io | https://navinpai.github.io/decoding-jev/ | T2 | Exa web_search_exa | Architektúra-elemzés, túlzott magabiztosság és hőmérséklet-illesztés megjegyzése |

Kimenet mentve: `/home/claude/work/kutatas-jev/sq02-pontossag.md`

---

# SQ03 — Ár, elszámolás, és mi történik, ha elfogy a keret vagy nem elérhető

*Kutatási eszköz: kizárólag Exa (`web_search_exa`, `web_fetch_exa`), az utasításnak megfelelően. Alügynök-indítás (deep-web-research skill teljes pipeline-ja) nem történt — ez egy önálló, célzott kör, Exa-only módban, elsődleges (TypeSafe hivatalos + gateway hivatalos) forrásokra támaszkodva, ezért degradált, de forrás-fegyelmezett módszerrel.*

## Rövid válasz

A TypeSafe hivatalos bejelentő blogja (2026-09-14/15) szó szerint **$0,042 / millió bemeneti token, a kimenet ingyenes** árat közöl — ezt közvetlenül, elsődleges forrásból megerősítettem. Az elszámolás hivatalosan **kredit-alapú**: a Master Customer Agreement (MCA) 8.2. szakasza szerint minden Inputot „TypeSafe-managed Credits” fedez, opcionális automatikus feltöltéssel — ez pontosítja/cáfolja az előző (SQ00) kutatási kör azon állítását, hogy „nincs hivatalos, előre feltöltött egyenleg-rendszer”. A hivatalos TypeSafe API dokumentált hibakódjai (`docs.typesafe.ai`) kizárólag **401, 422, 429, 529** — nincs bennük 402 vagy bármilyen „elfogyott a kredit” kód; a MCA csak annyit mond, hogy ilyenkor „TypeSafe may decline to generate Output”, a pontos HTTP-mechanizmus nincs dokumentálva. A 429/529 esetére a hivatalos ajánlás egyértelmű: exponenciális backoff, amit a saját SDK-k automatikusan kezelnek. A gateway-eknél viszont pontosan dokumentált, kvótázott a hiba: **OpenRouter 402**-t ad `{"error":{"code":402,"message":"Insufficient credits..."}}` testtel és lekérdezhető egyenleggel (`GET /credits`, `GET /api/v1/key`); a **Vercel AI Gateway** szintén **402**-t ad `type: "quota_for_entity_exceeded"` mezővel, és van beépített, e-mailes küszöb-riasztása (50/75/100%); a **Cloudflare AI Gateway** a saját „Spend limit” szabályánál viszont **429**-et ad, és opcionálisan olcsóbb modellre tud esni. Mindhárom gateway kínál modell/provider-fallback mechanizmust, a hivatalos TypeSafe API-nak viszont nincs saját fallback funkciója. Szállítói kockázat szempontjából a TypeSafe 2024-ben alapított, 2026-09-15-én lépett ki stealth-ből ~40 millió dolláros seed-körrel (DCVC), a Jev pedig a kutatás idején (2026-09-25) mindössze 10 napos, hivatalosan is „preview”/„early access” státuszú termék, üzemeltetői ToS-e szerint bármikor, bármilyen okból felfüggeszthető vagy megszüntethető, és a fel nem használt előre fizetett kreditek megszűnéskor nem járnak vissza.

## 1. Hivatalos árazás (TypeSafe)

Közvetlenül lekért, elsődleges forrás — a TypeSafe hivatalos bejelentő blogja:

> „Input tokens: $0.042 / MTok ($ 42 per billion tokens). Output tokens: FREE (too cheap to meter)."
(typesafe.ai/blog/introducing-system-one-models-and-jev, 2026-09-14/15, T1, `web_fetch_exa`-val közvetlenül lekérve)

Ez **szó szerint megerősíti** az azonosító kör (SQ00) és a felhasználói kérdés „$0,042 / millió bemeneti token, kimenet ingyenes” állítását — elsődleges forrásból, közvetlen idézettel.

Két független, egymástól eltérő forrás is megerősíti ugyanezt a számot:
- Refix (T3, 2026-09-18): „TypeSafe's models page currently lists Jev 1.13 at… Input price | $0.042 per million tokens… Output tokens | free."
- eesel AI (T3): „TypeSafe Jev costs $0.042 per million input tokens, and output tokens are free."

**Nincs külön, publikált „pricing” oldal**: `typesafe.ai/pricing` 404-et ad — ezt három egymástól független forrás is megerősíti (eesel AI, learnjev.com FAQ, refix.ai), egyik forrás sem T1, de mindhárom egybehangzó, és saját ellenőrzésem (a hivatalos oldalstruktúrán, `typesafe.ai/legal/*` és `docs.typesafe.ai` linkek között) sem talált külön ártáblázat-oldalt — az ár egyedül a launch blogposztban és a `typesafe.ai/models` oldalon szerepel (ez utóbbit SQ00 sem tudta közvetlenül lekérni).

Minimum díj: **nincs dokumentált minimum díj** magán az API-n (csak a gateway-eknél van minimum kártyás feltöltés, l. lentebb). Ingyenes keret: a hivatalos launch-poszt (2026-09-15) még várólistás „early access”-t ír le, publikált ingyenes csomag nélkül; **2026-09-20 után** több, egymástól független hírforrás (l. 2. pont) szerint minden új fiók **$5 promóciós kreditet** kap — ezt azonban **közvetlen hivatalos (typesafe.ai) oldalról nem tudtam megerősíteni** (a nyilvánosan elérhető blog- és jogi oldalak ezt nem tartalmazzák), csak konkordáns T2/T3 híroldalakról, amelyek egy hivatalos TypeSafe X/Twitter-posztra hivatkoznak.

Kontextus (a hivatalos blog összehasonlító táblázatából): a fennálló, nagy nyelvi modellek bemeneti ára a blog szerint „$0.20 to $10 / MTok", a Jev-é „$0.042 / MTok" — a cég saját 238×-os (eesel AI szerinti) állítása erre az összevetésre épül.

## 2. Elszámolási modell

### 2.1 TypeSafe hivatalos API — kredit-rendszer (MCA)

A Master Customer Agreement (typesafe.ai/legal/mca, utolsó frissítés 2026-08-27, T1) **kifejezetten kredit-alapú elszámolást ír le**, nem pusztán utólagos, tokenenkénti számlázást:

> „In order to generate Output or otherwise use the Services, Customer must obtain TypeSafe-managed credits that are consumed by each Input submitted to the Services through Customer's account (each, a 'Credit'). Credits include Credits purchased by Customer… ('Purchased Credit') and Credits that TypeSafe, at its sole discretion, issues to Customer at no cost… ('Promotional Credits')."

> „Customer may view Customer's current Credit balance in Customer's account."

> „Credits (y) are not redeemable, refundable, transferable, or legal tender or currency, and (z) do not constitute or confer upon Customer any personal property right."

Automatikus feltöltés **opt-in**:

> „if Customer's Credit balance reaches zero (or falls below the applicable threshold)… then (y) if Customer has opted in to automatic Purchased Credit refills, TypeSafe will automatically add to Customer's Credit balance a number of Credits equal to the refill dollar amount… selected at the time of the opt in, or (z) if Customer has not opted in… TypeSafe may decline to generate Output in response to Customer's submission of Input."

Purchased Credit lejárat: „expire on the earlier of (y) the end of the Term and (z) the date that is 12 months after the purchase date." Promotional Credit előbb fogy el, mint a Purchased: „such Promotional Credits will be consumed prior to the consumption of any of Customer's then-available Purchased Credits."

**Ez pontosítja SQ00-t**: az előző kutatási kör azt állította, hogy „nincs hivatalos, publikált előre-feltöltött 'balance'/kredit rendszer… a TypeSafe saját API-jánál" — ez a MCA fényében **téves vagy legalábbis félrevezető** volt (l. „Ellentmondások"). A MCA egyértelműen a `typesafe.ai` checkout oldalára és a `console.typesafe.ai`-ra is vonatkozik („the entity identified as 'Customer' in… the checkout page on TypeSafe's website"), tehát nem csak nagyvállalati szerződésekre.

Havidíj/subscription: **nincs dokumentált fix havidíj** — egy T3 aggregátor (jevplayground.com) egyenesen idézi a MCA-t: „TypeSafe's current public terms describe API usage through Credits consumed by each submitted Input. They do not describe a required fixed monthly API subscription for self-serve usage." Ezt a saját, közvetlen MCA-olvasásom is alátámasztja: a 8. szakasz kizárólag Credit-alapú fogyasztást ír le, subscription-tier-t nem.

### 2.2 Gateway-ek elszámolási modellje

**OpenRouter** — előre feltöltött, prepaid kredit-egyenleg fiókszinten, plusz opcionális, kulcsonkénti költési limit:

> „Account balance — your available credits across the account… Per-key credit limits — an optional spending cap configured on an individual API key." (OpenRouter hivatalos dokumentáció, „API Credit & Rate Limits", T1)

Egyenleg API-n lekérdezhető: `GET /credits` → `{"data":{"total_credits":…, "total_usage":…}}`; kulcsonkénti limit: `GET /api/v1/key` → `limit`, `limit_reset`, `limit_remaining` mezők (T1, OpenRouter API referencia).

**Vercel AI Gateway** — kétszintű: ingyenes tier havi „included credit”-tel (alacsonyabb rate limitekkel), és fizetős tier vásárolt „AI Gateway Credits”-szel, plusz **budget** (költségkeret) réteg, ami külön a hitel-egyenlegtől:

> „Budgets limit usage; they do not reserve or purchase capacity. Your team still needs credits or a payment method to make requests." (Vercel hivatalos dokumentáció, „Budgets and Spend Limits", T1)

Automatikus feltöltés (auto top-up) elérhető: „You can configure auto top-up to automatically add AI Gateway Credits when your balance falls below a threshold… AI Gateway automatically charges your payment method and adds the configured amount to your balance." Egyenleg API-n is lekérdezhető: „`GET /v1/credits` returns your credit balance and lifetime spend." (Vercel AI Gateway FAQ, T1)

**Cloudflare AI Gateway** — kétféle mód gateway-enként választható: „Standard billing" (a Cloudflare-számla végén terhelve) vagy „Unified Billing" (előre feltöltött Cloudflare-kredit, valós idejű levonással):

> „To use Unified Billing, you must purchase and load credits into your Cloudflare account in the Cloudflare dashboard… A 5% fee is applied to all credits purchased through Unified Billing. For example, a $100 credit purchase will result in a $105 charge. Inference pricing from providers is passed through with no markup." (Cloudflare AI Gateway hivatalos dokumentáció, „Unified Billing", T1)

A Jev/TypeSafe modell mindhárom gateway-en megjelenik hivatalos modell-oldalon: OpenRouter (`typesafe/jev-1.13`), Vercel (`typesafe-ai/jev`, hivatalos guide: „$0.042 per 1M input tokens", ZDR és No-Training opció per kérés), Cloudflare Workers AI (`typesafe/jev`, „View pricing in the Cloudflare dashboard").

## 3. Mi történik PONTOSAN, ha elfogy az egyenleg / túllépjük a keretet

### 3.1 TypeSafe hivatalos API

A hivatalos API-referencia (docs.typesafe.ai, T1, közvetlenül lekérve) **teljes, dokumentált hibakód-táblázata**:

> „Errors use standard HTTP status codes with a JSON body describing what went wrong.
> `401 Unauthorized` — Missing or invalid API key. Check the `Authorization` header.
> `422 Unprocessable Entity` — The request body failed validation — for example a missing required field or a malformed question. The body details the offending field.
> `429 Too Many Requests` — You have exceeded your rate limit. Back off and retry after a short delay.
> `529 Overloaded` — TypeSafe is temporarily overloaded. Retry after a short delay."

Ebben a hivatalos táblázatban **nincs 402 és nincs „insufficient credit" / „quota exceeded" kód** — ezt legalább három, egymástól független, a hivatalos SDK-kra hivatkozó közösségi forrás is megerősíti (a Python SDK kivétel-hierarchiáját dokumentáló `docs.typesafe.ai/sdk/python/api/exceptions.md`, T1, ugyanezt a négy kódot + 400/403/404-et sorolja; a nem hivatalos Elixir „typesafe_api" hexdocs és a Rust „typesafe-jev" docs.rs crate is ugyanezt a négy „elsődleges" kódot listázza, kifejezetten „mirrors the official TypeSafe SDKs" megjegyzéssel). A `learnjev.com` „production checklist" (T3) ugyanezt írja, és külön kiemeli: „The error body shape is undocumented… There is no published schema — no documented `error.type` or `error.message`."

A MCA (8.2(a), l. fent) csak ennyit mond a kredit-kifogyásról: **„TypeSafe may decline to generate Output in response to Customer's submission of Input."** — ez jogi, nem API-szintű megfogalmazás; **nincs hivatalos forrás arra, PONTOSAN milyen HTTP-kóddal/hibaformátummal** valósul ez meg technikailag (l. „Amire nincs forrás").

Előzetes figyelmeztetés / egyenleg API-n való lekérdezhetősége: a MCA csak annyit mond, hogy a Credit-egyenleg a „Customer's account"-ban (feltehetően a `console.typesafe.ai` webes felületen) tekinthető meg — **nem találtam hivatalos forrást külön, programozott (API-n keresztüli) egyenleg-lekérdező végpontra** a `api.typesafe.ai`-n (l. „Amire nincs forrás").

### 3.2 OpenRouter — 402, dokumentált testtel

> „402: Your account or API key has insufficient credits. Add more credits and retry the request." (OpenRouter hivatalos „API Error Handling and Debugging", T1)

Konkrét, dokumentált hibatest (OpenRouter TypeScript SDK hivatalos referenciája, T1):
```
{"error": {"code": 402, "message": "Insufficient credits. Add more using https://openrouter.ai/credits"}}
```

> „On 429 and 503 responses, and on 402 responses whose `error.metadata.limit_source` is `openrouter_in_flight_budget`… OpenRouter may include a standard HTTP `Retry-After` response header… A 402 without the header is not a wait-and-retry case; see Handling 402 errors." (OpenRouter hivatalos dokumentáció, T1)

Előzetes figyelmeztetés: nincs push-jellegű riasztás dokumentálva; a hivatalos ajánlás proaktív pollozás: „Monitor proactively. Call `GET /api/v1/key`… to track `limit_remaining` and usage before requests start failing." (OpenRouter hivatalos „API Credit & Rate Limits", T1)

### 3.3 Vercel AI Gateway — 402, típusos mezővel

> „Once spend reaches the limit, AI Gateway rejects further requests for that scope with an HTTP `402` response until the budget resets or you raise it. The `type` is always `quota_for_entity_exceeded`, and the `message` names the scope that was exceeded along with its current spend and limit." (Vercel hivatalos „Budgets and Spend Limits", T1)

A hivatalos FAQ két különböző 402-esetet különböztet meg (T1):

> „`402` whose `type` is not `quota_for_entity_exceeded` | The team does not have a positive credit balance | Add AI Gateway Credits" / „`402` with `quota_for_entity_exceeded` | A team, project, API key, or user budget has reached its limit | Wait for the budget to refresh or raise its limit"

Fontos árnyalat: „A budget is a soft cap, not a hard limit. The check runs at the start of each request, so the request that crosses the limit still completes and total spend can end up slightly over the budget." (Vercel hivatalos dokumentáció, T1)

Előzetes figyelmeztetés **VAN**, e-mailben, konfigurálható küszöbökkel: „Turn on email spend alerts to notify your team's usage notification recipients when usage crosses 50%, 75%, or 100% of a limit within a refresh period." (Vercel changelog, T1)

### 3.4 Cloudflare AI Gateway — 429, opcionális olcsóbb-modell-fallback

> „Spend limits let you set cost-based budgets on your AI Gateway. When cumulative spend reaches the limit within a time window, AI Gateway blocks further requests with a `429` response until the window resets." / „Block requests (default) - The request is rejected until the budget window resets. Fall back to a cheaper model - Create a Dynamic Route with a primary model and a fallback… When the primary model's budget is exceeded, AI Gateway automatically routes requests to the fallback model instead of blocking them." (Cloudflare AI Gateway hivatalos dokumentáció, „Spend limits", T1)

Fontos: ez a **429-es válasz a konfigurálható „Spend limit" szabályra** vonatkozik. Arra, hogy magának az előre feltöltött Unified Billing-egyenlegnek a nullára fogyása pontosan milyen HTTP-választ ad (nem a Spend limit szabály, hanem maga a hitelkeret kimerülése), **nem találtam külön, explicit hivatalos idézetet** (l. „Amire nincs forrás").

## 4. Nem elérhetőség: időtúllépés, 429, 5xx — gyártói ajánlás és gateway-fallback

**TypeSafe hivatalos ajánlása** (docs.typesafe.ai, „Handling rate limits", T1, közvetlenül lekérve):

> „When you receive a `429 Too Many Requests` or `529 Overloaded` response, retry the request with exponential backoff instead of retrying immediately. Our client SDKs handle this automatically, so no extra handling is needed if you use one of our SDKs with its default retry policy."

Ezt konzisztensen megerősíti minden vizsgált (nem hivatalos, de „mirrors the official SDK" jelzéssel ellátott) kliens-implementáció: a hivatalos Python SDK kivétel-táblája retryable kategóriaként a 429/5xx-et jelöli (docs.typesafe.ai, T1); az Elixir és Rust community SDK-k (docs.rs, hexdocs, T2/T3, de mindegyik kifejezetten „mirrors the official TypeSafe SDKs" retry-politikát ír le) egyöntetűen: 2 újrapróbálkozás, 0,5 mp kezdő késleltetés, duplázódó backoff 5 mp plafonig, `Retry-After`/`retry-after-ms` fejléc tiszteletben tartása, ~30 mp teljes időkeret.

Fontos technikai figyelmeztetés (community SDK-k, T2/T3, konzisztensen több forrásban): a `POST /v1/systemone` **nem idempotens és nincs idempotency-key**, ezért kapcsolati hiba/timeout esetén az újrapróbálkozás **dupla számlázás kockázatával jár** — ezért ezek a kliensek alapértelmezésben óvatosabbak timeout/connection-error újrapróbálásnál, mint 429/5xx esetén.

**Gateway-szintű fallback:**

- **OpenRouter**: dedikált `models` tömb — „The `models` parameter lets you automatically try other models if the primary model's providers are down, rate-limited, or refuse to reply due to content moderation… If the model you selected returns an error, OpenRouter will try to use the fallback model instead." (OpenRouter hivatalos „Model Fallbacks", T1). Emellett automatikus, alapértelmezetten bekapcsolt „provider-layer failover" is van ugyanazon modellen belül, más szolgáltatóra: „For a single model served by multiple providers, OpenRouter automatically tries the next provider when the chosen one returns a 5xx or rate-limits." (T1). **Nem találtam közvetlen, hivatalos példát arra, hogy ez a `models` fallback kifejezetten a Jev „decision”-végponton (nem a chat/completions API-n) is elérhető-e** — a dokumentált példák chat/completions-modellekre vonatkoznak (l. „Amire nincs forrás").
- **Vercel AI Gateway**: „AI Gateway routes requests across providers and fallback models… Provider failover: Route a model across healthy providers and configure ordered provider and model fallbacks." (Vercel hivatalos „AI Gateway" áttekintő oldal, T1). BYOK-specifikus fallback is van: „If a BYOK request fails, AI Gateway can fall back to system credentials." (T1)
- **Cloudflare AI Gateway**: explicit `fallback` lánc és `cf-aig-step` válaszfejléc jelzi, melyik lépés szolgálta ki a kérést: „Cloudflare can trigger your fallback provider in response to request errors or predetermined request timeouts." (Cloudflare hivatalos „Fallbacks", T1). Emellett gateway-szintű, konfigurálható újrapróbálkozás is van kliens-kód nélkül: „Retry count — the maximum number of retry attempts (up to 5). Delay — the base delay between retries… Backoff — the backoff strategy… Constant, Linear, or Exponential." (Cloudflare hivatalos „Manage gateways", T1)

A **hivatalos TypeSafe API-nak magának nincs beépített fallback-mechanizmusa** — ez csak a gateway-rétegben létezik.

**Kiesési előzmény**: a TypeSafe hivatalos, publikus státusz-oldala (`status.typesafe.ai`, T1) 90 napos uptime-ot mutat `api.typesafe.ai`-ra 99,85–99,86% körüli értékkel, néhány perces-órás incidensekkel (pl. „Console is unavailable", 2026-09-21, feloldva ugyanaznap). Egy T3 forrás (jevaiguide.com) szerint a launch napján (szept. 15.) a kereslet átmenetileg szolgáltatás-kimaradást okozott, TechCrunch-ra hivatkozva — ezt a TechCrunch-cikkből közvetlenül nem tudtam idézni, csak másodkézből.

## 5. Szállítói kockázat

**Cégkor és finanszírozás** — BusinessWire hivatalos sajtóközlemény (T1, elsődleges céghír):

> „SAN FRANCISCO--(BUSINESS WIRE)--TypeSafe AI, a frontier AI lab building machine-native, composable AI, today emerged from stealth with $40 million in seed funding led by DCVC. Founded by former OpenAI researcher and co-inventor of RLHF/ChatGPT, Diogo Almeida, with Erik Gafni and Sasha Sheng… Founded in 2024 and headquartered in San Francisco, TypeSafe has raised approximately $40 million in funding led by DCVC. Early access to its first frontier model, Jev, is waitlisted at typesafe.ai."

Forbes (T1 újságírás, 2026-09-15): a cég ~200 millió dolláros értékelésen jutott a 40M-hez („This $200 Million Startup..."). Egy T3 elemzés (sylt.ing) felhívja rá a figyelmet, hogy a Dealroom nevű adatbázis csak 25,9 millió dollárt sorol a seed-körből, szemben a cég saját 40 milliós állításával — ezt az ellentmondást a T3 forrás maga is jelzi, független megerősítés nélkül.

**Early access státusz** — a hivatalos launch-poszt (2026-09-15, T1) még várólistás korlátozott hozzáférést ír le: „Our first public model is Jev, available today in early access… bringing developers off the waitlist as quickly as we can." Legalább hat, egymástól független hírforrás (jevainews.com, techstrong.ai, dev.to, cryptobriefing.com, ainewscrypto.com, cryptoinfo.ch — mind T2/T3, de tartalmilag konzisztensek és egy közös elsődleges forrásra, a TypeSafe hivatalos X/Twitter-posztjára hivatkoznak) szerint **2026-09-20-án a várólistát megszüntették**, és minden új fiók **$5 kezdő kreditet** kap. Ugyanakkor egy másik T3 forrás (jevaiplayground.com, utolsó ellenőrzés 2026-09-24) szerint **2026-09-22-én a regisztrációt átmenetileg ismét szüneteltették** — ezt más, ugyanabból az időszakból (szept. 22.) származó forrás nem erősíti meg egyértelműen (l. „Ellentmondások"). A kutatás lezárásának napján (2026-09-25) a pontos, éppen aktuális önkiszolgáló hozzáférési állapot ezért **bizonytalan**.

**A szolgáltatás jogi minősítése „preview"-ként, korlátozott felelősséggel** — a `typesafe.ai/terms-and-conditions` (2025-11-19, T1):

> „User understands and acknowledges that User is receiving access to a preview version of the Interfaces and that the Interfaces may not be suitable for use in a production environment."

> „Typesafe may suspend User's access to and use of the Interfaces or terminate this Agreement, and all permissions or rights granted to User under this Agreement, in each case, immediately at any time for any reason."

> „Typesafe may update the Interfaces from time to time without notice (including to add or remove features or functionality), and any such update may adversely affect the performance or availability of the Interfaces… Typesafe does not guarantee that User's access to the Interfaces will be uninterrupted."

> „UNDER NO CIRCUMSTANCES WILL TYPESAFE BE LIABLE TO USER… FOR (A) ANY CONSEQUENTIAL, INDIRECT, INCIDENTAL, EXEMPLARY, PUNITIVE, RELIANCE, OR SPECIAL DAMAGES, OR ANY DAMAGES RELATED TO LOSS OF DATA, OR (B) AGGREGATE TOTAL DAMAGES OR LIABILITY OF ANY KIND IN EXCESS OF $50 USD."

**Árváltozás / megszüntetés feltételei** — a weboldal Terms of Use (`typesafe.ai/legal/terms`, T1):

> „TypeSafe reserves the right to modify or discontinue the Site at any time (including by limiting or discontinuing certain features of the Site), temporarily or permanently, without notice to you. TypeSafe will have no liability for any change to the Site or any suspension or termination of your access to or use of the Site."

A Master Customer Agreement (fizetős/API-szerződés, T1) egyoldalú módosítást enged, 60 napos előzetes értesítéssel:

> „TypeSafe may from time to time notify Customer of updates to this Agreement (including by displaying a notification on the Services). Unless a later date is specified by TypeSafe, such updated version of this Agreement will become effective on a going forward basis on the date that is at least 60 days after the date on which TypeSafe provided such notice to Customer."

Megszűnéskor a fel nem használt, előre kifizetett kredit **nem jár vissza**:

> „TypeSafe will have no obligation to provide any compensation or refund for any prepaid amounts not consumed as of the effective date of such termination or expiration."

A cég maga is elismeri, hogy az ár fenntarthatósága bizonytalan (a hivatalos launch-blogot idézve, eesel AI aggregátoron keresztül, T2 — a mondat eredete a hivatalos blog, de a pontos forrás-elérést nem sikerült közvetlenül reprodukálnom):

> „We make our pricing transparent. We can't prove it isn't subsidized; we'll need the long-term to prove the sustainability of our pricing (which we expect to go down, not up)."

Összegzésül: a szolgáltató **kevesebb mint két hetes nyilvános múltú, „preview"-ként jogilag minősített, bármikor felfüggeszthető/megszüntethető** korai fázisú startup-termék, alacsony ($50) szerződéses felelősségkorlátozással, vissza nem térítendő előre fizetett kreditekkel, és — saját bevallása szerint is — bizonytalan hosszú távú árazási fenntarthatósággal.

## Ellentmondások

1. **A kredit-rendszer létezése**: az előző kutatási kör (SQ00) azt állította, hogy „nincs hivatalos, publikált előre-feltöltött 'balance'/kredit rendszer és nincs publikált ingyenes csomag a TypeSafe saját API-jánál". A jelen kör a Master Customer Agreement (typesafe.ai/legal/mca, T1) közvetlen elolvasásával **kifejezett, hivatalos Credit-rendszert talált** (Purchased + Promotional Credits, opcionális automatikus feltöltés). A korábbi állítás vagy nem találta meg a MCA-t, vagy a „nincs önkiszolgáló, azonnal kártyás pricing-oldal" tényét tévesen általánosította „nincs kredit-rendszer"-ré. A két állítás nem ugyanazt a dokumentumkört vizsgálta.
2. **Várólista státusza, 2026-09-25-én**: hat, egymástól független, de egy közös (nem hivatalos módon hozzáférhető) TypeSafe-Twitter-posztra visszavezethető hírforrás szerint 2026-09-20-tól nincs várólista és van $5 kezdő kredit; egy másik forrás (jevaiplayground.com, T3) szerint 2026-09-22-én a regisztrációt újra szüneteltették; egy harmadik, ugyanaznapi forrás (dev.to, 2026-09-22) még „open registration"-ként írja le. Ezt közvetlen, hivatalos typesafe.ai-forrásból **nem sikerült egyértelműen tisztázni** — az utolsó általam elért hivatalos blog-verzió (2026-09-14/15) még várólistás állapotot ír le.
3. **Két, átfedő de eltérő jogi dokumentum**: a `typesafe.ai/terms-and-conditions` (2025-11-19, „preview Interfaces", $50 felelősségkorlát, bármikor bármely okból felfüggeszthető) és a `typesafe.ai/legal/mca` (2026-08-27, Credit-rendszer, csak meghatározott okokból azonnal felfüggeszthető, 60 napos módosítási értesítés) tartalmilag részben átfedő, részben ellentmondó szabályokat tartalmaz (pl. eltérő felfüggesztési feltételek). Nyilvános forrásból nem derül ki egyértelműen, hogy az önkiszolgáló (nem-enterprise) Jev-felhasználókra melyik dokumentum az irányadó ma, vagy hogy az újabb (MCA) hatályon kívül helyezte-e a régebbit (preview ToS).
4. **Finanszírozás összege**: a cég és a BusinessWire-sajtóközlemény (T1) ~40 millió dollárt állít, a Forbes (T1) ~200 millió dolláros értékelést közöl ehhez; egy T3 elemzés (sylt.ing) szerint a Dealroom adatbázis csak 25,9 millió dollárt regisztrál a körből — ezt egyetlen, nem elsődleges forrás állítja, független megerősítés nélkül.

## Amire NINCS forrás

- **A pontos HTTP-válasz (kód + hibatest) a hivatalos TypeSafe API-n**, amikor a Credit-egyenleg elfogy és nincs automatikus feltöltés — a hivatalos hibakód-táblázat (401/422/429/529) ezt nem tartalmazza, a MCA csak jogi szinten („may decline to generate Output") fogalmaz.
- **Programozott (API-n keresztüli) egyenleg-lekérdező végpont** a hivatalos `api.typesafe.ai`-n — a MCA csak a webes fiókfelületen (`console.typesafe.ai`) való megtekintést említi.
- **Előzetes (pl. e-mail/webhook) figyelmeztetés a kredit-kifogyás előtt** a hivatalos TypeSafe API-n — nincs erre utaló hivatalos dokumentáció.
- **A jelenlegi (2026-09-25-i), önkiszolgáló regisztráció pontos állapota** (nyitott-e, vagy szünetel) — ellentmondó, kizárólag T3 forrásokból származó állítások, hivatalos megerősítés nélkül.
- **Az OpenRouter `models` fallback-tömb kifejezett működése a Jev/„decision" végponton** (a dokumentált példák chat/completions-modellekre vonatkoznak).
- **A Cloudflare AI Gateway Unified Billing előre feltöltött egyenlegének nullára fogyása esetén adott pontos HTTP-válasz** (megkülönböztetve a külön konfigurálható „Spend limit" szabály 429-es válaszától, amit sikerült dokumentálni).
- **Konkrét, publikált minimum díj** a hivatalos TypeSafe API-n (csak a gateway-eknél van dokumentált minimum kártyás feltöltés, pl. OpenRouterön ~5 USD, ez azonban maga OpenRouter, nem TypeSafe szabálya).

## Meglátogatott és felderített linkek

| Cím | URL | Tier | Eszköz | Megjegyzés |
|---|---|---|---|---|
| Introducing System One Models & Jev (TypeSafe blog) | https://typesafe.ai/blog/introducing-system-one-models-and-jev | T1 | web_fetch_exa | Hivatalos árazás ($0,042/MTok, kimenet ingyenes) közvetlen idézete |
| Master customer agreement | https://typesafe.ai/legal/mca | T1 | web_fetch_exa | Hivatalos Credit-rendszer (8.2. szakasz), felfüggesztés, megszűnés, 60 napos módosítási szabály |
| Terms of Service (preview Interfaces) | https://typesafe.ai/terms-and-conditions | T1 | web_fetch_exa | „Preview" minősítés, $50 felelősségkorlát, bármikor felfüggeszthető |
| Terms of use (Site) | https://typesafe.ai/legal/terms | T1 | web_search_exa (highlight) | Site bármikor módosítható/megszüntethető, értesítés nélkül |
| Data processing addendum | https://typesafe.ai/legal/data-processing | T1 | web_search_exa (highlight) | DPA, korábbi körben már azonosítva |
| Acceptable Use Policy | https://typesafe.ai/legal/acceptable-use-policy | T1 | web_search_exa (highlight) | AUP, MCA-ra hivatkozik |
| API reference (evaluation endpoint) | https://docs.typesafe.ai/api.md | T1 | web_fetch_exa | Kérés/válasz formátum, `/v1/systemone` |
| Introduction | https://docs.typesafe.ai/introduction | T1 | web_fetch_exa | Termékleírás, primitívek |
| Quick start | https://docs.typesafe.ai/introduction/quickstart | T1 | web_fetch_exa | cURL/SDK példa, `TYPESAFE_API_KEY` |
| Exceptions (Python SDK) | https://docs.typesafe.ai/sdk/python/api/exceptions.md | T1 | web_fetch_exa | Hivatalos hibaosztályok: 400/401/403/404/422/429/5xx |
| Errors and retries (llms-full.txt) | https://docs.typesafe.ai/llms-full.txt | T1 | web_search_exa (highlight) | **Hivatalos hibakód-táblázat**: 401/422/429/529 + exponenciális backoff ajánlás, szó szerint idézve |
| Typesafe AI status | https://status.typesafe.ai/ | T1 | web_search_exa (highlight) | Hivatalos uptime-oldal, ~99,85% |
| Console is unavailable (incident) | https://status.typesafe.ai/incident/1070098 | T1 | web_search_exa (highlight) | 2026-09-21-i incidens, feloldva |
| TypeSafe AI Emerges From Stealth With $40M (BusinessWire) | https://www.businesswire.com/news/home/20260915525333/en/ | T1 | web_search_exa (highlight) | Hivatalos sajtóközlemény: alapítás 2024, $40M seed, DCVC |
| This $200 Million Startup Wants To Fix AI's Overconfidence Problem (Forbes) | https://www.forbes.com/sites/the-prompt/2026/09/15/ | T1 | web_search_exa (highlight) | Elsődleges újságírás, értékelés, Almeida-idézetek |
| ChatGPT Co-Creator Launches Jev (vktr.com) | https://www.vktr.com/ai-platforms/chatgpt-cocreator-launches-typesafe-ai-with-jev/ | T2 | web_search_exa (highlight) | Alapítók háttere, launch-részletek |
| API Error Handling and Debugging (OpenRouter) | https://openrouter.ai/docs/api_reference/errors-and-debugging | T1 | web_search_exa (highlight) | Hivatalos hibakód-táblázat, 402 leírás, Retry-After szabály |
| API Credit & Rate Limits (OpenRouter) | https://openrouter.ai/docs/api_reference/limits | T1 | web_search_exa (highlight) | Account balance vs. per-key limit, proaktív monitorozás ajánlása |
| PaymentRequiredResponseError (OpenRouter TS SDK) | https://openrouter.ai/docs/agent-sdk/typescript/errors/paymentrequiredresponseerror | T1 | web_search_exa (highlight) | Pontos 402 JSON-hibatest |
| Get remaining credits (OpenRouter) | https://openrouter.ai/docs/api/api-reference/credits/get-remaining-credits | T1 | web_search_exa (highlight) | `GET /credits` végpont sémája |
| Model Fallbacks (OpenRouter) | https://openrouter.ai/docs/guides/routing/model-fallbacks | T1 | web_search_exa (highlight) | Hivatalos `models` fallback-tömb dokumentáció |
| Provider Routing (OpenRouter) | https://openrouter.ai/docs/guides/routing/provider-selection | T1 | web_search_exa (highlight) | Provider-szintű automatikus failover |
| AI Gateway Budgets and Spend Limits (Vercel) | https://vercel.com/docs/ai-gateway/observability-and-spend/budgets | T1 | web_search_exa (highlight) | 402 + `quota_for_entity_exceeded`, soft cap, e-mail riasztás |
| AI Gateway Rate Limits (Vercel) | https://vercel.com/docs/ai-gateway/rate-limits | T1 | web_search_exa (highlight) | 429 vs. 402 megkülönböztetése |
| AI Gateway FAQ (Vercel) | https://vercel.com/docs/ai-gateway/faq | T1 | web_search_exa (highlight) | Hibakód-táblázat összefoglalva, `GET /v1/credits` |
| AI Gateway Pricing (Vercel) | https://vercel.com/docs/ai-gateway/pricing | T1 | web_search_exa (highlight) | Auto top-up mechanizmus |
| AI Gateway (áttekintés, Vercel) | https://vercel.com/docs/ai-gateway | T1 | web_search_exa (highlight) | Provider/model fallback, BYOK-fallback |
| How to classify, route, and score with Jev and AI SDK (Vercel) | https://vercel.com/kb/guide/typesafe-jev-and-ai-sdk | T1 | web_search_exa (highlight) | Jev a Vercel AI Gateway-en, ár, ZDR/No-Training opció |
| Jev (typesafe) — Cloudflare AI docs | https://developers.cloudflare.com/ai/models/typesafe/jev/ | T1 | web_search_exa (highlight) | Jev modell-oldal Cloudflare-en |
| Fallbacks — Cloudflare AI Gateway | https://developers.cloudflare.com/ai-gateway/configuration/fallbacks/ | T1 | web_search_exa (highlight) | `cf-aig-step` fejléc, fallback-lánc |
| Spend limits — Cloudflare AI Gateway | https://developers.cloudflare.com/ai-gateway/features/spend-limits/ | T1 | web_search_exa (highlight) | 429 spend-limit túllépésnél, olcsóbb modellre váltás opció |
| Unified Billing — Cloudflare AI Gateway | https://developers.cloudflare.com/ai-gateway/features/unified-billing/ | T1 | web_search_exa (highlight) | Előre feltöltött kredit, 5%-os díj |
| Manage gateways — Cloudflare AI Gateway | https://developers.cloudflare.com/ai-gateway/configuration/manage-gateway/ | T1 | web_search_exa (highlight) | Gateway-szintű retry-konfiguráció (count/delay/backoff) |
| Jev Pricing Calculator (jevplayground.com) | https://jevplaygound.com/jev-pricing (elért URL: jevplayground.com/jev-pricing) | T3 | web_search_exa (highlight) | MCA-t idéző aggregátor, „no fixed subscription" |
| TypeSafe Jev pricing 2026 (eesel AI) | https://www.eesel.ai/blog/typesafe-jev-pricing | T3 | web_search_exa (highlight) | 404-es pricing-oldal megerősítése, fenntarthatósági idézet |
| Jev pricing, latency, and benchmarks (Refix) | https://www.refix.ai/news/jev-pricing-latency-benchmarks/ | T3 | web_search_exa (highlight) | Rate limit számok (250k tok/s, 1200 req/perc) |
| Jev FAQ (Learn Jev) | https://learnjev.com/faq | T3 | web_search_exa (highlight) | Nincs publikált ingyenes csomag (2026-09-20 előtti állapot) |
| Shipping Jev to production: a checklist (Learn Jev) | https://learnjev.com/tutorials/production-checklist | T3 | web_search_exa (highlight) | Hibakód-táblázat, „undocumented error body shape" |
| Jev 429 Too Many Requests (Jev AI Guide) | https://jevaiguide.com/errors/429-too-many-requests/ | T3 | web_search_exa (highlight) | Backoff-kód-példa, retry-after viselkedés |
| OpenRouter 402 Insufficient Credits for Jev (Jev AI Guide) | https://jevaiguide.com/errors/402-insufficient-credits/ | T3 | web_search_exa (highlight) | OpenRouter 402 Jev-specifikus költségpélda |
| Is Jev Down? (Jev AI Guide) | https://jevaiguide.com/is-jev-down/ | T3 | web_search_exa (highlight) | Uptime-történet, launch-napi kapacitásprobléma (TechCrunch-ra hivatkozva) |
| Jev API docs (jevtypesafeai.com, NEM hivatalos) | https://jevtypesafeai.com/docs | T3 | web_search_exa (highlight) | Nem hivatalos wrapper saját 402 „insufficient_credits" kódja — NEM a TypeSafe hivatalos API kódja |
| Terms of Service (jevtypesafeai.com, NEM hivatalos) | https://jevtypesafeai.com/terms | T3 | web_search_exa (highlight) | Explicit „not affiliated with TypeSafe AI"; saját prepaid-rendszer |
| Jev pricing (jevtypesafeai.com, NEM hivatalos) | https://jevtypesafeai.com/pricing | T3 | web_search_exa (highlight) | Nem hivatalos felár (kb. 10×) a hivatalos árhoz képest |
| TypeSafe drops the Jev waitlist (jevainews.com) | https://jevainews.com/news/jev-no-waitlist/ | T2/T3 | web_search_exa (highlight) | 2026-09-20 várólista megszűnése, $5 kredit, TypeSafe-tweetre hivatkozva |
| TypeSafe Opens Jev for General Availability (techstrong.ai) | https://techstrong.ai/features/typesafe-opens-jev-for-general-availability/ | T2 | web_search_exa (highlight) | Független megerősítés: $5 kredit |
| Jev is now open to everyone (dev.to) | https://dev.to/li_alex_1ea2dbc2e3e338609/jev-is-now-open-to-everyone-what-a-system-one-model-costs-and-how-to-start-with-5-in-free-4jal | T2/T3 | web_search_exa (highlight) | Független megerősítés: $5 kredit, 2026-09-22 |
| TypeSafe opens Jev AI to public (cryptobriefing.com) | https://cryptobriefing.com/typesafe-jev-ai-public-access/ | T2/T3 | web_search_exa (highlight) | Független megerősítés a várólista megszűnésére |
| Typesafe opens Jev to the public with $5 credits (ainewscrypto.com) | https://www.ainewscrypto.com/news/typesafe-opens-jev-to-the-public-with-5-credits-as-builders-wire-it-into-sub-second-bots | T2/T3 | web_search_exa (highlight) | Független megerősítés |
| TypeSafe opens Jev AI to public (cryptoinfo.ch) | https://cryptoinfo.ch/typesafe-opens-jev-ai-to-public-after-rapid-adoption-forces-waitlist-removal/ | T2/T3 | web_search_exa (highlight) | Független megerősítés |
| Jev $5 starter credit: pricing and current signup status (jevaiplayground.com) | https://www.jevaiplayground.com/blog/jev-open-access-free-credit | T3 | web_search_exa (highlight) | Állítás: 2026-09-22-én szüneteltették az új regisztrációt — ellentmondásban más forrásokkal |
| How to Start Using JEV (sellingwithnas.com) | https://www.sellingwithnas.com/how-to-start-using-jev-step-by-step | T3 | web_search_exa (highlight) | 2026-09-22: „you may land on a waitlist" — bizonytalan hozzáférési állapot |
| What Is Jev? Inside TypeSafe's Decision-Only AI Model (firecrawl.dev) | https://www.firecrawl.dev/blog/what-is-jev | T2/T3 | web_search_exa (highlight) | Vercel AI Gateway integráció dátuma (szept. 16.) |
| RLHF Co-Inventor Raised 40 Million (sylt.ing) | https://sylt.ing/blogs/2534/RLHF-Co-Inventor-Raised-40-Million-to-Sell-AI-Decisions | T3 | web_search_exa (highlight) | Dealroom vs. cég saját összeg-ellentmondás; figyelmeztetés nem hivatalos viszonteladókra |
| TypeSafe Jev: The model built to kill chat (startuphub.ai) | https://www.startuphub.ai/ai-news/artificial-intelligence/2026/typesafe-jev-model-kills-chat | T2 | web_search_exa (highlight) | Alapítás, csapat háttere |
| TypeSafe AI's Jev Is Not an LLM (forkast.news) | https://forkast.news/typesafe-ais-jev-is-not-an-llm-and-that-may-be-the-point/ | T2 | web_search_exa (highlight) | ~200M értékelés, „no named production customers or revenue disclosed" |
| Jev — Overview, Features & Use Cases (beri.net) | https://www.beri.net/tools/typesafe-jev | T3 | web_search_exa (highlight) | Enterprise ZDR „contact for pricing" |
| TypeSafe (Opper.ai provider oldal) | https://opper.ai/provider/typesafe | T3 | web_search_exa (highlight) | Gateway-aggregátor ártábla |
| statusfield.com — api.typesafe.ai | https://statusfield.com/services/typesafe-ai/current-status-by-service/api-typesafe-ai | T3 | web_search_exa (highlight) | Harmadik fél uptime-tükrözés a hivatalos status-oldalról |
| TypeSafe posted an API and console outage (jevainews.com) | https://jevainews.com/news/typesafe-api-incident/ | T2/T3 | web_search_exa (highlight) | 2026-09-21-i incidens részletei, TypeSafe hivatalos X-posztjait idézve |

---

# SQ04 — Adatvédelem és megfelelés: mi történik a beküldött adattal

*Módszer: kizárólag Exa (`web_search_exa`, `web_fetch_exa`); egy helyen (OpenRouter ZDR-lista) `curl`-lal nyers JSON-t kérdeztem le szó szerinti ellenőrzésre, az utasításnak megfelelően. Alügynök-indítás (a `deep-web-research` skill teljes, több-ügynökös pipeline-ja) ebben a körben sem történt — ez egy egyszeri, célzott kutatási kör, ezért degradált, de Exa-only módban, kizárólag elsődleges (TypeSafe saját jogi oldalai, gateway-dokumentáció, EU-jogszabályszöveg) és jelölt harmadik feles forrásokra támaszkodva dolgoztam.*

## Rövid válasz

A TypeSafe saját, elsődleges jogi dokumentumai (Privacy Policy, Terms of Service, Master Customer Agreement, DPA) következetesen és szó szerint kimondják, hogy a beküldött promptot/Inputot **nem használják AI-modell tanítására**, és azt **harmadik félnek nem adják ki a saját alvállalkozóikon (subprocessor) kívül**; ugyanakkor a megőrzési idő nincs fix számban megadva, csak „amíg szükséges” jellegű megfogalmazás van, és a saját, publikus oldalaikon **nem találtam szó szerinti „zero data retention” kitételt** — a ZDR-ígéret („enterprise ügyfeleknek, privacy@typesafe.ai-on kérve”) csak harmadik feles (nem hivatalos) forrásokból (T3) igazolható vissza. A szolgáltatás hivatalosan **kizárólag az Egyesült Államokban fut** — ezt a TypeSafe saját Privacy Policy-ja szó szerint kimondja („The Services are hosted in the United States") —, EU-régió vagy EU-adatrezidencia nincs bejelentve. A DPA tartalmaz EU SCC-t (2021/914 modul 2/3) és UK Addendumot, tehát van szerződéses adatátviteli mechanizmus, de egy — egyetlen, nem hivatalos jogi elemzésből származó, más forrásból nem megerősíthető — állítás szerint a céget **nem találták meg** az EU–USA Data Privacy Framework hivatalos listáján. A szubfeldolgozó-lista (állítólag AWS, Modal, Slack, Google Workspace) csak innen a T3 forrásból ismert, a hivatalos `trust.typesafe.ai/subprocessors` oldal JavaScript-motorral (Vanta) renderelődik, ezért a kutatóeszközeimmel nem tudtam a tartalmát közvetlenül elolvasni. SOC 2 Type II-t a cég saját LinkedIn-oldala 2026-07-07-én bejelentette, de ezzel egy másik (nem hivatalos) forrás kifejezetten szembemegy, ISO 27001-re pedig csak egy megbízhatatlannak tűnő, feltehetően más céggel összekevert aggregátor-oldal hivatkozik. A három vizsgált gateway közül az OpenRouter és a Vercel AI Gateway **hivatalosan, dokumentáltan kínál ZDR-útválasztást a Jev/TypeSafe végpontra** (ez saját, a TypeSafe alapértelmezett szabályzatától független megállapodásuk eredménye), míg a Cloudflare (Workers AI-n és AI Gateway-en át) csak általános „nem tanítunk az ügyfél tartalmán” ígéretet és alapértelmezetten bekapcsolt, kikapcsolható naplózást dokumentál, kifejezett ZDR-címkét vagy EU-régió-garanciát a Jevre nem. Az EU AI Act és a GDPR szempontjából releváns elsődleges szövegeket (GDPR 22. cikk, AI Act 6. cikk (3) bekezdés és az 53. preambulumbekezdés, EDPB 28/2024 vélemény) megtaláltam és idézem, de arra, hogy ezek pontosan hogyan vonatkoznának egy memóriabejegyzés kategorizálására/elfogadására, sem a TypeSafe, sem más elsődleges forrás nem nyilatkozik — ez esetről esetre eldöntendő jogi kérdés, amiről nem vonok le következtetést.

## 1. TypeSafe hivatalos adatkezelés — mit mond a saját Privacy Policy / ToS / MCA / DPA

Forrásdokumentumok (mind `typesafe.ai` alatt, elsődleges, T1):
- Privacy Policy — `https://typesafe.ai/legal/privacy` (Last updated: **Nov 19, 2025**)
- Terms of Service (Playground/API preview-ra) — `https://typesafe.ai/terms-and-conditions` (Last updated: **Nov 19, 2025**)
- Terms of Use (weboldalra) — `https://typesafe.ai/legal/terms`
- Master Customer Agreement (MCA, fizető ügyfeleknek) — `https://typesafe.ai/legal/mca`
- Data Processing Addendum (DPA) — `https://typesafe.ai/legal/data-processing` (Last updated: **Apr 24, 2026**)
- Acceptable Use Policy (AUP) — `https://typesafe.ai/legal/acceptable-use-policy`

**Megőrzik-e a kérést/választ, meddig?**
- Privacy Policy, „Retention" szakasz: *„We retain personal data about you for as long as reasonably necessary to provide you with the Services, or otherwise in support of our business or commercial purposes. When you request that we do so, we take measures to delete your personal data or keep it in a form that does not permit identifying you when this personal data is no longer reasonably necessary for the purposes for which we process it, unless we are required by law to keep this data for a longer period."* — **nincs fix, számszerű megőrzési határidő**.
- DPA, Schedule I: *„Customer Personal Data will be retained for as long as necessary taking into account the purpose of the Processing, and in compliance with applicable laws, including laws on the statute of limitations and Data Protection Law."*
- MCA, „Term and Termination" szakasz: *„TypeSafe will be under no obligation to store or retain Customer Data and may delete Customer Data at any time in its sole discretion. Customer Confidential Information may be retained in TypeSafe's standard backups notwithstanding any obligation to delete the applicable Confidential Information but will remain subject to this Agreement's confidentiality restrictions."* — vagyis szerződés megszűnése (vagy közben) után a TypeSafe **bármikor, saját belátása szerint törölheti** az adatot, de arra sincs kötelezve, hogy törölje; biztonsági mentésben tovább élhet.

**Tanítanak-e rajta?**
- Privacy Policy: *„We collect the personal data you provide when you use the Services, including your prompts, data, instructions, and other input ('Input'). We will not train or fine tune any artificial intelligence or machine learning models on your prompts or other Input."*
- Ugyanott, „How We Use the Personal Data We Collect" alatt: *„We (1) will not train or fine tune any artificial intelligence or machine learning models on Input, and (2) will not disclose any Input to a third party other than our service providers."*
- ToS (API/Playground preview), 4. pont: *„Typesafe will not train or fine tune any artificial intelligence or machine learning models on Input"* és *„Typesafe will not disclose any Input or Output to a third party other than Typesafe's service providers."*
- MCA, 4.1: a TypeSafe kap egy tág, világméretű licencet az Input/Output/Customer Data feldolgozására a szolgáltatás nyújtásához, Telemetria előállításához és jogi megfelelés céljából, **de** kifejezetten: *„The foregoing license does not grant TypeSafe the right to, and TypeSafe will not, include Customer Data in a dataset used to train (i.e., to modify the model weights of) any artificial intelligence or machine learning models without Customer's prior consent."* — tehát az MCA-ban ez **ügyfél előzetes hozzájárulása nélkül tiltott**, nem feltétel nélkül tiltott, mint a Privacy Policy-ban.

**Naplóznak-e?**
- A publikus oldalakon nincs önálló „logging"/naplózási szakasz, de a ToS és az MCA is a „technical or usage logs" kifejezést használja a feldolgozható adatok között: ToS 4. pont: *„...any information collected by or through the Interfaces or otherwise made available to Typesafe by User during the Term, including any Inputs, Outputs, and technical or usage logs..."* — tehát a TypeSafe maga is elismeri, hogy technikai/használati naplókat vezet, és ezekre ugyanaz a „nem tanítunk, nem adjuk ki" korlátozás vonatkozik, mint az Inputra/Outputra.
- AUP: *„TypeSafe may monitor compliance with this AUP and investigate any violations."* — vagyis a TypeSafe saját maga (nem harmadik fél) hozzáférhet a tartalomhoz visszaélés-ellenőrzés céljából.

**Ki fér hozzá?**
- DPA 2.2: a TypeSafe nem adhatja el/oszthatja meg (CCPA-értelemben) a Customer Personal Data-t, és nem használhatja/tárolhatja/fedheti fel a Dokumentált Utasításokon kívüli célra.
- MCA 14 (Confidentiality): *„Recipient may disclose Confidential Information to its employees, agents, contractors, and other representatives having a legitimate need to know (including, where TypeSafe is Recipient, the subcontractors referenced in Section 15.10 (Subcontractors)), provided it remains responsible for their compliance with this Section 14 (Confidentiality) and they are bound to confidentiality obligations no less protective than this Section 14."* — tehát „need-to-know" elv, TypeSafe alkalmazottai/alvállalkozói férhetnek hozzá, titoktartási kötelezettséggel.
- Nemzetközi látogatóknak, régió: Privacy Policy, „International Visitors" szakasz — szó szerint: *„The Services are hosted in the United States ('U.S.'). If you choose to use the Services from the EEA, the UK or other regions of the world with laws governing data collection and use that may differ from U.S. law, then please note that you are transferring your personal data outside of those regions to the U.S. for storage and processing."* — ez egy **elsődleges, T1 forrásból szó szerint** megerősíti, hogy nincs EU-hosztolás, minden adat az USA-ba kerül.

## 2. Zero Data Retention (ZDR) — kinek jár, hogyan kérhető

- A TypeSafe saját publikus jogi oldalain (Privacy Policy, ToS, MCA, DPA, AUP) **nem találtam szó szerinti „zero data retention" vagy „ZDR" kifejezést** — ezek az oldalak csak az általános „nem tanítunk / nem adjuk ki" ígéretet tartalmazzák, fix megőrzési idő vagy nulla-megőrzési opció nélkül.
- A ZDR-ígéret harmadik feles (nem hivatalos, T3) forrásokból ismert:
  - jevaiguide.com: *„TypeSafe offers zero data retention (ZDR) to enterprise customers. […] Zero data retention on request. Enterprise customers can get ZDR by contacting privacy@typesafe.ai."* (`https://jevaiguide.com/typesafe-ai/`, `https://jevaiguide.com/faq/does-jev-train-on-your-data/`)
  - Ezt a sq00-azonosító kör két másik T3 forrása is megerősítette (`jevaiguide.com/faq`, `modemguides.com`), tehát legalább **három**, egymástól független, de mind harmadik feles forrás mondja ugyanezt — elsődleges (TypeSafe-saját) megerősítés viszont nincs.
- Ezzel szemben egy gateway-aggregátor/monitoring oldal (Opper.ai, T3) a TypeSafe közvetlen API-útvonalára kifejezetten *„Not established"* (nem kialakított) állapotot ír a Zero Data Retention mezőben: *„Zero data retention posture is not established for this route. No training on customer data."* (`https://opper.ai/provider/typesafe`) — lásd „Ellentmondások”.
- Fontos megkülönböztetés: a **gateway-ek saját ZDR-ajánlata** (OpenRouter, Vercel AI Gateway) a Jev végpontra **igenis dokumentáltan, hivatalosan elérhető** — ez azonban a gateway és a TypeSafe közötti külön megállapodás eredménye, nem azonos a TypeSafe saját, közvetlen API-jának alapértelmezett szabályzatával (lásd az 5. pontot).

## 3. Régió, EU-rezidencia, alfeldolgozók

- Régió: Privacy Policy (T1, lásd fent): *„The Services are hosted in the United States."* Ezt független, T2/T3 harmadik felek is megerősítik: requesty.ai (`https://www.requesty.ai/models/typesafe`): *„Location 🇺🇸 US"*; Opper.ai (`https://opper.ai/provider/typesafe`): *„Region: Multi (United States)"*. **Tehát legalább egy elsődleges (T1) és két független harmadik feles (T2/T3) forrás egybehangzóan USA-hosztolást mond, EU-régió sehol nincs bejelentve.**
- Alfeldolgozók (subprocessorok): a DPA 3.1 pontja a hivatalos listát a `https://trust.typesafe.ai/subprocessors` oldalra mutatja: *„Customer provides general authorization for Typesafe to engage the following subprocessors as described in https://trust.typesafe.ai/subprocessors."* Ez az oldal (és maga a `https://trust.typesafe.ai/` „Trust Center" főoldal is) egy Vanta-alapú, JavaScript-tel renderelt widget — az Exa `web_fetch_exa` eszközzel csak az üres HTML-vázat és a Vanta-betöltő szkriptet tudtam lekérni, **a tényleges tartalmat (mely cégek szerepelnek a listán) nem tudtam közvetlenül elolvasni.**
  - Az egyetlen konkrét névsor, amit találtam, egy nem hivatalos jogi elemzésből (T3) származik: Wunderlandmedia (`https://wunderlandmedia.com/typesafe-ai-jev-terms-of-service-gdpr`, szerző: Kemal Esensoy): *„The subprocessors, verified from the page: AWS stores and processes live request data, Modal processes prompts without storing them and is the one running inference, and Slack and Google Workspace handle support. Four companies, all US, no EU entity."* — ezt **más, független forrásból nem sikerült megerősítenem** (a `trust.modem.dev/subprocessors` oldal, amit találtam, egy másik cég — modem.dev — saját alfeldolgozó-listája, amin a TypeSafe *mint modem.dev alvállalkozója* szerepel, nem a TypeSafe saját alvállalkozó-listáját erősíti meg).
  - Ugyanez a forrás (Wunderlandmedia) egy szerződéses „kiskaput" is leír: a MCA „Third-Party Platform” fogalma (7. szakasz) szerinte kikerüli az alfeldolgozó-bejelentési kötelezettséget, és a Privacy Policy „potential transactional partners" kitétele (fenti idézet: „Merger, Sale, or Other Asset Transfers") miatt cégfelvásárlás esetén az adat gazdát cserélhet — ez egy **harmadik fél jogi értelmezése**, elsődleges forrásból nem tudtam külön ellenőrizni.

## 4. DPA, GDPR, EU–US adatátvitel (DPF, SCC), SOC 2 / ISO 27001

**DPA / GDPR-szerepek** — a TypeSafe DPA-ja (`https://typesafe.ai/legal/data-processing`, Last updated Apr 24, 2026) T1, szó szerint:
- 1.1: *„Customer is the 'controller' and 'business' […], and Typesafe is the 'processor' and 'service provider'."*
- 5.2 (biztonsági incidens): *„Typesafe will notify Customer without undue delay and in any case within 72 hours after becoming aware of any accidental or unauthorized access to, or disclosure or use of, Customer Personal Data."*
- 5.3 (audit): ügyfél saját költségén, évente legfeljebb egyszer auditálhatja a TypeSafe kontrolljait.
- 4.1 (érintetti jogok): a TypeSafe köteles továbbítani az ügyfélnek a hozzá beérkező érintetti kéréseket.

**EU–US adatátvitel:**
- DPA 6.1–6.3: a TypeSafe az Európai Bizottság 2021/914 végrehajtási határozata szerinti **EU SCC-ket** (2. modul: controller-to-processor, illetve 3. modul, ha az ügyfél maga is processzor) és a brit **UK Addendumot** alkalmazza az EEA-ból, illetve az Egyesült Királyságból történő adattovábbításra, és a svájci FADP-re vonatkozó szabályokat is rögzíti. Szó szerint: *„For transfers of Customer Personal Data from the European Union, Typesafe and Customer conclude Module 2 (controller-to-processor) […] of the EU SCCs…"* — tehát **van** szerződéses adatátviteli mechanizmus (SCC), ha egy magyar cég EU SCC-alapon akarna adatot küldeni.
- **EU–US Data Privacy Framework (DPF):** a hivatalos `dataprivacyframework.gov` keresőoldalát és résztvevő-listáját én magam nem tudtam megbízhatóan lekérdezni (a lista dinamikus, JavaScript-alapú, az Exa-lekérés csak töredékes/hibás táblázatot adott vissza). Az egyetlen konkrét állítás, hogy a TypeSafe **nincs** a DPF-listán, egy nem hivatalos jogi blogtól (T3, Wunderlandmedia) származik: *„TypeSafe is not certified under the EU-US Data Privacy Framework. I checked rather than assumed: the search box on dataprivacyframework.gov is broken, so I paged all 232 active participants under the letter T. The closest entry is Tynker."* Ez a sq00-kör azonos következtetésével egybevág, de **mindkét kör ugyanabból az egyetlen T3 forrásból** dolgozik — **nem sikerült két, egymástól független forrással megerősíteni**, csak a saját (sikertelen) próbálkozásommal konzisztens.
- **SOC 2 Type II:** a TypeSafe saját, hivatalos vállalati LinkedIn-oldala 2026-07-07-én bejelentette: *„At 11:39am I received the second most important Slack message I've received today — TypeSafe AI had officially become SOC 2 Type II compliant. […] thank our incredible partners, Vanta and Advantage Partners…"* (`https://www.linkedin.com/posts/typesafe-ai_activity-7480343405286313984-qWxZ`, szerző: TypeSafe AI hivatalos oldala). Ez a cég saját közlése (elsődlegesnek tekinthető, de nem szabályzat/jogi dokumentum, hanem közösségimédia-poszt). **Ezzel szemben** egy másik, T2/T3 forrás (HokAI, `https://hokai.io/hub/companies/typesafe-ai`) kifejezetten az ellenkezőjét állítja: *„TypeSafe AI has not published SOC 2, ISO 27001, or other third-party compliance certifications."* — lásd „Ellentmondások”.
- **ISO 27001:** nem találtam megbízható, elsődleges forrást. Egyetlen találat (`soc2c.com/company/akka`) állítja, hogy a „Typesafe Inc" ISO 27001-tanúsítvánnyal (és SOC 3, ISO 27018, ISO 22301, ISO 42001, HIPAA, PCI DSS, CSA STAR, NIST CSF minősítéssel) is rendelkezik, **de** ennek az oldalnak az URL-je („/company/akka") és a benne hivatkozott trust center (`trust.akka.io`) egy **másik cégre (Akka)** utal — ez valószínűleg egy aggregátor-oldal adatminőségi hibája/összekeverése, ezért **nem megbízható forrásként kezelem**, és a lista mögötti valós TypeSafe-tanúsítványokat nem tudom megerősíteni.
- A `trust.typesafe.ai` hivatalos Trust Center léte önmagában megerősített (a DPA is hivatkozik rá, és egy harmadik fél API-katalógus, `apis.io/providers/typesafe-ai/`, is említi: *„a Vanta trust center"*), de **a benne felsorolt konkrét tanúsítványok tartalmát a JS-renderelés miatt nem tudtam elolvasni.**

## 5. A gateway-ek saját adatkezelése (ha rajtuk keresztül hívnánk a Jevet)

**OpenRouter** (T1, hivatalos dokumentáció):
- Alap: *„OpenRouter does not store your prompts or responses, unless you opt in to one or both of the following: Private Input & Output Logging […] OpenRouter Use of Inputs/Outputs […]"* (`https://openrouter.ai/docs/guides/privacy/data-collection`).
- Metaadat mindig tárolódik: *„OpenRouter does store metadata (e.g. number of prompt and completion tokens, latency, etc) for each request. […] This metadata does not include the content of your prompts or responses."*
- ZDR: *„Zero Data Retention (ZDR) means that a provider will not store your data for any period of time. […] The following endpoints have a ZDR policy. Note that this list is also available programmatically via https://openrouter.ai/api/v1/endpoints/zdr."* (`https://openrouter.ai/docs/guides/features/zdr`) — a hivatalos, gépileg lekérdezhető JSON-listát **magam is lekértem `curl`-lal** (2026-09-25-i állapot): a `typesafe` provider-tag és a `typesafe/jev-1.13` model_id **szerepel** a listában (`"name": "TypeSafe | typesafe/jev-1.13-20260917", "provider_name": "TypeSafe"`), azaz a Jev **hivatalosan ZDR-képes végpontként van megjelölve** az OpenRouterön.
- EU-régió: *„For enterprise customers, OpenRouter supports EU in-region routing. When enabled for your account, your prompts and completions are processed within the European Union and do not leave the EU. Use the base URL https://eu.openrouter.ai […] This feature is only enabled for enterprise customers by request."* (`https://openrouter.ai/docs/guides/privacy/provider-logging`, illetve `https://openrouter.ai/docs/guides/features/sovereign-ai`) — ez **OpenRouter-szintű** EU-feldolgozási garancia, nem jelenti azt, hogy maga a TypeSafe/Jev modell EU-ban fut; azt jelenti, hogy az OpenRouter csak olyan providerhez routol EU-módban, amelyik EU-régióban tud futni — nincs forrásom arra, hogy a TypeSafe/Jev szerepel-e az OpenRouter EU-in-region routing által elérhető providerek között (lásd „Amire NINCS forrás”).

**Vercel AI Gateway** (T1, hivatalos dokumentáció/changelog):
- ZDR: *„Zero data retention (ZDR) is available for Pro and Enterprise users on AI Gateway. […] Team-wide zero data retention — $0.10 per 1,000 requests […] Per-request zero data retention — No additional cost."* (`https://vercel.com/docs/ai-gateway/security-and-compliance/zdr`)
- Alapértelmezett gateway-szintű ígéret: *„AI Gateway uses zero data retention by default. It permanently deletes your prompts and responses after requests complete."* (`https://vercel.com/docs/ai-gateway/security-and-compliance`)
- Jev-specifikusan, hivatalos KB-útmutató és changelog: *„Jev supports Zero Data Retention and No Training, enabled per request in the example."* (`https://vercel.com/changelog/typesafe-ai-jev-now-available-on-ai-gateway`; ugyanez: `https://vercel.com/kb/guide/typesafe-jev-and-ai-sdk`, „Data controls: Zero Data Retention and No Training, per request").
- Ezzel szemben egy külső gateway-monitoring oldal (Opper.ai, T3, amely nem a Vercel-en, hanem a TypeSafe közvetlen route-ját figyeli) *„Zero data retention: Not established"* státuszt ír — ez nem feltétlenül ellentmondás, hanem arra utalhat, hogy a **Vercel és a TypeSafe közötti külön, negyedleges megállapodás** biztosítja a ZDR-t a Gateway-en át, míg a TypeSafe saját, alapértelmezett/közvetlen API-szabályzata (amit Opper figyel) ezt nem garantálja alapból — de mivel a két forrás pontosan mit mér, arról nincs teljesen egyértelmű, egybevágó leírás, ezért ezt az „Ellentmondások” közt is jelzem.

**Cloudflare** — két különböző terméket kell megkülönböztetni:
- *Workers AI* (Cloudflare saját, hosztolt modellkatalógusa, ahol a `typesafe/jev` mint „Third-party" modell szerepel: `https://developers.cloudflare.com/ai/models/typesafe/jev/`, 32 000 tokenes kontextusablakkal). Hivatalos adatkezelési oldal (`https://developers.cloudflare.com/workers-ai/platform/data-usage/`): *„Cloudflare neither creates nor trains the AI models made available on Workers AI. The models constitute Third-Party Services… Cloudflare does not use your Customer Content to (1) train any AI models made available on Workers AI or (2) improve any Cloudflare or third-party services, and would not do so unless we received your explicit consent."* — ez a Cloudflare **saját** ígérete a maga rétegére, nem a TypeSafe modell-szolgáltatói szabályzatának helyettesítése; a modell saját feltételeire a katalógusoldal külön hivatkozik („Terms and License” link).
- *AI Gateway* (Cloudflare routing/observability rétege, amely bármely providerhez, elvileg a TypeSafe API-hoz is proxyzhat): a naplózás **alapértelmezetten be van kapcsolva**: *„Logs, which include metrics as well as request and response data, are enabled by default for each gateway. […] If you are concerned about privacy or compliance and want to turn log collection off, you can go to settings and opt out of logs."* (`https://developers.cloudflare.com/ai-gateway/observability/logging/`) — kérésenként is felülírható (`cf-aig-collect-log`, `cf-aig-collect-log-payload` fejlécekkel), és a naplók tárolási korlátja csomagtól függ, automatikus törléssel konfigurálható.
- **EU-régió/lokalizáció a Jevre nézve:** nem találtam kifejezett forrást arra, hogy a Cloudflare a `typesafe/jev` hívásait EU-régióban tartaná. Egy független, GDPR-fókuszú monitoring oldal (InferCheck, T3) kifejezetten írja általánosan a Workers AI-ra: *„Cloudflare does not publicly guarantee EU-only inference for Workers AI; its data-localization docs also state Jurisdictional Restrictions for data location/storage are not supported for Workers AI today."* (`https://infercheck.eu/en/provider/cloudflare-workers-ai`) — vagyis a Cloudflare szélesebb „Data Localization Suite / Regional Services” EU-eszközei **nem terjednek ki** a Workers AI-ra (így feltehetően a Jev-hívásokra sem), de ezt kifejezetten a Jevre nézve TypeSafe- vagy Cloudflare-elsődleges forrásból nem tudtam megerősíteni.
- Cloudflare-specifikus ZDR-„címke” (mint a Vercelnél/OpenRouternél) a Jevre nincs dokumentálva — csak az általános „nem tanítunk” ígéret.

Egy összefoglaló, nem hivatalos forrás (jevaiguide.com, T3) táblázatba is szedte, kit ki lát a hívási láncban: *„TypeSafe API: TypeSafe — Vercel AI Gateway: Vercel, then TypeSafe — OpenRouter: OpenRouter, then TypeSafe — Cloudflare Workers AI: Cloudflare, then TypeSafe."* (`https://jevaiguide.com/faq/does-jev-train-on-your-data/`) — ez konzisztens azzal, amit a hivatalos gateway-dokumentációkban találtam: minden gateway egy **további szereplőt** told be, saját metaadat-naplózással, mielőtt a kérés a TypeSafe-hez érne.

## 6. EU AI Act / GDPR: mi számít, ha egy külső modell dönt egy memóriabejegyzés kategóriájáról/elfogadásáról

Ezen a ponton **kizárólag elsődleges jogforrást** idézek, és **nem vonok le jogi következtetést** arra nézve, hogy ezek pontosan hogyan alkalmazandók az easter-memory-system-re — ez esetről esetre eldöntendő jogi kérdés.

- **GDPR 22. cikk (1) bekezdés**, szó szerint (EUR-Lex / a megfelelő UK GDPR-tükör azonos szövegezéssel): *„The data subject shall have the right not to be subject to a decision based solely on automated processing, including profiling, which produces legal effects concerning him or her or similarly significantly affects him or her."* (`https://eur-lex.europa.eu/eli/reg/2016/679/art_22/oj`; azonos szöveg: `https://www.legislation.gov.uk/eur/2016/679/article/22/adopted?view=plain`) — ez **csak akkor** aktiválódik, ha (a) a döntés **kizárólag automatizált**, és (b) **jogi hatással jár, vagy hasonlóan jelentősen érinti** az érintettet.
- **EDPB 28/2024. sz. vélemény** (2024-12-17, AI-modellekről), amely kifejezetten megemlíti, hogy AI-modellek üzemeltetése kapcsán a GDPR 22. cikke releváns lehet: *„Automated-decision making, including profiling: The processing operations conducted in the context of AI models may fall under the scope of Article 22 GDPR, which imposes additional obligations on controllers and provides additional safeguards to data subjects."* (`https://www.edpb.europa.eu/system/files/2024-12/edpb_opinion_202428_ai-models_en.pdf`)
- **EU AI Act, 6. cikk (3) bekezdés**, szó szerint: *„By derogation from paragraph 2, an AI system referred to in Annex III shall not be considered to be high-risk where it does not pose a significant risk of harm to the health, safety or fundamental rights of natural persons, including by not materially influencing the outcome of decision making. The first subparagraph shall apply where any of the following conditions is fulfilled: (a) the AI system is intended to perform a narrow procedural task; […] Notwithstanding the first subparagraph, an AI system referred to in Annex III shall always be considered to be high-risk where the AI system performs profiling of natural persons."* (`https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-6`, ugyanez másodlagos tükrökön is: `https://ai-act-text.com/article-6-ai-act`, `https://en.ai-act.io/...`)
- Az AI Act (53) preambulumbekezdése konkrét példát is ad a „szűk eljárási feladat” kivételre — szó szerint: *„…an AI system that transforms unstructured data into structured data, an AI system that classifies incoming documents into categories or an AI system that is used to detect duplicates among a large number of applications. Those tasks are of such narrow and limited nature that they pose only limited risks…"* (`https://futurium.ec.europa.eu/system/files/2025-03/EU%20COMMISSION%20-%20AI%20ACT%20%28en%29.pdf`).
- Az Európai Bizottság magas-kockázatú AI-rendszerek besorolásáról szóló, 2026-os tervezett iránymutatása (draft guidelines, nem végleges jogszabály, de hivatalos bizottsági dokumentum) tovább pontosítja ezt a kivételt, és **korlátozza** is: *„However, this condition does not apply to all categorisation systems. In particular, AI systems that perform a value judgement of data relevant for decision-making, for example categorisation of input data as 'useful' or 'less useful' for the human assessment, or attributing a score or ranking to input data, are likely to have a broader impact on the assessment process and will therefore not be considered to perform only a 'narrow procedural task'."* (`https://table.media/assets/documents/draft_guidelines_on_the_classification_of_high_risk_ai_annex_iii_7mxr3yiz2gw3uppjpwvvndd8ioi_128561.pdf`, (91)–(93) bekezdés) — ez fontos árnyalat, mert a Jev pontosan „score"/„choice" (rangsorolás, választás) típusú kimeneteket is ad, ami a fenti idézet szerint **túlmutathat** a puszta „dokumentum-kategorizáláson”.
- Emellett fontos: az AI Act 6. cikke csak akkor releváns egyáltalán, ha a rendszer az **Annex III-ban felsorolt, magas kockázatú felhasználási esetek** valamelyikébe esik — arra, hogy egy általános, projekt/ügyfél/tech-kategorizáló memóriarendszer ilyen Annex III-eset alá esne-e, **nem találtam sem TypeSafe-, sem más elsődleges forrást**, és ezt magam sem állítom vagy zárom ki.
- A TypeSafe saját anyagaiban (Privacy Policy, ToS, MCA, DPA, AUP, blog) **nem találtam említést** sem a GDPR 22. cikkére, sem az EU AI Act-re, sem arra, hogy a Jev-et hogyan minősítik AI Act-szempontból (pl. general-purpose AI modellként, vagy Annex III-magas kockázatú komponensként) — ez nyílt kérdés marad.

## Ellentmondások

1. **SOC 2 Type II léte.** A TypeSafe saját hivatalos LinkedIn-oldala (2026-07-07) kijelenti, hogy SOC 2 Type II megfelelőséget szereztek (Vanta + Advantage Partners auditpartnerekkel). Egy másik, T2/T3 forrás (hokai.io) ugyanakkor kifejezetten azt írja: *„TypeSafe AI has not published SOC 2, ISO 27001, or other third-party compliance certifications."* A két állítás nem összeegyeztethető; lehetséges, hogy a hokai.io oldal elavult (a SOC 2-bejelentés utáni frissítés hiánya), de ezt nem tudtam időrendben tisztázni.
2. **ISO 27001.** Egyetlen forrás (`soc2c.com/company/akka`) állítja a TypeSafe ISO 27001-tanúsítványát, de az oldal URL-je és a hivatkozott trust center (`trust.akka.io`) egy másik céget (Akka) sejtet — valószínűsíthető adatminőségi hiba/összekeverés az aggregátor oldalán, ezért ezt az állítást **nem tekintem megbízhatónak**.
3. **ZDR a TypeSafe közvetlen API-ján.** Nem hivatalos, de több forrás (jevaiguide.com és mások, T3) szerint a TypeSafe „enterprise ügyfeleknek kérésre” ZDR-t ad. Egy gateway-monitoring aggregátor (Opper.ai) ugyanakkor a TypeSafe közvetlen route-jára *„Zero data retention: Not established"* státuszt ír. Lehet, hogy ez csak azt jelenti, hogy nincs **alapértelmezett/publikus** ZDR (csak egyedi, kérésre adott enterprise-megállapodás), amit egy automatizált monitoring-eszköz nem tud „megállapítottként” bejelölni — de ez csak feltételezés, nem megerősített magyarázat.
4. **A gateway-szintű ZDR és a TypeSafe „natív” ZDR-állapota közötti viszony.** A Vercel AI Gateway hivatalos dokumentációja és changelogja kifejezetten állítja, hogy a Jev „per request” ZDR-t és „No Training”-et támogat a Gateway-en át, miközben ugyanakkor (más forrás szerint) a TypeSafe saját, direkt API-ja alapból nem garantál ZDR-t. Ez arra utalhat, hogy a gateway és a TypeSafe között van egy, a nyilvános TypeSafe-szabályzatnál szigorúbb, egyedi megállapodás — ezt viszont egyik fél nyilvános dokumentuma sem mondja ki kifejezetten, ezért ezt a nyitott kérdést jelzem, nem oldom fel.
5. **MCA vs. Privacy Policy a tanítás kérdésében (a sq00-kör által jelzett feszültség pontosítása).** A sq00-kutatás egy külső jogi elemzésre (Wunderlandmedia) hivatkozva „feszültséget” jelzett a Privacy Policy feltétlen „nem tanítunk” ígérete és az MCA 4.1-es klauzulája között. Ebben a körben elolvastam az MCA 4.1 pontjának pontos szövegét, és az **kifejezetten megismétli** a „nem tanítunk” ígéretet, csak azzal a különbséggel, hogy az MCA szerint ez „az Ügyfél előzetes hozzájárulása nélkül” érvényes (tehát elméletileg felülírható hozzájárulással), míg a Privacy Policy ezt a feltételt nem említi. A feszültség tehát **valós, de enyhébb**, mint ahogy egy felületes olvasat sugallhatná — mindkét dokumentum alapesetben tiltja a tanítást, csak az MCA hagy nyitva egy hozzájárulás-alapú kivételt.

## Amire NINCS forrás

- Nincs elsődleges (TypeSafe-saját) forrás a „zero data retention” kifejezés szó szerinti használatára vagy pontos feltételeire (csak T3 összefoglalók, „privacy@typesafe.ai”-hoz irányítva).
- Nem sikerült elolvasni a `trust.typesafe.ai` és a `trust.typesafe.ai/subprocessors` oldal tényleges (JS által renderelt) tartalmát — így a szubfeldolgozó-lista (AWS, Modal, Slack, Google Workspace) és a Trust Centerben esetlegesen felsorolt tanúsítványok **csak egyetlen, nem hivatalos harmadik feles forrásból (Wunderlandmedia)** ismertek, függetlenül nem megerősíthetők.
- Nincs megbízható, elsődleges forrás a TypeSafe ISO 27001-tanúsítására.
- Nem sikerült két egymástól független forrással megerősíteni a TypeSafe hiányát az EU–US Data Privacy Framework listáján — csak egyetlen T3 forrás (Wunderlandmedia) explicit ellenőrzése áll rendelkezésre, amit én magam sem tudtam a dinamikus kormányzati oldalon reprodukálni.
- Nincs forrás arra, hogy az OpenRouter EU in-region routingja (`eu.openrouter.ai`) ténylegesen elérhető-e a `typesafe/jev-1.13` végpontra (azaz hogy a TypeSafe szerepel-e az EU-régióban futtatható providerek között), csak arra van forrás, hogy ez a funkció létezik és enterprise-ügyfeleknek elérhető általánosságban.
- Nincs forrás arra, hogy a Cloudflare AI Gateway vagy a Workers AI kifejezetten EU-régióban futtatná a `typesafe/jev` hívásait; az elérhető forrás csak azt mondja, hogy a Cloudflare Data Localization Suite **általánosságban** nem terjed ki a Workers AI-ra.
- Nincs forrás arra, hogy a TypeSafe saját anyagaiban bármilyen módon reflektálna a GDPR 22. cikkére vagy az EU AI Act-re (pl. hogy a Jev-et milyen AI Act-kategóriába sorolják, vagy hogy Annex III magas-kockázatú esetnek tekintik-e bármelyik tipikus felhasználását).
- Nincs forrás (sem TypeSafe-től, sem független jogi elemzésből) arra a konkrét kérdésre, hogy egy memóriabejegyzés (projekt/ügyfél/tech kategória) automatikus TypeSafe/Jev-alapú előkategorizálása/elfogadás-ellenőrzése GDPR 22. cikk vagy AI Act Annex III szempontjából „magas kockázatúnak” vagy „kizárólag automatizált, jogi hatású döntésnek” minősülne-e — ez nyitott jogi kérdés, amiről nem vonok le következtetést.

## Meglátogatott és felderített linkek

| Cím | URL | Tier | Eszköz | Megjegyzés |
|---|---|---|---|---|
| Privacy policy — TypeSafe AI | https://typesafe.ai/legal/privacy | T1 | Exa web_fetch_exa | Teljes oldal elolvasva; „Retention”, „International Visitors” szakaszok kulcsidézetei innen |
| Data processing addendum (DPA) — TypeSafe AI | https://typesafe.ai/legal/data-processing | T1 | Exa web_fetch_exa + web_search_exa | SCC/UK Addendum, subprocessor-hivatkozás, retention, security incident |
| Master customer agreement (MCA) — TypeSafe AI | https://typesafe.ai/legal/mca | T1 | Exa web_search_exa (highlight) | 4.1 (Use of Customer Data / no-training kivétel), Term/Termination, Confidentiality |
| Terms of Service (Playground/API preview) — TypeSafe AI | https://typesafe.ai/terms-and-conditions | T1 | Exa web_search_exa (highlight) | 4. pont: Input/Output/technikai naplók, no-training, no 3rd-party disclosure |
| Terms of use — TypeSafe AI | https://typesafe.ai/legal/terms | T1 | Exa web_search_exa (highlight) | Weboldal-szintű ÁSZF, Privacy Policy-ra hivatkozik |
| Acceptable Use Policy — TypeSafe AI | https://typesafe.ai/legal/acceptable-use-policy | T1 | Exa web_search_exa (highlight) | AUP-monitoring kitétel |
| Typesafe.ai Trust Center (főoldal) | https://trust.typesafe.ai/ | T1 (elérhetetlen tartalom) | Exa web_fetch_exa | JS/Vanta-renderelt, tartalom nem olvasható ki |
| Typesafe.ai Trust Center — subprocessors | https://trust.typesafe.ai/subprocessors | T1 (elérhetetlen tartalom) | Exa web_fetch_exa | JS/Vanta-renderelt, tartalom nem olvasható ki |
| TypeSafe AI Jev Terms of Service: EU Read — Wunderlandmedia | https://wunderlandmedia.com/typesafe-ai-jev-terms-of-service-gdpr | T3 | Exa web_search_exa (highlight) | Egyetlen forrás a subprocessor-névsorra és a DPF-hiányra; jogi blogger, nem hivatalos |
| TypeSafe's customer agreement forbids publishing benchmarks — Dark Factory Dev | https://darkfactory.dev/news/2026-09-19-extra/story-2 | T2/T3 | Exa web_search_exa (highlight) | MCA dátumozása („last updated August 27, 2026”), 2.3/6/12.3 szakaszok |
| Data Collection — OpenRouter Privacy | https://openrouter.ai/docs/guides/privacy/data-collection | T1 | Exa web_search_exa (highlight) | Alap adatgyűjtési/logolási szabályok |
| Provider Logging and Data Retention Policies — OpenRouter | https://openrouter.ai/docs/guides/privacy/provider-logging | T1 | Exa web_search_exa (highlight) | EU in-region routing (`eu.openrouter.ai`), provider-szintű politika |
| Zero Data Retention — OpenRouter | https://openrouter.ai/docs/guides/features/zdr | T1 | Exa web_search_exa (highlight) | ZDR-mechanizmus leírása, programozott lista hivatkozása |
| OpenRouter ZDR endpoints (nyers JSON) | https://openrouter.ai/api/v1/endpoints/zdr | T1 | curl (nyers fájl) | Magam kértem le; a `typesafe`/`typesafe/jev-1.13` szerepel a ZDR-listában |
| Sovereign AI — In-Region AI Routing — OpenRouter | https://openrouter.ai/docs/guides/features/sovereign-ai | T1 | Exa web_search_exa (highlight) | EU/US in-region routing, ZDR + data_collection kombinálva |
| Terms of Service — OpenRouter | https://openrouter.ai/terms | T1 | Exa web_search_exa (highlight) | Prompt logging opt-in licenc, kategorizáló modell „nem tárol” kitétel |
| Jev 1.13 — API Pricing & Providers — OpenRouter | https://openrouter.ai/typesafe/jev-1.13 | T2 | Exa web_fetch_exa | Modell-oldal, ár, provider (TypeSafe), uptime |
| Jev Documentation — OpenRouter community | https://openrouter.ai/docs/guides/community/jev | T2 | Exa web_search_exa (highlight) | Modell-ID, alias, kontextushossz |
| AI Gateway Zero Data Retention (ZDR) — Vercel | https://vercel.com/docs/ai-gateway/security-and-compliance/zdr | T1 | Exa web_fetch_exa + web_search_exa | Team-wide/per-request ZDR, árazás, provider-lista (Alibaba, Baseten, Cerebras, Claude AWS, DeepInfra, Google Vertex, Moonshot, Particle.AI — TypeSafe nem szerepelt a látott listarészletben) |
| Security and Compliance — Vercel AI Gateway | https://vercel.com/docs/ai-gateway/security-and-compliance | T1 | Exa web_search_exa (highlight) | Gateway-szintű alapértelmezett ZDR-ígéret |
| TypeSafe AI's Jev now available on AI Gateway — Vercel changelog | https://vercel.com/changelog/typesafe-ai-jev-now-available-on-ai-gateway | T1 | Exa web_search_exa (highlight) | „Jev supports Zero Data Retention and No Training, enabled per request” |
| How to classify, route, and score with Jev and AI SDK — Vercel KB | https://vercel.com/kb/guide/typesafe-jev-and-ai-sdk | T1 | Exa web_search_exa (highlight) | „Data controls: Zero Data Retention and No Training, per request” |
| TypeSafe API with AI Gateway — Vercel | https://vercel.com/docs/ai-gateway/sdks-and-apis/typesafe | T1 | Exa web_search_exa (highlight) | Kompatibilis végpont, SDK-példák |
| AI Gateway Provider Routing and Fallbacks — Vercel | https://vercel.com/docs/ai-gateway/models-and-providers/provider-options | T1 | Exa web_search_exa (highlight) | `typesafe-ai` provider szerepel az elérhető providerek közt |
| TypeSafe AI models — Vercel AI Gateway | https://vercel.com/ai-gateway/models/providers/typesafe-ai | T1 | Exa web_search_exa (highlight) | Ár/ZDR/No Training/Regional Inference táblázat (a mezők üresen/nem olvashatóan jelentek meg a lekérésben) |
| Jev — Vercel AI Gateway modelloldal | https://vercel.com/ai-gateway/models/jev | T1 | Exa web_search_exa (highlight) | Modell-ID, ár, kontextus |
| Logging — Cloudflare AI Gateway docs | https://developers.cloudflare.com/ai-gateway/observability/logging/ | T1 | Exa web_search_exa (highlight) | Alapból bekapcsolt naplózás, opt-out, fejléc-szintű vezérlés |
| Workers Logpush — Cloudflare AI Gateway docs | https://developers.cloudflare.com/ai-gateway/observability/logging/logpush/ | T1 | Exa web_search_exa (highlight) | Titkosított log-export |
| Data usage — Workers AI (Cloudflare) | https://developers.cloudflare.com/workers-ai/platform/data-usage/ | T1 | Exa web_search_exa (highlight) | „Nem tanítunk, nem osztjuk meg más ügyféllel” ígéret |
| Jev (typesafe) — Cloudflare AI docs | https://developers.cloudflare.com/ai/models/typesafe/jev/ | T1 | Exa web_search_exa (highlight) | Modell-katalógus bejegyzés, 32K kontextus, példakérés/válasz |
| Cloudflare's approach to responsible AI | https://www.cloudflare.com/trust-hub/responsible-ai/ | T1 | Exa web_search_exa (highlight) | Általános „nem tanítunk LLM-eket” vállalati ígéret, AI Act GPAI-megjegyzés |
| FAQs — Cloudflare Data Localization Suite | https://developers.cloudflare.com/data-localization/metadata-boundary/faq/ | T1 | Exa web_search_exa (highlight) | Regional Services / Metadata Boundary — külön termék, nem Workers AI-specifikus |
| Cloudflare Workers AI — GDPR Compliance Profile — InferCheck | https://infercheck.eu/en/provider/cloudflare-workers-ai | T3 | Exa web_search_exa (highlight) | „Nincs nyilvánosan garantált EU-only inference a Workers AI-ra” |
| TypeSafe AI: The Company Behind Jev — Jev AI Guide | https://jevaiguide.com/typesafe-ai/ | T3 | Exa web_search_exa (highlight) | ZDR enterprise-kérésre, privacy@typesafe.ai |
| Does Jev Train on Your Data? — Jev AI Guide | https://jevaiguide.com/faq/does-jev-train-on-your-data/ | T3 | Exa web_search_exa (highlight) | Csatorna-táblázat (TypeSafe API / Vercel / OpenRouter / Cloudflare) |
| Jev on Cloudflare Workers AI — Jev AI Guide | https://jevaiguide.com/channels/cloudflare-workers-ai/ | T3 | Exa web_search_exa (highlight) | Cloudflare-csatorna részletei, modellválasz-minta |
| TypeSafe AI — HokAI | https://hokai.io/hub/companies/typesafe-ai | T2/T3 | Exa web_search_exa (highlight) | Állítja: nincs publikált SOC 2/ISO 27001 — ellentmond a LinkedIn-bejelentésnek |
| TypeSafe AI LinkedIn — SOC 2 Type II bejelentés | https://www.linkedin.com/posts/typesafe-ai_activity-7480343405286313984-qWxZ | T1 (céges közlés, nem szabályzat) | Exa web_search_exa (highlight) | A cég saját bejelentése, 2026-07-07 |
| typesafe ai — LinkedIn cégoldal | https://linkedin.com/company/typesafe-ai | T1 | Exa web_search_exa (highlight) | Megerősíti a SOC 2 Type II posztot |
| Typesafe Inc SOC 2 Type II compliance — soc2c.com | https://soc2c.com/company/akka | T3 (megbízhatatlan) | Exa web_search_exa (highlight) | URL/trust-center-hivatkozás („Akka”) más céget sejtet — adatminőségi hiba gyanús |
| TypeSafe AI — apis.io API-katalógus | https://apis.io/providers/typesafe-ai/ | T2/T3 | Exa web_search_exa (highlight) | Megerősíti a Vanta Trust Center, HackerOne, TLS/HSTS/DNSSEC/DMARC meglétét |
| TypeSafe AI — Opper.ai gateway-aggregátor | https://opper.ai/provider/typesafe | T3 | Exa web_search_exa (highlight) | „Zero data retention: Not established”, régió „Multi (United States)”, DPA elérhető |
| TypeSafe AI, Inc. Models — Requesty.ai | https://www.requesty.ai/models/typesafe | T2/T3 | Exa web_search_exa (highlight) | Régió („US”) megerősítése, nem tanít ígéret |
| Data residency on Modal | https://modal.com/docs/guide/data-residency.md | T1 (Modal saját dok.) | Exa web_search_exa (highlight) | Modal (feltételezett TypeSafe-alvállalkozó) saját régió-politikája — nem TypeSafe-specifikus |
| Typesafe AI status | https://status.typesafe.ai/ | T1 | Exa web_search_exa (highlight) | Uptime-oldal, nem ad adatvédelmi infót |
| Infrastructure Engineer, Kubernetes Specialist — Ashby (TypeSafe álláshirdetés) | https://jobs.ashbyhq.com/typesafe-ai/4da613b6-6d56-4e8d-8cc4-fad8ca57e4ce | T2 | Exa web_search_exa (highlight) | „multi-region, multi-cloud” infrastruktúra-terv — jövőbeli jel, nem jelenlegi EU-régió megerősítés |
| TypeSafe AI docs (llms-full.txt) | https://docs.typesafe.ai/llms-full.txt | T1 | Exa web_search_exa (highlight) | Kód-/koncepció-dokumentáció, subcontractor-hivatkozás kontextusa |
| Regulation (EU) 2024/1689 (AI Act) hivatalos szöveg | https://futurium.ec.europa.eu/system/files/2025-03/EU%20COMMISSION%20-%20AI%20ACT%20%28en%29.pdf | T1 | Exa web_search_exa (highlight) | (53) preambulumbekezdés — „narrow procedural task” példák |
| Implementation Guidance for the EU AI Act — Európai Bizottság | https://futurium.ec.europa.eu/system/files/2026-07/Implementation-Guidance-EU-AI-Act_1.pdf | T1 | Exa web_search_exa (highlight) | Általános AI Act-értelmezési segédlet |
| Article 6 — AI Act Service Desk (EU Bizottság) | https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-6 | T1 | Exa web_search_exa (highlight) | 6. cikk (3) bek. szó szerinti szövege |
| Article 53 — AI Act Service Desk | https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-53 | T1 | Exa web_search_exa (highlight) | GPAI-szolgáltatói kötelezettségek (kontextus) |
| Draft guidelines on classification of high-risk AI (Annex III) — Európai Bizottság | https://table.media/assets/documents/draft_guidelines_on_the_classification_of_high_risk_ai_annex_iii_7mxr3yiz2gw3uppjpwvvndd8ioi_128561.pdf | T1 (tervezet) | Exa web_search_exa (highlight) | „narrow procedural task” kivétel korlátai, „value judgement” kizárás |
| EDPB Opinion 28/2024 on AI models | https://www.edpb.europa.eu/system/files/2024-12/edpb_opinion_202428_ai-models_en.pdf | T1 | Exa web_search_exa (highlight) | GDPR 22. cikk relevanciája AI-modelleknél |
| GDPR Article 22 — EUR-Lex | https://eur-lex.europa.eu/eli/reg/2016/679/art_22/oj | T1 | Exa web_search_exa (highlight) | Hivatalos szöveg + (71) preambulumbekezdés |
| GDPR Article 22 (UK GDPR-tükör) — legislation.gov.uk | https://www.legislation.gov.uk/eur/2016/679/article/22/adopted?view=plain | T1 | Exa web_search_exa (highlight) | Azonos szövegű cikk, könnyebben idézhető formában |
| Rights related to automated decision making — ICO | https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/rights-related-to-automated-decision-making-including-profiling/ | T2 (felügyeleti hatóság iránymutatása) | Exa web_search_exa (highlight) | Gyakorlati magyarázat a 22. cikkhez |
| Data Privacy Framework — hivatalos program-oldal | https://www.dataprivacyframework.gov/Program-Overview | T1 | Exa web_search_exa (highlight) | DPF-program működése, listázás szabályai |
| Data Privacy Framework List | https://www.dataprivacyframework.gov/list | T1 (nem lekérdezhető megbízhatóan) | Exa web_search_exa (highlight) | Dinamikus, JS-alapú lista — TypeSafe-re nem tudtam rákeresni benne |
| Cross-Border Data Flows and the Adequacy Decision Map for AI — FirmAdapt | https://firmadapt.com/blog/cross-border-data-flows-adequacy-2026 | T3 | Exa web_search_exa (highlight) | Általános figyelmeztetés: sok AI-szolgáltató nincs DPF-en, ellenőrizni kell |
| sq00-azonositas.md (korábbi kutatási kör, ehhez a projekthez) | /home/claude/work/kutatas-jev/sq00-azonositas.md | — | Read (helyi fájl) | Kiinduló kontextus, kritikusan kezelve, e körben számos ponton önállóan újra-ellenőrizve |

---

# SQ05 — Mire használják a Jevet és a hasonló „döntési modelleket" — és illik-e a memória-rendszer feladataira

*Kutatási eszköz: kizárólag Exa (`web_search_exa`, `web_fetch_exa`), a `_kozos.txt` előírása szerint. Alügynök-indítás (a `deep-web-research` skill teljes, sok-ügynökös pipeline-ja) ebben a környezetben nem állt rendelkezésre — ez egyetlen, egyágensű, Exa-only kutatási kör, ezért degradált módban, de a `_kozos.txt` és az `sq00` módszertanát (elsődleges forrás, szó szerinti idézet, T1/T2/T3 jelölés, kettős megerősítés) követve dolgoztam. Az `sq00-azonositas.md`-t elolvastam, de nem vettem át ellenőrizetlenül.*

## Rövid válasz

A Jevet a piac ma túlnyomórészt pontosan azokra a feladatokra használja, amiket a memória-rendszer felhasználója kérdezett: osztályozás/kategória-választás, útválasztás (modell- és csapat-routing), moderálás/guardrail-szűrés, RAG-relevancia-ítélet és reranking — ezekre bőséges, egymástól független (fejlesztői blog, gateway-dokumentáció, önálló nyílt forrású csomag) megerősítés van, a gyártói és független mérések (Banking77, CLINC150, saját ügyfél-adatok) általában 79–91% közötti pontosságot és a frontier LLM-ekhez képest 2–13 pontos elmaradást mutatnak, cserébe 10–200×-os sebesség- és költségelőnyért. Deduplikáció/entitás-egyeztetés van a Jev hivatalos „cookbook"-jai közt (`docs.typesafe.ai/cookbooks/entity_alignment`), de erre csak a gyártói forrást és egy nem hivatalos tükröt találtam, független megerősítés nélkül. Ellentmondás-felismerésre is van dokumentált minta (külön „contradicts" `Noul` kérdésként RAG-passzus-szűrésnél), és ezt három egymástól független fejlesztői forrás is használja/leírja. Kifejezett, elnevezett memória-rendszer (mem0, Zep, Letta, Basic Memory) natív Jev-integrációját NEM találtam — ezek hivatalos dokumentációjában, GitHub-jában nincs Jev/TypeSafe/„System One" említés —, viszont van egy 2026-09-21-i, a TypeSafe-től független egyetemi (UT Dallas) arXiv-cikk, a „Jev-Mem", amely kifejezetten Jevet (mint „System-One control plane"-t) épít be egy önálló agentikus memória-architektúrába, publikált benchmarkkal (LoCoMo). A Jev helyét a kis, helyi klasszifikátorok/cross-encoder rerankerek/NLI-modellek/zero-shot embedding-klasszifikátorok mezőnyében egy 2026-os akadémiai benchmark (BTZSC) segít elhelyezni, bár ott Jev maga (zárt, fizetős API lévén) nem szerepel. A negyedik kérdésre — mennyit javít egy második modell (pl. Jev), ha a döntést ELSŐRE már egy frontier LLM meghozta — pontosan erre a sorrendre (frontier dönt előbb, gyors modell ellenőriz utána) NINCS FORRÁS; a fellelt kaszkád-irodalom szinte kivétel nélkül a fordított sorrendet vizsgálja (olcsó modell dönt előbb, drágább/frontier ellenőriz/eszkalál utána), és az egyik ide vonatkozó akadémiai eredmény (a „blind spot" cikk) arra utal, hogy egy olcsó ellenőrző modell vakfoltja éppen egy erősebb, magabiztosabb „javasoló" modell hibáinál nő meg — ami óvatosságra int a Jev-mint-utólagos-ellenőr ötlettel szemben, de ez csak áttételes, nem közvetlen bizonyíték.

## 1. Publikált felhasználási esetek a Jevre

### 1.1 Osztályozás (classification)

**Gyártói forrás.** A TypeSafe saját „cookbook" gyűjteménye (`docs.typesafe.ai/cookbooks`, T1, elért 2026-09-25) külön „Classification" szekciót tartalmaz: *„Hierarchical classification — Classifies documents through deep patent, retail product, biomedical, and source-code hierarchies using parallel beam search over TypeSafe Choice probabilities."*; *„Classification using confidence — Classify SEC annual reports into 75 industry groups with one Choice each, then read the answer's own confidence to decide whether to report that group or the broader division above"*. (docs.typesafe.ai/cookbooks)

**Független beszámolók.** A Towards Data Science stílusú, de a worldprogramming.org-on közölt cikk (T2, 2026-09-21) ügyfélszolgálati szándék-osztályozást (intent classification) tesztelt Jevvel OpenAI Terra/Luna ellen: *„On accuracy, Jev performs noticeably worse than both OpenAI models: 79.0%, compared with 83.9% for Terra and 86.2% for Luna. The difference is statistically significant."*, majd *„When I reduced the task from 77 labels to just 7, the results improved significantly and were roughly on par with the OpenAI models."* (worldprogramming.org/posts/a-new-kind-of-model-for-ai-decision-making-wepuso)

Az OpenRouter saját blogja (T2, gateway-üzemeltető, 2026-09-22) Banking77 (3080 sor, 77 kategória) teszten Claude Opus 5-tel vetette össze: *„Claude Opus 5 achieved 84.4% accuracy and 83.6% macro-F1, while Jev 1.13 achieved 81.0% accuracy and 80.5% macro-F1. The paired gap was 3.3 percentage points on accuracy with a 95% bootstrap interval from 2.3 to 4.4 percentage points. The models agreed on 89.3% of utterances."* (openrouter.ai/blog/insights/jev-vs-claude-opus-5-classification)

Az AY Automate LLC független, nem-vendor mérése (T2, 2026-09-20, 3955 hívás, McNemar-teszttel) 8-utas és 77-utas routing/osztályozási feladaton: *„On 8-way routing Jev was behind GPT-5.4 nano (Jev alone right on 2 items, nano alone right on 12, p = 0.013) and behind GPT-5.6 Terra (2 to 11, p = 0.022)... In plain terms, Jev behaved like a good small model, not like a frontier model."* Ugyanakkor egy Jev-first kaszkádnál (Jev dönt, ha magabiztos, egyébként a frontier modell): *„At the 0.80 gate, 19.4 percent of 8-way items and 23.0 percent of 77-way items went to Terra, and the combined accuracy was 90.0 and 84.8 percent against 89.4 and 84.3 percent for Terra alone... Cost was 26 to 28 percent of Terra alone."* (ayautomate.com/blog/jev-vs-llm-benchmark)

Egy egyedi, gyakorlati oldalról (dev.to, T3, 2026-09-18) más eredmény: ugyanazon a bounded-döntési feladaton (Arbitrum hackathon zsűriző-gate) *„Jev choice plus four diagnostic Nouls reached 100.0% accuracy against the existing labels across the 306 decisions... Claude Sonnet 5 at high reasoning reached 99.0%."*, és *„Jev's Expected Calibration Error was 0.037. Sonnet high's was 0.058."* — itt tehát Jev egy szűk, jól definiált bináris/hármas döntésen minimálisan jobb és jobban kalibrált volt, mint a frontier modell. (dev.to/bengreenberg/jev-vs-claude-who-wins-4mln)

Az önálló JevBench aggregátor (T2, „Independent evidence for Jev", nincs szponzoráció, utolsó frissítés 2026-09-19) explicit summázza a szórást: *„Across the runs recorded here Jev ranges from 62.6% to 95.4%. There is no universal Jev accuracy, and our schema has nowhere to store one."*, Banking77-en 83.2% (vs. GPT-5.4 nano 79.3%, GPT-5.6 Terra 87.5%, BGE-small+logreg 93.3%, minősítve „AMBIGUOUS"). (jevbench.xyz)

**Összegzés (Q1/osztályozás):** legalább öt egymástól független forrás (worldprogramming.org, OpenRouter, AY Automate, JevBench, dev.to/bengreenberg) méri egymástól függetlenül a Jev osztályozási pontosságát frontier LLM-ekhez képest; az eredmény feladatfüggő — nagy címkeszámnál (77+) rendre 2–7 pontos elmaradás, kis/bináris döntésnél olykor egyenrangú vagy jobb. Egyik forrás sem vendor-only; a gyártói cookbookok konkrét pontosságszámot erre nem közölnek, csak a séma helyességét („nem hallucinál formátumot") állítják.

### 1.2 Útválasztás (routing)

**Gyártói/gateway forrás.** Az Akka.io blog (T2, hivatalos AI-gateway-integráció, 2026-09-23): *„Akka's gateway can also use semantic routing to quickly route based on use case... If you want to route based on interrogation of the message and its content, then you can use Jev to triage your AI message traffic."*, példával: *„Fast Q&A routing | Jev scores an incoming support ticket on urgency (1 to 5) and the router sends 4 and 5 to a Sonnet-backed agent... and 1 to 3 to a Haiku-backed responder."* (akka.io/blog/fast-cheap-agent-decisions)

**Ügyfél-beszámoló (T2, biztonsági cég, saját adaton mérve).** A Vega.io (SOC/security agent gyártó) 2026-09-21-i blogja triage-agent elé állította Jevet kapuként: *„Jev, TypeSafe's new decision model, does one kind of task, a fixed question with known options, fast and cheap... As a gate it closed 15% of the agent's alerts on the busy tenant and a third on the quiet one, right about 98% of the time by three LLM judges whose labels our security analysts then verified and corrected by hand."* Fontos önkorlátozás ugyanabból a posztból: *„We also checked whether it could decide outright, which was never the goal. It cannot, and the tenant's own history is what made the gate work."* (vega.io/blog/jev-closed-up-to-a-third-of-our-triage-agents-alerts)

**Független fejlesztői forrás.** A Prescott Data / JarvisCore blog (T2, 2026-09-19) agent-keretrendszer-szintű routingot ír le: *„JarvisCore 1.12.0 adds a different path. Jev is a System One model built for typed decisions inside software. We now support it natively across agent code, Kernel routing, model-tier selection, and retrieval."* (developers.prescottdata.io/blog/typesafe-jev-agent-routing-rag-jarviscore)

Egy másik, kifejezetten a memória-rendszer kérdéséhez közeli, egyéni (nem-vendor) teszt (dev.to, T3, 2026-09-24) éppen „melyik projekthez tartozik ez a feladat" kategória-döntést hasonlította Jev és Claude több szintje közt: *„On 53 of my own tasks with a known project, Jev picked the wrong project 9 times and Claude Opus 5 picked it wrong 12 times. Jev answered in a median 209 ms against 4,689 ms, and a call cost about $0.00019 against $0.025."* (dev.to/zika_zag_c43dc387e13f45ea/picking-a-new-tasks-project-in-200-ms-jev-vs-claude-on-53-of-my-tasks-32ab)

**Összegzés (Q1/routing):** legalább négy egymástól független forrás (Akka, Vega, Prescott/JarvisCore, dev.to task-router teszt) írja le/méri a routing use case-t; a Vega-eset az egyetlen, amely emberi ellenőrzéssel validált, termelésközeli (bár PoC-fázisú) adatot közöl.

### 1.3 Moderálás / guardrail-szűrés

**Gyártói/gateway forrás.** Az OpenRouter tutorial blogja (T2, 2026-09-23) kifejezetten erre a use case-re épül: *„This guide shows how to use Jev on a problem of your own, worked end to end on one example, moderating listings on a marketplace in TypeScript... You also want to catch items in the wrong category and descriptions that contradict the title or the declared condition."* (openrouter.ai/blog/tutorials/how-to-use-jev)

**Nem hivatalos harmadik fél oldal (T3, csak jelölve).** A `jevtypesafeai.com/use-cases` (nem hivatalos, magát TypeSafe-hez nem kötő tükör-/wrapper-oldal) is listáz „Content moderation — Guardrail user-generated content before it hits your app" és „LLM guardrail — Screen a user prompt before it reaches your model" pontokat, de ez T3 forrás, önmagában nem vehető bizonyítéknak.

**Független fejlesztői forrás.** A Java SDK-t építő fejlesztő (dev.to, T3, 2026-09-20) írja: *„Guardrails are Jev's officially recommended use case: screening every input and output of an LLM application at a tiny fraction of the cost of the LLM call itself."*, konkrét kódrészlettel egy Spring AI „prompt guard advisor"-hoz. (dev.to/jamilxt/i-built-the-first-java-sdk-for-jev-typesafes-system-one-model-2m37)

**Összegzés (Q1/moderálás):** két, egymástól független, nem-vendor forrás (OpenRouter tutorial mint gateway-partner, illetve a Java SDK dev.to-poszt) erősíti meg a gyártói „officially recommended use case" állítást; ehhez jön egy T3, nem hivatalos oldal további (nem önálló bizonyítékként számító) megerősítése.

### 1.4 Deduplikáció / entitás-egyeztetés

**Kizárólag gyártói forrás, gyenge független megerősítéssel.** A TypeSafe hivatalos cookbookja (`docs.typesafe.ai/cookbooks/entity_alignment`, T1, közvetlenül lekérve 2026-09-25; a benne szereplő futtatás dátuma `jev-1.12`, 2026-08-11) explicit deduplikációs/entitás-feloldási mintát ad: *„A key problem in knowledge graphs is deciding whether an incoming entity duplicates an existing one... a single TypeSafe `Score` decides whether each pair is a duplicate, or whether it deserves a closer look from a curator."* A választott adatsor a Magellan „Beer" benchmark, 450 jelölt pár, három szintű `Score` (different / related-uncertain / same) + mezőnkénti `Noul`. A cookbook explicit figyelmeztet: *„Merging two entities inappropriately is the more expensive mistake... Pairwise predictions are not automatically transitive."*

Az egyetlen talált, nem hivatalos tükör (`jev-ai.pro/entity-matching`, T3) szó szerint ugyanezt a cookbookot ismétli meg, tehát nem számít önálló, független megerősítésnek. **A `_kozos.txt` szabálya szerint ez az állítás — hogy a Jev deduplikációra/entitás-egyeztetésre használható — csak a gyártói forrásból van alátámasztva, két egymástól független (nem-vendor) megerősítést NEM találtam rá.** (A `jev-table` PyPI-csomag „Dedupe" funkciója más: az csak azonos szöveg/kérdés hash-alapú cache-elését jelenti, nem szemantikai duplikátum-felismerést.)

### 1.5 Ellentmondás-felismerés (contradiction detection)

Ez a memória-rendszer D-38 pontjához (nincs kapu, mert embedding nem megbízható ellentmondásra) különösen releváns. Három, egymástól független forrás ír le azonos alapmintát: egy külön `Noul` kérdés arra, hogy egy passzus ellentmond-e egy premisszának.

- Egy fejlesztő RAG-memória-eszközének (Zerikai Memory) leírása (dev.to, T2/T3, 2026-09-22): *„Every passage gets four typed questions... `questions[f\"contradicts::{pid}\"]`... By separating relevance from injection risk and contradiction, you hand the IDE agent a level of structural awareness that most RAG pipelines never expose."* (dev.to/kike/how-i-went-from-trust-me-bro-to-boomer-with-receipts-using-jev-2141)
- A Prescott Data/JarvisCore blog (T2, 2026-09-19): *„With `RAG_DECISION_PROVIDER=typesafe`... it then asks four independent Noul questions about every query-passage pair: ... 3. Does it contradict a factual premise in the query? ... In our live three-passage test... a legacy passage that denied the query premise routed to conflicting evidence."* (developers.prescottdata.io/blog/typesafe-jev-agent-routing-rag-jarviscore)
- A Refix.ai cikk (T2, 2026-09-18): *„For each passage, ask questions such as: ... Does it contradict a premise in the query or another selected source? ... Code can then decide: ... preserve and label a useful contradiction..."* (refix.ai/news/jev-rag-reranking-citation-checks)

**Fontos korlát, ugyanezekből a forrásokból.** A Refix cikk explicit figyelmeztet: *„A reranker cannot recover a relevant document that retrieval never found. A citation checker cannot fix a claim that has no source."* — vagyis a Jev-alapú ellentmondás-jelzés is csak azon a szűk halmazon dolgozik, amit a keresés már behozott, és típusosan egy bináris/valószínűségi jelzést ad, amit a hívó kódnak kell értelmeznie (küszöbbel), nem automatikus műveletet.

**Összegzés (Q1/ellentmondás):** a mintázat (külön `contradicts` `Noul` kérdés) három egymástól független, nem-vendor forrásból megerősített, konzisztens minta, de mindhárom RAG-kontextusban (lekérdezés kontra passzus), nem memória-írás-kontra-meglévő-jegyzet kontextusban — ez utóbbira (két meglévő memória-bejegyzés egymásnak ellentmond-e) nem találtam Jev-specifikus publikált esetet.

### 1.6 Relevancia-ítélet / RAG-reranking

Ez a legjobban dokumentált és legtöbb független adattal alátámasztott use case.

**Gyártói forrás, közvetlenül ellenőrizve.** `docs.typesafe.ai/cookbooks/rerank_typesafe` (T1, lekérve 2026-09-25, `jev-1.12`, adatkészlet: CLERC, 3565 bírósági passzus, 40 kérdés, BM25 top-30 shortlist): *„With re-ranking, the correct passage lands in first place for 18% of queries, up from 5% with fast search alone."* Táblázatosan: top-1 5%→18%, top-5 15%→35%, top-10 38%→62%. A cookbook saját maga hangsúlyozza a korlátot: *„the top-30 shortlist contained the correct passage for every one of the 40 queries"* — vagyis a plafon 100% lett volna, és a Jev csak 18%-ig jutott, ami azt jelzi, hogy a jogi idézet-egyeztetés önmagában nehéz feladat, nem csak a keresés hibája.

**Független, számszerű reranker-benchmark.** A `hev-rerank` nyílt csomag (T2, módszertan és nyers adat is közölve, BEIR-alkészletek: SciFact, NFCorpus, FiQA): *„Jev, 30 Nouls in one state | 0.768 | 0.358 | 0.376 | ...| $0.13–0.19"*, és összegzésként: *„a general decision model with no reranker training lands in the same quality and price bracket as the best purpose-built rerankers, a third of Cohere's price... trading with Voyage, the strongest purpose-built reranker here (edge on SciFact, tie on NFCorpus, loss on FiQA by ~0.02)."* (pypi.org/project/hev-rerank)

**Független kalibrációs vizsgálat.** A `jevrag` csomag (T2, MIT, kalibrációs metrikák: ECE, Brier, AURC) direkt a memória-rendszer szempontjából releváns kérdést teszi fel — mennyire bízható a Jev magabiztossága döntésenként —, és a válasz: nem egységes. *„Its confidence Jev returns *ranks* good evidence above bad evidence reasonably well (its AURC of 0.4470 sits well between a perfect signal's 0.1724 and a useless signal's 0.5871). But its absolute numbers are not well calibrated: ... ECE = 0.3322 ... it does *worse* than a naive constant guess by one standard measure (Brier skill = −0.4486)."* egy „evidence-sufficiency" (mennyi bizonyíték elég) döntésnél, míg egy másik döntéstípusnál (`chunk-boundary`) *„ECE 0.087 and Brier skill +0.21"* — vagyis jól kalibrált. Konklúziójuk: *„Jev's confidence is not uniformly trustworthy or untrustworthy — it depends on the specific question being asked."* (pypi.org/project/jevrag)

**Összegzés (Q1/relevancia):** legalább négy egymástól független forrás (TypeSafe saját cookbookja, hev-rerank, jev-relevance/BEIR, jevrag) ad számszerű, reprodukálható adatot; a konzisztens üzenet, hogy a Jev-alapú reranking/relevancia-szűrés versenyképes a bevett cross-encoder rerankerekkel (Cohere, Voyage, Mixedbread szinten), de a *magabiztosság-értéke* (ami a memória-rendszer D-20/D-38 típusú küszöb-döntéseihez kellene) döntéstípus-függően megbízhatatlan lehet.

## 2. Agent-memória rendszerek és Jev/„döntési modell" beépítés

### 2.1 A vizsgált rendszerek saját dokumentációja és GitHub-ja

Közvetlenül átnéztem/kerestem a mem0 (`mem0ai/mem0` GitHub), a Zep (`getzep/zep` GitHub, hivatalos blog), a Letta (`letta-ai/letta`, korábban MemGPT) és a Basic Memory (`basicmachines-co/basic-memory`) hivatalos anyagait, „Jev", „TypeSafe" és „System One model" kulcsszavakkal kombinálva. **Egyikben sem találtam Jev- vagy TypeSafe-integrációt, sem nyitott issue-t, sem dokumentációs utalást.** Ez negatív találat: a keresés lefedte a hivatalos repókat és a launch (2026-09-15) utáni közösségi visszhangot is 2026-09-25-ig, de a Jev nagyon friss termék, így a hiány részben az idő rövidségének is betudható, nem feltétlenül elvi inkompatibilitásnak.

Amit *helyette* találtam ezekben a rendszerekben, releváns háttérként a memória-rendszer D-20/D-38 kérdéséhez:

- A Basic Memory ténylegesen használ egy kis, helyben futó cross-encoder rerankert, de **nem Jevet**, hanem egy nyílt súlyú modellt: *„Optional search reranking. Rescore the strongest vector and hybrid candidates with a local FastEmbed cross-encoder or a LiteLLM-backed provider... The default model is `jinaai/jina-reranker-v1-tiny-en`."* (github.com/basicmachines-co/basic-memory)
- A mem0-ban nyílt, élő vita zajlik pontosan az ellentmondás-kezelésről, tisztán LLM-alapon (nem Jev-szerű típusos döntéssel): egy GitHub-issue (`mem0ai/mem0#4536`, T1, 2026-03–07) szerint *„The DEFAULT_UPDATE_MEMORY_PROMPT... says that when an added fact is contradictory, then the fact is deleted... perhaps instead the memory should be updated"*, amire válaszul *„This behavior changed in the v3 memory pipeline... The v3 algorithm is ADD-only — it no longer uses DELETE for contradictions. Instead, contradicting facts are extracted as new memories and linked to existing ones via `linked_memory_ids`."* — vagyis a mem0 az LLM-et magát kéri meg a kontradikció eldöntésére, nem egy külön, gyors, típusos modellt.
- Egy másik, közvetve releváns GitHub-jegyzőkönyv (Hermes-agent + Hindsight memóriaszolgáltatás, T2, dátum nélkül, de 2026-as) empirikusan igazolja a memória-rendszer saját feltételezését, hogy *„beágyazással nem megbízható"* az ellentmondás-detekció: *„a similarity metric cannot distinguish a restatement from a contradiction"*, konkrét adatokkal: `„decided to adopt Kafka…" vs „decided not to adopt Kafka…"` Jaccard-hasonlósága 0.825, `„late-delivery penalty at 0.01%/day" vs „at 0.03%/day"` 0.771, `„deployment is feasible" vs „is not feasible"` 0.880 — mindhárom a duplikátum-küszöb *fölött* van, holott valójában ellentmondások. (github.com/NousResearch/hermes-agent — a GitHub URL formátuma alapján ez egy issue-idézet, nem hivatalos Nous-repó; független megerősítésként kezelendő, nem Jevről szól, hanem a probléma valóságáról.)

### 2.2 Egyetlen talált, kifejezetten Jev-alapú, tudományos publikációjú memória-architektúra

A `arXiv:2609.23986`, „**Jev-Mem: System-One-Controlled Agentic Memory for Efficient AI Agents**" (T1, 2026-09-21, szerzők: Dongming Jiang, Yi Li, Bingzhe Li, University of Texas at Dallas — a TypeSafe-től független egyetemi kutatás, kód nyilvánosan elérhető: `github.com/libingzheren/Jev-Mem`) pontosan a SQ05 2. kérdésére válaszol. Idézet: *„Jev TypeSafe AI (2026) makes such a separation practical by producing typed probabilistic decisions without autoregressive generation... Jev-Mem introduces a dedicated System-One control plane that handles high-frequency structured decisions, a shared structured memory data plane, and a System-Two reasoning plane reserved for complex synthesis and answer generation."*

A beépítés helye a memória-életciklusban — szó szerint: *„on the write path, System One performs memory typing, redundancy filtering, and semantic, temporal, causal, and entity relation construction; on the read path, it performs query routing, retrieval-budget allocation, graph traversal, candidate scoring, evidence assessment, and adaptive stopping."* Vagyis a Jev itt éppen a memória-rendszer duplikátum-szűrését („redundancy filtering") és kapcsolat-/ellentmondás-észlelését („contradiction" a karbantartási körben) is végzi.

**Kapcsolhatóság.** A szerzők explicit hangsúlyozzák, hogy nem a Jevhez vannak kötve: *„Jev provides one concrete realization of the System-One controller through typed probabilistic decisions, but the key novelty of Jev-Mem is the architectural separation of lightweight memory control from deliberative reasoning."* — tehát a „System-One control plane" interfész elvben más, hasonló döntési modellel is helyettesíthető (ezt maga a cikk nem teszteli más backenddel, csak kimondja az architektúra szándékát).

**Mért eredmény (LoCoMo benchmark, saját mérés, T1, tehát ellenőrzés alatt tartandó, mert a szerzők saját rendszerüket mérik):** *„on LoCoMo Jev-Mem achieves an overall LLM-as-a-Judge score of 0.777, an 11.0% relative improvement over the strongest baseline, while reducing memory construction time to 158 s, a 6.6× speedup over the fastest competing memory system, and lowering average query latency to 0.93 s, a 36.7% reduction."* Ez egyetlen forrás (a cikk saját benchmarkja); két független megerősítést erre NEM találtam — a cikk 2026-09-21-i, tehát négy nappal a kutatás lezárása előtti, még nincs idézettsége vagy reprodukciója.

### 2.3 Kisebb, nem „named" memória-/RAG-eszközök Jev-integrációval

Több önálló, kisebb nyílt forráskódú csomag köti be a Jevet kifejezetten RAG-kontextus-szűrésre (ami memória-visszaolvasásnál analóg feladat), de ezek egyike sem a felsorolt nagy rendszerek (mem0/Zep/Letta/Basic Memory) egyike, hanem önálló, kis közösségű projekt:

- `rag-jev` (PyPI, MIT): *„Inspectable context selection for existing RAG pipelines, powered by Jev... Python, HTTP, TypeScript, LangChain and Dify integrations are included."*
- `jev-relevance` (PyPI): LangChain `BaseRetriever` drop-in, saját BEIR/NFCorpus benchmarkkal: *„On nfcorpus at the default 0.5 threshold, Jev roughly doubles precision at the cost of some recall."*
- „Zerikai Memory" — egy egyéni fejlesztő IDE-agent kód-keresési memóriarétege, amely kifejezetten a relevancia/ellentmondás/prompt-injekció szétválasztására használja a Jevet (l. 1.5 pont).

Ezek pluggable jellegűek (interfész mögé rejtett, cserélhető backend), de nem a nevesített, elterjedt memória-rendszerek részei, hanem azok mellett/helyett futó, saját kisprojektek.

## 3. A Jevhez hasonló kategóriák és alternatívák — csak annyira, hogy a hely érthető legyen

A cél itt NEM teljes piackép, csak annyi, hogy a Jev egy nagyobb mezőnyben hol helyezkedik el a memória-rendszer releváns feladataira (osztályozás, relevancia-rangsorolás, ellentmondás).

**Zero-shot szöveg-osztályozás — NLI cross-encoder, embedding-modell, reranker, instrukció-hangolt LLM összevetése.** A BTZSC (ICLR 2026, T1 akadémiai benchmark, 22 nyilvános adathalmaz, 38 modell — Jev maga NEM szerepel benne, mert zárt, fizetős API, a benchmark csak nyílt checkpointokat mér) fő eredményei: *„modern rerankers, exemplified by Qwen3-Reranker-8B, set a new state-of-the-art with macro F1 = 0.72; ... strong embedding models such as GTE-large-en-v1.5 substantially close the accuracy gap while offering the best trade-off between accuracy and latency; ... NLI cross-encoders plateau even as backbone size increases."* Konkrét számok: `ms-marco-MiniLM-L6-v2` reranker átlag F1 0.42 (gyengébb, mint az NLI cross-encoderek), a legjobb NLI cross-encoder (`deberta-v3-large-nli-triplet`) kb. F1 0.58-0.60 körül, `gte-large-en-v1.5` embedding-modell F1 0.62, instrukció-hangolt LLM-ek (4-12B) F1 akár 0.67-ig. (arxiv.org/html/2603.11991)

Ez azt jelzi: a Jevhez hasonló „típusos döntés" kategóriában versengő legjobb *nyílt* megoldások (nagy reranker vagy közepes LLM) F1 0.6-0.72 tartományban vannak egy nehéz, sok-osztályos zero-shot feladaton — ezzel szemben a fentebb (1.1 pont) idézett Jev-mérések (Banking77, 77 osztály) 79-83% *accuracy* körül mozognak, ami más metrika és más adathalmaz, ezért **közvetlen számszerű összevetés a Jev és a BTZSC-modellek közt nem lehetséges** ezekből a forrásokból — csak a nagyságrendi kép állítható fel (mindkettő „jó, de nem tökéletes" sávban van, a frontier LLM-ek fölötte).

**Cross-encoder reranker vs. Jev közvetlen összevetés.** Ezt már az 1.6 pontban (`hev-rerank`) idéztem: Jev *„at or above Cohere on all three corpora... trading with Voyage."*

**Nyílt „System One"-stílusú alternatívák magához a Jevhez.** A gadgetpilipinas.net cikk (T2, 2026-09-20) szerint néhány nappal a Jev után megjelent egy nyílt válasz, a „Laya": *„Laya is Apache-2.0 and ships three checkpoints: a 421M English model, a 322M multilingual model... Mukkunnoth reports 32.8ms per question on one T4 GPU... 0.766 on the shared typed-decisions set against Jev's published 0.727."* Egy független (T2) teszt más eredményt hozott: *„Jev, run by the suite's author against the hosted API, scored 0.974. A 27B model compressed to about one bit per weight scored 0.885, GLiNER2 0.795, Von 0.769, and Laya last at 0.590 while still being fastest at 30ms per case against roughly 302ms for Jev."* — vagyis a kis, helyi „System One"-klónok (Laya, von, mini-jev, jev-lite) sebességben versenyeznek, pontosságban egyelőre lemaradnak. (gadgetpilipinas.net/2026/09/typesafe-jev-system-one-model-laya)

**NLI-modellek ellentmondásra.** Kifejezett Jev-vs-NLI-modell (pl. DeBERTa-MNLI) közvetlen benchmarkot **nem találtam**. A BTZSC és a „Building Efficient Universal Classifiers with NLI" (arXiv:2312.17543, T1) cikkek az NLI-alapú zero-shot klasszifikáció általános erősségeit/korlátait írják le (pl. *„deberta-v3-zeroshot-v1.1-all-33... significantly outperforms the NLI-only model both on held-in and held-out tasks"*), de ezek nem a Jevvel összevetve, hanem egymás közt mérnek.

## 4. Egy második modell (pl. Jev) ellenőrzésének haszna, ha az ELSŐ döntést már egy frontier LLM meghozta

**A pontos kérdésre — frontier LLM (Claude/Codex) dönt ELŐSZÖR, egy gyors, olcsó típusos modell (Jev) ELLENŐRZI UTÓBB ugyanazt a döntést, és ez mennyit javít — NINCS FORRÁS.** Sem gyártói, sem független forrást nem találtam, amely pontosan ezt a sorrendet és pontosan a memória-rendszer által kérdezett esetet (kategória-döntés utólagos ellenőrzése) vizsgálná. Az összes talált kaszkád-jellegű forrás (gyártói és független egyaránt) a **fordított** sorrendet írja le és méri: az olcsó/gyors modell (Jev) dönt előbb, és csak bizonytalanság esetén escalálódik egy drágább/frontier modellhez — ez költség-optimalizáló, nem minőség-ellenőrző mintázat, és nem válaszol a memória-rendszer kérdésére.

Példák erre a (fordított sorrendű) mintázatra:
- OpenRouter blog: *„The Jev-verified cascade cookbook has the escalation pattern in code, with a cheap model drafting, Jev checking the draft, and a frontier model handling only what fails the check."* — itt Jev a KÖZÉPSŐ, nem az utolsó ellenőr, és nem egy frontier döntés utólagos ellenőrzője. (openrouter.ai/blog/insights/jev-vs-claude-opus-5-classification)
- AY Automate: *„TypeSafe's docs include an extraction cascade cookbook built on the same idea: let the cheap model answer when it is sure and escalate when it is not."* — Jev dönt előbb.
- JevBench: *„Jev → DeepSeek v4 Pro cascade | 80.2%"*, *„Answer with Jev when its confidence clears a threshold and escalate to a larger model otherwise"* — ismét Jev előbb.

**A legközelebbi, de nem azonos helyzet:** a Vega.io-eset (l. 1.2), ahol Jev egy már működő triage-*agent* döntése *elé* (nem mögé) került kapuként, tenant-kontextussal kiegészítve — ez nem „utólagos ellenőrzés", hanem helyettesítő előszűrés, és a szerzők maguk mondják ki: *„We also checked whether it could decide outright, which was never the goal. It cannot."*

**Áttételesen releváns, de nem Jev-specifikus akadémiai irodalom**, amit óvatosan, egyértelműen elkülönítve közlök, mert nem a pontos kérdésre válaszol:

- „Cheap Verifiers, Large Blind Spots: Measuring the Reliability Cost of Cost-Saving Cascades" (arXiv:2609.01345, 2026-09-01, T1): *„the verifier's blind spot, the fraction of the student's wrong answers it accepts, is large and moves adversarially: it grows with student capability (β from 0.12 to 0.55 as the student scales 0.5B to 32B) and shrinks with verifier capability."* Ez azt sugallja — de matematikailag/módszertanilag EGY MÁS beállításban (olcsó tanuló + olcsó ellenőrző, nem „frontier dönt, olcsó ellenőriz") —, hogy egy olcsó ellenőrző modell vakfoltja éppen egy *erősebb, magabiztosabb* döntéshozó hibáinál nagyobb, ami a memória-rendszer felvetésére nézve óvatosságra int: nem biztos, hogy Jev jól fogná ki, ha Claude/Codex hibázik.
- „Variation in Verification: Understanding Verification Dynamics in Large Language Models" (arXiv:2509.17995, T1): *„we identify regimes where a strong verifier (e.g., GPT-4o) offers no additional benefit and can be replaced by a weaker verifier... This occurs with strong generators or with problems at either extreme of the difficulty spectrum."* — vagyis általánosan (nem Jevre nézve), minél erősebb az „első döntéshozó", annál kevesebb a marginális haszna BÁRMILYEN második ellenőrzésnek, gyengének vagy erősnek egyaránt.
- „Towards a Cascaded LLM Framework for Cost-effective Human-AI Decision-Making" (arXiv:2506.11887 / NeurIPS 2025, T1) és a „CrossVerify" (2026-09-16, T1) cikkek is a kaszkád/ellenőrzés általános elméletét építik, de egyik sem Jev-specifikus, és egyik sem a „frontier dönt előbb" sorrendet vizsgálja fő esetként.

**Egyetlen konkrét, bár nem „ellenőrzés utólag" jellegű, hanem párhuzamos-összevetés jellegű adatpont**, amely mégis tájékoztat a kérdés irányáról: a dev.to/bengreenberg Arbitrum-teszt (l. 1.1) megfigyelése, hogy *„Sonnet recognized that something was wrong, but it was highly confident in the wrong category"* — azaz amikor Claude Sonnet hibázott, azt magabiztosan tette (0.9-1.0-es sávban), míg a Jev hibái alacsony konfidenciával jártak (0.2-0.3). Ez — egyetlen, 306 döntéses, egy szerzős, nem-peer-reviewed forrásból — arra utalhat, hogy ha lenne is haszna egy Jev-alapú második véleménynek, az valószínűbb, hogy a Jev *saját* alacsony konfidenciájú eseteinél jelentkezne, nem feltétlenül azáltal, hogy Jev felülbírálná Claude magabiztos, de téves válaszát. Ez azonban egyetlen, meg nem erősített forrás, ezért **nem tekinthető megbízható válasznak a Q4 kérdésre**, csak egy irányjelző adalék.

**Összegzés (Q4): a memória-rendszer által feltett pontos kérdésre nincs forrás. A rendelkezésre álló irodalom (gyártói és akadémiai is) szinte kizárólag a fordított munkamegosztást (olcsó dönt előbb, drága ellenőriz/escalál utólag) dokumentálja, és az egyetlen áttételes akadémiai jelzés (Cheap Verifiers, Large Blind Spots) inkább amellett szól, hogy egy gyors, olcsó modell nem feltétlenül fogja jól elkapni egy erősebb, magabiztos modell tévedéseit.**

## Ellentmondások

1. **A Jev pontossága klasszifikáción**: nagyon szórnak az eredmények forrásonként és feladatonként — a JevBench aggregátor saját maga mondja ki: *„Jev ranges from 62.6% to 95.4%. There is no universal Jev accuracy."* Van forrás, ahol Jev egyértelműen alulmarad a frontier LLM-ekhez képest (worldprogramming.org: 79.0% vs. 83.9-86.2%; OpenRouter Banking77: 81.0% vs. 84.4%; AY Automate: szignifikánsan rosszabb 8-way/77-way routingon), és van, ahol egyenrangú vagy jobb (dev.to/bengreenberg Arbitrum-teszt: 100.0% vs. 99.0%, jobb kalibrációval; dev.to/zika_zag projekt-választás: kevesebb hibás találat, mint Opus). Nem simítottam el: a kép feladatfüggő, és több forrás explicit figyelmeztet, hogy a gyártói (193.6×/444.6×) számok „valószínűleg a felső határ" (l. sq00).
2. **Jev kalibrációja**: a JevBench/OpenRouter szerint a Jev konfidenciája NEM kalibrált valószínűség (*„it's not a calibrated probability... it overestimated its own accuracy mid-range"*), miközben a `jevrag` független mérése szerint EGYES döntéstípusokon (chunk-boundary) igen jól kalibrált (ECE 0.087), MÁSOKON (evidence-sufficiency) rosszul (ECE 0.332) — vagyis maga a „kalibrált-e" kérdés forrásonként/feladatonként ellentmondó választ kap, és a legrészletesebb (jevrag) forrás szerint ez nem véletlen szórás, hanem feladatfüggő tulajdonság.
3. **Az architektúra eredetisége**: a gadgetpilipinas.net cikk szerint egy kutató (Nandakishor Mukkunnoth, ConvAI Innovations) azt állítja, a TypeSafe „uncredited prior art"-ot használt fel (2025 márciusi saját publikációra hivatkozva), míg a TypeSafe erre nyilvánosan nem reagált, és a Hacker News-közösség szerint „the concept has academic precursors and... TypeSafe's contribution was shipping a product." Ez vitatott állítás, mindkét oldalt idéztem, döntést nem hozok.

## Amire NINCS forrás

- **Pontosan a Q4 kérdésre** (frontier LLM ELSŐ döntése + Jev UTÓLAGOS ellenőrzése, és ennek számszerű haszna) — sem gyártói, sem független, sem akadémiai forrást nem találtam. Csak a fordított sorrendű (olcsó előbb, drága utólag) kaszkád-mintázatra van bőséges adat.
- **Két egymástól független, nem-vendor forrás a Jev deduplikációs/entitás-egyeztetési használatára** — csak a gyártói cookbook és annak egy T3 tükre van, önálló, független megerősítés nélkül.
- **Jev-specifikus, publikált, kontrollált NLI-kontradikció-benchmark** (pl. Jev közvetlenül egy DeBERTa-MNLI-szerű dedikált NLI-modellel összevetve ugyanazon adathalmazon) — nincs ilyen forrás; csak általános (nem Jev-es) NLI-benchmarkok (BTZSC) és Jev-es RAG-kontradikció *minta* (nem számszerű benchmark) van.
- **Bármilyen forrás arra, hogy a mem0, Zep, Letta vagy a Basic Memory hivatalos terméke natívan, dokumentáltan integrálná a Jevet vagy egy „System One"-stílusú döntési modellt** — a keresés (hivatalos dokumentáció, GitHub, blog) ezt nem találta; a Jev-Mem az egyetlen kapcsolódó, de ez egy tőlük független egyetemi kutatási prototípus, nem ezek egyike.
- **Független (nem a Jev-Mem szerzői által mért) megerősítés a Jev-Mem LoCoMo-benchmark számaira** (0.777 LLM-as-Judge, 11.0% relatív javulás, 6.6× gyorsulás) — a cikk 2026-09-21-i, egyelőre csak a szerzők saját mérése áll rendelkezésre.
- **Magyar nyelvű Jev-használati eset vagy magyar nyelvű benchmark** — az összes fenti forrás angol nyelvű feladatokról szól; erre lásd még az `sq00` „Amire NINCS forrás" pontját is (magyar nyelvi támogatás kérdése már ott is megválaszolatlan maradt).

## Meglátogatott és felderített linkek

| Cím | URL | Tier | Eszköz | Megjegyzés |
|---|---|---|---|---|
| Cookbooks (index) | https://docs.typesafe.ai/cookbooks | T1 | Exa web_fetch_exa | Hivatalos cookbook-lista, minden use case kategóriája (classification, RAG, guardrails, extraction stb.) |
| Re-ranking (cookbook) | https://docs.typesafe.ai/cookbooks/rerank_typesafe | T1 | Exa web_fetch_exa | CLERC jogi reranking, 5%→18% top-1, közvetlenül ellenőrizve |
| Knowledge graph entity alignment (cookbook) | https://docs.typesafe.ai/cookbooks/entity_alignment | T1 | Exa web_fetch_exa | Deduplikáció/entitás-egyeztetés, Beer/Magellan adatsor, 450 pár |
| Jev use cases — jevtypesafeai.com | https://jevtypesafeai.com/use-cases | T3 | Exa web_search_exa | Nem hivatalos tükör, moderálás/routing/guardrail lista |
| How to Use Jev: Moderation — OpenRouter Blog | https://openrouter.ai/blog/tutorials/how-to-use-jev/ | T2 | Exa web_search_exa | Gateway-partner tutorial, moderálás use case |
| Is Jev as Accurate as Frontier Models at Classification? — OpenRouter Blog | https://openrouter.ai/blog/insights/jev-vs-claude-opus-5-classification/ | T2 | Exa web_search_exa | Banking77, Jev vs Claude Opus 5, számszerű, statisztikai teszttel |
| 230x Faster, 2,000x Cheaper, 98% Right — Vega | https://vega.io/blog/jev-closed-up-to-a-third-of-our-triage-agents-alerts | T2 | Exa web_search_exa | Ügyfél-esettanulmány, SOC triage gate, humán-validált |
| Fast, Cheap Agent Decisions — Akka | https://akka.io/blog/fast-cheap-agent-decisions | T2 | Exa web_search_exa | Gateway-integráció, routing use case, nyílt „OpenJev" említése |
| Rebuilding our agent with Jev — Vuink.com | https://vuink.com/post/hfralz-d-dpbz/technical-blog/rebuilding-our-agent-with-jev | T3 | Exa web_search_exa | Független fejlesztői blog, konfidencia-alapú escalation |
| Early experimentation using Jev to rethink harness UX — elvex | https://www.elvex.com/blog/early-experimentation-using-jev-to-rethink-harness-ux | T2/T3 | Exa web_search_exa | Memória-worthiness osztályozás, ambient classification |
| RAG ranking is not the same as judging with Jev — DEV (Zerikai Memory) | https://dev.to/kike/how-i-went-from-trust-me-bro-to-boomer-with-receipts-using-jev-2141 | T2/T3 | Exa web_search_exa | Kontradikció+relevancia+injekció szétválasztása, memória-jellegű RAG-eszköz |
| How I Replaced Local Vector-Based Search with JEV — natashatherobot.com | https://www.natashatherobot.com/p/replaced-vector-search-with-jev | T3 | Exa web_search_exa | Gibberish-osztályozás, sok nyelvű bemenet |
| How to Build and Deploy a Jev-Powered App | https://www.ai.joaoqueiros.com/blog/build-jev-app-intelligent-form-vps-deployment | T3 | Exa web_search_exa | Lead-scoring use case, döntési kontraktus minta |
| I Built the First Java SDK for Jev — DEV | https://dev.to/jamilxt/i-built-the-first-java-sdk-for-jev-typesafes-system-one-model-2m37 | T3 | Exa web_search_exa | Guardrail „officially recommended use case" idézet |
| A New Kind of Model for AI Decision-Making? — WPS/Towards Data Science | https://www.worldprogramming.org/posts/a-new-kind-of-model-for-ai-decision-making-wepuso | T2 | Exa web_search_exa | Intent classification, Jev vs OpenAI Terra/Luna, számszerű pontosság |
| How to Use Jev — DEV (valyuai) | https://dev.to/valyuai/how-to-use-jev-a-practical-guide-to-typesafes-system-one-model-g5e | T3 | Exa web_search_exa | „What people shipped in first 48 hours" — több use case (papír-osztályozás, böngésző-agent, kereskedés) |
| TypeSafe Cookbook - Re-ranking (aggregátor) — frutik.github.io | https://frutik.github.io/awesome-search/Articles/TypeSafe-Cookbook---Re-ranking | T2 | Exa web_search_exa | Független elemzés a hivatalos rerank-cookbookról, statisztikai korlátok kiemelve |
| rag-jev v0.2.0 — PyPI | https://pypi.org/project/rag-jev/ | T2 | Exa web_search_exa | Önálló, nyílt forráskódú RAG-kontextusszűrő Jev-backenddel, LangChain/Dify integráció |
| Jev for RAG reranking — Jagent | https://jev-agent.com/use-cases/rag-reranking | T3 | Exa web_search_exa | Nem hivatalos, de konkrét kódpéldát ad relevancia-szűrésre |
| jev-relevance v0.1.0 — PyPI | https://pypi.org/project/jev-relevance/ | T2 | Exa web_search_exa | LangChain drop-in retriever, saját BEIR/NFCorpus benchmark |
| jev-reranker v0.1.2 — PyPI | https://pypi.org/project/jev-reranker/0.1.2/ | T2 | Exa web_search_exa | Listwise/pointwise/pairwise reranking könyvtár |
| jevrag v0.1.0 — PyPI | https://pypi.org/project/jevrag/ | T2 | Exa web_fetch_exa + web_search_exa | Kalibráció-first RAG döntési keretrendszer, ECE/Brier/AURC mérésekkel, cserélhető backend |
| TypeSafe Jev in JarvisCore — Prescott Data | https://developers.prescottdata.io/blog/typesafe-jev-agent-routing-rag-jarviscore | T2 | Exa web_search_exa | Agent-keretrendszer natív routing+RAG-kontradikció integráció |
| hev-rerank v0.1.0 — PyPI | https://pypi.org/project/hev-rerank/ | T2 | Exa web_search_exa | Jev vs Cohere/Voyage/Mixedbread reranker, BEIR nDCG@10 |
| Jev for RAG and citation checks — Refix | https://www.refix.ai/news/jev-rag-reranking-citation-checks/ | T2 | Exa web_search_exa | Relevancia/kontradikció/injekció/citáció-ellenőrzés szétválasztása |
| typedrank v0.1.1 — PyPI | https://pypi.org/project/typedrank/0.1.1/ | T2 | Exa web_search_exa | Univerzális típusos reranker keretrendszer, Jev és Laya backend |
| Basic Memory vs Mem0 vs Letta — Basic Memory Blog | https://basicmemory.com/blog/basic-memory-vs-mem0-vs-letta | T1 (saját termék) | Exa web_search_exa | Nincs Jev-említés; a piac-térkép kontextusához |
| basicmachines-co/basic-memory — GitHub | https://github.com/basicmachines-co/basic-memory/ | T1 | Exa web_search_exa | Saját reranker: `jinaai/jina-reranker-v1-tiny-en`, nem Jev |
| Mem0 vs Zep vs Letta vs Cognee vs LangMem — DEV | https://dev.to/izgorodin/mem0-vs-zep-vs-letta-vs-cognee-vs-langmem-vs-mnemoverse-an-honest-map-of-agent-memory-in-2026-3l7b | T2 | Exa web_search_exa | Piac-térkép, nincs Jev-említés |
| Suggest change to memory adding with contradicting facts — mem0 GitHub #4536 | https://github.com/mem0ai/mem0/issues/4536 | T1 | Exa web_search_exa | Mem0 saját, LLM-alapú kontradikció-kezelése, nem Jev |
| dedup restated facts / contradiction guard — Hermes-agent GitHub issue | https://github.com/NousResearch/hermes-agent/issues/88471 | T2 | Exa web_search_exa | Empirikus bizonyíték: embedding/Jaccard-hasonlóság nem különbözteti meg az ismétlést az ellentmondástól |
| Jev-Mem: System-One-Controlled Agentic Memory — arXiv | https://arxiv.org/abs/2609.23986 (HTML: https://arxiv.org/html/2609.23986) | T1 | Exa web_fetch_exa | Egyetemi (UT Dallas), Jev-alapú memória-architektúra, LoCoMo benchmark |
| BTZSC: A Benchmark for Zero-Shot Text Classification — arXiv | https://arxiv.org/html/2603.11991 | T1 | Exa web_search_exa | Akadémiai (ICLR 2026) NLI/embedding/reranker/LLM összevetés, Jev nélkül (zárt API) |
| Building Efficient Universal Classifiers with NLI — arXiv | https://arxiv.org/pdf/2312.17543v2.pdf | T1 | Exa web_search_exa | DeBERTa-v3 NLI-alapú zero-shot klasszifikáció háttere |
| JevBench — Independent evidence for Jev | https://jevbench.xyz/ | T2 | Exa web_fetch_exa | Független, szponzoráció nélküli benchmark-aggregátor, több feladat, PASS/FAIL/AMBIGUOUS jelöléssel |
| Jev vs Claude: Who Wins? — DEV (bengreenberg) | https://dev.to/bengreenberg/jev-vs-claude-who-wins-4mln | T3 | Exa web_search_exa | Egyedi, 306 döntéses teszt, kalibráció-összevetés (ECE) |
| Picking a New Task's Project in 200 ms — DEV | https://dev.to/zika_zag_c43dc387e13f45ea/picking-a-new-tasks-project-in-200-ms-jev-vs-claude-on-53-of-my-tasks-32ab | T3 | Exa web_search_exa | Kategória-választás (projekt-hozzárendelés) Jev vs Claude Opus/Sonnet/Haiku |
| Jev vs GPT-5 vs Claude for AI Classification and Routing — alekseialeinikov.com | https://www.alekseialeinikov.com/en/blog/topics/ai/jev-vs-gpt-5-claude-classification-routing | T2/T3 | Exa web_search_exa | Döntési fa: kód / Jev / frontier LLM mikor melyik |
| Jev vs GPT and Claude: Independent Benchmark (2026) — AY Automate | https://www.ayautomate.com/blog/jev-vs-llm-benchmark | T2 | Exa web_search_exa | Módszertanilag legrészletesebb független benchmark (McNemar, Wilson-intervallum) |
| Jev in the Agent Runtime — Bloss0m | https://www.bloss0m.com/en/blog/108-jev-confidence-gated-agent-runtime/ | T2/T3 | Exa web_search_exa | Konfidencia-kapuzási minta ágens-futtatókörnyezetben |
| TypeSafe Jev: System One Model, answered by Laya — gadgetpilipinas.net | https://www.gadgetpilipinas.net/2026/09/typesafe-jev-system-one-model-laya/ | T2 | Exa web_search_exa | Nyílt alternatíva (Laya), prioritási vita, független teszt-számok |
| How Jev Works: The Logit Trick — DEV | https://dev.to/programmerraja/how-jev-works-the-logit-trick-behind-typesafes-system-one-model-4lpd | T3 | Exa web_search_exa | Technikai magyarázat (logit-olvasás), RLCD kritikai megjegyzések |
| Towards a Cascaded LLM Framework — arXiv | https://arxiv.org/html/2506.11887v2 | T1 | Exa web_search_exa | Akadémiai kaszkád-elmélet, NEM Jev-specifikus, fordított sorrend (olcsó előbb) |
| Cheap Verifiers, Large Blind Spots — arXiv | https://arxiv.org/abs/2609.01345 | T1 | Exa web_search_exa | Áttételesen releváns Q4-hez: olcsó ellenőrző vakfoltja nő az erősebb „student" mellett |
| Variation in Verification — arXiv | https://arxiv.org/html/2509.17995 | T1 | Exa web_search_exa | Áttételesen releváns Q4-hez: erős generátornál az ellenőrzés haszna csökken |
| Moving My Research Pipeline's Judgment Calls to Jev — DEV | https://dev.to/shimo4228/moving-my-research-pipelines-judgment-calls-from-an-llm-to-jev-a-judgment-only-model-4ncj | T3 | Exa web_search_exa | Relevancia-ítélet kutatási pipeline-ban, Claude tervez / Jev ítél munkamegosztás |
| Jev for LLM routing — Jagent | https://jev-agent.com/use-cases/llm-model-routing | T3 | Exa web_search_exa | Modell-kaszkád routing minta, nem hivatalos oldal |
| Stop Sending Every Decision to an LLM — DEV | https://dev.to/sreeni5018/stop-sending-every-decision-to-an-llm-code-vs-jev-vs-claude-32e4 | T3 | Exa web_search_exa | Kód/Jev/Claude háromrétegű döntési architektúra |
| How to Use Jev With Claude Code, Codex and Cursor — DEV | https://dev.to/sebastianbennis/how-to-use-jev-with-claude-code-codex-and-cursor-free-reference-file-54a3 | T3 | Exa web_search_exa | Kifejezetten Claude Code/Codex-szel kombinált használat, API-hibák dokumentálása |
| Ask HN: Thinking about memory for AI coding agents | https://news.ycombinator.com/item?id=46742800 | T3 | Exa web_search_exa | Közösségi vita memória-deduplikációról, nincs Jev-említés |
| Mem0 stores memories, but doesn't learn user patterns — HN | https://news.ycombinator.com/item?id=46891715 | T3 | Exa web_search_exa | Piac-kontextus, nincs Jev-említés |
| similar memories repeat quite frequently — mem0 GitHub #5205 | https://github.com/mem0ai/mem0/issues/5205 | T1 | Exa web_search_exa | Mem0 dedup/kontradikció gyakorlati problémái, nem Jev |
| Mem0 vs Letta vs Zep — plur-ai GitHub Discussion #654 | https://github.com/plur-ai/plur/discussions/654 | T2 | Exa web_search_exa | Piac-térkép, nincs Jev-említés |

---

# SQ06 — Kapcsolható külső modell: kikapcsolás, elfogyó keret, automatikus visszaállás — a bevett minták

*Kutatási eszköz: kizárólag Exa (`web_search_exa`) a beépített WebSearch/WebFetch helyett, az utasításnak megfelelően (`web_fetch_exa`-ra nem volt szükség, mert a keresési highlightok minden esetben elegendő szó szerinti szöveget adtak). Alügynök-indítás (a `deep-web-research` skill teljes, sok-ügynökös pipeline-ja) ebben a körben sem történt — ez egy egyszeri, célzott mintakutatás, ezért degradált, de Exa-only módban, kizárólag elsődleges (gyártói/szabványforrás) dokumentációra és a névvel megnevezett kanonikus szerzőkre (Fowler, Dean & Barroso, Marc Brooker) támaszkodva dolgoztam. A Jev/TypeSafe-specifikus tényeket (SQ00) itt nem kutattam újra — ez a fájl kizárólag az általános, technológia-független bevett mintákról szól, amiket a felhasználó feltétele (kapcsoló, elfogyó keret, automatikus visszaállás) megkövetel egy tetszőleges kapcsolható külső döntési modellhez.*

## Rövid válasz

A négy kért terület mindegyikére van jól dokumentált, elsődleges forrásokból származó, egymással is megerősített bevett minta. (1) A **circuit breaker** mintát az Azure Architecture Center, Martin Fowler és három konkrét könyvtár (Resilience4j – Java, Polly – .NET, opossum – Node.js) egyaránt Closed/Open/Half-Open állapotgépként írja le; Node/TypeScript környezetre az `opossum` a kanonikus választás, és az npm-regisztrációja szerint **0 futásidejű függősége** van, ami illeszkedik a „kevés külső függőség” elvhez (D-01/8). (2) A **feature flag / kill switch** Martin Fowler (illetve Pete Hodgson) által névvel is „Kill Switch”-nek nevezett, futásidőben, konfigurációból kapcsolható mintája; az AWS Well-Architected Framework ugyanezt a mechanizmust (feature flag, újratelepítés nélküli visszakapcsolás) a biztonságos kiadási stratégiák részeként ajánlja. (3) A **graceful degradation/fallback** a Google SRE könyv szerint sosem lehet néma: a leállás/visszaváltás eseményét naplózni és riasztani kell, ezt az Azure Architecture Center és a Polly telemetria-mechanizmusa is megerősíti — ez közvetlenül válaszolja a „mikor kell jelezni” kérdést: **mindig**, amikor az állapot megváltozik. (4) A **timeout/hedging/deadline propagation** kánonja az AWS Builders' Library (Marc Brooker), a Google SRE könyv és a gRPC hivatalos dokumentációja: minden távoli hívásra kell timeout, a determinisztikus végső határidőt (deadline) a hívási lánc tetején kell kijelölni és lefelé kell örökíteni (deadline propagation), a „hedging” pedig egy második, párhuzamos próbahívás a p95 késleltetés után (Dean & Barroso, „The Tail at Scale”) — de **konkrét ezredmásodperc-ajánlást egyik elsődleges forrás sem ad**, mindegyik explicit módon szolgáltatás-specifikusnak mondja ezt. (5) A **költségkeret-kezelésre** az LLM-gateway-ek (LiteLLM, OpenRouter, Portkey) és az AWS mind ugyanazt a két rétegű mintát követik: puha figyelmeztetés (soft budget/alert) egy küszöbnél, majd kemény blokkolás vagy más modellre terelés (fallback) a tényleges kereten; az AWS API Gateway dokumentációja ugyanakkor kifejezetten figyelmeztet, hogy a rate-limit/quota **nem** megbízható költségkorlát, arra külön AWS Budgets Actions szolgál. (6) A **megfigyelhetőségre/árnyék-módra** az AWS SageMaker „shadow testing” hivatalos dokumentációja és egy széles körben idézett gyakorlati blogbejegyzés (Neal Lathia) ad kanonikus leírást: az új modell mindent kiszámol és naplóz, de a döntést a régi módszer hozza, majd utólag hasonlítják össze — ez pontosan a felhasználó „ne erőltessük, de vizsgáljuk ki” elvárásának technikai megvalósítása.

---

## 1. Circuit breaker: állapotok, küszöbök, félig nyitott próba

### Kanonikus leírás (Azure Architecture Center, Martin Fowler)

Az Azure Architecture Center a mintát proxy-ként írja le, három állapottal:

> „**Closed:** The request from the application is routed to the operation. The proxy maintains a count of the number of recent failures. If the call to the operation is unsuccessful, the proxy increments this count. If the number of recent failures exceeds a specified threshold within a given time period, the proxy is placed into the **Open** state and starts a time-out timer. When the timer expires, the proxy is placed into the **Half-Open** state.“
> „**Open:** The request from the application fails immediately and an exception is returned to the application.“
> „**Half-Open:** A limited number of requests from the application are allowed to pass through and invoke the operation. If these requests are successful, the circuit breaker assumes that the fault that caused the failure is fixed, and the circuit breaker switches to the **Closed** state. […] If any request fails, the circuit breaker assumes that the fault is still present, so it reverts to the **Open** state.“
(learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker, `ms.date: 02/05/2025`)

Martin Fowler (a minta népszerűsítője, Michael Nygard „Release It!” könyvére hivatkozva) ugyanezt tömören így fogalmazza meg:

> „You wrap a protected function call in a circuit breaker object, which monitors for failures. Once the failures reach a certain threshold, the circuit breaker trips, and all further calls to the circuit breaker return with an error, without the protected call being made at all. Usually you'll also want some kind of monitor alert if the circuit breaker trips.“
(martinfowler.com/bliki/CircuitBreaker.html, 2014-03-06)

A Wikipédia „Circuit breaker design pattern” szócikke ugyanezt a három állapotot (Closed/Open/Half-open) írja le, harmadlagos, de a fentieket megerősítő forrásként.

### Konkrét könyvtárak és küszöbök

**Resilience4j (Java)** — a hivatalos dokumentáció szerint a modern verzió három normál állapotot (`CLOSED`, `OPEN`, `HALF_OPEN`) és három speciális állapotot (`METRICS_ONLY`, `DISABLED`, `FORCED_OPEN`) különböztet meg:

> „The CircuitBreaker is implemented via a finite state machine with three normal states: CLOSED, OPEN and HALF_OPEN and three special states METRICS_ONLY, DISABLED and FORCED_OPEN.“
(resilience4j.readme.io/docs/circuitbreaker)

Alapértelmezett küszöbök a forráskódból (`CircuitBreakerConfig.java`, resilience4j GitHub repó): `failureRateThreshold = 50` (%), `slidingWindowSize = 100`, `minimumNumberOfCalls = 100`, `waitDurationInOpenState = 60` másodperc, `permittedNumberOfCallsInHalfOpenState = 10`. A `DISABLED` állapot explicit „mindig enged” (kikapcsolt breaker), a `FORCED_OPEN` explicit „mindig tilt” — ez gyakorlatilag a manuális kapcsoló (kill switch) beépített megfelelője magában a könyvtárban.

**Polly (.NET, v8/Polly.Core)** — más alapértelmezett számokkal, és architektúrában is eltérő félig-nyitott logikával:

> „`FailureRatio` | 0.1 | The failure-success ratio that will cause the circuit to break/open. `0.1` means 10% failed of all sampled executions.“
> „`MinimumThroughput` | 100 | The minimum number of executions that must occur within the specified sampling duration.“
> „`SamplingDuration` | 30 seconds […] `BreakDuration` | 5 seconds […]“
> „If the first action after the break duration period results in a handled exception, the circuit will break again for another BreakDuration; if no exception is thrown, the circuit will reset.“
(pollydocs.org/strategies/circuit-breaker és pollydocs.org/api/Polly.CircuitBreaker.CircuitBreakerStrategyOptions-1.html)

Polly négy állapotot különböztet meg: `Closed`, `Open`, `HalfOpen`, és egy explicit manuális `Isolated` állapotot (`CircuitBreakerManualControl`), ami — akárcsak Resilience4j `FORCED_OPEN`-je — direkt kapcsolóként (kill switch) is használható kódból.

**opossum (Node.js)** — a hivatalos GitHub/npm leírás:

> „Opossum is a Node.js circuit breaker that executes asynchronous functions and monitors their execution status. When things start failing, `opossum` plays dead and fails fast. If you want, you can provide a fallback function to be executed when in the failure state.“
(github.com/nodeshift/opossum, nodeshift.dev/opossum/)

**Van-e TypeScript/Node könyvtár, és mekkora függőség?** Igen — az `opossum` a kanonikus Node.js circuit breaker (Red Hat/nodeshift fejleszti, Apache-2.0 licenc, ~900K–1,3M heti letöltés, 390+ függő csomag). A hivatalos npm-regisztráció szerint:

> „0 Dependencies“ — „Unpacked Size: 382.7KB“ — „Total Files: 13“
(registry.npmjs.org/opossum; a depscope.dev független csomag-egészségügyi oldal is megerősíti: „0 deps“)

TypeScript-típusdefiníció külön csomagban érhető el (`@types/opossum`, DefinitelyTyped), nem a fő csomag része — ez a hivatalos dokumentáció explicit megjegyzése mindkét vizsgált verzióban (8.1.3 és a jelenlegi GitHub README). A GitHub aktuális főágán az „Engines: Node.js >= 22” szerepel, míg a nodeshift.dev/opossum/ 8.1.3-as dokumentációs pillanatképe még „Node.js >= 16”-ot ír — ez a dokumentáció-verziók közti eltérés, nem ellentmondás (lásd „Ellentmondások”).

Java oldalon a `resilience4j-core` (2.4.0-s Maven POM szerint) egyetlen futásidejű függősége az `slf4j-api`; a GitHub release-jegyzetek szerint a korábban jelen lévő Vavr-függőséget is eltávolították („Removed Vavr as a dependency”, v2.0.0) — tehát Resilience4j is a „minimális függőség” elvet követi, bár ez a tény a Maven POM-fájlból és a release note-okból derül ki, nem egyetlen hivatalos prózai kijelentésből (lásd „Amire nincs forrás”).

---

## 2. Feature flag / kill switch: futásidejű kikapcsolás konfigurációból

Martin Fowler / Pete Hodgson kanonikus cikke a „Feature Toggles”-en belül külön kategóriaként nevezi meg az „Ops Toggle”-ök egy alcsoportját „Kill Switch” néven:

> „However it's not uncommon for systems to have a small number of long-lived **“Kill Switches”** which allow operators of production environments to gracefully degrade non-vital system functionality when the system is enduring unusually high load. […] These types of long-lived Ops Toggles **could be seen as a manually-managed Circuit Breaker.**“
(martinfowler.com/articles/feature-toggles.html, Pete Hodgson, 2017-10-09)

Fowler saját, korábbi bliki-bejegyzése a kategóriákat is rögzíti (release, experiment, ops, permissioning toggle), és explicit kimondja, hogy a legtöbb feature flag futásidőben állítható, konfigurációs fájlból:

> „Most feature flags I've heard about are set at run-time […]“
> „Hodgson also identifies experiment toggles for A/B testing, **ops toggles to provide controls for operations staff**, and permissioning toggles […]“
(martinfowler.com/bliki/FeatureFlag.html, 2010-10-29)

Ezt a mintát az AWS Well-Architected Framework, más terminológiával (de gyakorlatilag azonos mechanizmusként), a megbízhatósági/üzemeltetési pillérben is ajánlja:

> „Feature flags (also known as feature toggles) are configuration options on an application. You can deploy the software with a feature turned off […]. You can then turn on the feature […] or you can set the change pace to 100% to see the effect. **If the deployment has problems, you can simply turn the feature back off without rolling back.**“
(docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/implement-change.html)

Az AWS Well-Architected Operational Excellence pillér (OPS06-BP01, OPS06-BP04) a feature flag-et explicit felsorolja a „sikertelen változtatás visszaállítására” szolgáló stratégiák és az automatizált teszt/rollback eszközök között — de az AWS anyagai nem használják a „kill switch” elnevezést, ez kifejezetten Fowler/Hodgson terminológiai hozzájárulása; a mögöttes mechanizmus (futásidejű, konfiguráció-vezérelt ki/bekapcsolás, üzemeltetői kézben) viszont a két, egymástól független forrásban (Fowler — gyakorló tanácsadó cég, ThoughtWorks; AWS — felhőszolgáltató) egyezik.

---

## 3. Graceful degradation / fallback: mikor tilos a csendes visszaállás

A Google SRE könyv 22. fejezete („Addressing Cascading Failures”) külön alfejezetet szentel a „Load Shedding and Graceful Degradation”-nek, és explicit megköveteli a megfigyelhetőséget:

> „**Monitor and alert when too many servers enter these modes.**“
> „Complex load shedding and graceful degradation can cause problems themselves […] **Design a way to quickly turn off complex graceful degradation or tune parameters if needed.** Storing this configuration in a consistent system that each server can watch for changes […] can increase deployment speed […]“
> „**Graceful degradation shouldn't trigger very often**—usually in cases of a capacity planning failure or unexpected load shift. Keep the system simple and understandable, particularly if it isn't used often.“
> „Remember that **the code path you never use is the code path that (often) doesn't work.** In steady-state operation, graceful degradation mode won't be used, implying that you'll have much less operational experience with this mode […] You can make sure that graceful degradation stays working by regularly running a small subset of servers near overload in order to exercise this code path.“
(sre.google/sre-book/addressing-cascading-failures/, szerző: Mike Ulrich)

Ez közvetlenül válaszolja a kérdést: a Google SRE könyv szerint a degradált/visszaesési mód **soha nem lehet néma** — kötelező a monitorozás és riasztás minden alkalommal, amikor egy szerver degradált módba lép, és kötelező egy explicit, gyors kikapcsolási mechanizmust is biztosítani magára a degradációs logikára (ami gyakorlatilag egy második szintű kill switch: kikapcsoló a fallback-logika fölött).

Az Azure Architecture Center ugyanezt az elvet a circuit breaker állapotváltásaira mondja ki:

> „If the circuit breaker raises an event each time it changes state, this information can help monitor the health of the protected system component or **alert an administrator when a circuit breaker switches to the Open state.**“
(learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker)

A Polly dokumentáció ugyanezt kódszinten kényszeríti ki: minden állapotváltásra explicit callback (`OnClosed`, `OnOpened`, `OnHalfOpened`) és egy dedikált „Telemetry” alfejezet írja elő, hogy „the circuit breaker strategy reports the following telemetry events” — vagyis a könyvtár tervezésébe eleve be van építve, hogy az állapotváltás sosem maradhat nyomtalan.

**Következtetés (három egymástól független forrásból — Google, Microsoft/Azure, Polly/.NET közösség):** a bevett minta szerint a csendes (naplózatlan, riasztás nélküli) visszaállás/degradálás tilos; jelezni kell minden állapotváltáskor (napló + metrika + esemény), és a degradációs/fallback-logikának magának is kell legyen egy gyors, kézi kikapcsolója.

---

## 4. Timeout és késleltetési költségvetés: ajánlott időtúllépés, hedging, deadline propagation

### Timeout minden távoli híváson

Az AWS Builders' Library (Marc Brooker, „Timeouts, retries, and backoff with jitter”) alapelve:

> „To build resilient systems, we employ three essential tools: timeouts, retries, and backoff. […] To avoid this situation, clients set timeouts. **Timeouts are the maximum amount of time that a client waits for a request to complete.**“
> „[We recommend] to set a timeout on any remote call, and generally on any call across processes even on the same box. This includes both a connection timeout and a request timeout.“
(d1.awsstatic.com/builderslibrary/pdfs/timeouts-retries-and-backoff-with-jitter.pdf, szerző: Marc Brooker, AWS Senior Principal Engineer)

**Fontos: ez a forrás explicit NEM ad konkrét ezredmásodperc-számot** — a timeout hosszát szolgáltatás-specifikusnak mondja, és a hangsúlyt a „legyen timeout, backoff-fal és jitterrel kombinálva” elvre helyezi, nem egy univerzális számra.

### Deadline és deadline propagation

A Google SRE könyv „Latency and Deadlines” alfejezete definiálja a fogalmat és egy konkrét számpéldán mutatja be:

> „**RPC deadlines** define how long a request can wait before the frontend gives up […]“
> „**Deadline propagation.** Rather than inventing a deadline when sending RPCs to backends, servers should employ deadline propagation. […] For example, if server A selects a 30-second deadline, and processes the request for 7 seconds before sending an RPC to server B, the RPC from A to B will have a 23-second deadline. If server B takes 4 seconds […] the RPC from B to C will have a 19-second deadline, and so on.“
(sre.google/sre-book/addressing-cascading-failures/)

Ugyanezt, egymástól függetlenül, a gRPC hivatalos dokumentációja is leírja (nem Google SRE könyv, hanem a gRPC projekt saját doksija), gyakorlatilag azonos elvvel, saját szekvencia-diagrammal:

> „A deadline is used to specify a point in time past which a client is unwilling to wait for a response from a server. […] **Deadline Propagation.** Your server might need to call another server to produce a response. In these cases where your server also acts as a client you would want to honor the deadline set by the original client. Automatically propagating the deadline from an incoming RPC to an outgoing one is supported by some gRPC implementations. […] To address this gRPC converts the deadline to a timeout from which the already elapsed time is already deducted.“
(grpc.io/docs/guides/deadlines/, 2025-07-07)

Egy harmadik, valóban független (Microsoft) forrás, az ASP.NET Core gRPC dokumentáció, ugyanezt a mintát írja le .NET-specifikus API-val, és kimondottan figyelmeztet, hogy a kézi propagálás hibalehetőség:

> „**Propagating deadlines.** […] Manually propagating deadlines can be cumbersome. The deadline needs to be passed to every call, and it's easy to accidentally miss. An automatic solution is available with gRPC client factory. Specifying `EnableCallContextPropagation`: Automatically propagates the deadline and cancellation token to child calls.“
(learn.microsoft.com/en-us/aspnet/core/grpc/deadlines-cancellation, 2024-07-31)

**Három, egymástól független szervezettől (Google, gRPC/CNCF-projekt, Microsoft) származó forrás egyezik meg abban, hogy a deadline-t a hívási lánc tetején kell kijelölni, és automatikusan (nem kézzel) kell lefelé örökíteni, az eltelt idő levonásával.**

### Hedging

A jelenség kanonikus, elsődleges forrása Dean & Barroso „The Tail at Scale” cikke (Communications of the ACM, 2013 február, 56. kötet, 2. szám, 74–80. oldal):

> „**Hedged requests.** A simple way to curb latency variability is to issue the same request to multiple replicas and use the results from whichever replica responds first. We term such requests “hedged requests” because a client first sends one request to the replica believed to be the most appropriate, but then falls back on sending a secondary request after some brief delay. The client cancels remaining outstanding requests once the first result is received.“
> „One such approach is to **defer sending a secondary request until the first request has been outstanding for more than the 95th-percentile expected latency** for this class of requests. This approach limits the additional load to approximately 5% while substantially shortening the latency tail. […] sending a hedging request after a 10ms delay reduces the 99.9th-percentile latency for retrieving all 1,000 values from 1,800ms to 74ms while sending just 2% more requests.“
(cacm.acm.org/research/the-tail-at-scale/, Jeffrey Dean, Luiz André Barroso, 2013-02-01)

A gRPC hivatalos „Request Hedging” dokumentációja ezt gyakorlati konfigurációs mechanizmusként valósítja meg, explicit felső korláttal:

> „With hedging, a gRPC client sends multiple copies of the same request to different backends and uses the first response it receives. […] `maxAttempts`: maximum number of in-flight requests […] If the specified value is greater than `5`, gRPC uses a value of `5`.“
(grpc.io/docs/guides/request-hedging/, 2023-10-03)

**Összegzés a 4. ponthoz:** nincs egységes, elsődleges forrásból származó „ajánlott X ezredmásodperc” szám egy szinkron írási művelethez ágyazott külső döntési hívásra (ez pontosan a SQ06/Jev-forgatókönyv, és erre nincs közvetlen, kutatható elsődleges forrás — l. „Amire NINCS forrás”). Ami dokumentált: (a) legyen explicit timeout minden ilyen híváson; (b) a timeout/deadline-t a hívási lánc elején kell kijelölni és lefelé örökíteni, nem újra kitalálni minden lépésnél; (c) a hedging (második, párhuzamos próbahívás a p95 késleltetés tájékán) csökkenti a farok-késleltetést, de maga is terhelés-többletet és — túlterhelés esetén — lavinaveszélyt jelent, ezért gyakorlatban circuit breakerrel/adaptív küszöbbel szokás kombinálni (ezt maga a gRPC dokumentáció valósítja meg a `RetryThrottlingPolicy` mechanizmussal, ami a hedgelt kéréseket egy token-számláló alapján fojtja el túlterhelésnél).

---

## 5. Költségkeret: elfogyó keret kezelése LLM-gateway-eknél és felhős API-knál

### LiteLLM

A LiteLLM proxy kétrétegű mintát dokumentál: „soft budget” (csak riasztás, nem blokkol) és „max budget” (kemény blokkolás):

> „A **soft budget** is a spending threshold that triggers email notifications when exceeded, **but does not block requests**. This is different from a **hard budget** (`max_budget`), which rejects requests once the limit is reached.“
(docs.litellm.ai/docs/proxy/ui_team_soft_budget_alerts)

A kemény korlát elérésekor alapból hibát ad vissza (`budget_exceeded`, HTTP „429” kód a LiteLLM saját JSON-hibaformátumában), de opcionálisan konfigurálható automatikus, más modellre terelő tartalék-lánc is:

> „By default `model_max_budget` blocks requests once a key's spend on a model crosses its cap. `budget_fallbacks` lets you configure a per-model fallback chain on the key itself, so the request is **silently rerouted** to the first fallback that still has budget remaining. Spend is attributed to the fallback model, not the exhausted one.“
> „Once the developer burns $20 of Opus in a day, subsequent Opus requests silently reroute to Sonnet; if Sonnet is also tapped out, Haiku picks up.“
(docs.litellm.ai/docs/proxy/budget_fallbacks; docs.litellm.ai/docs/tutorials/claude_code_cut_costs)

Fontos, dokumentált él-eset: adatbázis nélküli (DB-less) telepítésen a globális/kulcs-szintű budget-ellenőrzés **fail-open** módon viselkedik:

> „`litellm_settings.max_budget` fails open there rather than erroring: the proxy's global spend is only loaded when a database client exists, and with no total to compare against, the global budget check is skipped and requests keep being served past the limit. **A warning is logged once at startup** when a budget is set with no database connected, but nothing blocks at request time.“
(docs.litellm.ai/docs/proxy/users)

### OpenRouter

Az OpenRouter explicit HTTP `402`-t definiál a keret-kimerülésre:

> „402: Your account or API key has insufficient credits. Add more credits and retry the request.“
> „`payment_required` | 402 | The account or API key has insufficient credits. Add credits and retry.“
(openrouter.ai/docs/api_reference/errors-and-debugging)

A modell-fallback (a `models` paraméter) 402-n kívüli hibákra (rate limit, downtime, moderáció) automatikusan másik modellre vált, de a dokumentáció explicit figyelmezet, hogy a 402-t egyik SDK sem próbálja automatikusan újra:

> „None of them retries a `402` on its own, so for the in-flight budget case catch the error, read `Retry-After`, and retry explicitly.“
> „To resolve errors: Add credits to bring your account balance above zero. […] **Monitor proactively.** Call `GET /api/v1/key` […] to track `limit_remaining` and usage before requests start failing.“
(openrouter.ai/docs/api_reference/limits)

### Portkey

A Portkey AI Gateway a fallback-et és a költségkeretet két külön, egymásba komponálható stratégiaként dokumentálja:

> „## Fallbacks — Fallback between providers and models for resilience […] ## Budget Limits — Set usage limits based on costs incurred or tokens used.“
(docs.portkey.ai/docs/product/ai-gateway)

> „Usage limits policies allow you to set maximum usage (cost or tokens) that can be consumed over a period. **When the limit is reached, requests will be blocked until the limit resets** (if `periodic_reset` is configured).“
(portkey-docs.mintlify.dev/docs/product/enterprise-offering/budget-policies)

A fallback stratégia külön, státuszkód-alapú triggerrel konfigurálható (`on_status_codes`), ami elvben a 402/429 kódokra is beköthető ugyanabban a mechanizmusban, mint az általános hibafallback.

### Felhős API-k / alkalmazás-szintű minta (AWS)

Az AWS API Gateway hivatalos dokumentációja egy kulcsfontosságú, a naiv elvárásnak ellentmondó figyelmeztetést ad: a rate-limit/kvóta **nem** megbízható költségkorlát:

> „Usage plan throttling and quotas are **not hard limits**, and are applied on a best-effort basis. In some cases, clients can exceed the quotas that you set. **Don't rely on usage plan quotas or throttling to control costs** or block access to an API. Consider using **AWS Budgets** to monitor costs and AWS WAF to manage API requests.“
(docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html)

A valódi, kemény („hard stop”) mechanizmust az AWS egy külön szolgáltatásban, az AWS Budgets Actions-ben adja:

> „You can use AWS Budgets to run an action on your behalf when a budget exceeds a certain cost or usage threshold. […] Your available actions include applying an IAM policy or a service control policy (SCP). […] For **How do you want to be alerted** when this action is run […]“
(docs.aws.amazon.com/cost-management/latest/userguide/budgets-controls.html, budgets-action-configure.html)

Az AWS Budgets Actions API explicit támogat automatikus (`ApprovalModel: 'AUTOMATIC'`) és kézi jóváhagyásos (`'MANUAL'`) leállítást is, tehát a „kapcsolóval kikapcsol” és a „keret elfogy → automatikusan leáll” elv az AWS saját, elsődleges dokumentációjában is explicit, konfigurálható kétféle módként jelenik meg.

**Összegzés az 5. ponthoz — egységes, három egymástól független gateway-nél (LiteLLM, OpenRouter, Portkey) és az AWS-nél is megjelenő minta:**
1. Két küszöb: puha (csak riasztás/napló) és kemény (blokkolás vagy más — olcsóbb/másik — célra terelés).
2. A kemény blokkolás tipikus HTTP-jelzése 402 (Payment Required, OpenRouter) vagy a gateway saját hibaformátuma (LiteLLM `budget_exceeded`).
3. A „keret elfogy → másik modellre/erőforrásra automatikus váltás” maga is egy fallback-lánc, amit a fő hibafallback mechanizmustól élesen el kell választani (LiteLLM külön `budget_fallbacks` objektumot használ, nem a router-szintű `fallbacks`-et).
4. A rate-limit/kvóta-mechanizmus **önmagában nem alkalmas** költségkorlátra (AWS explicit figyelmeztetése) — kell egy külön, a tényleges elköltött összeget mérő „budget guard”-szerű komponens.

---

## 6. Megfigyelhetőség: mit naplózzunk, mit mérjünk — árnyék-mód (shadow mode)

Az AWS SageMaker hivatalos „shadow testing” funkció-dokumentációja pontosan azt írja le, amit a felhasználó szeretne: az új modell fut, de a döntést a régi hozza, és a két oldalt utólag összevetik:

> „Amazon SageMaker now allows you to compare the performance of a new version of a model serving stack with the currently deployed version prior to a full production rollout using a deployment safety practice known as **shadow testing**. […] SageMaker takes care of deploying the new version alongside the current version serving production requests, routing a portion of requests to the shadow version. **You can then compare the performance of the two versions using metrics such as latency and error rate.** […] **Only the responses of the production variant are returned to the calling application.** You can choose to discard or log the responses of the shadow variant for offline comparison.“
(aws.amazon.com/blogs/machine-learning/minimize-the-production-impact-of-ml-model-updates-with-amazon-sagemaker-shadow-testing/, 2022-12-01)

Az AWS ehhez konkrét, mérendő metrikákat is megnevez: `ModelLatency`, `Invocation4xxErrors`, `InvocationsPerInstance`, `OverheadLatency`, `CPUUtilization`, `DiskUtilization` (mind az `AWS/SageMaker` CloudWatch névtérben).

Egy széles körben idézett, gyakorlati (nem gyártói) leírás a jelenség lényegét a legtömörebben adja vissza:

> „[…] systems that are in “shadow mode” are somewhere in between: when called, they do some work, **they log data about all of their decisions, and then return a default value as if they were off. All of the work is done, but the decision is not acted on.**“
> „You end up with […] a boat load of data that you can use to pragmatically answer the question: **what if this system had been on?** (because, technically, it was on!) without requiring Data Scientists to try and reverse engineer answers to this out of historical data.“
(nlathia.github.io/2020/07/Shadow-mode-deployments.html, Neal Lathia, 2020-07-04 — a szerző gyakorló adattudós/mérnök, ez a cikk gyakran hivatkozott MLOps-forrás, de **nem gyártói/szabvány dokumentáció**, ezért T2-ként jelölve.)

Ugyanez a szerző explicit meg is különbözteti a shadow mode-ot az A/B teszttől — ez direkt releváns a D-44 döntéshez (miért nem A/B, hanem árnyék-teszt egy döntés-modellnél):

> „shadow mode allows you to know whether a system **inherently works** before you go ahead and experiment with whether it impacts a business metric.“ […] „There are other scenarios where regulatory guidance may impede running A/B tests (I imagine this is the case with **credit scoring models**), or where you have low-volume/high-impact traffic (as is the case in **fraud monitoring**) where you may not want to send a percentage of traffic down a path that you don't know anything about.“

**Mit kell naplózni/mérni (az AWS SageMaker és a gyakorlati irodalom közös metszete):**
- **Egyezés/eltérés (agreement/disagreement rate):** hányszor hozott volna a külső modell más döntést, mint a jelenlegi módszer, kategóriánként lebontva.
- **Késleltetés:** a külső hívás saját latenciája (percentilisekkel, pl. p50/p95/p99), különösen azért, mert ez közvetlenül a 4. pontban tárgyalt timeout-budget bemenete.
- **Hibaarány:** a külső hívás sikertelenségi/timeout-aránya saját magában (ez a circuit breaker küszöbének bemenete is).
- **Költség:** hívásonkénti/token-alapú költség, összesítve — ez köti össze a shadow móddal mért „megéri-e” kérdést az 5. pont költségkeret-mechanizmusával.
- Az AWS explicit kimondja, hogy a shadow-variánsok válaszát „choose to discard or log […] for offline comparison” — azaz a naplózás/eldobás a rendszer tervezésének explicit, dokumentált opciója, nem mellékhatás.

---

## Ellentmondások

1. **A circuit breaker küszöbszámai könyvtáranként eltérnek, nincs egységes „ipari szabvány” szám.** Polly alapértelmezett hibaaránya 10% (`FailureRatio = 0.1`, 30 másodperces mintavételi ablakban, min. 100 hívással), míg a Resilience4j alapértelmezett hibaaránya 50% (`failureRateThreshold = 50`, szintén min. 100 hívásos ablakban). Ez nem hiba, hanem a könyvtárak tudatosan eltérő alapbeállítása — mindkettő explicit „ez az alapérték, állítsd a saját rendszeredhez” filozófiát követ, de a két szám (10% vs. 50%) önmagában félrevezető lenne, ha valaki az egyiket „az” iparági standardnak tekintené.
2. **A „félig nyitott” (half-open) állapot viselkedése architekturálisan eltér Polly és Resilience4j között.** A Resilience4j egy külön, konfigurálható méretű mintavételi ablakot használ a fél-nyitott állapotban is (`permittedNumberOfCallsInHalfOpenState`, alapból 10 hívás, és ezek hibaaránya dönt), míg a Polly dokumentációja szerint „If the first action after the break duration period results in a handled exception, the circuit will break again […]; if no exception is thrown, the circuit will reset” — azaz Polly-nál **egyetlen próbahívás** dönt teljes egészében a vissza- vagy tovább-nyitásról, nincs külön fél-nyitott mintavételi ablak. Ez tervezési döntésnél számít: a két könyvtár nem csereszabatos „ugyanaz a minta, más szintaxis” szinten.
3. **Feszültség a „soha ne legyen néma visszaállás” elv (Google SRE, Azure, Polly) és az LLM-gateway-ek „silent” fallback-gyakorlata (LiteLLM) között.** A LiteLLM saját dokumentációja szó szerint a „silently rerouted” kifejezést használja a költségkeret-alapú fallback-re: a hívó alkalmazás felé **nem jelenik meg hiba**, amikor egy olcsóbb modellre terelődik a kérés. Ez technikailag nem „néma” abban az értelemben, hogy a rendszer oldalán naplózásra kerül (a `/spend/logs` végpont pontosan attribuálja az új modellhez a költést), de **a hívó alkalmazás/felhasználó szemszögéből** igen — nincs kivétel, nincs figyelmeztető válaszfejléc. Ez ellentétben áll azzal az elvvel, amit a Google SRE könyv és az Azure Architecture Center a circuit breaker/degradáció állapotváltásaira megkövetel (esemény + riasztás minden váltáskor). A két terület (általános rezíliencia-minták vs. LLM-gateway gyakorlat) tehát nem old fel egyértelműen: a gateway-ek a „silent” fallback-et tudatos termék-döntésként kínálják (mert a cél a fejlesztői élmény zavartalansága), miközben az SRE-irodalom kifejezetten az átláthatóságot követeli meg üzemeltetői szemszögből.
4. **Az `opossum` dokumentáció-változatai eltérő Node.js-verzió-követelményt adnak meg** (a 8.1.3-as dokumentációs pillanatkép „Node.js >= 16”-ot, a jelenlegi GitHub főág „Node.js >= 22”-t ír elő) — ez nem tartalmi ellentmondás, hanem a dokumentáció verziózásának természetes következménye, de érdemes tudni, hogy a pontos minimális Node-verzió a ténylegesen telepített `opossum`-verziótól függ, nem egy változatlan konstans.

## Amire NINCS forrás

- **Konkrét, elsődleges forrásból származó ezredmásodperc-ajánlás** egy szinkron írási művelet közben elhelyezett, külső döntési-modell hívásra (ez pontosan a SQ06/Jev-forgatókönyv: „mennyi timeout legyen egy new-note-írás közbeni külső modell-hívásra”). Az AWS Builders' Library és a Google SRE könyv is kifejezetten elutasítja az univerzális szám megadását, és szolgáltatás-specifikusnak mondja a helyes timeout-értéket — konkrét számot egyik elsődleges forrásban sem találtam erre a use case-re.
- **Egy formálisan elnevezett, Fowler/Azure/AWS-szintű „budget guard” vagy „cost circuit breaker” minta** mint önálló, katalogizált tervezési minta. A koncepció a gyakorlatban létezik és jól dokumentált (LiteLLM `budget_fallbacks`, OpenRouter kulcsszintű `limit_remaining`, Portkey usage-limit policy, AWS Budgets Actions), de nem találtam olyan elsődleges forrást (Azure Architecture Center katalógus, AWS Well-Architected minta-lista, vagy Fowler-cikk), amely ezt önálló, névvel ellátott mintaként (a Circuit Breaker vagy Feature Toggle mintájához hasonló önálló szócikként) katalogizálná.
- **Polly saját dokumentációja nem közöl explicit állítást a könyvtár összes függőségének számáról** (a pollydocs.org oldalain nem találtam „N Dependencies” vagy azzal egyenértékű nyilatkozatot ebben a kutatási körben) — így a Resilience4j/opossum függőség-adatával ellentétben Pollyhoz nem tudok forrással alátámasztott, konkrét függőségszámot megadni.
- **Resilience4j hivatalos, prózai (nem forráskód-/POM-alapú) kijelentése a „minimális függőség” elvről** — a `slf4j-api`-n kívüli függetlenség ténye a Maven Central POM-fájlból és a GitHub release-jegyzetekből (Vavr eltávolítása) derül ki, nem egy dedikált „miért ilyen kevés a függőségünk” dokumentációs oldalból; ha kell egy közvetlen gyártói idézet erre, azt ebben a körben nem találtam.
- **Konkrét, elsődleges forrásból származó minimális mintaszám vagy időtartam „árnyék-módra”** egy alacsony volumenű (pl. napi néhány tucat jegyzetírásos) belső rendszerhez — az AWS SageMaker és a gyakorlati irodalom (pl. a kutatás során talált, de itt nem idézett harmadik féltől származó „shadow deployment” útmutatók) nagy volumenű (napi több száz–több ezer kérés) rendszerekre adnak mintaszám-ajánlásokat; egy alacsony volumenű, belső memória-rendszerre vonatkozó, elsődleges forrásból származó konkrét ajánlást nem találtam.

## Meglátogatott és felderített linkek

| Cím | URL | Tier | Eszköz | Megjegyzés |
|---|---|---|---|---|
| Circuit Breaker Pattern — Azure Architecture Center | https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker | T1 | Exa web_search_exa | Hivatalos Microsoft/Azure minta-katalógus, állapotgép-leírás, `ms.date: 02/05/2025` |
| docs/patterns/circuit-breaker.md (GitHub, mspnp/architecture-center) | https://github.com/mspnp/architecture-center/blob/master/docs/patterns/circuit-breaker.md | T1 | Exa web_search_exa | Ugyanaz a tartalom forrás-repóban, megerősíti a fenti szöveget |
| Circuit Breaker pattern (korábbi, „previous-versions” archív oldal) | https://learn.microsoft.com/en-us/previous-versions/msp-n-p/dn589784(v=pandp.10) | T1 | Exa web_search_exa | Archív Microsoft patterns & practices verzió, ugyanazt az elvet írja le hosszabban |
| Circuit breaker design pattern — Wikipédia | https://en.wikipedia.org/wiki/Circuit_breaker_design_pattern | T2 | Exa web_search_exa | Tercier, de megerősíti az állapotokat |
| Circuit Breaker — Martin Fowler bliki | https://martinfowler.com/bliki/CircuitBreaker.html | T1 | Exa web_search_exa | A minta kanonikus, elsődleges leírása (2014-03-06) |
| CircuitBreaker — resilience4j (jelenlegi doksi) | https://resilience4j.readme.io/docs/circuitbreaker | T1 | Exa web_search_exa | Hivatalos könyvtár-dokumentáció, 6 állapot, küszöbök |
| CircuitBreaker — resilience4j v0.17.0 (archív) | https://resilience4j.readme.io/v0.17.0/docs/circuitbreaker | T1 | Exa web_search_exa | Korábbi verzió, csak 2 speciális állapot — a fejlődés összehasonlítására |
| CircuitBreakerConfig.java — resilience4j GitHub | https://github.com/resilience4j/resilience4j/blob/master/resilience4j-circuitbreaker/src/main/java/io/github/resilience4j/circuitbreaker/CircuitBreakerConfig.java | T1 | Exa web_search_exa | Forráskód, alapértelmezett küszöbszámok |
| README.adoc — resilience4j GitHub | https://github.com/resilience4j/resilience4j/blob/master/README.adoc | T1 | Exa web_search_exa | Projekt-áttekintés, ajánlott gyakorlat (külön breaker szolgáltatásonként) |
| io.github.resilience4j:resilience4j-core — Maven Central | https://central.sonatype.com/artifact/io.github.resilience4j/resilience4j-core | T1 | Exa web_search_exa | POM-fájl, egyetlen futásidejű függőség (slf4j-api) |
| Releases · resilience4j/resilience4j | https://github.com/resilience4j/resilience4j/releases | T1 | Exa web_search_exa | Vavr-függőség eltávolítása (v2.0.0) |
| Circuit breaker resilience strategy — Polly | https://www.pollydocs.org/strategies/circuit-breaker | T1 | Exa web_search_exa | Hivatalos Polly v8 dokumentáció, alapértékek, állapotok |
| CircuitBreakerStrategyOptions — Polly API doksi | https://www.pollydocs.org/api/Polly.CircuitBreaker.CircuitBreakerStrategyOptions-1.html | T1 | Exa web_search_exa | API-referencia, `FailureRatio`, `BreakDuration` stb. |
| Implementing the Circuit Breaker pattern — .NET (Microsoft Learn) | https://learn.microsoft.com/en-us/dotnet/architecture/microservices/implement-resilient-applications/implement-circuit-breaker-pattern | T1 | Exa web_search_exa | Microsoft hivatalos útmutató Polly+IHttpClientFactory kombinációra |
| nodeshift/opossum — GitHub | https://github.com/nodeshift/opossum | T1 | Exa web_search_exa | Hivatalos repó, licenc, letöltésszám, engine-követelmény |
| opossum — Nodeshift dokumentáció | https://nodeshift.dev/opossum/ | T1 | Exa web_search_exa | Hivatalos API-doksi (8.1.3-as pillanatkép) |
| opossum — npm regisztráció (registry.npmjs.org) | https://registry.npmjs.org/opossum | T1 | Exa web_search_exa | „0 Dependencies”, csomagméret |
| opossum — npmjs.com csomagoldal | https://www.npmjs.com/package/opossum | T1 | Exa web_search_exa | Verzió 10.0.0, dev-függőségek listája (build-idejű, nem futásidejű) |
| README.md — nodeshift/opossum (GitHub) | https://github.com/nodeshift/opossum/blob/main/README.md | T1 | Exa web_search_exa | Aktuális README, „Node.js >= 22” |
| opossum — DepScope csomag-egészség oldal | https://depscope.dev/pkg/npm/opossum | T2 | Exa web_search_exa | Független megerősítés: „0 deps” |
| Feature Toggles (aka Feature Flags) — Martin Fowler / Pete Hodgson | https://martinfowler.com/articles/feature-toggles.html | T1 | Exa web_search_exa | „Kill Switch” kategória, ops toggle, canary release |
| Feature Flag — Martin Fowler bliki | https://www.martinfowler.com/bliki/FeatureFlag.html | T1 | Exa web_search_exa | Toggle-kategóriák, futásidejű vs. build-idejű |
| Canary Release — Martin Fowler bliki | https://martinfowler.com/bliki/CanaryRelease.html | T1 | Exa web_search_exa | Kapcsolódó minta, kontextusnak |
| Dark Launching — Martin Fowler bliki | https://martinfowler.com/bliki/DarkLaunching.html | T1 | Exa web_search_exa | Kapcsolódó minta (feature flag mögötti néma bevezetés) |
| OPS06-BP03 Employ safe deployment strategies — AWS Well-Architected | https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_mit_deploy_risks_deploy_mgmt_sys.html | T1 | Exa web_search_exa | Feature flag mint biztonságos kiadási stratégia |
| Implement change — AWS Well-Architected Reliability Pillar | https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/implement-change.html | T1 | Exa web_search_exa | „turn the feature back off without rolling back” idézet forrása |
| OPS06-BP01 Plan for unsuccessful changes — AWS Well-Architected | https://docs.aws.amazon.com/wellarchitected/latest/framework/ops_mit_deploy_risks_plan_for_unsucessful_changes.html | T1 | Exa web_search_exa | Feature flag mint helyreállítási stratégia |
| DL.ADS.4 Implement Incremental Feature Release Techniques — AWS DevOps Guidance | https://docs.aws.amazon.com/wellarchitected/latest/devops-guidance/dl.ads.4-implement-incremental-feature-release-techniques.html | T1 | Exa web_search_exa | Dark launch + feature flag összefüggés |
| OPS06-BP04 Automate testing and rollback — AWS Well-Architected | https://docs.aws.amazon.com/wellarchitected/latest/framework/ops_mit_deploy_risks_auto_testing_and_rollback.html | T1 | Exa web_search_exa | Feature-flag tesztelés, automatikus rollback |
| Cascading Failures: Reducing System Outage — Google SRE könyv, 22. fejezet | https://sre.google/sre-book/addressing-cascading-failures/ | T1 | Exa web_search_exa | Load shedding, graceful degradation, deadline propagation, hedged/cancellation — kulcsfejezet |
| 22. Addressing Cascading Failures — O'Reilly (SRE könyv) | https://www.oreilly.com/library/view/site-reliability-engineering/9781491929117/ch22.html | T1 | Exa web_search_exa | Ugyanaz a fejezet, kiadói oldal, tartalomjegyzék megerősítése |
| Google: Addressing Cascading Failures — High Scalability | https://highscalability.com/google-addressing-cascading-failures/ | T2 | Exa web_search_exa | Kivonat/összefoglaló, szó szerinti idézetekkel a könyvből |
| Google SRE: Production Services Best Practices | https://sre.google/sre-book/service-best-practices/ | T1 | Exa web_search_exa | Graceful degradation + retry/backoff kapcsolódó ajánlások |
| Google SRE - Managing Load (Workbook) | https://sre.google/workbook/managing-load/ | T1 | Exa web_search_exa | RPC deadline gyakorlati ajánlás |
| Timeouts, retries, and backoff with jitter (PDF) — AWS Builders' Library | https://d1.awsstatic.com/builderslibrary/pdfs/timeouts-retries-and-backoff-with-jitter.pdf | T1 | Exa web_search_exa | Marc Brooker, timeout/retry/backoff alapelvek |
| Timeouts, retries, and backoff with jitter — AWS Builder Center | https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter | T1 | Exa web_search_exa | Ugyanazon cikk másik hivatalos elérése |
| Exponential Backoff And Jitter — AWS Architecture Blog | https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/ | T1 | Exa web_search_exa | Marc Brooker, 2015-03-04, jitter-stratégiák |
| Making retries safe with idempotent APIs — AWS Builders' Library | https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/ | T1 | Exa web_search_exa | Kapcsolódó, idempotencia |
| Marc Brooker — AWS Builders' Library szerzői oldal | https://aws.amazon.com/builders-library/authors/marc-brooker/ | T1 | Exa web_search_exa | Szerző hitelesítése |
| Request Hedging — gRPC hivatalos dokumentáció | https://grpc.io/docs/guides/request-hedging/ | T1 | Exa web_search_exa | Hedging konfiguráció, `maxAttempts`, throttling |
| content/en/docs/guides/request-hedging.md — grpc/grpc.io GitHub | https://github.com/grpc/grpc.io/blob/main/content/en/docs/guides/request-hedging.md | T1 | Exa web_search_exa | Ugyanaz forrás-repóban |
| Deadlines — gRPC hivatalos dokumentáció | https://grpc.io/docs/guides/deadlines/ | T1 | Exa web_search_exa | Deadline propagation önálló gRPC-doksin, 2025-07-07 |
| content/en/docs/guides/deadlines.md — grpc/grpc.io GitHub | https://github.com/grpc/grpc.io/blob/main/content/en/docs/guides/deadlines.md | T1 | Exa web_search_exa | Ugyanaz forrás-repóban |
| gRPC and Deadlines — gRPC blog | https://grpc.io/blog/deadlines/ | T1 | Exa web_search_exa | 2018-02-26, gyakorlati tanácsok kliens/szerver deadline-ra |
| Core concepts, architecture and lifecycle — gRPC | https://grpc.io/docs/what-is-grpc/core-concepts/ | T1 | Exa web_search_exa | Deadline/timeout fogalmi áttekintés |
| Reliable gRPC services with deadlines and cancellation — Microsoft Learn | https://learn.microsoft.com/en-us/aspnet/core/grpc/deadlines-cancellation | T1 | Exa web_search_exa | Független (Microsoft) megerősítés a deadline-propagálásra |
| The Tail at Scale — Communications of the ACM (Dean & Barroso) | https://cacm.acm.org/research/the-tail-at-scale/ | T1 | Exa web_search_exa | Elsődleges tudományos közlemény, hedged requests definíció és számpélda |
| The tail at scale (PDF, Duke egyetem tükör) | https://courses.cs.duke.edu/cps296.4/fall13/838-CloudPapers/dean_longtail.pdf | T1 | Exa web_search_exa | Ugyanaz a cikk, egyetemi tükörpéldány |
| The Tail at Scale — Google Research absztrakt | https://research.google/pubs/the-tail-at-scale/ | T1 | Exa web_search_exa | Szerzői/kiadói hivatkozás, absztrakt |
| The tail at scale — DOI/ACM Digital Library rekord | https://doi.org/10.1145/2408776.2408794 | T1 | Exa web_search_exa | Formális publikációs rekord, idézettségi szám |
| Budget Fallbacks — LiteLLM docs | https://docs.litellm.ai/docs/proxy/budget_fallbacks | T1 | Exa web_search_exa | „silently rerouted”, per-modell fallback-lánc |
| Budget Routing (Provider budgets) — LiteLLM docs | https://docs.litellm.ai/docs/proxy/provider_budget_routing | T1 | Exa web_search_exa | Provider-szintű időszakos keret, Redis-alapú követés |
| [New] Fallback Management Endpoints — LiteLLM docs | https://docs.litellm.ai/docs/proxy/fallback_management | T1 | Exa web_search_exa | Router-szintű vs. budget-fallback megkülönböztetés |
| Budgets, Rate Limits — LiteLLM docs | https://docs.litellm.ai/docs/proxy/users | T1 | Exa web_search_exa | Fail-open viselkedés DB nélkül, `fail_closed_enforcement` |
| Team Soft Budget Alerts — LiteLLM docs | https://docs.litellm.ai/docs/proxy/ui_team_soft_budget_alerts | T1 | Exa web_search_exa | Soft vs. hard budget megkülönböztetés, e-mail riasztás |
| Claude Code - Cut Costs — LiteLLM docs | https://docs.litellm.ai/docs/tutorials/claude_code_cut_costs | T1 | Exa web_search_exa | Gyakorlati budget-fallback-lánc példa |
| Model Fallbacks — OpenRouter docs | https://openrouter.ai/docs/guides/routing/model-fallbacks | T1 | Exa web_search_exa | Automatikus modell-fallback hibakódokra |
| API Error Handling and Debugging — OpenRouter docs | https://openrouter.ai/docs/api_reference/errors-and-debugging | T1 | Exa web_search_exa | 402/429/503 kódok, `Retry-After` |
| PaymentRequiredResponseError — OpenRouter TS SDK docs | https://openrouter.ai/docs/agent-sdk/typescript/errors/paymentrequiredresponseerror | T1 | Exa web_search_exa | 402-hiba SDK-szintű reprezentációja |
| API Credit & Rate Limits — OpenRouter docs | https://openrouter.ai/docs/api_reference/limits | T1 | Exa web_search_exa | 402-kezelési ajánlások, proaktív monitorozás |
| Provider Routing — OpenRouter docs | https://openrouter.ai/docs/guides/routing/provider-selection | T1 | Exa web_search_exa | Provider-szintű fallback-részletek |
| OpenRouter FAQ | https://openrouter.ai/docs/faq | T1 | Exa web_search_exa | Fallback-mechanizmus általános leírása |
| AI Gateway — Portkey docs | https://docs.portkey.ai/docs/product/ai-gateway | T1 | Exa web_search_exa | Fallback/Conditional Routing/Budget Limits áttekintés |
| Conditional Routing — Portkey docs | https://portkey.ai/docs/product/ai-gateway/conditional-routing | T1 | Exa web_search_exa | Feltételes útválasztás, kompozitálhatóság |
| Fallbacks — Portkey docs | https://portkey.ai/docs/product/ai-gateway/fallbacks | T1 | Exa web_search_exa | Sorrendezett fallback-lista, kompozitálhatóság |
| Usage & Rate Limit Policies — Portkey Enterprise docs | https://portkey-docs.mintlify.dev/docs/product/enterprise-offering/budget-policies | T1 | Exa web_search_exa | Kemény blokkolás keret elérésekor, periodikus reset |
| Config Object — Portkey API Reference | https://portkey.ai/docs/api-reference/inference-api/config-object | T1 | Exa web_search_exa | `on_status_codes` alapú fallback-trigger sémája |
| Usage plans and API keys for REST APIs — AWS API Gateway docs | https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html | T1 | Exa web_search_exa | „Don't rely on usage plan quotas […] to control costs” idézet forrása |
| Throttle requests to your REST APIs — AWS API Gateway docs | https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html | T1 | Exa web_search_exa | Token bucket algoritmus, 429-es válasz |
| UsagePlan — AWS API Gateway API Reference | https://docs.aws.amazon.com/apigateway/latest/api/API_UsagePlan.html | T1 | Exa web_search_exa | Ugyanaz a figyelmeztetés API-referencia szinten |
| Amazon API Gateway quotas | https://docs.aws.amazon.com/apigateway/latest/developerguide/limits.html | T1 | Exa web_search_exa | Konkrét alapértelmezett kvótaszámok |
| Maintain a usage plan for REST APIs — AWS API Gateway docs | https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-usage-plan-manage-usage.html | T1 | Exa web_search_exa | Kvóta-monitorozás gyakorlati lépései |
| Configuring a budget action — AWS Cost Management docs | https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-action-configure.html | T1 | Exa web_search_exa | Automatikus/kézi jóváhagyású költségvetési akció beállítása |
| Configuring budget actions — AWS Cost Management docs | https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-controls.html | T1 | Exa web_search_exa | IAM/SCP-alapú kemény leállítás leírása |
| create_budget_action — Boto3 docs | https://docs.aws.amazon.com/boto3/latest/reference/services/budgets/client/create_budget_action.html | T1 | Exa web_search_exa | API-szintű `ApprovalModel: AUTOMATIC/MANUAL` |
| CreateBudgetAction — AWS Cost Management API Reference | https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_budgets_CreateBudgetAction.html | T1 | Exa web_search_exa | Formális API-séma |
| UpdateBudgetAction — AWS Cost Management API Reference | https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_budgets_UpdateBudgetAction.html | T1 | Exa web_search_exa | Kiegészítő API-séma |
| Minimize the production impact of ML model updates with Amazon SageMaker shadow testing — AWS ML Blog | https://aws.amazon.com/blogs/machine-learning/minimize-the-production-impact-of-ml-model-updates-with-amazon-sagemaker-shadow-testing/ | T1 | Exa web_search_exa | Hivatalos AWS shadow testing funkció-leírás, 2022-12-01, konkrét metrikák |
| Shadow mode deployments — Neal Lathia | https://nlathia.github.io/2020/07/Shadow-mode-deployments.html | T2 | Exa web_search_exa | Gyakran idézett, gyakorló szakértői blogbejegyzés, shadow vs. A/B különbség |
| Shadow Deployment for Safe Model Releases — EngineersOfAI | https://engineersofai.com/docs/ai-systems/model-serving/shadow-deployment | T2/T3 | Exa web_search_exa | Gyakorlati (nem gyártói) mélyebb technikai leírás, graduation-kritériumok — csak háttér-kontextusnak, nem idézve a fő szövegben |
| Shadow Deployment: How It Works, And Key Considerations — Portainer blog | https://www.portainer.io/blog/shadow-deployment | T3 | Exa web_search_exa | Termékgyártói (Portainer) marketing-közeli blog, csak háttér-kontextusnak |
| Shadow Mode Deployment for ML Model Testing — ML Journey | https://mljourney.com/shadow-mode-deployment-for-ml-model-testing/ | T3 | Exa web_search_exa | Másodlagos összefoglaló blog, csak háttér-kontextusnak |

---

# ELL01 — A Jev API-, ár- és szállítói állításainak ellenőrzése

*Módszer: kizárólag Exa (`web_search_exa`, `web_fetch_exa`) eszközzel, elsődleges (typesafe.ai, docs.typesafe.ai, status.typesafe.ai) forrásokat közvetlenül lekérve, majd minden állításhoz legalább egy, TypeSafe-től független második forrással (sajtó, vagy egy gateway saját hivatalos doksija). Alügynök-indítás (deep-web-research teljes pipeline) nem történt, ez egy önálló, Exa-only, degradált módú kör. Az előző kör (SQ00/SQ01/SQ03) idézeteit nem vettem át ellenőrzés nélkül — minden idézett oldalt magam is közvetlenül lekértem újra.*

## Verdikt-összefoglaló

| # | Állítás | Verdikt | Egy mondat |
|---|---|---|---|
| 1 | Jev = TypeSafe AI modell, bejelentve 2026-09-15; `jev-1.13.0`; nem generál szöveget; Choice(max. 255)/Score(2–10)/Noul | RÉSZBEN | A modellnév, a szöveg-nem-generálás és a három kérdéstípus pontos limitjei elsődleges forrásból szó szerint igazolhatók, de maga a TypeSafe blog saját dátumbélyege „Sep 14, 2026"-ot mutat, míg a cég saját sajtóközleménye és minden független sajtó Sep 15-öt ír. |
| 2 | Nincs temperature/seed; „stabil, de nem tökéletesen determinisztikus" (~0,0102 szórás) | IGAZOLVA | A hivatalos „Self-consistency: nouls" cookbook oldal szó szerint közli a 0,0102-es átlagos szórást; ez azonban TypeSafe saját, nem harmadik fél által megismételt mérése. |
| 3 | Kontextus: 64k/kérés, 32k state+leghosszabb kérdés — vs. gateway-ek 32k-ja | IGAZOLVA | A TypeSafe hivatalos Models oldala 64k/32k-t ír, míg az OpenRouter és a Cloudflare saját, hivatalos modell-oldalai kizárólag 32k-s kontextusablakot hirdetnek ugyanarra a modellre. |
| 4 | Korlátok: 250 000 tok/mp, 1200 kérés/perc; hibakódok 401/422/429/529 | IGAZOLVA | Mindkét szám és a négy hibakód szó szerint szerepel a hivatalos dokumentációban, egy független fejlesztői útmutató (apidog.com) pedig szó szerint ugyanezt a táblázatot reprodukálja saját teszteléssel. |
| 5 | 2026-09-20: megszűnt a várólista („available to everyone. No waitlist.") | IGAZOLVA | Legalább három, egymástól független hírforrás idézi ugyanazt a 2026-09-20-i hivatalos TypeSafe-posztot, egybehangzóan; magát a posztot az X-en közvetlenül az Exa nem érte el. |
| 6 | Van státuszoldal (~99,858% uptime), nincs SLA; MCA kizárja a megszakítás-mentességet | IGAZOLVA | A hivatalos status.typesafe.ai oldalon pontosan 99,858% szerepel az api.typesafe.ai-ra, és az MCA 9.3 szakasza szó szerint kizárja a megszakítás-mentesség garanciáját — de az Exa által lekért oldal-pillanatkép „Sep 16, 2026" dátumú, tehát nem feltétlenül friss, mai állapot. |
| 7 | Ár: $0,042/millió bemeneti token, kimenet ingyenes | IGAZOLVA | A hivatalos launch-blog szó szerint ezt írja, és az OpenRouter független, saját ártáblázata pontosan ugyanezt az árat listázza. |
| 8 | Kredit-alapú elszámolás (MCA 8.2); kredit nem visszatéríthető; nincs dokumentált „elfogyott a kredit" hibakód | IGAZOLVA | Az MCA 8.2 szakasza szó szerint kredit-rendszert ír le, nem visszatérítendő krediteket, és a hivatalos hibakód-tábla valóban nem tartalmaz 402-t vagy hasonlót. |
| 9 | OpenRouter 402 + `GET /credits`; Vercel 402 `quota_for_entity_exceeded`; Cloudflare spend limit 429 | IGAZOLVA | Mindhárom mechanizmust közvetlenül, az adott gateway saját hivatalos dokumentációjából, szó szerinti idézettel sikerült megerősíteni. |
| 10 | Felelősségkorlátozás $50; a szolgáltatás bármikor felfüggeszthető | RÉSZBEN/PONTOSÍTANDÓ | A $50-os kemény plafon és a „bármikor, bármely okból" felfüggesztés szó szerint csak az ingyenes „preview" ToS-ben szerepel; a fizetős, kredites API-szerződés (MCA) felelősségi plafonja ehelyett „a 12 havi kifizetés VAGY $50 közül a nagyobbik", és a felfüggesztés ott 4 konkrét, felsorolt okra korlátozódik. |
| 11 | A cég 2024-ben alakult, ~40 millió dolláros seed, DCVC vezetésével | IGAZOLVA | A hivatalos BusinessWire sajtóközlemény és legalább két független lap (The Register, the-decoder) egybehangzóan, szó szerint megerősíti mindhárom számot. |

## Állításonként

### 1. Azonosítás, dátum, kérdéstípusok — RÉSZBEN

A TypeSafe hivatalos blogja saját, látható dátumbélyeggel: **„Sep 14, 2026"**, *„Our first public model is Jev, available today in early access."* (https://typesafe.ai/blog/introducing-system-one-models-and-jev, közvetlenül lekérve)

Ezzel szemben a cég saját, hivatalos BusinessWire sajtóközleménye: *„Sep 15, 2026 3:00 PM Eastern Daylight Time … SAN FRANCISCO–(BUSINESS WIRE)–TypeSafe AI … today emerged from stealth with $40 million in seed funding led by DCVC."* (https://www.businesswire.com/news/home/20260915525333/en/, T1)

Második, TypeSafe-től teljesen független forrás ugyanerre a Sep 15-i dátumra: The Register, publikálva „Published wed 16 Sep 2026 // 02:35 UTC": *„TypeSafe AI, a startup bestowed with $40 million in funding, on Tuesday declared itself a maker of frontier models with the release of Jev…"* (Tuesday = szept. 15; https://www.theregister.com/ai-and-ml/2026/09/16/typesafe-ai-debuts-model-for-machines-that-plays-doom/5296711, T2). A the-decoder.com cikke is „Sep 16, 2026" dátumozású, a bejelentést a megelőző napra utalva.

Modellnév — hivatalos Models oldal, közvetlenül lekérve: *„| Jev 1.13 | `jev-1.13.0` |"* (https://docs.typesafe.ai/models).

Nem generál szöveget — hivatalos blog: *„While Jev gives up string generation, it's optimized for structured outputs and can't hallucinate."* / *„Think of Jev as a frontier-intelligence function call: unstructured state in, typed probabilistic decisions out."* Második, független forrás: TechCrunch (Tim Fernholz, 2026-09-18): *„the company released a new transformer-based model, Jev, that is not a large language model (LLM). It doesn't output text, but instead produces probabilities, or what the company calls 'calibrated decisions.'"* (https://techcrunch.com/2026/09/18/a-new-kind-of-ai-model-from-a-chatgpt-inventor-is-thrilling-developers/, T1 újságírás)

Kérdéstípusok, limitek — hivatalos API-referencia, közvetlenül lekérve (https://docs.typesafe.ai/api): *„Choice … You can have a maximum of 255 options per Choice."* / *„Score … A Score should have at least two levels; the API accepts up to 10."* / Noul: yes/no kérdés, valószínűséggel. Második, független megerősítés: a Cloudflare saját hivatalos Jev-modell oldala ugyanezt a három típust, ugyanazokkal a mezőnevekkel írja le: *„It evaluates one state against typed Noul, Choice, and Score questions and returns calibrated answers with probabilities and confidence."* (https://developers.cloudflare.com/ai/models/typesafe/jev/, T2, hivatalos gateway-doksi).

**Következtetés**: a modellnév, a „nem generál szöveget" jelleg és a három kérdéstípus pontos limitje (255/2–10) elsődleges forrásból, szó szerint és két független forrással is alátámasztható — IGAZOLVA. Az egyetlen valódi eltérés a bejelentés napja: a TypeSafe **saját** blogoldala Sep 14-et mutat, miközben a cég **saját** sajtóközleménye és a teljes független sajtó (legalább két, egymástól is független lap) Sep 15-öt ír — ez egy dokumentált, fel nem oldott, egynapos belső ellentmondás magán a TypeSafe anyagain belül, ezért a teljes állítás összességében RÉSZBEN.

### 2. Determinizmus — IGAZOLVA

Hivatalos API-referencia (state/model/questions mezők) nem sorol fel `temperature` vagy `seed` mezőt (https://docs.typesafe.ai/api, közvetlenül ellenőrizve).

A pontos hely, ahol a „stabil, de nem tökéletesen determinisztikus" állítás és a szórásszám áll: a hivatalos „Self-consistency: nouls" cookbook, közvetlenül lekérve: *„TypeSafe's mean per-question probability standard deviation is `0.0102`, below all LLM probability conditions here. Its `covered` answers span `0.43` to `0.53`, crossing a `0.5` decision threshold."* (https://docs.typesafe.ai/cookbooks/consistency_noul_cookbook)

**Fontos árnyalat**: ez a mérés a TypeSafe **saját** kiadású, hivatalos cookbookjában szerepel (`jev-latest`, mintavétel 2026-09-11-én, saját tesztkörnyezetben, összevetve a Claude Haiku 4.5/GPT-5.4-mini/GPT-5.5/Claude Opus 4.8 modellekkel) — független, harmadik fél által megismételt validációját ennek a konkrét számnak nem találtam ebben a körben sem.

### 3. Kontextusméret vs. gateway-ek — IGAZOLVA

Hivatalos Models oldal, közvetlenül lekérve: *„Context length: 64k tokens per request; 32k tokens for `state` plus the longest question."* (https://docs.typesafe.ai/models)

OpenRouter saját, hivatalos modell-oldala, közvetlenül lekérve: *„Context 32K"* (https://openrouter.ai/typesafe/jev-1.13)

Cloudflare saját, hivatalos modell-oldala, közvetlenül lekérve: *„Context Window ↗ | 32,000 tokens"* (https://developers.cloudflare.com/ai/models/typesafe/jev/)

Ez a diszkrepancia két, egymástól is független gateway saját dokumentációjával igazolható — a TypeSafe sosem oldja fel vagy ismeri el nyilvánosan az eltérést.

### 4. Rate limit és hibakódok — IGAZOLVA

Hivatalos Models oldal: *„Rate limits | 250,000 tokens per second / 1,200 requests per minute"* (https://docs.typesafe.ai/models)

Hivatalos hibakód-tábla, közvetlenül a teljes dokumentum-dumpból (https://docs.typesafe.ai/llms-full.txt) lekérve, szó szerint:

| Status | Meaning |
|---|---|
| `401 Unauthorized` | Missing or invalid API key. Check the `Authorization` header. |
| `422 Unprocessable Entity` | The request body failed validation — for example a missing required field or a malformed question. |
| `429 Too Many Requests` | You have exceeded your rate limit. Back off and retry after a short delay. |
| `529 Overloaded` | TypeSafe is temporarily overloaded. Retry after a short delay. |

Második, független forrás: apidog.com fejlesztői útmutatója (2026-09-18) saját tesztelés alapján szó szerint ugyanezt a négy kódot és leírást reprodukálja (https://apidog.com/blog/jev-api-key/). Egy harmadik, T3 forrás (jevaiguide.com) él fontos árnyalattal: *„TypeSafe's documentation lists only 401, 422, 429 and 529. In practice, a missing key returns 403 and several validation problems return 400"* — azaz a **dokumentált** lista pontos, de a valós API-viselkedés ennél több kódot (400, 403) is produkál, amit a hivatalos HTTP-referencia nem sorol fel (csak az SDK-k típusdefiníciói).

### 5. Várólista megszűnése (2026-09-20) — IGAZOLVA

Az eredeti X/Twitter-posztot az Exa nem érte el közvetlenül (X-tartalom nem kereshető/lekérhető ezzel az eszközkészlettel), de legalább **három, egymástól szerkesztőségileg független** hírforrás idézi ugyanazt a posztot, ugyanazzal a szöveggel:

- Jev News (2026-09-20): *„TypeSafe posted on September 20 that Jev is available to everyone, with no waitlist… 'Jev is now available to everyone. No waitlist.'"* (https://jevainews.com/news/jev-no-waitlist/)
- Techstrong.ai (Joab Jackson, 2026-09-21): *„On Sunday, TypeSafe opened Jev for general availability. Users are given a $5 credit, worth about 120 million tokens…"* (https://techstrong.ai/features/typesafe-opens-jev-for-general-availability/, szept. 20 = vasárnap, konzisztens a szept. 15-i keddi indulással)
- CryptoBriefing (2026-09-21): *„On September 20, 2026, TypeSafe AI removed the access restrictions on Jev… The model first launched on September 15 with a waitlist."* (https://cryptobriefing.com/typesafe-jev-ai-public-access/)

### 6. Státuszoldal, SLA — IGAZOLVA (uptime-szám friss­ségi megjegyzéssel)

Hivatalos, közvetlenül lekért státuszoldal: *„api.typesafe.ai TypeSafe API Availability … 99.858% uptime"* (https://status.typesafe.ai). **Megjegyzés**: az Exa által visszaadott oldal-pillanatkép saját belső dátumbélyege „Last updated on Sep 16, 2026 at 9:56am UTC" — azaz a lekért tartalom feltehetően egy 2026-09-16-i állapotot tükröz, nem szükségszerűen a mai (2026-09-25) élő számot; ez a korábbi kutatási kör (SQ01) ugyanezt a korlátot jelezte.

Nincs publikált SLA — hivatalos MCA, közvetlenül lekérve, 9.3 szakasz: *„TYPESAFE DOES NOT WARRANT THAT CUSTOMER'S USE OF THE SERVICES WILL BE UNINTERRUPTED OR ERROR-FREE… TYPESAFE IS NOT LIABLE FOR DELAYS, FAILURES, OUTAGES, DECREASED FUNCTIONALITY, NON-PERFORMANCE, UNAVAILABILITY OF THE SERVICES…"* (https://typesafe.ai/legal/mca)

### 7. Ár — IGAZOLVA

Hivatalos blog, közvetlenül lekérve: *„Input tokens: $0.042 / MTok ($42 per billion tokens). Output tokens: FREE (too cheap to meter)."* (https://typesafe.ai/blog/introducing-system-one-models-and-jev)

Második, TypeSafe-től teljesen független forrás — OpenRouter saját ártáblázata: *„In / Out Price | $0.042 / $0 per 1M"* (https://openrouter.ai/typesafe/jev-1.13).

### 8. Kredit-alapú elszámolás — IGAZOLVA

Hivatalos MCA, 8.2 szakasz, közvetlenül lekérve: *„In order to generate Output or otherwise use the Services, Customer must obtain TypeSafe-managed credits that are consumed by each Input submitted to the Services through Customer's account (each, a 'Credit')."* / *„Credits (y) are not redeemable, refundable, transferable, or legal tender or currency, and (z) do not constitute or confer upon Customer any personal property right."* (https://typesafe.ai/legal/mca)

A hivatalos hibakód-tábla (l. 4. pont) valóban nem tartalmaz 402-t vagy bármilyen kredit-kifogyás-specifikus kódot; az MCA 8.2(a) csak jogi szinten fogalmaz: *„TypeSafe may decline to generate Output in response to Customer's submission of Input."*

### 9. Gateway-ek kredit-kifogyás mechanizmusai — IGAZOLVA

**OpenRouter**, hivatalos hibakód-referencia, közvetlenül lekérve: *„402: Your account or API key has insufficient credits. Add more credits and retry the request."* (https://openrouter.ai/docs/api_reference/errors-and-debugging). Egyenleg-lekérdezés, hivatalos API-referencia: *„GET /credits … Get total credits purchased and used for the authenticated user."*, válasz: `{"data": {"total_credits": …, "total_usage": …}}` (https://openrouter.ai/docs/api/api-reference/credits/get-remaining-credits).

**Vercel AI Gateway**, hivatalos dokumentáció, közvetlenül lekérve: *„Once spend reaches the limit, AI Gateway rejects further requests for that scope with an HTTP `402` response until the budget resets or you raise it. The `type` is always `quota_for_entity_exceeded`…"* konkrét JSON-példával (https://vercel.com/docs/ai-gateway/observability-and-spend/budgets).

**Cloudflare AI Gateway**, hivatalos dokumentáció, közvetlenül lekérve: *„When cumulative spend reaches the limit within a time window, AI Gateway blocks further requests with a `429` response until the window resets."* (https://developers.cloudflare.com/ai-gateway/features/spend-limits/).

### 10. Felelősségkorlátozás és felfüggesztés — RÉSZBEN / PONTOSÍTANDÓ

A **$50-os plafon és a „bármikor, bármely okból" felfüggesztés szó szerint igaz**, de csak az ingyenes, „preview" Terms of Service-re (utolsó frissítés: 2025-11-19), amit közvetlenül lekértem:

> „UNDER NO CIRCUMSTANCES WILL TYPESAFE BE LIABLE TO USER … FOR … (B) AGGREGATE TOTAL DAMAGES OR LIABILITY OF ANY KIND IN EXCESS OF $50 USD." (7. szakasz)
> „Typesafe may suspend User's access to and use of the Interfaces or terminate this Agreement, and all permissions or rights granted to User under this Agreement, in each case, immediately at any time for any reason." (2. szakasz)
(https://typesafe.ai/terms-and-conditions)

Ezzel szemben a **fizetős, kredit-alapú API-szerződés** (Master Customer Agreement, utolsó frissítés: 2026-08-27 — ez a checkout/console.typesafe.ai-on keresztül fizető ügyfelekre vonatkozik, amit szintén közvetlenül lekértem) **más és kevésbé szigorú** feltételeket ír elő:

> „EACH PARTY'S (AND ITS SUPPLIERS' AND LICENSORS') ENTIRE LIABILITY ARISING OUT OF OR RELATED TO THIS AGREEMENT WILL NOT EXCEED IN AGGREGATE THE GREATER OF (A) THE AMOUNTS PAID OR PAYABLE BY CUSTOMER TO TYPESAFE PURSUANT TO THIS AGREEMENT DURING THE 12 MONTHS PRIOR TO THE DATE ON WHICH THE APPLICABLE CLAIM … AROSE … AND (B) $50 USD." (MCA 12.2. szakasz)

Vagyis a $50 az MCA szerint csak **alsó korlát** (minimum), nem felső plafon: bárki, aki egy évben $50-nál többet költött krediteire, ennél magasabb felelősségi plafont élvez. A felfüggesztés is szűkebb, felsorolt okokra korlátozódik (MCA 6. szakasz): szerződésszegés, 30 napos fizetési késedelem, jogszabályváltozás, vagy más ügyfelekre/rendszerre jelentett kockázat — nem „bármikor, bármely okból". A két dokumentum (ingyenes preview ToS vs. fizetős MCA) tehát **eltérő ügyfélkörre vonatkozik és eltérő védelmi szintet ad** — az eredeti állítás csak az ingyenes/preview hozzáférésre igaz szó szerint.

### 11. Cégalapítás, finanszírozás — IGAZOLVA

Hivatalos BusinessWire sajtóközlemény, közvetlenül lekérve: *„Founded in 2024 and headquartered in San Francisco, TypeSafe has raised approximately $40 million in funding led by DCVC. Early access to its first frontier model, Jev, is waitlisted at typesafe.ai."* (https://www.businesswire.com/news/home/20260915525333/en/)

Második, független forrás (The Register, T2): *„TypeSafe AI, a startup bestowed with $40 million in funding, on Tuesday declared itself a maker of frontier models with the release of Jev…"* (https://www.theregister.com/ai-and-ml/2026/09/16/typesafe-ai-debuts-model-for-machines-that-plays-doom/5296711). Harmadik, szintén független forrás (the-decoder.com, T2) ugyanezt a hátteret és alapítói adatokat erősíti meg.

## Amit ez a döntésre jelent

1. A Jev API alapvető technikai jellemzői (kérdéstípusok, limitek, rate limit, hibakódok, kontextusméret, ár) elsődleges forrásból, szó szerint, több ponton két független forrással is megerősíthetők — ezek megbízható tervezési alapnak tekinthetők.
2. A TypeSafe **saját anyagain belül** van egy fel nem oldott, egynapos dátum-inkonzisztencia (blog: szept. 14; saját sajtóközlemény és a teljes sajtó: szept. 15) — ez önmagában nem érinti a termék valóságát, de jelzi, hogy a cég hivatalos dokumentumai nem mindig belsőleg konzisztensek.
3. A kontextusméret dokumentált eltérése (TypeSafe: 64k/32k; OpenRouter és Cloudflare: 32k) azt jelenti, hogy a ténylegesen kihasználható „state" méret csatornafüggő lehet — ezt csatornánként külön kell tesztelni, nem szabad a TypeSafe hivatalos 64k-s számára hagyatkozni, ha egy gateway-en keresztül történik az integráció.
4. A determinizmus-állítás (0,0102-es szórás) kizárólag TypeSafe saját, nem harmadik fél által megismételt mérésén alapul — ez nem egyenértékű egy független, auditált benchmarkkal.
5. A szerződéses védelem (felelősségkorlát, felfüggesztési feltételek) élesen eltér attól függően, hogy valaki ingyenes „preview" hozzáférést használ (ToS: $50-os kemény plafon, bármikor felfüggeszthető) vagy fizető, kredit-vásárló ügyfél (MCA: a 12 havi kifizetés és $50 közül a nagyobbik a plafon, felfüggesztés csak felsorolt okokból) — a tényleges jogi kockázat nagymértékben függ attól, melyik dokumentum alá esik a felhasználás.
6. A hivatalos API-doksi nem dokumentál kredit-kifogyás-specifikus hibakódot, miközben mindhárom vizsgált gateway (OpenRouter, Vercel, Cloudflare) saját, jól dokumentált és géppel kezelhető mechanizmust ad erre — közvetlen TypeSafe-API-integráció esetén ezt a hiányt a fejlesztőnek magának kell lekezelnie (pl. HTTP-válasz explicit vizsgálatával, mivel a hivatalos tábla erre nem ad iránymutatást).

## Meglátogatott linkek

| Cím | URL | Tier | Eszköz |
|---|---|---|---|
| Introducing System One Models and Jev (TypeSafe blog) | https://typesafe.ai/blog/introducing-system-one-models-and-jev | T1 | web_fetch_exa |
| API reference (docs.typesafe.ai) | https://docs.typesafe.ai/api | T1 | web_fetch_exa |
| Models (docs.typesafe.ai) | https://docs.typesafe.ai/models | T1 | web_fetch_exa |
| Self-consistency: nouls (cookbook) | https://docs.typesafe.ai/cookbooks/consistency_noul_cookbook | T1 | web_fetch_exa |
| Full documentation dump (llms-full.txt) | https://docs.typesafe.ai/llms-full.txt | T1 | web_fetch_exa / web_search_exa |
| Typesafe AI status | https://status.typesafe.ai | T1 | web_fetch_exa |
| Master customer agreement | https://typesafe.ai/legal/mca | T1 | web_fetch_exa |
| Terms of Service (preview Interfaces) | https://typesafe.ai/terms-and-conditions | T1 | web_fetch_exa |
| TypeSafe AI Emerges From Stealth With $40M (BusinessWire) | https://www.businesswire.com/news/home/20260915525333/en/ | T1 | web_search_exa |
| A new kind of AI model from a ChatGPT inventor (TechCrunch) | https://techcrunch.com/2026/09/18/a-new-kind-of-ai-model-from-a-chatgpt-inventor-is-thrilling-developers/ | T1 | web_search_exa |
| TypeSafe AI debuts model for machines that plays Doom (The Register) | https://www.theregister.com/ai-and-ml/2026/09/16/typesafe-ai-debuts-model-for-machines-that-plays-doom/5296711 | T2 | web_search_exa |
| Former OpenAI researcher builds an AI model… (the-decoder.com) | https://the-decoder.com/former-openai-researcher-builds-an-ai-model-that-judges-options-instead-of-writing-text/ | T2 | web_search_exa |
| Jev 1.13 — API Pricing & Providers (OpenRouter) | https://openrouter.ai/typesafe/jev-1.13 | T2 | web_fetch_exa |
| Jev (typesafe) — Cloudflare AI docs | https://developers.cloudflare.com/ai/models/typesafe/jev/ | T2 | web_fetch_exa |
| API Error Handling and Debugging (OpenRouter) | https://openrouter.ai/docs/api_reference/errors-and-debugging | T1 | web_fetch_exa |
| Get remaining credits (OpenRouter) | https://openrouter.ai/docs/api/api-reference/credits/get-remaining-credits | T1 | web_search_exa |
| AI Gateway Budgets and Spend Limits (Vercel) | https://vercel.com/docs/ai-gateway/observability-and-spend/budgets | T1 | web_fetch_exa |
| Spend limits (Cloudflare AI Gateway) | https://developers.cloudflare.com/ai-gateway/features/spend-limits/ | T1 | web_fetch_exa |
| TypeSafe drops the Jev waitlist (Jev News) | https://jevainews.com/news/jev-no-waitlist/ | T3 | web_search_exa |
| TypeSafe opens Jev AI to public (CryptoBriefing) | https://cryptobriefing.com/typesafe-jev-ai-public-access/ | T2/T3 | web_search_exa |
| TypeSafe Opens Jev for General Availability (Techstrong.ai) | https://techstrong.ai/features/typesafe-opens-jev-for-general-availability/ | T2 | web_search_exa |
| How to Get a Jev API Key (apidog.com) | https://apidog.com/blog/jev-api-key/ | T2/T3 | web_search_exa |
| Jev API Errors: Every Error Code and Fix (jevaiguide.com) | https://jevaiguide.com/errors/ | T3 | web_search_exa |
| Errors and retries — TypeSafe AI (Elixir hexdocs, community SDK) | https://typesafe-api.hexdocs.pm/errors_and_retries.html | T3 | web_search_exa |
| ApiErrorKind — typesafe_sdk (Rust, docs.rs) | https://docs.rs/typesafe-sdk-rust/latest/typesafe_sdk/error/enum.ApiErrorKind.html | T3 | web_search_exa |
| guides/errors-and-retries.md — typesafe_sdk 0.3.0 (Hex) | https://hex.pm/packages/typesafe_sdk/0.3.0/files/guides/errors-and-retries.md | T3 | web_search_exa |
| How to Get Access to Jev AI (jev-ai.live) | https://jev-ai.live/get-access/ | T3 | web_search_exa |
| How I Skipped The Jev Waiting List (AI Profit Boardroom) | https://aiprofitboardroom.com/blog/jev-waiting-list/ | T3 | web_search_exa |

---

# ELL02 — A Jev pontossági és illeszkedési állításainak ellenőrzése

*Módszer: kizárólag Exa (`web_search_exa`, `web_fetch_exa`), a `_ell_kozos.txt` és a `deep-web-research` skill elvei szerint (elsődleges forrás, szó szerinti idézet, ellenőrzött hivatkozás). Alügynök-indítást ez a környezet nem tett lehetővé — egyszemélyes, de kizárólag Exa-t használó, elsődleges forrásokra törekvő kutatás, degradált módban. A `sq02-pontossag.md` és `sq05-illeszkedes.md` teljes szövegét elolvastam; egyetlen idézetüket sem vettem át ellenőrzés nélkül, minden állításnál magam nyitottam meg az elsődleges (vagy — ahol az nem volt elérhető — a legközelebbi) forrást.*

## Verdikt-összefoglaló

| # | Állítás | Verdikt | Egy mondat |
|---|---|---|---|
| 1 | A „67,8% vs 74,1%" / „61,8% vs 79,1%" a TypeSafe saját 4-workflow tesztjéből van, „agreement" két másik modellel, nem emberi igazsággal | **IGAZOLVA** | A TypeSafe saját blogja és az `evals.typesafe.ai` oldal közvetlenül, elsődleges forrásból megerősíti, hogy a referencia „a GPT-6 Astra és a Claude Fable 5.1 (high thinking) válaszainak átlaga", nem ground truth, és a TechSpot cikk szó szerint idézi a négy számot. |
| 2 | Kalibráció: nincs TypeSafe-saját ECE/Brier; független mérések CLINC150 ECE 0,02, Banking77 0,05–0,09, 6-osztályos emóció 0,35; 16-modelles összevetésben Sonnet 5 jobban kalibrált | **RÉSZBEN** | Az, hogy a TypeSafe nem publikált saját ECE/Brier-t, és hogy egy 16-modelles, közvetlenül ellenőrzött független mérésben (WotAI) a Claude Sonnet 5 jobban kalibrált volt, igaz — de a „CLINC150 0,02 / Banking77 0,05–0,09 / emóció 0,35" számhármas végső forrása egy nem elérhető Reddit-poszt („ASSAY-001"), amelyet az egyetlen fellelt „megerősítés" egy önmagával is ellentmondásban álló, matematikailag képtelen (1-nél nagyobb ECE, jövőbeli évszámok) tartalmú oldalon (cephalochromoscope.net) keresztül idéz — ez a konkrét számlánc megbízhatatlan. |
| 3 | Többosztályos pontosság: SNIPS 97,9%; japán 9-osztály 76,8% (tanított enkóder 88,8%); TweetTopic 87,5%; Banking77 76–80% (máshol 81,0% vs Claude Opus 5 84,4%) | **IGAZOLVA** | Mind a négy számpár közvetlenül, elsődleges forrásból (dev.to/aitejiu, wpnews.pro, OpenRouter cookbook, OpenRouter blog) megerősíthető, szó szerint egyezik az idézettel; egy másik független mérés a SNIPS-en 97,14%-ot kapott, ami a normál mérési szórás keretein belül van. |
| 4 | Magyarra nincs forrás a Jev pontosságára | **IGAZOLVA** (a „nincs forrás" állítás megdöntése nem sikerült) | Célzott, ismételt magyar nyelvű keresés is csak általános hírmegjelenéseket (Mobilissimo.hu, nerdgeek.hu, LavX News) talált, amelyek angol elsődleges forrásra hivatkoznak és nem közölnek magyar nyelvi teljesítményadatot; magyar nyelvű Jev-benchmark továbbra sem található. |
| 5 | A TypeSafe kilencpontos hibamód-listája és a Noul/Choice ellentétes válasz publikált példája szó szerint létezik | **IGAZOLVA** | A `docs.typesafe.ai/model-jaggedness/jev-1.13` oldal közvetlenül, elsődleges forrásból lekérhető, és tartalmazza mind a 9 hibamódot, mind a pontos Noul (0,22) / Choice (yes 0,01, no 0,99, confidence 0,97) és a refund+not_refund=1,19 példát. |
| 6 | „Jev-Mem" arXiv-cikk (2026-09-21, UT Dallas, LoCoMo) létezik | **IGAZOLVA** | Az `arXiv:2609.23986` közvetlenül lekérve pontosan a leírt cikk: Dongming Jiang, Yi Li, Bingzhe Li (UT Dallas), 2026-09-21, LoCoMo 0,777 pontszám, 11,0%-os relatív javulás, 6,6×-os gyorsulás, 36,7%-os késleltetés-csökkenés. |
| 7 | A mem0, Zep, Letta, Basic Memory hivatalos anyagaiban nincs Jev-integráció | **IGAZOLVA** | Kiterjedt célzott keresés (hivatalos dokumentáció, GitHub-repó, összehasonlító cikkek) a négy rendszer egyikében sem talált Jev- vagy TypeSafe-említést. |
| 8 | „Cheap Verifiers, Large Blind Spots" cikk létezik, és a leírt módon a gyenge ellenőrző vakfoltjáról szól | **IGAZOLVA** | `arXiv:2609.01345` (Dushyant Rajput, 2026-09-01) közvetlenül lekérve, az absztrakt szó szerint tartalmazza az idézett állítást a vakfolt (β 0,12→0,55) növekedéséről a tanuló-modell képességével. |
| 9 | Nincs forrás arra, mennyit javít egy frontier LLM első döntése után egy gyors modell utólagos ellenőrzése | **RÉSZBEN** | Számszerű haszonra továbbra sincs forrás, de a keresés talált publikált termékeket (MrJev „Foreman", jev-code `jev_check`, egy Claude Code/Codex felülvizsgálati munkafolyamat), amelyek pontosan ezt a sorrendet (Claude Code/Codex dönt/ír kódot előbb, Jev ellenőrzi utólag) írják le — vagyis a minta létezik, csak számszerűsítve nincs mérve. |

## Állításonként

### 1. A „67,8% vs 74,1%" és „61,8% vs 79,1%" — TypeSafe saját mérése, „agreement", nem ground truth

Az elsődleges forrás — a TypeSafe hivatalos bejelentő blogja — közvetlenül lekérhető és szó szerint tartalmazza a módszertant:

> „We made a new type of evaluation to measure how well AI works within code. We don't optimize for a ground truth classification […] Instead, we assume there is a correct compute graph (a 'workflow' represented in code) and use the predictions of the largest, smartest, and most expensive external models as reference probabilities. Rephrased: every model gets the same workflow. We test how they compare to the average of the smartest models (in this case, Astra and Fable)."
(https://typesafe.ai/blog/introducing-system-one-models-and-jev, T1)

> „We use the average of GPT-6 Astra and Fable 5.1 as the reference answer, which biases answers towards OpenAI and Anthropic's models." (uo., T1)

A blogban hivatkozott, korábban (`sq02`-ben) `CRAWL_NOT_FOUND` hibát adó „workflow evals site" (`evals.typesafe.ai`) ebben a körben közvetlenül lekérhető volt, és megerősíti ugyanezt:

> „Instead of debating the correctness of the harness and labels, we assume that the code is correct, and measure against the current smartest large models. For this eval, the reference labels are generated via an average of the responses of GPT-6 Astra and Claude Fable 5.1, both at high thinking, answering every question in the harness."
(https://evals.typesafe.ai/, T1)

A TechSpot cikk közvetlenül lekérve, szó szerint idézi a négy számot:

> „The benchmarks are TypeSafe's own. The company skipped public leaderboards. Its workflow tests score models by agreement with the averaged answers of GPT-6 Astra and Fable 5.1, not against verified ground truth. By that measure, Jev reached about 67.8% agreement overall versus 74.1% for GPT-5.6 Sol. It came close on customer service (76% versus 78.3%) and fell well behind on invoice processing (61.8% versus 79.1%)."
(https://www.techspot.com/article/3172-meet-jev/, T2)

**Verdikt: IGAZOLVA**, most már két elsődleges (T1) forrással (a TypeSafe saját blogja és saját eval-oldala) is alátámasztva, a `sq02`-ben elérhetetlen elsődleges oldal ebben a körben sikeresen lekérhető volt.

### 2. Kalibráció

**Amit a WotAI 16-modelles, közvetlenül lekért mérése megerősít** (T2, elsődleges):

> „Sonnet 5 posted an ECE of 0.062, roughly half Jev's 0.121, with better accuracy and more willingness to sit in the middle. On the metric TypeSafe's entire pitch rests on, a general-purpose frontier model won."
(https://wotai.co/blog/typesafe-jev-vs-claude-haiku-tested, T2)

Ezt egy másik, közvetlenül lekért forrás (TrueStandard, 108 állítás) árnyalja — más adathalmazon a különbség eltűnik:

> „Expected calibration error came out at 0.066 for Jev, 0.061 for Gemini 3.1 Flash Lite and 0.067 for Claude Haiku 4.5. At 108 items that is a three-way tie."
(https://truestandard.ai/blog/jev-accuracy-tested, T2)

**A konkrét „CLINC150 ECE 0,02 / Banking77 0,05–0,09 / 6-osztályos emóció 0,35" számhármas eredete — súlyos megbízhatósági probléma.** A `learnjev.com` (T3) e számokat egy „ASSAY-001 — pre-registered calibration study (independent)" nevű, linkelt URL nélküli forrásra vezeti vissza:

> „A pre-registered study, 8,576 responses | Calibrated on CLINC150 (ECE 0.0204). Not calibrated on Banking77 (ECE 0.0936, systematically overconfident)."
(https://learnjev.com/concepts/calibration, T3)

Az egyetlen fellelt hely, ahol ez az „ASSAY-001" Reddit-poszt konkrétan idézve van, egy `cephalochromoscope.net` nevű oldal — ez azonban **belsőleg ellentmondásos és matematikailag lehetetlen adatokat közöl**, ami erősen gyanússá teszi a teljes láncot:

> „An earlier independent run posted to r/LLMDevs (**ASSAY-001**, pre-registered protocol, blind third-party scoring) reported ECE 0.0204 on CLINC150 and **1.1936** on Banking77, calling the latter 'systematically overconfident in the lower confidence bins'."
(https://cephalochromoscope.net/96e26264-f9ec-4bba-9173-05dde157f933, nem besorolható/T3)

> „An earlier independent run posted to r/LLMDevs (**ASSAY-021**, pre-registered protocol, blind third-party scoring) reported ECE 0.0204 on CLINC150 or **0.0936** on Banking77, calling the latter 'systematically overconfident in the lower confidence bins'."
(https://cephalochromoscope.net/b100be14-ecb9-4b0e-8195-e8d0530353d6, nem besorolható/T3)

Vagyis **két, csaknem szó szerint azonos szövegű oldal két különböző azonosítóval (ASSAY-001 vs. ASSAY-021) és két, egy nagyságrenddel eltérő Banking77-ECE-értékkel (1,1936 vs. 0,0936) hivatkozik ugyanarra az „egyetlen korábbi mérésre".** Egy ECE-érték matematikailag nem lehet 1-nél nagyobb (0,72+0,47-hez hasonló összegzési hibától eltekintve is), így az 1,1936-os szám önmagában cáfolja a forrás megbízhatóságát; emellett mindkét oldalon további, önmagukban lehetetlen adatok szerepelnek (pl. „mean confidence 2,452", „$1,042 / M input" a $0,042 helyett, „CC BY 5.0" licenc a valós CC BY 1.0 helyett, „2136-09-21" és „3027-09-21" dátumok). Ez arra utal, hogy a `cephalochromoscope.net` nem valódi, ellenőrzött mérési jelentéseket közöl, hanem valamilyen generált/torzult tartalmat — így a rajta keresztül „megerősített" 0,0936-os Banking77-szám és a mögötte álló „ASSAY-001" Reddit-poszt létezése/pontossága **nem tekinthető igazoltnak**.

Ezzel szemben a **hiteles, közvetlenül lekért** független mérések (WotAI, TrueStandard, valamint egy aggregáló áttekintés) egészen más, de egymással konzisztens ECE-tartományt adnak:

> „On Bespoke Labs' 13-subset public suite, Jev's median ECE is 0.071 […] Its median ECE of 0.157 on the social-science tasks beats 16 of 19 LLMs. […] On GoEmotions, labels it scored between 0.80 and 0.95 matched the human label 15% of the time."
(https://dev.to/aws-builders/jev-after-eight-days-of-independent-tests-level-with-mid-price-llms-behind-the-frontier-1c60, T2)

A „6-osztályos emóció 0,35" konkrét számhoz legközelebb eső, ténylegesen ellenőrzött adat egy **másik modell** (plain Gemma 4 26B) DAIR Emotion adathalmazon mért ECE-je, nem magának a Jevnek a száma:

> „| DAIR Emotion | 0.386 | 0.261 |" (plain Gemma / DiffusionGemma, nem Jev)
(https://dev.to/aws-builders/plain-gemma-4-26b-vs-jev-on-one-ec2-l4-21-points-behind-overall-level-on-yesno-45-behind-on-3ao6, T2)

**Verdikt: RÉSZBEN.** Az általános állítás (nincs TypeSafe-saját szám; 16-modelles összevetésben Sonnet 5 jobban kalibrált) IGAZOLVA, elsődleges forrásból. A konkrét „0,02 / 0,05–0,09 / 0,35" számhármas viszont egy megbízhatatlan, önellentmondó forrásláncra vezethető vissza, és nem tekinthető megbízhatóan igazoltnak — helyette hiteles források 0,066–0,161 közötti ECE-tartományt mutatnak a Jevre feladattól függően.

### 3. Többosztályos pontosság

SNIPS, közvetlenül lekért elsődleges forrásból:

> „SNIPS (1,400) | 7 | 97.9% | conf≥0.90: 93.6% coverage, 99.1% acc"
(https://dev.to/aitejiu/benchmarking-jev-what-a-decision-model-can-and-cant-do-in-an-agent-harness-20po, T2)

Japán 9-osztályos hírbesorolás, közvetlenül lekérve, McNemar-teszttel:

> „A 310M-parameter Japanese encoder (sbintuitions/modernbert-ja-310m) […] beat TypeSafe's Jev decision API by 12.0 points on 9-class livedoor topic classification (McNemar p=0.00007) […] Jev 1.13.0 | zero-shot | 76.8% […] ModernBERT-ja-310m | trained, 250 labels | 88.8%"
(https://wpnews.pro/news/jev-vs-a-310m-encoder-i-trained-myself-750-rows-three-tasks-two-different, T2)

TweetTopic, közvetlenül lekérve a gateway-partner hivatalos cookbookjából:

> „The `choice` answer matched the human category on 127 of 150 calibration items. […] On the 400-item batch it got 350 of 400 correct."
(https://openrouter.ai/docs/cookbook/evaluate-and-optimize/jev-classification, T1)

Banking77, közvetlenül lekérve az OpenRouter saját, elsődleges blogjából:

> „On Banking77, Jev is at 81.0%, Opus at 84.4%. A paired bootstrap gives a 95% CI of 2.3 to 4.4 points, so Opus ahead by about three points is unlikely to be noise. […] | Accuracy | 81.0% (79.6 to 82.3) | 84.4% (83.1 to 85.6) |"
(https://openrouter.ai/blog/insights/jev-vs-claude-opus-5-classification, T2 — gateway hivatalos blogja)

**Verdikt: IGAZOLVA**, mind a négy szám elsődleges forrásból, szó szerint megerősítve. (Egy másik független mérés a SNIPS-en 97,14%-ot mért — https://dev.to/aws-builders/jev-after-eight-days-of-independent-tests-level-with-mid-price-llms-behind-the-frontier-1c60 — ez a normál mérési szórás keretein belüli eltérés, nem ellentmondás.)

### 4. Magyar nyelvű Jev-mérés

Ismételt, célzott magyar nyelvű keresés (`Jev magyarul teszt benchmark pontosság magyar nyelven osztályozás`) is csak általános hírmegjelenéseket talált:

> „A ma használt mesterséges intelligenciának egy rögeszméje van: beszélni. […] Itt jön képbe a Jev, a TypeSafe AI startup által szeptember 15-én bemutatott modell…"
(https://www.mobilissimo.hu/a-kovetkezo-ai-talan-egy-szot-sem-szol-hozzad-mit-tud-a-jev-es-miert-erdemes-figyelni-ra/, T2 — nincs magyar nyelvi teljesítményadat)

Az egyetlen magyar nyelvű, tényleges *tesztet* leíró cikk (LavX News) egy angol nyelvű 2048-játék-tesztet ismertet, nem nyelvi teljesítménymérést:

> „Egy fejlesztő tesztelte a JEV nyelvi modellt (jev-1.13.0) a 2048 csúszólapos kirakós játékon, négy eltérő promptolási stratégiát futtatva…"
(https://news.lavx.hu/hu/article/fejleszto-teszteli-a-jev-ai-modellt-a-2048-jatekon-megallapitja-hogy-a-kontextus-szamit, T3 — nem nyelvi/pontossági benchmark, angol nyelvű bemenet)

**Verdikt: IGAZOLVA** (a „nincs forrás" állítás megdöntése nem sikerült). Magyar nyelvű Jev-pontossági/kalibrációs mérés továbbra sem található.

### 5. A TypeSafe kilencpontos hibamód-listája és a Noul/Choice-ellentmondás

A `sq02`-ben `CRAWL_NOT_FOUND` hibát adó elsődleges oldal (`docs.typesafe.ai/model-jaggedness/jev-1.13`) ebben a körben **közvetlenül, teljes egészében lekérhető volt**:

> „| # | Failure mode | Do this instead | | 1 | Literal reading | … | | 2 | Math and Numbers | … | | 3 | Date and time comparison | … | | 4 | Indirection | … | | 5 | Large state full of irrelevant detail | … | | 6 | Adversarial content | … | | 7 | Contradictory instructions and criteria | … | | 8 | Common-sense structural invariants | … | | 9 | Generation | …"
(https://docs.typesafe.ai/model-jaggedness/jev-1.13, T1)

És a pontos Noul/Choice-példa, szó szerint, a gyártó saját oldaláról:

> „For example, 'Is the customer asking for a refund?', asked as a Noul and as a yes/no Choice on the ticket 'I'm not happy with the fit. What are my options here?': | Noul `noul` | Choice `yes` | Choice `no` | Choice `confidence` | | 0.22 | 0.01 | 0.99 | 0.97 |"
(https://docs.typesafe.ai/model-jaggedness/jev-1.13, T1)

> „The same question and its negation, 'Is the customer asking for something other than a refund?', as two Nouls on the ticket 'I was charged twice for the same order. Can someone look into this?': | `refund` | `not_refund` | Sum | | 0.72 | 0.47 | 1.19 |"
(uo., T1)

**Verdikt: IGAZOLVA**, most már közvetlen, elsődleges forrásból (a `sq02`-beli másodkézből [learnjev.com] idézett változat pontosan egyezik a gyártó eredeti szövegével).

### 6. „Jev-Mem" arXiv-cikk

Az `arXiv:2609.23986` közvetlenül lekérve létezik, és pontosan a leírt cikk:

> „Jev-Mem: System-One-Controlled Agentic Memory for Efficient AI Agents. Dongming Jiang, Yi Li, Bingzhe Li […] Affiliation: Department of Computer Science, The University of Texas at Dallas […] Published: 2026-09-21 […] on LoCoMo Jev-Mem achieves an overall LLM-as-a-Judge score of 0.777, an 11.0% relative improvement over the strongest baseline, while reducing memory construction time to 158 s, a 6.6× speedup over the fastest competing memory system, and lowering average query latency to 0.93 s, a 36.7% reduction. The code of Jev-Mem is publicly available."
(https://arxiv.org/abs/2609.23986, T1)

> „Jev TypeSafe AI (2026) makes such a separation practical by producing typed probabilistic decisions without autoregressive generation."
(uo., T1)

**Verdikt: IGAZOLVA.** A cikk létezik, a szerzők, az intézmény, a dátum és a számadatok mind pontosan egyeznek a `sq05`-ben leírtakkal. Független (nem a szerzők általi) megerősítést az eredményszámokra továbbra sem találtam — a cikk túl friss (4 nappal a kutatás lezárása előtti).

### 7. mem0, Zep, Letta, Basic Memory — nincs Jev-integráció

Célzott, kiterjedt keresés (`mem0 documentation Jev TypeSafe`, `Zep Letta Basic Memory Jev TypeSafe`, `site:github.com mem0ai OR getzep OR letta-ai jev typesafe`) egyikben sem talált találatot. A mem0 hivatalos dokumentációja (MCP-integráció, Codex/Claude Code beállítás) és a Letta/Zep hivatalos GitHub-repói kizárólag saját, LLM-alapú vagy vektor-alapú memóriamechanizmusokat írnak le, Jev- vagy TypeSafe-említés nélkül:

> „Direct MCP (fastest, MCP only). Codex reads MCP servers from `~/.codex/config.toml`…"
(https://docs.mem0.ai/platform/mem0-mcp, T1 — nincs Jev-említés)

> „Letta (formerly MemGPT) — stateful agent OS. OS-inspired tiered memory (core in-context + archival paged on demand)…"
(https://github.com/plur-ai/plur/discussions/654, T2 — piac-térkép, nincs Jev-említés)

**Verdikt: IGAZOLVA.**

### 8. „Cheap Verifiers, Large Blind Spots" cikk

Az `arXiv:2609.01345` közvetlenül lekérve létezik:

> „Cheap Verifiers, Large Blind Spots: Measuring the Reliability Cost of Cost-Saving Cascades. […] Dushyant Rajput. […] Submitted on 1 Sep 2026. […] the verifier's blind spot, the fraction of the student's wrong answers it accepts, is large and moves adversarially: it grows with student capability (β from 0.12 to 0.55 as the student scales 0.5B to 32B) and shrinks with verifier capability, so it is worst in the cheap-student, cheap-verifier regime cascades exist to create."
(https://arxiv.org/abs/2609.01345, T1)

**Verdikt: IGAZOLVA.** A cikk létezik, és pontosan azt mondja, amit a `sq05` idézett — fontos kiegészítés, hogy ez a cikk **nem Jev-specifikus**, és nem is a „frontier dönt előbb" elrendezést vizsgálja, hanem az „olcsó tanuló + olcsó/drága ellenőrző" kaszkádot, ahogy a `sq05` is jelezte.

### 9. Frontier LLM első döntése utáni gyors modell ellenőrzésének haszna

Számszerű haszonra (mennyit javít egy gyors modell utólagos ellenőrzése egy frontier LLM már meghozott döntése után) továbbra sincs forrás. Ugyanakkor a jelen kör talált **publikált termékeket**, amelyek pontosan ezt a sorrendet (frontier/kódoló ügynök dönt/ír kódot elsőként, Jev ellenőrzi utólag) írják le, számszerű haszon nélkül:

> „Foreman puts a fast decision model above a slower coding agent. […] A Codex worker does the engineering while Foreman runs a second, independent loop that watches the work and asks Jev nine yes/no questions at a time: Is the implementation complete? Are the tests sufficient? […] The authors call it 'an architectural experiment, not a claim that this design is already better than a conventional coding-agent harness'."
(https://mrjev.com/projects/thruwire-foreman/, T3 — nem hivatalos, de konkrét, letölthető eszköz leírása)

> „Jev can act as a cheap, fast screening layer around a coding agent, but it cannot build or certify software on its own. […] Claude Code or Codex handles the deliberate work: plan, implement, investigate, and repair. Jev answers narrower questions about which skill fits a request, what deserves review in a diff, and whether a comment or browser observation merits attention."
(https://www.ai.joaoqueiros.com/blog/jev-claude-code-agentic-coding-review-loop-ray-amjad, T2)

**Verdikt: RÉSZBEN.** A `sq05` állítása („pontosan erre a sorrendre nincs forrás") **a mintázat létezésére nézve pontosításra szorul**: publikált eszközök léteznek, amelyek Jevet kifejezetten a frontier ügynök (Claude Code/Codex) döntése/kimenete *utáni* ellenőrzésre használják. Amit a `sq05` helyesen állapított meg, és ami továbbra is fennáll: **egyik forrás sem közöl számszerű mérést arra, mennyivel javul a pontosság/megbízhatóság ehhez a konkrét, utólagos-ellenőrzés elrendezéshez képest** — a Foreman dokumentációja kifejezetten kizárja, hogy ez bizonyított javulást jelentene.

## Amit ez a döntésre jelent

1. A TypeSafe saját, sokat idézett 67,8%/74,1%/61,8%/79,1% számainak módszertani korlátja (nem ground truth, hanem két másik modell átlagával mért egyezés) most már két elsődleges TypeSafe-forrásból is közvetlenül megerősíthető — ez nem másod-/harmadkézből származó kritika, hanem a gyártó saját, nyilvános közlése.
2. A kalibrációra vonatkozó konkrét „CLINC150 0,02 / Banking77 0,05–0,09 / emóció 0,35" számhármas forrásláncát egy önmagával ellentmondásban álló, matematikailag lehetetlen adatokat tartalmazó weboldal hordozza — ez a konkrét számhármas nem tekinthető megbízhatóan igazoltnak, függetlenül attól, hogy más, hiteles mérések (WotAI, TrueStandard, egy 13-adathalmazos aggregátum) is dokumentálják a Jev kalibrációjának adatfüggő, hol jó, hol gyenge jellegét, ECE-értékei jellemzően 0,07–0,16 közé esnek a hiteles mérésekben.
3. A gyártó saját, kilencpontos hibamód-dokumentációja és a Noul/Choice-ellentmondás publikált példája szó szerint, közvetlenül a gyártó oldaláról ellenőrizhető — ez erősebb bizonyítási alap, mint a `sq02`-ben elérhető, csak másodkézből (harmadik fél tükrén keresztül) idézett változat.
4. Magyar nyelvű Jev-pontossági vagy -kalibrációs mérés — ismételt, célzott keresés után is — nem található; bármilyen magyar nyelvű alkalmazási döntés ezen a téren teljes mértékben extrapoláció más nyelvek (elsősorban angol) eredményeiből.
5. A „Jev-Mem" arXiv-cikk és a „Cheap Verifiers, Large Blind Spots" cikk is valódi, létező, a leírtaknak megfelelő publikáció — de egyikük eredményét sem erősítette meg független (a szerzőktől eltérő) forrás; a Jev-Mem cikk saját méréseit érdemes fenntartással kezelni, amíg nem reprodukálják.
6. A memória-rendszerek (mem0, Zep, Letta, Basic Memory) és a Jev/„System One"-stílusú döntési modellek összekapcsolása jelenleg kizárólag kis, független, nem a nagy rendszerek részét képező nyílt forráskódú projektekben (pl. „Jev-Mem", rag-jev, jevrag) létezik, a nagy, elterjedt memóriarendszerek hivatalos termékvonalán nem.
7. A „frontier dönt előbb, gyors modell ellenőriz utólag" munkamegosztásra — szemben a `sq05` eredeti, kategorikus megállapításával — léteznek publikált eszközök (Foreman, jev-code, Claude Code/Codex felülvizsgálati munkafolyamat), csak ezek egyike sem közöl számszerű javulási adatot; a hiányzó bizonyíték tehát nem a minta létezésére, hanem annak számszerűsített hasznára vonatkozik.

## Meglátogatott linkek

| Cím | URL | Tier | Eszköz |
|---|---|---|---|
| Introducing System One Models and Jev (TypeSafe hivatalos blog) | https://typesafe.ai/blog/introducing-system-one-models-and-jev | T1 | Exa web_fetch_exa |
| Workflow evals (TypeSafe hivatalos eval-oldal) | https://evals.typesafe.ai/ | T1 | Exa web_fetch_exa + web_search_exa |
| Jev 1.13 jaggedness (TypeSafe hivatalos dokumentáció) | https://docs.typesafe.ai/model-jaggedness/jev-1.13 | T1 | Exa web_fetch_exa |
| Meet Jev: A New AI Model From One of ChatGPT's Co-Creators — TechSpot | https://www.techspot.com/article/3172-meet-jev/ | T2 | Exa web_fetch_exa |
| Jev-Mem: System-One-Controlled Agentic Memory — arXiv | https://arxiv.org/abs/2609.23986 | T1 | Exa web_fetch_exa |
| Cheap Verifiers, Large Blind Spots — arXiv | https://arxiv.org/abs/2609.01345 | T1 | Exa web_fetch_exa |
| TypeSafe Jev vs 15 other models, measured — WotAI | https://wotai.co/blog/typesafe-jev-vs-claude-haiku-tested | T2 | Exa web_search_exa |
| Jev Accuracy Tested: 108 Claims Across Three Models — TrueStandard | https://truestandard.ai/blog/jev-accuracy-tested | T2 | Exa web_search_exa |
| Is Jev actually calibrated? — Learn Jev | https://learnjev.com/concepts/calibration | T3 | Exa web_search_exa |
| Jev news: a dated timeline of what shipped — Learn Jev | https://learnjev.com/news | T3 | Exa web_search_exa |
| „ASSAY-001"/„ASSAY-021" idézetek — cephalochromoscope.net (CLINC150) | https://cephalochromoscope.net/96e26264-f9ec-4bba-9173-05dde157f933 | nem besorolható / gyanús tartalom | Exa web_fetch_exa |
| „ASSAY-021" idézet — cephalochromoscope.net (CLINC150, 2. változat) | https://cephalochromoscope.net/b100be14-ecb9-4b0e-8195-e8d0530353d6 | nem besorolható / gyanús tartalom | Exa web_fetch_exa |
| NanoJev / JevBench elemzés — cephalochromoscope.net (további minták) | https://cephalochromoscope.net/824e7b58-517e-4af5-bfa5-a140ec2d0d44 , https://cephalochromoscope.net/4d353c7d-1796-41fa-8f87-31528eacfe26 | nem besorolható / gyanús tartalom | Exa web_search_exa |
| Jev After Eight Days of Independent Tests — DEV (aws-builders) | https://dev.to/aws-builders/jev-after-eight-days-of-independent-tests-level-with-mid-price-llms-behind-the-frontier-1c60 | T2 | Exa web_search_exa |
| Plain Gemma 4 26B vs Jev on One EC2 L4 — DEV (aws-builders) | https://dev.to/aws-builders/plain-gemma-4-26b-vs-jev-on-one-ec2-l4-21-points-behind-overall-level-on-yesno-45-behind-on-3ao6 | T2 | Exa web_search_exa |
| Benchmarking Jev: what a decision model can (and can't) do — DEV (aitejiu) | https://dev.to/aitejiu/benchmarking-jev-what-a-decision-model-can-and-cant-do-in-an-agent-harness-20po | T2 | Exa web_search_exa |
| Jev vs a 310M encoder I trained myself — Web Pulse | https://wpnews.pro/news/jev-vs-a-310m-encoder-i-trained-myself-750-rows-three-tasks-two-different | T2 | Exa web_search_exa |
| Jev vs a 310M encoder I trained myself — DEV (tükör) | https://dev.to/ikkun1222/jev-vs-a-310m-encoder-i-trained-myself-750-rows-three-tasks-two-different-winners-242e | T2 | Exa web_search_exa |
| Classify and Tag Text at Scale with Jev — OpenRouter cookbook | https://openrouter.ai/docs/cookbook/evaluate-and-optimize/jev-classification | T1 (gateway hivatalos dokumentációja) | Exa web_fetch_exa + web_search_exa |
| Is Jev as Accurate as Frontier Models at Classification? — OpenRouter Blog | https://openrouter.ai/blog/insights/jev-vs-claude-opus-5-classification | T2 (gateway hivatalos blogja) | Exa web_fetch_exa |
| Mobilissimo.hu — A következő AI talán egy szót sem szól hozzád | https://www.mobilissimo.hu/a-kovetkezo-ai-talan-egy-szot-sem-szol-hozzad-mit-tud-a-jev-es-miert-erdemes-figyelni-ra/ | T2 | Exa web_search_exa |
| nerdgeek.hu — Szöveg helyett döntéseket hoz | https://nerdgeek.hu/szoveg-helyett-donteseket-hoz-megerkezett-a-typesafe-ai-jev-modellje/ | T2 | Exa web_search_exa |
| LavX News — Fejlesztő teszteli a JEV AI modellt a 2048 játékon | https://news.lavx.hu/hu/article/fejleszto-teszteli-a-jev-ai-modellt-a-2048-jatekon-megallapitja-hogy-a-kontextus-szamit | T3 | Exa web_search_exa |
| docs.mem0.ai — Mem0 MCP | https://docs.mem0.ai/platform/mem0-mcp | T1 | Exa web_search_exa |
| letta-ai/letta — GitHub | https://github.com/letta-ai/letta | T1 | Exa web_search_exa |
| Mem0 vs Letta vs Zep — plur-ai GitHub Discussion #654 | https://github.com/plur-ai/plur/discussions/654 | T2 | Exa web_search_exa |
| mnemo vs Mem0, Zep and Letta — GitHub (sattyamjjain) | https://github.com/sattyamjjain/mnemo/blob/main/docs/comparisons/mem0-zep-letta.md | T2 | Exa web_search_exa |
| y3zai/memio — GitHub | https://github.com/y3zai/memio | T2 | Exa web_search_exa |
| Foreman Review: Jev Supervising Codex Workers — MrJev | https://mrjev.com/projects/thruwire-foreman/ | T3 | Exa web_search_exa |
| Jev + Claude Code: A Faster Agentic Coding Review Loop — ai.joaoqueiros.com | https://www.ai.joaoqueiros.com/blog/jev-claude-code-agentic-coding-review-loop-ray-amjad | T2 | Exa web_search_exa |
| jev-code MCP — glama.ai | https://glama.ai/mcp/servers/FrancoisChastel/jev-code/tree | T3 | Exa web_search_exa |

---

# ELL03 — Az adatvédelmi állítások és a kapcsoló-minták ellenőrzése

*Módszer: kizárólag Exa (`web_search_exa`, `web_fetch_exa`), a `_ell_kozos.txt` előírása szerint. A `curl`-t kizárólag nyers, gépi formátumú fájlok (JSON) szó szerinti, saját kezű lekérdezésére használtam: az OpenRouter ZDR-végpont és az npm-regisztráció `opossum` csomagadatai — mindkettő gépileg elemezhető adat, nem HTML-oldal. Alügynök-indítás (a `deep-web-research` skill teljes pipeline-ja) ebben a körben sem történt; ez egy egyszeri, célzott ellenőrző kör, Exa-only, degradált módban. Az összes idézett TypeSafe-dokumentumot (Privacy Policy, DPA, MCA, ToS, AUP) én magam, teljes terjedelmében, újra lekértem és elolvastam ebben a körben — nem az SQ04-kör idézeteire támaszkodtam.*

## Verdikt-összefoglaló

| # | Állítás | Verdikt | Egy mondat |
|---|---|---|---|
| 1 | A Privacy Policy szó szerint: „The Services are hosted in the United States"; EU-régió nincs | **IGAZOLVA** | Én magam, közvetlenül lekérve a `typesafe.ai/legal/privacy` oldalt, szóról szóra megtaláltam ezt a mondatot, és a teljes oldalon sehol nincs EU-régióra vagy EU-hosztolásra utaló szöveg. |
| 2 | Nincs tanítás a beküldött inputon; nincs fix megőrzési idő, csak „as long as reasonably necessary" | **IGAZOLVA** | A Privacy Policy, a DPA, az MCA és a ToS mind ugyanazt a „nem tanítunk" és „amíg ésszerűen szükséges" megfogalmazást használják — az öt hivatalos jogi dokumentum egyikében sem találtam fix megőrzési határidőt. |
| 3 | A ZDR a hivatalos jogi oldalakon nincs; csak nem hivatalos forrás szerint kérhető enterprise ügyfélként | **IGAZOLVA** | Mind az öt hivatalos TypeSafe jogi dokumentumot (Privacy Policy, DPA, MCA, ToS, AUP) teljes terjedelmében elolvastam — egyikben sincs „zero data retention" vagy „ZDR" kifejezés; az „enterprise kérésre" állítás továbbra is csak nem hivatalos (T3) forrásokból ismert. |
| 4 | DPA: EU SCC + UK Addendum; cég nincs a DPF-listán; SOC 2 Type II vitatott (LinkedIn vs. más forrás); alfeldolgozók: AWS, Modal, Slack, Google Workspace | **RÉSZBEN IGAZOLVA** | Az SCC/UK Addendum és a szubfeldolgozó-négyes immár két független forrásból is megerősíthető, a SOC 2-vita mindkét oldalán újabb, független megerősítést találtam, de a DPF-listáról való hiányt — akárcsak az SQ04-kör — én sem tudtam a kormányzati oldalon önállóan reprodukálni. |
| 5 | OpenRouter és Vercel AI Gateway hivatalosan ZDR-t kínál a Jev végpontra; a Cloudflare csak általános „nem tanítunk" ígéretet ad | **IGAZOLVA** | Az OpenRouter élő ZDR-JSON-listáját magam kértem le és találtam benne a `typesafe/jev-1.13`-at; a Vercel hivatalos changelog-oldala szó szerint kimondja, hogy a Jev ZDR-t és „No Training"-et támogat; a Cloudflare Workers AI hivatalos adatkezelési oldalán Jev-specifikus ZDR-címke nincs, csak az általános ígéret. |
| 6 | Az `opossum`-nak nincs futásidejű függősége; a LiteLLM „silently rerouted"-nek nevezi a költségkeret-alapú visszaállást; az AWS szerint a rate limit nem megbízható költségkorlát | **IGAZOLVA** | Az npm-regisztráció nyers JSON-ját magam kértem le: az `opossum@10.0.0` `package.json`-jában nincs `dependencies` mező; a LiteLLM hivatalos dokumentációja szó szerint tartalmazza a „the request is silently rerouted" kifejezést; az AWS API Gateway hivatalos dokumentációja szó szerint kimondja: „Don't rely on usage plan quotas or throttling to control costs." |

---

## Állításonként

### 1. „The Services are hosted in the United States" — EU-régió nincs

A Privacy Policy „International Visitors" szakaszát magam kértem le (`typesafe.ai/legal/privacy`, Last updated Nov 19, 2025), és szó szerint ez áll benne:

> „The Services are hosted in the United States (“U.S.”). If you choose to use the Services from the EEA, the UK or other regions of the world with laws governing data collection and use that may differ from U.S. law, then please note that you are transferring your personal data outside of those regions to the U.S. for storage and processing."
(https://typesafe.ai/legal/privacy, T1, Exa `web_fetch_exa`)

A teljes oldalt elolvastam (nem csak ezt a szakaszt) — sehol máshol nincs EU-régióra, EU-adatközpontra vagy EU-rezidenciára utaló mondat. Ezt egy második, független (nem TypeSafe-tulajdonú) forrás is megerősíti:

> „Where the data goes. The product page says us-west. The privacy policy says the United States and nothing more."
(https://wunderlandmedia.com/typesafe-ai-jev-terms-of-service-gdpr, T3, Exa `web_search_exa`)

**A megdöntési kísérlet eredménye:** nem sikerült megdönteni. Nem találtam sem újabb (a Nov 19, 2025-ös verziónál frissebb) Privacy Policy-verziót, sem a Jev 2026-09-15-i indulása után közzétett bejelentést EU-hosztolásról. Egy állásajánlás (Ashby, SQ04-kör által idézve: „multi-region, multi-cloud” infrastruktúra-terv) jövőbeli szándékot jelezhet, de ez nem jelenlegi állapot, és ezt magam nem kerestem újra, mert nem elsődleges, jelenlegi állapotot igazoló forrás.

### 2. Nincs tanítás; nincs fix megőrzési idő

Privacy Policy, „Retention" szakasz (magam lekérve):

> „We retain personal data about you for as long as reasonably necessary to provide you with the Services, or otherwise in support of our business or commercial purposes. […] unless we are required by law to keep this data for a longer period."
(https://typesafe.ai/legal/privacy, T1, Exa `web_fetch_exa`)

Ugyanott, tanítási tilalom:

> „We will not train or fine tune any artificial intelligence or machine learning models on your prompts or other Input."
> „We (1) will not train or fine tune any artificial intelligence or machine learning models on Input, and (2) will not disclose any Input to a third party other than our service providers."
(https://typesafe.ai/legal/privacy, T1, Exa `web_fetch_exa`)

A DPA Schedule I ugyanezt a „nincs fix idő" mintát ismétli:

> „Customer Personal Data will be retained for as long as necessary taking into account the purpose of the Processing, and in compliance with applicable laws, including laws on the statute of limitations and Data Protection Law."
(https://typesafe.ai/legal/data-processing, T1, Exa `web_fetch_exa`)

Az MCA-t (Last updated Aug 27, 2026) és a ToS-t (Last updated Nov 19, 2025) is teljes terjedelmükben elolvastam: mindkettő megismétli a „nem tanítunk" ígéretet (az MCA 4.1-ben ügyfél-hozzájárulási kivétellel: „without Customer's prior consent"), és egyikben sincs számszerű megőrzési határidő.

**A megdöntési kísérlet eredménye:** nem sikerült megdönteni; a korábbi kör állítása szó szerint pontos.

### 3. Zero Data Retention — hiányzik a hivatalos oldalakról

Ebben a körben mind az öt hivatalos TypeSafe jogi dokumentumot (Privacy Policy, DPA, MCA, ToS, AUP) teljes terjedelmükben magam kértem le és olvastam el. Egyikben sem szerepel a „zero data retention" vagy „ZDR" kifejezés, sem szó szerint, sem körülírva.

A nem hivatalos ZDR-állítás továbbra is csak T3 forrásokból ismert, és ebben a körben egy második, a korábbitól eltérő T3 forrásban (beri.net, nem azonos a jevaiguide.com-mal) is megtaláltam ugyanezt az állítást:

> „Enterprise zero data retention. Contact for pricing. ✓ Zero data retention on request via privacy@typesafe.ai. ✓ Data Processing Agreement and Master Customer Agreement"
(https://www.beri.net/tools/typesafe-jev, T3, Exa `web_fetch_exa`)

> „Zero data retention on request. Enterprise customers can get ZDR by contacting privacy@typesafe.ai."
(https://jevaiguide.com/faq/does-jev-train-on-your-data/, T3, Exa `web_search_exa`)

Fontos korlát: nem zárható ki, hogy ez a két T3 forrás egymástól (vagy egy közös, nem azonosított sajtóanyagtól) másolja az információt — a két domain közötti tartalmi függetlenség nincs igazolva, csak a domain-tulajdonos különbözik. Emellett az Opper.ai gateway-monitoring oldal a TypeSafe közvetlen route-jára továbbra is „Not established" állapotot ír mindkét aljlapján:

> „Zero data retention posture is not established for this route. No training on customer data."
(https://opper.ai/provider/typesafe és https://opper.ai/typesafe, T3, Exa `web_search_exa`)

**A megdöntési kísérlet eredménye:** nem sikerült megdönteni — sőt, a saját, teljes körű újraolvasásom megerősítette az öt dokumentum mindegyikére nézve, hogy a ZDR kifejezés hivatalosan sehol nem szerepel.

### 4. DPA (SCC + UK Addendum), DPF-lista, SOC 2, alfeldolgozók

**SCC és UK Addendum** — a DPA-t magam kértem le, 6.1–6.3 szakasz, szó szerint:

> „6.1. Data Transfers. […] pursuant to (a) the contractual clauses annexed to the European Commission's Implementing Decision 2021/914 of 4 June 2021 […] (“EU SCCs”) or (b) the International Data Transfer Addendum to the EU Commission Standard Contractual Clauses issued by the UK Information Commissioner, Version B1.0, in force 21 March 2022 […] (“UK Addendum”)."
> „6.2. EU Data Transfers. […] Typesafe and Customer conclude Module 2 (controller-to-processor) of the EU SCCs and, if Customer is a processor on behalf of a third-party controller, Module 3 (Processor-to-Subprocessor) […]"
(https://typesafe.ai/legal/data-processing, T1, Exa `web_fetch_exa`) — **ez pontosan megerősíti** az SQ04-állítást.

**DPF-lista hiánya** — magam is megpróbáltam ellenőrizni a `dataprivacyframework.gov/list` hivatalos oldalt (Exa `web_fetch_exa` és `web_search_exa`, több URL-variánssal, pl. `?search=typesafe` paraméterrel is). Az eredmény minden esetben ugyanaz volt: a dinamikus, klasszikus ABC-sorrendű lista eleje (AiSDR, DevRev, [24]7.ai, 11:11 Systems stb.), keresési szűrő nélkül — a `?search=` paraméteres URL-ek lekérése hibát dobott. **Én magam sem tudtam a „TypeSafe" névre szűrt listát elérni.** Ez azt jelenti, hogy az egyetlen konkrét állítás — miszerint a TypeSafe nincs a listán, és a „T" betű alatti 232 aktív résztvevő közül a legközelebbi találat a „Tynker" — továbbra is **kizárólag egyetlen, nem hivatalos forrásból (Wunderlandmedia)** ismert:

> „And TypeSafe is not certified under the EU-US Data Privacy Framework. I checked rather than assumed: the search box on dataprivacyframework.gov is broken, so I paged all 232 active participants under the letter T. The closest entry is Tynker."
(https://wunderlandmedia.com/typesafe-ai-jev-terms-of-service-gdpr, T3, Exa `web_search_exa`)

**Verdikt erre a részre: NEM ELDÖNTHETŐ** — sem megerősíteni, sem megdönteni nem tudtam két független forrással; a saját önálló kísérletem is ugyanabba a technikai korlátba ütközött, amit az SQ04-kör is jelzett.

**SOC 2 Type II** — a vita mindkét oldalára találtam **újabb, független megerősítést**, ami a korábbinál szilárdabbá teszi magát az ellentmondást (nem oldja fel, de igazolja, hogy nem egyetlen forrás hibájáról van szó):

*„Igen" oldal, két különböző személy, azonos napon:*
> „At 11:39am I received the second most important Slack message I've received today — TypeSafe AI had officially become SOC 2 Type II compliant. […] thank our incredible partners, Vanta and Advantage Partners…"
(https://www.linkedin.com/posts/typesafe-ai_activity-7480343405286313984-qWxZ, TypeSafe AI hivatalos oldal, 2026-07-07, T1 céges közlés)
> „TypeSafe is officially SOC2 Compliant! Big thanks to Elise Liu, Kevin Zhang, Noam Samuel, Nathan LeClaire and Vanta for making it happen."
(https://www.linkedin.com/posts/erik-spock-gafni-906b0125_typesafe-is-officially-soc2-compliant-big-activity-7480371326176763905-lA3K, Erik Spock Gafni, TypeSafe AI társalapító-CTO, 2026-07-07, T1 céges közlés, Exa `web_search_exa`)

*„Nem" oldal, két különböző, egymástól független harmadik fél:*
> „TypeSafe AI has not published SOC 2, ISO 27001, or other third-party compliance certifications."
(https://hokai.io/hub/companies/typesafe-ai, T2/T3, Exa `web_search_exa` — az SQ04-körből átvéve, ebben a körben nem kérdeztem le újra)
> „Regulated buyers who need SOC 2 or HIPAA attestations, SSO or a self-hosted deployment today; none are published…" / „Security & Compliance: ✗ soc2 ✗ gdpr ✗ hipaa ✗ iso27001 ✗ sso ✗ data residency"
(https://www.beri.net/tools/typesafe-jev, T3, Exa `web_fetch_exa`)

Egy lehetséges (nem bizonyított) magyarázat a feszültségre, amit a Wunderlandmedia-forrás vet fel, és amit a Trust Center JS-korlátja miatt sem megerősíteni, sem cáfolni nem tudtam: a SOC 2-jelentés létezhet, de „request access” gomb mögé zárva:

> „…the SOC 2 report behind that link sits behind a 'Request access' button."
(https://wunderlandmedia.com/typesafe-ai-jev-terms-of-service-gdpr, T3)

**Verdikt erre a részre: RÉSZBEN IGAZOLVA** — az ellentmondás valós és két oldalról is (2+2 forrás) alátámasztott, de nem feloldható; a „nem publikált” és a „megszerezte, de hozzáférés-kéréshez kötött” állítások technikailag nem zárják ki egymást.

**Alfeldolgozók (AWS, Modal, Slack, Google Workspace)** — a hivatalos `trust.typesafe.ai/subprocessors` oldalt magam is lekértem: ugyanúgy, mint az SQ04-kör, én is csak az üres, Vanta-JavaScript-tel renderelt HTML-vázat kaptam vissza, tartalom nélkül. **Ebben a körben viszont egy második, a Wunderlandmediától független T3 forrást is találtam**, amely ugyanazt a négyes listát írja le, láthatóan önállóan (más megfogalmazással, más cikk-struktúrában):

> „The Trust Center identifies several subprocessors: Amazon Web Services stores and processes live-request customer information in the United States. Modal processes customer AI prompts on managed compute; TypeSafe's listing says Modal does not store those prompts. Slack and Google Workspace may process customer information used for support and collaboration."
(https://www.findmilan.ca/blog/typesafe-ai-jev-system-one-model-automation-guide, T3, Exa `web_fetch_exa`)

> „The subprocessors, verified from the page: AWS stores and processes live request data, Modal processes prompts without storing them and is the one running inference, and Slack and Google Workspace handle support."
(https://wunderlandmedia.com/typesafe-ai-jev-terms-of-service-gdpr, T3, Exa `web_search_exa`)

**Verdikt erre a részre: RÉSZBEN IGAZOLVA, magasabb bizonyossággal, mint az SQ04-kör állította** — két, egymástól függetlennek tűnő T3 forrás egyezik meg pontosan ugyanazon négy cégben, de a hivatalos, elsődleges (TypeSafe Trust Center) oldal tartalmát én sem tudtam elolvasni, tehát TypeSafe-saját, elsődleges megerősítés továbbra sincs.

### 5. OpenRouter, Vercel AI Gateway és Cloudflare adatkezelése

**OpenRouter** — a hivatalos, gépileg lekérdezhető ZDR-listát (`https://openrouter.ai/api/v1/endpoints/zdr`) magam kértem le `curl`-lal (2026-09-25, ma), és Python-nal szűrtem a 916 bejegyzés között „typesafe" kulcsszóra. Pontosan egy találat volt:

> `{"name": "TypeSafe | typesafe/jev-1.13-20260917", "model_id": "typesafe/jev-1.13", "provider_name": "TypeSafe", …}`
(https://openrouter.ai/api/v1/endpoints/zdr, T1, `curl`, nyers JSON, magam lekérve és elemezve, 2026-09-25)

Ez közvetlen, elsődleges, gépi bizonyíték arra, hogy az OpenRouter a Jev végpontot ZDR-képesnek minősíti.

**Vercel AI Gateway** — a hivatalos changelog-oldalt (nem csak a highlightját, a teljes oldalt) magam kértem le:

> „Jev supports Zero Data Retention and No Training, enabled per request in the example. Evaluation calls also appear in logs and custom reporting, count toward budgets, and accept other Gateway provider options in the same `providerOptions.gateway` object."
(https://vercel.com/changelog/typesafe-ai-jev-now-available-on-ai-gateway, T1, Exa `web_fetch_exa`, Published: September 16, 2026)

A kódpélda is szó szerint tartalmazza a `providerOptions: { gateway: { zeroDataRetention: true } }` mezőt Jev-hívásra.

**Cloudflare** — a Workers AI hivatalos adatkezelési oldalát (`developers.cloudflare.com/workers-ai/platform/data-usage/`) magam kértem le, Last updated Apr 21, 2026:

> „Cloudflare neither creates nor trains the AI models made available on Workers AI. […] Cloudflare does not use your Customer Content to (1) train any AI models made available on Workers AI or (2) improve any Cloudflare or third-party services, and would not do so unless we received your explicit consent."
(https://developers.cloudflare.com/workers-ai/platform/data-usage/, T1, Exa `web_fetch_exa`)

Ezen az oldalon, sem az oldal többi részén, **nincs** Jev-specifikus vagy modell-specifikus „ZDR" címke, csak ez az általános, minden Workers AI-modellre vonatkozó „nem tanítunk" ígéret.

**A megdöntési kísérlet eredménye:** nem sikerült megdönteni — mindhárom gateway-re vonatkozó állítás közvetlen, elsődleges forrásból, ma lekérve, szó szerint megerősíthető.

### 6. (SQ06) `opossum` függőségek, LiteLLM „silently rerouted", AWS rate limit

**`opossum` — 0 futásidejű függőség.** Az npm-regisztráció nyers JSON-ját (`registry.npmjs.org/opossum/latest`) magam kértem le `curl`-lal, majd Python-nal ellenőriztem:

> `version: 10.0.0` — `has dependencies key: False` — `dependencies value: None` — `devDependencies count: 23`
(https://registry.npmjs.org/opossum/latest, T1, `curl`, nyers JSON, magam lekérve és elemezve)

Vagyis a csomag `package.json`-jában **nincs is `dependencies` mező** — ez technikailag még az SQ06-kör „0 Dependencies" állításánál is erősebb megerősítés (nem csak nulla elemű a lista, a mező maga hiányzik), miközben a 23 `devDependencies`-bejegyzés (build-/tesztidejű, nem futásidejű) létezik.

**LiteLLM — „silently rerouted".** A hivatalos dokumentációs oldalt (`docs.litellm.ai/docs/proxy/budget_fallbacks`) magam kértem le teljes terjedelmében:

> „By default `model_max_budget` blocks requests once a key's spend on a model crosses its cap. `budget_fallbacks` lets you configure a per-model fallback chain on the key itself, so the request is silently rerouted to the first fallback that still has budget remaining. Spend is attributed to the fallback model, not the exhausted one."
(https://docs.litellm.ai/docs/proxy/budget_fallbacks, T1, Exa `web_fetch_exa`)

A „silently rerouted" kifejezés szó szerint, pontosan így szerepel a hivatalos dokumentációban.

**AWS — a rate limit nem megbízható költségkorlát.** A hivatalos API Gateway dokumentációt (`docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html`) magam kértem le:

> „Usage plan throttling and quotas are not hard limits, and are applied on a best-effort basis. In some cases, clients can exceed the quotas that you set. Don't rely on usage plan quotas or throttling to control costs or block access to an API. Consider using AWS Budgets to monitor costs and AWS WAF to manage API requests."
(https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html, T1, Exa `web_fetch_exa`)

**A megdöntési kísérlet eredménye:** egyik alállítást sem sikerült megdönteni; mindhárom szó szerint, elsődleges forrásból, ma, önállóan megerősíthető.

---

## Amit ez a döntésre jelent

1. Az EU-hosztolás hiánya és a fix megőrzési idő hiánya (1–2. állítás) a TypeSafe öt hivatalos jogi dokumentumának teljes, önálló újraolvasásával is megerősítést nyert — ez a réteg a döntéshozatalban stabil, nem vitatott alapnak tekinthető.
2. A „zero data retention" kifejezés egyetlen hivatalos TypeSafe-dokumentumban sem szerepel (ezt ötből öt dokumentum teljes elolvasásával ellenőriztem) — bármilyen ZDR-re épülő tervezési döntés a TypeSafe közvetlen API-ján csak egyedi, nem nyilvános, e-mailben egyeztetett megállapodásra támaszkodhatna, nem publikus szabályzatra.
3. A gateway-rétegek (OpenRouter, Vercel) ZDR-állítása ezzel szemben ma, élő, gépileg lekérdezhető, elsődleges forrásból megerősíthető a Jev végpontra — ez azt jelenti, hogy egy ZDR-igényű integrációnak technikailag van azonnal ellenőrizhető, dokumentált útja (gateway-en át), míg a közvetlen TypeSafe API-n nincs.
4. A DPF-lista kérdése továbbra is nyitott: sem az SQ04-kör, sem ez a kör nem tudta a kormányzati oldalt önállóan, a TypeSafe névre szűrve lekérdezni; az egyetlen konkrét „nincs rajta" állítás egyetlen, nem hivatalos forrásból származik, függetlenül nem megerősített.
5. A SOC 2 Type II léte körüli ellentmondás nem egyetlen blogger tévedése: két, a céghez köthető, egymástól független személy (CEO-oldal, illetve a társalapító-CTO saját posztja) állítja a megszerzését ugyanazon a napon, míg két, egymástól független, harmadik fél véleménye szerint nincs publikált SOC 2/ISO 27001-tanúsítvány — ez egy „megszerzett, de nem publikusan hozzáférhető" állapottal összeegyeztethető, de erre sincs elsődleges megerősítés.
6. Az alfeldolgozó-lista (AWS, Modal, Slack, Google Workspace) immár két, egymástól láthatóan független harmadik feles forrásból egyezik — ez erősebb bizonyíték, mint amit az SQ04-kör talált, de a hivatalos, elsődleges Trust Center-oldal (JavaScript-renderelt) tartalma továbbra sem olvasható ki sem az SQ04-, sem ebben a körben.

---

## Meglátogatott linkek

| Cím | URL | Tier | Eszköz |
|---|---|---|---|
| Privacy policy — TypeSafe AI | https://typesafe.ai/legal/privacy | T1 | Exa web_fetch_exa |
| Data processing addendum — TypeSafe AI | https://typesafe.ai/legal/data-processing | T1 | Exa web_fetch_exa |
| Master customer agreement — TypeSafe AI | https://typesafe.ai/legal/mca | T1 | Exa web_fetch_exa |
| Terms of Service — TypeSafe AI | https://typesafe.ai/terms-and-conditions | T1 | Exa web_fetch_exa |
| Acceptable Use Policy — TypeSafe AI | https://typesafe.ai/legal/acceptable-use-policy | T1 | Exa web_fetch_exa |
| Typesafe.ai Trust Center — subprocessors | https://trust.typesafe.ai/subprocessors | T1 (tartalom nem olvasható) | Exa web_fetch_exa |
| Typesafe.ai Trust Center (főoldal) | https://trust.typesafe.ai/ | T1 (tartalom nem olvasható) | Exa web_fetch_exa |
| TypeSafe AI Jev Terms of Service: EU Read — Wunderlandmedia | https://wunderlandmedia.com/typesafe-ai-jev-terms-of-service-gdpr | T3 | Exa web_search_exa |
| TypeSafe AI Jev Review: Features, Cost & Limits — findmilan.ca | https://www.findmilan.ca/blog/typesafe-ai-jev-system-one-model-automation-guide | T3 | Exa web_fetch_exa |
| TypeSafe Jev — THE D*AI*LY BRIEF (beri.net) | https://www.beri.net/tools/typesafe-jev | T3 | Exa web_fetch_exa |
| TypeSafe AI: The Company Behind Jev — Jev AI Guide | https://jevaiguide.com/typesafe-ai/ | T3 | Exa web_search_exa |
| Does Jev Train on Your Data? — Jev AI Guide | https://jevaiguide.com/faq/does-jev-train-on-your-data/ | T3 | Exa web_search_exa |
| TypeSafe AI — HokAI | https://hokai.io/hub/companies/typesafe-ai | T2/T3 | Exa web_search_exa |
| TypeSafe AI — Opper.ai (provider) | https://opper.ai/provider/typesafe | T3 | Exa web_search_exa |
| TypeSafe AI — Opper.ai (typesafe) | https://opper.ai/typesafe | T3 | Exa web_search_exa |
| TypeSafe AI LinkedIn — SOC 2 Type II bejelentés (céges oldal) | https://www.linkedin.com/posts/typesafe-ai_activity-7480343405286313984-qWxZ | T1 (céges közlés) | Exa web_search_exa |
| Erik Spock Gafni LinkedIn — SOC 2 bejelentés | https://www.linkedin.com/posts/erik-spock-gafni-906b0125_typesafe-is-officially-soc2-compliant-big-activity-7480371326176763905-lA3K | T1 (céges közlés) | Exa web_search_exa |
| typesafe ai — LinkedIn cégoldal | https://linkedin.com/company/typesafe-ai | T1 | Exa web_search_exa |
| Data Privacy Framework List (hivatalos) | https://www.dataprivacyframework.gov/list | T1 (nem szűrhető) | Exa web_fetch_exa + web_search_exa |
| Data Privacy Framework List, search paraméterrel (sikertelen) | https://www.dataprivacyframework.gov/list?search=typesafe | T1 (elérhetetlen) | Exa web_fetch_exa |
| Zero Data Retention (ZDR) endpoints — OpenRouter (nyers JSON) | https://openrouter.ai/api/v1/endpoints/zdr | T1 | curl (nyers fájl), saját lekérdezés és elemzés, 2026-09-25 |
| AI Gateway Zero Data Retention (ZDR) — Vercel | https://vercel.com/docs/ai-gateway/security-and-compliance/zdr | T1 | Exa web_fetch_exa |
| TypeSafe AI's Jev now available on AI Gateway — Vercel changelog | https://vercel.com/changelog/typesafe-ai-jev-now-available-on-ai-gateway | T1 | Exa web_fetch_exa |
| Your Data and Workers AI — Cloudflare Workers AI docs | https://developers.cloudflare.com/workers-ai/platform/data-usage/ | T1 | Exa web_fetch_exa |
| opossum — npm regisztráció (registry.npmjs.org, nyers JSON) | https://registry.npmjs.org/opossum/latest | T1 | curl (nyers fájl), saját lekérdezés és elemzés |
| Budget Fallbacks — LiteLLM docs | https://docs.litellm.ai/docs/proxy/budget_fallbacks | T1 | Exa web_fetch_exa |
| Usage plans and API keys for REST APIs — AWS API Gateway docs | https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html | T1 | Exa web_fetch_exa |
| sq04-adatvedelem.md (előző kutatási kör) | /home/claude/work/kutatas-jev/sq04-adatvedelem.md | — | Read (helyi fájl) |
| sq06-kapcsolo-visszaallas.md (előző kutatási kör) | /home/claude/work/kutatas-jev/sq06-kapcsolo-visszaallas.md | — | Read (helyi fájl) |
| _ell_kozos.txt (közös adverzariális instrukció) | /home/claude/work/kutatas-jev/_ell_kozos.txt | — | Read (helyi fájl) |
