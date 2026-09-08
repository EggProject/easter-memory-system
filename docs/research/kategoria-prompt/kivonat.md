# Kivonat — A kategória-választó prompt mérete (token-korlát, darabszám, leírás-hossz)

*Kutatási kivonat a `.research/kategoria-prompt/` alatti anyagból. Dátum: 2026-09-06.
Ez a dokumentum a meglévő kutatási jegyzeteket (claims.jsonl fájlok, SQ-04/SQ-05
findings/megallapitasok, links, gaps, contradictions) foglalja össze összefüggő magyar
szövegben — nem tartalmaz új keresést, és nem tartalmaz szintézist vagy ajánlást.*

---

## 1. Mire kerestünk választ

A vizsgált rendszerben minden memória-kategóriához tartozik egy „prompt": egy szöveges
leírás arról, milyen bejegyzés tartozik az adott kategóriába. Amikor egy külső, memóriát
író agent (lehet Claude, Codex, vagy bármelyik más LLM-alapú kliens) új bejegyzést akar
elhelyezni, nem egyetlen kategória leírását kapja meg — hanem **az összes létező
kategória promptját egyszerre**, mert ezek közül kell választania. A kutatás kiindulási
kérdése az volt, hogy ehhez a helyzethez milyen **token-alapú ajánlott felső határ**
adható, és hogyan függjön ez a határ a kategóriák darabszámától: ha valaki sok
kategóriát szeretne, az egyes leírásoknak rövidebbnek kell lenniük, és fordítva. A
tervezett viselkedés nem tiltás, hanem erős jelzés (figyelmeztetés) a küszöb átlépésekor.

A kutatást indító vezetői felismerés, amit direkt igazolni vagy cáfolni kellett, a
következő volt: mivel a hívó agenthez ténylegesen egyetlen, összefüggő utasítás-blokk
kerül — az összes kategória-leírás egymás után fűzve —, a releváns korlátnak nem a
darabszámra és nem az egyenkénti hosszra **külön-külön** kell vonatkoznia, hanem **a
kettő szorzatára**: arra a teljes token-mennyiségre, ami ténylegesen bekerül a hívó agent
kontextusába egyetlen döntési helyzetben.

Ezt a kérdést öt al-kérdésre bontva vizsgáltuk: (SQ-01) mennyibe kerül tokenben egy
leírás és hol a gyakorlati plafon; (SQ-02) hogyan romlik a választás pontossága a
választható elemek *számának* növekedésével; (SQ-03) hogyan romlik az egy elemre jutó
*leírás hosszának* növekedésével; (SQ-04) mit ír elő saját magának a gyakorlatban több
valós rendszer (Anthropic, OpenAI, MCP-specifikáció, kutatási prototípusok); és (SQ-05)
van-e mért bizonyíték arra, hogy egy nagy utasítás-blokk jelenléte nemcsak a
kategória-választást, hanem a hívó agent *egyéb, ettől független feladatát* is rontja. Egy
korábbi kutatási kör (2026-08-23) már megállapította, hogy a valós rendszerek jellemzően
3–15 kategóriát használnak, hogy egy erős modell (GPT-4) zero-shot besorolási pontossága
3/18/60 kategóriánál kb. 0,54–0,72 / 0,59–0,67 / 0,62–0,72 között mozgott, hogy a Claude
skill-dokumentáció 1024 karakteres leírás-limitet ír elő, és hogy egy tanulmány szerint
„increasing prompt context sometimes decreases accuracy" — ezeket az adatokat e kör nem
kutatta újra, csak épít rájuk.

## 2. SQ-01 — Mennyibe kerül tokenben egy leírás

**Konkrét mért méretek.** Anthropic saját `count_tokens` végpontján egy rendszerprompt +
rövid felhasználói üzenet önmagában 14 input tokent fogyaszt; ugyanez egyetlen egyszerű,
egyparaméteres eszközdefinícióval (`get_weather`) kiegészítve már 403 input tokent —
tehát egyetlen minimális eszközleírás ára itt kb. 390 token
(`platform.claude.com/token-counting`). Anthropic egy másik hivatalos anyaga szerint egy
öt MCP-szerveres (GitHub 35, Slack 11, Sentry 5, Grafana 5, Splunk 2 eszköz, összesen 58)
beállítás **kb. 55 000 tokent** emészt fel a definíciókban, mielőtt a beszélgetés
elkezdődne; egy másik, „hagyományos megközelítésnek" nevezett példában 50+ MCP-eszköz
definíciója előre betöltve **kb. 72 000 tokent** tesz ki; és Anthropic azt írja, hogy
belső eszközkészleteknél a definíciók már **134 000 tokenre** is felduzzadtak
optimalizálás előtt. Ezek a számok Anthropic saját termékére (Claude, MCP-integráció)
vonatkozó, saját méréssel alátámasztott állítások, ezért — a feladat szigorú szabálya
szerint — **T2**-nek, nem T1-nek minősülnek, még akkor is, ha hivatalos dokumentációs
oldalon szerepelnek.

Ugyanez az anyag mutatja be a Tool Search Tool nevű funkciót, ami a fenti terhelést a
keresőeszköz maga (~500 token) plusz 3–5 ténylegesen felfedezett eszköz (~3000 token) —
összesen **kb. 8700 token** — szintre csökkenti a korábbi ~77 000 tokenhez képest, azaz
kb. **85%-os csökkenés** (T2, saját mérés). Egy nem hivatalos, degradált-lekérésű GitHub
issue (T3, ellenőrizetlen felhasználói állítás) szerint a valós MCP-eszközdefiníciók
5–15-ször több tokent fogyasztanak, mint amennyi a minimális sémához szükséges lenne, és
egy tipikus, 20–30 regisztrált MCP-eszközt használó Claude Code munkamenetben a
séma-definíciók önmagukban 15–30 KB kontextust foglalnak el, mielőtt egyetlen
felhasználói üzenet is elhangzana.

**Karakter/token-limitek konkrét számokban.** Az Anthropic Agent Skills specifikációja
kőkeményen 1024 karakterben maximálja a skill `description` mezőjét (nem lehet üres, nem
tartalmazhat XML-taget) — ezt egy valós eset is megerősíti: Anthropic saját, csomagolt
`claude-api` skillje 1068 karakteres leírással jelent meg, ami *meghaladta* a platform
saját 1024-es limitjét, és a validáció el is utasította (`Actual: 1068; allowed maximum:
1024.`) — ez bizonyítja, hogy a limit ténylegesen érvényesített szabály, nem csak ajánlás
(T3, GitHub issue). Az OpenAI function-calling API-ja ugyanígy kemény validációs hibát dob
1024 karakter fölötti eszközleírásnál (`Invalid 'tools[1].function.description': string
too long. Expected a string with maximum length 1024...`, T3, fórumbejegyzés egy hibaüzenet
idézésével). Ezzel szemben a hivatalos Model Context Protocol specifikáció a tool NÉV
hosszára ad csak SHOULD-szintű ajánlást (1–128 karakter), a tool LEÍRÁS mezőt viszont
puszta szabad szövegként definiálja („Human-readable description of functionality"),
**semmilyen numerikus karakter- vagy token-limit nélkül** — ez éles kontraszt Anthropic és
OpenAI kemény 1024-es korlátjához képest.

Az Anthropic Agent Skills rendszerének progresszív feltárása konkrét token-költség
táblázatot közöl: a Level 1 metaadat (`name` + `description`, mindig betöltve minden
kérésnél) kb. **100 token/skill**; amíg egy skill nincs kiválasztva, csak ez a metaadat
foglal helyet — ezért sok skill telepíthető kontextus-büntetés nélkül; a Level 2 (a
SKILL.md törzse, csak kiváltáskor töltődik be) ajánlottan **5000 token alatt** marad.

**Nyelvi szorzó — miért drágább magyarul.** Egy magyar nyelvű technikai blog szerint egy
adott hosszúságú magyar szöveg általában **kb. kétszer annyi** tokenből áll, mint az
angol megfelelője, a kínai, japán, koreai vagy hindi nyelveknél pedig ez a különbség
**akár 5–10-szeres** is lehet. Ugyanez a forrás megjegyzi, hogy egy önálló magyar
ékezetes betű (pl. „Ű") önmagában két tokenre bomolhat, mert a bájt-szintű tokenizáló
számára a nem-ASCII karakterek több bájtot igényelnek:

> „Emiatt egy adott hosszúságú magyar szöveg általában nagyjából kétszer annyi tokenből
> áll össze, mint az angol nyelvű változata."
— https://webdevcenter.hu/chatgpt-magyarul-dragabb/

> „Például, egy „Ű" betű önmagában is két tokenből áll össze."
— https://webdevcenter.hu/chatgpt-magyarul-dragabb/

Ezt egy peer-reviewed (NeurIPS 2025) tanulmány is alátámasztja általánosabb szinten: a
magas „token-prémiumú" nyelvek (amelyeknél ugyanaz a szövegtartalom több tokent igényel)
alacsonyabb tanítási átviteli sebességet és magasabb inferencia-költséget szenvednek el, és
a tanulmány szerint a tokenizáló tanítóadata és a tesztszöveg közti hasonlóság **nem**
magyarázza a nyelvek közti token-prémium különbségeket — vagyis a jelenség strukturális,
nem egyszerűen "kevesebb tanítóadat" kérdése. Fontos technikai megjegyzés: Anthropic
dokumentációja szerint a Claude 4.7 és újabb modellek (és a Claude Mythos Preview) egy
újabb tokenizálót használnak, ami ugyanarra a szövegre **kb. 30%-kal több** tokent termel,
mint a korábbi Claude-modelleken — tehát a token-számokat modellgenerációnként újra kell
mérni, nem vihetők át egyik modellről a másikra.

## 3. SQ-02 — Hogyan romlik a pontosság a darabszám növekedésével

**A görbe alakja: meredek kezdeti esés, majd ellaposodás — de van, ahol szikla.** A
MetaTool-benchmark eredménye szerint a helyes eszközválasztási arány (CSR) szinte minden
tesztelt LLM-nél csökken, ahogy a felkínált eszközlista hossza nő, és a csökkenés
**legmeredekebb szakasza a top-5 és a top-10 tartomány között** koncentrálódik, nem
egyenletesen oszlik el a teljes tartományon. A ChatGLM2 modellnél ez konkrétan: 82,29% (5
elem) → 56,19% (10 elem, 26 pontos esés) → 48,07% (15 elem, további 8 pontos esés) — azaz
meredek esés, majd ellaposodás mintázata. Ezzel szemben a LongICLBench cikk valódi
sziklaperemet talált: 174 címke esetén (Discovery diskurzus-reláció feladat) minden
tesztelt modell, a GPT-4-Turbót is beleértve, majdnem nulla pontosságra omlott, mert a
modellek már magát a feladatdefiníciót sem tudták értelmezni ekkora címketérnél.

**Modellek közötti nagy szórás.** A LongFuncEval hét modellen (hat nyílt súlyú, egy zárt,
mind 128K kontextusú) mérve **7%-tól 85%-ig terjedő** teljesítménycsökkenést talált, ahogy
nő az eszközkatalógus mérete — ez a legszélesebb szórás, amit a kutatás egyáltalán talált
egyetlen jelenségre, ami azt jelzi, hogy nincs egyetlen univerzális görbe, a modellek
között hatalmas a különbség. Ezt erősíti meg a LongICLBench Banking77-es (77 osztályos)
mérése is: GPT-4-Turbo 84,4%-ot ér el, míg egy 7 milliárd paraméteres nyílt modell
(Qwen-1,5-7B) csak 67,8%-ot, a Mistral-7B pedig 64,0%-ot — vagyis ugyanaz a kategóriaszám,
amit egy frontier modell viszonylag jól kezel, egy kisebb, nyílt modellnek már komoly
probléma. A label-space-reduction (LSR) tanulmány szerint ez a mintázat rendszeres:
átlagosan a Llama-3.1-70B **7,0%**, a Gemma-2-27B **5,1%**, a Qwen2.5-72B **4,9%**, a
Claude-3.5-Sonnet pedig csak **3,3%** macro-F1-et nyer a címketér szűkítéséből — a
kisebb/gyengébb modellek sokkal többet nyernek, mint az erős, zárt modellek.

**Konkrét eszközszám-lépcsők, letisztult mérésekkel.** A „How Many Tools Should an LLM
Agent See" tanulmány BFCL-en (370 valós eszköz) azt találta, hogy fix K=20 eszköz
87,5%-os, fix K=50 pedig 90,8%-os lefedettséget ad, míg egy adaptív policy 90,3%-os
lefedettséget ér el mindössze átlag 7,4 eszközzel megmutatva — azaz közel ugyanazt a
teljesítményt hétszer kevesebb eszköz megmutatásával. Egy Claude Sonnet 4.6-tal futtatott
downstream teszten közepes nehézségű kérdéseknél (a helyes eszköz a 2–5. helyen van a
felkínált listában) a pontosság **60,9%** fix 5-elemű listánál, **72,0%** fix 10-elemű
listánál, **76,0%** fix 20-elemű listánál — tehát a puszta listaméret önmagában 15
százalékpontot mozgat a pontosságon. A RAG-MCP tanulmány szerint, ha az LLM közvetlenül,
előszűrés nélkül választ egy nagy/növekvő MCP-eszközkészletből, mindössze **13,62%**
pontosságot ér el, míg egy előzetes visszakeresési lépéssel (ami leszűkíti a jelölteket)
ez **43,13%**-ra nő — 3,2-szeres különbség pusztán attól, hány eszközt lát egyszerre a
modell.

**A hasonlóság (konfúzió) legalább annyira számít, mint a puszta darabszám.** A Zep
memóriarendszer hivatalos dokumentációja explicit tervezési elvként mondja ki, hogy az
entitás-/él-típusok leírásainak kölcsönösen kizárónak kell lenniük, mert az átfedő vagy
kétértelmű leírások következetlen LLM-osztályozáshoz vezetnek — és kifejezetten
megkülönbözteti a NÉV-átfedést a LEÍRÁS-átfedéstől:

> „Overlapping or ambiguous descriptions lead to inconsistent classification, because
> there is no single correct type for the fact."
— https://help.getzep.com/customizing-graph-structure

> „Overlapping names are fine as long as the descriptions make the types genuinely
> distinct."
— https://help.getzep.com/customizing-graph-structure

Ezt kísérletileg is alátámasztja két tanulmány. Az „On the Robustness of Agentic Function
Calling" azt mérte, hogy ha a kérdést változatlanul hagyva mindössze kb. 3, szemantikailag
hasonló „csali" eszközt adnak a toolkithoz (átlagosan 2,7-ről 5,6 eszközre nőve), az
kilenc vezető modellnél (Llama3.1-70B, Llama3.3-70B, DeepSeek-V2.5, Qwen2.5-72B,
Granite3.1-8B, Claude-3.5-Haiku, Claude-3.5-Sonnet, GPT-4o-mini, o1-mini) 1–8
százalékpontos relatív pontosságesést okozott — ez lényegesen KISEBB, mint a
puszta-átfogalmazásból (a kérdés más megfogalmazása, a toolkit változatlanul hagyása
mellett) adódó 8–19 százalékpontos esés. A domináns hibamód nem a szintaxis (rossz
formátum), hanem a rossz FÜGGVÉNY kiválasztása és a rossz PARAMÉTER-hozzárendelés egy
egyébként jól kiválasztott függvényhez — azaz a modell zavara arról szól, MELYIK
majdnem-egyforma eszközt/mezőt válassza, nem arról, hogyan formázza a hívást. A
label-space-reduction tanulmány is megerősíti ezt: amikor a címkék finomabb szemcsézettek
és hasonlóbbak egymáshoz (pl. „Intent" szint), nagyobb optimális k (látható címkeszám)
szükséges, mint amikor a címkék durvábbak és jobban elkülönülnek (pl. „Scenario" szint)
ugyanazon a doménen — vagyis nem a nyers darabszám, hanem a kategóriák egymáshoz való
szemantikai közelsége szabja meg, mekkora látható választék még kezelhető.

**Amikor a módszer kompenzál a darabszám ellen.** Retrieval-alapú few-shot választással
(azaz nem statikus, hanem a bejegyzéshez releváns few-shot példák dinamikus
kiválasztásával) a Llama-2-70B magas pontosságot tartott meg még nagy címkeszámnál is:
92,11% a Banking77-en (77 osztály), 91,73% a HWU64-en (64 osztály), 98,18% a Clinc150-en
(150 osztály), 10-shot mellett — vagyis a puszta darabszám önmagában NEM omlasztja össze
a pontosságot, ha a promptépítési módszer kompenzál. Ugyanígy egy már kicsi (K=11 osztály,
Mtop Domain adathalmaz) feladatnál minden tesztelt modell már 95% feletti pontosságot ért
el — a benchmark telített volt, a címketér-szűkítésnek nem volt hova javítania. Egy
külön, érdekes eredmény: pusztán a teljes (nem szűkített) címkelista *újrarangsorolása* —
a valószínűbb címkék előre hozása anélkül, hogy bármit eltávolítanánk — önmagában a
lehetséges maximális javulás **78,6%-át** hozza; a tényleges címketér-szűkítés csak a
maradék **21,4%-ot** teszi hozzá.

## 4. SQ-03 — Hogyan romlik a leírás hosszával

**Inverz-U / csökkenő hozam mintázat.** A „Navigating the Prompt Space" tanulmány
(GPT-4o és Gemini 2.0 Flash, 2×2×2 faktoriális elrendezés: címke-leírás mélysége,
instrukciós „nudge"-ok, few-shot példák jelenléte/hiánya) kimondja:

> „a minimal increase in prompt context yields the highest increase in performance, while
> further increases in context only tend to yield marginal performance increases
> thereafter"
— arXiv 2603.25422, Abstract

> „Alarmingly, increasing prompt context sometimes decreases accuracy."
— arXiv 2603.25422, Abstract

Vagyis a legelső, minimális kontextus-bővítés (a semmiből egy komponensre) hozza a
legtöbb javulást, minden további hozzáadás egyre kevesebbet ad, és bizonyos
konfigurációkban a pontosság ténylegesen ROMLIK a több kontextustól. A tanulmány
konklúziója óva int attól, hogy csak a feladathoz feltétlenül szükséges minimális
információt tartalmazó promptot használjunk — legalább egy kontextus-komponens
hozzáadása jobb, mint a puszta minimum. Ugyanakkor a hatás erősen heterogén: modellenként
(GPT-4o vs. Gemini 2.0 Flash), feladatonként és batch-mérettől (hány szöveget küldünk egy
hívásban) függően eltérő, ami arra utal, hogy nincs univerzális szabály. A GPT-4o
weighted F1-je az érzelem-detektálási feladatban a különböző konfigurációk és batch-méretek
között kb. **0,75 és 0,90 között** szórt.

**Constraint-halmozás: minél több megkötés egy instrukcióban, annál rosszabb a
teljesítés.** A FollowBench-benchmark, amely szigorúan egyesével adja hozzá a
megkötéseket ugyanahhoz az alap-instrukcióhoz (L1=1 megkötés … L5=5 megkötés), azt
találta, hogy a GPT-4-Preview-1106 „Hard Satisfaction Rate"-je **84,7%-ról (L1) 61,9%-ra
(L5)** esik, ahogy 1-ről 5-re nő az egy instrukción belüli megkötések száma — vagyis maga
a megkötés-SZÁM (nem a szöveg hossza általában, hanem a bennük lévő elvárások
felhalmozódása) rontja a végrehajtást.

**Séma-elhelyezés hatása — hova kerüljön a kategória-definíció.** A „Your Prompt is Not
the Only Prompt" tanulmány kifejezetten azt méri, mi történik, ha ugyanazt a
kategória-definíciós szöveget (azonos tartalom, azonos hossz) áthelyezik a rendszerprompt
és egy séma-/mezőleírás (pl. egy tool-paraméter `description` mezője) között:

> „schema placement underperformed system prompts by 11–13 percentage points"
— arXiv 2608.08254, Abstract

Ez GPT-4.1-nél és GPT-5.4-nél is fennállt, **még akkor is, amikor a két csatorna
tartalma megegyezett** — tehát pusztán az elhelyezés (rendszerprompt vs. séma) 11-13
százalékpontot számított, azonos tartalom mellett. Ha a séma-szintű leírás
ELLENTMOND a rendszerprompt kategória-definíciójának, a hatás drasztikus lehet: a Claude
Haiku 4.5 pontossága **52,5%-ról 7%-ra** (45,5 pontos esés) zuhant — ami azt mutatja, hogy
a séma-szintű instrukció csendben felülírhatja a prompt-szintű instrukciót. Pozitív
oldalról: egy kötelező köztes „indoklás" mező beillesztése a válaszmező elé a sémán belül
(mielőtt a modell megadná a végső címkét) **15–24 százalékponttal** javította a
séma-only pontosságot, minden tesztelt elhelyezés-változtatásnál nagyobb hatással.

**Anthropic saját tapasztalata: a leírás minősége, nem csak hossza, számít.** Anthropic
„Writing Effective Tools for AI Agents" cikke szerint az eszközleírások precíz
finomítása (nem pusztán a hosszuk növelése) vitte a Claude Sonnet 3.5-öt
állam-a-legjobb (SOTA) szintre a SWE-bench Verified benchmarkon (T2, saját termékről szóló
teljesítmény-állítás). A cikk egy konkrét, mért példát is hoz a tömörség hasznáról: egy
„tömör" válaszformátum kb. harmadannyi tokent használt, mint a „részletes" (72 vs. 206
token ugyanahhoz az adathoz), a technikailag alacsony értékű azonosítók elhagyásával (T2).
Egy másik konkrét eset: egy termelési hibát — amikor Claude szó szerint a „2025" évszámot
fűzte a keresési lekérdezésekhez, torzítva a találatokat — kizárólag az eszközLEÍRÁS
szövegének finomításával javítottak ki, kódmódosítás nélkül. Anthropic tervezési elve
explicit módon a sparse/kétértelmű leírásokat diagnosztizálható hibaforrásnak tekinti: a
gyakori, érvénytelen paraméterekre vonatkozó hibák azt jelzik, hogy a leírás nem elég
világos vagy nincs elég példa hozzá.

**Pozitív megfogalmazás elve (kapcsolódó, de nem hossz-specifikus megfigyelés).** Egy
független blog (amely maga is explicit módon jelzi, hogy anekdotikus Reddit-beszámolókra
támaszkodik, nem kontrollált kísérletre), Anthropic hivatalos prompt-engineering
útmutatására hivatkozva idézi az elvet:

> „Tell Claude what to do instead of what not to do."
— eval.16x.engineer, „The Pink Elephant Problem"

vagyis a tiltó megfogalmazás (pl. „Ne használj markdownt") helyett a pozitív instrukciót
(pl. „írj folyó szövegű bekezdésekben") ajánlja — ez nem közvetlenül a hosszról szól, de
releváns arra, HOGYAN kerüljön be egy kategória-leírásba egy megkötés, ha már bekerül.
Végül egy tágabb, nem méréses megállapítás egy másik tanulmányból: a tool-interfészek
(természetes nyelvű leírások + paraméter-sémák) általában ember-orientáltak maradnak, és
gyakran szűk keresztmetszetté válnak, amikor az agentnek sok jelölt közül kell választania.

## 5. SQ-04 — Mit írnak elő maguknak a valós rendszerek

**A kutatás egyik legkonkrétabb, hivatalos forrásból származó eredménye.** Az Anthropic
Tool Search Tool dokumentációja szó szerint, számszerűen kimondja, mikor érdemes
bekapcsolni a lusta eszközbetöltést, és mikor kezd biztosan romlani a pontosság:

> „Use tool search when any of the following apply: You have 10 or more tools available.
> Your tool definitions consume more than 10k tokens. Tool selection accuracy drops as
> your toolset grows. You aggregate multiple MCP servers (200+ tools). Your tool library
> grows over time."
— https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool

> „Claude's ability to pick the right tool degrades once you exceed 30–50 available
> tools."
— ugyanaz a forrás

Ezt a két mondatot két, egymástól független, eltérő promptú lekéréssel is
kereszt-ellenőrizték, és szó szerint egyezett — ez a kutatás legmegbízhatóbb, legdirektebb
találata arra a kérdésre, hogy van-e explicit iparági küszöbszám. Fontos: ez a küszöb
maga **T1** (dokumentált konfigurációs irányelv), de a hozzá tartozó %-os
teljesítményjavulási számok (lásd lentebb) **T2**, mert Anthropic saját termékéről szóló
mérések.

**Az Agent Skills rendszer saját, dokumentált darabszám-küszöbe.** A hivatalos,
letölthető Anthropic skill-építési útmutató „Large context issues" hibaelhárítási
szakasza, „Reduce enabled skills" pont alatt:

> „Evaluate if you have more than 20 - 50 skills enabled simultaneously — Recommend
> selective enablement — Consider skill 'packs' for related capabilities"
— https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf

Ez a legkonkrétabb, hivatalos Anthropic-forrásból származó darabszám-küszöb az egész
kutatásban: 20–50 egyszerre bekapcsolt skill fölött már érdemes felülvizsgálni, tényleg
mindegyik kell-e. Ugyanennek a rendszernek van egy „100+ elérhető skill"
tervezési-feltételezése is a best-practices dokumentációban:

> „The description is critical for skill selection: Claude uses it to choose the right
> Skill from potentially 100+ available Skills."
— https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

Ez azonban nem mért felső határ, csak tervezési feltételezés.

**A Model Context Protocol hivatalos, protokoll-szintű ajánlása — a legszorosabban
„szorzat-szerű" küszöb, amit találtunk.** A modelcontextprotocol.io hivatalos
kliens-ajánlása (nem egyetlen gyártó terméke, hanem maga a protokoll-specifikáció)
explicit módon a teljes kontextusablak arányában adja meg a küszöböt:

> „Progressive discovery is best used when tool definitions take large parts of the
> context window... We recommend that clients implement thresholds to determine when to
> switch: Implement a threshold as a percentage of the context window. For example,
> 1%-5%."
— https://modelcontextprotocol.io/docs/2026-07-28/develop/clients/client-best-practices

Ugyanez a dokumentum egy „catalog → inspect → execute" háromrétegű mintát ír le (előbb
egy kis meta-eszköz keres az elérhető képességek közt, majd csak a kiválasztott jelölt
teljes definícióját tölti be, végül hajtja végre) — ez pontosan a „hierarchikus menü:
először kategória, aztán az abban lévő elemek" minta egy hivatalosan dokumentált,
elnevezett változata —, valamint négy konkrét felfedezési stratégiát (kulcsszó-alapú,
embedding-alapú, szubagent-alapú, hibrid) és egy namespace-elvet: „Group tools by server:
Present tools organized by their source server so the model can reason about related
capabilities."

**OpenAI hivatalos ajánlásai.** Az OpenAI function-calling dokumentációja szerint
„aim for fewer than 20 functions… though this is just a soft suggestion", a
tool-search-dokumentáció pedig szűkebb, namespace-enkénti ajánlást ad: „aim to keep each
namespace to fewer than 10 functions for better token efficiency and model performance."

**Az összes explicit küszöbszám egy táblázatban** (mértékegység szerint csoportosítva,
mert nincs egyetlen közös mértékegység):

| Forrás | Mit mér | Küszöb |
|---|---|---|
| OpenAI, function-calling doksi (T1) | eszközszám / kör (turn) elején | „fewer than **20** functions" (soft suggestion) |
| OpenAI, tool-search doksi (T1) | eszközszám / namespace | „fewer than **10** functions" |
| Anthropic, Tool Search Tool doksi (T1) | mikor kapcsold be | „**10 or more** tools" VAGY „more than **10k tokens**" |
| Anthropic, Tool Search Tool doksi (T1) | mikor romlik látványosan | „degrades once you exceed **30–50** available tools" |
| Anthropic, Skills PDF-útmutató (T1) | hány skill legyen egyszerre engedélyezve | „more than **20-50** skills enabled simultaneously" |
| MCP hivatalos kliens-ajánlás (T1) | kontextusablak-arány | „a threshold... **1%-5%**" |
| MCP GitHub-fórum (T3, anekdota) | eszközszám, gyakorlati tapasztalat | „**60-80** tools works fine... Beyond **100**, you should definitely split" |

**A retrieval mint megoldás: javít, de nem csodaszer.** A RAG-MCP tanulmány (T1) egy
4400+ szerveres MCP-regiszteren mérve azt találta, hogy az „összes eszközleírást egyszerre
a promptba tesszük" alapmódszer 13,62% pontosságot ér el, retrieval-lel viszont 43,13%-ot
(„more than triples tool selection accuracy"), miközben a prompt-token-szám átlagosan
2133,84-ről 1084,00-re csökken. A stressz-teszt (N=1-től 11 100-ig) azt mutatja, hogy a
helyes eszköz pozíciója alatt 30 a retrieval saját sikerrátája 90% fölötti, 30-70 között
csökken (mert nő a szemantikai átfedés az MCP-leírások között), 100 fölött pedig már
számottevően romlik. Fontos, hogy ez a RAG-MCP RETRIEVERÉNEK saját pontosságát méri a
találat pozíciójának függvényében, nem az „összes eszköz a promptban" alapmódszer
N-függő görbéjét — a kettőt nem szabad összekeverni (lásd 7. pont). A retrieval azonban
maga sem tökéletes megoldás nagy méretekben: a „Retrieval Models Aren't Tool-Savvy"
tanulmány (ACL Findings 2025, T1) 43 000 eszközös korpuszon még a legjobb kereskedelmi IR-
modellnél (NV-Embed-v1) is csak 33,83-as nDCG@10-et mért, és minden tesztelt retriever
35% alatt maradt Completeness@10-ben, illetve 52% alatt recall@10-ben — vagyis a
retrieval-alapú megközelítés jobb, mint a naiv „mindent a promptba" módszer, de maga is
nehéz, messze nem tökéletes feladat nagyon nagy eszköztérben.

**Amit NEM találtunk.** Egyetlen forrás sem fogalmazza meg explicit módon a
„darabszám × átlagos leírás-hossz" SZORZATOT mint önálló, névvel illetett metrikát vagy
küszöböt — minden hivatalos küszöb az EREDMÉNY (összesített) token-számra vonatkozik (10k
token; kontextusablak 1-5%-a), ami matematikailag ekvivalens a szorzattal, de a
forrásokban nem így, hanem végeredményként van megfogalmazva. Nem találtunk kontrollált,
publikált kísérletet KIFEJEZETTEN „sok, hosszú leírású kategória közötti választásra" — a
mért adatok szinte mind eszköz-/API-/skill-VÁLASZTÁSRA vonatkoznak, ami analóg, de nem
azonos probléma a memória-kategorizálással.

## 6. SQ-05 — Rontja-e az utasítás-blokk a hívó agent saját feladatát

**Őszinte kiinduló válasz: nincs olyan tanulmány, amely pontosan ezt a konfigurációt
tesztelte volna** — egy VÁLASZTHATÓ (nem betartandó) kategória-menü mérete és egy attól
FÜGGETLEN, saját feladat minősége közötti összefüggést. Ez tényleges kutatási rés. Az
alábbiakban élesen elválasztva mutatjuk be, mi a KÖZVETLEN mérés, és mi csak ANALÓGIA.

### Közvetlen mérés

A legszorosabb (bár még mindig nem azonos konfigurációjú) találat egy 2026 márciusi,
nem peer-reviewed Microsoft-preprint (Mittal, „Did You Forget What I Asked? Prospective
Memory Failures in Large Language Models"), amely kifejezetten azt méri, hogy egy
formázási megkötés jelenléte ront-e egy TŐLE FÜGGETLEN feladat pontosságán:

> „Interference is bidirectional: formatting constraints can also reduce task accuracy,
> with one model's GSM8K accuracy dropping from 93% to 27%."
— arXiv 2603.23530

> „compliance drops by 2–21% under concurrent task load"
— arXiv 2603.23530 (8000+ prompt, három modellcsalád: o4-mini, DeepSeek-V3.1,
Llama-3.3-70B)

Ez azt mutatja, hogy egy, a fő feladattól idegen instrukció jelenléte KÉTIRÁNYÚAN árthat:
a fő feladat (GSM8K matek) pontossága összeomlik a megkötés jelenlétében, ÉS a megkötés
betartása is romlik konkuráló feladatterhelés alatt. A különbség a mi kérdésünkhöz képest:
itt egy KÖVETENDŐ SZABÁLY (formázási megkötés, amit be KELL tartani) versenyez egy
feladattal — nálunk egy VÁLASZTHATÓ MENÜ (kategória-leírás-lista, amit nem kell
„betartani", csak közülük választani) áll egy másik feladat mellett. Ez utóbbi elvben
kevésbé direktíva-jellegű, tehát enyhébb hatást várnánk — de ezt semmi nem méri
közvetlenül.

A másik közvetlen mérés-csoport azt vizsgálja, hogy sok egyidejű instrukció rontja-e
EGYMÁS betartását ugyanabban a promptban (bár itt nincs külön „másik feladat", minden
elem a modell saját válaszára vonatkozó direktíva). Az „Instruction Stacking Collapse"
(2026.07, nem peer-reviewed preprint, 24 verifikálható instrukciót halmozva 1-től 20-ig,
Claude Sonnet 4.6, GPT-5-mini, Gemini 2.5 Flash):

> „Instruction-following degrades non-linearly: the follow rate falls from ~96% to as
> low as 20%, driven by a structured and reproducible set of pairwise conflicts."
— arXiv 2608.02639

20 instrukciónál: Claude Sonnet 4.6 60,4%, Gemini 2.5 Flash 43,3%, GPT-5-mini 20,1%
követési arány. A „Phase Transitions in Compositional Constraint Satisfaction"
(2026.08, szintén nem peer-reviewed, egyszerzős preprint, 15 modell, k=1-12 megkötés)
matematikai mechanizmust ad ehhez: az egyenkénti megkötés-teljesítés csak lassan romlik,
de mivel a hibák közel függetlenek, az ÖSSZES megkötés EGYSZERRE teljesülésének
valószínűsége kombinatorikusan omlik össze:

> „a model passing individual constraints at ∼41% at k=8 succeeds on all eight just
> 5.7% of the time."
— arXiv 2608.12426

> „Performance becomes unreliable beyond 5-6 simultaneous constraints, with the
> strongest model dropping below 50% success at seven constraints."
— arXiv 2608.12426

### Analógia (nem közvetlen mérés a mi kérdésünkre)

Egy nagy, egymást megerősítő irodalom mutatja, hogy egy DOKUMENTUM/KONTEXTUS hossza,
pozíciója vagy irreleváns tartalma rontja a rá épülő feladatot — de ezek mind
visszakeresésre/kontextus-feldolgozásra vonatkoznak, nem kifejezetten „választható
kategória-menü + saját feladat" elrendezésre:

- **Lost in the Middle** (Liu et al., TACL 2024): a GPT-3.5-Turbo többdokumentumos QA
  teljesítménye a lista közepén elhelyezett releváns dokumentumnál akár **56,1%-os
  „vak" alapszint alá** esik — rosszabbul teljesít, mintha semmilyen dokumentumot nem
  kapott volna. U-alakú pozíció-görbe: legjobb elején/végén, legrosszabb középen.
- **Context Rot** (Chroma Research, T2): a módszertan szándékosan VÁLTOZATLANUL tartotta
  a feladat nehézségét, és csak a bemeneti hosszt variálta — „model performance varies
  significantly as input length changes, even on simple tasks." Még egy triviális,
  szóismétlési feladaton is romlott a teljesítmény pusztán a hossz miatt minden
  tesztelt (18) modellnél.
- **NoLiMa** (ICML 2025): kifejezetten úgy tervezve, hogy KIZÁRJA a szó szerinti
  egyezést — a GPT-4o pontossága 99,3%-ról **69,7%-ra** esik már 32K tokennél (nem
  128K-nál!), és „11 models drop below 50% of their strong short-length baselines" 32K-nál;
  disztraktor jelenlétében „GPT-4o now demonstrates an effective length of just 1K."
- **Same Task, More Tokens** (Levy et al., ACL 2024): öt modell átlagos pontossága
  0,92-ről 0,68-ra esik, ahogy a bemenetet kb. 3000 tokenre „kitömik" irreleváns
  szöveggel, MAGA a feladat nehézsége nélkül változna — és a romlás már **500-3000
  tokennél**, nem csak a „hosszú kontextus" tartományban elkezdődik. Ez a legfontosabb
  méret-nagyságrendi közvetett bizonyíték: néhány ezer token töltelék már önmagában
  mérhető pontosságromlást okozhat.
- **Chen et al.** (COLM 2024): a hibaarány szemantikailag hasonló, de irreleváns
  disztraktor jelenlétében kb. **4x-esre** nő (5,5%→22,5%, GPT-3.5 Turbo, POPQA) — minél
  hasonlóbb a disztraktor a valódi tartalomhoz, annál rosszabb.
- **RULER** (NVIDIA): a hirdetett kontextushossz és az „effektív" (még jól teljesítő)
  kontextushossz gyakran nagyon eltér — pl. GPT-4-nél 128K hirdetett vs. 64K effektív.

Anthropic saját, hivatalos mérnöki iránymutatása (nem mérés, hanem tervezési elv) explicit
módon nevesíti a túlzsúfolt eszközkészletet mint gyakori hibaforrást:

> „One of the most common failure modes we see is bloated tool sets that cover too much
> functionality or lead to ambiguous decision points about which tool to use."
— https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

> „Find the smallest set of high-signal tokens that maximize the likelihood of your
> desired outcome."
— ugyanaz a forrás

Egy egyetlen valós-világ anekdota (T3, GitHub issue, nem kontrollált tanulmány) szerint a
`kimi-k2.5` modell alapértelmezett (hosszabb, több megkötést tartalmazó) rendszerpromptja
mellett rosszabbul teljesített kódolási benchmarkokon (58,0±2,4 vs. 54,1±3,8; 67,1±1,0 vs.
60,0±2,4), mint egy finomhangolt, rövidebb prompt mellett — de itt a hossz hatása
összekeveredik a rossz/ellentmondásos instrukciók hatásával, a beszámoló szerint
„overly aggressive brevity constraints" és „internally conflicting instructions" is
szerepet játszottak, tehát nem tisztán a MÉRET okozta a romlást.

**A „sok rövid vs. kevés hosszú, azonos token-budget mellett" kérdésre nincs mért
válasz.** Nem találtunk olyan kontrollált tanulmányt, amely fixen tartaná a teljes
token-mennyiséget, és csak azt variálná, hogy ez sok rövid egységre vagy kevés hosszú
egységre van-e elosztva. A legközelebbi közvetett jelek (az Instruction Stacking Collapse
kompilátor-kísérlete, ami sok külön instrukciót egy koherens blokká von össze) azt
mutatják, hogy a „kevesebb, összeszervezett egység jobb" hatás **erősen
modellfüggő**: gyenge modelleknél +11 pontot ér, erős modelleknél (pl. Sonnet) gyakorlatilag
nulla (−1,2pp) — tehát ez sem egyetemes szabály, és a kompilátor egyébként is tömörít is,
nem csak átrendez, így nem tiszta azonos-token-számú összehasonlítás.

## 7. Ellentmondások

**A „hány elem/tool fölött kell váltani" küszöb 10x szórást mutat forrásonként, de nem
igazi ellentmondás — inkább különböző mértékegységek.** A 10-100 közötti számok (lásd az
5. pont táblázatát) nem ugyanazt a mennyiséget mérik: van, ami eszközszám/kör, van, ami
eszközszám/namespace, van, ami összes elérhető eszköz, van, ami token-összeg, van, ami
kontextusablak-százalék. Ha mindet „darabszámra" vetítenénk, a tartomány 10-től 100-ig
terjedne — de a kép koherensebb, ha a „10-20"-as számokat *belépési küszöbnek* (mikor
érdemes elkezdeni figyelni), a „30-50"-et pedig *látható degradációs pontnak* (mikor már
biztosan romlik) tekintjük. Az Anthropic Tool Search Tool doksija maga is ezt a két külön
küszöböt adja meg egymás mellett.

**RAG-MCP: két, könnyen összekeverhető mérés.** A RAG-MCP tanulmány „Blank Conditioning"
(minden eszköz egyszerre a promptban) vs. RAG-MCP módszer összevetése (43,13% vs. 13,62%,
NEM egy N-függő görbe) és a stressz-teszt (N=1-11100, ahol a mért mennyiség a retriever
SAJÁT pontossága a helyes eszköz POZÍCIÓJÁNAK függvényében) két különböző dolgot mér.
Másodkézből idéző források néha egybemossák a kettőt, mintha „100 eszköz fölött a
pontosság minden esetben zuhanni kezdene" — ez nem pontos leírása a mért eredménynek.

**„Anthropic's independent implementation achieved 98.7% reduction" — nem igazolható
állítás.** Egy független mérnöki blog (blog.synapticlabs.ai, T3) ezt az adatot
Anthropicnak tulajdonítja, de a legmagasabb hivatalos Anthropic-forrásban közölt szám
85%-os csökkenés (77K→8,7K token). Ez az állítás sehol nem található meg elsődleges
Anthropic-forrásban — lehet túlzás vagy félreidézés, nem használtuk fel tényként.

**„Koherens szöveg rosszabb, mint kevert" (Chroma) vs. az általános „szervezett prompt
jobb" tervezési tanács (Anthropic) — valódi feszültség.** A Chroma Context Rot riport azt
találta:

> „models perform worse when the haystack preserves a logical flow of ideas. Shuffling
> the haystack and removing local coherence consistently improves performance."
— https://www.trychroma.com/research/context-rot

Ezzel szemben Anthropic saját hivatalos irányelve a jól szervezett, tömör kontextust
ajánlja általános elvként. A feloldás: a Chroma-megfigyelés egy szűk, mesterséges
needle-in-haystack elrendezésre vonatkozik, míg az Anthropic-ajánlás a tartalom
MINŐSÉGÉRE (ne legyen felesleges zaj), nem a mondatok sorrendjére vonatkozik — de a két
állítás felszínesen ellentétesnek hat, és nincs egyértelmű, konszenzusos válasz arra, hogy
egy kategória-lista „logikus" csoportokba rendezve vagy semlegesen listázva jobb-e.

**RULER (optimistább) vs. NoLiMa (pesszimistább) — módszertan-függő becslés, valódi,
dokumentált feszültség.** Ugyanarra a kérdésre („mennyire tartja meg a modell a
teljesítményét hosszú kontextusban?") a két benchmark gyökeresen eltérő képet ad: RULER
szerint a GPT-4 degradációja „csak" 15,4 pont 4K-ról 128K-ra (96,6%→81,2%), NoLiMa szerint
a GPT-4o már 32K-nál (nem 128K-nál) 99,3%-ról 69,7%-ra esik. A különbség oka azonosítható:
a NoLiMa direkt válaszul íródott arra, hogy a RULER-szerű benchmarkok túl optimisták,
mert szó szerinti lexikai kapaszkodót hagynak a modellnek. Egy kategória-választási
feladat (ahol a bejegyzés szövege és a kategória-leírás között ritkán van szó szerinti
átfedés) methodológiailag közelebb áll a NoLiMa-forgatókönyvhöz.

**Az instrukció-kompilátor haszna csak gyenge modelleknél számít.** A sok külön
instrukció egyetlen koherens blokká vonása gyenge modelleknél +11 pontot ér, erős
modelleknél (pl. Sonnet) gyakorlatilag semmit (−1,2pp) — vagyis a „kevesebb, jól
szervezett egység jobb" elv NEM egyetemes igazság, hanem modellképesség-függő.

## 8. Hiányok

*Ezt a szakaszt szándékosan nem szépítjük — a szakirodalom hiányosságait az eredeti
kutatási jegyzetek (`sq04/gaps.md`, `sq05/gaps.md`) alapján, változtatás nélkül közöljük.
SQ-01, SQ-02 és SQ-03 esetében nem készült külön, dedikált hiány-elemzés fájl — az alábbi
lista elsősorban SQ-04 és SQ-05 dokumentált réseit tartalmazza.*

1. **Nincs olyan forrás, amely explicit módon a „darabszám × leírás-hossz szorzatát"
   adná meg küszöbként.** Minden hivatalos küszöb az EREDMÉNY-token-összegre vonatkozik
   (Anthropic: 10k token; MCP: kontextusablak 1-5%-a), ami matematikailag ekvivalens a
   szorzattal, de a forrásokban nincs kimondva mint önálló, névvel illetett tervezési
   elv. Célzott keresés ("tool count times description length", "N × average description
   tokens threshold") sem hozott találatot.

2. **Nincs kontrollált, publikált kísérlet KIFEJEZETTEN „kategória-választó prompt"
   (osztályozási címke-lista) méretére.** A talált mért adatok csaknem mind
   eszköz-/API-/skill-VÁLASZTÁSRA vonatkoznak (function calling, MCP tool retrieval), nem
   „melyik kategóriába tartozik ez a szöveg" jellegű zéró-lövéses klasszifikációra sok,
   hosszú leírású kategóriával.

3. **A „98.7%-os csökkenés" (Anthropicnak tulajdonított) állítás nem igazolható** —
   sem megerősítő, sem cáfoló elsődleges forrást nem sikerült találni.

4. **Nincs friss, nagymintás, független (nem gyártói) benchmark a Tool Search Tool /
   progresszív feltárás hatásáról.** Az összes számszerű teljesítményadat (77K→8,7K token,
   79,5%→88,1% pontosság, 49%→74% Opus 4-nél) kizárólag Anthropic saját közlése a saját
   termékéről; független reprodukciót vagy auditot nem találtunk.

5. **Egyetlen forrás sem ad konkrét ajánlást kifejezetten Markdown-alapú, kézzel írt
   kategória-prompt rendszerekre.** Minden talált küszöbszám API/tool/skill-JSON-sémákra
   vonatkozik, nem szabad szöveges „mikor tartozik ide egy bejegyzés" jellegű promptokra.

6. **A legfontosabb hiány: nincs olyan tanulmány, amely pontosan az SQ-05 konfigurációt
   tesztelte volna** — egy VÁLASZTHATÓ (nem betartandó) kategória/leírás-menü + egy attól
   FÜGGETLEN, saját feladat egyazon promptban, mérve, hogy a menü méretének növelése
   rontja-e a SAJÁT feladat minőségét. Többszöri, különböző szögekből futtatott keresés
   sem hozott találatot, ami az „evidence of absence" irányába billen, de teljes
   bizonyossággal nem zárható ki, hogy egy nagyon friss vagy niche publikáció elkerülte a
   figyelmet.

7. **Nincs „azonos token-budget, sok rövid vs. kevés hosszú" kísérlet.** Egyetlen
   forrás sem tartja fixen a teljes token-mennyiséget úgy, hogy csak azt variálja, sok
   rövid egységre vagy kevés hosszú egységre van-e elosztva.

8. **A Chroma Context Rot riport disztraktor-szekciójának pontos százalékai csak
   grafikonon érhetők el**, szövegesen nem — a szöveg-alapú lekérés nem tudta kiolvasni
   ezeket a számokat, így ezt a konkrét számsort nem lehetett idézni, csak a kvalitatív
   irányt.

9. **A LongIns tanulmány részletes táblázatai nem kerültek elő** — csak két minőségi
   mondat volt kinyerhető az absztraktból; ez inkább erőforrás-korlát, mint „nincs adat"
   jellegű rés.

10. **Módszertani korlát: minden idézet egy kisebb, gyors segédmodell által készített
    lekérés eredménye**, nem a nyers oldal-szöveg. A magas tétű, döntő idézeteket (pl. az
    Anthropic Tool Search Tool küszöbök, a „20-50 skills" mondat, a NoLiMa GPT-4o
    32K-számai, a RULER GPT-4 táblázat) két, eltérő promptú, független lekéréssel
    kereszt-ellenőrizték, és mindkétszer szó szerint egyezett. Számos alacsonyabb tétű,
    kiegészítő idézetnél (blogok, egyes preprint-számok) ez a kereszt-ellenőrzés nem
    történt meg — ezeket alacsonyabb bizonyossággal kell kezelni.

## 9. Minden meglátogatott link

A feladat szerint ez a lista az `sq04/links.md`, `sq05/links.md` és `05-links.jsonl`
uniója. Egy fontos pontosítás: a `05-links.jsonl` fájlban szereplő mind a 95 bejegyzés
`status: not_opened` jelöléssel szerepel — ezek olyan kimenő linkek, amelyeket a
ténylegesen meglátogatott oldalakon TALÁLTAK, de magukat NEM nyitották meg. Emellett az
SQ-01, SQ-02 és SQ-03 al-kérdések saját, ténylegesen lekért és lementett (a `clean/`
mappákban archivált) forrásai egyik uniós fájlban sem szerepelnek, mert azok nem
„talált linkek", hanem maguk a kutatás elsődleges bemenetei. A teljesség és az őszinteség
együttes megőrzése érdekében az alábbi felosztást alkalmazzuk: **(A)** ténylegesen
meglátogatott/feldolgozott források (SQ-01/02/03 saját forrásai + az SQ-04 és SQ-05
kutatás során ténylegesen megnyitott linkek — ez felel meg a szigorú „meglátogatott"
értelemnek), majd **(B)** talált, de meg NEM nyitott további linkek (az SQ-04/SQ-05 saját
„nem nyitva" jegyzései + a teljes `05-links.jsonl` állomány, deduplikálva a fentiekkel).

Tier-kulcs: **T1** = hivatalos dokumentáció/spec/peer-reviewed vagy arXiv paper · **T2** =
jó minőségű, független másodlagos forrás VAGY gyártó saját termékére vonatkozó
teljesítmény-állítás (ez a szabály szerint sosem T1, még hivatalos domainen sem) · **T3**
= fórum, vélemény, marketing, ellenőrizetlen blog (hivatalos domainen — pl. GitHub issue —
is T3).

### 9/A — Ténylegesen meglátogatott, feldolgozott források

**SQ-01 (tokenköltség és karakterlimitek) forrásai**

| URL | Tier | Mire volt jó |
|---|---|---|
| https://www.anthropic.com/engineering/advanced-tool-use | T1 (mechanizmus) / T2 (saját %-os számok) | Az 55K/72K/134K tokenes MCP-eszközterhelési példák, a Tool Search Tool 85%-os token-csökkenése és a 3-5 tool ajánlás forrása |
| https://github.com/modelcontextprotocol/modelcontextprotocol/issues/2808 | T3 | Egy felhasználó saját, nem hivatalos állítása MCP tool-token overheadről (degradált lekérés) |
| https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview | T1 | Skill leírás 1024 karakteres kemény limitje, 3-szintű progresszív feltárás token-táblázata (~100 token/skill) |
| https://github.com/anthropics/skills/issues/1613 | T3 | Valós eset: Anthropic saját claude-api skillje túllépte a saját 1024-es limitjét (1068 karakter) |
| https://arxiv.org/abs/2510.21909 | T1 (peer-reviewed, NeurIPS 2025) | Cross-lingual tokenizer inequity: a token-prémium nem a tanítóadat-hasonlóságból ered |
| https://community.openai.com/t/tool-calling-api-upgrade-1024-char-limit-is-limiting/951951 | T3 | OpenAI 1024 karakteres kemény validációs hiba dokumentálása egy hibaüzenettel |
| https://webdevcenter.hu/chatgpt-magyarul-dragabb/ | T2 | Magyar nyelvű token-prémium: kb. 2x angolhoz képest, CJK/hindi 5-10x, „Ű" betű 2 tokenre bomlik |
| https://modelcontextprotocol.io/specification/2025-11-25/server/tools | T1 | MCP spec: tool NÉV SHOULD 1-128 karakter, tool LEÍRÁS szabad szöveg, nincs numerikus limit |
| https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | T1 | Kontextus mint véges erőforrás elve, „bloated tool sets" mint hibaforrás, sub-agent összegzés 1000-2000 tokenes ökölszabálya |
| https://platform.claude.com/docs/en/build-with-claude/token-counting | T1 | count_tokens worked example (14 vs. 403 token), Claude 4.7+ tokenizer ~30%-kal több tokent termel |

**SQ-02 (darabszám-degradáció) forrásai**

| URL | Tier | Mire volt jó |
|---|---|---|
| https://arxiv.org/html/2605.24660v1 | T1 | „How Many Tools Should an LLM Agent See" — BFCL/ToolBench/MetaTool fedettségi görbék, adaptív vs. fix K |
| https://arxiv.org/html/2502.08436v2 | T1 | Label-space reduction: optimális k=2-5, modellfüggő haszon (kisebb modell többet nyer) |
| https://help.getzep.com/customizing-graph-structure | T1 | Zep hivatalos tervezési elve: átfedő leírás = következetlen osztályozás, névátfedés nem baj |
| https://arxiv.org/html/2504.00914v1 | T1 | Konfúzió-teszt: ~3 hasonló csali-eszköz hatása kilenc modellen, hibamódok elemzése |
| https://arxiv.org/abs/2505.10570 | T1 | LongFuncEval: 7-85%-os szórás a teljesítménycsökkenésben modellenként |
| https://arxiv.org/abs/2505.03275 | T1 | RAG-MCP absztrakt: 13,62% vs. 43,13% pontosság retrieval nélkül/-lel |
| https://arxiv.org/html/2310.03128v4 | T1 | MetaTool: CSR-görbe top5/top10/top15, meredek esés majd ellaposodás |
| https://aclanthology.org/2023.genbench-1.14.pdf | T1 (workshop, peer-reviewed) | Retrieval-augmented few-shot: magas pontosság 150 osztálynál is (Llama-2-70B) |
| https://arxiv.org/html/2404.02060v2 | T1 | LongICLBench: valódi cliff 174 címkénél, Banking77 kis/nagy modell szakadék |

**SQ-03 (leírás-hossz degradáció) forrásai**

| URL | Tier | Mire volt jó |
|---|---|---|
| https://arxiv.org/abs/2603.25422 | T1 | „Navigating the Prompt Space": minimális kontextus-bővítés a leghatékonyabb, néha romlik a pontosság |
| https://arxiv.org/abs/2310.20410 | T1 | FollowBench: HSR 84,7%→61,9% 1→5 megkötésnél (L1-L5) |
| https://arxiv.org/abs/2407.03978 | T1 | ComplexBench — csak absztrakt szintű adat volt kinyerhető |
| https://www.anthropic.com/engineering/writing-tools-for-agents | T1 (elvek) / T2 (SOTA-állítás) | Tool-leírás finomítás → SWE-bench SOTA; tömör vs. részletes válasz (72 vs. 206 token) |
| https://arxiv.org/html/2608.08254v1 | T1 | Séma-elhelyezés hatása: 11-13pp különbség, ellentmondás esetén 45,5pp összeomlás |
| https://arxiv.org/abs/2404.11018 | T1 | Many-shot ICL — háttér-forrás, nem közvetlenül a rövid kategória-prompt kérdésre |
| https://arxiv.org/pdf/2409.00105 | T1 | Negation blindness — gyenge illeszkedés (kép-generálásra vonatkozik), háttér-bizonyíték |
| https://eval.16x.engineer/blog/the-pink-elephant-negative-instructions-llms-effectiveness-analysis | T2 | Pozitív vs. negatív megfogalmazás elve, önmaga jelzi: anekdotikus |
| https://arxiv.org/html/2602.20426v1 | T1 | Tool-leírás átírás: a puszta bővítés nem mindig javít, tool-interfészek ember-orientáltak |

**SQ-04 (valós rendszerek saját küszöbei) — az `sq04/links.md` alapján**

| URL | Tier | Mire volt jó |
|---|---|---|
| https://www.anthropic.com/engineering/advanced-tool-use | T1 (mechanizmus) / T2 (%-os számok) | Tool Search Tool, Programmatic Tool Calling, Tool Use Examples hivatalos leírása |
| https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview | T1 | Progresszív feltárás 3 szintje, pontos karakterlimitek |
| https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | T1 | Progresszív feltárás filozófiája, „manual/table of contents" analógia |
| https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | T1 | SKILL.md max. 500 sor ajánlás; „100+ available Skills" megfogalmazás |
| https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool | T1 (küszöb) / T2 (%-os hatás) | A pontos „mikor használj Tool Search-öt" küszöblista (10+ tool, 10k token, 30-50 tool degradáció) |
| https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf | T1 | „20-50 skills enabled simultaneously" küszöb |
| https://modelcontextprotocol.io/docs/2026-07-28/develop/clients/client-best-practices | T1 | MCP hivatalos kliens-ajánlás: 1-5%-os kontextusablak-küszöb, catalog/inspect/execute minta |
| https://developers.openai.com/api/docs/guides/tools-tool-search | T1 | „fewer than 10 functions" namespace-enkénti ajánlás |
| https://developers.openai.com/api/docs/guides/function-calling | T1 | „fewer than 20 functions… soft suggestion" |
| https://arxiv.org/abs/2505.03275 | T1 | RAG-MCP absztrakt |
| https://arxiv.org/pdf/2505.03275 | T1 | RAG-MCP teljes szöveg: N-tartomány, pontosság, token-számok |
| https://arxiv.org/html/2505.03275v1 | T1 | RAG-MCP HTML-verzió, degradációs mondatok |
| https://arxiv.org/html/2503.01763 | T1 | ToolRet (ACL Findings 2025): 43k eszközös korpusz, retrieval-pontosság gyengeségei |
| https://arxiv.org/pdf/2305.15334 | T1 | Gorilla paper — nem tartalmazott releváns skálázási görbét |
| https://huggingface.co/papers/2307.16789 | T1 | ToolLLM: 16 464 API, 49 kategória, retriever-komponens |
| https://achan2013.medium.com/how-many-tools-functions-can-an-ai-agent-has-21e0a82b7847 | T2 | Vendor-limitek összegyűjtése (OpenAI 128 hard limit, BFCL átlag 3 fv/teszt) |
| https://www.askaibrain.com/en/posts/context-engineering-why-600-skills-make-agents-less-effective/ | T3 | „600 skills" elrettentő példa — marketing-blog, forrás nélkül |
| https://github.com/modelcontextprotocol/modelcontextprotocol/discussions/2036 | T3 | Gyakorlói tapasztalat: 60-80 tool jól működik Claude-dal, 100 fölött szét kell bontani |
| https://blog.synapticlabs.ai/bounded-context-packs-meta-tool-pattern | T3 | Meta-tool minta, a nem igazolható „98,7%-os csökkenés" állítás forrása |
| https://www.mindstudio.ai/blog/context-rot-claude-code-skills-bloated-files | T3 | „2000-3000 token alatt tartsd" ajánlás — vendor content-marketing |
| https://boliv.substack.com/p/lazy-skills-a-token-efficient-approach | T3 | Kulcsszó-alapú relevancia-detektálás 50 skill alatt — nem verifikálható anekdota |
| https://cobusgreyling.substack.com/p/bigtool-from-langchain | T3 | LangGraph BigTool — szerző maga jelzi, nincs skálázási benchmarkja |
| https://aws.amazon.com/blogs/machine-learning/govern-ai-agent-tool-access-with-amazon-bedrock-agentcore-gateway/ | T3 | AWS AgentCore Gateway — governance-fókusz, nem releváns adat |

**SQ-05 (más feladat romlása) — az `sq05/links.md` alapján**

| URL | Tier | Mire volt jó |
|---|---|---|
| https://arxiv.org/abs/2307.03172 | T1 (peer-reviewed, TACL 2024) | Lost in the Middle — U-alakú pozíció-érzékenység |
| https://arxiv.org/abs/2502.05167 | T1 (peer-reviewed, ICML 2025) | NoLiMa — drasztikus összeomlás lexikai kapaszkodó nélkül |
| https://arxiv.org/abs/2302.00093 | T1 (peer-reviewed, ICML 2023) | Shi et al. — irreleváns mondatok matek feladatokban (GSM-IC) |
| https://arxiv.org/abs/2404.06654 | T1 | RULER — effektív vs. hirdetett kontextushossz |
| https://arxiv.org/abs/2608.12426 | T1 (preprint, nem peer-reviewed) | Phase Transitions — konstraint-halmozás kombinatorikus összeomlása |
| https://arxiv.org/abs/2608.02639 | T1 (preprint, nem peer-reviewed) | Instruction Stacking Collapse — 96%→20% követési arány |
| https://arxiv.org/abs/2406.17588 | T1 | LongIns — csak absztrakt-szintű idézet volt kinyerhető |
| https://arxiv.org/html/2606.22470 | T1 (preprint) | PRIME — csak 2 ütköző instrukciót vizsgál, nem a mi kérdésünket |
| https://arxiv.org/abs/2505.06120 | T1 | LLMs Get Lost in Multi-Turn Conversation — analógia, 39%-os átlagos esés |
| https://arxiv.org/abs/2402.14848 | T1 (peer-reviewed, ACL 2024) | Same Task, More Tokens — 0,92→0,68 azonos feladat mellett |
| https://arxiv.org/abs/2404.03302 | T1 (peer-reviewed, COLM 2024) | Chen et al. — kb. 4x-es hibaarány-növekedés hasonló disztraktornál |
| https://arxiv.org/abs/2607.25398 | T1 (preprint) | HANDBOOK.md — nagy szabályzat-dokumentum betartási arány (36,2% legjobb modellnél) |
| https://arxiv.org/html/2412.14454v1 | T1 (preprint) | „Are Longer Prompts Always Better?" — item-szám tengely, nem leírás-hossz |
| https://arxiv.org/html/2602.14878v1 | T1 (preprint) | „MCP Tool Descriptions Are Smelly!" — leírás-bővítés trade-off |
| https://arxiv.org/html/2603.23530v1 | T1 (preprint, nem peer-reviewed) | Prospective Memory Failures — GSM8K 93%→27%, legközvetlenebb SQ-05 találat |
| https://arxiv.org/abs/2601.11564 | T1 (preprint) | Context Discipline — inkább infrastruktúra/KV-cache fókuszú |
| https://www.trychroma.com/research/context-rot | T2 | Context Rot riport — 18 modell, feladat-nehézség fixen tartva |
| https://github.com/anomalyco/opencode/issues/20258 | T3 | kimi-k2.5 alapértelmezett prompt vs. finomhangolt prompt anekdota |
| https://mlops.community/blog/the-impact-of-prompt-bloat-on-llm-output-quality | T3 | Vélemény-blog, más kutatásokat aggregál, nincs saját mérés |
| https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | T1 | Hivatalos tervezési elv: „bloated tool sets" mint hibaforrás |

Összesen **67 egyedi URL** tartozik a ténylegesen meglátogatott/feldolgozott kategóriába
(a fenti öt tábla URL-jei között van néhány átfedés — pl. az `advanced-tool-use` és az
`effective-context-engineering` oldalt több al-kérdés is önállóan felhasználta —, ezeket
egyszer számoljuk).

### 9/B — Talált, de meg NEM nyitott további linkek

Az alábbiak olyan URL-ek, amelyeket a fentebb felsorolt, ténylegesen meglátogatott
oldalakon TALÁLTUNK (kimenő hivatkozásként), de saját magukat nem nyitottuk meg és nem
dolgoztuk fel — tehát nem hordoznak önálló, ellenőrzött állítást ebben a kutatásban. A
teljesség kedvéért, forrásonként csoportosítva soroljuk fel őket, a „mit sejtet" oszlop a
horgonyszöveg vagy a linkkörnyezet alapján.

**Az SQ-04 saját „nem nyitott" jegyzései:**

| URL/domain | Megjegyzés |
|---|---|
| stacklok.com (MCP Optimizer blog, pontos URL nélkül) | Keresési találatban látott, nem fetchelve |
| marktechpost.com (Hermes Agent cikk, pontos URL nélkül) | Másodkézből ugyanazok a számok, mint amit T1/T2-ből már megszereztünk |
| ascii.co.uk (cikk, pontos URL nélkül) | Keresési találatban látott, nem fetchelve |

**Az SQ-05 saját „nem nyitott" jegyzései:**

| URL | Megjegyzés |
|---|---|
| https://arxiv.org/html/2403.04797v1 | „Found in the Middle" — pozíció-korrekciós módszer, nem fetchelve részletesen |
| https://github.com/nelson-liu/lost-in-the-middle | Lost in the Middle hivatalos kód-repója, csak azonosításra |
| https://arxiv.org/abs/2411.07037 | LIFBench — csak keresési találatként azonosítva |
| https://arxiv.org/abs/2607.27912 | IFHierBench — csak keresési találatként azonosítva |
| https://scale.com/blog/long-context-instruction-following | Scale AI vendor blog — csak keresési találatként azonosítva |

**A `05-links.jsonl`-ből (a fenti, ténylegesen meglátogatott URL-ekkel átfedő bejegyzéseket
kihagyva; 87 egyedi URL, forrás-oldal szerint csoportosítva):**

*SQ-01 kutatás közben talált, meg nem nyitott linkek (33):*
https://www.anthropic.com/research/building-effective-agents ("build effective agents"),
https://www.anthropic.com/engineering/code-execution-with-mcp ("code execution with
MCP"), https://www.claude.com/claude-for-excel ("Claude for Excel"),
https://www.anthropic.com/ ("Anthropic home"), https://www.anthropic.com/engineering
("Engineering at Anthropic"), https://arxiv.org/abs/2311.12983 ("GIA benchmarks"),
https://github.com/anthropics/claude-cookbooks/blob/main/tool_use/tool_search_with_embeddings.ipynb
("Cookbook for Tool Search Tool"),
https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling
("Documentation for Programmatic Tool Calling"),
https://github.com/anthropics/claude-cookbooks/blob/main/tool_use/programmatic_tool_calling_ptc.ipynb
("Cookbook for Programmatic Tool Calling"),
https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use#providing-tool-use-examples
("Documentation for Tool Use Examples"), https://github.com/luw2007 (szerzői profil),
https://github.com/anthropics/skills ("skills repository"),
https://agentskills.io/specification#description-field,
https://github.com/anthropics/skills/pull/1649, https://github.com/anthropics/skills/pull/1616,
https://arxiv.org/pdf/2510.21909, https://arxiv.org/html/2510.21909v1,
https://community.openai.com/t/was-the-character-limit-for-schema-descriptions-upgraded/1225975,
https://community.openai.com/t/character-limit-for-tools-descriptions/1153112,
https://aihirfolyam.hu/2024/05/gpt-4o-magyar-dragabb-mint-angol/ (kapcsolódó magyar
tokenköltség-cikk), https://platform.openai.com/tokenizer ("OpenAI tokenizáló eszköz"),
https://modelcontextprotocol.io/llms.txt,
https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview ("Prompt
engineering overview"), https://modelcontextprotocol.io/docs/getting-started/intro
("Model Context Protocol"), https://www.anthropic.com/engineering/multi-agent-research-system
("Multi-agent research system"), https://www.anthropic.com/news/context-management
("Context management feature"), https://platform.claude.com/docs/en/api/messages-count-tokens
("token counting endpoint"), https://platform.claude.com/docs/en/build-with-claude/context-windows
("Context windows"), https://platform.claude.com/docs/en/build-with-claude/prompt-caching
("Prompt caching"), https://arxiv.org/html/2601.13328v1, https://arxiv.org/html/2604.14210v1,
https://medium.com/@harangpeter/how-efficient-are-llms-tokenizers-on-hungarian-text-d1f78f9565a7
(kapcsolódó magyar tokenizálási cikk), https://github.com/modelcontextprotocol/modelcontextprotocol
(az MCP repó gyökere).

*SQ-02 kutatás közben talált, meg nem nyitott linkek (11):*
https://www.kaggle.com/datasets/danofer/dbpedia-classes ("DBpedia on Kaggle" — adathalmaz
hivatkozás), https://datasf.org/opendata/ ("Crime Dataset on DataSF"),
https://deepinfra.com ("DeepInfra API" — infrastruktúra-hivatkozás),
https://github.com/getzep/zep/blob/main/pkg/extractors/ontology.yaml (Zep saját
ontológia-fájlja), https://www.zep.ai/pricing ("pricing page"),
https://huggingface.co/datasets/ibm-research/BFCL-FC-robustness (adathalmaz-hivatkozás),
https://doi.org/10.48550/arXiv.2505.10570 (DOI-hivatkozás a LongFuncEval paperre),
https://doi.org/10.48550/arXiv.2505.03275 (DOI-hivatkozás a RAG-MCP paperre),
https://arxiv.org/abs/2304.08244, https://arxiv.org/html/2607.11564,
https://arxiv.org/html/2601.07206v1.

*SQ-03 kutatás közben talált, meg nem nyitott linkek (43 — ebből jó néhány egy arXiv-cikk
bibliográfiai/jogi láblécének DOI- és intézményi hivatkozása, nem tartalmi forrás):*
https://arxiv.org/, https://info.arxiv.org/about, https://info.arxiv.org/about/accessible_HTML.html,
https://arxiv.org/abs/2603.25422v1, https://arxiv.org/pdf/2603.25422v1,
https://info.arxiv.org/help/license/index.html#licenses-available,
https://www.senate.gov/legislative/common/briefing/leg_laws_acts.htm (a „Navigating the
Prompt Space" cikk egyik lábjegyzet-hivatkozása), https://doi.org/10.48550/arXiv.2507.19457,
https://doi.org/10.1007/s44382-026-00021-8, https://doi.org/10.1561/113.00000128,
https://doi.org/10.48550/arXiv.2005.14165, https://doi.org/10.1017/pan.2025.10017,
https://doi.org/10.1093/pnasnexus/pgaf069, https://doi.org/10.48550/arXiv.2507.21831
(mind a fenti DOI-k a „Navigating the Prompt Space" cikk saját bibliográfiájából
kimenő, tartalmilag nem ellenőrzött hivatkozások), https://www.anthropic.com/news/web-search
("web search tool"), https://www.anthropic.com/engineering/swe-bench-sonnet ("SWE-bench
Verified"), https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implement-tool-use#best-practices-for-tool-definitions
("Developer Guide"), https://modelcontextprotocol.io/ ("MCP servers"),
https://www.anthropic.com/claude-code ("Claude Code"), https://modelcontextprotocol.io/docs/sdk
("MCP SDK"), https://docs.anthropic.com/llms.txt, https://modelcontextprotocol.io/docs/develop/connect-local-servers
("local MCP server"), https://www.anthropic.com/engineering/desktop-extensions ("Desktop
extension"), https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview
("Anthropic API"), https://platform.claude.com/cookbook/tool-evaluation-tool-evaluation
("tool evaluation cookbook"), https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking#interleaved-thinking
("interleaved thinking"), https://www.anthropic.com/research/tracing-thoughts-language-model
("say what they mean"), https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implement-tool-use#tool-use-system-prompt
("system prompt"), https://modelcontextprotocol.io/specification/2025-06-18/server/tools
("tool annotations"),
https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools/blob/main/Cursor%20Prompts/Agent%20Prompt%20v1.2.txt
("leaked system prompt for Cursor"), https://docs.anthropic.com/en/release-notes/system-prompts
("Anthropic's system prompt"), https://www.reddit.com/r/ClaudeAI/comments/1lrf2az/tired_of_claudes_convolution_for_everything/,
https://www.reddit.com/r/ClaudeAI/comments/1mes0jj/what_are_your_favourite_constraints_to_use_with/,
https://www.reddit.com/r/GeminiAI/comments/1l88kwa/negative_instructions_gemini_25_flash_and_25_pro/
(mind Reddit-anekdoták negatív instrukciókról, a Pink Elephant cikk saját forrásai),
https://en.wikipedia.org/wiki/Ironic_process_theory,
https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices,
https://www.reddit.com/r/ClaudeAI/comments/1lrf2az/comment/n1aitrh/, https://eval.16x.engineer/
("16x Eval" — a blog saját főoldala), https://rapidapi.com/, https://themoviedb.org,
https://spotify.com (mind példa-API-k egy tool-leírás-átíró cikkben),
https://glama.ai/blog/2026-04-03-tool-description-quality-score-tdqs,
https://arxiv.org/html/2407.03978v3#S5.

---

### Összegzés a linkekről

- **Ténylegesen meglátogatott, tartalmilag felhasznált források: 67 egyedi URL**
  (SQ-01: 10, SQ-02: 9, SQ-03: 9, SQ-04 saját listája: 23, SQ-05 saját listája: 20 —
  átfedésekkel csökkentve 67-re).
- **Talált, de meg nem nyitott további linkek: 95 egyedi URL** (SQ-04: 3, SQ-05: 5,
  `05-links.jsonl`: 87, miután kivontuk a fentebb már szereplő, ténylegesen meglátogatott
  URL-eket).
- **Összesen 162 egyedi URL** szerepel ebben a szakaszban.

---

*Ez a dokumentum kizárólag a meglévő kutatási anyag összefoglalása. Nem tartalmaz
szintézist, ajánlást vagy következtetést — ezt a vezető (Opus) írja külön.*
