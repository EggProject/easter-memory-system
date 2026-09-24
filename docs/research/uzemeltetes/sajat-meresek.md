# Saját mérések — üzemeltetés

Környezet: Linux 6.18 konténer (Anthropic felhő), `/dev/vda` SSD, **Bun 1.4.0**, **SQLite 3.53.2**
(a `bun:sqlite` beépített SQLite-ja). `PRAGMA journal_mode=WAL`, `synchronous=NORMAL`, lapméret 4096 bájt.
Minden mérés **külön folyamatban** futott, hogy ne legyen folyamaton belüli lapgyorsítótár-átszivárgás.
A „hideg” méréseket `sync` + `echo 3 > /proc/sys/vm/drop_caches` előzte meg.

**Korlát, amit ki kell mondani:** ez egy virtualizált konténer, ahol a gazdagép a vendég alatt is
gyorsítótárazhat. A „hideg” értékek tehát **felső becslések a gyorsítótár hatására**, nem valódi
lemez-hozzáférési idők. Az arányok (VACUUM INTO vs fájlmásolás, quick_check vs integrity_check)
megbízhatóak; az abszolút MB/s értékek gépfüggők.

Tesztadat: `bejegyzes` tábla (útvonal, cím, 2–4 KB magyar szöveg-törzs, időbélyeg) + `beagyazas` tábla
(768 dimenziós float32 BLOB = 3072 bájt/sor), két index a törzsön és egy idegen kulcs index.

---

## 1. `VACUUM INTO` időigénye méret szerint

| adatbázis | bejegyzés | `VACUUM INTO` hideg | `VACUUM INTO` meleg (3 futás) | nyers fájlmásolás meleg | teljes fájl beolvasása meleg |
|---|---|---|---|---|---|
| 44,3 MB | 5 600 | 124 ms | 108 / 106 / 111 ms | 14–16 ms | 24–30 ms |
| 196,3 MB | 24 800 | 464 ms | 443 / 446 / 481 ms | 54–67 ms | 86–101 ms |
| 994,7 MB | 125 600 | 2 342 ms | 2 538 / 2 319 / 2 393 ms | 361–366 ms | 426–496 ms |

**Lineáris a mérettel: ~2,4 ms/MB, azaz ~415 MB/s.** Egy gigabájtos adatbázis mentése ~2,4 másodperc.
A `VACUUM INTO` **6–7-szer lassabb, mint a nyers fájlmásolás** — ez az ára annak, amit cserébe kapunk
(konzisztens pillanatkép + a törölt tartalom kihagyása).

A gyorsítótár állapota alig számít (hideg 464 ms vs meleg 443 ms 196 MB-on), mert a b-fa bejárása
lényegében szekvenciális olvasás, amire az előreolvasás jól működik.

## 2. Integritás-ellenőrzés költsége

| adatbázis | `quick_check` hideg / meleg | `integrity_check` hideg / meleg | `foreign_key_check` hideg / meleg |
|---|---|---|---|
| 44,3 MB | 704 / 29 ms | 681 / 36 ms | 20 / 11 ms |
| 196,3 MB | 2 891 / 104 ms | 3 039 / 135 ms | 91 / 43 ms |
| 994,7 MB | 14 540 / 526 ms | 14 031 / 671 ms | 618 / 222 ms |

Sorrendhatás kizárva: fordított sorrendben, hidegen a 44 MB-os adatbázison `integrity_check` 710 ms,
`quick_check` 665 ms; a 994 MB-oson 15 103 vs 13 476 ms — vagyis a két ellenőrzés hidegen **gyakorlatilag
egyforma**.

**Meleg gyorsítótárral az `integrity_check` 1,2–1,3-szer lassabb a `quick_check`-nél** (nem nagyságrenddel,
ahogy az O(N) vs O(N log N) sugallná). **A gyorsítótár hatása ennél sokkal nagyobb: 20–27×.**

Meleg értékek fajlagosan: `quick_check` ~0,53 ms/MB, `integrity_check` ~0,67 ms/MB.

## 3. A WAL viselkedése mentés közben — kontrollos mérés

Azonos író alfolyamat, azonos 196 MB-os adatbázis, azonos hosszúságú időablak. 3 kontroll + 3 kísérlet.

| futás | WAL az ablak előtt | WAL az ablak alatt | író átbocsátás aránya |
|---|---|---|---|
| KONTROLL #1 (nincs mentés) | 4,0 MB | 4,0 MB | 98% |
| KONTROLL #2 | 4,0 MB | 4,0 MB | 98% |
| KONTROLL #3 | 4,0 MB | 4,0 MB | 108% |
| KÍSÉRLET #1 (`VACUUM INTO` fut) | 4,0 MB | **472,3 MB** | 181% |
| KÍSÉRLET #2 | 4,0 MB | **451,1 MB** | 157% |
| KÍSÉRLET #3 | 4,0 MB | **523,3 MB** | 167% |

A nyugalmi 4,0 MB pontosan a dokumentált `wal_autocheckpoint` alapérték (1000 oldal × 4096 bájt).

A mentés alatt a WAL **113–131-szeresére** nő. Az író eközben **nem lassul, hanem gyorsul** (157–181%),
mert a blokkolt checkpoint miatt nem kell a lapokat visszaírnia a fő adatbázisfájlba — csak a WAL végére
fűz. Ez a dokumentált „checkpoint starvation” működés közben.

**Az író egyetlen `SQLITE_BUSY` hibát sem kapott, és a mentés `integrity_check`-je `ok`.**

## 4. A felfújt WAL visszanyerése

| lépés | WAL mérete |
|---|---|
| írás közben, mentés előtt | 4,1 MB |
| közvetlenül a `VACUUM INTO` (817 ms) után | 111,1 MB |
| 2 mp tétlenség után, a kapcsolat nyitva | 111,1 MB |
| `wal_checkpoint(PASSIVE)` → `{busy:0, log:28281, checkpointed:28281}` | 111,1 MB |
| `wal_checkpoint(TRUNCATE)` → `{busy:0, log:0, checkpointed:0}` | **0,0 MB** |
| az író leállítása után | 0,0 MB |

A `PASSIVE` checkpoint mind a 28 281 keretet visszamásolta, de **a fájlt nem zsugorította**.
Csak a `TRUNCATE` vitte vissza — és ehhez **nem kellett a szolgáltatást újraindítani**.

## 5. Pillanatkép-határ: mi kerül a mentésbe?

Konkurens író mellett indított `VACUUM INTO`: az indulás pillanatában az író ~767 750 sornál tartott,
a végén ~1 085 375-nél; a mentésben **816 250** konkurens sor van. A mintavételezés 400 ms-os, ami
~137 000 sor/mp mellett ~55 000 sor bizonytalanság — vagyis a mentés tartalma a **VACUUM INTO indulási
állapotával** egyezik a mérési hibán belül, nem a végállapottal.

**A mentés közben írt adat nem kerül bele.** A mentés `integrity_check`-je `ok`.

## 6. Hibaesetek (`VACUUM INTO`)

| eset | eredmény |
|---|---|
| létező célfájlra | `HIBA — output file already exists` |
| nem létező könyvtárba | `HIBA — unable to open database: …` |
| nyitott tranzakción belül | `HIBA — cannot VACUUM from within a transaction` |
| forrás `journal_mode` | `wal` |
| **mentés `journal_mode`** | **`delete`** — a WAL-beállítás nem öröklődik |

A `journal_mode` nem-öröklődése a mérésből derült ki; az ELL03 megerősítette, hogy a hivatalos
dokumentáció **hallgat** erről (a `page_size`, `auto_vacuum`, `user_version`, `application_id`
öröklődése viszont forráskódból igazolható). Visszaállításnál tehát a WAL-módot **külön be kell állítani**.

## 7. Törölt tartalom a mentésben

20 MB-os adatbázisba beírtunk egy jelölő karakterláncot, majd töröltük a sorát, és `wal_checkpoint(TRUNCATE)`-et
futtattunk.

| | a jelölő nyers bájtszinten |
|---|---|
| forrásfájl a törlés előtt | MEGVAN |
| forrásfájl a törlés **után** | **MEGVAN** (a lap nincs felülírva) |
| nyers fájlmásolat (`cp`) | **MEGVAN** — a törölt tartalom átkerült |
| `VACUUM INTO` kimenet | **NINCS** |

Ez a D-36 gerincét adó tulajdonság, most már két oldalról igazolva: a hivatalos dokumentáció mondja
(ELL03: IGAZOLVA, szó szerint), és mi is megmértük.

## 8. FTS5 szerkezeti módosíthatósága (a D-37/5-höz)

Külön futtatás, ugyanezen a Bun/SQLite páron:

| művelet virtuális táblán | eredmény |
|---|---|
| `ALTER TABLE … ADD COLUMN` | `HIBA — virtual tables may not be altered` |
| `ALTER TABLE … DROP COLUMN` | `HIBA — cannot drop column from virtual table` |
| `ALTER TABLE … RENAME COLUMN` | `HIBA — cannot rename columns of virtual table` |
| `ALTER TABLE … RENAME TO` | **SIKERÜLT** |
| tokenizáló megváltoztatása `ALTER`-rel | `HIBA — near "SET": syntax error` (nincs ilyen szintaxis) |
| `INSERT INTO t(t) VALUES('rebuild')` | SIKERÜLT |
| `INSERT INTO t(t) VALUES('integrity-check')` | SIKERÜLT |
| `DROP` + `CREATE VIRTUAL TABLE … tokenize='trigram'` + `rebuild` | SIKERÜLT; a részszó-keresés (`szerz`) 100 sort adott |
| trigger létrehozása után, `rebuild` **előtt** | 0 találat |
| ugyanaz `rebuild` **után** | 50 találat |

A D-37/5 eddig a dokumentáció hallgatásából levezetett állítás volt. **Mostantól mérés.**
