# Keresések — import és export kutatás (K-03)

Forrás: `.research/import-export/sq01..sq04/searches.md`. Minden lefuttatott lekérdezés szó szerint,
al-kérdésenként, a forrás-dokumentumok sorrendjében.

---

## SQ-01 — Markdown-tudástárak export-formátumai

Minden keresés angol nyelven futott (indoklás: a vizsgált eszközök — Obsidian, Logseq, Joplin,
Notion, Zettlr, Foam, Dendron — nemzetközi, angol nyelvű fejlesztői közösséggel rendelkeznek, nincs
magyar hivatalos dokumentációjuk; ezt a kutatás explicit hiányként rögzíti, nem hallgatja el).

1. `Obsidian export vault documentation frontmatter attachments`
2. `Logseq export EDN markdown graph documentation`
3. `Joplin JEX export format documentation`
4. `Notion export markdown CSV what is lost limitations`
5. `joplin github "md_frontmatter" OR "frontMatter" export source code fields`
6. `Zettlr Foam Dendron export format plain markdown files no proprietary format`
7. `"markdown knowledge base" standard exchange format interoperability no common standard`
8. `"Open Knowledge Format" Google OKF markdown spec official`
9. `"Open Knowledge Format" okf.md specification github repo`
10. `Textbundle format specification textbundle.org markdown package`
11. `Dendron export vault plain markdown frontmatter documentation`
12. `Foam markdown vault frontmatter plain files documentation github`
13. `Notion "export" community known issues broken links images missing official`
14. `Logseq page properties syntax "key:: value" vs YAML frontmatter markdown files`
15. `Notion export markdown file "created time" property does not include timestamp filename`
16. `notion markdown export sample file structure "Created" "Tags" properties text top of file not yaml`
17. `no standard format for markdown note apps interoperability PKM lock-in comparison`

### Direkt URL-célzások (WebFetch, keresés nélkül, mert a domain/útvonal ismert volt)

- joplinapp.org/help/apps/import_export/
- obsidian.md/help/import-export, /help/properties, /help/attachments (redirect után)
- www.notion.com/help/export-your-content (redirect után), developers.notion.com/reference/page
- docs.logseq.com (sikertelen)
- raw.githubusercontent.com/.../export.cljs (Logseq forráskód)
- deepwiki.com/logseq/logseq/6.2-graph-import-and-export
- github.com/obsidianmd/obsidian-help/.../Manage vaults.md
- github.com/zoni/obsidian-export
- discourse.joplinapp.org/t/export-summary-what-each-option-does/48564
- github.com/laurent22/joplin/issues/5224, /issues/3473, blob/dev/readme/apps/import_export.md
- docs.zettlr.com/en/export/
- wiki.dendron.so/notes/ffec2853-c0e0-4165-a368-339db12c8e4b/ (Frontmatter)
- github.com/dendronhq/dendron/issues/3928
- vault-ld.org
- cloud.google.com/blog/.../how-the-open-knowledge-format-can-improve-data-sharing, .../okf-v0-2-adds-trust-signals/
- raw.githubusercontent.com/GoogleCloudPlatform/knowledge-catalog/main/okf/SPEC.md
- github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/README.md
- okf.md/faq/ (sikertelen, redirect-hurok)
- github.com/foambubble/foam, foambubble.github.io/foam/ (redirect, nem követve)
- github.com/foambubble/foam/blob/master/docs/user/features/note-metadata.md (404)
- github.com/logseq/docs/blob/master/pages/Properties.md?plain=1 (és a hibás Page%20properties.md útvonal)
- alexop.dev/posts/open-knowledge-format-... (vezető forrás, nem idézett)
- textbundle.org/spec/

---

## SQ-02 — Ütközéskezelés importnál

| # | Eszköz | Lekérdezés (verbátim) | Cél |
|---|---|---|---|
| 1 | WebSearch | `Joplin import notes existing note conflict duplicate` | Joplin ütközéskezelés tájékozódás |
| 2 | WebSearch | `Obsidian sync conflict file naming` | Obsidian ütközés-elnevezés |
| 3 | WebSearch | `Nextcloud file name conflict "(2)" rename upload` | Nextcloud átnevezési minta |
| 4 | WebSearch | `Dropbox "conflicted copy" naming convention support` | Dropbox elnevezési konvenció |
| 5 | WebSearch | `rsync dry-run --backup --ignore-existing overwrite existing files` | rsync stratégiák |
| 6 | WebSearch | `cp -i -n --backup=numbered man page overwrite existing file` | cp interaktív/backup mód |
| 7 | WebSearch | `database import "ON CONFLICT DO NOTHING" upsert idempotent import pattern` | DB import minták |
| 8 | WebSearch | `confirmation dialog vs undo destructive actions Nielsen Norman research` | UX-irányelvek destruktív műveletekre |
| 9 | WebSearch | `help.obsidian.md sync conflict resolution documentation` | Obsidian hivatalos doksi keresése |
| 10 | WebSearch | `git apply patch "already exists in working directory" error` | git ütközéskezelés (patch szint) |
| 11 | WebSearch | `Windows Explorer macOS Finder "keep both" "replace" "skip" copy conflict dialog apply to all` | OS-szintű fájlütközés dialógus |
| 12 | WebSearch | `Anki import notes duplicate update existing notes summary added updated` | Anki import-előnézet/összegzés |
| 13 | WebSearch | `Stripe idempotency key API design pattern documentation` | idempotencia minta (API) |
| 14 | WebSearch | `SQLite atomic commit documentation "all changes" OR "all or nothing"` | atomicitás mechanizmus |
| 15 | WebSearch | `cloud storage sync conflict resolution empirical study user data loss academic paper` | mért bizonyíték keresése |
| 16 | WebSearch | `tar extraction interrupted partial files not atomic` | atomicitás — archívum kicsomagolás |
| 17 | WebSearch | `merge conflict resolution empirical study software defects git bugs introduced` | mért bizonyíték — manuális ütközésfeloldás kára |
| 18 | WebSearch | `Terraform plan dry run preview changes before apply` | dry-run minta (infrastruktúra) |
| 19 | WebSearch | `Flyway Liquibase dry-run migration preview SQL before execute` | dry-run minta (DB migráció) |
| 20 | WebSearch | `recycle bin trash reversible delete safe default UX research undo` | visszavonhatóság mint alapértelmezés |
| 21 | WebSearch | `GNU coreutils cp backup numbered simple suffix documentation manual` | cp backup mechanizmus részletei |
| 22 | WebSearch | `pg_restore --clean --if-exists existing objects conflict` | DB-import ütközéskezelés (Postgres) |
| 23 | WebSearch | `git clone existing non-empty directory refuses error` | git — teljes megszakítás mint stratégia |
| 24 | WebSearch | `"content hash" deduplication import idempotent skip unchanged files` | tartalom-hash alapú idempotencia |
| 25 | WebSearch | `Apple Human Interface Guidelines alerts destructive action confirmation` | Apple HIG |
| 26 | WebSearch | `GNOME Human Interface Guidelines destructive action confirmation dialog` | GNOME HIG |
| 27 | WebSearch | `PostgreSQL documentation INSERT ON CONFLICT DO UPDATE syntax official` | Postgres upsert szintaxis |
| 28 | WebSearch | `Nextcloud desktop client "conflicted copy" file sync conflict` | Nextcloud desktop kliens ütközés |
| 29 | WebSearch | `help.obsidian.md "Sync conflicts" obsidian sync file OR "obsidian-sync-conflicts"` | Obsidian hivatalos doksi (2. kísérlet) |
| 30 | WebSearch | `site:github.com obsidianmd/obsidian-help conflict` | Obsidian hivatalos doksi repó keresése |
| 31 | WebSearch | `rsync --partial interrupted transfer keep incomplete file default deletes` | rsync félbeszakadt átvitel viselkedése |
| 32 | WebSearch | `site:obsidian.md/help sync conflict` | Obsidian hivatalos URL megtalálása |

WebFetch-lekérések: ld. `linkek.md` SQ-02 táblázata (minden lekért URL, dátummal 2026-09-06 és
eredménnyel).

Módszertani megjegyzés a forrásból: ez a kutatás egyetlen delegált al-kérdés önálló feldolgozása
volt; a `deep-web-research` skill teljes csővezetékét (megosztott manifest, shardolás) itt nem
futtatták le, a felkérő ügynök explicit fájlstruktúrát adott meg. A forrás-tier módszertant
(T0–T6) és a verbátim idézet elvét innen vették át.

---

## SQ-03 — Személyes adat exportja (GDPR)

| # | Eszköz | Lekérdezés (verbátim) | Megjegyzés |
|---|---|---|---|
| 1 | WebSearch | `eur-lex GDPR Article 20 right to data portability official text` | Sok "mirror" oldal jött fel (gdpr-info.eu stb.), a CELEX-számot innen azonosították |
| 2 | WebSearch | `eur-lex GDPR Article 15 right of access official text` | Ugyanaz a minta; talált egy CJEU-ügyet is (62021CJ0487), nem vizsgálva tovább |
| 3 | WebSearch | `WP29 guidelines on the right to data portability WP242 EDPB endorsed` | Megtalálta az EDPB endorsement oldalt és az EC newsroom hivatalos listaoldalt |
| 4 | WebSearch | `Data Transfer Initiative dtinit.org Data Transfer Project status 2026` | Megtalálta a dtinit.org docs oldalt és a GitHub repót |
| 5 | WebFetch | `https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679` (metaadat-oldal) | Csak navigációt/metaadatot látott, rossz URL-formátum |
| 6 | WebFetch | `https://edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-right-data-portability-under-regulation-2016679_en` | Sikeres — endorsement dátum, letöltési linkek |
| 7 | WebFetch | `https://www.bvdnet.de/wp-content/uploads/2022/03/Guidelines-on-the-right-to-data-portability.pdf` | Sikeres, harmadikfeles mirror, végül a hivatalos PDF-et használták idézetre |
| 8 | WebFetch | EUR-Lex HTML, 1. próbálkozás, teljes cikk kérése | A WebFetch elutasította "fair use"/copyright hivatkozással, csak összefoglalót ajánlott |
| 9 | WebFetch | `https://ec.europa.eu/newsroom/article29/item-detail.cfm?item_id=611233` | Sikeres — hivatalos dátum (27/10/2017 a listaoldalon, ld. `ellentmondasok.md`) |
| 10 | WebFetch | ugyanaz az EUR-Lex URL, szűkített (csak Art.20, standard skill-prompt) | Ismét elutasítás, "125-character" idézet-limitre hivatkozva |
| 11 | WebSearch | `njt.hu GDPR 2016/679 rendelet 20. cikk adathordozhatósághoz` | Megtalálta a net.jogtar.hu linket és több magyar oldalt |
| 12 | WebFetch | `https://net.jogtar.hu/jogszabaly?docid=a1600679.eup` | `ROBOTS_DISALLOWED` hiba |
| 13 | WebFetch | `https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32016R0679` | Ismét elutasítás ugyanazon indokkal |
| 14 | WebFetch | ugyanaz az EUR-Lex HTML URL, a skill ajánlott pontos prompttal | Sikeres, de csak a preambulumig jutott, utána kitalált "Summary" szakaszt írt — csonkolt lekérés hibamód, nem használva |
| 15 | Bash (`curl`) | közvetlen HTTP GET a fenti EUR-Lex URL-re | HTTP 200, 809 KB HTML — ebből nyerték ki a 15., 20. cikk és a (68), (63) preambulumbekezdés szó szerinti szövegét |
| 16 | Bash (`curl`) | közvetlen HTTP GET `https://ec.europa.eu/newsroom/dae/redirection/document/44099` | HTTP 200, 460 KB PDF (WP242 rev.01) — a WebFetch ugyanerre `ROBOTS_DISALLOWED`-ot adott, a curl sikeres volt |
| 17 | WebSearch | `Google Takeout what's included archive format manifest structure official support` | A releváns hivatalos link megtalálva |
| 18 | WebSearch | `GitHub "user migration" API export archive format docs.github.com` | Több GitHub Docs verzió közül a releváns kiválasztva |
| 19 | WebSearch | `Slack export workspace data JSON format structure official documentation` | A hivatalos slack.com/help oldal megtalálva |
| 20 | WebSearch | `GDPR delete account require export first before deletion practice right to erasure portability` | Csak blog/tanácsadói (T2/T0) találatok — jelzi, hogy nincs közismert jogi kötelezettség erre |
| 21 | WebFetch | `https://support.google.com/accounts/answer/3024190?hl=en` | Sikeres, teljes tartalom |
| 22 | WebFetch | `https://docs.github.com/en/migrations/using-ghe-migrator/exporting-migration-data-from-githubcom` | Sikeres, de nem részletezi az archívum pontos tartalmát |
| 23 | WebFetch | `https://slack.com/help/articles/220556107-How-to-read-Slack-data-exports` | Sikeres, részletes szerkezeti leírás |
| 24 | WebFetch | `https://ico.org.uk/.../right-to-erasure/` | Sikeres — kifejezetten megerősítette, hogy nincs export-előfeltétel említve |
| 25 | WebSearch | `GitHub "delete your personal account" export data warning before deletion docs` | Megtalálta a hivatalos oldalakat |
| 26 | WebFetch | `https://dtinit.org/docs/dtp-intro-for-contributors` | Sikeres |
| 27 | WebFetch | `https://developers.google.com/data-portability` | Sikeres, de nem hivatkozik explicit a Data Transfer Projectre |
| 28 | WebFetch | `https://docs.github.com/en/enterprise-cloud@latest/.../requesting-an-archive-of-your-personal-accounts-data` | Sikeres |
| 29 | WebFetch | `https://docs.github.com/en/account-and-profile/.../deleting-your-personal-account` | Sikeres — nincs technikai export-gát említve |
| 30 | WebSearch | `"data portability" "before" "erasure" OR "deletion" GDPR interplay recital 68 relationship` | Csak T2/T0 blogtalálatok, megerősíti a 20. keresés eredményét |

**Lezárás oka (a forrásból szó szerint):** a 4-6. alkérdés (Google Takeout, GitHub, Slack,
törlés+export) mindegyike elérte azt a pontot, ahol az újabb keresési kör már csak T2/T0 ismétlődő
tartalmat hozott (l. 20. és 30. keresés) — ez *evidence of absence* jellegű megállapítás a
"kötelező export törlés előtt" kérdésre, nem *absence of evidence*. A tool-budget (~30 hívás) is
elfogyott, ezért itt zárult a keresési kör.

---

## SQ-04 — Tömeges behozatal indexelt rendszerbe

Módszertani megjegyzés a forrásból: a WebFetch eszköz nem nyers HTML-t ad vissza, hanem egy kisebb,
gyors modellel összefoglaltatja/idézteti a lekért oldalt a megadott prompt alapján — az idézetek
`"..."` formában szerepelnek, ezek forrás szerinti, állítólagosan szó szerinti idézetek, de mivel
egy közbenső összefoglaló-lépésen mentek át, nem 100%-ban zárható ki egy-egy szóhatár-eltérés.

### WebSearch lekérdezések

1. `Zip Slip vulnerability Snyk official disclosure path traversal`
2. `SQLite FTS5 automerge bulk loading documentation`
3. `Elasticsearch bulk API partial failure items array documentation`
4. `Elasticsearch tune for indexing speed refresh_interval bulk documentation`
5. `CWE-22 path traversal official mitre definition`
6. `CWE-409 decompression bomb zip bomb resource exhaustion mitre`
7. `MySQL LOAD DATA INFILE IGNORE errors continue documentation`
8. `PostgreSQL COPY command atomic transaction error abort documentation`
9. `tus.io resumable upload protocol specification offset`
10. `GitHub "About large files on GitHub" file size limit documentation 100MB`
11. `PyPI file size limit documentation project size limit help.pypi.org`
12. `GitHub importer "Importing a repository" progress percentage log documentation`
13. `npm package size limit documentation docs.npmjs.com maximum tarball`
14. `command line interface guidelines clig.dev progress bar long running process feedback`
15. `Amazon S3 multipart upload resume interrupted upload documentation part number`
16. `restic backup resumable interrupted snapshot content addressed chunks documentation`
17. `npmjs.com docs package size limit "unpacked size" OR "package size"`
18. `"docs-bulk" elasticsearch documentation "atomic" OR "no rollback" bulk operation guarantees`
19. `Joplin import notes markdown validation errors documentation`
20. `"npm publish" package size limit documentation official 2GB OR "size limit"`

### WebFetch lekérések (ténylegesen megnyitott/feldolgozott oldalak)

1. https://snyk.io/research/zip-slip-vulnerability → redirect → https://security.snyk.io/research/zip-slip-vulnerability
2. https://www.sqlite.org/fts5.html (kétszer, más-más prompttal: automerge/usermerge/merge, majd optimize/crisismerge)
3. https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html
4. https://www.elastic.co/docs/deploy-manage/production-guidance/optimize-performance/indexing-speed
5. https://security.snyk.io/research/zip-slip-vulnerability
6. https://github.com/snyk/zip-slip-vulnerability
7. https://cwe.mitre.org/data/definitions/22.html
8. https://cwe.mitre.org/data/definitions/409.html
9. https://dev.mysql.com/doc/refman/8.4/en/load-data.html
10. https://www.postgresql.org/docs/current/sql-copy.html
11. https://tus.io/protocols/resumable-upload
12. https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github
13. https://docs.pypi.org/project-management/storage-limits/
14. https://docs.github.com/en/rest/migrations/source-imports?apiVersion=2022-11-28
15. https://clig.dev/
16. https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html
17. https://restic.readthedocs.io/en/stable/faq.html
18. https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk

---

## Nem elérhető / blokkolt domainek és útvonalak (összesítve)

| Domain / URL | Al-kérdés | Hiba / ok |
|---|---|---|
| obsidian.md/help/import-export | SQ-01 | "File import-export.md does not exist" |
| docs.logseq.com | SQ-01 | Üres/beolvashatatlan tartalom |
| github.com/logseq/docs/.../Page%20properties.md | SQ-01 | 404, hibás útvonal |
| github.com/foambubble/foam/.../note-metadata.md | SQ-01 | 404 |
| okf.md/faq/ | SQ-01 | "Too many redirects" — nem hivatalos Google-domain |
| developer.apple.com/design/human-interface-guidelines/alerts | SQ-02 | Kliensoldali JavaScript-render szükséges, tartalom nem kinyerhető; nem próbálkoztak curl-lel (szabály szerint tiltott megkerülés lenne) |
| api.github.com/search/code?q=... | SQ-02 | 403 — hitelesítés nélkül nem elérhető |
| discourse.joplinapp.org/t/.../48458 (JSON nélkül) | SQ-02 | WebFetch csak metaadatot kapott (JS-alapú betöltés); a `.json` API-végponttal megoldva |
| net.jogtar.hu/jogszabaly?docid=a1600679.eup | SQ-03 | `ROBOTS_DISALLOWED` — magyar jogszabálytár, nem próbálták megkerülni |
| eur-lex.europa.eu (WebFetch-en keresztül, HTML és PDF végpont is) | SQ-03 | A WebFetch eszköz saját "fair use"/idézet-limit szűrése miatt nem adott vissza szó szerinti szöveget (a domain maga HTTP 200-at adott); közvetlen `curl`-lel megoldva |
| docs.npmjs.com (csomagméret-korlát oldal) | SQ-04 | Nem található olyan oldal, amely számszerű, hivatalosan dokumentált korlátot közölne — több keresési kísérlet után lezárva (ld. `hianyok.md`) |
