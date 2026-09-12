# Kutatási terv — adatbázis-illesztő (a D-34 megalapozásához)

Dátum: 2026-09-09 · Vezető: Opus (a szintézist ő írja) · Keresők: Sonnet, párhuzamosan

## Miért ez a kör

A tulajdonos kimondta: az adatbázist **illesztő vagy más illesztési programozási mintát
használva** kell megoldani, mert később más adatbázis-típusokat is be akar vezetni, és azoknál
nem fognak kelleni az itt felfedezett SQLite-specifikus fogások.

A D-34 első változata **kutatás nélkül** íródott — ez hiba volt, és ez a kampány javítja.
Ráadásul tartalmazott egy tárgyi tévedést: az „egy írós" korlátot alkalmazás-szintű
feltevésként írta le, holott az **SQLite tulajdonsága**, tehát pont az illesztő dolga elnyelni.
(A D-07 fájlonkénti írási sora ettől független alrendszer: markdown fájlok lemezre írása,
nem adatbázis.)

## A rendszer, amihez a mintát keressük

- Két tár: egy **eldobható keresési index** (SQLite FTS5 szöveges index + beágyazás-vektorok)
  és egy **nem eldobható adattár** (felhasználók, projektek, jogok) — Drizzle-lel, a
  bejelentkezés Better Authtal.
- Egy gépen, két konténerben fut; egy szerverfolyamat.
- Az itt felfedezett SQLite-specifikus fogások, amiket el kell szigetelni: a `MATCH` nem megy
  JOIN-aliasszal; `ANALYZE` nélkül nagyságrendekkel lassabb a JOIN-os lekérdezés; a Drizzle
  séma-feltolásnak kizáró listára van szüksége az FTS5 öt árnyéktáblájával; macOS-en a
  rendszer-SQLite FTS5 hibája.
- A keresés hibrid: szöveges + jelentés-láb, **helyezés-alapú** egyesítéssel (RRF).
- A jogosultsági előszűrés ma azért ingyenes, mert a jelentés-láb **pontos végigolvasás**.

## Négy al-kérdés

- **SQ-01 — Melyik minta, és hol van a varrat.** Ports & Adapters, Repository, DAO, Data
  Mapper, Gateway: mit mondanak az elsődleges források, és mik a dokumentált bukásaik?
- **SQ-02 — Párhuzamosság és tranzakciók motorok között.** Hogyan fejezhető ki az atomiság és
  a sorosítás motor-függetlenül? Mit nyel el a Unit of Work? Mi az, amit tényleg nem lehet
  elrejteni? **Ez a legfontosabb kérdés ebben a körben.**
- **SQ-03 — Szöveges és vektoros keresés hordozható felület mögött.** Mi tér el motoronként, és
  sikerült-e bárkinek jól absztrahálnia?
- **SQ-04 — Hogyan tartható őszinte egy illesztő.** Szerződés-tesztek, közös tesztkészletek —
  és van-e bizonyíték arra, hogy az „egy megvalósítás + port" megközelítés megtérül-e.

## Hatókörön kívül

- Konkrét ORM kiválasztása (a Drizzle a D-12-vel eldőlt).
- A keresés algoritmusa (D-02, D-32) — csak a felület alakja érdekel.
