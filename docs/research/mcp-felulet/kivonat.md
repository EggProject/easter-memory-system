# KIVONAT — Az MCP felület kutatása

Készült a `.research/mcp-felulet/` mappa anyagából (00-plan.md, sq01–sq04). A dokumentum a
kutatás eredményeit foglalja össze; szintézist, ajánlást vagy döntést nem tartalmaz — azt a
vezető (Opus) írja külön. Tier-jelölés a forrásanyag definíciója szerint: **T1** = hivatalos
specifikáció/dokumentáció/SDK forráskód; **T2** = megbízható másodlagos forrás VAGY gyártó saját
termékéről szóló állítás (ide tartozik a gyártói önmérés is, még ha hivatalos blogon jelent is
meg); **T3** = fórum/vélemény/marketing; **T4** = preprint/önjelentett technikai/közösségi audit;
**T6** = általános fórum-/marketing-tartalom. Minden állításnál jelezve van, melyik MCP
specifikáció-verzióra vonatkozik.

---

## 1. Mire kerestünk választ

A kutatás tárgya egy tervezett rendszer MCP-felülete: markdown fájlokban tárolt memória/tudástár
három gyökér alatt (`projects/`, `knowledge/`, `personal/<email>/`), öt szállított, de bővíthető
kategóriával, amelyekhez egy-egy, a hívó agenshez kerülő prompt tartozik. A keresés hibrid (FTS5 +
beágyazás, helyezés-alapú egyesítés, kapu-mechanizmus). A jogosultság **projektenként, konkrét
emberekhez van rendelve** — amihez egy adott embernek nincs joga, az a rendszer szemszögéből nem
is létezik. A törlés **három állapotú** folyamat, minden állapotváltáshoz kötelező szöveges
indoklással. Az egész rendszer egy gépen, két konténerben, egyetlen szerverfolyamatként fut.

Az MCP felület — vagyis hogy pontosan milyen eszközöket lát a hívó agent, milyen paraméterekkel,
milyen válaszformátumban és milyen hibaüzenetekkel — ennek a rendszernek a szerződése a
külvilággal. A kutatás megindításakor ez a szerződés **teljesen hiányzott** a leírásból, miközben
több élő tervezési döntés (a kategóriadefiníció helye a sémában, hogy törlést és újraolvasást is
lehet-e MCP-n kérni, hogy a felület angol nyelvű legyen-e, hogy a csonka keresési válasz jelzése
hol álljon) már explicit rá hivatkozott, mintha létezne.

Négy alkérdést vizsgáltunk. **SQ-01**: mit tud és mit nem tud formálisan kifejezni egy MCP
eszközdefiníció a hivatalos specifikáció szerint — elnevezés, leírás, séma, strukturált kimenet,
hibamodell, annotációk, lapozás, eszköz vs. erőforrás vs. prompt. **SQ-02**: milyen
eszközfelületet használnak ténylegesen jól a nagy nyelvi modellek — mit mondanak erről a gyártói
(Anthropic, OpenAI) útmutatók és mérések a leírásokról, a paraméterezésről, az eszközök
darabolásáról és a modellnek szóló hibaüzenetekről. **SQ-03**: mit csinálnak a ma létező,
memória-jellegű MCP szerverek a gyakorlatban — milyen eszközöket adnak, milyen paraméterekkel, és
milyen hibákból mit tanultak. **SQ-04**: hogyan lehet egyáltalán tudni MCP-n keresztül, ki hívja a
szervert — mert a teljes tervezett jogosultsági modell ezen áll vagy bukik.

A kutatás egyik, önmagában is fontos felismerése, hogy az MCP specifikációnak a kutatás
megkezdése előtt hat héttel (2026-07-28-án) megjelent egy új, a kampány tervezésekor még nem
számított kiadása, amely gyökeresen átalakítja a protokoll több alapfogalmát: megszűnt a session
és az `initialize` handshake, átszámozódtak a hibakódok, megváltozott a listaváltozás-értesítés
mechanizmusa. Emiatt a kutatás minden pontnál külön jelzi, melyik verzióra vonatkozik egy-egy
állítás, és felhívja a figyelmet arra, hogy a gyakorlatban elérhető cikkek, SDK-k és
StackOverflow-válaszok többsége még a korábbi, session-alapú modellt írja le.

---

## 2. SQ-01 — A specifikáció

### Melyik verzió érvényes, és mi változott

A GitHub release-lista, a hivatalos specifikáció-oldal és a hivatalos bejelentő blogbejegyzés
(szerzők: David Soria Parra és Den Delimarsky, "Lead Maintainer"-ek) egybehangzóan megerősíti,
hogy a 2026-09-12-i mai állapot szerint a legfrissebb stabil MCP-specifikáció a **`2026-07-28`**
revízió. Ez a verzió a legfontosabb szerkezeti változásként eltávolította a session-koncepciót és
az `initialize`/`notifications/initialized` handshake-et:

> "1. Remove protocol-level sessions and the `Mcp-Session-Id` header from the Streamable HTTP
> transport. List endpoints (`tools/list`, `resources/list`, `prompts/list`) no longer vary
> per-connection. Servers that need cross-call state use explicit, server-minted handles passed
> as ordinary tool arguments (SEP-2567)."
>
> "2. Make MCP stateless: remove the `initialize`/`notifications/initialized` handshake. Every
> request now carries its protocol version and client capabilities in `_meta` ... Version
> mismatches return `UnsupportedProtocolVersionError` (SEP-2575)."
— modelcontextprotocol.io/specification/2026-07-28/changelog (T1)

Fontos korábbi mérföldkövek: a tool-annotációk (`readOnlyHint`, `destructiveHint`,
`idempotentHint`, `openWorldHint`) `2025-03-26`-ban jelentek meg; a `title` mező, a strukturált
kimenet (`outputSchema`/`structuredContent`) és a `resource_link` `2025-06-18`-ban; a `resultType`
mező, az MRTR-minta, a session/handshake eltávolítása és a `subscriptions/listen` `2026-07-28`-ban.

### Eszközdefiníció — mezők

A `Tool` interfész (2026-07-28 schema.ts, T1) alapja:

```typescript
export interface Tool extends BaseMetadata, Icons {
  description?: string;
  inputSchema: { $schema?: string; type: "object"; [key: string]: unknown };
  outputSchema?: { $schema?: string; [key: string]: unknown };
  annotations?: ToolAnnotations;
  _meta?: MetaObject;
}
```

Az eszköznévre (`name`) van SHOULD-szintű ajánlás — 1–128 karakter, csak ASCII betű/szám/`_`/`-`/
`.`, egyediség egy szerveren belül —, de ez **SHOULD, nem MUST**: a protokoll formálisan nem
kényszeríti ki. A `description` mezőre viszont **semmilyen hosszkorlát nincs** a specifikációban —
sem MUST, sem SHOULD szinten; a `tools` oldal és a `Tool` interfész teljes forráskód-kommentjének
átolvasása után sem került elő ilyen korlát (evidence of absence). A megjelenítési név
precedenciája (T1, `Tool` doksi-komment): "Display name precedence order is: `title`,
`annotations.title`, then `name`." Az `inputSchema`-nak `MUST` valid JSON Schema objektumnak
lennie, `type: "object"` gyökérrel; paraméter nélküli eszközhöz a spec kifejezetten a
`{"type": "object", "additionalProperties": false}` formát ajánlja "Recommended" jelzéssel.

A támogatandó JSON Schema dialektus `2026-07-28`-ban bővült: a korábbi verziókhoz képest most
bármilyen 2020-12-es kulcsszó megengedett a séma gyökerén (`oneOf`, `anyOf`, `allOf`, `if/then/
else`, `$ref`, `$defs` stb.), de két új, kifejezetten biztonsági korlátozás is bekerült: `$ref`
hálózati URI-ra **MUST NOT** automatikusan feloldódjon, és a kompozíciós kulcsszavakra (SHOULD)
ésszerű korlátokat (mélység, subschema-szám, időbudget) kell alkalmazni, nehogy a séma
szolgáltatásmegtagadási vektorként működjön a validátor ellen.

### Strukturált kimenet

A `structuredContent` mezőt `2025-06-18`-ban vezették be, és `2025-11-25`-ig kizárólag JSON
objektum lehetett. `2026-07-28`-tól **bármilyen** JSON érték lehet (objektum, tömb, string, szám,
boolean, null) — ez a changelog szerint explicit bővítés (SEP-2106), nem ellentmondás a korábbi
állapottal. Ha van `outputSchema`, a szervernek **MUST** azt betartania; a kliens oldali
validáció csak SHOULD. Visszafelé-kompatibilitásból egy strukturált választ adó eszköznek SHOULD
(nem MUST) szöveges `TextContent`-ben is visszaadnia a szerializált JSON-t.

### A hibamodell — a legfontosabb pont

A `2026-07-28` `tools` doksi-oldal (T1) két, élesen elkülönített hibacsatornát különböztet meg:

> "Tools use two error reporting mechanisms:
> 1. **Protocol Errors** indicate issues with the request structure itself that models are less
> likely to be able to fix: Unknown tool; Malformed requests...; Server errors. They are returned
> as standard JSON-RPC errors...
> 2. **Tool Execution Errors** contain actionable feedback that language models can use to
> self-correct and retry with adjusted parameters: API failures; Input validation errors...;
> Business logic errors. They are reported in tool results with `isError: true`...
> Clients **MAY** provide protocol errors to language models... Clients **SHOULD** provide tool
> execution errors to language models to enable self-correction."
— modelcontextprotocol.io/specification/2026-07-28/server/tools (T1)

A normatív erősség kulcskülönbsége: a *tool execution error* modellhez juttatása **SHOULD**, a
*protokollhiba* modellhez juttatása csak **MAY** — vagyis a specifikáció szerint egy
protokollszintű JSON-RPC hiba nem feltétlenül jut el a modellhez egyáltalán, a kliens dönti el; a
tool-szintű hiba viszont SHOULD-szinten eljut. A séma forráskódja (`CallToolResult`, `isError`
mező kommentje) még élesebben fogalmaz:

> "Any errors that originate from the tool SHOULD be reported inside the result object, with
> `isError` set to true, _not_ as an MCP protocol-level error response. Otherwise, the LLM would
> not be able to see that an error occurred and self-correct. However, any errors in _finding_
> the tool, an error indicating that the server does not support tool calls, or any other
> exceptional conditions, should be reported as an MCP error response."
— schema.ts, 2026-07-28 (T1)

A döntési szabály tehát: ha az eszköz *létezik és lefutott*, de az eszköz logikája szerint hiba
történt (üzleti szabály sértés, validációs hiba) → `isError: true` a `tools/call` eredményében.
Ha az eszköz *megtalálásával/hívásával* van baj (nem létező eszköznév, malformed request) → MCP
protokollhiba (JSON-RPC `error` mező). A kutatás saját értelmezése szerint (nem spec-idézet) a
tervezett rendszer üzleti szabály jellegű elutasításai (pl. "nincs jogod törölni ezt a projektet",
"az indoklás kötelező paraméter és hiányzik") a `tool execution error` csatornába illenek, mert
csak így garantált, hogy a hívó modell lássa és korrigálja magát.

Az erőforrás-nem-található hibakód `2025-11-25`-ig `-32002` volt, `2026-07-28`-tól `-32602`
(Invalid Params) — a kliensnek SHOULD még elfogadnia a `-32002`-t is visszafelé kompatibilitásból,
de a szervernek MUST NOT azt kibocsátania. Az MCP-specifikus hibakódok is átszámozódtak:
`HeaderMismatch`, `MissingRequiredClientCapability`, `UnsupportedProtocolVersion` a `-3200x`
tartományból a `-3202x` tartományba kerültek, egy új, explicit particionálási politikával
(`-32000`–`-32019` legacy, `-32020`–`-32099` MCP-fenntartott).

### Annotációk

A `ToolAnnotations` interfész négy hint-je (`readOnlyHint` alap `false`, `destructiveHint` alap
**`true`**, `idempotentHint` alap `false`, `openWorldHint` alap `true`) mind opcionális. A
specifikáció kétszer is, forráskód-kommentben és doksi-oldalon egyaránt figyelmeztet:

> "NOTE: all properties in `ToolAnnotations` are **hints**. They are not guaranteed to provide a
> faithful description of tool behavior (including descriptive properties like `title`). Clients
> should never make tool use decisions based on `ToolAnnotations` received from untrusted
> servers."
— schema.ts, 2026-07-28 (T1)

> "For trust & safety and security, clients **MUST** consider tool annotations to be untrusted
> unless they come from trusted servers."
— specification/2026-07-28 (T1, azonos szöveg 2025-11-25-ben is)

Az `openWorldHint` definíciója maga is egy memória-szervert hoz példának "closed world"-re: "the
world of a web search tool is open, whereas that of a memory tool is not."

### Eszköz vs. erőforrás vs. prompt

A három primitíva vezérlési modellje (T1, mindhárom saját doksi-oldaláról szó szerint):

> "Tools in MCP are designed to be **model-controlled**..." /
> "Resources in MCP are designed to be **application-driven**..." /
> "Prompts are designed to be **user-controlled**, meaning they are exposed from servers to
> clients with the intention of the user being able to explicitly select them for use."

A `resource_link` (bevezetve `2025-06-18`-ban) egy könnyűsúlyú, csak-referencia visszatérési elem:
a tool nem tölti be a teljes tartalmat a válaszba, hanem egy URI-t ad vissza, amit a kliens külön
`resources/read`-del tölthet le vagy amire feliratkozhat — "Resource links returned by tools are
not guaranteed to appear in the results of a `resources/list` request."

### Lapozás és nagy válaszok

A lapozás opak, cursor-alapú: "Page size is determined by the server, and clients **MUST NOT**
assume a fixed page size." A cursort a kliens nem értelmezheti, egy üres string is érvényes
cursor. **Válaszméret-korlátra vagy "túl nagy válasz" eljárásra a specifikáció sehol nem tér ki**
— ez valódi hiány, nem csak keresési kudarc (a `tools`, `resources`, `basic`, `pagination` oldalak
teljes átolvasása után sem került elő ilyen szabály). Az egyetlen közvetve kapcsolódó mező a
`Resource.size` (opcionális, informatív, nem korlát).

### Listaváltozás — gyökeresen megváltozott mechanizmus `2026-07-28`-ban

`2025-11-25`-ig és korábban a `listChanged: true` képesség deklarálása után a kliens
**automatikusan** megkapta a `notifications/tools/list_changed` üzenetet. `2026-07-28`-tól a
kliensnek **explicit fel kell iratkoznia** egy `subscriptions/listen` streamre
`toolsListChanged: true` paraméterrel, különben **sosem kap** értesítést, még akkor sem, ha a
szerver deklarálta a képességet. Ez a projekt szempontjából releváns, mert ha a kategóriák
futásidőben szerkeszthetők, egy egyszerű, rövid életű kliens sosem fog `list_changed` értesítést
kapni, hacsak nem nyit explicit streamet. Emellett `2026-07-28`-ban új, kötelező `ttlMs` és
`cacheScope` mező jelent meg minden lista-válaszban, és új követelmény, hogy a szerver
determinisztikus sorrendben adja vissza az eszközlistát (a prompt-cache találati arány miatt).

### Elnevezési konvenciók

Az eszköznév-egyediség csak egy szerveren belülre skálázott. `2026-07-28`-ban új, dedikált
figyelmeztetés jelent meg a több-szerveres aggregálásra: "Tool name uniqueness is scoped to a
single server... clients or proxies... **SHOULD** implement a disambiguation strategy such as
prefixing tool names with a server identifier," és külön: "The server `name`... is not guaranteed
to be unique across servers and **SHOULD NOT** be relied upon for disambiguation." Kötelező
névtér-szintaxist a spec nem ír elő.

---

## 3. SQ-02 — Modellbarát eszközfelület

Fő T1 források: Anthropic hivatalos engineering blog ("Writing effective tools for AI agents",
2025-09-11) és a Claude API hivatalos dokumentáció (define-tools, handle-tool-calls,
tool-search-tool, strict-tool-use); OpenAI hivatalos function-calling útmutató. T2 forrásként a
gyártói önmérések (Advanced Tool Use, Code execution with MCP blog).

### Leírás és paraméterek

Az Anthropic hivatalos ajánlása szerint a leírás a legfontosabb tényező:

> "Provide extremely detailed descriptions. This is by far the most important factor in tool
> performance... Aim for at least 3–4 sentences for each tool description, more if the tool is
> complex."
— platform.claude.com/docs, Define tools (T1)

A paramétereket egyértelműen kell elnevezni: "instead of a parameter named `user`, try a
parameter named `user_id`" (T1). Az OpenAI ugyanerre az elvre jut függetlenül: "Write clear and
detailed function names, parameter descriptions, and instructions" / "Apply the 'intern test'" /
"Use enums and object structure preventing invalid states" (T1). Példa-mezőkre (Anthropic
`input_examples`) mért token-költség: **~20–50 token** egyszerű, **~100–200 token** komplex,
beágyazott objektumnál (T1, dokumentált tényadat). Mért hatás (T2, gyártói önmérés): "Tool use
accuracy improved from **72% to 90%** on complex parameter handling in internal testing" a
tool-use példák bevezetése után.

### Eszközök darabolása

Mindkét gyártó a konszolidációt ajánlja: "Consolidate related operations into fewer tools. Rather
than creating a separate tool for every action..., group them into a single tool with an action
parameter" (Anthropic, T1); "Combine functions always called in sequence" / "Start with fewer than
**20** initially available functions" (OpenAI, T1). Ez **tervezési ajánlás**, nem kontrollált
kísérlet eredménye — egyik forrás sem közöl A/B-tesztet egy nagy multi-action tool és több kicsi
összevetésére.

Konkrét küszöbszám a pontosságromlásra: "Claude's ability to pick the right tool degrades once you
exceed **30–50 available tools**" (T1 dokumentáció, T2 mögöttes mérés), és "Use tool search
when... You have **10 or more tools** available." Mért javulás sok eszköz esetén a Tool Search
Tool bevezetése után (T2, Anthropic saját mérés): "Opus 4 improved from **49% to 74%**; Opus 4.5
improved from **79.5% to 88.1%**." Egy öt-szerveres beállítás (GitHub, Slack, Sentry, Grafana,
Splunk) kb. **55 000 token**-t fogyaszt beszélgetés-kezdés előtt, egyes esetekben akár **134 000
tokent** optimalizálás előtt — a Tool Search ezt kb. **85%-kal** csökkenti. Egy független (nem
gyártói), nem lektorált Meta-preprint (T4, arxiv.org/html/2605.24660v1) más kérdést mér — nem
azt, hány eszközt tervezzünk, hanem hány *jelöltet* mutassunk egy keresési lépésben —, ezért ennek
számai (pl. "K=7.4" 90,3%-os lefedettséggel) nem hasonlíthatók közvetlenül a fenti tervezési
küszöbökhöz.

### Mit adjon vissza egy eszköz

Tervezési elv: "tool implementations should take care to return only high signal information back
to agents... eschew low-level technical identifiers (for example: uuid, 256px_image_url,
mime_type)" (T1). Dokumentált minta a válasz méretének szabályozására a `response_format` enum
(`"concise"`/`"detailed"`), mért példával: "detailed tool responses may consume **206 tokens**
while concise responses use only **72 tokens**" (egyetlen Slack-thread-példa, nem
benchmark-átlag). Claude Code termékbeli konfigurációs tény: "tool responses are restricted to
**25 000 tokens** by default." Alternatív, radikálisabb architektúra (T2, kód-végrehajtás a nyers
tool-hívás helyett): "the traditional approach consumed **150 000 tokens** versus **2 000 tokens**
with code execution — a time and cost saving of **98.7%**."

### Hibaüzenetek a modellnek — kiemelt pont

A központi ajánlás: "**Write instructive error messages.** Instead of generic errors like
'failed', include what went wrong and what Claude should try next (for example, 'Rate limit
exceeded. Retry after 60 seconds.'). This gives Claude the context it needs to recover or adapt
without guessing." (platform.claude.com/docs, T1) — vagyis a hivatalos válasz szerint **nem elég**
egy puszta hibakód vagy opak hibaüzenet; kell mellé, mi történt és mit próbáljon a modell
legközelebb. Konkrét JSON-példák is szerepelnek a dokumentációban (hiányzó paraméter esetén:
`"Error: Missing required 'location' parameter"`; végrehajtási hiba esetén:
`"ConnectionError: the weather service API is not available (HTTP 500)"`).

A dokumentált (nem mért) viselkedés a helyreállásra: "**If a tool request is invalid or missing
parameters, Claude will retry 2-3 times with corrections before apologizing to the user.**" (T1) —
ez leíró jellegű állítás, nem specifikációs garancia arra, hogy ez hardkódolt limit lenne.
**Fontos hiány**: egyetlen forrás sem közöl kontrollált mérést arról, hogy a hibaüzenet konkrét
megfogalmazása (kód+javaslat vs. csak kód) milyen arányban javítja a helyreállási sikerarányt,
vagy mi vezet statisztikailag végtelen ciklushoz — ez kvalitatív ajánlás marad, nem mért adat.

### Kötelező paraméterek

A "strict tool use" / grammar-constrained sampling (Anthropic `strict: true`, OpenAI hasonló
`strict` mező) a mintavételezést a séma szerint érvényes tokenekre korlátozza, így a kötelező mező
strukturálisan nem maradhat ki: "Without strict mode, Claude might return incompatible types...
or **omit required fields**... With strict: true, the response always contains passengers: 2."
(T1) A kutatás saját elemzése (nem forrás-állítás): ez a mező *jelenlétét és típusát* garantálja,
nem a *tartalom releváns minőségét* — egy kötelező indoklás-mező sémaszinten kikényszeríthető, de
hogy a modell releváns szöveget ír-e bele, arra nincs mechanizmus vagy mérés.

### Megerősítés és visszafordíthatatlan műveletek

Az MCP-annotációk (destructiveHint stb.) csak javaslatok — "Clients should never make tool use
decisions based on ToolAnnotations received from untrusted servers" — vagyis a protokoll maga nem
kényszerít ki védelmet veszélyes műveletekre; a tényleges védelmet a kliensnek vagy a szerver saját
üzleti logikájának kell megvalósítania. A gyakorlatban létező, de nem protokoll-előírt minta a
Supabase MCP server (T4) háromszintű kockázati kategorizálása (`safe`/`write`/`destructive`) egy
külön `confirm_destructive_operation` eszközzel és `live_dangerously` mód-kapcsolóval — ez a
legkonkrétabb, kétlépéses megerősítési minta, amit a kutatás talált.

### Idempotencia

Az `idempotentHint` alapértelmezése **`false`** — a protokoll alapból NEM feltételezi az
idempotenciát. A spec nem ír elő idempotencia-kulcs/deduplikáció mechanizmust a protokoll szintjén;
ez teljesen a szerver implementáció felelőssége, és nincs adat arra, milyen gyakorlatban valósítják
meg ezt a létező MCP-szerverek.

---

## 4. SQ-03 — Létező memória-MCP szerverek

### A hivatalos referencia-szerver (`modelcontextprotocol/servers/src/memory`)

Egyetlen gráf-adatmodell: `entities` (`name`, `entityType`, `observations: string[]`) és
`relations` (`from`, `to`, `relationType`) — nincs timestamp, nincs forrás/eredet mező, az entitás
neve az elsődleges kulcs, minden egy `memory.jsonl` fájlban él. **Kilenc eszköz**:
`create_entities`, `create_relations`, `add_observations`, `delete_entities`,
`delete_observations`, `delete_relations`, `read_graph`, `search_nodes`, `open_nodes`. A keresés
a forráskód szerint szó szerint:

```
// Very basic search function
async searchNodes(query: string): Promise<KnowledgeGraph> {
  ... e.name.toLowerCase().includes(query.toLowerCase()) ||
      e.entityType.toLowerCase().includes(query.toLowerCase()) ||
      e.observations.some(o => o.toLowerCase().includes(query.toLowerCase()))
}
```

Vagyis kis-nagybetű-független substring-keresés, se FTS, se embedding, se relevancia-pontszám,
nincs lapozás, nincs csonkítás-jelzés — a maintainerek maguk minősítik "very basic"-nek a
kódkommentben. Az `entityType` szabad string, nincs zárt kategória-enum. Minden törlés azonnali és
visszavonhatatlan; módosítás csak `add_observations`/`delete_observations` páron keresztül. A
duplikátumkezelés csendben, exact-string/hármas-egyezés alapon szűri a pontos duplikátumokat.
**Nincs felhasználó-fogalom**: egyetlen `MEMORY_FILE_PATH` = egyetlen megosztott gráf az egész
szerverfolyamatra; a README ajánlott rendszerprompt-konvenciója ("assume you are interacting with
default_user") promptmérnöki trükk, nem hozzáférés-vezérlés.

**Konkurencia — konkrét forráskód-szintű tanulság.** A kódkomment a `#1819` hibajegyre hivatkozva:
"Without this, concurrent tool calls (e.g. multiple mutations dispatched from one LLM turn) each
independently load the graph, mutate their own copy, and write it back — so whichever write lands
last silently overwrites the other's changes, and interleaved writes to the same file can corrupt
it outright." A jelenlegi kód ezt egy `mutationQueue`/`withLock` mechanizmussal és atomi
temp-fájl+rename írással oldja meg. Egy még nyitott hibajegy (`#4117`) hét további hiányt sorol
fel: nem biztonságos alapértelmezett tárolási hely, nincs audit trail a törlésekhez, a törlő
eszközök megerősítés nélkül futnak, nincs méret-kvóta, nincs titok-redakció, nincs
namespace-elkülönítés.

### Más memória-szerverek — összehasonlító táblázat

| Szerver | Eszközök (fő lista) | Fő paraméterek / adatmodell | Keresés típusa | Törlés |
|---|---|---|---|---|
| **Hivatalos referencia** | `create_entities`, `create_relations`, `add_observations`, `delete_entities`, `delete_observations`, `delete_relations`, `read_graph`, `search_nodes`, `open_nodes` | `Entity{name,entityType,observations[]}`, `Relation{from,to,relationType}` | Kis-nagybetű-független substring, nincs rangsorolás | Közvetlen, kaszkádolt, visszavonhatatlan |
| **mem0** | `add_memory`, `update_memory`, `delete_memory`, `delete_all_memories`, `search_memories`, `get_memories`, `get_memory`, `delete_entities`, `list_entities`, `list_events`, `get_event_status` (11) | `MemoryItem{id,memory,hash,metadata,score,created_at,updated_at}` + `user_id/agent_id/run_id/actor_id` | Hibrid: szemantika + BM25 + entitás-boost, `score` visszaadva | Közvetlen, kaszkádolt (`delete_entities`) |
| **Graphiti/Zep** | `add_memory`, `add_triplet`, `search_nodes`, `search_memory_facts`, `summarize_saga`, `build_communities`, `get_episode_entities`, `delete_entity_edge`, `delete_episode`, `get_entity_edge`, `get_episodes`, `clear_graph`, `get_status` (13) | `EntityNode`, `EntityEdge{valid_at,invalid_at,expired_at}`, `EpisodicNode`, `group_id` | Hibrid BM25+koszinusz, RRF/MMR/cross-encoder rerank | Közvetlen + temporális "szuperszedálás" (érvénytelenítés, nem törlés) |
| **Letta/MemGPT** | `core_memory_append`, `core_memory_replace`, `memory_replace`, `memory_insert`, `memory_rethink`, `memory` (str_replace/insert/delete/rename), `archival_memory_insert`, `archival_memory_search`, `conversation_search` | Blokk: `label,value,description,limit`; Archival: `content,tags` | Szemantikus (archival), hibrid (conversation) | `core_memory_replace("")`; git-alapú history/visszaállítás |
| **basic-memory** | `write_note`, `read_note`, `edit_note`, `move_note`, `delete_note`, `read_content`, `view_note`, `search_notes`, `build_context`, `recent_activity`, `list_memory_projects`, `create_memory_project`, `delete_project`, `list_directory`, `schema_validate`, `schema_infer`, `schema_diff`, ChatGPT-kompatibilis `search`/`fetch` (~20) | Markdown + YAML frontmatter; `note_type` (szabad), `categories`, `entity_types` | `search_type`: text/title/permalink/vector/semantic/hybrid; lapozás; `min_similarity` | `delete_note`/`delete_project` (alapból fájlmegtartással) |
| **OpenMemory** (megszűnőben) | `add_memories`, `search_memory`, `list_memories`, `delete_all_memories` (4) | Nem részletezett (forrás nem adta meg) | Nem részletezett | Csak "mindent töröl" |
| **memento-mcp** (`gannonh`) | Hivatalos referencia API + `get_relation`, `update_relation`, `semantic_search`, `get_entity_history`, `get_relation_history`, `get_graph_at_time`, `get_decayed_graph` | Reláció: `strength`,`confidence` (0.0–1.0), időbélyeges history | Szemantikus + hibrid, konfidencia-lecsengés (felezési idő) | Közvetlen, teljes verziótörténettel visszakövethető |
| **memento** (`iAchilles`) | Hivatalos referencia API + `set_importance` | `entityType` szabad, `importance`: critical/important/normal/temporary/deprecated (zárt enum) | FTS5 + `sqlite-vec` szemantikus (BGE-M3, offline) | Megegyezik a hivatalossal; opcionális írás-esemény JSONL napló |

Ehhez kapcsolódóan: a **mem0 Claude Code plugin** dokumentációja (T2, tömörítve kapott oldal)
szerint egy migráció során "Nine read/write tools replaced by the single read-only
`search_memories` tool" — vagyis a mem0 platform mellett a Claude Code-specifikus rétegben is
drasztikusan csökkentették az eszközök számát, egyetlen csak-olvasó eszközre, ahol az írás
automatikus háttérfolyamattá vált.

### Jogosultság-összefoglaló

| Szerver | Van-e felhasználó-fogalom? | Milyen szinten? |
|---|---|---|
| Hivatalos referencia | Nincs | Egyetlen megosztott fájl, "default_user" csak promptkonvenció |
| mem0 | Van | `user_id`/`agent_id`/`run_id`/`actor_id` — scoping, nem szerepkör-alapú |
| Graphiti | Van | `group_id` namespace — scoping, nem szerepkör-alapú |
| Letta | Nincs (memória-eszközök szintjén) | Agent-központú, nem felhasználó-központú |
| basic-memory | **Van, RBAC** | Öt szerepkör (Viewer/Editor/User Admin/Admin/Owner), csapat/workspace szinten |
| OpenMemory | Nincs | Egyfelhasználós, helyi célra tervezve |

A legtöbb vizsgált rendszer **azonosító-alapú hatókör-szűrést** (scoping) valósít meg, ami nem
azonos a valódi jogosultságkezeléssel (ki férhet hozzá kinek az adatához, milyen műveletre). Az
egyetlen explicit szerepkör-modell a basic-memory csapat/felhő-funkciója. Egyik vizsgált szerver
sem old meg **projektenkénti, emberekhez rendelt** jogosultságot.

### Amit tanultak

1. **Konkurens írás → fájlkorrupció** (hivatalos referencia, T1): egy LLM egy körben több
   eszközhívást indíthat egyszerre, ami versenyhelyzetet és fájlkorrupciót okoz, ha a szerver nem
   zárolja a mutációkat; a jelenlegi kód explicit mutáció-sorosító zárral és atomi írással oldja
   meg.
2. **A hivatalos szerver keresése saját bevallás szerint is "very basic"** — nincs
   relevancia-rangsorolás, nincs csonkítás-jelzés.
3. **mem0: a dokumentált "ellentmondás-feloldás" nem létezik a gyakorlatban** — lásd a
   6. fejezetben (Ellentmondások).
4. **Graphiti: a konfliktus detektálása és a hívó felé jelzése két külön dolog** — a
   `resolve_edge_contradictions()` automatikusan lezárja a régi tényt, de ez belső mechanizmus, a
   hívó nem kap explicit "ütközés volt" jelzést.
5. **A hivatalos szerver hiányosságai köré kiegészítő gazdaság szerveződött** — több közösségi
   fork (`memento-mcp`, `iAchilles/memento`) pontosan a hivatalos szerver API-ját tartja meg, csak
   a keresést és a perzisztenciát cseréli le — közvetett bizonyíték arra, hogy éles használatban a
   keresési minőség és a konkurenciakezelés a két fő szűk keresztmetszet.
6. **OpenMemory négy eszközből állt, és megszűnt** — a README explicit "sunsetting"
   figyelmeztetést tartalmaz, a pontos indoklást (miért éppen ezt a minimalista terméket) nem
   sikerült feltárni.
7. **mem0 Claude Code plugin: kilenc eszközből egy lett** (fentebb részletezve) — közvetlen,
   bár tömörítve kapott (T2) precedens az eszközszám-csökkentés mellett.

---

## 5. SQ-04 — Azonosítás és jogosultság

### Verzió-térkép az auth-fejezetre

| Verzió | Auth-fejezet státusza |
|---|---|
| 2024-11-05 | Nincs auth-fejezet. |
| 2025-03-26 | Első authorization-fejezet: OAuth 2.1-alapú, OPTIONAL. |
| 2025-06-18 | RFC 8707 kliens oldalon kötelező; MCP szerver = OAuth Resource Server; RFC 9728 megjelenik. |
| 2025-11-25 | Session-kezelés (`Mcp-Session-Id`) még protokollszintű; Security Best Practices bővül (Session Hijacking, Token Passthrough, Confused Deputy). |
| 2026-07-28 (jelenlegi) | Statelessé válik, session megszűnik; RFC 9728 MUST mindkét oldalon; CIMD váltja a Dynamic Client Registration-t; új védekezések (mix-up attack, state handle hijacking). |

A `2024-11-05` verzióban szó szerint: "Authentication and authorization are not currently part of
the core MCP specification... Clients and servers **MAY** negotiate their own custom
authentication and authorization strategies." (T1) A `2025-03-26`-tól máig érvényes alapelv:
"Authorization is **OPTIONAL** for MCP implementations." A `2026-07-28`-as gyakorlati tutorial ezt
így árnyalja: "While authorization for MCP servers is **optional**, it is strongly recommended
when: Your server accesses user-specific data... You need to audit who performed which actions...
You're building for enterprise environments with strict access controls..." (T1) — vagyis a
protokoll semmit nem kényszerít ki; hogy tudjuk-e, ki hív, kizárólag az adott implementáció
döntése.

### OAuth-minta

Az MCP szerver mindig OAuth 2.1 Resource Server, sosem Authorization Server: "An *MCP client*
acts as an [OAuth 2.1 client], making protected resource requests on behalf of a resource owner.
The *authorization server* is responsible for interacting with the user..." (2026-07-28, T1, elv
2025-03-26 óta változatlan). Az RFC 8707 (Resource Indicators) `2025-06-18`-ban még csak
kliensoldali kötelezettség, `2026-07-28`-tól mindkét irányban MUST. Az RFC 9728 (Protected
Resource Metadata) `2025-06-18`-ban jelenik meg, `2026-07-28`-ban MUST mindkét oldalon — ez a
mechanizmus mondja meg a kliensnek egy `401` válasz és `WWW-Authenticate` fejléc útján, melyik
authorization szerverhez kell fordulnia. A Dynamic Client Registration (RFC 7591) `2026-07-28`-ra
**deprecated**lett: "Dynamic Client Registration is deprecated and retained for backwards
compatibility with authorization servers that do not support Client ID Metadata Documents." (T1)
Helyette a Client ID Metadata Document (CIMD) minta ajánlott.

### Confused deputy

A specifikáció explicit figyelmeztet (azonos szöveggel `2025-11-25` és `2026-07-28`-ban):
"Attackers can exploit MCP proxy servers that connect to third-party APIs, creating 'confused
deputy' vulnerabilities. This attack allows malicious clients to obtain authorization codes
without proper user consent by exploiting the combination of static client IDs, dynamic client
registration, and consent cookies." (T1) A védekezés MUST-szinten kötelező: "To prevent confused
deputy attacks, MCP proxy servers **MUST** implement per-client consent and proper security
controls" — konkrét listákkal (per-client consent registry, redirect URI exact-match validáció,
kriptográfiailag biztos, csak consent után eltárolt state paraméter). Ez a hiba-osztály közvetlen
tükörképe a projekt "ki hívja" kérdésének: egy proxy/közvetítő szerep (mint egy agent) más entitás
nevében jár el anélkül, hogy azt valóban ellenőrizné.

### Token-átjátszás

Explicit tiltás, azonos szöveggel `2025-11-25` és `2026-07-28`-ban: "'Token passthrough' is an
anti-pattern where an MCP server accepts tokens from an MCP client without validating that the
tokens were properly issued *to the MCP server* and passes them through to the downstream API."
A kockázat egyik indoka szó szerint a projekt problémájára mutat: "*The MCP Server will be unable
to identify or distinguish between MCP Clients* when clients are calling with an upstream-issued
access token which may be opaque to the MCP Server." A kemény előírás: "MCP servers **MUST NOT**
accept any tokens that were not explicitly issued for the MCP server." / "MCP clients **MUST NOT**
send tokens to the MCP server other than ones issued by the MCP server's authorization server."

### stdio vs. HTTP

**stdio (helyi) transport — nincs protokollszintű ember-azonosítás.** A spec `2025-03-26` óta
változatlanul kimondja: "Implementations using an STDIO transport **SHOULD NOT** follow this
specification, and instead retrieve credentials from the environment." A `2026-07-28`-as
gyakorlati megfogalmazás: "Because a STDIO-built MCP server runs locally, it has access to a range
of flexible options when it comes to acquiring user credentials that may or may not rely on
in-browser authentication and authorization flows." A gyakorlatban ez azt jelenti, hogy a
"hitelesítés" a folyamatindítás előtti rétegre tolódik (környezeti változók, konfigurációs fájlban
tárolt kulcsok) — a Security Best Practices dokumentum implicit egyetlen emberre optimalizál
(a kliens ellenőrzi, hogy a helyi felhasználó indította-e a folyamatot, nem azt, hogy több embert
megkülönböztessen). Nyitva maradt kérdés: a `2026-07-28`-as stdio-oldal új szövege megemlíti, hogy
a `_meta.io.modelcontextprotocol/*` mezőkben "optional client identity" utazhat, de nem
tisztázott, hogy ez a kliens-szoftvert vagy egy emberi felhasználót azonosít.

**HTTP (távoli) transport — session-alapú, majd state-handle-alapú modell.** `2025-11-25`-ig és
korábban a szerver `MCP-Session-Id` fejlécet rendelhetett a kapcsolathoz. A spec explicit
figyelmeztet a session hijackingre, és kőkeményen tiltja, hogy a session maga hitelesítésre
szolgáljon: "MCP servers that implement authorization **MUST** verify all inbound requests. MCP
Servers **MUST NOT** use sessions for authentication." / "MCP servers **SHOULD** bind session IDs
to user-specific information... Use a key format like `<user_id>:<session_id>`." `2026-07-28`-tól
a session megszűnt, helyette "state handle" jött, ugyanazzal a logikával: "MCP servers **MUST NOT**
treat possession of a state handle as authentication... MCP servers **SHOULD** bind handles
server-side to the authenticated user... where the user ID is derived from the verified token
rather than supplied by the client."

### Kinek a jogaival fut az agent

A spec két OAuth grant-típust különböztet meg (`2025-03-26` óta): "Authorization Code: useful when
the client is acting **on behalf of a (human) end user**... Client Credentials: the client is
another application (not a human)... No need to impersonate the end user." A legnagyobb valós,
sokfelhasználós MCP-kliens (Anthropic/Claude) gyakorlata egyértelműen az első mintát követi
kizárólagosan: "A pure machine-to-machine `client_credentials` grant — where a server-to-server
token is issued with no user in the loop — is **not supported**. Every connection requires user
consent." (claude.com/docs/connectors/building/authentication, T1) Az `oauth_anthropic_creds`
mechanizmusban a kliens-azonosító lehet közös/szervezetszintű, de a kiadott token — és ezáltal az,
hogy "ki hívott" — mindig egyedi, egy adott ember explicit consentjéhez kötött. Kivétel a
`static_headers` mód, ahol "The credential is shared by the organization rather than pasted per
user" — ez a projekt céljaira nézve explicit anti-minta, mert nem különbözteti meg az egyes
embereket. A GitHub hivatalos MCP szervere (T1, de a fetch összefoglalva adta vissza) hasonló
mintát követ: a GitHub OAuth token maga az azonosító, a jogosultság a token scope-jaiból
következik, és a `--oauth-scopes` szűkítése egyszerre szűkíti a jogot és az elérhető eszközlistát.

A gyakorlati minta (Keycloak + TS/Python/C# munkapélda alapján, T1): a hívó OAuth access tokent
küld → a szerver validálja (aláírás vagy introspekció) és ellenőrzi az `aud` claimet → a hívó
ember azonosítója a token `sub` claimjéből (esetleg `preferred_username`/email) származik → a
jogosultság a scope-okból és/vagy egy, a `sub`-hoz kötött, a szerver saját adatbázisában tárolt
szerepkörből következik — ez utóbbi (scope→jogosultság leképezés) explicit az MCP specifikáción
kívül esik ("organization specific").

---

## 6. Ellentmondások

### 6.1 Eltérő eszközszám-küszöb: Anthropic vs. OpenAI (SQ-02)

- Anthropic (T1 dok., T2 mögöttes mérés): "Claude's ability to pick the right tool degrades once
  you exceed **30–50 available tools**."
- OpenAI (T1): "Start with **fewer than 20** initially available functions."

Nem feloldható a rendelkezésre álló forrásokból, melyik szám "helyes" — mindkettő saját gyártó
saját modelljére és mérési módszertanára vonatkozik, közös benchmark nélkül. Az OpenAI száma
konzervatív kiindulási ajánlás, az Anthropic száma megfigyelt romlási pont — más dolgot mérnek, de
ha valaki csak az egyiket idézi abszolút határként, az félrevezető. Minősítés: **Vitatott**.

### 6.2 Annotációk mint "csak javaslat" vs. gyakorlati kemény blokkolás (SQ-02)

A specifikáció szerint az annotációk (pl. `destructiveHint`) csak hint-ek, amiket a kliens
figyelmen kívül hagyhat. Ezzel szemben a Codex CLI (T3/T4) leírása szerint `destructiveHint ==
true` esetén a kliens *mindig* jóváhagyást kér, és konfigurációval teljesen le is tiltható ("hard
block, not a prompt"). Nem logikai ellentmondás (a spec nem tiltja a szigorú kliens-viselkedést),
de fontos árnyalás: a specifikáció megengedő jellege és egy konkrét kliens szigorú gyakorlata két
külön dolog — nem feltételezhető, hogy minden kliens így viselkedik.

### 6.3 mem0 dokumentáció vs. tényleges viselkedés (SQ-03)

- **Állítás A** (mem0 dokumentáció, idézve a `mem0ai/mem0#4896` hibajegyben): "Latest truth wins
  when contradictions detected."
- **Állítás B** (tényleges kód/viselkedés, T1, ugyanaz a hibajegy): a `2026 áprilisi` "v3"
  ADD-only architektúra ezt nem teszi meg — két egymásnak ellentmondó tény mindkettő külön ADD
  eseményként kerül be, felülírás vagy összevonás nélkül.

A hibajegy bejelentője ezt explicit "documentation mismatch"-nek nevezi; a közösségi válasz szerint
ez szándékos tervezési döntésnek tűnik (a v2-es ADD/UPDATE/DELETE/NONE logikát tudatosan
egyszerűsítették v3-ban), de a dokumentációt nem frissítették ezzel összhangban.

Kapcsolódó, magában is ellentmondásos részlet: egy `#4787` discussion-válasz (T2/T3, közösségi,
nem jelölt mem0-alkalmazott) szerint "New memories are still emitted as ADD, but they can include
`linked_memory_ids` pointing to related old memories" — ezt a `#4896` hibajegy reprodukciós
lépései nem említik. Nem eldönthető, hogy ez időbeli egymásutániság (funkció később került be) vagy
csak bizonyos hívási módokra vonatkozik — **Alacsony bizonyosság**.

### 6.4 "Optional" a specifikációban vs. "gyakorlatilag elvárt" (SQ-04)

Nem klasszikus forrás-ellentmondás, hanem tervezési feszültség: a spec minden verzióban kimondja,
hogy a hitelesítés OPTIONAL, miközben ugyanaz a dokumentumkör "strongly recommended"-nek nevezi,
mihelyt a szerver "user-specific data"-t kezel vagy "audit who performed which actions" szükséges —
ami pontosan a projekt esete. A protokoll semlegesnek szánja magát, a döntés súlyát teljes
egészében az implementátorra hárítja.

### 6.5 A Client Credentials grant sorsa — nyitott kérdés (SQ-04)

- `2025-03-26`: a spec kifejezetten leírja mindkét OAuth grant-típust.
- Stack Overflow blog (T2, 2026-01-21): "The client credentials grant was mentioned in the
  2025-03-26 version of MCP, **was removed** and now is **coming back**."
- A `2026-07-28`-as authorization spec lekért részében nem szerepelt explicit "OAuth Grant Types"
  alfejezet.

Nem eldönthető ebben a körben, hogy a szakasz tényleg kikerült-e és még nem tért vissza, egy nem
lekérdezett aloldalra költözött-e, vagy a fetch tömörítve hagyta ki. **Ellenőrizetlen.**

### 6.6 stdio `_meta` "optional client identity" vs. "nincs azonosítás stdio-n" (SQ-04)

A spec `2025-03-26` óta következetesen azt állítja, hogy stdio-n nincs protokollszintű
azonosítás, a hitelesítést a környezetre kell bízni. Ugyanakkor a `2026-07-28`-as stdio-oldal új
szövege megemlíti, hogy a `_meta.io.modelcontextprotocol/*` mezőkben "optional client identity"
utazhat. Formálisan nem zárják ki egymást (az egyik hitelesítésről, a másik metaadatban utazó
identitás-adatról szól), de gyakorlati feszültséget hordoz: ha egy kliens ezt a mezőt
"ember-azonosítóként" kezdi használni, az pontosan az a "bízz a hívó fél önkéntes állításában"
minta lenne, amit a token-passthrough és confused-deputy szakaszok tokenekre nézve kifejezetten
tiltanak — csak itt nincs is token, aminek érvényességét ellenőrizni lehetne.

### 6.7 Nem-ellentmondások, amiket a kutatás explicit kizárt

A hibaüzenet-tervezésre nem talált ellentmondást a kutatás: az Anthropic ajánlása
("write instructive error messages... what Claude should try next") és az MCP hibamodell
(isError csatorna) kiegészítik, nem cáfolják egymást. Az SQ-01-ben talált eltérések
(`structuredContent` típusbővítés, hibakód-átszámozás, `listChanged` mechanizmusváltás) **nem
valódi ellentmondások**, hanem dokumentált, egymást követő verziók közti evolúciók — ugyanaz a
hivatalos changelog nevezi meg mindkét (régi és új) állapotot.

---

## 7. Hiányok

### Valódi hiányok a specifikációban (SQ-01)

- Nincs hosszkorlát a `description` mezőre (van a `name`-re, SHOULD 1–128 karakter).
- Nincs válaszméret-korlát vagy "túl nagy válasz" eljárás — a lapozás az egyetlen mechanizmus; egy
  célzott WebSearch (`site:modelcontextprotocol.io response size limit`) is nulla releváns
  hivatalos találatot hozott.
- Nincs kötelező névtér-szintaxis több szerver aggregálására, csak SHOULD-szintű ajánlás.
- Nem ellenőrzött: a gyakorlati SDK/kliens-adoptáció állapota `2026-07-28`-ra — nem világos, hogy
  a ma elterjedt MCP-kliensek ténylegesen ezt a verziót beszélik-e, vagy még a
  `2025-06-18`/`2025-11-25` handshake-et várják.

### Amire nincs mért adat (SQ-02)

- Nincs kontrollált mérés a hibaüzenet-stílus és a helyreállási sikerarány kapcsolatáról — csak
  kvalitatív ajánlás és egy dokumentált (nem statisztikai) viselkedési tény (2–3 újrapróbálkozás).
- Nincs mért adat arra, milyen arányban hagy ki a modell kötelező paramétert N kötelező paraméter
  esetén (a Berkeley Function-Calling Leaderboard vélhetően tartalmazna ilyen bontást, de ezt a
  kör nem nyitotta meg mélyen).
- Nincs mért/dokumentált gyakorlat az MCP-szerverek tényleges idempotencia-megvalósítására.
- Nincs kontrollált kísérlet "egy nagy multi-action tool vs. sok kicsi tool" pontosság-hatásáról; az
  egyetlen talált kvantitatív tanulmány (Meta, T4) más kérdést (retrieval-time jelöltlista-méret)
  mér.
- Magyar nyelvi ellenőrzés lefutott, de kizárólag általános, marketing-jellegű MCP-bemutató
  tartalmat hozott (Microsoft Learn HU, sidekickautomations.hu, devertix.hu stb.) — ez megerősíti,
  hogy nincs releváns magyar elsődleges forrás ehhez az alkérdéshez.

### Amit nem sikerült feltárni (SQ-03)

- Az OpenMemory pontos megszüntetési indoklása — a `#4923` hibajegy tartalmát nem sikerült
  kinyerni, csak a címét.
- A mem0 Claude Code plugin "9 eszköz → 1 `search_memories`" migrációjának pontos indoklása és
  dátuma.
- A Letta pontos forráskódja — két közvetlen `raw.githubusercontent.com` próbálkozás 404-et adott;
  az adatok egy közösségi audit (T2) forráskód-hivatkozásaira támaszkodnak, nem magára a kódra.
- A basic-memory tényleges forráskódja — csak a hivatalos dokumentációs oldalt (T2) néztük meg.
- Egy ígéretes "claude-code-memory → MemoryGraph" migrációs dokumentum (`gregorydickson/
  memory-graph`) robots.txt miatt nem volt elérhető.
- A `carsteneu/ai-memory-comparison/evidence/` mappa teljes tartalma (GitHub fa-nézet robots.txt,
  API 403) — lehet további releváns fájl, amit nem találtunk meg.
- Nyelvi lefedettség: kizárólag angol nyelvű keresés zajlott (indokolt, nemzetközi nyílt
  forráskódú közösségről van szó).

### Amit nem sikerült lezárni (SQ-04)

- A `2025-06-18`-as Security Best Practices oldal pontos szövegét nem töltöttük le közvetlenül,
  csak a `2025-11-25`/`2026-07-28` szöveg alapján rekonstruáltuk (valószínű, de nem garantált
  azonosság).
- A Client Credentials grant jelenlegi spec-béli státusza (ld. 6.5. pont).
- A stdio `_meta` "optional client identity" pontos jelentése (ld. 6.6. pont).
- Csak két konkrét, mélyen vizsgált valós implementáció (GitHub, Anthropic/Claude) — a szélesebb
  ökoszisztéma (Sentry, Notion, Linear, Stripe MCP szerverei, OpenAI/Google/Microsoft
  kliens-infrastruktúrái) nem lett feltérképezve.
- A "Claude Managed Agents" pontos identitás-modellje (emberhez kötött-e végig, vagy van benne
  szolgáltatás-fiók elem) nem derült ki.
- A "MCP Authorization Extensions" repository (github.com/modelcontextprotocol/ext-auth) és a
  SEP-1359 GitHub issue tartalmát nem sikerült megnézni.

### Ahol a lekérés nem szó szerinti tartalmat adott vissza

Egyik kutatási körben sem fordult elő a legsúlyosabb hiba (egy keresőmotor AI-összefoglalója egy
valódi oldal helyett) — ezt minden SQ explicit ellenőrizte és rögzítette nemleges eredményként.
Előfordult azonban **tömörített/renderelt** tartalom több helyen, amit a forrásanyag maga is
külön megjelöl, és ami miatt bizonyos idézetek nem tekinthetők bájt szerint szó szerintinek:

- **SQ-02**: az Anthropic fő blogbejegyzésben a "rossz" vs. "jó" hibaüzenet-példapár **képként**
  szerepel, a WebFetch ezt nem tudta szöveggé alakítani (csak jelezte a kép létét). Az OpenAI
  function-calling guide első lekérése egy táblázatos összefoglalót adott a kért verbatim markdown
  helyett.
- **SQ-03**: minden GitHub issue/discussion "idézete" valójában a WebFetch kis modellje által
  **tömörített** olvasat, nem bájt szerinti másolat — konkrétan a `modelcontextprotocol/
  servers#4117` és a `mem0ai/mem0/discussions/4787` esetében jelezve, hogy esetleges további
  kommentek kimaradhattak.
- **SQ-04**: a `github.com/github/github-mcp-server/docs/oauth-login.md` és a
  `blog.modelcontextprotocol.io/posts/2026-07-28/` lekérése is **összefoglalást**, nem nyers
  oldalszöveget adott vissza — a konkrét idézőjelbe tett mondatok valószínűleg pontosak, de nem
  lettek keresztellenőrizve a nyers HTML/markdown-nal.

---

## 8. Minden meglátogatott link

Az alábbi lista a négy `links.md` uniója. "Felhasznált" = idézve/állításalapként szerepel a
megfelelő `megallapitasok.md`-ben; "nem nyitva/lead" = csak találatként jelent meg, nem lett
feldolgozva.

### SQ-01 — a specifikáció (mind `modelcontextprotocol.io`/hivatalos GitHub, hacsak nincs jelölve)

- github.com/modelcontextprotocol/modelcontextprotocol/releases — T1, felhasznált — release-lista, `2026-07-28` = Latest Stable.
- modelcontextprotocol.io/specification/2026-07-28 — T1, felhasznált — jelenlegi spec főoldala.
- blog.modelcontextprotocol.io/posts/2026-07-28/ — T1, felhasznált (SQ-04-ben is, ott részben összefoglalva kapva) — hivatalos bejelentés.
- modelcontextprotocol.io/specification/2026-07-28/server/tools — T1, felhasznált — eszközdefiníció, hibamodell, listaváltozás fő forrása.
- modelcontextprotocol.io/specification/2025-11-25/server/tools — T1, felhasznált — összehasonlításhoz.
- raw.githubusercontent.com/.../schema/2026-07-28/schema.ts — T1, felhasznált — `Tool`/`ToolAnnotations`/`CallToolResult` stb. interfészek.
- modelcontextprotocol.io/specification/2026-07-28/server/resources — T1, felhasznált — resource_link, annotációk, hibakód-változás.
- modelcontextprotocol.io/specification/2026-07-28/server/prompts — T1, felhasznált — "user-controlled" definíció.
- modelcontextprotocol.io/specification/2026-07-28/server/utilities/pagination — T1, felhasznált — lapozási modell.
- modelcontextprotocol.io/specification/2026-07-28/basic — T1, felhasznált — hibakódok, `_meta`, JSON Schema szabályok.
- modelcontextprotocol.io/specification/2026-07-28/architecture — T1, felhasznált — host/client/server modell.
- modelcontextprotocol.io/specification/2026-07-28/basic/patterns/subscriptions — T1, felhasznált — `subscriptions/listen`.
- modelcontextprotocol.io/specification/2026-07-28/changelog — T1, felhasznált — verzió-evolúció teljes listája.
- modelcontextprotocol.io/specification/2025-06-18/changelog — T1, felhasznált — strukturált kimenet/resource_link bevezetése.
- modelcontextprotocol.io/specification/2025-03-26/changelog — T1, felhasznált — tool annotációk bevezetése.
- en.wikipedia.org/wiki/Model_Context_Protocol — T3/T5, nem forrásként — landscape-feltérképezés.
- hidekazu-konishi.com/entry/mcp_specification_version_timeline.html — másodlagos, nem citálva.
- ts.sdk.modelcontextprotocol.io/v2/servers/tools.html — SDK-doksi, nem citálva (a kérdés a spec-re vonatkozott).
- workos.com/blog/mcp-2025-11-25-spec-update — T3, nem citálva, landscape-jelzés.

### SQ-02 — modellbarát eszközfelület

- anthropic.com/engineering/writing-tools-for-agents — T1, felhasznált — fő Anthropic engineering blog (2025-09-11).
- platform.claude.com/docs/.../define-tools — T1, felhasznált — leírás-ajánlások.
- platform.claude.com/docs/.../handle-tool-calls — T1, felhasznált — is_error, hibaüzenet-minták, retry-viselkedés.
- platform.claude.com/docs/.../tool-search-tool — T1, felhasznált — 30–50 eszköz küszöb.
- platform.claude.com/docs/.../strict-tool-use — T1, felhasznált — grammar-constrained sampling.
- anthropic.com/engineering/advanced-tool-use — T2, felhasznált — Tool Search Tool mért hatásai (49%→74% stb.).
- anthropic.com/engineering/code-execution-with-mcp — T2, felhasznált — 150k→2k token példa.
- modelcontextprotocol.io/specification/2025-06-18/server/tools — T1, felhasznált — hibamodell (ez a `2025-06-18` verziójú oldal, külön az SQ-01 `2026-07-28`-as verziójától).
- raw.githubusercontent.com/.../schema/2025-06-18/schema.ts — T1, felhasznált — `ToolAnnotations` (2025-06-18-as verzió).
- modelcontextprotocol.io/specification/2025-06-18/client/elicitation — T1, felhasznált — elicitation nem szenzitív megerősítésre szánva.
- developers.openai.com/api/docs/guides/function-calling — T1, felhasznált — OpenAI hivatalos ajánlások.
- arxiv.org/html/2605.24660v1 — T4 (Meta preprint), felhasznált — "How Many Tools Should an LLM Agent See?"
- arxiv.org/html/2601.15812v2 — T4, felhasznált korlátozott relevanciával — ErrorMap/ErrorAtlas, nem tool-specifikus.
- codex.danielvaughan.com/.../mcp-tool-annotations-risk-vocabulary-codex-cli/ — T3/T4, felhasznált — Codex CLI jóváhagyási logika.
- stacklok.com/blog/tool-annotations-are-becoming-the-risk-vocabulary... — T3/T4, felhasznált — "hints, not contracts".
- github.com/alexander-zuev/supabase-mcp-server (README) — T4, felhasznált — kétlépéses megerősítési minta.
- dev.to/thedailyagent/mcp-tool-overload... — T6, nem nyitva.
- tianpan.co/blog/2026-04-19-over-tooled-agent-problem — T6, nem nyitva.
- achan2013.medium.com/how-many-tools... — T6, nem nyitva.
- arxiv.org/abs/2305.15334 (Gorilla, NeurIPS 2024) — T2 peer-reviewed, nem dolgozva fel részletesen.
- huggingface.co/datasets/gorilla-llm/Berkeley-Function-Calling-Leaderboard — T1/T4 határeset, nem nyitva.
- gorilla.cs.berkeley.edu/leaderboard.html — T1, nem nyitva.
- glama.ai/mcp/servers/mako10k/mcp-confirm — T4/T6, nem nyitva.
- glama.ai/mcp/servers/@portel-dev/ncp/.../confirm-before-run.md — T4, nem nyitva.
- dzone.com/articles/mcp-elicitation-human-in-the-loop-for-mcp-servers — T3, nem nyitva.
- learn.microsoft.com/hu-hu, sidekickautomations.hu, devertix.hu, cloudmentor.hu, minner.hu — T3/T6, magyar nyelvi ellenőrzés, általános marketing-tartalom, nem releváns a részletekhez.

### SQ-03 — létező memória-MCP szerverek

- raw.githubusercontent.com/modelcontextprotocol/servers/main/src/memory/index.ts — T1, verbatim, felhasznált — teljes forráskód.
- raw.githubusercontent.com/modelcontextprotocol/servers/main/src/memory/README.md — T1, verbatim, felhasznált.
- github.com/modelcontextprotocol/servers/issues/1819 — T1, tömörített, felhasznált — race condition.
- github.com/modelcontextprotocol/servers/issues/4117 — T1, tömörített, felhasznált — hét hiányosság.
- github.com/modelcontextprotocol/servers/issues/2577, 2578, 2579 — nem nyitva, feltehetően duplikátumok.
- github.com/modelcontextprotocol/servers/tree/main/src/memory — T1, nem közvetlenül fetchelve.
- npmjs.com/package/@modelcontextprotocol/server-memory — T2, nem fetchelve.
- docs.mem0.ai/platform/mem0-mcp — T2, felhasznált — 11 eszköz listája.
- docs.mem0.ai/integrations/claude-code — T2, tömörített, felhasznált — "9 eszköz → 1 search_memories".
- docs.mem0.ai/v0x/core-concepts/memory-operations/add — T2, a kért tartalom nem volt a lapon.
- github.com/mem0ai/mem0/discussions/4787 — T1/T2, tömörített, felhasznált.
- github.com/mem0ai/mem0/issues/4896 — T1, tömörített, felhasznált — dokumentáció vs. viselkedés ellentmondás.
- github.com/mem0ai/mem0/issues/4923 — T1, csak cím, tartalom nem elérhető.
- github.com/mem0ai/mem0/blob/main/openmemory/README.md — T1, tömörített, felhasznált — sunsetting figyelmeztetés.
- mem0.ai/blog/introducing-openmemory-mcp — T2, felhasznált — 4 eszköz.
- mem0.ai/blog/how-to-make-your-clients-more-context-aware-with-openmemory-mcp — T2, nem fetchelve.
- github.com/pinkpixel-dev/mem0-mcp — T2, nem fetchelve.
- github.com/simon9679/mem-audit — T2, nem fetchelve.
- github.com/mem0ai/mem0-mcp — T2, nem fetchelve.
- raw.githubusercontent.com/getzep/graphiti/main/mcp_server/README.md — T1, verbatim, felhasznált — 13 eszköz.
- raw.githubusercontent.com/carsteneu/ai-memory-comparison/main/evidence/graphiti.md — T2, verbatim (forráskód-hivatkozásokkal), felhasznált.
- help.getzep.com/graphiti/getting-started/mcp-server — T2, nem fetchelve.
- blog.getzep.com/cursor-adding-memory-with-graphiti-mcp/ — T2, nem fetchelve.
- getzep.com/product/knowledge-graph-mcp/ — T2, nem fetchelve.
- docs.letta.com/guides/legacy/memgpt_agents_legacy — T2, redirect, nem releváns tartalom.
- docs.letta.com/guides/core-concepts/memory/memory-blocks — T2, a kért paraméterek nem szerepeltek.
- docs.letta.com/guides/core-concepts/memory/archival-memory — T2, verbatim, felhasznált.
- docs.letta.com/guides/ade/core-memory/ — T2, nem releváns tartalom.
- raw.githubusercontent.com/carsteneu/ai-memory-comparison/main/evidence/letta.md — T2, verbatim (forráskód-hivatkozásokkal), felhasznált.
- raw.githubusercontent.com/letta-ai/letta/main/letta/functions/function_sets/base.py — 404, nem sikerült.
- docs.basicmemory.com/reference/mcp-tools-reference — T2, verbatim, felhasznált — ~20 eszköz teljes paramétertáblázata.
- docs.basicmemory.com/teams/members-and-roles — T2, verbatim, felhasznált — öt szerepkör.
- github.com/basicmachines-co/basic-memory — nem fetchelve, csak találat.
- github.com/basicmachines-co/basic-memory-skills — nem fetchelve.
- apidog.com/blog/openmemory-mcp-server/ — T2, nem fetchelve.
- deepwiki.com/mem0ai/mem0/15.2-openmemory-mcp-server — T2, nem fetchelve (AI-generált wiki, tudatosan mellőzve elsődleges forrásként).
- deepwiki.com/mem0ai/mem0/15.1-openmemory-overview-and-migration — T2, nem fetchelve.
- raw.githubusercontent.com/gannonh/memento-mcp/main/README.md — T1, verbatim, felhasznált.
- github.com/iAchilles/memento — T1 (github oldal-fetch, nem raw), felhasznált.
- github.com/carsteneu/ai-memory-comparison/tree/main/evidence — blokkolva (robots.txt).
- api.github.com/repos/carsteneu/ai-memory-comparison/contents/evidence — 403 (rate limit).
- glama.ai/mcp/servers/@gregorydickson/memory-graph/.../MIGRATION.md — blokkolva (robots.txt), tartalma ismeretlen maradt.
- github.com/okooo5km/memory-mcp-server — nem fetchelve, csak találat.
- mnemoverse.com/docs/library/memory-mcp-servers-compared — T3/T4, nem fetchelve, időhiány miatt.
- github.com/mem0ai/mem0/issues/4910 — nem releváns (konfigurációs bug).
- tooljunction.io/mcp/basic-memory, mcpservers.org/servers/..., glama.ai/mcp/servers/... — katalógusoldalak, csak találatok.

### SQ-04 — azonosítás és jogosultság

- modelcontextprotocol.io/specification/versioning — T1, verbatim, felhasznált — verzió-lista.
- modelcontextprotocol.io/specification/2024-11-05/basic — T1, verbatim, felhasznált — nincs auth.
- modelcontextprotocol.io/specification/2025-03-26/basic/authorization — T1, verbatim, felhasznált — első authorization-fejezet.
- modelcontextprotocol.io/specification/2025-06-18/changelog — T1, verbatim, felhasznált (SQ-01-ben is szerepel, azonos URL) — RFC 8707/9728.
- modelcontextprotocol.io/specification/2025-11-25/basic/transports — T1, verbatim, felhasznált — `Mcp-Session-Id`.
- modelcontextprotocol.io/docs/2025-11-25/tutorials/security/security_best_practices — T1, verbatim, felhasznált — Confused Deputy, Token Passthrough, Session Hijacking.
- modelcontextprotocol.io/specification/2026-07-28/basic/authorization — T1, verbatim, felhasznált — jelenlegi auth-spec.
- modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices — T1, verbatim, felhasznált — State Handle Hijacking, mix-up attack.
- modelcontextprotocol.io/specification/2026-07-28/basic/transports — T1, verbatim, felhasznált — stateless kimondása.
- modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio — T1, verbatim, felhasznált — "optional client identity".
- modelcontextprotocol.io/docs/2026-07-28/tutorials/security/authorization — T1, verbatim, felhasznált — gyakorlati Keycloak+SDK munkapélda.
- blog.modelcontextprotocol.io/posts/2026-07-28/ — T1, részben összefoglalva (azonos URL, mint SQ-01-ben), felhasznált a kulcsmondatokra.
- github.com/github/github-mcp-server/blob/main/docs/oauth-login.md — T1, **összefoglalva kapva, nem verbatim**, felhasznált korlátozott bizonyossággal.
- claude.com/docs/connectors/building/authentication — T1, verbatim, felhasznált — Claude connector-azonosítási minta.
- stackoverflow.blog/2026/01/21/is-that-allowed-authentication-and-authorization-in-model-context-protocol/ — T2, verbatim, felhasznált.
- aembit.io/blog/mcp-authentication-and-authorization-patterns/ — T3, lead, nem nyitva.
- descope.com/blog/post/mcp-auth-spec — lead, nem nyitva.
- auth0.com/blog/mcp-streamable-http/ — lead, nem nyitva.
- equixly.com/blog/2026/08/05/stateless-mcp/ — lead, nem nyitva.
- medium.com/@ayshsandu/the-evolution-of-mcp-auth-... — T3, lead, nem nyitva.
- workos.com/blog/what-is-mcp-authorization — T2/T3, lead, nem nyitva.
- truto.one/blog/implementing-end-user-oauth-identity-passthrough-for-remote-mcp-servers/ — lead, nem nyitva.
- github.com/modelcontextprotocol/modelcontextprotocol/issues/1359 (SEP-1359) — T1 (lenne), nem nyitva.

---

*A dokumentum a `.research/mcp-felulet/` mappa tartalmának kivonata. A forrásmappa érintetlen
maradt; a fenti szöveg nem tartalmaz szintézist vagy ajánlást — kizárólag a négy alkérdés kutatási
anyagának összefoglalását.*
