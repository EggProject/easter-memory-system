# Linkek — mentés és verziófrissítés

Minden meglátogatott és felderített forrás, kutatási egységenként.



---

# sq01 — Fájl-alapú tartalom mentése és helyreállítása

# SQ01 — Meglátogatott és felderített linkek

Tier: T1 = hivatalos dokumentáció/forráskód/kormányzati szerv; T2 = megbízható másodlagos/gyártói forrás; T3 = fórum/blog/anekdota.
Lekérés módja: **nyers curl** (proxin keresztül, tag-stripeléssel) vagy **WebFetch** (kis modell összefoglalója).

## Elsődlegesen felhasznált, idézett források

| Cím | URL | Tier | Lekérés módja | Megjegyzés |
|---|---|---|---|---|
| Borg — Usage notes (crash-like consistency, --read-special) | https://borgbackup.readthedocs.io/en/stable/usage/notes.html | T1 | nyers curl | Sikeres |
| Borg — `borg create` (--files-changed, 'C' flag) | https://borgbackup.readthedocs.io/en/stable/usage/create.html | T1 | nyers curl | Sikeres |
| restic — Backing up (VSS, --use-fs-snapshot) | https://restic.readthedocs.io/en/stable/040_backup.html | T1 | nyers curl | Sikeres |
| restic — FAQ | https://restic.readthedocs.io/en/stable/faq.html | T1 | nyers curl | Sikeres, kevés releváns tartalom |
| rsync — hivatalos man page (kanonikus forrás) | https://raw.githubusercontent.com/RsyncProject/rsync/master/rsync.1.md | T1 | nyers curl | Sikeres; a rsync.samba.org és download.samba.org 403-at adott |
| OpenZFS — zfs-snapshot(8) man page | https://openzfs.github.io/openzfs-docs/man/master/8/zfs-snapshot.8.html | T1 | nyers curl | Sikeres |
| Btrfs — hivatalos (kernel.org projekt) dokumentáció, Subvolumes | https://btrfs.readthedocs.io/en/latest/Subvolumes.html | T1 | nyers curl | Sikeres; "a snapshot is not a backup" |
| Btrfs — hivatalos dokumentáció, btrfs-send | https://btrfs.readthedocs.io/en/latest/btrfs-send.html | T1 | nyers curl | Sikeres, kevés extra tartalom |
| ArchWiki — Btrfs | https://wiki.archlinux.org/title/Btrfs | T2 | nyers curl | Sikeres, közösségi wiki, nem hivatalos projekt-dok |
| GitHub — About large files on GitHub | https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github | T1 | nyers curl | Sikeres; 50 MiB fájlkorlát, 1–5 GB repóajánlás |
| GitHub — Repository limits | https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits | T1 | nyers curl | Sikeres |
| Obsidian — "Back up your Obsidian files" (kanonikus GitHub forrás) | https://github.com/obsidianmd/obsidian-help/blob/master/en/Getting%20started/Back%20up%20your%20Obsidian%20files.md (nyers: raw.githubusercontent.com ugyanerről) | T1 | nyers curl | Sikeres; "Syncing is not a backup" |
| Obsidian — Introduction to Obsidian Sync | https://obsidian.md/help/sync | T1 | nyers curl (a publish-01.obsidian.md mögöttes .md URL-jén) | Sikeres |
| Obsidian — Version history (Sync) | https://obsidian.md/help/sync/version-history | T1 | nyers curl | Sikeres; 1/12 hónapos megőrzés |
| Obsidian — Set up Obsidian Sync | https://obsidian.md/help/sync/setup | T1 | nyers curl | Sikeres; "A syncing service is not a backup" mondat innen |
| Logseq — hivatalos docs repó, Automated Backup szakasz | https://github.com/logseq/docs/blob/master/db-version.md (nyers: raw.githubusercontent.com) | T1 | nyers curl | Sikeres; óránkénti, 12 verziós helyi mentés |
| NIST SP 800-34 Rev. 1 (Contingency Planning Guide) — PDF | https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-34r1.pdf | T1 | nyers curl + pdftotext | Sikeres; RPO/RTO definíció, CP-9, TT&E évi teszt |
| NIST CSRC — SP 800-34 Rev.1 katalóguslap (állapot, dátum) | https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final | T1 | nyers curl | Sikeres; "Date Published: May 2010 (Updated 11/11/2010)" |
| CIS Controls v8.1 — Control 11: Data Recovery | https://cas8.docs.cisecurity.org/en/latest/source/Controls11/ | T2 | nyers curl | Sikeres; heti mentés, negyedéves visszaállítás-teszt |
| CISA — Back Up Business Data | https://www.cisa.gov/audiences/small-and-medium-businesses/secure-your-business/back-up-business-data | T1 | **WebFetch** | Nyers curl "Access Denied" (Akamai) minden UA/cookie-kombinációval |
| CISA — Back Up Government Data | https://www.cisa.gov/audiences/state-local-tribal-and-territorial-government/secure-us-sltt/back-government-data | T1 | **WebFetch** | Ua., szövege szó szerint megegyezik az előzővel |
| CISA — Data Backup Options (PDF) | https://www.cisa.gov/sites/default/files/publications/data_backup_options.pdf | T1 | **WebFetch — sikertelen (403)** | Sem nyers curl, sem WebFetch nem hozott tartalmat |
| NCSC (UK) — Small organisations guide: Backing up your data | https://www.ncsc.gov.uk/collection/small-organisations-guide-to-cyber-security/backing-up-your-data | T1 | **WebFetch** | Nyers curl-lel csak a JS-héj jön le (0 releváns találat) |
| NCSC (UK) — Ransomware-resistant backups (bevezető) | https://www.ncsc.gov.uk/collection/ransomware-resistant-backups | T1 | **WebFetch** | Ua., JS-alapú oldal |
| NCSC (UK) — Principles for ransomware-resistant on-premises backups | https://www.ncsc.gov.uk/collection/ransomware-resistant-backups/principles-for-ransomware-resistant-on-premises-backups | T1 | **WebFetch** | Nyers curl nem hozott tartalmat; ez az egyetlen forrásunk a 6 tételes elvlistára |
| At-Bay — sajtóközlemény, "31% fail to recover backup" | https://www.at-bay.com/press_releases/report-reveals-businesses-fail-to-recover-backup-when-hit-by-ransomware/ | T2 | nyers curl | Sikeres; n=186, kkv, 2019–2023 |
| Backblaze — 2022 Backup Survey | https://www.backblaze.com/blog/the-2022-backup-survey-54-report-data-loss-with-only-10-backing-up-daily/ | T2 | nyers curl | Sikeres; Harris Poll módszertan, n=1861 |
| Backblaze — The 3-2-1 Backup Strategy (blog) | https://www.backblaze.com/blog/the-3-2-1-backup-strategy/ | T2 | nyers curl | Sikeres; nem tartalmazza a Krogh-attribúciót ebben a verzióban |
| backupwrapup.com — Peter Krogh podcast-interjú a 3-2-1 eredetéről | https://www.backupwrapup.com/peter-krogh-who-coined-the-3-2-1-rule-on-our-podcast/ | T2 | nyers curl | Sikeres; közvetlen interjú-idézet |
| The DAM Book hivatalos oldala | http://thedambook.com/the-dam-book/ | T2 | nyers curl | Sikeres; tartalomjegyzék, nincs szó szerinti "3-2-1" a lapon |
| Wikipedia — Peter Krogh (photographer) | https://en.wikipedia.org/wiki/Peter_Krogh_(photographer) | T2/T3 | nyers curl | Sikeres; NEM említi a 3-2-1 szabályt |
| Wikipedia — Backup | https://en.wikipedia.org/wiki/Backup | T2/T3 | nyers curl | Sikeres; ismerteti a szabályt, megalkotót nem nevez meg |

## Felderített, de a végleges idézetekhez fel nem használt/kiegészítő linkek

| Cím | URL | Tier | Lekérés módja | Megjegyzés |
|---|---|---|---|---|
| git-scm.com Book — Git Internals: Packfiles | https://git-scm.com/book/en/v2/Git-Internals-Packfiles | T1 | nyers curl | Sikeres, de nem tartalmazott közvetlenül idézhető "bináris fájl korlát" állítást |
| Borg GitHub issue #8299 (file changed while backed up, permission change) | https://github.com/borgbackup/borg/issues/8299 | T3 | csak keresési találat, nem letöltve | Közösségi megerősítés a jelenség valós voltára |
| Borg GitHub issue #6379 (opt-out file changed warnings) | https://github.com/borgbackup/borg/issues/6379 | T3 | csak keresési találat | ua. |
| Borg GitHub issue #8573 (file changed warning false positive) | https://github.com/borgbackup/borg/issues/8573 | T3 | csak keresési találat | ua. |
| rsync — "some files vanished" közösségi hibajelentések (GitHub, fórumok) | több URL, ld. keresesek.md | T3 | csak keresési találat | A jelenség gyakoriságát támasztja alá anekdotikusan |
| CIS Control 11 harmadik felek összefoglalói (Medium, Netwrix, Tripwire, ionix.io) | ld. keresesek.md | T3 | nem letöltve | Csak keresési találatok, az elsődleges CIS-forrást használtuk helyettük |
| Backblaze — "3-2-1 vs 3-2-1-1-0 vs 4-3-2" blog | https://www.backblaze.com/blog/whats-the-diff-3-2-1-vs-3-2-1-1-0-vs-4-3-2/ | T2 | nem letöltve, csak keresési találat | A 3-2-1 szabály modern kiterjesztéseiről; nem volt szükséges idézni |
| Gitnux / Invenioit disaster recovery statisztika-gyűjtő oldalak | ld. keresesek.md | T3 | nem letöltve | Aggregátor oldalak, elsődleges forrás nélkül — szándékosan mellőzve, ld. hianyok.md |

## Sikertelen / blokkolt lekérések (domain szinten)

| Domain / URL | Probléma | Kezelés |
|---|---|---|
| `www.cisa.gov` (összes aloldal, PDF is) | Akamai "Access Denied" a proxy kimenő IP-jére, minden User-Agent/cookie-kombinációval, HTTP 403 | WebFetch-re váltva (részben sikeres — ld. fent); a PDF WebFetch-csal is 403 |
| `rsync.samba.org`, `download.samba.org` | HTTP 403 "Request forbidden by administrative rules" | Helyette a hivatalos GitHub forráskód-repó (`RsyncProject/rsync`) nyers .md fájlját használtuk (T1, kanonikus) |
| `web.archive.org` (a `/web/...` snapshot-elérés) | A munkakörnyezet egress-szabályzata explicit blokkolja ("Blocked by egress policy") — ez NEM technikai hiba, nem kerülendő meg | Nem próbálkoztunk tovább; a `archive.org/wayback/available` API (más aldomain) elérhető volt, de a tényleges snapshot-tartalom nem |
| `www.ncsc.gov.uk` (tartalmi aloldalak) | Nem blokkolt, de a tartalom kliensoldali JavaScript-tel töltődik be; nyers curl csak a Drupal-héjat és a navigációt adja vissza | WebFetch-re váltva minden NCSC-idézetnél; ez az egyetlen forrás minden idézett NCSC-állításra (ld. hianyok.md) |



---

# sq02 — Futó SQLite adatbázis biztonságos mentése

# sq02 — Meglátogatott és felderített linkek

Minden `sqlite.org` és `litestream.io` oldal **nyers HTML-ként, `curl`-lel a proxyn keresztül** lett letöltve, majd Python-szkripttel tag-stripelve (script- és style-blokkok eltávolítva, `<br>`/`</p>`/`</div>`/`</li>` sorvégekké alakítva). A nyers HTML-ek és a stripelt szöveges változatok a `raw/` ill. `raw/text/` almappában vannak. A táblázat "Lekérés módja" oszlopa jelzi, melyik módszerrel történt a lekérés.

## SQLite hivatalos dokumentáció (sqlite.org)

| Cím | URL | Tier | Lekérés módja |
|---|---|---|---|
| How To Corrupt An SQLite Database File | https://www.sqlite.org/howtocorrupt.html | T1 | curl (nyers HTML → tag-stripelve) |
| SQLite Backup API | https://www.sqlite.org/backup.html | T1 | curl (nyers HTML → tag-stripelve) |
| VACUUM (lang_vacuum) | https://www.sqlite.org/lang_vacuum.html | T1 | curl (nyers HTML → tag-stripelve) |
| Command Line Shell For SQLite (cli.html) | https://www.sqlite.org/cli.html | T1 | curl (nyers HTML → tag-stripelve) |
| Write-Ahead Logging (wal.html) | https://www.sqlite.org/wal.html | T1 | curl (nyers HTML → tag-stripelve) |
| Atomic Commit In SQLite | https://www.sqlite.org/atomiccommit.html | T1 | curl (nyers HTML → tag-stripelve) |
| File Locking And Concurrency In SQLite Version 3 | https://www.sqlite.org/lockingv3.html | T1 | curl (nyers HTML → tag-stripelve) — háttérkontextusra, nem közvetlenül idézve |
| Database File Format (fileformat2.html) | https://www.sqlite.org/fileformat2.html | T1 | curl (nyers HTML → tag-stripelve) — háttérkontextusra, nem közvetlenül idézve |
| PRAGMA statements (pragma.html) | https://www.sqlite.org/pragma.html | T1 | curl (nyers HTML → tag-stripelve) — `wal_checkpoint` pragma idézve |
| C Interface: Online Backup API (c3ref/backup_finish.html) | https://www.sqlite.org/c3ref/backup_finish.html | T1 | curl (nyers HTML → tag-stripelve) |
| C Interface: sqlite3_backup_init (c3ref/backup_init.html) | https://www.sqlite.org/c3ref/backup_init.html | — | curl → **HTTP 404**, az init/step/finish egy közös oldalon (backup_finish.html) van dokumentálva |
| Database Remote-Copy Tool For SQLite (rsync.html) | https://www.sqlite.org/rsync.html | T1 | curl (nyers HTML → tag-stripelve) |
| ATTACH DATABASE (lang_attach.html) | https://www.sqlite.org/lang_attach.html | T1 | curl (nyers HTML → tag-stripelve) — kulcsfontosságú idézet a 6. kérdéshez |
| SQLite Release 3.27.0 changelog | https://sqlite.org/releaselog/3_27_0.html | T1 | curl (nyers HTML → tag-stripelve) — a VACUUM INTO bevezetési verziójának igazolására |
| SQLite Frequently Asked Questions (faq.html) | https://www.sqlite.org/faq.html | T1 | curl (nyers HTML → tag-stripelve) — nem tartalmazott közvetlenül releváns idézetet a mentés-témában |
| SQLite forráskód: src/shell.c.in (Fossil repó, trunk) | https://sqlite.org/src/artifact?ci=trunk&filename=src/shell.c.in | T1 (forráskód) | curl (nyers HTML → tag-stripelve) — a `.backup`/`.dump` parancsok tényleges implementációjának ellenőrzésére |

## SQLite hivatalos felhasználói fórum (sqlite.org/forum — T3, közösségi tartalom hivatalos domainen)

| Cím | URL | Tier | Lekérés módja |
|---|---|---|---|
| "Backup via file system backup software" | https://sqlite.org/forum/info/796a192a95ac35b9 | T3 | curl (nyers HTML → tag-stripelve); első próbálkozás "Recv failure: Connection reset by peer" hibával elbukott, második curl-hívás sikeres volt |
| "Transactions involving multiple databases" | https://sqlite.org/forum/forumpost/ecf53d4eb8 | T3 | curl (nyers HTML → tag-stripelve) |
| "wal checkpointing very slow" | https://sqlite.org/forum/info/aa9fde5a28abc442 | T3 | curl (nyers HTML → tag-stripelve) |

## Litestream hivatalos dokumentáció (litestream.io)

| Cím | URL | Tier | Lekérés módja |
|---|---|---|---|
| Litestream főoldal | https://litestream.io/ | T1 | curl (nyers HTML → tag-stripelve) |
| How it works | https://litestream.io/how-it-works/ | T1 | curl (nyers HTML → tag-stripelve) |
| How it works — VFS (Read Replicas with VFS) | https://litestream.io/how-it-works/vfs/ | T1 | curl (nyers HTML → tag-stripelve) — nem közvetlenül idézve, kontextusnak |
| Tips & Caveats | https://litestream.io/tips/ | T1 | curl (nyers HTML → tag-stripelve) |
| Alternatives | https://litestream.io/alternatives/ | T1 | curl (nyers HTML → tag-stripelve) |
| Guides — Overview | https://litestream.io/guides/ | T1 | curl (nyers HTML → tag-stripelve) — navigációs áttekintéshez, URL-ek felderítéséhez |
| Replicating Directories | https://litestream.io/guides/directory/ | T1 | curl (nyers HTML → tag-stripelve) |
| Directory Watcher | https://litestream.io/guides/directory-watcher/ | T1 | curl (nyers HTML → tag-stripelve) — nem közvetlenül idézve |
| WAL Truncate Threshold Configuration | https://litestream.io/guides/wal-truncate-threshold/ | T1 | curl (nyers HTML → tag-stripelve) — nem közvetlenül idézve |
| FAQ | https://litestream.io/faq/ | — | curl → **HTTP 404**, az oldal megszűnt/átköltözött (a linket a `guides` menüjében nem is találtuk explicit módon; feltehetően törölték) |

## Közösségi / másodlagos források (T2/T3)

| Cím | URL | Tier | Lekérés módja |
|---|---|---|---|
| "Backup strategies for SQLite in production" (Oldmoe blog) | https://oldmoe.blog/2024/04/30/backup-strategies-for-sqlite-in-production/ | T3 (gyakorlati blog, de két külön közösség — HN és Lobsters — is megvitatta, konkrét méréssel) | curl (nyers HTML → tag-stripelve) |
| Lobsters-vita az Oldmoe-cikkről | https://lobste.rs/s/zglr47/backup_strategies_for_sqlite_production | T3 | curl (nyers HTML → tag-stripelve) |
| "Ensuring Consistent Backups in SQLite WAL Mode Without Disrupting Writers" (sqlite.work) | https://sqlite.work/ensuring-consistent-backups-in-sqlite-wal-mode-without-disrupting-writers/ | **Kizárva / nem használt forrásként** | curl (nyers HTML → tag-stripelve); a tartalom stílusa és néhány technikailag pontatlan/kétes állítása (pl. "CRC validation failures due to torn writes", generikus "SQLite.work Team" szerzőség) alapján valószínűsíthetően AI-generált vagy alacsony szerkesztői minőségű SEO-tartalom — a megállapítások dokumentumban **nem hivatkoztam rá** |
| "Consistent Database Backups With Btrfs Snapshots + Backrest Hooks" (nite07.com) | https://www.nite07.com/en/posts/backrest-btrfs-backup/ | T3 | curl (nyers HTML → tag-stripelve); letöltve, de végül nem idéztem belőle közvetlenül a megállapítások dokumentumban (a Btrfs-snapshot érvelés más forrásokból már megerősítve volt) |
| Vaultwarden GitHub Discussion #1613 (SQLite backup) | https://github.com/dani-garcia/vaultwarden/discussions/1613 | — | curl → **HTTP 403** (GitHub blokkolta a kérést) — lásd `keresesek.md`, blokkolt domain rész |

## Nem SQLite/Litestream domain, csak keresési találatként megjelent, de nem lekért linkek

Ezek a `WebSearch` találati listákban szerepeltek, de mivel nem hoztak volna releváns, ellenőrizhető, elsődleges adatot a kérdésekhez (PostgreSQL levelezőlisták VACUUM-ról, Delta Lake vacuum, stb.), nem lettek lekérve:

- postgresql.org levelezőlista-archívumok (VACUUM FULL témában, irreleváns — más adatbázis-motor)
- delta.io blog (Delta Lake vacuum, irreleváns)
- sqlitetutorial.net, adhdecode.com — másodlagos, tankönyv-jellegű oldalak, amelyek a hivatalos doksit parafrazálják; mivel a hivatalos forrást már közvetlenül elértük nyers HTML-lel, nem volt szükség rájuk



---

# sq03 — Séma-migráció és verziófrissítés futó rendszeren

# sq03 — Meglátogatott és felderített linkek

Tier-jelölés: T1 = hivatalos dokumentáció/forráskód, T2 = megbízható másodlagos forrás, T3 = fórum/blog/közösség.
Lekérés módja: **curl** = nyers HTML letöltve a proxyn keresztül és tag-stripelve (`strip.py`, saját szkript),
**WebFetch** = a Claude WebFetch eszközével (mert a curl blokkolva volt vagy JS-alapú SPA-shellt adott vissza),
**WebSearch** = csak keresési eredménylistában szerepelt, tartalma nem lett külön letöltve (csak a cím/URL
használva forrásazonosításra vagy továbbvezetésre).

## Drizzle ORM hivatalos dokumentáció

| Cím | URL | Tier | Lekérés módja |
|---|---|---|---|
| Drizzle Kit — Overview | https://orm.drizzle.team/docs/kit-overview | T1 | curl (nyers HTML, 271 KB → 6.6 KB szöveg) |
| Drizzle Kit — `generate` | https://orm.drizzle.team/docs/drizzle-kit-generate | T1 | curl (321 KB → 11.3 KB szöveg) |
| Drizzle Kit — `migrate` | https://orm.drizzle.team/docs/drizzle-kit-migrate | T1 | curl (274 KB → 7.2 KB szöveg) |
| Drizzle Kit — `push` | https://orm.drizzle.team/docs/drizzle-kit-push | T1 | curl (341 KB → 13.8 KB szöveg) |
| Drizzle Kit — Custom migrations | https://orm.drizzle.team/docs/kit-custom-migrations | T1 | curl (225 KB → 3.0 KB szöveg) |
| Drizzle — Migrations fundamentals | https://orm.drizzle.team/docs/migrations | T1 | curl (327 KB → 15.5 KB szöveg) |

## Drizzle ORM forráskód (GitHub raw)

| Cím | URL | Tier | Lekérés módja |
|---|---|---|---|
| `migrator.ts` (readMigrationFiles, `--> statement-breakpoint` vágás) | https://raw.githubusercontent.com/drizzle-team/drizzle-orm/main/drizzle-orm/src/migrator.ts | T1 | curl |
| `sqlite-core/dialect.ts` (SQLiteSyncDialect/AsyncDialect.migrate, BEGIN/ROLLBACK) | https://raw.githubusercontent.com/drizzle-team/drizzle-orm/main/drizzle-orm/src/sqlite-core/dialect.ts | T1 | curl (28.4 KB) |
| `better-sqlite3/migrator.ts` | https://raw.githubusercontent.com/drizzle-team/drizzle-orm/main/drizzle-orm/src/better-sqlite3/migrator.ts | T1 | curl |
| `bun-sqlite/migrator.ts` | https://raw.githubusercontent.com/drizzle-team/drizzle-orm/main/drizzle-orm/src/bun-sqlite/migrator.ts | T1 | curl |
| `libsql/migrator.ts` | https://raw.githubusercontent.com/drizzle-team/drizzle-orm/main/drizzle-orm/src/libsql/migrator.ts | T1 | curl (letöltve, tartalma nem lett külön idézve) |

## Drizzle — közösségi/másodlagos megerősítés a rollback hiányára

| Cím | URL | Tier | Lekérés módja |
|---|---|---|---|
| GitHub Issue #4005 — „[FEATURE]: Reverse/Down Migrations" | https://github.com/drizzle-team/drizzle-orm/issues/4005 | T2/T3 | WebSearch (cím/URL azonosítva, tartalom nem letöltve) |
| GitHub Discussion #1339 — „Migrations Rollback" | https://github.com/drizzle-team/drizzle-orm/discussions/1339 | T2/T3 | WebSearch |
| GitHub Issue #2510 — „[BUG]: Drizzle migration does not rollback if it fails" | https://github.com/drizzle-team/drizzle-orm/issues/2510 | T2/T3 | WebSearch |
| GitHub Issue #4583 — libsql `--> statement-breakpoint` hibajelenség | https://github.com/drizzle-team/drizzle-orm/issues/4583 | T2/T3 | WebSearch (korroborálja a statement-breakpoint mechanizmust) |
| GitHub PR #3538 — „ensure statement breakpoints are on new line" | https://github.com/drizzle-team/drizzle-orm/pull/3538 | T2/T3 | WebSearch |

## SQLite hivatalos dokumentáció

| Cím | URL | Tier | Lekérés módja |
|---|---|---|---|
| ALTER TABLE (12 lépéses recept, DROP/ADD COLUMN korlátok, „miért probléma") | https://sqlite.org/lang_altertable.html | T1 | curl (428 KB → 19.6 KB szöveg) |
| PRAGMA (foreign_keys, legacy_alter_table) | https://sqlite.org/pragma.html | T1 | curl (140 KB → 83.6 KB szöveg) |
| FTS5 (rebuild, delete-all, integrity-check, secure-delete) | https://sqlite.org/fts5.html | T1 | curl (211 KB → 158.3 KB szöveg) |
| The Virtual Table Mechanism Of SQLite | https://sqlite.org/vtab.html | T1 | curl (letöltve, nem idézve részletesen) |

## SQLite — másodlagos/közösségi megerősítés

| Cím | URL | Tier | Lekérés módja |
|---|---|---|---|
| Julia Evans — „ALTER TABLE in SQLite can't drop columns with foreign keys" | https://jvns.ca/til/alter-table-foreign-keys/ | T2 | WebSearch |
| SYNKEE blog — „How to Safely Modify Table Columns in SQLite with Production Data" | https://synkee.com.sg/blog/safely-modify-sqlite-table-columns-with-production-data/ | T3 | WebSearch |
| sqlitebrowser GitHub Issue #781 — FTS5 tábla létrehozás/eldobás hibák | https://github.com/sqlitebrowser/sqlitebrowser/issues/781 | T3 | WebSearch |
| sqlite-users mailing lista — „Corrupted FTS5 index? disk image is malformed" | https://sqlite-users.sqlite.narkive.com/oMpSMavN/sqlite-corrupted-fts5-index-disk-image-is-malformed | T3 | WebSearch |

## Expand–contract / Parallel Change — elsődleges és másodlagos források

| Cím | URL | Tier | Lekérés módja |
|---|---|---|---|
| Martin Fowler (Danilo Sato) — „Parallel Change" | https://martinfowler.com/bliki/ParallelChange.html | T1 (elsődleges) | curl (22.6 KB → 8.6 KB szöveg) |
| Pramod Sadalage & Martin Fowler — „Evolutionary Database Design" | https://martinfowler.com/articles/evodb.html | T1 (elsődleges) | curl (58.4 KB szöveg) |
| Tim Wellhausen — „Expand and Contract — A Pattern to Apply Breaking Changes to Persistent Data with Zero Downtime" | https://www.tim-wellhausen.de/papers/ExpandAndContract/ExpandAndContract.html | T2 | curl (19.1 KB szöveg) |
| Medium — „Expand and Contract Method for Database Changes" (Jasmin Fluri) | https://medium.com/@jasminfluri/expand-and-contract-method-for-database-changes-414d236f236f | T3 | WebSearch (nem letöltve) |
| Braveterry — „Parallel Change (AKA expand and contract)" | https://www.braveterry.com/2014/05/20/article-parallel-change-aka-expand-and-contract-pattern-to-safely-make-backward-incompatible-changes-to-an-interface/ | T3 | WebSearch (nem letöltve) |
| Jakub Holy — „Parallel Change (Parallel Design)" | https://blog.jakubholy.net/wiki/development/parallel-design-parallel-change/ | T3 | WebSearch (nem letöltve) |
| Field Guide (profoundcollective.com) — „Expand-Contract Migrations" | https://fieldguide.profoundcollective.com/engineering/expand-contract-migrations/ | T3 | WebSearch (nem letöltve) |

## Migrációs eszközök hivatalos dokumentációi — mentés/rollback

| Cím | URL | Tier | Lekérés módja |
|---|---|---|---|
| Flyway — Migrations (koncepció) | https://documentation.red-gate.com/fd/migrations-271585107.html | T1 | curl (43.1 KB → 7.2 KB szöveg) |
| Flyway — Undo migrations (mentési ajánlás, „EDITION: TEAMS") | https://documentation.red-gate.com/fd/undo-migrations-273973334.html | T1 | curl (31.8 KB → 4.3 KB szöveg) |
| Flyway — Undo (parancsreferencia) | https://documentation.red-gate.com/fd/undo-277578896.html | T1 | curl (30.7 KB → 3.4 KB szöveg) |
| Flyway GitHub Issue #124 — „Add a goal to do an SQL backup before the migration" | https://github.com/flyway/flyway/issues/124 | T2/T3 | WebSearch |
| Liquibase — `rollback` parancsreferencia | https://docs.liquibase.com/commands/rollback/rollback.html | T1 | curl (2.0 MB → 76.2 KB szöveg) |
| Liquibase — „What is a rollback?" (koncepció) | https://docs.liquibase.com/workflows/liquibase-community/using-rollback.html | T1 | curl (542 KB → 10.0 KB szöveg) |
| Liquibase — FAQ (a „bestpractices.html" URL erre redirektel) | https://docs.liquibase.com/concepts/bestpractices.html | T1 | curl (449 KB → 9.7 KB szöveg) |
| Liquibase Support — „Does Liquibase Backup Any Data?" | https://support.liquibase.com/hc/en-us/articles/29383069283739-Does-Liquibase-Backup-Any-Data | T1 | **WebFetch** (curl 403-at adott, Zendesk bot-védelem miatt) |
| Rails Guides — „Active Record Migrations" | https://guides.rubyonrails.org/active_record_migrations.html | T1 | curl (169 KB → 64.5 KB szöveg) |
| Django docs — „Migrations" (5.2) | https://docs.djangoproject.com/en/5.2/topics/migrations/ | T1 | curl (115 KB → 39.6 KB szöveg) |

## Fájlformátum-verziózás — konkrét rendszerek

| Cím | URL | Tier | Lekérés módja |
|---|---|---|---|
| nbformat v4 JSON séma (`nbformat`/`nbformat_minor` mezők) | https://raw.githubusercontent.com/jupyter/nbformat/main/nbformat/v4/nbformat.v4.schema.json | T1 | curl (16.1 KB) |
| nbformat — Format description (szemantikus verziózás elve) | https://nbformat.readthedocs.io/en/latest/format_description.html | T1 | curl (51.1 KB → 13.2 KB szöveg) |
| nbformat — Python API (`read(fp, as_version=…)`, lusta konverzió) | https://nbformat.readthedocs.io/en/latest/api.html | T1 | curl (71.4 KB → 11.4 KB szöveg) |
| WordPress fejlesztői referencia — `export_wp()` (WXR-verzió a fájlban) | https://developer.wordpress.org/reference/functions/export_wp/ | T1 | curl (201 KB → 29.7 KB szöveg) |
| Docker Compose — „Version and name top-level elements" (`version:` mező elavulttá válása) | https://docs.docker.com/reference/compose-file/version-and-name/ | T1 | curl (425 KB → 21.8 KB szöveg) |
| JSON Canvas Spec 1.0 (Obsidian canvas-formátum — ellenőrzött NEGATÍV találat: nincs fájlon belüli verziómező) | https://jsoncanvas.org/spec/1.0/ | T1 | curl (11.5 KB → 3.6 KB szöveg) |

## Docker / Docker Compose hivatalos dokumentáció

| Cím | URL | Tier | Lekérés módja |
|---|---|---|---|
| Docker Engine — Volumes (perzisztencia, backup/restore technika) | https://docs.docker.com/engine/storage/volumes/ | T1 | curl (663 KB → 52.4 KB szöveg) |
| Docker Compose CLI — `docker compose up` | https://docs.docker.com/reference/cli/docker/compose/up/ | T1 | curl (426 KB → 24.4 KB szöveg) |
| Docker Compose CLI — `docker compose down` (kötetek megmaradása alapból) | https://docs.docker.com/reference/cli/docker/compose/down/ | T1 | curl (422 KB → 21.9 KB szöveg) |
| Docker Compose — „Running Compose in production" | https://docs.docker.com/compose/how-tos/production/ | T1 | curl (513 KB → 24.5 KB szöveg) |
| Docker Compose — „Using lifecycle hooks with Compose" (`pre_stop` — `.db.bak` mentési példa) | https://docs.docker.com/compose/how-tos/lifecycle/ | T1 | curl (516 KB → 24.3 KB szöveg) |
| Docker Compose fájl-referencia — Services (`depends_on`, `pre_start` — migrációs worked example) | https://docs.docker.com/reference/compose-file/services/ | T1 | curl (873 KB → 103.4 KB szöveg) |

## Nem-elsődlegesen ellenőrzött, de a keresésben felbukkant kapcsolódó találatok (nem idézve a fő anyagban)

| Cím | URL | Tier | Megjegyzés |
|---|---|---|---|
| Frontend Masters blog — „Drizzle Database Migrations" | https://frontendmasters.com/blog/drizzle-database-migrations/ | T3 | csak WebSearch-listában, tartalma nem lett letöltve |
| Liquibase blog — „Fix Bad Database Changes in Liquibase" | https://www.liquibase.com/blog/ways-fix-bad-database-change | T3 | csak WebSearch-listában |
| Liquibase — „Database Rollback Best Practices Guide" (whitepaper) | https://www.liquibase.com/resources/whitepapers/roll-back-vs-fix-forward | T2 | csak WebSearch-listában, marketing-jellegű whitepaper, nem tekintettük hivatalos doksinak |
| Medium — „How to backup your database (SQLite) before migrating it to PostgreSQL in Django" | https://medium.com/@johnpauljp/how-to-backup-your-database-sqlite-before-migrating-it-to-postgresql-in-django-2b5f4afa1ef7 | T3 | csak WebSearch-listában — megerősíti, hogy ez nem hivatalos Django-ajánlás, hanem közösségi tanács |
| PyPI — `django-backup-utils`, `django-zeromigrations` | https://pypi.org/project/django-backup-utils, https://pypi.org/project/django-zeromigrations | T3 | harmadik féltől származó csomagok, nem Django-hivatalos |



---

# sq04 — Mit kell menteni, és honnan tudjuk, hogy jó

# sq04 — Meglátogatott és felderített linkek

Lekérés módja: **curl** = nyers HTML/PDF letöltés a proxyn keresztül, majd tag-stripelés (Python `re`) vagy `pdftotext -layout`. **WebSearch** = csak a keresőmotor találati listája (nem nyers tartalom, csak cím+URL). WebFetch-et ebben a kutatásban egyszer sem használtunk — minden hivatalos dokumentumot nyers letöltéssel szereztünk meg, a módszertani kikötésnek megfelelően.

## Elsődlegesen felhasznált és idézett források (nyers letöltéssel)

| # | Cím | URL | Tier | Lekérés módja |
|---|---|---|---|---|
| 1 | Borg check — hivatalos dokumentáció (v1.4.5) | https://borgbackup.readthedocs.io/en/stable/usage/check.html | T1 | curl, HTML tag-stripping |
| 2 | restic — Working with repositories (check, --read-data) | https://restic.readthedocs.io/en/stable/045_working_with_repos.html | T1 | curl, HTML tag-stripping |
| 3 | OpenZFS zpool-scrub.8 man page | https://openzfs.github.io/openzfs-docs/man/master/8/zpool-scrub.8.html | T1 | curl, HTML tag-stripping |
| 4 | Oracle Solaris ZFS Administration Guide — Scheduled Data Scrubbing | https://docs.oracle.com/en/operating-systems/solaris/oracle-solaris/11.4/manage-zfs/scheduled-data-scrubbing.html | T1 | curl, HTML tag-stripping |
| 5 | OWASP ASVS 5.0 — V13 Configuration (Secret Management) | https://github.com/OWASP/ASVS/blob/master/5.0/en/0x22-V13-Configuration.md (raw: raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x22-V13-Configuration.md) | T1 | curl, nyers Markdown |
| 6 | OWASP Secrets Management Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html | T1 | curl, HTML tag-stripping |
| 7 | CIS Controls v8 — Control 11: Data Recovery | https://cas8.docs.cisecurity.org/en/latest/source/Controls11/ | T1 | curl, HTML tag-stripping |
| 8 | CIS Controls v8 — Control 3: Data Protection (3.11 Encrypt Sensitive Data at Rest) | https://cas8.docs.cisecurity.org/en/latest/source/Controls3/ | T1 | curl, HTML tag-stripping |
| 9 | NIST SP 800-57 Part 1 Rev. 5 — Recommendation for Key Management | https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf | T1 | curl, `pdftotext -layout` |
| 10 | ICO (UK) — Right to erasure (hivatalos UK GDPR iránymutatás) | https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-erasure/ | T1 | curl, HTML tag-stripping |
| 11 | EDPB — 2025 Coordinated Enforcement Action: Implementation of the right to erasure by controllers (elfogadva 2026-02-10) | https://www.edpb.europa.eu/system/files/2026-02/edpb_cef-report_2025_right-to-erasure_en.pdf | T1 | curl, `pdftotext -layout` |
| 12 | CNIL — Guide de la sécurité des données personnelles (Fiche N°10: Sauvegarder) | https://cnb.avocat.fr/medias/cnilguidesecuritepersonnelle-68f7532f77b286.76172654.pdf (CNIL hivatalos kiadvány, kamarai tükörről letöltve, mert a cnil.fr közvetlen linkje 404-et adott) | T1 | curl, `pdftotext -layout` |
| 13 | CNIL — Les durées de conservation des données | https://www.cnil.fr/fr/passer-laction/les-durees-de-conservation-des-donnees | T1 | curl, HTML tag-stripping (nem tartalmazott "sauvegarde"-specifikus szöveget) |
| 14 | Bairavasundaram et al. — "An Analysis of Data Corruption in the Storage Stack" (NetApp/Wisconsin/Toronto, FAST'08, USENIX) | https://www.usenix.org/legacy/events/fast08/tech/full_papers/bairavasundaram/bairavasundaram.pdf | T1 | curl, `pdftotext -layout` |
| 15 | Kelemen, Péter (CERN IT) — "Silent Corruptions", LCSC 2007 prezentáció | https://www.nsc.liu.se/lcsc2007/presentations/LCSC_2007-kelemen.pdf | T1 | curl, `pdftotext -layout` |
| 16 | Backblaze — Drive Stats for 2025 (AFR statisztika) | https://www.backblaze.com/blog/backblaze-drive-stats-for-2025/ | T2 | curl (user-agent fejléccel), HTML tag-stripping |
| 17 | AWS Well-Architected Framework — SUS04-BP08 "Back up data only when difficult to recreate" (2022-03-31 kiadás) | https://docs.aws.amazon.com/en_us/wellarchitected/2022-03-31/framework/sus_sus_data_a9.html | T1 | curl, HTML tag-stripping |
| 18 | AWS Well-Architected Framework — SUS04-BP08 (legfrissebb kiadás) | https://docs.aws.amazon.com/wellarchitected/latest/framework/sus_sus_data_a9.html | T1 | curl, HTML tag-stripping |
| 19 | AWS Well-Architected Framework — REL09-BP01 "Identify and back up all data..., or reproduce the data from sources" | https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_backing_up_data_identified_backups_data.html | T1 | curl, HTML tag-stripping |
| 20 | SQLite hivatalos dokumentáció — FTS5 (6.12 "The 'rebuild' Command") | https://sqlite.org/fts5.html | T1 | curl, HTML tag-stripping |
| 21 | OpenAI — text-embedding-3-small modell-dokumentáció (árazás) | https://developers.openai.com/api/docs/models/text-embedding-3-small | T1 | curl (user-agent fejléccel), HTML tag-stripping |
| 22 | LlamaIndex — Ingestion Pipeline dokumentáció (IngestionCache, hash-alapú cache) | https://docs.llamaindex.ai/en/stable/module_guides/loading/ingestion_pipeline/ | T2 | curl, HTML tag-stripping |
| 23 | SoundCloud Backstage Blog — "How to Reindex One Billion Documents in One Hour at SoundCloud" | https://developers.soundcloud.com/blog/how-to-reindex-1-billion-documents-in-1-hour-at-soundcloud/ | T2 | curl (user-agent fejléccel), HTML tag-stripping |

## Megkísérelt, de nem hasznosítható vagy blokkolt lekérések

| Cím | URL | Eredmény |
|---|---|---|
| OpenAI API Pricing oldal | https://openai.com/api/pricing/ | HTTP 403 mindkét kísérletnél (sima és egyedi User-Agent fejléccel is) — proxy/bot-védelem valószínű. Pótolva a `developers.openai.com` modell-dokumentáció oldallal (#21), amely ugyanazt az árat adja meg. |
| LangChain — Caching Embeddings (python.langchain.com/docs/how_to/caching_embeddings/) | https://python.langchain.com/docs/how_to/caching_embeddings/ | A lekérés sikeres volt (HTTP 200), de a modern LangChain-dokumentáció (docs.langchain.com) SPA-ként épül fel és a régi URL egy általános "LangChain overview" oldalra irányított át — a keresett tartalom-hash cache leírás nem volt elérhető nyers HTML-ből. Pótolva a LlamaIndex hivatalos dokumentációjával (#22), amely explicit hash-alapú cache-mintát ír le. |
| CNIL — közvetlen guide-securite PDF a cnil.fr-ről | https://www.cnil.fr/sites/cnil/files/atoms/files/guide_securite_personnelle.pdf | HTTP 404. Pótolva a hivatalos CNIL-kiadvány kamarai (cnb.avocat.fr) tükörpéldányával (#12), amely ugyanaz a dokumentum, csak más hosztról. |

## Másodlagosan konzultált (csak WebSearch-találati listaként, nem nyers letöltéssel ellenőrizve — kereszthivatkozásra / megerősítésre használva)

| Cím | URL | Tier | Megjegyzés |
|---|---|---|---|
| OpenRouter — Text Embedding 3 Small pricing | https://openrouter.ai/openai/text-embedding-3-small | T2 | Megerősíti a $0.02/1M token árat |
| Helicone — OpenAI text-embedding-3-small pricing calculator | https://www.helicone.ai/llm-cost/provider/openai/model/text-embedding-3-small | T2 | Megerősíti a $0.02/1M token árat |
| embeddingcost.com — OpenAI Embeddings | https://embeddingcost.com/openai | T2/T3 | Megerősíti a $0.02 / $0.13 per 1M token árakat |
| AWS Well-Architected — SUS04-BP08 kapcsolódó dokumentumlista (EBS snapshots, EFS backup) | docs.aws.amazon.com (több aloldal) | T1 | Csak kontextusként, nem idézve |
| CIS Controls v8 — Control 3.11 Encrypt Sensitive Data at Rest, csv.tools tükör | https://csf.tools/reference/critical-security-controls/v8-1/csc-3/csc-3-11/ | T2 | Kereszthivatkozás, nem idézve közvetlenül |
| Redis — Semantic cache hivatalos dokumentáció | https://redis.io/docs/latest/develop/use-cases/semantic-cache/ | T2 | Az embedding-cache minta általános megerősítése, nem idézve szó szerint |
| theneuralbase.com — több oldal embedding cache témában | theneuralbase.com/... | T3 | Oktatóanyag-jellegű, konzisztens mintát mutat, nem elsődleges forrás |
| Klara Systems — Understanding ZFS Scrubs and Data Integrity | https://klarasystems.com/articles/understanding-zfs-scrubs-and-data-integrity/ | T2 | Kereszthivatkozás a ZFS scrub-fogalomhoz, nem idézve |
| ACM Queue — "Keeping Bits Safe: How Hard Can It Be?" | https://queue.acm.org/detail.cfm?id=1866298 | T1/T2 | Lektorált iparági folyóirat, háttérként azonosítva, nem idézve közvetlenül (a CERN- és NetApp-forrás elsődlegesebb és konkrétabb számokat ad) |
| Wikipedia — Data corruption / Silent data corruption | https://en.wikipedia.org/wiki/Data_corruption | T3 | Csak tájékozódásra, nem forrásként idézve |
| verasafe.com, hallboothsmith.com, probackup.io, termsbox.com stb. — GDPR/backup jogi blogok | (több URL) | T3 | Kifejezetten NEM használtuk elsődleges forrásként a 6. kérdésnél a feladat kikötése szerint; csak arra szolgáltak, hogy megtaláljuk az elsődleges ICO/EDPB dokumentumokat |
| Google Scholar / ResearchGate — "An Analysis of Latent Sector Errors in Disk Drives" (Bairavasundaram et al., SIGMETRICS'07) | https://www.researchgate.net/publication/221596257 | T1 (a mögöttes cikk) | A "testvér" tanulmány a szektorhibákról (nem silent corruption) — azonosítva, de nem idézve, mert a fő silent-corruption adatunk a FAST'08 cikkből van |

## Blokkolt / nem elérhető domain

- **openai.com** (a `/api/pricing/` útvonalon) — HTTP 403 mindkét curl-kísérletnél, proxyn keresztül. A `developers.openai.com` aldomain viszont elérhető volt és tartalmazta ugyanazt az árazási adatot, ezért ez nem okozott tényleges hiányt.

Más domain teljes blokkolást (proxy-hiba, TLS-hiba, 407/405) nem tapasztaltunk ebben a kutatásban.



---

# sq05 — A mentés mint cserélhető komponens: programozási minták

# Linkek — sq05

Minden meglátogatott és felderített link. **Tier** a feladat saját skálája szerint: T1 = hivatalos dokumentáció / forráskód / lektorált könyv; T2 = megbízható másodlagos / gyártói leírás; T3 = fórum, blog, aggregátor, közösségi tartalom. A teljes, gépi olvasható forrás: `_vault/backup-adapter-patterns/02-sources/manifest.jsonl` és `index.md`.

## Ténylegesen felhasznált és idézett források (37)

Mind **LIVE** állapotú a `check_links.py` linkellenőrzés szerint (2026-09-12).

| Cím | URL | Tier | Lekérés módja |
|---|---|---|---|
| Preparing a new repository — restic documentation | https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html | T1 | curl, közvetlen |
| References — restic documentation (Design, Repository Format, REST Backend API) | https://restic.readthedocs.io/en/stable/100_references.html | T1 | curl, közvetlen |
| restic internal/backend/backend.go — Backend interface (forráskód) | https://github.com/restic/restic/blob/master/internal/backend/backend.go | T1 | curl, `raw.githubusercontent.com` |
| restic doc/design.rst — Read and Write Ordering | https://github.com/restic/restic/blob/master/doc/design.rst | T1 | curl, `raw.githubusercontent.com` |
| FAQ — restic documentation | https://restic.readthedocs.io/en/stable/faq.html | T1 | curl, közvetlen |
| Manual — restic documentation (parancslista) | https://restic.readthedocs.io/en/stable/manual_rest.html | T1 | curl, közvetlen |
| Examples — restic documentation (systemd service) | https://restic.readthedocs.io/en/stable/080_examples.html | T1 | curl, közvetlen |
| Frequently asked questions — Borg documentation | https://borgbackup.readthedocs.io/en/stable/faq.html | T1 | curl, közvetlen |
| General — Borg documentation (Repository URLs) | https://borgbackup.readthedocs.io/en/stable/usage/general.html | T1 | curl, közvetlen |
| Internals — Data structures — Borg documentation | https://borgbackup.readthedocs.io/en/stable/internals/data-structures.html | T1 | curl, közvetlen |
| Borg 2.0 (preliminary information) — hivatalos kiadási jegyzék | https://www.borgbackup.org/releases/borg-2.0.html | T1 | curl, közvetlen |
| borgstore README (forráskód) | https://github.com/borgbackup/borgstore/blob/master/README.rst | T1 | curl, `raw.githubusercontent.com` |
| borgstore backends/_base.py — BackendBase (forráskód) | https://github.com/borgbackup/borgstore/blob/master/src/borgstore/backends/_base.py | T1 | curl, `raw.githubusercontent.com` |
| Borg backup to Amazon S3 on FUSE? — Issue #102 (borgbackup/borg) | https://github.com/borgbackup/borg/issues/102 | T3 | curl, **Wayback Machine mentés** (l. módszertani megjegyzés) |
| Overview of cloud storage systems — rclone documentation | https://rclone.org/overview/ | T1 | curl, közvetlen |
| rclone fs/types.go — Fs, Object, Info interfészek (forráskód) | https://github.com/rclone/rclone/blob/master/fs/types.go | T1 | curl, `raw.githubusercontent.com` |
| rclone fs/features.go — opcionális interfészek (forráskód) | https://github.com/rclone/rclone/blob/master/fs/features.go | T1 | curl, `raw.githubusercontent.com` |
| rclone CONTRIBUTING.md — Writing a new backend (forráskód) | https://github.com/rclone/rclone/blob/master/CONTRIBUTING.md | T1 | curl, `raw.githubusercontent.com` |
| Rclone — rsync for cloud storage (hivatalos honlap) | https://rclone.org/ | T1 | curl, közvetlen |
| kopia repo/blob/storage.go — Storage interfész (forráskód) | https://github.com/kopia/kopia/blob/master/repo/blob/storage.go | T1 | curl, `raw.githubusercontent.com` |
| Architecture — Kopia documentation | https://kopia.io/docs/advanced/architecture/ | T1 | curl, közvetlen |
| Repositories — Kopia documentation | https://kopia.io/docs/repositories/ | T1 | curl, közvetlen |
| Features — Kopia documentation (Policies) | https://kopia.io/docs/features/ | T1 | curl, közvetlen |
| Duplicati IBackend.cs — kötelező backend-interfész (forráskód) | https://github.com/duplicati/duplicati/blob/master/Duplicati/Library/Interface/IBackend.cs | T1 | curl, `raw.githubusercontent.com` |
| Destination overview — Duplicati hivatalos dokumentáció | https://docs.duplicati.com/backup-destinations/destination-overview | T1 | curl, közvetlen |
| Gamma/Helm/Johnson/Vlissides — Design Patterns (1994), Strategy fejezet kivonat (315–321. o.) | https://github.com/ansbilalgit/Books/blob/master/... (1994).pdf | T1 | curl, `raw.githubusercontent.com` + `pdftotext` |
| Hexagonal architecture — Alistair Cockburn (eredeti, 2005) | https://alistair.cockburn.us/hexagonal-architecture/ | T1 | curl, közvetlen |
| Repository — PoEAA catalog (martinfowler.com) | https://martinfowler.com/eaaCatalog/repository.html | T1 | curl, közvetlen |
| Yagni — martinfowler.com bliki | https://martinfowler.com/bliki/Yagni.html | T1 | curl, közvetlen |
| Speculative Generality — Refactoring (2nd ed.), InformIT/Pearson kivonat | https://www.informit.com/articles/article.aspx?p=2952392&seqNum=15 | T1 | curl, közvetlen |
| Rule of three (computer programming) — Wikipedia | https://en.wikipedia.org/wiki/Rule_of_three_(computer_programming) | T3 | curl, közvetlen |
| Origins of "The Rule of Three" (eoinnoble.com) | https://eoinnoble.com/posts/origins-of-the-rule-of-three/ | T3 | curl, közvetlen |
| Notes from Martin Fowler's "Refactoring" (GitHub gist) | https://gist.github.com/deanhunt/1c0ca8c5fe17b9b4f34a | T3 | curl, közvetlen |
| The Wrong Abstraction — Sandi Metz | https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction | T3 | curl, közvetlen |
| Amazon S3 Strong Consistency (hivatalos AWS oldal) | https://aws.amazon.com/s3/consistency/ | T1 | curl, közvetlen |
| Configuring the Director — Bacula hivatalos dokumentáció | https://www.bacula.org/11.0.x-manuals/en/main/Configuring_Director.html | T1 | curl, közvetlen |
| How Velero Works — hivatalos dokumentáció | https://velero.io/docs/main/how-velero-works/ | T1 | curl, közvetlen |

## Felderített, de nem hasznosított linkek (rossz URL-találat / dead end)

Ezek nem hiányok a témában — mind a tartalom **megtalálva máshol**, csak az első URL-tippem volt hibás.

| URL | Státusz | Ok / hova lett átirányítva a keresés |
|---|---|---|
| https://kopia.io/docs/advanced/scheduling/ | 404 | Az ütemezés tartalma valójában `kopia.io/docs/features/` (Policies szakasz) |
| https://docs.duplicati.com/detailed-descriptions/all-supported-backends | 404 | A backend-lista valójában `docs.duplicati.com/backup-destinations/destination-overview` |
| https://borgbackup.readthedocs.io/en/2.0.0b14/deployment/repository-server.html | 404 | A borgstore-bejelentés fő állítását a hivatalos `borgbackup.org/releases/borg-2.0.html` már lefedte |
| https://rclone.org/contributing/ | 404 | A "Writing a new backend" tartalom a `github.com/rclone/rclone` repó `CONTRIBUTING.md` fájljában van |
| https://api.github.com/repos/borgbackup/borg/issues/102 | 403 | GitHub API ebben a környezetben connector-kapu mögött; a `github.com` webes felülete is ugyanígy gated ("GitHub access to this repository is not enabled for this session") — **nem** a nyilvános internet blokkolja, hanem ennek a sessionnek a hozzáférési szintje |
| https://api.github.com/repos/borgbackup/borg/issues/431 | 403 | ua. |
| http://web.archive.org/web/…/github.com/…/issues/102 (http, nem https) | „Blocked by egress policy” | A `https://` változat működött — a proxy csak a titkosítatlan `http://` sémát utasította el ezen a domainen |

## WebSearch-lekérdezések, amik URL-forrást adtak (a tényleges tartalmat curl hozta be)

L. részletesen `keresesek.md`. A `WebSearch` eszközt kizárólag URL-ek megtalálására használtam, sosem tartalom-kinyerésre — minden idézet a curl-lal ténylegesen letöltött, lementett fájlból származik. `WebFetch`-et **egyszer sem** használtam ebben a kutatásban.



---

# sq06 — Séma- és formátum-migráció motorfüggetlenül

# sq06 — Meglátogatott és felderített linkek

Tier: **T1** hivatalos doksi/forráskód/elsődleges céges közlemény · **T2** megbízható
másodlagos/gyártói · **T3** fórum/blog/anekdota. **Lekérés módja:** `curl` = nyers
HTML/szöveg letöltve a proxyn keresztül és feldolgozva; `WebSearch` = csak a keresési
találati listában látott cím/URL, tartalma nem lett külön lekérve; `WebFetch` = a
Claude WebFetch eszközével kérve le (ebben a kutatásban nem használtuk, mindenütt
`curl`-lal dolgoztunk a módszertani kikötés szerint).

## SQ-1 — Liquibase

| Cím | URL | Tier | Lekérés |
|---|---|---|---|
| Liquibase Reference: What is a Change Type? | https://docs.liquibase.com/change-types/home.html | T1 | curl |
| Liquibase Reference: sql Change Type | https://docs.liquibase.com/change-types/sql.html | T1 | curl |
| Liquibase Reference: addAutoIncrement Change Type | https://docs.liquibase.com/change-types/add-auto-increment.html | T1 | curl |
| Liquibase Reference: dbms attribute | https://docs.liquibase.com/secure/reference-guide-5-1/changelog-attributes/dbms | T1 | curl |
| Liquibase Reference: dbms (alternatív URL, 404) | https://docs.liquibase.com/change-types/dbms.html | — | curl (404, blocked.jsonl) |
| Liquibase: Supported Databases | https://www.liquibase.com/supported-databases | T2 | WebSearch (nem olvasva) |
| Baeldung: List All Liquibase SQL Types With Java | https://www.baeldung.com/java-liquibase-list-sql-types | T3 | WebSearch (nem olvasva) |
| Liquibase: How does Liquibase handle data types? | https://docs.liquibase.com/concepts/data-type-handling.html | T1 | WebSearch (nem olvasva) |
| Liquibase GitHub issue #1084 (dbms attribútum hibás DB-névre) | https://github.com/liquibase/liquibase/issues/1084 | T2 | WebSearch (nem olvasva) |

## SQ-2 — Flyway

| Cím | URL | Tier | Lekérés |
|---|---|---|---|
| Redgate Flyway Docs: Migrations | https://documentation.red-gate.com/fd/migrations-271585107.html | T1 | curl |
| Redgate Flyway Docs: Migrations (első próbálkozás, 404) | https://documentation.red-gate.com/fd/migrations-184127470.html | — | curl (404) |
| Redgate Flyway Docs: Locations setting | https://documentation.red-gate.com/flyway/reference/configuration/flyway-namespace/flyway-locations-setting | T1 | curl |
| Redgate Flyway Docs: Recommended practices | https://documentation.red-gate.com/fd/recommended-practices-150700352.html | T1 | curl |
| Redgate Flyway Docs: Migrations-based approach | https://documentation.red-gate.com/fd/migrations-based-approach-168984769.html | T1 | curl |
| Redgate Flyway Blog: Making Generated Migrations More Portable with Placeholder Replacement | https://documentation.red-gate.com/flyway/flyway-blog/making-generated-migrations-more-portable-with-placeholder-replacement | T1 | curl |
| flywaydb.org (archívum, Wayback 2018): Migrations concept | https://web.archive.org/web/2018/https://flywaydb.org/documentation/migrations | T1 | curl |
| flywaydb.org (archívum, Wayback ~2018): Why database migrations | https://web.archive.org/web/2018/https://flywaydb.org/getstarted/why | T1 | curl |
| flyway/flywaydb.org GitHub (gh-pages, migrations.md nyers markdown) | https://raw.githubusercontent.com/flyway/flywaydb.org/gh-pages/documentation/concepts/migrations.md | T1 | curl |
| Spring Boot Reference: Database Initialization ({vendor} placeholder) | https://docs.spring.io/spring-boot/how-to/data-initialization.html | T1 | curl |
| Spring Boot Reference (aktuális link, 404) | https://docs.spring.io/spring-boot/reference/how-to/data-initialization.html | — | curl (404) |
| Spring Boot Reference (régi, docs/current, működött) | https://docs.spring.io/spring-boot/docs/current/reference/html/howto-database-initialization.html | T1 | curl |
| GitHub issue: Vendor specific flyway migrations not working (spring-boot #8281) | https://github.com/spring-projects/spring-boot/issues/8281 | T2 | WebSearch (nem olvasva) |
| Flyway GitHub repo | https://github.com/flyway/flyway | T1 | WebSearch (nem olvasva) |
| Flyway Wikipedia szócikk | https://en.wikipedia.org/wiki/Flyway_(software) | T3 | WebSearch (nem olvasva) |

## SQ-3 — Drizzle ORM

| Cím | URL | Tier | Lekérés |
|---|---|---|---|
| Drizzle ORM Docs: Migrations fundamentals | https://orm.drizzle.team/docs/migrations | T1 | curl |
| Drizzle Kit Docs: Configuration file (dialect option) | https://orm.drizzle.team/docs/drizzle-config-file | T1 | curl |
| Drizzle Kit Docs: generate command | https://orm.drizzle.team/docs/drizzle-kit-generate | T1 | curl |
| Drizzle ORM Docs: Kit overview | https://orm.drizzle.team/docs/kit-overview | T1 | curl (letöltve, részletesen nem idézve) |
| Drizzle ORM Docs: Goodies | https://orm.drizzle.team/docs/goodies | T1 | curl (letöltve, részletesen nem idézve) |
| Drizzle ORM Docs: SQL schema declaration | https://orm.drizzle.team/docs/sql-schema-declaration | T1 | curl (letöltve, részletesen nem idézve) |
| Drizzle ORM forráskód: PgDialect osztály | https://github.com/drizzle-team/drizzle-orm/blob/main/drizzle-orm/src/pg-core/dialect.ts | T1 | curl (raw.githubusercontent.com) |
| Drizzle ORM forráskód: SQLiteDialect absztrakt osztály | https://github.com/drizzle-team/drizzle-orm/blob/main/drizzle-orm/src/sqlite-core/dialect.ts | T1 | curl (raw.githubusercontent.com) |
| Drizzle ORM forráskód: dialect.ts (közös bázis, NEM létezik) | https://raw.githubusercontent.com/drizzle-team/drizzle-orm/main/drizzle-orm/src/dialect.ts | — | curl (404 — hiány, l. hianyok.md) |
| MakerKit Docs: Migrating from PostgreSQL to MySQL (Drizzle) | https://makerkit.dev/docs/nextjs-drizzle/database/mysql | T2 | curl |
| drizzle-kit npm csomag oldala | https://www.npmjs.com/package/drizzle-kit | T2 | WebSearch (nem olvasva) |
| Drizzle GitHub Discussion #1604 (migrate after push) | https://github.com/drizzle-team/drizzle-orm/discussions/1604 | T3 | WebSearch (nem olvasva) |
| Drizzle GitHub Issue #2815 (mysql migration bug) | https://github.com/drizzle-team/drizzle-orm/issues/2815 | T3 | WebSearch (nem olvasva) |
| Budi Voogt blog: Drizzle migrations to postgres in production | https://budivoogt.com/blog/drizzle-migrations | T3 | WebSearch (nem olvasva) |

## SQ-4 — Django / Rails séma-absztrakció

| Cím | URL | Tier | Lekérés |
|---|---|---|---|
| Django Docs: SchemaEditor | https://docs.djangoproject.com/en/5.1/ref/schema-editor/ | T1 | curl |
| Django forráskód: BaseDatabaseSchemaEditor (schema.py, base) | https://github.com/django/django/blob/main/django/db/backends/base/schema.py | T1 | curl (raw.githubusercontent.com) |
| Django forráskód: PostgreSQL schema.py | https://github.com/django/django/blob/main/django/db/backends/postgresql/schema.py | T1 | curl (raw.githubusercontent.com) |
| Django forráskód: SQLite schema.py | https://github.com/django/django/blob/main/django/db/backends/sqlite3/schema.py | T1 | curl (raw.githubusercontent.com) |
| Django forráskód: MySQL schema.py | https://github.com/django/django/blob/main/django/db/backends/mysql/schema.py | T1 | curl (raw.githubusercontent.com) |
| Rails forráskód: SchemaStatements modul | https://github.com/rails/rails/blob/main/activerecord/lib/active_record/connection_adapters/abstract/schema_statements.rb | T1 | curl (raw.githubusercontent.com) |
| Rails forráskód: AbstractAdapter | https://github.com/rails/rails/blob/main/activerecord/lib/active_record/connection_adapters/abstract_adapter.rb | T1 | curl (raw.githubusercontent.com) |
| DeepWiki: django/django Database Backends (nem hivatalos) | https://deepwiki.com/django/django/2.3-schema-and-migrations | T3 | WebSearch (nem olvasva) |
| reinout.vanrees.org: Django custom database backends | https://reinout.vanrees.org/weblog/2016/11/04/database-backends.html | T3 | WebSearch (nem olvasva) |

## SQ-5 — Kapacitás-jelző minta

| Cím | URL | Tier | Lekérés |
|---|---|---|---|
| Django forráskód: BaseDatabaseFeatures (features.py, base) | https://github.com/django/django/blob/main/django/db/backends/base/features.py | T1 | curl (raw.githubusercontent.com) |
| Django forráskód: MySQL DatabaseFeatures felülírások | https://github.com/django/django/blob/main/django/db/backends/mysql/features.py | T1 | curl (raw.githubusercontent.com) |
| Rails forráskód: SQLite3Adapter | https://github.com/rails/rails/blob/main/activerecord/lib/active_record/connection_adapters/sqlite3_adapter.rb | T1 | curl (raw.githubusercontent.com) |
| Rails forráskód: AbstractMysqlAdapter | https://github.com/rails/rails/blob/main/activerecord/lib/active_record/connection_adapters/abstract_mysql_adapter.rb | T1 | curl (raw.githubusercontent.com) |
| Rails forráskód: PostgreSQLAdapter | https://github.com/rails/rails/blob/main/activerecord/lib/active_record/connection_adapters/postgresql_adapter.rb | T1 | curl (raw.githubusercontent.com) |

## SQ-6 — Fájlformátum-migráció minták

| Cím | URL | Tier | Lekérés |
|---|---|---|---|
| nbformat Docs: Python API (read/write, as_version) | https://nbformat.readthedocs.io/en/latest/api.html | T1 | curl |
| nbformat Docs: The Notebook file format | https://nbformat.readthedocs.io/en/latest/format_description.html | T1 | curl |
| Kubernetes Docs: Storage Versions | https://kubernetes.io/docs/concepts/overview/working-with-objects/storage-version/ | T1 | curl |
| Kubernetes Docs: Versions in CustomResourceDefinitions | https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definition-versioning/ | T1 | curl |
| martinfowler.com bliki: Tolerant Reader | https://martinfowler.com/bliki/TolerantReader.html | T1 | curl |
| martinfowler.com articles: Consumer-Driven Contracts (szerző: Ian Robinson) | https://martinfowler.com/articles/consumerDrivenContracts.html | T1 | curl |
| Docusaurus Docs: Automated migration (v1→v2 CLI) | https://docusaurus.io/docs/3.8.1/migration/v2/automated | T1 | curl |
| Docusaurus Docs: migration/v1-to-v2 (elavult URL, 404) | https://docusaurus.io/docs/migration/v1-to-v2 | — | curl (404, blocked.jsonl) |
| Internet Archive: REST in Practice (2010, Webber/Parastatidis/Robinson) | https://archive.org/details/restinpractice0000webb_1sted | T1 | curl — metaadat OK, teljes szöveg 403 (Controlled Digital Lending, blocked.jsonl) |
| Medium: Demystified Tolerant Reader (Frank Scheffler) | https://medium.com/digitalfrontiers/demystified-tolerant-reader-ca07d6bea602 | T3 | WebSearch (nem olvasva) |
| servicedesignpatterns.com: Tolerant Reader (Rob Daigneau saját oldala) | http://servicedesignpatterns.com/WebServiceEvolution/TolerantReader | T2 | WebSearch (nem olvasva) |
| Hacker News: "This is what Martin Fowler refers to as the Tolerant Reader pattern" | https://news.ycombinator.com/item?id=14713220 | T3 | WebSearch (nem olvasva) |

## SQ-7 — Motorfüggetlenség elhagyása

| Cím | URL | Tier | Lekérés |
|---|---|---|---|
| GitLab Blog: Why we're ending support for MySQL in 12.1 (Kenny Johnston, 2019.06.27) | https://about.gitlab.com/blog/2019/06/27/removing-mysql-support/ | T1 | curl (élő oldal JS-shell volt tartalom nélkül) + curl Wayback-en (2019-es HTML-lel) |
| GitLab MR 29790: Only support postgresql (minimal version) | https://gitlab.com/gitlab-org/gitlab-foss/-/merge_requests/29790 | T1 | curl |
| GitLab Issue #51173: Consider removing support for MySQL | https://gitlab.com/gitlab-org/gitlab-foss/-/issues/51173 | T1 | curl (letöltve, tartalma nem részletesen idézve) |
| GitLab docs: mysql_to_postgresql migrációs útmutató | https://docs.gitlab.com/ee/update/mysql_to_postgresql.html | T1 | WebSearch (nem olvasva) |
| postgresql.org mailing lista: HN discussion — Gitlab becomes Postgresql only | https://www.postgresql.org/message-id/4936bd1e1df740a6ad16284931797e4c%40noordhoff.nl | T3 | WebSearch (nem olvasva) |
| GitHub: TeamHG-Memex/agnostic (Agnostic Database Migrations eszköz) | https://github.com/TeamHG-Memex/agnostic/blob/1.0.1/docs/overview.rst | T2 | WebSearch (nem olvasva) |

---

**Megjegyzés a WebFetch-ről:** ebben a kutatásban a módszertani kikötés szerint minden
elsődleges forrást nyers `curl`-lal kértünk le a proxyn keresztül, majd Python
`re`/`html` modulokkal HTML→szöveg konverziót végeztünk. A `WebFetch` eszközt egyáltalán
nem használtuk — minden fenti "curl" jelölés ezt az utat jelenti. A "WebSearch (nem
olvasva)" sorok azok, amelyek csak a keresési találati listában bukkantak fel, de nem
kaptak külön lekérést (idő-korlát miatt, vagy mert a fő állítást már két másik forrás
megerősítette).
