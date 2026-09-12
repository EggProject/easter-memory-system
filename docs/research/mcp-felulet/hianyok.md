# Hiányok — amire nem találtunk választ

Kampány: `mcp-felulet` · 2026-09-12


---

## SQ-01 — Mit tud kifejezni egy MCP eszközdefiníció

# SQ-01 — Hiányok, nyitott kérdések

## Valódi hiányok a specifikációban (evidence of absence, nem keresési kudarc)

1. **Nincs `description` mező hosszkorlát.** A `name` mezőre van SHOULD
   1–128 karakteres ajánlás, a `description`-re semmi. Négy releváns oldal
   (`tools`, `basic`, a `Tool` interfész teljes forráskód-kommentje) teljes
   átolvasása után sem találtam ilyen korlátot. Ez nekünk azért fontos, mert
   a `D-26/7` döntés szerint az indoklás megelőzi a kategóriát a sémában —
   ha hosszú indoklás-szövegeket teszünk a description-be, a specifikáció
   ezt nem tiltja, de nem is ad iránymutatást ésszerű felső határra.
2. **Nincs válaszméret-korlát vagy "túl nagy válasz" eljárás.** A lapozás az
   egyetlen mechanizmus. Külön WebSearch-csel (`site:modelcontextprotocol.io
   response size limit`) is rákérdeztem, nulla releváns találat jött. Nem
   zárom ki, hogy egy nem-normatív "best practices" guide (a
   `modelcontextprotocol.io/docs/...` ág, nem a `/specification/...` ág)
   foglalkozik ezzel — ezt a kutatási kört nem futottam le, mert a feladat
   kifejezetten a "hivatalos specifikációra" kérdezett, azon belül pedig ez
   tényleg hiányzik.
3. **Nincs kötelező névtér-szintaxis több szerver aggregálására.** A spec
   csak SHOULD szinten ajánl "valamilyen" disambiguation stratégiát (pl.
   előtag), konkrét formátumot nem ír elő, és explicit kizárja, hogy a
   `serverInfo.name`-re építsünk. Ez nyitott tervezési kérdés marad a mi
   oldalunkon, ha valaha több szerverre bontanánk a rendszert.

## Amit nem tudtam (ezen a körön belül) ellenőrizni

4. **A gyakorlati SDK/kliens-adoptáció állapota `2026-07-28`-ra.** A
   hivatalos blogbejegyzés említi, hogy "TypeScript, Python, Go, and C#"
   Tier 1 SDK-k már támogatják, és a Rust SDK béta státuszban van — de nem
   ellenőriztem, hogy pl. a Claude Desktop / Claude Code / más elterjedt
   MCP-kliensek ténylegesen a `2026-07-28` protokollverziót beszélik-e, vagy
   még visszafelé-kompatibilis módban a `2025-06-18`/`2025-11-25` handshake-et
   várják. Ez élesen releváns döntés a mi rendszerünk szempontjából (melyik
   verziót célozzuk), de ez inkább SQ-02/SQ-03 hatóköre — itt csak jelzem
   nyitott kérdésként.
5. **Nem kerestem rá dedikáltan** "mikor legyen valami resource és mikor
   tool" külön, elmélyült tervezési útmutatóra a `docs/` (nem
   `specification/`) ágban — a User Interaction Model szakaszokból
   levezetett válasz valószínűleg elég, de egy külön "guide" dokumentum
   létezhet bővebb indoklással. Ez SQ-02 (jó eszközfelület-tervezés)
   területére esik inkább, ott érdemes utánanézni.
6. **Nem találtam AI-összefoglalót forrásként** ebben a körben (ld.
   `searches.md`), tehát ez a visszatérő hiba itt nem fordult elő — ezt
   explicit rögzítem, mert a feladat kérte a figyelmet erre.

## Egy megjegyzésre méltó, nem-hiány, de figyelmeztető pont

7. A `2026-07-28` revízió **hat héttel** a mai dátum (2026-09-12) előtt
   jelent meg. A blogbejegyzés maga is elismeri: "there will be some
   migration cost, especially for developers that did depend on session
   identifiers." Ez azt jelenti, hogy bár ez a *jelenleg érvényes*
   specifikáció, a **gyakorlatban használt eszközök/cikkek/StackOverflow
   válaszok többsége még a korábbi, session-alapú modellt írja le** — ha a
   projekt csapata más forrásokból (nem ebből a kutatásból) tájékozódik,
   könnyen a `2025-06-18`/`2025-11-25` modellt fogja "az MCP-nek" hinni.
   Ezt explicit jelezni kell a szintézisben.


---

## SQ-02 — Milyen eszközfelületet használnak jól a modellek

# SQ-02 — Hiányok (gaps)

## 1. Nincs számszerű mérés a hibaüzenet-minőség és a helyreállási sikerarány kapcsolatáról (Q4)

Ez a legfontosabb hiány, mert a kérdés kifejezetten ezt kérte ("van-e mérés... hogyan kell
hibaüzenetet fogalmazni"). Amit találtunk: **kvalitatív, hivatalos ajánlás** ("legyen instruktív,
mondja meg mit próbáljon a modell") és **egy dokumentált viselkedési tény** (Claude 2-3
próbálkozás után feladja hibás/hiányos tool-hívásnál). **Nem találtunk** olyan tanulmányt vagy
gyártói mérést, amely két hibaüzenet-stílust (pl. "ERROR_400" vs "Hiányzik a 'location' mező, add
meg pl. 'Budapest, HU' formátumban") kontrollált módon összehasonlítva mérte volna a
helyreállási/sikeres-újrapróbálkozási arányt. Ez **hiányzó bizonyíték (absence of evidence)**, nem
**bizonyított hiány (evidence of absence)** — lehet, hogy létezik ilyen belső Anthropic/OpenAI
adat, csak nem publikus, vagy nem került elő a keresési budget alatt. Javasolt következő lépés, ha
ez a kérdés kritikus marad: közvetlenül az Anthropic tool-evaluation cookbook
(platform.claude.com/cookbook/tool-evaluation-tool-evaluation) végigolvasása, amit a fő
blogbejegyzés referenciaként említ, de amit ez a kör nem nyitott meg.

## 2. Nincs mért adat a kötelező paraméter (pl. indoklás) kihagyásának arányáról (Q5)

Találtunk egy általános (nem tool-specifikus) LLM hibataxonómiát (ErrorMap/ErrorAtlas, arXiv
preprint), ahol a "Missing Required Element" a 2. leggyakoribb hibakategória — de ez nem
function/tool-call kontextusban mért szám. A Berkeley Function-Calling Leaderboard (BFCL) valószínű
tartalmaz ilyen bontást (hiszen ismert kategóriái közt van "missing parameter" hibatípus), de a
leaderboard/dataset oldalait nem nyitottuk meg mélyen ebben a körben — **ez explicit, célzottan
zárható hiány**, ha valaki egy következő kutatási kört indít erre.

## 3. Nincs mért/dokumentált gyakorlat az MCP-szerverek tényleges idempotencia-megvalósítására (Q7)

A specifikáció definiálja az `idempotentHint`-et, de sem hivatalos ajánlást, sem felmérést nem
találtunk arra, hogy a valódi MCP-szerverek hogyan valósítják meg (vagy nem valósítják meg)
ténylegesen az idempotenciát ismételt hívásnál (pl. kliens-generált művelet-azonosító + dedup, vagy
egyszerűen semmi védelem). Ez egy tiszta specifikáció-szintű rés, amit a vault tervezésekor saját
döntéssel kell pótolni.

## 4. WebFetch által "renderelt" (nem verbatim) tartalom két esetben

- Az Anthropic fő blogbejegyzésben a "rossz" vs "jó" hibaüzenet-példapár **képként** szerepel az
  oldalon; a WebFetch (kis modell) ezt nem tudta szöveggé alakítani, csak azt jelezte, hogy a kép
  létezik, és körülírta a szöveges kontextust. **Nem konstruáltunk hozzá kitalált szöveget** — ezt a
  hiányt a megallapitasok.md is jelzi Q4-nél.
- Az OpenAI function-calling guide oldal első fetchelése egy **táblázatos összefoglalót** adott
  vissza a kért verbatim markdown helyett (pl. "Function Definition Schema" szekció táblázatos
  formában, nem az eredeti prózai szöveggel). Ez nem AI-generált "hamis" tartalom volt (a tények
  egyeznek a séma JSON-példával, amit ellenőriztünk), de módszertanilag jelezni kell: ez egy
  **kompresszált rendering**, nem szó szerinti másolat. Nem használtuk fel belőle szó szerinti
  idézetként semmit, csak parafrázisként jelöltük meg a megallapitasok.md-ben.
- Egyik fetch sem adott vissza **teljes oldal helyett AI-összefoglaló figyelmeztető oldalt** (pl.
  Cloudflare-jellegű "ez egy AI-összefoglaló" bannert) — ez a korábbi kampányok visszatérő hibája
  volt, itt nem fordult elő, de a fenti két esetet óvatosságból mégis jelezni kell.

## 5. Magyar nyelvi lefedettség — várható, nem hiányos

A playbook előírja, hogy intézményhez/joghoz kötött témáknál kötelező magyar nyelvű kört futtatni.
Ez a téma (LLM tool-use tervezés) nem magyar intézményi/jogi horgonyú, hanem angol nyelvű gyártói
dokumentáció-vezérelt. Egy ellenőrző magyar keresést mégis futtattunk (`MCP eszköz tervezés
hibaüzenet AI ügynök magyar`) — az eredmény kizárólag általános, marketing-jellegű MCP-bemutató
tartalom volt (Microsoft Learn HU, sidekickautomations.hu, devertix.hu stb.), egyik sem
foglalkozott a kérdés részleteivel (leírás-tervezés, hibaüzenet-formátum, kötelező paraméterek).
**Ez megerősíti, hogy nincs elérhető, releváns magyar nyelvű elsődleges forrás ezen alkérdéshez**,
nem azt, hogy nem néztünk utána.

## 6. Gorilla / BFCL mélyebb feldolgozás elmaradt

A Gorilla-cikk (arXiv 2305.15334, NeurIPS 2024 elfogadva — tehát valójában **T2 peer-reviewed**,
nem csak preprint) API-hallucinációról szól, ami rokon, de nem azonos a "kötelező paraméter
kihagyása" kérdéssel (a hallucináció inkább nem-létező API/funkció kitalálása). Nem dolgoztuk fel
részletesen idő/budget okokból — ha a szintézis ezt a kérdést kritikusnak ítéli, érdemes külön
lekérni.

## 7. "Egy nagy multi-action tool vs sok kicsi tool" — nincs közvetlen kontrollált összehasonlítás

Mindkét gyártó (Anthropic, OpenAI) **tervezési ajánlásként** a konszolidációt (kevesebb, nagyobb
eszköz egy `action` paraméterrel) javasolja, de egyik forrásunk sem közöl kontrollált kísérletet,
amely ugyanazt a feladatot egyszer egy nagy, egyszer több kis eszközzel oldatna meg, és mérné a
pontosságkülönbséget. A talált egyetlen kvantitatív tanulmány (Meta BoR-arXiv) más kérdésre
(retrieval-time jelöltlista-méret) mér. Ez a vault D-26/8-hoz hasonló döntéseknél (pl. "egy nagy
`manage_project` tool vs `create_project`/`update_project`/`delete_project` külön") releváns nyitott
kérdés, amit csak saját kiértékeléssel (ahogy az Anthropic blog is javasolja) lehetne lezárni.


---

## SQ-03 — Létező memória-MCP szerverek

# SQ-03 — Hiányosságok (gaps)

## Módszertani korlát — WebFetch "renderelés", nem bájtmásolat

A `WebFetch` eszköz minden esetben egy kis, gyors modellel dolgozza fel az oldalt a megadott
prompt szerint, még akkor is, ha a prompt explicit verbatim/szó szerinti visszaadást kér. Ez
**nem** azonos a feladatleírásban tiltott hibával ("egy fetch AI-összefoglalót ad vissza a valódi
oldal helyett", pl. egy keresőmotor AI Overview doboza egy valódi cikk helyett) — minden esetben a
tényleges célzott oldal tartalma alapján válaszolt az eszköz, nem egy külső AI-összefoglalót adott
vissza helyette. Ugyanakkor a gyakorlati hatás hasonló: **nem minden idézőjelbe tett "idézet" szó
szerinti** ebben a dokumentumban, ha a forrás egy GitHub issue/discussion vagy hosszabb doksioldal
volt, és a válasz "Summary of..."/"Based on the provided content..." jellegű bevezetőt kapott.
Ahol ez történt, a `megallapitasok.md`-ben és a `links.md`-ben jelöltem "tömörített"-ként. Két
eset volt kirívó:

- **`modelcontextprotocol/servers#4117`** — hét pontos hiányosság-lista, amit felhasználtam, de
  a hibajegy esetleges kommentjeit/válaszait (ha voltak) nem kaptam meg, csak az eredeti leírás
  tömörítését.
- **`mem0ai/mem0/discussions/4787`** — két közösségi választ kaptam (barry166, 23HughAI), de nem
  tudom, volt-e további válasz a szálban, amit a tömörítés kihagyott.

**Javaslat egy esetleges gap-körnek:** ha ez az SQ-03 anyag bekerül a szintézisbe és egy adott
állítás (pl. a `#4117` pontos hét pontja, vagy a mem0 "kilenc eszköz → egy search_memories"
migráció indoklása) kulcsfontosságúvá válik, érdemes egy második, célzottabb fetch-kört futtatni
kifejezetten ezekre az oldalakra, esetleg más promptozással (pl. rövidebb szakaszokra bontva
kérni a tartalmat).

## Konkrét, meg nem válaszolt kérdések

1. **Miért szüntetik meg az OpenMemory-t pontosan?** A `mem0ai/mem0#4923` hibajegy címén és
   metaadatain (nyitó: `trades2much`, 2026-04-22, lezárva) kívül semmilyen tartalmat nem sikerült
   kinyerni — a fetch szerint a hibajegy leírása mindössze annyi, hogy "README needs 'Sunsetting'
   warning in title", ami furcsa (ez inkább egy dokumentációs kérés, nem a döntés indoklása). Nem
   tudom, hogy a tényleges döntési indoklás egy másik issue-ban, egy blogbejegyzésben, vagy egy
   Discord-beszélgetésben van-e — nem találtam meg.
2. **A mem0 Claude Code plugin "9 eszköz → 1 `search_memories`" migrációjának pontos indoklása és
   dátuma.** Csak azt a mondatot kaptam meg tömörítve, hogy ez megtörtént; nem tudom, milyen
   konkrét problémákra volt válasz (túl sok eszköz zavarta a modellt? túl sok hibás hívás? ez
   egybevágna az SQ-02 méréseivel az eszközszám-korlátozásról, de ezt itt nem tudtam közvetlenül
   alátámasztani).
3. **Letta pontos forráskódja.** Két közvetlen `raw.githubusercontent.com` próbálkozás a
   `letta-ai/letta` repóra 404-et adott (a fájl-útvonal feltehetően megváltozott egy refaktorálás
   során). A Letta-adatok ezért egy közösségi audit (`carsteneu/ai-memory-comparison`)
   forráskód-hivatkozásaira támaszkodnak, amit T2-nek, nem T1-nek minősítettem. Nem zárható ki,
   hogy az audit egy korábbi verzióra vonatkozik, és a jelenlegi Letta már máshogy nevezi az
   eszközöket.
4. **basic-memory tényleges forráskódja.** Csak a hivatalos dokumentációs oldalt (T2) néztem meg,
   magát a `basicmachines-co/basic-memory` Python/TS forráskódot nem — a paramétertáblázatok
   nagyon részletesek és belsőleg konzisztensek, de nem T1-ellenőrzöttek.
5. **`gregorydickson/memory-graph` "claude-code-memory → MemoryGraph" migrációs dokumentum.** A
   `glama.ai`-n át próbáltam elérni, de a robots.txt letiltotta. A cím alapján ez pontosan egy
   "mit tanultunk, mit változtattunk" jellegű dokumentum lehetett volna — nem sikerült elolvasni.
   Nem próbáltam más útvonalon (pl. közvetlenül a GitHub-repón, ha van ilyen) elérni, időkorlát
   miatt.
6. **`carsteneu/ai-memory-comparison/evidence/` mappa teljes tartalma.** A GitHub fa-nézet
   robots.txt miatt nem volt listázható, a GitHub API pedig rate-limitelt (403) volt. Csak
   találgatással (`mem0.md`, `graphiti.md`, `letta.md` létezett; `basic-memory.md`,
   `mcp-memory.md` nem) jutottam a meglévő fájlokhoz. **Lehet, hogy van további releváns fájl
   ebben a mappában** (pl. `chatgpt-memory.md`, `openmemory.md`, `zep.md` külön a `graphiti.md`-től),
   amit nem találtam meg, mert nem tudtam a pontos fájlnevet.
7. **Nyelvi lefedettség.** Kizárólag angol nyelvű keresést végeztem. A téma (MCP-alapú
   memória-szerverek) túlnyomó többségben angol nyelvű, nemzetközi nyílt forráskódú közösségben
   zajlik, ezért ezt alacsony kockázatú hiánynak tartom, de a `search-playbook.md` szabálya
   szerint explicit ki kell mondanom: **nem futtattam nem angol nyelvű keresési kört.**
8. **Relevancia-jelzés Lettánál.** Nem találtam explicit numerikus relevancia-pontszámot az
   `archival_memory_search` válaszában (csak "semantically relevant" szöveges jellemzést) — nem
   tudom biztosan, hogy ez azért van, mert a Letta API valóban nem ad vissza számszerű score-t,
   vagy mert a forrás, amit láttam, egyszerűen nem részletezte ezt.
9. **`modelcontextprotocol/servers#2577/#2578/#2579`** — nem néztem meg részletesen ezt a három,
   feltűnően egymáshoz hasonló című hibajegyet (mindegyik "Bug Report and Resolution:
   `mcp-server-memory` Failures due to Race Condition and Environment Misconfiguration" címmel).
   Nem tudom, hogy ezek valódi duplikátum-bejelentések, egy bot által generált spam, vagy három
   különböző, releváns részlettel bővíthető beszámoló-e ugyanarról a hibáról.


---

## SQ-04 — Azonosítás és jogosultság MCP-ben

# SQ-04 — Hiányosságok, nyitott kérdések

## 1. Fetch-összefoglalás forrás-hűségi kockázata (visszatérő probléma, ahogy a feladat is jelezte)

- **github.com/github/github-mcp-server/docs/oauth-login.md** — a WebFetch a verbatim
  kérés ellenére **összefoglalást** adott vissza, nem a nyers oldalszöveget (nem volt
  "## All links" szakasz, a válasz explicit "The documentation does not explicitly
  explain..." jellegű meta-kommentárt is tartalmazott, ami a search-playbook szerint
  önmagában is jele a nem-verbatim capture-nek). A konkrét idézőjelbe tett mondatok
  ("On first use it walks you through...", "A static token still takes precedence...")
  valószínűleg pontosak, de ezt nem sikerült a nyers HTML/markdown oldallal
  keresztellenőrizni ebben a körben. **Ajánlás a szintézisnek:** ezt a forrást
  Közepes-nél magasabb megbízhatósággal ne kezeljék önmagában.
- **blog.modelcontextprotocol.io/posts/2026-07-28/** — hasonlóképpen: a válasz
  strukturált összefoglaló volt, saját alcímekkel ("Key Changes", "No Handshake or
  Sessions" stb.), amelyeket a fetch-eszköz generált, nem a blogbejegyzés eredeti
  szerkezete. A ténylegesen idézőjelbe tett mondatok ("Each request now travels on
  its own...", "Dropping the protocol-level session doesn't force...", "Authorization
  servers should return the `iss` parameter...") feltehetően szó szerintiek, a
  köréjük szerkesztett összefoglaló szöveg viszont **nem** forrás — csak a
  megallapitasok.md-ben idézőjelben szereplő részek tekinthetők elsődleges idézetnek.

## 2. Verzió-specifikus szövegek, amiket nem sikerült közvetlenül leellenőrizni

- A **2025-06-18-as** "Security Best Practices" oldal pontos szövegét nem töltöttem
  le — csak a changelog-bejegyzést ("Clarify security considerations... in a new
  security best practices page"), illetve a nála későbbi (2025-11-25, 2026-07-28)
  verziók szövegét. Lehetséges, hogy a "Confused Deputy" / "Token Passthrough"
  szakaszok pontos megfogalmazása 2025-06-18-ban még eltért a később idézett,
  szó szerint azonosnak talált 2025-11-25/2026-07-28-as szövegtől.
- A **2026-07-28-as authorization spec** "OAuth Grant Types" alfejezetét (amely
  2025-03-26-ban az Authorization Code vs. Client Credentials grant-ok
  megkülönböztetését tartalmazta) **nem sikerült megtalálni a jelenlegi oldal
  lekért verziójában.** Lehet, hogy: (a) máshova költözött egy aloldalra, amit nem
  kérdeztünk le; (b) a WebFetch kihagyta terjedelmi okokból; vagy (c) ténylegesen
  kikerült/átalakult a specifikációból. Ez közvetlenül összefügg a
  `contradictions.md`-ben részletezett client_credentials-kérdéssel.
- Nem sikerült megtalálni/lekérni a hivatalos **"MCP Authorization Extensions"**
  repository (github.com/modelcontextprotocol/ext-auth) tartalmát, amelyre a
  2026-07-28-as authorization spec hivatkozik ("A list of supported extensions can
  be found in the MCP Authorization Extensions repository") — ez tartalmazhatná a
  client_credentials-alapú, "enterprise" escenáriókra vonatkozó bővítményt, amit a
  Stack Overflow blog is említ ("A draft extension allows MCP clients to 'get
  tokens without the OAuth redirect'").
- A **SEP-1359 GitHub issue** ("Protocol-Level Sessions for MCP"), ami valószínűleg a
  stateless-átállás mögötti indoklást/vitát tartalmazza, csak a keresési
  találatok között bukkant fel — a tartalmát nem néztem meg.

## 3. Breadth-korlát: csak két valós implementáció mélyfeldolgozása

A budget (kb. 30 tool hívás) miatt csak **két** konkrét, sokfelhasználós MCP-szerver/
kliens azonosítási gyakorlatát dolgoztam fel mélyen: a GitHub hivatalos MCP szerverét
és az Anthropic/Claude connector-infrastruktúráját. Nem vizsgáltam meg (csak
keresési címként láttam, tartalmilag nem):

- Sentry, Notion, Linear, Stripe és más kereskedelmi MCP szerverek saját
  azonosítási mintáit.
- A `mcpauth/mcpauth` és hasonló, nyílt forráskódú "MCP auth middleware" projektek
  konkrét megvalósítását (ezek jó jelöltek lennének egy következő körnek, mert
  explicit, kódszintű mintát adnának a `sub`→belső user ID leképezésre).
- OpenAI, Google, Microsoft (Copilot) saját MCP-kliens-infrastruktúráinak
  azonosítási gyakorlatát — csak az Anthropic oldalt vizsgáltuk, ami torzíthatja az
  "iparági bevett minta" általánosítást egyetlen szereplő felé.

**Ez korlátozza a Q7/Q8 alatti "bevett minta"-állítás általánosíthatóságát**: amit
találtunk, egyértelműen igaz a vizsgált két implementációra, de nem tudjuk
teljes bizonyossággal kijelenteni, hogy ez *az* egyetlen bevett minta az egész
ökoszisztémában.

## 4. "Optional client identity" a stdio `_meta` mezőben (2026-07-28)

Ahogy a megallapitasok.md 5. pontja is jelzi: a 2026-07-28-as stdio-transport oldal
megemlíti, hogy a `_meta.io.modelcontextprotocol/*` mezőkben "optional client
identity" utazhat, de nem sikerült kideríteni (sem a lekért oldalakból, sem
kiegészítő kereséssel, budget-korlát miatt), hogy ez pontosan mit takar: a kliens
*szoftver* azonosítóját, egy munkamenet-azonosítót, vagy ténylegesen egy emberi
felhasználó azonosítóját. Ez direkt releváns lenne a mi rendszerünk stdio-ági
tervezéséhez, és érdemes egy célzott, következő körben (pl. a `schema.ts` vagy a
`_meta` mezőt definiáló aloldal közvetlen elolvasásával) tisztázni.

## 5. Claude Managed Agents identitás-modellje

A `claude.com/docs/connectors/building/authentication` oldal megemlíti, hogy a
"Claude Managed Agents uses a separate credential set", de nem részletezi, hogy ez
a credential-készlet emberhez kötött-e (mint a directory/custom connectorok), vagy
tartalmaz-e szolgáltatás-fiók jellegű elemet. Mivel a mi rendszerünk pontosan egy
"agent hívja a szervert a felhasználó nevében" architektúra, ez a pont különösen
releváns lenne egy következő körnek.
