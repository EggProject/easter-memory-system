# Hiányok

## Bizonyított hiány (ne keressük tovább — mérni kell)

1. **Batch=1 CPU-késleltetés a szóba jövő beágyazó modellekre** (multilingual-E5, MiniLM, BGE-M3).
   Senki nem publikál ilyet; minden közzétett szám nagy kötegre vonatkozik, ami nem írja le az élő
   lekérdezési utat. → Saját mérés kell.
2. **Magyar nyelvű visszakeresési minőség** ezekre a modellekre: egyik modellkártya sem sorolja fel
   a magyart. → A saját mérésünk (`90-meresek.html`) többet ér itt bármelyik leaderboardnál.
3. **Dokumentált SQLite-korrupciós incidens Docker Desktop macOS fájlmegosztásán**: nem található.
   Az érv architekturális (VM + megosztási réteg), nem incidens-alapú.
4. **Feltételekkel ellátott FTS5 újraépítési / újra-beágyazási benchmark**: nincs.

## Hiányzó bizonyíték (lehetne még keresni)

| Hiány | Fontosság | Mi zárná |
|---|---|---|
| Bun-specifikus TechEmpower rps szám feltételekkel | alacsony | az interaktív dashboard adata; a döntéshez nem kell |
| IPC-mérés nagyobb üzenetméretre (nem 1 bájt) | alacsony | a mért arány (ezredrész) így is elsöprő |
| `Bun.serve({ unix })` szerver-oldali doksi | közepes | ez kell a 2. fázisú szétvágáshoz |
| text-embeddings-inference és llama.cpp-szerver saját konkurencia-doksija | **közepes-magas** | ez dönti el, melyik beágyazó szolgáltatást válasszuk |
| „interface first, transport later" elnevezett gyakorlói forrás | alacsony | az elv Fowler MonolithFirst lábjegyzetéből is levezethető |
| MTEB magyar alcsoport | közepes | de a saját mérés úgyis felülírja |

## Amit a következő körben mérni kell, nem keresni

1. A választott modell batch=1 késleltetése a célgépen, magyar rövid lekérdezésekkel.
2. Hány egyidejű keresésnél romlik el a válaszidő egy Bun folyamaton.
3. A `reusePort` melletti olvasói skálázódás.
4. Egy FTS5 teljes újraépítés ideje a mi korpuszunkon — ez határolja be, mennyire rossz egy
   index-hiba.
