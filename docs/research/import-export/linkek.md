# Linkek — import és export kutatás (K-03)

Forrás: `.research/import-export/sq01..sq04/links.md`. A tier-jelölések változatlanul, az egyes
al-kérdés saját skálája szerint vannak átvéve (SQ-01 és SQ-04: T1–T3; SQ-02: T1–T6; SQ-03: T0–T3
— ld. az adott al-kérdés saját tier-meghatározását lent). Az azonosító formátuma: `SQxx-Lnn`.

---

## A) Feldolgozott, felhasznált források

### SQ-01 — Markdown-tudástárak export-formátumai

Tier-skála: T1 = hivatalos dokumentáció/forráskód/spec · T2 = jó minőségű másodlagos (pl. hivatalos
fórum részletes válasza) · T3 = fórum, vélemény, marketing.

| ID | URL | Cím / mit ad | Tier | Mire volt jó |
|---|---|---|---|---|
| SQ01-L01 | https://obsidian.md/help/properties | Obsidian — Properties (frontmatter) hivatalos doksi | T1 | A YAML frontmatter szintaxisa és az alapértelmezett mezők (tags, aliases, cssclasses) leírása |
| SQ01-L02 | https://obsidian.md/help/attachments | Obsidian — Attachments hivatalos doksi | T1 | Igazolja, hogy a csatolmányok sima fájlok a vault-fában |
| SQ01-L03 | https://github.com/obsidianmd/obsidian-help/blob/master/en/Files%20and%20folders/Manage%20vaults.md | Obsidian — Manage vaults (help-repo) | T1 | Igazolja: a vault mozgatása fájlrendszer-másolás, nincs formális export-lépés |
| SQ01-L04 | https://github.com/zoni/obsidian-export | obsidian-export CLI (Rust) README | T1 | Bizonyíték arra, hogy az Obsidian natív markdown-ja (wikilink/embed) külön konverzió nélkül nem "sima" markdown |
| SQ01-L05 | https://github.com/logseq/docs/blob/master/pages/Properties.md?plain=1 | Logseq — Properties dokumentáció | T1 | A `kulcs:: érték` property-szintaxis igazolása (nem YAML frontmatter) |
| SQ01-L06 | https://raw.githubusercontent.com/logseq/logseq/master/deps/db/src/logseq/db/sqlite/export.cljs | Logseq DB-gráf EDN export forráskódja | T1 | Az EDN-export docstringjének szó szerinti idézete, graph-agnosztikus exportformátum |
| SQ01-L07 | https://deepwiki.com/logseq/logseq/6.2-graph-import-and-export | Logseq — AI-generált kódösszefoglaló (deepwiki) | T3 | Csak vezetésre/keresztellenőrzésre; a zip-backup export állítás innen származik, forráskóddal nem igazolt |
| SQ01-L08 | https://joplinapp.org/help/apps/import_export/ | Joplin — Import/Export hivatalos doksi | T1 | JEX (tar) vs. RAW (könyvtár) megkülönböztetés, "lossless" állítás |
| SQ01-L09 | https://github.com/laurent22/joplin/blob/dev/readme/apps/import_export.md | Joplin import/export doksi forrás-repója | T1 | Megerősíti a fenti hivatalos oldal tartalmát |
| SQ01-L10 | https://discourse.joplinapp.org/t/export-summary-what-each-option-does/48564 | Joplin Discourse — "Export Summary: what each option does" | T2 | Részletes, technikailag konzisztens leírás minden export-opcióról (RAW ID-alapú nevek, MD metaadat-vesztés) |
| SQ01-L11 | https://github.com/laurent22/joplin/issues/5224 | Joplin GitHub issue — MD+Frontmatter export terve | T1 | A front matterbe kerülő mezők explicit listája és a tudatosan elhagyott mezők (ID, ütközés-állapot) |
| SQ01-L12 | https://github.com/laurent22/joplin/issues/3473 | Joplin GitHub issue — fájlnév-duplikáció MD exportnál | T1 | Bizonyíték a cím-alapú fájlnevezés kockázatára |
| SQ01-L13 | https://www.notion.com/help/export-your-content | Notion — Export your content hivatalos súgó | T1 | Formátum (MD/CSV), korlátok, csatolmányok, mappaszerkezet; a "nem re-importálható" kulcsmondat |
| SQ01-L14 | https://developers.notion.com/reference/page | Notion API-referencia — Page objektum | T1 | Igazolja, hogy created_time/last_edited_time API-szinten létezik (de export-szinten nem megerősített) |
| SQ01-L15 | https://docs.zettlr.com/en/export/ | Zettlr — Export hivatalos doksi | T1 | A Textbundle/Textpack ajánlása mellékletes megosztáshoz |
| SQ01-L16 | https://wiki.dendron.so/notes/ffec2853-c0e0-4165-a368-339db12c8e4b/ | Dendron — Frontmatter hivatalos wiki-oldal | T1 | Alapértelmezett mezők (id, title, updated, created) leírása |
| SQ01-L17 | https://github.com/dendronhq/dendron/issues/3928 | Dendron GitHub issue — frontmatter elvész exportnál | T1 | Nyitott hiányosság: a markdown pod export nem viszi át a frontmattert |
| SQ01-L18 | https://github.com/foambubble/foam | Foam — hivatalos README | T1 | Data-ownership elv; nincs dedikált export, mert a mappa maga a natív formátum |
| SQ01-L19 | http://textbundle.org/spec/ | TextBundle specifikáció | T1 | A `.textbundle`/`.textpack` és az `info.json` manifeszt leírása |
| SQ01-L20 | https://vault-ld.org/ | Vault-LD projektoldal | T1 | Niche, RDF-alapú markdown-csereformátum-kísérlet (v0.5.0) |
| SQ01-L21 | https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing | Google Cloud Blog — OKF bejelentés | T1 | Az Open Knowledge Format specifikáció bemutatása (markdown+YAML mappa AI-ügynököknek) |
| SQ01-L22 | https://cloud.google.com/blog/products/data-analytics/okf-v0-2-adds-trust-signals/ | Google Cloud Blog — OKF v0.2 | T1 | A v0.2 bizalmi/proveniencia-mezők hozzáadása, visszafelé kompatibilitás |
| SQ01-L23 | https://raw.githubusercontent.com/GoogleCloudPlatform/knowledge-catalog/main/okf/SPEC.md | OKF v0.2 specifikáció szövege | T1 | A kötelező `type` mező, fenntartott fájlnevek (`index.md`, `log.md`) |
| SQ01-L24 | https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/README.md | OKF repó README | T1 | A SPEC.md-re mutató kontextus (korlátozottan felhasznált) |
| SQ01-L25 | https://alexop.dev/posts/open-knowledge-format-markdown-frontmatter-agent-knowledge/ | Személyes blog az OKF-ről | T3 | Csak vezetésre használva (innen jutott el a kutatás a hivatalos Google Cloud Blogig), érdemi állítás nem innen |

### SQ-02 — Ütközéskezelés importnál

Tier-skála (a projekt szabálya szerint kiterjesztett): T1 = nyílt/közösségi spec-jellegű dokumentáció
(POSIX/man page, GNU, git, PostgreSQL, SQLite, GNOME HIG) · T2 = lektorált tudományos publikáció ·
T3 = hivatalos gyártói/projekt dokumentáció saját termékről (Dropbox, Obsidian, Anki, Nextcloud,
Terraform, Flyway, NNGroup) · T4 = gyártói/mérnöki blog, informális önbeszámoló · T5 =
aggregátor/tercier (AI-összefoglaló) · T6 = fórum/GitHub-issue nem igazolt szerzőtől, hivatalos
domainen is.

| ID | URL | Cím / mit ad | Tier | Mire volt jó |
|---|---|---|---|---|
| SQ02-L01 | https://help.dropbox.com/organize/conflicted-copy | Dropbox — Conflicted copy súgócikk | T3 | "Conflicted copy" elnevezési minta, kézi feloldás ajánlása |
| SQ02-L02 | https://www.nngroup.com/articles/confirmation-dialog/ | NNGroup — Confirmation Dialogs Can Prevent User Errors | T3 | Megerősítő dialógus ajánlások; a cikk maga jelzi, hogy nincs mögötte kvantitatív kutatás |
| SQ02-L03 | https://www.nngroup.com/articles/proximity-consequential-options/ | NNGroup — Dangerous UX: Consequential Options Close to Benign Options | T3 | Destruktív és ártalmatlan opciók térbeli/vizuális elválasztásának ajánlása |
| SQ02-L04 | https://www.gnu.org/software/coreutils/manual/html_node/Backup-options.html | GNU coreutils kézikönyv — Backup options | T1 | `cp --backup` numbered/simple mód pontos mechanizmusa |
| SQ02-L05 | https://man7.org/linux/man-pages/man1/cp.1.html | `cp` man page | T1 | `-n`/`--no-clobber`, `-i`, alapértelmezett felülírás pontos szövege |
| SQ02-L06 | https://discourse.joplinapp.org/t/importing-jex-while-file-system-sync-is-enabled-causes-duplicate-notes-no-id-collision-handling/48458.json | Joplin Discourse — ID-ütközés hiánya JEX importnál | T6 | Konkrét, névvel/verzióval ellátott felhasználói panasz a hiányzó ütközéskezelésről |
| SQ02-L07 | https://github.com/laurent22/joplin/issues/537 | Joplin GitHub issue — duplikált notebook importnál | T6 | Elvárt (de nem létező) import-összegző üzenet leírása |
| SQ02-L08 | https://sqlite.org/atomiccommit.html | SQLite — Atomic Commit hivatalos doksi | T1 | Tranzakció-atomicitás "all-or-nothing" garanciája |
| SQ02-L09 | https://docs.stripe.com/api/idempotent_requests | Stripe API — Idempotent requests | T3 | Kliens-generált idempotencia-kulcs minta |
| SQ02-L10 | https://docs.ankiweb.net/importing/text-files.html | Anki kézikönyv — Importing text files | T3 | GUID/első-mező alapú duplikátum-kezelés, frissítés vs. új jegyzet |
| SQ02-L11 | https://www.postgresql.org/docs/current/sql-insert.html | PostgreSQL — INSERT dokumentáció | T1 | `ON CONFLICT DO NOTHING`/`DO UPDATE` (upsert) pontos szintaxisa és atomicitása |
| SQ02-L12 | https://developer.hashicorp.com/terraform/cli/commands/plan | Terraform — `plan` parancs doksi | T3 | Dry-run/előnézet minta infrastruktúra-kontextusban |
| SQ02-L13 | https://help.nextcloud.com/t/auto-rename-if-file-already-exists/114905 | Nextcloud fórum — auto-rename feature request | T6 | Szerver-oldali blokkoló viselkedés (2021) és a felhasználói elégedetlenség dokumentálása |
| SQ02-L14 | https://developer.gnome.org/hig/patterns/feedback/dialogs.html | GNOME HIG — Dialogs | T1 | Az undo elsőbbsége a megerősítő dialógussal szemben (közösségi tervezési szabvány) |
| SQ02-L15 | https://devblogs.microsoft.com/oldnewthing/20190604-00/?p=102539 | Microsoft "Old New Thing" blog | T4 | Windows fájlmásolás-ütközés numerikus utótag-opciójának létezése |
| SQ02-L16 | https://learn.microsoft.com/id-id/archive/blogs/b8/designing-the-windows-8-file-name-collision-experience | Windows 8 tervezési blog — fájlnév-ütközés élmény | T4 | Konkrét, tesztelt (RITE/eye-tracking) usability-döntés: nincs alapértelmezett kiválasztás |
| SQ02-L17 | https://link.springer.com/article/10.1007/s10664-019-09735-4 | Brindescu et al. 2020, Empirical Software Engineering | T2 | Egyetlen ténylegesen mért adat: kézi merge-ütközésfeloldás 26x nagyobb hibaaránnyal jár |
| SQ02-L18 | https://raw.githubusercontent.com/nextcloud/documentation/master/user_manual/desktop/conflicts.rst | Nextcloud desktop kliens kézikönyv | T3 | "Conflicted copy YYYY-MM-DD" elnevezési minta, kézi feloldás |
| SQ02-L19 | https://git-scm.com/docs/git-merge#_how_conflicts_are_presented | git — merge dokumentáció | T1 | Soronkénti kézi ütközésfeloldás jelölőinek hivatalos leírása |
| SQ02-L20 | https://github.com/flyway/flywaydb.org/blob/gh-pages/documentation/concepts/dryruns.md | Flyway — Dry Runs dokumentáció | T3 | Dry-run mint SQL-fájl generálás alkalmazás nélkül |
| SQ02-L21 | https://rsync.samba.org/ftp/rsync/rsync.1 | rsync man page | T1 | `--dry-run`, `--ignore-existing`, `--backup` hivatalos leírása |
| SQ02-L22 | https://deepwiki.com/obsidianmd/obsidian-help/2.3-synchronization-and-conflict-resolution | Obsidian Sync — AI-generált összefoglaló (deepwiki) | T5 | Csak orientációra; később hivatalos forrással megerősítve |
| SQ02-L23 | https://obsidian.md/help/sync/settings | Obsidian Sync — Settings hivatalos doksi | T3 | "Conflict resolution" beállítás (automatikus egyesítés alapértelmezett) |
| SQ02-L24 | https://obsidian.md/help/sync/troubleshoot | Obsidian Sync — Troubleshoot hivatalos doksi | T3 | Automatikus egyesítés vs. konfliktusfájl-létrehozás elnevezési mintája |
| SQ02-L25 | https://www.postgresql.org/docs/current/app-pgrestore.html | PostgreSQL — pg_restore dokumentáció | T1 | `--clean`/`--if-exists` (teljes felülírás) és `--list` (előnézet) |
| SQ02-L26 | https://man7.org/linux/man-pages/man2/rename.2.html | POSIX `rename()` man page | T1 | A "temp fájlba írás + átnevezés" atomicitási minta alapja |

### SQ-03 — Személyes adat exportja (GDPR)

Tier-skála: T1 = maga a jogszabály szövege (EUR-Lex) vagy hivatalos EDPB/WP29/termék-dokumentáció ·
T2 = hiteles mirror, hatósági útmutató (nem maga a jogszabály), szakmai elemzés · T3 = jó hírű
másodlagos forrás · T0 = marketing/SEO-blog, nem használt idézetre.

| ID | URL | Cím / mit ad | Tier | Mire volt jó |
|---|---|---|---|---|
| SQ03-L01 | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679 | GDPR hivatalos konszolidált szövege (EN) | T1 | A 15., 20. cikk és a (63), (68) preambulumbekezdés szó szerinti szövege |
| SQ03-L02 | https://ec.europa.eu/newsroom/dae/redirection/document/44099 | WP29 WP242 rev.01 hivatalos PDF | T1 | Az adathordozhatósági iránymutatás teljes szövege (provided vs. inferred, formátum-ajánlás) |
| SQ03-L03 | https://ec.europa.eu/newsroom/article29/item-detail.cfm?item_id=611233 | WP242 rev.01 hivatalos listaoldala | T1 | Dátum és referenciaszám megerősítése |
| SQ03-L04 | https://edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-right-data-portability-under-regulation-2016679_en | EDPB oldal — WP242 jóváhagyása | T1 | Az EDPB általi formális jóváhagyás (endorsement) igazolása |
| SQ03-L05 | https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-erasure/ | ICO — Right to erasure hivatalos útmutató | T1 | Igazolja: nincs benne export-előfeltétel a törléshez (evidence of absence) |
| SQ03-L06 | https://support.google.com/accounts/answer/3024190?hl=en | Google Takeout hivatalos súgó | T1 | Formátum, szerkezet, méret/élettartam-korlát, "nem törli az adatot" figyelmeztetés |
| SQ03-L07 | https://docs.github.com/en/migrations/using-ghe-migrator/exporting-migration-data-from-githubcom | GitHub — migrációs export doksi | T1 | tar.gz formátum, letöltési mód |
| SQ03-L08 | https://docs.github.com/en/enterprise-cloud@latest/get-started/archiving-your-github-personal-account-and-public-repositories/requesting-an-archive-of-your-personal-accounts-data | GitHub — személyes fiók archívum doksi | T1 | Méretkorlát (20 GB), 7 napos élettartam |
| SQ03-L09 | https://docs.github.com/en/account-and-profile/how-tos/account-management/deleting-your-personal-account | GitHub — fiók törlése doksi | T1 | Mentési ajánlás törlés előtt; nincs technikai gát export nélkül |
| SQ03-L10 | https://slack.com/help/articles/220556107-How-to-read-Slack-data-exports | Slack export hivatalos súgó | T1 | JSON/TXT export szerkezete, mezők, fájlnevek |
| SQ03-L11 | https://dtinit.org/docs/dtp-intro-for-contributors | Data Transfer Initiative hivatalos doksi | T1 | A Data Transfer Project állapota, adatkategóriák, demó ≠ éles rendszer |
| SQ03-L12 | https://developers.google.com/data-portability | Google Data Portability API doksi | T1 | Google saját állítása a portability API-járól (vállalati elsődleges forrás) |
| SQ03-L13 | https://www.bvdnet.de/wp-content/uploads/2022/03/Guidelines-on-the-right-to-data-portability.pdf | Harmadik fél mirror a WP242-ről | T2 | Csak keresztellenőrzésre, idézetre a hivatalos PDF-et használtuk |

### SQ-04 — Tömeges behozatal indexelt rendszerbe

Tier-skála: T1 = hivatalos dokumentáció/forráskód/spec/CWE-MITRE · T2 = jó másodlagos (szakmai, de
nem hivatalos szabvány/gyártói doksi) · T3 = fórum, vélemény, marketing. Gyártói teljesítményállítás
saját termékről NEM T1.

| ID | URL | Cím / mit ad | Tier | Mire volt jó |
|---|---|---|---|---|
| SQ04-L01 | https://security.snyk.io/research/zip-slip-vulnerability | Snyk — Zip Slip Vulnerability kutatási oldal | T1 | A Zip Slip sebezhetőségi osztály kanonikus, névvel ellátott leírása |
| SQ04-L02 | https://github.com/snyk/zip-slip-vulnerability | Zip Slip PoC-kódtár | T1 | Sebezhető minta (Java) és a javítási minta bemutatása |
| SQ04-L03 | https://cwe.mitre.org/data/definitions/22.html | CWE-22 — Path Traversal | T1 | A path traversal hivatalos taxonómiája és mitigációja (kanonikus útvonal-feloldás) |
| SQ04-L04 | https://cwe.mitre.org/data/definitions/409.html | CWE-409 — Improper Handling of Highly Compressed Data | T1 | Dekompressziós bomba hivatalos definíciója és mitigációja |
| SQ04-L05 | https://www.sqlite.org/fts5.html | SQLite — FTS5 hivatalos doksi | T1 | automerge/usermerge/crisismerge/merge/optimize parancsok és paraméterek |
| SQ04-L06 | https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html | Elasticsearch — Bulk API doksi | T1 | Elemenkénti (`items` tömb) válaszstruktúra, HTTP kérésméret-korlát |
| SQ04-L07 | https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk | Elasticsearch — Bulk API-referencia | T1 | Kiegészítő API-referencia a bulk endpointhoz |
| SQ04-L08 | https://www.elastic.co/docs/deploy-manage/production-guidance/optimize-performance/indexing-speed | Elasticsearch — Indexing speed teljesítmény-útmutató | T1 | `refresh_interval=-1`, replikák kikapcsolása tömeges betöltésnél |
| SQ04-L09 | https://dev.mysql.com/doc/refman/8.4/en/load-data.html | MySQL 8.4 — LOAD DATA referencia | T1 | `IGNORE` opció hatása részleges hibára |
| SQ04-L10 | https://www.postgresql.org/docs/current/sql-copy.html | PostgreSQL — COPY dokumentáció | T1 | Hiba esetén a beírt sorok "deleted state"-be kerülnek, VACUUM szükséges |
| SQ04-L11 | https://tus.io/protocols/resumable-upload | tus resumable upload protokoll spec | T1 | Offset-alapú folytatási mechanizmus (HEAD → Upload-Offset) |
| SQ04-L12 | https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github | GitHub — nagy fájlok doksi | T1 | 50 MiB figyelmeztetés, 100 MiB tiltás, repó-méret ajánlás |
| SQ04-L13 | https://docs.pypi.org/project-management/storage-limits/ | PyPI — Storage limits doksi | T1 | 100 MB/fájl, 10 GB/projekt alapértelmezett korlát; yank vs. törlés különbsége |
| SQ04-L14 | https://docs.github.com/en/rest/migrations/source-imports?apiVersion=2022-11-28 | GitHub — Source imports REST API doksi | T1 | Fázis-állapotgép (`status`) és számszerű haladás (`percent`) egy hosszú futású importnál |
| SQ04-L15 | https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html | AWS S3 — Multipart upload doksi | T1 | Rész-alapú újrapróbálkozás, `ListParts` állapot-lekérdezés |
| SQ04-L16 | https://restic.readthedocs.io/en/stable/faq.html | restic — hivatalos GYIK | T1 | Tartalom-címzett darabolás + periodikus checkpoint-index minta |
| SQ04-L17 | https://clig.dev/ | Command Line Interface Guidelines | T2 | Közösségi irányelv hosszú futású folyamatok visszajelzésére (progress/spinner) |

---

## B) Felderített, de meg nem nyitott linkek

### SQ-01

| URL | Tier | Megjegyzés |
|---|---|---|
| https://obsidian.md/help/import-export | T1 (elérés sikertelen) | "File import-export.md does not exist" hiba |
| https://docs.rs/obsidian-export | — | Csak keresési találat |
| https://forum.obsidian.md/t/moving-notes-with-attachments-to-new-vault/66869 | T3 | Csak keresési találat (fórum) |
| https://raccoon.page/blog/export-obsidian-vault/ | T3 | Content-farm jellegű, nem használt |
| https://docs.logseq.com | T1 (elérés sikertelen) | Üres/beolvashatatlan tartalom |
| https://github.com/logseq/docs/blob/master/pages/Page%20properties.md | — | 404, hibás útvonal |
| https://github.com/logseq/logseq/issues/4211 | T1 (nem fetch-elve) | "Export Graph to EDN inserts some gratuitous text" — csak cím szerint azonosítva |
| https://discuss.logseq.com/t/an-idea-for-a-more-standard-markdown-property-syntax/20073 | T3 | Csak keresési találat |
| https://github.com/logseq/rdf-export | T1 (nem fetch-elve) | Csak keresési találat |
| https://discourse.joplinapp.org/t/export-the-correct-command-syntax-for-exporting-note-as-jex-format/870 | T3 | Csak keresési találat |
| https://discourse.joplinapp.org/t/export-to-jex-or-raw/36622 | T3 | Csak keresési találat |
| https://discourse.joplinapp.org/t/pb-accented-characters-in-toc/7556 | T3 | Ékezetes karakter probléma, nem fetch-elve |
| https://github.com/laurent22/joplin/issues/7970 | T1 (nem fetch-elve) | "problems when exporting markdown and attachments with spaces" |
| https://github.com/laurent22/joplin/issues/853 | T1 (nem fetch-elve) | "Bug with filename charset on export under Windows" |
| https://github.com/laurent22/joplin/issues/316 | T1 (nem fetch-elve) | "Export Human-readable Filenames and Folders" |
| https://discourse.joplinapp.org/t/strange-file-names-in-resource-folder/36586 | T3 | Csak keresési találat |
| https://deepwiki.com/laurent22/joplin/5.5-content-import-and-export | T3 | Csak keresési találat |
| https://fileinfo.com/extension/jex | T3 | Generikus fájltípus-oldal |
| https://en.wikipedia.org/wiki/Joplin_(software) | T3 | Csak keresési találat |
| https://noteforms.com/resources/notion-export | T3 | Content-marketing |
| https://www.breeze.pm/articles/export-from-notion | T3 | Csak keresési találat |
| https://raccoon.page/blog/notion-export-limitations/ | T3 | Content-farm gyanús |
| https://unmarkdown.com/blog/notion-export-broken | T3 | Csak keresési találat |
| https://restora.cc/blog/what-notion-export-leaves-behind | T3 | Csak keresési találat |
| https://mdstill.com/blog/notion-markdown-export-quirks | T3 | Csak keresési találat |
| https://clonepartner.com/blog/definitive-guide-notion-data-export-api-pdf-html | T3 | Csak keresési találat |
| https://github.com/CherryHQ/cherry-studio/issues/11384 | T1 (nem fetch-elve) | "Notion export missing content" bug |
| https://docs.zettlr.com/en/first-time-users/exporting-files/ | T1 (nem fetch-elve) | Csak keresési találat |
| https://github.com/dendronhq/dendron/issues/541 | T1 (nem fetch-elve) | "Markdown Export Pod" |
| https://github.com/dendronhq/dendron/issues/309 | T1 (nem fetch-elve) | "Robust exporting to plain markdown directories" |
| https://foambubble.github.io/foam/ → https://docs.foam.md/ | T1 (redirect, nem követve) | Nem néztük meg a végleges célt |
| https://github.com/foambubble/foam/blob/master/docs/user/features/note-metadata.md | T1 (elérés sikertelen) | 404 |
| https://github.com/textbundle/textbundle.org | T1 (nem fetch-elve) | A spec forrás-repója |
| https://blog.ulysses.app/introducing-textbundle/ | T1/T2 (nem fetch-elve) | Gyártói bejelentés |
| https://zerokspot.com/weblog/2020/05/15/working-with-textbundles/ | T3 | Személyes blog, nem használt |
| https://github.com/The-Knowledge-Graph-Guys/vault-ld | T1 (nem fetch-elve) | A Vault-LD GitHub repója |
| https://github.com/GoogleCloudPlatform/open-knowledge-format | T1 (nem fetch-elve) | Külön repó, nem vizsgálva |
| https://okf.md/faq/ | T3/ismeretlen (elérés sikertelen) | "Too many redirects" hiba |
| https://okf.md/spec/ | T3/ismeretlen (nem fetch-elve) | Nem hivatalos Google-domain |
| https://suganthan.com/blog/open-knowledge-format/ | T3 | Csak keresési találat |
| https://www.startuphub.ai/ai-news/insights/2026/google-open-knowledge-format-okf-explained-2026 | T3 | Csak keresési találat |
| https://groundingpage.com/facts/open-knowledge-format/ | T3 | Content-farm gyanús |
| https://witscode.com/open-knowledge-format | T3 | Csak keresési találat |
| https://www.marktechpost.com/2026/06/16/google-cloud-introduces-open-knowledge-format-okf... | T3 | Tech-hír oldal, nem fetch-elve |
| https://www.gitbook.com/blog/what-is-okf-open-knowledge-format | T3 | Csak keresési találat |
| https://medium.com/@tahirbalarabe2/what-is-open-knowledge-format-okf-270b20791802 | T3 | Csak keresési találat |
| toolfinder.com, lumanote.org, stik.ink, turnwall.com és "Best PKM/Markdown App" listázó cikkek | T3 | Marketing/roundup jellegű, nem használt |

### SQ-02

| URL | Tier | Megjegyzés |
|---|---|---|
| https://github.com/nextcloud/documentation/blob/master/user_manual/desktop/conflicts.rst | T3 | GitHub-renderelt nézet (a raw verzió lekérve) |
| https://github.com/nextcloud/server/issues/12217 | T6 | Nextcloud szerver-oldali név-ütközés issue |
| https://forum.obsidian.md/t/robust-sync-conflict-resolution/93544 | T6 | Közösségi vita robusztusabb ütközéskezelésről |
| https://community.obsidian.md/plugins/conflict-manager | T6 | Harmadik feles plugin — jelzi a beépített mechanizmus elégtelenségét egyeseknek |
| https://forums.ankiweb.net/t/import-duplicate-handling/52167 | T6 | Anki közösségi vita a duplikátum-kezelésről |
| https://www.dropboxforum.com/discussions/101001014/what-to-do-with-conflicted-copies/193060 | T6 | Dropbox közösségi fórum |
| https://www.se.cs.uni-saarland.de/publications/docs/VHF+22.pdf | T2 (nem feldolgozva) | "Challenges of Resolving Merge Conflicts: A Mining and Survey Study" |
| https://arxiv.org/pdf/2102.11307 | T2 (nem feldolgozva) | "Automatic Detection and Resolution of Software Merge Conflicts" |
| https://dada.cs.washington.edu/research/tr/2014/05/UW-CSE-14-05-02.PDF | T2 (nem feldolgozva) | MetaSync — fájlszinkronizációs kutatási jelentés |
| https://ennanzhai.github.io/pub/fast20-cloudconflict.pdf | T2 (nem feldolgozva) | FAST'20 "Lock-Free Collaboration Support for Cloud Storage Services" |
| https://conservancy.umn.edu/items/7b8f7759-b31b-4740-8646-11dff64407b6 | T2 (nem feldolgozva) | Dropbox-esettanulmány felhasználói együttműködésről |
| https://help.nextcloud.com/t/avoid-creating-local-conflicted-copy-files-always-take-server-version-overwrite-local/175699 | T6 | Csak találati listában, nem nyitva |
| https://developer.apple.com/design/human-interface-guidelines/alerts | T3 (blokkolt) | JavaScript-render szükséges, nem sikerült kinyerni |
| https://api.github.com/search/code?q=... | — | 403, hitelesítés nélkül nem elérhető |

### SQ-03

| URL | Tier | Megjegyzés |
|---|---|---|
| https://net.jogtar.hu/jogszabaly?docid=a1600679.eup | T2 (blokkolt) | ROBOTS_DISALLOWED — magyar jogszabálytár |
| https://cdn.digitaleurope.org/uploads/2019/01/Position%20Paper%20...WP%20242.pdf | T2 | DIGITALEUROPE iparági lobbi-álláspont, nem lekérve |
| https://www.technethics.com/wp29s-revised-guidelines-on-the-right-to-data-portability/ | T2 | Szakmai blogösszefoglaló, nem lekérve |
| https://www.i-scoop.eu/right-to-data-portability/ | T2 | Szakmai cikk, nem lekérve |
| https://www.cpomagazine.com/data-protection/access-erasure-portability-examining-data-subject-rights-gdpr/ | T2 | Szakmai cikk a 15/17/20. cikk viszonyáról, nem lekérve |
| https://medium.com/@sohail_saifii/gdpr-implementation-building-data-deletion-and-export-apis-that-actually-work-833b34eb09f6 | T2 | Fejlesztői blog, nem lekérve |
| https://gdprlocal.com/right-to-data-portability/ | T2 | Szakmai cikk, nem lekérve |
| https://en.wikipedia.org/wiki/Data_Transfer_Project | T3 | Wikipedia-összefoglaló, helyette a hivatalos dtinit.org forrás használva |
| https://github.com/dtinit/data-transfer-project | T2 | DTP forráskód-repó, nem lekérve részletesen |
| https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX%3A62021CJ0487 | T1 (nem vizsgálva) | Egy CJEU-ítélet az Art.15 kapcsán — kívül esett a kutatás keretén |
| gdpr-info.eu, gdpr-text.com, privacy-regulation.eu, legiscope.com, advisera.com, clarip.com, gdpr.eu.org, cms-digitallaws.com, luxgap.com | T0/T3 | Art.15/Art.20 "mirror" oldalak — szándékosan nem idézve, helyettük az EUR-Lex hivatalos szöveg |
| androidpolice.com, hackmag.com, en.wikipedia.org/wiki/Google_Takeout, recoverytools.com, arysontechnologies.com | T0/T3 | Google Takeout témában, helyettük support.google.com hivatalos oldal |
| mimecast.com (2 cikk), github.com/omgitsjessie/slack-exports, trailhead.salesforce.com, techresolve.blog, dev.to, usecarly.com | T0/T3 | Slack export témában, helyettük slack.com hivatalos súgó |
| i-scoop.eu, cpomagazine.com, elsmar.com fórum, gdpr-advisor.com, termsbox.com, recordinglaw.com, gdpreu.org, probackup.io, reform.app, axonbuild.com | T0/T3 | Törlés+export kérdésben, nem hoztak új hivatalos állítást |
| teachprivacy.com, privacyresources.eu | T0/T3 | EDPB-dokumentum-gyűjtő oldalak, csak navigációra |
| dtinit.org/policy, dtinit.org/blog | T1 (nem lekérve) | Időkorlát miatt nem részletezve |
| eur-lex.europa.eu (magyar nyelvű GDPR-változatok, HU/TXT, HU/LSU) | T1 (nem lekérve) | A kutatás az angol hivatalos szöveget használta |
| elte.hu adatkezelési tájékoztató PDF, infornax.hu, adatvedelmirendelet.hu (njt.hu) | T0/T3 | Magyar oldalak, nem lekérve |

### SQ-04

| URL | Tier | Megjegyzés |
|---|---|---|
| https://medium.com/@ibm_ptc_security/zip-slip-attack-e3e63a13413f | T3 | Blog, harmadik fél összefoglalója |
| https://safeguard.sh/resources/blog/zip-slip-vulnerability-cheat-sheet | T3 | Marketing blog |
| https://discuss.elastic.co/t/bulk-api-item-error-types/242639 | T3 | Fórum, hivatalos domainen, de nem T1 |
| https://github.com/elastic/elasticsearch/issues/54549 | T2/T3 határ | Issue tracker vita, nem hivatalos dokumentáció |
| https://joplinapp.org/help/apps/import_export/ | T1 (nem lekérve ebben az al-kérdésben) | A keresési snippet nem ígért technikai részletet validálásról |
| https://discourse.joplinapp.org/... | T3 | Közösségi fórum |
| https://forum.restic.net/... | T3 | Közösségi fórum, nem használva |
| https://github.com/aws/aws-sdk-js/issues/1452, https://repost.aws/... | T3 | Fórum/support-kérdés |
| https://gitlab.com/gitlab-org/gitlab/-/issues/* | T3 | Issue tracker, terméktervezési vita |
| https://pentestreports.com/weaknesses/CWE-409, https://turingsecure.com/... | T3 | Harmadik feles CWE-tükrözés, nem az eredeti MITRE oldal |
| npm csomagméret-korlát keresések (docs.npmjs.com) | — | Nem hozott találatot, ld. `hianyok.md` |
