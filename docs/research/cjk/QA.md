# Önellenőrzés — `cjk` kampány

## Ami előzte: egy hibás feltevés

Ez a kampány **hibajavításként** indult. Amikor a CJK-kérdés felmerült, azt javasoltam, hogy ne
foglalkozzunk vele — abból kiindulva, hogy a rendszert magyarul fogják használni. A felhasználó
ezt visszautasította: *„nem ertem mi koze barminek a magyar nyelvhez? mondtam neked barmikor hogy
mindig csak magyarok fogjak hasznalni?"*

**Igaza volt.** Sosem mondta ezt. A javaslatot visszavontam, és a kérdést kutatással válaszoltuk
meg. A végeredmény ugyanaz lett („ne építsünk CJK-tokenizálót"), de **más okból**: nem azért,
mert nincs CJK-felhasználó, hanem mert a lexikai keresés CJK-n mérés szerint akkor is gyenge, ha
megoldjuk a tokenizálást — és mert a tokenizáló-váltás ára ismeretlen a magyar keresésre nézve.

**A tanulság nem az, hogy a válasz jó lett.** Az, hogy egy ki nem mondott feltevésre építettem
ajánlást, és ha a felhasználó nem kérdez vissza, az bekerül a specifikációba indoklás nélkül.

## Folyamat

| Amit a szabály előír | Betartva? |
|---|---|
| Webes keresést Sonnet subagent végzi | **igen** |
| `deep-web-research` skill használata | **igen** |
| Párhuzamos indítás | **n. a.** — egy al-kérdés volt, egy kereső |
| A szintézis és a döntés Opusé | **igen** — `SZINTEZIS.md` |
| Minden szám a mérési dokumentumba kerül | **igen** — 90-meresek, 13. szakasz |

## Amit a kutatás megdöntött vagy gyengített

1. **„A trigram a megoldás CJK-ra."** Részben igaz, de a Lucene-alapú motorok és a `pg_bigm`
   egyaránt **bigramot** használnak, nem trigramot — és a `trigram`-nál a háromnál rövidebb
   keresés soha nem talál, ami CJK-n gyakori eset. A „kézenfekvő" megoldás nem az, amit mások
   választottak.

2. **„Az ICU a rendes út."** FTS5-ben nem létezik. Ez nem ár-kérdés, hanem elérhetőség-kérdés —
   az SQLite dokumentációja szó szerint kimondja.

3. **„Van egy indexméret-szorzó, amit idézhetünk."** Nincs. 1,85× és 18,3× között szór, és
   hivatalos szám nem létezik. Amit a specifikációba írni lehet, az a **szórás maga**.

## Ami nyitva maradt

- Nincs mért adat a `trigram` hatására a **magyar** BM25-relevanciára. A legközelebbi forrás
  (McNamee & Mayfield) fizetőfal mögött van, és más n-értékre vonatkozik. **Ez a kampány
  legnagyobb hiánya**, és ez indokolja, hogy ne szállítsunk bekapcsolható kapcsolót.
- Nincs friss, hivatalos ICU4C méretadat — az egyetlen hivatalos lap ~15 éve nem frissült.
  Nem számít, mert az ICU-út FTS5-ben amúgy sem járható.

## Forráshűség

A `sqlite.org`, `postgresql.org`, `elastic.co` és `opensearch.org` lapjait **nyers `curl`-lal**
kértük le, nem a WebFetch összefoglalóján keresztül. Ez nem óvatoskodás volt: az OpenSearch
CJK-lapja és több GitHub README kliens-oldalon töltődik, és a WebFetch hiányos tartalmat adott
vissza. Ha ezt nem ellenőrizzük, a szakasz egy része nem létező idézetekre épült volna.
