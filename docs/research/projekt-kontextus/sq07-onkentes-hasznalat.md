# SQ07 — Használják-e az agentek önként a memória-eszközt? A bizonyítékok

*Módszertani megjegyzés: al-ügynököket nem indítottam (degradált mód, ahogy az `_kozos.txt` engedélyezi), egyetlen szálon, szekvenciális Exa-kereséssel/-olvasással dolgoztam. Az Exa (`mcp__Exa__web_search_exa`, `mcp__Exa__web_fetch_exa`) elérhető volt, kizárólag ezt használtam; beépített WebSearch/WebFetch-et nem hívtam. A Saha-cikket (arXiv:2607.20972) teljes terjedelmében (absztrakt, §1–§8, hivatkozásjegyzék) közvetlenül lehívtam az arXiv HTML-változatából, nem másodkézből idézem.*

## Rövid válasz

Egy közvetlenül releváns, kontrollált — de egyszerzős, nem lektorált, kis mintás — kísérlet (Saha, 2026, arXiv:2607.20972) azt találja, hogy a kódoló agentek önkéntes memóriahasználata gyakorlatilag nulla: a legerősebb, előre feltöltött tárral, csatlakoztatott eszközökkel és explicit szöveges útmutatással futtatott ágban (V arm, n=1) az agent 114 körben egyetlen memóriahívást sem tett, és az öt "felszerelt, de nem célzottan táplált" futásban (B+C ágak) összesen 0–1 önkéntes írás történt. Ezt a mintázatot — hogy a modellek a rendelkezésre álló memória-/tudás-eszközöket nem, vagy csak redundánsan, hatékonytalanul használják — egy tőle független, más szerzők által készített, más feladatkörön (vállalati többplatformos munkafolyamat) futtatott, NeurIPS 2025-ön bemutatott benchmark (MEMTRACK, arXiv:2510.01353) is megerősíti. Ezen túl nincs publikált, több kódoló-CLI-t (Claude Code, Codex, Cursor, Gemini CLI, Copilot) azonos protokollal összehasonlító, kvantitatív mérés az önkéntes memória-MCP-hívási arányról — ezt a hiányt maguk a gyártók is implicit módon elismerik azzal, hogy egyik memóriarendszerük sem bízza a felidézést tisztán az agent önkéntes döntésére: az Anthropic memory tool-ja automatikusan ellenőrzi a memóriakönyvtárat feladat előtt, a GitHub Copilot Memory session indításkor automatikusan befűzi a releváns emlékeket a promptba. A felhasználói visszajelzések (GitHub-issue-k, Cursor-fórum) szisztematikusan ugyanazt a mintát mutatják: a karbantartók explicit megerősítik, hogy egy MCP-eszköz önkéntes hívását nem lehet garantálni, és a bevett munkakörüli megoldás mindig valamiféle kényszerítő mechanizmus (hook, kötelező projektutasítás, automatikus injekció). Ellenérvként egyetlen kontrollált forrás (maga a Saha-cikk) mutatja, hogy az injektálás UTÁN az agent önkéntes memóriaműveletei megnőnek ("injection begets engagement"), vagyis az önkéntes használat nem soha nem történik meg, hanem tipikusan a kényszerített felidézést *követi*, nem helyettesíti.

## 1. A Saha-cikk (arXiv:2607.20972) részletesen

### 1.1 Mit mértek pontosan

**Szerző és publikálás:** Swapnanil Saha, független kutató, „Delivery, Not Storage: Cue-Anchored Working Memory as a Harness Property for Coding Agents", arXiv:2607.20972, 2026 július. Forrás: https://arxiv.org/abs/2607.20972 , teljes szöveg: https://arxiv.org/html/2607.20972v1 (T2 — arXiv preprint, egyetlen szerző, nincs feltüntetett lektorált megjelenés).

**Modell:** minden ágban ugyanaz — „All arms run the same agent product, same model (Claude Sonnet 5, claude-sonnet-5), same prompt, same corpus SHA." (https://arxiv.org/html/2607.20972v1, §5). A repeated-compaction decay-próba (§5.7) egy másik, kisebb modellt használ: „executed by a small fast model (Claude Haiku 4.5)".

**Agent-termék:** Claude Code („the agent harness (Claude Code, an agentic coding CLI)", §4).

**Feladat:** egy valódi, natúr kódolási feladat egy rögzített (pinned) Apache Camel checkout-on (~169k indexelt chunk): „implement the reverse option for the stream-mode Resequencer EIP (Enterprise Integration Pattern)... gated by a harness-provided acceptance test that must pass unmodified plus the resequencer-scoped regression set (-Dtest='*Resequenc*Test', 42 tests)" (§5).

**Karok (arms) — pontos meghatározás (§5 táblázat):**
- A (n=3): nincs memória-felszín — kontroll.
- B (n=2): „store (cold) + tools + guidance" → delivery: **voluntary**.
- C (n=3): „store + tools + proxy, cold store" → delivery: injection (de üres tár, nincs mit injektálni).
- CS (n=1): „store seeded" → delivery: proxy injection.
- H (n=2): „store seeded" → delivery: native hooks (session-start / prompt-submit / pre-tool-use / pre-compact).
- V (n=1): „store seeded" → delivery: **voluntary** (a hookok eltávolítva; ez H kontrollja).

Összesen 9 pilot + 3 native-channel = 12 kiértékelt (graded) futás.

**"Guidance" definíciója:** a cikk ezt nem külön szakaszban definiálja formálisan, hanem a workspace-instrukciós fájlokban (pl. CLAUDE.md-szerű dokumentumok) elhelyezett, a memóriaeszköz használatára buzdító szöveges utasításokként kezeli, amelyeket a §5.2 „32 memory-guidance mentions in the workspace instruction files" számszerűsít. Vagyis a „guidance" = a projekt írásos instrukciói, amelyek a modellt a memóriaeszköz (nem kényszerített, önkéntes) használatára biztatják — ez különbözik az „injection"-től, ami a harness (nem a modell) által deterministikusan, hook- vagy proxy-mechanizmuson keresztül a kontextusba juttatott tartalom.

### 1.2 Mit talált a „voluntary" (önkéntes) ágakon

A §5.2 szakasz („Adoption: voluntary memory does not happen") szó szerint:

> „Unseeded equipped runs (B, C): voluntary memory writes 0–1 across all five runs, despite 32 memory-guidance mentions in the workspace instruction files and a verified connected tool surface. The native auto-memory directory was never created in any run."

> „The seeded-voluntary control (V) is the strongest form of the finding: same four task-relevant notes in the store as the H arms, same connected tools, same guidance — the agent made zero memory calls in 114 turns. Knowledge present in a store contributes nothing by itself."

Forrás: https://arxiv.org/html/2607.20972v1, §5.2.

Fontos módszertani megjegyzés: a headline „0 memory calls in 114 turns" szám **egyetlen futásból (V1, n=1)** származik; az unseeded B+C ágak összesített, szintén nagyon alacsony (0–1 írás/futás) eredménye 5 futáson alapul. Ezek nagyon kis mintaszámok, amit a szerző maga is a threats-to-validity szakaszban (§7) explicit elismer (l. 1.4 alább).

### 1.3 Mit talált a „delivery" (kényszerített injektálás) ágakon

A §5.3 szakasz („Mechanism: deterministic delivery, proven on two channels") két csatornán (proxy és natív hook) méri a determinisztikus injektálást:

> „Native hooks (H×2): the prompt-submit hook injected a three-note index at launch in both runs, behaviorally confirmed in H1 by the agent's first three tool calls being recalls of exactly the three injected note ids... False-alarm injections: zero in both runs, across 40 and 35 audit-logged trigger evaluations respectively."

A §5.2 egy különösen fontos, az önkéntes/kényszerített dichotómiát árnyaló megfigyelést is tartalmaz:

> „Injection begets engagement: the seeded-proxy run (CS) produced the matrix's only memory-hygiene loop (recall by id, forget of the gotcha its implementation had just obsoleted, then remember of a completion note)... Voluntary memory operations occur after and because of delivery, not instead of it."

Forrás: https://arxiv.org/html/2607.20972v1, §5.2–§5.3.

A repeated-compaction decay-próba (§5.7) ugyanezt más skálán ismétli meg: 108, illetve 138 kényszerített kompaktálás mellett a memória nélküli kar (N) 106/108 összegzésben nulla tényt tartott meg, míg az injektált tárral rendelkező kar (M) 139 auditnaplózott szállítást ért el minden egyes kompaktálás-utáni újraindításkor (138/138):

> „The daemon's audit ledger records 157 session-start evaluations, of which 139 delivered all ten facts into the run: one at every single compact-resume (138/138) plus the first phase launch."

Forrás: https://arxiv.org/html/2607.20972v1, §5.7.

### 1.4 A szerző saját korlátai (§7 — Threats to validity)

A cikk explicit, önálló szakaszt szentel a korlátoknak; a legfontosabb, a voluntary/injection kérdést közvetlenül érintő idézetek:

> „Construct... The decay probe's facts are synthetic and carry an explicit closing-phase obligation — the probe measures survival and delivery under compaction pressure, not spontaneous use."

> „Internal... The evaluated implementation and the benchmark harness share an author; mitigations: pinned corpus SHA (a543dc64), fingerprinted acceptance test, per-run launch-posture assertions archived, audit-log-gated mechanism claims, all raw transcripts, graders, and analyzers published."

> „External. One corpus (Apache Camel), one task family per experiment, one agent product, one model family; the decay probe uses a small fast model (Claude Haiku 4.5)... Results are directional evidence with asserted controls, not population estimates."

> „Conclusion. Sample sizes are small throughout (12 graded matrix runs; one gated run per decay arm, each after protocol repairs documented in the published run log). We report absolute numbers with n visible, claim direction rather than effect size."

Forrás: https://arxiv.org/html/2607.20972v1, §7.

Vagyis a szerző maga mondja ki: (1) az implementációt és a kiértékelő keretrendszert **ugyanaz a szerző** készítette (egyszemélyes, nem független validálás — csak archívált nyers adatokkal ellensúlyozva); (2) egyetlen kódbázis, egyetlen feladatcsalád, egyetlen agent-termék, egyetlen modellcsalád; (3) a mintaszámok kicsik (a legerősebb önkéntes-állítás n=1 futáson alapul); (4) az eredmények iránymutató bizonyítékok, nem populációs becslések.

### 1.5 Kód elérhetősége

A cikk „Artifact Availability" szakasza szerint minden futásarchívum, indítási-állapot-igazolás, kiértékelő szkript, a decay-próba keretrendszere és a teljes nyers tranzakciós napló nyilvánosan elérhető:

> „All run archives, launch-posture assertions, graders, the re-exploration analyzer, the decay-probe harness, and per-run transcripts are published in the Vectr repository (github.com/swapnanil/vectr) under research/proactive-gate/... and research/brain-memory/ (this paper, the analyzer, and measurement data)."

Forrás: https://arxiv.org/html/2607.20972v1, „Artifact availability" szakasz. A GitHub-repót közvetlenül is megtaláltam (a cikk markdown-változata a `research/brain-memory/delivery-not-storage.md` útvonalon van tárolva): https://github.com/swapnanil/vectr/blob/main/research/brain-memory/delivery-not-storage.md — ez megerősíti, hogy a hivatkozott repó valóban létezik és tartalmazza a cikket, de a mögöttes nyers futásadatokat (`research/proactive-gate/`) én magam nem futtattam le és nem ellenőriztem sor-szintjén.

### 1.6 Replikáció vagy vita

Célzottan kerestem citációkat, replikációkat és kritikákat („2607.20972" OR „Delivery, Not Storage" Saha cited by / citation / semantic scholar). Eredmény:
- **Semantic Scholar** keresés a szerző nevére és a cím kulcsszavaira **nem hozott ehhez a konkrét cikkhez tartozó citációs bejegyzést** — a találatok más, azonos vezetéknevű szerzők (Aytijhya Saha, Sujata Saha) teljesen más témájú munkái voltak.
- Találtam egy **másodlagos, nem tudományos** feldolgozást: Daniel Vaughan, „Delivery, Not Storage: Why Cue-Anchored Working Memory Changes How You Think About Codex CLI's Memory Stack", https://codex.danielvaughan.com/2026/07/28/... (2026-07-27, T3 — blog, a szerző maga sem tudományos intézményhez kötött, a cikket összefoglalja és Codex CLI-re alkalmazza, kritikát nem fogalmaz meg).
- Aggregátor-oldalak (alphaXiv, papers.cool, Hugging Face Papers, pubdb.com) megjelenítik a cikket, de **érdemi vita, replikáció vagy cáfolat egyiken sem szerepel** (a Hugging Face Papers „AI Summary" funkciója bejelentkezést igényel, ezt nem tudtam ellenőrizni).

**Következtetés: nem találtam bizonyítékot arra, hogy a Saha-cikk kísérletét bárki független szerző megismételte vagy tartalmilag vitatta volna.** Ez összhangban van azzal, hogy a cikk 2026 júliusában jelent meg, egyszerzős, nem lektorált preprint, és — ahogy a szerző maga is jelzi — az implementáció és a kiértékelés ugyanattól a személytől származik.

## 2. Más mérések vagy szisztematikus beszámolók

### 2.1 MEMTRACK (arXiv:2510.01353) — a legközelebbi független megerősítés

**Szerzők/kiadó:** Darshan Deshpande, Varun Gangal, Hersh Mehta, Rebecca Qian, Anand Kannapan, Peng Wang (Patronus AI + akadémiai szerzők), 2025. október. Forrás: https://arxiv.org/abs/2510.01353 ; OpenReview: https://openreview.net/pdf?id=mVxmbMng4B ; NeurIPS 2025 prezentációs diák: https://neurips.cc/media/neurips-2025/Slides/124523.pdf (T1/T2 — a NeurIPS-en bemutatott anyag léte megerősíthető, a pontos megjelenési sáv — fősáv vagy workshop — a lehívott oldalakból nem volt egyértelműen megállapítható).

Ez a benchmark **más szerzőktől, más feladatkörön (vállalati többplatformos: Slack, Linear, Git), más memória-backend-eken (Mem0, Zep)** teszteli ugyanazt a kérdést: vajon az agent önkéntesen és hatékonyan használja-e a rendelkezésre álló memóriaeszközöket. Az eredmény ugyanabba az irányba mutat, mint a Saha-cikk, bár más mérőszámmal (nem „nulla hívás", hanem „redundáns/hatékonytalan hívás"):

> „Through our findings, we show that state-of-the-art LLMs fail to perform effective multi-platform context reasoning. Furthermore, we show that LLMs cannot use memory tools effectively and using such tools increases redundancy in planning and overall tool use."

> „RQ2: Can agents use memory databases and backends such as Zep and Mem0 effectively to reason over large codebases? According to Table 3, we can observe that memory equipped LLMs fail to call memory tools effectively. LLMs with memory tools consistently display increased redundancy as well as drop in performance efficiency. As observed in the qualitative analysis above, models generally prefer repeatedly accessing information over using the memory component."

Forrás: https://arxiv.org/abs/2510.01353.

A Patronus AI saját blogbejegyzése (T3, gyártói forrás, de ugyanazok a szerzők) ezt tömöríti:

> „The memory components don't cause a significant improvement in performance. Likely because when provided with memory tools, LLMs fail to call them effectively."

Forrás: https://www.patronus.ai/blog/memtrack.

**Fontos árnyalás/eltérés a Saha-cikktől** (l. „Ellentmondások" szakasz): a MEMTRACK azt találja, hogy a modellek **inkább újra és újra hozzáférnek** az alapadatokhoz, ahelyett hogy a memóriakomponenst használnák („models generally prefer repeatedly accessing information over using the memory component") — ez nem „nulla hívás", hanem **rossz arányú, redundáns** hívásmintázat. A két forrás tehát nem azonos jelenséget ír le szó szerint, de mindkettő arra a következtetésre jut, hogy a memóriaeszköz önkéntes, hatékony használata nem történik meg megbízhatóan.

### 2.2 TriggerBench (arXiv:2606.23459) — miért nehéz az önkéntes felidézés

**Szerzők:** Tianhua Zhang, Xinjiang Wang, Qianxi Zhang, Qi Chen, Kun Li, Yaoqi Chen, DingDong Wang, Helen Meng, Yan Lu (Chinese University of Hong Kong + Microsoft Research Asia). Forrás: https://arxiv.org/abs/2606.23459 (T1/T2 — Microsoft Research társszerzőség, arXiv, 2026).

A cikk a „prospective memory" (a látens korlátra spontán, prompt nélküli emlékezés és cselekvés képessége) fogalmát különbözteti meg a „retrospective memory"-tól (explicit lekérdezésre történő visszakeresés):

> „While Large Language Models (LLMs) are increasingly deployed in long interactions, existing evaluations focus predominantly on retrospective memory (RM) via explicit queries. Prospective memory (PM), the critical ability to spontaneously recall and act on latent constraints without direct prompts, remains largely unevaluated."

> „PM is notably harder than RM: on identical contexts, RM near-saturates up to 100K tokens ($\sim$98%), while PM performance suffers a clear drop."

> „models may overfit to an 'always-remind' heuristic. Furthermore, PM accuracy degrades substantially under implicit constraints or triggers overloaded by concurrent user requests, indicating that robust PM remains an open challenge."

Forrás: https://arxiv.org/abs/2606.23459.

Ez közvetlen elméleti alátámasztást ad a Saha-cikk „voluntary lookup is the fallback, never the load-bearing path" állításának: a retrospektív (kért) memóriahasználat megbízható, de a proaktív/önkéntes (kéretlen) felidézés — ami a memória-MCP önkéntes hívásának pontosan megfelel — szisztematikusan gyengébb, és romlik a kontextushosszal.

### 2.3 Van-e mérés, ahol ugyanaz a modell önkéntes hívással vs. automatikus beadással dolgozik?

Ezt a kérdést célzottan kerestem. Az egyetlen forrás, amit találtam, amely **ugyanazt a modellt, ugyanazt az agent-terméket, ugyanazt a feladatot** kontrolláltan futtatja mindkét delivery-móddal (voluntary vs. injection), a **Saha-cikk maga** (§5, V arm vs. H/CS arms, l. 1.1–1.3 fent). Ezen kívül **NINCS FORRÁS** olyan, több kódoló-agent-terméket (Claude Code, Codex, Cursor, Gemini CLI, Copilot) azonos protokollal, azonos modellel összehasonlító, publikált kontrollált kísérletre, amely a memória-MCP önkéntes hívási arányát méri.

### 2.4 Gyártói adatok — közvetett bizonyíték a probléma elismerésére

Egyik vizsgált gyártó sem publikál explicit „önkéntes hívási arány" számot, de mindegyik termékterve **elkerüli, hogy a felidézés tisztán az agent önkéntes döntésén múljon** — ez maga is közvetett bizonyíték arra, hogy a tisztán önkéntes hívás nem megbízható.

**Anthropic memory tool** (élő dokumentáció, 2026-09-25-i állapot):

> „When the memory tool is enabled, Claude automatically checks its memory directory before starting a task. As it works, Claude stores what it learns in files under /memories and reads them back in later conversations to continue earlier work."

Forrás: https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool (T1, hivatalos dokumentáció). Megjegyzés: ez a jelenlegi szöveg már nem tartalmazza a korábbi, erősebb, csupa nagybetűs kényszerítő megfogalmazást, amit a Saha-cikk idéz („Anthropic's memory tool force-injects an all-caps directive to check memory before anything else") — ezt magam nem tudtam szó szerint visszaigazolni az élő oldalon, csak a jelenlegi, enyhébb, de tartalmilag azonos irányú („automatically checks") megfogalmazást; ez konzisztens az ELL05-jelentés (2026-09-25) hasonló, korábbi vizsgálati körben tett megfigyelésével, miszerint a gyártói dokumentáció szövege gyorsan változik.

**GitHub Copilot Memory** (hivatalos blog, 2026-01-15):

> „When an agent starts a new session, we retrieve the most recent memories for the target repository and include them in the prompt. Future implementations will enable additional retrieval techniques, such as a search tool and weighted prioritization."

Forrás: https://github.blog/ai-and-ml/github-copilot/building-an-agentic-memory-system-for-github-copilot/ (T1, hivatalos gyártói blog). Vagyis a Copilot Memory **olvasási/felidézési oldalon nem bízik az agent önkéntes döntésében** — automatikusan befűzi a memóriákat session indításkor —, míg az írás (memória létrehozása) explicit ágensi eszközhívásként van implementálva: „We implemented memory creation as a tool that agents can invoke when they discover something that's likely to have actionable [value]" (ugyanott).

Ez a mintázat — automatikus injektálás olvasásra/felidézésre, önkéntes eszköz csak írásra — megegyezik a Saha-cikk „delivery, not storage" architektúrájának alapelvével, függetlenül attól, hogy a két cél (Anthropic memory tool, GitHub Copilot Memory) egymástól függetlenül, eltérő csapatoktól, eltérő időpontban született.

## 3. Dokumentált felhasználói tapasztalat

### 3.1 GitHub-hibajegyek — karbantartói megerősítéssel

**alioshr/memory-bank-mcp #24 — „Why memory bank don't work in Claude code?"** (2025-08-18, lezárva). A felhasználó hetekig használta a Claude Code-ot anélkül, hogy a memória-MCP fájlokat írt volna:

> „I got it, I thought it's an automatic tool, but it's not... why don't you make it automatic?"

A karbantartó (a projekt szerzője) válasza:

> „One cannot enforce an MCP tool to be called by an LLM if not through a 'wrapper' (like Cline for instance). Even with an AI 'wrapper' there is no guarantee that an LLM will follow instructions. LLMs are non deterministic... Did you add the custom instructions mentioned in the docs to claude code? LLMs tend to follow them and always consult the memory bank when planning work."

Forrás: https://github.com/alioshr/memory-bank-mcp/issues/24 (T2 — elsőkézi GitHub-hibajegy, karbantartói válasszal). Ez a maintainer explicit, technikai indoklással ellátott megerősítése annak, hogy egy MCP-eszköz önkéntes hívása nem garantálható, és a bevett munkakörüli megoldás egy külső kényszerítő mechanizmus (custom instructions / wrapper).

**doobidoo/mcp-memory-service #14 — „Memory awareness in context"** (2025-03-24, „completed" néven lezárva). A felhasználó azért kért funkciót, mert az agent nem volt tisztában azzal, hogy egyáltalán van memóriája:

> „I'm wondering if there's any way to inject into the default context of each chat a selected list of topics or tags stored in memory... If there was a way to inject custom instructions 'You have a searchable memory.'"

A karbantartó válasza megerősíti, hogy a natív MCP-protokoll nem old meg ilyet, és külön eszközt épített a probléma megkerülésére:

> „While direct context injection isn't part of the MCP protocol, there are several creative ways we could implement this functionality... I've implemented a solution to this issue by creating a dedicated utility: Claude Memory Context... it allows Claude to have memory awareness at the start of conversations without modifying the MCP protocol."

Forrás: https://github.com/doobidoo/mcp-memory-service/issues/14 (T2). Ugyanennek a repónak egy másik, 2026-os hozzászólása (Exa-találat, nem külön lehívott issue) direkt összeveti a passzív vs. akció-orientált eszközleírásokat, és a mem0/OpenMemory imperatív megfogalmazását javasolja mintaként:

> „These leave it entirely up to the LLM to decide when to call, which often means they don't get called at all... OpenMemory's MCP server uses action-oriented descriptions: 'search_memory: This method is called EVERYTIME the user asks anything.'"

Forrás (Exa-keresési kivonat, github.com/doobidoo/mcp-memory-service, README/issue-szál, pontos URL a keresési találatban nem volt önállóan azonosítható — ezt T3-ként, nem önállóan visszaellenőrzött forrásként kezelem).

**mem0ai/mem0 #5413 — „Provide one-click hooks + MCP setup for Claude Code / Codex with self-hosted Mem0"** (2026-06-07, nyitott). A kérés maga is abból indul ki, hogy pusztán a statikus instrukciós fájl nem elég:

> „3. Rely only on CLAUDE.md or AGENTS.md — Static instruction files can remind the agent to use memory, but they do not provide automatic memory retrieval / persistence. Hooks are a better fit for dynamic memory injection."

Forrás: https://github.com/mem0ai/mem0/issues/5413 (T2 — nyitott hibajegy/feature request, a mem0 karbantartója triázsolta, nem vitatta az alapállítást).

### 3.2 Cursor közösségi fórum

**„A connected memory server can still do nothing in Cursor"** (2026-09-12):

> „I connected a memory MCP server to Cursor, saw the green status, and assumed the agent would start remembering. It didn't... The connection only gives the agent tools. It still needs an operating rule for when to call them."

Forrás: https://forum.cursor.com/t/a-connected-memory-server-can-still-do-nothing-in-cursor/171402 (T3 — közösségi fórumbejegyzés).

**„My AI doesnt like MCP and use its own lol... issue?"** (2025-04-14) — itt a felhasználó azt írja le, hogy hosszabb beszélgetés után az agent nem hívja a memória-MCP-t, hanem egy kitalált, saját belső „MCP memóriát" imitál a válaszában:

> „During the first few messages when I start a new chat the AI use the MCP server correctly but after a while it might forget to use it and when I tell it to use the MCP server for his memory he just makes his own ''MCP Memory''... So instead of calling the tool to access the MCP server it thinks that it can create an internal MCP memory?"

Forrás: https://forum.cursor.com/t/my-ai-doesnt-like-mcp-and-use-its-own-lol-issue/79201 (T3).

Több további Cursor-fórum bejegyzés (T3) dokumentálja a natív „Memories" funkció megbízhatatlanságát (nem feltétlenül önkéntesség kérdése, inkább regresszió/hibakérdés, de ugyanazt a felhasználói frusztrációs mintát erősíti): https://forum.cursor.com/t/tool-update-memory-not-found/132487 , https://forum.cursor.com/t/cursor-memory-doesnt-longer-work/136128 , https://forum.cursor.com/t/agents-have-lost-access-to-memory-capability/143310 . Ez utóbbiban egy Cursor-alkalmazott elismeri: „Hey, thanks for the report. This is a known recurring issue that's affecting multiple users."

### 3.3 Gyakorlati beszámoló több keretrendszerről (T3, önálló, nem lektorált)

Egy gyakorló fejlesztő „hat hónap éles használat, két agent-keretrendszer" tapasztalatát összegző GitHub-repója (nem tudományos publikáció, hanem dokumentált saját eset) a jelenséget „Ground Truth Gap"-nek nevezi:

> „This gap is systemic. It affects every memory architecture I've tested across two major agent frameworks over six months of production use. And it's not a pipeline bug — it's an identity bug... The infrastructure of memory works perfectly. The pipeline captures, stores, retrieves, and injects. But the agent doesn't use the injected context — because nothing in its identity tells it to."

Forrás: https://github.com/ClaudioDrews/ground-truth-gap (T3 — egyetlen szerző, nem lektorált, nem független validált mérés, csak beszámoló).

### 3.4 Mintázat összegzése

Mind a négy egymástól független projekt (memory-bank-mcp, mcp-memory-service, mem0, Cursor natív Memories) és a fenti gyakorlati beszámoló **ugyanazt a mintát** dokumentálja: (1) a felhasználó feltételezi, hogy a csatlakoztatott memória-eszközt az agent automatikusan, önkéntesen használni fogja; (2) tapasztalja, hogy nem így történik; (3) a karbantartó vagy a közösség válasza mindig valamilyen **kényszerítő mechanizmus** (custom instructions/CLAUDE.md, hook, wrapper, identitás-dokumentum-szintű szabály) felé mutat, nem pedig „várj, a modell úgyis megtanulja". Ez négy egymástól **független forrásból** (más MCP-szerver, más karbantartó, más felhasználói bázis) konvergáló mintázat, ami önmagában — bár mindegyik T2/T3 szintű, anekdotikus forrás — erősíti a Saha-cikk és a MEMTRACK kontrollált eredményeinek külső érvényességét.

## 4. Ellenérvek: mikor működik jól az önkéntes használat, és mitől függ?

Nem találtam olyan kontrollált mérést, amely azt mutatná, hogy az önkéntes memória-MCP-hívás **önmagában, kényszerítő mechanizmus nélkül** megbízhatóan működik. Az alábbi források azonban konkrét tényezőket azonosítanak, amelyek **javítják** (de nem oldják meg teljesen) a helyzetet:

**(a) Akció-orientált, imperatív eszközleírás.** A doobidoo/mcp-memory-service közösségi javaslata konkrét összehasonlítást tesz a passzív és az akció-orientált eszközleírás között, az OpenMemory (mem0) mintájára hivatkozva, amely explicit „EVERYTIME" (mindig) megfogalmazást használ a leírásban a „lehet használni" helyett — ez azonban egy **javaslat**, nem egy előtte-utána mért, kontrollált eredmény (l. 3.1, T3).

**(b) Injektálás utáni önkéntes folytatás.** A Saha-cikk egyetlen, de kontrollált megfigyelése szerint az injektálás **kiváltja** a további önkéntes memóriaműveleteket, míg pusztán a tudás tárban léte (injektálás nélkül) nem:

> „Voluntary memory operations occur after and because of delivery, not instead of it."

Forrás: https://arxiv.org/html/2607.20972v1, §5.2 (l. 1.3 fent). Ez azt sugallja, hogy az önkéntes használat nem „soha nem történik meg" jelenség, hanem jellemzően egy előzetes, nem-önkéntes felidézési eseményhez kötött láncreakció.

**(c) Explicit, konkrét horgony (anchor) a mikor-triggerre.** A TriggerBench szerint a modellek proaktív felidézése akkor sikeresebb, ha a kiváltó feltétel explicit, de ennek ára van: túl erős, általános „mindig emlékeztess" instrukció túltriggerelést (hamis riasztást) okoz:

> „models struggle to maintain situational awareness without explicit anchors (implicit vs. explicit constraints)... models may overfit to an 'always-remind' heuristic."

Forrás: https://arxiv.org/abs/2606.23459 (l. 2.2 fent). Ez azt jelzi, hogy a „mikor" kérdésre adott válasz (explicit horgonyok) egy trade-off: javítja a felidézést, de rontja a pontosságot/precizitást.

**(d) Identitás-szintű, kötelező hierarchia-szabály (anekdotikus).** A „Ground Truth Gap" beszámoló szerint az injektált memóriablokkok explicit rangsorolása a modell identitás-dokumentumában (pl. „injected context > memory API results > model training knowledge") mérhető viselkedésváltozást hozott a gyakorlatban tesztelt két keretrendszerben:

> „The fix is not in the pipeline. The fix is in the agent's identity documents — the files that define who the agent is and how it should operate... With the hierarchy, injected memory becomes authoritative. The agent stops rediscovering."

Forrás: https://github.com/ClaudioDrews/ground-truth-gap (T3 — egyetlen szerző saját, nem kontrollált, nem független validálású megfigyelése, előtte-utána mérőszám nélkül).

**(e) Operatív szabály/„loop" kézzel felírva a promptba (Cursor-közösségi tanács).** A Cursor-fórum bejegyzés konkrét, felhasználó által kidolgozott szabályokat ad meg arra, mikor kell keresni/menteni, de maga a szerző is jelzi, hogy ez pótlás, nem megoldás a mögöttes problémára: „The connection only gives the agent tools. It still needs an operating rule for when to call them" (l. 3.2 fent, T3).

**Egy gyártói termék marketing-állítása, amit nem tudtam függetlenül ellenőrizni:** a `codex-agent-mem` MCP-szerver README-je azt állítja, hogy megfelelő konfiguráció mellett az agent proaktívan, emlékeztetés nélkül használja a memóriát: „Once configured, the agent should use codex-agent-mem proactively when continuity matters. You should not need to repeat 'use the memory MCP' every few turns." (https://github.com/MarceloCaporale/codex-agent-mem, T3). Ehhez az állításhoz **semmilyen mért adatot, benchmarkot vagy előtte-utána összehasonlítást nem közöl a repó** — önmagában áll a fentebb dokumentált, ellentétes irányú, jóval szélesebb körű tapasztalati mintázattal szemben.

## Ellentmondások

- **„Nulla hívás" (Saha) vs. „redundáns, de nem nulla hívás" (MEMTRACK).** A Saha-cikk fő állítása, hogy a legerősebb önkéntes ágban (V, n=1) az agent **egyetlen** memóriahívást sem tett 114 körben. A MEMTRACK ezzel szemben azt találja, hogy a memóriaeszközzel felszerelt modellek **igenis hívják** a memóriakomponenst, csak redundánsan és hatékonytalanul: „LLMs with memory tools consistently display increased redundancy as well as drop in performance efficiency" (https://arxiv.org/abs/2510.01353). A két forrás nem közvetlenül cáfolja egymást — más feladatkör (egyetlen kódolási feladat vs. vállalati többplatformos QA), más memória-architektúra (cue-anchored, harness-vezérelt tár vs. Mem0/Zep query-time retrieval) —, de a „soha nem hívja" és a „túl gyakran, rosszul hívja" két, tartalmilag eltérő hibaüzemmód, amit érdemes megkülönböztetni, nem egy jelenségként kezelni.
- **Marketing-állítás (codex-agent-mem: „nem kell emlékeztetni") vs. a dokumentált mintázat túlnyomó többsége** (Saha, MEMTRACK, alioshr/memory-bank-mcp, doobidoo/mcp-memory-service, mem0, Cursor-fórum), amely szerint az önkéntes, kényszerítés nélküli használat megbízhatatlan. A codex-agent-mem állítását semmilyen közölt mérőszám nem támasztja alá — ellentétben áll a többi, forrásolt tapasztalattal, de mivel egyik oldal sem kontrollált, publikált mérés (a codex-agent-mem README esetében), ezt inkonzisztenciaként, nem cáfolatként rögzítem.
- **Az Anthropic memory tool dokumentációjának jelenlegi (2026-09-25) szövege** („Claude automatically checks its memory directory before starting a task") enyhébb megfogalmazású, mint amit a Saha-cikk idéz („force-injects an all-caps directive"). Nem tudtam eldönteni, hogy ez a Saha-cikk pontatlansága, vagy a dokumentáció azóta megváltozott (ez utóbbi valószínűbb, az ELL05-jelentés hasonló megfigyelést tett más idézetre nézve ugyanezen az oldalon) — erre nézve NEM ELDÖNTHETŐ, melyik forgatókönyv áll fenn.

## Amire NINCS forrás

- **NINCS FORRÁS** olyan publikált, kontrollált kísérletre, amely azonos protokollal, azonos feladaton **több** kódoló-agent-terméket (Claude Code, Codex, Cursor, Gemini CLI, Copilot) egyszerre hasonlítana össze az önkéntes memória-/tudás-MCP-hívási arány szempontjából.
- **NINCS FORRÁS** semmilyen gyártó (Anthropic, OpenAI, Google, GitHub/Microsoft) által nyilvánosan közölt, konkrét százalékos „önkéntes hívási arány" számra a saját memóriarendszerükre nézve; a fellelt gyártói számok (pl. Anthropic 84%/39%, l. ELL05) teljesítmény- és token-megtakarítási mutatók, nem hívási gyakoriság.
- **NINCS FORRÁS** a Saha-cikk (arXiv:2607.20972) független tudományos citációjára, replikációjára vagy formális szakmai cáfolatára — a Semantic Scholar-keresés nem hozott találatot, és a fellelt másodlagos feldolgozás (codex.danielvaughan.com) sem tudományos, sem kritikai jellegű.
- **NINCS FORRÁS** kontrollált mérésre a Gemini CLI vagy a GitHub Copilot CLI önkéntes memória-MCP-hívási arányáról; a Copilot Memory esetében csak a tervezési döntést (automatikus injektálás olvasásra) dokumentáltam, mért hívási arányt nem.
- **NEM ELDÖNTHETŐ**, hogy a doobidoo/mcp-memory-service repóban talált „OpenMemory vs. mcp-memory-service tool description" összehasonlítás (3.1 (a) pont) pontos GitHub-issue-URL-je melyik — az Exa-keresés kivonatolt szöveget adott, önálló, közvetlen lehívással nem tudtam megerősíteni a pontos issue-számot vagy dátumot; ezt a forrást ezért T3-ként, alacsonyabb megbízhatósággal kezelem, és második független forrással nem tudtam megerősíteni.

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
