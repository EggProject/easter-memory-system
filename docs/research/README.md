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
| `kereses-indexeles/` | 2026-09-08 | Jogosultság-szűrés, index-elcsúszás, beágyazó kiesése, törölt bejegyzés az indexben | 132 | — | 7 703 szó |
| `adatbazis-illeszto/` | 2026-09-09 | Illesztési minták, párhuzamosság motorok között, hordozható keresés, szerződés-tesztek | ~115 | — | 8 728 szó |
| `mcp-felulet/` | 2026-09-12 | MCP specifikáció, modellbarát eszközfelület, létező memória-szerverek, azonosítás | 114 | — | 6 775 szó |
| `mcp-hibak/` | 2026-09-12 | Hibamodell (adverzariálisan ellenőrizve), jogosultság-elutasítás, MCP erőforrás-szerver követelményei | 60+ | — | megállapítások al-kérdésenként |
| `cjk/` | 2026-09-12 | Szóköz nélküli írásrendszerek a szöveges keresésben: FTS5 tokenizálók, ICU, trigram-ár, mások megoldásai | 29 | — | megállapítások al-kérdésenként |
| `mentes-frissites/` | 2026-09-12 | Mentés, helyreállítás, séma- és formátum-migráció; a mentés mint cserélhető komponens | 272 | — | 33 277 szó |
| `tartalom-kapu/` | 2026-09-15 | Mi kerülhet be a memóriába: titokfelismerés, memory poisoning, determinisztikus szűrés | 60+ | — | **döntés előtt** |
| `korai-korok-ujra/` | 2026-09-15 | A 2026-08-20/23-i körök újramérése mai fegyelemmel — a D-01…D-10, D-15, D-16 forrásolása | 70+ | **161** | 160 forrásolt állítás |
| `uzemeltetes/` | 2026-09-16 | Monitorozás, állapotellenőrzés, üzemeltetési napló, indulás/összeomlás, SQLite-egészség, riasztás — 3 ellenőrző körrel és saját mérésekkel | 221 | — | 32 977 szó + mérések |
| `ertesites/` | 2026-09-16 | Helyi asztali értesítés háttérszolgáltatásból (macOS/Linux), és hogyan jeleznek a mentőeszközök elmaradt mentést — adverzariális ellenőrző körrel | 161 | — | 16 545 szó |
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
- **Az adverzariális ellenőrzési kör a `szerver-technika`, a `skalazas` és az `mcp-hibak`
  kampányon futott le.** A `router-rangsor`, `kategoria-prompt`, `import-export`,
  `kereses-indexeles`, `adatbazis-illeszto`, `mcp-felulet`, `cjk` és `mentes-frissites`
  kampányokon nem. A `router-rangsor` `allitasok.csv`-jében
  a verdikt-oszlop üres. A `kategoria-prompt`-nál és az `import-export`-nál a keresők a saját fő állításaikat
  ellenőrizték — kétszeri, eltérő lekéréssel, illetve a jogszabály-idézeteket a mentett
  pillanatképekkel összevetve —, de független támadás egyiken sem futott. Mind a hat számait
  óvatosabban kell kezelni, mint a `szerver-technika` és a `skalazas` tárét; mindegyik `QA.md`
  kiírja, mi dőlt meg és mit nem sikerült megerősíteni.
- **Az `adatbazis-illeszto` tárban a lekérések egy része AI-átfogalmazott szöveget adott
  vissza a valódi oldal helyett.** Ahol lehetett, második lekéréssel kereszt-ellenőriztük;
  ahol nem, ott csak az idézőjelbe tett mondatok megbízhatóak. **Ez a kampány legnagyobb
  minőségi kockázata**, és a `QA.md` kiírja, mely forrásokat érintette.
- **A `kereses-indexeles`, az `adatbazis-illeszto`, az `mcp-felulet`, az `mcp-hibak`, a
  `cjk` és a `mentes-frissites` tárban nincs `allitasok.csv`.** Ezek a kampányok al-kérdésenkénti
  megállapítás-fájlokban tárolják az állításokat, nem soronkénti táblában — az idézetek a
  `kivonat.md`-ben és a `linkek.md`-ben vannak, forrásonként.
- **A `cjk` tár egyetlen keresővel készült**, ezért nincs benne kereszt-ellenőrzés két
  független kereső között. Cserébe minden hivatalos dokumentációs lapot **nyers `curl`-lal**
  kért le a WebFetch-összefoglaló helyett — ami itt nem óvatoskodás volt: az OpenSearch
  CJK-lapja és több GitHub README hiányos tartalmat adott vissza WebFetch-en. A `hianyok.md`
  kiírja, melyeket érintette.
- **A `mentes-frissites` hat keresője degradált módban futott**: mindegyik jelezte, hogy ő maga
  nem tudott további alügynököt indítani, tehát a keresés és a szintézis nem külön modellen,
  egymástól izolálva zajlott. A párhuzamosság a kampány szintjén megvolt (hat egyidejű kereső),
  és az idézetek nyers letöltésből, automatikus egyezés-ellenőrzéssel készültek — az
  ellentmondás-keresés mélysége viszont egy olvasatra korlátozódott. A `QA.md` kiírja.
- **A `korai-korok-ujra/` nem új téma, hanem újramérés.** A korai körökhöz (`memoriabol/`) nem
  készült URL-lista és állítás-tábla; ez a kampány pótolta. **Ha egy korai döntés forrását keresed,
  ide nézz, ne a `memoriabol/`-ba** — az a jegyzet, ez a bizonyíték.
- **Egy cáfolat is lejár.** A `korai-korok-ujra` derítette ki, hogy egy 2026-09-01-én megdöntött
  állítás (a Claude Code 10 000 karakteres hook-limitje) azóta hivatalosan dokumentálttá vált.
  A „nincs dokumentálva" megállapításokat ezért ugyanúgy újra kell mérni, mint a megerősítetteket.
- **A `QA.md`-t érdemes elolvasni**, mielőtt bármelyik számot használnád. Ott van kiírva, hol
  tévedtek a kutatók és hol tévedtem én.

## `memoriabol/`

A 2026-08-20, 08-23 és 09-01-i körök jegyzetei, amikor még nem készült strukturált tár. **A
2026-09-01-i adverzariális ellenőrzéssel kezdd**, ha régi számot akarsz használni: az első két kör
több állítása megdőlt vagy pontosításra szorult, és az ellenőrzés kiírja a védhető megfogalmazásukat.
