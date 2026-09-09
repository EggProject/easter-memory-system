# Kutatási terv — keresés és indexelés (a 30-kereses.html frissítéséhez)

Dátum: 2026-09-08 · Vezető: Opus (a szintézist ő írja) · Keresők: Sonnet, párhuzamosan

## Miért ez a kör

A `30-kereses.html` 2026-08-21-én íródott, a D-02 alapján, és „részleges" jelöléssel áll.
Azóta tizenkét döntés született, amiket nem ismer. A dokumentum saját „Ami még nyitva van"
listájának egy része azóta eldőlt, más része viszont máig nyitott — és pont azokhoz kell
kutatás.

## Amit már tudunk, NE kutassátok újra

- **Rangsorolás és egyesítés** (`router-rangsor` kampány): az RRF képlet, a 60-as csillapító,
  a helyezés-alapú egyesítés. Ez áll, nem kell hozzá új anyag.
- **FTS5 + Drizzle mechanika** (`szerver-technika` kampány): virtuális tábla kézzel írt
  migrációban, öt árnyéktábla a kizáró listán, paraméterezett lekérdezés, `bm25()` növekvő
  sorrend, automerge/crisismerge.
- **Bun/SQLite/beágyazás teljesítmény** (`skalazas` kampány): a szinkron illesztő, a
  folyamathatár ~1/1000 egy beágyazás árához képest, a granite mérések, a macOS FTS5 hiba.
- **Kategória-prompt költségvetés** (`kategoria-prompt` kampány).

## Négy al-kérdés

- **SQ-01 — Jogosultság-szűrés helye a hibrid keresésben.** Előszűrés vagy utószűrés? A D-13
  szerint amihez nincs jog, az nem létezik: se találat, se szám, se jelzés. Ez kizárja-e az
  utószűrést? Mit csinálnak a valós rendszerek, és mi ennek a mért ára?
- **SQ-02 — Index és lemez elcsúszásának észlelése és javítása (K-01, K-02).** Miből derül ki,
  hogy az index már nem egyezik a lemezzel? Mit ellenőriz egy napi konzisztencia-futás, mit
  szabad automatikusan javítani, és mit csak jelenteni?
- **SQ-03 — Mi történjen, ha a beágyazó nem elérhető lekérdezéskor?** A hibrid keresés egyik
  lába kiesik. Milyen viselkedések léteznek, és van-e mért adat arról, mennyit romlik a
  találati minőség csak a szöveges lábbal?
- **SQ-04 — Törlésre jelölt bejegyzés az indexben.** A D-21 szerint a jelölt bejegyzés azonnal
  kikerül a keresésből, de akinek joga van, annak látszik. Kivegyük az indexből, vagy
  lekérdezéskor szűrjük? Mit mondanak a források a két útról FTS5-ben és vektoros keresésben?

## Hatókörön kívül

- A rangsorolás képlete és a kapu logikája — ezek állnak.
- Modellválasztás, beágyazó modell cseréje.
- A felület (60-felulet.html) és az MCP szerződés — külön körök.
