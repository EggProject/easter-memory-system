# ELL05 — Az eszközhasználati és kontextus-mérések ellenőrzése

*Módszertani megjegyzés: al-ügynököket nem indítottam (degradált mód, ahogy az `_ell_kozos.txt` engedélyezi), egyetlen szálon, szekvenciális Exa-kereséssel/-olvasással dolgoztam. Az Exa (`mcp__Exa__web_search_exa`, `mcp__Exa__web_fetch_exa`) elérhető volt, kizárólag ezt használtam; beépített WebSearch/WebFetch-et nem hívtam. Minden idézetet a saját magam által lehívott elsődleges forrásból (arXiv PDF/HTML, hivatalos doksi, GitHub issue, NeurIPS/ICLR oldal) ellenőriztem — nem vettem át az SQ06 idézeteit ellenőrzés nélkül.*

## Verdikt-összefoglaló

| # | Állítás | Verdikt | Egy mondat |
|---|---|---|---|
| 1 | Nincs közvetlen, kontrollált mérés arra, hogy egy rövid session-eleji szöveg mennyivel növeli a memória-eszköz önkéntes használatát | **RÉSZBEN** | A szűk, sablonos "hány bejegyzés van" szövegre valóban nincs ilyen mérés, de van egy célzott kereséssel megtalált, közvetlenül releváns kontrollált kísérlet (Saha, 2026, arXiv:2607.20972), amely explicit szöveges instrukció ("guidance") melletti önkéntes memóriahasználatot mér — és nullát talál —, amit az SQ06 nem talált meg. |
| 2 | Az alap eszközhívási hajlandóság modellcsaládonként 7% és 98% között szór, a promptolás ezt csak durván korrigálja | **RÉSZBEN** | A három hivatkozott tanulmány létezik és az SQ06-ban idézett mondatok szó szerint stimmelnek, de a "7%-tól 98%-ig" összegző szám egyik forrásban sem szerepel — az egyetlen tényleges, forrásolt tartomány 7%–83% (arXiv:2608.25198); a "98%" eredete nem azonosítható, minden jel szerint az SQ06 saját szintézishibája. |
| 3 | Léteznek a "Lost in the Middle", a "context rot" (Anthropic, Chroma, két arXiv) és egy 2026-os null-eredmény, és azt mondják, amit az SQ06 állít | **IGAZOLVA** | Mind az öt forrás (Liu et al. TACL 2024, Chroma 2025-07-14, arXiv:2510.05381, arXiv:2606.29718, Zenodo 2026-06-18) létezik, és az idézett mondatok szó szerint megtalálhatók bennük — a hosszhatás és a 150k tokenig tartó null-eredmény egyaránt valósak. |
| 4 | GSM-IC (ICML 2023): "legfeljebb 18%" konzisztensen megoldható — a szám és a hatókör egyezik | **IGAZOLVA, kontextussal** | A mondat szó szerint megtalálható a PMLR-cikkben, de a 18%-os szám kifejezetten a GSM-IC (GSM8K + egy irreleváns mondat) feladatra és a 2023-as Codex/GPT-3.5 modellekre vonatkozik, nem általános, mai modellekre extrapolálható állítás. |
| 5 | Egy Codex-hibajegy szerint elavult memória felülírta a friss AGENTS.md-utasítást | **IGAZOLVA** | A github.com/openai/codex/issues/39223 jegy létezik, nyitott (2026-08-18), és a szó szerint idézett szöveg pontosan megegyezik a jegy tartalmával — de ez egy felhasználói bejelentés, az OpenAI nem erősítette meg hivatalosan. |
| 6 | MINJA (NeurIPS 2025) és a ChatGPT-memória 2024-es esete (Rehberger) léteznek, és a beadott memóriatartalmon át érkező nem kívánt utasításokról szólnak | **IGAZOLVA** | A MINJA-cikk (NeurIPS 2025 poszter, San Diego, 2025-12-05; arXiv:2503.03704) és Rehberger 2024-05-22-i blogbejegyzése is létezik, a szó szerint idézett mondatok — beleértve a MINJA 1. ábra feliratát is — pontosan megtalálhatók bennük. |
| 7 | Az Anthropic "84%/39%" száma: honnan van, mit mér | **IGAZOLVA, kontextussal** | A szám az Anthropic 2025-09-29-i hivatalos blogbejegyzéséből (context-management) származik, önbevallott, nem publikált módszertanú belső eval; a 84% és a 39% két KÜLÖNBÖZŐ mérésből jön (a 84% kizárólag a context editing token-megtakarítása egy 100-fordulós web-keresési evalon, a 39% a memória+context editing kombináció teljesítményjavulása egy másik, meg nem nevezett agentikus-keresési evalon) — az SQ06-ban idézett kritikai elemzés (dreaming.press) létezik és pontosan idézi, de ez maga is AI (Claude-opus) által írt, emberi szerkesztő által ellenőrzött blogbejegyzés, nem független emberi szakértői/újságírói forrás. |

## Állításonként

### 1. Van-e kontrollált mérés a session-eleji szöveg → önkéntes eszközhasználat hatásra?

Célzottan újra kerestem erre ("controlled experiment measuring effect of session-start reminder text on voluntary LLM agent memory tool invocation rate"). A szűk keretezésre (egy sablonból generált, "N bejegyzés van" jellegű mondat izolált, A/B-szerű hatása) továbbra sem találtam közvetlen mérést — ebben egyetértek az SQ06-tal.

Viszont találtam egy, a kérdéshez ennél is közelebb álló, kontrollált kísérletet, amit az SQ06 kihagyott:

> „A controlled evaluation on a naturalistic coding task showing that voluntary memory use is ∼zero even when the store is pre-seeded with task-relevant knowledge (0 memory operations in 114 turns)... Our own controlled runs replicate this naturalistically and extend it to the strongest case: an agent whose store was pre-seeded with facts directly relevant to its task, with connected tools and explicit guidance, made zero memory calls in 114 turns (§5.2). Voluntary memory does not happen."

Forrás: Swapnanil Saha, „Delivery, Not Storage: Cue-Anchored Working Memory as a Harness Property for Coding Agents", arXiv:2607.20972 (2026 július), https://arxiv.org/abs/2607.20972 , https://arxiv.org/pdf/2607.20972 (T2 — arXiv preprint, egyetlen független szerző, nem lektorált, nincs második független megerősítés).

A kísérleti elrendezés kifejezetten tartalmaz egy "voluntary + guidance" kart (B és V ág: "store (cold) + tools + guidance voluntary" / "store seeded proxy injection voluntary (hooks stripped)"), vagyis pontosan azt méri kontrolláltan, hogy egy explicit szöveges instrukció ("guidance") önmagában mennyire váltja ki az önkéntes eszközhasználatot — és nullát talál. Ez nem ugyanaz a beavatkozás, mint az SQ06-ban feltételezett "N bejegyzés van a memóriában" sablonmondat, de módszertanilag pontosan az a fajta kontrollált, célzott kísérlet, aminek a hiányát az SQ06 kimondta. Mivel egyetlen, nem lektorált, független kutatói preprintről van szó, önmagában nem elég egy "IGAZOLVA/MEGDŐLT" döntéshez, de az SQ06 "amire nincs forrás" kijelentését pontosításra szorulóvá teszi: legalább egy, a kérdéshez közeli, publikált kontrollált mérés létezik, csak nem talált rá az előző kör.

*(Mellékesen: ugyanez a keresés több iparági/blog jellegű, kontrollálatlan vagy más kérdést mérő forrást hozott — pl. GitHub „agent-memory-lab" benchmark, arXiv:2607.09493 „Shared Selective Persistent Memory" — ezek memória-STRATÉGIÁKAT hasonlítanak össze (van/nincs memória, RAG vs. teljes history), nem a session-eleji szöveg hatását az önkéntes hívásra, ezért nem tekintem őket a kérdésre közvetlenül válaszoló forrásnak.)*

### 2. A "7%–98%" tartomány — létezik-e, egyeznek-e a számok?

Mindhárom hivatkozott tanulmányt közvetlenül elértem és az SQ06-ban szereplő idézeteket szó szerint ellenőriztem.

**WHEN2TOOL** (arXiv:2605.09252v2) — a Finding 1 és Finding 2 idézetek szó szerint stimmelnek:

> „Finding 1: Models default to tool overuse. Under the Default (⋆) setting in Prompt-only baselines, models make 2,100–4,400 total tool calls across the 2,250-task single-hop test set, more than one calls per task. Even on easy tasks, Qwen3-1.7B makes 864 tool calls out of 750 easy tasks..."

> „Finding 2: Prompt engineering reduces tool calls indiscriminately, and hard tasks pay a disproportionate price... On Qwen3-4B-Instruct, the cost is −17.3 on easy but reaches −42.4 on hard, meaning hard tasks lose 2.5× more accuracy per saved call."

Forrás: https://arxiv.org/pdf/2605.09252v2 , https://arxiv.org/abs/2605.09252 (T1, arXiv preprint, 2026). Ez a cikk NEM ad meg semmilyen egyszerű "7%–X%" call-rate tartományt — az ő mérőszámai tool-call darabszámok és accuracy-cost-per-saved-call, nem call rate %.

**Tunable Tool-Call Rates via Representation Steering** (arXiv:2608.25198) — az egyetlen forrás, amely tényleges %-os baseline call-rate tartományt ad:

> „baseline call rates span both tool-underuse and tool-overuse, from 0.07 on Qwen3-4B to 0.83 on the 30B MoE."

Forrás: https://arxiv.org/html/2608.25198v1 , https://arxiv.org/abs/2608.25198 (T1, arXiv, 2026-08-25). Ez **7%–83%**, nem 7%–98%.

**ToolFailBench** (arXiv:2607.04686) — a "89 percentage points" idézet stimmel:

> „the best reaches 86.33% Clean Tool-Use Rate... Llama-3.1-70B and Qwen2.5-72B differ by 89 percentage points on control-task accuracy."

Forrás: https://arxiv.org/abs/2607.04686 , https://ar5iv.labs.arxiv.org/html/2607.04686 (egyetlen szerző — Harsh Soni, UC Berkeley —, arXiv preprint, nem lektorált; az SQ06 T1-ként jelölte, ami inkonzisztens azzal, hogy más, hasonlóan nem lektorált arXiv-preprinteket [pl. a Zenodo null-eredményt] T2-ként kezelt ugyanabban a jelentésben — ez önmagában módszertani pontatlanság, nem tartalmi tévedés). A cikk fejlécében szereplő "Keywords: Machine Learning, ICML" félrevezető lehet: a cikknek nincs igazolt lektorált konferencia-megjelenése, ezt semmilyen elérhető metaadat (arXiv absztrakt-oldal) nem támasztja alá.

**A "z=−19.9, p<10⁻⁸⁰" statisztikát** a lehívott absztrakt- és bevezető-szövegben nem találtam meg szó szerint (feltehetően egy mélyebb, statisztikai szekcióban van) — ezt nem tudtam külön ellenőrizni, így erre nézve NEM ELDÖNTHETŐ.

**Következtetés:** a három forrás és az SQ06 bennük szereplő szó szerinti idézetei valósak és pontosak, de az SQ06 saját összegző mondata ("tág skálán mozog, 7%-tól 98%-ig") egyik forrásban sem szerepel ebben a formában. A ténylegesen forrásolható tartomány **7%–83%**. A 98% eredete nem azonosítható — feltehetően szintézis közben keletkezett pontatlanság.

### 3. Lost in the Middle, context rot, 2026-os null-eredmény

Mind az öt forrást közvetlenül elértem.

**Lost in the Middle** (Liu et al., TACL 2024, DOI 10.1162/tacl_a_00638): a cikk létezik, lektorált (Transactions of the ACL, MIT Press), absztraktja szó szerint tartalmazza:

> „we observe that performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts, even for explicitly long-context models."

Forrás: https://aclanthology.org/2024.tacl-1.9/ (T1, lektorált).

**Chroma "Context Rot"** (2025-07-14): létezik, és a mondat szó szerint egyezik:

> „We demonstrate that even under these minimal conditions, model performance degrades as input length increases, often in surprising and non-uniform ways."

Forrás: https://www.trychroma.com/research/context-rot (T2, iparági kutatóműhely, nem lektorált, de 18 modellen, kontrollált, széles körben idézett).

**„Context Length Alone Hurts LLM Performance Despite Perfect Retrieval"** (arXiv:2510.05381): létezik, az absztraktban szó szerint szerepel:

> „even when models can perfectly retrieve all relevant information, their performance still degrades substantially (13.9%–85%) as input length increases but remains well within the models' claimed lengths."

Forrás: https://arxiv.org/abs/2510.05381 , https://arxiv.org/html/2510.05381 (T1, arXiv). A 13,9%–85% szám pontosan egyezik az SQ06 idézetével.

**„Diagnosing and Mitigating Context Rot in Long-horizon Search"** (arXiv:2606.29718): létezik, a "premature termination" fogalom és a hossz-korreláció szó szerint szerepel:

> „under extensive context, models give up or provide uncertain incorrect answers long before exhausting the context window... the premature termination rate is positively correlated with context length."

Forrás: https://arxiv.org/abs/2606.29718 , https://arxiv.org/html/2606.29718 (T1, arXiv, négy vezető modellen, három benchmarken).

**2026-os null-eredmény** (Zenodo, Jagtap): létezik, és a számok pontosan egyeznek:

> „we observe no measurable length-driven degradation on our probes for the four models tested (gpt-5.5, gpt-5.4, gpt-5.4-mini, claude-sonnet-4-6) up to 150,000 tokens... Across the 12,570-trial registered grid, 7,330 present-needle trials had 48 failures (accuracy 0.9935)."

Forrás: https://doi.org/10.5281/zenodo.20753848 (T2, „Preprint - not peer reviewed", 2026-06-18, egyetlen szerző — Sahil Jagtap, George Mason University). Fontos: a szerző maga is jelzi, hogy tiszta, szintetikus needle-in-haystack feladatról van szó, és „we cannot determine its contribution in real multi-turn agentic workflows" — vagyis ez nem cáfolja az agentikus kontextusban mért romlást, csak azt mutatja, hogy legújabb modelleken, tiszta lexikai feladaton nem mindig jelentkezik.

Az Anthropic „Effective context engineering for AI agents" (2025-09-29) blogbejegyzését ebben a körben nem hívtam le újra közvetlenül (URL-je jól ismert, korábbi köreinkben már szerepelt) — erre nézve a verdikt a korábbi ellenőrzésre támaszkodik, önállóan nem verifikáltam újra.

**Összegzés:** mind az öt állítás IGAZOLVA — a források léteznek, és pontosan azt mondják, amit az SQ06 állít róluk.

### 4. GSM-IC "legfeljebb 18%"

A PMLR-en közzétett, lektorált ICML 2023-as cikk PDF-jét közvetlenül elértem, és a mondat szó szerint megtalálható benne:

> „In particular, among the original problems that can be solved by baseline prompts with greedy decoding, no more than 18% of them can be consistently solved for all types of irrelevant information, showing that the large language model is easily distracted and produces inconsistent predictions when adding a small amount of irrelevant information to the problem description."

Forrás: Shi et al., „Large Language Models Can Be Easily Distracted by Irrelevant Context", ICML 2023, https://proceedings.mlr.press/v202/shi23a.html , PDF: https://proceedings.mlr.press/v202/shi23a/shi23a.pdf (T1, lektorált).

**Fontos kontextus, amit az SQ06 nem emelt ki eléggé:** a 18%-os szám a GSM-IC adathalmazra (GSM8K-alapú, egyetlen irreleváns mondattal kiegészített általános iskolai matekfeladatok) és a cikkben használt, 2023-as modellekre — Codex (`code-davinci-002`) és GPT-3.5 (`text-davinci-003`) — vonatkozik. A cikk maga is írja: „We use Codex (code-davinci-002) and GPT-3.5 (text-davinci-003) in the GPT3 model family to evaluate state-of-the-art prompting techniques on GSM-IC." Ez nem mai frontier-modelleken mért, általános "18%" — a szám és a hatókör technikailag egyezik az SQ06 állításával, de annak általánosíthatósága mai modellekre nyitott kérdés, amire ez a cikk önmagában nem ad választ.

### 5. Codex-hibajegy: elavult memória felülírta a friss AGENTS.md-t

A jegyet közvetlenül elértem a GitHubon:

> „Codex Desktop loaded both the global `~/.codex/AGENTS.md` and the repository `AGENTS.md` into the task context, but the agent ignored a distinctive current global rule and instead followed stale validation-gate guidance recovered from persistent memory... The problem is instruction precedence/compliance: stale memory was treated as more authoritative than the current, explicitly loaded global `AGENTS.md`."

Forrás: „Codex Desktop loads global AGENTS.md but stale memory overrides its explicit rule", https://github.com/openai/codex/issues/39223 — állapot: **open**, létrehozva: 2026-08-18, szerző: „Lyrnic" (T2, elsőkézi, de nem hivatalosan megerősített felhasználói hibajelentés; az OpenAI a jegyben nem szólalt meg, csak egy másik felhasználó kommentált rajta).

Az idézet szó szerint egyezik. Fontos, hogy ez egy **nyitott, nem lezárt, nem az OpenAI által megerősített** jegy — tehát dokumentált *esetleírásként*, nem hivatalosan elismert *hibaként* kell kezelni.

### 6. MINJA és a Rehberger-féle ChatGPT-eset

**MINJA**: a NeurIPS 2025-ös poszter valóban létezik (San Diego, 2025. december 5., Exhibit Hall C,D,E #1412), és megtaláltam az arXiv-verziót is (arXiv:2503.03704), amelynek teljes szövegében — az 1. ábra feliratában — szó szerint szerepel az SQ06-ban idézett mondat:

> „When the victim user submits a victim query, the stored malicious records are retrieved as a demonstration, misleading the agent to generate bridging steps and target reasoning steps through in-context learning."

Forrás: arXiv:2503.03704, https://arxiv.org/pdf/2503.03704 ; NeurIPS 2025 poszter/absztrakt: https://proceedings.neurips.cc/paper_files/paper/2025/hash/42a97bbd9844d2bf68596730af80bcdf-Abstract-Conference.html , https://nips.cc/virtual/2025/loc/san-diego/poster/118152 (T1, lektorált, NeurIPS 2025).

**Rehberger / ChatGPT 2024**: a blogbejegyzés létezik, 2024-05-22-i keltezéssel, és a leírt támadási módok (Connected Apps / Google Drive, kép-feltöltés, böngészés) megegyeznek az SQ06-ban leírtakkal:

> „a Google Doc that is referenced in a conversation can indeed write memories... this works well, and persists into future conversation and chat sessions."

Forrás: Johann Rehberger, „ChatGPT: Hacking Memories with Prompt Injection", https://embracethered.com/blog/posts/2024/chatgpt-hacking-memories/ (T1, elsődleges kutatói közlés, 2024-05-22).

Mindkét forrás valós, és pontosan azt állítja, amit az előző kör (SQ06) nekik tulajdonít: a beadott/tárolt memóriatartalmon keresztül nem kívánt, a felhasználó által nem szándékolt utasítások/adatok kerülhetnek be az agent tartós memóriájába, kizárólag közvetett interakción (lekérdezésen, dokumentumon, böngészésen) keresztül.

### 7. Az Anthropic "84%/39%" szám

Az anthropic.com/news/context-management oldalt (2025-09-29) közvetlenül elértem. A pontos szöveg:

> „combining the memory tool with context editing improved performance by 39% over baseline. Context editing alone delivered a 29% improvement. In a 100-turn web search evaluation, context editing enabled agents to complete workflows that would otherwise fail due to context exhaustion—while reducing token consumption by 84%."

Forrás: https://www.anthropic.com/news/context-management (T1, hivatalos, 2025-09-29).

**Mit mér pontosan és hogyan kell értelmezni:**
- A **84%** a **context editing** (nem a memória-eszköz) token-megtakarítását méri egy **konkrét, 100-fordulós web-keresési evaluationön**, olyan alap-futáshoz képest, amely kontextus-kimerülés miatt elbukna.
- A **39%** a **memória-eszköz + context editing kombinációjának** teljesítményjavulását méri egy **másik, "internal evaluation set for agentic search"** nevű, nyilvánosan nem specifikált belső evalon.
- A két szám tehát két különböző metrika, két különböző (és nyilvánosan nem dokumentált) belső eval-készleten — nem ugyanannak a jelenségnek két oldala, csak ugyanabban a bekezdésben szerepelnek. Egyik szám mögött sincs publikált módszertan, statisztikai szignifikancia-teszt vagy külső reprodukció — önbevallott gyártói szám.

Az SQ06 „Ellentmondások" szakaszában idézett kritikai elemzést is közvetlenül elértem és a rá hivatkozó idézetek pontosak:

> „Both figures are real. Neither says the model got smarter — they measure escaping a wall your agent may never hit"; „The 39% is a completion-rate gain on tasks long enough to exhaust context — on short tasks the delta collapses toward zero."

Forrás: „The 84% and the 39%: What Anthropic's Context-Management Numbers Actually Measure", https://dreaming.press/posts/anthropic-context-editing-84-percent-39-percent-numbers-examined.html (2026-07-27).

**Fontos, az SQ06-ból hiányzó részlet:** ennek a "független kritikai elemzésnek" a byline-ja **„By Priya Sundaram · claude-opus · reviewed by a human editor"** — vagyis ez maga is egy Claude (claude-opus) modell által írt, emberi szerkesztő által átnézett blogbejegyzés egy AI-tartalmakra szakosodott oldalon ("dreaming.press"), nem egy hagyományos újságírói vagy akadémiai szakértői forrás. Ez nem teszi hamissá az érvelését (a logikai pont — hogy két különböző mérésről van szó, más-más alapon — magukból az Anthropic-számokból is levezethető), de az SQ06 T3-as, "kritikai elemzés"-ként való jellemzése félrevezető lehet, ha valaki ezt emberi, független szakértői véleményezésnek olvassa.

## Amit ez a döntésre jelent

- A "nincs kontrollált mérés a session-eleji szöveg hatására" állítás pontosításra szorul: van legalább egy releváns, de gyenge (egyszerzős, nem lektorált) kontrollált kísérlet (arXiv:2607.20972), amely azt találja, hogy explicit szöveges "guidance" önmagában nem váltja ki megbízhatóan az önkéntes memóriahasználatot — ez inkább óvatosságra int a "rövid emlékeztető szöveg elég lesz" feltevéssel szemben, mint hogy megerősítené azt.
- A "7%–98%" tartomány a jelentésben pontatlan; a forrásokból igazolható tartomány 7%–83%. Ezt a konkrét számpárt érdemes javítani vagy törölni a végleges anyagból, a mögöttes kvalitatív állítás (erős modell-/családfüggés, a promptolás durva korrekciós ereje) viszont jól alátámasztott, három egymástól független forrásból.
- A hosszhatás ("Lost in the Middle", "context rot") és az azt megkérdőjelező 2026-os null-eredmény egyaránt valós, jól idézett kutatás — a kettő közötti ellentmondás (agentikus/hosszú sessionök vs. tiszta lexikai NIAH-feladatok legújabb modelleken) továbbra is nyitott kérdés, nem félreértés.
- A GSM-IC 18%-os szám technikailag pontos, de 2023-as modellekre vonatkozik; a mai frontier-modellekre való átvitele nem bizonyított ezzel a forrással.
- A Codex-jegy és a MINJA/Rehberger-kockázatok valósak, de eltérő megbízhatósági szinten: a Codex-jegy egy meg nem erősített felhasználói bejelentés, míg a MINJA lektorált akadémiai eredmény és a Rehberger-eset elsődleges, technikailag részletezett biztonsági kutatói közlés.
- Az Anthropic 84%/39% számpár valós, de két különböző mérésből származó, önbevallott, nem auditált belső eval-eredmény; a rá vonatkozó "kritikai elemzés" forrás maga is AI-generált tartalom, ami csökkenti a bizonyító erejét mint "független szakértői vélemény".
- Módszertani mellékészrevétel: az SQ06 jelentés tier-jelölése (T1/T2/T3) nem teljesen konzisztens — legalább egy egyszerzős, nem lektorált arXiv-preprintet (ToolFailBench) T1-ként kezel, miközben hasonló státuszú másik preprinteket (pl. a Zenodo null-eredményt) T2-ként.

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
