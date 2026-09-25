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

## Meglátogatott linkek

| Cím | URL | Tier | Eszköz |
|---|---|---|---|
| open-second-brain — Releases lista | https://github.com/itechmeat/open-second-brain/releases | T1 | web_fetch_exa |
| open-second-brain v1.54.0 release | https://github.com/itechmeat/open-second-brain/releases/tag/v1.54.0 | T1 | web_fetch_exa |
| open-second-brain v1.40.0 release | https://github.com/itechmeat/open-second-brain/releases/tag/v1.40.0 | T1 | web_fetch_exa |
| open-second-brain v0.9.0 release | https://github.com/itechmeat/open-second-brain/releases/tag/v0.9.0 | T1 | web_fetch_exa |
| open-second-brain v0.21.0 release | https://github.com/itechmeat/open-second-brain/releases/tag/v0.21.0 | T1 | web_fetch_exa |
| open-second-brain v1.52.0 release | https://github.com/itechmeat/open-second-brain/releases | T1 | web_fetch_exa |
| open-second-brain README (raw) | https://raw.githubusercontent.com/itechmeat/open-second-brain/main/README.md | T1 | web_fetch_exa |
| open-second-brain help-text.ts (blob) | https://github.com/itechmeat/open-second-brain/blob/main/src/cli/brain/help-text.ts | T1 | web_fetch_exa |
| open-second-brain help-text.ts (raw, teljes) | https://raw.githubusercontent.com/itechmeat/open-second-brain/main/src/cli/brain/help-text.ts | T1 | web_fetch_exa |
| open-second-brain docs/how-it-works.md (main) | https://github.com/itechmeat/open-second-brain/blob/main/docs/how-it-works.md | T1 | web_fetch_exa |
| open-second-brain docs/how-it-works.md (commit 7e6a5672) | https://github.com/itechmeat/open-second-brain/blob/7e6a5672/docs/how-it-works.md | T1 | web_search_exa |
| open-second-brain src/core/brain/dream.ts | https://github.com/itechmeat/open-second-brain/blob/7e6a5672/src/core/brain/dream.ts | T1 | web_search_exa |
| open-second-brain src/core/brain/types.ts | https://github.com/itechmeat/open-second-brain/blob/7e6a5672/src/core/brain/types.ts | T1 | web_search_exa |
| Anthropic — Dreams (felhasználói dok.) | https://platform.claude.com/docs/en/managed-agents/dreams | T1 | web_fetch_exa + web_search_exa |
| Anthropic — Dreams (API-referencia) | https://platform.claude.com/docs/en/api/beta/dreams | T1 | web_fetch_exa |
| Claude by Anthropic blog — dreaming bejelentés | https://claude.com/blog/new-in-claude-managed-agents | T1 | web_fetch_exa |
| Harvey — Legal Agent Benchmark blog | https://www.harvey.ai/blog/introducing-harveys-legal-agent-benchmark | T1 | web_search_exa |
| Claude customer case study — Harvey | https://claude.com/customers/harvey | T1 | web_search_exa |
| Let's Data Science — Harvey 6x kritikus elemzés | https://letsdatascience.com/blog/anthropic-dreaming-claude-managed-agents-self-improving-may-6 | T2 | web_search_exa |
| VentureBeat — Anthropic dreaming | https://venturebeat.com/technology/anthropic-introduces-dreaming-a-system-that-lets-ai-agents-learn-from-their-own-mistakes | T2 | web_search_exa |
| LinkedIn — Claude Managed Agents launch poszt | https://www.linkedin.com/posts/claude_new-in-claude-managed-agents-activity-7457833168184762369-T9n2 | T2 | web_search_exa |
| AIntelligenceHub — Claude dreaming | https://aintelligencehub.com/articles/claude-dreaming-may-2026 | T3 | web_search_exa |
| anthropics/claude-code GitHub Issue #47959 | https://github.com/anthropics/claude-code/issues/47959 | T1 | web_fetch_exa |
| Claude Code hivatalos memória-dokumentáció | https://code.claude.com/docs/en/memory | T1 | web_search_exa |
| HFurther/claude-code-stable — AutoDream (nem hivatalos) | https://github.com/HFurther/claude-code-stable/blob/main/docs/en/memory/03-autodream.md | T3 | web_search_exa |
| mem0 blog — Dream bejelentés | https://mem0.ai/blog/dream-background-memory-consolidation-for-ai-agents | T1 | web_fetch_exa |
| mem0ai/mem0 — dream skill SKILL.md | https://github.com/mem0ai/mem0/blob/main/integrations/mem0-plugin/skills/dream/SKILL.md | T1 | web_fetch_exa |
| mimir-mem-core — consolidate.rs (docs.rs) | https://docs.rs/mimir-mem-core/latest/src/mimir_core/consolidate.rs.html | T1 | web_fetch_exa |
| letta-ai/letta-code PR #1856 | https://github.com/letta-ai/letta-code/pull/1856 | T1 | web_fetch_exa |
| Letta blog — Sleep-time Compute | https://www.letta.com/blog/sleep-time-compute/ | T1 | web_fetch_exa |
| engrxiv — Active Dreaming Memory (preprint oldal) | https://engrxiv.org/preprint/view/5919 | T1 | web_search_exa |
| engrxiv — Active Dreaming Memory (teljes szöveg) | https://engrxiv.org/preprint/download/5919/9826 | T1 | web_search_exa |
| ResearchGate — Active Dreaming Memory | https://www.researchgate.net/publication/398306877_Active_Dreaming_Memory_Biologically-Inspired_Episodic_Consolidation_for_Lifelong_Learning_in_Autonomous_Agents | T2 | web_search_exa |
| GreaterWrong/LessWrong — Sleeping Machines (ADM hivatkozás) | https://www.greaterwrong.com/posts/TajwK45XBiNEumfim/sleeping-machines-why-our-ai-agents-still-behave-like | T2/T3 | web_search_exa |
| Level Up Coding — Claude Code /dream cikk | https://levelup.gitconnected.com/your-ai-coding-agent-now-needs-sleep-heres-what-dream-actually-does-81d32977ec25 | T3 (nem elsődleges, nem használt döntő bizonyítékként) | web_fetch_exa |
| Ogham MCP blog — konszolidáció-történet | https://ogham-mcp.dev/blog/memory-consolidation-lineage/ | T3 (kizárva — belső dátum-ellentmondás) | web_search_exa |
