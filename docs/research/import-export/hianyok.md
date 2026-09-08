# Hiányok — import és export kutatás (K-03)

Az `sq01..sq04/gaps.md` egyesítve. Minden tételnél megjelölve, hogy a forrás-dokumentum melyik
kategóriába sorolta magát: **[NINCS ILYEN]** — a kutatás azt állítja, hogy a jelenség/szabály/adat
a szakirodalomban/gyakorlatban feltehetően nem létezik (evidence of absence, kimerítő keresés után);
vagy **[NEM TALÁLTUK MEG]** — létezhet, de ez a kutatási kör nem ért el hozzá, vagy nem volt rá
ideje/eszköze (absence of evidence). Ahol a forrás maga jelzett átmenetet vagy bizonytalanságot a két
kategória közt, azt is jelöljük.

---

## SQ-01 — Markdown-tudástárak export-formátumai

### 1. Joplin JEX/RAW — van-e dedikált manifeszt-fájl a csomagon belül?
**[NEM TALÁLTUK MEG.]** A hivatalos doksi és a hivatalos fórum leírása alapján valószínűsíthető,
hogy maga az adatbázis-struktúra (ID-alapú fájlnevek, szülő-hivatkozások) tölti be a manifeszt
szerepét, de erre nincs konkrét forráskód-idézet vagy hivatalos doksi-mondat. A Joplin
forráskódjában (`InteropService_Exporter_Jex` vagy hasonló) való elmélyedésre nem jutott idő.
Státusz a forrásból: "nyitott — nem bizonyítottan nincs, hanem nem találtuk meg / nem volt időnk
alaposan megnézni."

### 2. Logseq DB-gráf zip-backup export — forráskód-szintű megerősítés hiányzik
**[NEM TALÁLTUK MEG.]** A `db-based-export-repo-as-zip!` függvény létezéséről/viselkedéséről
kizárólag a deepwiki.com (T3, AI-generált) forrásból van adat; a `src/main/frontend/handler/export.cljs`
fájlt nem kérdezték le nyers forráskódként. Érdemes lenne közvetlenül lekérni a GitHub raw URL-t.

### 3. Notion Markdown export — pontos fájlformátum a metaadatra nézve
**[NEM TALÁLTUK MEG.]** Nem sikerült megerősíteni: (a) van-e frontmatter-szerű blokk az exportált
`.md` fájl tetején; (b) bekerül-e a created_time/last_edited_time/created_by/last_edited_by
bármelyike a fájlba, vagy csak API-szinten létezik; (c) van-e a fájlnévben egyedi azonosító. A
hivatalos "Export your content" súgóoldal egyszerűen nem tér ki erre a szintre — ezt csak egy
tényleges exportált fájl megvizsgálása döntené el, ami kívül esett a kutatás keretén.

### 4. Ékezetes / speciális karakteres fájlnevek kezelése
**[NEM TALÁLTUK MEG.]** Egyik vizsgált eszköznél (Obsidian, Logseq, Joplin, Notion, Zettlr, Foam,
Dendron) sem található explicit, dedikált hivatalos dokumentáció erről. Amit találtak, az közvetett
bizonyíték bug-jelentésekből (Joplin #853, #3473). Ez valószínűleg csak tényleges teszteléssel
zárható le megbízhatóan (kísérleti munka, nem kutatás).

### 5. Obsidian — automatikus fájlrendszer-metaadat a frontmatterben
**[RÉSZBEN NINCS ILYEN, RÉSZBEN NEM TALÁLTUK MEG.]** Nincs sem megerősítő, sem cáfoló hivatalos
mondat arra, hogy az Obsidian automatikusan beírná a fájl létrehozás/módosítás idejét vagy a
szerzőt a frontmatterbe — ez negatív bizonyíték (a hivatalos Properties-oldal hallgatása), nem
közvetlen tagadás. A forrás szerint "erős a gyanú, hogy nincs ilyen automatizmus, de ezt hivatalos
forrásból nem sikerült 100%-osan kimondatni."

### 6. "Elterjedt, nyílt csereformátum" — nincs másodlagos/harmadik feles megerősítés a negatív állításra
**[NINCS ILYEN — de a megerősítés maga NEM TALÁLHATÓ.]** A "nincs elterjedt csereformátum" válasz
saját, közvetlen T1-bizonyítékokból (a 4 vizsgált eszköz mind saját formátumot használ) levont
következtetés, Magas biztonságú — de nem talált olyan külső elemző/szakértői forrást, amely
kifejezetten ezt a hiányt dokumentálná/elemezné (csak content-farm/marketing találatok jöttek fel).

### 7. Vault-LD elterjedtsége/valós használata
**[NEM TALÁLTUK MEG.]** Csak a projekt saját weboldala az információforrás; nincs harmadik féltől
származó megerősítés vagy kritika a tényleges használtságról. Valószínűleg azért, mert a projekt
ténylegesen nagyon kicsi/friss.

### 8. OKF harmadik feles adaptációja
**[NEM TALÁLTUK MEG — időfüggő.]** A Google saját közlése szerint (2026 közepén) még nem volt
dokumentált harmadik feles (nem Google) implementáció vagy elfogadás; a kutatás időpontja csak
néhány hónappal van a v0.2 bejelentés után, érdemes később újranézni.

---

## SQ-02 — Ütközéskezelés importnál

### 1. Nincs mért, kvantitatív bizonyíték kifejezetten import-ütközési stratégiákra
**[NINCS ILYEN — közepes-magas bizonyossággal, kimerítő keresés után.]** Nem található olyan
tanulmány, incidens-elemzés vagy hibajegy-statisztika, amely kifejezetten a "kihagyás vs. felülírás
vs. átnevezés vs. kézi döntés vs. teljes megszakítás" stratégiákat hasonlítaná össze fájl-/
jegyzetimport kontextusában. Ugyanakkor van néhány **[NEM TALÁLTUK MEG]** jellegű, fel nem
dolgozott akadémiai szál (ld. lent, 7. pont) — ezért a forrás explicit jelzi: "ez nyitott kérdés,
nem lezárt »nincs bizonyíték« állítás" a kapcsolódó tudományos irodalom teljes egészére nézve, csak
a ténylegesen átnézett forrásokra.

Az egyetlen ténylegesen mért, lektorált analóg forrás (Brindescu et al. 2020) **tartalmi (soron
belüli) git-ütközésről szól, nem fájlnév-ütközésről importnál** — analógia, nem közvetlen
bizonyíték.

### 2. Apple Human Interface Guidelines — nem sikerült elérni
**[NEM TALÁLTUK MEG — technikai okból.]** A `developer.apple.com/.../alerts` oldal kliensoldali
JavaScript-renderelést igényel, a WebFetch csak "This page requires JavaScript" üzenetet kapott.
Nem próbálkoztak más lekérő eszközzel (ez megkerülésnek számítana). Apple hivatalos
destruktív-akció ajánlása ezért hiányzik ebből a kutatásból.

### 3. Tar-kicsomagolás atomicitása — nincs erős elsődleges forrás
**[NEM TALÁLTUK MEG.]** Nincs kifejezett dokumentáció arra, hogy a `tar` kicsomagolás
félbeszakadás esetén milyen részleges állapotot hagy hátra. A jelenség maga (soros fájlírás, nincs
tranzakció) levezethető a formátum architektúrájából és analóg a cp/rsync viselkedésével, de ez
nem azonos egy idézhető hivatalos dokumentációval.

### 4. Joplin (és általában jegyzet-appok) import-tranzakció szintje ismeretlen
**[NEM TALÁLTUK MEG.]** Nem állapítható meg forráskód-vizsgálat nélkül, hogy a Joplin JEX-import
egyetlen adatbázis-tranzakcióban fut-e vagy jegyzetenként commitol. A fórum-/issue-források csak a
végeredményt (duplikáció) írják le, a belső mechanizmust nem.

### 5. MySQL import-eszközök nincs elsődleges forrással alátámasztva
**[NEM TALÁLTUK MEG.]** A PostgreSQL/SQLite mellett a MySQL-oldalt (`INSERT IGNORE`/`REPLACE INTO`)
csak keresési találatok szintjén érintették, hivatalos MySQL-dokumentációt erre nem kértek le.

### 6. Nyelvi lefedettség
**[TUDATOS KIHAGYÁS, NEM HIÁNYPÓTLANDÓ.]** Kizárólag angol nyelvű keresés futott. A vizsgált
eszközök nemzetközi, angol nyelvű dokumentációs kultúrával rendelkeznek — a forrás szerint ez nem
súlyos hiány, de a szabály szerint explicit ki kell mondani: nem futtattak magyar nyelvű keresési
kört.

### 7. Fel nem dolgozott, releváns tudományos találatok
**[NEM TALÁLTUK MEG — jövőbeli körnek.]** "Challenges of Resolving Merge Conflicts: A Mining and
Survey Study" (Saarland Egyetem); "Lock-Free Collaboration Support for Cloud Storage Services"
(FAST'20); "Towards Reliable User Collaboration over Cloud-based File Synchronization System:
Dropbox as a Case Study" — egyik sincs feldolgozva, pontos URL a `linkek.md` B) szakaszában.

---

## SQ-03 — Személyes adat exportja (GDPR)

### 1. GitHub migrációs archívum manifesztje
**[NEM TALÁLTUK MEG.]** A két hivatalos GitHub Docs oldal nem ír kifejezetten egy különálló
"manifest" vagy index fájlról a személyes fiók archívumában — csak azt mondja el, hogy `tar.gz`,
nagy vonalakban mit tartalmaz, és mekkora lehet. A forrás explicit jelzi: "ez evidence of absence a
dokumentációban, nem feltétlenül evidence of absence magában a termékben."

### 2. Google-fiók (nem csak Takeout) törlési folyamata
**[NEM TALÁLTUK MEG.]** Csak a Takeout oldalát vizsgálták részletesen; a Google saját fióktörlési
felületét (myaccount.google.com) nem kérdezték le. Nem megerősíthető vagy cáfolható, hogy az a
felület technikailag felajánlja-e/megköveteli-e a Takeout futtatását törlés előtt.

### 3. A GDPR hivatalos magyar nyelvű szövege
**[TUDATOS KIHAGYÁS, NEM HIÁNYPÓTLANDÓ.]** A kutatás angol nyelvű EUR-Lex szöveget használt; a
hivatalos magyar változatot nem kérdezték le és nem vetették össze vele. A feladatleírás
megengedte az angol vagy magyar hivatalos szöveg használatát is, formálisan nem hiba.

### 4. A Data Transfer Project tényleges éles használatának mértéke
**[NEM TALÁLTUK MEG.]** A hivatalos DTP-doksi nem közöl számot arra, hány nagy szolgáltató fut
ténylegesen éles DTP-integráción. A Google Data Portability API és a DTP kapcsolata csak
közvetett/valószínűsíthető — a hivatalos Google-oldal szövege nem hivatkozik rá explicit módon, ezt
a kutatás nem is állította tényként.

### 5. "Kötelező export törlés előtt" — általánosabb jogi/szabványossági kontextus
**[TUDATOS HATÓKÖR-SZŰKÍTÉS, NEM HIÁNY.]** Csak a GDPR-t, az ICO guidance-t és a WP242-t vizsgálták
elsődleges forrásként; más joghatóságok (CCPA/CPRA, LGPD) hasonló rendelkezéseit nem nézték át — ez
explicit kívül esett a feladat hatókörén.

### 6. Konkrét termékek (Google, Microsoft, Meta stb.) tényleges "delete gate" mechanizmusa
**[NEM TALÁLTUK MEG — de a vizsgáltak esetében NINCS ILYEN.]** Csak a GitHubot vizsgálták meg
részletesen erre a kérdésre. Nem zárható ki, hogy létezik olyan éles rendszer valahol (pl. belső
vállalati rendszer), amely technikailag tiltja a törlést export nélkül — de a három vizsgált
nyilvános, jól dokumentált rendszer (Google, GitHub, Slack) egyike sem tesz így, és a
jogszabály/EDPB-iránymutatás sem írja elő. Erre a szűkebb, vizsgált körre nézve tehát **[NINCS
ILYEN]** technikai gát.

---

## SQ-04 — Tömeges behozatal indexelt rendszerbe

### 1. npm csomagméret-korlát — nincs hivatalosan dokumentált szám
**[NEM TALÁLTUK MEG — inkább absence of evidence, mint evidence of absence.]** Több célzott keresés
után sem található a docs.npmjs.com hivatalos dokumentációjában számszerű, hivatalosan dokumentált
csomag- vagy tarball-méret-korlát. A forrás szerint: "valószínűsíthető, hogy az npm regisztrinek
van gyakorlati korlátja (közismert anekdotikus információ szerint van ilyen), de ezt hivatalos,
elsődleges forrásból ebben a kutatási körben nem sikerült megerősíteni." Nem használtak fel kitalált
számot.

### 2. Elasticsearch Bulk API — "nem atomikus" explicit kimondása
**[NEM TALÁLTUK MEG — a jelenség maga a válaszstruktúrából levezetett, nem direkt kimondott.]** A
hivatalos Bulk API dokumentáció lekért részleteiben nincs olyan mondat, amely szó szerint kimondaná
"a bulk nem atomikus" vagy "nincs rollback" — ez az `items` tömb dokumentált, elemenkénti
válaszszerkezetéből vezetett következtetés, nem egy direkt idézett kijelentés. Oka lehet, hogy a
WebFetch eszköz csak részben dolgozta fel az oldalt.

### 3. SQLite FTS5 — nincs explicit "bulk loading" ajánlási szakasz
**[NINCS ILYEN.]** A kutatási kérdés feltételezte, hogy van dokumentált tömeges-betöltési ajánlás
automerge/merge paraméterekkel. A hivatalos `sqlite.org/fts5.html` oldal nem tartalmaz ilyen
explicit, összefüggő szakaszt — csak a mechanikát írja le, amelyből egy mérnök levezetheti a
stratégiát, de a dokumentáció ezt nem mondja ki "így tölts be nagy mennyiségű adatot" formában. Ezt
a forrás kifejezett korrekcióként jelöli a kiinduló feltételezéshez képest.

### 4. Séma-validálás és kódolás-validálás importnál
**[NEM TALÁLTUK MEG.]** Nincs elsődleges forrású, névvel ellátott ipari szabvány vagy dokumentált
ajánlás kifejezetten "markdown fájl importjának séma-validálására" vagy "kódolás (UTF-8)
ellenőrzésére import előtt". A kutatás a path traversal (zip slip) és a méret/dekompressziós-bomba
oldalára talált elsődleges forrást, de erre nem. A forrás javasolja: érdemes az SQ-01
(export-formátumok) kutatásban is rákeresni (JSON Schema, frontmatter-validátorok).

### 5. Nincs mért teljesítményadat a "menet közben vs. a végén" indexelésről Bun/SQLite kontextusban
**[NEM TALÁLTUK MEG — implementáció-specifikus mérés, nem dokumentáció-kérdés.]** A kutatás
dokumentációs jellegű volt, nem benchmark-keresés. Ha ez a szám fontos, csak saját prototípus
benchmarkkal zárható le.

### 6. GitHub böngészős feltöltési korlát (25 MiB) — nem közvetlenül idézett mondat
**[GYENGÉBB BIZONYOSSÁG, NEM HIÁNY.]** A 25 MiB szám a WebFetch összefoglalójából származik, nem
közvetlenül a nyers HTML-ből másolt mondatból, és nem található meg egy második, független
forrásban ebben a kutatási körben — ezért alacsonyabb bizonyossággal kezelendő, mint a többi
GitHub-szám (50/100 MiB, <1GB/<5GB), amelyek a fetch-válaszban egyértelmű idézőjeles mondatként
szerepeltek.

### 7. Joplin és más markdown-alapú jegyzetkezelők hivatalos import-dokumentációja
**[NEM TALÁLTUK MEG — nyitva hagyott szál.]** Van egy hivatalos Joplin import/export dokumentációs
oldal, de nem lett lekérve ebben az al-kérdésben (a keresési snippet nem ígért technikai részletet
validálásról/részleges hibakezelésről). Ez a legközelebbi valós analógia a tervezett rendszerhez
(markdown-fájl-alapú jegyzetkezelő tömeges importtal) — érdemes lenne az SQ-01 anyagával
összevetni (ott van Joplin-anyag, de más szempontból).
