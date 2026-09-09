# Önellenőrzés — `kereses-indexeles` kampány

Lezárva: 2026-09-08. Ez a fájl azt írja le, **hol tévedtünk és mit nem tudtunk megerősíteni.**
Olvasd el, mielőtt bármelyik számot használnád.

---

## A legfontosabb: erre a kampányra NEM futott adverzariális ellenőrzési kör

Négy Sonnet kereső dolgozott, mindegyik a saját al-kérdésén, és mindegyik maga jelölte a
forrásait. **Független támadás nem futott az anyagon**, és nincs `allitasok.csv` sem — ez a
kampány al-kérdésenkénti megállapítás-fájlokban tárolja az állításokat, nem soronkénti
állítás-táblában.

Gyakorlati következmény: a tier-jelölés a legerősebb támpont, nem egy ellenőrzési verdikt.
Ahol a `kivonat.md` gyártói mérést idéz, ott az T2 — akkor is, ha hivatalos oldalon áll.

---

## Ami a kutatás során a saját feltevésünket cáfolta

A terv abból indult, hogy a jogosultság-szűrés helye nálunk is nehéz kompromisszum lesz,
mert a szakirodalom drámai recall-összeomlásokat mér. **Ez a feltevés hibás volt.** Az
összeomlás **közelítő (ANN) indexek** tulajdonsága; pontos végigolvasásnál nem létezik. A
kampány legfontosabb eredménye tehát nem egy szám, hanem az, hogy **a probléma fele nem a
miénk** — ezt a `SZINTEZIS.md` 2.1 pontja mondja ki.

---

## Amit nem sikerült megerősíteni, ezért nem használjuk

1. **Nincs hivatalos (T1) SQLite-ajánlás az FTS5 + jogosultsági JOIN mintára.** Az `fts5.html`
   specifikáció szó szerinti keresésre **egyáltalán nem tárgyalja a JOIN-t**. A 170 s → 0,259 s
   `ANALYZE`-adat a hivatalos SQLite fórumból való, tehát **T3** — hiteles, de nem normatív.
   Ezért a döntés az `ANALYZE`-t üzemeltetési kötelezettségként írja elő, nem hivatkozott
   szabályként.
2. **Nincs mért hash-átbocsátás és nincs fordulópont** arra, hány fájlnál válik a teljes
   tartalom-hash vállalhatatlanná. Egyik T1/T2 forrás sem adott ilyet. A kétlépcsős minta ezt
   megkerüli, de a saját korpuszunkon ki kell mérni.
3. **Nincs RRF-fúzió-specifikus forrás a szűrés helyéről.** Minden talált anyag egyetlen lábra
   vonatkozik. Hogy a szűrésnek lábanként vagy az egyesítés után kell-e lennie, azt
   következtetéssel döntöttük el, nem forrásból.
4. **Nincs dokumentált eset arra, hogy automatikus index-javítás élő adatot törölt volna.**
   Csak a fordított hiba van dokumentálva (alul-törlés, FSCrawler #531). Az rclone óvintézkedése
   tehát elvi alapon került a döntésbe, nem egy megtörtént baleset miatt.
5. **A beágyazó kiesésére csak az Elasticsearch mond ki bármit** hivatalosan. Az OpenSearch,
   Vespa, Weaviate, Qdrant, Milvus és Typesense esetében erre a pontos forgatókönyvre nincs
   hivatalos dokumentáció — csak közösségi hibajegyek (T3). Ez érdemi hiány.
6. **Typesense belső törlés-mechanizmusa dokumentálatlan.**
7. **Nincs FTS5-specifikus hivatalos állítás a `bm25()` torzításáról** törölt sorok mellett —
   a `SZINTEZIS.md` erre vonatkozó megállapítása a képletből levezetett következtetés, és más
   rendszerek mért adata támasztja alá, nem az SQLite dokumentációja.

---

## Ellentmondások, amiket nem oldottunk fel, csak rögzítettünk

- **Utószűrés a forrásrendszernél vs. előszűrés a keresőrétegben.** Az AWS biztonsági blogja
  a visszakeresés utáni, forrásrendszer-szintű ellenőrzést ajánlja, mert a keresőindex
  metaadata elavulhat. A domináns iparági minta ezzel szemben a keresőrétegbeli előszűrés.
  **Nálunk a kettő nem zárja ki egymást**: az index eldobható és a fájlból épül, tehát a
  metaadat-elavulás pont az, amit a napi összefésülés kezel.
- **Circuit breaker.** Az AWS Well-Architected ajánlja, az AWS Builders' Library viszont
  „nehezen tesztelhetőnek" nevezi, és helyette helyi token-bucket korlátozást javasol. Két
  hivatalos forrás ugyanattól a cégtől, ellentétes irányba.
- **Tombstone-takarítás.** A Weaviate dokumentációja szerint a takarítás megoldja a
  felhalmozódást; a Ghost Vectors kutatás szerint viszont csak a gráfbejárást javítja, a
  lemez-szintű adatot nem törli garantáltan. **Ez a mi harmadik törlési állapotunkat érinti**,
  és ezért került be a döntésbe, hogy a végleges törlés nem támaszkodhat tombstone-ra.
- **Racy-git.** A git saját dokumentuma szerint az azonos másodpercen belüli módosítás nagy
  repókban ritkán fordul elő; egy 2018-as elemzés szerint a gyors, eseményvezérelt eszközök
  ezt gyakoribbá teszik. A feloldás a terhelés jellegében van: tömeges fabejárásnál ritka,
  egyfájlos gyors műveletnél nem — és nálunk pont mindkettő létezik (napi futás vs. K-01).

---

## Folyamathiba, amit magamnak írok fel

Az **SQ-01-et egyedül indítottam**, a maradék hármat utána egyetlen üzenetben, párhuzamosan.
A szabály az, hogy mind a négy egyszerre menjen. Ez a második ilyen eset — a `kategoria-prompt`
kampánynál az első három ment egyesével.

Emellett egy kérdésfeltevésem félrevezető volt: a törlésre jelölt bejegyzésről szóló
kérdésben úgy fogalmaztam, hogy „visszavonáskor újra bemegy", anélkül hogy megmondtam volna,
mi az a visszavonás. A tulajdonos jogosan kérdezett rá, hogy ezt honnan vettem — a
D-21/5-ből, amit ő maga kért. **A kérdésekben a hivatkozott funkciót meg kell nevezni**, nem
elég rá utalni.
