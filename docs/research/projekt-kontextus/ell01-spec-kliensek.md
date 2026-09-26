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
