# Ellentmondások — mentés és verziófrissítés

Ahol a források egymásnak ellentmondanak, és mi a feloldás.



---

# sq01 — Fájl-alapú tartalom mentése és helyreállítása

# SQ01 — Ellentmondások és feloldásuk

## 1. "Snapshot" — marketingkifejezés vs. valódi fájlrendszer-pillanatkép

**Az ellentmondás:** A restic a mentés eredményét "snapshot"-nak nevezi ("The contents of a directory at a specific point in time is called a 'snapshot' in restic" — restic hivatalos dok., T1). Ezzel szemben az OpenZFS hivatalos man page-e sokkal szigorúbb, formális definíciót ad ugyanerre a szóra: "Snapshots are created atomically. That is, a snapshot is a consistent image of a dataset at a specific point in time; it includes all modifications to the dataset made by system calls that have successfully completed before that point in time" (T1).

**Feloldás:** A két "snapshot" **nem ugyanazt jelenti**. A restic snapshot egy **logikai, alkalmazásszintű** fogalom: a mentési folyamat végén létrejövő, névvel ellátott állapotrögzítés — de maga a beolvasás (Linuxon, VSS nélkül) **nem atomi**, fájlonként, időben elhúzódva történik, tehát ha a mentés 10 percig tart, az elején és végén olvasott fájlok "keveredhetnek" egy inkonzisztens együttes állapotba. A ZFS snapshot ezzel szemben **fájlrendszer-szintű, rendszerhívás-atomi** művelet: egyetlen pillanatban rögzíti a teljes datasetet. **A gyakorlati következtetés:** ha egy rendszer valódi, teljes-fa-szintű pillanatkép-konzisztenciát akar, a restic/Borg/rsync típusú eszközöket egy alatta futó fájlrendszer-pillanatképpel (ZFS/Btrfs/LVM/VSS) kell kombinálni — ezt maguk a Borg-dokumentáció (LVM-példa) és a restic-dokumentáció (VSS) is alátámasztják, csak más-más platformon.

## 2. NIST: "évente teszteld" vs. "szervezet döntse el a gyakoriságot"

**Az ellentmondás:** A NIST SP 800-34 Rev. 1 fő szövege (3.2 fejezet) kimondja: "The plan recovery capabilities and personnel shall be **tested annually**." Ezzel szemben ugyanennek a dokumentumnak a Függelék E-jében szereplő formális CP-9(1) kontroll-szöveg így fogalmaz: "The organization tests backup information **[Assignment: organization-defined frequency]** to verify media reliability and information integrity" — vagyis nem ad fix számot, a szervezetre bízza.

**Feloldás:** Ez nem valódi logikai ellentmondás, hanem **két különböző absztrakciós szint** a dokumentumon belül. A "tested annually" az **általános kontinuitási terv egészére** (ISCP — teljes terv, személyzet, eljárások) vonatkozó minimumkövetelmény. A CP-9(1) egy **specifikus technikai biztonsági kontroll** a NIST SP 800-53 katalógusból, amit a szervezetek kockázatalapon paraméterezhetnek ("assignment" mező — ez a NIST kontroll-katalógusok bevett mintája, sok más kontrollnál is így működik). A gyakorlatban ez azt jelenti: **legalább évente mindenképp legyen egy teljes körű teszt**, de a konkrét mentés-visszaállítási tesztek gyakoriságát (ami lehet ennél sűrűbb) a szervezet saját RPO/RTO-kockázatértékelése alapján állapítja meg.

## 3. CISA aktívan hirdeti a 3-2-1 szabályt, a NIST formális szabványa nem említi

**Az ellentmondás:** A CISA (US kiberbiztonsági ügynökség) hivatalos, közönségnek szóló oldalain a "3-2-1" kifejezést név szerint, kiemelve használja. A NIST SP 800-34 Rev. 1 (a szövetségi informatikai rendszerek hivatalos kontinuitástervezési szabványa) a teljes dokumentumban **egyszer sem** említi ezt a kifejezést.

**Feloldás:** Nem tartalmi ellentmondás, hanem **műfaji különbség**. A CISA idézett oldalai **kisvállalkozásoknak és önkormányzatoknak szóló, közérthető oktatóanyagok** — ezek célja egy könnyen megjegyezhető ökölszabály terjesztése. A NIST SP 800-34 egy **formális, szövetségi rendszerekre kötelező technikai szabvány**, amely szándékosan kerüli a leegyszerűsített ökölszabályokat, helyette kockázatalapú, szervezetre szabott paramétereket (RPO, RTO, MTD) használ. A két dokumentum különböző célközönségnek, különböző absztrakciós szinten kommunikál ugyanarról a mögöttes elvről (több másolat, több hely, több adathordozó) — az egyik ezt "3-2-1"-be sűríti, a másik formális kontrollparaméterekbe.

## 4. "A pillanatkép nem mentés" vs. "a pillanatkép jó módszer konzisztens mentésre"

**Az ellentmondás (látszólagos):** A Btrfs hivatalos dokumentációja kimondja: "A snapshot is not a backup" — ugyanakkor ugyanez a dokumentáció (és a Borg dokumentációja is, LVM-példával) azt is mondja, hogy a pillanatkép "jó módszer" ("this is a good method") a konzisztens mentéshez.

**Feloldás:** Ez nem ellentmondás, csak felületesen tűnhet annak. A pontos állítás: a pillanatkép **önmagában** (mint egyetlen védelmi réteg, más adathordozón lévő másolat nélkül) nem mentés, mert ugyanazon a fizikai tárolón, ugyanazokat az adatblokkokat osztja meg az eredetivel (COW — copy-on-write miatt), tehát egy lemezhiba mindkettőt tönkreteheti. Ugyanakkor a pillanatkép **eszközként, egy nagyobb mentési folyamat egy lépéseként** ("to fix the state of a filesystem for making a full backup without anything changing underneath it" — szó szerint a Btrfs-dokumentációból) kiválóan alkalmas arra, hogy a tényleges mentőprogram (Borg, restic, rsync) egy konzisztens, nem változó bemenetből dolgozhasson. A két állítás tehát ugyanabból a dokumentumból, egymást kiegészítve, nem cáfolva szerepel.

## 5. A 3-2-1 szabály eredete — Krogh saját szavai vs. az attribúció széles körű elterjedtsége

**Az ellentmondás:** Az iparágban (backup-podcastok, gyártói blogok) szinte egyöntetűen Peter Krogh-nak tulajdonítják a "3-2-1" kifejezés megalkotását — ugyanakkor sem a Wikipedia "Backup" cikke, sem Krogh saját Wikipedia-életrajza nem erősíti meg ezt az állítást, és Krogh maga is relativizálja saját szerepét ("He didn't invent the idea of three copies and offsite backup, but he did distill it down to what we now refer to as the 3-2-1 rule").

**Feloldás:** Nincs valódi tartalmi ellentmondás, csak **forráshiányosság**. Krogh saját nyilatkozata (T2, közvetlen interjú) tulajdonképpen **pontosan megegyezik** azzal, amit egy körültekintő enciklopédikus forrás mondana: nem ő találta ki az alapelvet, csak ő adta neki ezt a tömör, mára kanonikussá vált formát egy 2005-ös fényképész-szakkönyvben. A Wikipedia hallgatása erről nem cáfolat, csak azt jelzi, hogy ez az attribúció **nem ment át enciklopédikus szerkesztői ellenőrzésen** — vagyis inkább iparági szájhagyomány/legenda szintjén él, mint dokumentált történeti tényként. A kutatás ezt **T2-es, egyetlen közvetlen forrásra visszavezethető** állításként kezeli, nem T1-es, megkérdőjelezhetetlen tényként.

## 6. Nincs valódi ellentmondás a mentési gyakoriság kérdésében — csak eltérő konkrétsági szint

**Megjegyzés (nem ellentmondás, de érdemes rögzíteni):** A CISA/NCSC (kormányzati) tudatosan **nem** ad konkrét számot a mentési gyakoriságra ("rendszeres, automatikus"), míg a CIS Controls (nonprofit, de kvázi-szabványos szervezet) igen, konkrétan "heti" gyakoriságot ír elő. Ez nem azért van, mert a két forrás egymásnak ellentmondana, hanem mert **különböző dokumentum-típusok**: a kormányzati oldalak széles közönségnek szóló, minden szervezeti méretre alkalmazható általános tanácsot adnak, míg a CIS Controls egy tételes, auditálható biztonsági keretrendszer, aminek muszáj számot adnia, hogy mérhető/ellenőrizhető legyen. A kutatás ezt a különbséget a `megallapitasok.md` 5. szakaszában részletesen tárgyalja, itt csak jelezzük, hogy tudatosan nem soroltuk fel "ellentmondásként", mert nincs tényleges cáfolat egyik oldalon sem.



---

# sq02 — Futó SQLite adatbázis biztonságos mentése

# sq02 — Ellentmondások és feloldásuk

## 1. "Checkpoint + `cp` a fő fájlt" mint mentési technika: közösségi ajánlás vs. a hivatalos "3 biztonságos módszer" listája

**A feszültség:** A SQLite hivatalos `howtocorrupt.html` oldala kifejezetten **három** módszert nevez meg biztonságosként élő adatbázison ("In no particular order"): `sqlite3_rsync`, `VACUUM INTO`, Backup API. A sima fájlmásolás (`cp`) csak akkor "biztonságos" a dokumentáció szerint, ha **nincs folyamatban tranzakció** a másolás pillanatában — ezt a feltételt egy folyamatosan futó, konkurens szerveren nehéz garantálni.

Ezzel szemben egy SQLite fórum hozzászóló (T3, [forum/info/796a192a95ac35b9](https://sqlite.org/forum/info/796a192a95ac35b9), anonim, 2022-07-17) egy gyakorlati megoldást ajánl, ami **nem** szerepel a hivatalos 3-as listán:
> "while in WAL mode, do a FULL Wal checkpoint. After which you can copy the main db file, this is a pristine snapshot of the db status right after the checkpoint (as long as no other checkpoints are attempted while the file is being copied, you might want to disable auto checkpoint temporarily if it is on right before you do this)"

**Feloldás:** Ez **nem valódi ellentmondás**, hanem eltérő megbízhatósági szint. A "checkpoint + `cp`" technika helyes elméleti alapon nyugszik (egy sikeres `FULL`/`RESTART`/`TRUNCATE` checkpoint után a fő fájl valóban tartalmazza az összes addigi commitot), **de** a helyesség fenntartása teljes egészében **kézi fegyelmen** múlik: az auto-checkpointot ki kell kapcsolni, és semmilyen más kapcsolat nem írhat/checkpontolhat, amíg a `cp` fut — ezt a SQLite semmilyen szinten nem kényszeríti ki vagy ellenőrzi. Ezzel szemben a hivatalos 3 módszer (Backup API, `VACUUM INTO`, `sqlite3_rsync`) mindegyike **saját maga koordinálja** a zárolást/konzisztenciát a SQLite-motor szintjén, függetlenül attól, hogy az operátor fegyelmezett-e. A gyakorlatban tehát a fórumos technika **működhet**, de magasabb üzemeltetési kockázattal jár, és pontosan ezért nem szerepel a hivatalos, "garantáltan biztonságos" listán. Egy másik SQLite fórum-hozzászóló (Simon Slavin, ugyanabban a szálban) ezt közvetve meg is erősíti, amikor leszögezi, hogy csak a tranzakciók lezárása és az írások felfüggesztése ad valódi garanciát, nem pusztán egy időzített checkpoint.

## 2. Litestream WAL2-kompatibilitás — állítás vs. megerősítés hiánya

**A feszültség:** Az Oldmoe blog (T3, [oldmoe.blog](https://oldmoe.blog/2024/04/30/backup-strategies-for-sqlite-in-production/)) a Litestream hátrányai között felsorolja:
> "Potentially not compatible with the more advanced WAL2 mode."

A hivatalos Litestream-dokumentáció egyik általunk lekért oldala (`how-it-works`, `tips`, `alternatives`, `guides/directory`) sem említi a WAL2-t egyáltalán — sem megerősítésként, sem cáfolatként.

**Feloldás: nem tudjuk feloldani, nyitva hagyjuk.** Mivel a hivatalos oldalak egyszerűen hallgatnak a témáról, nem tudjuk megállapítani, hogy ez elavult (a blogbejegyzés 2024-04-30-i, azóta a Litestream v0.5-re frissült és alapvetően átdolgozta a WAL-kezelését, ld. `megallapitasok.md` 5. szakasz), vagy ma is releváns korlátozás. Mivel a WAL2 egyébként is kísérleti, nem a fő SQLite-ágba integrált funkció, ez valószínűleg nem kritikus a jelen kampányra — de expliciten hiányként (lásd `hianyok.md` 8. pont), nem megerősített tényként kezeljük.

## 3. `BEGIN DEFERRED` vs. `BEGIN IMMEDIATE` a kézi `cp`+tranzakció technikában — önkorrekció egy forráson belül

**A feszültség:** Az Oldmoe blog eredeti szövege a kézi `cp`-alapú módszerhez `BEGIN DEFERRED`-et ajánl a WAL-fájl törlésének megakadályozására másolás közben. Egy kommentelő (aarondfrancis) megkérdőjelezte ezt:
> "Does begin deferred not run the risk of someone writing to the WAL file while you're copying it? Wouldn't you need to do begin immediate to ensure that the WAL file is pristine?"

A szerző válasza árnyalja (nem cáfolja, de pontosítja) az eredeti állítást:
> "Not, really, being deferred ensures the WAL file will not be truncated while you are reading from it. But you will miss any new data changes while you are reading. You will be basically reading a snapshot"

**Feloldás:** Ez nem két forrás közötti ellentmondás, hanem egy **forráson belüli önkorrekció/pontosítás**, amit érdemes megőrizni, mert rávilágít egy finomságra: a `BEGIN DEFERRED` megvédi a WAL-fájlt a **csonkolástól** (truncation) a másolás alatt, de nem zárja ki, hogy közben **új** commitok kerüljenek a WAL végére — ezeket a másolás egyszerűen nem fogja tartalmazni (a másolat egy korábbi, de önmagában konzisztens pillanatot tükröz, nem a "legfrissebb" állapotot). Ez összhangban van a hivatalos dokumentációval (a Backup API is pontosan így viselkedik: "a bit-wise identical copy of the source database as it was when the copying commenced"), tehát a végkövetkeztetés nem ellentmond a hivatalos anyagnak, csak a kézi technika egyik nem triviális részletét tisztázza.

## 4. A `cp --reflink=always` "~2 ms" mérése — kockázat a túláltalánosításra

**Nem forrásközi ellentmondás, hanem értelmezési csapda, amit explicit ki kell mondani:** Az Oldmoe blog mérése (~2 ms egy 440 MB-os és egy 4,4 GB-os fájl másolására is) igaz és valós mérés, **de kizárólag** a Btrfs Copy-on-Write reflink-másolásra vonatkozik, ahol a művelet lényegében csak fájlrendszer-metaadatot módosít, nem tényleges adatlapokat másol. Ha valaki ezt a számot általánosítaná a Backup API-ra vagy a `VACUUM INTO`-ra ("SQLite mentés ~2 ms bármekkora DB-n"), az **téves következtetés** lenne — azok a módszerek ténylegesen olvassák/írják/tömörítik a lapokat, tehát méretarányos I/O-idővel járnak. Ezt a `megallapitasok.md` 4. szakaszában és a `hianyok.md`-ben is explicit módon jeleztük, hogy elkerüljük ezt a lehetséges félreértést.

## 5. Litestream marketingszövege vs. saját technikai figyelmeztetései

**A feszültség:** A Litestream főoldala (`litestream.io/`) így fogalmaz:
> "No-worry backups — Continuously stream SQLite changes to your preferred cloud storage or local files. Quickly recover to your most recent replicated transaction if your server goes down."

Ezzel szemben a saját, technikai "Tips & Caveats" és "Alternatives" oldalai kifejezetten hangsúlyozzák a korlátokat:
> "During this time where data has not yet been replicated, a catastrophic crash on your server will result in the loss of data in that time window."
> "Sometimes Litestream can be overkill for projects with a small database that do not have high durability requirements."

**Feloldás:** Ez nem tényszerű ellentmondás, hanem tipikus **marketing-szint vs. technikai-dokumentáció-szint** eltérés, ami sok szoftver hivatalos oldalán megjelenik. A "No-worry" megfogalmazás a főoldal marketingszövege, míg a technikai oldalak (amelyeket a feladat módszertana szerint helyesen nyers HTML-ből, nem a főoldal összefoglalójából olvastunk ki) pontosan definiálják a korlátokat. A `megallapitasok.md`-ben a technikai oldalak (`tips`, `alternatives`) idézeteit tekintettük mérvadónak, nem a főoldal szlogenjét — ez alátámasztja a feladat azon módszertani kikötését, hogy a nyers HTML-t kell felhasználni, nem az automatikus összefoglalót, mert épp az ilyen árnyalatok (a "No-worry" szlogen mögötti, kevésbé csillogó technikai valóság) vesznek el egy leegyszerűsítő összefoglalóban.

## 6. Módszertani (nem faktuális) feszültség: a SQLite fórum tier-besorolása

Nem tartalmi ellentmondás, de érdemes rögzíteni: a SQLite hivatalos fórumát (`sqlite.org/forum`) a hivatalos SQLite-domainen futtatják, és gyakran maguk a SQLite core-fejlesztői/konzulensei (pl. Keith Medcalf, Larry Brasfield, Richard Hipp közeli munkatársai) válaszolnak rajta — ez sok kutatási protokollban T1-T2 közötti, "féighivatalos" forrásnak számítana. A feladat tier-definíciója szerint viszont ("T3 = fórum, blog, anekdota") szigorúan **T3**-nak kell besorolni, függetlenül a hitelességtől. Ebben a kutatásban a szigorúbb, szó szerinti definíciót követtük (fórum = T3), és emiatt minden fórumos idézetet **kizárólag** olyan helyen használtunk fel, ahol legalább egy T1-es hivatalos dokumentum-oldal is megerősítette ugyanazt az állítást (pl. a Backup API "restart" viselkedése egyszerre szerepel a `backup.html`-en/`c3ref/backup_finish.html`-en ÉS a fórumon) — kivéve a checkpoint+cp technikát és a kereszt-adatbázis "nincs bevett megoldás" konklúziót, ahol a fórum az egyetlen elérhető forrás, de ezt explicit módon jeleztük tier-jelöléssel.



---

# sq03 — Séma-migráció és verziófrissítés futó rendszeren

# sq03 — Ellentmondások és feloldásuk

## 1. Drizzle dokumentáció szövege vs. a tényleges CLI-funkciókészlet és forráskód

**Az ellentmondás:** A hivatalos „Migrations fundamentals" oldal (Option 4, futásidejű `migrate()` hívás)
kimondja:

> „This approach is widely used for monolithic applications when you apply database migrations during zero
> downtime deployment and **rollback DDL changes if something fails**."

Ez a mondat azt sugallja, hogy a Drizzle valamilyen módon támogatja a DDL-változtatások visszagörgetését hiba
esetén. Ezzel szemben:

- a hivatalos, kimerítő parancslista (`generate, migrate, push, pull, check, up, studio, export`) **nem
  tartalmaz** semmilyen `down`/`undo`/`rollback` parancsot;
- a forráskód (`sqlite-core/dialect.ts`) csak azt mutatja, hogy **egy adott migrációs futás** egyetlen
  tranzakcióban zajlik, és **a tranzakción belüli** hiba esetén SQL-szintű `ROLLBACK` történik — ez nem azonos
  egy korábbi séma-verzióhoz való visszaállással;
- a GitHub Issue #4005 („[FEATURE]: Reverse/Down Migrations") **nyitott feature-kérésként** él, ami önmagában
  bizonyítja, hogy a közösség és feltehetően a karbantartók is hiányként kezelik a funkciót;
- a GitHub Issue #2510 azt is dokumentálja, hogy **még ez a tranzakció-szintű rollback sem működött megbízhatóan
  minden esetben** egyes driver-kombinációknál.

**Feloldás:** A hivatalos mondat valószínűleg **nem a Drizzle Kit egy konkrét funkciójára**, hanem az
**alkalmazás-szintű deploy-folyamatra** utal általánosságban (pl. „ha valami elromlik, az alkalmazás egy korábbi
image-re és egy korábbi DB-mentésre áll vissza, azaz a *rendszer egésze* képes rollbackelni, nem maga a Drizzle
CLI"). Ezt a mondatot **nem szabad úgy érteni**, hogy létezik egy `drizzle-kit down` vagy hasonló parancs — ez
egyértelműen cáfolható a parancslistával és a forráskóddal. A jelentésben ezt a mondatot idézzük, de expliciten
jelöljük a kétértelműségét, és nem állítunk mögé konkrét funkciót.

## 2. Flyway „Undo Migrations" — marketing-percepció vs. tényleges elérhetőség

**Az ellentmondás:** A Flyway-t gyakran „migrációs eszköz beépített rollback-képességgel" hírben ismerik (mivel
az „Undo Migrations" funkció szerepel a fő dokumentációban, ugyanazon az „Migrations" fogalmi oldalon, mint a
sima migrációk, megkülönböztetés nélkül a bekezdés szintjén). A dokumentáció oldal maga is csak ennyit mond
elsőre: „Undo migrations are the opposite of regular versioned migrations."

**Feloldás — nem valódi ellentmondás, hanem elrejtett feltétel:** A részletes „Undo migrations" aloldal tetején
világosan jelölve van: **„EDITION: TEAMS"**. Ez azt jelenti, hogy a funkció **kizárólag a fizetős Flyway Teams
kiadásban** érhető el, az ingyenes Community kiadásban **nincs** beépített rollback. Ez fontos, mert egy felületes
olvasás (csak a „Migrations" koncepció-oldal, az „Undo" aloldal edition-jelölése nélkül) téves benyomást kelthet.
A jelentésben ezt explicit módon jelöltük mindkét idézetnél.

## 3. „Rollback = adat-visszaállítás" tévhit — Liquibase és Flyway is cáfolja

**Az ellentmondás/tévhit, amit tisztázni kell:** Könnyű azt hinni, hogy egy migrációs eszköz „rollback" vagy
„undo" funkciója egyenértékű a mentésből való visszaállítással (azaz visszahozza a törölt adatokat is).

**Feloldás — mindkét hivatalos forrás explicit módon cáfolja ezt:**

- Liquibase support-FAQ (WebFetch): „any changeset that either removes or deletes data either intentionally or
  indirectly will delete the data" — azaz a rollback **nem hozza vissza** a törölt adatot, csak a séma-szerkezetet
  állítja vissza.
- Flyway „Undo migrations" oldal: „Undo migrations assume the whole migration succeeded and should now be
  undone. […] They work for undoing schema changes but not so well for undoing data changes — If your versioned
  migration script contains destructive changes (drop, delete, truncate, …), then restoring both table and data
  in the undo script can be challenging unless that data is static."

**Ez nem forrásaink közötti ellentmondás, hanem egy fontos, mindkét eszköznél egybehangzóan hangsúlyozott
korlátozás**, amit a jelentésben (5.2 és 5.3 pontok) mindkét idézettel alátámasztottunk. Ez erősíti a
`megallapitasok.md` végkövetkeztetését: **egy valódi biztonsági mentés (fájl- vagy volume-szintű másolat) más
kategóriájú védelem, mint bármelyik eszköz beépített „rollback"-ja**, és a kettő nem helyettesíti egymást.

## 4. Docker Compose `version:` mező — deprecation ellentétben áll a 6. kérdés „bevett minta" feltételezésével

**A feszültség:** A kutatási kérdés (6. pont) azt feltételezte, hogy a „bevett minta" fájlformátum-verziózásra a
„verziómező a fájlban + lusta migráció olvasáskor" páros. A Docker Compose példája ezzel **részben szembemegy**:
itt a fejlesztők **explicit módon elhagyták** a verzió-alapú elágazást, és helyette egy „mindig legfrissebb
séma + engedékeny feldolgozás" stratégiát vezettek be — vagyis a `version:` mező ma már **nem** vált ki
migrációt, csak informatív, elavult jelzés.

**Feloldás — nem ellentmondás, hanem két legitim, egymás mellett létező stratégia:** A jelentés (6.3 és 6.5
pontok) ezt nem próbálja „beerőltetni" az eredeti feltételezésbe, hanem **külön, harmadik mintaként** mutatja be:
(A) verzió szerinti elágazó/konvertáló olvasás (nbformat), (B) verziómező az exportált fájlban, importáló dönt
(WXR), (C) a verziómező megszüntetése, egységes/engedékeny séma (Compose). A JSON Canvas (6.4) pedig egy negyedik,
„nincs is szükség verziómezőre, additív bővítéssel megoldható" esetet mutat. A jelentés ezt a sokszínűséget
explicit módon jelzi, nem egyetlen „a" bevett mintaként tálalja a kérdést.

## 5. Az „egy gépes rendszer nem igényli az expand-contractot" következtetés — nem egyetlen forrás mondja ki explicit módon

**Amit tisztázni kell, nehogy félreértésre adjon okot:** A `megallapitasok.md` 4.3–4.4 pontjaiban levont
következtetés (miszerint az easter-memory-systemhez hasonló, egy-példányos rendszereknél az expand-contract
minta teljes, formális alkalmazása felesleges bonyodalom) **nem egyetlen forrás szó szerinti kimondása**, hanem
**három különálló forrás (Fowler/Sadalage „evodb", Wellhausen tanulmány, és maga a Fowler „Parallel Change" oldal
alkalmazási példáinak jellege) együttes, konvergens olvasatából levezetett szintézis.** Egyik forrás sem mondja
ki szó szerint azt a mondatot, hogy „egy gépen felesleges az expand-contract" — de mindhárom, egymástól
függetlenül, ugyanabba az irányba mutat (lásd a pontos idézeteket a `megallapitasok.md`-ben). Ezt itt tisztázzuk,
nehogy a jelentés olvasója egyetlen forrásnak tulajdonítsa ezt az összegző állítást — ez a kutatás saját,
átlátható szintézise, nem egy talált idézet.

## 6. `PRAGMA foreign_keys` alapértéke — dokumentált bizonytalanság, nem forrásaink közötti ellentmondás

Az SQLite hivatalos dokumentációja maga jelzi a bizonytalanságot:

> „As of SQLite version 3.6.19, the default setting for foreign key enforcement is OFF. However, **that might
> change in a future release of SQLite**. […] To minimize future problems, applications should set the foreign
> key enforcement flag as required by the application and not depend on the default setting."

Ez nem két forrás közötti ellentmondás, hanem **maga a hivatalos dokumentáció explicit figyelmeztetése** arra,
hogy ne bízzunk semmilyen feltételezett alapértékben. A gyakorlati következmény az easter-memory-system 12-lépéses
tábla-migrációs kódjára nézve: **mindig explicit módon** kell kiadni a `PRAGMA foreign_keys=OFF`/`=ON`
parancsokat a migráció elején/végén, ne hagyatkozzon a kód a driver vagy az SQLite-verzió alapértelmezésére —
ezt a jelentés a 2.3 pontban külön kiemeli, éppen ez okból.



---

# sq04 — Mit kell menteni, és honnan tudjuk, hogy jó

# sq04 — Ellentmondások és feloldásuk

## 1. OWASP Secrets Management Cheat Sheet vs. NIST SP 800-57 — mentsük-e a titkokat?

**A látszólagos ellentmondás:**

- Az **OWASP Secrets Management Cheat Sheet** (T1) kifejezetten *javasolja* a titkok mentését: "**Backup: back up secrets to product-critical operations in separate storage (e.g., cold storage), especially encryption keys.**" — ez proaktívan a titkok mentését írja elő, nem a kihagyásukat.
- A **NIST SP 800-57 Part 1 Rev. 5** (T1) ezzel szemben azt mondja: "**if operations can be continued without the backup of keying material... it may be preferable not to save the keying material in order to lessen the possibility of a compromise**" — ez a *nem mentés* felé billenti a mérleget, ha lehetséges.

**Feloldás:** ez nem valódi ellentmondás, hanem **más-más kockázati célra optimalizált ajánlás, más-más titoktípusra**:

- A NIST anyaga *kriptográfiai kulcsokra* fókuszál, és kulcstípusonként differenciál (lásd a 7–8. táblázat: némelyik "No", némelyik "OK"). A NIST elve konkrétan azokra a kulcsokra vonatkozik, amelyek *újragenerálhatók* (pl. munkamenet-kulcsok, ephemeral kulcsok, RBG seed) — ezekre valóban azt mondja, ne mentsük.
- Az OWASP anyaga *operatív, üzletkritikus titkokra* (pl. adatbázis-jelszavak, harmadik fél API-kulcsok, "encryption keys" mint elsődleges titkosító kulcs) fókuszál, amelyek **nem triviálisan újragenerálhatók** — ha elvész egy ilyen kulcs, az egész titkosított adathalmaz olvashatatlanná válhat. Erre logikus a mentés.

**A közös nevező mindkét forrásban**, ami a valódi, megoldást adó elv: **"mentsd, ha a hiánya helyreállíthatatlan kárt (adatvesztést) okozna; ne mentsd, ha újragenerálható, és a mentés csak plusz kompromittálódási felület."** Az easter-memory-system esetére lefordítva: az embedding-szolgáltatás API-kulcsa (ami nélkül a rendszer nem tud új embeddinget generálni, de a *létező* adat nem válik olvashatatlanná tőle) inkább az "OWASP-eset" felé húz (érdemes menteni, védetten) — DE ez már értékelő állásfoglalás, amit a döntéshozónak kell meghoznia, nem a kutatás dolga eldönteni.

## 2. "Csendes adatromlás mennyire gyakori" — a CERN/NetApp-mérés vs. a Backblaze-féle AFR-szám félreérthetősége

**A látszólagos ellentmondás:** ha valaki csak felületesen keres rá a témára, könnyen összemossa a "lemez éves meghibásodási arányát" (Backblaze AFR, 2025: 1.36%) a "csendes bitkorrupció arányával" (CERN: 0.000000185%; NetApp: 0.66%/17 hónap egy adott lemez legalább egy checksum-eltérésére). Ezek nagyságrendekben különböző számok, és ha valaki a Backblaze 1.36%-ot idézné "ennyi az esély, hogy egy fájlom csendben megsérül" állításként, az **hibás lenne**.

**Feloldás:** ez nem a források közötti valódi ellentmondás, hanem egy **mérési tárgy (measurement target) különbség**, amit a `megallapitasok.md` 4.3 pontjában explicit külön is választottunk:

- A Backblaze-szám a **teljes meghajtó-meghibásodást** méri (a meghajtó lecserélésre kerül, working/failed bináris állapot).
- A CERN- és NetApp-szám a **néma, a hardver/szoftver által nem jelzett bitszintű korrupciót** méri, ami egy egyébként *működő, nem meghibásodottnak jelzett* lemezen történik.

A két jelenség részben független: egy lemez lehet "nem meghibásodott" (Backblaze szerint egészséges) és mégis hordozhat néma bithibát (CERN/NetApp értelemben). A helyes értelmezés: ezek **kiegészítő, nem helyettesítő** metrikák — mindkettő releváns kockázat, de különböző mechanizmusra és különböző védekezésre (RAID/redundancia a meghibásodás ellen, checksumolás/scrub a néma korrupció ellen).

## 3. ZFS scrub ajánlott gyakorisága — nincs egységes szám a forrásokban

**A látszólagos ellentmondás:** a hivatalos OpenZFS man page (`zpool-scrub.8`) nem ad konkrét számot, csak azt említi, hogy "weekly and monthly timer units are provided" (systemd-integráció) — vagyis mindkét gyakoriság hivatalosan támogatott, választás kérdése. Az Oracle Solaris ZFS Administration Guide viszont konkrét alapértelmezett számot ad: **30 nap**. Közösségi fórumokon (T3, nem idézett) gyakran látni "heti" ajánlást megbízhatatlanabb (fogyasztói) lemezekre.

**Feloldás:** ez **nem ellentmondás, hanem hiányzó egységes szabvány** — a scrub gyakorisága kifejezetten **kockázat-függő tervezési döntés**, amit maga a ZFS-ökoszisztéma sem egységesít egyetlen "helyes" számra. Az Oracle 30 napos alapértéke egy *konkrét termék alapbeállítása*, nem egy iparági konszenzus-minimum vagy -maximum. A helyes olvasat: **30 nap egy ésszerű, hivatalosan dokumentált kiindulópont, de nem az egyetlen "helyes" válasz** — a döntéshozó a lemez megbízhatósága és a helyreállítási kockázat alapján ettől eltérhet (rövidebbre, megbízhatatlanabb hardvernél).

## 4. GDPR / backup törlés — "azonnal kell törölni" vs. "a mentés integritása védendő"

**A látszólagos ellentmondás:** a GDPR Article 17(1) szó szerint "indokolatlan késedelem nélkül" ("without undue delay") törlést ír elő, ami első olvasatra azonnali, teljes törlést sugallna minden rendszerből, mentésekkel együtt. Ugyanakkor az EDPB 2026-os jelentése kifejezetten elismeri: "**Depending on the technical settings and risks, it might not always be advisable to modify or delete information from back-ups.**"

**Feloldás:** ez nem a jogszabály és a hatóság közötti ellentmondás, hanem **a hatóság (EDPB) saját, explicit értelmezési rugalmassága** a jogszabály gyakorlati alkalmazására — az EDPB nem mondja, hogy a törvény ne vonatkozna a mentésekre, hanem azt mondja, hogy a "indokolatlan késedelem nélkül" teljesíthető úgy is, hogy (a) az élő rendszerből azonnal törlünk, (b) a mentésben lévő adatot "beyond use" (ICO terminológiája) állapotba helyezzük — nem használjuk fel semmilyen célra —, és (c) a mentés a saját, előre meghatározott, dokumentált rotációs ütemterve szerint természetes úton semmisül meg (felülíródik/lejár). Ez a hatóságok (ICO, EDPB) által elfogadott, **de nem konkrét határidővel kvantifikált** megoldás — az ellentmondás feloldása maga is bizonytalan/nyitott terület, amit az EDPB kifejezetten további iránymutatás-igénylésként azonosít saját magának ("the EDPB may consider... providing more guidance"). **Ezt tehát nem lezárt ellentmondásként, hanem a hatóságok által is nyitottan kezelt kérdésként kell rögzíteni** a döntéshozó felé — nem javasolunk saját jogi értelmezést a nyitott kérdés lezárására.

## 5. "Származtatott adatot nem kell menteni" elv és az embedding-cache gyakorlat közötti feszültség

**A látszólagos ellentmondás:** az 1. kérdés fő elve szerint a derived (újraépíthető) adatot nem kell klasszikus mentésbe tenni. A 2. kérdés viszont azt mutatja, hogy a gyakorlatban mégis *cache-elik* (perzisztensen tárolják) az embeddingeket tartalom-hash alapján — ami tulajdonképpen egyfajta "mentés"-nek tűnhet ugyanarra a derived adatra.

**Feloldás:** ez nem valódi ellentmondás, hanem **terminológiai átfedés két különböző célú művelet között**:

- A **klasszikus mentés (backup)** célja: katasztrófa-elhárítás, egy teljes rendszerállapot visszaállítása egy másik időpontban/helyen.
- Az **embedding-cache** célja: *ismétlődő, felesleges munka elkerülése* a normál (nem katasztrófa) működés során — ha egy dokumentum tartalma nem változott, ne fizessünk/várjunk újra az embeddingért.

A kettő tehát különböző réteg: **egy cache-elt embedding-tár maga is lehet pusztán "derived és eldobható"** abban az értelemben, hogy ha elveszik, újra kiszámítható (csak pénzbe/időbe kerül) — miközben *napi/fejlesztési munkafolyamat szintjén* mégis érdemes megtartani/gyorsítótárazni, hogy ne kelljen minden egyes indexújraépítésnél az összes bejegyzést újra kifizetni/kiszámítani. A `megallapitasok.md` 2.3 pontja ezt a kétszintű logikát külön is kifejti: a "technikailag derived, biztonsággal eldobható" és a "gyakorlatilag érdemes cache-elni, mert drága újraszámolni" nem zárják ki egymást — egy jó tervezés mindkettőt figyelembe veszi (a mentési stratégia szempontjából eldobható, de a napi működés szempontjából érdemes tartalom-hash alapon perzisztálni, hogy ne kelljen feleslegesen újraszámolni).



---

# sq05 — A mentés mint cserélhető komponens: programozási minták

# Ellentmondások — sq05

Ahol a források egymásnak (vagy önmaguknak, időben) ellentmondanak, és mi a feloldás.

## 1. „Miért nincs Borgnak object storage backendje” — a válasz megváltozott alóla

**Az ellentmondás:** a Borg 1.x hivatalos FAQ-ja és architektúra-dokumentációja egy **szerkezeti, technikai** indoklást ad arra, miért nincs objektumtár-backend: „Borg is doing nothing special in the filesystem, it only uses very common and compatible operations (**even the locking is just 'rename'**)” [T1] — egy olyan műveletre (atomikus rename) hivatkozva, amit egy PUT/GET/LIST objektumtár API nem biztosít. Eszerint a hiány **elvi, tartós** akadálynak tűnik. Ezzel szemben a Borg **2.0 hivatalos kiadási jegyzéke** (ugyanaz a projekt!) bejelenti a `borgstore` réteget, ami kifejezetten **`s3:`/`b2:` backendeket** is támogat [T1].

**Feloldás:** nincs valódi logikai ellentmondás, csak **időbeli fejlődés egy meg nem változtatott premissza miatt**. A korlát sosem az volt, hogy „egy mentőeszköz elvileg nem tud objektumtárral dolgozni” — hanem hogy **a Borg 1.x konkrét repository-formátuma** (append-only szegmens-log, szerver-oldali kompakció, ami meglévő szegmensfájlok újraírását igényli) feltételezett egy megosztható, véletlen-elérésű, zárolható fájlrendszert. A Borg 2.0 **megváltoztatta a repository-formátumot** (a csomagok kliens-oldalon állnak össze: „packs are assembled client-side, then stored into the repository, enabling efficient usage of cloud storage” [T1]) — ezzel a random-access-igény megszűnt, és az absztrakció **azonnal, könnyen** bevezethetővé vált. **Tanulság erre a projektre:** a „lehet-e absztrahálni a tárolási célt” kérdés nem elvi/architektúra-filozófiai kérdés, hanem **a választott tárolási formátum (fájlfa, hozzáfűzős napló, SQLite) konkrét hozzáférési mintájának** a függvénye. Mivel ennek a rendszernek a mentendő adatai (markdown fájlfa, audit napló, SQLite) natívan is fájlrendszer-szemléletűek, ez kedvezőbb helyzet, mint a Borg 1.x szegmens-kompakciós formátuma volt.

## 2. A „rule of three” népszerű (Wikipédia-féle) és eredeti (Roberts-féle) olvasata

**Az ellentmondás:** a Wikipédia (T3) úgy fogalmazza meg a szabályt, hogy „két hasonló kódrészlet nem igényel refaktorálást, de három már igen, és ki kell emelni egy **új eljárásba**” — vagyis egy **függvény-szintű**, kód-duplikáció elleni heurisztika. Az eoinnoble.com alapos forráskutatása (T3, de közvetlenül idézi a Fowler-könyvet és nyomon követi Roberts 1996-os társszerzős cikkét egy 1988-as workshopig) ezzel szemben azt állítja: „I am struck by how the Wikipedia article has taken quite generic advice from Roberts and transformed it into a recommendation about when to write 'a new procedure' […] Roberts is interested in **refactoring across entire systems**, code abstractions that are only apparent after the creation of **multiple related applications**.” [T3]

**Feloldás:** mindkét olvasat „igaz”, csak más **granularitási szinten**. A mai, hétköznapi refaktorálási gyakorlatban a szabályt valóban függvény/metódus-szinten használják (ez a Wikipédia-féle, elterjedt olvasat). Roberts eredeti, Johnsonnal közösen írt megfogalmazása viszont **keretrendszer/rendszer-szintű újrafelhasználhatóságról** szól: egy komponens csak **több (≥3) konkrét alkalmazásban** való felhasználás után bizonyul ténylegesen általánosíthatónak. **Erre a projektre nézve a mélyebb (Roberts-féle) olvasat a releváns**, mert itt nem egy függvény kiemeléséről van szó, hanem egy architekturális réteg (mentési cél-adapter) bevezetéséről — ami pontosan az a granularitás, amiről Roberts eredetileg beszélt.

## 3. YAGNI mint általános absztrakció-ellenes elv vs. a felhasználó explicit kérése

**A látszólagos ellentmondás:** a kutatási kérdés (2. pont, motiváció) a felhasználó kimondott kérése egy cserélhető mentési-réteg megépítésére; eközben a szoftvertervezési irodalom (YAGNI, Speculative Generality) általában **óva int** az „egy nap talán kelleni fog” jellegű előre-építéstől.

**Feloldás — nem valódi ellentmondás, hanem kategória-tévesztés elkerülése.** Fowler saját szövege explicit kettéválasztja a két esetet: „**Yagni only applies to capabilities built into the software to support a presumptive feature**, it does not apply to effort to make the software easier to modify.” [T1] A YAGNI a **hallgatólagosan feltételezett**, be nem jelentett jövőbeli igények ellen szól — nem a **kimondottan, tervezetten** kért rugalmasság ellen. Mivel a felhasználó itt explicit, elhangzott szabályként (nem az agent feltételezéseként) kérte a cserélhetőséget, ez a YAGNI hatókörén **kívül** esik. A releváns kérdés emiatt nem az, hogy „legyen-e absztrakció”, hanem hogy „**milyen szűkre** legyen szabva” — ezt tárgyalja a `megallapitasok.md` „Ajánlás” szakasza.

## 4. Miért választják külön a helyreállítást — két különböző, egyaránt érvényes indoklás

**A látszólagos ellentmondás:** a Bacula és a Velero **mindkettő** külön Job-típust/objektumot használ a helyreállításra, de a dokumentációjuk **különböző okot** sugall. Bacula: a restore nem indítható automatikusan a scheduler által, „to restore files, you must use the restore command in the console” [T1] — ez emberi döntést feltételez. Velero: a restore **explicit előfeldolgozást** igényel (API-verzió kompatibilitás, névtér-átírás) — „runs some preprocessing on the backed up resources to make sure the resources will work on the new cluster” [T1] — ez viszont **automatizálható**, csak bonyolultabb logikát igényel, nem emberi jóváhagyást.

**Feloldás:** ez nem ellentmondás, hanem **két, egymástól független, egyaránt legitim indok ugyanarra a szerkezeti döntésre** (külön restore-interfész/objektum). A két indok nem zárja ki egymást, és egy rendszer akár mindkettővel rendelkezhet egyszerre. **Erre a projektre nézve:** mivel itt sem nagy horizontális skálázás (Velero-jellegű K8s-kompatibilitási előfeldolgozás), sem tömeges, felügyelet nélküli automatizált restore-igény (Bacula-jellegű ütemezési korlátozás) nincs kimondva a specifikációban, egyik indok sem kényszerítő erejű — vagyis nincs erős érv a mentési cél-adaptertől elkülönített, önálló restore-interfész mellett (l. `megallapitasok.md` 6. pont zárása).

## 5. Kopia: hirdetett univerzalitás vs. bevallott, korlátozott teszteltség

**Nem forrás-ellentmondás, hanem egy forráson belüli, tanulságos önellentmondás:** ugyanaz a Kopia-dokumentum egyszerre állítja, hogy „in theory, all Rclone-supported storage providers should work with Kopia”, majd azonnal hozzáteszi: „**however, in practice, only Dropbox, OneDrive, and Google Drive have been tested** to work with Kopia through Rclone.” [T1]

**Feloldás / tanulság:** ez nem two forrás közti vita, hanem egy **jó gyakorlat mintája**, amit érdemes követni: egy delegált (rclone-alapú) backend-mechanizmus elméleti hatóköre és a ténylegesen **letesztelt** hatóköre eltérhet, és ezt a különbséget **a dokumentációban explicit ki kell mondani** (figyelmeztető dobozzal), nem hallgatni el. Ez konzisztens a `megallapitasok.md` 4. pontjában levont fő tanulsággal: a jó mentési interfész nem rejti el a korlátait, hanem explicitté teszi őket.



---

# sq06 — Séma- és formátum-migráció motorfüggetlenül

# sq06 — Ellentmondások és feloldásuk

---

## 1. Liquibase (motor-NÉV szerinti elágazás) vs. Django/Rails (kapacitás-jelző szerinti elágazás)

**Az ellentmondás:** A megbízás 5. kérdése azt feltételezi, hogy a migrációs eszközök
esetleg ugyanazt a kapacitás-jelző mintát követik, mint a korábbi kutatásban talált
SQLAlchemy. Ez **részlegesen igaz, részlegesen hamis**:

- Django (`BaseDatabaseFeatures.supports_*`) és Rails (`AbstractAdapter.supports_*?`)
  **igen**, kapacitásra kérdeznek: a séma-szerkesztő kód `self.connection.features.
  supports_foreign_keys` (Django) vagy `supports_check_constraints?` (Rails) formában,
  **nem** `if vendor == "mysql"` formában dönt.
- Liquibase **nem**: a `dbms` changelog-attribútum explicit **motor-NÉV enumeráció**
  (`mysql`, `postgresql`, `oracle`, ...) — egy changeset alkalmazhatóságát a fejlesztő
  saját maga, a motor **nevére** hivatkozva korlátozza, nem egy elvont képességre.

**Feloldás:** ez **nem hiba egyik forrásban sem**, hanem a két eszköztípus eltérő
architektúrájának valós, dokumentált következménye:

- Django/Rails/SQLAlchemy **ORM-ek**, amelyeknél a séma-generáló kód **maga a
  keretrendszer belső logikája** — a keretrendszer fejlesztői írják és karbantartják a
  kapacitás-jelzőket, és ők döntik el, milyen finomságú kapacitás-halmazra van szükség
  (~94 Django-jelző, 40 Rails-jelző). Ez egy **zárt, kontrollált kódbázis**, ahol a
  kapacitás-alapú elágazás befektetése megtérül, mert a keretrendszer maga generál SQL-t
  minden egyes műveletre.
- Liquibase egy **changelog-alapú, deklaratív eszköz**, ahol a **végfelhasználó** (nem a
  Liquibase fejlesztői) írja a changeset-eket, és dönt arról, mely motorokra
  vonatkozzanak. Egy végfelhasználó számára sokkal egyszerűbb és átláthatóbb egy
  "ez a changeset csak Oracle-ön fusson" (`dbms="oracle"`) szabály, mint egy "ez a
  changeset csak ott fusson, ahol van X kapacitás" absztrakció — a Liquibase saját maga
  (a `addAutoIncrement` stb. change type-jaiban) **belsőleg** persze kapacitás-szerűen
  dönt (a "Database support" táblák lényegében befagyasztott kapacitás-adatok), de ezt
  **nem teszi elérhetővé** a végfelhasználó számára mint programozható predikátumot —
  csak mint dokumentációt.

**Következtetés a mentes-frissites saját tervezésére:** ha a saját portrétegük a
**belső** kódjukban dönt (mint egy ORM), a kapacitás-jelző minta a jobb választás
(karbantarthatóbb, jövőbiztosabb új motor hozzáadásakor). Ha viszont a **konfigurációs
fájlban / migrációs szkriptben** a végfelhasználó (fejlesztő) dönt motoronként, a
Liquibase-stílusú, név-alapú `dbms`-szerű megoldás egyszerűbb és érthetőbb — ez a kettő
**nem zárja ki egymást**, egy réteges architektúrában mindkettő megjelenhet (belül
kapacitás-jelző, kifelé név-alapú konfiguráció).

---

## 2. "A Flyway placeholder mechanizmusa motorfüggetlenséget ad" (téves benyomás) vs. a doksi tényleges állítása

**Az ellentmondás:** Több keresési találat (blogok, StackOverflow-jellegű tartalmak,
amiket a kutatás során láttunk címben, de nem olvastunk el részletesen) sugallja, hogy a
Flyway "placeholder" funkciója valamiféle motorfüggetlenségi mechanizmus. A hivatalos
doksi szó szerinti idézete viszont ezt mondja:

> "In addition to regular SQL syntax, Flyway also supports placeholder replacement...
> This can be very useful to abstract differences between **environments**." [kiemelés
> tőlünk]

**Feloldás:** a Flyway placeholder-jei **környezetek** (dev/staging/prod, séma-nevek,
tenant-nevek) közti különbségeket hidalják át, **nem motorok** közöttieket. A `{vendor}`
mechanizmus (ami tényleg motoronkénti mappákat választ) **nem Flyway-funkció**, hanem
Spring Boot-integrációs réteg — l. `megallapitasok.md` 2.2. Ez a különbségtétel a
forrásokban nem mindig explicit (a Flyway és a Spring Boot doksijait gyakran együtt
olvassák/idézik a fejlesztők), ezért a "Flyway támogatja a motoronkénti mappákat"
állítás **félrevezető általánosítás**, amit ez a kutatás explicit korrigál.

---

## 3. "Tolerant Reader = Fowler" vagy "Tolerant Reader = Robinson"? — a szerzőségi kérdés két olvasata

**Az ellentmondás:** A kutatási megbízás kifejezetten figyelmeztetett, hogy egy korábbi
mintánál már kiderült téves attribúció ebben a projektben, és arra kért, ellenőrizzük a
"Tolerant Reader" szerzőségét. Két, egymásnak ellentmondó olvasat lehetséges:

- **(A) olvasat:** "Tolerant Reader" = Fowler saját ötlete (2011), amit ő maga publikált
  a saját bliki-jén.
- **(B) olvasat, amit a téves attribúció kockázata felvet:** mivel a "Tolerant Reader"
  cikk maga is a "Consumer-Driven Contracts" (Ian Robinson, 2006) folytatásaként
  hivatkozik magára, és mindkettő ugyanazon a domainen (martinfowler.com), ugyanabban a
  témában (szolgáltatás-evolúció, séma-kompatibilitás) jelent meg, könnyen adódhat a
  téves általánosítás, hogy "ezek mind Fowler mintái" vagy fordítva, "ezek mind
  Robinson/ThoughtWorks-kollektíva mintái".

**Feloldás — ellenőrzött ténymegállapítás:** a két cikk bylineja **egyértelműen eltér**:
- Tolerant Reader (martinfowler.com/bliki/TolerantReader.html): byline **"Martin
  Fowler"**, dátum **"9 May 2011"**.
- Consumer-Driven Contracts (martinfowler.com/articles/consumerDrivenContracts.html):
  byline **"Ian Robinson"**, dátum **"12 June 2006"**, "Ian Robinson is a Principal
  Consultant with Thoughtworks" életrajzi sorral.

Tehát a **helyes** attribúció: "Tolerant Reader" = **Fowler** (nem téves attribúció,
ha valaki Fowlernek tulajdonítja); "Consumer-Driven Contracts" = **Robinson** (téves
attribúció volna, ha valaki Fowlernek tulajdonítaná, mivel Fowler csak a saját oldalán
publikálta, de nem ő a szerző). A kutatás nem talált bizonyítékot arra, hogy a
"Tolerant Reader" elnevezés Fowler 2011-es posztja **előtt** másnál (pl. a 2010-es
"REST in Practice" könyvben) már megjelent volna — ezt a `hianyok.md` 7. pontja
fenntartásként explicit rögzíti (a könyv teljes szövegéhez való hozzáférés hiánya
miatt nem zárható ki 100%-osan).

**Gyakorlati tanulság a mentes-frissites csapat számára:** ha korábban valamelyik
belső dokumentumuk "Tolerant Reader"-t Robinsonnak, vagy "Consumer-Driven
Contracts"-ot Fowlernek tulajdonította, azt érdemes javítani — ez pontosan az a
tévesztés-típus (szomszédos, azonos oldalon publikált, azonos témájú minták
összecserélése), amire a megbízás figyelmeztetett.

---

## 4. Django "16 dokumentált metódus" vs. forráskódban talált "80 def" — ez ellentmondás vagy sem?

**A látszólagos ellentmondás:** a hivatalos Django doksi-oldal 16 metódust dokumentál a
`SchemaEditor` "Methods" szekciójában, míg a tényleges forráskódban (`schema.py`) 80
`def` található.

**Feloldás — nem valódi ellentmondás, hanem réteg-különbség:** a 80-ból kb. 64 metódus
**alulvonás-prefixű** (`_alter_column_type_sql`, `_create_index_sql`, stb.) — ezek a
Django saját belső konvenciója szerint **privát/implementációs részletek**, amiket a
doksi tudatosan nem old fel nyilvános API-ként, csak a motoronkénti alosztályok írnak
felül. A doksi 16 metódusa a **ténylegesen stabil, kifelé dokumentált szerződés**; a
80 a **teljes, belső komplexitás beleértve azt is, amit egy motor-implementálónak
ismernie kell, ha mélyebb testreszabást akar**. Ezt a `megallapitasok.md` 4.1 pontja
mindkét számmal, a különbség okát is megmagyarázva közli — szándékosan nem
egyszerűsítettük egyetlen "a válasz X metódus" mondatra, mert az félrevezető volna.
