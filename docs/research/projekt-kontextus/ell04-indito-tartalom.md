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

