# Szintézis — szóköz nélküli írásrendszerek (CJK)

**Kampány:** `cjk` · 2026-09-12 · 1 kereső, 29 forrás · A döntés: **Spec 30, 09. szakasz**

Ez a fájl a következtetéseket mondja ki. A forrásokat és a szó szerinti idézeteket a
`megallapitasok.md` tartalmazza.

---

## A döntés

**Nem építünk CJK-tokenizálót.** Nem kapcsoljuk be a `trigram` tokenizálót, nem lépünk vissza
FTS3/4-re az ICU kedvéért, és nem hozunk be szótár-alapú szegmentálót.

---

## Az öt megállapítás, amin a döntés áll

### 1. Az ICU-út FTS5-ben egyszerűen nincs

Az SQLite dokumentációja az FTS5/FTS3-összehasonlításban szó szerint kimondja: *„The ICU
tokenizer is not available."* Az ICU-tokenizáló csak a régebbi FTS3/4 modulban létezik, ott is
fordítási opcióként (`SQLITE_ENABLE_ICU`), C-s ICU-könyvtár-függőséggel. Két út marad:
visszalépni egy régebbi modulra, vagy saját FTS5-tokenizálót írni C-ben, ami maga hívja az ICU
`BreakIterator`-t. Hivatalos `fts5_icu` modult a kutatás nem talált.

**Az ár aránytalan** ahhoz képest, amit kapnánk: a dokumentáció maga nevezi az ICU-tokenizálót
*„very simple"*-nek — csak szóhatárt keres, nem végez morfológiai elemzést.

### 2. A trigram nem ingyen van, és nincs hozzá szám

A `trigram` az FTS5 egyetlen nyelvfüggetlen megoldása, de három dolgot hoz magával:

- **Átnyúlik a szóhatárokon.** A dokumentáció saját példája szerint a szóköz beleszámít a
  hármasba. Ez ellentétes a PostgreSQL `pg_trgm`-jével, ami kifejezetten kizárja a
  nem-alfanumerikus karaktereket. Aki a kettőt azonosnak hiszi, téved.
- **Háromnál rövidebb keresés soha nem talál.** Ez CJK-n különösen fáj, ahol egy-két karakteres
  keresőkifejezés gyakori.
- **Az indexméret-szorzóra nincs hivatalos szám.** A talált közösségi mérések 1,85× és 18,3×
  között szórnak, és a szórás oka ismert (természetes szöveg vs. strukturált, ismétlődő adat).
  Egy tervezési dokumentum ezt nem idézheti mértékadó adatként.

**Következtetés:** ilyen kapcsolót nem lehet megalapozottan bekapcsolni, csak saját korpuszon
kimérve. Amíg nincs CJK-tartalom a rendszerben, nincs min mérni.

### 3. A lexikai keresés CJK-n akkor is gyenge, ha megoldjuk a tokenizálást

Ez a legfontosabb megállapítás, és ez fordítja meg a kérdést.

A BGE-M3 cikk (ACL Findings 2024, lektorált) MIRACL-mérésén a **tiszta BM25** japánra **31,2**,
koreaira **37,1** nDCG@10-et ér el. Ugyanezen a mérésen a BGE-M3 japánra **75,2**, koreaira
**72,2**. A különbség nem árnyalatnyi: **kétszeres**.

Vagyis a tokenizálás megoldása nem egy gyenge lábból erőset csinálna, hanem egy nem létezőből
gyengét. A munka javát CJK-n a beágyazás végzi — ami nálunk amúgy is a fő láb (D-02).

**A BM25-kontroll a modell szerzőitől független adat**: nem a saját modelljük dicsérete, hanem
egy szabványos kontroll ugyanazon a benchmarkon.

### 4. Nincs egyetlen helyes megoldás — ez önálló tervezési terület

Aki megoldotta, mind mást választott, és ezek egymásnak ellentmondó tervezési döntések:

| Ki | Mit csinál |
|---|---|
| Lucene-alapú motorok (`cjk` analizátor) | nyelv-agnosztikus **bigram** (2-gram), nem trigram |
| Elasticsearch `smartcn` | valószínűségi szegmentálás kínaira, kevert kínai-angol szöveget is kezel |
| Elasticsearch `kuromoji` / `nori` | **szótár-alapú** morfológiai elemzés (a koreai szótár nyers mérete 219 MB) |
| PostgreSQL `pg_trgm` | alapból **kizárja** a nem-alfanumerikus karaktereket — ezért jött létre külön a `pg_bigm` (2-gram) |

Még az OpenSearch saját dokumentációja is elismeri, hogy a beépített `cjk` analizátor nem a
legjobb választás (*„You may find that the `icu_analyzer` … works better"*). **Ez nem egy
kapcsoló, hanem egy önálló tervezési terület**, saját mérésekkel és karbantartási terheléssel.

### 5. Amiről nincs adat, pedig kellene

Arra, hogy a `trigram` tokenizáló mennyivel rontaná a **magyar** BM25-relevanciát az
alapértelmezett `unicode61`-hez képest, **nincs mérés**. A legközelebbi forrás (McNamee &
Mayfield, karakter-n-gram európai nyelvekre) más n-értékre, más nyelvekre és más metrikára
vonatkozik, és a teljes szövege fizetőfal mögött van.

Ez azt jelenti, hogy egy „kapcsoljuk be mindenkinél" megoldás **ismeretlen mértékben rontaná a
mostani keresést** egy olyan nyelvi esetért cserébe, amire nincs felhasználónk.

---

## Amit a döntés kockáztat — kimondva

**CJK tartalmon a beágyazó kiesése teljes keresés-kiesést jelent.** Latin írású tartalomnál a
Spec 30 06-os szakasza szerint a szöveges láb megmarad tartaléknak, és a kapu közli, hogy csak az
fut. CJK-nál ez a tartalék nincs meg.

**Ez viszont nem új mechanizmust igényel.** A már meglévő kapu (D-32/5) helyesen kezeli ezt az
esetet is, mert nem hazudik teljességet: ha a szöveges láb üresen tér vissza, a válasz „most
nincs keresés", nem „ennyit találtam". A **viselkedés** tehát változatlan; a **hatás** más, és
ezt a Spec 30 kiírja, mielőtt valaki CJK tartalmat tölt a rendszerbe.

## Ha később mégis kell

A belépési pont a szöveges láb tokenizálója, ami a **D-34** szerint az illesztő mögött van,
tehát **egy helyen cserélhető**. A sorrend akkor: (1) mérés saját korpuszon indexméretre és
magyar relevancia-romlásra, (2) bigram vagy trigram választása a mérés alapján, (3) az illesztő
mögötti csere. Addig nem tartunk fenn kapcsolót, amit senki nem mért meg.
