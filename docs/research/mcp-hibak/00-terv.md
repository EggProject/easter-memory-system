# Kutatási terv — hibamodell, jogosultság-elutasítás és távoli hitelesítés

Dátum: 2026-09-12 · Vezető: Opus · Keresők: Sonnet, párhuzamosan

## Miért ez a kör

A tulajdonos három dolgot kifogásolt a frissen megírt Spec 40-ben és a D-35-ben:

1. **Ellenőrizni kell**, hogy tényleg nem adhatunk-e vissza saját hibát protokoll-hibaként —
   a vezető állítása szerint adhatunk sajátot, csak az eredmény-objektumban, `isError`-ral.
   Ez teherbíró állítás, adverzariális ellenőrzést kíván.
2. **A jogosultság-hiányra adott üres válasz rossz.** A modell nem tudja megkülönböztetni,
   hogy „nincs ilyen", „nem láthatod" vagy „hiba történt". A „nincs jogod" üzenet szerinte nem
   feltétlenül baj — kell egy általános hibaüzenet-forma.
3. **Ezt nem lehet nyitva hagyni, és beállíthatónak kell lennie** — alap ajánlásokkal.

Plusz: a távoli hitelesítésnél eddig csak a mintát írtuk le, nem azt, hogy pontosan mit kell
megvalósítania egy szabványos erőforrás-szervernek.

## A rendszer

Markdown memória, jogosultság projektenként emberekhez rendelve (D-11). A D-13 eddig azt
mondta: amihez nincs jog, az nem létezik — se találat, se darabszám, se jelzés. Az MCP felület
kizárólag távoli, HTTP-n kiszolgált (D-35/2). Érvényes protokoll-változat: **2026-07-28**.

## Három al-kérdés

- **SQ-01 — A hibamodell adverzariális ellenőrzése.** Igaz-e, hogy a saját üzleti hibáink az
  eredmény-objektumba valók? Próbáld megdönteni.
- **SQ-02 — Jogosultság-elutasítás: mit áruljunk el.** 403 vs 404, a „nem található vagy nem
  hozzáférhető" minta, mit csinálnak a valós rendszerek, és **van-e ajánlott alapérték**.
  Beállíthatóvá teszi-e bárki, és ha igen, mi az alapja?
- **SQ-03 — Mit kell megvalósítania egy szabványos MCP erőforrás-szervernek.**
