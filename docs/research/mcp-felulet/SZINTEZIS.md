# Szintézis — az MCP felület

Kampány: `mcp-felulet` · Lezárva: 2026-09-12 · A szintézist a vezető (Opus) írta,
a kereséseket négy Sonnet ügynök végezte, párhuzamosan.

---

## 1. A kiindulópontom elavult volt

A terv a `2025-06-18`-as specifikációt feltételezte. **A ma érvényes stabil változat a
`2026-07-28`**, és ez nem finomhangolás, hanem **átépítés**: megszűnt az `initialize`
kézfogás, megszűnt a munkamenet-fogalom és az `Mcp-Session-Id`; minden kérés magában hordozza
a verziót és a képességeket; új a `resultType` mező és a több körös kérés (MRTR).

A tulajdonos kimondta, hogy a legújabbat használjuk. **Egy kockázatot viszont ki kell mondani:**
a kiadás nagyjából hat hetes, és a kutatás szerint a legtöbb létező cikk és SDK-dokumentáció
még a régi, munkamenet-alapú modellt írja le. Ezt a döntés előtt mérlegelni kell.

---

## 2. A hibamodell — ez a legfontosabb, és közvetlenül érint négy döntést

A specifikáció **két csatornát** különít el élesen, és a `schema.ts` szó szerint megmondja,
melyiket mikor:

> „Any errors that originate from the tool SHOULD be reported inside the result object, with
> `isError` set to true, not as an MCP protocol-level error response. Otherwise, the LLM would
> not be able to see that an error occurred and self-correct."

- **Protokoll-hiba** (JSON-RPC `error`): ismeretlen eszköz, hibás kérés. A kliens **MAY**
  adja tovább a modellnek — tehát **nem biztos, hogy eljut hozzá**.
- **Eszköz-hiba** (`isError: true` az **eredményben**): üzleti szabály sértése. A kliens
  **SHOULD** adja tovább a modellnek.

**Amit ez nálunk eldönt.** Minden üzleti elutasítás az eredménybe megy, nem protokoll-hibaként:
a hiányzó törlési indoklás (D-21/9), a kategória-költségvetés túllépése (D-26), a csonka
keresési válasz (D-32/6), az újraindexelési kérés elutasítása (D-33/1). Ha ezeket
protokoll-hibaként adnánk vissza, **a hívó modell nem biztos, hogy látná** — és akkor nem tud
javítani.

**Egy kivétel, amit külön kell gondolni:** a jogosultság-hiány. A D-13 szerint amihez nincs
jog, az **nem létezik**. Egy „nincs jogod ehhez" hibaüzenet önmagában elárulná, hogy van ott
valami. A válasznak tehát nem elutasításnak kell lennie, hanem **üres eredménynek** — ugyanannak,
amit egy nem létező útvonal ad.

---

## 3. Az azonosítás — itt van a valódi kockázat, és van rá válasz

### 3.1 Amit a specifikáció ad, és amit nem

**Helyi (stdio) szervernél a specifikáció kimondottan elhárítja magától a kérdést:**

> „Implementations using an STDIO transport SHOULD NOT follow this specification, and instead
> retrieve credentials from the environment."

Vagyis a stdio ágon **a protokoll semmit nem ad** az ember azonosításához. Ha a rendszerünk
ott is működni akar, **magának kell felépítenie és garantálnia** az azonosítást.

**Távoli (HTTP) szervernél** a bevett minta két mélyen megvizsgált valós implementációban
ugyanaz: OAuth token → a `sub` és `aud` igény ellenőrzése → leképezés belső felhasználóra. A
jogosultsági leképezés maga **kifejezetten a specifikáción kívül esik**.

### 3.2 A jó hír, ami eldönti a kérdést

A modellünk — a jog emberhez kötve, az agent csak közvetítő — **megvalósítható**, és nem
elméletben: pontosan ezt csinálja a legnagyobb valós, sokfelhasználós MCP-kliens. Az Anthropic
saját dokumentációja szerint

> „A pure machine-to-machine client_credentials grant… is not supported. Every connection
> requires user consent."

A specifikáció saját grant-iránymutatása ugyanezt mondja: Authorization Code = ember nevében;
Client Credentials = „no need to impersonate the end user".

**Tehát az agent a felhasználó jogaival fut, nem szolgáltatás-fiókként.** Ez a D-11
alapfeltevése, és most már nem feltevés, hanem az iparági minta.

### 3.3 Ami ebből ránk vár

A stdio ágon nekünk kell kitalálni, honnan jön az ember. A D-25 egyszeri beállító linkje már
precedens arra, hogy a rendszer generál egy titkot, amit az ember elhelyez. Ugyanez a forma
itt is működik: **a felületen generált, felhasználóhoz kötött token**, amit az agent a
környezetéből olvas.

---

## 4. Az eszközfelület alakja

### 4.1 Amit a gyártók egybehangzóan mondanak

- A leírás **három-négy mondat**: mit csinál, mikor kell, mikor NEM kell, és mit jelentenek a
  paraméterek. Az OpenAI „gyakornok-tesztje": megértené-e egy új ember belőle.
- A paraméterek neve **legyen egyértelmű** — `user_id`, ne `user`.
- **Kevesebb, nagyobb eszköz** jobb, mint sok kicsi. Az Anthropic saját mérése szerint az
  eszközválasztás **30–50 eszköz fölött romlik**; az OpenAI „20 alatt" mond. A két szám
  eltérése maga is adat.
- Az eszközhasználati példák a bonyolult paraméterkezelés pontosságát **72%-ról 90%-ra** vitték.

**Nálunk ez nem szorító korlát:** hat-hét eszközről beszélünk, jóval a küszöbök alatt. A
tanulság inkább a leírásokra és a példákra vonatkozik.

### 4.2 A kötelező indoklás-paraméterek — egy figyelmeztetés

A szigorú, nyelvtan-vezérelt eszközhasználat **garantálja, hogy a kötelező mező jelen lesz és
jó típusú** — de **nem garantálja, hogy értelmes**. Egy modell kielégítheti a „kötelező
indoklás" szabályt egyetlen szóval.

Ez érinti a D-21/9-et (kötelező törlési indoklás minden csatornán) és a D-26/7-et
(indoklás a kategória előtt). **A séma nem elég**: a leírásban meg kell mondani, mit várunk,
és a rendszernek legalább az üres vagy triviális indoklást vissza kell utasítania — az
eredményben, `isError: true`-val, hogy a modell javíthasson.

### 4.3 Hibaüzenet, amiből a modell felépül

> „Write instructive error messages. Instead of generic errors like 'failed', include what went
> wrong and what Claude should try next… This gives Claude the context it needs to recover or
> adapt without guessing."

Dokumentált viselkedés: a modell **kettő-három javítási kísérletet** tesz, mielőtt feladja.

**Mért adat viszont nincs** arra, hogy a megfogalmazás hogyan hat a helyreállásra, és arra sem,
mi visz végtelen ciklusba. Ez nyílt hiány.

---

## 5. Amit a létező memória-szerverek tanultak

A hivatalos referencia-szerver kilenc eszközt ad, és a keresése a **saját kódkommentje szerint
is „very basic"**: kis-nagybetű-független részszöveg-egyezés, nulla rangsorolás, teljes
tartalom visszaadva, nincs lapozás. **Nincs benne felhasználó-fogalom.**

Négy tanulság, ami közvetlenül ránk vonatkozik:

1. **Konkurens írás fájlkorrupciót okozott** a hivatalos szerverben, és a javítás pontosan az,
   amit a D-07 előír: mutáció-zár és ideiglenes fájl + átnevezés. **A mi döntésünk tehát nem
   túlbiztosítás** — ez a hiba megtörtént.
2. **A mem0 dokumentációja és viselkedése elvált**: az ígért ellentmondás-feloldást egy későbbi
   architektúra kivette, és két ellentmondó tény azóta mindkettő bekerül. A közösség saját
   auditáló eszközt épített rá.
3. **A Graphiti megkülönbözteti a konfliktus feloldását a jelzésétől** — felold, de nem szól.
   Ez a mi D-20-unk (íráskori duplikátum-figyelmeztetés) melletti érv: a jelzés külön érték.
4. **Kétlépcsős törlési kérelem egyik vizsgált rendszerben sincs.** A törlés mindenütt
   közvetlen és visszafordíthatatlan. A D-21 ebben egyedi — és ez nem baj, csak tudni kell,
   hogy nincs kitől mintát venni.

Egy erős precedens az eszközszám ellen: a **mem0 Claude Code bővítménye kilenc olvasó/író
eszközt cserélt le egyetlen csak-olvasó keresésre**. Indoklást nem közöltek.

---

## 6. Két dolog, ami a mi terveinket közvetlenül veszélyezteti

### 6.1 A szerkeszthető kategóriák és az értesítés

A D-22 szerint a kategóriák és promptjaik a felületről szerkeszthetők. A hívó agent viszont az
**eszközleírásban** kapja meg őket (D-26/8: pontosan egy helyen).

A `2026-07-28` specifikációban a kliensnek **kifejezetten fel kell iratkoznia** a lista
változására — enélkül **soha nem kap értesítést**. Vagyis egy agent, ami nem iratkozott fel,
tetszőlegesen sokáig **elavult kategórialistával** dolgozhat.

A D-06 `prompt_version` mezője pont erre való, de eddig csak a fájlba írtuk. **Az MCP felületen
is meg kell jelennie**, hogy a hívó észrevehesse az elcsúszást.

### 6.2 Az annotációk nem védenek

A `destructiveHint` és társai **csak jelzések**. A specifikáció kétszer is kimondja, hogy nem
megbízható szervertől **nem szabad rájuk biztonsági döntést alapozni**.

Vagyis a „ez a művelet veszélyes" jelzés **dokumentáció, nem védelem**. A védelmet a
rendszernek magának kell adnia — a D-20 kétlépcsős duplikátum-ellenőrzése és a D-21 kötelező
indoklása pontosan ilyen. **Formális „figyelmeztet, aztán kényszeríthető" minta a protokollban
nincs**; ami van, az közösségi konvenció.

---

## 7. Ami nincs a specifikációban

- **Válaszméret-korlát nincs.** Sem korlát, sem eljárás arra, mit tegyen a szerver, ha a
  válasz túl nagy. A lapozás megvan (opak kurzor), a méret a szerver dolga. Tájékoztatásul: a
  Claude Code alapértelmezésben **25 000 tokennél** vágja a válaszokat.
- **Idempotencia-kulcs nincs.** Az `idempotentHint` csak jelzés, alapértéke hamis; ismételt
  hívás kezelésére a protokoll semmit nem ad.
- **Névtér-konvenció csak SHOULD szintű.** Az eszköznév egyedisége egy szerveren belülre
  skálázott, és a `serverInfo.name`-re **kifejezetten tilos** építeni.

---

## 8. Ami döntést kíván

| # | Kérdés | A javaslatom |
|---|---|---|
| 1 | Melyik specifikáció-változat | `2026-07-28`, vállalva a hat hetes érettség kockázatát |
| 2 | Hány eszköz, milyen alakban | Külön eszköz szándékonként, 6–7 darab — jóval a küszöbök alatt |
| 3 | Ki a hívó a stdio ágon | Felületen generált, felhasználóhoz kötött token a környezetből |
| 4 | A kategória-elcsúszás kezelése | A `prompt_version` minden válaszban, és íráskor jelzés, ha elavult |
