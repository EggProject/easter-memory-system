# SQ02 — Hogyan döntik el a meglévő memória-rendszerek, hová kerül egy új emlék, és honnan tudják a projektet?

> **Degradált mód megjegyzése:** ez a kutatás egyetlen ügynökként, alügynökök indítása nélkül készült (a futtató környezetben nem állt rendelkezésre olyan eszköz, amellyel párhuzamos kutató-alügynökök indíthatók lettek volna a `deep-web-research` skill elvei szerint). A kutatás ezért egy hosszú, szekvenciális Exa-keresési munkamenetben zajlott, ugyanazokkal a forrás- és idézési szabályokkal (elsődleges forrás, szó szerinti idézet, kereszt-megerősítés), de alügynökök általi párhuzamos lefedettség nélkül. A kizárólagos keresőeszköz az Exa (`mcp__Exa__web_search_exa`, `mcp__Exa__web_fetch_exa`) volt; a beépített WebSearch/WebFetch-et nem használtam.

## Rövid válasz

A vizsgált rendszerek négy, egymástól jól elkülöníthető mintát követnek a „hova kerüljön az emlék" és a „honnan tudom a projektet" kérdésre. (1) **Explicit hívó-paraméter, szerver-oldali fallback-kel**: a basic-memory `project` paramétere, a mem0/OpenMemory `user_id`/`agent_id`/`app_id`/`run_id`-je és a Graphiti `group_id`-je mind a hívó (az ágens) által, tool-hívásban adható meg, de mindegyiknél van szerver-oldali alapérték (`default_project` konfig, `DEFAULT_USER_ID` env, `--group-id main`), ha a hívó nem ad meg semmit. (2) **Kapcsolat-/fejléc-alapú, a hívó által nem felülírható kötés**: a Zep hivatalos Memory MCP Servere és a `opspresso/mcp-memory` tudatosan **kizárja** a tool-argumentumot a bérlő/projekt kiválasztásából — a projekt/identitás az OAuth-bejelentkezéshez vagy egy HTTP fejléchez van kötve, mert (idézve az opspresso indoklását) „a model that can name its own tenant can read another project's memories by asking". (3) **Fájlrendszer-hierarchia / munkakönyvtár-bejárás, teljesen automatikus**: a Claude Code CLAUDE.md-je és a Codex AGENTS.md-je a cwd-ből felfelé sétálva, projekt-gyökérig (jellemzően `.git`) automatikusan megtalálja a releváns fájlokat, tool-hívás vagy paraméter nélkül; a Serena `--project-from-cwd` opciója szintén automatikus detektálást ad. (4) **Explicit aktiválás/session-állapot**: a Serena `activate_project` tool-ja és a Letta agent-hez kötött blokk-modellje a projektet egy korábbi hívás által beállított munkamenet-állapotként kezeli. A több szintű hatókör (személyes/projekt/közös) szinte mindegyik rendszerben megvan valamilyen formában (Claude Code: managed→user→project→local; Serena: project vs. `global/`; Zep: user graph vs. group graph; mem0 Platformnál org→project→user/agent/run), de a döntést szinte sosem a szerver hozza automatikusan: vagy az ágens dönt explicit felhasználói utasítás alapján (Serena: „If explicitly instructed, use the global/ prefix"), vagy a felhasználó/fejlesztő állítja be konfigurációban/fájlhelyen (Claude Code: melyik fájlba ír a user), vagy a szerver üzemeltetője rögzíti kapcsolat-szinten (Zep, opspresso). A saját projekt kutatási hiányossága — hogy sehol nincs explicit definiálva, honnan tudja az ágens/szerver az aktuális projektet — tehát nem egyedi: a Codex saját „memories" funkciója (a `AGENTS.md`-től eltérő, tanult-kontextus rétege) jelenleg **explicit módon, forráskódban dokumentáltan globális**, projekt-izoláció nélkül fut, és a közösség (GitHub issue) éppen emiatt kéri számon a projekt-szintű elkülönítést — ez szinte szó szerint ugyanaz a hiány, amit ez a kutatási projekt is azonosított.

---

## 1. basic-memory

**Forrás típusa:** T1 — hivatalos dokumentáció (`docs.basicmemory.com`, tükrözve `basicmachines-co-basic-memory.mintlify.app` és `basicmachines.mintlify.app` alatt is → 2 független tükör ugyanattól a projekttől, tartalmilag megegyezik).

### 1. Írási eszköz sémája
A `write_note` tool Python-szignatúrája (mintlify-tükör):
> „`async def write_note(title: str, content: str, directory: str, project: Optional[str] = None, workspace: Optional[str] = None, tags: list[str] | str | None = None, note_type: str = "note", metadata: dict | None = None, overwrite: bool | None = None, output_format: Literal["text", "json"] = "text", context: Context | None = None) -> str | dict`"

A `project` mező leírása: „Project name to write to. **Optional** - server resolves using hierarchy." — tehát a `project` paraméter nem kötelező.

### 2. Honnan tudja a rendszert az aktuális projektet
A hivatalos MCP Tools Reference táblázata a feloldási sorrendet írja le:
> „Project resolution order is: constrained project env -> explicit `project` parameter -> `default_project` fallback."
> „`BASIC_MEMORY_MCP_PROJECT` — Environment-level project constraint for MCP sessions. Locks operations to one project for that process/session — Highest-priority project constraint"

A konfigurációs doksi szerint:
> „`default_project` — Fallback project name used when tools/commands do not pass a project. Type: `string | null` — Default: unset — the first configured project is used (`"main"` on fresh installs, where a `main` project is seeded)."

A koncepció-doksi (Projects and folders) az ágens viselkedését is leírja:
> „When you run a command or an AI tool like `write_note`, it targets the project you name — each call carries a `project` parameter or CLI argument. If you don't specify one, it goes to the default project... The AI will simply pass `project="personal"` on its next tool calls — there's no switch step; it discovers your projects with `list_memory_projects`."

Van egy „single-project mode" is, ahol a `project` paraméter teljesen figyelmen kívül marad:
> „`basic-memory mcp --project work-notes` — This locks the entire MCP session - the `project` parameter in tool calls will be ignored."

### 3. Több szintű hatókör, ki dönt
A basic-memory-nak **nincs** beépített személyes/projekt/közös hierarchiája — projektjei egyenrangú, névvel azonosított, egymástól elszigetelt tárolók (`projects: {"main": {...}, "research": {...}}` a configban), a felhasználó/ágens dönt melyikbe ír, a döntést a `project` paraméter vagy a session-szintű alapértelmezés hordozza. Nincs automatikus „ez tech-tudás, ez menjen feljebb" logika.

### 4. Olvasás/keresés hatóköre
A mintlify-tükör (guides/mcp-tools-reference) explicit kimondja:
> „`search_notes(...)` # Searches current project only" — „`write_note(...)` # Creates note in current project" szemben a globális `list_projects()`, `create_project()` hívásokkal, amelyek projekt-függetlenek.

---

## 2. mem0 (Platform + OSS) és OpenMemory MCP

**Forrás típusa:** T1 — `docs.mem0.ai` (hivatalos), `github.com/mem0ai/mem0` forráskód (hivatalos repó), `github.com/mem0ai/mem0-mcp` (hivatalos MCP wrapper repó). Kiegészítésül T2/T3: `github.com/pinkpixel-dev/mem0-mcp` (nem hivatalos, közösségi wrapper — külön jelölve).

### 2.1 mem0 OSS (`Memory` osztály, self-hosted)

**Írási séma** (`mem0/memory/main.py`, hivatalos forráskód):
> „`def add(self, messages, *, user_id: Optional[str] = None, agent_id: Optional[str] = None, run_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None, ...)` ... Adds new memories scoped to a single session id (e.g. `user_id`, `agent_id`, or `run_id`). **One of those ids is required.**"

A validáció forráskódból:
> „`if not session_ids_provided: raise Mem0ValidationError(message="At least one of 'user_id', 'agent_id', or 'run_id' must be provided.", ...)`"

Tehát a mem0 OSS-nek **nincs** `project` fogalma és **nincs** szerver-oldali alapértelmezés — kötelező explicit azonosítót adni minden híváskor, különben kivétel dobódik. Ez éles ellentétben áll a basic-memory-val, ahol van fallback.

**Projekt forrása:** kizárólag a hívó adja meg, minden egyes hívásban; nincs env-alapú vagy konfig-alapú fallback a nyílt forráskódú `Memory` osztályban.

### 2.2 mem0 Platform (`MemoryClient`, felhő)

A `MemoryClient` konstruktora opcionális `org_id`/`project_id` mezőket vesz fel (LLM.md, hivatalos):
> „`client = MemoryClient(api_key="your-api-key", host="https://api.mem0.ai", org_id="your-org-id", project_id="your-project-id")`"

Itt tehát megjelenik egy valódi, Platform-szintű `project_id`, ami a Pro-csomag szervezeti struktúráját (org → project) reprezentálja, konfig-időben (kliens-inicializáláskor) rögzítve, nem minden hívásnál újra megadva.

### 2.3 Nem hivatalos MCP wrapperek (T2/T3, óvatosan kezelve)

A `pinkpixel-dev/mem0-mcp` (közösségi, nem a mem0ai szervezet repója) egy negyedik paramétert ad hozzá:
> „**`appId`** - Identifies the user's project/application - **this controls project scope!** (optional) ... Fallback: `DEFAULT_APP_ID` environment variable"

**Ellentmondás/inkonzisztencia:** ez a nem hivatalos wrapper az `app_id`-t nevezi „projekt hatókörnek", miközben a hivatalos Mem0 Platform egy teljesen külön, valódi `project_id` mezőt definiál Pro-csomagban — a két fogalom a mem0-ökoszisztémán belül nem esik egybe, és ezt sehol nem tisztázzák egyértelműen (lásd Ellentmondások fejezet).

Elsőbbségi sorrend ugyanebben a wrapperben (T3, közösségi doksi):
> „1. **Tool Parameters** (highest priority) - Values provided by the LLM in tool calls / 2. **Environment Variables** (fallback) - Values from your MCP configuration"

### 2.4 OpenMemory MCP (mem0ai hivatalos, önhosztolt)

**Forrás:** `github.com/mem0ai/mem0/blob/main/openmemory/api/app/mcp_server.py` (hivatalos forráskód) + `mem0.ai/blog/introducing-openmemory-mcp` (hivatalos blog).

Itt a projekt/identitás **nem tool-paraméter**, hanem az URL útvonalból és kontextusváltozóból jön:
> „`user_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("user_id")` / `client_name_var: contextvars.ContextVar[str] = contextvars.ContextVar("client_name")`"
> „`@mcp_router.get("/{client_name}/sse/{user_id}") async def handle_sse(request: Request): ... uid = request.path_params.get("user_id") ... client_name = request.path_params.get("client_name")`"

Az `add_memories` tool szignatúrája **nem is tartalmaz** `user_id` paramétert:
> „`@mcp.tool(...) async def add_memories(text: str, infer: bool = True) -> str: uid = user_id_var.get(None); client_name = client_name_var.get(None) ... if not uid: return "Error: user_id not provided"`"

Vagyis az OpenMemory az ágenshez rendelt kapcsolat (SSE endpoint URL `/{client_name}/sse/{user_id}`) alapján dönti el, ki az adott felhasználó és melyik alkalmazás (client) ír — ez a „kapcsolat-szintű" mintát mutatja, hasonlóan a Zephez.

**Keresés hatóköre:** a `search_memory` tool mindig a saját `user_id`-jára szűrt: „`filters = {"user_id": uid}`" — más felhasználó memóriája elérhetetlen ezen a tool-on keresztül.

**Több szintű hatókör:** két szint — `user_id` (személy) és `app_id`/`client_name` (alkalmazás/eszköz, pl. Cursor vs. Claude Desktop) —, ACL-lel szabályozható engedélyezés/szüneteltetés app-onként (mem0.ai hivatalos blog: „Pause or revoke any client's access at app or memory level").

### 2.5 mem0 OpenCode-integráció — automatikus, git-alapú projekt-detektálás (T1, `docs.mem0.ai`)

Ez a hivatalos integráció explicit automatikus, munkakönyvtár-alapú projekt-forrást ad, tool-paraméter nélkül:
> „The project id (`app_id`) is derived from your git remote (`owner-repo`), falling back to the git repo's root directory name, then the current directory."

És egy háromszintű hatókör-modellt is bevezet, amit az ágens dönt el (nyelvi kérés alapján), nem a szerver:
> „| Scope | Reads | Writes | | --- | --- | --- | | `project` (default) | this repo (`user_id` + `app_id`) | this repo | | `session` | this run only (`+ run_id`) | this run | | `global` | all your projects in the workspace (`app_id: "*"`) | user-wide |"
> „Ask naturally, for example, 'search my memories across all my projects'. The agent passes `scope: "global"`. For normal questions it stays scoped to the current project automatically."

---

## 3. Letta

**Forrás típusa:** T1 — `docs.letta.com` (hivatalos), `github.com/letta-ai/letta` (hivatalos forráskód).

### 1–2. Írási séma és a „projekt" forrása
Letta-ban a memória alapegysége nem a „projekt", hanem az **agent** és az ahhoz csatolt **memory block**. A `project_id` egy Letta Cloud-specifikus, adminisztratív mező, ami az agenteket rendezi a felhő-dashboardon, **nem** befolyásolja, melyik memória-blokkot melyik agent látja.

OpenAPI-specifikáció (hivatalos, `letta-agents-api-openapi.yml`):
> „`project_id` — in: query — required: false — description: Search agents by project ID - **this will default to your default project on cloud**"

Agent-létrehozáskor fejlécen keresztül is átadható (hivatalos forráskód, `routers/v1/agents.py`):
> „`x_project: str | None = Header(None, alias="X-Project", description="The project slug to associate with the agent (cloud only).")`"

Tehát Lettánál a „projekt" forrása: (a) explicit `project_id` query-paraméter, vagy (b) `X-Project` HTTP fejléc, vagy (c) hiányukban a cloud fiók alapértelmezett projektje — **self-hosted (nem cloud) telepítésnél a `project_id` fogalma nem is releváns** (a doksi mindenhol „cloud only"-t ír).

### 3. Több szintű hatókör, ki dönt
A tényleges memória-hatókört nem a `project_id`, hanem a **block attachment** adja: egy memory block egy vagy több agenthez csatolható, és ha több agent van hozzácsatolva, közös (shared) memóriává válik.
> „Memory blocks can be attached to multiple agents at once ('shared blocks')." / „Shareable - Multiple agents can access the same block; update once, visible everywhere"

A döntést itt kizárólag a **fejlesztő** hozza meg API-hívással (explicit attach/detach), nem az ágens saját belátásából és nem szerver-szabály alapján:
> „You can also directly create blocks and attach them to an agent. This can be useful if you want to create blocks that are shared between multiple agents." / „You can also attach blocks to existing agents"

A MemFS-modell (git-repó-alapú memória) is megerősíti, hogy a megosztás mindig explicit fejlesztői/agent-döntés:
> „Shared memory repositories give several agents access to the same files. Attaching one recompiles the agent's system prompt..."

### 4. Olvasás/keresés hatóköre
Az archívumi keresés (`archival_memory_search`) szigorúan az adott agent saját archívumára korlátozódik; a blokk-lista (`list blocks`) viszont globálisan is lekérdezhető label szerint: „You can list all blocks, optionally filtering by label or searching by label text. This is useful for finding blocks across your project." — itt a „project" szó köznyelvi értelemben szerepel, nem a `project_id` mezőre utal.

---

## 4. Zep — hivatalos Memory MCP Server, és a Graphiti MCP szerver

**Forrás típusa:** T1 — `help.getzep.com` (hivatalos doksi), `blog.getzep.com` (hivatalos blog), `github.com/getzep/graphiti` (hivatalos forráskód).

### 4.1 Zep Memory MCP Server (a jelenlegi, hivatalos termék)

Ez a rendszer **explicit, tudatos döntéssel kizárja** a hívó (ágens/tool-argumentum) szerepét a projekt/felhasználó kiválasztásából — ez a leginkább releváns minta a kutatási kérdés szempontjából.

**1–2. Írási séma, projekt forrása:**
> „Each connected user can always read their own user graph. **User-graph tools take no user, graph, or project argument.** The target is fixed by the authenticated identity, so one user's token cannot select another user's memory or another project."
> „**The project cannot be selected by an MCP request or tool argument.** ... Zep binds the issued token to the selected connection and project."

Ehelyett a projekt/identitás forrása egy OAuth-alapú, adminisztrátor által konfigurált kapcsolat:
> „What the user can reach. Zep uses the user's work email to discover the organization's identity provider. After authentication, Zep finds every enabled project connection that admits the verified identity. It selects the project automatically when there is one, shows a chooser when there is more than one, and denies access when there are none."

**3. Több szintű hatókör, ki dönt:** user graph (személyes) vs. **standalone graph** (megosztott, csapat-szintű), amit `graph_id` azonosít, és amit egy `list_graphs`/directory tool tesz felfedezhetővé:
> „`list_graphs` — read — List other accessible graphs in the project (graph directory)" / „`search_graph_in` — read — Search a selected standalone graph by `graph_id`"

A hozzáférést nem az ágens, hanem a szerver üzemeltetője (admin) dönti el kapcsolat-szinten, két módban:
> „Connections can use project-wide access or UserGroup ABAC to grant specific graphs to each user. Plans without ABAC retain project-wide access." / „project-wide mode makes every standalone graph available; UserGroup ABAC mode limits the directory and selected-graph tools to explicit grants."

**4. Keresés hatóköre:** alapból csak a saját user graph, csapat/projekt-szintű grafokhoz csak explicit `graph_id` és jogosultság birtokában:
> „A graph a user is not authorized to see is absent from directory results and counts entirely."

### 4.2 Graphiti MCP szerver (a Zep nyílt forráskódú, önhosztolható komponense — más architektúra, mint a 4.1-es hivatalos termék)

**Forrás:** `github.com/getzep/graphiti/blob/main/mcp_server/README.md` (hivatalos), `help.getzep.com/graphiti/getting-started/mcp-server` (hivatalos).

**1. Írási séma** (`add_memory` tool):
> „`group_id (str, optional): A unique ID for this graph. If not provided, uses the default group_id from CLI or a generated one.`"

**2. Projekt forrása:** parancssori argumentum indításkor, VAGY tool-hívásban explicit `group_id`, ezek hiányában szerver-oldali alapérték:
> „`--group-id`: Set a namespace for the graph (optional). **If not provided, defaults to "main"**." (README)
> „Hint: specify a `group_id` to namespace graph data. If you do not specify a `group_id`, the server will use 'main' as the group_id." (ugyanaz a README, más helyen — megerősítve)

Egy korábbi verzió forráskódja (`graphiti_mcp_server.py`) még véletlenszerű UUID-t generált alapértékként, nem "main"-t:
> „`else: config.group_id = f'graph_{uuid.uuid4().hex[:8]}'; logger.info(f'Generated random group_id: {config.group_id}')`"

**Ellentmondás/időbeli eltérés:** a dokumentáció (mindkét hivatalos forrás) ma „main"-t ír alapértékként, de a régebbi forráskód-verzió (`dbe21a19` commit) véletlenszerű UUID-t generált — ez egy dokumentált viselkedés-változás a projekt történetében, nem egy jelenleg is fennálló ellentmondás.

**3. Több szintű hatókör:** a Graphiti-nak nincs beépített személyes/projekt/közös hierarchiája — a `group_id` egy lapos, tetszőleges string-namespace; a hierarchiát (ha van) a hívó fél építi fel konvencióval (pl. `"acme-corp/project-a"`).

**4. Keresés hatóköre:** a kereső tool-ok (`search_nodes`, `search_memory_facts`) `group_ids` paramétere lista is lehet, több namespace egyszerre kereshető, vagy ha üres, a konfigurált alapértelmezett group-ra esik vissza:
> „`group_ids: Optional[list[str]] = None ... effective_group_ids = (group_ids if group_ids is not None else [config.group_id] if config.group_id else [])`"

---

## 5. Claude Code saját memóriája (CLAUDE.md-hierarchia + auto memory)

**Forrás típusa:** T1 — `code.claude.com/docs/en/memory` (Anthropic hivatalos doksi), megerősítve 2 független tükrön/harmadik féltől (`claudeable.co`, `developertoolkit.ai`, `claude.yourdocs.dev`, GitHub-issue-k az `anthropics/claude-code` repóban).

### 1–2. Séma és a projekt forrása
A CLAUDE.md-nek **nincs tool-paramétere** — tisztán fájlrendszer-hierarchia és munkakönyvtár-bejárás dönti el, mi töltődik be:
> „Claude Code reads CLAUDE.md files by walking up the directory tree from your current working directory, checking each directory along the way for `CLAUDE.md` and `CLAUDE.local.md` files. This means if you run Claude Code in `foo/bar/`, it loads instructions from `foo/bar/CLAUDE.md`, `foo/CLAUDE.md`, and any `CLAUDE.local.md` files alongside them."

Négy hatókör, helyalapúan definiálva (nem paraméterrel, hanem azzal, hogy a felhasználó *hova írja a fájlt*):
> „| Scope | Location | ... | | Managed policy | `/etc/claude-code/CLAUDE.md` stb. | ... | | User instructions | `~/.claude/CLAUDE.md` | Personal preferences for all projects | Just you (all projects) | | Project instructions | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team-shared instructions for the project | Team members via source control | | Local instructions | `./CLAUDE.local.md` | Personal project-specific preferences... | Just you (current project) |"

Betöltési sorrend és elsőbbség:
> „Across the directory tree, content is ordered from the filesystem root down to your working directory... so instructions closer to where you launched Claude are read last." — „Within each directory, `CLAUDE.local.md` is appended after `CLAUDE.md`, so your personal notes are the last thing Claude reads at that level."

Az **auto memory** (amit maga Claude ír, nem a felhasználó) projekt-azonosítása git-repó-alapú, nem cwd-alapú:
> „Each project gets its own memory directory at `~/.claude/projects//memory/`. The `` path is **derived from the git repository**, so all worktrees and subdirectories within the same repo share one auto memory directory. Outside a git repo, the project root is used instead."

### 3. Több szintű hatókör, ki dönt
Négy hierarchikus szint (managed policy → user → project → local), **a felhasználó dönti el**, melyik fájlba ír a szándéka szerint — nincs automatikus besorolási logika, a döntés tisztán a fájl elhelyezésén (`~/.claude/CLAUDE.md` vs. `./CLAUDE.md` vs. `./CLAUDE.local.md`) múlik. Az auto memory esetében **Claude dönt** (ágens, nem a szerver), mit ér meg megjegyezni: „Claude doesn't save something every session. It decides what's worth remembering based on whether the information would be useful in a future conversation." Az auto memory viszont csak projekt-szintű — nincs "user-wide auto memory" vagy "org-wide auto memory" réteg.

### 4. Olvasás/keresés hatóköre
A CLAUDE.md-fájlok betöltése kizárólag a munkakönyvtár hierarchiájára korlátozódik (a gyökérig, nem tovább): „Claude Code recurses up to (but not including) the root directory /". Az auto memory a projektkönyvtár saját `MEMORY.md`-jére és a hozzá tartozó témafájlokra korlátozódik, más projekt memóriája nem érhető el a session-ből.

---

## 6. Cursor — Rules és memories

**Forrás típusa:** T1 — `cursor.com/docs/rules`, `cursor.com/help/customization/rules.md` (hivatalos), keresztellenőrizve a `prod.cursor.com` tükörrel (megegyezik) és harmadik féltől (`learncursor.dev`, `memories.sh` — T3, kiegészítő).

### 1–2. Séma és a projekt forrása
Cursor-nak nincs saját MCP írási tool-ja a rule-okhoz — a `.cursor/rules/*.mdc` fájlokat vagy a felhasználó írja kézzel, vagy egy beépített `/create-rule` slash command generálja. A „projekt" forrása egyszerűen a **workspace gyökérkönyvtár**:
> „Project rules live in `.cursor/rules` as `.mdc` files and are version-controlled and scoped to your codebase."

Egy `.mdc` fájl frontmatter-je (`description`, `globs`, `alwaysApply`) dönti el, mikor lép életbe — de ez fájl-útvonal, nem hatókör:
> „| `alwaysApply` | `description` | `globs` | Behavior | | --- | --- | --- | --- | | `true` | — | — | Always included... | | `false` | — | provided | Auto-attached when a matching file is in context. |"

### 3. Több szintű hatókör, ki dönt
Három explicit szint, amit a **felhasználó** dönt el a rule elhelyezésével:
> „- Project rules are stored in `.cursor/rules/` inside your project folder. They're version-controlled with git. - User rules in Cursor Settings are stored on your Cursor account. They apply across all your projects and sync when you sign in on another machine. ... - Team rules are stored on Cursor's servers and managed from the team dashboard. They sync automatically to all team members."

A `CLAUDE.md`-t és az `AGENTS.md`-t is natívan beolvassa Cursor, de más szabállyal:
> „`CLAUDE.md` files are always applied to every conversation, regardless of any `alwaysApply` frontmatter setting." — míg az `AGENTS.md` almappákban is öröklődik: „Nested `AGENTS.md` support in subdirectories is now available."

### 4. Olvasás/keresés hatóköre
Nincs „keresés" tool a beépített rule-rendszerben (statikus betöltés indításkor/relevancia szerint), viszont egy harmadik féltől származó MCP-integráció (`memories.sh`, T3) mutatja meg, hogyan lehet ezt kiterjeszteni MCP-szerverré — ez a rendszer kívül esik Cursor hivatalos termékén, ezért csak kiegészítő adatként szerepel.

---

## 7. Codex (OpenAI) — AGENTS.md és a „Memories" funkció

**Forrás típusa:** T1 — `developers.openai.com/codex` (hivatalos), `learn.chatgpt.com/docs` (hivatalos, ugyanaz a tartalom más URL-en → 2. független megerősítés), `github.com/openai/codex` (hivatalos forráskód, Rust) — 3 független, egymást megerősítő elsődleges forrás.

### 7.1 AGENTS.md — projekt-szintű, automatikus (ez működik jól)

**1–2. Séma és forrás:** nincs tool-paraméter; könyvtár-bejárás projekt-gyökértől (git-gyökér) a cwd-ig:
> „Project scope: Starting at the project root (typically the Git root), Codex walks down to your current working directory. If Codex cannot find a project root, it only checks the current directory."
> „Merge order: Codex concatenates files from the root down, joining them with blank lines. Files closer to your current directory override earlier guidance because they appear later in the combined prompt."

Forráskód-szintű megerősítés (`codex-rs/core/src/agents_md.rs`, hivatalos):
> „Determine the project root by walking upwards from the current working directory until a configured `project_root_markers` entry is found. When `project_root_markers` is unset, the default marker list is used (`.git`)."

**Dokumentált korlát (ellentmondás — lásd Ellentmondások):** a `project_doc_max_bytes` (alapból 32 KiB) **kumulatív** költségvetés a teljes root→cwd láncra, nem fájlonkénti — ezt egy hivatalos GitHub-issue (`openai/codex#36371`) írja le, két, egymásnak ellentmondó doksi-oldalra hivatkozva.

### 7.2 „Memories" — jelenleg GLOBÁLIS, nincs projekt-izoláció (ez a releváns párhuzam a kutatott hiányossággal)

Ez a réteg **elkülönül** az AGENTS.md-től, és a saját tanult-kontextus rétege — ez az, amiről a hivatalos doksi (`learn.chatgpt.com/docs/customization/memories.md`, T1) ezt írja:
> „Codex stores memories under your Codex home directory. By default, that's `~/.codex`... The main memory files live under `~/.codex/memories/` and include summaries, durable entries, recent inputs, and supporting evidence from prior chats."

Ez a doksi **nem** említ projekt-szintű elkülönítést — és a forráskód (hivatalos PR-terv, `github.com/openai/codex/pull/11364`, „feat: mem v2 - PR1") ezt explicit meg is erősíti, hogy szándékosan és dokumentáltan globális:
> „**Target behavior** - One shared memory root only: `~/.codex/memories/`. **No per-cwd memory buckets, no cwd hash handling.**"
> „PR 3: Remove per-cwd memories and move to one global memory root ... Remove cwd-hash bucket helpers and normalization logic used only for memory pathing... Acceptance criteria: New runs only read/write `~/.codex/memories`. No new cwd-scoped consolidation jobs are enqueued."

Ez azt jelenti, hogy a Codex fejlesztői **korábban volt** valamilyen cwd-alapú (per-projekt) memória-elkülönítés, és **explicit döntéssel egyszerűsítették globálissá** — ellentétes irányba mozdulva, mint amit ez a kutatási projekt tervez.

A közösség ezt hiányként azonosította — egy nyitott hivatalos GitHub-issue (`openai/codex#18343`, „Scoped memory management for Codex (global, project...)"), amely szó szerint a mi kutatási kérdésünket veti fel:
> „Today, memory appears to be effectively global under the current `CODEX_HOME`, which can cause cross-project contamination over time. In practice, many memories are highly specific to one repository, one codebase, or one workflow, and should not automatically influence unrelated projects."
> „I would like Codex to support configurable memory scopes such as: **Global**: shared across all projects / **Project**: isolated to the current project/repo/worktree / **Hybrid**... / **Thread-only / no carryover**..."

Fontos módszertani megjegyzés: ennek az issue-nak a hosszú hozzászólásai (idézve a keresési találatban) külső, nem-hivatalos blogokra (`blog.kinthai.ai`) és állítólagos saját tapasztalatokra hivatkoznak egy „31 agent" méretű rendszerről — ezek **T3, nem ellenőrzött, közösségi vélemények**, nem hivatalos Codex-dokumentáció, és itt csak azért szerepelnek, mert jól illusztrálják a piaci konszenzust arról, milyen hierarchiát (global → namespace/org → project → session) szoktak javasolni ilyen esetekre.

**3–4. Hatókör, keresés:** mivel a „memories" réteg jelenleg egyetlen globális gyökeret használ, nincs projekt-szintű szűrés sem olvasáskor/injektáláskor — a `memories.use_memories` konfig csak be/kikapcsolja a teljes funkciót, nem szűri projekt szerint (`learn.chatgpt.com/docs/customization/memories.md`, T1).

---

## 8. Serena

**Forrás típusa:** T1 — `oraios.github.io/serena` (hivatalos doksi), `github.com/oraios/serena` (hivatalos forráskód).

### 1–2. Séma és a projekt forrása — háromféle mechanizmus, kontextustól függően

**(a) Explicit ágens-hívás konverzáció közben** (`activate_project` tool):
> „while in a conversation, by telling the LLM to activate a project, e.g., 'Activate the project /path/to/my_project' (for first-time activation with auto-creation) / 'Activate the project my_project'"
> „Note that this option requires the `activate_project` tool to be active, which it isn't in single-project contexts like `ide` or `claude-code` if a project is provided at startup."

**(b) Parancssori argumentum indításkor** (single-project mód, tipikusan Claude Code / IDE-kliensek esetén):
> „when the MCP server starts, by passing the project path or name as a command-line argument... `--project <path|name>`"

**(c) Automatikus cwd-detektálás:**
> „`--project-from-cwd`: auto-detect the project from current working directory (looking for a directory containing `.serena/project.yml` or `.git` in parent directories and activating the containing directory as the project root, if any). This option is intended for CLI-based agents like Claude Code, Gemini and Codex."

A `write_memory` tool sémája (hivatalos forráskód, `memory_tools.py`) — ez a **legpontosabb, szó szerinti válasz a 3. kérdésre** (ki dönt a hatókörről):
> „Write information (utf-8-encoded) about this project that can be useful for future tasks to a memory in md format. The memory name should be meaningful and can include '/' to organize into topics (e.g., 'auth/login/logic'). **If explicitly instructed, use the "global/" prefix** for writing a memory that is shared across projects (e.g., 'global/java/style_guide')"

### 3. Több szintű hatókör, ki dönt
Két ortogonális szint (hivatalos doksi, `045_memories.html`):
> „Two orthogonal memory scopes - per-project (committed alongside the code) and global (shared across all your projects) - can be combined freely."
> „Global memories use the top-level topic `global`, i.e. **whenever a memory name starts with `global/`**, it is stored in the global memories directory (`~/.serena/memories/global/`) and is shared across all projects."

A döntést tehát **az ágens hozza**, de a tool docstring kifejezetten korlátozza: „If explicitly instructed" / „The 'global' topic should only be used if explicitly instructed" — azaz alapértelmezésben mindig projekt-szintűre ír, a globálisra váltás user-utasításhoz kötött konvenció, nem automatikus/heurisztikus döntés.

Read-only védelem regex-mintával, ami szerver-/konfig-oldali szabályt is bevezet a döntésbe:
> „If you want to protect them from accidental modification by the agent, you can add regex patterns to `read_only_memory_patterns` in your global or project-level configuration. For example, setting 'global/.*' will mark all global memories as read-only."

A `query_project` tool egy negyedik, ritkább esetet fed le: explicit, **másik** regisztrált projekt kódjának/szimbólumainak lekérdezése (nem memóriaolvasás, hanem kód-hozzáférés) engedéllyel:
> „If, while working on a project, you want Serena to be able to read code or other information from another project... this can be enabled via the `query_project` tool."

### 4. Olvasás/keresés hatóköre
`list_memories`/`read_memory` alapból az aktív projekt memóriáit adja vissza, de topikkal címezhető a globális réteg is:
> „If the topic is omitted, both global and project-specific memories are returned." (forráskód, `MemoriesManager.list_memories`)

---

## 9. cognee

**Forrás típusa:** T1 — `docs.cognee.ai` (hivatalos), `raw.githubusercontent.com/topoteretes/cognee` README (hivatalos), `github.com/topoteretes/cognee` PR/commit (hivatalos forráskód-változtatás).

### 1–2. Séma és a projekt forrása — client-alapú, nem cwd-alapú
A cognee MCP-je **nem a munkakönyvtárból**, hanem **a csatlakozó MCP-kliens azonosságából** vezeti le az alapértelmezett „projektet" (itt: dataset):
> „**Agent Scoping (per-client default datasets)** — By default, each MCP client gets its own auto-named dataset (e.g. Cursor → `cursor_vscode_memory`, Claude Code → `claude_code_memory`) so different agents don't share memory unintentionally. The dataset is created on demand the first time a client writes to it."
> „LLM-direct calls to `cognify`, `remember`, `improve`, and `cognify_status` route to the agent-scoped dataset when `dataset_name` is omitted. Pass `dataset_name` explicitly to override (e.g. `dataset_name="main_dataset"` still works)."

Ez egy **negyedik, eddig nem látott mintázat**: a „projekt" itt nem a felhasználó munkakönyvtára vagy git-repója, hanem az **AI-kliens típusa** (Cursor vs. Claude Code vs. …) — ha valaki két különböző repót nyit meg ugyanabban a kliensben, alapból ugyanabba a datasetbe kerülnek, hacsak nem adnak meg explicit `dataset_name`-et.

A `remember`/`recall`/`forget` a jelenlegi (2026-as) egyszerűsített, ajánlott felület:
> „The MCP server intentionally exposes only the memory API: `remember`, `recall`, and `forget`... Operational helpers such as `cognify`, `search`, `list_data`, `delete`, `prune`, `improve`, and document retrieval helpers are kept internal and are not exposed as MCP tools [by default]."

Az alacsonyabb szintű `cognify`/`add` réteg paramétere (hivatalos Python API, `docs.cognee.ai/python-api/add`):
> „`async def add(data, dataset_name: str = 'main_dataset', ..., dataset_id: Optional[UUID] = None, ...)` — dataset_name: Name of the dataset to store data in. **Defaults to 'main_dataset'.**"

### 3. Több szintű hatókör, ki dönt
A cognee-nak nincs personal/project/shared elnevezésű beépített hierarchiája, hanem **datasetek** vannak, tulajdonossal, és egy explicit engedélyezési kapcsoló dönti el, mennyire szigetelt az adatbázis-réteg:
> „**`true` (default)** — each `(user, dataset)` pair gets its own per-dataset Kuzu + LanceDB... and search is strictly per-dataset. **`false`** — all datasets share one Kuzu graph DB and one LanceDB. The dataset filter is honored for top-level data points, but `GRAPH_COMPLETION` traversal can pull connected nodes from any dataset."

A megosztás (személyes → közös) explicit, tulajdonos-vezérelt engedélyezéssel történik, UUID-alapon, nem automatikusan:
> „Datasets sent by name will only map to datasets owned by the request sender. To search datasets not owned by the request sender, dataset UUID is needed. If dataset_ids is provided, the datasets name list is ignored."

### 4. Olvasás/keresés hatóköre
Alapból minden hozzáférhető datasetre kiterjed, ha nincs szűrés megadva:
> „`datasets` | `str` | `None` | Comma-separated dataset names. Name lookup is owner-scoped." és „`recall` currently accepts dataset names, not `dataset_ids`. If Bob is querying Alice's shared dataset, `datasets='shared_dataset'` can fail even when Bob has permission to use it. In that case, either omit `datasets` to search across all accessible datasets..."

---

## 10. Kiegészítés: az MCP hivatalos referencia „memory" szervere (baseline, nulladik szint)

**Forrás típusa:** T1 — `github.com/modelcontextprotocol/servers/blob/main/src/memory/README.md` (a Model Context Protocol szervezet hivatalos referencia-implementációja), megerősítve NPM-regisztri leírással (`registry.npmjs.org`) és a forráskóddal (`index.ts`) — 3 független forrás.

Ez a legegyszerűbb, „projekt" fogalom **nélküli** baseline: egyetlen JSONL-fájl, amelynek helyét kizárólag a szerver **üzemeltetője** (deploy-time env var) dönti el, tool-hívás vagy session-állapot nélkül:
> „`MEMORY_FILE_PATH`: Path to the memory storage JSONL file (default: `memory.jsonl` in the server directory)"

Nincs `create_entities`/`search_nodes` tool-nak semmilyen hatókör-paramétere (`entities`, `query` stb. az egyetlen bemenet) — a teljes gráf egyetlen lapos névtér, projekt/felhasználó megkülönböztetés nélkül. Ez azért fontos referenciapont, mert megmutatja, milyen a „nulla megoldás" azon a skálán, amin a többi rendszer mozog.

---

## 11. Kiegészítés: Anthropic saját `memory` tool-ja (Claude API, nem MCP)

**Forrás típusa:** T1 — `platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool` (Anthropic hivatalos doksi), megerősítve az Anthropic hivatalos blogbejegyzésével (`claude.com/blog/context-management`) és a hivatalos cookbook-kal (`github.com/anthropics/anthropic-cookbook`) — 3 független hivatalos forrás.

Ez nem MCP-szerver, hanem egy **kliens-oldali** Anthropic-tool (`memory_20250818`), amit érdemes megemlíteni, mert a célrendszer terve (markdown-fájl-alapú memória) erre erősen hasonlít, és mert világosan mutatja: itt a „projekt" fogalmát **szándékosan nem** definiálja maga az eszköz, hanem teljesen az azt beépítő alkalmazásra bízza:
> „Because the memory tool is client-side, Claude only requests memory operations. Your application executes each request against storage you control... The `/memories` path is a prefix that your handler maps onto real storage, such as a per-user directory or keys in a database. **Memory lives entirely in your application.**"

A tool parancskészlete fájlrendszer-műveletekre hasonlít (`view`, `create`, `str_replace`, `insert`, `delete`, `rename`), de nincs beépített `project`/`scope` paraméter egyikben sem — ezt a hívó alkalmazásnak kell megvalósítania a path-előtag konvenciójával.

---

## 12. Bónusz: más, csapatoknak szóló, távoli memória-MCP-szerverek (a `_kozos.txt` opcionális kérése)

Ezek **kis, nem „mainstream" közösségi projektek** — GitHub README-jük hivatalos forrásnak számít az adott projektre nézve (T1), de a módszertan előírása szerint minden lényeges állítást két független forrással kellene megerősíteni, és **ezt ezeknél a kis projekteknél nem sikerült**: nincs második, tőlük független dokumentáció vagy híradás róluk. Ezt itt jelzem — a lenti idézetek egyetlen forrásra (a saját README-jükre) támaszkodnak.

**`opspresso/mcp-memory`** — ez a legrelevánsabb minta a kutatási kérdés szempontjából, mert a README **kifejezetten megindokolja**, miért a fejléc és nem a tool-argumentum hordozza a bérlő/projekt-azonosítót:
> „**The tenant comes from a header and never from a tool argument** — an explicit `X-Memory-Tenant`, or the `X-Tenant-Id` header Agent Studio stamps on every MCP request when no explicit one is configured... A tool argument is something the *model* chose — and a model that can name its own tenant can read another project's memories by asking, including a model that was talked into it by text it retrieved a moment earlier. No amount of validation fixes that; the channel is wrong."

Ugyanez a szerver két hatókört különböztet meg (`remember` tool `scope` paramétere), és ez is dokumentált tool-séma-idézet:
> „**`remember` takes a `scope`.** `project` (the default, and what every memory written before scopes existed is) is shared by every conversation of the tenant. `conversation` is this conversation's alone... and is recalled, listed and de-duplicated only where the same `X-Conversation-Id` asks."

**`malinkaboy/MCP-Team-memory`** — itt a projekt-azonosító fejléc + UUID kombináció, és van egy explicit `memory_projects` tool a projektek kezelésére:
> „Minimal `.mcp.json` for Claude Code: ... `"headers": { "Authorization": "Bearer <YOUR_TOKEN>", "X-Project-Id": "<PROJECT_UUID>" }`" / „`memory_projects` | Manage projects (list/create/update/delete) |"

**`arpanroy41/nexmem-mcp`** — itt egy env-változó (`NEXMEM_TEAM_NAME`) dönti el a névteret, konfiguráció-időben, minden csapattag azonos értéket állít be:
> „**In team mode**, `NEXMEM_TEAM_NAME` determines the namespace. All team members who set the same team name share one knowledge graph." / „| `MODE=team, TEAM_NAME=platform-eng` | `team:platform-eng` | Everyone with same team name |"

---

## Összefoglaló táblázat

| Rendszer | Cél-/hatókör-paraméter | Projekt forrása | Szintek | Ki dönt a szintről | Keresés hatóköre |
|---|---|---|---|---|---|
| **basic-memory** | `project` (opcionális, tool-paraméter) | Sorrend: `BASIC_MEMORY_MCP_PROJECT` env → tool `project` paraméter → `default_project` config | Lapos, egyenrangú, elnevezett projektek (nincs personal/shared hierarchia) | Az ágens/felhasználó, minden híváskor | Csak az aktuális (aktív/megadott) projekt |
| **mem0 OSS** (`Memory`) | `user_id`/`agent_id`/`run_id` (min. 1 **kötelező**) | Kizárólag a hívó, minden híváskor; nincs env/config fallback | Nincs beépített hierarchia; a fogalmakat (user/agent/run) a hívó tölti meg tartalommal | A hívó (ágens) | Amit a `filters` explicit megad |
| **mem0 Platform** | `org_id`/`project_id` (kliens-init) + `user_id`/`agent_id`/`run_id` (hívásonként) | `project_id` a kliens konstruálásakor rögzített; a session-azonosítók hívásonként | org → project → user/agent/run (Pro csomag) | Fejlesztő (kliens-konfig) + ágens (hívásonkénti id-k) | A megadott entitás-szűrők szerint |
| **OpenMemory MCP** | Nincs tool-paraméter; `user_id`+`client_name` az URL-útvonalból | HTTP-kapcsolat (SSE endpoint `/{client_name}/sse/{user_id}`) | user (személyes) + app/client (eszköz), ACL-lel | Kapcsolat-konfiguráció (ki milyen URL-t kap) | Mindig a saját `user_id`-ra szűrve |
| **Letta** | `project_id` / `X-Project` fejléc (csak Cloud, agent-listázáshoz) | Cloud: query-param vagy fejléc, alapból a fiók default projektje; self-host: nincs ilyen fogalom | Memória-hatókört a **block attachment** adja (agent-specifikus vs. több agenthez csatolt „shared block") | Fejlesztő, explicit API-hívással (attach/detach) | Agent-scópolt (`archival_memory_search`), vagy globális block-lista label szerint |
| **Zep (hivatalos Memory MCP Server)** | **Nincs** — tudatosan kizárva a tool-argumentumból | OAuth-bejelentkezés → admin által konfigurált „connection" → automatikusan/választóval kiválasztott projekt | user graph (személyes) vs. standalone graph (`graph_id`, csapat/projekt) | Szerver-admin (connection-szintű policy: project-wide vagy UserGroup ABAC) | Alapból csak saját user graph; standalone graph csak explicit jogosultsággal |
| **Graphiti MCP (Zep OSS)** | `group_id` (opcionális, tool- vagy CLI-paraméter) | Tool `group_id` → hiányában a `--group-id` CLI-argumentum → hiányában `"main"` (jelenlegi doksi) | Lapos namespace, nincs beépített hierarchia | Az ágens (hívásonként) vagy az üzemeltető (indításkor) | `group_ids` lista is megadható; hiányában a konfigurált alapértelmezett group |
| **Claude Code (CLAUDE.md)** | Nincs tool-paraméter; fájlelhelyezés dönt | Munkakönyvtár-hierarchia bejárása (cwd → gyökér) | Managed policy → User → Project → Local (4 szint, fix precedencia) | A felhasználó (hova írja a fájlt) | Csak a cwd hierarchiája, gyökérig |
| **Claude Code (auto memory)** | Nincs tool-paraméter | Git-repó azonosítja a projektet (worktree-k közösek) | Csak projekt-szintű (nincs user-wide vagy org-wide auto memory) | Claude (az ágens) dönt, mit érdemes megjegyezni | Csak a saját projekt memóriakönyvtára |
| **Cursor (Rules)** | Nincs tool-paraméter; fájlelhelyezés + frontmatter | Workspace-gyökér (`.cursor/rules/`) | Project rules / User rules (fiók) / Team rules (Cursor szerver) | A felhasználó (hova/hogyan menti a rule-t) | Statikus betöltés relevancia/glob szerint, nincs MCP-szintű keresés natívan |
| **Codex (AGENTS.md)** | Nincs tool-paraméter; fájlelhelyezés dönt | Git-gyökértől a cwd-ig bejárás (`project_root_markers`, alapból `.git`) | Global (`~/.codex/AGENTS.md`) → Project (repo, könyvtáranként) | A felhasználó (hova írja a fájlt) | Csak a projekt-gyökér→cwd lánc |
| **Codex (Memories funkció)** | Nincs; jelenleg **explicit globális**, projekt-paraméter nélkül | `~/.codex/memories/` — dokumentáltan **nem** cwd-alapú (korábban volt cwd-hash, szándékosan eltávolítva) | Csak egy (globális) szint jelenleg; közösségi igény van projekt-szintre (nyitott GH-issue) | Nincs döntési pont — mindig globális | Globális, minden korábbi chat-en át, projekt-szűrés nélkül |
| **Serena** | `activate_project` tool / `--project` CLI / `--project-from-cwd` | (a) explicit ágens-hívás, (b) indítási argumentum, (c) automatikus cwd-detektálás (`.serena/project.yml` vagy `.git`) | Project memories vs. `global/` (előtaggal címzett, cross-project) | Az ágens, de a `global/` váltás **csak explicit felhasználói utasításra** (tool-docstring szerint) | Alapból aktív projekt; `global/` topikkal a globális réteg is; `query_project`-tel más projekt kódja is |
| **cognee** | `dataset_name`/`datasets` (opcionális) | **MCP-kliens azonossága** (Cursor, Claude Code stb.) → automatikus, kliens-specifikus dataset-név; explicit paraméterrel felülírható | Datasetek (tulajdonossal), nincs personal/project/shared elnevezés, de `ENABLE_BACKEND_ACCESS_CONTROL` per-(user,dataset) izolációt ad | A rendszer (kliens-azonosítás alapján) alapból; a hívó explicit `dataset_name`-mel felülbírálhatja | Alapból minden hozzáférhető dataset; explicit `datasets` paraméterrel szűkíthető |
| **MCP referencia `memory` szerver** | Nincs | Deploy-time env var (`MEMORY_FILE_PATH`) — egyetlen fájl | Nincs (egyetlen lapos gráf) | Az üzemeltető (deploy-konfig) | Az egész gráf, nincs szűrés |
| **Anthropic `memory` tool (Claude API)** | Nincs beépített; a `/memories` path-előtagot a befogadó alkalmazás értelmezi | A befogadó alkalmazás (nem az eszköz) dönti el, mit jelent egy path | Amit az alkalmazás épít rá (pl. per-user könyvtár) | A befogadó alkalmazás fejlesztője | Amit az alkalmazás engedélyez |
| *(bónusz)* `opspresso/mcp-memory` | Nincs tool-paraméter a bérlőhöz; `remember`-nek van `scope` (`project`/`conversation`) | HTTP fejléc (`X-Memory-Tenant` / `X-Tenant-Id`) — **explicit tervezési döntéssel** kizárva a tool-argumentum | Tenant (=projekt) → ezen belül `project` vs. `conversation` scope | Az üzemeltető (fejléc-konfig) a tenantről; az ágens a `scope`-ról | Tenant saját memóriái + az adott `X-Conversation-Id` |

---

## Ellentmondások

1. **mem0 „app_id mint projekt" vs. mem0 Platform valódi `project_id`-je.** A nem hivatalos `pinkpixel-dev/mem0-mcp` wrapper dokumentációja szerint „`appId` ... this **controls project scope**!", miközben a hivatalos Mem0 Platform (`docs.mem0.ai`, `LLM.md`) egy teljesen külön, valódi `project_id` mezőt definiál a `MemoryClient` konstruktorában (Pro-csomag, org→project hierarchia). A két fogalom terminológiailag ütközik az ökoszisztémán belül; a hivatalos mem0 dokumentáció sehol nem nevezi az `app_id`-t „projekt"-nek.

2. **Codex `project_doc_max_bytes` — fájlonkénti vs. kumulatív korlát.** Ezt egy hivatalos GitHub-issue (`openai/codex#36371`) dokumentálja explicit ellentmondásként két hivatalos doksi-oldal között:
   > „Two documentation pages describe `project_doc_max_bytes` in mutually exclusive ways, and the implementation only matches one of them... **The implementation matches Page B** [kumulatív]... So the budget is **cumulative and order-dependent**, not per file."
   Ez azt jelenti, hogy — a forráskóddal megerősítve (`agents_md.rs`) — egy nagy gyökér-szintű `AGENTS.md` teljesen kiütheti egy mélyebb, specifikusabb `AGENTS.md` betöltését, ami pont az ellenkezője annak, amit „split instructions across nested directories" tanácsként az egyik doksi-oldal javasol.

3. **Claude Code CLAUDE.md-konkatenáció sorrendje/elsőbbsége — történelmi félreértés, ma tisztázott.** Egy nyitott hivatalos GitHub-issue (`anthropics/claude-code#54955`) és egy korábbi feature-request (`#2353`) azt mutatja, hogy a felhasználók korábban nem tudták egyértelműen eldönteni, a „később olvasott" fájl (gyökér vagy cwd-közeli) élvez-e elsőbbséget. A **jelenlegi** hivatalos doksi (`code.claude.com/docs/en/memory`) ezt explicit, egyértelműen tisztázza: „instructions closer to where you launched Claude are read last" — vagyis a cwd-specifikus fájl a legutolsó, tehát facto legerősebb —, ami összhangban van a harmadik féltől származó összefoglalóval is („More specific memory takes precedence over broader memory"). A GitHub-issue-kban leírt korábbi zavart ezért **korábbi, mára feloldott** ellentmondásként jelzem, nem jelenleg is fennálló tartalmi ellentmondásként.

4. **Graphiti `group_id` alapértéke — dokumentált viselkedésváltozás.** A jelenlegi hivatalos README és a jelenlegi hivatalos „getting started" doksi is `"main"`-t ír a `group_id` alapértékeként, míg egy korábbi forráskód-verzió (`dbe21a19` commit, hivatalos repó) véletlenszerű UUID-t generált, ha nem adtak meg `group_id`-t. Ez nem egyidejű ellentmondás, hanem a projekt élete során bekövetkezett, dokumentált viselkedésváltozás — mindkét állapotot pontos verzió/commit-hivatkozással jelöltem.

---

## Amire NINCS forrás

- **Nem találtam hivatalos forrást arra**, hogyan dönt (ha egyáltalán) a Letta **self-hosted** (nem Cloud) telepítése bármiféle „projekt" vagy „workspace" elkülönítésről — a `project_id`/`X-Project` mechanizmus minden hivatalos forrásban kifejezetten „cloud only"-ként van megjelölve, és nem találtam dokumentációt arra, mi történik ugyanezzel önhosztolt Letta szerveren (feltehetően nincs ilyen fogalom, de ezt explicit kimondó hivatalos forrást nem találtam).
- **Nem sikerült két független forrással megerősítenem** a 12. fejezet bónusz-rendszereit (`opspresso/mcp-memory`, `malinkaboy/MCP-Team-memory`, `arpanroy41/nexmem-mcp`, `CedraInteractive/Memory-MCP`, `FlarelyLegal/memory-mcp`) — ezekhez kizárólag a saját GitHub README-jük állt rendelkezésre forrásként, harmadik féltől származó ismertetőt, adopciós adatot vagy független auditot egyikhez sem találtam. Ez konzisztens azzal, hogy ezek kis, feltehetően egy-két fejlesztő által karbantartott közösségi projektek.
- **Nem találtam részletes, hivatalos technikai leírást arra**, hogy a Cursor „User Rules” (fiók-szintű, Cursor Settings-ben tárolt) beállítás pontosan milyen szerver-oldali adatmodellben (milyen „projekt"-fogalommal, ha van neki) tárolódik — a hivatalos doksi csak annyit mond, hogy „stored on your Cursor account" és „sync when you sign in on another machine", technikai részletek (API, adatmodell) nem nyilvánosak.
- **A Zep hivatalos Memory MCP Server pontos ABAC-adatmodelljét** (hogyan van definiálva egy „UserGroup", ki hozza létre, milyen gránularitású a jogosultság) csak a felhasználói dokumentáció szintjén találtam meg, mélyebb (pl. adatbázis-séma szintű) hivatalos leírást nem.

---

## Meglátogatott és felderített linkek

| Cím | URL | Tier | Eszköz | Megjegyzés |
|---|---|---|---|---|
| MCP Tools Reference (basic-memory) | https://docs.basicmemory.com/reference/mcp-tools-reference | T1 | web_search_exa | Hivatalos; `project` paraméter, resolution order |
| Configuration (basic-memory) | https://docs.basicmemory.com/reference/configuration | T1 | web_search_exa | Hivatalos; `default_project`, `BASIC_MEMORY_MCP_PROJECT` |
| Content management (write_note szignatúra) | https://basicmachines-co-basic-memory.mintlify.app/api/mcp/content-management | T1 | web_search_exa | Hivatalos tükör; teljes Python szignatúra |
| Projects and folders | https://docs.basicmemory.com/concepts/projects-and-folders | T1 | web_search_exa | Hivatalos; hogyan dönt az ágens projekt-váltáskor |
| Local user guide (basic-memory) | https://docs.basicmemory.com/local/user-guide | T1 | web_search_exa | Hivatalos; single-project mode, URL resolution |
| CLI Reference (basic-memory) | https://docs.basicmemory.com/reference/cli-reference | T1 | web_search_exa | Hivatalos; `bm project default` |
| MCP tools reference (mintlify tükör, guides) | https://basicmachines.mintlify.app/guides/mcp-tools-reference | T1 | web_search_exa | Hivatalos tükör; „searches current project only” idézet |
| MCP tools (local) | https://docs.basicmemory.com/local/mcp-tools-local | T1 | web_search_exa | Hivatalos |
| PARAMETER_GUIDE.md (pinkpixel mem0-mcp) | https://github.com/pinkpixel-dev/mem0-mcp/blob/main/PARAMETER_GUIDE.md | T3 | web_search_exa | Nem hivatalos wrapper; `appId`="project scope" állítás |
| add_memory — Mem0 MCP Server (Glama) | https://glama.ai/mcp/servers/mem0ai/mem0-mcp/tools/add_memory | T2 | web_search_exa | Harmadik féltől katalogizált tool-séma, hivatalos szerver alapján |
| Add Memory (mem0 docs) | https://docs.mem0.ai/core-concepts/memory-operations/add | T1 | web_search_exa | Hivatalos; user/session identifierek |
| Schema — Mem0 MCP Server (Glama) | https://glama.ai/mcp/servers/mem0ai/mem0-mcp/schema | T2 | web_search_exa | Harmadik féltől katalogizált séma |
| pinkpixel-dev/mem0-mcp README | https://github.com/pinkpixel-dev/mem0-mcp/ | T3 | web_search_exa | Nem hivatalos wrapper, elsőbbségi sorrend idézet |
| mem0.ai/platform/mem0-mcp | https://docs.mem0.ai/platform/mem0-mcp | T1 | web_search_exa | Hivatalos; tool-lista |
| mem0ai/mem0-mcp (hivatalos repó) | https://github.com/mem0ai/mem0-mcp | T1 | web_search_exa | Hivatalos MCP wrapper, `MEM0_DEFAULT_USER_ID` |
| mem0-open-mcp (PyPI) | https://pypi.org/project/mem0-open-mcp/0.1.15/ | T3 | web_search_exa | Nem hivatalos csomag, csak kiegészítő |
| SDK & Tools changelog (mem0) | https://docs.mem0.ai/changelog/sdk | T1 | web_search_exa | Hivatalos; entity-id validáció, filters kontra top-level |
| How to make your clients more context-aware with OpenMemory MCP | https://mem0.ai/blog/how-to-make-your-clients-more-context-aware-with-openmemory-mcp | T1 | web_search_exa | Hivatalos blog; SSE endpoint felépítés |
| mem0/openmemory/api/app/mcp_server.py (main) | https://github.com/mem0ai/mem0/blob/ece7ff6b/openmemory/api/app/mcp_server.py | T1 | web_search_exa | Hivatalos forráskód; contextvars, add_memories |
| mem0/openmemory/.../mcp_server.py (3e6ab394) | https://github.com/mem0ai/mem0/blob/3e6ab394/openmemory/api/app/mcp_server.py | T1 | web_search_exa | Ugyanaz más commit — megerősítés |
| Mem0 OpenCode integráció | https://docs.mem0.ai/integrations/opencode | T1 | web_search_exa | Hivatalos; git-alapú automatikus projekt-detektálás, scope tábla |
| OpenMemory — AI Memory MCP Server | https://mem0.ai/openmemory | T1 | web_search_exa | Hivatalos termékoldal |
| Introducing OpenMemory MCP | https://mem0.ai/blog/introducing-openmemory-mcp | T1 | web_search_exa | Hivatalos launch blog |
| mem0-open-mcp v0.1.15 (PyPI, config) | https://pypi.org/project/mem0-open-mcp/0.1.15/ | T3 | web_search_exa | Nem hivatalos, más URL-struktúra bemutatása |
| Letta memory blocks index | https://docs.letta.com/guides/core-concepts/memory/memory-blocks/index.md | T1 | web_search_exa | Hivatalos; block-modell, shared blocks |
| Letta archival memory | https://docs.letta.com/v1-sdk/memory/archival-memory/ | T1 | web_search_exa | Hivatalos |
| Letta memory blocks (v1-sdk) | https://docs.letta.com/v1-sdk/memory/memory-blocks/ | T1 | web_search_exa | Hivatalos, ismétlés más URL-en |
| Letta Blocks API (typescript) | https://docs.letta.com/api/typescript/resources/agents/subresources/blocks/ | T1 | web_search_exa | Hivatalos; `project_id?` mező a block/agent API-ban |
| Letta Memory overview | https://docs.letta.com/agent-sdk/memory/index.md | T1 | web_search_exa | Hivatalos; MemFS, dreaming |
| Letta MemFS | https://docs.letta.com/concepts/memfs/index.md | T1 | web_search_exa | Hivatalos; git-repó-alapú memória |
| Letta stateful agents | https://docs.letta.com/guides/core-concepts/stateful-agents/index.md | T1 | web_search_exa | Hivatalos alapfogalmak |
| letta-agents-api-openapi.yml (tükör) | https://raw.githubusercontent.com/api-evangelist/letta/refs/heads/main/openapi/letta-agents-api-openapi.yml | T2 | web_search_exa | Harmadik féltől tükrözött hivatalos OpenAPI-spec; `project_id` leírás |
| letta/server/rest_api/routers/v1/agents.py | https://github.com/letta-ai/letta/blob/67013ef1/letta/server/rest_api/routers/v1/agents.py | T1 | web_search_exa | Hivatalos forráskód; `X-Project` header, `project_id` query |
| Letta Templates API | https://docs.letta.com/api/resources/templates/ | T1 | web_search_exa | Hivatalos; `project_slug` |
| letta-ai/letta compare 0.11.7...0.12.1 | https://github.com/letta-ai/letta/compare/0.11.7...0.12.1 | T1 | web_search_exa | Hivatalos changelog; „change project to project slug” |
| Letta Agents API (apis.io tükör) | https://apis.io/apis/letta/letta-agents-api/ | T2 | web_search_exa | Harmadik féltől katalogizált API-lista |
| Letta Templates (typescript) | https://docs.letta.com/api/typescript/resources/templates/ | T1 | web_search_exa | Hivatalos |
| Zep Memory MCP Server | https://help.getzep.com/memory-mcp-server | T1 | web_search_exa | Hivatalos; „no user/graph/project argument” kulcsidézet |
| Zep — Share Memory Across Users (group graphs) | https://help.getzep.com/v2/cookbook/how-to-share-memory-across-users-using-group-graphs.mdx | T1 | web_search_exa | Hivatalos; `group_id` API-példa |
| Zep quickstart | https://help.getzep.com/v2/quickstart.mdx | T1 | web_search_exa | Hivatalos; user graph vs. group graph |
| Zep agent memory quickstart | https://help.getzep.com/quick-start-guide | T1 | web_search_exa | Hivatalos |
| Zep MCP + Claude Agent SDK (Composio) | https://composio.dev/toolkits/zep/framework/claude-agents-sdk | T3 | web_search_exa | Harmadik féltől integrációs útmutató, csak kiegészítő |
| Memory for every agent your team uses (Zep blog) | https://blog.getzep.com/agent-memory-mcp/ | T1 | web_search_exa | Hivatalos; ABAC, connection-modell részletesen |
| mcp-server-zep-cloud (fshamim) | https://github.com/fshamim/mcp-server-zep-cloud/blob/main/README.md | T3 | web_search_exa | Nem hivatalos (közösségi) Zep-wrapper, `ZEP_DEFAULT_USER_ID` prioritási sorrend — csak kiegészítő, más architektúra mint a hivatalos MCP |
| Zep Documentation MCP server | https://help.getzep.com/docs-mcp-server.mdx | T1 | web_search_exa | Hivatalos, de más célú szerver (doksi-kereső, nem memória) |
| Graphiti MCP Server (Zep docs) | https://help.getzep.com/graphiti/getting-started/mcp-server | T1 | web_search_exa | Hivatalos |
| graphiti/mcp_server/README.md | https://github.com/getzep/graphiti/blob/main/mcp_server/README.md | T1 | web_search_exa | Hivatalos; `--group-id`, alapérték „main” |
| Graphiti cursor_rules.md | https://github.com/getzep/graphiti/blob/main/mcp_server/docs/cursor_rules.md | T1 | web_search_exa | Hivatalos; ágens-instrukciók a memóriahasználathoz |
| graphiti_mcp_server.py (dbe21a19) | https://github.com/getzep/graphiti/blob/dbe21a1975b0747cd450ee3aa1b2c72b26f59230/mcp_server/graphiti_mcp_server.py | T1 | web_search_exa | Hivatalos, korábbi verzió — UUID alapérték |
| mcp_server/src/graphiti_mcp_server.py (d631437d) | https://github.com/getzep/graphiti/blob/d631437d/mcp_server/src/graphiti_mcp_server.py | T1 | web_search_exa | Hivatalos, `add_memory` teljes docstring |
| mcp_server/src/graphiti_mcp_server.py (0290e4de) | https://github.com/getzep/graphiti/blob/0290e4de/mcp_server/src/graphiti_mcp_server.py | T1 | web_search_exa | Hivatalos, `search_memory_facts` |
| mcp_server/src/graphiti_mcp_server.py (b59d4ba0) | https://github.com/getzep/graphiti/blob/b59d4ba0/mcp_server/src/graphiti_mcp_server.py | T1 | web_search_exa | Hivatalos, legfrissebb `add_memory` bővített paraméterekkel |
| mcp_server/src/graphiti_mcp_server.py (4f62cfe7) | https://github.com/getzep/graphiti/blob/4f62cfe7/mcp_server/src/graphiti_mcp_server.py | T1 | web_search_exa | Hivatalos, ismétlés más commit-on — megerősítés |
| How Claude remembers your project (Claude Code memory) | https://code.claude.com/docs/en/memory | T1 | web_search_exa | Hivatalos, Anthropic; teljes CLAUDE.md + auto memory leírás |
| Claude Code memory (rsc variáns) | https://code.claude.com/docs/en/memory?_rsc=4Vrbm42DZc3Y7r9j | T1 | web_search_exa | Ugyanaz a hivatalos oldal, technikai URL-variáns — megerősítés |
| GH issue #54955 (CLAUDE.md concatenation ambiguity) | https://github.com/anthropics/claude-code/issues/54955 | T2 | web_search_exa | Hivatalos repó issue-ja, korábbi doksi-félreérthetőség dokumentálása |
| GH issue #2353 (hierarchical CLAUDE.md) | https://github.com/anthropics/claude-code/issues/2353 | T2 | web_search_exa | Hivatalos repó issue-ja, felhasználói elvárás vs. tényleges működés |
| Claude Code Memory Docs (Claudeable, tükör) | https://claudeable.co/claude-md/claude-code-memory-docs | T2 | web_search_exa | Harmadik féltől összefoglaló a hivatalos doksi alapján |
| Claude Code memory system (developertoolkit.ai) | https://developertoolkit.ai/en/claude-code/advanced-techniques/memory-system/ | T2 | web_search_exa | Harmadik féltől részletes összefoglaló, megerősíti a hivatalos doksit |
| Claude Code Memory (claude.yourdocs.dev) | https://claude.yourdocs.dev/docs/claude-code/memory | T2 | web_search_exa | Harmadik féltől tükör/összefoglaló |
| lenneTech/claude-code docs-cache/memory.md | https://github.com/lenneTech/claude-code/blob/main/.claude/docs-cache/memory.md | T2 | web_search_exa | Harmadik fél által cache-elt hivatalos doksi-szöveg, `autoMemoryDirectory` részletek |
| Cursor Rules docs | https://cursor.com/docs/rules | T1 | web_search_exa | Hivatalos; `.mdc`, frontmatter, AGENTS.md |
| Cursor Rules (help) | https://cursor.com/help/customization/rules.md | T1 | web_search_exa | Hivatalos; user/project/team rules |
| Cursor Rules (prod tükör) | https://prod.cursor.com/help/customization/rules | T1 | web_search_exa | Hivatalos staging-tükör, azonos tartalom — megerősítés |
| cursor-project-memory usage doc | https://github.com/general-alexson/cursor-project-memory/blob/main/doc/usage.md | T3 | web_search_exa | Nem hivatalos VS Code/Cursor kiterjesztés, csak kiegészítő |
| general-alexson/cursor-project-memory | https://github.com/general-alexson/cursor-project-memory | T3 | web_search_exa | Nem hivatalos, ugyanaz a projekt |
| memories.sh — Cursor integráció | https://memories.sh/docs/integrations/cursor | T3 | web_search_exa | Nem hivatalos, harmadik féltől MCP-integráció Cursorhoz |
| Cursor rules gyakorlati útmutató (learncursor.dev) | https://www.learncursor.dev/learn/cursor-rules | T2 | web_search_exa | Harmadik féltől, hivatalos doksira alapuló összefoglaló |
| Documentation as context (developertoolkit.ai) | https://developertoolkit.ai/en/shared-workflows/context-management/documentation-as-context/ | T2 | web_search_exa | Harmadik féltől, több rendszert összehasonlító cikk |
| Custom instructions with AGENTS.md (Codex) | https://developers.openai.com/codex/guides/agents-md | T1 | web_search_exa | Hivatalos OpenAI; discovery precedencia |
| Customization (Codex) | https://developers.openai.com/codex/concepts/customization | T1 | web_search_exa | Hivatalos; AGENTS.md + Memories mint két külön réteg |
| Custom instructions with AGENTS.md (learn.chatgpt.com tükör) | https://learn.chatgpt.com/docs/agent-configuration/agents-md | T1 | web_search_exa | Hivatalos tükör, azonos szöveg — megerősítés |
| codex-rs/core/src/project_doc.rs | https://github.com/openai/codex/blob/d807d44a/codex-rs/core/src/project_doc.rs | T1 | web_search_exa | Hivatalos forráskód; project root marker logika |
| codex-rs/core/src/agents_md.rs (31519549) | https://github.com/openai/codex/blob/31519549/codex-rs/core/src/agents_md.rs | T1 | web_search_exa | Hivatalos forráskód |
| GH issue #36371 (project_doc_max_bytes ellentmondás) | https://github.com/openai/codex/issues/36371 | T1 | web_search_exa | Hivatalos repó issue, doksi-ellentmondás dokumentálása |
| AGENTS.md (learn.chatgpt.com, .md variáns) | https://learn.chatgpt.com/docs/agent-configuration/agents-md.md | T1 | web_search_exa | Hivatalos tükör |
| codex-rs/core/src/agents_md.rs (ac4332c0) | https://github.com/openai/codex/blob/ac4332c05b11e00ae775a24cb762edc05c5b5932/codex-rs/core/src/agents_md.rs | T1 | web_search_exa | Hivatalos forráskód, másik commit — megerősítés |
| The Project Workflow (Serena) | https://oraios.github.io/serena/02-usage/040_workflow.html | T1 | web_search_exa | Hivatalos; activate_project, onboarding |
| Serena clients doc (030_clients.md) | https://github.com/oraios/serena/blob/9cd33aa5/docs/02-usage/030_clients.md | T1 | web_search_exa | Hivatalos; kliens-specifikus aktiválási minták |
| Serena workflow_tools.py | https://github.com/oraios/serena/blob/a0984015/src/serena/tools/workflow_tools.py | T1 | web_search_exa | Hivatalos forráskód; onboarding tool |
| Serena running doc (020_running.md) | https://github.com/oraios/serena/blob/981f560f/docs/02-usage/020_running.md | T1 | web_search_exa | Hivatalos; `--project-from-cwd` |
| Serena project.py (9cd33aa5) | https://github.com/oraios/serena/blob/9cd33aa5/src/serena/project.py | T1 | web_search_exa | Hivatalos forráskód, korábbi MemoriesManager |
| Serena project.py (a0984015) | https://github.com/oraios/serena/blob/a0984015/src/serena/project.py | T1 | web_search_exa | Hivatalos forráskód, frissebb MemoriesManager (`GLOBAL_TOPIC`) |
| oraios/serena README | https://github.com/oraios/serena | T1 | web_search_exa | Hivatalos főrepó |
| Serena agent.py | https://github.com/oraios/serena/blob/a0984015/src/serena/agent.py | T1 | web_search_exa | Hivatalos forráskód; activate_project logika |
| Serena Memories & Onboarding (045_memories.html) | https://oraios.github.io/serena/02-usage/045_memories.html | T1 | web_search_exa | Hivatalos; `global/` prefix teljes magyarázata |
| Serena docs/045_memories.md (GitHub) | https://github.com/oraios/serena/blob/main/docs/02-usage/045_memories.md | T1 | web_search_exa | Hivatalos, ugyanaz forrásból — megerősítés |
| Serena memory_tools.py (a0984015) | https://github.com/oraios/serena/blob/a0984015/src/serena/tools/memory_tools.py | T1 | web_search_exa | Hivatalos forráskód; `write_memory`/`RenameMemoryTool` docstring, „If explicitly instructed” |
| Serena memory_tools.py (0c915bd1) | https://github.com/oraios/serena/blob/0c915bd1/src/serena/tools/memory_tools.py | T1 | web_search_exa | Hivatalos, azonos tartalom más commit — megerősítés |
| Serena project.py (0c915bd1) | https://github.com/oraios/serena/blob/0c915bd1/src/serena/project.py | T1 | web_search_exa | Hivatalos; `_is_global` teljes implementáció |
| cognee MCP Tools Reference | https://docs.cognee.ai/cognee-mcp/mcp-tools | T1 | web_search_exa | Hivatalos; `remember`/`recall`/`forget` séma |
| cognee dataset support commit | https://github.com/topoteretes/cognee/commit/1fb2af18555f064630b5157804a421d805589fea | T1 | web_search_exa | Hivatalos forráskód-commit |
| cognee PR #2459 | https://github.com/topoteretes/cognee/pull/2459 | T1 | web_search_exa | Hivatalos PR, `dataset_name` bevezetése |
| cognee search API | https://docs.cognee.ai/api-reference/search/search | T1 | web_search_exa | Hivatalos API-referencia; `datasets`/`dataset_ids` |
| cognee cognify API | https://docs.cognee.ai/api-reference/cognify/cognify | T1 | web_search_exa | Hivatalos API-referencia |
| cognee-mcp README (raw) | https://raw.githubusercontent.com/topoteretes/cognee/HEAD/cognee-mcp/README.md | T1 | web_search_exa | Hivatalos; „Agent Scoping (per-client default datasets)” kulcsidézet |
| cognee add() Python API | https://docs.cognee.ai/python-api/add | T1 | web_search_exa | Hivatalos; `dataset_name` alapérték |
| cognee add API (mintlify) | https://cognee.mintlify.app/api-reference/add/add | T1 | web_search_exa | Hivatalos tükör — megerősítés |
| Anthropic memory tool docs | https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool | T1 | web_search_exa | Hivatalos; kliens-oldali memória-tool |
| Context editing docs | https://platform.claude.com/docs/en/build-with-claude/context-editing | T1 | web_search_exa | Hivatalos; kapcsolódó funkció |
| Memory & context management cookbook | https://platform.claude.com/cookbook/tool-use-memory-cookbook?2f226f2c_page=2 | T1 | web_search_exa | Hivatalos cookbook |
| Managing context on Claude Developer Platform (blog) | https://claude.com/blog/context-management | T1 | web_search_exa | Hivatalos launch blog |
| Effective context engineering for AI agents | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | T1 | web_search_exa | Hivatalos Anthropic engineering blog |
| anthropic-cookbook memory_cookbook.ipynb | https://github.com/anthropics/anthropic-cookbook/blob/main/tool_use/memory_cookbook.ipynb | T1 | web_search_exa | Hivatalos cookbook forráskód |
| modelcontextprotocol/servers memory README | https://github.com/modelcontextprotocol/servers/blob/main/src/memory/README.md | T1 | web_search_exa | Hivatalos MCP referencia-szerver |
| modelcontextprotocol/servers memory index.ts | https://github.com/modelcontextprotocol/servers/blob/main/src/memory/index.ts | T1 | web_search_exa | Hivatalos forráskód |
| memory README (raw tükör) | https://raw.githubusercontent.com/modelcontextprotocol/servers/main/src/memory/README.md | T1 | web_search_exa | Hivatalos, raw tükör — megerősítés |
| @modelcontextprotocol/server-memory (npm registry) | https://registry.npmjs.org/%40modelcontextprotocol%2Fserver-memory | T1 | web_search_exa | Hivatalos csomag-leírás |
| @modelcontextprotocol/server-memory (npmjs.com) | https://www.npmjs.com/package/@modelcontextprotocol/server-memory | T1 | web_search_exa | Hivatalos, azonos tartalom — megerősítés |
| memory index.ts (d31124c9) | https://github.com/modelcontextprotocol/servers/blob/d31124c9/src/memory/index.ts | T1 | web_search_exa | Hivatalos, másik commit — megerősítés |
| Letta OpenAPI project_id (2. keresés, api-evangelist tükör) | https://raw.githubusercontent.com/api-evangelist/letta/refs/heads/main/openapi/letta-agents-api-openapi.yml | T2 | web_search_exa | Ismételt találat, project_id/X-Project megerősítés |
| Antigravity Projects docs | https://antigravity.google/docs/projects/ | T3 | web_search_exa | Kapcsolódó, de más eszköz (Google Antigravity) — nem Letta; irreleváns találat, nem használtam fel állításhoz |
| modelcontextprotocol memory (egyéb generikus „project” találatok, Hamsa/Evidently/Sippulse/CloudStation/Upsolve) | (több URL, ld. keresési log) | T3 | web_search_exa | Általános „mi az a Projekt” SaaS-dokumentációk, nem memória-MCP-k — csak a keresési zaj dokumentálására, nem használtam fel állításhoz |
| prmichaelsen/remember-mcp | https://github.com/prmichaelsen/remember-mcp/ | T3 | web_search_exa | Nem hivatalos, multi-tenant memória-MCP; csak jelzésértékű, nem idéztem a fő táblázatban |
| FlarelyLegal/memory-mcp | https://github.com/FlarelyLegal/memory-mcp | T3 | web_search_exa | Nem hivatalos; namespace-RBAC minta, egyetlen forrásból |
| opspresso/mcp-memory | https://github.com/opspresso/mcp-memory | T3 | web_search_exa | Nem hivatalos, de erős releváns idézet a fejléc-alapú tenant-döntésről |
| Coordination Memory MCP (Glama, yanqiw) | https://glama.ai/mcp/servers/yanqiw/comem | T3 | web_search_exa | Nem memória-tárolás, hanem multi-agent koordináció — nem releváns, nem idéztem |
| datamcpapp/datamcp-app | https://github.com/datamcpapp/datamcp-app | T3 | web_search_exa | Nem hivatalos, hosztolt memória-MCP projekt-fogalommal — csak jelzésértékű |
| CedraInteractive/Memory-MCP (tükör) | https://github.laiyagushi.com/CedraInteractive/Memory-MCP | T3 | web_search_exa | Nem hivatalos, `project` mező a memory_upsert tool-ban |
| Antony-A-tech/MCP-Team-memory (malinkaboy fork) | https://github.com/malinkaboy/MCP-Team-memory | T3 | web_search_exa | Nem hivatalos; `X-Project-Id` fejléc + `memory_projects` tool |
| arpanroy41/nexmem-mcp | https://github.com/arpanroy41/nexmem-mcp | T3 | web_search_exa | Nem hivatalos; `NEXMEM_TEAM_NAME` env-alapú névtér |
