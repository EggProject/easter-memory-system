# Önellenőrzés — `import-export` kampány

Lezárva: 2026-09-06. Olvasd el, mielőtt bármelyik számot vagy állítást használnád.

---

## Erre a kampányra NEM futott adverzariális ellenőrzési kör

A kereső ügynökök a saját fő állításaikat ellenőrizték — az SQ-03 esetében a jogszabály-idézeteket
a mentett pillanatképekkel is összevetették —, de **független támadás nem futott az anyagon**.
Az `allitasok.csv` megbízhatósági oszlopa ezért nem ellenőrzési verdikt, hanem a forrás
erősségének gépies besorolása.

Megoszlás: **89 állításból 1 kapott „magas"** minősítést (négy független elsődleges forrás
konvergenciája: „nincs elterjedt csereformátum"), 67 „közepes", 21 „alacsony". Ez a korpusz
természete: nagyrészt egy-egy termék hivatalos dokumentációjából származó tények, amiket nincs
mivel keresztellenőrizni — a Notion exportjáról csak a Notion doksija nyilatkozik.

---

## Két kiinduló feltevés megdőlt

**1. Azt feltételeztük, hogy az SQLite FTS5-nek van dokumentált tömeges-betöltési ajánlása.**
Nincs. Az automerge/crisismerge/merge/optimize mechanizmus dokumentált, de **explicit „bulk
loading" szakasz nem létezik** a doksiban. Ez érdemi korrekció: azt jelenti, hogy nem trükközünk
az indexszel importnál, hanem a meglévő újraindexelési utat használjuk (D-19).

**2. Azt feltételeztük, hogy létezik valamilyen bevett csereformátum.** Nem létezik. Ez a hiány
végül a legerősebb eredmény lett — és ez fordította meg a tervezést: nem formátumot találunk ki,
hanem felismerjük, hogy a mappafa maga az.

---

## Amit nem sikerült megerősíteni

1. **A Notion markdown-exportjának metaadat-tartalma.** A hivatalos súgó nem nyilatkozik arról,
   hogy időbélyeg vagy szerző bekerül-e a fájlba. Csak az API-modell ismeri ezeket a mezőket.
   Nem állítunk róla semmit.
2. **A Joplin JEX manifeszt létezése és szerkezete.** Nem találtuk meg elsődleges forrásból.
3. **A tar-kicsomagolás atomicitása** és a **Joplin belső tranzakció-kezelése** — nincs
   elsődleges forrás.
4. **Az npm hivatalos, számszerű csomagméret-korlátja** — nem találtuk meg.
5. **Az Apple emberi felület-irányelvei** — az oldal JavaScripttel renderel, nem volt lekérhető.

---

## Ahol a bizonyíték hiánya maga az eredmény

**Nincs mért, kvantitatív bizonyíték arra, hogy melyik importütközés-stratégia okoz kevesebb
adatvesztést vagy kevesebb felhasználói hibát.** Ez kimerítő keresés után kimondott „nincs
ilyen", nem „nem találtuk meg" — és ez fontos, mert ez a kérdés dönti el az egész
ütközéskezelést.

Ami helyette van, az **analógia**: git tartalmi ütközéseknél a kézi feloldás 26-szoros
hibaarányú kóddal jár (Brindescu és társai, 2020, lektorált). Más domén, más ütközésfajta —
irányjelzésnek jó, bizonyítéknak nem.

Ugyanígy: az alapértelmezésekre vonatkozó irányelvek (GNOME, NNGroup) **jórészt bevett szakmai
gyakorlat, nem mért kutatás** — az NNGroup cikke maga is elismeri, hogy nem hivatkozik kutatásra.

---

## Egy módszertani megjegyzés a jogi részhez

A GDPR szövegét a hivatalos EUR-Lex forrásból kellett kinyerni, mert a szokásos lekérő eszköz
szerzői jogi szűrője megakadályozta. Az idézetek **betű szerintiek**, és a mentett
pillanatképekkel összevetve egyeznek.

Ügyvédi iroda vagy szakmai blog elemzése **T2**, nem T1 — a rendelet szövege az egyetlen T1
ebben a kérdésben. Ez azért fontos, mert a 15. és a 20. cikket a másodlagos irodalom gyakran
összemossa, és mi ezt a hibát nem akartuk átvenni.

**Ez nem jogi tanácsadás, és nem is annak készült.** A kampány azt gyűjtötte össze, mit mond a
jogszabály szó szerint, és mit csinálnak a valós rendszerek.

---

## Tier-skálák keveredése

Az al-kérdések ügynökei nem egyforma skálát használtak: az SQ-01 és SQ-04 T1–T3-at, az SQ-02
T1–T6-ot, az SQ-03 T0–T3-at. **Nem egységesítettük**, mert az átminősítés hamisítás lenne —
a `linkek.md` és az `allitasok.csv` elején jelezve van.
