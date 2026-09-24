# ELL04 — TypeScript / Bun / Drizzle / Better Auth ellenőrzés

> **Módszertani megjegyzés.** A keresést kizárólag az Exa eszközökkel (`mcp__Exa__web_search_exa`, `mcp__Exa__web_fetch_exa`) végeztem, a `_ell_kozos.txt` előírása szerint. `curl`-t kizárólag nyers fájlok (npm registry JSON, GitHub raw `package.json`/`CHANGELOG.md`) szó szerinti, gépi lekérdezésére használtam. A `anthropic-skills:deep-web-research` skill alügynök-indítási képessége ebben a környezetben sem érhető el (nincs `Agent`/`Task` eszköz), ezért — a `sq06.md`-hez hasonlóan — degradált módban, egyetlen szálon dolgoztam; nem készült `.research/` evidence-vault, nem futott Opus-szintézis/Sonnet-verifikáció. Minden verdikthez törekedtem két, egymástól független elsődleges forrásra (npm registry + GitHub, vagy két különböző hivatalos doksi-oldal); ahol ez nem sikerült, azt külön jelzem.

---

## Verdikt-összefoglaló

| # | Állítás | Verdikt | Egy mondat |
|---|---|---|---|
| 1 | Létezik hivatalos `@paradedb/drizzle-paradedb` (MIT), peer: `drizzle-orm@1.0.0-rc.4`; legfrissebb verzió/dátum | **IGAZOLVA** | Az npm registry és a GitHub `CHANGELOG.md` egybehangzóan: legfrissebb **0.5.0**, publikálva **2026-08-21**, MIT licenc, peer `drizzle-orm: "1.0.0-rc.4"`. |
| 2a | A Drizzle stabil „latest" 2026-09 közepén **0.45.3** (kit **0.31.11**), az 1.0 még RC | **IGAZOLVA** | Az npm registry `dist-tags` szerint `latest`=0.45.3 / 0.31.11 (publikálva 2026-09-21), `rc`=1.0.0-rc.4, `rc5`=1.0.0-rc.5 (2026-09-09) — a friss RC-ág is még RC, nem stabil. |
| 2b | Mikorra ígérik a Drizzle 1.0-t (hivatalos forrás) | **NEM ELDÖNTHETŐ** | Nincs friss, konkrét hivatalos dátum; a Drizzle-alapító egy 2025 végi becslése („v1 beta ősszel, a stabil ugyanolyan idősávban") azóta bő egy éve nem teljesült, a hivatalos Roadmap-oldal és a nyitott „when will we have v1.0.0?" issue sem ad dátumot. |
| 2c | Van-e mód a ParadeDB-t a stabil Drizzle-lel, hivatalos csomag nélkül használni (`index().using('paradedb', …)` + nyers `sql`) | **IGAZOLVA** | A `PgIndexMethod` típus és a `.using()` metódus, amely tetszőleges stringet elfogad, már egy 2024/2025-ös (stabil ág előtti) commitban is jelen volt változatlan formában, és a nyers `sql` sablon-literál a Drizzle mag része — technikailag megvalósítható a hivatalos RC-csomag nélkül is, bár típusbiztonság és a csomag saját teszt-lefedettsége nélkül. |
| 3 | Drizzle natívan támogatja a `vector` oszlopot, távolságfüggvényeket, HNSW-indexet — stabil verzióban is, nem csak RC-ben | **IGAZOLVA** | A hivatalos „Vector similarity search" útmutató explicit minimumverziót ad: „You should have `drizzle-orm@0.31.0` and `drizzle-kit@0.22.0` or higher" — ez a jelenlegi 0.45.3/0.31.11 stabil ág messze fölötti régi minimum, tehát a funkció a stabil ágban is megvan, nem RC-exkluzív. |
| 4a | Better Auth Drizzle-adapter: Drizzle 1.0 RC-vel csak Better Auth 1.7 RC kompatibilis (PR #9489) | **RÉSZBEN (elavult állítás)** | A PR #9489 valóban a Better Auth 1.7-es vonalán (először `1.7.0-beta.10`-ben) vezette be a Drizzle v1-kompatibilis `relations-v2` adaptert — de mára (2026-09-22) a Better Auth 1.7 **stabil** kiadás (npm „latest" = 1.7.5, 2026-09-14), tehát az állítás „csak RC" korlátozása ma már nem igaz. |
| 4b | Stabil Better Auth + stabil Drizzle (0.45) + Postgres működik-e | **IGAZOLVA** | A Better Auth 1.7.5 npm `package.json` `peerDependencies` mezője explicit: `"drizzle-orm": "^0.45.2 \|\| >=1.0.0-rc.1 <2.0.0"` — azaz a stabil 0.45.x ág hivatalosan, változatlanul támogatott (ez volt az egyetlen támogatott sáv is a korábbi 1.6.x vonalon). |
| 5a | `Bun.sql` Postgres-kliens érett-e, hivatalos státusz | **RÉSZBEN** | Hivatalosan promózott, benchmarkolt, „production" címkével kommunikált funkció, de a saját GitHub tracking issue-ja (#15088) még **nyitva** van, és 2026 június–július folyamán (a kutatás időpontjához képest 2-3 hónapja) is kerültek elő és javultak konkurenciafüggő adatvesztési/leállási hibák (pl. #32004, a hozzá tartozó #32772 javítás, #33665). |
| 5b | Mely Drizzle Postgres-driverek támogatottak Bun alatt stabilan (postgres.js, node-postgres, bun-sql) | **RÉSZBEN** | A hivatalos Bun-doksi FAQ-ja mindhármat jóváhagyja („You can use npm packages like postgres.js … pg, and node-postgres in Bun … They're great options"), és a Drizzle mindhármat dokumentálja — de explicit, egy mondatos „ez a hivatalosan ajánlott" rangsorolást egyik forrás sem ad, és a `postgres.js`/Bun kombinációnak korábban (2024 végén) volt már lezárt regressziós hibája. |
| 6 | macOS-en a `bun:sqlite` a rendszer SQLite-ját használja, bővítmény nem tölthető be; igaz-e ma (Bun 1.4), és van-e dokumentált kerülőút (`Database.setCustomSQLite`) | **IGAZOLVA** | A hivatalos, ma lekért Bun-dokumentáció szó szerint ezt írja, és két 2026 augusztusi GitHub-issue (#38647, #38772) kifejezetten Bun **1.3.14 / 1.4.0-canary** alatt reprodukálja a hibát; a `Database.setCustomSQLite(path)` a hivatalosan dokumentált és több független (Bun-doksi, `sqlite-vec` repó) forrásban is megerősített kerülőút. |

---

## Állításonként

### 1. `@paradedb/drizzle-paradedb` — hivatalos csomag, MIT, peer `drizzle-orm@1.0.0-rc.4`, legfrissebb verzió

Az npm registry API közvetlen lekérdezése (`registry.npmjs.org/@paradedb/drizzle-paradedb`):

> `"dist-tags":{"latest":"0.5.0"}` … a `0.5.0` verzió `"modified"` időbélyege: `2026-08-21T14:10:27.851Z`.
(https://registry.npmjs.org/@paradedb/drizzle-paradedb)

A publikált `0.5.0` verzió saját metaadata (`registry.npmjs.org/@paradedb/drizzle-paradedb/0.5.0`):

> `"license":"MIT"`, `"peerDependencies":{"drizzle-orm":"1.0.0-rc.4"}`
(https://registry.npmjs.org/@paradedb/drizzle-paradedb/0.5.0)

Ezt független forrásként megerősíti a repó saját `CHANGELOG.md`-je (nyersen lekérve):

> „## [0.5.0] - 2026-08-21 ### Changed - Upgraded to Drizzle 1.0.0-rc.4."
(https://raw.githubusercontent.com/paradedb/drizzle-paradedb/main/CHANGELOG.md)

**Verdikt: IGAZOLVA.** Két, technikailag különböző lekérési útvonalon (npm registry JSON API, illetve a repó saját, verziózott changelog fájlja) egybehangzó adat: a csomag hivatalos, MIT licencű, legfrissebb verziója **0.5.0** (**2026-08-21**), amely a Drizzle **1.0.0-rc.4**-et írja elő peer-dependencyként. (A `sq06.md` korábbi kutatása ugyanezt találta a fő ágon; itt függetlenül, a publikált npm-verzión is megerősítettem.)

---

### 2a. Drizzle stabil „latest" 2026-09 közepén 0.45.3 (kit 0.31.11), az 1.0 még RC

Az npm registry API friss (a mai napon végzett) lekérdezése:

> `drizzle-orm` dist-tags: `"latest":"0.45.3"`, időbélyeg `2026-09-21T10:06:39.969Z`; `"rc":"1.0.0-rc.4"`; `"rc5":"1.0.0-rc.5-5935859"` (2026-09-09).
> `drizzle-kit` dist-tags: `"latest":"0.31.11"`, időbélyeg `2026-09-21T10:06:58.727Z`; `"rc":"1.0.0-rc.4"`.
(https://registry.npmjs.org/drizzle-orm, https://registry.npmjs.org/drizzle-kit)

**Verdikt: IGAZOLVA.** Az állítás pontos: a „latest" npm-tag 2026-09-21-i publikálással is a 0.45.3/0.31.11 stabil sorozatra mutat, míg az 1.0-s ág — még a legújabb `rc5` build is — release candidate státuszú.

### 2b. Mikorra ígérik a Drizzle 1.0-t (hivatalos forrás)

A hivatalos Roadmap-oldal (`orm.drizzle.team/roadmap`) felsorolja a hátralévő funkciókat („MSSQL support", „🎉 V1 RELEASE STREAM 🎉", „Down migrations, better rollbacks…", „MariaDB support" stb.), de **egyetlen konkrét dátumot sem** tartalmaz.
(https://orm.drizzle.team/roadmap)

A `drizzle-team/drizzle-orm` GitHub repóban nyitott kérdés:

> **[QUESTION] when will we have v1.0.0?** (#5660, nyitva, 2026-04-18 óta) — a közösségi válaszokban (nem maintainer) blokkoló hiányként a „down migrations" és a „Full RLS production ready support" szerepel; maintainer-válasz/dátum **nincs** a szálban.
(https://github.com/drizzle-team/drizzle-orm/issues/5660)

Egy korábbi, hivatalos maintainer-bejelentés (AndriiSherman, a Drizzle Team alapítója, tömeges issue-frissítő üzenetben, kb. 2025 vége):

> „We are hoping to get v1 for drizzle in beta this fall and same timeline for latest." … „Where it brings us: We are getting drizzle-orm into a new good shape where we can call it `drizzle-orm@1.0.0`!"
(https://github.com/drizzle-team/drizzle-orm/issues/1869, ugyanez megismételve: https://github.com/drizzle-team/drizzle-orm/issues/4760)

Ez a becslés (2025 ősz) **nem teljesült**: a `beta` tag csak 2026 elején vált release candidate-té (AndriiSherman, 2026-01-03: „This issue has been fixed in the `beta` tag, which serves as the release candidate for Drizzle v1"), és 2026-09-22-i állapot szerint (ld. 2a) még mindig RC-ben van, immár `rc.5`-nél.

**Verdikt: NEM ELDÖNTHETŐ.** Volt hivatalos, konkrét (ha nem is dátumszerű, hanem évszakos) ígéret — de az egy éve elavult, és azóta sem a Roadmap-oldal, sem a nyitott GitHub-kérdés nem tartalmaz újabb, hivatalos időbecslést. Harmadik, frissebb hivatalos nyilatkozatot (blog, X/Twitter) nem találtam a keresés során.

### 2c. Használható-e ParadeDB stabil Drizzle-lel, hivatalos csomag nélkül (`index().using('paradedb', …)` + nyers `sql`)

A Drizzle ORM `pg-core/indexes.ts` forrása egy, a jelenlegi 1.0 RC-ág előtti (stabil-korabeli) commit-változatban (`273c7807`) **szó szerint ugyanazt** a kódot tartalmazza, mint a jelenlegi `main`:

> „`export type PgIndexMethod = 'btree' | 'hash' | 'gist' | 'spgist' | 'gin' | 'brin' | 'hnsw' | 'ivfflat' | (string & {});`" … „**You can always specify any string you want in the method, in case Drizzle doesn't have it natively in its types**"
(https://github.com/drizzle-team/drizzle-orm/blob/273c7807/drizzle-orm/src/pg-core/indexes.ts, összevetve: https://raw.githubusercontent.com/drizzle-team/drizzle-orm/main/drizzle-orm/src/pg-core/indexes.ts)

A hivatalos Drizzle-dokumentáció (mintlify tükör, jelenlegi doksi-tartalom) is mutat `.using()`-mintát tetszőleges metódusnévvel (`gin`, `brin` stb.), külön RC-megjegyzés nélkül.
(https://drizzle-team-drizzle-orm.mintlify.app/schema/indexes)

**Verdikt: IGAZOLVA (technikai lehetőség).** Mivel az `.using(method, …)` API — amely a ParadeDB saját `paradedbIndex()` helperének is az alapja (ld. `sq06.md` 1.3 pontja) — már a stabil (RC előtti) Drizzle-ágban is jelen volt, és a nyers `sql` sablon-literál mindig elérhető volt/van, technikailag lehetséges `USING paradedb`/`bm25` indexet és `@@@`-lekérdezést stabil Drizzle-lel, a hivatalos `@paradedb/drizzle-paradedb` csomag nélkül is megvalósítani. **Korlát:** ezt konkrétan, végponttól végpontig (stabil `drizzle-kit@0.31.11` `generate`/`push` és tényleges ParadeDB migráció) senki hivatalos vagy közösségi forrás nem dokumentálja/tesztelte — a hivatalos csomag saját tesztje (ld. `sq06.md` 1.5 pont) kizárólag az RC `drizzle-kit/api-postgres`-t használja.

---

### 3. Drizzle natívan támogatja a `vector` oszlopot, távolságfüggvényeket, HNSW-indexet — stabil verzióban is?

A hivatalos „Vector similarity search with pgvector extension" útmutató (frissen lekérve):

> „You should have `drizzle-orm@0.31.0` and `drizzle-kit@0.22.0` or higher."
(https://orm.drizzle.team/docs/guides/vector-similarity-search)

Ugyanez az oldal a teljes mintát mutatja: `vector()` oszlop, `index('embeddingIndex').using('hnsw', table.embedding.op('vector_cosine_ops'))`, valamint `cosineDistance` a lekérdezésben — mindezt kifejezetten a fenti (0.31.0+) minimumverzió mellett.

A „PostgreSQL extensions" oldal (frissen lekérve) ugyanezt, kibővítve `halfvec`/`sparsevec`/`bit` típusokra és mind a hat távolságfüggvényre (`l2Distance`, `l1Distance`, `innerProduct`, `cosineDistance`, `hammingDistance`, `jaccardDistance`), valamint `hnsw`/`ivfflat` indexmintákra.
(https://orm.drizzle.team/docs/extensions/pg)

**Verdikt: IGAZOLVA.** Két, egymástól független hivatalos doksi-oldal egybehangzóan, RC-specifikus megjegyzés nélkül mutatja be a funkciót, és az explicit minimumverzió (0.31.0/0.22.0) jóval a jelenlegi stabil `latest` (0.45.3/0.31.11) alatt van — tehát a pgvector-integráció **régóta a stabil ág natív, beépített része**, nem RC-kizárólagos újdonság.

---

### 4a. Better Auth Drizzle-adapter Postgres-szel: Drizzle 1.0 RC-vel csak Better Auth 1.7 RC kompatibilis (PR #9489)?

A Better Auth `packages/drizzle-adapter/CHANGELOG.md` (1.7.0 bejegyzés):

> „#9489 `ea06c5a` Thanks @ping-maxwell! - Add a new `@better-auth/drizzle-adapter/relations-v2` entry point for projects using Drizzle Relations v2."
(https://github.com/better-auth/better-auth/blob/main/packages/drizzle-adapter/CHANGELOG.md, ill. konkrét commit: https://github.com/better-auth/better-auth/blob/c3688ba/packages/drizzle-adapter/CHANGELOG.md)

Harmadik fél (Dosu/Devin) összefoglalója, amely a hivatalos changelogra és a PR-re hivatkozik:

> „Better Auth added native support in `@better-auth/drizzle-adapter@1.7.0-beta.10` (via PR #9489, included in the v1.7 release)." … táblázat: „≥ 1.7.0 (RC+) | ✅ Default adapter | ✅ Use `/relations-v2` entry point"
(https://app.dosu.dev/cdda13d9-dd27-4d31-b09a-5d8bec92de21/documents/d44cb4d1-c83b-43d5-998a-c0a6dec2b641 — **T3, csak tájékozódásra**, a tényt az alábbi elsődleges forrásokkal ellenőriztem)

**Ám az npm registry szerint a Better Auth 1.7-es vonal mára stabil kiadás:**

> `better-auth` dist-tags: `"latest":"1.7.5"` (publikálva **2026-09-14**), `"rc":"1.7.0-rc.6"` (2026-08-14, „befagyott", a `latest` már elhagyta), `"release-1.6":"1.6.33"`.
(https://registry.npmjs.org/better-auth)

> `better-auth@1.7.0` publikálási időbélyege: `2026-08-18T00:10:16.757Z`.
(https://registry.npmjs.org/better-auth, `time` mező)

A hivatalos Better Auth blog is 1.7-et stabil kiadásként kommunikálja:

> „Better Auth 1.7" — publikálva **2026-08-17**. „We introduced the first part of this work in [the] 1.7 release candidate. … Follow the 1.7 upgrade guide for the migration steps."
(https://better-auth.com/blog/1-7)

**Verdikt: RÉSZBEN (elavult állítás).** Az eredeti állítás ténye — hogy a PR #9489 és a Drizzle-v1-kompatibilitás először a Better Auth **1.7 release candidate**-jében jelent meg — igaz volt a maga idejében (a fejlesztés `1.7.0-beta.10`-ben kezdődött, majd RC-ken át futott). **De 2026-09-22-i állapot szerint a Better Auth 1.7 már nem RC, hanem stabil, „latest"-tagelt kiadás** (jelenleg 1.7.5, 2026-09-14), tehát az „csak RC-vel kompatibilis" korlátozás **ma már nem helytálló**.

### 4b. Stabil Better Auth + stabil Drizzle (0.45) + Postgres működik-e?

A Better Auth **1.7.5** (jelenlegi „latest") npm-csomagjának `peerDependencies` mezője (közvetlen npm registry lekérdezés):

> `"drizzle-orm": "^0.45.2 || >=1.0.0-rc.1 <2.0.0"`, `"drizzle-kit": ">=0.31.4 || >=1.0.0-beta.1"`, `"pg": "^8.0.0"`
(https://registry.npmjs.org/better-auth/1.7.5)

Ezt megerősíti a PR, amely ezt a tartományt bevezette:

> „Expand `drizzle-orm` peer range in `packages/better-auth/package.json` to `^0.45.2 || >=1.0.0-rc.1 <2.0.0` and align `pnpm-lock.yaml` specifier to support 1.0 RCs and avoid peer conflicts; installs still resolve to `0.45.2` unless a 1.0 RC is present." (#10501, mergelve, review: „Thank you! I'm merging this 🫡")
(https://github.com/better-auth/better-auth/pull/10501)

Második, független megerősítés: a korábbi, **1.6.33** (`release-1.6` tag) `peerDependencies`-je is `"drizzle-orm": "^0.45.2"`-t ír elő — azaz a stabil 0.45.x sáv már a Drizzle-v1-támogatás bevezetése **előtt** is az egyetlen, hivatalosan deklarált, támogatott verzió volt.
(https://registry.npmjs.org/better-auth/1.6.33)

A Drizzle-adapter dokumentációja (`provider: "pg"`) a Postgres-módot már korábban is (RC-től függetlenül) leírta:
(https://better-auth.com/docs/adapters/drizzle — idézve `sq06.md` 4.1 pontjában)

**Verdikt: IGAZOLVA.** Két, egymástól független npm-lekérdezés (1.7.5 és a párhuzamosan karbantartott 1.6.33 branch) és a hivatalos PR-leírás egybehangzóan igazolja: a **stabil** Better Auth (akár a jelenlegi 1.7.x, akár a korábbi 1.6.x vonal) + **stabil** Drizzle (`^0.45.2`) + Postgres (`pg` provider) kombináció **hivatalosan, explicit peer-dependency szinten támogatott és működő** — ez volt/maradt az alapértelmezett, „biztonságos" konfiguráció.

---

### 5a. `Bun.sql` Postgres-kliens érettsége, hivatalos státusz

A Bun hivatalos főoldala (`bun.com`, frissen lekérve) marketing-szinten éretten kommunikálja:

> „## Bun in production … `bun run dev` for `bun run dev` and keep shipping" … „`Bun.sql` Postgres, MySQL, SQLite" … benchmark-táblázat: „Bun v1.4 | 20,243 queries/s | 80 MB" (vs. Node.js 10,000 queries/s, Deno 10,406 queries/s).
(https://bun.com/)

Ugyanakkor a hivatalos GitHub tracking issue jelenleg is **nyitva** van:

> **„`Bun.sql` tracking issue (Postgres client)"** (#15088) — State: **open**, utolsó frissítés 2026-01-05 (majd további issue-k hivatkoznak rá 2026 áprilisban, májusában).
(https://github.com/oven-sh/bun/issues/15088)

2026 június–júliusban (a kutatás időpontjához, 2026-09-22-höz képest **2–3 hónapja**) több, konkurenciafüggő, adatvesztést/leállást okozó hibát találtak és javítottak:

> **#32004** „SQL: connection pool stalls under concurrent begin() + parameterized queries" — bejelentve 2026-06-09, javítás-ellenőrzés: „Verified on main … the issue's repro script … completed 40/40 consecutive runs with no hang. The same script against a build predating both PRs (1.4.0-canary.1+1498d7b77) hung 2/10."
(https://github.com/oven-sh/bun/issues/32004)

> **#32772** „sql(postgres): stop sending a redundant Sync after a simple Query" — mergelve 2026-06-26. „`Bun.SQL` (Postgres) silently delivers another query's rows to the wrong query, with no error, when a simple-protocol query runs concurrently with a not-yet-prepared parameterized query on the same connection."
(https://github.com/oven-sh/bun/pull/32772)

> **#33665** „Bun SQL prepared statement cache causes intermittent Postgres decode/protocol errors under concurrency" — bejelentve 2026-07-07, Bun 1.3.14 ellen, root cause megerősítve és más PR-hez kapcsolva javításra.
(https://github.com/oven-sh/bun/issues/33665)

**Verdikt: RÉSZBEN.** A `Bun.sql` hivatalosan promózott, benchmarkolt, aktívan fejlesztett Postgres-kliens, alapszintű használatra funkcionális és gyors — de a saját tracking issue-ja nyitva van, és a kutatás időpontjához képest néhány hónapon belül is kerültek elő és javultak **helyességi** (nem csak teljesítmény-) hibák konkurens/pooling forgatókönyvekben. Ez arra utal, hogy 2026-09-22-i állapotában **aktívan érő, de még nem lezárt/nem "kőbe vésett" stabilitású** komponens — explicit „production-ready" vagy „stabil API" hivatalos minősítést egyik forrásban sem találtam, csak implicit (marketing-szintű) promóciót.

### 5b. Mely Drizzle Postgres-driverek támogatottak Bun alatt stabilan (postgres.js, node-postgres, bun-sql)?

A hivatalos Bun SQL-dokumentáció FAQ-szekciója (frissen lekérve, `docs/runtime/sql.mdx`):

> „## Frequently Asked Questions … You can use npm packages like postgres.js, pg, and node-postgres in Bun … They're great options."
(https://github.com/oven-sh/bun/blob/88a63988/docs/runtime/sql.mdx)

A Drizzle hivatalos „Bun SQL" oldala:

> „Drizzle ORM natively supports `bun sql` module and it's crazy fast 🚀" — telepítés `drizzle-orm@rc`/`drizzle-kit@rc` csomagokkal.
(https://orm.drizzle.team/docs/connect-bun-sql — idézve `sq06.md` 3.2 pontjában)

A Drizzle „Get Started – PostgreSQL" oldala mindhárom drivert (`node-postgres`, `postgres.js`, „Bun SQL") felsorolja, rangsorolás nélkül.
(https://orm.drizzle.team/docs/get-started-postgresql — idézve `sq06.md` 3.3 pontjában)

Korábbi (2024 végi), már lezárt regresszió a `postgres.js`/Bun kombinációra:

> „postgres-js queries hang indefinitely on Bun 1.1.35+" (#15438) — Closed, javítás: PR #15543.
(https://github.com/oven-sh/bun/issues/15438)

**Verdikt: RÉSZBEN.** Mindhárom driver (`postgres.js`, `node-postgres`/`pg`, `Bun.sql`/`bun-sql`) hivatalosan dokumentált és a Bun saját FAQ-ja explicit jóváhagyja mindhármat („great options") — de **egyik forrás sem mond ki explicit, egyértelmű rangsorolást** arra, melyik a Bun alatt „hivatalosan javasolt" választás; a `bun-sql` Drizzle-integrációja emellett (ld. 2a/5a) még RC-csomagokhoz kötött, míg a `postgres.js`/`pg` a stabil Drizzle-lel is használható, saját (részben már javított) Bun-specifikus hibatörténettel.

---

### 6. macOS-en a `bun:sqlite` a rendszer SQLite-ját használja → bővítmény (pl. `sqlite-vec`) nem tölthető be; igaz-e ma (Bun 1.4), és van-e dokumentált kerülőút?

A hivatalos, **ma lekért** Bun SQLite-dokumentáció:

> „macOS users By default, macOS ships with Apple's proprietary build of SQLite, which doesn't support extensions. To use extensions, install a vanilla build of SQLite." … „To point `bun:sqlite` to the new build, call `Database.setCustomSQLite(path)` before creating any `Database` instances. (On other operating systems, this is a no-op.) Pass a path to the SQLite `.dylib` file, not the executable."
(https://bun.com/docs/runtime/sqlite.md)

Ugyanezt egy másik, önálló hivatalos API-referencia oldal is megerősíti:

> „On macOS, this requires linking a custom SQLite3 library because the Apple build of SQLite disables loading extensions. See `Database.setCustomSQLite`." … „Bun chooses the Apple build of SQLite on macOS because it brings a ~50% performance improvement."
(https://bun.com/reference/bun/sqlite/Database/loadExtension)

**Két friss (2026 augusztusi), a hiba jelenlegi fennállását igazoló GitHub-issue**, kifejezetten a kutatáshoz közeli Bun-verziókon reprodukálva:

> **#38647** „bun:sqlite: statically link Bun's bundled SQLite on macOS too" — „What version of Bun is running? **1.3.14 (also reproduces on 1.4.0-canary)**." … „The only documented workaround … requires every end user to `brew install sqlite` and call `Database.setCustomSQLite(path)`."
(https://github.com/oven-sh/bun/issues/38647, bejelentve 2026-08-14)

> **#38772** (ugyanaz a hiba, más bejelentő) — „What version of Bun is running? **1.3.14**." Mindkettőt a fenntartó-bot **#16717**-tel duplikátumként zárta le, amely maga **nyitva van** (state: open, utolsó frissítés 2026-08-16).
(https://github.com/oven-sh/bun/issues/38772, https://github.com/oven-sh/bun/issues/16717)

A dokumentált kerülőutat harmadik fél (a `sqlite-vec` hivatalos repója) is megerősíti, gyakorlati kóddal:

> „MacOS *might* have to do this, as the builtin SQLite library on MacOS doesn't allow extensions: `Database.setCustomSQLite('/usr/local/opt/sqlite3/lib/libsqlite3.dylib');`"
(https://github.com/asg017/sqlite-vec/issues/78, ill. https://github.com/asg017/sqlite-vec/blob/main/site/using/js.md)

**Ellentmondás/árnyalat, amit a keresés feltárt:** volt egy 2026 májusában **mergelt** hivatalos PR (#31293, „build: enable static SQLite by default on macOS"), amely a `staticSqlite` build-flag alapértékét `true`-ra állította macOS-en, és a hozzá tartozó issue-kommentár szerint ennek „side benefit"-je lett volna, hogy a `loadExtension()` „out of the box" működjön. **Ennek ellenére** a fent idézett #38647/#38772 issue-k **három hónappal később (2026 augusztus)**, kifejezetten Bun **1.3.14 és 1.4.0-canary** alatt **továbbra is reprodukálják** az eredeti hibát, és a **ma lekért** hivatalos dokumentáció is változatlanul az Apple-féle rendszer-SQLite-ot és a `setCustomSQLite` kerülőutat írja le. Ennek pontos okát (a build-flag nem került éles kiadásba, vagy más regresszió történt) a rendelkezésre álló források nem magyarázzák meg egyértelműen — ezt NEM ELDÖNTHETŐ részletként jelzem.

**Verdikt: IGAZOLVA.** A leírt probléma (macOS rendszer-SQLite → bővítmény nem tölthető be) a mai napig (Bun 1.4 vonal, beleértve a `1.4.0-canary`-t is) fennáll, hivatalos forrásból és két független, 2026 augusztusi GitHub-issue-ból is megerősítve; a dokumentált kerülőút (`Database.setCustomSQLite(path)`, Homebrew-SQLite `.dylib`-re mutatva) ma is a hivatalos és a közösségi (pl. `sqlite-vec`) dokumentáció szerint is érvényes és működő megoldás.

---

## Amit ez a döntésre jelent

1. A ParadeDB hivatalos Drizzle-csomagja (0.5.0, 2026-08-21, MIT) és a Drizzle 1.0 közötti kötés **ma is fennáll**: a csomag peer-dependencyje mereven `1.0.0-rc.4`-hez van kötve, miközben az npm „latest" stabil Drizzle 0.45.3/0.31.11.
2. Nincs friss, hivatalos, konkrét dátum a Drizzle 1.0 stabil megjelenésére; az egyetlen fellelhető hivatalos időbecslés (2025 ősz) régen lejárt, és a fejlesztés azóta is RC-fázisban van (jelenleg `rc.5`).
3. Technikailag lehetséges ParadeDB-indexet és `@@@`-lekérdezést a **stabil** Drizzle-lel, a hivatalos RC-kötött csomag nélkül megvalósítani (`index().using('paradedb', …)` + nyers `sql`), mert ez az API már a stabil ágban is jelen van — de ennek konkrét, gyakorlati (migrációgenerálási) működését senki nem dokumentálta/tesztelte nyilvánosan.
4. A pgvector-alapú vektoros keresés (oszloptípus, távolságfüggvények, HNSW/IVFFlat index) **régóta, a stabil Drizzle-ágban is** natívan elérhető (min. 0.31.0/0.22.0 óta) — ez nem függ a Drizzle 1.0 RC-ágtól.
5. A Better Auth + Drizzle + Postgres kompatibilitási kép **időközben megváltozott** azóta, hogy a „csak 1.7 RC" megállapítás született: a Better Auth 1.7 mára stabil kiadás, és explicit peer-dependency-szinten egyszerre támogatja mind a stabil Drizzle 0.45.x-et, mind a Drizzle 1.0 RC-t.
6. A Bun-oldali kockázatok (a `Bun.sql` még nyitott tracking issue-ja és friss konkurenciahibái, illetve a macOS `bun:sqlite`/bővítmény-probléma) továbbra is fennállnak a kutatás időpontjában (Bun 1.4 vonal) — utóbbira van hivatalosan dokumentált, működő kerülőút, előbbire (a Bun.sql érettsége) nincs hivatalos „production-ready" minősítés, csak marketing-szintű promóció és aktív hibajavítási történet.

---

## Meglátogatott linkek

| Cím | URL | Tier | Eszköz |
|---|---|---|---|
| npm registry — @paradedb/drizzle-paradedb | https://registry.npmjs.org/@paradedb/drizzle-paradedb | T1 | curl (JSON API) |
| npm registry — @paradedb/drizzle-paradedb@0.5.0 | https://registry.npmjs.org/@paradedb/drizzle-paradedb/0.5.0 | T1 | curl (JSON API) |
| drizzle-paradedb CHANGELOG.md | https://raw.githubusercontent.com/paradedb/drizzle-paradedb/main/CHANGELOG.md | T1 | curl (nyers fájl) |
| drizzle-paradedb package.json (main) | https://raw.githubusercontent.com/paradedb/drizzle-paradedb/main/package.json | T1 | curl (nyers fájl) |
| GitHub — paradedb/drizzle-paradedb tags/releases | https://api.github.com/repos/paradedb/drizzle-paradedb/tags | — | curl (hozzáférés megtagadva ebben a sessionben, nem használt forrás) |
| npm registry — drizzle-orm | https://registry.npmjs.org/drizzle-orm | T1 | curl (JSON API) |
| npm registry — drizzle-kit | https://registry.npmjs.org/drizzle-kit | T1 | curl (JSON API) |
| npm registry — better-auth | https://registry.npmjs.org/better-auth | T1 | curl (JSON API) |
| npm registry — better-auth@1.7.5 | https://registry.npmjs.org/better-auth/1.7.5 | T1 | curl (JSON API) |
| npm registry — better-auth@1.6.33 | https://registry.npmjs.org/better-auth/1.6.33 | T1 | curl (JSON API) |
| Drizzle ORM — v1 Roadmap | https://orm.drizzle.team/roadmap | T1 | Exa fetch |
| GitHub issue — drizzle-orm #5660 „when will we have v1.0.0?" | https://github.com/drizzle-team/drizzle-orm/issues/5660 | T1 | Exa fetch |
| GitHub issue — drizzle-orm #1869 (AndriiSherman timeline-üzenete) | https://github.com/drizzle-team/drizzle-orm/issues/1869 | T1 | Exa search |
| GitHub issue — drizzle-orm #4760 (ugyanaz az üzenet, más issue) | https://github.com/drizzle-team/drizzle-orm/issues/4760 | T1 | Exa search |
| drizzle-orm indexes.ts (main) | https://github.com/drizzle-team/drizzle-orm/blob/main/drizzle-orm/src/pg-core/indexes.ts | T1 | Exa search |
| drizzle-orm indexes.ts (korábbi, stabil-korabeli commit) | https://github.com/drizzle-team/drizzle-orm/blob/273c7807/drizzle-orm/src/pg-core/indexes.ts | T1 | Exa search |
| Drizzle ORM — Indexes (mintlify tükördoksi) | https://drizzle-team-drizzle-orm.mintlify.app/schema/indexes | T2 | Exa search |
| Drizzle ORM — PostgreSQL extensions | https://orm.drizzle.team/docs/extensions/pg | T1 | Exa fetch |
| Drizzle ORM — Vector similarity search guide | https://orm.drizzle.team/docs/guides/vector-similarity-search | T1 | Exa fetch |
| GitHub issue — drizzle-orm #2935 „generate ignores index operators" | https://github.com/drizzle-team/drizzle-orm/issues/2935 | T1 | Exa fetch |
| Better Auth — Drizzle adapter changelog | https://github.com/better-auth/better-auth/blob/main/packages/better-auth/CHANGELOG.md | T1 | Exa search |
| Better Auth — drizzle-adapter changelog (1.7.0) | https://github.com/better-auth/better-auth/blob/c3688ba/packages/drizzle-adapter/CHANGELOG.md | T1 | Exa search |
| Better Auth — PR #10501 (peer-range igazítás) | https://github.com/better-auth/better-auth/pull/10501 | T1 | Exa search |
| Better Auth — v1.7.0 release | https://github.com/better-auth/better-auth/releases/tag/v1.7.0 | T1 | Exa search |
| Better Auth blog — „Better Auth 1.7" | https://better-auth.com/blog/1-7 | T1 | Exa search |
| Dosu/Devin — „Drizzle ORM v1 Compatibility" összefoglaló | https://app.dosu.dev/cdda13d9-dd27-4d31-b09a-5d8bec92de21/documents/d44cb4d1-c83b-43d5-998a-c0a6dec2b641 | T3 | Exa search (csak tájékozódásra, elsődleges forrásokkal ellenőrizve) |
| Bun — főoldal (benchmark, „Bun in production") | https://bun.com/ | T1 | Exa search |
| Bun — SQL dokumentáció (docs/runtime/sql.mdx) | https://github.com/oven-sh/bun/blob/88a63988/docs/runtime/sql.mdx | T1 | Exa search |
| GitHub issue — oven-sh/bun #15088 „Bun.sql tracking issue" | https://github.com/oven-sh/bun/issues/15088 | T1 | Exa search |
| GitHub issue — oven-sh/bun #32004 (pool stall) | https://github.com/oven-sh/bun/issues/32004 | T1 | Exa search |
| GitHub PR — oven-sh/bun #32772 (redundant Sync javítás) | https://github.com/oven-sh/bun/pull/32772 | T1 | Exa search |
| GitHub issue — oven-sh/bun #33665 (prepared statement cache hiba) | https://github.com/oven-sh/bun/issues/33665 | T1 | Exa search |
| GitHub issue — oven-sh/bun #15438 (postgres-js hang, lezárt) | https://github.com/oven-sh/bun/issues/15438 | T1 | (idézve `sq06.md`-ből, nem újra-olvasva) |
| Bun — SQLite dokumentáció | https://bun.com/docs/runtime/sqlite.md | T1 | Exa search |
| Bun — Database.loadExtension referencia | https://bun.com/reference/bun/sqlite/Database/loadExtension | T1 | Exa search |
| GitHub issue — oven-sh/bun #38647 (macOS statikus SQLite kérés) | https://github.com/oven-sh/bun/issues/38647 | T1 | Exa fetch |
| GitHub issue — oven-sh/bun #38772 (ua., duplikátum) | https://github.com/oven-sh/bun/issues/38772 | T1 | Exa fetch |
| GitHub issue — oven-sh/bun #16717 (SQLite version is incorrect, nyitva) | https://github.com/oven-sh/bun/issues/16717 | T1 | Exa fetch |
| GitHub issue — oven-sh/bun #31247 (macOS SQLite 3.43.2 vs 3.53.0) | https://github.com/oven-sh/bun/issues/31247 | T1 | Exa fetch |
| GitHub PR — oven-sh/bun #31249 („ai slop", lezárt, nem mergelt) | https://github.com/oven-sh/bun/pull/31249 | T1 | Exa fetch |
| GitHub PR — oven-sh/bun #31293 (static SQLite alapérték, mergelve) | https://github.com/oven-sh/bun/pull/31293 | T1 | Exa fetch |
| GitHub issue — asg017/sqlite-vec #78 (macOS kerülőút) | https://github.com/asg017/sqlite-vec/issues/78 | T1 | Exa search |
| sqlite-vec — site/using/js.md (hivatalos használati doksi) | https://github.com/asg017/sqlite-vec/blob/main/site/using/js.md | T1 | Exa search |
