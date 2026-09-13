# Szintézis — mentés, helyreállítás és verziófrissítés

**Kampány:** `mentes-frissites` · 2026-09-12 · 6 kereső, párhuzamosan
**A döntések:** D-36 (mentés és helyreállítás), D-37 (verziófrissítés)

Ez a fájl a következtetéseket mondja ki. A forrásokat és a szó szerinti idézeteket a
`kivonat.md` tartalmazza, egységenként.

---

## A hat megállapítás, ami a két döntést eldöntötte

### 1. A futó SQLite mentése nem fájlmásolás — és a hivatalos ajánlás nálunk többet ad, mint kényelmet

Az SQLite dokumentációja kimondja a bukási módot: *„The backup copy then might contain some old
and some new content, and thus be corrupt."* Három biztonságos utat nevez meg, rangsor nélkül
(*„In no particular order"*).

A `VACUUM INTO` mellett nem a kényelme döntött, hanem ez a mondat:

> „all deleted content is purged from the backup, leaving behind no forensic traces"

**Ez pontosan a D-21 végleges törlésének felel meg.** Egy Backup API-val készült bájtmásolat a
már törölt tartalmat is átvinné a mentésbe — vagyis egy „véglegesen töröltük" kérés eredménye
ott maradna a mentésekben. A `VACUUM INTO` ezt magától megoldja.

A Backup API ellen egy második érv is szól, szó szerint a dokumentációból: *„If the backup process
is restarted frequently enough it may never run to completion and the backupDb() function may
never return."* Egy folyamatosan író szerveren ez nem elméleti.

### 2. A két adatbázis közös pillanatképére nincs megoldás — de nekünk nincs is rá szükségünk

Ez volt a kampány legkellemetlenebb kérdése, és a válasz egyértelműen **hiány**:

- Az SQLite saját többfájlos atomicitása (`ATTACH` + super-journal) **WAL módban nem működik**:
  *„If the main database is ':memory:' or if the journal_mode is WAL, then transactions continue
  to be atomic within each individual database file."*
- A Litestream **adatbázisonként teljesen független** replikációs folyamot futtat, kereszt-garancia
  nélkül.
- A vizsgált gyakorlati anyagok közül **egyetlen sem tárgyalja** ezt önálló problémaként.

**Nálunk viszont nincs kérdés, mert csak egy adatbázist mentünk.** Az index eldobható (D-03),
tehát ki sem kerül a mentésbe. Ez nem szerencse: a D-03 eldobhatósági döntése oldotta meg
előre ezt a problémát, mielőtt felmerült volna.

### 3. A markdown fájlok fájlszintű másolása nálunk biztonságos — a D-07 miatt

A mentőeszközök dokumentációi részletesen tárgyalják, mi történik, ha egy fájl a mentés alatt
változik, és a bevett válasz a fájlrendszer-pillanatkép (ZFS/Btrfs/LVM/VSS). A Btrfs
dokumentációja külön leszögezi, hogy *„A snapshot is not a backup"* — a pillanatkép eszköz,
nem cél.

**Nálunk ez a réteg nem kell.** A D-07/7 szerint minden írás ideiglenes fájlba megy, aztán atomi
átnevezés két fsync-kel. Egy fájl tehát **vagy a régi, vagy az új** — soha nem félkész. Egy
fájlszintű másolás így fájlonként mindig konzisztens állapotot lát.

Amit ez nem ad: hogy a fa **egésze** egyetlen pillanatot mutasson. Ezt elfogadjuk, mert a fájlok
között nincs tranzakció — mindegyik önmagában értelmes.

### 4. A frissítésnek nincs visszaútja, tehát a mentés nem javaslat, hanem feltétel

A Drizzle-nek **nincs visszagörgetése**. Ezt a kutatás nem a dokumentáció hallgatásából
következtette ki, hanem forráskódból igazolta: a migrátorban lévő `ROLLBACK` a **futó**
tranzakciót védi, nem visz vissza egy korábbi sémához. Nincs `down` migráció, nincs `undo`
parancs, és a nyitott közösségi kérés is ezt erősíti.

Hat migrációs eszköz dokumentációját néztük meg abból a szempontból, ajánlanak-e mentést:

| Eszköz | Mit mond |
|---|---|
| **SQLite** (ALTER TABLE) | felszólító módban: *„make backup copies of important databases prior to running this procedure"* |
| **Flyway** | *„a proper, well tested, backup and restore strategy… no migration script can break it"* |
| **Liquibase** | elhárítja: *„No, Liquibase does not back up any data before deploying any changesets."* |
| Rails, Django, Drizzle | **meg sem említi** |

**Következtetés:** ez nem olyasmi, amit egy könyvtár megold helyettünk. Ezért lett a D-37/2-ben
feltétel, nem javaslat — ez a rendszer egyetlen helye, ahol tiltunk, nem jelzünk.

### 5. Az index eldobhatósága a frissítést is egyszerűsíti — erre nem számítottunk

Ha az index sémája változik, **nem migrálunk: eldobjuk és újraépítjük.** Ez triviálisnak hangzik,
de a következménye nem az: **a séma-migráció kockázata kizárólag a felhasználói adatbázist
érinti.** Az FTS5 táblák, a triggerek és a beágyazás-tárolás — vagyis a séma bonyolultabb fele —
soha nem kerül migrációba.

Ez azért fontos, mert az FTS5 a migráció legkellemetlenebb része volna. A hivatalos dokumentáció
**egyáltalán nem tárgyalja** egy virtuális tábla oszloplistájának vagy tokenizálójának utólagos
megváltoztatását, javításra pedig egyetlen eszköz van, a teljes `rebuild` — az `integrity-check`
csak jelez, nem javít. Egy csapdát is kimond: *„creating the triggers does not copy existing
rows"* — a trigger létrehozása nem tölti fel visszamenőleg az indexet.

### 6. A cserélhetőségre kész, több forrásból igazolt válasz van

A felhasználó kérésére (ne legyen minden beégetve) a kutatás négy egymástól független mentőeszköz
forráskódját nézte meg, és **egybehangzó mintát talált**:

| Eszköz | Kötelező metódusok |
|---|---|
| restic `Backend` | 13 |
| Borg 2.0 `borgstore` | 12 |
| Kopia `Storage` | 12 |
| rclone `Fs`+`Info` | 11 |
| Duplicati `IBackend` | 10 |

**Tíz és tizenhárom között** — vagyis egy tároló-interfész „helyes" mérete egy tucat körül van.
A variánsok nem a magban laknak: az rclone-nál 26 külön nevesített **opcionális** interfész van,
és mind az öt eszköz **explicit jelzőkkel** teszi láthatóvá a képesség-különbségeket
(`HasAtomicReplace`, `HasFlakyErrors`, `PartialUploads`, „quota support (only posixfs)").

**Egyik eszköz sem próbálja elrejteni vagy egységesíteni ezeket a különbségeket.** Ez a
legfontosabb tanulság a D-36/6-hoz, és pontosan egybevág azzal, amit a D-34 az adatbázis-illesztőnél
már kimondott: amit egy réteg nem tud hitelesen elrejteni, azt nem is próbálja.

A portvágás szabályára Cockburn eredeti cikke szó szerint válaszol — és ez a projektben korábban
már felmerült kérdés:

> „Their shift in design was to architect the system's interfaces by purpose rather than by
> technology, and to have the technologies be substitutable (on all sides) by adapters."

Vagyis **egy** „mentési cél" port, mögötte adapterek — nem külön port a lemeznek és külön az
objektumtárnak. Cockburn saját preferenciája összesen 2–4 port egy rendszerben.

---

## Az ellensúly: mikor árt az absztrakció

A felhasználó absztrakciót kért, és a kutatás feladata volt megkeresni az ellenérveket is.

Fowler saját szövege **kiveszi ezt az esetet a YAGNI hatóköréből**:

> „Yagni only applies to capabilities built into the software to support a presumptive feature,
> it does not apply to effort to make the software easier to modify."

Vagyis egy **kimondott** tervezési követelmény nem „feltételezett jövőbeli igény". A kérdés tehát
nem az, hogy legyen-e réteg, hanem hogy **milyen szűk** legyen. Innen jön a D-36/5 döntése:
a port megvan, de most **egy** adaptert szállítunk.

A „rule of three" eredeti értelmezése ezt támogatja: Roberts megfigyelése rendszer-szinten arról
szólt, hogy egy komponens **több konkrét alkalmazás után** bizonyul ténylegesen újrafelhasználhatónak.
Sandi Metz pedig a fordított kockázatot írja le: *„duplication is far cheaper than the wrong
abstraction"* — egy rosszul bevált absztrakciót vissza kell vonni, nem feltételekkel foltozni.

**És van egy dokumentált eset a hiányzó absztrakció áráról is:** a BorgBackup egy évtizedig
tudatosan nem épített tároló-absztrakciót, mert a repository-formátuma (append-only szegmens-log,
zárolás átnevezéssel) nem tette lehetővé olcsón. Amikor a 2.0-ban a formátumot megváltoztatták,
az absztrakció (`borgstore`) azonnal bevezethetővé vált. **Az absztrakció helye tehát a formátum
döntésén múlt, nem azon, hogy „jó gyakorlat"-e.**

---

## Ahol a szakma nem ad választ

**A méretünkre nincs ajánlás.** Egyetlen hivatalos vagy mért forrás sem szól néhány felhasználós,
néhány ezer fájlos rendszerről — sem gyakoriságra, sem helyreállítás-próbára. A ténylegesen
kormányzati szervek (CISA, NCSC) **szándékosan kerülik** a számot; az egyetlen konkrét ajánlás
(CIS: heti mentés, negyedéves visszaállítás-próba) a saját specifikációja szerint sem kötelező
kis szervezeteknél.

**Nincs mért idő a mentésre.** Az SQLite dokumentációja egyetlen teljesítményszámot sem közöl sem
a Backup API-ra, sem a `VACUUM INTO`-ra, és megbízható közösségi mérést sem találtunk méret
szerint.

**Nincs mért idő a beágyazások újraszámítására.** Az **árra** van adat (elhanyagolható), az
**időre** nincs — pedig a visszaállítás tényleges hosszát ez dönti el.

**A visszaállított jogosultságokra egyetlen forrás sem tér ki.** Az ICO és az EDPB részletesen
tárgyalja a személyes adat törlését a mentésekben, de azt sehol nem, hogy egy visszaállítás
visszahozhat-e egy visszavont jogosultságot. A D-36/12 a törölt **bejegyzésekre** megoldás; a
jogosultságokra nem az, és ezt a döntés ki is mondja.

**A „3-2-1 szabály" nem szabvány.** Egy 2005-ös fényképész-könyvből ered, a CISA ma is hirdeti,
de a NIST vonatkozó szabványa **egyszer sem említi** — helyette RPO/RTO kockázatalapú
paramétereket használ. Aki szabványként hivatkozik rá, téved.

---

## Amit a kampány a korábbi döntésekhez hozzátett

- **D-03** (az index eldobható): ez a döntés két külön problémát old meg előre — a két adatbázis
  mentés-konzisztenciáját és a séma-migráció kockázatát. Egyik sem volt látható, amikor megszületett.
- **D-07** (atomi írás): ez teszi biztonságossá a markdown fa fájlszintű mentését. Szintén nem
  ezért született.
- **D-21** (végleges törlés): a `VACUUM INTO` „no forensic traces" tulajdonsága ezt terjeszti ki
  a mentésekre is.
- **D-34** (adatbázis-illesztő): a D-36/6 ugyanazt a szabályt viszi tovább a mentésre — képességet
  jelzünk, nem rejtünk el. A D-37/7 pedig a migrációra: **képességre kérdezünk, nem motornévre**,
  ahogy a Django (~94 jelző) és a Rails (40 predikátum) teszi, és nem ahogy a Liquibase.
