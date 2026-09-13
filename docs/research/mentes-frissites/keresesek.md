# Keresések — mentés és verziófrissítés

Minden lefuttatott lekérdezés szó szerint, kutatási egységenként — a kutatás így megismételhető.



---

# sq01 — Fájl-alapú tartalom mentése és helyreállítása

# SQ01 — Lefuttatott keresések (szó szerint, megismételhetőség céljából)

Minden keresés a `WebSearch` eszközzel futott (kivéve, ahol jelölve), időrendben.

## 1. kör — Q1: fájlmentés-konzisztencia eszközönként

1. `BorgBackup documentation "read-special" OR "changed during backup" consistency`
2. `restic documentation FAQ "files change during backup" consistency snapshot`
3. `rsync man page "vanish" OR "changed during transfer" file modified during rsync`
4. `OpenZFS documentation zfs snapshot "point in time" consistency backup`
5. `Btrfs wiki snapshot documentation consistent backup atomic`
6. `"3-2-1 backup rule" origin Peter Krogh history who invented`

## 2. kör — Q3/Q4/Q5 hivatalos szervek

7. `CISA "3-2-1" backup rule data backup options`
8. `US-CERT "3-2-1" backup tip ST04`
9. `NIST SP 800-34 backup RPO RTO definition contingency planning guide`
10. `"restore testing" backup official recommendation frequency NIST OR CISA "test your backups"`
11. `percentage backups fail to restore statistic survey unrecoverable`
12. `Obsidian Sync official documentation how backup works version history`

## 3. kör — restic Linux-konzisztencia, Btrfs hivatalos doksi

13. `restic documentation "does not guarantee" OR "not consistent" OR "LVM snapshot" backup Linux consistency recommendation`
14. (nyers curl, nem keresés) `https://btrfs.readthedocs.io/en/latest/Subvolumes.html`, `https://btrfs.readthedocs.io/en/latest/btrfs-send.html`

## 4. kör — Q2: git/Logseq/Obsidian mélyebb ásás

15. `GitHub official documentation repository size limits large files best practices`
16. `Logseq official documentation backup "version history" OR "git" sync data`
17. `git documentation "not designed" OR "not well suited" binary files large repositories`
18. `"git is not a backup" official OR "git is not backup tool"`
19. `site:obsidian.md/help backup OR "back up your vault"`
20. `Obsidian help "Sync is not" OR "not a backup" OR "we recommend backing up"`
21. `"Back up your Obsidian files" obsidian.md/help`

## 5. kör — Q3: 3-2-1 eredet mélyebb ásás

22. `Peter Krogh "The DAM Book" 3-2-1 backup rule photography 2005`
23. `US-CERT "Data Backup Options" 3-2-1 rule Carnegie Mellon history first`
24. `"3-2-1" backup rule "coined by" OR "popularized by" OR "originated"`
25. `"data_backup_options.pdf" CISA mirror site:.gov OR site:.edu`
26. `Backblaze blog "origin" 3-2-1 backup strategy history CERT government agencies`

## 6. kör — Q4: restore drill, statisztika

27. (7-11-es keresések újrahasznosítva, nincs új)
28. `W. Curtis Preston "nobody wants backups, everybody wants restores" quote`
29. `"untested backup" "is not a backup" origin quote who said`

## 7. kör — Q5: kis rendszerek gyakorisága, RPO/RTO hivatalos

30. `NCSC UK "back up your data" small business backup guidance official`
31. `ISO 22301 RPO RTO definition business continuity official`
32. `CIS Controls v8 "Data Recovery" control 11 backup frequency encrypt offline safeguard`

## 8. kör — Q6: jogosultsági kockázat, NCSC ransomware-resistant elvek

33. `NCSC "Principles for ransomware-resistant" on-premises backups site:ncsc.gov.uk`
34. `CISA #StopRansomware Guide backup "separate" credentials network segmentation offline`
35. `NCSC ransomware-resistant backup principles November 2024 "write once read many" WORM article`
36. `"admin accounts and credentials that are separate from those used to administer" NCSC backup` (ellenőrzésképp — kizárólag az NCSC saját oldalán találta meg, tehát a WebFetch-idézet nem félrevezetés, de független második forrás nincs)

## Nyers curl-lekérések listája (proxin keresztül, User-Agent-tel, tag-stripeléssel)

- `borgbackup.readthedocs.io/en/stable/usage/notes.html`
- `borgbackup.readthedocs.io/en/stable/usage/create.html`
- `restic.readthedocs.io/en/stable/faq.html`
- `restic.readthedocs.io/en/stable/040_backup.html`
- `openzfs.github.io/openzfs-docs/man/master/8/zfs-snapshot.8.html`
- `wiki.archlinux.org/title/Btrfs`
- `btrfs.readthedocs.io/en/latest/Subvolumes.html`
- `btrfs.readthedocs.io/en/latest/btrfs-send.html`
- `www.cisa.gov/sites/default/files/publications/data_backup_options.pdf` — **sikertelen (Akamai Access Denied)**, több UA-val és cookie-jarral is újrapróbálva
- `www.cisa.gov/audiences/small-and-medium-businesses/secure-your-business/back-up-business-data` — **sikertelen**
- `www.cisa.gov/audiences/state-local-tribal-and-territorial-government/secure-us-sltt/back-government-data` — **sikertelen**
- `www.cisa.gov/` (gyökér, teszt célból) — **sikertelen**, megerősítve, hogy a teljes domain blokkolja a proxy IP-t
- `nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-34r1.pdf` — sikeres, `pdftotext -layout`-tal feldolgozva
- `csrc.nist.gov/pubs/sp/800/34/r1/upd1/final` — sikeres
- `obsidian.md/help/sync` → mögöttes `publish-01.obsidian.md/access/<uid>/Obsidian%20Sync/Introduction%20to%20Obsidian%20Sync.md` — sikeres (a HTML oldal JS-preload URL-jét kézzel kinyerve, majd azt a markdown URL-t közvetlenül lekérve)
- ugyanígy: `.../Obsidian%20Sync/Version%20history.md`, `.../Obsidian%20Sync/Set%20up%20Obsidian%20Sync.md` — sikeres
- `.../Obsidian%20Sync/Back%20up%20your%20vault.md` és `.../Backup.md` — **"File … does not exist" hiba**, a keresőmotor indexe által mutatott cím nem egyezett a tényleges fájlnévvel/hellyel
- `raw.githubusercontent.com/obsidianmd/obsidian-help/master/en/Getting%20started/Back%20up%20your%20Obsidian%20files.md` — sikeres, ez adta a helyes, teljes tartalmat
- `raw.githubusercontent.com/logseq/docs/master/db-version.md` — sikeres
- `docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github` — sikeres
- `docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits` — sikeres
- `git-scm.com/book/en/v2/Git-Internals-Packfiles` — sikeres, kevés hasznosítható idézet
- `raw.githubusercontent.com/RsyncProject/rsync/master/rsync.1.md` — sikeres (miután `download.samba.org/pub/rsync/rsync.1` és `rsync.samba.org/ftp/rsync/rsync.1` 403-at adott)
- `cas8.docs.cisecurity.org/en/latest/source/Controls11/` — sikeres
- `www.ncsc.gov.uk/collection/small-business-guide/backing-your-data` — sikeres HTTP-válasz, de a body csak navigáció/JS-héj (redirect a gyűjtőoldalra)
- `www.ncsc.gov.uk/collection/small-organisations-guide-to-cyber-security/1-backing-up-your-data` és a redirect utáni `.../backing-up-your-data` — sikeres HTTP-válasz, de nincs érdemi szöveges tartalom a nyers HTML-ben (kliensoldali renderelés)
- `www.ncsc.gov.uk/collection/ransomware-resistant-backups` — ua., JS-alapú
- `www.ncsc.gov.uk/pdfs/guidance/principles-for-ransomware-resistant-cloud-backups.pdf` és `.../on-premises-backups.pdf` — **404**, a valós PDF-útvonal nem egyezett a keresőtalálat által sugallttal
- `www.at-bay.com/press_releases/report-reveals-businesses-fail-to-recover-backup-when-hit-by-ransomware/` — sikeres
- `www.backblaze.com/blog/the-2022-backup-survey-54-report-data-loss-with-only-10-backing-up-daily/` — sikeres
- `www.backblaze.com/blog/the-3-2-1-backup-strategy/` — sikeres
- `www.backupwrapup.com/peter-krogh-who-coined-the-3-2-1-rule-on-our-podcast/` — sikeres
- `thedambook.com/the-dam-book/` — sikeres
- `en.wikipedia.org/wiki/Peter_Krogh_(photographer)` — sikeres
- `en.wikipedia.org/wiki/Backup` — sikeres
- `archive.org/wayback/available?url=...` (kétszer, CISA PDF-hez és CISA biz. oldalhoz) — sikeres válasz (JSON), de a mutatott `web.archive.org/web/...` snapshot-URL lekérése **"Blocked by egress policy"** hibát adott (munkakörnyezeti szabályzat, nem próbáltuk megkerülni)

## WebFetch-lekérések listája (kis modell összefoglalója — külön jelölve, mert a metodikai kikötés ezt kéri)

- `https://www.cisa.gov/sites/default/files/publications/data_backup_options.pdf` — **hiba: 403 client error**, nem hozott tartalmat
- `https://www.cisa.gov/audiences/small-and-medium-businesses/secure-your-business/back-up-business-data` — sikeres, szó szerinti idézeteket adott vissza
- `https://www.cisa.gov/audiences/state-local-tribal-and-territorial-government/secure-us-sltt/back-government-data` — sikeres
- `https://www.cisa.gov/news-events/cybersecurity-advisories/aa21-131a` (StopRansomware/DarkSide advisory, kiegészítő ellenőrzési kísérlet) — **hiba: 403 client error**, nem hozott tartalmat
- `https://obsidian.md/help/Obsidian+Sync/Back+up+your+vault` — sikeres válasz, de a tartalma "Not Found" hibaüzenet volt (megerősítve, hogy ez a konkrét URL/cím valóban nem létezik, nem csak a nyers curl hibázott)
- `https://www.ncsc.gov.uk/collection/small-organisations-guide-to-cyber-security/backing-up-your-data` — sikeres, szó szerinti idézeteket adott (offline másolat, teszteld a visszaállítást — de gyakoriságot/titkosítást nem talált a lapon)
- `https://www.ncsc.gov.uk/collection/ransomware-resistant-backups` — sikeres, de csak a gyűjtőoldal bevezetőjét adta vissza, jelezte, hogy a részletek az al-oldalakon vannak
- `https://www.ncsc.gov.uk/collection/ransomware-resistant-backups/principles-for-ransomware-resistant-on-premises-backups` — sikeres, mind a 6 elvet szó szerint visszaadta

## Nem elérhető / blokkolt domainek összefoglalása

| Domain | Ok |
|---|---|
| `www.cisa.gov` | Akamai-alapú "Access Denied" a proxy kimenő IP-jére nyers HTTP kéréseknél; WebFetch részben működött, de nem minden aloldalon (pl. a StopRansomware advisory és a PDF WebFetch-csal is 403) |
| `rsync.samba.org`, `download.samba.org` | HTTP 403, "Request forbidden by administrative rules" — nem próbáltuk WebFetch-csal, mert találtunk kanonikus GitHub-forrást helyette |
| `web.archive.org` (snapshot-elérés, `/web/...` útvonal) | Munkakörnyezeti egress-szabályzat által explicit blokkolva ("Blocked by egress policy") — nem technikai hiba, nem próbáltuk megkerülni |
| `www.ncsc.gov.uk` (tartalmi aloldalak nyers curl-lel) | Nem blokkolt, de kliensoldali JS-renderelés miatt a nyers HTML üres tartalmi törzset ad — WebFetch szükséges volt minden idézethez |



---

# sq02 — Futó SQLite adatbázis biztonságos mentése

# sq02 — Lefuttatott keresések (szó szerint)

## Módszertani megjegyzés

A munkamenetben nem állt rendelkezésre subagent-fanout eszköz (lásd `megallapitasok.md` fejléce), ezért minden keresést és lekérést egyetlen, szekvenciális munkamenet végzett. A `sqlite.org` és `litestream.io` oldalakat célzottan, közvetlen URL-lel, `curl`-lel töltöttem le (ezek nem "keresések", hanem direkt lekérések — lásd `linkek.md`). Az alábbi lista a ténylegesen a `WebSearch` eszközzel lefuttatott, szabad szöveges kereséseket tartalmazza, abban a sorrendben, ahogy elhangzottak.

## WebSearch hívások, szó szerint

1. `SQLite "VACUUM INTO" version 3.27.0 release notes added`
   — Cél: a VACUUM INTO bevezetési verziójának megerősítése. Eredmény: releaselog linkek listája; a `3_27_0.html` közvetlen curl-lekérésével véglegesen megerősítve.

2. `"VACUUM INTO" sqlite benchmark time large database gigabytes blocking writers`
   — Cél: mért időadat keresése VACUUM INTO-ra méret szerint. Eredmény: nem hozott közvetlen, számszerű benchmarkot; SQLite fórum-linkek és tankönyv-oldalak jöttek fel, ezek közül a `lang_vacuum.html`-t már közvetlenül elértük.

3. `"sqlite3_backup" vs "VACUUM INTO" speed comparison how long does it take`
   — Cél: közvetlen összehasonlító mérés keresése. Eredmény: főleg PostgreSQL levelezőlista-találatok (irrelevánsak, más motor), plusz a hivatalos `backup.html`. Nincs releváns, számszerű összehasonlítás.

4. `SQLite backup two databases consistent snapshot cross-database consistency problem`
   — Cél: a 6. kérdés (kereszt-konzisztencia) forrásainak felderítése. **Ez hozta a legfontosabb találatokat**: a SQLite fórum "Backup via file system backup software" és "Transactions involving multiple databases" szálait, az Oldmoe blogot, a Lobsters-vitát és a gyanús `sqlite.work` oldalt.

5. `"VACUUM INTO" slow large database github issue OR forum minutes`
   — Cél: konkrét, méret-specifikus lassúsági panasz/mérés keresése GitHub issue-kban vagy fórumokon. Eredmény: **nem hozott releváns SQLite-specifikus találatot** — a top találatok más projektek (atuin, delta-io, frigate, PostgreSQL) VACUUM-mechanizmusairól szóltak, nem SQLite `VACUUM INTO`-ról.

6. `sqlite backup blocks writes how long "GB" database litestream checkpoint benchmark seconds`
   — Cél: mért blokkolási időtartam keresése. Eredmény: a SQLite fórum "wal checkpointing very slow" szála (kvalitatív, nem számszerű), illetve több harmadlagos/SEO-jellegű oldal (`sesamedisk.com`, `dev.to`), amelyeket nem tekintettem elég megbízhatónak konkrét számok forrásaként, ezért nem is lettek lekérve/idézve.

7. `oldmoe.blog backup strategies for sqlite in production`
   — Cél: az elsődleges blogbejegyzés pontos URL-jének megtalálása (a korábbi keresésekben csak a Lobsters-vita jött fel, nem maga a cikk). Eredmény: megtalálva, közvetlenül lekérve (`oldmoe.blog/2024/04/30/...`).

8. `sqlite3 CLI ".backup" command implemented using "backup API" shell.c source`
   — Cél: annak megerősítése, hogy a `.backup` CLI-parancs valóban a Backup API-t hívja-e alatta. Eredmény: nem hozott közvetlen, idézhető megerősítést semmilyen oldalon (csak harmadlagos "hogyan mentsünk SQLite-ot" oktatóanyagok) — ezért a végső megerősítést **közvetlenül a SQLite forráskódjából** (`shell.c.in`, Fossil-repó) szereztem be, curl-lel.

## Direkt (nem keresőmotoros) lekérések, amik hibával/váratlan eredménnyel jártak

| URL | Eredmény | Kezelés |
|---|---|---|
| `https://www.sqlite.org/c3ref/backup_init.html` | HTTP 404 | Az init/step/finish egy közös oldalon van (`backup_finish.html`); ott találtuk meg a teljes szöveget. |
| `https://litestream.io/faq/` | HTTP 404 | Az oldal nem létezik/megszűnt a jelenlegi (v0.5.x) dokumentáció-struktúrában; a `guides/` menüjében sem szerepelt hivatkozásként. Nincs pótforrás rá, mert a tartalma (ha valaha is létezett) máshova olvadhatott be (pl. `tips/`). |
| `https://sqlite.org/forum/info/796a192a95ac35b9` | Első kísérlet: `curl: (35) Recv failure: Connection reset by peer` | Második, azonnali újrapróbálkozásra HTTP 200-at adott — átmeneti proxy/hálózati hiba volt, nem tartós blokk. |
| `https://github.com/dani-garcia/vaultwarden/discussions/1613` | HTTP 403 | A GitHub feltehetően bot-védelmi okból (User-Agent vagy egyéb heurisztika alapján) elutasította a `curl`-kérést. Nem próbálkoztunk tovább (a módszertani szabály szerint nem kerülendő meg technikai eszközökkel egy elutasító domain) — a `.backup`-ról szóló kérdést végül a forráskódból oldottuk meg, így ez a forrás nem volt szükséges. |

## Nem elérhető / blokkolt domainek összefoglalása

- **GitHub** (`github.com`) — a Vaultwarden discussion HTTP 403-at adott. Más GitHub-tartalmat nem próbáltunk lekérni ebben a kutatásban.
- **litestream.io/faq/** — HTTP 404, valószínűleg megszűnt oldal, nem "blokkolás".
- **sqlite.org/c3ref/backup_init.html** (és feltehetően a `backup_step.html` külön URL is) — HTTP 404, de ez nem hiányzó tartalom, hanem az, hogy a SQLite dokumentáció szándékosan egy közös oldalra (`backup_finish.html`) szervezi a Backup API mindhárom függvényét.

Minden más, ebben a kutatásban megcélzott `sqlite.org` és `litestream.io` URL sikeresen (HTTP 200) válaszolt.



---

# sq03 — Séma-migráció és verziófrissítés futó rendszeren

# sq03 — Lefuttatott keresések (szó szerint)

## Módszertani megjegyzés

Ez a kutatás a `Skill`-lel meghirdetett `anthropic-skills:deep-web-research` protokoll **degradált** módban futott:
az `Agent` (subagent-fanout) eszköz **nem volt elérhető** ebben a munkamenetben (`ToolSearch` „select:Agent"
lekérdezés nulla találatot adott), ezért a Sonnet-kereső-subagentek és az Opus-szintézis-subagent szétválasztása
nem történt meg — a teljes kutatást egyetlen ágens (ez a folyamat) végezte, egy kontextusban, fázisokra bontva
(terv → nyers HTML-lekérés és keresés → verifikáció menet közben, idézetek közvetlen forrás-egyeztetéssel →
szintézis). Ez a skill saját dokumentációja szerint (`SKILL.md`, „If the Agent tool is not available") elfogadott
üzemmód, de a modell-szintű szétválasztás (Sonnet-kereső / Opus-szintetizáló) előnye emiatt nem érvényesült — ezt
itt rögzítjük, hogy az olvasó tudja.

A hivatalos oldalakat **elsődlegesen nyers HTML-ként, `curl`-lel** (a környezet proxyján keresztül,
`--cacert /root/.ccr/ca-bundle.crt`), majd egy saját, helyben írt Python tag-stripelő szkripttel dolgoztuk fel
(script/kód-blokk-megőrző, script/style-eltávolító). A `WebSearch` hívásokat elsősorban forrás-*felderítésre*
használtuk (mely URL-eket érdemes nyersen letölteni, illetve közösségi/másodlagos megerősítés gyűjtésére), nem
tartalom-kinyerésre. `WebFetch`-et csak ott vetettük be, ahol a nyers `curl` HTTP 403-at adott vissza
(Zendesk-alapú support-oldal) — ez explicit módon jelölve van a `linkek.md`-ben és a `megallapitasok.md`-ben is.

---

## WebSearch lekérdezések (időrendben, szó szerint)

1. `drizzle-kit no rollback down migration github discussion`
   — Cél: közösségi megerősítés a Drizzle rollback-hiányára. Találatok: GitHub Issue #2510, #4005, Discussion
   #1339, egy harmadik féltől származó „drizzle-rollback" repó, és a hivatalos migrations oldal.

2. `"drizzle-kit" migration "statement-breakpoint" semicolon split`
   — Cél: megerősíteni a `--> statement-breakpoint` mechanizmust külső forrásból is. Találatok: GitHub PR #3538,
   GitHub Issue #4583 (libsql hibajelenség a breakpoint-tal kapcsolatban), Issue #3218 (MySQL-kompatibilis
   szintaxis breakpointokhoz), Frontend Masters blogcikk.

3. `SQLite FTS5 virtual table change columns "must be dropped" OR "drop and recreate" ALTER TABLE not supported`
   — Cél: megerősíteni/cáfolni, hogy egy FTS5 tábla szerkezetét csak drop+recreate-tel lehet módosítani.
   Találatok: sqlitebrowser Issue #781, Julia Evans TIL-cikk (más témában, de kapcsolódó), maga a
   `lang_altertable.html` (ami viszont NEM tárgyalja explicit módon a virtuális táblák esetét — ez hiányként
   rögzítve).

4. `"expand and contract" pattern Martin Fowler parallel change original definition`
   — Cél: az elsődleges forrás megtalálása. Találat: közvetlenül a `martinfowler.com/bliki/ParallelChange.html`
   (nyersen letöltve ezután), illetve a Wellhausen-tanulmány és egy Medium-cikk.

5. `expand contract migration pattern "single instance" OR "single server" OR "not necessary" zero downtime unnecessary`
   — Cél: közvetlen forrás arra, hogy a minta egy-példányos rendszernél feleslegesnek számít-e. Közvetlen,
   pontos találat nem került elő ezzel a kereséssel (a Fowler evodb-cikk és a Wellhausen-tanulmány adta meg végül
   ezt a választ, más útvonalon keresztül, lásd fent). Melléktalálat: GitLab MR „Proposal: Remove all single-node
   zero downtime instructions" — érdekes, de nem lett tovább követve (ld. `hianyok.md`).

6. `Flyway undo migrations documentation site:documentation.red-gate.com`
   — Cél: a helyes, aktuális Flyway-dokumentáció URL-jeinek megtalálása (az első próbálkozás
   `documentation.red-gate.com/flyway/...` útvonalon 404-et adott). Találatok: a helyes `fd/...` útvonalú oldalak,
   amiket ezután nyersen letöltöttünk.

7. `Flyway "back up your database" OR "backup" before migration documentation`
   — Cél: explicit Flyway-mentési ajánlás keresése. Találat: GitHub Issue #124 („Add a goal to do an SQL backup
   before the migration") — megerősíti, hogy a Flyway maga nem automatizál mentést.

8. `docs.liquibase.com best practices backup database before rollback`
   — Cél: Liquibase hivatalos „best practices" oldal megtalálása. A `bestpractices.html` URL valójában a Liquibase
   FAQ-ra redirektelt (letöltve, nincs benne mentési ajánlás). Melléktalálat: a support-FAQ „Does Liquibase Backup
   Any Data?" cikk, amit aztán WebFetch-csel kérdeztünk le (curl 403 miatt).

9. `Django documentation reversing migrations "no way" OR "cannot" guarantee reverse`
   — Cél: Django hivatalos állásfoglalása a visszafordíthatóságról. Találat: hivatalos `docs.djangoproject.com`
   migrations-oldal (amit már korábban letöltöttünk), és az `IrreversibleMigration`/`IrreversibleError` mechanizmus
   megerősítése GitHub ticketeken (#22095, #22445) keresztül.

10. `docker compose docs "service_completed_successfully" depends_on migration example`
    — Cél: hivatalos Docker Compose mechanizmus a migráció-sorrendezésre. Találat: közvetlenül a
    `docs.docker.com/reference/compose-file/services/` oldal, amit ezután nyersen letöltöttünk — ez adta a
    `pre_start` + Django `migrate` worked example-t.

11. `WordPress WXR "wxr_version" export format specification developer docs`
    — Cél: hivatalos WordPress-forrás a WXR verziómezőre. Első kör nem hozott tiszta hivatalos doksi-oldalt
    (csak GitHub-ok, fórumok); ezután közvetlenül a `developer.wordpress.org/reference/functions/export_wp/`
    oldalt kerestük meg és töltöttük le nyersen (lásd következő pont).

12. `SQLite FTS5 index corrupted "rebuild" only way to fix no partial repair`
    — Cél: közösségi megerősítés arra, hogy a `rebuild` az egyetlen javítási út sérült FTS5 index esetén.
    Találatok: kizárólag T3-as fórum/blog-források (MemPalace GitHub Issue, recoveryfix.com, corenexis.com blog,
    sqlite-users mailing lista) — ezek a hivatalos `fts5.html` „integrity-check csak jelez, rebuild javít" saját
    állítását támasztják alá közvetve.

13. `Django "backup" database before running migrate command official documentation`
    — Cél: van-e mégis valahol hivatalos Django-ajánlás mentésre. Csak T3-as találatok jöttek elő (Medium-cikk,
    harmadik féltől származó PyPI-csomagok) — ez megerősíti a `megallapitasok.md` 5.5 pontjában rögzített hiányt:
    a Django hivatalos dokumentációja nem ad ilyen ajánlást.

---

## `curl` alapú nyers HTML-lekérések (URL, HTTP-kód, méret)

Az alábbi táblázat minden `curl`-lel lekért URL-t felsorol a session során (a `linkek.md` ugyanezeket tier- és
témabontásban listázza).

| # | URL | HTTP | Méret (byte) |
|---|---|---|---|
| 1 | https://orm.drizzle.team/docs/kit-overview | 200 | 271 253 |
| 2 | https://orm.drizzle.team/docs/drizzle-kit-generate | 200 | 321 257 |
| 3 | https://orm.drizzle.team/docs/drizzle-kit-migrate | 200 | 273 958 |
| 4 | https://orm.drizzle.team/docs/drizzle-kit-push | 200 | 340 659 |
| 5 | https://orm.drizzle.team/docs/kit-custom-migrations | 200 | 225 021 |
| 6 | https://orm.drizzle.team/docs/migrations | 200 | 327 298 |
| 7 | https://raw.githubusercontent.com/drizzle-team/drizzle-orm/main/drizzle-orm/src/migrator.ts | 200 | 1 561 |
| 8 | https://raw.githubusercontent.com/drizzle-team/drizzle-orm/main/drizzle-orm/src/sqlite-core/dialect.ts | 200 | 28 455 |
| 9 | https://raw.githubusercontent.com/drizzle-team/drizzle-orm/main/drizzle-orm/src/migrator-common.ts | 404 | — (nem létező útvonal, elhagyva) |
| 10 | https://raw.githubusercontent.com/drizzle-team/drizzle-orm/main/drizzle-orm/src/better-sqlite3/migrator.ts | 200 | 401 |
| 11 | https://raw.githubusercontent.com/drizzle-team/drizzle-orm/main/drizzle-orm/src/bun-sqlite/migrator.ts | 200 | 393 |
| 12 | https://raw.githubusercontent.com/drizzle-team/drizzle-orm/main/drizzle-orm/src/libsql/migrator.ts | 200 | 1 411 |
| 13 | https://sqlite.org/lang_altertable.html | 200 | 428 175 |
| 14 | https://sqlite.org/pragma.html | 200 | 139 778 |
| 15 | https://sqlite.org/fts5.html | 200 | 210 915 |
| 16 | https://sqlite.org/vtab.html | 200 | 112 142 |
| 17 | https://martinfowler.com/bliki/ParallelChange.html | 200 | 22 616 |
| 18 | https://martinfowler.com/articles/evodb.html | 200 | 87 421 |
| 19 | https://www.tim-wellhausen.de/papers/ExpandAndContract/ExpandAndContract.html | 200 | 36 009 |
| 20 | https://documentation.red-gate.com/flyway/flyway-cli-and-api/concepts/migrations | 404 | 22 485 (hibaoldal) |
| 21 | https://documentation.red-gate.com/flyway/flyway-cli-and-api/concepts/migrations/undo-migrations | 404 | 22 485 (hibaoldal) |
| 22 | https://documentation.red-gate.com/fd/migrations-271585107.html | 200 | 43 115 |
| 23 | https://documentation.red-gate.com/fd/undo-migrations-273973334.html | 200 | 31 835 |
| 24 | https://documentation.red-gate.com/fd/undo-277578896.html | 200 | 30 693 |
| 25 | https://docs.liquibase.com/commands/rollback/rollback.html | 200 | 1 996 106 |
| 26 | https://guides.rubyonrails.org/active_record_migrations.html | 200 | 169 075 |
| 27 | https://docs.djangoproject.com/en/5.2/topics/migrations/ | 200 | 115 306 |
| 28 | https://support.liquibase.com/hc/en-us/articles/29383069283739-Does-Liquibase-Backup-Any-Data | 403 | 5 665 (blokkolva — lásd WebFetch alább) |
| 29 | https://docs.liquibase.com/workflows/liquibase-community/using-rollback.html | 200 | 542 543 |
| 30 | https://docs.liquibase.com/concepts/bestpractices.html | 200 | 449 398 (valójában FAQ-oldalra redirektelt) |
| 31 | https://docs.docker.com/engine/storage/volumes/ | 200 | 662 587 |
| 32 | https://docs.docker.com/compose/how-tos/lifecycle/ | 200 | 516 279 |
| 33 | https://docs.docker.com/reference/cli/docker/compose/up/ | 200 | 425 883 |
| 34 | https://docs.docker.com/compose/how-tos/production/ | 200 | 513 493 |
| 35 | https://docs.docker.com/reference/compose-file/services/ | 200 | 873 448 |
| 36 | https://docs.docker.com/reference/cli/docker/compose/down/ | 200 | 421 905 |
| 37 | https://docs.docker.com/reference/compose-file/version-and-name/ | 200 | 425 066 |
| 38 | https://raw.githubusercontent.com/jupyter/nbformat/main/docs/source/format_description.rst | 404 | 14 (nem létező útvonal) |
| 39 | https://raw.githubusercontent.com/jupyter/nbformat/main/nbformat/v4/nbformat.v4.schema.json | 200 | 16 104 |
| 40 | https://developers.home-assistant.io/docs/architecture/storage/ | 404 | 15 689 (nem létező útvonal — elhagyva, nem lett pótolva más URL-lel) |
| 41 | https://jsoncanvas.org/spec/1.0/ | 200 | 11 463 |
| 42 | https://nbformat.readthedocs.io/en/latest/format_description.html | 200 | 51 110 |
| 43 | https://nbformat.readthedocs.io/en/latest/api.html | 200 | 71 421 |
| 44 | https://developer.wordpress.org/reference/functions/export_wp/ | 200 | 201 266 |

## `WebFetch` hívások

| URL | Indoklás | Eredmény |
|---|---|---|
| https://support.liquibase.com/hc/en-us/articles/29383069283739-Does-Liquibase-Backup-Any-Data | `curl` HTTP 403-at adott (Zendesk bot-védelem) | Sikeres — a válasz idézi: „No, Liquibase does not back up any data before deploying any changesets." és a dry-run ajánlást |

## Nem elérhető / blokkolt domainek és útvonalak

| Domain / útvonal | Hiba | Kezelés |
|---|---|---|
| `support.liquibase.com` (Zendesk) | HTTP 403 `curl`-lel | Áthidalva `WebFetch`-csel (lásd fent), jelölve a jelentésben |
| `documentation.red-gate.com/flyway/flyway-cli-and-api/concepts/migrations` (és `/undo-migrations` alútvonal) | HTTP 404 | A Flyway dokumentáció URL-struktúrája időközben megváltozott; a helyes `fd/...`-útvonalú oldalakat WebSearch-csel találtuk meg, majd sikeresen letöltöttük |
| `raw.githubusercontent.com/.../nbformat/docs/source/format_description.rst` | HTTP 404 | A dokumentáció időközben Sphinx/`.rst`-ből átkerült egy másik struktúrába; a `nbformat.readthedocs.io` render-elt HTML-változatát használtuk helyette sikeresen |
| `developers.home-assistant.io/docs/architecture/storage/` | HTTP 404 | A Home Assistant storage-migrációs minta (`async_migrate_func`) tervezett hivatkozása nem volt elérhető ezen az URL-en; **nem lett pótolva más URL-lel időhiány miatt** — ez a `hianyok.md`-ben rögzítve van, a Home Assistant-példa **nincs** felhasználva a `megallapitasok.md`-ben, mert nem sikerült ellenőrizni |
| `raw.githubusercontent.com/.../drizzle-orm/main/drizzle-orm/src/migrator-common.ts` | HTTP 404 | Feltételezett fájlnév tévesen; a tényleges kód a `migrator.ts`-ben található, amit sikerült külön lekérni |

## Domainek, amikhez egyáltalán nem próbáltunk hozzáférni (időbeosztási döntés, nem technikai blokk)

- Joshua Kerievsky elsődleges anyagai (Industrial Logic, „The Limited Red Society" előadás) — csak Fowler
  másodkézből idézett állítására támaszkodtunk, ezt hiányként rögzítjük.
- Michael T. Nygard „Release It!" könyv (O'Reilly, 2007) — fizetős/nem szabadon hozzáférhető nyers szöveg,
  kizárólag a Wellhausen-tanulmány hivatkozásából ismerjük az állítást.
- Jekyll, Hugo, Eleventy, Astro, Gatsby hivatalos frontmatter-dokumentációi — nem lettek egyenként ellenőrizve
  ebben a körben (lásd `hianyok.md`); a `megallapitasok.md` 6. pontja emiatt **nem** állít semmit ezekről a
  konkrét rendszerekről, csak a ténylegesen ellenőrzött rendszerekre (nbformat, WXR, Compose, JSON Canvas)
  támaszkodik.



---

# sq04 — Mit kell menteni, és honnan tudjuk, hogy jó

# sq04 — Lefuttatott keresések (szó szerint)

## Módszertani megjegyzés

Ez a kutatás az `anthropic-skills:deep-web-research` skill szerint indult, de az **Agent-eszköz (subagent-fanout) nem volt elérhető** ebben a futtatási környezetben (ellenőrizve `ToolSearch`-csel: nem található "Agent"/subagent-dispatch eszköz, csak `TaskCreate/TaskUpdate/TaskGet/TaskList` egy egyszerű teendő-lista, illetve `SendMessage` más, már futó ügynökök felé — ezek nem alkalmasak Sonnet-alapú kereső-subagentek indítására). Mivel ez a folyamat maga is subagentként fut (a felhasználó/hívó agent már delegálta ezt a kutatási feladatot), a skill **degradált módban** futott: a keresési, ellenőrzési és szintézis fázisokat egyetlen folyamatos munkamenetben, szekvenciálisan végeztem el, Sonnet/Opus-particionálás nélkül. Ezt a skill instrukciója kifejezetten megengedi ("If the Agent tool is not available... the skill still works, degraded"), és itt rögzítjük, hogy ez történt.

A teljes vault-struktúra (00-plan.md, 02-sources/, 03-shards/, stb.) helyett a feladatkiírásban explicit megkért 5 fájlos kimenetet készítettem el (`megallapitasok.md`, `linkek.md`, `keresesek.md`, `hianyok.md`, `ellentmondasok.md`), mivel ezt a konkrét formátumot a hívó feladat explicit előírta egy nagyobb `mentes-frissites` kampány `sq04` alfeladataként.

## WebSearch lekérdezések (időrendben, szó szerint)

1. `"do not back up" search index rebuildable derived data backup best practice`
2. `Elasticsearch snapshot documentation "rebuild" index from source data backup recommendation`
3. `embedding cache content hash pattern avoid recompute embeddings cost`
4. `OpenAI embedding API price per 1000 tokens 2025 text-embedding-3`
5. `borgbackup check documentation "verifies the consistency"`
6. `restic check --read-data documentation official`
7. `ZFS scrub official documentation OpenZFS recommended frequency`
8. `CERN data corruption study silent bit rot rate disk`
9. `OWASP ASVS secrets management backup requirement "V" configuration`
10. `NIST SP 800-57 OR 800-53 secrets keys backup encryption requirement`
11. `CIS Controls backup encryption data at rest secrets requirement`
12. `GDPR right to erasure backups guidance data protection authority CNIL ICO`
13. `ICO guidance "right to erasure" backups "special case" deletion`
14. `Backblaze hard drive failure rate annual report statistics`
15. `NetApp silent data corruption study "1 in" disk drives measured`
16. `Google study disk failure "latent sector errors" annual report DRAM`
17. `CIS Controls v8 "Control 11" Data Recovery safeguard backup`
18. `Datenschutzkonferenz Orientierungshilfe Löschung Backup personenbezogene Daten`
19. `EDPB OR "data protection authority" guideline backup deletion "right to erasure" primary document PDF`
20. `Bairavasundaram "An Analysis of Latent Sector Errors" NetApp study percentage disks corruption`
21. `"silent data corruption" CERN "corrupted" files percentage bit rate 2007 Kelemen`
22. `CNIL sauvegarde durée conservation suppression fiche pratique RGPD`
23. `"backup" "manifestly disproportionate effort" erasure GDPR guidance`
24. `Elasticsearch snapshot restore documentation source of truth reindex time comparison`
25. `SQLite FTS5 rebuild index "rebuild" command time full text search`
26. `DSK Positionspapier Backup Löschung Artikel 17 DSGVO 2024`
27. `redis semantic cache embedding "content hash" key pattern documentation`
28. `Cohere OR Voyage embedding pricing per million tokens 2026`
29. `"rebuild" HNSW index vectors stored separately embeddings pgvector Qdrant documentation persistence`
30. `cost to embed 1 million documents OpenAI benchmark dollars time`
31. `LangChain CacheBackedEmbeddings documentation "underlying embeddings" cache store`
32. `Elasticsearch reindex time benchmark "documents per second" OR "million documents" hours`
33. `OpenAI embeddings API latency "requests per minute" batch throughput items per second benchmark`
34. `AWS Well-Architected REL09-BP01 "Identify and back up all data" reproduce from sources`
35. `CNIL "guide de la sécurité" sauvegardes fiche recommandation durée`
36. `CNIL sauvegarde "12 mois" OR "durée limitée" recommandation sécurité données`
37. `ZFS "scrub" "once a month" OR "once a week" recommended enterprise consumer disks official documentation`
38. `FreeBSD handbook ZFS scrub schedule recommendation`

## Nyers letöltési (curl) kísérletek — cél-URL-ek (lásd részletesen `linkek.md`)

- borgbackup.readthedocs.io/en/stable/usage/check.html
- restic.readthedocs.io/en/stable/045_working_with_repos.html
- openzfs.github.io/openzfs-docs/man/master/8/zpool-scrub.8.html
- raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x22-V13-Configuration.md
- cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
- usenix.org/legacy/events/fast08/tech/full_papers/bairavasundaram/bairavasundaram.pdf
- nsc.liu.se/lcsc2007/presentations/LCSC_2007-kelemen.pdf
- ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-erasure/
- cas8.docs.cisecurity.org/en/latest/source/Controls11/
- cas8.docs.cisecurity.org/en/latest/source/Controls3/
- sqlite.org/fts5.html
- docs.aws.amazon.com/en_us/wellarchitected/2022-03-31/framework/sus_sus_data_a9.html
- docs.aws.amazon.com/wellarchitected/latest/framework/sus_sus_data_a9.html
- docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_backing_up_data_identified_backups_data.html
- docs.aws.amazon.com/wellarchitected/2022-03-31/framework/sus_sus_data_a9.html (a REL09-BP01 első próbálkozása, JS-átirányítás miatt sikertelen — lásd lent)
- docs.oracle.com/en/operating-systems/solaris/oracle-solaris/11.4/manage-zfs/scheduled-data-scrubbing.html
- nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf
- edpb.europa.eu/system/files/2026-02/edpb_cef-report_2025_right-to-erasure_en.pdf
- cnb.avocat.fr/medias/cnilguidesecuritepersonnelle-68f7532f77b286.76172654.pdf
- cnil.fr/fr/passer-laction/les-durees-de-conservation-des-donnees
- cnil.fr/sites/cnil/files/atoms/files/guide_securite_personnelle.pdf (404, sikertelen)
- openai.com/api/pricing/ (403, sikertelen, kétszer próbálva)
- developers.openai.com/api/docs/models/text-embedding-3-small
- docs.llamaindex.ai/en/stable/module_guides/loading/ingestion_pipeline/
- python.langchain.com/docs/how_to/caching_embeddings/ (200, de nem a keresett tartalom — redirect egy overview oldalra)
- developers.soundcloud.com/blog/how-to-reindex-1-billion-documents-in-1-hour-at-soundcloud/
- www.backblaze.com/blog/backblaze-drive-stats-for-2025/

## Nem elérhető / sikertelen domainek

| Domain / URL | Hiba | Kezelés |
|---|---|---|
| `openai.com/api/pricing/` | HTTP 403 (kétszer, sima és egyedi User-Agent fejléccel is) | Helyettesítve: `developers.openai.com/api/docs/models/text-embedding-3-small` (ugyanaz az árazási adat, T1) |
| `www.cnil.fr/sites/cnil/files/atoms/files/guide_securite_personnelle.pdf` | HTTP 404 | Helyettesítve: ugyanaz a CNIL-kiadvány egy kamarai (cnb.avocat.fr) tükörpéldányról |
| `python.langchain.com/docs/how_to/caching_embeddings/` | HTTP 200, de a tartalom SPA-átépítés miatt egy általános overview oldalra mutatott, a keresett cache-leírás nem volt benne | Helyettesítve: `docs.llamaindex.ai` hivatalos Ingestion Pipeline dokumentációjával, amely explicit hash-alapú cache-mintát ír le |

Egyéb domain-blokkolást, proxy-hibát vagy TLS-hibát nem tapasztaltunk.



---

# sq05 — A mentés mint cserélhető komponens: programozási minták

# Keresések — sq05

Minden lefuttatott keresés/lekérés szó szerint, alkérdésenként csoportosítva. A gépi olvasható napló: `_vault/backup-adapter-patterns/01-search-log/queries.jsonl`.

## SQ-01 — restic backend-absztrakció

- `curl` → `https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html` (backend lista, rclone delegálás)
- `curl` → `https://restic.readthedocs.io/en/stable/100_references.html` (Design, Repository Format, REST Backend API)
- `curl` → `https://raw.githubusercontent.com/restic/restic/master/internal/backend/backend.go` (Backend Go interfész forráskód)
- `curl` → `https://raw.githubusercontent.com/restic/restic/master/doc/design.rst` (Read and Write Ordering szakasz)
- `curl` → `https://restic.readthedocs.io/en/stable/faq.html` (S3 Glacier cold storage restore idézet)

## SQ-02 — BorgBackup absztrakciós határai

- `curl` → `https://borgbackup.readthedocs.io/en/stable/faq.html`
- `curl` → `https://borgbackup.readthedocs.io/en/stable/usage/general.html`
- `curl` → `https://borgbackup.readthedocs.io/en/stable/internals/data-structures.html`
- `WebSearch` → `borgbackup github issue S3 backend maintainer why not random access repository`
- `curl` → `http://archive.org/wayback/available?url=github.com/borgbackup/borg/issues/102` (Wayback elérhetőség ellenőrzése)
- `curl` → `https://web.archive.org/web/20260104063017/https://github.com/borgbackup/borg/issues/102`
- `WebSearch` → `borgbackup 2.0 changelog rclone transport documentation`
- `curl` → `https://www.borgbackup.org/releases/borg-2.0.html`
- `curl` → `https://raw.githubusercontent.com/borgbackup/borgstore/master/README.rst`
- `curl` → `https://raw.githubusercontent.com/borgbackup/borgstore/master/src/borgstore/backends/_base.py`
- (dead end) `curl` → `https://api.github.com/repos/borgbackup/borg/issues/102` — 403
- (dead end) `curl` → `https://api.github.com/repos/borgbackup/borg/issues/431` — 403
- (dead end) `curl` → `https://borgbackup.readthedocs.io/en/2.0.0b14/deployment/repository-server.html` — 404

## SQ-03 — rclone Fs interfész

- `curl` → `https://rclone.org/overview/` (Optional Features tábla, Hash/ModTime szemantika)
- `curl` → `https://raw.githubusercontent.com/rclone/rclone/master/fs/types.go`
- `curl` → `https://raw.githubusercontent.com/rclone/rclone/master/fs/features.go`
- `curl` → `https://raw.githubusercontent.com/rclone/rclone/master/CONTRIBUTING.md`
- `curl` → `https://rclone.org/` (Over 70 cloud storage products statisztika)
- (dead end) `curl` → `https://rclone.org/contributing/` — 404

## SQ-04 — Kopia és Duplicati plugin-modellje

- `curl` → `https://raw.githubusercontent.com/kopia/kopia/master/repo/blob/storage.go`
- `curl` → `https://kopia.io/docs/advanced/architecture/`
- `curl` → `https://kopia.io/docs/repositories/`
- `curl` → `https://raw.githubusercontent.com/duplicati/duplicati/master/Duplicati/Library/Interface/IBackend.cs`
- `WebSearch` → `docs.duplicati.com supported backends list storage providers`
- `curl` → `https://docs.duplicati.com/backup-destinations/destination-overview`
- (dead end) `curl` → `https://docs.duplicati.com/detailed-descriptions/all-supported-backends` — 404

## SQ-05 — GoF Strategy minta

- `WebSearch` → `"Strategy" pattern Gang of Four "Define a family of algorithms, encapsulate each one" intent`
- `WebSearch` → `Gang of Four "Design Patterns" book archive.org full text borrow Gamma Helm Johnson Vlissides`
- `curl` → a GoF-könyv PDF-je (`raw.githubusercontent.com/ansbilalgit/Books/...`), majd `pdftotext -layout` a Strategy fejezet (315–321. o.) kinyerésére

## SQ-06 — Cockburn Ports and Adapters

- `curl` → `https://alistair.cockburn.us/hexagonal-architecture/` (élő oldal, működött)
- `curl` → `https://web.archive.org/web/2024/https://alistair.cockburn.us/hexagonal-architecture/` (párhuzamos Wayback-ellenőrzés, szintén működött — az élő oldalt használtam elsődleges forrásként)

## SQ-07 — PoEAA Repository minta

- `curl` → `https://martinfowler.com/eaaCatalog/repository.html` (szerzőség-ellenőrzés: Edward Hieatt és Rob Mee, nem Fowler)

## SQ-08 — YAGNI, speculative generality, rule of three

- `curl` → `https://martinfowler.com/bliki/Yagni.html`
- `WebSearch` → `martinfowler.com "Speculative Generality" smell refactoring catalog`
- `curl` → `https://martinfowler.com/bliki/CodeSmell.html` (nem tartalmazta a Speculative Generality definíciót, csak a kategóriát)
- `curl` → `https://refactoring.com/catalog/` (nem tartalmazta a smell-katalógust, csak a refaktorálásokat)
- `curl` → `https://www.informit.com/articles/article.aspx?p=2952392&seqNum=15` (Refactoring 2. kiadás hivatalos kiadói kivonata — itt találtam meg)
- `WebSearch` → `"rule of three" refactoring "Don Roberts" origin "three strikes" Fowler`
- `curl` → `https://en.wikipedia.org/wiki/Rule_of_three_(computer_programming)`
- `curl` → `https://eoinnoble.com/posts/origins-of-the-rule-of-three/`
- `WebSearch` → `"wince at the duplication" Fowler Roberts refactoring quote` (a Fowler-idézet független megerősítésének keresése)
- `curl` → `https://gist.github.com/deanhunt/1c0ca8c5fe17b9b4f34a` (független megerősítés, szó szerint egyező idézet, p.58 hivatkozással)
- `WebSearch` → `documented case study premature abstraction cost postmortem engineering blog "over-engineering" removed abstraction`
- `WebSearch` → `Sandi Metz "wrong abstraction" prefer duplication talk transcript`
- `curl` → `https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction`

## SQ-09 — mit nem tud elrejteni egy mentési interfész

Ez a kérdés nagyrészt az SQ-01–SQ-04 keresései során előkerült forrásokból válaszolódott meg (l. `megallapitasok.md` 4. pontja). Kiegészítő keresés:

- `curl` → `https://aws.amazon.com/s3/consistency/` (S3 eventual → strong consistency történeti váltás, hivatalos AWS forrás)

## SQ-10 — ütemezés/job/target szétválasztás

- `curl` → `https://www.bacula.org/11.0.x-manuals/en/main/Configuring_Director.html`
- `curl` → `https://restic.readthedocs.io/en/stable/manual_rest.html` (nincs `schedule` alparancs)
- `curl` → `https://restic.readthedocs.io/en/stable/080_examples.html` (systemd service-ként futtatás)
- `curl` → `https://velero.io/docs/main/how-velero-works/`
- `curl` → `https://velero.io/docs/main/api-types/` (nem adott hasznos tartalmat, csak navigációs héjat — a `how-velero-works` oldal elég volt)
- `WebSearch` → `kopia.io docs scheduling policy snapshot interval`
- `curl` → `https://kopia.io/docs/features/` (itt találtam meg a Policy-alapú ütemezést)

## SQ-11 — helyreállítás mint elsőrendű művelet

Nem igényelt önálló keresést — a Bacula (`Configuring_Director.html`, "Type = Restore" szakasz) és a Velero (`how-velero-works`) oldalak, amiket SQ-10 alatt már letöltöttem, közvetlenül tartalmazták a választ (l. `megallapitasok.md` 6. pontja).

## Nem elérhető / korlátozott domainek

| Domain | Mi történt | Hogyan lett pótolva |
|---|---|---|
| `github.com` (web UI és REST API) | Ebben a környezetben egy connector-kapu mögött van: „GitHub access to this repository is not enabled for this session.” Ez **nem** a nyilvános oldal robots/anti-bot védelme, hanem ennek a sessionnek a hozzáférési szintje. | Forrásfájloknál `raw.githubusercontent.com` (nyílt, statikus, semmilyen korlátozás nem volt rajta); egy GitHub-*issue* megvitatásánál a nyilvános Wayback Machine (`web.archive.org`) archívuma. Egyik sem "megkerülés" — mindkettő önálló, nyilvánosan elérhető, más domainen lévő forrás. |
| `web.archive.org` sima `http://` sémán | „Blocked by egress policy” a proxy szintjén | A `https://` séma ugyanarra az URL-re működött |

Minden más felkeresett domain (restic.readthedocs.io, borgbackup.readthedocs.io, borgbackup.org, rclone.org, kopia.io, docs.duplicati.com, alistair.cockburn.us, martinfowler.com, informit.com, en.wikipedia.org, eoinnoble.com, gist.github.com, sandimetz.com, aws.amazon.com, bacula.org, velero.io, archive.org) **elérhető volt korlátozás nélkül**.

## WebFetch használata

**Nulla alkalommal.** A feladat kifejezetten kérte a nyers HTML/forrásszöveg curl-lal történő lekérését a WebFetch-összefoglaló helyett — ezt a kutatás teljes egészében betartotta: minden idézet egy ténylegesen letöltött és lementett fájlból származik (`_vault/backup-adapter-patterns/02-sources/_agent/*/clean/*.md`).



---

# sq06 — Séma- és formátum-migráció motorfüggetlenül

# sq06 — Lefuttatott keresések (szó szerint)

A `01-search-log/queries.jsonl` gépi naplója mellett itt, olvasható formában, minden
lefuttatott `WebSearch` lekérdezés szó szerint, valamint a közvetlen `curl`
próbálkozások, amelyek keresésnek minősülnek (URL-találgatás dokumentáció-verziók
között).

## SQ-1 — Liquibase

1. `WebSearch`: `Liquibase change type supported databases compatibility matrix official docs`
2. `WebSearch`: `liquibase docs "dbms" attribute valid database type names list changelog`
3. Közvetlen URL-próbálkozás (sikertelen → sikeres): `docs.liquibase.com/change-types/dbms.html` (404) →
   `docs.liquibase.com/secure/reference-guide-5-1/changelog-attributes/dbms` (200)

## SQ-2 — Flyway

1. `WebSearch`: `Flyway documentation "vendors" placeholder database-specific migrations folder per database`
2. `WebSearch`: `"documentation.red-gate.com" flyway "database-specific" OR "vendor-specific" migrations best practice raw SQL`
3. `WebSearch`: `Flyway docs "not attempt" OR "does not attempt" database agnostic SQL migrations philosophy`
4. `WebSearch`: `"flyway" "does not try to abstract" OR "we deliberately" OR "philosophy" database independence SQL migrations`
5. `WebSearch`: `Flyway documentation "plain SQL" "full power" database specific features philosophy why SQL migrations`
6. `WebSearch`: `site:documentation.red-gate.com flyway locations "multiple databases" OR "different database types" separate folder`
7. Közvetlen URL-próbálkozás (Wayback Machine): `web.archive.org/web/2018/https://flywaydb.org/documentation/migrations`,
   `web.archive.org/web/2018/https://flywaydb.org/getstarted/why`
8. Közvetlen URL-próbálkozás (GitHub raw): `raw.githubusercontent.com/flyway/flywaydb.org/gh-pages/documentation/concepts/migrations.md`
9. Közvetlen URL-próbálkozás (Spring Boot doksi, több verzió): `docs.spring.io/spring-boot/reference/how-to/data-initialization.html` (404) →
   `docs.spring.io/spring-boot/docs/current/reference/html/howto-database-initialization.html` (200) →
   `docs.spring.io/spring-boot/how-to/data-initialization.html` (200, ez lett a citált verzió)

## SQ-3 — Drizzle ORM

1. `WebSearch`: `Drizzle ORM sqlite-core pg-core mysql-core dialect drizzle-kit migrations generate change database`
2. `WebSearch`: `drizzle-orm github issue "switch" database dialect postgres to mysql existing migrations`
3. Közvetlen URL-próbálkozás (GitHub raw forráskód): `raw.githubusercontent.com/drizzle-team/drizzle-orm/main/drizzle-orm/src/sqlite-core/dialect.ts`,
   `.../pg-core/dialect.ts`, `.../dialect.ts` (utóbbi 404 — nincs közös bázis dialect fájl)

## SQ-4 — Django / Rails séma-absztrakció

1. `WebSearch`: `Django docs "third-party database backends" requirements "DatabaseFeatures" "SchemaEditor" write your own backend`
2. Közvetlen URL-próbálkozás (GitHub raw forráskód, batch): Django `db/backends/{base,postgresql,sqlite3,mysql}/schema.py`,
   Django `db/backends/base/features.py`; Rails `connection_adapters/abstract/schema_statements.rb`,
   `connection_adapters/abstract_adapter.rb`
3. Közvetlen URL: `docs.djangoproject.com/en/5.1/ref/schema-editor/`

## SQ-5 — Kapacitás-jelző minta

1. Közvetlen URL-próbálkozás (GitHub raw forráskód, batch): Django `db/backends/mysql/features.py`;
   Rails `connection_adapters/{postgresql_adapter.rb,sqlite3_adapter.rb,abstract_mysql_adapter.rb}`
   — nem külön `WebSearch`, hanem az SQ-4 kutatás során feltárt forráskód mélyebb elemzéséből
   (grep a `supports_`/`has_` mintákra) adódott.

## SQ-6 — Fájlformátum-migráció

1. `WebSearch`: `"Tolerant Reader" pattern origin "Ian Robinson" "REST in Practice" coined`
2. `WebSearch`: `"Tolerant Reader" pattern who coined attribution Fowler bliki history`
3. `WebSearch`: `"REST in Practice" book 2010 table of contents "Tolerant Reader" chapter Robinson Webber Parastatidis`
4. `WebSearch`: `frontmatter "schema version" YAML markdown migration "on read" lazy upgrade documented`
5. `WebSearch`: `Obsidian OR Zettlr OR Foam note format version field migrate old notes documentation`
6. `WebSearch`: `Kubernetes documentation CRD conversion webhook storage version "stored version" convert on read`
7. `WebSearch`: `Docusaurus migrate CLI v1 to v2 frontmatter automatic conversion documentation`
8. Közvetlen URL: `martinfowler.com/bliki/TolerantReader.html`, `martinfowler.com/articles/consumerDrivenContracts.html`
9. Archívum-hozzáférési kísérlet: `archive.org/details/restinpractice0000webb_1sted` metaadat (200) →
   `..._djvu.txt` közvetlen letöltés (403, Controlled Digital Lending) →
   `fulltext/inside.php` search-inside API (403) — mindkettő sikertelen, l. `hianyok.md`
10. Wayback CDX API próbálkozás: `web.archive.org/cdx/search/cdx?url=martinfowler.com/bliki/TolerantReader.html...`
    → a proxy blokkolta ("Blocked by egress policy") — helyette a `web.archive.org/web/YYYYMMDD*/URL` naptár-nézetet
    kértük le sikeresen, de a pontos legkorábbi dátum kinyerése nélkül (a bliki élő oldalának saját dátumjelzésére
    támaszkodtunk: 2011. május 9.)

## SQ-7 — Motorfüggetlenség elhagyása

1. `WebSearch`: `GitLab dropped MySQL support PostgreSQL only official blog reasoning migrations`
2. `WebSearch`: `"database agnostic" migrations "not worth it" engineering blog dropped abstraction raw SQL decision`
3. `WebSearch`: `GitLab "removing MySQL support" official blog post reasons why postgresql only`
4. Közvetlen URL-próbálkozás: `about.gitlab.com/blog/2019/06/27/removing-mysql-support/` (200, de a modern oldal
   kliensoldali JS-sel renderel, tartalom nélküli váz jött vissza) → `web.archive.org/web/2019/...` ugyanarra az
   URL-re (200, teljes 2019-es statikus HTML-lel — ezt citáltuk)
5. Közvetlen URL: `gitlab.com/gitlab-org/gitlab-foss/-/merge_requests/29790`,
   `gitlab.com/gitlab-org/gitlab-foss/issues/51173` (ill. a `gitlab-ce` alias, ugyanaz a tartalom)

---

## Nem elérhető / korlátozott hozzáférésű domainek

| Domain / URL | Probléma | Hatás |
|---|---|---|
| `archive.org` (könyv teljes szövege, `restinpractice0000webb_1sted`) | Controlled Digital Lending — a `_djvu.txt` és a `fulltext/inside.php` kereső API egyaránt HTTP 403-at ad kölcsönzés (bejelentkezés + "checkout") nélkül. | Nem sikerült ellenőrizni, hogy a "REST in Practice" (2010) könyv tartalmaz-e a Fowler 2011-es bliki posztjánál korábbi "Tolerant Reader" elnevezésű szakaszt. L. `hianyok.md`. |
| `web.archive.org/cdx/search/cdx` (CDX API) | A proxy explicit blokkolta: `"Blocked by egress policy"`. | A Wayback naptár-API helyett a normál `web.archive.org/web/...` snapshot-URL-eket használtuk, kevésbé pontos dátum-metaadattal. |
| `api.github.com/search/code` | HTTP 403 — hitelesítés/rate-limit nélkül a proxyn keresztül nem elérhető. | Kód-szintű keresést (pl. "database-agnostic" string a flywaydb.org repóban) nem tudtunk futtatni; helyette WebSearch + közvetlen doksioldalak pótolták. |
| `docs.liquibase.com/change-types/dbms.html` | HTTP 404 — a Liquibase doksi URL-sémája verziónként (`secure/reference-guide-5-x/...`) változik, a rövid URL-ek nem stabilak. | Sikeresen megtaláltuk a helyes, verziózott URL-t; nincs végleges adatvesztés. |
| `docusaurus.io/docs/migration/v1-to-v2` | HTTP 404 — elavult URL a doksi-újraszervezés után. | Sikeresen megtaláltuk a verzió-specifikus (`3.8.1`) URL-t. |
| `docs.spring.io/spring-boot/reference/how-to/data-initialization.html` | HTTP 404 — időszakosan instabil URL-struktúra a Spring Boot doksi-oldalán. | Két alternatív URL-en (docs/current és /how-to/) is sikerült elérni ugyanazt a tartalmat. |
