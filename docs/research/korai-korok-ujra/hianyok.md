# Hiányok — korai-korok-ujra



---

# sq01 — A fa mint jogosultsági modell, és a kategóriák

# Hiányok — amit nem sikerült kideríteni (sq01 újramérés)

A módszertani mandátum szerint minden hiányt explicit dokumentálni kell, ahelyett
hogy hallgatólagosan kimaradna. Az alábbi lista alkérdésenként rendezve mutatja,
mit nem sikerült forrással alátámasztani, és — ahol lehet — miért (hiányzó
bizonyíték vs. a bizonyított hiány ténye).

## SQ-01 — Útvonal mint jogosultsági modell

- **Basic Memory hozzáférés-vezérlési nyilatkozat hiánya.** A Basic Memory hivatalos
  MCP Tools Reference oldala (`docs.basicmemory.com`) a "projekteket" különálló,
  nevesített munkaterületekként írja le, de az oldalon **nem található semmilyen
  hozzáférés-vezérlési vagy jogosultsági nyelvezet** (nincs "permission", "access
  control", "security boundary" szó vagy ezzel egyenértékű állítás). Ez önmagában
  nem idézhető állításként (nem lehet "forrás azt mondja, hogy nincs X" formában
  idézni egy hiányt), ezért ez itt saját, jelölt következtetésként szerepel, nem
  `allitasok.csv` sorként: **a Basic Memory dokumentációja a vizsgált oldalon nem
  tesz kijelentést arról, hogy a projekt/mappa-struktúra biztonsági határ volna
  vagy sem — a kérdés ezen a forráson nyitva marad.** Ez evidence of absence
  helyett inkább absence of evidence: lehet, hogy más (nem vizsgált) Basic Memory
  oldalakon van ilyen nyilatkozat, ezt nem zártuk ki teljeskörűen.
- **AWS `${aws:username}` policy-változó konkrét példája.** Az S3 hozzáférés-
  szabályozásról szóló elsődleges walkthrough-oldalon kerestük az IAM
  policy-változók (pl. `${aws:username}` mappa-per-felhasználó mintázat) konkrét
  példáját; a kifejezetten erre szolgáló másik AWS-oldalon
  (`amazon-s3-policy-keys.html`) sem találtuk meg pontosan ebben a formában.
  Ez inkább keresési lefedettségi hiány, mint bizonyított hiány — az AWS
  dokumentációja nagy terjedelmű, elképzelhető, hogy más oldalon szerepel.

## SQ-02 — Valódi többbérlős izoláció

- Nincs kritikus hiány; mindhárom vizsgált rendszer (Kubernetes, Vault, S3)
  hivatalos, elsődleges dokumentációval alátámasztott.

## SQ-03 — Öröklődés a fában

- **macOS/APFS ACL-öröklés hivatalos dokumentációja.** Csak Linux (POSIX ACL,
  man7.org) és Windows (NTFS, Microsoft Learn) hivatalos forrást találtunk az
  öröklés irányára/visszavonhatatlanságára. macOS-re nem kerestünk és nem
  találtunk elsődleges Apple-dokumentációt — ez explicit ki lett zárva az
  időkeret miatt, nem azért, mert nincs ilyen dokumentáció.

## SQ-04 — Kategóriák száma

- **Nincs egyetlen, minden rendszerre nézve konszenzusos "ideális szám".**
  A talált három megközelítés (PARA = pontosan 4; Johnny.Decimal = legfeljebb 10x10;
  Zettelkasten = 0, szándékosan nincs előre definiált kategória) egymással
  ellentmondó ajánlásokat ad — ez maga az eredmény, nem hiány, de fontos
  hangsúlyozni: **nincs olyan forrás, ami azt állítaná, hogy létezik egy
  tudományosan levezetett "helyes" kategóriaszám mappa-alapú rendszerekhez.**
  Lásd `ellentmondasok.md`.
- Nem találtunk semmilyen forrást arra, hogy az öt tervezett kategória
  (`decisions/mistakes/procedures/facts/preferences`) mint *fajta* (nem téma)
  szerinti felosztás bárhol elő lenne írva vagy mérve — ez a konkrét
  kategorizálási elv (episztemikus típus szerinti, nem téma szerinti mappázás)
  egyik vizsgált forrásban sem szerepel explicit módon.

## SQ-05 — Kategóriaszám és besorolási pontosság

- **Nincs olyan lektorált vagy nem lektorált forrás, ami kifejezetten
  markdown-fájlrendszerbeli mappa-választást (mint klasszifikációs feladatot)
  mérne.** A két talált mérés (Scientific Reports: intent-osztályozás kis
  modelleken; arXiv Haystack-to-Needle: zero-shot szöveg-klasszifikáció nagy
  modelleken) mindkettő *szöveg-klasszifikációs* feladat, nem *fájlrendszer-
  navigációs/mappaválasztási* feladat. Az átvitel (kategóriaszám → mappaszám)
  analógiás, nem közvetlenül mért. Ezt a `megallapitasok.md` is explicit jelzi.
- Az arXiv Haystack-to-Needle tanulmány (T4, nem lektorált) esetében nem
  találtunk független, lektorált megerősítést ugyanazokra a konkrét
  F1-javulási százalékokra (7.0% / 5.1% / 4.9% / 3.3%) — ezek egyetlen,
  nem lektorált forrásból származnak. Ez explicit "Alacsony" megbízhatósági
  jelölést kapott az `allitasok.csv`-ben.

## SQ-06 — Mappanév minősége

- **Nem található kifejezetten mappanevekre (folder naming) vonatkozó, LLM-
  ügynök-alapú fájlkeresési/navigációs mérés.** A talált két forrás kód-
  *azonosítókra* (változó-, függvénynevek) vonatkozik: Lawrie et al. 2007
  (ember alanyok, nem LLM) és a 2025-ös "When Names Disappear" (LLM-ek, de
  kódazonosítók, nem mappa/fájlnevek). Egyetlen forrást sem találtunk, ami
  kifejezetten mappa- vagy fájlnév-leíróképesség és LLM-alapú "megtalálom-e a
  helyes mappát" pontosság közötti összefüggést mérné.
- **Dátum-alapú elnevezési konvenciók hatása.** Egyik forrás sem vizsgálta
  kifejezetten a dátum-alapú (pl. `2026-09-15-döntés.md`) elnevezést a leíró
  vagy rövidítéses elnevezéssel szemben. Ez teljes hiány (nem találtunk
  releváns mérést), nem csak keresési lefedettségi rés — több kereséssel (ld.
  `keresesek.md`, SQ-06 blokk) sem került elő ilyen tanulmány.

## SQ-07 — Útvonal-biztonsági hibaosztályok

- Mind a négy kért hibaosztályra (naiv prefix-illesztés, symlink, Unicode-
  normalizáció, névütközés) találtunk konkrét, azonosítóval ellátott CVE-t,
  ezért itt nincs érdemi hiány. Egy apró pontatlanság: a CVE-2025-54387 NVD-
  leírása nem nevezi meg explicit a CWE-22-t, ez a GitHub Security Advisory
  (GHSA-mm3p-j368-7jcr) szövegéből derül ki — ezt jelöltük a forrásjegyzetben.

## Általános / módszertani hiány

- **Nincs alkérdésenkénti Sonnet-verifikáló szubágens-lefedettség.** A skill
  előírása szerint a Phase 5 verifikációt külön Sonnet szubágenseknek kellene
  végezniük az evidence table-ön. Ebben a környezetben nem állt rendelkezésre
  Agent/szubágens-dispatch eszköz (ellenőrizve `ToolSearch`-csel), ezért a
  degradált módot alkalmaztuk: ugyanaz a munkamenet végezte a keresést és az
  önellenőrzést is. Kompenzációként minden számot tartalmazó vagy "Magas"
  bizalmi szintre jelölt állítást élő URL-ellenőrzéssel (curl/WebFetch
  újralekérés) és — ahol volt rá mód — nyers HTML-ből való `grep`-es
  idézet-visszakereséssel ellenőriztünk, de ez nem helyettesíti a modell-
  szintű függetlenséget, amit a skill design-ja megkövetelne. Ez maga is egy
  dokumentált hiány, nem csak egy lábjegyzet.



---

# sq02 — A markdown fájl mint memória-egység, és a fejléc

# Hiányok — sq02

Amit ebben a kutatási körben **nem** sikerült megbízhatóan megtudni, forrással alátámasztani, vagy amit csak részlegesen sikerült lezárni. A cél, hogy egy jövőbeli kör pontosan tudja, hol kell folytatnia — nem "csendben kihagyni" a hiányt.

## H1. Konkrét számszerű ajánlás a frontmatter mezők számára (SQ-03)

Egyik vizsgált hivatalos forrásban (Obsidian, Jekyll, Hugo) sem található kimondott, számszerű ajánlás arra, hogy "N mező felett már sok". Az Obsidian dokumentációja csak minőségi elvet fogalmaz meg ("small, atomic bits of information"), az SSW.com.au stíluskalauz (T3, nem hivatalos) is csak azt mondja, hogy kerülni kell a "felesleges komplexitást", szám nélkül. **Ez hiány marad** — ha a döntéshez (pl. D-03/D-05/D-06) szükséges egy konkrét szám, azt nem lehet ebből a forrásanyagból levezetni; vagy a "négy mező" (tags, modified, prompt_version, format_version) döntést más elven kell indokolni (pl. a konkrét felhasználási eset elemzésével), nem egy általános iparági ajánlással.

## H2. Zettlr és Dendron frontmatter-mezői elsődleges forrásból

A WebSearch talált releváns hivatalos oldalakat (`docs.zettlr.com/en/editor/yaml-frontmatter.html`, `wiki.dendron.so`), de idő/keret hiányában ezeket nem dolgoztuk fel elsődleges forrásból, nyers curl-lekéréssel. Ezek a `linkek.md` "Felderített, de nem megnyitott" szakaszában szerepelnek, mint következő körre ajánlott lépés.

## H3. A "Norway problem" kifejezés pontos eredete

Sikerült dokumentálni egy dátumozott, jól idézhető **népszerűsítési pontot** (Bram.us, 2022-01-11, egy 2022-01-10-i tweetre hivatkozva), de nem sikerült megállapítani, hogy a kifejezést ki és mikor használta *elsőként* — lehet, hogy a közösségben (yaml-core levelezőlista, korábbi fórumbejegyzések) korábban is létezett informálisan. Ez a kutatási kör csak ennyit tud állítani: *legkésőbb 2022 januárjában már elterjedt, dokumentált fogalom volt*; korábbi eredetről nincs megbízható adatunk.

## H4. Notion export — cím elhelyezése markdown exportban

A hivatalos Notion súgóoldal (`notion.com/help/export-your-content`) leírja az exportálás *folyamatát*, de nem specifikálja a keletkező markdown fájl belső szerkezetét (pl. hogy a lap címe H1-ként a törzsben, a fájlnévben, vagy esetleg egyáltalán nem ismétlődik-e meg a tartalomban). Ez konkrét hiány marad SQ-07 szempontjából; a kérdés megválaszolásához egy tényleges exportfájlt kellene megvizsgálni (amihez Notion-fiók és teszttartalom szükséges — ez ennek a kutatási körnek a keretein kívül esik).

## H5. Obsidian saját fact-szintű indexelése / gráf nézet granularitása

Erősen valószínű (közismert termékviselkedés alapján), hogy az Obsidian beépített Gráf nézete és keresése **jegyzet-szinten** (fájl-szinten) működik, nem tény-szinten — de ezt ebben a körben nem sikerült egy konkrét, elsődleges Obsidian-dokumentum idézetével alátámasztani (a `Search.md` és `Graph view.md` súgóoldalak URL-találgatása 404-et adott, a helyes elérési utat nem találtuk meg az időkereten belül). A `megallapitasok.md`-ben ezt az állítást ezért **nem** T1 idézettel, hanem "T2/köztudott, de ebben a körben nem igazolt elsődleges forrással" jelöléssel szerepeltetjük — ezt tekintsük résznek, amit egy következő kör lezárhat.

## H6. Chunk-méret ipari "ökölszabályok" (pl. "512 token") eredete

A feladat kifejezetten kérte a gyártói marketing-torzítás jelzését. Több gyakorlati blogbejegyzés (Pinecone, LangChain, Weaviate stb.) hivatkozik "jellemző" chunk-méret ökölszabályokra (pl. néhány száz token), de ebben a körben **nem találtunk kontrollált méréssel alátámasztott, elsődleges forrást** ezekre a konkrét számokra — csak a Dense X Retrieval (EMNLP 2024, T2) eredményét sikerült szilárdan lehorgonyozni mérési feltételekkel együtt (lásd A20–A23). Ez azt jelenti: **a chunk-méret téma nagy része valóban erősen gyártói-marketing vezérelt, ahogy a feladat feltételezte**, és a kutatás ezt nem cáfolta, csak egyetlen szigetszerű, valóban lektorált kivételt talált (a propozíció-alapú granularitás kérdésében).

## H7. mem0 "How Mem0 Works" hivatalos áttekintő oldala

A `docs.mem0.ai/core-concepts/how-mem0-works` URL 404-et adott (feltehetően megváltozott az elérési út egy dokumentáció-átszervezés miatt). A mem0 architektúráját ezért a `graph-memory` és a `vectordbs/overview` aloldalakból, valamint a GitHub README-ből rekonstruáltuk — ezek elegendőek voltak a fő állítások (alapértelmezett vektortár = Qdrant, natív gráfréteg) alátámasztásához, de egy teljes, egységes "hogyan működik" hivatkozást nem sikerült találni ebben a körben.

## H8. Letta "core memory" (memory blocks) formátuma

SQ-01 megválaszolásához elsősorban az "archival memory" (vektor-DB, tény-szintű) oldalt dolgoztuk fel. A Letta másik memória-mechanizmusát, a "core memory"/"memory blocks"-ot (amely a kontextusablakba rögzített, szerkeszthető szövegblokk, nem adatbázisban tárolt tény) nem dolgoztuk fel részletesen elsődleges forrásból ebben a körben — ez nem befolyásolja az SQ-01 fő következtetését (Letta = vektor-DB a tény-szintű tárolóhoz), de a Letta teljes memória-architektúrájának árnyaltabb leírásához hiányzik.



---

# sq03 — Beágyazás magyarra/többnyelvűre, és az integrációs felületek

# Hiányok — sq03

Amit nem sikerült megtudni, vagy amit a hivatalos/publikált források maguk sem közölnek. A feladat kifejezetten kéri, hogy a hiányokat is írjuk meg — ezek nem kudarcok, hanem eredmények.

## 1. Snowball magyar tövező — nincs elérhető, konkrét mérés

A magyar Snowball-tövező mögötti tudományos hivatkozás (Tordai & de Rijke, "Four Stemmers and a Funeral: Stemming in Hungarian at CLEF 2005", DOI 10.1007/11878773_20) **létezik és azonosítható**, de a tényleges tartalmát ebben a kutatási körben **nem sikerült elérni**:
- Springer (`link.springer.com`) — fizetőfal mögött.
- ResearchGate — 403 "Temporarily Unavailable" (bot-védelem).
- A szerzők eredeti forrásoldala (ILPS, Amsterdami Egyetem, `ilps.science.uva.nl`) — DNS-hiba, a domain valószínűleg megszűnt (~20 éves egyetemi erőforrás).
- Semantic Scholar API — megerősíti a tanulmány létezését és metaadatait, de az absztraktot "CLOSED" hozzáférésűnek jelzi, nem közli.

**Következmény:** nem tudjuk megmondani, mekkora (ha van egyáltalán) mérhető IR-teljesítmény-változást okoz a Snowball magyar tövező alkalmazása magyar szóalakokon. A kampány saját, "bizonyítottan ront" jellegű állítása (Spec 30) emiatt **jelenleg nem visszavezethető** egyetlen konkrét számhoz sem — sem a mi kutatásunkból, sem a kampány saját belső dokumentumaiból.

## 2. Multilingual vs. monolingual — nincs standard, nagy léptékű, hivatalos gyártói mérés magyarra

Nem találtunk olyan publikált mérést (pl. a `multilingual-e5`, `BGE-M3` vagy hasonló modell hivatalos technikai riportjában), amely kifejezetten egy nagy, kereskedelmi többnyelvű modellt egy **azonos paraméterszámú, kizárólag magyarra tanított** modellel vetne össze, és egyetlen %-os javulási számban összegezné az eredményt. A Multilingual E5 technikai riport (arXiv 2402.05672) egyáltalán nem tartalmaz monolingual-összehasonlítást (nulla találat a "monolingual" szóra). Amit találtunk (Antal Margit 2025, Hatvani & Yang 2024), az kisebb léptékű, akadémiai, magyar nyelvű kutatás — értékesek, de nem "hivatalos gyártói ajánlás" szintű bizonyíték.

## 3. Brute-force keresés felső határa — nincs egyetlen hivatalos "N vektor" szám

Sem az SQLite/sqlite-vec, sem a pgvector, sem a FAISS hivatalos dokumentációja nem ad egyetlen konkrét vektorszámot, amitől kezdve a brute-force/exact keresés már nem ésszerű. A FAISS a leginformatívabb, de ott is a döntés a lekérdezésszám és a RAM-korlát függvénye, nem egy önmagában álló vektorszám. Az egyetlen konkrét (idő+memória) adatpontunk egy nem lektorált magánblog egyetlen futtatásából származik (T3, ~14 millió vektor becsülve, nem közvetlenül megadva) — ez nem tekinthető megbízható, általánosítható referenciaértéknek.

## 4. Bináris kvantálás pontosságromlása — nincs hivatalos, sqlite-vec-specifikus szám

A sqlite-vec saját dokumentációjában van egy "## Benchmarks" alcím a bináris és skalár kvantálási útmutatókban is — **mindkettő üresen áll**, tartalom nélkül. Vagyis a projekt maga is jelezte a szándékát egy ilyen mérés közlésére, de **jelenleg nem publikálta**. A konkrét recall-számokat (0,9445–0,9966) egy másik termékről (Qdrant) vettük, ami nem feltétlenül reprezentatív a sqlite-vec saját implementációjára.

## 5. Wayback Machine / archive.org nem elérhető ebben a környezetben

Minden kísérlet a `web.archive.org` és `archive.org` elérésére (a CDX API-n, az `available` API-n és a `WebFetch` eszközön keresztül egyaránt) sikertelen volt: a `curl`-hívások megszakadtak ("Connection reset by peer"), a `WebFetch` pedig `SITE_BLOCKED` hibát adott vissza. Ez konkrétan megakadályozta, hogy pontosan megállapítsuk, **mikor** frissült a Claude Code hivatalos hook-dokumentációja a 10 000 karakteres korlát bevezetésével (l. `ellentmondasok.md` 1. pont) — csak azt tudjuk, hogy 2026-09-01-én (a kampány ellenőrzése szerint) még nem volt ott, 2026-09-15-én (a mi ellenőrzésünk szerint) már ott van.

## 6. GitHub API és GitHub kódkeresés nem elérhető ebben a környezetben

Az `api.github.com` és a `github.com/search` végpontok ebben a proxykörnyezetben egy Claude Code GitHub Actions-specifikus hibaüzenetet adnak vissza, nem a valódi GitHub-választ. Emiatt nem tudtuk pontosan megkeresni pl. a `mteb` Python-csomag forráskódjában az egyes taszkok definícióját (pl. melyik konkrét Python-fájlban van a `HunSum2AbstractiveRetrieval` osztály). Ezt megkerültük a Hugging Face API-n és a nyers `mteb/results` parquet-adatbázison keresztül, ami végül **jobb, elsődleges forrásnak** bizonyult (közvetlen eredmény-adat, nem kódmeghatározás), de a hiányt dokumentáljuk.

## 7. Antigravity kliens — nem vizsgáltuk újra ma

Az Antigravity kliens (nincs `SessionStart`-szerű hookja, helyette állítólag `PreInvocation`, 12 000 karakteres szabály-limittel) a kampány saját belső mérésében szerepel, de a feladat listája (Claude Code, Codex, Gemini CLI, Cursor "és ami még releváns") ezt nem emelte ki kötelező elemként, és időkorlát miatt nem futtattunk rá ma önálló, hivatalos-forrású ellenőrzést. Ezt a számot tehát **nem erősítettük meg és nem is cáfoltuk** — a `megallapitasok.md` táblázatában "nem ellenőriztük ma újra" jelöléssel szerepel.

## 8. MCP kliens-képesség mátrix — csak "hallgatás", nem minden esetben explicit tábla

A Cursor esetében explicit, kizáró táblázatot találtunk (Sampling hiányzik egy kimerítőnek szánt listából) — ez erős bizonyíték. Claude Code, Gemini CLI és Codex esetében viszont csak azt tudjuk mondani, hogy a "sampling" szó nem fordul elő a hivatalos dokumentációban — ez **hallgatás**, nem explicit kizárás, és gyengébb bizonyíték arra, hogy a képesség ténylegesen nincs implementálva (elképzelhető, hogy support van, csak nincs dokumentálva). Ezt a különbséget a `megallapitasok.md`-ben és az `allitasok.csv` megbízhatósági oszlopában külön jelöltük.
