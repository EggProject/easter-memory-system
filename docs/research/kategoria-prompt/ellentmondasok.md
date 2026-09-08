# Ellentmondások — ahol a források egymásnak ellentmondanak

Egyesítve: `sq04/contradictions.md` + `sq05/contradictions.md`. Mindkét oldal szó szerinti idézettel és forrással;
ahol van feloldás, jelölve; ahol nincs, "nyitva marad" jelzéssel.

---

## 1. A "hány eszköz/kategória fölött kell váltani" küszöb kb. 10x szórást mutat forrásonként (SQ-04)

| Forrás | Mit mér | Küszöb (szó szerint) |
|---|---|---|
| OpenAI hivatalos function-calling doksi | eszközszám / kör (turn) elején | „Aim for fewer than **20** functions… though this is just a soft suggestion.” |
| OpenAI hivatalos tool-search doksi | eszközszám / namespace | „aim to keep each namespace to fewer than **10** functions” |
| Anthropic hivatalos Tool Search Tool doksi | mikor kapcsold be | „**10 or more** tools available” VAGY „tool definitions consume more than **10k tokens**” |
| Anthropic hivatalos Tool Search Tool doksi | mikor romlik látványosan a választás | „degrades once you exceed **30–50** available tools” |
| Anthropic hivatalos Skills-útmutató (PDF) | hány skill legyen egyszerre engedélyezve | „Evaluate if you have more than **20-50** skills enabled simultaneously” |
| MCP hivatalos kliens-ajánlás | mikor váltás kontextusablak-arányban | „a threshold as a percentage of the context window. For example, **1%-5%**” |
| GitHub MCP fórum-beszélgetés (T3, anekdota) | eszközszám, gyakorlati tapasztalat | „**60-80 tools** works fine… Beyond **100**, you should definitely split” |
| „Lazy Skills” Substack (T3, nem ellenőrzött) | kulcsszó-alapú relevancia-észlelés | „Effective for fewer than **50** skills; beyond that, precision degrades” |

**Az ellentmondás jellege:** nincs egyetlen, egymásnak ellentmondó számpár ugyanarra a mértékegységre — hét-nyolc
forrás, hét-nyolc **különböző** mértékegységben (eszköz/kör, eszköz/namespace, összes elérhető eszköz,
token-összeg, kontextusablak-százalék, skill-darabszám) ad küszöböt, és ha mindet "darabszámra" vetítjük ki, a
tartomány 10-től 100-ig terjed. Nincs egyetlen iparági konszenzus-szám, csak egy nagyságrendi sáv.

**Feloldás:** ha a "10-20" ajánlásokat *belépési küszöbnek* (mikor érdemes elkezdeni figyelni / mikor kapcsold be
a funkciót), a "30-50"-et pedig *látható degradációs pontnak* (mikor már biztosan romlik a pontosság) tekintjük,
a két szám nem mond ellent egymásnak, csak két különböző kérdésre válaszol. Az Anthropic Tool Search Tool doksija
maga is ezt a két külön küszöböt adja meg egymás mellett. A fórum-anekdota (60-80/100) és a Substack-állítás
(50) nagyságrendileg még mindig ebbe a sávba esnek, csak a sáv magasabb végén — ezek magasabb (kevésbé
konzervatív) becslések, nem éles ellentmondás a hivatalos ajánlásokkal.

---

## 2. A RAG-MCP "pozíció szerinti" degradáció vs. az "N szerinti" degradáció összemosásának kockázata (SQ-04)

A RAG-MCP paper (arXiv 2505.03275) két, könnyen összekeverhető mérést közöl:

- **Baseline (Blank Conditioning, N eszköz egyszerre a promptban) pontossága: 43.13% vs 13.62%** — a RAG-MCP
  módszer és a "mindent egyszerre a promptba" módszer összevetése, NEM egy N-függő görbe.
- **Stressz-teszt N = 1-től 11100-ig, 26 intervallumban**, ahol a mért mennyiség a RAG-MCP SAJÁT visszakeresési
  pontossága a helyes eszköz *pozíciójának* függvényében:
  > "MCP positions below 30 exhibit… success rates above 90%"
  > "Beyond position ~100, purple dominates [signifying that retrieval precision diminishes]"

Ez a két szám NEM ugyanazt méri, és a forrásokban (másodkézből idéző blogok) néha egybemosva jelenik meg, mintha
"100 eszköz fölött a pontosság minden esetben 90%-ról zuhanni kezdene".

**Feloldás:** a két mérést szét kell választani — a "pozíció szerinti" szám a RAG-MCP retriever saját
teljesítménye, nem egy általános "N eszköz fölötti romlás" törvény. Nem éles forrás-vs-forrás ellentmondás, hanem
egy INTERPRETÁCIÓS kockázat egyetlen papíron belül, amit a jelen kutatás explicit módon külön tart.

---

## 3. A meta-tool minta "98.7%-os csökkenés" állítása nem igazolható (SQ-04)

A blog.synapticlabs.ai cikk azt állítja:
> "Anthropic's independent implementation achieved: 98.7% reduction in tool overhead."

Ez az állítás SEHOL nem található meg semmilyen Anthropic elsődleges forrásban (sem az advanced-tool-use
engineering blogban, sem a Tool Search Tool doksiban, sem a Skills-doksikban) — ott a legmagasabb közölt szám
85%-os csökkenés:
> "This represents an 85% reduction in token usage while maintaining access to your full tool library."
(https://www.anthropic.com/engineering/advanced-tool-use)

**Nyitva marad.** Lehet, hogy a blog szerzője egy nem publikus vagy meg nem talált forrásra hivatkozik, vagy
egyszerűen túlbecsüli/félreidézi a nyilvános 85%-os számot — ezt az állítást T3-as, ellenőrizetlen forrásként
kezeljük, és nem tényként használjuk (ld. `hianyok.md` #9).

---

## 4. "Koherens haystack rosszabb, mint kevert" (Chroma) vs. az általános "szervezett prompt jobb" tervezési tanács (Anthropic) (SQ-05)

**Chroma Context Rot (S2)** azt találta, hogy a mesterségesen összekevert, logikai folytonosság nélküli
kontextus JOBB eredményt ad, mint a koherens, logikusan felépített szöveg:
> "models perform worse when the haystack preserves a logical flow of ideas. Shuffling the haystack and removing
> local coherence consistently improves performance."
— https://www.trychroma.com/research/context-rot

Ezzel szemben **Anthropic saját hivatalos mérnöki irányelve (S11)** implicit módon az ellenkezőjét sugallja — a
jól szervezett, gondosan megkomponált kontextus a cél:
> "our overall guidance across the different components of context (system prompts, tools, examples, message
> history, etc) is to be thoughtful and keep your context informative, yet tight."
— https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

**Feloldás:** nem feltétlenül egymásnak ellentmondó állítások — a Chroma-megfigyelés egy szűk, mesterséges
needle-in-haystack elrendezésre vonatkozik (ahol a "koherencia" azt jelentette, hogy a needle körüli szöveg
tematikusan összefügg, ami megzavarhatja a modellt, hogy melyik mondat a releváns), míg az Anthropic-ajánlás
általános tervezési elv a tartalom MINŐSÉGÉRE (ne legyen felesleges, zajos token), nem a mondatok sorrendjére.
**Részben nyitva marad**: egy kategória-prompt-lista tervezésénél releváns eldönteni, hogy a kategóriákat
"logikus" csoportokba rendezve vagy inkább semlegesen listázva érdemes-e megadni — erre nincs egyértelmű,
konszenzusos válasz a forrásokban.

---

## 5. A "hosszú kontextus mennyire romlik" kérdésre a válasz erősen módszertan-függő — RULER (optimistább) vs. NoLiMa (pesszimistább) (SQ-05)

**RULER (S5)** — amely tartalmaz "könnyű", lexikai egyezésen alapuló visszakeresési feladatokat is — azt
találta, hogy a GPT-4 "effektív kontextushossza" 64K (128K hirdetett kapacitásból), és a legjobb modell
degradációja "csak" 15,4 pont 4K-ról 128K-ra:
> GPT-4: 96,6 (4K) → 81,2 (128K) — "the least but non-marginal degradation (15.4)"
— https://arxiv.org/html/2404.06654v1

**NoLiMa (S3)** — amely KIFEJEZETTEN úgy lett megtervezve, hogy KIZÁRJA a szó szerinti lexikai egyezés
lehetőségét (a needle és a kérdés között nincs szó szerinti átfedés) — sokkal drasztikusabb összeomlást mér, MÉG
RÖVIDEBB (32K-os) kontextusnál is:
> GPT-4o: 99,3% (rövid) → 69,7% (32K) — kb. 30 pontos esés MÁR 32K-nál, nem 128K-nál.
> "At 32K, for instance, 11 models drop below 50% of their strong short-length baselines."
> Disztraktorral: "GPT-4o now demonstrates an effective length of just 1K."
— https://arxiv.org/pdf/2502.05167

**Ez valódi, dokumentált feszültség, nem csak látszólagos**: ugyanarra a kérdésre ("mennyire tartja meg a modell
a teljesítményét hosszú kontextusban?") a két benchmark GYÖKERESEN eltérő képet ad.

**Feloldás:** a különbség oka pontosan azonosítható — a NoLiMa módszertanilag direkt válaszul íródott arra, hogy
a korábbi (RULER-szerű) benchmarkok "túl optimisták", mert lexikai kapaszkodót hagynak a modellnek (ez már magából
a NoLiMa címéből — "Beyond Literal Matching" — is következik). **A mi SQ-05 kérdésünk szempontjából ez különösen
fontos**: egy kategória-választási feladat (ahol a bejegyzés szövege és a kategória-leírás között ritkán van szó
szerinti átfedés, inkább szemantikai) módszertanilag KÖZELEBB áll a NoLiMa (pesszimistább) forgatókönyvhöz, mint a
RULER (optimistább) forgatókönyvhöz — tehát extrapolálva a NoLiMa-féle, drasztikusabb becslés a relevánsabb
támpont. A módszertani ok tisztázott, de **melyik szám a "helyes" abszolút becslés a mi konkrét use case-ünkre,
az nyitva marad** — egyik benchmark sem méri közvetlenül a kategória-választást.

---

## 6. Az instrukció-kompilátor haszna: "kevesebb egység jobb" — de csak GYENGE modelleknél (SQ-05)

Nem két forrás közötti, hanem EGY forráson belüli (S7, Instruction Stacking Collapse) feszültség, ami releváns a
6. alkérdésre: a sok külön instrukció egyetlen koherens blokká vonása
> "recovers up to +11 points of follow rate for weaker models... while leaving stronger models, which already
> internalise the same structure, essentially unchanged" (Sonnet-nél: −1,2pp, azaz gyakorlatilag nincs haszna.)
— https://arxiv.org/html/2608.02639

**A feszültség:** a "kevesebb, jól szervezett > sok külön szétszórt" elv NEM egyetemes igazság — erős modelleknél
gyakorlatilag közömbös, csak gyenge modelleknél számít.

**Feloldás:** nem ellentmondás, hanem modell-függőség — mindkét irány igaz, csak más-más modellképesség mellett.
**Nyitva marad**, hogy ez a modellfüggés hogyan vetítendő át egy adott, konkrét hívó agentre (pl. Claude Opus
esetén valószínűleg elhanyagolható a hatás, egy kisebb/nyíltabb modellnél viszont nem) — ezt a forrás (preprint,
nem peer-reviewed) sem méri minden lehetséges modellre.

---

## Megjegyzés a forráskeverésről

A fenti 1-3. pont az `sq04/contradictions.md`-ből, a 4-6. pont az `sq05/contradictions.md`-ből származik
változatlan tartalommal, csak egy dokumentumba egyesítve. Az SQ-01/02/03 anyagban (`claims.jsonl`) nem található
külön dokumentált, két forrás közötti nyílt ellentmondás — az ottani sub-agent nem vezetett külön
`contradictions.md`-szerű naplót; ahol két forrás eltérő számot közöl ugyanarra a jelenségre (pl. MetaTool és
LongFuncEval eltérő %-os degradációs sávjai, ld. `allitasok.csv` SQ-02-C015 és SQ-02-C017), azt önmagában nem
tekintettük "ellentmondásnak", mert különböző benchmarkokról, különböző modellhalmazokról van szó — ez inkább az
"1. pontban" leírt, mértékegység/módszertan-függő szórási jelenség egy további példája, nem éles cáfolat.
