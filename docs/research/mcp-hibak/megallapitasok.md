# Megállapítások — al-kérdésenként

Kampány: `mcp-hibak` · 2026-09-12


---

## SQ-01 — A hibamodell adverzariális ellenőrzése

# SQ-01 — A hibamodell adverzariális ellenőrzése

**Vizsgált állítás:** „Az MCP-ben a szerver saját üzleti hibáit az eredmény-objektumban
kell visszaadni, `isError: true` mezővel — NEM JSON-RPC protokoll-hibaként. Azért, mert a
kliens a protokoll-hibát csak MAY adja tovább a nyelvi modellnek, az eszköz-hibát viszont
SHOULD. Egy protokollhibaként visszaadott üzleti elutasítás tehát lehet, hogy soha nem jut
el a modellhez."

---

## VERDIKT: **ÁLL**, egy pontosítással a hatókörről

Az állítás minden egyes fő eleme szó szerint, T1-es forrásból (élő specifikáció, séma,
mindkét hivatalos SDK forráskódja és hivatalos dokumentációja) igazolható a 2026-07-28-as
kiadásra nézve, és a próbált megdöntés nem talált ellenbizonyítékot a lényegi állításra —
sőt, a Python SDK hivatalos dokumentációja *erősebben* fogalmaz, mint az eredeti
megállapítás: protokollhiba esetén "nincs semmi, amit a modell olvashatna" (lásd 4-es
pont). A MAY/SHOULD megkülönböztetés valódi, RFC 2119-es normatív kulcsszavakkal, és a
felhasználó saját esete — kötelező paraméterek (indoklás, kategória) hiánya/hibája — a
specifikáció **kifejezett, névvel ellátott kanonikus példája** szerint Tool Execution
Error, tehát `isError: true` alá tartozik, nem protokollhiba alá.

Egyetlen érdemi pontosítás gyengíti az állítás **általánosított** ("Az MCP-ben...")
megfogalmazását: a szabály szó szerint és kizárólag a **`tools/call`**-ra vonatkozik. A
`resources/read`-nek nincs `isError`-ekvivalense — egy erőforrás "nem található" állapota
*mindig* JSON-RPC protokollhiba (ma `-32602`, SEP-2164), mert nincs másik csatorna, amin
keresztül visszamehetne. Ha a projekt ezt a mintát erőforrás-jogosultsági döntésekre
(SQ-02, D-13) is át akarná vinni, az a jelen szabály hatókörén kívül esik — ott nincs
"tedd az eredmény-objektumba" lehetőség, mert a `ReadResourceResult` sémája nem tartalmaz
`isError` mezőt.

Talált még egy kisebb, valódi SDK-inkonzisztenciát (lásd 4-es pont vége): a TypeScript SDK
az "ismeretlen eszköznevet" explicit protokollhibaként dobja (összhangban a spec
szövegével), a Python SDK FastMCP rétege viszont ugyanezt egy általános `except`-ágban
`isError: true` eredménnyé alakítja — ez eltér a spec explicit "Unknown tool → Protocol
Error" besorolásától, de **nem érinti** a fő állítást (üzleti/validációs hibák → `isError`),
mert mindkét SDK ott egyetért.

---

## 1. Szó szerint megvan-e a szöveg a 2026-07-28-as specifikációban?

**IGEN, két helyen is, szó szerint.**

### 1a. A séma (`schema.ts`) — `CallToolResult.isError` doksikommentje

Forrás: `schema/2026-07-28/schema.ts`, a `CallToolResult` interfészben (1796-1838. sor).
T1 — a hivatalos séma-repó forráskódja.

> „Any errors that originate from the tool SHOULD be reported inside the result object,
> with `isError` set to true, _not_ as an MCP protocol-level error response. Otherwise,
> the LLM would not be able to see that an error occurred and self-correct.
>
> However, any errors in _finding_ the tool, an error indicating that the server does not
> support tool calls, or any other exceptional conditions, should be reported as an MCP
> error response."

(Az utolsó "should" itt kisbetűs, tehát leíró próza, nem RFC 2119 kulcsszó — l. 2. pont.)

Forrás-URL:
`https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/2026-07-28/schema.ts`
(a `schema/2026-07-28/` mappa a jelenlegi, 2026-07-28-as kiadás sémája — a repó README-je
ezt nevesíti "first"-ként definiált forrásként).

### 1b. A specifikáció prózai szövege (`server/tools.mdx`) — "Error Handling" szakasz

Ez a valódi forrása a MAY/SHOULD megkülönböztetésnek, és ez a szöveg **szó szerint
megegyezik** az élő, renderelt oldalon (`https://modelcontextprotocol.io/specification/2026-07-28/server/tools#error-handling`)
és a GitHub-repó forrás-mdx-ében is (kétszer ellenőrizve — nyers `curl` letöltés a
raw.githubusercontent.com-ról, illetve a renderelt HTML-ből kinyert szöveg, AI-összefoglaló
nélkül, sima regex-alapú tag-eltávolítással):

> „Clients **MAY** provide protocol errors to language models, though these are less
> likely to result in successful recovery.
> Clients **SHOULD** provide tool execution errors to language models to enable
> self-correction."

Forrás-URL-ek:
- Renderelt: `https://modelcontextprotocol.io/specification/2026-07-28/server/tools`
- Forrás (mdx): `https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/specification/2026-07-28/server/tools.mdx` (476-477. sor a kompakt szerkesztésben; a jelenlegi verzióban ~789-790. sor)

**Kritikus pont — mióta van ez így?** Ez a MAY/SHOULD mondatpár **NEM** szerepel a
2024-11-05, 2025-03-26 és 2025-06-18 kiadású `tools.mdx`-ekben (ellenőrizve mindhárom
verzióra, a teljes "Error Handling" szakasz szó szerinti összevetésével — ott a szakasz a
JSON példával véget ér, nincs utána normatív mondat). **Először a 2025-11-25-ös kiadásban
jelenik meg**, szó szerint ugyanígy, és onnan változatlanul öröklődik a 2026-07-28-as
kiadásba (csak a bekezdés szerkesztése/sorrendje módosult kozmetikailag). Ez azt jelenti,
hogy a megállapítás igaz a *jelenleg érvényes* verzióra, de nem "öröktől fogva" így volt —
kb. egy éve, a SEP-1303 nyomán vált explicitté (l. 6. pont).

---

## 2. Tényleg MAY vs SHOULD, RFC 2119 értelemben?

**IGEN.** A specifikáció oldal explicitly vastagítva, nagybetűvel jelöli mindkét
kulcsszót (`**MAY**`, `**SHOULD**`) a Markdown forrásban, ami a modelcontextprotocol.io
dokumentációs konvenciója az RFC 2119 kulcsszavak kiemelésére (ugyanígy jelöli a `MUST`,
`MUST NOT` szavakat is a "Security Considerations" szakaszban közvetlenül alatta:
„Servers **MUST**: Validate all tool inputs…", „Clients **SHOULD**: …").

Van egy apró stiluseltérés, amit érdemes megjegyezni: a séma-fájl (`schema.ts`)
kommentjében a tool-hiba oldalán nagybetűs "SHOULD" szerepel, de a protokollhiba oldalán
**kisbetűs** "should" ("...or any other exceptional conditions, should be reported as an
MCP error response") — tehát a séma kommentje csak az egyik irányban normatív
(SHOULD-erősségű), a másik irányban leíró próza. A `tools.mdx` specifikáció-oldal viszont
mindkét irányban explicit, nagybetűs kulcsszót használ (MAY / SHOULD) — ez a mérvadó,
teljes erejű normatív szöveg, mert ez a specifikáció fő szövegtestje, a séma csak
kísérő dokumentáció.

---

## 3. Van-e ellenpélda — üzleti/validációs hiba mégis protokollhibaként?

**Igen, egyetlen strukturális ellenpélda van, de az más RPC-metódusra vonatkozik, nem a
`tools/call`-ra**, és éppen ez világítja meg, *miért* van egyáltalán MAY/SHOULD
megkülönböztetés.

### 3a. `resources/read` — nincs `isError`-mező, tehát minden hiba protokollhiba

A `ReadResourceResult` séma (2026-07-28) **nem tartalmaz** `isError` mezőt:

```ts
export interface ReadResourceResult extends CacheableResult {
  contents: (TextResourceContents | BlobResourceContents)[];
}
```

(Forrás: `schema/2026-07-28/schema.ts`.) Emiatt egy "az erőforrás nem található" állapot —
ami tartalmilag ugyanolyan "üzleti" jellegű, mint egy tool-validációs hiba — **nem tud**
az eredmény-objektumba kerülni, mert nincs hozzá mező. A specifikáció ezért ide egy külön
SEP-et (SEP-2164, "Standardize Resource Not Found Error Code") írt, ami a kódot
`-32002`-ről (JSON-RPC "server error" tartomány, implementáció-függő) `-32602`-re
(Invalid Params) egységesíti — de a mechanizmus mindkét esetben **JSON-RPC
protokollhiba marad**, mert nincs másik csatorna.

Forrás: `https://modelcontextprotocol.io/seps/2164-resource-not-found-error` (T1,
elfogadott/Final SEP). Idézet az Abstract-ból:

> „The current MCP specification recommends -32002 as the error code for resource not
> found. However, -32002 falls within the JSON-RPC "server error" range (-32000 to
> -32099) which is reserved for implementation-defined errors, not protocol-level
> semantics. […] This SEP standardizes on -32602 (Invalid Params), the correct JSON-RPC
> error code for this case, and aligns the specification with the JSON-RPC standard."

**Ez az egyetlen valódi "üzleti hiba mint protokollhiba" eset a specifikációban** — de
strukturálisan indokolt (nincs `isError`-slot a `resources/read`-hez), nem azért van, mert
a spec megengedné a `tools/call`-nál is a protokollhiba-utat üzleti tartalomra. A
`tools/call`-ra nincs ilyen kivétel.

### 3b. `-32602` (Invalid Params) kettős szerepe

A `-32602` kód a specifikációban **kétféle, egymástól elválasztott** dologra szolgál:

1. **Protokoll-szintű** "invalid params": a `CallToolRequest` boríték maga hibás (pl.
   `name` mező hiányzik, vagy nem string) — ez valódi JSON-RPC hiba.
2. **Üzleti validációs hiba B-terve (csak a `resources/read`-nél és néhány SDK-belső
   esetnél)**: pl. a fenti resource-not-found. Ez félrevezető is lehet, mert **ugyanaz a
   számkód** két kategorizálásra használatos a specifikáció más-más pontjain — de a
   `tools/call` világában a `-32602` kizárólag a boríték-szintű hibákra (pl. "Unknown
   tool") vonatkozik, az input-validációs hibák (a tool saját `inputSchema`-ja szerint)
   oda NEM tartoznak — l. 7. pont.

Nincs olyan hivatalos szövegrész, ami azt mondaná, hogy egy tool saját üzleti-logikai
elutasítását (pl. "nincs jogod ehhez a kategóriához") *szabad* protokollhibaként
visszaadni a `tools/call` kontextusban. A `resources/read` kivétele strukturális, nem
filozófiai megengedés.

---

## 4. Mit csinálnak a hivatalos SDK-k a gyakorlatban? (a legerősebb ellenőrzés)

### 4a. TypeScript SDK (`modelcontextprotocol/typescript-sdk`, `main` ág, a 2026-07-28
kiadással párhuzamos v2-fejlesztési vonal — lásd a `packages/core-internal/src/wire/rev2026-07-28/` mappát a repóban)

Fájl: `packages/server/src/server/mcp.ts`, a `tools/call` handler
(`this.server.setRequestHandler('tools/call', …)`), kb. 209-233. sor:

```ts
this.server.setRequestHandler('tools/call', async (request, ctx) => {
    const tool = this._registeredTools[request.params.name];
    if (!tool) {
        throw new ProtocolError(ProtocolErrorCode.InvalidParams, `Tool ${request.params.name} not found`);
    }
    if (!tool.enabled) {
        throw new ProtocolError(ProtocolErrorCode.InvalidParams, `Tool ${request.params.name} disabled`);
    }

    try {
        const args = await this.validateToolInput(tool, request.params.arguments, request.params.name);
        const result = await this.executeToolHandler(tool, args, ctx);
        await this.validateToolOutput(tool, result, request.params.name);
        if (isInputRequiredResult(result)) return result;
        return this.server.projectCallToolResult(result, tool.outputSchemaJson);
    } catch (error) {
        if (error instanceof ProtocolError && error.code === ProtocolErrorCode.UrlElicitationRequired) {
            throw error; // Return the error to the caller without wrapping in CallToolResult
        }
        return this.createToolError(error instanceof Error ? error.message : String(error));
    }
});
```

Ahol `createToolError` (247-256. sor):

```ts
private createToolError(errorMessage: string): CallToolResult {
    return { content: [{ type: 'text', text: errorMessage }], isError: true };
}
```

**Ez pontosan megfelel a spec kategorizálásának:**
- "Tool not found" / "Tool disabled" → valódi `ProtocolError` dobás, **a `try`-blokkon
  kívül** → tényleges JSON-RPC hibaként hagyja el a szervert.
- **Minden más** — beleértve a `validateToolInput`-ban dobott hibát is, ami a tool saját
  `inputSchema`-ja elleni validációs hiba (l. 7. pont) — a `try`-blokkon belül van, a
  `catch` elkapja, és `createToolError`-ral `isError: true` eredménnyé alakítja. Az
  egyetlen kivétel az `UrlElicitationRequired` kódú `ProtocolError`, amit direkt
  újradob — ez egy szerkezeti (out-of-band elicitation) eset, nem üzleti hiba.

Külön érdekesség: a `validateToolInput` maga is egy `ProtocolError(ProtocolErrorCode.InvalidParams, …)`
példányt dob input-validációs hiba esetén (270-282. sor) — vagyis egy `ProtocolError`
*osztályú* kivétel is `isError: true`-vá alakul, ha nem a kifejezetten kizárt
`UrlElicitationRequired` kóddal érkezik. Ez azt mutatja, hogy a "ProtocolError" itt csak
egy belső jelzési mechanizmus/osztály, és nem maga dönt a drótra kerülő formáról — a
`tools/call` handler `catch`-hálója dönt.

Forrás: `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/packages/server/src/server/mcp.ts`
(GitHub: `modelcontextprotocol/typescript-sdk`, `packages/server/src/server/mcp.ts`).
Kiegészítő forrás a `ProtocolError` osztályhoz: `packages/core-internal/src/types/errors.ts`,
ami explicit dokumentálja: „Protocol errors are JSON-RPC errors that cross the wire as
error responses."

### 4b. Python SDK (`modelcontextprotocol/python-sdk`, v2.2.0 / `main`)

Fájl: `src/mcp/server/mcpserver/server.py`, `_handle_call_tool` (428-447. sor körül):

```python
async def _handle_call_tool(self, params, context):
    try:
        return await self.call_tool(params.name, params.arguments or {}, context)
    except MCPError:
        raise
    except Exception as exc:
        if isinstance(exc, ToolError) and not isinstance(exc, UnexpectedToolError):
            ...
        else:
            logger.exception("Tool %r raised an unexpected exception", params.name)
        return CallToolResult(content=[TextContent(type="text", text=str(exc))], is_error=True)
```

Vagyis: **minden** kivétel (`ToolError`, egy sima `KeyError`, bármi) `isError: true`
eredménnyé alakul, **kivéve** az `MCPError`-t, amit a kód explicit újradob (`raise`) —
az válik valódi JSON-RPC hibává.

**A hivatalos Python SDK dokumentációja ezt szó szerint, tankönyvi élességgel írja le** —
ez a legerősebb egyetlen idézet, amit a kutatás talált. Forrás:
`https://py.sdk.modelcontextprotocol.io/servers/handling-errors/` (T1, hivatalos SDK-doksi):

> „A tool can fail in three ways, and the SDK treats each differently. Raise `ToolError`
> and the model sees your message. Raise `MCPError` and the protocol sees it. Raise
> anything else and it is a crash: the model learns only that the call failed, and your
> log gets the traceback."

...és a `MCPError`-ra vonatkozó szakaszból:

> „`MCPError` is the SDK's protocol error. It is the one exception the tool wrapper does
> not catch: it propagates, and the whole tools/call request fails with a JSON-RPC error
> instead of a result. […] **There is no result. No content, no is_error: nothing for the
> model to read. The host application gets the error instead, the same way it would if
> the tool didn't exist at all.**"

...és a döntési szabály:

> „Raise `ToolError` for a failure of execution: the thing your tool tried to do didn't
> work. The model chose the call, so the model should see the consequence and get a
> chance to recover. […] Raise `MCPError` when the request itself should be rejected […]
> No retry from the model fixes any of those, so there is nothing to gain from handing it
> the message. One question decides it: could a smarter model have avoided this? Yes ->
> `ToolError`. No -> `MCPError`."

Ez a megfogalmazás **erősebb**, mint az eredeti kutatási megállapítás "lehet, hogy nem jut
el" (MAY) árnyalata — a hivatalos doksi kategorikusan állítja, hogy `MCPError` esetén
"nincs semmi, amit a modell olvashatna", azaz a hivatalos SDK szintjén ez nem esély
kérdése, hanem garantált: a modell strukturálisan nem kapja meg, hacsak a host-alkalmazás
külön, kézzel be nem vezeti a hibaüzenetet a kontextusba (amit az SDK nem tesz meg
automatikusan — l. 5. pont).

A dokumentáció a resource-hibára is kitér, megerősítve a 3a. pontot:

> „Resources draw the same line, and ship one named exception for the common case. […]
> The SDK turns it into the protocol error the spec assigns to a missing resource: -32602
> with the requested URI in data."

### 4c. SDK-inkonzisztencia (mellékes, de valós megfigyelés)

A Python SDK `ToolManager.call_tool` (`src/mcp/server/mcpserver/tools/tool_manager.py`)
egy ismeretlen eszköznévre **`ToolError`-t** dob ("Unknown tool: {name}"), nem
`MCPError`-t. Mivel a `_handle_call_tool` csak az `MCPError`-t engedi át változatlanul, ez
azt jelenti, hogy a **Python SDK FastMCP rétegében az "ismeretlen eszköz" hiba
`isError: true` eredménnyé alakul**, szemben a specifikáció explicit "Unknown tool = Protocol
Error" kategorizálásával és a TypeScript SDK viselkedésével (ahol ez explicit,
try-blokkon kívüli `ProtocolError`). Ez egy valódi, dokumentált SDK-eltérés a két
hivatalos implementáció között — nem cáfolja a fő állítást (mert az üzleti/validációs
hibák kezelésében mindkét SDK egyetért), de mutatja, hogy a specifikáció betűje és a
gyakorlat nem mindig 100%-ban fedi egymást minden hibakategóriában.

Forrás: `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/src/mcp/server/mcpserver/tools/tool_manager.py`
és `.../src/mcp/server/mcpserver/server.py`.

---

## 5. Van-e olyan kliens, ami mégis továbbadja a protokollhibákat a modellnek?

**Ezen a ponton a bizonyíték gyengébb — ez a kutatás fő rése (l. `gaps.md`).**

Amit T1 forrásból tudunk: a Python SDK kliens-oldali API-ja strukturálisan **két különböző
csatornát** ad a hívó (host/agent) kódnak:

- Tool Execution Error → `await client.call_tool(...)` **rendesen visszatér**, a kapott
  `CallToolResult.is_error` mezővel — ez már eleve "beszélgetés-alakú" adat, amit a legtöbb
  agent-hurok automatikusan a modell kontextusába told, mert ugyanabban a formában
  érkezik, mint egy sikeres válasz.
- Protokollhiba → `await client.call_tool(...)` **kivételt dob** (`MCPError`) a hívó Python
  kódban. Ez azt jelenti, hogy a host-alkalmazásnak *külön, szándékos* kódot kell írnia,
  ami elkapja ezt a kivételt, és a tartalmát (kódot, üzenetet) manuálisan
  visszafordítja a modell számára érthető szöveggé. Ez maga a strukturális oka annak,
  hogy a spec miért "MAY" (nem "MUST", nem "SHOULD") — mert ez mindig extra, nem
  automatikus munka minden egyes host-implementációnak.

Forrás (T1, hivatalos SDK-példa, kifejezetten ezt demonstrálandó írva):
`https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/examples/stories/error_handling/client.py`
— a fájl kommentje maga is ezt mondja: „Prove the two error channels: is_error results
return; MCPError raises."

**Konkrét, éles kliens forráskódját, ami bizonyítottan elnyeli/nem adja tovább a
protokollhibát a modellnek, NEM sikerült T1 szinten azonosítani** (a Claude Desktop, Cursor,
Cline stb. zárt forráskódúak vagy nem voltak elérhetők ebben a kutatási körben). Találtunk
egy **T3-as, egyetlen, megerősítetlen** GitHub-issue-t, ami közvetett bizonyíték arra, hogy
a valós kliensek **eltérően** kezelik ugyanazt a JSON-RPC hibát:

> „All tools work correctly in Claude Code/ROO code/Cline/kilo code/TRAE. However, the
> same memory mcp service encounters an error 32602 when use reading tools like
> 'search_nodes' in the Cursor."
> — https://github.com/modelcontextprotocol/servers/issues/3122 (nincs karbantartói
> válasz vagy magyarázat a jelentésre; T3, gyenge, mert nem tudni, hogy a jelenség oka a
> tárgyalt MAY/SHOULD-mechanizmus, vagy valami más — pl. relatívabb session-kezelési
> különbség).

**Következtetés erre a pontra**: az "lehet, hogy soha nem jut el a modellhez" állítás
*mechanizmusát* T1 szinten megerősítettük (a kivétel-alapú útvonal strukturálisan
elválik a modell-kontextusba kerülő útvonaltól, és a hivatalos doksi kimondja: "nothing
for the model to read"). Azt viszont, hogy *a gyakorlatban létező, éles kliensek közül
melyik hogyan viselkedik ezzel*, nem sikerült kimerítően, cégnév szerint dokumentálni —
ez nyitva marad, és jelöljük a `gaps.md`-ben.

---

## 6. Változott-e ez a 2026-07-28-as kiadásban? Érinti-e a `resultType`?

**A MAY/SHOULD szabály tartalmilag nem változott 2025-11-25 óta** (l. 1b. pont) — a
2026-07-28-as kiadás csak kozmetikailag rendezte át a bekezdést (a két kategória leírását
a felsorolás-pontok fejlécébe emelte), a normatív mondatok szó szerint azonosak maradtak.

**A `resultType` mező (2026-07-28, SEP-2322, "Multi Round-Trip Requests") teljesen
ortogonális az `isError` kérdéshez.** A séma szerint minden `Result`-leszármazott
(így a `CallToolResult` is) mostantól kötelezően hordoz egy `resultType: "complete" |
"input_required"` mezőt — ez azt jelzi, hogy a válasz egy lezárt eredmény, vagy egy
többfordulós (MRTR) folyamat közbenső, további bemenetet kérő állapota. A kanonikus
"invalid-tool-input-error.json" példa (l. 7. pont) is `"resultType": "complete"` mellett
hordozza az `"isError": true`-t — a kettő egymástól függetlenül, egyszerre van jelen.
**Nincs olyan összefüggés, hogy egy üzleti hiba `resultType: "input_required"` lenne**,
vagy hogy a `resultType` bármilyen módon módosítaná, kiváltaná vagy felülírná az
`isError`/protokollhiba megkülönböztetést.

Forrás: `docs/specification/2026-07-28/changelog.mdx`, 8. főbb változás; `schema.ts`
`Result` és `CallToolResult` interfészek; a kanonikus példafájl.

---

## 7. A validációs hibák külön esete — a projekt szempontjából a legfontosabb pont

**Ez a pont a projekt saját kötelező paramétereire (indoklás, kategória) nézve
egyértelműen és T1 szinten eldönthető: a séma-szintű bemeneti validációs hiba Tool
Execution Error, tehát `isError: true` alá tartozik — NEM protokollhiba.**

### 7a. A `CallToolRequest` boríték-sémája nem ismeri a tool saját mezőit

```ts
export interface CallToolRequestParams extends InputResponseRequestParams {
  name: string;
  arguments?: { [key: string]: unknown };
}
```

(`schema/2026-07-28/schema.ts`.) Az `arguments` mező **teljesen tipizálatlan**
(`{ [key: string]: unknown }`) a protokoll-boríték szintjén. Ez azt jelenti, hogy a
"Malformed requests (requests that fail to satisfy CallToolRequest schema)" — amit a spec
Protocol Error-ként sorol be — **csak** azt ellenőrzi, hogy `name` string-e és
`arguments` objektum-e (vagy hiányzik-e). A tool saját, deklarált `inputSchema`-ja elleni
validáció (pl. "indoklás" kötelező mező, "kategória" enum-érték) **nem** ennek a
sémának a része — az egy külön, szerver-oldali lépés.

### 7b. A spec explicit, kanonikus példája pontosan ezt a forgatókönyvet mutatja

A `server/tools.mdx` "Error Handling" szakasza szó szerint így sorolja be:

> „2. **Tool Execution Errors** contain actionable feedback that language models can use
> to self-correct and retry with adjusted parameters:
>    - API failures
>    - **Input validation errors (e.g., date in wrong format, value out of range)**
>    - Business logic errors"

...és a hozzá tartozó kanonikus JSON-példa fájlneve is ezt erősíti meg:
`schema/2026-07-28/examples/CallToolResult/invalid-tool-input-error.json`:

```json
{
  "resultType": "complete",
  "content": [{"type": "text", "text": "Invalid departure date: must be in the future. Current date is 08/08/2025."}],
  "isError": true
}
```

Ez egy **elnevezett, hivatalos, sémaszintű canonical example** — nem csak prózai leírás —
arra, hogy egy bemeneti (schema-szintű) validációs hiba `isError: true` eredmény, nem
JSON-RPC hiba.

### 7c. Ez nem mindig volt így ilyen egyértelműen — a SEP-1303 története

A 2024-11-05 / 2025-03-26 / 2025-06-18 kiadásokban a besorolás **kétértelmű** volt:
"Invalid arguments" a Protocol Errors alatt szerepelt, "Invalid input data" pedig a Tool
Execution Errors alatt — a két megfogalmazás gyakorlatilag megkülönböztethetetlen volt
egymástól, ami valós zavart okozott a fejlesztők körében. Ezt oldotta fel a **SEP-1303**
("Input Validation Errors as Tool Execution Errors", létrehozva 2025-08-05, Final
státusz), aminek Abstract-ja szó szerint ezt mondja (T1,
`https://modelcontextprotocol.io/seps/1303-input-validation-errors-as-tool-execution-errors`):

> „This SEP proposes treating tools input validation errors as Tool Execution Errors
> rather than Protocol Errors. This change would enable language models to receive
> validation error feedback in their context window, allowing them to self-correct and
> successfully complete tasks without human intervention, significantly improving task
> completion rate."

...és a Motivation szakasz kimondja a jelen kutatás fő tézisét is, mint az akkori
probléma leírását:

> „Protocol Errors are catch at the application level by the MCP Client. Only Tool
> Execution Errors are forwarded back to the model as JSON-RPC responses. With the
> current specifications, models cannot see these error messages and thus cannot
> self-correct, leading to repeated failures and poor user experiences."

Ez a SEP vezetett a "Malformed requests (fail CallToolRequest schema)" vs. "Input
validation errors (date formátum, érték tartomány)" mai, egyértelmű kettéválasztásához.

### 7d. SDK-megerősítés

Mindkét SDK forráskódja megerősíti 7a-7b-t (l. 4. pont): a TypeScript SDK
`validateToolInput` metódusa a tool `inputSchema`-ja elleni validációs hibát a `try`
blokkon *belül* dobja, így az a `catch`-en át `isError: true`-vá válik. A Python SDK
hivatalos doksija (`tutorial001.py`, `docs_src/handling_errors/`) kifejezetten egy
"nincs a katalógusban" (tehát bemenet-vezérelt, üzleti) hibát `raise ToolError(...)`-ként
mutat be mintapéldaként, ami `is_error=True` eredményt hoz létre — **nem** `MCPError`-t
ajánl erre az esetre (sőt, a doksi kifejezetten *rossz döntésként* mutatja be, amikor
valaki tévedésből `MCPError`-t használ egy javítható bemeneti hibára — l. 4b. pont, "the
second version of get_author made the wrong choice").

**Következtetés a projektre nézve:** ha a szerver a "indoklás" vagy "kategória" mezőt a
tool `inputSchema`-jában kötelezőként/enumként deklarálja, és a hívás ezt nem teljesíti,
az — mind a specifikáció szövege, mind mindkét hivatalos SDK viselkedése szerint —
**Tool Execution Error**, tehát `isError: true` eredményben, szöveges, a modell számára
javítható üzenettel kell visszaadni. Ezt protokollhibaként (JSON-RPC `error` mezőben)
visszaadni **eltérne** a specifikáció explicit, kanonikus példájától, és megfosztaná a
modellt attól, hogy lássa és javítsa a hibát — pontosan a SEP-1303 által leírt, korábban
valós problémától.

---

## Összefoglaló táblázat — mit talált a próbált megdöntés

| # | Ellenőrzési pont | Eredmény |
|---|---|---|
| 1 | Szó szerint megvan-e a 2026-07-28 specifikációban | **Igen**, két helyen (séma-komment + spec-próza), élő oldalon és forrás-mdx-ben egyaránt ellenőrizve |
| 2 | Valódi MAY vs SHOULD (RFC 2119) | **Igen**, explicit nagybetűs kulcsszavak a spec fő szövegében |
| 3 | Van-e ellenpélda üzleti hibára mint protokollhibára | **Igen, egy, de hatókör-korlátozott**: `resources/read` nem-található hibája (SEP-2164) — strukturális okból (nincs `isError`-slot), nem filozófiai kivétel |
| 4 | Mit csinálnak a hivatalos SDK-k | **Megerősíti, sőt erősíti** az állítást — mindkét SDK forráskódja és a Python SDK hivatalos doksija szó szerint ugyanezt a kettéválasztást implementálja |
| 5 | Van-e kliens, ami mégis továbbadja a protokollhibát | **Részben nyitott** — strukturális bizonyíték van (kivétel vs. visszatérési érték), konkrét éles kliens-forráskód nem volt elérhető; egy gyenge (T3) jelzés van kliens-eltérésre |
| 6 | Változott-e 2026-07-28-ban / érinti-e a `resultType` | A MAY/SHOULD szöveg 2025-11-25 óta változatlan; a `resultType` teljesen ortogonális |
| 7 | Validációs hibák (a projekt saját esete) | **Egyértelműen `isError`-eset**, kanonikus, elnevezett spec-példával és mindkét SDK dokumentált viselkedésével alátámasztva |

**A legerősebb egyetlen bizonyíték az állítás mellett**: a hivatalos Python SDK
dokumentációjának mondata — „There is no result. No content, no is_error: nothing for the
model to read." — mert ez nem egy MAY-szintű lehetőség leírása, hanem a tényleges,
garantált SDK-viselkedés dokumentálása arra az esetre, amikor egy hiba protokollhibaként
(nem `isError`-ral) kerül visszaadásra.


---

## SQ-02 — Jogosultság-elutasításkor mit szabad elárulni

# SQ-02 — Jogosultság-elutasításkor mit szabad elárulni?

Kutatta: Sonnet keresőügynök · Dátum: 2026-09-12
Tier-jelölés minden állításnál: **T1** = RFC/szabvány/hivatalos gyártói dok, **T2** = megbízható
másodlagos (pl. MDN, biztonsági cég elemzése, jó hírű blog), **T3** = fórum/vélemény/blog.

---

## 1. A 403 vs 404 vita — mit mond az RFC 9110 szó szerint

A [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) (HTTP Semantics, 2022, ez az
érvényben lévő HTTP-szemantika-szabvány) szövegét közvetlenül letöltöttem
(`rfc-editor.org/rfc/rfc9110.txt`) és a 15.5.4/15.5.5 szakaszokat soronként ellenőriztem. **[T1]**

**15.5.4. 403 Forbidden** (idézet, szó szerint):

> "The 403 (Forbidden) status code indicates that the server understood the request but
> refuses to fulfill it. A server that wishes to make public why the request has been
> forbidden can describe that reason in the response content (if any)."
>
> "An origin server that wishes to "hide" the current existence of a forbidden target
> resource **MAY** instead respond with a status code of 404 (Not Found)."

**15.5.5. 404 Not Found** (idézet, szó szerint):

> "The 404 (Not Found) status code indicates that the origin server did not find a current
> representation for the target resource or **is not willing to disclose that one exists**."

**Ez a kérdés kulcs-válasza: igen, az RFC kifejezetten kimondja, hogy 404 adható elrejtés
céljából** — de ez egy explicit **MAY** (opcionális) kivétel a 403 szakaszban, nem a 404
alapértelmezett jelentése. Az RFC szerkezete azt sugallja, hogy:
- a 403 az "őszinte" (semantically correct) válasz jogosultsághiányra,
- a 404-et **eredetszerverek választhatják**, ha kifejezetten el akarják rejteni egy erőforrás
  létezését — ez egy tudatos, nevesített kivétel, nem az általános szabály.

A klasszikus érvelés mindkét oldalon:
- **403 mellett**: szemantikailag pontos, könnyebb debug/hibakeresés, a HTTP-kliens és a
  fejlesztő azonnal tudja, hogy hitelesítés/engedély a probléma.
- **404 mellett**: megakadályozza a magánerőforrások létezésének megerősítését
  (enumeration/probing elleni védelem) — ezt választotta pl. a GitHub (ld. 5. pont).

Forrás: [RFC 9110 (rfc-editor.org)](https://www.rfc-editor.org/rfc/rfc9110.html), nyers
szöveg archiválva: `sq02/nyers-forrasok/rfc9110-403-404-snippet.txt`.

Megerősítő **[T2]** forrás (MDN, közvetlenül RFC 9110-re hivatkozva):
[MDN 403 Forbidden](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/403):
> "Server owners may decide to send a 404 response instead of a 403 if acknowledging the
> existence of a resource to clients with insufficient privileges is not desired."

---

## 2. Biztonsági iránymutatások — OWASP és CWE

### OWASP Top 10:2021 — A01 Broken Access Control **[T1]**
Az official markdown forrást töltöttem le
([github.com/OWASP/Top10](https://github.com/OWASP/Top10/blob/master/osib/docs/A01_2021-Broken_Access_Control.md)).
A "How to Prevent" lista **nem tartalmaz** 403/404 vagy létezés-elrejtési utasítást. Az
egyetlen releváns, általános elv: "Except for public resources, deny by default." A dokumentum
hivatalosan a **CWE-200** (Exposure of Sensitive Information to an Unauthorized Actor) hozzárendelt
gyengeségek közé tartozik ehhez a kategóriához.

### OWASP ASVS 4.0.3 — V4 Access Control **[T1]**
Az official markdownot közvetlenül letöltöttem
([github.com/OWASP/ASVS](https://github.com/OWASP/ASVS/blob/master/4.0/en/0x12-V4-Access-Control.md)).
**Nincs benne 403/404-re vagy létezés-elrejtésre vonatkozó tétel.** Csak általános
IDOR/least-privilege követelmények (4.1.3, 4.2.1) szerepelnek.

### OWASP ASVS 4.0.3 — V7 Error Handling and Logging **[T1]** — a legközelebbi találat
Ez a legfontosabb ASVS-idézet a kérdésünkhöz. A **7.4.1** követelmény (L1 szint — vagyis
minden szintre kötelező alapkövetelmény, CWE-210):

> "Verify that a generic message is shown when an unexpected or security sensitive error
> occurs, potentially with a unique ID which support personnel can use to investigate."

Ez **normatív** ("Verify that..." = ASVS-ben ez a MUST-nak megfelelő ellenőrzési forma) és
**pontosan az a mintázat, amit a tulajdonos javasol**: általános hibaüzenet-forma +
nyomkövetési azonosító. **De fontos korlátozás**: ez "unexpected or security sensitive error"-ra
vonatkozik általánosságban (pl. stack trace-ek, rendszerhibák elrejtésére), **nem specifikusan
a 403-vs-404 jogosultsági kérdésre** — az ASVS sehol nem mondja ki explicit módon, hogy a
jogosultság-elutasítást is ebbe a kategóriába kellene sorolni, bár a szellemisége odavág.
Forrás: `sq02/nyers-forrasok/owasp-asvs-v7-error-logging.md`.

### OWASP Cheat Sheet Series — Authorization Cheat Sheet **[T1 hivatalos, de nincs benne
explicit iránymutatás]**
A teljes markdownot letöltöttem
([raw.githubusercontent.com](https://raw.githubusercontent.com/OWASP/CheatSheetSeries/master/cheatsheets/Authorization_Cheat_Sheet.md)).
**Nincs benne "403", "404", "hide", "disclose" vagy "enumeration" szó.** Van egy IDOR-példa,
amely retorikai kérdésként veti fel: "lesz-e a hiba egyszerűen a 523-as fiók
nem-létezésének eredménye, vagy egy sikertelen hozzáférés-ellenőrzés miatt?" — de ez **nem
zárul le ajánlással**, csak illusztrálja a problémát.

Az **Access Control Cheat Sheet elavult** és az Authorization Cheat Sheet-re irányít át — ott
sincs 403/404 vagy létezés-elrejtési tartalom.

### CWE bejegyzések **[T1]**

- **[CWE-209](https://cwe.mitre.org/data/definitions/209.html)** — Generation of Error Message
  Containing Sensitive Information. Általános kategória; a CVE-2008-1579 példa mutatja, hogy
  hibaüzenetből ki lehet következtetni felhasználók létezését — analóg a mi kérdésünkkel, de
  nem specifikusan authorization-ról szól.
- **[CWE-210](https://cwe.mitre.org/data/definitions/210.html)** — Self-generated Error Message
  Containing Sensitive Information (a CWE-209 gyermeke). **Ezt hivatkozza az ASVS 7.4.1.**
- **[CWE-200](https://cwe.mitre.org/data/definitions/200.html)** — Exposure of Sensitive
  Information to an Unauthorized Actor. Az OWASP Top10 A01-hez hivatalosan hozzárendelt CWE.
- **[CWE-203](https://cwe.mitre.org/data/definitions/203.html)** — Observable Discrepancy —
  **ez áll legközelebb a konkrét jelenséghez**: "The product behaves differently or sends
  different responses under different circumstances in a way that is observable to an
  unauthorized actor." Megfigyelt példája (CVE-2004-0778) egy verziókezelő rendszerről szól,
  amely eltérő hibaüzeneteket ad nem létező fájlokra/könyvtárakra, ezzel elárulva azok
  létezését — ez **közvetlen analógia** a 403-vs-404 kérdésre, bár nem HTTP-specifikus.

**Összegzés a 2. pontra**: van CWE, ami a jelenséget osztályozza (CWE-203, CWE-200, CWE-209/210),
és van ASVS-tétel, ami a szellemiségében támogatja az "általános hibaüzenet" elvet (7.4.1), de
**egyik hivatalos OWASP-dokumentum sem mondja ki kifejezetten**: "jogosultsághiányra 403-at vagy
404-et adj". Ez a hiány maga is fontos megállapítás — lásd a 3. pontot.

---

## 3. ⭐ VAN-E AJÁNLOTT ALAPÉRTÉK? — kiemelt szakasz

**Rövid válasz: nincs olyan T1 szabvány vagy iránymutatás, amely kimondaná: "alapból X-et
válaszd, Y feltétellel" konkrétan a 403-vs-404 jogosultsági kérdésre.** Ezt módszeresen
kerestem — RFC 9110, OWASP Top10, OWASP ASVS (V4 Access Control ÉS V7 Error Handling), OWASP
Authorization Cheat Sheet, CWE-200/203/209/210 — egyikben sincs ilyen explicit alapértelmezési
ajánlás.

Amit **helyette** találtam, ami a legközelebb áll egy "alapértékhez":

1. **RFC 9110 szerkezeti sugallata** (T1, de nem explicit ajánlás): a 403 a "normál" válasz
   jogosultsághiányra; a 404-gyel való elrejtés egy külön kimondott **MAY** kivétel
   ("origin server that **wishes** to hide..."), amit a szerver **választhat**, nem
   alapértelmezett kötelezettség vagy ajánlás. Ez leginkább úgy értelmezhető, hogy az RFC
   *lehetővé teszi*, de nem *javasolja* alapértékként a 404-et.

2. **OWASP ASVS 7.4.1** (T1, normatív MUST-szintű "Verify that..."): "biztonsági szempontból
   érzékeny hiba esetén általános üzenetet kell mutatni, opcionális nyomkövetési azonosítóval."
   Ez **nem specifikusan** a 403/404 kérdésre vonatkozik, de a tulajdonos által kért "általános
   hibaüzenet-forma" elve **pontosan ez** — csak nem a mi konkrét esetünkre alkalmazva, hanem az
   "unexpected or security sensitive error" általános kategóriájára. Ha az ASVS szellemiségét
   extrapoláljuk (amit a kutatás nem tehet meg állításként, csak jelezhet), ez alátámasztaná egy
   olyan alapértéket, ahol a válasz mindig egy generikus, kód/ID-vel ellátott hibaforma —
   függetlenül attól, hogy a mögöttes ok "nincs jogod" vagy "nem létezik".

3. **A gyakorlatban megfigyelt többségi minta** (nem normatív, csak leíró — lásd 5. pont):
   GitHub és GitLab is **404-et** ad (rejtő stratégia) API-szinten jogosultsághiányra; a
   Google Drive is 404-et ad *olvasási* jog hiányában (de 403-at *írási* jog hiányában, amikor
   a fájl létezése már ismert). Ez azt sugallja, hogy a **de facto ipari gyakorlat** inkább a
   404 felé hajlik olvasási/létezési szintű jogosultsághiánynál — de ez **megfigyelés, nem
   szabvány által kimondott ajánlás**.

**Következtetés**: A tulajdonos azon állítása, hogy "kell egy alap ajánlás", jogos igény, de
**nincs rá kész, idézhető szabványos válasz**. Bármilyen alapérték-döntés ebben a rendszerben
**saját tervezési döntés lesz**, amit legfeljebb az ASVS 7.4.1 szelleme (generikus hibaforma +
korrelációs azonosító) és a megfigyelt ipari többségi gyakorlat (404-szerű elrejtés
olvasásnál) tud alátámasztani — nem egy T1 forrás direkt előírása.

---

## 4. A „nem található vagy nem hozzáférhető" egyesített üzenet

Ez a mintázat **létezik és ténylegesen használatban van**, de **nincs neki egységesen elfogadott
neve** a szakirodalomban — ezt kifejezetten kerestem (pl. "ambiguous denial", "unified 404
pattern" stb.), és nem találtam bevett terminust sem T1, sem T2 forrásban. A jelenség mögötti
*sebezhetőség* neve létezik (CWE-203 Observable Discrepancy — ld. 2. pont), de magának a
*védekező mintának* nincs kanonikus neve.

Kik használják ezt ténylegesen, dokumentáltan:

- **GitLab** — hivatalos dokumentáció, szó szerint **[T1]**
  ([docs.gitlab.com/api/rest/troubleshooting](https://docs.gitlab.com/api/rest/troubleshooting/),
  ellenőrizve `curl`-lel):
  > "404 Not Found: A resource couldn't be accessed. For example, an ID for a resource
  > couldn't be found, or the user isn't authorized to access the resource."

  Ez szó szerint az "nem található VAGY nem hozzáférhető" minta hivatalos megfogalmazása —
  **de indoklás nélkül** (GitLab nem mondja meg, *miért* vonta össze a két esetet).

- **Google Drive API** — hivatalos dokumentáció, szó szerint **[T1]**
  ([developers.google.com/workspace/drive/api/guides/handle-errors](https://developers.google.com/workspace/drive/api/guides/handle-errors),
  ellenőrizve `curl`-lel): a `notFound` hiba leírása:
  > "This error occurs when the user doesn't have read access to a file, or the file
  > doesn't exist."

  Ismét szó szerint az egyesített minta — **de csak olvasási jogosultságra**; írási jog
  hiányában (ha a fájl már ismert) a Google **külön 403 `insufficientFilePermissions`
  hibát** ad ("The user does not have sufficient permissions for file {fileId}"), tehát
  Google egy **fokozatos** modellt alkalmaz: amíg a hívó nem látott semmit, egyesíti a két
  okot; amint valamit már látott (pl. metaadatot), explicit 403-at ad.

- **Atlassian Jira** — a `"Issue does not exist or you do not have permission to see it."`
  sztring **maga a szoftver kimenete** (nagyon sok független közösségi jelentés reprodukálja
  szó szerint, pl.
  [community.developer.atlassian.com](https://community.developer.atlassian.com/t/issue-does-not-exist-or-you-do-not-have-permission-to-see-it-via-rest-curl-api/39804)),
  tehát **magas megbízhatósággal tényleges Jira-viselkedés**, de **nem találtam hivatalos
  Atlassian dokumentációs oldalt**, amely ezt a stringet és a mögötte lévő indoklást
  dokumentálná — ez **[T3]** forrásból ismert tény, hivatalos [T1] magyarázat nélkül. Ez
  hiányként a `gaps.md`-ben is szerepel.

**Az érvelés emellett**: a minta pontosan a CWE-203 Observable Discrepancy elleni védekezés —
ha a két eset (nincs / nem látható) egyformán válaszol, a támadó nem tud különbséget tenni, és
nem tudja feltérképezni, mely erőforrás-azonosítók léteznek egy rendszerben, amelyhez nincs
hozzáférése.

---

## 5. Valós rendszerek — mit adnak vissza, és dokumentálják-e miért

| Rendszer | Válasz jogosultsághiányra | Indoklást dokumentálja? | Forrás |
|---|---|---|---|
| **GitHub** (privát repó) | **404** | **IGEN, kifejezetten** — lásd alább | T1, docs.github.com |
| **GitLab** (privát projekt) | **404** | Csak a viselkedést írja le, indoklást nem | T1, docs.gitlab.com |
| **Google Drive API** | **404** olvasásnál / **403** írásnál (ha a fájl már látható) | Nem indokolja, csak leírja | T1, developers.google.com |
| **Atlassian Jira** | Egyesített szöveg ("does not exist or you do not have permission") | Nincs hivatalos dok. találva | T3 (közösségi jelentések) |
| **Microsoft Graph** | 403 `accessDenied` / 404 `itemNotFound` — külön kezelve | A hivatalos hibakezelési oldal nem hasonlítja össze a kettőt, nem tér ki elrejtésre | T1 (részleges — ld. gaps.md) |
| **AWS S3** | **403** (nem 404!) objektum hiányában, ha a hívónak nincs `s3:ListBucket` joga | A viselkedés jól dokumentált több független forrásban, de a *konkrét indoklás mondatát* hivatalos AWS-oldalon nem találtam | T2 (a jelenség), indoklás csak közösségi cikkben |
| **Kubernetes (RBAC)** | **403 Forbidden**, és **explicit módon megnevezi** a kért erőforrást/igét a hibaüzenetben | Nem rejt — sőt, egy 2024-es hibajegy pont azt jelezte biztonsági problémaként, hogy a 403-üzenet *túl sokat* árult el (RBAC-konfigurációs részleteket) | T1 (viselkedés) + T3 (GitHub issue a túlzott közlésről) |

**GitHub hivatalos indoklása** (a legerősebb, legközvetlenebb T1 találat az egész kutatásban),
szó szerint, ellenőrizve `curl`-lel
([docs.github.com/en/rest/using-the-rest-api/troubleshooting-the-rest-api](https://docs.github.com/en/rest/using-the-rest-api/troubleshooting-the-rest-api),
"404 Not Found for an existing resource" szakasz):

> "GitHub uses a `404 Not Found` response instead of a `403 Forbidden` response to avoid
> confirming the existence of private repositories."

Ez az **egyetlen** a vizsgált rendszerek közül, amely **explicit, hivatalos, dokumentált
indoklást** ad a döntésére.

**Kubernetes ellenpéldája**: a [kubernetes/kubernetes #124406](https://github.com/kubernetes/kubernetes/issues/124406)
hibajegy (HackerOne-on jelentve biztonsági problémaként) megmutatja, hogy Kubernetes
alapesetben **nem rejt semmit** — a tiltó üzenet tartalmazza a kért erőforrást/igét
(pl. `forbidden: User "x" cannot get path "/foo"`), és a jegy pont azt kifogásolta, hogy egy
konfigurációs hiba miatt **még ennél is több** (RBAC-belső részletek) szivárgott ki. Ez azt
mutatja: Kubernetes tervezési filozófiája a "mondd meg, mit kértél" — az elrejtés nem cél,
csak a *belső konfiguráció* kiszivárgása számít hibának.

**AWS IAM (általánosan, nem csak S3)**: az IAM saját "access denied" hibaüzenetei
([awsdocs/iam-user-guide](https://github.com/awsdocs/iam-user-guide/blob/main/doc_source/troubleshoot_access-denied.md),
T1) **explicit módon feltárják** a principal ARN-t, az akciót és az erőforrás ARN-t a
hibaüzenetben — ez az **ellentéte** az elrejtésnek, és kifejezetten a hibakereshetőséget
szolgálja. Ez fontos ellenpélda: nem minden AWS-szolgáltatás rejt — az IAM policy-szintű
hibaüzenetek kifejezetten *informatívak*, míg az S3 objektum-szintű 403 kifejezetten *rejtő*.
**AWS-en belül sincs egységes irányelv** — szolgáltatásonként eltér.

---

## 6. ⭐ BEÁLLÍTHATÓVÁ TESZI-E BÁRKI? — kiemelt szakasz

**A vizsgált fő rendszerek (GitHub, GitLab, Google Drive, Jira, Microsoft Graph, AWS, Kubernetes)
egyikénél sem találtam ügyfél-konfigurálható kapcsolót**, amely azt szabályozná, hogy a
jogosultság-elutasítás elrejtse-e egy erőforrás létezését. Mindegyik **egy fixen bekódolt
viselkedést** valósít meg (GitHub/GitLab mindig rejt; Kubernetes mindig felfed; Google
fokozatosan; AWS S3 mindig rejt 403-mal). Ezt módszeresen kerestem célzott keresésekkel
("configurable", "toggle", "setting" + "hide existence" + az egyes rendszerek neve) — nem
találtam.

**DE találtam egy konkrét, más rendszerben, amely pontosan ezt csinálja** — ez a legfontosabb
találat a 6. pontra, és közvetlen precedens a saját tervezési döntésünkhöz:

### Discourse (nyílt forráskódú fórummotor) — `detailed_404` beállítás **[T1]**

Forrás: a Discourse hivatalos GitHub-repója,
[`config/site_settings.yml`](https://github.com/discourse/discourse/blob/main/config/site_settings.yml)
(ellenőrizve `curl`-lel, `security:` szekció, 3103. sor) és
[`config/locales/server.en.yml`](https://github.com/discourse/discourse/blob/main/config/locales/server.en.yml)
(2132. sor, a beállítás admin felületen megjelenő leírása):

- **Beállítás neve**: `detailed_404`
- **Típus**: boolean (be/ki kapcsoló)
- **Elhelyezés**: `security` (Biztonság) beállítási csoport
- **Lehetséges értékek**: `true` / `false`
- **Alapértelmezés**: **`false`** (KIKAPCSOLVA — vagyis alapból REJT)
- **Hivatalos leírás** (szó szerint, a Discourse forráskódjából):
  > "Provides more details to users about why they can't access a particular topic. Note:
  > This is less secure because users will know if a URL links to a valid topic."

**Ez pontosan az a mintázat, amit a tulajdonos kér**: egy elnevezett, be/ki kapcsolható
beállítás, explicit alapértelmezéssel, és a gyártó saját szavaival dokumentált
biztonsági-vs-használhatósági kompromisszummal. Az alapérték a **rejtő** (biztonságosabb)
oldal — a felhasználónak/adminnak *tudatosan* kell bekapcsolnia a részletesebb, de kevésbé
biztonságos módot.

**Összegzés a 6. pontra**: a kifejezetten kért nagy rendszerek egyikénél sincs ilyen kapcsoló
— ez saját magában is fontos, kimondandó negatív eredmény. Van viszont **élő, dokumentált
precedens** (Discourse `detailed_404`) arra, hogy ez a fajta kapcsoló (i) létezik a gyakorlatban,
(ii) alapból a rejtő oldalra áll, és (iii) a gyártó explicit módon kimondja a biztonsági
kompromisszumot a leírásában. Ez erős érv amellett, hogy a mi rendszerünkben tervezett
"beállítható, alapértelmezett ajánlással" megközelítés **nem precedens nélküli, working
mintát követ**.

---

## 7. A „silent failure" ellenérve — mikor okoz több kárt az elrejtés

Ezen a téren **nincs T1 vagy T2 szabványos irodalom** — a CWE/OWASP dokumentumok csak az
elrejtés *elmulasztásának* kockázatát (enumeration) írják le, az elrejtés *saját* költségeit
nem. Amit találtam, mind **[T3]** gyakorlati/blog irodalom, de tartalmilag konzisztens és
konkrét:

- **["Returning HTTP 404 Responses Instead of 403 For Unauthorised Access" (dev.to,
  ashallendesign)](https://dev.to/ashallendesign/returning-http-404-responses-instead-of-403-for-unauthorised-access-22ba)**
  — konkrét hátrányok:
  - *Hibakeresési nehézség*: "returning a 404 for both non-existent resources and
    unauthorised access can make it harder to identify the root cause of an issue."
  - *Korlátozott biztonsági érték*: időzítés-alapú (timing) támadásokkal a létezés így is
    kideríthető — a 404 önmagában nem elég védelem.
  - *Felhasználói zavar*: jogos felhasználók, akik tudják, hogy egy erőforrás létezik, 404-et
    kapva megzavarodnak.
  - Végkövetkeztetés: **szelektív** használatot javasol (csak valódi enumeration-kockázatú,
    nem-publikus erőforrásoknál), nem blanket-politikát.

- **["Not Found is the wrong answer to a permission problem" (dev.to,
  nasrulhazim)](https://dev.to/nasrulhazim/not-found-is-the-wrong-answer-to-a-permission-problem-25cm)**
  — ez a cikk kifejezetten **AI-ügynök/MCP-szerver kontextusban** íródott (ld. 8. pont is), és
  élesen fogalmaz:
  - *Hibakeresési frusztráció*: "It sends them hunting for a typo in the tool name" — a
    fejlesztő/hívó a hibás névre gyanakszik, nem a jogosultságra.
  - *Elvész a cselekvésre ösztönző infó*: a felhasználónak azt kellene hallania, hogy "This
    action requires the X permission" — nem azt, hogy "nem található".
  - Kulcsmondat: **"Visibility is a courtesy, authorisation is a check."** — vagyis az
    elrejtést (visibility) meg kell különböztetni magától az engedélyezés-ellenőrzéstől
    (authorisation): ha valakinek van hozzáférése a szerverhez/eszközhöz, de csak egy adott
    jogosultsága hiányzik, a "nem található" válasz **hazugság**, nem biztonsági intézkedés.
  - Javaslata: az elrejtést **csak** ott alkalmazd, ahol a hívónak *az egész felülethez*
    nincs hozzáférése (szerepkör szinten), és **ne** ott, ahol a hívó jogosult a szerverhez/
    eszközhöz, csak egy konkrét erőforrás-szintű engedélye hiányzik.

- **Valós támogatási teher bizonyítéka** (nem elemzés, hanem közvetlen empirikus jel): a
  GitLab saját issue-trackerén több, évek óta nyitott jegy létezik erre a témára —
  pl. [gitlab-ce#65271 "Release API: return 403 instead of 404 when
  not enough permissions"](https://gitlab.com/gitlab-org/gitlab-ce/-/issues/65271),
  [gitlab#20878 "The 404 response could also indicate a permissions problem? Why not choose
  401 here?"](https://gitlab.com/gitlab-org/gitlab/-/issues/20878),
  [gitlab#36367 "Empty private-token for api call results in '404 Project Not
  Found'"](https://gitlab.com/gitlab-org/gitlab/-/issues/36367) — ezek **[T3]** (issue tracker,
  nem hivatalos állásfoglalás), de önmagukban is bizonyítékai annak, hogy a fejlesztők
  rendszeresen összezavarodnak/panaszkodnak az egyesített 404-válasz miatt.

---

## 8. Gépi hívó esete

**Szabvány vagy hivatalos iránymutatás szintjén ezt nem találtam kimondva sehol** — sem az
OWASP, sem a CWE, sem az RFC nem tesz különbséget ember és gép hívó között. Ez fontos hiány,
amit külön ki kell mondani.

**A releváns MCP-specifikáció maga** (2026-07-28, ugyanaz a verzió, mint a D-35-ben) —
[modelcontextprotocol.io/specification/2026-07-28/basic/authorization](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization)
— **[T1]**, "Error Handling" szakasz:

> "Servers **MUST** return appropriate HTTP status codes for authorization errors:
> | 401 | Unauthorized | Authorization required or token invalid |
> | 403 | Forbidden | Invalid scopes or insufficient permissions |
> | 400 | Bad Request | Malformed authorization request |"

**Fontos hatókör-figyelmeztetés**: ez a táblázat az OAuth-réteg (token/scope-érvényesítés)
hibáira vonatkozik — arra az esetre, amikor a *hozzáférési tokennek* nincs elég hatóköre.
**Nem szól** a mi konkrét esetünkről: amikor egy protokoll-szinten érvényes, megfelelő
hatókörű tokennel rendelkező hívó egy konkrét erőforráshoz (pl. egy adott projekthez tartozó
memória-rekordhoz) fér hozzá, amihez üzleti/rekord-szintű jogosultsága nincs. Ez egy
**réteggel feljebb** dől el a specifikációban, mint ahol a mi SQ-02 kérdésünk ül — az MCP-spec
nem ad iránymutatást a rekord-szintű, alkalmazás-logikai jogosultság-elutasítás formájára.
(Ezt a `gaps.md`-ben is jelzem, és érdemes összevetni az SQ-03 megállapításaival.)

**Gyakorlati/iparági érvelés (mind [T3], de tartalmilag erős és közvetlenül releváns)**:

- **["Not Found is the wrong answer to a permission
  problem"](https://dev.to/nasrulhazim/not-found-is-the-wrong-answer-to-a-permission-problem-25cm)**
  (ugyanaz a cikk, mint a 7. pontban, kifejezetten ügynök-orientált API-tervezésről):
  > "Here's the thing about exposing an app to an agent: every assumption your web UI
  > quietly relies on stops holding. There's no session. There's no human reading the screen
  > and going 'hmm, that's odd.' An agent takes your response literally, and then acts on it."
  >
  > "An agent that only ever receives sentences can't distinguish 'you may not do this' from
  > 'this doesn't exist' from 'your token is too narrow' — and those call for completely
  > different next moves."
  >
  > "Refusals are an API. Design them as carefully as the success payloads. A wrong refusal
  > costs more than a missing feature, because the caller acts on it."

  Ez a cikk **pontosan** a tulajdonos érvelését támasztja alá: gép/ügynök hívónál a
  megkülönböztethetőség nem luxus, hanem funkcionális szükséglet, mert az ügynök nem tud
  "hümmögni" egy furcsa válaszon, hanem szó szerint cselekszik rá.

- **["Why your API's error messages fail when called by an LLM" (dev.to,
  johnonline35)](https://dev.to/johnonline35/why-your-apis-error-messages-fail-when-called-by-an-llm-and-how-to-fix-them-5a5d)**:
  a modell nem tud tisztázó kérdést feltenni ("The LLM can't ask clarifying questions. It
  needs to autonomously recover or the task is dead."), és megfigyelt hibamintaként ismétlődő,
  változatlan újrapróbálkozást ír le, amíg az ügynök fel nem adja a feladatot.

- **[apxml.com kurzusanyag, "Tool Error
  Handling"](https://apxml.com/courses/building-advanced-llm-agent-tools/chapter-1-llm-agent-tooling-foundations/tool-error-handling)**:
  ajánlja a hibák strukturált kategorizálását (pl. `InputValidationError`, `APIFailure`,
  `NetworkError`, `ToolInternalError`), hogy az ügynök el tudja dönteni: újrapróbálja,
  tisztázást kér, vagy feladja. Ez direkt válasz a tulajdonos azon aggályára, hogy a hívónak
  "meg kell tudnia különböztetnie a hibától" a választ, nehogy vég nélkül próbálkozzon.

**Összegzés a 8. pontra**: nincs szabványos (T1/T2) forrás, amely kimondaná, hogy gép- és
emberi hívónál más a helyes válasz — ez tisztán gyakorlati/blog szintű felismerés (T3), bár
tartalmilag erősen konzisztens és közvetlenül a mi helyzetünkre szabott (több forrás
kifejezetten MCP/ügynök-kontextusban íródott). Az egyetlen T1 forrás, ami *egyáltalán* szóba
hozza a gépi hívó kérdését ebben a kontextusban, maga az **MCP-spec hibakezelési táblázata** —
de az egy réteggel feljebb, az OAuth-szintű hozzáférés-ellenőrzésnél ül, nem az
alkalmazás-szintű, rekord-alapú jogosultsági kérdésnél.

---

## Normatív előírás vs. jó gyakorlat — összefoglaló táblázat

| Forrás | Állítás | Normatív (MUST/SHOULD) vagy jó gyakorlat? |
|---|---|---|
| RFC 9110 §15.5.4 | 404 adható elrejtésre | **MAY** (opcionális, normatív engedély, nem előírás) |
| RFC 9110 §15.5.4 | 403-hoz indoklás adható | **CAN** (nem kötelező) |
| OWASP ASVS 7.4.1 | Generikus üzenet + ID biztonsági hibánál | **MUST-szintű ("Verify that")**, de nem a mi konkrét esetünkre írva |
| OWASP Top10 A01 | "Deny by default" | Jó gyakorlat / ajánlás, nem 403/404-specifikus |
| GitHub gyakorlata | 404 magánrepóra | Vállalati tervezési döntés, nem szabvány |
| MCP spec 2026-07-28 | 403 = "insufficient permissions" (OAuth-scope szinten) | **MUST** — de más rétegre vonatkozik, mint a mi kérdésünk |
| Discourse `detailed_404` | Alapból rejt, kapcsolható | Termék-szintű konfigurációs alapérték, nem szabvány |

---

## Mi az, amiben biztos vagyok / Mi az, amiben nem

**Biztos vagyok benne** (T1 forrásból, közvetlenül ellenőrzött szó szerinti idézettel):
- Az RFC 9110 kifejezetten megengedi (MAY) a 404 használatát erőforrás-létezés elrejtésére a
  403 helyett — ez szó szerint benne van a szabványban, ellenőriztem a nyers RFC-szövegben.
- Az OWASP Top10:2021 A01 és az OWASP ASVS 4.0 V4 Access Control **nem** ad explicit 403-vs-404
  ajánlást — ezt a teljes hivatalos szövegek átvizsgálásával állapítottam meg, nem a hiányuk
  feltételezésével.
- Az OWASP ASVS 7.4.1 kifejezetten előírja az általános hibaüzenet + azonosító mintát biztonsági
  szempontból érzékeny hibákra (általánosságban, nem a mi konkrét esetünkre szabva).
- A GitHub hivatalosan, dokumentáltan, indoklással 404-et ad magánrepókra jogosultsághiány
  esetén; a GitLab és a Google Drive is egyesített/rejtő választ ad, de indoklás nélkül.
- A Discourse-nak van egy `detailed_404` nevű, alapból kikapcsolt (rejtő) beállítása pontosan
  erre a problémára, gyártói dokumentációval a kompromisszumról.
- Az MCP 2026-07-28 spec normatív hibatáblázata a 403-at "insufficient permissions"-höz köti,
  de ez az OAuth-scope rétegre vonatkozik, nem a rekord-szintű üzleti jogosultságra.

**Nem vagyok biztos benne / korlátozott a bizonyíték**:
- Az AWS S3 403-vs-404 viselkedésének *konkrét indoklása* csak közösségi (AWS re:Post, nem
  "AWS OFFICIAL" jelölésű) cikkből származik — a viselkedés ténye jól dokumentált, de a hivatalos
  "miért" mondatot nem találtam AWS-oldalon.
- A Microsoft Graph 403/404 pontos, egymáshoz viszonyított hivatalos definícióját
  (`itemNotFound` vs `accessDenied`) nem sikerült egyetlen, teljes hivatalos oldalról
  kiolvasnom — a `security-error-codes.md` lekérés nem hozta vissza a kívánt definíciókat
  (lásd `gaps.md`).
- A Jira "does not exist or you do not have permission" sztringet csak közösségi
  bejegyzésekből ismerem — nagyon valószínű, hogy pontos szoftverkimenet (sok független
  forrás egyezik meg benne), de hivatalos atlassian.com dokumentációt hozzá nem találtam.
- Nem zárható ki teljes bizonyossággal, hogy létezik olyan kevésbé ismert rendszer/keretrendszer,
  amely kifejezetten nevesített, dokumentált 403/404-elrejtési kapcsolót kínál a kutatásban
  megkérdezett hat rendszeren (GitHub/GitLab/Google/Jira/MS Graph/AWS/K8s) kívül — a keresés
  kiterjedt (Spring, Django REST, Laravel, HashiCorp Vault, Docker Registry spec is), de
  negatív eredmény nem bizonyítja a nemlétezést, csak azt, hogy elérhető idővel/eszközzel nem
  találtam ilyet rajtuk kívül a Discourse-on túl.
- A "gépi hívónál más a helyes válasz" állítás mögött **nincs** szabványos (T1/T2) forrás —
  ez tisztán gyakorlati/blog szintű (T3) konszenzus, még ha tartalmilag erős is.


---

## SQ-03 — Mit kell megvalósítania egy szabványos MCP erőforrás-szervernek

# SQ-03 — Mit kell megvalósítania egy szabványos MCP erőforrás-szervernek

Spec-verzió, amihez minden állítás alapból kötve van, hacsak másképp nincs jelölve:
**`2026-07-28`** (a modelcontextprotocol.io `/docs/2026-07-28/learn/versioning` oldal szerint ez a
"Current" — azaz jelenleg érvényes — protokollverzió; l. Q0 lent).

Módszertani megjegyzés: minden idézet a hivatalos `modelcontextprotocol.io` oldalak **nyers
Markdown-forrásából** (a `.md` végződésű URL-változat, amit a Mintlify motor szolgál ki AI-
összefoglalás nélkül) vagy a IETF/RFC-editor nyers szövegéből származik, `curl`-lal letöltve —
tehát nem a `WebFetch` eszköz kis-modelles összefoglalóján keresztül. Ez kiküszöböli azt a
kockázatot, hogy egy AI-összefoglaló kerüljön be idézetként. L. `searches.md`.

Jelölés: **[T1]** = elsődleges forrás (hivatalos MCP spec, RFC, IETF draft). A dokumentum
MUST/SHOULD/MAY szintjét mindig a szó szerinti idézet tartalmazza.

---

## Q0 — Melyik verzió az érvényes, és mi változott a korábbihoz képest

**[T1]** `https://modelcontextprotocol.io/docs/2026-07-28/learn/versioning`:

> "The **current** protocol version is [**2026-07-28**]."

A korábbi verziók sorrendje (ugyanez az oldal, revíziólista és `llms.txt` alapján):
`2024-11-05` → `2025-03-26` → `2025-06-18` → `2025-11-25` → **`2026-07-28`** (current) →
`draft` (folyamatban).

---

## Q1 — Milyen szerepet tölt be az MCP szerver? (erőforrás-szerver / hitelesítési szerver / mindkettő)

**[T1]** `specification/2026-07-28/basic/authorization` — "Roles" szakasz:

> "A protected *MCP server* acts as an [OAuth 2.1 resource server](...), capable of accepting
> and responding to protected resource requests using access tokens."
>
> "An *MCP client* acts as an [OAuth 2.1 client](...), making protected resource requests on
> behalf of a resource owner."
>
> "The *authorization server* is responsible for interacting with the user (if necessary) and
> issuing access tokens for use at the MCP server. The implementation details of the
> authorization server are beyond the scope of this specification. It may be hosted with the
> resource server or a separate entity."

**Értékelés:**
- Az MCP szerver szerepe a specifikációban explicit módon **erőforrás-szerver** (OAuth 2.1
  resource server) — ez a normatív alapállás, nem javaslat szintű.
- A hitelesítési szerver (authorization server) egy **külön OAuth-szerep**, amelynek
  implementációs részletei "beyond the scope" — a spec **nem tiltja**, hogy ugyanaz a fizikai
  szolgáltatás lássa el mindkét szerepet ("It may be hosted with the resource server or a
  separate entity"), de **nem is ír elő** semmilyen konkrét kötelezettséget arra az esetre,
  amikor az MCP szerver saját maga az AS is — azt egyszerűen kívül helyezi a spec hatókörén.
- Tehát: **kötelező szerep = resource server**; az AS-szerep **megengedett, de nem szabályozott**
  extra, ha az üzemeltető úgy dönt, hogy egybe vonja a kettőt. Explicit tiltó ("MUST NOT act as
  authorization server") mondatot **nem találtam** egyik 2026-07-28-as oldalon sem.

---

## Q2 — Védett erőforrás metaadat (RFC 9728)

### 2.1 Kötelező-e kiajánlani?

**[T1]** `specification/2026-07-28/basic/authorization` — "Overview", 4. pont:

> "MCP servers **MUST** implement OAuth 2.0 Protected Resource Metadata ([RFC9728]). MCP
> clients **MUST** use OAuth 2.0 Protected Resource Metadata for [authorization server
> discovery]."

**[T1]** `specification/2026-07-28/basic/authorization/authorization-server-discovery`:

> "MCP servers **MUST** implement the OAuth 2.0 Protected Resource Metadata ([RFC9728])
> specification to indicate the locations of authorization servers. The Protected Resource
> Metadata document returned by the MCP server **MUST** include the `authorization_servers`
> field containing at least one authorization server."

Ez **MUST**-szintű, nem opció — mind a 2025-06-18, mind a 2026-07-28 verzióban azonos erővel
(a 2025-06-18-as oldalon ugyanez a mondat szó szerint megvan, l. `contradictions.md` / verzió-
összevetés).

### 2.2 Melyik végponton, milyen tartalommal?

**[T1]** Ugyanez az oldal, "Protected Resource Metadata Discovery Requirements":

> "MCP servers **MUST** implement one of the following discovery mechanisms to provide
> authorization server location information to MCP clients:
> 1. **WWW-Authenticate Header**: Include the resource metadata URL in the `WWW-Authenticate`
>    HTTP header under `resource_metadata` when returning `401 Unauthorized` responses...
> 2. **Well-Known URI**: Serve metadata at a well-known URI as specified in [RFC9728]. This can
>    be either:
>    * At the path of the server's MCP endpoint: `https://example.com/public/mcp` could host
>      metadata at `https://example.com/.well-known/oauth-protected-resource/public/mcp`
>    * At the root: `https://example.com/.well-known/oauth-protected-resource`"

Fontos pontosítás: ez **"MUST implement one of"** — tehát a szervernek a kettő közül
**legalább az egyiket** kötelező megvalósítania, nem mindkettőt egyszerre. (A kliens oldalon
viszont mindkét felismerési utat kötelező támogatnia — l. lent.)

Maga a `.well-known` végpont RFC 9728-forrása **[T1]** (`rfc9728.txt`, 2. szakasz):

> "resource
>    REQUIRED.  The protected resource's resource identifier, as defined in Section 1.2.
>
> authorization_servers
>    OPTIONAL.  JSON array containing a list of OAuth authorization server issuer
>    identifiers, as defined in [RFC8414], for authorization servers that can be used with
>    this protected resource. ..."

Az MCP spec ezt a mezőt **saját maga MUST-ra szigorítja**: a fenti idézet (2.1 pont) szerint az
`authorization_servers` mező jelenléte "at least one authorization server"-rel MCP-kontextusban
kötelező — miközben az alap RFC 9728-ban ez a mező önmagában csak OPTIONAL. Ez tehát egy **MCP-
specifikus szigorítás** az RFC alapkövetelményéhez képest, nem az RFC saját normatív szintje.

A végpont lekérdezési formátuma **[T1]** (`rfc9728.txt`, 3. szakasz, sor 403–436):

> "A protected resource metadata document MUST be queried using an HTTP ... GET request at the
> previously specified path. ... A successful response MUST use the 200 OK HTTP status code..."

### 2.3 Mi történik, ha hiányzik?

A specifikáció **nem ír elő explicit hibaágat** arra az esetre, ha egy MCP szerver egyáltalán
nem ajánl ki PRM-et (sem fejlécben, sem well-known útvonalon) — de a kliensoldali normatív
folyamatábra ezt implicit módon kezeli. **[T1]**
`authorization-server-discovery` mermaid-diagramja:

> "alt Sub-path metadata found ... else Sub-path not found ... alt Root metadata found ...
> else Root metadata not found ... Note over C: Abort or use pre-configured values"

Vagyis: ha a szerver **nem** ajánlja ki a PRM-et egyik csatornán sem, a kliens architektúrálisan
elő van készítve arra, hogy **megszakítsa a folyamatot vagy előre konfigurált (out-of-band)
értékekre essen vissza** — de ez kliens-viselkedés, nem szerver-mentesség. A szerver oldalán a
"MUST implement" azt jelenti, hogy egy PRM nélküli szerver **nem konform** ezzel a
specifikációval; a spec nem ad neki "gracefully degradál" utat.

**Kritikus árnyalat**, amit a felhasználó feltevése ("Kötelező-e kiajánlani?") pontosításra
szorul: a fenti "MUST implement one of the following" azt jelenti, hogy **legalább egy**
felfedezési csatorna kötelező — egy szerver, amelyik PRM-et *csak* a well-known útvonalon
szolgál ki és sosem ad 401-et `WWW-Authenticate: resource_metadata`-val, ugyanúgy megfelel,
mint fordítva.

---

## Q3 — A `WWW-Authenticate` fejléc

### 3.1 Hitelesítetlen kérésre (401) — MCP-specifikus forma

**[T1]** `specification/2026-07-28/basic/authorization`, "Scope Selection Strategy" — konkrét
példa:

> ```
> HTTP/1.1 401 Unauthorized
> WWW-Authenticate: Bearer resource_metadata="https://mcp.example.com/.well-known/oauth-protected-resource",
>                          scope="files:read"
> ```

### 3.2 Alap-RFC-forrás — RFC 9728 5.1 szakasz

**[T1]** `rfc9728.txt`, 5.1 "WWW-Authenticate Response":

> "This specification introduces a new parameter in the WWW-Authenticate HTTP response header
> field to indicate the protected resource metadata URL:
>
> resource_metadata:
>    The URL of the protected resource metadata.
>
> The response below is an example of a WWW-Authenticate header that includes the resource
> identifier.
>
> HTTP/1.1 401 Unauthorized
> WWW-Authenticate: Bearer resource_metadata=
>   "https://resource.example.com/.well-known/oauth-protected-resource"
>
> The HTTP status code in the example response above is defined by [RFC6750]."

Fontos: maga az RFC 9728 ezt **"MAY"**-ként vezeti be ("A protected resource **MAY** use the
WWW-Authenticate HTTP response header field...", 5. szakasz eleje) — tehát az alap-RFC szintjén
a `WWW-Authenticate`-en keresztüli kiajánlás önmagában opcionális (alternatíva a well-known
URI-hoz képest). Az **MCP spec** teszi kötelezővé, hogy a szerver **legalább az egyik**
mechanizmust (a kettő közül) megvalósítsa — l. Q2.2.

### 3.3 Elégtelen jogosultság (403) — `insufficient_scope`

**[T1]** `specification/2026-07-28/basic/authorization`, "Runtime Insufficient Scope Errors":

> "When a client makes a request with an access token with insufficient scope during runtime
> operations, the server **SHOULD** respond with:
> * `HTTP 403 Forbidden` status code (per [RFC 6750 Section 3.1])
> * `WWW-Authenticate` header with the `Bearer` scheme and additional parameters:
>   * `error="insufficient_scope"` - indicating the specific type of authorization failure
>   * `scope="required_scope1 required_scope2"` - specifying the minimum scopes needed for the
>     operation
>   * `resource_metadata` - the URI of the Protected Resource Metadata document (for
>     consistency with 401 responses)
>   * `error_description` (optional) - human-readable description of the error"
>
> Példa:
> ```
> HTTP/1.1 403 Forbidden
> WWW-Authenticate: Bearer error="insufficient_scope",
>                          scope="files:write",
>                          resource_metadata="https://mcp.example.com/.well-known/oauth-protected-resource",
>                          error_description="File write permission required for this operation"
> ```

Ez **SHOULD**, nem MUST — az elégtelen scope esetén a 403+`WWW-Authenticate` válasz ajánlott,
de nem kőbe vésett kötelezettség (szemben a lenti hibakód-táblázattal, ami MUST).

### 3.4 Hibakód-táblázat (MUST szint)

**[T1]** ugyanaz az oldal, "Error Handling":

> "Servers **MUST** return appropriate HTTP status codes for authorization errors:
>
> | Status Code | Description  | Usage                                      |
> | ----------- | ------------ | ------------------------------------------ |
> | 401         | Unauthorized | Authorization required or token invalid    |
> | 403         | Forbidden    | Invalid scopes or insufficient permissions |
> | 400         | Bad Request  | Malformed authorization request            |"

### 3.5 Alap-OAuth 2.1 draft szöveg (a `WWW-Authenticate` mögötti kötelezettség)

**[T1]** `draft-ietf-oauth-v2-1-13`, 5.3.1 szakasz:

> "If the protected resource request does not include authentication credentials or does not
> contain an access token that enables access to the protected resource, the resource server
> **MUST** include the HTTP WWW-Authenticate response header field; it MAY include it in
> response to other conditions as well. ... All challenges for this token type MUST use the
> auth-scheme value Bearer."

Ez a mondat az, ami ténylegesen kötelezővé teszi magának a `WWW-Authenticate` fejlécnek a
jelenlétét egy hitelesítetlen (401) válaszban — az MCP spec ezt hivatkozással veszi át
("Access token handling ... **MUST** conform to the requirements defined in OAuth 2.1 Section 5").

### 3.6 Formátum-részletek, invalid_token példa (RFC 6750)

**[T1]** `rfc6750.txt`, 3. szakasz:

> "And in response to a protected resource request with an authentication attempt using an
> expired access token:
>
>   HTTP/1.1 401 Unauthorized
>   WWW-Authenticate: Bearer realm=\"example\",
>                     error=\"invalid_token\",
>                     error_description=\"The access token expired\""

---

## Q4 — Resource Indicators (RFC 8707)

### 4.1 Az alap-RFC szintje: MAY, nem MUST

**[T1]** `rfc8707.txt`, 2. szakasz:

> "In requests to the authorization server, a client **MAY** indicate the protected resource
> (a.k.a. resource server, application, API, etc.) to which it is requesting access by
> including the following parameter in the request.
>
> resource
>    Indicates the target service or resource to which access is being requested. Its value
>    **MUST** be an absolute URI... The URI **MUST NOT** include a fragment component."

Vagyis maga az RFC 8707 a `resource` paraméter *használatát* csak lehetőségként (MAY) definiálja
a kliens számára — de ha használják, a formátumára (abszolút URI, fragment nélkül) már MUST-
szabályokat ír elő.

### 4.2 Az MCP spec szigorítása: MUST

**[T1]** `specification/2026-07-28/basic/authorization`, "Resource Parameter Implementation":

> "MCP clients **MUST** implement Resource Indicators for OAuth 2.0 as defined in [RFC 8707] to
> explicitly specify the target resource for which the token is being requested. The `resource`
> parameter:
> 1. **MUST** be included in both authorization requests and token requests.
> 2. **MUST** identify the MCP server that the client intends to use the token with.
> 3. **MUST** use the canonical URI of the MCP server as defined in [RFC 8707 Section 2]."
>
> "MCP clients **MUST** send this parameter regardless of whether authorization servers
> support it."

Tehát az MCP spec az alap-RFC opcionális mezőjét **kliensoldali kötelezettséggé (MUST)**
emeli — ez az egyik legfontosabb "MCP szigorítja az alap-RFC-t" eset egész témában.

### 4.3 Miért kell — a veszély, ha kihagyják

**[T1]** `specification/2026-07-28/basic/authorization/security-considerations`, "Token
Audience Binding and Validation":

> "[RFC 8707] Resource Indicators provide critical security benefits by binding tokens to their
> intended audiences **when the Authorization Server supports the capability**. ... MCP
> servers **MUST** validate that tokens presented to them were specifically issued for their
> use."

**[T1]** ugyanaz az oldal, "Access Token Privilege Restriction" zárómondata:

> "MCP clients **MUST** implement and use the `resource` parameter as defined in [RFC 8707 -
> Resource Indicators for OAuth 2.0] to explicitly specify the target resource for which the
> token is being requested. This requirement aligns with the recommendation in [RFC 9728
> Section 7.4]. This ensures that access tokens are bound to their intended resources and
> **cannot be misused across different services**."

**[T1]** alap-RFC 8707 indoklása (`rfc8707.txt`, Bevezető):

> "To prevent misuse, several important security assumptions must hold, one of which is that an
> access token must only be valid for use at a specific protected resource and for a specific
> scope of access. ... When the authorization server is informed of the resource that will
> process the access token, it can restrict the intended audience of that token to the given
> resource such that the token cannot be used successfully at other resources."

**A veszély kihagyás esetén** (levezetve a fentiekből, nem szó szerinti idézet): `resource`
paraméter nélkül az AS nem tudja audience-hez kötni a kiadott tokent egy adott MCP szerverhez;
ha a klienst egyszerre több AS/erőforrás használatára veszik rá (vagy egy rosszindulatú MCP
szerver visszaküldi a nála látott tokent), a token — audience-kötés hiányában — más
szolgáltatásoknál is felhasználhatóvá válhat. Ez pontosan az, amit a "Token Passthrough" és
"Confused Deputy" szakaszok (l. Q6–Q7) tovább részleteznek.

---

## Q5 — Token-validáció: mit KELL ellenőriznie a szervernek

### 5.1 Amit a spec explicit MUST-ként kimond

**[T1]** `specification/2026-07-28/basic/authorization`, "Token Handling":

> "MCP servers, acting in their role as an OAuth 2.1 resource server, **MUST** validate access
> tokens as described in [OAuth 2.1 Section 5.2]. MCP servers **MUST** validate that access
> tokens were issued specifically for them as the intended audience, according to [RFC 8707
> Section 2]. If validation fails, servers **MUST** respond according to [OAuth 2.1 Section
> 5.3] error handling requirements. Invalid or expired tokens **MUST** receive a HTTP 401
> response."
>
> "MCP clients **MUST NOT** send tokens to the MCP server other than ones issued by the MCP
> server's authorization server."
>
> "MCP servers **MUST** only accept tokens that are valid for use with their own resources."
>
> "MCP servers **MUST NOT** accept or transit any other tokens."

**[T1]** `security-considerations` oldal, "Access Token Privilege Restriction":

> "MCP servers **MUST** validate access tokens before processing the request, ensuring the
> access token is issued specifically for the MCP server, and take all necessary steps to
> ensure no data is returned to unauthorized parties."
>
> "A MCP server **MUST** follow the guidelines in [OAuth 2.1 - Section 5.2] to validate inbound
> tokens."
>
> "MCP servers **MUST** only accept tokens specifically intended for themselves and **MUST**
> reject tokens that do not include them in the audience claim or otherwise verify that they
> are the intended recipient of the token."

### 5.2 Az OAuth 2.1 hivatkozott alapszövege (5.2 szakasz — ez az, amit a fentiek hivatkoznak)

**[T1]** `draft-ietf-oauth-v2-1-13`, 5.2 "Access Token Validation":

> "After receiving the access token, the resource server **MUST** check that the access token
> is not yet expired, is authorized to access the requested resource, was issued with the
> appropriate scope, and meets other policy requirements of the resource server to access the
> protected resource."

**Fontos pontosítás a felhasználó feltevéséhez képest:** a kérdés úgy volt megfogalmazva, hogy
"aud, iss, exp, aláírás, scope" — a spec-szöveg **nem sorolja fel név szerint** ezt a négyes
listát explicit MUST-tételként. Amit ténylegesen, szó szerint előír:
- **lejárat (exp)** — igen, explicit: "not yet expired" (OAuth 2.1 5.2) + "Invalid or expired
  tokens MUST receive a HTTP 401 response" (MCP spec).
- **audience (aud)** — igen, explicit és kétszer is kimondva MCP-specifikusan ("MUST validate
  that access tokens were issued specifically for them as the intended audience").
- **scope** — igen, explicit: "was issued with the appropriate scope" (OAuth 2.1 5.2).
- **kibocsátó (iss) és aláírás (signature)** — a token *saját* `iss`/aláírás-ellenőrzését a
  vizsgált oldalak **nem mondják ki külön, tételes MUST-ként** a *token* szintjén. Az `iss`
  ellenőrzés, amit a spec ténylegesen és részletesen tárgyal, az **authorization response**
  (az OAuth `iss` paramétere, RFC 9207) validálására vonatkozik, nem magára az access tokenre —
  ez más réteg (l. `authz.md` "Authorization Response Validation" szakasza, amelyet fentebb már
  idéztünk). A JWT-alapú token aláírás-ellenőrzését az OAuth 2.1 5.2 csak közvetve, a
  "meets other policy requirements" és a hivatkozott [RFC9068] (JWT Profile for Access Tokens)
  említésén keresztül fedi le, saját maga nem ír elő explicit aláírás-ellenőrzési MUST-ot — ez
  a implementáció-specifikus tokenformátum (referencia vs. self-encoded JWT) kérdése, amit a
  spec nyitva hagy: "Access tokens generally fall into two categories: reference tokens or
  self-encoded tokens." (OAuth 2.1, 5.2).

**Gap-jelölés:** ez azt jelenti, hogy a "mit KELL ellenőriznie" kérdésre a pontos, tételes
válasz **exp + aud + scope explicit MUST**, míg **iss/aláírás ellenőrzés implementáció-függő**
(a válaszottt token-formától — self-encoded JWT esetén ez szükségszerű, reference token esetén
az AS introspection-je végzi el). L. `gaps.md`.

### 5.3 Mi történik, ha a token nem ennek a szervernek szól

**[T1]** `security-considerations` oldal, "Confused Deputy Problem" szakasz zárása:

> "If the MCP server makes requests to upstream APIs, it may act as an OAuth client to them.
> The access token used at the upstream API is a separate token, issued by the upstream
> authorization server. The MCP server **MUST NOT** pass through the token it received from
> the MCP client."

**[T1]** `security_best_practices` (tutorial), "Token Passthrough" → "Mitigation":

> "MCP servers **MUST NOT** accept any tokens that were not explicitly issued for the MCP
> server."

Azaz: ha a bejövő token nem az adott MCP szervernek szól (audience mismatch), a szervernek
**el kell utasítania** — nem próbálhatja meg "átengedni" vagy továbbküldeni upstream felé.
A konkrét HTTP-válasz erre az esetre a fenti "Invalid or expired tokens MUST receive a HTTP 401
response" (audience-mismatch tokent a spec gyakorlatilag érvénytelen tokenként kezeli).

---

## Q6 — Token-átjátszás (token passthrough) — tiltás és indoklás

### 6.1 A tiltás szó szerint

**[T1]** `security-considerations` oldal:

> "MCP servers **MUST NOT** accept or transit any other tokens." *(basic/authorization oldal)*

> "If the MCP server makes requests to upstream APIs, it may act as an OAuth client to them.
> The access token used at the upstream API is a separate token, issued by the upstream
> authorization server. The MCP server **MUST NOT** pass through the token it received from
> the MCP client." *(security-considerations oldal, Confused Deputy Problem alatt)*

**[T1]** `security_best_practices` (tutorial), "Token Passthrough" definíciója:

> "'Token passthrough' is an anti-pattern where an MCP server accepts tokens from an MCP
> client without validating that the tokens were properly issued *to the MCP server* and
> passes them through to the downstream API."
>
> "Token passthrough is explicitly forbidden in the [authorization specification] as it
> introduces a number of security risks..."
>
> "**Mitigation** — MCP servers **MUST NOT** accept any tokens that were not explicitly
> issued for the MCP server."

### 6.2 Miért tiltja — a spec saját maga sorolja fel az okokat

**[T1]** `security_best_practices`, "Risks" alszakasz (szó szerint, tömörítve a négy alcím
köré):

> "**Security Control Circumvention** — The MCP Server or downstream APIs might implement
> important security controls like rate limiting, request validation, or traffic monitoring,
> that depend on the token audience or other credential constraints. If clients can obtain and
> use tokens directly with the downstream APIs without the MCP server validating them properly
> ... they bypass these controls."
>
> "**Accountability and Audit Trail Issues** — The MCP Server will be unable to identify or
> distinguish between MCP Clients when clients are calling with an upstream-issued access
> token which may be opaque to the MCP Server. The downstream Resource Server's logs may show
> requests that appear to come from a different source with a different identity, rather than
> the MCP server that is actually forwarding the tokens. ... If the MCP Server passes tokens
> without validating their claims ... a malicious actor in possession of a stolen token can use
> the server as a proxy for data exfiltration."
>
> "**Trust Boundary Issues** — ... If the token is accepted by multiple services without
> proper validation, an attacker compromising one service can use the token to access other
> connected services."
>
> "**Future Compatibility Risk** — Even if an MCP Server starts as a \"pure proxy\" today, it
> might need to add security controls later. Starting with proper token audience separation
> makes it easier to evolve the security model."

Ez a négy indok maga a spec normatív indoklása — nem másodlagos értelmezés.

---

## Q7 — A "confused deputy" probléma

### 7.1 Mit ír le a spec pontosan

**[T1]** `security_best_practices`, "Confused Deputy Problem" bevezetője:

> "Attackers can exploit MCP proxy servers that connect to third-party APIs, creating
> \"[confused deputy]\" vulnerabilities. This attack allows malicious clients to obtain
> authorization codes without proper user consent by exploiting the combination of static
> client IDs, dynamic client registration, and consent cookies."

A spec pontosan definiálja a szerepeket ("MCP Proxy Server", "Third-Party Authorization
Server", "Third-Party API", "Static Client ID") és a sebezhető feltételeket:

> "This attack becomes possible when all of the following conditions are present:
> * MCP proxy server uses a **static client ID** with a third-party authorization server
> * MCP proxy server allows MCP clients to **dynamically register** (each getting their own
>   client_id)
> * The third-party authorization server sets a **consent cookie** after the first
>   authorization
> * MCP proxy server does not implement proper per-client consent before forwarding to
>   third-party authorization"

A támadási lánc 8 lépésben: egy támadó dinamikusan regisztrál egy kliens-ID-t saját
redirect_uri-jával, a sértett böngészőjében meglévő consent-cookie miatt a third-party AS
átugorja a hozzájárulási képernyőt, és az MCP-authorization-code a támadó szerverére kerül
átirányításra, amit a támadó tokenre vált be — a felhasználó explicit jóváhagyása nélkül.

### 7.2 Mit ír elő ellene

**[T1]** `security_best_practices`, "Mitigation":

> "To prevent confused deputy attacks, MCP proxy servers **MUST** implement per-client consent
> and proper security controls as detailed below."

Konkrét, tételes MUST-listák (szó szerint):

> "**Per-Client Consent Storage** — MCP proxy servers **MUST**:
> * Maintain a registry of approved `client_id` values per user
> * Check this registry **before** initiating the third-party authorization flow
> * Store consent decisions securely (server-side database, or server specific cookies)"
>
> "**Consent UI Requirements** — The MCP-level consent page **MUST**:
> * Clearly identify the requesting MCP client by name
> * Display the specific third-party API scopes being requested
> * Show the registered `redirect_uri` where tokens will be sent
> * Implement CSRF protection (e.g., state parameter, CSRF tokens)
> * Prevent iframing via `frame-ancestors` CSP directive or `X-Frame-Options: DENY` to prevent
>   clickjacking"
>
> "**Redirect URI Validation** — The MCP proxy server **MUST**:
> * Validate that the `redirect_uri` in authorization requests exactly matches the registered
>   URI
> * Reject requests if the `redirect_uri` has changed without re-registration
> * Use exact string matching (not pattern matching or wildcards)"

**[T1]** ugyanez tömörebben a normatív `security-considerations` oldalon:

> "MCP proxy servers using static client IDs **MUST** obtain user consent for each
> [dynamically registered client] before forwarding to third-party authorization servers
> (which may require additional consent)."

**Fontos hatókör-pontosítás:** a "confused deputy" fejezet kifejezetten a **proxy-mintára**
vonatkozik (MCP szerver → third-party API delegálás statikus kliens-ID-vel). Ha a rendszer
nem proxyz tovább third-party AS felé (azaz maga az MCP szerver az egyetlen erőforrás, saját
AS-szel vagy anélkül), ez a konkrét MUST-lista nem aktiválódik — de az általánosabb "MUST NOT
pass through the token" (Q6) attól függetlenül mindig érvényes.

---

## Q8 — Kliens-regisztráció: CIMD vs. DCR (2026-07-28)

**A másodlagos forrás állítása megerősítve: igen, a `2026-07-28`-ban a CIMD (Client ID
Metadata Documents) az elsődleges, ajánlott mechanizmus, a DCR pedig formálisan deprecated.**

### 8.1 A három regisztrációs mechanizmus és a prioritási sorrend

**[T1]** `specification/2026-07-28/basic/authorization/client-registration`:

> "MCP supports three client registration mechanisms. Choose based on your scenario:
> * **Client ID Metadata Documents**: When client and server have no prior relationship (most
>   common)
> * **Pre-registration**: When client and server have an existing relationship
> * **Dynamic Client Registration**: For backwards compatibility or specific requirements
>
> Clients supporting all options **SHOULD** use the following priority order:
> 1. Use pre-registered client information for the server if the client has it available
> 2. Use Client ID Metadata Documents if the Authorization Server indicates that it supports
>    them (via `client_id_metadata_document_supported` in OAuth Authorization Server Metadata)
> 3. Use Dynamic Client Registration as a fallback if the Authorization Server supports it (via
>    `registration_endpoint` in OAuth Authorization Server Metadata)
> 4. Prompt the user to enter the client information if no other option is available"

### 8.2 A DCR explicit deprecation-figyelmeztetése

**[T1]** ugyanaz az oldal, "Dynamic Client Registration" szakasz:

> "⚠️ Dynamic Client Registration is deprecated. New implementations should use [Client ID
> Metadata Documents] instead. This option remains available for backwards compatibility with
> authorization servers that do not support Client ID Metadata Documents."
>
> "MCP clients and authorization servers **MAY** support the OAuth 2.0 Dynamic Client
> Registration Protocol [RFC7591] to allow MCP clients to obtain OAuth client IDs without user
> interaction."

Vö. a fő `authorization` oldal Overview 3. pontjával:

> "Authorization servers and MCP clients **MAY** support the OAuth 2.0 Dynamic Client
> Registration Protocol ([RFC7591]). Note that [Dynamic Client Registration] is **deprecated**
> and retained for backwards compatibility with authorization servers that do not support
> Client ID Metadata Documents."

...szemben a CIMD-vel, ugyanott, 2. pont:

> "Authorization servers and MCP clients **SHOULD** support [OAuth Client ID Metadata
> Documents] ([draft-ietf-oauth-client-id-metadata-document-00])."

**Tehát MUST/SHOULD/MAY szinten:** CIMD = **SHOULD** támogatni; DCR = már csak **MAY**
(visszaminősítve a korábbi SHOULD-ról — l. 8.4 verzió-összevetés).

### 8.3 Hivatalos deprecation-bejegyzés

**[T1]** `specification/2026-07-28/deprecated` (Deprecated Features Registry), táblázatsor:

> "| [Dynamic Client Registration](.../client-registration#dynamic-client-registration) |
> [PR #2858] | `2026-07-28` | [Client ID Metadata Documents]
> (.../client-registration#client-id-metadata-documents) | First revision released on or
> after 2027-07-28 |"

Azaz a DCR hivatalosan **`2026-07-28`-tól deprecated**, migrációs útja explicit a CIMD, és a
protokoll saját feature-lifecycle szabálya szerint (min. 12 hónap) legkorábban a
**2027-07-28-at követő revízióban** válhat eltávolíthatóvá — vagyis 2026-07-28-ban a DCR **még
támogatott** (MAY szinten), csak nem ajánlott az új implementációknak.

### 8.4 Verzió-összevetés: mi volt a `2025-06-18`-ban

**[T1]** `specification/2025-06-18/basic/authorization` (nyers Markdown, letöltve
összehasonlításra):

> "2. Authorization servers and MCP clients **SHOULD** support the OAuth 2.0 Dynamic Client
> Registration Protocol..."

A 2025-06-18-as verzióban **nincs CIMD-említés egyáltalán** — a DCR ott még **SHOULD**-szinten
az elsődleges, ajánlott regisztrációs mechanizmus volt. A CIMD tehát **teljesen új elem a
2026-07-28-ban**, és a DCR pozíciója SHOULD → MAY-re gyengült, miközben formálisan deprecated
lett. **Ez pontosan az a változás, amit a feladat "másodlagos forrás" felvetése állított — a
elsődleges forrásból (a spec maga) most már közvetlenül igazolható.**

### 8.5 A CIMD lényege dióhéjban

**[T1]** `client-registration` oldal:

> "This approach enables clients to use HTTPS URLs as client identifiers, where the URL points
> to a JSON document containing client metadata. This addresses the common MCP scenario where
> servers and clients have no pre-existing relationship."
>
> "The `client_id` URL **MUST** use the \"https\" scheme and contain a path component... The
> metadata document **MUST** include at least the following properties: `client_id`,
> `client_name`, `redirect_uris`... Clients **MUST** ensure the `client_id` value in the
> metadata matches the document URL exactly."

Az authorization server oldali kötelezettségek közül:

> "**For Authorization Servers:**
> * **SHOULD** fetch metadata documents when encountering URL-formatted client_ids
> * **MUST** validate that the fetched document's `client_id` matches the URL exactly
> * **SHOULD** cache metadata respecting HTTP cache headers
> * **MUST** validate redirect URIs presented in an authorization request against those in the
>   metadata document
> * **MUST** validate the document structure is valid JSON and contains required fields"

---

## Q9 — A MINIMUM: mit KELL megvalósítania egy szervernek a szabványos hitelesítéshez

Csak **MUST**-szintű tételek, kizárólag a fenti idézetekből levezetve, `2026-07-28`-ra.
(Az **egész hitelesítési mechanizmus maga OPTIONAL** az MCP-ben — l. lent a záró
megjegyzést —, de *ha* egy szerver megvalósítja, az alábbiak mind MUST-kötelezettségek.)

1. **Szerepvállalás**: a szerver OAuth 2.1 *resource server*-ként jár el (nem authorization
   server-ként — az AS külön szerep, kívül eshet a szerveren).
2. **Protected Resource Metadata (RFC 9728) kiajánlása**, és ezen belül **legalább az egyik**
   felfedezési csatorna megvalósítása:
   - `WWW-Authenticate: Bearer resource_metadata="<URL>"` fejléc 401 válaszban, **vagy**
   - metaadat kiszolgálása a `/.well-known/oauth-protected-resource` (root vagy az MCP
     végpont útvonalára illesztett) URI-n.
   A metaadat dokumentumnak tartalmaznia kell az `authorization_servers` mezőt legalább egy
   AS-szel.
3. **401 válasz `WWW-Authenticate` fejléccel** minden olyan kérésre, amely nem tartalmaz
   érvényes, hozzáférést engedő access tokent (`Bearer` auth-scheme kötelező).
4. **Hibakód-státuszok betartása**: 401 = hitelesítés szükséges/érvénytelen token; 403 =
   érvénytelen/elégtelen scope; 400 = hibás kérés.
5. **Access token validáció** minden kérésen: nem járt-e le (exp), a kért erőforráshoz van-e
   jogosultsága, a megfelelő scope-pal lett-e kiadva ("not yet expired, is authorized to
   access the requested resource, was issued with the appropriate scope").
6. **Audience-kötés kikényszerítése**: a szerver **kizárólag** olyan tokent fogadhat el, amely
   kifejezetten neki lett kiállítva; minden más tokent **el kell utasítania** (nem csak
   figyelmen kívül hagynia — audience-mismatch esetén 401).
7. **Token-átjátszás tilalma**: ha a szerver upstream/harmadik fél API-t hív, ahhoz **saját,
   külön** tokent kell szereznie (mint OAuth kliens) — a klienstől kapott tokent **nem**
   küldheti tovább változatlanul.
8. **"Confused deputy" védelem**, *ha* a szerver proxyként statikus kliens-ID-vel harmadik fél
   AS felé fordul: per-kliens hozzájárulás-nyilvántartás, ellenőrzése minden továbbküldés
   előtt, pontos `redirect_uri` egyeztetés, biztonságos consent-cookie kezelés.
9. **`resource` paraméter (RFC 8707) elfogadása/figyelembevétele** az audience-ellenőrzés
   részeként (ez elsősorban kliensoldali MUST — a `resource` paramétert a kliensnek kell
   küldenie —, de a szerver validációja csak akkor működik helyesen, ha az AS ezt az
   audience-t ténylegesen bekötötte a tokenbe).
10. **HTTPS kényszerítés**: minden AS-végpont és redirect URI kizárólag HTTPS (vagy
    `localhost`) lehet.

**Záró megjegyzés a "minimum" kereteként:** a specifikáció explicit kimondja, hogy maga az
egész hitelesítési réteg **OPTIONAL az MCP implementációk számára**:

> "Authorization is **OPTIONAL** for MCP implementations. When supported: Implementations
> using an HTTP-based transport **SHOULD** conform to this specification." *(authorization
> oldal, "Protocol Requirements")*

Mivel a rendszer leírása szerint (00-plan.md) az MCP felület **kizárólag távoli, HTTP-n
kiszolgált**, és a jogosultság emberhez kötött — tehát hitelesítés szükséges —, ez esetben a
fenti "SHOULD conform to this specification" lép életbe: HTTP-transzport esetén a
specifikációnak való megfelelés **SHOULD**, nem MUST szintű kötelezettség magára a
"kövesd-e ezt a specifikációt" döntésre nézve — de **ha** a döntés a megfelelés mellett esik
(ami a jelen rendszer esetén az egyetlen ésszerű választás, mivel emberhez kötött
jogosultságot kell kikényszeríteni), onnantól a fenti 1–10. pontok mindegyike **MUST**-szintű,
nem választható.

---

## Mi az, amiben biztos vagyok / Mi az, amiben nem

**Biztos vagyok benne** (közvetlenül, szó szerint, elsődleges forrásból ellenőrizve):
- `2026-07-28` a jelenleg érvényes ("Current") MCP protokollverzió.
- MCP szerver = OAuth 2.1 resource server; az AS-szerep külön, opcionálisan egybevonható.
- PRM (RFC 9728) kiajánlása MUST, két elfogadott csatornával, amiből legalább egy kötelező.
- A `WWW-Authenticate: Bearer resource_metadata="..."` pontos formátuma 401-re, és az
  `error="insufficient_scope"` formátuma 403-ra — mindkettő szó szerint a spec példáiból.
- A `resource` paraméter RFC 8707-ben MAY, MCP-ben klienseknek MUST.
- Token passthrough explicit, kimondott tilalom, négy tételes indoklással.
- Confused deputy: pontos definíció, sebezhető feltételek négyes listája, és tételes MUST-
  védelmi lista — mind proxy-forgatókönyvre szabva.
- CIMD (2026-07-28, SHOULD) váltja a DCR-t (deprecated, MAY, migrációs határidő
  2027-07-28 után) — ez a másodlagos forrás állítását elsődleges forrásból megerősíti.

**Nem vagyok teljesen biztos / árnyalásra szorul:**
- A token-validáció "aud/iss/exp/aláírás/scope" négyes-ötös listája **nem szerepel így,
  tételesen** a spec szövegében — az exp/aud/scope explicit MUST, az iss/aláírás
  ellenőrzése implementáció-függő (token-formátumtól, self-encoded JWT vs. reference token).
  L. `gaps.md`.
- Az "MUST implement one of the following discovery mechanisms" pontosan mit jelent egy olyan
  szerverre nézve, amelyik **egyiket sem** valósítja meg — a spec ezt "nem konform"-ként
  kezeli implicit módon, de nincs egy külön "ha hiányzik, X hiba" normatív mondat rá; a
  kliensoldali válasz ("abort or use pre-configured values") csak a mermaid-diagram
  jegyzeteiben szerepel, nem a folyószövegben.
- Az OAuth 2.1 draft-verziószám következetlensége a security-considerations oldalon (`-13`
  a legtöbb helyen, `-14` a Refresh Tokens szakaszban) — valószínűleg redakciós hiba a
  hivatalos oldalon, nem tartalmi ellentmondás. L. `contradictions.md`.
