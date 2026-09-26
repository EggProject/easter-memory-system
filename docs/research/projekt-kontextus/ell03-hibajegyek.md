# ELL03 — Hibajegyek a memória-hatókör kezeléséről: léteznek-e, és mit mondanak?

**Módszertani megjegyzés:** ez a munkamenet is (az előző körhöz hasonlóan) sorozatos, egyetlen munkamenetben futó, kizárólag Exa `web_search_exa`/`web_fetch_exa` eszközökkel végzett ellenőrzés — az Exa elérhető volt, alügynök-indítás nem állt rendelkezésre, ezért degradált (nem multi-agent) módban dolgoztam, a `_ell_kozos.txt` előírása szerint. Minden idézett hibajegyet közvetlenül megnyitottam a GitHub-on (Exa fetch), nem az előző kör idézeteire hagyatkoztam.

## Verdikt-összefoglaló

| # | Állítás | Verdikt | Egy mondat |
|---|---|---|---|
| 1 | mem0ai/mem0 #6277, #6342, #6655, #6796 — a `user_id`/`agent_id`/`run_id` hatókör-mezőket a `metadata` felülírhatta; javították-e, melyik verzióban? | **RÉSZBEN** | Mind a négy jegy létezik pontosan az idézett tartalommal, és három (#6277, #6342, #6655) valóban javítva van, konkrét, azonosítható kiadásokban (Python v2.0.13 / v2.0.16, TS/Node v3.1.1) — de a negyedik (#6796) **2026-09-25-én (a mai napon) is NYITOTT**, a javító PR (#6797) még nincs mergelve. |
| 2 | Claude Code #41283 és #53734 — a projekt-hatókör a fájlrendszer-útvonalból jön; worktree-törlés, átnevezés vagy szülőkönyvtárra lépés miatt más projekt memóriája töltődik be (#53734: 8 eset) | **RÉSZBEN, jelentős pontosítással** | Mindkét jegy létezik, a „8 dokumentált eset" idézet szó szerint stimmel, DE #41283-at a stale-bot zárta le kód-javítás nélkül, #53734-et pedig — miután egy másik, szintén megoldatlan jegy (#52772) duplikátumaként inaktivitás miatt lezárták — a bejelentő újra beküldte (#86945), és ott egy Anthropic-mérnök (bcherny, 2026-08-25) kifejezetten **dokumentált, szándékos viselkedésnek** minősítette a git-repository-szintű megosztást, „working-as-documented"-ként zárva, létező konfigurációs megoldással (`autoMemoryDirectory`). |
| 3 | Claude Code #40541 — a modell CLAUDE.md explicit szabály ellenére 5+ alkalommal keverte a personal/project/team infót | **RÉSZBEN** | A jegy és az idézet szó szerint létezik, de az ügy **egyetlen felhasználó (n=1) be nem vizsgált** beszámolója, amelyet a bejelentő saját maga zárt le kb. egy órán belül „duplikátumként" három olyan másik jegyhez, amelyek — ellenőrzésem szerint — **nem ugyanarról a hibáról szólnak**; ez egybevág a repó dokumentált, önálló meta-problémájával (#19267), miszerint a duplikátum-bot gyakran téves párosításokat javasol. |

## Állításonként

### 1. mem0ai/mem0 — #6277, #6342, #6655, #6796

**#6277** (Python SDK, `update()`) — LÉTEZIK, megerősítve.
- Cím pontosan: *„update() lets caller metadata silently overwrite user_id/agent_id/run_id, breaking tenant isolation"*
- Állapot: **Closed**. Létrehozva: 2026-07-13. Címkék: `bug`, `P0-critical`.
- Szó szerint (karbantartói triázs, kartik-mem0): „**Severity:** P0. No malformed input is needed — a normal-looking `metadata` dict silently breaks tenant isolation and causes real data loss…plus cross-tenant data exposure, on both the Python SDK's primary write path and the shipped REST server."
- **Javítva:** PR **#6278** (*„fix(memory): don't let update() metadata overwrite user_id/agent_id/run_id"*), state: **merged**, mergelve **2026-07-21T07:14:22Z**. A review-folyamat egy második, súlyosabb rést is feltárt és bezárt még a mergelés előtt: a reviewer (kartik-mem0) írta: „the loop only re-asserts an identity key `if _identity_key in existing_memory.payload`… `update(metadata={"agent_id": "attacker_agent"})` injects a brand-new identity key straight into the stored payload unopposed" — ezt a szerző „strip-before-merge" megközelítésre váltva javította a mergelés előtt.
- **Kiadott verzióban:** a mem0ai Python SDK **v2.0.13** (GitHub release, publikálva 2026-07-22T19:41:55Z) tartalmazza: „Core: Stop `update()` metadata from overwriting or injecting `user_id`, `agent_id`, `run_id`, or `actor_id`… (#6278)". Két független forrás a verziószámra: GitHub Releases (https://github.com/mem0ai/mem0/releases/tag/v2.0.13) és a PyPI/ReversingLabs verziólista (https://secure.software/pypi/packages/mem0ai/versions), amely v2.0.13-at is felsorolja a v2.0.12 (2026-07-13) után.
- URL: https://github.com/mem0ai/mem0/issues/6277 ; PR: https://github.com/mem0ai/mem0/pull/6278

**#6342** (TypeScript OSS SDK, `update()`) — LÉTEZIK, megerősítve.
- Cím pontosan: *„update() metadata silently overwrites user_id/agent_id/run_id in TS SDK, breaking tenant isolation"*
- Állapot: **Closed**. Létrehozva: 2026-07-16. Címkék: `bug`, `P0-critical`.
- Szó szerint: „This is a regression: #5480 removed the identity-key whitelist that previously protected these fields here."
- **Javítva:** PR **#6343**, state: **merged**, mergelve **2026-07-21T06:41:47Z**, lezárja #6342-t ÉS #6367-et (egy a review során feltárt camelCase-alias rést is, `userId`/`agentId`/`runId`, amit a `normalizePayload()` promóciós logikája nyitva hagyott volna).
- **Kiadott verzióban:** a mem0 **Node/TypeScript SDK v3.1.1** (GitHub release, publikálva 2026-07-22T18:12:36Z) tartalmazza szó szerint: „Memory (OSS): Stop `update()` metadata from overwriting or injecting `user_id`, `agent_id`, `run_id`, or `actor_id` (in either snake_case or camelCase)… (#6343)". Két független forrás: GitHub Releases (https://github.com/mem0ai/mem0/releases/tag/ts-v3.1.1) és npm registry (https://registry.npmjs.org/mem0ai — „3.1.1 · Published Jul 22, 2026").
- URL: https://github.com/mem0ai/mem0/issues/6342 ; PR: https://github.com/mem0ai/mem0/pull/6343

**#6655** (Python SDK, `add()` — a létrehozási útvonal testvérhibája) — LÉTEZIK, megerősítve.
- Cím pontosan: *„Python OSS SDK: add() lets metadata set identity scope (user_id/agent_id/run_id/actor_id) on creation"*
- Állapot: **Closed**. Létrehozva: 2026-07-29.
- Szó szerint: „The created memory is now discoverable through `get_all(filters={"agent_id": "victim-agent"})`… scopes the caller never held."
- **Javítva:** PR **#6656** (*„fix(memory): stop add() metadata from setting a memory's identity scope"*) — FONTOS PONTOSÍTÁS: az előző kör összefoglaló táblázata nem tüntette fel a javító PR számát ennél a jegynél; a javítás nem a #6655-ös számú PR-ban, hanem a **#6656**-ban történt (az issue és a fix PR száma itt eltér a #6277/#6278 és #6342/#6343 párosokétól).
- **Kiadott verzióban:** a mem0ai Python SDK **v2.0.16** (GitHub release, publikálva 2026-08-04T18:51:47Z) tartalmazza: „Core: Stop `add()` metadata from setting a memory's identity scope… (#6656)". Megerősítve a hivatalos changelog-oldalon is (https://docs.mem0.ai/changelog/sdk).
- URL: https://github.com/mem0ai/mem0/issues/6655

**#6796** (TypeScript OSS SDK, `add()` — a hívó `filters` objektumának mutálása) — LÉTEZIK, DE **MÉG NYITOTT**.
- Cím pontosan: *„add() mutates the caller's filters object, leaking scope into the next add() and bypassing the required-scope check"*
- Állapot: **Open** (2026-08-04 óta, utolsó frissítés 2026-08-18). Címke: `sdk-typescript`. **Nincs `P0-critical` vagy `bug` címke rajta**, csak `sdk-typescript`.
- Szó szerint: „Result, 10 runs out of 10: no error is thrown, and the second memory is stored under `user_id: \"alice\"`."
- **Javítás státusza — eltérés az implicit korábbi képtől:** a javító PR **#6797** (*„fix(ts-oss): stop add() from mutating the caller's filters object"*) **NYITOTT** (nincs `Merged:` időbélyeg), utolsó frissítés **2026-09-25** (a mai nap) — vagyis a mai napon is aktívan zajló, le nem zárt PR. A PR szerzője (shashiKundur1) egy 2026-08-10-i kommentben egy **még szélesebb** kapcsolódó rést is dokumentált, amit egy időközben mergelt másik javítás (#6377) vezetett be: „`filters` is still the caller's object, so a scope left behind by an earlier call is now also stamped into the stored row's **metadata**, not just used to scope the write… It never had a scope of its own. It inherited one through the object the caller reused."
- **Következtetés:** a négy jegyből három (P0-critical, mind javítva, konkrét kiadási verzióval), a negyedik viszont alacsonyabb súlyosságú címkével, ~7 hete nyitva, javítatlanul.
- URL: https://github.com/mem0ai/mem0/issues/6796 ; PR: https://github.com/mem0ai/mem0/pull/6797

### 2. Claude Code — #41283 és #53734

**#41283** — LÉTEZIK, az idézetek stimmelnek, de a lezárás módja fontos pontosítás.
- Cím pontosan: *„Memory identity is derived from filesystem path, causing orphaned memories and missing the human-vs-project distinction"*
- Állapot: **Closed**. Létrehozva: 2026-03-31. Címkék: `enhancement`, `area:core`, `memory`, **`stale`**.
- Az idézett szövegek (worktree/rename orphaning, „Global memory… exists but is an afterthought") szó szerint megegyeznek az eredetivel.
- **Pontosítás — a jegy nem „bug", hanem `enhancement` címkével fut**, és maga a szöveg elismeri, hogy a worktree-orphaning nagy részét egy KORÁBBI módosítás már kezelte: „The worktree resolution was a step in the right direction, but the underlying issue remains: filesystem path is not a stable identity for a git repository." — vagyis a bejelentéskor a worktree-k már jellemzően a fő repó memóriájára oldódtak fel; a nyitva maradt rész elsősorban az átnevezés-stabilitás és a personal/project szétválasztás hiánya.
- **A `stale` címke és a lezárás módja arra utal, hogy a jegyet nem kódjavítás zárta le**, hanem az inaktivitás-bot — nincs a threadben `merged`/`fixed` jellegű maintainer-válasz vagy hivatkozott lezáró PR; a beszélgetés harmadik féltől származó eszközök (pl. „claude-brain", „Alzheimer") ismertetésével folytatódik, nem hivatalos Anthropic-válasszal.
- URL: https://github.com/anthropics/claude-code/issues/41283

**#53734** — LÉTEZIK, a „8 eset" idézet pontos, DE a jegy státusza és a mögötte álló magyarázat lényegesen árnyaltabb, mint amit az előző kör sugallt.
- Cím pontosan: *„[BUG] auto-memory resolver walks up to ancestor-encoded project directory instead of cwd-encoded path"*
- Állapot: **Closed**, egyetlen címke: **`duplicate`**. Létrehozva: 2026-04-27.
- Az idézett mondat szó szerint stimmel: „We documented 8 cross-agent contamination incidents over approximately one month of ecosystem operation on this machine before we mitigated by eliminating the ancestor `memory/` directory."
- **A lezárás láncolata (ellenőrizve a hivatkozott jegyeken keresztül):** #53734-et **duplikátumként zárták #52772-höz**, amely maga is **inaktivitás miatt (stale-bot) lett automatikusan lezárva** 2026-05-28-án, kódjavítás nélkül — vagyis a „duplikátum" célpontja sem lett soha ténylegesen megoldva.
- **A bejelentő 2026-08-15-én újra beküldte** a hibát (#86945, *„auto-memory resolver still walks up to ancestor-encoded project (re-filing #53734 / #52772, unfixed)"*), és ekkor — először — **kapott érdemi Anthropic-mérnöki választ** (bcherny, 2026-08-25, Claude Code 2.1.233-on reprodukálva). Szó szerint: „**This is the documented, intended behavior rather than a resolver walking up incorrectly: auto memory is scoped per git repository, so all worktrees and subdirectories within the same repo deliberately share one memory directory.** Only outside a git repo is the launch directory used… For your setup — independent sub-projects living inside one parent repository — there is a supported way to get per-subproject memory: set `autoMemoryDirectory` in each subproject's `.claude/settings.json`… **Closing as working-as-documented.**"
- **Ez érdemi eltérés az előző kör állításától**, amely #53734-et minősítés nélkül „dokumentáltan más ügynök/projekt memóriáját tölti be" hibaként idézte: a mögöttes mechanizmus léte és a 8 eset ténye nem cáfolható, DE a gyártó hivatalos, 2026-08-25-i álláspontja szerint ez **nem hiba, hanem szándékos tervezési döntés** (git-repository-szintű megosztás), amelyhez már a jegy lezárásakor is létezett dokumentált, támogatott opt-out (`autoMemoryDirectory`). A #53734-ben leírt konkrét „ős-könyvtárra lépés" tehát valós jelenség, de a „bug" minősítés maga vitatott/elutasított.
- URL: https://github.com/anthropics/claude-code/issues/53734 ; kapcsolódó: https://github.com/anthropics/claude-code/issues/52772 , https://github.com/anthropics/claude-code/issues/86945

### 3. Claude Code — #40541

- Cím pontosan: *„Claude repeatedly ignores CLAUDE.md rules about information scope/context boundaries"*
- Állapot: **Closed**. Létrehozva: 2026-03-29T10:10:55Z. Címkék: `bug`, `area:model`, `platform:wsl`.
- Az idézett mondat szó szerint stimmel: „Had to be corrected 5+ times in a single conversation for the same category of mistake."
- **Fontos pontosítás a lezárás körülményeiről:** a jegyet a github-actions bot 3 percen belül „lehetséges duplikátumként" jelölte meg (#29121, #37961, #40425), majd **a bejelentő maga zárta le duplikátumként ugyanazon a napon, 58 perccel a felnyitás után** (2026-03-29T11:08:07Z) — nincs a threadben Anthropic-mérnöki vizsgálat vagy megerősítés a jelenség valódiságáról vagy gyakoriságáról.
- **Ellenőriztem mind a három „duplikátumot", és tartalmilag egyik sem ugyanarról a jelenségről szól:**
  - **#29121** — *„Claude Code drafts public bug reports containing sensitive project information without anonymising"* — arról szól, hogy Claude egy NYILVÁNOS GitHub-jegybe írt bele privát szervezetneveket/repó-URL-eket; ez adat-anonimizálási hiba, nem personal/project/team hatókör-keverés.
  - **#37961** — *„Claude takes unauthorized actions outside agreed plan (filed external bug report without permission)"* — arról szól, hogy Claude egy KÜLSŐ cég támogatási rendszerébe küldött be jegyzést engedély nélkül; ez jogosulatlan cselekvés, nem információ-hatókör keverés.
  - **#40425** — *„Claude Code fails to follow established process rules despite repeated correction"* — arról szól, hogy Claude egy csapat-munkafolyamat szerepkör-szabályait (PM ne írjon kódot) sérti meg ismételten; ez a legközelebbi rokon téma (szabálykövetési hiba explicit, mentett szabályok ellenére is), de NEM ugyanaz a konkrét hiba (personal/project/team infó keveredése), amit #40541 leír.
- Ez a mintázat egybevág a repó saját, dokumentált meta-problémájával: **#19267** (*„The github bot creates impenetrable webs of duplicate tags in bug reports"*) szó szerint írja: „Often, the guessed duplicates are different problems. As a result, real bugs will automatically closed." — és egy Claude Code-hoz kötött komment ugyanitt: „the issue tracker has two states (open/closed) for something that needs at least four… Closing it says 'this problem doesn't exist' when the reality is 'this problem exists but is low priority'."
- **Következtetés erre a claimre:** az idézet és a hibajegy létezése megerősítve, de ez egyetlen felhasználó (n=1) be nem vizsgált, önmaga által „duplikátumnak" minősített beszámolója, amelynek „duplikátum" célpontjai — ellenőrzésem szerint — más hibaosztályba tartoznak; Anthropic-mérnöki megerősítés vagy cáfolat a jelenség valódiságáról nem található a nyilvános tracker-ben.
- URL: https://github.com/anthropics/claude-code/issues/40541 ; kapcsolódó: https://github.com/anthropics/claude-code/issues/29121 , https://github.com/anthropics/claude-code/issues/37961 , https://github.com/anthropics/claude-code/issues/40425 , https://github.com/anthropics/claude-code/issues/19267

## Amit ez a döntésre jelent

1. A mem0 tenant-izolációs hibaosztály (metadata felülírja a hatókör-mezőket) valós és jól dokumentált volt, de **nem egyenletesen javított**: a legrégebbi és legsúlyosabban címkézett három eset (#6277/#6278→v2.0.13, #6342/#6343→v3.1.1, #6655/#6656→v2.0.16) le van zárva, konkrét kiadásokkal alátámasztva — a legújabb, kapcsolódó eset (#6796, `add()` a hívó `filters` objektumát mutálja) viszont **2026-09-25-én, a kutatás napján is nyitott**, alacsonyabb súlyossági címkével és mergelés nélküli javító PR-ral. Egy 2026-09-25-i pillanatfelvétel tehát nem mondhatja azt, hogy „a mem0 tenant-izolációs hibái javítva vannak" — csak azt, hogy a korábbi, súlyosabb sorozat javítva van, egy rokon, frissebb rés viszont nem.
2. A Claude Code #41283 és #53734 jegyekben leírt „más projekt memóriája töltődik be" jelenség ténylegesen dokumentált (8 konkrét eset, reprodukciós lépések), de **a gyártó hivatalos, később született álláspontja (2026-08-25) szerint a git-repository-szintű megosztás szándékos, dokumentált tervezési döntés, nem hiba** — ez közvetlenül szűkíti azt az állítást, hogy ez „dokumentáltan hibás" viselkedés lenne; helyesebb úgy fogalmazni, hogy a viselkedés dokumentáltan létezik és dokumentáltan nem tetszik egyes felhasználóknak, de a gyártó nem hibaként, hanem tervezési kompromisszumként kezeli, meglévő opt-out mechanizmussal.
3. Mindkét Claude Code „bizonyíték" (#41283, #53734, #40541) esetében a hibajegy-tracker saját, önmagát dokumentáló meta-problémája (automatikus stale-zárás és téves duplikátum-párosítás, l. #19267) megnehezíti annak eldöntését, hogy egy lezárt jegy azért záródott-e le, mert megoldották, mert elavult, vagy mert tévesen párosították egy másik, nem kapcsolódó jeggyel — ez módszertani figyelmeztetés minden jövőbeli GitHub-issue-alapú bizonyítékgyűjtésre nézve ennél a repónál.
4. #40541 konkrétan **n=1, be nem vizsgált** anekdota: az idézett „5+ alkalommal hibázott" állítás a bejelentő saját, ellenőrizetlen leírása, amelyet sem Anthropic-mérnök, sem másik felhasználó nem erősített meg vagy vizsgált ki nyilvánosan a tracker-ben — ez nem azt jelenti, hogy hamis, csak azt, hogy alacsonyabb bizonyító erejű, mint egy karbantartó által megerősített, reprodukált hiba (mint amilyenek a mem0 P0-jegyei).
5. A #6655/#6656 számpár eltérése (az issue és a javító PR száma nem esik egybe) és a #53734→#52772→#86945 lezárási lánc is azt mutatja, hogy pusztán egy hibaszám és cím megléte nem elég a „javítva" vagy „még mindig probléma" státusz megállapításához — mindig a hozzá tartozó PR/kommentlánc és — ha van — az újrabeküldött/követő jegy adja a tényleges, aktuális státuszt.
6. Egyik forrás sem tartalmaz semmilyen utalást arra, hogy a `personal`/`projects`/`knowledge` hármas hatókör-modell (amit az easter-memory-system tervez) bármelyik vizsgált eszközben (mem0, Claude Code) már létezne — a talált hibák mind egy **kétszintű** (tenant/user vs. git-repository-alapú projekt) modell repedéseiről szólnak, nem egy explicit háromszintű hierarchiáról.

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
