# Kutatási kivonatok

Itt élnek az easter-memory-system kutatásainak **kivonatai**. Nem a letöltött nyersanyag — az a
konténerben marad és elmúlik —, hanem az, ami hat hónap múlva is számít: **mit állítottunk, mire
alapoztuk, és hol találjuk vissza a forrást.**

Miért van ez a repóban: egy kutatás akkor ér valamit, ha később meg lehet nézni, mire alapoztunk
egy döntést. A beszélgetés elmúlik, ez marad.

## Kampányok

| Mappa | Mikor | Miről szól | Forrás | Állítás | Kivonat |
|---|---|---|---|---|---|
| `router-rangsor/` | 2026-09-01 | Router-ötlet és a találatok rangsorolása | 47 | 69 | 2 182 szó |
| `szerver-technika/` | 2026-09-05 | Írási sorbaállítás, Better Auth, Drizzle+FTS5, audit napló | 122 | 223 | 3 820 szó |
| `skalazas/` | 2026-09-05 | Egy app vagy több; Bun, SQLite, beágyazás, Docker | 67 | 105 | 2 830 szó |
| `kategoria-prompt/` | 2026-09-06 | A kategória-választó prompt token-költségvetése | 71 | 149 | 7 202 szó |
| `import-export/` | 2026-09-06 | Csereformátum, ütközéskezelés, adathordozhatóság, tömeges behozatal | 80 | 89 | 5 459 szó |
| `memoriabol/` | 2026-08-20 … | Korábbi körök jegyzetei, a projektmemóriából átmásolva | | | |

## Mit találsz egy kampány mappájában

- **`kivonat.md` — itt kezdd.** Ez a megírt kivonat: egy ügynök elolvasta a mentett forrásokat, és
  megírta, mit mondanak — **szó szerinti idézetekkel**, a számokhoz odatéve a feltételeiket
  (milyen hardveren, milyen egyidejűséggel, milyen tokenizálóval mérték), és külön megjelölve, amit
  az ellenőrzés gyengített. **Ez a fájl a törölt oldal-pillanatképek helyett áll**: úgy készült,
  hogy nélkülük is érthető legyen.
- **`SZINTEZIS.md`** — a kampány saját összefoglalója. A `kivonat.md` ez alatt egy réteggel
  dolgozik: az a forrásokat idézi, ez a következtetéseket mondja ki.
- **`linkek.md`** — **minden meglátogatott és felderített link.** Az archivált források tierrel és
  élő/halott állapottal; alattuk azok, amiket a keresők láttak, de nem nyitottak meg — egy későbbi
  kör onnan folytathatja.
- **`allitasok.csv`** — minden állítás, szó szerinti idézettel és forrásazonosítóval.
- **`keresesek.md`** — minden lefuttatott lekérdezés szó szerint, tehát a kutatás megismételhető.
  A végén a nem elérhető domainek.
- `hianyok.md` — amit **nem** sikerült megtudni, és hogy az „nincs ilyen" vagy „nem találtuk meg".
- `ellentmondasok.md` — ahol a források egymásnak ellentmondanak, és mi a feloldás.
- `QA.md` — a kampány önellenőrzése: hány állítás dőlt meg, hol tévedtünk.
- `00-terv.md` — a kutatási terv, al-kérdésekkel.

## Amit tudni kell

- **A forrás-pillanatképek nincsenek itt.** Tudatos csere: a teljes anyag 17 MB és 1 653 fájl volt,
  a kivonat fél megabájt. A helyükre három dolog került: a `kivonat.md` kiírja a lényegi mondatokat
  szó szerint, a `linkek.md`-ből megvan, mi volt a forrás, az `allitasok.csv`-ben pedig minden
  állítás idézete. Ha egy hivatkozás elrothad, ennyiből rekonstruálható, mire alapoztunk.
- **A megbízhatósági jelölés szigorú.** A `Magas` két független elsődleges forrást kíván. A
  `szerver-technika` tárban **egyetlen** ilyen van, a `skalazas`-ban 66 — ez nem szigor-különbség,
  hanem a korpuszok természete: az egyik hibajegyekre és fórumokra épült, a másik specifikációkra.
- **A `router-rangsor`, a `kategoria-prompt` és az `import-export` kampányon NEM futott
  adverzariális ellenőrzési kör.** A `router-rangsor` `allitasok.csv`-jében a verdikt-oszlop
  üres. A `kategoria-prompt`-nál és az `import-export`-nál a keresők a saját fő állításaikat
  ellenőrizték — kétszeri, eltérő lekéréssel, illetve a jogszabály-idézeteket a mentett
  pillanatképekkel összevetve —, de független támadás egyiken sem futott. Mindhárom számait
  óvatosabban kell kezelni, mint a `szerver-technika` és a `skalazas` tárét; mindegyik `QA.md`
  kiírja, mi dőlt meg és mit nem sikerült megerősíteni.
- **A `QA.md`-t érdemes elolvasni**, mielőtt bármelyik számot használnád. Ott van kiírva, hol
  tévedtek a kutatók és hol tévedtem én.

## `memoriabol/`

A 2026-08-20, 08-23 és 09-01-i körök jegyzetei, amikor még nem készült strukturált tár. **A
2026-09-01-i adverzariális ellenőrzéssel kezdd**, ha régi számot akarsz használni: az első két kör
több állítása megdőlt vagy pontosításra szorult, és az ellenőrzés kiírja a védhető megfogalmazásukat.
