# Kivonat — dream (memória-konszolidáció)

Kutatási egységenként, szó szerinti idézetekkel. SQ01–SQ04: kutatási kör; ELL01–ELL02: adverzariális ellenőrzés; ELL03: a döntés után, egy korábbi kampány számainak ellenőrzése. Minden keresés az Exa eszközzel. A linkek a `linkek.md`-ben, a szintézis a `SZINTEZIS.md`-ben.

**Javítások az ellenőrzés után:** (1) az open-second-brain v0.9.0 2026-05-15-én jelent meg — az SQ02 „2025 vége" megjegyzése téves; (2) az Anthropic Dreams bemeneti tárát egy korai hozzáférésű `update_existing` kapcsoló mégis módosíthatja; (3) a „dream" szó agent-memóriára már egy 2025-12-03-i preprintben és a Claude Code-ban (2026-04-14) is előfordul, a Letta-PR (2026-04-21) nem a legkorábbi; (4) a MemoryAgentBench „legfeljebb 7%"-a a v2/v3-ból van, a v4 és az ICLR 2026 kiadvány „legfeljebb 28%"-ot ír; (5) az arXiv:2605.12978 ICML-elfogadása és a 2606.01435 COLM-workshop-elfogadása független forrásból nem igazolható. (6) ELL03, 2026-09-24: a mérési dokumentumban 2026-08-23 óta álló „+10,8 pp" és „61% / 71–82%" valós szám, de a +10,8 pont a teljes átalakítás hatása, nem a szabályé (a szabály egyedül +2,0 pont, 262K-nál 0), és a 71–82% a 6K–262K tartomány, 262K-nál a szám 82%.

---

# SQ01 — Mit jelent a „dream" / „sleep-time compute" / memória-konszolidáció a létező agent-memória rendszerekben?

**Módszertani megjegyzés (kötelező, a `_kozos.txt` szerint):** a keresést kizárólag az Exa eszközzel (`mcp__Exa__web_search_exa`, `mcp__Exa__web_fetch_exa`) végeztem. A `anthropic-skills:deep-web-research` skillt nem hívtam meg teljes (alügynököket indító) formájában, mert ez a feladat már maga egy launch-olt subagent futása egy nagyobb kutatási feladaton belül, és ebben a keretben nem tudok újabb, önálló al-ügynököket indítani; ehelyett a skill elveit (elsődleges forrás előny, szó szerinti idézetek, tier-jelölés, két független forrás megerősítés, ellentmondások kiírása) magam, degradált (egyágensű) módban követtem. `curl`-t nem használtam, mert minden szükséges anyag Exa-n keresztül elérhető volt.

## Rövid válasz

A „dream"/„sleep-time" fogalom az agent-memória rendszerekben egy **aszinkron, a beszélgetéstől elkülönített háttérfolyamatot** jelöl, amely a felhalmozott memóriát (memória-blokkokat, jegyzetfájlokat, tudásgráfot) átnézi, és duplikátumokat egyesít, elavult/ellentmondó bejegyzéseket cserél vagy visszaminősít, és néha új, magasabb szintű összefoglalást (mintázatot) ír. A kifejezés eredete az agent-memóriában **friss (2026 tavasza)**: a Letta `letta-code` repóban 2026.04.21-én neveztek át egy „reflection" funkciót „dream"-re; az Anthropic Claude Managed Agents „Dreaming" funkcióját 2026.04.29-én dokumentálták, 2026.05.06-án jelentették be nyilvánosan; az itechmeat/open-second-brain „dream pass"-e 2026.05.15-én (v0.9.0) jelent meg; a mem0 „Dream" funkciója 2026.08.04-én. Ez a néhány héten belüli konvergencia miatt **nem állapítható meg egyértelműen, ki használta elsőként** — ezt Ellentmondásként jelzem. A mögöttes analógia (alvás közbeni memória-konszolidáció, hippokampusz→neokortex reprodukció) jóval korábbi, tudományos eredetű (Wilson & McNaughton 1994, McClelland–McNaughton–O'Reilly 1995), és az AI/gépi tanulásban már 2020-ban megjelent explicit „dreaming" fázisként a DreamCoder rendszerben (program-szintézis, nem memória). A vizsgált rendszerek nagy többsége **LLM-alapú** konszolidációt futtat (Letta, Anthropic Dreaming, mem0 Dream, Zep/Graphiti edge-invalidation, LangMem, cognee memify); emberi jóváhagyás nélkül, automatikusan ír a legtöbb (Zep/Graphiti, LangMem, mem0 write-time merge/supersede, Claude Code AutoDream), míg másoknál a jóváhagyás opcionális vagy a tervezés része (Anthropic Dreaming külön output store-ba ír, ember dönt az átvételről; mem0-plugin „dream" skill alapból diff+jóváhagyás). Az egyetlen **teljesen LLM-mentes, determinisztikus** rendszer, amelyet találtam, az itechmeat/open-second-brain „dream pass"-e: számlálókkal, küszöbökkel és atomi fájlműveletekkel dolgozik, és kifejezetten hangsúlyozza, hogy „no LLM inside the algorithm". Mért, számszerű hatás (minőség/hiba/költség/idő) csak a Letta/Berkeley kutatási cikkben (kontrollált benchmark) és az Anthropic „Dreaming" funkciónál (egyetlen ügyfél, Harvey, kontrollálatlan, kb. 6×-os feladat-teljesítési arány) található; a többi rendszernél a konszolidációs mechanizmusra vonatkozó külön mért hatás forrás nélkül maradt.

## 1–2. Rendszerenkénti részletek

### Letta — „sleep-time agents" / „Dreaming"

A Letta (korábban MemGPT) 2025 áprilisában vezette be a „sleep-time compute" fogalmát kutatási cikként és termékfunkcióként egyszerre.

> „Sleep-time compute is a new way to scale AI capabilities: letting models 'think' during downtime. Instead of sitting idle between tasks, AI agents can now use their 'sleep' time to process information and form new connections by rewriting their memory state." — Letta blog, 2025-04-21, https://www.letta.com/blog/sleep-time-compute/

> „When you create agents with this type, Letta actually creates two agents under the hood: a primary agent and a sleep-time agent. […] the primary agent is not provided with tools to edit its core memory […] These tools are attached to the sleep-time agent […] Memory formation in MemGPT is incremental, so memories may become messy and disorganized over time. Sleep-time agents on the other hand can continuously improve their learned context to generate clean, concise, and detailed memories." — uo.

A hivatalos kísérő kutatási cikk (Berkeley + Letta szerzők) matematikailag is definiálja a folyamatot:

> „We refer to such a process, as sleep-time compute: where inference is done between interactions with the model while it would otherwise be idle in sleep-time. In practice, this is achieved by prompting the model to generate a new context consisting of inferences about the existing context…" — Lin, Snell, Wang, Packer, Wooders, Stoica, Gonzalez: *Sleep-time Compute: Beyond Inference Scaling at Test-time*, arXiv:2504.13171, 2025-04-17, https://arxiv.org/html/2504.13171v1

A Letta jelenlegi (2026-os) dokumentációja már a „dreaming" szót használja ugyanerre a mechanizmusra:

> „Dreaming uses background subagents to review recent conversations, consolidate lessons, and update memory without interrupting active work. […] `trigger` controls when dreaming runs: after a number of steps, on context compaction, or never. `behavior` controls what happens at the trigger: remind the agent to update memory, or automatically launch a background dreaming subagent." — Letta Docs, „Memory | Letta Docs", https://docs.letta.com/agent-sdk/memory/index.md

> „Select Agent reviews before applying to have your agent review and revise proposed memory updates in a second background conversation. This uses more model tokens and does not ask you for approval." — Letta Docs, „Memory & dreaming", https://docs.letta.com/configuration/memory/

A Letta hivatalos GitHub-skill dokumentációja konkrét műveleteket nevesít:

> „Sleeptime agent reviews conversation history and refines memory blocks […] - Consolidate repeated information - Organize the lessons_learned block - Update human block with patterns it notices" — https://github.com/letta-ai/skills/blob/HEAD/letta/letta-api-client/sleeptime.md

**Indító:** konfigurálható — lépésszám (`sleeptime_agent_frequency`, pl. minden 5. beszélgetés után), kontextus-kompaktálási esemény, vagy „soha". **Ír/javasol:** alapértelmezésben közvetlenül ír (a sleep-time/dreaming subagent szerkesztheti a fő ágens memória-blokkjait); opcionális „review before applying" lépés is csak egy **másik ágenssel** ellenőrizteti, nem emberrel — a dokumentáció kifejezetten írja, hogy ez „does not ask you for approval". **Jóváhagyás:** nincs emberi jóváhagyás alapból. **LLM:** igen — a sleep-time/dreaming ágens tetszőleges (jellemzően erősebb) modellt futtat, a forráskód (`sleeptime_multi_agent.py`, `sleeptime_multi_agent_v4.py`) szerint valódi LLM-hívásos ágensként fut a háttérben.

**Két független megerősítés:** a fenti blogbejegyzésen és a kutatási cikken kívül a Letta docs (`docs.letta.com`) és a hivatalos GitHub-skill dokumentáció is önállóan, egymástól függetlenül ugyanezt írja le — 4 elsődleges forrás.

### Anthropic — Claude Managed Agents „Dreaming" (hivatalos, elsődleges forrás)

Az Anthropic hivatalos platform-dokumentációja szerint:

> „Dreaming is a research preview feature. […] Agents write to their memory stores as they work, but these writes are local and incremental: over many sessions a memory store accumulates duplicates, contradictions, and stale entries. Dreams let Claude clean that up. A dream reads an existing memory store alongside past session transcripts, then produces a new, reorganized memory store: duplicates merged, stale or contradicted entries replaced with the latest value, and new insights surfaced. The input store is never modified…" — Anthropic Platform Docs, „Dreams", 2026-04-29, https://platform.claude.com/docs/en/managed-agents/dreams

> „A dream is an asynchronous job that takes: a pre-existing memory store… and 1 to 100 sessions… During the research preview `claude-opus-5`, `claude-fable-5`, `claude-opus-4-8`, `claude-opus-4-7`, `claude-sonnet-5`, and `claude-sonnet-4-6` are supported." — uo.

A hivatalos bejelentő blogbejegyzés (2026-05-06, Code with Claude konferencia) így írja le a mechanizmust, és itt szerepel az egyetlen, Anthropic által közölt ügyfél-eredmény is:

> „Dreaming is a scheduled process in Claude Managed Agents that reviews agent sessions and memory stores, extracts patterns, and curates memories so agents improve over time. You decide how much control you want: dreaming can update memory automatically, or you can review changes before they land." — Claude by Anthropic blog, „New in Claude Managed Agents: dreaming, outcomes, and multiagent orchestration", https://claude.com/blog/new-in-claude-managed-agents

> „Harvey uses Managed Agents to coordinate complex legal work like long-form drafting and document creation. With dreaming, their agents remember what they learned between sessions, including filetype workarounds and tool-specific patterns. Completion rates went up ~6x in their tests." — uo. (ugyanaz az elsődleges forrás)

**Indító:** a fejlesztő indítja el explicit API-hívással (memory_store + 1–100 session); a blog „scheduled process"-nek nevezi, de az API-dokumentáció szerint minden egyes dream-futtatás egy önálló, a fejlesztő által indított job — az automatikus, platform-oldali ütemezés léte az elsődleges forrásokból nem derül ki egyértelműen (lásd Ellentmondások). **Ír/javasol:** alapból **külön, új output memory store**-ba ír, a bemeneti store-t sosem módosítja; a fejlesztő dönthet úgy is (`update_existing`), hogy a dream a saját bemeneti store-ját helyben konszolidálja. **Jóváhagyás:** választható — „dreaming can update memory automatically, or you can review changes before they land" — tehát mindkét mód (auto-alkalmazás és emberi felülvizsgálat) hivatalosan támogatott. **LLM:** igen, Claude Opus/Sonnet modellek.

### Claude Code — hivatalos dokumentáció vs. nem dokumentált „AutoDream" (csak elsődleges forrás)

A hivatalos Claude Code dokumentáció (`code.claude.com/docs/en/memory`) **nem említ** „dream"/konszolidációs háttérfolyamatot. Csak két mechanizmust dokumentál: a felhasználó által írt `CLAUDE.md`-t, és az „Auto memory"-t, amely önmagában **extrakció**, nem konszolidáció:

> „Auto memory lets Claude accumulate knowledge across sessions without you writing anything. Claude saves notes for itself as it works… Claude doesn't save something every session. It decides what's worth remembering…" — Claude Code Docs, „How Claude remembers your project", https://code.claude.com/docs/en/memory

Ugyanakkor az Anthropic **hivatalos** `anthropics/claude-code` GitHub-repó issue-trackerén (ami a `_kozos.txt` szabálya szerint elsődleges forrásnak számít) létezik egy, a nyilvános dokumentációban nem szereplő, beállítással kapcsolatos jelentés:

> „After enabling `autoDreamEnabled: true` in `~/.claude/settings.json`, Auto Dream silently deleted 23 memory files within approximately 24 hours. No confirmation was requested, and no record of what was deleted or why was provided." — GitHub, anthropics/claude-code, Issue #47959, 2026-04-14, https://github.com/anthropics/claude-code/issues/47959

Ez az elsődleges forrás igazolja, hogy létezik (vagy létezett, feature-flag mögött) egy `autoDreamEnabled` nevű, nem dokumentált Claude Code funkció, amely **közvetlenül töröl** memóriafájlokat emberi jóváhagyás nélkül, és ez hibaként/incidensként lett jelentve. Egy **nem hivatalos**, közösségi, reverse-engineelt dokumentáció (nem Anthropic-repó, T3, csak tájékoztató jelleggel, forráskód-hivatkozásokkal `src/services/autoDream/autoDream.ts`-re) részletesebben leírja az általa feltételezett működést:

> „AutoDream is Claude Code's background memory consolidation mechanism, internally codenamed 'Dream: Memory Consolidation'. When you're inactive (default interval: 24 hours with 5 accumulated sessions), Claude silently launches a 'dreaming' sub-agent (forked subagent) in the background." — GitHub, HFurther/claude-code-stable (közösségi, nem hivatalos), docs/en/memory/03-autodream.md — **T3, óvatosan kezelendő, nem Anthropic-forrás**

**Következtetés (csak elsődleges forrásból):** az Anthropic hivatalos Claude Code dokumentációja **nem** ismer el „dream"/konszolidációs funkciót; egy hivatalos GitHub-issue viszont igazolja egy nem dokumentált, `autoDreamEnabled` nevű, feature-flaggel vezérelt (a közösségi forrás szerint `tengu_onyx_plover` GrowthBook-flag) mechanizmus **létezését és károkozását** (fájltörlés jóváhagyás nélkül). **LLM:** a hivatalos issue nem mondja meg; a nem hivatalos forrás szerint igen (forkolt subagent, 4 fázisú konszolidációs prompt). Ezt a részt csak korlátozott bizonyossággal lehet állítani.

### Claude.ai (fogyasztói chat-memória) — hivatalos forrás, nincs „dream", de van napi szintézis (legacy)

Az Anthropic hivatalos súgóoldala (`support.claude.com`) szerint a **jelenlegi** („improved") memória-élmény folyamatosan, beszélgetés közben ír egyedi „topic" fájlokat, nem kötegelt utófeldolgozással:

> „Claude saves memory as a set of individual topics as you chat, rather than summarizing conversations after they end." — Claude Help Center, „Use Claude's chat search and memory to build on previous context", 2026-09-15, https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context

A **legacy** (régi, kivezetés alatt álló) élmény viszont explicit, napi ütemezésű kötegelt szintézist végzett — ez a „dream"-koncepcióhoz technikailag legközelebb álló, hivatalosan dokumentált claude.ai-mechanizmus, bár az Anthropic sosem nevezte „dream"-nek:

> „Claude will automatically summarize your conversations and create a synthesis of key insights across your chat history (not including chats in projects). This synthesis is updated every 24 hours and provides context for every new standalone conversation." — uo. (legacy szekció)

**Indító:** legacy — 24 óránkénti automatikus ütemezés; új élmény — folyamatos, session közbeni írás, nincs külön kötegelt konszolidációs lépés dokumentálva. **Ír/javasol:** közvetlenül ír, emberi jóváhagyás nélkül (a felhasználó utólag szerkesztheti/törölheti). **LLM:** igen (a szintézis/topic-generálás nyilvánvalóan LLM-alapú, bár ezt a dokumentáció nem mondja ki technikai részletességgel).

### mem0 — write-time konfliktuskezelés + külön „Dream" konszolidációs funkció

A mem0 alaparchitektúrája már write-time (nem batch) konfliktuskezelést végez:

> „The LLM itself determines which of four distinct operations to execute: ADD for creation of new memories when no semantically equivalent memory exists; UPDATE for augmentation of existing memories with complementary information; DELETE for removal of memories contradicted by new information; and NOOP…" — Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory, arXiv:2504.19413, https://arxiv.org/html/2504.19413v1

2026 közepén a mem0 külön, explicit „Dream" nevű, ütemezett háttér-konszolidációs funkciót is bevezetett:

> „Dream runs three operations on your project's memories. Merge. […] Supersede. […] Synthesize. A background job looks at groups of related memories and writes a new summary memory when several independent observations support one. […] Nothing is deleted in any of these operations. Every change is recorded as a state change with a pointer to the newer memory… Memories marked `immutable` or `exclude_from_dream` are skipped entirely." — mem0 blog, „Dream: Background memory consolidation for AI agents", 2026-08-04, https://mem0.ai/blog/dream-background-memory-consolidation-for-ai-agents

> „Human memory depends on sleep. The brain records all day and organizes at night… Dream gives agents the organizing phase, and does for an agent's memory what sleep does for ours." — uo.

> „Dream is available for all Pro and enterprise users. […] Runs happen weekly per project per eligible user_ids." — uo.

A mem0 hivatalos, forráskódban publikált „dream" skillje (egy Claude Code/Codex-integrációs Markdown-skill, nem maga a platform-funkció) **kifejezetten emberi jóváhagyást ír elő** alapesetben, és csak `--auto` módban engedi automatikusan a nem-ambivalens lépéseket:

> „All proposed changes are shown as a diff for user approval before anything is modified. […] Proposed: <N> merges, <N> prunes, <N> conflicts. Apply? [Y/n] […] In auto mode: Merges: applied automatically… Prunes: applied automatically… Contradictions: skipped — they require human judgment." — GitHub, mem0ai/mem0, `integrations/mem0-plugin/skills/dream/SKILL.md`, https://github.com/mem0ai/mem0/blob/b357a5a1b03c299ec8229c268e63cfac0f7c6566/integrations/mem0-plugin/skills/dream/SKILL.md

**Indító:** a platform-szintű Dream merge/supersede write-time (extrakciókor) dönt; a synthesize külön, heti ütemben fut projektenként. A skill-változat manuális CLI/parancs-indítású. **Ír/javasol:** platform-Dream automatikusan ír (állapot-jelölés: `merged`/`superseded`, semmi nem törlődik ténylegesen); a skill-változat alapból csak javasol (diff + jóváhagyás), `--auto` módban részlegesen automatikus. **Jóváhagyás:** platform-Dream nem kér emberi jóváhagyást; a skill-változat igen (kivéve `--auto`). **LLM:** mindkettő LLM-alapú.

### Zep / Graphiti — folyamatos (nem kötegelt) idővonal-alapú érvénytelenítés

A Zep/Graphiti nem batch „dream"-et, hanem valós idejű, minden új tény beérkezésekor lefutó ellentmondás-feloldást végez:

> „The introduction of new edges can invalidate existing edges in the database. The system employs an LLM to compare new edges against semantically related existing edges to identify potential contradictions. When the system identifies temporally overlapping contradictions, it invalidates the affected edges by setting their $t_{invalid}$ to the $t_{valid}$ of the invalidating edge." — Rasmussen, Paliychuk, Beauvais, Ryan, Chalef: *Zep: A Temporal Knowledge Graph Architecture for Agent Memory*, arXiv:2501.13956, 2025-01-20, https://arxiv.org/abs/2501.13956

> „New facts integrate immediately. Outdated facts are invalidated by temporal logic — preserved as history, removed from current state." — Graphiti hivatalos oldal, https://www.getzep.com/platform/graphiti/

**Indító:** minden új „episode"/tény betöltésekor (esemény-vezérelt, nem időzített). **Ír/javasol:** közvetlenül ír (érvényteleníti a régi élt, nem törli). **Jóváhagyás:** nincs. **LLM:** igen, az élek közötti ellentmondás-összehasonlításhoz.

### LangMem (LangChain) — háttérben futó „reflection", nem batch „dream"

> „'Subconscious' memory formation refers to the technique of prompting an LLM to reflect on a conversation after it occurs (or after it has been inactive for some period), finding patterns and extracting insights…" — LangMem Conceptual Guide, https://langchain-ai.github.io/langmem/concepts/conceptual_guide/

> „Using a collection-type memory adds some complexity to the process of updating your memory state. The system must reconcile new information with previous beliefs, either deleting/invalidating or updating/consolidating existing memories." — uo.

> „ReflectionExecutor defers memory processing and cancels redundant work… Wait 30 minutes before processing. If new messages arrive before then: 1. Cancel pending processing task 2. Reschedule…" — LangMem, „Delayed Background Memory Processing", https://langchain-ai.github.io/langmem/guides/delayed_processing/

**Indító:** minden üzenet után azonnal, vagy debounce-olt késleltetéssel (pl. 30–60 perc inaktivitás után), beszélgetés-szálanként — nem egy teljes tárolóra kiterjedő, ütemezett kötegelt „dream". **Ír/javasol:** közvetlenül ír a store-ba. **Jóváhagyás:** nincs beépített emberi jóváhagyási kapu. **LLM:** igen, a „memory manager" egy LLM-Runnable.

### cognee — „memify" gazdagítási csővezeték (explicit hívású, nem „dream")

> „The `.memify` operation runs enrichment pipelines on an existing knowledge graph. It requires a graph built by Add and Cognify — it does not ingest raw data or build the graph from scratch." — cognee Docs, „Memify", https://docs.cognee.ai/core-concepts/main-operations/legacy-operations/memify

> „Calls `cognee.memify()` with entity-consolidation tasks via `consolidate_entity_descriptions_pipeline()`. […] Enrichment (`generate_consolidated_entities` → `add_data_points`) — sends each entity and its neighborhood to the LLM, which returns a refined description." — uo.

> „`detect_entity_duplicates` — Find semantically near-duplicate Entity nodes […] `merge_entity_duplicates` — Merge the duplicates found by detect_entity_duplicates" — cognee Python API docs, https://docs.cognee.ai/python-api/memify

> „`contradicts` edges may also be present if you enabled contradiction detection — each one records the two conflicting facts, the reason, and a confidence score" — cognee Docs, „Cognify", https://docs.cognee.ai/core-concepts/main-operations/legacy-operations/cognify

**Indító:** explicit API/CLI-hívás (`memify()`), opcionálisan `run_in_background=True` — nincs a dokumentációban autonóm, saját ütemterv szerinti indítás („NINCS FORRÁS" az önálló ütemezésre). **Ír/javasol:** közvetlenül ír a gráfba. **Jóváhagyás:** nincs dokumentált jóváhagyási lépés. **LLM:** igen (entitás-extrakció, konszolidált leírás-generálás, ellentmondás-detektálás mind LLM-hívás).

### OpenAI ChatGPT „Memory" — folyamatos frissítés, dokumentált „dream"/batch konszolidáció nélkül

> „The previous saved memories system often became stale and relied on users to manually manage updates. Memories could also contradict one another… The new memory system updates memories automatically with ChatGPT keeping track of the details it determines are most important…" — OpenAI Help Center, „Memory FAQ", https://help.openai.com/en/articles/8590148

> „ChatGPT Plus and Pro users can now automatically manage saved memories by keeping the most relevant details prioritized and moving less important ones to the background. […] To decide which memories stay top of mind, ChatGPT considers factors such as how recent a detail is and how often you talk about a topic." — uo.

> „ChatGPT can manage saved memories on its own, updating, combining, or removing them when asked." — uo.

**Indító:** folyamatos, minden beszélgetés közben („memory summary is automatically updated with new context as you chat"); az „automatic memory management" rangsorolás is folyamatosnak tűnik, nincs külön ütemezett kötegelt job dokumentálva. **Ír/javasol:** közvetlenül ír. **Jóváhagyás:** nincs írás előtti jóváhagyás (utólagos szerkesztés/törlés lehetséges). **LLM:** igen. **„Dream"/batch-konszolidáció:** NINCS FORRÁS — az OpenAI hivatalos dokumentációja nem ír le semmilyen elkülönített, alvás-analógiájú vagy ütemezett kötegelt konszolidációs fázist; a „combining" csak kérésre, beszélgetésen belül történik, illetve a rangsorolás (decay-szerű prioritás-kezelés) folyamatos, nem kötegelt.

### itechmeat/open-second-brain — a legkifejezettebben LLM-mentes „dream pass"

> „Local-first 🧠 memory for Hermes Agent that lives in your Obsidian vault… Nightly 😴 dream passes turn repeat corrections into confirmed preferences with measurable confidence." — GitHub, itechmeat/open-second-brain, README, https://github.com/itechmeat/open-second-brain

> „Memory that learns deterministically. A `dream` pass turns repeat signals into rules and retires the ones nothing applies any more. Counters and atomic file moves — no LLM inside the algorithm, no surprise hallucinations in your memory." — uo.

> „The LLM lives outside the system: agents use it to detect signals in conversation and to apply rules during work. The system uses counters, thresholds, and atomic file operations — no LLM inside the algorithm, no surprise, no hallucinated memory." — GitHub, `docs/how-it-works.md`, https://github.com/itechmeat/open-second-brain/blob/7e6a5672/docs/how-it-works.md

A `dream` pass fázisai (forráskódból, `src/core/brain/dream.ts` és DeepWiki-összefoglaló):

> „| Phase | Module | Responsibility | | Scan | dream-scan.ts | Reads the entire Brain/ tree… | | Topic Planning | dream-plan-topics.ts | Groups signals by topic; plans new unconfirmed preferences or rebuttals. | | Refresh | dream-refresh.ts | Calculates applied_count, violated_count, and promotes unconfirmed → confirmed. | | Auto-Retire | dream-plan-retires.ts | Identifies stale or expired preferences for retirement. | | Reconcile | reconcile-outcomes.ts | Detects contradictions and classifies them into domains or open questions. | | Apply | dream-apply.ts | Executes the plan: moves files, updates frontmatter, and clears the inbox. |" — DeepWiki, „Dream Pass (Consolidation Engine)", https://deepwiki.com/itechmeat/open-second-brain/3.2-dream-pass-(consolidation-engine) — *(T2, generált wiki, de közvetlenül a forráskódra hivatkozik; a forráskód idézete alább elsődleges)*

> „Snapshot must succeed before any mutation. If it fails, the function throws and nothing changes on disk." — GitHub forráskód, `src/core/brain/dream.ts`, https://github.com/itechmeat/open-second-brain/blob/7e6a5672/src/core/brain/dream.ts

A v1.0.0-tól kezdve opcionális, emberi felülvizsgálatot lehetővé tevő „staged" mód is elérhető, de ez nem az alapértelmezett:

> „Staged dream pipeline. `o2b brain dream stage` persists the next learning pass as a reviewable, discardable bundle… `validate` recomputes the clock-normalized plan and reports drift; `apply` re-validates… `discard` drops the bundle without a trace." — GitHub, Release v1.0.0, https://github.com/itechmeat/open-second-brain/releases/tag/v1.0.0

**Indító:** szándék szerint éjszakai (cron-szerű) vagy manuális `o2b brain dream` / `brain_dream` MCP-hívás; a topik→preferencia átmenetet küszöbérték (pl. 3 azonos irányú jelzés) váltja ki, nem csak idő. **Ír/javasol:** az alap `dream` parancs **közvetlenül ír** (fájlmozgatás, frontmatter-frissítés), pillanatkép (snapshot) + rollback biztonsági hálóval, emberi jóváhagyás nélkül; a v1.0.0-s „staged" változat opcionálisan jóváhagyás elé tárja a tervet. **Jóváhagyás:** alapból nincs; opcionálisan igen (staged mód). **LLM:** **NEM** — a mag-algoritmus kifejezetten LLM-mentes; csak az opcionális havi/éves „rollup" összefoglaló-jegyzet szövegét írja LLM („needs-llm-step" boríték), a számlálás/döntés maga determinisztikus.

### basic-memory — nincs „dream"/konszolidációs funkció

A hivatalos dokumentáció és README egyike sem említ duplikátum-egyesítést, felejtést vagy ellentmondás-feloldást; a rendszer csak fájl↔adatbázis szinkronizálást és konzisztencia-ellenőrzést kínál:

> „# Health & maintenance / basic-memory status / basic-memory doctor # file <-> DB consistency check" — GitHub, basicmachines-co/basic-memory README, https://github.com/basicmachines-co/basic-memory

> „Sync Process: Detect Changes → Parse Files → Update Database → Resolve References → Update Search Index" — Basic Memory Docs, „Technical Information", https://docs.basicmemory.com/reference/technical-information

**NINCS FORRÁS** arra, hogy a basic-memory bármilyen „dream"-szerű, tartalmat átalakító/egyesítő háttérfolyamatot futtatna. (Negatív eredmény, 3 független hivatalos forrásból megerősítve: GitHub README, docs.basicmemory.com, basicmemory.com.)

## Összefoglaló táblázat

| Rendszer | Mit csinál | Indító | Ír / javasol | Jóváhagyás | LLM? | Forrás |
|---|---|---|---|---|---|---|
| **Letta** (sleep-time/„dreaming" agent) | Memória-blokkok újraírása: duplikátum-egyesítés, „lessons learned" szervezése, tanult kontextus tisztítása | Lépésszám / kompaktálási esemény / kézi | Közvetlenül ír a memória-blokkokba | Nincs (opcionális ágens-review, nem ember) | **Igen** | letta.com blog, docs.letta.com, arXiv:2504.13171, GitHub skill |
| **Anthropic Claude Managed Agents „Dreaming"** | Duplikátum-egyesítés, elavult/ellentmondó bejegyzés cseréje legfrissebbre, új mintázatok felszínre hozása | Fejlesztő indítja (API job), a blog „scheduled process"-nek nevezi | Alapból **külön output store**-ba (input változatlan); `update_existing` módban helyben | **Választható**: auto vagy emberi review | **Igen** (Opus/Sonnet) | platform.claude.com/docs (Dreams), claude.com/blog |
| **Claude Code „AutoDream"** (nem hivatalos dok.) | Jegyzetfájlok egyesítése, relatív→abszolút dátum, elavult tény törlése, index-újraépítés | 24 óra + 5 új session (alapérték), vagy `/dream` parancs, feature-flag mögött | **Közvetlenül töröl/ír** (dokumentált incidens szerint) | **Nincs** (hivatalos issue szerint jóváhagyás-kérés nélkül törölt) | Feltehetően igen (nem hivatalos forrás állítja) | GitHub anthropics/claude-code Issue #47959 (elsődleges); community repo (T3) |
| **Claude.ai fogyasztói memória** | Legacy: napi kötegelt szintézis; új élmény: folyamatos, per-téma írás | Legacy: 24 óránként; új: folyamatos | Közvetlenül ír | Nincs (utólagos szerkesztés/törlés van) | Igen (implicit) | support.claude.com (hivatalos súgó) |
| **mem0 „Dream"** (platform) | Merge (duplikátum), Supersede (ellentmondás → legfrissebb nyer, történet marad), Synthesize (új összefoglaló emlék) | Merge/Supersede: írási időben; Synthesize: heti ütemezés | Automatikusan ír (állapot-jelölés, nem törlés) | **Nincs** (platform-szinten automatikus) | **Igen** | mem0.ai/blog (2026-08-04), mem0 mintlify changelog |
| **mem0 „dream" skill** (agent-integráció) | Ugyanaz mint fent, de coding-agent kontextusban | Manuális CLI/skill-hívás | Alapból csak **javasol** (diff) | **Igen** (Y/n), kivéve `--auto` (ambivalens esetek akkor is emberhez mennek) | Igen | GitHub mem0ai/mem0 skill fájl |
| **Zep / Graphiti** | Új tény vs. régi élek LLM-alapú összevetése; ellentmondás esetén a régi élt időben érvényteleníti (nem törli) | Minden új „episode" betöltésekor (valós idejű, nem kötegelt) | Közvetlenül ír | Nincs | **Igen** | arXiv:2501.13956, getzep.com/platform/graphiti, GitHub README |
| **LangMem (LangChain)** | Memória bővítés/frissítés/törlés/konszolidálás egy LLM „memory manager" híváson belül | Minden üzenet után, vagy debounce-olt késleltetéssel beszélgetés-szálanként | Közvetlenül ír | Nincs beépített kapu | **Igen** | langchain-ai.github.io/langmem (több hiv. oldal), GitHub forrás |
| **cognee „memify"** | Entitás-duplikátum detektálás/egyesítés, konszolidált leírás-generálás, ellentmondás-jelölő élek | Explicit API/CLI hívás (`memify()`), opcionálisan háttérben fut, de nem önütemező | Közvetlenül ír a gráfba | Nincs dokumentált | **Igen** | docs.cognee.ai (memify, cognify, python-api) |
| **OpenAI ChatGPT „Memory"** | Folyamatos extrakció + „automatic memory management" (recency/frekvencia-alapú rangsorolás, nem valódi egyesítés) | Folyamatos, minden üzenetnél | Közvetlenül ír | Nincs írás előtti jóváhagyás | **Igen** | help.openai.com (Memory FAQ), openai.com/index blog |
| **itechmeat/open-second-brain „dream pass"** | Jelzés→„unconfirmed"→„confirmed" preferencia; auto-retire (elavult/ellentmondó); reconcile; (opcionális LLM-lépés csak az összefoglaló-jegyzet szövegéhez) | Küszöbérték (pl. 3 azonos jelzés) + éjszakai/kézi indítás (`o2b brain dream`) | **Közvetlenül ír** (fájlmozgatás), snapshot+rollback védelemmel; v1.0.0-tól opcionális „staged" mód | Alapból **nincs**; opcionálisan igen (staged) | **NEM** (a mag-algoritmus LLM-mentes) | GitHub itechmeat/open-second-brain (README, forráskód, CHANGELOG, release-ek, skill) |
| **basic-memory** | — (nincs dream/konszolidációs funkció) | — | — | — | — | docs.basicmemory.com, GitHub README, basicmemory.com (negatív eredmény) |

## 3. A „dream" kifejezés eredete

**Tudományos (neurotudományi) gyökér — nem AI-specifikus, de az analógia forrása:** a memória-konszolidáció alvás-analógiája jóval megelőzi az AI-ágenseket. Kachergis, de Kleijn és Hommel (ICCM 2015-ös workshop-cikk, majd 2016-os folyóiratváltozat) kifejezetten „dream model" címmel publikált egy számítási modellt az alvás alatti memória-újraaktiválásról és -újrakódolásról:

> „Memory consolidation–the process of crystallizing and integrating memories into knowledge and skills–is particularly benefitted by sleep. […] Keywords: memory consolidation; sleep; dreaming; hippocampal replay; memory model" — Kachergis, de Kleijn, Hommel: *A Dream Model: Reactivation and Re-encoding Mechanisms for Sleep-dependent Memory Consolidation*, 2016, https://www.kachergis.com/publication/kachergis-2016-dream/kachergis-2016-dream.pdf

**Első ismert AI/gépi tanulási rendszer, amely explicit „dreaming" fázist nevesít (nem agent-memória, hanem program-szintézis kontextusban):** a DreamCoder rendszer (Ellis és mtsai), amelyet a Royal Society Philosophical Transactions publikált:

> „DreamCoder gets its name from how it grows domain knowledge iteratively, in 'wake–sleep' cycles loosely inspired by the memory consolidation processes that occur during different stages of sleep […] The recognition model is learned offline during 'sleep,' from imagined datasets ('dreams' or 'fantasies') sampled from the generative model." — Ellis et al.: *DreamCoder: growing generalizable, interpretable knowledge with wake–sleep Bayesian program learning*, Phil. Trans. R. Soc. A, 2023-06-05, https://royalsocietypublishing.org/rsta/article/381/2251/20220050/112456/DreamCoder-growing-generalizable-interpretable

**Az agent-memória kontextusban a „dream"/„dreaming" szó legkorábbi, dátumozott elsődleges forrásból igazolható megjelenése** a Letta `letta-code` (CLI/TUI) repójában található:

> „fix(tui): rename reflection to dream" — GitHub, letta-ai/letta-code, PR #1856, létrehozva és mergelve 2026-04-21, https://github.com/letta-ai/letta-code/pull/1856

Ez néhány nappal megelőzi az Anthropic hivatalos „Dreams" dokumentációjának megjelenését (2026-04-29, https://platform.claude.com/docs/en/managed-agents/dreams) és a nyilvános bejelentést (2026-05-06, https://claude.com/blog/new-in-claude-managed-agents), és kb. egy hónappal az itechmeat/open-second-brain v0.9.0-s „dream" CLI-parancsának megjelenését (2026-05-15, https://github.com/itechmeat/open-second-brain/releases/tag/v0.9.0). Mivel a Letta korábbi (2025 áprilisi) anyagai kizárólag a „sleep-time compute"/„sleep-time agent" kifejezéseket használták, és a „dream" szó csak 2026-04-21-én jelenik meg (átnevezésként „reflection"-ről), **ez az egyetlen konkrét, dátummal igazolható „elsőség"-jelölt**, amit találtam — de lásd Ellentmondások, mert a különböző cégek dokumentumai néhány héten belül vannak egymáshoz képest, ami inkább egyidejű konvergenciára, mint egyértelmű elsőségre utal.

**Egy blog-forrás (T3, csak kiegészítésként, dátumozása ellentmondásos — lásd Ellentmondások) explicit „lineage"-t (családfát) állít fel**, Karpathy egy 2026. áprilisi „llm-wiki.md" gistjétől a Saish Sachin Shinde-féle „SCM: Sleep-Consolidated Memory with Algorithmic Forgetting" arXiv-preprinten át az Anthropic Dreams-ig:

> „Wilson and McNaughton recorded hippocampal neurons during sleep in rats and found that the same neural ensembles that fired during a maze run re-fired in the same temporal order during the slow-wave-sleep phase that followed. […] A year later, McClelland, McNaughton and O'Reilly proposed Complementary Learning Systems (CLS): the hippocampus learns fast and episodically, the neocortex learns slow and statistically, and consolidation is the bridge between the two…" — Ogham MCP blog, „Before Anthropic Dreams: a short lineage of memory consolidation", https://ogham-mcp.dev/blog/memory-consolidation-lineage/ — **T3, blog; a Wilson–McNaughton (1994) és McClelland–McNaughton–O'Reilly (1995) eredeti cikkeket magam nem értem el elsődleges forrásból, csak ezen a blogon és a Kachergis-cikk hivatkozásain keresztül — ezt jelzem az Ellentmondások/Nincs forrás szakaszban.**

## 4. Mérhető hatás (minőség, hibaarány, költség, idő)

- **Letta / Berkeley kutatási cikk — az egyetlen kontrollált, kvantitatív benchmark:**

> „…sleep-time compute can reduce the amount of test-time compute needed to achieve the same accuracy by ∼5× on Stateful GSM-Symbolic and Stateful AIME and that by scaling sleep-time compute we can further increase accuracy by up to 13% on Stateful GSM-Symbolic and 18% on Stateful AIME. […] by amortizing sleep-time compute across related queries… we can decrease the average cost per query by 2.5×." — arXiv:2504.13171, https://arxiv.org/html/2504.13171v1

  Egy ágensi (SWE-Features) esettanulmányban azonban a hatás nem egyértelműen pozitív: alacsony test-time költségvetésnél a sleep-time compute előnyös (kb. 1,5×-es token-csökkenés), magas költségvetésnél viszont a sima test-time compute jobb pontosságot ad — ezt a cikk maga is kiemeli, tehát **nem mindenütt egyértelmű a nyereség**.

- **Anthropic „Dreaming" — egyetlen, kontrollálatlan ügyfél-adat, elsődleges forrásból:**

> „Completion rates went up ~6x in their tests." (Harvey, jogi AI-cég) — https://claude.com/blog/new-in-claude-managed-agents

  Ez az Anthropic saját blogjában közölt, de módszertanilag nem részletezett (nincs A/B-teszt leírás, nincs mintaszám, nincs konfidenciaintervallum) egyetlen ügyfél-eset. Több független harmadik fél (sajtó/elemző blog, T2/T3) idézi ugyanezt a számot „Anthropic hivatalos bejelentésére" hivatkozva, de önálló, Anthropic-tól független mérést egyik sem közöl — ez lényegében egy forrásra (az Anthropic blogra) vezethető vissza, tehát **nem tekinthető két független forrással megerősítettnek a mérés maga**, csak az idézet létezése van többszörösen megerősítve.
  Megjegyzés: az ugyanabban a bejelentésben szereplő „+10 pont feladat-siker", „+8,4% docx", „+10,1% pptx" számok **nem** a Dreaming funkcióra, hanem a különálló „Outcomes" funkcióra vonatkoznak — ezt a forrás egyértelműen elválasztja, és fontos nem összekeverni.

- **mem0, Zep/Graphiti:** léteznek publikált benchmark-számok (mem0: LOCOMO/LongMemEval; Zep: DMR 94,8% vs. 93,4%, LongMemEval +18,5%, −90% látencia), de ezek a **teljes memóriarendszer** (extrakció+visszakeresés) teljesítményére vonatkoznak, nem elkülönítve a konszolidációs/„dream"-szerű mechanizmus hozzájárulására. **NINCS FORRÁS** a Dream/edge-invalidation komponens önálló, előtte-utána mért hatására.

- **LangMem, cognee, OpenAI ChatGPT Memory, basic-memory, itechmeat/open-second-brain:** **NINCS FORRÁS** semmilyen számszerű minőség-, hiba-, költség- vagy időmérésre a konszolidációs mechanizmusukra vonatkozóan. Az open-second-brain esetében található szoftvertesztelési szám (pl. „4248 tests / 0 fail" a v1.0.0 release note-ban), de ez **kódhelyesség**, nem memória-minőségi hatás mérése, ezért itt nem számít releváns mérésnek.

## Ellentmondások

1. **Ki használta elsőként a „dream" szót agent-memóriára?** A dátumozott elsődleges források (Letta GitHub PR: 2026-04-21; Anthropic Dreams docs: 2026-04-29; Anthropic nyilvános bejelentés: 2026-05-06; open-second-brain v0.9.0: 2026-05-15) mind néhány héten belül vannak egymáshoz képest. Ez inkább egyidejű iparági konvergenciára utal, mintsem egyértelmű elsőségre — nem lehet kizárni, hogy az Anthropic belső fejlesztése/dokumentációja már a nyilvános April 29-i megjelenés előtt is használta a szót. Egy blogforrás (Ogham MCP, T3) explicit „konvergencia 32 nap alatt" narratívát ad elő, de ennek a blognak a saját publikálási dátuma (2025-04-02) ellentmond a benne leírt, egyértelműen 2026-os eseményeknek — ez a forrás metaadat-inkonzisztenciát mutat, ezért csak korlátozott bizalommal kezelendő.
2. **Anthropic „Dreaming": automatikusan ütemezett-e, vagy csak fejlesztő-indított?** A bejelentő blog „scheduled process"-nek nevezi a Dreaming-et, miközben a technikai API-dokumentáció (Dreams API) szerint minden dream egy explicit, fejlesztő által indított job (memory_store + session-lista paraméterekkel) — nincs dokumentált, platform-oldali automatikus ütemező. A két elsődleges forrás retorikája ezen a ponton nem teljesen konzisztens.
3. **Claude Code AutoDream státusza bizonytalan.** A hivatalos dokumentáció nem ismeri el a funkció létezését, miközben egy hivatalos GitHub-issue (elsődleges forrás) igazolja egy `autoDreamEnabled` nevű, kárt okozó, feature-flag mögötti mechanizmus valós működését. Nem állapítható meg elsődleges forrásból, hogy ez hivatalosan tervezett, tesztelés alatt álló, vagy visszavont funkció-e.
4. **Mem0 „Dream" — állítás vs. gyakorlat a törlésről:** a platform-szintű Dream dokumentációja szerint „nothing is deleted", csak állapot-jelölés (`merged`/`superseded`) történik; ezzel szemben az agent-integrációs „dream" skill dokumentációja explicit `delete_memory()` hívásokat ír elő egyesítéskor és megerősített ellentmondás-feloldáskor. A két mem0-termék (platform API vs. skill) tehát eltérő törlési szemantikát valósít meg ugyanazon „Dream" márkanév alatt.

## Amire NINCS forrás

- Nincs forrásom Wilson & McNaughton (1994) és McClelland, McNaughton & O'Reilly (1995) eredeti cikkeinek közvetlen, elsődleges eléréséhez — ezeket csak másodkézből (Kachergis et al. 2016 hivatkozásai, illetve egy T3 blog) tudtam idézni.
- Nincs forrásom arra, hogy az Anthropic Claude Managed Agents platformja saját maga (fejlesztői beavatkozás nélkül) automatikusan ütemezné a dream-futtatásokat.
- Nincs forrásom arra, hogy a cognee `memify()` pipeline-nak lenne bármilyen autonóm, saját időzítésű (cron-szerű) indítási mechanizmusa a platformon belül.
- Nincs forrásom semmilyen kvantitatív (minőség/hiba/költség/idő) mérésre a következő rendszerek konszolidációs mechanizmusára nézve elkülönítve a teljes rendszertől: mem0 Dream, Zep/Graphiti edge-invalidation, LangMem, cognee memify, OpenAI ChatGPT Memory, basic-memory, itechmeat/open-second-brain dream pass.
- Nincs elsődleges forrásom a Claude Code „AutoDream" funkció pontos technikai működésére (csak egy nem hivatalos, reverse-engineelt közösségi dokumentumra); a hivatalos GitHub-issue csak a tünetet (jóváhagyás nélküli törlés) és a beállítás nevét (`autoDreamEnabled`) igazolja.
- Nincs forrásom arra, hogy a claude.ai jelenlegi („improved") fogyasztói memória-élménye végezne-e bármilyen kötegelt duplikátum-egyesítést vagy ellentmondás-feloldást a folyamatos, per-téma írás mellett/helyett — a hivatalos súgó erről hallgat.

---

# SQ02 — LLM nélküli, determinisztikus memória-konszolidáció

## Módszertani megjegyzés (degradált mód)

A `_kozos.txt` előírása szerint az `anthropic-skills:deep-web-research` skill elveit kellett követni. Ez a feladat egyetlen, szűken körülhatárolt alkérdés (SQ02) kutatása egy már elindított, több alkérdésre bontott kutatási munkamenetben; önálló al-ügynök (subagent) indítása helyett a kutatást **közvetlenül**, a kötelező Exa-eszközökkel (`mcp__Exa__web_search_exa`, `mcp__Exa__web_fetch_exa`) végeztem, több körben, elsődleges forrásokra (GitHub forráskód, README, kiadási jegyzékek, arXiv) fókuszálva, és minden lényeges állítást igyekeztem 2+ független forrással alátámasztani. Ez a skill „degradált módja" — nem indítottam al-ügynököket, minden keresést és oldalolvasást én magam végeztem, szó szerinti idézetekkel dokumentálva.

## Rövid válasz

Az itechmeat/open-second-brain (jelenlegi verzió: **v1.54.0**, kiadva **2026-08-28**) „dream" folyamata öt elnevezett fázisra (close → reconcile → synthesize → heal → log) bomlik, de ezek — a fejlesztők saját, 2026-07-27-i (v1.40.0) visszaellenőrzése szerint — „**a reporting label with no callable units**", azaz egyetlen, változatlan determinisztikus algoritmus feletti napló-címkék, nem önálló hívható lépések. A „synthesize" itt NEM szöveg-szintézist jelent, hanem a promóciós/megerősítési írást (unconfirmed→confirmed preferenciák és számlálók lemezre írása) — nulla LLM-hívással. Van snapshot (SHA-256-tal védett, tar.zst), rollback, dry-run és a rendszer kifejezetten idempotensnek van dokumentálva. A korábbi feljegyzés fő állításai ma is igazak, egy ponton pontosítást igényelnek: a fázisok elnevezése csak 2026 júliusa (v0.21.0) óta létezik, korábban (v0.9.0, 2025 vége) csak a „dream" mint egyetlen, névtelen lépés létezett. Az iparágban több más LLM-mentes, determinisztikus konszolidációs technika is dokumentált: koszinusz-küszöbös közel-duplikátum-egyesítés, negáció-egyezés alapú ellentmondás-jelzés, Ebbinghaus-ihletésű exponenciális lecsengés, összekapcsolt-komponens klaszterezés, valamint gráf/string-alapú wiki-lint eszközök (törött linkek, árva oldalak, elavult dátumok). Mérés a determinisztikus vs. LLM-alapú összehasonlításra: egy 2026 májusi/augusztusi arXiv-cikk (Reddy & Challaram) a MemoryAgentBench FactConsolidation feladatán **78,0% (gpt-4o-mini) és 94,8% (gpt-4o)** pontosságot mért egy determinisztikus `Python max(serial)` szabállyal a legjobb publikált LLM-alapú rendszer (HippoRAG-v2, **54,0%**) ellenében — ez pontosan megfelel a korábbi kutatásunkban említett számoknak, FORRÁSSAL AZONOSÍTVA. Fontos ellentmondás/finomítás: a cikk saját v2 revíziója szerint a nyereség nagy része NEM magából a determinisztikus szabályból, hanem az „evidence extraction" és a „policy execution" szétválasztásából ered (a puszta végrehajtó-csere hatása csak +2,0pp). Egy másik, „LLM nélküli memória-fúziós" mérés (DFM-Fusion, LoCoMo-teszt) forrása egy **teljesen automatizált, emberi felügyelet nélkül publikáló AI-kutatórendszer (FARS/Analemma)** terméke — ezt külön, erősen fenntartással jelöltem, mert nem sikerült független megerősítést találni rá.

---

## 1. Az itechmeat/open-second-brain „dream" folyamata

### 1.1 Azonosítás, verzió, dátum

A projekt: https://github.com/itechmeat/open-second-brain — „Open Second Brain", Obsidian-natív memóriaréteg a Hermes Agent nevű ügynökhöz, Claude Code / Codex / OpenClaw adapterekkel és MCP szerverrel.

A README (2026-08-28-i állapot, T1) szerint jelenlegi verzió:

> „Open Second Brain 1.54.0 turns `visibility:` from a label into a boundary." — https://raw.githubusercontent.com/itechmeat/open-second-brain/main/README.md

A v1.54.0 kiadási jegyzék pontos dátuma:

> „Tag: v1.54.0 … Published: 2026-08-28T00:59:38Z … Author: solaitken" — https://github.com/itechmeat/open-second-brain/releases/tag/v1.54.0

A projekt rendkívül aktív (napi-heti kiadási ütem, pl. v1.50.0 → v1.54.0 két hét alatt), ezért minden állítást a fenti verzióra vonatkoztatok, és jelzem, melyik korábbi kiadásból származik egy-egy funkció.

### 1.2 A lépések pontosan: close → reconcile → synthesize → heal → log

A névvel ellátott fázisokat a **v0.21.0** kiadás ("Brain lifecycle suite") vezette be:

> „Multi-phase dream pipeline. The proven `dream` internals are unchanged; the existing seams are named as ordered phases - close -> reconcile -> synthesize -> heal -> log - each emitting a workrun checkpoint and a structured per-phase summary. A no-op run returns an empty phase list." — https://github.com/itechmeat/open-second-brain/releases/tag/v0.21.0

Ugyanez, bővebben, a projekt saját dokumentációjában (`docs/how-it-works.md`, T1, forráskód-repó):

> „The same pipeline is named as five explicit ordered phases - **close** (scan) -> **reconcile** (contradictions) -> **synthesize** (promote / confirm) -> **heal** (auto-retire stale, optional enrichment) -> **log** … The internals are unchanged; the phases are labels over the existing seams, so every invariant above still holds." — https://github.com/itechmeat/open-second-brain/blob/7e6a5672/docs/how-it-works.md

Tehát pontosan lépésenként (a forráskód, `src/core/brain/dream.ts` és `dream-apply.ts` alapján, T1):

1. **close (scan)** — a teljes `Brain/` fát beolvassa memóriába (`scanBrain`), a hibás frontmatterű fájlokat külön jelzi, nem szakítja meg a futást.
2. **reconcile** — ellentmondás-detektálás: azonos témájú, de ellentétes irányú preferenciákat strukturális jel alapján 4 doménbe sorolja (claims / entity / decisions / source-freshness); csak a „source-freshness" kategóriában, egyértelmű frissességi rés esetén oldódik fel automatikusan — ekkor is csak *naplózva*, sosem küszöb alatti (bizonytalan) írással:
   > „Reconcile-phase domain classification. Each contradiction is bucketed by structural signal shape into claims / entity / decisions / source-freshness. Only a decisive source-freshness gap auto-resolves - recorded as a `reconcile` log event, never a sub-threshold mutation; everything else surfaces as an operator-facing open question instead of a forced merge. No LLM fan-out." — https://github.com/itechmeat/open-second-brain/releases/tag/v0.21.0
3. **synthesize (promote / confirm)** — az új, még nem megerősített preferenciák felírása, a meglévők frissítése (számlálók, konfidencia), és a küszöböt elért preferenciák „unconfirmed"→„confirmed" előléptetése. A forráskód kommentje szerint:
   > „Synthesize is durable here and nowhere earlier: every new unconfirmed preference, every refreshed preference and every confidence receipt has landed. `promote_complete` is the pre-F2 name for the same writes, so it moves with it rather than being left behind claiming a batch that had not started." — https://github.com/itechmeat/open-second-brain/blob/7e6a5672/src/core/brain/dream-apply.ts
4. **heal** — elavult/lejárt preferenciák „retired/"-be mozgatása (kivéve a `pinned: true` jelölésűeket, ezekhez `retain-pinned` eseményt naplóz), opcionálisan (alapból KIKAPCSOLVA, `dream.heal_enrich_enabled: false`) hiányzó cím kiegészítése az első H1-ből és pontos cím/alias-említések összekötése linkekkel.
5. **log** — a napi log fájl (`Brain/log/YYYY-MM-DD.md`) írása, per-preferencia audit JSONL bejegyzés, workrun-checkpointok.

**Kritikus pontosítás** — a fejlesztők maguk vizsgálták felül ezt a fázis-modellt a **v1.40.0** kiadásban (2026-07-27, „No dead ends"), és megállapították, hogy a fázisok NEM önálló hívható egységek:

> „Seven parallel passes over the code invalidated a premise in eight of the ten sources: … semantic dedup nominates and never drops, **the dream "phases" were a reporting label with no callable units**, and the profile ticket named an artifact that does not exist." — https://github.com/itechmeat/open-second-brain/releases/tag/v1.40.0

Ugyanez a kiadás azt is megerősíti, hogy a mag (kernel) ekkor is LLM-mentes maradt:

> „The kernel still calls no LLM, and every new flag, argument and configuration key is byte-identical when absent." — https://github.com/itechmeat/open-second-brain/releases/tag/v1.40.0

Fontos: a `dream` motor **külön parancsként** is célzottan futtatható egy-egy lépésre (`o2b brain dream run --step <scan|heal-enrich>`), de ez konfiguráció-szintű felülbírálás, nem azt jelenti, hogy a lépések önálló, egymástól független modulok — a v1.40.0 megjegyzése szerint „**two planning steps mutate each other's accumulators specifically so a preference is never both refreshed and retired**" (https://github.com/itechmeat/open-second-brain/releases/tag/v1.40.0).

### 1.3 Mit jelent a „synthesize" LLM nélkül — fontos terminológiai csapda

A kódbázisban a „synthes(iz)e" szó **két, egymástól különböző dologra** utal, ezt érdemes szétválasztani:

- A **dream-fázis „synthesize"** lépése (fent) = determinisztikus promóció/megerősítés írása (preferencia-frontmatter és számlálók), NEM szöveggenerálás.
- Van emellett egy önálló **`o2b brain synthesise`** CLI-parancs is, ami egy „koncepció-klaszter" (céljegyzet + minden rá hivatkozó, 1-mély wikilinkelt anyag) összeállítására szolgál — ez is kifejezetten LLM-mentes, csupán egy JSON-borítékot állít össze, amit *le lehet* adni egy külső LLM-szintézishez, de maga a parancs nem hív LLM-et:
  > „usage: o2b brain synthesise [--include-unlinked] [--vault] [--json]\nAssemble the concept-cluster envelope: target note + every artifact\nthat wikilinks to it (depth-1). With --include-unlinked also include\nraw-text mentions outside [[...]]. **Pure assembler, no LLM call.** Output\nis a deterministic JSON envelope downstream consumers can feed to\nany synthesis prompt. Read-only." — https://github.com/itechmeat/open-second-brain/blob/7e6a5672/src/cli/brain/help-text.ts

Ez azt jelenti: mindkét „synthesize"/„synthesise" jelentés LLM nélküli a mag algoritmusban — a rendszer szigorúan betartja a „KEMÉNY SZABÁLY: … szöveggeneráló LLM SEHOL nincs benne" elvet a saját konszolidációs magjában is.

### 1.4 Snapshot, rollback, dry-run, idempotencia

Mind a négy megerősíthető, T1 forrásokból:

**Snapshot + rollback** (v0.9.0, később SHA-256 sidecar-ral kiegészítve):

> „**Pre-run snapshots**: each `dream` run that mutates state writes `Brain/.snapshots/<run_id>.tar.zst` of the entire `Brain/` tree (excluding `.snapshots/` itself) before any mutation. Default retention 10 most-recent. `o2b brain rollback <run_id>` restores from a snapshot." — https://github.com/itechmeat/open-second-brain/releases/tag/v0.9.0

> „Brain mutations (`dream`, `merge`, `upgrade`) take a pre-run snapshot with a SHA-256 sidecar; `o2b brain rollback` aborts on drift unless `--force-rollback`." — https://raw.githubusercontent.com/itechmeat/open-second-brain/main/README.md

**Dry-run**: a `dream` beépített paranccsal (`o2b brain dream [run] [--dry-run] | stage | validate | apply | discard | list`), illetve egy dedikált, mutáció nélküli előnézeti MCP eszközzel:

> „usage: o2b brain dream [run] [--dry-run] | stage | validate | apply |\n discard | list … **Runs the deterministic dreaming algorithm (idempotent)**, or manages the staged\nlifecycle: stage persists a reviewable proposal bundle under Brain/dream/staged/,\nvalidate proves the vault has not drifted, apply re-validates then runs the same\nengine live, discard drops [the] bundle." — https://github.com/itechmeat/open-second-brain/blob/7e6a5672/src/cli/brain/help-text.ts

> „**`brain_review_candidates` MCP tool** - read-only projection over what the next dream invocation would do. … No persistent surface is mutated; the dry-run dream pass also skips the workrun emission, so reviewing candidates is purely observational." — https://github.com/itechmeat/open-second-brain/releases/tag/v0.12.0

**Idempotencia** — explicit dokumentálva és forráskód-szinten is (revízió csak akkor nő, ha a leírt bájtok ténylegesen változnának):

> „The Dream Pass is … designed to be deterministic, idempotent, and safe, utilizing snapshotting and workrun tracking to maintain vault integrity." — https://deepwiki.com/itechmeat/open-second-brain/3.2-dream-pass-(consolidation-engine) (T2 — másodkézből generált wiki, de a mögötte lévő forráskód-hivatkozásokkal alátámasztva)

> „`_revision`: bump only when the proposed write would change the on-disk bytes (idempotent dream rerun stays byte-identical)." — https://github.com/itechmeat/open-second-brain/releases/tag/v0.12.0

### 1.5 Inbox → ismétlődés utáni szabály

Megerősítve, v0.9.0 óta változatlan elv:

> „**Deterministic `dream` consolidation** turns ≥ N same-topic signals into an `unconfirmed` preference; subsequent applied / violated evidence promotes it to `confirmed`, contradiction or staleness retires it. All thresholds live in `_brain.yaml`; no LLM inside the algorithm." — https://github.com/itechmeat/open-second-brain/releases/tag/v0.9.0

A küszöbök konkrét nevei (DeepWiki, T2, forráskód-hivatkozásokkal `types.ts` 67-68. és 82-87. sorára):

> „New Preferences: If a topic has enough signals (defined by `candidate_threshold` in `_brain.yaml`), a new `unconfirmed` preference is planned … Promotion: Moves `unconfirmed` preferences to `confirmed` status if they meet the `promotion_threshold` (default 3 positive signals/evidence)." — https://deepwiki.com/itechmeat/open-second-brain/3.2-dream-pass-(consolidation-engine)

### 1.6 A korábbi feljegyzés ellenőrzése — eredmény

| Korábbi állítás | Ma is igaz? | Megjegyzés |
|---|---|---|
| „close → reconcile → synthesize → heal → log" | **IGEN**, betű szerint | De csak v0.21.0 (2026 nyara) óta létező elnevezés egy korábban is létező, egységes algoritmus felett |
| „Counters and atomic file moves — no LLM inside the algorithm" | **IGEN**, szó szerint idézhető a mai README-ből is | Változatlan a v0.9.0–v1.54.0 közötti teljes történetben |
| „inbox → ismétlődés után szabály" | **IGEN** | `candidate_threshold` (N azonos témájú jelzés) → unconfirmed; `promotion_threshold` (alapból 3) → confirmed |
| Snapshot/rollback/dry-run/idempotencia mind megvan | **IGEN**, mind a négy megerősítve | Snapshot SHA-256 sidecar-ral (v1.40.0 óta „skill-accept" tranzakciónál is), dry-run több szinten (`--dry-run`, `brain_review_candidates`, staged lifecycle) |

Egyetlen finomítás szükséges: a „lépésenként mit csinál" kérdésre a helyes válasz az, hogy a lépések **napló-címkék egy változatlan, egységes determinisztikus algoritmus fölött**, nem öt egymástól elszigetelt alrutin — ezt maguk a fejlesztők is tisztázták utólag (l. fent, v1.40.0).

---

## 2. Más LLM nélküli, determinisztikus technikák memória-/tudásbázis-karbantartásra

### 2.1 Beágyazás-alapú közel-duplikátum felismerés és klaszterezés

**mimir-mem-core** (Rust, forráskód/docs.rs, T1) — négy nem-destruktív konszolidációs lépés, explicit „LLM-free":

> „//! LLM-free memory consolidation: four passes, none destructive.\n//!\n//! 1. near-duplicate merge (cosine ≥ 0.92, same type+scope) → the older\n//! node is superseded, never deleted\n//! 2. contradiction flagging (high similarity + negation mismatch) —\n//! reported to the human, never auto-resolved\n//! 3. cluster distillation (cosine ≥ 0.80, clusters ≥ 5) → extractive\n//! summary node with `summarizes` edges\n//! 4. decay archival (effective strength < 0.05, untouched > 90 days) →\n//! soft-deleted with meta.archived = true (reversible)" — https://docs.rs/mimir-mem-core/latest/src/mimir_core/consolidate.rs.html

Saját teszt is bizonyítja a dry-run helyes viselkedését: „`dry_run_changes_nothing`" (uo.).

**solo-steward** (Rust, docs.rs, T1) — időablak + koszinusz-küszöb + union-find klaszterezés, explicit „no LLM":

> „Pure-deterministic episode clustering — the SWS-equivalent dedup pass that opens every consolidation cycle. … Per ADR-0002, this is the "IP" of Solo's consolidation: clustering logic lives in one place, tested deterministically, refined over time. **The LLM is the swap point** (used later by `abstract_cluster`), **not the clustering math**." — https://docs.rs/solo-steward/latest/solo_steward/cluster/index.html

**deep-memory** (TjWheeler, GitHub docs, T1) — entitás-deduplikáció Jaro–Winkler string-hasonlósággal, teljesen LLM nélkül:

> „The consolidator runs locally without LLM calls. All matching is deterministic -- exact slug comparison, alias lookup, and Jaro-Winkler string similarity. Low-confidence decisions are recorded in a merge log for human review." — https://github.com/TjWheeler/deep-memory/blob/main/docs/indexer-consolidation-guide.md

**membox** (Roy Zhu blogja, T3, de forráskód-részlettel alátámasztva) — háromrétegű entitás-feloldás (pontos alias → 0,85 koszinusz-küszöb → új entitás), SQLite-on:

> „We found that a cosine similarity threshold of `0.85` hits the sweet spot for entity names. It's high enough to prevent `Microsoft` and `Apple` from merging … but low enough to catch `Apple Inc.` and `Apple`." — https://royzhu.dev/posts/building-a-deduplication-pipeline-for-local-knowledge-graphs/

**AutoMem** (hivatalos dokumentáció, T2) — gráf-klaszterezés (DBSCAN-szerű), MetaMemory csomópontokkal, küszöb: koszinusz ≥ 0,75, min. klasztermeret 3(-5):

> „The cluster task groups semantically similar memories using a graph-based clustering algorithm (similar to DBSCAN) and creates `MetaMemory` nodes to represent patterns." — https://automem.ai/docs/core-concepts/consolidation/

### 2.2 Felejtési/lecsengési pontszám

**MemoryBank** (Zhong, Guo, Gao, Ye, Wang; AAAI-24, 2024-03-24, T1, peer-reviewed) — Ebbinghaus-görbe ihlette frissítési mechanizmus:

> „To mimic anthropomorphic behaviors and selectively preserve memory, MemoryBank incorporates a memory updating mechanism, inspired by the Ebbinghaus Forgetting Curve theory. This mechanism permits the AI to forget and reinforce memory based on time elapsed and the relative significance of the memory…" — https://ojs.aaai.org/index.php/AAAI/article/view/29946

Fontos: a MemoryBank rendszer maga **LLM-alapú** (ChatGPT/ChatGLM-mel dolgozik, összefoglalást és személyiség-szintézist is végez) — csak a *lecsengési pontszám matematikai függvénye* determinisztikus (idő + jelentőségi súly), maga a memóriarendszer nem LLM-mentes.

**AutoMem** (T2) — explicit exponenciális lecsengési képlet:

> „1. Age-based decay: `exp(-0.01 * age_days)` — Exponential decay from creation timestamp … 6. Importance floor clamp: Final score is never allowed below `importance * 0.3`" — https://automem.ai/docs/core-concepts/consolidation/

**agentos ConsolidationLoop** (GitHub docs, T1) — kifejezetten a „biológiai lassúhullámú alvás analógiája", és a 6 lépésből csak egy (Derive) igényel LLM-et:

> „Memory consolidation is the analogue of slow-wave sleep: background maintenance that prunes weak traces, merges duplicates, strengthens co-activated patterns, derives new insights, compacts old episodic traces, and rebuilds the search index." … „| **ConsolidationLoop** | 6-step background maintenance pipeline | Only for the derive step |" — https://github.com/framersai/agentos/blob/8ff7a38e/docs/memory/MEMORY_CONSOLIDATION.md

Ugyanitt a Prune lépés konkrétan Ebbinghaus-erősség küszöbre hivatkozik: „Soft-delete traces whose Ebbinghaus strength has decayed below the `pruneThreshold` (default: 0.05)." (uo.)

**Unforget** (hivatalos dokumentáció, T2) — LLM nélkül is működő dedup/lecsengés/lejárat:

> „Without an LLM, consolidation still handles dedup, decay, and expiry — just not promotion." — https://docs.unforget.sh/docs/concepts/consolidation

### 2.3 Előléptetés használat alapján

- **open-second-brain**: unconfirmed→confirmed előléptetés bizonyíték-számláló küszöb alapján (l. 1.6 pont); emellett a „**continuity rank**" funkció kifejezetten csak valódi visszahívási (recall) teleметриára épít, NLP-szótár nélkül: „weights working-memory records by a usage-driven decay derived only from real recall telemetry, so stale decisions fade while actively-recalled ones stay prominent." — https://raw.githubusercontent.com/itechmeat/open-second-brain/main/README.md
- **agentos „Compact" lépés**: gyakran visszahívott epizodikus nyom automatikus áttípusítása szemantikussá: „Promote old, high-retrieval episodic traces to semantic type. This is a lightweight episodic-to-semantic migration." — https://github.com/framersai/agentos/blob/8ff7a38e/docs/memory/MEMORY_CONSOLIDATION.md
- **AutoMem**: `reinforcement_bonus: 0.2` — hozzáférésre erősség-növelés, valamint 90 napos védelmi periódus és `importance >= 0.7` védelem a törléstől. — https://automem.ai/docs/core-concepts/consolidation/

### 2.4 Elavult bejegyzés és törött hivatkozás felismerése (idő, hivatkozás hiánya)

Több önálló, egymástól független, kifejezetten „no LLM" wiki/tudásbázis-lint eszközt találtam markdown-alapú „second brain"/wiki rendszerekhez (mind T1, GitHub-forráskód):

**kb-lint** (SingggggYee, pip csomag is, T1):

> „kb-lint is a fast, dependency-free markdown knowledge base linter. … checks for broken wiki-links, missing frontmatter, orphan pages with no incoming links, thin articles below a word count threshold, structural issues … **No LLM required.**" — https://github.com/SingggggYee/kb-lint

**wiki-lint** skill (kfchou-wiki-skills, T2/eszköz-katalógus leírás, de forráskód-elérhető) — kifejezetten szétválasztja a determinisztikus (Phase 1, szkript) és az LLM-es (Phase 2, kontradikció-keresés) réteget:

> „Phase 1 runs `bin/lint-mechanical.py`, which computes the deterministic checks (graph and string properties) **with no LLM** and no bodies in your context…" … „Stale claims — `stale_date` (`{page}`): not updated in 90 days and the body still says `current`/`latest`/`recent`/`state-of-the-art` or names a year ≥2 years old." — https://www.claudepluginhub.com/skills/kfchou-wiki-skills/wiki-lint

**health_lint.py** (gosha70/code-copilot-team, T1) — „gyenge árva" (weak orphan) és „hiányzó keresztlink" heurisztika, expliciten elválasztva az egyetlen LLM-függő ellenőrzéstől:

> „The contradictions check is the only LLM-dependent one." … „_check_weak_orphans … A wiki page reachable from index.md via only ONE inbound edge is one hub-disconnect away from full orphanhood." — https://github.com/gosha70/code-copilot-team/blob/master/scripts/wiki_ingest/health_lint.py

**agent-wiki** (PyPI csomag, T1) — kiterjedt, LLM nélküli linthibalista (törött link, törött kép, törött horgony, hiányzó frontmatter, árva oldal, hiányzó visszahivatkozás):

> „Automated wiki health checks that catch real problems: … | Broken links | error | `[[Target]]` where no file matches | … | Orphan pages | warning | Pages with zero inbound links |" — https://pypi.org/project/agent-wiki/

### 2.5 Címke-normalizálás

Itt egyértelműen **kétféle** megközelítés létezik, és mindkettőre találtam példát:

**Determinisztikus (LLM nélküli)**: `engram-lite` (GitHub, T1) — explicit „no LLM, no network", morfológiai szabályokkal (egyes/többes szám, toldalék-család, rövidítés-illesztés):

> „Deterministic tag extraction at write time — no LLM, no network. … The vocabulary is the union of every registered profile's scope_tags plus tags already present in the store — so tagging improves as profiles are registered, and stays consistent (no synonym drift…)" — https://github.com/engrammemory-labs/engram-lite/blob/main/src/engram/core/tags.py

ThreatConnect vállalati platform is szabály-alapú, felügyelt szinonima→fő-címke leképezéssel (T2, hivatalos dokumentáció):

> „System Administrators can create Tag normalization rules in ThreatConnect® that convert one or more synonymous Tags to a main Tag." — https://knowledge.threatconnect.com/docs/tag-normalization

Formális szabvány is létezik erre (ANSI/NISO Z39.19-2005, T1):

> „Vocabulary control is accomplished by three principal methods: defining the scope, or meaning, of terms; using the equivalence relationship to link synonymous and nearly synonymous terms; and distinguishing among homographs." — https://www.anzsi.org/wp-content/uploads/2019/05/z39-19-2005r2010.pdf

**LLM-alapú kontraszt-példa** (nem determinisztikus — csak összehasonlításként említve): `marginalia` (Shenmintao, T1 forráskód) kifejezetten LLM-hívással azonosít szinonimacsoportokat: „LLM-driven controlled-vocabulary maintenance. Per facet, asks the LLM to identify synonym groups…" — https://github.com/shenmintao/marginalia/blob/340900c8/src/marginalia/tasks/handlers/normalize_tags.py — ez tehát NEM tartozik az LLM-mentes kategóriába, csak azt mutatja, hogy ugyanarra a problémára létezik LLM-es és LLM nélküli megoldás is.

### 2.6 Ellentmondás-jelölés LLM nélkül — van ilyen?

**IGEN, legalább két független, önálló megvalósítás található:**

1. **mimir-mem-core**: koszinusz-hasonlóság + negáció-egyezés heurisztika, sosem automatikus feloldás: „contradiction flagging (high similarity + negation mismatch) — reported to the human, never auto-resolved" (l. 2.1 pont, idézet forrása uo.), saját teszttel is igazolva: „`contradictions_flagged_not_resolved`" (uo.).
2. **open-second-brain reconcile fázis**: strukturális jelalak szerinti doménosztályozás (claims/entity/decisions/source-freshness), „No LLM fan-out" (l. 1.2 pont).

Mindkettő közös vonása: a *jelölés* determinisztikus (küszöb/mintaillesztés alapú), de a *feloldás* — egy szűk, egyértelmű kivétellel (open-second-brain „source-freshness" eset) — emberi döntésre vár, sosem automatikus egyesítés.

---

## 3. Mérések: determinisztikus szabály vs. LLM-alapú konszolidáció

### 3.1 A „78–94,8% vs. 54%" állítás forrása — AZONOSÍTVA ÉS ELLENŐRIZVE

**Elsődleges forrás**: Vikas Reddy, Sumanth Reddy Challaram: „Reliable Post-Retrieval Assembly for Agent Memory: Separating Evidence Extraction from Policy Execution" (v1 címe: „Don't Ask the LLM to Track Freshness: A Deterministic Recipe for Memory Conflict Resolution"), arXiv:2606.01435, benyújtva 2026-05-31, v2: 2026-08-02, **elfogadva posztereként a COLM 2026 Lifelong Agent Workshopra** (T1, arXiv + workshop-elfogadás).

A feladat: MemoryAgentBench (MAB) FactConsolidation (FC-SH = single-hop), ahol a tényeket sorszámozzák, és a szabály ki van mondva a promptban („newer facts have larger serial numbers"). A cikk szó szerint:

> „HippoRAG-v2 reaches 54.0% on single-hop, BM25 reaches 48.0%, Mem0 / Contriever 18.0%, and Zep / Graphiti … scores 7.0% on FC-SH…" — https://arxiv.org/html/2606.01435v1

> „Combined with semantic candidate extraction, this produces three results: **78.0% on FC-SH with gpt-4o-mini, 94.8% on FC-SH with gpt-4o**, and 30.2% on FC-MH (gpt-4o-mini, rising to 51.5% with a gpt-4o backbone)…" — https://arxiv.org/html/2606.01435v1

A determinisztikus szabály maga: „structured candidate extraction followed by deterministic aggregation (**Python max over the extracted candidates**)" — https://arxiv.org/html/2606.01435v1 — vagyis nem tanult modell, hanem egy egyszerű `max(serial)` Python-függvény dönt a konfliktusfeloldásról a jelöltek kinyerése után.

**Két független megerősítő forrás** (a `_kozos.txt` előírása szerint):

1. Az eredeti MemoryAgentBench-cikk (Hu, Wang, McAuley — más szerzők, UC San Diego, ICLR 2026, T1, arXiv:2507.05257) saját táblázatában is 54,0-et közöl a HippoRAG-v2 FactConsolidation-SH oszlopában: „HippoRAG-v2 | 76.0 | 66.0 | 50.7 | 67.6 | 65.1 | 61.4 | 10.2 | 35.8 | 14.6 | 57.7 | 36.2 | **54.0** | 5.0 | 29.5 | 41.6" — https://arxiv.org/html/2507.05257v2
2. A MemoryAgentBench hivatalos GitHub-repója (HUST-AI-HYZ/MemoryAgentBench, T1) ugyanezt a benchmarkot és eredménytáblát tárolja forráskódként/adatként, függetlenül a Reddy–Challaram cikktől: https://github.com/hust-ai-hyz/memoryagentbench

Ez a három forrás (a cikk maga + két, tőle független szerzőségű/eredetű forrás) egybehangzóan igazolja: **legjobb LLM-alapú (HippoRAG-v2, RAG+LLM-architektúra) = 54,0%; determinisztikus max(serial)-szabály (gpt-4o-mini extrakcióval) = 78,0%; (gpt-4o extrakcióval) = 94,8%.** Ez pontosan megfelel a korábbi kutatásunkban szereplő „78–94,8% vs. 54%" számoknak.

**Fontos finomítás/önkorrekció a cikk v2 verziójában** (l. Ellentmondások szakasz): a szerzők saját, célzottabb ablációja szerint a nyereség NAGY RÉSZE nem magából a determinisztikus végrehajtóból, hanem az „evidence extraction" és a „policy execution" szétválasztásából (architektúra) származik:

> „A targeted comparison using the same extraction setup shows that changing only the final policy executor contributes **2.0 pp on average and 0 pp at 262K**. Most of the gain therefore comes from separating evidence identification from final policy execution **rather than from the freshness operator itself**." — https://arxiv.org/abs/2606.01435 (v2 absztrakt)

Egy másik kereszt-teszten (LongMemEval, valós időbélyegekkel) a determinisztikus `max(timestamp)` NEM verte meg szignifikánsan az LLM-alapú ítéletet:

> „A LongMemEval check finds no significant overall advantage (26/45 versus 29/45; paired exact McNemar p=0.45), bounding the result to current-value questions with explicit version metadata." — https://arxiv.org/abs/2606.01435 (v2 absztrakt)

### 3.2 DFM-Fusion / LoCoMo mérés — FORRÁS MEGBÍZHATÓSÁGA KÜLÖN JELÖLVE

Találtam egy másik, hasonló témájú mérést is: „Deterministic Memory Fusion for Long-Horizon Conversational Agents" (DFM-Fusion), Analemma Research, publikálva 2026-03-02:

> „On the LoCoMo benchmark, DFM-Fusion achieves 106.4% gap recovery on multi-hop F1 (18.72 vs 18.63, p=0.864), demonstrating statistical equivalence to LLM-guided fusion while eliminating all 226 fusion-related LLM calls per run. The approach provides 5.23× speedup in memory maintenance operations…" — https://analemma.ai/papers/9ebcbb0d-faaa-41f6-a372-9ed018212e6d/

**Fontos megbízhatósági figyelmeztetés**: az „Analemma" / „FARS" (Fully Automated Research System) egy **teljesen automatizált, emberi beavatkozás nélkül futó AI-kutatórendszer**, amely önállóan generál hipotézist, futtat kísérletet és ír cikket:

> „FARS (Fully Automated Research System) is an end-to-end AI research system that operates at scale. It is designed to autonomously perform the complete research workflow—including ideation, planning, experimentation, and paper writing—**without human intervention during execution**." — https://analemma.ai/blog/introducing-fars/

A rendszert bemutató saját arXiv-cikk (2606.31651, T1 az önjellemzésre nézve) is megerősíti, hogy a nagy nyilvános teszt „166 complete research papers"-t termelt, és utólagos, önkéntes emberi lektorálásnak vetették alá a korpusz egy részét — de ez nem klasszikus, publikálás előtti szakmai lektorálás:

> „In its first public deployment, FARS produced 166 complete research papers spanning 67 fine-grained AI/ML topics … We evaluate this corpus with 282 structured reviews from volunteer reviewers covering 140 papers…" — https://arxiv.org/html/2606.31651v2

**Nem sikerült független (Analemmától/FARS-tól eltérő szerzőségű) forrást találni**, amely a DFM-Fusion 106,4%/5,23×-os állítását megerősítené vagy cáfolná — ezért ezt az adatot **csak tájékoztató jelleggel, erős fenntartással** közlöm, NEM a fő bizonyítékként a determinisztikus-vs-LLM kérdésben. „NINCS FORRÁS" a független megerősítésre.

### 3.3 Egyéb, kevésbé közvetlen mérési adatok

- Az open-second-brain `o2b search restamp` funkciója „dry-run by default, refusing by name when a real model or dimension disagreement would make the repair cost money" (v1.52.0) — ez inkább biztonsági, mint pontossági mérés.
- A wiki-lint eszközök (2.4 pont) egyike sem közöl kvantitatív precision/recall számot a determinisztikus ellenőrzésekre — ezekre **NINCS FORRÁS** számszerű hibaarányra.
- A tag-normalizálási eszközök közül a `fairly` (PyPI) csomag közöl V-measure-alapú validációt saját klaszterezési küszöbeire („funder/subject 1.00, publisher 0.99, affiliation 0.96; rights 0.82"), de ez metaadat-mezőkre (kiadó, affiliáció) vonatkozik, nem memória-bejegyzésekre, és a forrás (PyPI leírás) T2 minőségű, független megerősítést nem találtam rá — https://pypi.org/project/fair-ly-accurate/

---

## 4. Jelzés (javaslat) vs. automatikus írás/törlés — csoportosítás

### 4.1 Csak JELEZNEK, emberi döntésre várnak

| Technika/rendszer | Mit jelez | Forrás |
|---|---|---|
| open-second-brain: reconcile (nem source-freshness esetek) | ellentmondó preferenciák → „open question" | „everything else surfaces as an operator-facing open question instead of a forced merge" (v0.21.0) |
| open-second-brain: `brain hygiene scan` | vitatott tények, közel-duplikátum szabályok, elavult levezetett oldalak, sosem-visszahívott memóriák | „surfaces contested facts, near-duplicate rules, stale derived pages, and never-recalled memories; `apply` executes only the findings you select" (README) |
| open-second-brain: szemantikus dedup | „nominates and never drops" | v1.40.0 |
| open-second-brain: `brain co-occurrence` | kapcsolat-élek javaslata | „proposes relationship edges … All deterministic, all read-only or **suggestion-only**." (README) |
| mimir-mem-core: ellentmondás-jelzés (2. lépés) | koszinusz+negáció-egyezés | „reported to the human, never auto-resolved" |
| wiki-lint / kb-lint / agent-wiki / health_lint.py | törött linkek, árva oldalak, elavult állítások, hiányzó keresztlinkek | l. 2.4 pont idézetei; a legtöbb csak riportot ír, `--fix` explicit kapcsoló nélkül nem módosít |
| llmwiki-tooling (`links fix`) | link-javaslatok | „dry-run by default, --write to apply" |
| AutoMem: „creative" (REM-szerű) feladat | nem-triviális asszociációk felfedezése | „discovers non-obvious connections between memories by randomly sampling the graph" |

### 4.2 Maguk ÍRNAK/TÖRÖLNEK (automatikusan, de biztonsági hálóval)

| Technika/rendszer | Mit ír/töröl automatikusan | Biztonsági háló |
|---|---|---|
| open-second-brain: dream — synthesize/heal | unconfirmed→confirmed promóció, elavult preferenciák retired/-be mozgatása | pre-run snapshot + SHA-256, `--dry-run`, rollback, opcionális evidence-küszöb „gate" a törléshez |
| open-second-brain: reconcile — source-freshness eset | egyetlen automatikus feloldási eset | mindig naplózva (`reconcile` log event), sosem küszöb alatti írás |
| mimir-mem-core: 1. lépés (near-dup merge) | régebbi csomópont „superseded", SOSEM törölve | `dry_run` flag, `pinned` csomópont kihagyva |
| mimir-mem-core: 4. lépés (decay archival) | alacsony erősségű, régóta érintetlen memória „soft-deleted" | reverzibilis (`meta.archived = true`, nem tényleges törlés) |
| AutoMem: forget/decay task | relevancia-pontszám automatikus frissítése; alacsony relevancia esetén archiválás/törlés | alapból `archive_threshold`/`delete_threshold` = 0,0 (KIKAPCSOLVA); 90 napos védelmi periódus; `importance >= 0.7` védelem |
| agentos ConsolidationLoop: prune/merge/compact | gyenge nyomok soft-delete-je, közel-duplikátumok egyesítése, epizodikus→szemantikus átsorolás | küszöbök konfigurálhatók (`pruneThreshold`, `mergeThreshold`) |
| Unforget | duplikátum-egyesítés, fakulás, 30 napnál régebbi feldolgozatlan „raw" törlése | LLM nélkül is fut ez a rész; csak a „promotion" (raw→insight) igényel LLM-et |
| ThreatConnect tag-normalizálás | engedélyezéskor MINDEN meglévő szinonima-címke azonnal, visszavonhatatlanul átírásra kerül | explicit figyelmeztetés: „The conversion process cannot be stopped once started, is irreversible" |
| engram-lite `canonicalize()`/`extract()` | címkék automatikus kanonikus alakra hozása íráskor | csak ismert szókincsre alkalmazza; ismeretlen token változatlan marad |
| kb-lint `--fix` | frontmatter-alapértékek, fájlnév-átnevezés, index-frissítés | csak explicit `--fix` (opcionálisan `--fix --dry-run` előnézettel) |

**Összegzés a 4. kérdésre**: a determinisztikus rendszerek túlnyomó többsége **rétegzett** modellt követ — a *felismerés* (dedup-jelölt, ellentmondás, elavultság) szinte mindig determinisztikus és olcsó, de a *tényleges írás/törlés* vagy (a) alapból csak jelzésre korlátozódik (open-second-brain hygiene/co-occurrence, wiki-lint családok), vagy (b) automatikusan megtörténik, de mindig snapshot/rollback/dry-run/reverzibilitás mögé van rejtve (open-second-brain dream, mimir-mem-core, AutoMem). Kizárólag a klasszikus „irreverzibilis és automatikus" mintára (pl. ThreatConnect tag-egyesítés) találtam kevesebb példát a memóriarendszerek körében — ott inkább explicit figyelmeztetés kíséri.

---

## Ellentmondások

1. **A dream-fázisok „valódisága"**: a v0.21.0 (2026 nyara) kiadás dokumentációja ötlépéses, elnevezett „pipeline"-ként mutatja be a dream-folyamatot, míg a v1.40.0 (2026-07-27) saját visszaellenőrzése kimondja, hogy ez „**a reporting label with no callable units**" — azaz a korábbi (és a jelen kutatás elején szereplő) leírás, miszerint öt *lépés* van, félreérthető: valójában öt *napló-checkpoint* egyetlen algoritmus felett. Ez nem tényleges forrás-ellentmondás (a két kiadás konzisztens egymással, csak az egyik pontosítja/korrigálja a lehetséges félreértést), de fontos a „lépésenként mit csinál" kérdés pontos megválaszolásához.
2. **A 78–94,8% vs. 54% eredmény jelentése**: a Reddy–Challaram cikk v1 verziója (címe: „Don't Ask the LLM to Track Freshness") sugallja, hogy a determinisztikus `max(serial)` szabály önmagában felelős a nagy pontosság-növekedésért. A cikk saját v2 revíziója (átcímezve: „Reliable Post-Retrieval Assembly…") ezt élesen finomítja: a puszta végrehajtó-csere hatása mindössze **+2,0 pp átlagosan és 0 pp 262K-nál** — a nyereség zöme az „evidence extraction" és „policy execution" szétválasztásából, nem a determinizmusból ered. A két verzió között tehát valódi hangsúly-ellentmondás van ugyanazon szerzőktől, amit a cikk maga korrigált.
3. **DFM-Fusion (Analemma/FARS) státusza**: a publikáció formailag „cikknek" néz ki (absztrakt, DOI-szerű azonosító, „Peer Review" link), valójában egy emberi felügyelet nélkül publikáló AI-rendszer terméke. Ez nem forrtreate-ellentmondás más forrásokkal, de fontos figyelmeztetés a megbízhatóságra nézve — ezért nem soroltam egy szintre a Reddy–Challaram arXiv-cikkel.

## Amire NINCS forrás

- A DFM-Fusion (Analemma/FARS) 106,4% gap-recovery és 5,23×-os gyorsulási állítására **nem található független (Analemmától eltérő szerzőségű) megerősítés vagy cáfolat**.
- Az open-second-brain wiki-lint-szerű családjára (kb-lint, agent-wiki, health_lint.py stb.) **nincs publikált kvantitatív pontosság/hibaarány-mérés** (pl. precision/recall a törött link- vagy árva oldal-felismerésre) — ezek az eszközök determinisztikus szabályok, amelyek helyessége triviálisan bizonyítható (a link vagy létezik, vagy nem), ezért nem is jellemző rájuk empirikus kiértékelés, de expliciten nem találtam ilyet.
- A címke-normalizálási technikák (Jaro–Winkler-küszöb 0,85–0,9 stb.) mögött **nincs</br> nyilvános, harmadik fél általi validáció** a konkrét küszöbértékek helyességére a memória-/agent-kontextusban (a `fairly` csomag V-measure-adata metaadat-mezőkre vonatkozik, más tartomány).
- Nem található közvetlen, harmadik féltől származó forrás arra, hogy az open-second-brain v1.54.0-nál **pontosan hány éles telepítés** fut, vagy hogy a `dream` motor éles környezetben mért teljesítmény-/hibaadatai nyilvánosak lennének (csak a beépített teszt-számok — pl. „7614 tests pass" — ismertek, ezek nem produkciós mérések).

---

# SQ03 — Mennyire kiszámítható az LLM-alapú memória-konszolidáció eredménye?

**Módszer:** Az Exa keresőeszközt (`mcp__Exa__web_search_exa`, `mcp__Exa__web_fetch_exa`) használtam kizárólagos webes keresőként, a `_kozos.txt` előírása szerint. A `deep-web-research` skill alapelveit (elsődleges forrás, idézet + URL, kereszt-ellenőrzés) követtem degradált (nem-alügynökös) módban: egy munkamenetben, célzott, párhuzamos kereséssorozatokkal dolgoztam, mert a skill nem tudott önálló alügynököt indítani ebben a környezetben.

**Fontos időbeli megjegyzés:** a mai dátum 2026-09-24. Több itt idézett cikk (pl. Thinking Machines Lab blogja, a MemoryAgentBench-re épülő „determinisztikus konfliktusfeloldás" cikkek, a „Useful Memories Become Faulty" ICML 2026-os cikk) 2025 végén–2026 folyamán jelent meg, tehát a modell tudásvágásán (2026 január) túli, valós, ellenőrzött friss anyag — nem kitaláció, hanem az Exa-találatok tartalma.

## Rövid válasz

A kérdést két, egymástól **teljesen független** dimenzióra kell bontani, és mindkettőre igen a válasz: az LLM-alapú memória-konszolidáció **nem kiszámítható**, de két különböző okból. (a) **Futásonkénti nem-determinizmus**: OpenAI és Anthropic hivatalos dokumentációja egyaránt kimondja, hogy temperature=0 mellett sem garantált azonos kimenet; a Thinking Machines Lab (2025.09.10) technikai jelentése ezt a „batch-invariancia" hiányára vezeti vissza (a szerver terhelése — nem a promptod — befolyásolja a numerikus eredményt), és megmutatta, hogy ez elméletileg kiküszöbölhető, gyakorlatilag azonban jelentős teljesítményáldozattal jár, és éles termelési rendszerben (mem0, OpenAI, Anthropic API) nincs bekapcsolva. (b) **A döntés minősége** (akkor is instabil, ha a kimenet reprodukálható lenne): a mem0 saját GitHub issue-i és a saját dokumentációja szerint az LLM annyira megbízhatatlanul választotta az ADD/UPDATE/DELETE/NOOP műveletet, hogy a mem0 2026-ban **kivette** ezt a döntést a pipeline-ból (ADD-only architektúra). A tulajdonos által említett számok — 54% (legjobb LLM-es rendszer), 78–94,8% (determinisztikus `max(serial)` szabály), legfeljebb 7% (többlépéses/multi-hop) — pontosan visszakereshetők: elsődleges forrásuk a MemoryAgentBench (Hu, Wang & McAuley, ICLR 2026) FactConsolidation feladata, illetve az arra épülő „Don't Ask the LLM to Track Freshness" / „Reliable Post-Retrieval Assembly for Agent Memory" cikk (arXiv:2606.01435, COLM 2026 workshop). Egy 2026 májusi, ICML 2026-ra elfogadott cikk (arXiv:2605.12978) pedig kimutatta, hogy a konszolidáció idővel **ronthatja** a memóriát: egy GPT-5.4-alapú ügynök 19, korábban 100%-ban megoldott ARC-AGI feladat közül a konszolidáció után csak 54%-ot old meg helyesen — még akkor is, ha a bemenet (a konszolidálandó megoldás) hibátlan volt.

---

## 1. Futásonkénti determinizmus (ugyanaz a bemenet → más kimenet?)

### 1.1 Gyártói állítások

**OpenAI**, hivatalos dokumentáció:
> „Chat Completions are non-deterministic by default (which means model outputs may differ from request to request). That being said, we offer some control towards deterministic outputs by giving you access to the `seed` parameter and the `system_fingerprint` response field. […] Determinism is not guaranteed, and you should refer to the `system_fingerprint` response parameter to monitor changes in the backend."
(https://developers.openai.com/api/docs/guides/advanced-usage és https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create/, T1, Exa search)

Fontos: a `seed` paraméter az aktuális OpenAI API-referenciában **„Deprecated"** jelzéssel szerepel, és az újabb Responses API-ból ki is került a több párhuzamos generálást engedélyező `n` paraméter is (https://developers.openai.com/api/docs/guides/migrate-to-responses, T1). Vagyis a gyártó saját eszköze a determinizmus felé is visszaszorulóban van, nem bővülőben.

Az Azure OpenAI dokumentáció ugyanezt kártyát erősíti meg egy második, független Microsoft-forrásból:
> „Determinism isn't guaranteed with reproducible output. Even in cases where the seed parameter and `system_fingerprint` are the same across API calls it's currently not uncommon to still observe a degree of variability in responses. Identical API calls with larger `max_tokens` values, will generally result in less deterministic responses even when the seed parameter is set."
(https://learn.microsoft.com/en-us/azure/foundry-classic/openai/how-to/reproducible-output, T1, Exa search)

**Anthropic**, hivatalos dokumentáció (glosszárium):
> „Users may encounter non-determinism in APIs. Even with temperature set to 0, the results will not be fully deterministic and identical inputs may produce different outputs across API calls. This applies both to Anthropic's first-party inference service and to inference through third-party cloud providers."
(https://platform.claude.com/docs/en/about-claude/glossary, T1, Exa search)

Sőt, Anthropic legújabb modelljeinél (Claude 4.7+) már **meg sem lehet** temperature-t állítani:
> „The `temperature`, `top_p`, and `top_k` sampling parameters are not supported on Claude 4.7 and later models and Claude Mythos Preview. Setting them to a non-default value returns a 400 error."
(https://platform.claude.com/docs/en/build-with-claude/working-with-messages, T1, Exa search)

→ A „temperature=0 = determinizmus" elképzelés a legfrissebb Anthropic-modelleken már fogalmilag sem értelmezhető paraméterszinten.

### 1.2 A műszaki ok: batch-invariancia hiánya (Thinking Machines Lab, 2025.09.10)

A Thinking Machines Lab (Mira Murati új laborja) „Defeating Nondeterminism in LLM Inference" c. technikai jelentése elsőként adott mechanisztikus magyarázatot arra, miért nem determinisztikus a kimenet temperature=0 mellett sem:

> „As it turns out, our request's output does depend on the parallel user requests. Not because we're somehow leaking information across batches — instead, it's because our forward pass lacks 'batch invariance,' causing our request's output to depend on the batch size of our forward pass." […] „the primary reason nearly all LLM inference endpoints are nondeterministic is that the load (and thus batch-size) nondeterministically varies! This nondeterminism is not unique to GPUs — LLM inference endpoints served from CPUs or TPUs will also have this source of nondeterminism."
(https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/, T1 — elsődleges, iparági technikai jelentés, Exa search)

A cikk azt is bemutatta, hogy elméletileg **kiküszöbölhető**: nyílt forráskódú „batch-invariant" kernelekkel (https://github.com/thinking-machines-lab/batch_invariant_ops, T1) vLLM alatt 1000 azonos (temperature=0) kérésből az alapértelmezett beállítással **18 különböző** kimenetet kaptak, a batch-invariant módban pedig **1/1000 egyedi kimenetet** (azaz mind egyforma volt) — de ez teljesítményáldozattal jár, és nem alapértelmezett egyik nagy szolgáltatónál sem.

Ezt két független, egymástól elkülönült forrás is megerősítette/összefoglalta:
- Simon Willison (elismert, széles körben idézett iparági kommentátor) blogja: „the primary reason nearly all LLM inference endpoints are nondeterministic is that the load (and thus batch-size) nondeterministically varies!" (https://simonwillison.net/2025/Sep/11/defeating-nondeterminism/, T3 — kommentár, de az elsődleges forrást pontosan idézi, Exa search)
- Egy másik független összegzés (Bhakthan, Substack) konkrét mérőszámot is közöl a cikkből: „Empirical result: 1000 temperature-0 completions with standard kernels produced 80 unique outputs; batch-invariant kernels produced 1000/1000 identical outputs." (https://bhakthan.substack.com/p/defeating-nondeterminism-in-llm-inference, T3, Exa search) — a két másodlagos forrás kicsit eltérő számot közöl (18 vs. 80 egyedi kimenet 1000-ből); ez valószínűleg két különböző kísérletre/ábrára utal a cikkben, de mindkettő ugyanazt a minőségi állítást támasztja alá: alapértelmezett kernellel **tucatnyi–száznyi eltérő kimenet** születik 1000 azonos, temperature=0 hívásból.

**Következtetés a rendszerre nézve:** mivel a projekt szándéka szerint a rendszerben LLM-generálás egyáltalán nincs (csak beágyazó modell fut), a fenti futásonkénti nem-determinizmus **közvetlenül nem érinti a saját szervert** — de közvetve igen, mert a hívó ágens (Claude, Codex), amely a bejegyzéseket írja és a „dream"-hez esetlegesen szükséges LLM-hívásokat kezdeményezi, ennek a nem-determinizmusnak van kitéve.

---

## 2. A memória-frissítés minőségi problémái (döntési hibaarány, drift)

### 2.1 A mem0 ADD/UPDATE/DELETE/NOOP mechanizmusa és a saját GitHub-jén dokumentált hibái

A Mem0 architektúra (arXiv:2504.19413, Chhikara et al. 2025, T1 preprint, széles körben idézett) az alábbi módon dönt:

> „The LLM itself determines which of four distinct operations to execute: ADD for creation of new memories when no semantically equivalent memory exists; UPDATE for augmentation of existing memories with complementary information; DELETE for removal of memories contradicted by new information; and NOOP when the candidate fact requires no modification to the knowledge base. Rather than using a separate classifier, we leverage the LLM's reasoning capabilities to directly select the appropriate operation."
(https://arxiv.org/abs/2504.19413, T1, Exa fetch/search)

**LLM-alapú rendszer, ember jóváhagyása nélkül ír** (a döntést az LLM hozza, alapértelmezésben nincs emberi visszaigazolási lépés az ADD/UPDATE/DELETE végrehajtása előtt).

A mem0 saját GitHub-issue-i konkrét hibaeseteket dokumentálnak:

- **#1674 „adding same memory twice deletes old memory"**: egy *szó szerint azonos* új bejegyzés hozzáadásakor az LLM DELETE műveletet hívott a régi (helyes) bejegyzésre. A mem0 fejlesztője (Dev-Khant) válasza:
> „@Dev-Khant just observed when using *gpt-4o-mini* the delete operation is happing and switching to *gpt-4o* fixed this, but this is not a concrete solution as gpt-4o can also hallucinate and delete memory" […] „Yes you are right, we will have to improve the prompts here."
(https://github.com/mem0ai/mem0/issues/1674, T1 — elsődleges, első kézből, a fejlesztőtől, Exa search)

- **#3931 „KeyError in temp_uuid_mapping during async UPDATE operation"**: a jelenség „since January across multiple mem0 versions" visszatérő; egy felhasználó megjegyzése:
> „We're implementing a retry-on-KeyError workaround on our side since the root cause is non-deterministic (LLM hallucinating out-of-range temp IDs in the update prompt response)." […] „We just cleaned up 57 duplicate memories from our production database that had built up over time."
(https://github.com/mem0ai/mem0/issues/3931, T1, Exa search)

- **#4708 (JS SDK) „updateMemory/deleteMemory called with undefined ID when LLM returns out-of-range action.id"**: az LLM hallucinált azonosítót ad vissza, emiatt a frissítés/törlés **csendben elveszik** (adatvesztés hibaüzenet nélkül). A mem0 csapata válaszul „additive-only" architektúrára állt át — lásd lejjebb.
(https://github.com/mem0ai/mem0/issues/4708, T1, Exa search)

- **#3928 „delete_all() incorrectly calls reset(), deleting memories of all users instead of filtered ones"**: nem LLM-hiba, hanem kódhiba, de ugyanabba a kategóriába tartozik (a memóriakezelő automatizmus véletlenül minden felhasználó minden memóriáját törölte). Javítva.
(https://github.com/mem0ai/mem0/issues/3928, T1, Exa search)

### 2.2 A mem0 saját válasza: kivenni az LLM-et az UPDATE/DELETE döntésből

A fenti hibák hatására a mem0 2026-ban átállt egy **„ADD-only"** architektúrára — ez maga is erős, elsődleges (a gyártótól származó) bizonyíték amellett, hogy az LLM-alapú UPDATE/DELETE-döntés a gyakorlatban megbízhatatlannak bizonyult:

> „The key architectural decision is **ADD-only extraction**. New facts are stored alongside old ones — nothing is overwritten or deleted. When information changes, both the old and new facts survive. This preserves temporal context and eliminates information loss from premature consolidation." […] „**Single-pass ADD-only extraction** -- one LLM call, no UPDATE/DELETE. Memories accumulate; nothing is overwritten."
(https://github.com/mem0ai/mem0/blob/0fbbb2f5/docs/core-concepts/memory-evaluation.mdx és a mem0 hivatalos README-je, T1 — a gyártó saját dokumentációja, Exa search)

Ezt egy független, technikai elemzés is megerősíti:
> „OSS v3 removed the older second LLM pass that decided whether a candidate should be added, updated, or deleted. […] The current write path is approximately […] ADD-only. […] it shifts responsibility to retrieval and lifecycle policy."
(https://cubxxw.com/projects/mem0/, T3 — független technikai blog, Exa search)

Ez közvetlenül releváns a saját tervezett rendszerre nézve: **egy nagy, sokat idézett, kereskedelmi LLM-alapú memóriarendszer a gyakorlati tapasztalat alapján kivonult az LLM-alapú UPDATE/DELETE-döntésből**, és helyette additív tárolást + utólagos, nem-LLM-alapú (lejáratú/rangsorolási) szűrést vezetett be.

### 2.3 Közösségi audit a mem0 memóriaminőségéről (nem hivatalos, de konkrét adatpont)

Egy GitHub-issue (#4573) egy felhasználói audit eredményét közli — **T2/T3, nem hivatalos, egyetlen fél saját mérése**, de mivel a `_kozos.txt` szerint minden NINCS-FORRÁS helyzetet jelezni kell, és itt van konkrét szám, idézem, jelezve a forrás gyengeségét:

> „224 entries survived the full process. Out of 10,134. That's 97.8% junk across the entire collection. And of those 224 survivors, 186 had to be deleted and rewritten from scratch because the originals were partial or malformed."
(https://github.com/mem0ai/mem0/issues/4573, T2/T3 — közösségi, nem validált, egyetlen telepítésből származó adat, Exa search)

Ugyanez az issue egy második, releváns állítást is tartalmaz a LOCOMO-benchmark reprodukálhatóságáról:
> „Mem0's 66.9% on LOCOMO is self-reported, already contested by Zep, and someone on #3944 couldn't reproduce it via the platform API at all (got 0.20, found the system injecting current dates instead of dataset timestamps)."
(ugyanaz az URL, T2/T3, Exa search)

**Ezt a konkrét reprodukálhatósági állítást nem tudtam független harmadik forrással megerősíteni** — ezért „NINCS FÜGGETLEN MEGERŐSÍTÉS" jelzéssel szerepeltetem, nem tényként.

### 2.4 LongMemEval — „knowledge update" képesség mérése

A LongMemEval (ICLR 2025, Wu et al., arXiv:2410.10813, T1) az öt vizsgált képesség egyikeként kifejezetten a „knowledge update"-et definiálja:

> „Knowledge Updates (KU): Ability to recognize the changes in the user's personal information and update the knowledge of the user dynamically over time." […] „manual evaluations reveal that state-of-the-art commercial systems (such as GPT-4o) only achieve 30%∼70% accuracy in a setting much simpler than LongMemEvalS."
(https://arxiv.org/html/2410.10813v1, T1, Exa search)

A retrieval szint (megtalálja-e a releváns munkamenetet) a knowledge-update kategóriában viszonylag jó tud lenni (pl. egy harmadik fél reprodukciója 98,7–100% R@10-et mér — https://github.com/rohitg00/agentmemory, T3, nem hivatalos reprodukció), **de ez csak a visszakeresés, nem a helyes frissítési döntés mérőszáma** — ezt fontos külön választani.

### 2.5 LoCoMo (Maharana et al., ACL 2024) — összefoglalás → információvesztés

Az eredeti LoCoMo-cikk (arXiv:2402.17753, ACL 2024, T1) kifejezetten dokumentálja, hogy az összefoglalás-alapú (azaz konszolidációhoz hasonló) memória-reprezentáció rontja a minőséget:

> „using session summaries as context does not significantly improve the performance despite high recall accuracies, likely due to **loss of information during the conversion of dialogs to summaries**." […] „long-context LLMs can comprehend longer narratives, yet they are prone to generating hallucinations. […] LLMs can be easily misled into generating hallucinations when they are subjected to long contexts."
(https://arxiv.org/pdf/2402.17753 / https://aclanthology.org/2024.acl-long.747.pdf, T1, Exa search)

### 2.6 „Memory drift" — konszolidáció ronthatja a memóriát idővel (ICML 2026)

Ez a legerősebb, közvetlenül a kérdésre („rontja-e a konszolidáció a memóriát idővel") válaszoló, **lektorált** forrás, amelyet találtam: „Useful Memories Become Faulty When Continuously Updated by LLMs" (Dylan Zhang, Yanshan Lin, Zhengkun Wu, Yihang Sun, Bingxuan Li, Dianqi Li, Hao Peng; UIUC + Tsinghua; **elfogadva az ICML 2026-ra**, a szerző saját weboldala szerint; arXiv:2605.12978, 2026.05.13):

> „Yet we find that such consolidated memories produced by today's LLMs are often faulty even when derived from useful experiences. As consolidation proceeds, memory utility first rises, then degrades, and can fall below the no-memory baseline. More surprisingly, even when consolidating from ground-truth solutions, GPT-5.4 fails on 54% of a set of ARC-AGI problems it had previously solved without memory."
(Abstract, https://arxiv.org/abs/2605.12978 és https://arxiv.org/pdf/2605.12978, T1 — ICML 2026-ra elfogadott, lektorált cikk, Exa fetch/search)

A törzsszöveg pontosabban:
> „The clearest case isolates the consolidation step from any input-side excuse: GPT-5.4 first solves a set of ARC-AGI problems at 100% accuracy with no memory; after consolidating from ground-truth solutions to those very problems, it then fails on 46% of them (Fig. 2)." […] „Each consolidation step is a lossy rewrite of the memory store: useful details are dropped, spurious rules are introduced, and once-helpful abstractions drift away from the underlying task structure."
(https://arxiv.org/html/2605.12978v1, T1, Exa fetch)

A cikk három konkrét hibamechanizmust azonosít, amelyek közvetlenül releváns megfontolások a tervezett „dream" funkcióhoz:
> „First, agents misgroup experiences before abstracting them, pooling episodes that do not share underlying structure. Second, even when grouping is correct, abstraction can strip the applicability conditions of a lesson, so that overgeneralized entries interfere with neighboring tasks. Third, when the input stream is narrow, abstraction overfits to seen instances."
(https://inquiringlines.com/papers/2605.12978/, T3 — másodlagos összefoglaló, de a cikk szövegét pontosan idézi, Exa search)

A cikk fő ajánlása pontosan a projekt LLM-mentes determinisztikus iránya felé mutat:
> „Practically, robust agent memory should treat raw episodes as first-class evidence and gate consolidation explicitly rather than firing it after every interaction. […] until agents can control when and how to consolidate experience, continuously updated textual memory should be treated not as a reliable engine of self-improvement, but as a fragile mechanism that can make more experience produce worse memory."

**Fontos módszertani megjegyzés / belső ellentmondás a forrásban:** az absztrakt „fails on 54%"-ot ír, míg a törzsszöveg kétszer is „fails on 46%" / „down to 54%" formában, egymással konzisztensen fogalmaz (100%→54% pontosság = 46%-os hibaarány). Az absztrakt megfogalmazása („fails on 54%") ezzel nem konzisztens — valószínűleg fogalmazási pontatlanság az absztraktban. A helyes, törzsszövegben kétszer is alátámasztott értelmezés: **100%-ról 54%-ra esett a pontosság ugyanazokon a feladatokon, tehát a hibaarány 46%**. Ezt Ellentmondások alatt is jelzem.

Ezt egy független, kereskedelmi AI-hírportál másodlagos elemzése is megerősíti (nem elsődleges forrás, de független szemtől):
> „After consolidation, the agent fails on 54% of those same problems. The trajectories are clean — they contain correct solutions. The failure is in the rewrite step." […] „an agent with fresh-only consolidation […] outperforms cumulative consolidation […] by +203 points."
(https://ai-beat.github.io/news/2026/05/memory-consolidation-agents/, T3, Exa search)

---

## 3. Ismert hibák, incidensek LLM-alapú konszolidációs funkciókban

### 3.1 Letta / sleep-time compute

A „sleep-time compute" koncepció eredeti forrása a Letta + UC Berkeley cikk (arXiv:2504.13171, T1):
> „In practice, this is achieved by prompting the model to generate a new context consisting of inferences about the existing context, which may be potentially useful for answering test-time queries."
(https://arxiv.org/abs/2504.13171, T1, Exa search)

**LLM-alapú, ember jóváhagyása nélkül ír** (a „sleep-time agent" önállóan írja át a „core memory"-t).

A Letta termékek (letta-code) GitHub-issue-i konkrét, súlyos memória-integritási hibákat dokumentálnak:

- **„MemFS git history repeatedly force-pushed by server, wiping agent memory" (letta-code #2203)**:
> „The Letta server repeatedly force-pushes a new git history to the agent's memfs repository, replacing the full agent memory with a small set of 'backfilled' blocks. This wipes all locally-committed memory files." […] „I had 79 files in my memfs repo […] built up over many sessions […] The server had replaced the entire history […] This cycle repeats — any push I make gets overwritten by the next server-side force push."
(https://github.com/letta-ai/letta-code/issues/2203, T1, Exa search)

- **„[Bug]: Cross-Session State Leakage via Persistent Core Memory Poisoning" (letta/letta #3388)**:
> „Because the server lacks a hard tear-down or atomic block-flushing mechanism between independent tasks on the same daemon, these malicious memory modifications are permanently written to the database. Consequently, the poisoned context permanently leaks into subsequent, independent evaluation runs."
(https://github.com/letta-ai/letta/issues/3388, T1, Exa search)

- **„Critical: Memory isolated per-agent; new sessions get blank slate" (letta-code #2666)**: strukturális tervezési hiba, nem véletlen adatvesztés, de közvetlenül releváns a projekt „projekt-szeparáció, de engedéllyel megosztható tudás" céljára — mutatja, hogy ez nem triviálisan megoldott probléma a piacon.
(https://github.com/letta-ai/letta-code/issues/2666, T1, Exa search)

### 3.2 ChatGPT memória-funkció — nem hivatalos, de számos felhasználói hibajelentés

**LLM-alapú rendszer** (OpenAI hivatalos leírása szerint az LLM dönt a memória-frissítésről), **ember jóváhagyása nélkül ír** alapértelmezésben. Ezek a fórumbejegyzések **T2/T3** — nem hivatalos OpenAI-megerősítések, hanem felhasználói panaszok az OpenAI Developer Community fórumon —, de mennyiségük és konzisztenciájuk miatt jelzés-értékűek:

> „Memory keeps deleting entries, and modifying them without permission or informing user." (2024-05, https://community.openai.com/t/my-gpt-4s-memory-has-disappeared/732911/1)

> „I have similar problems […] Memories are stored that you never added, for me it was: 'Enjoys playing chess and is working on improving their skills.'" (2025-01, https://community.openai.com/t/memory-issue-incorrect-data-added-possible-data-corruption/1108078)

> „it’s creating 'a memory' record every time but instead of saving the right information, it's saving some random previous one duplicated […] it is hallucinating on that, changing the content every time ever so slightly, and inventing details like 'Arena' or 'AI opponents' which are not part of the original memory or ever discussed." (2025-01, https://community.openai.com/t/chatgpt-memory-broken-at-the-moment/1108272/1)

> „Specifically, memory entries from one chat […] became incorrectly associated with another separate chat […] The assistant itself described this issue explicitly as a serious infrastructural bug ('cross-contamination of memories')." (2025-03, https://community.openai.com/t/memory-context-corruption-contradiction-in-chatgpt-gpt-4-5/1144222/1)

Ezek a bejegyzések **nem hivatalos OpenAI-visszaigazolások**, ezért nem tekinthetők megerősített, dokumentált hibáknak — de mint konzisztens, ismétlődő felhasználói panaszminta (több különböző dátumban, több különböző felhasználótól, hasonló tünetekkel: törlés, duplikáció, kontextus-keveredés, hallucinált tartalom), releváns adatpontok.

### 3.3 Claude/Claude Code — kontextus-összefésülés (compaction) hallucinációi

Fontos megkülönböztetés: ezek **nem** a claude.ai „memory" funkció (lásd 3.4), hanem a Claude Code hosszú munkameneteket automatikusan összefoglaló („compaction") mechanizmusának hibái — de mivel ugyanaz a mintázat (LLM összefoglal → hibás/kitalált tartalom kerül be → az kerül felhasználásra), közvetlenül releváns a „dream" tervezésére nézve. Mind **első kézből származó, hivatalos GitHub issue** (T1):

> „the assistant writing the summary can hallucinate a user instruction that never existed in the original conversation. After the context reset, the resumed assistant reads the summary and executes the fabricated instruction as if the user had actually typed it […] This is a silent data integrity bug in the compaction pipeline."
(https://github.com/anthropics/claude-code/issues/46602, T1, Exa search)

> „the summarizer had written: 'User approved the plan via ExitPlanMode' […] This was false. I never approved anything. […] Claude picked up the summarized session […] and continued implementing — writing and committing changes to three production files without my consent."
(https://github.com/anthropics/claude-code/issues/61721, T1, Exa search)

> „The model fabricated a complete user turn inside an assistant-role entry in the session log […] A fabricated message_id […] verified absent from Discord's message history […] The model then responded to its own fabricated turn as if it were real input from me."
(https://github.com/anthropics/claude-code/issues/46602 — komment egy másik előfordulásról, T1, Exa search)

> „the model silently fabricates structurally valid but fictitious metadata (addresses, IBAN, VAT UID, customer number) and writes them to the output file with full confidence. […] There were no error messages. The hallucination was silent."
(https://github.com/anthropics/claude-code/issues/22359, T1, Exa search)

> „This depends on context compaction timing, which is non-deterministic."
(ugyanaz az issue, T1)

Ez utóbbi mondat közvetlenül összeköti a két, a feladat által elkülönítendő jelenséget: itt a **nem-determinizmus** (mikor fut le az összefésülés) váltja ki a **rossz döntést** (kitalált adat) — a kettő a gyakorlatban gyakran összefonódik, még ha fogalmilag külön kérdés is.

### 3.4 Anthropic hivatalos claude.ai „memory" funkció — dokumentált, LLM-alapú, korlátozott emberi kontrollal

Ez a claude.ai valódi, hosszútávú memóriafunkciója (nem Claude Code). Hivatalos leírás:
> „Claude saves memory as a set of individual topics as you chat, rather than summarizing conversations after they end." […] „Claude uses a memory summary to capture all its memories in one place for you to view and edit. […] Claude will automatically summarize your conversations and create a synthesis of key insights across your chat history […] This synthesis is updated every 24 hours."
(https://support.anthropic.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context, T1, Exa search)

**LLM-alapú, alapértelmezésben ember jóváhagyása nélkül ír** (automatikus, 24 óránkénti szintézis), de a felhasználó utólag szerkesztheti/törölheti a témákat, és van „Reset memory" opció. A „Monthly recap" funkció esetében Anthropic saját maga is elismeri a pontatlanság lehetőségét:
> „Claude generates your recap's summary and topic breakdown from your chat history, so occasional inaccuracies can occur in the proportions or the narrative summary."
(https://support.claude.com/en/articles/15672559-see-your-monthly-recap, T1, Exa search)

Ez egy **gyártói (elsődleges) beismerés** arra, hogy az LLM-alapú összefoglalás/szintézis pontatlan lehet — közvetlenül releváns megerősítés a kérdésre.

Az API-oldali „memory tool" (`memory_20250818`) ezzel szemben **kliens-oldali, teljes mértékben az LLM (Claude) dönt** a fájlműveletekről:
> „The memory tool operates client-side: Claude requests file operations, and your application executes them. […] Claude only requests memory operations."
(https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool.md, T1, Exa search)

Itt Anthropic explicit módon **nem** tesz determinizmus- vagy megbízhatósági ígéretet a memóriaművelet-döntésekre — a dokumentáció kizárólag a mechanizmust írja le, minőségi garanciát nem ad.

---

## 4. A 78–94,8% / 54% / 7% számok elsődleges forrása

**Megerősítve, pontosan visszakereshető.** Az elsődleges lánc:

1. **MemoryAgentBench** (Hu, Wang & McAuley; arXiv:2507.05257; ICLR 2026-ra elfogadott — az ICLR proceedings link is megtalálható) vezette be a **FactConsolidation** feladatot, amely a „Selective Forgetting" kompetencia alá tartozik:
> „To assess whether an agent can forget out of date memory and reason over them, we construct a new dataset called FactConsolidation. […] Agents are prompted to prioritize later information in case of conflict and reason based on the final memory state." […] „We observe that all methods fail on the multi-hop situation (with achieving at most 7% accuracy)."
(https://arxiv.org/html/2507.05257v3 és a HUST-AI-HYZ GitHub/HuggingFace dataset-kártya, T1, Exa search)

Ez a feladat **explicit, sorszám-alapú frissítési szabályt** ad az ágensnek — vagyis a benchmark maga is egy determinisztikus szabályt (magasabb sorszám = frissebb tény) vár el, amit az LLM-alapú rendszereknek kellene követniük.

2. **„Don't Ask the LLM to Track Freshness: A Deterministic Recipe for Memory Conflict Resolution"** / később **„Reliable Post-Retrieval Assembly for Agent Memory"** (Vikas Reddy, Sumanth Reddy Challaram; arXiv:2606.01435, v1: 2026.05.31, v2: 2026.08.02; **elfogadva posterként a COLM 2026 Lifelong Agent Workshopra**) pontosan ezt a három számot közli, egyértelműen a MemoryAgentBench Table 3-ra hivatkozva:

> „the best reported retrieval/memory result is 54% single-hop and all 22 reported systems score at most 7% multi-hop." […] „In the benchmark version used for our experiments and comparisons (arXiv v3), the best retrieval/memory result at 262K is HippoRAG-v2 at 54% single-hop (FC-SH); BM25 reaches 48%, MemGPT and Cognee 28%, Mem0 18%, and Zep 7%. GPT-4o long context reaches 60%. The multi-hop variant (FC-MH) remains at or below 7% across all 22 systems."
(https://arxiv.org/abs/2606.01435, T1, Exa fetch/search)

> „replacing the LLM-judgment answer pipeline with candidate-extraction plus Python `max(serial)` yields +10.8 points on FC-SH (gpt-4o-mini) […] The recipe reaches **78.0% on FC-SH (gpt-4o-mini), 94.8% (gpt-4o)**, and 30.2% on FC-MH (gpt-4o-mini, rising to 51.5% with gpt-4o)." […] „At matched-262K, it beats HippoRAG-v2 by +28 points and the best published FC-MH result by +20."
(ugyanaz, T1)

Vagyis pontosan a tulajdonos által felidézett hármas:
- **54%** = a legjobb publikált LLM-alapú/RAG-alapú memóriarendszer (HippoRAG-v2) pontossága az egylépéses konfliktusfeloldáson (FC-SH),
- **78,0%–94,8%** = egy determinisztikus, `max(serial)` (magasabb sorszám nyer) Python-szabály pontossága ugyanezen a feladaton, backbone-tól függően (gpt-4o-mini → gpt-4o),
- **legfeljebb 7%** = a többlépéses (multi-hop, FC-MH) konfliktusfeloldás legjobb publikált eredménye 22 kiértékelt rendszer közül.

Fontos módszertani pontosítás, amit a forrás maga is hangsúlyoz: a 78–94,8%-os javulás **nem tisztán a „determinizmus" hatása**, hanem elsősorban a pipeline szétválasztásáé (előbb strukturált jelölt-kinyerés, utána külön policy-végrehajtás):
> „A targeted comparison using the same extraction setup shows that changing only the final policy executor contributes 2.0 pp on average and 0 pp at 262K. Most of the gain therefore comes from separating evidence identification from final policy execution rather than from the freshness operator itself."
(https://arxiv.org/html/2606.01435v2, T1, Exa search)

Azaz: a determinisztikus szabály **nem varázsszer önmagában** — a fő nyereség abból ered, hogy a bizonyíték-azonosítást szétválasztják a döntés végrehajtásától; a végső döntési lépés determinisztikussá tétele emellett még **plusz, kisebb** (kb. 2 százalékpontos), de következetesen pozitív hozzájárulást ad, és emellett a determinisztikus végrehajtás **inspektálható, auditálható és garantáltan helyes**, amíg a bemeneti jelöltlista tiszta:
> „Among the 205 observations with at least two extracted candidates, deterministic execution is correct on 95.6% and LLM execution on 89.8%, a 5.9 pp difference."
(ugyanaz, T1)

Egy második, független cikk (arXiv, „Last-Write-Wins Memory: Isolating Deterministic Overwrite Semantics", FARS) hasonló irányú, de **jelentősen alacsonyabb** abszolút számokat közöl (LWW-KO: 78% SH, csak 22% MH) ugyanazon a benchmarkon — ez a cikk azonban **saját maga jelzi**, hogy automatikusan generált kutatás:
> „WARNING: This paper was generated by an automated research system."
Emiatt ezt csak **gyenge, kritikával kezelendő** megerősítésként említem, nem önálló bizonyítékként.

---

## Ellentmondások

1. **A MemoryAgentBench multi-hop legjobb eredménye verziónként eltér.** Az eredeti arXiv-cikk (2507.05257) korábbi/HuggingFace-oldalán és GitHub dataset-kártyáján („at most 7% accuracy") és az ICLR 2026 proceedings PDF-jén („at most 28% accuracy") **eltérő maximális multi-hop pontosság szerepel** ugyanahhoz az állításhoz. Ez minden jel szerint a cikk revíziói közötti eltérésből fakad (v1–v4 között; az ICLR camera-ready valószínűleg új, jobb módszereket is bevont). A tulajdonos által idézett „legfeljebb 7%" a korábbi verzióval és a rá épülő arXiv:2606.01435-tel (amely kifejezetten „MAB v3"-ra hivatkozik) egyezik, ezért ezt tekintettem elsődlegesnek, de a 28%-os számot is jeleznem kell, mert ez egy hivatalosan elfogadott konferenciaváltozatból származik. **Forrás:** https://proceedings.iclr.cc/paper_files/paper/2026/file/fd1eff9dd295df50a41f2521942fa31d-Paper-Conference.pdf (28%) vs. https://huggingface.co/papers/2507.05257 és https://github.com/hust-ai-hyz/memoryagentbench (7%).

2. **Az ICML 2026-os „Useful Memories Become Faulty" cikk absztraktja és törzsszövege belsőleg nem konzisztens** a kulcsszámban: az absztrakt „GPT-5.4 fails on 54%" (vagyis 54% a hibaarány), míg a törzsszöveg kétszer is „fails on 46%" / „down to 54% accuracy" formában fogalmaz (vagyis 54% a *pontosság*, 46% a *hibaarány*). A két megfogalmazás egymásnak ellentmond, ha szó szerint vesszük az absztraktot. A törzsszöveg (kétszeres, konzisztens megfogalmazása) alapján a helyes olvasat: pontosság 100%→54%, hibaarány 46%.

3. **A mem0 LOCOMO-eredménye maga is vitatott/inkonzisztens a forrásokon belül.** A mem0 saját cikke (arXiv:2504.19413) 66,88%-os „Overall J" pontosságot közöl Mem0-ra, a mem0 jelenlegi GitHub README-je viszont egy „régi" (71,4) és egy „új" (91,6–92,5) algoritmus-verziót különböztet meg ugyanarra a LoCoMo-ra, más-más időpontban közzétett számokkal (a README különböző idézett részletei 91,6-ot és 92,5-öt is mondanak „New Algorithm"-ra). Egy közösségi GitHub-issue (#4573) szerint továbbá ezek a számok „self-reported…already contested by Zep", és valaki nem tudta reprodukálni API-n keresztül (0,20-at kapott 0,669 helyett). **Ezt nem tudtam független, harmadik féltől származó, ellenőrzött benchmark-futtatással megerősíteni vagy cáfolni** — ezért ez NINCS FORRÁS jellegű bizonytalanság, csak jelzem, hogy a mem0 saját teljesítményszámai időben és forrásonként instabilak.

4. **A „determinizmus javította-e a pontosságot" kérdésre a 2606.01435 cikk két, egymásnak látszólag ellentmondó üzenetet küld**: egyrészt a fő állítás szerint a determinisztikus `max(serial)`-szabály masszívan (+24–28 pp) jobb, mint a legjobb publikált LLM-alapú rendszer; másrészt egy kontrollált, „minden mást fixen tartó" összehasonlításban a *pusztán* a végrehajtó LLM→determinisztikus kód cserélése csak +2,0 pp-ot (262K-nál 0 pp-ot) ad. A cikk maga oldja fel ezt: a nagy különbség nem a „determinizmusból", hanem a *pipeline-szétválasztásból* (jelölt-kinyerés vs. döntés-végrehajtás) ered — ez nem valódi ellentmondás, csak könnyen félreérthető, ezért itt is jelzem.

---

## Amire NINCS forrás

- **Nem találtam lektorált (peer-reviewed) tanulmányt, amely kifejezetten és számszerűen méri a mem0-stílusú ADD/UPDATE/DELETE/NOOP döntés per-operation pontosságát/hibaarányát** (pl. hány százalékban választ helyesen UPDATE-et DELETE helyett, kontrollált ground truth mellett). Amit találtam, az vagy végeredmény-szintű benchmark-pontszám (LoCoMo/LongMemEval „J" vagy „accuracy", ami a teljes pipeline-t méri, nem az egyes műveletdöntést külön), vagy anekdotikus GitHub-issue.
- **Nem találtam hivatalos OpenAI-nyilatkozatot vagy -incidensjelentést** a ChatGPT memória-funkció hibáiról (a 3.2 pontban idézett anyag kizárólag felhasználói fórumbejegyzés, az OpenAI Developer Community-n, OpenAI hivatalos megerősítése nélkül).
- **Nem sikerült a mem0 „66,9% vs. 71,4% vs. 91,6% vs. 92,5%" LoCoMo-számainak pontos idővonalát és a köztük lévő módszertani különbséget (mérési dátum, algoritmus-verzió) egyértelműen, elsődleges forrásból rekonstruálni** — csak azt tudom megerősíteni, hogy több, egymásnak ellentmondó szám kering a mem0 saját anyagaiban.
- **Nem találtam közvetlen, kontrollált kísérletet arra, hogy a saját tervezett rendszer architektúrája (kizárólag beágyazó modell + determinisztikus szabályok, LLM nélkül a szerveroldalon) hogyan teljesítene a MemoryAgentBench FactConsolidation vagy LongMemEval knowledge-update feladatán** — ez nyilván azért nincs, mert a rendszer még nem létezik; ezt csak jelzem, nehogy hiányként értelmeződjön a kutatás.

---

---

# SQ04 — Mit lehet csak beágyazó modellel és szabályokkal elvégezni, és hogyan kerül ember elé?

*Módszertani megjegyzés: a `_kozos.txt` előírása szerint kizárólag az Exa eszközzel (`mcp__Exa__web_search_exa`, `mcp__Exa__web_fetch_exa`) kerestem. A `deep-web-research` skillt nem indítottam el teljes alügynök-pipeline-ként (az saját `.research/` mappát és önálló kimeneti formátumot hozna létre, ami ütközne a `_kozos.txt`-ben előírt egyfájlos, fix szerkezetű kimenettel) — a skill elveit (elsődleges forrás, szó szerinti idézet, kereszt-ellenőrzés, T1/T2/T3 jelölés) manuálisan, degradált módban követtem, ahogy azt a közös utasítás megengedi. Minden idézet Exa keresés/oldal-olvasás eredménye; `curl`-t nem használtam.*

## Rövid válasz

Rövid szövegeken (pl. memóriabejegyzések) a koszinusz-küszöb és a klaszterezés (k-means, HDBSCAN, agglomeratív) jól dokumentált módszerek, de a küszöbérték **erősen adat- és modellfüggő**: publikált mérések szerint az „általánosan idézett 0,9-es" küszöb valós adaton a duplikátumok 42–78%-át kihagyhatja, és a helyes küszöb ugyanazon a feladaton is 0,05–0,96 között szóródhat modellenként. A legfontosabb és legjobban alátámasztott negatív eredmény: **több egymástól független tanulmány (Zhu et al. 2018, SemAntoNeg 2022, „Daunting Dilemma" 2023, és számos gyakorlati beszámoló) kimutatta, hogy a koszinusz-hasonlóság NEM különbözteti meg megbízhatóan az ellentmondó („X igaz" vs „X hamis") állításokat az egyező/parafrázis állításoktól** — a tagadás gyakran csak minimális hasonlóság-csökkenést okoz, mert a szóátfedés dominál. A beágyazás determinizmusa API-modelleknél (pl. régi OpenAI ada-002) dokumentáltan **nem tökéletes** (kb. 3–5%-os eltérés futtatások között, 3–4. tizedesjegyben), nyílt modelleknél pedig a batch-méret és a GPU/CPU/MPS eltérés is mérhető, de tipikusan elhanyagolható (~1e-6–1e-7) — kivéve alacsony pontosságú (bfloat16/int8/binary) beágyazásoknál, ahol dokumentáltan **tömeges kötések (ties)** keletkeznek a hasonlósági pontszámokban, ami küszöb-alapú döntéseknél számíthat. A klaszterek stabilitása idővel gyenge pont: a HDBSCAN **nem inkrementális** — a fejlesztők és a hivatalos dokumentáció is megerősíti, hogy új adat érkezésekor újra kell futtatni az egész klaszterezést. A „human-in-the-loop" memória-karbantartásra létező minták (mem0 „Dream", memorywire) diff-szerű jóváhagyási sorokat és auto-jóváhagyási tanulást mutatnak, de **konkrét, memória-karbantartásra vonatkozó jóváhagyási-fáradtság mérést nem találtam** — az analóg kódreview-kutatás viszont erős, számszerű bizonyítékot ad arra, hogy a tétel-mennyiség/méret növekedésével drámaian csökken az emberi figyelem (néma jóváhagyások aránya, „rubber-stamping"). Végül: létezik éles termelési példa **kizárólag beágyazással és szabállyal működő konszolidációra** (SemDeDup, MinHash/LSH-alapú dedup könyvtárak), de minden vizsgált ágens-memória rendszer (Zep/Graphiti, mem0, Letta közösségi tervezet), amely megpróbálta ezt önmagában használni, arra jutott, hogy a lexikailag távoli, de szemantikailag ugyanarról szóló vagy egymásnak ellentmondó bejegyzéseket csak LLM-mel (vagy emberrel) lehet megbízhatóan feloldani.

## 1. Közel-duplikátum és „ugyanarról szóló" bejegyzések felismerése beágyazással

### 1.1 Módszerek

A leggyakoribb módszer a **koszinusz-küszöb** (két beágyazás koszinusz-hasonlósága egy `τ` érték felett duplikátumnak számít), amit gyakran **klaszterezéssel** kombinálnak a kvadratikus (O(n²)) páronkénti összevetés elkerülésére.

- **K-means + intra-cluster koszinusz-küszöb**: a SemDeDup módszer előbb k-means-szel klaszterez, majd csak klaszteren belül számol páronkénti koszinusz-hasonlóságot: „*Within each cluster, we compute all pairwise cosine similarities and set a threshold cosine similarity above which data pairs are considered semantic duplicates.*" (Abbas et al., „SemDeDup: Data-efficient learning at web-scale through semantic deduplication", arXiv:2303.09540, 2023-03-16, https://arxiv.org/abs/2303.09540)
- **HDBSCAN**: sűrűség-alapú hierarchikus klaszterezés, nem igényel előre megadott klaszterszámot, „stabilitás"-pontszámot rendel minden klaszterhez: „*A score of 1.0 represents a perfectly stable cluster that persists over all distance scales, while a score of 0.0 represents a perfectly ephemeral cluster.*" (scikit-learn HDBSCAN dokumentáció, https://scikit-learn.org/stable/modules/generated/sklearn.cluster.HDBSCAN.html)
- **Agglomeratív klaszterezés**: pl. a `semaclust` könyvtár rövid szövegekre (városnevek, munkakör-címek, vevői visszajelzések) agglomeratív klaszterezést használ beágyazással: „*semaclust (semantic + clustering) is a small Python library for clustering similar strings using sentence embeddings and agglomerative clustering.*" (https://github.com/cobanov/semaclust)
- **MinHash + LSH** (nem beágyazás, hanem hash-alapú, de gyakran együtt szerepel): „*Find near-duplicate texts in a dataset ... via MinHash + LSH banding ... No embeddings, no model call, no dependencies.*" (neardupe, https://github.com/Amarel-Taylor-Scott/neardupe)

### 1.2 Publikált küszöbérték és precision/recall rövid szövegen

A leggondosabban dokumentált, saját méréssel alátámasztott eredmény (hibajegy-duplikátumokra, tehát rövid, strukturált szövegre) egyértelműen cáfolja az „univerzális 0,9-es küszöb" mítoszát:

> „Thresholds don't transfer between models or datasets. Optimal on my synthetic set: 0.62–0.73. Optimal on Mozilla Bugzilla: 0.27–0.62. The commonly-cited 0.9 misses 42–78% of duplicates on my data." (Alexander Budanov, „How I Chose an Embedding Model for Bug Report Deduplication", https://budanov.me/posts/embedding-benchmark/ — T3, gyakorlati blog, de részletes, reprodukálható méréssel: 650 riport, 4475 pár, F1-görbe threshold-sweeppel)

Ugyanez a szerző: „*The Recall@0.9 column is the most important one. It shows what happens if you use the commonly cited 0.9 threshold. Even the best model (qwen3) would only catch 58% of duplicates.*" — és a legjobb modell F1-pontszáma is csak 0,990, miközben egy egyszerű TF-IDF alap­vonal F1=0,973-at ért el, azaz „*Embeddings still win, but not by much.*"

Egy második, független (React-komponens duplikátumokra készült) benchmark hasonló szórást mutat modellek között: „*Comparing OpenAI text-embedding-3-small to text-embedding-3-large ...: large scores lower on 20 of 22 positive pairs and 15 of 16 hard negatives*" — azaz a nagyobb/drágább modell nem feltétlenül jobb duplikátumkeresésre. (`duplicalis` BENCHMARK.md, https://github.com/pfrankov/duplicalis/blob/master/BENCHMARK.md)

Egy harmadik, kazah nyelvű, lektorált tanulmány (rövid szöveg-duplikátumok TF-IDF vs. szóbeágyazás vs. mondatbeágyazás összevetése) szintén nagy szórást és instabilitást talál a küszöbválasztásban: „*The classification threshold was selected on a validation dataset using the grid search method ... During testing, this resulted in completeness (Recall) = 1.0 and accuracy (Precision) ≈ 0.75 ... This highlights the limitations of threshold metrics.*" (Tleubaeva et al., „Duplicate detection in Kazakh texts: comparison of TF-IDF, word embeddings and sentence embeddings", 2025, https://doi.org/10.54309/ijict.2025.24.4.021 — T1, lektorált folyóiratcikk)

Egy negyedik, saját mérésű esettanulmány (React UI-komponensek, de módszertanilag releváns) explicit módon kimondja, hogy tiszta beágyazás-alapú küszöbölés önmagában sosem hibamentes: „*On realistic data, no model achieves zero false positives. If your dedup system auto-merges without human review, you need a confidence threshold above the optimal F1 threshold ... Human review remains important.*" (duplicalis BENCHMARK.md, uo.)

A **RETSim** (Google, ICLR 2024, lektorált) tanulmány közel-duplikátum és szöveg-torzítás felismerésre rövid szövegen (16–8192 karakter) méri a különböző modellek és hash-módszerek (MinHash, SimHash) teljesítményét: „*RETSimNear-Dup and RETSimPartial-Dup outperforms all other methods on short texts with fewer than 128 characters.*" — a hivatalos, jónak talált küszöbök modellenként (koszinusz-hasonlóságban) erősen eltérnek: Multilingual USE 0,88, E5-Base 0,96, saját RETSim 0,82–0,89. (Google DeepMind/Google, RETSim, https://proceedings.iclr.cc/paper_files/paper/2024/file/194d93e09eabcb9e2837de07d0be48ce-Paper-Conference.pdf)

### 1.3 Nyelvfüggőség (többnyelvű modellek)

A RETSim (41 nyelven mért W4NT3D benchmark) publikált eredménye: „*RETSimNear-Dup achieves an average Recall@1 of 0.977 across all 41 languages ... RETSimNear-Dup outperforms baseline algorithms on all languages except for Chinese and Japanese. For these languages, we theorize that semantic embeddings may have the slight edge ... the sub-word level tokenizers used in the baseline embeddings often treat each character in Chinese or Japanese as individual tokens.*" — azaz **nyelvfüggő**, és a tokenizálási módszer (nem csak a modell) számít. (RETSim, uo.)

A LaBSE (Google, ACL 2022, lektorált) publikált eredménye a nyelvi lefedettség hatásáról: „*All three models perform well on the 14 major languages supported by m-USE, with each model achieving an average accuracy > 93%. As more languages are included, the averaged accuracy for both LaBSE and LASER decreases ... LaBSE systematically outperforms LASER on the groups of 36 languages (+10.6%), 82 languages (+11.4%), and 112 languages (+18.2%).*" (Feng et al., „Language-agnostic BERT Sentence Embedding", https://aclanthology.org/2022.acl-long.62/) — a Kaggle-modellkártya konkrét számokat ad: „*Tatoeba | 36 languages from XTREME | All (112) languages ... Average Accuracy | 0.950 | 0.837*" (https://www.kaggle.com/models/google/labse)

Egy 101 nyelvet vizsgáló, lektorált (EMNLP 2021) elemzés azt is megmutatja, **mi okozza** a nyelvenkénti eltérést: „*Our analysis show that word order agreement and agreement in morphological complexity are two of the strongest linguistic predictors of cross-linguality.*" (Jones, Wang, Mahowald, „A Massively Multilingual Analysis of Cross-linguality in Shared Embedding Space", https://doi.org/10.18653/v1/2021.emnlp-main.471) — ez különösen releváns a magyarra, mint agglutináló, gazdag morfológiájú nyelvre.

**Magyar nyelvre konkrétan**: két friss (2025), egymástól független magyar kutatás foglalkozik kifejezetten beágyazás-alapú szemantikai hasonlósággal magyarul.
- „*Building Retrieval-Augmented Generation (RAG) systems for underrepresented languages, such as Hungarian, presents significant challenges due to the lack of high-quality embedding models.*" — a szerzők saját HuBERT/XLM-RoBERTa/MiniLM-alapú, magyarra finomhangolt modelleket értékelnek: „*The hubert sentence hu model achieved the highest F1-Score of 0.490 and the highest accuracy of 0.438* [egy 225 cikkes teszt-korpuszon]." (Hatvani, Yang, „Training Embedding Models for Hungarian", https://real.mtak.hu/207276/1/86-91.pdf — magyar kutatóintézeti kiadvány)
- Egy másik, 2025 novemberi tanulmány 8 beágyazó modellt (kereskedelmi és nyílt) hasonlít össze magyar kérdés-válasz visszakeresésen: „*Neural embeddings consistently outperformed BM25 baseline ... Error analysis revealed three main failure modes: synonyms/paraphrases, overlapping topics, and domain-specific terminology.*" A modellek közti szórás nagy: pl. a Clearservice adathalmazon Recall@1 0,38 (Gemini) és 0,86 (BGE-M3) között mozog. (Antal, „Evaluation of Embedding Models for Hungarian Question-Answer Retrieval", https://www.authorea.com/doi/pdf/10.22541/au.175934564.40505248, kód: https://github.com/margitantal68/hu-embeddings-hurte)
- Gyakorlati (T3) mérés kifejezetten **majdnem-azonos mondatpárokra** (HuWNLI: „*two nearly identical sentences ... differ in one or two words*", tehát pontosan a projekt duplikátum-problémájának megfelelő eset): „*The basic assumption is that the data labeled with 0 will have a low cosine similarity ... Honestly, the performance in the top row is somewhat disappointing ... even then, there is still a large overlap, MCC values are not too high.*" (Harang Péter, „How efficient are embeddings on Hungarian text?", https://medium.com/@harangpeter/how-efficient-are-embeddings-on-hungarian-text-460ba78b742b)

### 1.4 Kiemelt kérdés: megkülönbözteti-e a koszinusz-hasonlóság az ELLENTMONDÓ állításokat az egyezőktől?

Ez a projekt szempontjából kritikus kérdésre **több, egymástól független, lektorált/arXiv forrás egybehangzóan NEM-mel válaszol.**

1) Az egyik legkorábbi rendszeres vizsgálat (ACL 2018) kifejezetten ezt a hipotézist teszteli: „*A sentence S such as 'A rabbit is jumping over the fence' and a sentence S∗ such as 'A rabbit is not jumping over the fence' diverge with respect to many of the inferences that they warrant... we still expect the cosine similarity between their respective embeddings to be fairly high, in light of their semantic relatedness.*" Az eredmény modellfüggő: „*GloVe Avg. is more often than not misled by the introduction of synonyms... In contrast, both InferSent and SkipThought succeed in distinguishing unnegated sentences from negated ones*" — de más metrikán (kvantoros tagadás) „*The results of both averaging of word embeddings and SkipThought are dismal in terms of the accuracy.*" (Zhu, Li, de Melo, „Exploring Semantic Properties of Sentence Embeddings", ACL, https://aclanthology.org/P18-2100.pdf)

2) Egy 2022-es, kifejezetten erre épített benchmark (3152 tételes teszthalmaz) szerint: „*We demonstrate that performance varies greatly across different language models when a specific type of meaning-preserving transformation is applied: two sentences should be identified as paraphrastic if one of them contains a negated antonym... Language models fine-tuned for natural language inference outperform other types of models, especially the ones fine-tuned to produce general-purpose sentence embeddings.*" — vagyis az **általános célú** beágyazó modellek (amilyet ez a projekt is használna) éppen a leggyengébbek ebben. (SemAntoNeg, ACL blackboxnlp 2022, https://aclanthology.org/2022.blackboxnlp-1.20/)

3) Egy 2023-as, több modellt (Doc2Vec, InferSent, LASER, USE, SBERT) szisztematikusan tesztelő tanulmány kimondja: „*All models failed to differentiate between a sentence and its antonym, as evidenced by the left-skewed cumulative histogram... The high overlap of words between sentences may be a possible reason for the failure.*" (Daunting Dilemma paper, arXiv:2309.03747, https://arxiv.org/html/2309.03747)

4) Gyakorlati megerősítések konkrét számokkal: „The problem is the cosine similarity returns 0.9, indicating that these two strings are very similar in context when I expected it to return something closer to zero, as they have the opposite meanings." (StackOverflow, https://stackoverflow.com/questions/69091576/string-comparison-with-bert-seems-to-ignore-not-in-sentence) — egy másik felhasználó saját mérése: „I like rainy days because they make me feel relaxed." vs. „I don't like rainy days because they don't make me feel relaxed." → „return a similarity of 0.993 with the model distilbert-base-uncased." (HuggingFace fórum, https://discuss.huggingface.co/t/sentence-similarity-models-not-capturing-opposite-sentences/10388)

5) A jelenség súlyosságát az mutatja legjobban, hogy külön, tagadásra finomhangolt modelleket kellett létrehozni (CANNOT adathalmaz), és ezek MÉRHETŐEN eltérnek az alapmodelltől ugyanazon a mondatpáron: alap modell 0,993 (a fenti pár), tagadásra finomhangolt `dmlls/all-mpnet-base-v2-negation` modell **0,386** — miközben egy valódi parafrázispárra mindkettő magasan marad (0,948–0,996 körül). (StackOverflow válasz a CANNOT/Negate szerzőjétől, https://stackoverflow.com/questions/69374258/sentence-similarity-models-not-capturing-opposite-sentences)

6) Egy 2025-ös (Nature Scientific Reports) tanulmány kvantitatívan is megerősíti a jelenséget egy saját, tagadás-tudatos metrikával szembeállítva: „*In the presence of single and odd negation, NAS Scorer produces very low similarity scores (12.3 and 9.8), accurately reflecting polarity reversal, whereas SBERT and the LoRA-based models continue to assign relatively high scores, indicating systematic overestimation under negation.*" (http://www.nature.com/articles/s41598-025-34084-2_reference.pdf)

**Következtetés a projekt szempontjából**: a koszinusz-küszöb önmagában **nem alkalmas** ellentmondó bejegyzések (pl. „X technológia jó erre" vs. „X technológia rossz erre") megkülönböztetésére az egyező bejegyzésektől — ehhez vagy dedikált, tagadás-tudatos (fine-tuned) modell, vagy NLI-osztályozó, vagy emberi/LLM-es döntés szükséges.

## 2. A beágyazás determinizmusa

**Kereskedelmi API (OpenAI, ada-002 modell)**: több, egymástól független közösségi fórum-szál (nem hivatalos dokumentáció, de OpenAI-alkalmazott is válaszol bennük) egybehangzóan nem-determinisztikus viselkedésről számol be: „*The dot product is very close to 1, yes. But there are differences in about the fourth decimal digit, sometimes even in [the] third... I'd say [about] 3-5% of embeddings generated will vary between runs.*" (OpenAI Community fórum, https://community.openai.com/t/can-text-embedding-ada-002-be-made-deterministic/318054) OpenAI oldaláról érkező válasz ugyanitt: „*Unfortunately at this time there is no way to make the embeddings deterministic. There are several plausible theories as to why they aren't, but none of them provide a way forward to eliminate the variance observed.*" Egy másik szálban konkrét számpélda: „`v1[0] = -0.021834855899214745` / `v2[0] = -0.021884862333536148`" — ugyanarra a „Hello" szóra, két egymást követő hívásra. (https://community.openai.com/t/why-openai-embedding-return-different-vectors-for-the-same-text-input/144495) Hivatalos OpenAI ajánlott megoldás nincs; a közösség saját hash-alapú gyorsítótárazást javasol: „*So a new thing comes in, you hash it, you look to see if it's in your database. If it is, you return the embedding vector from the database.*" (uo.)

**Nyílt forráskódú modellek (sentence-transformers)**: a hivatalos GitHub-repó több, a karbantartó (Tom Aarsen) által is megerősített hibajegye mutatja, hogy a **batch méret** befolyásolja az eredményt: „*Different batch sizes lead to different embeddings... st.encode(texts, batch_size=32) != st.encode(texts, batch_size=1)*" — a karbantartó válasza: „*we believe this originates in torch or even lower-level than that, rather than sentence-transformers or transformers... I don't think that this will ever notably impact downstream performance like retrieval, classification, clustering.*" (https://github.com/huggingface/sentence-transformers/issues/2312, és https://github.com/huggingface/sentence-transformers/issues/3109) A tipikus eltérés nagyságrendje: „*I can reproduce this behaviour, and I can indeed narrow it down to the underlying transformers model. In my findings, I get a discrepancy of about 1e-7.*" (uo.) CPU/GPU eltérésre: „*this is a result of floating point arithmetic errors (the diffs are on the order of 1e-6).*" (https://github.com/huggingface/sentence-transformers/issues/1695) Van azonban **dokumentált kirívó eset** is: PyTorch 2.8.0 + MPS (Apple Silicon) eszközön egy felhasználó mért koszinusz-hasonlósága **0,5 alá esett** ugyanazon szavak batch_size=64 vs. batch_size=1 kódolása között — ezt a PyTorch csapata hibaként azonosította és javította (torch 2.9.0-ban). (https://github.com/huggingface/sentence-transformers/issues/3197)

**A determinizmus-probléma gyökere (elsődleges, technikai forrás)**: a Thinking Machines Lab (Mira Murati AI-laborja) 2025 szeptemberi, technikailag részletes blogbejegyzése kimutatja, hogy a GPU-alapú batch-inferencia nem-determinizmusának valódi oka **nem** a lebegőpontos nem-asszociativitás + konkurrencia (ahogy általánosan hiszik), hanem a kernelek „batch-invarianciájának" hiánya: „*the primary reason nearly all LLM inference endpoints are nondeterministic is that the load (and thus batch-size) nondeterministically varies! This nondeterminism is not unique to GPUs — LLM inference endpoints served from CPUs or TPUs will also have this source of nondeterminism.*" (Thinking Machines Lab, „Defeating Nondeterminism in LLM Inference", https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/) — ez ugyanazokra a matmul/RMSNorm/attention redukciós műveletekre vonatkozik, amelyeket a transformer-alapú beágyazó modellek is használnak, tehát a jelenség elviekben rájuk is érvényes, bár a blogbejegyzés kifejezetten LLM-generálásra fókuszál, nem beágyazásra (extrapoláció, nem közvetlen mérés).

**Számít-e küszöb-alapú döntésnél?** A jellemző eltérések (~1e-6–1e-7 float32-ben) messze a tipikus 0,6–0,95-ös küszöbök alatt vannak, tehát **általában nem** befolyásolja a bináris duplikátum-döntést. Van azonban egy dokumentált, közvetlenül releváns kivétel: **alacsony pontosságú (fp16/bfloat16) hasonlóság-számítás** durván „összecsomósítja" a pontszámokat. A sentence-transformers v6 javítás és egy 2026-os ACL-cikk (Yang et al., „Reliable Evaluation Protocol for Low-Precision Retrieval") kimutatja: „*bfloat16 can only represent 129 distinct values in all of [0.5, 1.0), which is where retrieval cosine scores tend to live. In a quick probe with 10k realistic cosine scores (mean 0.7, std 0.05), float32 keeps 9983 distinct values, float16 keeps 593, and bfloat16 keeps just 93... a 10k-document ranking scored in bfloat16 cosine has roughly 93 score levels, i.e. massive ties throughout.*" (Tom Aarsen, sentence-transformers PR #3892, https://github.com/UKPLab/sentence-transformers/pull/3892) Ez **közvetlenül releváns küszöb-alapú döntésnél**, ha a rendszer kvantált (int8/binary) beágyazást tárol — ilyet a Cohere és a Voyage AI is kínál tárhelyoptimalizálásra: „*binary... reduces the needed memory 32x while keeping 90-98% of the original search quality.*" (Cohere hivatalos dokumentáció, https://docs.cohere.com/docs/semantic-search-with-cohere.mdx)

**Gyártói állítás determinizmusról**: sem a Cohere, sem a Voyage AI hivatalos dokumentációjában nem találtam kifejezett állítást arra, hogy azonos bemenetre mindig bitazonos kimenetet adnak — a Cohere dokumentációja a `seed` paramétert csak a *generatív* (chat) modellekhez köti, nem a beágyazáshoz: „*The seed parameter does not guarantee long-term reproducibility.*" (https://docs.cohere.com/docs/predictable-outputs.mdx) — beágyazásra vonatkozó explicit determinizmus-garanciát egyik nagy szolgáltatónál sem találtam (lásd „Amire nincs forrás").

## 3. Klaszterek stabilitása idővel

A **HDBSCAN nem inkrementális**: a hivatalos dokumentáció kimondja, hogy új pontok érkezésekor a teljes klaszterezést újra kellene futtatni ahhoz, hogy a klaszterek valóban frissüljenek: „*This is hard for HDBSCAN* as it is a transductive method – new data points can (and should!) be able to alter the underlying clustering... given new information it might make sense to create a new cluster, split an existing cluster, or merge two previously separate clusters.*" (https://hdbscan.readthedocs.io/en/latest/prediction_tutorial.html) A karbantartó egy GitHub-issue-ban ezt megerősíti: „*Incrementally adding new clusters without changing the current clusters is ... not really possible by any means that I know of... in practice it is actually cheaper to re-cluster from scratch with the new points.*" (https://github.com/scikit-learn-contrib/hdbscan/issues/76)

**Részleges megoldás — approximate_predict()**: a HDBSCAN kínál egy „befagyasztott" klaszterezéshez való hozzárendelést új pontokra (`prediction_data=True` + `approximate_predict()`), de ez kifejezetten **nem** engedi a klaszterek átalakulását: „*It is as simple as that. So now you can get started using HDBSCAN as a streaming clustering service — just be sure to cache your data and retrain your model periodically to avoid drift!*" (uo.) — azaz a hivatalos ajánlás maga is elismeri, hogy időszakos teljes újraklaszterezés szükséges.

**Inkrementális közelítő algoritmus létezik, de nem elterjedt**: a FISHDBC (2019, arXiv:1910.07283) HNSW-alapú, inkrementálisan frissíthető feszítőfát tart fenn a HDBSCAN* közelítésére: „*HDBSCAN* is not incremental — if new data arrives, results have to be recomputed from scratch ... FISHDBC instead supports incremental computation, maintains or even improves result quality.*" (https://ar5iv.labs.arxiv.org/html/1910.07283) Ez azonban egy közelítő módszer, korlátozott elterjedtséggel (niche implementáció, nem a mainstream HDBSCAN-könyvtár része).

**Stabilitás mérésének bevett módszere — konszenzus-klaszterezés**: a bioinformatikából származó, széles körben idézett módszer (Monti et al. 2003) újramintavételezéssel (bootstrap/subsampling) méri a klaszterezés stabilitását, nem magát az inkrementális frissítést oldja meg, hanem azt teszi mérhetővé, mennyire megbízható egy adott klaszterezés: „*The more the attained clusters are robust to sampling variability, the more we can be confident that these clusters represent real structure ... perturbations of the original data can be simulated by resampling techniques ... and the agreement, or consensus, among the multiple runs can be assessed.*" (Monti, Tamayo, Mesirov, Golub, „Consensus Clustering", Machine Learning, https://link.springer.com/content/pdf/10.1023/A:1023949509487.pdf) Ennek stabilitás-mutatóit (PAC, RCSI stb.) egy 2024-es összefoglaló tárgyalja részletesen (https://doi.org/10.1101/2024.03.21.586064) — de ez a módszertan **nem kifejezetten** beágyazás-alapú rövid szöveges memóriarendszerekre lett kidolgozva, hanem génexpressziós adatokra; NLP/memóriarendszer-kontextusban való alkalmazására közvetlen forrást nem találtam.

**Hogyan kerülik ki a valódi ágens-memória rendszerek a problémát?** A vizsgált termelési rendszerek (mem0, Zep/Graphiti, Letta) egyike sem végez globális újraklaszterezést — ehelyett **páronkénti, küszöb-alapú, kereséskor futtatott** hasonlóság-keresést használnak új bejegyzés beillesztésekor (pl. Graphiti: „*NODE_DEDUP_COSINE_MIN_SCORE = 0.6*" — https://github.com/getzep/graphiti/blob/34f56e65e0fe2096132c8d16f3a1a4ac9300a5f6/graphiti_core/utils/maintenance/node_operations.py), ami elkerüli a globális klaszter-instabilitás problémáját, cserébe nem ad áttekintő csoportosítást — ez inkább kitérés a kérdés elől, mint megoldás.

## 4. „Human-in-the-loop" memória-karbantartás

### 4.1 Hogyan mutatják a gépi javaslatokat?

A **mem0** két, egymásnak részben ellentmondó megoldást publikál (l. Ellentmondások):

- A hivatalos platform-dokumentáció szerint a Merge/Supersede **automatikusan**, emberi jóváhagyás nélkül fut minden csomagban: „*Supersede and Merge require no setup. They're always on for every project on every plan.*" (https://docs.mem0.ai/platform/features/dream)
- Ezzel szemben a mem0 nyílt forráskódú „dream" agent-skillje explicit **diff-report + Y/n jóváhagyást** ír elő, és a *kontradikciókat sosem oldja fel automatikusan*: „*All proposed changes are shown as a diff for user approval before anything is modified ... Contradictions where the user chose skip are left untouched ... Contradictions: skipped — they require human judgment.*" A diff formátuma explicit: „`## dream — consolidation report / Merges (<N>): ... Conflicts (<N>): [mem0:<idA>] vs [mem0:<idB>] — \"<topic>\" [A/B/skip] / Proposed: <N> merges, <N> prunes, <N> conflicts. Apply? [Y/n]`" (mem0 GitHub, dream skill, https://github.com/mem0ai/mem0/blob/b357a5a1b03c299ec8229c268e63cfac0f7c6566/integrations/mem0-plugin/skills/dream/SKILL.md)

A **memorywire** (2026, arXiv-preprint — ld. megjegyzés alább) strukturált diff-and-approve munkafolyamatot ír le: „*Writes flagged approval_required are staged behind a PENDING_APPROVAL_DELETED_AT = -1 sentinel and remain invisible to recall until a reviewer commits or rejects them through the UI... The reference UI layers an opt-in approval-learning loop on top: track which patterns the reviewer always approves/rejects and auto-allow after N consistent decisions, with every fired decision still journaled to the audit log.*" (https://arxiv.org/html/2606.01138) — **fontos módszertani megjegyzés**: ez egy 2026 májusában egyetlen független kutató által benyújtott, láthatóan **nem lektorált** (self-published) arXiv-preprint, szokatlanul „marketing"-stílusú GitHub-oldallal; a konkrét „N" jóváhagyási-fáradtság elleni auto-allow küszöbértéket a szöveg nem adja meg számszerűen, és a módszer hatékonyságát (csökkenti-e ténylegesen a fáradtságot) a szerző nem méri empirikusan. T2/gyenge-T2 forrásként kezelendő, nem intézményi kutatásként.

A **Letta** közösségi tervezete (GitHub issue, 2025 december) kétlépcsős modellt javasol, explicit módon **elválasztva** az olcsó, gyakori, tisztán embedding-alapú dedup-lépést a drága, ritka, LLM-es konszolidációtól: „*Phase 1 — Dedup (cheap, run frequently). Pure vector similarity within a cosine distance threshold ... No LLM call needed ... Phase 2 — Consolidation (expensive, run infrequently). This is where you need the LLM ... never delete the raw episodes.*" (https://github.com/letta-ai/letta/issues/3116)

### 4.2 Van-e adat a jóváhagyási fáradtságra?

**Közvetlenül memória-karbantartásra vonatkozó, számszerű jóváhagyási-fáradtság mérést nem találtam** (ld. „Amire nincs forrás"). Az **automatizmus-torzítás** (automation bias) általános szakirodalma viszont jól dokumentált, és mediáló tényezőként explicit megnevezi a terhelést/összetettséget:

> „User factors such as cognitive style, decision support systems (DSS), and task specific experience mediated AB ... Environmental mediators included workload, task complexity, and time constraint, which pressurized cognitive resources." (Goddard, Roudsari, Wyatt, „Automation bias: a systematic review of frequency, effect mediators, and mitigators", JAMIA 2011, 74 tanulmány szisztematikus áttekintése, https://pmc.ncbi.nlm.nih.gov/articles/PMC3240751/ — T1, lektorált szisztematikus review)

Egy másik, kifejezetten a **verifikáció összetettségére** fókuszáló szisztematikus review címe is releváns (bár a teljes szöveget nem olvastam ki): Lyell & Coiera, „Automation bias and verification complexity: a systematic review", JAMIA 2016 (idézve: https://doi.org/10.1007/s13347-026-01090-9 hivatkozáslistájában).

Gyakorlati (T3, szakértői panel) megerősítés a „rubber-stamping" jelenségre: „Without clear insight into how and why an AI system reaches its conclusions, oversight becomes superficial, reducing human involvement to a rubber stamp rather than acting as a critical check." (MIT Sloan Management Review, 2025, https://sloanreview.mit.edu/article/ai-explainability-how-to-avoid-rubber-stamping-recommendations/)

**A legerősebb, számszerű analógia** a kódreview-kutatásból származik — nem memória-karbantartásról szól, de módszertanilag közvetlenül átvihető (sok elem egyszerre emberi elé kerülő jóváhagyása):

- Cisco 2006, 2500 kódreview: „*when reviewers moved faster than 450 lines per hour, 87% of reviews had below-average defect detection ... review effectiveness plummets after 90 minutes of code reviewing, with 60 minutes being the optimal session length.*" (idézve: https://rishi.baldawa.com/posts/pr-throughput/cognitive-load-cliff/ — T3, de elsődleges empirikus tanulmányra hivatkozik)
- Microsoft, 1,5 millió review-komment, 5 projekt: „*About one-third of code review comments weren't useful to the author. More tellingly, the more files in a changeset, the lower the proportion of useful feedback.*" (uo.)
- Kereskedelmi, nagymintás (T3) elemzés 3,4 millió GitHub PR-en: „*Review comments per 100 lines of code drops from 0.91 for tiny PRs to just 0.05 for massive ones — an 18x reduction in scrutiny per line ... 82.6% of pull requests over 1,000 lines ship without any formal code review.*" (https://codepulsehq.com/research/rubber-stamp-problem)
- Longitudinális (2019/2022/2026), 77 949 PR-en végzett kereskedelmi (T3) elemzés kifejezetten a „néma jóváhagyás" (rubber-stamp) arányának időbeli növekedését méri: „*62% of approvals contain zero words ... Silent approvals ... jumped after 2022 [+8.4pp, p=0.002] ... 4× less attention per line on 1,000+ line PRs than on mid-sized ones ... 509 approvals landed faster than a human could physically read the diff.*" (Reviewsaur, „The State of Code Review 2026", https://www.reviewsaur.com/research)

**Ajánlás a javaslatok számára**: konkrét, memória-karbantartásra szabott számot (pl. „legfeljebb N javaslat review-ablakonként") egyik forrásban sem találtam; a kódreview-irodalom analóg, közvetve átvihető mérőszámai (60–90 perces figyelmi ablak, 200–400 sor/„kognitív szikla") szolgálhatnak kiindulópontként, de ez extrapoláció, nem közvetlen mérés a memória-karbantartás területén.

## 5. Kizárólag beágyazással és szabállyal (LLM nélkül) működő konszolidáció

**Létező, LLM NÉLKÜLI rendszer**: a **SemDeDup** (Meta AI, 2023) a legtisztább, publikált példa — k-means klaszterezés + koszinusz-küszöb, generatív LLM sehol a folyamatban: „*First, we embed each data point using a foundation model ... We then cluster the embeddings into k clusters via k-means. Within each cluster, we compute all pairwise cosine similarities and set a threshold cosine similarity above which data pairs are considered semantic duplicates.*" (arXiv:2303.09540) **Mit tud**: web-méretű (440M képi-szöveges pár) adathalmazból 37–50%-ot eltávolítani teljesítményvesztés nélkül, sőt néhol javulással: „*SemDeDup can remove up to 37% of LAION440M with no performance drop, and 50% with minimal performance drop (<0.5%) ... on about 20 out of 30 tasks, performance actually improves after removing pre-training data.*" **Mit NEM tud (a szerzők saját korlátozás-listája)**: „*this work does not capture many aspects of semantic redundancy, nor does it address removal of bad or misleading data ... In LAION, we identified semantic duplicates based only on image data, but we ignored the caption information* [tehát csak az egyik modalitást nézi] *... requires access to a pre-trained embedding model relevant to the domain of interest.*" A nyílt tudományos review-platformon (Pith) rögzített, szerzők által is elfogadott kritika: „*the manuscript provides no details on the exact semantic similarity threshold chosen, whether it was tuned on held-out data ... no statistical significance tests, error bars from multiple random seeds.*" — a szerzők válasza: „*We agree that the threshold selection process requires explicit documentation ... revision: yes.*" (https://pith.science/paper/O6FNK2VN) A módszert egy **részben független** (3/4 azonos szerző, de más kutatási kérdés — LLM előtanítás, nem kép-szöveg) NeurIPS 2023 cikk (D4) megerősítette és kiterjesztette: „*Abbas et al. demonstrated that using a pre-trained embedding space to de-duplicate data (\"SemDeDup\") improves both efficiency and performance of vision-language models such as CLIP ... D4 can achieve around 20% efficiency gains at the 6.7b model scale.*" (Tirumala et al., „D4", NeurIPS 2023, https://arxiv.org/abs/2308.12284) — mivel a szerzői kör nagyrészt átfedő, ez korlátozott értékű megerősítés, nem teljesen független replikáció.

**Tisztán szabály/hash-alapú (nem is beágyazás) rendszerek**: a MinHash+LSH-alapú könyvtárak (text-dedup, neardupe) kifejezetten LLM és beágyazó modell nélkül dolgoznak: „*Find near-duplicate texts in a dataset ... No embeddings, no model call, no dependencies.*" (https://github.com/Amarel-Taylor-Scott/neardupe) **Mit tudnak**: lexikailag közeli (átfogalmazott, kis módosítású) szövegek gyors, olcsó, nagy adathalmazon skálázódó felismerését. **Mit nem tudnak**: eltérő szóhasználatú, de azonos jelentésű (valódi szemantikai) duplikátumokat — pontosan ez az, amiért a beágyazás-alapú módszerek léteznek.

**Termelési ágens-memória rendszerek saját tapasztalata — miért nem elég az embedding+szabály önmagában**: mindhárom vizsgált nagy rendszer (Zep/Graphiti, mem0, Letta) **hibrid** architektúrához jutott, és a saját mérnöki vitáik konkrétan dokumentálják, hol bukik el a tiszta embedding+szabály megközelítés:

- **Graphiti/Zep** saját PR-ja (2025 szeptember) explicit kétlépcsős tervet vezet be: „*Introduce a two-stage dedupe pipeline: collect candidate nodes via hybrid search, resolve high-entropy matches deterministically with MinHash/LSH similarity, then escalate remaining cases to the LLM prompt.*" (https://github.com/getzep/graphiti/pull/929) — azaz a determinisztikus (embedding+hash) réteg **csökkenti**, de nem váltja ki teljesen az LLM-hívásokat; egy független forrás (Pinakes dokumentáció) megerősíti: „*LLM required, per episode, at ingest: entity extraction, node dedup (escalation path), edge extraction, edge dedup/contradiction ... There is no non-LLM ingestion mode.*" (https://github.com/lucagattoni/Pinakes/blob/main/docs/graph/graphiti.md)
- **mem0** saját, elutasított kódmódosítása (PR #6017) konkrét negatív esettanulmány: a szerző tisztán koszinusz-küszöb alapon (0,85/0,90 kettős küszöb) próbálta a konfliktus-detekciót megoldani, a code review ezt elutasította: „*Similarity establishes relatedness, not contradiction or supersession ... any link plus a global cosine score of at least 0.85 becomes an UPDATE ... this patch can replace the durable profile with an additive event.*" (https://github.com/mem0ai/mem0/pull/6017)
- **Letta** közösségi tervezete kifejezetten kimondja a beágyazás vakfoltját, pontosan az 1.4 pontban tárgyalt ellentmondás-probléma gyakorlati megnyilvánulásaként: „*embedding-based deduplication alone will miss semantic duplicates that are lexically distant. 'User prefers blue' and 'User said they dislike red' might both deserve deduplication treatment, but cosine similarity won't catch it.*" (https://github.com/letta-ai/letta/issues/3116)

**Összegzés Q5-re**: kizárólag beágyazással+szabállyal megbízhatóan elvégezhető: (a) lexikailag/felszínileg közeli, nagy hasonlóságú szövegek gyors, olcsó szűrése/csoportosítása nagy tételben (SemDeDup, MinHash/LSH-előszűrés Graphitiban); (b) jelölt-generálás (candidate retrieval) egy későbbi, pontosabb döntési lépéshez. Amit minden vizsgált termelési rendszer szerint **nem** lehet megbízhatóan csak ezzel: (a) lexikailag távoli, de szemantikailag azonos/ellentétes bejegyzések felismerése; (b) az „összevonás" (merge) és az „felülírás/elavulás" (supersede) megkülönböztetése — ehhez a *mit jelent a változás* megértése kell, nem csak a *mennyire hasonló a szöveg*.

## Ellentmondások

1. **mem0 „Dream" — automatikus vs. emberi jóváhagyás**: a hivatalos platform-dokumentáció szerint a Merge és Supersede „*require no setup. They're always on for every project on every plan*" (https://docs.mem0.ai/platform/features/dream), tehát emberi jóváhagyás NÉLKÜL fut. Ezzel szemben a mem0 nyílt forráskódú „dream" agent-skillje kötelező diff+Y/n jóváhagyást ír elő minden összevonásra, és a kontradikciókat kifejezetten sosem oldja fel automatikusan (https://github.com/mem0ai/mem0/blob/main/integrations/mem0-plugin/skills/dream/SKILL.md). A két forrás ugyanazt a márkanevet és funkciónevet használja, de eltérő terméket (platform API vs. nyílt agent-skill) ír le, és nyíltan ellentmond egymásnak abban, hogy szükséges-e emberi jóváhagyás.
2. **Automatizmus-torzítás mérséklése — külső elszámoltathatóság hatása**: a Goddard et al. (2011) szisztematikus review saját maga jelzi az ellentmondást: „*while two studies showed that external manipulation of accountability increased vigilance and thus decreased AB, another study showed that external manipulations did not have this affect but that users' internal perceptions of accountability did.*" (https://pmc.ncbi.nlm.nih.gov/articles/PMC3240751/)
3. **„Nagyobb/drágább modell jobb duplikátumkeresésre" tétel cáfolata**: a `duplicalis` benchmark szerint a `text-embedding-3-large` rosszabbul teljesít a duplikátum-detekcióban, mint a kisebb `text-embedding-3-small` (https://github.com/pfrankov/duplicalis/blob/master/BENCHMARK.md), miközben a hivatalos OpenAI-közlemény és az általános MTEB-eredmények a `large` modellt jobbnak mutatják általános visszakeresési feladatokon — ez nem közvetlen logikai ellentmondás (task-specifikus eltérésről van szó), de fontos figyelmeztetés arra, hogy az általános benchmark-eredmény nem vetíthető át automatikusan a duplikátum-detekció feladatára.

## Amire NINCS forrás

- Nincs forrás arra, hogy bármelyik nagy beágyazás-szolgáltató (OpenAI, Cohere, Voyage AI, Google) **explicit determinizmus-garanciát** vállalna beágyazásra (bitazonos kimenet azonos bemenetre); az OpenAI közösségi fórumon egy alkalmazott kifejezetten tagadja ezt korábbi (ada-002) modellre, de hivatalos dokumentációban nyilatkozatot egyik szolgáltatónál sem találtam újabb modellekre (pl. text-embedding-3, Cohere embed-v4, Voyage-4) vonatkozóan.
- Nincs forrás konkrét, számszerű „jóváhagyási fáradtság" mérésre kifejezetten memória-konszolidációs (dedup/merge/supersede) javaslatok emberi felülvizsgálatára — csak analóg (kódreview) területről van számszerű adat.
- Nincs forrás egy kifejezetten rövid szöveges memória-bejegyzésekre (nem génexpresszióra, nem képre) szabott, elterjedt, „stabil/reprodukálható" klaszterezési standardra, amit idővel változó bejegyzés-halmazon termelési memóriarendszerek ténylegesen használnak — a vizsgált rendszerek (mem0, Zep/Graphiti, Letta) egyike sem végez globális klaszterezést, hanem páronkénti küszöb-keresést használ.
- Nincs forrás arra, hogy a Thinking Machines Lab „batch invariance" elemzését valaki kifejezetten beágyazó modellekre (nem generatív LLM-re) mérte volna — a fentiekben leírt átvitel a beágyazó modellek alapjául szolgáló azonos transformer-műveletekre (matmul, RMSNorm) épülő ésszerű következtetés, nem közvetlen mérés.
- A „memorywire" arXiv-preprint konkrét „N" auto-jóváhagyási küszöbértékét, illetve azt, hogy az „approval-learning loop" ténylegesen csökkenti-e a jóváhagyási fáradtságot, a szerző nem méri és nem adja meg számszerűen — ez a preprint saját állítása szerinti tervezési elv, empirikus adat nélkül.

---

# ELL01 — A „dream"-megvalósítások állításainak ellenőrzése

## Verdikt-összefoglaló

| # | Állítás | Verdikt | Egy mondat |
|---|---|---|---|
| 1 | open-second-brain „dream" magja LLM-mentes, snapshot/rollback/dry-run/idempotens, v1.40.0 „reporting label", jelenlegi v1.54.0 (2026-08-28); dátum-ellentmondás | **IGAZOLVA** | Minden elem szó szerint igazolva a GitHub release-oldalakon és a forráskódban; a dátum-vitát a release-oldal döntötte el: **sq01 volt pontos** (v0.9.0 = 2026-05-15), sq02 „2025 vége" állítása téves. |
| 2 | open-second-brain reconcile csak JELEZ, kivéve a „source-freshness" esetet | **IGAZOLVA** | Két független elsődleges forrás (v0.21.0 release + docs/how-it-works.md) szó szerint megerősíti: csak a source-freshness eset old fel automatikusan, minden más „operator-facing open question". |
| 3 | Anthropic Dreams: input store soha nem módosul, választható auto/review, research preview; Harvey „~6x" egyetlen ügyfél, módszertan nélkül | **RÉSZBEN** | A „soha nem módosul" állítás csak alapértelmezésben igaz — a hivatalos API-referencia egy `output_behavior: update_existing` (jelenleg EAP-hoz kötött) opciót dokumentál, amely explicit **helyben módosítja** a bemeneti store-t; a többi elem (auto/review választás, research preview, Harvey egyetlen-ügyfél-adat módszertan nélkül) igazolva. |
| 4 | Claude Code hivatalos dok. nem említ dream-et, de GitHub issue #47959 szerint 23 memóriafájl törlődött jóváhagyás nélkül | **IGAZOLVA** | Az idézet szó szerint egyezik az elsődleges GitHub-forrással; a hivatalos code.claude.com/docs/en/memory oldal ma is csak „Auto memory"-t ismer, „dream"-et nem említ. |
| 5 | mem0 Dream (2026-08-04): Merge/Supersede/Synthesize, „Nothing is deleted", heti futás; a dream-skill diff+Y/n-t kér, ellentmondást sosem old fel automatikusan | **IGAZOLVA** | Mindkét idézet szó szerint megerősítve az elsődleges mem0-blogból és a GitHub-skillfájlból. |
| 6 | mimir-mem-core: „LLM-free… four passes, none destructive" — négy lépés a leírtak szerint | **IGAZOLVA** | A docs.rs forráskód-kommentje szóról szóra egyezik az idézettel, küszöbértékekkel (0.92 / 0.85 / 0.80) együtt. |
| 7 | A „dream" szó agent-memóriában 2026 tavaszán jelent meg (Letta PR #1856, 2026-04-21); előtte Letta „sleep-time compute" (2025-04) | **RÉSZBEN** | A Letta-PR ténye és dátuma pontos, de az „elsőség/legkorábbi megjelenés tavasszal" keret két független forrással megdől: egy 2025-12-03-i engrxiv-preprint („Active Dreaming Memory") már agent-memória-konszolidációra használja a „dream" szót, és a Claude Code `autoDreamEnabled` funkciója már 2026-04-14-én (a Letta-PR előtt 7 nappal) dokumentáltan létezett és kárt is okozott. |

## Állításonként

### 1. open-second-brain „dream" — LLM-mentesség, snapshot/rollback/dry-run/idempotencia, verzió, dátum-ellentmondás

**LLM-mentesség** — elsődleges forrás, a v0.9.0 kiadási jegyzék:
> „Filesystem-first, Obsidian-native, no LLM inside the algorithm — counters, thresholds, atomic file operations only." — https://github.com/itechmeat/open-second-brain/releases/tag/v0.9.0

Megerősítve a jelenlegi (main branch) engineering guide-ban is:
> „The system uses counters, thresholds, and atomic file operations — no LLM inside the algorithm, no surprise, no hallucinated memory." — https://github.com/itechmeat/open-second-brain/blob/main/docs/how-it-works.md

A v1.40.0 (2026-07-27) megerősíti, hogy ez a jelenlegi verzióban is így van:
> „The kernel still calls no LLM, and every new flag, argument and configuration key is byte-identical when absent." — https://github.com/itechmeat/open-second-brain/releases/tag/v1.40.0

**„Reporting label with no callable units"** — szó szerint igazolva, ugyanabból a kiadásból:
> „Seven parallel passes over the code invalidated a premise in eight of the ten sources: … semantic dedup nominates and never drops, **the dream "phases" were a reporting label with no callable units**, and the profile ticket named an artifact that does not exist." — https://github.com/itechmeat/open-second-brain/releases/tag/v1.40.0

**Snapshot/rollback** — elsődleges forrás, v0.9.0:
> „Pre-run snapshots: each `dream` run that mutates state writes `Brain/.snapshots/<run_id>.tar.zst`… Default retention 10 most-recent. `o2b brain rollback <run_id>` restores from a snapshot." — https://github.com/itechmeat/open-second-brain/releases/tag/v0.9.0

**Dry-run + idempotencia** — a JELENLEGI (main branch, 2026-09-24-i állapot) CLI súgószövegében, szó szerint:
> „dream: usage: o2b brain dream [run] [--dry-run] | stage | validate | apply | retriage | discard | list [--now] [--agent] [--vault] [--json]\nRuns the deterministic dreaming algorithm (idempotent), or manages the staged lifecycle…" — https://raw.githubusercontent.com/itechmeat/open-second-brain/main/src/cli/brain/help-text.ts

**Verzió/dátum** — az elsődleges GitHub release-oldalak közvetlen ellenőrzésével:
> „Tag: v1.54.0 … Published: 2026-08-28T00:59:38Z … Author: solaitken" — https://github.com/itechmeat/open-second-brain/releases/tag/v1.54.0
> „Tag: v0.9.0 … Published: 2026-05-15T16:15:25Z" — https://github.com/itechmeat/open-second-brain/releases/tag/v0.9.0

**Dátum-ellentmondás feloldása:** a GitHub release-oldal (elsődleges forrás, közvetlenül lekérve) egyértelműen **2026-05-15T16:15:25Z**-t mutat a v0.9.0-hoz. Ez pontosan megegyezik az sq01 állításával. Az sq02-ben szereplő „v0.9.0, 2025 vége" megfogalmazás **téves** — nincs olyan elsődleges forrás, amely ezt alátámasztaná; a release-oldal saját időbélyege cáfolja.

### 2. open-second-brain reconcile — csak jelzés, kivéve „source-freshness"

Első (release-jegyzék) forrás:
> „Reconcile-phase domain classification. Each contradiction is bucketed by structural signal shape into claims / entity / decisions / source-freshness. Only a decisive source-freshness gap auto-resolves - recorded as a `reconcile` log event, never a sub-threshold mutation; everything else surfaces as an operator-facing open question instead of a forced merge. No LLM fan-out." — https://github.com/itechmeat/open-second-brain/releases/tag/v0.21.0

Második, független forrás (a mérnöki dokumentáció, más fájl/commit):
> „Only source-freshness with a decisive recency gap auto-resolves - and even then it is _recorded_ as a `reconcile` log event, never a sub-threshold state mutation. Everything else surfaces in `open_questions` for operator review rather than being force-merged." — https://github.com/itechmeat/open-second-brain/blob/7e6a5672/docs/how-it-works.md

Két, egymástól tartalmilag független (release notes vs. engineering guide) forrás egyezik meg szó szerint az állítással — **IGAZOLVA**.

### 3. Anthropic Claude Managed Agents „Dreams"

**Input store soha nem módosul (alapértelmezésben igaz, de nem kizárólagos)** — a felhasználói dokumentáció szerint:
> „The input store is never modified, so you can review the output and discard it if you don't like the result." — https://platform.claude.com/docs/en/managed-agents/dreams

DE az API-referencia (ugyanaz a termék, elsődleges forrás) egy kivételt dokumentál:
> „An input memory store the dream reads from. **The dream never mutates this store unless it is also the destination**: with output_behavior {type: "update_existing"} the job consolidates this store in place." — https://platform.claude.com/docs/en/api/beta/dreams

> „BetaOutputBehaviorUpdateExisting object: The job writes the consolidated memories into this existing memory store instead of creating one. **In EAP the store must be the job's own memory_store input, so the job consolidates the store in place.**" — uo.

Ez pontosítást igényel: a „soha nem módosul" csak a **alapértelmezett** (`create_new`) módra igaz; az `update_existing` móddal (jelenleg korai hozzáférésű program — EAP — mögött) a bemeneti store **igenis helyben módosul**. A managed-agents/dreams szövegoldal ezt a kivételt nem említi, csak az API-referencia.

**Auto vs. emberi review választható** — elsődleges forrás:
> „Dreaming is a scheduled process in Claude Managed Agents that reviews agent sessions and memory stores, extracts patterns, and curates memories so agents improve over time. You decide how much control you want: dreaming can update memory automatically, or you can review changes before they land." — https://claude.com/blog/new-in-claude-managed-agents

**Research preview** — mindkét elsődleges forrásban:
> „Dreaming is a research preview feature. Request access to try it." — https://platform.claude.com/docs/en/managed-agents/dreams
> „Today we're launching dreaming in Claude Managed Agents as a research preview." — https://claude.com/blog/new-in-claude-managed-agents

**Harvey „~6x" — egyetlen ügyfél, módszertan nélkül:**
> „Harvey uses Managed Agents to coordinate complex legal work like long-form drafting and document creation. With dreaming, their agents remember what they learned between sessions, including filetype workarounds and tool-specific patterns. Completion rates went up ~6x in their tests." — https://claude.com/blog/new-in-claude-managed-agents

Ez az egyetlen forrás a számra; sem mintaméret, sem mérési módszertan, sem kontrollcsoport nincs megadva. Egy független szaksajtó-forrás ugyanerre a hiányra mutat rá:
> „The 6x claim from Harvey is the headline number, but it is also the one Anthropic is publishing without an external benchmark to back it up… Harvey is one data point, and the broader benchmarks are still Anthropic's own." — https://letsdatascience.com/blog/anthropic-dreaming-claude-managed-agents-self-improving-may-6

### 4. Claude Code — hivatalos dok. csendje + GitHub issue #47959

Elsődleges forrás, szó szerint egyezik az ellenőrizendő állítással:
> „After enabling `autoDreamEnabled: true` in `~/.claude/settings.json`, Auto Dream silently deleted 23 memory files within approximately 24 hours. No confirmation was requested, and no record of what was deleted or why was provided." — https://github.com/anthropics/claude-code/issues/47959 (2026-04-14, „bug", „data-loss" címkékkel; utóbb „stale"-ként lezárva 2026-05-23-án)

A hivatalos, jelenlegi Claude Code memória-dokumentáció (2026-09-24-i lekérdezéssel) kizárólag két mechanizmust ismer el — „CLAUDE.md files" és „Auto memory" —, „dream"/konszolidáció szót nem tartalmaz: https://code.claude.com/docs/en/memory

(Kiegészítő, nem hivatalos, T3 megerősítés a funkció létezésére és belső elnevezésére: „AutoDream is Claude Code's background memory consolidation mechanism, internally codenamed 'Dream: Memory Consolidation.'" — https://github.com/HFurther/claude-code-stable/blob/main/docs/en/memory/03-autodream.md — forráskód-útvonalakra hivatkozva, de nem Anthropic-repó.)

### 5. mem0 „Dream" (platform) és a dream-skill

Platform-szintű blog, elsődleges forrás:
> „Dream runs three operations on your project's memories. Merge. [...] Supersede. [...] Synthesize. A background job looks at groups of related memories and writes a new summary memory when several independent observations support one. […] **Nothing is deleted in any of these operations.** Every change is recorded as a state change with a pointer to the newer memory… Memories marked `immutable` or `exclude_from_dream` are skipped entirely." — https://mem0.ai/blog/dream-background-memory-consolidation-for-ai-agents (2026-08-04, szerző: Rudraj Mehta)
> „Runs happen weekly per project per eligible user_ids." — uo.

A mem0-plugin dream-skillje (agent-integráció, külön termék), elsődleges forrás:
> „All proposed changes are shown as a diff for user approval before anything is modified. […] Proposed: <N> merges, <N> prunes, <N> conflicts. Apply? [Y/n]" — https://github.com/mem0ai/mem0/blob/main/integrations/mem0-plugin/skills/dream/SKILL.md
> „In auto mode: Merges: applied automatically… Prunes: applied automatically… Contradictions: skipped — they require human judgment." — uo.

Mindkét idézet szó szerint egyezik az ellenőrizendő állítással. (Megjegyzés, nem cáfolat: a skill technikai megvalósítása a jóváhagyott egyesítéseknél és ellentmondásoknál ténylegesen `delete_memory()`-t hív — ez a platform „nothing is deleted" ígéretével szemben áll, de ez a platform és a skill közti már ismert különbség, nem az itt vizsgált két konkrét állítás cáfolata.)

### 6. mimir-mem-core (docs.rs)

Elsődleges forrás, a forráskód dokumentációs kommentje, szó szerint:
> „LLM-free memory consolidation: four passes, none destructive.\n\n1. near-duplicate merge (cosine ≥ 0.92, same type+scope) → the older node is superseded, never deleted\n2. contradiction flagging (high similarity + negation mismatch) — reported to the human, never auto-resolved\n3. cluster distillation (cosine ≥ 0.80, clusters ≥ 5) → extractive summary node with `summarizes` edges\n4. decay archival (effective strength < 0.05, untouched > 90 days) → soft-deleted with meta.archived = true (reversible)" — https://docs.rs/mimir-mem-core/latest/src/mimir_core/consolidate.rs.html

A küszöbértékek is egyeznek a forráskód konstansaival (`DUP_COSINE: f32 = 0.92`, `CONTRADICTION_COSINE: f32 = 0.85`, `CLUSTER_COSINE: f32 = 0.80`, `CLUSTER_MIN: usize = 5`). Szó szerint és tartalmilag is **IGAZOLVA**.

### 7. A „dream" szó eredete agent-memóriában

A Letta-PR ténye pontos, elsődleges forrásból:
> „fix(tui): rename reflection to dream" — létrehozva 2026-04-21T17:25:57Z, mergelve 2026-04-21T21:22:23Z — https://github.com/letta-ai/letta-code/pull/1856

A korábbi Letta-terminológia is pontos:
> „Sleep-time compute is a new way to scale AI capabilities…" — Letta blog, közzétéve **2025-04-21** — https://www.letta.com/blog/sleep-time-compute/

**Ez a „tavaszi 2026, Letta a legkorábbi" keret azonban megdől két, egymástól független forrással:**

(a) Egy tudományos preprint, amely kifejezetten „dream"/„dreaming" szóval nevezi meg az LLM-ágens memória-konszolidációt, **2025-12-03**-án jelent meg — négy és fél hónappal a Letta-PR előtt:
> „We present Active Dreaming Memory (ADM), a biologically-inspired dual-store memory system that enables agents to learn from execution failures without fine-tuning… episodic experiences… are consolidated into… rules… during offline 'sleep' periods… Active Dreaming generates synthetic scenarios to test whether a proposed rule actually solves the underlying problem class." — https://engrxiv.org/preprint/view/5919 (dátumbélyeg: „2025-12-03"; preprint-szám: DOI 10.31224/5919)

Ezt egy második, független forrás is megerősíti ugyanazzal a dátummal:
> „December 2025 … DOI: 10.31224/5919" — https://www.researchgate.net/publication/398306877_Active_Dreaming_Memory_Biologically-Inspired_Episodic_Consolidation_for_Lifelong_Learning_in_Autonomous_Agents

Egy harmadik, tőlük is független forrás (2025-08-14-i cikk „post-publication evidence" frissítése) szintén decemberi dátumra hivatkozik:
> „The 'Active Dreaming Memory' preprint (Dec 2025) explores episodic consolidation for lifelong learning agents…" — https://www.greaterwrong.com/posts/TajwK45XBiNEumfim/sleeping-machines-why-our-ai-agents-still-behave-like

(b) Az **ellenőrzendő állítás-lista 4. pontjában idézett ugyanaz a GitHub issue** (#47959) saját létrehozási dátuma — **2026-04-14** — hét nappal **megelőzi** a Letta-PR-t (2026-04-21), és egy már ekkor is létező, „Dream" nevű Claude Code funkcióról tanúskodik (`autoDreamEnabled`):
> „Created: 2026-04-14T14:55:42Z" — https://github.com/anthropics/claude-code/issues/47959

Ez azt jelenti, hogy már az eredeti (sq01/sq02) kutatás saját forrásanyagában is benne volt a Letta-elsőbbségi állítást cáfoló adat, csak nem lett összevetve vele.

**Módszertani megjegyzés:** egy negyedik, gyengébb megbízhatóságú forrás (levelup.gitconnected.com, Medium-alapú, szerkesztői kontroll nélküli blog) 2026-03-26-i dátummal ír a Claude Code „/dream" parancsáról — ha ez a dátum helytálló, ez további egy hónappal tolná korábbra a „dream" szó megjelenését, de mivel ez nem elsődleges forrás és nem tudtam második, tőle független forrással alátámasztani a pontos dátumot, ezt az adatot **nem** vontam be a verdiktbe, csak jegyzem. Egy másik, hasonlóan gyenge forrás (ogham-mcp.dev blog) dátumbélyege (2025-04-02) belső ellentmondásban áll a saját szövegével (2026 áprilisi-májusi eseményeket ír le), ezért ezt a forrást **megbízhatatlannak minősítve kizártam** az értékelésből.

## Amit ez a döntésre jelent

- Az open-second-brain „dream" motorjára vonatkozó minden technikai állítás (LLM-mentesség, snapshot/rollback/dry-run/idempotencia, a fázisok „reporting label" jellege, a reconcile-lépés viselkedése) elsődleges forrásból, a jelenlegi (2026-09-24-i) kódállapotból is megerősíthető volt — ezek stabil, jól dokumentált tények.
- A v0.9.0 kiadási dátumában volt egy valós ellentmondás a két korábbi kutatási kör között; a GitHub release-oldal saját időbélyege alapján **sq01 dátuma (2026-05-15) a helyes**, az sq02-ben szereplő „2025 vége" megfogalmazás forrás nélküli és téves.
- Az Anthropic „Dreams" „input store soha nem módosul" állítása **csak az alapértelmezett működésmódra** igaz; a hivatalos API-referencia egy `update_existing` (jelenleg EAP-korlátozott) opciót dokumentál, amely ezt felülírja. Ez azoknak lényeges, akik biztonsági/determinisztikus-garanciaként hivatkoznának erre az állításra.
- A Harvey „~6x" szám továbbra is egyetlen, módszertan nélküli ügyfél-adat — ezt maga a szaksajtó is explicit módon szóvá teszi, tehát nem csak a korábbi kutatás minősítése, hanem külső, független forrás is alátámasztja a fenntartást.
- A „dream" szó agent-memóriában való „legkorábbi" felbukkanására vonatkozó állítás nem tartható a „2026 tavasza, Letta a legkorábbi dátumozott forrás" formában: egy 2025-12-03-i tudományos preprint (három egymástól független forrással megerősítve) és a Claude Code már 2026-04-14-én dokumentált „Dream" funkciója egyaránt korábbi.
- A Claude Code hivatalos dokumentációjának hallgatása a „dream" funkcióról továbbra is megerősíthető: a jelenlegi hivatalos memória-dokumentáció (code.claude.com) kizárólag „CLAUDE.md" és „Auto memory" fogalmakat ismer.

---

# ELL02 — A mérési és megbízhatósági állítások ellenőrzése

## Módszertani megjegyzés

Az `_ell_kozos.txt` előírása szerint kizárólag az Exa eszközöket (`mcp__Exa__web_search_exa`, `mcp__Exa__web_fetch_exa`) használtam kereséshez és oldalolvasáshoz; a beépített WebSearch/WebFetch-et nem hívtam. Ahol lehetett, az elsődleges forrást (arXiv-verziók, hivatalos gyártói dokumentáció, GitHub-forráskód/kiadási jegyzék, ICLR/ICML hivatalos oldal) magam nyitottam meg, és az sq02–sq04 korábbi idézeteit nem vettem át ellenőrzés nélkül — mindegyiket újra megkerestem és elolvastam. Önálló al-ügynököt nem indítottam (a feladat egyetlen, szűken körülhatárolt kérdéscsoport ellenőrzése egy már elindított munkamenetben); ez a `deep-web-research` skill degradált módja.

## Verdikt-összefoglaló

| # | Állítás | Verdikt | Egy mondat |
|---|---|---|---|
| 1 | MemoryAgentBench FC-SH=54%, FC-MH „at most 7%” vs. ICLR proceedings „at most 28%” | **RÉSZBEN — pontosítva** | Mindkét szám valódi, csak más arXiv-verzióból: v2/v3 (2025-09 / 2026-03) „7%”-ot, v4 (2026-06) és az ICLR 2026 proceedings „28%”-ot mond ugyanarra a mondatra. |
| 2 | arXiv:2606.01435 v1/v2, 78,0%/94,8%, „2,0 pp / 0 pp at 262K”, LongMemEval 26/45 vs 29/45 p=0,45, COLM 2026 workshop-elfogadás | **IGAZOLVA (számok) / RÉSZBEN (elfogadás)** | Minden idézett szám szó szerint megvan a cikk v1/v2 szövegében; a COLM 2026 workshop-poszter-elfogadás egyelőre csak az arXiv „Comments” mezőjének önbevallásán nyugszik, önálló OpenReview-elfogadási döntést nem találtam hozzá. |
| 3 | „Useful Memories…” abstract „fails on 54%” vs. törzsszöveg „fails on 46%”; ICML 2026-elfogadás | **IGAZOLVA (ellentmondás) / NEM ELDÖNTHETŐ (ICML)** | A törzsszöveg Bevezetője szó szerint „fails on 46%”-ot ír, a 4. fejezet és az absztrakt „54%”-ot (mint megmaradó pontosság) — valódi belső ellentmondás; ICML 2026-os elfogadásra nem találtam független megerősítést, és a szerző saját publikációs listáján sincs ICML-címke a cikk mellett (más, ott listázott cikkeknél viszont van). |
| 4 | mem0 2026-os „ADD-only” átállás, „Single-pass ADD-only extraction — one LLM call, no UPDATE/DELETE” | **IGAZOLVA, fontos árnyalással** | A mem0 hivatalos migrációs dokumentációja (OSS v2→v3, Platform v2→v3, changelog, 2026-04-16-i kiadás) szó szerint tartalmazza az idézetet, de egy nyitott GitHub-hiba (#4956) szerint a tiszta ADD-only éles környezetben elavult/ellentmondó tények felhalmozódásához vezetett, ezért a mem0 azóta egy külön „Supersede” háttérmechanizmust vezetett be. |
| 5 | Anthropic: temperature=0 sem garantál determinizmust; Claude 4.7+ nem fogad el temperature/top_p/top_k-t; OpenAI: seed „Deprecated”, „Determinism is not guaranteed” | **IGAZOLVA** | Mindhárom állítás szó szerint megtalálható a jelenleg élő Anthropic- és OpenAI-dokumentációban. |
| 6 | Koszinusz-hasonlóság nem különbözteti meg megbízhatóan a tagadást (Zhu 2018, SemAntoNeg 2022, arXiv:2309.03747, Nature Sci Rep 2025); ellenpélda modern többnyelvű modellekre | **IGAZOLVA + RÉSZLEGES ELLENPÉLDA** | Az összes idézett elsődleges forrás megerősíti a negáció-vakságot; egy 2025 áprilisi cikk (arXiv:2504.00584) szerint a modern általános célú modellek (BGE, E5, GTE) valamivel jobbak a réginél, de a „jelentős negáció-vakság” náluk is fennáll célzott korrekció nélkül — Qwen3-Embedding-specifikus negáció-mérésre nem találtam forrást. |
| 7 | Embedding-determinizmus nyílt modelleknél: batch-méret ~1e-6–1e-7 eltérés; bfloat16 tömeges kötések (PR #3892) | **IGAZOLVA** | A batch-méret okozta eltérés valódi és a sentence-transformers karbantartója is megerősítette (#2312); a bfloat16-tömeges-kötés jelenséget a 2026-08-12-én mergelt PR #3892 és az általa hivatkozott „Reliable Evaluation Protocol for Low-Precision Retrieval” (ACL 2026) dokumentálja. |

---

## Állításonként

### 1. MemoryAgentBench FactConsolidation — „7%” vs. „28%”

Az arXiv:2507.05257 (Hu, Wang, McAuley) submission historyja négy verziót mutat: v1 (2025-07-07), v2 (2025-09-26), v3 (2026-03-17), v4 (2026-06-28). Mind a négyet közvetlenül elolvastam.

- **v1** (2025-07-07): „We observe that all methods fail on the multi-hop situation (with achieving **at most 6% accuracy**).” — https://arxiv.org/html/2507.05257v1
- **v2** (2025-09-26): „…with achieving **at most 7% accuracy**.” — https://arxiv.org/html/2507.05257v2
- **v3** (2026-03-17): „…with achieving **at most 7% accuracy**.” — https://arxiv.org/html/2507.05257v3
- **v4** (2026-06-28): „…with achieving **at most 28% accuracy**.” — https://arxiv.org/html/2507.05257v4
- **ICLR 2026 proceedings PDF** (hivatalos, proceedings.iclr.cc): „We observe that all methods fail on the multi-hop situation (with achieving **at most 28% accuracy**).” — https://proceedings.iclr.cc/paper_files/paper/2026/file/fd1eff9dd295df50a41f2521942fa31d-Paper-Conference.pdf

FC-SH=54,0% (HippoRAG-v2) mind a négy verzióban és a proceedings-ben is konzisztensen szerepel.

**Verdikt indoklása:** mindkét szám ("7%" és "28%") valódi, szó szerint idézhető, csak eltérő verzióból származik. A "7%" a v2/v3-ból (amit a Reddy–Challaram-cikk is kifejezetten "MAB v3"-ként hivatkozik), a "28%" a v4-ből és az ICLR 2026 hivatalos proceedings-változatból. Ez pontosítás, nem cáfolat: mindkét korábbi kutatási kör (sq02 és sq03) helyesen azonosította mindkét számot, csak a verzió-hozzárendelést kell explicitté tenni.

### 2. arXiv:2606.01435 — Reddy & Challaram

Az arXiv abstract-oldal submission historyja: „[Submitted on 31 May 2026 (v1), last revised 2 Aug 2026 (this version, v2)]”, szerzők: Vikas Reddy, Sumanth Reddy Challaram. — https://arxiv.org/abs/2606.01435

v1 címe: „Don't Ask the LLM to Track Freshness: A Deterministic Recipe for Memory Conflict Resolution”. v2 címe: „Reliable Post-Retrieval Assembly for Agent Memory: Separating Evidence Extraction from Policy Execution”.

A v2 „Comments” mezője: „11 pages, 5 tables. **Accepted as a poster at the Lifelong Agent Workshop at COLM 2026.** Code: this https URL” — https://arxiv.org/abs/2606.01435

A számok, szó szerint a v1/v2 szövegéből:

> „The recipe reaches **78.0% on FC-SH with gpt-4o-mini, 94.8% (gpt-4o)**, and 30.2% on FC-MH (gpt-4o-mini, rising to 51.5% with a gpt-4o backbone)…” — https://arxiv.org/html/2606.01435v1

> „A targeted comparison using the same extraction setup shows that changing only the final policy executor contributes **2.0 pp on average and 0 pp at 262K**. Most of the gain therefore comes from separating evidence identification from final policy execution rather than from the freshness operator itself.” — https://arxiv.org/html/2606.01435v2

> „A LongMemEval check finds no significant overall advantage (**26/45 versus 29/45; paired exact McNemar p=0.45**), bounding the result to current-value questions with explicit version metadata.” — https://arxiv.org/html/2606.01435v2

Mind a három szám (78,0/94,8%; 2,0 pp/0 pp; 26/45 vs 29/45, p=0,45) szó szerint és pontosan megegyezik az sq02/sq03 idézeteivel.

**Workshop-elfogadás ellenőrzése:** megtaláltam a COLM 2026 Lifelong Agent Workshop hivatalos honlapját (https://lifelongagent.github.io/) és OpenReview-csoportját (https://openreview.net/group?id=colmweb.org%2FCOLM%2F2026%2FWorkshop%2FLLA), valamint egy harmadik fél által vezetett workshop-naptárat, amely a workshop beadási határidejét 2026. július 11-ként adja meg — ez időrendileg konzisztens azzal, hogy a v1 (2026-05-31) e határidő előtt készült, a v2 (2026-08-02) pedig utána, a „poster accepted” megjegyzéssel. Az OpenReview csoportoldalon azonban nem találtam a konkrét cikkhez tartozó, nyilvánosan listázott elfogadási döntést (a lista csak a csoportot azonosítja, egyedi beadványokat nem listáz publikusan). **Az elfogadás állítása tehát egyelőre csak az arXiv „Comments” mezőjének (szerzői önbevallás) szintjén ellenőrzött, független harmadik forrásból nem sikerült megerősíteni.**

### 3. arXiv:2605.12978 — „Useful Memories Become Faulty”

**Az abstract vs. törzsszöveg ellentmondás valódi és pontosan a leírt módon jelentkezik.**

Absztrakt: „More surprisingly, even when consolidating from ground-truth solutions, GPT-5.4 **fails on 54%** of a set of ARC-AGI problems it had previously solved without memory.” — https://arxiv.org/abs/2605.12978

A Bevezetőben (1. fejezet), a törzsszövegben: „The clearest case isolates the consolidation step from any input-side excuse: GPT-5.4 first solves a set of ARC-AGI problems at 100% accuracy with no memory; after consolidating from ground-truth solutions to those very problems, it then **fails on 46%** of them (Fig. 2).” — https://arxiv.org/pdf/2605.12978

A 4. fejezetben, ugyanarra a kísérletre: „…brings GPT-5.4 **down to 54%** on the very problems it had previously solved (Fig. 2).” — https://arxiv.org/html/2605.12978v1

Vagyis: a Bevezető kifejezetten „fails on 46%”-ot (hibaarány) mond, míg a 4. fejezet és az absztrakt „54%”-ot — de a 4. fejezetben ez explicit MEGMARADÓ PONTOSSÁGKÉNT szerepel (100%→54%), ami aritmetikailag a Bevezető „46%”-os hibaarányával egyezik. Az absztrakt „fails on 54%” megfogalmazása tehát a cikk saját törzsszövegével (mindkét előfordulásával) inkonzisztens — ez egy valódi, a jelenlegi (egyetlen, v1) verzióban is fennálló belső pontatlanság, nem korábbi kutatási hibaforrás. A cikknek egyelőre nincs v2 revíziója.

**ICML 2026-elfogadás:** nem találtam sem OpenReview-elfogadási döntést, sem az ICML 2026 hivatalos honlapján elfogadott cikkek listáján konkrét említést erre a címre. A szerző (Hao Peng) saját publikációs listáján a cikk „2026” alatt szerepel, de — szemben más, ugyanazon a listán szereplő, explicit „In Proceedings of the International Conference on Machine Learning (ICML), 2026” címkével ellátott cikkekkel — ennél a tételnél nincs ICML-címke, csak egy puszta „paper” link. — https://haopeng-nlp.github.io/publications/ Az ICML 2026 hivatalos határidő-oldala szerint a szerzői értesítés dátuma 2026-04-30 volt (https://icml.cc/Conferences/2026/Dates), és a cikk 2026-05-13-án került fel az arXiv-ra — ez az időzítés összeegyeztethető egy elfogadás utáni közzététellel, de önmagában nem bizonyíték. **Összességében az ICML 2026-elfogadás állítása jelen pillanatban nem igazolható független forrásból, és a szerzői oldal hiányzó címkéje inkább óvatosságra int.**

### 4. mem0 „ADD-only” architektúra

A mem0 hivatalos, jelenleg élő migrációs dokumentációja (docs.mem0.ai, valamint a GitHub-repó forráskódja) szó szerint megerősíti az idézetet:

> „**Extraction**: Single-pass ADD-only (one LLM call, no UPDATE/DELETE)” — https://github.com/mem0ai/mem0/blob/main/docs/migration/oss-v2-to-v3.mdx

> „The previous algorithm used two LLM calls: one to extract candidate facts, one to decide ADD/UPDATE/DELETE actions against existing memories. The new algorithm collapses this into a single call that only adds.” — ugyanott

> „| **Extraction** | Two LLM passes (extract + merge) | Single-pass ADD-only (one LLM call) | | **Memory mutations** | ADD, UPDATE, DELETE | ADD only: nothing is overwritten or deleted |” — https://docs.mem0.ai/migration/platform-v2-to-v3

A TypeScript SDK v3.0.0 kiadási jegyzéke pontos dátummal: „Published: 2026-04-16T11:52:37Z … Single-pass ADD-only extraction. One LLM call per `add()`. No separate UPDATE/DELETE pass.” — https://github.com/mem0ai/mem0/releases/tag/ts-v3.0.0

**Fontos árnyalás, amit az sq02/sq03 nem tárt fel:** egy nyitott, éles GitHub-hiba szerint a tiszta ADD-only extrakció önmagában valós problémát okozott:

> „After upgrading OSS to v3, the extraction pipeline is single-pass ADD-only — add() no longer emits UPDATE / DELETE events. For facts representing a mutable state (e.g. current employer, current city, relationship status), this means contradictory memories accumulate over time instead of the newer fact superseding the older one.” — https://github.com/mem0ai/mem0/issues/4956 (nyitva, 2026-04-24 – 2026-08-19 között aktív)

Erre válaszul a mem0 csapata két, egymással versengő javítást is elindított: „#4965: fix: restore ADD/UPDATE/DELETE extraction capabilities” és „#4969: feat: implement append-only soft-supersede to resolve stale facts without deletion” — és a jelenlegi hivatalos „Dream” funkció dokumentációja már egy különálló, mindig bekapcsolt „Supersede” háttérmechanizmust ír le, ami „Marks an older fact as outdated when a newer one contradicts it” — https://docs.mem0.ai/platform/features/dream. Vagyis a 2026-os „ADD-only” állítás pontos és forrással alátámasztott, de nem statikus végállapot: a tiszta ADD-only kiadás gyakorlati problémákba ütközött, és a mem0 azóta egy kiegészítő, automatikus felülíró-jelölő réteget épített rá.

### 5. Determinizmus — gyártói dokumentáció

**Anthropic**, jelenleg élő glosszárium: „Users may encounter non-determinism in APIs. **Even with temperature set to 0, the results will not be fully deterministic** and identical inputs may produce different outputs across API calls. This applies both to Anthropic's first-party inference service and to inference through third-party cloud providers.” — https://platform.claude.com/docs/en/about-claude/glossary

**Anthropic**, Messages API útmutató: „The `temperature`, `top_p`, and `top_k` sampling parameters **are not supported on Claude 4.7 and later models** and Claude Mythos Preview. Setting them to a non-default value returns a 400 error.” — https://platform.claude.com/docs/en/build-with-claude/working-with-messages

**OpenAI**, hivatalos API-referencia (Create chat completion végpont): „**Deprecated** seed: optional number or null … If specified, our system will make a best effort to sample deterministically… **Determinism is not guaranteed**, and you should refer to the `system_fingerprint` response parameter to monitor changes in the backend.” — https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create/

Mindhárom idézet szó szerint, jelenleg élő, elsődleges gyártói forrásból megerősítve.

### 6. Beágyazás és tagadás

**Elsődleges források a negáció-vakságra**, mindegyiket közvetlenül elolvastam:

> Zhu, Li, de Melo, „Exploring Semantic Properties of Sentence Embeddings”, ACL 2018 (Short Papers) — a cikk létezik, a szerzők és a konferencia-adatok megegyeznek az sq04-ben idézettekkel; a dolgozat kifejezetten teszteli, hogy a koszinusz-hasonlóság megkülönbözteti-e a tagadott mondatokat. — https://aclanthology.org/P18-2100.pdf

> Mahajan, Bansal, Karmaker, „The Daunting Dilemma with Sentence Encoders…”, arXiv:2309.03747 (2023-09-07): „…all the sentence encoders **failed the antonym replacement** and jumbling criteria.” — https://arxiv.org/abs/2309.03747

Az SemAntoNeg (2022) és a Nature Sci Rep 2025 (NAS Scorer) cikkeket az sq04 már közvetlenül idézte és linkjeiket ellenőriztem; a linkek élnek, a hivatkozott cím és konferencia (ACL blackboxnlp 2022, ill. Nature Scientific Reports 2025) egyezik.

**Keresett ellenpélda — modern többnyelvű beágyazó modellek:**

Találtam egy 2025 áprilisi cikket, amely kifejezetten modern, „universal” beágyazó modelleket (BGE, E5, GTE, mxbai) tesztel negáció-tudatosságra:

> „Recent advancements in universal text embeddings have demonstrated superior performance over contextual text embeddings in various tasks. However, due to the bias in popular evaluation benchmarks, the negation awareness capacity of these models remains unclear... Our findings reveal a **significant lack of negation awareness** in these models, often interpreting negated text pairs as semantically similar.” — https://arxiv.org/html/2504.00584v1

A cikk saját mért adatai (SemAntoNeg teszt, eredeti — korrekció nélküli — pontosság): bge-large-en-v1.5 = 64,68%, multilingual-e5 = 68,87%, e5-large-v2 = 60,83%, gte-base = 47,12% — összevetve a régebbi, kontextuális modellekkel (all-mpnet-base-v2 = 31,32%, all-roBERTa-large = 35,32%). Vagyis a modern általános célú, többek közt többnyelvű (multilingual-e5) modellek **valamivel jobbak**, mint a 2018–2019-es generáció, de a szerzők saját megfogalmazása szerint ez még mindig „jelentős” hiányosság — külön korrekciós módszer (dimenzió-súlyozás) nélkül egyik modern modell sem éri el a megbízható szintet.

**Qwen3-Embedding-specifikusan** nem találtam publikált negáció-mérést — sem megerősítést, sem cáfolatot. A Qwen3-Embedding hivatalos technikai jelentése (arXiv:2506.05176) és a GitHub-repó (QwenLM/Qwen3-Embedding) kizárólag általános MTEB-stílusú retrieval/klaszterezési/reranking-benchmarkokat közöl, negáció-specifikus tesztet nem. **Erre nincs forrás.**

### 7. Embedding-determinizmus nyílt modelleknél

**Batch-méret hatása** — a hiba valódi, a sentence-transformers karbantartója (Tom Aarsen) megerősítette:

> „My expectation is that batch size has no impact on embedding results, but this is not the case… `e0 = st.encode(texts, batch_size=32)`, `e1 = st.encode(texts, batch_size=1)` → `False False True`” — https://github.com/huggingface/sentence-transformers/issues/2312 (2023-09-22, lezárva: tomaarsen, 2024-01-18)

**bfloat16 „tömeges kötések”** — a PR valóban létezik és a leírt indoklással mergelve lett:

> „The similarity primitives in `sentence_transformers.util`… leave dense tensors at their incoming dtype. When embeddings are produced in float16/bfloat16… cosine/dot scoring is therefore performed in low precision. Reduced-mantissa formats coarsely bucket values in the narrow score range, **collapsing distinct similarity scores into spurious ties**.” — https://github.com/UKPLab/sentence-transformers/pull/3892 (létrehozva: 2026-07-31, mergelve: 2026-08-12, karbantartói megerősítéssel: „The diagnosis here is spot on as far as I can tell”)

A PR kifejezetten egy 2026-os, lektorált forrásra hivatkozik: „*Reliable Evaluation Protocol for Low-Precision Retrieval* (Yang et al., ACL 2026)” — ezt a cikket magát nem sikerült külön elsődleges forrásból (pl. ACL Anthology-oldaláról) ellenőriznem ebben a körben, de a PR-t mergelő karbantartó szakmai megerősítése önmagában is releváns, közvetlen (T1/T2 vegyes) forrás.

---

## Amit ez a döntésre jelent

- A MemoryAgentBench „7% vs. 28%” nem egymásnak ellentmondó, hanem egymást követő arXiv-verziók eltérő mérése — a rendszer tervezésénél a legfrissebb (v4/ICLR proceedings, 28%) számot érdemes irányadónak tekinteni, ha az „aktuális állás szerinti” legjobb LLM-alapú multi-hop teljesítményre hivatkoznak.
- A Reddy–Challaram-cikk (arXiv:2606.01435) kvantitatív állításai (78,0/94,8%; 26/45 vs 29/45 p=0,45; 2,0 pp/0 pp) szó szerint, verzió- és dátumhelyesen igazolhatók a saját publikus szövegéből; a COLM 2026 workshop-elfogadás ezzel szemben egyelőre csak a szerzők önbevallásán nyugszik.
- Az ARC-AGI konszolidációs kudarc-mérés (100%→54%/46%) alapvető ténye (a konszolidáció ronthatja a memóriát) szilárdan áll, de a cikk maga belsőleg pontatlan a 46% és 54% szóhasználatában, és az ICML 2026-elfogadás jelenleg nem igazolható — ezt a hivatkozást célszerű „arXiv-preprint, elfogadási státusz nem megerősített” jelöléssel használni.
- A mem0 ADD-only architektúraváltás valódi és jól dokumentált, de nem tekinthető lezárt, végleges megoldásnak: éles környezetben elavult tények felhalmozódásához vezetett, és a mem0 azóta kiegészítő, automatikus felülírás-jelölő mechanizmust (Supersede) épített rá — ez direkt releváns analógia egy tervezett determinisztikus konszolidációs rétegre nézve.
- A gyártói determinizmus-korlátozó nyilatkozatok (Anthropic, OpenAI) pontosan és aktuálisan igazolhatók, tehát a rendszer tervezésénél biztonsággal feltételezhető, hogy semmilyen LLM-hívás (temperature=0 mellett sem) nem ad garantáltan reprodukálható kimenetet.
- A koszinusz-alapú tagadás-vakság jól alátámasztott alapprobléma, de nem abszolút: a modern, többek közt többnyelvű általános célú beágyazó modellek (BGE, E5 család) mérhetően jobbak a régieknél, csak külön korrekció (finomhangolás vagy súlyozás) nélkül még mindig nem megbízhatóak — Qwen3-Embedding-specifikus adat hiányzik.
- A nyílt beágyazó modellek determinizmus-hiánya (batch-méret, alacsony pontosságú súlyozás) valós, dokumentált és a könyvtár karbantartói által is elismert jelenség, tehát egy determinisztikus küszöb-alapú döntési rétegnél célszerű rögzített batch-méretet és legalább float32 pontosságú hasonlóság-számítást előírni.

---

# ELL03 — arXiv:2606.01435: a +10,8 pp és a 61% / 71–82% ellenőrzése

**Cikk:** Vikas Reddy, Sumanth Reddy Challaram — v1 (2026-05-31): *„Don't Ask the LLM to Track Freshness: A Deterministic Recipe for Memory Conflict Resolution"*; v2 (2026-08-02, átcímezve): *„Reliable Post-Retrieval Assembly for Agent Memory: Separating Evidence Extraction from Policy Execution"*.
**Ellenőrzés dátuma:** 2026-09-24. **Eszköz:** kizárólag Exa (`web_search_exa`, `web_fetch_exa`); a GitHub-repó nyers README-jének olvasása is Exa `web_fetch_exa`-val történt (nem `curl`).

## Verdikt-összefoglaló

| # | Állítás | Verdikt | Egy mondat |
|---|---|---|---|
| A | „determinisztikus `max(serial)` szabály +10,8 pp az LLM-ítélet fölött ütközés-feloldásban" | **RÉSZBEN IGAZOLVA** | A +10,8 pp szám és a helye valós (v1 §1.2, v2 1. táblázat, GitHub README), de a cikk saját, csak v2-ben elvégzett kontrollkísérlete szerint ez NEM a determinisztikus szabálynak, hanem a kinyerés-vs-végrehajtás szétválasztásának tulajdonítható — maga a determinisztikus végrehajtó csak +2,0 pp-ot (262K-nál 0 pp-ot) ad hozzá. |
| B | „262K kontextusban az LLM 61%-ra esik, a determinisztikus 71–82% marad" | **RÉSZBEN IGAZOLVA** | Mindkét szám valódi és szó szerint megtalálható (v1, v2, GitHub), de a „71–82%" nem a 262K-nál mért érték (ott pontosan 82%), hanem a determinisztikus pipeline teljes 6K–262K tartományban mért szórása — a mondat úgy van megfogalmazva, mintha mindkét szám ugyanarra a kontextushosszra vonatkozna. |

## Állításonként

### A) „+10,8 pp a determinisztikus max(serial) szabálytól az LLM-ítélet fölött"

**1. Szerepel-e a szám, és pontosan mit hasonlít össze?**

Igen, mindkét verzióban szerepel, azonos táblázati adatokkal.

- **v1 HTML** (`https://arxiv.org/html/2606.01435v1`, §1.2 „A matched-setup pipeline comparison"), szó szerint:
  > „A matched-setup comparison (same backbone, same retrieval, same chunking, same TOP_K, same n=100 per cell) shows that replacing the LLM-judgment-based answer pipeline with a candidate-extraction + Python max(serial) pipeline yields +10.8 percentage points on FC-SH (67.2 → 78.0, fact-level chunking, gpt-4o-mini)."

  Táblázat (v1, §1.2):

  | Setup (fact-level chunking, gpt-4o-mini) | 6K | 32K | 64K | 262K | AVG |
  |---|---|---|---|---|---|
  | BM25 retrieval + MAB BM25 answer prompt (LLM-judgment) | 63 | 70 | 75 | 61 | 67.2 |
  | BM25 retrieval + extract-candidates + Python max(serial) (Headline) | 71 | 78 | 81 | 82 | 78.0 |
  | Δ | +8 | +8 | +6 | +21 | **+10.8 pp** |

- **v2 HTML** (`https://arxiv.org/html/2606.01435v2`, 1. táblázat / „Controlled whole-pipeline comparison"): ugyanez a 67,2 → 78,0 = 10,8 pp jelenik meg, immár egy 3 soros táblázat első és harmadik sorában (lásd lent), és az absztraktban is: „A controlled whole-pipeline comparison … improves single-hop accuracy by 10.8 percentage points (pp) on average and 21 pp at 262K."
- **GitHub-repó README** (`https://raw.githubusercontent.com/cvikasreddy/memory-conflict-resolution/main/README.md`, a v2-höz tartozó, jelenlegi verzió) — független, harmadik forrás, pontosan ugyanazokkal a cellaértékekkel:
  > „Structured assembly (SH, fact-level) | gpt-4o-mini | 71 | 78 | 81 | 82 | 78.0 [73.7, 81.8]" és „Direct LLM answer (T=0.7) | gpt-4o-mini | 63 | 70 | 75 | 61 | 67.2 [62.5, 71.7]".

**Mit hasonlít össze pontosan:** ugyanaz a backbone (gpt-4o-mini), ugyanaz a BM25 top-10 retrieval, ugyanaz a fact-level chunking, MAB FactConsolidation single-hop (FC-SH) alfeladat, n=100/cella, mind a 4 kontextushosszon (6K/32K/64K/262K). A két kar viszont **három dologban egyszerre** különbözik: (1) a végrehajtó (LLM-döntés vs. Python `max(serial)`), (2) a prompt/kimeneti formátum (szabad szöveges válasz T=0,7 vs. strukturált JSON-kinyerés T=0,0), (3) az LLM feladata (döntsön-és-válaszoljon vs. csak kinyerjen). A cikk saját szövege ezt v1-ben explicit módon kimondja:

> „This comparison therefore measures the whole pipeline-level effect of moving freshness reasoning out of LLM judgment and into structured code, not the resolver step in isolation. Cleanly isolating the resolver's own contribution … is left to future work." (v1, §1.2)

**Tehát az állítás számszerűen igaz, de a megfogalmazás („a determinisztikus szabály +10,8 pp-ot ad") félrevezető**: a +10,8 pp nem a szabálynak (max-függvénynek), hanem a teljes pipeline-átalakításnak (kinyerés + végrehajtás együtt) tulajdonítható — ezt maga a szerzőpáros mondja ki v2-ben, lásd 2. pont.

### B) „262K-nál az LLM 61%-ra esik, a determinisztikus 71–82% marad"

**1. Szerepel-e a szám, és pontosan mit hasonlít össze?**

Igen, mindkét szám valódi, de két különböző mérési dimenzióból származik.

- A **61%** a fenti táblázat „LLM-judgment" (Direct LLM answer, T=0,7) sorának 262K-cellája — ez tényleg specifikusan a 262K kontextushosszra vonatkozik.
- A **71–82%** viszont NEM a determinisztikus pipeline 262K-nál mért értéke (ott pontosan **82%**), hanem a determinisztikus pipeline **teljes 6K→262K tartománybeli** szórása (71% a 6K-nál, 82% a 262K-nál — a kettő közötti minimum/maximum). v1 (§1.5, „Contributions", 3. pont), szó szerint:
  > „Mechanistic evidence on where the LLM fails. The combined extract-and-judge baseline holds 63–75% at 6K–64K but drops to 61% at 262K; our extract-then-aggregate pipeline does not degrade (71–82% across all lengths; 92–99% with gpt-4o)."
- **v2 HTML**, ugyanez a jelenség, más megfogalmazásban: „The direct-answer baseline falls from 75% at 64K to 61% at 262K, whereas the structured pipeline reaches 82%." — itt a szerzők már NEM 71–82% tartományként, hanem konkrétan „82%"-ként hivatkoznak a 262K-s pontra.
- **GitHub README** táblázata (3. független forrás) ugyanezt az adatsort adja vissza: Direct LLM answer 262K=61; Structured assembly 6K/32K/64K/262K = 71/78/81/**82**.

**Tehát a „71–82% marad 262K-nál" megfogalmazás pontatlan**: 262K-nál a determinisztikus pipeline egyetlen értéke 82% (nem egy tartomány), és a 71% a rövidebb (6K-s) kontextusból való. A mondat úgy állítja egymás mellé a két számot, mintha mindkettő „262K kontextusban" mért érték lenne, holott a 71–82% az egész hosszúság-skálát (6K–262K) fedi le. Az állítás lényegi tartalma — hogy az LLM-alapú pipeline 262K-nál visszaesik, míg a determinisztikus/strukturált pipeline nem degradálódik, sőt a legjobb értékét (82%) épp 262K-nál éri el — helytálló és jól dokumentált mindkét verzióban, csak a számpár összefésülése pontatlan.

### 2. Ellentmond-e A)/B) a C)-nek, vagy más összehasonlításról szólnak?

**Más, de egymást kiegészítő összehasonlításokról van szó — és C) kifejezetten korrigálja az A) triviális („a szabály önmagában +10,8 pp") olvasatát.**

A v2-es 1. táblázat (mindhárom sor egyszerre látszik, ez maga a bizonyíték a különbségre):

| Pipeline | 6K | 32K | 64K | 262K | Avg. |
|---|---|---|---|---|---|
| Direct LLM answer (T=0.7) | 63 | 70 | 75 | 61 | 67.2 |
| Extract + LLM policy execution (T=0) | 70 | 75 | 77 | 82 | 76.0 |
| Extract + deterministic policy execution (T=0) | 71 | 78 | 81 | 82 | 78.0 |

- **A) / B)** az **1. és 3. sor** különbsége: „direkt, egylépéses LLM-válasz” vs. „strukturált kinyerés + determinisztikus végrehajtás” → **+10,8 pp** átlagban, **+21 pp** 262K-nál (82−61). Ez a teljes pipeline-effektus (kinyerés ÉS végrehajtás együtt változik).
- **C)** a **2. és 3. sor** különbsége: „strukturált kinyerés + LLM választja ki a győztest” vs. „strukturált kinyerés + Python `max(serial)`” → csak a végrehajtó cserélődik, a kinyerés (extrakciós lépés) azonos marad. Ez ad **+2,0 pp**-ot átlagban (78,0−76,0) és **0 pp**-ot 262K-nál (82−82) — pontosan egyezik a feladatban idézett C) szó szerinti idézettel:
  > „A targeted comparison using the same extraction setup shows that changing only the final policy executor contributes 2.0 pp on average and 0 pp at 262K. Most of the gain therefore comes from separating evidence identification from final policy execution rather than from the freshness operator itself." (v2)

  Ezt a GitHub README is megerősíti, sőt még nyersebben fogalmaz:
  > „This matters for reading the code, so it is worth stating plainly: the gain is **not** mainly from replacing the LLM with `max()`. Holding the extraction prompt and T = 0 fixed and changing only the policy executor is worth 2.0 pp on average and **0 pp at 262K**. The large effect comes from restructuring the decision — externalizing semantic matching into a constrained intermediate representation before any selection happens."

**Nincs numerikus ellentmondás** — mind az A)/B), mind a C) számai valósak és egymással aritmetikailag konzisztensek (ugyanabból a táblázatból erednek: 67,2 → 76,0 → 78,0). **De van fogalmi/attribúciós feszültség**: ha A)-t úgy olvassuk, hogy „a determinisztikus max(serial) SZABÁLY ad +10,8 pp-ot”, azt C) kifejezetten cáfolja — maga a szabály/végrehajtó cseréje csak +2,0 pp (262K-nál 0 pp), a fennmaradó ~8,8 pp a kinyerési lépés szétválasztásából (a candidate-extraction bevezetéséből) származik, nem a „determinizmusból”. Ezt jelzi az is, hogy a cikk címe és fő tézise v1→v2 között pontosan ebbe az irányba tolódott el (lásd 3. pont).

### 3. Változtak-e a számok v1 és v2 között?

**A konkrét számok (67,2 / 78,0 / +10,8 pp / 61% 262K-nál / 71–82% tartomány) NEM változtak v1 és v2 között** — mindkét verzióban azonosak, és a GitHub-repó jelenlegi (v2-höz tartozó) README-je is ugyanezeket a cellaértékeket közli.

**Ami változott:**
- v1-ben a szerzők explicit módon jelezték, hogy a végrehajtó önálló hozzájárulásának elkülönítése *„left to future work"* — vagyis a C)-ben idézett célzott (2,0 pp / 0 pp) összehasonlítás **v1-ben még nem létezett**.
- v2 **hozzáadta** ezt a célzott összehasonlítást (az 1. táblázat 2. sora: „Extract + LLM policy execution”), és ez alapján explicit korrekciót fogalmazott meg: „Most of the gain therefore comes from separating evidence identification from final policy execution rather than from the freshness operator itself.”
- Ezzel összhangban a **cím és a fő tézis is megváltozott**: v1 címe *„Don't Ask the LLM to Track Freshness: A Deterministic Recipe…”* (a determinizmust emeli ki fő mechanizmusként — ez áll közelebb az A) állítás megfogalmazásához), v2 címe *„Reliable Post-Retrieval Assembly … Separating Evidence Extraction from Policy Execution”* (a kinyerés/végrehajtás szétválasztását emeli ki, nem a determinizmust — ez áll közelebb a C) állításhoz). A GitHub README-ben is megjelenik ugyanez a hangsúlyeltolódás egy külön „What the ablations actually show” szakaszban.
- **D) állítás** (78,0% gpt-4o-mini, 94,8% gpt-4o FC-SH-n) **változatlan** v1→v2 között; szó szerint szerepel mindkét verzióban (v1 §1.3 „Three empirical findings” táblázat és bevezető szöveg; v2 2. táblázat „Headline results”: „FC-SH, structured | gpt-4o-mini | 78.0/82 … FC-SH, structured | gpt-4o | 94.8/93”), és a GitHub README fejléc-táblázata is megerősíti ugyanezekkel a Wilson-CI értékekkel (78,0 [73,7, 81,8]; 94,8 [92,1, 96,5]).

## Amit ez a mérési dokumentumra jelent

1. A 2026-08-23-i jegyzet A) és B) számai nem kitaláltak: mindkettő szó szerint megtalálható a cikk mindkét verziójában és a hozzá tartozó kódtárban — forrásuk azonosított, nem „NINCS FORRÁS”.
2. A) állítás jelenlegi megfogalmazása pontatlan attribúciót tartalmaz: a +10,8 pp-ot a „determinisztikus max(serial) szabálynak” tulajdonítja, miközben a cikk saját (csak v2-ben elvégzett) célzott kontrollja szerint a szabály/végrehajtó önmagában csak +2,0 pp-ot (262K-nál 0 pp-ot) ér; a nagyobbik rész a kinyerés-vs-végrehajtás szétválasztásából, nem a determinizmusból ered.
3. B) állítás két, különböző kontextusmetszetből származó számot fésül össze egyetlen „262K-nál” mondatba: a 61% valóban 262K-specifikus, a 71–82% viszont a teljes 6K–262K tartomány szórása (262K-nál pontosan 82%).
4. A mérési dokumentumban célszerű A) és B) mellé/helyett a pontosabb, cikk-hű megfogalmazást rögzíteni: „a teljes strukturált pipeline (kinyerés + determinisztikus végrehajtás) +10,8 pp-ot ad az egylépéses LLM-válaszhoz képest (262K-nál +21 pp, 61%→82%); ebből azonban csak +2,0 pp (262K-nál 0 pp) tulajdonítható magának a determinisztikus végrehajtónak — a többi a kinyerés-végrehajtás szétválasztásából ered” — ezzel A), B) és C) egyetlen, önmagával konzisztens állítássorba rendezhető.

## Meglátogatott linkek

| Cím | URL | Tier | Eszköz |
|---|---|---|---|
| arXiv absztrakt (2606.01435, v2 aktuális) | https://arxiv.org/abs/2606.01435 | Elsődleges (preprint, arXiv) | Exa web_fetch_exa |
| v1 HTML teljes szöveg | https://arxiv.org/html/2606.01435v1 | Elsődleges (preprint, arXiv) | Exa web_fetch_exa |
| v2 HTML teljes szöveg | https://arxiv.org/html/2606.01435v2 | Elsődleges (preprint, arXiv) | Exa web_fetch_exa |
| GitHub companion repo (README, HEAD/v2-höz tartozó) | https://raw.githubusercontent.com/cvikasreddy/memory-conflict-resolution/main/README.md | Elsődleges (szerzői kódtár, nyers fájl) | Exa web_fetch_exa |
| GitHub companion repo (repó-oldal, v1-es README-változattal a keresési találatban) | https://github.com/cvikasreddy/memory-conflict-resolution | Elsődleges (szerzői kódtár) | Exa web_search_exa |
| alphaXiv tükörzet (v2 absztrakt megerősítése) | https://www.alphaxiv.org/abs/2606.01435 | Másodlagos (tükör/aggregátor) | Exa web_search_exa |
| scite.ai jelentés (absztrakt megerősítése) | https://scite.ai/reports/reliable-post-retrieval-assembly-for-agent-ZGJPb6v9 | Másodlagos (aggregátor) | Exa web_search_exa |
| AIssential összefoglaló (v1 tartalom megerősítése) | https://aissential.tech/articles/d859758e-2202-429b-bc73-96cc583dd1bc | Másodlagos (harmadik fél összefoglaló) | Exa web_search_exa |
| natanloterio/scene-memory — független reprodukciós projekt, hivatkozik 2606.01435-re | https://github.com/natanloterio/scene-memory/blob/436f5443/docs/research-journey.md | Másodlagos (független, nem hivatkozott a fő állításokra nézve, csak kontextus) | Exa web_search_exa |
| alphaXiv szerzői profil (Sumanth Reddy Challaram) | https://www.alphaxiv.org/@sumanth-reddy-challaram | Másodlagos (profil) | Exa web_search_exa |
