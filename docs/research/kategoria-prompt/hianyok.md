# Hiányok — amire nem sikerült választ találni

Egyesítve: `sq04/gaps.md` + `sq05/gaps.md`, kiegészítve az SQ-01/02/03 anyagban (`02-sources/_agent/SQ-0X/manifest.jsonl`
és `claims.jsonl` megjegyzés-mezői) jelzett hiányokkal. Minden tételnél jelölve, hogy **„nincs ilyen a
szakirodalomban”** (a kutatás direktben megkereste/ellenőrizte, és a hiány konfirmált) vagy **„létezhet, de nem
találtuk meg”** (a keresés nem talált rá, de nem zárható ki, hogy létezik). Egy harmadik, gyakori eset — amikor a
forrás bizonyítottan létezik és tartalmazza az adatot, csak a lekérő eszköz (WebFetch) nem tudta szó szerint
kinyerni belőle — a „létezhet, de nem találtuk meg” kategóriába van sorolva, de külön jelölve, mert itt nem a
keresés, hanem a KINYERÉS hiúsult meg.

---

## SQ-01 — Mennyibe kerül tokenben egy leírás

### 1. Nincs numerikus token/karakter-limit a tool `description` mezőre a hivatalos MCP specifikációban

A Model Context Protocol hivatalos specifikációja (`modelcontextprotocol.io/specification/2025-11-25/server/tools`)
a tool NÉV mezőjére ad csak SHOULD-szintű, 1-128 karakteres ajánlást; a description mezőt csak szabad szövegként
("Human-readable description of functionality") definiálja, számszerű hossz- vagy token-korlát **sehol** nincs
hozzá rendelve a specifikációban.

**Minősítés: nincs ilyen a szakirodalomban.** A forrást közvetlenül elolvasva (nem csak keresve) konfirmált hiány
— éles kontrasztban az Anthropic Agent Skills (1024 karakter) és az OpenAI function-calling (szintén 1024 karakter)
kemény limitjeivel.

---

## SQ-02 — Darabszám szerinti degradáció

### 2. "How Many Tools Should an LLM Agent See?" (arXiv 2605.24660) — Appendix A / Hivatkozások szakasz nem teljesen szó szerinti

A fetch-eszköz a References/Appendix A szakaszokat rövidítve adta vissza, nem teljes szó szerinti formában. A
cikk fő eredményei (BFCL/MetaTool/ToolBench táblázatok) megvannak, de a függelékben esetlegesen szereplő további
számadatok nem lettek kinyerve.

**Minősítés: létezhet, de nem találtuk meg** (pontosabban: a forrás bizonyítottan létezik, csak a lekérő eszköz
nem hozta vissza szó szerint — technikai kinyerési korlát, nem tartalmi hiány).

### 3. LongFuncEval (arXiv 2505.10570) — a Results szakasz teljes táblázatai nem érhetők el

A teljes HTML-oldal (`arxiv.org/html/2505.10570v1`) lekérését a fetch-eszköz KÉTSZER is megtagadta, szerzői jogi
politikára hivatkozva ("reproducing substantial portions as exact text would constitute reproducing copyrighted
material"), és csak egy 125 karakteres idézetre korlátozott parafrázist adott. A per-modell táblázatok, a pontos
eszközszám-értékek, és hogy a katalógusméretet eszközszámban vagy tokenben mérik-e — mind **nem** érhetők el
megbízhatóan ebből a forrásból; csak az absztrakt (a különálló `/abs/` URL-en) szerezhető meg valódi idézetekkel.
Ez fel is került a `01-search-log/blocked.jsonl`-be.

**Minősítés: létezhet, de nem találtuk meg** (a teljes cikk létezik, a kinyerés hiúsult meg).

### 4. RAG-MCP (arXiv 2505.03275) — a teljes HTML-törzs csak összefoglalva

A teljes cikktörzset a fetch-eszköz két alkalommal is összefoglalta/megtagadta; csak az absztrakt-szintű idézetek
biztosíthatók megbízhatóan innen ehhez a konkrét forrás-bejegyzéshez (bár a `sq04` kör egy másik fetch-kísérlete —
`arxiv.org/pdf/2505.03275` és `arxiv.org/html/2505.03275v1` — sikeresen hozzáfért a teljes szöveghez, ld.
`linkek.md`).

**Minősítés: létezhet, de nem találtuk meg** (ennél a konkrét forrás-bejegyzésnél; máshonnan részben pótolva).

---

## SQ-03 — Leírás-hossz szerinti degradáció

### 5. "Navigating the Prompt Space" (arXiv 2603.25422) — a Figure 2-5 numerikus F1-értékei nem kinyerhetők szövegként

A WebFetch 3/4 alkalommal harmadik személyű összefoglalássá degradálta a cikket; csak azok a mondatok
tekinthetők szó szerintinek, amelyeket a fetch-eszköz saját maga tett idézőjelbe. Az egyes konfigurációk pontos
F1-értékei csak a 2-5. ábrákon élnek, szövegként nem kinyerhetők; csak az aggregált GPT-4o emocionalitás-
detektálási F1-tartomány (0,75-0,90) és a batch-méret-listák voltak számként visszanyerhetők.

**Minősítés: létezhet, de nem találtuk meg** (a számok léteznek a cikk ábráin, csak szöveges kinyeréssel nem
hozzáférhetők).

### 6. ComplexBench (arXiv 2407.03978) — a kompozíció-típusonkénti pontszámok hiányoznak

Csak az absztrakt volt elérhető; a teljes szöveg lekérése két kísérletben is megszakadt az eredménytáblázatok
előtt. A manifest saját megjegyzése szó szerint: "numeric per-composition-type scores are a GAP, not fabricated."

**Minősítés: létezhet, de nem találtuk meg** — a forrás explicit módon saját magát jelöli hiányként, nem
kitalált számmal pótolva.

---

## SQ-04 — Mit írnak elő maguknak a valós rendszerek

### 7. Nincs forrás, amely kifejezetten a "darabszám × leírás-hossz szorzatát" adná meg küszöbként

A vezető felismerése szerint a releváns korlát nem a kategóriaszám, nem is az egyenkénti prompt-hossz, hanem a
kettő szorzata — az az össz-token-mennyiség, ami egyszerre bekerül a hívó agent kontextusába. **Egyetlen forrás
sem fogalmazza meg explicit módon ezt a "szorzat" absztrakciót.** A legközelebb hozzá:
- Anthropic Tool Search Tool doksi: "Your tool definitions consume more than 10k tokens" — összeg-alapú küszöb.
- MCP hivatalos ajánlás: "a threshold as a percentage of the context window… 1%-5%" — szintén összeg-alapú.

Kipróbált keresések: "tool count times description length", "token budget product categories descriptions",
"N × average description tokens threshold" — egyikre sem volt találat.

**Minősítés: nincs ilyen a szakirodalomban.** A valós rendszerek mindig az EREDMÉNY-token-összeget adják meg
küszöbként, sosem a két tényező szorzataként vezetik le — ez matematikailag ugyanaz, de a forrásokban nincs
kimondva.

### 8. Nincs kontrollált, publikált kísérlet kifejezetten "kategória-választó prompt" (osztályozási címke-lista) méretére

A talált mért adatok csaknem mind eszköz-/API-/skill-VÁLASZTÁSRA vonatkoznak (function calling, MCP tool
retrieval), nem "melyik kategóriába tartozik ez a szöveg" jellegű zéró-lövéses klasszifikációra sok, hosszú
leírású kategóriával.

**Minősítés: nincs ilyen a szakirodalomban** — kifejezetten erre a konfigurációra; analóg irodalom (eszköz-
választás) bőven van, de az nem azonos a mi kategória-választó use case-ünkkel.

### 9. A "98.7%-os csökkenés" (synapticlabs blog, Anthropic-nak tulajdonítva) nem igazolható

A blog.synapticlabs.ai cikk azt állítja, hogy "Anthropic's independent implementation achieved 98.7% reduction
in tool overhead." Az Anthropic hivatalos oldalain (advanced-tool-use, tool-search-tool doksi,
equipping-agents… blog) ez a szám **sehol nem szerepel** — ott a legmagasabb közölt szám 85%.

**Minősítés: létezhet, de nem találtuk meg** — nem zárható ki, hogy a blog egy nem publikus vagy általunk meg
nem talált forrásra hivatkozik; de az is lehet, hogy egyszerűen téves/túlbecsült állítás.

### 10. Nincs friss, nagymintás, független (nem gyártói) benchmark a Tool Search Tool / progresszív feltárás hatásáról

Az összes számszerű teljesítmény-adat (77K→8.7K token, 79.5%→88.1% pontosság, 49%→74% Opus 4-nél,
43 588→27 297 token programozott tool-hívásnál) kizárólag Anthropic saját közlése a saját termékéről. Kipróbált
keresések: "Tool Search Tool independent benchmark", "Anthropic tool search reproduction study", "Opus 4.5 tool
selection accuracy study" — nincs találat független mérésre.

**Minősítés: létezhet, de nem találtuk meg.**

### 11. Nincs konkrét ajánlás kifejezetten Markdown-alapú, kézzel írt kategória-prompt rendszerekre

Minden talált küszöbszám API/tool/skill-JSON-sémákra vonatkozik (`input_schema`, `description` mező), nem szabad
szöveges "mikor tartozik ide egy bejegyzés" jellegű promptokra.

**Minősítés: nincs ilyen a szakirodalomban** — ez egy át nem hidalt rés a tool-description és a szabad szöveges
kategória-prompt use case között.

### Módszertani megjegyzés (nem tartalmi hiány, hanem eljárási korlát)

A WebFetch eszköz egy kis segédmodellen keresztül dolgozza fel az oldalakat. A magas tétű, döntő idézeteknél
(Anthropic Tool Search Tool küszöbök; Anthropic Skills PDF "20-50 skills" mondat) ezt kétszer, eltérő
prompttal futtatott független lekéréssel kereszt-ellenőrizték, és mindkétszer szó szerint ugyanazt kapták — ez
erősen valószínűsíti, hogy valódi oldaltartalomról van szó. Az alacsonyabb tétű, kiegészítő idézeteknél (pl.
blogok) ezt a kereszt-ellenőrzést idő hiányában nem végezték el mindenhol.

---

## SQ-05 — Van-e mért bizonyíték arra, hogy a nagy utasítás-blokk minden mást is ront

### 12. Nincs közvetlen mérés a pontos SQ-05 konfigurációra

A keresett kísérlet: (a) a hívó agent egy VÁLASZTHATÓ (nem "betartandó") kategória/leírás-menüt kap a
rendszerpromptban, ÉS (b) van egy ettől független, saját feladata is, ÉS (c) mérik, hogy a menü méretének
növelése rontja-e a SAJÁT feladat minőségét. Próbált keresések (ld. `keresesek.md`): "system prompt length
degrades performance other tasks unrelated instructions measurement", "instruction interference multiple
unrelated instructions same prompt LLM performance study", "number of tools available degrades unrelated task
accuracy LLM agent study", és további 3 variáns.

**Minősítés: létezhet, de nem találtuk meg.** A legközelebbi találat (Prospective Memory Failures, arXiv
2603.23530) is más elrendezést mér (KÖVETENDŐ szabály, nem VÁLASZTHATÓ menü). Ez erősen az "evidence of
absence" irányba billen (többszöri, különböző szögekből futtatott keresés sem hozott találatot), de nem zárható
ki teljes bizonyossággal, hogy egy nagyon friss vagy niche publikáció elkerülte a figyelmet — a WebSearch csak a
nyilvánosan indexelt tartalmat éri el.

### 13. Nincs "azonos token-budget, sok rövid vs. kevés hosszú" kontrollált kísérlet

A keresett összehasonlítás: a teljes token-mennyiséget FIXen tartva variálják, hogy sok rövid egységre vagy
kevés hosszú egységre van-e elosztva. Próbált keresések: '"many short" vs "few long" instructions same token
count LLM performance comparison', "consolidated tool description vs many separate tools same token budget
accuracy comparison study", '"number of options" classification prompt length degrades LLM accuracy choosing
category'.

**Minősítés: létezhet, de nem találtuk meg.** A legközelebbi találatok (S17 "Are Longer Prompts Always Better",
S18 MCP tool description ablation, S7 instrukció-kompilátor) mind más tengelyt mérnek (item-szám,
komponens-ablation, illetve tömörítés+átszervezés együtt) — egyik sem tartja fixen az össz-token-számot.

### 14. Chroma Context Rot riport — a disztraktor-szekció pontos számai csak grafikonon

A `trychroma.com/research/context-rot` oldalt kétszer is lekérték, kifejezetten a disztraktor-kísérlet (0/1/4
disztraktor) pontos %-os eredményeiért. Mindkétszer csak minőségi leírást kaptak vissza — a tool jelezte, hogy a
tényleges számok "only presented graphically in charts... without accompanying numerical tables in the text."

**Minősítés: létezhet, de nem találtuk meg** — a számok léteznek (a riport diagramjain), csak szöveges
formában nem kinyerhetők.

### 15. LongIns (arXiv 2406.17588) pontos táblázata nem került elő

Csak két minőségi mondat volt kinyerhető az absztraktból; a részletes GIST/LIST/LIMT táblázatok konkrét számai
nem. **Ez inkább erőforrás-korlát, mint "nincs adat" jellegű rés** — egy jövőbeli kereső ügynök érdemben
próbálkozhatna újra (pl. a PDF közvetlen letöltésével, más promptozással).

**Minősítés: létezhet, de nem találtuk meg** (a forrás saját jegyzete szerint inkább idő-/erőforrás-korlát, mint
valódi hiány).

### 16. Tudatos hatókör-szűkítések (nem hiányosságok, hanem döntések)

- Nem futtattak külön keresést kifejezetten magyar nyelvű forrásokra (a téma domináns nyelve angol).
- Nem mentek bele mélyen a "Context Discipline…" (S20) és "SkillReducer" jellegű, infrastruktúra/KV-cache-
  fókuszú munkákba, mert azok inkább számítási költségről, mint válaszminőségről szólnak (ez az SQ-01 hatóköre).
- Nem ellenőrizték részletesen a LIFBench (arXiv 2411.07037) és IFHierBench (arXiv 2607.27912) cikkeket — csak
  keresési találatként azonosították őket, idő-/terjedelem-korlát miatt nem fetchelték le.

**Minősítés: nem alkalmazandó** — ezek tudatos hatókör-döntések, nem "nem találtuk" jellegű hiányok; egy
jövőbeli kutatási kör bővítheti velük az anyagot.

### Eljárási megjegyzés (nem tartalmi hiány)

A `sq05/gaps.md` saját feljegyzése szerint az eredetileg kért `sq05/findings.md` fájl helyett — a fájlírás
eszköz "ne írj report/summary/findings/analysis nevű fájlt" szabálya miatt — a strukturált SQ-05 válasz a
`sq05/megallapitasok.md` fájlba került; ez a jelen összeállításban is innen lett feldolgozva.
