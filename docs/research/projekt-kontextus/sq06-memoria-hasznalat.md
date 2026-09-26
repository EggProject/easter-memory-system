# SQ06 — Mitől használja egy agent ténylegesen a memória-eszközöket?

*Módszertani megjegyzés (kötelező bevezető): ez a kutatás degradált módban készült. A `deep-web-research` skill elvei szerint dolgoztam (elsődleges forrás előny, szó szerinti idézet + URL minden állításhoz, T1/T2/T3 jelölés, két független forrás vagy „nincs forrás"), de al-ügynököket (subagentek párhuzamos indítását) nem indítottam — egyetlen kutató szálon, szekvenciális Exa-kereséssel és -olvasással dolgoztam. Az Exa (`mcp__Exa__web_search_exa`, `mcp__Exa__web_fetch_exa`) elérhető volt és kizárólagosan ezt használtam keresésre/olvasásra; beépített WebSearch/WebFetch-et nem hívtam.*

## Rövid válasz

Közvetlen, kontrollált mérést arra, hogy egy rövid, session-eleji sablonszöveg (,,van memória, N bejegyzés, használd a keresőt") önmagában mennyivel növeli egy memória-eszköz önkéntes meghívási arányát, nem találtam — ez pontosan az a rés, amit ez a kutatási kérdés keres, és amire nincs közvetlen forrás. Van viszont bőséges közvetett bizonyíték: (1) az általános eszközhasználati kutatás azt mutatja, hogy a modellek alapból erősen alul- vagy túlhasználják az elérhető eszközöket modellcsaládtól függően, és a puszta promptolás („ne hívj eszközt feleslegesen") ezt csak durván, nem szelektíven tudja korrigálni; (2) mindhárom nagy gyártó (Anthropic, OpenAI, Google) a gyakorlatban explicit, kikényszerített szöveget told a rendszerpromptba, amikor memória-eszköz van jelen — ami önmagában bizonyítja, hogy a puszta eszköz-elérhetőség a gyártók szerint sem elég; (3) a Google Gemini CLI forráskódjában dokumentált mérnöki döntés kifejezetten kimondja, hogy erősebb modellnél (Gemini 3) elhagyható az explicit memória-instrukció, mert a modell magától is megbízhatóan használja az eszközt — vagyis a szükséges „nógatás" mennyisége modellfüggő; (4) a beadott szöveg pozíciója és hossza jól mért hatás: a „Lost in the Middle" U-alakú görbe és a „context rot" jelenség szerint a session eleji rövid szöveg relatív súlya csökken, ahogy utána nő a kontextus, bár egy 2026-os kontrollált null-eredmény ezt 150k tokenig nem tudta reprodukálni; (5) a kockázatok oldalán irreleváns tartalom mérten rontja a teljesítményt (GSM-IC, Shi et al. 2023), elavult/ütköző memória dokumentáltan felülírhatja az aktuális, helyesen betöltött instrukciót (Codex Desktop GitHub-jegy), és a beadott memória-tartalmon át indirekt prompt injection is dokumentált, mind akadémiai támadásként (MINJA, NeurIPS 2025), mind valós incidensként (ChatGPT memória-feature, Rehberger 2024).

## 1. Van-e mérés az önkéntes eszközhasználati gyakoriságra, és mennyit változtat rajta egy emlékeztető/címlista/utasítás?

### 1.1 Alapszintű eszközhasználati arány — erős modellfüggés, alul- és túlhasználat egyaránt

A „WHEN2TOOL" benchmark (2026, arXiv 2605.09252) kifejezetten azt méri, mikor hív egy agent eszközt, ha nem kellene, és mikor nem hív, ha kellene volna:

> „Finding 1: Models default to tool overuse. Under the Default (⋆) setting in Prompt-only baselines, models make 2,100–4,400 total tool calls across the 2,250-task single-hop test set, more than one calls per task. Even on easy tasks, Qwen3-1.7B makes 864 tool calls out of 750 easy tasks... The model's default behavior is 'tools are available, therefore use them,' even when the task is simple enough to solve directly."

Ugyanez a tanulmány közvetlenül a kérdésre válaszol: mennyit ér a puszta promptolás (emlékeztető/utasítás)?

> „Finding 2: Prompt engineering reduces tool calls indiscriminately, and hard tasks pay a disproportionate price... On Qwen3-4B-Instruct, the cost is −17.3 on easy but reaches −42.4 on hard, meaning hard tasks lose 2.5× more accuracy per saved call."

Forrás: „LLM Agents Already Know When to Call Tools – Even Without Reasoning", arXiv:2605.09252, https://arxiv.org/pdf/2605.09252v2 (T1, arXiv, 2026).

A „ToolFailBench" (arXiv 2607.04686) 19 modellen mérve mutatja, hogy a legjobb modell is csak 86,33%-os „Clean Tool-Use Rate"-et ér el, és a modellcsaládok között drámai eltérés van:

> „Llama-3.1-70B and Qwen2.5-72B differ by 89 percentage points on control-task accuracy... two-proportion z=−19.9, p<10⁻⁸⁰."

Forrás: „ToolFailBench: Diagnosing Tool-Use Failures in LLM Agents", arXiv:2607.04686, https://ar5iv.labs.arxiv.org/html/2607.04686 (T1, 2026).

A reprezentáció-terelős tanulmány (arXiv 2608.25198) direkt megméri az eszközhívási arányt (call rate) mint kontrollálható, folytonos mennyiséget:

> „Adding the direction with strength α moves the call rate monotonically from near 0% to over 90% while keeping calls well-formed... baseline call rates span both tool-underuse and tool-overuse, from 0.07 on Qwen3-4B to 0.83 on the 30B MoE."

Forrás: „Tunable Tool-Call Rates in LLM Agents via Representation Steering", arXiv:2608.25198, https://arxiv.org/html/2608.25198v1 (T1, 2026-08-25).

**Ez három egymástól független kutatócsoport konvergáló eredménye**: az alap eszközhívási hajlandóság erősen modell- és családfüggő, tág skálán mozog (7%-tól 98%-ig kontroll-feladatokon), és a puszta szöveges promptolás („ne hívj feleslegesen") ezt csak durván, a nehéz (valóban szükséges) eseteket is sújtva tudja csökkenteni.

### 1.2 Memória-specifikus benchmarkok: az eszközhívás megtörténik, de a *hasznos* eszközhívás nem triviális

A LongMemEval (ICLR 2025) — az egyik legidézettebb hosszútávú-memória benchmark — nem az önkéntes hívás gyakoriságát méri közvetlenül (a hívás a keretrendszer szintjén kötelező), hanem azt, hogy a visszakeresés/válasz mennyire jó:

> „...commercial chat assistants and long-context LLMs showing a 30% accuracy drop on memorizing information across sustained interactions."

Forrás: LONGMEMEVAL, ICLR 2025, https://proceedings.iclr.cc/paper_files/paper/2025/file/d813d324dbf0598bbdc9c8e79740ed01-Paper-Conference.pdf (T1, peer-reviewed).

Egy harmadik fél implementáció (ReMe, agentikus/ReAct módban futtatva a LongMemEval-t) közvetve mégis mutat valamit az önkéntes eszközhasználati mintázatról: a kérdéstípusonkénti pontosság 0,633 és 1,000 között szór, és az átlagos eszközhívás-szám kérdéstípusonként 1,89-től 4,97-ig terjed — vagyis még kötelezően eszközös módban futtatva is nagy szórás van abban, hányszor „próbálkozik" az agent a memóriában (github.com/agentscope-ai/ReMe, T2, közösségi implementáció, nem lektorált).

Az eredeti **MemGPT** (arXiv 2310.08560, később ICLR 2024) explicit kimondja, hogy az önkéntes (self-directed) memóriakezelő függvényhívás **nem magától jön létre**, hanem csak explicit rendszerpromptból táplálkozó instrukcióval:

> „Memory edits and retrieval are entirely self-directed: MemGPT autonomously updates and searches through its own memory based on the current context... We implement self-directed editing and retrieval by providing explicit instructions within the system instructions that guide the LLM on how to interact with the MemGPT memory systems. These instructions comprise two main components: (1) a detailed description of the memory hierarchy and their respective utilities, and (2) a function schema..."

> „Awareness of context limits is a key aspect in making the self-editing mechanism work effectively, to this end MemGPT prompts the processor with warnings regarding token limitations to guide its memory management decisions."

Forrás: „MemGPT: Towards LLMs as Operating Systems", arXiv:2310.08560, https://arxiv.org/abs/2310.08560 (T1, 2023, azóta ~2000+ hivatkozás).

**Ez az egyik legközvetlenebb bizonyíték a kérdésre**: már az „önkéntes" memóriahasználatot definiáló alapmű is azt állítja, hogy ez csak explicit, a memória-hierarchiát és a függvényeket leíró rendszerprompt-szöveggel működik — magától, instrukció nélkül a szerzők szerint nem.

### 1.3 A gyártói gyakorlat mint közvetett bizonyíték: mindenki explicit szöveget told be

Lásd részletesen a 2. pontot — de ide kívánkozik az egyetlen konkrét, *modellváltozat szerint mért* vendor-oldali állítás, amit találtam. A Google Gemini CLI nyílt forráskódú repójában egy 2026 februári PR (elsődleges forrás, a gyártó saját commitja) kifejezetten eltávolítja a memória-eszköz használatára vonatkozó explicit instrukciót Gemini 3 modelleknél:

> „This PR removes the explicit memory tool instructions from the Gemini 3 series system prompt. These instructions were previously necessary for earlier models to correctly utilize the memory tool, but Gemini 3 models exhibit high reliability in using the tool without explicit guidance."

> „Verify that all tests pass (Gemini 2.5 still uses the legacy prompt which contains the instructions, while Gemini 3 uses the updated prompt)."

Forrás: google-gemini/gemini-cli, PR #18559, https://github.com/google-gemini/gemini-cli/pull/18559 (T1, gyártói forráskód/PR, 2026-02-08). *Ez egyetlen, nem publikált, nem kvantifikált (nincs %-os szám) gyártói mérnöki állítás — nem sikerült második, független forrással megerősíteni, ezért önmagában áll; iránymutatásként kezelendő, nem mért effektusméretként.*

## 2. Gyártói útmutatás: mit ajánl a rendszerprompt / eszközleírás / indító szöveg szintjén

### 2.1 Anthropic — Claude API memory tool

A hivatalos dokumentáció (platform.claude.com) kimondja, hogy **maga az API automatikusan told be egy kikényszerítő szöveget**, amint a memória-eszköz szerepel a `tools` listában — a fejlesztőnek ezt nem kell megírnia:

> „When the memory tool is present in your request's `tools`, the API automatically adds this instruction to the system prompt. You don't need to send it yourself:
> ```
> IMPORTANT: ALWAYS VIEW YOUR MEMORY DIRECTORY BEFORE DOING ANYTHING ELSE.
> MEMORY PROTOCOL:
> 1. Use the `view` command of your `memory` tool to check for earlier progress.
> 2. ... (work on the task) ...
>    - As you make progress, record status / progress / thoughts etc in your memory.
> ASSUME INTERRUPTION: Your context window might be reset at any moment, so you risk losing any progress that is not recorded in your memory directory.
> ```"

Forrás: „Memory tool", Claude Platform Docs, https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool (T1, hivatalos, elérve 2026-09-25; a fejlesztő emellett saját szöveggel finomíthatja: „when editing your memory folder, always try to keep its content up-to-date, coherent and organized").

Ez direkt megerősíti a kutatási kérdés alapfeltevését: a gyártó szerint az eszköz puszta jelenléte **nem elég**, ezért ők maguk automatikusan injektálnak egy kényszerítő, felkiáltójeles emlékeztetőt minden hívás elé.

A bejelentő blogbejegyzés (2025-09-29) mért számokat is közöl a memória+context-editing kombináció hasznáról, de ezek önbevallott, belső eval-eredmények:

> „On an internal evaluation set for agentic search... combining the memory tool with context editing improved performance by 39% over baseline. Context editing alone delivered a 29% improvement... In a 100-turn web search evaluation, context editing enabled agents to complete workflows that would otherwise fail due to context exhaustion—while reducing token consumption by 84%."

Forrás: „Managing context on the Claude Developer Platform", Anthropic, https://www.anthropic.com/news/context-management (T1, 2025-09-29). *Egy független, kritikai elemzés (T3, dreaming.press, 2026-07-27) rámutat, hogy ez a szám egy kontextus-kimerüléses vészhelyzetből való kimenekülést mér, nem általános képességnövekedést, és rövid feladatokon a hatás nullához tart — lásd „Ellentmondások".*

### 2.2 Anthropic — Claude Code (CLAUDE.md + auto memory)

A hivatalos Claude Code dokumentáció (code.claude.com/docs/en/memory) szerint a CLAUDE.md-fájlok minden session elején automatikusan betöltődnek, de **nem kikényszerített konfiguráció, hanem kontextus**:

> „Claude Code has two complementary memory systems. Both are loaded at the start of every conversation. Claude treats them as context, not enforced configuration. To block an action regardless of what Claude decides, use a PreToolUse hook instead. The more specific and concise your instructions, the more consistently Claude follows them."

> „CLAUDE.md content is delivered as a user message after the system prompt, not as part of the system prompt itself. Claude reads it and tries to follow it, but there's no guarantee of strict compliance, especially for vague or conflicting instructions."

> „Because they're context rather than enforced configuration, how you write instructions affects how reliably Claude follows them. Specific, concise, well-structured instructions work best."

Forrás: „How Claude remembers your project", Claude Code Docs, https://code.claude.com/docs/en/memory (T1, hivatalos, elérve 2026-09-25).

Az „auto memory" (a Claude saját maga írt jegyzetei) esetében a hivatalos doksi kimondja, hogy ez **nem minden alkalommal aktiválódó**, hanem a modell saját döntése:

> „Claude doesn't save something every session. It decides what's worth remembering based on whether the information would be useful in a future conversation."

Ugyanez forrás. *(Megjegyzés: a session-induló rendszerprompt pontos, betű szerinti szövegét — a `loadMemoryPrompt()` által beillesztett instrukciós blokkot — az Anthropic nem publikálja hivatalosan; több független, nem hivatalos, forráskód-visszafejtésen alapuló repository (pl. `luyao618/Claude-Code-Source-Study`, `leaf-kit/claude-analysis`) közöl belőle részleteket, de ezek hitelessége nem ellenőrizhető és nem hivatalos Anthropic-forrás — T3, óvatosan kezelendő, lásd „Ellentmondások".)*

### 2.3 OpenAI — Codex (AGENTS.md) és Agents SDK (Sessions)

A Codex esetében **nincs külön „memória-eszköz"**, amit a modellnek proaktívan meg kellene hívnia — az AGENTS.md fájlokat a keretrendszer session-indításkor automatikusan a fejlesztői üzenetbe fűzi, olvasás nélkül is látja a modell. A beépített rendszerprompt-részlet (a Codex forráskódjából, `default.md`) explicit előírja, hogy kötelezően be kell tartani, amit egyszer betöltött:

> „Repos often contain AGENTS.md files. These files are a way for humans to give you (the agent) instructions or tips for working within the container... For every file you touch in the final patch, you must obey instructions in any AGENTS.md file whose scope includes that file... The contents of the AGENTS.md file at the root of the repo and any directories from the CWD up to the root are included with the developer message and don't need to be re-read."

Forrás: codex-rs/protocol/src/prompts/base_instructions/default.md, https://github.com/openai/codex/blob/385c0a9351e2199929e01f7864ec78a8f7d5e580/codex-rs/protocol/src/prompts/base_instructions/default.md (T1, gyártói forráskód).

A hivatalos Codex-doksi külön kiemeli, hogy az AGENTS.md-t helyesbítő visszacsatolással kell karbantartani, és a modellt kell megkérni, hogy maga frissítse:

> „When the agent makes incorrect assumptions about your codebase, correct them in `AGENTS.md` and ask the agent to update `AGENTS.md` so the fix persists. Treat it as a feedback loop."

Forrás: „Customization – Codex", https://developers.openai.com/codex/concepts/customization (T1, hivatalos).

Az **OpenAI Agents SDK** „Sessions" mechanizmusa strukturálisan **más elvre épül**, mint az Anthropic memory tool: itt a modellnek nem kell proaktívan „eszközt hívnia" a memóriához — a runner automatikusan, minden futás előtt visszatölti és a bemenet elé fűzi a session-history-t:

> „When session memory is enabled: 1. Before each run: The runner automatically retrieves the conversation history for the session and prepends it to the input items. 2. After each run: All new items generated during the run... are automatically stored in the session."

Forrás: „Overview - OpenAI Agents SDK", https://openai.github.io/openai-agents-python/sessions/ (T1, hivatalos). Ez azt jelenti, hogy az OpenAI Agents SDK „memóriája" alapesetben **nem** a modell önkéntes eszközhívásán múlik — ezzel elkerüli a kutatási kérdés által feltételezett problémát (,,rávegyük a modellt, hogy keressen"), mert a betöltés automatikus/kikényszerített infrastruktúra-szinten, nem modell-döntés.

### 2.4 Google — Gemini CLI (GEMINI.md + memory tool)

A hivatalos Gemini CLI dokumentáció szerint a GEMINI.md-fájlok hierarchikusan, session-indításkor automatikusan betöltődnek és összefűződnek:

> „The CLI uses a hierarchical system to source context. It loads various context files from several locations, concatenates the contents of all found files, and sends them to the model with every prompt."

Forrás: „Provide context with GEMINI.md files", https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/gemini-md.md (T1, hivatalos).

A Gemini CLI forráskódjában (`packages/core/src/prompts/snippets.ts`, gyártói repo) explicit, szó szerinti utasítás szerepel a modellnek arra, *mikor* hívja meg a memória-eszközt — ez a legkonkrétabb, közvetlenül idézhető „eszközleírás-szintű" rábeszélő szöveg, amit találtam:

> „**Memory Tool:** Use `save_memory` to persist facts across sessions. It supports two scopes via the `scope` parameter: `"global"` (default): Cross-project preferences and personal facts loaded in every workspace. `"project"`: Facts specific to the current workspace... Never save transient session state. Do not use memory to store summaries of code changes, bug fixes, or findings discovered during a task."
>
> (korábbi verzióban, explicit feltétel-megadással:) „Use the 'save_memory' tool to remember specific, *user-related* facts or preferences when the user explicitly asks, or when they state a clear, concise piece of information that would help personalize or streamline *your future interactions with them*... This tool is for user-specific information that should persist across sessions. Do *not* use it for general project context or information. If unsure whether to save something, you can ask the user, 'Should I remember that for you?'"

Forrás: google-gemini/gemini-cli, `packages/core/src/prompts/snippets.ts` és `packages/core/src/core/prompts.ts`, https://github.com/google-gemini/gemini-cli/blob/caa04664/packages/core/src/prompts/snippets.ts , https://github.com/google-gemini/gemini-cli/blob/e79b149/packages/core/src/core/prompts.ts (T1, gyártói forráskód, több egymást követő commit-verzióban konzisztens).

A memóriaverzió (V2) esetén a forrás explicit „routing" szabályokat is ad, hogy melyik szintű fájlba írjon a modell — ez direkt analóg az SQ06 projekt saját nyitott kérdésével (,,hova kerüljön az új bejegyzés"):

> „**Routing rules — pick exactly one tier per fact:** ... If a fact could plausibly belong to more than one tier, **ask the user** which tier they want before writing. **Never duplicate or mirror the same fact across tiers**..."

Ugyanaz a forrás.

## 3. A beadott szöveg helye és hossza — mérések

### 3.1 Pozíció: „Lost in the Middle" (Liu et al., TACL 2024 / arXiv 2023)

A legidézettebb, lektorált (Transactions of the ACL) tanulmány szerint a relevancia-pozíció U-alakú teljesítménygörbét ad — a legelején és a legvégén lévő információ jobban hasznosul, mint a középen lévő:

> „We observe that performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts, even for explicitly long-context models."

> „For example, when relevant information is placed in the middle of its input context, GPT-3.5-Turbo's performance on the multi-document question task is lower than its performance when predicting without any documents (i.e., the closed-book setting; 56.1%)."

Forrás: „Lost in the Middle: How Language Models Use Long Contexts", TACL 2024, https://aclanthology.org/2024.tacl-1.9/ ; eredeti preprint: https://arxiv.org/abs/2307.03172 (T1, lektorált).

Ez direkt releváns a kutatási kérdésre: egy session-eleji rövid emlékeztető szöveg (primacy pozíció) elméletileg **kedvezőbb** helyen van, mint egy középre kerülő szöveg — de a hossz növekedésével (több dokumentum/token) ez az előny is csökken.

### 3.2 Hossz és „context rot": a session hossza rontja a korábban beadott szöveg hatását

Az Anthropic saját mérnöki blogja (Effective context engineering for AI agents, 2025-09-29) explicit összekapcsolja a jelenséget az „attention budget" fogalmával:

> „Studies on needle-in-a-haystack style benchmarking have uncovered the concept of context rot: as the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases... Like humans, who have limited working memory capacity, LLMs have an 'attention budget' that they draw on when parsing large volumes of context. Every new token introduced depletes this budget by some amount..."

Forrás: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents (T1, hivatalos, 2025-09-29).

A Chroma kutatócsapat 18 modellen (GPT-4.1, Claude 4, Gemini 2.5, Qwen3 stb.) kontrollált kísérletekkel — a feladat nehézségét állandó szinten tartva, csak a bemenet hosszát változtatva — függetlenül igazolta ugyanezt:

> „We demonstrate that even under these minimal conditions, model performance degrades as input length increases, often in surprising and non-uniform ways... Across all experiments, model performance consistently degrades with increasing input length."

Forrás: „Context Rot: How Increasing Input Tokens Impacts LLM Performance", https://www.trychroma.com/research/context-rot (T2, iparági kutatóműhely, nem lektorált, de módszertanilag kontrollált, széles körben idézett).

Egy harmadik, független tanulmány (2026) még szélsőségesebb változatban mutatja meg ugyanezt: **tökéletes visszakeresés mellett is** romlik a teljesítmény, pusztán a hossztól:

> „...even when models can perfectly retrieve all relevant information, their performance still degrades substantially (13.9%–85%) as input length increases... This failure occurs even when the irrelevant tokens are replaced with minimally distracting whitespace, and, more surprisingly, when they are all masked and the models are forced to attend only to the relevant tokens."

Forrás: „Context Length Alone Hurts LLM Performance Despite Perfect Retrieval", arXiv:2510.05381, https://arxiv.org/html/2510.05381 (T1, 2026).

Egy negyedik, hosszú-horizontú keresési (agentic search) tanulmány azt méri, hogy hosszú kontextusban a modellek *idő előtt feladják* a feladatot:

> „...under extensive context, models give up or provide uncertain incorrect answers long before exhausting the context window... the premature termination rate is positively correlated with context length [when query difficulty is held fixed]."

Forrás: „Diagnosing and Mitigating Context Rot in Long-horizon Search", arXiv:2606.29718, https://arxiv.org/html/2606.29718 (T1, 2026). **Ez négy egymástól független kutatócsoport (Anthropic, Chroma, egy önálló arXiv-szerzői csoport, egy másik önálló arXiv-csoport) konvergáló eredménye** — a session hossza szisztematikusan rontja a korábban beadott információ hasznosulását.

A gyártói termékdokumentáció is közvetlenül alkalmazza ezt a memória-fájlokra: a Claude Code auto-memory rendszernél a `MEMORY.md`-nek explicit méretkorlátja van, és a hivatalos doksi szerint a **rövidebb** fájlok jobban követve vannak:

> „The first 200 lines of `MEMORY.md`, or the first 25KB, whichever comes first, are loaded at the start of every conversation. Content beyond that threshold is not loaded at session start... This limit applies only to `MEMORY.md`. CLAUDE.md files are loaded in full regardless of length, though shorter files produce better adherence."

Forrás: https://code.claude.com/docs/en/memory (T1, hivatalos).

### 3.3 Ellenpélda / null-eredmény a hosszhatásra (lásd „Ellentmondások")

Egy 2026-os, **nem lektorált** preprint kifejezetten megpróbálta reprodukálni a „context rot"-ot kontrollált, előre regisztrált kísérletben 4 friss modellen (gpt-5.5, gpt-5.4, gpt-5.4-mini, claude-sonnet-4-6), és 150 000 tokenig **nem talált mérhető hosszfüggő romlást**:

> „...we observe no measurable length-driven degradation on our probes for the four models tested... up to 150,000 tokens... Across the 12,570-trial registered grid, 7,330 present-needle trials had 48 failures (accuracy 0.9935)."

Forrás: „Is Context Rot Real? A Controlled, Cross-Provider Null for Length-Driven Degradation in Frontier Models up to 150k Tokens", Zenodo preprint, https://doi.org/10.5281/zenodo.20753848 (T2, „Preprint - not peer reviewed", 2026-06-18). A szerző maga hangsúlyozza, hogy szintetikus, tiszta needle-in-haystack feladatokról van szó, és „we cannot determine its contribution in real multi-turn agentic workflows" — tehát nem cáfolja az agentikus/hosszú-session kontextusban mért romlást (3.2 pont), csak azt jelzi, hogy legújabb frontier-modelleken, tiszta lexikai visszakeresési feladaton a hatás nem mindig mutatkozik.

## 4. Kockázatok: ronthatja-e a munkát egy beadott címlista/tartalom?

### 4.1 Irreleváns tartalom zavarja a modellt — mért hatás

A Shi et al. (ICML 2023, lektorált) GSM-IC benchmarkja kifejezetten azt méri, mennyire téríti el a modellt egyetlen irreleváns mondat beszúrása egy egyébként megoldható feladatba:

> „...among the original problems that can be solved by baseline prompts with greedy decoding, no more than 18% of them can be consistently solved for all types of irrelevant information, showing that the large language model is easily distracted and produces inconsistent predictions when adding a small amount of irrelevant information to the problem description."

> „Adding irrelevant information to the exemplars shown in the prompt consistently boosts the performance, and the same holds for adding an instruction to ignore irrelevant context. This suggests that language models are—to some extent—able to learn to ignore irrelevant information by following examples or instructions."

Forrás: „Large Language Models Can Be Easily Distracted by Irrelevant Context", ICML 2023, https://proceedings.mlr.press/v202/shi23a.html (T1, lektorált).

Ez direkt releváns arra a kockázatra, hogy egy sablonos „emlékeztető" szöveg (ami a konkrét kérdéshez esetleg nem kapcsolódó memória-tartalmat vagy metaadatot sorol fel) önmagában zavaró tényező lehet — bár egy explicit instrukció („hagyd figyelmen kívül, ha irreleváns") részben ellensúlyozza.

### 4.2 Elavult lista félrevezetheti a modellt — dokumentált eset

Egy közösségi GitHub-jegy (nem hivatalosan megerősített hibajelentés) a Codex Desktopban dokumentál egy esetet, ahol egy **elavult, memóriában tárolt** munkafolyamat felülírta a helyesen, aktuálisan betöltött AGENTS.md-utasítást:

> „Codex Desktop loaded both the global `~/.codex/AGENTS.md` and the repository `AGENTS.md` into the task context, but the agent ignored a distinctive current global rule and instead followed stale validation-gate guidance recovered from persistent memory... The problem is instruction precedence/compliance: stale memory was treated as more authoritative than the current, explicitly loaded global `AGENTS.md`."

Forrás: „Codex Desktop loads global AGENTS.md but stale memory overrides its explicit rule", GitHub issue, https://github.com/openai/codex/issues/39223 (T2, első kézből származó, de nem hivatalosan megerősített/lezárt hibajelentés).

Ez pontosan az az eset, amire az SQ06 kérdés rákérdez: ha a memóriában/emlékeztetőben elavult információ van (pl. egy régi, már nem érvényes bejegyzés-lista), az konkrétan félre tudja vezetni az agentet a friss, helyes instrukció rovására.

### 4.3 Prompt injection a beadott tartalmon keresztül — akadémiai támadás

A MINJA (,,Memory INJection Attack", NeurIPS 2025, lektorált) formálisan bizonyítja, hogy egy támadó **kizárólag lekérdezéseken keresztül**, a memóriabank közvetlen elérése nélkül tud rosszindulatú bejegyzéseket becsempészni, amelyeket a rendszer később, más felhasználó kérésére visszahív:

> „The attacker injects malicious records into the memory bank by only interacting with the agent via queries and output observations... When the victim user submits a victim query, the stored malicious records are retrieved as a demonstration, misleading the agent to generate bridging steps and target reasoning steps through in-context learning... Our extensive experiments across diverse agents demonstrate the effectiveness of MINJA in compromising agent memory."

Forrás: „Memory Injection Attacks on LLM Agents via Query-Only Interaction", NeurIPS 2025, https://proceedings.neurips.cc/paper_files/paper/2025/hash/42a97bbd9844d2bf68596730af80bcdf-Abstract-Conference.html (T1, lektorált).

### 4.4 Prompt injection a beadott tartalmon keresztül — valós, dokumentált incidens

Johann Rehberger biztonsági kutató 2024-ben (saját, elsődleges közlésű blogján, később Ars Technica és Bruce Schneier is megerősítette/idézte) dokumentált egy valós, éles ChatGPT-memória elleni indirekt prompt injection támadást:

> „Within three months of the rollout, Rehberger found that memories could be created and permanently stored through indirect prompt injection... The researcher demonstrated how he could trick ChatGPT into believing a targeted user was 102 years old, lived in the Matrix, and insisted Earth was flat and the LLM would incorporate that information to steer all future conversations. These false memories could be planted by storing files in Google Drive or Microsoft OneDrive, uploading images, or browsing a site like Bing."

Forrás: Ars Technica, „Hacker plants false memories in ChatGPT to steal user data in perpetuity", 2024-09-24, https://arstechnica.com/security/2024/09/false-memories-planted-in-chatgpt-give-hacker-persistent-exfiltration-channel/ (T2, minőségi tech-újságírás, elsődleges kutatói közlésre alapozva).

A kutató saját, elsődleges technikai leírása (embracethered.com) megerősíti, és két súlyos következményt is dokumentál: tartós adatszivárgást és tartós szolgáltatás-megtagadást (DoS), mindkettő a memória-injektáláson keresztül, munkameneteken átívelően:

> „What is really interesting is this is memory-persistent now... The prompt injection inserted a memory into ChatGPT's long-term storage. When you start a new conversation, it actually is still exfiltrating the data."

Forrás: Johann Rehberger, „ChatGPT: Hacking Memories with Prompt Injection", https://embracethered.com/blog/posts/2024/chatgpt-hacking-memories/ (T1, elsődleges kutatói közlés, 2024-05-22).

> „Malicious memory modifications remain until the user manually removes the attacker-created memories... From now on, ChatGPT will refuse every future response."

Forrás: Johann Rehberger, „Sorry, ChatGPT Is Under Maintenance: Persistent Denial of Service through Prompt Injection and Memory Attacks", https://embracethered.com/blog/posts/2024/chatgpt-persistent-denial-of-service/ (T1, elsődleges, 2024-07-08).

Fontos, hogy OpenAI kezdetben nem biztonsági, hanem „modellbiztonsági" (model safety) ügyként zárta le a jelentést, majd 2024 szeptemberében részlegesen javította:

> „When security researcher Johann Rehberger recently reported a vulnerability in ChatGPT that allowed attackers to store false information and malicious instructions in a user's long-term memory settings, OpenAI summarily closed the inquiry, labeling the flaw a safety issue, not, technically speaking, a security concern... OpenAI released a fix for the macOS app last week."

Forrás: Ars Technica, ugyanaz mint fent (T2); megerősítve: Bruce Schneier, „Hacking ChatGPT by Planting False Memories into Its Data", https://www.schneier.com/blog/archives/2024/10/hacking-chatgpt-by-planting-false-memories-into-its-data.html (T3, biztonsági szakértői kommentár, idézi az elsődleges forrást).

**Ez a négy forrás (MINJA akadémiai támadás + Rehberger elsődleges közlés + Ars Technica + Schneier) két, egymástól teljesen független bizonyítékvonalat ad**: egy formális, lektorált akadémiai támadási technikát, és egy valós, gyártó által is (részlegesen) elismert incidenst — vagyis a kockázat mind elméletileg, mind gyakorlatilag igazolt.

## Ellentmondások

- **A 84%/39%-os Anthropic-szám értelmezése.** Az Anthropic saját bejelentése szerint a memória-eszköz + context editing kombináció „39%-kal" jobb teljesítményt, a context editing önmagában „84%-kal" kevesebb tokenfelhasználást ad — ez elsőre úgy hangzik, mintha a memória-eszköz általában sokat javítana. Egy független, kritikai elemzés (T3, dreaming.press, 2026-07-27) rámutat, hogy ezek a számok egy **kontextus-kimerüléses bukásból** való megmenekülést mérik, nem általános képességnövekedést: „Both figures are real. Neither says the model got smarter — they measure escaping a wall your agent may never hit... on short tasks the delta collapses toward zero." Vagyis rövid session esetén (amilyen egy tipikus, néhány üzenetes interakció is lehet) a mért haszon a nullához tarthat — ellentétben azzal a benyomással, amit a puszta „39%" szám sugall. Ez direkt releváns az SQ06 alapkérdésére: egy rövid, session-eleji emlékeztető haszna feltehetően szintén a session hosszától és a kontextus-nyomástól függ, nem konstans.

- **A hosszhatás („context rot") univerzalitása vitatott.** Négy egymástól független forrás (Anthropic, Chroma, két önálló arXiv-tanulmány) mért, szisztematikus teljesítményromlást talál a bemeneti hossz növekedésével, míg egy 2026-os, nem lektorált, előre regisztrált null-eredmény (Zenodo) 150 000 tokenig **nem** talált mérhető hosszfüggő romlást 4 legújabb frontier-modellen tiszta needle-in-haystack feladaton. A szerző maga jelzi, hogy ez nem feltétlenül mond ellent az agentikus, több-fordulós forgatókönyveknek — csak azt, hogy a legújabb modelleken, tiszta lexikai feladaton a hatás nem mindig, nem minden körülmények között jelentkezik. A két eredménykör tehát nem feltétlenül zárja ki egymást, de a hatás mértéke és univerzalitása nyitott kérdés marad.

- **A Claude Code belső rendszerprompt-szövegének hitelessége.** Az Anthropic hivatalosan **nem** publikálja a Claude Code session-induló memória-instrukciós blokk (`loadMemoryPrompt()`) pontos szövegét. Több, egymással erősen egyező, de nem hivatalos, forráskód-visszafejtésen alapuló GitHub-repository (`luyao618/Claude-Code-Source-Study`, `leaf-kit/claude-analysis`, `zackautocracy/claude-code`, `y-agent.github.io/inside-claude-code`) közöl belőle kódrészleteket és promptszövegeket — ezek egymással konzisztensek, de valószínűleg **közös eredetre** (ugyanarra a kiszivárgott/visszafejtett forrásra) vezethetők vissza, nem egymástól független megerősítések, és hitelességük (hogy tényleg a jelenlegi, éles Claude Code kódjából származnak-e) nem ellenőrizhető külső, hivatalos forrásból. Ezért ezeket a részleteket a jelen jelentésben csak jelzésértékű, T3 minősítésű adalékként használtam, nem tényként.

## Amire NINCS forrás

- **Nincs forrás** egy kontrollált (A/B jellegű) kísérletre, amely kifejezetten azt mérné: egy rövid, sablonból generált, session-eleji szöveg (,,van memória, N bejegyzés, használd a keresőt") jelenléte vs. hiánya mennyivel változtatja meg egy memória- vagy kereső-eszköz **önkéntes** meghívási arányát, elkülönítve a hatást a szöveg hosszától és tartalmától. Ez pontosan a kutatási kérdés fókusza, és a fenti 1–3. pontban idézett tanulmányok mind csak közvetett, rokon jelenségeket (általános eszközhasználati arány, memória-benchmark pontosság, pozíció/hossz hatása szövegértésre) mérnek, nem ezt a konkrét beavatkozást.
- **Nincs forrás** arra, hogy a beadott szövegben szereplő **konkrét bejegyzésszám** (,,17 bejegyzés van a memóriában") önmagában, számszerűsítve hogyan befolyásolja a modell keresési hajlandóságát vagy a keresés mélységét/pontosságát.
- **Nincs forrás** (lektorált vagy gyártói) arra, hogy az Anthropic, OpenAI vagy Google konkrétan mérte volna a saját session-indító emlékeztető szövegük hosszának hatását a memóriahasználatra — a gyártói dokumentációk csak minőségi ajánlásokat adnak („legyen rövid és specifikus"), számszerű ablációt egyik gyártó sem publikált nyilvánosan.
- **Nincs forrás** az OpenAI Codex/Agents SDK esetére vonatkozó, a Gemini CLI PR #18559-hez hasonló, explicit, modellváltozatonkénti gyártói nyilatkozatra arról, hogy mennyi explicit „nógatás" szükséges a memóriahasználathoz.

## Meglátogatott és felderített linkek

| Cím | URL | Tier | Eszköz | Megjegyzés |
|---|---|---|---|---|
| Memory tool — Claude Platform Docs | https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool | T1 | Exa search+fetch | Auto-injektált „MEMORY PROTOCOL" szöveg szó szerint |
| Memory & context management cookbook (Claude Sonnet 4.6) | https://platform.claude.com/cookbook/tool-use-memory-cookbook | T1 | Exa search | Fejlesztői MEMORY_SYSTEM_PROMPT minta |
| Effective context engineering for AI agents | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | T1 | Exa search | „context rot", „attention budget" fogalmak eredete |
| Managing context on the Claude Developer Platform | https://www.anthropic.com/news/context-management | T1 | Exa search | 84%/39% önbevallott mérési számok |
| How Claude remembers your project — Claude Code Docs | https://code.claude.com/docs/en/memory | T1 | Exa search | CLAUDE.md + auto memory hivatalos leírása |
| Explore the context window — Claude Code Docs | https://code.claude.com/docs/en/context-window | T1 | Exa search | Compaction utáni memória-újrainjektálás |
| Custom instructions with AGENTS.md — Codex | https://developers.openai.com/codex/guides/agents-md | T1 | Exa search | AGENTS.md betöltési sorrend, méretkorlát |
| Customization — Codex | https://developers.openai.com/codex/concepts/customization | T1 | Exa search | AGENTS.md vs memories vs skills |
| codex-rs/core/src/agents_md.rs (openai/codex) | https://github.com/openai/codex/blob/main/codex-rs/core/src/agents_md.rs | T1 | Exa search | Forráskód: AGENTS.md betöltés/csonkolás |
| codex-rs base_instructions/default.md | https://github.com/openai/codex/blob/385c0a9351e2199929e01f7864ec78a8f7d5e580/codex-rs/protocol/src/prompts/base_instructions/default.md | T1 | Exa search | Codex beépített rendszerprompt szövege AGENTS.md-ről |
| AGENTS.md silently truncated — issue #7138 | https://github.com/openai/codex/issues/7138 | T2 | Exa search | 32 KiB csonkolási hiba, gyártói válasszal |
| Codex Desktop stale memory overrides AGENTS.md — issue #39223 | https://github.com/openai/codex/issues/39223 | T2 | Exa search | Elavult memória felülírja friss instrukciót — dokumentált eset |
| Overview — OpenAI Agents SDK (Sessions) | https://openai.github.io/openai-agents-python/sessions/ | T1 | Exa search | Automatikus history-betöltés, nem eszközhívás-alapú |
| Sessions — OpenAI Agents SDK (JS) | https://openai.github.io/openai-agents-js/guides/sessions/ | T1 | Exa search | Ugyanaz TS SDK-ban |
| Short-Term Memory Management with Sessions (cookbook) | https://developers.openai.com/cookbook/examples/agents_sdk/session_memory | T2 | Exa search | Trimming/summarizing session implementáció |
| Provide context with GEMINI.md files | https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/gemini-md.md | T1 | Exa search | Hierarchikus, JIT context-betöltés |
| Manage context and memory (Gemini CLI tutorial) | https://geminicli.com/docs/cli/tutorials/memory-management/ | T1 | Exa search | `/memory show`, `/memory reload` |
| Gemini CLI core prompts.ts | https://github.com/google-gemini/gemini-cli/blob/e79b149/packages/core/src/core/prompts.ts | T1 | Exa search | Memória-eszköz használatára vonatkozó rendszerprompt-szöveg (korábbi verzió) |
| Gemini CLI snippets.ts (toolUsageRememberingFacts) | https://github.com/google-gemini/gemini-cli/blob/caa04664/packages/core/src/prompts/snippets.ts | T1 | Exa search | Jelenlegi memória-instrukció + tier-routing szabályok |
| refactor: remove memory tool instructions from Gemini 3 prompt — PR #18559 | https://github.com/google-gemini/gemini-cli/pull/18559 | T1 | Exa search | Modellfüggő „nógatás"-szükséglet — kulcsbizonyíték Q1-hez |
| Lost in the Middle: How Language Models Use Long Contexts (TACL 2024) | https://aclanthology.org/2024.tacl-1.9/ | T1 | Exa search | U-alakú pozíció-teljesítmény görbe, lektorált |
| Lost in the Middle (arXiv preprint) | https://arxiv.org/abs/2307.03172 | T1 | Exa search | Ugyanaz, eredeti preprint |
| Context Rot: How Increasing Input Tokens Impacts LLM Performance (Chroma) | https://www.trychroma.com/research/context-rot | T2 | Exa search | 18 modell, kontrollált hosszkísérlet |
| Context Length Alone Hurts LLM Performance Despite Perfect Retrieval | https://arxiv.org/html/2510.05381 | T1 | Exa search | Hossz önmagában árt, elterelés nélkül is |
| Diagnosing and Mitigating Context Rot in Long-horizon Search | https://arxiv.org/html/2606.29718 | T1 | Exa search | „premature termination", hossz-korreláció |
| Is Context Rot Real? Controlled Cross-Provider Null (Zenodo) | https://doi.org/10.5281/zenodo.20753848 | T2 | Exa search | Ellenpélda: nem talált hosszhatást 150k tokenig |
| Large Language Models Can Be Easily Distracted by Irrelevant Context (ICML 2023) | https://proceedings.mlr.press/v202/shi23a.html | T1 | Exa search | GSM-IC, irreleváns tartalom mért hatása |
| LONGMEMEVAL (ICLR 2025) | https://proceedings.iclr.cc/paper_files/paper/2025/file/d813d324dbf0598bbdc9c8e79740ed01-Paper-Conference.pdf | T1 | Exa search | 30%-os pontosságesés hosszú-memória feladaton |
| MemGPT: Towards LLMs as Operating Systems | https://arxiv.org/abs/2310.08560 | T1 | Exa search | Önkéntes memóriakezelés csak explicit instrukcióval működik |
| LLM Agents Already Know When to Call Tools (WHEN2TOOL) | https://arxiv.org/pdf/2605.09252v2 | T1 | Exa search | Prompt-only beavatkozás durva, nem szelektív hatása |
| ToolFailBench | https://ar5iv.labs.arxiv.org/html/2607.04686 | T1 | Exa search | 19 modell, eszközhasználati hibaarányok |
| Tunable Tool-Call Rates in LLM Agents via Representation Steering | https://arxiv.org/html/2608.25198v1 | T1 | Exa search | Eszközhívási arány mint mérhető, kontrollálható változó |
| To Call or Not to Call: A Framework to Assess and Optimize LLM Tool Calling | https://arxiv.org/html/2605.00737v3 | T1 | Exa search | Vélt vs. valós szükséglet közti eltérés |
| Memory Injection Attacks on LLM Agents via Query-Only Interaction (MINJA, NeurIPS 2025) | https://proceedings.neurips.cc/paper_files/paper/2025/hash/42a97bbd9844d2bf68596730af80bcdf-Abstract-Conference.html | T1 | Exa search | Lektorált memória-injekciós támadás |
| ChatGPT: Hacking Memories with Prompt Injection | https://embracethered.com/blog/posts/2024/chatgpt-hacking-memories/ | T1 | Exa search | Elsődleges kutatói közlés (Rehberger), valós eset |
| Spyware Injection Into Your ChatGPT's Long-Term Memory | https://embracethered.com/blog/posts/2024/chatgpt-macos-app-persistent-data-exfiltration/ | T1 | Exa search | Tartós adatszivárgás memórián át |
| Sorry, ChatGPT Is Under Maintenance (persistent DoS) | https://embracethered.com/blog/posts/2024/chatgpt-persistent-denial-of-service/ | T1 | Exa search | Tartós szolgáltatás-megtagadás memórián át |
| Hacker plants false memories in ChatGPT (Ars Technica) | https://arstechnica.com/security/2024/09/false-memories-planted-in-chatgpt-give-hacker-persistent-exfiltration-channel/ | T2 | Exa search | Összefoglaló, OpenAI reakció idézve |
| Hacking ChatGPT by Planting False Memories (Schneier on Security) | https://www.schneier.com/blog/archives/2024/10/hacking-chatgpt-by-planting-false-memories-into-its-data.html | T3 | Exa search | Szakértői kommentár |
| The 84% and the 39%: What Anthropic's Numbers Actually Measure | https://dreaming.press/posts/anthropic-context-editing-84-percent-39-percent-numbers-examined.html | T3 | Exa search | Kritikai elemzés a vendor-számokról |
| docs-en/31-memory-subsystem-overview.md (Claude-Code-Source-Study) | https://github.com/luyao618/Claude-Code-Source-Study/blob/main/docs-en/31-memory-subsystem-overview.md | T3 | Exa search | Nem hivatalos forráskód-visszafejtés, óvatosan kezelendő |
| src/memdir/memdir.ts (leaf-kit/claude-analysis) | https://github.com/leaf-kit/claude-analysis/blob/main/src/memdir/memdir.ts | T3 | Exa search | Ugyanaz, más tükör — hitelesség nem ellenőrizhető |
| Benchmarking Agent Tool Use (LangChain blog, 2023) | https://www.langchain.com/blog/benchmarking-agent-tool-use | T3 | Exa search | Korai, kiegészítő iparági benchmark |
| Exploring Anthropic's Memory Tool (Leonie Monigatti blog) | https://www.leoniemonigatti.com/blog/claude-memory-tool.html | T3 | Exa search | Független demonstráció: agent csak akkor hív memóriát, ha „szükséges" |
