# Önellenőrzés — `mcp-felulet` kampány

Lezárva: 2026-09-12. Ez a fájl azt írja le, **hol tévedtünk és mit nem tudtunk megerősíteni.**

---

## A kutatási terv kiindulópontja elavult volt

A terv a `2025-06-18`-as specifikációt feltételezte érvényesnek. **A ma érvényes stabil változat
a `2026-07-28`**, és ez nem finomhangolás: megszűnt az `initialize` kézfogás, megszűnt a
munkamenet-fogalom és az `Mcp-Session-Id`, minden kérés magában hordozza a verziót és a
képességeket, új a `resultType` mező és a több körös kérés.

Két kereső ügynök egymástól függetlenül állapította ezt meg és korrigálta a tervet. **Ez a
kampány egyik legfontosabb eredménye** — az elavult kiindulópontból írt specifikáció rossz
protokollra épült volna.

**Következmény, amit a döntésbe is beírtunk:** a kiadás nagyjából hat hetes, és a kutatás
szerint a legtöbb létező cikk és SDK-dokumentáció még a régi, munkamenet-alapú modellt írja le.
A tulajdonos tudatosan választotta a legújabbat, ennek a kockázatnak a vállalásával.

---

## Amit nem sikerült megerősíteni

1. **A leírás-mező hosszkorlátja.** A specifikációban nem találtunk számszerű korlátot az
   eszközleírásra. Ez „evidence of absence", nem megállapítás.
2. **Válaszméret-korlát a specifikációban nincs** — sem korlát, sem eljárás arra, mit tegyen a
   szerver, ha a válasz túl nagy. A 25 000 tokenes vágás a Claude Code alapértelmezése, nem
   protokoll-szabály.
3. **Nincs mért adat arra, hogyan hat a hibaüzenet megfogalmazása a helyreállásra**, és arra
   sem, mi visz egy modellt végtelen ciklusba. A „kettő-három javítási kísérlet" dokumentált
   viselkedés, nem mérés. **Ez érdemi hiány**, mert a felület hibaüzeneteit erre alapoznánk.
4. **A Client Credentials grant pontos jelenlegi státusza tisztázatlan** a `2026-07-28`
   specifikációban. Egy másodlagos forrás szerint „eltűnt, majd visszatérőben van" — ezt nem
   sikerült a friss spec-szövegből megerősíteni.
5. **A stdio ág `_meta` mezőjében említett „optional client identity" jelentése nyitott.**
   Nálunk ez kevésbé súlyos, mert a stdio ág kikerült — de ha valaha visszakerül, ezt tisztázni
   kell.
6. **Az eszközszám-küszöbökre két gyártó két számot mond**: az Anthropic 30–50 fölött jelez
   romlást, az OpenAI „20 alatt" ajánl. Más módszertan, más termék — nem feloldható a
   forrásokból.
7. **Az OpenMemory megszűnésének indoka** nem derült ki, csak a README „sunsetting"
   figyelmeztetése. És **a mem0 Claude Code bővítménye kilenc eszközt cserélt le egyetlen
   olvasóra, indoklás nélkül** — erős precedens, de meg nem magyarázott.
8. **Csak két valós, sokfelhasználós implementációt** vizsgáltunk mélyen az azonosításnál
   (GitHub, Anthropic). A „bevett minta" általánosíthatósága ezért közepes, nem magas
   megbízhatóságú.
9. **A Letta adatai közösségi audit forráskód-hivatkozásain alapulnak**, nem közvetlenül látott
   forráskódon — két lekérés 404-et adott.

---

## Módszertani megjegyzés

Az SQ-03-nál minden GitHub hibajegy- és vitafonal-lekérés **tömörített, nem bájt szerinti**
olvasat volt. Ez nem ugyanaz a hiba, mint az `adatbazis-illeszto` kampányban tapasztalt
AI-átfogalmazás, de az idézetek pontossága emiatt gyengébb, és ez minden érintett helyen
jelezve van.

**Ebben a kampányban az AI-összefoglaló-probléma nem volt jelentős** — az anyag túlnyomó része
hivatalos specifikációból és forráskódból származik, ami a korábbi körökhöz képest javulás.

---

## Ellentmondások, amiket nem oldottunk fel

- **Eszközszám-küszöb**: Anthropic 30–50, OpenAI 20 alatt. Nálunk nem szorító, mert hat-hét
  eszközről van szó.
- **Eszköz-darabolás**: mindkét gyártó a kevesebb, nagyobb eszközt ajánlja — a tulajdonos
  viszont a szándékonkénti külön eszközt választotta, azzal az indokkal, hogy a kötelező
  paraméterkészletek műveletenként eltérnek, és ezt egy közös sémában nehéz tisztán kifejezni.
  **Ez tudatos eltérés a gyártói ajánlástól**, és a döntésben ki van írva.
- **A mem0 dokumentációja és viselkedése elvált** egymástól az ellentmondás-feloldásban.

---

## Amit a kutatás megerősített, és ami a döntés gerince lett

- **A hibamodell kettéválasztása**, a `schema.ts` saját szövegével: az eszköz-hibák az
  eredménybe mennek, `isError: true`-val, nem protokoll-hibaként — különben a modell nem látja
  és nem tud javítani.
- **A stdio ág önmagától elhárítja az azonosítást**: „Implementations using an STDIO transport
  SHOULD NOT follow this specification, and instead retrieve credentials from the environment."
  Ez döntötte el, hogy a stdio ág kikerül.
- **Az agent a felhasználó jogaival fut**, nem szolgáltatás-fiókként — az Anthropic saját
  dokumentációja szerint minden kapcsolat felhasználói hozzájárulást igényel. Ez a D-11
  alapfeltevése, és most már iparági minta, nem feltevés.
- **A konkurens írás fájlkorrupciót okozott** a hivatalos memória-szerverben, és a javítás
  pontosan az, amit a D-07 előír. A mi döntésünk tehát nem túlbiztosítás volt.
- **Az annotációk nem védenek**: a spec kétszer mondja ki, hogy nem megbízható szervertől nem
  szabad rájuk biztonsági döntést alapozni.
