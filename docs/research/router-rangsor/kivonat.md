# Router és keresési rangsor — kivonat

*2026-09-05. Forrás: `.research/router-rangsor/` — 47 archivált forrás-pillanatkép, 69 kivont állítás. A pillanatképek törlésre kerülnek; ez a fájl az, ami megmarad.*

A kutatás két tervezési ötletet vizsgált egy markdown-alapú, projekt-szintű agent-memóriarendszerhez: (1) hogy egy LLM automatikusan, emberi jóváhagyás nélkül átemelhet-e tudást egyik projektből a másikba ("router"), és (2) hogy egy összekötött projekt találatainak kötelezően a saját projekt találatai után kell-e következniük a keresésben. Alább a forrásokban ténylegesen leírtak, idézve.

## 1. A router-ötlet

### 1.1 Amit a valós rendszerek csinálnak — és amit nem

Hat rendszert néztünk át kifejezetten arra, van-e bennük LLM-ítéleten alapuló, hatókörök közötti tartalom-propagáció. Egyikben sem volt.

**Basic Memory** — hivatalos dokumentáció, a legkeményebb izolációs kijelentés a korpuszban:
> „Notes in one project do not appear in another. Relations in one project cannot link to notes in a different project."

Az átvitel kizárólag kézi, szkriptelt read→write→delete művelet:
> „There is no built-in cross-workspace 'Move to…' action yet. MCP doesn't expose an atomic cross-project or cross-workspace move."

**Mem0** — a hatókör-azonosítók (user_id/agent_id/app_id/run_id) célja kifejezetten az elkülönítés: „By tagging each write and query with the right identifiers, you can prevent data from mixing between them." A saját, cross-repo demó blogbejegyzésük (vendor blog) a legközelebbi analógia a router-ötlethez, de **húzó (pull), nem toló (push) modell**: Agent A rögzíti a változást, de Agent B csak akkor jut hozzá, ha „searches memory before coding, discovers the field change" — addig nem történik semmi, amíg B maga rá nem kérdez.

**Letta** megosztott memóriablokkjai nem másolást csinálnak, hanem egyetlen objektumot osztanak meg:
> „Shared memory blocks let multiple agents access and update the same memory. When one agent updates the block, all others see the change immediately."

Itt nincs mit „eldönteni", mert nincs második példány. Ezzel szemben a Letta **sleep-time (dreaming)** ágense saját memórián belül tényleg gépi ítélettel, jóváhagyás nélkül ír:
> „Select Agent reviews before applying to have your agent review and revise proposed memory updates in a second background conversation. This uses more model tokens and does not ask you for approval."

Ez az egyetlen valódi „gép dönt, ember nem" precedens a korpuszban — de **egy ágens saját memóriáján belüli konszolidáció**, nem két független projekt közötti átvitel.

**Zep** minden felhasználóhoz külön gráfot épít automatikusan („Zep automatically constructs a temporal knowledge graph for each of your users") — a dokumentáció nem említ felhasználók/csoportok közötti tényátvitelt.

Egyetlen forrás használja a „propagation" szót két hatókör között: egy 2026-os, gyártóhoz kötődő preprint (arXiv 2606.24535, MemClaw/ArgusFleet), amely „97.5% fleet-sibling visibility rate"-et jelent. De ez **láthatósági szabály egy hierarchiában** (agent-local → team-shared → tenant-global), nem LLM-ítélet alapján történő másolás két egyenrangú, független hatókör között. A jegyzeteink szerint a forrás „self-evaluated, no external validation" — gyártó-közeli önértékelés.

**Ez a rész a bizonyíték egyik legerősebb pontja, de pontosan kell fogalmazni, mit jelent.** Ez nem azt jelenti, hogy megmérték és rossznak találták a router-mintát. Azt jelenti: **hat célzottan megnézett rendszer közül egyikben sincs ilyen**, tehát nincs mire alapozni a tervet mint bevett gyakorlatra. „Nincs precedens" — nem „mért kudarc".

### 1.2 Az ítélet minősége, ami a router alapja lenne

A routernek meg kellene bíznia egy LLM ítéletében: „ez a tudásdarab máshol is hasznos". Erre van mérés, méghozzá lektorált forrásokból.

Arabzadeh & Clarke (SIGIR 2025, peer-reviewed, Table 2, TREC DL 2020/2021 adatokon, GPT-4o/LLaMA3.2-3B/Mistral-7B, temperature 0):

| Modell | Prompt írója | Bináris κ | Graded (0–3) κ | Páros κ |
|---|---|---|---|---|
| GPT-4o | LLM | 0,434 | 0,215 | 0,849 |
| GPT-4o | ember | 0,270 | 0,215 | 0,578 |
| LLaMA 3.2-3B | LLM | 0,303 | 0,033 | 0,439 |
| Mistral-7B | LLM | 0,405 | 0,008 | 0,574 |

A kisebb, helyben futtatható modellek graded-ítélete gyakorlatilag nulla egyezés. A cikk saját megfogalmazása: „graded relevance judgments are highly sensitive to prompt variations."

Az UMBRELA (Bing-stílusú GPT-4o értékelő; Upadhyay et al. 2024, és a TREC 2024 RAG Track nagy vizsgálata, Upadhyay et al., 301 téma, 77 futás, 19 csapat) négyfokú skálán κ ≈ 0,31–0,37 — a szerzők szerint „fair agreement". Ugyanez a rendszer **rendszerfutás-szinten** kiváló: Spearman ρ 0,9729–0,9923. De a nagy TREC-vizsgálat pontosít: ez csak „run-level effectiveness"-re igaz, és még ott is „UMBRELA achieves only 'coarse-grained differentiation' and cannot reliably distinguish among similarly-performing systems, particularly for nDCG@20". Topikszinten a korreláció „weakens significantly". A torzítás iránya dokumentált: „often rates passages as more relevant than NIST assessors, partly due to inferences a human might deem unwarranted" — vagyis hamis pozitív irányba torzít.

**Forráskritikai megjegyzés:** mindkét UMBRELA-forrás automatikus összefoglaló-lekérővel készült, „not a byte-exact copy" jelzéssel — a számok valószínűleg helyesek, de nem szó szerint ellenőrzött PDF-idézetek.

Az áthelyezhetőség tovább romlik nem betanításhoz hasonló kérdéseken: „Mistral-24B with DPO training drops from 76.57% (weak, seen) to 68.56% (weak, unseen) — an 8.01 percentage point decline" (arXiv 2509.23542, T4 preprint).

Konkrétan a „ez az új infó felülírja-e a régit" döntésre — ami a router feladatával rokon — a MemoryAgentBench (T4, ICLR 2026 beadvány, tehát még nem lektorált) szerint: „All methods fail on the multi-hop situation (with achieving at most 7%)". Egy másik, 2026 júniusi preprint (arXiv 2606.01435) megmutatja, hogy ha az LLM-ítéletet egy determinisztikus szabállyal (Python `max(serial_number)`) váltják ki, a pontosság a HippoRAG-v2 54,0%-áról 78,0%-ra (gpt-4o-mini) illetve 94,8%-ra (gpt-4o) nő **egylépéses** feladaton; többlépéses (multi-hop) feladaton 7%-ról 30,2%-ra. Ugyanez a forrás jelzi: egy másik benchmarkon (LongMemEval) a determinisztikus módszer csak döntetlent hoz, nem javulást — a hatás nem univerzális.

Egy lektorált módszertani cikk (Soboroff, Information Retrieval Research Journal 2025) elvi ellenvetést tesz a számok mellé: ha egy LLM állítja elő az „igazi" relevancia-címkét, az a modellt teszi mérhetetlen felső korláttá — „you are declaring the model to represent ideal performance", és „retrieval and evaluation are the same problem". Nem szám, hanem érv arra, miért nehéz egyáltalán megmérni egy LLM saját ítéletének minőségét, ha ugyanolyan modell dönt is, ítél is.

### 1.3 A hiba terjedése — mérve

| Támadás | Forrás (típus) | Mérgezett arány | Mért hatás |
|---|---|---|---|
| PoisonedRAG | USENIX Security 2025, lektorált (arXiv 2402.07867) | 5 szöveg / milliós tudásbázis | „90% attack success rate" |
| AgentPoison | NeurIPS 2024, lektorált (arXiv 2407.12784) | „less than 0.1%" a tudásbázisból | „higher than 80%" siker, „less than 1%" jóindulatú teljesítményromlás |
| MINJA | arXiv 2503.03704, lektorált-track preprint, csak lekérdezésen át, direkt hozzáférés nélkül | — | ISR 95,6–100% (adathalmaztól függően); **ASR (tényleges viselkedés-módosítás) csak 57,0–98,9%, adathalmazonként nagyon eltérő**; haszonromlás −10,0-től +0-ig |

A MINJA-nál fontos a pontosítás, amit a szintézis elmosott: az „injekciós siker" (bejegyzés bekerül a memóriába, >90-100%) és a „támadási siker" (a bejegyzés ténylegesen rossz döntést vált ki, 57–99%) két különböző szám, és utóbbi az egyik adathalmazon (MIMIC-III) alig több mint fele.

Valós eset: a Cisco 2026 áprilisi jelentése (MemoryTrap) szerint egy npm postinstall-hook útján bejuttatott payload „overwrites every project's memory (MEMORY.md files… at ~/.claude/projects/*/memory/MEMORY.md) and global hooks configuration". A payload öngyógyító: kikapcsolt automemory mellett is „silently re-enables the auto-memory feature every time users launch Claude" egy shell-alias révén. Az OWASP ASI06 (Memory and Context Poisoning) rovatvezetője ezt nevezi meg kanonikus valós példaként: „The issue is not just that the model saw something malicious once. The issue is persistence." Anthropic válaszlépése: „As of Claude Code v2.1.50, Anthropic included mitigation removing user memories from the system prompt."

### 1.4 Amit ez NEM támaszt alá

- Nem azt találtuk, hogy a routert kipróbálták és rosszul teljesített — **senki nem csinálja**, tehát nincs is mit mérni rajta közvetlenül. A „nincs precedens" és a „mérve rosszabb" két különböző erősségű állítás; itt csak az előbbi áll.
- A poisoning-számok (90%+, <0,1%) mind **más rendszerekre** (RAG-tudásbázis, autonóm ügynök-memória) vonatkoznak, nem az itt tervezett markdown-router konkrét megvalósítására — analógiaként, nem közvetlen mérésként számítanak.
- A jóváhagyási fáradtság valós, jól dokumentált mintázat (alert fatigue, automation bias — Goddard et al. 2012, JAMIA, lektorált), de a konkrét „73 jóváhagyás, a 68.-nál csúszik át a hiba" történet egy enciklopédia-oldal (aipatternbook.com, T4, nem elsődleges tudományos forrás) **illusztratív, nem mért** anekdotája.
- A MemoryAgentBench és a 2606-os freshness-cikk friss preprintek (utóbbi ICLR 2026 beadványként jelölve) — még nem mentek át teljes lektoráláson.

## 2. A keresési rangsor ötlete

### 2.1 Amit a keresőmotorok és termékek csinálnak

Öt keresőmotort és hat terméket néztünk át. Egyikben sincs beépített, kötelező „saját forrás mindig előre" szabály.

- **Elasticsearch** cross-cluster search: „This document's _index parameter doesn't include a cluster name. This means the document came from the local cluster" — a hivatalos példa helyi és távoli találatot **egyetlen, `_score` szerint globálisan rendezett listában** mutat. Az `indices_boost` létezik, de opt-in: „useful when hits coming from some indices matter more than hits from other" — súlyozás, nem kikényszerített sorrend.
- **Azure AI Search** scoring profile-jai egy indexen belüli súlyozásra szolgálnak; több index forrás-alapú egyesítésére nincs dokumentált primitív.
- **Vespa** federációja explicit rábízza az összefésülést az alkalmazásra: „This is not an easy task, and we will not attempt to solve it here." A hivatalos `ResultBlender` példakód nem sorrendet állít, hanem **küszöböt**: a másodlagos (news) forrás találata csak akkor kerül be, ha `hit.getRelevance().getScore() > 0.7`.
- A klasszikus federált IR-irodalom (Lu & Callan, ECIR 2005, CORI-stílus) kifejezetten a forrásfüggő pontszámok **forrásfüggetlenné normalizálását** célozza — az ellenkező irányba mutat, mint egy forrás-alapú sorrend.
- **OpenSearch** fórumbejegyzés (T6, közösségi) szerint az alapértelmezett cross-cluster keresés „results determined solely by relevance scoring across clusters" — klaszterenkénti kiegyenlítést csak `collapse` mezővel, workaroundként lehet elérni.
- **Confluence** minden space-en átível: „Confluence looks for content in all spaces (including personal spaces)". A hivatalos rangsor-képlet három tényezőt kombinál (tartalomtípus × mezőtípus × frissesség) — **space-hovatartozás nincs köztük**. Egy 2006 óta nyitott, 162 szavazatos kérés éppen a jelenlegi space-re szűkítést kéri — a kevert lista a vitatott, de bevett alapértelmezés.
- **GitHub** explicit hatókör-minősítőt kér (`repo:`, `org:`, `enterprise:`), alapértelmezett keverék nélkül. **Slack** egyetlen kevert listát ad `in:` szűrővel. **Notion**-ban a Teamspace csak utólagos szűrő, az alapkeresés a teljes workspace-en fut.

### 2.2 A mérés, ami van — és amit nem lehetett megmérni

A FeB4RAG (preprint, arXiv 2402.11891) a naiv, round-robin forrás-keverést hasonlítja a relevancia szerint csökkenő sorrendbe rendezetthez: „preferences for responses generated by the RAG pipeline that rely on best-fed occur across all datasets; we note this is not the case for naive-fed." Ez adathalmazonként következetes, minőségi preferenciakülönbség — de a rögzített szöveg szerint **konkrét számszerű nDCG-érték nem szerepel** a lekért oldalon: „specific numerical nDCG or precision scores for different merging strategies are not provided in the paper's quantitative results." A hatás iránya tehát dokumentált, a nagysága nem.

Arra, hogy mennyibe kerülne egy **kötelezően merev** „saját projekt mindig előre" szabály, nincs mérés sehol a korpuszban — mert egyetlen vizsgált rendszer sem alkalmazza, tehát nincs mit mérni rajta. Ez ugyanaz a „nincs precedens, nem mért kudarc" szerkezet, mint a routernél.

### 2.3 Amit ez NEM támaszt alá

A bizonyíték nem azt mutatja, hogy valaki kipróbálta a merev forrás-sorrendet, és rosszabb lett. Azt mutatja, hogy a merev sorrend fel sem merül tervezési opcióként az iparágban — a rendelkezésre álló minták küszöbön (Vespa) vagy tiszta pontszám-normalizáláson (CORI) alapulnak, súlyozott előny formájában (`indices_boost`), sosem kikényszerített sorrendben.

## Amire ez a kutatás nem ad választ

**Ellenőriztük, és nem létezik / nem elérhető:**
- A Wikipédia bot-jóváhagyási szabályzata (en.wikipedia.org) nem volt lekérhető ebben a környezetben („cache-only", nem hozható le élőben) — az SQ-03 (emberi jóváhagyás mintái) egyik tervezett forrása kimaradt.
- Egy ACM-cikk („Limitations of LLM-as-a-Judge for Expert Knowledge Tasks", IUI 2025) 403-as fizetőfal mögött van.
- Egy Microsoft Research monográfia a federált keresésről csak erősen összefoglalva volt lekérhető, idézésre alkalmatlan minőségben — kimaradt.
- Az OpenSearch hivatalos cross-cluster search dokumentációja JS-renderelt oldal, nem volt lekérhető; helyette csak egy közösségi fórumbejegyzés (alacsonyabb megbízhatóságú forrás) szolgált SQ-05 OpenSearch-részéhez.

**Elfogyott a keret / nem futott le:**
- Nem futott önálló ellenőrző ügynök: a `06-evidence-table.csv` `verdict` és `confidence` oszlopa mind a 69 sorban üres. Csak a linkek élő állapotát ellenőrizték (mind a 47 élő), az idézetek szó szerintiségét nem ellenőrizte független fél.
- A jóváhagyási fáradtságra nincs kemény szám — csak analóg terület (alert fatigue, automation bias) és egy nem mért anekdota.
- Egy Mem0-hoz kapcsolódó CVE-számot (CVE-2026-31245) kerestünk, de nem sikerült megerősíteni élő forrásból — lehet téves vagy nem létező azonosító.
- Több cikk pontos számait csak automatikus összefoglaló-lekérőn keresztül sikerült megszerezni (mindkét UMBRELA-forrás, MemoryAgentBench, a determinisztikus freshness-cikk, FeB4RAG), „not byte-exact" jelzéssel — valószínűleg helyes, de nem szó szerint ellenőrzött számok.

## Mire használtuk

Három élő tervezési döntés támaszkodik erre a kutatásra:

1. **Nincs projekt-összekötés automatikus tartalom-átvitellel.** Ha B-nek szüksége van A tudására, keresésben lát bele, nem kap másolatot (mem0 pull-modell). Ami mindkettőnek kell, az a közös `tudas/` gyökérbe kerül, emberi jóváhagyással (Letta megosztott blokk mintája).
2. **A hasonlóság mérését egy éjszakai karbantartó folyamat végzi, nem élő LLM-ítélet soronként.** Ez közvetlenül az 1.2 pont mérési eredményeire épül: az egyedi, tétel-szintű LLM-ítélet gyenge és felfelé torzít; ha a mérés téved, vagy a determinisztikus alternatíva várt előnye nem jön be, ezt a döntést kell újragondolni.
3. **A rangsorolás küszöbön alapul, nem kikényszerített sorrenden** — a Vespa `ResultBlender` mintája. Ha később kiderül, hogy mégis kell forrás-alapú súlyozás, az `indices_boost`-szerű, opt-in súlyként vezethető be, nem visszaállított merev sorrendként.

Mindhárom döntés annyira erős, amennyire az alapja: az első kettő „nincs precedens + mérve gyenge ítélet" — magas bizonyosságú negatív eredmény; a harmadik „nincs precedens" — magas bizonyosságú, de a küszöb konkrét számértékére (hol legyen a levágás) itt nincs mérés, azt saját adaton kell majd kalibrálni.
