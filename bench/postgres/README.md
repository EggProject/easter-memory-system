# Postgres-próbák a ParadeDB-re váltáshoz

A `docs/00-dontesek.html` **D-43** döntése és a `docs/90-meresek.html` **18. szakasza** (`#s19`) mögötti saját próbák.
Sima Postgres + `pgvector` kell hozzá — a ParadeDB-specifikus részek (`pg_search` index) itt nem próbálhatók ki,
azokat a `docs/research/paradedb/` kutatás fedi le.

Mért környezet: Ubuntu 24.04 konténer, **PostgreSQL 16.13**, **pgvector 0.6.0**, 2026-09-22.

## Mit próbál ki

| rész | szkript | kérdés | amiért fontos |
|---|---|---|---|
| A | `probak.sh` | A törölt sor tartalma megmarad-e az adatfájlban, a WAL-ban, a `pg_dump` kimenetében, egy nyers fájlmásolatban? | D-36/3: a mentésben ne maradjon nyoma a véglegesen törölt tartalomnak (D-21); D-21/12 |
| B | `probak.sh` | Egy tranzakcióba tett, félúton elhasaló migráció visszagörget-e mindent? | D-37/2: mi marad a mentés szerepe |
| C | `probak.sh` | Pontos (index nélküli) vektorkeresés jogosultsági előszűréssel ugyanazt adja-e, mint a teljes átnézés, és mennyi ideig tart 50 000 × 768 dimenzión? | D-32/2, D-43/6: a jelentés-láb pontos marad |
| D | `probak.sh` | Elrontott táblatartalmat észrevesz-e a `pg_amcheck`, a `pg_dump` és egy `SELECT` — az adatlap-ellenőrzőösszeg nélkül és vele? | D-42: mi a mentés előtti ellenőrzés; D-43/5 |
| E | `mentes-ido.sh` | Mennyi ideig tart a `pg_dump` (tömörítéssel és nélküle), a `pg_restore` és a `pg_amcheck` három méreten? | D-36 és D-37 nyitott pontjai, D-42/4 |

A `probak.sh` az elején kiírja az `autovacuum` beállítását és beépített alapértékét is (D-32/3, D-33/8).

## Futtatás

```
PGBIN=/usr/lib/postgresql/16/bin ./probak.sh
PGBIN=/usr/lib/postgresql/16/bin ./mentes-ido.sh
```

Rootként kell futtatni (a Postgres-fürtöket a `postgres` felhasználóval indítja). Macen nem próbáltuk.
Az E rész egy futása ~5 perc, és több gigabájt átmeneti helyet kér.

## Kimenetek

| fájl | mi |
|---|---|
| `kimenet-a.txt` | `probak.sh`, a nap harmadik futása (a `pg_dump` hibaüzenetét és az autovacuumot még nem rögzítette) |
| `kimenet-b.txt`, `kimenet-c.txt` | `probak.sh`, a bővített szkripttel |
| `kimenet-e1.txt` … `kimenet-e3.txt` | `mentes-ido.sh`; a tömörítés nélküli sor az e2-től van benne |

A nap első két `probak.sh`-futása (egy kézi és egy szkriptes) nincs elmentve; a mérési dokumentum a három elmentett
futás tartományát közli.

## Egy tanulság a szkript írásából

A D) rész első változatából kimaradt az `amcheck` bővítmény telepítése, és a `pg_amcheck` ezért **mindkét
esetben** 1-es kóddal lépett ki. Ez hiányzó előfeltétel volt, nem hibaészlelés. A második futás mutatta meg.
Egy ellenőrző eszköz nem nulla kilépési kódja önmagában nem bizonyítja, hogy sérülést talált.
