# ELL01 — Licenc, kiadás és a cég helyzete

> **Módszertani megjegyzés.** Ez adverzariális ellenőrzés: a cél az sq01/sq02 korábbi állításainak megdöntése, nem megerősítése. A kötelező kereső­eszköz az **Exa** volt (`mcp__Exa__web_search_exa`, `mcp__Exa__web_fetch_exa`) — mindkettő elérhető volt és kizárólagosan ezekkel kerestem/olvastam oldalakat; beépített `WebSearch`/`WebFetch` egyszer sem futott. `curl`-t kizárólag nyers, verbatim ellenőrzésre használtam: GitHub raw fájlok (`LICENSE`, `Cargo.toml`, `CONTRIBUTING.md`, `README.md`), a Docker Hub és PGXN gépi API-i (kiadási jegyzékek), valamint a hivatalos GNU AGPL-3.0/FAQ szövegek nyers `.txt`/`.html` verziói. Egy esetben (`docs.paradedb.com/deploy/enterprise`) a `curl`-lal lekért nyers HTML kliensoldalon renderelt (JS-alapú) oldalnak bizonyult, üres tartalommal — ezért a tényleges szöveget Exa-fetch-csel szereztem be, ez az egyetlen pont, ahol a `curl`-teszt önmagában félrevezető lett volna (l. 2. állítás). Alügynök-fan-out (Sonnet-kereső / Opus-szintézis) ebben a környezetben nem indítható, ezért egyetlen szálon, szekvenciálisan dolgoztam — ez a `_ell_kozos.txt` szerinti degradált mód. Minden verdiktet igyekeztem két, egymástól független forrással alátámasztani; ahol ez nem sikerült, jelzem.

## Verdikt-összefoglaló

| # | Állítás | Verdikt | Egy mondat |
|---|---|---|---|
| 1 | `paradedb/paradedb` (pg_search) licence ma AGPL-3.0; legfrissebb stabil kiadás v0.25.9 (2026-09-11) | **RÉSZBEN IGAZOLVA** | A licenc (AGPL-3.0) tökéletesen igazolt; a v0.25.9/2026-09-11 verziót két független, géppel olvasható registry (Docker Hub API, PGXN) is megerősíti, de a GitHub saját „latest release" oldala (Exa-fetch) ellentmondóan v0.25.6-ot (2026-08-27) mutatott. |
| 2 | Van fizetős Enterprise; hivatalos összehasonlítás szerint a keresési funkciók azonosak, a különbség replikáció/HA/olvasó replikák (standby-olvasás csak Enterprise-ban) | **RÉSZBEN IGAZOLVA** | A funkcionális összehasonlítás (keresés/index azonos, HA+Read Replica csak Enterprise-ban, standby-olvasás Community-n technikailag tiltott) szó szerint stimmel, de az állítás hiányos: a hivatalos oldal szerint az Enterprise emellett **licencben is más** ("waives the copyleft provision of AGPL-3.0") és tartalmaz nem specifikált zárt forráskódú funkciókat is. |
| 3 | A cég minden közreműködőtől CLA-t kér, amely AGPL **és** kereskedelmi licencelést is lehetővé tesz | **IGAZOLVA** | A `CONTRIBUTING.md` szó szerint kimondja, hogy a hozzájárulás egyszerre AGPL-3.0 **és** kereskedelmi szoftver licence alá kerül, amit a CLA saját, tág szerzői jogi engedmény-szövege is alátámaszt. |
| 4 | A licenc „a kezdetektől" AGPL; a korábbi `pg_analytics` PostgreSQL License alatt futott, 2025-03-19-én archiválták | **IGAZOLVA** (a „from day one" rész a cég saját, nem független állítása) | A `pg_analytics` PostgreSQL License-e és 2025-03-19-i archiválása közvetlenül, két forrásból igazolt; az „AGPL a kezdetektől" kizárólag a cég 2024-es utólagos blogbejegyzésén nyugszik, 2023-as független forrás erre nem található. |
| 5 | A Neon 2026 márciusában bejelentette a `pg_search` kivezetését, teljes megszűnés 2026-09-21 | **IGAZOLVA** | A Neon két hivatalos, egymástól különböző dokumentációs oldala szó szerint megerősíti: új projekteken 2026. március 19. óta nem elérhető, meglévő telepítéseket 2026. szeptember 21-én távolítják el. |
| 6 | Létezik a Timescale/TigerData `pg_textsearch` BM25-bővítménye PostgreSQL License alatt — érettség, verzió, támogatott Postgres, magyar nyelv, BM25 | **IGAZOLVA** | PostgreSQL License megerősítve; jelenlegi verzió v1.4.0 (2026-08-18), csak PG 17–18-at támogat (19 béta best-effort), valódi BM25-rangsorolást ad, és a magyar ("hungarian") szerepel a támogatott 29 Postgres text-search-konfiguráció között — de a projekt előzetes kiadása csak 2025-10-23-i, tehát kevesebb, mint egy éve fejlesztik. |
| 7 | AGPL-3.0 13. § a módosított program hálózati elérésére vonatkozik (szó szerint); van-e ParadeDB-saját nyilatkozat a csak SQL-en beszélő, változatlan klienshasználatra | **RÉSZBEN IGAZOLVA** | A 13. § szó szerinti szövege pontosan igazolt és megegyezik a ParadeDB saját `LICENSE` fájljával; ugyanakkor semmilyen hivatalos ParadeDB-oldal, FAQ vagy blogbejegyzés nem foglalkozik kifejezetten azzal az esettel, amikor egy külön folyamatban futó alkalmazás csupán SQL-en (Postgres wire protocol-on) keresztül, a `pg_search`-öt nem módosítva használja azt — ilyen nyilatkozat nem található. |

---

## Állításonként

### 1. Licenc és legfrissebb stabil kiadás

**Licenc — teljesen igazolva.** A `paradedb/paradedb` monorepó gyökér `LICENSE` fájlja (nyers fájl, `curl`, 2026-09-22, HTTP 200):

> „GNU AFFERO GENERAL PUBLIC LICENSE
> Version 3, 19 November 2007"

Forrás: https://raw.githubusercontent.com/paradedb/paradedb/main/LICENSE

A `Cargo.toml` workspace-szekciója megerősíti:

> „[workspace.package]
> version = \"0.25.6\"
> edition = \"2024\"
> license = \"AGPL-3.0\""

Forrás: https://raw.githubusercontent.com/paradedb/paradedb/main/Cargo.toml (curl, 2026-09-22)

**Verzió/dátum — két független, géppel olvasható forrás egyezik, a GitHub saját oldala viszont nem.**

Docker Hub hivatalos API (`paradedb/paradedb` szervezeti fiók, `curl`, közvetlen JSON, 2026-09-22):

```
v0.25.9   2026-09-11T18:28:54.209419Z
0.25.9    2026-09-11T18:28:57.099286Z
```

Forrás: https://hub.docker.com/v2/repositories/paradedb/paradedb/tags?page_size=20&ordering=last_updated

PGXN (PostgreSQL Extension Network), önálló, verziószámozott URL (Exa-fetch, 2026-09-22):

> „# pg_search 0.25.9
> pg_search 0.25.9: Full text search for PostgreSQL using BM25 / PostgreSQL Extension Network"

Forrás: https://pgxn.org/dist/pg_search/0.25.9/ (a `https://pgxn.org/dist/pg_search/0.25.9/META.json` közvetlen géppel-olvasható változata 404-et adott ezen a napon, de a HTML-oldal maga létezik és verzió-specifikus).

**Ellentmondás:** a GitHub saját „latest release" oldala (Exa-fetch, 2026-09-22) ugyanekkor ezt adta vissza:

> „# v0.25.6
> - Tag: v0.25.6
> - Published: 2026-08-27T21:44:47Z"

Forrás: https://github.com/paradedb/paradedb/releases/latest

Ez logikailag ellentmond a Docker Hub-adatnak (a v0.25.9 tag később, 2026-09-11-én jelent meg, mint a v0.25.6 2026-08-27-i dátuma, tehát ha létezik, a GitHub „latest"-nek is azt kellene mutatnia). A `curl`-lal indított közvetlen GitHub API-hívás (`api.github.com/repos/paradedb/paradedb/releases/latest`) ebben a környezetben HTTP 403-at adott („GitHub access to this repository is not enabled for this session"), így ezt nem lehetett közvetlenül feloldani; a legvalószínűbb magyarázat egy elavult Exa-crawler-cache a GitHub dinamikus oldalán, nem valódi adatellentmondás — de ezt nem sikerült bizonyítani, csak valószínűsíteni.

### 2. Enterprise vs. Community — funkciók és licenc

A hivatalos oldal aktuális, teljes szövege (Exa-fetch, kétszer lekérve különböző URL-eken — `docs.paradedb.com/deploy/enterprise` és a canonicalizált `www.paradedb.com/docs/operate/deploy/enterprise`, mindkettő ugyanazt a tartalmat adta, 2026-09-22):

> „ParadeDB Community is our open source product, licensed under AGPL-3.0. This license permits free use, modification, and distribution of the software, provided that distributed, derivative works of the software are released under the same license (copyleft provision).
>
> In addition to all of the features of ParadeDB Community, ParadeDB Enterprise:
> 1. Waives the copyleft provision of AGPL-3.0
> 2. Contains several closed-source features that are recommended for ParadeDB to service enterprise, production workloads"

A „Feature Comparison" táblázat szó szerint (kivonat):

> „| | ParadeDB Community | ParadeDB Enterprise |
> | BM25 scoring | ✅ | ✅ |
> | Hybrid search | ✅ | ✅ |
> | Query builder API | ✅ | ✅ |
> | Highlighting | ✅ | ✅ |
> | Maximum cluster size | 1 | Unlimited |
> | Logical Replication | ✅ | ✅ |
> | High Availability Support | ❌ | ✅ |
> | Read Replica Support | ❌ | ✅ |"

Forrás: https://docs.paradedb.com/deploy/enterprise

Tehát a keresési/index funkciók (BM25, hibrid keresés, highlighting, aggregátumok stb.) valóban azonosak — de az Enterprise **nem csak** funkcionálisan más: saját megfogalmazásuk szerint a kereskedelmi verzió a copyleft-kötelezettséget is feloldja, plusz „several closed-source features"-t tartalmaz, amit a táblázat nem sorol fel tételesen.

**„Standby-ról olvasás csak Enterprise-ban" — közvetlenül igazolva**, mégpedig egy éles GitHub-hibaüzenet szó szerinti szövegével (2026, nyitott issue):

> „replicas are not supported on community and require paradedb enterprise, which guarantees physical replication safety on standbys."

Forrás: https://github.com/paradedb/paradedb/issues/6007 („Community ParadeDB index creation stops all PostgreSQL physical replication")

Ezt megerősíti a hivatalos „Guarantees" oldal is:

> „ParadeDB Community supports logical replication, but not physical replication: […] The ParadeDB index does not get physically replicated and won't be available on other nodes in a high availability setup.
> ParadeDB Enterprise supports both: […] It supports physical replication and high availability, ensuring that the ParadeDB index remains consistent and crash-safe across nodes."

Forrás: https://docs.paradedb.com/welcome/guarantees

### 3. CLA — AGPL és kereskedelmi licencelés egyszerre

A `CONTRIBUTING.md` (nyers fájl, `curl`, 2026-09-22, HTTP 200) „Legal Info" szakasza szó szerint:

> „In order for us, ParadeDB, Inc., to accept patches and other contributions from you, you need to adopt our ParadeDB Contributor License Agreement (the \"CLA\"). […]
>
> ### License
> By contributing to ParadeDB, you agree that your contributions will be licensed under the [GNU Affero General Public License v3.0](LICENSE) **and as commercial software**."

Forrás: https://raw.githubusercontent.com/paradedb/paradedb/main/CONTRIBUTING.md

Második, független forrás — maga a CLA-dokumentum (a társalapító, philippemnoel publikus gist-je, 2024-01-25), amely a tág szerzői jogi engedményt adja meg, ami a fenti kettős licencelést jogilag lehetővé teszi:

> „Grant of Copyright License. […] You hereby grant to the Company and to recipients of software distributed by the Company a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable copyright license to reproduce, prepare derivative works of, publicly display, publicly perform, sublicense, and distribute Your Contributions and such derivative works."

Forrás: https://gist.github.com/philippemnoel/5ba3a20230bc1c3c0ae89caeb0597f4a (hivatkozva a `CONTRIBUTING.md`-ben is, mint „CLA Assistant website": https://cla-assistant.io/paradedb/paradedb)

### 4. Licenctörténet: „AGPL a kezdetektől" és a `pg_analytics` PostgreSQL License

A `pg_analytics` (korábban `pg_lakehouse`) repó `LICENSE` fájlja (nyers fájl, `curl`, 2026-09-22, HTTP 200):

> „The PostgreSQL License
>
> Copyright (c) 2025, ParadeDB
>
> Permission to use, copy, modify, and distribute this software and its documentation for any purpose, without fee, and without a written agreement is hereby granted…"

Forrás: https://raw.githubusercontent.com/paradedb/pg_analytics/dev/LICENSE

Az archiválás dátuma két, egymástól független módon igazolt:

1. GitHub repó-metaadat (Exa-fetch, 2026-09-22): „Status: ARCHIVED", „This repository was archived by the owner on Mar 19, 2025. It is now read-only." — forrás: https://github.com/paradedb/pg_analytics és https://github.com/paradedb/pg_analytics/releases
2. Az utolsó kiadási tag időbélyege pontosan egybevág: „v0.3.7 — Published: 2025-03-19T19:27:38Z — feat: Final release" — forrás: https://github.com/paradedb/pg_analytics/releases/tag/v0.3.7

Egy harmadik, tartalmilag konzisztens (bár azonos cégtől, más aldomainről származó) forrás a döntés indoklását is adja:

> „On April 2, 2025, we will be deprecating `pg_analytics` […] The `pg_analytics` repository will be archived and will no longer be maintained. […] This decision was made because our work on Postgres analytics is being done in our primary extension, `pg_search`."

Forrás: https://paradedb-dev.mintlify.site/changelog/0.15.9

Az „AGPL a kezdetektől" állítás forrása a cég saját, 2024. augusztusi blogbejegyzése:

> „ParadeDB has been licensed under the GNU Affero General Public License 3.0 — also known as AGPL — from day one."

Forrás: https://www.paradedb.com/blog/agpl

Ez **nem független, utólagos (kb. 1 évvel az alapítás után írt) önbevallás** — 2023-as, a céghez nem köthető, korabeli forrás nem található rá (a Wayback Machine ebben a környezetben blokkolva volt, és az Exa-találatok között sem szerepelt ilyen). A `pg_analytics` esete ugyanakkor bizonyítja, hogy **nem minden ParadeDB-komponens** volt/és AGPL — csak a fő motor.

### 5. Neon — `pg_search` kivezetése

Neon hivatalos changelog-bejegyzés (2026-04-03, Exa-fetch):

> „### pg_search deprecation
> Neon support for the `pg_search` extension is deprecated. As of **March 19, 2026**, it is not available for **new** Neon projects.
> If you already use `pg_search`: you will continue to have access to the extension on your existing projects."

Forrás: https://neon.com/docs/changelog/2026-04-03

A migrációs útmutató a teljes megszűnés dátumát adja meg:

> „`pg_search` (ParadeDB) is deprecated on Neon: new installs are blocked, and **existing installs will be removed on September 21, 2026**."
>
> „Once your queries run on `lakebase_text` […], drop `pg_search` ahead of the September 21, 2026 removal."

Forrás: https://neon.com/docs/extensions/migrate-pg-search-to-lakebase-text

Egy harmadik, tőle független forrás (felhasználói GitHub-vita) megerősíti a piaci hatást is:

> „Neon has stopped allowing new `pg_search` installations and says existing installations will be removed in September 2026. This has already caused some new self-hosted deployments to fail during database migration."

Forrás: https://github.com/lobehub/lobehub/issues/18303

### 6. `pg_textsearch` (Timescale/TigerData) érettsége

Licenc — nyers fájl (`curl`, 2026-09-22, HTTP 200):

> „The PostgreSQL License
> Permission to use, copy, modify, and distribute this software and its documentation for any purpose, without fee, and without a written agreement is hereby granted…"

Forrás: https://raw.githubusercontent.com/timescale/pg_textsearch/main/LICENSE

Verzió és dátum (Exa-fetch, GitHub release-oldal, közvetlen, 2026-09-22):

> „# v1.4.0
> Published: 2026-08-18T17:05:02Z
> * Optimizations for top-K queries with a WHERE filter (aka faceted search) yielding significant (up to 5X) speedups […]
> * Chinese-language support via zhparser
> * Robustness improvements for large corpuses"

Forrás: https://github.com/timescale/pg_textsearch/releases/tag/v1.4.0

Támogatott Postgres-verziók (README, Exa-fetch):

> „pg_textsearch supports PostgreSQL 17 and 18. PostgreSQL 19 (beta) is supported on a best-effort basis while it is in beta; its CI is allowed to fail and prebuilt binaries are not published for it yet."

Forrás: https://github.com/timescale/pg_textsearch/blob/main/README.md — ez **szűkebb** támogatott sáv, mint a `pg_search` PG 15–18 tartománya.

BM25: valódi, konfigurálható BM25-rangsorolás (`k1`, `b` paraméterek, Block-Max WAND gyorsítás):

> „BM25 ranking with configurable `k1` and `b`", „Fast top-k queries with Block-Max WAND"

Forrás: https://github.com/timescale/pg_textsearch (README)

**Magyar nyelv — igazolva.** A README saját, explicit felsorolása a támogatott Postgres text-search-konfigurációkról tartalmazza a magyart:

> „### Text Search Configurations
> Available configurations depend on your Postgres installation:
> ```
> # SELECT cfgname FROM pg_ts_config;
>   cfgname
> ------------
>  simple
>  arabic
>  armenian
>  …
>  hungarian
>  …
>  yiddish
> (29 rows)
> ```
> Further language support is available via extensions such as [zhparser]."

Forrás: https://github.com/timescale/pg_textsearch/blob/main/README.md

Érettség/kor: a Tiger Data (korábban TimescaleDB) saját blogja szerint az előzetes (preview) kiadás 2025-10-23-án jelent meg:

> „We're announcing the preview release of a PostgreSQL extension built specifically for this third epoch…"

Forrás: https://www.tigerdata.com/blog/introducing-pg_textsearch-true-bm25-ranking-hybrid-retrieval-postgres (2025-10-23)

Vagyis a projekt a kutatás időpontjában (2026-09-22) **kevesebb, mint 11 hónapja** létezik nyilvánosan, jelenlegi verziója v1.4.0 — a v1.0.0-tól v1.4.0-ig gyors, havi-kéthavi kiadási ütemben fejlesztik (a releases-lista szerint v1.0.0, v1.1.0, v1.2.0, v1.3.0, v1.3.1, v1.4.0 egymást követik néhány hetes-hónapos távolságokban), de érettségben (támogatott PG-verziók száma, kiadások kora) egyértelműen fiatalabb, mint a `pg_search`.

### 7. AGPL-3.0 13. szakasz és a ParadeDB saját nyilatkozata

A hivatalos GNU-szöveg (`curl`, https://www.gnu.org/licenses/agpl-3.0.txt, 2026-09-22, HTTP 200), szó szerint:

> „13. Remote Network Interaction; Use with the GNU General Public License.
>
> Notwithstanding any other provision of this License, if you modify the Program, your modified version must prominently offer all users interacting with it remotely through a computer network (if your version supports such interaction) an opportunity to receive the Corresponding Source of your version by providing access to the Corresponding Source from a network server at no charge, through some standard or customary means of facilitating copying of software. This Corresponding Source shall include the Corresponding Source for any work covered by version 3 of the GNU General Public License that is incorporated pursuant to the following paragraph.
>
> Notwithstanding any other provision of this License, you have permission to link or combine any covered work with a work licensed under version 3 of the GNU General Public License into a single combined work, and to convey the resulting work. The terms of this License will continue to apply to the part which is the covered work, but the work with which it is combined will remain governed by version 3 of the GNU General Public License."

Ez **szóról szóra megegyezik** a ParadeDB repó saját `LICENSE` fájljával (`curl`, https://raw.githubusercontent.com/paradedb/paradedb/main/LICENSE, ugyanaz a szövegrész, sorindex 540–559) — tehát a ParadeDB nem módosította a szabvány AGPL-3.0-szöveget.

**ParadeDB-saját nyilatkozat a témában — nem található.** Sem a „Why We Picked AGPL" blogbejegyzés (https://www.paradedb.com/blog/agpl), sem a hivatalos dokumentáció-index (`llms.txt`), sem az Enterprise-oldal nem tér ki kifejezetten arra, hogy egy különálló folyamatként futó, a `pg_search`-öt nem módosító, csak SQL-en/wire protocol-on kommunikáló alkalmazásra mi vonatkozik. Célzott Exa-keresések (pl. „ParadeDB does not require open source your application AGPL SQL wire protocol") sem hoztak fel ilyen hivatalos állásfoglalást.

Az egyetlen, témába vágó — de **nem hivatalos dokumentáció, csupán fórum-hozzászólás** — forrás egy 2024-es Hacker News-komment, amelyet a poszt szerzője a ParadeDB társalapítójaként azonosít:

> „We don't believe AGPL should prevent you from self-hosting for your own internal usage. […] We spent a lot of time evaluating which license to use, and decided to follow the footsteps of Citus Data and go with a standard OSS license while ensuring that we can't be hosted on public clouds without a partnership."

Forrás: https://news.ycombinator.com/item?id=38849928

Ez a komment a **saját-hosztolásról és a felhő-szolgáltatók kizárásáról** szól, nem kifejezetten a „csak SQL-en beszélő, változatlan kliens" esetről — így nem tekinthető az állításban feltett kérdésre adott közvetlen válasznak. A kérdés tehát nyitott marad: **nincs ParadeDB-saját, hivatalos nyilatkozat** erre a konkrét forgatókönyvre.

Kiegészítésül, a GNU hivatalos FAQ-ja (`curl`, https://www.gnu.org/licenses/gpl-faq.html, 2026-09-22) két, elméletileg releváns, de egymástól különálló pontot tartalmaz:

> „AGPLv3ServerAsUser: […] AGPLv3 requires a program to offer source code to 'all users interacting with it remotely through a computer network.' It doesn't matter if you call the program a 'client' or a 'server,' the question you need to ask is whether or not there is a reasonable expectation that a person will be interacting with the program remotely over a network."

> „MereAggregation: […] Where's the line between two separate programs, and one program with two parts? This is a legal question, which ultimately judges will decide. We believe that a proper criterion depends both on the mechanism of communication (exec, pipes, rpc, function calls within a shared address space, etc.) and the semantics of the communication…"

Ezek az FSF általános GPL-családi elvei, nem ParadeDB-specifikus és nem is kifejezetten az „adatbázis-kiterjesztés + tőle különálló, wire protocol-on kommunikáló kliens" esetre szabott állásfoglalások.

---

## Amit ez a döntésre jelent

- A licenc-alapállítás (AGPL-3.0, ma is érvényes, szó szerint megegyezik a hivatalos GNU-szöveggel) minden vizsgált forrásban konzisztens és megkérdőjelezhetetlen.
- A „legfrissebb stabil kiadás" pontos száma és dátuma forrásfüggő: a strukturált, géppel olvasható registry-k (Docker Hub API, PGXN) egyöntetűen v0.25.9-et (2026-09-11) mutatnak, míg a GitHub saját „latest release" felülete (a lekérés időpontjában) egy korábbi, v0.25.6 (2026-08-27) címkét adott vissza — ez vagy crawler-cache-probléma, vagy a GitHub „latest" jelölésének valamilyen sajátossága (pl. pre-release/draft-jelölés), de nem sikerült egyértelműen tisztázni.
- Az Enterprise-Community különbség a keresési funkciók szintjén valóban nulla (BM25, hibrid keresés, highlighting stb. mindkettőben ✅), a tényleges különbség pontosan a replikáció/HA/olvasó-replika kérdésére szűkül — ezt egy éles GitHub-hibaüzenet is alátámasztja szó szerint. Ugyanakkor az Enterprise emellett licenc-váltást (copyleft feloldása) és nem részletezett zárt forráskódú funkciókat is tartalmaz, amit egy tisztán funkcionális összehasonlítás elfed.
- A `pg_analytics` PostgreSQL License alatti működése és 2025-03-19-i archiválása egyértelműen, több, egymást megerősítő ponttal (repó-státusz, utolsó release időbélyege, changelog-bejegyzés) igazolt tény; az „AGPL a kezdetektől" állítás viszont kizárólag a cég saját, utólagos (2024-es) retrospektív nyilatkozatán nyugszik, független 2023-as forrás nélkül.
- A Neon-kivezetés pontos dátumai (2026-03-19 új projektekre, 2026-09-21 teljes megszűnés) két különböző Neon-dokumentációs oldalon és egy független, harmadik fél (felhasználói GitHub-vita) által is megerősítve — ez a legerősebben alátámasztott állítás a hét közül.
- A `pg_textsearch` valódi, aktívan fejlesztett, PostgreSQL License alatti BM25-alternatíva, amely kimutathatóan támogatja a magyar nyelvet (a Postgres 29 beépített `text search configuration`-je között), de PG 17–18-ra korlátozódik (pg_search PG 15–18-hoz képest szűkebb) és kevesebb mint egy éve létezik nyilvánosan.
- A ParadeDB semmilyen hivatalos csatornán nem foglal állást abban a konkrét kérdésben, hogy egy tőle különálló folyamatként futó, csak SQL/wire protocol-on kommunikáló, a `pg_search`-öt nem módosító alkalmazásra vonatkozik-e az AGPL 13. §-a — ez nyitott értelmezési kérdés marad, amit sem az FSF általános FAQ-ja, sem a ParadeDB dokumentációja nem old fel expliciten erre a konkrét architektúrára.

---

## Meglátogatott linkek

| Cím | URL | Tier | Eszköz |
|---|---|---|---|
| paradedb/paradedb — LICENSE (nyers) | https://raw.githubusercontent.com/paradedb/paradedb/main/LICENSE | T1 | curl |
| paradedb/paradedb — Cargo.toml (nyers) | https://raw.githubusercontent.com/paradedb/paradedb/main/Cargo.toml | T1 | curl |
| paradedb/paradedb — CONTRIBUTING.md (nyers) | https://raw.githubusercontent.com/paradedb/paradedb/main/CONTRIBUTING.md | T1 | curl |
| pg_analytics — LICENSE (nyers) | https://raw.githubusercontent.com/paradedb/pg_analytics/dev/LICENSE | T1 | curl |
| pg_textsearch — LICENSE (nyers) | https://raw.githubusercontent.com/timescale/pg_textsearch/main/LICENSE | T1 | curl |
| pg_textsearch — README.md (nyers) | https://raw.githubusercontent.com/timescale/pg_textsearch/main/README.md | T1 | curl |
| GNU AGPL-3.0 hivatalos szöveg | https://www.gnu.org/licenses/agpl-3.0.txt | T1 | curl |
| GNU GPL FAQ | https://www.gnu.org/licenses/gpl-faq.html | T1 | curl |
| Docker Hub API — paradedb/paradedb tags | https://hub.docker.com/v2/repositories/paradedb/paradedb/tags | T1 | curl (API) |
| GitHub API — releases/latest (403, nem elérhető) | https://api.github.com/repos/paradedb/paradedb/releases/latest | — | curl (sikertelen) |
| GitHub — releases/latest | https://github.com/paradedb/paradedb/releases/latest | T1 | Exa fetch |
| GitHub — paradedb/paradedb főoldal | https://github.com/paradedb/paradedb | T1 | Exa search |
| GitHub — paradedb/pg_analytics | https://github.com/paradedb/pg_analytics | T1 | Exa search |
| GitHub — pg_analytics releases | https://github.com/paradedb/pg_analytics/releases | T1 | Exa search |
| GitHub — pg_analytics v0.3.7 tag | https://github.com/paradedb/pg_analytics/releases/tag/v0.3.7 | T1 | Exa search |
| GitHub — pg_textsearch releases | https://github.com/timescale/pg_textsearch/releases | T1 | Exa fetch |
| GitHub — pg_textsearch v1.4.0 tag | https://github.com/timescale/pg_textsearch/releases/tag/v1.4.0 | T1 | Exa fetch |
| GitHub — pg_textsearch README | https://github.com/timescale/pg_textsearch/blob/main/README.md | T1 | Exa search |
| GitHub issue #6007 — replikáció/standby hiba | https://github.com/paradedb/paradedb/issues/6007 | T1 | Exa search |
| ParadeDB — Enterprise doksi | https://docs.paradedb.com/deploy/enterprise | T1 | Exa fetch |
| ParadeDB — Guarantees doksi | https://docs.paradedb.com/welcome/guarantees | T1 | Exa fetch |
| ParadeDB — Deploy overview | https://www.paradedb.com/docs/deploy/overview | T1 | Exa search |
| ParadeDB — „Why We Picked AGPL" blog | https://www.paradedb.com/blog/agpl | T1 | Exa search |
| ParadeDB — CLA gist (philippemnoel) | https://gist.github.com/philippemnoel/5ba3a20230bc1c3c0ae89caeb0597f4a | T1 | Exa fetch |
| ParadeDB — CLA Assistant oldal | https://cla-assistant.io/paradedb/paradedb | T2 | Exa fetch |
| ParadeDB-dev changelog 0.15.9 (pg_analytics deprecation) | https://paradedb-dev.mintlify.site/changelog/0.15.9 | T2 | Exa search |
| PGXN — pg_search 0.25.9 | https://pgxn.org/dist/pg_search/0.25.9/ | T1/T2 | Exa fetch |
| PGXN — pg_search (index) | https://pgxn.org/dist/pg_search/ | T1/T2 | Exa fetch |
| Neon — changelog 2026-04-03 | https://neon.com/docs/changelog/2026-04-03 | T1 | Exa search |
| Neon — migrate pg_search → lakebase_text | https://neon.com/docs/extensions/migrate-pg-search-to-lakebase-text | T1 | Exa search |
| Neon — pg_search extension doksi | https://neon.com/docs/extensions/pg_search | T1 | Exa search |
| Neon website repo — pg_search.md | https://github.com/neondatabase/website/blob/main/content/docs/extensions/pg_search.md | T1 | Exa search |
| LobeHub GitHub issue — Neon pg_search removal hatása | https://github.com/lobehub/lobehub/issues/18303 | T2 | Exa search |
| Tiger Data — pg_textsearch bejelentő blog | https://www.tigerdata.com/blog/introducing-pg_textsearch-true-bm25-ranking-hybrid-retrieval-postgres | T1 | Exa search |
| Tiger Data — pg_textsearch doksi | https://www.tigerdata.com/docs/use-timescale/latest/extensions/pg-textsearch | T1 | Exa search |
| Hacker News — ParadeDB alapítói komment (AGPL/self-hosting) | https://news.ycombinator.com/item?id=38849928 | T2 | Exa search |
| api-evangelist/paradedb (nem hivatalos, harmadik fél) | https://github.com/api-evangelist/paradedb | T3 (nem használt bizonyítékként) | Exa search |
