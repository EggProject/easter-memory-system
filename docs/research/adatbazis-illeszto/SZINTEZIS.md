# Szintézis — adatbázis-illesztő

Kampány: `adatbazis-illeszto` · Lezárva: 2026-09-09 · A szintézist a vezető (Opus) írta,
a kereséseket négy Sonnet ügynök végezte.

> Ez a fájl a **következtetéseket** mondja ki. A forrásokat és az idézeteket a `kivonat.md`
> tartalmazza.

---

## 1. Miért futott ez a kampány

A tulajdonos kimondta, hogy az adatbázist illesztési minta mögé kell tenni, mert később más
adatbázis-típusokat is be akar vezetni. A **D-34 első változata kutatás nélkül íródott** —
ez a munkamódszer megsértése volt.

És tartalmazott egy tárgyi tévedést is: az „egy írós" korlátot **alkalmazás-szintű
feltevésként** írtam le, olyasmiként, ami átszivárog bármilyen illesztőn. A tulajdonos ezt
visszadobta azzal, hogy ha ez adatbázis-szolgáltatói kérdés, akkor ott kell kezelni.

**Igaza volt a besorolásban, de a kutatás mindkettőnket árnyal.** Ez a kampány elsősorban
erre a kérdésre válaszol.

---

## 2. Az „egy író" kérdés — a valódi válasz

### 2.1 Amiben a tulajdonosnak igaza van

A mechanizmus **az illesztő dolga**. Az alkalmazás kódjában nem lehet SQLite-elágazás. Erre
van élő példa: a Prisma SQLite-on **csendben `BEGIN IMMEDIATE`-tel** nyit tranzakciót — ez
illesztő-szintű megoldás, az alkalmazás nem tud róla.

Az én eredeti megfogalmazásom — hogy ez „átszivárog bármilyen illesztőn" — **hibás volt**.

### 2.2 Amiben viszont nem elég a „kezeljük a szolgáltatóval"

A kutatás legerősebb bizonyítéka a **Django #29280** hibajegy: egy húsz éve fejlesztett,
iparági szabvány hordozható ORM **nem tudta** transzparensen elrejteni ezt. A csapat
kifejezetten **elvetette** azt a javítást, hogy mindenhol `IMMEDIATE` tranzakciót nyissanak,
mert az a Postgres- és MySQL-felhasználókat is lassította volna:

> „the performance hit… seems too high to implement this in Django"

Ami végül kikerült, az egy **SQLite-specifikus, opcionális beállítás** — nem rejtett
viselkedésváltozás. Ugyanez a Django dokumentációjában a pesszimista zárolásról:

> `select_for_update()` — „Calling it will have no effect."

És a „database is locked" hiba első ajánlott orvossága a Django saját dokumentációjában az,
hogy **váltsunk másik adatbázisra**.

Mind a **kilenc** megvizsgált több-motoros adatréteg (SQLAlchemy, Prisma, Knex, Kysely,
Doctrine, Hibernate/JPA, ActiveRecord, Ecto, Drizzle) **dokumentálja** a motorok közti
eltéréseket ahelyett, hogy elfedné őket — támogatási táblázattal, alsó korláttal
(„guaranteed to be at least READ_COMMITTED"), vagy explicit „nem támogatott" jelöléssel.

Elméleti alátámasztás: Berenson és társai szerint már **maguk az ANSI izolációs szintek nevei
is kétértelműek**, tehát egy réteg, ami csak továbbadja a szint nevét a motornak, nem tudja
garantálni, hogy ugyanaz történik.

### 2.3 A megoldás, ami ebből következik

**A port ne tranzakciót kérjen, hanem garanciát mondjon ki** — és olyan garanciát, amit
minden motor teljesíteni tud.

A kutatás megnevezi az egyetlen **valóban motor-független** párhuzamosság-kezelési
mechanizmust: a **verzióoszlopos optimista zárolást** (Rails `lock_version` /
`StaleObjectError`, a Prisma dokumentált OCC-mintája). Azért hordozható, mert **soha nem
támaszkodott motor-specifikus zárolási primitívre**. A pesszimista `SELECT ... FOR UPDATE`
pontosan ezért nem hordozható — SQLite-ban egyszerűen nincs.

Tehát:

- **Az alkalmazás** optimista zárolást használ, verzióoszloppal. Ez SQLite-on és bármilyen
  kiszolgáló-alapú adatbázison ugyanaz.
- **Az SQLite-illesztő** a saját dolgát maga oldja meg: `BEGIN IMMEDIATE`, `busy_timeout`,
  sorbaállítás. Ebből az alkalmazás semmit nem lát.
- **Egy Postgres-illesztő** ugyanazt a garanciát MVCC-vel vagy sorzárral teljesíti.

**Így az „egy író" tényleg illesztő-részlet lesz.** Nem azért, mert eltűnik, hanem mert nem
az alkalmazás fizeti meg.

### 2.4 És amit ettől függetlenül tisztázni kell

A D-34 első változata **két különböző dolgot kevert össze**. Az SQLite egy-írós modellje
adatbázis-kérdés. A **D-07 fájlonkénti írási sora** viszont a markdown fájlok lemezre írásáról
szól — ideiglenes fájl, `fsync`, átnevezés, könyvtár-`fsync`. **Annak semmi köze a
DB-illesztőhöz**, és nem is kerül mögé.

---

## 3. Hol van a varrat

Cockburn saját szövege adja a döntő szempontot: a portokat **cél szerint kell particionálni,
nem technológia szerint**, az ajánlott sáv **2–4 port**, és „nincs különösebb kár abban, ha
rossz számú portot választunk".

Ez megerősíti a **két port** felosztást — keresési index és adattár —, de nem azért, mert két
adatbázisfájl van (az technológia), hanem mert **két különböző célt szolgálnak**: az egyik
eldobható és újraépíthető, a másik nem. Erre a konkrét párra egyébként **nincs közvetlen
forrás**; ez extrapoláció Cockburn elvéből.

Egy pontosítás, ami az első változatban tévesen szerepelt: a Repository mintát a PoEAA
katalógusban **nem Fowler jegyzi**, hanem Hieatt és Mee. A Data Mapper és a Gateway az övé.

### A vita, amit nem hallgathatunk el

A „Repository ORM fölé" mintának **élő, dokumentált ellenzéke van** (Comartin, Conery,
Abraham, Bogard), és egy kiegyensúlyozott középső álláspont (Jon P Smith). Az ellenérv lényege,
hogy egy ORM már maga is absztrakció, és a fölé húzott Repository elrejti azt, amit tudni
kellene — lusta betöltés, N+1 lekérdezés.

A kutató ügynök megállapítása szerint a nézetkülönbség jó eséllyel **architektúra-stílustól
függ** (CQRS/vertical slice kontra rétegzett DDD), nem egyszerű tévedés egyik oldalon.

**Nálunk ez azért nem dönt el semmit**, mert a mi indokunk nem a tesztelhetőség és nem a
tisztaság: **négy konkrét, motor-specifikus fogás** derült ki egyetlen körben, és azok
elszigetelése a cél. De a vita létezését be kell írni, mert egy későbbi olvasó azt hihetné,
hogy ez eldöntött legjobb gyakorlat.

---

## 4. A keresés — itt szerencsénk van, és ez most már forrásolt

Az első változatban azt írtam, hogy az RRF „nem szándékolt haszna" a hordozhatóság. **Ez a
kutatás szerint nem véletlen, hanem az RRF tervezési célja.**

Az eredeti RRF-cikk (Cormack, Clarke, Buettcher, SIGIR 2009) szerint a módszer

> „combines ranks without regard to the arbitrary scores returned by particular ranking methods"

Az Elasticsearch RRF-dokumentációja ugyanezt mondja, kifejezetten BM25 + vektoros találatok
egyesítésére, „without score normalization", és hogy „the different relevance indicators do
not have to be related to each other".

A pontszámok összemérhetetlensége pedig **hivatalosan elismert**:

- Az Elasticsearch saját „Getting consistent scoring" oldala szerint **ugyanaz a lekérdezés
  kétszer futtatva is más sorrendet adhat**, mert a replikák eltérő index-statisztikát
  hordozhatnak.
- A PostgreSQL dokumentációja szerint a `ts_rank` „does not use any global information, so it
  is impossible to produce a fair normalization to 1% or 100%", és a beépített rangsorolók
  „only examples".

Sőt: a **Meilisearch és a Typesense egyáltalán nem BM25-öt használ** — szekvenciális
holtverseny-feloldó szabályrendszert. Egy olyan port tehát, ami BM25-szemantikát feltételez,
már ma is rossz lenne. **A helyezés-alapú egyesítés ezt is túléli.**

### A vektoros oldal, és egy megerősítés

Minden megvizsgált vektormotor (pgvector, Qdrant, Milvus, Faiss) **maga jelenti be a
dokumentált felületén, hogy pontos vagy közelítő keresést ad** — ez nem rejtett megvalósítási
részlet náluk sem.

Ez megerősíti a D-34 hatodik pontját: a mi portunknak is meg kell mondania magáról. És
emlékeztet arra, hogy **egy közelítő illesztő újranyitja a D-32/2-t**.

Szabvány nincs: az SQL:2023-ban nincs vektor-típus, és közös vektorkeresési kliens-felület sem
létezik. <span>(Ez utóbbi gyengén forrásolt — hiány, nem megállapítás.)</span>

---

## 5. Hogyan tartható őszinte az illesztő

A legkonkrétabb, dokumentált minta az **SQLAlchemy**-é: közös `testing.suite`, plusz
**képesség-alapú** követelmény-zászlók — **nem motornév szerint**, hanem képesség szerint —,
plusz explicit felülírás ott, ahol kell.

Ez pontosan az a forma, ami nekünk kell, és **magától megoldja a pontos/közelítő kérdést is**:
az nem külön kivétel lesz, hanem egy képesség-zászló a többi között.

A Rails harmadik variánst mutat: közös tesztosztály és motoronkénti alosztályok, futásidejű
öngátlással.

### A kockázat, amit ki kell írni

A Testcontainers saját dokumentációja mondja ki, hogy a memóriabeli helyettesítők „may not
have all the features… and behave slightly differently".

És van egy dokumentált eset: egy **1241/1241 zöld SQLite-tesztkészlet elrejtett három valós
hibát** — hiányzó idegenkulcs-kényszer, azonosító-újrafelhasználás, nulla migrációs
lefedettség —, amik csak valódi PostgreSQL ellen derültek ki. A szerző hozzáteszi, hogy a
javítás után is maradtak motorkülönbségek.

**Egy zöld szerződés-tesztkészlet tehát nem bizonyítja, hogy egy másik motor működni fog.**

És amit a szerződés-teszt eleve nem néz: a Pact dokumentációja szerint a **mellékhatások**
kívül esnek rajta. A teljesítmény és a párhuzamossági viselkedés szintén — ez utóbbira nem
találtunk explicit elsődleges forrást, csak közvetettet.

---

## 6. Az őszinte rész: megéri-e egyáltalán

**Nincs empirikus adat arra, hogy megéri-e portot építeni egyetlen megvalósításhoz.** Csak
vélemények vannak, mindkét oldalon.

Fowler YAGNI-esszéje normatív érvet ad ellene, és egy nem ide tartozó empirikus adatot idéz
(Kohavi és társai: a funkcióknak csak nagyjából harmada térül meg) — ez **analógia, nem
bizonyíték**. A védelem (Rainsberger) pedig nem is a hordozhatóságról szól, hanem a **mai
tesztelhetőségről** — ez fontos és elhanyagolt megkülönböztetés.

**Ezt ki kell mondani a döntésben.** Nem azért, hogy vitassam — a tulajdonos kimondta, és van
konkrét második felhasználás a fejében —, hanem mert a döntési napló akkor ér valamit, ha
megmondja, mire alapul. Ez a döntés **szándékon és négy konkrét, megtapasztalt csapdán**
alapul, nem méréseken.

---

## 7. Amit a D-34-ben javítani kell

| # | Mi volt | Mi lesz |
|---|---|---|
| 5. pont | Az „egy írós" korlát átszivárog bármilyen illesztőn | **Hibás.** Az illesztő dolga; az alkalmazás optimista zárolást használ. A D-07 fájlírási sora külön alrendszer. |
| 5. pont | „a tranzakciós viselkedés motoronként más" — homályos | Konkrét: az izolációs szint **neve** sem hordozható; a port a szükséges garanciát mondja ki, nem a szintet |
| 7. pont | Az RRF hordozhatósága „nem szándékolt haszon" | **Az RRF tervezési célja** — forrással |
| — | hiányzott | A Repository-vita létezése, és hogy ez nem eldöntött legjobb gyakorlat |
| — | hiányzott | Cockburn elve: a port **cél szerint** particionál, nem technológia szerint |
| 4. pont | „szerződés-tesztkészlet" általánosságban | **Képesség-alapú** zászlók, az SQLAlchemy mintája szerint |
| 4. pont | hiányzott | Egy zöld tesztkészlet nem bizonyíték — dokumentált esettel |
| — | hiányzott | Nincs empirikus bizonyíték a port megtérülésére |

**Számot ez a kampány nem ad a mérési dokumentumba** — mintákról és dokumentált gyakorlatról
szól, nem mérésekről.
