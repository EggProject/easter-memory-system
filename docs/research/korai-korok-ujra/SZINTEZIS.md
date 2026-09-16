# Szintézis — a korai körök újramérése

**Kampány:** `korai-korok-ujra` · 2026-09-15 · 3 kereső, párhuzamosan · **160 forrásolt állítás**

Ez a kör nem új témát kutatott, hanem **visszakereshetőséget adott** a D-01…D-10, D-15 és D-16
döntéseknek. A korai körökhöz nem készült URL-lista és állítás-tábla; most már van.

---

## Amit a mai mérés megváltoztatott

### 1. Egy megdöntött állítás feltámadt — és ez a kampány fő tanulsága

A Claude Code hook-limitje (**10 000 karakter**) 2026-09-01-én **megdöntött** állítás volt: az
ellenőrzés négy hivatalos oldalt átnézett, és sehol nem találta. Ma a hivatalos dokumentáció
**két helyen is kimondja**, szó szerint.

**Nem a szám változott, hanem a világ.** És ebből egy szabály következik, ami eddig nem volt
kimondva: **egy „nincs dokumentálva" megállapítás lejár.** A cáfolatokat ugyanúgy újra kell
mérni, mint a megerősítéseket — különben a specifikáció egy elavult tagadásra hivatkozik, ami
pontosan olyan hiba, mint egy elavult állításra hivatkozni.

Kiegészítés, ami a régi megfigyelést igazolja: a dokumentáció szerint a limit fölötti tartalom
fájlba kerül, és a modell **előnézetet** kap. A korábbi kör pont ezt figyelte meg. A gyakorlati
előnézet-méret (kb. 2 000 karakter) **nincs** dokumentálva — arra a specifikáció nem hivatkozhat.

### 2. A kategóriaszám kérdése most két oldalról van megmérve

| Modellfajta | Mit mértek | Eredmény |
|---|---|---|
| Nagy, generáló | 3 / 18 / 60 kategória | **nincs látványos romlás** |
| Kis, kódoló (lektorált) | 3 vs. 13 kategória | **83–84% → 62,8%** |

A kettő **nem mond ellent egymásnak** — együtt azt mondják, hogy **a hatás a modell erejétől
függ**. Ez megerősíti a D-04/4 mostani, javított szövegét.

**A korlátot ki kell mondani:** a lektorált mérés BERT- és RoBERTa-osztályú **kódoló** modelleken
készült. Nem az a fajta, amelyik nálunk kategóriát választana. Az irányt igazolja, a mértéket nem
lehet átvinni.

### 3. Az útvonal sehol nem biztonsági határ — tíz forrásból

Se az agent-memória rendszerekben, se az infrastruktúrában: a tényleges izolációt mindig egy
**külön, aktívan kikényszerített szabályzat-réteg** adja, nem a fában elfoglalt hely.

**Ez nálunk pontosan így van** — a D-11 szerint az ellenőrzés a kérés-rétegben történik, az
útvonal csak azt mondja meg, **mit** kell ellenőrizni. A megkülönböztetés eddig hallgatólagos
volt; most forrásolt.

### 4. A YAML-csapda él, de nem a specifikáció hibája

A YAML 1.2 a Core Schema szintjén **megoldotta** a `no` → hamis problémát. **A két legelterjedtebb
parser forráskódja viszont ma is az 1.1-es, tág szabályt használja.**

Egy sokat idézett blog szerint a hiba „a specifikáció szerint szándékos" — **ez téves**, és a nyers
specifikáció cáfolja. Ha valaha erre hivatkoznánk, az hiba volna.

**Nálunk ez nem változtat semmin**, mert a D-05/2 minden szöveges értéket idézőjelbe tesz — de az
*indoklás* pontosabb lett: nem a spec rossz, hanem az, amit a parserek ténylegesen csinálnak.

### 5. A markdown-fájl mint tárolóegység nem precedens nélküli

Van egy éles rendszer (**basic-memory**), amelyik fájl-elsődleges: *„the database serves as a
secondary index"* — és egy fájlon belül tény-szintű egységeket is elkülönít. **Pontosan a mi
D-03-unk szerkezete.** A többi tény-szintű rendszer mind gráf- vagy vektor-adatbázist használ.

Ez a D-03 legjobb alátámasztása, és eddig hiányzott.

---

## Amit megerősített, de pontosabban

- **Magyar a nagy benchmarkban:** 28 taszk, és a magyar visszakeresési alkészleten 191 modellnek
  van pontszáma. Ezúttal **nyers adatbázis-lekérdezéssel** igazolva, nem másodkézből.
- **A tövezés kérdése:** az angol tövező magyarra **nulla hasznot** hoz, a magyar tövező
  **elrontja az alapalakot**. A Spec 30 korábbi „bizonyítottan ront" megfogalmazása ennél
  erősebb volt — javítva.
- **SQLite mint vektortár:** a vonatkozó bővítmény hivatalosan **csak brute-force**, és nincs
  kimondott méret-ajánlása. Egyes rendszereken a rendszer-SQLite nem tud bővítményt tölteni —
  ez fejlesztői gépen éles korlát.
- **Az FTS5-ben nincs beépített Snowball**, a meglévő tövező kifejezetten csak angolra készült.

---

## Ami ebből következik

A kampány **egyetlen döntést sem borított fel.** Három megfogalmazást pontosított (D-15,
Spec 30 tövezés, D-04/4 korlátai), és a többihez megadta azt, ami eddig hiányzott: a forrást.

**A legfontosabb, amit magunkkal viszünk, nem tartalmi:** a cáfolat is lejár. Ez a mérési
dokumentumba is bekerült, a hook-limit szakaszához.
