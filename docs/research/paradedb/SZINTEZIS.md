# Szintézis — ParadeDB mint egyetlen adatbázis?

Kampány: `paradedb/` · 2026-09-22 · 7 kutatási egység (SQ01–SQ07, a régi keresővel) + 5 ellenőrző egység
(ELL01–ELL05, már az **Exa** keresővel; a döntés után még ELL06–ELL07, lásd a 8. szakaszt). Keresés: párhuzamos Sonnet alügynökök. Szintézis: Opus.

A felhasználó kérdése szó szerint: „úgy hallottam hogy a paradb pont nekünk megfelelő lenne, vector keresés stb …
nézzetek utána rendesen és ha megfelel akkor inkább csak ez legyen a db és nem kell akkor külön interface-ek amivel
gyorsítunk majd a fejlesztésen".

---

## 1. Mi ez egyáltalán

A „paradb" a **ParadeDB**. (Két másik „ParaDB" is létezik — egy paranormális adatbázis és egy gombagenomikai — egyiknek
sincs köze az adatbázis-motorokhoz.) A ParadeDB **nem önálló adatbázis**, hanem saját szavaival *„vanilla Postgres
with an extension installed, not a Postgres fork or sidecar process"*. A lényeg a `pg_search` bővítmény (Rust, Tantivy
motor): BM25 szöveges keresés, szűrés, hibrid keresés, és 2026 nyara óta saját vektorindex is.

## 2. Ahol nagyon jól illik

| Amit tud | Miért számít nekünk | Biztonság |
|---|---|---|
| **Egy motor**: BM25 szöveg + vektor + rendszeradatok | Nem kell külön vektortár; a D-32 „mindkét láb előszűr" terve egyetlen lekérdezésben megoldható | igazolt |
| **Szűrés az indexen belül** („Filter Pushdown") — `project_id IN (…)` | Pontosan a jogosultsági előszűrés; ha az oszlop indexelt, nem utólag szűr | igazolt, két hivatalos oldal |
| **Hibrid keresés RRF-fel, k=60** hivatalos mintával, mindkét ágban ugyanazzal a szűrővel | Ez a mi mért, kapuzott stratégiánk alapja (RRF, k=60) | igazolt |
| **Magyar tövező** (`stemmer=hungarian`) + kapcsolható ékezet-lehagyás, **oszloponként** más tokenizáló | Az SQLite FTS5-nek nincs magyar tövezője; az azonosító-mező mehet `literal`/`source_code` tokenizálóval | igazolt, a ParadeDB saját forkjából |
| **Azonosítók** (`PROJ-4412`, `RATE_LIMIT_URL`) | Van rájuk tokenizáló; a sima Postgres `tsvector` ezeket **szétszedi** | igazolt |
| **Több egyidejű író** | Az SQLite-terv külön írási sorbaállítást igényelt | Postgres-alaptulajdonság |
| **Megoldja az SQLite-terv egyik nyitott gondját** | macOS-en a `bun:sqlite` nem tud bővítményt (pl. `sqlite-vec`) betölteni — a jelentés-index szerkezete emiatt is nyitott maradt | igazolt (kerülőút van: `setCustomSQLite`) |
| Hivatalos **Drizzle**-csomag; a Better Auth 1.7 stabil már Postgres + stabil Drizzle mellett megy | A stack megmarad | igazolt, de lásd lent |

## 3. Ahol ma nem illik

**3.1 Fiatal, és ez a döntés szempontjából nem kozmetika.**
- 0.x verzió, kb. heti másfél kiadás. Nincs 1.0 vagy API-stabilitási ígéret.
- **Az ingyenes (Community) változat csak a v0.24.0 óta írja az indexet összeomlás-biztosan — ez 2026. június 3.**
  (Az első kör 2025-öt írt; az ellenőrzés három forrással javította.) Vagyis három és fél hónapja.
- **A saját vektorindex a v0.25.0-val jött, 2026. július 28-án** — nyolc hete.
- **A mostani stabil verzióban (v0.25.9) van ismert hibás-találat hiba (#6108)**, a javítás csak a `0.26.0-rc.1`-ben.
  Egy memóriarendszernél a hibás találat a legrosszabb hibaosztály: csendes.
- Nyitott hiba: SERIALIZABLE izoláció mellett phantom write skew (#6390). READ COMMITTED mellett nem érint.
- Egyes verzióváltásoknál **kötelező az újraindexelés** (kiadási jegyzékek: 0.15.0, 0.22.0, 0.25.1); Postgres
  főverzió-váltásra nincs ParadeDB-útmutató.
- A menedzselt szolgáltatók nem támogatják: a **Neon épp 2026. szeptember 21-én vezette ki**; AWS RDS listáján nincs.

**3.2 Licenc: AGPL-3.0.** Egy kft. enterprise termékénél ez **jogi kérdés, nem műszaki**. A 13. szakasz a
*módosított* program hálózati elérésére vonatkozik; hogy egy vele csak SQL-en beszélő, változatlanul használt
motorra épülő alkalmazásra mi vonatkozik, arról sem az FSF, sem a ParadeDB nem nyilatkozik konkrétan. Van fizetős
Enterprise-licenc, ami a copyleftet feloldja. A cég minden közreműködőtől CLA-t kér (a licencet ő szabja meg).
**Jogi következtetést nem vonunk le — jogásznak kell megnéznie.**

**3.3 Ütközik a saját korábbi szabályainkkal** — ezt a felhasználónak kell tudatosan felülírnia:
- **D-01/1:** „Vector DB tilos. Postgres tilos." — szó szerint.
- **D-34 (illesztő/port minta)** — a felhasználó kérése volt: „ne legyen minden beégetve".
- **Projektcél: „legkevesebb külső függőség"** — a ParadeDB egy külön szerverfolyamat + bővítmény + `pgvector`.
  Beágyazott, egyfájlos mód nincs. A D-16 két konténere (app + beágyazó) háromra nő.

## 4. Mit borít fel, ha váltunk

| Döntés | Most | ParadeDB-vel |
|---|---|---|
| D-01/1 | Postgres és vektor-DB tilos | felülírva |
| D-12, Spec 20 | három SQLite-fájl | egy Postgres-adatbázis; az audit napló marad fájl (az nem adatbázis-kérdés) |
| D-34 | illesztő mögött, motorfüggetlen | a felhasználó kérése szerint kivezetve |
| D-36 mentés | `VACUUM INTO` (a törölt tartalom nem kerül át) | `pg_dump` — logikai mentés, csak élő sorok, tehát ugyanez a tulajdonság megmarad; az index visszaállításkor újraépül |
| D-37 frissítés | az index soha nem migrál, újraépül | **ez a ParadeDB-vel még fontosabb lesz** (kötelező REINDEX egyes verzióknál) |
| D-42 | `quick_check` mentés előtt | `pdb.verify_index` + Postgres saját ellenőrzései |
| Spec 30, `bench/` | FTS5 mérések | újra kell mérni ParadeDB-n — a kapuzott stratégia elve átvihető, a számok nem |
| Spec 50, 90/17 | SQLite üzemeltetési mérések | nagy része érvényét veszti |

**Ami nem változik:** a markdown fájl az egyetlen igazság (D-03); az index eldobható; csak beágyazó modell fut.

## 5. Az összevetési alap: sima Postgres + pgvector, ParadeDB nélkül (az én ötletem, nem kérés volt)

Engedékeny licenc (PostgreSQL License), érett mag. **De:** BM25 csak a Timescale `pg_textsearch` bővítménnyel
(PostgreSQL License, 1.0 GA 2026. április, v1.4.0 2026. augusztus, csak PG 17–18, egy évnél fiatalabb); a `tsvector`
az azonosítókat szétszedi (`PROJ-4412` → `PROJ` + `4412`); a Postgres Snowball magyar tövezője egy független
vizsgálat (Endrédy 2015) szerint a leggyengébb a magyar tövezők közül. A hibrid RRF dokumentált, de alkalmazás-oldalon kell megírni.

## 6. A mérlegem

**Funkcionálisan a ParadeDB jobban illik a keresési tervünkhöz, mint a mostani SQLite-terv** — egyetlen motorban
adja azt, amit most három darabból raknánk össze, és megoldja a macOS-es vektortár-gondot is.

**Ma viszont két dolog nem illik:** az érettség (a jelenlegi stabil verzióban ismert hibás-találat hiba, három és fél
hónapos összeomlás-biztonság, nyolchetes vektorindex) és a licenc (AGPL egy cég enterprise termékében).
Az első idővel javul — mi még tervezési fázisban vagyunk. A második nem javul magától.

## 7. Amire nincs forrás

- Független mérés ParadeDB kontra SQLite FTS5.
- A ParadeDB saját vektorindexének dimenziókorlátja (a talált 2000 egy elavult, 0.25 előtti típusé).
- Független recall-mérés a saját vektorindexre szűréssel — csak a ParadeDB saját CI-adata van (recall@10 ~0,87–0,98).
- Közösségi, éles üzemi beszámoló — két egyező, független beszámolót nem sikerült találni.
- Hivatalos minimum RAM-igény.

---

## 8. Kiegészítés 2026-09-22 — a döntés után

**A döntés.** A tulajdonos a ParadeDB ingyenes (Community) változatát választotta egyetlen adatbázisnak, illesztő-réteg
nélkül. A választott válasz két szabályt hozott magával: a ParadeDB kódját nem módosítjuk, és megvalósításkor rögzített
verziót használunk, amiben már benne van a #6108 javítása (0.26 stabil vagy újabb). A döntés a döntési napló **D-43**-a.

**A jogászról.** A 3.2 pont („jogásznak kell megnéznie”) túlhangsúlyos volt. A tulajdonos kérdése: „milyen jogász? nem
ingyenes a paradb?” — az. Az AGPL feltétele a *módosított* program hálózati elérésére vonatkozik; a nyitott kérdés csak
az, hogy egy vele SQL-en beszélő, változatlanul használt motorra épülő termék értékesítésekor mi a helyzet. Ez üzleti
döntés, nem tervezési feltétel.

**Második ellenőrző kör (ELL06–ELL07, Exa).** A leírások átírása előtt:

- ELL06 — mentés és migráció: a `pg_dump` konzisztens és nem blokkol (igazolt); hogy csak az élő sorokat viszi, azt a
  doksi szó szerint nem mondja ki (a saját próba mutatta meg); a Postgres DDL tranzakciós, a `CREATE INDEX CONCURRENTLY`
  kivétel (igazolt); a Drizzle Postgres-migrátora egy tranzakcióban fut (forráskódból igazolt); hogy a ParadeDB-index
  visszaállításkor helyesen újraépül-e, arra nincs hivatalos ParadeDB-mondat; táblánként egy ParadeDB-index (igazolt);
  a ParadeDB-index csak a saját operátoraival aktiválódik, tehát a pontos `pgvector`-keresést nem zavarja (igazolt).
- ELL07 — adatlap-ellenőrzőösszeg: a Postgres 18 alapból bekapcsolja (igazolt); utólag csak leállított fürtön
  kapcsolható be; a `pg_amcheck` csak táblát és B-fa indexet néz, minden mást csendben átugrik (igazolt); a ParadeDB-re
  a `pdb.verify_index` való.

**Saját próbák sima Postgresen** (`bench/postgres/`, mérések 18. szakasz): a törölt sor nincs a `pg_dump`-ban, de az
adatfájlban és a WAL-ban megmarad; a félúton elhasaló migráció nyomtalanul visszagörgetődik; a pontos vektorkeresés
jogosultsági előszűréssel a teljes átnézéssel azonos top-10-et ad; ellenőrzőösszeg nélkül a táblatartalom csendes
sérülését semmi nem veszi észre, vele a `pg_dump` is elhasal; a `pg_dump`, a `pg_restore` és a `pg_amcheck` ideje három
méreten lemérve.

**Egy pontosítás a 2. szakaszhoz.** A magyar tövezőt ott előnyként írtam, de a Spec 30 szerint a szó-index tövező nélkül
épül (egy korábbi saját próba szerint a Snowball magyar tövező elrontja az alapalakot). A ParadeDB-ből ténylegesen az
ékezet-lehagyás és az oszloponkénti tokenizáló kell.
