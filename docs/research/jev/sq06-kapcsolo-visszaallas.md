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
