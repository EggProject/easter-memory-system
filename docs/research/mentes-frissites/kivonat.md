# Kivonat — mentés és verziófrissítés

A `mentes-frissites` kampány hat kutatási egységének megírt kivonata, egységenként.
Minden idézet szó szerinti, a forrás nyers letöltéséből. A következtetések a `SZINTEZIS.md`-ben
vannak, ez a fájl a forrásokat idézi.



---

# sq01 — Fájl-alapú tartalom mentése és helyreállítása

# SQ01 — Fájl-alapú tartalom mentése és helyreállítása — Megállapítások

Kutatási kampány: `mentes-frissites`, alkérdés: **sq01**
Készült: 2026-09-12
Tier-jelölés: **T1** = hivatalos dokumentáció / forráskód / kormányzati szerv; **T2** = megbízható másodlagos forrás vagy gyártói anyag konkrét, ellenőrizhető tartalommal; **T3** = fórum / blog / anekdota.
Lekérés módja minden idézetnél jelölve: **[nyers curl]** vagy **[WebFetch]** (kis modell összefoglalója — külön figyelmeztetéssel, ha releváns).

---

## 1. Hogyan mentik a fájl-alapú tartalmat, ami közben változhat?

### 1.1 BorgBackup — detektálja, de nem előzi meg a versenyhelyzetet

**[nyers curl]** Forrás: `borgbackup.readthedocs.io/en/stable/usage/create.html` (T1, hivatalos dokumentáció)

> "The `--files-changed` option controls how Borg detects if a file has changed during backup: […] disabled: Disable the "file has changed while we backed it up" detection completely. This is not recommended unless you know what you're doing, as it could lead to inconsistent backups if files change during the backup process."

> Az elem-jelölések (`--list` kimenet) között: "'C' = regular file, it changed while we backed it up"

**Értelmezés:** Borg maga **nem véd** a mentés közbeni módosítás ellen — csak *észleli* és figyelmezteti a felhasználót (`C` flag, "file changed while we backed it up" figyelmeztetés). A dokumentáció kifejezetten kimondja, hogy a detekció kikapcsolása inkonzisztens mentéshez vezethet. Ez azt jelenti, hogy egy futás közben módosuló fájl a mentésbe bekerülhet **részlegesen/kevert állapotban**, csak egy log-üzenet jelzi utólag.

**[nyers curl]** Forrás: `borgbackup.readthedocs.io/en/stable/usage/notes.html` (T1)

Borg hivatalos ajánlása nagy, élő rendszerek (pl. LVM logikai kötetek) konzisztens mentésére a **fájlrendszer-pillanatkép + utána mentés** minta:

> "Imagine you have made some snapshots of logical volumes (LVs) you want to backup. […] For some scenarios, this is a good method to get "crash-like" consistency (I call it crash-like because it is the same as you would get if you just hit the reset button or your machine would abruptly and completely crash). This is better than no consistency at all and a good method for some use cases, but likely not good enough if you have databases running."

**Értelmezés:** Borg saját dokumentációja szerint a pillanatkép-alapú konzisztencia csak "crash-like" (összeomlás-szerű) garanciát ad — ez jobb a semminél, de **adatbázisokhoz nem elég**. Ez direkt válasz a kérdésre: nincs "tökéletes" konzisztencia-garancia, csak fokozatok.

Megerősítés (második, független forrás): a Borg GitHub issue-k (`borgbackup/borg#8299`, `#6379`, `#8573` — **T3**, közösségi vitafórum) megerősítik, hogy a "file changed while we backed it up" figyelmeztetés élő, gyakran felmerülő probléma valós rendszereken, nem csak elméleti eset.

---

### 1.2 restic — Windows alatt VSS-t ajánl, Linuxon nincs beépített pillanatkép

**[nyers curl]** Forrás: `restic.readthedocs.io/en/stable/040_backup.html` (T1)

> "On Windows, the `--use-fs-snapshot` option will use Windows' Volume Shadow Copy Service (VSS) when creating backups. Restic will transparently create a VSS snapshot for each volume that contains files to backup. Files are read from the VSS snapshot instead of the regular filesystem. **This allows to backup files that are exclusively locked by another process during the backup.**"

**Értelmezés:** A restic hivatalos dokumentációja explicit módon a **VSS pillanatképet** ajánlja megoldásként a "fájl változik mentés közben" problémára — de **csak Windows alatt** van erre beépített opció. Linux alatt a restic dokumentációja NEM kínál natív fájlrendszer-pillanatkép integrációt; a gyakorlatban a felhasználónak kell LVM/ZFS/Btrfs pillanatképet csinálnia és arra futtatnia a restic-et (ezt a restic hivatalos dokumentációja nem mondja ki explicit módon egy külön szakaszban — **ez hiány**, ld. `hianyok.md`).

Emellett a restic a mentés eredményét "snapshot"-nak nevezi:
> "The contents of a directory at a specific point in time is called a 'snapshot' in restic."

**Fontos árnyalat (ld. `ellentmondasok.md`):** ez a "snapshot" elnevezés **marketing/terminológiai**, nem azonos egy fájlrendszer atomi pillanatképével — a restic Linux alatt sorban, fájlonként olvassa be az adatokat, tehát a mentés maga NEM atomi a teljes fájlfa szintjén, hacsak nem VSS-t vagy külső FS-pillanatképet használ alatta.

---

### 1.3 rsync — alapértelmezett ideiglenes fájl + átnevezés, explicit figyelmeztetés az `--inplace` opciónál

**[nyers curl]** Forrás: a hivatalos rsync forráskód-repó kézikönyv-oldala, `github.com/RsyncProject/rsync/blob/master/rsync.1.md` (T1 — ez a kanonikus forrás, mivel a `rsync.samba.org` és a `download.samba.org` közvetlen elérése a proxin keresztül 403-mal elutasítva — ld. `keresesek.md`).

Az `--inplace` opció leírásánál:
> "This option changes how rsync transfers a file when its data needs to be updated: instead of the default method of creating a new copy of the file and moving it into place when it is complete, rsync instead writes the updated data directly to the destination file. […] The file's data will be in an inconsistent state during the transfer and will be left that way if the transfer is interrupted or if an update fails. […] **WARNING: you should not use this option to update files that are being accessed by others**, so be careful when choosing to use this for a copy."

**Értelmezés:** Ez közvetve megerősíti, hogy az rsync **alapértelmezett** viselkedése ("creating a new copy of the file and moving it into place") maga is az ideiglenes fájl + atomi mozgatás minta — ugyanaz az elv, amit az easter-memory-system leírása is használ (temp fájl + atomi rename). Az `--inplace` explicit kivétel ez alól, és a dokumentáció kifejezetten figyelmeztet, hogy élő/használatban lévő fájloknál ne használják.

A `--delay-updates` opció leírása még pontosabban fogalmaz a teljes fastruktúra-szintű atomicitásról:
> "This option puts the temporary file from each updated file into a holding directory until the end of the transfer, at which time all the files are renamed into place in rapid succession. **This attempts to make the updating of the files a little closer to atomic.**"

**Értelmezés:** Az rsync hivatalos dokumentációja explicit elismeri, hogy az alap működés **fájlonként** atomi, de a **teljes fa** szintű atomicitáshoz külön opció (`--delay-updates`) vagy egy mellékelt "atomic-rsync" segédszkript kell — vagyis nincs "ingyen" garantált teljes-fa-konzisztencia.

Kilépési kód szinten is dokumentált a versenyhelyzet ténye:
> "24 - Partial transfer due to vanished source files"

**Értelmezés:** Az rsync hivatalos exit-kód listája külön kódot rendel ahhoz az esethez, amikor a forrásfájlok "eltűnnek" (törlődnek/módosulnak) mentés közben — ez direkt elismerése annak, hogy élő fájlrendszeren futtatva ez normális, kezelendő eset.

---

### 1.4 ZFS — a pillanatkép hivatalosan is "atomi és konzisztens"

**[nyers curl]** Forrás: `openzfs.github.io/openzfs-docs/man/master/8/zfs-snapshot.8.html` (T1, hivatalos OpenZFS kézikönyv)

> "Snapshots are created atomically. That is, **a snapshot is a consistent image of a dataset at a specific point in time**; it includes all modifications to the dataset made by system calls that have successfully completed before that point in time."

**Értelmezés:** Ez az egyetlen vizsgált technológia, ahol a hivatalos dokumentáció **kifejezett, formális konzisztencia-garanciát** ad: a pillanatkép a rendszerhívás-szinten befejezett módosításokig konzisztens állapotot rögzít, atomi módon. Ez erősebb garancia, mint a Borg "crash-like" jellemzése vagy az rsync fájlonkénti temp+rename mintája.

---

### 1.5 Btrfs — "egy pillanatkép nem mentés"

**[nyers curl]** Forrás: `btrfs.readthedocs.io/en/latest/Subvolumes.html` — ez a kernel.org Btrfs projekt hivatalos, Sphinx-alapú dokumentációja (T1; megkülönböztetve az ArchWiki-től, ami T2/közösségi).

> "**A snapshot is not a backup**: snapshots work by use of BTRFS' copy-on-write behaviour. A snapshot and the original it was taken from initially share all of the same data blocks. If that data is damaged in some way (cosmic rays, bad disk sector, accident with dd to the disk), then the snapshot and the original will both be damaged. Snapshots are useful to have local online "copies" of the filesystem that can be referred back to, or to implement a form of deduplication, **or to fix the state of a filesystem for making a full backup without anything changing underneath it**. They do not in themselves make your data any safer."

**Értelmezés:** Ez a legfontosabb egyetlen mondat az egész Q1 kérdéshez: a Btrfs hivatalos dokumentációja szerint a pillanatkép **helyes és ajánlott felhasználási módja** pontosan az, amit a Borg is bemutat (LVM példa) és amit a restic VSS-integrációja is megvalósít: *a pillanatkép nem helyettesíti a mentést, hanem eszköz arra, hogy a mentés programja egy "befagyasztott", nem változó állapotból dolgozhasson.* Ez a minta 3 független, egymástól teljesen különböző projekt (Borg, restic, Btrfs) hivatalos dokumentációjában konzisztensen megjelenik → **magas megbízhatóságú, iparági konszenzus jellegű megállapítás.**

### Összefoglaló válasz Q1-re

| Eszköz | Van-e beépített, alapértelmezett konzisztencia-garancia élő fájlokra? | Hivatalos ajánlás |
|---|---|---|
| Borg | Nem — csak észlel és figyelmeztet (`C` flag) | Fájlrendszer/LVM pillanatkép + `--read-special` a mentés előtt, ha erős konzisztencia kell |
| restic | Csak Windows/VSS alatt van beépített megoldás | `--use-fs-snapshot` (VSS) Windows alatt; Linuxon a felhasználóra van bízva a pillanatkép-integráció (dokumentálatlan hiány) |
| rsync | Fájlonként igen (temp+rename alapértelmezés), teljes fa szinten nem | `--delay-updates` a fa-szintű atomicitás közelítésére; `--inplace` ellen kifejezett figyelmeztetés |
| ZFS | Igen, explicit "atomic … consistent image" garancia | `zfs snapshot` a mentés előtt |
| Btrfs | Igen (COW-alapú pillanatkép), de a dokumentáció hangsúlyozza: a pillanatkép önmagában nem mentés | Pillanatkép + `btrfs send`/külső mentőeszköz kombinációja |

---

## 2. Markdown-alapú jegyzet-/tudásrendszerek mentési gyakorlata

### 2.1 Obsidian — hivatalos, explicit megkülönböztetés: "A szinkronizálás nem mentés"

**[nyers curl]** Forrás: az Obsidian hivatalos súgó-tartalmának kanonikus GitHub-repója, `github.com/obsidianmd/obsidian-help`, fájl: `en/Getting started/Back up your Obsidian files.md` (T1 — ez az Obsidian saját, verziókövetett dokumentáció-forrása, amit az `obsidian.md/help/backup` publikus oldal is megjelenít).

> "## Syncing is not a backup
> Services like Obsidian Sync, iCloud, OneDrive, and Dropbox help you sync your notes across different devices. While they may offer features like note restoration, **they are not designed for backups**. Syncing keeps your notes updated, but it doesn't protect against data loss.
> - **Sync:** Syncing ensures your files are the same on all devices. […]
> - **Backup:** A backup saves a copy of your data in a different location to help recover it in case of data loss or corruption. Backups are not meant for real-time updates or collaboration.
> To properly back up your vault, use a dedicated backup tool that creates a **one-way copy** of your data."

**Értelmezés:** Ez szó szerint ugyanaz a fogalmi megkülönböztetés, mint a Btrfs "a pillanatkép nem mentés" állítása — csak itt szinkronizáció vs. mentés a téma. **Ez egy második, teljesen független forrásból (fájlrendszer-szint vs. jegyzetalkalmazás-szint) megerősített minta**, ami erősíti a megállapítás általánosíthatóságát: a *verziókezelés / szinkronizáció / pillanatkép nem helyettesíti a különálló, más helyre irányuló, egyirányú mentést.*

Az Obsidian hivatalos dokumentációja konkrét eszközöket is ajánl (community plugin, nem hivatalosan jóváhagyott, de a hivatalos dokumentáció megemlíti):
> "**Obsidian Git:** Use this plugin to back up your vault by committing its contents to a Git Repository. It's an effective way to version control your notes and ensure their safety on a remote server."
> "**Linux**: `rsync` to a directory or drive of choice." (az operációs rendszer natív mentési lehetőségei közt)

**[nyers curl]** Az Obsidian Sync hivatalos dokumentációja (`obsidian.md/help/sync`, `Version history.md`) a szinkronizáció beépített verziótörténetét írja le:
> "The retention period for your version history depends on your Obsidian Sync plan. On the Standard plan, notes are retained for 1 month, while on the Plus plan, they are kept for 12 months. After this period, older versions of your notes are deleted. For attachments, older versions are stored for two weeks."

**Értelmezés:** Ez direkt bizonyítja, hogy a beépített "Sync verziótörténet" **időben korlátozott** (1 vagy 12 hónap), tehát önmagában tényleg nem helyettesíti a hosszú távú mentést — alátámasztja a fenti hivatalos kijelentést, nem csak állítja azt.

### 2.2 Logseq — hivatalos, automatikus, óránkénti helyi mentés, korlátozott megőrzéssel

**[nyers curl]** Forrás: `github.com/logseq/docs/blob/master/db-version.md` (T1, a Logseq projekt saját hivatalos dokumentáció-repója)

> "## Automated Backup
> This feature is _only_ for the browser and desktop. An automated backup of graphs is available by clicking on the upper right three dots menu and selecting `Export Graph`.
> For the browser, you can specify a folder (directory) to save backups. A backup folder can be reused across graphs as each graph gets its own folder within a backup folder. After choosing this folder, **hourly backups begin. The last 12 backups are saved.**
> For the desktop, backups are automatically enabled at the `backups` folder inside your graph directory. **The last 12 backups are saved.**"

**Értelmezés:** A Logseq mintája nagyon hasonló elvi felépítésű, mint amit az easter-memory-system tervez: helyi, automatikus, óránkénti pillanatkép-mentés, korlátozott számú (12) megőrzött verzióval — ez egy iparági bevett minta kis, lokális, fájl-alapú jegyzetrendszerekben, nem csak elméleti javaslat.

### 2.3 Git mint mentés — hivatalos korlátok (méret, bináris fájlok)

**[nyers curl]** Forrás: `docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github` (T1, hivatalos GitHub dokumentáció)

> "GitHub limits the size of files allowed in repositories. If you attempt to add or update a file that is larger than 50 MiB, you will receive a warning from Git."
> "**Git is not designed to handle large SQL files.** To share large databases with other developers, we recommend using a file sharing service."
> "We recommend repositories remain small, **ideally less than 1 GB, and less than 5 GB is strongly recommended.** Smaller repositories are faster to clone and easier to work with and maintain."

**Értelmezés:** Ez közvetlenül releváns az easter-memory-system SQLite-indexére és bármilyen bináris melléklet-tárolására: a hivatalos GitHub-dokumentáció kifejezetten kimondja, hogy a git **nem alkalmas nagy bináris/SQL adatbázis-fájlok kezelésére**, és számszerű méretajánlást ad (1 GB ideális, 5 GB felső határ egy repóra). Ez alátámasztja azt a tervezési döntést, hogy az eldobható SQLite index NE kerüljön verziókezelt mentésbe, csak a forrás markdown fájlok.

**Fontos, hogy MIT nem találtunk:** nincs hivatalos git-scm.com vagy GitHub nyilatkozat, ami kimondaná, hogy "a git nem mentőeszköz" ilyen direkt megfogalmazásban (szemben az Obsidian/Btrfs explicit "nem mentés" kijelentéseivel). Ez a konkrét mondat **csak közösségi blogokban/fórumokon (T3)** kering (pl. "Why git clone is not a backup solution" – rewind.com, T3/gyártói blog). → **hiányként dokumentálva**, ld. `hianyok.md`.

---

## 3. A „3-2-1 szabály" eredete és mai hivatalos állása

### 3.1 Eredet — Peter Krogh, "The DAM Book" (2005)

**[nyers curl]** Forrás: `backupwrapup.com/peter-krogh-who-coined-the-3-2-1-rule-on-our-podcast/` (T2 — iparági backup-podcast, de **közvetlen interjú az állítólagos megalkotóval**, ami erősebb, mint egy sima másodkézből származó blogbejegyzés)

> "Peter Krogh coined the term fifteen years ago. […] He first talks about how he coined the term "3-2-1 Rule" while writing the first edition of **The DAM Book: Digital Asset Management for Photographers**, now in its 3rd edition. **He didn't invent the idea of three copies and offsite backup, but he did distill it down to what we now refer to as the 3-2-1 rule.** (Three copies on two media types, one of which is offsite.)"

**Értelmezés:** Fontos árnyalat magából az idézetből: Krogh maga sem állítja, hogy ő találta ki az "adatot több példányban, több helyen tárold" alapelvet (ez régebbi, informális gyakorlat volt fényképészek/rendszergazdák közt) — csak azt állítja, hogy **ő fogalmazta meg tömören "3-2-1" formában**, a *The DAM Book* c. 2005-ös fényképész-szakkönyvében.

**[nyers curl]** Másodlagos megerősítés: `thedambook.com/the-dam-book/` (T2, a könyv hivatalos oldala) — a könyv fejezetjegyzékében szerepel: "8 – Backup, Verification and Restoration", ami megerősíti, hogy a könyv ténylegesen foglalkozik mentési stratégiával, de a "3-2-1" kifejezés szó szerint nem jelenik meg ezen a marketingoldalon (ez önmagában nem cáfolat, csak nem ad közvetlen szöveges bizonyítékot).

**Hiány/ellentmondás:** A Wikipedia „Peter Krogh (photographer)" cikke (**[nyers curl]**, T2/tercier forrás) **egyáltalán nem említi** a 3-2-1 szabályt vagy annak megalkotását Krogh életrajzában — pedig ott lenne a helye egy ilyen állításnak, ha széles körben elfogadott, forrásolt tényről lenne szó. A Wikipedia „Backup" cikke (**[nyers curl]**) ismerteti magát a 3-2-1 szabályt, de **nem nevez meg megalkotót**, senkinek nem tulajdonítja. → Az eredettörténet tehát **iparági legendárium szintjén dokumentált (T2, egyetlen közvetlen interjú-forrásra vezethető vissza), nem enciklopédikusan/tudományosan igazolt tény.** Részletek: `ellentmondasok.md`.

### 3.2 Mai hivatalos állás — CISA igen, NIST nem használja a kifejezést

**[WebFetch]** Forrás: `cisa.gov/audiences/small-and-medium-businesses/secure-your-business/back-up-business-data` és `cisa.gov/audiences/state-local-tribal-and-territorial-government/secure-us-sltt/back-government-data` (T1, mindkettő a US CISA — Cybersecurity and Infrastructure Security Agency — hivatalos oldala; **mindkét oldalt raw curl-lel nem sikerült elérni**, Akamai "Access Denied" hibát adott minden User-Agent/cookie-kombinációval — ld. `keresesek.md`; WebFetch-csal viszont sikerült, és a két oldal szövege szó szerint megegyezik).

> "3 copies of important files, 2 different types of storage media (like a hard drive and the cloud), 1 copy stored off-site"

**Értelmezés:** A CISA — az Egyesült Államok hivatalos kiberbiztonsági ügynöksége — **jelenleg (2026) aktívan használja és ajánlja** a 3-2-1 szabályt, nevesítve, mindkét fő közönség-oldalán (kisvállalkozás és állami/önkormányzati szervek). Mivel a szöveg szó szerint azonos a két oldalon, ez technikailag **egy forrásból (CISA sablon-szöveg) származik**, nem két független megerősítés — jelölve.

**[nyres curl]** Ezzel szemben a **NIST SP 800-34 Rev. 1** (a szövetségi informatikai rendszerek katasztrófa-helyreállítási tervezésének hivatalos NIST-szabványa, T1, teljes szövegében átvizsgálva) **egyetlen egyszer sem említi** a "3-2-1" kifejezést. A NIST dokumentum a CP-9 kontroll (Information System Backup) alatt sokkal általánosabban fogalmaz: "organization-defined frequency", nem ad ki kész számformulát.

**Következtetés:** A "3-2-1 szabály" **nem egy formális NIST-szabvány vagy -kontroll**, hanem egy **kommunikációs/oktatási ökölszabály**, amit a CISA (közönségtájékoztatási céllal, gyakorlati, nem szabványosítási dokumentumaiban) átvett és népszerűsít, miközben a NIST szigorúbb, technikai kontroll-dokumentuma nem hivatkozik rá. Ez nem ellentmondás, hanem **két különböző dokumentum-műfaj** (közérthető oktatóanyag vs. formális szabályzat) közötti különbség.

Nem található bizonyíték arra, hogy bármelyik **nemzeti CERT** (pl. magyar NBSZ NKI, német BSI, brit NCSC) a "3-2-1" kifejezést szó szerint, névvel ellátva kanonizálná mint saját szabványt — az NCSC (UK) hivatalos oldalain (ld. Q6/Q5) a hasonló elvet (több másolat, más adathordozó, offline másolat) **explicit "3-2-1" címke nélkül**, körülírva adja elő. → hiányként jelölve.

---

## 4. Helyreállítás-ellenőrzés (restore drill)

### 4.1 NIST — konkrét szám: évente

**[nyers curl]** Forrás: NIST SP 800-34 Rev. 1, 3.2 fejezet (T1)

> "The plan recovery capabilities and personnel shall be **tested annually** to identify weaknesses of the capability."

A 3.6/Table 3-6 (TT&E — Testing, Training, and Exercises) tevékenységtáblázatban külön nevesített tétel:

> "**System Backup (CP-9)**: Test backup information to verify media reliability and information integrity. (For a high-impact system, use sample backup information and ensure that backup copies are stored in a separate facility.)" — kötelező közepes és magas hatású rendszereknél ("Mod. Impact = Yes, High Impact = Yes"), alacsony hatásúaknál nem elvárás ("Low Impact = N/A").

**Értelmezés:** Ez **konkrét, számszerű hivatalos ajánlás**: a NIST szerint a teljes kontinuitási terv (beleértve a mentés-helyreállítást) **évente** tesztelendő szövetségi informatikai rendszereknél, súlyozva a rendszer kritikussága szerint (FIPS 199 hatásbesorolás). Ugyanakkor a konkrét CP-9(1) technikai kontroll szövege (Appendix E) **nem ad fix számot**, hanem "organization-defined frequency"-t ír elő — tehát a NIST-en belül is van egy általánosabb ("szervezet döntse el") és egy konkrétabb ("évente") szint. Ld. `ellentmondasok.md`.

### 4.2 CIS Controls v8 — negyedévente (konkrétabb, nem kormányzati szabvány)

**[nyers curl]** Forrás: `cas8.docs.cisecurity.org/en/latest/source/Controls11/` (T2 — a Center for Internet Security egy nonprofit szervezet, nem kormányzati testület, de kontrolljait sok kormányzati keretrendszer referenciaként használja)

> "**11.5: Test Data Recovery** — Test backup recovery **quarterly**, or more frequently, for a sampling of in-scope enterprise assets."

**Értelmezés:** Ez a legkonkrétabb, számszerű, kifejezetten a *helyreállítás tesztelésére* (nem az egész kontinuitási tervre) vonatkozó ajánlás, amit találtunk: **negyedévente**, mintavételezéssel. Feltétel: ez a CIS Controls Implementation Group 2 és 3 (közepes/nagyobb szervezetek) szintjén elvárt safeguard, kis (1-es csoportos) szervezeteknél nem kötelező elem a hivatalos specifikáció szerint.

### 4.3 Mennyi mentés bizonyul helyreállíthatatlannak? — mért adat, konkrét feltételekkel

**[nyers curl]** Forrás: At-Bay ("Backup Breakdown: How Data Recovery Solutions Impacts the Outcome of Cyber Attacks" sajtóközlemény, `at-bay.com/press_releases/...`) (T2 — kiberbiztosító saját, elsődleges kárigény-adatai, konkrét módszertannal)

> "Despite 92% of businesses reporting having backups, **more than 1 in 4 businesses (31%) fail to restore data from them** during a ransomware attack."
> Módszertan: "The dataset used for the analysis in this report is from small to mid-sized businesses that held an At-Bay policy between 2019 to 2023, which covers 50,000 policy years. **We analyzed 186 ransomware claims** in which backups were involved."

**Feltételek, amik alatt ez a szám érvényes:** kkv-k (small-to-mid-sized businesses), **konkrétan zsarolóvírus-támadás** kontextusában (nem általános meghibásodás), At-Bay biztosítási ügyfélkör, 2019–2023, n=186 kárigény. **Ez nem általánosítható minden mentési forgatókönyvre** — kifejezetten a "támadás közben derül ki, hogy a mentés nem áll helyre" esetre vonatkozik.

**Nem találtunk** olyan hivatalos (kormányzati/szabványügyi) forrást, amely általános, minden körülmények közötti "hány százalék mentés helyreállíthatatlan" számot közölne. A gyakran idézett "Gartner szerint a tape-mentések X%-a nem működik" típusú állítások nyomát nem sikerült egy ellenőrizhető, elsődleges Gartner-forrásig visszavezetni ebben a kutatásban → **hiányként jelölve**, ld. `hianyok.md`.

### 4.4 "A nem tesztelt mentés nem mentés" — iparági közmondás, nem azonosítható egyetlen hivatalos forrás

A mondás ("nobody wants backup, everybody wants restore") **W. Curtis Preston**-nak ("Mr. Backup") tulajdonítva kering (T3 — blogbejegyzések, Hacker News-fórum, podcast-leírások), de **nem sikerült elsődleges, dátumozott, ellenőrizhető forrást találni**, ahol Preston ezt először, dokumentáltan kimondta volna. Ez tisztán **hiányként** dokumentált: az állítás valós és széles körben idézett, de a "ki mondta ki elsőként, mikor" kérdésre nincs megbízható válasz.

---

## 5. Mentési gyakoriság kis rendszereknél; RPO/RTO definíciók

### 5.1 RPO és RTO — hivatalos NIST-definíció

**[nyers curl]** Forrás: NIST SP 800-34 Rev. 1, Glosszárium és 3.1 fejezet (T1)

> "**Recovery Time Objective (RTO).** RTO defines the maximum amount of time that a system resource can remain unavailable before there is an unacceptable impact on other system resources, supported mission/business processes, and the MTD."

> "**Recovery Point Objective (RPO).** The RPO represents the point in time, prior to a disruption or system outage, to which mission/business process data can be recovered (given the most recent backup copy of the data) after an outage. Unlike RTO, RPO is not considered as part of MTD. Rather, it is a factor of how much data loss the mission/business process can tolerate during the recovery process."

Glosszárium rövid formában:
> "Recovery Point Objective: The point in time to which data must be recovered after an outage."
> "Recovery Time Objective: The overall length of time an information system's components can be in the recovery phase before negatively impacting the organization's mission or mission/business processes."

**Értelmezés:** Az **RPO = mennyi adatot engedhetünk meg magunknak elveszíteni** (időben mérve — "az utolsó mentés óta eltelt idő"), az **RTO = mennyi ideig lehet a rendszer elérhetetlen**, amíg helyre nem áll. A dokumentum explicit kimondja: "the RTO must normally be shorter than the MTD" (MTD = Maximum Tolerable Downtime, a szervezet által elviselhető max. leállás). Ez a hivatalos, kanonikus definíció-forrás, amit gyakorlatilag minden másodlagos (gyártói) forrás átvesz/parafrazál.

### 5.2 Konkrét gyakoriság-ajánlás kis rendszerekre

**[nyers curl]** CIS Controls v8, 11.2 Safeguard (T2):
> "Perform automated backups of in-scope enterprise assets. **Run backups weekly, or more frequently, based on the sensitivity of the data.**"

**[WebFetch]** CISA hivatalos oldalak (T1): nem adnak számot, csak "runs automatically and regularly" — explicit elkerülik a konkrét szám megadását.

**[WebFetch]** NCSC (UK) hivatalos kisszervezeti útmutató (`ncsc.gov.uk/collection/small-organisations-guide-to-cyber-security/backing-up-your-data`, T1 — az oldal JavaScript-alapú, nyers curl-lel a tartalom nem hozzáférhető, csak a Drupal-héj jön le; WebFetch-csal sikerült kinyerni; ld. `keresesek.md`/`hianyok.md`) sem ad számot, csak minőségi ajánlást ad ("legyen automatikus, rendszeres" + különálló, offline másolat + teszteld a visszaállítást).

**Következtetés:** Az egyetlen **konkrét, számszerű** ajánlás kis/közepes rendszerekre, amit hivatalos/félhivatalos forrásban találtunk, a **CIS Controls "heti" (weekly) gyakorisága**, kifejezetten adatérzékenység-függő módosítással ("or more frequently, based on the sensitivity of the data"). A ténylegesen kormányzati (CISA, NCSC) források tudatosan **nem** adnak ki fix számot, hanem "rendszeres, automatizált" megfogalmazást használnak — ez azt sugallja, hogy a hivatalos szervek szándékosan kerülik az egy-mindenre-illő szám megadását, és a konkrét RPO-t a szervezetre bízzák a saját kockázatértékelése alapján (ahogy a NIST CP-9 kontroll is teszi: "organization-defined frequency consistent with recovery time and recovery point objectives").

**Kifejezetten "néhány felhasználós, néhány ezer fájlos" méretre szabott hivatalos vagy mért ajánlást nem találtunk** — ez konkrét hiány, ld. `hianyok.md`.

---

## 6. A mentés jogosultsági kockázata

### 6.1 NCSC (UK) — konkrét, tételes elvek a mentőrendszer jogosultságaira

**[WebFetch]** Forrás: `ncsc.gov.uk/collection/ransomware-resistant-backups/principles-for-ransomware-resistant-on-premises-backups` (T1, brit Nemzeti Kiberbiztonsági Központ; nyers curl-lel a tartalom JS-mögötti, nem kinyerhető — ld. `keresesek.md`; **ez egyetlen forrásból (NCSC) igazolt tartalom**, független második megerősítést nem találtunk szó szerinti idézetre, ld. `hianyok.md`).

A hat elv közül a jogosultsági kockázatra vonatkozók:

> "Make sure a backup solution uses **admin accounts and credentials that are separate** from those used to administer the rest of your network."

> "Have in place robust key management for data-at-rest protection" — javasolt gyakorlat: kövessük "the NCSC key storage guidance"-t, és legyen "an out-of-band key backup option, such as committing a master key to paper."

> "Alerts are triggered if significant changes are made, or privileged actions attempted" (azaz a mentőrendszeren végzett kiemelt jogú műveletekről riasztás fusson).

Immutabilitásra (a "ki állíthat vissza / ki írhatja felül" kérdés technikai oldalára):
> "Using storage media that is 'write once, read many' (or WORM) is one way to achieve this."
> Offline védelemre: "Storing physically disconnected backup media separately, off the network."

**Értelmezés:** Ez a legkonkrétabb, legkevésbé általános válasz a kérdésre: a hivatalos brit kiberbiztonsági ügynökség kifejezetten **külön adminisztrátori fiókot/hitelesítő adatokat** ír elő a mentőrendszerhez képest a normál hálózati adminisztrációhoz, **WORM-tárolást** javasol az visszaállíthatatlan felülíráshoz, és **kulcskezelési** elvárást fogalmaz meg titkosításhoz (offline "papír" kulcs-mentés is szerepel mint konkrét gyakorlat).

### 6.2 NIST — a mentés bizalmasságának/integritásának védelme mint formális kontroll-elem

**[nyers curl]** NIST SP 800-34 Rev. 1, CP-9 kontroll (T1):

> "d. **Protects the confidentiality and integrity of backup information at the storage location.**"
> "An organizational assessment of risk guides the use of encryption for protecting backup information."
> "Encryption is most effective when applied to both the primary data storage device and on backup media going to an offsite location. […] A solid key management process must be established so encrypted data is available as needed. […] These keys should be stored separate from, but accessible to, the primary encrypted backup data."

**Értelmezés:** A NIST **nem ír elő kötelezően** titkosítást minden esetben — a döntést a szervezet kockázatértékelésére bízza ("organizational assessment of risk guides the use of encryption") —, de ha titkosítást használnak, akkor **kulcskezelési** elvárásokat fogalmaz meg (a kulcsokat külön, de elérhető helyen kell tárolni a titkosított adathoz képest). Ez összhangban van az NCSC fenti, konkrétabb ajánlásával.

### 6.3 CISA — fizikai védelem, titkosítás, offline másolat együtt

**[WebFetch]** CISA hivatalos oldalak (T1, ld. fent):
> "Leverage protections for backups, including **physical security, encryption and offline copies**."

**Értelmezés:** A CISA nem bontja ki tételesen (nincs "külön admin fiók" kikötés, mint az NCSC-nél), csak felsorolásszerűen említi a titkosítást és a fizikai/offline védelmet — kevésbé technikai mélységű, mint az NCSC anyag.

### 6.4 A mentés jogosultság-megkerülő természete — nincs formális, számszerű kockázatbecslés

**Fontos hiány:** egyik vizsgált hivatalos forrás sem ad **számszerű** kockázatbecslést arra, hogy "a mentésben lévő, jogosultsági rendszert megkerülő teljes hozzáférés hányszor vezetett tényleges incidenshez" — ez a kockázat minőségileg (elvi ajánlásokkal: külön fiók, titkosítás, WORM, riasztás) van kezelve minden forrásban, de **mért gyakorisági/súlyossági adat nincs**. Ez hiányként dokumentálva, ld. `hianyok.md`.

---

## Összegzés — a hat kérdésre adott rövid válasz

1. **Változó fájlok mentése:** minden vizsgált eszköz (Borg, restic, rsync) vagy explicit figyelmeztet a mentés közbeni változásra, vagy fájlrendszer-szintű pillanatképet (ZFS/Btrfs/VSS) ajánl megoldásként. A Btrfs és a restic/Borg dokumentációja egybehangzóan úgy fogalmaz, hogy a pillanatkép szerepe **a mentés programjának "befagyasztott" bemenetet biztosítani**, nem maga a mentés.
2. **Jegyzetrendszerek:** Obsidian és a Btrfs projekt egymástól függetlenül, azonos fogalmi éllel mondja ki: *szinkronizáció/verziótörténet ≠ mentés*. Logseq hivatalos, óránkénti, 12 verziót megőrző helyi mentése strukturálisan hasonlít az easter-memory-system tervéhez. A git hivatalos (GitHub) korlátai (max. ajánlott repóméret 1–5 GB, bináris/SQL fájlok nem ajánlottak) közvetlenül indokolják az eldobható SQLite index kizárását a verziókezelésből.
3. **3-2-1 szabály:** iparági eredetű (Peter Krogh, 2005, *The DAM Book*), amit a CISA ma is aktívan hirdet, de a NIST formális szabványa (SP 800-34) **nem használja/nem hivatkozza**. Nem találtunk nemzeti CERT-et, amely saját névvel kanonizálná.
4. **Helyreállítás-teszt:** a NIST konkrét számot ad — **évente** (a teljes kontinuitási tervre), a CIS Controls **negyedévente** (kifejezetten a mentés-helyreállításra, közepes+ szervezeteknél). Konkrét, feltételes mért adat a mentés-helyreállítás sikertelenségére: **31% (n=186, kkv-k, zsarolóvírus-kontextus, At-Bay biztosítási adat, 2019–2023)**.
5. **Gyakoriság kis rendszereknél:** a kormányzati szervek (CISA, NCSC) tudatosan nem adnak számot, csak "rendszeres, automatikus" ajánlást. A CIS Controls konkrét számot ad: **heti**, adatérzékenységtől függő gyakorítással. Az RPO/RTO fogalompár hivatalos definíciós forrása a NIST SP 800-34 Rev. 1.
6. **Jogosultsági kockázat:** az NCSC (UK) ad legkonkrétabb, tételes ajánlást: külön admin-fiók a mentőrendszerhez, WORM/immutábilis tárolás, kulcskezelés (offline kulcs-mentés is), riasztás kiemelt műveletekre. A NIST ezt kockázatalapú, szervezetre bízott döntésként kezeli, konkrét kontroll-elemekkel (CP-9d: bizalmasság+integritás védelme a tárolási helyen).



---

# sq02 — Futó SQLite adatbázis biztonságos mentése

# sq02 — Futó SQLite adatbázis biztonságos mentése — megállapítások

**Kampány:** mentes-frissites · **Alfeladat:** sq02
**Dátum:** 2026-09-12
**Módszer:** minden `sqlite.org` és `litestream.io` oldal nyers HTML-ként letöltve `curl`-lel a proxyn keresztül, majd tag-stripelve (lásd `raw/` mappa és a letöltött szöveges változatok `raw/text/` alatt). A `.backup`/`.dump` parancsok belső működését közvetlenül a SQLite forráskódjából (`shell.c.in`, a hivatalos Fossil-repóból, `sqlite.org/src`) ellenőriztem — ez T1-es forrás (forráskód).

**Módszertani korlát (fontos, átlátszóság kedvéért):** ez a kutatás **nem** a deep-web-research skill teljes multi-agent (Sonnet-kereső / Opus-szintéző) pipeline-jával futott, mert ebben a munkakörnyezetben nem állt rendelkezésre subagent-indító (`Agent`/`Task`-dispatch) eszköz. A keresést, a nyers HTML-letöltést, az idézetek ellenőrzését és a szintézist egyetlen munkamenet végezte, szekvenciálisan. Ez nem jelenti azt, hogy a fázisok izoláltak lettek volna — a modellszétválasztás (Sonnet-kereső / Opus-szintetizáló), amit a skill fő pillérének nevez, **nem valósult meg**. Az idézetek pontosságát ez nem érinti (nyers HTML + szó szerinti grep-ellenőrzés), de a szintézis mélysége egyetlen áttekintésre korlátozódik.

Tier-jelölés: **T1** = hivatalos dokumentáció / forráskód; **T2** = megbízható másodlagos forrás (elismert szakértő, gyártói blog, jól dokumentált gyakorlat); **T3** = fórum, blog, közösségi anekdota. A SQLite hivatalos fórumát (`sqlite.org/forum`) — bár a hivatalos domainen van, és gyakran a SQLite fejlesztői/konzulensei (pl. Keith Medcalf, Simon Slavin, Larry Brasfield) válaszolnak — a tier-rendszer szó szerinti definíciója szerint **T3**-ként (fórum) jelölöm, nem T1-ként, mert nem hivatalos, lektorált dokumentáció.

---

## 0. Vezetői összefoglaló

1. A SQLite hivatalos dokumentációja **kifejezetten kimondja**, hogy egy futó adatbázis fájlmásolása tranzakció közben korrupciót okozhat, és **három** hivatalosan biztonságosnak nyilvánított módszert sorol fel: `sqlite3_rsync`, `VACUUM INTO`, Backup API. Egyszerű fájlmásolás (`cp`) is biztonságos, de **csak** ha a másolás pillanatában nincs folyamatban tranzakció, és a `-wal`/`-journal` fájlt is átmásolják a fő fájllal együtt.
2. A Backup API **nem blokkolja folyamatosan** az írókat (a forrást csak rövid, lépésenkénti pillanatokra zárolja), de dokumentáltan **újraindulhat** külső írás esetén, és a hivatalos dokumentáció szó szerint kimondja: ha az írás elég gyakori, a backup **sosem fejeződik be** ("may never run to completion"). A CLI beépített `.backup` parancsa (forráskód-ellenőrzéssel igazolva) **nem** implementál újrapróbálkozást zárolási hiba esetén — egyetlen `SQLITE_BUSY`/`SQLITE_LOCKED` esetén elbukik.
3. A két adatbázis (felhasználói + index) **kereszt-konzisztenciájára nincs bevett SQLite-megoldás**, ha mindkettő WAL módban fut. A hivatalos `ATTACH` dokumentáció kimondja: több adatbázis közötti tranzakció csak akkor atomi, ha **egyik sem** `:memory:` és a `journal_mode` **nem** WAL. WAL módban — ami egy folyamatosan futó, konkurens szerverhez szükséges — a több fájlra kiterjedő atomicitás **nincs garantálva**, még a SQLite saját `ATTACH` mechanizmusával sem. Erre a forráskutatás során **semmilyen forrás** (hivatalos vagy közösségi) nem mutatott be bevett, általános megoldást a mi esetünkhöz hasonló, két *külön* SQLite-fájl esetére — ez tehát valódi, dokumentált hiány, nem csak az én kutatásom hiányossága.

---

## 1. A hivatalos dokumentáció a futó adatbázis fájlmásolásáról

**Forrás (elsődleges, T1):** [How To Corrupt An SQLite Database File](https://www.sqlite.org/howtocorrupt.html), 1.2. szakasz — "Backup or restore while a transaction is active". Utoljára frissítve: 2026-04-13 (a lap alján jelzett dátum, nyers HTML-ből ellenőrizve).

> "Systems that run automatic backups in the background might try to make a backup copy of an SQLite database file while it is in the middle of a transaction. The backup copy then might contain some old and some new content, and thus be corrupt."

Ez a pontos, szó szerinti megfogalmazás a bukási módra: **"some old and some new content"** — vagyis a naiv fájlmásolás a régi és az új tartalom keverékét másolhatja ki, ha az épp íráson lévő tranzakció közepén kapja el a fájlt.

A lap ezután felsorolja a hivatalosan biztonságosnak nyilvánított módszereket:

> "There are multiple safe approaches to making backup copies of SQLite databases - safe in the sense that they are generate a correct, uncorrupted backup. In no particular order:
> The sqlite3_rsync utility program (available beginning with SQLite 3.47.0 (2024-10-21) and later) will make a copy of a live SQLite over SSH using a bandwidth-efficient protocol.
> The VACUUM INTO filename command copies out the current state of an SQLite database into a separate file.
> The backup API is a C-language interface that can make a consistent copy of an SQLite database."

Fontos, gyakran félreértett rész — **az egyszerű fájlmásolás sem feltétlenül tilos**:

> "Any of the above approaches will work even on a live database. It is also safe to make a copy of an SQLite database file as long as there are no transactions in progress while the copy is taking place. If the previous write transaction failed, then it is important that any rollback journal (the *-journal file) or write-ahead log (the *-wal file) be copied together with the database file itself."

Vagyis: `cp` **is** biztonságos, de csak akkor, ha (a) a másolás pillanatában garantáltan nincs nyitott tranzakció, és (b) ha bármilyen `-journal` vagy `-wal` fájl létezik, azt is át kell másolni a fő fájllal együtt. Egy folyamatosan futó, konkurens írásokat fogadó szerver esetén az "(a)" feltétel gyakorlatilag nem garantálható alkalmazás-szintű koordináció nélkül — ez az egész kérdés magja.

### A három bukási mód név szerint

A dokumentáció külön szakaszokban tárgyalja a három konkrét bukási módot, amit a kutatási kérdés is kért:

**(i) "Hot journal" törlése/eltávolítása — 1.3. szakasz:**
> "SQLite must see the journal files in order to recover from a crash or power failure. If the hot journal files are moved, deleted, or renamed after a crash or power failure, then automatic recovery will not work and the database may go corrupt."

**(ii) Fájl és napló összekeverése — 1.4. szakasz ("Mispairing database files and hot journals"):** a felsorolt, korrupcióhoz vezető műveletek között:
> "Copying a database file without also copying its journal."
> "Overwriting a database file with another without also deleting any hot journal associated with the original database."

**(iii) Részleges ("torn") lapírás — az Atomic Commit In SQLite dokumentumból (T1, [atomiccommit.html](https://www.sqlite.org/atomiccommit.html), 4.1. szakasz, "When Something Goes Wrong…"):** ez a mechanizmus írja le pontosan azt az állapotot, amit egy félbekapott fájlmásolás is befagyaszthat:
> "We were trying to change three pages of the database file but only one page was successfully written. Another page was partially written and a third page was not written at all."

Ez a szakasz technikailag az áramkimaradás utáni helyreállításról szól, de **ugyanaz a mechanizmus** magyarázza, miért veszélyes egy `cp`, ha épp akkor fut, amikor egy író folyamat lapokat ír: a másoló folyamat pontosan ugyanabba az átmeneti, "néhány lap régi, néhány új, egy lap félig írt" állapotba futhat bele, amit a dokumentum "torn page"-ként (részlegesen írt lapként) azonosít.

### Második és harmadik független megerősítés

**Második forrás (T1):** [SQLite Backup API](https://www.sqlite.org/backup.html), 1. szakasz, a "történelmi" (naiv) mentési módszer hátrányairól:
> "This procedure works well in many scenarios and is usually very fast. However, this technique has the following shortcomings: […] If a power failure or operating system failure occurs while copying the database file the backup database may be corrupted following system recovery."

**Harmadik forrás (T3, de a hivatalos SQLite fórumon, gyakorlati megerősítésként):** [SQLite Forum — "Backup via file system backup software"](https://sqlite.org/forum/info/796a192a95ac35b9), Simon Slavin hozzászólása (2021-04-25):
> "You cannot backup an open, changing, SQLite database and depend on getting a perfect uncorrupted backup. Because your backup doesn't take a snapshot of the database and its journal file all in the same instant, you will get inconsistencies."

A három forrás (két T1 hivatalos oldal + egy T3 fórum-megerősítés neves SQLite-közreműködőtől) egybehangzóan ugyanazt állítja: **a naiv, koordinálatlan fájlmásolás egy futó adatbázison korrupciót okozhat**, és a hivatalos dokumentáció ehhez pontosan három elfogadott alternatívát nevez meg.

---

## 2. A hivatalos mentési utak egyenként

### 2.1. Online Backup API (`sqlite3_backup_init/step/finish`)

**Forrás (T1):** [SQLite Backup API](https://www.sqlite.org/backup.html) + [C Interface referencia](https://www.sqlite.org/c3ref/backup_finish.html) (a második egy különálló, egymástól függetlenül szerkesztett hivatalos oldal — két T1 forrás).

**Mit garantál:**
> "The effect of completing the backup call sequence is to make the destination a bit-wise identical copy of the source database as it was when the copying commenced. (The destination becomes a 'snapshot.')"

**Blokkolja-e az írókat?** Nem folyamatosan. A referencia-oldal explicit módon leírja a zárolási modellt:
> "SQLite holds a write transaction open on the destination database file for the duration of the backup operation. The source database is read-locked only while it is being read; it is not locked continuously for the entire backup operation. Thus, the backup may be performed on a live source database without preventing other database connections from reading or writing to the source database while the backup is underway."

Tehát: a **cél**fájlon (az új backup-fájlon) folyamatos írás-zár van a teljes művelet alatt (ez a mi esetünkben irreleváns, mert a cél egy új, dedikált backup-fájl); a **forrás**on (az éles adatbázison) csak az egyes `sqlite3_backup_step()` hívások rövid időtartamára kerül shared lock.

**Újraindul-e írás közben?** Igen — a dokumentáció szó szerint kimondja, és ez a kutatási kérdés egyik kulcs-pontja:
> "Because the source database is not locked between calls to sqlite3_backup_step(), the source database may be modified mid-way through the backup process. If the source database is modified by an external process or via a database connection other than the one being used by the backup operation, then the backup will be automatically restarted by the next call to sqlite3_backup_step(). If the source database is modified by using the same database connection as is used by the backup operation, then the backup database is automatically updated at the same time."

A "Using the SQLite Online Backup API" oldal (backup.html, 3.1. szakasz) ugyanezt írja le, kiegészítve a **starvation** (soha be nem fejeződés) kockázatával — ez direkt válasz a kutatási kérdés "starvation" részére is (lásd 3. szakasz lent):
> "Whether or not the backup process is restarted as a result of writes to the source database mid-backup, the user can be sure that when the backup operation is completed the backup database contains a consistent and up-to-date snapshot of the original. However: Writes to an in-memory source database, or writes to a file-based source database by an external process or thread using a database connection other than pDb are significantly more expensive than writes made to a file-based source database using pDb (as the entire backup operation must be restarted in the former two cases). If the backup process is restarted frequently enough it may never run to completion and the backupDb() function may never return."

**Független (T3) megerősítés** — a Lobsters-en (Hacker-News-szerű közösségi oldal) egy hozzászóló szó szerint ugyanerre a hivatalos szövegre hivatkozva vonja le a gyakorlati következtetést ([lobste.rs vita](https://lobste.rs/s/zglr47/backup_strategies_for_sqlite_production), *letmetweakit*, 2024-09-14):
> "So if you backup on a different connection, and your live database is written frequently, your backup might never finish."

**A CLI `.backup` parancs viselkedése (forráskód-szintű T1 megerősítés, saját ellenőrzés):** a SQLite hivatalos Fossil-repójából (`sqlite.org/src`) letöltött `src/shell.c.in` forrás szerint a `.backup` (és `.save`) dot-parancs pontosan a fenti Backup API-t hívja:
```
pBackup = sqlite3_backup_init(pDest, "main", p->db, zDb);
while(  (rc = sqlite3_backup_step(pBackup,100))==SQLITE_OK ){}
sqlite3_backup_finish(pBackup);
```
**Fontos, a dokumentációban nem kiemelt részlet:** ez a ciklus **nem** implementál semmilyen alvást/újrapróbálkozást `SQLITE_BUSY`/`SQLITE_LOCKED` esetén (szemben a backup.html saját "Example 2" ajánlott mintakódjával, amely 250 ms-ot alszik és újrapróbálkozik BUSY/LOCKED esetén). A `while` ciklus feltétele kizárólag `==SQLITE_OK`; bármilyen más visszatérési érték (beleértve BUSY/LOCKED-et is) kilépteti a ciklusból, és a parancs hibaként kezeli, ha nem `SQLITE_DONE` az eredmény. **Következmény:** a beépített `.backup` CLI-parancs zárolási ütközés esetén egyszerűen elbukhat, ahelyett hogy kivárná a zárat — ezt semelyik hivatalos oldal nem mondja ki explicit szöveggel, ez a forráskód közvetlen olvasásából származó megállapítás (T1, de nem "idézhető" dokumentáció-szöveg, hanem kódrészlet).

### 2.2. `VACUUM INTO`

**Forrás (T1):** [VACUUM dokumentáció](https://www.sqlite.org/lang_vacuum.html), 2.1. szakasz.

**Melyik verziótól:** SQLite **3.27.0** (2019-02-07). Ellenőrizve közvetlenül a hivatalos [changelog](https://sqlite.org/releaselog/3_27_0.html) nyers HTML-jéből:
> "SQLite Release 3.27.0 On 2019-02-07 — Added the VACUUM INTO command"

**Tömörít-e:** Igen — ez az egyik fő különbség a Backup API-hoz képest. A `VACUUM INTO` a teljes adatbázist újratömöríti/deframentálja írás közben, míg a Backup API bájt-pontos, tömörítés nélküli másolatot készít.

**Mit garantál:**
> "If the INTO clause is included, then the original database file is unchanged and a new database is created in a file named by the argument to the INTO clause. […] The new database will contain the same logical content as the original database, fully vacuumed."
> "The VACUUM INTO command is transactional in the sense that the generated output database is a consistent snapshot of the original database."

**Mit NEM garantál:**
> "However, if the VACUUM INTO command is interrupted by an unplanned shutdown or power loss, then the generated output database might be incomplete and corrupt."

Ezt enyhíti a `synchronous` beállítás, ha az sikeresen lefutott:
> "However, if the PRAGMA synchronous setting of the original database is NORMAL or FULL, then SQLite invokes fsync() or FileFlushBuffers() to sync the output database to disk after it has been written. This means that in these cases, a power failure or unplanned shutdown that occurs after the VACUUM INTO command has completed should not corrupt the database (assuming the OS, file-system and hardware are functioning correctly)."

**Explicit, hivatalos összehasonlítás a Backup API-val (ez a kért "ajánlás" — pontosan idézve):**
> "The VACUUM command with an INTO clause is an alternative to the backup API for generating backup copies of a live database. The advantage of using VACUUM INTO is that the resulting backup database is minimal in size and hence the amount of filesystem I/O may be reduced. Also, all deleted content is purged from the backup, leaving behind no forensic traces. On the other hand, the backup API uses fewer CPU cycles and can be executed incrementally."

Vagyis a hivatalos "ajánlás" gyakorlatilag egy trade-off: `VACUUM INTO` → kisebb, "tisztább" (törölt adatoktól mentes) kimenet, több CPU; Backup API → kevesebb CPU, inkrementálisan futtatható, de nem tömörít és nem takarít.

**Zárolási különbség (finom, de fontos részlet, ugyanerről az oldalról):**
> "A VACUUM will fail if there is an open transaction on the database connection that is attempting to run the VACUUM. […] VACUUM (but not VACUUM INTO) is a write operation and so if another database connection is holding a lock that prevents writes, then the VACUUM will fail."

Ez azt jelenti, hogy a sima `VACUUM` (helyben-újraírás) elbukik, ha más kapcsolat írás-zárat tart, de a `VACUUM INTO` — mivel nem írja felül az eredeti fájlt — ebből a szempontból megengedőbb.

**Hogyan működik belülről (mechanika, ugyanaz az oldal, 3. szakasz):**
> "The VACUUM INTO command works the same way [mint a sima VACUUM] except that it uses the file named on the INTO clause in place of the temporary database and omits the step of copying the vacuumed database back over top of the original database."

### 2.3. `.backup` parancs a CLI-ben

Lásd fent (2.1. szakasz vége) — a CLI `.backup` parancsa **közvetlenül** a Backup API-t hívja (`sqlite3_backup_init/step(100 lapos lépésekben)/finish`), forráskód-szinten igazolva. A hivatalos [cli.html](https://www.sqlite.org/cli.html) dokumentáció csak a szintaxist adja meg:
> ".backup ?DB? FILE        Backup DB (default \"main\") to FILE"
> ".save ?OPTIONS? FILE     Write database to FILE (an alias for .backup ...)"

A `--safe` CLI-mód explicit kikapcsolja a `.backup`/`.save` parancsokat, jelezve, hogy ezek "fájlrendszerre kiható" (nem csak a fő adatbázisfájlt érintő) műveletnek számítanak:
> "The .backup and .save commands." — a `--safe` kapcsoló által letiltott parancsok listáján.

### 2.4. `.dump` (SQL szöveg)

**Forrás (T1):** [cli.html](https://www.sqlite.org/cli.html), 9. szakasz ("Converting An Entire Database To A Text File"):
> "Use the '.dump' command to convert the entire contents of a database into a single UTF-8 text file. This file can be converted back into a database by piping it back into sqlite3."
> "A good way to make an archival copy of a database is this: $ sqlite3 ex1 .dump | gzip -c >ex1.dump.gz"
> "The text format is pure SQL so you can also use the .dump command to export an SQLite database into other popular SQL database engines."

**Mikor jobb:** hordozhatóság (más SQL motorra is átvihető szöveges formátum), jól tömöríthető (SQL szöveg), és — forráskód-szintű saját ellenőrzés (T1, `shell.c.in`) alapján — a `.dump` a teljes olvasást egyetlen `SAVEPOINT dump;` blokkban végzi, ami (ha nincs már nyitott tranzakció) implicit tranzakciót indít; ez azt jelenti, hogy a `.dump` a WAL-mód snapshot-izolációja miatt **konzisztens, egy pillanatra vonatkozó olvasást** ad egy éppen változó adatbázison is — ugyanúgy, mint a Backup API vagy a `VACUUM INTO`. (Ez a részlet nincs kimondva egyik hivatalos leíró oldalon sem — közvetlenül a forráskódból derül ki, ezért csak T1-es kódbizonyítékként, nem dokumentum-idézetként kezelendő.)

**Mikor rosszabb:** a `cli.html` 10. szakasza ("Recover Data From a Corrupted Database") mellékesen megjegyzi a `.dump` egyik korlátját:
> "[…] whereas '.dump' stops when the first sign of corruption is encountered."

Azaz a `.dump` sérült adatbázison megáll, nem robusztus (ellentétben a `.recover` paranccsal). Emellett — T3, gyakorlati összegzés az Oldmoe blogból (lásd lent 4. szakasz is) — a `.dump` a legnagyobb helyigényű és leglassabb visszaállítású módszer az összes hivatalos opció közül, mert a bináris lapok helyett szöveges SQL-parancsokat generál soronként.

### Hivatalos ajánlás összefoglalva (a kért "melyiket mikor" kérdésre)

A hivatalos oldalak **nem adnak explicit "használd ezt, ne azt" ranglistát** — a `howtocorrupt.html` kifejezetten leszögezi: *"In no particular order"*. Az egyetlen explicit, kvantitatív trade-off-leírás a `lang_vacuum.html`-en található (idézve fent): **Backup API** = kevesebb CPU, inkrementális; **VACUUM INTO** = kisebb, tisztább kimenet, több CPU. A `.dump` és a nyers `cp` a `howtocorrupt.html`/`backup.html` szövegezéséből következtethetően inkább "van, de van jobb" kategóriák: a `.dump` hordozhatóságért cserébe lassúságot és helyet áldoz, a nyers `cp` csak szigorú előfeltételek (nincs nyitott tranzakció + WAL/journal fájl együtt-másolása) mellett biztonságos.

---

## 3. WAL-mód és a mentés kölcsönhatása

**Forrás (T1):** [Write-Ahead Logging](https://www.sqlite.org/wal.html).

**Elég-e a fő fájlt menteni WAL-módban?** **Nem elég önmagában.** A `howtocorrupt.html` (1.2. szakasz, idézve fent) kifejezetten kimondja, hogy ha `-wal` fájl létezik, azt a fő fájllal **együtt** kell másolni. A `wal.html` oldal is megerősíti a `-wal`/`-shm` fájlok "kvázi-permanens" jellegét:
> "There is an additional quasi-persistent \"-wal\" file and \"-shm\" shared memory file associated with each database, which can make SQLite less appealing for use as an application file-format."

**A `-wal` és `-shm` fájl sorsa:** amíg a WAL nincs teljesen checkpontolva és nullázva, a fő `.db` fájl **önmagában hiányos** — a legújabb, még nem checkpontolt tranzakciók csak a `-wal` fájlban léteznek. A `-shm` fájl a WAL-index megosztott memória-leképezése; írásjogosultság kell hozzá:
> "The opening process must have write privileges for '-shm' wal-index shared memory file associated with the database, if that file exists, or else write access on the directory containing the database file if the '-shm' file does not exist."

**Checkpoint mentés előtt — gyakorlati közösségi (T3) megoldás, hivatalos fórumból**, amely közvetlenül válaszol a kérdésre: elég-e a fő fájlt lementeni WAL után egy checkpont-tal? [SQLite Forum, "Backup via file system backup software"](https://sqlite.org/forum/info/796a192a95ac35b9), anonim hozzászóló (2022-07-17):
> "One easier method though is, while in WAL mode, do a FULL Wal checkpoint. After which you can copy the main db file, this is a pristine snapshot of the db status right after the checkpoint (as long as no other checkpoints are attempted while the file is being copied, you might want to disable auto checkpoint temporarily if it is on right before you do this)"

Ez egy **feltételes** válasz: igen, elég a fő fájlt menteni **egy `PRAGMA wal_checkpoint(FULL)` (vagy `RESTART`/`TRUNCATE`) után**, DE csak ha közben nem indul újabb checkpoint (amit auto-checkpoint kikapcsolásával kell biztosítani), és — ez a forrás nem mondja ki, de a hivatalos `wal_checkpoint` pragma-dokumentáció igen — a `FULL`/`RESTART` checkpoint **blokkolja a konkurens írókat**, amíg fut:
> "FULL — This mode blocks (invokes the busy-handler callback) until there is no database writer and all readers are reading from the most recent database snapshot. […] FULL blocks concurrent writers while it is running, but readers can proceed."
> "RESTART — This mode works the same way as FULL with the addition that after checkpointing the log file it blocks […] until all readers are finished with the log file. […] RESTART blocks concurrent writers while it is running, but allows readers to proceed."
> "TRUNCATE — This mode works the same way as RESTART with the addition that the WAL file is truncated to zero bytes upon successful completion." (Forrás: [pragma.html](https://www.sqlite.org/pragma.html))

Tehát a "checkpont, majd `cp` a fő fájlt" módszer **rövid ideig blokkolja az írókat** (a checkpont idejére), utána pedig — a checkpont és a `cp` közötti résben — **kockázatos**, mert bármely másik kapcsolat írhat és újraindíthatja a WAL-t, mielőtt a `cp` lefutna. Ez a hivatalos, kifejezetten a Backup API/VACUUM INTO/rsync mellett szóló érv: ezek a módszerek SQLite-szinten koordinálják a zárolást, a "checkpoint + cp" kézi módszer nem.

**Van-e olyan eset, ahol a mentés hosszú írás alatt nem fejeződik be (starvation)?** Igen, **két külön, dokumentált mechanizmus** van erre:

1. **Backup API starvcore (idézve fent, 2.1. szakasz):** *"If the backup process is restarted frequently enough it may never run to completion and the backupDb() function may never return."* — ez direkt a Backup API viselkedésére vonatkozik.

2. **Checkpoint starvation** — a `wal.html` saját, külön nevesített szakasza (4. rész, "Avoiding Excessively Large WAL Files"):
> "Checkpoint starvation. A checkpoint is only able to run to completion, and reset the WAL file, if there are no other database connections using the WAL file. If another connection has a read transaction open, then the checkpoint cannot reset the WAL file because doing so might delete content out from under the reader. […] However, if a database has many concurrent overlapping readers and there is always at least one active reader, then no checkpoints will be able to complete and hence the WAL file will grow without bound."

Ez a `wal.html`-en dokumentált jelenség nem közvetlenül a "mentésről" szól, hanem a checkpont-mechanizmusról — de mivel a checkpont a WAL→fő-fájl átvitel motorja, ez közvetlen hatással van minden olyan mentési stratégiára, amely feltételezi, hogy a WAL egy ponton "leürül": ha a szerveren folyamatosan van legalább egy aktív olvasó tranzakció, a checkpont sosem futhat le teljesen, és a WAL fájl korlátlanul nőhet. A dokumentáció ajánlott ellenszere:
> "This scenario can be avoided by ensuring that there are 'reader gaps': times when no processes are reading from the database and that checkpoints are attempted during those times. […] one might also consider running manual checkpoints with the SQLITE_CHECKPOINT_RESTART or SQLITE_CHECKPOINT_TRUNCATE option which will ensure that the checkpoint runs to completion before returning. The disadvantage […] is that readers might block while the checkpoint is running."

---

## 4. Mérési adatok: időtartam és blokkolás

**Ez az a kérdéskör, ahol a hivatalos SQLite-dokumentáció NEM ad számokat.** Sem a `backup.html`, sem a `lang_vacuum.html`, sem a `wal.html` nem közöl semmilyen teljesítmény-benchmarkot ("X GB adatbázis Y másodperc alatt"). Ez önmagában is megállapítás — lásd `hianyok.md`.

Amit **közösségi méréssel (kifejezetten T3-ként jelölve)** sikerült találni:

**T3 — `cp --reflink=always` (Btrfs/XFS Copy-on-Write reflink-másolás), NEM a Backup API vagy VACUUM INTO, hanem a nyers fájlmásolás CoW-optimalizált változata:** [Oldmoe blog, "Backup strategies for SQLite in production"](https://oldmoe.blog/2024/04/30/backup-strategies-for-sqlite-in-production/) (2024-04-30, [Hacker News](https://news.ycombinator.com/item?id=41618117) és [Lobsters](https://lobste.rs/s/zglr47/backup_strategies_for_sqlite_production) is tárgyalta, tehát legalább két független közösségi fórum reagált rá és nem cáfolta a mérést):
> "On a VM with attached block storage hosting both the source and destination databases this operation takes ~2ms to complete for a 440MB database file. The same ~2ms are required to copy a 4.4GB database file as well." … "No extra space was used (actually a tiny bit of space for the file metadata)."

**Fontos korlátozás erre a számra:** ez **nem** a Backup API vagy a `VACUUM INTO` mérése, hanem a `cp --reflink=always` (metaadat-szintű, blokk-megosztásos) másolásé Btrfs-en — ami azért ilyen gyors (2 ms, mérettől függetlenül), mert nem másol tényleges adatlapokat, csak a fájlrendszer B-tree metaadatait duplikálja. Ez a szám **nem extrapolálható** a Backup API-ra vagy a `VACUUM INTO`-ra, amelyek ténylegesen lapokat olvasnak/írnak/tömörítenek, tehát a méret és az I/O-sebesség lineárisan számít.

**A Backup API és a `VACUUM INTO` tényleges (lapmásoló/tömörítő) időtartamára és a blokkolás mértékére konkrét, számszerű, méret szerinti mérést — sem hivatalosat, sem megbízható közösségit — nem találtam.** A kereséseim (lásd `keresesek.md`) nem hoztak fel konkrét "X GB → Y másodperc" jellegű, hitelesnek tekinthető, méret-specifikus benchmarkot egyik SQLite-fórumon, GitHub issue-ban vagy blogban sem. Az egyetlen kapcsolódó, de nem pontosan ide illő adat a SQLite fórum "wal checkpointing very slow" szála volt ([sqlite.org/forum/info/aa9fde5a28abc442](https://sqlite.org/forum/info/aa9fde5a28abc442)), amely kvalitatív (nem számszerű) leírást ad arról, hogy a checkpont miért lehet lassabb, mint a nyers írás, de konkrét mérőszámot ez sem közöl.

**Ami levezethető elméletileg (T1, mechanika alapján, nem mérés):**
- A Backup API alapból **nem** blokkol folyamatosan (csak lépésenként, rövid ideig zárolja a forrást) — ld. 2.1. szakasz.
- A `VACUUM INTO` a teljes adatbázist újraírja/tömöríti, ezért I/O- és CPU-igénye az eredeti adatbázis méretével arányos, és — mivel nem írja felül az eredetit — **nem blokkolja** más kapcsolatok írásait a forrás oldalán (ellentétben a sima `VACUUM`-mal, ld. 2.2. szakasz zárolási idézete).
- Egy `PRAGMA wal_checkpoint(FULL)` vagy `(RESTART)` **igen**, blokkolja a konkurens írókat, amíg fut (idézve fent, 3. szakasz) — ez a legvalószínűbb pont, ahol egy "checkpoint majd mentés" stratégia ténylegesen érzékelhető szünetet okoz az íróknak, de ennek időtartamára sincs hivatalos szám.

**Összefoglalva:** a mért idő/blokkolás kérdésre a válasz jelentős részben **hiány** — ezt explicit módon jelzem a `hianyok.md`-ben, nem találtam ki számokat.

---

## 5. Litestream és hasonló folyamatos replikáció

**Forrás (T1):** [litestream.io](https://litestream.io/) hivatalos dokumentáció, nyers HTML-ből letöltve (`how-it-works`, `tips`, `alternatives`, `guides/directory` oldalak).

**Mit replikál pontosan:**
> "Litestream is a streaming replication tool for SQLite databases. It runs as a separate background process and continuously copies write-ahead log pages from disk to a replica. This asynchronous replication provides disaster recovery similar to what is available with database servers like Postgres or MySQL."

A jelenlegi (v0.5.x) architektúra a WAL-lapokat "LTX" (Litestream Transaction Log) fájlokba csomagolja, monoton növekvő tranzakció-azonosítóval (TXID), és rétegzett kompaktálást (L0→L1→L2→L3 + napi snapshot) végez — ez egy jelentős architekturális váltás a korábbi v0.3.x "generation"-alapú, árnyék-WAL-fájlos megközelítéshez képest (a dokumentáció ezt maga is jelzi: *"Earlier v0.3.x releases tracked replication state using randomly-generated 'generation' IDs and a directory of shadow WAL files. Litestream v0.5 replaces both concepts with TXID-based LTX files."*). **Ez fontos verzió-függőség**, amit egy mai kiértékelésnél figyelembe kell venni.

**Mekkora adatvesztéssel (a kért, konkrét kérdés):**
> "By default, Litestream will replicate new changes to an S3 replica every second. During this time where data has not yet been replicated, a catastrophic crash on your server will result in the loss of data in that time window."
> "For more typical shutdown scenarios, when Litestream receives a signal to close, it will attempt to synchronize all outstanding WAL changes to the S3 replica before terminating."
> "Synchronous replication is on the Litestream roadmap but has not yet been implemented."

Vagyis: **legfeljebb kb. 1 másodpercnyi** adatvesztés egy hirtelen (nem tiszta) leállás/összeomlás esetén, alapértelmezett konfiguráció mellett; tiszta leállásnál (SIGTERM/SIGINT) a dokumentáció szerint Litestream megpróbálja szinkronizálni a hátralévő WAL-változásokat, mielőtt kilépne — de ez "megpróbálja" (attempt), nem garantált nulla adatvesztés.

**Megkötések (explicit, hivatalos):**
- **Csak WAL módban működik:** *"Litestream only works with the SQLite WAL journaling mode. […] Litestream will automatically set the database mode to WAL if it has not already been enabled by the application."*
- **Adatbázisonként egy replika-cél:** *"Each database replicates to a single replica destination. If you need multiple backup destinations, see the replica settings section of the configuration reference for alternatives."*
- **A checkpontolást "elveszi" a rendszertől:** *"Litestream works by effectively taking over the checkpointing process. It starts a long-running read transaction to prevent any other process from checkpointing and restarting the WAL file."* — ez azt jelenti, hogy Litestream futtatásakor a checkpontolás menetét gyakorlatilag Litestream vezérli, nem az alkalmazás vagy a SQLite auto-checkpoint mechanizmusa.
- **Nem véd több, egyszerre ugyanoda replikáló alkalmazás ellen:** *"Multiple applications replicating into the same bucket & path can cause situations where you will be unable to restore. It is your responsibility to ensure you do not have multiple applications replicating concurrently."*
- **Busy timeout beállítás szükséges az alkalmazás oldalán:** *"Litestream requires periodic but short write locks on the database when checkpointing occurs. SQLite will return an error by default if your application tries to obtain a write lock at the same time. […] It is recommended to set this to 5 seconds: PRAGMA busy_timeout = 5000;"*

**Működik-e több adatbázissal:** **Igen**, egyetlen Litestream-folyamat több SQLite-fájlt is replikálhat — vagy explicit `dbs:` lista, vagy `dir:`+`pattern:` alapú könyvtár-szkennelés formájában ([Replicating Directories útmutató](https://litestream.io/guides/directory/)):
> "Directory replication is useful for: Multi-tenant applications where each tenant has their own database; Applications managing multiple SQLite databases; Batch replication without listing each database individually"

**Fontos, a kérdés szempontjából kulcsfontosságú negatív megállapítás:** a több adatbázisos (`dbs:`/`dir:`) dokumentáció **egyáltalán nem említ** semmilyen kereszt-adatbázis konzisztencia-garanciát. Minden adatbázis **teljesen független** replikációs folyamot kap, saját TXID-sorozattal, saját metaadat-könyvtárral, saját snapshot-ütemezéssel:
> "Each database in a directory gets a unique replica path by appending its relative path from the directory root. This ensures isolated storage with no collision risk." … "Each database receives a unique metadata directory under the root, mirroring its relative path"

Vagyis Litestream **nem** ad semmilyen mechanizmust arra, hogy két külön adatbázis (a mi esetünkben: felhasználói DB + index DB) mentései egyazon logikai pillanatot tükrözzenek. Ez közvetlenül releváns a 6. kérdésre.

**Hátránya egy kis, egygépes rendszernél — a hivatalos "Alternatives" oldal saját szavaival:**
> "Litestream aims to provide a balance between durability and operational complexity by batching changes into one-second windows and asynchronously backing those changes up to external storage. This improves write performance at the expense of having a small window of data loss in the event of a catastrophic failure. However, this tradeoff may not make sense for all applications."
> "Periodic SQLite backups — Sometimes Litestream can be overkill for projects with a small database that do not have high durability requirements. In these cases, it may be more appropriate to simply back up your database daily or hourly. This approach can also be used in conjunction with Litestream as a fallback."

Ez maga a Litestream hivatalos dokumentációja mondja ki: **kis, alacsony durability-igényű projekteknél a Litestream "overkill" lehet**, és a periodikus (`VACUUM INTO`/Backup API alapú) mentés önmagában is elfogadható — sőt, kombinálhatók.

**Gyakorlati (T2/T3) hátrányok, amiket a hivatalos dokumentáció nem, de a közösségi tapasztalat igen kiemel** ([Lobsters-vita](https://lobste.rs/s/zglr47/backup_strategies_for_sqlite_production), *dhnaranjo*, 2024-09-15):
> "I used Litestream […] and found it excellent once I was done feeling like an absolute fraud because of how much trouble I had initially setting it up."

— vagyis a beüzemelés (S3-kompatibilis object storage szükséges, konfiguráció, monitorozás) nem triviális egy olyan kis, egygépes rendszernél, ahol amúgy sincs meglévő objektumtár-infrastruktúra. Ez összhangban van azzal, amit a hivatalos "Alternatives" oldal is elismer (lásd fent).

---

## 6. Két adatbázis egymáshoz képesti konzisztenciája — VAN-E BEVETT MEGOLDÁS?

Ez a legfontosabb, legkevésbé megnyugtató válasszal záruló kérdés — **explicit módon kimondom: nincs bevett, általános megoldás erre a konkrét esetre** (két külön SQLite-fájl, folyamatosan futó szerver, WAL mód), és ezt több, egymástól független forrás támasztja alá.

### 6.1. A SQLite saját, beépített többfájlos atomicitás-mechanizmusa — és miért nem alkalmazható itt

A SQLite-nak **van** saját mechanizmusa több adatbázisfájl közötti atomi tranzakcióra: az `ATTACH DATABASE` + "super-journal" (más néven "master journal") fájl. Ez T1 forrásból, az [Atomic Commit In SQLite](https://www.sqlite.org/atomiccommit.html) dokumentum 5. szakaszából ("Multi-file Commit"):
> "SQLite allows a single database connection to talk to two or more database files simultaneously through the use of the ATTACH DATABASE command. When multiple database files are modified within a single transaction, all files are updated atomically."

**DE** — és ez a kulcs-korlátozás — ez a mechanizmus kifejezetten **nem működik WAL módban**. A hivatalos [`ATTACH` dokumentáció](https://www.sqlite.org/lang_attach.html) szó szerint kimondja:
> "Transactions involving multiple attached databases are atomic, assuming that the main database is not \":memory:\" and the journal_mode is not WAL. If the main database is \":memory:\" or if the journal_mode is WAL, then transactions continue to be atomic within each individual database file. But if the host computer crashes in the middle of a COMMIT where two or more database files are updated, some of those files might get the changes where others might not."

Ezt **T3-as, de a hivatalos SQLite fórumon zajló, gyakorlati megbeszélés is megerősíti és pontosítja** ([SQLite Forum, "Transactions involving multiple databases"](https://sqlite.org/forum/forumpost/ecf53d4eb8), Keith Medcalf, 2020-12-10):
> "in the case where the journal_mode is not WAL […] and the main database (and the attached database) is not :memory: […] THEN two-phase commit is used to maintain consistency across attached database files. However, if there [sic] conditions are NOT complied with (that is, one of the databases involved is a :memory: database, or the main database is a :memory: database, or the journal mode is not rollback using rollback files on persistent (disk) storage) that two-phase commit WILL NOT BE USED"

**Ez közvetlenül releváns a mi rendszerünkre:** a leírt `easter-memory-system` egy folyamatosan futó, konkurens írásokat fogadó szerver, aminél a WAL mód gyakorlatilag elvárt (a rollback-journal mód nem engedi meg egyidejű olvasást és írást ugyanolyan hatékonysággal). Ha viszont WAL módban futnak a fájlok, a SQLite saját `ATTACH`-alapú, beépített kereszt-fájl atomicitása **nem alkalmazható** — még akkor sem, ha valaki egyetlen kapcsolatból, `ATTACH`-csal kötné össze a két adatbázist.

**Fontos módszertani megjegyzés:** ez a mechanizmus egyébként is *tranzakciós* atomicitásról szól (egyetlen `COMMIT`, ami mindkét fájlt módosítja), nem *mentésről*. A kérdés ("ha két külön SQLite fájlt mentek külön-külön, a két mentés nem egy időpontot mutat") egy ennél is gyengébb, de gyakorlatilag ugyanabból a problémából fakadó eset: még ha a rendszer maga sosem futtat is egyetlen közös tranzakciót a két adatbázison, a **mentési** művelet két külön időpontban készül, tehát a két mentés közötti résben történt bármilyen írás (pl. egy új felhasználó rögzítése, ami az index frissítését is kellene, hogy kiváltsa) inkonzisztenciát okozhat a két mentés között.

### 6.2. Van-e bármilyen általános eszköz, ami ezt megoldja két *külön* SQLite-fájlra?

**Nem találtam ilyet.** Konkrétan:

- A **Backup API** és a **`VACUUM INTO`** kizárólag **egyetlen** adatbázisra vonatkoznak; nincs "backupold ezt a két fájlt egy közös, koordinált pillanatban" hivatalos parancs vagy API.
- A **Litestream** dokumentációja (lásd 5. szakasz) kifejezetten **adatbázisonként külön, egymástól független replikációs folyamot** ír le, kereszt-adatbázis konzisztencia-garancia **nélkül**.
- A fájlrendszer-szintű, "crash consistent" pillanatkép-alapú megoldások (VSS Windows-on, APFS snapshot macOS-en, ZFS/Btrfs snapshot Linuxon) **elméletileg** megoldanák ezt, mert egyetlen atomi műveletben fagyasztják be a teljes fájlrendszert (mindkét .db/.wal/.shm fájlt egyszerre) — ezt a hivatalos SQLite fórum-vita is megerősíti (T3, de technikailag pontos és több hozzászóló egyetért vele — [uo. forum-szál](https://sqlite.org/forum/info/796a192a95ac35b9), Keith Medcalf, RandomCoder, 2021–2022 közötti hozzászólások):
> "This is in contrast to backup software which operates on a 'snapshot' of the filesystem that is maintained consistent from the start of the backup of that filesystem to the end of the backup of that filesystem (this is called 'Crash Consistent'…)"
> "Most any Windows backup solution, including the built in one, will use Volume Shadow Copy Service. VSCS is similar to APFS's Snapshot, providing the backup software with a consistent point in time copy of a database file (along with the journal files) regardless of what's going on on the machine during the backup operation."

  **DE**: (a) ez a mi esetünkben **fájlrendszer-függő** megoldás (ZFS/Btrfs/LVM szükséges, sima ext4-en `cp --reflink` sem elérhető), nem "SQLite-os" megoldás, és a kutatási feladat kifejezetten kizárta a vektor-DB-t és PostgreSQL-t, de nem tér ki fájlrendszer-szintű snapshotra — ez tehát egy **lehetséges**, de a kérdésben fel nem tett, infrastruktúra-szintű válasz, amit nem SQLite, hanem az OS/fájlrendszer ad; (b) egy ilyen snapshot még mindig csak **"crash consistent"** — vagyis olyan állapotot ad vissza, mintha a gép abban a pillanatban áramkimaradást szenvedett volna el. A SQLite ebből az állapotból helyre tudja állítani **saját magát** (WAL/journal lejátszásával), de ez nem jelenti azt, hogy a két adatbázis (user DB, index DB) *tartalma* logikailag konzisztens egymással — csak azt, hogy mindkettő önmagában ép lesz.
- Nem találtam a `sqlite3_rsync` dokumentációjában sem (T1, [rsync.html](https://www.sqlite.org/rsync.html)) semmilyen többfájlos/kereszt-adatbázis funkciót — az kifejezetten egyetlen fájlra vonatkozó, SSH-alapú remote-copy eszköz.

### 6.3. Mit tesznek a gyakorlatban — "mindenki külön menti és elfogadja"?

A begyűjtött közösségi anyagokban (Oldmoe blog, Lobsters-vita, SQLite fórum) **egyetlen szerző sem tárgyalja kifejezetten** a "két külön SQLite-adatbázis kereszt-konzisztens mentése" problémát mint önálló témát — mindegyik forrás egyetlen adatbázisfájl mentési stratégiáiról beszél. Ez önmagában erős közvetett bizonyíték arra, hogy **a probléma nem egy bevetten kezelt, elterjedt minta**, hanem vagy (a) a legtöbb gyakorlati rendszer egyetlen SQLite-fájlt használ (elkerülve a kérdést), vagy (b) a több-DB-s rendszerek üzemeltetői egyszerűen elfogadják a kis inkonzisztencia-ablakot, vagy alkalmazás-szintű, egyedi megoldást építenek (pl. az index adatbázis eldobható és markdown-ból újraépíthető — ami pontosan az `easter-memory-system` saját tervezési válasza erre a problémára, a kontextus-leírás szerint).

**Konklúzió erre a kérdésre (explicit, nem kitalált válasz):** **nincs bevett, általános, hivatalosan dokumentált SQLite- vagy Litestream-szintű megoldás** két külön adatbázisfájl kereszt-konzisztens mentésére. Az egyetlen SQLite-natív mechanizmus (`ATTACH` + super-journal) kifejezetten **nem működik WAL módban**, ami egy konkurens, folyamatosan futó szerver esetén szinte elkerülhetetlen üzemmód. A fájlrendszer-szintű atomikus snapshot (ZFS/Btrfs/VSS/APFS) az egyetlen olyan technika, ami elméletileg egy pillanatban tudná mindkét fájlt (és azok WAL-jait) befagyasztani, de ez OS/fájlrendszer-függő infrastruktúra-döntés, nem SQLite-funkció, és csak "crash consistent" (nem logikailag garantált konzisztens) állapotot ad. Erre a konkrét kérdésre — pontosan a feladat által kért módon — **ki kell mondani a hiányt**: nincs rá kényelmes, dobozból kész válasz.



---

# sq03 — Séma-migráció és verziófrissítés futó rendszeren

# sq03 — Séma-migráció és verziófrissítés egy futó rendszeren: megállapítások

Kutatási kérdés kontextusa: `easter-memory-system` — markdown fájlok mint igazságforrás, két SQLite adatbázis
(felhasználók/jogosultságok Better Authtal; eldobható FTS5 keresési index), Node/Bun, Drizzle ORM, Docker,
**egy gép, egy cég, néhány felhasználó**. A cél eldönteni: kell-e kötelező mentés minden migráció/frissítés előtt,
és mennyire releváns az expand–contract minta egy ilyen kis rendszernél.

Tier-jelölés: **T1** = hivatalos dokumentáció / forráskód / elsődleges forrás. **T2** = megbízható másodlagos forrás
(szakcikk, gyártói blog, elismert szerző esszéje). **T3** = fórum, közösségi vita, blogposzt, anekdota.

Minden idézet a hivatalos oldal nyers HTML-jéből lett kinyerve (`curl` a proxyn keresztül, majd tag-stripelés),
kivéve ahol külön jelölve van, hogy WebFetch-csel történt (mert a curl 403-at kapott).

---

## 1. Drizzle migrációs modell

### 1.1 A három alap-munkafolyamat: `generate` / `migrate` / `push`

**[T1]** A `drizzle-kit generate` a hivatalos leírás szerint:

> „Drizzle Kit generate command triggers a sequence of events: It will read through your Drizzle schema file(s)
> and compose a json snapshot of your schema. It will read through your previous migrations folders and compare
> current json snapshot to the most recent one. Based on json differences it will generate SQL migrations.
> Save migration.sql and snapshot.json in migration folder under current timestamp"

Forrás: https://orm.drizzle.team/docs/drizzle-kit-generate (nyers HTML letöltve, tag-stripelve)

**[T1]** A `drizzle-kit migrate` a hivatalos leírás szerint:

> „Drizzle Kit migrate command triggers a sequence of events: Reads through migration folder and read all .sql
> migration files. Connects to the database and fetches entries from drizzle migrations log table. Based on
> previously applied migrations it will decide which new migrations to run. Runs SQL migrations and logs applied
> migrations to drizzle migrations table"

Forrás: https://orm.drizzle.team/docs/drizzle-kit-migrate

**[T1]** A `drizzle-kit push` közvetlenül az adatbázisra alkalmazza a séma-diffet, generált SQL-fájlok nélkül
(„push your schema directly to the database"; lásd „Fundamentals › Migrations" oldal, Option 2). Ez a
gyors prototípus-készítésre ajánlott mód: „That's the best approach for rapid prototyping and we've seen dozens
of teams and solo developers successfully using it as a primary migrations flow in their production applications."
Forrás: https://orm.drizzle.team/docs/migrations

**[T1] Fontos guardrail a `push`-nál** — a `drizzle-kit push` CLI-opciói között:

> „verbose — print all SQL statements prior to execution
> explain — print the planned SQL changes, without applying them (dry run)
> force — auto-accept all data-loss statements"

Forrás: https://orm.drizzle.team/docs/drizzle-kit-push

Vagyis alapértelmezésben a `push` **megállítja és megerősítést kér** minden adatvesztéssel járó (destruktív)
változtatás előtt; ez a `--force` nélkül futtatva egyfajta beépített védőháló — bár nem helyettesíti a mentést,
csökkenti a véletlen adatvesztés kockázatát interaktív használat esetén.

A teljes parancslista a hivatalos overview oldalon (nincs `down`, `undo`, `rollback` parancs közte):

> „npx drizzle-kit generate / migrate / push / pull / check / up / studio / export"

Forrás: https://orm.drizzle.team/docs/kit-overview

### 1.2 Van-e visszagörgetés (rollback / down migration)?

**[T1] Nincs hivatalos „down migration" vagy „rollback" CLI-parancs vagy funkció Drizzle Kit-ben.** A teljes
parancslista (fent) kimerítő, és egyik hivatalos oldal sem dokumentál semmilyen `undo`/`down`/`rollback` parancsot
vagy migrációs fájltípust (szemben pl. Rails „down" metódusával vagy Flyway „undo" migrációjával — lásd lentebb).

Az egyetlen, rollback-hez közeli hivatalos mondat kétértelmű és **nem CLI-funkcióra**, hanem az alkalmazás saját
deploy-folyamatára utal:

> „This approach is widely used for monolithic applications when you apply database migrations during zero
> downtime deployment and rollback DDL changes if something fails."

Forrás: https://orm.drizzle.team/docs/migrations (4. opció: futásidejű `migrate()` hívás)

Ez a mondat nem specifikál semmilyen konkrét mechanizmust arra, *hogyan* történne a „rollback" — nincs hozzá
kapcsolódó API, parancs vagy fájlformátum (nincs pl. `0001_xxx.down.sql`). Ezt megerősíti a közösségi visszajelzés:

**[T2/T3]** GitHub issue, nyitott feature request (2026-ban is nyitva): „[FEATURE]: Reverse/Down Migrations" —
https://github.com/drizzle-team/drizzle-orm/issues/4005 — vagyis a fejlesztők maguk is hiányként kezelik.

**[T2/T3]** GitHub Discussion: „Migrations Rollback" — https://github.com/drizzle-team/drizzle-orm/discussions/1339
— közösségi kérdés/vita arról, hogyan lehetne rollbackelni, ami szintén azt jelzi, hogy nincs beépített út erre.

**[T2/T3]** GitHub issue: „[BUG]: Drizzle migration does not rollback if it fails" —
https://github.com/drizzle-team/drizzle-orm/issues/2510 — még a *sikertelen* migráció automatikus
visszagörgetése is hibásan működött egyes driver-kombinációknál (nem garantált).

**[T1] Forráskód-szintű megerősítés** (`drizzle-orm` repó, `main` ág, `sqlite-core/dialect.ts`,
`SQLiteSyncDialect.migrate` és `SQLiteAsyncDialect.migrate`):

```ts
session.run(sql`BEGIN`);
try {
  for (const migration of migrations) {
    ...
    for (const stmt of migration.sql) {
      session.run(sql.raw(stmt));
    }
    ...
  }
} catch (e) {
  session.run(sql`ROLLBACK`);
  throw e;
}
session.run(sql`COMMIT`);
```//megrövidítve, a lényeg: egy tranzakcióban fut minden még nem alkalmazott migráció

Async változat: `await session.transaction(async (tx) => { ... })`.

Forrás: https://raw.githubusercontent.com/drizzle-team/drizzle-orm/main/drizzle-orm/src/sqlite-core/dialect.ts

**Értelmezés:** ez a „rollback" **csak a folyamatban lévő tranzakció** visszagörgetése hiba esetén (SQLite szintű
`ROLLBACK`), **nem** egy korábbi séma-verzióhoz való visszatérés funkció. Ha egy migráció sikeresen lefutott és
*utólag* derül ki, hogy hibás volt, a Drizzle Kit-nek nincs eszköze ennek visszacsinálására — ehhez vagy kézzel
írt „ellentétes" SQL migrációt kell generálni (`drizzle-kit generate --custom`), vagy vissza kell állítani egy
mentésből.

**Összegzés:** a hivatalos dokumentáció **nem mondja ki kifejezetten**, hogy „nincs rollback", de a parancslista
kimerítő felsorolása, a forráskód, és a többszörös, egymástól független közösségi visszajelzés (feature-kérés,
vita, bugjelentés) mind ugyanazt támasztja alá: **nincs beépített, tervezett séma-visszagörgetési mechanizmus.**
Ez közvetlen ellentétben áll pl. Rails-szel (natív `down`/`revert`) és Liquibase-szel (dedikált `rollback`
parancscsalád), és részleges ellentétben Flyway-jel (van „Undo Migration", de az fizetős Teams-funkció — lásd 5. pont).

### 1.3 Nyers SQL és több-utasításos migráció kezelése — pontosvessző vagy egyéb?

**[T1] Nem pontosvessző mentén vág.** A migrációs fájlokat beolvasó és feldolgozó függvény
(`readMigrationFiles`, `drizzle-orm/src/migrator.ts`) szó szerint egy egyedi elválasztó string mentén darabol:

```ts
const result = query.split('--> statement-breakpoint').map((it) => it);
```

Forrás: https://raw.githubusercontent.com/drizzle-team/drizzle-orm/main/drizzle-orm/src/migrator.ts
(a `migrator.ts` maga csak re-exportál egy `migrator-common.ts`-ből; a tényleges kód ugyanezen az útvonalon
elérhető és letöltve lett — a fenti idézet a ténylegesen futó kódból származik).

Ez azt jelenti, hogy egy migrációs `.sql` fájlon belül a `drizzle-kit generate` explicit `--> statement-breakpoint`
jelölőket szúr be az egyes SQL utasítások közé (ha a `breakpoints` beállítás — alapértelmezetten `true` —
engedélyezve van), és a futtató kód **ez alapján**, nem pontosvessző alapján bontja szét a fájlt futtatható
egységekre. Ennek oka (nem dokumentált explicit módon, de következik a tervezésből): egyes SQL dialektusokban
(pl. tárolt eljárások, triggerek létrehozásakor) a pontosvessző az utasításon *belül* is előfordulhat, így a
naiv pontosvessző-vágás hibás darabolást eredményezne.

**[T1]** A `drizzle-kit generate` config-opciók között:

> „breakpoints — SQL statements breakpoints, default is true"

Forrás: https://orm.drizzle.team/docs/drizzle-kit-generate

**[T1]** A tényleges végrehajtás (SQLite szinkron dialektus) minden egyes darabolt utasítást külön futtat:

```ts
for (const stmt of migration.sql) {
  session.run(sql.raw(stmt));
}
```

Forrás: fent idézett `sqlite-core/dialect.ts`.

**Több migrációs fájl** esetén a `migrate` parancs a `meta/_journal.json` alapján dönti el, mely fájlokat még
nem alkalmazta (a `__drizzle_migrations` naplótábla `hash`/`created_at` mezői alapján), és a nem alkalmazottakat
sorban, egy közös tranzakcióban futtatja le (lásd 1.2 pont forráskódja).

**[T1] Kézzel írt (custom) migráció** — ha a Drizzle Kit diffelő motorja nem tud lekövetni egy DDL-változtatást
(pl. FTS5 virtuális tábla létrehozása, ami nem Drizzle-séma-objektum), a hivatalos ajánlás az üres migrációs fájl
generálása és kézi feltöltése:

> „You can generate empty migration files to write your own custom SQL migrations for DDL alternations currently
> not supported by Drizzle Kit or data seeding, which you can then run with drizzle-kit migrate command."
> ```
> drizzle-kit generate --custom --name=seed-users
> ```

Forrás: https://orm.drizzle.team/docs/kit-custom-migrations — **ez pontosan az `easter-memory-system` FTS5
triggerek/virtuális tábla esetére vonatkozó, hivatalosan ajánlott út.**

---

## 2. SQLite-specifikus migrációs korlátok

### 2.1 Mit tud az `ALTER TABLE`

**[T1]** Az official SQLite `ALTER TABLE` oldal (https://sqlite.org/lang_altertable.html) szerint az egyetlen,
közvetlenül támogatott almondatok:

> „The only schema altering commands directly supported by SQLite are the ‘rename table', ‘rename column',
> ‘add column', ‘drop column' commands shown above."

(Kiegészítve 2026 tavaszán, SQLite 3.53.0-tól: `ALTER TABLE ... ALTER COLUMN ... SET/DROP NOT NULL` — de
**kizárólag** a NOT NULL megkötés be- vagy kikapcsolására, semmi másra:

> „The ability to set or drop NOT NULL constraints from a column using the ALTER TABLE ALTER COLUMN syntax was
> added in SQLite 3.53.0 (2026-04-09).")

**ADD COLUMN korlátai (szó szerint):**

> „The column may not have a PRIMARY KEY or UNIQUE constraint. The column may not have a default value of
> CURRENT_TIME, CURRENT_DATE, CURRENT_TIMESTAMP, or an expression in parentheses. If a NOT NULL constraint is
> specified, then the column must have a default value other than NULL. If foreign key constraints are enabled
> and a column with a REFERENCES clause is added, the column must have a default value of NULL. The column may
> not be GENERATED ALWAYS ... STORED, though VIRTUAL columns are allowed."

**DROP COLUMN csak akkor sikerül, ha a mezőt semmi más nem hivatkozza:**

> „The DROP COLUMN command only works if the column is not referenced by any other parts of the schema and is
> not a PRIMARY KEY and does not have a UNIQUE constraint." — majd egy 8 pontos lista a lehetséges hibaokokról
> (PRIMARY KEY része, UNIQUE megkötés, indexelt, partial index WHERE-ében szerepel, CHECK-ben szerepel, foreign
> key-ben szerepel, generált oszlop kifejezésében szerepel, trigger/view-ban szerepel).

**Hogyan működik belül:**

> „SQLite stores the schema as plain text in the sqlite_schema table. All ALTER TABLE commands modify that text
> and then attempt to reparse the entire schema. The command is only successful if the schema is still valid
> after the text has been modified."

Ez az **oka** annak, hogy az SQLite ALTER TABLE-je ilyen korlátozott (lásd 2.5 pont, „miért probléma").

Forrás mindhez: https://sqlite.org/lang_altertable.html (nyers HTML, tag-stripelve)

**[T2/T3] Két független megerősítés a korlátokra:**
- https://jvns.ca/til/alter-table-foreign-keys/ — Julia Evans blogja, konkrétan a DROP COLUMN + foreign key
  korlátról
- https://sqlite-users.sqlite.narkive.com és hasonló fórumok, ill. gyakorlati útmutatók (pl.
  https://synkee.com.sg/blog/safely-modify-sqlite-table-columns-with-production-data/) ugyanezt a 12-lépéses
  eljárást írják le másodlagos forrásként.

### 2.2 A 12 lépéses tábla-átépítési recept (szó szerint)

**[T1]** A hivatalos „Making Other Kinds Of Table Schema Changes" szakasz (8. pont) adja meg a **hivatalosan
kimondott, egyedüli javasolt eljárást** tetszőleges szerkezeti változtatásra:

> „The steps to make arbitrary changes to the schema design of some table X are as follows:
> 1. If foreign key constraints are enabled, disable them using PRAGMA foreign_keys=OFF.
> 2. Start a transaction.
> 3. Remember the format of all indexes, triggers, and views associated with table X. This information will be
>    needed in step 8 below. One way to do this is to run a query like the following:
>    SELECT type, sql FROM sqlite_schema WHERE tbl_name='X'.
> 4. Use CREATE TABLE to construct a new table "new_X" that is in the desired revised format of table X. Make
>    sure that the name "new_X" does not collide with any existing table name, of course.
> 5. Transfer content from X into new_X using a statement like: INSERT INTO new_X SELECT ... FROM X.
> 6. Drop the old table X: DROP TABLE X.
> 7. Change the name of new_X to X using: ALTER TABLE new_X RENAME TO X.
> 8. Use CREATE INDEX, CREATE TRIGGER, and CREATE VIEW to reconstruct indexes, triggers, and views associated
>    with table X. […]
> 9. If any views refer to table X in a way that is affected by the schema change, then drop those views using
>    DROP VIEW and recreate them with whatever changes are necessary […]
> 10. If foreign key constraints were originally enabled then run PRAGMA foreign_key_check to verify that the
>     schema change did not break any foreign key constraints.
> 11. Commit the transaction started in step 2.
> 12. If foreign keys constraints were originally enabled, reenable them now."

(A dokumentum maga „12-step generalized ALTER TABLE procedure"-ként hivatkozik erre a lentebbi bekezdésben —
tehát a „12 lépés" **a hivatalos dokumentáció saját elnevezése**, nem külső interpretáció.)

**Kritikus figyelmeztetés a helyes sorrendre** (miért nem szabad előbb átnevezni a régi táblát):

> „Take care to follow the procedure above precisely. […] In the procedure on the right, the initial rename of
> the table to a temporary name might corrupt references to that table in triggers, views, and foreign key
> constraints. The safe procedure on the left constructs the revised table definition using a new temporary
> name, then renames the table into its final name, which does not break links."

Vagyis: **előbb** kell létrehozni az új táblát ideiglenes néven, adatot átmásolni, a régit eldobni, és **utána**
átnevezni az újat a végleges névre — fordítva (régi tábla átnevezése ideiglenes névre elsőként) hibás és
2018 óta (3.25.0/3.26.0 óta megerősített RENAME viselkedés miatt) különösen veszélyes triggerek/view-k/foreign
key-k törésére.

**Mikor kell a teljes 12 lépés, és mikor elég egy egyszerűbb (de veszélyesebb) mód:**

> „The 12-step generalized ALTER TABLE procedure above will work even if the schema change causes the
> information stored in the table to change. So the full 12-step procedure above is appropriate for dropping a
> column, changing the order of columns, adding or removing a UNIQUE constraint or PRIMARY KEY, adding CHECK or
> FOREIGN KEY or NOT NULL constraints, or changing the datatype for a column, for example. However, a simpler
> and faster procedure can optionally be used for some changes that do not affect the on-disk content in any
> way."

Az „egyszerűbb" eljárás közvetlenül a `sqlite_schema` táblát módosítja `PRAGMA writable_schema=ON` mellett —
**ehhez kapcsolódik a dokumentáció explicit, szó szerinti mentési ajánlása**, lásd az 5. pontban.

Forrás mindhez: https://sqlite.org/lang_altertable.html, 8. szakasz.

### 2.3 `PRAGMA foreign_keys` viselkedése migráció közben

**[T1] Szó szerint:**

> „PRAGMA foreign_keys; PRAGMA foreign_keys = boolean; Query, set, or clear the enforcement of foreign key
> constraints. This pragma is a no-op within a transaction; foreign key constraint enforcement may only be
> enabled or disabled when there is no pending BEGIN or SAVEPOINT."

> „As of SQLite version 3.6.19, the default setting for foreign key enforcement is OFF. However, that might
> change in a future release of SQLite. […] To minimize future problems, applications should set the foreign
> key enforcement flag as required by the application and not depend on the default setting."

Forrás: https://sqlite.org/pragma.html, `PRAGMA foreign_keys` szakasz.

**Ez közvetlenül megmagyarázza a 12 lépéses recept 1. és 2. lépésének sorrendjét**: a `PRAGMA foreign_keys=OFF`-ot
**a tranzakció megkezdése ELŐTT** kell kiadni, mert a pragma tranzakción belül hatástalan (no-op). Ha valaki
felcseréli a sorrendet (előbb BEGIN, aztán próbálja kikapcsolni a foreign key-eket), a pragma nem lép életbe, és
a tábla-újraépítés hibázhat a foreign key ellenőrzésen.

### 2.4 `PRAGMA legacy_alter_table` viselkedése

**[T1] Szó szerint:**

> „This pragma sets or queries the value of the legacy_alter_table flag. When this flag is on, the ALTER TABLE
> RENAME command […] only rewrites the initial occurrence of the table name in its CREATE TABLE statement and in
> any associated CREATE INDEX and CREATE TRIGGER statements. Other references to the table are unmodified,
> including: References to the table within the bodies of triggers and views. References to the table within
> CHECK constraints in the original CREATE TABLE statement. References to the table within the WHERE clauses of
> partial indexes. The default setting for this pragma is OFF, which means that all references to the table
> anywhere in the schema are converted to the new name. […] New applications should leave this flag turned off."

> „The legacy alter table behavior is a per-connection setting. […] The setting does not persist. Changing this
> setting in one connection does not affect any other connections."

Forrás: https://sqlite.org/pragma.html, `PRAGMA legacy_alter_table` szakasz.

**Kapcsolódó, a `lang_altertable.html`-en található kompatibilitási táblázat** azt mutatja, hogy 3.26.0 előtt a
`PRAGMA foreign_keys` és a `legacy_alter_table` beállítás kombinációja határozta meg, hogy egy tábla átnevezésekor
a rá mutató FOREIGN KEY hivatkozások frissülnek-e; 3.26.0-tól ez mindig frissül, hacsak a `legacy_alter_table`
nincs bekapcsolva. **Gyakorlati tanulság az easter-memory-system-hez:** ha az SQLite verzió modern (ami a Bun
beépített SQLite-jánál vagy a `better-sqlite3`/`libsql` csomagoknál tipikusan igaz), a `RENAME TO`/`RENAME COLUMN`
biztonságosan frissíti a hivatkozásokat, feltéve hogy a `legacy_alter_table` alapértéken (OFF) marad.

---

## 3. FTS5 virtuális tábla és triggerek migrációban

### 3.1 A `rebuild` parancs — csak teljes újraépítés, nincs részleges javítás

**[T1] Szó szerint, a hivatalos FTS5 dokumentációból:**

> „6.12. The 'rebuild' Command. This command first deletes the entire full-text index, then rebuilds it based
> on the contents of the table or content table. It is not available with contentless tables.
> INSERT INTO ft(ft) VALUES('rebuild');"

Forrás: https://sqlite.org/fts5.html, 6.12. szakasz.

**Mikor ajánlja a dokumentáció a `rebuild`-et?** Amikor a külső-tartalmú (`content=`) FTS5 tábla és a mögötte
álló „valódi" tábla inkonzisztenssé válik — pl. mert a triggereket **utólag** hozták létre, és nem tartalmazzák
a már meglévő sorokat:

> „[…] the content table and external content FTS5 table are inconsistent, as creating the triggers does not
> copy existing rows from the content table into the FTS index. The triggers are only able to ensure that
> updates made to the content table after they are created are reflected in the FTS index. In this, and any
> other situation where the FTS index and its content table have become inconsistent, the 'rebuild' command may
> be used to completely discard the contents of the FTS index and rebuild it based on the current contents of
> the content table."

**Ez pontosan az easter-memory-system helyzete lehet**, ha a triggereket egy kézzel írt migrációban hozzák létre
egy már létező, adatokkal teli tábla mellé: a triggerek önmagukban **nem** töltik fel visszamenőleg az FTS5
indexet — ehhez explicit `rebuild` (vagy kezdeti feltöltő `INSERT INTO fts_tábla SELECT ...`) szükséges.

### 3.2 A `'delete-all'` parancs

**[T1] Szó szerint:**

> „6.4. The 'delete-all' Command. This command is only available with external content and contentless tables
> (including contentless-delete tables). It deletes all entries from the full-text index.
> INSERT INTO ft(ft) VALUES('delete-all');"

Forrás: https://sqlite.org/fts5.html, 6.4. szakasz.

A `delete-all` **csak töröl**, nem tölt fel újra — ez a `rebuild` „törlés" fele önmagában, kézi újra-feltöltési
lépés (pl. `INSERT INTO ft SELECT ... FROM content_table`) nélkül.

### 3.3 Az `'integrity-check'` parancs — csak diagnosztika, NEM javítás

**[T1] Szó szerint:**

> „6.7. The 'integrity-check' Command. This command is used to verify that the full-text index is internally
> consistent, and, optionally, that it is consistent with any external content table. […] In all cases, if any
> discrepancies are found, the command fails with an SQLITE_CORRUPT_VTAB error."

Forrás: https://sqlite.org/fts5.html, 6.7. szakasz.

Ez megerősíti: **nincs részleges/inkrementális javítási mechanizmus.** Az `integrity-check` kizárólag *jelzi* a
problémát (hibával elbukik), a tényleges korrekcióra a dokumentáció egyetlen eszközt ismer: a teljes `rebuild`-et.
Ezt közvetve megerősíti a `secure-delete` opció dokumentációjának hibaüzenete is:

> „Attempting to do so results in an error, with an error message like ‘invalid fts5 file format (found 5,
> expected 4) - run 'rebuild'‘. […] by running the 'rebuild' command on the table using version 3.42.0 or later."

Vagyis maga az SQLite motor is a `rebuild`-re utal hivatalos hibaüzenetében, mint az egyetlen javítási útra.

### 3.4 Szerkezeti változtatás (oszlopok, tokenizer) — dokumentációs hiány

**[Hiány — nem T1]** A hivatalos `fts5.html` oldal **sehol nem tárgyalja** kifejezetten, hogy egy FTS5 virtuális
tábla oszloplistáját vagy tokenizerét hogyan lehet utólag megváltoztatni, és nem említi az `ALTER TABLE`
alkalmazhatóságát virtuális táblákra sem (a keresés a teljes dokumentumban nem talált `ALTER TABLE` említést).
Ez maga is releváns megállapítás: **a hivatalos FTS5-dokumentáció implicit módon abból indul ki, hogy egy FTS5
tábla szerkezetét nem „alterezzük", hanem `DROP TABLE` + újra `CREATE VIRTUAL TABLE ... USING fts5(...)` +
`rebuild`/újra-feltöltés a bevett út** — ezt közvetett módon támasztja alá, hogy a `CREATE VIRTUAL TABLE`
szintaxist önálló, teljes definícióként dokumentálja, és az `ALTER TABLE` oldal (`lang_altertable.html`) egyáltalán
nem említi a virtuális táblákat kivételként vagy támogatott esetként.

**[T3]** Közvetett megerősítés közösségi forrásokból (fórum/issue szinten, nem hivatalos állítás):
https://github.com/sqlitebrowser/sqlitebrowser/issues/781 (FTS5 tábla létrehozása/eldobása körüli hibák
dokumentálása gyakorlati eszközben).

**Következtetés a triggerekre nézve:** a triggerek (amik az FTS5 tábla adatszinkronizálását végzik a „valódi"
tábla és az index között) hagyományos SQL objektumok, ezekre **teljes mértékben** vonatkozik a 2. pontban leírt
12 lépéses recept, ha az alapul szolgáló tábla szerkezete változik — vagyis egy migrációban a triggereket is
`DROP TRIGGER` + `CREATE TRIGGER` formában újra kell generálni, ha a mögöttes tábla oszlopai megváltoznak (ezt a
12-lépéses recept 8. pontja explicit módon előírja: „Use CREATE INDEX, CREATE TRIGGER, and CREATE VIEW to
reconstruct indexes, triggers, and views associated with table X […] making changes as appropriate for the
alteration").

---

## 4. Az expand–contract (parallel change) minta

### 4.1 Elsődleges forrás és pontos definíció

**[T1 — elsődleges forrás]** A mintát Danilo Sato (ThoughtWorks) írta le és nevezte el „Parallel Change"
(közismertebb nevén „expand and contract") címmel, martinfowler.com-on, 2014. május 13-án:

> „Parallel change, also known as expand and contract, is a pattern to implement backward-incompatible changes
> to an interface in a safe manner, by breaking the change into three distinct phases: expand, migrate, and
> contract."

A három fázis pontos meghatározása:

> „In the expand phase you augment the interface to support both the old and the new versions. […] During the
> migrate phase you update all clients using the old version to the new version. […] Once all usages have been
> migrated to the new version, you perform the contract phase to remove the old version and change the interface
> so that it only supports the new version."

Forrás: https://martinfowler.com/bliki/ParallelChange.html (nyers HTML, tag-stripelve)

**A minta eredete, a szerző saját elismerése szerint:**

> „This technique was first documented as a refactoring strategy by Joshua Kerievsky in 2006 and presented in
> his talk The Limited Red Society presented at the Lean Software and Systems Conference in 2010."

Ezt **nem ellenőriztük közvetlenül** Kerievsky elsődleges anyagain (lásd `hianyok.md`) — ez Fowler oldalának saját
állítása a származásról (T2 minőségű attribúció, maga a mintaleírás viszont T1, mert ez a normatív,
legszélesebb körben hivatkozott forrás).

**[T2] Független megerősítés a származásra és a motivációra** — Tim Wellhausen „Expand and Contract — A Pattern
to Apply Breaking Changes to Persistent Data with Zero Downtime" c. tanulmánya (tim-wellhausen.de) saját
hivatkozásjegyzékében:

> „[1] Michael T. Nygard: Release It!, Chapter on Zero Downtime Deployments, O'Reilly, 2007
> [2] Danilo Sato: Parallel Change"

Forrás: https://www.tim-wellhausen.de/papers/ExpandAndContract/ExpandAndContract.html

Ez tehát egy **második, egymástól független szál** is felfedezhető a minta eredetéhez: Michael T. Nygard 2007-es
„Release It!" könyvének „Zero Downtime Deployments" fejezete (ezt a könyvet magát nem tudtuk nyersen letölteni,
lásd `hianyok.md`).

### 4.2 Adatbázis-refaktorálásra alkalmazva: az „Evolutionary Database Design" mint másodig elsődleges forrás

**[T1 — elsődleges forrás, ugyanaz a szerzőpáros, aki a technikát az adatbázis-világba emelte]** Pramod Sadalage
és Martin Fowler „Evolutionary Database Design" c. cikkében:

> „Database refactoring: this is a key component to evolutionary database design. Most database refactorings
> follow the parallel change pattern, where the migrate phase is the transition period between the original and
> the new schema, until all database access code has been updated to work with the new schema."

Forrás: https://martinfowler.com/articles/evodb.html (nyers HTML, tag-stripelve; szerzőség a lap fejlécéből:
„Pramod Sadalage […] developed the original techniques of evolutionary database design and database refactoring
used by Thoughtworks in 2000. […] Martin Fowler.")

### 4.3 A kulcskérdés: alkalmazható-e egyetlen gépen, néhány felhasználós rendszernél?

Ez a kutatás legfontosabb ténymegállapítása, és **három, egymástól független forrás mutat ugyanabba az irányba**:

**[T1 — elsődleges forrás, ugyanaz a cikk mint 4.2]** Az „Evolutionary Database Design" cikk explicit módon
kimondja, hogy egyszerű, egy-verziós projekteknél **nincs szükség** a több-verziós adatbázis-kezelésre:

> „Variations […] Multiple versions. A simple project can survive with just a single code line, and thus a
> single database version. With more complex projects there's a need to support multiple versions for AB
> testing, or rolling deployments when doing Canary Releases and thus multiple varieties of the project
> database."

Ugyanez a cikk az „egyszerű rendszer" tipikus megoldását is leírja — és ez **szó szerint megegyezik** azzal, amit
az easter-memory-system valószínűleg tesz (Drizzle `migrate()` induláskor):

> „Shipping changes with application. In some projects we have seen that the changes to the product have to be
> shipped to thousands of end customers. In these kinds of projects its better to allow the application upgrade
> itself by packaging all the database changes along with the application (as we have no idea what version the
> customer is upgrading from) and let the application upgrade the database on startup using frameworks like
> Flyway or one of its many cousins."

Forrás: https://martinfowler.com/articles/evodb.html

**[T2] Wellhausen tanulmánya explicit módon a minta szükségességének OKÁT a redundáns, több-példányos,
24/7-es üzemeltetéshez köti, és kimondja, hogy korábban (amikor le lehetett állítani a rendszert karbantartásra)
ez a probléma nem is állt fenn:**

> „Applying the pattern on persistent data in a database is particularly challenging because existing data needs
> to be migrated from the old into the new structure. Doing this was still fairly straight-forward at the times
> when you could shut down a system temporarily to do some maintenance. Nowadays, many systems need to operate
> 24/7 without any maintenance downtime […]"

> „In order to achieve 24/7 operations, all system components exist redundantly. In particular, there are
> multiple instances of the database system and multiple instances of the application server. Deployments of
> updated system components are done instance by instance, which means that some instances are unavailable
> during a system update."

Forrás: https://www.tim-wellhausen.de/papers/ExpandAndContract/ExpandAndContract.html

**[T1] Maga Fowler „Parallel Change" oldalának minden alkalmazási példája** eleve több egyidejű szereplőt tételez
fel, akik nem tudnak egyszerre frissülni: „refactoring […] especially when changing a PublishedInterface"
(több hívó fél), „database refactoring" (több hozzáférő kód-verzió), „deployments […] canary releases and
BlueGreenDeployment" (több párhuzamos szolgáltatáspéldány), „remote API evolution" (több kliens). A minta
lényege — idézve újra a definíciót — hogy „a client code still accesses" a régi struktúrát **miközben** már az
új is létezik; ha nincs több, egymástól függetlenül frissülő fogyasztó, ez a feltétel nem áll fenn.

### 4.4 Következtetés az easter-memory-system esetére

A fenti három forrás (a minta két elsődleges szerzőjének saját cikke + egy független, kifejezetten erre a
kérdésre fókuszáló tanulmány) **egybehangzóan** azt támasztja alá, hogy az expand–contract minta **teljes,
formális alkalmazása feleslegesen bonyolult** egy olyan rendszernél, ahol:

- egyetlen alkalmazás-példány fut (nincs „rolling deployment", nincs egyszerre több, vegyes verziójú kliens),
- a Docker-konténer cseréje és az adatbázis-migráció **atomikusan, egy karbantartási ablakban** történik (a
  folyamat leáll, migrál, újraindul — nem kell 0 másodperces rendelkezésre állást garantálni),
- nincs külső, a fejlesztőtől független API-fogyasztó, aminek saját ütemben kellene frissülnie.

Ez **pontosan** megfelel az „Evolutionary Database Design" által leírt „a simple project can survive with just a
single code line, and thus a single database version" esetnek, és a Wellhausen-tanulmány által leírt „a times
when you could shut down a system temporarily to do some maintenance" helyzetnek. A hivatalosan dokumentált
egyszerűbb alternatíva — „let the application upgrade the database on startup" — pontosan a Drizzle
`drizzle-kit migrate` / `migrate()` induláskori mintája (lásd 1. pont).

**Amit ez NEM jelent:** ez nem azt jelenti, hogy a migrációt hanyagul, teszt és mentés nélkül kellene végezni —
csupán azt, hogy a *parallel change három fázisú, „expand most, migrate-clients-fokozatosan, contract később"*
menete (ami elsősorban a több-verziós egyidejűség kezelésére való) nem indokolt overhead egy egypéldányos
rendszerben. A kockázatcsökkentés itt más eszközökkel (mentés, teszt-migráció egy másolaton, dry-run) érhető el
— lásd az 5. pontot.

---

## 5. Mentés a migráció előtt — hivatalos ajánlások eszközönként

Ez a kérdés esetében **vegyes kép** rajzolódik ki: egyes eszközök hivatalosan kimondják, mások következetesen
hallgatnak róla a fő migrációs dokumentációjukban.

### 5.1 SQLite hivatalos dokumentáció — EXPLICIT mentési ajánlás (a kézi séma-szerkesztési eljáráshoz)

**[T1] Szó szerint**, a `lang_altertable.html` 8. szakaszának „egyszerűbb eljárás" részénél (amely közvetlenül a
`sqlite_schema` tábla `UPDATE`-elésével dolgozik `PRAGMA writable_schema=ON` mellett):

> „Caution: Making a change to the sqlite_schema table like this will render the database corrupt and unreadable
> if the change contains a syntax error. It is suggested that careful testing of the UPDATE statement be done on
> a separate blank database prior to using it on a database containing important data."

> „Caution: Once again, making changes to the sqlite_schema table like this will render the database corrupt and
> unreadable if the change contains an error. Carefully test this entire procedure on a separate test database
> prior to using it on a database containing important data **and/or make backup copies of important databases
> prior to running this procedure.**"

Forrás: https://sqlite.org/lang_altertable.html, 8. szakasz.

**Fontos árnyalás:** ez a mentési ajánlás kifejezetten a **kézi `sqlite_schema`-szerkesztős, gyorsabb** eljáráshoz
kapcsolódik (amely csak korlátok-eltávolítására/alapértékek módosítására ajánlott), **nem** a szokásos, biztonságos
12 lépéses „create new / copy / drop old / rename" eljáráshoz — ott a dokumentáció csak a *sorrend pontos
betartására* figyelmeztet, expliciten mentést nem említ. Mindazonáltal ez **az egyetlen fellelt eset**, ahol egy
adatbázis-mechanizmus hivatalos dokumentációja szó szerint, felszólító módban mentést javasol migráció-jellegű
művelet előtt.

### 5.2 Flyway — EXPLICIT ajánlás: mentés és visszaállítás mint az undo migráció kiegészítője/helyettesítője

**[T1] Szó szerint**, az „Undo migrations" oldal „Important notes" szakaszából:

> „Please note, you should take care if you have destructive changes (drop, delete, truncate etc) in your
> deployment. Undo migrations assume the whole migration succeeded and should now be undone. […] In such
> circumstances, an alternative approach could be to maintain backwards compatibility between the DB and all
> versions of the code currently deployed in production. […] **This should be complemented with a proper, well
> tested, backup and restore strategy. It is independent of the database structure, and once it is tested and
> proven to work, no migration script can break it.** For optimal performance, and if your infrastructure
> supports this, we recommend using the snapshot technology of your underlying storage solution."

Forrás: https://documentation.red-gate.com/fd/undo-migrations-273973334.html

**Fontos kontextus:** a Flyway „Undo Migration" funkció maga is jelölve van a lapon: „EDITION: TEAMS" — tehát
**fizetős**, csak a Teams-kiadásban elérhető funkció, a Community (ingyenes) verzióban nincs beépített
visszagörgetés sem. A hivatalos dokumentáció emiatt kifejezetten a mentés-visszaállítást ajánlja, mint ami
**„independent of the database structure"** és **„no migration script can break it"** — vagyis erősebb garanciát
ad, mint bármilyen migrációs eszköz saját rollback-mechanizmusa.

**[T2/T3] Közvetett megerősítés**, hogy a Flyway *automatikus* mentést **nem** végez: a hivatalos GitHub
repóban évek óta nyitott feature-kérés van erre — „Add a goal to do an SQL backup before the migration" —
https://github.com/flyway/flyway/issues/124 — vagyis a közösség is hiányként azonosítja azt, hogy a Flyway maga
nem csinál automatikus mentést, csak *ajánlja* azt külön eszközzel.

### 5.3 Liquibase — a hivatalos koncepció-oldalak HALLGATNAK a mentésről; a support-FAQ explicit módon elhárítja a felelősséget

**[T1]** A `rollback` parancs referencia-oldalán (https://docs.liquibase.com/commands/rollback/rollback.html) és
a „What is a rollback?" koncepció-oldalon (https://docs.liquibase.com/workflows/liquibase-community/using-rollback.html)
**nem található** a „backup"/„back up" szavak egyike sem — ellenőrizve teljes szöveg-kereséssel a letöltött,
tag-stripelt oldalakon.

**[T1, de WebFetch-csel lekérve, mert a curl 403-at kapott a Zendesk-alapú support oldalról]** A hivatalos
Liquibase support-FAQ explicit módon kimondja, hogy a Liquibase **nem** csinál mentést:

> „No, Liquibase does not back up any data before deploying any changesets."

és helyette a dry-run ellenőrzést ajánlja:

> „We recommend that you run the update-sql command and verify what is going to run on the database before
> executing."

valamint figyelmezteti a felhasználót, hogy a rollback nem hoz vissza törölt adatot:

> „any changeset that either removes or deletes data either intentionally or indirectly will delete the data"
> (azaz a rollback csak a séma-szerkezetet állítja vissza, adatot nem).

Forrás: https://support.liquibase.com/hc/en-us/articles/29383069283739-Does-Liquibase-Backup-Any-Data
**(WebFetch-csel lekérve — jelölve, mert a nyers `curl` HTTP 403-at adott vissza erre a Zendesk-oldalra)**

**Értékelés:** ez nem azonos egy „mindig készíts mentést" felszólítással, de funkcionálisan ugyanoda vezet: a
Liquibase hivatalosan kimondja, hogy a felelősség a felhasználóé, és dry-run futtatást ajánl helyette/mellette.

### 5.4 Rails (Active Record Migrations Guide) — NINCS mentési ajánlás, de van natív rollback

**[T1 — hiány, alaposan ellenőrizve]** A teljes hivatalos „Active Record Migrations" útmutatóban
(https://guides.rubyonrails.org/active_record_migrations.html, ~64 500 karakter, tag-stripelt szöveg) a
„backup"/„back up" kifejezés **egyetlen releváns előfordulásban sem** szerepel (a talált egyezés hamis pozitív
volt: „migrating **back up** again"). A guide viszont natívan, elsőrangú funkcióként kínálja a visszagörgetést:

> „Active Record knows how to reverse this migration as well; if we roll this migration back, it will remove the
> table." […] „With reversible migrations, not only does the migration create the table when applied, but it
> also enables smooth rollback functionality."

> „Sometimes your migration will do something which is just plain irreversible; […] you can raise
> ActiveRecord::IrreversibleMigration in your change method […] If someone tries to revert your migration, an
> error message will be displayed"

Forrás: https://guides.rubyonrails.org/active_record_migrations.html — tehát a Rails filozófiája a
kockázatkezelésre **a visszagörgethetőség tervezése és a nem-visszagörgethető műveletek explicit jelölése**, nem
a mentés előírása.

### 5.5 Django — NINCS mentési ajánlás; a visszafordítás explicit módon NEM garantált

**[T1 — hiány, ellenőrizve]** A hivatalos „Migrations" témaoldalon (https://docs.djangoproject.com/en/5.2/topics/migrations/)
a „backup" szó **egyszer sem** fordul elő (teljes szöveg-kereséssel ellenőrizve a letöltött, tag-stripelt
oldalon). A dokumentáció viszont világosan kimondja a visszafordítás korlátait:

> „A migration is irreversible if it contains any irreversible operations. Attempting to reverse such migrations
> will raise IrreversibleError: […] django.db.migrations.exceptions.IrreversibleError: Operation <RunSQL
> sql='DROP TABLE demo_books'> in books.0003_auto is not reversible"

Forrás: https://docs.djangoproject.com/en/5.2/topics/migrations/

**[T3]** Kizárólag közösségi (nem hivatalos) forrásokban találtunk kifejezett „mentsd a DB-t a migrálás előtt"
tanácsot Django kapcsán (pl. Medium-cikk, PyPI-csomagok mint `django-backup-utils` és `django-zeromigrations`
opcionális backup-funkcióval) — ezek **harmadik féltől** származnak, nem a Django hivatalos dokumentációjából.

### 5.6 Drizzle — NINCS hivatalos mentési ajánlás egyik átvizsgált oldalon sem

**[T1 — hiány, ellenőrizve]** A `backup`/`back up` kifejezés **egyik letöltött, tag-stripelt Drizzle-dokumentum-
oldalon sem** fordul elő (kit-overview, generate, migrate, push, custom-migrations, migrations-fundamentals).
A Drizzle a kockázatot inkább a `push --explain` (dry-run) és `push --force` (explicit megerősítés
adatvesztéshez) mechanizmusokkal kezeli (lásd 1.1 pont) — de ez nem helyettesíti a mentést, csak a *véletlen*
destruktív módosítást hivatott megakadályozni egy interaktív munkamenetben.

### 5.7 Összegzés táblázatosan

| Eszköz | Explicit hivatalos mentési ajánlás a fő dokumentációban? | Beépített rollback? |
|---|---|---|
| SQLite (ALTER TABLE, kézi sqlite_schema-szerkesztés) | **IGEN** — szó szerint, kétszer is | n/a (motor-szintű mechanizmus) |
| Flyway | **IGEN** — szó szerint, az Undo Migrations oldalon | Van, de fizetős (Teams) és korlátozott |
| Liquibase | Közvetve — a support-FAQ elhárítja a felelősséget, dry-runt ajánl | Van, ingyenes, gazdag parancskészlet |
| Rails | Nincs | Van, natív, ingyenes (`down`/`revert`) |
| Django | Nincs | Részleges — sok művelet `IrreversibleError` |
| Drizzle | Nincs | **Nincs** (lásd 1.2 pont) |

**A minta, ami kirajzolódik:** minél gyengébb/kockázatosabb egy eszköz beépített rollback-képessége (Drizzle:
nincs; Flyway Community: nincs, csak fizetősben van), annál inkább **vagy** a mentést hangsúlyozzák explicit
módon (Flyway), **vagy** egyszerűen hallgatnak róla, a felelősséget a felhasználóra hagyva (Drizzle). Minél
erősebb a beépített rollback (Rails, Liquibase), annál kevésbé hangsúlyozzák a mentést a fő dokumentációban —
bár a Liquibase support-oldala ekkor is tisztázza, hogy a rollback nem hoz vissza törölt *adatot*, csak
séma-szerkezetet.

**Az easter-memory-system esetére vetítve:** mivel a Drizzle-nek nincs rollback funkciója (1.2 pont), és a
hivatalos Drizzle-dokumentáció nem ad mentési ajánlást sem, a kockázatkezelés **kizárólag** a felhasználóra hárul
— ez erősíti azt az érvet, hogy egy ilyen stacknél a mentés-előtte-migrálunk szabály **indokolt belső
házirendként**, még ha ezt maga a Drizzle nem is írja elő. Ezt közvetve az SQLite hivatalos dokumentációja is
alátámasztja (5.1 pont), amennyiben bármilyen séma-szintű, kézi beavatkozás történik.

---

## 6. Adatfájl-formátum verziózása (nem adatbázis — fájl-alapú séma)

Az easter-memory-systemhez leginkább hasonló, konkrétan fellelt és ellenőrzött rendszerek:

### 6.1 Jupyter Notebook (`nbformat`) — verziómező a fájlban + lusta migráció olvasáskor

**[T1]** A hivatalos `nbformat` v4 JSON-séma kötelezővé teszi a verziómezőket magában a fájlban:

> „nbformat_minor: […] Incremented for backward compatible changes to the notebook format."
> „nbformat: […] Incremented between backwards incompatible changes to the notebook format."

Forrás: https://raw.githubusercontent.com/jupyter/nbformat/main/nbformat/v4/nbformat.v4.schema.json

**[T1]** A hivatalos formátumleírás explicit módon rögzíti a szemantikus-verziózási elvet és a
kompatibilitási politikát:

> „The notebook format is an evolving format. When backward-compatible changes are made, the notebook format
> minor version is incremented. When backward-incompatible changes are made, the major version is incremented."
> „New cell or output types will not be rendered in versions that do not recognize them, but they will be
> preserved."

Forrás: https://nbformat.readthedocs.io/en/latest/format_description.html

**[T1] A „lusta migráció olvasáskor" minta pontos, dokumentált API-ja:**

> „nbformat.read(fp, as_version, …) — Read a notebook from a file as a NotebookNode of the given version. The
> string can contain a notebook of any version. **The notebook will be returned as_version, converting, if
> necessary.**"
> „The reading functions require you to pass the as_version parameter. […] nb = nbformat.read('path/to/notebook.ipynb', as_version=4)
> **This will automatically upgrade or downgrade notebooks in other versions of the notebook format to the
> structure your code knows about.**"

Forrás: https://nbformat.readthedocs.io/en/latest/api.html

**Ez a kutatás legjobban dokumentált, leginkább „tankönyvi" példája** a kért mintára: verziómező magában a
fájlban + automatikus, olvasáskor futó konverzió a kért verzióra, explicit `NO_CONVERT` opcióval kikapcsolható.

### 6.2 WordPress WXR export formátum — verziómező beágyazva az interchange-fájlba

**[T1]** A hivatalos `export_wp()` PHP-függvény forráskódja (fejlesztői referencia-dokumentáció) szerint minden
exportált fájl explicit verzió-elemet és verzió-számot tartalmazó névtér-URI-kat kap:

> „<rss version="2.0" xmlns:excerpt="https://wordpress.org/export/<?php echo WXR_VERSION; ?>/excerpt/" […]
> xmlns:wp="https://wordpress.org/export/<?php echo WXR_VERSION; ?>/"> […]
> <wp:wxr_version><?php echo WXR_VERSION; ?></wp:wxr_version>"

Forrás: https://developer.wordpress.org/reference/functions/export_wp/

Itt a mintázat kicsit más, mint az nbformat-nál: nem „lusta migráció olvasáskor" történik minden importálónál
automatikusan, hanem az importáló (WordPress Importer plugin) a fájlban talált `wxr_version` alapján dönti el,
hogyan értelmezze a további XML-elemeket — ez inkább **„exportáláskor lezárt verzió + verzióra tudatos
importáló"** minta, nem tömeges átírás.

*(Érdekesség, nem központi állítás: a fájl saját megjegyzése explicit kimondja, hogy ez NEM biztonsági mentés:
„This file is not intended to serve as a complete backup of your site." — forrás ugyanaz.)*

### 6.3 Docker Compose fájlformátum — a verziómező „obszoletté" tétele, verzió-agnosztikus, engedékeny feldolgozás felé

**[T1]** A Compose fájlformátum korábban kötelező `version:` mezőt használt (pl. `"3.8"`), de a Compose
Specification ezt később **elavulttá** nyilvánította, és a feldolgozó logikát verzió-függetlenné tette:

> „The top-level version property is defined by the Compose Specification for backward compatibility. It is
> only informative and you'll receive a warning message that it is obsolete if used. **Compose always uses the
> most recent schema to validate the Compose file, regardless of the version field.** Compose validates whether
> it can fully parse the Compose file. If some fields are unknown, typically because the Compose file was
> written with fields defined by a newer version of the Specification, you'll receive a warning message."

Forrás: https://docs.docker.com/reference/compose-file/version-and-name/

**Ez egy fontos, ellentétes irányú minta a 6.1–6.2 pontokhoz képest**: ahelyett, hogy a verziómező alapján
ágazna el a feldolgozás (és migrálná a régi formátumot), a Compose **megszüntette** a verzió-alapú elágazást, és
helyette egyetlen, mindig legfrissebb sémával, engedékeny (ismeretlen mezőket csak figyelmeztetéssel jelző)
feldolgozást vezetett be. Ez is „bevett minta" — csak nem a „verzió szerinti migráció", hanem a „verzió-mező
leépítése, additív/engedékeny séma" stratégia.

### 6.4 Ellenpélda: JSON Canvas (Obsidian nyílt canvas-formátum) — NINCS fájlon belüli verziómező

**[T1, ellenőrizve — negatív találat]** A JSON Canvas hivatalos specifikációja (https://jsoncanvas.org/spec/1.0/)
a fájl felépítését („Top level: nodes, edges") részletesen leírja, és **nem tartalmaz semmilyen `version` mezőt
magában a `.canvas` fájl JSON-struktúrájában** — kizárólag maga a *specifikáció-dokumentum* van dátumozva/verzió-
jelölve („Version 1.0 — 2024-03-11"), a fájlformátum maga nem hordoz verzióazonosítót. Ez azt mutatja, hogy nem
minden egyszerű, ember-olvasható adatformátum tervezője tartja szükségesnek a fájlonkénti verziómezőt — az
additív, visszafelé kompatibilis bővítés (új, opcionális mezők) alternatív stratégia lehet.

### 6.5 Összegzés — mi a bevett minta?

A kért három mintázat (verziómező a fájlban / lusta migráció olvasáskor / egyszeri tömeges átírás) közül **csak
az első kettőre találtunk közvetlenül, hivatalos dokumentációval alátámasztott, megnevezett rendszert**:

- **Verziómező a fájlban + explicit, dokumentált konverziós API olvasáskor**: Jupyter `nbformat` (6.1) — ez a
  legtisztább, „tankönyvi" megvalósítás.
- **Verziómező a fájlban, importáló dönt a verzió alapján**: WordPress WXR (6.2).
- **Verziómező megszüntetése, mindig-legfrissebb-séma + engedékeny feldolgozás**: Docker Compose (6.3) — ez egy
  harmadik, a kérdésben nem szereplő, de releváns stratégia.
- **„Egyszeri tömeges átírás"** mintára **nem találtunk** hivatalos dokumentációval alátámasztott, megnevezett,
  konkrét rendszert ebben a kutatásban (lásd `hianyok.md`) — ez inkább migrációs szkriptek/CLI-eszközök
  (pl. `codemod`, keretrendszer-specifikus `upgrade` parancsok) gyakorlatában él, de ezt nem sikerült egy
  konkrét, hivatalos, „markdown/YAML frontmatter" kontextusú dokumentációval alátámasztani ebben a körben.

Az easter-memory-system markdown-fájljaihoz **az nbformat-mintázat** (explicit verziómező a YAML fejlécben +
olvasáskor futó, cél-verzióra konvertáló betöltő függvény) tűnik a leginkább dokumentáltan bevált, jól
karbantartott, valós rendszerekben (Jupyter) évek óta üzemelő megoldásnak.

---

## 7. Docker-alapú frissítés kis rendszernél

### 7.1 Adat-tartósítás — a volume túléli a konténer cseréjét

**[T1] Szó szerint**, a hivatalos Docker Engine „Volumes" oldaláról:

> „A volume's contents exist outside the lifecycle of a given container. When a container is destroyed, the
> writable layer is destroyed with it. **Using a volume ensures that the data is persisted even if the container
> using it is removed.**"

> „Removing the service doesn't remove any volumes created by the service."

> „Volumes are easier to back up or migrate than bind mounts." […] „Volumes are useful for backups, restores,
> and migrations."

Forrás: https://docs.docker.com/engine/storage/volumes/

A hivatalos oldal konkrét, futtatható parancssort is ad a kötet-alapú mentésre/visszaállításra (helper-konténeres
`tar` technika):

> „$ docker run --rm --volumes-from dbstore -v $(pwd):/backup ubuntu tar cvf /backup/backup.tar /dbdata"

Forrás: ugyanaz az oldal, „Back up a volume" szakasz.

### 7.2 `docker compose down` — alapértelmezetten NEM törli a névvel ellátott köteteket

**[T1] Szó szerint:**

> „Stops containers and removes containers, networks, volumes, and images created by up. **By default, the only
> things removed are:** Containers for services defined in the Compose file. Networks defined in the networks
> section of the Compose file. The default network, if one is used. **Networks and volumes defined as external
> are never removed.**"

> „-v, --volumes — Remove named volumes declared in the ‘volumes' section of the Compose file and anonymous
> volumes attached to containers"

> „Anonymous volumes are not removed by default. […] **For data that needs to persist between updates, use
> explicit paths as bind mounts or named volumes.**"

Forrás: https://docs.docker.com/reference/cli/docker/compose/down/

**Ez közvetlen, hivatalos válasz** a kérdésre: a konténer (és akár a teljes Compose-projekt) cseréje/újraindítása
**nem** viszi el az adatot, amíg a köteteket (volumes) használjuk **és** nem adjuk meg kifejezetten a `-v` /
`--volumes` kapcsolót a `down` parancshoz.

### 7.3 Leállással járó frissítés — hivatalos „production" útmutató

**[T1]** A „Running Compose in production" hivatalos oldal a frissítés menetét így írja le (nincs benne
adatbázis-migrációra vonatkozó lépés — ez fontos **hiány**, lásd `hianyok.md`):

> „When you make changes to your app code, remember to rebuild your image and recreate your app's containers.
> To redeploy a service called web, use: $ docker compose build web ; $ docker compose up --no-deps -d web.
> This first command rebuilds the image for web and then stops, destroys, and recreates just the web service."

> „Specifying a restart policy like restart: always to avoid downtime"

Forrás: https://docs.docker.com/compose/how-tos/production/

Ez a hivatalos oldal **kifejezetten leállással jár** (stop → destroy → recreate), és nem tesz külön említést a
migráció időzítéséről ebben a konkrét szövegkörnyezetben.

### 7.4 Frissítési sorrend: migráció előbb vagy a konténer előbb? — a hivatalos `pre_start` mechanizmus és worked example

**[T1] A legkonkrétabb, migrációs sorrendre vonatkozó hivatalos anyag** a Compose fájl-referencia `pre_start`
életciklus-horgony (lifecycle hook) leírásában és **pontosan egy adatbázis-migrációs példával**:

> „pre_start defines a sequence of init containers to run before the service container is started. Each step
> runs to completion, in declared order, and the service container only starts once every step has exited 0. A
> non-zero exit fails the bring-up of the service and its dependents."

> „pre_start steps only run once the service's depends_on conditions have been satisfied, so a step can rely on
> those dependencies the same way the main service command does."

A dokumentáció saját, szó szerinti példakódja:

```yaml
services:
  app:
    image: myapp:latest
    depends_on:
      db:
        condition: service_healthy
    pre_start:
      - command: ["./manage.py", "migrate"]
      - image: busybox
        command: sh -c 'chown -R 1000:1000 /data'
        volumes:
          - data:/data
  db:
    image: postgres:16
volumes:
  data:
```

Forrás: https://docs.docker.com/reference/compose-file/services/, `pre_start` szakasz.

**Ez explicit módon, egy hivatalos, kidolgozott példán keresztül** mutatja be a javasolt sorrendet: (1) az
adatbázis-szolgáltatás legyen egészséges (`condition: service_healthy`), (2) **ezután** fusson le a migráció
(`pre_start`, „./manage.py migrate" — Django-példa), és **csak ha ez sikeres (0-s kilépőkóddal)**, induljon el
maga az alkalmazás-konténer főfolyamata. Fontos korlátozás: a `pre_start` a **Docker Compose 5.3.0-tól** érhető
el — ez egy viszonylag friss (2026-os) funkció, régebbi Compose-verzióknál a hagyományos megoldás egy különálló,
egyszeri „migrate" szolgáltatás `depends_on: condition: service_completed_successfully` feltétellel:

> „service_completed_successfully: Specifies that a dependency is expected to run to successful completion
> before starting a dependent service."

Forrás: https://docs.docker.com/reference/compose-file/services/, `depends_on` szakasz.

**Amit a hivatalos dokumentáció NEM tesz meg**: nincs olyan önálló, prózai „best practice" bekezdés, ami
kimondaná: „mindig migrálj a konténercsere ELŐTT/UTÁN" — ehelyett a sorrendet a **mechanizmus maga** (a
`depends_on`/`pre_start` feltételrendszer) és a **worked example** demonstrálja, explicit ajánló szöveg nélkül.
Ezt hiányként rögzítjük (lásd `hianyok.md`).

### 7.5 Bónusz-találat: hivatalos `pre_stop` példa — adatfájl mentése konténerleállás előtt

**[T1] A hivatalos „Using lifecycle hooks with Compose" oldal saját, szó szerinti példája** majdnem szó szerint az
easter-memory-system helyzetét írja le (SQLite-szerű adatfájl mentése leállás előtt):

> „Pre-stop hooks are commands that run before the container is stopped by a specific command (like docker
> compose down or stopping it manually with Ctrl+C). […] Because the pre-stop hook runs before the stop signal
> is sent to the container, it is suited for actions that must complete while the application is still fully
> running. In the following example, **the hook backs up a data file before the container receives the stop
> signal.**"

```yaml
services:
  app:
    image: backend
    volumes:
      - data:/data
    pre_stop:
      - command: cp /data/app.db /data/app.db.bak
        user: root
volumes:
  data: {}
```

Forrás: https://docs.docker.com/compose/how-tos/lifecycle/, „Pre-stop hooks" szakasz.

Ez egy **direkt, hivatalos, kidolgozott mintapélda** arra, hogyan lehet a konténer-infrastruktúra szintjén (nem
az alkalmazás kódjában) garantálni, hogy egy `.db`-szerű fájl mentése megtörténjen minden leállás/frissítés
előtt — ez gyakorlatilag „ingyen" megvalósítja a kért „mentés minden frissítés előtt" szabályt Compose-natív
eszközökkel, feltéve, hogy a Compose verzió (2.30.0+) ezt támogatja.

### 7.6 Összegzés

| Kérdés | Hivatalos válasz | Forrás |
|---|---|---|
| A kötet túléli-e a konténer cseréjét? | Igen, alapból | docs.docker.com/engine/storage/volumes/ |
| `docker compose down` törli-e az adatot? | Nem, csak `-v` kapcsolóval | docs.docker.com/reference/cli/docker/compose/down/ |
| Van-e hivatalos „backup-hook" minta? | Igen, `pre_stop` + `cp` példa | docs.docker.com/compose/how-tos/lifecycle/ |
| Van-e hivatalos „migrálj a konténerindítás előtt" minta? | Igen, `pre_start` + `depends_on: service_healthy` + Django `migrate` példa | docs.docker.com/reference/compose-file/services/ |
| Van-e explicit prózai ajánlás a sorrendre? | **Nincs** — csak a mechanizmus és a worked example implikálja | (hiány) |
| Van-e hivatalos ajánlás a migráció-vs-konténer sorrendre downtime-tűrő, kis rendszerben? | **Nincs explicit prózai állásfoglalás** — a production-útmutató nem tér ki rá | docs.docker.com/compose/how-tos/production/ |



---

# sq04 — Mit kell menteni, és honnan tudjuk, hogy jó

# sq04 — Mit kell menteni, és honnan tudjuk, hogy a mentés jó

Kutatási jegyzőkönyv az `easter-memory-system` mentési politikájának megalapozásához. Minden állításnál tier-jelölés: **T1** = hivatalos dokumentáció/forráskód/lektorált tanulmány/hatósági anyag; **T2** = megbízható másodlagos forrás vagy gyártói termékdokumentáció; **T3** = fórum/blog/anekdota. A hivatalos dokumentumokat nyers HTML/PDF-ként kértük le (`curl` a proxyn keresztül, majd tag-stripelés / `pdftotext -layout`) — ez minden idézetnél jelölve, ahol WebFetch-et használtunk, az is jelölve (ebben a kutatásban egyszer sem kellett WebFetch-hez folyamodni, minden hivatalos forrás nyers letöltéssel sikerült).

---

## 1. Származtatott adat mentése — kell vagy nem?

**Fő megállapítás: a bevett gyakorlat és a hivatalos ajánlások egyaránt azt mondják, hogy az újraépíthető (derived) adatot NEM kell menteni, ha a forrásból való újraépítés az elvárt helyreállítási időn (RTO) belül elvégezhető.** Ez pontosan illik az index SQLite (FTS5 + embeddings) esetére, amely a markdown fájlokból újraépíthető.

### 1.1 AWS Well-Architected Framework — explicit, elvi szintű ajánlás

A **SUS04-BP08 "Back up data only when difficult to recreate"** gyakorlat kifejezetten ezt a kérdést tárgyalja (T1, hivatalos AWS dokumentáció, nyers HTML-ből, `curl`):

> "To minimize storage consumption, only back up data that has business value or is needed to satisfy compliance requirements. Examine backup policies and exclude ephemeral storage that doesn't provide value in a recovery scenario."
> — Implementation guidance: "Use your data classification to establish what data needs to be backed up. **Exclude data that you can easily recreate.** Exclude ephemeral data from your backups. Exclude local copies of data, unless the time required to restore that data from a common location exceeds your service level agreements (SLAs)."
> (AWS Well-Architected Framework, 2022-03-31 kiadás, SUS04-BP08, https://docs.aws.amazon.com/en_us/wellarchitected/2022-03-31/framework/sus_sus_data_a9.html)

A jelenlegi (legfrissebb) kiadásban ugyanez kicsit bővebben, "Common anti-pattern"-ként fogalmazva:

> "Common anti-patterns: You do not have a backup strategy for your data. **You back up data that can be easily recreated.**"
> — "Implementation steps: ... Exclude data that can be easily recreated. Exclude ephemeral data from your backups."
> (AWS Well-Architected Framework, legfrissebb kiadás, https://docs.aws.amazon.com/wellarchitected/latest/framework/sus_sus_data_a9.html) — T1

Egy másik, kapcsolódó AWS best practice (**REL09-BP01, "Identify and back up all data that needs to be backed up, or reproduce the data from sources"**) explicit kritériumot ad arra, mikor felesleges a mentés, és konkrét analóg példát is hoz — index-jellegű, forrásból újraépíthető adatra:

> "You might be able to meet data recovery needs by reproducing the data from other sources. ... In cases where sources like this can be used to meet your Recovery Point Objective (RPO) and Recovery Time Objective (RTO), **you might not require a backup**. Another example, if working with Amazon EMR, **it might not be necessary to backup your HDFS data store, as long as you can reproduce the data into Amazon EMR from Amazon S3.**"
> (https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_backing_up_data_identified_backups_data.html) — T1

Ez az utolsó példa (HDFS ↔ S3) szerkezetileg megegyezik az easter-memory-system esetével: HDFS egy számítási/index-réteg S3 (a tartós forrás) fölött, ahogy az FTS5+embedding index egy számítási/index-réteg a markdown fájlok (a tartós forrás) fölött.

**Megerősítés (2. és 3. független forrás):** A CIS Controls v8 Control 11 (Data Recovery) és a NIST-hez köthető RPO/RTO-fogalom általánosan ugyanezt az elvet közvetíti (a helyreállítási cél az irányadó, nem a "mindent ments el" elve) — ugyanakkor sem a CIS, sem a NIST-anyagok, amiket találtunk, nem mondják ki ilyen direkt módon a "ne mentsd, ami újraépíthető" elvet, mint az AWS anyaga. Ez az elv leginkább az AWS Well-Architected Frameworkből, illetve a lenti konkrét rendszerpéldákból (SQLite FTS5, Elasticsearch/keresőmotorok, HDFS) igazolható közvetlenül.

### 1.2 Konkrét rendszerek, amelyek kimondottan kihagyják a származtatott indexet a mentésből, és hogyan indokolják

**SQLite FTS5 — a hivatalos dokumentáció kifejezetten "eldobható és újraépíthető" adatszerkezetként kezeli a teljes szövegű indexet** (T1, https://sqlite.org/fts5.html, nyers HTML):

> "In this, and any other situation where the FTS index and its content table have become inconsistent, the **'rebuild' command may be used to completely discard the contents of the FTS index and rebuild it based on the current contents of the content table.**"

> "6.12. The 'rebuild' Command — This command **first deletes the entire full-text index, then rebuilds it based on the contents of the table or content table.**"
> `INSERT INTO ft(ft) VALUES('rebuild');`

Ez szó szerint az easter-memory-system indexére alkalmazható esetleírás: a markdown fájlok a "content table" szerepét töltik be, az FTS5-index pedig bármikor eldobható és a tartalomból újraépíthető. A `secure-delete` opció dokumentációja is megerősíti, hogy egy formátumváltás esetén a hivatalos ajánlott hiba-elhárítás maga a `rebuild` parancs ("invalid fts5 file format ... run 'rebuild'").

**Elasticsearch / keresőmotorok — mért idő egy valós, nagy méretű indexre.** A SoundCloud mérnöki csapata nyilvánosan dokumentálta, hogy a teljes katalógusukat (720+ millió dokumentum) egy forrásból (Kafka log + MySQL) **1 óra alatt tudják újraépíteni**, optimalizálás előtt ez **1 hétig, rosszabb esetben 1 hónapig** tartott (T2, mérnöki blog, konkrét production-számokkal, nem lektorált):

> "This process took up to one week, though there was even one scenario where it almost took one month to roll out a bug fix." ... "Including the long tail, **the primary shard indexing takes around 30 minutes for more than 720 million documents**, whereas it previously took three hours."
> (SoundCloud Backstage Blog, "How to Reindex One Billion Documents in One Hour at SoundCloud", 2019, https://developers.soundcloud.com/blog/how-to-reindex-1-billion-documents-in-1-hour-at-soundcloud/)

Ez azt jelenti, hogy egy pár ezer fájlos, egygépes rendszer esetén (az easter-memory-system mérete) az index-újraépítés ideje minden bizonnyal **másodperces–perces nagyságrendben** van, nem órákban — de erre a konkrét, kis méretre nem találtunk közvetlenül mért benchmarkot (lásd `hianyok.md`).

**Kihagyás indoklása általánosságban, a keresőmotor-architektúrákban**: a fenti AWS/SQLite/SoundCloud-minta közös logikája, hogy a **napló/forrás (Kafka, S3, markdown-fájlrendszer) a tartós igazságforrás, az index csak egy gyorsítótár-jellegű vetület rajta** — ezt a mintát "Kappa Architecture"-nek nevezi a SoundCloud-cikk is (T2). Ugyanez az elv áll az easter-memory-system mögött is: a markdown a forrás, az FTS5+embedding index a vetület.

**Tér-megtakarítás mért adata:** közvetlen, konkrét "X MB szöveg → Y MB derived index, ennyivel kisebb a mentés" mérést nem találtunk publikált formában (lásd hiányok). Az AWS és SQLite dokumentáció csak elvi szinten (STORAGE consumption minimization) érvel, konkrét arányszám nélkül.

---

## 2. A beágyazások (embedding vektorok) különleges esete

**Fő megállapítás: az embedding-generálás pénzbe és számítási időbe kerül (külső API-hívás vagy helyi modellfuttatás soronként), ezért a bevett minta nem az, hogy "sose mentsd", hanem hogy egy tartalom-hash alapú gyorsítótárral (cache) elkerülik az ismételt, felesleges újraszámítást — függetlenül attól, hogy a végleges vektorindexet magát mentik-e.**

### 2.1 A tartalom-hash alapú embedding cache mint bevett minta

A **LlamaIndex hivatalos dokumentációja** (T2, gyártói/projekt-dokumentáció, https://docs.llamaindex.ai/en/stable/module_guides/loading/ingestion_pipeline/, nyers HTML-ből) kifejezetten ezt a mintát írja le az `IngestionPipeline`/`IngestionCache` komponensben:

> "Each node+transformation pair is cached, so that subsequent runs (if the cache is persisted) with the same node+transformation combination can use the cached result and save you time." ... "**In an IngestionPipeline, each node + transformation combination is hashed and cached.** This saves time on subsequent runs that use the same data."

A dokumentum konkrét kódpéldát is ad `OpenAIEmbedding()`-re mint az egyik "transformation"-re, tehát a hash-elt és cache-elt lépések közé kifejezetten beletartozik az embedding-számítás is. Emellett a dokumentáció külön dokumentum-szintű deduplikációt is leír hash alapján:

> "Storing a map of doc_id -> document_hash ... If a duplicate doc_id is detected, and the hash has changed, the document will be re-processed and upserted. If a duplicate doc_id is detected and the hash is unchanged, **the node is skipped.**"

Ez pontosan az easter-memory-systemre alkalmazható minta: ha egy markdown fájl (bejegyzés) tartalmi hash-e nem változott, nem kell újraszámolni az embeddingjét — akár friss mentésből való visszaállítás, akár indexújraépítés esetén.

**Megerősítés — más eszközök hasonló mintája (T3, oktató-jellegű, de konzisztens több forrásból):** több RAG-fejlesztési útmutató (pl. „Caching embeddings: avoid re-embedding", theneuralbase.com; Redis „semantic cache" hivatalos dokumentáció, redis.io/docs/latest/develop/use-cases/semantic-cache/) ugyanezt az elvet ismétli: a drága embedding-hívást kulcs-alapú (jellemzően tartalmi hash vagy normalizált szöveg alapú) cache-elje a rendszer, mielőtt újra API-hívást indítana. Ezek nem hivatalos szabványok, hanem konzisztensen ismételt gyakorlati minta.

### 2.2 Mért újraszámítási költség

**Ár (T1, OpenAI hivatalos modelldokumentáció, https://developers.openai.com/api/docs/models/text-embedding-3-small, nyers HTML `curl`-lel, user-agent fejléccel — az `openai.com/api/pricing/` oldal a proxyn keresztül 403-at adott, ez dokumentálva a `keresesek.md`-ben):**

> "Embeddings Per 1M tokens ∙ Batch API price. Cost $0.02" (text-embedding-3-small) — "Quick comparison Cost text-embedding-3-large $0.13 · text-embedding-3-small $0.02"

Vagyis (OpenAI hivatalos árazás, 2026 eleji állapot): **$0.02 / 1M token** a kisebb, **$0.13 / 1M token** a nagyobb embedding-modellnél. Ezt független másodlagos forrásokkal (OpenRouter modell-oldala, Helicone árkalkulátor, embeddingcost.com) is megerősítettük — mindegyik ugyanezt a két számot adja vissza (T2, keresés-eredmények alapján, nem nyers letöltéssel ellenőrizve egyenként).

Egy pár ezer bejegyzésből álló, egygépes rendszer esetén ez a költség gyakorlatilag elhanyagolható (pl. 5000 bejegyzés × átlag 200 token ≈ 1 millió token ≈ **$0.02–0.13 összesen egy teljes újraszámításért**) — ez fontos arányítási adat a döntéshez.

**Idő/tétel mért adat: hiány.** Az OpenAI hivatalos dokumentációjában nem találtunk konkrét, publikált "másodperc/tétel" vagy "tétel/másodperc" átviteli sebesség-számot az embeddings végpontra (csak rate limit-eket TPM/RPM-ben, ami *korlát*, nem *mért teljesítmény*). A Rate limits szakasz konkrét számokat ad a korlátokra (pl. Tier 1: 1,000,000 TPM), de ez felső korlát, nem tényleges mért idő. **Ezt hiányként rögzítjük** — nem találtunk lektorált vagy hivatalos "X ezer embedding ennyi idő alatt" benchmarkot; csak közvetett becslés lehetséges a TPM-korlátokból.

### 2.3 A kétszintű származtatottság — miért kell külön kezelni az embeddinget a puszta indextől

A kutatás megerősíti a kérdésfeltevés implicit állítását: **két különböző "derived data" réteg van, és ezeket nem szabad egy kalap alá venni.**

- A **szöveges index (FTS5 b-tree)** tisztán számítási művelet a meglévő szövegen — CPU-idő, nincs külső függőség, nincs pénzköltség, gyors (ld. SQLite `rebuild` parancs fent). Ez klasszikus "derived, biztonsággal kihagyható" adat.
- Az **embedding vektorok** ezzel szemben egy külső (vagy helyi, de számításigényes) modell kimenete, aminek újraszámítása **pénzbe kerül és időt/API-kvótát emészt fel**, ezért még ha technikailag "származtatott" (rebuildable) adat is, a gyakorlatban érdemesebb tartalom-hash alapú cache-eléssel elkerülni az *ismételt* felesleges újraszámítást — nem azért, mert menteni kellene őket egy klasszikus katasztrófa-helyreállítási mentésben, hanem mert egy egyszerű "dobjuk el és építsük újra minden alkalommal" stratégia pazarló lenne napi/gyakori helyreállítási vagy fejlesztési ciklusban.

Ez a megkülönböztetés (rebuild-cost szempontjából "ingyenes" derived data vs. "drága" derived data) nincs kimondva egyetlen forrásunkban sem explicit terminológiával — ez a mi szintézisünk a fenti tényekből, ezért **ezt nem forrás-idézetként, hanem levezetésként** jelöljük.

---

## 3. Mentés-ellenőrzés (verification) — mit ellenőriznek a nagy mentőeszközök, és mit NEM

### 3.1 BorgBackup `check` (T1, https://borgbackup.readthedocs.io/en/stable/usage/check.html, Borg 1.4.5, nyers HTML)

> "The `check` command **verifies the consistency of a repository and its archives.** It consists of two major steps: [1] Checking the consistency of the repository itself. This includes checking the segment magic headers, and both the metadata and data of all objects in the segments. **The read data is checked by size and CRC. Bit rot and other types of accidental damage can be detected this way.** [2] Checking consistency and correctness of the archive metadata **and optionally archive data (requires `--verify-data`)**. ... To cryptographically verify the file (content) data integrity pass `--verify-data`, but keep in mind that **this requires reading all data and is hence very time consuming.**"

Tehát **alapértelmezett `borg check` NEM olvassa vissza és nem ellenőrzi kriptográfiailag a tényleges fájltartalmat** — csak a szegmens-CRC-ket és a metaadat-konzisztenciát. A tényleges tartalmi integritást csak a `--verify-data` opcióval ellenőrzi, ami "very time consuming":

> "The `--verify-data` option will perform a full integrity verification (as opposed to checking the CRC32 of the segment) of data, which means reading the data from the repository, decrypting and decompressing it. **It is a complete cryptographic verification and hence very time consuming, but will detect any accidental and malicious corruption.**"

A `check` **alapból csak olvasás (read-only)**, és a hibajavítás (`--repair`) explicit figyelmeztetéssel jár a maga veszélyéről:

> "The check command is a **read-only task by default**." ... "`--repair` is a **POTENTIALLY DANGEROUS FEATURE and might lead to data loss!**" ... "Repairing a repository means **sacrificing some data** for the sake of the repository as a whole ... it is, by definition, a **potentially lossy task**."

A dokumentáció **nem ad konkrét ajánlott gyakoriságot** (nincs "havonta" vagy "hetente" kimondva ezen az oldalon) — csak azt, hogy hosszú repository-nál `--max-duration`-nel részleges, ütemezhető ellenőrzésre osztható a feladat. Ezt hiányként rögzítjük.

### 3.2 restic `check` / `check --read-data` (T1, https://restic.readthedocs.io/en/stable/045_working_with_repos.html, nyers HTML)

> "In order to detect these things before they become a problem, **it's a good idea to regularly use the check command** to test whether your repository is healthy and consistent... There are two types of checks that can be performed: [1] **Structural consistency and integrity**, e.g. snapshots, trees and pack files (**default**) [2] **Integrity of the actual data** that you backed up (enabled with flags, see below)"

> "**By default, `check` does not verify that the actual pack files on disk in the repository are unmodified**, because doing so requires reading a copy of every pack file in the repository. To tell restic to also verify the integrity of the pack files in the repository, use the `--read-data` flag." ... "Since `--read-data` has to download all pack files in the repository, **beware that it might incur higher bandwidth costs than usual and also that it takes more time than the default check.**"

Vagyis a restic-nél is **pontosan ugyanaz a kettéválás, mint a Borgnál**: az alapértelmezett `check` csak a szerkezetet (index, snapshot-fa, pack-fájl jelenlét) nézi, a tényleges bájtszintű tartalom-integritást (bitrot-detektálás) csak `--read-data` végzi el, és ez drága (idő + esetleg hálózati sávszélesség/felhő-letöltési díj).

A dokumentáció itt is felkínálja a részleges mintavételes megoldást a teljes költség elkerülésére:

> "Alternatively, use the `--read-data-subset` parameter to check only a subset of the repository pack files at a time. ... `--read-data-subset=x%` ... **it is easy to automate checking a small subset of data after each backup.**"

**Ajánlott gyakoriság:** a restic hivatalos dokumentációja itt sem ad konkrét számot (nap/hét/hónap) — csak azt sugallja, hogy a `--read-data-subset`-et "minden mentés után" lehet automatizálni kis részhalmazra. Ez implicit ajánlás, nem explicit szám — hiányként jelöljük.

### 3.3 ZFS `scrub` (T1, https://openzfs.github.io/openzfs-docs/man/master/8/zpool-scrub.8.html — OpenZFS hivatalos man page)

> "A normal scrub **examines all data in the specified pools and verifies each block's checksum.** A thorough scrub additionally decrypts and/or decompresses blocks as they are read. For replicated (mirror, raidz, or draid) devices, **ZFS automatically repairs any damage discovered during the scrub.**" ... "Scrubbing and resilvering are very similar operations. **The difference is that resilvering only examines data that ZFS knows to be out of date** ... **whereas scrubbing examines all data to discover silent errors due to hardware faults or disk failure.**"

Ez a legteljesebb a három közül: a scrub minden blokk checksumját ellenőrzi, és replikált (redundáns) vdev esetén automatikusan javít is — de ez a javítás **csak akkor lehetséges, ha van redundancia** (mirror/raidz/draid); egyetlen lemezes pool esetén a scrub csak *detektál*, javítani nem tud.

**Ajánlott gyakoriság — konkrét szám, más hivatalos forrásból (Oracle Solaris ZFS Administration Guide, T1, https://docs.oracle.com/en/operating-systems/solaris/oracle-solaris/11.4/manage-zfs/scheduled-data-scrubbing.html):**

> "`scrubinterval` determines the time interval between automatic scrubbing. ... **By default, the time interval is set to 30 days.**"

Ez az egyetlen forrásunk, amely **konkrét, hivatalosan ajánlott számszerű gyakoriságot ad** (30 nap) a három mentés-/integritás-ellenőrző eszköz közül. A közösségi gyakorlat (fórumokon, T3, nem idézzük szó szerint) ehhez hasonlóan "havi" scrub-ot javasol asztali/vállalati lemezeknél, "heti"-t megbízhatatlanabb (pl. fogyasztói SATA/SMR) lemezeknél — de ez konszenzus-jellegű közösségi ajánlás, nem T1 forrás.

### 3.4 Összefoglaló táblázat: mit ellenőriznek, és mit NEM

| Eszköz | Alapértelmezett viselkedés | Mit ellenőriz alapból | Mit NEM ellenőriz alapból | Teljes tartalom-ellenőrzés |
|---|---|---|---|---|
| **Borg `check`** | csak szerkezet | szegmens CRC, metaadat-konzisztencia | tényleges fájltartalom bájt szerint | `--verify-data` (lassú, kriptográfiai) |
| **restic `check`** | csak szerkezet | index, snapshot-fa, pack-fájl jelenléte | pack-fájlok tényleges tartalma a lemezen | `--read-data` (lassú, sávszélesség-igényes); részleges mintavétel: `--read-data-subset` |
| **ZFS `scrub`** | teljes adat | minden blokk checksuma; redundancia esetén automatikus javítás | — (ez a "teljes" szint) | maga a `scrub` már ez; `-t` (thorough) még dekódolja/dekompresszálja is |

**Közös mintázat mindhárom eszköznél:** a gyors, olcsó ellenőrzés (metaadat/szerkezet) *nem* garantálja, hogy a mentés visszaállítható — csak azt, hogy a "boríték" nem sérült. A tényleges "vissza tudom-e állítani sértetlenül" kérdésre csak a drága, teljes-adat-olvasásos mód ad választ (Borg `--verify-data`, restic `--read-data`, ZFS `scrub`). Ez direkt válasz a feladat 3. kérdésére: **anélkül, hogy ténylegesen visszaállítanánk, csak a teljes adat visszaolvasásával és checksum-ellenőrzésével lehet megbízhatóan megállapítani a visszaállíthatóságot** — a metaadat-szintű ellenőrzés ennél gyengébb garanciát ad.

---

## 4. Csendes adatromlás (bit rot / silent corruption) — mért gyakoriság

### 4.1 CERN (Kelemen, 2007) — az eredeti, gyakran hivatkozott mérés

**Forrás (T1, elsődleges, a szerző saját prezentációja, https://www.nsc.liu.se/lcsc2007/presentations/LCSC_2007-kelemen.pdf, PDF, `pdftotext -layout`-tal kinyerve):** "Silent Corruptions", Peter Kelemen (CERN IT), LCSC 2007, Linköping, Svédország, 2007. október 18.

**Módszertan:** a `fsprobe` nevű, saját fejlesztésű eszközzel **4000 CERN-csomóponton** futtattak háttérfolyamatot, amely ismert bitmintát ír egy kb. 2 GiB-os tesztfájlba, majd visszaolvassa és összehasonlítja (max. 1 MiB/s I/O terheléssel, hogy ne zavarja a produkciós terhelést).

**Mért eredmény, szó szerint:**

> "fsprobe deployed on 4000 nodes · **2000 incidents reported (total ~97 PiB traffic)** · >6/day on average observed! · **192 MiB data corrupt: 0.000000185%** · **320 nodes affected (27 hardware types)**"

Vagyis: ~97 PiB adatforgalomból összesen 192 MiB sérült meg észrevétlenül — ez **kb. 1.85 × 10⁻⁹ arány (0.000000185%)**. Ez a szám kifejezetten a *silent* (a hardver/szoftver által nem jelzett) korrupcióra vonatkozik, nem az összes lemez/hardverhibára.

A kontextus, amit a CERN infrastruktúrájáról ad: "~6'000 nodes, ~20'000 hard drives (18'610 models), ~1'200 RAID controllers ... corruptions are more like a **question of when, not if**."

**Konklúzió a prezentációból, szó szerint:**

> "silent corruptions are a **fact of life** — first step towards a solution is detection — complete elimination seems impossible" ... "existing datasets are **at the mercy of Murphy**" ... "**correction will cost time AND money**"

A prezentáció zárómondata (Ronald Reagan-idézettel): "**Trust, but verify**" — ami direkt válasz a sq04 szellemére.

### 4.2 NetApp / Wisconsin-Madison / Toronto tanulmány (Bairavasundaram et al., FAST '08) — nagy méretű, lektorált vizsgálat

**Forrás (T1, lektorált konferenciacikk, USENIX FAST '08, https://www.usenix.org/legacy/events/fast08/tech/full_papers/bairavasundaram/bairavasundaram.pdf, PDF, `pdftotext -layout`-tal kinyerve):** "An Analysis of Data Corruption in the Storage Stack", Bairavasundaram (Wisconsin-Madison), Goodson (NetApp), Schroeder (Toronto), Arpaci-Dusseau × 2 (Wisconsin-Madison).

**Módszertan:** **1.53 millió lemez** (NetApp production storage rendszerekben, 358 000 nearline/SATA és 1.17 millió enterprise/FC lemez), **41 hónapos** megfigyelési időszak.

**Mért eredmény, szó szerint:**

> "We find **more than 400,000 instances of checksum mismatches** over the 41-month period." ... "Of the total sample of 1.53 million disks, **3855 disks developed checksum mismatches – 3088 of the 358,000 nearline disks (0.86%) and 767 of the 1.17 million enterprise class disks (0.065%).**" ... "**On average, each disk developed 0.26 checksum mismatches.**"

17 hónapos, összehasonlítható ablakra szűkítve:

> "**0.66% of nearline disks develop at least one mismatch** within 17 months... while ... **only 0.06% of enterprise class disks develop a mismatch** during that time."

Fontos minőségi megállapítás (nem csak arányszám):

> "(i) **nearline disks (and their adapters) develop checksum mismatches an order of magnitude more often than enterprise class disk drives**, (ii) checksum mismatches within the same disk **are not independent events** and they show **high spatial and temporal locality**, (iii) checksum mismatches across different disks in the same storage system **are not independent.**"

**Az elváláshoz kritikus megállapítás — a csendes korrupció miért veszélyesebb, mint egy egyszerű szektorhiba:**

> "**Silent data corruptions could lead to data loss more often than latent sector errors, since, unlike latent sector errors, they cannot be detected or repaired by the disk drive itself.** ... In fact, **basic protection schemes such as RAID may also be unable to detect these problems.**"

### 4.3 Backblaze meghajtó-meghibásodási statisztika — más metrika, fontos megkülönböztetés

**Forrás (T2, gyártói/üzemeltetői blog publikált módszertannal és nyilvános nyers adattal, https://www.backblaze.com/blog/backblaze-drive-stats-for-2025/, nyers HTML):**

> "As of the end of 2025, Backblaze was monitoring 341,664 drives..." ... "**The annual AFR is down: this year finishes strong at 1.36%, down from 1.55% in 2024.**" ... "**Lifetime AFR is 1.30%** this quarter."

**Fontos módszertani figyelmeztetés:** ez az AFR (Annualized Failure Rate) a **teljes meghajtó-meghibásodást** méri (a meghajtót lecserélik/kiesik), **NEM azonos a csendes bitkorrupcióval** (ami a CERN- és NetApp-tanulmány tárgya). A Backblaze-szám tehát más jelenséget mér, mint amit a 4.1–4.2 pont — ezt a report-ban explicit külön kell választani, nehogy a két metrikát összemossuk. A Backblaze-adatot csak kontextusként (a "lemezek egyáltalán mennyire megbízhatók" háttérkérdésre) idézzük, nem a "silent corruption" kérdésre válaszként.

### 4.4 Mit jelent ez egy néhány ezer fájlos, egygépes rendszer méretében?

A fenti mérések alapján a válasz: **igen, a forrásaink alapján ez a kockázat a kérdéses rendszer méretében gyakorlatilag elhanyagolható, de nem nulla.**

- A CERN-mérés szerint a silent corruption aránya kb. **1.85 × 10⁻⁹** (192 MiB / 97 PiB) — egy néhány ezer fájlos, tipikusan néhány tíz–száz MB méretű markdown-korpusz esetén ez a valószínűségi szám gyakorlatilag azt jelenti, hogy **évekig, sőt évtizedekig sem várható egyetlen néma bitsérülés sem** pusztán a mérés arányszáma alapján — DE ez a szám 1 gépre, 1 lemezre vonatkozó extrapoláció, és a CERN-mérés maga is hangsúlyozza, hogy a korrupció "nem független" (térben/időben csomósodik), tehát egyetlen hibás lemez esetén a helyi kockázat ugrásszerűen megnőhet.
- A NetApp-tanulmány szerint egyetlen lemez 17 hónap alatt **0.66% (nearline) / 0.06% (enterprise)** eséllyel fejleszt ki *legalább egy* checksum-eltérést — ez lemezenkénti, nem fájlonkénti valószínűség, és nem jelenti azt, hogy a konkrét adatfájl sérül, csak hogy a lemez valahol legalább egy checksum-hibát mutat.
- **Konklúzió, amit a források alapján ki lehet mondani:** egygépes, néhány ezer fájlos méretben a silent corruption **statisztikailag ritka, de nem elméleti** kockázat — pontosan ezért létezik a checksumos mentés-ellenőrzés (3. pont) mint olcsó védekezés, nem azért, mert a kockázat nagy, hanem mert a *detektálás* olcsó, a *be nem észlelt* korrupció következménye (csendes adatvesztés) viszont aránytalanul súlyos lehet egy pótolhatatlannak jelölt adatnál (markdown fájlok, audit napló, felhasználói DB). Ezt a CERN-anyag is kimondja: "correction will cost time AND money" — tehát a védekezés ára nem a valószínűséggel arányos, hanem a *következmény súlyosságával*.

---

## 5. Titkok és kulcsok a mentésben

### 5.1 NIST SP 800-57 Part 1 Rev. 5 — a legrészletesebb, kulcstípusonként bontott hivatalos ajánlás

**Forrás (T1, hivatalos NIST kiadvány, https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf, PDF, `pdftotext -layout`):**

Az általános elv, szó szerint (8.2.2 szakasz):

> "It is often necessary for users and/or administrators to be able to recover keying materials from backup storage. **However, if operations can be continued without the backup of keying material (e.g., by re-keying) or the keying material can be recovered or reconstructed without being saved, it may be preferable not to save the keying material in order to lessen the possibility of a compromise of the keying material or other cryptographically related information.**"

Ez **közvetlen, elvi szintű megerősítése** a sq04 alapfeltevésének: ha egy titok újragenerálható/pótolható, jobb, ha nem mentjük — a mentés maga is kompromittálódási felület.

A backup storage (8.2.2.1) szakasz további finomítást ad:

> "**Not all keys need to be backed up.** The storage requirements of Section 6.2.2 apply to keying material that is backed up. Tables 7 and 8 provide guidance about the backup of each type of keying material and other related information. **An 'OK' indicates that storage is permissible but not necessarily required.**"

A dokumentum **kulcstípusonként bontott "Backup?" táblázatot** ad (7. és 8. táblázat), a legfontosabb sorok szó szerint:

| Kulcs-/adattípus | Mentés? (NIST SP 800-57 Pt.1 Rev.5, 7–8. táblázat) |
|---|---|
| Private signature key | **"No (in general)"** — az aláírás-letagadhatatlanság sérülne; kivétel indokolt esetben (pl. CA aláíró kulcsa), de akkor is a tulajdonos kizárólagos kontrollja alatt |
| Random number generation key | **"Not necessary and may not be desirable"** |
| Private ephemeral key-agreement key | **"No"** |
| Shared secret | **"No"** |
| RBG seed | **"No"** |
| Symmetric data encryption key | "OK" (megengedett, nem kötelező) |
| Symmetric authentication key | "OK" |
| Public signature-verification key | "OK; jelenléte egy publikus tanúsítványban elegendő lehet" |

Élettartamra vonatkozó szabály:

> "Keying material maintained in backup storage should remain in storage for at least as long as the same keying material is maintained for normal operational use ... When removed from backup storage, **all traces of the information in backup storage shall be destroyed** in accordance with Section 8.3.4."

**Megerősítés 2 — CIS Controls v8, Control 11.3 "Protect Recovery Data"** (T1, iparági szabványtest, https://cas8.docs.cisecurity.org/en/latest/source/Controls11/):

> "**Protect recovery data with equivalent controls to the original data. Reference encryption or data separation, based on requirements.**"

Ez azt mondja ki, hogy *ha* egy titok/kulcs mégis bekerül a mentésbe, az adott titokra érvényes védelmi szintet (titkosítás, hozzáférés-korlátozás) a mentésen is fenn kell tartani — nem lehet gyengébb védelem alatt, mint az élő rendszerben.

**Megerősítés 3 — francia CNIL "Guide de la sécurité des données personnelles"** (T1, hatósági, https://www.cnil.fr — a PDF-et egy ügyvédi kamarai tükörről, cnb.avocat.fr-ről töltöttük le, mert a cnil.fr közvetlen linkje 404-et adott; a tartalom a CNIL hivatalos kiadványa), 10. sz. adatlap ("Sauvegarder et prévoir la continuité d'activité"):

> "**Protéger les données sauvegardées au même niveau de sécurité que celles stockées sur les serveurs d'exploitation** (par exemple en chiffrant les sauvegardes, en prévoyant un stockage dans un lieu sécurisé, en encadrant contractuellement une prestation d'externalisation des sauvegardes)."
> (magyarul: "A mentett adatokat ugyanolyan biztonsági szinten kell védeni, mint az üzemeltetési szervereken tároltakat, például a mentések titkosításával...")

Ez a három forrás (NIST, CIS, CNIL) egybehangzóan azt mondja: **titkot/kulcsot csak akkor tegyünk mentésbe, ha ez elengedhetetlen a helyreállításhoz, és akkor is legalább ugyanolyan (titkosított) védelemmel, mint élesben.**

### 5.2 OWASP — Secrets Management Cheat Sheet és ASVS v5.0

**OWASP Secrets Management Cheat Sheet** (T1, hivatalos OWASP kiadvány, https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html, nyers HTML), 2.9 "Downtime, Break-glass, Backup and Restore" szakasz:

> "Consider the possibility that a secrets management service becomes unavailable for various reasons... **A few requirements regarding backup & restore. Ensure that:** An automated backup procedure is in place and executed periodically; base the frequency of the backups and snapshots on the number of secrets and their lifecycle. Frequently test restore procedures to guarantee that the backups are intact. **Encrypt backups and put them on secure storage with reduced access rights.** Monitor the backup location for (unauthorized) access and administrative actions."

Ugyanez a dokumentum a CI/CD szekcióban (3.2.2) még explicitebb:

> "**Backup: back up secrets to product-critical operations in separate storage (e.g., cold storage), especially encryption keys.**"

**Fontos: az OWASP itt NEM azt mondja, hogy a titkokat ki kell hagyni a mentésből — épp ellenkezőleg, kifejezetten javasolja a titkok (különösen a titkosító kulcsok) mentését, elkülönített, titkosított tárolóban.** Ez árnyalja (de nem mondja ellent) a NIST fenti, kulcstípus-függő megközelítésének — lásd `ellentmondasok.md`.

**OWASP ASVS 5.0, V13.3 "Secret Management"** (T1, hivatalos OWASP szabvány, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x22-V13-Configuration.md, nyers Markdown a GitHub raw-ról):

> "**13.3.1** Verify that a secrets management solution, such as a key vault, is used to securely create, store, control access to, and destroy backend secrets. ... **Secrets must not be included in application source code or included in build artifacts.** For an L3 application, this must involve a hardware-backed solution such as an HSM."
> "**13.3.2** Verify that access to secret assets adheres to the principle of least privilege."
> "**13.3.4** Verify that secrets are configured to expire and be rotated based on the application's documentation."

Fontos, hogy **az ASVS V13.3 nem tér ki kifejezetten a "titok a mentésben" kérdésre** — csak az alkalmazás forráskódjából/build-artefaktumaiból tiltja ki a titkokat, a mentésekről nem szól direktben. Ezt hiányként rögzítjük: **az ASVS-ben nincs explicit "ne kerüljön titok a mentésbe" vagy "csak titkosítva kerülhet mentésbe" szabály** — ez a védelem csak közvetve, a secrets management megoldás (kulcstároló) általános elve felől vezethető le.

### 5.3 Összefoglalás — mit lehet kimondani a szakasz kérdésére

A hivatalos ajánlások összessége (NIST, CIS, CNIL, OWASP) alapján:

1. **Alapelv:** ha egy titok pótolható/újragenerálható a rendszer megszakítása nélkül, ne kerüljön mentésbe (NIST SP 800-57 explicit indoklással: csökkenti a kompromittálódási felületet).
2. **Ha egy titok szükséges a helyreállításhoz** (pl. az easter-memory-system esetében az embedding-szolgáltatás API-kulcsa, aminek hiányában az egész rendszer nem indítható újra), **azt lehet és sok esetben kell is menteni** — de a mentésnek ugyanolyan (vagy erősebb) védelemmel kell rendelkeznie, mint az élő titoknak (titkosítás, hozzáférés-korlátozás, monitorozás) — ezt mind a CIS, mind a CNIL, mind az OWASP kimondja.
3. **Egyik forrás sem javasolja a titkok mentésből való teljes, feltétel nélküli kizárását** — ez tévhit lenne; a helyes megközelítés a *feltételes* mentés (csak ami szükséges) + *fokozott védelem*.

---

## 6. Mentés visszaállítása és a jogosultság — GDPR törléshez való jog vs. mentés

**Fontos módszertani megjegyzés a teljes szakaszhoz:** az alábbiakban kizárólag azt közöljük, amit a hatósági források **szó szerint kimondanak**. Nem vonunk le jogi következtetést, és nem adunk jogi tanácsot — a döntést embernek kell meghoznia.

### 6.1 Az Egyesült Királyság adatvédelmi hatósága (ICO) — a legrészletesebb, közvetlenül kérdésre szabott hivatalos iránymutatás

**Forrás (T1, elsődleges, hatósági, https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-erasure/, nyers HTML):**

Az ICO külön alcímet szentel a kérdésnek: **"Do we have to erase personal data from backup systems?"**

> "**If a valid erasure request is received and no exemption applies then you will have to take steps to ensure erasure from backup systems as well as live systems.** Those steps will depend on your particular circumstances, your retention schedule (particularly in the context of its backups), and the technical mechanisms that are available to you."

> "You must be **absolutely clear with individuals as to what will happen to their data** when their erasure request is fulfilled, including in respect of backup systems. It may be that **the erasure request can be instantly fulfilled in respect of live systems, but that the data will remain within the backup environment for a certain period of time until it is overwritten.**"

A kulcsmondat, amely a gyakorlati megoldást írja le:

> "**The key issue is to put the backup data 'beyond use', even if it cannot be immediately overwritten.** You must ensure that you do not use the data within the backup for any other purpose, i.e. that the backup is simply held on your systems until it is replaced in line with an established schedule. **Provided this is the case it may be unlikely that the retention of personal data within the backup would pose a significant risk**, although this will be context specific."

**Nincs konkrét, számszerű határidő** az ICO ezen oldalán — a "beyond use" elv és az "established schedule" (a szervezet saját, előre meghatározott mentés-rotációs ütemterve) az irányadó, nem egy fix naptári határidő.

### 6.2 EDPB (Európai Adatvédelmi Testület) — 2025-ös koordinált vizsgálat, "Issue 6: Deletion of personal data in the context of back-ups"

**Forrás (T1, elsődleges, EU-s hatósági testület, https://www.edpb.europa.eu/system/files/2026-02/edpb_cef-report_2025_right-to-erasure_en.pdf, "2025 Coordinated Enforcement Action — Implementation of the right to erasure by controllers", elfogadva 2026. február 10., PDF `pdftotext -layout`-tal kinyerve):**

Ez egy kifejezetten friss (2026 februári), 32 EGT-s adatvédelmi hatóság közös vizsgálatán alapuló jelentés, amely 764 adatkezelő válaszát elemzi. Külön fejezetet szentel a mentések kérdésének:

> "**Back-up is an important tool to protect the integrity of the personal data** when the controller is affected by a security incident (for example ransomware). It is therefore important to protect the integrity of the back-up. **Depending on the technical settings and risks, it might not always be advisable to modify or delete information from back-ups.** But, in that case, organisations should have appropriate procedures to keep track of erasure requests and comply with them on restored systems, as much as possible, in case of a data breach affecting the integrity of the organisation's system."

Ez fontos: **az EDPB kifejezetten elismeri, hogy nem mindig tanácsos módosítani/törölni a mentésekből** — vagyis a mentés integritása (immutabilitása) legitim, elismert ellenérdek a törléssel szemben, feltéve, hogy a szervezet más módon (pl. visszaállítás utáni utólagos törlési eljárással) kezeli a kockázatot.

**Megfigyelt gyakorlatok, szó szerint (a jelentés nem ír elő új szabályt, hanem a vizsgált gyakorlatokat írja le):**

> "**Half of the responding SAs raised concerns regarding the deletion of personal data in this context.** Many controllers were found not to have specific procedures and measures in place to handle erasure requests in the context of back-ups, relying either on automatic deletion measures (not specific to the erasure requests received) or on the implementation of retention periods applicable to the concerned back-ups."

> "Some controllers further raised concerns over technical aspects, stating that **in certain situations it may not be possible to simply change parts of the data, especially when the back-up must be preserved as a whole.**"

> "Some controllers were found to rely on the retention periods they implement for their back-ups to ensure that back-ups are wiped after a specific period of time. ... one SA identified a practice where controllers rely on internal procedures **deleting personal data in increments spanning long periods of time. The SA found that this procedure creates difficulties to conclude whether deletion triggered by a data subject's erasure request takes place 'without undue delay', as per the requirement of Article 17(1) GDPR.**"

**A jövőre nézve — az EDPB maga mondja ki, hogy jelenleg NINCS kész, egységes iránymutatás:**

> "As a result of the CEF, the EDPB **may consider** the following actions: **Providing more guidance and recommendations to explain how controllers should practically deal with erasure in back-ups and what is meant by 'without undue delay' in this context.**"

Ez direkt, elsődleges forrásból származó megerősítése annak, hogy **jelenleg (2026 eleje) nincs uniós szinten egységesen előírt, számszerű határidő** a mentésekből való törlésre — az EDPB épp azt jelzi, hogy ezt a hiányt a jövőben pótolni *tervezi*.

**Konkrét, megfigyelt (nem előírt, hanem gyakorlatban látott) mintapélda a jelentésből:**

> "For instance, an interesting solution implemented by a controller consists of relying on a tool that, upon reaching a pre-determined end-date (retention period), extracts all the personal data relating to a data subject from all systems of the organisation. The data is then moved away from employees' access to an anonymised and separate system where **it will be permanently erased one month later.**"

> "Some stated that data from back-ups is only deleted **when it is automatically overwritten by another back-up or when updating or deleting the back-up at set intervals, for instance, one month.**"

**Ajánlott gyakorlatok a jelentésből (nem kötelező előírás, hanem az EDPB által kiemelt jó gyakorlat):**

> "Follow established standards to erase and destroy data in a secure and structured manner." / "Verify that erasure has been carried out and be able to demonstrate such erasure." / "To mitigate the structural impact deletion brings to back-ups, some controllers **replace the personal data they wish to delete with strings of random characters.**"

### 6.3 Összefoglalás a 6. kérdésre — kizárólag azt állítva, amit a források kimondanak

- **Igen, létezik hatósági, elsődleges forrásból származó kezelés** erre a problémára: az ICO (UK) és az EDPB (EU, 2026. február) egyaránt kifejezetten a mentések kontextusában tárgyalja a törléshez való jogot.
- **Egyik hatósági forrás sem mond ki egy konkrét, kötelező számszerű határidőt** a mentésekből való törlésre. Az ICO a "beyond use" elvet és a szervezet saját rotációs ütemtervét nevezi meg irányadónak; az EDPB pedig kifejezetten jelzi, hogy **jelenleg nincs egységes uniós iránymutatás** arra, mit jelent a "indokolatlan késedelem nélkül" (Article 17(1) GDPR) egy mentési kontextusban, és ezt **a jövőben tervezi pótolni**.
- **Mindkét forrás elismeri** legitim technikai ellenérvként, hogy egy mentés integritásának megőrzése (nem módosítható/nem részlegesen törölhető jellege) ütközhet az azonnali törlés elvárásával, és mindkettő elfogadható megoldásként kezeli, ha a szervezet a mentést "használaton kívülre helyezi" (nem használja fel más célra) és egy előre meghatározott, dokumentált ütemterv szerint természetes úton (felülírással/lejárattal) semmisíti meg.
- **A "visszakerülő jogosultságok" konkrét kérdésére** (visszaállított bejegyzés visszakapja-e a korábban visszavont jogosultságot) **egyik forrásunk sem tért ki explicit módon** — sem az ICO, sem az EDPB anyaga nem tárgyalja külön a hozzáférés-jogosultságok (mint access control state) visszaállítás utáni kezelését, csak a személyes adatok törlését általánosságban. **Ezt konkrét hiányként rögzítjük** (lásd `hianyok.md`).



---

# sq05 — A mentés mint cserélhető komponens: programozási minták

# Megállapítások — mentés és helyreállítás mint cserélhető komponens

**Kampány:** `mentes-frissites` · **Egység:** `sq05`
**Készült:** 2026-09-12
**Módszer:** `anthropic-skills:deep-web-research`, **degradált (egyágenses) módban** — l. a módszertani megjegyzést alább.
**Bizonyítékanyag:** `_vault/backup-adapter-patterns/` (37 forrás, 75 atomi állítás, mind idézve és linkellenőrizve — l. `linkek.md`, `keresesek.md`)

**Tier-jelölés e dokumentumban** (a feladat saját skáláját követve): **T1** = hivatalos dokumentáció / forráskód / könyv; **T2** = megbízható másodlagos / gyártói leírás; **T3** = fórum, blog, közösségi tartalom, aggregátor (Wikipedia is ide esik, mert nem elsődleges és nem szerkesztőségi). A begyűjtött 37 forrásból **32 T1**, **0 T2**, **5 T3** — a kutatás túlnyomórészt elsődleges forrásokra épül.

---

## Módszertani megjegyzés (degradált mód)

A skill előírása szerint a keresést Sonnet-alágensek, a szintézist egy Opus-alágens végzi, külön kontextusban. **Ez a session maga egy alegység-agent** egy nagyobb kampányban (`mentes-frissites`), ebben a környezetben nincs `Agent`/`Task` eszköz további subagentek indítására, és a skill maga is tiltja az egymásba ágyazott subagenteket. Ezért a keresés, a verifikáció és a szintézis **egyetlen folytonos kontextusban, szekvenciális fázisokban** zajlott (terv → keresés témánként → merge/shard/index → linkellenőrzés + önverifikáció → szintézis), Sonnet/Opus modell-szétválasztás **nélkül**. Ez a skill fő tervezési pillére, ezért ez a hiány itt kimondva marad. Ennek gyakorlati következménye: a forrás-gyűjtés alaposságát a nyers dokumentum-mennyiség (37 forrás, 32 T1) és a szigorú idézet-egyezés (minden állítás csak akkor került be, ha a pontos idézet szó szerint megtalálható volt a lementett forrásban) igyekszik pótolni, de a kontradikció-keresés és a megbízhatósági besorolás nem egy független második olvasat eredménye.

Minden fontos hivatalos dokumentációt és forráskódot **nyers HTML/nyers szövegként, curl-lal, a proxyn keresztül** kérdeztem le (GitHub fájloknál `raw.githubusercontent.com`), a `WebFetch` eszközt csak keresésre (`WebSearch`) és sehol tartalom-kinyerésre nem használtam ebben a kutatásban — minden idézet a ténylegesen letöltött, lementett fájlból származik. Kivétel: a `github.com` maga (web UI és API) ebben a környezetben egy külön kapcsolati réteg mögött van („GitHub access to this repository is not enabled for this session”), ezért a GitHub-on lévő *forrásfájlokat* `raw.githubusercontent.com`-on, egy GitHub-*issue* megvitatását pedig a Wayback Machine (`web.archive.org`) nyilvános archívumán keresztül értem el — ez nem a domain blokkjának megkerülése, hanem egy másik, önmagában is nyilvános és independens archívum használata. Részletek: `keresesek.md`.

---

## 1. Hogyan absztrahálják a valódi mentőeszközök a tárolási célt?

### 1.1 restic — kettős interfész: egy belső Go-interfész és egy nyilvános huzal-protokoll

A restic forráskódjában (`internal/backend/backend.go`) a **`Backend` interfész 13 metódusból** áll:

> „`Properties() Properties`, `Hasher() hash.Hash`, `Remove(...)`, `Close() error`, `Save(...)`, `Load(...)`, `Stat(...)`, `List(...)`, `IsNotExist(...)`, `IsPermanentError(...)`, `Delete(...)`, `Warmup(...)`, `WarmupWait(...)`” [T1, forráskód]

Fontos, hogy ez **belső** (`internal/`) csomag — nincs stabil, dokumentált, harmadik fél számára nyitott Go-plugin-felület. A ténylegesen **nyilvános, dokumentált „backend-interfész”** egy huzal-szintű **REST API-specifikáció**, amit bármilyen szerver implementálhat:

> „Restic can interact with an HTTP backend that respects the following REST API.” [T1, restic hivatalos doksi, References > REST Backend]

Ezt implementálja a hivatalos `rest-server`, és — ez a kutatás egyik kulcsfelfedezése — **maga az rclone is**, a `rclone serve restic` alparanccsal. A restic **12 tárolási célt implementál natívan a kódjában** (local, sftp, REST Server, Amazon S3, Minio, S3-kompatibilis, Wasabi, Alibaba OSS, OpenStack Swift, Backblaze B2, Azure Blob Storage, Google Cloud Storage), és **minden további célt nem maga valósít meg, hanem az rclone-nak delegál**:

> „The program rclone can be used to access many other different services and store data there. […] Restic takes care of starting and stopping rclone.” [T1]

**Mit rejtenek el szándékosan a metódusnevekben, és mit nem:** a `Backend` interfészhez tartozó `Properties` struct **explicit kapacitás-flageket** hordoz, amiket a réteg *nem* egyenlít ki, csak jelez:

> „`HasAtomicReplace bool` — states whether Save() can atomically replace files” és „`HasFlakyErrors bool` — states whether the backend may temporarily return errors that are considered as permanent for existing files.” [T1]

A `Warmup`/`WarmupWait` metóduspár kifejezetten a hideg tárolású (S3 Glacier-szerű) backendek átmenetét kezeli — és a hivatalos FAQ nyíltan kimondja, hogy ez **időben is** eltér backendenként:

> „Expect restores to hang from 1 up to 42 hours depending on your storage class, provider and luck.” [T1]

A restic tervezési dokumentuma (`doc/design.rst`) egy application-szintű **írási/olvasási sorrend-protokollt** definiál kifejezetten azért, hogy a repository konzisztens maradjon **akkor is**, ha „a kliens vagy a tároló backend összeomlik, például áramkimaradás miatt, vagy megszakad a (hálózati) kapcsolat” [T1] — vagyis a magasabb réteg kompenzálja azt, amit a backend-kontraktus önmagában nem garantál.

### 1.2 BorgBackup — a legkevesebb absztrakció, majd (Borg 2.0-ban) explicit fordulat

A Borg 1.x repository-URL-je **csak két dolgot** ismer: helyi (vagy helyileg mountolt) fájlrendszer-útvonalat, illetve `ssh://` távoli repót [T1, Usage > General > Repository URLs]. Az `ssh://` mögött **nem egy absztrakt tárolási backend** áll, hanem egy **másik, a szerveren telepített Borg-folyamat**, amivel a kliens SSH-n át beszél:

> „the client uses SSH as a transport to talk to the remote agent, which is another Borg process” [T1, FAQ]

A hivatalos FAQ **explicit technikai indoklást** ad arra, miért nincs objektumtár-backend — nem egy „miért nincs S3 támogatás” bekezdésben, hanem a fájlrendszer-kompatibilitási szakaszban:

> „Borg is doing nothing special in the filesystem, it only uses very common and compatible operations (even the locking is just 'rename').” [T1]

Ez pontosan az a művelet (atomikus `rename`), amit egy objektumtár API (PUT/GET/LIST/DELETE) nem biztosít. A Borg belső repository-formátuma egy **append-only szegmens-log** (`BORG_SEG`), amit egy *forward-compacting* algoritmus tart karban — ez meglévő szegmensfájlok beolvasását és újraírását igényli [T1, Internals > Data structures], ami egy tisztán kulcs-érték objektumtár API-val drágán, ha egyáltalán megoldható.

**2015 óta** egy 48 lájkot kapott, mai napig nyitott közösségi feature-kérésben (`borgbackup/borg#102`) a felhasználó explicit az S3 „eventual consistency” viselkedését nevezte meg aggodalomként [T3, közösségi tartalom, nem hivatalos állásfoglalás] — vagyis a felhasználói igény és az aggály már 11 éve dokumentált.

**Fordulat — Borg 2.0 (2024+):** a hivatalos kiadási jegyzék szerint a Borg 2.0 egy **teljesen új, különálló absztrakciós réteget** vezetett be, a **`borgstore`** kulcs-érték tárolót:

> „packs are assembled client-side, then stored into the repository, enabling efficient usage of cloud storage (and other high-latency storages)” […] „borgstore is a key/value store in Python, currently supporting file:, REST […], sftp:, rclone:, and s3:/b2: backends. Borgstore backends are easy to implement, so there might be even more in the future.” [T1, borgbackup.org hivatalos kiadási jegyzék]

A `borgstore` forráskódjában a **`BackendBase` absztrakt osztály 12 kötelező (absztrakt) metódusból** áll — `create, destroy, open, close, mkdir, rmdir, info, load, store, delete, move, list` —, plusz 3, alapértelmezett implementációval rendelkező, felülírható metódus (`defrag`, `hash`, `quota`) [T1, forráskód]. A saját README **explicit kimondja a képesség-egyenlőtlenséget**, nem rejti el:

> „quota support (only `posixfs`)” […] „permissions checking (only `posixfs`)” [T1]

— vagyis csak a helyi fájlrendszer-backend tudja a kvótát és a jogosultságokat kezelni, a többi nem. A forráskód egy külön megjegyzésben azt is rögzíti, hogy az rclone-alapú backend **nem tud valódi tárolás-oldali módosítási időbélyeget** adni:

> „backends that would only echo a client-supplied timestamp (e.g. rclone) must report 0 (unknown) instead” [T1]

**Ez a Borg-történet önmagában is válasz a 3. kérdésre** (mikor nem éri meg absztrahálni): egy évtizedig helyesen döntöttek úgy, hogy *nem* építenek backend-absztrakciót, mert a repository-formátum nem tette lehetővé olcsón — amikor a formátumot (packek kliens-oldali összeállítása) megváltoztatták, az absztrakció is azonnal, könnyen bevezethetővé vált. Az absztrakció helye tehát a *repository-formátum* döntésétől függött, nem attól, hogy „jó gyakorlat”-e absztrahálni.

### 1.3 rclone — kis kötelező mag + nevesített, opcionális képesség-interfészek

Az rclone forráskódja explicit kimondja:

> „Fs is the interface a cloud storage system must provide” [T1, `fs/types.go`]

Ez az **`Fs` interfész** az `Info` interfészt (6 tag: `Name`, `Root`, `String`, `Precision`, `Hashes`, `Features`) és 5 saját metódust (`List`, `NewObject`, `Put`, `Mkdir`, `Rmdir`) tartalmaz — összesen **11 kötelező metódus**. A forráskód saját megjegyzése explicit elválasztja ettől az opcionális réteget:

> „Note that optional interfaces are found in features.go” [T1]

A `features.go`-ban **26 külön nevesített opcionális interfész** van (`Purger`, `Copier`, `Mover`, `DirMover`, `CleanUpper`, `ListRer`, `Abouter`, `ChangeNotifier`, `Disconnecter`, `UserInfoer`, `Shutdowner` stb.) [T1, forráskód]. A `Features` struct egy explicit, nevesített flaget is tartalmaz a részleges feltöltésre:

> „`PartialUploads bool` — uploaded file can appear incomplete on the fs while it's being uploaded” [T1]

Az rclone hivatalos „Overview” dokumentációja egy **táblázatban**, backendenként közli, mely opcionális képesség (Purge, Copy, Move, DirMove, CleanUp, ListR, StreamUpload, MultithreadUpload, LinkSharing, About, EmptyDir) érhető el — ez a **legrészletesebb, hivatalosan dokumentált „mit nem tud elrejteni egy backend-absztrakció” táblázat**, amit ez a kutatás talált (l. 4. pont). A hozzájárulási útmutató kimondja:

> „we have >50 backends to maintain so keeping them as similar as possible to each other is a high priority” [T1, volatilis, 2026-09-12-i állapot]

és a főoldal szerint (2026-09-12-i állapot) „**Over 70 cloud storage products support rclone**” [T1, volatilis]. Az rclone tehát a legszélesebb — és a restic, a Borg 2.0, valamint a Duplicati is *ráépít* a hosszú far kezelésére (l. lent, kereszthivatkozott megállapítás).

### 1.4 Kopia — a legexplicitebb, prózában megfogalmazott konzisztencia-kontraktus

A Kopia `Storage` interfésze (`repo/blob/storage.go`) **12 metódusból** áll (`GetCapacity`, `ListBlobs`, `GetBlob`, `GetMetadata`, `ConnectionInfo`, `DisplayName`, `PutBlob`, `DeleteBlob`, `Close`, `FlushCaches`, `ExtendBlobRetention`, `IsReadOnly`) [T1, forráskód]. A forráskód doc-kommentje **ez a kutatás legerősebb egyetlen idézete a 4. kérdésre**, mert szó szerint, prózában kimondja a backendtől elvárt kontraktust:

> „The underlying storage system must provide: high durability, availability and bit-rot protection; **read-after-write** - blob written using PutBlob() must be immediately readable using GetBlob() and ListBlobs(); **atomicity** - it mustn't be possible to observe partial results of PutBlob() via either GetBlob() or ListBlobs(); timestamps that don't go back in time (small clock skew up to minutes is allowed); reasonably low latency for retrievals. The required semantics are provided by existing commercial cloud storage products (Google Cloud, AWS, Azure).” [T1]

Ez azt jelenti, hogy a Kopia **kizárja** azokat a tárolókat, amik nem read-after-write konzisztensek — vagyis egy régi, eventual-consistency-s object store *kontraktus szerint* nem lenne kompatibilis Kopia-backend. Egy sentinel hibaértékkel (`ErrSetTimeUnsupported`) és egy `DefaultProviderImplementation` mintával (ami alapból „nem támogatott” hibát ad vissza, amíg egy konkrét backend felül nem írja) kezeli az opcionális képességeket [T1].

Kopia natívan **8 célt** támogat (S3/S3-kompatibilis, Azure Blob, B2, GCS, Google Drive, WebDAV, SFTP, helyi/hálózati fájlrendszer), és — **immár harmadszor** ugyanaz a minta — az rclone-nak delegálja a többit, de itt a hivatalos dokumentáció **kockázatot is vállal az őszinteségben**:

> „WARNING: Rclone support is experimental. In theory, all Rclone-supported storage providers should work with Kopia. However, in practice, only Dropbox, OneDrive, and Google Drive have been tested to work with Kopia through Rclone.” [T1, volatilis]

### 1.5 Duplicati — a legkisebb kötelező interfész, kategorizált célok

A Duplicati `.NET` `IBackend` interfésze saját dokumentációja szerint:

> „The interface all backends must implement.” [T1, forráskód]

**10 tagból** áll (`DisplayName`, `ProtocolKey`, `ListAsync`, `PutAsync`, `GetAsync`, `DeleteAsync`, `Description`, `GetDNSNamesAsync`, `TestAsync`, `CreateFolderAsync`). Explicit kezeli azt az esetet, amikor egy backendnek nincs „mappa” fogalma: ilyenkor a `CreateFolderAsync`-nak `MissingMethodException`-t kell dobnia, ahelyett hogy színlelné a mappa-létrehozást [T1] — ismét egy eset, ahol a különbséget *jelzik*, nem *elrejtik*. A hivatalos dokumentáció **négy kategóriába** sorolja a célokat (standard, provider-specifikus, fájlszinkronizációs, decentralizált), és a decentralizált szolgáltatókról kimondja: „may have different speed characteristics, compared to other storage providers” [T1]. Az **rclone (negyedszerre!) itt is megjelenik**, mint „standard” célkategória tagja [T1].

### 1.6 Kereszttool-megállapítás: konvergencia egy tucat metódus körül, és a hosszú far egységes delegálása

Két, ebben a kutatásban külön is dokumentált, **több független T1 forrással alátámasztott** mintázat:

> **[Magas megbízhatóság]** Legalább **négy, egymástól teljesen független fejlesztésű mentőeszköz** (restic, Borg 2.0/borgstore, Kopia, Duplicati) jutott **függetlenül ugyanarra a megoldásra**: a hosszú far tárolási céljait (több tucat felhő-szolgáltató) nem újraimplementálják, hanem **az rclone-nak delegálják** — vagy alfolyamatként elindítva (restic, Kopia, Borg2), vagy külön binárisként hivatkozva rá (Duplicati). [Forrás: restic „Preparing a new repository”, Borg 2.0 kiadási jegyzék, Kopia „Repositories”, Duplicati „Destination overview” — mind T1]
>
> **[Magas megbízhatóság]** A négy tool kötelezően implementálandó backend-interfésze **feltűnően hasonló méretű**: restic `Backend` = 13 metódus, `borgstore` `BackendBase` = 12, Kopia `Storage` = 12, rclone `Fs`+`Info` = 11. Ez arra utal, hogy egy tárolási backend absztrakciójának „helyes” mérete a gyakorlatban **egy tucat körüli metódusra konvergál** — sem 3-4 (túl kevés, nem fedi le a valódi élettartam-kezelést), sem 30+ (a variánsokat inkább *opcionális* interfészekbe/flagekbe teszik ki, nem a kötelező magba). [Forrás: mind a négy forráskód-interfész, T1]
>
> **[Magas megbízhatóság]** Mind a négy eszköz **ugyanazt a szerkezeti döntést** hozta a képesség-különbségekre: kicsi kötelező mag + a különbségeket **nevesített, explicit** opcionális interfészekkel/kapacitás-flagekkel/hibaértékekkel jelzik (restic `HasAtomicReplace`/`HasFlakyErrors`; rclone 26 opcionális interfész + `PartialUploads`; borgstore „quota support (only posixfs)”; Kopia `ErrSetTimeUnsupported` + `DefaultProviderImplementation`). **Egyik eszköz sem próbálja meg egységesíteni vagy elrejteni ezeket a különbségeket** — mindegyik explicitté teszi őket a típusrendszerben. [Forrás: mind a négy forráskód, T1]

---

## 2. Melyik minta illik erre, és mit mondanak róluk az elsődleges források?

### 2.1 Strategy (Gang of Four, 1994) — pontosan erre való

A GoF könyv (Gamma, Helm, Johnson, Vlissides — *Design Patterns: Elements of Reusable Object-Oriented Software*, Addison-Wesley, 1994, 315. o.) Strategy-fejezetének **Intent**-sora szó szerint:

> „Define a family of algorithms, encapsulate each one, and make them interchangeable. Strategy lets the algorithm vary independently from clients that use it.” [T1, 315. o.]

Az **Applicability** szakasz négy esetet sorol fel, amikor a mintát ajánlják — az egyik szó szerint ez a mi esetünk:

> „you need different variants of an algorithm. For example, you might define algorithms reflecting different space/time trade-offs.” [T1, 316. o.]

A **Consequences** szakasz explicit kimondja a mintázat előnyét (a döntéshozó számára releváns: több implementáció közötti választás) **és korlátját is**:

> „A choice of implementations. Strategies can provide different implementations of the same behavior. The client can choose among strategies with different time and space trade-offs.” […] „Clients must be aware of different Strategies […] Therefore you should use the Strategy pattern only when the variation in behavior is relevant to clients.” [T1, 319. o.]

**Értelmezés erre a projektre:** a mentési *cél* (hova mentünk) pontosan „ugyanazon viselkedés különböző implementációi, más idő/tér/hálózati kompromisszumokkal” — ez szó szerint a GoF Applicability-listájának második pontja. A Strategy tehát nem analógia, hanem **a GoF saját szövege szerint pontosan erre lett kitalálva**. A korlát is releváns: csak akkor érdemes, ha a kliens (a rendszer üzemeltetője) számára *ténylegesen releváns* a különbség — ami ennél a projektnél igaz, mert a felhasználó kimondottan kérte a cserélhetőséget.

### 2.2 Ports and Adapters / Hexagonal Architecture (Alistair Cockburn, 2005) — a portvágás szabálya

Cockburn saját, eredeti (2005-ös, „HaT Technical Report 2005.02” jelzésű) cikke a `alistair.cockburn.us/hexagonal-architecture/` oldalon a **kulcskérdésre pontos, szó szerinti választ ad**. A „How Many Ports?” szakasz:

> „What exactly a port is and isn't is largely a matter of taste. At the one extreme, every use case could be given its own port, producing hundreds of ports for many applications. Alternatively, one could imagine merging all primary ports and all secondary ports so there are only two ports, a left side and a right side. **Neither extreme appears optimal.**” [T1]

> „My selection tends to favor a small number, **two, three or four ports**, as described above and in the Known Uses.” [T1]

A konkrét esettanulmányok mind kis számú, **célhoz kötött** portot mutatnak: az időjárás-riasztó rendszernek 4 (időjárás-hírfolyam, adminisztrátor, értesített feliratkozók, feliratkozói adatbázis), a kávégép-vezérlőnek 4 (felhasználó, receptek/árak adatbázisa, adagolók, pénzbedobó), a kórházi gyógyszerkiadó rendszernek 3 (nővér, receptadatbázis, gyógyszeradagoló) [T1].

**A legfontosabb, korábban ebben a projektben már vitatott pont — a portvágás alapja szándék, nem technológia:** Cockburn egy konkrét esettanulmányt ír le, ahol a csapat kezdetben *technológia szerint* azonosította az interfészeket („trigger-data arriving over a wire feed”, „notification data to be sent to answering machines” stb.), és ez karbantartási rémálomba torkollott, amikor új technológiákat (http, email) kellett hozzáadni. A megoldás:

> „**Their shift in design was to architect the system's interfaces by purpose rather than by technology**, and to have the technologies be substitutable (on all sides) by adapters.” [T1]

Ez szó szerint az a megfogalmazás, ami ebben a projektben korábban felmerült: **a portot cél/szándék szerint vágjuk** (pl. „mentési cél” mint egy port), **nem technológia szerint** (nem külön port az „S3-nak” és külön a „helyi lemeznek” — azok ugyanannak a portnak az adapterei).

**Erre a projektre nézve:** a hexagonális modell szerint valószínűleg **egy** port indokolt a mentésre/helyreállításra (a „hova mentünk” cél-port), amögött több adapter (fájlrendszer, S3-kompatibilis tároló stb.), plusz külön, önálló portok az adatbázis-illesztőnek (amit már megcsináltak) és esetleg az ütemezésnek — ez utóbbi kérdés az 5. pontban részletezve.

### 2.3 Repository (PoEAA) — a szerzőség fontos, és az analógia félrevezető

**Szerzőségi pontosítás (ahogy a feladat kérte):** a `martinfowler.com/eaaCatalog/repository.html` oldal — bár Martin Fowler honlapján, a *Patterns of Enterprise Application Architecture* katalógus részeként jelenik meg — **explicit, névvel ellátott szerzősége**:

> „This pattern is part of Patterns of Enterprise Application Architecture […] **Edward Hieatt and Rob Mee** — 05 March 2003” [T1]

Tehát **nem Fowler írta** a Repository mintát, hanem Edward Hieatt és Rob Mee. A minta definíciója:

> „Mediates between the domain and data mapping layers using a **collection-like interface** for accessing domain objects.” […] „Client objects construct query specifications declaratively and submit them to Repository for satisfaction.” [T1]

**Miért félrevezető analógia a mentésre:** a Repository fogalmilag egy **domén-objektum-gyűjtemény lekérdezhető, specifikáció-alapú** nézete egy adatleképezési réteg fölött — pontosan azért kell, mert a domén-objektumok komplexek, és a lekérdezéskonstrukciós logikát egy helyre kell koncentrálni. A mentési cél viszont nem domén-objektumok gyűjteménye, amit specifikációval lekérdezünk, hanem **durva szemcséjű bájt-blobok tárolása kulcs/útvonal szerint** (store/load/delete/list) — pontosan azt látjuk mind a négy vizsgált eszköznél (1. pont), hogy egyikük sem „gyűjtemény”-ként, hanem kulcs-érték / blob-tárként modellezi a célt. **Ez a kutatás nem talált elsődleges forrást, ami kimondottan a Repository-t kritizálná backup-kontextusban** (ez hiányként jelölve a `hianyok.md`-ben) — az itt levont következtetés a Repository saját, T1-forrásból idézett definíciójából adódó **következtetés**, nem egy külső forrás állítása.

---

## 3. Mikor NEM éri meg absztrahálni?

### 3.1 YAGNI — Kent Beck találta ki, Fowler csak dokumentálja

Martin Fowler saját bliki-bejegyzése (2015.05.26) **explicit nem magának tulajdonítja** a YAGNI-t:

> „The origin of the phrase is an early conversation between **Kent Beck and Chet Hendrickson** on the C3 project. Chet came up to Kent with a series of capabilities that the system would soon need, to each one Kent replied 'you aren't going to need it'.” [T1]

Fowler négy költségtípust azonosít egy felesleges, feltételezett funkcióra: **megépítés, késleltetés (delay), fenntartás (carry), javítás (repair)** költsége. Egy idézett külső vélemény (Jeremy Miller, tweet — **T3**, másodkézből idézve) frappánsan összefoglalja a kockázatot:

> „any extensibility point that's never used isn't just wasted effort, it's likely to also get in your way as well” [T3]

**Fontos árnyalat, ami ellensúlyozza a felhasználó kérését is:** Fowler explicit leszögezi, hogy a YAGNI **nem** vonatkozik a kód könnyebb módosíthatóságát célzó erőfeszítésre:

> „Yagni only applies to capabilities built into the software to support a **presumptive feature**, it does not apply to effort to make the software easier to modify.” [T1]

Ez azt jelenti: **ha a felhasználó kimondottan, explicit kérte** a cserélhetőséget (nem feltételezett, jövőbeli, spekulatív igény, hanem kinyilvánított tervezési szabály), akkor a YAGNI **nem** szól ellene automatikusan — a YAGNI a *hallgatólagosan feltételezett* jövőbeli igények ellen szól, nem a *kimondott* tervezési korlátok ellen. A hangsúly áttolódik arra, hogy **mekkora legyen** az absztrakció, nem arra, hogy legyen-e.

### 3.2 Speculative Generality — a nevet Brian Foote adta, nem Fowler/Beck

A *Refactoring* (2. kiadás, Martin Fowler és Kent Beck) hivatalos kiadói (Pearson/InformIT) kivonata:

> „**Brian Foote suggested this name** for a smell to which we are very sensitive. You get it when people say, 'Oh, I think we'll need the ability to do this kind of thing someday' and thus add all sorts of hooks and special cases to handle things that aren't required. **The result is often harder to understand and maintain.** If all this machinery were being used, it would be worth it. But if it isn't, it isn't.” [T1]

Vagyis a szagnak **három nevesített szerzője van egyszerre**: a nevet Brian Foote javasolta, a könyvet (amiben szerepel) Fowler és Beck írták. A diagnosztikai jel is dokumentált: „Speculative generality can be spotted when the only users of a function or class are test cases.” [T1] — ha csak a teszt használja, gyanús.

### 3.3 Rule of Three — Don Roberts fogalmazta meg Fowlernek, mélyebb gyökere 1988-ig nyúlik

A Wikipédia (T3, tájékozódásra) szerint „the rule was popularised by Martin Fowler in *Refactoring* and attributed to Don Roberts.” Ezt **két, egymástól független T3 forrás szó szerint megegyezően** idézi a *Refactoring* (2. kiadás) 58. oldaláról:

> „Here's a guideline Don Roberts gave me: The first time you do something, you just do it. The second time you do something similar, you wince at the duplication, but you do the duplicate thing anyway. The third time you do something similar, you refactor.” [T3×2, egyezően idézve: eoinnoble.com és egy független GitHub-jegyzet-gist, mindkettő p.58 hivatkozással]

Egy alapos, forrásokat idéző blogbejegyzés (eoinnoble.com) mélyebbre ás: Roberts és Ralph Johnson egy 1996-os cikkében („Evolving Frameworks”) saját mintájukat „a Rule of Three egy speciális esetének” nevezik, egy 1988-as RMISE workshopra hivatkozva (Ted Biggerstaff-nak tulajdonított megjegyzésekkel) [T3]. **Ez a nyomozás kimutatja, hogy Roberts eredeti tanácsa nem egy függvény-szintű „emeld ki, ha háromszor másolod” szabály volt, hanem egy rendszer/keretrendszer-szintű megfigyelés arról, hogy egy komponens csak több (legalább három) konkrét alkalmazás után bizonyul ténylegesen újrafelhasználhatónak** — ami **közvetlenül releváns erre a projektre**: a „hány konkrét mentési cél kell ahhoz, hogy megérje az absztrakció” kérdésre Roberts eredeti értelmezése szerint a válasz nem 1, hanem inkább 3 körüli (bár a felhasználó itt már *előre*, tervezetten jelezte az igényt, ami más helyzet, mint a visszamenőleges refaktorálás — l. 3.1 YAGNI-árnyalat).

### 3.4 Dokumentált eset a rossz/korai absztrakció káráról — Sandi Metz

Sandi Metz (RailsConf 2014, majd blogbejegyzés, 2016.01.20 — **T3**, elismert gyakorló szakember saját blogja, nem lektorált, de a szakmában széles körben idézett) egy konkrét, lépésről lépésre dokumentált mintázatot ír le arra, hogyan válik egy eredetileg jó absztrakció rosszá:

> „1. Programmer A sees duplication. 2. […] extracts duplication and gives it a name […] 5. A new requirement appears for which the current abstraction is *almost* perfect. 6. Programmer B […] alters the code to take a parameter, and then add logic to conditionally do the right thing […] 7. Another new requirement arrives. […] Another additional parameter. Another new conditional. **Loop until code becomes incomprehensible.**” [T3]

A jelenséget a *sunk cost fallacy* tartja fenn:

> „the more complicated and incomprehensible the code […] the more we feel pressure to retain it” [T3]

Metz tanácsa: „**duplication is far cheaper than the wrong abstraction**” [T3] — vagyis inkább vissza kell vonni (duplikációt visszaállítani) egy rosszul bevált absztrakciót, mint conditional-okkal foltozgatni.

**Erre a projektre nézve, ellensúlyként:** a kutatás nem talált **mért** (számszerűsített, pl. „X mérnökóra elveszett emiatt”) esettanulmányt korai absztrakció káráráról — ez hiányként jelölve. A dokumentált minták (Metz, Fowler) mind **kvalitatívak**: „nehezebb érteni és karbantartani”, nem számszerűsítettek. Ami viszont **igenis jól dokumentált és mérhető** ebben a kutatásban: a Borg-történet (1.2 pont) egy valós, ~10 éves esetet mutat, ahol a hiányzó absztrakció miatt egy egész főverziót (Borg 2.0) kellett bevezetni egy új réteggel (`borgstore`) — ez a „mikor éri meg” kérdés fordítottja: **a hiányzó, majd utólag bevezetett absztrakció migrációs költsége** dokumentált (kiadás-jegyzék, önálló GitHub-repó), bár nem számszerűsítve.

---

## 4. Mit nem tud elrejteni egy mentési interfész?

Ez a kérdés nagyrészt már az 1. pontban dokumentált forrásokból megválaszolt — itt csak összegezve, kategóriánként:

| Kategória | Konkrét, dokumentált példa | Forrás | Tier |
|---|---|---|---|
| **Atomicitás** | restic `Properties.HasAtomicReplace` — backendenkénti flag, nem egységes garancia | restic `backend.go` | T1 |
| **Atomicitás (kontraktus szintjén)** | Kopia: a backendnek „mustn't be possible to observe partial results of PutBlob()” — ha nem teljesíti, a backend *kontraktus szerint* nem használható | Kopia `storage.go` | T1 |
| **Átmeneti/„flaky” hibák** | restic `Properties.HasFlakyErrors` — egyes backendek időszakosan a végleges hibától megkülönböztethetetlen hibát adnak | restic `backend.go` | T1 |
| **Részleges feltöltés** | rclone `Features.PartialUploads` — „uploaded file can appear incomplete on the fs while it's being uploaded” | rclone `features.go` | T1 |
| **Hálózati megszakadás** | Borg `.checkpoint` archívum — alkalmazás-szintű, backend-független ellenállóképesség, mert a backend maga nem garantálja | Borg FAQ | T1 |
| **Hálózati megszakadás** | restic: az írási/olvasási sorrend-szabályok kifejezetten a „(network) connection between both is interrupted” esetére készültek | restic `design.rst` | T1 |
| **Eventual consistency** | Kopia kontraktusa kizárja a nem read-after-write backendeket; Amazon S3 **eredetileg** eventual consistency-vel indult, csak 2020 vége óta erősen konzisztens minden művelet | Kopia `storage.go`; AWS hivatalos oldal | T1 |
| **Eventual consistency (közösségi aggály)** | 2015-ös Borg-issue: felhasználó explicit kérdezte az S3 „eventual consistency” toleranciáját | GitHub issue #102 | T3 |
| **Sávszélesség-korlát** | Borg: feltöltési limit beépített (`--remote-ratelimit`), **letöltési (restore) limit NINCS beépítve**, külső eszköz kell | Borg FAQ | T1 |
| **Törlés-garanciák / mappa-fogalom hiánya** | Duplicati `IBackend.CreateFolderAsync` — ha a backendnek nincs „mappa” fogalma, explicit `MissingMethodException`-t kell dobnia, nem színlelni | Duplicati `IBackend.cs` | T1 |
| **Kvóta / jogosultság** | borgstore: „quota support (only posixfs)”, „permissions checking (only posixfs)” | borgstore README | T1 |
| **Módosítási időbélyeg pontossága** | rclone: 5-fokozatú skála (`-`, `R`, `R/W`, `DR`, `DR/W`) arra, mennyire megbízható a backend ModTime-ja; borgstore: rclone-backend csak 0-t (ismeretlen) adhat vissza | rclone Overview; borgstore `_base.py` | T1 |
| **Szerver-oldali műveletek hiánya** | rclone: ha egy backend nem támogatja a `Move`-ot, „rclone simulates it with Copy then delete”, ha a `Copy`-t sem, le kell tölteni és újra fel kell tölteni | rclone Overview | T1 |
| **Szabad hely lekérdezése** | rclone: „Backends without about capability cannot determine free space for an rclone mount” | rclone Overview | T1 |
| **Cluster-szintű atomicitás hiánya** | Velero: „cluster backups are not strictly atomic” — a mentés közben módosuló objektumok kimaradhatnak | Velero „How Velero Works” | T1 |
| **Sebesség-jellemzők** | Duplicati: a decentralizált tárolók „may have different speed characteristics” | Duplicati „Destination overview” | T1 |
| **Kísérleti/nem tesztelt lefedettség** | Kopia: az rclone-integráció „experimental”, elméletileg minden providerrel működne, gyakorlatban csak 3-at teszteltek | Kopia „Repositories” | T1 |

**[Magas megbízhatóság, kereszthivatkozott]** A mintázat, ami mind a négy tool forráskódjában/dokumentációjában egyformán megjelenik: **egyik eszköz sem próbálja meg elrejteni vagy egységesíteni ezeket a különbségeket** — mindegyik **explicit, nevesített** jelzőt (bool flag, sentinel hiba, dokumentált táblázat, figyelmeztető doboz) ad a fejlesztőnek/üzemeltetőnek, hogy tudja: *ez a konkrét backend itt más*. Ez maga a válasz a kérdésre: egy jól megtervezett mentési interfész **nem próbálja elrejteni** ezeket a különbségeket (mert nem is tudná hitelesen), hanem **explicitté teszi** azokat a típusrendszerben/kontraktusban.

---

## 5. Ütemezés és futtatás absztrakciója — mit/hova/mikor szétválasztása

### 5.1 Bacula — a legexplicitebb „What/Where/How/When” dekompozíció

A Bacula hivatalos dokumentációja **szó szerint** ezt a négyes felosztást adja:

> „Each Job resource definition contains the name of a Client and a FileSet to backup, the Schedule for the Job, where the data are to be stored, and what media Pool can be used. In effect, each Job resource must specify **What, Where, How, and When** or **FileSet, Storage, Backup/Restore/Level, and Schedule** respectively.” [T1]

Ez azt jelenti, hogy a Bacula konfigurációs modelljében **a mit (FileSet), a hova (Storage/Pool), a hogyan (Backup/Restore/Level) és a mikor (Schedule) mind külön, névvel ellátott, önállóan konfigurálható erőforrás-típusok**, amiket egy `Job` erőforrás köt össze. Egy `Job` csak egyféle típusú lehet; ha több kombináció kell, több `Job`-ot kell definiálni [T1].

### 5.2 restic — nincs beépített ütemező, szándékosan az OS-re bízva

A restic hivatalos parancslistájában (`restic --help`) **nincs** `schedule` vagy hasonló alparancs [T1, `manual_rest.html`] — csak `backup`, `restore`, `snapshots`, `forget`, `prune` stb. A hivatalos „Examples” dokumentáció bemutatja, hogyan kell resticet **systemd service-ként** futtatni (ambient capabilities beállítással) [T1] — vagyis a restic tudatosan **nem** foglalkozik az időzítéssel, azt az operációs rendszer eszközeire (cron, systemd timer) bízza.

### 5.3 Kopia — a „Policy” objektum a mit-et és a mikor-t köti össze, elkülönítve a hova-tól

A Kopia máshogy oldja meg: egy külön **`Policy`** objektum határozza meg **egyszerre** azt, hogy mit mentsünk és milyen gyakran:

> „Policies allow you to define what files/directories to backup in a snapshot and other features of a snapshot, including but not limited to: how frequently/when Kopia should automatically create snapshots of your data […]” [T1]

A policy hierarchikusan öröklődik (`global`, `username@hostname`, `@hostname`, `username@hostname:/path` szinteken) [T1], és **teljesen elkülönül** a `Repository` (a „hova”) konfigurációjától — a kettő külön parancscsoport (`kopia policy` vs `kopia repository`). Ez tehát egy **más felosztás**, mint Bacula négyes szétválasztása: itt a mit+mikor egy objektumban van, a hova külön.

### 5.4 Velero (Kubernetes) — külön CRD-k, külön kontrollerek

A Velero (T1, hivatalos doksi) három, egymástól elkülönített Kubernetes API-objektumot és kontrollert használ:

> „The schedule operation allows you to back up your data at recurring intervals. […] These intervals are specified by a Cron expression.” […] „The Velero client makes a call to the Kubernetes API server to create a `Backup` object. The `BackupController` notices the new `Backup` object […]” [T1]

A `Schedule` (mikor), a `Backup` (mit + eredmény), és a tárolási cél (`BackupStorageLocation`, külön, saját erőforrás) mind külön objektumok, külön kontrollerekkel.

**Összegzés — bevett szerkezet, de nem egységes felosztás:** mind a négy megnevezhető rendszer (Bacula, restic+systemd, Kopia, Velero) **szétválasztja** a mit/hova/mikor kérdéseket, de **különböző módokon** csoportosítja őket:
- Bacula: mind a négy (What/Where/How/When) teljesen külön, egy Job köti össze.
- restic: a mit+hogyan a repository-parancsokban van, a mikor **teljesen kívül van a programon** (OS-feladat).
- Kopia: mit+mikor egy `Policy`-ban, hova külön `Repository`-ban.
- Velero: mikor (`Schedule`) külön a mit-től (`Backup`), hova (`BackupStorageLocation`) is külön, mindegyik saját Kubernetes-objektum és kontroller.

---

## 6. Helyreállítás mint elsőrendű művelet

### 6.1 Van, ahol UGYANAZ az interfész — restic, Borg, Kopia

Mind a három fájlszintű eszköznél a `restore`/`extract` parancs **ugyanazon a repository-/storage-interfészen** keresztül fut, mint a `backup` — nincs külön „restore backend”. A restic parancslistájában a `restore` egy egyenrangú alparancs a `backup` mellett, ugyanazt a `-r/--repo` (Backend) kapcsolatot használva [T1, `manual_rest.html`].

### 6.2 Van, ahol SZÁNDÉKOSAN külön van választva, és a forrás megmondja, miért — Bacula

A Bacula ezt **explicit, dokumentáltan** másképp csinálja: a `Restore` egy **külön Job-típus**, aminek más a viselkedése:

> „Restore jobs cannot be automatically started by the scheduler as is the case for Backup, Verify and Admin jobs. To restore files, you must use the restore command in the console.” [T1]

> „no File database entries are generated since no Files are saved” [T1] — a restore-hoz lényegesen kevesebb katalógus-információ tartozik, mint a backuphoz.

**Az indoklás implicit a szövegből olvasható ki**: a restore emberi döntést igényel (*melyik* snapshot-ot, *melyik* fájlokat állítsuk vissza), ezért nem automatizálható ugyanúgy, mint egy rendszeres, felügyelet nélküli backup — a Bacula ezt a különbséget a Job-típus szintjén kényszeríti ki.

### 6.3 Van, ahol külön van választva, de más okból — Velero

A Velero is külön objektumot (`Restore`) és külön kontrollert (`RestoreController`) használ, de **más az indoklás**, mint Baculánál: nem az automatizálhatóság hiánya, hanem hogy a restore **explicit előkészítő lépéseket** igényel, amikre a backupnál nincs szükség:

> „The RestoreController fetches the backup information from the object storage service. It then runs some preprocessing on the backed up resources to make sure the resources will work on the new cluster. For example, using the backed-up API versions to verify that the restore resource will work on the target cluster.” [T1]

Ráadásul a Velero-nál a **tárolási cél** (`BackupStorageLocation`) is kaphat külön, restore-specifikus üzemmódot:

> „you can configure a backup storage location to be in read-only mode, which disables backup creation and deletion for the storage location” [T1]

— vagyis a backup és a restore ugyanazon a célon **eltérő jogosultsági/üzemmódi konfigurációt** kaphat.

**Összegzés:** a helyreállítást **nem kell** feltétlenül más interfészen megvalósítani, mint a mentést — a fájl-alapú eszközök (restic, Borg, Kopia) ezt sikeresen ugyanazon repository-interfészen oldják meg. Ahol mégis szándékosan szétválasztják (Bacula, Velero), ott a döntést **konkrét, eltérő operatív igény** indokolja (emberi jóváhagyás/kiválasztás szükségessége, illetve célrendszer-kompatibilitási előfeldolgozás) — nem az, hogy „a helyreállítás elvileg más”. **Erre a projektre nézve** ez azt sugallja: a mentési cél-portnak (adapter-interfésznek) elegendő lehet ugyanazokat a metódusokat (store/load/list/delete) kiszolgálnia mind mentéshez, mind visszaállításhoz — külön restore-specifikus interfészt csak akkor érdemes bevezetni, ha konkrét, azonosított igény van rá (pl. emberi jóváhagyási lépés az ütemező-rétegben, nem a tárolási adapterben).

---

## Ajánlás erre a projektre (szintézis, nem forrásidézet)

*Ez a szakasz nem forrásból idézett állítás, hanem a fenti bizonyítékanyagból levont, erre a konkrét projektre vonatkozó következtetés.*

1. **Minta:** **Strategy** (GoF) a mentési cél kiválasztására — pontosan a GoF saját Applicability-listájának megfelelően („different variants of an algorithm […] different space/time trade-offs”). A **Ports and Adapters** gondolkodás jó arra, hogy *hány és milyen* portot vágjunk: Cockburn saját szabálya szerint **cél szerint**, nem technológia szerint — vagyis valószínűleg **egy** „mentési cél” port (ami mögött több adapter: helyi fájlrendszer, S3-kompatibilis tároló stb.), nem külön port minden technológiának. A **Repository** minta neve/analógiája kerülendő — a store/load/list/delete blob-műveletek nem „gyűjtemény”-jellegűek, ez félrevezetheti a kódolvasót arra, hogy specifikáció-alapú lekérdezést várjon.
2. **Interfész mérete:** a 4 vizsgált eszköz konvergenciája alapján egy **~10-13 metódusos** kötelező mag (create/init, close, save/put, load/get, stat/info, list, delete, valamint explicit hibaosztályozás — pl. „nem létezik” vs. „átmeneti” vs. „végleges” hiba) reális célméret, a további képességkülönbségeket (atomicitás, kvóta, sávszélesség, cold-storage-restore-idő) **explicit, nevesített flagekkel/opcionális metódusokkal**, nem az alap-interfész bővítésével érdemes kezelni.
3. **YAGNI-ellensúly:** mivel a cserélhetőség **kimondott, explicit felhasználói követelmény** (nem hallgatólagos feltételezés), a Fowler-féle YAGNI-olvasat szerint ez **nem** esik a „presumptive feature” kategóriába — a kérdés nem az, hogy legyen-e adapter-réteg, hanem hogy **milyen szűkre** legyen szabva (rule-of-three olvasat: elég-e most 1-2 konkrét céllal, vagy várjunk a 3.-ig — ez már termékdöntés, nem architektúra-kérdés).
4. **Ütemezés:** a jelen rendszer mérete (egy gép, egy cég) alapján a **restic-mintázat** (nincs beépített ütemező, OS cron/systemd timer) vagy a **Kopia-mintázat** (egy „mikor + mit” policy-objektum, elkülönítve a céltól) egyaránt reális; a Bacula-szintű négyes szétválasztás valószínűleg túlméretezett ennyi felhasználóra.
5. **Restore:** nem szükséges külön interfész — ugyanaz a cél-adapter (store/load/list/delete) kiszolgálhatja mindkét irányt, hacsak nincs konkrét, azonosított igény (pl. emberi jóváhagyási lépés) az elkülönítésre.



---

# sq06 — Séma- és formátum-migráció motorfüggetlenül

# sq06 — Séma- és formátum-migráció motorfüggetlenül: megállapítások

**Kampány:** `mentes-frissites` · **Alkérdés:** sq06 · **Készült:** 2026-09-12
**Mód:** degradált egyágensű kutatás (lásd a dokumentum végén a módszertani megjegyzést)

Tier-jelölés: **T1** = hivatalos dokumentáció / forráskód / elsődleges céges közlemény ·
**T2** = megbízható másodlagos vagy gyártói/termék-leírás harmadik féltől ·
**T3** = fórum, blog, anekdota.

Minden idézet szó szerinti, a forrás nyers HTML-jéből/forráskódjából kinyerve (`curl` a
proxyn keresztül, ahol ez nem sikerült, ott jelölve). A `linkek.md` tartalmazza az összes
felkeresett URL-t lekérési móddal együtt; a `keresesek.md` az összes lefuttatott keresést.

---

## 0. Vezetői összefoglaló

A hét motort/eszközt megvizsgálva **két, egymással szemben álló tábor** rajzolódik ki:

- **Absztrakciót építők, ahol az absztrakció explicit HATÁRT is kap:** Liquibase,
  Django, Rails. Mindhárom dokumentálja (doksiban vagy forráskódban), hogy hol nem megy
  át az absztrakció — Liquibase changetype-onkénti "Database support" táblákkal,
  Django/Rails pedig **kapacitás-jelzőkkel** (`supports_*`), amelyek explicit **false**
  értéket vesznek fel motoronként pont azokra a képességekre, amiket a felhasználó
  kérdésként feltett (részleges index, generált oszlop).
- **Absztrakciót deliberáltan NEM építők:** Flyway core, Drizzle ORM. Mindkettő
  nyers, dialektus-specifikus SQL-t generál/futtat, és — ez fontos megállapítás —
  **egyikük hivatalos doksija sem tartalmaz kimondott "ne csináld motorfüggetlenné"
  mondatot**; a motorfüggetlenség hiánya inkább hallgatólagos tervezési következmény,
  amit külső eszközök (Spring Boot `{vendor}` placeholder) vagy közösségi gyakorlat
  (Drizzle: dialektusváltáskor migrációk törlése) old meg, NEM maga a mag-eszköz.

A **kapacitás-jelző minta** (SQLAlchemy-nál korábban azonosított minta) **tökéletes
megfelelőt talál** Django (`BaseDatabaseFeatures`, ~94 `supports_*`/`has_*` mező) és
Rails (`AbstractAdapter`, 40 db `supports_*?` predikátum) forráskódjában — mindkettő
**névre, nem motor-névre kérdez**. Liquibase ezzel szemben a `dbms` attribútumában
kifejezetten **motor-NÉV** szerint ágazik el, nem képesség szerint — ez éles,
dokumentált ellentét a két filozófia között (l. 5. és `ellentmondasok.md`).

A **GitLab 2019-es, névvel és dátummal ellátott hivatalos blogbejegyzése** a hiányzó
motorfüggetlenség-igény tankönyvi esete: konkrétan a **részleges index** hiányát
nevezi meg okként a MySQL-támogatás megszüntetésére — ugyanaz a konkrét képesség, amit
a Django/Rails forráskód `supports_partial_indexes`/`supports_partial_index?` jelzőként
kódol le. Ez a projekt egyik legerősebb, három egymástól független forrásból
(GitLab, Django, Rails) háromszorosan alátámasztott ténye.

A "Tolerant Reader" mintanév-ellenőrzés eredménye: **Martin Fowler valóban a saját
bliki-bejegyzésének (2011) szerzője** — ez NEM téves attribúció. A tényleges
összetévesztési kockázat a **szomszédos, gyakran együtt emlegetett** "Consumer-Driven
Contracts" mintával van, amit Fowler csak **közöl** a saját oldalán, de a **valódi
szerzője Ian Robinson** (2006) — ez pontosan az a fajta tévesztés, amire a megbízás
figyelmeztetett.

---

## 1. Liquibase — a "change type" absztrakció és a határa

### 1.1 Mit absztrahál a "change type"?

A hivatalos Liquibase referencia doksi (docs.liquibase.com, "What is a Change type?",
utolsó frissítés: 2026.08.12) így definiálja **[T1]**:

> "A Change Type is a database-independent XML, YAML, or JSON formatted change that you
> can specify to update your database with Liquibase. Change Types correspond to SQL
> statements applied to your database, such as CREATE TABLE."

Forrás: https://docs.liquibase.com/change-types/home.html

Tehát a change type egy **deklaratív, formátum-szintű** (XML/YAML/JSON) absztrakció egy
konkrét SQL-DDL-művelet felett — nem egy futásidejű köztes réteg, hanem egy
**fordítási időben (deploy-időben) SQL-re lefordított leíró**.

### 1.2 Van-e hivatalos kompatibilitási lista change type-onként?

**Igen — de nem egyetlen központi mátrix formájában, hanem change type-onkénti
"Database support" táblákban.** Minden egyes change type saját referencia-oldalán
szerepel egy tábla, amely soronként adatbázisonként "Supported" / "Not Supported"
státuszt ad meg. Példa: az `addAutoIncrement` change type oldala **[T1]**
(https://docs.liquibase.com/change-types/add-auto-increment.html):

> "DB2/LUW Supported No DB2/z Not Supported No Derby Not Supported No Firebird Not
> Supported No Google BigQuery Supported No H2 Supported No HyperSQL Supported No
> INGRES Supported No Informix Supported No MariaDB Supported No MySQL Supported No
> Oracle Not Supported No PostgreSQL Supported No Snowflake Not Supported No SQL
> Server Not Supported No SQLite Supported : If the column type is not INTEGER it is
> converted to INTEGER No Sybase Supported No Sybase Anywhere Supported No"

Ez azt jelenti: az `addAutoIncrement` **Oracle-ön, SQL Serveren, Snowflake-en, DB2/z-n,
Derbyn és Firebirdön hivatalosan NEM támogatott** — a Liquibase saját maga dokumentálja,
hogy itt az absztrakció megbicsaklik (Oracle-ön és SQL Serveren pl. az identitás-oszlop
létrehozása más deklaratív logikát igényel, amit a Liquibase nem told át transzparensen).

Összevetésképp a `sql` (nyers) change type táblája **minden** motorra "Supported"-et ír
— logikus, hiszen az maga a nyers SQL futtatása.

**Megállapítás:** a "hivatalos lista" tehát létezik, csak **elosztva, change
type-onként**, nem egy összesített mátrixban. Nem találtunk egyetlen, az összes change
type-ot és az összes motort keresztbe metsző hivatalos kompatibilitási táblázatot — ez
enyhe hiányosság a Liquibase dokumentációjában (l. `hianyok.md`).

### 1.3 A `dbms` attribútum: motor-NÉV szerinti, nem képesség szerinti elágazás

A `dbms` changelog-attribútum hivatalos leírása **[T1]**
(https://docs.liquibase.com/secure/reference-guide-5-1/changelog-attributes/dbms):

> "The dbms attribute is a string that specifies which database Liquibase should run a
> changeset on. dbms accepts "short names" of database management systems. Valid values
> include all, none, and the following values, which correspond with supported
> databases: ... mariadb maxdb mongodb mssql mysql neo4j oracle postgresql redshift
> snowflake sqlite sybase teradata vertica yugabytedb"

Ez egy explicit **motor-NÉV enumeráció** — nem "ha a motor támogatja a X
képességet", hanem "ha a motor neve Y". Ez éles kontraszt Django/Rails kapacitás-jelző
mintájával (l. 5. fejezet).

### 1.4 A nyers `sql`/`sqlFile` change type: mikor kell hozzányúlni?

A hivatalos doksi kifejezetten **eszkalációs útként** definiálja a nyers SQL change
type-ot **[T1]** (https://docs.liquibase.com/change-types/sql.html):

> "The sql Change Type is useful for complex changes that are not supported through
> Liquibase automated Change Types, such as stored procedures."

Vagyis a Liquibase saját dokumentációja mondja ki: **ott adja fel az absztrakciót, ahol
a change type-ok elfogynak** — tárolt eljárások, komplex logika esetén a felhasználónak
explicit nyers SQL-re kell váltania, amit a `dbms` attribútummal lehet motoronként
feltételessé tenni.

**Megbízhatóság:** mindhárom fenti idézet közvetlenül a docs.liquibase.com hivatalos
doksijából, nyers HTML-ből (`curl` a proxyn át) származik — kettős megerősítés: a
sql-changetype oldal és a changetype-home oldal egymástól függetlenül konzisztens
képet ad, és a Baeldung "List All Liquibase SQL Types" cikk (T3, nem lekérve, csak a
keresési találatok közt látott cím) közvetve megerősíti a `dbms`-alapú szűrés
gyakorlatát.

---

## 2. Flyway — az ellentétes filozófia

### 2.1 A core Flyway nem absztrahál — és ezt implicit módon teszi, nem kimondva

A Flyway (jelenlegi hivatalos doksi, documentation.red-gate.com, "Migrations",
utolsó frissítés: 2025.02.03) így írja le a migrációkat **[T1]**:

> "Migrations capture incremental changes to your development database. These are SQL
> scripts that can capture schema and data changes (eg., CREATE, ALTER, INSERT, UPDATE,
> etc.)."

A migrációk tehát **definíció szerint SQL-szkriptek**, nem egy motorfüggetlen leíró
nyelv. Ezt megerősíti egy korábbi (2018-as, web.archive.org-on át elért) flywaydb.org
doksi-oldal **[T1]**, amely explicit módon **elsőrangú funkcióként** sorolja fel a
motor-specifikus SQL-kiterjesztéseket:

> "Flyway supports all regular SQL syntax elements including: ... Database-specific SQL
> syntax extensions (PL/SQL, T-SQL, ...) typically used to define stored procedures,
> packages, ..."

**Nem találtunk** olyan mondatot a Flyway hivatalos dokumentációjában (sem a jelenlegi
documentation.red-gate.com-on, sem az archivált flywaydb.org-on), amely kimondottan azt
állítaná: "ne próbáld a migrációkat motorfüggetlenné tenni". A philozófia **hallgatólagos**
— a doksi egyszerűen sosem ígéri az absztrakciót, és a "Placeholder Replacement" funkciót
kifejezetten **környezetek közti** (dev/staging/prod névterek), nem **motorok közti**
különbségek áthidalására ajánlja:

> "In addition to regular SQL syntax, Flyway also supports placeholder replacement...
> This can be very useful to abstract differences between environments."

**Ez fontos megkülönböztetés a megbízás kérdésére válaszolva:** a Flyway "placeholder"
mechanizmusa **környezet-agnosztikus**, nem **motor-agnosztikus** — a két fogalmat a
Flyway doksi maga sem keveri össze, de nyíltan sem különíti el egy "miért nem vagyunk
motorfüggetlenek" szakaszban. **Ez hiányként rögzítve** (l. `hianyok.md`): nem találtunk
kimondott filozófiai állásfoglalást, csak a termék viselkedéséből visszafejthető
tervezési döntést.

### 2.2 A `{vendor}` mechanizmus: Spring Boot funkció, NEM Flyway-core

Kritikus, gyakran összekevert pont: a motoronkénti migrációs almappa-konvenció
(`db/migration/{vendor}`) **nem a Flyway saját funkciója**, hanem a **Spring Boot**
integrációs rétegéé. A hivatalos Spring Boot referencia doksi (docs.spring.io) így írja
le **[T1]**:

> "You can also add a special {vendor} placeholder to use vendor-specific scripts...
> Rather than using db/migration, the preceding configuration sets the directory to use
> according to the type of the database (such as db/migration/mysql for MySQL). The list
> of supported databases is available in DatabaseDriver."

Ezzel szemben a Flyway saját, motorfüggetlen `locations` beállítás-oldala
(documentation.red-gate.com) **semmilyen** `{vendor}`-szerű, beépített
motor-diszkrimináló szintaxist nem említ **[T1]**:

> "Array of locations to scan recursively for migrations. The location type is
> determined by its prefix." — majd csak `classpath:`, `filesystem:`, `s3:`, `gcs:`
> prefixeket sorol fel.

**Megállapítás:** a Flyway core filozófiája szerint **a fejlesztőnek magának kell
megszerveznie** a motoronkénti mappákat (pl. saját build-szkripttel vagy CI-lépéssel
választva a `locations` értékét), a Spring Boot pedig **erre a mintára rátett egy kényelmi
konvenciót**. Ez azt jelenti, hogy a "vendors mechanizmus" a megbízásban feltételezett
formában **nem Flyway-szintű, hanem keretrendszer-szintű döntés** — releváns adat a
mentes-frissites saját adapter-réteg tervezéséhez, mert pontosan ez a fajta "host
alkalmazás dönti el a mappát" minta az, amit érdemes lehet átvenni.

**Keresztellenőrzés:** a Spring Boot GitHub issue "Vendor specific flyway migrations not
working" (spring-projects/spring-boot #8281, T2, csak keresési találatként látva,
tartalma nem olvasva részletesen) közvetve megerősíti, hogy a `{vendor}` mechanizmus
gyakorlati használatában felhasználói zavart okoz — ami arra utal, hogy a
réteg-elkülönítés (Flyway vs. Spring Boot) a gyakorlatban sem mindig egyértelmű a
fejlesztők számára.

---

## 3. Drizzle ORM — dialektusok és a migrációk motorfüggősége

### 3.1 A dialektus-fogalom felépítése

A Drizzle ORM forráskódjában (github.com/drizzle-team/drizzle-orm,
`drizzle-orm/src/`) a dialektus **saját osztály motoronként**, nem egy közös
interfészt megvalósító, egyenrangú implementáció-halmaz **[T1]**:

- `drizzle-orm/src/pg-core/dialect.ts`: `export class PgDialect { ... }`
- `drizzle-orm/src/sqlite-core/dialect.ts`: `export abstract class SQLiteDialect { ... }`,
  amit két konkrét alosztály specializál tovább:
  `export class SQLiteSyncDialect extends SQLiteDialect` és
  `export class SQLiteAsyncDialect extends SQLiteDialect`.

Nem található közös, elvont `Dialect` bázisosztály vagy interfész a repóban
(`drizzle-orm/src/dialect.ts` nem létezik — 404-et adott a raw.githubusercontent.com-on).
Ez azt jelenti: a `sqlite-core`, `pg-core`, `mysql-core` **egymástól független modulok**,
amelyek saját típusrendszert, saját oszlop-builder API-t és saját SQL-generáló logikát
hordoznak — nincs egyetlen, mindhármuk fölé emelt absztrakt "Dialect" szerződés a
forráskód szintjén.

### 3.2 A migrációs fájlok dialektusonként generálódnak — nem motorfüggetlenek

A hivatalos Drizzle Kit doksi (orm.drizzle.team) egyértelművé teszi, hogy a
`drizzle.config.ts` **egyetlen, kötelező** `dialect` mezőt vár **[T1]**:

> `dialect: "postgresql", schema: "./src/schema.ts", out: "./drizzle",`

A `drizzle-kit generate` parancs pedig a séma **JSON-pillanatképéből** és az előző
migrációkkal vett **diffből** generál **konkrét, dialektus-specifikus SQL-t** **[T1]**
(https://orm.drizzle.team/docs/drizzle-kit-generate):

> "It will read through your Drizzle schema file(s) and compose a json snapshot of your
> schema... Based on json differences it will generate SQL migrations"

A generált `migration.sql` fájl expliciten Postgres-szintaxist tartalmaz a doksi saját
példájában (`SERIAL PRIMARY KEY`) — tehát a migrációs fájlok **nem** motorfüggetlenek:
egy adott projekt migrációs mappája egyetlen dialektushoz készül.

### 3.3 Mi történik motorváltáskor a meglévő migrációkkal? — HIVATALOS VÁLASZ NINCS

Végigolvastuk a Drizzle Kit teljes konfigurációs referenciáját és a `generate`/`migrate`
doksioldalakat: **egyik sem tárgyalja**, mi történik, ha egy projekt menet közben vált
dialektust (pl. `postgresql` → `mysql`). Ez egy **valódi, megnevezhető hiány** a Drizzle
hivatalos dokumentációjában (l. `hianyok.md`).

Amit találtunk helyette, egy **harmadik féltől** (MakerKit, egy kereskedelmi Next.js
SaaS-sablon dokumentációja, **T2**, https://makerkit.dev/docs/nextjs-drizzle/database/mysql)
származó, **gyakorlati** útmutató, amely kilenc lépésben írja le a Postgres→MySQL váltást,
és a 9. lépésben explicit **törli és újragenerálja** a teljes migrációs előzményt:

> "9. Regenerate migrations rm -rf packages/database/src/schema/meta rm
> packages/database/src/schema/*.sql pnpm --filter "@kit/database" drizzle:generate"

és a saját FAQ-jában is megerősíti a visszafordítás nehézségét:

> "Can I migrate back to PostgreSQL after switching to MySQL? This is possible but
> requires effort. You would need to reverse the adapter changes, regenerate the schema
> with PostgreSQL types, and migrate your production data."

**Megállapítás:** a Drizzle-ökoszisztémában elterjedt gyakorlati minta a **"nincs
konverzió, csak nulláról-generálás"** — de ezt **nem a Drizzle csapata**, hanem egy
független vendor dokumentálja. Ez azt sugallja, hogy a Drizzle tervezői egyszerűen nem
számítottak (vagy nem tartják elsődleges use case-nek) a dialektusváltásra egy élő
projektben — ami közvetlenül releváns a mentes-frissites saját portrétegének
tervezésénél: **ha a Drizzle-hez hasonló architektúrát választanak, a motorváltás nem
"migráció", hanem "újrakezdés" lesz**, hacsak a saját adapter-rétegük nem told be egy
saját konverziós lépést.

---

## 4. Django és Rails — az ORM-szintű séma-absztrakció tényleges határa

### 4.1 Django: `SchemaEditor` — a dokumentált interfész

A hivatalos Django doksi (docs.djangoproject.com, "SchemaEditor" oldal) explicit módon
nevezi meg a réteghatárt **[T1]**:

> "Django's migration system is split into two parts; the logic for calculating and
> storing what operations should be run (django.db.migrations), and the database
> abstraction layer that turns things like "create a model" or "delete a field" into SQL
> - which is the job of the SchemaEditor."

> "Each database backend in Django supplies its own version of SchemaEditor"

**Metódusszám:** a hivatalos doksi oldal **16 nyilvánosan dokumentált metódust** sorol
fel (`execute`, `create_model`, `delete_model`, `add_index`, `remove_index`,
`rename_index`, `add_constraint`, `remove_constraint`, `alter_unique_together`,
`alter_index_together`, `alter_db_table`, `alter_db_table_comment`,
`alter_db_tablespace`, `add_field`, `remove_field`, `alter_field`) — ez a **"publikus
szerződés"**, amit egy harmadik féltől származó backendnek biztosítania kell.

A tényleges forráskódban (`django/db/backends/base/schema.py`, letöltve
raw.githubusercontent.com-ról **[T1]**) a `BaseDatabaseSchemaEditor` osztály **80 db
`def` metódust** tartalmaz összesen — a különbség (80 vs. 16) a **belső, `_`-prefixű
segédmetódusokból** adódik (pl. `_alter_column_type_sql`, `_create_index_sql`,
`_constraint_names`), amelyeket a doksi nem old fel API-ként, csak a motoronkénti
alosztályok írnak felül belső logikaként. A PostgreSQL-, SQLite- és MySQL-specifikus
`DatabaseSchemaEditor` alosztályok rendre **18, 14 és 21 metódust** írnak felül/adnak
hozzá (forrás: `django/db/backends/{postgresql,sqlite3,mysql}/schema.py`) — vagyis a
"mennyit kell újraírni egy új motorhoz" válasz gyakorlatilag **"a 80-ból kb. 15-20
metódust, ha a motor viszonylag szabványos SQL-t beszél"**, amit a doksi maga is
megerősít:

> "If you are writing or maintaining a third-party database backend for Django, you
> will need to provide a SchemaEditor implementation in order to work with Django's
> migration functionality - however, as long as your database is relatively standard in
> its use of SQL and relational design, you should be able to subclass one of the
> built-in Django SchemaEditor classes and tweak the syntax a little."

### 4.2 Django: hol mondja ki explicit a határt?

Ugyanezen az oldalon, közvetlenül a fenti idézet előtt, a Django dokumentáció **saját
maga nevez meg egy konkrét, motor-specifikus törésvonalat** **[T1]**:

> "It exposes all possible operations as methods, that should be called in the order you
> wish changes to be applied. Some possible operations or types of change are not
> possible on all databases - for example, MyISAM does not support foreign key
> constraints."

Ez a Django hivatalos, dokumentált verziója a Liquibase "Database support" táblájának —
csak itt egy mondatba van sűrítve, nem egy exhausztív mátrixba.

### 4.3 Rails: `SchemaStatements` és az adapterek

A Rails ActiveRecord forráskódjában (`activerecord/lib/active_record/connection_adapters/`,
letöltve raw.githubusercontent.com-ról **[T1]**) a motorfüggetlen absztrakciós felület
a `ActiveRecord::ConnectionAdapters::SchemaStatements` modul, amely **78 db `def`
metódust** tartalmaz (`create_table`, `add_column`, `add_index`, `add_foreign_key`,
`add_check_constraint`, `change_column`, stb.) — ezt az **összes** konkrét adapter
(`PostgreSQLAdapter`, `Mysql2Adapter`, `SQLite3Adapter`) egyaránt örökli, és csak azokat
a részeket írja felül, ahol a motor SQL-dialektusa eltér.

**Nem találtunk** egy külön, Django-éhoz hasonló, önálló "íme az interfész, amit egy új
adapternek implementálnia kell" hivatalos doksioldalt a Rails Guides-on — a Rails
dokumentációja inkább a forráskód-kommenteken és a meglévő adapterek mintakódján
keresztül kommunikálja ezt, ami **gyengébb dokumentáltság**, mint a Django explicit
SchemaEditor-oldala (l. `hianyok.md`).

### 4.4 Konkrét motor-specifikus törésvonalak: részleges index és generált oszlop

Mindkét keretrendszer forráskódjában **pontosan** a megbízás által kiemelt két példát
találtuk meg, kódba öntve:

**Rails** (`abstract_adapter.rb`, alapértelmezés) **[T1]**:
```
def supports_partial_index?
  false
end
```
A `sqlite3_adapter.rb` **felülírja** `true`-ra (`def supports_partial_index? true end`
— a modern SQLite támogatja), az `abstract_mysql_adapter.rb` **nem írja felül**
(marad `false`, mert sem a MySQL, sem a MariaDB nem támogatja).

**Django** (`django/db/backends/mysql/features.py`) **[T1]**:
```python
# Neither MySQL nor MariaDB support partial indexes.
supports_partial_indexes = False
```
míg a bázis `django/db/backends/base/features.py`-ban `supports_partial_indexes = True`
az alapérték (amit PostgreSQL és SQLite öröklve tart).

Hasonlóan a **generált oszlopokra**: Django MySQL backend
`supports_stored_generated_columns = True` és `supports_virtual_generated_columns =
True`-t állít be, míg a bázisosztály mindkettőt `False`-ra állítja alapból — vagyis itt
épp fordítva, a MySQL a "gazdagabb" motor ezen a ponton, jó illusztrációja annak, hogy a
kapacitás-jelzők **nem egyetlen "legkisebb közös nevező" irányban** térnek el, hanem
motoronként változó mintázatban.

**Ez a három, egymástól teljesen független forrásból (Rails forráskód, Django forráskód,
GitLab hivatalos blogbejegyzés — l. 7. fejezet) függetlenül előkerülő "részleges index"
példa** az egyik legerősebb, leginkább megerősített ténymegállapítás ebben a
kutatásban.

---

## 5. A kapacitás-jelző (capability flag) minta migrációs eszközökben

**Igen, a minta megtalálható — és Django/Rails esetében szinte tankönyvi tisztasággal.**

### 5.1 Django: `BaseDatabaseFeatures`

A `django/db/backends/base/features.py` forráskódja **[T1]** egy `BaseDatabaseFeatures`
osztályt definiál, amely **~94 db** `supports_*` vagy `has_*` prefixű logikai
osztályattribútumot tartalmaz — néhány példa a fájlból:

```python
supports_nullable_unique_constraints = True
supports_partially_nullable_unique_constraints = True
supports_nulls_distinct_unique_constraints = False
supports_deferrable_unique_constraints = False
supports_foreign_keys = True
supports_column_check_constraints = True
supports_table_check_constraints = True
supports_tablespaces = False
```

A `django/db/backends/base/schema.py`-ban (a `BaseDatabaseSchemaEditor`
implementációjában) ezekre a jelzőkre **42 helyen** hivatkozik a kód `self.connection.
features.supports_...` formában — vagyis a schema-átalakító logika **döntően
kapacitásra, nem motor nevére kérdez**. Kivétel: néhány `if vendor == "postgresql"`
jellegű elágazás is előfordulhat komplexebb esetekben, de a domináns minta a
kapacitás-jelző.

### 5.2 Rails: `AbstractAdapter` `supports_*?` predikátumok

Az `activerecord/lib/active_record/connection_adapters/abstract_adapter.rb` **[T1]**
**40 db** `supports_*?` predikátum-metódust definiál (pl. `supports_partial_index?`,
`supports_check_constraints?`, `supports_foreign_keys?`, `supports_views?`,
`supports_json?`, `supports_common_table_expressions?`), amelyeket a konkrét adapterek
(PostgreSQL: 39 felülírás, SQLite3: 19 felülírás — a többi öröklődik) módosítanak. A
`schema_statements.rb`-ben ezekre a predikátumokra hivatkozva döntik el, pl., hogy egy
check constraint hozzáadható-e:

```ruby
return unless supports_check_constraints?
```

### 5.3 Kontraszt: Liquibase NÉV szerint ágazik el

Amint az 1.3 pontban idéztük, a Liquibase `dbms` attribútuma **motor-NÉV enumeráció**
(`mysql`, `postgresql`, `oracle`, ...), nem kapacitás-predikátum. **Ez direkt ellentmond**
a Django/Rails/SQLAlchemy mintának — l. részletesen `ellentmondasok.md`.

**Következtetés a mentes-frissites saját adapter-rétegére nézve:** a kutatás
megerősíti, hogy az iparágban két, jól megkülönböztethető, egyaránt elterjedt minta él
egymás mellett — (a) **ORM/séma-szerkesztő rétegek** (Django, Rails, és a korábban
vizsgált SQLAlchemy) a **kapacitás-jelző** mintát részesítik előnyben, (b) **deklaratív
changelog-alapú migrációs eszközök** (Liquibase) inkább **motor-név szerinti**
feltételezést használnak. A saját adapter-réteg tervezésekor érdemes tudatosan
választani a kettő közül — vagy hibrid megoldást építeni (névből kapacitás-halmazt
levezetve).

---

## 6. Adatfájl-formátum migrációja — a markdown/YAML fejléc esete

### 6.1 "Lazy migration on read" — dokumentált, megnevezhető rendszerek

**Jupyter nbformat** (`nbformat` Python csomag, hivatalos doksi, nbformat.readthedocs.io)
**[T1]** — a notebook fájl (`.ipynb`, JSON, YAML-frontmatterhez hasonló elven van
verziómezője: `nbformat`/`nbformat_minor`) olvasásakor a könyvtár **automatikusan**
konvertál:

> "The string can contain a notebook of any version. The notebook will be returned
> as_version, converting, if necessary."

> "This will automatically upgrade or downgrade notebooks in other versions of the
> notebook format to the structure your code knows about."

Ez a **legpontosabb dokumentált analógia** a "verziómező a fájlban + olvasáskori lusta
felfejlesztés" mintára — nem markdown, hanem JSON, de a mechanizmus (explicit
`nbformat`/`nbformat_minor` int mezők + `as_version` paraméterrel hívható
olvasó-konverter függvény) szerkezetileg azonos azzal, amit a megbízás leír.

**Kubernetes API szerver** (hivatalos doksi, kubernetes.io, "Storage Versions") **[T1]**
ugyanezt a mintát valósítja meg a saját erőforrás-tárolási rétegén:

> "Reads from the API Server will convert the stored data to the API representation of
> the object. This makes it so that old storage versions can sit indefinitely as long as
> no updates occur to the object. Writes, on the other hand, will convert the stored
> object to the new representation upon update."

Ez a **canonical, T1-es leírása** a lusta migrációnak: olvasáskor konvertál, írásig nem
kényszerít teljes átírást.

### 6.2 "Egyszeri tömeges átírás" — dokumentált, megnevezhető rendszerek

**Docusaurus** (hivatalos doksi, docusaurus.io, "Automated migration") **[T1]**: a
`@docusaurus/migrate` CLI egy **egyszeri**, a lemezen lévő fájlokat helyben felülíró
eszköz:

> "The migration CLI automatically migrates your v1 website to a v2 website."

> "The migration CLI updates existing files. Be sure to have committed them first!"

**Kubernetes `StorageVersionMigration`** (ugyanaz a doksioldal, mint 6.1) **[T1]**: a
lusta konverzió **kiegészítéseként** a Kubernetes explicit, egyszeri tömeges átírási
mechanizmust is kínál a régi tárolt verziók végleges felszámolására:

> "Option 1: Use Storage Version Migration Run Storage Version Migration for the custom
> resource."

**Fontos megállapítás:** a Kubernetes egyetlen rendszeren belül **mindkét mintát**
dokumentáltan kínálja — alapértelmezés a lusta, olvasás/írás-idejű konverzió, de amikor a
régi verziót véglegesen ki akarják vezetni, egy explicit, egyszeri tömeges migrációs
lépés is rendelkezésre áll. Ez jó modell lehet a mentes-frissites markdown-fejléc
kérdésére is: **lusta olvasás alapból + opcionális, explicit "tisztító" tömeges átírás
parancs**, amikor a csapat készen áll rá.

### 6.3 "Tolerant Reader" — a szerzőségi ellenőrzés eredménye

A martinfowler.com bliki-bejegyzés (**[T1]**, https://martinfowler.com/bliki/TolerantReader.html)
byline-ja egyértelműen **Martin Fowler**, dátuma **2011. május 9.**:

> "Martin Fowler" [byline], "9 May 2011" [dátum]

A cikk szövege maga is jelzi, hogy a **teljesebb, könyv-hosszúságú leírás** ezt
**követően** jelent meg máshol:

> "Since writing this bliki entry, Rob Daigneau published a full description of this
> pattern in Service Design Patterns"

**Eredmény: a "Tolerant Reader" elnevezés/minta Fowler saját szerzeménye — ez NEM téves
attribúció**, legalábbis a Fowler-bliki mint elsődleges, névvel ellátott közlés
tekintetében semmi nem utal arra, hogy más valaki korábban publikálta volna ugyanezt a
konkrét elnevezést hivatkozható formában (bár a mögöttes elv, a Postel-törvény, magától
Jon Posteltől származik, amit Fowler explicit idéz is a cikkben: *"be conservative in
what you do, be liberal in what you accept from others." -- Jon Postel*).

**A valódi tévesztési kockázat egy szomszédos mintánál van.** A "Tolerant Reader" cikk
végén Fowler saját maga hivatkozik egy "következő lépésként" a **Consumer-Driven
Contracts** mintára:

> "Some of you may recognize this as the next step to Consumer-Driven Contracts"

Ez a cikk (martinfowler.com/articles/consumerDrivenContracts.html, **[T1]**) **szintén
Fowler oldalán van közzétéve, de a byline egyértelműen más szerzőt nevez meg**:

> "12 June 2006 Ian Robinson Ian Robinson is a Principal Consultant with Thoughtworks."

**Ez pontosan az a fajta tévesztés, amire a megbízás figyelmeztetett**: mivel mindkét
cikk martinfowler.com-on van, és mindkettő ugyanabban a "szolgáltatás-evolúció"
témakörben mozog (Ian Robinson cikke maga is tárgyalja a "Schema Versioning" és
"Extension Points" — köztük a W3C TAG "Must Ignore" kiterjesztési mintáját —, amelyek
közvetlenül relevánsak a mentes-frissites saját kérdésére), könnyű a "Consumer-Driven
Contracts"-ot tévesen Fowlernek, vagy a "Tolerant Reader"-t tévesen Robinsonnak
tulajdonítani. **A helyes attribúció: Tolerant Reader = Fowler (2011); Consumer-Driven
Contracts = Ian Robinson (2006, Fowler oldalán publikálva).**

Kiegészítő, névvel ellátott minta ugyanebből az Ian Robinson-cikkből (**[T1]**,
"Schema Versioning" / "Extension Points" szekció): a **W3C TAG "Must Ignore"
kiterjesztési minta**, amit "David Orchard és Dare Obasanjo" papírjaira hivatkozva ír le
Robinson:

> "Making schemas both backwards- and forwards-compatible is a well-understood design
> task, best expressed by the Must Ignore pattern of extensibility (see the papers by
> David Orchard and Dare Obasanjo)."

Ez egy **negyedik, önállóan dokumentált, megnevezhető minta** a "tolerant reader"
családban — közvetlen elsődleges forrása a W3C TAG lenne, amit ez a kutatási kör
időkorlátok miatt nem ért el (l. `hianyok.md`).

---

## 7. Mikor NEM éri meg motorfüggetlen migrációt építeni?

### 7.1 A GitLab-eset: dokumentált, dátumozott, szerzővel ellátott döntés

A **GitLab hivatalos vállalati blogja** (about.gitlab.com, 2019.06.27, szerző: **Kenny
Johnston**) **[T1]** — ez pontosan az a fajta elsődleges forrás, amit a megbízás keresett
— explicit indokolja, miért szüntették meg a MySQL+PostgreSQL kettős motor-támogatást
(ezzel együtt a motorfüggetlen migrációs kódutakat is):

> "In most cases, it wasn't as simple as adding support to MySQL, but that by bending
> MySQL we typically broke PostgreSQL. To name a few limitations: We can't support
> nested groups with MySQL in a performant way ... MySQL doesn't support partial
> indexes"

> "In order to work around some of the pain points above, we ended [up] creating a lot
> of MySQL-specific code. In some cases this led to merge requests that were twice as
> complex because they had to support a second database backend. Creating and
> maintaining this code is a drain on our cycle time and velocity"

> "By providing support for both database backends (PostgreSQL and MySQL) we were unable
> to truly take advantage of either. Where we wanted to utilize specific performance and
> re[l]iability capabilities unique to a backend, we had to instead choose the lowest
> common denominator."

A blogposzt egy negyedik, adatalapú indokot is megad: a használati adatok szerint (GitLab
Usage Ping) a MySQL-t használó instance-ok száma (<1200) elhanyagolható volt a
PostgreSQL-t használókéhoz (110 000) képest — a kettős támogatás fenntartásának
költsége nem állt arányban a tényleges felhasználói igénnyel.

**Második, független forrás ugyanerre az esetre** — a tényleges kódváltoztatás MR-je
(**[T1]**, https://gitlab.com/gitlab-org/gitlab-foss/-/merge_requests/29790, "Only
support postgresql (minimal version)", Nick Thomas, 2019.06.18):

> "All the code is still mysql-compatible, but these changes will allow us to start
> adding postgresql-only code with confidence."

Ez a mondat pontosan azt a mozzanatot ragadja meg, amikor egy csapat **tudatosan
lemond** a motorfüggetlenség fenntartásáról, hogy kihasználhassa egy adott motor
specifikus képességeit — a "bizalommal" (*with confidence*) szó itt kulcsfontosságú: az
absztrakciós réteg fenntartása korábban **bizonytalanná** tette, hogy egy adott
kódrészlet biztonságosan használhat-e Postgres-specifikus funkciót.

### 7.2 Miért erős ez a forrás a megbízás szempontjából?

- **Elsődleges** (a döntést hozó cég saját, névvel ellátott közleménye, nem harmadik fél
  értelmezése).
- **Dátumozott és szerzővel ellátott** — ellenőrizhető, nem anonim fórumbejegyzés.
- **Konkrét technikai okot nevez meg** ("MySQL doesn't support partial indexes"), ami
  **szó szerint egybevág** a Django és Rails forráskódjában talált
  `supports_partial_indexes`/`supports_partial_index?` kapacitás-jelzőkkel — három
  független forrás, ugyanaz a konkrét jelenség.
- **Számszerű indokot is ad** (usage ping adatok), nem csak minőségi érvelést.

**Nem találtunk** ezen kívül más, hasonlóan tiszta, elsődleges, "megindokolt elhagyás"
esetet (pl. egy migrációs eszköz gyártójától, mint a Flyway vagy Liquibase, arról, hogy
*saját magának* a motorfüggetlen rétegét vonta volna vissza) — ez hiányként rögzítve.

---

## Módszertani megjegyzés (degradált mód)

Ez a kutatás **degradált, egyágensű módban** futott: a környezet nem biztosított
`Agent`/`Task`-jellegű eszközt párhuzamos Sonnet-alügynökök indítására, ezért a skill
tervezésének fő pillére (Sonnet-keresés és Opus-szintézis szétválasztása, egymástól
izolált munkameneteken) **nem valósult meg** — egyetlen munkamenet végezte mind a
keresést, mind az idézetek kiválasztását, mind a szintézist. Ezt a `00-plan.md` is
rögzíti. Kompenzációként:

- minden idézetet a nyers HTML/forráskód-letöltésből (`curl` a proxyn át) nyertünk ki,
  nem összefoglalóból;
- a `check_links.py` szkript az összes 31 forrás-URL-t automatikusan ellenőrizte
  (eredmény: mind a 31 **LIVE**);
- a `finalize.py` szkript a 21 rögzített állítás idézet-hűségét automatikusan
  ellenőrizte a mentett szövegekhez képest (eredmény: **21/21 pontos egyezés, 0
  hibás**);
- a **verifikációs lépést** (külön ügynök általi tartalmi ellenőrzés) **nem** egy
  második, izolált munkamenet végezte, hanem ugyanez a munkamenet, közvetlenül a
  forrásokból való kiemeléskor — ez gyengébb garancia, mint a skill által előírt
  kétlépcsős folyamat, és ezt a `report/QA.md` "verification coverage: 0%" sora is
  jelzi.
