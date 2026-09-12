# Keresések — minden lefuttatott lekérdezés

Kampány: `mcp-felulet` · 2026-09-12


---

## SQ-01 — Mit tud kifejezni egy MCP eszközdefiníció

# SQ-01 — Keresési napló

Módszertan: `deep-web-research` skill `search-playbook.md` ajánlása szerint
széles kérdéssel indultam, majd a talált szókincs (pl. "2026-07-28",
"resultType", "MRTR", "subscriptions/listen") alapján szűkítettem. A
tool-call költségvetést nem közelítettem meg (kb. 12 WebSearch/WebFetch
hívás összesen, a 30-as ajánlott keret alatt), mert a hivatalos domain
azonnal, közvetlenül elérhető és teljes válaszokat adott — nem volt szükség
sok reformulációra vagy alternatív forráskeresésre.

1. `Model Context Protocol specification version 2025` (WebSearch) — feltárta,
   hogy létezik `2025-11-25` verzió, és utalt egy "One Year of MCP" blogra;
   ez jelezte, hogy érdemes tovább keresni frissebb verzió után is.
2. `MCP specification tools/list inputSchema outputSchema structuredContent`
   (WebSearch) — vocabulary-feltárás, harmadik fél cikkeket hozott
   (nem citáltam őket), de megerősítette a keresendő kulcsszavakat.
3. `"modelcontextprotocol.io/specification" latest version 2026` (WebSearch)
   — nem hozott közvetlen 2026-07-28 találatot, de a fő specifikáció-oldal
   közvetlen fetch-elése (lépés 4) feltárta a verziót.
4. WebFetch: `modelcontextprotocol.io/specification/2025-11-25` — a
   kezdetben feltételezett "legfrissebb" verzió tartalmának rögzítése.
5. WebFetch: `github.com/modelcontextprotocol/modelcontextprotocol/releases`
   — **ez a lépés fedte fel, hogy `2026-07-28` az aktuális "Latest Stable"**,
   nem a `2025-11-25`. Kritikus fordulópont a kutatásban.
6. WebFetch: `modelcontextprotocol.io/specification/2025-11-25/server/tools`
   — a korábbi (helytelenül "aktuálisnak" hitt) állapot rögzítése
   összehasonlításhoz.
7. Innentől minden fetch a helyes, `2026-07-28` útvonalra irányult:
   `server/tools`, `server/resources`, `server/prompts`,
   `server/utilities/pagination`, `basic`, `architecture`,
   `basic/patterns/subscriptions`, `changelog`.
8. WebFetch: raw GitHub `schema.ts` (2026-07-28) — kétszer, célzott
   promptokkal, hogy a `Tool`/`ToolAnnotations`/`CallToolResult`/
   `BaseMetadata`/`Icons`/`Cursor` interfészeket szó szerint, kommentekkel
   együtt kapjam vissza (nem összefoglalva).
9. WebFetch: `2025-06-18/changelog` és `2025-03-26/changelog` — a
   strukturált kimenet és az annotációk bevezetési dátumának
   megállapítására ("mikortól van" kérdés).
10. WebSearch: `site:modelcontextprotocol.io response size limit large tool
    result` — nulla releváns hivatalos találat; ez erősítette meg, hogy a
    válaszméret-korlátozás valódi hiány a specifikációban (nem csak nem
    találtam meg).
11. WebFetch: `blog.modelcontextprotocol.io/posts/2026-07-28/` — a hivatalos
    bejelentés teljes szövege, a verzió véglegesítésére (harmadik
    független T1 megerősítés).
12. WebSearch: `modelcontextprotocol blog specification release September
    2026` — nem talált `2026-07-28`-nál újabb kiadást; ez zárta le a
    "van-e ennél frissebb" kérdést negatív eredménnyel (evidence of
    absence egy ilyen kiadásra "mai" dátum, 2026-09-12, szerint).

## AI-összefoglaló ellenőrzés

Minden WebFetch hívásnál explicit "verbatim, ne foglald össze" promptot
használtam (a search-playbook.md ajánlása szerint). Egyik visszakapott
tartalom sem tűnt AI-generált összefoglalónak — mindegyik a Mintlify-alapú
dokumentációs oldal natív markdown-exportjának tűnik (a "Documentation
Index" fejléc-blokk minden oldalon azonos, natív navigációs elem, nem
AI-összefoglaló jelzés). Nem találkoztam a "fetch AI-összefoglalót ad vissza
a valódi oldal helyett" hibával ebben a körben.


---

## SQ-02 — Milyen eszközfelületet használnak jól a modellek

# SQ-02 — Keresési napló

Eszközök: WebSearch, WebFetch (ToolSearch-csel betöltve). Kb. 32 hívás összesen (WebSearch + WebFetch),
a skill kb. 30-as irányértékén belül, a 40-es kemény limit alatt.

## Kör 1 — tájékozódás, tágabb lekérdezések

1. WebSearch: `Anthropic writing effective tools for agents` — megtalálta a fő T1 forrást
   (anthropic.com/engineering/writing-tools-for-agents)
2. WebSearch: `OpenAI function calling best practices guide` — vegyes találatok, a hivatalos
   fejlesztői doksi linkje (developers.openai.com) csak a következő körben került elő pontosan
3. WebSearch: `Anthropic tool use concise detailed response format token efficient` — megerősítette,
   hogy a "concise/detailed" fogalom a fő blogbejegyzésben van

## Kör 2 — elsődleges Anthropic-tartalom lekérése

4. WebFetch: anthropic.com/engineering/writing-tools-for-agents (teljes, verbatim)
5. WebSearch: `OpenAI platform docs function calling guide site:platform.openai.com OR
   site:developers.openai.com` — pontosította a hivatalos URL-t

## Kör 3 — hibaüzenet-részletek és hivatalos API-doksi

6. WebFetch: anthropic.com/engineering/writing-tools-for-agents (célzott: hibaüzenet-példa
   szövegének kinyerése — a fetch jelezte, hogy a példák képként szerepelnek, szöveg nem nyerhető ki)
7. WebFetch: platform.claude.com/.../handle-tool-calls (teljes, verbatim — is_error, retry-viselkedés)

## Kör 4 — eszközszám/pontosság, MCP-annotációk

8. WebFetch: platform.claude.com/.../tool-search-tool (teljes, verbatim — 30-50 eszköz küszöb)
9. WebSearch: `MCP tool annotations destructiveHint idempotentHint readOnlyHint openWorldHint
   specification`
10. WebSearch: `too many tools LLM function calling accuracy degradation benchmark number of tools`
    — megtalálta a Meta BoR-arXiv preprintet

## Kör 5 — mért adat és hivatalos spec-szöveg

11. WebFetch: arxiv.org/html/2605.24660v1 (Meta BoR-tanulmány, kulcs számok kinyerése)
12. WebFetch: modelcontextprotocol.io/specification/2025-06-18/server/tools (teljes, de az
    annotáció-definíciók a renderelt oldalon nem jelentek meg részletesen)

## Kör 6 — pontos annotáció-definíciók, idempotencia keresés

13. WebFetch: raw.githubusercontent.com/.../schema/2025-06-18/schema.ts (ToolAnnotations interfész,
    szó szerinti kommentekkel — sikeres, pontos T1 idézet)
14. WebSearch: `"idempotentHint" "destructiveHint" MCP schema description "If true"` — megerősítő
    kör, nem hozott újat a 13. lépéshez képest

## Kör 7 — OpenAI hivatalos doksi, elicitation, BFCL

15. WebFetch: developers.openai.com/api/docs/guides/function-calling (teljes, verbatim)
16. WebSearch: `MCP elicitation specification human in the loop confirmation dangerous action`
17. WebSearch: `Berkeley Function Calling Leaderboard missing required parameter error analysis` —
    nem hozott közvetlenül feldolgozható, konkrét %-os hibabontást (csak leaderboard/dataset linkek)

## Kör 8 — elicitation spec, hibataxonómia, Gorilla lead

18. WebFetch: modelcontextprotocol.io/specification/2025-06-18/client/elicitation (teljes, verbatim)
19. WebSearch: `LLM function calling error taxonomy "missing parameter" hallucinated parameter study
    measurement` — arXiv preprint találatok (ErrorMap/ErrorAtlas, Think-Augmented Function Calling)
20. WebSearch: `Gorilla API hallucination AST accuracy paper large language model connected massive
    APIs` — megerősítette, hogy a Gorilla-cikk NeurIPS 2024 elfogadott (T2), de nem dolgoztuk fel
    részletesen (idő/relevancia — a hallucináció-fókusz nem pontosan a "hiányzó kötelező paraméter"
    kérdés)

## Kör 9 — hibataxonómia-mélyítés, konkrét megerősítési minták keresése

21. WebFetch: arxiv.org/html/2601.15812v2 (ErrorMap/ErrorAtlas — kiderült, hogy NEM tool-specifikus)
22. WebFetch: codex.danielvaughan.com/.../mcp-tool-annotations-risk-vocabulary-codex-cli/ (konkrét
    kliens-oldali jóváhagyási logika leírása)
23. WebSearch: `MCP server dry_run confirm parameter pattern destructive action two-step "confirm:
    true"` — megtalálta a Supabase MCP server és más konkrét implementációk nyomát

## Kör 10 — konkrét kétlépéses minta megerősítése, Stacklok

24. WebSearch: `supabase-community mcp-server-supabase confirm_destructive_operation github
    execute_sql unsafe_mode` — megtalálta a helyes repót
25. WebFetch: stacklok.com/.../tool-annotations-are-becoming-the-risk-vocabulary... (nem talált
    mért adatot, csak elméleti érvelést — ezt a digestben jeleztem)

## Kör 11 — a konkrét minta forrásszövege, Advanced Tool Use blog

26. WebFetch: raw.githubusercontent.com/alexander-zuev/supabase-mcp-server/.../README.md (a
    háromszintű safe/write/destructive minta pontos leírása)
27. WebSearch: `Anthropic advanced tool use blog effective context engineering agents tool bloat`

## Kör 12 — záró mélyítés: kód-végrehajtás, tool-granularitás ellenpróba, magyar nyelvi ellenőrzés

28. WebFetch: anthropic.com/engineering/advanced-tool-use (teljes, verbatim — 49%→74%, 79.5%→88.1%,
    72%→90% számok)
29. WebFetch: anthropic.com/engineering/code-execution-with-mcp (150k→2k token példa)
30. WebSearch: `"single tool" "action parameter" vs multiple tools LLM accuracy granularity design`
    — nem hozott új, közvetlenül idézhető mért adatot a "1 nagy tool vs sok kicsi" kérdésre
31. WebSearch: `MCP eszköz tervezés hibaüzenet AI ügynök magyar` — megerősítette a nyelvi lefedettségi
    hiányt (csak általános MCP-bemutató tartalom magyarul, eszköztervezési részletek nélkül)

## Kör 13 — strict tool use mechanizmus lezárása

32. WebFetch: platform.claude.com/.../strict-tool-use (teljes, verbatim — grammar-constrained
    sampling mechanizmus, kötelező mező garancia)

## Amit KIHAGYTUNK, és miért

- Nem futtattunk külön keresési kört a Google/Gemini function calling dokumentációjára — a
  feladatkiírás kifejezetten Anthropic + OpenAI hivatalos útmutatóit kérte, ezt tartottuk
  elsődlegesnek a 30-as tool-call-budget mellett.
- Nem nyitottuk meg a BFCL/Gorilla leaderboard adatoldalait mélyebben (csak a metaadat-szintű
  keresésig jutottunk) — ez a `gaps.md`-ben szerepel nyitott hiányként a Q5 (kötelező paraméter
  kihagyás mért aránya) kérdésre.


---

## SQ-03 — Létező memória-MCP szerverek

# SQ-03 — Keresési napló

PRISMA-S stílusban, a ténylegesen kiadott lekérdezések, verbatim.

| Eszköz | Lekérdezés | Megjegyzés |
|---|---|---|
| WebSearch | `modelcontextprotocol servers memory server github source` | Orientáció, megtaláltam a repó/README/npm útvonalakat |
| WebSearch | `mem0 MCP server tools add_memory search_memory` | Orientáció mem0-hoz |
| WebSearch | `modelcontextprotocol/servers memory server issue #1819 concurrent writes corrupt` | Konkrét hibajegy keresése, miután a forráskód kommentje utalt rá |
| WebSearch | `Zep Graphiti MCP server tools add_memory search_facts source` | Orientáció Graphiti/Zep-hez |
| WebSearch | `basic-memory MCP server tools write_note search_notes read_note github` | Orientáció basic-memory-hoz |
| WebSearch | `OpenMemory MCP server mem0 tools add_memories search_memory list_memories delete_all_memories` | Orientáció OpenMemory-hoz |
| WebSearch | `Letta MemGPT MCP server memory tools archival_memory_insert core_memory_append` | Orientáció Letta/MemGPT-hez |
| WebSearch | `Letta docs memory blocks core_memory_append archival_memory_insert conversation_search tool` | Pontosabb Letta-dokumentáció keresése |
| WebSearch | `mem0 add_memory deduplication conflict resolution LLM merge existing memories` | Duplikátum/konfliktus-kezelés — ez hozta a #4787 discussion és #4896 issue találatokat |
| WebSearch | `"mcp-server" memory github "search_nodes" OR "delete_entities" issue lessons learned discussion` | Általános "lessons learned" keresés a hivatalos szerver köré — inkább közösségi forkokat hozott (okooo5km, memento) |
| WebSearch | `modelcontextprotocol servers memory server issue #1819 concurrent writes corrupt` | (duplikált, lásd fent) |
| WebSearch | `mem0 "ADD" "UPDATE" "DELETE" "NONE" memory operations arxiv paper LLM decides` | Az ADD/UPDATE/DELETE/NONE döntési logika hivatalos leírását kerestem — nem hozott közvetlen hivatalos oldalt, csak közvetett találatokat |
| WebSearch | `docs.letta.com core_memory_append core_memory_replace parameters tool` | Konkrét Letta-eszköz paraméterek keresése |
| WebSearch | `mem0ai openmemory github source api.py add_memories tool mcp_server` | OpenMemory forráskód helyének keresése (nem jártam sikerrel a tényleges .py fájllal) |
| WebSearch | `letta-ai/letta github source "core_memory_append" function definition base_tools.py` | Letta forráskód közvetlen elérésének kísérlete — nem hozott működő raw URL-t |
| WebSearch | `OpenMemory sunset mem0 why deprecated announcement self-hosted server` | A sunsetting indoklásának keresése — csak a #4923 cím került elő, tartalom nélkül |
| WebSearch | `letta-ai/letta github "function_sets" base.py core_memory_append raw githubusercontent` | Második kísérlet a Letta forráskód elérésére — szintén sikertelen, csak a carsteneu audit jött elő újra |
| WebSearch | `iAchilles memento MCP server memory embeddings improved search knowledge graph` | A `memento`-fork(ok) beazonosítása |
| WebSearch | `mem0 claude code plugin "nine" tools "search_memories" migration why simplified` | A "9 eszköz → 1 search_memories" állítás forrásának/indoklásának keresése — nem hozott külön migrációs dokumentumot |

## WebFetch hívások (célzott, nem kereső)

A fenti keresésekből kinyert URL-ek WebFetch-csel való lekérése a `links.md`-ben van részletezve
forrásonként (URL + tier + "verbatim/tömörített" jelöléssel). Nem ismétlem meg itt a teljes
listát a duplikáció elkerülése végett.

## Amit NEM kerestem meg (időkorlát/hatókör miatt)

- Nem futtattam külön magyar nyelvű keresési kört — ez a téma (MCP memória-szerverek) angol
  nyelvű ökoszisztéma, a fejlesztők és a dokumentáció is angolul íródik; magyar nyelvű elsődleges
  forrás esetén nem is várható releváns találat. Ezt a `search-playbook.md` nyelvi lefedettségi
  szabálya alapján explicit gap-ként rögzítem is a `gaps.md`-ben, nem hallgatom el.
- Nem néztem meg részletesen a `modelcontextprotocol/servers#2577/2578/2579` hibajegyeket
  (feltehetően duplikátumok az #1819-hez képest) — a forráskód-szintű javítás és az #1819 már
  megadta a lényeget, a további három megnyitása feltehetően nem hozott volna új információt a
  30 hívásos költségkeret erejéig.
- Nem próbáltam meg más módon (pl. GitHub code search UI-n át) megkeresni a Letta pontos
  forráskódját, miután két közvetlen raw-URL próbálkozás 404-et adott — a közösségi audit
  forráskód-hivatkozásaira támaszkodtam helyette.


---

## SQ-04 — Azonosítás és jogosultság MCP-ben

# SQ-04 — Keresési napló

Ügynök: Sonnet (kutató), egy menetben, kb. 24 tool hívás.
Dátum: 2026-09-12.

## WebSearch lekérdezések

1. `Model Context Protocol specification versions changelog 2024-11-05 2025-03-26 2025-06-18`
   — a spec-verziók feltérképezésére. Eredmény: felfedte, hogy a "jelenlegi" verzió
   valójában **2026-07-28**, nem 2025-06-18 (a kampány kiindulási feltevése elavult volt).
2. `MCP specification authorization "confused deputy"` — a "confused deputy" szakasz
   megtalálására. Talált: hivatalos security best practices oldal, + több másodlagos elemzés
   (nem nyitottam meg mindet).
3. `"Mcp-Session-Id" header session hijacking MCP specification` — a session-kezelés és
   session hijacking hivatalos leírásának megtalálására.
4. `GitHub MCP server OAuth authentication how identifies user` — valós, sokfelhasználós
   MCP szerver azonosítási mintájának kereséséhez.
5. `Claude remote MCP connector "on behalf of" user identity agent OAuth` — az
   "agent mint közvetítő" kérdéshez (Anthropic saját gyakorlata).
6. `"2026-07-28" MCP specification stdio authorization "SHOULD NOT" OR "OPTIONAL" environment credentials`
   — annak ellenőrzésére, hogy a legújabb spec-verzióban is optional-e a hitelesítés és mit
   mond a stdio-ról.
7. `MCP server multi-tenant "user_id" OAuth token sub claim map internal user pattern authorization`
   — a "bevett minta" (established pattern) kereséséhez, hogyan kötik egy híváshoz az
   embert.

## WebFetch — teljes oldal lekérések (elsődleges források)

Lásd részletesen `links.md`. Minden lekérésnél a WebFetch promptja explicit kérte a
"verbatim, ne foglald össze" formát a search-playbook ajánlása szerint. Egy esetben
(`github-mcp-server/docs/oauth-login.md`) a visszakapott szöveg **összefoglalás** volt, nem
szó szerinti másolat — ezt a `gaps.md` jelöli, és az onnan idézett részek csak az ott
konkrétan idézőjelbe tett mondatok erejéig tekinthetők szó szerintinek.

## Módszertani megjegyzés

Ez a kör nem használta a skill teljes script-alapú pipeline-ját (`capture_source.py`,
`add_claim.py` stb.) — a szülő ügynök (Opus) ehhez a kampányhoz egy egyszerűsített,
öt fájlos kimeneti szerkezetet írt elő SQ-mappánként (`megallapitasok.md`, `links.md`,
`searches.md`, `gaps.md`, `contradictions.md`). A forrás-tercizés (T1/T2/T3) és a
szó szerinti idézés elve változatlanul érvényes, csak a gépi index/manifest lépés maradt el.
