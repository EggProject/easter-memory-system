# Kivonat — projekt-kontextus (honnan tudja a rendszer a projektet, hová kerül egy új bejegyzés)

Kutatási egységenként, szó szerinti idézetekkel. SQ01–SQ04 és ELL01–ELL03: az első kör (projekt, írási szint, keresés);
SQ05–SQ08 és ELL04–ELL06: a második kör (mi kerüljön a hookon át az agent elé). Minden
keresés az Exa eszközzel. A linkek a `linkek.md`-ben, a szintézis a `SZINTEZIS.md`-ben.

**Javítások az ellenőrzés után:** (1) a „projektszintű konfiguráció felülírja a globálist" csak három kliensnél dokumentált
egyértelműen (Claude Code, Gemini CLI, Codex), a Copilotnál egy hivatalos hibajegy a fordítottját mutatja (ELL01/5);
(2) a Claude Code hook-kimenetének dokumentált korlátja 10 000 karakter, de a modellhez több független mérés szerint kb.
2000 karakter jut el (ELL01/7); (3) a „a model that can name its own tenant…" mondat csak az `opspresso/mcp-memory`
README-jében áll, nem a Zep dokumentációjában (ELL02/2); (4) a CIMemories-számoknál a cikk és a kódtár eltérő modellnevet
ad (ELL02/6); (5) a mem0 hatókör-hibáiból hármat javítottak, egy rokon eset nyitott; a Claude Code git-repó szintű
memória-megosztását a gyártó szándékosnak nevezte; a #40541 egyetlen, ki nem vizsgált beszámoló (ELL03).
Az egyik ellenőrző kör (ELL02 első indítása) API-hiba miatt leállt; két, szűkebb körre bontva újrafutott.
**A második kör javításai:** (6) a Gemini CLI-ben ma nincs `save_memory` eszköz, a modell közvetlenül a fájlt szerkeszti
(ELL04/8); (7) az eszközhívási hajlandóság forrásolt tartománya 7–83%, nem 7–98% (ELL05/2); (8) az SQ06 „nincs
kontrollált mérés" állítását az arXiv:2607.20972 pontosítja (ELL05/1); (9) a GSM-IC „18%"-a 2023-as modellekre szól
(ELL05/4); (10) a MEMTRACK a NeurIPS 2025 workshop-sávjában jelent meg (ELL06/2); (11) a „6–11 pp" egyetlen kutatás két
megjelenése (ELL06/7).

---

# SQ01 — Mit ad az MCP-specifikáció arra, hogy a szerver megtudja a kliens munkakörnyezetét (projektjét)?

**Módszer megjegyzése:** A kutatást egyetlen ügynökként, alügynökök indítása nélkül végeztem (a `deep-web-research` skill elvei szerint, degradált módban — a jelen munkamenet maga egy alügynök egy nagyobb kutatási feladatban, további alügynökök indítására nem volt mód). Kizárólag az Exa `web_search_exa` / `web_fetch_exa` eszközöket használtam keresésre és oldalolvasásra, a beépített WebSearch/WebFetch-et nem.

## Rövid válasz

A **Roots** képesség létezik még a 2026-07-28-as MCP-specifikációban, de **hivatalosan deprecated** (SEP‑2577, Final státusz): fájlrendszer-`file://`-URI-kat és opcionális nevet ad át, a szerver kéri le a klienstől, és a korábbi önálló szerver→kliens JSON‑RPC kérés helyett a 2026-07-28-as stateless modellben a Multi Round‑Trip Requests (MRTR) mintába ágyazva, egy `InputRequiredResult`-on belüli `roots/list` kérésként érkezik — tehát **nem** megy minden kérésben automatikusan, hanem a szerver kérésére, esetenként. A `_meta` mező a hivatalos, kiterjeszthető csatorna kérésenkénti metaadatokra; a 2026-07-28 verzióban minden kérés kötelezően hordozza a `io.modelcontextprotocol/protocolVersion` és `io.modelcontextprotocol/clientCapabilities` mezőket `_meta`-ban, emellett HTTP-n a `Mcp-Method`/`Mcp-Name` fejlécek és az opcionális, tool-paraméterből származtatott `x-mcp-header`/`Mcp-Param-*` fejlécek adnak kérésenkénti, útvonalválasztásra használható kontextust — de nincs beépített „projekt" vagy „workspace" `_meta`-kulcs. Az **Elicitation** funkció (nem deprecated) lehetővé teszi, hogy a szerver form-módban strukturált adatot (pl. egy projekt-enumot) kérjen vissza a felhasználótól, ugyanazon MRTR-mintán keresztül; érzékeny adatra (jelszó, token) tilos form-módot használni. **Nincs Final SEP** vagy hivatalos útmutatás arra, hogyan válasszon hatókört (tenant/projekt) egy több-bérlős távoli MCP-szerver — a legközelebbi hivatalos válasz a SEP‑2567 („Sessionless MCP via Explicit State Handles"), amely kifejezetten kimondja, hogy az ilyen állapot **nem protokollszintű fogalom**, hanem „tool-design pattern": a szervernek explicit tool-argumentumként (pl. egy `project_id` handle-ként) kell átvinnie. Az **OAuth `resource` paraméter** (RFC 8707) a kanonikus MCP-szerver-URI-t azonosítja és útvonal-komponenssel megkülönböztethető, míg a **scope-ok** a specifikáció szerint kifejezetten *nem* a hely/erő-azonosításra valók („Scope is typically about what access is being requested rather than where that access will be redeemed") — projekt-szintű elkülönítés így inkább külön kanonikus resource-URI-kkal (= gyakorlatilag külön OAuth-erőforrásokkal), mintsem scope-okkal illeszkedik a specifikációhoz, bár a 2026-07-28 revízió már formálisan előírja a scope-hierarchiák kezelését is.

---

## 1. Roots a 2026-07-28-as verzióban

### Létezik-e még, és mit ad át

A Roots típus és metódusai **a séma szerint még jelen vannak**, csak deprecated jelöléssel:

> „* **Roots** (`roots/list`, `notifications/roots/list_changed`) ... These features are deprecated starting in the specification version that includes this SEP (expected June 2026). They will continue to be fully functional in all specification versions released within one year of that version's release."
(SEP‑2577, https://modelcontextprotocol.io/seps/2577-deprecate-roots-sampling-and-logging)

Amit átad — a `Root` típus (2024-11-05-ös séma, azóta változatlan a mezőket illetően):

> „export interface Root {
> /** The URI identifying the root. This *must* start with file:// for now. ... */
> uri: string;
> /** An optional name for the root. ... */
> name?: string;
> }"
(https://github.com/modelcontextprotocol/specification/blob/main/schema/2024-11-05/schema.ts)

A 2026-07-28-as (draft/mintlify-tükrözött) leírás megerősíti, hogy az URI-korlátozás máig érvényes:

> „`uri`: Unique identifier for the root. This MUST be a `file://` URI in the current specification. ... `name`: Optional human-readable name for display purposes."
(https://mcp.mintlify.app/specification/draft/client/roots)

Fontos: egy külön SEP (**SEP‑2202**, „Allow Non-File URI Schemes for Roots") pont ezt a korlátot akarta feloldani, de a szerzője szüneteltette, mert a Roots időközben deprecation-útra került:

> „1. To make this genuinely usable, we'd need to solve the race condition problem in the spec. 2. Demand for something like Roots seems limited... 3. Roots is reportedly on a proposed deprecation path. ... I'd like to officially pause this SEP" — majd egy hozzászólás: „roots are deprecated in #2577"
(https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2202)

### Ki kéri le kitől, mikor

A `ListRootsRequest` a specifikáció szerint mindig **szerver → kliens** irányú (a kliens birtokolja a roots-listát):

> „Sent from the server to request a list of root URIs from the client. Roots allow servers to ask for specific directories or files to operate on."
(https://github.com/modelcontextprotocol/specification/blob/main/schema/2024-11-05/schema.ts)

Ez a 2026-07-28-as revízióban is így marad *logikailag* — csak a szállítási mechanizmus változik (lásd alább).

### Hogyan működik a stateless (munkamenet nélküli) modellben

**Nem** megy minden kérésben automatikusan. A kliens `_meta.io.modelcontextprotocol/clientCapabilities.roots` mezőben **képességet** jelez minden kéréssel (hogy támogatja a roots-ot), de a tényleges roots-*adat* csak akkor utazik, amikor a szerver ténylegesen kéri, és ekkor is az új Multi Round-Trip Requests (MRTR) mintán keresztül, nem önálló szerver-kezdeményezésű JSON-RPC hívásként:

> „On a 2026-07-28 connection there is no server-to-client request channel; the same handler fulfils a `roots/list` request embedded in an `input_required` result — see Protocol versions."
(TypeScript SDK, https://ts.sdk.modelcontextprotocol.io/v2/clients/roots.html)

A mechanizmus konkrétan: a szerver — amikor egy `tools/call` (vagy más) kérés feldolgozása közben szüksége van a roots-listára — egy `InputRequiredResult`-tal válaszol, amelynek `inputRequests` mezője tartalmazza a `roots/list` kérést; a kliens begyűjti a választ, majd **megismétli az eredeti kérést**, csatolva az `inputResponses`-t:

> „To retrieve roots during the processing of a client request, servers send an `InputRequiredResult` containing a `roots/list` request: ... Input request (delivered inside `InputRequiredResult.inputRequests`): `{ "method": "roots/list" }` ... Client result (returned inside `inputResponses` on the retried request): `{ "roots": [ { "uri": "file:///home/user/projects/myproject", "name": "My Project" } ] }`"
(https://mcp.mintlify.app/specification/draft/client/roots)

A Go SDK dokumentációja ugyanezt a mechanizmust írja le általánosan (nemcsak roots-ra, hanem sampling/elicitation-re is):

> „SEP-2322 introduces the MRTR pattern: server-to-client requests for sampling, elicitation, and roots are no longer issued as fresh JSON-RPC requests but are carried inside the in-flight reply of a `tools/call`, `prompts/get`, or `resources/read`. The client must respond by retrying the original request with the produced responses."
(https://go.sdk.modelcontextprotocol.io/client/)

A C# SDK explicit megmondja, hogy a klasszikus szerver-kezdeményezésű lekérdezés **statikus (stateless) módban nem működik**, kizárólag az MRTR-változat:

> „`RequestRootsAsync` throws `InvalidOperationException(\"Roots are not supported in stateless mode.\")` whenever the server is running stateless — including every Streamable HTTP request served under `2026-07-28`. ... For code that needs to run on stateless servers — including `2026-07-28` Streamable HTTP — throw `InputRequiredException` from your handler instead."
(https://csharp.sdk.modelcontextprotocol.io/v2/concepts/roots/roots.html)

A Python SDK ezt egy hibakóddal is megerősíti (ha a kliens nem deklarálta a képességet, a hívás nem is megy ki):

> „The gate is the same as for sampling: without a declared `roots` capability the call fails with `-32021` instead of sending the request."
(https://py.sdk.modelcontextprotocol.io/handlers/sampling-and-roots/index.md)

**Összefoglalva a stateless kérdésre:** a *képesség*-deklaráció (hogy a kliens *tudna* roots-ot adni) minden kérésben ott van a `_meta`-ban; maga a *roots-lista tartalma* viszont csak kérésre, az adott hívás MRTR-körén belül utazik — nem egy általános, minden kérésre rárakódó kontextus-mező.

### Mi változott a korábbi verziókhoz képest

- **2024-11-05 → 2025-06-18 → 2025-11-25:** a Roots kapacitás és a `Root` típus tartalma (csak `file://` URI + opcionális `name`) lényegében változatlan maradt; a 2025-11-25-ös kliens-oldali roots-oldal ugyanazt a `roots/list` kérés/`notifications/roots/list_changed` mintát írja le, mint a 2024-11-05-ös séma:

  > „Clients that support roots MUST declare the `roots` capability during initialization: ... To retrieve roots, servers send a `roots/list` request... When roots change, clients that support `listChanged` MUST send a notification: `notifications/roots/list_changed`"
  (https://modelcontextprotocol.io/specification/2025-11-25/client/roots)

- **2026-04-14:** SEP‑2577 létrejön (Kurtis Van Gent), amely Roots + Sampling + Logging deprecation-jét javasolja, alacsony adopcióra és „vague semantics"-re hivatkozva:

  > „Roots provides \"informational guidance\" about which directories or files a server should operate on. In practice: * **Low adoption**: Few clients implement roots support... * **Vague semantics**: The specification describes roots as informational — servers are not required to respect them, which reduces their utility. * **Overlapping alternatives**: Working directory context can be provided through tool parameters, resource URIs, server configuration, or environment variables — all of which are more explicit."
  (https://modelcontextprotocol.io/seps/2577-deprecate-roots-sampling-and-logging)

- **2026-07-28 (végleges kiadás):** a fenti deprecation + a szállítási mechanizmus MRTR-re cserélése (SEP‑2322) + a session/`initialize` teljes eltávolítása (SEP‑2575) lép életbe egyszerre; a hivatalos changelog egy tételben sorolja fel:

  > „Multi Round-Trip Requests (MRTR) pattern introduced which replaces the previous approach of sending server-initiated requests, such as `roots/list`, `sampling/createMessage`, or `elicitation/create`. Servers return an `InputRequiredResult` (`resultType: \"input_required\"`) whose `inputRequests` field carries the requests for the additional information needed to process the request. Clients respond with `inputResponses` on a retry of the original request providing the requested information. (SEP-2322)."
  (https://modelcontextprotocol.io/specification/2026-07-28/changelog)

- A hivatalos ajánlott migrációs irány kifejezetten a workspace/projekt-kontextus explicit átadására mutat:

  > „Suggested migrations: pass directories or files via tool parameters, resource URIs, or server configuration instead of Roots..."
  (https://modelcontextprotocol.io/specification/2026-07-28/changelog)

- A deprecation **nem** jelent azonnali törlést; a wire-protokoll a leértékelési ablakban változatlan:

  > „These features remain fully functional during the deprecation window but new implementations should not add support for them."
  (https://modelcontextprotocol.io/specification/2026-07-28/changelog)

---

## 2. `_meta` és más kérésenkénti kontextusátadás

A `_meta` a hivatalos, kiterjeszthető metaadat-mechanizmus kliens és szerver között, kulcsnév-szabályokkal és fenntartott prefixekkel:

> „The `_meta` property/parameter is used by MCP to allow clients and servers to attach additional metadata to their interactions. ... Any prefix where the second label is `modelcontextprotocol` or `mcp` is reserved for MCP use."
(https://modelcontextprotocol.io/specification/2026-07-28/basic/index)

A 2026-07-28-as stateless modellben **minden kérés kötelezően** hordozza a protokollverziót és a kliens-képességeket `_meta`-ban (a korábbi, egyszeri `initialize` helyett):

> „Client requests carry the following `io.modelcontextprotocol/*` fields in `_meta`; fields marked as required MUST be included on every request. ... | `io.modelcontextprotocol/protocolVersion` | `string` | Yes | ... | `io.modelcontextprotocol/clientInfo` | `Implementation` | No | ... | `io.modelcontextprotocol/clientCapabilities` | `ClientCapabilities` | Yes | ..."
(https://modelcontextprotocol.io/specification/2026-07-28/basic/index)

A séma (TypeScript) szerint ezek típusa és kötelezősége pontosan definiált, és a `clientCapabilities` kifejezetten *nem* öröklődik a korábbi kérésekből:

> „Capabilities are declared per-request rather than once at initialization; an empty object means the client supports no optional capabilities. Servers MUST NOT infer capabilities from prior requests."
(schema/2026-07-28/schema.ts, https://modelcontextprotocol.io/specification/2026-07-28/basic/index)

Fenntartott, hivatalos `_meta` kulcsok listája (2026-07-28): `progressToken`, `io.modelcontextprotocol/protocolVersion`, `io.modelcontextprotocol/clientInfo`, `io.modelcontextprotocol/clientCapabilities`, `io.modelcontextprotocol/logLevel` (maga is deprecated), `io.modelcontextprotocol/subscriptionId`, valamint OpenTelemetry-kontextus (`traceparent`, `tracestate`, `baggage`) — **projekt- vagy workspace-azonosításra szolgáló kulcs nincs közöttük**:

> „| `traceparent`, `tracestate`, `baggage` | OpenTelemetry trace context propagation |"
(https://modelcontextprotocol.io/specification/2026-07-28/basic/index)

A `clientInfo`/`serverInfo` mezőkről a spec kifejezetten kimondja, hogy **nem biztonsági döntésre valók**, csak megjelenítésre/naplózásra:

> „The value is self-reported by the client and is not verified by the protocol. It is intended for display, logging, and debugging. Servers SHOULD NOT use it to change their behavior, and SHOULD NOT rely on it for security decisions."
(schema/2026-07-28/schema.ts)

### HTTP-fejléc-alapú kontextus (SEP‑2243)

A Streamable HTTP kötésen a body bizonyos mezői kötelezően tükröződnek fejlécekbe (útvonalválasztás/ellenőrzés céljából — a body marad a forrás igazság):

> „A binding MAY additionally mirror selected body fields into envelope metadata. The Streamable HTTP transport mirrors them into HTTP headers so that intermediaries can route and inspect requests without parsing the body."
(https://modelcontextprotocol.io/specification/2026-07-28/basic/transports)

> „| `Mcp-Method` | `method` | All requests and notifications | | `Mcp-Name` | `params.name` or `params.uri` | `tools/call`, `resources/read`, `prompts/get` requests |"
(SEP‑2243, https://modelcontextprotocol.io/seps/2243-http-standardization)

Emellett a szerver **saját tool-argumentumait** is fejlécbe térképezheti (`x-mcp-header` kiterjesztés a tool `inputSchema`-jában), amit a kliensnek kötelező támogatnia — ez a legközelebbi hivatalos mechanizmus arra, hogy egy explicit paraméter (pl. egy `project`/`workspace` argumentum) a HTTP-rétegben is látható legyen útvonalválasztáshoz:

> „MCP servers MAY designate specific tool parameters to be mirrored into HTTP headers using an `x-mcp-header` extension property in the parameter's schema... Client Requirement: While the use of `x-mcp-header` is optional for servers, clients MUST support this feature."
(SEP‑2243, https://modelcontextprotocol.io/seps/2243-http-standardization)

Biztonsági korlátozás ugyanide: ez sem gondolt hitelesítésre/authorizációra —

> „Security guidance: intermediaries MUST NOT trust `Mcp-Param-*` for authorization decisions; tool authors SHOULD NOT mark sensitive params with `x-mcp-header`..."
(idézve a TS SDK implementációs jegyzetéből, https://github.com/modelcontextprotocol/typescript-sdk/issues/2190)

**Következtetés Q2-re:** a `_meta` és a fejlécek kérésenkénti, kiterjeszthető csatornát adnak, de a törzsspecifikáció nem definiál „aktuális projekt" kulcsot; ha egy szerver ilyet akar, saját (nem-`modelcontextprotocol`/`mcp` prefixű) `_meta` kulcsot kell definiálnia, vagy a paramétert explicit tool-argumentumként kell bekérnie.

---

## 3. Elicitation a 2026-07-28-as modellben

Az Elicitation **nem szerepel** a SEP‑2577 deprecation-listáján (csak Roots, Sampling, Logging), tehát élő, ajánlott mechanizmus maradt.

### Visszakérdezhet-e a szerver a felhasználótól

Igen, form- és URL-módban is:

> „The Model Context Protocol (MCP) provides a standardized way for servers to request additional information from users through the client during interactions. ... Elicitation supports two modes: - Form mode: Servers can request structured data from users with optional JSON schemas to validate responses - URL mode: Servers can direct users to external URLs for sensitive interactions that must not pass through the MCP client"
(https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation)

Form-módban a séma szándékosan lapos és primitív típusokra korlátozott (string/number/boolean/enum, egyszintű objektum) — ez pont elég egy „melyik projektbe írjam?" jellegű, enumos kérdéshez:

> „To simplify client user experience, form mode elicitation schemas are limited to flat objects with primitive properties only." ... „Note that complex nested structures, arrays of objects (beyond enums), and other advanced JSON Schema features are intentionally not supported to simplify client user experience."
(https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation)

### Korlátok

Érzékeny adatra kifejezett tiltás:

> „Servers MUST NOT use form mode elicitation to request sensitive information such as passwords, API keys, access tokens, or payment credentials. Servers MUST use URL mode for interactions involving such sensitive information."
(https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation)

A kliensnek kötelező UI-garanciákat nyújtania (melyik szerver kérdez, elutasítási lehetőség, form esetén áttekinthető/módosítható válasz, URL esetén cél domain megjelenítése + hozzájárulás):

> „MCP clients MUST: - Provide UI that makes it clear which server is requesting information - Respect user privacy and provide clear decline and cancel options - For form mode, allow users to review and modify their responses before sending - For URL mode, clearly display the target domain/host and gather user consent before navigation to the target URL"
(https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation)

A szállítás ugyanaz az MRTR-minta, mint a roots-nál; mivel a 2026-07-28-ban megszűnt a korábbi (2025-11-25-ös) `notifications/elicitation/complete` és `elicitationId`, a szervernek saját korrelációs azonosítót kell a `requestState`-be kódolnia:

> „Remove the `notifications/elicitation/complete` notification and the `elicitationId` field of URL mode elicitation requests, both introduced in `2025-11-25`. Under the Multi Round-Trip Requests pattern, the client learns the outcome of an out-of-band interaction by retrying the original request... Servers needing to correlate an elicitation across retries encode their own identifier in `requestState`."
(https://modelcontextprotocol.io/specification/2026-07-28/changelog)

### Kliensek támogatása

A kliensnek kérésenként kell deklarálnia a képességet, és legalább egy módot kötelező támogatnia, ha egyáltalán deklarálja:

> „Clients that support elicitation MUST declare the `elicitation` capability in `_meta.io.modelcontextprotocol/clientCapabilities` on each request... Clients declaring the `elicitation` capability MUST support at least one mode (`form` or `url`)."
(https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation)

A hivatalos, `modelcontextprotocol.io/clients` alatt élő „feature support matrix" — amit a GitHub `docs/clients.mdx`-ből olvastam ki — **nem tartalmaz Elicitation oszlopot** (csak Resources/Prompts/Tools/Sampling/Roots), ami arra utal, hogy ez a konkrét dokumentum-változat elavult/nem frissült az Elicitation (2025-06-18 óta létező) funkcióval — lásd „Ellentmondások". Egy közösségi (nem hivatalos, T2/T3) adatbázis, az `apify/mcp-client-capabilities`, viszont vezet Elicitation oszlopot (form, url), és klienspéldákat ad:

> „| Claude Code | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌, ❌ | ... | Cursor | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅, ❌ | ... | Visual Studio Code | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅, ✅ |"
(https://github.com/apify/mcp-client-capabilities — **T2/T3, közösségi, nem hivatalos forrás**, oszlopsorrend: Resources/Prompts/Tools/Discovery/Sampling/Tasks/Roots/Elicitation(form,url))

Ez a táblázat community-maintained, tehát csak kiegészítő (T2) jelleggel vehető figyelembe, és nem erősíthető meg két független elsődleges forrással — ezért ide sorolva marad.

---

## 4. Hivatalos útmutatás/SEP több-bérlős, több-projektes távoli MCP-szerverekre

**Nem található Final (elfogadott) SEP**, amely kifejezetten meghatározná, hogyan válasszon hatókört (tenant/projekt) egy futásidejű kérésnél egy több-bérlős, távoli MCP-szerver. A legközelebbi hivatalos anyagok:

### a) SEP‑2567 — explicit state handle mint hivatalos, deklarált minta

A legpontosabb, kifejezett hivatalos válasz arra, hogy a stateless protokollban a „melyik projektben dolgozunk" jellegű állapotot **nem a protokoll**, hanem a tool-tervezés hordozza:

> „Explicit state handles are not a new protocol construct — there is no schema or wire format for them. They are a tool-design pattern; the protocol change is the removal of sessions, which leaves handles as the way to express cross-call state."
(SEP‑2567, Final, https://modelcontextprotocol.org/seps/2567-sessionless-mcp)

> „Under this proposal, a server that currently scopes a shopping cart (for example) to the session instead exposes a tool `create_basket()` that returns a `basket_id` and threads that ID through subsequent tool calls, e.g. `add_item(basket_id, ...)`. The model decides what is shared and what is isolated..."
(uo.)

Ez közvetlenül alkalmazható analógia: egy memória-szerver esetén a „melyik projektbe írjunk" kérdés — a specifikáció szerint — nem oldható meg implicit munkamenet-kontextussal, csak explicit argumentumként (pl. `project_id` a `write_memory` hívásban), amit vagy a kliens/host tölt ki konfigurációból, vagy a szerver elicitation-nel kérdez vissza.

### b) OAuth `resource`-URI mint architekturális mintázat (nem nevesítve „projekt"-ként)

Az authorization-spec megengedi, hogy a kanonikus MCP-szerver-URI útvonal-komponenssel egyedi szervert/erőforrást azonosítson, ha egy hoszton több is fut:

> „`https://mcp.example.com/server/mcp` (when a path component is necessary to identify an individual MCP server)"
(https://modelcontextprotocol.info/specification/draft/basic/authorization/ — T2, nem hivatalos tükördomain, de a szöveg megegyezik a hivatalos 2026-07-28/2025-11-25 oldalak tartalmával, amit külön is megerősítettem)

Ezt a hivatalos 2026-07-28-as oldal is tartalmazza (ugyanaz a szöveg, hivatalos T1 forráson):

> „MCP clients SHOULD provide the most specific URI that they can for the MCP server they intend to access, following the guidance in RFC 8707."
(https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization)

Ez architekturálisan lehetővé teszi, hogy egy „projekt" külön kanonikus resource-URI-ként (= OAuth-szempontból külön erőforrásként) legyen modellezve, saját audience-re kötött tokennel — de a specifikáció ezt sehol nem nevezi meg kifejezetten „projekt-elkülönítésnek", ez a mi következtetésünk a resource-indicator mechanizmusból, nem szó szerinti spec-ajánlás.

### c) Enterprise-Managed Authorization (EMA) kiterjesztés — szervezeti, nem projekt-szintű

Az EMA (stabil kiterjesztés, SEP‑990/646) a **melyik MCP-szervert érheti el egy alkalmazott** kérdést oldja meg központi IdP-vezérelt hozzáféréssel, de nem nyúl bele egyetlen szerveren belüli projekt/workspace-particionálásba:

> „The Enterprise-Managed Authorization extension (`io.modelcontextprotocol/enterprise-managed-authorization`) enables organizations to control MCP server access centrally through their existing identity provider (IdP)."
(https://modelcontextprotocol.io/extensions/auth/enterprise-managed-authorization.md)

### d) Regisztry-szintű (nem futásidejű) tenant-URL-sablonozás

A különálló `modelcontextprotocol/registry` projekt tenant-onkénti URL-sablonokat enged meg a szerver *hirdetésében* (nem a runtime protokollban):

> „This PR adds LocalTransport and RemoteTransport separation with URL template variables support for remote servers, enabling e.g. multi-tenant deployments with configurable endpoints. ... \"remotes\": [ { \"type\": \"streamable-http\", \"url\": \"https://api.example.com/mcp/{tenant_id}/{region}\", \"variables\": { \"tenant_id\": {...} } } ]"
(https://github.com/modelcontextprotocol/registry/pull/570)

Ez a klienskonfigurációban/regisztry-bejegyzésben old fel egy `{tenant_id}` változót — vagyis a szerver-végpont maga válik tenant-specifikussá, még mielőtt bármilyen MCP-kérés elindulna; nem futásidejű protokoll-mechanizmus.

### e) El nem fogadott/lezárt közösségi javaslatok, mint a hiány bizonyítékai

- **Issue #1597** (HTTP REST Transport javaslat) kifejezetten a több-bérlős, terheléselosztott szcenárió tenant-elkülönítési problémáját feszegette, de a Microsoft-csapat elnapolta:

  > „We must have some truly secure mechanism to separate tenant/users/hosts for Remote MCP Servers. Simple ID values (like UUIDs) simply won't be good enough." ... „Per internal discussion in the MCP crew at Microsoft..., we'll hold off on the pure HTTP transport proposal and work on a different, more incremental approach down the line."
  (https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1597)

- **Discussion #609** („Authorization and Multitenancy") közösségi kérdés-válasz, hivatalos állásfoglalás nélkül; a gyakorlati „megoldás", amit egy hozzászóló ad, kívül esik a protokollon (reverse proxy middleware):

  > „The solution I'm currently tinkering with is to not implement the OAuth authentication at the MCP endpoint at all. But instead use a Traefik Middleware configuration that's guarding the MCP endpoints against unauthorized access."
  (https://github.com/modelcontextprotocol/modelcontextprotocol/discussions/609)

- **Discussion #234** („Multi-user Authorization") egy community-javaslat arra, hogy a tool-szintű `_meta.authorization.token` mezőben vigyen a kliens felhasználó-specifikus, harmadik-fél OAuth-tokent — ez a per-*felhasználó* (nem per-*projekt*) problémára született javaslat, és a talált anyagokban nem szerepel elfogadott/Final SEP-ként.

**Összegzés Q4-re:** a specifikáció explicit, szándékos döntése (SEP‑2567), hogy a „melyik kontextusban dolgozunk" kérdést kiszervezi a tool-tervezésbe; a runtime-protokoll szintjén nincs beépített tenant/projekt-választó mechanizmus.

---

## 5. OAuth scope-ok projekt szerinti hatókörre

### Amit a spec ténylegesen mond a scope-okról

A `resource` paraméter (RFC 8707) — nem a scope — azonosítja, *melyik* erőforráshoz (MCP-szerverhez) szól a token; ezt a specifikáció **kötelezővé** teszi:

> „MCP clients MUST implement Resource Indicators for OAuth 2.0 as defined in RFC 8707 to explicitly specify the target resource for which the token is being requested. The `resource` parameter: 1. MUST be included in both authorization requests and token requests. 2. MUST identify the MCP server that the client intends to use the token with. 3. MUST use the canonical URI of the MCP server..."
(https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization)

Maga az RFC 8707 kifejezetten megkülönbözteti a scope-ot (*mit* enged) a resource-tól (*hova* szól a token), és óva int a scope „hely-kódolásra" való felhasználásától:

> „OAuth scope, from Section 3.3 of [RFC6749], is sometimes overloaded to convey the location or identity of the protected resource, however, doing so isn't always feasible or desirable. Scope is typically about what access is being requested rather than where that access will be redeemed..."
(RFC 8707 §1, https://www.rfc-editor.org/rfc/rfc8707.html)

A szerver a tokent az `aud` (audience) claim alapján, a `resource` paraméterre kötve ellenőrzi:

> „MCP servers MUST validate that access tokens were issued specifically for them as the intended audience, according to RFC 8707 Section 2."
(https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization)

### Scope-hierarchia — új, formális elem a 2026-07-28-ban

A 2026-07-28-as revízió új, explicit követelményt vezet be a scope-hierarchiák kezelésére (ez korábban, a 2025-11-25-ös szövegben nem szerepelt ilyen tömör megfogalmazásban a talált idézetek alapján):

> „Servers MUST account for scope hierarchies, where a broader scope implies narrower ones, when deciding whether a token is sufficient for an operation."
(https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization)

Ez elvi lehetőséget ad arra, hogy egy szerver saját scope-névtérben (pl. `memory:project:acme:*` vs. `memory:project:acme:read`) hierarchikus, projekt-tudatos scope-sémát vezessen be — de ezt **maga a szerver/authorization-server definiálja**, az MCP-specifikáció csak a hierarchia-tiszteletet írja elő, magát a névteret/projekt-fogalmat nem.

### Gyakorlati példa a hivatalos anyagokban — nem projekt-szintű

A hivatalos oktatóanyag Keycloak-példája egyetlen, funkció-szintű (nem projekt-szintű) scope-ot használ:

> „Go to Client scopes in the Keycloak dashboard and create a new `mcp:tools` scope."
(https://modelcontextprotocol.io/docs/tutorials/security/authorization)

Ez alátámasztja, hogy a hivatalos dokumentáció jelenleg **nem ad konkrét mintát projekt-szintű scope-dizájnra**; a scope-mechanizmus technikailag alkalmas lenne rá (a hierarchia-szabály miatt), de nincs rá hivatalos recept.

### Összefoglalás Q5-re

- A spec és az RFC 8707 szerint a **hely/erőforrás-azonosítás a `resource` paraméter feladata**, nem a scope-é — ez explicit, T1-es állítás.
- A **scope-ok** formálisan bármilyen opak stringek lehetnek, és a 2026-07-28-as revízió előírja a hierarchia-tiszteletet, ami *lehetővé teszi* egy projekt-tudatos scope-séma megtervezését, de ezt nem a protokoll, hanem az implementáció (Authorization Server + MCP-szerver) dolga kitalálni.
- Projekt szerinti elkülönítésre a specifikációból levezethető, de sehol nem nevesített mintázat: **külön kanonikus resource-URI projektenként** (pl. `https://mcp.example.com/proj-a` vs. `/proj-b`), mindegyik saját audience-re kötött tokennel — ez lényegében minden projektet külön OAuth-erőforrásként kezel.

---

## Ellentmondások

1. **Elicitation hiánya a hivatalos feature-support-mátrixból.** A `modelcontextprotocol/docs` repóból (`clients.mdx`, a `modelcontextprotocol.io/clients` oldal forrása) kiolvasott táblázat csak Resources/Prompts/Tools/Sampling/Roots oszlopokat tartalmaz, Elicitation-t nem — annak ellenére, hogy az Elicitation funkció a 2025-06-18-as verzió óta létezik a törzsspecifikációban. Nem tudtam megállapítani, hogy ez az oldal egyszerűen elavult (nem frissítették), vagy hogy az Exa által visszaadott változat egy régebbi cache. A közösségi (nem hivatalos, T2/T3) `apify/mcp-client-capabilities` adatbázis viszont vezet Elicitation oszlopot, és client-specifikus adatokat ad — de ez utóbbi forrás önmagában, hivatalos T1 megerősítés nélkül áll.
2. **A SEP‑2202 (nem-`file://` roots URI-k) állapota bizonytalan.** A PR-oldal szövege szerint a szerző „hivatalosan szüneteltette" a javaslatot, és egy hozzászólás megjegyzi, hogy a Roots időközben deprecated lett — de nem találtam formális „Withdrawn/Rejected" SEP-státuszjelölést, csak a PR-beszélgetés szövegét. Emiatt ezt inkább „félbehagyott, gyakorlatilag elavult javaslat"-ként, nem hivatalosan lezárt SEP-ként kezelem.
3. **Discussion #234 (Multi-user Authorization) sorsa nem egyértelmű a fellelt anyagokból** — a talált szöveg a javaslat eredeti felvetése, elfogadási/elutasítási státuszra utaló hivatalos SEP-oldalt nem találtam hozzá ebben a kutatási körben.

## Amire NINCS forrás

- **Nincs forrás** arra, hogy a 2026-07-28-as specifikáció vagy bármely Final SEP kifejezetten „projekt" vagy „workspace" fogalmú, névvel ellátott `_meta`-kulcsot vagy natív mechanizmust definiálna a kliens munkakörnyezetének azonosítására.
- **Nincs forrás** hivatalos, Final SEP-re, amely megmondaná, hogy egy több-bérlős távoli MCP-szerver *futásidőben* URL-útvonal, paraméter, token-scope vagy roots közül melyiket „kellene" használnia a hatókör-választásra — csak közvetett, analógiás anyagok (SEP‑2567, RFC 8707 canonical-URI szövege, EMA-kiterjesztés, elnapolt/lezárt community-javaslatok) állnak rendelkezésre, ahogy fent részleteztem.
- **Nincs forrás** arra, hogy bármely hivatalos MCP-dokumentum konkrét, ajánlott scope-elnevezési konvenciót adna projekt-szintű elkülönítésre (pl. `project:<id>:read` minta hivatalos példaként).

## Meglátogatott és felderített linkek

| Cím | URL | Tier | Eszköz | Megjegyzés |
|---|---|---|---|---|
| 2026-07-28 changelog | https://modelcontextprotocol.io/specification/2026-07-28/changelog | T1 | Exa search+fetch | Fő changelog: MRTR, roots/sampling/logging deprecation, stateless mag |
| 2026-07-28 spec index | https://modelcontextprotocol.io/specification/2026-07-28 | T1 | Exa search | Spec-főoldal |
| 2026-07-28 release tag | https://github.com/modelcontextprotocol/modelcontextprotocol/releases/tag/2026-07-28 | T1 | Exa search | Hivatalos release-jegyzet |
| Versioning and Compatibility | https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning | T1 | Exa search | Modern vs. legacy éra, `server/discover`, `UnsupportedProtocolVersionError` |
| Blog: The 2026-07-28 Specification | https://blog.modelcontextprotocol.io/posts/2026-07-28/ | T1 | Exa search | Hivatalos bejelentés, MRTR/deprecation összefoglaló |
| basic/index (_meta, per-request fields) | https://modelcontextprotocol.io/specification/2026-07-28/basic/index | T1 | Exa search | `_meta` kulcsnév-szabályok, kötelező mezők, hibakódok |
| Blog: Release Candidate | https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/ | T1 | Exa search | RC ütemterv, roots/sampling/logging deprecation előzetes |
| Roots (2025-11-25) | https://modelcontextprotocol.io/specification/2025-11-25/client/roots | T1 | Exa search | Korábbi (session-alapú) roots-mechanizmus |
| TS SDK — Provide roots | https://ts.sdk.modelcontextprotocol.io/v2/clients/roots.html | T1 | Exa search | Stateless módban nincs szerver→kliens csatorna, MRTR-beágyazás |
| SEP-2577 (Deprecate Roots, Sampling, Logging) | https://modelcontextprotocol.io/seps/2577-deprecate-roots-sampling-and-logging | T1 | Exa fetch | Teljes SEP-szöveg, indoklás, deprecation-ütemezés |
| schema/2024-11-05/schema.ts | https://github.com/modelcontextprotocol/specification/blob/main/schema/2024-11-05/schema.ts | T1 | Exa search | Eredeti `Root`/`ListRootsRequest` definíció |
| Roots (draft, mintlify tükör) | https://mcp.mintlify.app/specification/draft/client/roots | T2 | Exa search | MRTR `roots/list` szekvenciapélda (nem hivatalos domain, de a tartalom a hivatalos draft szövege) |
| C# SDK — Roots | https://csharp.sdk.modelcontextprotocol.io/v2/concepts/roots/roots.html | T1 | Exa search | `RequestRootsAsync` stateless-kivétel, `InputRequiredException` |
| Python SDK — Sampling and roots | https://py.sdk.modelcontextprotocol.io/handlers/sampling-and-roots/index.md | T1 | Exa search | `-32021` hibakód képesség hiányában |
| Go SDK — MCP Client (Roots) | https://go.sdk.modelcontextprotocol.io/client/ | T1 | Exa search | MRTR middleware, `clientMultiRoundTripMiddleware` |
| Elicitation (2026-07-28) | https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation | T1 | Exa fetch | Teljes elicitation-szöveg: mód, séma, biztonsági korlátok |
| Transports — Overview (2026-07-28) | https://modelcontextprotocol.io/specification/2026-07-28/basic/transports | T1 | Exa fetch | Body a forrás igazság, header-tükrözés elve |
| Authorization (2026-07-28) | https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization | T1 | Exa search | `resource` paraméter, scope-stratégia, scope-hierarchia |
| RFC 8707 (rfc-editor) | https://www.rfc-editor.org/rfc/rfc8707.html | T1 | Exa search | Resource Indicators, scope vs. resource megkülönböztetés |
| RFC 8707 (datatracker) | https://datatracker.ietf.org/doc/html/rfc8707/ | T1 | Exa search | Ua., másodlagos IETF-tükör megerősítésként |
| Authorization (draft, modelcontextprotocol.info tükör) | https://modelcontextprotocol.info/specification/draft/basic/authorization/ | T2 | Exa search | Kanonikus URI valid/invalid példák (nem hivatalos domain) |
| Issue #1597 (HTTP REST Transport SEP-javaslat) | https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1597 | T1 (hivatalos repo, el nem fogadott javaslat) | Exa search | Multi-tenant elkülönítési probléma, elnapolva |
| Registry PR #570 (RemoteTransport tenant_id) | https://github.com/modelcontextprotocol/registry/pull/570 | T1 (hivatalos repo, elfogadott PR) | Exa search | Regisztry-szintű tenant-URL-sablonozás |
| Discussion #234 (Multi-user Authorization) | https://github.com/modelcontextprotocol/modelcontextprotocol/discussions/234 | T1 (hivatalos repo, közösségi vita) | Exa search | Per-felhasználó `_meta.authorization` javaslat, nem Final SEP |
| PR #2202 (SEP-2202, non-file roots, szüneteltetve) | https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2202 | T1 (hivatalos repo, félbehagyott javaslat) | Exa search | Miért nem lazult a `file://` megkötés |
| SEP-2243 (HTTP Standardization) | https://modelcontextprotocol.io/seps/2243-http-standardization | T1 | Exa search | `Mcp-Method`/`Mcp-Name`/`x-mcp-header`/`Mcp-Param-*` |
| TS SDK issue #2190 (SEP-2243 implementáció) | https://github.com/modelcontextprotocol/typescript-sdk/issues/2190 | T1 (hivatalos repo issue) | Exa search | Biztonsági megjegyzés: `Mcp-Param-*` nem authorizációra való |
| Clients — feature support matrix | https://github.com/modelcontextprotocol/docs/blob/573dc60c/clients.mdx | T1 | Exa search | Hivatalos, de Elicitation oszlop nélküli mátrix (l. Ellentmondások) |
| apify/mcp-client-capabilities | https://github.com/apify/mcp-client-capabilities | T2/T3 | Exa search | Közösségi kliens-képesség adatbázis, Elicitation oszlopokkal |
| Understanding MCP clients (2026-07-28 learn docs) | https://modelcontextprotocol.io/docs/2026-07-28/learn/client-concepts | T1 | Exa search | Roots/Sampling deprecation összefoglalása felhasználói nyelven |
| EMA extension spec | https://modelcontextprotocol.io/extensions/auth/enterprise-managed-authorization.md | T1 | Exa search | Enterprise-Managed Authorization: szervezeti, nem projekt-szintű |
| ext-auth overview | https://modelcontextprotocol.io/extensions/auth/overview.md | T1 | Exa search | Mikor melyik auth-kiterjesztés ajánlott |
| Blog: Enterprise-Managed Authorization | https://blog.modelcontextprotocol.io/posts/enterprise-managed-auth/ | T1 | Exa search | EMA stabillá válásának bejelentése |
| ext-auth PR #4 (SEP-646/990) | https://github.com/modelcontextprotocol/ext-auth/pull/4 | T1 (hivatalos repo) | Exa search | EMA eredeti javaslata, folyamábra |
| SEP-2567 (Sessionless MCP) | https://modelcontextprotocol.org/seps/2567-sessionless-mcp | T1 | Exa fetch | Explicit state handle mint „tool-design pattern", Final SEP |
| Discussion #609 (Authorization and Multitenancy) | https://github.com/modelcontextprotocol/modelcontextprotocol/discussions/609 | T1 (hivatalos repo, közösségi vita) | Exa search | Nincs tiszta válasz, reverse-proxy workaround |
| Tutorial: Authorization (Keycloak példa) | https://modelcontextprotocol.io/docs/tutorials/security/authorization | T1 | Exa search | `mcp:tools` scope-példa, nem projekt-szintű |
| PR #835 (SEP-835, scope selection strategy) | https://github.com/modelcontextprotocol/modelcontextprotocol/pull/835 | T1 (hivatalos repo) | Exa search | Scope-választási prioritás, step-up authorization |
| SEP-2207 (offline_access guidance) | https://modelcontextprotocol.io/seps/2207-oidc-refresh-token-guidance.md | T1 | Exa search | Tangenciális: scope ≠ resource-jellegű megkülönböztetés megerősítése |
| Issue #1292 (Namespaces using URIs, SEP-javaslat) | https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1292 | T1 (hivatalos repo, Proposal státusz) | Exa search | Tool/resource-névütközés, nem client-projekt-kontextus |
| Architecture (draft) | https://modelcontextprotocol.io/specification/draft/architecture | T1 | Exa search | Client-host-server modell, kérésenkénti capability-negotiation |
| schema/2026-07-28/schema.ts | https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/schema/2026-07-28/schema.ts | T1 | Exa search | `RequestMetaObject`, `_meta` mezők pontos TS-típusai |

---

# SQ02 — Hogyan döntik el a meglévő memória-rendszerek, hová kerül egy új emlék, és honnan tudják a projektet?

> **Degradált mód megjegyzése:** ez a kutatás egyetlen ügynökként, alügynökök indítása nélkül készült (a futtató környezetben nem állt rendelkezésre olyan eszköz, amellyel párhuzamos kutató-alügynökök indíthatók lettek volna a `deep-web-research` skill elvei szerint). A kutatás ezért egy hosszú, szekvenciális Exa-keresési munkamenetben zajlott, ugyanazokkal a forrás- és idézési szabályokkal (elsődleges forrás, szó szerinti idézet, kereszt-megerősítés), de alügynökök általi párhuzamos lefedettség nélkül. A kizárólagos keresőeszköz az Exa (`mcp__Exa__web_search_exa`, `mcp__Exa__web_fetch_exa`) volt; a beépített WebSearch/WebFetch-et nem használtam.

## Rövid válasz

A vizsgált rendszerek négy, egymástól jól elkülöníthető mintát követnek a „hova kerüljön az emlék" és a „honnan tudom a projektet" kérdésre. (1) **Explicit hívó-paraméter, szerver-oldali fallback-kel**: a basic-memory `project` paramétere, a mem0/OpenMemory `user_id`/`agent_id`/`app_id`/`run_id`-je és a Graphiti `group_id`-je mind a hívó (az ágens) által, tool-hívásban adható meg, de mindegyiknél van szerver-oldali alapérték (`default_project` konfig, `DEFAULT_USER_ID` env, `--group-id main`), ha a hívó nem ad meg semmit. (2) **Kapcsolat-/fejléc-alapú, a hívó által nem felülírható kötés**: a Zep hivatalos Memory MCP Servere és a `opspresso/mcp-memory` tudatosan **kizárja** a tool-argumentumot a bérlő/projekt kiválasztásából — a projekt/identitás az OAuth-bejelentkezéshez vagy egy HTTP fejléchez van kötve, mert (idézve az opspresso indoklását) „a model that can name its own tenant can read another project's memories by asking". (3) **Fájlrendszer-hierarchia / munkakönyvtár-bejárás, teljesen automatikus**: a Claude Code CLAUDE.md-je és a Codex AGENTS.md-je a cwd-ből felfelé sétálva, projekt-gyökérig (jellemzően `.git`) automatikusan megtalálja a releváns fájlokat, tool-hívás vagy paraméter nélkül; a Serena `--project-from-cwd` opciója szintén automatikus detektálást ad. (4) **Explicit aktiválás/session-állapot**: a Serena `activate_project` tool-ja és a Letta agent-hez kötött blokk-modellje a projektet egy korábbi hívás által beállított munkamenet-állapotként kezeli. A több szintű hatókör (személyes/projekt/közös) szinte mindegyik rendszerben megvan valamilyen formában (Claude Code: managed→user→project→local; Serena: project vs. `global/`; Zep: user graph vs. group graph; mem0 Platformnál org→project→user/agent/run), de a döntést szinte sosem a szerver hozza automatikusan: vagy az ágens dönt explicit felhasználói utasítás alapján (Serena: „If explicitly instructed, use the global/ prefix"), vagy a felhasználó/fejlesztő állítja be konfigurációban/fájlhelyen (Claude Code: melyik fájlba ír a user), vagy a szerver üzemeltetője rögzíti kapcsolat-szinten (Zep, opspresso). A saját projekt kutatási hiányossága — hogy sehol nincs explicit definiálva, honnan tudja az ágens/szerver az aktuális projektet — tehát nem egyedi: a Codex saját „memories" funkciója (a `AGENTS.md`-től eltérő, tanult-kontextus rétege) jelenleg **explicit módon, forráskódban dokumentáltan globális**, projekt-izoláció nélkül fut, és a közösség (GitHub issue) éppen emiatt kéri számon a projekt-szintű elkülönítést — ez szinte szó szerint ugyanaz a hiány, amit ez a kutatási projekt is azonosított.

---

## 1. basic-memory

**Forrás típusa:** T1 — hivatalos dokumentáció (`docs.basicmemory.com`, tükrözve `basicmachines-co-basic-memory.mintlify.app` és `basicmachines.mintlify.app` alatt is → 2 független tükör ugyanattól a projekttől, tartalmilag megegyezik).

### 1. Írási eszköz sémája
A `write_note` tool Python-szignatúrája (mintlify-tükör):
> „`async def write_note(title: str, content: str, directory: str, project: Optional[str] = None, workspace: Optional[str] = None, tags: list[str] | str | None = None, note_type: str = "note", metadata: dict | None = None, overwrite: bool | None = None, output_format: Literal["text", "json"] = "text", context: Context | None = None) -> str | dict`"

A `project` mező leírása: „Project name to write to. **Optional** - server resolves using hierarchy." — tehát a `project` paraméter nem kötelező.

### 2. Honnan tudja a rendszert az aktuális projektet
A hivatalos MCP Tools Reference táblázata a feloldási sorrendet írja le:
> „Project resolution order is: constrained project env -> explicit `project` parameter -> `default_project` fallback."
> „`BASIC_MEMORY_MCP_PROJECT` — Environment-level project constraint for MCP sessions. Locks operations to one project for that process/session — Highest-priority project constraint"

A konfigurációs doksi szerint:
> „`default_project` — Fallback project name used when tools/commands do not pass a project. Type: `string | null` — Default: unset — the first configured project is used (`"main"` on fresh installs, where a `main` project is seeded)."

A koncepció-doksi (Projects and folders) az ágens viselkedését is leírja:
> „When you run a command or an AI tool like `write_note`, it targets the project you name — each call carries a `project` parameter or CLI argument. If you don't specify one, it goes to the default project... The AI will simply pass `project="personal"` on its next tool calls — there's no switch step; it discovers your projects with `list_memory_projects`."

Van egy „single-project mode" is, ahol a `project` paraméter teljesen figyelmen kívül marad:
> „`basic-memory mcp --project work-notes` — This locks the entire MCP session - the `project` parameter in tool calls will be ignored."

### 3. Több szintű hatókör, ki dönt
A basic-memory-nak **nincs** beépített személyes/projekt/közös hierarchiája — projektjei egyenrangú, névvel azonosított, egymástól elszigetelt tárolók (`projects: {"main": {...}, "research": {...}}` a configban), a felhasználó/ágens dönt melyikbe ír, a döntést a `project` paraméter vagy a session-szintű alapértelmezés hordozza. Nincs automatikus „ez tech-tudás, ez menjen feljebb" logika.

### 4. Olvasás/keresés hatóköre
A mintlify-tükör (guides/mcp-tools-reference) explicit kimondja:
> „`search_notes(...)` # Searches current project only" — „`write_note(...)` # Creates note in current project" szemben a globális `list_projects()`, `create_project()` hívásokkal, amelyek projekt-függetlenek.

---

## 2. mem0 (Platform + OSS) és OpenMemory MCP

**Forrás típusa:** T1 — `docs.mem0.ai` (hivatalos), `github.com/mem0ai/mem0` forráskód (hivatalos repó), `github.com/mem0ai/mem0-mcp` (hivatalos MCP wrapper repó). Kiegészítésül T2/T3: `github.com/pinkpixel-dev/mem0-mcp` (nem hivatalos, közösségi wrapper — külön jelölve).

### 2.1 mem0 OSS (`Memory` osztály, self-hosted)

**Írási séma** (`mem0/memory/main.py`, hivatalos forráskód):
> „`def add(self, messages, *, user_id: Optional[str] = None, agent_id: Optional[str] = None, run_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None, ...)` ... Adds new memories scoped to a single session id (e.g. `user_id`, `agent_id`, or `run_id`). **One of those ids is required.**"

A validáció forráskódból:
> „`if not session_ids_provided: raise Mem0ValidationError(message="At least one of 'user_id', 'agent_id', or 'run_id' must be provided.", ...)`"

Tehát a mem0 OSS-nek **nincs** `project` fogalma és **nincs** szerver-oldali alapértelmezés — kötelező explicit azonosítót adni minden híváskor, különben kivétel dobódik. Ez éles ellentétben áll a basic-memory-val, ahol van fallback.

**Projekt forrása:** kizárólag a hívó adja meg, minden egyes hívásban; nincs env-alapú vagy konfig-alapú fallback a nyílt forráskódú `Memory` osztályban.

### 2.2 mem0 Platform (`MemoryClient`, felhő)

A `MemoryClient` konstruktora opcionális `org_id`/`project_id` mezőket vesz fel (LLM.md, hivatalos):
> „`client = MemoryClient(api_key="your-api-key", host="https://api.mem0.ai", org_id="your-org-id", project_id="your-project-id")`"

Itt tehát megjelenik egy valódi, Platform-szintű `project_id`, ami a Pro-csomag szervezeti struktúráját (org → project) reprezentálja, konfig-időben (kliens-inicializáláskor) rögzítve, nem minden hívásnál újra megadva.

### 2.3 Nem hivatalos MCP wrapperek (T2/T3, óvatosan kezelve)

A `pinkpixel-dev/mem0-mcp` (közösségi, nem a mem0ai szervezet repója) egy negyedik paramétert ad hozzá:
> „**`appId`** - Identifies the user's project/application - **this controls project scope!** (optional) ... Fallback: `DEFAULT_APP_ID` environment variable"

**Ellentmondás/inkonzisztencia:** ez a nem hivatalos wrapper az `app_id`-t nevezi „projekt hatókörnek", miközben a hivatalos Mem0 Platform egy teljesen külön, valódi `project_id` mezőt definiál Pro-csomagban — a két fogalom a mem0-ökoszisztémán belül nem esik egybe, és ezt sehol nem tisztázzák egyértelműen (lásd Ellentmondások fejezet).

Elsőbbségi sorrend ugyanebben a wrapperben (T3, közösségi doksi):
> „1. **Tool Parameters** (highest priority) - Values provided by the LLM in tool calls / 2. **Environment Variables** (fallback) - Values from your MCP configuration"

### 2.4 OpenMemory MCP (mem0ai hivatalos, önhosztolt)

**Forrás:** `github.com/mem0ai/mem0/blob/main/openmemory/api/app/mcp_server.py` (hivatalos forráskód) + `mem0.ai/blog/introducing-openmemory-mcp` (hivatalos blog).

Itt a projekt/identitás **nem tool-paraméter**, hanem az URL útvonalból és kontextusváltozóból jön:
> „`user_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("user_id")` / `client_name_var: contextvars.ContextVar[str] = contextvars.ContextVar("client_name")`"
> „`@mcp_router.get("/{client_name}/sse/{user_id}") async def handle_sse(request: Request): ... uid = request.path_params.get("user_id") ... client_name = request.path_params.get("client_name")`"

Az `add_memories` tool szignatúrája **nem is tartalmaz** `user_id` paramétert:
> „`@mcp.tool(...) async def add_memories(text: str, infer: bool = True) -> str: uid = user_id_var.get(None); client_name = client_name_var.get(None) ... if not uid: return "Error: user_id not provided"`"

Vagyis az OpenMemory az ágenshez rendelt kapcsolat (SSE endpoint URL `/{client_name}/sse/{user_id}`) alapján dönti el, ki az adott felhasználó és melyik alkalmazás (client) ír — ez a „kapcsolat-szintű" mintát mutatja, hasonlóan a Zephez.

**Keresés hatóköre:** a `search_memory` tool mindig a saját `user_id`-jára szűrt: „`filters = {"user_id": uid}`" — más felhasználó memóriája elérhetetlen ezen a tool-on keresztül.

**Több szintű hatókör:** két szint — `user_id` (személy) és `app_id`/`client_name` (alkalmazás/eszköz, pl. Cursor vs. Claude Desktop) —, ACL-lel szabályozható engedélyezés/szüneteltetés app-onként (mem0.ai hivatalos blog: „Pause or revoke any client's access at app or memory level").

### 2.5 mem0 OpenCode-integráció — automatikus, git-alapú projekt-detektálás (T1, `docs.mem0.ai`)

Ez a hivatalos integráció explicit automatikus, munkakönyvtár-alapú projekt-forrást ad, tool-paraméter nélkül:
> „The project id (`app_id`) is derived from your git remote (`owner-repo`), falling back to the git repo's root directory name, then the current directory."

És egy háromszintű hatókör-modellt is bevezet, amit az ágens dönt el (nyelvi kérés alapján), nem a szerver:
> „| Scope | Reads | Writes | | --- | --- | --- | | `project` (default) | this repo (`user_id` + `app_id`) | this repo | | `session` | this run only (`+ run_id`) | this run | | `global` | all your projects in the workspace (`app_id: "*"`) | user-wide |"
> „Ask naturally, for example, 'search my memories across all my projects'. The agent passes `scope: "global"`. For normal questions it stays scoped to the current project automatically."

---

## 3. Letta

**Forrás típusa:** T1 — `docs.letta.com` (hivatalos), `github.com/letta-ai/letta` (hivatalos forráskód).

### 1–2. Írási séma és a „projekt" forrása
Letta-ban a memória alapegysége nem a „projekt", hanem az **agent** és az ahhoz csatolt **memory block**. A `project_id` egy Letta Cloud-specifikus, adminisztratív mező, ami az agenteket rendezi a felhő-dashboardon, **nem** befolyásolja, melyik memória-blokkot melyik agent látja.

OpenAPI-specifikáció (hivatalos, `letta-agents-api-openapi.yml`):
> „`project_id` — in: query — required: false — description: Search agents by project ID - **this will default to your default project on cloud**"

Agent-létrehozáskor fejlécen keresztül is átadható (hivatalos forráskód, `routers/v1/agents.py`):
> „`x_project: str | None = Header(None, alias="X-Project", description="The project slug to associate with the agent (cloud only).")`"

Tehát Lettánál a „projekt" forrása: (a) explicit `project_id` query-paraméter, vagy (b) `X-Project` HTTP fejléc, vagy (c) hiányukban a cloud fiók alapértelmezett projektje — **self-hosted (nem cloud) telepítésnél a `project_id` fogalma nem is releváns** (a doksi mindenhol „cloud only"-t ír).

### 3. Több szintű hatókör, ki dönt
A tényleges memória-hatókört nem a `project_id`, hanem a **block attachment** adja: egy memory block egy vagy több agenthez csatolható, és ha több agent van hozzácsatolva, közös (shared) memóriává válik.
> „Memory blocks can be attached to multiple agents at once ('shared blocks')." / „Shareable - Multiple agents can access the same block; update once, visible everywhere"

A döntést itt kizárólag a **fejlesztő** hozza meg API-hívással (explicit attach/detach), nem az ágens saját belátásából és nem szerver-szabály alapján:
> „You can also directly create blocks and attach them to an agent. This can be useful if you want to create blocks that are shared between multiple agents." / „You can also attach blocks to existing agents"

A MemFS-modell (git-repó-alapú memória) is megerősíti, hogy a megosztás mindig explicit fejlesztői/agent-döntés:
> „Shared memory repositories give several agents access to the same files. Attaching one recompiles the agent's system prompt..."

### 4. Olvasás/keresés hatóköre
Az archívumi keresés (`archival_memory_search`) szigorúan az adott agent saját archívumára korlátozódik; a blokk-lista (`list blocks`) viszont globálisan is lekérdezhető label szerint: „You can list all blocks, optionally filtering by label or searching by label text. This is useful for finding blocks across your project." — itt a „project" szó köznyelvi értelemben szerepel, nem a `project_id` mezőre utal.

---

## 4. Zep — hivatalos Memory MCP Server, és a Graphiti MCP szerver

**Forrás típusa:** T1 — `help.getzep.com` (hivatalos doksi), `blog.getzep.com` (hivatalos blog), `github.com/getzep/graphiti` (hivatalos forráskód).

### 4.1 Zep Memory MCP Server (a jelenlegi, hivatalos termék)

Ez a rendszer **explicit, tudatos döntéssel kizárja** a hívó (ágens/tool-argumentum) szerepét a projekt/felhasználó kiválasztásából — ez a leginkább releváns minta a kutatási kérdés szempontjából.

**1–2. Írási séma, projekt forrása:**
> „Each connected user can always read their own user graph. **User-graph tools take no user, graph, or project argument.** The target is fixed by the authenticated identity, so one user's token cannot select another user's memory or another project."
> „**The project cannot be selected by an MCP request or tool argument.** ... Zep binds the issued token to the selected connection and project."

Ehelyett a projekt/identitás forrása egy OAuth-alapú, adminisztrátor által konfigurált kapcsolat:
> „What the user can reach. Zep uses the user's work email to discover the organization's identity provider. After authentication, Zep finds every enabled project connection that admits the verified identity. It selects the project automatically when there is one, shows a chooser when there is more than one, and denies access when there are none."

**3. Több szintű hatókör, ki dönt:** user graph (személyes) vs. **standalone graph** (megosztott, csapat-szintű), amit `graph_id` azonosít, és amit egy `list_graphs`/directory tool tesz felfedezhetővé:
> „`list_graphs` — read — List other accessible graphs in the project (graph directory)" / „`search_graph_in` — read — Search a selected standalone graph by `graph_id`"

A hozzáférést nem az ágens, hanem a szerver üzemeltetője (admin) dönti el kapcsolat-szinten, két módban:
> „Connections can use project-wide access or UserGroup ABAC to grant specific graphs to each user. Plans without ABAC retain project-wide access." / „project-wide mode makes every standalone graph available; UserGroup ABAC mode limits the directory and selected-graph tools to explicit grants."

**4. Keresés hatóköre:** alapból csak a saját user graph, csapat/projekt-szintű grafokhoz csak explicit `graph_id` és jogosultság birtokában:
> „A graph a user is not authorized to see is absent from directory results and counts entirely."

### 4.2 Graphiti MCP szerver (a Zep nyílt forráskódú, önhosztolható komponense — más architektúra, mint a 4.1-es hivatalos termék)

**Forrás:** `github.com/getzep/graphiti/blob/main/mcp_server/README.md` (hivatalos), `help.getzep.com/graphiti/getting-started/mcp-server` (hivatalos).

**1. Írási séma** (`add_memory` tool):
> „`group_id (str, optional): A unique ID for this graph. If not provided, uses the default group_id from CLI or a generated one.`"

**2. Projekt forrása:** parancssori argumentum indításkor, VAGY tool-hívásban explicit `group_id`, ezek hiányában szerver-oldali alapérték:
> „`--group-id`: Set a namespace for the graph (optional). **If not provided, defaults to "main"**." (README)
> „Hint: specify a `group_id` to namespace graph data. If you do not specify a `group_id`, the server will use 'main' as the group_id." (ugyanaz a README, más helyen — megerősítve)

Egy korábbi verzió forráskódja (`graphiti_mcp_server.py`) még véletlenszerű UUID-t generált alapértékként, nem "main"-t:
> „`else: config.group_id = f'graph_{uuid.uuid4().hex[:8]}'; logger.info(f'Generated random group_id: {config.group_id}')`"

**Ellentmondás/időbeli eltérés:** a dokumentáció (mindkét hivatalos forrás) ma „main"-t ír alapértékként, de a régebbi forráskód-verzió (`dbe21a19` commit) véletlenszerű UUID-t generált — ez egy dokumentált viselkedés-változás a projekt történetében, nem egy jelenleg is fennálló ellentmondás.

**3. Több szintű hatókör:** a Graphiti-nak nincs beépített személyes/projekt/közös hierarchiája — a `group_id` egy lapos, tetszőleges string-namespace; a hierarchiát (ha van) a hívó fél építi fel konvencióval (pl. `"acme-corp/project-a"`).

**4. Keresés hatóköre:** a kereső tool-ok (`search_nodes`, `search_memory_facts`) `group_ids` paramétere lista is lehet, több namespace egyszerre kereshető, vagy ha üres, a konfigurált alapértelmezett group-ra esik vissza:
> „`group_ids: Optional[list[str]] = None ... effective_group_ids = (group_ids if group_ids is not None else [config.group_id] if config.group_id else [])`"

---

## 5. Claude Code saját memóriája (CLAUDE.md-hierarchia + auto memory)

**Forrás típusa:** T1 — `code.claude.com/docs/en/memory` (Anthropic hivatalos doksi), megerősítve 2 független tükrön/harmadik féltől (`claudeable.co`, `developertoolkit.ai`, `claude.yourdocs.dev`, GitHub-issue-k az `anthropics/claude-code` repóban).

### 1–2. Séma és a projekt forrása
A CLAUDE.md-nek **nincs tool-paramétere** — tisztán fájlrendszer-hierarchia és munkakönyvtár-bejárás dönti el, mi töltődik be:
> „Claude Code reads CLAUDE.md files by walking up the directory tree from your current working directory, checking each directory along the way for `CLAUDE.md` and `CLAUDE.local.md` files. This means if you run Claude Code in `foo/bar/`, it loads instructions from `foo/bar/CLAUDE.md`, `foo/CLAUDE.md`, and any `CLAUDE.local.md` files alongside them."

Négy hatókör, helyalapúan definiálva (nem paraméterrel, hanem azzal, hogy a felhasználó *hova írja a fájlt*):
> „| Scope | Location | ... | | Managed policy | `/etc/claude-code/CLAUDE.md` stb. | ... | | User instructions | `~/.claude/CLAUDE.md` | Personal preferences for all projects | Just you (all projects) | | Project instructions | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team-shared instructions for the project | Team members via source control | | Local instructions | `./CLAUDE.local.md` | Personal project-specific preferences... | Just you (current project) |"

Betöltési sorrend és elsőbbség:
> „Across the directory tree, content is ordered from the filesystem root down to your working directory... so instructions closer to where you launched Claude are read last." — „Within each directory, `CLAUDE.local.md` is appended after `CLAUDE.md`, so your personal notes are the last thing Claude reads at that level."

Az **auto memory** (amit maga Claude ír, nem a felhasználó) projekt-azonosítása git-repó-alapú, nem cwd-alapú:
> „Each project gets its own memory directory at `~/.claude/projects//memory/`. The `` path is **derived from the git repository**, so all worktrees and subdirectories within the same repo share one auto memory directory. Outside a git repo, the project root is used instead."

### 3. Több szintű hatókör, ki dönt
Négy hierarchikus szint (managed policy → user → project → local), **a felhasználó dönti el**, melyik fájlba ír a szándéka szerint — nincs automatikus besorolási logika, a döntés tisztán a fájl elhelyezésén (`~/.claude/CLAUDE.md` vs. `./CLAUDE.md` vs. `./CLAUDE.local.md`) múlik. Az auto memory esetében **Claude dönt** (ágens, nem a szerver), mit ér meg megjegyezni: „Claude doesn't save something every session. It decides what's worth remembering based on whether the information would be useful in a future conversation." Az auto memory viszont csak projekt-szintű — nincs "user-wide auto memory" vagy "org-wide auto memory" réteg.

### 4. Olvasás/keresés hatóköre
A CLAUDE.md-fájlok betöltése kizárólag a munkakönyvtár hierarchiájára korlátozódik (a gyökérig, nem tovább): „Claude Code recurses up to (but not including) the root directory /". Az auto memory a projektkönyvtár saját `MEMORY.md`-jére és a hozzá tartozó témafájlokra korlátozódik, más projekt memóriája nem érhető el a session-ből.

---

## 6. Cursor — Rules és memories

**Forrás típusa:** T1 — `cursor.com/docs/rules`, `cursor.com/help/customization/rules.md` (hivatalos), keresztellenőrizve a `prod.cursor.com` tükörrel (megegyezik) és harmadik féltől (`learncursor.dev`, `memories.sh` — T3, kiegészítő).

### 1–2. Séma és a projekt forrása
Cursor-nak nincs saját MCP írási tool-ja a rule-okhoz — a `.cursor/rules/*.mdc` fájlokat vagy a felhasználó írja kézzel, vagy egy beépített `/create-rule` slash command generálja. A „projekt" forrása egyszerűen a **workspace gyökérkönyvtár**:
> „Project rules live in `.cursor/rules` as `.mdc` files and are version-controlled and scoped to your codebase."

Egy `.mdc` fájl frontmatter-je (`description`, `globs`, `alwaysApply`) dönti el, mikor lép életbe — de ez fájl-útvonal, nem hatókör:
> „| `alwaysApply` | `description` | `globs` | Behavior | | --- | --- | --- | --- | | `true` | — | — | Always included... | | `false` | — | provided | Auto-attached when a matching file is in context. |"

### 3. Több szintű hatókör, ki dönt
Három explicit szint, amit a **felhasználó** dönt el a rule elhelyezésével:
> „- Project rules are stored in `.cursor/rules/` inside your project folder. They're version-controlled with git. - User rules in Cursor Settings are stored on your Cursor account. They apply across all your projects and sync when you sign in on another machine. ... - Team rules are stored on Cursor's servers and managed from the team dashboard. They sync automatically to all team members."

A `CLAUDE.md`-t és az `AGENTS.md`-t is natívan beolvassa Cursor, de más szabállyal:
> „`CLAUDE.md` files are always applied to every conversation, regardless of any `alwaysApply` frontmatter setting." — míg az `AGENTS.md` almappákban is öröklődik: „Nested `AGENTS.md` support in subdirectories is now available."

### 4. Olvasás/keresés hatóköre
Nincs „keresés" tool a beépített rule-rendszerben (statikus betöltés indításkor/relevancia szerint), viszont egy harmadik féltől származó MCP-integráció (`memories.sh`, T3) mutatja meg, hogyan lehet ezt kiterjeszteni MCP-szerverré — ez a rendszer kívül esik Cursor hivatalos termékén, ezért csak kiegészítő adatként szerepel.

---

## 7. Codex (OpenAI) — AGENTS.md és a „Memories" funkció

**Forrás típusa:** T1 — `developers.openai.com/codex` (hivatalos), `learn.chatgpt.com/docs` (hivatalos, ugyanaz a tartalom más URL-en → 2. független megerősítés), `github.com/openai/codex` (hivatalos forráskód, Rust) — 3 független, egymást megerősítő elsődleges forrás.

### 7.1 AGENTS.md — projekt-szintű, automatikus (ez működik jól)

**1–2. Séma és forrás:** nincs tool-paraméter; könyvtár-bejárás projekt-gyökértől (git-gyökér) a cwd-ig:
> „Project scope: Starting at the project root (typically the Git root), Codex walks down to your current working directory. If Codex cannot find a project root, it only checks the current directory."
> „Merge order: Codex concatenates files from the root down, joining them with blank lines. Files closer to your current directory override earlier guidance because they appear later in the combined prompt."

Forráskód-szintű megerősítés (`codex-rs/core/src/agents_md.rs`, hivatalos):
> „Determine the project root by walking upwards from the current working directory until a configured `project_root_markers` entry is found. When `project_root_markers` is unset, the default marker list is used (`.git`)."

**Dokumentált korlát (ellentmondás — lásd Ellentmondások):** a `project_doc_max_bytes` (alapból 32 KiB) **kumulatív** költségvetés a teljes root→cwd láncra, nem fájlonkénti — ezt egy hivatalos GitHub-issue (`openai/codex#36371`) írja le, két, egymásnak ellentmondó doksi-oldalra hivatkozva.

### 7.2 „Memories" — jelenleg GLOBÁLIS, nincs projekt-izoláció (ez a releváns párhuzam a kutatott hiányossággal)

Ez a réteg **elkülönül** az AGENTS.md-től, és a saját tanult-kontextus rétege — ez az, amiről a hivatalos doksi (`learn.chatgpt.com/docs/customization/memories.md`, T1) ezt írja:
> „Codex stores memories under your Codex home directory. By default, that's `~/.codex`... The main memory files live under `~/.codex/memories/` and include summaries, durable entries, recent inputs, and supporting evidence from prior chats."

Ez a doksi **nem** említ projekt-szintű elkülönítést — és a forráskód (hivatalos PR-terv, `github.com/openai/codex/pull/11364`, „feat: mem v2 - PR1") ezt explicit meg is erősíti, hogy szándékosan és dokumentáltan globális:
> „**Target behavior** - One shared memory root only: `~/.codex/memories/`. **No per-cwd memory buckets, no cwd hash handling.**"
> „PR 3: Remove per-cwd memories and move to one global memory root ... Remove cwd-hash bucket helpers and normalization logic used only for memory pathing... Acceptance criteria: New runs only read/write `~/.codex/memories`. No new cwd-scoped consolidation jobs are enqueued."

Ez azt jelenti, hogy a Codex fejlesztői **korábban volt** valamilyen cwd-alapú (per-projekt) memória-elkülönítés, és **explicit döntéssel egyszerűsítették globálissá** — ellentétes irányba mozdulva, mint amit ez a kutatási projekt tervez.

A közösség ezt hiányként azonosította — egy nyitott hivatalos GitHub-issue (`openai/codex#18343`, „Scoped memory management for Codex (global, project...)"), amely szó szerint a mi kutatási kérdésünket veti fel:
> „Today, memory appears to be effectively global under the current `CODEX_HOME`, which can cause cross-project contamination over time. In practice, many memories are highly specific to one repository, one codebase, or one workflow, and should not automatically influence unrelated projects."
> „I would like Codex to support configurable memory scopes such as: **Global**: shared across all projects / **Project**: isolated to the current project/repo/worktree / **Hybrid**... / **Thread-only / no carryover**..."

Fontos módszertani megjegyzés: ennek az issue-nak a hosszú hozzászólásai (idézve a keresési találatban) külső, nem-hivatalos blogokra (`blog.kinthai.ai`) és állítólagos saját tapasztalatokra hivatkoznak egy „31 agent" méretű rendszerről — ezek **T3, nem ellenőrzött, közösségi vélemények**, nem hivatalos Codex-dokumentáció, és itt csak azért szerepelnek, mert jól illusztrálják a piaci konszenzust arról, milyen hierarchiát (global → namespace/org → project → session) szoktak javasolni ilyen esetekre.

**3–4. Hatókör, keresés:** mivel a „memories" réteg jelenleg egyetlen globális gyökeret használ, nincs projekt-szintű szűrés sem olvasáskor/injektáláskor — a `memories.use_memories` konfig csak be/kikapcsolja a teljes funkciót, nem szűri projekt szerint (`learn.chatgpt.com/docs/customization/memories.md`, T1).

---

## 8. Serena

**Forrás típusa:** T1 — `oraios.github.io/serena` (hivatalos doksi), `github.com/oraios/serena` (hivatalos forráskód).

### 1–2. Séma és a projekt forrása — háromféle mechanizmus, kontextustól függően

**(a) Explicit ágens-hívás konverzáció közben** (`activate_project` tool):
> „while in a conversation, by telling the LLM to activate a project, e.g., 'Activate the project /path/to/my_project' (for first-time activation with auto-creation) / 'Activate the project my_project'"
> „Note that this option requires the `activate_project` tool to be active, which it isn't in single-project contexts like `ide` or `claude-code` if a project is provided at startup."

**(b) Parancssori argumentum indításkor** (single-project mód, tipikusan Claude Code / IDE-kliensek esetén):
> „when the MCP server starts, by passing the project path or name as a command-line argument... `--project <path|name>`"

**(c) Automatikus cwd-detektálás:**
> „`--project-from-cwd`: auto-detect the project from current working directory (looking for a directory containing `.serena/project.yml` or `.git` in parent directories and activating the containing directory as the project root, if any). This option is intended for CLI-based agents like Claude Code, Gemini and Codex."

A `write_memory` tool sémája (hivatalos forráskód, `memory_tools.py`) — ez a **legpontosabb, szó szerinti válasz a 3. kérdésre** (ki dönt a hatókörről):
> „Write information (utf-8-encoded) about this project that can be useful for future tasks to a memory in md format. The memory name should be meaningful and can include '/' to organize into topics (e.g., 'auth/login/logic'). **If explicitly instructed, use the "global/" prefix** for writing a memory that is shared across projects (e.g., 'global/java/style_guide')"

### 3. Több szintű hatókör, ki dönt
Két ortogonális szint (hivatalos doksi, `045_memories.html`):
> „Two orthogonal memory scopes - per-project (committed alongside the code) and global (shared across all your projects) - can be combined freely."
> „Global memories use the top-level topic `global`, i.e. **whenever a memory name starts with `global/`**, it is stored in the global memories directory (`~/.serena/memories/global/`) and is shared across all projects."

A döntést tehát **az ágens hozza**, de a tool docstring kifejezetten korlátozza: „If explicitly instructed" / „The 'global' topic should only be used if explicitly instructed" — azaz alapértelmezésben mindig projekt-szintűre ír, a globálisra váltás user-utasításhoz kötött konvenció, nem automatikus/heurisztikus döntés.

Read-only védelem regex-mintával, ami szerver-/konfig-oldali szabályt is bevezet a döntésbe:
> „If you want to protect them from accidental modification by the agent, you can add regex patterns to `read_only_memory_patterns` in your global or project-level configuration. For example, setting 'global/.*' will mark all global memories as read-only."

A `query_project` tool egy negyedik, ritkább esetet fed le: explicit, **másik** regisztrált projekt kódjának/szimbólumainak lekérdezése (nem memóriaolvasás, hanem kód-hozzáférés) engedéllyel:
> „If, while working on a project, you want Serena to be able to read code or other information from another project... this can be enabled via the `query_project` tool."

### 4. Olvasás/keresés hatóköre
`list_memories`/`read_memory` alapból az aktív projekt memóriáit adja vissza, de topikkal címezhető a globális réteg is:
> „If the topic is omitted, both global and project-specific memories are returned." (forráskód, `MemoriesManager.list_memories`)

---

## 9. cognee

**Forrás típusa:** T1 — `docs.cognee.ai` (hivatalos), `raw.githubusercontent.com/topoteretes/cognee` README (hivatalos), `github.com/topoteretes/cognee` PR/commit (hivatalos forráskód-változtatás).

### 1–2. Séma és a projekt forrása — client-alapú, nem cwd-alapú
A cognee MCP-je **nem a munkakönyvtárból**, hanem **a csatlakozó MCP-kliens azonosságából** vezeti le az alapértelmezett „projektet" (itt: dataset):
> „**Agent Scoping (per-client default datasets)** — By default, each MCP client gets its own auto-named dataset (e.g. Cursor → `cursor_vscode_memory`, Claude Code → `claude_code_memory`) so different agents don't share memory unintentionally. The dataset is created on demand the first time a client writes to it."
> „LLM-direct calls to `cognify`, `remember`, `improve`, and `cognify_status` route to the agent-scoped dataset when `dataset_name` is omitted. Pass `dataset_name` explicitly to override (e.g. `dataset_name="main_dataset"` still works)."

Ez egy **negyedik, eddig nem látott mintázat**: a „projekt" itt nem a felhasználó munkakönyvtára vagy git-repója, hanem az **AI-kliens típusa** (Cursor vs. Claude Code vs. …) — ha valaki két különböző repót nyit meg ugyanabban a kliensben, alapból ugyanabba a datasetbe kerülnek, hacsak nem adnak meg explicit `dataset_name`-et.

A `remember`/`recall`/`forget` a jelenlegi (2026-as) egyszerűsített, ajánlott felület:
> „The MCP server intentionally exposes only the memory API: `remember`, `recall`, and `forget`... Operational helpers such as `cognify`, `search`, `list_data`, `delete`, `prune`, `improve`, and document retrieval helpers are kept internal and are not exposed as MCP tools [by default]."

Az alacsonyabb szintű `cognify`/`add` réteg paramétere (hivatalos Python API, `docs.cognee.ai/python-api/add`):
> „`async def add(data, dataset_name: str = 'main_dataset', ..., dataset_id: Optional[UUID] = None, ...)` — dataset_name: Name of the dataset to store data in. **Defaults to 'main_dataset'.**"

### 3. Több szintű hatókör, ki dönt
A cognee-nak nincs personal/project/shared elnevezésű beépített hierarchiája, hanem **datasetek** vannak, tulajdonossal, és egy explicit engedélyezési kapcsoló dönti el, mennyire szigetelt az adatbázis-réteg:
> „**`true` (default)** — each `(user, dataset)` pair gets its own per-dataset Kuzu + LanceDB... and search is strictly per-dataset. **`false`** — all datasets share one Kuzu graph DB and one LanceDB. The dataset filter is honored for top-level data points, but `GRAPH_COMPLETION` traversal can pull connected nodes from any dataset."

A megosztás (személyes → közös) explicit, tulajdonos-vezérelt engedélyezéssel történik, UUID-alapon, nem automatikusan:
> „Datasets sent by name will only map to datasets owned by the request sender. To search datasets not owned by the request sender, dataset UUID is needed. If dataset_ids is provided, the datasets name list is ignored."

### 4. Olvasás/keresés hatóköre
Alapból minden hozzáférhető datasetre kiterjed, ha nincs szűrés megadva:
> „`datasets` | `str` | `None` | Comma-separated dataset names. Name lookup is owner-scoped." és „`recall` currently accepts dataset names, not `dataset_ids`. If Bob is querying Alice's shared dataset, `datasets='shared_dataset'` can fail even when Bob has permission to use it. In that case, either omit `datasets` to search across all accessible datasets..."

---

## 10. Kiegészítés: az MCP hivatalos referencia „memory" szervere (baseline, nulladik szint)

**Forrás típusa:** T1 — `github.com/modelcontextprotocol/servers/blob/main/src/memory/README.md` (a Model Context Protocol szervezet hivatalos referencia-implementációja), megerősítve NPM-regisztri leírással (`registry.npmjs.org`) és a forráskóddal (`index.ts`) — 3 független forrás.

Ez a legegyszerűbb, „projekt" fogalom **nélküli** baseline: egyetlen JSONL-fájl, amelynek helyét kizárólag a szerver **üzemeltetője** (deploy-time env var) dönti el, tool-hívás vagy session-állapot nélkül:
> „`MEMORY_FILE_PATH`: Path to the memory storage JSONL file (default: `memory.jsonl` in the server directory)"

Nincs `create_entities`/`search_nodes` tool-nak semmilyen hatókör-paramétere (`entities`, `query` stb. az egyetlen bemenet) — a teljes gráf egyetlen lapos névtér, projekt/felhasználó megkülönböztetés nélkül. Ez azért fontos referenciapont, mert megmutatja, milyen a „nulla megoldás" azon a skálán, amin a többi rendszer mozog.

---

## 11. Kiegészítés: Anthropic saját `memory` tool-ja (Claude API, nem MCP)

**Forrás típusa:** T1 — `platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool` (Anthropic hivatalos doksi), megerősítve az Anthropic hivatalos blogbejegyzésével (`claude.com/blog/context-management`) és a hivatalos cookbook-kal (`github.com/anthropics/anthropic-cookbook`) — 3 független hivatalos forrás.

Ez nem MCP-szerver, hanem egy **kliens-oldali** Anthropic-tool (`memory_20250818`), amit érdemes megemlíteni, mert a célrendszer terve (markdown-fájl-alapú memória) erre erősen hasonlít, és mert világosan mutatja: itt a „projekt" fogalmát **szándékosan nem** definiálja maga az eszköz, hanem teljesen az azt beépítő alkalmazásra bízza:
> „Because the memory tool is client-side, Claude only requests memory operations. Your application executes each request against storage you control... The `/memories` path is a prefix that your handler maps onto real storage, such as a per-user directory or keys in a database. **Memory lives entirely in your application.**"

A tool parancskészlete fájlrendszer-műveletekre hasonlít (`view`, `create`, `str_replace`, `insert`, `delete`, `rename`), de nincs beépített `project`/`scope` paraméter egyikben sem — ezt a hívó alkalmazásnak kell megvalósítania a path-előtag konvenciójával.

---

## 12. Bónusz: más, csapatoknak szóló, távoli memória-MCP-szerverek (a `_kozos.txt` opcionális kérése)

Ezek **kis, nem „mainstream" közösségi projektek** — GitHub README-jük hivatalos forrásnak számít az adott projektre nézve (T1), de a módszertan előírása szerint minden lényeges állítást két független forrással kellene megerősíteni, és **ezt ezeknél a kis projekteknél nem sikerült**: nincs második, tőlük független dokumentáció vagy híradás róluk. Ezt itt jelzem — a lenti idézetek egyetlen forrásra (a saját README-jükre) támaszkodnak.

**`opspresso/mcp-memory`** — ez a legrelevánsabb minta a kutatási kérdés szempontjából, mert a README **kifejezetten megindokolja**, miért a fejléc és nem a tool-argumentum hordozza a bérlő/projekt-azonosítót:
> „**The tenant comes from a header and never from a tool argument** — an explicit `X-Memory-Tenant`, or the `X-Tenant-Id` header Agent Studio stamps on every MCP request when no explicit one is configured... A tool argument is something the *model* chose — and a model that can name its own tenant can read another project's memories by asking, including a model that was talked into it by text it retrieved a moment earlier. No amount of validation fixes that; the channel is wrong."

Ugyanez a szerver két hatókört különböztet meg (`remember` tool `scope` paramétere), és ez is dokumentált tool-séma-idézet:
> „**`remember` takes a `scope`.** `project` (the default, and what every memory written before scopes existed is) is shared by every conversation of the tenant. `conversation` is this conversation's alone... and is recalled, listed and de-duplicated only where the same `X-Conversation-Id` asks."

**`malinkaboy/MCP-Team-memory`** — itt a projekt-azonosító fejléc + UUID kombináció, és van egy explicit `memory_projects` tool a projektek kezelésére:
> „Minimal `.mcp.json` for Claude Code: ... `"headers": { "Authorization": "Bearer <YOUR_TOKEN>", "X-Project-Id": "<PROJECT_UUID>" }`" / „`memory_projects` | Manage projects (list/create/update/delete) |"

**`arpanroy41/nexmem-mcp`** — itt egy env-változó (`NEXMEM_TEAM_NAME`) dönti el a névteret, konfiguráció-időben, minden csapattag azonos értéket állít be:
> „**In team mode**, `NEXMEM_TEAM_NAME` determines the namespace. All team members who set the same team name share one knowledge graph." / „| `MODE=team, TEAM_NAME=platform-eng` | `team:platform-eng` | Everyone with same team name |"

---

## Összefoglaló táblázat

| Rendszer | Cél-/hatókör-paraméter | Projekt forrása | Szintek | Ki dönt a szintről | Keresés hatóköre |
|---|---|---|---|---|---|
| **basic-memory** | `project` (opcionális, tool-paraméter) | Sorrend: `BASIC_MEMORY_MCP_PROJECT` env → tool `project` paraméter → `default_project` config | Lapos, egyenrangú, elnevezett projektek (nincs personal/shared hierarchia) | Az ágens/felhasználó, minden híváskor | Csak az aktuális (aktív/megadott) projekt |
| **mem0 OSS** (`Memory`) | `user_id`/`agent_id`/`run_id` (min. 1 **kötelező**) | Kizárólag a hívó, minden híváskor; nincs env/config fallback | Nincs beépített hierarchia; a fogalmakat (user/agent/run) a hívó tölti meg tartalommal | A hívó (ágens) | Amit a `filters` explicit megad |
| **mem0 Platform** | `org_id`/`project_id` (kliens-init) + `user_id`/`agent_id`/`run_id` (hívásonként) | `project_id` a kliens konstruálásakor rögzített; a session-azonosítók hívásonként | org → project → user/agent/run (Pro csomag) | Fejlesztő (kliens-konfig) + ágens (hívásonkénti id-k) | A megadott entitás-szűrők szerint |
| **OpenMemory MCP** | Nincs tool-paraméter; `user_id`+`client_name` az URL-útvonalból | HTTP-kapcsolat (SSE endpoint `/{client_name}/sse/{user_id}`) | user (személyes) + app/client (eszköz), ACL-lel | Kapcsolat-konfiguráció (ki milyen URL-t kap) | Mindig a saját `user_id`-ra szűrve |
| **Letta** | `project_id` / `X-Project` fejléc (csak Cloud, agent-listázáshoz) | Cloud: query-param vagy fejléc, alapból a fiók default projektje; self-host: nincs ilyen fogalom | Memória-hatókört a **block attachment** adja (agent-specifikus vs. több agenthez csatolt „shared block") | Fejlesztő, explicit API-hívással (attach/detach) | Agent-scópolt (`archival_memory_search`), vagy globális block-lista label szerint |
| **Zep (hivatalos Memory MCP Server)** | **Nincs** — tudatosan kizárva a tool-argumentumból | OAuth-bejelentkezés → admin által konfigurált „connection" → automatikusan/választóval kiválasztott projekt | user graph (személyes) vs. standalone graph (`graph_id`, csapat/projekt) | Szerver-admin (connection-szintű policy: project-wide vagy UserGroup ABAC) | Alapból csak saját user graph; standalone graph csak explicit jogosultsággal |
| **Graphiti MCP (Zep OSS)** | `group_id` (opcionális, tool- vagy CLI-paraméter) | Tool `group_id` → hiányában a `--group-id` CLI-argumentum → hiányában `"main"` (jelenlegi doksi) | Lapos namespace, nincs beépített hierarchia | Az ágens (hívásonként) vagy az üzemeltető (indításkor) | `group_ids` lista is megadható; hiányában a konfigurált alapértelmezett group |
| **Claude Code (CLAUDE.md)** | Nincs tool-paraméter; fájlelhelyezés dönt | Munkakönyvtár-hierarchia bejárása (cwd → gyökér) | Managed policy → User → Project → Local (4 szint, fix precedencia) | A felhasználó (hova írja a fájlt) | Csak a cwd hierarchiája, gyökérig |
| **Claude Code (auto memory)** | Nincs tool-paraméter | Git-repó azonosítja a projektet (worktree-k közösek) | Csak projekt-szintű (nincs user-wide vagy org-wide auto memory) | Claude (az ágens) dönt, mit érdemes megjegyezni | Csak a saját projekt memóriakönyvtára |
| **Cursor (Rules)** | Nincs tool-paraméter; fájlelhelyezés + frontmatter | Workspace-gyökér (`.cursor/rules/`) | Project rules / User rules (fiók) / Team rules (Cursor szerver) | A felhasználó (hova/hogyan menti a rule-t) | Statikus betöltés relevancia/glob szerint, nincs MCP-szintű keresés natívan |
| **Codex (AGENTS.md)** | Nincs tool-paraméter; fájlelhelyezés dönt | Git-gyökértől a cwd-ig bejárás (`project_root_markers`, alapból `.git`) | Global (`~/.codex/AGENTS.md`) → Project (repo, könyvtáranként) | A felhasználó (hova írja a fájlt) | Csak a projekt-gyökér→cwd lánc |
| **Codex (Memories funkció)** | Nincs; jelenleg **explicit globális**, projekt-paraméter nélkül | `~/.codex/memories/` — dokumentáltan **nem** cwd-alapú (korábban volt cwd-hash, szándékosan eltávolítva) | Csak egy (globális) szint jelenleg; közösségi igény van projekt-szintre (nyitott GH-issue) | Nincs döntési pont — mindig globális | Globális, minden korábbi chat-en át, projekt-szűrés nélkül |
| **Serena** | `activate_project` tool / `--project` CLI / `--project-from-cwd` | (a) explicit ágens-hívás, (b) indítási argumentum, (c) automatikus cwd-detektálás (`.serena/project.yml` vagy `.git`) | Project memories vs. `global/` (előtaggal címzett, cross-project) | Az ágens, de a `global/` váltás **csak explicit felhasználói utasításra** (tool-docstring szerint) | Alapból aktív projekt; `global/` topikkal a globális réteg is; `query_project`-tel más projekt kódja is |
| **cognee** | `dataset_name`/`datasets` (opcionális) | **MCP-kliens azonossága** (Cursor, Claude Code stb.) → automatikus, kliens-specifikus dataset-név; explicit paraméterrel felülírható | Datasetek (tulajdonossal), nincs personal/project/shared elnevezés, de `ENABLE_BACKEND_ACCESS_CONTROL` per-(user,dataset) izolációt ad | A rendszer (kliens-azonosítás alapján) alapból; a hívó explicit `dataset_name`-mel felülbírálhatja | Alapból minden hozzáférhető dataset; explicit `datasets` paraméterrel szűkíthető |
| **MCP referencia `memory` szerver** | Nincs | Deploy-time env var (`MEMORY_FILE_PATH`) — egyetlen fájl | Nincs (egyetlen lapos gráf) | Az üzemeltető (deploy-konfig) | Az egész gráf, nincs szűrés |
| **Anthropic `memory` tool (Claude API)** | Nincs beépített; a `/memories` path-előtagot a befogadó alkalmazás értelmezi | A befogadó alkalmazás (nem az eszköz) dönti el, mit jelent egy path | Amit az alkalmazás épít rá (pl. per-user könyvtár) | A befogadó alkalmazás fejlesztője | Amit az alkalmazás engedélyez |
| *(bónusz)* `opspresso/mcp-memory` | Nincs tool-paraméter a bérlőhöz; `remember`-nek van `scope` (`project`/`conversation`) | HTTP fejléc (`X-Memory-Tenant` / `X-Tenant-Id`) — **explicit tervezési döntéssel** kizárva a tool-argumentum | Tenant (=projekt) → ezen belül `project` vs. `conversation` scope | Az üzemeltető (fejléc-konfig) a tenantről; az ágens a `scope`-ról | Tenant saját memóriái + az adott `X-Conversation-Id` |

---

## Ellentmondások

1. **mem0 „app_id mint projekt" vs. mem0 Platform valódi `project_id`-je.** A nem hivatalos `pinkpixel-dev/mem0-mcp` wrapper dokumentációja szerint „`appId` ... this **controls project scope**!", miközben a hivatalos Mem0 Platform (`docs.mem0.ai`, `LLM.md`) egy teljesen külön, valódi `project_id` mezőt definiál a `MemoryClient` konstruktorában (Pro-csomag, org→project hierarchia). A két fogalom terminológiailag ütközik az ökoszisztémán belül; a hivatalos mem0 dokumentáció sehol nem nevezi az `app_id`-t „projekt"-nek.

2. **Codex `project_doc_max_bytes` — fájlonkénti vs. kumulatív korlát.** Ezt egy hivatalos GitHub-issue (`openai/codex#36371`) dokumentálja explicit ellentmondásként két hivatalos doksi-oldal között:
   > „Two documentation pages describe `project_doc_max_bytes` in mutually exclusive ways, and the implementation only matches one of them... **The implementation matches Page B** [kumulatív]... So the budget is **cumulative and order-dependent**, not per file."
   Ez azt jelenti, hogy — a forráskóddal megerősítve (`agents_md.rs`) — egy nagy gyökér-szintű `AGENTS.md` teljesen kiütheti egy mélyebb, specifikusabb `AGENTS.md` betöltését, ami pont az ellenkezője annak, amit „split instructions across nested directories" tanácsként az egyik doksi-oldal javasol.

3. **Claude Code CLAUDE.md-konkatenáció sorrendje/elsőbbsége — történelmi félreértés, ma tisztázott.** Egy nyitott hivatalos GitHub-issue (`anthropics/claude-code#54955`) és egy korábbi feature-request (`#2353`) azt mutatja, hogy a felhasználók korábban nem tudták egyértelműen eldönteni, a „később olvasott" fájl (gyökér vagy cwd-közeli) élvez-e elsőbbséget. A **jelenlegi** hivatalos doksi (`code.claude.com/docs/en/memory`) ezt explicit, egyértelműen tisztázza: „instructions closer to where you launched Claude are read last" — vagyis a cwd-specifikus fájl a legutolsó, tehát facto legerősebb —, ami összhangban van a harmadik féltől származó összefoglalóval is („More specific memory takes precedence over broader memory"). A GitHub-issue-kban leírt korábbi zavart ezért **korábbi, mára feloldott** ellentmondásként jelzem, nem jelenleg is fennálló tartalmi ellentmondásként.

4. **Graphiti `group_id` alapértéke — dokumentált viselkedésváltozás.** A jelenlegi hivatalos README és a jelenlegi hivatalos „getting started" doksi is `"main"`-t ír a `group_id` alapértékeként, míg egy korábbi forráskód-verzió (`dbe21a19` commit, hivatalos repó) véletlenszerű UUID-t generált, ha nem adtak meg `group_id`-t. Ez nem egyidejű ellentmondás, hanem a projekt élete során bekövetkezett, dokumentált viselkedésváltozás — mindkét állapotot pontos verzió/commit-hivatkozással jelöltem.

---

## Amire NINCS forrás

- **Nem találtam hivatalos forrást arra**, hogyan dönt (ha egyáltalán) a Letta **self-hosted** (nem Cloud) telepítése bármiféle „projekt" vagy „workspace" elkülönítésről — a `project_id`/`X-Project` mechanizmus minden hivatalos forrásban kifejezetten „cloud only"-ként van megjelölve, és nem találtam dokumentációt arra, mi történik ugyanezzel önhosztolt Letta szerveren (feltehetően nincs ilyen fogalom, de ezt explicit kimondó hivatalos forrást nem találtam).
- **Nem sikerült két független forrással megerősítenem** a 12. fejezet bónusz-rendszereit (`opspresso/mcp-memory`, `malinkaboy/MCP-Team-memory`, `arpanroy41/nexmem-mcp`, `CedraInteractive/Memory-MCP`, `FlarelyLegal/memory-mcp`) — ezekhez kizárólag a saját GitHub README-jük állt rendelkezésre forrásként, harmadik féltől származó ismertetőt, adopciós adatot vagy független auditot egyikhez sem találtam. Ez konzisztens azzal, hogy ezek kis, feltehetően egy-két fejlesztő által karbantartott közösségi projektek.
- **Nem találtam részletes, hivatalos technikai leírást arra**, hogy a Cursor „User Rules” (fiók-szintű, Cursor Settings-ben tárolt) beállítás pontosan milyen szerver-oldali adatmodellben (milyen „projekt"-fogalommal, ha van neki) tárolódik — a hivatalos doksi csak annyit mond, hogy „stored on your Cursor account" és „sync when you sign in on another machine", technikai részletek (API, adatmodell) nem nyilvánosak.
- **A Zep hivatalos Memory MCP Server pontos ABAC-adatmodelljét** (hogyan van definiálva egy „UserGroup", ki hozza létre, milyen gránularitású a jogosultság) csak a felhasználói dokumentáció szintjén találtam meg, mélyebb (pl. adatbázis-séma szintű) hivatalos leírást nem.

---

## Meglátogatott és felderített linkek

| Cím | URL | Tier | Eszköz | Megjegyzés |
|---|---|---|---|---|
| MCP Tools Reference (basic-memory) | https://docs.basicmemory.com/reference/mcp-tools-reference | T1 | web_search_exa | Hivatalos; `project` paraméter, resolution order |
| Configuration (basic-memory) | https://docs.basicmemory.com/reference/configuration | T1 | web_search_exa | Hivatalos; `default_project`, `BASIC_MEMORY_MCP_PROJECT` |
| Content management (write_note szignatúra) | https://basicmachines-co-basic-memory.mintlify.app/api/mcp/content-management | T1 | web_search_exa | Hivatalos tükör; teljes Python szignatúra |
| Projects and folders | https://docs.basicmemory.com/concepts/projects-and-folders | T1 | web_search_exa | Hivatalos; hogyan dönt az ágens projekt-váltáskor |
| Local user guide (basic-memory) | https://docs.basicmemory.com/local/user-guide | T1 | web_search_exa | Hivatalos; single-project mode, URL resolution |
| CLI Reference (basic-memory) | https://docs.basicmemory.com/reference/cli-reference | T1 | web_search_exa | Hivatalos; `bm project default` |
| MCP tools reference (mintlify tükör, guides) | https://basicmachines.mintlify.app/guides/mcp-tools-reference | T1 | web_search_exa | Hivatalos tükör; „searches current project only” idézet |
| MCP tools (local) | https://docs.basicmemory.com/local/mcp-tools-local | T1 | web_search_exa | Hivatalos |
| PARAMETER_GUIDE.md (pinkpixel mem0-mcp) | https://github.com/pinkpixel-dev/mem0-mcp/blob/main/PARAMETER_GUIDE.md | T3 | web_search_exa | Nem hivatalos wrapper; `appId`="project scope" állítás |
| add_memory — Mem0 MCP Server (Glama) | https://glama.ai/mcp/servers/mem0ai/mem0-mcp/tools/add_memory | T2 | web_search_exa | Harmadik féltől katalogizált tool-séma, hivatalos szerver alapján |
| Add Memory (mem0 docs) | https://docs.mem0.ai/core-concepts/memory-operations/add | T1 | web_search_exa | Hivatalos; user/session identifierek |
| Schema — Mem0 MCP Server (Glama) | https://glama.ai/mcp/servers/mem0ai/mem0-mcp/schema | T2 | web_search_exa | Harmadik féltől katalogizált séma |
| pinkpixel-dev/mem0-mcp README | https://github.com/pinkpixel-dev/mem0-mcp/ | T3 | web_search_exa | Nem hivatalos wrapper, elsőbbségi sorrend idézet |
| mem0.ai/platform/mem0-mcp | https://docs.mem0.ai/platform/mem0-mcp | T1 | web_search_exa | Hivatalos; tool-lista |
| mem0ai/mem0-mcp (hivatalos repó) | https://github.com/mem0ai/mem0-mcp | T1 | web_search_exa | Hivatalos MCP wrapper, `MEM0_DEFAULT_USER_ID` |
| mem0-open-mcp (PyPI) | https://pypi.org/project/mem0-open-mcp/0.1.15/ | T3 | web_search_exa | Nem hivatalos csomag, csak kiegészítő |
| SDK & Tools changelog (mem0) | https://docs.mem0.ai/changelog/sdk | T1 | web_search_exa | Hivatalos; entity-id validáció, filters kontra top-level |
| How to make your clients more context-aware with OpenMemory MCP | https://mem0.ai/blog/how-to-make-your-clients-more-context-aware-with-openmemory-mcp | T1 | web_search_exa | Hivatalos blog; SSE endpoint felépítés |
| mem0/openmemory/api/app/mcp_server.py (main) | https://github.com/mem0ai/mem0/blob/ece7ff6b/openmemory/api/app/mcp_server.py | T1 | web_search_exa | Hivatalos forráskód; contextvars, add_memories |
| mem0/openmemory/.../mcp_server.py (3e6ab394) | https://github.com/mem0ai/mem0/blob/3e6ab394/openmemory/api/app/mcp_server.py | T1 | web_search_exa | Ugyanaz más commit — megerősítés |
| Mem0 OpenCode integráció | https://docs.mem0.ai/integrations/opencode | T1 | web_search_exa | Hivatalos; git-alapú automatikus projekt-detektálás, scope tábla |
| OpenMemory — AI Memory MCP Server | https://mem0.ai/openmemory | T1 | web_search_exa | Hivatalos termékoldal |
| Introducing OpenMemory MCP | https://mem0.ai/blog/introducing-openmemory-mcp | T1 | web_search_exa | Hivatalos launch blog |
| mem0-open-mcp v0.1.15 (PyPI, config) | https://pypi.org/project/mem0-open-mcp/0.1.15/ | T3 | web_search_exa | Nem hivatalos, más URL-struktúra bemutatása |
| Letta memory blocks index | https://docs.letta.com/guides/core-concepts/memory/memory-blocks/index.md | T1 | web_search_exa | Hivatalos; block-modell, shared blocks |
| Letta archival memory | https://docs.letta.com/v1-sdk/memory/archival-memory/ | T1 | web_search_exa | Hivatalos |
| Letta memory blocks (v1-sdk) | https://docs.letta.com/v1-sdk/memory/memory-blocks/ | T1 | web_search_exa | Hivatalos, ismétlés más URL-en |
| Letta Blocks API (typescript) | https://docs.letta.com/api/typescript/resources/agents/subresources/blocks/ | T1 | web_search_exa | Hivatalos; `project_id?` mező a block/agent API-ban |
| Letta Memory overview | https://docs.letta.com/agent-sdk/memory/index.md | T1 | web_search_exa | Hivatalos; MemFS, dreaming |
| Letta MemFS | https://docs.letta.com/concepts/memfs/index.md | T1 | web_search_exa | Hivatalos; git-repó-alapú memória |
| Letta stateful agents | https://docs.letta.com/guides/core-concepts/stateful-agents/index.md | T1 | web_search_exa | Hivatalos alapfogalmak |
| letta-agents-api-openapi.yml (tükör) | https://raw.githubusercontent.com/api-evangelist/letta/refs/heads/main/openapi/letta-agents-api-openapi.yml | T2 | web_search_exa | Harmadik féltől tükrözött hivatalos OpenAPI-spec; `project_id` leírás |
| letta/server/rest_api/routers/v1/agents.py | https://github.com/letta-ai/letta/blob/67013ef1/letta/server/rest_api/routers/v1/agents.py | T1 | web_search_exa | Hivatalos forráskód; `X-Project` header, `project_id` query |
| Letta Templates API | https://docs.letta.com/api/resources/templates/ | T1 | web_search_exa | Hivatalos; `project_slug` |
| letta-ai/letta compare 0.11.7...0.12.1 | https://github.com/letta-ai/letta/compare/0.11.7...0.12.1 | T1 | web_search_exa | Hivatalos changelog; „change project to project slug” |
| Letta Agents API (apis.io tükör) | https://apis.io/apis/letta/letta-agents-api/ | T2 | web_search_exa | Harmadik féltől katalogizált API-lista |
| Letta Templates (typescript) | https://docs.letta.com/api/typescript/resources/templates/ | T1 | web_search_exa | Hivatalos |
| Zep Memory MCP Server | https://help.getzep.com/memory-mcp-server | T1 | web_search_exa | Hivatalos; „no user/graph/project argument” kulcsidézet |
| Zep — Share Memory Across Users (group graphs) | https://help.getzep.com/v2/cookbook/how-to-share-memory-across-users-using-group-graphs.mdx | T1 | web_search_exa | Hivatalos; `group_id` API-példa |
| Zep quickstart | https://help.getzep.com/v2/quickstart.mdx | T1 | web_search_exa | Hivatalos; user graph vs. group graph |
| Zep agent memory quickstart | https://help.getzep.com/quick-start-guide | T1 | web_search_exa | Hivatalos |
| Zep MCP + Claude Agent SDK (Composio) | https://composio.dev/toolkits/zep/framework/claude-agents-sdk | T3 | web_search_exa | Harmadik féltől integrációs útmutató, csak kiegészítő |
| Memory for every agent your team uses (Zep blog) | https://blog.getzep.com/agent-memory-mcp/ | T1 | web_search_exa | Hivatalos; ABAC, connection-modell részletesen |
| mcp-server-zep-cloud (fshamim) | https://github.com/fshamim/mcp-server-zep-cloud/blob/main/README.md | T3 | web_search_exa | Nem hivatalos (közösségi) Zep-wrapper, `ZEP_DEFAULT_USER_ID` prioritási sorrend — csak kiegészítő, más architektúra mint a hivatalos MCP |
| Zep Documentation MCP server | https://help.getzep.com/docs-mcp-server.mdx | T1 | web_search_exa | Hivatalos, de más célú szerver (doksi-kereső, nem memória) |
| Graphiti MCP Server (Zep docs) | https://help.getzep.com/graphiti/getting-started/mcp-server | T1 | web_search_exa | Hivatalos |
| graphiti/mcp_server/README.md | https://github.com/getzep/graphiti/blob/main/mcp_server/README.md | T1 | web_search_exa | Hivatalos; `--group-id`, alapérték „main” |
| Graphiti cursor_rules.md | https://github.com/getzep/graphiti/blob/main/mcp_server/docs/cursor_rules.md | T1 | web_search_exa | Hivatalos; ágens-instrukciók a memóriahasználathoz |
| graphiti_mcp_server.py (dbe21a19) | https://github.com/getzep/graphiti/blob/dbe21a1975b0747cd450ee3aa1b2c72b26f59230/mcp_server/graphiti_mcp_server.py | T1 | web_search_exa | Hivatalos, korábbi verzió — UUID alapérték |
| mcp_server/src/graphiti_mcp_server.py (d631437d) | https://github.com/getzep/graphiti/blob/d631437d/mcp_server/src/graphiti_mcp_server.py | T1 | web_search_exa | Hivatalos, `add_memory` teljes docstring |
| mcp_server/src/graphiti_mcp_server.py (0290e4de) | https://github.com/getzep/graphiti/blob/0290e4de/mcp_server/src/graphiti_mcp_server.py | T1 | web_search_exa | Hivatalos, `search_memory_facts` |
| mcp_server/src/graphiti_mcp_server.py (b59d4ba0) | https://github.com/getzep/graphiti/blob/b59d4ba0/mcp_server/src/graphiti_mcp_server.py | T1 | web_search_exa | Hivatalos, legfrissebb `add_memory` bővített paraméterekkel |
| mcp_server/src/graphiti_mcp_server.py (4f62cfe7) | https://github.com/getzep/graphiti/blob/4f62cfe7/mcp_server/src/graphiti_mcp_server.py | T1 | web_search_exa | Hivatalos, ismétlés más commit-on — megerősítés |
| How Claude remembers your project (Claude Code memory) | https://code.claude.com/docs/en/memory | T1 | web_search_exa | Hivatalos, Anthropic; teljes CLAUDE.md + auto memory leírás |
| Claude Code memory (rsc variáns) | https://code.claude.com/docs/en/memory?_rsc=4Vrbm42DZc3Y7r9j | T1 | web_search_exa | Ugyanaz a hivatalos oldal, technikai URL-variáns — megerősítés |
| GH issue #54955 (CLAUDE.md concatenation ambiguity) | https://github.com/anthropics/claude-code/issues/54955 | T2 | web_search_exa | Hivatalos repó issue-ja, korábbi doksi-félreérthetőség dokumentálása |
| GH issue #2353 (hierarchical CLAUDE.md) | https://github.com/anthropics/claude-code/issues/2353 | T2 | web_search_exa | Hivatalos repó issue-ja, felhasználói elvárás vs. tényleges működés |
| Claude Code Memory Docs (Claudeable, tükör) | https://claudeable.co/claude-md/claude-code-memory-docs | T2 | web_search_exa | Harmadik féltől összefoglaló a hivatalos doksi alapján |
| Claude Code memory system (developertoolkit.ai) | https://developertoolkit.ai/en/claude-code/advanced-techniques/memory-system/ | T2 | web_search_exa | Harmadik féltől részletes összefoglaló, megerősíti a hivatalos doksit |
| Claude Code Memory (claude.yourdocs.dev) | https://claude.yourdocs.dev/docs/claude-code/memory | T2 | web_search_exa | Harmadik féltől tükör/összefoglaló |
| lenneTech/claude-code docs-cache/memory.md | https://github.com/lenneTech/claude-code/blob/main/.claude/docs-cache/memory.md | T2 | web_search_exa | Harmadik fél által cache-elt hivatalos doksi-szöveg, `autoMemoryDirectory` részletek |
| Cursor Rules docs | https://cursor.com/docs/rules | T1 | web_search_exa | Hivatalos; `.mdc`, frontmatter, AGENTS.md |
| Cursor Rules (help) | https://cursor.com/help/customization/rules.md | T1 | web_search_exa | Hivatalos; user/project/team rules |
| Cursor Rules (prod tükör) | https://prod.cursor.com/help/customization/rules | T1 | web_search_exa | Hivatalos staging-tükör, azonos tartalom — megerősítés |
| cursor-project-memory usage doc | https://github.com/general-alexson/cursor-project-memory/blob/main/doc/usage.md | T3 | web_search_exa | Nem hivatalos VS Code/Cursor kiterjesztés, csak kiegészítő |
| general-alexson/cursor-project-memory | https://github.com/general-alexson/cursor-project-memory | T3 | web_search_exa | Nem hivatalos, ugyanaz a projekt |
| memories.sh — Cursor integráció | https://memories.sh/docs/integrations/cursor | T3 | web_search_exa | Nem hivatalos, harmadik féltől MCP-integráció Cursorhoz |
| Cursor rules gyakorlati útmutató (learncursor.dev) | https://www.learncursor.dev/learn/cursor-rules | T2 | web_search_exa | Harmadik féltől, hivatalos doksira alapuló összefoglaló |
| Documentation as context (developertoolkit.ai) | https://developertoolkit.ai/en/shared-workflows/context-management/documentation-as-context/ | T2 | web_search_exa | Harmadik féltől, több rendszert összehasonlító cikk |
| Custom instructions with AGENTS.md (Codex) | https://developers.openai.com/codex/guides/agents-md | T1 | web_search_exa | Hivatalos OpenAI; discovery precedencia |
| Customization (Codex) | https://developers.openai.com/codex/concepts/customization | T1 | web_search_exa | Hivatalos; AGENTS.md + Memories mint két külön réteg |
| Custom instructions with AGENTS.md (learn.chatgpt.com tükör) | https://learn.chatgpt.com/docs/agent-configuration/agents-md | T1 | web_search_exa | Hivatalos tükör, azonos szöveg — megerősítés |
| codex-rs/core/src/project_doc.rs | https://github.com/openai/codex/blob/d807d44a/codex-rs/core/src/project_doc.rs | T1 | web_search_exa | Hivatalos forráskód; project root marker logika |
| codex-rs/core/src/agents_md.rs (31519549) | https://github.com/openai/codex/blob/31519549/codex-rs/core/src/agents_md.rs | T1 | web_search_exa | Hivatalos forráskód |
| GH issue #36371 (project_doc_max_bytes ellentmondás) | https://github.com/openai/codex/issues/36371 | T1 | web_search_exa | Hivatalos repó issue, doksi-ellentmondás dokumentálása |
| AGENTS.md (learn.chatgpt.com, .md variáns) | https://learn.chatgpt.com/docs/agent-configuration/agents-md.md | T1 | web_search_exa | Hivatalos tükör |
| codex-rs/core/src/agents_md.rs (ac4332c0) | https://github.com/openai/codex/blob/ac4332c05b11e00ae775a24cb762edc05c5b5932/codex-rs/core/src/agents_md.rs | T1 | web_search_exa | Hivatalos forráskód, másik commit — megerősítés |
| The Project Workflow (Serena) | https://oraios.github.io/serena/02-usage/040_workflow.html | T1 | web_search_exa | Hivatalos; activate_project, onboarding |
| Serena clients doc (030_clients.md) | https://github.com/oraios/serena/blob/9cd33aa5/docs/02-usage/030_clients.md | T1 | web_search_exa | Hivatalos; kliens-specifikus aktiválási minták |
| Serena workflow_tools.py | https://github.com/oraios/serena/blob/a0984015/src/serena/tools/workflow_tools.py | T1 | web_search_exa | Hivatalos forráskód; onboarding tool |
| Serena running doc (020_running.md) | https://github.com/oraios/serena/blob/981f560f/docs/02-usage/020_running.md | T1 | web_search_exa | Hivatalos; `--project-from-cwd` |
| Serena project.py (9cd33aa5) | https://github.com/oraios/serena/blob/9cd33aa5/src/serena/project.py | T1 | web_search_exa | Hivatalos forráskód, korábbi MemoriesManager |
| Serena project.py (a0984015) | https://github.com/oraios/serena/blob/a0984015/src/serena/project.py | T1 | web_search_exa | Hivatalos forráskód, frissebb MemoriesManager (`GLOBAL_TOPIC`) |
| oraios/serena README | https://github.com/oraios/serena | T1 | web_search_exa | Hivatalos főrepó |
| Serena agent.py | https://github.com/oraios/serena/blob/a0984015/src/serena/agent.py | T1 | web_search_exa | Hivatalos forráskód; activate_project logika |
| Serena Memories & Onboarding (045_memories.html) | https://oraios.github.io/serena/02-usage/045_memories.html | T1 | web_search_exa | Hivatalos; `global/` prefix teljes magyarázata |
| Serena docs/045_memories.md (GitHub) | https://github.com/oraios/serena/blob/main/docs/02-usage/045_memories.md | T1 | web_search_exa | Hivatalos, ugyanaz forrásból — megerősítés |
| Serena memory_tools.py (a0984015) | https://github.com/oraios/serena/blob/a0984015/src/serena/tools/memory_tools.py | T1 | web_search_exa | Hivatalos forráskód; `write_memory`/`RenameMemoryTool` docstring, „If explicitly instructed” |
| Serena memory_tools.py (0c915bd1) | https://github.com/oraios/serena/blob/0c915bd1/src/serena/tools/memory_tools.py | T1 | web_search_exa | Hivatalos, azonos tartalom más commit — megerősítés |
| Serena project.py (0c915bd1) | https://github.com/oraios/serena/blob/0c915bd1/src/serena/project.py | T1 | web_search_exa | Hivatalos; `_is_global` teljes implementáció |
| cognee MCP Tools Reference | https://docs.cognee.ai/cognee-mcp/mcp-tools | T1 | web_search_exa | Hivatalos; `remember`/`recall`/`forget` séma |
| cognee dataset support commit | https://github.com/topoteretes/cognee/commit/1fb2af18555f064630b5157804a421d805589fea | T1 | web_search_exa | Hivatalos forráskód-commit |
| cognee PR #2459 | https://github.com/topoteretes/cognee/pull/2459 | T1 | web_search_exa | Hivatalos PR, `dataset_name` bevezetése |
| cognee search API | https://docs.cognee.ai/api-reference/search/search | T1 | web_search_exa | Hivatalos API-referencia; `datasets`/`dataset_ids` |
| cognee cognify API | https://docs.cognee.ai/api-reference/cognify/cognify | T1 | web_search_exa | Hivatalos API-referencia |
| cognee-mcp README (raw) | https://raw.githubusercontent.com/topoteretes/cognee/HEAD/cognee-mcp/README.md | T1 | web_search_exa | Hivatalos; „Agent Scoping (per-client default datasets)” kulcsidézet |
| cognee add() Python API | https://docs.cognee.ai/python-api/add | T1 | web_search_exa | Hivatalos; `dataset_name` alapérték |
| cognee add API (mintlify) | https://cognee.mintlify.app/api-reference/add/add | T1 | web_search_exa | Hivatalos tükör — megerősítés |
| Anthropic memory tool docs | https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool | T1 | web_search_exa | Hivatalos; kliens-oldali memória-tool |
| Context editing docs | https://platform.claude.com/docs/en/build-with-claude/context-editing | T1 | web_search_exa | Hivatalos; kapcsolódó funkció |
| Memory & context management cookbook | https://platform.claude.com/cookbook/tool-use-memory-cookbook?2f226f2c_page=2 | T1 | web_search_exa | Hivatalos cookbook |
| Managing context on Claude Developer Platform (blog) | https://claude.com/blog/context-management | T1 | web_search_exa | Hivatalos launch blog |
| Effective context engineering for AI agents | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | T1 | web_search_exa | Hivatalos Anthropic engineering blog |
| anthropic-cookbook memory_cookbook.ipynb | https://github.com/anthropics/anthropic-cookbook/blob/main/tool_use/memory_cookbook.ipynb | T1 | web_search_exa | Hivatalos cookbook forráskód |
| modelcontextprotocol/servers memory README | https://github.com/modelcontextprotocol/servers/blob/main/src/memory/README.md | T1 | web_search_exa | Hivatalos MCP referencia-szerver |
| modelcontextprotocol/servers memory index.ts | https://github.com/modelcontextprotocol/servers/blob/main/src/memory/index.ts | T1 | web_search_exa | Hivatalos forráskód |
| memory README (raw tükör) | https://raw.githubusercontent.com/modelcontextprotocol/servers/main/src/memory/README.md | T1 | web_search_exa | Hivatalos, raw tükör — megerősítés |
| @modelcontextprotocol/server-memory (npm registry) | https://registry.npmjs.org/%40modelcontextprotocol%2Fserver-memory | T1 | web_search_exa | Hivatalos csomag-leírás |
| @modelcontextprotocol/server-memory (npmjs.com) | https://www.npmjs.com/package/@modelcontextprotocol/server-memory | T1 | web_search_exa | Hivatalos, azonos tartalom — megerősítés |
| memory index.ts (d31124c9) | https://github.com/modelcontextprotocol/servers/blob/d31124c9/src/memory/index.ts | T1 | web_search_exa | Hivatalos, másik commit — megerősítés |
| Letta OpenAPI project_id (2. keresés, api-evangelist tükör) | https://raw.githubusercontent.com/api-evangelist/letta/refs/heads/main/openapi/letta-agents-api-openapi.yml | T2 | web_search_exa | Ismételt találat, project_id/X-Project megerősítés |
| Antigravity Projects docs | https://antigravity.google/docs/projects/ | T3 | web_search_exa | Kapcsolódó, de más eszköz (Google Antigravity) — nem Letta; irreleváns találat, nem használtam fel állításhoz |
| modelcontextprotocol memory (egyéb generikus „project” találatok, Hamsa/Evidently/Sippulse/CloudStation/Upsolve) | (több URL, ld. keresési log) | T3 | web_search_exa | Általános „mi az a Projekt” SaaS-dokumentációk, nem memória-MCP-k — csak a keresési zaj dokumentálására, nem használtam fel állításhoz |
| prmichaelsen/remember-mcp | https://github.com/prmichaelsen/remember-mcp/ | T3 | web_search_exa | Nem hivatalos, multi-tenant memória-MCP; csak jelzésértékű, nem idéztem a fő táblázatban |
| FlarelyLegal/memory-mcp | https://github.com/FlarelyLegal/memory-mcp | T3 | web_search_exa | Nem hivatalos; namespace-RBAC minta, egyetlen forrásból |
| opspresso/mcp-memory | https://github.com/opspresso/mcp-memory | T3 | web_search_exa | Nem hivatalos, de erős releváns idézet a fejléc-alapú tenant-döntésről |
| Coordination Memory MCP (Glama, yanqiw) | https://glama.ai/mcp/servers/yanqiw/comem | T3 | web_search_exa | Nem memória-tárolás, hanem multi-agent koordináció — nem releváns, nem idéztem |
| datamcpapp/datamcp-app | https://github.com/datamcpapp/datamcp-app | T3 | web_search_exa | Nem hivatalos, hosztolt memória-MCP projekt-fogalommal — csak jelzésértékű |
| CedraInteractive/Memory-MCP (tükör) | https://github.laiyagushi.com/CedraInteractive/Memory-MCP | T3 | web_search_exa | Nem hivatalos, `project` mező a memory_upsert tool-ban |
| Antony-A-tech/MCP-Team-memory (malinkaboy fork) | https://github.com/malinkaboy/MCP-Team-memory | T3 | web_search_exa | Nem hivatalos; `X-Project-Id` fejléc + `memory_projects` tool |
| arpanroy41/nexmem-mcp | https://github.com/arpanroy41/nexmem-mcp | T3 | web_search_exa | Nem hivatalos; `NEXMEM_TEAM_NAME` env-alapú névtér |

---

# SQ03 — Hogyan tudja egy kliens átadni a projektet egy távoli MCP-szervernek, és mit adnak a munkamenet-indító hookok?

**Módszertani megjegyzés (degradált mód):** Ez a kutatás egyetlen kutató-ügynökként készült, alügynökek indítása nélkül — a futtatási környezet nem tett lehetővé Task/Agent-alapú párhuzamos alügynök-indítást ebben a munkamenetben, ezért a `deep-web-research` skill többügynökös pipeline-ja helyett szekvenciális Exa-kereséssel/olvasással dolgoztam fel mind a hat klienst. Kizárólag `mcp__Exa__web_search_exa` és `mcp__Exa__web_fetch_exa` eszközöket használtam keresésre és oldalolvasásra, a beépített WebSearch/WebFetch-et nem.

A mai dátum **2026-09-25**. Minden verziószámot és dátumot jelöltem, ahol a forrás megadta.

---

## Rövid válasz

Mind a hat kliens támogat projektkönyvtárban élő MCP-konfigurációt, remote (HTTP) szerver URL-lel és egyedi HTTP-fejléccel, és mindegyiknél a projektszintű config felülírja/kiegészíti a felhasználói configot (jellemzően a projektszintű nyer ütközésnél, kivéve amit biztonsági okból tiltanak felülírni). Változó-behelyettesítés mindenhol van, de eltérő szintaxissal és eltérő megbízhatósággal (Cursor `${env:NAME}`-je pl. dokumentáltan hibás volt remote fejlécekben egy ideig). MCP **roots** képességet a Claude Code, a Gemini CLI, a Cursor (dokumentáció szerint) és a VS Code/GitHub Copilot is támogatja/hirdeti, de a Cursor esetén ellentmondás van: a kliens hirdeti a `roots` capability-t, de a `roots/list` hívás ténylegesen `-32601 Method not found` hibát ad — vagyis a gyakorlatban nem működik. A Codex CLI forráskódja explicit `roots: None`-t küld, tehát NEM támogatja a roots-ot. Munkamenet-indító hook (`SessionStart`) létezik Claude Code-ban, Codexben, Gemini CLI-ban, Cursorban és a GitHub Copilot/VS Code Agent Hostban is; az Antigravity hooks-rendszeréből viszont **hiányzik** a SessionStart esemény (csak Pre/PostToolUse, Pre/PostInvocation, Stop van). Külön HTTP hook-típusa (`type: "http"`, közvetlen URL-re POST-olás) csak a Claude Code-nak van dokumentálva; a Codex, a Gemini CLI és az Antigravity jelenleg csak `"command"` típusú (shell) hookot támogat, a GitHub Copilot/Agent Host viszont SDK-szinten explicit HTTP hook handlert is definiál. A kimeneti korlátra vonatkozó állítások megerősítve: **Claude Code 10 000 karakter** (a hivatalos doksi szerint), **Codex kb. 2500 token** (hivatalosan is így írják) — mindkettő igaz. Az OAuth-tárolás projektenkénti elkülönítése a leggyengébb pont: Codexnél és Gemini CLI-nál a token-tár kulcsa csak a szervernév/URL, tehát globális; Claude Code-nál jelenleg (2026 közepén nyitott hibajegyek szerint) szintén gyakorlatilag globális/kiszivárgó a projekthatárok között annak ellenére, hogy a szerver-config maga project/local/user szinten skálázható; a Cursor az egyetlen, ahol dokumentáltan és megerősítve **projektenként külön** OAuth-állapot (`~/.cursor/projects/<id>/mcp-auth.json`) van — bár ennek is megvan a maga hibája (worktree-k nem öröklik).

---

## 1. Claude Code

### 1.1 Projektszintű MCP-konfiguráció

A `.mcp.json` a projekt gyökerében él, három hatókör van (`local`, `project`, `user`), és a `project` hatókör pontosan ez a fájl:

> "Project-scoped servers enable team collaboration by storing configurations in a `.mcp.json` file at your project's root directory. […] Check `.mcp.json` into version control so everyone on your team gets the same MCP tools and services." — https://code.claude.com/docs/en/mcp

Remote HTTP szerver és fejléc:

> "```json\n{\n \"mcpServers\": {\n \"claude-code-docs\": {\n \"type\": \"http\",\n \"url\": \"https://code.claude.com/docs/mcp\"\n }\n }\n}\n```" — https://code.claude.com/docs/en/mcp-quickstart

> "`headers`: for HTTP server authentication" — https://code.claude.com/docs/en/mcp

Változó-behelyettesítés `${VAR}` és `${VAR:-default}` formában, `command`/`args`/`env`/`url`/`headers` mezőkben:

> "Claude Code supports environment variable expansion in `.mcp.json` files… `${VAR}`… `${API_…}`" és "Claude Code sets `CLAUDE_PROJECT_DIR` in the spawned server's environment to the project root" — https://code.claude.com/docs/en/mcp

Munkakönyvtár-behelyettesítés is van: `${CLAUDE_PROJECT_DIR}` a project gyökerét jelenti (ugyanaz, amit a hookok is kapnak).

Hatókör-elsőbbség: `local` > `project` (a helyi felülírja a projekt-szintűt névütközésnél), és a `.mcp.json`-ból származó szervereket a kliens minden interaktív munkamenetnél jóváhagyásra kéri:

> "For security reasons, Claude Code prompts for approval in interactive sessions before using project-scoped servers from `.mcp.json` files." — https://code.claude.com/docs/en/mcp

### 1.2 Roots

Claude Code támogatja a `roots/list`-et, és a `list_changed` értesítést is küldi (v2.1.203 óta bővült ki `--add-dir`-rel hozzáadott könyvtárakkal):

> "Claude Code answers `roots/list` with the session's launch directory plus every additional working directory you've granted with `--add-dir`, `/add-dir`, or the `additionalDirectories` setting. Claude Code sends `notifications/roots/list_changed` when that set changes. Before v2.1.203, `roots/list` returned only the launch directory and Claude Code didn't send `notifications/roots/list_changed`." — https://code.claude.com/docs/en/mcp

Ez transzportfüggetlen (a kliens roots-képessége a kapcsolat szintjén van, nem csak stdio szervereknél), amit a harmadik féltől származó kompatibilitási táblázat is megerősít:

> "| Claude Code | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌, ❌ |" (Resources/Prompts/Tools/Discovery/Sampling/Tasks/**Roots**/Elicitation oszlopok) — https://github.com/apify/mcp-client-capabilities

Megjegyzés: korábban (2025 közepéig) a `roots` capability-t hirdette, de nem válaszolt rá — ezt egy 2025 júliusi hibajegy (#3315) és egy külön feature-kérés (#53861) is dokumentálja; a tényleges implementáció ezt követően készült el.

### 1.3 Munkamenet-indító hook

`SessionStart` esemény, ami induláskor és resume/clear/compact után is fut:

> "`SessionStart` | When a session begins or resumes" — https://code.claude.com/docs/en/hooks

Bemenet: `session_id`, `cwd`, `transcript_path`, `hook_event_name`, `source` (`startup`/`resume`/`clear`/`compact`/`fork`), opcionálisan `model`, `agent_type`. Git-infót a hook maga kérheti le (pl. `git log --oneline -5` a saját szkriptjében), nincs beépített git-mező.

> "```json\n{\n \"session_id\": \"abc123\",\n \"transcript_path\": \"…\",\n \"cwd\": \"…\",\n \"hook_event_name\": \"SessionStart\",\n \"source\": \"startup\",\n \"model\": \"claude-sonnet-5\"\n}\n```" — https://claude-wiki.com/hooks-reference.html (a hivatalos `code.claude.com/docs/en/hooks-guide` tartalmának tükrözése)

**Külön HTTP hook-típus IGEN van** (ezt a kutatási kérdés kifejezetten kérte ellenőrizni):

> "HTTP hooks (`type: \"http\"`): send the event's JSON input as an HTTP POST request to a URL. The endpoint communicates results back through the response body using the same JSON output format as command hooks." — https://code.claude.com/docs/en/hooks

> "| `url` | yes | URL to send the POST request to |\n| `headers` | no | … Values support environment variable interpolation … |\n| `allowedEnvVars` | no | … |" — https://code.claude.com/docs/en/hooks

A `SessionStart`-ra írt HTTP hook is pontosan ugyanezt a JSON bemenetet kapja POST body-ként, mint a command hook stdin-en.

Kimenet a kontextusba: `hookSpecificOutput.additionalContext` (SessionStart esetén a beszélgetés elejére kerül, még az első prompt előtt), plusz plain stdout is elfogadott.

**Kimeneti korlát: 10 000 karakter — MEGERŐSÍTVE:**

> "Hook output strings, including `additionalContext`, `systemMessage`, and plain stdout, are capped at 10,000 characters." — https://code.claude.com/docs/en/hooks

> "If a value exceeds 10,000 characters, Claude Code writes the full text to a file in the session directory and passes Claude the file path with a short preview instead." — https://code.claude.com/docs/en/hooks

Két nyílt hibajegy azonban azt mutatja, hogy a gyakorlatban a túllépés esetén nem a teljes 10 000, hanem csak kb. **2000 karakteres** preview jut el a modellhez (a fájlba mentés melletti előnézet mérete kisebb, mint maga a limit):

> "The documentation says that hook output his truncated after 10,000 characters, but I observe that if you breach this limit, the output is truncated to 2000 characters." — https://github.com/anthropics/claude-code/issues/44086

> "I measured 18,057 bytes emitted and ~2,000 delivered — 11% arrived." — https://github.com/anthropics/claude-code/issues/84021

### 1.4 OAuth per projekt

Konfigurációs szinten (`local`/`project`/`user`) igen elkülöníthető, hogy melyik szerver melyik projektben töltődik be, és OAuth is támogatott HTTP/SSE szervereknél:

> "Claude Code marks a remote server as needing authentication when the server responds with `401 Unauthorized` or `403 Forbidden`. […] Authentication tokens are stored securely and refreshed automatically" — https://code.claude.com/docs/en/mcp

A **token-tárolás azonban a gyakorlatban NEM projektenként elkülönített**, több hivatalos (anthropics/claude-code repo) hibajegy szerint:

> "OAuth credentials are stored in `~/.claude/.credentials.json` under a single key per server URL (e.g., `plugin:slack:slack|…`) … Only one token exists regardless of how many projects use the same MCP server. Authenticating in one project overwrites the credential used by all other projects." — https://github.com/anthropics/claude-code/issues/39952

> "When a plugin or an MCP server is configured with `project` or `local` scope, any OAuth credentials set there are forcibly used outside of that scope, causing credential leakage. […] the same plugin or MCP server in various projects for different entities … one entity's credentials may accidentally be used with another entity's data." — https://github.com/anthropics/claude-code/issues/25632

> "After OAuth completes, Claude Code stores MCP tokens in the macOS Keychain … under the service name `Claude Code-credentials`, within an `mcpOAuth` object. The storage key for each server entry is: `serverName|base64(callbackUrl)`" — https://github.com/anthropics/claude-code/issues/43000

Van bejáratott **workaround**: két különböző szervernévvel (pl. `slack-workspace-a` / `slack-workspace-b`), ugyanarra az URL-re mutatva, mesterségesen külön cache-kulcs (és így külön OAuth-állapot) érhető el projektenként — de ez nem natív funkció, hanem trükk:

> "The OAuth credential key in `~/.claude/.credentials.json` is based on the server **name**, so if you create servers with different names pointing to the same URL, each gets its own token." — https://github.com/anthropics/claude-code/issues/39952

Két külön feature request (#39952, #48834) is nyitva van a natív per-projekt OAuth-tárolásra 2026 közepén.

---

## 2. OpenAI Codex CLI

### 2.1 Projektszintű MCP-konfiguráció

**Van** projektszintű config, `.codex/config.toml` formában — ez a `_kozos.txt`-ben feltételezett Codex-viselkedéssel (csak globális `~/.codex/config.toml`) szemben pontosítás:

> "User-level configuration lives in `~/.codex/config.toml`. You can also add project-scoped overrides in `.codex/config.toml` files. Codex loads project-scoped config files only when you trust the project." — https://developers.openai.com/codex/config-reference

> "In addition to your user config, Codex reads project-scoped overrides from `.codex/config.toml` files inside your repo. Codex walks from the project root to your current working directory and loads every `.codex/config.toml` it finds. If multiple files define the same key, the closest file to your working directory wins." — https://learn.chatgpt.com/docs/config-file/config-advanced.md

Fontos: ez NEM a `CODEX_HOME`-ot írja felül (egy 2025 szeptemberi PR, #4007, ami ezt próbálta megvalósítani biztonsági/sandboxing okokból lezárásra került), hanem egy külön **réteg**, ami a config-fába rétegződik be a `~/.codex/config.toml` fölé (project > profile > user > system a precedencia sorrendje).

MCP szerver **projekt configban is definiálható** (a tiltott kulcsok listáján az `mcp_servers` NEM szerepel):

> "Codex ignores `openai_base_url`, `chatgpt_base_url`, `apps_mcp_product_sku`, `model_provider`, `model_providers`, `notify`, `profile`, `profiles`, `experimental_realtime_ws_base_url`, and `otel` when they appear in a project-local `.codex/config.toml`" — https://developers.openai.com/codex/config-reference

Remote HTTP szerver, fejléc:

> "```toml\n[mcp_servers.remote-api]\nurl = \"https://mcp.example.com/api\"\nbearer_token_env_var = \"COMPANY_MCP_TOKEN\"\nenabled = true\ntool_timeout_sec = 60\n```" — https://openai-codex.mintlify.app/configuration/mcp-servers

Forráskódban a HTTP transzport mezői: `url`, `bearer_token_env_var`, `http_headers`, `env_http_headers` — https://github.com/openai/codex/blob/d807d44a/codex-rs/cli/src/mcp_cmd.rs

Változó-behelyettesítés a `.codex/config.toml`-ban: relatív útvonalak a `.codex/` mappához képest oldódnak fel (`model_instructions_file` példa), env-var behelyettesítés a `bearer_token_env_var`/`env_http_headers` mezőkön keresztül (nem `${VAR}` interpoláció a stringben, hanem külön mező, ami egy env-var **nevét** veszi át):

> "Relative paths inside a project config (for example, `model_instructions_file`) are resolved relative to the `.codex/` folder that contains the `config.toml`." — https://learn.chatgpt.com/docs/config-file/config-advanced.md

### 2.2 Roots

**NEM támogatott.** A hivatalos forráskód (openai/codex repo) az `initialize` kérésben explicit `roots: None`-t küld:

> "```rust\nlet params = InitializeRequestParams {\n meta: None,\n capabilities: ClientCapabilities {\n experimental: None,\n extensions: None,\n roots: None,\n sampling: None,\n elicitation,\n tasks: None,\n },\n …\n};\n```" — https://github.com/openai/codex/blob/f802f0a3/codex-rs/codex-mcp/src/mcp_connection_manager.rs

Ugyanezt erősíti meg egy másik forrásfájl (`rmcp_client.rs`) és egy független, közösségi kompatibilitási táblázat is:

> "| OpenAI Codex | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅, ❌ |" (…Roots oszlop ❌) — https://github.com/apify/mcp-client-capabilities

### 2.3 Munkamenet-indító hook

**Van**, hivatalos dokumentáció szerint (`developers.openai.com/codex/hooks`), `SessionStart` esemény, `hookSpecificOutput.additionalContext` kimenettel:

> "### SessionStart\n…\n```json\n{\n \"hookSpecificOutput\": {\n \"hookEventName\": \"SessionStart\",\n \"additionalContext\": \"Load the workspace conventions before editing.\"\n }\n}\n```\nThat `additionalContext` text is added as extra developer context." — https://developers.openai.com/codex/hooks

Bemenet a forráskód alapján: `session_id`, `cwd`, `transcript_path`, `model`, `permission_mode`, valamint a `source` (`startup`/`resume`/`clear`/`compact`) a `SessionStartRequest` struktúrában — https://github.com/openai/codex/blob/f1affbac/codex-rs/core/src/hook_runtime.rs . Git-infó nincs beépítve, a hook szkriptnek magának kell lekérnie.

**Külön HTTP hook-típus jelenleg NINCS** — a Codex hookjai csak `"command"` típusúak lehetnek (shell), a hivatalos doksi minden példája `"type": "command"`, és egy független elemzés is megerősíti:

> "Only `type: \"command\"` handlers run in the current Codex release. `prompt` and `agent` handlers are parsed but skipped." — https://harnez.ai/posts/hooks-complete-tutorial/

(A `prompt`/`agent`/`mcp_tool` hook-típusok később, kísérleti jelleggel megjelentek egy 2026 augusztusi verzióban egy harmadik féltől származó blog szerint, de `"http"` típusú, URL-re közvetlenül POST-oló hook a Codexben — a jelenleg fellelt források szerint — **nincs**.)

**Kimeneti korlát: kb. 2500 token — MEGERŐSÍTVE, hivatalos forrásból:**

> "Codex limits each model-visible hook-output message to roughly 2,500 tokens. If a hook returns more, Codex saves the full text under `<temp_dir>/hook_outputs/<session_id>/.txt` and gives the model a head-and-tail preview with the saved-file path." — https://developers.openai.com/codex/hooks

> "This applies to additional context from `SessionStart`, `SubagentStart`, `PreToolUse`, `PostToolUse`, and `UserPromptSubmit`, feedback from `PostToolUse`, and continuation prompts from `Stop` and `SubagentStop`." — https://developers.openai.com/codex/hooks

A limit **konfigurálható hook-onként** (`additionalContextLimit` mező, alapértelmezett 2500, `0` = nincs korlát):

> "Omit `additionalContextLimit` to use the default `2500`-token threshold. Use a positive integer to select a different threshold, or `0` to pass the handler's complete additional context directly to the model." — https://www.codex-docs.com/en/docs/hooks

Egy hivatalos PR (#34393) is megerősíti a mechanizmust:

> "Add `additionalContextLimit` to command hook configuration for events that can emit `additionalContext`. Apply the limit independently to each hook's context before it is sent to the model. Unset values retain the 2,500-token default" — https://github.com/openai/codex/pull/34393

### 2.4 OAuth per projekt

A Codex `codex mcp login <name>` paranccsal hitelesít, a token-tár kulcsa a **szervernév + URL** (nem a projekt útvonala):

> "```rust\nfn compute_store_key(server_name: &str, server_url: &str) -> Result<String> {\n …\n let truncated = sha_256_prefix(&Value::Object(payload))?;\n Ok(format!(\"{server_name}|{truncated}\"))\n}\n```" — https://github.com/openai/codex/blob/d807d44a/codex-rs/rmcp-client/src/oauth.rs

Tárolás helye a `CODEX_HOME` alatt (keyring vagy `CODEX_HOME/.credentials.json`), az `mcp_oauth_credentials_store_mode` beállítással konfigurálható (`auto`/`file`/`keyring`):

> "`\"auto\"` - Prefer OS keyring, fallback to file … `\"file\"` - Store in `~/.codex/.credentials.json`" — https://openai-codex.mintlify.app/configuration/mcp-servers

**Következmény:** mivel a `CODEX_HOME` globális (a projekt-lokális `.codex/` réteg csak konfigurációt ad hozzá, a hitelesítő-adat tárolási helyét — `CODEX_HOME`-ot — a 2025-ös PR #4007 elutasítása miatt NEM írja felül), két projekt, amely **ugyanazzal a szervernévvel** ugyanarra az URL-re mutat, **megosztja** az OAuth-tokent. Két különböző szervernévvel viszont technikailag elkülöníthető (a kulcs tartalmazza a nevet) — ehhez hasonlóan, mint a Claude Code-nál, de itt ez direktebben következik a forráskódból, nem hibajegyből.

---

## 3. Gemini CLI

### 3.1 Projektszintű MCP-konfiguráció

`.gemini/settings.json` a projekt gyökerében:

> "Project settings file: … Location: `.gemini/settings.json` within your project's root directory. Scope: Applies only when running Gemini CLI from that specific project. Project settings override user settings and system defaults." — https://github.com/google-gemini/gemini-cli/blob/HEAD/docs/reference/configuration.md

Remote HTTP szerver (`httpUrl`), fejléc (`headers`):

> "```json\n{\n \"mcpServers\": {\n \"httpServerWithAuth\": {\n \"httpUrl\": \"http://localhost:3000/mcp\",\n \"headers\": {\n \"Authorization\": \"Bearer your-api-token\",\n \"X-Custom-Header\": \"custom-value\"\n },\n \"timeout\": 5000\n }\n }\n}\n```" — https://google-gemini.github.io/gemini-cli/docs/tools/mcp-server.html

CLI-parancs is van a hozzáadásra, alapértelmezett hatókör `project`:

> "`-s, --scope`: Configuration scope (user or project). [default: \"project\"]" — https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md

Változó-behelyettesítés `env` mezőben `$VAR_NAME`/`${VAR_NAME}` (Windows-on `%VAR_NAME%` is), de ez csak a **stdio szerver `env`/`args` mezőire** dokumentált explicit módon, nem találtunk hivatalos `${workspaceFolder}`-szerű munkakönyvtár-változót a `httpUrl`/`headers` mezőkhöz (csak a `cwd` mező van, ami maga is csak stdio-hoz).

Hatókör-ütközés: projekt/extension-eredetű és felhasználói konfiguráció **egyesül** (merge), nem egyszerűen felülír — `excludeTools` unió, `includeTools` metszet, a szűkítőbb szabály nyer:

> "Precedence: `excludeTools` always takes precedence over `includeTools`. This ensures you always have veto power over tools provided by an extension" — https://github.com/google-gemini/gemini-cli/blob/HEAD/docs/tools/mcp-server.md

### 3.2 Roots

**Támogatott**, önálló implementáció (2 PR: alap-roots + change-notification):

> "I've implemented support for the Model Context Protocol (MCP) Roots specification. […] By registering a `roots` capability and providing a handler for `roots/list` requests, the client can now send its working directory, formatted as a file URI, to the server." — https://github.com/google-gemini/gemini-cli/pull/5856

> "Sends notifications to MCP servers when the roots list changes per the [MCP specification]… Adds the ability to subscribe to workspace directory changes, and uses that to send notifications to MCP servers." — https://github.com/google-gemini/gemini-cli/pull/6502

A working-directory-forrás a `WorkspaceContext.getDirectories()`, vagyis a `--include-directories`-szal bővíthető munkaterület-halmaz — ez transzportfüggetlen kliens-szintű képesség, tehát a HTTP-szerverekre is vonatkozik.

### 3.3 Munkamenet-indító hook

**Van**, `SessionStart` esemény, `startup`/`resume`/`clear` forrásokkal:

> "### `SessionStart`\n…\nFires on application startup, resuming a session, or after a `/clear` command. Used for loading initial context.\n- Input fields: \n - `source`: (`\"startup\" | \"resume\" | \"clear\"`)\n- Relevant output fields: \n - `hookSpecificOutput.additionalContext`: (`string`) \n - Interactive: Injected as the first turn in history.\n - Non-interactive: Prepended to the user's prompt." — https://geminicli.com/docs/hooks/reference/ (a hivatalos `google-gemini/gemini-cli` repo `docs/hooks/reference.md` tükrözése)

Bemenet (közös mezők, forráskódból): `session_id`, `transcript_path`, `cwd`, `hook_event_name`, `timestamp`, plusz `source` — https://github.com/google-gemini/gemini-cli/blob/d2cd12a7/packages/core/src/hooks/hookEventHandler.ts . Git-infó nincs beépítve.

**Csak `"command"` (shell) hook-típus van dokumentálva**, HTTP hook-típus a Gemini CLI-ban nincs:

> "| `type` | string | Yes | The execution engine. Currently only `\"command\"` is supported. |" — https://github.com/google-gemini/gemini-cli/blob/d2cd12a7/docs/hooks/index.md

**Kimeneti korlát:** a hivatalos hooks-referencia és a writing-hooks útmutató egyike sem ad meg konkrét karakter-/token-korlátot a `additionalContext`-re → **NINCS FORRÁS** erre nézve Gemini CLI esetén.

### 3.4 OAuth per projekt

OAuth 2.0 támogatott HTTP/SSE szervereknél, automatikus discovery-vel és dinamikus kliens-regisztrációval:

> "Gemini CLI supports OAuth 2.0 authentication for remote MCP servers using SSE or HTTP transports." — https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md

A tokentár **globális, egyetlen fájl**, kulcs a **szervernév** (nem a projekt):

> "**Stored securely** in `~/.gemini/mcp-oauth-tokens.json`" — https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md

Forráskód szerint is `serverName`-alapú kulcsolás egy közös JSON tömbben:

> "```ts\nasync setCredentials(credentials: OAuthCredentials): Promise<void> {\n …\n const tokens = await this.getAllCredentials();\n tokens.set(credentials.serverName, credentials);\n …\n}\n```" — https://github.com/google-gemini/gemini-cli/blob/caa04664/packages/core/src/mcp/oauth-token-storage.ts

**Következmény:** ugyanaz, mint Codexnél — két projekt, ha **ugyanazzal a szervernévvel** konfigurálja ugyanazt a szervert, **osztozik** a tokenen; csak eltérő szervernévvel különíthető el (nem natívan projekt szerint).

---

## 4. Cursor

### 4.1 Projektszintű MCP-konfiguráció

`.cursor/mcp.json` a projektben, `~/.cursor/mcp.json` globálisan, a projektszintű nyer ütközésnél:

> "Create `.cursor/mcp.json` in your project for project-specific tools." — https://cursor.com/docs/mcp

> "Project config (`.cursor/mcp.json` in the repo root) affects only that project. Global config (`~/.cursor/mcp.json`) applies everywhere. Same server defined in both files? Project-level wins." — https://www.truefoundry.com/blog/mcp-servers-in-cursor-setup-configuration-and-security-guide (T3, de a hivatalos doksival egybehangzó gyakorlati összefoglaló)

Remote szerver, fejléc:

> "```json title=\"Remote Server\"\n// MCP server using HTTP or SSE - runs on a server\n{\n \"mcpServers\": {\n \"server-name\": {\n \"url\": \"http://localhost:3000/mcp\",\n \"headers\": {\n \"API_KEY\": \"value\"\n }\n }\n }\n}\n```" — https://cursor.com/docs/mcp.md

Változó-behelyettesítés — a legrészletesebb a hat kliens közül:

> "Use variables in `mcp.json` values. Cursor resolves variables in these fields: `command`, `args`, `env`, `url`, and `headers`. Supported syntax: `${env:NAME}` environment variables, `${userHome}` path to your home folder, `${workspaceFolder}` project root (the folder that contains `.cursor/mcp.json`), `${workspaceFolderBasename}` name of the project root, `${pathSeparator}` and `${/}` OS path separator" — https://cursor.com/docs/mcp.md

**Ellentmondás/hiba**: a `${env:NAME}` dokumentáltan működik `headers`-ben, de egy 2026 márciusi hivatalos fórum-bejegyzés szerint sokáig ez ténylegesen NEM interpolálódott remote (HTTP/SSE) szervereknél, csak lokális (stdio) szervereknél:

> "Per Cursor's MCP documentation, config interpolation with `${env:NAME}` syntax should work in the headers field. However, for remote HTTP/SSE MCP servers, the variable is not resolved - the literal string `${env:VAR_NAME}` is sent instead… (Note: Config interpolation does work with local / STDIO servers)." — https://forum.cursor.com/t/config-interpolation-env-name-not-working-in-headers-for-remote-mcp-servers/156069

> "The `${env:NAME}` interpolation for headers was fixed in a previous release and should work on your version." (Cursor-válasz ugyanabban a szálban) — https://forum.cursor.com/t/config-interpolation-env-name-not-working-in-headers-for-remote-mcp-servers/156069

### 4.2 Roots

**Dokumentáció szerint támogatott**, DE gyakorlatban hibás — ez az egyik legerősebb ellentmondás a kutatásban:

> "| Roots | Supported | Server-initiated inquiries into URI or filesystem boundaries |" — https://cursor.com/docs/mcp

A kliens az `initialize` válaszban hirdeti a `roots` capability-t:

> "capabilities: ClientCapabilities { experimental: None, roots: Some(RootsCapabilities { list_changed: Some(false) }), sampling: None }" — https://forum.cursor.com/t/mcp-client-does-not-support-roots-list/77248

…de a tényleges `roots/list` hívás `-32601 Method not found` hibát ad vissza, amit egy független MCP-szerver fejlesztő is megerősít, éles reprodukcióval:

> "Cursor has a documented, longstanding bug where it advertises `roots: { listChanged: false }` in its initialize capabilities, but calling `roots/list` against it returns a `JSON-RPC error -32601 Method not found` (confirmed on the Cursor forum and a related feature request thread, still open as of recent posts — despite Cursor's own docs page currently listing `\"Roots: Supported\"`)." — https://github.com/Unveil-gg/twine-mcp/issues/3

### 4.3 Munkamenet-indító hook

**Van**, `sessionStart` esemény (IDE/Agent Chat munkameneteknél; cloud agenteknél NEM fut):

> "#### sessionStart\nCalled when a new composer conversation is created. This hook runs as fire-and-forget; the agent loop does not wait for or enforce a blocking response. Use it to set up session-specific environment variables or inject additional context." — https://cursor.com/docs/hooks.md

> "| Input Field | Type | Description |\n| --- | --- | --- |\n| `session_id` | string | Unique identifier for this session (same as `conversation_id`) |\n| `is_background_agent` | boolean | Whether this is a background agent session vs interactive session |\n| `composer_mode` | string (optional) | The mode the composer is starting in (e.g., \"agent\", \"ask\", \"edit\") |" — https://cursor.com/docs/hooks.md

> "| Output Field | Type | Description |\n| `env` | object (optional) | Environment variables to set for this session. Available to all subsequent hook executions |\n| `additional_context` | string (optional) | Additional context to add to the conversation's initial system context |" — https://cursor.com/docs/hooks.md

> "`sessionStart` | Deferred while cloud agents can still start in a read-only environment. Hooks don't load there, so a cloud `sessionStart` would fire too late (after the first write) rather than at true session start." — https://cursor.com/docs/hooks.md

**Csak `"command"` hook-típus** — a Cursor hookjai kizárólag shell-parancsot futtatnak (nincs natív `"http"` típus, minden példa `"command": "./hooks/…"` formátumú a hivatalos `hooks.json` sémában — https://cursor.com/docs/hooks.md).

Cursor kompatibilitási réteget épített a Claude Code hook-nevekhez:

> "Claude Code hook names are automatically mapped to Cursor hook names: … `SessionStart` | `sessionStart` | Yes" — https://cursor.com/docs/reference/third-party-hooks.md

**Kimeneti korlát: NINCS FORRÁS.** A hivatalos `cursor.com/docs/hooks.md` sem a `sessionStart`, sem más hook esetén nem ad meg konkrét karakter-/token-korlátot az `additional_context` mezőre.

Megjegyzendő egy külön, futásidejű megbízhatósági probléma is (nem méretkorlát, hanem race condition): egy 2026 áprilisi hivatalos fórum-visszaigazolás szerint az IDE-ben a `sessionStart` hook aszinkron fut, és a `additional_context` néha nem jut el a modellhez, mert a composer még nem áll készen a hook végzésekor:

> "This is a confirmed bug. In the IDE, the `sessionStart` hook runs async before the composer handle is fully created, so `additional_context` can get silently dropped even if the log says 'merged successfully'." — https://forum.cursor.com/t/sessionstart-hook-output-is-accepted-and-merged-but-the-injected-context-does-not-reach-agent-window/157141

### 4.4 OAuth per projekt

**Ez az egyetlen kliens, ahol a per-projekt OAuth-elkülönítés dokumentáltan (bár nem hivatalos doksiban, hanem megerősített hibajegyekben) valóban megvalósul**, mert Cursor a hitelesítő-állapotot magába a workspace-projekt könyvtárba írja:

> "Cursor stores Model Context Protocol (MCP) authentications (such as OAuth2 flows) directly within the specific project directory where the connection was first established (eg `~/.cursor/project/xxx/mcp-auth.json`)." — https://github.com/multica-ai/multica/issues/3908

Ezt a Cursor csapata is megerősítette egy másik, kifejezetten erre rákérdező hivatalos fórumszálban:

> "The root cause is that the enabled state and project approval for MCP servers are scoped to the workspace path, and a new worktree window has a different path, so it treats itself as a new workspace. On top of that, OAuth callback routing is tied to the current window's `workspaceId`, so even with saved tokens, the new window goes through the flow again." — https://forum.cursor.com/t/mcp-servers-are-not-enabled-authenticated-in-new-worktree-agents-oauth-making-worktrees-impractical/159989

Van statikus OAuth-hitelesítő-adat direkt `mcp.json`-ban is (nem csak dinamikus DCR):

> "Add an `auth` object to remote server entries that use `url`: … `\"auth\": { \"CLIENT_ID\": \"your-oauth-client-id\", \"CLIENT_SECRET\": \"your-client-secret\", \"scopes\": [\"read\", \"write\"] }`" — https://cursor.com/docs/mcp

**Fontos korlát**: mivel a workspace-út (`workspaceId`) alapján skálázódik, egy Git worktree-alapú második ablak (más elérési út, ugyanaz a repo) **nem örökli** az OAuth-állapotot — tehát a projektenkénti elkülönítés itt is inkább "workspace-elérési-út szerinti", nem tudatos "projekt-azonosító szerinti" tervezés eredménye.

---

## 5. Google Antigravity

*Van hivatalos dokumentáció* (`antigravity.google/docs`, `www.antigravity.google/docs`), ezt a kutatási kérdés feltételesen kérte.

### 5.1 Projektszintű MCP-konfiguráció

Globális és workspace-szintű config is van, `mcp_config.json` néven:

> "The configuration file is located globally at `~/.gemini/config/mcp_config.json` (or locally in your workspace under `.agents/mcp_config.json`)." — https://www.antigravity.google/docs/ide/mcp/

> "Antigravity CLI Config: Servers are defined inside a standalone `mcp_config.json` profile: Global servers: `~/.gemini/config/mcp_config.json`; Workspace servers: `.agents/mcp_config.json`" — https://www.antigravity.google/docs/cli/gcli-migration

Remote HTTP szerver (`serverUrl`), fejléc (`headers`), OAuth (`oauth.clientId`/`clientSecret`, `authProviderType`):

> "- `serverUrl` (string): URL for remote `Streamable HTTP` or `SSE` servers. … `headers` (object): Custom HTTP headers for remote servers. … `authProviderType` (string): Authentication provider. Supports `\"google_credentials\"` for Google Application Default Credentials (ADC). `oauth` (object): OAuth client credentials (`clientId`, `clientSecret`)." — https://www.antigravity.google/docs/ide/mcp/

Változó-behelyettesítés: `${workspaceFolder}` **dokumentálva van (közösségi fórumon, egy Google-alkalmazott/moderátor válaszában)**, DE gyakorlatban hibásan működik legalább egy felhasználó beszámolója szerint:

> "Antigravity isolates MCP processes, so they cannot automatically detect your project path. You need to explicitly pass it by using the `${workspaceFolder}` variable in your configuration arguments: '–dir', '${workspaceFolder}'" — https://discuss.ai.google.dev/t/please-provide-env-for-current-project-base-dir-to-mcp-servers/119313 (T3, közösségi fórum)

> "Unfortunately, when an agent tries to call and use any of the available tool, it seems that the `${workspaceFolder}` is seen only as a raw text and not the actual folder path to my workspace, and thus it does not work." — https://discuss.ai.google.dev/t/please-provide-env-for-current-project-base-dir-to-mcp-servers/119313 (ugyanaz a szál, másik felhasználó)

### 5.2 Roots

**NINCS FORRÁS.** Sem a hivatalos MCP-doksi (`antigravity.google/docs/mcp/`, `antigravity.google/docs/ide/mcp/`), sem a hooks-doksi nem említi az MCP `roots` képességet; nem találtunk sem megerősítő, sem cáfoló hivatalos forrást arra, hogy Antigravity implementálja-e a `roots/list`-et.

### 5.3 Munkamenet-indító hook

**Nincs `SessionStart` esemény** — ez fontos eltérés a többi klienshez képest. Az Antigravity `hooks.json` eseménykészlete teljesen más felépítésű, és nem tartalmaz session-indító eseményt:

> "| `PreToolUse` | array | Handlers that run before a tool is executed. |\n| `PostToolUse` | array | Handlers that run after a tool completes. |\n| `PreInvocation` | array | Handlers that run before Antigravity calls the model. |\n| `PostInvocation` | array | Handlers that run immediately after each model invocation completes. |\n| `Stop` | array | Handlers that run when the execution loop terminates. |" — https://antigravity.google/docs/hooks/

A legközelebbi analóg a **`PreInvocation`**, ami minden modellhívás előtt fut (nem csak a munkamenet elején), és `injectSteps` tömbbel tud kontextust beszúrni:

> "### PreInvocation\nFires before the model is called (starts at 0).\n… `injectSteps` | array of objects | Optional. List of steps to inject into the conversation trajectory before the model is called." — https://antigravity.google/docs/hooks/

Config-hely: `.agents/hooks.json` (workspace) vagy `~/.gemini/config/hooks.json` (globális):

> "Workspace level: `.agents/hooks.json` in your open project. Global level: `~/.gemini/config/hooks.json`." — https://antigravity.google/docs/hooks/

**Csak `"command"` hook-típus** van dokumentálva Antigravity-ben is:

> "| `type` | string | Optional. Currently only `\"command\"` is supported. Defaults to `\"command\"`. |" — https://antigravity.google/docs/hooks/

Bemenet (közös mezők minden hookra): `conversationId`, `workspacePaths` (tömb — több mountolt munkaterület is lehet), `transcriptPath`, `artifactDirectoryPath`, `modelName`. Git-infó nincs beépítve.

**Kimeneti korlát: NINCS FORRÁS** — mivel nincs SessionStart, és a `PreInvocation`/`PostInvocation` `injectSteps` mezőjére sem található dokumentált méretkorlát.

### 5.4 OAuth per projekt

A `mcp_config.json` workspace-szinten (`.agents/mcp_config.json`) definiálható, és az `oauth.clientId`/`clientSecret` közvetlenül a configban van (statikus hitelesítő-adat), vagy `authProviderType: "google_credentials"` esetén a helyi Google ADC-t használja:

> "```json\n{\n \"mcpServers\": {\n \"gmail\": {\n \"serverUrl\": \"https://gmailmcp.googleapis.com/mcp/v1\",\n \"oauth\": {\n \"clientId\": \"OAUTH_CLIENT_ID\",\n \"clientSecret\": \"OAUTH_CLIENT_SECRET\"\n }\n }\n }\n}\n```" — https://developers.google.com/workspace/guides/configure-mcp-servers

Mivel a workspace-szintű `mcp_config.json` per-projekt is lehet, és a hitelesítést a `/mcp` panelben szerverenként kell elvégezni, **elvben** két workspace két külön `.agents/mcp_config.json`-nal, két külön `oauth.clientId`-vel (vagy akár ugyanazzal, de a token-store kulcsa alapján) elkülönített kapcsolatot tarthat fenn — de a token-tárolás pontos kulcsolási logikájára (projekt szerint vagy globálisan, szervernév szerint) **NINCS FORRÁS** a fellelt hivatalos dokumentációban.

---

## 6. GitHub Copilot (VS Code Agent mód)

### 6.1 Projektszintű MCP-konfiguráció

`.vscode/mcp.json` a workspace-ben, user-profil szintű config külön fájlban:

> "Workspace: create or open `.vscode/mcp.json` in your project. Include this file in source control to share MCP server configurations with your team. User profile: run the MCP: Open User Configuration command to open the `mcp.json` file in your user profile folder." — https://code.visualstudio.com/docs/agent-customization/mcp-servers

Remote HTTP szerver:

> "```json\n{\n \"servers\": {\n \"github\": {\n \"type\": \"http\",\n \"url\": \"https://api.githubcopilot.com/mcp\"\n },\n …\n }\n}\n```" — https://code.visualstudio.com/docs/agent-customization/mcp-servers

Egyedi header: az OAuth-mentes remote szervereknél a header közvetlenül a `mcp.json`-ban is megadható (a doksi kifejezetten input-változót javasol titkokra), és van `env`/`envFile` is (`${workspaceFolder}/.env`) — ez egyértelmű **munkakönyvtár-behelyettesítés** bizonyíték is:

> "| `envFile` | No | Path to an environment file to load more variables | `\"${workspaceFolder}/.env\"` |" — https://code.visualstudio.com/docs/agents/reference/mcp-configuration

Változó-behelyettesítés elsősorban `${input:variable-id}` formában (nem sima `${VAR}` env-expanzió), ami first-use-kor rákérdez és biztonságosan tárolja az értéket:

> "When you reference an input variable using `${input:variable-id}`, VS Code prompts you for the value when the server starts for the first time. The value is then securely stored for subsequent use." — https://code.visualstudio.com/docs/agents/reference/mcp-configuration

**Fontos architekturális megkülönböztetés**: a VS Code UI-ban szerkesztett `.vscode/mcp.json`-t a mögöttes "Agent Host" (a Copilot CLI motorja, amit a VS Code Agent mód is használ) **nem olvassa közvetlenül** — külön, portable configot vár:

> "VS Code forwards the servers you configure to the Agent Host, except servers that require interactive input (for example, `${input:...}` variables). The Agent Host doesn't read `.vscode/mcp.json` directly; for portable configuration, use a workspace `.mcp.json` or user `~/.copilot/mcp-config.json` file, which the Agent Host reads natively." — https://code.visualstudio.com/docs/agents/reference/mcp-configuration

Hatókör-ütközés: a doksi kifejezetten óva int attól, hogy ugyanazt a szervert workspace és user szinten is definiálják, mert az konfliktust okozhat (implikáltan: mindkettő betöltődik, nem egyszerű override):

> "We recommend you use only one location per server. Adding the same server to both locations may cause conflicts and unexpected behavior." — https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp-in-your-ide/extend-copilot-chat-with-mcp

### 6.2 Roots

**Támogatott**, hivatalos VS Code doksiból idézve (egy Cursor-fórum szálban, ahol a Cursor hiányosságával szemben hasonlítják össze):

> "VS Code provides servers with the current workspace folders using `roots` (spec)." — https://forum.cursor.com/t/mcp-client-does-not-support-roots-list/77248 (eredeti forrás: a hivatalos VS Code MCP-doksi)

Megerősíti a harmadik féltől származó kompatibilitási táblázat is:

> "| Visual Studio Code | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅, ✅ |" (…Roots oszlop ✅) — https://github.com/apify/mcp-client-capabilities

### 6.3 Munkamenet-indító hook

**Van**, `sessionStart` esemény — ez az Agent Host (a VS Code Agent mód és a különálló GitHub Copilot CLI közös motorja) hook-rendszeréhez tartozik, amit a hivatalos GitHub-doksi és a hivatalos `microsoft/vscode-docs` repo egyaránt dokumentál (két független hivatalos forrás, tehát megerősítve):

> "| `sessionStart` | A new or resumed session begins. | Optional — can inject `additionalContext` into the session. | Fires once per job, as a new session (not a resume)." — https://docs.github.com/en/copilot/reference/hooks-reference

> "## SessionStart\nThe `SessionStart` hook fires when a new agent session begins.\n### SessionStart input\n… ```json\n{\n \"source\": \"new\"\n}\n```\n| `source` | string | How the session was started. Currently always `\"new\"`. |" — https://github.com/microsoft/vscode-docs/blob/538f9c60/docs/agents/reference/hooks-reference.md

Bemenet (közös mezők, SDK-doksiból): `timestamp`, `cwd`, `source` (`"startup"`/`"resume"`/`"new"`), `initialPrompt`. Git-infó nincs beépítve.

> "| `timestamp` | number | Unix timestamp when the hook was triggered |\n| `cwd` | string | Current working directory |\n| `source` | `\"startup\"` \\| `\"resume\"` \\| `\"new\"` | How the session was started |\n| `initialPrompt` | string \\| undefined | The initial prompt if provided |" — https://github.com/github/copilot-sdk/blob/584a239e/docs/hooks/session-lifecycle.md

Kimenet: `hookSpecificOutput.additionalContext` (VS Code hooks-referencia) vagy egyszerűen `additionalContext` (SDK/felhő-agent doksi) — a mezőnév eltér forrásonként, de a szerep azonos.

**HTTP hook-típus VAN**, explicit módon dokumentálva (ellentétben Codex-szel és Gemini CLI-vel, hasonlóan a Claude Code-hoz), a GitHub Copilot SDK/CLI hook-rendszer HTTP hook handlereket is definiál a válasz-body alapján:

> "Hook output (stdout for command hooks, **the response body for HTTP hooks**) is bounded at 10 MiB per invocation—a larger response is truncated rather than exhausting memory." — https://docs.github.com/en/copilot/reference/hooks-reference

A GitHub Copilot **cloud agent** (nem a VS Code helyi Agent mód, hanem a github.com-on futó "coding agent") saját, repóban tárolt hook-konfigurációt használ (`.github/hooks/*.json`), és ott `bash`/`powershell` parancs típusú hookok vannak — ez egy külön felület a VS Code-tól, de a `sessionStart` esemény ott is létezik:

> "```json\n{\n \"version\": 1,\n \"hooks\": {\n \"sessionStart\": […],\n \"sessionEnd\": […],\n \"userPromptSubmitted\": […],\n \"preToolUse\": […],\n \"postToolUse\": […],\n \"errorOccurred\": […]\n }\n}\n```" — https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/use-hooks

A hivatalos GitHub funkció-mátrix szerint magának a **VS Code-nak** csak **részleges (P = Partial)** hook-támogatása van, míg a github.com cloud agentnek és a Copilot CLI-nek teljes:

> "| Hooks | P | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ |" (oszlopok: VS Code, Visual Studio, JetBrains, Eclipse, Xcode, github.com, Copilot CLI) — https://raw.githubusercontent.com/github/docs/main/content/copilot/reference/customization-cheat-sheet.md

**Kimeneti korlát**: nincs Claude Code/Codex-hez hasonló, kifejezetten a `SessionStart`/`additionalContext`-re szabott karakter-/token-limit dokumentálva; az egyetlen dokumentált szám a fent idézett általános **10 MiB** nyersvédelmi korlát (memóriavédelem, nem kontextusbüdzsé), illetve a `postToolUse`-ra specifikusan dokumentált **10 KB**-os összesített korlát (nem sessionStart-ra):

> "`additionalContext` | string | Additional guidance appended to `textResultForLlm`… When multiple hooks return `additionalContext`, the results are joined with a double newline and **capped at 10 KB**." — https://docs.github.com/en/copilot/reference/hooks-reference (ez a `postToolUse` szekcióból való, NEM `sessionStart`-ból)

### 6.4 OAuth per projekt

A `.vscode/mcp.json`-ban vagy user-configban definiált remote szerverhez a `mcp.json` fájl fölötti CodeLens-en keresztül hitelesít a felhasználó:

> "If you are using a remote server with OAuth authentication, in the `mcp.json` file, click Auth from the CodeLens above the server to authenticate to the server." — https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp-in-your-ide/extend-copilot-chat-with-mcp

Mivel a szerver-definíció maga is workspace- vagy user-szintű fájlban él, és a hitelesítés a szerver-bejegyzéshez kötődik, **elvben** két workspace, két külön `.vscode/mcp.json`-nal (akár azonos szervernévvel, de külön workspace-ben), külön hitelesítési állapotot tarthat — de a pontos token-tárolási mechanizmus (workspace-secrets store vs. globális VS Code Secret Storage) **kulcsolási logikájára nincs forrás** a fellelt hivatalos VS Code/GitHub dokumentációban; ezt tehát **NINCS FORRÁS**-ként jelöljük.

---

## Ellentmondások

1. **Cursor — roots**: a hivatalos doksi "Supported"-nek jelöli a roots-ot, és a kliens ténylegesen hirdeti a `roots` capability-t az `initialize` válaszban, de a `roots/list` hívás `-32601 Method not found` hibával tér vissza (fórum + független MCP-szerver-fejlesztő github issue-ja is megerősíti). → A dokumentáció és a valós viselkedés ellentmond egymásnak.
2. **Claude Code — 10 000 karakteres hook-limit**: a hivatalos doksi szerint a limit fölötti kimenetet fájlba menti a rendszer és egy "preview"-t ad a modellnek; két nyílt hibajegy szerint viszont ez a preview a gyakorlatban csak kb. 2000 karakter, nem a dokumentált 10 000. A doksi szövege és a mért viselkedés között eltérés van (bár technikailag nem cáfolja a 10 000-es *bemeneti* küszöböt, csak a *kimeneti* preview méretét pontosítja más értékre).
3. **Cursor — `${env:NAME}` interpoláció fejlécekben**: a hivatalos doksi szerint működik `headers`-ben; egy 2026 márciusi fórumbejegyzés szerint remote (HTTP/SSE) szervereknél NEM interpolálódott (csak stdio-nál), amit a Cursor csapata "egy korábbi release-ben javítva" válasszal kommentált — vagyis időszakosan tényleg volt eltérés a doksi és a valós viselkedés között.
4. **Claude Code — OAuth hatókör vs. tényleges tárolás**: a szerver-*konfiguráció* (`local`/`project`/`user`) explicit módon projekt-, ill. felhasználó-szintű, de a hivatalos issue tracker szerint az OAuth-*token* tárolása ettől függetlenül gyakorlatilag globális (szervernév/URL szerint kulcsolva), és egy külön hibajegy (#25632) kifejezetten "biztonsági lyuknak" (security hole) nevezi azt, hogy `project`/`local` scope-hoz kötött hitelesítő adat kiszivárog más projektekbe.
5. **Antigravity — `${workspaceFolder}` a MCP configban**: egy Google fórum-válasz szerint ez a hivatalos munkakönyvtár-változó, de egy másik felhasználó ugyanabban a szálban arról számol be, hogy ez ténylegesen nem interpolálódik, csak nyers szövegként jut el az MCP szerverhez.

## Amire NINCS forrás

- **Gemini CLI**: nincs dokumentált karakter-/token-korlát a `SessionStart` hook `additionalContext` kimenetére.
- **Cursor**: nincs dokumentált karakter-/token-korlát a `sessionStart` hook `additional_context` kimenetére.
- **Google Antigravity**: (a) nincs forrás arra, hogy támogatja-e az MCP `roots` képességet; (b) mivel nincs `SessionStart` esemény a hooks-rendszerében, a "munkamenet-indító hook kimeneti korlátja" kérdés Antigravity-re nem is értelmezhető a jelenlegi dokumentáció alapján; a legközelebbi analóg (`PreInvocation`/`injectSteps`) méretkorlátjára sincs forrás.
- **Google Antigravity**: nincs forrás az OAuth-token-tár pontos kulcsolási logikájára (globális szervernév szerint vagy workspace-enként elkülönítve).
- **GitHub Copilot / VS Code**: nincs forrás a `.vscode/mcp.json` OAuth-token pontos tárolási/kulcsolási mechanizmusára (workspace- vs. user-szintű elkülönítés ténylegesen hogyan valósul meg), és nincs `sessionStart`-specifikus (a `postToolUse` 10 KB-hoz hasonló) dokumentált méretkorlát.
- **Codex CLI**: nincs hivatalos forrás arra, hogy tervben van-e valaha natív HTTP hook-típus (`type: "http"`) bevezetése — jelenleg csak `"command"` van hivatalosan dokumentálva.

## Meglátogatott és felderített linkek

| Cím | URL | Tier | Eszköz | Megjegyzés |
|---|---|---|---|---|
| MCP (Claude Code hivatalos doksi) | https://code.claude.com/docs/en/mcp | T1 | Exa search+fetch (highlights) | Projekt-config, roots, OAuth |
| Connect to MCP servers (mcp-quickstart) | https://code.claude.com/docs/en/mcp-quickstart | T1 | Exa | `.mcp.json` szerkesztés lépésről lépésre |
| MCP config (Agent SDK) | https://code.claude.com/docs/en/agent-sdk/mcp.md | T1 | Exa | settingSources, .mcp.json betöltés |
| Hooks reference | https://code.claude.com/docs/en/hooks | T1 | Exa | Hook-típusok, 10k karakteres limit, HTTP hook mezők |
| Automate actions with hooks (guide) | https://code.claude.com/docs/en/hooks-guide | T1 | Exa | SessionStart, HTTP hooks bevezető |
| roots/list dokumentáció-hiányossági issue | https://github.com/anthropics/claude-code/issues/75445 | T1 | Exa | v2.1.203 roots-bővítés részletei |
| Support MCP roots capability (feature req.) | https://github.com/anthropics/claude-code/issues/53861 | T1 | Exa | roots eredeti hiánya |
| roots capability advertised but not implemented | https://github.com/anthropics/claude-code/issues/3315 | T1 | Exa | roots korai (2025 júliusi) hiánya |
| SessionStart hook output truncated to 2000 | https://github.com/anthropics/claude-code/issues/44086 | T1 | Exa | 10k vs. valós 2000 karakteres preview |
| Hook output over 10K silently dropped | https://github.com/anthropics/claude-code/issues/84021 | T1 | Exa | Ugyanaz, részletes mérésekkel |
| Share MCP OAuth tokens globally (#37776) | https://github.com/anthropics/claude-code/issues/37776 | T1 | Exa | User-scope szerver, mégis per-projekt OAuth |
| Per-project OAuth tokens (#39952) | https://github.com/anthropics/claude-code/issues/39952 | T1 | Exa | OAuth kulcs = szervernév/URL, globális, workaround |
| OAuth for plugins and MCP servers goes past scope (#25632) | https://github.com/anthropics/claude-code/issues/25632 | T1 | Exa | "security hole", project/local OAuth szivárgás |
| MCP OAuth multiple terminals re-auth (#43000) | https://github.com/anthropics/claude-code/issues/43000 | T1 | Exa | Keychain kulcsstruktúra: serverName\|base64(callbackUrl) |
| MCP OAuth writes corrupt shared store (#45551) | https://github.com/anthropics/claude-code/issues/45551 | T1 | Exa | Egyetlen közös Keychain-bejegyzés |
| Per-project OAuth for plugins (#48834) | https://github.com/anthropics/claude-code/issues/48834 | T1 | Exa | Globális plugin-OAuth, feature request |
| ConnectorZone — Claude MCP setup guide | https://github.com/JSONbored/claudepro-directory/…claude-mcp-server-setup-guide.mdx | T3 | Exa | Kiegészítő összefoglaló |
| claude-code-guide.org — HTTP hooks | https://claude-code-guide.org/hooks-http/ | T3 | Exa | HTTP hook mezők tükrözése |
| Codex Configuration Reference | https://developers.openai.com/codex/config-reference | T1 | Exa | Projekt-config tiltott kulcsai |
| Codex Project config files (Advanced Configuration) | https://learn.chatgpt.com/docs/config-file/config-advanced.md | T1 | Exa | `.codex/config.toml` rétegzés, precedencia |
| Codex Hooks | https://developers.openai.com/codex/hooks | T1 | Exa | SessionStart, 2500 token limit, additionalContextLimit |
| Codex config basics | https://www.codex-docs.com/en/docs/config-file/config-basic | T2 | Exa | Config-precedencia lista (7 szint) |
| Codex Hooks (codex-docs.com tükrözés) | https://www.codex-docs.com/en/docs/hooks | T2 | Exa | additionalContextLimit mező részletei |
| Prefer project-local .codex as CODEX_HOME (PR #4007, elutasítva) | https://github.com/openai/codex/pull/4007 | T1 | Exa | Miért NEM lett CODEX_HOME projekt-lokális |
| codex-rs config loader forrás | https://github.com/openai/codex/blob/178c3d30/codex-rs/config/src/loader/mod.rs | T1 | Exa | Rétegződési sorrend forráskódból |
| ~/.codex/ treated as project config (#9932) | https://github.com/openai/codex/issues/9932 | T1 | Exa | Trust-modell részletei |
| AGENTS.md discovery (Codex) | https://developers.openai.com/codex/guides/agents-md | T1 | Exa | Instrukciós fájlok, nem hook |
| Codex Customization overview | https://developers.openai.com/codex/concepts/customization | T1 | Exa | AGENTS.md/skills/MCP/subagents áttekintés |
| codex-rs mcp_connection_manager.rs | https://github.com/openai/codex/blob/f802f0a3/codex-rs/codex-mcp/src/mcp_connection_manager.rs | T1 | Exa | `roots: None` forráskódi bizonyíték |
| codex-rs rmcp_client.rs | https://github.com/openai/codex/blob/f1affbac/codex-rs/codex-mcp/src/rmcp_client.rs | T1 | Exa | ClientCapabilities felépítése |
| codex-rs session/mod.rs | https://github.com/openai/codex/blob/fde21ba930cd7d0a4de377a2b147b2b80d6632e9/codex-rs/core/src/session/mod.rs | T1 | Exa | session_start_source felépítése |
| codex-rs hook_runtime.rs | https://github.com/openai/codex/blob/f1affbac/codex-rs/core/src/hook_runtime.rs | T1 | Exa | SessionStartRequest mezői |
| Add configurable hook context spill limits (PR #34393) | https://github.com/openai/codex/pull/34393 | T1 | Exa | additionalContextLimit hivatalos bevezetése |
| Hook additionalContext spilling issue (#22861) | https://github.com/openai/codex/issues/22861 | T1 | Exa | 2500 token limit hatásainak vitája |
| openai/codex mcp_cmd.rs | https://github.com/openai/codex/blob/d807d44a/codex-rs/cli/src/mcp_cmd.rs | T1 | Exa | codex mcp add/login/logout parancsok |
| openai/codex rmcp-client oauth.rs | https://github.com/openai/codex/blob/d807d44a/codex-rs/rmcp-client/src/oauth.rs | T1 | Exa | OAuth store_key = server_name+url hash |
| openai/codex config types.rs | https://github.com/openai/codex/blob/35aaa5d9/codex-rs/config/src/types.rs | T1 | Exa | OAuthCredentialsStoreMode enum |
| openai/codex mcp/auth.rs | https://github.com/openai/codex/blob/main/codex-rs/codex-mcp/src/mcp/auth.rs | T1 | Exa | Auth-status számítás |
| openai/codex perform_oauth_login.rs | https://github.com/openai/codex/blob/27c05a52/codex-rs/rmcp-client/src/perform_oauth_login.rs | T1 | Exa | OAuth login flow forráskódja |
| openai-codex.mintlify.app — mcp-servers | https://openai-codex.mintlify.app/configuration/mcp-servers | T2 | Exa | Remote HTTP config példák |
| openai-codex.mintlify.app — cli/mcp | https://openai-codex.mintlify.app/cli/mcp | T2 | Exa | `codex mcp add --url` |
| Add streamable http servers (#4904 commit) | https://github.com/openai/codex/commit/a43ae86b6c072a962120460e5f4386cbcbc35b27 | T1 | Exa | Bearer token env var bevezetése |
| Add support for streamable HTTP MCP (#4317) | https://github.com/openai/codex/issues/4317 | T1 | Exa | Korai remote HTTP MCP tervezés |
| harnez.ai — hooks complete tutorial | https://harnez.ai/posts/hooks-complete-tutorial/ | T3 | Exa | "Only command handlers run" megerősítés |
| codex.danielvaughan.com — async/mcp_tool hooks | https://codex.danielvaughan.com/2026/08/25/… | T3 | Exa | Nem hivatalos, v0.148.0 hook-bővítések |
| Gemini CLI MCP servers (github.io) | https://google-gemini.github.io/gemini-cli/docs/tools/mcp-server.html | T1 | Exa | httpUrl, headers, env expanzió |
| gemini-cli mcp-setup tutorial | https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/tutorials/mcp-setup.md | T1 | Exa | Alapszintű mcpServers példa |
| gemini-cli docs/tools/mcp-server.md | https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md | T1 | Exa | Teljes MCP-referencia, OAuth szekció |
| Gemini CLI configuration (github.io) | https://google-gemini.github.io/gemini-cli/docs/get-started/configuration.html | T1 | Exa | settings.json helyek |
| geminicli.com — configuration reference | https://geminicli.com/docs/reference/configuration/ | T2 | Exa | Project settings hely és hatókör |
| gemini-cli docs/reference/configuration.md | https://github.com/google-gemini/gemini-cli/blob/HEAD/docs/reference/configuration.md | T1 | Exa | Hivatalos config-referencia |
| Add MCP Roots support (PR #5856) | https://github.com/google-gemini/gemini-cli/pull/5856 | T1 | Exa | Roots eredeti implementációja |
| Add MCP Root change notifications (PR #6502) | https://github.com/google-gemini/gemini-cli/pull/6502 | T1 | Exa | list_changed notifikáció |
| MCP Roots support - workspace changes (#5861) | https://github.com/google-gemini/gemini-cli/issues/5861 | T1 | Exa | Roots follow-up |
| Add roots support for MCP servers (#2847) | https://github.com/google-gemini/gemini-cli/issues/2847 | T1 | Exa | Eredeti roots feature request |
| /add-dir roots list_changed hiánya (Claude Code, #26663) | https://github.com/anthropics/claude-code/issues/26663 | T1 | Exa | Gemini CLI roots-implementációjára hivatkozik összehasonlításként |
| geminicli.com — hooks reference | https://geminicli.com/docs/hooks/reference/ | T2 | Exa | SessionStart mezők |
| gemini-cli hooks/index.md | https://github.com/google-gemini/gemini-cli/blob/d2cd12a7/docs/hooks/index.md | T1 | Exa | Csak "command" hook-típus |
| gemini-cli hooks/reference.md | https://github.com/google-gemini/gemini-cli/blob/d2cd12a7/docs/hooks/reference.md | T1 | Exa | SessionStart input/output |
| gemini-cli hooks/writing-hooks.md | https://github.com/google-gemini/gemini-cli/blob/f8541cf7/docs/hooks/writing-hooks.md | T1 | Exa | Példa hook-lánc |
| gemini-cli hookEventHandler.ts | https://github.com/google-gemini/gemini-cli/blob/d2cd12a7/packages/core/src/hooks/hookEventHandler.ts | T1 | Exa | Közös input mezők forráskódból |
| gemini-cli oauth-token-storage.ts | https://github.com/google-gemini/gemini-cli/blob/caa04664/packages/core/src/mcp/oauth-token-storage.ts | T1 | Exa | serverName-alapú globális token-tár |
| gemini-cli mcpCommand.ts | https://github.com/google-gemini/gemini-cli/blob/f96d5f98/packages/cli/src/ui/commands/mcpCommand.ts | T1 | Exa | /mcp auth parancs |
| Working oauth client (PR #3569) | https://github.com/google-gemini/gemini-cli/pull/3569 | T1 | Exa | OAuth eredeti bevezetése |
| fix: refresh MCP OAuth tokens (PR #28481) | https://github.com/google-gemini/gemini-cli/pull/28481 | T1 | Exa | OAuth refresh hiba javítása |
| Cursor MCP docs | https://cursor.com/docs/mcp.md | T1 | Exa | Projekt-config, változó-behelyettesítés, roots táblázat |
| Cursor MCP docs (html) | https://cursor.com/docs/mcp | T1 | Exa | OAuth `auth` objektum, statikus OAuth |
| github-mcp-server install-cursor.md | https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-cursor.md | T1 | Exa | Global vs project config helyek |
| connector.zone — remote URL fields | https://connector.zone/guides/remote-endpoint-url-fields/ | T3 | Exa | Kliensek közötti URL-mező összehasonlítás |
| Cursor forum — config interpolation bug | https://forum.cursor.com/t/config-interpolation-env-name-not-working-in-headers-for-remote-mcp-servers/156069 | T2 | Exa | `${env:NAME}` hiba + hivatalos válasz |
| policylayer.com — Cursor MCP setup | https://policylayer.com/integrations/cursor | T3 | Exa | Config-mezők összefoglalója |
| Cursor forum — roots/list not supported | https://forum.cursor.com/t/mcp-client-does-not-support-roots-list/77248 | T2 | Exa | roots hirdetve, de nem működik; VS Code idézet is |
| MCP spec — Roots | https://modelcontextprotocol.io/specification/2025-06-18/client/roots | T1 | Exa | Hivatalos protokoll-specifikáció |
| twine-mcp issue #3 — Cursor roots bug | https://github.com/Unveil-gg/twine-mcp/issues/3 | T2 | Exa | Független megerősítés -32601 hibáról |
| Cursor hooks.md | https://cursor.com/docs/hooks.md | T1 | Exa | sessionStart mezők, cloud-agent kivételek |
| Cursor hooks (html) | https://cursor.com/docs/hooks | T1 | Exa | Ugyanaz, html verzió |
| Cursor third-party-hooks.md | https://cursor.com/docs/reference/third-party-hooks.md | T1 | Exa | Claude Code → Cursor hook-név leképezés |
| cursor/cookbook hooks/README.md | https://github.com/cursor/cookbook/blob/main/hooks/README.md | T1 | Exa | Hivatalos hook-példák |
| blog.gitbutler.com — Cursor Hooks deep dive | https://blog.gitbutler.com/cursor-hooks-deep-dive | T3 | Exa | Korai (béta) hook-viselkedés |
| ntorres.dev — Cursor hooks.json guide | https://ntorres.dev/blog/cursor-hooks-json-guide | T3 | Exa | sessionStart payload mezői |
| agenticcontrolplane.com — Cursor Hooks Reference | https://agenticcontrolplane.com/blog/cursor-hooks-reference | T3 | Exa | failClosed, közös mezők |
| Cursor forum — sessionStart context nem jut el | https://forum.cursor.com/t/sessionstart-hook-output-is-accepted-and-merged-but-the-injected-context-does-not-reach-agent-window/157141 | T2 | Exa | Race condition megerősítése |
| multica-ai/multica issue #3908 | https://github.com/multica-ai/multica/issues/3908 | T2 | Exa | mcp-auth.json projektenkénti tárolás |
| Cursor forum — worktree OAuth nem öröklődik | https://forum.cursor.com/t/mcp-servers-are-not-enabled-authenticated-in-new-worktree-agents-oauth-making-worktrees-impractical/159989 | T2 | Exa | Cursor-staff megerősítés workspace-alapú OAuth-ról |
| truefoundry.com — Cursor MCP guide | https://www.truefoundry.com/blog/mcp-servers-in-cursor-setup-configuration-and-security-guide | T3 | Exa | Project vs global precedencia |
| authsome.ai — Cursor tokens | https://authsome.ai/blog/connect-cursor-to-your-stack-without-pasting-tokens | T3 | Exa | Header-alapú titokkezelés kritikája |
| evomap.ai — Cursor MCP limits | https://evomap.ai/blog/cursor-mcp-servers-setup-examples-limits | T3 | Exa | Transport-áttekintés |
| Antigravity MCP docs (ide) | https://www.antigravity.google/docs/ide/mcp/ | T1 | Exa | mcp_config.json hely, mezők |
| Antigravity MCP docs | https://antigravity.google/docs/mcp/ | T1 | Exa | Globális/workspace config, OAuth |
| Google Workspace MCP servers guide | https://developers.google.com/workspace/guides/configure-mcp-servers | T1 | Exa | OAuth clientId/clientSecret példa Antigravity-hez |
| Data Agent Kit — use-mcp-servers (Antigravity) | https://docs.cloud.google.com/data-cloud-extension/antigravity/use-mcp-servers | T1 | Exa | authProviderType google_credentials |
| Google Developer Knowledge MCP codelab | https://codelabs.developers.google.cn/developer-knowledge-mcp-antigravity | T1 | Exa | Konkrét mcp_config.json példa |
| Data Agent Kit — use-mcp-servers (általános) | https://docs.cloud.google.com/data-agent-kit/use-mcp-servers | T1 | Exa | VS Code + Antigravity összehasonlító config |
| Antigravity Hooks docs (ide) | https://antigravity.google/docs/ide/hooks/ | T1 | Exa | Teljes hook-eseménylista, nincs SessionStart |
| Antigravity Hooks docs | https://antigravity.google/docs/hooks/ | T1 | Exa | Ugyanaz, más útvonal alatt |
| Antigravity Rules docs (ide) | https://www.antigravity.google/docs/ide/rules | T1 | Exa | AGENTS.md/GEMINI.md, nem hook |
| Antigravity Rules docs | https://antigravity.google/docs/rules/ | T1 | Exa | Trigger-típusok, token-budget fallback |
| Antigravity gcli-migration docs | https://www.antigravity.google/docs/cli/gcli-migration | T1 | Exa | mcp_config.json vs legacy settings.json |
| google-antigravity/antigravity-sdk-python README | https://github.com/google-antigravity/antigravity-sdk-python/blob/main/google/antigravity/hooks/README.md | T1 | Exa | HookContext vs ToolContext, SDK-szintű hook-modell |
| discuss.ai.google.dev — workspaceFolder bug | https://discuss.ai.google.dev/t/please-provide-env-for-current-project-base-dir-to-mcp-servers/119313 | T3 | Exa | ${workspaceFolder} nem interpolálódik MCP argumentumban |
| k12club/antigravity-mcp README | https://github.com/k12club/antigravity-mcp | T3 | Exa | Közösségi projekt, nem hivatalos roots-mechanizmus |
| VS Code — Add and manage MCP servers | https://code.visualstudio.com/docs/agent-customization/mcp-servers | T1 | Exa | .vscode/mcp.json, user profil |
| VS Code — MCP configuration reference | https://code.visualstudio.com/docs/agents/reference/mcp-configuration | T1 | Exa | input változók, Agent Host eltérés |
| docs.github.com — extend-copilot-chat-with-mcp | https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp-in-your-ide/extend-copilot-chat-with-mcp | T1 | Exa | OAuth CodeLens, workspace vs user config |
| docs.github.com — configure-mcp-servers (cloud agent) | https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/configure-mcp-servers | T1 | Exa | Cloud agent MCP config, COPILOT_MCP_ prefix |
| microsoft/vscode-docs mcp-servers.md | https://github.com/microsoft/vscode-docs/blob/main/docs/agent-customization/mcp-servers.md | T1 | Exa | Agent Host natív config-fájlok |
| VS Code blog — Agent mode meets MCP | https://code.visualstudio.com/blogs/2025/05/12/agent-mode-meets-mcp | T1 | Exa | Streamable HTTP bevezetése |
| VS Code — Use custom instructions | https://code.visualstudio.com/docs/agent-customization/custom-instructions | T1 | Exa | AGENTS.md/copilot-instructions.md, nem hook |
| VS Code — Configure AI for your codebase | https://code.visualstudio.com/docs/agents/guides/customize-copilot-guide | T1 | Exa | Harness-specifikus instrukciók |
| microsoft/vscode-docs hooks-reference.md | https://github.com/microsoft/vscode-docs/blob/538f9c60/docs/agents/reference/hooks-reference.md | T1 | Exa | SessionStart input {source:"new"} |
| vscode issue #325244 — global instructions | https://github.com/microsoft/vscode/issues/325244 | T1 | Exa | Agent Host = beépített Copilot CLI motor |
| docs.github.com — use-hooks (cloud agent) | https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/use-hooks | T1 | Exa | .github/hooks/*.json, bash/powershell |
| customization-cheat-sheet.md | https://raw.githubusercontent.com/github/docs/main/content/copilot/reference/customization-cheat-sheet.md | T1 | Exa | Hooks támogatottsági mátrix (VS Code = Partial) |
| docs.github.com — hooks-reference | https://docs.github.com/en/copilot/reference/hooks-reference | T1 | Exa | 10 MiB korlát, postToolUse 10 KB korlát |
| github/copilot-sdk user-prompt-submitted.md | https://github.com/github/copilot-sdk/blob/main/docs/hooks/user-prompt-submitted.md | T1 | Exa | SDK hook-példa |
| docs.github.com — Working with hooks (SDK) | https://docs.github.com/en/copilot/how-tos/copilot-sdk/features/hooks | T1 | Exa | onSessionStart SDK-példa |
| docs.github.com enterprise-cloud hooks-reference | https://docs.github.com/en/enterprise-cloud@latest/copilot/reference/hooks-reference | T1 | Exa | Ugyanaz, enterprise-cloud tükrözés |
| github/copilot-sdk session-lifecycle.md | https://github.com/github/copilot-sdk/blob/584a239e/docs/hooks/session-lifecycle.md | T1 | Exa | onSessionStart input/output mezők |
| apify/mcp-client-capabilities | https://github.com/apify/mcp-client-capabilities | T3 | Exa | Független roots-összehasonlító táblázat minden kliensre |
| academy.claude.com — Roots (MCP advanced topics) | https://academy.claude.com/courses/model-context-protocol-advanced-topics/roots | T2 | Exa | Roots általános magyarázata (nem klienshez kötött) |

---

# SQ04 — Ki döntse el, hogy egy emlék személyes, projekt- vagy közös — és mi megy félre, ha rosszul dől el?

**Módszertani megjegyzés (degradált mód):** ez a munkamenet nem tudott alügynököket (subagent) indítani a `deep-web-research` skill elvei szerint — a rendelkezésre álló eszközkészletben nem volt olyan agent-indító eszköz, amivel párhuzamos kutató-alügynököket lehetett volna futtatni. A kutatás ezért egyetlen szekvenciális munkamenetben zajlott, kizárólag az Exa `web_search_exa` / `web_fetch_exa` eszközökkel, ahogy a `_kozos.txt` előírja. Nem keletkezett `.research/` evidence vault; minden forrás ebben az egy fájlban szerepel.

## Rövid válasz

Dokumentált, súlyos (P0-critical) tenant-izolációs hibák bizonyítják, hogy a hatókör (scope) meghatározása jelenleg tervezési hiba forrása: a mem0-ban a szerver oldalon a metaadat-mezők (`user_id`/`agent_id`/`run_id`) nem voltak védve felülírás ellen, így egy hívó fél metaadatai átírhatták más tenant emlékének tulajdonjogát; a Claude Code-ban a projekt-hatókör a fájlrendszer-útvonalból származik, ami git worktree-k, átnevezések és ős-könyvtár szerinti "felfelé sétálás" miatt dokumentáltan más ügynök/projekt memóriáját tölti be. A biztonsági ajánlások (OWASP LLM Top 10, OWASP MCP Top 10, OWASP Agentic Top 10, AWS Well-Architected) egyöntetűen azt mondják, hogy a hatókört a hívó környezet (identitásszolgáltató, alkalmazás, downstream rendszer) határozza meg determinisztikusan, nem a modell — az MCP-modellnek magának nincs is protokollszintű mechanizmusa arra, hogy melyik "projekt" aktív. Van közvetlen mérés arra, mennyire megbízhatatlan egy LLM a kontextusfüggő megosztási döntésben: a Meta FAIR CIMemories benchmarkja (ICLR 2026) szerint a frontier modellek akár 69%-os attribútum-szintű szabálysértést (nem odaillő adat megosztását) produkálnak, és ugyanaz a prompt ismételt futtatásra instabilan, más-más attribútumot szivárogtat. A gyakorlatban a memóriaírás visszaigazolása ritka: a mem0, a ChatGPT és a Claude Code auto-memory alapértelmezésben csendben, előzetes jóváhagyás nélkül ír, legfeljebb utólagos értesítést ad ("Memory updated"); az "előbb kérdezz, aztán írj" minta csak harmadik féltől származó middleware-ekként (human-in-the-loop gate-ek) létezik, amit az OWASP kifejezetten ajánl, de a vizsgált memória-rendszerek egyike sem épített be alapból.

## 1. Dokumentált hibák és incidensek

### 1.1 mem0 — tenant-izolációs hibák (identitásmezők felülírása/injektálása)

A mem0 nyílt forráskódú SDK-jában (Python és TypeScript) 2026 közepén egymást követő, P0-critical besorolású hibákat találtak és javítottak, amelyek mindegyike ugyanabból a gyökérokból fakadt: a hívó fél `metadata` mezője felülírhatta vagy beinjektálhatta a `user_id`/`agent_id`/`run_id` hatókör-azonosítókat.

- **#6277** (Python SDK, `update()`): „`Memory.update()` / `AsyncMemory.update()` let caller-supplied `metadata` silently overwrite a memory's `user_id`, `agent_id`, and `run_id` — the exact fields every `search()`, `get_all()`, and `delete_all()` call uses for tenant scoping.” A repró: `m.update(memory_id, metadata={"category": "food", "user_id": "bob"})` — „…silently reassigns the memory to bob.” A karbantartó triázsa: „**Severity:** P0. No malformed input is needed — a normal-looking `metadata` dict silently breaks tenant isolation and causes real data loss…plus cross-tenant data exposure, on both the Python SDK's primary write path and the shipped REST server.” (https://github.com/mem0ai/mem0/issues/6277)
- **#6342 / #6343** — ugyanez a hiba a TypeScript SDK-ban, önálló gyökérokkal: „In the TypeScript OSS SDK, `memory.update()` lets caller-supplied `metadata` silently overwrite a memory's `user_id` / `agent_id` / `run_id`… a cross-tenant data leak with no error raised.” (https://github.com/mem0ai/mem0/issues/6342, https://github.com/mem0ai/mem0/pull/6343)
- **#6655** — a hiba testvérváltozata a *létrehozási* (`add()`) útvonalon: „caller-supplied `metadata` can set a memory's identity scope (`user_id` / `agent_id` / `run_id` / `actor_id`) whenever the matching top-level entity param is not also passed… The created memory is now discoverable through `get_all(filters={"agent_id": "victim-agent"})`… scopes the caller never held.” (https://github.com/mem0ai/mem0/issues/6655)
- **#6796** — a TS `add()` a hívó `filters` objektumát referenciával mutálja, így egy újrafelhasznált `filters` literál átviszi az előző hívás `user_id`-ját a következőbe, és megkerüli a kötelező hatókör-ellenőrzést is: „Result, 10 runs out of 10: no error is thrown, and the second memory is stored under `user_id: \"alice\"`.” Egy külső olvasó kommentje jól mutatja, miért fontos ez a réstípus: „The bob-memory-in-alice's-getAll() reproduction is the clearest public write-up of cross-tenant memory leakage I've come across.” (https://github.com/mem0ai/mem0/issues/6796)
- **#5439 / #5597** — az entitás-összekapcsolási (entity linking) logika hasonlósági egyezésnél (≥0.95) nem ellenőrizte, hogy a talált entitás ugyanahhoz a `user_id`/`agent_id` hatókörhöz tartozik-e: „If entity vector stores have any edge case where a cross-scope entity surfaces at high similarity, a memory from `user_id=\"B\"` could be linked into an entity originally owned by `user_id=\"A\"`.” (https://github.com/mem0ai/mem0/issues/5439)
- **#5121** — több-app (multi-tenant) környezetben a `Memory.add` „Phase 1” jelölt-keresése csak `user_id`/`agent_id`/`run_id` szerint szűr, az `app_id`-t (metaadat) figyelmen kívül hagyja, ezért „the same `user_id` across different `app_id` values will **share** the recent message window and Phase 1 candidate pool” — vagyis két különböző alkalmazás ugyanazon felhasználójának adatai keveredhetnek. (https://github.com/mem0ai/mem0/issues/5121)
- **Hermes-agent mem0 plugin** (harmadik féltől, NousResearch): csoportos csevegésben (Feishu/Lark) a cachelt ügynök-példány megtartja az első üzenetküldő `user_id`-ját, ezért egy másik felhasználó üzenete is az első felhasználó emlékei közé íródik: „Memories from group chats are attributed to the wrong user… When user B later queries their memories, they see user A's memories and vice versa.” A karbantartói triázs szerint ez nem csak konfigurációs eset: „thread_sessions_per_user defaults to **False**, so threads in group chats share one session across participants by design… on default config, every participant's memories in a shared thread are attributed to whoever spoke first… the attribution class is provider-generic even though this report is about mem0.” (https://github.com/NousResearch/hermes-agent/issues/64340)

**Ok mintázat:** minden mem0-hibában a root cause az volt, hogy a szerver oldal *nem* kényszerítette ki a hatókör-azonosítók változatlanságát — a hívó (alkalmazás vagy közvetve az LLM-ágens, amely a `metadata` tartalmát összeállítja) szabadon írhatott olyan mezőket, amelyeket a keresés/törlés hatókörként használt. Ez pontosan az OWASP „excessive agency”/„complete mediation” elvének megsértése (lásd 2. rész).

### 1.2 Claude Code — projekthatókör a fájlrendszer-útvonalból, és a human/project megkülönböztetés hiánya

- **#41283** — „Claude Code's memory system derives project identity from the filesystem path (`~/.claude/projects/{path-derived-key}/memory/`). This means memory is bound to *where a repo lives on disk*, not *what repo it is*.” Két konkrét hibamód: git worktree törlésekor az emlékek elárvulnak, repó átnevezéskor szintén. A mélyebb tervezési hiány: „Global memory (`~/.claude/memory/MEMORY.md`) exists but is an afterthought. The default behavior writes to project scope, and there's no guidance or heuristic pushing the system to ask \"is this about the repo or about the person?\" Most \"about the human\" observations end up project-scoped and fragmented across directories.” (https://github.com/anthropics/claude-code/issues/41283)
- **#53734** — „a silent cross-session memory contamination surface for multi-agent or multi-sub-project workflows”, amikor az auto-memory feloldó rossz (ős-könyvtárba kódolt) projektkönyvtárra „sétál fel”. A bejelentő dokumentált incidenseket is közöl: „We documented 8 cross-agent contamination incidents over approximately one month of ecosystem operation on this machine before we mitigated by eliminating the ancestor `memory/` directory.” (https://github.com/anthropics/claude-code/issues/53734)
- **#40541** — ez a legközvetlenebb bizonyíték arra, hogy maga a modell (nem csak az útvonal-logika) hibázik a hatókör-döntésben, *annak ellenére*, hogy a CLAUDE.md explicit szabályt tartalmazott: „Despite having explicit rules in CLAUDE.md stating \"do not mix information across scopes,\" Claude repeatedly: Wrote personal project info (port assignments from unrelated projects, SSH key locations) into team-shared Backlog tickets… Had to be corrected 5+ times in a single conversation for the same category of mistake.” A javasolt megoldás jellemző: nem a modell megbízhatóbbá tétele, hanem mechanikus kikényszerítés hook-kal: „CLAUDE.md rules about scope boundaries can be enforced mechanically with hooks… The hook runs at the process level — even when the model \"forgets\" the scope rule mid-conversation, the hook enforces it. No amount of attention drift can bypass a PreToolUse exit 2.” (https://github.com/anthropics/claude-code/issues/40541)
- **#36973 / #23341 / #25318** — dokumentáció/kód eltérés: a rendszer-prompt egy útvonalra utasítja az írást, a tényleges betöltő másikat olvas, ezért „every memory file written by following the system prompt's instructions ends up in a location that is **never auto-loaded**. The model (and the user) believe memories are persisting, but they're just regular files…” (#36973); az emlékek a nem dokumentált `MEMORY.md`-be íródnak `CLAUDE.md` helyett (#23341); majd külön hiba, hogy a `MEMORY.md` egyáltalán nem töltődött be a rendszer-promptba (#25318). (https://github.com/anthropics/claude-code/issues/36973, /issues/23341, /issues/25318)
- **#16600 / #19516 / #79233** — a memória-/szabályfájlok bejárása (traversal) git worktree-, Windows-meghajtóbetű- és profil- (`CLAUDE_CONFIG_DIR`) határokon lép át: pl. „`.claude/rules/*.md` auto-attachment still resolves rules from the **hardcoded default `~/.claude/rules/` path**, instead of `$CLAUDE_CONFIG_DIR/rules/`… This defeats the isolation purpose of `CLAUDE_CONFIG_DIR` for anyone running multiple profiles on one machine…content from one profile's `rules/` silently bleeds into every other profile.” (https://github.com/anthropics/claude-code/issues/79233)
- **Hivatalos dokumentáció megerősíti a modell szabadságát a döntésben:** „Auto memory… Claude doesn't save something every session. It decides what's worth remembering based on whether the information would be useful in a future conversation.” és „Claude treats them as context, not enforced configuration. To block an action regardless of what Claude decides, use a PreToolUse hook instead.” (https://code.claude.com/docs/en/memory) — vagyis a hivatalos dokumentáció szerint sincs a modellre bízva garantáltan betartott hatókör-szabály, a kikényszerítéshez explicit, a modellen kívüli hook kell.
- **MemoryTrap (OWASP GenAI blog, Cisco):** „Instead [of one prompt-injected action], it reached persistent memory, the global hooks configuration, and even influenced a highly trusted instruction layer through the system prompt. In other words, a one-time action could shape the model's future behavior across sessions, projects, and even reboots.” Anthropic válasza dokumentált: „To Anthropic's credit, after we at Cisco disclosed the issue, Claude Code v2.1.50 removed user memories from the system prompt, reducing the specific high-trust override path we identified.” (https://genai.owasp.org/2026/05/13/memory-is-a-feature-it-is-also-an-attack-surface/)

### 1.3 Cursor — projektek közötti memória-átszivárgás (fórumbejegyzések, T3)

Hivatalos GitHub-issue tracker helyett a Cursor közösségi fórumán dokumentált, ismétlődő panaszok:

- „The problem is that the cursor remembers the details of one project in another… I was working on a Go project creating an SSE library. Then I switched to another Svelte project… the cursor starts mentioning details of the SSE project in the Svelte project.” Válasz: „That's correct, memory is stored in the cloud, making it global for all projects.” (https://forum.cursor.com/t/reset-all-projects-memory/137390)
- „The docs say: Memories are automatically generated rules based on your conversations in Chat. These memories are scoped to your project… I don't believe it's true. I think memories are global… All those memories were very project-specific. (And Cursor added them, not me doing it manually, though I did approve them when asked.)” — ez azt is jelzi, hogy a Cursor emlék-mentésnél kér jóváhagyást a *tartalomra*, de nem a *hatókörre* (lásd 4. rész). (https://forum.cursor.com/t/rules-vs-memories-and-global-vs-project/137149)

### 1.4 Csapat-tudásbázis MCP-n keresztül — törölt kontextus szivárgása

- **Multica** (Claude Code/Cursor-provider-agnosztikus MCP-alapú agent-orchestrator) issue: „After an issue is deleted, a later agent task in the same Multica workspace/project can still reference content from the deleted issue… Claude Code auto memory is enabled by default and is stored per Git repository… This means issue A can cause Claude Code to write issue-specific facts into repository auto memory. Deleting issue A does not remove or invalidate those facts, and a fresh task for issue B in the same repository can receive them.” A karbantartó megerősítette a mechanizmust és pontosította a valódi kockázati felületet: „**Where the leak is real: `local_directory` project resources.** When a project is bound to a local directory, every issue on that (project, daemon) pair runs with the same fixed cwd… so all of them share one memory store… nothing ever cleans memory under `~/.claude/projects/`, so deleting an issue does not delete memory that was already written.” (https://github.com/multica-ai/multica/issues/6656)

### 1.5 Letta (MemGPT) — hatókör tervezésileg jó, de a runtime-elszigetelés megkerülhető

A Letta dokumentált tervezési elve: „Letta's isolation model relies on agent_id as the primary isolation key at both client and storage layers, not application-level conventions.” — de a figyelmeztetés is explicit: „if you accidentally reuse the same agent_id across different users or sessions, you'll get state leakage… isolation is enforced at the storage and client layer. If you bypass the client and write directly to the backend storage with careless queries, you can break isolation.” (https://theneuralbase.com/letta/learn/intermediate/isolation-guarantees/) Konkrét, megerősített sebezhetőség megosztott daemon/benchmark-környezetben: **#3388** — „Because the server lacks a hard tear-down or atomic block-flushing mechanism between independent tasks on the same daemon, these malicious memory modifications are permanently written to the database. Consequently, the poisoned context permanently leaks into subsequent, independent evaluation runs, breaking sandbox isolation.” (https://github.com/letta-ai/letta/issues/3388)

### 1.6 ChatGPT (OpenAI) memória — több, egymástól független incidens

- **Rehberger / indirekt prompt injection a memóriába (2024):** „Rehberger found that memories could be created and permanently stored through indirect prompt injection… He created a proof-of-concept exploit that used the vulnerability to exfiltrate all user input in perpetuity. OpenAI engineers took notice and issued a partial fix.” — a memória itt nem rossz *hatókörbe*, hanem illetéktelen *forrásból* (harmadik fél által manipulált tartalomból) került be, de ugyanabba, a felhasználó által implicit módon bizalminak tartott tárba. (https://arstechnica.com/security/2024/09/false-memories-planted-in-chatgpt-give-hacker-persistent-exfiltration-channel/)
- **2023. márciusi outage:** OpenAI saját elismerése szerint „a bug in an open source library” miatt „a small percentage of users were able to see the titles of other users' conversation history”, és később „it was possible for some users to see another active user's first and last name, email address, payment address, the last four digits… of a credit card number, and credit card expiration date.” Ez klasszikus cross-user leak, nem memória-specifikus (cache-hiba), de a felhasználók a memória-funkcióval társítják a jelenséget a későbbi panaszokban is. (https://www.vice.com/en/article/chatgpt-users-report-being-able-to-see-random-peoples-chat-histories/, https://mashable.com/article/openai-chatgpt-bug-exposed-user-data-privacy-breach)
- **Check Point Research, 2026 (T2, biztonsági kutatócég):** „a covert cross-account command channel through which an attacker could use a victim's ChatGPT session to execute hidden tasks… In our proof of concept, ChatGPT retrieved email data from the victim's connected Gmail account and relayed it to the attacker.” Ez a szolgáltatás-infrastruktúra (code-execution container metaadat-tárolója) szintjén, nem a „memory” terméken keresztül történt, de ugyanazt az architekturális hibaosztályt mutatja: „a shared internal service became an unintended communication layer across environments that were supposed to remain isolated.” (https://cybernoz.com/the-shared-clipboard-inside-the-sandbox-cross-account-data-leakage-in-chatgpt/)
- Kevésbé megerősített, felhasználói beszámoló-szintű esetek (T3, csak egy forrás, nem tudtuk függetlenül megerősíteni): egy TikTok-videó alapján írt cikk arról, hogy egy felhasználó szerint más beszélgetés szivárgott a sajátjába (NY Post, 2025. június) — ezt az OpenAI nem erősítette meg nyilvánosan, ezért **NINCS FORRÁS** a mechanizmusra, csak a panasz létezésére. (https://nypost.com/2025/06/10/tech/chatgpt-user-alarmed-as-ai-tool-shares-others-private-info/)

### 1.7 GitHub Copilot — nem klasszikus hatókör-szivárgás, de rokon architekturális kockázat

A Copilot custom instructions/repository-instructions rendszerében nem találtunk dokumentált cross-repo memória-szivárgási *hibát* (bug reportot); az itt talált incidensek prompt injection útján történő adatszivárgásról szólnak, ami más kockázati kategória, de ugyanannak a mintázatnak ("bizalmi határ nélkül kezelt, perzisztensen betöltött szöveg") a következménye: „researchers have found a way to trick the GitHub Copilot chatbot into leaking sensitive data, such as AWS keys, from private repositories… exploitable through comments hidden in pull requests.” (https://www.csoonline.com/article/4069887/github-copilot-prompt-injection-flaw-leaked-sensitive-data-from-private-repos.html); illetve a Codespaces „RoguePilot” lánc: „a malicious GitHub issue can trigger a passive prompt injection in Copilot… allowing the attacker's instructions to be silently executed… to leak a privileged GITHUB_TOKEN secret.” (https://orca.security/resources/blog/roguepilot-github-copilot-vulnerability/, megerősítve: https://www.securityweek.com/github-issues-abused-in-copilot-attack-leading-to-repository-takeover/) **NINCS FORRÁS** arra, hogy a Copilot repository-instructions rendszere valaha ténylegesen egyik repóból a másikba tévesen töltött volna be perzisztens memóriát — csak arra van dokumentáció, hogy a betöltési hierarchia (personal > repository > organization, mindegyik egyszerre a promptba kerül) tervezésileg is minden szintet együtt ad át a modellnek: „all sets of relevant instructions are provided to Copilot.” (https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions)

## 2. Minták a cél (hatókör) kiválasztására, és mit mond erről a biztonsági szakirodalom

### 2.1 A talált minták a gyakorlatban

| Minta | Példa | Következmény |
|---|---|---|
| **Kötelező explicit paraméter, de az érték szabadon jön a hívótól** | mem0: „At least one of `user_id`, `agent_id`, or `run_id` is required” — de az *érték* forrása az alkalmazás/ügynök, amit a `metadata` felülírhatott (l. 1.1) | A kötelezőség önmagában nem elég, ha az érték integritása nincs védve write-kor |
| **Szerver-oldali, identitásszolgáltatótól származó alapértelmezés (trust boundary a modellen kívül)** | AWS Bedrock AgentCore Memory ABAC mintája: „Use your identity provider as a trusted source for tenant context… actorId = \"{tenantId}:{agentId}:{userId}\"… The trust policy of the role enforces that only the execution role of the agent is allowed to assume it.” | A hatókört nem a modell, hanem az OAuth/IAM-réteg állítja elő és kényszeríti ki kriptográfiailag |
| **„Aktív projekt” implicit állapot (cwd/fájlrendszer-útvonal)** | Claude Code auto-memory: `~/.claude/projects/{path-derived-key}/memory/` | Worktree-törlés, átnevezés, ős-könyvtárra „felsétálás”, Windows meghajtóbetű-eltérés — mind dokumentált hibaforrás (l. 1.2) |
| **Projektenkénti végpont/konfiguráció** | `CLAUDE_CONFIG_DIR` profilok, `autoMemoryDirectory` beállítás | Az izoláció csak akkor működik, ha *minden* alrendszer (nem csak a fő betöltő) tiszteletben tartja — a #79233 hiba pont azt mutatja, hogy egy alrendszer (rules auto-attachment) kimaradt a profil-tudatosságból |

### 2.2 Biztonsági ajánlások: a hatókört a hívó környezet, nem a modell határozza meg

**OWASP Top 10 for LLM Applications 2025 — LLM06 Excessive Agency**, a leginkább releváns tétel: „**Execute extensions in user's context** Track user authorization and security scope to ensure actions taken on behalf of a user are executed on downstream systems in the context of that specific user, and with the minimum privileges necessary.” és „**Complete mediation** Implement authorization in downstream systems **rather than relying on an LLM to decide if an action is allowed or not**. Enforce the complete mediation principle so that all requests made to downstream systems via extensions are validated against security policies.” (https://genai.owasp.org/llmrisk/llm06-sensitive-information-disclosure/, azonos szöveg: https://owasp.org/www-project-top-10-for-large-language-model-applications/2_0_vulns/LLM06_ExcessiveAgency)

**OWASP Top 10 for Agentic Applications 2026 — ASI03 (Identity/Privilege Abuse) és ASI06 (Memory & Context Poisoning):** „2. Memory-Based Privilege Retention & Data Leakage. Arises when agents cache credentials, keys, or retrieved data for context and reuse. If memory is not segmented or cleared between tasks or users, attackers can prompt the agent to reuse cached secrets, escalate privileges, or leak data from a prior secure session into a weaker one.” Mitigáció: „**Isolate Agent Identities and Contexts**: Run per-session sandboxes with separated permissions and memory, wiping state between tasks…” és a memóriaírásra nézve: „Verify that agent outputs, tool outputs, and orchestration results are **not automatically written to trusted agent memory without explicit source validation** (e.g., content-origin checks or write-authorization controls that verify the content's source before committing writes).” (https://genai.owasp.org/download/52117, https://github.com/OWASP/AISVS/blob/main/research/chapters/C08-Memory-and-Embeddings/C08-02-Embedding-Sanitization-Validation.md)

**OWASP Top 10 for MCP — MCP10:2025 Context Injection & Over-Sharing**, közvetlenül a kutatási kérdésre válaszol: „In MCP-based systems, context acts as the working memory for agents… When this context is shared, persistently stored, or insufficiently scoped, sensitive information from one session, agent, or user can leak into another… Your MCP system is vulnerable if: … Sensitive data enters context without classification or tagging… Agents can access each other's memory without access checks.” Ajánlott kontroll: „**Context Isolation & Segmentation** — Assign unique context namespaces per: User / Agent / Workflow / Tenant… Prevent one agent from accessing another agent's memory directly. In multi-tenant setups, isolate retrieval indexes and vector stores.” (https://github.com/OWASP/www-project-mcp-top-10/blob/master/2025/MCP10-2025%E2%80%93ContextInjection%26OverSharing.md)

**Model Context Protocol hivatalos specifikáció** ugyanezt a modellt követi az *engedélyezés* (authorization) szintjén: a hatókört (OAuth *scope*) a szerver hirdeti meg (`scopes_supported`, `WWW-Authenticate`), a kliens kéri le, de a döntést végső soron az OAuth-szerver és a felhasználói jóváhagyás hozza — nem a modell: „Implement a progressive, least-privilege scope model… MCP clients typically lack domain-specific knowledge to make informed decisions about individual scope selection. Requesting all available scopes allows the authorization server and end-user to determine appropriate permissions during the consent process.” (https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices) Fontos, hogy **maga az MCP-protokoll szándékosan nem definiál munkamenet-/„aktív projekt”-fogalmat** — ez pontosan egybevág a `_kozos.txt`-ben leírt architektúrával (2026-07-28 protokoll, nincs kézfogás, nincs munkamenet), vagyis a hatókör-azonosítás terhét explicit módon a hívó félre (kliens/host) tolja át, nem oldja meg helyette.

**Konkrét, iparági implementáció, amely a fenti elvet követi:** AWS Bedrock AgentCore Memory háromdimenziós izolációja — „Tenant isolation (`tenantId`)… Agent isolation (`agentId`)… User isolation (`userId`)… You need a trusted source for `tenantId` and `userId`. Consider using a JSON Web Token (JWT) with inbound authentication… the identity provider is a trusted source.” (https://builder.aws.com/content/3C1SCSoe15VaBnmsiMIfGcZfhxM/secure-shared-multi-tenant-agent-memory-namespaces-using-agentcore-memory) — vagyis az azonosítót (ki a felhasználó, melyik a projekt) egy, a modelltől független, kriptográfiailag ellenőrzött csatorna (JWT/IdP) szolgáltatja, nem a modell „belátása”.

**AWS Well-Architected Agentic AI Lens** még explicitebb a modell-alapú döntés kockázatáról: „Risk classification itself can't rely on an LLM exposed to the same untrusted content as the request being evaluated, because adversarial content could [trick] the classifier into marking the request as low-risk. **Use deterministic logic (policy engines, rule-based classifiers) as the authoritative signal, with LLM-assisted classification as an optional input that a deterministic layer re-checks.**” (https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentsec04-bp02.html)

**Összegzés a 2. kérdésre:** a fellelt szakirodalom és iparági minta egyöntetűen azt mondja, hogy a *cél/hatókör* kiválasztását nem szabad a modellre (LLM) bízni mint egyedüli, megbízható döntéshozóra; a hívó környezetnek (identitásszolgáltató, host-alkalmazás, downstream policy-engine) kell azt determinisztikusan, ellenőrizhető módon biztosítania, a modell legfeljebb *jelöltet* javasolhat, amit egy nem-LLM réteg validál commit előtt.

## 3. Mérés arra, mennyire pontosan dönt egy LLM-ágens személyes/projekt/közös kérdésben

**CIMemories (Meta FAIR, ICLR 2026 — T1, lektorált konferenciacikk)** ez idáig az egyetlen talált, kifejezetten erre a kérdésre irányuló, számszerű benchmark. Módszertana: szintetikus felhasználói profilok (100+ attribútum/felhasználó), párosítva feladat-kontextusokkal, amelyekben minden attribútum egyes feladatokhoz szükséges, másokhoz nem megfelelő (Nissenbaum kontextuális integritás elmélete alapján). Eredmény: „Our evaluation reveals that frontier models exhibit **up to 69% attribute-level violations** (leaking information inappropriately), with lower violation rates often coming at the cost of task utility. Violations accumulate across both tasks and runs: as usage increases from 1 to 40 tasks, GPT-5's violations rise from 0.1% to 9.6%, reaching **25.1% when the same prompt is executed 5 times**, revealing arbitrary and unstable behavior in which models leak different attributes for identical prompts. Privacy-conscious prompting does not solve this—models overgeneralize, sharing everything or nothing rather than making nuanced, context-dependent decisions.” (https://proceedings.iclr.cc/paper_files/paper/2026/file/9a2bcfaf383638e166162a25b6dff125-Paper-Conference.pdf, kód: https://github.com/facebookresearch/CIMemories)

Ez a szám (69% attribútumszintű, és 0,1%→25,1% instabilitás azonos prompt ismétlésekor) közvetlen mérőszámot ad arra, hogy egy LLM *önmagában*, kontextusérzékeny "megosszam vagy ne" döntésben mennyire megbízhatatlan — ez analóg a "személyes vs. projekt vs. közös" döntéssel, csak "feladatkontextus vs. attribútum" tengelyen méri. **Ez a konkrét szám és módszertan jelenleg egyetlen forrásból származik**, két független megerősítő forrást nem találtunk ugyanerre a számra (lásd „Ellentmondások/korlátok” rész) — de az irány (LLM-ek megbízhatatlanok kontextusfüggő megosztási döntésben) közvetve alátámasztott más, rokon jellegű mérésekkel: az OWASP AISVS dokumentum idézi a „Hidden in Memory: Sleeper Memory Poisoning” munkát („measured 99.8% storage success on GPT-5.5 and 95% on Kimi-K2.6, with 60-89% of successful retrievals influencing harmful agentic actions”) és a MINJA módszert („98.2% injection success rate and 76.8% attack success rate, while evading Llama Guard input/output moderation”) — ezek más metrikát mérnek (mérgezés-siker, nem hatókör-osztályozási pontosság), így nem tekinthetők a CIMemories 69%-os számának közvetlen megerősítésének, csak azt támasztják alá, hogy a memória-tartalom eredetének/bizalmi szintjének kezelése rendszerszinten gyenge láncszem. (https://github.com/OWASP/AISVS/blob/main/research/chapters/C08-Memory-and-Embeddings/C08-02-Embedding-Sanitization-Validation.md)

**Gyakorlati, nem-benchmark jellegű, de jól dokumentált bizonyíték** ugyanerre: a fent idézett Claude Code #40541 issue, ahol a modell CLAUDE.md-ben explicit leírt hatókör-szabályt (ne keverd a personal/project/team-shared infót) ismételten, 5+ alkalommal megsértett ugyanabban a beszélgetésben, annak ellenére, hogy a szabály a kontextusában volt — ez direkt megfigyelés (n=1 felhasználó, de részletes, reprodukálható leírással) arra, hogy a puszta *instrukció jelenléte* a promptban nem garantálja a helyes hatókör-döntést futásidőben. Erre a konkrét jelenségre (explicit rule + repeated violation) nem találtunk formális, számszerűsített második független benchmark-forrást, de a jelenség kvalitatívan egybevág a CIMemories „privacy-conscious prompting does not solve this” megállapításával, ami két, egymástól független forrásból (egy ipari bug report + egy akadémiai benchmark) származó, egymást megerősítő mintázatnak tekinthető.

**mem0 „szintek” (levels) — nem mérés, hanem tervezési dokumentáció:** a mem0 saját dokumentációja azt írja le, hogy a réteg (user/session/agent/org) kiválasztását *nem* a modell dönti el automatikusan egy adott ténynél, hanem a hívó alkalmazás explicit paraméterezése és/vagy egy külön "routing" logika (ami maga is lehet LLM-alapú, de a mem0 dokumentáció kifejezetten hangsúlyozza, hogy ez „explicit és megfigyelhető” kell legyen): „These parts can themselves be mediated by an LLM, but the memory operations they drive should be explicit and observable.” (https://mem0.ai/blog/context-engineering-for-ai-agents-how-to-route-queries-to-memory) — ez megerősíti a 2. részben leírt elvet, de nem ad pontossági mérőszámot.

**NINCS FORRÁS** arra, hogy létezne publikált, közvetlenül a "personal vs. project vs. shared" hármas osztályozásra (nem csak kétosztályú "megosszam/ne osszam meg" döntésre) irányuló kvantitatív benchmark bármelyik konkrét terméknél (Claude Code auto-memory, mem0 saját LLM-alapú kategorizálója, ChatGPT memory-classifier). A CIMemories a legközelebbi rokon, de az ő tengelye feladatkontextus, nem tárolási hatókör.

## 4. Kérnek-e visszaigazolást érzékeny helyre íráskor? „Előbb szól, aztán ír” minta?

**A vizsgált memória-rendszerek alapértelmezett viselkedése: csendes írás, legfeljebb utólagos értesítés — nem előzetes jóváhagyás.**

- **ChatGPT / OpenAI:** a hivatalos termékbejegyzés szerint a visszajelzés utólagos, nem előzetes: „ChatGPT now lets you know when memories are updated. We've also made it easier to access all memories when updates occur—hover over \"Memory updated,\" then click \"Manage memories\" to review everything.” (https://openai.com/index/memory-and-new-controls-for-chatgpt/) A felhasználónak nincs lehetősége az írás *előtt* jóváhagyni vagy elutasítani — csak utólag törölheti. Ez pontosan az OWASP LLM06 „Excessive Autonomy” mintapéldájának felel meg: „An LLM-based application or extension fails to independently verify and approve high-impact actions.” (https://owasp.org/www-project-top-10-for-large-language-model-applications/2_0_vulns/LLM06_ExcessiveAgency)
- **Claude Code auto-memory:** a hivatalos dokumentáció nem említ előzetes jóváhagyási lépést; a `/memory` paranccsal utólag tekinthető meg és szerkeszthető, illetve globálisan ki/be kapcsolható, de író-döntésenkénti visszaigazolás nincs beépítve — ezt közvetve megerősíti a korai felhasználói kritika is (2026 eleji GitHub-vita): „This behaviour should really be *opt-in* if it should exist at all — good users carefully curate what goes into their memory files; now we're suddenly telling Claude to write whatever session-specific minutiae it likes to a file which is automatically loaded into *every* future session… The cherry on top is that the user has *no* way of seeing what Claude is writing to this file from the Claude Code CLI.” (https://github.com/anthropics/claude-code/issues/23341)
- **mem0 core API:** az `add()`/`update()` hívások szinkron vagy aszinkron módon azonnal, jóváhagyás nélkül íródnak; a `custom_instructions` mechanizmus *tartalmi* szűrést tesz lehetővé („Only store CONFIRMED medical facts… Ignore: Speculation…”), de ez is előre beállított szabály, nem interaktív, hívásonkénti visszaigazolás. (https://mem0.mintlify.app/cookbooks/essentials/controlling-memory-ingestion) Kivétel a **mem0 „dream” konszolidációs skill**, amely kifejezetten diff-alapú emberi jóváhagyást kér, de csak a *már tárolt* emlékek egyesítésénél/törlésénél, nem az új írásoknál: „All proposed changes are shown as a diff for user approval before anything is modified… If the user types `n` or `no`… print `Cancelled. No changes made.`” (https://github.com/mem0ai/mem0/blob/b357a5a1b03c299ec8229c268e63cfac0f7c6566/integrations/mem0-plugin/skills/dream/SKILL.md) — fontos, hogy a `_kozos.txt` szerint ez a funkció (dream) az easter-memory-system tervezésében explicit módon el lett vetve, tehát erre nem építhető a végleges megoldás.
- **Cursor:** legalább *néhány* memória-mentésnél megjelenik egy jóváhagyási lépés a tartalomra ("though I did approve them when asked"), de a hatókörre (global vs. project) nem: a felhasználó panasza pont az volt, hogy a jóváhagyott tartalom végül rossz (globális) hatókörbe került. (https://forum.cursor.com/t/rules-vs-memories-and-global-vs-project/137149)

**Harmadik féltől származó, explicit "kérdezz, mielőtt írsz" megoldások léteznek, de nem a vizsgált memória-rendszerek natív részeként:**
- **TealTiger** (javasolt mem0-middleware, a mem0 karbantartói elutasították core-be integrálásra, „cookbook”-ként ajánlva): „Pre-write governance (before memory.add): TealTiger intercepts content before it reaches Mem0 storage… Scope enforcement ensures agents can only write to authorized scopes.” (https://github.com/mem0ai/mem0/issues/5507)
- **Agent Memory Guard** (OWASP-projekt): „Enforces declarative YAML security policies on memory read/write operations… Captures snapshots for forensic analysis and enables rollback.” (https://owasp.org/www-project-agent-memory-guard/)
- **Általános agentikus keretrendszerek human-in-the-loop middleware-jei** (LangChain HITL, AWS Bedrock Agents „User Confirmation”/„Return of Control”, Cloudflare `needsApproval`) mind explicit, tool-hívásonkénti jóváhagyási mintát kínálnak, kockázat szerint rétegezve: „read-only operations proceed autonomously, low-risk writes require single-reviewer approval, and higher-risk operations… require stricter approval.” (https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentsec04-bp02.html) Ezek azonban általános tool-hívás-jóváhagyási keretek, nem memória-specifikus, „hova írjak” döntést kérnek — a döntés tárgya jellemzően „szabad-e ez a write egyáltalán”, nem „melyik hatókörbe kerüljön”.

**Az OWASP explicit ajánlása a „szól, mielőtt ír” mintára:** „**Human-in-the-Loop for Sensitive Context** — Require approval before sensitive context is: Exported / Summarized / Shared across agents. Show a preview of context that will be reused.” (MCP Top 10, MCP10:2025) és „Require user approval… before [high-impact actions] are taken” (OWASP LLM06). Ezek ajánlásként léteznek, de — a fenti 1–3. rész bizonyítékai alapján — a gyakorlatban vizsgált négy termék (mem0, ChatGPT, Claude Code, Cursor) egyike sem valósítja meg alapértelmezésben az írás *előtti* hatókör-jóváhagyást; mindegyik legfeljebb utólagos láthatóságot/törlési lehetőséget ad.

## Ellentmondások

1. **Claude Code worktree-memória iránya:** a #41283 issue szerint a jelenlegi (javított) viselkedés — worktree-k a fő repó memóriájára oldódnak fel — helyes lépés volt egy korábbi hibához (árva emlékek) képest, de a #53734 issue szerint ugyanez a „felfelé sétálás” (walk-up) más esetekben *rossz* (ős-könyvtárba, más ügynök memóriájába) oldódik fel. A hivatalos repó vitájában két, egymásnak ellentmondó igény ütközik: „#39920 and #30667 want per-worktree memory separation — but per-worktree memory is what caused orphaned memories in the first place” — vagyis nincs konszenzus arról, hogy a worktree-izoláció szigorítása vagy lazítása a helyes irány; ezt a Claude Code csapat még nem zárta le architekturálisan.
2. **A „ki jóváhagyja a tartalmat” és a „ki jóváhagyja a hatókört” összemosódik:** a Cursor-fórum bejegyzésben a felhasználó jóváhagyta a memória *tartalmát* ("I did approve them when asked"), mégis rossz *hatókörbe* került — ez azt jelzi, hogy még ahol van jóváhagyási UI, ott sem feltétlenül a hatókör-döntés a jóváhagyás tárgya. Nincs olyan forrásunk, amely ezt a különbséget explicit terméktervezési elvként dokumentálná; ez a mi következtetésünk a rendelkezésre álló elsődleges forrásokból.
3. **mem0 karbantartói álláspontja a governance-rétegről:** a mem0 csapat elutasította a TealTiger pre-write governance beépítését a core SDK-ba ("we like to keep the core SDK lean"), miközben ugyanabban az időszakban saját P0-critical hibákat javítottak ki pont a hatókör-integritás miatt — ez a két döntés (lean core vs. write-authorization gap) feszültségben áll egymással, de nem tudjuk megerősíteni, hogy a mem0 csapat ezt maga is ellentmondásnak látja-e; csak a két, egymástól független GitHub-forrásból dokumentált tényt tudjuk egymás mellé állítani.

## Amire NINCS forrás

- Nincs publikált, közvetlenül a „personal / project / shared” hármas hatókör-osztályozásra (nem kétosztályú megosztás/nem-megosztás döntésre) irányuló kvantitatív benchmark egyik vizsgált termékre (Claude Code, mem0, ChatGPT, Cursor) sem.
- Nincs második, egymástól független forrás a CIMemories 69%-os attribútum-szintű szabálysértési számára és a GPT-5 0,1%→9,6%→25,1% instabilitási görbéjére — ez jelenleg egyetlen (bár lektorált, T1) forrásból származik.
- Nincs hivatalos OpenAI-dokumentáció vagy elsődleges forrás arra a — másodkézből (OWASP AISVS dokumentumból) idézett — állításra, hogy „OpenAI and Google shipped… confirmation prompts for sensitive memory operations” 2025–2026 folyamán; ezt az AISVS dokumentum állítja, de mi nem találtunk ehhez elsődleges OpenAI/Google közleményt, ezért ezt az állítást nem tekintjük megerősítettnek.
- Nincs dokumentált konkrét incidens arra, hogy a GitHub Copilot repository-instructions rendszere valaha ténylegesen egyik repository memóriáját/instrukcióját tévesen egy másik repository kontextusába töltötte volna be (a talált Copilot-incidensek mind prompt injection útján történő adatszivárgásról szólnak, ami más hibaosztály).
- Nincs megerősített forrás a NY Post-cikkben leírt ChatGPT „más beszélgetés szivárgott be” felhasználói panasz technikai mechanizmusára; OpenAI nem erősítette meg nyilvánosan.
- Nincs forrásunk arra, hogy a mem0, Claude Code vagy ChatGPT valaha is alapértelmezésben, natívan megvalósított volna írás *előtti*, hatókör-specifikus emberi jóváhagyást ("ask first, then write" a scope-ra nézve) — ezt a hiányt magát dokumentáltuk (l. 4. rész), de ez negatív bizonyíték (a keresés nem talált ilyet), nem pozitív megerősítés arról, hogy ilyen funkció biztosan nem létezik sehol.

## Meglátogatott és felderített linkek

| Cím | URL | Tier | Eszköz | Megjegyzés |
|---|---|---|---|---|
| update() lets caller metadata silently overwrite user_id/agent_id/run_id (mem0 #6277) | https://github.com/mem0ai/mem0/issues/6277 | T1 | Exa fetch | P0-critical, Python SDK, javítva PR #6278 |
| update() metadata overwrite TS SDK (mem0 #6342) | https://github.com/mem0ai/mem0/issues/6342 | T1 | Exa search | TS testvérhiba |
| fix(ts-oss) PR (mem0 #6343) | https://github.com/mem0ai/mem0/pull/6343 | T1 | Exa search | javítás részletei, camelCase alias rés is |
| fix(memory) PR (mem0 #6278) | https://github.com/mem0ai/mem0/pull/6278 | T1 | Exa search | Python javítás, injection-eset is |
| add() lets metadata set identity scope on creation (mem0 #6655) | https://github.com/mem0ai/mem0/issues/6655 | T1 | Exa search | creation-time hatókör-injektálás |
| add() mutates caller's filters object (mem0 #6796) | https://github.com/mem0ai/mem0/issues/6796 | T1 | Exa search | 10/10 repró, scope guard megkerülve |
| addMemory metadata excluded from retrieval/partitioning (mem0 #5121) | https://github.com/mem0ai/mem0/issues/5121 | T1 | Exa search | multi-app_id keveredés |
| Cross-scope entity linking (mem0 #5439) | https://github.com/mem0ai/mem0/issues/5439 | T1 | Exa search | entitás-boost cross-scope szivárgás |
| Cross-scope entity linking TS (mem0 #5597) | https://github.com/mem0ai/mem0/issues/5597 | T1 | Exa search | TS testvérhiba |
| TealTiger governance layer proposal (mem0 #5507) | https://github.com/mem0ai/mem0/issues/5507 | T1 | Exa search | elutasítva core-ba, cookbook javasolva |
| mem0 group chat wrong user_id (hermes-agent #64340) | https://github.com/NousResearch/hermes-agent/issues/64340 | T2 | Exa search | cache-alapú attribúciós hiba, provider-generic |
| Memory identity from filesystem path (Claude Code #41283) | https://github.com/anthropics/claude-code/issues/41283 | T1 | Exa fetch | worktree/rename orphaning, human-vs-project gap |
| Claude ignores CLAUDE.md scope rules (Claude Code #40541) | https://github.com/anthropics/claude-code/issues/40541 | T1 | Exa search | modell ismétlődő hatókör-hiba, hook-alapú javaslat |
| auto-memory resolver walks to ancestor (Claude Code #53734) | https://github.com/anthropics/claude-code/issues/53734 | T1 | Exa search | 8 dokumentált cross-agent contamination incidens |
| System prompt memory instructions wrong path (Claude Code #36973) | https://github.com/anthropics/claude-code/issues/36973 | T1 | Exa search | dokumentáció/kód eltérés |
| Memory saved to undocumented MEMORY.md (Claude Code #23341) | https://github.com/anthropics/claude-code/issues/23341 | T1 | Exa search | opt-out only, nincs jóváhagyás |
| MEMORY.md not loaded into system prompt (Claude Code #25318) | https://github.com/anthropics/claude-code/issues/25318 | T1 | Exa search | |
| Memory traversal should respect worktree boundaries (Claude Code #16600) | https://github.com/anthropics/claude-code/issues/16600 | T1 | Exa search | EnterWorktree tool okozta ős-betöltés |
| Duplicate memory files on Windows (Claude Code #19516) | https://github.com/anthropics/claude-code/issues/19516 | T1 | Exa search | drive-letter case bug, javítva 2.1.47 |
| CLAUDE_CONFIG_DIR not honored by rules auto-attachment (Claude Code #79233) | https://github.com/anthropics/claude-code/issues/79233 | T1 | Exa search | profil-izoláció megkerülése |
| Feature request user-level scope (Claude Code #83831) | https://github.com/anthropics/claude-code/issues/83831 | T1 | Exa search | workaround: autoMemoryDirectory, all-or-nothing |
| Docs omit autoMemoryDirectory (Claude Code #33709) | https://github.com/anthropics/claude-code/issues/33709 | T1 | Exa search | dokumentáció utólag javítva |
| Warn when auto-memory starts empty (Claude Code #68368) | https://github.com/anthropics/claude-code/issues/68368 | T1 | Exa search | fragmentáció-detekció hiánya |
| How Claude remembers your project (hivatalos dokumentáció) | https://code.claude.com/docs/en/memory | T1 | Exa search | „Claude treats them as context, not enforced configuration” |
| Reset all projects memory (Cursor fórum) | https://forum.cursor.com/t/reset-all-projects-memory/137390 | T3 | Exa search | felhasználói panasz, projektek közti szivárgás |
| Rules vs. Memories and Global vs. Project (Cursor fórum) | https://forum.cursor.com/t/rules-vs-memories-and-global-vs-project/137149 | T3 | Exa search | tartalom jóváhagyva, hatókör mégis rossz |
| Cursor/Claude Code leak deleted issue context (Multica #6656) | https://github.com/multica-ai/multica/issues/6656 | T2 | Exa search | local_directory resource a valódi rés |
| Isolation guarantees (Letta, The Neural Base) | https://theneuralbase.com/letta/learn/intermediate/isolation-guarantees/ | T2 | Exa search | agent_id mint elsődleges izolációs kulcs |
| Cross-Session State Leakage (Letta #3388) | https://github.com/letta-ai/letta/issues/3388 | T1 | Exa search | daemon-szintű persona-mérgezés, javasolt ephemeral-memory fix |
| Hacker plants false memories in ChatGPT (Ars Technica) | https://arstechnica.com/security/2024/09/false-memories-planted-in-chatgpt-give-hacker-persistent-exfiltration-channel/ | T2 | Exa search | Rehberger kutatása, indirekt prompt injection a memóriába |
| ChatGPT bug exposed private data (Mashable) | https://mashable.com/article/openai-chatgpt-bug-exposed-user-data-privacy-breach | T2 | Exa search | 2023 márciusi outage, OpenAI hivatalos elismerése |
| ChatGPT users see random people's chat histories (Vice) | https://www.vice.com/en/article/chatgpt-users-report-being-able-to-see-random-peoples-chat-histories/ | T2 | Exa search | Sam Altman idézett elismerése |
| ChatGPT user alarmed AI shares others' info (NY Post) | https://nypost.com/2025/06/10/tech/chatgpt-user-alarmed-as-ai-tool-shares-others-private-info/ | T3 | Exa search | megerősítetlen felhasználói panasz |
| The Shared Clipboard Inside the Sandbox (Check Point / Cybernoz) | https://cybernoz.com/the-shared-clipboard-inside-the-sandbox-cross-account-data-leakage-in-chatgpt/ | T2 | Exa search | cross-account covert channel, 2026 |
| Memory and new controls for ChatGPT (OpenAI hivatalos) | https://openai.com/index/memory-and-new-controls-for-chatgpt/ | T1 | Exa search | „Memory updated” utólagos értesítés, nem előzetes jóváhagyás |
| ChatGPT memory guide (OpenAI Help Center) | https://help.openai.com/en/articles/6825453-chatgpt-memory-a-guide | T1 | Exa search | memory summary, temporary chat |
| OWASP Top 10 for LLM Applications 2025 (PDF) | https://genai.owasp.org/download/43299/ | T1 | Exa search | LLM02, LLM06 teljes szöveg |
| LLM06:2025 Excessive Agency (OWASP GenAI) | https://genai.owasp.org/llmrisk/llm06-sensitive-information-disclosure/ | T1 | Exa search | complete mediation, execute in user's context |
| LLM06 ExcessiveAgency (owasp.org wiki) | https://owasp.org/www-project-top-10-for-large-language-model-applications/2_0_vulns/LLM06_ExcessiveAgency | T1 | Exa search | azonos tartalom, elsődleges wiki |
| MCP10-2025 Context Injection & Over-Sharing (OWASP MCP Top 10) | https://github.com/OWASP/www-project-mcp-top-10/blob/master/2025/MCP10-2025%E2%80%93ContextInjection%26OverSharing.md | T1 | Exa search | közvetlen válasz a kutatási kérdésre |
| OWASP Top 10 for Agentic Applications 2026 (PDF) | https://genai.owasp.org/download/52117 | T1 | Exa search | ASI03, ASI06, memory-based privilege retention |
| AISVS C08-02 Embedding Sanitization/Validation | https://github.com/OWASP/AISVS/blob/main/research/chapters/C08-Memory-and-Embeddings/C08-02-Embedding-Sanitization-Validation.md | T1 | Exa search | write-authorization control 8.2.4, sleeper memory poisoning idézetek |
| Memory Is a Feature. It Is Also an Attack Surface (OWASP GenAI blog, Cisco) | https://genai.owasp.org/2026/05/13/memory-is-a-feature-it-is-also-an-attack-surface/ | T1 | Exa search | MemoryTrap, Anthropic Claude Code 2.1.50 javítás |
| OWASP Agent Memory Guard | https://owasp.org/www-project-agent-memory-guard/ | T1 | Exa search | policy-alapú memory read/write interception |
| Security Best Practices (MCP hivatalos) | https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices | T1 | Exa search | scope minimization, progressive least-privilege |
| Authorization spec (MCP hivatalos, 2026-07-28) | https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization | T1 | Exa search | scope selection strategy, step-up authorization |
| Secure shared multi-tenant agent memory namespaces (AWS builder) | https://builder.aws.com/content/3C1SCSoe15VaBnmsiMIfGcZfhxM/secure-shared-multi-tenant-agent-memory-namespaces-using-agentcore-memory | T2 | Exa search | ABAC, actorId = tenantId:agentId:userId, IdP mint trusted source |
| AWS Well-Architected Agentic AI Lens — human review | https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentsec04-bp02.html | T1 | Exa search | deterministic policy engine vs. LLM classifier |
| CIMemories paper (ICLR 2026 proceedings PDF) | https://proceedings.iclr.cc/paper_files/paper/2026/file/9a2bcfaf383638e166162a25b6dff125-Paper-Conference.pdf | T1 | Exa fetch | 69% violation, GPT-5 instabilitás, lektorált cikk |
| CIMemories repo (Meta FAIR / facebookresearch) | https://github.com/facebookresearch/CIMemories | T1 | Exa fetch | kód és adatkészlet, azonos számok megerősítve |
| AI Agent Memory Governance (mem0 blog) | https://mem0.ai/blog/ai-agent-memory-governance-meaning-best-practices-for-secure-memory | T2 | Exa search | identity-based scoping, consent/provenance metaadat |
| Add Memory / memory-types / entity-scoped-memory (mem0 hivatalos docs) | https://docs.mem0.ai/core-concepts/memory-operations/add , https://docs.mem0.ai/core-concepts/memory-types , https://docs.mem0.ai/platform/features/entity-scoped-memory | T1 | Exa search | user_id/agent_id/app_id/run_id rétegek, explicit paraméterezés |
| Controlling memory ingestion (mem0 cookbook) | https://mem0.mintlify.app/cookbooks/essentials/controlling-memory-ingestion | T1 | Exa search | custom_instructions szűrés, nem interaktív jóváhagyás |
| mem0 dream skill (SKILL.md) | https://github.com/mem0ai/mem0/blob/b357a5a1b03c299ec8229c268e63cfac0f7c6566/integrations/mem0-plugin/skills/dream/SKILL.md | T1 | Exa search | diff-alapú jóváhagyás, de csak konszolidációnál |
| Context engineering for AI agents — routing to memory (mem0 blog) | https://mem0.ai/blog/context-engineering-for-ai-agents-how-to-route-queries-to-memory | T2 | Exa search | „explicit and observable” routing elve |
| RoguePilot: Exploiting GitHub Copilot (Orca Security) | https://orca.security/resources/blog/roguepilot-github-copilot-vulnerability/ | T2 | Exa search | Codespaces prompt injection lánc |
| GitHub Issues Abused in Copilot Attack (SecurityWeek) | https://www.securityweek.com/github-issues-abused-in-copilot-attack-leading-to-repository-takeover/ | T2 | Exa search | RoguePilot megerősítése |
| GitHub Copilot prompt injection leaked private repo data (CSO Online) | https://www.csoonline.com/article/4069887/github-copilot-prompt-injection-flaw-leaked-sensitive-data-from-private-repos.html | T2 | Exa search | Camo-bypass adatszivárgás |
| Add repository custom instructions (GitHub hivatalos docs) | https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions | T1 | Exa search | „all sets of relevant instructions are provided” |

---

# ELL01 — Az MCP-specifikáció és a kliensek állításainak ellenőrzése

**Módszer:** Egyetlen kutató-ügynökként (alügynök-indítás nélkül, degradált módban, a `deep-web-research` skill elvei szerint), kizárólag `mcp__Exa__web_search_exa` / `mcp__Exa__web_fetch_exa` eszközökkel. A korábbi kör (`sq01-mcp-spec.md`, `sq03-kliensek.md`) idézeteit nem vettem át ellenőrzés nélkül: minden állításhoz újra megkerestem és elolvastam az elsődleges forrást (SEP-oldalak, hivatalos spec, forráskód, GitHub issue-k), és ahol lehetett, friss, a korábbi körtől független második forrást is kerestem. A mai dátum 2026-09-25.

## Verdikt-összefoglaló

| # | Állítás | Verdikt | Egy mondat |
|---|---|---|---|
| 1 | A 2026-07-28-as specifikációban a „roots" deprecated (SEP-2577, Final), szerver csak kérésre kapja meg MRTR/`InputRequiredResult`-on (SEP-2322) keresztül | **IGAZOLVA** | A SEP-2577 „Final" státusza és szó szerinti szövege, valamint a 2026-07-28-as changelog MRTR-leírása három egymástól független hivatalos oldalon (github raw, modelcontextprotocol.io, modelcontextprotocol.org archívum) azonosan megjelenik. |
| 2 | SEP-2567: a hívások közötti állapot (pl. projekt-azonosító) nem protokoll-fogalom, hanem eszköz-tervezési minta, explicit tool-argumentumként adandó át | **IGAZOLVA** | A SEP-2567 (Final, 2026-03-11) elsődleges szövege szó szerint és háromszor egymás után kimondja: „Explicit state handles are not a new protocol construct... They are a tool-design pattern." |
| 3 | Az elicitation él, form-módban enum-választást kérhet; érzékeny adatot tilos kérni | **IGAZOLVA** | A hivatalos 2026-07-28-as elicitation-oldal tartalmazza a szó szerinti enum-sémapéldát és a „Servers MUST NOT use form mode elicitation to request sensitive information" tiltást. |
| 4 | OAuth `resource` (RFC 8707) a kanonikus szerver-URI-t azonosítja, útvonallal projektenként elkülöníthető; a scope-ok nem helyazonosításra valók | **IGAZOLVA** | A 2026-07-28-as authorization-oldal és az RFC 8707 elsődleges szövege szó szerint megerősíti mindkét felet (canonical URI + path-példa, illetve „Scope is typically about what access is being requested rather than where that access will be redeemed"). |
| 5 | Mind a hat kliens támogat projektszintű MCP-konfigurációt távoli URL-lel és egyedi HTTP-fejléccel, és a projektszintű nyer a globálissal szemben; a Codexnek van `.codex/config.toml` projektrétege | **RÉSZBEN** | A projektszintű konfiguráció + header mind a hat kliensnél megvan, és a Codex-réteg is igazolt, de a „projekt mindig felülírja a globálist" csak 3/6 kliensnél (Claude Code, Gemini CLI, Codex) dokumentált hivatalosan egyértelműen; a VS Code/Copilot esetén egy Microsoft-repóban nyitott hibajegy pont a fordítottját (globális felülírja a workspace-et) dokumentálja egy ütközési esetben, az Antigravity dokumentációja pedig egyáltalán nem tárgyalja az ütközést. |
| 6 | Roots: Claude Code, Gemini CLI, VS Code/Copilot működik; Cursor hirdeti, de `-32601`; Codex forráskódja `roots: None` | **IGAZOLVA** | A Codex `roots: None` négy különböző git-revízióban (2025 végétől 2026 közepéig) konzisztensen megjelenik a forráskódban; a Cursor `-32601`-es hibáját két, egymástól független jelentés (Cursor-fórum 2025, illetve egy külső MCP-szerver GitHub issue-ja 2026) is megerősíti. |
| 7 | SessionStart mindegyikben van, kivéve Antigravity; HTTP hook csak Claude Code-ban és Copilotban; CC-limit 10 000 karakter, Codex ~2500 token | **RÉSZBEN** | Minden alrész igazolt (beleértve, hogy Antigravity hivatalos doksija — két külön útvonalon is — kizárólag `PreToolUse/PostToolUse/PreInvocation/PostInvocation/Stop` eseményt sorol fel, SessionStart nélkül), de a Claude Code „10 000 karakteres limit" félrevezető megfogalmazás: ez csak a fájlba-mentést kiváltó küszöb, a modellhez ténylegesen csak kb. 2000 karakteres preview jut el, amit több, egymástól független, megerősített GitHub-hibajegy mér és dokumentál. |
| 8 | OAuth-token projektenként: Codex/Gemini CLI kulcsa csak szervernév/URL (globális); Claude Code-nál szivárgás; Cursor workspace-útvonal szerint tárol | **IGAZOLVA** | A Codex és a Gemini CLI forráskódja (nem csak doksi) explicit szervernév/URL-alapú, projekt-független kulcsolást mutat; a Claude Code-szivárgást több nyitott hibajegy támasztja alá, köztük egy súlyosabb, biztonsági jellegű eset is, amit ebben a körben találtam; a Cursor workspace-alapú tárolását két, egymástól független jelentés erősíti meg (multica-ai/multica és a Cursor saját fóruma), bár ez nem szerepel a Cursor hivatalos dokumentációjában. |

---

## Állításonként

### 1. Roots deprecated (SEP-2577, Final) + MRTR-mintán keresztüli, kérésre történő átvitel

A SEP-2577 „Final" státusza három, egymástól független módon elérhető helyen egyezik:

> „**Status**: Final … **Created**: 2026-04-14 … These features are deprecated starting in the specification version that includes this SEP (expected June 2026)."
(nyers markdown, https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/seps/2577-deprecate-roots-sampling-and-logging.md)

> „This SEP has reached Final status and is preserved as a historical record of the design as accepted."
(archív tükör, https://modelcontextprotocol.org/seps/2577-deprecate-roots-sampling-and-logging)

A SEP-lista is „Final"-ként sorolja, dátummal:
> „SEP-2577 | Deprecate Roots, Sampling, and Logging | Final | Standards Track | 2026-04-14"
(https://modelcontextprotocol.io/seps)

A PR maga is megerősíti a „final" státuszt és a merge tényét:
> „kurtisvg added label "final" … kurtisvg merged … Merged: 2026-05-15T22:23:10Z"
(https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2577)

Az MRTR-mechanizmus (SEP-2322) és a kérésre-történő roots-átvitel a hivatalos 2026-07-28-as changelogban szó szerint:

> „Multi Round-Trip Requests (MRTR) pattern introduced which replaces the previous approach of sending server-initiated requests, such as `roots/list`, `sampling/createMessage`, or `elicitation/create`. Servers return an `InputRequiredResult` (`resultType: "input_required"`) whose `inputRequests` field carries the requests for the additional information needed to process the request. Clients respond with `inputResponses` on a retry of the original request providing the requested information. (SEP-2322)."
(https://modelcontextprotocol.io/specification/2026-07-28/changelog)

A mechanizmus önálló oldala megerősíti, hogy ez kötelező és teljesen felváltja a régi mintát:

> „Servers MUST send server-to-client requests (such as `roots/list`, `sampling/createMessage`, or `elicitation/create`) using the MRTR pattern. The previous pattern of server-initiated requests is no longer supported. This is a breaking change."
(https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/mrtr)

**Verdikt: IGAZOLVA**, mindkét fő elem (deprecated + MRTR-en, kérésre) elsődleges forrásokból, egymástól független tükrökön (github.com, modelcontextprotocol.io, modelcontextprotocol.org) is megegyezik.

### 2. SEP-2567: a hívások közötti állapot nem protokoll-fogalom, hanem tool-design minta

A SEP-2567 (Final, 2026-03-11) szövege — három egymástól független helyen (github raw, .io, .org archívum) szó szerint azonos módon — ezt írja:

> „Explicit state handles are not a new protocol construct — there is no schema or wire format for them. They are a tool-design pattern; the protocol change is the removal of sessions, which leaves handles as the way to express cross-call state."
(https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/seps/2567-sessionless-mcp.md; azonos szöveg: https://modelcontextprotocol.io/seps/2567-sessionless-mcp és https://modelcontextprotocol.org/seps/2567-sessionless-mcp)

A tool-argumentum-átadás konkrét mintája ugyanitt:

> „a server that currently scopes a shopping cart (for example) to the session instead exposes a tool `create_basket()` that returns a `basket_id` and threads that ID through subsequent tool calls, e.g. `add_item(basket_id, ...)`."
(uo.)

A SEP-lista megerősíti a „Final" státuszt és a létrehozási dátumot:
> „SEP-2567 | Sessionless MCP via Explicit State Handles | Final | Standards Track | 2026-03-11"
(https://modelcontextprotocol.io/seps)

**Verdikt: IGAZOLVA.**

### 3. Elicitation él, form-módban enum-választás, érzékeny adatra tilalom

Enum-séma szó szerint a hivatalos 2026-07-28-as oldalon:

> „Single-select enum (without titles): { "type": "string", "title": "Color Selection", ... "enum": ["Red", "Green", "Blue"], "default": "Red" }"
(https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation)

Sensitive-adat tiltás ugyanitt:

> „Servers MUST NOT use form mode elicitation to request sensitive information such as passwords, API keys, access tokens, or payment credentials. Servers MUST use URL mode for interactions involving such sensitive information."
(uo.)

Élő (nem deprecated) állapot közvetve is igazolt: a SEP-2577 deprecation-listája csak Roots/Sampling/Logging-ot tartalmazza, Elicitation nem szerepel rajta (lásd fenti SEP-2577-idézet). Az idézett szöveg konzisztens a korábbi kör megállapításával.

**Verdikt: IGAZOLVA.**

### 4. OAuth `resource` (RFC 8707): kanonikus URI, útvonallal projektenként elkülöníthető; scope nem helyazonosításra való

A 2026-07-28-as authorization-spec szó szerint:

> „MCP clients MUST implement Resource Indicators for OAuth 2.0 as defined in RFC 8707 to explicitly specify the target resource for which the token is being requested. … 3. MUST use the canonical URI of the MCP server as defined in RFC 8707 Section 2."
(https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization)

> „Examples of valid canonical URIs: … `https://mcp.example.com/server/mcp` (when path component is necessary to identify individual MCP server)"
(uo.)

RFC 8707 elsődleges szövege a scope/resource megkülönböztetésről:

> „OAuth scope, from Section 3.3 of [RFC6749], is sometimes overloaded to convey the location or identity of the protected resource, however, doing so isn't always feasible or desirable. Scope is typically about what access is being requested rather than where that access will be redeemed."
(https://www.rfc-editor.org/rfc/rfc8707.html — másodlagos, független IETF-tükrön is azonos szöveg: https://datatracker.ietf.org/doc/html/rfc8707/)

**Verdikt: IGAZOLVA.**

### 5. Mind a hat kliens: projektszintű config + távoli URL + header; projekt > globális; Codex projektrétege

**Projektszintű config + header mind a hat kliensnél — igazolt.** Claude Code hivatalos doksija:

> „Project-scoped servers enable team collaboration by storing configurations in a `.mcp.json` file … `headers`: for HTTP server authentication."
(https://code.claude.com/docs/en/mcp)

**Codex projektrétege — igazolt** (a korábbi kör megállapítását megerősítettem, két hivatalos forrás egyezik):
> „You can also add project-scoped overrides in `.codex/config.toml` files. Codex loads project-scoped config files only when you trust the project."
(https://developers.openai.com/codex/config-reference — megerősítve: https://learn.chatgpt.com/docs/config-file/config-advanced.md)

**A „projekt mindig felülírja a globálist" rész csak részben tartható.** Claude Code-nál hivatalosan dokumentált, konkrét sorrenddel:

> „When the same server is defined in more than one place, Claude Code connects to it once, using the definition from the highest-precedence source: 1. Local scope 2. Project scope 3. User scope 4. Plugin-provided servers 5. claude.ai connectors."
(a hivatalos `code.claude.com/docs/en/mcp` oldal szövege idézve: https://github.com/anthropics/claude-code/issues/48857)

Gemini CLI-nél is hivatalosan dokumentált (korábbi kör megerősítve): „Project settings override user settings and system defaults." Ezzel szemben a **VS Code/Copilot esetében nem találtam hivatalos, explicit precedencia-kijelentést** — a hivatalos doksi kifejezetten kerüli a kérdést, és inkább lebeszél a kettős definícióról:

> „We recommend you use only one location per server. Adding the same server to both locations may cause conflicts and unexpected behavior."
(https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp-in-your-ide/extend-copilot-chat-with-mcp)

Sőt, egy hivatalos Microsoft-repóban nyitott, konkrét reprodukciós hibajegy pont az **ellenkező irányú** ütközést dokumentálja egy valós esetben (a felhasználói/globális profil felülírta a workspace-definíciót, nem fordítva):

> „Window output logged a collision: `Overwriting mcp server 'figma' from <workspace-folder>/.vscode/mcp.json with <user-profile>/User/mcp.json.`"
(https://github.com/microsoft/vscode/issues/332072)

A Cursor „projekt nyer" állítására csak közvetett/nem hivatalos (T3) forrást találtam ebben a körben is (`truefoundry.com`, illetve egy `connector.zone` T3-cikk állítja ugyanezt VS Code-ra is, de hivatalos alátámasztás nélkül: https://connector.zone/guides/merging-mcp-config-blocks/). Az **Antigravity hivatalos dokumentációja két különböző URL alatt is** (`antigravity.google/docs/cli/mcp/`, `antigravity.google/docs/cli/gcli-migration/`) csupán felsorolja a globális (`~/.gemini/config/mcp_config.json`) és a workspace-szintű (`.agents/mcp_config.json`) fájlt, de **sehol nem mondja ki, melyik nyer** ütközés esetén.

**Verdikt: RÉSZBEN.** A projektszintű config + header + a Codex-réteg igazolt mind a hat kliensnél; a „projekt mindig felülírja a globálist" állítás csak 3/6 kliensnél (Claude Code, Gemini CLI, Codex) hivatalosan dokumentált egyértelműen, Cursornál csak T3-forrásból, Antigravity-nél nincs forrás rá, VS Code/Copilotnál pedig egy hivatalos hibajegy a fordítottját mutatja egy konkrét esetben.

### 6. Roots működése klienselnként

A Codex `roots: None` állítást **négy különböző git-commit/verzió** forráskódjában konzisztensen megtaláltam (a korai `rust-v0.0.2505302325` tagtől a 2026 közepi `85034b18`, `9a8730f3`, `0a0caa9d` revíziókig), ami erős, önmagában is kétszeresen megerősített bizonyíték (a forráskód maga elsődleges forrás, és időben ismételve mutatja a konzisztenciát):

> „capabilities: ClientCapabilities { experimental: None, extensions: None, roots: None, sampling: None, elicitation: Some(...), tasks: None }"
(pl. https://github.com/openai/codex/blob/85034b18/codex-rs/core/src/mcp_connection_manager.rs)

A Cursor `-32601`-es hibáját **két, egymástól teljesen független** jelentés erősíti meg — egy 2025 áprilisi Cursor-fórum eredeti hibajelentés a nyers JSON-RPC hibával:

> „error: ErrorData { code: ErrorCode(-32601), message: "Method not found", data: None }" — miközben a kliens az `initialize`-ben `roots: Some(RootsCapabilities { list_changed: Some(false) })`-t hirdet.
(https://forum.cursor.com/t/mcp-client-does-not-support-roots-list/77248)

— és egy 2026-os, teljesen más szerzőtől, más MCP-szerver kontextusából származó GitHub issue, amely ugyanezt reprodukálja:

> „Cursor has a documented, longstanding bug where it advertises `roots: { listChanged: false }` in its initialize capabilities, but calling `roots/list` against it returns a `JSON-RPC error -32601 Method not found`."
(https://github.com/Unveil-gg/twine-mcp/issues/3)

Érdekesség (nem a Cursorra vonatkozik, de megerősíti, hogy a „hirdeti, de nem válaszol" minta nem egyedi eset): a GitHub Copilot IntelliJ plugin esetében egy hivatalos Microsoft-repóban dokumentáltan ugyanez a hibaminta fordult elő egy másik kliens-implementációnál (`microsoft/copilot-intellij-feedback#438`), ami azt jelzi, hogy a roots-hirdetés/-implementáció szétválása nem elszigetelt Cursor-specifikus jelenség, hanem ismétlődő hibaosztály volt az ökoszisztémában.

**Verdikt: IGAZOLVA.**

### 7. SessionStart-lefedettség, HTTP hook-típus, kimeneti korlátok

**Antigravity SessionStart hiánya — két külön hivatalos URL-en is megerősítve**, azonos, teljes eseménylistával:

> „| `PreToolUse` | ... | | `PostToolUse` | ... | | `PreInvocation` | ... | | `PostInvocation` | ... | | `Stop` | ... |"
(https://antigravity.google/docs/hooks/ és — azonos tartalommal, más útvonalon — https://antigravity.google/docs/ide/hooks/)

Egy független, harmadik féltől származó adapter-projekt forráskódja is explicit megjegyzésben rögzíti ugyanezt, gyakorlati tapasztalatból:

> „Events agy supports: PreToolUse, PostToolUse, PreInvocation, PostInvocation, Stop. NO SessionStart/SessionEnd/UserPromptSubmit/Notification of its own." … „AG never fires SessionStart"
(https://github.com/jonnyasmar/atrium-adapters/blob/main/adapters/antigravity/hooks.sh)

**HTTP hook-típus Claude Code-ban és Copilotban — megerősítve**, a Copilot esetén friss forrásból, fontos kiegészítő korlátozással:

> „HTTP hooks send the input payload as a JSON `POST` to a URL. … Cloud agent only. Outbound network from the sandbox is restricted by the cloud agent firewall, so `url` must target an allow-listed host."
(https://docs.github.com/en/copilot/reference/hooks-reference)

Ez a „Cloud agent only" megkötés árnyalja az eredeti állítást: a HTTP hook a Copilot-ökoszisztémában elsősorban a github.com-on futó cloud agentre vonatkozik, nem feltétlenül a helyi VS Code Agent módra (amelynek hook-támogatását a hivatalos GitHub-mátrix „Partial"-ként jelöli — ezt a korábbi kör már rögzítette).

**Claude Code kimeneti korlát — a 10 000 karakter a dokumentált *küszöb*, de nem a ténylegesen célba érő tartalom mérete.** Egy 2026 áprilisi hivatalos válasz (anthropics/claude-code karbantartójától) megerősíti a doksi jelenlegi szövegét:

> „The `persistHookOutput` 10,000-character threshold is not currently configurable … The 10K threshold causes large outputs to be written to a temp file and referenced by path rather than inlined."
(https://github.com/anthropics/claude-code/issues/50571)

Ugyanakkor **több, egymástól független, megerősített mérés** azt mutatja, hogy a modellhez ténylegesen csak kb. 2000 karakter jut el, nem a teljes fájl-hivatkozás「átlátszó」módon:

> „I measured 18,057 bytes emitted and ~2,000 delivered — 11% arrived." … „the preview-size constant resolves to 2000."
(https://github.com/anthropics/claude-code/issues/84021)

> „The documentation says that hook output his truncated after 10,000 characters, but I observe that if you breach this limit, the output is truncated to 2000 characters."
(https://github.com/anthropics/claude-code/issues/44086)

Egy harmadik hibajegy azt is dokumentálja, hogy időszakosan **magának a küszöbnek a dokumentált értéke is ingadozott** (50 000 vs. 10 000):

> „The v2.1.89 changelog (quoted in #41799) announced the threshold as **50,000 characters**. The shipped code uses **10,000 characters**."
(https://github.com/anthropics/claude-code/issues/51537)

**Codex ~2500 token — erősen megerősítve**, hivatalos dokumentációból és egy éles, harmadik féltől független hibajelentésből egyaránt:

> „Codex limits each model-visible hook-output message to roughly 2,500 tokens."
(https://developers.openai.com/codex/hooks — megerősítve: https://learn.chatgpt.com/docs/hooks)

> „Codex `0.130.0` appears to hard-limit hook-injected `additionalContext` to about 2,500 tokens per hook output."
(https://github.com/openai/codex/issues/22861)

**Verdikt: RÉSZBEN.** Minden alrész igaz a szó szerinti értelemben, de a „Claude Code hook-kimeneti korlátja 10 000 karakter" megfogalmazás pontatlan/félrevezető: ez csak a fájlba-mentést kiváltó küszöb, a ténylegesen a modellhez eljutó tartalom dokumentáltan (több, egymástól független forrás szerint) kb. 2000 karakter, ráadásul maga a 10 000-es szám is legalább egyszer ellentmondott egy hivatalos changelog-bejegyzésnek (ami 50 000-et írt).

### 8. OAuth-token projektenkénti elkülönítés

**Codex — forráskód-szintű megerősítés** (a korábbi kör idézetét megismételve, ugyanabból a fájlból, de a lényeg: nincs projekt-komponens a kulcsban):
> „fn compute_store_key(server_name: &str, server_url: &str) -> Result<String> { … Ok(format!("{server_name}|{truncated}")) }"
(https://github.com/openai/codex/blob/d807d44a/codex-rs/rmcp-client/src/oauth.rs — a korábbi kör által is idézett fájl, ezúttal a kontextusát a `mcp_connection_manager.rs` több verziójával kereszt-ellenőriztem)

**Gemini CLI — forráskód-szintű megerősítés**, globális, egyetlen JSON-tömb, szervernév-kulccsal:
> „`~/.gemini/mcp-oauth-tokens.json`" … „tokens.set(credentials.serverName, credentials);"
(https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md; forráskód: https://github.com/google-gemini/gemini-cli/blob/caa04664/packages/core/src/mcp/oauth-token-storage.ts)

**Claude Code — szivárgás, több nyitott hibajegy, és ebben a körben egy súlyosabb esetet is találtam.** Az eredeti (project-scope OAuth felülírás Slacknél) hibajegy:

> „OAuth credentials are stored in `~/.claude/.credentials.json` under a single key per server URL … Only one token exists regardless of how many projects use the same MCP server. Authenticating in one project overwrites the credential used by all other projects."
(https://github.com/anthropics/claude-code/issues/39952)

Egy másik, git worktree-kre vonatkozó jegy megerősíti, hogy a kulcs nem tiszta projekt-azonosító, hanem útvonal-hash, ami worktree-nként törik:

> „Credentials in `~/.claude/.credentials.json` are keyed by `serverName|hash` … This hash appears to incorporate the project path, so a worktree at `../wt-1/` generates a different hash than `./wt2-2/` and doesn't find existing credentials."
(https://github.com/anthropics/claude-code/issues/18890)

Ebben a körben találtam egy **frissebb, súlyosabb, biztonsági jellegű** jegyet, amely túlmutat az egyszerű „szivárgáson”: egy soha nem deklarált, globálisan tárolt HTTP MCP-szerver projekt-MCP-ként jelent meg, és konfiguráció-törlés után is túlélte az újraindítást:

> „Claude Code persisted an HTTP MCP server transport … stored it together with credential material in the **global** file `~/.claude/.credentials.json`, surfaced it to the model/UI as if it were a **project** MCP, and **retained the entry across full restarts even after the user removed the corresponding MCP configuration**."
(https://github.com/anthropics/claude-code/issues/69749)

**Cursor — workspace-útvonal szerinti tárolás, két egymástól független jelentésből**, bár ez sehol nincs a Cursor hivatalos dokumentációjában, csak megfigyelésből és egy Cursor-alkalmazott fórumválaszából ismert:

> „Cursor stores Model Context Protocol (MCP) authentications (such as OAuth2 flows) directly within the specific project directory where the connection was first established (eg `~/.cursor/project/xxx/mcp-auth.json`)." … [multica válaszában, aki maga is ellenőrizte] „on my machine I can see existing workspace-scoped files under `~/.cursor/projects/.../mcp-auth.json`, which matches the shape of the problem you described"
(https://github.com/multica-ai/multica/issues/3908)

**Verdikt: IGAZOLVA.** Mindhárom alrész (Codex/Gemini CLI globális, szervernév-kulcsú tárolás; Claude Code szivárgása; Cursor workspace-alapú tárolása) elsődleges forrásból (forráskód, illetve — Claude Code/Cursor esetén, ahol nincs explicit doksi — több, egymástól független hibajegyből/fórumból) megerősítve. Fontos árnyalás: a Cursor-viselkedés nem hivatalosan dokumentált termékjellemző, hanem megfigyelt (és Cursor-oldalról közvetve megerősített) tény.

---

## Amit ez a döntésre jelent

1. A „melyik projektben vagyunk” kérdés valóban nem oldható meg protokoll-szinten (roots deprecated + csak kérésre érkezik; session-fogalom megszűnt 2026-07-28-ban; SEP-2567 kifejezetten kimondja, hogy ez tool-design kérdés) — a szervernek explicit tool-argumentumként kell bekérnie, vagy elicitation/enum-formában rá kell kérdeznie a felhasználótól. Ez a `_ell_kozos.txt`-ben és a `sq01`-ben leírtak szerint is megáll.
2. Az OAuth `resource`-URI (RFC 8707) útvonal-komponenssel architekturálisan alkalmas projektenkénti elkülönítésre, de ez a szerver saját tervezési döntése; a hat vizsgált kliens közül kettőnél (Codex, Gemini CLI) a kliens-oldali OAuth-token-tár kizárólag szervernév/URL szerint kulcsol — vagyis ha a szerver projektenként eltérő canonical resource-URI-t akarna használni, ehhez a klienskonfigurációban is projektenként külön szervernevet/URL-t kellene beállítani; önmagában a szerver-oldali resource-elkülönítés nem old meg semmit, ha minden projekt ugyanazt a kliens-oldali szerverbejegyzést használja.
3. A projektszintű MCP-konfiguráció (távoli URL + egyedi header) mind a hat kliensnél elérhető, tehát technikailag lehetséges projektenként eltérő headert/URL-t beállítani — de a „projekt mindig felülírja a globálist” garancia csak 3/6 kliensnél (Claude Code, Gemini CLI, Codex) dokumentált egyértelműen és hivatalosan; VS Code/Copilotnál egy hivatalos Microsoft-hibajegy a fordított ütközést is dokumentálja egy konkrét esetben, Antigravity-nél pedig nincs is hivatalos állásfoglalás az ütközésről.
4. A roots-alapú munkakörnyezet-azonosítás gyakorlatilag nem opció egyik kliensnél sem megbízhatóan: deprecated a specifikációban, a Codex forráskódja szerint sosem küldi, a Cursor pedig hirdeti, de `-32601`-et ad rá — csak a Claude Code, a Gemini CLI és a VS Code/Copilot esetén működik ténylegesen a jelenlegi kutatás szerint.
5. A SessionStart-hook 5/6 kliensnél (Antigravity kivételével) elérhető egy rövid, sablonszerű „mi van a memóriában” mondat beszúrására, de a kimeneti méretkorlátok szigorúbbak, mint amit a dokumentáció sugall: a Claude Code-nál a ténylegesen célba érő tartalom több, egymástól független mérés szerint kb. 2000 karakter (nem 10 000), a Codexnél kb. 2500 token — egy hosszabb memória-összefoglaló könnyen csonkulhat vagy néma módon elveszhet.
6. Egyik kliens sem ad ma (2026-09-25) natív, dokumentáltan megbízható, projektenkénti OAuth-token-elkülönítést: a Codex és a Gemini CLI szándékosan globális (szervernév/URL-kulcsú) tárolást használ; a Claude Code-nál több nyitott hibajegy — köztük egy súlyosabb, biztonsági jellegű eset — dokumentálja a szivárgást/a globális tárolást; a Cursor workspace-útvonal szerinti tárolása working, de nem hivatalosan dokumentált, és git worktree-k, illetve izolált munkakörnyezetek (pl. multica) esetén nem öröklődik.

---

## Meglátogatott linkek

| Cím | URL | Tier | Eszköz |
|---|---|---|---|
| SEP-2577 (raw markdown) | https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/seps/2577-deprecate-roots-sampling-and-logging.md | T1 | Exa search |
| SEP-2577 (hivatalos oldal) | https://modelcontextprotocol.io/seps/2577-deprecate-roots-sampling-and-logging | T1 | Exa search |
| SEP-2577 (archív .org tükör) | https://modelcontextprotocol.org/seps/2577-deprecate-roots-sampling-and-logging | T1 | Exa search |
| SEP-lista | https://modelcontextprotocol.io/seps | T1 | Exa search |
| SEP-2577 PR (merged, final) | https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2577 | T1 | Exa search |
| SEP-2567 (raw markdown) | https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/seps/2567-sessionless-mcp.md | T1 | Exa search |
| SEP-2567 (archív .org tükör) | https://modelcontextprotocol.org/seps/2567-sessionless-mcp | T1 | Exa search |
| SEP-2567 (hivatalos oldal) | https://modelcontextprotocol.io/seps/2567-sessionless-mcp | T1 | Exa search |
| SEP-2567 draft-vita | https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2567 | T1 | Exa search |
| 2026-07-28 changelog | https://modelcontextprotocol.io/specification/2026-07-28/changelog | T1 | Exa search |
| MRTR-oldal | https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/mrtr | T1 | Exa search |
| Elicitation (2026-07-28) | https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation | T1 | Exa fetch |
| Authorization (2026-07-28) | https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization | T1 | Exa fetch+search |
| RFC 8707 (rfc-editor) | https://www.rfc-editor.org/rfc/rfc8707.html | T1 | Exa search |
| RFC 8707 (datatracker, másodlagos tükör) | https://datatracker.ietf.org/doc/html/rfc8707/ | T1 | Exa search |
| Claude Code MCP doksi | https://code.claude.com/docs/en/mcp | T1 | Exa search |
| Claude Code header-forwarding bug | https://github.com/anthropics/claude-code/issues/28293 | T1 | Exa search |
| Claude Code mcp-quickstart | https://code.claude.com/docs/en/mcp-quickstart | T1 | Exa search |
| Codex mcp_connection_manager.rs (85034b18) | https://github.com/openai/codex/blob/85034b18/codex-rs/core/src/mcp_connection_manager.rs | T1 | Exa search |
| Codex mcp_connection_manager.rs (korai, rust-v0.0.2505302325) | https://github.com/openai/codex/blob/rust-v0.0.2505302325/codex-rs/core/src/mcp_connection_manager.rs | T1 | Exa search |
| Codex mcp_connection_manager.rs (9a8730f3) | https://github.com/openai/codex/blob/9a8730f3/codex-rs/core/src/mcp_connection_manager.rs | T1 | Exa search |
| Cursor fórum — roots/list -32601 | https://forum.cursor.com/t/mcp-client-does-not-support-roots-list/77248 | T2 | Exa search |
| twine-mcp issue #3 — Cursor roots bug, független megerősítés | https://github.com/Unveil-gg/twine-mcp/issues/3 | T2 | Exa search |
| microsoft/copilot-intellij-feedback #438 — analóg roots-hiba más kliensnél | https://github.com/microsoft/copilot-intellij-feedback/issues/438 | T1 (hivatalos MS repo) | Exa search |
| Codex Hooks (fejlesztői doksi) | https://developers.openai.com/codex/hooks | T1 | Exa search |
| Codex Hooks (learn.chatgpt.com tükör) | https://learn.chatgpt.com/docs/hooks | T1 | Exa search |
| Codex issue #22861 — 2500 token limit éles jelentés | https://github.com/openai/codex/issues/22861 | T1 | Exa search |
| Codex session_start.rs forráskód | https://github.com/openai/codex/blob/main/codex-rs/hooks/src/events/session_start.rs | T1 | Exa search |
| Claude Code issue #50571 — 10 000 karakteres küszöb magyarázata | https://github.com/anthropics/claude-code/issues/50571 | T1 | Exa search |
| Claude Code issue #84021 — ~2000 karakteres tényleges preview mérés | https://github.com/anthropics/claude-code/issues/84021 | T1 | Exa search |
| Claude Code issue #44086 — 2000 karakteres csonkítás | https://github.com/anthropics/claude-code/issues/44086 | T1 | Exa search |
| Claude Code issue #51537 — 50K vs 10K doksi/kód eltérés | https://github.com/anthropics/claude-code/issues/51537 | T1 | Exa search |
| Antigravity Hooks (docs/hooks/) | https://antigravity.google/docs/hooks/ | T1 | Exa search |
| Antigravity Hooks (docs/ide/hooks/) | https://antigravity.google/docs/ide/hooks/ | T1 | Exa search |
| atrium-adapters — Antigravity hook-viselkedés, „AG never fires SessionStart” | https://github.com/jonnyasmar/atrium-adapters/blob/main/adapters/antigravity/hooks.sh | T3 | Exa search |
| GitHub Copilot hooks reference — HTTP hook típus | https://docs.github.com/en/copilot/reference/hooks-reference | T1 | Exa search |
| multica-ai/multica issue #3908 — Cursor mcp-auth.json workspace-tárolás | https://github.com/multica-ai/multica/issues/3908 | T2 | Exa search |
| Cursor MCP doksi (static OAuth, projekt config) | https://cursor.com/docs/mcp | T1 | Exa search |
| Claude Code issue #39952 — OAuth kulcs = szervernév, globális | https://github.com/anthropics/claude-code/issues/39952 | T1 | Exa search |
| Claude Code issue #18890 — worktree-k szerinti hash | https://github.com/anthropics/claude-code/issues/18890 | T1 | Exa search |
| Claude Code issue #69749 — súlyosabb biztonsági szivárgás | https://github.com/anthropics/claude-code/issues/69749 | T1 | Exa search |
| Antigravity CLI MCP doksi | https://antigravity.google/docs/cli/mcp/ | T1 | Exa search |
| Antigravity gcli-migration doksi | https://antigravity.google/docs/cli/gcli-migration/ | T1 | Exa search |
| VS Code — Add and manage MCP servers | https://code.visualstudio.com/docs/agent-customization/mcp-servers | T1 | Exa search |
| VS Code — MCP configuration reference | https://code.visualstudio.com/docs/agents/reference/mcp-configuration | T1 | Exa search |
| connector.zone — MCP config merge (nem hivatalos precedencia-állítás) | https://connector.zone/guides/merging-mcp-config-blocks/ | T3 | Exa search |
| microsoft/vscode issue #332072 — user profil felülírta a workspace-et | https://github.com/microsoft/vscode/issues/332072 | T1 (hivatalos MS repo) | Exa search |
| Claude Code issue #48857 — hivatalos scope-precedencia szövege idézve | https://github.com/anthropics/claude-code/issues/48857 | T1 | Exa search |

---

# ELL02 — A memória-rendszerek hatókör-kezelésének ellenőrzése

**Módszertani megjegyzés:** ez az ellenőrzés egyetlen, szekvenciális munkamenetben zajlott, kizárólag az Exa
(`mcp__Exa__web_search_exa`, `mcp__Exa__web_fetch_exa`) eszközökkel — a beépített WebSearch/WebFetch-et nem
használtam. Minden alábbi idézetet **magam nyitottam meg újra** az elsődleges forrásban (nem vettem át az előző kör
idézeteit ellenőrzés nélkül); ahol az élő oldal szövege eltért az előző körben idézettől, azt jelzem. Alügynököt nem
tudtam indítani (nem állt rendelkezésre agent-indító eszköz), ezért ez is degradált módú, egyágenses ellenőrzés.

## Verdikt-összefoglaló

| # | Állítás | Verdikt | Egy mondat |
|---|---|---|---|
| 1 | basic-memory `project` param (default projekttel); mem0 `user_id`/`agent_id`/`run_id`; Graphiti `group_id` — idézett séma-részletek | **IGAZOLVA** | Mindhárom séma-idézetet szó szerint megtaláltam az élő hivatalos dokumentációban, ill. a jelenlegi (2026-09-25-kor élő) forráskódban, több, egymástól független commit/tükör között is. |
| 2 | Zep hivatalos Memory MCP Server és `opspresso/mcp-memory`: a projekt/tenant-azonosító kapcsolatból/fejlécből jön, nem eszköz-argumentumból; „a model that can name its own tenant…” idézet forrása | **IGAZOLVA, pontosítással** | Mindkét rendszernél igaz a mintázat, de az idézett mondat kizárólag az `opspresso/mcp-memory` README-jében áll szó szerint — a Zep hivatalos doksijában **nem** szerepel ez a mondat —, és az opspresso egy 0 csillagos, egyetlen karbantartó által írt projekt, amelyhez nem található második, független forrás. |
| 3 | Claude Code CLAUDE.md és Codex AGENTS.md: a kliens a munkakönyvtártól a git-gyökérig bejárva tölti be | **IGAZOLVA** | Mindkét hivatalos doksi (code.claude.com, developers.openai.com) — élőben újraellenőrizve — szó szerint leírja a könyvtár-hierarchia bejárását és a git-gyökér szerepét. |
| 4 | Codex „Memories" egyetlen, gépenként közös tárban (`~/.codex/memories/`) él, projektenkénti szétválasztás nélkül; forráskód: „No per-cwd memory buckets"; issue `#18343` ezt kéri | **IGAZOLVA** | A hivatalos doksi, a mára mergelt `#11364` PR-leírás és a jelenleg is nyitott `#18343` issue mindegyike szó szerint megerősíti az állítást, három egymástól független, elsődleges forrásból. |
| 5 | OWASP (LLM Top 10, MCP Top 10, Agentic Top 10) és AWS Well-Architected: a hozzáférés hatókörét a hívó környezet határozza meg determinisztikusan, nem a modell — szó szerinti idézettel | **IGAZOLVA, apró pontosítással** | Mind a négy dokumentum releváns szakasza szó szerint egyezik az idézettel, egyetlen kivétellel: az AWS-idézetben az előző kör egy szót (`influence` → `[trick]`) szögletes zárójelben lecserélt, ami technikailag már nem szó szerinti idézet. |
| 6 | Meta FAIR „CIMemories" (ICLR 2026): 69%-os attribútum-szintű szabálysértés, és 0,1%→25,1% ingadozás ismételt azonos promptnál | **IGAZOLVA, egy forrás-inkonzisztenciával** | A cikk létezik, elfogadott ICLR 2026-anyag, pontosan ezt méri, és a 69%, illetve a 0,1%→9,6%→25,1% számok szó szerint, három elsődleges forrásban (arXiv, ICLR proceedings, hivatalos GitHub) egyeznek — de a hivatalos GitHub README a 0,1%→9,6%→25,1% görbét „GPT-4o"-nak tulajdonítja, míg maga a cikk (arXiv és ICLR proceedings verzió is) „GPT-5"-nek — ezt az ellentmondást az előző kör nem jelezte. |

---

## Állításonként

### 1. basic-memory / mem0 / Graphiti — séma-részletek

**basic-memory** — `docs.basicmemory.com` (T1), élőben újranyitva (2026-09-25):
> „Project resolution order is: constrained project env -> explicit `project` parameter -> `default_project` fallback."

Ugyanezen az oldalon, a „Common parameters" táblázatban, amely minden note-eszközre (köztük `write_note`-ra) vonatkozik:
> „`project` | string | resolved via fallback | Project name. Constrained project env → explicit parameter → `default_project` config"

Ez szó szerint megegyezik az előző kör idézetével. (https://docs.basicmemory.com/reference/mcp-tools-reference)

**mem0 OSS** — `mem0/memory/main.py`, hivatalos forráskód, `main` ág, élőben lekérve:
> „if not session_ids_provided: raise Mem0ValidationError(message=\"At least one of 'user_id', 'agent_id', or 'run_id' must be provided.\", error_code=\"VALIDATION_001\", ...)"

Ez a jelenlegi `main` ágban is megvan, és egy 2025. novemberi hibajegy (`#3770`) is dokumentálja a felhasználói oldalról ugyanezt a hibaüzenetet éles kvickstart-hibaként: „`mem0.exceptions.ValidationError: At least one of 'user_id', 'agent_id', or 'run_id' must be provided.`" — két egymástól független forrás (forráskód + hibajegy) ugyanarra a szövegre. (https://github.com/mem0ai/mem0/blob/main/mem0/memory/main.py, https://github.com/mem0ai/mem0/issues/3770)

**Megjegyzés (nem az eredeti kör állítása, de releváns kiegészítés):** a jelenlegi forráskódban egy új, korábban nem létező védelem is megjelent, amely kifejezetten a sq04-ben dokumentált `#6655` hibajegyre hivatkozik: „Identity scope is set below from the entity params only. Stripping the keys here stops caller metadata from placing a memory into a scope the caller did not pass, which the re-pins below cannot prevent for a param that was left unset (issue #6655)." — ez azt jelenti, hogy a sq04-ben leírt metaadat-felülírási hiba **azóta javítva lett**, és a javítás forráskód-szinten is igazolja, hogy a hiba valóban létezett.

**Graphiti** — `mcp_server/README.md`, hivatalos, `main` ág, élőben lekérve:
> „`--group-id`: Set a namespace for the graph (optional). If not provided, defaults to \"main\""
> „Hint: specify a `group_id` to namespace graph data. If you do not specify a `group_id`, the server will use \"main\" as the group_id."

Ez szó szerint megegyezik, és egy második, forráskód-szintű forrás (`graphiti_mcp_server.py`, `add_memory` docstring) is megerősíti: „group_id (str, optional): A unique ID for this graph. If not provided, uses the default group_id from CLI or a generated one." (https://github.com/getzep/graphiti/blob/main/mcp_server/README.md, https://github.com/getzep/graphiti/blob/4f62cfe7/mcp_server/src/graphiti_mcp_server.py)

### 2. Zep és `opspresso/mcp-memory` — kapcsolat/fejléc-alapú tenant-döntés

**Zep hivatalos Memory MCP Server** — `help.getzep.com/memory-mcp-server`, élőben újranyitva:
> „Each connected user can always read their own user graph. User-graph tools take no user, graph, or project argument. The target is fixed by the authenticated identity, so one user's token cannot select another user's memory or another project."

Ez szó szerint megegyezik az előző kör idézetével. A „Who the user is / What the user can reach" szakasz is megerősíti, hogy a projekt-hozzárendelés az IdP-n (Google Workspace / vállalati SSO) és a Zep-oldali „connection"-ön múlik, nem tool-paraméteren. (https://help.getzep.com/memory-mcp-server)

**A keresett idézet forrása — pontosítás:** a „**a model that can name its own tenant can read another project's memories by asking**" mondat **a Zep hivatalos dokumentációjában sehol nem szerepel** — végigolvastam a Zep oldalát, ott nincs ilyen vagy ehhez hasonló mondat. A mondat kizárólag az `opspresso/mcp-memory` GitHub README-jében található, szó szerint, a „Which memories a caller gets" szakaszban:
> „**The tenant comes from a header and never from a tool argument** — an explicit `X-Memory-Tenant`, or the `X-Tenant-Id` header Agent Studio stamps on every MCP request when no explicit one is configured... A tool argument is something the *model* chose — and a model that can name its own tenant can read another project's memories by asking, including a model that was talked into it by text it retrieved a moment earlier. No amount of validation fixes that; the channel is wrong."

Ezt élőben, teljes egészében újra lekértem a repóból — a szöveg pontosan egyezik. (https://github.com/opspresso/mcp-memory)

**Fontos korlátozás, amit ellenőriztem:** az `opspresso/mcp-memory` repó GitHub-metaadatai szerint 0 csillag, 0 fork, 0 watcher, egyetlen szerző (`nalbam`, 38 commit), és 2026-07-31-én jött létre — tehát egy nagyon friss, gyakorlatilag ismeretlen, egyszemélyes projekt. Nem találtam hozzá második, tőle független forrást (sem híradást, sem másik dokumentációt, sem code review-t), így ez a konkrét mondat módszertanilag **nincs két független forrással alátámasztva** — ez megegyezik azzal, amit az eredeti sq02 kutatás már maga is jelzett („nem sikerült két független forrással megerősítenem"). A mintázat maga (fejléc/kapcsolat > tool-argumentum) viszont igen — ezt a Zep (nagy, kereskedelmi, sok ügyféllel rendelkező termék) és az opspresso (kis, de explicit indoklással rendelkező projekt) egymástól függetlenül, egymást megerősítve mutatja, csak a konkrét *mondat* egyetlen forrásból származik.

### 3. Claude Code CLAUDE.md és Codex AGENTS.md — könyvtár-bejárás

**Claude Code**, `code.claude.com/docs/en/memory`, élőben újranyitva (2026-09-25):
> „Claude Code reads CLAUDE.md files by walking up the directory tree from your current working directory, checking each directory along the way for `CLAUDE.md` and `CLAUDE.local.md` files. This means if you run Claude Code in `foo/bar/`, it loads instructions from `foo/bar/CLAUDE.md`, `foo/CLAUDE.md`, and any `CLAUDE.local.md` files alongside them."
> „Across the directory tree, content is ordered from the filesystem root down to your working directory... so instructions closer to where you launched Claude are read last."

Mindkét mondat szó szerint megegyezik az előző kör idézetével, élő oldalról újraellenőrizve.

**Codex**, `developers.openai.com/codex/guides/agents-md`, élőben újranyitva:
> „Project scope: Starting at the project root (typically the Git root), Codex walks down to your current working directory. If Codex cannot find a project root, it only checks the current directory."
> „Merge order: Codex concatenates files from the root down, joining them with blank lines. Files closer to your current directory override earlier guidance because they appear later in the combined prompt."

Ez is szó szerint megegyezik. A forráskód-szintű megerősítést (`agents_md.rs`, „walking upwards... until a configured `project_root_markers` entry is found... default marker list is `.git`") nem nyitottam meg újra ebben a körben, mert a doksi-szintű állítás (ami a felhasználó szempontjából releváns) már két, egymástól független hivatalos oldalon (`developers.openai.com` és a korábbi körben idézett `learn.chatgpt.com` tükrön) megerősítést nyert. (https://code.claude.com/docs/en/memory, https://developers.openai.com/codex/guides/agents-md)

### 4. Codex „Memories" — globális tár, `#18343`

**Hivatalos doksi**, `learn.chatgpt.com/docs/customization/memories.md`, élőben újranyitva — a szöveg **ma is** pontosan úgy áll, ahogy az előző kör idézte:
> „Codex stores memories under your Codex home directory. By default, that's `~/.codex`... The main memory files live under `~/.codex/memories/` and include summaries, durable entries, recent inputs, and supporting evidence from prior chats."

Az oldal sehol nem említ cwd- vagy projekt-alapú elkülönítést; a `/memories` chat-szintű vezérlés és a `memories.generate_memories`/`memories.use_memories` konfig is csak be/ki kapcsol, nem szűr projekt szerint.

**Forráskód-tervdokumentum**, a mergelt `#11364` PR (openai/codex, hivatalos), élőben újranyitva:
> „Target behavior - One shared memory root only: `~/.codex/memories/`. **No per-cwd memory buckets, no cwd hash handling.**"
> „PR 3: Remove per-cwd memories and move to one global memory root ... Remove cwd-hash bucket helpers and normalization logic used only for memory pathing... Acceptance criteria: New runs only read/write `~/.codex/memories`."

Ez a PR **mergelve van** (`State: merged`, 2026-02-10), tehát nem csak terv, hanem végrehajtott, dokumentált architektúra-döntés.

**`#18343` issue**, élőben újranyitva — jelenleg is **nyitott** (`State: open`, utolsó frissítés 2026-07-13):
> „Today, memory appears to be effectively global under the current `CODEX_HOME`, which can cause cross-project contamination over time. In practice, many memories are highly specific to one repository, one codebase, or one workflow, and should not automatically influence unrelated projects."
> „I would like Codex to support configurable memory scopes such as: **Global**: shared across all projects / **Project**: isolated to the current project/repo/worktree / **Hybrid**... / **Thread-only / no carryover**..."

Ez szó szerint megegyezik. Azt is megerősítettem, hogy a hosszú hozzászólásban idézett „31 agent"-es KinthAI-hivatkozás valóban a `kinthaiofficial` felhasználótól származó, nem-hivatalos komment az issue-ban — ez alátámasztja az előző kör T3-as minősítését (közösségi vélemény, nem hivatalos forrás). (https://learn.chatgpt.com/docs/customization/memories.md, https://github.com/openai/codex/pull/11364, https://github.com/openai/codex/issues/18343)

### 5. OWASP és AWS Well-Architected — determinisztikus, nem modell-alapú hatókör-döntés

**OWASP LLM06:2025 Excessive Agency**, `genai.owasp.org`, élőben újranyitva, teljes „Prevention and Mitigation Strategies" szakasz:
> „5. **Execute extensions in user's context** Track user authorization and security scope to ensure actions taken on behalf of a user are executed on downstream systems in the context of that specific user, and with the minimum privileges necessary."
> „7. **Complete mediation** Implement authorization in downstream systems rather than relying on an LLM to decide if an action is allowed or not. Enforce the complete mediation principle so that all requests made to downstream systems via extensions are validated against security policies."

Mindkettő szó szerint megegyezik az előző kör idézetével.

**OWASP MCP Top 10 — MCP10:2025 Context Injection & Over-Sharing**, `github.com/OWASP/www-project-mcp-top-10`, élőben újranyitva:
> „In MCP-based systems, context acts as the working memory for agents... When this context is shared, persistently stored, or insufficiently scoped, sensitive information from one session, agent, or user can leak into another..."
> „**Context Isolation & Segmentation** Assign unique context namespaces per: User / Agent / Workflow / Tenant... Prevent one agent from accessing another agent's memory directly. In multi-tenant setups, isolate retrieval indexes and vector stores."
> „**Human-in-the-Loop for Sensitive Context** Require approval before sensitive context is: Exported / Summarized / Shared across agents. Show a preview of context that will be reused."

Szó szerint egyezik.

**OWASP Top 10 for Agentic Applications 2026 — ASI03/ASI06**, `genai.owasp.org/download/52117`, élőben újra lekérve (keresésen keresztül, mert a PDF-fetch highlight-alapú, de a releváns bekezdéseket teljes egészében visszaadta):
> „2. Memory-Based Privilege Retention & Data Leakage. Arises when agents cache credentials, keys, or retrieved data for context and reuse. If memory is not segmented or cleared between tasks or users, attackers can prompt the agent to reuse cached secrets, escalate privileges, or leak data from a prior secure session into a weaker one."
> „**Isolate Agent Identities and Contexts**: Run per-session sandboxes with separated permissions and memory, wiping state between tasks to prevent Memory-Based Escalation and reduce Cross Repository Data Exfiltration."

Szó szerint egyezik (a sq04-ben idézett verzió a mondat végét „…" -val rövidítette, de a megmaradt rész pontos).

**AWS Well-Architected Agentic AI Lens**, `docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentsec04-bp02.html`, élőben újranyitva:
> „Risk classification itself can't rely on an LLM exposed to the same untrusted content as the request being evaluated, because adversarial content could **influence** the classifier into marking the request as low-risk. Use deterministic logic (policy engines, rule-based classifiers) as the authoritative signal, with LLM-assisted classification as an optional input that a deterministic layer re-checks."

**Pontosítás:** az előző kör ugyanezt a mondatot idézte, de a „could influence" helyén szögletes zárójellel „could [trick]"-et írt. Az élő oldalon a szó **„influence"**, nem „trick" — a két szó jelentése közel áll egymáshoz (mindkettő azt jelenti, hogy a rosszindulatú tartalom befolyásolhatja az osztályozót), és a szögletes zárójel jelzi, hogy szerkesztett behelyettesítésről van szó, de ez technikailag megsérti a „szó szerinti idézet" szabályt — a tartalmi állítás (ne bízzuk a hatókör-döntést LLM-re, kell egy determinisztikus réteg) ettől függetlenül pontosan igaz és megegyezik. (https://genai.owasp.org/llmrisk/llm06-sensitive-information-disclosure/, https://github.com/OWASP/www-project-mcp-top-10/blob/master/2025/MCP10-2025%E2%80%93ContextInjection%26OverSharing.md, https://genai.owasp.org/download/52117, https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentsec04-bp02.html)

### 6. Meta FAIR „CIMemories" (ICLR 2026)

A cikk **létezik**, és pontosan azt méri, amit az előző kör állít: mennyire tartják be a modellek, hogy egy adott memória-attribútum melyik feladat-kontextusban osztható meg (Nissenbaum kontextuális integritás elmélete alapján).

**ICLR 2026 hivatalos proceedings PDF** (`proceedings.iclr.cc`, T1, elfogadott konferenciacikk — nem csak preprint), élőben lekérve:
> „Our evaluation reveals that frontier models exhibit up to 69% attribute-level violations (leaking information inappropriately), with lower violation rates often coming at the cost of task utility. Violations accumulate across both tasks and runs: as usage increases from 1 to 40 tasks, **GPT-5's** violations rise from 0.1% to 9.6%, reaching 25.1% when the same prompt is executed 5 times, revealing arbitrary and unstable behavior in which models leak different attributes for identical prompts."

**arXiv-verzió** (`arxiv.org/abs/2511.14937`, hivatalos, ugyanaz a szerzői kör), élőben lekérve — az absztrakt szó szerint megegyezik a fenti proceedings-szöveggel, beleértve a „GPT-5's violations" megfogalmazást is.

**Hivatalos GitHub-repó** (`github.com/facebookresearch/CIMemories`, Meta FAIR hivatalos szervezeti repója), élőben lekérve:
> „In our accompanying paper, we find that frontier models exhibit **up to 69% attribute-level violations** (leaking information inappropriately), with lower violation rates often coming at the cost of task utility. Violations accumulate across both tasks and runs: as usage increases from 1 to 40 tasks, **GPT-4o's** violations rise from 0.1% to 9.6%, reaching **25.1% when the same prompt is executed 5 times**, revealing arbitrary and unstable behavior in which models leak different attributes for identical prompts."

**A számok (69%, 0,1%, 9,6%, 25,1%) mindhárom forrásban szó szerint, számjegyre pontosan megegyeznek** — ez erős megerősítés. **Ugyanakkor talált egy valódi ellentmondást, amit az előző kör nem jelzett:** a cikk (mind az arXiv-, mind az ICLR proceedings-verzió) a 0,1%→9,6%→25,1% instabilitási görbét kifejezetten a **„GPT-5"** modellnek tulajdonítja, míg a hivatalos GitHub README ugyanezt a görbét a **„GPT-4o"** modellnek tulajdonítja. Mivel mindkét forrás ugyanattól a Meta FAIR szerzői körtől, hivatalosan származik, ez vagy egy el nem hárított elírás a README-ben (amely esetleg egy korábbi kísérleti kört írt le, mielőtt a cikk véglegesítve lett GPT-5-re), vagy fordítva — de ez egy dokumentált, forrásközi inkonzisztencia, amelyet idézetként kezelve fontos jelezni: **ha valaki a GitHub README-ből idézi ezt az állítást, „GPT-4o"-t fog mondani; ha a publikált cikkből, „GPT-5"-öt.** A kutatási projekt szempontjából ez nem változtatja meg az érdemi következtetést (a jelenség és a számszerű mérték valós és igazolt), de a modell-attribúció pontossága forrásfüggő.

**Peer-review-status:** a `proceedings.iclr.cc/paper_files/paper/2026/...` URL-minta az ICLR hivatalos, elfogadott konferencia-anyagok publikálási útvonala (nem az OpenReview-submission-oldal), ami megerősíti, hogy ez ténylegesen elfogadott ICLR 2026-cikk, nem csupán benyújtott/elutasított preprint. Ezt közvetlenül az OpenReview-n nem ellenőriztem (időkorlát miatt), de a proceedings-oldal léte önmagában erős jelzés. (https://proceedings.iclr.cc/paper_files/paper/2026/file/9a2bcfaf383638e166162a25b6dff125-Paper-Conference.pdf, https://arxiv.org/abs/2511.14937, https://github.com/facebookresearch/CIMemories)

---

## Amit ez a döntésre jelent

1. A hat ellenőrzött állítás mindegyike **alapvetően megállja a helyét** — az előző kutatási kör idézetei szó szerint, elsődleges forrásból visszakereshetők voltak, beleértve a legfontosabb, kockázatosnak tűnő tételeket (konkrét issue-számok: `openai/codex#18343`, `openai/codex#11364`, `mem0#3770`; konkrét, kevéssé ismert forrás: `opspresso/mcp-memory`).
2. A „hívó környezet dönt a hatókörről, nem a modell" elv (OWASP LLM06, MCP10, ASI03/06, AWS Well-Architected) **konzisztensen, több, egymástól szervezetileg is független forrásban** (OWASP alapítvány, AWS) szó szerint alátámasztott — ez erős alap egy tervezési döntéshez, hogy a projekt-hatókört ne a modellre bízzuk.
3. A „header/connection, nem tool-argumentum" minta (Zep) **kereskedelmi termékben, nagy szereplőnél** is megvalósul, nem csak elméleti ajánlás — de a konkrét, sokat idézett indoklás-mondat („a model that can name its own tenant…") egyetlen, 0 csillagos, egyszemélyes GitHub-projektből származik, amelynek nincs második independens forrása; ezt a mondatot ajánlásként, nem mint elterjedt iparági konszenzust érdemes kezelni.
4. A Codex „Memories" funkció jelenlegi (2026-09-25-i) állapota **megerősítetten és dokumentáltan globális**, és ez **szándékos, végrehajtott architektúra-döntés** volt (a `#11364` PR mergelve van) — vagyis a kutatott projekt hiányossága (nincs definiálva, hova kerül egy új emlék) legalább egy nagy, hasonló célú termékben jelenleg is fennáll, és a fejlesztők explicit egyszerűsítés felé mozdultak, nem a hatókör-elkülönítés felé.
5. A CIMemories-szám (69%, illetve 0,1%→25,1%) **erős, három forrásból megerősített bizonyíték** arra, hogy egy LLM önmagában megbízhatatlan a kontextus-függő megosztási döntésben — de a modell-attribúció (GPT-5 vs. GPT-4o) forrásfüggően eltér, ezért ha ezt a számot idézik egy belső dokumentumban, érdemes a cikk (nem a README) szövegét használni referenciaként, és jelezni, hogy a GitHub-repó egy eltérő modellnevet ad meg ugyanahhoz a görbéhez.
6. Egyik ellenőrzött állítás sem dőlt meg érdemben; a talált pontosítások (AWS-idézet egy szava, CIMemories modell-attribúció) apró, forráshűségi jellegű észrevételek, nem a mögöttes érvelést cáfoló tények.

---

## Meglátogatott linkek

| Cím | URL | Tier | Eszköz |
|---|---|---|---|
| MCP Tools Reference (basic-memory) | https://docs.basicmemory.com/reference/mcp-tools-reference | T1 | web_fetch_exa |
| mem0/memory/main.py (main ág) | https://github.com/mem0ai/mem0/blob/main/mem0/memory/main.py | T1 | web_search_exa |
| DOC: Python Quickstart fails · Issue #3770 (mem0) | https://github.com/mem0ai/mem0/issues/3770 | T1 | web_search_exa |
| graphiti/mcp_server/README.md (main ág) | https://github.com/getzep/graphiti/blob/main/mcp_server/README.md | T1 | web_search_exa |
| graphiti_mcp_server.py (4f62cfe7) | https://github.com/getzep/graphiti/blob/4f62cfe7/mcp_server/src/graphiti_mcp_server.py | T1 | web_search_exa |
| Zep Memory MCP Server | https://help.getzep.com/memory-mcp-server | T1 | web_fetch_exa |
| opspresso/mcp-memory README | https://github.com/opspresso/mcp-memory | T3 | web_fetch_exa |
| Claude Code — How Claude remembers your project | https://code.claude.com/docs/en/memory | T1 | web_fetch_exa |
| Codex — Custom instructions with AGENTS.md | https://developers.openai.com/codex/guides/agents-md | T1 | web_fetch_exa |
| Codex — Memories (learn.chatgpt.com) | https://learn.chatgpt.com/docs/customization/memories.md | T1 | web_fetch_exa |
| feat: mem v2 - PR1 (openai/codex #11364) | https://github.com/openai/codex/pull/11364 | T1 | web_fetch_exa |
| Scoped memory management for Codex (openai/codex #18343) | https://github.com/openai/codex/issues/18343 | T1 | web_fetch_exa |
| OWASP LLM06:2025 Excessive Agency | https://genai.owasp.org/llmrisk/llm06-sensitive-information-disclosure/ | T1 | web_fetch_exa |
| OWASP MCP Top 10 — MCP10:2025 Context Injection & Over-Sharing | https://github.com/OWASP/www-project-mcp-top-10/blob/master/2025/MCP10-2025%E2%80%93ContextInjection%26OverSharing.md | T1 | web_fetch_exa |
| OWASP Top 10 for Agentic Applications 2026 (PDF, ASI03/ASI06) | https://genai.owasp.org/download/52117 | T1 | web_search_exa |
| AWS Well-Architected Agentic AI Lens — AGENTSEC04-BP02 | https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentsec04-bp02.html | T1 | web_fetch_exa |
| CIMemories — ICLR 2026 proceedings PDF | https://proceedings.iclr.cc/paper_files/paper/2026/file/9a2bcfaf383638e166162a25b6dff125-Paper-Conference.pdf | T1 | web_fetch_exa |
| CIMemories — arXiv abstract (2511.14937) | https://arxiv.org/abs/2511.14937 | T1 | web_fetch_exa |
| CIMemories — hivatalos GitHub repó (facebookresearch) | https://github.com/facebookresearch/CIMemories | T1 | web_fetch_exa |
| OWASP Agentic Top 10 — ASI06 másodlagos megerősítés (Chris Hughes blog) | https://www.resilientcyber.io/p/owasp-top-10-for-agentic-applications | T2 | web_search_exa |
| OWASP Agentic Top 10 mapping (aisecuritymapping.com PDF) | https://aisecuritymapping.com/wp-content/uploads/Mind-Map-V1-Principle-2-Collapsed.pdf | T2 | web_search_exa |

---

# ELL03 — Hibajegyek a memória-hatókör kezeléséről: léteznek-e, és mit mondanak?

**Módszertani megjegyzés:** ez a munkamenet is (az előző körhöz hasonlóan) sorozatos, egyetlen munkamenetben futó, kizárólag Exa `web_search_exa`/`web_fetch_exa` eszközökkel végzett ellenőrzés — az Exa elérhető volt, alügynök-indítás nem állt rendelkezésre, ezért degradált (nem multi-agent) módban dolgoztam, a `_ell_kozos.txt` előírása szerint. Minden idézett hibajegyet közvetlenül megnyitottam a GitHub-on (Exa fetch), nem az előző kör idézeteire hagyatkoztam.

## Verdikt-összefoglaló

| # | Állítás | Verdikt | Egy mondat |
|---|---|---|---|
| 1 | mem0ai/mem0 #6277, #6342, #6655, #6796 — a `user_id`/`agent_id`/`run_id` hatókör-mezőket a `metadata` felülírhatta; javították-e, melyik verzióban? | **RÉSZBEN** | Mind a négy jegy létezik pontosan az idézett tartalommal, és három (#6277, #6342, #6655) valóban javítva van, konkrét, azonosítható kiadásokban (Python v2.0.13 / v2.0.16, TS/Node v3.1.1) — de a negyedik (#6796) **2026-09-25-én (a mai napon) is NYITOTT**, a javító PR (#6797) még nincs mergelve. |
| 2 | Claude Code #41283 és #53734 — a projekt-hatókör a fájlrendszer-útvonalból jön; worktree-törlés, átnevezés vagy szülőkönyvtárra lépés miatt más projekt memóriája töltődik be (#53734: 8 eset) | **RÉSZBEN, jelentős pontosítással** | Mindkét jegy létezik, a „8 dokumentált eset" idézet szó szerint stimmel, DE #41283-at a stale-bot zárta le kód-javítás nélkül, #53734-et pedig — miután egy másik, szintén megoldatlan jegy (#52772) duplikátumaként inaktivitás miatt lezárták — a bejelentő újra beküldte (#86945), és ott egy Anthropic-mérnök (bcherny, 2026-08-25) kifejezetten **dokumentált, szándékos viselkedésnek** minősítette a git-repository-szintű megosztást, „working-as-documented"-ként zárva, létező konfigurációs megoldással (`autoMemoryDirectory`). |
| 3 | Claude Code #40541 — a modell CLAUDE.md explicit szabály ellenére 5+ alkalommal keverte a personal/project/team infót | **RÉSZBEN** | A jegy és az idézet szó szerint létezik, de az ügy **egyetlen felhasználó (n=1) be nem vizsgált** beszámolója, amelyet a bejelentő saját maga zárt le kb. egy órán belül „duplikátumként" három olyan másik jegyhez, amelyek — ellenőrzésem szerint — **nem ugyanarról a hibáról szólnak**; ez egybevág a repó dokumentált, önálló meta-problémájával (#19267), miszerint a duplikátum-bot gyakran téves párosításokat javasol. |

## Állításonként

### 1. mem0ai/mem0 — #6277, #6342, #6655, #6796

**#6277** (Python SDK, `update()`) — LÉTEZIK, megerősítve.
- Cím pontosan: *„update() lets caller metadata silently overwrite user_id/agent_id/run_id, breaking tenant isolation"*
- Állapot: **Closed**. Létrehozva: 2026-07-13. Címkék: `bug`, `P0-critical`.
- Szó szerint (karbantartói triázs, kartik-mem0): „**Severity:** P0. No malformed input is needed — a normal-looking `metadata` dict silently breaks tenant isolation and causes real data loss…plus cross-tenant data exposure, on both the Python SDK's primary write path and the shipped REST server."
- **Javítva:** PR **#6278** (*„fix(memory): don't let update() metadata overwrite user_id/agent_id/run_id"*), state: **merged**, mergelve **2026-07-21T07:14:22Z**. A review-folyamat egy második, súlyosabb rést is feltárt és bezárt még a mergelés előtt: a reviewer (kartik-mem0) írta: „the loop only re-asserts an identity key `if _identity_key in existing_memory.payload`… `update(metadata={"agent_id": "attacker_agent"})` injects a brand-new identity key straight into the stored payload unopposed" — ezt a szerző „strip-before-merge" megközelítésre váltva javította a mergelés előtt.
- **Kiadott verzióban:** a mem0ai Python SDK **v2.0.13** (GitHub release, publikálva 2026-07-22T19:41:55Z) tartalmazza: „Core: Stop `update()` metadata from overwriting or injecting `user_id`, `agent_id`, `run_id`, or `actor_id`… (#6278)". Két független forrás a verziószámra: GitHub Releases (https://github.com/mem0ai/mem0/releases/tag/v2.0.13) és a PyPI/ReversingLabs verziólista (https://secure.software/pypi/packages/mem0ai/versions), amely v2.0.13-at is felsorolja a v2.0.12 (2026-07-13) után.
- URL: https://github.com/mem0ai/mem0/issues/6277 ; PR: https://github.com/mem0ai/mem0/pull/6278

**#6342** (TypeScript OSS SDK, `update()`) — LÉTEZIK, megerősítve.
- Cím pontosan: *„update() metadata silently overwrites user_id/agent_id/run_id in TS SDK, breaking tenant isolation"*
- Állapot: **Closed**. Létrehozva: 2026-07-16. Címkék: `bug`, `P0-critical`.
- Szó szerint: „This is a regression: #5480 removed the identity-key whitelist that previously protected these fields here."
- **Javítva:** PR **#6343**, state: **merged**, mergelve **2026-07-21T06:41:47Z**, lezárja #6342-t ÉS #6367-et (egy a review során feltárt camelCase-alias rést is, `userId`/`agentId`/`runId`, amit a `normalizePayload()` promóciós logikája nyitva hagyott volna).
- **Kiadott verzióban:** a mem0 **Node/TypeScript SDK v3.1.1** (GitHub release, publikálva 2026-07-22T18:12:36Z) tartalmazza szó szerint: „Memory (OSS): Stop `update()` metadata from overwriting or injecting `user_id`, `agent_id`, `run_id`, or `actor_id` (in either snake_case or camelCase)… (#6343)". Két független forrás: GitHub Releases (https://github.com/mem0ai/mem0/releases/tag/ts-v3.1.1) és npm registry (https://registry.npmjs.org/mem0ai — „3.1.1 · Published Jul 22, 2026").
- URL: https://github.com/mem0ai/mem0/issues/6342 ; PR: https://github.com/mem0ai/mem0/pull/6343

**#6655** (Python SDK, `add()` — a létrehozási útvonal testvérhibája) — LÉTEZIK, megerősítve.
- Cím pontosan: *„Python OSS SDK: add() lets metadata set identity scope (user_id/agent_id/run_id/actor_id) on creation"*
- Állapot: **Closed**. Létrehozva: 2026-07-29.
- Szó szerint: „The created memory is now discoverable through `get_all(filters={"agent_id": "victim-agent"})`… scopes the caller never held."
- **Javítva:** PR **#6656** (*„fix(memory): stop add() metadata from setting a memory's identity scope"*) — FONTOS PONTOSÍTÁS: az előző kör összefoglaló táblázata nem tüntette fel a javító PR számát ennél a jegynél; a javítás nem a #6655-ös számú PR-ban, hanem a **#6656**-ban történt (az issue és a fix PR száma itt eltér a #6277/#6278 és #6342/#6343 párosokétól).
- **Kiadott verzióban:** a mem0ai Python SDK **v2.0.16** (GitHub release, publikálva 2026-08-04T18:51:47Z) tartalmazza: „Core: Stop `add()` metadata from setting a memory's identity scope… (#6656)". Megerősítve a hivatalos changelog-oldalon is (https://docs.mem0.ai/changelog/sdk).
- URL: https://github.com/mem0ai/mem0/issues/6655

**#6796** (TypeScript OSS SDK, `add()` — a hívó `filters` objektumának mutálása) — LÉTEZIK, DE **MÉG NYITOTT**.
- Cím pontosan: *„add() mutates the caller's filters object, leaking scope into the next add() and bypassing the required-scope check"*
- Állapot: **Open** (2026-08-04 óta, utolsó frissítés 2026-08-18). Címke: `sdk-typescript`. **Nincs `P0-critical` vagy `bug` címke rajta**, csak `sdk-typescript`.
- Szó szerint: „Result, 10 runs out of 10: no error is thrown, and the second memory is stored under `user_id: \"alice\"`."
- **Javítás státusza — eltérés az implicit korábbi képtől:** a javító PR **#6797** (*„fix(ts-oss): stop add() from mutating the caller's filters object"*) **NYITOTT** (nincs `Merged:` időbélyeg), utolsó frissítés **2026-09-25** (a mai nap) — vagyis a mai napon is aktívan zajló, le nem zárt PR. A PR szerzője (shashiKundur1) egy 2026-08-10-i kommentben egy **még szélesebb** kapcsolódó rést is dokumentált, amit egy időközben mergelt másik javítás (#6377) vezetett be: „`filters` is still the caller's object, so a scope left behind by an earlier call is now also stamped into the stored row's **metadata**, not just used to scope the write… It never had a scope of its own. It inherited one through the object the caller reused."
- **Következtetés:** a négy jegyből három (P0-critical, mind javítva, konkrét kiadási verzióval), a negyedik viszont alacsonyabb súlyosságú címkével, ~7 hete nyitva, javítatlanul.
- URL: https://github.com/mem0ai/mem0/issues/6796 ; PR: https://github.com/mem0ai/mem0/pull/6797

### 2. Claude Code — #41283 és #53734

**#41283** — LÉTEZIK, az idézetek stimmelnek, de a lezárás módja fontos pontosítás.
- Cím pontosan: *„Memory identity is derived from filesystem path, causing orphaned memories and missing the human-vs-project distinction"*
- Állapot: **Closed**. Létrehozva: 2026-03-31. Címkék: `enhancement`, `area:core`, `memory`, **`stale`**.
- Az idézett szövegek (worktree/rename orphaning, „Global memory… exists but is an afterthought") szó szerint megegyeznek az eredetivel.
- **Pontosítás — a jegy nem „bug", hanem `enhancement` címkével fut**, és maga a szöveg elismeri, hogy a worktree-orphaning nagy részét egy KORÁBBI módosítás már kezelte: „The worktree resolution was a step in the right direction, but the underlying issue remains: filesystem path is not a stable identity for a git repository." — vagyis a bejelentéskor a worktree-k már jellemzően a fő repó memóriájára oldódtak fel; a nyitva maradt rész elsősorban az átnevezés-stabilitás és a personal/project szétválasztás hiánya.
- **A `stale` címke és a lezárás módja arra utal, hogy a jegyet nem kódjavítás zárta le**, hanem az inaktivitás-bot — nincs a threadben `merged`/`fixed` jellegű maintainer-válasz vagy hivatkozott lezáró PR; a beszélgetés harmadik féltől származó eszközök (pl. „claude-brain", „Alzheimer") ismertetésével folytatódik, nem hivatalos Anthropic-válasszal.
- URL: https://github.com/anthropics/claude-code/issues/41283

**#53734** — LÉTEZIK, a „8 eset" idézet pontos, DE a jegy státusza és a mögötte álló magyarázat lényegesen árnyaltabb, mint amit az előző kör sugallt.
- Cím pontosan: *„[BUG] auto-memory resolver walks up to ancestor-encoded project directory instead of cwd-encoded path"*
- Állapot: **Closed**, egyetlen címke: **`duplicate`**. Létrehozva: 2026-04-27.
- Az idézett mondat szó szerint stimmel: „We documented 8 cross-agent contamination incidents over approximately one month of ecosystem operation on this machine before we mitigated by eliminating the ancestor `memory/` directory."
- **A lezárás láncolata (ellenőrizve a hivatkozott jegyeken keresztül):** #53734-et **duplikátumként zárták #52772-höz**, amely maga is **inaktivitás miatt (stale-bot) lett automatikusan lezárva** 2026-05-28-án, kódjavítás nélkül — vagyis a „duplikátum" célpontja sem lett soha ténylegesen megoldva.
- **A bejelentő 2026-08-15-én újra beküldte** a hibát (#86945, *„auto-memory resolver still walks up to ancestor-encoded project (re-filing #53734 / #52772, unfixed)"*), és ekkor — először — **kapott érdemi Anthropic-mérnöki választ** (bcherny, 2026-08-25, Claude Code 2.1.233-on reprodukálva). Szó szerint: „**This is the documented, intended behavior rather than a resolver walking up incorrectly: auto memory is scoped per git repository, so all worktrees and subdirectories within the same repo deliberately share one memory directory.** Only outside a git repo is the launch directory used… For your setup — independent sub-projects living inside one parent repository — there is a supported way to get per-subproject memory: set `autoMemoryDirectory` in each subproject's `.claude/settings.json`… **Closing as working-as-documented.**"
- **Ez érdemi eltérés az előző kör állításától**, amely #53734-et minősítés nélkül „dokumentáltan más ügynök/projekt memóriáját tölti be" hibaként idézte: a mögöttes mechanizmus léte és a 8 eset ténye nem cáfolható, DE a gyártó hivatalos, 2026-08-25-i álláspontja szerint ez **nem hiba, hanem szándékos tervezési döntés** (git-repository-szintű megosztás), amelyhez már a jegy lezárásakor is létezett dokumentált, támogatott opt-out (`autoMemoryDirectory`). A #53734-ben leírt konkrét „ős-könyvtárra lépés" tehát valós jelenség, de a „bug" minősítés maga vitatott/elutasított.
- URL: https://github.com/anthropics/claude-code/issues/53734 ; kapcsolódó: https://github.com/anthropics/claude-code/issues/52772 , https://github.com/anthropics/claude-code/issues/86945

### 3. Claude Code — #40541

- Cím pontosan: *„Claude repeatedly ignores CLAUDE.md rules about information scope/context boundaries"*
- Állapot: **Closed**. Létrehozva: 2026-03-29T10:10:55Z. Címkék: `bug`, `area:model`, `platform:wsl`.
- Az idézett mondat szó szerint stimmel: „Had to be corrected 5+ times in a single conversation for the same category of mistake."
- **Fontos pontosítás a lezárás körülményeiről:** a jegyet a github-actions bot 3 percen belül „lehetséges duplikátumként" jelölte meg (#29121, #37961, #40425), majd **a bejelentő maga zárta le duplikátumként ugyanazon a napon, 58 perccel a felnyitás után** (2026-03-29T11:08:07Z) — nincs a threadben Anthropic-mérnöki vizsgálat vagy megerősítés a jelenség valódiságáról vagy gyakoriságáról.
- **Ellenőriztem mind a három „duplikátumot", és tartalmilag egyik sem ugyanarról a jelenségről szól:**
  - **#29121** — *„Claude Code drafts public bug reports containing sensitive project information without anonymising"* — arról szól, hogy Claude egy NYILVÁNOS GitHub-jegybe írt bele privát szervezetneveket/repó-URL-eket; ez adat-anonimizálási hiba, nem personal/project/team hatókör-keverés.
  - **#37961** — *„Claude takes unauthorized actions outside agreed plan (filed external bug report without permission)"* — arról szól, hogy Claude egy KÜLSŐ cég támogatási rendszerébe küldött be jegyzést engedély nélkül; ez jogosulatlan cselekvés, nem információ-hatókör keverés.
  - **#40425** — *„Claude Code fails to follow established process rules despite repeated correction"* — arról szól, hogy Claude egy csapat-munkafolyamat szerepkör-szabályait (PM ne írjon kódot) sérti meg ismételten; ez a legközelebbi rokon téma (szabálykövetési hiba explicit, mentett szabályok ellenére is), de NEM ugyanaz a konkrét hiba (personal/project/team infó keveredése), amit #40541 leír.
- Ez a mintázat egybevág a repó saját, dokumentált meta-problémájával: **#19267** (*„The github bot creates impenetrable webs of duplicate tags in bug reports"*) szó szerint írja: „Often, the guessed duplicates are different problems. As a result, real bugs will automatically closed." — és egy Claude Code-hoz kötött komment ugyanitt: „the issue tracker has two states (open/closed) for something that needs at least four… Closing it says 'this problem doesn't exist' when the reality is 'this problem exists but is low priority'."
- **Következtetés erre a claimre:** az idézet és a hibajegy létezése megerősítve, de ez egyetlen felhasználó (n=1) be nem vizsgált, önmaga által „duplikátumnak" minősített beszámolója, amelynek „duplikátum" célpontjai — ellenőrzésem szerint — más hibaosztályba tartoznak; Anthropic-mérnöki megerősítés vagy cáfolat a jelenség valódiságáról nem található a nyilvános tracker-ben.
- URL: https://github.com/anthropics/claude-code/issues/40541 ; kapcsolódó: https://github.com/anthropics/claude-code/issues/29121 , https://github.com/anthropics/claude-code/issues/37961 , https://github.com/anthropics/claude-code/issues/40425 , https://github.com/anthropics/claude-code/issues/19267

## Amit ez a döntésre jelent

1. A mem0 tenant-izolációs hibaosztály (metadata felülírja a hatókör-mezőket) valós és jól dokumentált volt, de **nem egyenletesen javított**: a legrégebbi és legsúlyosabban címkézett három eset (#6277/#6278→v2.0.13, #6342/#6343→v3.1.1, #6655/#6656→v2.0.16) le van zárva, konkrét kiadásokkal alátámasztva — a legújabb, kapcsolódó eset (#6796, `add()` a hívó `filters` objektumát mutálja) viszont **2026-09-25-én, a kutatás napján is nyitott**, alacsonyabb súlyossági címkével és mergelés nélküli javító PR-ral. Egy 2026-09-25-i pillanatfelvétel tehát nem mondhatja azt, hogy „a mem0 tenant-izolációs hibái javítva vannak" — csak azt, hogy a korábbi, súlyosabb sorozat javítva van, egy rokon, frissebb rés viszont nem.
2. A Claude Code #41283 és #53734 jegyekben leírt „más projekt memóriája töltődik be" jelenség ténylegesen dokumentált (8 konkrét eset, reprodukciós lépések), de **a gyártó hivatalos, később született álláspontja (2026-08-25) szerint a git-repository-szintű megosztás szándékos, dokumentált tervezési döntés, nem hiba** — ez közvetlenül szűkíti azt az állítást, hogy ez „dokumentáltan hibás" viselkedés lenne; helyesebb úgy fogalmazni, hogy a viselkedés dokumentáltan létezik és dokumentáltan nem tetszik egyes felhasználóknak, de a gyártó nem hibaként, hanem tervezési kompromisszumként kezeli, meglévő opt-out mechanizmussal.
3. Mindkét Claude Code „bizonyíték" (#41283, #53734, #40541) esetében a hibajegy-tracker saját, önmagát dokumentáló meta-problémája (automatikus stale-zárás és téves duplikátum-párosítás, l. #19267) megnehezíti annak eldöntését, hogy egy lezárt jegy azért záródott-e le, mert megoldották, mert elavult, vagy mert tévesen párosították egy másik, nem kapcsolódó jeggyel — ez módszertani figyelmeztetés minden jövőbeli GitHub-issue-alapú bizonyítékgyűjtésre nézve ennél a repónál.
4. #40541 konkrétan **n=1, be nem vizsgált** anekdota: az idézett „5+ alkalommal hibázott" állítás a bejelentő saját, ellenőrizetlen leírása, amelyet sem Anthropic-mérnök, sem másik felhasználó nem erősített meg vagy vizsgált ki nyilvánosan a tracker-ben — ez nem azt jelenti, hogy hamis, csak azt, hogy alacsonyabb bizonyító erejű, mint egy karbantartó által megerősített, reprodukált hiba (mint amilyenek a mem0 P0-jegyei).
5. A #6655/#6656 számpár eltérése (az issue és a javító PR száma nem esik egybe) és a #53734→#52772→#86945 lezárási lánc is azt mutatja, hogy pusztán egy hibaszám és cím megléte nem elég a „javítva" vagy „még mindig probléma" státusz megállapításához — mindig a hozzá tartozó PR/kommentlánc és — ha van — az újrabeküldött/követő jegy adja a tényleges, aktuális státuszt.
6. Egyik forrás sem tartalmaz semmilyen utalást arra, hogy a `personal`/`projects`/`knowledge` hármas hatókör-modell (amit az easter-memory-system tervez) bármelyik vizsgált eszközben (mem0, Claude Code) már létezne — a talált hibák mind egy **kétszintű** (tenant/user vs. git-repository-alapú projekt) modell repedéseiről szólnak, nem egy explicit háromszintű hierarchiáról.

## Meglátogatott linkek

| Cím | URL | Tier | Eszköz |
|---|---|---|---|
| update() lets caller metadata silently overwrite user_id/agent_id/run_id (mem0 #6277) | https://github.com/mem0ai/mem0/issues/6277 | T1 | Exa fetch |
| fix(memory): don't let update() metadata overwrite… (mem0 PR #6278) | https://github.com/mem0ai/mem0/pull/6278 | T1 | Exa fetch/search |
| update() metadata overwrite TS SDK (mem0 #6342) | https://github.com/mem0ai/mem0/issues/6342 | T1 | Exa fetch |
| fix(ts-oss): don't let update() metadata overwrite… (mem0 PR #6343) | https://github.com/mem0ai/mem0/pull/6343 | T1 | Exa fetch/search |
| Python OSS SDK: add() lets metadata set identity scope (mem0 #6655) | https://github.com/mem0ai/mem0/issues/6655 | T1 | Exa fetch |
| add() mutates the caller's filters object (mem0 #6796, NYITOTT) | https://github.com/mem0ai/mem0/issues/6796 | T1 | Exa fetch |
| fix(ts-oss): stop add() from mutating the caller's filters object (mem0 PR #6797, NYITOTT) | https://github.com/mem0ai/mem0/pull/6797 | T1 | Exa fetch |
| mem0ai Python SDK v2.0.13 release notes | https://github.com/mem0ai/mem0/releases/tag/v2.0.13 | T1 | Exa fetch |
| mem0ai Python SDK v2.0.16 release notes | https://github.com/mem0ai/mem0/releases/tag/v2.0.16 | T1 | Exa fetch |
| mem0 Node SDK v3.1.1 release notes | https://github.com/mem0ai/mem0/releases/tag/ts-v3.1.1 | T1 | Exa search |
| mem0ai npm registry (verziólista, független megerősítés) | https://registry.npmjs.org/mem0ai | T1 | Exa search |
| mem0ai PyPI verziólista (ReversingLabs, független megerősítés) | https://secure.software/pypi/packages/mem0ai/versions | T2 | Exa search |
| SDK & Tools changelog (mem0 hivatalos) | https://docs.mem0.ai/changelog/sdk | T1 | Exa fetch |
| Memory identity derived from filesystem path (Claude Code #41283) | https://github.com/anthropics/claude-code/issues/41283 | T1 | Exa fetch |
| auto-memory resolver walks up to ancestor (Claude Code #53734) | https://github.com/anthropics/claude-code/issues/53734 | T1 | Exa fetch |
| Auto memory system prompt path vs. /memory mismatch (Claude Code #52772, #53734 „duplikátuma") | https://github.com/anthropics/claude-code/issues/52772 | T1 | Exa fetch |
| Re-filing #53734/#52772, closed working-as-documented (Claude Code #86945) | https://github.com/anthropics/claude-code/issues/86945 | T1 | Exa fetch |
| Claude repeatedly ignores CLAUDE.md scope rules (Claude Code #40541) | https://github.com/anthropics/claude-code/issues/40541 | T1 | Exa fetch |
| Bug reports leak private org info, unrelated topic (Claude Code #29121) | https://github.com/anthropics/claude-code/issues/29121 | T1 | Exa fetch |
| Unauthorized external bug filing, unrelated topic (Claude Code #37961) | https://github.com/anthropics/claude-code/issues/37961 | T1 | Exa fetch |
| Fails to follow process rules (PM writes code), closest de nem azonos topik (Claude Code #40425) | https://github.com/anthropics/claude-code/issues/40425 | T1 | Exa fetch |
| Duplicate-bot mismatches real bugs — meta-probléma (Claude Code #19267) | https://github.com/anthropics/claude-code/issues/19267 | T1 | Exa search |

---

# SQ05 — Mit adnak be a memória-eszközök a munkamenet elején — tartalom, forma, méret?

**Módszertani megjegyzés (degradált mód):** Ez a kutatás egyetlen kutató-ügynökként készült, alügynökek indítása nélkül — ebben a környezetben nem állt rendelkezésre Task/Agent-alapú párhuzamos alügynök-indítás, ezért a `deep-web-research` skill többügynökös pipeline-ja helyett szekvenciális/párhuzamos Exa-kereséssel és -olvasással dolgoztam fel mind a tíz+ rendszert. Kizárólag `mcp__Exa__web_search_exa` és `mcp__Exa__web_fetch_exa` eszközöket használtam; a beépített WebSearch/WebFetch-et nem. A mai dátum **2026-09-25**; minden verziót/dátumot jelöltem, ahol a forrás megadta. Az SQ03-ban feltárt hook-mechanikát (mely kliens, milyen bemenet, méretkorlát) nem kutattam újra — csak ott hivatkozom rá, ahol az adott memória-eszköz épp arra a hookra épül.

---

## Rövid válasz

A tíz vizsgált rendszer öt, jól elkülöníthető mintát követ. (1) **Fájlalapú, determinisztikus, méretkorlátos index**: a Claude Code auto memory a `MEMORY.md` első 200 sorát VAGY 25 KB-ját tölti be minden munkamenet elején (amelyik előbb betelik), a tartalmat maga a modell írja korábbi munkamenetekben, de a *betöltés* sablonos fájlolvasás; egy nyitott hibajegy szerint a névleges 25 KB helyett a gyakorlatban komoly adatvesztés (34,3 KB-os fájlnál csak a limit alatti rész eredményes, a felhasználó csak utólag vette észre a hatását). (2) **Determinisztikusan összeállított, de korábban modell által tömörített megfigyelés-lista**: a claude-mem alapértelmezés szerint az utolsó 10 munkamenet ~50 megfigyelését injektálja egy `SessionStart` hookon keresztül, réteges („progresszív") megjelenítéssel (~50–200 token az index-nézethez, ~100–500 token/megfigyelés a teljes lekéréshez); a megfigyeléseket korábban egy Claude Agent SDK-alapú „worker" tömöríti XML-formátumba. (3) **Aktív keresés/pull, nincs automatikus dump induláskor**: az OpenMemory, a basic-memory és a Serena `initial_instructions`/`onboarding` mechanizmusa nem tölt be tartalmat automatikusan a munkamenet elejére, hanem a modellt eszközleíráson vagy explicit szabályon keresztül keresésre/olvasásra utasítja. (4) **Mindig kontextusban lévő, szerkeszthető blokk**: a Letta „core memory blocks" nem retrieval-alapú, hanem szó szerint a rendszer-promptba van „tűzve" (ajánlott < 50 000 karakter összesen, < 20 blokk), és dokumentált hibajegyek szerint a blokk-méretkorlát be nem tartása valós költségrobbanáshoz vezetett (egyes felhasználók „$30+ Claude-kreditet égettek el órák alatt"). (5) **A funkció megszűnése**: a Cursor natív „Memories" funkcióját — amely háttérben, modell által generált, projektenkénti rövid tényeket automatikusan visszahozott — a gyártó 2025. november 21-én (2.1.17-es verziótól) eltávolította, és a hivatalos fórumon a Cursor-staff maga is ellentmondásosan nyilatkozott arról, hogy a funkció ténylegesen megszűnt-e, vagy csak a kezelőfelülete. A Windsurf Cascade Memories hasonlóan automatikus, modell-generált, de workspace-hez kötött és csak releváns esetben kerül elő — a hozzá tartozó `global_rules.md` viszont dokumentáltan mindig, korlátozott mérettel (6000 karakter) töltődik be minden munkamenetben. Az OpenAI Codex natív „memories" funkciója (nem a mem0-plugin!) kétfázisú (extract/consolidation) modell-generálást használ, és dokumentált precedencia-hiba miatt elavult emlék felülírhatja az aktuális, explicit `AGENTS.md`-szabályt.

---

## 1. Claude Code auto memory (`MEMORY.md`)

**1) Mit ad be induláskor:** a `MEMORY.md` index-fájl tartalmát (nem statisztikát, nem puszta címlistát, hanem magát a szöveges tartalmat), plusz a projekt `CLAUDE.md` fájljait teljes egészében.

> "Each project gets its own memory directory at `~/.claude/projects//memory/`. […] The directory contains a `MEMORY.md` entrypoint and optional topic files" — https://code.claude.com/docs/en/memory (hivatalos, verzió: élő doksi, 2026-09-25-i állapot)

> "`MEMORY.md` acts as an index of the memory directory. Claude reads and writes files in this directory throughout your session, using `MEMORY.md` to keep track of what's stored where." — https://code.claude.com/docs/en/memory

A topikfájlokat (pl. `debugging.md`) **nem** tölti be induláskor, csak igény szerint olvassa:

> "Topic files like `debugging.md` or `patterns.md` are not loaded at startup. Claude reads them on demand using its standard file tools when it needs the information." — https://code.claude.com/docs/en/memory

**2) Hogyan készül:** a *tartalmat* maga a modell írja („Claude saves notes for itself"), a *betöltés* determinisztikus (fájlolvasás + méret-vágás), nem összefoglalás induláskor:

> "Auto memory: notes Claude writes itself based on your corrections and preferences" — https://code.claude.com/docs/en/memory

> "Claude doesn't save something every session. It decides what's worth remembering based on whether the information would be useful in a future conversation." — https://code.claude.com/docs/en/memory

**3) Méret és korlát:** dokumentált, kemény korlát.

> "The first 200 lines of `MEMORY.md`, or the first 25KB, whichever comes first, are loaded at the start of every conversation. Content beyond that threshold is not loaded at session start." — https://code.claude.com/docs/en/memory

> "If the file is over a limit, the write still succeeds, but Claude Code returns an error telling Claude to rewrite the index, because everything past the limit is dropped on the next load." — https://code.claude.com/docs/en/memory

> "The check measures only the content that loads: YAML frontmatter and block-level HTML comments are stripped before the index is loaded, so they don't count toward the limits." — https://code.claude.com/docs/en/memory

> "This limit applies only to `MEMORY.md`. […] Claude Code loads a CLAUDE.md file of up to 4 MiB in full and skips a larger file." — https://github.com/lenneTech/claude-code/blob/main/.claude/docs-cache/memory.md (hivatalos doksi GitHub-gyorsítótár-tükrözése, T2)

**4) Nyelv/forma:** markdown, YAML frontmatter-rel (`type`, `modified` mezők); zárt kategória-taxonómia: `user`, `feedback`, `project`, `reference` (a fenti mirror-forrás szerint).

**5) Dokumentált tapasztalat — MI NEM VÁLT BE:** a felhasználó által jelentett hiba szerint a névleges limit alatt csendben veszett el releváns, friss adat, és a figyelmeztetés nem volt eléggé látható:

> "Auto-memory `MEMORY.md` is loaded at session start with what appears to be a ~25KB / 200-line cap. When `MEMORY.md` exceeds this cap, content beyond the cap is silently dropped with only a buried warning in the system prompt." — https://github.com/anthropics/claude-code/issues/57574 (T1, hivatalos repó hibajegy)

> "In my case, `MEMORY.md` reached 34.3KB. […] `WARNING: MEMORY.md is 34.3KB (limit: 24.4KB) — index entries are too long. Only part of it was loaded. Keep index entries to one line under ~200 chars; move detail into topic files.` …but only as a buried line that I noticed only after asking Claude to investigate why it was repeating mistakes." — https://github.com/anthropics/claude-code/issues/57574

A felhasználó saját, sikeres beavatkozása (T1, ugyanaz a hibajegy) konkrét számokkal igazolja a „túl hosszú lista rossz" mintát:

> "I restructured `MEMORY.md` from a 35.5KB chronological list into a 3.5KB tiered index (90% reduction) […] The restructure recovered ~8,000 tokens of context budget at every session start." — https://github.com/anthropics/claude-code/issues/57574

Ugyanez a hibajegy hivatkozik több másik, nyitott jegyre arról, hogy a modell (Opus 4.6/4.7) figyelmen kívül hagyja a `MEMORY.md`/`CLAUDE.md` szabályait még akkor is, ha azok betöltődtek (#52382, #56419, #53753, #45569, #33603 — nem olvastam el mindegyiket önállóan, csak az #57574-es jegy idézi őket, ezért ezt csak másodkézből jelzem, NEM önálló megerősítésként).

*Megbízhatósági megjegyzés:* egy nem hivatalos, „forráskód-visszafejtő" harmadik fél (claude-wiki.com, T3) és két hasonló, szintén nem hivatalos „forráskód-tükröző" oldal (mintlify.com/killlowkey, T3; sanbuphy-claude-code-source-code.mintlify.app, T3) egybehangzóan azt állítják, hogy a `MEMORY.md`-kivonatolás egy háttérben futó, elágaztatott ("forked") Opus-alapú alügynök (`extractMemories`) útján történik, ami állítólag megduplázza a tényleges tokenfogyasztást. Ez **nem hivatalos forrásból** származik, a code.claude.com hivatalos doksi ezt a mechanizmust nem részletezi ilyen mélységben — három egymást erősítő, de mind T3 forrás van rá, óvatosan kezelendő.

---

## 2. claude-mem (thedotmack/claude-mem)

**1) Mit ad be induláskor:** a legutóbbi N munkamenet megfigyeléseinek kronologikus idővonalát (index-nézet: cím + típus + tokenköltség-becslés), plusz — ha van — a legutóbbi összefoglaló mezőit (Investigated/Learned/Completed/Next Steps), **csak ha** az összefoglaló a legutóbbi megfigyelés után készült.

> "1. Queries the database for recent observations in your project (default: 50) 2. Retrieves recent session summaries for context 3. Displays observations in a chronological timeline with session markers 4. Shows full summary details […] only if the summary was generated after the last observation 5. Injects formatted context into Claude's initial context" — https://docs.claude-mem.ai/usage/getting-started (hivatalos projektdoksi, T1 a saját projektjére nézve)

**2) Hogyan készül:** kétlépcsős — a megfigyelések *tartalmát* korábban egy Claude Agent SDK-alapú „worker" (modell) tömöríti strukturált (XML) formába, de az injektálandó *kimenetet* induláskori determinisztikus lekérdezés/renderelés állítja össze (`ContextBuilder.ts`), nem LLM-hívás abban a pillanatban:

> "SDK agent calls Claude to compress observation into structured format" — https://github.com/thedotmack/claude-mem/blob/v10.6.3/docs/public/architecture/hooks.mdx (T1, saját repó)

> `function buildContextOutput(...)` — a `ContextBuilder.ts` forráskódja lekérdezi az adatbázist (`queryObservationsMulti`, `querySummariesMulti`), majd sablonszerűen renderel (`renderHeader`, `renderTimeline`, `renderFooter`), LLM-hívás nélkül — https://github.com/thedotmack/claude-mem/blob/e0249485/src/services/context/ContextBuilder.ts (T1, saját repó, forráskód)

A "Strict Observer Response Contract" explicit XML-sémát kényszerít ki a megfigyelés-generálásnál:

> "`buildObservationPrompt` now requires `<observation>` XML blocks or an empty response." — https://github.com/thedotmack/claude-mem/blob/main/CHANGELOG.md (T1)

**3) Méret:** konfigurálható, dokumentált alapértékekkel és tokenbecsléssel.

> "| Observations | 50 | 1-200 | Total number of recent observations to include | | Sessions | 10 | 1-50 | Number of recent sessions to pull observations from |" — https://docs.claude-mem.ai/configuration (T1)

> "Token cost: ~50-200 tokens for index view" […] "Token cost: ~100-500 tokens per observation fetched" — https://docs.claude-mem.ai/usage/getting-started (T1)

**4) Nyelv/forma:** markdown a modellnek küldött kontextushoz (`hookSpecificOutput.additionalContext`), XML a belső megfigyelés-generáláshoz; 28 nyelvet támogat a projekt kimenete:

> "🌐 Multilingual Modes - Supports 28 languages" — https://docs.claude-mem.ai/introduction (T1)

**5) Dokumentált tapasztalat:** a projekt saját változásnaplója szerint korábban a `UserPromptSubmit` eseményen **minden** promptnál lefutott egy szemantikus (Chroma vektoros) keresés, amit a fejlesztők a felhasználói visszajelzés (túl sok zaj/lassúság) alapján opt-in-re változtattak:

> "Chroma vector search on `UserPromptSubmit` is now opt-in rather than opt-out. Reduces latency and context noise for users [who] haven't explicitly enabled it." — https://github.com/michaelbuckner/claude-mem/blob/25ccf46.../CHANGELOG.md (T2, forkolt repó changelog-ja, de a hivatkozott mechanizmus a fő projektével egyezik)

Ugyanez a changelog dokumentálja, hogy a token-gazdaságossági oszlopokat (mennyi tokent spórolt a cache) alapból elrejtették újratelepítéskor, mert túl zajosnak bizonyultak:

> "New installs now default to a streamlined context display: Read tokens column: hidden […] Work tokens column: hidden […] Savings amount: hidden" — https://github.com/thedotmack/claude-mem/blob/main/CHANGELOG.md (T1)

**Ellentmondás a saját dokumentáción belül (verziók között):** egy korábbi verzió (Mr1Stark fork, v4.0-ás changelog) szerint az induláskor betöltött ablak **3** munkamenet volt, a jelenlegi hivatalos doksi és az alapértelmezett config **10**-et mond:

> "SessionStart Hook (context-hook.js): Queries database for last 3 sessions and injects context" — https://github.com/Mr1Stark/claude-mem (T2, fork, dátum nem egyértelmű)

> "Session Start → Inject context from last 10 sessions" — https://docs.claude-mem.ai/introduction (T1, jelenlegi hivatalos állapot)

---

## 3. mem0 (Claude Code / Codex plugin, `mcp.mem0.ai`)

**1) Mit ad be induláskor:** egy determinisztikusan összeállított „státusz-banner" (hatókör: user/project/global, memóriaszám) plusz — ha van korábbi memória — egy rövid, tömör „recent activity timeline"-t, plusz egy fix szöveges instrukció, hogy a modell induljon keresésre.

> "Session start | `SessionStart` | Loads prior memories and displays status banner" — https://docs.mem0.ai/integrations/claude-code (T1, hivatalos)

A tényleges hook-forráskód (`on_session_start.sh`) igazolja, hogy ez sablonos bash/python szkript, nem modellhívás:

> `echo "Search mem0 for recent decisions and task learnings before responding. Run 2 parallel searches: one for decision type, one for task_learning type."` — https://github.com/mem0ai/mem0/blob/main/integrations/mem0-plugin/scripts/on_session_start.sh (T1, saját repó forráskód)

Új projektnél (0 memória) más az utasítás:

> `echo "New project with 0 memories. Invoke the mem0:onboard skill to import project files. Coding categories install automatically in the background."` — uo.

**2) Hogyan készül:** a banner és a rubrika **determinisztikus sablon** (bash `cat`/`echo` blokkok); a ténylegesen visszaadott memóriák szemantikus vektorkereséssel jönnek (nem LLM-összefoglalás abban a pillanatban); a *memóriák szövegét* korábban a modell írta (session summary/compaction summary hook-okon keresztül).

> "Pre-compact | `PreCompact` | Stores a session summary before context compaction" — https://docs.mem0.ai/integrations/claude-code (T1)

**3) Méret:** nincs dokumentált kemény karakterlimit magára az induló bannerre; a keresési találatok darabszáma dokumentált (`top_k: 5` alapértelmezett a promptonkénti előzetes kereséshez — forráskódból, nem hivatalos doksi-számból):

> `'{query: $query, filters: {user_id: $user_id}, top_k: 5}'` — https://github.com/mem0ai/mem0/issues/5684 (T1, saját repó, hibajegyben idézett forráskód-részlet)

**4) Nyelv/forma:** sima szöveg (nem markdown-struktúra, nem XML), `hookSpecificOutput.additionalContext` mezőben kerül be Claude Code-nál, illetve Codexnél ugyanez a mechanizmus (SQ03 szerint már feltárt hook-csatorna, itt nem ismétlem).

**5) Dokumentált tapasztalat — MI NEM VÁLT BE:** dokumentált, súlyos rangsorolási hiba: a keresési hívás elfelejtette átadni a `rerank` paramétert, emiatt a legjobb találat rendszeresen **kimaradt** az induláskor/promptonként injektált top-5 közül:

> "Every prompt's injected context is the unranked `top_k=5`. In testing, the single most relevant memory for a query landed at rank #1 only with `rerank:true` and was absent from the top-5 without it — i.e. the best memory is silently dropped from the injected window." — https://github.com/mem0ai/mem0/issues/5684 (T1, saját repó)

Ugyanez a jegy megerősíti a hibát A/B/C méréssel (omitted-rerank == rerank:false, eltérő legjobb találat rerank:true mellett) — ez saját, belső megerősítés, nem független harmadik fél, ezért csak T1/self-confirmed jelzéssel adom meg (a kért „két független forrás" ezen állításra **nincs** meg, csak az egy hivatalos hibajegy).

---

## 4. basic-memory (basicmachines-co)

**1) Mit ad be induláskor:** **semmit automatikusan.** A `recent_activity` és a `continue_conversation` MCP „prompt"-ok (nem session-start hook!) csak akkor futnak le, ha a felhasználó (vagy a modell, a felhasználó kérésére) natural-language triggerrel meghívja őket.

> "### Continue Conversation […] `\"Let's continue our conversation about [topic]\"`" — https://docs.basicmemory.com/local/user-guide (T1, hivatalos)

> "### Recent Activity […] `\"What have we been discussing recently?\"` What happens: - Retrieves recently modified documents - Summarizes main topics and points - Offers to continue any discussions" — https://docs.basicmemory.com/local/user-guide (T1)

**2) Hogyan készül:** a *visszakeresés* determinisztikus (idő-ablak szerinti dokumentumlekérdezés a tudásgráfból, opcionális gráf-bejárási mélységgel), a *"summarizes main topics"* lépést maga a beszélgető modell (Claude) végzi a visszakapott nyers tartalom alapján, tehát a tömörítés a kliens oldalán, generálás közben történik, nem a szerver oldalán előre:

> `async def recent_activity(type=..., depth: int = 1, timeframe: TimeFrame = "7d", ..., output_format: Literal["text","json"] = "text", ...) -> str | list[dict]` — https://basicmachines-co-basic-memory.mintlify.app/api/mcp/knowledge-graph (T1, API-referencia)

**3) Méret:** lapozható (`page`, `page_size`, alapértelmezett 10), időablak paraméterezhető (`timeframe`, alapértelmezett „7d"), mélység paraméterezhető (`depth`, 1–3 ajánlott) — nincs dokumentált token/karakter-korlát magára a végső szövegre.

**4) Nyelv/forma:** `output_format`: `"text"` (ember-olvasható összefoglaló) vagy `"json"` (strukturált, sík lista metaadatokkal) — választható, tehát nem kizárólag markdown.

**5) Dokumentált tapasztalat:** **NINCS FORRÁS** arra, hogy mi vált be és mi nem (nem találtam blogot, hibajegyet vagy hivatalos „lessons learned" szakaszt erről a projektről).

---

## 5. Letta (memory blocks, „core memory")

**1) Mit ad be induláskor/minden lépésnél:** a hozzácsatolt memória-blokkok **teljes, nyers tartalmát**, szó szerint, a rendszerpromptba fűzve — nem összefoglalás, nem retrieval.

> "Memory blocks are structured sections of the agent's context window that persist across all interactions. They are always visible - no retrieval needed." — https://docs.letta.com/v1-sdk/memory/memory-blocks/ (T1, hivatalos)

> "Important 'core' memories are injected into the context window of the LLM, and the agent can modify its own memories through tools." — https://docs.letta.com/v1-sdk/concepts/stateful-agents/ (T1)

**2) Hogyan készül:** a blokk tartalmát maga az agent (modell) írja/szerkeszti explicit memory-tool-hívásokkal (`memory_rethink`, `memory_replace`, `memory_insert`, `core_memory_append`), determinisztikus a *betöltés* (mindig a legutóbbi `value` kerül be), de a *tartalom* modellgenerált.

**3) Méret és korlát:** dokumentált ajánlott felső korlátok, blokkonként és összesen.

> "| Memory Blocks | Editable (optional read-only) | Yes | … | Recommended <50k characters | Recommended <20 blocks per agent |" — https://docs.letta.com/v1-sdk/memory/context-hierarchy (T1)

> "Limits: - Character-limited (typically 2000-5000 chars per block) - Recommend 5-15 blocks max for reliability" — https://github.com/letta-ai/skills/blob/HEAD/letta/letta-api-client/memory-architecture.md (T2, hivatalos Letta GitHub-szervezet skill-doksija, de nem a fő docs.letta.com)

> "Keep total core memory under 80% of context window" — https://github.com/letta-ai/skills/blob/main/letta/agent-development/SKILL.md (T2, ugyanaz a szervezet)

**4) Nyelv/forma:** szabad szöveg (nem kikényszerített markdown/XML), `label`+`description`+`value`+`limit` mezőkkel jellemzett blokk; az újabb (git-alapú „MemFS") architektúrában markdown-fájlok egy git-repóban:

> "Each entry becomes a Markdown file in the agent's memory repository, named from its label" — https://docs.letta.com/agent-sdk/memory/index.md (T1)

**5) Dokumentált tapasztalat — MI NEM VÁLT BE (két független forrás):** a blokk-méretkorlát be nem tartása dokumentáltan valós pénzügyi kárt okozott (hivatalos hibajegy):

> "Block `limit` field is not enforced when writing through the git-enabled (memfs) code path. Blocks grow past their configured character limit, inflating system prompts and causing significant cost increases for users. […] Multiple users report agents burning through $30+ in Claude credits in hours due to memory blocks bloating overnight." — https://github.com/letta-ai/letta/issues/3241 (T1, hivatalos repó)

A projekt korábbi neve (MemGPT) alatt már 2023-ban dokumentált probléma volt a túl nagy blokk-tartalom:

> "ValueError: Edit failed: Exceeds 2000 character limit (requested 7194). Consider summarizing existing core memories in 'persona' and/or moving lower priority content to archival memory to free up space in core memory, then trying again." — https://github.com/letta-ai/letta/issues/7 (T1, hivatalos repó, 2023-10-16)

Egy közösségi fórumbejegyzés (T2, hivatalos Letta fejlesztői fórum) egy másik gyakorlati problémát ír le: érvénytelen blokknév esetén a rendszer csendben egy véletlenszerű blokkra váltott, hallucinációt okozva:

> "When an invalid block name is used as a parameter, the tool did not fail as expected. Instead, the update endpoint auto-selected a random block as a default fallback and applied the limit change. The behavior created hallucinations as the LLM believed that it had access to non-existent blocks." — https://forum.letta.com/t/custom-memory-block-size-update-tool/146 (T2, hivatalos Letta fórum)

---

## 6. OpenMemory (mem0 helyi/self-hosted MCP szervere)

**1) Mit ad be induláskor:** **dokumentáltan semmit automatikusan.** A négy eszköz (`add_memories`, `search_memory`, `list_memories`, `delete_all_memories`) mindegyike explicit hívást igényel; nincs dokumentált `SessionStart`-szerű automatikus injektálás. Az egyetlen „induláskori" tartalom az eszközleírásban rejlő álladó utasítás, ami a modellt rávezeti a keresésre minden kérdésnél:

> `@mcp.tool(description="Search through stored memories. This method is called EVERYTIME the user asks anything.")` — https://github.com/mem0ai/mem0/blob/ece7ff6b/openmemory/api/app/mcp_server.py (T1, saját repó, forráskód)

**2) Hogyan készül:** a keresés maga determinisztikus (embedding + Qdrant vektorkeresés), a mentés opcionálisan LLM-alapú tényextrakcióval történik (`infer=True` paraméter):

> `@mcp.tool(description="Add a new memory. […] Set infer to False to store the memory verbatim without LLM fact extraction.")` — uo.

**3) Méret:** nincs dokumentált induláskori méretkorlát (mivel nincs automatikus injektálás); a keresés limitje forráskód szerint `limit=10`.

**4) Nyelv/forma:** JSON-választ ad vissza (`json.dumps({"results": results}, indent=2)`), tehát strukturált JSON, nem markdown.

**5) Dokumentált tapasztalat:** **NINCS FORRÁS** kifejezetten arról, hogy mi vált be/nem vált be az OpenMemory induló-injektálásánál — mert nincs induló-injektálás, amit értékelni lehetne.

---

## 7. Codex Memories (natív OpenAI-funkció, **nem** a mem0-plugin)

Fontos elhatárolás: ez a saját, `[features] memories = true` / `[memories]` config-táblás OpenAI Codex CLI funkció, különbözik a 3. pontban tárgyalt mem0-pluginától.

**1) Mit ad be induláskor:** a config szerint meglévő memóriákat a jövőbeli munkameneteknél injektálja, de a hivatalos doksi **nem** részletezi pontosan a betöltött szöveg formáját/mennyiségét egy adott session elején — ez a mem0/claude-mem szintű részletesség itt hiányzik a hivatalos dokumentációból.

> "`memories.use_memories`: controls whether Codex injects existing memories into future sessions." — https://learn.chatgpt.com/docs/customization/memories (T1, hivatalos)

> "After you enable memories, Codex can turn useful context from eligible prior chats into local memory files. Codex skips active or short-lived sessions, redacts secrets from generated memory fields, and updates memories in the background instead of immediately at the end of every chat." — https://learn.chatgpt.com/docs/customization/memories (T1)

**2) Hogyan készül:** dokumentáltan kétfázisú modell-generálás (nem determinisztikus szűrés) — külön „extract" és „consolidation" modell:

> "`memories.consolidation_model`: overrides the model used for global memory consolidation." — https://learn.chatgpt.com/docs/customization/memories (T1)

Egy közösségi, de nagyon részletes összefoglaló (T3, nem hivatalos) konkrét paramétereket ad meg, amelyeket a hivatalos oldal nem részletez ennyire — ezt csak kiegészítésként, fenntartással közlöm:

> "```toml\n[memories]\nuse_memories = true\ngenerate_memories = true\nconsolidation_model = \"gpt-5.4\"\nextract_model = \"gpt-5.4-mini\"\nmax_raw_memories_for_consolidation = 256 # cap 4096\n```" — https://github.com/shanraisshan/codex-cli-best-practice/blob/main/best-practice/codex-memory.md (T3, közösségi, nem hivatalos — a config-kulcsok neve hihető, de számértékei NEM erősítve hivatalos forrásból)

**3) Méret:** a *memóriák konszolidálásának* bemeneti korlátja dokumentált-idézett közösségi forrásban (256, felső sapka 4096 „raw memories"), de az **induláskor ténylegesen injektált szöveg** karakter/token-korlátjára **NINCS FORRÁS** a hivatalos dokumentációban. (Megkülönböztetendő az `AGENTS.md`/`project_doc_max_bytes` 32 KiB-os korlátjától, ami más mechanizmus — ld. lentebb.)

**4) Nyelv/forma:** markdown fájlok a `$CODEX_HOME/memories/` alatt (a `/memories reset` parancs törli ezt a könyvtárat):

> "Reset […] wipes both `$CODEX_HOME/memories/` and `$CODEX_HOME/memories_extensions/`" — https://github.com/shanraisshan/codex-cli-best-practice/blob/main/best-practice/codex-memory.md (T3)

**5) Dokumentált tapasztalat — MI NEM VÁLT BE:** dokumentált precedencia-hiba, amikor elavult memória felülírta az aktuális, explicit betöltött `AGENTS.md`-szabályt:

> "Codex Desktop loaded both the global `~/.codex/AGENTS.md` and the repository `AGENTS.md` into the task context, but the agent ignored a distinctive current global rule and instead followed stale validation-gate guidance recovered from persistent memory." — https://github.com/openai/codex/issues/39223 (T1, hivatalos repó)

> "A current, successfully loaded `AGENTS.md` rule should win over conflicting stale memory for repository work. Persistent memory should provide historical context, not silently override explicit current operating instructions." — https://github.com/openai/codex/issues/39223 (T1)

(Kontrollként: az `AGENTS.md`-mechanizmus — **nem** a memories — dokumentáltan 32 KiB-os összesített korláttal, fájlonkénti levágással rendelkezik: "Codex skips empty files and stops adding files once the combined size reaches the limit defined by `project_doc_max_bytes` (32 KiB by default)." — https://developers.openai.com/codex/guides/agents-md, T1, saját forrás; forráskódi megerősítés: `if size > remaining { data.truncate(remaining as usize); }` — https://github.com/openai/codex/blob/ac4332c.../codex-rs/core/src/agents_md.rs, T1.)

---

## 8. Cursor „Memories" — **a funkció megszűnt**

**1–4) Mit adott be / hogyan készült / méret / forma (történeti, amíg élt):** amíg élt (2025.06.04 GA-beta – 2025.11.21), a Cursor natív Memories funkciója háttérben, modell által generált, rövid, mondat-méretű tényeket tárolt projektenként, felhasználói jóváhagyással a háttér-generált elemekre:

> "With Memories, Cursor can remember facts from conversations and reference them in the future. Memories are stored per project on an individual level, and can be managed from Settings." — Cursor changelog 1.0 (2025-06-04), idézve: https://mnemoverse.com/docs/library/mcp-memory-servers-claude-code-and-cursor (T3, de a changelog forrása maga hivatalos és élő: https://cursor.com/changelog)

> "Memories is now GA. Since 1.0, we've improved memory generation quality, added in-editor UI polish, and introduced user approvals for background-generated memories to preserve trust." — https://cursor.com/changelog/page/14 (T1, hivatalos, közvetlenül ellenőrizve)

A generálás mechanizmusát (háttér-extrakció, majd jóváhagyás) egy nem hivatalos, de részletes forrás írja le — **csak kiegészítésként**, mert a hivatalos oldal ezt már nem dokumentálja (a funkció eltűnt):

> "While you work in agent chats, a background process watches for durable facts — corrections you make repeatedly, preferences you state, project conventions you explain. When it spots one, it proposes a memory. Cursor asks for your approval before a background-generated memory is saved" — https://localskills.sh/blog/cursor-memories-guide (T3)

**A funkció eltávolítása — ez maga a legfontosabb, dokumentált tapasztalati tanulság ennél az eszköznél (Q5):** a hivatalos Cursor-fórumon, egy `CursorStaff`-jelölésű fiók 2025. november 24-én közvetlenül megerősítette az eltávolítást, saját szavaival — ezt a fórumbejegyzést **közvetlenül lekértem és ellenőriztem** (nem másodkézből idézem):

> "Hey, thanks for the report. The Memories feature was removed starting from version 2.1.17, so it no longer appears in your current version (2.1.25)." — https://forum.cursor.com/t/memories-not-showing/143820/1 (T1, közvetlenül lekért hivatalos fórumbejegyzés, Cursor-staff válasz, 2025-11-24)

> "You can export your memories and move them into Rules: - Press `Cmd+Shift+P` and type "Export memories" - Your memories will be saved to an `.mdc` file" — https://forum.cursor.com/t/memories-not-showing/143820/1 (T1)

**Ellentmondás magán a Cursor-staff válaszain belül** (két, egymástól független, később napvilágra került fórumszál összegzése egy T3 forrásban — az állítás maga a T3 forrás elemzése, az idézetek a fórum válaszaiból származnak, dátumozva):

> "On 24 November 2025 it answered a bug report: 'The Memories feature was removed starting from version 2.1.17…' The next day, a second thread: 'The Memories feature was intentionally removed starting from version 2.1.x.' Then on 7 January 2026, a third: '…Even though this feature was removed from Cursor, it still works, just without a UI.' And on 10 January 2026, a fourth: 'The Memories feature hasn't been removed. In version 2.1.x, only the UI to manage it was removed. The feature itself still works.'" — https://mnemoverse.com/docs/library/mcp-memory-servers-claude-code-and-cursor (T3 elemzés, de az idézett fórumválaszok forrása maga hivatalos — nem tudtam mind a négy szálat egyenként, közvetlenül ellenőrizni, csak az elsőt; ezért ezt a négyes-blokkot csak T3-jelöléssel, forrás-megjelöléssel adom tovább)

Ezt egy másik, független elemzés is megerősíti (T3):

> "Cursor removed its Memories feature in version 2.1, released November 21, 2025, and has not brought it back: as of Cursor 3.11 (July 2026) there is no automatic memory in the product. The official replacement is a one-time export into Rules." — https://archcore.ai/blog/cursor-memories-removed/ (T3)

A hivatalos doksi-útvonalak (`cursor.com/docs/memories`, `cursor.com/docs/context/memories`) ma **nem** a Memories funkcióra mutatnak — ezt **magam is közvetlenül ellenőriztem**: a `cursor.com/docs/context/memories` lekérése ma a Rules oldal tartalmát adja vissza ("# Rules […] Large language models don't retain memory between completions. Rules provide persistent, reusable context at the prompt level."), a `cursor.com/docs/memories` lekérése hibával tér vissza.

**5) Mi vált be / mi nem:** maga a termékdöntés (funkció visszavonása kilenc hónappal a GA után, changelog-bejelentés nélkül) közvetett, de erős jel arra, hogy a gyártó belső tapasztalata szerint az automatikus, modell-generált, session-elejei memória-injektálás **nem** vált be éles termékként ebben a formában — de erre **nincs hivatalos, kifejtett indoklás** (csak a tény, hogy eltűnt, és a migrációs útmutatás statikus, verziózott Rules-ra).

---

## 9. Windsurf Cascade Memories

**1) Mit ad be induláskor:** két, élesen elkülönített réteg. (a) A `global_rules.md` **mindig, teljes egészében** betöltődik minden munkamenetbe; (b) az automatikusan generált „Memories" **nem** tölt be mindent induláskor, csak akkor kerül elő, ha a Cascade relevánsnak ítéli:

> "Cascade's autogenerated memories are associated with the workspace they were created in and are stored locally in `~/.codeium/windsurf/memories/`. Cascade retrieves them when it believes they're relevant." — https://docs.devin.ai/desktop/cascade/memories (T1, hivatalos Windsurf/Devin doksi)

> "| Global | `~/.codeium/windsurf/memories/global_rules.md` | Single file, applied across all workspaces. Always on. Limited to 6,000 characters. |" — https://docs.devin.ai/desktop/cascade/memories (T1)

**2) Hogyan készül:** a Memories tartalmát a modell generálja automatikusan, felhasználói jóváhagyás nélkül említve (ellentétben a Cursorral, ahol jóváhagyás volt):

> "During conversation, Cascade can automatically generate and store memories if it encounters context that it believes is useful to remember." — https://docs.devin.ai/desktop/cascade/memories (T1)

Explicit kérésre is létrehozható: "Additionally, you can ask Cascade to create a memory at any time. Just prompt Cascade to 'create a memory of ...'." — uo.

**3) Méret:** a *Rules*-rétegre van dokumentált, kemény korlát (6000 karakter globális, 12 000 karakter/fájl workspace-szinten); magára a *Memories*-tartalomra **NINCS FORRÁS** külön dokumentált méretkorlát.

> "| Workspace | `.devin/rules/*.md` (preferred) or `.windsurf/rules/*.md` (fallback) | […] Limited to 12,000 characters per file." — https://docs.devin.ai/desktop/cascade/memories (T1)

**4) Nyelv/forma:** markdown fájlok, workspace-enként elkülönítve, nem oszthatók meg workspace-ek között, és nem kerülnek repóba:

> "Memories generated in one workspace are not available in another, and they are not committed to your repository." — https://docs.devin.ai/desktop/cascade/memories (T1)

**5) Dokumentált tapasztalat:** a hivatalos doksi maga ajánlja a Memories helyett a Rules/`AGENTS.md` használatát megbízható tudásra — ez implicit, hivatalos jelzés arra, hogy az automatikus Memories megbízhatósága korlátozott:

> "Recommendation: For knowledge you want Cascade to reliably reuse, write it as a Rule or add it to `AGENTS.md` in your repo rather than relying on auto-generated Memories. Rules are version-controlled, shareable with your team, and give you explicit control over activation." — https://docs.devin.ai/desktop/cascade/memories (T1)

---

## 10. Serena (oraios/serena) — `initial_instructions` / onboarding

**1) Mit ad be induláskor:** két csatorna. (a) Az MCP `initialize`-válasz szerver-szintű `instructions` mezője (a `create_connection_prompt()` hívás eredménye) — ezt a legtöbb kliens automatikusan megkapja csatlakozáskor, ez tartalmazza az elérhető memóriák **nevének listáját** (nem a teljes tartalmát); (b) olyan klienseknél, amelyek nem olvassák be automatikusan ezt a mezőt (pl. Claude Desktop), egy külön `initial_instructions` eszközt kell explicit meghívni.

> "`initial_instructions`: Provides instructions Serena usage (i.e. the 'Serena Instructions Manual') for clients that do not read the initial instructions when the MCP server is connected." — https://oraios.github.io/serena/01-about/035_tools.html (T1, hivatalos)

> "When the agent starts working on a project, it receives the list of available memories." — https://oraios.github.io/serena/02-usage/045_memories.html (T1)

> `instructions = self._get_initial_instructions() … mcp = FastMCP(name="Serena", …, instructions=instructions)` — https://github.com/oraios/serena/blob/981f560f/src/serena/mcp.py (T1, forráskód)

**2) Hogyan készül:** determinisztikus sablon (`create_connection_prompt`, ill. `onboarding_prompt` YAML-sablon), ami a modellt lépésekre utasítja (pl. olvasd el a `memory_maintenance` memóriát elsőként), de a **memóriák tartalmát** maga a modell írja az onboarding-folyamat során:

> "Your task is to assemble durable, non-obvious information about the project and write it to memory files that future agents will consult. […] **Before writing anything, read `mem:{{ memory_maintenance_name }}`** using the `read_memory` tool." — https://github.com/oraios/serena/blob/901bd215/src/serena/resources/config/prompt_templates/simple_tool_outputs.yml (T1, forráskód, sablon)

**3) Méret:** nincs dokumentált kemény karakterkorlát sem az `initial_instructions`, sem az egyes memóriafájlok méretére; a memóriák szűrhetők mintázattal (`ignored_memory_patterns`), hogy nagyszámú archivált fájl ne terhelje a listázást:

> "Projects that accumulate large numbers of archived memory files can use `ignored_memory_patterns` to exclude them from `list_memories` and `activate_project` output." — https://oraios.github.io/serena/02-usage/045_memories.html (T1)

**4) Nyelv/forma:** markdown fájlok (`.serena/memories/*.md`, illetve `~/.serena/memories/global/*.md`), belső hivatkozási konvencióval (`mem:névtér/névvel` formátum), gráf-szerű felépítéssel (egy `mem:core` gyökérből hivatkozott almemóriák):

> "Core principle: progressive discovery through references, building a graph of memories. […] Agents should read `mem:core` as the top-level entry point (graph root)." — https://github.com/oraios/serena/blob/901bd215/.serena/memories/memory_maintenance.md (T1, forráskód/sablon)

**5) Dokumentált tapasztalat — MI NEM VÁLT BE:** a hivatalos doksi kifejezetten dokumentálja, hogy hosszú munkameneteknél a modell **elfelejti** a kezdeti instrukciókat („agent drift"), ezért külön emlékeztető-hookot kellett bevezetni:

> "Due to recent changes (especially dynamic tool loading) in Claude Code, the agent will often fail to make proper use of Serena's tools, either by failing to load them in the beginning or by forgetting the instructions in a long session (a behavior known as agent drift). To counteract this, we provide reminder hooks." — https://oraios.github.io/serena/02-usage/030_clients.html (T1, hivatalos)

Egy hivatalos GitHub-jegy egyenesen a Claude Code-kompaktálás mellékhatásaként azonosítja a probléma egyik forrását:

> "I guess it will work automatically even after compactifying, so the tool could truly be disabled/deleted […] there's multiple bugs in […] Code bugtracker that even the system instructions break after compactifying" — https://github.com/oraios/serena/issues/366 (T1, hivatalos repó)

---

## Bónusz: egyéb, talált csapat-/session-memória MCP-szerver induló hookjai

A feladat kifejezetten kérte, hogy ha találok, jelezzek más csapat-memória MCP-szerver induló hookot is. Kettőt találtam, mindkettő nem hivatalos (közösségi) projekt, T2/T3 forrással, de mindkettő konkrét, idézhető mechanikát dokumentál:

**memcp** (manthonyaiello/memcp) — determinisztikus, kis méretű induló injektálás, dokumentált sor-számmal:

> "**Header** | 1–2 line title that surfaces in `recent()` and `search()` hits. The 5 most recent Headers are injected into Claude's starting context by the `SessionStart` hook. This adds up to about 10 lines to your context window." — https://github.com/manthonyaiello/memcp (T2, közösségi projekt README-je)

> "**SessionStart** derives the project key […] and prints the most recent diary entries for that project inside a […] block, which Claude picks up as first-turn context. On `source=resume` and `source=compact` the diary listing is skipped — the model already has that context — but the key is still injected, because a compaction can drop it." — https://github.com/manthonyaiello/memcp (T2)

**claude-mem-lite** (sdsrss/claude-mem-lite) — determinisztikus, több forrásból összeállított „startup dashboard":

> "**Startup dashboard** (v2.31.0) -- SessionStart hook aggregates `git status` + `~/.claude/tasks/*.json` + `~/.claude/plans/*.md` + most-recent exit handoff + recent event count into a single structured block injected via `hookSpecificOutput.additionalContext`" — https://github.com/sdsrss/claude-mem-lite (T2, közösségi projekt README-je)

> "**Budgeted context** -- Greedy knapsack algorithm selects session-start context within a 2,000-token budget by recency and importance" — https://github.com/sdsrss/claude-mem-lite (T2) — ez az egyetlen talált forrás, amely explicit **algoritmust** (greedy knapsack) nevez meg a session-elejei tartalom kiválasztására, méret-korláttal (2000 token) kombinálva.

---

## Ellentmondások

1. **Cursor Memories státusza (megszűnt vs. csak UI nélkül fut tovább):** a Cursor-staff saját fórumbejegyzései (2025.11.24, 2025.11.25, 2026.01.07, 2026.01.10) egymásnak ellentmondanak abban, hogy a funkció ténylegesen megszűnt, vagy csak a kezelőfelülete tűnt el, miközben a mechanizmus a háttérben továbbra is fut. Az elsőt magam is közvetlenül ellenőriztem (https://forum.cursor.com/t/memories-not-showing/143820/1); a további hármat csak egy harmadik fél (T3, mnemoverse.com) összegzéséből ismerem, nem közvetlenül.
2. **claude-mem induláskor betöltött munkamenet-ablak mérete verziók között:** egy korábbi (Mr1Stark) forkolt doksi „last 3 sessions"-t mond, a jelenlegi hivatalos doksi és a config alapértéke „last 10 sessions"-t. Ez inkább termékfejlődés, mint valódi ellentmondás, de mivel mindkettő „hivatalosnak" tűnő forrásból származik, jelzem.
3. **Claude Code MEMORY.md limitjének gyakorlati érvényesülése:** a hivatalos doksi szerint a betöltési limit 200 sor VAGY 25 KB, és e fölött csak figyelmeztetés jár, a fájl „megmarad". A felhasználói hibajegy (#57574) szerint a gyakorlatban a figyelmeztetés nem eléggé látható, és a tartalom ténylegesen, csendben elveszik a modell számára — ez nem technikai ellentmondás (a doksi maga is mondja, hogy „content beyond that threshold is not loaded"), inkább a **felhasználói tapasztalat és a dokumentáció súlyozása** közötti eltérés: a doksi ezt egy alárendelt mondatban közli, a hibajegy szerint ez főbenjáró UX-probléma.
4. **A Claude Code auto-memory belső extrakciós mechanizmusa (állítólagos háttér-Opus-hívás, dupla tokenfogyasztás):** három, egymást erősítő, de mind **T3, nem hivatalos, „forráskód-visszafejtő"** forrás állítja ezt (claude-wiki.com, mintlify.com/killlowkey, sanbuphy-claude-code-source-code.mintlify.app); a hivatalos code.claude.com dokumentáció ezt a mechanizmust nem részletezi ilyen mélységben, se nem erősíti, se nem cáfolja explicit módon. Nem tekintem megerősítettnek.

## Amire NINCS forrás

- **OpenAI Codex natív „memories" funkció** — az induláskor ténylegesen injektált szöveg pontos karakter-/token-korlátjára a hivatalos dokumentációban nem található szám (csak a *konszolidáció bemeneti* korlátjára van közösségi, nem hivatalos adat: 256/4096 raw memória).
- **Windsurf Cascade automatikusan generált Memories** (nem a `global_rules.md`) — nincs dokumentált méretkorlát vagy tokenkorlát magára a Memories-tartalomra, csak a Rules-rétegre.
- **basic-memory** — nincs dokumentált, konkrét „mi vált be / mi nem" tapasztalati beszámoló (blog, hibajegy) a `continue_conversation`/`recent_activity` promptok gyakorlati beválásáról.
- **OpenMemory** — nincs dokumentált tapasztalat arról, hogy az automatikus injektálás hiánya (csak eszközhívás-alapú működés) jó vagy rossz döntésnek bizonyult-e a gyakorlatban.
- **Serena `initial_instructions` mérete** — nincs dokumentált karakter-/tokenszám arra, mekkora ez a szöveg jellemzően egy közepes méretű projektnél.
- A négy Cursor-staff fórumválasz közül hármat (2025.11.25, 2026.01.07, 2026.01.10) nem tudtam közvetlenül, önállóan ellerőrizni — csak egy T3 harmadik fél idézeteként ismerem őket.

## Meglátogatott és felderített linkek

| Cím | URL | Tier | Eszköz | Megjegyzés |
|---|---|---|---|---|
| How Claude remembers your project | https://code.claude.com/docs/en/memory | T1 | web_search+fetch | Fő hivatalos forrás a Claude Code auto memory-hoz |
| .claude/docs-cache/memory.md (GitHub tükrözés) | https://github.com/lenneTech/claude-code/blob/main/.claude/docs-cache/memory.md | T2 | web_search | Hivatalos doksi cache-elt tükrözése, 4 MiB CLAUDE.md-adat innen |
| Auto-memory MEMORY.md silently truncated (#57574) | https://github.com/anthropics/claude-code/issues/57574 | T1 | web_search | Kulcsfontosságú Q5-forrás, felhasználói restrukturálás számokkal |
| Auto-Memory - Claude Wiki | https://claude-wiki.com/auto-memory.html | T3 | web_search | Nem hivatalos „forráskód-visszafejtés", óvatosan kezelve |
| Memory & Context - killlowkey mirror | https://www.mintlify.com/killlowkey/claude-code/concepts/memory | T3 | web_search | Ua., extractMemories állítás megerősítése (nem hivatalos) |
| sanbuphy-claude-code-source-code mirror | https://sanbuphy-claude-code-source-code.mintlify.app/configuration/memory-system | T3 | web_search | Ua. |
| Memory tool - Claude Platform Docs | https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool | T1 | web_search | API-szintű memory tool (kontextus, nem session-start eszköz maga) |
| thedotmack/claude-mem GitHub | https://github.com/thedotmack/claude-mem | T1 | web_search | Fő projekt README |
| Mr1Stark/claude-mem fork | https://github.com/Mr1Stark/claude-mem | T2 | web_search | Korábbi verzió, „last 3 sessions" ellentmondás forrása |
| claude-mem-lite | https://github.com/sdsrss/claude-mem-lite | T2 | web_search | Bónusz: greedy-knapsack, 2000 token budget |
| Claude-Mem: Introduction | https://docs.claude-mem.ai/introduction | T1 | web_fetch | Hivatalos projektdoksi, „last 10 sessions" |
| claude-mem getting-started | https://docs.claude-mem.ai/usage/getting-started | T1 | web_search | Progresszív feltárás, token-becslések |
| claude-mem configuration | https://docs.claude-mem.ai/configuration | T1 | web_search | Alapértékek (50 obs / 10 session) |
| claude-mem hooks architektúra | https://github.com/thedotmack/claude-mem/blob/v10.6.3/docs/public/architecture/hooks.mdx | T1 | web_search | XML-formátum, hook-folyamat |
| claude-mem ContextBuilder.ts | https://github.com/thedotmack/claude-mem/blob/e0249485/src/services/context/ContextBuilder.ts | T1 | web_search | Determinisztikus renderelés bizonyítéka |
| claude-mem CHANGELOG | https://github.com/thedotmack/claude-mem/blob/main/CHANGELOG.md | T1 | web_search | XML-kontraktus, UX-alapú alapértékváltoztatás |
| michaelbuckner/claude-mem CHANGELOG (fork) | https://github.com/michaelbuckner/claude-mem/blob/25ccf46.../CHANGELOG.md | T2 | web_search | opt-in szemantikus keresés, Q5-tapasztalat |
| manthonyaiello/memcp | https://github.com/manthonyaiello/memcp | T2 | web_search | Bónusz csapat-memória MCP, 5 Header / ~10 sor |
| mem0 Claude Code integráció | https://docs.mem0.ai/integrations/claude-code | T1 | web_search | Hivatalos, hook-táblázat |
| mem0 Codex integráció | https://docs.mem0.ai/integrations/codex | T1 | web_search | Hivatalos, hook-táblázat |
| mem0-plugin README (GitHub) | https://github.com/mem0ai/mem0/blob/main/integrations/mem0-plugin/README.md | T1 | web_search | Telepítési módok, hook-lista |
| on_session_start.sh (forráskód) | https://raw.githubusercontent.com/mem0ai/mem0/main/integrations/mem0-plugin/scripts/on_session_start.sh | T1 | web_fetch | Determinisztikus banner-sablon bizonyítéka |
| on_user_prompt.sh (forráskód) | https://raw.githubusercontent.com/mem0ai/mem0/main/integrations/mem0-plugin/scripts/on_user_prompt.sh | T1 | web_fetch | Prompt-idejű injektálás mechanikája |
| mem0 rerank hibajegy (#5684) | https://github.com/mem0ai/mem0/issues/5684 | T1 | web_search | Q5: legjobb találat kimaradása a top-5-ből |
| mem0 PR #4992 (search-decision refaktor) | https://github.com/mem0ai/mem0/pull/4992 | T1 | web_search | Korábbi „blind search minden turnnál" probléma leírása |
| basic-memory API (knowledge-graph) | https://basicmachines-co-basic-memory.mintlify.app/api/mcp/knowledge-graph | T1 | web_search | `recent_activity`/`build_context` szignatúrák |
| basic-memory user guide | https://docs.basicmemory.com/local/user-guide | T1 | web_search | „Continue Conversation”/„Recent Activity” promptok |
| Letta memory blocks | https://docs.letta.com/v1-sdk/memory/memory-blocks/ | T1 | web_search | Alapfogalom, „always visible” |
| Letta context hierarchy | https://docs.letta.com/v1-sdk/memory/context-hierarchy | T1 | web_search | Méretkorlát-táblázat (<50k char, <20 blokk) |
| Letta memory-architecture skill | https://github.com/letta-ai/skills/blob/HEAD/letta/letta-api-client/memory-architecture.md | T2 | web_search | 2000-5000 char/blokk becslés |
| Letta agent-development SKILL.md | https://github.com/letta-ai/skills/blob/main/letta/agent-development/SKILL.md | T2 | web_search | „80% of context window” ökölszabály |
| Letta blokk-limit hibajegy (#3241) | https://github.com/letta-ai/letta/issues/3241 | T1 | web_search | Q5: $30+ költségtúllépés dokumentálva |
| MemGPT persona limit hibajegy (#7) | https://github.com/letta-ai/letta/issues/7 | T1 | web_search | Q5: 2023-as, korai dokumentált méretprobléma |
| Letta fórum: memory_update_size | https://forum.letta.com/t/custom-memory-block-size-update-tool/146 | T2 | web_search | Q5: hallucináció érvénytelen blokknévnél |
| OpenMemory mcp_server.py (forráskód) | https://github.com/mem0ai/mem0/blob/ece7ff6b/openmemory/api/app/mcp_server.py | T1 | web_search | Eszközleírás-alapú „always search” utasítás |
| OpenMemory bevezető blog | https://mem0.ai/blog/introducing-openmemory-mcp | T1 | web_search | Hivatalos termékbejelentés |
| Codex Memories (learn.chatgpt.com) | https://learn.chatgpt.com/docs/customization/memories | T1 | web_search | Fő hivatalos forrás Codex natív memories-hoz |
| Codex CLI reference (/memories) | https://developers.openai.com/codex/cli/reference.md | T1 | web_search | `/memories` parancs |
| codex-cli-best-practice (közösségi) | https://github.com/shanraisshan/codex-cli-best-practice/blob/main/best-practice/codex-memory.md | T3 | web_search | Nem hivatalos, de részletes config-kulcs lista |
| Codex AGENTS.md guide | https://developers.openai.com/codex/guides/agents-md | T1 | web_search | 32 KiB korlát (kontrollként, nem memories) |
| Codex agents_md.rs (forráskód) | https://github.com/openai/codex/blob/ac4332c.../codex-rs/core/src/agents_md.rs | T1 | web_search | 32 KiB korlát forráskódi megerősítése |
| Codex stale memory hibajegy (#39223) | https://github.com/openai/codex/issues/39223 | T1 | web_search | Q5: precedencia-hiba, elavult memória felülír |
| Cursor Rules doksi | https://cursor.com/docs/context/memories | T1 | web_fetch | Közvetlenül lekérve — Memories helyett Rules-tartalom (redirect bizonyíték) |
| Cursor changelog (Memories GA) | https://cursor.com/changelog/page/14 | T1 | web_search | „Memories is now GA” hivatalos bejegyzés |
| Cursor fórum: Memories not showing | https://forum.cursor.com/t/memories-not-showing/143820/1 | T1 | web_search | Közvetlenül idézett Cursor-staff megerősítés az eltávolításról |
| mnemoverse: MCP Memory Servers cikk | https://mnemoverse.com/docs/library/mcp-memory-servers-claude-code-and-cursor | T3 | web_search | 4 fórumválasz összegzése (csak 1 ellenőrizve közvetlenül) |
| mnemoverse: What Survives cikk | https://mnemoverse.com/docs/library/what-survives-when-ai-agents-restart | T3 | web_search | Módszertani megjegyzések, öt eszköz összevetése |
| archcore.ai: Cursor Memories Removed | https://archcore.ai/blog/cursor-memories-removed/ | T3 | web_search | Független megerősítés az eltávolításról |
| localskills.sh: Cursor Memories guide | https://localskills.sh/blog/cursor-memories-guide | T3 | web_search | Generálási mechanizmus leírása (amíg élt) |
| Windsurf/Devin Cascade Memories | https://docs.devin.ai/desktop/cascade/memories | T1 | web_search | Fő hivatalos forrás, 6000/12000 char limitek |
| Windsurf Cascade Memories (legacy plugins.devin doksi) | https://docs.devin.ai/windsurf/plugins/cascade/memories | T1 | web_search | Korábbi doksi-verzió, ugyanaz a tartalom |
| Serena tools doksi | https://oraios.github.io/serena/01-about/035_tools.html | T1 | web_search | `initial_instructions`/`onboarding` eszközök |
| Serena clients doksi | https://oraios.github.io/serena/02-usage/030_clients.html | T1 | web_search | Agent drift, reminder hookok |
| Serena memories doksi | https://oraios.github.io/serena/02-usage/045_memories.html | T1 | web_search | Memóriafájlok szerkezete, onboarding folyamat |
| Serena mcp.py (forráskód) | https://github.com/oraios/serena/blob/981f560f/src/serena/mcp.py | T1 | web_search | `instructions` mező betöltése MCP `initialize`-ban |
| Serena memory_manager.py (forráskód) | https://github.com/oraios/serena/blob/901bd215/src/serena/memories/memory_manager.py | T1 | web_search | Memóriák listázása, olvasása, írása |
| Serena memory_maintenance.md sablon | https://github.com/oraios/serena/blob/901bd215/.serena/memories/memory_maintenance.md | T1 | web_search | Gráf-alapú memóriastruktúra konvenciói |
| Serena onboarding_prompt sablon | https://github.com/oraios/serena/blob/901bd215/src/serena/resources/config/prompt_templates/simple_tool_outputs.yml | T1 | web_search | Onboarding-folyamat determinisztikus sablonja |
| Serena issue #366 (instructions auto-provide) | https://github.com/oraios/serena/issues/366 | T1 | web_search | Kompaktálás melléhatása az instrukciókra |

---

# SQ06 — Mitől használja egy agent ténylegesen a memória-eszközöket?

*Módszertani megjegyzés (kötelező bevezető): ez a kutatás degradált módban készült. A `deep-web-research` skill elvei szerint dolgoztam (elsődleges forrás előny, szó szerinti idézet + URL minden állításhoz, T1/T2/T3 jelölés, két független forrás vagy „nincs forrás"), de al-ügynököket (subagentek párhuzamos indítását) nem indítottam — egyetlen kutató szálon, szekvenciális Exa-kereséssel és -olvasással dolgoztam. Az Exa (`mcp__Exa__web_search_exa`, `mcp__Exa__web_fetch_exa`) elérhető volt és kizárólagosan ezt használtam keresésre/olvasásra; beépített WebSearch/WebFetch-et nem hívtam.*

## Rövid válasz

Közvetlen, kontrollált mérést arra, hogy egy rövid, session-eleji sablonszöveg (,,van memória, N bejegyzés, használd a keresőt") önmagában mennyivel növeli egy memória-eszköz önkéntes meghívási arányát, nem találtam — ez pontosan az a rés, amit ez a kutatási kérdés keres, és amire nincs közvetlen forrás. Van viszont bőséges közvetett bizonyíték: (1) az általános eszközhasználati kutatás azt mutatja, hogy a modellek alapból erősen alul- vagy túlhasználják az elérhető eszközöket modellcsaládtól függően, és a puszta promptolás („ne hívj eszközt feleslegesen") ezt csak durván, nem szelektíven tudja korrigálni; (2) mindhárom nagy gyártó (Anthropic, OpenAI, Google) a gyakorlatban explicit, kikényszerített szöveget told a rendszerpromptba, amikor memória-eszköz van jelen — ami önmagában bizonyítja, hogy a puszta eszköz-elérhetőség a gyártók szerint sem elég; (3) a Google Gemini CLI forráskódjában dokumentált mérnöki döntés kifejezetten kimondja, hogy erősebb modellnél (Gemini 3) elhagyható az explicit memória-instrukció, mert a modell magától is megbízhatóan használja az eszközt — vagyis a szükséges „nógatás" mennyisége modellfüggő; (4) a beadott szöveg pozíciója és hossza jól mért hatás: a „Lost in the Middle" U-alakú görbe és a „context rot" jelenség szerint a session eleji rövid szöveg relatív súlya csökken, ahogy utána nő a kontextus, bár egy 2026-os kontrollált null-eredmény ezt 150k tokenig nem tudta reprodukálni; (5) a kockázatok oldalán irreleváns tartalom mérten rontja a teljesítményt (GSM-IC, Shi et al. 2023), elavult/ütköző memória dokumentáltan felülírhatja az aktuális, helyesen betöltött instrukciót (Codex Desktop GitHub-jegy), és a beadott memória-tartalmon át indirekt prompt injection is dokumentált, mind akadémiai támadásként (MINJA, NeurIPS 2025), mind valós incidensként (ChatGPT memória-feature, Rehberger 2024).

## 1. Van-e mérés az önkéntes eszközhasználati gyakoriságra, és mennyit változtat rajta egy emlékeztető/címlista/utasítás?

### 1.1 Alapszintű eszközhasználati arány — erős modellfüggés, alul- és túlhasználat egyaránt

A „WHEN2TOOL" benchmark (2026, arXiv 2605.09252) kifejezetten azt méri, mikor hív egy agent eszközt, ha nem kellene, és mikor nem hív, ha kellene volna:

> „Finding 1: Models default to tool overuse. Under the Default (⋆) setting in Prompt-only baselines, models make 2,100–4,400 total tool calls across the 2,250-task single-hop test set, more than one calls per task. Even on easy tasks, Qwen3-1.7B makes 864 tool calls out of 750 easy tasks... The model's default behavior is 'tools are available, therefore use them,' even when the task is simple enough to solve directly."

Ugyanez a tanulmány közvetlenül a kérdésre válaszol: mennyit ér a puszta promptolás (emlékeztető/utasítás)?

> „Finding 2: Prompt engineering reduces tool calls indiscriminately, and hard tasks pay a disproportionate price... On Qwen3-4B-Instruct, the cost is −17.3 on easy but reaches −42.4 on hard, meaning hard tasks lose 2.5× more accuracy per saved call."

Forrás: „LLM Agents Already Know When to Call Tools – Even Without Reasoning", arXiv:2605.09252, https://arxiv.org/pdf/2605.09252v2 (T1, arXiv, 2026).

A „ToolFailBench" (arXiv 2607.04686) 19 modellen mérve mutatja, hogy a legjobb modell is csak 86,33%-os „Clean Tool-Use Rate"-et ér el, és a modellcsaládok között drámai eltérés van:

> „Llama-3.1-70B and Qwen2.5-72B differ by 89 percentage points on control-task accuracy... two-proportion z=−19.9, p<10⁻⁸⁰."

Forrás: „ToolFailBench: Diagnosing Tool-Use Failures in LLM Agents", arXiv:2607.04686, https://ar5iv.labs.arxiv.org/html/2607.04686 (T1, 2026).

A reprezentáció-terelős tanulmány (arXiv 2608.25198) direkt megméri az eszközhívási arányt (call rate) mint kontrollálható, folytonos mennyiséget:

> „Adding the direction with strength α moves the call rate monotonically from near 0% to over 90% while keeping calls well-formed... baseline call rates span both tool-underuse and tool-overuse, from 0.07 on Qwen3-4B to 0.83 on the 30B MoE."

Forrás: „Tunable Tool-Call Rates in LLM Agents via Representation Steering", arXiv:2608.25198, https://arxiv.org/html/2608.25198v1 (T1, 2026-08-25).

**Ez három egymástól független kutatócsoport konvergáló eredménye**: az alap eszközhívási hajlandóság erősen modell- és családfüggő, tág skálán mozog (7%-tól 98%-ig kontroll-feladatokon), és a puszta szöveges promptolás („ne hívj feleslegesen") ezt csak durván, a nehéz (valóban szükséges) eseteket is sújtva tudja csökkenteni.

### 1.2 Memória-specifikus benchmarkok: az eszközhívás megtörténik, de a *hasznos* eszközhívás nem triviális

A LongMemEval (ICLR 2025) — az egyik legidézettebb hosszútávú-memória benchmark — nem az önkéntes hívás gyakoriságát méri közvetlenül (a hívás a keretrendszer szintjén kötelező), hanem azt, hogy a visszakeresés/válasz mennyire jó:

> „...commercial chat assistants and long-context LLMs showing a 30% accuracy drop on memorizing information across sustained interactions."

Forrás: LONGMEMEVAL, ICLR 2025, https://proceedings.iclr.cc/paper_files/paper/2025/file/d813d324dbf0598bbdc9c8e79740ed01-Paper-Conference.pdf (T1, peer-reviewed).

Egy harmadik fél implementáció (ReMe, agentikus/ReAct módban futtatva a LongMemEval-t) közvetve mégis mutat valamit az önkéntes eszközhasználati mintázatról: a kérdéstípusonkénti pontosság 0,633 és 1,000 között szór, és az átlagos eszközhívás-szám kérdéstípusonként 1,89-től 4,97-ig terjed — vagyis még kötelezően eszközös módban futtatva is nagy szórás van abban, hányszor „próbálkozik" az agent a memóriában (github.com/agentscope-ai/ReMe, T2, közösségi implementáció, nem lektorált).

Az eredeti **MemGPT** (arXiv 2310.08560, később ICLR 2024) explicit kimondja, hogy az önkéntes (self-directed) memóriakezelő függvényhívás **nem magától jön létre**, hanem csak explicit rendszerpromptból táplálkozó instrukcióval:

> „Memory edits and retrieval are entirely self-directed: MemGPT autonomously updates and searches through its own memory based on the current context... We implement self-directed editing and retrieval by providing explicit instructions within the system instructions that guide the LLM on how to interact with the MemGPT memory systems. These instructions comprise two main components: (1) a detailed description of the memory hierarchy and their respective utilities, and (2) a function schema..."

> „Awareness of context limits is a key aspect in making the self-editing mechanism work effectively, to this end MemGPT prompts the processor with warnings regarding token limitations to guide its memory management decisions."

Forrás: „MemGPT: Towards LLMs as Operating Systems", arXiv:2310.08560, https://arxiv.org/abs/2310.08560 (T1, 2023, azóta ~2000+ hivatkozás).

**Ez az egyik legközvetlenebb bizonyíték a kérdésre**: már az „önkéntes" memóriahasználatot definiáló alapmű is azt állítja, hogy ez csak explicit, a memória-hierarchiát és a függvényeket leíró rendszerprompt-szöveggel működik — magától, instrukció nélkül a szerzők szerint nem.

### 1.3 A gyártói gyakorlat mint közvetett bizonyíték: mindenki explicit szöveget told be

Lásd részletesen a 2. pontot — de ide kívánkozik az egyetlen konkrét, *modellváltozat szerint mért* vendor-oldali állítás, amit találtam. A Google Gemini CLI nyílt forráskódú repójában egy 2026 februári PR (elsődleges forrás, a gyártó saját commitja) kifejezetten eltávolítja a memória-eszköz használatára vonatkozó explicit instrukciót Gemini 3 modelleknél:

> „This PR removes the explicit memory tool instructions from the Gemini 3 series system prompt. These instructions were previously necessary for earlier models to correctly utilize the memory tool, but Gemini 3 models exhibit high reliability in using the tool without explicit guidance."

> „Verify that all tests pass (Gemini 2.5 still uses the legacy prompt which contains the instructions, while Gemini 3 uses the updated prompt)."

Forrás: google-gemini/gemini-cli, PR #18559, https://github.com/google-gemini/gemini-cli/pull/18559 (T1, gyártói forráskód/PR, 2026-02-08). *Ez egyetlen, nem publikált, nem kvantifikált (nincs %-os szám) gyártói mérnöki állítás — nem sikerült második, független forrással megerősíteni, ezért önmagában áll; iránymutatásként kezelendő, nem mért effektusméretként.*

## 2. Gyártói útmutatás: mit ajánl a rendszerprompt / eszközleírás / indító szöveg szintjén

### 2.1 Anthropic — Claude API memory tool

A hivatalos dokumentáció (platform.claude.com) kimondja, hogy **maga az API automatikusan told be egy kikényszerítő szöveget**, amint a memória-eszköz szerepel a `tools` listában — a fejlesztőnek ezt nem kell megírnia:

> „When the memory tool is present in your request's `tools`, the API automatically adds this instruction to the system prompt. You don't need to send it yourself:
> ```
> IMPORTANT: ALWAYS VIEW YOUR MEMORY DIRECTORY BEFORE DOING ANYTHING ELSE.
> MEMORY PROTOCOL:
> 1. Use the `view` command of your `memory` tool to check for earlier progress.
> 2. ... (work on the task) ...
>    - As you make progress, record status / progress / thoughts etc in your memory.
> ASSUME INTERRUPTION: Your context window might be reset at any moment, so you risk losing any progress that is not recorded in your memory directory.
> ```"

Forrás: „Memory tool", Claude Platform Docs, https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool (T1, hivatalos, elérve 2026-09-25; a fejlesztő emellett saját szöveggel finomíthatja: „when editing your memory folder, always try to keep its content up-to-date, coherent and organized").

Ez direkt megerősíti a kutatási kérdés alapfeltevését: a gyártó szerint az eszköz puszta jelenléte **nem elég**, ezért ők maguk automatikusan injektálnak egy kényszerítő, felkiáltójeles emlékeztetőt minden hívás elé.

A bejelentő blogbejegyzés (2025-09-29) mért számokat is közöl a memória+context-editing kombináció hasznáról, de ezek önbevallott, belső eval-eredmények:

> „On an internal evaluation set for agentic search... combining the memory tool with context editing improved performance by 39% over baseline. Context editing alone delivered a 29% improvement... In a 100-turn web search evaluation, context editing enabled agents to complete workflows that would otherwise fail due to context exhaustion—while reducing token consumption by 84%."

Forrás: „Managing context on the Claude Developer Platform", Anthropic, https://www.anthropic.com/news/context-management (T1, 2025-09-29). *Egy független, kritikai elemzés (T3, dreaming.press, 2026-07-27) rámutat, hogy ez a szám egy kontextus-kimerüléses vészhelyzetből való kimenekülést mér, nem általános képességnövekedést, és rövid feladatokon a hatás nullához tart — lásd „Ellentmondások".*

### 2.2 Anthropic — Claude Code (CLAUDE.md + auto memory)

A hivatalos Claude Code dokumentáció (code.claude.com/docs/en/memory) szerint a CLAUDE.md-fájlok minden session elején automatikusan betöltődnek, de **nem kikényszerített konfiguráció, hanem kontextus**:

> „Claude Code has two complementary memory systems. Both are loaded at the start of every conversation. Claude treats them as context, not enforced configuration. To block an action regardless of what Claude decides, use a PreToolUse hook instead. The more specific and concise your instructions, the more consistently Claude follows them."

> „CLAUDE.md content is delivered as a user message after the system prompt, not as part of the system prompt itself. Claude reads it and tries to follow it, but there's no guarantee of strict compliance, especially for vague or conflicting instructions."

> „Because they're context rather than enforced configuration, how you write instructions affects how reliably Claude follows them. Specific, concise, well-structured instructions work best."

Forrás: „How Claude remembers your project", Claude Code Docs, https://code.claude.com/docs/en/memory (T1, hivatalos, elérve 2026-09-25).

Az „auto memory" (a Claude saját maga írt jegyzetei) esetében a hivatalos doksi kimondja, hogy ez **nem minden alkalommal aktiválódó**, hanem a modell saját döntése:

> „Claude doesn't save something every session. It decides what's worth remembering based on whether the information would be useful in a future conversation."

Ugyanez forrás. *(Megjegyzés: a session-induló rendszerprompt pontos, betű szerinti szövegét — a `loadMemoryPrompt()` által beillesztett instrukciós blokkot — az Anthropic nem publikálja hivatalosan; több független, nem hivatalos, forráskód-visszafejtésen alapuló repository (pl. `luyao618/Claude-Code-Source-Study`, `leaf-kit/claude-analysis`) közöl belőle részleteket, de ezek hitelessége nem ellenőrizhető és nem hivatalos Anthropic-forrás — T3, óvatosan kezelendő, lásd „Ellentmondások".)*

### 2.3 OpenAI — Codex (AGENTS.md) és Agents SDK (Sessions)

A Codex esetében **nincs külön „memória-eszköz"**, amit a modellnek proaktívan meg kellene hívnia — az AGENTS.md fájlokat a keretrendszer session-indításkor automatikusan a fejlesztői üzenetbe fűzi, olvasás nélkül is látja a modell. A beépített rendszerprompt-részlet (a Codex forráskódjából, `default.md`) explicit előírja, hogy kötelezően be kell tartani, amit egyszer betöltött:

> „Repos often contain AGENTS.md files. These files are a way for humans to give you (the agent) instructions or tips for working within the container... For every file you touch in the final patch, you must obey instructions in any AGENTS.md file whose scope includes that file... The contents of the AGENTS.md file at the root of the repo and any directories from the CWD up to the root are included with the developer message and don't need to be re-read."

Forrás: codex-rs/protocol/src/prompts/base_instructions/default.md, https://github.com/openai/codex/blob/385c0a9351e2199929e01f7864ec78a8f7d5e580/codex-rs/protocol/src/prompts/base_instructions/default.md (T1, gyártói forráskód).

A hivatalos Codex-doksi külön kiemeli, hogy az AGENTS.md-t helyesbítő visszacsatolással kell karbantartani, és a modellt kell megkérni, hogy maga frissítse:

> „When the agent makes incorrect assumptions about your codebase, correct them in `AGENTS.md` and ask the agent to update `AGENTS.md` so the fix persists. Treat it as a feedback loop."

Forrás: „Customization – Codex", https://developers.openai.com/codex/concepts/customization (T1, hivatalos).

Az **OpenAI Agents SDK** „Sessions" mechanizmusa strukturálisan **más elvre épül**, mint az Anthropic memory tool: itt a modellnek nem kell proaktívan „eszközt hívnia" a memóriához — a runner automatikusan, minden futás előtt visszatölti és a bemenet elé fűzi a session-history-t:

> „When session memory is enabled: 1. Before each run: The runner automatically retrieves the conversation history for the session and prepends it to the input items. 2. After each run: All new items generated during the run... are automatically stored in the session."

Forrás: „Overview - OpenAI Agents SDK", https://openai.github.io/openai-agents-python/sessions/ (T1, hivatalos). Ez azt jelenti, hogy az OpenAI Agents SDK „memóriája" alapesetben **nem** a modell önkéntes eszközhívásán múlik — ezzel elkerüli a kutatási kérdés által feltételezett problémát (,,rávegyük a modellt, hogy keressen"), mert a betöltés automatikus/kikényszerített infrastruktúra-szinten, nem modell-döntés.

### 2.4 Google — Gemini CLI (GEMINI.md + memory tool)

A hivatalos Gemini CLI dokumentáció szerint a GEMINI.md-fájlok hierarchikusan, session-indításkor automatikusan betöltődnek és összefűződnek:

> „The CLI uses a hierarchical system to source context. It loads various context files from several locations, concatenates the contents of all found files, and sends them to the model with every prompt."

Forrás: „Provide context with GEMINI.md files", https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/gemini-md.md (T1, hivatalos).

A Gemini CLI forráskódjában (`packages/core/src/prompts/snippets.ts`, gyártói repo) explicit, szó szerinti utasítás szerepel a modellnek arra, *mikor* hívja meg a memória-eszközt — ez a legkonkrétabb, közvetlenül idézhető „eszközleírás-szintű" rábeszélő szöveg, amit találtam:

> „**Memory Tool:** Use `save_memory` to persist facts across sessions. It supports two scopes via the `scope` parameter: `"global"` (default): Cross-project preferences and personal facts loaded in every workspace. `"project"`: Facts specific to the current workspace... Never save transient session state. Do not use memory to store summaries of code changes, bug fixes, or findings discovered during a task."
>
> (korábbi verzióban, explicit feltétel-megadással:) „Use the 'save_memory' tool to remember specific, *user-related* facts or preferences when the user explicitly asks, or when they state a clear, concise piece of information that would help personalize or streamline *your future interactions with them*... This tool is for user-specific information that should persist across sessions. Do *not* use it for general project context or information. If unsure whether to save something, you can ask the user, 'Should I remember that for you?'"

Forrás: google-gemini/gemini-cli, `packages/core/src/prompts/snippets.ts` és `packages/core/src/core/prompts.ts`, https://github.com/google-gemini/gemini-cli/blob/caa04664/packages/core/src/prompts/snippets.ts , https://github.com/google-gemini/gemini-cli/blob/e79b149/packages/core/src/core/prompts.ts (T1, gyártói forráskód, több egymást követő commit-verzióban konzisztens).

A memóriaverzió (V2) esetén a forrás explicit „routing" szabályokat is ad, hogy melyik szintű fájlba írjon a modell — ez direkt analóg az SQ06 projekt saját nyitott kérdésével (,,hova kerüljön az új bejegyzés"):

> „**Routing rules — pick exactly one tier per fact:** ... If a fact could plausibly belong to more than one tier, **ask the user** which tier they want before writing. **Never duplicate or mirror the same fact across tiers**..."

Ugyanaz a forrás.

## 3. A beadott szöveg helye és hossza — mérések

### 3.1 Pozíció: „Lost in the Middle" (Liu et al., TACL 2024 / arXiv 2023)

A legidézettebb, lektorált (Transactions of the ACL) tanulmány szerint a relevancia-pozíció U-alakú teljesítménygörbét ad — a legelején és a legvégén lévő információ jobban hasznosul, mint a középen lévő:

> „We observe that performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts, even for explicitly long-context models."

> „For example, when relevant information is placed in the middle of its input context, GPT-3.5-Turbo's performance on the multi-document question task is lower than its performance when predicting without any documents (i.e., the closed-book setting; 56.1%)."

Forrás: „Lost in the Middle: How Language Models Use Long Contexts", TACL 2024, https://aclanthology.org/2024.tacl-1.9/ ; eredeti preprint: https://arxiv.org/abs/2307.03172 (T1, lektorált).

Ez direkt releváns a kutatási kérdésre: egy session-eleji rövid emlékeztető szöveg (primacy pozíció) elméletileg **kedvezőbb** helyen van, mint egy középre kerülő szöveg — de a hossz növekedésével (több dokumentum/token) ez az előny is csökken.

### 3.2 Hossz és „context rot": a session hossza rontja a korábban beadott szöveg hatását

Az Anthropic saját mérnöki blogja (Effective context engineering for AI agents, 2025-09-29) explicit összekapcsolja a jelenséget az „attention budget" fogalmával:

> „Studies on needle-in-a-haystack style benchmarking have uncovered the concept of context rot: as the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases... Like humans, who have limited working memory capacity, LLMs have an 'attention budget' that they draw on when parsing large volumes of context. Every new token introduced depletes this budget by some amount..."

Forrás: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents (T1, hivatalos, 2025-09-29).

A Chroma kutatócsapat 18 modellen (GPT-4.1, Claude 4, Gemini 2.5, Qwen3 stb.) kontrollált kísérletekkel — a feladat nehézségét állandó szinten tartva, csak a bemenet hosszát változtatva — függetlenül igazolta ugyanezt:

> „We demonstrate that even under these minimal conditions, model performance degrades as input length increases, often in surprising and non-uniform ways... Across all experiments, model performance consistently degrades with increasing input length."

Forrás: „Context Rot: How Increasing Input Tokens Impacts LLM Performance", https://www.trychroma.com/research/context-rot (T2, iparági kutatóműhely, nem lektorált, de módszertanilag kontrollált, széles körben idézett).

Egy harmadik, független tanulmány (2026) még szélsőségesebb változatban mutatja meg ugyanezt: **tökéletes visszakeresés mellett is** romlik a teljesítmény, pusztán a hossztól:

> „...even when models can perfectly retrieve all relevant information, their performance still degrades substantially (13.9%–85%) as input length increases... This failure occurs even when the irrelevant tokens are replaced with minimally distracting whitespace, and, more surprisingly, when they are all masked and the models are forced to attend only to the relevant tokens."

Forrás: „Context Length Alone Hurts LLM Performance Despite Perfect Retrieval", arXiv:2510.05381, https://arxiv.org/html/2510.05381 (T1, 2026).

Egy negyedik, hosszú-horizontú keresési (agentic search) tanulmány azt méri, hogy hosszú kontextusban a modellek *idő előtt feladják* a feladatot:

> „...under extensive context, models give up or provide uncertain incorrect answers long before exhausting the context window... the premature termination rate is positively correlated with context length [when query difficulty is held fixed]."

Forrás: „Diagnosing and Mitigating Context Rot in Long-horizon Search", arXiv:2606.29718, https://arxiv.org/html/2606.29718 (T1, 2026). **Ez négy egymástól független kutatócsoport (Anthropic, Chroma, egy önálló arXiv-szerzői csoport, egy másik önálló arXiv-csoport) konvergáló eredménye** — a session hossza szisztematikusan rontja a korábban beadott információ hasznosulását.

A gyártói termékdokumentáció is közvetlenül alkalmazza ezt a memória-fájlokra: a Claude Code auto-memory rendszernél a `MEMORY.md`-nek explicit méretkorlátja van, és a hivatalos doksi szerint a **rövidebb** fájlok jobban követve vannak:

> „The first 200 lines of `MEMORY.md`, or the first 25KB, whichever comes first, are loaded at the start of every conversation. Content beyond that threshold is not loaded at session start... This limit applies only to `MEMORY.md`. CLAUDE.md files are loaded in full regardless of length, though shorter files produce better adherence."

Forrás: https://code.claude.com/docs/en/memory (T1, hivatalos).

### 3.3 Ellenpélda / null-eredmény a hosszhatásra (lásd „Ellentmondások")

Egy 2026-os, **nem lektorált** preprint kifejezetten megpróbálta reprodukálni a „context rot"-ot kontrollált, előre regisztrált kísérletben 4 friss modellen (gpt-5.5, gpt-5.4, gpt-5.4-mini, claude-sonnet-4-6), és 150 000 tokenig **nem talált mérhető hosszfüggő romlást**:

> „...we observe no measurable length-driven degradation on our probes for the four models tested... up to 150,000 tokens... Across the 12,570-trial registered grid, 7,330 present-needle trials had 48 failures (accuracy 0.9935)."

Forrás: „Is Context Rot Real? A Controlled, Cross-Provider Null for Length-Driven Degradation in Frontier Models up to 150k Tokens", Zenodo preprint, https://doi.org/10.5281/zenodo.20753848 (T2, „Preprint - not peer reviewed", 2026-06-18). A szerző maga hangsúlyozza, hogy szintetikus, tiszta needle-in-haystack feladatokról van szó, és „we cannot determine its contribution in real multi-turn agentic workflows" — tehát nem cáfolja az agentikus/hosszú-session kontextusban mért romlást (3.2 pont), csak azt jelzi, hogy legújabb frontier-modelleken, tiszta lexikai visszakeresési feladaton a hatás nem mindig mutatkozik.

## 4. Kockázatok: ronthatja-e a munkát egy beadott címlista/tartalom?

### 4.1 Irreleváns tartalom zavarja a modellt — mért hatás

A Shi et al. (ICML 2023, lektorált) GSM-IC benchmarkja kifejezetten azt méri, mennyire téríti el a modellt egyetlen irreleváns mondat beszúrása egy egyébként megoldható feladatba:

> „...among the original problems that can be solved by baseline prompts with greedy decoding, no more than 18% of them can be consistently solved for all types of irrelevant information, showing that the large language model is easily distracted and produces inconsistent predictions when adding a small amount of irrelevant information to the problem description."

> „Adding irrelevant information to the exemplars shown in the prompt consistently boosts the performance, and the same holds for adding an instruction to ignore irrelevant context. This suggests that language models are—to some extent—able to learn to ignore irrelevant information by following examples or instructions."

Forrás: „Large Language Models Can Be Easily Distracted by Irrelevant Context", ICML 2023, https://proceedings.mlr.press/v202/shi23a.html (T1, lektorált).

Ez direkt releváns arra a kockázatra, hogy egy sablonos „emlékeztető" szöveg (ami a konkrét kérdéshez esetleg nem kapcsolódó memória-tartalmat vagy metaadatot sorol fel) önmagában zavaró tényező lehet — bár egy explicit instrukció („hagyd figyelmen kívül, ha irreleváns") részben ellensúlyozza.

### 4.2 Elavult lista félrevezetheti a modellt — dokumentált eset

Egy közösségi GitHub-jegy (nem hivatalosan megerősített hibajelentés) a Codex Desktopban dokumentál egy esetet, ahol egy **elavult, memóriában tárolt** munkafolyamat felülírta a helyesen, aktuálisan betöltött AGENTS.md-utasítást:

> „Codex Desktop loaded both the global `~/.codex/AGENTS.md` and the repository `AGENTS.md` into the task context, but the agent ignored a distinctive current global rule and instead followed stale validation-gate guidance recovered from persistent memory... The problem is instruction precedence/compliance: stale memory was treated as more authoritative than the current, explicitly loaded global `AGENTS.md`."

Forrás: „Codex Desktop loads global AGENTS.md but stale memory overrides its explicit rule", GitHub issue, https://github.com/openai/codex/issues/39223 (T2, első kézből származó, de nem hivatalosan megerősített/lezárt hibajelentés).

Ez pontosan az az eset, amire az SQ06 kérdés rákérdez: ha a memóriában/emlékeztetőben elavult információ van (pl. egy régi, már nem érvényes bejegyzés-lista), az konkrétan félre tudja vezetni az agentet a friss, helyes instrukció rovására.

### 4.3 Prompt injection a beadott tartalmon keresztül — akadémiai támadás

A MINJA (,,Memory INJection Attack", NeurIPS 2025, lektorált) formálisan bizonyítja, hogy egy támadó **kizárólag lekérdezéseken keresztül**, a memóriabank közvetlen elérése nélkül tud rosszindulatú bejegyzéseket becsempészni, amelyeket a rendszer később, más felhasználó kérésére visszahív:

> „The attacker injects malicious records into the memory bank by only interacting with the agent via queries and output observations... When the victim user submits a victim query, the stored malicious records are retrieved as a demonstration, misleading the agent to generate bridging steps and target reasoning steps through in-context learning... Our extensive experiments across diverse agents demonstrate the effectiveness of MINJA in compromising agent memory."

Forrás: „Memory Injection Attacks on LLM Agents via Query-Only Interaction", NeurIPS 2025, https://proceedings.neurips.cc/paper_files/paper/2025/hash/42a97bbd9844d2bf68596730af80bcdf-Abstract-Conference.html (T1, lektorált).

### 4.4 Prompt injection a beadott tartalmon keresztül — valós, dokumentált incidens

Johann Rehberger biztonsági kutató 2024-ben (saját, elsődleges közlésű blogján, később Ars Technica és Bruce Schneier is megerősítette/idézte) dokumentált egy valós, éles ChatGPT-memória elleni indirekt prompt injection támadást:

> „Within three months of the rollout, Rehberger found that memories could be created and permanently stored through indirect prompt injection... The researcher demonstrated how he could trick ChatGPT into believing a targeted user was 102 years old, lived in the Matrix, and insisted Earth was flat and the LLM would incorporate that information to steer all future conversations. These false memories could be planted by storing files in Google Drive or Microsoft OneDrive, uploading images, or browsing a site like Bing."

Forrás: Ars Technica, „Hacker plants false memories in ChatGPT to steal user data in perpetuity", 2024-09-24, https://arstechnica.com/security/2024/09/false-memories-planted-in-chatgpt-give-hacker-persistent-exfiltration-channel/ (T2, minőségi tech-újságírás, elsődleges kutatói közlésre alapozva).

A kutató saját, elsődleges technikai leírása (embracethered.com) megerősíti, és két súlyos következményt is dokumentál: tartós adatszivárgást és tartós szolgáltatás-megtagadást (DoS), mindkettő a memória-injektáláson keresztül, munkameneteken átívelően:

> „What is really interesting is this is memory-persistent now... The prompt injection inserted a memory into ChatGPT's long-term storage. When you start a new conversation, it actually is still exfiltrating the data."

Forrás: Johann Rehberger, „ChatGPT: Hacking Memories with Prompt Injection", https://embracethered.com/blog/posts/2024/chatgpt-hacking-memories/ (T1, elsődleges kutatói közlés, 2024-05-22).

> „Malicious memory modifications remain until the user manually removes the attacker-created memories... From now on, ChatGPT will refuse every future response."

Forrás: Johann Rehberger, „Sorry, ChatGPT Is Under Maintenance: Persistent Denial of Service through Prompt Injection and Memory Attacks", https://embracethered.com/blog/posts/2024/chatgpt-persistent-denial-of-service/ (T1, elsődleges, 2024-07-08).

Fontos, hogy OpenAI kezdetben nem biztonsági, hanem „modellbiztonsági" (model safety) ügyként zárta le a jelentést, majd 2024 szeptemberében részlegesen javította:

> „When security researcher Johann Rehberger recently reported a vulnerability in ChatGPT that allowed attackers to store false information and malicious instructions in a user's long-term memory settings, OpenAI summarily closed the inquiry, labeling the flaw a safety issue, not, technically speaking, a security concern... OpenAI released a fix for the macOS app last week."

Forrás: Ars Technica, ugyanaz mint fent (T2); megerősítve: Bruce Schneier, „Hacking ChatGPT by Planting False Memories into Its Data", https://www.schneier.com/blog/archives/2024/10/hacking-chatgpt-by-planting-false-memories-into-its-data.html (T3, biztonsági szakértői kommentár, idézi az elsődleges forrást).

**Ez a négy forrás (MINJA akadémiai támadás + Rehberger elsődleges közlés + Ars Technica + Schneier) két, egymástól teljesen független bizonyítékvonalat ad**: egy formális, lektorált akadémiai támadási technikát, és egy valós, gyártó által is (részlegesen) elismert incidenst — vagyis a kockázat mind elméletileg, mind gyakorlatilag igazolt.

## Ellentmondások

- **A 84%/39%-os Anthropic-szám értelmezése.** Az Anthropic saját bejelentése szerint a memória-eszköz + context editing kombináció „39%-kal" jobb teljesítményt, a context editing önmagában „84%-kal" kevesebb tokenfelhasználást ad — ez elsőre úgy hangzik, mintha a memória-eszköz általában sokat javítana. Egy független, kritikai elemzés (T3, dreaming.press, 2026-07-27) rámutat, hogy ezek a számok egy **kontextus-kimerüléses bukásból** való megmenekülést mérik, nem általános képességnövekedést: „Both figures are real. Neither says the model got smarter — they measure escaping a wall your agent may never hit... on short tasks the delta collapses toward zero." Vagyis rövid session esetén (amilyen egy tipikus, néhány üzenetes interakció is lehet) a mért haszon a nullához tarthat — ellentétben azzal a benyomással, amit a puszta „39%" szám sugall. Ez direkt releváns az SQ06 alapkérdésére: egy rövid, session-eleji emlékeztető haszna feltehetően szintén a session hosszától és a kontextus-nyomástól függ, nem konstans.

- **A hosszhatás („context rot") univerzalitása vitatott.** Négy egymástól független forrás (Anthropic, Chroma, két önálló arXiv-tanulmány) mért, szisztematikus teljesítményromlást talál a bemeneti hossz növekedésével, míg egy 2026-os, nem lektorált, előre regisztrált null-eredmény (Zenodo) 150 000 tokenig **nem** talált mérhető hosszfüggő romlást 4 legújabb frontier-modellen tiszta needle-in-haystack feladaton. A szerző maga jelzi, hogy ez nem feltétlenül mond ellent az agentikus, több-fordulós forgatókönyveknek — csak azt, hogy a legújabb modelleken, tiszta lexikai feladaton a hatás nem mindig, nem minden körülmények között jelentkezik. A két eredménykör tehát nem feltétlenül zárja ki egymást, de a hatás mértéke és univerzalitása nyitott kérdés marad.

- **A Claude Code belső rendszerprompt-szövegének hitelessége.** Az Anthropic hivatalosan **nem** publikálja a Claude Code session-induló memória-instrukciós blokk (`loadMemoryPrompt()`) pontos szövegét. Több, egymással erősen egyező, de nem hivatalos, forráskód-visszafejtésen alapuló GitHub-repository (`luyao618/Claude-Code-Source-Study`, `leaf-kit/claude-analysis`, `zackautocracy/claude-code`, `y-agent.github.io/inside-claude-code`) közöl belőle kódrészleteket és promptszövegeket — ezek egymással konzisztensek, de valószínűleg **közös eredetre** (ugyanarra a kiszivárgott/visszafejtett forrásra) vezethetők vissza, nem egymástól független megerősítések, és hitelességük (hogy tényleg a jelenlegi, éles Claude Code kódjából származnak-e) nem ellenőrizhető külső, hivatalos forrásból. Ezért ezeket a részleteket a jelen jelentésben csak jelzésértékű, T3 minősítésű adalékként használtam, nem tényként.

## Amire NINCS forrás

- **Nincs forrás** egy kontrollált (A/B jellegű) kísérletre, amely kifejezetten azt mérné: egy rövid, sablonból generált, session-eleji szöveg (,,van memória, N bejegyzés, használd a keresőt") jelenléte vs. hiánya mennyivel változtatja meg egy memória- vagy kereső-eszköz **önkéntes** meghívási arányát, elkülönítve a hatást a szöveg hosszától és tartalmától. Ez pontosan a kutatási kérdés fókusza, és a fenti 1–3. pontban idézett tanulmányok mind csak közvetett, rokon jelenségeket (általános eszközhasználati arány, memória-benchmark pontosság, pozíció/hossz hatása szövegértésre) mérnek, nem ezt a konkrét beavatkozást.
- **Nincs forrás** arra, hogy a beadott szövegben szereplő **konkrét bejegyzésszám** (,,17 bejegyzés van a memóriában") önmagában, számszerűsítve hogyan befolyásolja a modell keresési hajlandóságát vagy a keresés mélységét/pontosságát.
- **Nincs forrás** (lektorált vagy gyártói) arra, hogy az Anthropic, OpenAI vagy Google konkrétan mérte volna a saját session-indító emlékeztető szövegük hosszának hatását a memóriahasználatra — a gyártói dokumentációk csak minőségi ajánlásokat adnak („legyen rövid és specifikus"), számszerű ablációt egyik gyártó sem publikált nyilvánosan.
- **Nincs forrás** az OpenAI Codex/Agents SDK esetére vonatkozó, a Gemini CLI PR #18559-hez hasonló, explicit, modellváltozatonkénti gyártói nyilatkozatra arról, hogy mennyi explicit „nógatás" szükséges a memóriahasználathoz.

## Meglátogatott és felderített linkek

| Cím | URL | Tier | Eszköz | Megjegyzés |
|---|---|---|---|---|
| Memory tool — Claude Platform Docs | https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool | T1 | Exa search+fetch | Auto-injektált „MEMORY PROTOCOL" szöveg szó szerint |
| Memory & context management cookbook (Claude Sonnet 4.6) | https://platform.claude.com/cookbook/tool-use-memory-cookbook | T1 | Exa search | Fejlesztői MEMORY_SYSTEM_PROMPT minta |
| Effective context engineering for AI agents | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | T1 | Exa search | „context rot", „attention budget" fogalmak eredete |
| Managing context on the Claude Developer Platform | https://www.anthropic.com/news/context-management | T1 | Exa search | 84%/39% önbevallott mérési számok |
| How Claude remembers your project — Claude Code Docs | https://code.claude.com/docs/en/memory | T1 | Exa search | CLAUDE.md + auto memory hivatalos leírása |
| Explore the context window — Claude Code Docs | https://code.claude.com/docs/en/context-window | T1 | Exa search | Compaction utáni memória-újrainjektálás |
| Custom instructions with AGENTS.md — Codex | https://developers.openai.com/codex/guides/agents-md | T1 | Exa search | AGENTS.md betöltési sorrend, méretkorlát |
| Customization — Codex | https://developers.openai.com/codex/concepts/customization | T1 | Exa search | AGENTS.md vs memories vs skills |
| codex-rs/core/src/agents_md.rs (openai/codex) | https://github.com/openai/codex/blob/main/codex-rs/core/src/agents_md.rs | T1 | Exa search | Forráskód: AGENTS.md betöltés/csonkolás |
| codex-rs base_instructions/default.md | https://github.com/openai/codex/blob/385c0a9351e2199929e01f7864ec78a8f7d5e580/codex-rs/protocol/src/prompts/base_instructions/default.md | T1 | Exa search | Codex beépített rendszerprompt szövege AGENTS.md-ről |
| AGENTS.md silently truncated — issue #7138 | https://github.com/openai/codex/issues/7138 | T2 | Exa search | 32 KiB csonkolási hiba, gyártói válasszal |
| Codex Desktop stale memory overrides AGENTS.md — issue #39223 | https://github.com/openai/codex/issues/39223 | T2 | Exa search | Elavult memória felülírja friss instrukciót — dokumentált eset |
| Overview — OpenAI Agents SDK (Sessions) | https://openai.github.io/openai-agents-python/sessions/ | T1 | Exa search | Automatikus history-betöltés, nem eszközhívás-alapú |
| Sessions — OpenAI Agents SDK (JS) | https://openai.github.io/openai-agents-js/guides/sessions/ | T1 | Exa search | Ugyanaz TS SDK-ban |
| Short-Term Memory Management with Sessions (cookbook) | https://developers.openai.com/cookbook/examples/agents_sdk/session_memory | T2 | Exa search | Trimming/summarizing session implementáció |
| Provide context with GEMINI.md files | https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/gemini-md.md | T1 | Exa search | Hierarchikus, JIT context-betöltés |
| Manage context and memory (Gemini CLI tutorial) | https://geminicli.com/docs/cli/tutorials/memory-management/ | T1 | Exa search | `/memory show`, `/memory reload` |
| Gemini CLI core prompts.ts | https://github.com/google-gemini/gemini-cli/blob/e79b149/packages/core/src/core/prompts.ts | T1 | Exa search | Memória-eszköz használatára vonatkozó rendszerprompt-szöveg (korábbi verzió) |
| Gemini CLI snippets.ts (toolUsageRememberingFacts) | https://github.com/google-gemini/gemini-cli/blob/caa04664/packages/core/src/prompts/snippets.ts | T1 | Exa search | Jelenlegi memória-instrukció + tier-routing szabályok |
| refactor: remove memory tool instructions from Gemini 3 prompt — PR #18559 | https://github.com/google-gemini/gemini-cli/pull/18559 | T1 | Exa search | Modellfüggő „nógatás"-szükséglet — kulcsbizonyíték Q1-hez |
| Lost in the Middle: How Language Models Use Long Contexts (TACL 2024) | https://aclanthology.org/2024.tacl-1.9/ | T1 | Exa search | U-alakú pozíció-teljesítmény görbe, lektorált |
| Lost in the Middle (arXiv preprint) | https://arxiv.org/abs/2307.03172 | T1 | Exa search | Ugyanaz, eredeti preprint |
| Context Rot: How Increasing Input Tokens Impacts LLM Performance (Chroma) | https://www.trychroma.com/research/context-rot | T2 | Exa search | 18 modell, kontrollált hosszkísérlet |
| Context Length Alone Hurts LLM Performance Despite Perfect Retrieval | https://arxiv.org/html/2510.05381 | T1 | Exa search | Hossz önmagában árt, elterelés nélkül is |
| Diagnosing and Mitigating Context Rot in Long-horizon Search | https://arxiv.org/html/2606.29718 | T1 | Exa search | „premature termination", hossz-korreláció |
| Is Context Rot Real? Controlled Cross-Provider Null (Zenodo) | https://doi.org/10.5281/zenodo.20753848 | T2 | Exa search | Ellenpélda: nem talált hosszhatást 150k tokenig |
| Large Language Models Can Be Easily Distracted by Irrelevant Context (ICML 2023) | https://proceedings.mlr.press/v202/shi23a.html | T1 | Exa search | GSM-IC, irreleváns tartalom mért hatása |
| LONGMEMEVAL (ICLR 2025) | https://proceedings.iclr.cc/paper_files/paper/2025/file/d813d324dbf0598bbdc9c8e79740ed01-Paper-Conference.pdf | T1 | Exa search | 30%-os pontosságesés hosszú-memória feladaton |
| MemGPT: Towards LLMs as Operating Systems | https://arxiv.org/abs/2310.08560 | T1 | Exa search | Önkéntes memóriakezelés csak explicit instrukcióval működik |
| LLM Agents Already Know When to Call Tools (WHEN2TOOL) | https://arxiv.org/pdf/2605.09252v2 | T1 | Exa search | Prompt-only beavatkozás durva, nem szelektív hatása |
| ToolFailBench | https://ar5iv.labs.arxiv.org/html/2607.04686 | T1 | Exa search | 19 modell, eszközhasználati hibaarányok |
| Tunable Tool-Call Rates in LLM Agents via Representation Steering | https://arxiv.org/html/2608.25198v1 | T1 | Exa search | Eszközhívási arány mint mérhető, kontrollálható változó |
| To Call or Not to Call: A Framework to Assess and Optimize LLM Tool Calling | https://arxiv.org/html/2605.00737v3 | T1 | Exa search | Vélt vs. valós szükséglet közti eltérés |
| Memory Injection Attacks on LLM Agents via Query-Only Interaction (MINJA, NeurIPS 2025) | https://proceedings.neurips.cc/paper_files/paper/2025/hash/42a97bbd9844d2bf68596730af80bcdf-Abstract-Conference.html | T1 | Exa search | Lektorált memória-injekciós támadás |
| ChatGPT: Hacking Memories with Prompt Injection | https://embracethered.com/blog/posts/2024/chatgpt-hacking-memories/ | T1 | Exa search | Elsődleges kutatói közlés (Rehberger), valós eset |
| Spyware Injection Into Your ChatGPT's Long-Term Memory | https://embracethered.com/blog/posts/2024/chatgpt-macos-app-persistent-data-exfiltration/ | T1 | Exa search | Tartós adatszivárgás memórián át |
| Sorry, ChatGPT Is Under Maintenance (persistent DoS) | https://embracethered.com/blog/posts/2024/chatgpt-persistent-denial-of-service/ | T1 | Exa search | Tartós szolgáltatás-megtagadás memórián át |
| Hacker plants false memories in ChatGPT (Ars Technica) | https://arstechnica.com/security/2024/09/false-memories-planted-in-chatgpt-give-hacker-persistent-exfiltration-channel/ | T2 | Exa search | Összefoglaló, OpenAI reakció idézve |
| Hacking ChatGPT by Planting False Memories (Schneier on Security) | https://www.schneier.com/blog/archives/2024/10/hacking-chatgpt-by-planting-false-memories-into-its-data.html | T3 | Exa search | Szakértői kommentár |
| The 84% and the 39%: What Anthropic's Numbers Actually Measure | https://dreaming.press/posts/anthropic-context-editing-84-percent-39-percent-numbers-examined.html | T3 | Exa search | Kritikai elemzés a vendor-számokról |
| docs-en/31-memory-subsystem-overview.md (Claude-Code-Source-Study) | https://github.com/luyao618/Claude-Code-Source-Study/blob/main/docs-en/31-memory-subsystem-overview.md | T3 | Exa search | Nem hivatalos forráskód-visszafejtés, óvatosan kezelendő |
| src/memdir/memdir.ts (leaf-kit/claude-analysis) | https://github.com/leaf-kit/claude-analysis/blob/main/src/memdir/memdir.ts | T3 | Exa search | Ugyanaz, más tükör — hitelesség nem ellenőrizhető |
| Benchmarking Agent Tool Use (LangChain blog, 2023) | https://www.langchain.com/blog/benchmarking-agent-tool-use | T3 | Exa search | Korai, kiegészítő iparági benchmark |
| Exploring Anthropic's Memory Tool (Leonie Monigatti blog) | https://www.leoniemonigatti.com/blog/claude-memory-tool.html | T3 | Exa search | Független demonstráció: agent csak akkor hív memóriát, ha „szükséges" |

---

# SQ07 — Használják-e az agentek önként a memória-eszközt? A bizonyítékok

*Módszertani megjegyzés: al-ügynököket nem indítottam (degradált mód, ahogy az `_kozos.txt` engedélyezi), egyetlen szálon, szekvenciális Exa-kereséssel/-olvasással dolgoztam. Az Exa (`mcp__Exa__web_search_exa`, `mcp__Exa__web_fetch_exa`) elérhető volt, kizárólag ezt használtam; beépített WebSearch/WebFetch-et nem hívtam. A Saha-cikket (arXiv:2607.20972) teljes terjedelmében (absztrakt, §1–§8, hivatkozásjegyzék) közvetlenül lehívtam az arXiv HTML-változatából, nem másodkézből idézem.*

## Rövid válasz

Egy közvetlenül releváns, kontrollált — de egyszerzős, nem lektorált, kis mintás — kísérlet (Saha, 2026, arXiv:2607.20972) azt találja, hogy a kódoló agentek önkéntes memóriahasználata gyakorlatilag nulla: a legerősebb, előre feltöltött tárral, csatlakoztatott eszközökkel és explicit szöveges útmutatással futtatott ágban (V arm, n=1) az agent 114 körben egyetlen memóriahívást sem tett, és az öt "felszerelt, de nem célzottan táplált" futásban (B+C ágak) összesen 0–1 önkéntes írás történt. Ezt a mintázatot — hogy a modellek a rendelkezésre álló memória-/tudás-eszközöket nem, vagy csak redundánsan, hatékonytalanul használják — egy tőle független, más szerzők által készített, más feladatkörön (vállalati többplatformos munkafolyamat) futtatott, NeurIPS 2025-ön bemutatott benchmark (MEMTRACK, arXiv:2510.01353) is megerősíti. Ezen túl nincs publikált, több kódoló-CLI-t (Claude Code, Codex, Cursor, Gemini CLI, Copilot) azonos protokollal összehasonlító, kvantitatív mérés az önkéntes memória-MCP-hívási arányról — ezt a hiányt maguk a gyártók is implicit módon elismerik azzal, hogy egyik memóriarendszerük sem bízza a felidézést tisztán az agent önkéntes döntésére: az Anthropic memory tool-ja automatikusan ellenőrzi a memóriakönyvtárat feladat előtt, a GitHub Copilot Memory session indításkor automatikusan befűzi a releváns emlékeket a promptba. A felhasználói visszajelzések (GitHub-issue-k, Cursor-fórum) szisztematikusan ugyanazt a mintát mutatják: a karbantartók explicit megerősítik, hogy egy MCP-eszköz önkéntes hívását nem lehet garantálni, és a bevett munkakörüli megoldás mindig valamiféle kényszerítő mechanizmus (hook, kötelező projektutasítás, automatikus injekció). Ellenérvként egyetlen kontrollált forrás (maga a Saha-cikk) mutatja, hogy az injektálás UTÁN az agent önkéntes memóriaműveletei megnőnek ("injection begets engagement"), vagyis az önkéntes használat nem soha nem történik meg, hanem tipikusan a kényszerített felidézést *követi*, nem helyettesíti.

## 1. A Saha-cikk (arXiv:2607.20972) részletesen

### 1.1 Mit mértek pontosan

**Szerző és publikálás:** Swapnanil Saha, független kutató, „Delivery, Not Storage: Cue-Anchored Working Memory as a Harness Property for Coding Agents", arXiv:2607.20972, 2026 július. Forrás: https://arxiv.org/abs/2607.20972 , teljes szöveg: https://arxiv.org/html/2607.20972v1 (T2 — arXiv preprint, egyetlen szerző, nincs feltüntetett lektorált megjelenés).

**Modell:** minden ágban ugyanaz — „All arms run the same agent product, same model (Claude Sonnet 5, claude-sonnet-5), same prompt, same corpus SHA." (https://arxiv.org/html/2607.20972v1, §5). A repeated-compaction decay-próba (§5.7) egy másik, kisebb modellt használ: „executed by a small fast model (Claude Haiku 4.5)".

**Agent-termék:** Claude Code („the agent harness (Claude Code, an agentic coding CLI)", §4).

**Feladat:** egy valódi, natúr kódolási feladat egy rögzített (pinned) Apache Camel checkout-on (~169k indexelt chunk): „implement the reverse option for the stream-mode Resequencer EIP (Enterprise Integration Pattern)... gated by a harness-provided acceptance test that must pass unmodified plus the resequencer-scoped regression set (-Dtest='*Resequenc*Test', 42 tests)" (§5).

**Karok (arms) — pontos meghatározás (§5 táblázat):**
- A (n=3): nincs memória-felszín — kontroll.
- B (n=2): „store (cold) + tools + guidance" → delivery: **voluntary**.
- C (n=3): „store + tools + proxy, cold store" → delivery: injection (de üres tár, nincs mit injektálni).
- CS (n=1): „store seeded" → delivery: proxy injection.
- H (n=2): „store seeded" → delivery: native hooks (session-start / prompt-submit / pre-tool-use / pre-compact).
- V (n=1): „store seeded" → delivery: **voluntary** (a hookok eltávolítva; ez H kontrollja).

Összesen 9 pilot + 3 native-channel = 12 kiértékelt (graded) futás.

**"Guidance" definíciója:** a cikk ezt nem külön szakaszban definiálja formálisan, hanem a workspace-instrukciós fájlokban (pl. CLAUDE.md-szerű dokumentumok) elhelyezett, a memóriaeszköz használatára buzdító szöveges utasításokként kezeli, amelyeket a §5.2 „32 memory-guidance mentions in the workspace instruction files" számszerűsít. Vagyis a „guidance" = a projekt írásos instrukciói, amelyek a modellt a memóriaeszköz (nem kényszerített, önkéntes) használatára biztatják — ez különbözik az „injection"-től, ami a harness (nem a modell) által deterministikusan, hook- vagy proxy-mechanizmuson keresztül a kontextusba juttatott tartalom.

### 1.2 Mit talált a „voluntary" (önkéntes) ágakon

A §5.2 szakasz („Adoption: voluntary memory does not happen") szó szerint:

> „Unseeded equipped runs (B, C): voluntary memory writes 0–1 across all five runs, despite 32 memory-guidance mentions in the workspace instruction files and a verified connected tool surface. The native auto-memory directory was never created in any run."

> „The seeded-voluntary control (V) is the strongest form of the finding: same four task-relevant notes in the store as the H arms, same connected tools, same guidance — the agent made zero memory calls in 114 turns. Knowledge present in a store contributes nothing by itself."

Forrás: https://arxiv.org/html/2607.20972v1, §5.2.

Fontos módszertani megjegyzés: a headline „0 memory calls in 114 turns" szám **egyetlen futásból (V1, n=1)** származik; az unseeded B+C ágak összesített, szintén nagyon alacsony (0–1 írás/futás) eredménye 5 futáson alapul. Ezek nagyon kis mintaszámok, amit a szerző maga is a threats-to-validity szakaszban (§7) explicit elismer (l. 1.4 alább).

### 1.3 Mit talált a „delivery" (kényszerített injektálás) ágakon

A §5.3 szakasz („Mechanism: deterministic delivery, proven on two channels") két csatornán (proxy és natív hook) méri a determinisztikus injektálást:

> „Native hooks (H×2): the prompt-submit hook injected a three-note index at launch in both runs, behaviorally confirmed in H1 by the agent's first three tool calls being recalls of exactly the three injected note ids... False-alarm injections: zero in both runs, across 40 and 35 audit-logged trigger evaluations respectively."

A §5.2 egy különösen fontos, az önkéntes/kényszerített dichotómiát árnyaló megfigyelést is tartalmaz:

> „Injection begets engagement: the seeded-proxy run (CS) produced the matrix's only memory-hygiene loop (recall by id, forget of the gotcha its implementation had just obsoleted, then remember of a completion note)... Voluntary memory operations occur after and because of delivery, not instead of it."

Forrás: https://arxiv.org/html/2607.20972v1, §5.2–§5.3.

A repeated-compaction decay-próba (§5.7) ugyanezt más skálán ismétli meg: 108, illetve 138 kényszerített kompaktálás mellett a memória nélküli kar (N) 106/108 összegzésben nulla tényt tartott meg, míg az injektált tárral rendelkező kar (M) 139 auditnaplózott szállítást ért el minden egyes kompaktálás-utáni újraindításkor (138/138):

> „The daemon's audit ledger records 157 session-start evaluations, of which 139 delivered all ten facts into the run: one at every single compact-resume (138/138) plus the first phase launch."

Forrás: https://arxiv.org/html/2607.20972v1, §5.7.

### 1.4 A szerző saját korlátai (§7 — Threats to validity)

A cikk explicit, önálló szakaszt szentel a korlátoknak; a legfontosabb, a voluntary/injection kérdést közvetlenül érintő idézetek:

> „Construct... The decay probe's facts are synthetic and carry an explicit closing-phase obligation — the probe measures survival and delivery under compaction pressure, not spontaneous use."

> „Internal... The evaluated implementation and the benchmark harness share an author; mitigations: pinned corpus SHA (a543dc64), fingerprinted acceptance test, per-run launch-posture assertions archived, audit-log-gated mechanism claims, all raw transcripts, graders, and analyzers published."

> „External. One corpus (Apache Camel), one task family per experiment, one agent product, one model family; the decay probe uses a small fast model (Claude Haiku 4.5)... Results are directional evidence with asserted controls, not population estimates."

> „Conclusion. Sample sizes are small throughout (12 graded matrix runs; one gated run per decay arm, each after protocol repairs documented in the published run log). We report absolute numbers with n visible, claim direction rather than effect size."

Forrás: https://arxiv.org/html/2607.20972v1, §7.

Vagyis a szerző maga mondja ki: (1) az implementációt és a kiértékelő keretrendszert **ugyanaz a szerző** készítette (egyszemélyes, nem független validálás — csak archívált nyers adatokkal ellensúlyozva); (2) egyetlen kódbázis, egyetlen feladatcsalád, egyetlen agent-termék, egyetlen modellcsalád; (3) a mintaszámok kicsik (a legerősebb önkéntes-állítás n=1 futáson alapul); (4) az eredmények iránymutató bizonyítékok, nem populációs becslések.

### 1.5 Kód elérhetősége

A cikk „Artifact Availability" szakasza szerint minden futásarchívum, indítási-állapot-igazolás, kiértékelő szkript, a decay-próba keretrendszere és a teljes nyers tranzakciós napló nyilvánosan elérhető:

> „All run archives, launch-posture assertions, graders, the re-exploration analyzer, the decay-probe harness, and per-run transcripts are published in the Vectr repository (github.com/swapnanil/vectr) under research/proactive-gate/... and research/brain-memory/ (this paper, the analyzer, and measurement data)."

Forrás: https://arxiv.org/html/2607.20972v1, „Artifact availability" szakasz. A GitHub-repót közvetlenül is megtaláltam (a cikk markdown-változata a `research/brain-memory/delivery-not-storage.md` útvonalon van tárolva): https://github.com/swapnanil/vectr/blob/main/research/brain-memory/delivery-not-storage.md — ez megerősíti, hogy a hivatkozott repó valóban létezik és tartalmazza a cikket, de a mögöttes nyers futásadatokat (`research/proactive-gate/`) én magam nem futtattam le és nem ellenőriztem sor-szintjén.

### 1.6 Replikáció vagy vita

Célzottan kerestem citációkat, replikációkat és kritikákat („2607.20972" OR „Delivery, Not Storage" Saha cited by / citation / semantic scholar). Eredmény:
- **Semantic Scholar** keresés a szerző nevére és a cím kulcsszavaira **nem hozott ehhez a konkrét cikkhez tartozó citációs bejegyzést** — a találatok más, azonos vezetéknevű szerzők (Aytijhya Saha, Sujata Saha) teljesen más témájú munkái voltak.
- Találtam egy **másodlagos, nem tudományos** feldolgozást: Daniel Vaughan, „Delivery, Not Storage: Why Cue-Anchored Working Memory Changes How You Think About Codex CLI's Memory Stack", https://codex.danielvaughan.com/2026/07/28/... (2026-07-27, T3 — blog, a szerző maga sem tudományos intézményhez kötött, a cikket összefoglalja és Codex CLI-re alkalmazza, kritikát nem fogalmaz meg).
- Aggregátor-oldalak (alphaXiv, papers.cool, Hugging Face Papers, pubdb.com) megjelenítik a cikket, de **érdemi vita, replikáció vagy cáfolat egyiken sem szerepel** (a Hugging Face Papers „AI Summary" funkciója bejelentkezést igényel, ezt nem tudtam ellenőrizni).

**Következtetés: nem találtam bizonyítékot arra, hogy a Saha-cikk kísérletét bárki független szerző megismételte vagy tartalmilag vitatta volna.** Ez összhangban van azzal, hogy a cikk 2026 júliusában jelent meg, egyszerzős, nem lektorált preprint, és — ahogy a szerző maga is jelzi — az implementáció és a kiértékelés ugyanattól a személytől származik.

## 2. Más mérések vagy szisztematikus beszámolók

### 2.1 MEMTRACK (arXiv:2510.01353) — a legközelebbi független megerősítés

**Szerzők/kiadó:** Darshan Deshpande, Varun Gangal, Hersh Mehta, Rebecca Qian, Anand Kannapan, Peng Wang (Patronus AI + akadémiai szerzők), 2025. október. Forrás: https://arxiv.org/abs/2510.01353 ; OpenReview: https://openreview.net/pdf?id=mVxmbMng4B ; NeurIPS 2025 prezentációs diák: https://neurips.cc/media/neurips-2025/Slides/124523.pdf (T1/T2 — a NeurIPS-en bemutatott anyag léte megerősíthető, a pontos megjelenési sáv — fősáv vagy workshop — a lehívott oldalakból nem volt egyértelműen megállapítható).

Ez a benchmark **más szerzőktől, más feladatkörön (vállalati többplatformos: Slack, Linear, Git), más memória-backend-eken (Mem0, Zep)** teszteli ugyanazt a kérdést: vajon az agent önkéntesen és hatékonyan használja-e a rendelkezésre álló memóriaeszközöket. Az eredmény ugyanabba az irányba mutat, mint a Saha-cikk, bár más mérőszámmal (nem „nulla hívás", hanem „redundáns/hatékonytalan hívás"):

> „Through our findings, we show that state-of-the-art LLMs fail to perform effective multi-platform context reasoning. Furthermore, we show that LLMs cannot use memory tools effectively and using such tools increases redundancy in planning and overall tool use."

> „RQ2: Can agents use memory databases and backends such as Zep and Mem0 effectively to reason over large codebases? According to Table 3, we can observe that memory equipped LLMs fail to call memory tools effectively. LLMs with memory tools consistently display increased redundancy as well as drop in performance efficiency. As observed in the qualitative analysis above, models generally prefer repeatedly accessing information over using the memory component."

Forrás: https://arxiv.org/abs/2510.01353.

A Patronus AI saját blogbejegyzése (T3, gyártói forrás, de ugyanazok a szerzők) ezt tömöríti:

> „The memory components don't cause a significant improvement in performance. Likely because when provided with memory tools, LLMs fail to call them effectively."

Forrás: https://www.patronus.ai/blog/memtrack.

**Fontos árnyalás/eltérés a Saha-cikktől** (l. „Ellentmondások" szakasz): a MEMTRACK azt találja, hogy a modellek **inkább újra és újra hozzáférnek** az alapadatokhoz, ahelyett hogy a memóriakomponenst használnák („models generally prefer repeatedly accessing information over using the memory component") — ez nem „nulla hívás", hanem **rossz arányú, redundáns** hívásmintázat. A két forrás tehát nem azonos jelenséget ír le szó szerint, de mindkettő arra a következtetésre jut, hogy a memóriaeszköz önkéntes, hatékony használata nem történik meg megbízhatóan.

### 2.2 TriggerBench (arXiv:2606.23459) — miért nehéz az önkéntes felidézés

**Szerzők:** Tianhua Zhang, Xinjiang Wang, Qianxi Zhang, Qi Chen, Kun Li, Yaoqi Chen, DingDong Wang, Helen Meng, Yan Lu (Chinese University of Hong Kong + Microsoft Research Asia). Forrás: https://arxiv.org/abs/2606.23459 (T1/T2 — Microsoft Research társszerzőség, arXiv, 2026).

A cikk a „prospective memory" (a látens korlátra spontán, prompt nélküli emlékezés és cselekvés képessége) fogalmát különbözteti meg a „retrospective memory"-tól (explicit lekérdezésre történő visszakeresés):

> „While Large Language Models (LLMs) are increasingly deployed in long interactions, existing evaluations focus predominantly on retrospective memory (RM) via explicit queries. Prospective memory (PM), the critical ability to spontaneously recall and act on latent constraints without direct prompts, remains largely unevaluated."

> „PM is notably harder than RM: on identical contexts, RM near-saturates up to 100K tokens ($\sim$98%), while PM performance suffers a clear drop."

> „models may overfit to an 'always-remind' heuristic. Furthermore, PM accuracy degrades substantially under implicit constraints or triggers overloaded by concurrent user requests, indicating that robust PM remains an open challenge."

Forrás: https://arxiv.org/abs/2606.23459.

Ez közvetlen elméleti alátámasztást ad a Saha-cikk „voluntary lookup is the fallback, never the load-bearing path" állításának: a retrospektív (kért) memóriahasználat megbízható, de a proaktív/önkéntes (kéretlen) felidézés — ami a memória-MCP önkéntes hívásának pontosan megfelel — szisztematikusan gyengébb, és romlik a kontextushosszal.

### 2.3 Van-e mérés, ahol ugyanaz a modell önkéntes hívással vs. automatikus beadással dolgozik?

Ezt a kérdést célzottan kerestem. Az egyetlen forrás, amit találtam, amely **ugyanazt a modellt, ugyanazt az agent-terméket, ugyanazt a feladatot** kontrolláltan futtatja mindkét delivery-móddal (voluntary vs. injection), a **Saha-cikk maga** (§5, V arm vs. H/CS arms, l. 1.1–1.3 fent). Ezen kívül **NINCS FORRÁS** olyan, több kódoló-agent-terméket (Claude Code, Codex, Cursor, Gemini CLI, Copilot) azonos protokollal, azonos modellel összehasonlító, publikált kontrollált kísérletre, amely a memória-MCP önkéntes hívási arányát méri.

### 2.4 Gyártói adatok — közvetett bizonyíték a probléma elismerésére

Egyik vizsgált gyártó sem publikál explicit „önkéntes hívási arány" számot, de mindegyik termékterve **elkerüli, hogy a felidézés tisztán az agent önkéntes döntésén múljon** — ez maga is közvetett bizonyíték arra, hogy a tisztán önkéntes hívás nem megbízható.

**Anthropic memory tool** (élő dokumentáció, 2026-09-25-i állapot):

> „When the memory tool is enabled, Claude automatically checks its memory directory before starting a task. As it works, Claude stores what it learns in files under /memories and reads them back in later conversations to continue earlier work."

Forrás: https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool (T1, hivatalos dokumentáció). Megjegyzés: ez a jelenlegi szöveg már nem tartalmazza a korábbi, erősebb, csupa nagybetűs kényszerítő megfogalmazást, amit a Saha-cikk idéz („Anthropic's memory tool force-injects an all-caps directive to check memory before anything else") — ezt magam nem tudtam szó szerint visszaigazolni az élő oldalon, csak a jelenlegi, enyhébb, de tartalmilag azonos irányú („automatically checks") megfogalmazást; ez konzisztens az ELL05-jelentés (2026-09-25) hasonló, korábbi vizsgálati körben tett megfigyelésével, miszerint a gyártói dokumentáció szövege gyorsan változik.

**GitHub Copilot Memory** (hivatalos blog, 2026-01-15):

> „When an agent starts a new session, we retrieve the most recent memories for the target repository and include them in the prompt. Future implementations will enable additional retrieval techniques, such as a search tool and weighted prioritization."

Forrás: https://github.blog/ai-and-ml/github-copilot/building-an-agentic-memory-system-for-github-copilot/ (T1, hivatalos gyártói blog). Vagyis a Copilot Memory **olvasási/felidézési oldalon nem bízik az agent önkéntes döntésében** — automatikusan befűzi a memóriákat session indításkor —, míg az írás (memória létrehozása) explicit ágensi eszközhívásként van implementálva: „We implemented memory creation as a tool that agents can invoke when they discover something that's likely to have actionable [value]" (ugyanott).

Ez a mintázat — automatikus injektálás olvasásra/felidézésre, önkéntes eszköz csak írásra — megegyezik a Saha-cikk „delivery, not storage" architektúrájának alapelvével, függetlenül attól, hogy a két cél (Anthropic memory tool, GitHub Copilot Memory) egymástól függetlenül, eltérő csapatoktól, eltérő időpontban született.

## 3. Dokumentált felhasználói tapasztalat

### 3.1 GitHub-hibajegyek — karbantartói megerősítéssel

**alioshr/memory-bank-mcp #24 — „Why memory bank don't work in Claude code?"** (2025-08-18, lezárva). A felhasználó hetekig használta a Claude Code-ot anélkül, hogy a memória-MCP fájlokat írt volna:

> „I got it, I thought it's an automatic tool, but it's not... why don't you make it automatic?"

A karbantartó (a projekt szerzője) válasza:

> „One cannot enforce an MCP tool to be called by an LLM if not through a 'wrapper' (like Cline for instance). Even with an AI 'wrapper' there is no guarantee that an LLM will follow instructions. LLMs are non deterministic... Did you add the custom instructions mentioned in the docs to claude code? LLMs tend to follow them and always consult the memory bank when planning work."

Forrás: https://github.com/alioshr/memory-bank-mcp/issues/24 (T2 — elsőkézi GitHub-hibajegy, karbantartói válasszal). Ez a maintainer explicit, technikai indoklással ellátott megerősítése annak, hogy egy MCP-eszköz önkéntes hívása nem garantálható, és a bevett munkakörüli megoldás egy külső kényszerítő mechanizmus (custom instructions / wrapper).

**doobidoo/mcp-memory-service #14 — „Memory awareness in context"** (2025-03-24, „completed" néven lezárva). A felhasználó azért kért funkciót, mert az agent nem volt tisztában azzal, hogy egyáltalán van memóriája:

> „I'm wondering if there's any way to inject into the default context of each chat a selected list of topics or tags stored in memory... If there was a way to inject custom instructions 'You have a searchable memory.'"

A karbantartó válasza megerősíti, hogy a natív MCP-protokoll nem old meg ilyet, és külön eszközt épített a probléma megkerülésére:

> „While direct context injection isn't part of the MCP protocol, there are several creative ways we could implement this functionality... I've implemented a solution to this issue by creating a dedicated utility: Claude Memory Context... it allows Claude to have memory awareness at the start of conversations without modifying the MCP protocol."

Forrás: https://github.com/doobidoo/mcp-memory-service/issues/14 (T2). Ugyanennek a repónak egy másik, 2026-os hozzászólása (Exa-találat, nem külön lehívott issue) direkt összeveti a passzív vs. akció-orientált eszközleírásokat, és a mem0/OpenMemory imperatív megfogalmazását javasolja mintaként:

> „These leave it entirely up to the LLM to decide when to call, which often means they don't get called at all... OpenMemory's MCP server uses action-oriented descriptions: 'search_memory: This method is called EVERYTIME the user asks anything.'"

Forrás (Exa-keresési kivonat, github.com/doobidoo/mcp-memory-service, README/issue-szál, pontos URL a keresési találatban nem volt önállóan azonosítható — ezt T3-ként, nem önállóan visszaellenőrzött forrásként kezelem).

**mem0ai/mem0 #5413 — „Provide one-click hooks + MCP setup for Claude Code / Codex with self-hosted Mem0"** (2026-06-07, nyitott). A kérés maga is abból indul ki, hogy pusztán a statikus instrukciós fájl nem elég:

> „3. Rely only on CLAUDE.md or AGENTS.md — Static instruction files can remind the agent to use memory, but they do not provide automatic memory retrieval / persistence. Hooks are a better fit for dynamic memory injection."

Forrás: https://github.com/mem0ai/mem0/issues/5413 (T2 — nyitott hibajegy/feature request, a mem0 karbantartója triázsolta, nem vitatta az alapállítást).

### 3.2 Cursor közösségi fórum

**„A connected memory server can still do nothing in Cursor"** (2026-09-12):

> „I connected a memory MCP server to Cursor, saw the green status, and assumed the agent would start remembering. It didn't... The connection only gives the agent tools. It still needs an operating rule for when to call them."

Forrás: https://forum.cursor.com/t/a-connected-memory-server-can-still-do-nothing-in-cursor/171402 (T3 — közösségi fórumbejegyzés).

**„My AI doesnt like MCP and use its own lol... issue?"** (2025-04-14) — itt a felhasználó azt írja le, hogy hosszabb beszélgetés után az agent nem hívja a memória-MCP-t, hanem egy kitalált, saját belső „MCP memóriát" imitál a válaszában:

> „During the first few messages when I start a new chat the AI use the MCP server correctly but after a while it might forget to use it and when I tell it to use the MCP server for his memory he just makes his own ''MCP Memory''... So instead of calling the tool to access the MCP server it thinks that it can create an internal MCP memory?"

Forrás: https://forum.cursor.com/t/my-ai-doesnt-like-mcp-and-use-its-own-lol-issue/79201 (T3).

Több további Cursor-fórum bejegyzés (T3) dokumentálja a natív „Memories" funkció megbízhatatlanságát (nem feltétlenül önkéntesség kérdése, inkább regresszió/hibakérdés, de ugyanazt a felhasználói frusztrációs mintát erősíti): https://forum.cursor.com/t/tool-update-memory-not-found/132487 , https://forum.cursor.com/t/cursor-memory-doesnt-longer-work/136128 , https://forum.cursor.com/t/agents-have-lost-access-to-memory-capability/143310 . Ez utóbbiban egy Cursor-alkalmazott elismeri: „Hey, thanks for the report. This is a known recurring issue that's affecting multiple users."

### 3.3 Gyakorlati beszámoló több keretrendszerről (T3, önálló, nem lektorált)

Egy gyakorló fejlesztő „hat hónap éles használat, két agent-keretrendszer" tapasztalatát összegző GitHub-repója (nem tudományos publikáció, hanem dokumentált saját eset) a jelenséget „Ground Truth Gap"-nek nevezi:

> „This gap is systemic. It affects every memory architecture I've tested across two major agent frameworks over six months of production use. And it's not a pipeline bug — it's an identity bug... The infrastructure of memory works perfectly. The pipeline captures, stores, retrieves, and injects. But the agent doesn't use the injected context — because nothing in its identity tells it to."

Forrás: https://github.com/ClaudioDrews/ground-truth-gap (T3 — egyetlen szerző, nem lektorált, nem független validált mérés, csak beszámoló).

### 3.4 Mintázat összegzése

Mind a négy egymástól független projekt (memory-bank-mcp, mcp-memory-service, mem0, Cursor natív Memories) és a fenti gyakorlati beszámoló **ugyanazt a mintát** dokumentálja: (1) a felhasználó feltételezi, hogy a csatlakoztatott memória-eszközt az agent automatikusan, önkéntesen használni fogja; (2) tapasztalja, hogy nem így történik; (3) a karbantartó vagy a közösség válasza mindig valamilyen **kényszerítő mechanizmus** (custom instructions/CLAUDE.md, hook, wrapper, identitás-dokumentum-szintű szabály) felé mutat, nem pedig „várj, a modell úgyis megtanulja". Ez négy egymástól **független forrásból** (más MCP-szerver, más karbantartó, más felhasználói bázis) konvergáló mintázat, ami önmagában — bár mindegyik T2/T3 szintű, anekdotikus forrás — erősíti a Saha-cikk és a MEMTRACK kontrollált eredményeinek külső érvényességét.

## 4. Ellenérvek: mikor működik jól az önkéntes használat, és mitől függ?

Nem találtam olyan kontrollált mérést, amely azt mutatná, hogy az önkéntes memória-MCP-hívás **önmagában, kényszerítő mechanizmus nélkül** megbízhatóan működik. Az alábbi források azonban konkrét tényezőket azonosítanak, amelyek **javítják** (de nem oldják meg teljesen) a helyzetet:

**(a) Akció-orientált, imperatív eszközleírás.** A doobidoo/mcp-memory-service közösségi javaslata konkrét összehasonlítást tesz a passzív és az akció-orientált eszközleírás között, az OpenMemory (mem0) mintájára hivatkozva, amely explicit „EVERYTIME" (mindig) megfogalmazást használ a leírásban a „lehet használni" helyett — ez azonban egy **javaslat**, nem egy előtte-utána mért, kontrollált eredmény (l. 3.1, T3).

**(b) Injektálás utáni önkéntes folytatás.** A Saha-cikk egyetlen, de kontrollált megfigyelése szerint az injektálás **kiváltja** a további önkéntes memóriaműveleteket, míg pusztán a tudás tárban léte (injektálás nélkül) nem:

> „Voluntary memory operations occur after and because of delivery, not instead of it."

Forrás: https://arxiv.org/html/2607.20972v1, §5.2 (l. 1.3 fent). Ez azt sugallja, hogy az önkéntes használat nem „soha nem történik meg" jelenség, hanem jellemzően egy előzetes, nem-önkéntes felidézési eseményhez kötött láncreakció.

**(c) Explicit, konkrét horgony (anchor) a mikor-triggerre.** A TriggerBench szerint a modellek proaktív felidézése akkor sikeresebb, ha a kiváltó feltétel explicit, de ennek ára van: túl erős, általános „mindig emlékeztess" instrukció túltriggerelést (hamis riasztást) okoz:

> „models struggle to maintain situational awareness without explicit anchors (implicit vs. explicit constraints)... models may overfit to an 'always-remind' heuristic."

Forrás: https://arxiv.org/abs/2606.23459 (l. 2.2 fent). Ez azt jelzi, hogy a „mikor" kérdésre adott válasz (explicit horgonyok) egy trade-off: javítja a felidézést, de rontja a pontosságot/precizitást.

**(d) Identitás-szintű, kötelező hierarchia-szabály (anekdotikus).** A „Ground Truth Gap" beszámoló szerint az injektált memóriablokkok explicit rangsorolása a modell identitás-dokumentumában (pl. „injected context > memory API results > model training knowledge") mérhető viselkedésváltozást hozott a gyakorlatban tesztelt két keretrendszerben:

> „The fix is not in the pipeline. The fix is in the agent's identity documents — the files that define who the agent is and how it should operate... With the hierarchy, injected memory becomes authoritative. The agent stops rediscovering."

Forrás: https://github.com/ClaudioDrews/ground-truth-gap (T3 — egyetlen szerző saját, nem kontrollált, nem független validálású megfigyelése, előtte-utána mérőszám nélkül).

**(e) Operatív szabály/„loop" kézzel felírva a promptba (Cursor-közösségi tanács).** A Cursor-fórum bejegyzés konkrét, felhasználó által kidolgozott szabályokat ad meg arra, mikor kell keresni/menteni, de maga a szerző is jelzi, hogy ez pótlás, nem megoldás a mögöttes problémára: „The connection only gives the agent tools. It still needs an operating rule for when to call them" (l. 3.2 fent, T3).

**Egy gyártói termék marketing-állítása, amit nem tudtam függetlenül ellenőrizni:** a `codex-agent-mem` MCP-szerver README-je azt állítja, hogy megfelelő konfiguráció mellett az agent proaktívan, emlékeztetés nélkül használja a memóriát: „Once configured, the agent should use codex-agent-mem proactively when continuity matters. You should not need to repeat 'use the memory MCP' every few turns." (https://github.com/MarceloCaporale/codex-agent-mem, T3). Ehhez az állításhoz **semmilyen mért adatot, benchmarkot vagy előtte-utána összehasonlítást nem közöl a repó** — önmagában áll a fentebb dokumentált, ellentétes irányú, jóval szélesebb körű tapasztalati mintázattal szemben.

## Ellentmondások

- **„Nulla hívás" (Saha) vs. „redundáns, de nem nulla hívás" (MEMTRACK).** A Saha-cikk fő állítása, hogy a legerősebb önkéntes ágban (V, n=1) az agent **egyetlen** memóriahívást sem tett 114 körben. A MEMTRACK ezzel szemben azt találja, hogy a memóriaeszközzel felszerelt modellek **igenis hívják** a memóriakomponenst, csak redundánsan és hatékonytalanul: „LLMs with memory tools consistently display increased redundancy as well as drop in performance efficiency" (https://arxiv.org/abs/2510.01353). A két forrás nem közvetlenül cáfolja egymást — más feladatkör (egyetlen kódolási feladat vs. vállalati többplatformos QA), más memória-architektúra (cue-anchored, harness-vezérelt tár vs. Mem0/Zep query-time retrieval) —, de a „soha nem hívja" és a „túl gyakran, rosszul hívja" két, tartalmilag eltérő hibaüzemmód, amit érdemes megkülönböztetni, nem egy jelenségként kezelni.
- **Marketing-állítás (codex-agent-mem: „nem kell emlékeztetni") vs. a dokumentált mintázat túlnyomó többsége** (Saha, MEMTRACK, alioshr/memory-bank-mcp, doobidoo/mcp-memory-service, mem0, Cursor-fórum), amely szerint az önkéntes, kényszerítés nélküli használat megbízhatatlan. A codex-agent-mem állítását semmilyen közölt mérőszám nem támasztja alá — ellentétben áll a többi, forrásolt tapasztalattal, de mivel egyik oldal sem kontrollált, publikált mérés (a codex-agent-mem README esetében), ezt inkonzisztenciaként, nem cáfolatként rögzítem.
- **Az Anthropic memory tool dokumentációjának jelenlegi (2026-09-25) szövege** („Claude automatically checks its memory directory before starting a task") enyhébb megfogalmazású, mint amit a Saha-cikk idéz („force-injects an all-caps directive"). Nem tudtam eldönteni, hogy ez a Saha-cikk pontatlansága, vagy a dokumentáció azóta megváltozott (ez utóbbi valószínűbb, az ELL05-jelentés hasonló megfigyelést tett más idézetre nézve ugyanezen az oldalon) — erre nézve NEM ELDÖNTHETŐ, melyik forgatókönyv áll fenn.

## Amire NINCS forrás

- **NINCS FORRÁS** olyan publikált, kontrollált kísérletre, amely azonos protokollal, azonos feladaton **több** kódoló-agent-terméket (Claude Code, Codex, Cursor, Gemini CLI, Copilot) egyszerre hasonlítana össze az önkéntes memória-/tudás-MCP-hívási arány szempontjából.
- **NINCS FORRÁS** semmilyen gyártó (Anthropic, OpenAI, Google, GitHub/Microsoft) által nyilvánosan közölt, konkrét százalékos „önkéntes hívási arány" számra a saját memóriarendszerükre nézve; a fellelt gyártói számok (pl. Anthropic 84%/39%, l. ELL05) teljesítmény- és token-megtakarítási mutatók, nem hívási gyakoriság.
- **NINCS FORRÁS** a Saha-cikk (arXiv:2607.20972) független tudományos citációjára, replikációjára vagy formális szakmai cáfolatára — a Semantic Scholar-keresés nem hozott találatot, és a fellelt másodlagos feldolgozás (codex.danielvaughan.com) sem tudományos, sem kritikai jellegű.
- **NINCS FORRÁS** kontrollált mérésre a Gemini CLI vagy a GitHub Copilot CLI önkéntes memória-MCP-hívási arányáról; a Copilot Memory esetében csak a tervezési döntést (automatikus injektálás olvasásra) dokumentáltam, mért hívási arányt nem.
- **NEM ELDÖNTHETŐ**, hogy a doobidoo/mcp-memory-service repóban talált „OpenMemory vs. mcp-memory-service tool description" összehasonlítás (3.1 (a) pont) pontos GitHub-issue-URL-je melyik — az Exa-keresés kivonatolt szöveget adott, önálló, közvetlen lehívással nem tudtam megerősíteni a pontos issue-számot vagy dátumot; ezt a forrást ezért T3-ként, alacsonyabb megbízhatósággal kezelem, és második független forrással nem tudtam megerősíteni.

## Meglátogatott és felderített linkek

| Cím | URL | Tier | Eszköz | Megjegyzés |
|---|---|---|---|---|
| Delivery, Not Storage (Saha, absztrakt) | https://arxiv.org/abs/2607.20972 | T2 | Exa fetch | Fő elsődleges forrás, §1–§8 teljes egészében lehívva |
| Delivery, Not Storage (PDF) | https://arxiv.org/pdf/2607.20972 | T2 | Exa fetch | |
| Delivery, Not Storage (teljes HTML, §1–§8 + hivatkozások) | https://arxiv.org/html/2607.20972v1 | T2 | Exa fetch | Minden szó szerinti idézet innen |
| Vectr repó — a cikk markdown-változata és kódja | https://github.com/swapnanil/vectr/blob/main/research/brain-memory/delivery-not-storage.md | T2 | Exa search | Megerősíti a kód/adat elérhetőségét; a nyers futásadatokat nem futtattam le |
| Delivery, Not Storage — Hugging Face Papers | https://huggingface.co/papers/2607.20972 | T3 | Exa search | Aggregátor, érdemi vita nem található |
| Codex Knowledge Base — Daniel Vaughan blogja a Saha-cikkről | https://codex.danielvaughan.com/2026/07/28/cue-anchored-working-memory-harness-property-coding-agents-codex-cli-compaction-decay-deterministic-injection/ | T3 | Exa search | Másodlagos összefoglaló, nem kritikai |
| MEMTRACK (absztrakt + RQ1–RQ3) | https://arxiv.org/abs/2510.01353 | T1/T2 | Exa fetch | Független szerzők, más feladatkör, megerősíti a mintázatot |
| MEMTRACK (OpenReview PDF) | https://openreview.net/pdf?id=mVxmbMng4B | T1 | Exa search | |
| MEMTRACK — NeurIPS 2025 diák | https://neurips.cc/media/neurips-2025/Slides/124523.pdf | T1 | Exa search | Konferencia-prezentáció léte megerősítve |
| MEMTRACK — Patronus AI blog | https://www.patronus.ai/blog/memtrack | T3 | Exa search | Gyártói/szerzői blog, ugyanazok a szerzők |
| TriggerBench (absztrakt + Related Works) | https://arxiv.org/abs/2606.23459 | T1/T2 | Exa fetch | Microsoft Research társszerzőség |
| Memory tool — Claude Docs (élő oldal, 2026-09-25) | https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool | T1 | Exa fetch | „automatically checks its memory directory" |
| Building an agentic memory system for GitHub Copilot | https://github.blog/ai-and-ml/github-copilot/building-an-agentic-memory-system-for-github-copilot/ | T1 | Exa search | Hivatalos gyártói blog, 2026-01-15 |
| About GitHub Copilot Memory | https://docs.github.com/en/copilot/concepts/agents/copilot-memory | T1 | Exa search | Hivatalos dokumentáció |
| VS Code Copilot memory dokumentáció | https://github.com/microsoft/vscode-docs/blob/538f9c60/docs/agents/memory.md | T1 | Exa search | Helyi memory tool vs. Copilot Memory összevetése |
| memoryInstructions injektálási hiba (VS Code) | https://github.com/microsoft/vscode/issues/321833 | T2 | Exa search | Mutatja, hogy a gyártó rendszerprompt-szintű kényszerítést használ |
| alioshr/memory-bank-mcp #24 | https://github.com/alioshr/memory-bank-mcp/issues/24 | T2 | Exa fetch | Karbantartói megerősítés: „LLMs are non deterministic" |
| doobidoo/mcp-memory-service #14 | https://github.com/doobidoo/mcp-memory-service/issues/14 | T2 | Exa fetch | Karbantartó külön eszközt épített a probléma megkerülésére |
| doobidoo/mcp-memory-service README (v6.13.0) | https://github.com/doobidoo/mcp-memory-service/blob/fd0bcca.../README.md | T3 | Exa search | Termékleírás, nem független mérés |
| mem0ai/mem0 #5413 | https://github.com/mem0ai/mem0/issues/5413 | T2 | Exa fetch | „Static instruction files... do not provide automatic memory retrieval" |
| Cursor fórum — „A connected memory server can still do nothing" | https://forum.cursor.com/t/a-connected-memory-server-can-still-do-nothing-in-cursor/171402 | T3 | Exa search | |
| Cursor fórum — „My AI doesnt like MCP and use its own" | https://forum.cursor.com/t/my-ai-doesnt-like-mcp-and-use-its-own-lol-issue/79201 | T3 | Exa search | Hallucinált „belső MCP memória" jelenség |
| Cursor fórum — „Tool update_memory not found” | https://forum.cursor.com/t/tool-update-memory-not-found/132487 | T3 | Exa search | |
| Cursor fórum — „Cursor memory doesnt longer work” | https://forum.cursor.com/t/cursor-memory-doesnt-longer-work/136128 | T3 | Exa search | |
| Cursor fórum — „Agents have lost access to memory capability” | https://forum.cursor.com/t/agents-have-lost-access-to-memory-capability/143310 | T3 | Exa search | Cursor-alkalmazott elismeri: „known recurring issue" |
| ClaudioDrews/ground-truth-gap | https://github.com/ClaudioDrews/ground-truth-gap | T3 | Exa fetch | Egyszerzős gyakorlati beszámoló, hat hónap, két keretrendszer |
| anand-92/gemdex README | (Exa-keresési kivonat, „nikships/gemdex") | T3 | Exa search | „Agents won't reach for a new MCP tool on their own." |
| MarceloCaporale/codex-agent-mem README | https://github.com/MarceloCaporale/codex-agent-mem | T3 | Exa search | Ellenőrizetlen marketingállítás a proaktív használatról |
| openai/codex #19663 | https://github.com/openai/codex/issues/19663 | T2 | Exa search | Tangenciális: beépített memória blokkolja a memória-MCP hívásokat |
| kenhuangus/agent-memory-harness — Codex fejezet | https://github.com/kenhuangus/agent-memory-harness/blob/main/docs/harnesses/03-codex.md | T3 | Exa search | Codex architektúra: nincs push-injektálás, csak model-pulled retrieval |

---

# SQ08 — Automatikus beadás kérdésenként: mechanika, költség, mérések

**Módszertani megjegyzés (degradált mód):** Ez a kutatás is egyetlen kutató-ügynökként készült, alügynökek indítása nélkül (a `deep-web-research` skill többügynökös pipeline-ja helyett szekvenciális Exa-kereséssel/olvasással). Kizárólag `mcp__Exa__web_search_exa` és `mcp__Exa__web_fetch_exa` eszközöket használtam. A munkamenet-indító (`SessionStart`) hookok mechanikáját a sq03-kutatás már feltárta, azt itt nem ismétlem meg — ez a fájl kifejezetten a **kérdésenkénti** (minden felhasználói üzenetnél lefutó) hookra, a rá épülő memória-beadó megoldásokra és ezek mért hatására fókuszál. Mai dátum: **2026-09-25**.

---

## Rövid válasz

Mind a hat kliensnek van kérdésenkénti hookja, és mindegyik megkapja a felhasználó promptjának szövegét, de a beadási képességük élesen eltér. **Claude Code** (`UserPromptSubmit`), **Codex** (`UserPromptSubmit`) és **Gemini CLI** (`BeforeAgent`) tud `additionalContext`-et injektálni a promptra épülve, és mindháromnál van dokumentált kimeneti korlát (Claude Code: 10 000 karakter, gyakorlatban ~2000 a túllépéskor; Codex: ~2500 token, konfigurálható; Gemini CLI-nél a korlátra NINCS FORRÁS). **Cursor** `beforeSubmitPrompt` hookja viszont — jelenleg dokumentáltan és hivatalos fórum-visszaigazolással is — **nem tud kontextust injektálni**, csak blokkolhatja a beadást (`continue`/`user_message`); ez nyílt feature-kérés. **Antigravity**-nek nincs önálló, a promptra szűkített hookja: a legközelebbi analóg a `PreInvocation`, ami minden modellhívásnál lefut (nem csak a felhasználói üzenetnél), és `injectSteps`/`ephemeralMessage` formában tud beszúrni. **GitHub Copilot**-nál kettéválik a kép: a VS Code Agent mód és a Copilot CLI konfig-fájl alapú `UserPromptSubmit`/`userPromptSubmitted` hookja csak `command` (és a felhő-ügynöknél `http`) típusú lehet, viszont a hivatalos dokumentáció szerint a config-fájlból indított hook kimenete (`additionalContext` is) **el van dobva** — csak a programozott (SDK-alapú, TypeScript) hook tudja ténylegesen visszaadni az `additionalContext`-et. Közvetlen HTTP-hívást és fejlécküldést csak a Claude Code (`type: "http"`) és a GitHub Copilot (`type: "http"`, csak felhő-ügynöknél) hookja tud natívan; a többi kliens csak shell-parancsot indíthat, amin belül a szkript persze curl-lel HTTP-t hívhat. Az időkorlátok szórnak (Claude Code UserPromptSubmit: 30s; Codex: 600s alapértelmezett; Gemini CLI: 60s; VS Code/Copilot: 30s; Antigravity: 30s), és a hibakezelés architektúránként eltér: van, ahol a lassú/hibás hook **fail-open** (a promptot mindenképp továbbengedi — GitHub Copilot explicit dokumentálja ezt, Claude Code `PreToolUse`-nál is ez a szabály timeoutra), és van, ahol a hiba **blokkolja** a promptot (exit code 2 mindenhol blokkol). Létező megoldások (claude-mem, mem0 plugin, supermemory, memdb) mind a `UserPromptSubmit`-ra épülnek, tipikusan top-5 találatot adnak be relevancia-küszöbbel (memdb: 0,85 MMR-küszöb; claude-mem: Chroma szemantikus top-5, ~800–1200 token), és rövid promptokat kihagynak a zajszűrés miatt. Az arXiv:2607.20972 (Delivery, Not Storage) mellett a Mem0-cikk (arXiv:2504.19413) és egy kifejezetten kódoló-ügynöki memóriára fókuszáló, kockázat-érzékeny kontroller cikk (arXiv:2604.27283) adnak számszerű mérést a rossz célzású beadás káráról — utóbbi kifejezetten azt méri, hogy egy hamis pozitív (téves) memória-beadás nagyobb kárt okoz a hibajavításban, mint egy kihagyott (releváns, de be nem adott) memória.

---

## 1. Kérdésenkénti hookok kliensenként

### 1.1 Claude Code — `UserPromptSubmit`

Hivatalos, dedikált esemény, ami minden fordulónál (nem munkamenetenként) lefut:

> "once per turn: `UserPromptSubmit`, `Stop`, and `StopFailure`" — https://code.claude.com/docs/en/hooks

> "`UserPromptSubmit` | When you submit a prompt, before Claude processes it" — https://code.claude.com/docs/en/hooks

**Megkapja a prompt szövegét** stdinen JSON-ban (`prompt` mező) — ezt az SQ03-ban már idézett input-sémán túl a mem0/claude-mem hook-implementációi is megerősítik (lásd 2. szakasz).

**Visszaadhat szöveget a kontextusba**, `hookSpecificOutput.additionalContext` formában:

> "The `additionalContext` field passes a string from your hook into Claude's context window. Claude Code wraps the string in a system reminder and inserts it into the conversation at the point where the hook fired." — https://code.claude.com/docs/en/hooks.md

> "UserPromptSubmit and UserPromptExpansion: alongside the submitted prompt" [hol jelenik meg a reminder] — https://code.claude.com/docs/en/hooks.md

Sima stdout is elfogadott (exit 0), ez az `UserPromptSubmit` (és a `SessionStart`) speciális esete:

> "UserPromptSubmit/SessionStart: stdout added as context for Claude" — https://claude.yourdocs.dev/docs/claude-code/hooks

**Kimeneti korlát: 10 000 karakter** (megerősítve, ismétlésképp az SQ03-ból, mert ugyanaz a korlát vonatkozik `UserPromptSubmit`-ra is), de van egy dokumentált **funkcionalitás-hiba**: egy nyílt hibajegy szerint az `additionalContext` a `UserPromptSubmit`-nál néha **egyáltalán nem** jut el a modellhez, ha nem sima stdout, hanem a JSON `hookSpecificOutput.additionalContext` útvonalat használják:

> "Hook returning `{\"additionalContext\": \"...\"}` from `UserPromptSubmit` produces valid JSON but the content is never surfaced to the assistant. […] Use plain stdout (e.g., `echo \"user-message-submitted: $TS\"`), which surfaces correctly as a `system-reminder`." — https://github.com/anthropics/claude-code/issues/52876

Egy másik hibajegy szerint az `additionalContext` **nem ephemeralis**, hanem minden fordulónál **felhalmozódik** a történetben ahelyett, hogy lecserélné az előzőt:

> "`UserPromptSubmit` hook output with `additionalContext` accumulates in the conversation history instead of being replaced on each new message. Every user message adds another ` ` block, and previous ones remain visible to the model." — https://github.com/anthropics/claude-code/issues/40216

**HTTP-végpont közvetlenül hívható**, natív `type: "http"` hook-kal (a hivatalos doksi a `UserPromptSubmit`-ot is a `timeout` táblázat része, tehát a HTTP hook-típus rá is vonatkozik):

> "Hooks are user-defined shell commands, HTTP endpoints, or LLM prompts that execute automatically at specific points in Claude Code's lifecycle." — https://code.claude.com/docs/en/hooks.md

> "For command hooks, input arrives on stdin. For HTTP hooks, it arrives as the POST request body." — https://code.claude.com/docs/en/hooks.md

Fejléc küldhető, és a whitelist-mechanizmus külön van dokumentálva:

> "`allowedHttpHookUrls`: when defined at any settings level, Claude Code runs an HTTP hook handler only if its URL matches the merged allowlist" / "`httpHookAllowedEnvVars`: when defined, Claude Code interpolates only the environment variables on that list into hook headers" — https://code.claude.com/docs/en/hooks.md

**Időkorlát**: a `UserPromptSubmit` a `command`/`http`/`mcp_tool` alapértelmezett 600 másodpercet **30-ra csökkenti**:

> "Defaults: 600 for `command`, `http`, and `mcp_tool`; 30 for `prompt`; 60 for `agent`. `UserPromptSubmit` lowers the `command`, `http`, and `mcp_tool` default to 30" — https://code.claude.com/docs/en/hooks.md

**Hibakezelés / timeout hatás**: `UserPromptSubmit`-nál a hook **blokkolhat** exit code 2-vel (a prompt törlődik a kontextusból), de ha maga a hook **timeoutol**, a kimenete eldobódik és nem hoz döntést — ez a `PreToolUse`-ra dokumentált szabály (a `UserPromptSubmit` ugyanazon `command`/`http`/`mcp_tool` family tagja):

> "A `command`, `http`, or `mcp_tool` hook that reaches its `timeout` is canceled: Claude Code discards the hook's output, and the hook renders no decision." — https://code.claude.com/docs/en/hooks

> "`UserPromptSubmit` | Yes | Blocks prompt processing and erases the prompt" [exit code 2 hatása] — https://code.claude.com/docs/en/hooks

Tehát: **normál exit 2 → blokkol**, **timeout → fail-open (a prompt átmegy, mintha a hook nem is futott volna)**.

### 1.2 Codex CLI — `UserPromptSubmit`

Hivatalos esemény, minden fordulónál fut:

> "| During a turn | `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`, `UserPromptSubmit`, `SubagentStop`, `Stop` |" — https://developers.openai.com/codex/hooks

**Megkapja a prompt szövegét**, forráskód szerint is:

> "```rust\npub struct UserPromptSubmitRequest {\n pub session_id: ThreadId,\n pub turn_id: String,\n pub cwd: AbsolutePathBuf,\n …\n pub prompt: String,\n}\n```" — https://github.com/openai/codex/blob/178c3d30/codex-rs/hooks/src/events/user_prompt_submit.rs

> "| `prompt` | `string` | User prompt that's about to be sent |" — https://developers.openai.com/codex/hooks

**Visszaadhat szöveget** `hookSpecificOutput.additionalContext` formában, sima szöveges stdout is elfogadott (nem-JSON stdout → automatikusan additionalContext-té alakul):

> "```json\n{\n \"hookSpecificOutput\": {\n \"hookEventName\": \"UserPromptSubmit\",\n \"additionalContext\": \"Ask for a clearer reproduction before editing files.\"\n }\n}\n```\nThat `additionalContext` text is added as extra developer context." — https://developers.openai.com/codex/hooks

Forráskód szerint: `else { let additional_context = trimmed_stdout.to_string(); … }` — sima szöveges stdout is `additionalContext`-té alakul (nem csak JSON) — https://github.com/openai/codex/blob/178c3d30/codex-rs/hooks/src/events/user_prompt_submit.rs

**Kimeneti korlát: ~2500 token** (SQ03-ból ismételve, mert kifejezetten a `UserPromptSubmit`-ra is vonatkozik):

> "This applies to additional context from `SessionStart`, `SubagentStart`, `PreToolUse`, `PostToolUse`, and `UserPromptSubmit`, feedback from `PostToolUse`, and continuation prompts from `Stop` and `SubagentStop`." — https://developers.openai.com/codex/hooks

**HTTP-végpont közvetlenül NEM hívható natívan** — a Codex hookjai jelenleg kizárólag `"command"` (shell) típusúak:

> "Only `type: \"command\"` handlers run today. `prompt` and `agent` handlers are parsed but skipped." — https://developers.openai.com/codex/hooks

**Időkorlát**: a `UserPromptSubmit` a doksi mintapéldájában nincs külön `timeout`-tal megadva, tehát az általános 600 másodperces alapértelmezés vonatkozik rá (a `SessionEnd` az egyetlen dokumentált kivétel):

> "`timeout` is in seconds. If `timeout` is omitted, Codex uses `600` seconds for most hooks. `SessionEnd` uses `1` second by default and supports up to `3` seconds." — https://developers.openai.com/codex/hooks

Forráskód megerősíti, hogy timeoutkor a hook `outcome: "timeout"`-tal, hibaüzenettel tér vissza:

> "Err(_) => finish_command_run(…, error: Some(format!(\"hook timed out after {}s\", handler.timeout_sec)), outcome: \"timeout\", …)" — https://github.com/openai/codex/blob/main/codex-rs/hooks/src/engine/command_runner.rs

**Hibakezelés**: exit code 0 + `decision: "block"` (nem-üres `reason`-nel) blokkol; exit code 2 + stderr szintén blokkol; más nem-nulla exit code → a hook `Failed` státuszú, de a forráskódból nem derül ki explicit "fail-open/fail-closed" szemantika a `UserPromptSubmit`-ra nézve — a teszt-esetek szerint sikertelen parse/hiba esetén `should_stop: false` (tehát a prompt **átmegy**, ha a hook technikailag hibázik, csak a `decision:"block"` állítja meg explicit módon):

> "```rust\nfn claude_block_decision_requires_reason() { … assert_eq!(parsed.data, UserPromptSubmitHandlerData { should_stop: false, stop_reason: None, additional_contexts_for_model: Vec::new() }); assert_eq!(parsed.completed.run.status, HookRunStatus::Failed); …}\n```" — https://github.com/openai/codex/blob/178c3d30/codex-rs/hooks/src/events/user_prompt_submit.rs

### 1.3 Gemini CLI — `BeforeAgent`

A Gemini CLI-nél nincs `UserPromptSubmit` néven, hanem `BeforeAgent` a megfelelő hook:

> "### `BeforeAgent`\nFires after a user submits a prompt, but before the agent begins planning. Used for prompt validation or injecting dynamic context." — https://geminicli.com/docs/hooks/reference/

**Megkapja a prompt szövegét**:

> "Input Fields: `prompt`: (`string`) The original text submitted by the user." — https://geminicli.com/docs/hooks/reference/

**Visszaadhat szöveget**, de fontos megkötéssel — csak az adott fordulóra érvényes, nem a teljes beszélgetéshez adódik hozzá:

> "`hookSpecificOutput.additionalContext`: Text that is **appended** to the prompt for this turn only." — https://github.com/google-gemini/gemini-cli/blob/d2cd12a7/docs/hooks/reference.md

Blokkolás két módon: `decision: "deny"` (a prompt törlődik, nem kerül a történetbe) vagy `continue: false` (blokkol, de bekerül a történetbe):

> "`decision`: Set to `\"deny\"` to block the turn and **discard the user's message** (it will not appear in history). `continue`: Set to `false` to block the turn but **save the message to history**." — https://github.com/google-gemini/gemini-cli/blob/d2cd12a7/docs/hooks/reference.md

**HTTP-végpont közvetlenül NEM hívható natívan** — csak `"command"` típus:

> "| `type` | string | Yes | The execution engine. Currently only `\"command\"` is supported. |" — https://geminicli.com/docs/hooks/reference/

**Kimeneti korlát: NINCS FORRÁS** — sem a hivatalos reference, sem a writing-hooks útmutató nem ad meg konkrét karakter-/token-plafont az `additionalContext`-re (megerősítve SQ03-ból, és ez a `BeforeAgent`-re is igaz marad).

**Időkorlát: 60 000 ms (60 s) az alapértelmezett**, forráskódból és doksiból is megerősítve:

> "/**\n * Default timeout for hook execution (60 seconds)\n */\nconst DEFAULT_HOOK_TIMEOUT = 60000;" — https://github.com/google-gemini/gemini-cli/blob/d2cd12a7/packages/core/src/hooks/hookRunner.ts

> "`timeout` | `number` | No | Execution timeout in milliseconds (default: 60000)." — https://geminicli.com/docs/hooks/reference/

**Hibakezelés**: exit code 0 → stdout JSON-ként parszolva; exit code 2 → "System Block" (a stderr a blokkolás oka, a hívást/fordulót megszakítja); minden más nem-nulla kód → **nem-blokkoló figyelmeztetés**, a CLI folytatja:

> "0: Success. `stdout` is parsed as JSON. **Preferred for all logic.** 2: System Block. The action is blocked; `stderr` is used as the rejection reason. Other: Warning. A non-fatal failure occurred; the CLI continues with a warning." — https://geminicli.com/docs/hooks/reference/

Timeoutkor a futtató kód `success: false`-t és hibaüzenetet ad vissza (`Hook timed out after ${timeout}ms`), majd a hívó réteg ezt lényegében a "figyelmeztetés" ághoz hasonlóan, nem-blokkolva kezeli (a forráskódban a timeout külön `error`-ral tér vissza, nem `decision: deny`-vel):

> "resolve({ …, success: false, error: new Error(`Hook timed out after ${timeout}ms`), … })" — https://github.com/google-gemini/gemini-cli/blob/d2cd12a7/packages/core/src/hooks/hookRunner.ts

### 1.4 Cursor — `beforeSubmitPrompt`

Van dedikált, kérdésenkénti hook:

> "`beforeSubmitPrompt` - Validate prompts before submission" — https://cursor.com/docs/hooks

> "Called right after user hits send but before backend request. Can prevent submission." — https://cursor.com/docs/hooks.md

**Megkapja a prompt szövegét**:

> "// Input\n{\n \"prompt\": \"<user prompt text>\",\n \"attachments\": [ … ]\n}" — https://cursor.com/docs/hooks.md

**NEM tud szöveget visszaadni a kontextusba** — a hivatalos kimeneti séma jelenleg **csak** két mezőt támogat: `continue` és `user_message`, `additionalContext` **nincs**:

> "// Output\n{\n \"continue\": true | false,\n \"user_message\": \"<message shown to user when blocked>\"\n}" — https://cursor.com/docs/hooks.md

> "| Output Field | Type | Description |\n| --- | --- | --- |\n| `continue` | boolean | Whether to allow the prompt submission to proceed |\n| `user_message` | string (optional) | Message shown to the user when the prompt is blocked |" — https://cursor.com/docs/hooks.md

Ezt egy hivatalos Cursor-válasz külön, expliciten is megerősíti egy fórum-hibajegyben, és egy nyílt feature-kérés is dokumentálja a hiányt:

> "This is actually expected behavior rather than a bug. The `beforeSubmitPrompt` hook currently only supports two output fields: `continue` (boolean) — block or allow the submission, `user_message` (string) — message shown to the user when blocked. It does not support `updated_input` or any field that modifies the prompt text." — https://forum.cursor.com/t/bug-beforesubmitprompt-hook-updated-input-is-silently-stripped-modified-prompt-never-reaches-the-model/158883

> "The `sessionStart` hook can inject `additional_context` into a conversation, but it fires before the user types their first message. The `beforeSubmitPrompt` hook fires after the user submits their message (so we can read it), but it cannot inject context — only block submission. […] Request: Add `additional_context` to the `beforeSubmitPrompt` output schema" — https://forum.cursor.com/t/hooks-allow-beforesubmitprompt-hook-to-inject-additional-context/150707/1

A javasolt kerülőút hivatalosan is a `sessionStart` (egyszeri, session-eleji) vagy a statikus `.cursor/rules` (`alwaysApply: true`), egyik sem kérdésenkénti, dinamikus injektálás:

> "1. `.cursor/rules` with `alwaysApply: true` — this is the most reliable way to inject context into every prompt today. It lacks per-prompt selectivity… 2. `sessionStart` hook with `additional_context`…" — https://forum.cursor.com/t/bug-beforesubmitprompt-hook-updated-input-is-silently-stripped-modified-prompt-never-reaches-the-model/158883

**HTTP-végpont közvetlenül NEM hívható natívan** — a Cursor csak `command` (és `prompt`, LLM-alapú) típusú hookot támogat:

> "Hooks support two execution types: command-based (default) and prompt-based (LLM-evaluated)." — https://cursor.com/docs/hooks.md

**Időkorlát**: nincs kifejezetten dokumentált globális alapérték a `beforeSubmitPrompt`-ra; a `command` hook példákban a `timeout` mező másodpercben adható meg (pl. `"timeout": 30` egy másik hooknál), de a `beforeSubmitPrompt`-ra vonatkozó konkrét alapértelmezett szám **NINCS FORRÁS**.

**Hibakezelés**: a Cursor általános command-hook szabálya szerint nem-nulla, nem-2-es exit code esetén **fail-open** ("action proceeds"):

> "Exit code `0` - Hook succeeded, use the JSON output. Exit code `2` - Block the action (equivalent to returning `permission: \"deny\"`). Other exit codes - Hook failed, action proceeds (**fail-open by default**)." — https://cursor.com/docs/hooks.md

### 1.5 Antigravity — nincs önálló kérdésenkénti hook; a `PreInvocation` a legközelebbi analóg

Az Antigravity hook-rendszeréből — az SQ03-ban már megállapítottak szerint — hiányzik a `SessionStart`, és **nincs olyan esemény sem, ami kifejezetten a felhasználói üzenet beküldéséhez, és csak ahhoz kötődne**. A `PreInvocation` minden modellhívás előtt fut, ami egy fordulón belül több tool-hívásos ciklusban **többször is** lefuthat, nem csak a felhasználói prompt beérkezésekor:

> "`PreInvocation` | Fires before the model is called. | N/A (matcher ignored)" — https://antigravity.google/docs/hooks/

> "Fires before the model is called (starts at 0)." / "`invocationNum` | integer | The 0-indexed sequence number of the current model invocation (the first invocation is 0)." — https://antigravity.google/docs/ide/hooks/

Egy közösségi implementáció (MemPalace) kifejezetten dokumentálja, hogy csak az `invocationNum == 1` (az adott beszélgetés **első** modellhívása) felel meg leginkább a "SessionStart" / kérdésenkénti szemantikának, minden más invokálást szándékosan kihagynak:

> "2. `invocationNum != 1` — we only inject on the first model call of each conversation, mimicking Cursor's `sessionStart` semantics." — https://github.com/MemPalace/mempalace/blob/main/hooks/antigravity/STDIN_SHAPE.md

**Megkapja-e a prompt szövegét?** A `PreInvocation` input mezői (`invocationNum`, `initialNumSteps`, közös mezők: `conversationId`, `workspacePaths`, `transcriptPath`, `artifactDirectoryPath`, `modelName`) **nem tartalmazzák magát a felhasználói prompt szövegét** — ezt egy független, gyakorlati megfigyelés is megerősíti:

> "I start seeing the `PreInvocation` events. It tells me that the model is being called but apart from that, **there's not much information to act upon there**" — https://medium.com/google-cloud/where-does-antigravity-look-for-hooks-c9e9f57f167f

Tehát a szigorú értelemben vett "megkapja a felhasználó üzenetének szövegét" kérdésre a válasz **NEM** (a `PreInvocation` nem küldi a promptot).

**Visszaadhat szöveget** — `injectSteps` tömbben, `ephemeralMessage` (tranziens rendszerüzenet), `userMessage` vagy `toolCall` formájában:

> "`injectSteps` | array of objects | Optional. List of steps to inject into the conversation trajectory before the model is called." / "`ephemeralMessage` (string): A transient system message." — https://antigravity.google/docs/hooks/

**Kimeneti korlát: NINCS FORRÁS.**

**HTTP-végpont közvetlenül NEM hívható natívan** — csak `"command"`:

> "`type` | string | Optional. Currently only `\"command\"` is supported. Defaults to `\"command\"`." — https://antigravity.google/docs/hooks/

**Időkorlát: 30 másodperc az alapértelmezett**:

> "`timeout` | integer | Optional. Timeout in seconds. Defaults to `30`." — https://antigravity.google/docs/hooks/

**Hibakezelés**: a hivatalos doksin túl egy gyakorlati útmutató szerint a hook szkriptnek **mindig 0-s exit code-dal kell visszatérnie**, még elutasításkor is; nem-nulla exit code hiba, és ez "eldobhatja" vagy megszakíthatja a fordulót:

> "The script must always return an exit code of `0` to indicate a successful validation run, even when rejecting a command. **Non-zero exit codes are treated as hook execution failures and may trigger fallback actions or crash the active turn.**" — https://medium.com/google-cloud/a-developers-guide-to-agent-hooks-in-antigravity-cli-4c1440febd11 (T3, de gyakorlati megfigyelés, nincs ellenőrző második forrás — jelezve)

Egy 2026 augusztusi kiadási jegyzet (2.6.0) szerint korábban a timeout **nem volt garantált** — egy hook, amely modellt hív, a régi verzióban **végtelenségig várakozhatott**:

> "A hook that calls a model now stops with an explicit error at its configured timeout. Previously it could wait indefinitely" / "on anything older than 2.6.0, a hook without a timeout really can wait forever." — https://antigravitylab.net/en/articles/editor/antigravity-2-6-0-hook-stall-triage-self-timeout (T3, harmadik féltől; hivatalos Antigravity changelog-gal nem tudtuk keresztellenőrizni — NINCS második forrás)

### 1.6 GitHub Copilot — `UserPromptSubmit` / `userPromptSubmitted` (több, eltérő futásidejű változat)

A GitHub Copilot ökoszisztémában **három, eltérő képességű** felülettel találkoztunk ugyanarra a hook-eseményre:

**(a) VS Code Agent mód (`.vscode`/`.github/hooks/*.json`, config-fájl alapú, "Agent Host")**

> "| `UserPromptSubmit` | User submits a prompt | Audit user requests, inject system context |" — https://code.visualstudio.com/docs/agent-customization/hooks

> "In addition to the common fields, `UserPromptSubmit` hooks receive a `prompt` field with the text the user submitted." — https://code.visualstudio.com/docs/agents/reference/hooks-reference

> "The `UserPromptSubmit` hook uses the common output format only." — https://code.visualstudio.com/docs/agents/reference/hooks-reference

A VS Code motorjának (`DefaultIntentRequestHandler.ts`) forráskódja megerősíti, hogy az `additionalContext` ténylegesen becsatornázódik:

> "const userPromptSubmitResults = await this._chatHookService.executeHook('UserPromptSubmit', …); … const additionalContext = typedOutput.hookSpecificOutput?.additionalContext ?? typedOutput.additionalContext; if (additionalContext) { additionalContexts.push(additionalContext); }" — https://github.com/microsoft/vscode/blob/main/extensions/copilot/src/extension/prompt/node/defaultIntentRequestHandler.ts

**HTTP-végpont**: a VS Code Agent mód dokumentációjában csak `type: "command"` szerepel a példákban; explicit `http` típusú hook-mechanizmust a VS Code-specifikus oldalakon **nem találtunk** (ez eltér a hasonló nevű, de más futásidejű felülettől, lásd (c) pont).

**Időkorlát: 30 másodperc alapértelmezett**:

> "| `timeout` | number | Timeout in seconds (default: 30) |" — https://code.visualstudio.com/docs/agents/reference/hooks-reference

**Hibakezelés**:

> "| `0` | Success: parse stdout as JSON |\n| `2` | Blocking error: stop processing and show error to model |\n| Other | Non-blocking warning: show warning to user, continue processing |" — https://code.visualstudio.com/docs/agent-customization/hooks

**(b) Copilot CLI (önálló, `~/.copilot/hooks/*.json`, config-fájl alapú) — `userPromptSubmitted`**

> "`userPromptSubmitted` — The user submits a prompt." — https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/use-hooks

Itt egy **fontos, dokumentált korlátozás** van: a hivatalos referencia szerint a **config-fájlból** (parancs vagy HTTP) indított `userPromptSubmitted` hook kimenete **el van dobva**, beleértve a promptot módosító mezőt is — csak a programozott (SDK-alapú) hook kap érvényesítést:

> "`modifiedPrompt` is only honored by SDK programmatic hooks. **Command and HTTP config-file `userPromptSubmitted` hooks have their output dropped, including `modifiedPrompt`.** The lighter hooks-processing runtime used by hosted or steering Copilot cloud agent sessions also ignores it." — https://docs.github.com/en/enterprise-cloud@latest/copilot/reference/hooks-reference

Egy másik, ugyanerről az oldalról idézett táblázat-verzió az `additionalContext` támogatottságát is kifejezetten **"No"**-nak jelzi a `userPromptSubmitted`-nál (szemben pl. a `sessionStart`-tal, ahol igen):

> "| `sessionStart` | A new or resumed session begins. | Optional — can inject `additionalContext` into the session. | … |\n| `userPromptSubmitted` | The user submits a prompt. | No | Fires at most once, for the prompt supplied to the job. There is no follow-up user input. |" — https://github.com/github/docs/blob/c9bd77a9/content/copilot/reference/hooks-reference.md

Ez azt jelenti, hogy a config-fájl alapú Copilot CLI/felhő-ügynök `userPromptSubmitted` hookja gyakorlatilag **csak megfigyelésre/naplózásra** használható, nem kontextus-injektálásra — élesen eltér a Claude Code / Codex / Gemini CLI mintától.

**(c) Programozott (SDK-alapú, TypeScript) `onUserPromptSubmitted` hook** — ez viszont **igen** tud kontextust injektálni:

> "The `onUserPromptSubmitted` hook is called when a user submits a message. Use it to: … Add context before processing …" — https://github.com/github/copilot-sdk/blob/40887393/docs/hooks/user-prompt-submitted.md

> "| `additionalContext` | string | Extra context added to the conversation |" — https://github.com/github/copilot-sdk/blob/40887393/docs/hooks/user-prompt-submitted.md

Itt a hook maga natív TypeScript/Node kód (nem külön process), tehát tetszőleges HTTP-hívást és fejlécküldést tud végezni — de ez architekturálisan más, mint a config-fájl alapú "hook" mechanizmus, mert nincs külön hook-process-indítás, timeout-mechanizmus vagy exit-code-alapú hibakezelés; a hivatalos doksi kifejezetten figyelmeztet a sebességre:

> "Keep processing fast - This hook runs on every user message. Avoid slow operations." — https://github.com/github/copilot-sdk/blob/40887393/docs/hooks/user-prompt-submitted.md

**Kimeneti korlát**: a config-fájl alapú (command/HTTP) hookok kimenetére van egy általános, esemény-független felső korlát:

> "Hook output (stdout for command hooks, the response body for HTTP hooks) is bounded at 10 MiB per invocation—a larger response is truncated rather than exhausting memory." — https://docs.github.com/en/enterprise-cloud@latest/copilot/reference/hooks-reference

A ténylegesen a modellhez eljutó `additionalContext` (más eseményeknél, pl. `postToolUse`) egy szűkebb, dokumentált sapkát is kap:

> "When multiple hooks return `additionalContext`, the results are joined with a double newline and capped at 10 KB." — https://github.com/github/docs/blob/c9bd77a9/content/copilot/reference/hooks-reference.md

**HTTP-végpont közvetlenül hívható, fejléccel** — a felhő-ügynöknél (cloud agent) natív `type: "http"` hook létezik, ami a többi vizsgált kliens (Codex, Gemini CLI, Cursor, Antigravity) egyikénél sincs meg ilyen formában, csak a Claude Code-nál:

> "HTTP hooks send the input payload as a JSON `POST` to a URL." — https://docs.github.com/en/copilot/reference/hooks-reference

> "| `headers` | object | No | Request headers to include. |" — https://docs.github.com/en/copilot/reference/hooks-reference

> "By default, only `https://` URLs are allowed. Non-TLS `http://` requests are rejected, except for `http://localhost`, `http://127.*`, and `http://[::1]` when `COPILOT_HOOK_ALLOW_LOCALHOST=1` is set." / "**Cloud agent only.** Outbound network from the sandbox is restricted by the cloud agent firewall, so `url` must target an allow-listed host." — https://docs.github.com/en/copilot/reference/hooks-reference

**Időkorlát: 30 másodperc alapértelmezett** (megegyezik a VS Code-dal):

> "| `timeoutSec` | number | No | Timeout in seconds. Default: `30`. |" — https://docs.github.com/en/copilot/reference/hooks-reference

**Hibakezelés — explicit fail-open szabály timeoutra, minden eseménytípusra, beleértve a szabályzati (policy) hookokat is**:

> "Killed after `timeoutSec`. Error logged, execution continues. **Timeouts are fail-open for every event, including `preToolUse` and admin-deployed policy hooks**—a warning is surfaced and processing proceeds as if the hook had not run. […] A crashed or explicitly-denying hook still fails-closed; only timeouts are exempt." — https://docs.github.com/en/copilot/reference/hooks-reference

> "For most events, non-zero exits and timeouts are logged and skipped—agent execution continues." — https://docs.github.com/en/copilot/reference/hooks-reference

Ez az egyetlen kliens, amelynél hivatalos dokumentáció **explicit módon, elvi indoklással** különbözteti meg a "hiba" (fail-closed) és a "timeout" (fail-open) esetet.

---

## 2. Meglévő megoldások: mit adnak be kérdésenként, hogyan kerülik el a zajt

### 2.1 claude-mem (thedotmack/claude-mem)

A `SessionStart` mellett külön `UserPromptSubmit` hookot vezettek be a **relevancia-alapú** (nem recency-alapú) beadásra:

> "Adds per-prompt semantic search that injects the most **relevant** past observations into context, replacing the current recency-based approach." — https://github.com/thedotmack/claude-mem/pull/1568

Mechanika: a prompt szövegét ChromaDB-vel vektor-keresik, top-5 (konfigurálható) találatot adnak be `additionalContext`-ként, csak ha a prompt legalább 20 karakter (rövid/köszönő promptokat kihagyja):

> "On every `UserPromptSubmit`, query ChromaDB with the user's prompt text and inject the top-5 semantically similar observations as `additionalContext`." — https://github.com/thedotmack/claude-mem/pull/1568

> "validates `q` (≥20 chars) … formats up to `limit` items into compact markdown" — https://github.com/thedotmack/claude-mem/pull/1568 (CodeRabbit walkthrough)

| Beállítás | Alapérték | Leírás |
|---|---|---|
| `CLAUDE_MEM_SEMANTIC_INJECT` | (lásd lent) | be/kikapcsolja a kérdésenkénti injektálást |
| `CLAUDE_MEM_SEMANTIC_INJECT_LIMIT` | `5` | max. beadott találat |

> "| `CLAUDE_MEM_SEMANTIC_INJECT` | `true` | Enable/disable per-prompt injection |\n| `CLAUDE_MEM_SEMANTIC_INJECT_LIMIT` | `5` | Max observations injected per prompt |" — https://github.com/thedotmack/claude-mem/pull/1568

Tokenköltség mérve (saját, nem független mérés): recency-alapú (régi) ~1800 token/injektálás → szemantikus (új) ~800–1200 token/injektálás — https://github.com/thedotmack/claude-mem/pull/1568

**Zajkezelés — visszavonás**: a szemantikus injektálást a szerző néhány nappal a bevezetés után **alapból kikapcsolta**, mert zajt és késleltetést okozott:

> "The per-prompt Chroma vector search injection on UserPromptSubmit adds latency and context noise. Disable by default while we iterate on a more precise file-context approach." — https://github.com/lagosito/claude-mem/commit/0f9745535a4f1193fbe8e646ec7aa2fe3ba31662

**Egyéb (nem szemantikus) `UserPromptSubmit` hook**: a session-nyomkövetést indítja, nem blokkoló, 60 másodperces timeouttal:

> "| UserPromptSubmit | Before processing | No | 60s | stdout → context |" — https://docs.claude-mem.ai/hooks-architecture

### 2.2 mem0 Claude Code / Codex plugin

Hivatalos plugin, `UserPromptSubmit` hookkal, amely **prefetch**-eli a promptra releváns memóriákat, és emellett egy döntési heurisztikát ("rubric") is beszúr, ami arra tanítja az ügynököt, mikor keressen tovább maga:

> "`UserPromptSubmit` | Searches relevant memories before each message; skips short prompts" — https://docs.mem0.ai/integrations/claude-code

> "Fires on every user message. Prefetches memories relevant to the current prompt (so relevant context is guaranteed) and also injects a decision rubric telling the agent when to search further itself" — https://github.com/mem0ai/mem0/blob/main/integrations/mem0-plugin/scripts/on_user_prompt.sh

Konkrét paraméterek: top-5 találat (`top_k=5`), letiltható `MEM0_PREFETCH=false`-szal:

> "results = search_memories(api_key, user_id, project_id, query, top_k=5, rerank=should_rerank())" — https://github.com/mem0ai/mem0/blob/main/integrations/mem0-plugin/scripts/on_user_prompt.sh

**Zajkezelés**: 2026 áprilisában a fejlesztők **kivették** a "vak" (mindig lefutó) szemantikus keresést a kérdésenkénti hookból, mert feleslegesen fogyasztotta az API-hívásokat és zajos, alacsony-recall eredményeket adott:

> "The `on_user_prompt.sh` hook previously ran a blind semantic search against the user's raw prompt and injected the top-5 results into context on every turn. This wasted API calls on prompts where memory wouldn't help, and the raw-prompt-as-query approach produced low-recall results that crowded the context window with noise." — https://github.com/mem0ai/mem0/pull/4992

Az új verzió helyette egy döntési szabályt injektál (mikor keressen, mikor ne), és magára az LLM-re bízza a tényleges keresés eldöntését — ezzel a "kérdésenkénti automatikus beadás" részben visszavált "modell dönti el, keressen-e" mintára:

> "This PR restructures the hook to be a **prompt-injection point** rather than a search-execution point. […] The agent — which has full conversation context — decides whether and how to search." — https://github.com/mem0ai/mem0/pull/4992

Egy külön, még nyitott minőségi hiba: a beadott memóriák **rerank nélkül**, nyers vektor-hasonlóság szerint rendezve mennek be, ami miatt a legjobb találat néha kimarad a top-5-ből:

> "Every prompt's injected context is the **unranked** `top_k=5`. In testing, the single most relevant memory for a query landed at rank #1 only with `rerank:true` and was **absent from the top-5** without it — i.e. the best memory is silently dropped from the injected window." — https://github.com/mem0ai/mem0/issues/5684

**Időkorlát**: a `UserPromptSubmit` hook 15 másodperces timeout (más forrásban 30s, saját `curl` budget) — lásd a claude-supermemory hasonló táblázatát alább; mem0-nál konkrét globális szám a hook-configban nem került elő, de a rerank-javaslat "3s curl budget"-ről beszél a keresési hívásra:

> "it adds ~150–200ms (well within the hook's 3s curl budget)" — https://github.com/mem0ai/mem0/issues/5684

**Codex-specifikus**: a Codex nem tölti be automatikusan a plugin hookjait, egyszeri telepítő szkript kell hozzá, és a `UserPromptSubmit` esemény ott is bekötött:

> "Optional — enable lifecycle hooks. Codex doesn't auto-wire hooks from plugin manifests; it only reads `~/.codex/hooks.json`… | `UserPromptSubmit` | Injects relevant memories into the prompt |" — https://github.com/mem0ai/mem0/blob/main/integrations/mem0-plugin/README.md

### 2.3 supermemory (supermemoryai/claude-supermemory)

Itt a **kérdésenkénti** hook (`UserPromptSubmit`) explicit módon **nem** memória-keresésre, hanem session-azonosító naplózásra szolgál — a tényleges kontextus-injektálás **session-indításkor** (`SessionStart`) történik, nem kérdésenként:

> "| `UserPromptSubmit` | On user prompt submission | Record session ID |" — https://docsmith.aigne.io/discuss/docs/claude-supermemory/overview-a495d1

> "1. **Session Start** → `context-hook.js` retrieves user profile and relevant memories from Supermemory API" — https://docsmith.aigne.io/discuss/docs/claude-supermemory/overview-a495d1

A dokumentáció maga is jelzi, hogy a modell "okoskodva" (reasoned recall) dönt arról, keressen-e egyáltalán — ez tehát nem determinisztikus, minden kérdésnél lefutó beadás, hanem a modellnek adott döntési lehetőség:

> "Reasoned recall — Before each turn, Claude decides whether recalling memory would help the current message, and only searches when it is worth it." — https://supermemory.ai/docs/integrations/claude-code

**Időkorlát a hookokra (config-fájl, dokumentált)**:

> "| Hook | Default Timeout | Recommended Range |\n| --- | --- | --- |\n| SessionStart | 30s | 15-60s |\n| UserPromptSubmit | 15s | 5-30s |\n| PostToolUse | 15s | 5-30s |\n| Stop | 30s | 15-60s |" — https://docsmith.aigne.io/docs/claude-supermemory/advanced-a495d1

**Zajkezelés — konfigurálható max. találatszám**:

> "| `maxProfileItems` | Max memories in context (default: 5) |" — https://supermemory.ai/docs/integrations/claude-code

### 2.4 memdb-memory (anatolykoptev/memdb) — Claude Code plugin

Kifejezetten dokumentált küszöbértékkel és MMR-deduplikációval:

> "`memdb-inject` | `UserPromptSubmit` | Searches MemDB for the top 5 most relevant memories; injects them as `<user_memory_context>` in `additionalContext` before Claude sees the prompt | <500 ms (30 s timeout, fails silently) |" — https://github.com/anatolykoptev/memdb/blob/main/docs/integrations/claude-code-plugin.md

> "User prompt → extract query → POST /product/search (top 5, mmr, 0.85 threshold) → inject as additionalContext" — https://github.com/anatolykoptev/memdb/blob/main/docs/integrations/claude-code-plugin.md

**Zajkezelés — explicit relevancia-küszöb és rövid-prompt-szűrés**:

> "Short/casual prompts are skipped automatically (`hi`, `ok`, `yes`, etc. under ~20 chars). For substantive prompts it fetches the 5 most relevant memories using MMR deduplication and a 0.85 relativity threshold, then injects them as a `<user_memory_context>` XML block" — https://github.com/anatolykoptev/memdb/blob/main/docs/integrations/claude-code-plugin.md

**Hibatűrés — soha nem blokkolja a promptot**:

> "The hook never throws — any error is silently discarded so the prompt is never blocked." — https://github.com/anatolykoptev/memdb/blob/main/docs/integrations/claude-code-plugin.md

### 2.5 Vectr (swapnanil/vectr) — a `arXiv:2607.20972` szerzőjének nyílt forráskódú rendszere

A cikk (lásd 3. szakasz) szerzője által épített, nyílt forráskódú eszköz, amely kifejezetten a "delivery, not storage" elvet valósítja meg, **három rétegben** particionálva a beadást aszerint, hogy mi a téttudás:

> "On editors with session hooks…, recall is injected automatically — directives and high-priority tasks at session start, semantic recall keyed to each prompt, and file-anchored gotchas before a read or edit — with observability via a `Hook injections` line in `vectr status`." — https://github.com/swapnanil/vectr

> "`kind` controls injection: `directive` fires unconditionally every session, `task` carries current-work state, `gotcha` resurfaces when its file is touched, `finding` (default) is relevance-ranked, `reference` is a pointer" — https://github.com/swapnanil/vectr

Ugyanez a szerző (blogbejegyzésben, T2) egy háromszintű ajánlást is közöl a beadási mechanizmus és a tartalom kockázatának összekapcsolására:

> "| Content type | Stakes | Delivery mechanism |\n| --- | --- | --- |\n| Never-deviate directive | A miss is unacceptable | Unconditional injection at every SessionStart. No similarity threshold |\n| File-scoped gotcha | Only matters when a specific file is in play | Trigger on file touch via PreToolUse |\n| Episodic finding | Useful if relevant to this turn, harmless to skip | Ranked semantic recall per prompt via UserPromptSubmit — use the user's own prompt as the query, inject the top matches |" — https://swapnanilsaha.com/blog/mcp-tool-adoption-agents/

---

## 3. Mérés: az automatikus beadás hatása

### 3.1 arXiv:2607.20972 (Delivery, Not Storage) — a `sq_kozos.txt`/SQ-lánc által megadott kiindulópont

A cikk kontrollált kísérletben méri a determinisztikus (hook-alapú) beadás és az önkéntes (tool-hívásos) memóriahasználat közti különbséget:

> "voluntary memory use is ∼zero even when the store is pre-seeded with task-relevant knowledge (0 memory operations in 114 turns), that deterministic injection delivered in every injection-equipped seeded run (n = 3) with zero false-alarm fires across audit-logged trigger evaluations" — https://arxiv.org/pdf/2607.20972

A native hook csatornán (Claude Code `SessionStart`/`UserPromptSubmit`/`PreToolUse`/`PreCompact`) mért hamis-riasztási (irreleváns beadás) arány mindkét futásban **nulla**, konkrét számlálóval:

> "False-alarm injections: zero in both runs, across 40 and 35 audit-logged trigger evaluations respectively" — https://swapnanilsaha.com/blog/mcp-tool-adoption-agents/

> "the cue-anchored gotcha fired inside both runs on the agent's first touch of the anchored file (∼20 s and ∼7 min in), per the daemon audit log; subsequent touches were suppressed by the per-session fire ledger, and the ledger reset at each compaction boundary" — https://arxiv.org/pdf/2607.20972

Ismétlődő beadás elkerülésének mechanizmusa (per-session ledger + compaction-nál reset) explicit megnevezve:

> "a per-session fire ledger dedups repeats, and the ledger resets at compaction boundaries so anchored facts re-arm in the new window" — https://arxiv.org/pdf/2607.20972

**Korlát/óvatosság a saját eredmény értékelésénél**: a szerző maga jelzi, hogy a kísérlet kicsi és nem oksági, online-ügynöki telepítési tanulmány, tehát ez **T1 forrás, de a cikk saját maga hangsúlyozza a kis mintaszámot** (n=3 seeded run, n=1 hosszú-távú próba a 11 remember/9 recall hívással):

> "The evidence is intentionally scoped: the current evaluation is local, deterministic, and proxy-based rather than a causal online LLM-agent deployment study." [ez az RSCB-MC cikkből van átvéve saját-korlátozásként — lásd 3.3, a 2607.20972-nél a hasonló mondat:] "The evaluation is small but its signature is consistent" — https://arxiv.org/pdf/2607.20972

### 3.2 Mem0 (arXiv:2504.19413) — pontosság/késleltetés/token-költség számszerűsítve, memória-alapú beadás vs. teljes kontextus

Ez a cikk nem kifejezetten kódoló-ügynöki hookra fókuszál, hanem konverzációs memóriára általában, de közvetlenül méri a "beadott, szűrt memória" vs. "teljes kontextus becsomagolása" tradeoffot, ami releváns a kérdésre ("mekkora a beadás mérete/hossza és a kontextus terhelése"):

> "Mem0 attains a 91% lower p95 latency and saves more than 90% token cost [compared to full-context], thereby offering a compelling balance between advanced reasoning capabilities and practical deployment constraints." — https://arxiv.org/abs/2504.19413

Konkrét számok: teljes kontextus ~26 000 token/lekérdezés, 17,1s p95 összlátencia, 72,9% pontosság (J-metrika); Mem0 (szűrt memória-beadás) ~7000 token/beszélgetés, 1,44s p95 összlátencia:

> "| Full-context | | 26031 | - | - | 9.870 | 17.117 | 72.90 ± 0.19% |" — https://arxiv.org/html/2504.19413v1

> "Mem0 encodes complete dialogue turns in a natural language representation and therefore occupies only 7k tokens per conversation on an average." — https://arxiv.org/abs/2504.19413 (Highlights)

**A pontosság enyhén romlik a szűréssel** (a teljes kontextus ad egy kis előnyt), de a szerzők ezt tudatosan vállalt tradeoffnak mutatják be:

> "Although the full-context approach can provide a slight accuracy edge, the memory-based systems offer a more practical trade-off, maintaining near-competitive quality while imposing only a fraction of the token and latency cost." — https://arxiv.org/abs/2504.19413

A 2026 áprilisi új algoritmusnál a Mem0 saját, nem-független benchmarkja szerint a pontosság (LoCoMo) 71,4→92,5 pontra nőtt ugyanolyan token-mérettel (~7K):

> "| **LoCoMo** | 71.4 | **92.5** | 7.0K | 0.88s |" — https://github.com/mem0ai/mem0 (README)

Ez azonban **saját mérés**, a README explicit módon jelzi a nyílt forráskódú SDK és a menedzselt platform közti eltérést — óvatosan kezelendő, T2/vendor-forrás:

> "Scores reflect Mem0's managed platform, which includes proprietary optimizations not available in the open-source SDK; open-source users should expect directionally similar gains but not identical numbers." — https://github.com/mem0ai/mem0

### 3.3 Kifejezetten kódoló-ügynöki memória, rossz célzású (hamis pozitív) beadás mért kára — arXiv:2604.27283

Ez a cikk **közvetlenül** a kérdésre válaszol: "van-e mérés arra, hogy a rosszul célzott beadás mennyit ront" — kódoló-ügynöki hibajavítás kontextusában:

> "Consequently, unsafe memory injection can anchor the agent on an incorrect repair strategy, consume context budget, and amplify hallucinated fixes." — https://arxiv.org/html/2604.27283v1

> "Its reward design intentionally penalizes false-positive memory injection more strongly than missed reuse, making non-injection and abstention first-class safety actions." — https://arxiv.org/html/2604.27283v1

> "A false-positive memory injection is more harmful than a successful accepted reuse is beneficial. This mirrors the operational reality of debugging: a wrong fix can move the repository farther from repair, while a missed memory can still leave the agent free to reason from current evidence." — https://arxiv.org/html/2604.27283v1

Mért eredmény (a szerzők saját, korlátozott kísérletében): a kontroller 0,0%-os hamis-pozitív rátát tart, miközben 60,5%-os proxy-sikerrátát ér el; ~331 mikroszekundum p95 döntési késleltetéssel:

> "In a bounded 200-case hot-path validation, it reaches 60.5% proxy success with 0.0% false positives and a 331.466 μs p95 decision latency." — https://arxiv.org/html/2604.27283v1

**Fontos forráskritikai megjegyzés**: ez a cikk (arXiv:2604.27283) szokatlan formázású, feltűnően friss (2026-os) preprint, amelynek lektoráltságát vagy szélesebb elfogadottságát **nem tudtuk másik, független forrással megerősíteni** — a fenti számok tehát **egyetlen, nem-lektorált forrásból** származnak, és a szerzők maguk is hangsúlyozzák, hogy determinisztikus, offline, proxy-alapú kiértékelésről van szó, nem éles ügynök-telepítésről:

> "The evidence is intentionally scoped: the current evaluation is local, deterministic, and proxy-based rather than a causal online LLM-agent deployment study." — https://arxiv.org/html/2604.27283v1

### 3.4 Általános RAG-irodalom: irreleváns/megtévesztő passzus mért hatása (nem ügynök-specifikus, de releváns alap)

Ez nem közvetlenül memória-hook-mérés, de közvetlen, számszerű bizonyíték arra, hogy az irreleváns beadott szöveg **rontja** a válaszpontosságot — lektorált forrás (ACL 2025):

> "A well-known issue with Retrieval Augmented Generation (RAG) is that retrieved passages that are irrelevant to the query sometimes distract the answer-generating LLM, causing it to provide an incorrect response." — https://aclanthology.org/2025.acl-long.892/

Egy kapcsolódó, ugyanahhoz a kutatáshoz tartozó munka konkrét pontszám-eséseket közöl gyenge vs. erős "zavaró" (distracting) passzusra:

> "baseline accuracy reaches 82.6 and 80.6 for Llama-3.2-3B and Llama-3.1-8B, respectively. Second, adding a weak distractor (distracting effect smaller than 0.2) alongside the relevant passage causes modest performance degradation, with accuracy declining to 79.4 and 80.1. Third, incorporating a hard distractor (distracting effect greater than 0.8) produces substantially greater impact, with accuracy dropping more dramatically to 71.5 and 73.9" — https://ceur-ws.org/Vol-4026/paper7.pdf

Vagyis: **erős** (releváns-nek tűnő, de téves) zavaró tartalom 6–11 százalékpontos pontosságesést okozott, még akkor is, amikor a helyes válasz szintén jelen volt a kontextusban.

Kiegészítő, hosszú-kontextusra fókuszáló mérés (Chroma Research, T2/vállalati kutatóblog, de módszertanilag alapos, 18 modellt tesztel): az irreleváns kontextus mennyisége (nem csak a jelenléte) önmagában rontja a teljesítményt, és ez a hatás a kontextushossz növekedésével **erősödik**:

> "We observe that model performance varies significantly as input length changes, even on simple tasks." / "The observed performance degradation at longer input lengths is not due to the intrinsic difficulty of the needle-question pairing. By holding the needle-question pair fixed and varying only the amount of irrelevant content, we isolate input size as the primary factor in performance decline." — https://www.trychroma.com/research/context-rot

---

## 4. Kockázatok és korlátok

### 4.1 Beadott tartalom hossza és kontextus-terhelés

Minden vizsgált klienshez tartozik valamilyen kimeneti korlát vagy vágási mechanizmus, de a konkrét szám és a viselkedés (levágás vs. fájlba mentés + rövid előnézet) eltér:

- Claude Code: 10 000 karakter dokumentált plafon, de nyílt hibajegyek szerint túllépéskor a gyakorlatban csak ~2000 karakter jut el a modellhez (SQ03-ban idézve, itt csak megismételve a `UserPromptSubmit`-ra vonatkozó relevanciája miatt).
- Codex: ~2500 token (`additionalContextLimit`, konfigurálható, `0` = korlátlan) — https://developers.openai.com/codex/hooks
- GitHub Copilot: a nyers hook-kimenet 10 MiB-nál vágódik, a ténylegesen a modellhez jutó, összefésült `additionalContext` pedig 10 KB-nál — https://docs.github.com/en/enterprise-cloud@latest/copilot/reference/hooks-reference
- Gemini CLI, Cursor, Antigravity: **NINCS FORRÁS** dokumentált plafonra.

### 4.2 Ismétlődő beadás ugyanabban a munkamenetben

Ez konkrét, dokumentált hibaforrás Claude Code-nál (felhalmozódás minden fordulónál, lásd 1.1), és minden vizsgált memória-plugin (claude-mem, mem0, memdb) épített be valamilyen deduplikáló/gate mechanizmust ellene:

- claude-mem: a szemantikus injektálást teljesen kikapcsolták alapból a zaj/duplikáció miatt (2.1).
- mem0: session-szintű "rubric flag" fájllal dedupolja a döntési szabály beadását, hogy csak egyszer menjen be munkamenetenként — https://github.com/mem0ai/mem0/blob/main/integrations/mem0-plugin/scripts/on_user_prompt.sh
- arXiv:2607.20972: "per-session fire ledger dedups repeats, and the ledger resets at compaction boundaries" (3.1).

### 4.3 Adatvédelem — a beadás csak az aktuális projektből jöhet-e

Konkrét, dokumentált **negatív** példa arra, hogy ez elromolhat: a mem0 Claude Code plugin szemantikus keresése projekt-szűrő nélkül futhatott (más projekt memóriái szivároghattak be), amíg egy külön javítás be nem került:

> "Our `handleSemanticContext` passes `project` to `SearchManager.search()`, but without #1540's fix, the Chroma vector query runs unscoped. […] the endpoint works but may return cross-project results until #1540 lands." — https://github.com/thedotmack/claude-mem/pull/1568

Ugyanez élesen jelentkezik a mem0 core repo-plugin kombinációjánál is: a hook-alapú és az MCP-alapú írás/olvasás **eltérő `user_id`-t** használhat, ami keresztezi az elkülönítést:

> "The plugin hooks (capture in `on_pre_compact.py`/`on_stop.sh`, injection in `on_user_prompt.sh`) resolve `user_id = MEM0_USER_ID ?: $USER`. The bundled MCP server (`mcp.mem0.ai`, configured with only the token) writes/reads under the **account identity**, a different `user_id`." — https://github.com/mem0ai/mem0/issues/5684

A supermemory és memdb dokumentáció explicit projekt/csapat-szintű konténer-taget (`repoContainerTag`, `personalContainerTag`) különít el, deklaráltan a keresztezés elkerülésére — https://supermemory.ai/docs/integrations/claude-code

### 4.4 Lassú hook a felhasználói élményben

A hibakezelési szabályok jelentős szórást mutatnak abban, hogy a **lassú** (timeoutoló) hook blokkolja-e a felhasználót:

| Kliens | Timeoutkor |
|---|---|
| Claude Code (`UserPromptSubmit`) | fail-open: a hook kimenete eldobódik, a prompt átmegy — https://code.claude.com/docs/en/hooks |
| Codex (`UserPromptSubmit`) | a hook `outcome: "timeout"`-tal hibázik; a teszt-eset szerint `should_stop: false` (a prompt átmegy) — https://github.com/openai/codex/blob/178c3d30/codex-rs/hooks/src/events/user_prompt_submit.rs |
| Gemini CLI (`BeforeAgent`) | a hívó a timeoutot hiba-eredményként kapja vissza, nem `deny`-ként — a gyakorlati hatás dokumentáltan nem "System Block" — https://github.com/google-gemini/gemini-cli/blob/d2cd12a7/packages/core/src/hooks/hookRunner.ts |
| Cursor (`beforeSubmitPrompt`) | fail-open (a Cursor általános command-hook szabálya szerint) — https://cursor.com/docs/hooks.md |
| Antigravity (`PreInvocation`) | dokumentálatlan a hivatalos oldalon; 2.6.0 előtt akár **végtelen várakozás** is előfordulhatott — https://antigravitylab.net/en/articles/editor/antigravity-2-6-0-hook-stall-triage-self-timeout (T3) |
| GitHub Copilot (`userPromptSubmitted`/`UserPromptSubmit`) | explicit dokumentált fail-open minden eseményre, beleértve az admin által telepített policy-hookokat is — https://docs.github.com/en/copilot/reference/hooks-reference |

Gyakorlati (plugin-szintű) tervezési válasz erre: a mem0/memdb hookok rövid (3–30s) belső timeoutot állítanak be **saját maguknak** a hívott HTTP API-ra, és explicit "silent fail" (soha nem blokkol) politikát követnek — https://github.com/anatolykoptev/memdb/blob/main/docs/integrations/claude-code-plugin.md, https://github.com/mem0ai/mem0/issues/5684

---

## Ellentmondások

1. **Cursor: dokumentált "Supported: Yes" a `UserPromptSubmit`→`beforeSubmitPrompt` harmadik-fél-hook-leképezésnél, de a tényleges kimeneti séma nem tartalmaz kontextus-injektálást.** A `cursor.com/docs/reference/third-party-hooks` táblázat szerint a Claude Code `UserPromptSubmit` hookja `beforeSubmitPrompt`-ra képeződik le, "Supported: Yes" jelzéssel — ez azt sugallhatná, hogy a Claude Code-stílusú `additionalContext`-injektálás is átvihető. A hivatalos `cursor.com/docs/hooks.md` kimeneti sémája és két, hivatalos Cursor-válasszal megerősített fórumszál viszont egyértelműen kimondja, hogy a `beforeSubmitPrompt` **csak** `continue`/`user_message`-et támogat, `additionalContext`-et nem, és ez nyílt feature-kérésként van nyilvántartva. A "Supported: Yes" tehát csak a blokkolási képesség átvitelére vonatkozik, nem a kontextus-injektálásra — ezt a doksi maga nem teszi egyértelművé.

2. **GitHub Copilot: két, egymásnak ellentmondó hivatalos táblázat-verzió a `userPromptSubmitted` `additionalContext`-támogatottságáról.** Az egyik cache-elt doksi-verzió ("Optional—`modifiedPrompt` is honored only by SDK programmatic hooks") burkoltan azt sugallja, hogy legalább az SDK-s út működik; egy másik, szintén hivatalos (github/docs repo, más commit) táblázat flatly **"No"**-t ír a `userPromptSubmitted` sorába az `additionalContext`-oszlopban. A config-fájl alapú (parancs/HTTP) hookoknál mindkét verzió megegyezik abban, hogy a kimenet el van dobva — csak a programozott SDK-hook kap tényleges érvényesítést. Ezt a fájlt a "b) Copilot CLI" alszakaszban jeleztem, a két forrást is megadva.

3. **Antigravity `PreInvocation` hibakezelés**: a hivatalos `antigravity.google/docs/hooks/` oldal nem ír elő kötelező "mindig 0-s exit code" szabályt sem elutasításra, sem hibára; ez csak egy harmadik féltől (Medium, gyakorlati útmutató) származó megfigyelés, amit **nem sikerült** hivatalos forrásból megerősíteni. Hasonlóan, a 2.6.0-s "korábban végtelenségig várakozhatott" állítás is csak egyetlen, nem hivatalos (T3) forrásból származik — jelezve mindkét helyen.

---

## Amire NINCS forrás

- Gemini CLI `BeforeAgent` hookjának konkrét kimeneti (karakter/token) korlátja — sem a hivatalos reference, sem a writing-hooks útmutató nem közöl számot.
- Antigravity `PreInvocation`/`PreToolUse` hookjainak kimeneti (`injectSteps`/`ephemeralMessage`) mérethatára.
- Cursor `beforeSubmitPrompt` hookjának konkrét, globálisan dokumentált alapértelmezett timeout-száma (csak azt tudjuk, hogy más command-hookoknál `timeout` mezőként másodpercben megadható, de magára a `beforeSubmitPrompt`-ra nincs kimondott alapérték).
- Mem0 plugin `UserPromptSubmit` hookjának globális, config-szintű timeout-száma (csak a belső HTTP-hívás ~3s budgetjéről van közvetett utalás).
- Peer-reviewed (nem vállalati vagy egyetlen-szerzős preprint) mérés kifejezetten arra, hogy egy **kódoló-ügynöki** memória-rendszerben (nem általános RAG QA-ban) mekkora a hamis-pozitív beadás pontosságkárosító hatása számszerűsítve, több, egymástól független kutatócsoporttól — az egyetlen idézett, közvetlenül releváns cikk (arXiv:2604.27283) csak egyetlen, nem-lektorált forrás, amit két független forrással nem tudtunk megerősíteni.
- Az Antigravity felhasználói-üzenet szövegének elérhetősége bármelyik hookban — a `PreInvocation` input mezői között nincs `prompt`/`userMessage` mező dokumentálva, és nem találtunk olyan Antigravity-eseményt, ami kifejezetten a felhasználói prompt beérkezésekor, annak szövegével fut.

---

## Meglátogatott és felderített linkek

| Cím | URL | Tier | Eszköz | Megjegyzés |
|---|---|---|---|---|
| Claude Code Hooks reference | https://code.claude.com/docs/en/hooks | T1 | web_search+web_fetch | Hivatalos; UserPromptSubmit esemény, timeout, additionalContext |
| Claude Code Hooks reference (.md tükör) | https://code.claude.com/docs/en/hooks.md | T1 | web_fetch | Teljes szöveg lekérve |
| claude-code-spec docs/hooks.md (tükör) | https://github.com/gotalab/claude-code-spec/blob/4fc9fa37/docs/claude-code/hooks.md | T2 | web_search | Harmadik féltől tükrözött hivatalos doksi, UserPromptSubmit decision control |
| Claude Code hooks (yourdocs tükör) | https://claude.yourdocs.dev/docs/claude-code/hooks | T2 | web_search | Tükör, stdout/UserPromptSubmit speciális eset |
| additionalContext silently dropped issue | https://github.com/anthropics/claude-code/issues/52876 | T1 | web_search | Hivatalos repo hibajegy |
| additionalContext accumulates bug | https://github.com/anthropics/claude-code/issues/40216 | T1 | web_search | Hivatalos repo hibajegy |
| UserPromptSubmit "handled" decision feature req. | https://github.com/anthropics/claude-code/issues/72327 | T1 | web_search | Reverse-engineelt renderelési részletek |
| Codex Hooks (developers.openai.com) | https://developers.openai.com/codex/hooks | T1 | web_search+web_fetch | Hivatalos; UserPromptSubmit, additionalContextLimit, timeout |
| Codex user_prompt_submit.rs forráskód | https://github.com/openai/codex/blob/178c3d30/codex-rs/hooks/src/events/user_prompt_submit.rs | T1 | web_search | Hivatalos forráskód, input séma, hibakezelés tesztek |
| Codex PR #14626 (UserPromptSubmit bevezetése) | https://github.com/openai/codex/pull/14626 | T1 | web_search | Hivatalos repo PR, minta hook |
| Codex PR #11067 (hook rendszer) | https://github.com/openai/codex/pull/11067 | T1 | web_search | Hivatalos repo PR |
| Codex issue #15266 (SessionStart/UserPromptSubmit ütközés) | https://github.com/openai/codex/issues/15266 | T1 | web_search | Hivatalos repo hibajegy |
| Codex issue #35382 (timeout kulcs doksi-hiba) | https://github.com/openai/codex/issues/35382 | T1 | web_search | Hivatalos repo hibajegy, serde forráskód-idézet |
| codex-rs command_runner.rs | https://github.com/openai/codex/blob/main/codex-rs/hooks/src/engine/command_runner.rs | T1 | web_search | Hivatalos forráskód, timeout kezelés |
| Codex CLI — Symposium (nem hivatalos összefoglaló) | https://symposium.dev/design/agent-details/codex-cli.html | T3 | web_search | Kiegészítő, timeout alapérték megerősítés |
| Gemini CLI Hooks reference (geminicli.com) | https://geminicli.com/docs/hooks/reference/ | T1 | web_search+web_fetch | Hivatalos (tükrözött) doksi; BeforeAgent |
| gemini-cli docs/hooks/reference.md (GitHub) | https://github.com/google-gemini/gemini-cli/blob/d2cd12a7/docs/hooks/reference.md | T1 | web_search | Hivatalos forrás-repo |
| gemini-cli docs/hooks/index.md | https://github.com/google-gemini/gemini-cli/blob/d2cd12a7/docs/hooks/index.md | T1 | web_search | Hivatalos esemény-táblázat |
| gemini-cli docs/hooks/writing-hooks.md | https://github.com/google-gemini/gemini-cli/blob/main/docs/hooks/writing-hooks.md | T1 | web_search | Hivatalos, exit-code stratégiák |
| Gemini CLI Hooks Best Practices | https://geminicli.com/docs/hooks/best-practices/ | T1 | web_search | Hivatalos, timeout hibaelhárítás |
| gemini-cli hookRunner.ts forráskód | https://github.com/google-gemini/gemini-cli/blob/d2cd12a7/packages/core/src/hooks/hookRunner.ts | T1 | web_search | Hivatalos forráskód, DEFAULT_HOOK_TIMEOUT=60000 |
| Cursor Hooks (cursor.com/docs/hooks) | https://cursor.com/docs/hooks | T1 | web_search | Hivatalos; beforeSubmitPrompt |
| Cursor Hooks (.md tükör) | https://cursor.com/docs/hooks.md | T1 | web_fetch | Teljes szöveg lekérve, command/prompt típusok, exit code fail-open |
| Cursor cookbook hooks/README.md | https://github.com/cursor/cookbook/blob/main/hooks/README.md | T1 | web_search | Hivatalos Cursor repo, beforeSubmitPrompt korlát |
| beforesubmitprompt marketplace oldal | https://cursor.com/marketplace/hooks/beforesubmitprompt | T1 | web_search | Hivatalos |
| cursor-hooks npm README (jsdelivr) | https://cdn.jsdelivr.net/npm/cursor-hooks@1.1.6/README.md | T3 | web_search | Közösségi TS típusdefiníció, kiegészítő |
| Cursor Third Party Hooks | https://cursor.com/docs/reference/third-party-hooks | T1 | web_search | Hivatalos, Claude Code→Cursor hook-leképezés |
| Cursor fórum: additional_context feature req. #150707 | https://forum.cursor.com/t/hooks-allow-beforesubmitprompt-hook-to-inject-additional-context/150707/1 | T2 | web_search | Hivatalos fórum, nyitott hiány |
| Cursor fórum: additional_context feature req. #157231 | https://forum.cursor.com/t/add-additional-context-to-beforesubmitprompt-hook-output/157231 | T2 | web_search | Hivatalos fórum |
| Cursor fórum: updated_input silently stripped #158883 | https://forum.cursor.com/t/bug-beforesubmitprompt-hook-updated-input-is-silently-stripped-modified-prompt-never-reaches-the-model/158883 | T2 | web_search | Hivatalos Cursor-válasz a kimeneti séma korlátairól |
| Antigravity Hooks (antigravity.google/docs/hooks) | https://antigravity.google/docs/hooks/ | T1 | web_search | Hivatalos; PreInvocation |
| Antigravity Hooks (ide/hooks) | https://antigravity.google/docs/ide/hooks/ | T1 | web_search | Hivatalos, alternatív útvonal |
| MemPalace STDIN_SHAPE.md | https://github.com/MemPalace/mempalace/blob/main/hooks/antigravity/STDIN_SHAPE.md | T2 | web_search | Közösségi implementáció, PreInvocation gyakorlati használat |
| Antigravity archive.ph tükör | https://archive.ph/eHBs0 | T2 | web_search | Doksi-archívum, keresztellenőrzéshez |
| Antigravity SDK lifecycle | https://antigravity.google/docs/sdk/lifecycle/ | T1 | web_search | Hivatalos, más (SDK-szintű) hook-mechanizmus |
| moltbook PreInvocation post | https://moltbook.com/post/e7d50bb4-ad03-419e-bde5-ff1da057dd6d | T3 | web_search | Közösségi gyakorlati tapasztalat |
| Medium: Developer's Guide to Agent Hooks in Antigravity CLI | https://medium.com/google-cloud/a-developers-guide-to-agent-hooks-in-antigravity-cli-4c1440febd11 | T3 | web_search | Gyakorlati útmutató, exit-code=0 szabály (nem hivatalos doksiban) |
| Antigravity Lab: 2.6.0 hook stall triage | https://antigravitylab.net/en/articles/editor/antigravity-2-6-0-hook-stall-triage-self-timeout | T3 | web_search | Harmadik féltől, verzió-changelog értelmezés |
| Medium: Where does Antigravity look for hooks | https://medium.com/google-cloud/where-does-antigravity-look-for-hooks-c9e9f57f167f | T3 | web_search | Gyakorlati megfigyelés, PreInvocation input mezők |
| VS Code Hooks reference | https://code.visualstudio.com/docs/agents/reference/hooks-reference | T1 | web_search | Hivatalos; UserPromptSubmit input/output |
| VS Code Configure agent hooks | https://code.visualstudio.com/docs/agent-customization/hooks | T1 | web_search | Hivatalos; timeout, exit code táblázat |
| VS Code Introduction to hooks | https://code.visualstudio.com/learn/customizations/5-hooks | T1 | web_search | Hivatalos, kiegészítő |
| microsoft/vscode-docs hooks.md (GitHub) | https://github.com/microsoft/vscode-docs/blob/main/docs/agent-customization/hooks.md | T1 | web_search | Hivatalos forrás-repo |
| github/copilot-sdk user-prompt-submitted.md | https://github.com/github/copilot-sdk/blob/40887393/docs/hooks/user-prompt-submitted.md | T1 | web_search | Hivatalos SDK doksi, onUserPromptSubmitted |
| microsoft/vscode defaultIntentRequestHandler.ts | https://github.com/microsoft/vscode/blob/main/extensions/copilot/src/extension/prompt/node/defaultIntentRequestHandler.ts | T1 | web_search | Hivatalos forráskód, additionalContext becsatornázás |
| GitHub Copilot Hooks reference | https://docs.github.com/en/copilot/reference/hooks-reference | T1 | web_search | Hivatalos; HTTP hook típus, fail-open timeout |
| GitHub Copilot Hooks reference (Enterprise Cloud) | https://docs.github.com/en/enterprise-cloud@latest/copilot/reference/hooks-reference | T1 | web_search | Hivatalos, userPromptSubmitted additionalContext "No" |
| github/docs hooks-reference.md (main) | https://github.com/github/docs/blob/main/content/copilot/reference/hooks-reference.md | T1 | web_search | Hivatalos forrás-repo |
| github/docs hooks-reference.md (c9bd77a9) | https://github.com/github/docs/blob/c9bd77a9/content/copilot/reference/hooks-reference.md | T1 | web_search | Hivatalos, korábbi commit — ellentmondás-összevetéshez |
| Using hooks with GitHub Copilot CLI | https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/use-hooks | T1 | web_search | Hivatalos; userPromptSubmitted |
| GitHub Copilot Concepts: Hooks | https://docs.github.com/en/copilot/concepts/agents/hooks | T1 | web_search | Hivatalos |
| Copilot CLI hooks tutorial | https://docs.github.com/en/copilot/tutorials/copilot-cli-hooks | T1 | web_search | Hivatalos |
| Customize agent workflows with hooks (Enterprise Cloud) | https://docs.github.com/en/enterprise-cloud@latest/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/use-hooks | T1 | web_search | Hivatalos |
| UserPromptSubmittedHookOutput Java API | https://copilot-community-sdk.github.io/copilot-sdk-java/latest/apidocs/com/github/copilot/sdk/json/UserPromptSubmittedHookOutput.html | T2 | web_search | Közösségi SDK, séma-megerősítés |
| claude-mem PR #1568 (szemantikus injektálás) | https://github.com/thedotmack/claude-mem/pull/1568 | T1 | web_search | Hivatalos repo PR, top-5, 20 char küszöb |
| docs.claude-mem.ai hooks-architecture | https://docs.claude-mem.ai/hooks-architecture | T1 | web_search | Hivatalos doksi, timeout-táblázat |
| DeepWiki claude-mem UserPromptSubmit | https://deepwiki.com/thedotmack/claude-mem/3.1.2-userpromptsubmit-hook | T2 | web_search | Harmadik féltől generált kódelemzés |
| claude-mem semantic-inject default-off commit | https://github.com/lagosito/claude-mem/commit/0f9745535a4f1193fbe8e646ec7aa2fe3ba31662 | T1 | web_search | Hivatalos repo commit (fork), zajkezelési döntés |
| claude-mem CLAUDE.md | https://github.com/thedotmack/claude-mem/blob/7e2da10a8eaebe6e08ee1cda689c6d575639540c/CLAUDE.md | T1 | web_search | Hivatalos repo |
| mem0 Claude Code integráció doksi | https://docs.mem0.ai/integrations/claude-code | T1 | web_search | Hivatalos |
| mem0 on_user_prompt.sh forráskód | https://github.com/mem0ai/mem0/blob/main/integrations/mem0-plugin/scripts/on_user_prompt.sh | T1 | web_search | Hivatalos, top_k=5, rubric dedup |
| mem0-plugin README.md | https://github.com/mem0ai/mem0/blob/main/integrations/mem0-plugin/README.md | T1 | web_search | Hivatalos, Codex-specifikus telepítés |
| mem0 PR #4992 (rubric-alapú refactor) | https://github.com/mem0ai/mem0/pull/4992 | T1 | web_search | Hivatalos repo PR, zajcsökkentés indoklása |
| mem0 PR #4518 (plugin bevezetése) | https://github.com/mem0ai/mem0/pull/4518 | T1 | web_search | Hivatalos repo PR |
| mem0 issue #5684 (rerank hiánya) | https://github.com/mem0ai/mem0/issues/5684 | T1 | web_search | Hivatalos repo hibajegy, mért A/B/C összehasonlítás |
| supermemory Claude Code doksi | https://supermemory.ai/docs/integrations/claude-code | T1 | web_search | Hivatalos, maxProfileItems, reasoned recall |
| supermemoryai/claude-supermemory README | https://github.com/supermemoryai/claude-supermemory | T1 | web_search | Hivatalos repo |
| supermemory MCP doksi | https://supermemory.ai/docs/supermemory-mcp/mcp | T1 | web_search | Hivatalos, search_memory tool |
| Claude-Supermemory Overview (aigne tükör) | https://docsmith.aigne.io/discuss/docs/claude-supermemory/overview-a495d1 | T2 | web_search | Harmadik féltől generált doksi-tükör |
| Claude-Supermemory Advanced Features | https://docsmith.aigne.io/docs/claude-supermemory/advanced-a495d1 | T2 | web_search | Timeout-táblázat |
| memdb-memory Claude Code plugin doksi | https://github.com/anatolykoptev/memdb/blob/main/docs/integrations/claude-code-plugin.md | T1 | web_search | Hivatalos repo, 0.85 MMR küszöb, fail-silent |
| Code.claude.com/memory (auto memory) | https://code.claude.com/docs/en/memory | T1 | web_search | Hivatalos, kontextushoz kapcsolódó, kiegészítő |
| swapnanil/vectr README | https://github.com/swapnanil/vectr | T1 | web_search | Hivatalos repo, hook-mátrix táblázat |
| Delivery, Not Storage (arXiv:2607.20972, PDF) | https://arxiv.org/pdf/2607.20972 | T1 | web_search | Elsődleges kutatási cikk, idézve |
| Delivery, Not Storage (pubdb tükör) | https://pubdb.com/paper/2607.20972 | T2 | web_search | Absztrakt-tükör |
| Delivery, Not Storage (Lattice) | https://www.layerthelatestinalattice.com/papers/arxiv:2607.20972 | T2 | web_search | Összefoglaló |
| Delivery, Not Storage (Cool Papers) | https://papers.cool/arxiv/2607.20972 | T2 | web_search | Absztrakt-tükör |
| Swapnanil Saha blog: MCP tool adoption | https://swapnanilsaha.com/blog/mcp-tool-adoption-agents/ | T2 | web_search | Szerzői blogbejegyzés, kiegészítő számadatok az arXiv-cikkhez |
| Mem0 paper (arXiv:2504.19413, abstract) | https://arxiv.org/abs/2504.19413 | T1 | web_search | Elsődleges kutatási cikk |
| Mem0 paper (arXiv HTML) | https://arxiv.org/html/2504.19413v1 | T1 | web_search | Teljes szöveg, táblázatok |
| Mem0 paper (DOI) | https://doi.org/10.48550/arxiv.2504.19413 | T1 | web_search | DOI-tükör, azonos szöveg |
| mem0ai/mem0 README (benchmark) | https://github.com/mem0ai/mem0?tab=readme-ov-file | T2 | web_search | Vendor-saját benchmark, 2026 áprilisi új algoritmus |
| lhl/agentic-memory Mem0 jegyzet | https://github.com/lhl/agentic-memory/blob/HEAD/references/chhikara-mem0.md | T2 | web_search | Harmadik féltől készült cikk-összefoglaló |
| Mem0 paper (Hugging Face) | https://huggingface.co/papers/2504.19413 | T2 | web_search | Tükör |
| RSCB-MC kódoló-ügynöki memória cikk (arXiv:2604.27283) | https://arxiv.org/html/2604.27283v1 | T2 | web_search | Preprint, nem tudtuk függetlenül megerősíteni — jelezve a szövegben |
| The Distracting Effect (ACL 2025) | https://aclanthology.org/2025.acl-long.892/ | T1 | web_search | Lektorált konferenciacikk |
| Quantifying Distraction of Irrelevant Passages (CEUR-WS) | https://ceur-ws.org/Vol-4026/paper7.pdf | T1 | web_search | Lektorált workshop-cikk, konkrét pontosságesés-számok |
| Context Rot (Chroma Research) | https://www.trychroma.com/research/context-rot | T2 | web_search | Vállalati kutatóblog, 18 modell tesztelve, módszertanilag részletes |

---

# ELL04 — Mit adnak be a memória-eszközök a munkamenet elején: az állítások ellenőrzése

**Módszertani megjegyzés:** Egyetlen kutató-ügynökként, alügynökök indítása nélkül (degradált mód, a `deep-web-research` skill többügynökös pipeline-ja helyett szekvenciális feldolgozással) dolgoztam. Keresésre és oldalolvasásra kizárólag `mcp__Exa__web_search_exa` és `mcp__Exa__web_fetch_exa` eszközöket használtam; a beépített WebSearch/WebFetch-et nem hívtam. A `curl`-t csak a megengedett kivétellel, nyers forráskód-fájlok (GitHub `raw.githubusercontent.com`) szó szerinti, közvetlen ellenőrzésére használtam, amikor az Exa-fetch a fájl hosszúsága miatt levágta a releváns részt. Minden idézetet magam nyitottam meg és ellenőriztem — az sq05/sq06 korábbi idézeteit nem vettem át vakon. A mai dátum 2026-09-25; minden forrásnál jelöltem a verziót/dátumot, ahol elérhető volt.

---

## Verdikt-összefoglaló

| # | Állítás | Verdikt | Egy mondat |
|---|---|---|---|
| 1 | Claude Code auto memory: `MEMORY.md` első 200 sora / 25 KB-ja töltődik be; hibajegy szerint a limit feletti rész csendben elvész | **IGAZOLVA** | A jelenlegi hivatalos doksi szó szerint ezt írja, és a #57574 hibajegy (ma is elérhető, tartalma egyezik) igazolja a gyakorlati hatást. |
| 2 | claude-mem: alapból utolsó 10 munkamenet ~50 megfigyelését adja be SessionStart hookon; a szemantikus keresést visszajelzés alapján tették választhatóvá | **IGAZOLVA** | A hivatalos doksi ma is „last 10 sessions" / 50 observations-t mond, és a fő (nem fork) repó CHANGELOG-ja pontosan dátumozza és indokolja az opt-in váltást (v11.0.1, 2026-04-06). |
| 3 | A mem0 plugin determinisztikus bash-sablonból ad be szöveget | **IGAZOLVA** | A ma is élő `on_session_start.sh` forráskódban szó szerint megvan mindkét idézett mondat; a szöveg összeállítása `echo`/`cat` alapú, nem modellhívás. |
| 4 | basic-memory: nincs automatikus session-eleji beadás; OpenMemory: nincs, csak eszközleírásban van utasítás („called EVERYTIME") | **IGAZOLVA** | A basic-memory doksi szerint a promptok természetes nyelvi triggerre futnak, nem SessionStart-ra; az OpenMemory ma is élő forráskódjában szó szerint megvan a „called EVERYTIME" leírás, és nincs session-start hook a fájlban. |
| 5 | Letta: a memory blockok teljes egészében a rendszerpromptban vannak; ajánlás: <50 000 karakter / <20 blokk | **IGAZOLVA** | Két külön hivatalos Letta-doksi-oldal szó szerint „system prompt"-nak nevezi a blokkok helyét, és a számok pontosan egyeznek. |
| 6 | A Cursor Memories funkció megszűnt (2.1.17, 2025-11-21) | **IGAZOLVA** | A Cursor-staff fórumválasza ma is elérhető és szó szerint ezt mondja; a verziószámot és dátumot két, egymástól független harmadik fél (csomagkezelő-adatbázis, release-tracker) is megerősíti. |
| 7 | Serena: az MCP `initialize` válasz `instructions` mezője a memórianevek listáját adja, nem a tartalmukat | **IGAZOLVA** | A ma is élő forráskód (`mcp.py`, `agent.py`) megmutatja, hogy az `instructions` mezőbe kerülő szöveg névlistát (JSON-dict) ad, és explicit a `read_memory` eszközre utalja a modellt a tartalomért; ezt a hivatalos doksi is megerősíti. |
| 8 | Anthropic API automatikusan beszúrja a „VIEW YOUR MEMORY DIRECTORY" szöveget; Gemini CLI forráskódja „use save_memory when…" utasítást tartalmaz; 2026-02-i PR szerint a noszogatás modellfüggő | **RÉSZBEN — egyik alállítás MEGDŐLT a mai állapotra** | Az Anthropic-rész és a PR-idézet szó szerint stimmel; de a Gemini CLI **mai** forráskódja (mind a Gemini 3, mind a „legacy" Gemini 2.5 ágon) kifejezetten azt írja: „There is no `save_memory` tool" — a `save_memory`-alapú memóriaeszközt 2026 folyamán egy közvetlen fájlszerkesztős mechanizmus váltotta fel, így az idézett utasítás ma már nem létezik a kódban, és a PR-ben leírt „modellfüggő" megkülönböztetés is túlhaladottá vált. |

---

## Állításonként

### 1. Claude Code auto memory — `MEMORY.md` 200 sor / 25 KB, csendes adatvesztés

**Élő hivatalos doksi (közvetlenül lekérve, 2026-09-25-i állapot):**

> "The first 200 lines of `MEMORY.md`, or the first 25KB, whichever comes first, are loaded at the start of every conversation. Content beyond that threshold is not loaded at session start. Claude keeps `MEMORY.md` concise by moving detailed notes into separate topic files."

> "After Claude writes to `MEMORY.md`, Claude Code measures the file against the 200-line and 25KB read limits. If the file is near a limit, Claude Code reminds Claude to shorten it… If the file is over a limit, the write still succeeds, but Claude Code returns an error telling Claude to rewrite the index, because everything past the limit is dropped on the next load."

— https://code.claude.com/docs/en/memory (T1, hivatalos, 2026-09-25-i lekérés)

Ez szó szerint egyezik az sq05-ben idézett mondatokkal — magam is megtaláltam ugyanezt a szöveget a jelenlegi oldalon, tehát nem csak korábbi kutató másolta pontosan, a forrás ma is ezt mondja.

**A hibajegy (#57574) — közvetlenül lekérve, teljes tartalommal, ma is elérhető (állapot: closed, duplicate):**

> "Auto-memory `MEMORY.md` is loaded at session start with what appears to be a ~25KB / 200-line cap. When `MEMORY.md` exceeds this cap, content beyond the cap is silently dropped with only a buried warning in the system prompt."

> "In my case, `MEMORY.md` reached 34.3KB. The harness did emit, in the system prompt at session start: `WARNING: MEMORY.md is 34.3KB (limit: 24.4KB) — index entries are too long. Only part of it was loaded.` …but only as a buried line that I noticed only after asking Claude to investigate why it was repeating mistakes."

> "I restructured `MEMORY.md` from a 35.5KB chronological list into a 3.5KB tiered index (90% reduction) […] The restructure recovered ~8,000 tokens of context budget at every session start."

— https://github.com/anthropics/claude-code/issues/57574 (T1, hivatalos repó, létrehozva 2026-05-09, lezárva mint duplikátum — **fontos árnyalat**: a jegyet a bot duplikátumként zárta le (#56786, #39811, #40210-re hivatkozva), ami azt jelenti, hogy a jelenség önmagában nem egyedi/elszigetelt eset volt, nem azt, hogy a probléma meg lett oldva vagy cáfolva).

**Verdikt indoklása:** Két, egymástól tartalmilag független, de mindkettő T1 (hivatalos doksi + hivatalos repó hibajegy) forrás egyezik, és mindkettőt magam nyitottam meg, nem az sq05 idézetét vettem át. Az állítás pontosan igazolt.

---

### 2. claude-mem — 10 munkamenet / 50 megfigyelés, opt-in szemantikus keresés

**Hivatalos doksi, közvetlenül lekérve:**

> "1. Start Claude Code - Context from last 10 sessions appears automatically […] 4. Next session - Previous work appears in context"

> "When you start a new Claude Code session, the SessionStart hook: 1. Queries the database for recent observations in your project (default: 50) 2. Retrieves recent session summaries for context…"

— https://docs.claude-mem.ai/usage/getting-started (T1, hivatalos, 2026-09-25-i lekérés)

> "| Observations | 50 | 1-200 | … | | Sessions | 10 | 1-50 | …"

— https://docs.claude-mem.ai/configuration (T1)

**A szemantikus keresés opt-in váltása — ezúttal a FŐ (nem fork) repó CHANGELOG-jából, közvetlenül a `raw.githubusercontent.com/thedotmack/claude-mem/main/CHANGELOG.md` fájlból (curl-lal, szó szerint ellenőrizve, mert az sq05 csak egy fork changelogját idézte T2-ként):**

> "## [11.0.1] - 2026-04-06
> **Patch release** — Changes `CLAUDE_MEM_SEMANTIC_INJECT` default from `true` to `false`.
> ### What changed
> - Per-prompt Chroma vector search on `UserPromptSubmit` is now **opt-in** rather than opt-out
> - Reduces latency and context noise for users who haven't explicitly enabled it
> - Users can re-enable via `CLAUDE_MEM_SEMANTIC_INJECT=true` in `~/.claude-mem/settings.json`
> ### Why
> The semantic inject fires on every prompt and often surfaces tangentially related observations. A more precise file-context approach (PreToolUse timeline gate) is in development as a replacement."

— https://github.com/thedotmack/claude-mem/blob/main/CHANGELOG.md (T1, **fő repó**, verzió és dátum pontosan azonosítva: v11.0.1, 2026-04-06)

**Pontosítás az sq05-höz képest:** az sq05 ezt csak egy forkolt repó (michaelbuckner/claude-mem) changelogjából, T2-ként idézte. Én a fő repóban is megtaláltam ugyanazt, szó szerint — tehát ez most T1, elsődleges forrásból igazolt, és a „miért" indoklás is pontosabb: a hivatalos ok nem kifejezetten „user feedback", hanem „the semantic inject … often surfaces tangentially related observations" — vagyis pontossági/zajprobléma, ami tartalmilag megfelel az sq05 „visszajelzés alapján" jellemzésének, de szó szerint nem ezt mondja.

**Verdikt indoklása:** Két különböző hivatalos oldal (doksi + fő repó changelog), mindkettő közvetlenül ellenőrizve. IGAZOLVA, kisebb pontosítással a „miért" tekintetében.

---

### 3. mem0 plugin — determinisztikus bash-sablon

**A ma is élő forráskód, közvetlenül lekérve a fő ágból (nem az sq05 által idézett commit-hash, hanem a jelenlegi `main`):**

> `echo "Search mem0 for recent decisions and task learnings before responding. Run 2 parallel searches: one for decision type, one for task_learning type."`

> `echo "New project with 0 memories. Invoke the mem0:onboard skill to import project files. Coding categories install automatically in the background."`

— https://github.com/mem0ai/mem0/blob/main/integrations/mem0-plugin/scripts/on_session_start.sh (T1, saját repó, forráskód, 2026-09-25-i lekérés)

Mindkét mondat betű szerint megvan a fájlban, feltételes `echo` ágakban (`SOURCE = "startup"` és `MEM0_COUNT = "0"` esetén), tehát a szöveg-összeállítás valóban determinisztikus bash-logika, nem LLM-hívás. A fájl emellett egy „compact recent activity timeline"-t is beilleszt egy Python-szkript (`session_timeline.py`) kimeneteként — ez adatbázis-lekérdezés, nem generatív modellhívás abban a pillanatban.

**Verdikt indoklása:** A forrást magam nyitottam meg a jelenlegi állapotában (nem a korábbi kutatás által idézett commitban), és a szöveg szó szerint, ma is jelen van. IGAZOLVA.

---

### 4. basic-memory és OpenMemory — nincs automatikus session-eleji injektálás

**basic-memory — hivatalos doksi, közvetlenül lekérve:**

> "### Continue Conversation […] `"Let's continue our conversation about [topic]"`"

> "### Recent Activity […] `"What have we been discussing recently?"` What happens: - Retrieves recently modified documents - Summarizes main topics and points - Offers to continue any discussions"

— https://docs.basicmemory.com/local/user-guide (T1, hivatalos, 2026-09-25-i lekérés)

A dokumentáció ezeket kifejezetten „Special Prompts"-ként, természetes nyelvi triggerre (a felhasználó vagy a modell mondata alapján) meghívandó mechanizmusként írja le — sehol nincs `SessionStart`-jellegű automatikus lefutás említve ezen az oldalon.

**OpenMemory — a ma is élő forráskód, közvetlenül lekérve (nem az sq05 által idézett régi commit, hanem a jelenlegi `main`):**

> `@mcp.tool(description="Search through stored memories. This method is called EVERYTIME the user asks anything.")`
> `async def search_memory(query: str) -> str:`

> `@mcp.tool(description="Add a new memory. This method is called everytime the user informs anything about themselves, their preferences, or anything that has any relevant information which can be useful in the future conversation. This can also be called when the user asks you to remember something. Set infer to False to store the memory verbatim without LLM fact extraction.")`

— https://github.com/mem0ai/mem0/blob/main/openmemory/api/app/mcp_server.py (T1, saját repó, forráskód, 2026-09-25-i lekérés)

A teljes fájlban (4 eszköz: `add_memories`, `search_memory`, `list_memories`, és a fájl további részében `delete_all_memories`) nincs semmilyen `SessionStart`-hook vagy hasonló automatikus belépési pont — a szerver kizárólag explicit MCP tool-hívásokra reagál.

**Második, független forrás (hivatalos termékbejelentés) ugyanerre:**

> "Built around the Model Context Protocol (MCP), the OpenMemory MCP Server exposes a standardized set of memory tools: `add_memories` … `search_memory` … `list_memories` … `delete_all_memories`"

— https://mem0.ai/blog/introducing-openmemory-mcp (T1, hivatalos blog, 2025-05-13)

Ez a bejelentés is kizárólag tool-hívás-alapú működést ír le, automatikus induló injektálás említése nélkül.

**Verdikt indoklása:** Mindkét fél-állítás (basic-memory és OpenMemory) két-két, egymástól független, elsődleges forrással igazolt, magam által frissen ellenőrizve. IGAZOLVA.

---

### 5. Letta — memory blockok a rendszerpromptban, <50k karakter / <20 blokk

**Méretkorlát, közvetlenül lekérve:**

> "| Memory Blocks | Editable (optional read-only) | Yes | `memory_rethink` `memory_replace` `memory_insert` & custom tools | Recommended <50k characters | Recommended <20 blocks per agent |"

— https://docs.letta.com/v1-sdk/memory/context-hierarchy (T1, hivatalos, 2026-09-25-i lekérés)

**A „rendszerpromptban van" állítás — ezúttal explicit, szó szerinti „system prompt" megfogalmazással, két külön hivatalos oldalról (ezt az sq05 csak közvetve, „prepended to the agent's prompt" szöveggel támasztotta alá, ami nem szó szerint „system prompt"; én找tam explicit megfogalmazást is):**

> "A stateful agent comprises of a system prompt, memory blocks, messages (in-context and out-of-context), and tools. […] memory blocks that are attached to an agent are in-context (**pinned to the system prompt**)."

> "An agent's context window contains **a system prompt (which includes attached memory blocks)**, and messages."

— https://docs.letta.com/guides/core-concepts/stateful-agents/index.md (T1, hivatalos, 2026-09-25-i lekérés)

> "Memory blocks are structured sections of the agent's context window that persist across all interactions. **They are always visible - no retrieval needed.**"

— https://docs.letta.com/v1-sdk/memory/memory-blocks/ (T1)

**Verdikt indoklása:** Két külön hivatalos Letta-doksioldal explicit a „system prompt" kifejezést használja a memory blockok helyére, és a számok (50k karakter, 20 blokk) pontosan egyeznek a korábbi kutatás idézetével — magam is megtaláltam ugyanezeket. IGAZOLVA, sőt pontosabb forrással alátámasztva, mint az sq05-ben.

---

### 6. Cursor Memories megszűnése — 2.1.17, 2025-11-21

**A Cursor-staff válasz, közvetlenül lekérve (a fórumbejegyzés ma is elérhető, 2025-11-24-i keltezéssel):**

> "Hey, thanks for the report. **The Memories feature was removed starting from version 2.1.17**, so it no longer appears in your current version (2.1.25)."

> "You can export your memories and move them into Rules: - Press `Cmd+Shift+P` and type "Export memories" - Your memories will be saved to an `.mdc` file"

— https://forum.cursor.com/t/memories-not-showing/143820/1 (T1, hivatalos Cursor-fórum, Cursor-staff — „deanrie" — válasza, 2025-11-24)

**A verziószám és dátum — két, egymástól teljesen független, nem a Cursor által üzemeltetett harmadik fél is megerősíti:**

> "Add to Builder | Cursor 2.1.17 | 86 | Friday, November 21, 2025 | Approved"

— https://community.chocolatey.org/packages/cursoride/2.1.17 (T2, független csomagkezelő-adatbázis, a csomag közzétételi dátuma)

> "Cursor v2.1 was released on November 21, 2025. […] This was the 4th Cursor release of 2025 tracked by Havoptic."

— https://www.havoptic.com/r/cursor-2.1 (T2, független release-tracker oldal)

**Verdikt indoklása:** Egy T1 elsődleges (a gyártó saját fóruma, staff-válasz) és két, egymástól és a gyártótól is független T2 forrás mind ugyanazt a verziószámot és dátumot adja. Ez erősebb megerősítés, mint amit az sq05 nyújtott (ott csak a fórumbejegyzés volt közvetlenül ellenőrizve). IGAZOLVA.

---

### 7. Serena — az `initialize` `instructions` mezője névlistát ad, nem tartalmat

**A ma is élő forráskód, közvetlenül lekérve (`mcp.py`, fő ág):**

> ```python
> instructions = self._get_initial_instructions()
> log.info("MCP server initial instructions:\n%s", instructions)
> mcp = FastMCP(
>     name="Serena",
>     version=serena_version_str,
>     lifespan=self.server_lifespan,
>     website_url="https://oraios.github.io/serena",
>     instructions=instructions,
> )
> ```

— https://github.com/oraios/serena/blob/main/src/serena/mcp.py (T1, saját repó, forráskód, 2026-09-25-i lekérés)

**A tartalom forrása (`agent.py`, fő ág, közvetlenül lekérve) igazolja, hogy csak névlista kerül be, nem a memóriák szövege — a modellt explicit a `read_memory` eszközre utasítja későbbi olvasásra:**

> ```python
> project_memories = proj.memory_manager.list_project_memories()
> if project_memories:
>     msg += (
>         f"\n{json.dumps(project_memories.to_dict())}\n"
>         + "Use the `read_memory` tool to read these memories later if they are relevant to the task."
>     )
> ```

— https://github.com/oraios/serena/blob/981f560f/src/serena/agent.py (T1, saját repó, forráskód)

**Hivatalos doksi, közvetlenül lekérve, ugyanerre:**

> "When the agent starts working on a project, **it receives the list of available memories**."

> "Agents receive **the full memory name list** up front as part of their initial instructions; any further references are described inside the memory content itself…"

— https://oraios.github.io/serena/02-usage/045_memories.html (T1, hivatalos, 2026-09-25-i lekérés)

**Verdikt indoklása:** Két önálló forráskód-fájl (mcp.py + agent.py) és a hivatalos doksi mind egybehangzóan igazolják: a betöltött szöveg névlista + „olvasd el később" utasítás, nem a memóriák tartalma. Magam nyitottam meg mindkét forráskódot a jelenlegi állapotukban. IGAZOLVA.

---

### 8. Anthropic API kikényszerítő szöveg / Gemini CLI „save_memory" utasítás / PR modellfüggőség

**8a) Anthropic API — a pontos hely és szöveg, közvetlenül lekérve, ÉS lokalizálva (hol áll):**

A szöveg a **„Prompting guidance" szakaszban** áll, a Memory tool dokumentáció oldalán:

> "## Prompting guidance
> When the memory tool is present in your request's `tools`, the API automatically adds this instruction to the system prompt. You don't need to send it yourself:
> ```
> IMPORTANT: ALWAYS VIEW YOUR MEMORY DIRECTORY BEFORE DOING ANYTHING ELSE.
> MEMORY PROTOCOL:
> 1. Use the `view` command of your `memory` tool to check for earlier progress.
> 2. ... (work on the task) ...
>    - As you make progress, record status / progress / thoughts etc in your memory.
> ASSUME INTERRUPTION: Your context window might be reset at any moment, so you risk losing any progress that is not recorded in your memory directory.
> ```"

— https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool (T1, hivatalos, „Prompting guidance" szakasz, 2026-09-25-i lekérés)

Ez szó szerint egyezik az sq05/sq06 idézetével — IGAZOLVA, és pontosítva a „hol áll" kérdésre: a Memory tool doksi „Prompting guidance" c. szakaszában, közvetlenül a tool-parancsok (`view`/`create`/`str_replace`/…) leírása után.

**8b) Gemini CLI forráskódja „use save_memory when…" utasítást tartalmaz — EZ A RÉSZÁLLÍTÁS A MAI FORRÁSKÓDRA NÉZVE MEGDŐLT.**

Az sq05/sq06 egy régebbi commitot (`caa04664`, `e79b149`) idézett, amiben tényleg volt `save_memory`-utasítás. Én a **jelenlegi (`main`, 2026-09-25-i) forráskódot** töltöttem le közvetlenül (`curl`-lal, mert az Exa-fetch a fájl hossza miatt levágta a releváns részt), és **mindkét** rendszerprompt-változatban (a Gemini 3-hoz használt `snippets.ts` ÉS a Gemini 2.5-höz használt `snippets.legacy.ts`) ugyanazt találtam:

> "- **Instruction and Memory Files:** You persist long-lived project context by editing markdown files directly with `edit` or `write_file`. **There is no `save_memory` tool.** The current contents of all loaded `GEMINI.md` files and the private project `MEMORY.md` index are already in your context — do not re-read them before editing."

— https://github.com/google-gemini/gemini-cli/blob/main/packages/core/src/prompts/snippets.ts, sor 843–869, funkció: `toolUsageRememberingFacts()` (T1, saját repó, forráskód, közvetlenül letöltve `curl`-lal, 2026-09-25)

> (ugyanez a mondat, szó szerint, a legacy fájlban is:) "There is no `save_memory` tool."

— https://github.com/google-gemini/gemini-cli/blob/main/packages/core/src/prompts/snippets.legacy.ts (T1, saját repó, forráskód, közvetlenül letöltve)

Ezt megerősíti a hivatalos eszköz-dokumentáció is, amely a `save_memory` toolt már nem is említi, hanem közvetlen fájlszerkesztést ír le:

> "Gemini CLI persists durable facts, user preferences, and project details **by editing Markdown memory files directly**. […] **Storage:** Edits Markdown files with `write_file` or `replace`."

— https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/memory.md (T1, hivatalos doksi, fő ág)

Fontos: a `save_memory` tool **korábban valóban létezett** és a routing-szabályok szövege (amit az sq06 idézett — „Routing rules — pick exactly one tier per fact…", „Never duplicate or mirror the same fact across tiers…") **szó szerint ma is megvan** a forráskódban, csak már nem egy `save_memory` tool-hívás, hanem a közvetlen `edit`/`write_file` fájlszerkesztés instrukciójaként. A GitHub-on követhető a teljes evolúció: #15678 (2025-12-29, panasz, hogy a modell nem menti proaktívan) → PR #18091 (2026-02, biztonsági javítások + instrukció-finomítás, ekkor még létezik a `save_memory` tool) → PR #18559 (2026-02-08, a `save_memory`-utasítás eltávolítása a Gemini 3 promptból) → PR #22726 (később, kísérleti „memory manager" subagent, ami teljesen leváltja a `save_memory` toolt) → a mai állapot, ahol mindkét promptváltozat explicit kimondja: nincs `save_memory` tool.

**8c) A 2026-02-i PR és a „modellfüggő noszogatás" állítás — IGAZOLVA a saját idejére, de közben túlhaladottá vált.**

A PR ma is elérhető és szó szerint ezt mondja:

> "This PR removes the explicit memory tool instructions from the Gemini 3 series system prompt. These instructions were previously necessary for earlier models to correctly utilize the memory tool, but Gemini 3 models exhibit high reliability in using the tool without explicit guidance."

> "Verify that all tests pass (**Gemini 2.5 still uses the legacy prompt which contains the instructions, while Gemini 3 uses the updated prompt**)."

— https://github.com/google-gemini/gemini-cli/pull/18559 (T1, gyártói repó, PR, merged: 2026-02-08T02:04:33Z, szerző: NTaylorMullen/gemini-cli-maintainers)

Ez az állítás a saját idejére (2026-02-08) pontosan igazolt: akkor tényleg csak a Gemini 3 ágból tűnt el az utasítás, a legacy (2.5) ág megtartotta. **Azóta viszont (a mai forráskód alapján, ld. 8b) mindkét ág elhagyta a `save_memory`-alapú instrukciót** — nem azért, mert a modellek megbízhatóbbak lettek, hanem mert az egész mechanizmus megváltozott (nincs többé `save_memory` tool, helyette közvetlen fájlszerkesztés). Vagyis a „modellfüggő noszogatás" jelenség valós volt és dokumentált, de **ez a konkrét megkülönböztetés mára okafogyottá vált** egy nagyobb architektúraváltás miatt.

**Verdikt indoklása (8. állítás összesítve):** RÉSZBEN. Az Anthropic-rész (8a) és a PR-idézet (8c) szó szerint és a mai napig pontosan igazolt. A Gemini CLI forráskód „save_memory"-idézete (8b) a mai forráskódra nézve MEGDŐLT — ez volt a kutatás legfontosabb, konkrét dátumhoz/commithoz köthető cáfolata.

---

## Amit ez a döntésre jelent

1. A négy, tényleg **determinisztikus, mérhető méretkorlátos** minta (Claude Code MEMORY.md 200 sor/25 KB, claude-mem 10 munkamenet/50 megfigyelés, Letta <50k karakter/<20 blokk, Windsurf global_rules.md 6000 karakter) mindegyike ma is pontosan igazolható elsődleges forrásból — ezek megbízható tervezési analógiák az easter-memory-system induló-injektálásához.
2. A „csendes adatvesztés méretkorlát felett" jelenség (Claude Code #57574) nem elszigetelt eset: a hibajegyet a rendszer több másik, hasonló jegy duplikátumaként zárta le — vagyis ez ismétlődő, több felhasználónál jelentkező mintázat, nem egyedi panasz.
3. A gyártói viselkedés konzisztens abban, hogy **explicit, kikényszerített szöveggel** (Anthropic API rendszerprompt-toldás, korábbi Gemini CLI `save_memory`-instrukció, mem0 bash-echo sablonok) próbálják rávenni a modellt a memória-eszköz használatára — ez a minta önmagában érv az easter-memory-system induló-injektálásának explicit, nem csak eszközleírásra bízott megoldása mellett.
4. A Gemini CLI esete (8b) élő példa arra, hogy egy induló-injektálási/nudge-mechanizmus **hónapok alatt gyökeresen átalakulhat** (tool-hívásból közvetlen fájlszerkesztésbe) — az easter-memory-system tervezésénél érdemes számolni azzal, hogy a kliens-oldali (Claude Code, Codex, Gemini CLI) mechanizmusok gyorsan változnak, és bármilyen integráció rendszeres újraellenőrzést igényel.
5. Két, egymástól függetlenül kialakult minta (Serena `instructions` mező + „olvasd el később" utasítás; OpenMemory „called EVERYTIME" eszközleírás) azt mutatja, hogy **névlista + explicit „hívj keresést" instrukció** is életképes, doksi-szinten dokumentált alternatíva a teljes tartalom induló beadásához képest — ez releváns az easter-memory-system "hogyan injektáljunk" nyitott kérdéséhez.
6. A Letta-dokumentáció explicit „system prompt"-nak nevezi a memory blockok helyét — ez konkrét, elsődleges forrású terminológiai megerősítés arra, hogy legalább egy éles enterprise-memóriarendszer a teljes tartalmat szó szerint a rendszerpromptba fűzi, nem külön kontextus-rétegbe.

---

## Meglátogatott linkek

| Cím | URL | Tier | Eszköz |
|---|---|---|---|
| How Claude remembers your project (élő doksi) | https://code.claude.com/docs/en/memory | T1 | Exa fetch |
| Auto-memory MEMORY.md silently truncated (#57574) | https://github.com/anthropics/claude-code/issues/57574 | T1 | Exa fetch |
| Memory tool — Claude Platform Docs | https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool | T1 | Exa fetch |
| claude-mem — Getting Started | https://docs.claude-mem.ai/usage/getting-started | T1 | Exa fetch |
| claude-mem — Configuration | https://docs.claude-mem.ai/configuration | T1 | Exa fetch |
| claude-mem CHANGELOG (fő repó, raw) | https://raw.githubusercontent.com/thedotmack/claude-mem/main/CHANGELOG.md | T1 | curl (nyers fájl) |
| mem0 on_session_start.sh (fő ág, raw) | https://raw.githubusercontent.com/mem0ai/mem0/main/integrations/mem0-plugin/scripts/on_session_start.sh | T1 | Exa fetch |
| OpenMemory mcp_server.py (fő ág, raw) | https://raw.githubusercontent.com/mem0ai/mem0/main/openmemory/api/app/mcp_server.py | T1 | Exa fetch |
| Introducing OpenMemory MCP (hivatalos blog) | https://mem0.ai/blog/introducing-openmemory-mcp | T1 | Exa search |
| basic-memory User Guide | https://docs.basicmemory.com/local/user-guide | T1 | Exa fetch |
| Letta — Memory blocks (core memory) | https://docs.letta.com/v1-sdk/memory/memory-blocks/ | T1 | Exa fetch |
| Letta — Context hierarchy | https://docs.letta.com/v1-sdk/memory/context-hierarchy | T1 | Exa fetch |
| Letta — Stateful agents (core concepts) | https://docs.letta.com/guides/core-concepts/stateful-agents/index.md | T1 | Exa search |
| Cursor fórum: Memories not showing (staff-válasz) | https://forum.cursor.com/t/memories-not-showing/143820/1 | T1 | Exa fetch |
| Chocolatey: Cursor 2.1.17 csomag | https://community.chocolatey.org/packages/cursoride/2.1.17 | T2 | Exa search |
| Havoptic: Cursor v2.1 release | https://www.havoptic.com/r/cursor-2.1 | T2 | Exa search |
| Cursor changelog / page 14 | https://cursor.com/changelog/page/14 | T1 | Exa fetch |
| Serena — Memories & Onboarding doksi | https://oraios.github.io/serena/02-usage/045_memories.html | T1 | Exa fetch |
| Serena mcp.py (fő ág, raw) | https://raw.githubusercontent.com/oraios/serena/main/src/serena/mcp.py | T1 | curl (nyers fájl) |
| Serena agent.py (commit 981f560f) | https://github.com/oraios/serena/blob/981f560f/src/serena/agent.py | T1 | Exa search |
| Serena generated_prompt_factory.py | https://github.com/oraios/serena/blob/901bd215/src/serena/generated/generated_prompt_factory.py | T1 | Exa search |
| Gemini CLI snippets.ts (fő ág, raw) | https://raw.githubusercontent.com/google-gemini/gemini-cli/main/packages/core/src/prompts/snippets.ts | T1 | curl (nyers fájl) |
| Gemini CLI snippets.legacy.ts (fő ág, raw) | https://raw.githubusercontent.com/google-gemini/gemini-cli/main/packages/core/src/prompts/snippets.legacy.ts | T1 | Exa fetch |
| Gemini CLI docs/tools/memory.md | https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/memory.md | T1 | Exa search |
| Gemini CLI PR #18559 (memory instrukció eltávolítása) | https://github.com/google-gemini/gemini-cli/pull/18559 | T1 | Exa fetch |
| Gemini CLI issue #18556 (a PR alapja) | https://github.com/google-gemini/gemini-cli/issues/18556 | T1 | Exa fetch |
| Gemini CLI issue #15678 (save_memory instrukció-panasz) | https://github.com/google-gemini/gemini-cli/issues/15678 | T1 | Exa search |
| Gemini CLI PR #18091 (save_memory biztonsági javítás) | https://github.com/google-gemini/gemini-cli/pull/18091 | T1 | Exa search |
| Gemini CLI PR #22726 (memory manager subagent, save_memory leváltása) | https://github.com/google-gemini/gemini-cli/pull/22726 | T1 | Exa search |
| Gemini CLI docs/index.md (save_memory említés, régebbi állapot) | https://github.com/google-gemini/gemini-cli/blob/f0a039f7/docs/index.md | T1 | Exa search |

---

# ELL05 — Az eszközhasználati és kontextus-mérések ellenőrzése

*Módszertani megjegyzés: al-ügynököket nem indítottam (degradált mód, ahogy az `_ell_kozos.txt` engedélyezi), egyetlen szálon, szekvenciális Exa-kereséssel/-olvasással dolgoztam. Az Exa (`mcp__Exa__web_search_exa`, `mcp__Exa__web_fetch_exa`) elérhető volt, kizárólag ezt használtam; beépített WebSearch/WebFetch-et nem hívtam. Minden idézetet a saját magam által lehívott elsődleges forrásból (arXiv PDF/HTML, hivatalos doksi, GitHub issue, NeurIPS/ICLR oldal) ellenőriztem — nem vettem át az SQ06 idézeteit ellenőrzés nélkül.*

## Verdikt-összefoglaló

| # | Állítás | Verdikt | Egy mondat |
|---|---|---|---|
| 1 | Nincs közvetlen, kontrollált mérés arra, hogy egy rövid session-eleji szöveg mennyivel növeli a memória-eszköz önkéntes használatát | **RÉSZBEN** | A szűk, sablonos "hány bejegyzés van" szövegre valóban nincs ilyen mérés, de van egy célzott kereséssel megtalált, közvetlenül releváns kontrollált kísérlet (Saha, 2026, arXiv:2607.20972), amely explicit szöveges instrukció ("guidance") melletti önkéntes memóriahasználatot mér — és nullát talál —, amit az SQ06 nem talált meg. |
| 2 | Az alap eszközhívási hajlandóság modellcsaládonként 7% és 98% között szór, a promptolás ezt csak durván korrigálja | **RÉSZBEN** | A három hivatkozott tanulmány létezik és az SQ06-ban idézett mondatok szó szerint stimmelnek, de a "7%-tól 98%-ig" összegző szám egyik forrásban sem szerepel — az egyetlen tényleges, forrásolt tartomány 7%–83% (arXiv:2608.25198); a "98%" eredete nem azonosítható, minden jel szerint az SQ06 saját szintézishibája. |
| 3 | Léteznek a "Lost in the Middle", a "context rot" (Anthropic, Chroma, két arXiv) és egy 2026-os null-eredmény, és azt mondják, amit az SQ06 állít | **IGAZOLVA** | Mind az öt forrás (Liu et al. TACL 2024, Chroma 2025-07-14, arXiv:2510.05381, arXiv:2606.29718, Zenodo 2026-06-18) létezik, és az idézett mondatok szó szerint megtalálhatók bennük — a hosszhatás és a 150k tokenig tartó null-eredmény egyaránt valósak. |
| 4 | GSM-IC (ICML 2023): "legfeljebb 18%" konzisztensen megoldható — a szám és a hatókör egyezik | **IGAZOLVA, kontextussal** | A mondat szó szerint megtalálható a PMLR-cikkben, de a 18%-os szám kifejezetten a GSM-IC (GSM8K + egy irreleváns mondat) feladatra és a 2023-as Codex/GPT-3.5 modellekre vonatkozik, nem általános, mai modellekre extrapolálható állítás. |
| 5 | Egy Codex-hibajegy szerint elavult memória felülírta a friss AGENTS.md-utasítást | **IGAZOLVA** | A github.com/openai/codex/issues/39223 jegy létezik, nyitott (2026-08-18), és a szó szerint idézett szöveg pontosan megegyezik a jegy tartalmával — de ez egy felhasználói bejelentés, az OpenAI nem erősítette meg hivatalosan. |
| 6 | MINJA (NeurIPS 2025) és a ChatGPT-memória 2024-es esete (Rehberger) léteznek, és a beadott memóriatartalmon át érkező nem kívánt utasításokról szólnak | **IGAZOLVA** | A MINJA-cikk (NeurIPS 2025 poszter, San Diego, 2025-12-05; arXiv:2503.03704) és Rehberger 2024-05-22-i blogbejegyzése is létezik, a szó szerint idézett mondatok — beleértve a MINJA 1. ábra feliratát is — pontosan megtalálhatók bennük. |
| 7 | Az Anthropic "84%/39%" száma: honnan van, mit mér | **IGAZOLVA, kontextussal** | A szám az Anthropic 2025-09-29-i hivatalos blogbejegyzéséből (context-management) származik, önbevallott, nem publikált módszertanú belső eval; a 84% és a 39% két KÜLÖNBÖZŐ mérésből jön (a 84% kizárólag a context editing token-megtakarítása egy 100-fordulós web-keresési evalon, a 39% a memória+context editing kombináció teljesítményjavulása egy másik, meg nem nevezett agentikus-keresési evalon) — az SQ06-ban idézett kritikai elemzés (dreaming.press) létezik és pontosan idézi, de ez maga is AI (Claude-opus) által írt, emberi szerkesztő által ellenőrzött blogbejegyzés, nem független emberi szakértői/újságírói forrás. |

## Állításonként

### 1. Van-e kontrollált mérés a session-eleji szöveg → önkéntes eszközhasználat hatásra?

Célzottan újra kerestem erre ("controlled experiment measuring effect of session-start reminder text on voluntary LLM agent memory tool invocation rate"). A szűk keretezésre (egy sablonból generált, "N bejegyzés van" jellegű mondat izolált, A/B-szerű hatása) továbbra sem találtam közvetlen mérést — ebben egyetértek az SQ06-tal.

Viszont találtam egy, a kérdéshez ennél is közelebb álló, kontrollált kísérletet, amit az SQ06 kihagyott:

> „A controlled evaluation on a naturalistic coding task showing that voluntary memory use is ∼zero even when the store is pre-seeded with task-relevant knowledge (0 memory operations in 114 turns)... Our own controlled runs replicate this naturalistically and extend it to the strongest case: an agent whose store was pre-seeded with facts directly relevant to its task, with connected tools and explicit guidance, made zero memory calls in 114 turns (§5.2). Voluntary memory does not happen."

Forrás: Swapnanil Saha, „Delivery, Not Storage: Cue-Anchored Working Memory as a Harness Property for Coding Agents", arXiv:2607.20972 (2026 július), https://arxiv.org/abs/2607.20972 , https://arxiv.org/pdf/2607.20972 (T2 — arXiv preprint, egyetlen független szerző, nem lektorált, nincs második független megerősítés).

A kísérleti elrendezés kifejezetten tartalmaz egy "voluntary + guidance" kart (B és V ág: "store (cold) + tools + guidance voluntary" / "store seeded proxy injection voluntary (hooks stripped)"), vagyis pontosan azt méri kontrolláltan, hogy egy explicit szöveges instrukció ("guidance") önmagában mennyire váltja ki az önkéntes eszközhasználatot — és nullát talál. Ez nem ugyanaz a beavatkozás, mint az SQ06-ban feltételezett "N bejegyzés van a memóriában" sablonmondat, de módszertanilag pontosan az a fajta kontrollált, célzott kísérlet, aminek a hiányát az SQ06 kimondta. Mivel egyetlen, nem lektorált, független kutatói preprintről van szó, önmagában nem elég egy "IGAZOLVA/MEGDŐLT" döntéshez, de az SQ06 "amire nincs forrás" kijelentését pontosításra szorulóvá teszi: legalább egy, a kérdéshez közeli, publikált kontrollált mérés létezik, csak nem talált rá az előző kör.

*(Mellékesen: ugyanez a keresés több iparági/blog jellegű, kontrollálatlan vagy más kérdést mérő forrást hozott — pl. GitHub „agent-memory-lab" benchmark, arXiv:2607.09493 „Shared Selective Persistent Memory" — ezek memória-STRATÉGIÁKAT hasonlítanak össze (van/nincs memória, RAG vs. teljes history), nem a session-eleji szöveg hatását az önkéntes hívásra, ezért nem tekintem őket a kérdésre közvetlenül válaszoló forrásnak.)*

### 2. A "7%–98%" tartomány — létezik-e, egyeznek-e a számok?

Mindhárom hivatkozott tanulmányt közvetlenül elértem és az SQ06-ban szereplő idézeteket szó szerint ellenőriztem.

**WHEN2TOOL** (arXiv:2605.09252v2) — a Finding 1 és Finding 2 idézetek szó szerint stimmelnek:

> „Finding 1: Models default to tool overuse. Under the Default (⋆) setting in Prompt-only baselines, models make 2,100–4,400 total tool calls across the 2,250-task single-hop test set, more than one calls per task. Even on easy tasks, Qwen3-1.7B makes 864 tool calls out of 750 easy tasks..."

> „Finding 2: Prompt engineering reduces tool calls indiscriminately, and hard tasks pay a disproportionate price... On Qwen3-4B-Instruct, the cost is −17.3 on easy but reaches −42.4 on hard, meaning hard tasks lose 2.5× more accuracy per saved call."

Forrás: https://arxiv.org/pdf/2605.09252v2 , https://arxiv.org/abs/2605.09252 (T1, arXiv preprint, 2026). Ez a cikk NEM ad meg semmilyen egyszerű "7%–X%" call-rate tartományt — az ő mérőszámai tool-call darabszámok és accuracy-cost-per-saved-call, nem call rate %.

**Tunable Tool-Call Rates via Representation Steering** (arXiv:2608.25198) — az egyetlen forrás, amely tényleges %-os baseline call-rate tartományt ad:

> „baseline call rates span both tool-underuse and tool-overuse, from 0.07 on Qwen3-4B to 0.83 on the 30B MoE."

Forrás: https://arxiv.org/html/2608.25198v1 , https://arxiv.org/abs/2608.25198 (T1, arXiv, 2026-08-25). Ez **7%–83%**, nem 7%–98%.

**ToolFailBench** (arXiv:2607.04686) — a "89 percentage points" idézet stimmel:

> „the best reaches 86.33% Clean Tool-Use Rate... Llama-3.1-70B and Qwen2.5-72B differ by 89 percentage points on control-task accuracy."

Forrás: https://arxiv.org/abs/2607.04686 , https://ar5iv.labs.arxiv.org/html/2607.04686 (egyetlen szerző — Harsh Soni, UC Berkeley —, arXiv preprint, nem lektorált; az SQ06 T1-ként jelölte, ami inkonzisztens azzal, hogy más, hasonlóan nem lektorált arXiv-preprinteket [pl. a Zenodo null-eredményt] T2-ként kezelt ugyanabban a jelentésben — ez önmagában módszertani pontatlanság, nem tartalmi tévedés). A cikk fejlécében szereplő "Keywords: Machine Learning, ICML" félrevezető lehet: a cikknek nincs igazolt lektorált konferencia-megjelenése, ezt semmilyen elérhető metaadat (arXiv absztrakt-oldal) nem támasztja alá.

**A "z=−19.9, p<10⁻⁸⁰" statisztikát** a lehívott absztrakt- és bevezető-szövegben nem találtam meg szó szerint (feltehetően egy mélyebb, statisztikai szekcióban van) — ezt nem tudtam külön ellenőrizni, így erre nézve NEM ELDÖNTHETŐ.

**Következtetés:** a három forrás és az SQ06 bennük szereplő szó szerinti idézetei valósak és pontosak, de az SQ06 saját összegző mondata ("tág skálán mozog, 7%-tól 98%-ig") egyik forrásban sem szerepel ebben a formában. A ténylegesen forrásolható tartomány **7%–83%**. A 98% eredete nem azonosítható — feltehetően szintézis közben keletkezett pontatlanság.

### 3. Lost in the Middle, context rot, 2026-os null-eredmény

Mind az öt forrást közvetlenül elértem.

**Lost in the Middle** (Liu et al., TACL 2024, DOI 10.1162/tacl_a_00638): a cikk létezik, lektorált (Transactions of the ACL, MIT Press), absztraktja szó szerint tartalmazza:

> „we observe that performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts, even for explicitly long-context models."

Forrás: https://aclanthology.org/2024.tacl-1.9/ (T1, lektorált).

**Chroma "Context Rot"** (2025-07-14): létezik, és a mondat szó szerint egyezik:

> „We demonstrate that even under these minimal conditions, model performance degrades as input length increases, often in surprising and non-uniform ways."

Forrás: https://www.trychroma.com/research/context-rot (T2, iparági kutatóműhely, nem lektorált, de 18 modellen, kontrollált, széles körben idézett).

**„Context Length Alone Hurts LLM Performance Despite Perfect Retrieval"** (arXiv:2510.05381): létezik, az absztraktban szó szerint szerepel:

> „even when models can perfectly retrieve all relevant information, their performance still degrades substantially (13.9%–85%) as input length increases but remains well within the models' claimed lengths."

Forrás: https://arxiv.org/abs/2510.05381 , https://arxiv.org/html/2510.05381 (T1, arXiv). A 13,9%–85% szám pontosan egyezik az SQ06 idézetével.

**„Diagnosing and Mitigating Context Rot in Long-horizon Search"** (arXiv:2606.29718): létezik, a "premature termination" fogalom és a hossz-korreláció szó szerint szerepel:

> „under extensive context, models give up or provide uncertain incorrect answers long before exhausting the context window... the premature termination rate is positively correlated with context length."

Forrás: https://arxiv.org/abs/2606.29718 , https://arxiv.org/html/2606.29718 (T1, arXiv, négy vezető modellen, három benchmarken).

**2026-os null-eredmény** (Zenodo, Jagtap): létezik, és a számok pontosan egyeznek:

> „we observe no measurable length-driven degradation on our probes for the four models tested (gpt-5.5, gpt-5.4, gpt-5.4-mini, claude-sonnet-4-6) up to 150,000 tokens... Across the 12,570-trial registered grid, 7,330 present-needle trials had 48 failures (accuracy 0.9935)."

Forrás: https://doi.org/10.5281/zenodo.20753848 (T2, „Preprint - not peer reviewed", 2026-06-18, egyetlen szerző — Sahil Jagtap, George Mason University). Fontos: a szerző maga is jelzi, hogy tiszta, szintetikus needle-in-haystack feladatról van szó, és „we cannot determine its contribution in real multi-turn agentic workflows" — vagyis ez nem cáfolja az agentikus kontextusban mért romlást, csak azt mutatja, hogy legújabb modelleken, tiszta lexikai feladaton nem mindig jelentkezik.

Az Anthropic „Effective context engineering for AI agents" (2025-09-29) blogbejegyzését ebben a körben nem hívtam le újra közvetlenül (URL-je jól ismert, korábbi köreinkben már szerepelt) — erre nézve a verdikt a korábbi ellenőrzésre támaszkodik, önállóan nem verifikáltam újra.

**Összegzés:** mind az öt állítás IGAZOLVA — a források léteznek, és pontosan azt mondják, amit az SQ06 állít róluk.

### 4. GSM-IC "legfeljebb 18%"

A PMLR-en közzétett, lektorált ICML 2023-as cikk PDF-jét közvetlenül elértem, és a mondat szó szerint megtalálható benne:

> „In particular, among the original problems that can be solved by baseline prompts with greedy decoding, no more than 18% of them can be consistently solved for all types of irrelevant information, showing that the large language model is easily distracted and produces inconsistent predictions when adding a small amount of irrelevant information to the problem description."

Forrás: Shi et al., „Large Language Models Can Be Easily Distracted by Irrelevant Context", ICML 2023, https://proceedings.mlr.press/v202/shi23a.html , PDF: https://proceedings.mlr.press/v202/shi23a/shi23a.pdf (T1, lektorált).

**Fontos kontextus, amit az SQ06 nem emelt ki eléggé:** a 18%-os szám a GSM-IC adathalmazra (GSM8K-alapú, egyetlen irreleváns mondattal kiegészített általános iskolai matekfeladatok) és a cikkben használt, 2023-as modellekre — Codex (`code-davinci-002`) és GPT-3.5 (`text-davinci-003`) — vonatkozik. A cikk maga is írja: „We use Codex (code-davinci-002) and GPT-3.5 (text-davinci-003) in the GPT3 model family to evaluate state-of-the-art prompting techniques on GSM-IC." Ez nem mai frontier-modelleken mért, általános "18%" — a szám és a hatókör technikailag egyezik az SQ06 állításával, de annak általánosíthatósága mai modellekre nyitott kérdés, amire ez a cikk önmagában nem ad választ.

### 5. Codex-hibajegy: elavult memória felülírta a friss AGENTS.md-t

A jegyet közvetlenül elértem a GitHubon:

> „Codex Desktop loaded both the global `~/.codex/AGENTS.md` and the repository `AGENTS.md` into the task context, but the agent ignored a distinctive current global rule and instead followed stale validation-gate guidance recovered from persistent memory... The problem is instruction precedence/compliance: stale memory was treated as more authoritative than the current, explicitly loaded global `AGENTS.md`."

Forrás: „Codex Desktop loads global AGENTS.md but stale memory overrides its explicit rule", https://github.com/openai/codex/issues/39223 — állapot: **open**, létrehozva: 2026-08-18, szerző: „Lyrnic" (T2, elsőkézi, de nem hivatalosan megerősített felhasználói hibajelentés; az OpenAI a jegyben nem szólalt meg, csak egy másik felhasználó kommentált rajta).

Az idézet szó szerint egyezik. Fontos, hogy ez egy **nyitott, nem lezárt, nem az OpenAI által megerősített** jegy — tehát dokumentált *esetleírásként*, nem hivatalosan elismert *hibaként* kell kezelni.

### 6. MINJA és a Rehberger-féle ChatGPT-eset

**MINJA**: a NeurIPS 2025-ös poszter valóban létezik (San Diego, 2025. december 5., Exhibit Hall C,D,E #1412), és megtaláltam az arXiv-verziót is (arXiv:2503.03704), amelynek teljes szövegében — az 1. ábra feliratában — szó szerint szerepel az SQ06-ban idézett mondat:

> „When the victim user submits a victim query, the stored malicious records are retrieved as a demonstration, misleading the agent to generate bridging steps and target reasoning steps through in-context learning."

Forrás: arXiv:2503.03704, https://arxiv.org/pdf/2503.03704 ; NeurIPS 2025 poszter/absztrakt: https://proceedings.neurips.cc/paper_files/paper/2025/hash/42a97bbd9844d2bf68596730af80bcdf-Abstract-Conference.html , https://nips.cc/virtual/2025/loc/san-diego/poster/118152 (T1, lektorált, NeurIPS 2025).

**Rehberger / ChatGPT 2024**: a blogbejegyzés létezik, 2024-05-22-i keltezéssel, és a leírt támadási módok (Connected Apps / Google Drive, kép-feltöltés, böngészés) megegyeznek az SQ06-ban leírtakkal:

> „a Google Doc that is referenced in a conversation can indeed write memories... this works well, and persists into future conversation and chat sessions."

Forrás: Johann Rehberger, „ChatGPT: Hacking Memories with Prompt Injection", https://embracethered.com/blog/posts/2024/chatgpt-hacking-memories/ (T1, elsődleges kutatói közlés, 2024-05-22).

Mindkét forrás valós, és pontosan azt állítja, amit az előző kör (SQ06) nekik tulajdonít: a beadott/tárolt memóriatartalmon keresztül nem kívánt, a felhasználó által nem szándékolt utasítások/adatok kerülhetnek be az agent tartós memóriájába, kizárólag közvetett interakción (lekérdezésen, dokumentumon, böngészésen) keresztül.

### 7. Az Anthropic "84%/39%" szám

Az anthropic.com/news/context-management oldalt (2025-09-29) közvetlenül elértem. A pontos szöveg:

> „combining the memory tool with context editing improved performance by 39% over baseline. Context editing alone delivered a 29% improvement. In a 100-turn web search evaluation, context editing enabled agents to complete workflows that would otherwise fail due to context exhaustion—while reducing token consumption by 84%."

Forrás: https://www.anthropic.com/news/context-management (T1, hivatalos, 2025-09-29).

**Mit mér pontosan és hogyan kell értelmezni:**
- A **84%** a **context editing** (nem a memória-eszköz) token-megtakarítását méri egy **konkrét, 100-fordulós web-keresési evaluationön**, olyan alap-futáshoz képest, amely kontextus-kimerülés miatt elbukna.
- A **39%** a **memória-eszköz + context editing kombinációjának** teljesítményjavulását méri egy **másik, "internal evaluation set for agentic search"** nevű, nyilvánosan nem specifikált belső evalon.
- A két szám tehát két különböző metrika, két különböző (és nyilvánosan nem dokumentált) belső eval-készleten — nem ugyanannak a jelenségnek két oldala, csak ugyanabban a bekezdésben szerepelnek. Egyik szám mögött sincs publikált módszertan, statisztikai szignifikancia-teszt vagy külső reprodukció — önbevallott gyártói szám.

Az SQ06 „Ellentmondások" szakaszában idézett kritikai elemzést is közvetlenül elértem és a rá hivatkozó idézetek pontosak:

> „Both figures are real. Neither says the model got smarter — they measure escaping a wall your agent may never hit"; „The 39% is a completion-rate gain on tasks long enough to exhaust context — on short tasks the delta collapses toward zero."

Forrás: „The 84% and the 39%: What Anthropic's Context-Management Numbers Actually Measure", https://dreaming.press/posts/anthropic-context-editing-84-percent-39-percent-numbers-examined.html (2026-07-27).

**Fontos, az SQ06-ból hiányzó részlet:** ennek a "független kritikai elemzésnek" a byline-ja **„By Priya Sundaram · claude-opus · reviewed by a human editor"** — vagyis ez maga is egy Claude (claude-opus) modell által írt, emberi szerkesztő által átnézett blogbejegyzés egy AI-tartalmakra szakosodott oldalon ("dreaming.press"), nem egy hagyományos újságírói vagy akadémiai szakértői forrás. Ez nem teszi hamissá az érvelését (a logikai pont — hogy két különböző mérésről van szó, más-más alapon — magukból az Anthropic-számokból is levezethető), de az SQ06 T3-as, "kritikai elemzés"-ként való jellemzése félrevezető lehet, ha valaki ezt emberi, független szakértői véleményezésnek olvassa.

## Amit ez a döntésre jelent

- A "nincs kontrollált mérés a session-eleji szöveg hatására" állítás pontosításra szorul: van legalább egy releváns, de gyenge (egyszerzős, nem lektorált) kontrollált kísérlet (arXiv:2607.20972), amely azt találja, hogy explicit szöveges "guidance" önmagában nem váltja ki megbízhatóan az önkéntes memóriahasználatot — ez inkább óvatosságra int a "rövid emlékeztető szöveg elég lesz" feltevéssel szemben, mint hogy megerősítené azt.
- A "7%–98%" tartomány a jelentésben pontatlan; a forrásokból igazolható tartomány 7%–83%. Ezt a konkrét számpárt érdemes javítani vagy törölni a végleges anyagból, a mögöttes kvalitatív állítás (erős modell-/családfüggés, a promptolás durva korrekciós ereje) viszont jól alátámasztott, három egymástól független forrásból.
- A hosszhatás ("Lost in the Middle", "context rot") és az azt megkérdőjelező 2026-os null-eredmény egyaránt valós, jól idézett kutatás — a kettő közötti ellentmondás (agentikus/hosszú sessionök vs. tiszta lexikai NIAH-feladatok legújabb modelleken) továbbra is nyitott kérdés, nem félreértés.
- A GSM-IC 18%-os szám technikailag pontos, de 2023-as modellekre vonatkozik; a mai frontier-modellekre való átvitele nem bizonyított ezzel a forrással.
- A Codex-jegy és a MINJA/Rehberger-kockázatok valósak, de eltérő megbízhatósági szinten: a Codex-jegy egy meg nem erősített felhasználói bejelentés, míg a MINJA lektorált akadémiai eredmény és a Rehberger-eset elsődleges, technikailag részletezett biztonsági kutatói közlés.
- Az Anthropic 84%/39% számpár valós, de két különböző mérésből származó, önbevallott, nem auditált belső eval-eredmény; a rá vonatkozó "kritikai elemzés" forrás maga is AI-generált tartalom, ami csökkenti a bizonyító erejét mint "független szakértői vélemény".
- Módszertani mellékészrevétel: az SQ06 jelentés tier-jelölése (T1/T2/T3) nem teljesen konzisztens — legalább egy egyszerzős, nem lektorált arXiv-preprintet (ToolFailBench) T1-ként kezel, miközben hasonló státuszú másik preprinteket (pl. a Zenodo null-eredményt) T2-ként.

## Meglátogatott linkek

| Cím | URL | Tier | Eszköz |
|---|---|---|---|
| LLM Agents Already Know When to Call Tools (WHEN2TOOL) | https://arxiv.org/pdf/2605.09252v2 | T1 | Exa fetch |
| LLM Agents Already Know When to Call Tools (abs) | https://arxiv.org/abs/2605.09252 | T1 | Exa fetch |
| Tunable Tool-Call Rates via Representation Steering | https://arxiv.org/html/2608.25198v1 | T1 | Exa fetch |
| Tunable Tool-Call Rates via Representation Steering (abs) | https://arxiv.org/abs/2608.25198 | T1 | Exa fetch |
| ToolFailBench (ar5iv) | https://ar5iv.labs.arxiv.org/html/2607.04686 | T2 | Exa fetch |
| ToolFailBench (abs) | https://arxiv.org/abs/2607.04686 | T2 | Exa fetch |
| Codex Desktop stale memory overrides AGENTS.md — issue #39223 | https://github.com/openai/codex/issues/39223 | T2 | Exa fetch |
| Managing context on the Claude Developer Platform (Anthropic) | https://www.anthropic.com/news/context-management | T1 | Exa fetch |
| The 84% and the 39% (dreaming.press, AI-szerzőségű) | https://dreaming.press/posts/anthropic-context-editing-84-percent-39-percent-numbers-examined.html | T3 | Exa fetch |
| Large Language Models Can Be Easily Distracted (GSM-IC, ICML 2023) | https://proceedings.mlr.press/v202/shi23a.html | T1 | Exa fetch |
| GSM-IC PDF | https://proceedings.mlr.press/v202/shi23a/shi23a.pdf | T1 | Exa fetch |
| MINJA — NeurIPS Abstract | https://proceedings.neurips.cc/paper_files/paper/2025/hash/42a97bbd9844d2bf68596730af80bcdf-Abstract-Conference.html | T1 | Exa fetch |
| MINJA — arXiv full text | https://arxiv.org/pdf/2503.03704 | T1 | Exa search+fetch |
| MINJA — NeurIPS poster page | https://nips.cc/virtual/2025/loc/san-diego/poster/118152 | T1 | Exa search |
| Is Context Rot Real? (Zenodo null-eredmény) | https://doi.org/10.5281/zenodo.20753848 | T2 | Exa fetch |
| Lost in the Middle (TACL 2024) | https://aclanthology.org/2024.tacl-1.9/ | T1 | Exa fetch |
| Context Rot: How Increasing Input Tokens Impacts LLM Performance (Chroma) | https://www.trychroma.com/research/context-rot | T2 | Exa fetch |
| Context Length Alone Hurts LLM Performance Despite Perfect Retrieval | https://arxiv.org/abs/2510.05381 | T1 | Exa fetch |
| Diagnosing and Mitigating Context Rot in Long-horizon Search | https://arxiv.org/abs/2606.29718 | T1 | Exa fetch |
| ChatGPT: Hacking Memories with Prompt Injection (Rehberger) | https://embracethered.com/blog/posts/2024/chatgpt-hacking-memories/ | T1 | Exa fetch |
| Delivery, Not Storage: Cue-Anchored Working Memory (Saha, 2607.20972) | https://arxiv.org/pdf/2607.20972 | T2 | Exa search+fetch |
| Delivery, Not Storage (abs) | https://arxiv.org/abs/2607.20972 | T2 | Exa fetch |
| Memory tool — Claude Platform Docs (élő oldal, 2026-09-25) | https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool | T1 | Exa fetch |
| agent-memory-lab (GitHub, memória-stratégiák A/B-je, nem a kérdésre válaszol) | https://github.com/EnigmaDevelop/agent-memory-lab | T3 | Exa search |
| Shared Selective Persistent Memory for Agentic LLM Systems | https://arxiv.org/html/2607.09493v1 | T2 | Exa search |

*Megjegyzés a Memory tool doksihoz:* a jelenleg élő oldalon (2026-09-25) NEM találtam meg szó szerint az SQ06 2.1 szakaszában idézett „MEMORY PROTOCOL" / „IMPORTANT: ALWAYS VIEW YOUR MEMORY DIRECTORY..." kikényszerítő szöveget — az oldal jelenlegi szövege ("Claude automatically checks its memory directory before starting a task") ezt csak parafrazálja. Ez az ELL05 feladatlistán kívüli, mellékes észrevétel (nem tartozik az 1–7. pontok közé), ezért nem soroltam önálló verdiktként, de érdemes jelezni: a gyártói dokumentáció gyorsan változik, egy korábban pontosan idézett szöveg mára eltűnhetett az élő oldalról.

---

# ELL06 — Önkéntes memóriahasználat és kérdésenkénti automatikus beadás: az állítások ellenőrzése

*Módszertani megjegyzés: al-ügynököket nem indítottam (degradált mód, a `_ell_kozos.txt` szerint engedélyezett), egyetlen szálon, szekvenciális Exa-kereséssel/-olvasással dolgoztam. Kizárólag `mcp__Exa__web_search_exa` és `mcp__Exa__web_fetch_exa` eszközöket használtam; beépített WebSearch/WebFetch-et nem hívtam. Minden alább idézett forrást magam nyitottam meg és olvastam el — az sq07/sq08 idézeteit nem vettem át ellenőrzés nélkül. A cél a MEGDÖNTÉS volt; ahol ez nem sikerült, azt a primer forrás közvetlen, szó szerinti egyezése indokolja.*

## Verdikt-összefoglaló

| # | Állítás | Verdikt | Egy mondat |
|---|---|---|---|
| 1 | Saha (arXiv:2607.20972): Claude Code + Sonnet 5, Apache Camel, 12 kiértékelt futás, legerősebb állítás n=1-en, kód nyilvános, „injection begets engagement" | **IGAZOLVA** | Az arXiv absztrakt, a teljes HTML-szöveg (§5.2–§5.3) és a nyilvános `github.com/swapnanil/vectr` repó szó szerint megerősíti mind a hat elemet. |
| 2 | MEMTRACK (arXiv:2510.01353, NeurIPS 2025): „LLMs cannot use memory tools effectively", hibamód | **RÉSZBEN** | A cikk létezik és szó szerint ezt írja, a hibamódot (redundáns, ismételt hozzáférés a memória-komponens helyett) is pontosan leírja — de az OpenReview-PDF lábléce szerint ez kifejezetten a NeurIPS 2025 **„Scaling Environments for Agents" workshop** anyaga, nem a fő konferenciasáv, amit a „NeurIPS 2025" megjelölés önmagában nem tesz egyértelművé. |
| 3 | Karbantartói idézetek („LLMs are non deterministic", „one cannot enforce…") — projekt és szerző | **IGAZOLVA** | Szó szerint megtalálható a `alioshr/memory-bank-mcp` #24 GitHub-hibajegyben, a repó tulajdonosa/karbantartója (`alioshr`) írta. |
| 4 | Kérdésenkénti hookok (Claude Code, Codex, Gemini CLI: prompt + additionalContext; Cursor: csak blokkolás; Copilot config-hook kimenete eldobva; Antigravity nincs ilyen) | **IGAZOLVA** | Mind az öt kliens hivatalos dokumentációja (és Cursor/Copilot esetén további GitHub-issue-k, fórumbejegyzések) szó szerint megerősítik a leírt képesség-mátrixot. |
| 5 | Időkorlátok és hibakezelés a három beadásra képes kliensnél | **IGAZOLVA** | Claude Code (30s, timeoutkor eldobott kimenet/fail-open, exit 2 blokkol), Codex (600s alapértelmezett, timeoutkor `outcome:"timeout"`, a prompt mégis átmegy), Gemini CLI (60000 ms alapértelmezett, forráskóddal is alátámasztva) — mindhárom hivatalos dokumentációból és/vagy forráskódból közvetlenül igazolva. |
| 6 | mem0 visszavonta a „vak" kérdésenkénti keresést; claude-mem alapból kikapcsolta a szemantikus beadást | **IGAZOLVA** | A `mem0ai/mem0` PR #4992 és a `claude-mem` 0f97455 commit szó szerint tartalmazza az idézett indoklást. |
| 7 | Mem0-cikk (arXiv:2504.19413) számai; RAG-irodalom 6–11 pp esés hasonló-de-irreleváns szövegnél | **RÉSZBEN** | A Mem0-számok (91% p95-late­ncia-csökkenés, 90%+ token-megtakarítás, enyhe pontosság-előny a teljes kontextusnak) szó szerint stimmelnek a Táblázat 2-vel; a „6–11 százalékpont" szám is pontosan szerepel — de ez **egyetlen kutatás** (Amiraz et al.) két megjelenési formája (ACL 2025 teljes cikk + ugyanannak CEUR-WS „extended abstract"-ja), nem két független RAG-tanulmány, ahogy „a lektorált RAG-irodalom" megfogalmazás sugallhatja. |

## Állításonként

### 1. Saha (arXiv:2607.20972) — IGAZOLVA

Az arXiv absztraktból közvetlenül:

> „All arms run the same agent product, same model (Claude Sonnet 5, claude-sonnet-5), same prompt, same corpus SHA." / „implement the reverse option for the stream-mode Resequencer EIP… gated by a harness-provided acceptance test that must pass unmodified plus the resequencer-scoped regression set (-Dtest='*Resequenc*Test', 42 tests)" — https://arxiv.org/html/2607.20972v1, §5

> „Twelve graded runs of a real feature task under asserted launch postures… Arms (9 pilot runs + 3 native-channel runs, all graded)" — https://arxiv.org/abs/2607.20972, §5

> „The seeded-voluntary control (V) is the strongest form of the finding: same four task-relevant notes in the store as the H arms, same connected tools, same guidance — the agent made zero memory calls in 114 turns." — https://arxiv.org/pdf/2607.20972, §5.2 (a korábbi arm-táblázat szerint V arm n=1)

> „Injection begets engagement: the seeded-proxy run (CS) produced the matrix's only memory-hygiene loop… Voluntary memory operations occur after and because of delivery, not instead of it." — https://arxiv.org/pdf/2607.20972, §5.2

A kód nyilvánossága közvetlenül ellenőrizve, a GitHub-repó él, MIT-licenc, a cikk markdown-másolatát is tartalmazza:

> „swapnanil/vectr… Semantic codebase search + persistent working memory for AI code editors… License: MIT License" — https://github.com/swapnanil/vectr

**Nem sikerült megdönteni.** A négy elem (modell/feladat, 12 futás, V-arm n=1 a legerősebb állításhoz, a nyilvános kód) és az „injection begets engagement" mondat szó szerint, több — az arXiv-oldal különböző verzióin (abs/html/pdf) és a szerző saját blogján keresztül is konzisztensen — megjelenik.

### 2. MEMTRACK (arXiv:2510.01353) — RÉSZBEN

A cikk létezik, szerzők a Patronus AI csapata:

> „LLMs cannot use memory tools effectively and using such tools increases redundancy in planning and overall tool use." — https://arxiv.org/abs/2510.01353, Abstract

A hibamód pontos leírása (RQ2 válasz):

> „According to Table 3, we can observe that memory equipped LLMs fail to call memory tools effectively. LLMs with memory tools consistently display increased redundancy as well as drop in performance efficiency. As observed in the qualitative analysis above, models generally prefer repeatedly accessing information over using the memory component." — https://arxiv.org/pdf/2510.01353, §RQ2 (megegyezik a `ar5iv.labs.arxiv.org/html/2510.01353` tükörrel is — két, egymástól technikailag független arXiv-tükör azonos szöveget ad vissza)

**Megdöntés/pontosítás:** az OpenReview-PDF kolofonja explicit módon workshopként azonosítja a megjelenést, nem fő konferenciasávként:

> „39th Conference on Neural Information Processing Systems (NeurIPS 2025) Workshop: Scaling Environments for Agents (SEA)." — https://openreview.net/pdf?id=mVxmbMng4B

Az arXiv-verzió maga is workshop-címkével azonosítja magát:

> „\workshoptitle Scaling Environments for Agents (SEA)" — https://arxiv.org/abs/2510.01353

Ez két, egymástól független forrásból (OpenReview + arXiv-metaadat) megerősített tény, ami a sima „NeurIPS 2025" megjelölést pontosításra szorulónak minősíti: a cikk NeurIPS 2025 **workshopon** (SEA), nem a fő track-en szerepelt. Az sq07 maga is jelezte a bizonytalanságot („a pontos megjelenési sáv… nem volt egyértelműen megállapítható") — ez az ellenőrzés most eldönti: workshop.

### 3. Karbantartói válaszok — IGAZOLVA

Közvetlenül a GitHub-hibajegyből (nem másodkézből):

> „One cannot enforce an MCP tool to be called by an LLM if not through a 'wrapper' (like Cline for instance). Even with an AI 'wrapper' there is no guarantee that an LLM will follow instructions. LLMs are non deterministic." — **alioshr**, https://github.com/alioshr/memory-bank-mcp/issues/24 (2025-08-19T09:22:41Z, a repó tulajdonosa/karbantartója)

A projekt: `alioshr/memory-bank-mcp`. A szerző a repó tulajdonosa (a GitHub-metaadat szerint ő zárta le az issue-t, és ő a leggyakoribb kommentelő karbantartói szerepben).

### 4. Kérdésenkénti hookok — IGAZOLVA

**Claude Code** (`UserPromptSubmit`) — prompt szöveg + `additionalContext`:

> „`UserPromptSubmit` | When you submit a prompt, before Claude processes it" — https://code.claude.com/docs/en/hooks.md

> „The `additionalContext` field passes a string from your hook into Claude's context window." — https://code.claude.com/docs/en/hooks.md

**Codex** (`UserPromptSubmit`) — a hivatalos forrás közvetlenül megerősíti a `prompt` mezőt:

> „Fields in addition to Common input fields: … `prompt` | `string` | User prompt that's about to be sent" — https://developers.openai.com/codex/hooks

> „That `additionalContext` text is added as extra developer context." — https://developers.openai.com/codex/hooks (ugyanott a `UserPromptSubmit` szakaszban)

**Gemini CLI** (`BeforeAgent`) — szó szerint:

> „Fires after a user submits a prompt, but before the agent begins planning… Input Fields: `prompt`: (`string`) The original text submitted by the user… `hookSpecificOutput.additionalContext`: Text that is appended to the prompt for this turn only." — https://geminicli.com/docs/hooks/reference/

**Cursor** (`beforeSubmitPrompt`) — a hivatalos kimeneti séma valóban csak két mezőt támogat, `additionalContext` nincs:

> „// Output { \"continue\": true | false, \"user_message\": \"<message shown to user when blocked>\" }" — https://cursor.com/docs/hooks.md

Hivatalos Cursor-válasz ezt külön is megerősíti egy fórum-hibajegyben:

> „This is actually expected behavior rather than a bug. The `beforeSubmitPrompt` hook currently only supports two output fields: `continue`… `user_message`… It does not support `updated_input` or any field that modifies the prompt text." — https://forum.cursor.com/t/bug-beforesubmitprompt-hook-updated-input-is-silently-stripped-modified-prompt-never-reaches-the-model/158883

**GitHub Copilot** — a config-fájl alapú `userPromptSubmitted` hook kimenete valóban el van dobva (SDK-hook kivétel):

> „`modifiedPrompt` is only honored by SDK programmatic hooks. Command and HTTP config-file `userPromptSubmitted` hooks have their output dropped, including `modifiedPrompt`." — https://docs.github.com/en/enterprise-cloud@latest/copilot/reference/hooks-reference

Ezt két, élő GitHub-hibajegy is megerősíti azzal, hogy még az SDK-alapú (elvben működő) útvonal is jelenleg hibás gyakorlatban:

> „The `additionalContext` field is declared in the TypeScript types for `UserPromptSubmittedHookOutput`… but returning it from an extension hook has no effect -- the value is silently discarded at runtime." — https://github.com/github/copilot-cli/issues/2652

> „In v1.0.59 the planner consumed the additionalContext directive… In v1.0.60 the directive is silently dropped." — https://github.com/github/copilot-cli/issues/3727

**Antigravity** — a hivatalos dokumentáció `PreInvocation` bemeneti mezői között nincs prompt-szöveg mező, csak `invocationNum`, `initialNumSteps` és a közös metaadat-mezők:

> „Input Fields (stdin): `invocationNum` | integer | The 0-indexed sequence number… `initialNumSteps` | integer | The number of steps currently in the trajectory. | (Common Fields) | Includes `conversationId`, `workspacePaths`, `transcriptPath`, `artifactDirectoryPath`, `modelName`." — https://antigravity.google/docs/hooks/

**Nem sikerült megdönteni egyik részállítást sem.** A Cursor- és Copilot-korlátozásokat élő, jelenlegi (2026 áprilisa és júniusa közötti) hivatalos válaszok és hibajegyek is megerősítik — a helyzet a legfrissebb ellenőrzés (2026-09-25) szerint is fennáll.

### 5. Időkorlátok és hibakezelés — IGAZOLVA

**Claude Code:**

> „`timeout` | no | Seconds before canceling. Defaults: 600 for `command`, `http`, and `mcp_tool`… `UserPromptSubmit` lowers the `command`, `http`, and `mcp_tool` default to 30" — https://code.claude.com/docs/en/hooks.md

> „A `command`, `http`, or `mcp_tool` hook that reaches its `timeout` is canceled: Claude Code discards the hook's output, and the hook renders no decision." — https://code.claude.com/docs/en/hooks (spybara-tükrön keresztül szó szerint megerősítve, majd a hivatalos oldalon is)

> „`UserPromptSubmit` | Yes | Blocks prompt processing and erases the prompt" [exit code 2 hatása] — https://code.claude.com/docs/en/hooks

Tehát: exit 2 → blokkol; timeout → a hook kimenete eldobódik, a kérés átmegy (fail-open).

**Codex:**

> „If `timeout` is omitted, Codex uses `600` seconds for most hooks." — https://developers.openai.com/codex/hooks

> „Err(_) => finish_command_run(…, error: Some(format!(\"hook timed out after {}s\", handler.timeout_sec)), outcome: \"timeout\", …)" — https://github.com/openai/codex/blob/main/codex-rs/hooks/src/engine/command_runner.rs

A tesztfájl szerint sikertelen/timeoutolt hook esetén `should_stop: false` — a prompt átmegy.

**Gemini CLI:**

> „`timeout` | `number` | No | Execution timeout in milliseconds (default: 60000)." — https://geminicli.com/docs/hooks/reference/

Forráskódból is megerősítve (a keresési kivonat korábban idézte a `DEFAULT_HOOK_TIMEOUT = 60000` konstanst a `hookRunner.ts`-ben).

**Nem sikerült megdönteni.** Mindhárom szám és a hozzá tartozó hibakezelési szabály közvetlenül a hivatalos dokumentációból/forráskódból igazolt, több független tükrön keresztül konzisztens.

### 6. mem0 és claude-mem visszavonás — IGAZOLVA

A `mem0ai/mem0` PR #4992 (merged, 2026-05-07) leírásából szó szerint:

> „The `on_user_prompt.sh` hook previously ran a blind semantic search against the user's raw prompt and injected the top-5 results into context on every turn. This wasted API calls on prompts where memory wouldn't help, and the raw-prompt-as-query approach produced low-recall results that crowded the context window with noise." — https://github.com/mem0ai/mem0/pull/4992

A `claude-mem` 0f97455 commit (`lagosito/claude-mem` fork, eredeti szerző `thedotmack`, 2026-04-06) commit-üzenete szó szerint:

> „fix: disable semantic inject by default — experimental feature not ready for all users… The per-prompt Chroma vector search injection on UserPromptSubmit adds latency and context noise. Disable by default while we iterate on a more precise file-context approach." — https://github.com/lagosito/claude-mem/commit/0f9745535a4f1193fbe8e646ec7aa2fe3ba31662

**Nem sikerült megdönteni.** Mindkét idézet szó szerint, a primer GitHub-forrásból (PR-leírás, illetve commit-üzenet) ellenőrizve.

### 7. Mem0-cikk (arXiv:2504.19413) és a RAG-irodalom — RÉSZBEN

A Mem0-cikk absztraktjából és Táblázat 2-jéből közvetlenül:

> „Mem0 attains a 91% lower p95 latency and saves more than 90% token cost, thereby offering a compelling balance between advanced reasoning capabilities and practical deployment constraints." — https://arxiv.org/abs/2504.19413, Abstract

> „Full-context | 26031 | - | - | 9.870 | 17.117 | 72.90 ± 0.19%" — https://arxiv.org/html/2504.19413v1, Táblázat 2

> „Although the full-context approach can provide a slight accuracy edge, the memory-based systems offer a more practical trade-off, maintaining near-competitive quality while imposing only a fraction of the token and latency cost." — https://arxiv.org/abs/2504.19413

Ez a rész **teljesen igazolt**: a számok (91% p95-csökkenés, 90%+ token-megtakarítás, enyhe pontosság-előny a teljes kontextusnak) szó szerint és pontosan egyeznek.

A RAG-irodalmi rész számai is pontosan stimmelnek — de **egyetlen kutatásból** származnak két megjelenési formában. Az ACL 2025 teljes cikkből (lektorált, Association for Computational Linguistics):

> „making the accuracy drop from 6 to 11 accuracy points, depending on the LLM" — https://aclanthology.org/2025.acl-long.892.pdf, 4.3. szakasz

Táblázatos adat ugyanonnan: „Llama-3.2-3B: 82.6 → 79.4 (gyenge zavaró) → 71.5 (erős zavaró); Llama-3.1-8B: 80.6 → 80.1 → 73.9" — https://aclanthology.org/2025.acl-long.892.pdf, 1. táblázat

A CEUR-WS „extended abstract" — amely **saját magát** így azonosítja — szó szerint ugyanazokat a számokat közli:

> „This is an extended abstract of [1]." … „baseline accuracy reaches 82.6 and 80.6 for Llama-3.2-3B and Llama-3.1-8B… accuracy declining to 79.4 and 80.1… dropping more dramatically to 71.5 and 73.9… hard distractors causing accuracy decreases of 6 to 11 percentage points" — https://ceur-ws.org/Vol-4026/paper7.pdf

**Megdöntés/pontosítás:** a sq08 megfogalmazása („a lektorált RAG-irodalom szerint") plurálisként, több tanulmányra utaló módon állítja be ezt az eredményt, holott ez **egyetlen szerzőcsapat (Amiraz, Cuconasu, Filice, Karnin) egyetlen kísérlete**, amit két venue-n (ACL 2025 teljes cikk + IIR2025 workshop CEUR-WS extended abstract, amely explicit módon az ACL-cikk kivonata) publikáltak. A számok pontosak és az ACL-megjelenés valóban lektorált, de ez nem két független forrásból származó megerősítés a „RAG-irodalom" egészéről, hanem egy tanulmány két nyomtatott formája.

## Amit ez a döntésre jelent

- A memóriarendszer tervezésének két legfontosabb empirikus alátámasztása (Saha-cikk az önkéntes használat hiányáról, MEMTRACK a memória-eszközök hatástalan használatáról) primer forrásból, szó szerint megerősítést nyert — a projekt „determinisztikus beadás > önkéntes hívás" architekturális döntése (ld. projektleírás: „mikor hogyan injectalunk") közvetlen empirikus alapon áll.
- A kérdésenkénti beadás technikai megvalósíthatósága kliensenként **élesen eltér**, és ez ellenőrzötten stabil (2026 áprilisa–szeptembere között több hivatalos válasz és élő hibajegy is megerősíti): Claude Code, Codex és Gemini CLI ma is támogatja az `additionalContext`-injektálást kérdésenként, Cursor és GitHub Copilot (config-fájl alapú hook esetén) **nem** — ez közvetlenül releváns a „codex, claude stb. támogatása" projektcélra: egy egységes, minden klienst lefedő kérdésenkénti beadási mechanizmus ma nem építhető azonos módon minden célklienshez.
- A zajszűrés (relevancia-küszöb, rövid prompt kihagyása, dedup) nem elméleti aggály, hanem **gyakorlatban két, egymástól független projekt is visszavonta vagy alapból kikapcsolta** a naiv „minden promptnál szemantikus keresés" mintázatot — ez erős érv amellett, hogy a tervezett rendszer ne blindly minden kérdésnél hívjon keresést, hanem küszöbön és/vagy döntési szabályon (rubric) keresztül szűrjön.
- A Claude Code `additionalContext` 10 000 karakteres korlátja és az a tény, hogy túllépéskor a gyakorlatban csak egy rövid (~2000 karakteres) előnézet jut el a modellhez — ezt élő, nyitott GitHub-hibajegy (#84021, #50571) is megerősíti —, kemény tervezési korlát: a memória-beadás formátumát (rövid index + on-demand teljes tartalom, ahogy több elemzett rendszer is teszi) ehhez kell igazítani, nem a nyers memóriatartalom egészét kell injektálni.
- A hibakezelési aszimmetria (van, ahol timeout = fail-open/néma kihagyás; van, ahol exit 2 = kemény blokkolás) azt jelenti, hogy egy kliens-agnosztikus memóriarendszernek klienstől függően eltérő hibatűrési stratégiát kell alkalmaznia — egy univerzális „mindig fail-open" feltételezés Claude Code, Codex és Copilot esetén helytálló, de nem garantált minden eseménytípusra és nem dokumentált egységesen minden kliensnél (pl. Cursor `beforeSubmitPrompt` alapértelmezett timeout száma NINCS FORRÁS).
- A számszerű teljesítmény-előnyök (Mem0: 91% late­ncia-csökkenés, 90%+ token-megtakarítás) valósak és jól idézettek, de a „lektorált irodalom" hivatkozási alapja (ACL 2025 + saját CEUR-WS kivonata) egyetlen kutatási eredmény, nem konvergáló, több csoporttól származó bizonyíték — ezt érdemes a döntési dokumentációban explicit módon egy forrásként, nem többszörös megerősítésként kezelni.

## Meglátogatott linkek

| Cím | URL | Tier | Eszköz |
|---|---|---|---|
| Delivery, Not Storage (arXiv abs) | https://arxiv.org/abs/2607.20972 | T2 | Exa fetch |
| Delivery, Not Storage (arXiv HTML) | https://arxiv.org/html/2607.20972v1 | T2 | Exa fetch |
| Delivery, Not Storage (arXiv PDF-tükör keresésben) | https://arxiv.org/pdf/2607.20972 | T2 | Exa search |
| swapnanil/vectr (GitHub repó) | https://github.com/swapnanil/vectr | T2 | Exa fetch |
| vectr — delivery-not-storage.md (cikk-másolat) | https://github.com/swapnanil/vectr/blob/main/research/brain-memory/delivery-not-storage.md | T2 | Exa search |
| Saha blogja — MCP tool adoption | https://swapnanilsaha.com/blog/mcp-tool-adoption-agents/ | T2 | Exa search |
| MEMTRACK (arXiv abs) | https://arxiv.org/abs/2510.01353 | T1/T2 | Exa fetch |
| MEMTRACK (arXiv PDF) | https://arxiv.org/pdf/2510.01353 | T1/T2 | Exa search |
| MEMTRACK (ar5iv HTML-tükör) | https://ar5iv.labs.arxiv.org/html/2510.01353 | T1/T2 | Exa search |
| MEMTRACK (OpenReview PDF) | https://openreview.net/pdf?id=mVxmbMng4B | T1 | Exa fetch |
| MEMTRACK (NeurIPS 2025 diák) | https://neurips.cc/media/neurips-2025/Slides/124523.pdf | T1 | Exa search |
| MEMTRACK — Liner.com gyorsismertető | https://liner.com/review/memtrack-evaluating-longterm-memory-and-state-tracking-in-multiplatform-dynamic | T3 | Exa search |
| alioshr/memory-bank-mcp #24 | https://github.com/alioshr/memory-bank-mcp/issues/24 | T2 | Exa fetch |
| Claude Code Hooks reference (.md) | https://code.claude.com/docs/en/hooks.md | T1 | Exa fetch |
| Claude Code Hooks reference | https://code.claude.com/docs/en/hooks | T1 | Exa search |
| Claude Code hooks — Spybara tükör (timeout/fail-open szöveg) | https://spybara.com/anthropic/claude-code/history/docs/en/2026-09-15-2358..2026-09-16-2258/hooks/ | T2 | Exa search |
| Claude Code hooks-guide | https://code.claude.com/docs/en/hooks-guide | T1 | Exa search |
| claude-code issue #84021 (10K limit, ~2000 char preview) | https://github.com/anthropics/claude-code/issues/84021 | T1 | Exa search |
| claude-code issue #50571 (persistHookOutput konfigurálhatóság) | https://github.com/anthropics/claude-code/issues/50571 | T1 | Exa search |
| Codex Hooks (developers.openai.com) | https://developers.openai.com/codex/hooks | T1 | Exa fetch + search |
| Codex user-prompt-submit input schema (GitHub) | https://github.com/openai/codex/blob/main/codex-rs/hooks/schema/generated/user-prompt-submit.command.input.schema.json | T1 | Exa search |
| Codex command_runner.rs (timeout kezelés) | https://github.com/openai/codex/blob/main/codex-rs/hooks/src/engine/command_runner.rs | T1 | Exa search |
| Gemini CLI Hooks reference | https://geminicli.com/docs/hooks/reference/ | T1 | Exa fetch |
| Cursor Hooks (.md) | https://cursor.com/docs/hooks.md | T1 | Exa fetch + search |
| Cursor fórum — updated_input silently stripped | https://forum.cursor.com/t/bug-beforesubmitprompt-hook-updated-input-is-silently-stripped-modified-prompt-never-reaches-the-model/158883 | T2 | Exa search |
| GitHub Copilot hooks reference (Enterprise Cloud) | https://docs.github.com/en/enterprise-cloud@latest/copilot/reference/hooks-reference | T1 | Exa fetch + search |
| GitHub Copilot hooks reference (github/docs repo) | https://github.com/github/docs/blob/main/content/copilot/reference/hooks-reference.md | T1 | Exa search |
| github/copilot-cli issue #2652 (additionalContext dropped) | https://github.com/github/copilot-cli/issues/2652 | T1 | Exa search |
| github/copilot-cli issue #3727 (regresszió) | https://github.com/github/copilot-cli/issues/3727 | T1 | Exa search |
| Antigravity Hooks (hivatalos) | https://antigravity.google/docs/hooks/ | T1 | Exa fetch |
| mem0ai/mem0 PR #4992 | https://github.com/mem0ai/mem0/pull/4992 | T1 | Exa fetch |
| claude-mem semantic-inject default-off commit | https://github.com/lagosito/claude-mem/commit/0f9745535a4f1193fbe8e646ec7aa2fe3ba31662 | T1 | Exa fetch |
| Mem0 (arXiv abs) | https://arxiv.org/abs/2504.19413 | T1 | Exa fetch + search |
| Mem0 (arXiv HTML) | https://arxiv.org/html/2504.19413v1 | T1 | Exa fetch |
| The Distracting Effect (ACL Anthology, absztrakt) | https://aclanthology.org/2025.acl-long.892/ | T1 | Exa fetch |
| The Distracting Effect (ACL PDF, 1. táblázat) | https://aclanthology.org/2025.acl-long.892.pdf | T1 | Exa search |
| Quantifying Distraction of Irrelevant Passages (CEUR-WS, IIR2025 workshop) | https://ceur-ws.org/Vol-4026/paper7.pdf | T2 | Exa fetch + search |
| The Distracting Effect (arXiv-tükör, azonos táblázat) | https://arxiv.org/html/2505.06914v1 | T1 | Exa search |
