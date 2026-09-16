# Kutatási terv — a korai körök újramérése

**Kampány:** `korai-korok-ujra` · **Dátum:** 2026-09-15 · **Keresők:** 3 Sonnet subagent, párhuzamosan

## Miért indult

A 2026-08-20, 08-23 és 09-01-i körök **a mai fegyelem előtt** készültek: van hozzájuk megírt
jegyzet, de **nincs `linkek.md` és nincs `allitasok.csv`** — vagyis nincs URL-lista és nincs
állításonkénti szó szerinti idézet. Minden későbbi kampánynak mind a kettő megvan.

A **D-01…D-10, D-15 és D-16** döntések erre a három körre épülnek.

**Ennek konkrét ára volt.** 2026-09-15-én kiderült, hogy egy ebből a korszakból származó szám
(egy kategóriaszám és egy F1-érték) semmilyen forrásra nem vezethető vissza, és ki kellett venni
a specifikációból. Egy másikat pedig — a Codex 2500 tokenes limitjét — **tévesen kitöröltünk**,
mert nem tudtuk, hol a forrása; utóbb kiderült, hogy megvolt.

**A cél tehát nem új tudás, hanem visszakereshetőség:** ugyanaz a téma, mai fegyelemmel, hogy a
korai döntések ugyanolyan nyomon követhetők legyenek, mint a későbbiek.

**Kikötés a keresőknek:** ne abból induljanak ki, hogy a korábbi eredmény igaz. Ha valami mást
mutat, az értékes eredmény.

## Al-kérdések

| Egység | Amire ment | Mely döntéseket érint |
|---|---|---|
| `sq01` | A fa mint jogosultsági modell, öröklődés, kategóriák száma és elnevezése, útvonal-biztonsági hibaosztályok | D-04, D-08, D-09, D-10 |
| `sq02` | A markdown fájl mint memória-egység, indexelési granularitás, YAML fejléc és csapdái, TOML mint alternatíva | D-03, D-05, D-06 |
| `sq03` | Magyar és többnyelvű beágyazás, brute-force vs. közelítő keresés, SQLite mint vektortár, kliensenkénti integrációs limitek | D-02, D-15, D-16 |

## Kikötések

- **Minden számhoz kötelező a forrás URL-je és a mérés feltétele.** Forrás nélküli szám ebbe a
  kampányba nem kerülhet be — ez az egész kör értelme.
- A `linkek.md` és az `allitasok.csv` **fő termék**, nem melléklet.
- A benchmark-pontszámok élő adatok — a lekérés dátumával együtt.
