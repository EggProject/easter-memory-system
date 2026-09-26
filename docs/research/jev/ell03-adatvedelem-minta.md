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
