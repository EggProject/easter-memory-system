# Ellentmondások — ahol a források nem egyeznek

Kampány: `mcp-felulet` · 2026-09-12


---

## SQ-01 — Mit tud kifejezni egy MCP eszközdefiníció

# SQ-01 — Ellentmondások és verzió-eltérések

Ebben a körben nem találtam **valódi ellentmondást** két egyenrangú, T1
forrás között (minden forrás egyazon hivatalos domain egymást követő
verziói vagy egymást kiegészítő aloldalai voltak). Amit találtam, azok
**verzió-közti eltérések** — ezeket itt különítem el explicit, mert a
feladat kérte, hogy "ha több él egymás mellett, mondd meg, melyik mit
változtatott".

## 1. `structuredContent` típusa

- **`2025-06-18`–`2025-11-25`**: "Structured content is returned as a JSON
  **object** in the `structuredContent` field" — csak objektum.
- **`2026-07-28`**: "Structured content is returned as a JSON **value** in
  the `structuredContent` field ... This can be any JSON value (object,
  array, string, number, boolean, or null)" — bármilyen JSON érték.

Ez nem ellentmondás, hanem explicit bővítés — a `2026-07-28` changelog
maga is dokumentálja ("Loosen ... `structuredContent` to allow any JSON
value", SEP-2106).

## 2. Erőforrás-nem-található hibakód

- **`2025-11-25` és korábbi**: `-32002`.
- **`2026-07-28`**: `-32602` (Invalid Params), a `-32002`-t visszafelé
  kompatibilitásból a kliensnek **SHOULD** még elfogadnia, de a szervernek
  **MUST NOT** kibocsátania.

Explicit dokumentált váltás, nem ellentmondás — de fontos, mert egy
`2025-11-25`-öt implementáló szerver és egy `2026-07-28`-at váró kliens
között ez interop-problémát okozhatna, ha a kliens szigorúan csak
`-32602`-t venné figyelembe (a spec ezt a kliens oldalán explicit SHOULD
szinten hidalja át).

## 3. `listChanged` értesítés kézbesítési mechanizmusa

- **`2025-11-25` és korábbi**: automatikus — ha a szerver deklarálta a
  `listChanged: true` képességet, a kliens minden további feliratkozás
  nélkül megkapta a `notifications/tools/list_changed` üzenetet.
- **`2026-07-28`**: feliratkozás-alapú — a kliensnek explicit
  `subscriptions/listen`-t kell nyitnia `toolsListChanged: true`
  paraméterrel, különben **nem kap** értesítést, még akkor sem, ha a szerver
  deklarálta a képességet.

Ez a legnagyobb gyakorlati hatású eltérés a mi projektünkre nézve (a
kategória-szerkeszthetőség miatt), ezért ezt a `megallapitasok.md` 7.
pontjában részletesen kifejtettem. Nem ellentmondás a két verzió között —
egyértelműen dokumentált, szándékos protokollváltás (SEP-2575) —, de a
szintézisnek külön ki kell emelnie, mert könnyen elsikkad, ha valaki csak a
`2025-11-25` doksit olvassa (ami továbbra is elérhető és sok helyen
hivatkozott).

## 4. Hibakód-számozás MCP-specifikus kódokra

- **`2025-11-25`**: `HeaderMismatch` = `-32001`, `MissingRequiredClientCapability`
  = `-32003`, `UnsupportedProtocolVersion` = `-32004`.
- **`2026-07-28`**: ugyanezek átszámozva `-32020`, `-32021`, `-32022`-re, egy
  új, explicit particionálási politika bevezetésével (`-32000`–`-32019`
  legacy/implementáció-specifikus, `-32020`–`-32099` MCP-fenntartott).

Nem ellentmondás, dokumentált renumbering — de ha valaki egy `2025-11-25`
korú kódmintát másolna be a mi rendszerünkbe, rossz (és a jelenlegi spec
szerint tiltott) kódtartományt használna.

## Módszertani megjegyzés

Mind a négy pont **azonos tier-szintű (T1), egymást nem cáfoló, hanem
időrendben egymásra épülő** forrásokból ered — a hivatalos changelog minden
esetben explicit megnevezi a régi és az új állapotot is, tehát ezek nem
"vitatott" (`Vitatott`) jellegű állítások, hanem dokumentált evolúciók.
A szintézisben ezért nem GRADE "Vitatott" címkével, hanem "melyik verzióban
mi változott" táblázatos formában érdemes szerepeltetni őket.


---

## SQ-02 — Milyen eszközfelületet használnak jól a modellek

# SQ-02 — Ellentmondások és eltérések

## 1. Eltérő számszerű küszöb a "hány eszköz még jó" kérdésre — Anthropic vs OpenAI

- **Anthropic** (T1 dokumentáció, T2 mögöttes mérés): "Claude's ability to pick the right tool
  degrades once you exceed **30–50 available tools**." Emellett: "Use tool search when... you have
  **10 or more tools**."
- **OpenAI** (T1 hivatalos dokumentáció): "Start with **fewer than 20** initially available
  functions."

**Értékelés**: ez nem feltétlenül valódi ellentmondás — mindkét szám a saját gyártó saját modelljére
és saját mérési módszertanára vonatkozik, és nincs közös benchmark, ami összevethetővé tenné őket.
Az OpenAI száma inkább egy **konzervatív kiindulási ajánlás** ("start with"), az Anthropic száma egy
**megfigyelt romlási pont** ("degrades once you exceed") — a kettő különböző dolgot mér (ajánlott
kiindulás vs empirikusan észlelt töréspont). Mégis érdemes jelezni: **ha valaki csak az egyik
gyártó számát idézi abszolút határként, az félrevezető**, mert a másik gyártó másik számot ad.
**Nem oldható fel** a rendelkezésre álló forrásokból, melyik a "helyes" szám — mindkettő T1
forrásban szerepel, de egyik sem közöl mögöttes nyers adatot, ami az összevetést lehetővé tenné.
Minősítés a validation-protocol skála szerint: **Vitatott** (két hiteles forrás, eltérő számmal,
nincs egyértelműen jobb/frissebb).

## 2. Az annotációk mint "csak javaslat" (spec) vs a gyakorlatban tapasztalt egylépéses/kemény blokkolás (Codex CLI)

A hivatalos MCP-specifikáció szerint az annotációk (pl. `destructiveHint`) **csak hint-ek**, amiket
a kliens figyelmen kívül hagyhat. Ezzel szemben a Codex CLI leírása (T3/T4 másodlagos forrás)
konkrét, **kikényszerített** viselkedést ír le: `destructiveHint == true` esetén mindig jóváhagyást
kér, és konfigurációval **teljesen le is tiltható** ("hard block, not a prompt"). Ez nem logikai
ellentmondás (a specifikáció NEM tiltja, hogy egy kliens szigorúan vegye figyelembe a hint-eket,
csak azt mondja, hogy nem KÖTELEZŐ), de fontos árnyalás: **a specifikáció megengedő jellege és egy
konkrét kliens szigorú gyakorlata két külön dolog** — a vault tervezésénél nem szabad feltételezni,
hogy minden kliens úgy fog viselkedni, mint a Codex CLI; a szerver oldali védelem (mint a Supabase
MCP server mintája) emiatt szükséges, nem opcionális.

## 3. "Kevesebb, nagyobb tool" tervezési ajánlás vs a Meta BoR-tanulmány más léptékű problémája

Nem valódi ellentmondás, de **könnyen összekeverhető, ezért itt rögzítjük**: Anthropic/OpenAI a
tool-KÖNYVTÁR tervezésének idejére (design-time) ad tanácsot ("konszolidálj kevesebb tool-ba"),
míg a Meta BoR-tanulmány egy **retrieval-time** kérdésre (hány jelöltet mutassunk meg egy adott
keresési lépésben, amikor több száz/ezer tool közül válogatunk) ad mért választ. A kettő
összefésülése ("minél kevesebb tool van összesen, annál jobb" vs "minél kevesebb jelöltet mutass
egy keresésnél, annál jobb, DE adaptívan") **felszínesen hasonló következtetésre jut** (kevesebb
jobb), de más mechanizmusból és más mért jelenségből. A szintézisnek nem szabad a Meta-tanulmány
számait (pl. "K=7.4") úgy idéznie, mintha az Anthropic 30-50-es küszöbét pontosítaná — ez két
különböző metrika.

## 4. A "concise/detailed" 206 vs 72 token szám — egyetlen illusztráció, nem benchmark-átlag

Ez nem ellentmondás más forrással, de fontos figyelmeztetés a szintézis felé: ez a szám egyetlen,
konkrét Slack-thread példából származik (Anthropic saját blogbejegyzése), **nem** egy szisztematikus
mérés átlaga sok tool-on és feladaton keresztül. Ha a szintézis ezt úgy idézi, mintha "a concise
válaszok általánosan kb. 65%-kal rövidebbek", az túlgeneralizálás lenne a forrás tartalmához képest.

## 5. Nincs egymásnak ellentmondó forrás a hibaüzenet-tervezés alapelvére

Ellenőriztük kifejezetten: az Anthropic ("write instructive error messages... what Claude should
try next") és az MCP hivatalos specifikáció (isError csatorna, protocol vs execution error
megkülönböztetése) **nem mond ellent egymásnak** — kiegészítik egymást (az egyik a tartalmi
minőségről, a másik a csatorna-struktúráról szól). Ezt azért rögzítjük explicit módon, mert a
feladatkiírás kifejezetten kérte az ellentmondások keresését ezen a kritikus ponton, és a nemleges
eredmény is dokumentálandó.


---

## SQ-03 — Létező memória-MCP szerverek

# SQ-03 — Ellentmondások

## 1. mem0 dokumentáció vs. tényleges viselkedés — ellentmondás-feloldás

- **Állítás A (dokumentáció, T2, idézve a `mem0ai/mem0#4896` hibajegyben):** a mem0
  dokumentációja szerint "Latest truth wins when contradictions detected" — azaz ha egy új
  memória ellentmond egy régi, tárolt ténynek, a rendszernek fel kéne ismernie ezt, és az újabbat
  kellene megtartania.
- **Állítás B (tényleges kód/viselkedés, T1, ugyanaz a hibajegy + a hozzá tartozó reprodukciós
  lépések):** a 2026 áprilisi "v3" ADD-only architektúra ezt **nem teszi meg** — két egymásnak
  ellentmondó tény (pl. "a nevem X" majd "a nevem Y") mindkettő külön ADD eseményként kerül be,
  felülírás vagy összevonás nélkül.
- **Feloldás/értelmezés:** ez nem két különböző forrás közötti ellentmondás, hanem a **gyártó
  saját dokumentációja és a gyártó saját kódjának tényleges viselkedése közötti** eltérés — a
  hibajegy bejelentője explicit "documentation mismatch"-nek nevezi. A közösségi válasz szerint ez
  szándékos tervezési döntésnek tűnik (a v2-es ADD/UPDATE/DELETE/NONE logikát tudatosan
  egyszerűsítették v3-ban), de a dokumentációt (állításom szerint, a hibajegy idézete alapján) nem
  frissítették ezzel összhangban. **Ezt magas biztonsággal (a hibajegy T1 jellege miatt) kezelem,
  de nem ellenőriztem közvetlenül a jelenlegi `docs.mem0.ai` oldalon, hogy az idézett mondat még
  mindig szerepel-e ott** — ez gap is egyben, lásd `gaps.md`.

## 2. mem0 duplikátumkezelés — két, egymásnak részben ellentmondó közösségi leírás

- **`#4787` discussion válasz (barry166, 2026-06-29, T2/T3 — közösségi válasz, nem hivatalos
  mem0-alkalmazott jelöletlen):** "New memories are still emitted as ADD, but they can include
  `linked_memory_ids` pointing to related old memories" — ez azt sugallja, hogy van egy
  **összekapcsolási** mechanizmus az ellentmondó/kapcsolódó memóriák között.
- **`#4896` issue (T1, hibajegy leírás):** a reprodukciós lépések szerint két ellentmondó tény
  (két különböző név) **egyszerűen mindkettő bekerül**, semmilyen `linked_memory_ids` vagy egyéb
  összekapcsolás említése nélkül a hibajegyben.
- **Feloldás/értelmezés:** nem zárható ki, hogy a két leírás **különböző verziókra** vonatkozik
  (a discussion válasz dátuma később van, mint amikor a `#4896`-ban leírt "mem0 version 2.0.0"
  környezet készült — bár a "2.0.0" itt valószínűleg a mem0 könyvtár verziószáma, nem feltétlenül
  ugyanaz az időpont, mint a discussion válaszé). Lehet, hogy a `linked_memory_ids` egy időközben
  bevezetett funkció, amit a hibajegy bejelentője nem látott/nem az ő verziójában volt jelen.
  **Nem tudtam egyértelműen eldönteni, hogy a két állítás időben egymást követi-e (funkció
  hozzáadva a hibajegy után), vagy egyszerre igaz mindkettő valamilyen más okból (pl. csak
  bizonyos hívási módokban kap `linked_memory_ids`-t az új memória).** Ezt `Alacsony` bizonyossággal
  kezelem, és gap-ként is rögzítem.

## 3. Nincs más éles ellentmondás a vizsgált forrásaim között

A többi szerverre (hivatalos referencia, Graphiti, Letta, basic-memory, OpenMemory, közösségi
forkok) vonatkozó állításaim forrásai (elsősorban T1 forráskód/README, illetve egy konzisztens
módszertanú, forráskódra hivatkozó közösségi audit) nem mondtak egymásnak ellent — ahol a
`carsteneu/ai-memory-comparison` audit egy korábbi (nem az én forrásom, hanem az ő saját
projektjük korábbi) összehasonlító táblázatot javított ("claims ❌ — DISCOVERY ❌→✅" jelölések),
azt **nem** kezelem ellentmondásnak az én szintézisemben, mert az egy módszertani önkorrekció volt
az ő oldalukon ("code beats docs" elv), nem két, általam idézett forrás közötti feszültség.


---

## SQ-04 — Azonosítás és jogosultság MCP-ben

# SQ-04 — Ellentmondások és feszültségek

## 1. "Optional" a specifikációban vs. "gyakorlatilag elvárt" a valós, sokfelhasználós rendszerekben

Nem klasszikus forrás-ellentmondás, hanem egy **tervezési feszültség**, amit érdemes
tudatosítani: a spec minden verzióban kimondja, hogy a hitelesítés **OPTIONAL**
("Authorization is OPTIONAL for MCP implementations"), miközben a gyakorlati
tutorial ugyanakkor azt írja, hogy "strongly recommended" mihelyt a szerver
"user-specific data"-t kezel vagy "audit who performed which actions" szükséges —
ami pontosan a mi rendszerünk esete. **Ez nem ellentmondás a forrásokban**, csak azt
jelenti, hogy a protokoll semlegesnek szánja magát, és a döntés súlyát teljes
egészében az implementátorra (ránk) hárítja. **Confidence a feszültség létezésére:
Magas** — mindkét mondat ugyanabból a hivatalos dokumentumkörből, egymást nem cáfolva,
de eltérő hangsúllyal szerepel.

## 2. A Client Credentials grant sorsa a specifikációban — nyitott, nem lezárt kérdés

- **2025-03-26**: a spec kifejezetten leírja mindkét OAuth grant-típust (Authorization
  Code = emberi felhasználó nevében; Client Credentials = "the client is another
  application (not a human)").
- **Stack Overflow blog (T2, 2026-01-21)**: azt állítja, hogy "The client credentials
  grant was mentioned in the 2025-03-26 version of MCP, **was removed** and now is
  **coming back**" — vagyis valamelyik köztes verzióban (2025-06-18 vagy 2025-11-25)
  ez a szakasz kikerült a specifikációból, majd 2026 elején napirendre került a
  visszahozatala.
- **2026-07-28-as authorization spec** (a mi lekérésünk): a "Roles" és "Overview"
  szakaszokban nem szerepel explicit "OAuth Grant Types" alfejezet a Client
  Credentials/Authorization Code megkülönböztetéssel.

**Ez háromféleképpen oldható fel, és ebben a körben nem sikerült eldönteni, melyik az
igaz:**
(a) a szakasz tényleg kikerült és 2026-07-28-ban sem tért még vissza (a blog
"coming back"-je egy jövőbeli, e riport idején még nem élő tervre utalt);
(b) a szakasz létezik a 2026-07-28-as specifikációban, csak egy olyan aloldalon,
amit ez a kutatási kör nem kérdezett le (pl. egy külön "OAuth Grant Types" oldal a
`basic/authorization/` alatt, hasonlóan a `client-registration`,
`authorization-server-discovery`, `security-considerations` alstruktúrához, amit
láttunk hivatkozva, de nem nyitottunk meg mindet);
(c) a WebFetch a hosszú oldalt tömörítve adta vissza, és a szakasz létezik, csak
kimaradt a kapott szövegből.

**Ajánlás:** a szintézisben ezt "Ellenőrizetlen" címkével kell kezelni, és — mivel ez
közvetlenül releváns Q8-ra (agent mint közvetítő, service-account minta léte/nem
léte a jelenlegi specifikációban) — egy következő kutatási körben célszerű
közvetlenül megnyitni a `https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/`
alatti összes aloldalt, és/vagy magát a GitHub repo `.mdx` forrásfájlját.

## 3. A stdio `_meta` "optional client identity" mezője és a "nincs azonosítás stdio-n" alapelv közötti feszültség

A spec 2025-03-26 óta következetesen azt az elvet képviseli, hogy stdio-n nincs
protokollszintű azonosítás, és a hitelesítést a "környezetre" (environment) kell
bízni — ez explicit, ismételt MUST/SHOULD-szintű állítás. Ugyanakkor a 2026-07-28-as
stdio-oldal új szövege megemlíti, hogy a `_meta.io.modelcontextprotocol/*` mezőkben
**"optional client identity"** utazhat a stdio csatornán is. Ez a két állítás nem
zárja ki egymást formálisan (az egyik arról szól, hogy nincs *hitelesítés*, a másik
csak azt mondja, hogy *lehet* identitás-adat a metaadatban — ami nem ugyanaz, mint
hitelesített azonosítás), de **gyakorlati feszültséget hordoz**: ha egy jövőbeli MCP
kliens elkezdi ezt a mezőt "ember-azonosítóként" használni, az pontosan az a fajta
"bízz a hívó fél önkéntes állításában" minta lenne, amit a token-passthrough és a
confused-deputy szakaszok kifejezetten *tokenekre* nézve tiltanak — csak itt nincs is
token, aminek az érvényességét ellenőrizni lehetne. **Ezt a kutatás nem tudta
tisztázni** (ld. `gaps.md` 4. pont) — jelöljük nyitott kérdésként, mert releváns a mi
architektúránkra (egy gép, egy szerverfolyamat, több `personal/<email>` gyökér).

## 4. "Bevett minta" általánosíthatósága — módszertani korlát, nem tartalmi ellentmondás

A megallapitasok.md 7-8. pontjai egy konzisztens, jól dokumentált mintát írnak le
(OAuth token → `sub`/`aud` validáció → belső user ID), de ez **két** implementáció
(GitHub, Anthropic) alapján lett rekonstruálva. Nincs talált forrás, amely ezzel
*ellentétes* mintát írna le egy más, hasonlóan nagy, sokfelhasználós MCP
rendszerben — de ez lehet azért is, mert a kutatás nem nézett meg ilyen forrásokat
(ld. `gaps.md` 3. pont), nem azért, mert bizonyítottan nincs ellenpélda. Ezt a
szintézisnek "Közepes" konfidenciával, nem "Magas"-sal érdemes kezelnie az
általánosító mondatoknál.
