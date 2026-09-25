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

## Meglátogatott linkek

| Cím | URL | Tier | Eszköz |
|---|---|---|---|
| MemoryAgentBench arXiv abs (submission history) | https://arxiv.org/abs/2507.05257 | T1 | web_fetch_exa |
| MemoryAgentBench v1 HTML | https://arxiv.org/html/2507.05257v1 | T1 | web_search_exa |
| MemoryAgentBench v2 HTML | https://arxiv.org/html/2507.05257v2 | T1 | web_search_exa |
| MemoryAgentBench v3 HTML | https://arxiv.org/html/2507.05257v3 | T1 | web_fetch_exa + web_search_exa |
| MemoryAgentBench v4 HTML | https://arxiv.org/html/2507.05257v4 | T1 | web_search_exa |
| ICLR 2026 proceedings — Abstract-Conference | https://proceedings.iclr.cc/paper_files/paper/2026/hash/fd1eff9dd295df50a41f2521942fa31d-Abstract-Conference.html | T1 | web_search_exa |
| ICLR 2026 proceedings — Paper PDF | https://proceedings.iclr.cc/paper_files/paper/2026/file/fd1eff9dd295df50a41f2521942fa31d-Paper-Conference.pdf | T1 | web_fetch_exa + web_search_exa |
| arXiv:2606.01435 abs (v1/v2 history, Comments mező) | https://arxiv.org/abs/2606.01435 | T1 | web_fetch_exa |
| arXiv:2606.01435 v1 HTML | https://arxiv.org/html/2606.01435v1 | T1 | web_search_exa |
| arXiv:2606.01435 v2 HTML | https://arxiv.org/html/2606.01435v2 | T1 | web_search_exa |
| COLM 2026 Lifelong Agent Workshop honlap | https://lifelongagent.github.io/ | T1 | web_search_exa |
| COLM 2026 Workshop LLA — OpenReview csoport | https://openreview.net/group?id=colmweb.org%2FCOLM%2F2026%2FWorkshop%2FLLA | T1 | web_search_exa |
| Workshop-naptár (LLA beadási határidő) | https://aiworkshoptracker.com/workshop/colm-2026-lla/ | T3 | web_search_exa |
| arXiv:2605.12978 abs (abstract szövege) | https://arxiv.org/abs/2605.12978 | T1 | web_fetch_exa |
| arXiv:2605.12978 PDF (törzsszöveg, „fails on 46%”) | https://arxiv.org/pdf/2605.12978 | T1 | web_search_exa |
| arXiv:2605.12978 v1 HTML (törzsszöveg, „down to 54%”) | https://arxiv.org/html/2605.12978v1 | T1 | web_fetch_exa + web_search_exa |
| Dylan Zhang szerzői oldal (blogösszefoglaló) | https://dylanzsz.github.io/faulty-memory/ | T1 | web_fetch_exa |
| Hao Peng publikációs lista (nincs ICML-címke) | https://haopeng-nlp.github.io/publications/ | T1 | web_fetch_exa |
| ICML 2026 hivatalos határidő-oldal | https://icml.cc/Conferences/2026/Dates | T1 | web_search_exa |
| ICML 2026 honlap | https://icml.cc/ | T1 | web_search_exa |
| mem0 OSS v2→v3 migrációs útmutató | https://github.com/mem0ai/mem0/blob/main/docs/migration/oss-v2-to-v3.mdx | T1 | web_search_exa |
| mem0 Platform v2→v3 migrációs útmutató | https://docs.mem0.ai/migration/platform-v2-to-v3 | T1 | web_search_exa |
| mem0 SDK changelog | https://docs.mem0.ai/changelog/sdk | T1 | web_search_exa |
| mem0 Node SDK v3.0.0 kiadási jegyzék (2026-04-16) | https://github.com/mem0ai/mem0/releases/tag/ts-v3.0.0 | T1 | web_search_exa |
| mem0 Dream funkció hivatalos dok. | https://docs.mem0.ai/platform/features/dream | T1 | web_fetch_exa |
| mem0 memory-evaluation.mdx | https://github.com/mem0ai/mem0/blob/main/docs/core-concepts/memory-evaluation.mdx | T1 | web_fetch_exa |
| mem0 GitHub issue #4956 (ADD-only regresszió) | https://github.com/mem0ai/mem0/issues/4956 | T1 | web_search_exa |
| Anthropic glosszárium | https://platform.claude.com/docs/en/about-claude/glossary | T1 | web_fetch_exa + web_search_exa |
| Anthropic Messages API útmutató | https://platform.claude.com/docs/en/build-with-claude/working-with-messages | T1 | web_fetch_exa |
| OpenAI Advanced usage guide | https://developers.openai.com/api/docs/guides/advanced-usage | T1 | web_fetch_exa |
| OpenAI Chat Completions API referencia (seed Deprecated) | https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create/ | T1 | web_search_exa |
| Fed Reserve working paper (Anthropic idézet másodkézből) | https://www.federalreserve.gov/econres/feds/files/2025044pap.pdf | T1 | web_search_exa |
| Zhu, Li, de Melo — ACL 2018 PDF | https://aclanthology.org/P18-2100.pdf | T1 | web_fetch_exa |
| „Daunting Dilemma” — arXiv:2309.03747 | https://arxiv.org/abs/2309.03747 | T1 | web_fetch_exa |
| „Enhancing Negation Awareness in Universal Text Embeddings” | https://arxiv.org/html/2504.00584v1 | T1 | web_search_exa |
| Qwen3-Embedding technikai jelentés | https://arxiv.org/html/2506.05176v2 | T1 | web_search_exa |
| Qwen3-Embedding GitHub repó | https://github.com/QwenLM/Qwen3-Embedding | T1 | web_search_exa |
| sentence-transformers issue #2312 (batch-méret) | https://github.com/huggingface/sentence-transformers/issues/2312 | T1 | web_fetch_exa |
| sentence-transformers PR #3892 (bfloat16 ties) | https://github.com/UKPLab/sentence-transformers/pull/3892 | T1 | web_fetch_exa |
