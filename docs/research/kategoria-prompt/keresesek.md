# Keresések — Kategória-választó prompt mérete kutatás

Minden lefuttatott lekérdezés szó szerint, al-kérdésenként csoportosítva. Forrás: `01-search-log/queries.jsonl` (SQ-01/02/03), `sq04/searches.md`, `sq05/searches.md`.

## SQ-01

(8 lekérdezés, mind `WebSearch` eszközzel, `01-search-log/queries.jsonl`-ből.)

1. `Anthropic "tool definitions" tokens context window MCP` (WebSearch, 9 találat, 2026-09-05T23:17:11Z)
2. `Anthropic engineering blog "context engineering" tool use tokens` (WebSearch, 9 találat, 2026-09-05T23:17:11Z)
3. `Anthropic MCP "tool search" dynamic tool loading reduce context tokens` (WebSearch, 9 találat, 2026-09-05T23:17:11Z)
4. `Anthropic Agent Skills description character limit 1024` (WebSearch, 10 találat, 2026-09-05T23:21:25Z)
5. `OpenAI function calling description max length characters recommendation` (WebSearch, 10 találat, 2026-09-05T23:21:25Z)
6. `tokenizer language disparity non-English tokens per word arxiv "token premium"` (WebSearch, 10 találat, 2026-09-05T23:21:25Z)
7. `Hungarian language tokenizer tokens per word GPT tiktoken efficiency` (WebSearch, 9 találat, 2026-09-05T23:25:14Z)
8. `model context protocol specification tool description schema best practices modelcontextprotocol.io` (WebSearch, 9 találat, 2026-09-05T23:25:14Z)

## SQ-02

(16 lekérdezés, mind `WebSearch` eszközzel, `01-search-log/queries.jsonl`-ből.)

1. `LLM tool selection accuracy degrades number of tools benchmark` (WebSearch, 8 találat, 2026-09-06T00:53:02Z)
2. `MetaTool benchmark tool selection accuracy number of candidate tools` (WebSearch, 8 találat, 2026-09-06T00:53:02Z)
3. `LLM zero-shot classification accuracy number of classes labels degradation` (WebSearch, 8 találat, 2026-09-06T00:53:02Z)
4. `Berkeley Function Calling Leaderboard accuracy scaling number of functions` (WebSearch, 8 találat, 2026-09-06T00:53:02Z)
5. `"number of tools" accuracy drop LLM function calling arxiv` (WebSearch, 8 találat, 2026-09-06T00:53:02Z)
6. `many-class text classification LLM small model accuracy decreases with classes` (WebSearch, 8 találat, 2026-09-06T00:53:02Z)
7. `Rabinovich Anaby-Tavor function calling accuracy tool catalog size similar tools` (WebSearch, 7 találat, 2026-09-06T00:59:33Z)
8. `LongFuncEval function calling long context many tools accuracy` (WebSearch, 6 találat, 2026-09-06T00:59:33Z)
9. `RAG-MCP paper tool selection accuracy number of MCP tools degradation` (WebSearch, 9 találat, 2026-09-06T00:59:33Z)
10. `Zep "Overlapping or ambiguous descriptions" classification memory documentation` (WebSearch, 8 találat, 2026-09-06T00:59:33Z)
11. `LLM email ticket routing classification accuracy number of departments categories folders` (WebSearch, 8 találat, 2026-09-06T01:02:31Z)
12. `"in-context learning" many classes LLM classification accuracy does not degrade flat number of labels` (WebSearch, 9 találat, 2026-09-06T01:02:31Z)
13. `MetaTool benchmark findings tool count increases accuracy decreases GPT-4` (WebSearch, 7 találat, 2026-09-06T01:02:31Z)
14. `API-Bank benchmark accuracy number of APIs candidate pool size` (WebSearch, 7 találat, 2026-09-06T01:02:31Z)
15. `"number of classes" LLM classification accuracy open source small model Mistral Llama benchmark` (WebSearch, 9 találat, 2026-09-06T01:02:31Z)
16. `LLM document routing accuracy number of destination folders classification benchmark` (WebSearch, 9 találat, 2026-09-06T01:02:31Z)

## SQ-03

(12 lekérdezés, mind `WebSearch` eszközzel, `01-search-log/queries.jsonl`-ből.)

1. `arXiv 2603.25422` (WebSearch, 9 találat, 2026-09-06T01:04:50Z)
2. `"prompt context" "marginal" accuracy "minimal increase" arxiv` (WebSearch, 10 találat, 2026-09-06T01:04:50Z)
3. `tool description length accuracy LLM function calling selection benchmark` (WebSearch, 6 találat, 2026-09-06T01:07:01Z)
4. `tool description rewriting enrichment improves tool selection accuracy LLM arxiv` (WebSearch, 7 találat, 2026-09-06T01:07:01Z)
5. `FollowBench multi-level constraints LLM instruction following accuracy decreases with more constraints` (WebSearch, 7 találat, 2026-09-06T01:07:58Z)
6. `ComplexBench compositional instructions LLM accuracy number of constraints benchmark` (WebSearch, 9 találat, 2026-09-06T01:07:58Z)
7. `few-shot examples in tool description function calling accuracy improvement arxiv` (WebSearch, 10 találat, 2026-09-06T01:09:37Z)
8. `LLM negation understanding poorly negative instructions do not prompt arxiv` (WebSearch, 7 találat, 2026-09-06T01:09:37Z)
9. `Anthropic writing tool descriptions best practices engineering blog agent` (WebSearch, 8 találat, 2026-09-06T01:10:43Z)
10. `tool description length ablation study ambiguous accuracy ToolBench arxiv` (WebSearch, 9 találat, 2026-09-06T01:13:20Z)
11. `including example in function description schema improves LLM parameter accuracy study` (WebSearch, 9 találat, 2026-09-06T01:13:20Z)
12. `in-context examples prompt length diminishing returns saturation number of examples accuracy arxiv` (WebSearch, 9 találat, 2026-09-06T01:14:24Z)

## SQ-04

Forrás: `sq04/searches.md`. Módszer: WebSearch (kulcsszavas) + WebFetch (célzott oldal-lekérés, kérdéssel). A WebFetch egy kis segédmodellen keresztül tömöríti/idézi az oldalt — a magas tétű idézeteket (Anthropic Tool Search Tool küszöbök, Anthropic Skills PDF "20-50 skills" mondat) két független, eltérő prompttal futtatott WebFetch hívással kereszt-ellenőrizték; szó szerint egyeztek.

### WebSearch lekérdezések (időrendben)

1. `Anthropic Agent Skills progressive disclosure SKILL.md`
2. `Anthropic Tool Search Tool token savings accuracy 79.5% 88.1%`
3. `Anthropic "Agent Skills" documentation "progressive disclosure" site:anthropic.com OR site:docs.claude.com`
4. `"agent skills" "hundreds of skills" OR "many skills" context window degrade description`
5. `RAG-MCP dynamic tool retrieval arxiv large tool count accuracy`
6. `"too many tools" LLM function calling recommended maximum number threshold`
7. `MCP tool namespacing grouping "meta-tool" OR "toolset" pattern reduce context`
8. `Gorilla ToolBench tool retrieval accuracy scaling number of tools benchmark`
9. `OpenAI function calling best practices number of functions limit recommendation`
10. `ToolLLM hierarchical API category tree DFSDT tool retrieval paper`
11. `"lazy loading" tools agent context "category" first select then list items pattern engineering blog`
12. `Anthropic skills "how many skills" OR "number of skills" recommend limit best practice`
13. `LangChain "create_retriever_tool" OR "big tool" dynamic tool selection vector store many tools`
14. `AWS Bedrock Agents action groups too many tools OR Azure AI agent tool limit guidance`

### WebFetch célzott lekérések (URL + mire kérdeztünk rá)

- `anthropic.com/engineering/advanced-tool-use` — Tool Search Tool mechanizmus, token/pontosság számok
- `docs.claude.com/.../agent-skills/overview → redirect → platform.claude.com/.../agent-skills/overview` — progresszív feltárás szintjei, token-számok
- `anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills` — progresszív feltárás filozófiája
- `platform.claude.com/docs/en/agents-and-tools/agent-skills/overview` — pontos karakter/token limitek
- `docs.claude.com/.../best-practices → redirect → platform.claude.com/.../best-practices` — SKILL.md hossz-ajánlás, leírás-verseny 100+ skill között
- `askaibrain.com/en/posts/context-engineering-why-600-skills-make-agents-less-effective/` — állítólagos küszöbszám ellenőrzése
- `arxiv.org/abs/2505.03275 (RAG-MCP)` — absztrakt, mért számok
- `arxiv.org/pdf/2505.03275` — pontos számok (N tartomány, pontosság, token)
- `arxiv.org/html/2505.03275v1` — teljes szöveg, degradációs mondatok szó szerint
- `modelcontextprotocol.io/docs/2026-07-28/develop/clients/client-best-practices` — hivatalos MCP ajánlás küszöbre
- `github.com/modelcontextprotocol/modelcontextprotocol/discussions/2036` — gyakorlói (fórum) tapasztalat, számok
- `arxiv.org/html/2503.01763 (ToolRet / "Retrieval Models Aren't Tool-Savvy")` — benchmark méret, pontosság
- `developers.openai.com/api/docs/guides/tools-tool-search` — OpenAI tool search küszöb
- `developers.openai.com/api/docs/guides/function-calling` — OpenAI function-count ajánlás
- `achan2013.medium.com/how-many-tools-functions-can-an-ai-agent-has-...` — összegyűjtött vendor-számok
- `platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool` — Anthropic hivatalos küszöb-ajánlás (2x, kereszt-ellenőrizve)
- `blog.synapticlabs.ai/bounded-context-packs-meta-tool-pattern` — meta-tool minta leírása
- `arxiv.org/pdf/2305.15334 (Gorilla)` — skálázási adatok keresése (nem talált relevánsat)
- `huggingface.co/papers/2307.16789 (ToolLLM)` — kategorizálás, retriever leírása
- `resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf` — skill-darabszám küszöb (2x, kereszt-ellenőrizve)
- `cobusgreyling.substack.com/p/bigtool-from-langchain` — LangGraph BigTool leírás
- `aws.amazon.com/blogs/machine-learning/govern-ai-agent-tool-access-with-amazon-bedrock-agentcore-gateway/` — nem talált releváns küszöböt
- `www.mindstudio.ai/blog/context-rot-claude-code-skills-bloated-files` — fájlméret-ajánlás
- `boliv.substack.com/p/lazy-skills-a-token-efficient-approach` — lusta betöltés számai (nem hivatalos, jelölve T3)

### Amit az SQ-04 ügynök tudatosan elhagyott (nem nyitott meg, mert az elsődleges forrásokból már megvolt a válasz)

- Stacklok MCP Optimizer blog (csak keresési találatban jelent meg)
- MarkTechPost Hermes Agent cikk (másodkézből ugyanazt a 49%→74% Opus 4 számot közli, amit közvetlenül az Anthropic oldaláról már megszereztünk elsődleges közelségben)
- ASCII News cikk (hír-összefoglaló, nem hordozott új adatot a címen túl)

## SQ-05

Forrás: `sq05/searches.md`. Minden keresés a `WebSearch` toollal futott (US-only index), dátum: 2026-09-06.

1. `"Lost in the Middle" Liu et al. how language models use long contexts arxiv`
2. `Chroma research "context rot" long context performance degradation report`
3. `NoLiMa benchmark distractor long context literal match LLM`
4. `RULER benchmark long context distractor needle in a haystack degradation`
5. `instruction following degradation long context IFEval FollowBench LongIns`
6. `"Large Language Models Can Be Easily Distracted by Irrelevant Context" Shi et al GSM-IC`
7. `system prompt length degrades performance other tasks unrelated instructions measurement`
8. `"many short" vs "few long" instructions same token count LLM performance comparison`
9. `tool description bloat context degrades agent performance benchmark tokens`
10. `"context rot" Chroma 18 models needle question haystack distractor results`
11. `FollowBench number of constraints instruction following accuracy degrades`
12. `"instruction interference" multiple unrelated instructions same prompt LLM performance study`
13. `number of tools available degrades unrelated task accuracy LLM agent study`
14. `"context interference" OR "task interference" system prompt many tool definitions hurts reasoning`
15. `LongIns benchmark long context instruction following LLM degradation paper`
16. `arxiv 2608.12426 "Phase Transitions in Compositional Constraint Satisfaction" (létezés-ellenőrzés)`
17. `arxiv 2608.02639 "Instruction Stacking Collapse" "Prompt Compilation" (létezés-ellenőrzés)`
18. `"LLMs Get Lost In Multi-Turn Conversation" paper degradation accumulated context`
19. `"prompt bloat" LLM output quality study accuracy drop percentage`
20. `"Same Task, More Tokens" reasoning degradation input length paper`
21. `"How Easily do Irrelevant Inputs Skew the Responses" LLM semantic similarity paper`
22. `consolidated tool description vs many separate tools same token budget accuracy comparison study`
23. `"number of options" classification prompt length degrades LLM accuracy choosing category`
24. `arxiv "system prompt" length "other tasks" degrade unrelated benchmark experiment 2026`
25. `IFEval score long context appended irrelevant text degradation experiment`
26. `"Prospective Memory Failures in Large Language Models" arxiv 2603.23530 GSM8K formatting constraint (létezés-ellenőrzés)`

### WebFetch hívások (elsődleges tartalom-lekérések)

A fenti keresésekből kiválasztott URL-eket `WebFetch`-csel is lekérték, jellemzően kétszer is (egyszer az absztrakt, egyszer a HTML/PDF teljes szöveg felől), hogy a számokat kereszt-ellenőrizzék. A teljes lista a `linkek.md`-ben. Kiemelt kereszt-ellenőrzések:

- NoLiMa GPT-4o 32K = 69,7% szám két független fetch-ben (abs + html + pdf) egyezett.
- RULER GPT-4 táblázat (96.6/96.3/95.2/93.2/87.0/81.2) két független fetch-ben egyezett.
- A Chroma "Context Rot" riport disztraktor-szekciójának pontos százalékai csak grafikonon szerepelnek, szöveges/táblázatos formában NEM — ezt két külön promptú fetch is megerősítette (ld. `hianyok.md`).

### Nem futtatott, de fontolóra vett irányok

- Nem kerestek rá közvetlenül konkrét termékek (LangChain, LlamaIndex, AutoGPT stb.) saját "system prompt hossz" ajánlásaira — ez SQ-04 hatóköre a tervben, itt csak a MÉRÉSI oldalra koncentráltak.
- Nem futtattak külön keresést kifejezetten magyar nyelvű forrásokra — a téma (LLM kutatás) domináns nyelve angol, és a terv is angol nyelvű elsődleges forrásokat vár el.

## Nem elérhető / blokkolt domainek

Forrás: `01-search-log/blocked.jsonl`.

| al-kérdés | URL | ok |
|---|---|---|
| SQ-01 | https://aihirfolyam.hu/2024/05/gpt-4o-magyar-dragabb-mint-angol/ | WebFetch returned CLIENT_ERROR: page returned a 403 client error |
| SQ-02 | https://arxiv.org/html/2505.10570v1 | WebFetch tool refused to reproduce paper body text citing copyright policy ('reproducing substantial portions as exact text would constitute reproducing copyrighted material'), offering only a 125-character-quote-limited paraphrase. Full per-model Results tables for LongFuncEval's tool-catalog-size experiment could not be captured verbatim; only the abstract (via the separate /abs/ URL) was securable with real quotes. |

Az SQ-04 és SQ-05 kutatási körben nem készült külön `blocked.jsonl`-szerű napló; a `sq04/searches.md` és `sq05/searches.md` fájlok nem jeleznek elérhetetlen/blokkolt domaint, csak tudatosan mellőzött (nem releváns, vagy már máshonnan megvan) linkeket — ezeket a fenti SQ-04/SQ-05 szakaszok "tudatosan elhagyott"/"nem futtatott" alpontjai sorolják fel.
