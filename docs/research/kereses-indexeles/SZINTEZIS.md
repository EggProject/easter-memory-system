# Szintézis — keresés és indexelés

Kampány: `kereses-indexeles` · Lezárva: 2026-09-08 · A szintézist a vezető (Opus) írta,
a kereséseket négy Sonnet ügynök végezte.

> Ez a fájl a **következtetéseket** mondja ki. A forrásokat és az idézeteket a `kivonat.md`
> tartalmazza. Ami itt számként szerepel, annak ott van a forrása.

---

## 1. A kérdés

A `30-kereses.html` 2026-08-21-én íródott, a D-02 alapján, „részleges" jelöléssel. Azóta
tizenkét döntés született, amiket nem ismer: a három gyökér, a jogosultsági modell, az
„amihez nincs jog, az nem létezik", a friss írás azonnali kereshetősége, a három törlési
állapot, a leválasztott beágyazó konténer.

A dokumentum saját nyitott listájából négy kérdés maradt élő, és ezekhez kellett kutatás.

---

## 2. A négy megállapítás

### 2.1 A jogosultság-szűrés dilemmája nálunk nem létezik

A szakirodalom ezen a ponton fájdalmas számokat ad. A Qdrant saját mérésében módosítatlan
HNSW-gráfon, 1%-os szelektivitású szűrőnél a recall **0,1%-ra** zuhan. A pgvector 0.8.0-nál
az AWS mérése szerint naiv utószűréssel a recall **10%-ra, illetve 1%-ra** esett — iteratív
bejárással 100%-ra javult.

**De mindkét szám közelítő (ANN) indexek problémája.** Egy közelítő index azért gyors, mert
nem néz meg mindent; ha a szűrő kivágja a gráf nagy részét, a bejárás elakad. Ha viszont a
jelentés-láb **pontos végigolvasás** a jogosult halmazon — egy cég, egy gép, egy szerver-
folyamat (D-16) —, akkor nincs gráf, amit el lehetne rontani: az előszűrés ingyen van, és a
recall definíció szerint pontos.

Ez a kampány legfontosabb felismerése: **a mi méretünk eltünteti a problémát, ami a
szakirodalom fele.**

A megerősítés az irányra: mind a nyolc megvizsgált rendszer (Elasticsearch, OpenSearch,
Qdrant, Weaviate, Milvus, Typesense, Meilisearch) a szűrést a lekérdezésbe ágyazva,
előszűrésként valósítja meg. Egyik sem futtat különálló utószűrő réteget.

### 2.2 Két FTS5-csapda, ami üzemeltetési kötelezettséggé válik

- A `MATCH` operátor **nem működik JOIN-aliasszal**. A szöveges találatot alkérdésben kell
  előállítani, és arra jön a jogosultsági JOIN. Ez nem stílus kérdése, hanem az egyetlen
  működő alak.
- Az FTS5 **statikus költségbecslést** ad a lekérdezés-tervezőnek, és ez JOIN-nál rossz tervet
  eredményez. Egy dokumentált esetben `ANALYZE` lefuttatása után ugyanaz a lekérdezés
  **170 másodpercről 0,259 másodpercre** gyorsult — nagyságrendileg 656-szoros különbség.

A második ebből **telepítési és karbantartási kötelezettség**: az `ANALYZE`-nak le kell futnia,
és nem egyszer, hanem az adatmennyiség érdemi változásakor. Enélkül a rendszer nem lassú lesz,
hanem használhatatlan — és semmi nem jelzi, mert a lekérdezés helyes eredményt ad.

### 2.3 A darabszám és a pontszám szivárog — ezt ki kell mondani

Az Elasticsearch hivatalos dokumentációja a dokumentum-szintű biztonságnál **kimondja**, hogy
az aggregáció és a relevancia-pontszám (a globális IDF-statisztikán keresztül) árulkodhat olyan
dokumentumokról, amiket a kérdező nem láthat.

Ez a D-13-at érinti: „amihez nincs jog, az nem létezik — se találat, se szám, se jelzés."

**Amit vállalhatunk:** nincs találat, nincs darabszám, nincs „további N rejtett" felirat. Ezt
az előszűrés maradéktalanul teljesíti.

**Amit nem vállalhatunk közös indexben:** hogy egy látható találat pontszáma soha ne
függjön a nem látható tartalomtól. A BM25 a korpusz egészének statisztikájából számol.

A tiszta megoldás projektenként külön index lenne — de az sok kis index, drágább karbantartás,
és a közös tudás minden kereséskor külön láb. **Egy cégen belüli rendszernél ez az ár nem éri
meg**, viszont az ígéretet pontosan kell fogalmazni: a tartalom nem szivárog, a statisztika
elvben igen.

### 2.4 A beágyazó kiesésénél a kapu már megválaszolta a kérdést

A hibrid és a csak-BM25 keresés különbsége **erősen feladatfüggő**: az Elastic BEIR-alapú
mérésében 18% (RRF) – 24% (súlyozott) nDCG@10 különbség, egy 2026-os pénzügyi paperben viszont
csak 6,5%. Ugyanakkor a BEIR maga dokumentálja, hogy **a BM25 több feladaton veri a sűrű
visszakeresést** — és a gyakorlati bukási esetek is nevesítettek: hibakód, azonosító,
függvénynév, ritka entitás. Ott a szöveges láb a jobb.

Ez pontosan a **kapu** kérdése (D-02): előfordul-e a kérdés minden szava együtt egy
dokumentumban? Ha igen, a kérdező pontos dolgot keres — és a szöveges láb önmagában is
értékes. Ha nem, átfogalmazott a kérdés, és a szöveges láb a kapu saját érvelése szerint zaj.

**Tehát nem kell új szabály: a meglévő kapu megmondja, mikor van értelme a fél keresésnek.**
Nyitott kapunál kiszolgáljuk, csonkának jelölve. Zárt kapunál nem zajt adunk, hanem hibát.

Az iparági minta ezt támogatja: az Elasticsearch hiányzó inference endpointnál **fail-fast** —
mind az indexelés, mind a szemantikus lekérdezés elbukik. A Vespának van igazi
`coverage.degraded` mezője, de az sem erre az esetre való. **„X-Degraded" fejléc-konvenció
sehol nem létezik** — a jelzésnek a válasz tartalmában kell lennie.

### 2.5 A törlésre jelöltet ki kell venni az indexből

Három egymást erősítő ok:

- **Szivárgás.** Bent hagyva a jelölt bejegyzés beleszámít a statisztikákba, tehát a látható
  találatok pontszámát is befolyásolja — pont az a csatorna, amit az Elasticsearch
  dokumentációja szivárgásként megnevez.
- **Ár.** A tombstone-ok felhalmozódása mérhetően drága: az Elastic saját blogja szerint
  50%-os töröltaránynál **18–46%-os lassulás**, és a term-statisztikák a merge pillanatában
  ugranak a valós értékükhöz, megváltoztatva a pontszámokat.
- **A visszavonás olcsó.** A szöveg a fájlban megvan (a fájl az igazságforrás), a beágyazás
  újraszámolása a mért adatok szerint néhány ezredmásodperc rövid szövegre. Nincs miért
  bent tartani.

**Egy lelet, ami a D-21 harmadik állapotát érinti.** A Ghost Vectors paper szerint puha törlés
után a nyers vektor tipikusan **fizikailag a lemezen marad** (Weaviate, ChromaDB). Nálunk ez
nem végzetes, mert az index eldobható — de következik belőle egy szabály: **a végleges törlés
soha nem támaszkodhat egy tombstone-ra.** A fájl törlése után az indexből célzottan ki kell
venni, és ha kétség van, újraépíteni.

### 2.6 Az összefésülésnek van neve, formája és bevett gyakorisága

- Az **mtime önmagában szerkezetileg elégtelen**: a git saját `racy-git` dokumentuma, a
  BorgBackup, az NFS kézikönyvlap és egy restic hibajegy egymástól függetlenül igazolja.
  Konkrét bukási módok: másodperc-granularitás, a `touch`/`utimes(2)` bármit beállíthat,
  óracsúszás, fuse fájlrendszerek, amik egyáltalán nem állítanak mtime-ot. És a
  legalattomosabb: egy csomagkezelő visszaállítja a tartalmat, de meghagyja a régi mtime-ot.
- A bevett minta **kétlépcsős**: olcsó metaadat-összevetés (méret + mtime) az egész fán, és
  tartalom-hash **csak a gyanús fájlokra**. Ez az rsync „quick check" vs `--checksum`
  párosa és a git „racily clean" visszaesése.
- A mintának neve van — **reconciliation / anti-entropy** —, és minden megtalált konkrét
  rendszer **naponta vagy ritkábban** futtatja, soha nem gyakrabban. Az Atlassian
  index-öngyógyítása hajnali 1-kor fut naponta, és pontosan azt a három kategóriát
  különbözteti meg, ami nekünk is kell: **árva index-bejegyzés, index nélküli fájl, elavult
  bejegyzés.**
- **Amit szabad automatikusan javítani**: az Atlassian a jól körülhatárolt eseteket javítja,
  de ha az összkép „egészségtelen", megáll és **kézi teljes újraindexelést kér**. Az rclone
  szabálya még élesebb: *„Files in the destination won't be deleted if there were any errors
  at any point."*
- **Az FTS5-nek nincs részleges javító eszköze.** Az `integrity-check` csak `rank=1` mellett
  veti össze a külső tartalom-táblával; a `rebuild` mindig az **egész** indexet építi újra.
  A részleges javítás tehát a mi rétegünkben történik, célzott törlés + újrabeszúrással.

---

## 3. A négy döntés

| # | Kérdés | Döntés |
|---|---|---|
| 1 | Hol szűr a jogosultság | **Előszűrés mindkét lábban.** Szöveges: alkérdés + JOIN, kötelező `ANALYZE`. Jelentés: pontos végigolvasás a jogosult halmazon. |
| 2 | Ha a beágyazó nem elérhető | **A kapu dönt.** Nyitottnál a szöveges láb kiszolgál, a válaszban csonkának jelölve. Zártnál világos hiba — nem zaj. |
| 3 | Törlésre jelölt az indexben | **Kikerül** mindkét indexből. Visszavonáskor visszakerül: szöveg a fájlból, beágyazás újraszámolva. |
| 4 | Mit javít a napi futás | **Jól körülhatárolt eseteket, hibátlan futásnál.** Bármilyen hiba esetén nem töröl. Sok eltérésnél megáll és kézi újraindexelést kér. |

---

## 4. Amit a `90-meresek.html`-be be kell írni

- HNSW recall 1%-os szelektivitású szűrőnél, módosítatlan gráfon: **0,1%** (gyártói mérés)
- pgvector naiv utószűrés recall: **10%, illetve 1%**; iteratív bejárással **100%** (gyártói mérés)
- FTS5 + JOIN `ANALYZE` előtt/után: **170 s → 0,259 s**
- SQLite `quick_check` **O(N)** vs `integrity_check` **O(N log N)**
- Hibrid vs csak-BM25 nDCG@10 különbség: **18% (RRF) – 24% (súlyozott)** egy mérésben,
  **6,5%** egy másikban — a szórás maga az adat
- Töröltarány 50% → **18–46%** lassulás (gyártói blog)
- HNSW: fizikai törlésnél a recall stabil (~0,81 SIFT1B), logikai törlésnél romlik ismételt
  frissítésekkel
- Takarítási küszöbök más rendszerekben: Qdrant `deleted_threshold=0.2` +
  `vacuum_min_vector_number=1000`; Weaviate 300 s; Elasticsearch 12 h
- Recoll bejárási mérés: 18 000 PDF / 30 GB — **11 perc 40 mp SSD**, **24 perc 40 mp NFS**

**Nyitott mérés:** nincs megbízható adat a hash-átbocsátásra és arra, hány fájlnál válik a
teljes tartalom-hash vállalhatatlanná. A kétlépcsős minta ezt megkerüli, de a fordulópontot
a saját korpuszunkon kell kimérni.
