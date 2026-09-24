# ELL03 — SQLite állítások ellenőrzése

**Módszertani megjegyzés.** Ez az ellenőrzés a `deep-web-research` skill **degradált** módjában készült: a futtató munkamenet nem ért el Agent/subagent-dispatch eszközt, ezért nem volt külön Sonnet-kereső hullám és külön Opus-szintézis — ezt a skill saját szabálya szerint itt rögzítem. Kompenzálásul minden állítást **közvetlenül letöltött, nyers HTML-ből** (`curl` a sqlite.org domainről) és a **hivatalos, csak-olvasható SQLite forráskód-tükörből** (`github.com/sqlite/sqlite`, amelyre maga a sqlite.org is hivatkozik forráskód-elérésként) ellenőriztem szövegkereséssel (`grep`/Python), nem összefoglaló-eszköz (pl. LLM-alapú lapfeldolgozó) kimenetéből. Ez kizárja az LLM-parafrázisból eredő idézet-pontatlanságot. Két állításnál (2c és 4b) a hivatalos próza-dokumentáció hallgat vagy csak közvetett, ezért a hivatalos SQLite forráskódot is bevontam (a `sqlite.org/src` fossil-webfelület robot-elhárítása miatt az `src/vacuum.c` és `src/shell.c.in` fájlokat a hivatalos GitHub-tükörről töltöttem le).

A teljes bizonyíték-vault (9 archivált forrás, 15 rögzített idézet, 100%-os idézet-egyezés) itt található: `/home/claude/work/kutatas-uzemeltetes/.research/ell03-sqlite/`.

---

## Ítélet

| # | Állítás | Ítélet |
|---|---|---|
| 1 | `quick_check` O(N), `integrity_check` O(N log N) | **IGAZOLVA** — szó szerint így áll a dokumentációban |
| 1b | A `quick_check` kihagyja a UNIQUE-ellenőrzést és az index/tábla-tartalom egyezés-ellenőrzést | **IGAZOLVA** |
| 2a | A `busy_timeout`-nak nincs számszerű hivatalos alapértéke | **IGAZOLVA** |
| 2b | Alapból nincs busy handler (NULL), ezért azonnal `SQLITE_BUSY` jön | **IGAZOLVA** |
| 2c | A `sqlite3` CLI-nek saját (nullától eltérő) alapértelmezett busy timeoutja van | **CÁFOLVA** — a forráskód szerint nincs ilyen |
| 3 | `wal_autocheckpoint` alapértéke 1000 oldal | **IGAZOLVA** — pragma.html és wal.html is megerősíti |
| 3b | 1000 oldal ≈ 4 MB (4096 bájtos lapmérettel) | **IGAZOLVA** — a dokumentáció maga mondja ki a "~4MB"-ot |
| 4 | A `VACUUM INTO` kimenete nem őrzi meg a forrás `journal_mode`-ját (delete módban jön létre) | **RÉSZBEN** — a dokumentáció explicit **hallgat** a `journal_mode`-ról; a forráskód és egy általános pragma-mondat közvetve alátámasztja a mérést |
| 4b | `page_size`, `auto_vacuum`, `user_version`, `application_id` öröklődik a VACUUM(INTO) kimenetére | **IGAZOLVA** — forráskód szerint (a dokumentáció csak a `page_size`/`auto_vacuum`-ot említi kifejezetten) |
| 5a | `VACUUM INTO` nem futtatható nyitott tranzakción belül | **IGAZOLVA** — forráskód + doksi együtt |
| 5b | Létező célfájlra hiba: *"output file already exists"* | **IGAZOLVA** — szó szerint ez a forráskódi hibaüzenet |
| 5c | Dokumentált-e, mi történik félbeszakadt `VACUUM INTO`-nál | **RÉSZBEN** — a "korrupt/hiányos" kimenet dokumentált, de a félkész fájl sorsáról (megmarad-e a lemezen) nincs explicit mondat |
| 6 | `VACUUM INTO` pillanatkép-szemantikája dokumentált | **IGAZOLVA** (röviden) |
| 6b | A dokumentáció a `VACUUM INTO`-nál éppúgy tárgyalja a párhuzamos írást, mint a `sqlite3_backup` API-nál | **CÁFOLVA** — a `backup.html` sokkal részletesebb, a `lang_vacuum.html` **hallgat** a párhuzamos írásról |
| 7 | `VACUUM INTO` kimenete nem tartalmazza a törölt tartalmat | **IGAZOLVA** — szó szerint "no forensic traces" |

---

## 1. `quick_check` vs `integrity_check` — O(N) vs O(N log N)

**URL:** https://www.sqlite.org/pragma.html#pragma_quick_check

**Szó szerinti idézet:**

> "The pragma is like integrity_check except that it does not verify UNIQUE constraints and does not verify that index content matches table content. By skipping UNIQUE and index consistency checks, quick_check is able to run faster. PRAGMA quick_check runs in O(N) time whereas PRAGMA integrity_check requires O(NlogN) time where N is the total number of rows in the database. Otherwise the two pragmas are the same."

**Ítélet: IGAZOLVA, szó szerint.** A vizsgált állítás pontosan megfelel a hivatalos szövegnek — nem kellett parafrazálni vagy közelítő megfogalmazást keresni.

**Mit hagy ki pontosan a `quick_check`?** A dokumentáció szerinti teljes felsorolás (két elem):
1. "it does not verify UNIQUE constraints"
2. "does not verify that index content matches table content"

Minden más tekintetben ("Otherwise the two pragmas are the same") a két PRAGMA azonos ellenőrzéseket végez.

---

## 2. `busy_timeout` alapértéke és a CLI saját alapértéke

### 2a–2b. C API és PRAGMA szintje

**URL:** https://www.sqlite.org/c3ref/busy_handler.html

**Szó szerinti idézet:**

> "If the busy callback is NULL, then SQLITE_BUSY is returned immediately upon encountering the lock. If the busy callback is not NULL, then the callback might be invoked with two arguments." […] "The default busy callback is NULL."

**URL:** https://www.sqlite.org/c3ref/busy_timeout.html

**Szó szerinti idézet:**

> "This routine sets a busy handler that sleeps for a specified amount of time when a table is locked. […] Calling this routine with an argument less than or equal to zero turns off all busy handlers."

Ez az oldal **nem** ad meg semmilyen numerikus alapértéket a busy timeout-hoz — csak a mechanizmust írja le.

**URL:** https://www.sqlite.org/pragma.html#pragma_busy_timeout

**Szó szerinti idézet (a teljes szakasz):**

> "Query or change the setting of the busy timeout. This pragma is an alternative to the sqlite3_busy_timeout() C-language interface which is made available as a pragma for use with language bindings that do not provide direct access to sqlite3_busy_timeout(). Each database connection can only have a single busy handler. This PRAGMA sets the busy handler for the process, possibly overwriting any previously set busy handler."

Ez a szakasz — más pragmákkal ellentétben (pl. `wal_autocheckpoint`, ahol kifejezetten szerepel "enabled by default with an interval of 1000") — **nem tartalmaz egyetlen számot sem** alapértékként. Ez pontosan alátámasztja az ellenőrizendő állítást: nincs számszerű hivatalos alapérték kimondva erre a pragmára, csak a viselkedés van leírva (NULL handler → azonnali `SQLITE_BUSY`).

A `busy_handler.html` külön dokumentálja a holtpont-elkerülési esetet is:

> "The presence of a busy handler does not guarantee that it will be invoked when there is lock contention. If SQLite determines that invoking the busy handler could result in a deadlock, it will go ahead and return SQLITE_BUSY to the application instead of invoking the busy handler."

**Ítélet: IGAZOLVA.** A `busy_timeout`-nak nincs dokumentált számszerű alapértéke; a busy handler alapból NULL, ezért zárolás esetén a hívás azonnal `SQLITE_BUSY`-t ad vissza — ez szó szerint így szerepel a hivatalos C API dokumentációban.

### 2c. Van-e a `sqlite3` CLI-nek saját alapértelmezett busy timeoutja?

A `cli.html` (https://www.sqlite.org/cli.html) csak ennyit mond a `.timeout` parancsról:

> ".timeout MS              Try opening locked tables for MS milliseconds"

— **nem ad meg semmilyen alapértéket**, és a dokumentáció egyáltalán nem tér ki arra, hogy a shell indításkor beállít-e valamilyen busy timeout-ot.

Mivel a hivatalos dokumentáció itt **hallgat**, a kérdést a hivatalos forráskódból (`github.com/sqlite/sqlite`, `src/shell.c.in`) ellenőriztem. A `sqlite3_busy_timeout()` C-függvénynek **egyetlen** hívása van a teljes shell forrásában, a `.timeout` meta-parancs kezelőjében:

```c
if( c=='t' && n>4 && cli_strncmp(azArg[0], "timeout", n)==0 ){
    open_db(p, 0);
    sqlite3_busy_timeout(p->db, nArg>=2 ? (int)integerValue(azArg[1]) : 0);
}else
```
— (`src/shell.c.in`, github.com/sqlite/sqlite, `master` ág, 13003–13005. sor)

A kapcsolatot megnyitó `open_db()` függvényben (5065. sortól) **nincs** `sqlite3_busy_timeout()` vagy `sqlite3_busy_handler()` hívás. Vagyis a shell indításkor, `.timeout` parancs nélkül, **nem** állít be saját busy timeout-ot — a könyvtár sima alapértéke (NULL handler, azonnali `SQLITE_BUSY`) érvényesül. Ha a felhasználó `.timeout` argumentum nélkül futtatja, az `0`-t ad át, ami — a `busy_timeout.html` szerint — "turns off all busy handlers", azaz kifejezetten kikapcsolja azt.

**Ítélet: CÁFOLVA (a gyakori félreértéssel szemben).** A hivatalos dokumentáció nem állít semmit erről explicit módon (sem "van", sem "nincs" — ezt ki kell mondani: **a dokumentáció hallgat róla**), de a hivatalos forráskód egyértelműen mutatja, hogy a `sqlite3` parancssori eszköznek **nincs** saját, nullától eltérő alapértelmezett busy timeoutja.

---

## 3. `wal_autocheckpoint` alapértéke — 1000 oldal / ~4 MB

**URL:** https://www.sqlite.org/wal.html#automatic_checkpoint (és a 6. "Avoiding Excessively Large WAL Files" szakasz)

**Szó szerinti idézetek:**

> "By default, SQLite will automatically checkpoint whenever a COMMIT occurs that causes the WAL file to be 1000 pages or more in size, or when the last database connection on a database file closes."

> "In normal cases, new content is appended to the WAL file until the WAL file accumulates about 1000 pages (and is thus about 4MB in size) at which point a checkpoint is automatically run and the WAL file is recycled."

**URL:** https://www.sqlite.org/pragma.html#pragma_wal_autocheckpoint

**Szó szerinti idézet:**

> "Autocheckpointing is enabled by default with an interval of 1000 or SQLITE_DEFAULT_WAL_AUTOCHECKPOINT."

**Bájtban, 4096 bájtos lapmérettel:** 1000 × 4096 bájt = 4 096 000 bájt (≈ 3,91 MiB). A `pragma.html#pragma_page_size` megerősíti, hogy 4096 bájt a lapméret alapértéke SQLite 3.12.0 (2016-03-29) óta:

> "beginning with SQLite version 3.12.0 (2016-03-29), the default page size increased to 4096."

A `wal.html` **saját maga mondja ki a konkrét MB-számot**: "about 1000 pages (and is thus about 4MB in size)" — tehát a dokumentáció nem hallgat erről, hanem kifejezetten megadja a kerekített 4 MB-os értéket (nem a pontos 4 096 000 bájtot, hanem "about 4MB"-ot).

**Ítélet: IGAZOLVA**, mind a wal.html, mind a pragma.html oldalon, szó szerint.

---

## 4. `VACUUM INTO` és a `journal_mode` öröklődése

**URL:** https://www.sqlite.org/lang_vacuum.html

A teljes oldalon (`grep`-pel ellenőrizve) a `journal_mode` kifejezés **egyszer sem fordul elő**. A dokumentáció **kifejezetten hallgat** arról, hogy a `VACUUM INTO` kimenete milyen naplózási módban jön létre.

Amit a dokumentáció **igen** kimond az öröklődő tulajdonságokról:

> "Normally, the database page_size and whether or not the database supports auto_vacuum must be configured before the database file is actually created. However, when not in write-ahead log mode, the page_size and/or auto_vacuum properties of an existing database may be changed by using the page_size and/or pragma auto_vacuum pragmas and then immediately VACUUMing the database."

Ez a mondat a `page_size`/`auto_vacuum` **beállítási mechanizmusáról** szól, nem kifejezetten a `VACUUM INTO` öröklődéséről. A pontos öröklődési listát a **forráskód** (`src/vacuum.c`, `sqlite3RunVacuum()`) adja meg egyértelműen:

```c
sqlite3BtreeSetPageSize(pTemp, sqlite3BtreeGetPageSize(pMain), nRes, 0)   /* page_size öröklődik */
...
sqlite3BtreeSetAutoVacuum(pTemp, db->nextAutovac>=0 ? db->nextAutovac :
                                         sqlite3BtreeGetAutoVacuum(pMain));  /* auto_vacuum öröklődik */
...
static const unsigned char aCopy[] = {
   BTREE_SCHEMA_VERSION,     1,  /* Add one to the old schema cookie */
   BTREE_DEFAULT_CACHE_SIZE, 0,  /* Preserve the default page cache size */
   BTREE_TEXT_ENCODING,      0,  /* Preserve the text encoding */
   BTREE_USER_VERSION,       0,  /* Preserve the user version */
   BTREE_APPLICATION_ID,     0,  /* Preserve the application id */
};
```
— (`src/vacuum.c`, github.com/sqlite/sqlite, kb. 281., 290. és 358–363. sor)

Vagyis a forráskód szerint **explicit módon öröklődik**: `page_size`, `auto_vacuum`, `user_version`, `application_id` (és a séma-verzió +1-gyel, valamint a szövegkódolás). A `journal_mode` **nem szerepel** ebben a listában, és sehol máshol a fájlban nincs olyan hívás, amely a `VACUUM INTO` célfájljának naplózási módját a forrás `journal_mode`-jára állítaná.

Ezt közvetve alátámasztja egy általános (nem VACUUM-specifikus) pragma-mondat is:

**URL:** https://www.sqlite.org/pragma.html#pragma_journal_mode

> "The DELETE journaling mode is the default."

Mivel a `VACUUM INTO` egy vadonatúj fájlt hoz létre (`ATTACH`-csal), és a forráskód nem állítja be rajta a `journal_mode`-ot a forrás alapján, az új fájl az általános SQLite-alapértelmezésen (DELETE) marad — ez **magyarázza**, de nem **mondja ki explicit módon** a mért jelenséget ("a mentés delete módban jön létre, nem WAL-ban").

**Ítélet: RÉSZBEN.** A `lang_vacuum.html` és a `pragma.html` egyaránt **hallgat** arról, hogy a `VACUUM INTO` kimenete milyen `journal_mode`-ban jön létre — ezt itt ki kell mondani, nem szabad logikával pótolni a hivatalos-forrás-idézetek helyén. A mért jelenség (delete mód, nem WAL) a forráskód elemzésével **magyarázható és konzisztens** (a `journal_mode` nincs az öröklődő tulajdonságok listáján, és az általános alapértelmezés DELETE), de ez forráskód-szintű következtetés, nem dokumentációs kijelentés.

---

## 5. `VACUUM INTO` tranzakció-tilalom, "output file already exists", félbeszakadás

### 5a. Nyitott tranzakción belüli tilalom

**URL:** https://www.sqlite.org/lang_vacuum.html

**Szó szerinti idézet:**

> "A VACUUM will fail if there is an open transaction on the database connection that is attempting to run the VACUUM. Unfinalized SQL statements typically hold a read transaction open, so the VACUUM might fail if there are unfinalized SQL statements on the same connection. VACUUM (but not VACUUM INTO) is a write operation and so if another database connection is holding a lock that prevents writes, then the VACUUM will fail."

Ez a bekezdés a `VACUUM`/`VACUUM INTO` közös leírásán belül van, közvetlenül azután, hogy a szöveg kifejezetten megkülönbözteti a kettőt ("VACUUM (but not VACUUM INTO) is a write operation…") — vagyis a nyitott tranzakcióra vonatkozó tiltás **nem** kap kivételt a `VACUUM INTO` számára, csak a másik kapcsolat write-lockjára vonatkozó rész.

Ezt a **forráskód egyértelműen megerősíti**: a tranzakció-ellenőrzés a `VACUUM INTO`-ági elágazás (`pOut`) **előtt** fut le, tehát mindkét formára vonatkozik:

```c
if( !db->autoCommit ){
    sqlite3SetString(pzErrMsg, db, "cannot VACUUM from within a transaction");
    return SQLITE_ERROR; /* IMP: R-12218-18073 */
}
```
— (`src/vacuum.c`, github.com/sqlite/sqlite, 169–171. sor, a `pOut` néven megkülönböztetett `VACUUM INTO`-ág előtt)

**Ítélet: IGAZOLVA**, dokumentáció + forráskód együtt.

### 5b. "output file already exists"

**URL:** https://www.sqlite.org/lang_vacuum.html

**Szó szerinti idézet (dokumentáció):**

> "The file named by the INTO clause must not previously exist, or else it must be an empty file, or the VACUUM INTO command will fail with an error."

A dokumentáció nem idézi szó szerint a hibaüzenet szövegét, csak a szabályt írja le. A **pontos hibaüzenet-string** a forráskódban van:

```c
if( id->pMethods!=0 && (sqlite3OsFileSize(id, &sz)!=SQLITE_OK || sz>0) ){
    rc = SQLITE_ERROR;
    sqlite3SetString(pzErrMsg, db, "output file already exists");
    goto end_of_vacuum;
}
```
— (`src/vacuum.c`, github.com/sqlite/sqlite, 236–241. sor)

**Ítélet: IGAZOLVA, szó szerint egyezik** ("output file already exists") — de a pontos szöveg forrása a **forráskód**, nem a lang_vacuum.html próza (az csak a szabályt írja le, az üzenetet nem idézi).

### 5c. Félbeszakadt `VACUUM INTO`

**URL:** https://www.sqlite.org/lang_vacuum.html

**Szó szerinti idézet:**

> "The VACUUM INTO command is transactional in the sense that the generated output database is a consistent snapshot of the original database. However, if the VACUUM INTO command is interrupted by an unplanned shutdown or power loss, then the generated output database might be incomplete and corrupt."

> "However, if the PRAGMA synchronous setting of the original database is NORMAL or FULL, then SQLite invokes fsync() or FileFlushBuffers() to sync the output database to disk after it has been written. This means that in these cases, a power failure or unplanned shutdown that occurs after the VACUUM INTO command has completed should not corrupt the database."

**Ítélet: RÉSZBEN.** A dokumentáció **nem hallgat teljesen** erről — kifejezetten kimondja, hogy megszakítás (áramkimaradás, tervezetlen leállás) esetén a kimeneti adatbázis **"incomplete and corrupt"** lehet. Amiről viszont **explicit módon hallgat**: hogy a félkész célfájl a lemezen **marad-e** (nincs törlés/cleanup lépés említve), vagy hogy a fájlrendszer szintjén milyen méretű/állapotú fájl marad vissza. Ez utóbbi kérdésre nincs szó szerinti válasz a dokumentációban — ezt itt ki kell mondani, nem szabad kikövetkeztetni.

---

## 6. `VACUUM INTO` pillanatkép-szemantikája vs. `sqlite3_backup` API

**URL:** https://www.sqlite.org/lang_vacuum.html

**Szó szerinti idézet (a `VACUUM INTO` teljes vonatkozó szövege):**

> "The VACUUM INTO command is transactional in the sense that the generated output database is a consistent snapshot of the original database."

Ez az **egyetlen** mondat a `lang_vacuum.html`-en, amely a pillanatkép-jelleget tárgyalja. A párhuzamos írásokról **semmi mást nem mond** ez az oldal — nincs benne olyan bekezdés, amely arról szólna, mi történik, ha egy másik kapcsolat a `VACUUM INTO` futása közben ír az adatbázisba.

**URL:** https://www.sqlite.org/backup.html (3.1. "File and Database Connection Locking")

**Szó szerinti idézet:**

> "During the 250 ms sleep in step 3 above, no read-lock is held on the database file and the mutex associated with pDb is not held. This allows other threads to use database connection pDb and other connections to write to the underlying database file."

> "If another thread or process writes to the source database while this function is sleeping, then SQLite detects this and usually restarts the backup process when sqlite3_backup_step() is next called. There is one exception to this rule: If the source database is not an in-memory database, and the write is performed from within the same process as the backup operation and uses the same database handle (pDb), then the destination database […] is automatically updated along with the source."

> "Whether or not the backup process is restarted as a result of writes to the source database mid-backup, the user can be sure that when the backup operation is completed the backup database contains a consistent and up-to-date snapshot of the original."

**Összehasonlítás:** A `backup.html` egy teljes alfejezetet (3.1.) szentel annak, hogy pontosan mi történik, ha másik kapcsolat ír a forrásba a mentés közben (újraindítás, kivétel ugyanazon kapcsolatra, teljesítmény-következmények, végtelen újraindítás kockázata). Ezzel szemben a `lang_vacuum.html` a `VACUUM INTO`-ra vonatkozóan **egyetlen, tömör mondatban** intézi el a pillanatkép-kérdést, és **nem tér ki** arra, mi történik párhuzamos írás esetén (újraindul-e a másolás, hibázik-e, vagy egyszerűen a `BEGIN`-kor rögzített olvasási pillanatképet másolja tovább — ez utóbbi a forráskódból [`sqlite3BtreeBeginTrans(pMain, pOut==0 ? 2 : 0, 0)`, azaz `VACUUM INTO`-nál sima olvasási tranzakció] következtethető ki, de a dokumentáció ezt nem mondja ki).

**Ítélet: IGAZOLVA a pillanatkép-állítás (röviden dokumentált), CÁFOLVA az az elvárás, hogy a két oldal hasonló mélységben tárgyalná a témát** — a `backup.html` explicit és részletes, a `lang_vacuum.html` erről a részről **hallgat**.

---

## 7. `VACUUM INTO` és a törölt tartalom / `secure_delete`

**URL:** https://www.sqlite.org/lang_vacuum.html

**Szó szerinti idézet:**

> "The advantage of using VACUUM INTO is that the resulting backup database is minimal in size and hence the amount of filesystem I/O may be reduced. Also, all deleted content is purged from the backup, leaving behind no forensic traces."

Ugyanez a lap, a `VACUUM` általános indoklásánál, még korábban:

> "Running VACUUM will clean the database of all traces of deleted content, thus preventing an adversary from recovering deleted content. Using VACUUM in this way is an alternative to setting PRAGMA secure_delete=ON."

**URL:** https://www.sqlite.org/pragma.html#pragma_secure_delete

**Szó szerinti idézet:**

> "When secure_delete is on, SQLite overwrites deleted content with zeros. […] Applications that wish to avoid leaving forensic traces after content is deleted or updated should enable the secure_delete pragma prior to performing the delete or update, or else run VACUUM after the delete or update."

**Ítélet: IGAZOLVA, szó szerint.** A hivatalos dokumentáció kifejezetten kimondja, hogy a `VACUUM INTO` kimenete **nem tartalmazza** a törölt tartalom maradványait ("no forensic traces"), és ezt egyenrangú alternatívaként állítja a `PRAGMA secure_delete=ON` mellé.

---

## Amit nem sikerült ellenőrizni

- **A "félkész célfájl megmarad-e a lemezen" kérdés (5c)** — a hivatalos dokumentáció nem tér ki erre explicit módon, és a forráskód gyors átvizsgálása sem talált egyértelmű "cleanup on error" lépést a `VACUUM INTO` hibaágán (a `goto end_of_vacuum` egy közös hibakezelő útra ugrik, amely nem törli explicit a részlegesen írt kimeneti fájlt) — ez utóbbi állítást azonban **nem tekintem véglegesen igazoltnak**, mert nem futtattam le a teljes hibakezelő ág lépésről lépésre történő nyomkövetését (pl. nem ellenőriztem, hogy az `ATTACH`-hoz tartozó `DETACH`/`sqlite3BtreeClose` valamilyen implicit törlést végez-e sikertelen `VACUUM INTO` esetén). Ez egy tisztán forráskód-alapú, nem dokumentált kérdés — a hivatalos próza-dokumentáció erről **hallgat**.
- **A `VACUUM INTO` konkrét viselkedése párhuzamos író esetén** (újraindul-e, hibázik-e, vagy csendben a régi pillanatképet másolja) — ezt a forráskód (`sqlite3BtreeBeginTrans` olvasási tranzakcióként) valószínűsíti, de **nincs hivatalos próza-dokumentáció**, amely ezt kimondaná; méréssel (pl. tényleges konkurens írás közbeni `VACUUM INTO` futtatásával) lehetett volna közvetlenül tesztelni, de ez az ellenőrzés a dokumentáció/forráskód-szintre korlátozódott, élő adatbázis-teszt nélkül.
- **`SQLITE_DEFAULT_WAL_AUTOCHECKPOINT` fordítás-idejű módosításának tényleges elterjedtsége** disztribúciónként (pl. Debian/Ubuntu csomagolt SQLite-ja módosítja-e) — ezt nem vizsgáltam, mert az eredeti állítás csak a hivatalos alapértékre kérdezett rá.
- Nem volt szükség T3 (StackOverflow stb.) forrásra egyik állításnál sem — minden kérdés megválaszolható volt elsődleges forrásból (sqlite.org dokumentáció vagy a hivatalos forráskód-tükör).

---

## Meglátogatott és felderített linkek

| Cím | URL | Tier | Lekérés módja | Megjegyzés |
|---|---|---|---|---|
| SQLite PRAGMA Statements | https://www.sqlite.org/pragma.html | T0 | `curl` (nyers HTML) | quick_check, integrity_check, busy_timeout, wal_autocheckpoint, page_size, journal_mode, secure_delete szakaszok |
| Write-Ahead Logging | https://www.sqlite.org/wal.html | T0 | `curl` (nyers HTML) | 3.1 Automatic Checkpoint és 6. Avoiding Excessively Large WAL Files szakaszok |
| VACUUM | https://www.sqlite.org/lang_vacuum.html | T0 | `curl` (nyers HTML) | Teljes oldal grep-elve journal_mode/page_size/auto_vacuum/transaction/snapshot kulcsszavakra |
| The Online Backup API | https://www.sqlite.org/backup.html | T0 | `curl` (nyers HTML) | 3.1 File and Database Connection Locking szakasz |
| sqlite3_busy_timeout (C API) | https://www.sqlite.org/c3ref/busy_timeout.html | T0 | `curl` (nyers HTML) | Nincs numerikus alapérték megadva |
| sqlite3_busy_handler (C API) | https://www.sqlite.org/c3ref/busy_handler.html | T0 | `curl` (nyers HTML) | "The default busy callback is NULL." |
| Command Line Shell For SQLite | https://www.sqlite.org/cli.html | T0 | `curl` (nyers HTML) | `.timeout` parancs leírása, nincs alapérték megadva |
| SQLite forráskód: `src/vacuum.c` | https://github.com/sqlite/sqlite/blob/master/src/vacuum.c | T0 | `curl` (raw.githubusercontent.com, hivatalos csak-olvasható git tükör) | "output file already exists", tranzakció-ellenőrzés, aCopy meta-lista (page_size/auto_vacuum/user_version/application_id öröklődés) |
| SQLite forráskód: `src/shell.c.in` | https://github.com/sqlite/sqlite/blob/master/src/shell.c.in | T0 | `curl` (raw.githubusercontent.com, hivatalos csak-olvasható git tükör) | Az egyetlen `sqlite3_busy_timeout()` hívás a `.timeout` meta-parancsban van, `open_db()`-ben nincs |
| SQLite hivatalos Fossil forráskód-böngésző (`sqlite.org/src`) | https://sqlite.org/src/finfo?name=src/shell.c.in | T0 | `curl` — **sikertelen**, robot-elhárító JS-kihívás | Ezért a GitHub-tükröt használtam helyette a forráskód-ellenőrzéshez |
| SQLite PRAGMA page_size | https://www.sqlite.org/pragma.html#pragma_page_size | T0 | ugyanaz a `pragma.html` letöltés | 4096 bájtos alapértelmezett lapméret (3.12.0 óta) igazolásához |
| SQLite PRAGMA journal_mode | https://www.sqlite.org/pragma.html#pragma_journal_mode | T0 | ugyanaz a `pragma.html` letöltés | "The DELETE journaling mode is the default." — közvetett bizonyíték a 4. állításhoz |

*(StackOverflow vagy egyéb T3 forrás egyik állítás ellenőrzéséhez sem volt szükséges — minden kérdésre elsődleges forrásból található válasz vagy explicit dokumentációs csend.)*
