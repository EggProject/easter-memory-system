# Szintézis — hibamodell, jogosultság-elutasítás, távoli hitelesítés

Kampány: `mcp-hibak` · Lezárva: 2026-09-12 · A szintézist a vezető (Opus) írta,
a kereséseket három Sonnet ügynök végezte, **egy üzenetben, párhuzamosan**.

---

## 1. Miért futott ez a kör

A tulajdonos három dolgot kifogásolt a frissen megírt Spec 40-ben:

1. **Ellenőriztesd** az állítást, hogy a saját hibáinkat nem adhatjuk vissza protokoll-hibaként.
2. **Az üres válasz rossz** jogosultság-hiánynál — és a „nincs jogod" nem feltétlenül baj.
3. **Ezt nem lehet nyitva hagyni, és beállíthatónak kell lennie**, alap ajánlással.

Plusz a távoli hitelesítésnél eddig csak a minta szerepelt, nem a követelmények.

**Mindhárom kifogás jogos volt.** A második és a harmadik tervezési hiba, a negyedik hiányosság.

---

## 2. A hibamodell — az állítás áll, és erősebben, mint gondoltam

**Verdikt: ÁLL**, egy hatókör-pontosítással. Az adverzariális ellenőrzés nem tudta megdönteni.

A legerősebb bizonyíték nem is a specifikáció, hanem a **hivatalos Python SDK dokumentációja**,
ami élesebben fogalmaz, mint az eredeti megállapítás:

> „MCPError is the SDK's protocol error. It is the one exception the tool wrapper does not
> catch: it propagates… **There is no result. No content, no is_error: nothing for the model to
> read.** The host application gets the error instead."

A specifikációban valódi RFC 2119 kulcsszavakkal ott a mondatpár: *„Clients **MAY** provide
protocol errors to language models… Clients **SHOULD** provide tool execution errors…"*.
Mindkét hivatalos SDK forráskódja ezt a kettéválasztást valósítja meg: minden kivétel
`isError`-rá alakul, kivéve a kifejezetten protokoll-célút.

**A döntő részlet a mi szempontunkból:** a séma kanonikus, elnevezett példája
(`invalid-tool-input-error.json`) **kifejezetten a bemeneti és validációs hibákat** teszi
`isError` alá. Ez pontosan a mi esetünk — a kötelező indoklás és a kategória.

**A pontosítás:** a szabály szó szerint a `tools/call`-ra vonatkozik. A `resources/read`-nek
nincs `isError` mezője, ott minden hiba szükségszerűen protokoll-hiba. **Minket nem érint**,
mert csak eszközöket adunk ki — de ez egy további érv amellett, hogy így is maradjon.

Egy apró, nem döntő eltérés: a Python SDK az „ismeretlen eszköz" hibát is `isError`-rá
alakítja, szemben a spec kategorizálásával és a TypeScript SDK viselkedésével.

**Ki kell mondani, mert félreértettem magam is:** saját hibát **igenis visszaadunk**, saját
szöveggel. A kérdés csak az volt, melyik mezőben.

---

## 3. A jogosultság-elutasítás — itt tévedtem, és van kiforrott minta

### 3.1 Amit a HTTP specifikáció mond

Az elrejtés **kifejezetten engedélyezett, de kivételként**:

> „An origin server that wishes to 'hide' the current existence of a forbidden target resource
> **MAY** instead respond with a status code of 404 (Not Found)."

**MAY**, a 403-as szakaszhoz csatolva — nem a 404 alapértelmezett jelentése.

### 3.2 Ajánlott alapértéket egyetlen szabvány sem mond ki

**Ezt nyíltan ki kell mondani.** Sem a HTTP specifikáció, sem az OWASP Top 10, sem az ASVS,
sem az OWASP Authorization Cheat Sheet, sem a vonatkozó CWE-bejegyzések nem mondanak ki
ajánlott alapértéket a 403-vs-404 kérdésre.

Ami a legközelebb áll hozzá, és **normatív**: az ASVS 4.0.3 előírása biztonságérzékeny
hibákra — **általános üzenet plusz egy azonosító**, amivel az esemény visszakereshető. Ez nem
erre a kérdésre íródott, de pontosan azt adja, amit a tulajdonos kért: nem üres válasz, de nem
is árulkodó.

### 3.3 Az egyesített üzenet bevett gyakorlat — de nincs neve

A GitLab dokumentációja szó szerint:

> „A resource couldn't be accessed. For example, an ID for a resource couldn't be found, **or
> the user isn't authorized** to access the resource."

A Google Drive ugyanígy: `notFound`, ha a felhasználónak nincs olvasási joga **vagy** a fájl
nem létezik.

**A GitHub az egyetlen a megvizsgáltak közül, amelyik az indokát is dokumentálja:** hogy ne
erősítse meg privát tárak létezését.

**Ellenpélda is van:** a Kubernetes szándékosan megmondja, mihez nem volt jogod — és egy
2024-es biztonsági bejelentés épp azt kifogásolta, hogy **túl sokat** árul el a jogosultsági
belsőségekből. Vagyis a nyílt út sem kockázatmentes, csak más a kockázata.

### 3.4 A fokozatos modell — ez oldja fel a kifogást

A Google Drive **nem egyetlen szabályt** használ, hanem kettőt: „nem található", ha a
felhasználó nem látja a fájlt — de **explicit elutasítás**, ha már látja, csak írni nem tud.

Ez pontosan a tulajdonos kifogásának feloldása. Azt mondta: *„a nincs jogod hozzá nem feltétlen
baj"*. Igaza van, és van rá elvi szabály: **ha a létezés az adott hívó előtt már nem titok,
akkor nincs mit rejteni.**

### 3.5 A beállíthatóság — egyetlen precedens van, de pontos

A hét megvizsgált nagy rendszer közül **egyik sem** ad ilyen kapcsolót. A **Discourse** viszont
igen, és pontosan abban a formában, amit a tulajdonos kért: `detailed_404`, logikai érték,
biztonsági csoportban, **alapértelmezésben kikapcsolva** (elrejt), a saját leírásával:

> „Provides more details to users about why they can't access a particular topic. **Note: This
> is less secure** because users will know if a URL links to a valid topic."

**Ez a minta:** kapcsolható, elrejtő alapértékkel, és a beállítás mellett kiírva, mit cserélünk.

**Amit ki kell mondani:** ez egyetlen precedens. Nem rossz ötlet — de nincs mögötte iparági
tömeg, és ezt a döntésben jelölni kell.

### 3.6 Egy dolog, ami félreérthető

A MCP specifikáció előír 403-at „elégtelen jogosultságra" — **de csak az OAuth-hatókör
szintjén**. A rekord-szintű üzleti jogosultsággal nem foglalkozik, tehát **nem válaszolja meg
előre** ezt a kérdést. Könnyű összekeverni a kettőt.

---

## 4. A távoli hitelesítés — a követelmények, amiket eddig nem írtunk le

A MUST-szintű minimum, ha egy telepítés hitelesítést valósít meg:

1. OAuth 2.1 **erőforrás-szerver** szerep — a hitelesítési szerver külön, opcionális szerep.
2. **Védett erőforrás metaadat** (RFC 9728), legalább az egyik módon kiajánlva.
3. `401` és `WWW-Authenticate: Bearer` minden érvényes token nélküli kérésre.
4. Helyes státuszkódok: 401 / 403 / 400.
5. **Minden token validálása**: lejárat, erőforrás, hatókör.
6. **Közönség-kötés**: csak az ennek a szervernek kiállított tokent fogadjuk el.
7. **Token-átjátszás tilos** felfelé; ha nekünk kell hívni, külön tokent kérünk.
8. **RFC 8707 `resource` paraméter**.
9. **HTTPS** mindenhol.

**És egy elavulás, amibe könnyű beleszaladni:** a **dinamikus kliens-regisztráció (DCR)
elavult** a `2026-07-28`-ban — SHOULD-ról MAY-re esett, 2027-07-28 után eltávolítható.
Helyette **CIMD** (Client ID Metadata Documents) az ajánlott. Ez új a korábbi változathoz
képest, amiben CIMD még nem is létezett — és a legtöbb létező leírás még a DCR-t írja le.

---

## 5. Amit ez a kör megváltoztat

| Hol | Mi volt | Mi lesz |
|---|---|---|
| D-35/7 | üres eredmény jogosultság-hiánynál | egységes elutasítás `isError`-ral + eseményazonosító; fokozatosan nyílt, ha a hívó már látja |
| D-35/7 | nyitva hagyva | **beállítható**, elrejtő alapértékkel, a Discourse mintájára |
| D-35/3 | csak a minta | a teljes MUST-lista + a DCR elavulása és a CIMD |
| D-13 | „se találat, se szám, se jelzés" | ez a **keresésre** áll; a **nevesített** hozzáférés egységes elutasítást kap (új 4. pont) |
| Spec 40 | — | mindhárom átvezetve |

**Számot ez a kampány nem ad a mérési dokumentumba** — előírásokról és dokumentált
gyakorlatról szól.
