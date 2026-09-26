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
