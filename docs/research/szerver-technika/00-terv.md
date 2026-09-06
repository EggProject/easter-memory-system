# Kutatási terv — szerver-oldali technikai kérdések

Dátum: 2026-09-01 · Vezető: Opus (fő szál, a szintézist ő írja) · Keresők: Sonnet

## A rendszer, amibe kerül

Bun + TypeScript szerver, két SQLite adatbázis (egy eldobható keresési index, egy nem eldobható
adat: felhasználók, projektek, jogok, audit), Drizzle ORM, Better Auth. A tartalom markdown
fájlokban él egy könyvtárfában. Minden írás a szerveren megy át — nincs közvetlen fájlhozzáférés.
Egy cég egy telepített szervert használ, több felhasználóval és több projekttel.

## Három téma, nyolc al-kérdés

**A) Írási sorbaállítás** (SQ-01…SQ-03) — hogyan biztosítjuk, hogy egy markdown fájlt egyszerre
tényleg egy folyamat írjon. Már eldöntött: minden írás viszi az olvasott tartalom lenyomatát, és
eltérésnél megáll. Ez viszont az ütközést ÉSZLELI, nem előzi meg.

**B) Better Auth és Drizzle** (SQ-04…SQ-05) — beépíthető-e a saját projekt-jogosultság a Better
Auth ellenőrzésébe; és hogyan viszonyul a Drizzle az FTS5 virtuális táblákhoz.

**C) Audit napló tárolása** (SQ-06…SQ-08) — hogyan tároljuk hatékonyan, hogy ne legyen többgigás
fájl, és olvasásra is jó legyen (két nézet: teljes rendszer és egy felhasználó).

## Explicit hatókörön kívül

- Vektoradatbázisok, beágyazó modellek — eldöntött kérdések.
- Elosztott rendszerek, több szerver, klaszterezés — egy szerver van.
- Felület-kinézet.
- Több-bérlős izoláció.
