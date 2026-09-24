# Üzemeltetési mérések

A `docs/90-meresek.html` **17. szakaszának** mérései. Mindegyik szkript önálló, csak `bun:sqlite` kell hozzá.
A munkafájlok az `adat/` alkönyvtárba kerülnek, és a szkriptek a végén törlik őket.

Mért környezet: **Bun 1.4.0, SQLite 3.53.2** (a `bun:sqlite` beépített SQLite-ja), Linux konténer.
Első futás: 2026-09-16. Második, független futás egy újraindított konténeren: 2026-09-22.

## Mi mit mér

| szkript | mit mér | a 17. szakasz melyik táblája |
|---|---|---|
| `futtat-meret.sh` | `VACUUM INTO`, nyers fájlmásolás, `quick_check`, `integrity_check`, `foreign_key_check` — 50 / 200 / 1000 MB, hidegen és melegen, minden mérés külön folyamatban | mentés ideje · integritás-ellenőrzés ára |
| `wal-kontroll.ts` | ugyanaz az író mentés nélkül (3×) és `VACUUM INTO` alatt (3×): a WAL mérete és az író átbocsátása | a WAL a mentés alatt |
| `wal-visszanyeres.ts` | a felfújt WAL-t visszanyeri-e a `PASSIVE`, illetve a `TRUNCATE` checkpoint, újraindítás nélkül | a felfújt WAL visszanyerése |
| `pillanatkep.ts` | konkurens író mellett a mentés az indulási vagy a végső állapotot őrzi-e | a pillanatkép határa |
| `hibaesetek.ts` | a `VACUUM INTO` hibaesetei, és mely beállítások öröklődnek a kimenetre (nem alapértelmezett értékekkel) | hibaesetek |
| `torolt-tartalom.ts` | a törölt sor tartalma megmarad-e nyers bájtszinten a forrásban, a fájlmásolatban és a `VACUUM INTO` kimenetében | törölt tartalom |
| `fts5-szerkezet.ts` | módosítható-e utólag egy FTS5 tábla szerkezete, és feltölt-e visszamenőleg egy trigger | FTS5 szerkezeti korlátai |
| `futtat-index.sh` | az index újraépítése a fájlfából: 1 000 / 10 000 / 50 000 fájl, 1 KB és 4 KB törzs, fázisonként | az index újraépítése |
| `ekezet-teszt.ts` | hogyan kezeli a `unicode61` tokenizáló a magyar ékezeteket, a `remove_diacritics` beállítás szerint | — (megfigyelés) |

Segédszkriptek: `epit.ts` (szintetikus adatbázis), `meres.ts` (egy mérés, saját folyamatban),
`iro.ts` és `tetlen.ts` (konkurens írók), `gen-fa.ts` (szintetikus markdown fa), `ujraepit.ts` (egy újraépítés).

## Futtatás

```
BUN=bun ./futtat-meret.sh
BUN=bun ./futtat-index.sh
bun wal-kontroll.ts
bun wal-visszanyeres.ts
bun pillanatkep.ts
bun hibaesetek.ts
bun torolt-tartalom.ts
bun fts5-szerkezet.ts
bun ekezet-teszt.ts
```

A „hideg" mérés (`sync` + `drop_caches`) **csak Linuxon, rootként** fut; macOS-en a szkript „meleg*" jelöléssel
futtatja ugyanazt. A konténerben a gazdagép a vendég alatt is gyorsítótárazhat, ezért a hideg értékek
felső becslések a gyorsítótár hatására. **Az arányok megbízhatóak, az abszolút számok gépfüggők.**

## Egy megjegyzés az `fts5-szerkezet.ts`-ről

Az eredeti, 2026-09-15-i szkript egy konténer-újraindításkor elveszett, csak a kimenete maradt meg.
Ez a változat a rögzített kimenet alapján készült újra, ugyanazokkal a lépésekkel és nevekkel.
**A 2026-09-22-i futása soronként megegyezik az eredeti kimenettel.**
