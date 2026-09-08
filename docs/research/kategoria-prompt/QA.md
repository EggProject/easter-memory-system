# Önellenőrzés — `kategoria-prompt` kampány

Lezárva: 2026-09-06. Ez a fájl azt írja le, **hol tévedtünk és mit nem tudtunk megerősíteni.**
Olvasd el, mielőtt bármelyik számot használnád.

---

## A legfontosabb: erre a kampányra NEM futott adverzariális ellenőrzési kör

A `szerver-technika` és a `skalazas` kampányoknál külön ellenőrző ügynökök próbálták megdönteni
a kereső ügynökök állításait. Itt ez **nem történt meg** — a kereső ügynökök saját maguk
ellenőrizték a fő állításaikat (a két legfontosabb Anthropic-küszöböt kétszer, eltérő promptú
lekéréssel is), de nincs független támadás az anyagon.

Gyakorlati következmény: a `Magas` megbízhatóságú sorok az `allitasok.csv`-ben azok, ahol a
forrásanyag maga két független elsődleges forrás egyezésére hivatkozik. Minden más sornál a
tier a legerősebb támpont, nem egy ellenőrzési verdikt.

---

## A kutatási terv egy feltevése megdőlt — jó irányba

A `00-terv.md` abból indult ki, hogy „senki nem mond ki ideális számot”, és azt vártuk, hogy
legfeljebb közvetett támpontokat találunk.

**Ez tévedés volt.** Több hivatalos forrás mond ki **explicit, számszerű küszöböt**:

- Anthropic Tool Search Tool: „10 or more tools” / „more than 10k tokens” / „degrades once you
  exceed 30–50 available tools”
- Anthropic Skills útmutató: „more than 20 - 50 skills enabled simultaneously”
- Model Context Protocol kliens-ajánlás: „a threshold as a percentage of the context window.
  For example, 1%-5%”
- OpenAI: „fewer than 20 functions”, névtéren belül „fewer than 10 functions”

A korábbi körben rögzített „senki nem mond ki ideális számot” állítást tehát **vissza kell
vonni**: kategória-darabszámra tényleg nem mond ki senki ideális számot, de **eszköz- és
skill-darabszámra igen**, és ezek a mi esetünkre átvihetők.

---

## Amit nem sikerült megerősíteni, ezért nem használjuk

1. **„Anthropic's independent implementation achieved 98.7% reduction”** — egy független blog
   állítása. Egyetlen elsődleges forrásból sem sikerült megerősíteni. **Kizárva.**
2. **A Chroma „Context Rot” riport disztraktor-szekciójának pontos százalékai** — csak
   grafikonon vannak, szövegesen nem. Csak a kvalitatív irányt (`már egyetlen disztraktor is
   ront`) idézzük, számot nem.
3. **A LongIns pontos táblázata** — a lekérésekből csak két minőségi mondat jött ki. A „GPT-4
   128k rosszul teljesít 16k-nál” állítást tartjuk, számot nem.
4. **A ToolLLM retrieval-pontossági számai** — a teljes cikk mélyebb átvizsgálása nem történt
   meg, csak az absztrakt. Csak a szerkezeti megállapítást (49 kategória + retriever) használjuk.

---

## Ahol tudatosan szigorúbbak voltunk, mint a forrás

Az Anthropic saját, saját termékére vonatkozó teljesítményszámai — **77K → 8,7K token (85%)**
és **79,5% → 88,1% pontosság** — hivatalos Anthropic-oldalon vannak, mégis **T2-ként** kezeljük,
nem T1-ként, mert gyártói önértékelések független reprodukció nélkül. A küszöb-**ajánlás**
maga (10 eszköz / 10 000 token) T1, mert az konfigurációs irányelv, nem teljesítményállítás.

Ugyanígy T3 minden fórumbejegyzés, akkor is, ha hivatalos domainen van — a domain nem tesz egy
hozzászólást elsődleges forrássá. Ez érinti a `modelcontextprotocol/modelcontextprotocol`
GitHub-vitafonal „60-80 tool jól működik, 100 fölött bontsd szét” állítását.

---

## A friss preprintek súlya

Az SQ-05 három legközvetlenebbnek tűnő forrása — Instruction Stacking Collapse, Phase
Transitions, Prospective Memory Failures — mind **2026-os, nem peer-reviewed preprint**,
egy- vagy kétszerzős munkák. Az `allitasok.csv`-ben ezért `Alacsony` megbízhatóságot kaptak,
a T1 besorolás ellenére.

Ezek adják a legerősebb számokat (93% → 27%, 96% → 20%), tehát **éppen a leglátványosabb
adatok a leggyengébben alátámasztottak.** A régi, sokat citált, peer-reviewed munkák
(Lost in the Middle, GSM-IC, RULER, Same Task More Tokens) adják a szolidabb, de kevésbé
drámai képet — a döntést ezekre alapoztuk.

---

## A kampány két valódi kutatási rése

Ezekre **nincs válasz a szakirodalomban**, nem arról van szó, hogy nem találtuk meg:

1. Nincs mérés arra, hogy egy **választható kategória-menü** rontja-e a hívó agent saját,
   független feladatát. A legközelebbi mérés egy **betartandó megkötés** és egy feladat
   versenyét méri — más helyzet.
2. Nincs mérés arra, hogy **azonos token-keret mellett** sok rövid vagy kevés hosszú leírás
   a rosszabb.

A `4.1`-es sávhatárok a `SZINTEZIS.md`-ben ezért **más rendszerek kimondott küszöbeiből**
származnak, nem a mi elrendezésünkre végzett mérésből. Ezt a felületen is ki kell írni.

---

## Módszertani figyelmeztetés, ami a döntést befolyásolta

A NoLiMa és a RULER benchmark ugyanarra a kérdésre gyökeresen eltérő képet ad, és a különbség
oka azonosítható: a RULER megenged szó szerinti lexikai kapaszkodót, a NoLiMa kizárja.

Egy kategória-választás **szemantikai**, nem szó szerinti egyezésen alapul — tehát a NoLiMa
pesszimistább képe a relevánsabb. Ezért a `SZINTEZIS.md` a hivatalos sávok **alsó** széléhez
igazítja a zöld határt, nem a felsőhöz.

---

## Folyamathiba, amit a tulajdonos jelzett

A keresések Sonnet ügynökökkel futottak, ahogy a szabály előírja, de az első három al-kérdést
**egyesével indítottam, nem párhuzamosan** (SQ-01, aztán SQ-02, aztán SQ-03, külön üzenetekben).
Az SQ-04 és SQ-05 már egyetlen üzenetben, párhuzamosan futott. Ez nem az anyag minőségét
érintette, hanem az időt — de a szabály attól még szabály volt.
