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
