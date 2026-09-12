# Linkek — minden meglátogatott forrás

Kampány: `mcp-felulet` · 2026-09-12


---

## SQ-01 — Mit tud kifejezni egy MCP eszközdefiníció

# SQ-01 — Felhasznált linkek

Minden alábbi forrás a hivatalos `modelcontextprotocol.io` doménről vagy a
hivatalos `github.com/modelcontextprotocol` szervezettől való (T1), kivéve
ahol jelölve.

## Verzió-azonosítás

- https://github.com/modelcontextprotocol/modelcontextprotocol/releases — T1,
  release-lista, megerősíti hogy `2026-07-28` a legfrissebb stabil kiadás.
- https://modelcontextprotocol.io/specification/2026-07-28 — T1, a jelenlegi
  specifikáció főoldala.
- https://blog.modelcontextprotocol.io/posts/2026-07-28/ — T1, hivatalos
  bejelentő blogbejegyzés (szerzők: David Soria Parra, Den Delimarsky —
  "Lead Maintainer"-ek), 2026. július 28.

## Eszköz-definíció / tools

- https://modelcontextprotocol.io/specification/2026-07-28/server/tools — T1,
  fő forrás az 1., 2., 3., 6., 7., 8. ponthoz.
- https://modelcontextprotocol.io/specification/2025-11-25/server/tools — T1,
  összehasonlításhoz (a `listChanged`/hibamodell/annotációk korábbi állapota).
- https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/2026-07-28/schema.ts
  — T1, a séma forráskódja: `Tool`, `ToolAnnotations`, `CallToolResult`,
  `CallToolRequest`, `BaseMetadata`, `Icons`, `TextContent`,
  `PaginatedRequestParams`/`PaginatedResult`/`Cursor` interfészek.

## Erőforrás / resource

- https://modelcontextprotocol.io/specification/2026-07-28/server/resources —
  T1, `resource_link`, annotációk (audience/priority/lastModified), URI
  sémák, hibakód-változás (`-32002` → `-32602`).

## Prompt

- https://modelcontextprotocol.io/specification/2026-07-28/server/prompts —
  T1, a "user-controlled" definícióhoz és a `Prompt`/`PromptMessage`
  adattípusokhoz.

## Lapozás

- https://modelcontextprotocol.io/specification/2026-07-28/server/utilities/pagination
  — T1, teljes lapozási modell.

## Alapprotokoll / hibakódok / `_meta` / JSON Schema

- https://modelcontextprotocol.io/specification/2026-07-28/basic — T1,
  JSON-RPC üzenettípusok, `resultType`, hibakód-particionálás, `_meta`
  kulcsformátum és reserved kulcsok, JSON Schema dialektus-szabályok,
  `$ref` feloldási korlátozás, `icons`.

## Architektúra / primitívák viszonya

- https://modelcontextprotocol.io/specification/2026-07-28/architecture — T1,
  host/client/server modell, capability negotiation, design principles.

## Subscriptions / listaváltozás mechanizmus

- https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/subscriptions
  — T1, `subscriptions/listen`, feliratkozási szűrők, `subscriptionId`.

## Changelogok (verzió-evolúció)

- https://modelcontextprotocol.io/specification/2026-07-28/changelog — T1,
  a `2025-11-25` → `2026-07-28` változások teljes listája.
- https://modelcontextprotocol.io/specification/2025-06-18/changelog — T1,
  strukturált kimenet és resource_link bevezetése.
- https://modelcontextprotocol.io/specification/2025-03-26/changelog — T1,
  tool annotációk bevezetése.

## Egyéb (keresési találatok, nem citált tartalommal, csak tájékozódásra)

- https://en.wikipedia.org/wiki/Model_Context_Protocol — T3/T5 jellegű
  áttekintő, NEM használtam forrásként állításhoz, csak a keresési
  landscape feltérképezésére.
- https://hidekazu-konishi.com/entry/mcp_specification_version_timeline.html
  — másodlagos, NEM citáltam belőle semmit, T1 forrásokat kerestem helyette.
- https://ts.sdk.modelcontextprotocol.io/v2/servers/tools.html — SDK-doksi,
  NEM citáltam, mert a kérdés a specifikációra kérdez, nem az SDK-ra.
- https://workos.com/blog/mcp-2025-11-25-spec-update — T3, gyártói/harmadik
  fél összefoglaló a 2025-11-25 kiadásról, NEM citáltam, csak a keresési
  landscape jelzésére szolgált.


---

## SQ-02 — Milyen eszközfelületet használnak jól a modellek

# SQ-02 — Linkgyűjtemény

Formátum: URL — tier — státusz — megjegyzés. "Felhasznált" = idézve a megallapitasok.md-ben és
archiválva a snapshots/ alatt. "Lead / nem nyitva" = megjelent találatként, de nem lett feldolgozva
(pl. mert más forrás jobban lefedte a témát, vagy időhiány miatt).

## Felhasznált, archivált T1 (hivatalos dokumentáció / specifikáció)

- https://www.anthropic.com/engineering/writing-tools-for-agents — T1 — felhasznált — Anthropic fő
  engineering blog a tool-tervezésről (2025-09-11). Archiválva:
  `snapshots/anthropic-writing-tools-for-agents.md`
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools — T1 — felhasznált —
  Claude API hivatalos "best practices for tool definitions". Archiválva:
  `snapshots/claude-docs-define-tools-handle-tool-calls.md`
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls — T1 — felhasznált
  — is_error, hibaüzenet-minták, retry-viselkedés. Ugyanabban a snapshot fájlban.
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool — T1 — felhasznált
  — 30-50 eszköz feletti pontosságromlás, defer_loading. Archiválva:
  `snapshots/claude-docs-tool-search-tool.md`
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use — T1 — felhasznált —
  grammar-constrained sampling, kötelező mező garancia. Archiválva:
  `snapshots/other-sources-consolidated.md`
- https://www.anthropic.com/engineering/advanced-tool-use — T2 (gyártói önmérés, hivatalos blogon) —
  felhasznált — Tool Search Tool / Programmatic Tool Calling / Tool Use Examples mért hatásai.
  Archiválva: `snapshots/other-sources-consolidated.md`
- https://www.anthropic.com/engineering/code-execution-with-mcp — T2 — felhasznált — 150k→2k token
  példa, köztes eredmények szűrése. Archiválva: `snapshots/other-sources-consolidated.md`
- https://modelcontextprotocol.io/specification/2025-06-18/server/tools — T1 — felhasznált — MCP
  hivatalos Tools specifikáció, hibamodell (Protocol Error vs Tool Execution Error), biztonsági
  ajánlások. Archiválva: `snapshots/other-sources-consolidated.md`
- https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/2025-06-18/schema.ts
  — T1 — felhasznált — `ToolAnnotations` interfész pontos, szó szerinti definíciója
  (readOnlyHint/destructiveHint/idempotentHint/openWorldHint + "hints, not guarantees"
  figyelmeztetés). Archiválva: `snapshots/other-sources-consolidated.md`
- https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation — T1 — felhasznált —
  emberi-jóváhagyás féle interakció a specifikációban, de kifejezetten NEM szenzitív/veszélyes
  művelet megerősítésre szánva. Archiválva: `snapshots/other-sources-consolidated.md`
- https://developers.openai.com/api/docs/guides/function-calling — T1 — felhasznált — OpenAI
  hivatalos function calling útmutató (leírás, "intern test", <20 eszköz ajánlás). Archiválva:
  `snapshots/other-sources-consolidated.md`

## Felhasznált T3-T4 (másodlagos / önjelentett technikai / preprint)

- https://arxiv.org/html/2605.24660v1 — T4 (arXiv preprint, Meta Platforms) — felhasznált — "How
  Many Tools Should an LLM Agent See?" — Bits-over-Random metrika, BFCL/ToolBench mért lefedettségi
  számok. Archiválva: `snapshots/other-sources-consolidated.md`
- https://arxiv.org/html/2601.15812v2 — T4 (arXiv preprint) — felhasznált, de **korlátozott
  relevanciával** — ErrorMap/ErrorAtlas, általános LLM hibataxonómia, NEM tool-hívás-specifikus
  mérés. Archiválva: `snapshots/other-sources-consolidated.md`
- https://codex.danielvaughan.com/2026/04/12/mcp-tool-annotations-risk-vocabulary-codex-cli/ — T3/T4
  (másodlagos technikai blog egy konkrét kliens implementációjáról) — felhasznált — Codex CLI
  jóváhagyási logikája destructiveHint alapján. Archiválva: `snapshots/other-sources-consolidated.md`
- https://stacklok.com/blog/tool-annotations-are-becoming-the-risk-vocabulary-for-agentic-systems-that-matters-more-than-it-might-seem/
  — T3/T4 (biztonsági szolgáltató saját blogja, érvelés, nem mérés) — felhasznált — "Annotations are
  hints, not contracts" megerősítés. Archiválva: `snapshots/other-sources-consolidated.md`
- https://github.com/alexander-zuev/supabase-mcp-server (README) — T4 (nyílt forráskódú projekt
  saját dokumentációja, forráskóddal ellenőrizhető) — felhasznált — konkrét, működő háromszintű
  megerősítési minta (`confirm_destructive_operation`, `live_dangerously`). Archiválva:
  `snapshots/other-sources-consolidated.md`

## Lead / nem nyitva (más SQ-hoz tartozhat, vagy nem bizonyult elég relevánsnak)

- https://dev.to/thedailyagent/mcp-tool-overload-why-more-tools-make-your-agent-worse-5a49 — T6 —
  cím alapján releváns ("tool overload"), de fórum/blog jellegű, tartalmilag valószínűleg
  átfedésben az Anthropic tool-search anyagával — nem nyitottuk meg, mert T1 forrás már lefedte a
  jelenséget mért számokkal.
- https://tianpan.co/blog/2026-04-19-over-tooled-agent-problem — T6 — hasonló okból nem nyitva.
- https://achan2013.medium.com/how-many-tools-functions-can-an-ai-agent-has-21e0a82b7847 — T6 —
  Medium-vélemény, nem nyitva (T0/T6 kategória, nem load-bearing forrásnak szántuk).
- https://arxiv.org/abs/2305.15334 (Gorilla: Large Language Model Connected with Massive APIs,
  NeurIPS 2024, **T2 peer-reviewed** — figyelem, ez valójában elfogadott konferenciacikk, tehát
  magasabb tier, mint egy sima preprint) — cím/absztrakt alapján releváns (API-hallucináció), de
  a hívási-hibák/hiányzó paraméter szemszögéből nem néztük meg részletesen — **hiányos lefedettség,
  ld. gaps.md**.
- https://huggingface.co/datasets/gorilla-llm/Berkeley-Function-Calling-Leaderboard — T1/T4 határeset
  (adatkészlet-oldal) — nem nyitva, a BFCL hibakategória-bontását (pl. missing-parameter arány)
  emiatt nem sikerült közvetlenül lekérdezni.
- https://gorilla.cs.berkeley.edu/leaderboard.html — T1 (projekt saját oldala) — nem nyitva,
  ugyanaz az ok.
- https://glama.ai/mcp/servers/mako10k/mcp-confirm — T4/T6 (MCP-regisztrációs oldal egy konkrét
  szerverről) — nem nyitva, a Supabase-példa már illusztrálta a mintát.
- https://glama.ai/mcp/servers/@portel-dev/ncp/blob/.../docs/confirm-before-run.md — T4 — nem nyitva,
  ugyanaz az ok (redundáns lett volna a Supabase-példával).
- https://dzone.com/articles/mcp-elicitation-human-in-the-loop-for-mcp-servers — T3 — nem nyitva,
  mert a hivatalos MCP elicitation-specifikációt (T1) közvetlenül elolvastuk.
- Magyar nyelvű találatok (learn.microsoft.com/hu-hu, sidekickautomations.hu, devertix.hu,
  cloudmentor.hu, minner.hu) — mind T3/T6 általános MCP-bemutató/marketing tartalom, **egyik sem
  foglalkozik kifejezetten eszköztervezési/hibaüzenet-mintákkal** — ez megerősíti, hogy a téma
  angol nyelvi horgonyú, nem hiányos magyar lefedettség kérdése (ld. gaps.md).

## Nem forrásként használt (AI-összefoglaló vagy nem elsődleges tartalom gyanúja)

- Egyik fetch sem adott vissza egyértelmű AI-generált "összefoglaló oldalt" a valódi tartalom
  helyett — ez a korábbi kampányok visszatérő hibája volt, itt nem fordult elő. Volt viszont egy
  ezzel rokon jelenség: a WebFetch (kis modell) néhány esetben **saját szavakkal renderelte** a
  tartalmat ahelyett, hogy a kért verbatim markdown-t adta volna vissza (pl. az anthropic blog
  hibaüzenet-képeinek leírása, az OpenAI function-calling guide táblázatos összefoglalása). Ezt a
  `gaps.md`-ben külön jelöltem, és ahol lehetett, második, célzottabb prompttal újra lekértem az
  adott szakaszt.


---

## SQ-03 — Létező memória-MCP szerverek

# SQ-03 — Linkek

Jelölés: **T1** forráskód/hivatalos spec, **T2** megbízható másodlagos vagy gyártói állítás saját
termékről, **T3** fórum/vélemény/marketing. A "verbatim?" oszlop jelzi, hogy a WebFetch szó
szerinti tartalmat adott-e vissza, vagy tömörített olvasatot (lásd `gaps.md`).

## Hivatalos referencia memória-szerver

- T1, verbatim (kód) — https://raw.githubusercontent.com/modelcontextprotocol/servers/main/src/memory/index.ts — a teljes `index.ts` forráskód
- T1, verbatim — https://raw.githubusercontent.com/modelcontextprotocol/servers/main/src/memory/README.md — hivatalos README, teljes eszközlista és rendszerprompt-példa
- T1, tömörített — https://github.com/modelcontextprotocol/servers/issues/1819 — "Memory server race condition causes corrupted JSON"
- T1, tömörített — https://github.com/modelcontextprotocol/servers/issues/4117 — "memory: safer persistence defaults, atomic writes, quotas, redaction, and destructive-operation guardrails" (nyitott javaslat)
- Nem nyitva (csak találati cím, nem releváns/redundáns) — https://github.com/modelcontextprotocol/servers/issues/2577, 2578, 2579 — három, feltehetően egymást ismétlő "Bug Report and Resolution" issue ugyanarra a race condition-re; nem néztem meg részletesen, mert az #1819 + a forráskód-javítás már lefedte a lényeget
- T1 — https://github.com/modelcontextprotocol/servers/tree/main/src/memory — a szerver forráskód-mappája (találati lista útján, nem közvetlenül fetchelve)
- T2 — https://www.npmjs.com/package/@modelcontextprotocol/server-memory — npm csomagoldal (nem fetchelve, csak találat)

## mem0

- T2, verbatim próbálkozás → részleges — https://docs.mem0.ai/platform/mem0-mcp — hivatalos MCP dokumentáció, 11 eszköz listája
- T2, tömörített — https://docs.mem0.ai/integrations/claude-code — Claude Code plugin dokumentáció, "kilenc eszköz → egy search_memories" migrációs megjegyzés
- T2, "nem található a lapon" válasz — https://docs.mem0.ai/v0x/core-concepts/memory-operations/add — ADD-only pipeline leírása; az ADD/UPDATE/DELETE/NONE döntési logikát NEM tartalmazta a fetch szerint
- T1/T2, tömörített — https://github.com/mem0ai/mem0/discussions/4787 — "How does Mem0 handle memory deduplication and contradiction resolution at scale?" (közösségi kérdés + fejlesztői válaszok)
- T1, tömörített — https://github.com/mem0ai/mem0/issues/4896 — "ADD-only architecture doesn't implement conflict resolution for semantically similar memories"
- T1 (cím csak) — https://github.com/mem0ai/mem0/issues/4923 — "OpenMemory Sunsetting" — tartalom nem volt kinyerhető
- T1, tömörített — https://github.com/mem0ai/mem0/blob/main/openmemory/README.md — az OpenMemory README, benne a sunsetting-figyelmeztetés
- T2 — https://mem0.ai/blog/introducing-openmemory-mcp — bejelentő blogbejegyzés, 4 eszköz neve
- T2, nem fetchelve, csak találat — https://mem0.ai/blog/how-to-make-your-clients-more-context-aware-with-openmemory-mcp
- T2, nem fetchelve — https://github.com/pinkpixel-dev/mem0-mcp — közösségi mem0 MCP wrapper (nem hivatalos)
- T2, nem fetchelve — https://github.com/simon9679/mem-audit — külső auditáló eszköz duplikátum/ellentmondás-kereséshez (a #4896 hibajegyből)
- T2 — https://github.com/mem0ai/mem0-mcp — hivatalos mem0 MCP repó (csak találat, nem fetchelve részletesen)

## Zep / Graphiti

- T1, verbatim (elég részletesen) — https://raw.githubusercontent.com/getzep/graphiti/main/mcp_server/README.md — hivatalos MCP szerver README, 13 eszköz teljes listája
- T2, verbatim (forráskód-hivatkozásokkal) — https://raw.githubusercontent.com/carsteneu/ai-memory-comparison/main/evidence/graphiti.md — közösségi audit, `graphiti_core/` fájlokra hivatkozva
- T2, nem fetchelve — https://help.getzep.com/graphiti/getting-started/mcp-server
- T2, nem fetchelve — https://blog.getzep.com/cursor-adding-memory-with-graphiti-mcp/
- T2, nem fetchelve — https://www.getzep.com/product/knowledge-graph-mcp/

## Letta / MemGPT

- T2, generikus áttekintésre redirectelt (nem a kért tartalom) — https://docs.letta.com/guides/legacy/memgpt_agents_legacy
- T2, "a lap nem tartalmazza a kért eszközparamétereket" — https://docs.letta.com/guides/core-concepts/memory/memory-blocks
- T2, verbatim (jó részletesség) — https://docs.letta.com/guides/core-concepts/memory/archival-memory — `archival_memory_insert`/`archival_memory_search` paraméterek
- T2, "nem releváns tartalom" — https://docs.letta.com/guides/ade/core-memory/
- T2, verbatim (forráskód-hivatkozásokkal, fájl/függvény szinten) — https://raw.githubusercontent.com/carsteneu/ai-memory-comparison/main/evidence/letta.md
- Nem sikerült (404) — https://raw.githubusercontent.com/letta-ai/letta/main/letta/functions/function_sets/base.py — a fájl-útvonal feltehetően megváltozott, nem találtam meg a helyeset a rendelkezésre álló kereséssel/idővel

## basic-memory

- T2, verbatim, nagyon részletes — https://docs.basicmemory.com/reference/mcp-tools-reference — teljes eszköz- és paramétertáblázat
- T2, verbatim — https://docs.basicmemory.com/teams/members-and-roles — öt szerepkör, tagsági státuszok
- Nem fetchelve, csak találat — https://github.com/basicmachines-co/basic-memory — a tényleges forráskód-repó (a kényszerítő okok miatt a hivatalos doksit használtam elsődleges forrásként, nem magát a Python/TS kódot)
- Nem fetchelve — https://github.com/basicmachines-co/basic-memory-skills

## OpenMemory

- Lásd a mem0 szekciót — a README és a blogbejegyzés innen fedi.
- T2, nem fetchelve — https://apidog.com/blog/openmemory-mcp-server/
- T2, nem fetchelve — https://deepwiki.com/mem0ai/mem0/15.2-openmemory-mcp-server (DeepWiki — AI-generált wiki, tudatosan nem használtam elsődleges forrásként)
- T2, nem fetchelve — https://deepwiki.com/mem0ai/mem0/15.1-openmemory-overview-and-migration

## Közösségi forkok a hivatalos referenciára

- T1, verbatim — https://raw.githubusercontent.com/gannonh/memento-mcp/main/README.md
- T1, verbatim (GitHub oldal-fetch, nem raw) — https://github.com/iAchilles/memento (a `raw.githubusercontent.com/.../main/README.md` 404-et adott, a `master` ág vagy más útvonal lehet a helyes; a `github.com` sablon-oldal viszont sikeresen visszaadta a README-t)
- Blokkolva (robots.txt) — https://github.com/carsteneu/ai-memory-comparison/tree/main/evidence — a mappalistázás nem volt elérhető; helyette közvetlen fájlnév-találgatással (`mem0.md`, `graphiti.md`, `letta.md`) jutottam a tartalomhoz
- 403 (proxy/rate limit, nem valódi elutasítás, de nem újrapróbáltam más útvonalon idő hiányában) — https://api.github.com/repos/carsteneu/ai-memory-comparison/contents/evidence
- Blokkolva (robots.txt) — https://glama.ai/mcp/servers/@gregorydickson/memory-graph/blob/.../docs/archive/MIGRATION.md — egy ígéretes "claude-code-memory → MemoryGraph" migrációs dokumentum, aminek a tartalmát NEM sikerült megszerezni
- Nem fetchelve, csak találat — https://github.com/okooo5km/memory-mcp-server — Go-nyelvű, hasonló API-jú fork (nem néztem meg részletesen)
- Nem fetchelve, csak találat — https://mnemoverse.com/docs/library/memory-mcp-servers-compared — "13 Memory MCP Servers Compared (2026)" — ígéretes másodlagos áttekintő, időhiány miatt nem dolgoztam fel

## Egyéb, csak találatként látott, nem feldolgozott linkek

- https://github.com/mem0ai/mem0/issues/4910 — OpenMemory env-var override hiba (nem releváns az SQ-03 kérdéseihez, csak konfigurációs bug)
- https://www.tooljunction.io/mcp/basic-memory, https://mcpservers.org/servers/..., https://glama.ai/mcp/servers/... — katalógusoldalak, csak keresési találatok, nem elsődleges forrásként használva


---

## SQ-04 — Azonosítás és jogosultság MCP-ben

# SQ-04 — Források (linkek)

Tier-rendszer a feladat szerint: **T1** = hivatalos spec/RFC/hivatalos dokumentáció/SDK
forráskód. **T2** = megbízható másodlagos VAGY gyártó saját termékéről szóló állítás.
**T3** = fórum/vélemény/marketing.

## T1 — Hivatalos MCP specifikáció és dokumentáció

| URL | Mit tartalmaz | Megjegyzés |
|---|---|---|
| https://modelcontextprotocol.io/specification/versioning | Verzió-lista, "current" = 2026-07-28 | Teljes, verbatim letöltve |
| https://modelcontextprotocol.io/specification/2024-11-05/basic | Az ELSŐ spec-verzió "Auth" szakasza: nincs hitelesítés | Teljes, verbatim |
| https://modelcontextprotocol.io/specification/2025-03-26/basic/authorization | Az ELSŐ authorization-fejezet: OAuth 2.1, OPTIONAL, stdio kivétel, 3rd-party flow | Teljes, verbatim |
| https://modelcontextprotocol.io/specification/2025-06-18/changelog | Mi változott 2025-03-26 → 2025-06-18: RFC 8707, RFC 9728, "OAuth Resource Server" besorolás | Teljes, verbatim |
| https://modelcontextprotocol.io/specification/2025-11-25/basic/transports | `Mcp-Session-Id`, session management, session ID formátum | Teljes, verbatim |
| https://modelcontextprotocol.io/docs/2025-11-25/tutorials/security/security_best_practices | Confused Deputy, Token Passthrough, **Session Hijacking** (szó szerint), Local Server Compromise | Teljes, verbatim |
| https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization | A JELENLEGI (2026-09-12-én érvényes) authorization spec: RFC9728 MUST, CIMD, iss-validáció, refresh token szabályok | Teljes, verbatim |
| https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices | Ugyanaz mint fent, kiegészítve: **State Handle Hijacking** (a session-koncepció megszűnése után), SSRF, mix-up attack, localhost redirect impersonation, CIMD trust policy, scope minimization | Teljes, verbatim |
| https://modelcontextprotocol.io/specification/2026-07-28/basic/transports | Transport-réteg jelenlegi felépítése — kimondja, hogy a protokoll **stateless** | Teljes, verbatim |
| https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio | stdio transport jelenlegi (2026-07-28) leírása, `_meta` mezőben "optional client identity" | Teljes, verbatim |
| https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/authorization | Gyakorlati oktató anyag: "authorization is optional", stdio = environment-based credentials, teljes Keycloak+TS/Python/C# munkapélda JWT `sub`/`aud` validációval | Teljes, verbatim (hosszú, fájlba mentve) |
| https://blog.modelcontextprotocol.io/posts/2026-07-28/ | Hivatalos blogbejegyzés a 2026-07-28 verzióról: miért lett stateless, mi változott az authorization-ban | Részben összefoglalva a fetch-eszköz által, de a kulcsmondatok idézőjelben szerepelnek |
| https://github.com/github/github-mcp-server/blob/main/docs/oauth-login.md | GitHub hivatalos MCP szervere: OAuth token vagy PAT, memóriában tartott token, scope-alapú tool-szűrés | **A fetch összefoglalást adott vissza, nem verbatim szöveget** — ld. `gaps.md` |
| https://claude.com/docs/connectors/building/authentication | Anthropic hivatalos dokumentációja: hogyan azonosítja Claude a hívó felhasználót MCP connectoroknál, `oauth_dcr`/`oauth_cimd`/`oauth_anthropic_creds`/`static_headers`/`none`, "every connection requires user consent" | Teljes, verbatim |

## T2 — Megbízható másodlagos forrás

| URL | Mit tartalmaz | Megjegyzés |
|---|---|---|
| https://stackoverflow.blog/2026/01/21/is-that-allowed-authentication-and-authorization-in-model-context-protocol/ | Stack Overflow szerkesztőségi blogja: stdio vs HTTP fenyegetettségi modell, downstream-authorization rés, Token Exchange (RFC 8693) ajánlás, client_credentials történet | Teljes, verbatim letöltve |

## Megnyitott, de mélyebben nem feldolgozott találatok (leadek, nem forrás)

Ezek csak a WebSearch snippetjeiben jelentek meg, a teljes oldalt nem töltöttem le, ezért
**nem szerepelnek forrásként** a megallapitasok.md-ben. Későbbi körnek érdemes lehet:

- aembit.io/blog/mcp-authentication-and-authorization-patterns/ (T3-gyanús, vendor blog)
- descope.com/blog/post/mcp-auth-spec ("Diving Into the MCP Authorization Specification")
- auth0.com/blog/mcp-streamable-http/ ("Why MCP's Move Away from SSE Simplifies Security")
- equixly.com/blog/2026/08/05/stateless-mcp/ ("Stateless MCP: what the 2026-07-28 spec changes for security")
- medium.com/@ayshsandu/the-evolution-of-mcp-auth-... (verzió-történeti áttekintés, de Medium = T3 hacsak a szerző nem azonosítható szakértő)
- workos.com/blog/what-is-mcp-authorization (vendor, IdP-szolgáltató — T2/T3 határon)
- truto.one/blog/implementing-end-user-oauth-identity-passthrough-for-remote-mcp-servers/
- github.com/modelcontextprotocol/modelcontextprotocol/issues/1359 (SEP-1359, a stateless
  átállás javaslata — T1 lenne, mivel a projekt saját GitHub issue-ja, de nem nyitottam meg)
