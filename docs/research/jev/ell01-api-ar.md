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
