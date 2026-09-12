# Ellentmondások és feszültségek a forrásokban — sq01

## 1. SQLite trigram vs. PostgreSQL pg_trgm — eltérő tervezési döntés, nem tényellentmondás

Nem klasszikus "ellentmondás" (nem ugyanazt a tényt állítják kétféleképp), hanem **eltérő tervezési döntés**, amit érdemes explicit módon kiemelni, mert könnyen összekeverhető:

- **SQLite FTS5 trigram**: a hivatalos dokumentáció saját példája szerint a trigramok **átnyúlhatnak szóhatárokon** (`"hij klm"` mintázat egyezik a `'...hij KLMNOPQRST uvw...'` sorra, a szóköz karakterként számít bele a trigramba).
- **PostgreSQL pg_trgm**: a hivatalos dokumentáció kifejezetten **kizárja** ezt: *"pg_trgm ignores non-word characters (non-alphanumerics) when extracting trigrams"*, és minden "szót" (nem-alfanumerikus karakterekkel határolt darabot) külön, szóköz-paddel kezel — tehát **nem** képez szóközön átnyúló trigramot.

**Következmény, amit fontos kimondani:** ha valaki a két rendszer trigram-viselkedését azonosnak feltételezi ("a trigram az trigram"), az téves. A két implementáció **eltérő pontossági/fals pozitív karakterisztikával** rendelkezik latin szövegen, bár CJK-ra (ahol nincsenek natív szóhatárok) ez a különbség valószínűleg kevésbé releváns.

## 2. PostgreSQL pg_trgm és a CJK-támogatás — a hivatalos doksi hallgat, a harmadik féltől származó doksi konkrétumot mond

A **pg_trgm hivatalos PostgreSQL-dokumentációja** (`pgtrgm.html`) sehol nem említi, hogy a modul alapból kizárja a nem-alfanumerikus (pl. CJK) karaktereket a trigram-képzésből — ez implicit, a "non-word characters (non-alphanumerics)" megfogalmazásból következtethető ki, de nincs kimondva.

A **pg_bigm harmadik féltől (NTT-eredetű) projekt dokumentációja** viszont **explicit kimondja**: *"You can use full text search for non-alphabetic language by commenting out KEEPONLYALNUM macro variable in contrib/pg_trgm/pg_trgm.h and rebuilding pg_trgm module"* — vagyis nevesíti a konkrét forráskód-korlátozást (`KEEPONLYALNUM` makró), amit a hivatalos pg_trgm-oldal nem tesz meg.

**Ez nem ellentmondás a szó szoros értelmében** (a két forrás nem mond egymásnak ellent), hanem **kiegészítő, csak a másodlagos forrásból elérhető részletezettség** — fontos jelezni, hogy ez a konkrét, technikailag pontos állítás (`KEEPONLYALNUM` makró neve) **nem hivatalos PostgreSQL-forrásból**, hanem egy T2-es projektdokumentációból származik, amit a hivatalos pg_trgm-oldal sem meg nem erősít, sem cáfol.

## 3. Trigram-index méretnövekedés — nagyságrendi szórás, nem tényellentmondás, de zavaró lehet, ha nem magyarázzuk

Két talált mérés (`andrewmara.com`: ~1,85×; `hermes-agent` GitHub issue: 18,3×) **látszólag ellentmond egymásnak**, ha valaki csak a két számot nézi. Nem tényellentmondás, mert:

- Az `andrewmara.com` mérés **általános, természetes szöveges** (log/URL-szerű) adatra vonatkozik, 18,2 millió sorra.
- A `hermes-agent` issue kifejezetten **strukturált, ismétlődő JSON-mezők** (tool_calls) trigram-indexelésére vonatkozik, amit a szerző maga is "novel documentation of JSON amplification"-ként jellemez — vagyis egy **tudottan szélsőséges, torzított eset**.

**Tanulság, amit a jelentésbe explicit be kell építeni:** a trigram-index méretnövekedése **erősen tartalomfüggő**, a két szám nem egy "tartomány" két végpontja ugyanarra a jelenségre, hanem két, minőségileg eltérő terhelési profil eredménye. Egy tervezési dokumentumban **egyik számot sem szabad "az" elvárt szorzóként idézni**.

## 4. Az OpenSearch dokumentáció önmagának ellentmond(ani látszik) a `cjk` analizátor ajánlásában

Az OpenSearch hivatalos oldal egyszerre:
(a) dokumentálja a beépített `cjk` (bigram-alapú) analizátort mint elérhető, működő eszközt, és
(b) ugyanazon az oldalon kifejezetten azt mondja: *"You may find that the icu_analyzer in the ICU analysis plugin works better for CJK text than the cjk analyzer."*

**Ez nem valódi ellentmondás**, hanem a hivatalos dokumentáció **önmaga relativizálja saját beépített megoldását** — vagyis még a gyártó/karbantartó is elismeri, hogy a legegyszerűbb (bigram) megoldásuk nem a legjobb, és van jobb, de külön pluginhoz (ICU) kötött alternatíva. Ez fontos analógia a mi esetünkhöz: **a "működik" és a "legjobb minőségű" nem ugyanaz**, még a natívan CJK-ra tervezett eszközöknél sem.

## 5. Nincs talált közvetlen ellentmondás a 6. pont (embedding CJK-teljesítmény) kapcsán

A BGE-M3 cikk saját mérése (mE5-large vs. BGE-M3, MIRACL-on) és az általános piaci narratíva ("BGE-M3 jobb multilingual/CJK-ra, mint a korábbi E5-modellek") **összhangban van** — nem találtunk olyan T1/T2 forrást, amely ennek ellentmondana (pl. amely azt állítaná, hogy multilingual-E5-large jobb CJK-n, mint BGE-M3). Ezt fontos jelezni: **ezen a ponton a bizonyítékok konvergálnak**, nincs vitatott állítás rögzítésre.

## Összegzés

Az ebben a kutatási körben talált "ellentmondások" túlnyomórészt **eltérő tervezési döntések vagy eltérő terhelési profilok félreértelmezhető egymás mellé állításai**, nem valódi, egymást kizáró ténybeli állítások ugyanarra a kérdésre. Egyetlen pont sem igényel a szintézisben "vitatott" (Vitatott/GRADE) minősítést két egymásnak ellentmondó, azonos súlyú forrás miatt — inkább **kontextus-függőségre és a források eltérő hatókörére** kell figyelmeztetni a jelentésben.
