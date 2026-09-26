# ELL02 — A Jev pontossági és illeszkedési állításainak ellenőrzése

*Módszer: kizárólag Exa (`web_search_exa`, `web_fetch_exa`), a `_ell_kozos.txt` és a `deep-web-research` skill elvei szerint (elsődleges forrás, szó szerinti idézet, ellenőrzött hivatkozás). Alügynök-indítást ez a környezet nem tett lehetővé — egyszemélyes, de kizárólag Exa-t használó, elsődleges forrásokra törekvő kutatás, degradált módban. A `sq02-pontossag.md` és `sq05-illeszkedes.md` teljes szövegét elolvastam; egyetlen idézetüket sem vettem át ellenőrzés nélkül, minden állításnál magam nyitottam meg az elsődleges (vagy — ahol az nem volt elérhető — a legközelebbi) forrást.*

## Verdikt-összefoglaló

| # | Állítás | Verdikt | Egy mondat |
|---|---|---|---|
| 1 | A „67,8% vs 74,1%" / „61,8% vs 79,1%" a TypeSafe saját 4-workflow tesztjéből van, „agreement" két másik modellel, nem emberi igazsággal | **IGAZOLVA** | A TypeSafe saját blogja és az `evals.typesafe.ai` oldal közvetlenül, elsődleges forrásból megerősíti, hogy a referencia „a GPT-6 Astra és a Claude Fable 5.1 (high thinking) válaszainak átlaga", nem ground truth, és a TechSpot cikk szó szerint idézi a négy számot. |
| 2 | Kalibráció: nincs TypeSafe-saját ECE/Brier; független mérések CLINC150 ECE 0,02, Banking77 0,05–0,09, 6-osztályos emóció 0,35; 16-modelles összevetésben Sonnet 5 jobban kalibrált | **RÉSZBEN** | Az, hogy a TypeSafe nem publikált saját ECE/Brier-t, és hogy egy 16-modelles, közvetlenül ellenőrzött független mérésben (WotAI) a Claude Sonnet 5 jobban kalibrált volt, igaz — de a „CLINC150 0,02 / Banking77 0,05–0,09 / emóció 0,35" számhármas végső forrása egy nem elérhető Reddit-poszt („ASSAY-001"), amelyet az egyetlen fellelt „megerősítés" egy önmagával is ellentmondásban álló, matematikailag képtelen (1-nél nagyobb ECE, jövőbeli évszámok) tartalmú oldalon (cephalochromoscope.net) keresztül idéz — ez a konkrét számlánc megbízhatatlan. |
| 3 | Többosztályos pontosság: SNIPS 97,9%; japán 9-osztály 76,8% (tanított enkóder 88,8%); TweetTopic 87,5%; Banking77 76–80% (máshol 81,0% vs Claude Opus 5 84,4%) | **IGAZOLVA** | Mind a négy számpár közvetlenül, elsődleges forrásból (dev.to/aitejiu, wpnews.pro, OpenRouter cookbook, OpenRouter blog) megerősíthető, szó szerint egyezik az idézettel; egy másik független mérés a SNIPS-en 97,14%-ot kapott, ami a normál mérési szórás keretein belül van. |
| 4 | Magyarra nincs forrás a Jev pontosságára | **IGAZOLVA** (a „nincs forrás" állítás megdöntése nem sikerült) | Célzott, ismételt magyar nyelvű keresés is csak általános hírmegjelenéseket (Mobilissimo.hu, nerdgeek.hu, LavX News) talált, amelyek angol elsődleges forrásra hivatkoznak és nem közölnek magyar nyelvi teljesítményadatot; magyar nyelvű Jev-benchmark továbbra sem található. |
| 5 | A TypeSafe kilencpontos hibamód-listája és a Noul/Choice ellentétes válasz publikált példája szó szerint létezik | **IGAZOLVA** | A `docs.typesafe.ai/model-jaggedness/jev-1.13` oldal közvetlenül, elsődleges forrásból lekérhető, és tartalmazza mind a 9 hibamódot, mind a pontos Noul (0,22) / Choice (yes 0,01, no 0,99, confidence 0,97) és a refund+not_refund=1,19 példát. |
| 6 | „Jev-Mem" arXiv-cikk (2026-09-21, UT Dallas, LoCoMo) létezik | **IGAZOLVA** | Az `arXiv:2609.23986` közvetlenül lekérve pontosan a leírt cikk: Dongming Jiang, Yi Li, Bingzhe Li (UT Dallas), 2026-09-21, LoCoMo 0,777 pontszám, 11,0%-os relatív javulás, 6,6×-os gyorsulás, 36,7%-os késleltetés-csökkenés. |
| 7 | A mem0, Zep, Letta, Basic Memory hivatalos anyagaiban nincs Jev-integráció | **IGAZOLVA** | Kiterjedt célzott keresés (hivatalos dokumentáció, GitHub-repó, összehasonlító cikkek) a négy rendszer egyikében sem talált Jev- vagy TypeSafe-említést. |
| 8 | „Cheap Verifiers, Large Blind Spots" cikk létezik, és a leírt módon a gyenge ellenőrző vakfoltjáról szól | **IGAZOLVA** | `arXiv:2609.01345` (Dushyant Rajput, 2026-09-01) közvetlenül lekérve, az absztrakt szó szerint tartalmazza az idézett állítást a vakfolt (β 0,12→0,55) növekedéséről a tanuló-modell képességével. |
| 9 | Nincs forrás arra, mennyit javít egy frontier LLM első döntése után egy gyors modell utólagos ellenőrzése | **RÉSZBEN** | Számszerű haszonra továbbra sincs forrás, de a keresés talált publikált termékeket (MrJev „Foreman", jev-code `jev_check`, egy Claude Code/Codex felülvizsgálati munkafolyamat), amelyek pontosan ezt a sorrendet (Claude Code/Codex dönt/ír kódot előbb, Jev ellenőrzi utólag) írják le — vagyis a minta létezik, csak számszerűsítve nincs mérve. |

## Állításonként

### 1. A „67,8% vs 74,1%" és „61,8% vs 79,1%" — TypeSafe saját mérése, „agreement", nem ground truth

Az elsődleges forrás — a TypeSafe hivatalos bejelentő blogja — közvetlenül lekérhető és szó szerint tartalmazza a módszertant:

> „We made a new type of evaluation to measure how well AI works within code. We don't optimize for a ground truth classification […] Instead, we assume there is a correct compute graph (a 'workflow' represented in code) and use the predictions of the largest, smartest, and most expensive external models as reference probabilities. Rephrased: every model gets the same workflow. We test how they compare to the average of the smartest models (in this case, Astra and Fable)."
(https://typesafe.ai/blog/introducing-system-one-models-and-jev, T1)

> „We use the average of GPT-6 Astra and Fable 5.1 as the reference answer, which biases answers towards OpenAI and Anthropic's models." (uo., T1)

A blogban hivatkozott, korábban (`sq02`-ben) `CRAWL_NOT_FOUND` hibát adó „workflow evals site" (`evals.typesafe.ai`) ebben a körben közvetlenül lekérhető volt, és megerősíti ugyanezt:

> „Instead of debating the correctness of the harness and labels, we assume that the code is correct, and measure against the current smartest large models. For this eval, the reference labels are generated via an average of the responses of GPT-6 Astra and Claude Fable 5.1, both at high thinking, answering every question in the harness."
(https://evals.typesafe.ai/, T1)

A TechSpot cikk közvetlenül lekérve, szó szerint idézi a négy számot:

> „The benchmarks are TypeSafe's own. The company skipped public leaderboards. Its workflow tests score models by agreement with the averaged answers of GPT-6 Astra and Fable 5.1, not against verified ground truth. By that measure, Jev reached about 67.8% agreement overall versus 74.1% for GPT-5.6 Sol. It came close on customer service (76% versus 78.3%) and fell well behind on invoice processing (61.8% versus 79.1%)."
(https://www.techspot.com/article/3172-meet-jev/, T2)

**Verdikt: IGAZOLVA**, most már két elsődleges (T1) forrással (a TypeSafe saját blogja és saját eval-oldala) is alátámasztva, a `sq02`-ben elérhetetlen elsődleges oldal ebben a körben sikeresen lekérhető volt.

### 2. Kalibráció

**Amit a WotAI 16-modelles, közvetlenül lekért mérése megerősít** (T2, elsődleges):

> „Sonnet 5 posted an ECE of 0.062, roughly half Jev's 0.121, with better accuracy and more willingness to sit in the middle. On the metric TypeSafe's entire pitch rests on, a general-purpose frontier model won."
(https://wotai.co/blog/typesafe-jev-vs-claude-haiku-tested, T2)

Ezt egy másik, közvetlenül lekért forrás (TrueStandard, 108 állítás) árnyalja — más adathalmazon a különbség eltűnik:

> „Expected calibration error came out at 0.066 for Jev, 0.061 for Gemini 3.1 Flash Lite and 0.067 for Claude Haiku 4.5. At 108 items that is a three-way tie."
(https://truestandard.ai/blog/jev-accuracy-tested, T2)

**A konkrét „CLINC150 ECE 0,02 / Banking77 0,05–0,09 / 6-osztályos emóció 0,35" számhármas eredete — súlyos megbízhatósági probléma.** A `learnjev.com` (T3) e számokat egy „ASSAY-001 — pre-registered calibration study (independent)" nevű, linkelt URL nélküli forrásra vezeti vissza:

> „A pre-registered study, 8,576 responses | Calibrated on CLINC150 (ECE 0.0204). Not calibrated on Banking77 (ECE 0.0936, systematically overconfident)."
(https://learnjev.com/concepts/calibration, T3)

Az egyetlen fellelt hely, ahol ez az „ASSAY-001" Reddit-poszt konkrétan idézve van, egy `cephalochromoscope.net` nevű oldal — ez azonban **belsőleg ellentmondásos és matematikailag lehetetlen adatokat közöl**, ami erősen gyanússá teszi a teljes láncot:

> „An earlier independent run posted to r/LLMDevs (**ASSAY-001**, pre-registered protocol, blind third-party scoring) reported ECE 0.0204 on CLINC150 and **1.1936** on Banking77, calling the latter 'systematically overconfident in the lower confidence bins'."
(https://cephalochromoscope.net/96e26264-f9ec-4bba-9173-05dde157f933, nem besorolható/T3)

> „An earlier independent run posted to r/LLMDevs (**ASSAY-021**, pre-registered protocol, blind third-party scoring) reported ECE 0.0204 on CLINC150 or **0.0936** on Banking77, calling the latter 'systematically overconfident in the lower confidence bins'."
(https://cephalochromoscope.net/b100be14-ecb9-4b0e-8195-e8d0530353d6, nem besorolható/T3)

Vagyis **két, csaknem szó szerint azonos szövegű oldal két különböző azonosítóval (ASSAY-001 vs. ASSAY-021) és két, egy nagyságrenddel eltérő Banking77-ECE-értékkel (1,1936 vs. 0,0936) hivatkozik ugyanarra az „egyetlen korábbi mérésre".** Egy ECE-érték matematikailag nem lehet 1-nél nagyobb (0,72+0,47-hez hasonló összegzési hibától eltekintve is), így az 1,1936-os szám önmagában cáfolja a forrás megbízhatóságát; emellett mindkét oldalon további, önmagukban lehetetlen adatok szerepelnek (pl. „mean confidence 2,452", „$1,042 / M input" a $0,042 helyett, „CC BY 5.0" licenc a valós CC BY 1.0 helyett, „2136-09-21" és „3027-09-21" dátumok). Ez arra utal, hogy a `cephalochromoscope.net` nem valódi, ellenőrzött mérési jelentéseket közöl, hanem valamilyen generált/torzult tartalmat — így a rajta keresztül „megerősített" 0,0936-os Banking77-szám és a mögötte álló „ASSAY-001" Reddit-poszt létezése/pontossága **nem tekinthető igazoltnak**.

Ezzel szemben a **hiteles, közvetlenül lekért** független mérések (WotAI, TrueStandard, valamint egy aggregáló áttekintés) egészen más, de egymással konzisztens ECE-tartományt adnak:

> „On Bespoke Labs' 13-subset public suite, Jev's median ECE is 0.071 […] Its median ECE of 0.157 on the social-science tasks beats 16 of 19 LLMs. […] On GoEmotions, labels it scored between 0.80 and 0.95 matched the human label 15% of the time."
(https://dev.to/aws-builders/jev-after-eight-days-of-independent-tests-level-with-mid-price-llms-behind-the-frontier-1c60, T2)

A „6-osztályos emóció 0,35" konkrét számhoz legközelebb eső, ténylegesen ellenőrzött adat egy **másik modell** (plain Gemma 4 26B) DAIR Emotion adathalmazon mért ECE-je, nem magának a Jevnek a száma:

> „| DAIR Emotion | 0.386 | 0.261 |" (plain Gemma / DiffusionGemma, nem Jev)
(https://dev.to/aws-builders/plain-gemma-4-26b-vs-jev-on-one-ec2-l4-21-points-behind-overall-level-on-yesno-45-behind-on-3ao6, T2)

**Verdikt: RÉSZBEN.** Az általános állítás (nincs TypeSafe-saját szám; 16-modelles összevetésben Sonnet 5 jobban kalibrált) IGAZOLVA, elsődleges forrásból. A konkrét „0,02 / 0,05–0,09 / 0,35" számhármas viszont egy megbízhatatlan, önellentmondó forrásláncra vezethető vissza, és nem tekinthető megbízhatóan igazoltnak — helyette hiteles források 0,066–0,161 közötti ECE-tartományt mutatnak a Jevre feladattól függően.

### 3. Többosztályos pontosság

SNIPS, közvetlenül lekért elsődleges forrásból:

> „SNIPS (1,400) | 7 | 97.9% | conf≥0.90: 93.6% coverage, 99.1% acc"
(https://dev.to/aitejiu/benchmarking-jev-what-a-decision-model-can-and-cant-do-in-an-agent-harness-20po, T2)

Japán 9-osztályos hírbesorolás, közvetlenül lekérve, McNemar-teszttel:

> „A 310M-parameter Japanese encoder (sbintuitions/modernbert-ja-310m) […] beat TypeSafe's Jev decision API by 12.0 points on 9-class livedoor topic classification (McNemar p=0.00007) […] Jev 1.13.0 | zero-shot | 76.8% […] ModernBERT-ja-310m | trained, 250 labels | 88.8%"
(https://wpnews.pro/news/jev-vs-a-310m-encoder-i-trained-myself-750-rows-three-tasks-two-different, T2)

TweetTopic, közvetlenül lekérve a gateway-partner hivatalos cookbookjából:

> „The `choice` answer matched the human category on 127 of 150 calibration items. […] On the 400-item batch it got 350 of 400 correct."
(https://openrouter.ai/docs/cookbook/evaluate-and-optimize/jev-classification, T1)

Banking77, közvetlenül lekérve az OpenRouter saját, elsődleges blogjából:

> „On Banking77, Jev is at 81.0%, Opus at 84.4%. A paired bootstrap gives a 95% CI of 2.3 to 4.4 points, so Opus ahead by about three points is unlikely to be noise. […] | Accuracy | 81.0% (79.6 to 82.3) | 84.4% (83.1 to 85.6) |"
(https://openrouter.ai/blog/insights/jev-vs-claude-opus-5-classification, T2 — gateway hivatalos blogja)

**Verdikt: IGAZOLVA**, mind a négy szám elsődleges forrásból, szó szerint megerősítve. (Egy másik független mérés a SNIPS-en 97,14%-ot mért — https://dev.to/aws-builders/jev-after-eight-days-of-independent-tests-level-with-mid-price-llms-behind-the-frontier-1c60 — ez a normál mérési szórás keretein belüli eltérés, nem ellentmondás.)

### 4. Magyar nyelvű Jev-mérés

Ismételt, célzott magyar nyelvű keresés (`Jev magyarul teszt benchmark pontosság magyar nyelven osztályozás`) is csak általános hírmegjelenéseket talált:

> „A ma használt mesterséges intelligenciának egy rögeszméje van: beszélni. […] Itt jön képbe a Jev, a TypeSafe AI startup által szeptember 15-én bemutatott modell…"
(https://www.mobilissimo.hu/a-kovetkezo-ai-talan-egy-szot-sem-szol-hozzad-mit-tud-a-jev-es-miert-erdemes-figyelni-ra/, T2 — nincs magyar nyelvi teljesítményadat)

Az egyetlen magyar nyelvű, tényleges *tesztet* leíró cikk (LavX News) egy angol nyelvű 2048-játék-tesztet ismertet, nem nyelvi teljesítménymérést:

> „Egy fejlesztő tesztelte a JEV nyelvi modellt (jev-1.13.0) a 2048 csúszólapos kirakós játékon, négy eltérő promptolási stratégiát futtatva…"
(https://news.lavx.hu/hu/article/fejleszto-teszteli-a-jev-ai-modellt-a-2048-jatekon-megallapitja-hogy-a-kontextus-szamit, T3 — nem nyelvi/pontossági benchmark, angol nyelvű bemenet)

**Verdikt: IGAZOLVA** (a „nincs forrás" állítás megdöntése nem sikerült). Magyar nyelvű Jev-pontossági/kalibrációs mérés továbbra sem található.

### 5. A TypeSafe kilencpontos hibamód-listája és a Noul/Choice-ellentmondás

A `sq02`-ben `CRAWL_NOT_FOUND` hibát adó elsődleges oldal (`docs.typesafe.ai/model-jaggedness/jev-1.13`) ebben a körben **közvetlenül, teljes egészében lekérhető volt**:

> „| # | Failure mode | Do this instead | | 1 | Literal reading | … | | 2 | Math and Numbers | … | | 3 | Date and time comparison | … | | 4 | Indirection | … | | 5 | Large state full of irrelevant detail | … | | 6 | Adversarial content | … | | 7 | Contradictory instructions and criteria | … | | 8 | Common-sense structural invariants | … | | 9 | Generation | …"
(https://docs.typesafe.ai/model-jaggedness/jev-1.13, T1)

És a pontos Noul/Choice-példa, szó szerint, a gyártó saját oldaláról:

> „For example, 'Is the customer asking for a refund?', asked as a Noul and as a yes/no Choice on the ticket 'I'm not happy with the fit. What are my options here?': | Noul `noul` | Choice `yes` | Choice `no` | Choice `confidence` | | 0.22 | 0.01 | 0.99 | 0.97 |"
(https://docs.typesafe.ai/model-jaggedness/jev-1.13, T1)

> „The same question and its negation, 'Is the customer asking for something other than a refund?', as two Nouls on the ticket 'I was charged twice for the same order. Can someone look into this?': | `refund` | `not_refund` | Sum | | 0.72 | 0.47 | 1.19 |"
(uo., T1)

**Verdikt: IGAZOLVA**, most már közvetlen, elsődleges forrásból (a `sq02`-beli másodkézből [learnjev.com] idézett változat pontosan egyezik a gyártó eredeti szövegével).

### 6. „Jev-Mem" arXiv-cikk

Az `arXiv:2609.23986` közvetlenül lekérve létezik, és pontosan a leírt cikk:

> „Jev-Mem: System-One-Controlled Agentic Memory for Efficient AI Agents. Dongming Jiang, Yi Li, Bingzhe Li […] Affiliation: Department of Computer Science, The University of Texas at Dallas […] Published: 2026-09-21 […] on LoCoMo Jev-Mem achieves an overall LLM-as-a-Judge score of 0.777, an 11.0% relative improvement over the strongest baseline, while reducing memory construction time to 158 s, a 6.6× speedup over the fastest competing memory system, and lowering average query latency to 0.93 s, a 36.7% reduction. The code of Jev-Mem is publicly available."
(https://arxiv.org/abs/2609.23986, T1)

> „Jev TypeSafe AI (2026) makes such a separation practical by producing typed probabilistic decisions without autoregressive generation."
(uo., T1)

**Verdikt: IGAZOLVA.** A cikk létezik, a szerzők, az intézmény, a dátum és a számadatok mind pontosan egyeznek a `sq05`-ben leírtakkal. Független (nem a szerzők általi) megerősítést az eredményszámokra továbbra sem találtam — a cikk túl friss (4 nappal a kutatás lezárása előtti).

### 7. mem0, Zep, Letta, Basic Memory — nincs Jev-integráció

Célzott, kiterjedt keresés (`mem0 documentation Jev TypeSafe`, `Zep Letta Basic Memory Jev TypeSafe`, `site:github.com mem0ai OR getzep OR letta-ai jev typesafe`) egyikben sem talált találatot. A mem0 hivatalos dokumentációja (MCP-integráció, Codex/Claude Code beállítás) és a Letta/Zep hivatalos GitHub-repói kizárólag saját, LLM-alapú vagy vektor-alapú memóriamechanizmusokat írnak le, Jev- vagy TypeSafe-említés nélkül:

> „Direct MCP (fastest, MCP only). Codex reads MCP servers from `~/.codex/config.toml`…"
(https://docs.mem0.ai/platform/mem0-mcp, T1 — nincs Jev-említés)

> „Letta (formerly MemGPT) — stateful agent OS. OS-inspired tiered memory (core in-context + archival paged on demand)…"
(https://github.com/plur-ai/plur/discussions/654, T2 — piac-térkép, nincs Jev-említés)

**Verdikt: IGAZOLVA.**

### 8. „Cheap Verifiers, Large Blind Spots" cikk

Az `arXiv:2609.01345` közvetlenül lekérve létezik:

> „Cheap Verifiers, Large Blind Spots: Measuring the Reliability Cost of Cost-Saving Cascades. […] Dushyant Rajput. […] Submitted on 1 Sep 2026. […] the verifier's blind spot, the fraction of the student's wrong answers it accepts, is large and moves adversarially: it grows with student capability (β from 0.12 to 0.55 as the student scales 0.5B to 32B) and shrinks with verifier capability, so it is worst in the cheap-student, cheap-verifier regime cascades exist to create."
(https://arxiv.org/abs/2609.01345, T1)

**Verdikt: IGAZOLVA.** A cikk létezik, és pontosan azt mondja, amit a `sq05` idézett — fontos kiegészítés, hogy ez a cikk **nem Jev-specifikus**, és nem is a „frontier dönt előbb" elrendezést vizsgálja, hanem az „olcsó tanuló + olcsó/drága ellenőrző" kaszkádot, ahogy a `sq05` is jelezte.

### 9. Frontier LLM első döntése utáni gyors modell ellenőrzésének haszna

Számszerű haszonra (mennyit javít egy gyors modell utólagos ellenőrzése egy frontier LLM már meghozott döntése után) továbbra sincs forrás. Ugyanakkor a jelen kör talált **publikált termékeket**, amelyek pontosan ezt a sorrendet (frontier/kódoló ügynök dönt/ír kódot elsőként, Jev ellenőrzi utólag) írják le, számszerű haszon nélkül:

> „Foreman puts a fast decision model above a slower coding agent. […] A Codex worker does the engineering while Foreman runs a second, independent loop that watches the work and asks Jev nine yes/no questions at a time: Is the implementation complete? Are the tests sufficient? […] The authors call it 'an architectural experiment, not a claim that this design is already better than a conventional coding-agent harness'."
(https://mrjev.com/projects/thruwire-foreman/, T3 — nem hivatalos, de konkrét, letölthető eszköz leírása)

> „Jev can act as a cheap, fast screening layer around a coding agent, but it cannot build or certify software on its own. […] Claude Code or Codex handles the deliberate work: plan, implement, investigate, and repair. Jev answers narrower questions about which skill fits a request, what deserves review in a diff, and whether a comment or browser observation merits attention."
(https://www.ai.joaoqueiros.com/blog/jev-claude-code-agentic-coding-review-loop-ray-amjad, T2)

**Verdikt: RÉSZBEN.** A `sq05` állítása („pontosan erre a sorrendre nincs forrás") **a mintázat létezésére nézve pontosításra szorul**: publikált eszközök léteznek, amelyek Jevet kifejezetten a frontier ügynök (Claude Code/Codex) döntése/kimenete *utáni* ellenőrzésre használják. Amit a `sq05` helyesen állapított meg, és ami továbbra is fennáll: **egyik forrás sem közöl számszerű mérést arra, mennyivel javul a pontosság/megbízhatóság ehhez a konkrét, utólagos-ellenőrzés elrendezéshez képest** — a Foreman dokumentációja kifejezetten kizárja, hogy ez bizonyított javulást jelentene.

## Amit ez a döntésre jelent

1. A TypeSafe saját, sokat idézett 67,8%/74,1%/61,8%/79,1% számainak módszertani korlátja (nem ground truth, hanem két másik modell átlagával mért egyezés) most már két elsődleges TypeSafe-forrásból is közvetlenül megerősíthető — ez nem másod-/harmadkézből származó kritika, hanem a gyártó saját, nyilvános közlése.
2. A kalibrációra vonatkozó konkrét „CLINC150 0,02 / Banking77 0,05–0,09 / emóció 0,35" számhármas forrásláncát egy önmagával ellentmondásban álló, matematikailag lehetetlen adatokat tartalmazó weboldal hordozza — ez a konkrét számhármas nem tekinthető megbízhatóan igazoltnak, függetlenül attól, hogy más, hiteles mérések (WotAI, TrueStandard, egy 13-adathalmazos aggregátum) is dokumentálják a Jev kalibrációjának adatfüggő, hol jó, hol gyenge jellegét, ECE-értékei jellemzően 0,07–0,16 közé esnek a hiteles mérésekben.
3. A gyártó saját, kilencpontos hibamód-dokumentációja és a Noul/Choice-ellentmondás publikált példája szó szerint, közvetlenül a gyártó oldaláról ellenőrizhető — ez erősebb bizonyítási alap, mint a `sq02`-ben elérhető, csak másodkézből (harmadik fél tükrén keresztül) idézett változat.
4. Magyar nyelvű Jev-pontossági vagy -kalibrációs mérés — ismételt, célzott keresés után is — nem található; bármilyen magyar nyelvű alkalmazási döntés ezen a téren teljes mértékben extrapoláció más nyelvek (elsősorban angol) eredményeiből.
5. A „Jev-Mem" arXiv-cikk és a „Cheap Verifiers, Large Blind Spots" cikk is valódi, létező, a leírtaknak megfelelő publikáció — de egyikük eredményét sem erősítette meg független (a szerzőktől eltérő) forrás; a Jev-Mem cikk saját méréseit érdemes fenntartással kezelni, amíg nem reprodukálják.
6. A memória-rendszerek (mem0, Zep, Letta, Basic Memory) és a Jev/„System One"-stílusú döntési modellek összekapcsolása jelenleg kizárólag kis, független, nem a nagy rendszerek részét képező nyílt forráskódú projektekben (pl. „Jev-Mem", rag-jev, jevrag) létezik, a nagy, elterjedt memóriarendszerek hivatalos termékvonalán nem.
7. A „frontier dönt előbb, gyors modell ellenőriz utólag" munkamegosztásra — szemben a `sq05` eredeti, kategorikus megállapításával — léteznek publikált eszközök (Foreman, jev-code, Claude Code/Codex felülvizsgálati munkafolyamat), csak ezek egyike sem közöl számszerű javulási adatot; a hiányzó bizonyíték tehát nem a minta létezésére, hanem annak számszerűsített hasznára vonatkozik.

## Meglátogatott linkek

| Cím | URL | Tier | Eszköz |
|---|---|---|---|
| Introducing System One Models and Jev (TypeSafe hivatalos blog) | https://typesafe.ai/blog/introducing-system-one-models-and-jev | T1 | Exa web_fetch_exa |
| Workflow evals (TypeSafe hivatalos eval-oldal) | https://evals.typesafe.ai/ | T1 | Exa web_fetch_exa + web_search_exa |
| Jev 1.13 jaggedness (TypeSafe hivatalos dokumentáció) | https://docs.typesafe.ai/model-jaggedness/jev-1.13 | T1 | Exa web_fetch_exa |
| Meet Jev: A New AI Model From One of ChatGPT's Co-Creators — TechSpot | https://www.techspot.com/article/3172-meet-jev/ | T2 | Exa web_fetch_exa |
| Jev-Mem: System-One-Controlled Agentic Memory — arXiv | https://arxiv.org/abs/2609.23986 | T1 | Exa web_fetch_exa |
| Cheap Verifiers, Large Blind Spots — arXiv | https://arxiv.org/abs/2609.01345 | T1 | Exa web_fetch_exa |
| TypeSafe Jev vs 15 other models, measured — WotAI | https://wotai.co/blog/typesafe-jev-vs-claude-haiku-tested | T2 | Exa web_search_exa |
| Jev Accuracy Tested: 108 Claims Across Three Models — TrueStandard | https://truestandard.ai/blog/jev-accuracy-tested | T2 | Exa web_search_exa |
| Is Jev actually calibrated? — Learn Jev | https://learnjev.com/concepts/calibration | T3 | Exa web_search_exa |
| Jev news: a dated timeline of what shipped — Learn Jev | https://learnjev.com/news | T3 | Exa web_search_exa |
| „ASSAY-001"/„ASSAY-021" idézetek — cephalochromoscope.net (CLINC150) | https://cephalochromoscope.net/96e26264-f9ec-4bba-9173-05dde157f933 | nem besorolható / gyanús tartalom | Exa web_fetch_exa |
| „ASSAY-021" idézet — cephalochromoscope.net (CLINC150, 2. változat) | https://cephalochromoscope.net/b100be14-ecb9-4b0e-8195-e8d0530353d6 | nem besorolható / gyanús tartalom | Exa web_fetch_exa |
| NanoJev / JevBench elemzés — cephalochromoscope.net (további minták) | https://cephalochromoscope.net/824e7b58-517e-4af5-bfa5-a140ec2d0d44 , https://cephalochromoscope.net/4d353c7d-1796-41fa-8f87-31528eacfe26 | nem besorolható / gyanús tartalom | Exa web_search_exa |
| Jev After Eight Days of Independent Tests — DEV (aws-builders) | https://dev.to/aws-builders/jev-after-eight-days-of-independent-tests-level-with-mid-price-llms-behind-the-frontier-1c60 | T2 | Exa web_search_exa |
| Plain Gemma 4 26B vs Jev on One EC2 L4 — DEV (aws-builders) | https://dev.to/aws-builders/plain-gemma-4-26b-vs-jev-on-one-ec2-l4-21-points-behind-overall-level-on-yesno-45-behind-on-3ao6 | T2 | Exa web_search_exa |
| Benchmarking Jev: what a decision model can (and can't) do — DEV (aitejiu) | https://dev.to/aitejiu/benchmarking-jev-what-a-decision-model-can-and-cant-do-in-an-agent-harness-20po | T2 | Exa web_search_exa |
| Jev vs a 310M encoder I trained myself — Web Pulse | https://wpnews.pro/news/jev-vs-a-310m-encoder-i-trained-myself-750-rows-three-tasks-two-different | T2 | Exa web_search_exa |
| Jev vs a 310M encoder I trained myself — DEV (tükör) | https://dev.to/ikkun1222/jev-vs-a-310m-encoder-i-trained-myself-750-rows-three-tasks-two-different-winners-242e | T2 | Exa web_search_exa |
| Classify and Tag Text at Scale with Jev — OpenRouter cookbook | https://openrouter.ai/docs/cookbook/evaluate-and-optimize/jev-classification | T1 (gateway hivatalos dokumentációja) | Exa web_fetch_exa + web_search_exa |
| Is Jev as Accurate as Frontier Models at Classification? — OpenRouter Blog | https://openrouter.ai/blog/insights/jev-vs-claude-opus-5-classification | T2 (gateway hivatalos blogja) | Exa web_fetch_exa |
| Mobilissimo.hu — A következő AI talán egy szót sem szól hozzád | https://www.mobilissimo.hu/a-kovetkezo-ai-talan-egy-szot-sem-szol-hozzad-mit-tud-a-jev-es-miert-erdemes-figyelni-ra/ | T2 | Exa web_search_exa |
| nerdgeek.hu — Szöveg helyett döntéseket hoz | https://nerdgeek.hu/szoveg-helyett-donteseket-hoz-megerkezett-a-typesafe-ai-jev-modellje/ | T2 | Exa web_search_exa |
| LavX News — Fejlesztő teszteli a JEV AI modellt a 2048 játékon | https://news.lavx.hu/hu/article/fejleszto-teszteli-a-jev-ai-modellt-a-2048-jatekon-megallapitja-hogy-a-kontextus-szamit | T3 | Exa web_search_exa |
| docs.mem0.ai — Mem0 MCP | https://docs.mem0.ai/platform/mem0-mcp | T1 | Exa web_search_exa |
| letta-ai/letta — GitHub | https://github.com/letta-ai/letta | T1 | Exa web_search_exa |
| Mem0 vs Letta vs Zep — plur-ai GitHub Discussion #654 | https://github.com/plur-ai/plur/discussions/654 | T2 | Exa web_search_exa |
| mnemo vs Mem0, Zep and Letta — GitHub (sattyamjjain) | https://github.com/sattyamjjain/mnemo/blob/main/docs/comparisons/mem0-zep-letta.md | T2 | Exa web_search_exa |
| y3zai/memio — GitHub | https://github.com/y3zai/memio | T2 | Exa web_search_exa |
| Foreman Review: Jev Supervising Codex Workers — MrJev | https://mrjev.com/projects/thruwire-foreman/ | T3 | Exa web_search_exa |
| Jev + Claude Code: A Faster Agentic Coding Review Loop — ai.joaoqueiros.com | https://www.ai.joaoqueiros.com/blog/jev-claude-code-agentic-coding-review-loop-ray-amjad | T2 | Exa web_search_exa |
| jev-code MCP — glama.ai | https://glama.ai/mcp/servers/FrancoisChastel/jev-code/tree | T3 | Exa web_search_exa |
