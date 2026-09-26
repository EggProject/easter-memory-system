# SQ02 — Mennyire pontos és megbízható a Jev döntése

*Módszer: kizárólag Exa (`web_search_exa`, `web_fetch_exa`), a `_kozos.txt` és a `deep-web-research` skill elvei szerint. Alügynök-indítás (a skill teljes, több-ügynökös pipeline-ja) ebben a körben sem történt — egyszemélyes, de Exa-only, elsődleges forrásokra törekvő kutatás, a `sq00-azonositas.md` kontextusára építve. Minden számot a forrás nyelvén, szó szerint idézek; ahol a szám csak másod-/harmadkézből érhető el, azt jelzem.*

## Rövid válasz

A TypeSafe egyetlen saját mérést tett közzé induláskor (2026-09-15): egy 4 munkafolyamatos ("workflow eval") tesztet, ahol a referenciaválasz **két másik modell (GPT-6 Astra és Claude Fable 5.1, „high thinking") átlaga**, nem emberi igazság — ezen a mércén a Jev összesített egyezése 67,8%, szemben a GPT-5.6 Sol 74,1%-ával, számlafeldolgozásnál pedig 61,8% a 79,1%-hoz képest; ezt a négy számot legalább hat egymástól független forrás (TechSpot és öt másik elemzés) egyezően idézi. Kalibrációra (ECE, Brier, reliability diagram) a TypeSafe **nem tett közzé semmilyen saját mérőszámot** — ezt egy független elemzés kifejezetten hiányként nevesíti —, a közösségi mérések pedig adatfüggően hol jól, hol rosszul kalibráltnak találták a modellt, és legalább egy 16-modelles összevetésben egy általános célú frontier-LLM (Claude Sonnet 5) jobban kalibrált volt nála ugyanazon a feladaton. Többosztályos (5–20 címkés) besorolásra van adat: 7 osztályon 97,9%, 9 osztályos japán hírtéma-besoroláson 76,8% (egy kis, 250 mintán tanított enkóder itt 12 ponttal jobb volt), 6 kategórián 87,5%; a tartományon kívüli, de releváns Banking77 (77 osztály) feladaton 76–80,3% között mozgott, és több kis, illetve frontier LLM is megelőzte. Angol nyelvű mérés bőven van, **magyarra nincs forrás** — egyetlen Jev-specifikus magyar nyelvi tesztet vagy akár csak említést sem találtam; más nyelvekre (orosz, spanyol, kínai, koreai, japán, német) szórt adatok egyöntetűen nyelvváltáskor bekövetkező pontosságesést mutatnak. Ismert hibamódokra sok adat van: a TypeSafe saját dokumentációja kilenc hibamódot sorol fel (szó szerinti értelmezés, aritmetika, dátumösszehasonlítás, indirekció, irreleváns adattal túlterhelt állapot, ellenséges tartalom, ellentmondó instrukció/kritérium, strukturális következetlenség, generálásigény), és független mérések is dokumentáltak magabiztos, de téves választásokat (≥90%-os konfidencia mellett is), hosszú bemenetnél/elmosódott címkéknél bekövetkező pontosságesést, valamint hasonló/átfedő opciók közti szisztematikus tévesztést. Kifejezett „ellentmondó állítás Noul-lal" tesztet nem találtam, de a TypeSafe saját, publikált példája mutatja, hogy ugyanaz a tény Noul-ként és Choice-ként kérdezve homlokegyenest ellentétes választ ad, és két, egymás logikai tagadásának szánt Noul-válasz összege nem ad ki 1-et. Frontier LLM-hez képest a Jev jellemzően „középkategóriás" modellekkel egy szinten van és 6,5–11,5 ponttal lemarad a csúcsmodellektől; kis, saját adaton tanított helyi osztályozóhoz (BERT-típusú enkóder) képest 200–300 címkézett példa felett a helyi modell rendszeresen jobb és gyorsabb; tiszta, tanítás nélküli koszinusz-hasonlóságú beágyazás-osztályozóval való számszerű összevetést nem találtam — csak minőségi állításokat arról, hogy ez „kategóriahiba", mert az embedding önmagában nem válaszol kérdésre.

## 1. Pontossági mérések: gyártói teszt és a TechSpot-számok eredete

### 1.1 A TypeSafe saját („workflow eval") mérése

A hivatalos bejelentő blogposztban (typesafe.ai, 2026-09-15, szerző Diogo Almeida) a cég maga írja le a módszertant:

> „We made a new type of evaluation to measure how well AI works within code. We don't optimize for a ground truth classification […] Instead, we assume there is a correct compute graph (a 'workflow' represented in code) and use the predictions of the largest, smartest, and most expensive external models as reference probabilities. Rephrased: every model gets the same workflow. We test how they compare to the average of the smartest models (in this case, Astra and Fable)."
(https://typesafe.ai/blog/introducing-system-one-models-and-jev, T1)

Vagyis a „pontosság" itt **nem emberi/objektív igazsághoz**, hanem **két másik modell (GPT-6 Astra és Claude Fable 5.1, „high thinking" módban) válaszainak átlagához** viszonyított egyezés. A blog saját maga is jelzi a torzítást:

> „We use the average of GPT-6 Astra and Fable 5.1 as the reference answer, which biases answers towards OpenAI and Anthropic's models. We likely underestimate the relative performance of our model and DeepSeek's models." (uo., T1)

A blog a konkrét számtáblát nem az oldal szövegében, hanem egy külön „workflow evals site"-on közli (erre a blog hivatkozik: „See our workflow evals site for all the details"), amit Exa-val nem sikerült közvetlenül lekérni (a `typesafe.ai/evals` és a `typesafe.ai/models` URL is `CRAWL_NOT_FOUND` hibát adott — ugyanaz a probléma, mint a `sq00-azonositas.md`-ben dokumentált `typesafe.ai/models` esetén).

### 1.2 A „67,8% vs. 74,1%" és „61,8% vs. 79,1%" szám eredete és jelentése

A TechSpot cikke (2026-09-20, Julio Franco) közvetlenül idézi ezt a táblázatot:

> „The benchmarks are TypeSafe's own. The company skipped public leaderboards. Its workflow tests score models by agreement with the averaged answers of GPT-6 Astra and Fable 5.1, not against verified ground truth. By that measure, Jev reached about 67.8% agreement overall versus 74.1% for GPT-5.6 Sol. It came close on customer service (76% versus 78.3%) and fell well behind on invoice processing (61.8% versus 79.1%)."
(https://www.techspot.com/article/3172-meet-jev/, T2)

Tehát a szám pontos jelentése: **egyezés (agreement) a GPT-6 Astra + Claude Fable 5.1 átlagával, mint referenciaválasszal**, nem külső, emberi igazsághoz mért pontosság. A négy szám (67,8% / 74,1% / 61,8% / 79,1%) legalább öt további, egymástól független forrásban is megjelenik, azonos értékekkel:

- **dev.to (aws-builders, 2026-09-24)**: „Eval accuracy. Reference labels are 'an average of the responses of GPT-6 Astra and Claude Fable 5.1, both at high thinking', so accuracy there means agreement with two LLMs. Jev scores 67.8%, equal to Sonnet 5, with GPT-5.6 Sol leading at 74.1%. On invoice processing Jev scores 61.8% against Sol's 79.1%." (T2)
- **benchlm.ai**: „Its workflow evaluations, scored against the average of GPT-6 Astra and Claude Fable 5.1 at high thinking, put Jev at 67.8 percent agreement and GPT-5.6 Sol at 74.1, averaging four workflows with equal weight. These are agreements with model-generated labels, not human-scored accuracy." (T2)
- **agenccy.ai**: „Averaged across four workflows, Jev scores 67.8%. That places it behind Sol at 74.1% and Opus 5 at 73.1%, level with Terra at 67.9% and tied with Sonnet 5, also 67.8%. […] The reference labels were 'generated via an average of the responses of GPT-6 Astra and Claude Fable 5.1, both at high thinking' — so accuracy here measures agreement with two frontier models, which are also the models Jev is marketed against." (T2)
- **bug.hr (horvát, 2026-09-22)** táblázatban közli ugyanezt (Jev 67,8%, GPT-5.6 Luna 66,8%, GPT-5.6 Terra 67,9%, Claude Sonnet 5 67,8%, Claude Opus 5 73,1%, GPT-5.6 Sol 74,1%) és hozzáteszi: „Test je izradio TypeSafeov tim, a 'točan odgovor' je prosjek odgovora GPT-6 Astre i Fablea 5.1. Jev se dakle ne mjeri prema stvarno točnim odgovorima, nego prema tome koliko se slaže s velikim modelima." (T3, de a tartalom megegyezik a T1/T2 forrásokéval)
- **datasciocean.com (kínai, 2026-09-22)**: „這張表裡 67.8% 一致率的『參考答案』不是人工標註的真值（ground truth），而是用 GPT-6 Astra 跟 Fable 5.1 兩個模型的平均答案當標準答案。" (T2/T3)

**Fontos árnyalat**, amit az agenccy.ai és a benchlm.ai is kiemel: a TypeSafe táblázatában minden más modell **kétszer** szerepel (egyszer „workflow" — lebontott, kód-vezérelt — módban, egyszer „prompt" módban, ahol egy generált promptban maga végzi a láncolt logikát, és ez utóbbiban lényegesen rosszabbul teljesít), miközben a Jevnek nincs „prompt" sora, mert szerkezetileg nem futtatható úgy. A horvát cikk saját számítást is közöl arra, hogy a lebontás (a workflow-formátum) önmagában mennyit javít: „Svaki model u prosjeku je točniji kad je zadatak rastavljen, a najveća je razlika kod Claude Haikua 4.5 (53,6 prema 18,1 posto)." — vagyis a nyereség jó része nem a Jev modellből, hanem a feladat lebontásából ered.

### 1.3 Független mérések listája (fő pontossági eredmények)

| Forrás | Módszer | Fő eredmény |
|---|---|---|
| Aman Kumar blogja (amankumar.ai, 2026-09-18, T2) | ~16 000 API-hívás, 4 nyilvános adathalmaz (Enron spam, SST-2, AG News, Banking77) + 1005 valós dokumentumoldal + 800 e-mail, kimenet valós üzleti eredményhez mérve | „On short-text classification it is level with or ahead of gpt-5.4-mini and gpt-5.6-luna on three of four public sets... It is best on short input with crisp labels. […] On a whole-document read it is worse than the small model we run today." |
| WotAI (wotai.co, Alex Kim, 2026-09-18, T2) | 16 modell, 150 passzázs, Noul-kérdés (kalibráció) + 2 Choice-feladat | „Was Jev more accurate? Not consistently… Across three tasks it lost one, won one and tied one: 79.9% against 83.2% on business categories, 50.0% against 42.0% on commit types, 66.0% each on prose voice." |
| TrueStandard (truestandard.ai, 2026-09-18, T2) | 108 kézzel címkézett állítás, 6 domain, 3 modell (Jev, Gemini 3.1 Flash Lite, Claude Haiku 4.5) | „Jev finished 1.9 points ahead of Gemini 3.1 Flash Lite and 2.8 ahead of Claude Haiku 4.5 on raw accuracy" — 96,3% vs. 94,4% vs. 93,5% |
| AY Automate (ayautomate.com, 2026-09-20, T2) | 791 címkézett döntés, Banking77 (8- és 77-utas) + prompt-injekció-detekció, McNemar-teszt | „Not more accurate than GPT-5.6 Terra: on 77-way intent routing Terra was 5 points ahead… Jev behaved like a good small model, not like a frontier model." |
| primeline.cc (2026-09-18, T2) | pre-regisztrált, 3600+ tétel (film-, hír-, hangulat-, Banking77-adat) + 798 saját commit + 450 tudásbázis-tétel, Jev vs. Claude Haiku 4.5 | „Jev won the commit-message job clearly: 65.7% accuracy against Haiku's 54.8%… Jev lost the knowledge-category job just as clearly." |
| dev.to/aitejiu (2026-09-21, T2) | 10 nyilvános/félig-szintetikus adathalmaz ágens-eszközökre (InjecAgent, BEIR SciFact, SNIPS, Banking77, MetaTool, BFCL, SkillRetBench, RouterBench, Who&When) | vegyes: nagyon jó prompt-injekció-detekción és rerankeren, gyenge modell-routingon (51,3%, „no signal") és trajektória-hibaazonosításon (AUROC 0,560, véletlenszintű) |
| wpnews.pro (2026-09-21, T2) | 3 japán osztályozási feladat, 250 címkézett sor/feladat, 6 rendszer | 9-osztályos témabesorolás: Jev 76,8%, egy 310M-paraméteres tanított enkóder 88,8% (McNemar p=0,00007) |

## 2. Kalibráció: van-e mérés arra, hogy a valószínűség tényleg megfelel-e a találati aránynak?

A TypeSafe hivatalos állítása (a blogban): „Always communicates confidence and uncertainty with every output. Calibrated: higher confidence means higher accuracy." (typesafe.ai/blog/introducing-system-one-models-and-jev, T1) — de ehhez **maga a cég semmilyen ECE/Brier/reliability-diagram számot nem publikált**. Egy Jev-dokumentációs oldal (nem hivatalos, de nem is marketing-célú, technikai jellegű) ezt kifejezetten kritizálja:

> „Calibration is a specific, testable property with a precise definition and a standard metric. TypeSafe built a company on it and published neither a number nor a curve. […] TypeSafe has published no calibration metric of its own — no ECE, no Brier score, no reliability diagram. For a company whose entire differentiator is calibration, and for the single easiest property in machine learning to measure, that remains the most conspicuous omission of the launch."
(https://learnjev.com/concepts/calibration, T3 — nem hivatalos Jev-oldal, de a `_kozos.txt` szerint jelölve, önmagában nem elegendő forrás, ezért az alábbi független mérésekkel erősítve)

Ugyanez az oldal összefoglal több független mérést egy táblázatban:

| Független mérés | Eredmény |
|---|---|
| Pre-regisztrált vizsgálat, 8576 válasz | „Calibrated on CLINC150 (ECE 0.0204). Not calibrated on Banking77 (ECE 0.0936, systematically overconfident). Same model, same method, two datasets, opposite verdicts." |
| Konfidencia-sáv ellenőrzés | „On the 126 rows where Jev reported confidence ≥ 0.9, it was 72.2% accurate. That is the failure mode calibration is supposed to prevent." |
| Küszöbérték-átvihetőségi teszt | „The optimal threshold moved from 0.67 to 0.37 between two datasets… 'nothing measured on the first dataset predicted the second.'" |

Ezt más, önálló mérések is megerősítik és árnyalják:

- **WotAI (16 modell, 150 sor, Noul-kérdés, 2026-09-18, T2)**: „Sonnet 5 posted an ECE of 0.062, roughly half Jev's 0.121, with better accuracy and more willingness to sit in the middle. On the metric TypeSafe's entire pitch rests on, a general-purpose frontier model won." Ugyanakkor a sub-second (1 másodperc alatti) modellek közt „Jev had the best calibration error of the three models that qualified" (0,121 vs. Haiku 0,122 vs. gpt-5.4-mini 0,192).
- **TrueStandard (108 állítás, 2026-09-18, T2)**: „Expected calibration error came out at 0.066 for Jev, 0.061 for Gemini 3.1 Flash Lite and 0.067 for Claude Haiku 4.5. At 108 items those are one number… A cheap frontier-lab model, asked properly for a probability, calibrates about as well as the model built to produce calibrated probabilities." Fontos módszertani megjegyzés a cikkből: első (22 tételes) futtatásukban a Jev „nyert" a kalibráción, de ez a prompt hibája volt (nem kérték a chat-modelleket a teljes 0–1 skála használatára); a hibát javítva a különbség eltűnt.
- **dev.to (aws-builders, aggregált áttekintés, 2026-09-24, T2)**: „On Bespoke Labs' 13-subset public suite, Jev's median ECE is 0.071, lower than Nimble-9B's on 11 of 13 subsets… Against LLMs that write their confidence as a number, Jev's own probabilities usually win. Its median ECE of 0.157 on the social-science tasks beats 16 of 19 LLMs. Once every model gets one fitted temperature, 15 of those LLMs beat it." Ugyanez a cikk azt is jelzi, hogy az irány (túlzott vagy alulzott magabiztosság) adatfüggő: „On public multi-class sets Jev is overconfident: on GoEmotions, labels it scored between 0.80 and 0.95 matched the human label 15% of the time. On crash narratives and synthetic items it is under-confident."
- **jevkit-calibrate és jevcal (közösségi Python-csomagok, PyPI, T3/community eszköz)**: mindkettő kifejezetten azért készült, mert a felhasználóknak saját maguknak kell mérniük az ECE-t/Brier-t/reliability-diagramot — vagyis a piac maga is elismeri, hogy erre nincs gyártói szám: „Verify TypeSafe Jev's calibration on your own data. […] TypeSafe measures this across groups of predictions and says plainly that it does not guarantee any individual answer. This package checks the claim on your data, which is the part nobody else can do for you." (jevkit-calibrate, PyPI, T3)
- **Bernoulli.app elemzés (2026-09-18, T2)**, amely a `confidence` mező (nem az alap valószínűség) matematikai eredetét vizsgálta 1 millió hívás alapján: „Across one million tests, Choice confidence closely follows a normalized top probability within just a rounding error… The practical truth, however, is that neither result establishes that Jev's confidence value relates to the probability of being right, that is model uncertainty in general." Ez azt jelenti, hogy a `confidence` mező egy egyszerű, a válasz-eloszlásból levezetett újraskálázás, nem egy külön, tanult bizonytalanság-becslés.

**Összefoglalva**: van mérés (több is), de a kép kevert és erősen adatfüggő — a kalibrációs hiba (ECE) nagyságrendileg 0,02-től (CLINC150) 0,35-ig (6-osztályos emóció-adathalmaz) terjed a különböző tesztekben, és legalább egy közvetlen összevetésben egy általános célú LLM (Claude Sonnet 5) jobban kalibrált volt a Jevnél ugyanazon a feladaton.

## 3. Többosztályos besorolás (5–20 címke) mérése

Több forrás pontosan ebbe a tartományba eső osztályszámmal tesztelt:

| Adathalmaz | Osztályszám | Jev pontosság | Összevetés |
|---|---|---|---|
| SNIPS (dev.to/aitejiu, 2026-09-21) | 7 | 97,9% | „conf≥0.90: 93.6% coverage, 99.1% acc" |
| AG News (Aman Kumar, 2026-09-18) | 4 (a tartomány alján) | 91,3% | gpt-5.4-mini 88,3%, gpt-5.6-luna 89,7% — Jev nyer |
| livedoor hírtéma (wpnews.pro, 2026-09-21, japán) | 9 | 76,8% | egy 310M-paraméteres, 250 mintán tanított ModernBERT-ja enkóder 88,8% (McNemar p=0,00007); GLiClass zero-shot 62,8% |
| TweetTopic (OpenRouter cookbook, 2026-09-21, T1 — gateway hivatalos dokumentációja) | 6 | „got 350 of 400 correct" = 87,5% | kalibrációs bontás: „Confidence splits here are at 0.8 or above: 114 of 122 matched; at 0.5 to below 0.8: 9 of 18; below 0.5: 4 of 10." |
| Banking77 8-utas alcsoport (AY Automate, 2026-09-20) | 8 (a tartomány alján) | 83,8% | gpt-5.4-nano 90,0%, GPT-5.6 Terra 89,4% — mindkettő megelőzi |
| Banking77 teljes (több forrás) | 77 (a tartományon kívül, de releváns szélső eset) | 76,0–80,3% (forrásonként eltérő mintavétel) | Aman Kumar: gpt-5.4-mini 78,7%, gpt-5.6-luna 81,7% — mindkét kis LLM megelőzi; AY Automate 77-utas altesztjén GPT-5.6 Terra 84,0% vs. Jev 78,8% |
| MetaTool eszközkatalógus (dev.to/aitejiu) | 199 (a tartományon kívül) | 96,5% „similar distractors (k=5)" mellett | „the paper reports 69.1% for ChatGPT on the same 'similar choices' subtask" |

A mintázat több forrásban is megegyezik: **kevés, jól elkülönülő osztálynál (≤10) a Jev jellemzően erős vagy vezet**, míg **sok, egymást átfedő, finomszemcsés osztálynál (77-es Banking77) mind kis, mind frontier LLM-ek megelőzik**. Aman Kumar ezt így fogalmazza meg: „In our interpretation, when classification spaces exhibit dense semantic overlap across dozens of labels, Jev's discriminative certainty degrades alongside its underlying classification precision." (amankumar.ai, T2, megerősítve a braindetox.kr másodforrás által, T2/T3)

## 4. Nyelvek: angol és magyar

**Angol**: a fenti mérések túlnyomó többsége angol nyelvű szövegen történt, ez a fő nyelv, amin adat van.

**Magyar**: a jelen kutatás során **egyetlen forrást sem találtam**, amely kifejezetten magyar nyelvű bemeneten mérte volna a Jev pontosságát, kalibrációját vagy bármilyen teljesítménymutatóját. A magyar nyelvű technológiai média (Mobilissimo.hu, 2026-09-19; nerdgeek.hu, 2026-09-23) beszámolt a Jev indulásáról, de ezek a cikkek a modell általános leírására szorítkoznak, angol nyelvű elsődleges forrásokra (elsősorban TechCrunch) hivatkozva, és nem foglalkoznak a magyar nyelvi teljesítménnyel:

> „Szövegenerálás helyett villámgyors döntésekre tervezték a TypeSafe AI legújabb mesterséges intelligenciáját, a Jev modellt…" (nerdgeek.hu, 2026-09-23, T2 — de nem tartalmaz nyelvi teljesítményadatot)

**Következtetés: NINCS FORRÁS** a magyar nyelvi teljesítményre.

Más, nem angol nyelvekre viszont van szórt (bár nem magyar) adat, amely egy általánosabb mintázatot mutat — a teljesítmény nyelvváltáskor csökken:

- **Orosz**: „Russian XNLI dropped from 88.3% to 77.3% with ECE tripling" (dev.to/aws-builders, 2026-09-24, T2)
- **Spanyol**: „Spanish cost 3 to 6 points" (uo.)
- **Német**: „German cost 0.5 points on MASSIVE" (uo.)
- **Kínai vs. angol** (modell-nehézség-útválasztás, RouterBench): „Chinese subset 14.6% vs English 57.7%." (dev.to/aitejiu, 2026-09-21, T2)
- **Koreai vs. angol** (SkillRetBench): „Non-English tasks: KO R@1 48.9% vs EN 61.5%." (uo.)
- **Japán**: 3 feladaton 65,2–76,8% közötti zero-shot pontosság (wpnews.pro, 2026-09-21, T2), ahol egy kis, saját nyelvre tanított enkóder egy feladaton lényegesen jobb volt.

Egy horvát nyelvű elemzés (bug.hr, 2026-09-22, T3, de tartalma összhangban a fentiekkel) kifejezetten figyelmezteti a nem angol nyelvű felhasználókat:

> „Prema dokumentaciji engleski je glavni jezik treninga, a ostale jezike model obrađuje, ali ne jednako dobro, pa hrvatske tekstove treba testirati na vlastitim podacima."
(„A dokumentáció szerint az angol a fő betanítási nyelv, a többi nyelvet a modell kezeli, de nem egyenlő eséllyel, ezért a [nem angol] szövegeket saját adaton kell tesztelni.")

Ez közvetve megerősíti, hogy a hivatalos TypeSafe-dokumentáció is jelzi az angol elsődlegességét, de ehhez konkrét magyar (vagy akár horvát) számot ez a forrás sem közöl — csak azt tanácsolja, hogy magának a felhasználónak kell megmérnie.

## 5. Ismert hibamódok

### 5.1 A TypeSafe saját, dokumentált hibamód-listája

Egy Jev-dokumentációs oldal (learnjev.com/tutorials/failure-modes, T3, de a TypeSafe hivatalos dokumentációjára hivatkozva és azt idézve) 9 pontban sorolja fel a `jev-1.13` ismert gyengeségeit, TypeSafe-idézetekkel alátámasztva:

| # | Hibamód | TypeSafe ajánlása |
|---|---|---|
| 1 | Szó szerinti értelmezés | „Write the exact condition, criteria for each available option" |
| 2 | Matematika és számok | „Keep the arithmetic in code" |
| 3 | Dátum- és időösszehasonlítás | „Extract components; compare in code" |
| 4 | Indirekció (közvetett hivatkozás) | „Reduce hops; point to the relevant state" |
| 5 | Irreleváns részlettel túlterhelt állapot („context rot") | „Filter first; send only what the question needs" |
| 6 | Ellenséges/manipulatív tartalom | „Write precise prompts, and test edge cases before deploying" |
| 7 | Ellentmondó instrukció és kritérium | „Align the criteria and instruction" |
| 8 | Köznapi strukturális invariánsok megsértése | „Ask each decision one way; enforce identities in code" |
| 9 | Generálásigény (a modell nem tud szöveget írni) | „Use a generative model" |

A horvát bug.hr cikk (2026-09-22) függetlenül is megerősíti ugyanezt a listát: „dokumentacija ima stranicu o devet tipičnih slabosti verzije jev-1.13. Model griješi u računanju, usporedbi datuma i praćenju neizravnih upućivanja, upute čita previše doslovno, zbunjuju ga proturječne upute i zlonamjeran sadržaj, a točnost mu pada kad je stanje pretrpano nevažnim detaljima (context rot)."

### 5.2 Rossz választás magabiztosan (confident wrong answer)

- **TechSpot**: „'Can't hallucinate' is a narrow claim. Jev can't return an answer outside the list it was given… But it can still confidently pick the wrong option." (T2)
- **AY Automate (791 döntés, McNemar-teszt, 2026-09-20, T2)**: „Confident answers were still sometimes wrong: 5 of 112 on 8-way routing and 12 of 153 on 77-way routing at 0.90 or above." A konkrét hibapélda: „The five confident 8-way errors were all the same mistake. Each was labeled 'direct debit payment not recognised' and Jev called it 'card payment not recognised' at 0.93 to 0.99 confidence. GPT-5.6 Terra made the same call on all five, which points at the two labels overlapping, not at a Jev quirk."
- **learnjev.com konfidencia-sáv-elemzés** (a fenti, kalibrációs táblázatból): „On the 126 rows where Jev reported confidence ≥ 0.9, it was 72.2% accurate." (T3, önmagában nem elég, de az AY Automate és a TechSpot fenti megállapításával összhangban)
- **primeline.cc (2026-09-18)** hasonlót talált a saját tudásbázis-teszten: „letting Jev abstain below 0.8 confidence would close the gap — it reaches 98.6% accuracy on the 79% of items it feels confident about," de „on the exact same 356 items Jev chooses to keep, Haiku still wins (98.9% against Jev's 98.6%)" — vagyis a magas magabiztosság nem garantálja, hogy jobb lenne egy alternatívánál.

### 5.3 Hosszú bemenet

- **Aman Kumar**: „It is best on short input with crisp labels. The longer the input and the fuzzier the labels, or the more business logic the question carries, the more its accuracy and its confidence fall together. On a whole-document read it is worse than the small model we run today, and no prompt fixed that." Konkrét számpélda: „A 2,000-email phishing bench had Jev at 62.6% against 81.3% for Claude Haiku 4.5, with worse calibration."
- **learnjev.com (writing-state oldal)**, TypeSafe-idézettel: „Jev suffers from context rot, so unrelated material in the state costs you accuracy." (T3, de a fenti Aman Kumar-eredménnyel és a bug.hr-rel összhangban)
- **navinpai.github.io** (T2): „Long option lists squeeze the descriptions; the repository recommends staying below about 20 choices. Its benchmark report also says the shipped probabilities are overconfident and that temperature fitting helps."

### 5.4 Hasonló/átfedő opciók

- Lásd fent (5.2): a „direct debit payment not recognised" vs. „card payment not recognised" tévesztés az AY Automate tesztben, amit a GPT-5.6 Terra is ugyanúgy elhibázott — az elemzés szerint ez a **címkekészlet átfedésének**, nem kifejezetten a Jev hibájának tudható be.
- **dev.to/aitejiu (MetaTool teszt)**: „MetaTool comparison: the paper reports 69.1% for ChatGPT on the same 'similar choices' subtask (different exact setup — treat as magnitude reference). Errors cluster on near-duplicate tools: descriptions need explicit `not_for` boundaries." — 96,5% pontosság hasonló disztraktorok mellett (k=5), de a hibák szisztematikusan a majdnem-azonos eszközökön csoportosulnak.
- **Banking77** (76 vs. 77 finom, átfedő banki szándék-kategória) minden korábban idézett forrásban a leggyengébb pontja a Jevnek a rövid szövegű tesztek közül.

### 5.5 Ellentmondó állítások felismerése / Noul-kérdéssel kapcsolatos következetlenség

Kifejezett „ellentmondó állítás felismerése" tesztet (pl. két egymásnak ellentmondó mondatot tartalmazó bemeneten Noul-kérdéssel) nem találtam. Amit találtam, az a **modell saját belső következetlensége** azonos tény különböző kérdezési módokon (Noul vs. Choice), amit maga a TypeSafe dokumentál nyilvánosan, „jaggedness" néven:

> „On the ticket 'I'm not happy with the fit. What are my options here?', asked as 'Is the customer asking for a refund?': Noul 0.22 | Choice yes 0.01 | Choice no 0.99 | Choice confidence 0.97. Same question, same ticket, two primitives. Published on TypeSafe's jev-1.13 jaggedness page."
(https://learnjev.com/tutorials/three-primitives, T3, TypeSafe hivatalos „jaggedness" oldalára hivatkozva, amit közvetlenül nem sikerült Exa-val lekérni — `typesafe.ai/blog/jev-1-13-jaggedness` CRAWL_NOT_FOUND hibát adott)

Ugyanez az oldal egy másik, logikai ellentmondást is dokumentál: két, egymás tagadásának szánt Noul-kérdés összege nem 1:

> „On 'I was charged twice for the same order. Can someone look into this?': `refund` 0,72, `not_refund` 0,47, összeg 1,19."

A jevaiguide.com (T3) is megerősíti ugyanezt a jelenséget, saját méréssel:

> „In our own test, 'Is the customer asking for money back?' scored 0.50 on a message that complained about a charge but never mentioned a refund, while 'Does the customer say a charge might be wrong?' scored 0.97. Neither is wrong; the first question was ambiguous."

Ez a jelenség közvetlenül a `_kozos.txt`-ben említett **D-20 (duplikátum-/hasonlóság-ellenőrzés) és D-22/D-26 (kategória-választó prompt)** döntésekhez kapcsolódóan releváns kockázat: ha egy jövőbeli integráció ellentmondó állítások felismerésére Noul-kérdést használna, a fenti adatok azt jelzik, hogy (a) a Noul és az ezzel logikailag ekvivalens Choice-kérdés eltérő választ adhat, és (b) egy állítás és tagadásának Nouljai nem feltétlenül összegződnek 1-re — vagyis a modell nem konzisztens logikai értelemben a kérdezési primitívek között. Erre a TypeSafe hivatalos ajánlása: „Never carry a threshold tuned on a Noul across to a Choice. Never assume complementary questions sum to 1." (learnjev.com, TypeSafe-idézet nyomán, T3)

## 6. Összevetés: frontier LLM, kis helyi osztályozó, beágyazás/koszinusz-alapú osztályozás

### 6.1 Frontier LLM-mel

| Forrás | Eredmény |
|---|---|
| WotAI (16 modell, 2026-09-18) | „Claude Sonnet 5, on calibration error (0.062) and accuracy (71.3%)… If your budget allows a 1.7-second gate, Sonnet 5 is the better instrument." Jev accuracy 66,0% (holtverseny Claude Haiku 4.5-tel), de leggyorsabb (455ms). |
| AY Automate (2026-09-20) | „Not more accurate than GPT-5.6 Terra: on 77-way intent routing Terra was 5 points ahead, and a paired test says that gap is real (p=0.029)." |
| dev.to/aws-builders (aggregált, 2026-09-24, egy nagy pre-regisztrált tanulmány, Ibrahim & Zaki replikáció, ~7977 emberi válasz alapján) | „On accuracy, Jev sits level with mid-price LLMs and 6.5 to 11.5 points behind the frontier in the cleanest comparison." Táblázat: Claude Fable 5.1 84,0% (ECE 0,064), GPT-6 Astra 79,0%, DeepSeek V4.1 Flash 76,0%, MiniMax M3 75,5%, Kimi K3 74,5%, **Jev 72,5%** (ECE 0,161) — Jev az utolsó helyen pontosságban ebben az összevetésben. |
| TrueStandard (108 állítás) | Jev 96,3% vs. Gemini 3.1 Flash Lite 94,4% vs. Claude Haiku 4.5 93,5% — itt a Jev vezet, elsősorban a nehéz („adversarial near-miss") kategórián: 91,7% vs. 83,3%/80,6%. |

Tehát **a kép vegyes és feladatfüggő**: van olyan teszt, ahol a Jev veri a kisebb/olcsóbb LLM-eket, és van, ahol egy csúcsmodell (Sonnet 5, GPT-5.6 Terra, Claude Fable 5.1/GPT-6 Astra) egyértelműen jobb nála pontosságban és/vagy kalibrációban.

### 6.2 Kis, helyben futó (saját adaton tanított) osztályozóval

- **wpnews.pro (2026-09-21)**: egy 310M-paraméteres japán ModernBERT-enkóder, 250 címkézett sorral tanítva, 5-szörös keresztvalidációval: „beat TypeSafe's Jev decision API by 12.0 points on 9-class livedoor topic classification (McNemar p=0.00007) while running 4–20× faster, but only tied Jev on the two polarity tasks." A cikk explicit szabálya: „if the label is visible in the words, train something small; if the label is a judgement about the words, use a decision API."
- **dev.to/aws-builders** (Bespoke Nimble-9B, egy LoRA-alapú, Qwen 3.5 9B-re épülő „klón" modell összevetése): „Kev-9B vs. Jev, out of domain | Accuracy 82–85% vs 85.7%. ECE 0.042 vs 0.049. Coverage at ≤ 5% error: 0.45–0.57 vs 0.70" — itt a nyílt, kis, tanított modell hasonló pontosságú és kalibrációjú, de **lényegesen rosszabb „coverage"-t** (mennyi döntést lehet automatizálni adott hibaköltség mellett) ér el, mint a Jev, mert bár a kalibrációs hiba (ECE) hasonló, a Jev jobban **rangsorolja** saját helyes válaszait a hibás fölé.
- **jev-agent.com (T3, nem hivatalos, de technikai összevetés)** táblázata szerint: „Is Jev more accurate than a fine-tuned BERT classifier? Not on a single fixed task where you have plenty of clean labels — a small trained model will usually beat a general decision model on both accuracy and inference cost. Jev wins when the labels do not exist yet, when the taxonomy moves, or when you need many different judgements rather than one."
- **jevaiguide.com (T3)** hasonló következtetésre jut egy összehasonlító táblázatban: fix, nagy volumenű, sok címkével rendelkező feladatnál a finomhangolt (fine-tuned) osztályozót ajánlja, új/változó taxonómiájú, kevés vagy semennyi címkével rendelkező feladatnál a Jevet.

### 6.3 Beágyazás-alapú (koszinusz) osztályozással

**Konkrét, számszerű összevetést tiszta koszinusz-hasonlóságú (tanítás nélküli, pl. sentence-transformer + legközelebbi centroid) osztályozóval nem találtam.** A fellelt (nem hivatalos, T3) elemzések csak minőségi állításokat tesznek:

> „'Jev vs embeddings' is a category error worth untangling. An embedding model turns text into a vector so you can measure similarity. It does not answer a question. The comparable approach is embeddings plus a k-nearest-neighbour lookup over labelled examples, which is a legitimate and very cheap classifier — but it still needs labelled neighbours, and it can only answer questions that similarity happens to encode."
(https://jev-agent.com/jev-vs-classifier, T3)

> „Is Jev the same as an embedding model? No. Embeddings give you a vector so you can measure similarity; Jev gives you a decision over options you named, with a probability for each. Embeddings plus kNN is a real alternative for classification, but it needs labelled neighbours and it cannot answer a question the vectors were not built for."
(uo.)

A jevaiguide.com egy táblázatban helyezi el az „Embeddings + small model" oszlopot a Jev és a finomhangolt osztályozó között, de konkrét pontossági számot nem közöl hozzá, csak minőségi jellemzőket („Labeled data needed: Dozens to hundreds", „Probabilities: Depends on the model you fit"). Egy kapcsolódó, de **nem azonos** módszer — a nulla-mintás (zero-shot), NLI-alapú **GLiClass** osztályozó (amely span-alapú entailment-modellt használ, nem tiszta koszinusz-hasonlóságot) — viszont szerepel egy számszerű összevetésben:

> „Zero-shot, it scored 62.8 / 87.2 / 44.8: it lost to Jev [76,8/94,4/74,0] on all three tasks, and on the 3-class polarity task it was barely above chance (44.8% against 33.3%)."
(wpnews.pro, 2026-09-21, T2)

Ez azonban **nem koszinusz-alapú beágyazás-osztályozó**, hanem egy tanítás nélküli NLI-osztályozó, ezért csak közvetve releváns a kérdésre — a `_kozos.txt` D-20 pontjában említett, beágyazással végzett hasonlóság-ellenőrzéshez (duplikátum-keresés) közelebb álló, tiszta koszinusz-alapú *osztályozási* összevetésre **nincs forrás**.

## Ellentmondások

1. **A kalibráció minősége forrásonként ellentétes verdiktet kap.** A WotAI 16-modelles teszt szerint a Jev ECE-je (0,121) rosszabb egy frontier LLM-énél (Claude Sonnet 5, 0,062) ugyanazon a feladaton — „On the metric TypeSafe's entire pitch rests on, a general-purpose frontier model won." Ezzel szemben a dev.to/aws-builders aggregált áttekintése szerint a Jev medián ECE-je (0,071) a 13 adathalmazos Bespoke Labs-csomagon jobb, mint a tesztelt 19 LLM közül 16-é, és „Jev's own probabilities usually win" az LLM-ekkel szemben. A TrueStandard-teszt szerint pedig, ha egy olcsó LLM-et megfelelően (a teljes 0–1 skála használatára) kérnek, a kalibrációs különbség gyakorlatilag eltűnik (ECE 0,061–0,069 mindhárom modellre). A három forrás nem feltétlenül zárja ki egymást (más-más feladat, más-más LLM-ek), de együtt azt mutatják, hogy **nincs egységes, minden helyzetben érvényes kalibrációs előny** — erősen adat- és összevetés-függő.
2. **A „0% hallucináció" állítás és a tényleges pontossági rangsor feszültsége.** A TypeSafe maga írja: „Our number is not empirical. Schema matching is guaranteed, thus we can confidently add 0% into the plots." (typesafe.ai blog, T1) — vagyis ez csak azt garantálja, hogy a válasz szintaktikailag érvényes, nem azt, hogy helyes. Az agenccy.ai és az opentweet.io külön is felhívja a figyelmet arra, hogy ezt a marketingszám a sajtóban gyakran összemosódik a tényleges helyességgel: „A guaranteed-valid output is being marketed on the same chart as measured error rates, and a buyer reading it will conclude the model cannot be wrong. The company's own evals say otherwise — fourth on accuracy." (agenccy.ai)
3. **Ellentétes megállapítás arról, hogy több osztály rontja-e a kalibrációt/pontosságot.** Az általános elvárás (és a legtöbb forrás mintázata, pl. Banking77) az, hogy sok, átfedő osztály nehezebb. Ugyanakkor a primeline.cc pre-regisztrált tesztje explicit ennek ellenkezőjét találta az ő adatukon: „having more answer options does not make calibration worse either: the 5-level sentiment scale was harder to calibrate than the 77-option classifier, because the 5 levels are neighbours on a scale and Jev would confidently pick the level right next to the correct one, while the 77 categories are mostly unrelated to each other." Ez nem feltétlenül mond ellent a Banking77-es eredményeknek (ott más volt a mérőszám: pontosság, nem kalibráció), de érdemes jelezni, hogy „sok osztály = rosszabb" nem egyetemes szabály, a kérdéstípus (kategorikus vs. ordinális skála) legalább annyira számít.
4. **A gyorsulási szorzó (193,6x / 444,6x) és a független mérések közötti eltérés** közvetve érinti a megbízhatóság kérdését is: a WotAI ezt írja: „TypeSafe's landing page claims 20 to 200x, and I did not find the workload where that appears" — mérése 1,4–3,7x-es gyorsulást talált. A TrueStandard külön cikkben (2026-09-19) ezt árnyalja: „When we reproduced that shape [6 szekvenciális LLM-hívás egy batch Jev-hívással szemben], we measured 100.7x faster… When we compared a single classification call instead, we measured 1.7x. Both are correct measurements of different things." Ez nem pontossági, hanem sebességi ellentmondás, de mivel a felhasználói kérdés a Jev általános megbízhatóságára vonatkozik, érdemes jelezni: a fejenkénti szorzószámok nagyban függenek attól, mihez hasonlítjuk.

## Amire NINCS forrás

- **Magyar nyelvű teljesítménymérés** — sem pontosságra, sem kalibrációra, sem semmilyen más mérőszámra nem található közvetlen adat magyar nyelvű bemeneten. A magyar nyelvű médiamegjelenések (Mobilissimo.hu, nerdgeek.hu) csak a modell általános bemutatására szorítkoznak.
- **Tiszta, tanítás nélküli koszinusz-hasonlóságú beágyazás-osztályozóval (pl. sentence-transformer + centroid/kNN, kifejezetten mint önálló osztályozási módszer) végzett, számszerű összevetés a Jevvel** — csak minőségi állítások vannak arról, hogy ez „kategóriahiba", konkrét pontossági/ECE-szám nem található hozzá. A talált „embedding-szerű" összevetés (GLiClass) valójában egy NLI-alapú zero-shot modell, nem tiszta koszinusz-osztályozó.
- **Kifejezett, kontrollált teszt „ellentmondó állítások felismerésére" Noul-kérdéssel** (pl. két, egymásnak ellentmondó mondatot tartalmazó bemeneten explicit „van-e ellentmondás" kérdés) — csak közvetett adat van: a modell saját belső következetlensége (Noul vs. Choice eltérés, tagadás-összeg ≠ 1) ugyanarra a tényre, amit maga a TypeSafe dokumentál, de ez más jelenség, mint egy bemeneten belüli, két állítás közötti ellentmondás felismerése.
- **A TypeSafe „workflow evals" oldalának (a nyers számokat és a teljes módszertant tartalmazó oldal) közvetlen, elsőkézből való tartalma** — az oldal (`typesafe.ai/evals` és a blogban hivatkozott „workflow evals site") Exa-val nem volt lekérhető (`CRAWL_NOT_FOUND`), ezért a 67,8%/74,1%/61,8%/79,1% számokat csak másod-/harmadkézből (TechSpot és az őt megerősítő öt további forrás) sikerült megerősíteni, nem a gyártó saját oldaláról közvetlenül.
- **Pontos ECE/Brier-szám magára a TypeSafe hivatalos, saját méréséből** — ilyen, mint fent részletezve, nem létezik; minden számadat független, harmadik féltől származik.

## Meglátogatott és felderített linkek

| Cím | URL | Tier | Eszköz | Megjegyzés |
|---|---|---|---|---|
| Introducing System One Models and Jev (TypeSafe hivatalos blog) | https://typesafe.ai/blog/introducing-system-one-models-and-jev | T1 | Exa web_fetch_exa | Elsődleges forrás; leírja a „workflow eval" módszertant, de a konkrét számtáblát nem tartalmazza a lekért szövegben |
| typesafe.ai/evals | https://typesafe.ai/evals | — | Exa web_fetch_exa | Sikertelen lekérés (CRAWL_NOT_FOUND) |
| typesafe.ai/blog/jev-1-13-jaggedness | https://typesafe.ai/blog/jev-1-13-jaggedness | — | Exa web_fetch_exa | Sikertelen lekérés (CRAWL_NOT_FOUND) — a Noul/Choice-eltérés hivatalos „jaggedness" oldala, csak másodkézből (learnjev.com) idézhető |
| typesafe.ai/models | https://typesafe.ai/models | — | Exa web_fetch_exa | Sikertelen lekérés (CRAWL_NOT_FOUND), lásd sq00 is |
| Meet Jev: A New AI Model From One of ChatGPT's Co-Creators — TechSpot | https://www.techspot.com/article/3172-meet-jev/ | T2 | Exa web_fetch_exa | A 67,8%/74,1%/61,8%/79,1% szám elsődleges újságírói közlése |
| Is Jev actually calibrated? — Learn Jev | https://learnjev.com/concepts/calibration | T3 | Exa web_search_exa | Nem hivatalos, de technikai jellegű; ECE-hiány kritikája és független mérések összefoglalása |
| Jev topics — benchmarks — jevtypesafeai.com | https://jevtypesafeai.com/jev | T3 | Exa web_search_exa | Nem hivatalos; „every Jev benchmark you will see today is about speed, cost and calibration — not a public accuracy leaderboard" |
| TypeSafe Jev vs 15 other models, measured — WotAI | https://wotai.co/blog/typesafe-jev-vs-claude-haiku-tested | T2 | Exa web_search_exa | Független, 16 modelles, reprodukálható ECE/pontosság-teszt |
| Jev Accuracy Tested: 108 Claims Across Three Models — TrueStandard | https://truestandard.ai/blog/jev-accuracy-tested | T2 | Exa web_search_exa | Független, 108 kézzel címkézett állítás, ECE/Brier-számítással |
| jevkit-calibrate v0.1.0 — PyPI | https://pypi.org/project/jevkit-calibrate/ | T3 | Exa web_search_exa | Közösségi eszköz saját kalibráció-méréshez, jelzi a gyártói szám hiányát |
| jevcal v0.2.0 — PyPI | (jevcal PyPI oldal) | T3 | Exa web_search_exa | Hasonló közösségi kalibráció-mérő eszköz |
| Jev AI: the typed, calibrated decision model — jevtypesafeai.com | https://jevtypesafeai.com/jev-ai | T3 | Exa web_search_exa | Nem hivatalos termékbemutató oldal |
| Jev and RLCD: A Decision Model... — Saulius blog | https://saulius.io/blog/jev-rlcd-decision-model-calibrated-probabilities | T2 | Exa web_search_exa | RLCD-elemzés, Kev-9B/Nimble/Bespoke Labs eredmények aggregálása |
| Jev After Eight Days of Independent Tests — DEV Community (aws-builders) | https://dev.to/aws-builders/jev-after-eight-days-of-independent-tests-level-with-mid-price-llms-behind-the-frontier-1c60 | T2 | Exa web_search_exa | Legátfogóbb aggregáló cikk, sok elsődleges mérést újraszámol |
| Testing Jev on public and private data — Aman Kumar | https://amankumar.ai/blogs/jev-measured | T2 | Exa web_search_exa | ~16 000 hívás, 4 nyilvános + valós üzleti adat, „trust the ends, not the middle" |
| Measuring Jev — braindetox.kr | https://braindetox.kr/en/posts/jev_typesafe_classifier_filter_evaluation_2026.html | T2/T3 | Exa web_search_exa | Aman Kumar eredményeinek másodforrásos összefoglalása |
| Jev vs GPT and Claude: Independent Benchmark — AY Automate | https://www.ayautomate.com/blog/jev-vs-llm-benchmark | T2 | Exa web_search_exa | 791 döntés, McNemar-teszt, Wilson-intervallumok, AUROC |
| Is Jev Really 193x Faster? — TrueStandard | https://truestandard.ai/blog/is-jev-really-193x-faster | T2 | Exa web_search_exa | Sebesség-szorzó módszertani kritikája |
| TypeSafe Jev vs Claude Code: 4 Models, 2 Real Jobs — primeline.cc | https://primeline.cc/blog/typesafe-jev-pre-registered-test | T2 | Exa web_search_exa | Pre-regisztrált teszt, kérdéstípusonkénti kalibráció (Noul/Choice/Score) |
| Jev's 0% Hallucination Sits Beside a 67.8% Accuracy Score — agenccy.ai | https://agenccy.ai/news/jevs-0-percent-hallucination-sits-beside-a-678-percent-accuracy-score/ | T2 | Exa web_search_exa | A „0% hallucináció" és a pontossági rangsor közti feszültség elemzése |
| Benchmarking Jev: what a decision model can (and can't) do — DEV Community (aitejiu) | https://dev.to/aitejiu/benchmarking-jev-what-a-decision-model-can-and-cant-do-in-an-agent-harness-20po | T2 | Exa web_search_exa | 10 nyilvános adathalmaz, SNIPS/Banking77/MetaTool/RouterBench eredmények |
| TypeSafe AI 的 Jev 號稱快 193.6 倍？— DataSci Ocean | https://datasciocean.com/ai-concept/jev-overview/ | T2/T3 | Exa web_search_exa | Kínai nyelvű, több független forrást összesítő elemzés |
| Jev: AI koji ne priča, nego radi — Bug.hr | https://www.bug.hr/softver/jev-ai-koji-ne-prica-nego-radi-63035 | T3 (horvát tech média, de tartalma T1/T2-vel egyező) | Exa web_search_exa | 9 hibamód és nyelvi figyelmeztetés horvátul |
| Jev cannot write. That is the feature and the limit. — benchlm.ai | https://benchlm.ai/blog/posts/what-is-jev | T2 | Exa web_search_exa | Módszertani összefoglaló, saját (korlátozott) smoke teszttel |
| Jev vs a fine-tuned classifier — BERT, embeddings & cost — Jev Agent | https://jev-agent.com/jev-vs-classifier | T3 | Exa web_search_exa | Nem hivatalos, de technikai összevetés Jev / klasszikus osztályozó / embedding között |
| Jev vs Classifiers and Embeddings: Which to Use — jevaiguide.com | https://jevaiguide.com/compare/jev-vs-classifiers/ | T3 | Exa web_search_exa | Táblázatos összevetés Jev / fine-tuned / embeddings+kNN / zero-shot |
| Jev vs a 310M encoder I trained myself — Web Pulse | https://wpnews.pro/news/jev-vs-a-310m-encoder-i-trained-myself-750-rows-three-tasks-two-different | T2 | Exa web_search_exa | 3 japán feladat, McNemar-teszttel igazolt eredmények, GLiClass zero-shot összevetés |
| jevbench: Jev vs GPT-5-mini, Claude Sonnet 5, DistilBERT, BART NLI és Laya — madewithlaya.com | https://www.madewithlaya.com/builds/jevbench-classifiers | T3 (saját termék promóciója is) | Exa web_search_exa | Reprodukálható benchmark-keret, de a Laya (saját termék) javára is érdekelt lehet |
| Jev failure modes: 9 documented weaknesses — Learn Jev | https://learnjev.com/tutorials/failure-modes | T3 | Exa web_search_exa | A TypeSafe 9 hibamódjának részletes, TypeSafe-idézetekkel alátámasztott bemutatása |
| Jev Limitations: Known Weak Spots and Workarounds — jevaiguide.com | https://jevaiguide.com/jev-limitations/ | T3 | Exa web_search_exa | Ugyanaz a hibamód-lista, más megfogalmazásban |
| Jev primitives: Noul, Choice and Score — Learn Jev | https://learnjev.com/tutorials/three-primitives | T3 | Exa web_search_exa | A TypeSafe „jaggedness" oldaláról idézett Noul/Choice-eltérés és tagadás-összeg példák |
| Noul: Jev's Yes/No Question Type Explained — Jev AI Guide | https://jevaiguide.com/concepts/noul/ | T3 | Exa web_search_exa | Noul-viselkedés és következetlenség megerősítése saját teszttel |
| Jev Confidence and Calibration Explained — Jev AI Guide | https://jevaiguide.com/concepts/confidence/ | T3 | Exa web_search_exa | `confidence` mező vs. kalibráció fogalmi tisztázása |
| Is Jev confident? — Bernoulli.app | https://bernoulli.app/articles/is-jev-confident | T2 | Exa web_search_exa | 1 millió hívás alapján a `confidence` mező matematikai eredetének feltárása |
| Designing state for Jev — Learn Jev | https://learnjev.com/tutorials/writing-state | T3 | Exa web_search_exa | „Context rot" (hosszú/irreleváns bemenet) hivatalos TypeSafe-idézettel |
| Classify and Tag Text at Scale with Jev — OpenRouter cookbook | https://openrouter.ai/docs/cookbook/evaluate-and-optimize/jev-classification | T1 (gateway hivatalos dokumentációja) | Exa web_search_exa | TweetTopic 6-kategóriás teszt, 350/400 pontosság, kalibrációs bontás |
| Jev Confidence Thresholds: How to Choose Them — MrJev | https://mrjev.com/guides/confidence-thresholds/ | T3 | Exa web_search_exa | Noul-küszöbérték gyakorlati útmutató |
| Decoding Jev — Architecture, inference, and RLCD — navinpai.github.io | https://navinpai.github.io/decoding-jev/ | T2 | Exa web_search_exa | Architektúra-elemzés, túlzott magabiztosság és hőmérséklet-illesztés megjegyzése |

Kimenet mentve: `/home/claude/work/kutatas-jev/sq02-pontossag.md`
