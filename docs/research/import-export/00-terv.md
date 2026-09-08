# Kutatási terv — import és export

Dátum: 2026-09-06 · Vezető: Opus (a szintézist ő írja) · Keresők: Sonnet, párhuzamosan

## A kérdés, ahogy a tulajdonos feltette (K-03)

Kell import és export. **Amit el kell dönteni:** milyen formátum, mi a hatóköre (egész fa, egy
projekt, egy kategória, egy ember személyes mappája), mit csinál ütközésnél, és mit visz magával
a verziókból, az indexből és a jogosultságokból.

**Az export nem kényelmi funkció:** a D-24 szerint felhasználót törölni csak úgy lehet, hogy
előtte lefut egy export a személyes mappájáról. Vagyis az export a felhasználó-kezelés
előfeltétele.

Az import a D-20/1 következménye is: ha a felület nem hoz létre bejegyzést, kell egy tömeges út
a kezdeti feltöltéshez és a közös tudás behozatalához.

## A rendszer korlátai, amiket a kutatásnak tiszteletben kell tartania

- A tartalom **markdown fájl**, három gyökér alatt: `projects/`, `knowledge/`, `personal/<email>/`
- A fejlécben pontosan három mező: `tags`, `modified`, `prompt_version` (D-06)
- Verziók vannak, és a **végleges törléskor eltűnnek** (D-21/6) — ez a git elvetésének oka
- Az index **eldobható**, a fájlból épül újra (D-19)
- A jogosultság a **projekté**, és az útvonalból jön (D-04, D-11)
- Nincs vektoradatbázis, nincs Postgres; SQLite index van
- **Csak beágyazó modell fut, szöveggeneráló nincs**

## Négy al-kérdés

- **SQ-01** Milyen formátumban exportálnak markdown-alapú tudástárak, és mit tesznek a metaadattal.
- **SQ-02** Ütközéskezelés importnál: milyen stratégiák léteznek, és melyik okoz kevesebb kárt.
- **SQ-03** Személyes adat exportja: mit ír elő a hordozhatóság, és mit tartalmaz egy ilyen csomag.
- **SQ-04** Tömeges behozatal indexelt rendszerbe: validálás, részleges hiba, újraindíthatóság.

## Hatókörön kívül

- A felület rajza (az a döntés után jön)
- Migráció más konkrét termékből (nem tudjuk, honnan jön majd az anyag)
- Titkosítás és tömörítési algoritmusok részletei
