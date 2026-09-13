# Hiányok — mentés és verziófrissítés

Amit nem sikerült megtudni, és hogy az „nincs ilyen" vagy „nem találtuk meg".



---

# sq01 — Fájl-alapú tartalom mentése és helyreállítása

# SQ01 — Hiányok, amit nem sikerült megtudni

Jelölés: **[nincs ilyen]** = a kutatás alapján erős a gyanú, hogy az adott dolog egyszerűen nem létezik/nem hivatalos; **[nem találtuk meg]** = valószínűleg létezik, de ez a kutatás nem jutott el hozzá (idő/hozzáférés-korlát).

## Q1 — Fájlmentés konzisztencia

- **[nem találtuk meg]** A restic hivatalos dokumentációjában nem található egy külön, Linux-specifikus szakasz, amely explicit módon azt mondaná ki: "Linux alatt kösd össze LVM/ZFS/Btrfs pillanatképpel a konzisztens mentéshez." A VSS-integráció (Windows) dokumentált, a Linux oldali minta csak közvetetten, közösségi blogokból (T3, nem gyűjtött ebbe a kutatásba) vezethető le. Ez hiány a hivatalos dokumentációban, nem a kutatásunkban — de jelezzük, mert a megállapítások szakaszban ebből következtetést vontunk le.
- **[nem találtuk meg]** Nem sikerült elérni a `rsync.samba.org` és `download.samba.org` oldalakat közvetlenül (403), így a hivatalos "elsődleges" rsync man page helyett a projekt GitHub-forráskód-repójából (kanonikus, de nem a hagyományos publikálási csatorna) származó man page-et használtuk. Tartalmilag ugyanaz, de formálisan más URL.

## Q2 — Jegyzetrendszerek

- **[nincs ilyen]** Nem található **hivatalos** (git-scm.com, GitHub, GitLab) nyilatkozat, amely szó szerint kimondaná: "a git nem mentőeszköz" / "git is not a backup tool". Ez a mondás kizárólag közösségi blogokban, T3 forrásokban kering (pl. rewind.com, dzone.com, betterstack.com — ezeket a kutatás csak keresési találatként azonosította, nem dolgozta fel részletesen, mert a metodikai kikötés szerint a fő hivatalos forrásokra kellett fókuszálni). A GitHub hivatalos dokumentációja **közvetve** támasztja alá ugyanezt (bináris/SQL fájlokra, méretkorlátra vonatkozó explicit figyelmeztetéssel), de a "git nem backup" kifejezést nem használja szó szerint.
- **[nem találtuk meg]** Az Obsidian hivatalos "Back up your vault" / "Backup.md" oldalát a keresőmotor és a webes linkstruktúra alapján kerestük a `publish-01.obsidian.md` API-n keresztül, de a fájl a jelzett elnevezéssel/helyen **nem létezett** ("File … does not exist" — ezt WebFetch is megerősítette). A helyes, tényleges tartalmat végül a projekt GitHub-repójából ("Back up your Obsidian files.md") sikerült előkeríteni. Ez egy konkrét eset arra, hogy egy indexelt/linkelt cím nem feltétlenül vezet élő tartalomhoz — dokumentálva, hogy ne tűnjön úgy, mintha az Obsidian dokumentációja hiányos lenne (nem az, csak az URL-struktúra változott).
- **[nem találtuk meg]** Nem vizsgáltuk részletesen a git-annex-et vagy a Git LFS hivatalos dokumentációját, mint alternatív megoldást a bináris/nagy fájlok git-alapú kezelésére — ez tartalmilag releváns lehetne, de a kérdés fókusza (markdown jegyzetrendszerek mentése) miatt nem vontuk be mélyebben, elegendőnek ítéltük a GitHub hivatalos korlát-dokumentációját.
- **[nem találtuk meg]** Dokumentum-tárak (pl. Notion, Confluence) hivatalos mentési dokumentációját a kutatás nem dolgozta fel — a kérdés fájl-alapú (markdown-alapú, nem szerver-adatbázis-alapú) rendszerekre fókuszált, és az easter-memory-system kontextusa (fájl-igazságforrás) miatt ezt tudatosan kihagytuk.

## Q3 — 3-2-1 szabály eredete

- **[nincs ilyen]** Nem található **egyetlen, vitathatatlan, elsődleges dokumentum** (pl. Krogh saját, dátumozott cikke, vagy a könyv szkennelt oldala), amely bizonyítaná, hogy a "3-2-1" kifejezés pontosan a *The DAM Book* első kiadásában (2005) jelent meg először, ezzel a pontos szóhasználattal. Az állítás egyetlen forrásra (a `backupwrapup.com` podcast-interjú, amiben maga Krogh nyilatkozik) vezethető vissza ebben a kutatásban — ez T2 tier, nem T1. **Ez konkrétan azt jelenti, hogy az eredet-történet hihető, de nem hivatalosan/tudományosan dokumentált.**
- **[nincs ilyen]** Nem található olyan **nemzeti CERT** (magyar, német, francia stb.) hivatalos oldal, amely a "3-2-1" kifejezést **saját nevén, kanonizálva** használná (mint ahogy a CISA teszi). Az NCSC (UK) körülírja ugyanazt az elvet, de nem használja a "3-2-1" címkét a vizsgált oldalakon.
- **[nem találtuk meg]** A gyakran emlegetett "US-CERT ST04 tipp" vagy hasonló azonosítójú hivatalos amerikai CERT-dokumentum létezését nem sikerült megerősíteni — a keresés nem hozott ilyen tippszámú, azonosítható dokumentumot; lehet, hogy ez tévesen terjedő állítás, vagy egy már megszűnt/átnevezett US-CERT oldalra utal, amit a mai CISA-struktúra nem őrzött meg ezen az azonosítón.

## Q4 — Helyreállítás-ellenőrzés

- **[nincs ilyen]** Nem található **egyetlen, egyetemesen elfogadott számadat** arra, hogy "a mentések hány százaléka bizonyul általánosságban helyreállíthatatlannak". A talált egyetlen konkrét, módszertannal alátámasztott szám (At-Bay, 31%) **kifejezetten zsarolóvírus-támadás kontextusára, kkv-kra** vonatkozik — nem általánosítható minden mentési forgatókönyvre. A gyakran hivatkozott "Gartner-számok" (pl. "a tape-mentések X%-a hibás") nyomát ebben a kutatásban nem sikerült egy ellenőrizhető, elsődleges Gartner-jelentésig visszavezetni — **ez konkrétan hiány, nem állítjuk, hogy a szám ne létezne, csak hogy ez a kutatás nem találta meg az elsődleges forrást.**
- **[nincs ilyen]** A "nobody wants backup, everybody wants restore" mondás elsődleges, dátumozott forrását (ki mondta ki ELŐSZÖR, mikor, milyen fórumon) nem sikerült azonosítani. W. Curtis Preston neve következetesen felmerül másodkézből (blogok, podcastok), de egyetlen elsődleges idézet-forrást sem találtunk, ahol ő maga, dátummal ellátva, elsőként dokumentáltan kimondta volna.
- **[nem találtuk meg]** Nem vizsgáltuk az ISO 22301 szabvány szövegét közvetlenül (fizetős szabvány, nem elérhető szabadon a proxin keresztül sem) — csak másodlagos forrásokból (PECB, Advisera) ismert a tartalma, ezeket a kutatás nem dolgozta fel részletesen, mert a NIST SP 800-34 ingyenesen elérhető, T1 alternatívát adott ugyanarra a fogalompárra.

## Q5 — Mentési gyakoriság kis rendszereknél

- **[nincs ilyen]** Kifejezetten **"néhány felhasználós, néhány ezer fájlos" méretkategóriára szabott** hivatalos vagy mért ajánlást **nem találtunk**. Minden talált forrás (CISA, NCSC, CIS, NIST) általános vállalati/szervezeti méretskálán fogalmaz, explicit kis rendszerekre vonatkozó, méret-specifikus szám nélkül. A CIS Controls "heti" ajánlása a legközelebbi számszerű támpont, de ez sem méret-specifikus (adatérzékenység-alapú, nem fájlszám-alapú).
- **[nem találtuk meg]** Nem találtunk mért/empirikus tanulmányt (pl. akadémiai vagy iparági benchmark), amely konkrét fájlszám/felhasználószám mellett mérte volna az optimális mentési gyakoriságot. Ez valószínűleg azért is nehéz, mert a gyakoriság optimális értéke elsősorban az adatváltozás sebességétől (RPO-tűrés) függ, nem a fájlok számától — ezt a NIST RPO-definíciója is alátámasztja (a döntés "organization-defined", kockázatalapú, nem méret-alapú).

## Q6 — Jogosultsági kockázat

- **[nem találtuk meg]** Az NCSC "Principles for ransomware-resistant on-premises backups" oldal mind a hat elvét **csak egyetlen forrásból (a hivatalos NCSC-oldal maga, WebFetch-csal kinyerve)** sikerült megszerezni. Nem találtunk második, független forrást (pl. tech-sajtó cikket), amely szó szerint idézte volna ugyanezeket a mondatokat, így ezekhez az idézetekhez **nincs kereszthivatkozás** — csak az egy elsődleges forrás. Ez módszertanilag korrekt (a forrás maga hivatalos, T1), de a kikötött "két független forrás" elv itt nem teljesült.
- **[nem találtuk meg]** Nem sikerült nyers curl-lel hozzáférni az NCSC oldalak tartalmához (kliensoldali JS-renderelés miatt), ezért minden NCSC-idézet **WebFetch-alapú**, ami a metodikai kikötés szerint kockázatosabb (kis modell összefoglalója). A WebFetch válaszai belsőleg konzisztensek voltak és konkrét, ellenőrizhető szövegrészeket adtak vissza (nem általános összefoglalót), de ez nem helyettesíti a nyers HTML-ből származó, szó szerint ellenőrzött idézetet.
- **[nincs ilyen]** Nem található **számszerű** (pl. "X% -ban vezetett incidenshez a jogosultság-megkerülés") kockázatbecslés semelyik vizsgált hivatalos forrásban. A kockázatot minden forrás kvalitatív ajánlásokkal kezeli (külön fiók, titkosítás, WORM), mért gyakorisági adat nélkül.
- **[nem találtuk meg]** A CISA PDF-je ("Data Backup Options") — amely a keresési találatok alapján valószínűleg tartalmazna releváns, tömör összefoglalást a 3-2-1 szabályról és a hozzáférés-védelemről — **sem nyers curl-lel, sem WebFetch-csal nem volt elérhető** (mindkettő 403-at adott). Ennek tartalmát csak a helyette elérhető CISA weboldalak (amik feltehetően ugyanazt a szöveget tartalmazzák HTML formában) alapján rekonstruáltuk — ez nem teljesen biztos helyettesítés.

## AI-összefoglalót vagy hiányos tartalmat visszaadó lekérések (külön jelölve, a kikötés szerint)

- **WebFetch `https://www.cisa.gov/audiences/small-and-medium-businesses/secure-your-business/back-up-business-data`** és a government-verzió: a WebFetch kis modellje szó szerinti idézeteket adott vissza, ezek konzisztensek voltak egymással (két oldal, azonos szöveg) — nem tűnik hiányosnak, de nem tudjuk 100%-ban kizárni, hogy a modell kihagyott egy releváns bekezdést, mivel nem volt hozzáférésünk a nyers HTML-hez ellenőrzésképp.
- **WebFetch `https://www.ncsc.gov.uk/collection/small-organisations-guide-to-cyber-security/backing-up-your-data`**: a modell explicit jelezte, hogy bizonyos témákat (gyakoriság, titkosítás, hozzáférés-szabályozás) **nem talált az oldalon** — ez lehet, hogy a lap tényleg nem tér ki ezekre, vagy hogy a modell nem jutott el az oldal alján lévő tartalomig. Nem tudtuk ellenőrizni nyers HTML-lel (JS-renderelés miatt).
- **WebFetch `https://www.ncsc.gov.uk/collection/ransomware-resistant-backups`**: a modell explicit jelezte, hogy csak a gyűjtőoldal bevezetőjéhez fért hozzá, a részletes elvek egy másik al-oldalon vannak — ezt a modell maga jelezte, nem utólag derült ki, ez a legmegbízhatóbb típusú WebFetch-válasz (a modell nem állította, hogy teljes, amikor nem volt az).
- **WebFetch `https://obsidian.md/help/Obsidian+Sync/Back+up+your+vault`**: a válasz "Not Found" volt — ezt megerősítettük nyers curl-lel is (ugyanaz a hibaüzenet jött vissza az API-n keresztül), tehát ez nem WebFetch-hiba, hanem valós 404/hiányzó tartalom.



---

# sq02 — Futó SQLite adatbázis biztonságos mentése

# sq02 — Hiányok (amit nem sikerült megtudni)

A feladat kifejezetten kérte: "Ha valamire nincs adat, azt írd meg hiányként. Ne találj ki számot." Az alábbi lista pontosan ezt teszi — megkülönböztetve, hogy egy adott hiány **"nincs ilyen"** (a dokumentáció/forrás szándékosan nem foglalkozik vele, mert nem releváns vagy nem létezik a jelenség), vagy **"nem találtuk meg"** (valószínűleg létezik ilyen adat valahol, de ebben a kutatásban nem került elő).

---

## 1. Mért időtartam-adatok a Backup API-ra és a VACUUM INTO-ra, méret szerint

**Státusz: NEM TALÁLTUK MEG** (valószínűleg létezik ilyen mérés valahol, pl. belső blogokban, de a keresés nem hozta fel).

Sem a hivatalos SQLite-dokumentáció (`backup.html`, `lang_vacuum.html`, `wal.html`), sem a fellelt közösségi tartalom nem közöl konkrét, "X GB adatbázis → Y másodperc" jellegű, méret-specifikus benchmarkot sem a Backup API-ra, sem a `VACUUM INTO`-ra. A `keresesek.md`-ben dokumentált 6 különböző keresési kísérlet (pontos szó szerinti lekérdezésekkel) egyike sem hozott fel hiteles, konkrét számot.

Az egyetlen számszerű adat, amit találtunk (`~2ms` egy 440 MB-os, illetve egy 4,4 GB-os adatbázis másolására), a `cp --reflink=always` Btrfs Copy-on-Write művelethez tartozik, **nem** a Backup API-hoz vagy a `VACUUM INTO`-hoz — ez a szám metaadat-szintű blokk-megosztásból adódik, és nem extrapolálható a ténylegesen lapokat olvasó/író/tömörítő módszerekre. Ezt explicit módon jeleztük a `megallapitasok.md` 4. szakaszában, nem kevertük össze a két dolgot.

**Következmény a döntéshez:** ha a `mentes-frissites` kampányban konkrét időbecslésre van szükség (pl. "mennyi ideig áll le/lassul a szerver egy mentés alatt"), ezt **saját méréssel** kell megállapítani a tényleges (vagy ahhoz hasonló méretű) adatbázison — nincs megbízható külső referenciaszám, amire támaszkodni lehetne.

## 2. Blokkolja-e, és mennyi ideig, a `VACUUM INTO` a konkurens írókat — közvetlen mérés

**Státusz: RÉSZLEGES HIÁNY.** A hivatalos dokumentáció (`lang_vacuum.html`) elméleti/zárolási szinten leírja, hogy a sima `VACUUM` (nem `VACUUM INTO`) elbukik, ha másik kapcsolat írás-zárat tart, és hogy a `VACUUM INTO` ebből a szempontból megengedőbb (nem "write operation" a többi kapcsolat szemszögéből). **De nincs kimondva**, hogy a `VACUUM INTO` futása közben a forrás-adatbázison keletkező írások pontosan hogyan viselkednek (várakoznak-e, elbuknak-e, vagy problémamentesen lefutnak-e párhuzamosan) — ezt logikailag levezettük ("mivel nem write operation, nem blokkolja"), de ezt **nem támasztja alá szó szerinti, explicit dokumentum-idézet**, csak közvetett következtetés a meglévő szövegből.

## 3. A `.backup` CLI-parancs explicit dokumentációs megerősítése arról, hogy a Backup API-t hívja

**Státusz: MEGOLDVA, DE NEM A VÁRT MÓDON.** Egyetlen hivatalos *leíró* oldal (`cli.html`, `backup.html`) sem mondja ki explicit szöveggel, hogy a `.backup` dot-parancs a `sqlite3_backup_*` C-függvényeket hívja. Ezt végül **közvetlenül a forráskódból** (`src/shell.c.in`, a hivatalos Fossil-repóból) igazoltuk — ez T1-es bizonyíték, de kódrészlet, nem "dokumentáció-idézet" a szó szoros értelmében. Ha a feladat szigorúan csak *dokumentáció*-idézetet fogadna el (nem forráskódot), ez a pont **hiányként** kezelendő.

## 4. Mennyi ideig tart egy tipikus `PRAGMA wal_checkpoint(FULL)` / `(RESTART)` / `(TRUNCATE)` egy adott méretű WAL-on

**Státusz: NEM TALÁLTUK MEG.** A `pragma.html` és `wal.html` leírja a mechanizmust és azt, hogy a `FULL`/`RESTART` blokkolja az írókat, de nem ad időbecslést. A "wal checkpointing very slow" SQLite fórum-szál (T3) kvalitatív magyarázatot ad arra, *miért* lehet lassú (sok kis tranzakció → sok megváltozott lap → sok checkpoint-munka), de nem közöl konkrét mérőszámot (sem "MB/s", sem "lap/s", sem konkrét másodperc-adatot adott WAL-mérethez).

## 5. Konkrét, számszerűsített "reader gap" ajánlás a checkpoint starvation elkerülésére

**Státusz: NINCS ILYEN (a dokumentáció szándékosan nem ad számot).** A `wal.html` "Checkpoint starvation" szakasza kvalitatív tanácsot ad ("biztosíts időszakos szüneteket, amikor senki sem olvas"), de nem ad konkrét küszöbértéket (pl. "X másodpercenként legyen legalább Y másodperc olvasó-mentes ablak"). Ez rendszer-specifikus paraméter, amit a dokumentáció explicit módon az alkalmazásfejlesztőre bíz.

## 6. A `.dump` konzisztencia-garanciájának hivatalos, explicit kimondása

**Státusz: NEM TALÁLTUK MEG hivatalos dokumentum-szövegben.** Azt, hogy a `.dump` egyetlen `SAVEPOINT`/implicit tranzakción belül fut (tehát konzisztens, egy pillanatra vonatkozó olvasást ad egy változó adatbázison is), **csak a forráskódból** (`shell.c.in`, `SAVEPOINT dump;` sor) sikerült megállapítani — egyetlen hivatalos leíró oldal (`cli.html`) sem mondja ki ezt kifejezetten szöveggel. Ez ugyanaz a típusú hiány, mint a 3. pont.

## 7. Bevett, dokumentált megoldás két külön SQLite-fájl kereszt-konzisztens mentésére

**Státusz: EZ EXPLICIT, MEGERŐSÍTETT HIÁNY — NEM CSAK "NEM TALÁLTUK MEG", HANEM VALÓSZÍNŰLEG "NINCS ILYEN".** Ezt részletesen tárgyaljuk a `megallapitasok.md` 6. szakaszában. Összefoglalva: a SQLite saját `ATTACH`-alapú többfájlos atomicitása kifejezetten nem működik WAL módban (hivatalos, szó szerint idézett dokumentáció-szöveg a `lang_attach.html`-ről); a Litestream dokumentációja adatbázisonként teljesen független replikációs folyamot ír le, kereszt-adatbázis garancia nélkül; és **egyetlen** felkutatott közösségi forrás (SQLite fórum, Oldmoe blog, Lobsters-vita) sem tárgyalja ezt a problémát mint önálló, megoldott témát. Ez a hiány önmagában is releváns kutatási eredmény: a probléma vagy ritkán merül fel gyakorlatban (mert a legtöbb rendszer egyetlen SQLite-fájlt használ), vagy azok, akik szembesülnek vele, alkalmazás-szintű, egyedi (nem publikált, nem szabványosított) megoldást választanak.

## 8. Litestream WAL2 (WAL módú, két WAL-fájlos SQLite-kiterjesztés) kompatibilitás

**Státusz: ELLENTMONDÁSOS/BIZONYTALAN, RÉSZLETEZVE `ellentmondasok.md`-ben.** Az Oldmoe blog (T3, 2024-04-30) megjegyzi Litestream hátrányai között: "Potentially not compatible with the more advanced WAL2 mode." Ezt a hivatalos Litestream-dokumentáció egyetlen általunk lekért oldalán sem sikerült sem megerősíteni, sem cáfolni — a `tips.txt`, `how-it-works.txt` egyike sem említi a WAL2-t. Mivel a WAL2 egyébként is kísérleti SQLite-funkció (nem release az fő ágban), ez valószínűleg nem releváns a jelen kampányra, de a forrásból nem derül ki egyértelműen, ezért hiányként jelezzük, nem állítjuk sem igazként, sem hamisként.

## 9. A `sqlite3_rsync` gyakorlati teljesítménye/elterjedtsége

**Státusz: NEM VOLT A FELADAT KÖZVETLEN KÉRDÉSE, DE KAPCSOLÓDIK.** A `howtocorrupt.html` és `backup.html` mindkettő megemlíti a `sqlite3_rsync`-et mint harmadik hivatalos, biztonságos mentési módot (3.47.0-tól, 2024-10-21). Mivel ez viszonylag új eszköz, és a feladat kifejezetten csak a Backup API-t, `VACUUM INTO`-t, `.backup`-ot és `.dump`-ot kérte részletesen, nem mélyedtünk el benne — de érdemes megjegyezni, hogy **létezik egy negyedik hivatalos út is**, amit a task nem kért expliciten, de a hivatalos dokumentáció vele egy sorban említi a többit. Ha a `mentes-frissites` kampány következő lépésében SSH-alapú, távoli gépre történő mentés is szóba kerül, ez a dedikált eszköz érdemes a további vizsgálatra.



---

# sq03 — Séma-migráció és verziófrissítés futó rendszeren

# sq03 — Hiányok és nyitott kérdések

Minden tételnél jelölve: **„nincs ilyen"** = a hivatalos forrás átvizsgálva, és a keresett állítás/funkció
kimutathatóan nem szerepel benne (megbízható negatív találat); **„nem találtuk meg"** = időkorlát vagy elérési
akadály miatt nem sikerült ellenőrizni, a válasz továbbra is nyitott.

---

## 1. Drizzle migrációs modell

- **„Nincs ilyen"**: nincs `drizzle-kit down`/`undo`/`rollback` parancs. A teljes, hivatalosan felsorolt
  parancslista (`generate, migrate, push, pull, check, up, studio, export`) kimerítő, ezt kétszer is
  keresztellenőriztük (overview oldal + a `--help`-stílusú parancslista más aloldalakon).
- **„Nem találtuk meg"**: nem sikerült egyértelműen tisztázni, mit jelent pontosan a migrations-fundamentals
  oldal „rollback DDL changes if something fails" fordulata — ez lehet (a) az alkalmazás-deploy szintű
  visszaállás (pl. előző image visszaállítása + DB visszaállítás mentésből), vagy (b) egy konkrét, de nem
  dokumentált mechanizmus. A hivatalos szöveg nem ad linket, példát vagy API-t ehhez a mondathoz. Ezt
  kétértelműségként kezeltük a `megallapitasok.md`-ben, nem állítottunk mögé konkrét funkciót.
- **„Nem találtuk meg"**: nem ellenőriztük részletesen a `drizzle-kit pull`, `drizzle-kit check` és
  `drizzle-kit up` parancsok dokumentációját (csak az overview-ból ismert egy-mondatos leírásuk) — ezek
  valószínűleg nem relevánsak a rollback/mentés kérdéshez, de teljesség kedvéért megjegyezzük, hogy nem lettek
  mélységében átvizsgálva.
- **„Nem találtuk meg"**: nem ellenőriztük, hogy a Bun natív `bun:sqlite` drivere (amit az easter-memory-system
  feltehetően használ) milyen alapértelmezett `PRAGMA foreign_keys` értékkel indul — ez a target rendszer saját
  technológiai választásától függő, gyakorlati kérdés, amit ez a kutatás nem tudott lefedni, mert nem szerepelt
  a hivatalos Drizzle- vagy SQLite-dokumentációban (driver-specifikus beállítás, nem motor-alapértelmezés).

## 2. SQLite ALTER TABLE / 12 lépés

- Ezen a témán nincs érdemi hiány — a hivatalos `sqlite.org/lang_altertable.html` oldal kimerítően és
  egyértelműen válaszolt minden feltett kérdésre, szó szerinti idézetekkel alátámasztva.
- **„Nem találtuk meg"**: nem vizsgáltuk meg részletesen a `PRAGMA writable_schema` teljes dokumentációját (csak
  az `ALTER TABLE`-lapon felbukkanó hivatkozásait), így nem tudjuk pontosan, milyen egyéb kockázatai vannak ennek
  a pragmának a 8. szakaszban leírt „egyszerűbb eljáráson" kívül.

## 3. FTS5 rebuild/triggerek

- **„Nem találtuk meg"**: a hivatalos `fts5.html` dokumentáció **sehol nem mondja ki explicit módon**, hogy egy
  FTS5 virtuális tábla oszloplistáját vagy tokenizerét hogyan (vagy hogy egyáltalán) lehet utólag megváltoztatni
  `ALTER TABLE`-lel, illetve hogy az `ALTER TABLE RENAME`/`ADD COLUMN`/`DROP COLUMN` egyáltalán alkalmazható-e
  virtuális táblákra. Ez egy valódi dokumentációs rés (nem a mi kutatási hiányosságunk, hanem magának az SQLite
  hivatalos dokumentációjának a hiánya) — csak közvetett, közösségi (T3) jelekre tudtunk támaszkodni annak
  feltételezésére, hogy a bevett gyakorlat a `DROP TABLE` + újra-`CREATE VIRTUAL TABLE` + `rebuild`/újratöltés.
  **Ezt gyakorlati teszteléssel (pl. egy próba-adatbázison `ALTER TABLE fts_tabla RENAME TO ...` kipróbálásával)
  lehetne csak megbízhatóan lezárni, amit ez a kutatás nem végzett el.**
- **„Nem találtuk meg"**: nem sikerült elérni a Home Assistant hivatalos storage-migrációs dokumentációját
  (`developers.home-assistant.io/docs/architecture/storage/` — 404-et adott), ami egy tervezett, konkrét
  „verziómező + `async_migrate_func`" példa lett volna JSON-alapú konfigurációs fájlokra. Emiatt a
  `megallapitasok.md` 6. pontja **nem** hivatkozik Home Assistantra, csak a ténylegesen ellenőrzött rendszerekre.

## 4. Expand–contract

- **„Nem találtuk meg"** (elsődleges forrás hiánya): Joshua Kerievsky 2006-os eredeti leírását (amire Fowler
  bliki-oldala hivatkozik: „first documented as a refactoring strategy by Joshua Kerievsky in 2006") **nem
  ellenőriztük közvetlenül**. Ezt kizárólag Fowler saját állításából ismerjük (másodkézből), így ezt a konkrét
  történeti attribúciót T2-es, nem T1-es bizonyossággal kezeljük a jelentésben.
- **„Nem találtuk meg"**: Michael T. Nygard „Release It!" (2007) könyvének „Zero Downtime Deployments" fejezetét
  nem sikerült nyersen elérni (nem szabadon hozzáférhető online szöveg) — ezt csak a Wellhausen-tanulmány
  hivatkozásjegyzékéből (másodkézből) ismerjük, mint a minta egy másik, független eredetszálát.
- **„Nem találtuk meg"** egy kifejezetten „single-instance rendszereknél az expand-contract szükségtelen"
  kimondást tartalmazó, name-elt, hivatalos forrás — ehelyett **következtetést vontunk le** három, egymástól
  független forrás (Fowler/Sadalage evodb cikke + Wellhausen tanulmány + maga a Fowler Parallel Change oldal
  alkalmazási példáinak jellege) együttes olvasatából. Ez a jelentésben világosan jelölve van mint levezetett
  következtetés, nem mint egyetlen forrás szó szerinti kimondása.
- A GitLab „Proposal: Remove all single-node zero downtime instructions" MR (találtuk WebSearch-ben, nem
  vizsgáltuk tovább) potenciálisan releváns, iparági gyakorlati példa lehetne arra, hogy egy valós, nagy projekt
  hogyan kezeli a kis/egy-node telepítéseket a zero-downtime dokumentációban, de **nem lett tovább vizsgálva**
  időbeosztási okokból.

## 5. Mentés a migráció előtt

- **„Nincs ilyen"** (megbízható negatív találat, teljes szöveg átvizsgálva): a Drizzle, a Rails Active Record
  Migrations Guide és a Django Migrations témaoldal egyike sem tartalmaz explicit „készíts mentést" ajánlást a
  fő migrációs dokumentációjában.
- **„Nem találtuk meg"**: nem vizsgáltuk át a Rails és Django **teljes** hivatalos dokumentációját (csak a
  migrációkról szóló fő oldalakat) — elképzelhető, hogy egy külön „Deployment checklist" vagy „Production"
  oldalukon van mentési ajánlás, ami nem kifejezetten a migrációs guide-hoz kötődik. Ezt nem zártuk ki teljesen,
  csak a migrációs témaoldalakra szűkítettük az állítást.
- **„Nem találtuk meg"**: nem sikerült egyértelmű, hivatalos Liquibase „best practices" oldalt találni (a
  `concepts/bestpractices.html` URL valójában az FAQ-ra redirektel a jelenlegi doksi-struktúrában) — lehet, hogy
  létezik egy külön, jól elnevezett „best practices" hivatalos oldal más URL-en, amit nem sikerült megtalálni.

## 6. Fájlformátum-verziózás

- **„Nem találtuk meg"**: a leggyakoribb markdown/YAML-frontmatter-alapú statikus oldal-generátorok (Jekyll,
  Hugo, Eleventy, Astro, Gatsby, Docusaurus) hivatalos frontmatter-dokumentációit **ebben a körben nem néztük
  át egyenként** — így nem tudjuk megerősített T1-forrással alátámasztani azt a (valószínűsíthető, de itt nem
  ellenőrzött) általános benyomást, hogy ezek jellemzően NEM definiálnak séma-verzió mezőt a frontmatterben. A
  `megallapitasok.md`-ben ezért **nem** szerepel ilyen általánosító állítás ezekről a konkrét rendszerekről —
  csak a ténylegesen ellenőrzött rendszerek (nbformat, WXR, Compose, JSON Canvas) kerültek be.
- **„Nem találtuk meg"**: „egyszeri tömeges átírás" (bulk one-time rewrite) mintára **nem találtunk** konkrét,
  megnevezett, hivatalos dokumentációval alátámasztott rendszert ebben a kutatási körben. Ez lehet, hogy létezik
  (pl. valamelyik statikus site-generátor `migrate`/`upgrade` CLI-parancsa ilyet csinál), de nem sikerült ezt
  hivatalos forrással igazolni a rendelkezésre álló idő alatt.
- **„Nem találtuk meg"**: a Home Assistant `.storage` JSON-fájljainak `version`/`minor_version` mezőit és
  `async_migrate_func` mechanizmusát (ami egy nagyon jó párhuzamos példa lenne) nem sikerült hivatalos forrásból
  megerősíteni (404-es hivatkozás, lásd fent) — emiatt kimaradt a fő jelentésből.

## 7. Docker-alapú frissítés

- **„Nincs ilyen"**: a hivatalos „Running Compose in production" oldal (`docs.docker.com/compose/how-tos/production/`)
  **nem tartalmaz** explicit, prózai ajánlást arra, hogy adatbázis-migrációt a konténer-csere előtt vagy után kell-e
  futtatni — ezt a teljes, letöltött, tag-stripelt szöveg átvizsgálásával állapítottuk meg (nincs „migrat" szótő
  előfordulás a lényegi, nem-navigációs részben).
- **„Nem találtuk meg"**: bár a `pre_start`/`depends_on: condition: service_completed_successfully` mechanizmus
  hivatalosan dokumentált, és van egy konkrét, kidolgozott (Django `manage.py migrate`) példa, **nem találtunk
  kifejezett, önálló „best practice" bekezdést**, ami *érvelne* amellett, hogy ez a helyes sorrend — a
  dokumentáció a mechanizmust és egy példát ad, de nem fogalmaz meg normatív ajánlást szöveges formában.
- **„Nem találtuk meg"**: nem ellenőriztük, hogy a `pre_start` funkció (Compose 5.3.0+, a dokumentáció szerint)
  ténylegesen elérhető-e a `docker compose` legfrissebb, széles körben telepített verzióiban, vagy ez egy
  nagyon friss/kísérleti funkció, amire még nem sok gyakorlati telepítés támaszkodik. Ez fontos gyakorlati
  szűkítés lehet az easter-memory-system tervezésénél, ha annak Compose-verziója régebbi.
- **„Nem találtuk meg"**: nem vizsgáltuk meg külön a Docker hivatalos „Backup and restore data" (a
  `docker-volumes.txt`-ben a tartalomjegyzékben látott, de külön nem részletezett) szakaszt teljes egészében —
  csak a „Back up a volume"/„Restore volume from a backup" alszakaszokat idéztük.
- **„Nincs ilyen"**: nem találtunk hivatalos Docker/Compose ajánlást arra vonatkozóan, hogy egy SQLite-fájl-alapú
  adatbázis esetén (szemben egy szerver-alapú DB-vel, mint Postgres) hogyan kezelendő speciálisan a
  „service_healthy" healthcheck-feltétel — ez a mechanizmus dokumentáltan szerver-DB-kre (pl. Postgres) van
  szabva a hivatalos példákban, SQLite-fájlra nincs analóg „healthcheck" fogalom, ezt a jelentés nem old fel,
  csak jelzi mint a minta korlátját az easter-memory-system konkrét esetére nézve.



---

# sq04 — Mit kell menteni, és honnan tudjuk, hogy jó

# sq04 — Hiányok

Az alábbiak azok a pontok, ahol a kérdésfeltevés konkrét, mért adatot vagy explicit hatósági/szabványi kimondást várt, de a kutatás során **nem találtunk** ilyet — megkülönböztetve, hogy ez "nincs ilyen adat/szabály" (evidence of absence) vagy "nem sikerült megtalálni" (absence of evidence, további kereséssel esetleg előkerülhetne).

## 1. Származtatott adat mentése

- **Hiány: nincs publikált, konkrét "X MB forrásszöveg → Y MB derived index" térmegtakarítási arányszám.** Az AWS Well-Architected és a SQLite dokumentáció csak elvi szinten ("minimize storage consumption") érvel, számszerű arány nélkül. Ez inkább *nem találtuk meg* típusú hiány — valószínűleg létezik ilyen benchmark valamelyik adatbázis/keresőmotor teljesítmény-blogján, de a rendelkezésre álló keresési idő alatt nem került elő hivatalos vagy lektorált forrásból.
- **Hiány: nincs kifejezetten kis méretű (néhány ezer dokumentumos, egygépes) rendszerre vonatkozó mért index-újraépítési idő.** A talált konkrét szám (SoundCloud, 720 millió dokumentum, ~30 perc–1 óra) több nagyságrenddel nagyobb rendszerre vonatkozik. A kisebb méretre vonatkozó extrapoláció (másodperces–perces nagyságrend) a mi következtetésünk, nem mért adat — ezt a `megallapitasok.md`-ben jelöltük "nem mért, hanem levezetett" jelleggel.
- Ez utóbbi *evidence of absence*-nek tekinthető abban az értelemben, hogy egy néhány ezer fájlos SQLite FTS5 index újraépítése olyan triviálisan gyors (feltehetően < 1 másodperc – néhány másodperc), hogy ritkán éri meg külön megmérni és publikálni — tehát a hiány oka valószínűleg az, hogy a kérdés a gyakorlatban nem elég érdekes ahhoz, hogy valaki lemérje és közzétegye, nem az, hogy rejtett probléma volna.

## 2. Beágyazások speciális esete

- **Hiány: nincs hivatalos, publikált "idő/tétel" (pl. ms/embedding vagy embedding/másodperc) átviteli sebesség-szám az OpenAI (vagy más nagy szolgáltató) hivatalos dokumentációjában.** Csak felső korlátokat (rate limit, TPM/RPM) találtunk, ami nem azonos a tényleges mért teljesítménnyel. Ez *nem találtuk meg* típusú hiány — ilyen benchmarkot valószínűleg lehetne találni harmadik féltől (pl. független API-terhelés-tesztek), de ezek T3-as, nem hivatalos jellegűek lettek volna, és a kikötés szerint nem akartunk kitalált vagy nem-hivatalos számot beépíteni a fő megállapítások közé.
- **Hiány: nem találtunk hivatalos dokumentációt kifejezetten "content-hash alapú embedding cache" néven, iparági szabvány vagy szabványosított minta formájában.** Az, amit találtunk (LlamaIndex `IngestionCache`, Redis semantic cache, LangChain-ekvivalensek), mind egyedi termékek/keretrendszerek dokumentációja (T2), nem egy általánosan elfogadott, elnevezett minta hivatalos szabványból. Ez azt jelenti: **a minta létezik és széles körben alkalmazott, de nincs rá egységes "hivatalos" definíció** — ez inkább *evidence of absence* egy formális szabvány tekintetében, miközben a gyakorlati minta létezését (T2 szinten) megerősítettük.
- **Hiány: helyi (self-hosted) embedding-modellek újraszámítási költsége** (pl. GPU-idő egy helyi sentence-transformers modellel) — a kérdés kifejezetten "külső vagy helyi modell hívása" mindkettőt említi, de mi csak a külső (OpenAI) API-árat tudtuk hivatalos forrásból dokumentálni. Helyi modell esetén a "költség" áram/GPU-idő formájában jelentkezik, erre nem találtunk mért, hivatalos benchmarkot a rendelkezésre álló időben.

## 3. Mentés-ellenőrzés (verification)

- **Hiány: sem a Borg, sem a restic hivatalos dokumentációja nem ad konkrét, számszerű ajánlott gyakoriságot** (pl. "havonta futtasd a `--verify-data`-t") a teljes adattartalom-ellenőrzésre. Mindkettő csak "regularly"/"it's a good idea to regularly" megfogalmazást használ, konkrét szám nélkül. Ez **evidence of absence**: kifejezetten kerestük ("recommended frequency"), és sem a hivatalos dokumentáció, sem a hivatalos fórumok releváns szálai nem adtak T1-es, számszerű választ ezekre az eszközökre — ezzel szemben a ZFS/Oracle dokumentáció igenis ad konkrét számot (30 nap alapértelmezett), ami arra utal, hogy ez tudatos tervezési döntés különbség a checksumos fájlrendszer (ahol a scrub olcsó, automatizált, beépített) és a deduplikáló mentőeszközök (ahol a teljes ellenőrzés drága, külön kell elindítani) között.

## 4. Csendes adatromlás (bit rot)

- **Hiány: nem találtunk Google-specifikus, névvel azonosítható "silent corruption" tanulmányt** a kért formában (a Google-lel kapcsolatos találatok a Pinheiro et al. 2007 "Failure Trends in a Large Disk Drive Population" tanulmányra mutattak, amely **lemez-meghibásodásról**, nem csendes bitkorrupcióról szól — más metrika, mint amit a CERN/NetApp mér). Ezt jeleztük a `megallapitasok.md` 4.3 pontjában is: a Backblaze/Google-típusú adatok a *teljes meghajtó-meghibásodást* mérik, nem a *néma* korrupciót — ez fontos módszertani megkülönböztetés, amit a jelentésben explicit módon külön kell kezelni, nehogy összemosódjon a két jelenség.
- **Hiány: nem sikerült frissebb (2015 utáni), hasonlóan nagy mintaméretű, lektorált silent-corruption tanulmányt találni**, amely megismételné vagy frissítené a 2007-es CERN- és a 2008-as NetApp-mérést modern (SSD, NVMe) tárolókra. A talált modernebb hivatkozás (Facebook/Meta "Silent Data Corruptions at Scale", arXiv 2102.11245) a keresési listában megjelent, de **nem került nyers letöltésre és idézésre** ebben a körben — ezt konkrét, kihasznált hiányként rögzítjük: érdemes lenne egy következő körben ezt a Facebook/Meta-tanulmányt is bevonni SSD/CPU-szintű silent corruption adatokért, mivel az láthatóan modernebb infrastruktúrára vonatkozik, mint a 2007–2008-as HDD-alapú mérések.

## 5. Titkok és kulcsok a mentésben

- **Hiány: az OWASP ASVS 5.0 nem tartalmaz explicit, "titok NE kerüljön mentésbe" vagy "titok csak feltétellel kerülhet mentésbe" szabálypontot.** A V13.3 szakasz csak az alkalmazás forráskódjából/build-artefaktumaiból tiltja ki a titkokat, a mentésekre nem tér ki külön. Ez **evidence of absence** a konkrét ASVS-dokumentumban — a védelem csak közvetve (secrets management megoldás elve, illetve az OWASP *Cheat Sheet* — ami külön dokumentum, nem maga az ASVS-szabvány — 2.9 és 3.2.2 szakasza) vezethető le.
- **Hiány: nem találtunk konkrét NIST-előírást arra, hogy az easter-memory-system konkrét esetére (pl. egy embedding-szolgáltatás API-kulcsa) melyik kategóriába esne** a NIST SP 800-57 kulcstáblázatában — az API-kulcs nem klasszikus kriptográfiai kulcs a szabvány taxonómiájában (inkább hitelesítési/hozzáférési titok), ezért a táblázat sorai csak analógiával, nem közvetlenül alkalmazhatók rá. Ezt a mi levezetésünkként jelöltük, nem közvetlen szabványi kimondásként.

## 6. Mentés visszaállítása és jogosultság (GDPR)

- **Hiány (a legfontosabb ezen a területen): egyik talált hatósági forrás (ICO, EDPB) sem tér ki explicit módon a "visszaállított bejegyzés visszakapja-e a korábban visszavont hozzáférési jogosultságot" kérdésre.** Mindkét forrás kizárólag a *személyes adatok törlését* tárgyalja a mentések kontextusában, nem a *hozzáférés-vezérlési állapot* (jogosultságok, szerepkörök) visszaállítás utáni kezelését. Ez **evidence of absence**: kifejezetten kerestünk erre vonatkozó anyagot, és nem került elő — ez arra utal, hogy ez egy kevésbé feltárt, kifejezetten technikai/gyakorlati kérdés, amit a jogi/hatósági irodalom eddig nem kezelt külön kategóriaként (valószínűleg azért, mert jogi szempontból a hozzáférési jogosultság-visszaállás beleérthető az általánosabb "adatvédelmi incidens" vagy "hozzáférés-vezérlési" szabályozásba, nem a törléshez való jog speciális eseteként kezelik).
- **Hiány: nem találtunk friss, elsődleges forrásból származó, konkrét számszerű határidőt** (pl. "X nap/hónap") a mentésekből való törlésre sem az ICO, sem az EDPB anyagában — ezt a `megallapitasok.md` 6.3 pontjában kifejezetten "nincs ilyen" (evidence of absence) jelleggel rögzítettük, mert az EDPB kifejezetten kimondja, hogy egységes iránymutatás **jelenleg nincs**, és ennek megalkotását csak "megfontolja" a jövőben.
- **Hiány: a német Datenschutzkonferenz (DSK) konkrét, névvel azonosítható 2024-es "Positionspapier"-ét, amelyre a másodlagos (heise.de, bits.gmbh) német nyelvű cikkek hivatkoznak, nem sikerült elsődleges forrásból (datenschutzkonferenz-online.de) azonosítani és letölteni** — a keresés csak a témában született blogbejegyzéseket és egy másik témájú (tudományos kutatási célú adatkezelésről szóló) DSK-dokumentumot hozott fel. **Ez evidence of absence jellegű bizonytalanság**: lehet, hogy a dokumentum létezik, de nem került elő a keresési kísérletekben, vagy lehet, hogy a német sajtó egy még nem hivatalosan publikált/tervezet állapotú anyagra hivatkozik. Ezt a hiányt nem pótoltuk másodlagos (T3) forrásból való idézettel, mert a feladat kifejezetten elsődleges forrást kért a 6. kérdésnél.



---

# sq05 — A mentés mint cserélhető komponens: programozási minták

# Hiányok — sq05

Amit nem sikerült (teljesen) megtudni, és hogy ez „nincs ilyen” (evidence of absence) vagy „nem találtuk meg” (absence of evidence, a kutatás korlátai miatt).

## 1. Mért/számszerűsített esettanulmány korai absztrakció káráráról

**Kérdés:** „Van-e mért vagy dokumentált eset, ahol a korai absztrakció konkrét kárt okozott?”

**Státusz: nem találtuk meg** (nem „nincs ilyen”). Dedikált `WebSearch` kereséseket futtattam kifejezetten erre (`documented case study premature abstraction cost postmortem…`, `Sandi Metz "wrong abstraction"…`), és találtam **kvalitatív, jól dokumentált mintázatokat** (Sandi Metz „The Wrong Abstraction” esszéje — lépésről lépésre leírt romlási minta; a Borg-projekt kb. egy évtizedes története, ahol a hiányzó absztrakció miatt egy teljes főverziót kellett új réteggel kiegészíteni). **Egyik sem tartalmaz azonban számszerűsített kárt** (pl. „X mérnökóra”, „Y hetes csúszás”, konkrét dollárösszeg). Ez valószínűleg azért van, mert az ilyen belső költség-adatokat cégek ritkán publikálják nyilvánosan, konkrétan erre a kérdésre kihegyezve — de nem zárható ki, hogy alaposabb, fizetős szoftvermérnöki adatbázisokban (pl. akadémiai esettanulmány-gyűjtemények) van ilyen, amit ez a kutatás nem ért el.

## 2. GoF Bridge minta — összevetés a Strategy-vel

**Kérdés:** a Strategy és a Bridge minta explicit GoF-szintű megkülönböztetése (mivel a mentési cél absztrakciója felületesen mindkettőre hasonlíthat).

**Státusz: nem találtuk meg**, technikai okból. A letöltött GoF-könyv PDF-jét `pdftotext -layout`-tal alakítottam szöveggé; a Strategy-fejezet (315–321. o.) tisztán kinyerhető volt, de a Bridge-fejezet keresésekor (`grep "^Bridge$"`, `grep "decouple an abstraction"`) **nem találtam találatot** a konvertált szövegben — valószínűleg a kétoszlopos/ábrás oldal-elrendezés miatt a `pdftotext` másképp tördelte azt a fejezetet. **Ez a fejezet biztosan létezik a könyvben** (ez tehát „nem találtuk meg”, nem „nincs ilyen”), csak ennek a kutatásnak a technikai kinyerési lépése nem érte el. A `megallapitasok.md`-ben ezért nem szerepel GoF-szintű Strategy-vs-Bridge összevetés — csak a Strategy önmagában dokumentált.

## 3. Kopia és Duplicati dedikált „új backend írása” fejlesztői útmutató

**Kérdés:** van-e a Kopiánál és a Duplicatinél az rclone `CONTRIBUTING.md`-jéhez („Writing a new backend”) hasonló, dedikált, írott útmutató harmadik féltől érkező backend-hozzájárulóknak?

**Státusz: nem néztük meg kifejezetten** — ez a kutatás csak a két projekt backend-*interfészét* (forráskód) és a felhasználói dokumentációt (repository-lista) kereste meg, nem futtattam külön keresést a `CONTRIBUTING.md`/fejlesztői wiki oldalaikra. Nem állítható tehát sem az, hogy van ilyen, sem az, hogy nincs — ez explicit **kimaradt kutatási terület**, nem megválaszolt kérdés.

## 4. A Refactoring könyv (Fowler & Beck, 2. kiadás) 58. oldalának közvetlen ellenőrzése

**Kérdés:** a „rule of three” Don Roberts-idézet pontossága.

**Státusz: közvetett módon megerősítve, nem elsődleges forrásból közvetlenül.** A könyv online (O'Reilly Learning) változata regisztrációt/fizetős hozzáférést igényel, amit ez a kutatás nem tudott elérni. **Két, egymástól független, T3-as (blog, illetve GitHub-jegyzet) forrás szó szerint megegyezően** idézi a passzust ugyanarról az oldalról (58.) — ez erős, de nem T1-es megerősítés. A `megallapitasok.md`-ben ezt a claim-et emiatt **Közepes**, nem **Magas** megbízhatósági szinttel jelöltem.

## 5. Bacula: miért nem indítható a Restore Job a schedulerrel — az indoklás forrása

**Státusz: a tény T1-dokumentált, az indoklás a kutatás következtetése, nem idézett forrás állítása.** A Bacula dokumentációja kimondja a *tényt* („Restore jobs cannot be automatically started by the scheduler”), de nem fejti ki explicit prózában, *miért* van ez így. A `megallapitasok.md` 6.2 pontjában megadott indoklás („a restore emberi döntést igényel: melyik snapshotot, melyik fájlokat”) egy **ésszerű, a dokumentum kontextusából levont következtetés**, nem szó szerinti Bacula-állítás — ez ott explicit jelölve van („Az indoklás implicit a szövegből olvasható ki”).

## 6. Elsődleges forrás a Repository minta backup-kontextusbeli kritikájára

**Kérdés:** van-e olyan elsődleges/szakmai forrás, ami *kimondottan* kritizálja a Repository mintát mint félrevezető analógiát backup-rendszerekre?

**Státusz: nincs ilyen** (a kutatás keretein belül) — ez a kutatás nem talált egyetlen forrást sem, ami ezt a konkrét összevetést (Repository vs. backup-target) tárgyalná. A `megallapitasok.md` 2.3 pontjában szereplő érvelés ezért kifejezetten **saját következtetésként** van jelölve, a Repository-minta saját (Hieatt/Mee) T1-definíciójából levezetve, nem egy külső kritikus forrásból idézve. Ez fontos különbség: itt nem arról van szó, hogy „nem találtuk meg” egy létező kritikát, hanem hogy ezt a konkrét kérdést valószínűleg senki nem publikálta még ilyen formában — a Repository mintát tipikusan ORM/DDD kontextusban tárgyalja a szakirodalom, nem backup-rendszerek kontextusában.

## 7. Duplicati és Kopia backend-számának pontos, hivatalos, egyetlen számjegyű összesítése

**Státusz: részleges.** A Duplicati hivatalos oldala 4 kategóriába sorolva kb. 25 néven nevezett célt listáz (nem ad összesített „N backend” számot); a Kopia oldal 8 natív célt nevesít + rclone-delegáció. Ezekkel szemben restic és rclone esetében a hivatalos forrás **explicit összesített számot** ad (restic: implicit 12 a felsorolt fejezetcímekből; rclone: „Over 70”). Vagyis Duplicati/Kopia esetén a szám a kutatás saját összeszámlálása a hivatalos listából, nem egy hivatalosan kimondott összesítő szám — ez methodológiai árnyalat, nem hiány, de érdemes jelölni.

## 8. Az "Only posixfs" korlátozás mértéke a borgstore-ban — teljes lista

**Státusz: részleges.** A borgstore README csak két konkrét képességet nevesít explicit „only posixfs”-ként (kvóta, jogosultság-ellenőrzés). Nem futtattam mélyebb forráskód-elemzést (pl. az egyes backend-fájlok — `sftp.py`, `rclone.py`, `s3.py` — tényleges implementációjának összevetését), ami esetleg további, nem dokumentált képesség-egyenlőtlenségeket tárna fel. Ez a jelenlegi állítás a README **saját, explicit kijelentésére** korlátozódik, nem egy teljes forráskód-audit eredménye.



---

# sq06 — Séma- és formátum-migráció motorfüggetlenül

# sq06 — Hiányok (amit nem sikerült megtudni)

Minden tétel jelöli, hogy **"nincs ilyen"** (a kutatás alapján valószínűsíthetően a
dolog egyszerűen nem létezik/nincs dokumentálva sehol), vagy **"nem találtuk meg"**
(létezhet, de ez a kutatási kör — időkorlátok, elérhetetlen forrás, degradált
egyágensű mód — nem jutott el hozzá).

---

### 1. Egyetlen, összesített Liquibase change-type × motor kompatibilitási mátrix
**Státusz: nem találtuk meg / valószínűleg nincs ilyen.**
A Liquibase minden egyes change type saját oldalán közöl "Database support" táblát
(l. `megallapitasok.md` 1.2), de nem találtunk egyetlen, az összes change type-ot és az
összes motort egyszerre keresztbe metsző, összesített hivatalos táblázatot. Ez azt
jelenti, hogy egy fejlesztőnek **változatonként külön kell ellenőriznie** minden egyes
change type-ot, amit használni akar egy adott motoron — nincs egy helyen látható
"gyorsképe" a teljes lefedettségnek. Nem zárható ki, hogy egy Liquibase Pro/Secure
fizetős doksi-terület tartalmaz ilyet, de a nyilvánosan elérhető referenciában nem
találtunk rá.

### 2. Flyway hivatalos, kimondott filozófiai állásfoglalás a motorfüggetlenség ellen
**Státusz: nem találtuk meg — valószínűleg nincs ilyen, kimondott formában.**
A megbízás kifejezetten kérdezte: "Kimondja-e valahol, hogy a migrációkat nem érdemes
motorfüggetlenné tenni?" Sem a jelenlegi (documentation.red-gate.com), sem az archivált
(flywaydb.org, Wayback Machine-en át elért) Flyway dokumentációban nem találtunk
egyetlen olyan mondatot sem, amely explicit ezt állítaná. A filozófia **hallgatólagos**:
a doksi egyszerűen sosem ígéri az absztrakciót, és a "plain SQL" megközelítést adottnak
veszi. Ez fontos különbség a Liquibase (ami legalább *megpróbál* absztrahálni, és
dokumentálja, hol nem sikerül neki) és a Flyway között (ami *meg sem próbálja*, de ezt
sem indokolja meg külön). Lehetséges, hogy egy régebbi (2015 előtti) flywaydb.org FAQ
oldal tartalmazott ilyet, de ezt nem sikerült megtalálni sem élőben, sem
Wayback-en (a közvetlen `faq.md` URL 404-et adott).

### 3. Drizzle ORM hivatalos állásfoglalása a dialektusváltásról
**Státusz: nincs ilyen — megerősített hiány.**
Alaposan átnéztük a Drizzle Kit teljes konfigurációs referenciáját (`drizzle-config-file`),
a `generate` és `migrate` parancsok doksioldalait, és a `migrations` alapfogalmi oldalt:
egyik sem tárgyalja, mi történik egy projekt meglévő migrációs előzményével, ha a
`dialect` mezőt megváltoztatják. Ezt egy **valódi és fontos hiánynak** tekintjük a
Drizzle dokumentációjában — nem csak arról van szó, hogy nem találtuk meg, hanem arról,
hogy egy jóhiszemű, célzott keresés (a Kit teljes doksi-fája + GitHub keresés) sem hozott
elő ilyen szakaszt. Amit találtunk helyette, egy harmadik féltől (MakerKit, T2) származó
gyakorlati recept, amely a migrációk teljes törlését/újragenerálását javasolja — ez
közvetve megerősíti, hogy nincs hivatalos konverziós útvonal.

### 4. Egy közös, absztrakt "Dialect" bázisosztály/interfész a Drizzle ORM forráskódjában
**Státusz: nincs ilyen (megerősítve negatív találattal).**
A `drizzle-orm/src/dialect.ts` fájl nem létezik a főágon (404 a
raw.githubusercontent.com-on) — a `PgDialect`, `SQLiteDialect` (és feltehetően
`MySqlDialect`, amit időhiány miatt nem töltöttünk le külön) egymástól függetlenül
definiált osztályok, nem egy közös TypeScript interfészt implementáló testvérek.

### 5. Rails hivatalos "így írj saját adaptert" doksi-oldal (Django SchemaEditor-oldal Rails-megfelelője)
**Státusz: nem találtuk meg — valószínűleg gyengébben dokumentált, nem feltétlenül
"nincs ilyen".**
A Django `docs.djangoproject.com/.../ref/schema-editor/` oldalának nincs pontos Rails
megfelelője a Rails Guides-on (guides.rubyonrails.org) — ezt nem néztük át kimerítően,
de a keresés nem hozott elő ilyen dedikált oldalt. A Rails dokumentáltsága ezen a ponton
inkább a forráskód-kommentekre és a meglévő adapterek mintakódjára támaszkodik. Ez a
kutatási kör nem zárja ki, hogy a Rails Guides valamelyik "Active Record and PostgreSQL/
MySQL/SQLite" fejezetében van erre vonatkozó rövid útmutatás — ezt egy következő
kutatási körben érdemes külön megnézni.

### 6. A W3C TAG "Must Ignore" kiterjesztési minta elsődleges forrása
**Státusz: nem találtuk meg (időkorlát miatt).**
Ian Robinson 2006-os cikke (l. `megallapitasok.md` 6.3) "David Orchard és Dare Obasanjo"
papírjaira hivatkozik a "Must Ignore" mintával kapcsolatban, konkrét URL nélkül a
letöltött szövegben. Ez egy releváns, negyedik névvel-ellátható minta lenne a
fájlformátum-verziózás témájában, de az elsődleges W3C TAG dokumentumot (feltehetően
"Versioning XML Languages", David Orchard, W3C TAG Finding) ez a kutatási kör nem érte
el — ezt egy következő kör priorizálhatja.

### 7. "REST in Practice" (2010) könyv tényleges tartalma a Tolerant Reader kifejezésről
**Státusz: nem találtuk meg (hozzáférési korlát miatt).**
A könyv (Webber/Parastatidis/Robinson, O'Reilly, 2010) megelőzi Fowler 2011-es
bliki-posztját, és Ian Robinson (a könyv egyik szerzője) már 2006-ban írt a schema
evolúcióról Fowler oldalán. Elviekben lehetséges, hogy a könyv már használja/definiálja
a "Tolerant Reader" kifejezést Fowler posztja előtt — ezt az Internet Archive
kölcsönzési korlátozása (l. `keresesek.md` végén) miatt **nem sikerült ellenőrizni**.
Ez azt jelenti, hogy a `megallapitasok.md` 6.3 pontjában adott végkövetkeztetés ("a
Tolerant Reader Fowler saját szerzeménye") **a Fowler-bliki mint elsődleges, nyilvánosan
elérhető, névvel ellátott közlés alapján áll**, de nem zárható ki 100%-osan, hogy a
kifejezés már korábban, a könyvben is szerepelt — ez explicit fenntartásként kezelendő.

### 8. Konkrét, megnevezett markdown/YAML **frontmatter**-specifikus (nem JSON/API)
rendszer a "lazy migration on read" mintára
**Státusz: részleges — nem találtunk tisztán "markdown YAML frontmatter" példát, csak
analóg (JSON/API-szintű) rendszereket.**
A megbízás kifejezetten markdown YAML fejlécekről kérdezett. A két legerősebb talált
példa (Jupyter nbformat, Kubernetes storage version) **nem markdown YAML frontmatter**,
hanem JSON dokumentum, illetve API-objektum szinten működik — bár szerkezetileg
(verziómező a dokumentumban + olvasáskori automatikus konverzió) pontosan az kért
mintát valósítják meg. Tiszta markdown-frontmatter példát (pl. Obsidian, Zettlr, Foam,
Jekyll) kerestünk, de nem találtunk **dokumentált, névvel megnevezhető** esetet, ahol
egy ilyen eszköz kifejezetten "frontmatter schema version + lazy migration" mintát
írna le a saját doksijában. Ez azt sugallja, hogy **a markdown-ökoszisztémában ez a
minta kevésbé explicit/dokumentált**, mint az API- vagy fájlformátum-szabványok (JSON,
Kubernetes YAML manifest) világában — ez önmagában is releváns megállapítás a
mentes-frissites tervezéséhez: **nincs kész, lemásolható "iparági sztenderd" recept
kifejezetten markdown frontmatterhez**, a csapatnak az analóg (nbformat/Kubernetes)
mintákból kell adaptálnia a saját megoldását.

### 9. Számszerű adat arról, hány projekt hagyta el a motorfüggetlen migrációt
**Státusz: nincs ilyen adat / nem találtuk meg.**
A GitLab-eset (l. `megallapitasok.md` 7.) egy jól dokumentált, konkrét eset, de nem
találtunk semmilyen **összesítő, számszerűsített** forrást (pl. felmérés vagy
esettanulmány-gyűjtemény) arról, hogy hány, vagy milyen arányú szoftverprojekt hagyta el
idővel a motorfüggetlen migráció-absztrakciót. Ez pusztán egyetlen (bár erős) eset,
nem statisztika — ezt explicit nem szabad általánosítani.

### 10. Liquibase vagy Flyway saját magának motorfüggetlen rétegének visszavonása
**Státusz: nincs ilyen / nem találtuk meg.**
A megbízás 7. kérdése arra is rákérdezett, van-e dokumentált eset, ahol egy **migrációs
eszköz gyártója saját magának a termékében** vonta volna vissza a motorfüggetlenséget.
Ilyet nem találtunk sem Liquibase-nél, sem Flyway-nél — mindkét eszköz a mai napig
fenntartja az eredeti architektúráját (Liquibase: change type-ok + database-support
táblák; Flyway: nyers SQL). A GitLab-eset egy **alkalmazás**, nem egy **migrációs
eszköz gyártójának** döntése — ez a különbség fontos, és a `megallapitasok.md` 7.2
pontjában explicit jelezve van.
