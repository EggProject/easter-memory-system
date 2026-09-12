# Önellenőrzés — `adatbazis-illeszto` kampány

Lezárva: 2026-09-09. Ez a fájl azt írja le, **hol tévedtünk és mit nem tudtunk megerősíteni.**

---

## Ez a kampány egy hiba javítására indult

A **D-34 első változata kutatás nélkül íródott.** A tulajdonos kimondta, hogy az adatbázist
illesztési minta mögé kell tenni, én pedig a „írd fel, aztán mehetünk tovább" mondatból arra
következtettem, hogy a kutatási kör kihagyható. **Nem az én döntésem volt** — a munkamódszer
szerint minden témában fut kutatás.

A kutatás nélkül írt döntés **tárgyi tévedést** tartalmazott: az „egy írós" korlátot
alkalmazás-szintű feltevésként írtam le, olyasmiként, ami átszivárog bármilyen illesztőn.
A tulajdonos ezt visszadobta, és igaza volt a besorolásban. A kutatás mindkettőnket árnyalt —
a részletek a `SZINTEZIS.md` 2. szakaszában.

**Két dolog keveredett össze**, ez külön hiba volt: az SQLite egy-írós modellje
(adatbázis-kérdés, illesztő mögé való) és a D-07 fájlonkénti írási sora (markdown fájlok
lemezre írása, semmi köze a DB-illesztőhöz).

---

## Folyamathiba, ami ebben a körben is megismétlődött

**Négyszer egymás után egyesével indítottam a kereső ügynököket**, holott a szabály az, hogy
egy üzenetben, párhuzamosan menjenek. Ebben a kampányban kétszer is bejelentettem, hogy most
mind egyszerre mennek — és utána megint egyet indítottam.

A `kategoria-prompt` és a `kereses-indexeles` kampány `QA.md`-je ugyanezt írja. **Ez tehát nem
egyszeri figyelmetlenség, hanem visszatérő hiba.**

---

## Módszertani probléma, ami az anyag minőségét érinti

**Több lekérés AI-átfogalmazott szöveget adott vissza a valódi oldal helyett** — kitalált
alcímekkel, a szó szerinti oldalszöveg helyett. Ez érintette az Oracle DAO-leírását, Fowler
YAGNI-esszéjét, CodeOpinion-cikkeket, a DDD Reference-t, az OpenSearch hibrid-keresés
dokumentációját és Qdrant-oldalakat.

Ahol lehetett, második lekéréssel kereszt-ellenőriztük; ahol nem, ott **csak az idézőjelbe
tett mondatokat** kezeltük megbízhatónak, és a többit a `hianyok.md` rögzíti. **Ez a kampány
legnagyobb minőségi kockázata**, és nem egyenletesen oszlik el: az SQ-02 és SQ-03 anyaga
túlnyomórészt hivatalos dokumentációból van, az SQ-01-é jóval vegyesebb.

---

## Amit nem sikerült megerősíteni

1. **Eric Evans szó szerinti szövegéhez nem fértünk hozzá.** A lekérő eszköz kétszer is
   megtagadta a DDD-könyv Repository-szakaszának idézését szerzői jogi okra hivatkozva. Ami
   van, az másodkézből származik — ezért a szintézis nem hivatkozik Evansra normatív forrásként.
2. **Az SQLite FTS5 pontszám-összemérhetetlenségét az sqlite.org nem mondja ki.** Csak a
   képlet korpusz- és lekérdezés-függéséből következtethető. A kutató ezt **saját
   következtetésként** jelölte, nem idézetként — helyesen.
3. **Nincs névvel azonosítható eset arra, hogy egy közös szerződés-tesztkészlet fedett volna
   el motorkülönbséget.** Van egy szorosan rokon, dokumentált eset (1241/1241 zöld SQLite-teszt,
   három valós hiba), de az nem szerződés-tesztkészletről szól. **Ez explicit hiány.**
4. **A Drizzle SQLite-specifikus tranzakciós felülete nem került elő** — pedig ez a rendszer
   tényleges ORM-je (D-12). Csak a Postgres-oldali beállítási felülete lett meg. **Ez a
   legfontosabb nyitott hiány**, és a részletes tervezés előtt pótolni kell.
5. **Nincs szabvány a vektorkeresésre** — ez „evidence of absence", és csak gyengén
   (Wikipédián keresztül) forrásolt. Nem állítás, hanem hiány.
6. **Nincs empirikus adat arra, hogy megéri-e portot építeni egy megvalósításhoz.** A keresés
   kizárólag véleményblogokat hozott. Ezt nem szépítjük: a D-34 szándékon és négy
   megtapasztalt csapdán alapul, nem méréseken.
7. **A varrat helyére a keresési index / adattár párosnál nincs közvetlen forrás.** A két port
   melletti érv Cockburn „cél szerint particionálj" elvéből **extrapoláció**.

---

## Ellentmondások, amiket nem oldottunk fel

- **Repository ORM fölé: kell vagy káros.** Comartin, Conery, Abraham és Bogard ellene;
  Jon P Smith kiegyensúlyozottan. A kutató megállapítása szerint a nézetkülönbség
  architektúra-stílustól függ (CQRS/vertical slice kontra rétegzett DDD), nem tévedés egyik
  oldalon. **A szintézis ezért nem dönti el**, csak rögzíti, hogy ez nem eldöntött legjobb
  gyakorlat.
- **A „Subclass to Test" minta vitatott.** Van róla antipattern-vita a c2 wikin (a tartalma
  nem volt elérhető), és Rainsbergernek külön előadása van a védelmében.
- **Ecto mást hangsúlyoz, mint az SQLAlchemy.** Az SQLAlchemy motor-agnosztikus, képesség-alapú
  tesztkészletet dokumentál; az Ecto valódi motor elleni, tranzakcióval izolált tesztelést.
  Mindkettő a saját ökoszisztémájában védhető.

---

## Amit a kutatás megerősített, és ami a döntés gerince lett

- A **Django #29280** hibajegy — húsz éves hordozható ORM, ami **nem tudta** transzparensen
  elrejteni az SQLite egy-írós korlátját, és SQLite-specifikus opcionális beállítást szállított
  helyette. Ez a kampány legerősebb egyetlen bizonyítéka.
- Az **eredeti RRF-cikk** és az Elasticsearch RRF-dokumentációja: a helyezés-alapú egyesítés
  **tervezési célja** a pontszám-függetlenség. Ez nem szerencse, ahogy az első változatban írtam.
- **Cockburn saját szövege** a portok cél szerinti particionálásáról.
- Az **SQLAlchemy képesség-alapú** követelmény-zászlói — konkrét, dokumentált forma arra, amit
  a D-34 negyedik pontja előír.
