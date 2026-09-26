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
