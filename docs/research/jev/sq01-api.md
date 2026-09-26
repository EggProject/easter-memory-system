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
