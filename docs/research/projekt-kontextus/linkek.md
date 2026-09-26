# Linkek — projekt-kontextus

---

# SQ01 — Mit ad az MCP-specifikáció arra, hogy a szerver megtudja a kliens munkakörnyezetét (projektjét)?
## Meglátogatott és felderített linkek
| Cím | URL | Tier | Eszköz | Megjegyzés |
|---|---|---|---|---|
| 2026-07-28 changelog | https://modelcontextprotocol.io/specification/2026-07-28/changelog | T1 | Exa search+fetch | Fő changelog: MRTR, roots/sampling/logging deprecation, stateless mag |
| 2026-07-28 spec index | https://modelcontextprotocol.io/specification/2026-07-28 | T1 | Exa search | Spec-főoldal |
| 2026-07-28 release tag | https://github.com/modelcontextprotocol/modelcontextprotocol/releases/tag/2026-07-28 | T1 | Exa search | Hivatalos release-jegyzet |
| Versioning and Compatibility | https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning | T1 | Exa search | Modern vs. legacy éra, `server/discover`, `UnsupportedProtocolVersionError` |
| Blog: The 2026-07-28 Specification | https://blog.modelcontextprotocol.io/posts/2026-07-28/ | T1 | Exa search | Hivatalos bejelentés, MRTR/deprecation összefoglaló |
| basic/index (_meta, per-request fields) | https://modelcontextprotocol.io/specification/2026-07-28/basic/index | T1 | Exa search | `_meta` kulcsnév-szabályok, kötelező mezők, hibakódok |
| Blog: Release Candidate | https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/ | T1 | Exa search | RC ütemterv, roots/sampling/logging deprecation előzetes |
| Roots (2025-11-25) | https://modelcontextprotocol.io/specification/2025-11-25/client/roots | T1 | Exa search | Korábbi (session-alapú) roots-mechanizmus |
| TS SDK — Provide roots | https://ts.sdk.modelcontextprotocol.io/v2/clients/roots.html | T1 | Exa search | Stateless módban nincs szerver→kliens csatorna, MRTR-beágyazás |
| SEP-2577 (Deprecate Roots, Sampling, Logging) | https://modelcontextprotocol.io/seps/2577-deprecate-roots-sampling-and-logging | T1 | Exa fetch | Teljes SEP-szöveg, indoklás, deprecation-ütemezés |
| schema/2024-11-05/schema.ts | https://github.com/modelcontextprotocol/specification/blob/main/schema/2024-11-05/schema.ts | T1 | Exa search | Eredeti `Root`/`ListRootsRequest` definíció |
| Roots (draft, mintlify tükör) | https://mcp.mintlify.app/specification/draft/client/roots | T2 | Exa search | MRTR `roots/list` szekvenciapélda (nem hivatalos domain, de a tartalom a hivatalos draft szövege) |
| C# SDK — Roots | https://csharp.sdk.modelcontextprotocol.io/v2/concepts/roots/roots.html | T1 | Exa search | `RequestRootsAsync` stateless-kivétel, `InputRequiredException` |
| Python SDK — Sampling and roots | https://py.sdk.modelcontextprotocol.io/handlers/sampling-and-roots/index.md | T1 | Exa search | `-32021` hibakód képesség hiányában |
| Go SDK — MCP Client (Roots) | https://go.sdk.modelcontextprotocol.io/client/ | T1 | Exa search | MRTR middleware, `clientMultiRoundTripMiddleware` |
| Elicitation (2026-07-28) | https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation | T1 | Exa fetch | Teljes elicitation-szöveg: mód, séma, biztonsági korlátok |
| Transports — Overview (2026-07-28) | https://modelcontextprotocol.io/specification/2026-07-28/basic/transports | T1 | Exa fetch | Body a forrás igazság, header-tükrözés elve |
| Authorization (2026-07-28) | https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization | T1 | Exa search | `resource` paraméter, scope-stratégia, scope-hierarchia |
| RFC 8707 (rfc-editor) | https://www.rfc-editor.org/rfc/rfc8707.html | T1 | Exa search | Resource Indicators, scope vs. resource megkülönböztetés |
| RFC 8707 (datatracker) | https://datatracker.ietf.org/doc/html/rfc8707/ | T1 | Exa search | Ua., másodlagos IETF-tükör megerősítésként |
| Authorization (draft, modelcontextprotocol.info tükör) | https://modelcontextprotocol.info/specification/draft/basic/authorization/ | T2 | Exa search | Kanonikus URI valid/invalid példák (nem hivatalos domain) |
| Issue #1597 (HTTP REST Transport SEP-javaslat) | https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1597 | T1 (hivatalos repo, el nem fogadott javaslat) | Exa search | Multi-tenant elkülönítési probléma, elnapolva |
| Registry PR #570 (RemoteTransport tenant_id) | https://github.com/modelcontextprotocol/registry/pull/570 | T1 (hivatalos repo, elfogadott PR) | Exa search | Regisztry-szintű tenant-URL-sablonozás |
| Discussion #234 (Multi-user Authorization) | https://github.com/modelcontextprotocol/modelcontextprotocol/discussions/234 | T1 (hivatalos repo, közösségi vita) | Exa search | Per-felhasználó `_meta.authorization` javaslat, nem Final SEP |
| PR #2202 (SEP-2202, non-file roots, szüneteltetve) | https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2202 | T1 (hivatalos repo, félbehagyott javaslat) | Exa search | Miért nem lazult a `file://` megkötés |
| SEP-2243 (HTTP Standardization) | https://modelcontextprotocol.io/seps/2243-http-standardization | T1 | Exa search | `Mcp-Method`/`Mcp-Name`/`x-mcp-header`/`Mcp-Param-*` |
| TS SDK issue #2190 (SEP-2243 implementáció) | https://github.com/modelcontextprotocol/typescript-sdk/issues/2190 | T1 (hivatalos repo issue) | Exa search | Biztonsági megjegyzés: `Mcp-Param-*` nem authorizációra való |
| Clients — feature support matrix | https://github.com/modelcontextprotocol/docs/blob/573dc60c/clients.mdx | T1 | Exa search | Hivatalos, de Elicitation oszlop nélküli mátrix (l. Ellentmondások) |
| apify/mcp-client-capabilities | https://github.com/apify/mcp-client-capabilities | T2/T3 | Exa search | Közösségi kliens-képesség adatbázis, Elicitation oszlopokkal |
| Understanding MCP clients (2026-07-28 learn docs) | https://modelcontextprotocol.io/docs/2026-07-28/learn/client-concepts | T1 | Exa search | Roots/Sampling deprecation összefoglalása felhasználói nyelven |
| EMA extension spec | https://modelcontextprotocol.io/extensions/auth/enterprise-managed-authorization.md | T1 | Exa search | Enterprise-Managed Authorization: szervezeti, nem projekt-szintű |
| ext-auth overview | https://modelcontextprotocol.io/extensions/auth/overview.md | T1 | Exa search | Mikor melyik auth-kiterjesztés ajánlott |
| Blog: Enterprise-Managed Authorization | https://blog.modelcontextprotocol.io/posts/enterprise-managed-auth/ | T1 | Exa search | EMA stabillá válásának bejelentése |
| ext-auth PR #4 (SEP-646/990) | https://github.com/modelcontextprotocol/ext-auth/pull/4 | T1 (hivatalos repo) | Exa search | EMA eredeti javaslata, folyamábra |
| SEP-2567 (Sessionless MCP) | https://modelcontextprotocol.org/seps/2567-sessionless-mcp | T1 | Exa fetch | Explicit state handle mint „tool-design pattern", Final SEP |
| Discussion #609 (Authorization and Multitenancy) | https://github.com/modelcontextprotocol/modelcontextprotocol/discussions/609 | T1 (hivatalos repo, közösségi vita) | Exa search | Nincs tiszta válasz, reverse-proxy workaround |
| Tutorial: Authorization (Keycloak példa) | https://modelcontextprotocol.io/docs/tutorials/security/authorization | T1 | Exa search | `mcp:tools` scope-példa, nem projekt-szintű |
| PR #835 (SEP-835, scope selection strategy) | https://github.com/modelcontextprotocol/modelcontextprotocol/pull/835 | T1 (hivatalos repo) | Exa search | Scope-választási prioritás, step-up authorization |
| SEP-2207 (offline_access guidance) | https://modelcontextprotocol.io/seps/2207-oidc-refresh-token-guidance.md | T1 | Exa search | Tangenciális: scope ≠ resource-jellegű megkülönböztetés megerősítése |
| Issue #1292 (Namespaces using URIs, SEP-javaslat) | https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1292 | T1 (hivatalos repo, Proposal státusz) | Exa search | Tool/resource-névütközés, nem client-projekt-kontextus |
| Architecture (draft) | https://modelcontextprotocol.io/specification/draft/architecture | T1 | Exa search | Client-host-server modell, kérésenkénti capability-negotiation |
| schema/2026-07-28/schema.ts | https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/schema/2026-07-28/schema.ts | T1 | Exa search | `RequestMetaObject`, `_meta` mezők pontos TS-típusai |

---

# SQ02 — Hogyan döntik el a meglévő memória-rendszerek, hová kerül egy új emlék, és honnan tudják a projektet?
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

---

# SQ03 — Hogyan tudja egy kliens átadni a projektet egy távoli MCP-szervernek, és mit adnak a munkamenet-indító hookok?
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

---

# SQ04 — Ki döntse el, hogy egy emlék személyes, projekt- vagy közös — és mi megy félre, ha rosszul dől el?
## Meglátogatott és felderített linkek
| Cím | URL | Tier | Eszköz | Megjegyzés |
|---|---|---|---|---|
| update() lets caller metadata silently overwrite user_id/agent_id/run_id (mem0 #6277) | https://github.com/mem0ai/mem0/issues/6277 | T1 | Exa fetch | P0-critical, Python SDK, javítva PR #6278 |
| update() metadata overwrite TS SDK (mem0 #6342) | https://github.com/mem0ai/mem0/issues/6342 | T1 | Exa search | TS testvérhiba |
| fix(ts-oss) PR (mem0 #6343) | https://github.com/mem0ai/mem0/pull/6343 | T1 | Exa search | javítás részletei, camelCase alias rés is |
| fix(memory) PR (mem0 #6278) | https://github.com/mem0ai/mem0/pull/6278 | T1 | Exa search | Python javítás, injection-eset is |
| add() lets metadata set identity scope on creation (mem0 #6655) | https://github.com/mem0ai/mem0/issues/6655 | T1 | Exa search | creation-time hatókör-injektálás |
| add() mutates caller's filters object (mem0 #6796) | https://github.com/mem0ai/mem0/issues/6796 | T1 | Exa search | 10/10 repró, scope guard megkerülve |
| addMemory metadata excluded from retrieval/partitioning (mem0 #5121) | https://github.com/mem0ai/mem0/issues/5121 | T1 | Exa search | multi-app_id keveredés |
| Cross-scope entity linking (mem0 #5439) | https://github.com/mem0ai/mem0/issues/5439 | T1 | Exa search | entitás-boost cross-scope szivárgás |
| Cross-scope entity linking TS (mem0 #5597) | https://github.com/mem0ai/mem0/issues/5597 | T1 | Exa search | TS testvérhiba |
| TealTiger governance layer proposal (mem0 #5507) | https://github.com/mem0ai/mem0/issues/5507 | T1 | Exa search | elutasítva core-ba, cookbook javasolva |
| mem0 group chat wrong user_id (hermes-agent #64340) | https://github.com/NousResearch/hermes-agent/issues/64340 | T2 | Exa search | cache-alapú attribúciós hiba, provider-generic |
| Memory identity from filesystem path (Claude Code #41283) | https://github.com/anthropics/claude-code/issues/41283 | T1 | Exa fetch | worktree/rename orphaning, human-vs-project gap |
| Claude ignores CLAUDE.md scope rules (Claude Code #40541) | https://github.com/anthropics/claude-code/issues/40541 | T1 | Exa search | modell ismétlődő hatókör-hiba, hook-alapú javaslat |
| auto-memory resolver walks to ancestor (Claude Code #53734) | https://github.com/anthropics/claude-code/issues/53734 | T1 | Exa search | 8 dokumentált cross-agent contamination incidens |
| System prompt memory instructions wrong path (Claude Code #36973) | https://github.com/anthropics/claude-code/issues/36973 | T1 | Exa search | dokumentáció/kód eltérés |
| Memory saved to undocumented MEMORY.md (Claude Code #23341) | https://github.com/anthropics/claude-code/issues/23341 | T1 | Exa search | opt-out only, nincs jóváhagyás |
| MEMORY.md not loaded into system prompt (Claude Code #25318) | https://github.com/anthropics/claude-code/issues/25318 | T1 | Exa search | |
| Memory traversal should respect worktree boundaries (Claude Code #16600) | https://github.com/anthropics/claude-code/issues/16600 | T1 | Exa search | EnterWorktree tool okozta ős-betöltés |
| Duplicate memory files on Windows (Claude Code #19516) | https://github.com/anthropics/claude-code/issues/19516 | T1 | Exa search | drive-letter case bug, javítva 2.1.47 |
| CLAUDE_CONFIG_DIR not honored by rules auto-attachment (Claude Code #79233) | https://github.com/anthropics/claude-code/issues/79233 | T1 | Exa search | profil-izoláció megkerülése |
| Feature request user-level scope (Claude Code #83831) | https://github.com/anthropics/claude-code/issues/83831 | T1 | Exa search | workaround: autoMemoryDirectory, all-or-nothing |
| Docs omit autoMemoryDirectory (Claude Code #33709) | https://github.com/anthropics/claude-code/issues/33709 | T1 | Exa search | dokumentáció utólag javítva |
| Warn when auto-memory starts empty (Claude Code #68368) | https://github.com/anthropics/claude-code/issues/68368 | T1 | Exa search | fragmentáció-detekció hiánya |
| How Claude remembers your project (hivatalos dokumentáció) | https://code.claude.com/docs/en/memory | T1 | Exa search | „Claude treats them as context, not enforced configuration” |
| Reset all projects memory (Cursor fórum) | https://forum.cursor.com/t/reset-all-projects-memory/137390 | T3 | Exa search | felhasználói panasz, projektek közti szivárgás |
| Rules vs. Memories and Global vs. Project (Cursor fórum) | https://forum.cursor.com/t/rules-vs-memories-and-global-vs-project/137149 | T3 | Exa search | tartalom jóváhagyva, hatókör mégis rossz |
| Cursor/Claude Code leak deleted issue context (Multica #6656) | https://github.com/multica-ai/multica/issues/6656 | T2 | Exa search | local_directory resource a valódi rés |
| Isolation guarantees (Letta, The Neural Base) | https://theneuralbase.com/letta/learn/intermediate/isolation-guarantees/ | T2 | Exa search | agent_id mint elsődleges izolációs kulcs |
| Cross-Session State Leakage (Letta #3388) | https://github.com/letta-ai/letta/issues/3388 | T1 | Exa search | daemon-szintű persona-mérgezés, javasolt ephemeral-memory fix |
| Hacker plants false memories in ChatGPT (Ars Technica) | https://arstechnica.com/security/2024/09/false-memories-planted-in-chatgpt-give-hacker-persistent-exfiltration-channel/ | T2 | Exa search | Rehberger kutatása, indirekt prompt injection a memóriába |
| ChatGPT bug exposed private data (Mashable) | https://mashable.com/article/openai-chatgpt-bug-exposed-user-data-privacy-breach | T2 | Exa search | 2023 márciusi outage, OpenAI hivatalos elismerése |
| ChatGPT users see random people's chat histories (Vice) | https://www.vice.com/en/article/chatgpt-users-report-being-able-to-see-random-peoples-chat-histories/ | T2 | Exa search | Sam Altman idézett elismerése |
| ChatGPT user alarmed AI shares others' info (NY Post) | https://nypost.com/2025/06/10/tech/chatgpt-user-alarmed-as-ai-tool-shares-others-private-info/ | T3 | Exa search | megerősítetlen felhasználói panasz |
| The Shared Clipboard Inside the Sandbox (Check Point / Cybernoz) | https://cybernoz.com/the-shared-clipboard-inside-the-sandbox-cross-account-data-leakage-in-chatgpt/ | T2 | Exa search | cross-account covert channel, 2026 |
| Memory and new controls for ChatGPT (OpenAI hivatalos) | https://openai.com/index/memory-and-new-controls-for-chatgpt/ | T1 | Exa search | „Memory updated” utólagos értesítés, nem előzetes jóváhagyás |
| ChatGPT memory guide (OpenAI Help Center) | https://help.openai.com/en/articles/6825453-chatgpt-memory-a-guide | T1 | Exa search | memory summary, temporary chat |
| OWASP Top 10 for LLM Applications 2025 (PDF) | https://genai.owasp.org/download/43299/ | T1 | Exa search | LLM02, LLM06 teljes szöveg |
| LLM06:2025 Excessive Agency (OWASP GenAI) | https://genai.owasp.org/llmrisk/llm06-sensitive-information-disclosure/ | T1 | Exa search | complete mediation, execute in user's context |
| LLM06 ExcessiveAgency (owasp.org wiki) | https://owasp.org/www-project-top-10-for-large-language-model-applications/2_0_vulns/LLM06_ExcessiveAgency | T1 | Exa search | azonos tartalom, elsődleges wiki |
| MCP10-2025 Context Injection & Over-Sharing (OWASP MCP Top 10) | https://github.com/OWASP/www-project-mcp-top-10/blob/master/2025/MCP10-2025%E2%80%93ContextInjection%26OverSharing.md | T1 | Exa search | közvetlen válasz a kutatási kérdésre |
| OWASP Top 10 for Agentic Applications 2026 (PDF) | https://genai.owasp.org/download/52117 | T1 | Exa search | ASI03, ASI06, memory-based privilege retention |
| AISVS C08-02 Embedding Sanitization/Validation | https://github.com/OWASP/AISVS/blob/main/research/chapters/C08-Memory-and-Embeddings/C08-02-Embedding-Sanitization-Validation.md | T1 | Exa search | write-authorization control 8.2.4, sleeper memory poisoning idézetek |
| Memory Is a Feature. It Is Also an Attack Surface (OWASP GenAI blog, Cisco) | https://genai.owasp.org/2026/05/13/memory-is-a-feature-it-is-also-an-attack-surface/ | T1 | Exa search | MemoryTrap, Anthropic Claude Code 2.1.50 javítás |
| OWASP Agent Memory Guard | https://owasp.org/www-project-agent-memory-guard/ | T1 | Exa search | policy-alapú memory read/write interception |
| Security Best Practices (MCP hivatalos) | https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices | T1 | Exa search | scope minimization, progressive least-privilege |
| Authorization spec (MCP hivatalos, 2026-07-28) | https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization | T1 | Exa search | scope selection strategy, step-up authorization |
| Secure shared multi-tenant agent memory namespaces (AWS builder) | https://builder.aws.com/content/3C1SCSoe15VaBnmsiMIfGcZfhxM/secure-shared-multi-tenant-agent-memory-namespaces-using-agentcore-memory | T2 | Exa search | ABAC, actorId = tenantId:agentId:userId, IdP mint trusted source |
| AWS Well-Architected Agentic AI Lens — human review | https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentsec04-bp02.html | T1 | Exa search | deterministic policy engine vs. LLM classifier |
| CIMemories paper (ICLR 2026 proceedings PDF) | https://proceedings.iclr.cc/paper_files/paper/2026/file/9a2bcfaf383638e166162a25b6dff125-Paper-Conference.pdf | T1 | Exa fetch | 69% violation, GPT-5 instabilitás, lektorált cikk |
| CIMemories repo (Meta FAIR / facebookresearch) | https://github.com/facebookresearch/CIMemories | T1 | Exa fetch | kód és adatkészlet, azonos számok megerősítve |
| AI Agent Memory Governance (mem0 blog) | https://mem0.ai/blog/ai-agent-memory-governance-meaning-best-practices-for-secure-memory | T2 | Exa search | identity-based scoping, consent/provenance metaadat |
| Add Memory / memory-types / entity-scoped-memory (mem0 hivatalos docs) | https://docs.mem0.ai/core-concepts/memory-operations/add , https://docs.mem0.ai/core-concepts/memory-types , https://docs.mem0.ai/platform/features/entity-scoped-memory | T1 | Exa search | user_id/agent_id/app_id/run_id rétegek, explicit paraméterezés |
| Controlling memory ingestion (mem0 cookbook) | https://mem0.mintlify.app/cookbooks/essentials/controlling-memory-ingestion | T1 | Exa search | custom_instructions szűrés, nem interaktív jóváhagyás |
| mem0 dream skill (SKILL.md) | https://github.com/mem0ai/mem0/blob/b357a5a1b03c299ec8229c268e63cfac0f7c6566/integrations/mem0-plugin/skills/dream/SKILL.md | T1 | Exa search | diff-alapú jóváhagyás, de csak konszolidációnál |
| Context engineering for AI agents — routing to memory (mem0 blog) | https://mem0.ai/blog/context-engineering-for-ai-agents-how-to-route-queries-to-memory | T2 | Exa search | „explicit and observable” routing elve |
| RoguePilot: Exploiting GitHub Copilot (Orca Security) | https://orca.security/resources/blog/roguepilot-github-copilot-vulnerability/ | T2 | Exa search | Codespaces prompt injection lánc |
| GitHub Issues Abused in Copilot Attack (SecurityWeek) | https://www.securityweek.com/github-issues-abused-in-copilot-attack-leading-to-repository-takeover/ | T2 | Exa search | RoguePilot megerősítése |
| GitHub Copilot prompt injection leaked private repo data (CSO Online) | https://www.csoonline.com/article/4069887/github-copilot-prompt-injection-flaw-leaked-sensitive-data-from-private-repos.html | T2 | Exa search | Camo-bypass adatszivárgás |
| Add repository custom instructions (GitHub hivatalos docs) | https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions | T1 | Exa search | „all sets of relevant instructions are provided” |

---

# ELL01 — Az MCP-specifikáció és a kliensek állításainak ellenőrzése
## Meglátogatott linkek
| Cím | URL | Tier | Eszköz |
|---|---|---|---|
| SEP-2577 (raw markdown) | https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/seps/2577-deprecate-roots-sampling-and-logging.md | T1 | Exa search |
| SEP-2577 (hivatalos oldal) | https://modelcontextprotocol.io/seps/2577-deprecate-roots-sampling-and-logging | T1 | Exa search |
| SEP-2577 (archív .org tükör) | https://modelcontextprotocol.org/seps/2577-deprecate-roots-sampling-and-logging | T1 | Exa search |
| SEP-lista | https://modelcontextprotocol.io/seps | T1 | Exa search |
| SEP-2577 PR (merged, final) | https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2577 | T1 | Exa search |
| SEP-2567 (raw markdown) | https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/seps/2567-sessionless-mcp.md | T1 | Exa search |
| SEP-2567 (archív .org tükör) | https://modelcontextprotocol.org/seps/2567-sessionless-mcp | T1 | Exa search |
| SEP-2567 (hivatalos oldal) | https://modelcontextprotocol.io/seps/2567-sessionless-mcp | T1 | Exa search |
| SEP-2567 draft-vita | https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2567 | T1 | Exa search |
| 2026-07-28 changelog | https://modelcontextprotocol.io/specification/2026-07-28/changelog | T1 | Exa search |
| MRTR-oldal | https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/mrtr | T1 | Exa search |
| Elicitation (2026-07-28) | https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation | T1 | Exa fetch |
| Authorization (2026-07-28) | https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization | T1 | Exa fetch+search |
| RFC 8707 (rfc-editor) | https://www.rfc-editor.org/rfc/rfc8707.html | T1 | Exa search |
| RFC 8707 (datatracker, másodlagos tükör) | https://datatracker.ietf.org/doc/html/rfc8707/ | T1 | Exa search |
| Claude Code MCP doksi | https://code.claude.com/docs/en/mcp | T1 | Exa search |
| Claude Code header-forwarding bug | https://github.com/anthropics/claude-code/issues/28293 | T1 | Exa search |
| Claude Code mcp-quickstart | https://code.claude.com/docs/en/mcp-quickstart | T1 | Exa search |
| Codex mcp_connection_manager.rs (85034b18) | https://github.com/openai/codex/blob/85034b18/codex-rs/core/src/mcp_connection_manager.rs | T1 | Exa search |
| Codex mcp_connection_manager.rs (korai, rust-v0.0.2505302325) | https://github.com/openai/codex/blob/rust-v0.0.2505302325/codex-rs/core/src/mcp_connection_manager.rs | T1 | Exa search |
| Codex mcp_connection_manager.rs (9a8730f3) | https://github.com/openai/codex/blob/9a8730f3/codex-rs/core/src/mcp_connection_manager.rs | T1 | Exa search |
| Cursor fórum — roots/list -32601 | https://forum.cursor.com/t/mcp-client-does-not-support-roots-list/77248 | T2 | Exa search |
| twine-mcp issue #3 — Cursor roots bug, független megerősítés | https://github.com/Unveil-gg/twine-mcp/issues/3 | T2 | Exa search |
| microsoft/copilot-intellij-feedback #438 — analóg roots-hiba más kliensnél | https://github.com/microsoft/copilot-intellij-feedback/issues/438 | T1 (hivatalos MS repo) | Exa search |
| Codex Hooks (fejlesztői doksi) | https://developers.openai.com/codex/hooks | T1 | Exa search |
| Codex Hooks (learn.chatgpt.com tükör) | https://learn.chatgpt.com/docs/hooks | T1 | Exa search |
| Codex issue #22861 — 2500 token limit éles jelentés | https://github.com/openai/codex/issues/22861 | T1 | Exa search |
| Codex session_start.rs forráskód | https://github.com/openai/codex/blob/main/codex-rs/hooks/src/events/session_start.rs | T1 | Exa search |
| Claude Code issue #50571 — 10 000 karakteres küszöb magyarázata | https://github.com/anthropics/claude-code/issues/50571 | T1 | Exa search |
| Claude Code issue #84021 — ~2000 karakteres tényleges preview mérés | https://github.com/anthropics/claude-code/issues/84021 | T1 | Exa search |
| Claude Code issue #44086 — 2000 karakteres csonkítás | https://github.com/anthropics/claude-code/issues/44086 | T1 | Exa search |
| Claude Code issue #51537 — 50K vs 10K doksi/kód eltérés | https://github.com/anthropics/claude-code/issues/51537 | T1 | Exa search |
| Antigravity Hooks (docs/hooks/) | https://antigravity.google/docs/hooks/ | T1 | Exa search |
| Antigravity Hooks (docs/ide/hooks/) | https://antigravity.google/docs/ide/hooks/ | T1 | Exa search |
| atrium-adapters — Antigravity hook-viselkedés, „AG never fires SessionStart” | https://github.com/jonnyasmar/atrium-adapters/blob/main/adapters/antigravity/hooks.sh | T3 | Exa search |
| GitHub Copilot hooks reference — HTTP hook típus | https://docs.github.com/en/copilot/reference/hooks-reference | T1 | Exa search |
| multica-ai/multica issue #3908 — Cursor mcp-auth.json workspace-tárolás | https://github.com/multica-ai/multica/issues/3908 | T2 | Exa search |
| Cursor MCP doksi (static OAuth, projekt config) | https://cursor.com/docs/mcp | T1 | Exa search |
| Claude Code issue #39952 — OAuth kulcs = szervernév, globális | https://github.com/anthropics/claude-code/issues/39952 | T1 | Exa search |
| Claude Code issue #18890 — worktree-k szerinti hash | https://github.com/anthropics/claude-code/issues/18890 | T1 | Exa search |
| Claude Code issue #69749 — súlyosabb biztonsági szivárgás | https://github.com/anthropics/claude-code/issues/69749 | T1 | Exa search |
| Antigravity CLI MCP doksi | https://antigravity.google/docs/cli/mcp/ | T1 | Exa search |
| Antigravity gcli-migration doksi | https://antigravity.google/docs/cli/gcli-migration/ | T1 | Exa search |
| VS Code — Add and manage MCP servers | https://code.visualstudio.com/docs/agent-customization/mcp-servers | T1 | Exa search |
| VS Code — MCP configuration reference | https://code.visualstudio.com/docs/agents/reference/mcp-configuration | T1 | Exa search |
| connector.zone — MCP config merge (nem hivatalos precedencia-állítás) | https://connector.zone/guides/merging-mcp-config-blocks/ | T3 | Exa search |
| microsoft/vscode issue #332072 — user profil felülírta a workspace-et | https://github.com/microsoft/vscode/issues/332072 | T1 (hivatalos MS repo) | Exa search |
| Claude Code issue #48857 — hivatalos scope-precedencia szövege idézve | https://github.com/anthropics/claude-code/issues/48857 | T1 | Exa search |

---

# ELL02 — A memória-rendszerek hatókör-kezelésének ellenőrzése
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

---

# ELL03 — Hibajegyek a memória-hatókör kezeléséről: léteznek-e, és mit mondanak?
## Meglátogatott linkek
| Cím | URL | Tier | Eszköz |
|---|---|---|---|
| update() lets caller metadata silently overwrite user_id/agent_id/run_id (mem0 #6277) | https://github.com/mem0ai/mem0/issues/6277 | T1 | Exa fetch |
| fix(memory): don't let update() metadata overwrite… (mem0 PR #6278) | https://github.com/mem0ai/mem0/pull/6278 | T1 | Exa fetch/search |
| update() metadata overwrite TS SDK (mem0 #6342) | https://github.com/mem0ai/mem0/issues/6342 | T1 | Exa fetch |
| fix(ts-oss): don't let update() metadata overwrite… (mem0 PR #6343) | https://github.com/mem0ai/mem0/pull/6343 | T1 | Exa fetch/search |
| Python OSS SDK: add() lets metadata set identity scope (mem0 #6655) | https://github.com/mem0ai/mem0/issues/6655 | T1 | Exa fetch |
| add() mutates the caller's filters object (mem0 #6796, NYITOTT) | https://github.com/mem0ai/mem0/issues/6796 | T1 | Exa fetch |
| fix(ts-oss): stop add() from mutating the caller's filters object (mem0 PR #6797, NYITOTT) | https://github.com/mem0ai/mem0/pull/6797 | T1 | Exa fetch |
| mem0ai Python SDK v2.0.13 release notes | https://github.com/mem0ai/mem0/releases/tag/v2.0.13 | T1 | Exa fetch |
| mem0ai Python SDK v2.0.16 release notes | https://github.com/mem0ai/mem0/releases/tag/v2.0.16 | T1 | Exa fetch |
| mem0 Node SDK v3.1.1 release notes | https://github.com/mem0ai/mem0/releases/tag/ts-v3.1.1 | T1 | Exa search |
| mem0ai npm registry (verziólista, független megerősítés) | https://registry.npmjs.org/mem0ai | T1 | Exa search |
| mem0ai PyPI verziólista (ReversingLabs, független megerősítés) | https://secure.software/pypi/packages/mem0ai/versions | T2 | Exa search |
| SDK & Tools changelog (mem0 hivatalos) | https://docs.mem0.ai/changelog/sdk | T1 | Exa fetch |
| Memory identity derived from filesystem path (Claude Code #41283) | https://github.com/anthropics/claude-code/issues/41283 | T1 | Exa fetch |
| auto-memory resolver walks up to ancestor (Claude Code #53734) | https://github.com/anthropics/claude-code/issues/53734 | T1 | Exa fetch |
| Auto memory system prompt path vs. /memory mismatch (Claude Code #52772, #53734 „duplikátuma") | https://github.com/anthropics/claude-code/issues/52772 | T1 | Exa fetch |
| Re-filing #53734/#52772, closed working-as-documented (Claude Code #86945) | https://github.com/anthropics/claude-code/issues/86945 | T1 | Exa fetch |
| Claude repeatedly ignores CLAUDE.md scope rules (Claude Code #40541) | https://github.com/anthropics/claude-code/issues/40541 | T1 | Exa fetch |
| Bug reports leak private org info, unrelated topic (Claude Code #29121) | https://github.com/anthropics/claude-code/issues/29121 | T1 | Exa fetch |
| Unauthorized external bug filing, unrelated topic (Claude Code #37961) | https://github.com/anthropics/claude-code/issues/37961 | T1 | Exa fetch |
| Fails to follow process rules (PM writes code), closest de nem azonos topik (Claude Code #40425) | https://github.com/anthropics/claude-code/issues/40425 | T1 | Exa fetch |
| Duplicate-bot mismatches real bugs — meta-probléma (Claude Code #19267) | https://github.com/anthropics/claude-code/issues/19267 | T1 | Exa search |

---

# SQ05 — Mit adnak be a memória-eszközök a munkamenet elején — tartalom, forma, méret?
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

---

# SQ06 — Mitől használja egy agent ténylegesen a memória-eszközöket?
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

---

# SQ07 — Használják-e az agentek önként a memória-eszközt? A bizonyítékok
## Meglátogatott és felderített linkek
| Cím | URL | Tier | Eszköz | Megjegyzés |
|---|---|---|---|---|
| Delivery, Not Storage (Saha, absztrakt) | https://arxiv.org/abs/2607.20972 | T2 | Exa fetch | Fő elsődleges forrás, §1–§8 teljes egészében lehívva |
| Delivery, Not Storage (PDF) | https://arxiv.org/pdf/2607.20972 | T2 | Exa fetch | |
| Delivery, Not Storage (teljes HTML, §1–§8 + hivatkozások) | https://arxiv.org/html/2607.20972v1 | T2 | Exa fetch | Minden szó szerinti idézet innen |
| Vectr repó — a cikk markdown-változata és kódja | https://github.com/swapnanil/vectr/blob/main/research/brain-memory/delivery-not-storage.md | T2 | Exa search | Megerősíti a kód/adat elérhetőségét; a nyers futásadatokat nem futtattam le |
| Delivery, Not Storage — Hugging Face Papers | https://huggingface.co/papers/2607.20972 | T3 | Exa search | Aggregátor, érdemi vita nem található |
| Codex Knowledge Base — Daniel Vaughan blogja a Saha-cikkről | https://codex.danielvaughan.com/2026/07/28/cue-anchored-working-memory-harness-property-coding-agents-codex-cli-compaction-decay-deterministic-injection/ | T3 | Exa search | Másodlagos összefoglaló, nem kritikai |
| MEMTRACK (absztrakt + RQ1–RQ3) | https://arxiv.org/abs/2510.01353 | T1/T2 | Exa fetch | Független szerzők, más feladatkör, megerősíti a mintázatot |
| MEMTRACK (OpenReview PDF) | https://openreview.net/pdf?id=mVxmbMng4B | T1 | Exa search | |
| MEMTRACK — NeurIPS 2025 diák | https://neurips.cc/media/neurips-2025/Slides/124523.pdf | T1 | Exa search | Konferencia-prezentáció léte megerősítve |
| MEMTRACK — Patronus AI blog | https://www.patronus.ai/blog/memtrack | T3 | Exa search | Gyártói/szerzői blog, ugyanazok a szerzők |
| TriggerBench (absztrakt + Related Works) | https://arxiv.org/abs/2606.23459 | T1/T2 | Exa fetch | Microsoft Research társszerzőség |
| Memory tool — Claude Docs (élő oldal, 2026-09-25) | https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool | T1 | Exa fetch | „automatically checks its memory directory" |
| Building an agentic memory system for GitHub Copilot | https://github.blog/ai-and-ml/github-copilot/building-an-agentic-memory-system-for-github-copilot/ | T1 | Exa search | Hivatalos gyártói blog, 2026-01-15 |
| About GitHub Copilot Memory | https://docs.github.com/en/copilot/concepts/agents/copilot-memory | T1 | Exa search | Hivatalos dokumentáció |
| VS Code Copilot memory dokumentáció | https://github.com/microsoft/vscode-docs/blob/538f9c60/docs/agents/memory.md | T1 | Exa search | Helyi memory tool vs. Copilot Memory összevetése |
| memoryInstructions injektálási hiba (VS Code) | https://github.com/microsoft/vscode/issues/321833 | T2 | Exa search | Mutatja, hogy a gyártó rendszerprompt-szintű kényszerítést használ |
| alioshr/memory-bank-mcp #24 | https://github.com/alioshr/memory-bank-mcp/issues/24 | T2 | Exa fetch | Karbantartói megerősítés: „LLMs are non deterministic" |
| doobidoo/mcp-memory-service #14 | https://github.com/doobidoo/mcp-memory-service/issues/14 | T2 | Exa fetch | Karbantartó külön eszközt épített a probléma megkerülésére |
| doobidoo/mcp-memory-service README (v6.13.0) | https://github.com/doobidoo/mcp-memory-service/blob/fd0bcca.../README.md | T3 | Exa search | Termékleírás, nem független mérés |
| mem0ai/mem0 #5413 | https://github.com/mem0ai/mem0/issues/5413 | T2 | Exa fetch | „Static instruction files... do not provide automatic memory retrieval" |
| Cursor fórum — „A connected memory server can still do nothing" | https://forum.cursor.com/t/a-connected-memory-server-can-still-do-nothing-in-cursor/171402 | T3 | Exa search | |
| Cursor fórum — „My AI doesnt like MCP and use its own" | https://forum.cursor.com/t/my-ai-doesnt-like-mcp-and-use-its-own-lol-issue/79201 | T3 | Exa search | Hallucinált „belső MCP memória" jelenség |
| Cursor fórum — „Tool update_memory not found” | https://forum.cursor.com/t/tool-update-memory-not-found/132487 | T3 | Exa search | |
| Cursor fórum — „Cursor memory doesnt longer work” | https://forum.cursor.com/t/cursor-memory-doesnt-longer-work/136128 | T3 | Exa search | |
| Cursor fórum — „Agents have lost access to memory capability” | https://forum.cursor.com/t/agents-have-lost-access-to-memory-capability/143310 | T3 | Exa search | Cursor-alkalmazott elismeri: „known recurring issue" |
| ClaudioDrews/ground-truth-gap | https://github.com/ClaudioDrews/ground-truth-gap | T3 | Exa fetch | Egyszerzős gyakorlati beszámoló, hat hónap, két keretrendszer |
| anand-92/gemdex README | (Exa-keresési kivonat, „nikships/gemdex") | T3 | Exa search | „Agents won't reach for a new MCP tool on their own." |
| MarceloCaporale/codex-agent-mem README | https://github.com/MarceloCaporale/codex-agent-mem | T3 | Exa search | Ellenőrizetlen marketingállítás a proaktív használatról |
| openai/codex #19663 | https://github.com/openai/codex/issues/19663 | T2 | Exa search | Tangenciális: beépített memória blokkolja a memória-MCP hívásokat |
| kenhuangus/agent-memory-harness — Codex fejezet | https://github.com/kenhuangus/agent-memory-harness/blob/main/docs/harnesses/03-codex.md | T3 | Exa search | Codex architektúra: nincs push-injektálás, csak model-pulled retrieval |

---

# SQ08 — Automatikus beadás kérdésenként: mechanika, költség, mérések
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

---

# ELL04 — Mit adnak be a memória-eszközök a munkamenet elején: az állítások ellenőrzése
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

---

# ELL05 — Az eszközhasználati és kontextus-mérések ellenőrzése
## Meglátogatott linkek
| Cím | URL | Tier | Eszköz |
|---|---|---|---|
| LLM Agents Already Know When to Call Tools (WHEN2TOOL) | https://arxiv.org/pdf/2605.09252v2 | T1 | Exa fetch |
| LLM Agents Already Know When to Call Tools (abs) | https://arxiv.org/abs/2605.09252 | T1 | Exa fetch |
| Tunable Tool-Call Rates via Representation Steering | https://arxiv.org/html/2608.25198v1 | T1 | Exa fetch |
| Tunable Tool-Call Rates via Representation Steering (abs) | https://arxiv.org/abs/2608.25198 | T1 | Exa fetch |
| ToolFailBench (ar5iv) | https://ar5iv.labs.arxiv.org/html/2607.04686 | T2 | Exa fetch |
| ToolFailBench (abs) | https://arxiv.org/abs/2607.04686 | T2 | Exa fetch |
| Codex Desktop stale memory overrides AGENTS.md — issue #39223 | https://github.com/openai/codex/issues/39223 | T2 | Exa fetch |
| Managing context on the Claude Developer Platform (Anthropic) | https://www.anthropic.com/news/context-management | T1 | Exa fetch |
| The 84% and the 39% (dreaming.press, AI-szerzőségű) | https://dreaming.press/posts/anthropic-context-editing-84-percent-39-percent-numbers-examined.html | T3 | Exa fetch |
| Large Language Models Can Be Easily Distracted (GSM-IC, ICML 2023) | https://proceedings.mlr.press/v202/shi23a.html | T1 | Exa fetch |
| GSM-IC PDF | https://proceedings.mlr.press/v202/shi23a/shi23a.pdf | T1 | Exa fetch |
| MINJA — NeurIPS Abstract | https://proceedings.neurips.cc/paper_files/paper/2025/hash/42a97bbd9844d2bf68596730af80bcdf-Abstract-Conference.html | T1 | Exa fetch |
| MINJA — arXiv full text | https://arxiv.org/pdf/2503.03704 | T1 | Exa search+fetch |
| MINJA — NeurIPS poster page | https://nips.cc/virtual/2025/loc/san-diego/poster/118152 | T1 | Exa search |
| Is Context Rot Real? (Zenodo null-eredmény) | https://doi.org/10.5281/zenodo.20753848 | T2 | Exa fetch |
| Lost in the Middle (TACL 2024) | https://aclanthology.org/2024.tacl-1.9/ | T1 | Exa fetch |
| Context Rot: How Increasing Input Tokens Impacts LLM Performance (Chroma) | https://www.trychroma.com/research/context-rot | T2 | Exa fetch |
| Context Length Alone Hurts LLM Performance Despite Perfect Retrieval | https://arxiv.org/abs/2510.05381 | T1 | Exa fetch |
| Diagnosing and Mitigating Context Rot in Long-horizon Search | https://arxiv.org/abs/2606.29718 | T1 | Exa fetch |
| ChatGPT: Hacking Memories with Prompt Injection (Rehberger) | https://embracethered.com/blog/posts/2024/chatgpt-hacking-memories/ | T1 | Exa fetch |
| Delivery, Not Storage: Cue-Anchored Working Memory (Saha, 2607.20972) | https://arxiv.org/pdf/2607.20972 | T2 | Exa search+fetch |
| Delivery, Not Storage (abs) | https://arxiv.org/abs/2607.20972 | T2 | Exa fetch |
| Memory tool — Claude Platform Docs (élő oldal, 2026-09-25) | https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool | T1 | Exa fetch |
| agent-memory-lab (GitHub, memória-stratégiák A/B-je, nem a kérdésre válaszol) | https://github.com/EnigmaDevelop/agent-memory-lab | T3 | Exa search |
| Shared Selective Persistent Memory for Agentic LLM Systems | https://arxiv.org/html/2607.09493v1 | T2 | Exa search |

*Megjegyzés a Memory tool doksihoz:* a jelenleg élő oldalon (2026-09-25) NEM találtam meg szó szerint az SQ06 2.1 szakaszában idézett „MEMORY PROTOCOL" / „IMPORTANT: ALWAYS VIEW YOUR MEMORY DIRECTORY..." kikényszerítő szöveget — az oldal jelenlegi szövege ("Claude automatically checks its memory directory before starting a task") ezt csak parafrazálja. Ez az ELL05 feladatlistán kívüli, mellékes észrevétel (nem tartozik az 1–7. pontok közé), ezért nem soroltam önálló verdiktként, de érdemes jelezni: a gyártói dokumentáció gyorsan változik, egy korábban pontosan idézett szöveg mára eltűnhetett az élő oldalról.

---

# ELL06 — Önkéntes memóriahasználat és kérdésenkénti automatikus beadás: az állítások ellenőrzése
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

---
