# Kutatási terv — skálázás és üzemeltetés

Dátum: 2026-09-05 · Vezető: Opus (fő szál, a szintézist ő írja) · Keresők: Sonnet

## A rendszer, amibe kerül

Bun + TypeScript szerver, egy cég egy telepített példányt használ. A tartalom markdown fájlokban
él egy könyvtárfában, egy gép lemezén. Két SQLite: eldobható keresési index (FTS5 + jelentés-index)
és nem eldobható adat (userek, projektek, jogok), Drizzle ORM-mel. Az audit napló fájl-alapú
(JSON Lines). Minden írás a szerveren megy át. A keresés kapuzott: a jelentés-keresés MINDIG fut,
a szöveges láb csak pontos szóegyezésnél. Docker-ben fog futni.

## A döntés, amit el kell dönteni

**Egy program maradjon, vagy több, egymással kommunikáló alkalmazás legyen?** A tulajdonos
kérdése szó szerint: „mi van ha 100 user egyszerre használja?" — és külön appot képzel el a
karbantartónak és a fájlírásnak.

Az eddigi elemzésem: a szabály nem „egy folyamat", hanem „egy ÍRÓ"; az olvasó oldal zár nélkül
szaporítható; a felső határ egy gép, mert a fájlok és az SQLite egy lemezen vannak. Ehhez kellenek
számok, amiket nem szabad megsaccolni.

## Hat al-kérdés

- **SQ-01** Bun HTTP-kiszolgáló egyidejűsége — mennyi kérést bír egy folyamat, mi korlátozza.
- **SQ-02** SQLite egyidejű olvasók egy gépen — WAL vs rollback, kapcsolatkezelés, blokkolás.
- **SQ-03** Beágyazás-számítás valós költsége kérésenként, CPU-n.
- **SQ-04** Index frissessége íráskor — inkrementális frissítés költsége és mintái.
- **SQ-05** Egy-írós szolgáltatás mint minta + folyamatközi kommunikáció költsége egy gépen.
- **SQ-06** Docker + Bun + SQLite konkrétumai.

## Explicit hatókörön kívül

- Több gépre szétterítés, klaszterezés, replikáció — az alapmodell egy géphez köti.
- Vektoradatbázisok, Postgres — eldöntött tiltás.
- Felület-kinézet, jogosultsági modell, audit napló tartalma.
