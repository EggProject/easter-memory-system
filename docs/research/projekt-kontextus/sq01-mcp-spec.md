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
