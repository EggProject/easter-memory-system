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
