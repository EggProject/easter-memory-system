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
