# Szintézis — import és export

Kampány: `import-export` · Lezárva: 2026-09-06 · A szintézist a vezető (Opus) írta,
a kereséseket négy párhuzamos Sonnet ügynök végezte.

> Ez a fájl a **következtetéseket** mondja ki. A forrásokat és a szó szerinti idézeteket a
> `kivonat.md` és az `allitasok.csv` tartalmazza.

---

## 1. A formátumot nem kellett kitalálni

A kutatás legfontosabb eredménye egy hiány: **nincs elterjedt, nyílt csereformátum markdown
alapú tudástárakhoz.** Négy vizsgált eszköz, négy egymással nem kompatibilis megoldás. Ez az
egyetlen olyan megállapítás az egész kampányban, ami **magas** megbízhatóságot kapott, mert
négy független elsődleges forrás mondja ugyanazt.

Ami ehelyett kiderült, az sokkal használhatóbb: **kétféle rendszer van, és mi nem abba
tartozunk, amelyiknek formátumot kell kitalálnia.**

| | Rejtett állapotú rendszer | Sima fájlos rendszer |
|---|---|---|
| Példa | Notion, Joplin | Obsidian, mi |
| Az igazság forrása | adatbázis | a fájl maga |
| Export | kitalált formátum, veszteséggel | a mappa másolása |
| Visszaimportálható? | Notion: **nem** | igen, triviálisan |

A Notion saját dokumentációja mondja ki, hogy az exportja egyirányú. A Joplin fejlesztői egy
hivatalos hibajegyben dokumentálták a kettősséget: van veszteségmentes, azonosító-alapú
formátumuk, és van emberi olvasásra szánt markdown-exportjuk, amiről szó szerint azt írták,
hogy *„all ID's will be lost. Conflict status will also be lost. These are acceptable loses"*.
Az Obsidiannak **nincs is exportja** — nem hanyagságból, hanem mert nála a vault másolása maga
az export.

**Nálunk a tartalom sima markdown, rejtett állapot nélkül. Tehát a mappafa maga a formátum.**
Mellé csak az kell, ami a fából nem derül ki: mit, mikor, ki és milyen hatókörben vitt ki.

---

## 2. A tulajdonos döntései

Négy kérdést tettem fel, és mind a négyre volt válasz.

### 2.1 A verziók utaznak — külön kapcsolóval

Alapértelmezésben az export a **mostani állapotot** viszi. Egy külön kapcsolóval kérhető
**verziótörténettel együtt** is.

**Ennek van ára, és ki kell mondani:** egy történettel készült export olyan másolat, amit a
végleges törlés (D-21/6) **már nem ér el**. A végleges törlés értelme az volt, hogy egy jelszó
vagy kulcs nyomtalanul eltűnjön — egy régi exportcsomagban viszont ott marad. A tulajdonos ezt
a cserét ismerve választotta.

### 2.2 Az import mindig új verziót készít

Nincs „kihagyás" és nincs „megállás ütközésnél". Az importált fájl **új verzió lesz** a
meglévő fölött. Ha a tartalom azonos, az eredmény **„nincs változás"** — de az import ténye
akkor is látszik.

Ez nálunk azért működik, ami másoknál nem: **a felülírás nem pusztító, mert a régi állapot
verzióként megmarad.** A kutatásban vizsgált eszközök egyikénél sincs meg ez a védőháló, ezért
kell nekik a kihagyás/átnevezés/megállás hármas.

**A verziótörténet importjának szabálya:**
- **új fájl** + a csomagban van történet → a történet is bejön
- **létező fájl** + a csomagban van történet → a történetet **eldobjuk**, és ezt az előnézet
  kiírja

Miért: két történetet nem lehet értelmesen összefűzni. Vagy a csomagé az igazság, vagy a
meglévőé — és a meglévőt nem dobhatjuk el, mert az a rendszerben született.

### 2.3 Csak a saját formátumunkat fogadjuk el

Az import **nem általános markdown-behozó**. Csak olyan csomagot fogad el, amit ez a rendszer
készített, felismerhető manifeszttel és mezővalidációval.

**Ennek is van egy következménye, amit ki kell mondani:** a K-03 eredetileg a kezdeti
feltöltésről és a közös tudás behozataláról is szólt. Máshonnan érkező anyagot tehát **előbb a
mi formátumunkba kell alakítani.** Ez nem nagy ár, mert a formátum egy mappafa plusz egy JSON
manifeszt — egy rövid szkript elő tudja állítani. **De ebből tervezési kötelezettség
következik: a manifesztnek elég egyszerűnek kell lennie ahhoz, hogy kézzel is megírható
legyen.** Ha bonyolult, akkor a „csak a sajátunkat fogadjuk el" szabály nem óvatosság lesz,
hanem fal.

### 2.4 Személyes export: csak a saját mappa · Jogosultság: mindkettő aszerint

Felhasználó törlésekor (D-24) csak a `personal/<email>/` mappája megy. Amit projektbe írt, az a
projekté marad.

Exportot és importot is **jogosultság szerint** lehet indítani.

---

## 3. Ütközéskezelés: nincs mért bizonyíték, de van egy erős analógia

A kereső kimerítő keresés után **egyértelműen kimondta, hogy nincs mért, kvantitatív
bizonyíték** arra, melyik ütközési stratégia okoz kevesebb adatvesztést. Ez „a hiány
bizonyítéka", nem „nem találtuk meg".

Egyetlen mért, lektorált adat van a közelben, más területről: git tartalmi ütközéseknél a
**kézi feloldás 26-szoros hibaarányú kóddal** jár (Brindescu és társai, 2020, Empirical
Software Engineering). Ez nem fájlnév-ütközésre vonatkozik, tehát analógia — de abba az irányba
mutat, hogy **ne fájlonként kelljen dönteni.** A tulajdonos döntése (egy szabály az egész
importra) ezzel összhangban van.

**Idempotencia.** A bevett minta: azonosító vagy tartalom-lenyomat a manifesztben. Az
ellenpélda dokumentált: a Joplin nem ellenőrzi az azonosító-ütközést importnál, és a valós
következmény is le van írva — *„creates large-scale duplication that is painful to clean up"*.
Nálunk a „nincs változás" eredmény pontosan ezt zárja ki: ugyanannak a csomagnak a kétszeri
importja nem csinál verzió-szemetet.

---

## 4. Amit a jogi rész mond — és amit nem

A GDPR 20. cikke szűkebb, mint sokan hiszik: csak az érintett által **adott** adatra vonatkozik,
csak hozzájárulás vagy szerződés jogalapon, és „structured, commonly used and machine-readable"
formátumot kíván. A 15. cikk tágabb, de gyengébb a formátumra. A határidő a 12. cikk (3)
bekezdése szerint egy hónap, indokolt esetben plusz kettő.

A WP29/EDPB iránymutatás konkrét: a **származtatott adat nem tartozik bele**, a PDF rossz
formátum, a JSON/XML/CSV ajánlott, metaadattal együtt.

**A törlés és az export között nincs jogi kapcsolat.** A (68) preambulumbekezdés kifejezetten
függetlennek mondja a két jogot, és sem a Google, sem a GitHub, sem a Slack nem kényszerít
exportot törlés előtt — legfeljebb ajánl.

**Ebből az következik, hogy a D-24 szigorúbb, mint a jogi minimum.** Ez nem hiba: jó szabály,
és a tulajdonos házirendje. De a specifikációban nem szabad úgy állnia, mintha megfelelési
kényszer lenne — mert akkor egy későbbi olvasó nem tudja, hogy lazíthat-e rajta.

A mi csomagunk egyébként megfelel az iránymutatás szellemének: mappa markdown fájlokkal plusz
egy JSON manifeszt, metaadattal. Nem PDF.

---

## 5. Biztonság: itt van egy valódi, dokumentált támadási forma

A **Zip Slip** nem elméleti kockázat, hanem nevesített sebezhetőség: nem validált bejegyzésnév
(`../../valami`) hozzáfűzése a célútvonalhoz, aminek eredménye fájlfelülírás vagy
kódfuttatás. A hivatalos elhárítás (CWE-22): **a feloldott, kanonikus útvonalat kell
ellenőrizni**, hogy a célkönyvtáron belül marad-e — nem a nyers stringet.

Mellette a **CWE-409** (dekompressziós bomba): a **kicsomagolt** méretet kell korlátozni, nem
a tömörítettet.

Ez a két dolog akkor is kötelező, ha csak a saját formátumunkat fogadjuk el — mert egy ellenséges
csomag is állíthatja magáról, hogy a miénk.

---

## 6. Behozatal és indexelés: nincs új gépezet

Az Elasticsearch hivatalosan ajánlja a frissítési időköz kikapcsolását tömeges betöltéshez. Az
**SQLite FTS5-nek viszont nincs dokumentált tömeges-betöltési ajánlása** — ez fontos korrekció
a kiinduló feltételezésünkhöz képest, és azt jelenti, hogy **nem trükközünk az indexszel.**

Nem is kell: a D-19 szerint a **fájl a véglegesítés pontja**, és ha az indexelés elmarad,
a bejegyzés az újraindexelési listára kerül. **A tömeges import ugyanezt használja**: kiírja a
fájlokat, ráteszi őket a listára, az indexelés a háttérben utoléri. Az állapot-képernyő már ma
is mutatja a listát, a beágyazás pedig a D-16 óta külön konténerben fut, tehát nem állítja meg
a keresést.

**Egyetlen új mechanizmus sem kell hozzá.**

A részleges hibára a kutatás nem ad egységes mintát — architektúrafüggő. Fájlrendszeren a
teljes import atomicitása **nem érhető el**, és a vizsgált eszközök közül egyik sem állítja,
hogy elérné. Amit tudunk: az előnézet jóváhagyásáig **semmi nem íródik**, utána fájlonként
atomi írás (D-07), a végén pedig lista arról, mi ment be és mi nem.

---

## 7. A javasolt megvalósítás egy lapon

| Kérdés | A válasz |
|---|---|
| Formátum | ZIP: a mappafa úgy, ahogy van, plusz `manifest.json` a gyökérben |
| Hatókör | útvonal-előtag; négy előbeállítás: teljes fa, egy projekt, egy kategória, egy személyes mappa |
| Mi utazik | a mostani fájlok + a három fejlécmező + a manifeszt |
| Verziók | alapból nem; kapcsolóval igen — és ez a másolat kikerül a törlés hatálya alól |
| Index | soha (eldobható, a fájlból újraépül) |
| Jogosultság | a manifesztben információként; importnál **soha nem alkalmazzuk** — a cél útvonalából jön |
| Audit napló | nem megy az exportba; az import viszont naplózott esemény |
| Ütközés | mindig új verzió; azonos tartalomnál „nincs változás" |
| Történet importja | új fájlnál bejön, létező fájlnál eldobjuk (az előnézet kiírja) |
| Idegen csomag | elutasítva — csak a saját formátumunk |
| Kötelező előnézet | igen: mi új, mi ütközik, mi elutasított — írás előtt |
| Biztonság | kanonikus útvonal-ellenőrzés, kicsomagolt méretkorlát, mezővalidáció |
| Ki indíthatja | mindkettőt a jogosultsága szerint |

---

## 8. Ami nyitva marad

**A történettel készült export és a „jogosultság szerint bárki" együtt gyengíti a végleges
törlés garanciáját.** Aki egy projektet olvashat, elvihet egy verziótörténetes másolatot — és
azt egy későbbi végleges törlés nem éri el. Két szűkítés jöhet szóba: a történet-kapcsoló csak
adminnak, vagy a történettel készült export külön, kiemelt naplóesemény. A második amúgy is
kell; a kérdés az első.

**A manifeszt pontos szerkezete.** Elég egyszerűnek kell lennie ahhoz, hogy kézzel is
megírható legyen — különben a „csak a sajátunkat fogadjuk el" szabály elzárja a kezdeti
feltöltés útját.

**A csomagméret korlátja.** A kutatás adott iparági számokat (GitHub 50 MiB figyelmeztetés /
100 MiB tiltás, PyPI 100 MB fájlonként), de a mi tartalmunk markdown, tehát a méret nem a
fájlokból, hanem a darabszámból jön. Ez mérési feladat, nem átvehető szám.
