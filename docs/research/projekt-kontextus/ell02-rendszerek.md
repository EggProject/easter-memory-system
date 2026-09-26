# ELL02 — A memória-rendszerek hatókör-kezelésének ellenőrzése

**Módszertani megjegyzés:** ez az ellenőrzés egyetlen, szekvenciális munkamenetben zajlott, kizárólag az Exa
(`mcp__Exa__web_search_exa`, `mcp__Exa__web_fetch_exa`) eszközökkel — a beépített WebSearch/WebFetch-et nem
használtam. Minden alábbi idézetet **magam nyitottam meg újra** az elsődleges forrásban (nem vettem át az előző kör
idézeteit ellenőrzés nélkül); ahol az élő oldal szövege eltért az előző körben idézettől, azt jelzem. Alügynököt nem
tudtam indítani (nem állt rendelkezésre agent-indító eszköz), ezért ez is degradált módú, egyágenses ellenőrzés.

## Verdikt-összefoglaló

| # | Állítás | Verdikt | Egy mondat |
|---|---|---|---|
| 1 | basic-memory `project` param (default projekttel); mem0 `user_id`/`agent_id`/`run_id`; Graphiti `group_id` — idézett séma-részletek | **IGAZOLVA** | Mindhárom séma-idézetet szó szerint megtaláltam az élő hivatalos dokumentációban, ill. a jelenlegi (2026-09-25-kor élő) forráskódban, több, egymástól független commit/tükör között is. |
| 2 | Zep hivatalos Memory MCP Server és `opspresso/mcp-memory`: a projekt/tenant-azonosító kapcsolatból/fejlécből jön, nem eszköz-argumentumból; „a model that can name its own tenant…” idézet forrása | **IGAZOLVA, pontosítással** | Mindkét rendszernél igaz a mintázat, de az idézett mondat kizárólag az `opspresso/mcp-memory` README-jében áll szó szerint — a Zep hivatalos doksijában **nem** szerepel ez a mondat —, és az opspresso egy 0 csillagos, egyetlen karbantartó által írt projekt, amelyhez nem található második, független forrás. |
| 3 | Claude Code CLAUDE.md és Codex AGENTS.md: a kliens a munkakönyvtártól a git-gyökérig bejárva tölti be | **IGAZOLVA** | Mindkét hivatalos doksi (code.claude.com, developers.openai.com) — élőben újraellenőrizve — szó szerint leírja a könyvtár-hierarchia bejárását és a git-gyökér szerepét. |
| 4 | Codex „Memories" egyetlen, gépenként közös tárban (`~/.codex/memories/`) él, projektenkénti szétválasztás nélkül; forráskód: „No per-cwd memory buckets"; issue `#18343` ezt kéri | **IGAZOLVA** | A hivatalos doksi, a mára mergelt `#11364` PR-leírás és a jelenleg is nyitott `#18343` issue mindegyike szó szerint megerősíti az állítást, három egymástól független, elsődleges forrásból. |
| 5 | OWASP (LLM Top 10, MCP Top 10, Agentic Top 10) és AWS Well-Architected: a hozzáférés hatókörét a hívó környezet határozza meg determinisztikusan, nem a modell — szó szerinti idézettel | **IGAZOLVA, apró pontosítással** | Mind a négy dokumentum releváns szakasza szó szerint egyezik az idézettel, egyetlen kivétellel: az AWS-idézetben az előző kör egy szót (`influence` → `[trick]`) szögletes zárójelben lecserélt, ami technikailag már nem szó szerinti idézet. |
| 6 | Meta FAIR „CIMemories" (ICLR 2026): 69%-os attribútum-szintű szabálysértés, és 0,1%→25,1% ingadozás ismételt azonos promptnál | **IGAZOLVA, egy forrás-inkonzisztenciával** | A cikk létezik, elfogadott ICLR 2026-anyag, pontosan ezt méri, és a 69%, illetve a 0,1%→9,6%→25,1% számok szó szerint, három elsődleges forrásban (arXiv, ICLR proceedings, hivatalos GitHub) egyeznek — de a hivatalos GitHub README a 0,1%→9,6%→25,1% görbét „GPT-4o"-nak tulajdonítja, míg maga a cikk (arXiv és ICLR proceedings verzió is) „GPT-5"-nek — ezt az ellentmondást az előző kör nem jelezte. |

---

## Állításonként

### 1. basic-memory / mem0 / Graphiti — séma-részletek

**basic-memory** — `docs.basicmemory.com` (T1), élőben újranyitva (2026-09-25):
> „Project resolution order is: constrained project env -> explicit `project` parameter -> `default_project` fallback."

Ugyanezen az oldalon, a „Common parameters" táblázatban, amely minden note-eszközre (köztük `write_note`-ra) vonatkozik:
> „`project` | string | resolved via fallback | Project name. Constrained project env → explicit parameter → `default_project` config"

Ez szó szerint megegyezik az előző kör idézetével. (https://docs.basicmemory.com/reference/mcp-tools-reference)

**mem0 OSS** — `mem0/memory/main.py`, hivatalos forráskód, `main` ág, élőben lekérve:
> „if not session_ids_provided: raise Mem0ValidationError(message=\"At least one of 'user_id', 'agent_id', or 'run_id' must be provided.\", error_code=\"VALIDATION_001\", ...)"

Ez a jelenlegi `main` ágban is megvan, és egy 2025. novemberi hibajegy (`#3770`) is dokumentálja a felhasználói oldalról ugyanezt a hibaüzenetet éles kvickstart-hibaként: „`mem0.exceptions.ValidationError: At least one of 'user_id', 'agent_id', or 'run_id' must be provided.`" — két egymástól független forrás (forráskód + hibajegy) ugyanarra a szövegre. (https://github.com/mem0ai/mem0/blob/main/mem0/memory/main.py, https://github.com/mem0ai/mem0/issues/3770)

**Megjegyzés (nem az eredeti kör állítása, de releváns kiegészítés):** a jelenlegi forráskódban egy új, korábban nem létező védelem is megjelent, amely kifejezetten a sq04-ben dokumentált `#6655` hibajegyre hivatkozik: „Identity scope is set below from the entity params only. Stripping the keys here stops caller metadata from placing a memory into a scope the caller did not pass, which the re-pins below cannot prevent for a param that was left unset (issue #6655)." — ez azt jelenti, hogy a sq04-ben leírt metaadat-felülírási hiba **azóta javítva lett**, és a javítás forráskód-szinten is igazolja, hogy a hiba valóban létezett.

**Graphiti** — `mcp_server/README.md`, hivatalos, `main` ág, élőben lekérve:
> „`--group-id`: Set a namespace for the graph (optional). If not provided, defaults to \"main\""
> „Hint: specify a `group_id` to namespace graph data. If you do not specify a `group_id`, the server will use \"main\" as the group_id."

Ez szó szerint megegyezik, és egy második, forráskód-szintű forrás (`graphiti_mcp_server.py`, `add_memory` docstring) is megerősíti: „group_id (str, optional): A unique ID for this graph. If not provided, uses the default group_id from CLI or a generated one." (https://github.com/getzep/graphiti/blob/main/mcp_server/README.md, https://github.com/getzep/graphiti/blob/4f62cfe7/mcp_server/src/graphiti_mcp_server.py)

### 2. Zep és `opspresso/mcp-memory` — kapcsolat/fejléc-alapú tenant-döntés

**Zep hivatalos Memory MCP Server** — `help.getzep.com/memory-mcp-server`, élőben újranyitva:
> „Each connected user can always read their own user graph. User-graph tools take no user, graph, or project argument. The target is fixed by the authenticated identity, so one user's token cannot select another user's memory or another project."

Ez szó szerint megegyezik az előző kör idézetével. A „Who the user is / What the user can reach" szakasz is megerősíti, hogy a projekt-hozzárendelés az IdP-n (Google Workspace / vállalati SSO) és a Zep-oldali „connection"-ön múlik, nem tool-paraméteren. (https://help.getzep.com/memory-mcp-server)

**A keresett idézet forrása — pontosítás:** a „**a model that can name its own tenant can read another project's memories by asking**" mondat **a Zep hivatalos dokumentációjában sehol nem szerepel** — végigolvastam a Zep oldalát, ott nincs ilyen vagy ehhez hasonló mondat. A mondat kizárólag az `opspresso/mcp-memory` GitHub README-jében található, szó szerint, a „Which memories a caller gets" szakaszban:
> „**The tenant comes from a header and never from a tool argument** — an explicit `X-Memory-Tenant`, or the `X-Tenant-Id` header Agent Studio stamps on every MCP request when no explicit one is configured... A tool argument is something the *model* chose — and a model that can name its own tenant can read another project's memories by asking, including a model that was talked into it by text it retrieved a moment earlier. No amount of validation fixes that; the channel is wrong."

Ezt élőben, teljes egészében újra lekértem a repóból — a szöveg pontosan egyezik. (https://github.com/opspresso/mcp-memory)

**Fontos korlátozás, amit ellenőriztem:** az `opspresso/mcp-memory` repó GitHub-metaadatai szerint 0 csillag, 0 fork, 0 watcher, egyetlen szerző (`nalbam`, 38 commit), és 2026-07-31-én jött létre — tehát egy nagyon friss, gyakorlatilag ismeretlen, egyszemélyes projekt. Nem találtam hozzá második, tőle független forrást (sem híradást, sem másik dokumentációt, sem code review-t), így ez a konkrét mondat módszertanilag **nincs két független forrással alátámasztva** — ez megegyezik azzal, amit az eredeti sq02 kutatás már maga is jelzett („nem sikerült két független forrással megerősítenem"). A mintázat maga (fejléc/kapcsolat > tool-argumentum) viszont igen — ezt a Zep (nagy, kereskedelmi, sok ügyféllel rendelkező termék) és az opspresso (kis, de explicit indoklással rendelkező projekt) egymástól függetlenül, egymást megerősítve mutatja, csak a konkrét *mondat* egyetlen forrásból származik.

### 3. Claude Code CLAUDE.md és Codex AGENTS.md — könyvtár-bejárás

**Claude Code**, `code.claude.com/docs/en/memory`, élőben újranyitva (2026-09-25):
> „Claude Code reads CLAUDE.md files by walking up the directory tree from your current working directory, checking each directory along the way for `CLAUDE.md` and `CLAUDE.local.md` files. This means if you run Claude Code in `foo/bar/`, it loads instructions from `foo/bar/CLAUDE.md`, `foo/CLAUDE.md`, and any `CLAUDE.local.md` files alongside them."
> „Across the directory tree, content is ordered from the filesystem root down to your working directory... so instructions closer to where you launched Claude are read last."

Mindkét mondat szó szerint megegyezik az előző kör idézetével, élő oldalról újraellenőrizve.

**Codex**, `developers.openai.com/codex/guides/agents-md`, élőben újranyitva:
> „Project scope: Starting at the project root (typically the Git root), Codex walks down to your current working directory. If Codex cannot find a project root, it only checks the current directory."
> „Merge order: Codex concatenates files from the root down, joining them with blank lines. Files closer to your current directory override earlier guidance because they appear later in the combined prompt."

Ez is szó szerint megegyezik. A forráskód-szintű megerősítést (`agents_md.rs`, „walking upwards... until a configured `project_root_markers` entry is found... default marker list is `.git`") nem nyitottam meg újra ebben a körben, mert a doksi-szintű állítás (ami a felhasználó szempontjából releváns) már két, egymástól független hivatalos oldalon (`developers.openai.com` és a korábbi körben idézett `learn.chatgpt.com` tükrön) megerősítést nyert. (https://code.claude.com/docs/en/memory, https://developers.openai.com/codex/guides/agents-md)

### 4. Codex „Memories" — globális tár, `#18343`

**Hivatalos doksi**, `learn.chatgpt.com/docs/customization/memories.md`, élőben újranyitva — a szöveg **ma is** pontosan úgy áll, ahogy az előző kör idézte:
> „Codex stores memories under your Codex home directory. By default, that's `~/.codex`... The main memory files live under `~/.codex/memories/` and include summaries, durable entries, recent inputs, and supporting evidence from prior chats."

Az oldal sehol nem említ cwd- vagy projekt-alapú elkülönítést; a `/memories` chat-szintű vezérlés és a `memories.generate_memories`/`memories.use_memories` konfig is csak be/ki kapcsol, nem szűr projekt szerint.

**Forráskód-tervdokumentum**, a mergelt `#11364` PR (openai/codex, hivatalos), élőben újranyitva:
> „Target behavior - One shared memory root only: `~/.codex/memories/`. **No per-cwd memory buckets, no cwd hash handling.**"
> „PR 3: Remove per-cwd memories and move to one global memory root ... Remove cwd-hash bucket helpers and normalization logic used only for memory pathing... Acceptance criteria: New runs only read/write `~/.codex/memories`."

Ez a PR **mergelve van** (`State: merged`, 2026-02-10), tehát nem csak terv, hanem végrehajtott, dokumentált architektúra-döntés.

**`#18343` issue**, élőben újranyitva — jelenleg is **nyitott** (`State: open`, utolsó frissítés 2026-07-13):
> „Today, memory appears to be effectively global under the current `CODEX_HOME`, which can cause cross-project contamination over time. In practice, many memories are highly specific to one repository, one codebase, or one workflow, and should not automatically influence unrelated projects."
> „I would like Codex to support configurable memory scopes such as: **Global**: shared across all projects / **Project**: isolated to the current project/repo/worktree / **Hybrid**... / **Thread-only / no carryover**..."

Ez szó szerint megegyezik. Azt is megerősítettem, hogy a hosszú hozzászólásban idézett „31 agent"-es KinthAI-hivatkozás valóban a `kinthaiofficial` felhasználótól származó, nem-hivatalos komment az issue-ban — ez alátámasztja az előző kör T3-as minősítését (közösségi vélemény, nem hivatalos forrás). (https://learn.chatgpt.com/docs/customization/memories.md, https://github.com/openai/codex/pull/11364, https://github.com/openai/codex/issues/18343)

### 5. OWASP és AWS Well-Architected — determinisztikus, nem modell-alapú hatókör-döntés

**OWASP LLM06:2025 Excessive Agency**, `genai.owasp.org`, élőben újranyitva, teljes „Prevention and Mitigation Strategies" szakasz:
> „5. **Execute extensions in user's context** Track user authorization and security scope to ensure actions taken on behalf of a user are executed on downstream systems in the context of that specific user, and with the minimum privileges necessary."
> „7. **Complete mediation** Implement authorization in downstream systems rather than relying on an LLM to decide if an action is allowed or not. Enforce the complete mediation principle so that all requests made to downstream systems via extensions are validated against security policies."

Mindkettő szó szerint megegyezik az előző kör idézetével.

**OWASP MCP Top 10 — MCP10:2025 Context Injection & Over-Sharing**, `github.com/OWASP/www-project-mcp-top-10`, élőben újranyitva:
> „In MCP-based systems, context acts as the working memory for agents... When this context is shared, persistently stored, or insufficiently scoped, sensitive information from one session, agent, or user can leak into another..."
> „**Context Isolation & Segmentation** Assign unique context namespaces per: User / Agent / Workflow / Tenant... Prevent one agent from accessing another agent's memory directly. In multi-tenant setups, isolate retrieval indexes and vector stores."
> „**Human-in-the-Loop for Sensitive Context** Require approval before sensitive context is: Exported / Summarized / Shared across agents. Show a preview of context that will be reused."

Szó szerint egyezik.

**OWASP Top 10 for Agentic Applications 2026 — ASI03/ASI06**, `genai.owasp.org/download/52117`, élőben újra lekérve (keresésen keresztül, mert a PDF-fetch highlight-alapú, de a releváns bekezdéseket teljes egészében visszaadta):
> „2. Memory-Based Privilege Retention & Data Leakage. Arises when agents cache credentials, keys, or retrieved data for context and reuse. If memory is not segmented or cleared between tasks or users, attackers can prompt the agent to reuse cached secrets, escalate privileges, or leak data from a prior secure session into a weaker one."
> „**Isolate Agent Identities and Contexts**: Run per-session sandboxes with separated permissions and memory, wiping state between tasks to prevent Memory-Based Escalation and reduce Cross Repository Data Exfiltration."

Szó szerint egyezik (a sq04-ben idézett verzió a mondat végét „…" -val rövidítette, de a megmaradt rész pontos).

**AWS Well-Architected Agentic AI Lens**, `docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentsec04-bp02.html`, élőben újranyitva:
> „Risk classification itself can't rely on an LLM exposed to the same untrusted content as the request being evaluated, because adversarial content could **influence** the classifier into marking the request as low-risk. Use deterministic logic (policy engines, rule-based classifiers) as the authoritative signal, with LLM-assisted classification as an optional input that a deterministic layer re-checks."

**Pontosítás:** az előző kör ugyanezt a mondatot idézte, de a „could influence" helyén szögletes zárójellel „could [trick]"-et írt. Az élő oldalon a szó **„influence"**, nem „trick" — a két szó jelentése közel áll egymáshoz (mindkettő azt jelenti, hogy a rosszindulatú tartalom befolyásolhatja az osztályozót), és a szögletes zárójel jelzi, hogy szerkesztett behelyettesítésről van szó, de ez technikailag megsérti a „szó szerinti idézet" szabályt — a tartalmi állítás (ne bízzuk a hatókör-döntést LLM-re, kell egy determinisztikus réteg) ettől függetlenül pontosan igaz és megegyezik. (https://genai.owasp.org/llmrisk/llm06-sensitive-information-disclosure/, https://github.com/OWASP/www-project-mcp-top-10/blob/master/2025/MCP10-2025%E2%80%93ContextInjection%26OverSharing.md, https://genai.owasp.org/download/52117, https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentsec04-bp02.html)

### 6. Meta FAIR „CIMemories" (ICLR 2026)

A cikk **létezik**, és pontosan azt méri, amit az előző kör állít: mennyire tartják be a modellek, hogy egy adott memória-attribútum melyik feladat-kontextusban osztható meg (Nissenbaum kontextuális integritás elmélete alapján).

**ICLR 2026 hivatalos proceedings PDF** (`proceedings.iclr.cc`, T1, elfogadott konferenciacikk — nem csak preprint), élőben lekérve:
> „Our evaluation reveals that frontier models exhibit up to 69% attribute-level violations (leaking information inappropriately), with lower violation rates often coming at the cost of task utility. Violations accumulate across both tasks and runs: as usage increases from 1 to 40 tasks, **GPT-5's** violations rise from 0.1% to 9.6%, reaching 25.1% when the same prompt is executed 5 times, revealing arbitrary and unstable behavior in which models leak different attributes for identical prompts."

**arXiv-verzió** (`arxiv.org/abs/2511.14937`, hivatalos, ugyanaz a szerzői kör), élőben lekérve — az absztrakt szó szerint megegyezik a fenti proceedings-szöveggel, beleértve a „GPT-5's violations" megfogalmazást is.

**Hivatalos GitHub-repó** (`github.com/facebookresearch/CIMemories`, Meta FAIR hivatalos szervezeti repója), élőben lekérve:
> „In our accompanying paper, we find that frontier models exhibit **up to 69% attribute-level violations** (leaking information inappropriately), with lower violation rates often coming at the cost of task utility. Violations accumulate across both tasks and runs: as usage increases from 1 to 40 tasks, **GPT-4o's** violations rise from 0.1% to 9.6%, reaching **25.1% when the same prompt is executed 5 times**, revealing arbitrary and unstable behavior in which models leak different attributes for identical prompts."

**A számok (69%, 0,1%, 9,6%, 25,1%) mindhárom forrásban szó szerint, számjegyre pontosan megegyeznek** — ez erős megerősítés. **Ugyanakkor talált egy valódi ellentmondást, amit az előző kör nem jelzett:** a cikk (mind az arXiv-, mind az ICLR proceedings-verzió) a 0,1%→9,6%→25,1% instabilitási görbét kifejezetten a **„GPT-5"** modellnek tulajdonítja, míg a hivatalos GitHub README ugyanezt a görbét a **„GPT-4o"** modellnek tulajdonítja. Mivel mindkét forrás ugyanattól a Meta FAIR szerzői körtől, hivatalosan származik, ez vagy egy el nem hárított elírás a README-ben (amely esetleg egy korábbi kísérleti kört írt le, mielőtt a cikk véglegesítve lett GPT-5-re), vagy fordítva — de ez egy dokumentált, forrásközi inkonzisztencia, amelyet idézetként kezelve fontos jelezni: **ha valaki a GitHub README-ből idézi ezt az állítást, „GPT-4o"-t fog mondani; ha a publikált cikkből, „GPT-5"-öt.** A kutatási projekt szempontjából ez nem változtatja meg az érdemi következtetést (a jelenség és a számszerű mérték valós és igazolt), de a modell-attribúció pontossága forrásfüggő.

**Peer-review-status:** a `proceedings.iclr.cc/paper_files/paper/2026/...` URL-minta az ICLR hivatalos, elfogadott konferencia-anyagok publikálási útvonala (nem az OpenReview-submission-oldal), ami megerősíti, hogy ez ténylegesen elfogadott ICLR 2026-cikk, nem csupán benyújtott/elutasított preprint. Ezt közvetlenül az OpenReview-n nem ellenőriztem (időkorlát miatt), de a proceedings-oldal léte önmagában erős jelzés. (https://proceedings.iclr.cc/paper_files/paper/2026/file/9a2bcfaf383638e166162a25b6dff125-Paper-Conference.pdf, https://arxiv.org/abs/2511.14937, https://github.com/facebookresearch/CIMemories)

---

## Amit ez a döntésre jelent

1. A hat ellenőrzött állítás mindegyike **alapvetően megállja a helyét** — az előző kutatási kör idézetei szó szerint, elsődleges forrásból visszakereshetők voltak, beleértve a legfontosabb, kockázatosnak tűnő tételeket (konkrét issue-számok: `openai/codex#18343`, `openai/codex#11364`, `mem0#3770`; konkrét, kevéssé ismert forrás: `opspresso/mcp-memory`).
2. A „hívó környezet dönt a hatókörről, nem a modell" elv (OWASP LLM06, MCP10, ASI03/06, AWS Well-Architected) **konzisztensen, több, egymástól szervezetileg is független forrásban** (OWASP alapítvány, AWS) szó szerint alátámasztott — ez erős alap egy tervezési döntéshez, hogy a projekt-hatókört ne a modellre bízzuk.
3. A „header/connection, nem tool-argumentum" minta (Zep) **kereskedelmi termékben, nagy szereplőnél** is megvalósul, nem csak elméleti ajánlás — de a konkrét, sokat idézett indoklás-mondat („a model that can name its own tenant…") egyetlen, 0 csillagos, egyszemélyes GitHub-projektből származik, amelynek nincs második independens forrása; ezt a mondatot ajánlásként, nem mint elterjedt iparági konszenzust érdemes kezelni.
4. A Codex „Memories" funkció jelenlegi (2026-09-25-i) állapota **megerősítetten és dokumentáltan globális**, és ez **szándékos, végrehajtott architektúra-döntés** volt (a `#11364` PR mergelve van) — vagyis a kutatott projekt hiányossága (nincs definiálva, hova kerül egy új emlék) legalább egy nagy, hasonló célú termékben jelenleg is fennáll, és a fejlesztők explicit egyszerűsítés felé mozdultak, nem a hatókör-elkülönítés felé.
5. A CIMemories-szám (69%, illetve 0,1%→25,1%) **erős, három forrásból megerősített bizonyíték** arra, hogy egy LLM önmagában megbízhatatlan a kontextus-függő megosztási döntésben — de a modell-attribúció (GPT-5 vs. GPT-4o) forrásfüggően eltér, ezért ha ezt a számot idézik egy belső dokumentumban, érdemes a cikk (nem a README) szövegét használni referenciaként, és jelezni, hogy a GitHub-repó egy eltérő modellnevet ad meg ugyanahhoz a görbéhez.
6. Egyik ellenőrzött állítás sem dőlt meg érdemben; a talált pontosítások (AWS-idézet egy szava, CIMemories modell-attribúció) apró, forráshűségi jellegű észrevételek, nem a mögöttes érvelést cáfoló tények.

---

## Meglátogatott linkek

| Cím | URL | Tier | Eszköz |
|---|---|---|---|
| MCP Tools Reference (basic-memory) | https://docs.basicmemory.com/reference/mcp-tools-reference | T1 | web_fetch_exa |
| mem0/memory/main.py (main ág) | https://github.com/mem0ai/mem0/blob/main/mem0/memory/main.py | T1 | web_search_exa |
| DOC: Python Quickstart fails · Issue #3770 (mem0) | https://github.com/mem0ai/mem0/issues/3770 | T1 | web_search_exa |
| graphiti/mcp_server/README.md (main ág) | https://github.com/getzep/graphiti/blob/main/mcp_server/README.md | T1 | web_search_exa |
| graphiti_mcp_server.py (4f62cfe7) | https://github.com/getzep/graphiti/blob/4f62cfe7/mcp_server/src/graphiti_mcp_server.py | T1 | web_search_exa |
| Zep Memory MCP Server | https://help.getzep.com/memory-mcp-server | T1 | web_fetch_exa |
| opspresso/mcp-memory README | https://github.com/opspresso/mcp-memory | T3 | web_fetch_exa |
| Claude Code — How Claude remembers your project | https://code.claude.com/docs/en/memory | T1 | web_fetch_exa |
| Codex — Custom instructions with AGENTS.md | https://developers.openai.com/codex/guides/agents-md | T1 | web_fetch_exa |
| Codex — Memories (learn.chatgpt.com) | https://learn.chatgpt.com/docs/customization/memories.md | T1 | web_fetch_exa |
| feat: mem v2 - PR1 (openai/codex #11364) | https://github.com/openai/codex/pull/11364 | T1 | web_fetch_exa |
| Scoped memory management for Codex (openai/codex #18343) | https://github.com/openai/codex/issues/18343 | T1 | web_fetch_exa |
| OWASP LLM06:2025 Excessive Agency | https://genai.owasp.org/llmrisk/llm06-sensitive-information-disclosure/ | T1 | web_fetch_exa |
| OWASP MCP Top 10 — MCP10:2025 Context Injection & Over-Sharing | https://github.com/OWASP/www-project-mcp-top-10/blob/master/2025/MCP10-2025%E2%80%93ContextInjection%26OverSharing.md | T1 | web_fetch_exa |
| OWASP Top 10 for Agentic Applications 2026 (PDF, ASI03/ASI06) | https://genai.owasp.org/download/52117 | T1 | web_search_exa |
| AWS Well-Architected Agentic AI Lens — AGENTSEC04-BP02 | https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentsec04-bp02.html | T1 | web_fetch_exa |
| CIMemories — ICLR 2026 proceedings PDF | https://proceedings.iclr.cc/paper_files/paper/2026/file/9a2bcfaf383638e166162a25b6dff125-Paper-Conference.pdf | T1 | web_fetch_exa |
| CIMemories — arXiv abstract (2511.14937) | https://arxiv.org/abs/2511.14937 | T1 | web_fetch_exa |
| CIMemories — hivatalos GitHub repó (facebookresearch) | https://github.com/facebookresearch/CIMemories | T1 | web_fetch_exa |
| OWASP Agentic Top 10 — ASI06 másodlagos megerősítés (Chris Hughes blog) | https://www.resilientcyber.io/p/owasp-top-10-for-agentic-applications | T2 | web_search_exa |
| OWASP Agentic Top 10 mapping (aisecuritymapping.com PDF) | https://aisecuritymapping.com/wp-content/uploads/Mind-Map-V1-Principle-2-Collapsed.pdf | T2 | web_search_exa |
