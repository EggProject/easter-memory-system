# Szintézis — honnan tudja a rendszer a projektet, és hová kerül egy új bejegyzés?

Kampány: `projekt-kontextus/` · 2026-09-25 · 4 kutatási egység (SQ01–SQ04) + 3 ellenőrző egység (ELL01–ELL03), első kör; a második kör (SQ05–SQ08, ELL04–ELL06) a 7. szakasztól;
598 egyedi link, mind az
**Exa** keresővel, párhuzamos Sonnet alügynökökkel. Szintézis: Opus.

A kiváltó hiány: a `write_memory` kötelező adatai (tartalom, kategória, indoklás, prompt_version) között nincs, **hová**
kerül az új bejegyzés (`projects/<p>/`, `knowledge/`, `personal/<u>/`), és sehol nincs leírva, **honnan tudja** az agent
vagy a szerver, melyik projektben dolgozik a felhasználó. Ez a projektcél („hogyan olvassuk a session-ből és mikor hogyan
injektálunk") magja.

---

## 1. Az MCP-protokoll erre nem ad semmit — szándékosan

- A „roots" képesség (a kliens megmondja a munkakönyvtárát) a 2026-07-28-as változatban **elavult** (SEP-2577), és csak
  kérésre jön. A Codex forráskódja sosem küldi, a Cursor hirdeti, de hibát ad rá. (SQ01, ELL01/1, /6)
- A SEP-2567 kimondja: a hívások közötti állapot — például egy projekt-azonosító — **nem protokoll-fogalom, hanem
  eszköztervezési kérdés**. (ELL01/2)
- A szerver visszakérdezhet a felhasználótól (elicitation, választólistával), de a kliensek támogatása egyenetlen. (ELL01/3)

Vagyis ezt nekünk kell megoldani, és kétféle út van: **a kapcsolat hordozza a projektet**, vagy **az eszköz kéri paraméterben**.

## 2. Mit tudnak a kliensek

- **Mind a hat vizsgált kliens** (Claude Code, Codex, Gemini CLI, Cursor, Antigravity, Copilot/VS Code) tud **projektszintű
  MCP-konfigurációt** — a repóban élő fájlt —, benne a távoli szerver címével és **egyedi HTTP-fejléccel**. Hogy a
  projektszintű beállítás felülírja-e a felhasználói szintűt, az csak háromnál dokumentált egyértelműen. (ELL01/5)
- **A bejelentkezési token** a kliensek többségénél a szerver címéhez kötődik, nem a projekthez: a Codex és a Gemini CLI
  kifejezetten globálisan tárolja. Ha tehát projektenként **más címet** adnánk, projektenként újra be kellene lépni; ha
  **ugyanaz a cím, más fejléccel**, egy bejelentkezés elég. (ELL01/8)
- **Munkamenet-indító hook** az Antigravity kivételével mindegyikben van; közvetlen HTTP-hívásra csak a Claude Code és a
  Copilot képes, a többi shell-parancsot futtat. A Claude Code-nál a dokumentált korlát 10 000 karakter, de több
  független mérés szerint a modellhez ténylegesen kb. 2000 karakter jut el; a Codexnél kb. 2500 token. (ELL01/7)

## 3. Mit csinálnak a meglévő memória-rendszerek

| Minta | Példák |
|---|---|
| Az eszköz paraméterben kéri, a szerver alapértelmezéssel pótol | basic-memory (`project`), mem0 (`user_id`/`agent_id`/`run_id`), Graphiti (`group_id`) |
| **A kapcsolat hordozza — tudatosan nem eszköz-argumentum** | Zep hivatalos MCP-szervere (bejelentkezés és admin által beállított kapcsolat), OpenMemory (URL-útvonal), `opspresso/mcp-memory` (fejléc) |
| A munkakönyvtárból, fájlhierarchiából | Claude Code CLAUDE.md, Codex AGENTS.md |
| „Aktív projekt" állapot, külön paranccsal | Serena (`activate_project`) |
| Nincs projekt-fogalom | a Codex „Memories" funkciója — szándékosan globális; egy nyitott hibajegy ezt kifogásolja |

Háromszintű hatókört (személyes / projekt / közös) egyik vizsgált rendszer sem ad úgy, ahogy mi tervezzük. (ELL03/6)

## 4. Ki döntse el a hatókört — amit a biztonsági ajánlások és a mérések mondanak

- **OWASP** (LLM, MCP és Agentic Top 10) és az **AWS Well-Architected** egybehangzóan: a hozzáférés hatókörét a hívó
  környezet kényszerítse ki determinisztikusan, ne a modell döntsön róla. (ELL02/5)
- **Mérés:** a Meta FAIR CIMemories (ICLR 2026) szerint a frontier modellek egy memória-attribútum kontextus szerinti
  megosztásában **akár 69%-ban hibáznak**, és ugyanaz a kérés ismételve **0,1% és 25,1% között** ingadozott. (ELL02/6 —
  fenntartás: a cikk és a kódtár eltérő modellnevet ad ugyanahhoz a görbéhez.)
- **Esetek:** a mem0-ban a hatókör-mezőket a metaadat felülírhatta; három esetet javítottak, egy rokon eset ma is nyitott.
  A Claude Code git-repó szintű memória-megosztását a gyártó szándékosnak nevezte, nem hibának. Egy Claude Code-bejelentés
  szerint a modell kifejezett szabály ellenére keverte a személyes és a projekt-infót — ez egyetlen, ki nem vizsgált eset. (ELL03)
- Egyik vizsgált rendszer sem kér alapból visszaigazolást, mielőtt közös helyre ír. (SQ04)

## 5. A mérlegem

A kérdés valójában **kettő**, és a két fele mást kíván:

**(A) Melyik projektben vagyunk?** Ez nem tartalmi kérdés, hanem környezeti tény — tehát **ne a modell mondja meg**. A
legjobban illő út nálunk: **a repóban élő MCP-konfiguráció egy fejlécben adja meg a projektet**, ugyanazon a szervercímen.
Egy bejelentkezés elég; a szerver minden hívásnál ellenőrzi, hogy a felhasználónak van-e joga ahhoz a projekthez (D-11);
a modell nem tud másik projektet megnevezni. Ahol nincs ilyen fejléc (pl. általános beszélgetés), ott nincs aktuális
projekt: projektbe írni nem lehet, csak a közös tudásba és a személyes mappába.

**(B) Melyik szintre kerül egy bejegyzés — projekt, közös vagy személyes?** Ez tartalmi ítélet (a D-04/5 szerint egy
beszélgetésből kétféle láthatóságú tény is jöhet), tehát a hívó ágensnek kell eldöntenie — de a mérés szerint ebben
bizonytalan. Ezért: a szintet egy **kötelező, három értékű paraméter** adja (nincs alapértelmezés), a projekt nevét viszont
nem a modell adja, hanem a kapcsolat. A legnagyobb kockázat a **közös tudásba** (mindenki látja) írás: ott érdemes a D-20
mintáját követni — az első hívás nem ír, hanem visszaszól, hogy ez az egész cégnek látszik, és csak a második, kifejezett
hívás ír. Ez az én ötletem.

**(C) Mit lát a keresés egy projekt-munkamenetben?** A mai szöveg szerint a keresés a felhasználó teljes jogosult
halmazán fut (D-32/1), munkamenet-projekt pedig nincs — az én olvasatom szerint ez azt jelenti, hogy aki két projekthez is
jogosult, annak bármelyik munkamenetében mindkettő találatai megjelennek. A projektcél viszont azt mondja, hogy a projektek szeparáltak, és a másikat
csak külön engedéllyel látják. Ha van aktuális projekt, a keresés alapból arra, a közös tudásra és a személyes mappára
szűkülhet. Ez döntést kíván.

## 6. Amire nincs forrás

- Hogy a Claude Code HTTP-hookja elküldheti-e ugyanazt a projekt-fejlécet, mint az MCP-kapcsolat (a 4. ponthoz, a hook
  tartalmához kell majd).
- Hogy a projektszintű konfiguráció a Cursornál, az Antigravitynél és a Copilotnál megbízhatóan felülírja-e a globálist.
- Mérés arra, hogy egy „előbb szól, aztán ír" lépés mennyit javít a szintválasztáson.

---

# Második kör — mi kerüljön a hookon át az agent elé (a fejlesztés előtti lista 4. pontja)

SQ05–SQ08 + ELL04–ELL06, 2026-09-25. A D-48 után: a projektet a kapcsolat fejléce adja, a hook ugyanezt küldheti.

## 7. Az önkéntes használat gyenge — a működő eszközök beadnak

- **Egy kontrollált kísérlet** (arXiv:2607.20972, Saha, 2026-07; egyszerzős, nem lektorált; Claude Code + Claude Sonnet 5,
  egy nyílt forrású kódbázis feladatán): előre feltöltött, releváns tár, bekötött eszközök és kifejezett útmutatás mellett is
  **nulla memória-hívás 114 körben**; a szerző szavaival: *„Voluntary memory does not happen."* Ugyanő figyelte meg, hogy
  a beadás után az agent magától is többet keres: *„injection begets engagement"*. A kód nyilvános; független
  megismétlést nem találtunk. (SQ07, ELL06/1)
- **Egy másik mérés** (MEMTRACK, NeurIPS 2025 workshop) is azt találta, hogy a modellek nem használják jól a
  memória-eszközöket — más hibamóddal (ismételt, felesleges hívás). (ELL06/2)
- **Karbantartói tapasztalat:** „one cannot enforce an MCP tool to be called" (`alioshr/memory-bank-mcp` #24). (ELL06/3)
- **A gyártók és a működő eszközök beadnak:** az Anthropic API a memória-eszköz mellé automatikusan parancsoló mondatot
  szúr be; a claude-mem, a mem0-plugin és a Letta maga viszi a tartalmat a modell elé. (SQ05, ELL04)

## 8. Kérdésenkénti automatikus beadás — mit tudnak a kliensek

| Kliens | Hook minden üzenetnél | Beadhat szöveget? | Közvetlen HTTP | Ha lassú vagy hibás |
|---|---|---|---|---|
| Claude Code | `UserPromptSubmit` | igen | igen | időtúllépésnél a kimenet elvész, a kérés átmegy |
| Codex | `UserPromptSubmit` | igen | nem (parancs) | időtúllépésnél a kérés átmegy |
| Gemini CLI | `BeforeAgent` | igen | nem (parancs) | — |
| Cursor | `beforeSubmitPrompt` | **nem**, csak blokkolhat | nem | — |
| Copilot | van | a konfigurációs hook kimenete elvész | csak felhőben | — |
| Antigravity | nincs | — | — | — |

(ELL06/4–5.) Két ismert hiba a Claude Code-nál: egy hibajegy szerint a `UserPromptSubmit` JSON-os `additionalContext`-je
nem jut el a modellhez (a sima kimenet igen), egy másik szerint a beadott szöveg **minden fordulóval felhalmozódik** a
történetben. (SQ08)

**A zaj valós:** a mem0 csapata visszavonta a „vak", minden kérdésnél lefutó keresést a zaj és a felesleges hívások miatt;
a claude-mem alapból kikapcsolta a szemantikus beadást. (ELL06/6) Egy lektorált RAG-mérés szerint a hasonló, de
irreleváns szövegrészek 6–11 százalékponttal rontják a pontosságot — ez egyetlen kutatás két megjelenése. (ELL06/7)

## 9. A mérlegem a 4. ponthoz

A D-15/3 azt mondja: „A hook csak emlékeztet … elhagyható anélkül, hogy bármi elveszne" — mert az agent úgyis használja az
eszközöket. **A bizonyítékok ezt gyengítik:** az önkéntes használat alacsony, a működő eszközök beadnak. Ezért a hook
nálunk ne csak emlékeztető legyen, hanem — ahol a kliens tudja — **beadás**:

- **Munkamenet elején** egy sablonból készült, rövid szöveg az aktuális projektről (mi van benne, kategóriánként hány
  bejegyzés, és hogy keressen). Szövegíró modell nélkül.
- **Minden kérdésnél** (Claude Code, Codex, Gemini CLI) a szerver a kérdés szövegével keres a D-48 hatókörében, és
  **csak egy küszöb fölötti, kevés találatot** ad be — rövid kivonattal, egyértelműen „referencia, nem utasítás" jelöléssel,
  rövid kérdéseknél kihagyva. A küszöböt és a darabszámot **a fejlesztés előtt, a saját korpuszon kell kimérni**.
- Ahol a kliens nem tud beadni (Cursor, Antigravity, a Copilot konfigurációs hookja), ott marad az MCP — ez a kötelező alap.

Ez a D-15/3 átírását jelenti — erről a tulajdonos dönt.

## 10. Amire nincs forrás

- Több kliensre kiterjedő, kontrollált mérés az önkéntes és a beadott memória különbségére.
- A Gemini CLI beadási korlátja.
- A saját korpuszunkra érvényes relevancia-küszöb és darabszám.
