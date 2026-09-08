# Import és export — kutatási kivonat (K-03)

Dátum: 2026-09-06. Forrás: `.research/import-export/` (00-plan.md, sq01–sq04). Ez a dokumentum a
négy párhuzamos al-kérdés kutatási anyagát fogja össze összefüggő szövegbe; nem tartalmaz új
kutatást, és nem tartalmaz ajánlást vagy döntést — a szintézist a vezető írja külön.

---

## 1. Mire kerestünk választ

A rendszer tulajdonosa (K-03) importot és exportot kér a memóriarendszerhez. Ez nem kényelmi
funkció: a D-24 szerint egy felhasználót csak úgy lehet véglegesen törölni, hogy előtte lefut egy
export a személyes mappájáról — az export tehát a felhasználó-kezelés előfeltétele. Az import a
D-20/1 következménye is: ha a felület önmagában nem hoz létre bejegyzést, kell egy tömeges út a
kezdeti feltöltéshez és a közös tudás behozatalához.

Amit el kell dönteni: milyen **formátumban** exportáljon a rendszer, mekkora legyen a **hatóköre**
(egész fa, egy projekt, egy kategória, egy ember személyes mappája), mit tegyen **ütközésnél**
importkor, és mi utazzon a **verziókból, az indexből és a jogosultságokból**. A rendszer korlátai,
amiket a kutatásnak tiszteletben kellett tartania: a tartalom markdown fájl három gyökér alatt
(`projects/`, `knowledge/`, `personal/<email>/`), a fejlécben pontosan három mező (`tags`,
`modified`, `prompt_version`), verziók vannak, amik végleges törléskor eltűnnek, az index eldobható
és a fájlból újraépíthető, a jogosultság a projekté és az útvonalból jön, nincs vektoradatbázis
vagy Postgres (SQLite index van), és csak beágyazó modell fut, szöveggeneráló nincs.

Négy al-kérdésre bontva: (SQ-01) milyen formátumban exportálnak a markdown-alapú tudástárak, és mi
történik a metaadattal; (SQ-02) milyen ütközéskezelési stratégiák léteznek importnál, és melyik
okoz kevesebb kárt; (SQ-03) mit ír elő a személyes adat hordozhatósága, és mit tartalmaz egy valós
export-csomag; (SQ-04) hogyan kell validálni, kezelni a részleges hibát és biztosítani az
újraindíthatóságot egy tömeges, indexelt rendszerbe történő behozatalnál.

---

## 2. SQ-01 — Milyen formátumban exportálnak a markdown-tudástárak

### Nincs formális export ott, ahol a munkaformátum már maga a csereformátum

Az **Obsidian** hivatalos dokumentációja szerint a vault mozgatása/másolása nem export-lépés, hanem
szó szerinti fájlrendszer-másolás:

> "Select **Move vault**, and then select the new location."
(https://github.com/obsidianmd/obsidian-help/blob/master/en/Files%20and%20folders/Manage%20vaults.md)

A metaadat YAML frontmatterben van, alapértelmezett mezőkkel (`tags`, `aliases`, `cssclasses`), de a
hivatalos oldal nem tér ki az exportra vagy a más eszközökkel való interoperabilitásra. Fontos
árnyalat: az Obsidian natív markdown-ja **nem azonos** a "sima" markdown-nal — az, hogy létezik egy
dedikált community-eszköz (`obsidian-export`, Rust) a `[[wikilink]]`/`![[embed]]` szintaxis
átalakítására, önmagában jelzi, hogy a nyers `.md` fájl csak részlegesen hordozható más
markdown-eszközök felé:

> "Obsidian Export is a CLI program and a Rust library to export an Obsidian vault to regular
> Markdown." ... "obsidian-export supports most but not all of Obsidian's Markdown flavor."
(https://github.com/zoni/obsidian-export)

A **Foam** ugyanezt az elvet vallja explicit módon: nincs dedikált export, mert a VS Code-ban
szerkesztett markdown-mappa maga a natív, hordozható formátum:

> "You own the information you create with Foam, and you're free to share it, and collaborate on it
> with anyone you want." (https://github.com/foambubble/foam)

### A Logseq eltér a "YAML frontmatter" mintától

A **Logseq** oldal- és blokk-tulajdonságai **nem** a `---`-vel határolt YAML frontmattert
használják, hanem egy saját `kulcs:: érték` szintaxist (pl. `rating:: 8`,
`author:: [[sönke ahrens]]`) — a hivatalos docs-repó szerint ez a lap első blokkjában vagy bármely
blokkban jelenik meg (https://github.com/logseq/docs/blob/master/pages/Properties.md?plain=1). Ez
azt jelenti, hogy egy Logseq fájl-alapú gráf markdown fájljai szintaktikailag nem azonosak azzal,
amit egy Obsidian/Joplin frontmatter-parser vár. A Logseq emellett DB-alapú gráf esetén egy külön
EDN-exportot is kínál, amelynek célja explicit "graph-agnosztikus" ábrázolás:

> "Builds sqlite.build EDN to represent nodes in a graph-agnostic way. Useful for exporting and
> importing across DB graphs"
(https://raw.githubusercontent.com/logseq/logseq/master/deps/db/src/logseq/db/sqlite/export.cljs)

### A Joplin a legrészletesebben dokumentált eset: tudatos lossless/lossy megkülönböztetés

A **Joplin** négy exportformátumot kínál, és a hivatalos dokumentáció + egy GitHub issue (a
tervezési döntés elsődleges dokumentuma) explicit módon szétválasztja a "gépi, veszteségmentes" és
az "emberi, olvasható, de tudottan veszteséges" utat:

- **JEX** — tar-csomag: "a lossless format in that all the notes, but also metadata such as
  **geo-location, updated time, tags, etc. are preserved**" (https://joplinapp.org/help/apps/import_export/).
- **RAW** — "This is the same as the JEX format except that the data is saved to a directory and
  each item represented by a single file" (uo.). A hivatalos fórum szerint mindkettőnél a
  fájlnevek **belső ID-k** (pl. `{hexnumber}.md`), nem a cím — ez elkerüli az
  ékezetes/speciális-karakteres fájlnév-problémákat, cserébe "not human readable"
  (https://discourse.joplinapp.org/t/export-summary-what-each-option-does/48564).
- **MD** (sima markdown) — a metaadat **tudottan és dokumentáltan elvész**: "Meta data is lost (no
  ids, no other properties)" (uo.).
- **MD + Front Matter** — a köztes megoldás. A hivatalos GitHub issue rögzíti a pontos
  tervezési döntést:

> "a new export format with the utility of markdown export, but one that is less lossy" — a
> megtartott mezők: **title, created time, updated time, author (ha van), source URL (ha van),
> latitude/longitude/altitude (ha van), tags (ha van)**, valamint todo-knál completed status és due
> date. A tudatosan elhagyott mezőkről: "**all ID's will be lost. Conflict status will also be
> lost. These are acceptable loses**" [sic].
(https://github.com/laurent22/joplin/issues/5224)

Azaz a Joplin fejlesztői tudatosan **külön kezelik** a gépi visszaállíthatóságot (ID, ütközés-állapot
megmarad JEX/RAW-nál) és az emberi olvashatóságot/hordozhatóságot (MD+FM: dátum és szerző megmarad,
ID és ütközés-állapot nem) — ez a legközvetlenebb, T1-forrásból igazolható válasz arra, hogy "mi
utazzon a verziókból": a Joplin explicit döntése szerint az ütközés-állapot **nem** utazik át egyik
emberi olvasható exportformátumban sem.

### A Notion saját magát mondja ki egyirányúnak

A **Notion** egyedi oldalt `.md` fájlként, adatbázist CSV + al-oldal `.md` fájlokként exportál
(https://www.notion.com/help/export-your-content). A hivatalos súgóoldal maga sorolja fel a
korlátokat — nem lehet Form-nézetet exportálni, a más felhasználók privát oldalai kimaradnak, a
callout blokkok HTML-ként (nincs markdown megfelelőjük) exportálódnak — és a legfontosabb, a
kérdésre közvetlenül releváns mondat:

> "**You can't instantly recreate your workspace by reuploading your exported workspace content.**"
(https://www.notion.com/help/export-your-content)

A Notion tehát saját magát nyilatkoztatja **egyirányú, archiváló célú** exportnak, nem kerekre zárt
(round-trip) csereformátumnak. Fontos rés: a hivatalos súgóoldal nem árulja el, hogy a
`created_time`/`last_edited_time` mezők (amik az API-szinten léteznek,
https://developers.notion.com/reference/page) bekerülnek-e egyáltalán az exportált `.md` fájlba —
ezt a kutatás nem tudta megerősíteni sem irányban.

### Zettelkasten-család: TextBundle mint valódi, de szűk körű csomagformátum

A **Zettlr** a **TextBundle**/**TextPack** formátumot ajánlja mellékletes megosztáshoz
(https://docs.zettlr.com/en/export/). Ez egy önálló, több macOS/iOS alkalmazás (Ulysses és mások)
által elfogadott spec, valódi manifeszttel:

> Két változat: `.textbundle` (könyvtár, app-app cseréhez) és `.textpack` (ZIP, felhasználói
> megosztáshoz). Tartalma: `info.json` ("All meta information about the bundle"), `text.*` és egy
> `assets/` könyvtár. Az `info.json` kötelező mezője a `version` (jelenleg 2).
(http://textbundle.org/spec/)

A **Dendron** frontmattere hasonló elven működik (`id`, `title`, `desc`, `updated`, `created` —
utóbbi kettő unix timestamp: https://wiki.dendron.so/notes/ffec2853-c0e0-4165-a368-339db12c8e4b/),
de a dedikált markdown pod exportja **elveszíti a frontmattert**, hacsak nem opcionális kapcsolóval
mentik meg — ez egy nyitott feature request a kutatás idején is
(https://github.com/dendronhq/dendron/issues/3928).

### Van-e elterjedt, nyílt csereformátum? — nincs

A négy fő eszköz (Obsidian, Logseq, Joplin, Notion) mindegyike saját, egyedi formátumot használ, és
egyik sem implementál olyan szabványt, amit egy másik is elfogadna. Ez negatív megállapítás, amit
négy független T1-forrás konvergáló bizonyítéka támaszt alá (Magas biztonságú), bár nincs harmadik
feles/elemző forrás, ami kifejezetten ezt a hiányt dokumentálná (a keresés csak content-farm
oldalakat hozott erre).

Két friss, niche kísérletet azonosítottunk: a **Vault-LD** (2026, egy RDF-alapú markdown-csereformátum,
v0.5.0, "The Knowledge Graph Guys", https://vault-ld.org/) és a Google 2026 júniusában publikált
**Open Knowledge Format (OKF)**, ami a legkomolyabb jelölt, de **nem PKM-export-formátum, hanem
AI-ügynökök számára készített tudás-context szabvány**:

> "An open specification that formalizes the LLM-wiki pattern into a portable, interoperable
> format... a directory of markdown files with YAML frontmatter, with a small set of agreed-upon
> conventions." Egyetlen kötelező mező: `type`.
(https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing)

Az OKF saját magát is korainak nyilvánítja — "OKF v0.1 is a starting point, not a finished
standard." (https://cloud.google.com/blog/products/data-analytics/okf-v0-2-adds-trust-signals/) —
és nincs bizonyíték arra, hogy bármelyik vizsgált PKM-eszköz importálná/exportálná.

---

## 3. SQ-02 — Ütközéskezelés importnál

### A hat stratégia és ki melyiket használja

A kutatás mind a hat, a kérdésben feltételezett stratégiára talált legalább egy dokumentált,
éles gyakorlatban élő példát:

1. **Kihagyás (skip)** — `cp -n`/`--no-clobber`: "(deprecated) silently skip existing files"
   (https://man7.org/linux/man-pages/man1/cp.1.html); `rsync --ignore-existing`: "skip updating
   files that exist on receiver" (https://rsync.samba.org/ftp/rsync/rsync.1). Fontos: egyik
   eszköznél sem ez az alapértelmezés — explicit kérésre aktiválódó opció; kapcsoló nélkül mindkettő
   **felülír**.
2. **Felülírás, esetleg biztonsági másolattal** — `cp` alapból mindent felülír; a `--backup` opció
   előbb átnevezi a régit ("numbered" vagy "simple" módban:
   https://www.gnu.org/software/coreutils/manual/html_node/Backup-options.html); `pg_restore
   --clean`/`--if-exists` teljesen eldob és újraépít mindent objektum-szinten
   (https://www.postgresql.org/docs/current/app-pgrestore.html).
3. **Átnevezés / duplikátum-létrehozás** — a Dropbox "conflicted copy" mintája (a fájlnévbe kerül a
   szerkesztő neve és a mentés dátuma: https://help.dropbox.com/organize/conflicted-copy), a
   Nextcloud desktop kliens hasonló mintája (`"mydata (conflicted copy 2018-04-10 093612).txt"`),
   és az Obsidian Sync **opcionális** "Create conflict file" módja
   (`"original-note-name (Conflicted copy device-name YYYYMMDDHHMM).md"`,
   https://obsidian.md/help/sync/troubleshoot). Feloldásuk mindig **kézi** ("The recommended
   approach involves comparing both versions and merging them manually.").
4. **Verzióként hozzáfűzés / automatikus egyesítés** — az Obsidian Sync markdown fájloknál
   **alapértelmezetten** ezt csinálja, nem duplikál: "Obsidian Sync merges the changes using
   Google's diff-match-patch algorithm" (https://obsidian.md/help/sync/settings). Fontos: bináris/
   canvas fájloknál ugyanaz a termék "last modified wins"-t alkalmaz, beállítás-fájloknál mezőnkénti
   JSON-egyesítést — **egy terméken belül három különböző stratégia** három fájltípusra.
5. **Kézi döntés soronként** — a git a legtisztább mintaadó: amikor mindkét oldal módosítja a fájl
   ugyanazon részét, "Git cannot randomly pick one side over the other, and asks you to resolve it
   by leaving what both sides did to that area" (https://git-scm.com/docs/git-merge). Ez tartalmi
   (nem fájlnév-) ütközés, de a legmunkaigényesebb, sor-szintű minta.
6. **Teljes megszakítás (abort/refuse)** — a Nextcloud szerver-oldali fájlművelete (2021) egyszerűen
   visszautasította az azonos nevű másolást ("Could not copy [filename]; target exists.",
   https://help.nextcloud.com/t/auto-rename-if-file-already-exists/114905) — és maguk a
   felhasználók találták kellemetlennek, funkciókérést nyitva alternatívára.

Egy **negyedik, gépi-szabály-alapú** minta is dokumentált, ami nem illik pontosan az előző hatba:
adatbázis-import eszközök soronként kiértékelt, deklaratív szabállyal döntenek. A PostgreSQL `INSERT
... ON CONFLICT DO UPDATE` "guarantees an atomic INSERT or UPDATE outcome... even under high
concurrency. This is also known as UPSERT." (https://www.postgresql.org/docs/current/sql-insert.html)

### Valós kár — a Joplin esete

A dedikált ütközéskezelés **hiánya** valós kárral dokumentált: a Joplin JEX importja nem ellenőrzi
a meglévő ID-t, ezért duplikátumot hoz létre. Egy 2026-os, konkrét, verzióval ellátott felhasználói
panasz:

> "The JEX import path does not check whether an item with the same `id` already exists in the
> local database or via the current sync target." ... "Actual: Duplicates are created, suggesting
> there is no check for existing note/item IDs during import." ... "Impact: This creates
> large-scale duplication that is painful to clean up and makes JEX import risky as a bootstrap
> method."
(https://discourse.joplinapp.org/t/importing-jex-while-file-system-sync-is-enabled-causes-duplicate-notes-no-id-collision-handling/48458)

### Dry run, atomicitás, idempotencia

**Dry run** bevett gyakorlat nagy hatású műveletek előtt — `terraform plan`, `rsync --dry-run`
("This makes rsync perform a trial run that doesn't make any changes"), Flyway dry-run (SQL fájlt
generál futtatás nélkül), `pg_restore -l` (tartalom-előnézet visszaállítás nélkül) — de **nincs**
kimondott, elvi szabvány, ami minden import-eszköztől megkövetelné.

**Atomicitás**: a SQLite tranzakciói "appear to be atomic even if the transaction is interrupted by
an operating system crash or power failure" (https://sqlite.org/atomiccommit.html); a POSIX
`rename()` szisztéma-hívás garantálja, hogy "if newpath already exists, it will be atomically
replaced" (https://man7.org/linux/man-pages/man2/rename.2.html) — ez a "temp fájlba írás +
átnevezés" minta technikai alapja. Fájlrendszer-alapú eszközöknél (cp, rsync) **nincs** explicit
dokumentált "egészben vagy semennyire" garancia a teljes műveletre, csak az egyes fájlműveletek
atomiak.

**Idempotencia**: a Stripe idempotencia-kulcs mintája (kliens-generált egyedi azonosító a kérésben)
klasszikus analógia egy export-manifesztre; a PostgreSQL upsert és az Anki GUID/első-mező-alapú
egyeztetése ("the existing note's other fields will be updated based on content of the imported
file", https://docs.ankiweb.net/importing/text-files.html) explicit, dokumentált,
azonosító-alapú idempotens mintát követ. A Joplin **ellenpélda**: a JEX import nem idempotens, mert
nem ellenőrzi a meglévő ID-t.

### Van-e mért bizonyíték arra, melyik stratégia okoz kevesebb kárt?

**Nem.** A kutatás kimerítő keresés után sem talált olyan tanulmányt, incidens-elemzést vagy
hibajegy-statisztikát, amely kifejezetten fájlnév-ütközési importstratégiákat hasonlítana össze
adatvesztés vagy felhasználói hiba szempontjából. A legközelebbi, ténylegesen mért adat egy más
doménből (git tartalmi merge) származik:

> Brindescu, Ahmed, Jensen, Sarma (Empirical Software Engineering, 2020), 143 nyílt forráskódú
> projekt elemzése alapján: amikor a feloldás kézi beavatkozást igényelt, "the code is 26× more
> likely to have a bug."
(https://link.springer.com/article/10.1007/s10664-019-09735-4)

Ez **nem** import-ütközésről szól, hanem git-tartalmi merge-ről — analógiaként idézhető ("a kézi
döntést igénylő ütközésfeloldás mérhetően kockázatosabb, mint az automatikus"), de nem helyettesíti
a hiányzó, közvetlen bizonyítékot.

### Tervezési irányelvek az alapértelmezésről

A GNOME HIG explicit az undo-t részesíti előnyben a megerősítő dialógussal szemben destruktív
műveleteknél ("Destructive actions should always be accompanied by either a confirmation dialog or
an offer to undo the action", https://developer.gnome.org/hig/patterns/feedback/dialogs.html). Az
NNGroup (saját bevallása szerint nem kutatás-alapú, hanem szakértői ajánlás) szerint destruktív
megerősítésnél ne legyen alapértelmezett "igen" ("Omit defaults entirely or potentially default to
'No.'"). A Windows 8 tervezői egy konkrét, tesztelt (RITE-módszer, eye-tracking) usability-döntéssel
kerülték el az alapértelmezett kiválasztást a "keep both" jelölőnégyzeteknél: "Removed to prevent
accidental data loss when conflicting files scroll off-screen."
(https://learn.microsoft.com/id-id/archive/blogs/b8/designing-the-windows-8-file-name-collision-experience)
Mindhárom forrás egy irányba mutat, de csak a Brindescu-tanulmány mért adat — a többi bevett
gyakorlat/szakértői vélemény.

---

## 4. SQ-03 — Személyes adat exportja

### A GDPR 20. cikk pontos szövege és hatóköre

> **Article 20 — Right to data portability**
> 1. The data subject shall have the right to receive the personal data concerning him or her,
> which he or she has provided to a controller, in a structured, commonly used and
> machine-readable format and have the right to transmit those data to another controller without
> hindrance from the controller to which the personal data have been provided, where: (a) the
> processing is based on consent pursuant to point (a) of Article 6(1) or point (a) of Article
> 9(2) or on a contract pursuant to point (b) of Article 6(1); and (b) the processing is carried
> out by automated means.
> 3. The exercise of the right referred to in paragraph 1 of this Article shall be without
> prejudice to Article 17. [...]
(https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679)

A **formátum**: "structured, commonly used and machine-readable" — hármas, együttes követelmény;
a rendelet nem nevez meg konkrét fájlformátumot. A **hatókör**: csak azokra a személyes adatokra,
amelyeket az érintett **"has provided to a controller"**, és csak akkor, ha a jogalap hozzájárulás
vagy szerződés **és** az adatkezelés automatizált. A **határidő** a 12. cikk (3) bekezdéséből jön,
ami a 15–22. cikkre (így a 20.-ra is) vonatkozik:

> "The controller shall provide information on action taken on a request under Articles 15 to 22
> to the data subject without undue delay and in any event within one month of receipt of the
> request. That period may be extended by two further months where necessary, taking into account
> the complexity and number of the requests."

Azaz alapesetben **1 hónap**, indokolt esetben (bonyolultság, sok kérés) további **2 hónappal**
meghosszabbítható. A **törléshez való viszony**: a 20. cikk (3) bekezdése kimondja, hogy a
hordozhatóság gyakorlása "without prejudice to Article 17" — a két jog egymástól **független**. A
(68) preambulumbekezdés ezt élesen megerősíti: a hordozhatósági jog "should not imply the erasure
of personal data concerning the data subject which have been provided by him or her for the
performance of a contract to the extent that and for as long as the personal data are necessary
for the performance of that contract."

### 15. cikk vs. 20. cikk — a gyakran összekevert különbség

> **Article 15(3)**: "[...] Where the data subject makes the request by electronic means, and
> unless otherwise requested by the data subject, the information shall be provided in a commonly
> used electronic form."

A 15. cikk szerinti másolat bármilyen "commonly used electronic form"-ban jöhet (akár egy olvasható
PDF is megfelelhet), és **minden** kezelt személyes adatra kiterjed, függetlenül a jogalaptól — a
20. cikk szerinti export viszont kötelezően "structured **and** machine-readable" kell legyen, és
csak a szűkebb, "provided by the data subject" körre vonatkozik.

### A WP29/EDPB iránymutatás (WP242 rev.01) — mi számít "megadottnak"

A hivatalos, EDPB által 2018-ban jóváhagyott iránymutatás élesen elválasztja a "provided by the data
subject" kategóriát a "inferred/derived data"-tól:

> "The following categories can be qualified as 'provided by the data subject': Data actively and
> knowingly provided by the data subject (for example, mailing address, user name, age, etc.) [—]
> Observed data provided by the data subject by virtue of the use of the service or the device.
> [...] In contrast, inferred data and derived data are created by the data controller on the basis
> of the data 'provided by the data subject.' [...] are not covered by the right to data
> portability."
(https://ec.europa.eu/newsroom/dae/redirection/document/44099)

Azaz: igen a nyers/megfigyelt adat, nem a származtatott/kikövetkeztetett adat. A formátum
konkrét jelentésére a WP242 explicit példát ad — **rossz** és **jó** egyaránt:

> "It is unlikely therefore that providing an individual with PDF versions of an email inbox would
> be sufficiently structured or descriptive to allow the inbox data to be easily re-used." [...]
> "data controllers should provide personal data using commonly used open formats (e.g. XML, JSON,
> CSV, …) along with useful metadata at the best possible level of granularity"

A metaadat-követelménynek van korlátja is: "processing additional metadata for the sole purpose
that they might be needed or wanted to answer a data portability request poses no legitimate
ground for such processing."

A legközelebbi hivatalos állásfoglalás a "törlés előtt export" kérdéshez:

> "the Working Party recommends that data controllers always include information about the right
> to data portability before data subjects close any account they may have."

Fontos pontosan olvasni: ez **tájékoztatási** kötelezettség a jog **létezéséről**, nem technikai
előírás, hogy a rendszernek automatikusan le kellene futtatnia egy exportot vagy blokkolnia kellene
a törlést export nélkül.

### Konkrét megvalósítások

- **Google Takeout**: zip/tgz konténer, termékenként külön mappákba szervezve, e-mailes linken vagy
  felhő-tárhelyre közvetlen feltöltéssel kézbesítve; az archívum kb. 7 napig érhető el, legfeljebb 5
  alkalommal tölthető le. Explicit figyelmeztetés: "If you download your Google data, it doesn't
  delete it from Google's servers." — az export és a törlés két, egymástól elválasztott folyamat.
- **GitHub**: személyes fiók archívuma `tar.gz`, mérete "must be less than 20 GB", 7 nap után
  automatikusan törlődik. A fiók törlése előtt a mentés **ajánlott** ("Once your personal account
  has been deleted, GitHub cannot restore your content."), de **nem** technikailag kikényszerített
  előfeltétel.
- **Slack**: JSON export, csatornánként/DM-enként külön mappával, azon belül dátum szerinti JSON
  fájlokkal ("A folder will only be included in the export file if there are messages present for
  the date range you've exported").
- **Data Transfer Project** (gondozza: Data Transfer Initiative, nonprofit): élő, karbantartott
  nyílt forráskódú infrastruktúra, jelenleg 8 adatkategóriát támogat, de a demó oldal "is not run by
  anybody in production" — nincs bizonyíték rá, hogy szélesen elterjedt, kötelező ipari szabvány
  lenne.

### Törlés és export együtt — van-e erre előírás?

**Nem.** A GDPR-ban nem található olyan rendelkezés, amely előírná, hogy a törlés (17. cikk) előtt
kötelezően le kellene futtatni egy exportot — a (68) preambulumbekezdés kifejezetten a két jog
függetlenségét mondja ki. Az Egyesült Királyság adatvédelmi hatóságának (ICO) hivatalos "right to
erasure" útmutatójában **egyáltalán nincs szó** export-előfeltételről — ez explicit keresés utáni,
evidence-of-absence jellegű megállapítás. A három vizsgált, valós rendszer (Google, GitHub, Slack)
egyike sem blokkolja technikailag a törlést export nélkül. **A tervezett "törlés csak kötelező
export után" szabály tehát szigorúbb, mint amit akár a jogszabály, akár a vizsgált termékek
gyakorlata előír vagy technikailag kikényszerít** — ez nem azt jelenti, hogy a döntés helytelen
volna, csak azt, hogy ez a kutatás nem talált rá kötelező jogi vagy elterjedt technikai precedenst.

---

## 5. SQ-04 — Tömeges behozatal indexelt rendszerbe

### Validálás import előtt: Zip Slip és a CWE-taxonómia

A **Zip Slip** egy 2018-ban a Snyk biztonsági csapata által nyilvánosságra hozott, névvel ellátott
sebezhetőségi osztály archívum-kicsomagolásnál:

> "Zip Slip is a widespread arbitrary file overwrite critical vulnerability, which typically
> results in remote command execution." ... "The vulnerability is exploited using a specially
> crafted archive that holds directory traversal filenames (e.g. `../../evil.sh`)."
(https://security.snyk.io/research/zip-slip-vulnerability)

A hiba lényege, hogy az archívumbeli bejegyzés nevét validálás nélkül fűzik a célkönyvtárhoz. Ezt
formalizálja a **CWE-22** (Path Traversal, MITRE hivatalos taxonómia):

> "Many file operations are intended to take place within a restricted directory. By using special
> elements such as '..' and '/' separators, attackers can escape outside of the restricted location
> to access files or directories that are elsewhere on the system."
(https://cwe.mitre.org/data/definitions/22.html)

Ajánlott mitigáció: kanonikus útvonal-feloldás (`realpath()`, `getCanonicalPath()`), majd annak
ellenőrzése, hogy az eredmény a megengedett könyvtáron belül van-e — **minden egyes bejegyzés
feloldott célútvonalát ellenőrizni kell a kiírás előtt**, a nyers bejegyzésnév sosem fűzhető
direktben útvonalhoz. A méret-oldalon a **CWE-409** (dekompressziós bomba) a releváns:

> "The product does not handle or incorrectly handles a compressed input with a very high
> compression ratio that produces a large output." ... "System resources, CPU and memory, can be
> quickly consumed."
(https://cwe.mitre.org/data/definitions/409.html)

A mitigáció itt a **kicsomagolt** (nem a becsomagolt) méret korlátozása/figyelése menet közben.
Séma- és kódolás-validálásra (frontmatter mezők, UTF-8-ellenőrzés) a kutatás nem talált elsődleges
forrású, névvel ellátott ipari szabványt — ez általános bevett gyakorlat, de nincs rá konkrét,
idézhető dokumentáció.

### Részleges hiba: architektúrafüggő minta, nem egységes válasz

Két, egymástól élesen eltérő minta létezik, és a különbség strukturális — attól függ, hogy a
rendszer egyetlen tranzakciós egységben dolgozik-e, vagy elemenként független műveletekként.

**Elasticsearch Bulk API** — elemenkénti válaszszerkezet (az `items` tömb minden akcióhoz külön
státuszt ad), ami azt mutatja, hogy a sikeres elemek a hibásak mellett is bekerülnek az indexbe:

```
{"took":7, "errors": false, "items":[{"index":{"_index":"test","_id":"1","_version":1,"result":"created","forced_refresh":false}}]}
```
(https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html)

**MySQL LOAD DATA** — a döntés explicit, opt-in: `IGNORE` nélkül "data-interpretation errors
terminate the operation"; `IGNORE`-ral a hiba figyelmeztetéssé szelídül, és a betöltés folytatódik
(https://dev.mysql.com/doc/refman/8.4/en/load-data.html). **PostgreSQL COPY** hiba esetén a már
beírt sorok "left in a deleted state" — logikailag eltűnnek, de fizikailag `VACUUM`-ig foglalják a
helyet (https://www.postgresql.org/docs/current/sql-copy.html) — ez a "teljes visszagörgetés"
mintájának egy változata.

A tanulság a tervezett rendszerre: mivel a fájl az igazság forrása és az index eldobható/
újraépíthető, az **index-írás** oldala inkább az Elasticsearch-mintához hasonlítható (független,
elemenkénti műveletek, megtartható részleges siker + hibalista), míg a **fájlrendszerre történő
kiírás** inkább az SQL-mintához hasonlóan kezelhető: minden fájl saját, önálló siker/hiba egység.

### Újraindíthatóság — közös minta három, jól dokumentált rendszerből

Egyik forrás sem tárgyalja kifejezetten "markdown-fájlok tömeges importjának" újraindíthatóságát,
de a szomszédos, jól dokumentált területek (fájlfeltöltés, backup) közös, átvihető mintát mutatnak:

- **tus protokoll**: "A `HEAD` request is used to determine the offset at which the upload should
  be continued." (https://tus.io/protocols/resumable-upload)
- **AWS S3 multipart upload**: "you only need to retry uploading the parts that are interrupted
  during the upload. You don't need to restart uploading your object from the beginning."
  (https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html)
- **restic**: "restic periodically writes index files to keep a record of the uploaded data. [...]
  Next time restic runs, it is then able to find the uploaded data through these indexes."
  (https://restic.readthedocs.io/en/stable/faq.html)

A közös minta három elemből áll: **egyedi azonosító** az egész műveletre, **lekérdezhető állapot**
arról, mi készült már el, és **folytatás a hiányzó résztől**, nem a teljes újrakezdéstől. A restic a
legközelebbi dokumentált analógia a "tartalom-hash alapú" checkpoint ötlethez (content-addressed
deduplikáció), de kifejezetten "import-checkpoint fájl tartalom-hash-sel" mintát dokumentáló
elsődleges forrást a kutatás nem talált.

### Indexelés: a drága munkát a végére kell halasztani

Az **Elasticsearch** explicit, névvel dokumentált ajánlása: tömeges betöltésnél kapcsold ki az
azonnali kereshetővé tételt, a végén kapcsold vissza:

> "set the refresh interval to `-1`. This prevents Elasticsearch from performing any refreshes
> during the bulk indexing process." ... "Only re-enable refreshing after your bulk indexing is
> complete and you need the data to be searchable."
(https://www.elastic.co/docs/deploy-manage/production-guidance/optimize-performance/indexing-speed)

A **SQLite FTS5** mechanizmusa (automerge, alapértelmezés 4, max 16; `merge`/`optimize` parancsok)
pontosan dokumentált, de a hivatalos oldal **nem tartalmaz** explicit, névvel ellátott "bulk
loading" ajánlást — ez fontos korrekció: a mechanizmusból levezethető ("kapcsold ki az automerge-t
importkor, majd optimize a végén"), de a dokumentáció ezt nem mondja ki ilyen formában. Mindkét
rendszer ugyanabba az irányba mutat: **a drága indexelési/összefésülési munkát halasszuk a nagy
import végére**, ne fájlonként/soronként végezzük.

### Visszajelzés hosszú futású importnál

Nincs formális ipari szabvány (ISO/W3C) a haladás megjelenítésére, de van egy közösségi irányelv és
egy konkrét, élesben működő termékpélda. A Command Line Interface Guidelines szerint "if your
program displays no output for a while, it will look broken" (https://clig.dev/). A GitHub
forrás-import API-ja explicit fázis-állapotgépet dokumentál (`detecting`, `importing`, `mapping`,
`pushing`, `complete`, plusz hibaállapotok), számszerű haladási mezőkkel (`percent`, `push_percent`)
(https://docs.github.com/en/rest/migrations/source-imports?apiVersion=2022-11-28) — ez egy jól
követhető minta: fázisokra bontott állapot (pl. `validating` → `writing` → `indexing` →
`complete`/`error`), és ezen belül számszerű százalék.

### Méretkorlátok — mit dokumentálnak a valós rendszerek

| Rendszer | Korlát | Idézet |
|---|---|---|
| GitHub (git push) | 50 MiB felett figyelmeztetés, 100 MiB felett tiltás | "GitHub blocks files larger than 100 MiB." |
| GitHub (repó, ajánlás) | <1 GB ideális, <5 GB erősen ajánlott | "We recommend repositories remain small, ideally less than 1 GB, and less than 5 GB is strongly recommended." |
| PyPI | 100.0 MB/fájl, 10.0 GB/projekt (alapértelmezett) | "By default, PyPI limits the size of individual files to 100.0 MB." |
| Elasticsearch | 100 MB/HTTP-kérés (alapértelmezett) | "Elasticsearch limits the maximum size of a HTTP request to 100mb by default" |
| AWS S3 multipart | rész-szám 1–10 000 | "You can choose any part number between 1 and 10,000." |
| npm | nincs hivatalosan dokumentált, számszerű korlát | — (ld. `hianyok.md`) |

A PyPI külön kiemeli: "Yanking a release or file does not free up storage space" — csak a tényleges
törlés szabadít fel helyet.

---

## 6. Ellentmondások

A teljes, forrásonkénti bontás az `ellentmondasok.md`-ben található; itt a legfontosabbak, mindkét
oldal idézetével.

**Nextcloud — két alrendszer, két alapértelmezés (SQ-02).** A szerver-oldali fájlművelet blokkol:
"Could not copy [filename]; target exists." — a desktop szinkron-kliens viszont duplikál:
`"mydata (conflicted copy 2018-04-10 093612).txt"`. **Feloldás:** nem ellentmondás, két különböző
komponens két különböző tervezési döntése ugyanazon termékcsaládon belül.

**"Mindent-vagy-semmit" vs. "megtartom, ami átment" (SQ-04).** A PostgreSQL COPY hiba esetén a
korábban beírt sorokat logikailag eltűnteti ("left in a deleted state"), míg az Elasticsearch Bulk
API elemenkénti válasza szerint a sikeres elemek a hibásak mellett is bekerülnek az indexbe.
**Feloldás:** architektúrafüggő különbség — a COPY egyetlen tranzakcióba csomagolja a műveletet, az
Elasticsearch Bulk API-nak nincs több-dokumentumos tranzakciós fogalma. A kérdés nem az, melyik a
"helyes" minta, hanem hogy milyen egységekben definiáljuk a siker/hiba állapotát.

**A WP242 rev.01 dátuma (SQ-03).** Három forrás három dátumot mutat (2016.12.13. eredeti elfogadás;
2017.04.05. felülvizsgált "rev.01"; 2018.05.25. EDPB-jóváhagyás; az EC newsroom 2017.10.27-et mutat
listaoldalán). **Feloldás:** négy különböző esemény dátuma ugyanahhoz a dokumentumhoz, nem
ellentmondás — mindegyiket külön feltüntettük.

**Az OKF "nyíltsága" és a "Google alone" kontrollja (SQ-01).** A cloud.google.com blog egyszerre
állítja, hogy az OKF "vendor-neutral" és "an open standard", miközben a specifikációt kizárólag
Google-alkalmazottak írták, és minden referencia-implementáció Google-termék. **Nyitva marad:**
ez nem forrás-ellentmondás, hanem gyártói állítás és a dokumentált állapot közti feszültség — a
formátum *célja* nyílt, az *aktuális állapota* (2026 közepén) egyetlen szereplőhöz kötött.

A többi vizsgált terület (SQ-02 konvergáló irányelvek: GNOME/NNGroup/Brindescu; SQ-04 MySQL
`IGNORE` mint opt-in vs. Elasticsearch nem-kikapcsolható részleges siker) nem tényszerű
ellentmondás, hanem architekturális vagy hangsúlybeli különbség — részletesen az
`ellentmondasok.md`-ben.

---

## 7. Hiányok

A teljes lista al-kérdésenként a `hianyok.md`-ben; itt a legfontosabbak, élesen megkülönböztetve.

**Amiről a kutatás azt állítja, hogy [NINCS ILYEN]** (evidence of absence, kimerítő keresés után):
- Nincs mért, kvantitatív bizonyíték arra, melyik importütközési stratégia (kihagyás/felülírás/
  átnevezés/kézi döntés/megszakítás) okoz kevesebb kárt (SQ-02).
- A GDPR-ban nincs olyan rendelkezés, ami előírná a kötelező exportot törlés előtt; az ICO
  útmutatójában sincs export-előfeltétel (SQ-03).
- A SQLite FTS5 hivatalos doksija nem tartalmaz explicit "bulk loading" ajánlási szakaszt (SQ-04).
- Nincs hivatalosan dokumentált, számszerű npm csomagméret-korlát (SQ-04) — inkább absence of
  evidence jellegű, mint tiszta "nincs ilyen".

**Amiről a kutatás azt állítja, hogy [NEM TALÁLTUK MEG]** (létezhet, de ez a kör nem ért el hozzá):
- Van-e dedikált manifeszt-fájl a Joplin JEX/RAW csomagokban (SQ-01), illetve a GitHub személyes
  fiók migrációs archívumában (SQ-03).
- A Notion Markdown exportja tartalmaz-e bármilyen frontmatter-szerű blokkot vagy időbélyeget
  (SQ-01).
- Ékezetes/speciális karakteres fájlnevek kezelése egyik vizsgált eszköznél sem dokumentált
  explicit módon (SQ-01).
- Az Apple Human Interface Guidelines destruktív-akció ajánlása technikai okból (JS-render) nem
  volt elérhető (SQ-02).
- A Joplin (és általában a fájl-alapú jegyzet-appok) import-tranzakció szintje ismeretlen — egyetlen
  tranzakcióban vagy fájlonként fut-e (SQ-02, SQ-04).
- A Google saját fióktörlési felülete (nem a Takeout) technikailag felajánlja/megköveteli-e a
  Takeout futtatását törlés előtt (SQ-03).
- Az Elasticsearch Bulk API "nem atomikus" jellege a lekért dokumentáció-részletekben nincs
  explicit kimondva, csak a válaszstruktúrából levezetett (SQ-04).
- Mért teljesítményadat a "menet közben vs. a végén" indexelésről Bun/SQLite kontextusban — ez
  implementáció-specifikus mérés lenne, nem dokumentáció-kérdés (SQ-04).

Tudatos hatókör-szűkítések (nem hiányok): a kutatás csak angol nyelven keresett (az eszközök
nemzetközi dokumentációs kultúrája miatt); a GDPR-t csak angol EUR-Lex szövegből idézte; és csak a
GDPR-t/ICO-t/WP242-t vizsgálta jogi kontextusként, más joghatóságokat (CCPA, LGPD) nem.

---

## 8. Minden meglátogatott link

A teljes, tier-besorolt lista (feldolgozott és fel nem dolgozott linkek) a `linkek.md`-ben van. Az
alábbi táblázat a ténylegesen felhasznált, idézett forrásokat sorolja fel al-kérdésenként.

### SQ-01 — Markdown-tudástárak (tier-skála: T1 hivatalos/spec, T2 jó másodlagos, T3 fórum/marketing)

| URL | Tier | Mire volt jó |
|---|---|---|
| https://obsidian.md/help/properties | T1 | Frontmatter/Properties leírása |
| https://obsidian.md/help/attachments | T1 | Csatolmányok leírása |
| https://github.com/obsidianmd/obsidian-help/blob/master/en/Files%20and%20folders/Manage%20vaults.md | T1 | Vault mozgatás = fájlrendszer-másolás |
| https://github.com/zoni/obsidian-export | T1 | Obsidian markdown ≠ sima markdown |
| https://github.com/logseq/docs/blob/master/pages/Properties.md?plain=1 | T1 | `kulcs:: érték` property-szintaxis |
| https://raw.githubusercontent.com/logseq/logseq/master/deps/db/src/logseq/db/sqlite/export.cljs | T1 | EDN export forráskódja |
| https://deepwiki.com/logseq/logseq/6.2-graph-import-and-export | T3 | Csak vezetés/keresztellenőrzés |
| https://joplinapp.org/help/apps/import_export/ | T1 | JEX/RAW/MD/MD+FM formátumok |
| https://github.com/laurent22/joplin/blob/dev/readme/apps/import_export.md | T1 | Megerősítés |
| https://discourse.joplinapp.org/t/export-summary-what-each-option-does/48564 | T2 | ID-alapú fájlnevek, MD metaadat-vesztés |
| https://github.com/laurent22/joplin/issues/5224 | T1 | MD+FM tervezési döntés |
| https://github.com/laurent22/joplin/issues/3473 | T1 | Fájlnév-duplikáció bug |
| https://www.notion.com/help/export-your-content | T1 | Formátum, korlátok, "nem re-importálható" |
| https://developers.notion.com/reference/page | T1 | API-mezők (created_time stb.) |
| https://docs.zettlr.com/en/export/ | T1 | Textbundle/Textpack ajánlás |
| https://wiki.dendron.so/notes/ffec2853-c0e0-4165-a368-339db12c8e4b/ | T1 | Dendron frontmatter mezők |
| https://github.com/dendronhq/dendron/issues/3928 | T1 | Frontmatter elvész exportnál |
| https://github.com/foambubble/foam | T1 | Data-ownership elv |
| http://textbundle.org/spec/ | T1 | TextBundle spec, info.json manifeszt |
| https://vault-ld.org/ | T1 | Niche RDF-markdown csereformátum |
| https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing | T1 | OKF bejelentés |
| https://cloud.google.com/blog/products/data-analytics/okf-v0-2-adds-trust-signals/ | T1 | OKF v0.2 |
| https://raw.githubusercontent.com/GoogleCloudPlatform/knowledge-catalog/main/okf/SPEC.md | T1 | OKF specifikáció |
| https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/README.md | T1 | OKF repó README |
| https://alexop.dev/posts/open-knowledge-format-markdown-frontmatter-agent-knowledge/ | T3 | Csak vezetés |

### SQ-02 — Ütközéskezelés (tier-skála: T1 nyílt/spec, T2 lektorált tudomány, T3 gyártói hivatalos, T4 gyártói blog, T5 AI-aggregátor, T6 fórum/issue)

| URL | Tier | Mire volt jó |
|---|---|---|
| https://help.dropbox.com/organize/conflicted-copy | T3 | Conflicted copy minta |
| https://www.nngroup.com/articles/confirmation-dialog/ | T3 | Megerősítő dialógus ajánlások |
| https://www.nngroup.com/articles/proximity-consequential-options/ | T3 | Térbeli elválasztás ajánlása |
| https://www.gnu.org/software/coreutils/manual/html_node/Backup-options.html | T1 | `cp --backup` mechanizmus |
| https://man7.org/linux/man-pages/man1/cp.1.html | T1 | `cp -n`, `-i`, alapértelmezett felülírás |
| https://discourse.joplinapp.org/.../48458.json | T6 | Joplin ID-ütközés hiánya |
| https://github.com/laurent22/joplin/issues/537 | T6 | Elvárt import-összegzés |
| https://sqlite.org/atomiccommit.html | T1 | Tranzakció-atomicitás |
| https://docs.stripe.com/api/idempotent_requests | T3 | Idempotencia-kulcs minta |
| https://docs.ankiweb.net/importing/text-files.html | T3 | GUID-alapú duplikátum-kezelés |
| https://www.postgresql.org/docs/current/sql-insert.html | T1 | `ON CONFLICT` upsert |
| https://developer.hashicorp.com/terraform/cli/commands/plan | T3 | Dry-run minta |
| https://help.nextcloud.com/t/auto-rename-if-file-already-exists/114905 | T6 | Blokkoló viselkedés (2021) |
| https://developer.gnome.org/hig/patterns/feedback/dialogs.html | T1 | Undo > megerősítés |
| https://devblogs.microsoft.com/oldnewthing/20190604-00/?p=102539 | T4 | Windows numerikus utótag |
| https://learn.microsoft.com/id-id/archive/blogs/b8/designing-the-windows-8-file-name-collision-experience | T4 | Nincs alapértelmezett kiválasztás |
| https://link.springer.com/article/10.1007/s10664-019-09735-4 | T2 | Brindescu et al. — 26x hibaarány |
| https://raw.githubusercontent.com/nextcloud/documentation/master/user_manual/desktop/conflicts.rst | T3 | Nextcloud desktop kliens minta |
| https://git-scm.com/docs/git-merge#_how_conflicts_are_presented | T1 | Soronkénti kézi feloldás |
| https://github.com/flyway/flywaydb.org/blob/gh-pages/documentation/concepts/dryruns.md | T3 | Flyway dry-run |
| https://rsync.samba.org/ftp/rsync/rsync.1 | T1 | rsync dry-run/ignore-existing/backup |
| https://deepwiki.com/obsidianmd/obsidian-help/2.3-synchronization-and-conflict-resolution | T5 | Csak orientáció |
| https://obsidian.md/help/sync/settings | T3 | Automatikus egyesítés alapértelmezett |
| https://obsidian.md/help/sync/troubleshoot | T3 | Konfliktusfájl-elnevezés |
| https://www.postgresql.org/docs/current/app-pgrestore.html | T1 | `--clean`/`--if-exists`/`--list` |
| https://man7.org/linux/man-pages/man2/rename.2.html | T1 | POSIX rename() atomicitás |

### SQ-03 — Személyes adat exportja (tier-skála: T1 jogszabály/hivatalos EDPB/termék, T2 hiteles mirror/hatósági, T3 másodlagos, T0 marketing)

| URL | Tier | Mire volt jó |
|---|---|---|
| https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679 | T1 | GDPR 15., 20. cikk, (63), (68) preambulum |
| https://ec.europa.eu/newsroom/dae/redirection/document/44099 | T1 | WP242 rev.01 teljes szövege |
| https://ec.europa.eu/newsroom/article29/item-detail.cfm?item_id=611233 | T1 | WP242 dátum/referencia |
| https://edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-right-data-portability-under-regulation-2016679_en | T1 | EDPB jóváhagyás |
| https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-erasure/ | T1 | Nincs export-előfeltétel (ICO) |
| https://support.google.com/accounts/answer/3024190?hl=en | T1 | Google Takeout formátum/korlátok |
| https://docs.github.com/en/migrations/using-ghe-migrator/exporting-migration-data-from-githubcom | T1 | GitHub migrációs export |
| https://docs.github.com/en/enterprise-cloud@latest/.../requesting-an-archive-of-your-personal-accounts-data | T1 | Méretkorlát, élettartam |
| https://docs.github.com/en/account-and-profile/.../deleting-your-personal-account | T1 | Mentési ajánlás törlés előtt |
| https://slack.com/help/articles/220556107-How-to-read-Slack-data-exports | T1 | Slack export szerkezete |
| https://dtinit.org/docs/dtp-intro-for-contributors | T1 | Data Transfer Project állapota |
| https://developers.google.com/data-portability | T1 | Google Data Portability API |
| https://www.bvdnet.de/wp-content/uploads/2022/03/Guidelines-on-the-right-to-data-portability.pdf | T2 | Csak keresztellenőrzés |

### SQ-04 — Tömeges behozatal (tier-skála: T1 hivatalos/spec/CWE, T2 jó másodlagos, T3 fórum/marketing)

| URL | Tier | Mire volt jó |
|---|---|---|
| https://security.snyk.io/research/zip-slip-vulnerability | T1 | Zip Slip definíció |
| https://github.com/snyk/zip-slip-vulnerability | T1 | PoC-kód |
| https://cwe.mitre.org/data/definitions/22.html | T1 | CWE-22 Path Traversal |
| https://cwe.mitre.org/data/definitions/409.html | T1 | CWE-409 dekompressziós bomba |
| https://www.sqlite.org/fts5.html | T1 | automerge/merge/optimize |
| https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html | T1 | Bulk API válaszszerkezet |
| https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk | T1 | Bulk API-referencia |
| https://www.elastic.co/docs/deploy-manage/production-guidance/optimize-performance/indexing-speed | T1 | refresh_interval, replikák |
| https://dev.mysql.com/doc/refman/8.4/en/load-data.html | T1 | LOAD DATA IGNORE |
| https://www.postgresql.org/docs/current/sql-copy.html | T1 | COPY hiba → deleted state |
| https://tus.io/protocols/resumable-upload | T1 | Offset-alapú folytatás |
| https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github | T1 | GitHub méretkorlátok |
| https://docs.pypi.org/project-management/storage-limits/ | T1 | PyPI méretkorlátok |
| https://docs.github.com/en/rest/migrations/source-imports?apiVersion=2022-11-28 | T1 | Import-állapotgép, haladás |
| https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html | T1 | S3 multipart, ListParts |
| https://restic.readthedocs.io/en/stable/faq.html | T1 | Content-addressed checkpoint |
| https://clig.dev/ | T2 | Progress feedback irányelv |

*(A fel nem dolgozott, csak keresésben látott linkek teljes listája a `linkek.md` B) szakaszában.)*
