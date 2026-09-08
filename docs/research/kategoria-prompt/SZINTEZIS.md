# Szintézis — a kategória-választó prompt költségvetése

Kampány: `kategoria-prompt` · Lezárva: 2026-09-06 · A szintézist a vezető (Opus) írta,
a kereséseket öt párhuzamos Sonnet ügynök végezte.

> Ez a fájl a **következtetéseket** mondja ki. A forrásokat és a szó szerinti idézeteket a
> `kivonat.md` és az `allitasok.csv` tartalmazza. Ami itt számként szerepel, annak ott van
> a forrása.

---

## 1. A kérdés

A kategóriák promptját **nem a mi rendszerünk dolgozza fel**. A memóriát író külső agent
kapja meg — Claude, Codex, bármelyik —, hogy el tudja dönteni, melyik kategóriába való a
bejegyzés. Ezért nem lehet akármekkora.

A vezető felismerése, amit a kutatásnak igazolnia vagy cáfolnia kellett:

> A modell **nem egy kategória promptját kapja, hanem az összesét egyszerre**, mert azok
> közül választ. Tehát a korlátnak nem a darabszámra és nem a prompt hosszára külön kell
> vonatkoznia, hanem **a kettő szorzatára**.

**A kutatás ezt igazolta** — sőt, kiderült, hogy a valós rendszerek pontosan így is
szabályozzák, csak nem „szorzat” néven. Minden megtalált hivatalos küszöb az **eredmény
össz-token-számra** vonatkozik, ami matematikailag ugyanaz, mint darabszám × átlagos hossz.
Külön darabszám-limit és külön hossz-limit sehol nincs egymás mellé téve; ahol darabszámot
mondanak, ott is odateszik a token-alternatívát („10 or more tools **or** more than 10k
tokens”).

---

## 2. Az öt megállapítás, ami eldönti a kérdést

### 2.1 A helyes analógia nem a SKILL.md, hanem a skill **metaadata**

Az Anthropic Agent Skills három szintet definiál, és ez a hármas tagolás pontosan azt a
különbséget képezi le, ami minket érdekel:

| Szint | Mikor töltődik | Költség | Mi ez |
|---|---|---|---|
| 1 — metaadat | **mindig, indításkor, MINDEN skillé** | **~100 token / skill** | név + leírás |
| 2 — utasítások | csak a **kiválasztott** skillnél | < 5 000 token | a SKILL.md test |
| 3 — erőforrások | csak ha megnyitja | 0, amíg nem olvassa | csatolt fájlok |

A kategória-promptunk szerkezetileg **első szintű**: mindegyik, mindig, egyszerre, éppen
azért, hogy legyen miből választani. Tehát a mérce a **~100 tokenes nagyságrend és az 1024
karakteres kemény korlát**, nem az 5 000 szavas SKILL.md.

Ez a különbség a kutatás egyik legfontosabb hozadéka, mert a naiv olvasat („a Claude
skilleknél 5 000 szó a limit, akkor nekünk is annyi lehet”) **nagyságrenddel téved**.

Ugyanezt az 1024 karakteres kemény korlátot **két, egymástól független ökoszisztéma**
alkalmazza: az Anthropic Agent Skills és az OpenAI function-calling. Az MCP specifikáció
ellenben a leírásra **semmilyen hosszkorlátot nem ír elő** — csak a névre (1–128 karakter,
SHOULD). Ez nem engedékenység, hanem a specifikáció hallgatása: a korlátot a kliensnek kell
kikényszerítenie.

### 2.2 A tényleges romlás jóval a hivatalos küszöbök alatt kezdődik

A hivatalos küszöbök (Anthropic: 10 000 token; MCP: a kontextusablak 1–5%-a) azt mondják meg,
hol érdemes **átállni másik architektúrára**. Azt nem mondják meg, hol kezdődik a romlás.

A romlás kezdetére van külön mérés, és az sokkal korábban van: irreleváns „töltelék” szöveggel
felduzzasztott, de **változatlan nehézségű** feladatokon a pontosság már **500 token fölött**
csökkenni kezd, és ~3 000 tokennél 0,92-ről 0,68-ra esik (öt modell átlaga).

Ebből a gyakorlati következtetés: **nincs „ingyenes” sáv.** Minden kategória-prompt token
elvesz valamit a hívó agent saját feladatától. A kérdés nem az, hogy „mennyi fér bele”, hanem
hogy „mennyit ér meg”.

### 2.3 A darabszám kevésbé számít, mint az **összekeverhetőség**

Ez a kampány legfontosabb **gyakorlati** eredménye, és nem az volt, amit kerestünk.

- A címketér-csökkentésről szóló mérés szerint nem a nyers osztályszám, hanem a **címkék
  hasonlósága** szabja meg, mekkora címketér kezelhető: finomabb szemcsézetű, egymásra
  hasonlító címkékhez nagyobb `k` kellett, mint durvább címkékhez ugyanazon a domainen.
- Ugyanez a mérés azt is kimutatta, hogy a teljes, **nem szűkített** címkelista puszta
  **átrangsorolása** hozza a lehetséges javulás **78,6%-át**, míg maga a szűkítés csak
  21,4%-ot. Vagyis a sorrend többet ér, mint a rövidítés.
- A Zep dokumentációja kimondja, hogy a típusdefinícióknak **kölcsönösen kizárónak** kell
  lenniük, mert az átfedő vagy kétértelmű leírás inkonzisztens besorolást okoz — és
  hangsúlyozza, hogy ez a **leírások**, nem a nevek átfedéséről szól.
- Független mérés szerint a **szemantikailag erősen hasonló** disztraktor kb. **négyszeresére**
  emeli a hibaarányt a nem hasonlóhoz képest (5,5% → 22,5%).

Ez azt jelenti, hogy **rossz dolgot figyelnénk, ha csak a darabszámot néznénk.** Nyolc élesen
elváló kategória jobb, mint négy egymásba folyó. És erre van eszközünk: **a beágyazó modell,
ami már a rendszer része** — nem szöveggenerálás, tehát nem sérti a szabályt, hogy LLM-et
csak beágyazásra használunk.

### 2.4 Ugyanaz a szöveg más helyen mást ér — és az ellentmondás katasztrofális

- Ugyanazt a kategória-definíciót a rendszerpromptból egy séma-mező leírásába átmozgatva —
  **tartalmi és hosszbeli változtatás nélkül** — a pontosság 11–13 százalékponttal esett két
  modellnél, **még akkor is, amikor a két csatorna egyetértett**.
- Amikor a séma-leírás **ellentmondott** a rendszerprompt kategória-definíciójának, az egyik
  modell 52,5%-ról **7%-ra** zuhant.

Ebből egy kemény tervezési szabály következik: **a kategóriadefiníció pontosan egy helyen
jelenhet meg az MCP felületen.** Ha az eszköz leírásában is ott van és a paraméter enum
leírásában is, és a kettő idővel elcsúszik, az nem apró következetlenség, hanem
teljesítmény-összeomlás.

### 2.5 Egy meglepő, olcsó nyereség

Ugyanabban a mérésben egy kötelező, köztes **indoklás-mező** beépítése a sémába — a válasz
előtt — **15–24 százalékponttal** javította a pontosságot. Ez **több, mint bármelyik
elhelyezési trükk**, amit vizsgáltak.

Ez a mi esetünkben azt jelentené, hogy a bejegyzést író agenttől nemcsak a kategóriát kérjük,
hanem egy rövid indoklást is — és az indoklás létezése önmagában javítja a kategória
minőségét, függetlenül attól, hogy eltesszük-e.

---

## 3. Amit NEM tudunk, és nem is fogunk pontos szám alapján

Ezt élesen ki kell mondani, mert a döntés formáját ez szabja meg.

1. **Nincs mérés arra, hogy egy választható kategória-menü rontja-e a hívó agent saját,
   független feladatát.** Van rá közvetett bizonyíték (egy formázási megkötés jelenléte az
   egyik modell GSM8K-pontosságát 93%-ról 27%-ra vitte le), de az egy **betartandó szabály**
   és egy feladat versenye, nem egy **választható menü** és egy feladat együttélése. Ez
   analógia, nem mérés.
2. **Nincs mérés arra, hogy azonos token-keret mellett sok rövid vagy kevés hosszú leírás a
   rosszabb.** Erre a szakirodalomban egyáltalán nincs adat.
3. **A modellek közötti szórás óriási.** Ugyanarra a jelenségre az egyik mérés 7%-tól 85%-ig
   terjedő romlást talált modelltől függően. Egy szám nem lesz igaz mindenkire.
4. **A tokenizáló mozog.** Az Anthropic dokumentálja, hogy a Claude 4.7-től kezdve ugyanaz a
   szöveg **kb. 30%-kal több tokent** ad, mint a korábbi modelleken. Egy kódba égetett
   token-szám tehát önmagában elavul.
5. **A magyar szöveg kb. kétszer annyi tokenbe kerül, mint az azonos tartalmú angol.** Egy
   karakter-alapú korlát ezért a magyar tartalmat rendszerszinten büntetné.

**Ebből következik, hogy nem tiltunk, hanem jelzünk** — pontosan úgy, ahogy a tulajdonos kérte.
És a jelzés mellé oda kell írni, mire alapozzuk, mert a szám nem egy törvény, hanem egy sáv.

---

## 4. A javasolt költségvetés

### 4.1 Egy szám a mérce: a teljes blokk

A rendszer azt méri, ami ténylegesen a hívó agenthez kerül: **az összes kategória neve és
promptja együtt, plusz a keretszöveg.** Minden más ebből származik.

| Sáv | Teljes blokk | Mire alapozzuk |
|---|---|---|
| **Zöld** | 2 000 token alatt | Az MCP hivatalos ajánlásának alsó széle (a kontextusablak 1%-a) 200 ezres ablaknál |
| **Sárga** | 2 000 – 10 000 token | Már a mérhető romlás zónájában (a romlás ~500 token fölött indul), de még az MCP 1–5%-os sávjában |
| **Piros** | 10 000 token fölött | Az Anthropic kimondott küszöbe („more than 10k tokens” → válts szűrésre), egyben az MCP 5%-a 200 ezres ablaknál |

A két határ mindkét oldalról alá van támasztva: a 2 000 az MCP alsó sávja, a 10 000 egyszerre
az Anthropic explicit küszöbe és az MCP felső sávja. Ez a **legjobban dokumentált két szám**,
amit a kutatás talált.

**A zöld sáv nem azt jelenti, hogy ingyen van.** Azt jelenti, hogy a hívó agentnek nem kell
emiatt architektúrát váltania.

### 4.2 Egy kategória prompt-ja

**Ajánlott felső határ: ~400 token.** Ez annyi, amennyibe az Anthropic saját mérésében egy
**teljes eszközdefiníció** kerül (403 token a puszta 14-hez képest, tehát ~390 token).
Összehasonlításul: az „mindig betöltve” metaadat-szint **~100 token**.

Tehát a sáv, amiben a valós rendszerek mindig-betöltött leírói mozognak: **100 és 400 token
között.** Aki 400 fölé megy, olyat csinál, amire a nagy ökoszisztémákban nincs példa.

Fontos: **tokenben mérünk, nem karakterben.** Az 1024 karakteres iparági korlát angolra van
szabva; magyarul ugyanaz a tartalom kb. kétszer annyi tokenbe kerül, tehát egy karakter-korlát
a magyar tartalmat büntetné.

### 4.3 Darabszám

**Nincs külön darabszám-korlát** — a darabszám a költségvetésen keresztül érvényesül, ahogy a
tulajdonos felismerte. Tájékoztatásul viszont oda kell írni a felületre, mit csinálnak mások:

- OpenAI: „fewer than 20 functions” (puha ajánlás), névtéren belül „fewer than 10”
- Anthropic: 10 eszköz **vagy** 10 000 token fölött kapcsold be a szűrést; **30–50 fölött**
  már látható a romlás
- Anthropic Skills: 20–50 egyszerre engedélyezett skill fölött vizsgáld felül

A szállított öt kategória (D-10) ezekben a sávokban **kényelmesen belül van.**

### 4.4 Hasonlóság-őr — az igazi védelem

A 2.3 pont miatt a rendszernek nem elsősorban a darabszámot kell figyelnie, hanem azt, hogy
**két kategória prompt-ja nem túl hasonló-e**. Mentéskor a szerkesztő beágyazza az új
kategória promptját, összeveti a meglévőkkel, és ha túl közel van valamelyikhez, kiírja:
„ez a kategória nagyon hasonlít erre: …”.

Ehhez **nem kell új komponens** — a beágyazó modell már a rendszer része, és ez nem
szöveggenerálás.

**A küszöb értékét viszont nem tudjuk a szakirodalomból.** Ez mérési feladat: a szállított öt
kategórián kell kalibrálni, és a mért értéket a `90-meresek.html`-be kell beírni. Addig a
szerkesztő megjeleníti a hasonlósági értéket, de nem mond rá ítéletet.

### 4.5 Hogyan számolunk tokent LLM nélkül

Nem hívhatunk API-t, és nem futtatunk szöveggeneráló modellt. Három út van, és mindegyiknek
van hibája:

1. **Beépített BPE tokenizáló könyvtár** — tiszta kódkönyvtár, nem modell-futtatás. Pontos
   arra a tokenizálóra, amelyikét beépítjük; más modelleknél eltér.
2. **A beágyazó modell saját tokenizálója** — már itt van, nem kell semmit hozzátenni, de a
   szótára nem a hívó modellé, tehát rendszerszinten eltér.
3. **Karakter-alapú becslés** — nem igényel semmit, de a magyar/angol kétszeres eltérés miatt
   nyelvenként másképp téved.

Bármelyiket választjuk, a felületnek **oda kell írnia, hogy becslés, és mivel mérve** — mert
a hívó modell tokenizálója változik (Claude 4.7-től ~30% eltérés ugyanarra a szövegre).

---

## 5. Ami ebből döntést kíván

| # | Kérdés | A javaslatom |
|---|---|---|
| 1 | A költségvetés sávjai | 2 000 / 10 000 token, három sáv, tiltás nélkül |
| 2 | Hasonlóság-őr a kategória-szerkesztőben | Legyen, beágyazás-alapon; a küszöb mérési feladat |
| 3 | Token-számlálás módja | Beépített BPE tokenizáló, a felületen jelölve, mivel mérünk |
| 4 | Indoklás-mező az MCP hívásban | Kérjük el; 15–24 pp nyereség, és nekünk nem kerül futásidőbe |

---

## 6. Amit a `90-meresek.html`-be be kell írni

Szám a specifikációban csak akkor lehet, ha a mérési dokumentumban is ott van. Ebből a
kampányból ezek kerülnek oda:

- ~100 token / skill — mindig betöltött metaadat (Anthropic)
- 403 vs. 14 token — egy eszközdefiníció mért költsége (Anthropic `count_tokens`, claude-opus-5)
- 1024 karakter — kemény leíráskorlát az Anthropic Agent Skills és az OpenAI function-calling
  felületén; az MCP specifikáció nem ír elő ilyet
- 10 eszköz / 10 000 token — az Anthropic kimondott küszöbe a szűrésre váltáshoz
- 30–50 eszköz — az Anthropic által megnevezett látható romlási pont
- 20–50 skill — az Anthropic Skills útmutatójának küszöbe
- a kontextusablak 1–5%-a — az MCP hivatalos kliens-ajánlása
- ~500 token / 0,92 → 0,68 ~3 000 tokennél — a romlás kezdete változatlan nehézségű feladaton
- 78,6% / 21,4% — a rangsorolás és a szűkítés hozzájárulása a javuláshoz
- 5,5% → 22,5% — a szemantikailag hasonló disztraktor hibaarány-hatása
- 11–13 pp, illetve 52,5% → 7% — a definíció elhelyezésének és az ellentmondásnak a hatása
- 15–24 pp — az indoklás-mező nyeresége
- kb. 2× — a magyar szöveg token-többlete az angolhoz képest
- kb. +30% — a Claude 4.7-től érvényes tokenizáló-eltérés

**Nyitott mérés:** a hasonlóság-őr küszöbértéke. Nincs a szakirodalomban; a szállított öt
kategórián kell kimérni.
