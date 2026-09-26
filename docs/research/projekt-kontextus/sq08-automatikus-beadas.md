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