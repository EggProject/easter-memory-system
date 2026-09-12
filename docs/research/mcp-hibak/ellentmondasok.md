# Ellentmondások — ahol a források nem egyeznek

Kampány: `mcp-hibak` · 2026-09-12


---

## SQ-01 — A hibamodell adverzariális ellenőrzése

# SQ-01 — Ellentmondások

## 1. TypeScript SDK vs. Python SDK: "ismeretlen eszköznév" kategorizálása

**Nem a fő állítást érintő, de valós ellentmondás a két hivatalos SDK között.**

- **Specifikáció** (`server/tools.mdx`, mindegyik vizsgált verzióban 2024-11-05-től):
  "Unknown tool(s)" a **Protocol Errors** listában szerepel.
- **TypeScript SDK** (`packages/server/src/server/mcp.ts`, `tools/call` handler):
  az "ismeretlen tool" ellenőrzés a `try`-blokkon *kívül* van, és explicit
  `throw new ProtocolError(ProtocolErrorCode.InvalidParams, ...)`-t dob — ez ténylegesen
  JSON-RPC hibaként hagyja el a szervert. **Összhangban van a specifikációval.**
- **Python SDK** (`src/mcp/server/mcpserver/tools/tool_manager.py` +
  `src/mcp/server/mcpserver/server.py`): a `ToolManager.call_tool` egy ismeretlen névre
  `ToolError`-t dob (nem `MCPError`-t), amit a `_handle_call_tool` generikus
  `except Exception` ága elkap, és `CallToolResult(is_error=True)`-vá alakít.
  **Ellentmond a specifikáció explicit "Unknown tool = Protocol Error" besorolásának,
  és ellentmond a TypeScript SDK viselkedésének is.**

**Feloldás/értékelés**: ez egy szűk, névhez köthető inkonzisztencia, ami NEM érinti a
kutatás fő tárgyát (üzleti/validációs hibák kezelése) — abban mindkét SDK egyetért, és
egyezik a specifikációval. Nem "megdöntő" bizonyíték, de dokumentálandó pontatlanság a
Python SDK-ban a specifikációhoz képest. Nincs jele annak, hogy ez szándékos tervezési
döntés lenne (a hivatalos "Handling errors" doksi-oldal nem tér ki külön az "ismeretlen
tool" esetre, csak a "tool talált, de hibázik" esetekre).

## 2. A séma-kommentár (`schema.ts`) és a spec-próza (`tools.mdx`) kulcsszó-ereje között

A `CallToolResult.isError` doksikommentje a protokollhiba-irányban **kisbetűs** "should"-ot
használ ("...or any other exceptional conditions, **should** be reported as an MCP error
response"), míg a tool-hiba irányban nagybetűs "SHOULD"-ot. A `tools.mdx` spec-oldal
viszont **mindkét** irányban explicit, nagybetűs RFC 2119 kulcsszót használ (`**MAY**` a
protokollhiba, `**SHOULD**` a tool-hiba oldalán). Ez nem tartalmi ellentmondás — mindkét
szöveg ugyanazt az irányt támogatja —, csak egy formai következetlenség a séma
dokumentációja és a fő spec-szöveg normatív-erőssége között. A `tools.mdx` a mérvadó,
mert az a specifikáció fő, normatív szövegteste; a séma csak kísérő magyarázat.

## 3. Nincs talált tartalmi ellentmondás a fő állítással szemben

Az adverzariális ellenőrzés célja a megdöntés volt. **Nem találtam olyan T1 vagy T2
forrást, ami azt állítaná, hogy egy `tools/call`-on belüli üzleti/validációs hibát
JSON-RPC protokollhibaként *kellene* vagy *szabadna* visszaadni.** Az egyetlen talált
"üzleti hiba mint protokollhiba" eset (resource-not-found, SEP-2164) egy másik RPC-
metódusra (`resources/read`) vonatkozik, és strukturális okból (nincs `isError`-mező
ott), nem azért, mert a tervezési filozófia megengedné ugyanezt a `tools/call`-nál is.
Ez tehát hatókör-pontosítás, nem cáfolat.


---

## SQ-02 — Jogosultság-elutasításkor mit szabad elárulni

# SQ-02 — Ellentmondások és feszültségek a forrásaim között

## 1. Az RFC 9110 belső feszültsége: mi a "normál" válasz?
Az RFC 9110 egyszerre mondja, hogy:
- a 403 "indicates that the server understood the request but refuses to fulfill it" — ez
  hangzik az alapesetnek,
- de a 404 leírása is tartalmazza, hogy az "is not willing to disclose that one exists" —
  vagyis a 404 *önmagában, saját jogán* is jelentheti a szándékos elrejtést, nem csak a 403
  szakaszból átirányított kivételes esetként.

Ez nem logikai ellentmondás (a két szakasz konzisztens: a 403 a "hivatalos" jelzés, a 404 az
"opcionális rejtő" jelzés), de **gyakorlati kétértelműséget** hagy: az RFC nem mondja meg,
*mikor* indokolt élni a rejtő opcióval és mikor nem — ezt teljesen a szerver tervezőjére bízza.

## 2. GitHub vs. Kubernetes — homlokegyenest ellentétes filozófia, mindkettő "jó gyakorlatként" hivatkozva
A kutatás során mindkét irányra találtam hivatkozási alapot:
- **GitHub**: mindig rejt (404), és ezt kifejezetten *biztonsági jó gyakorlatként* mutatja be.
- **Kubernetes**: alapból *nem* rejt (403, a kért erőforrás nevesítésével), és egy 2024-es
  biztonsági jegy éppen azt kifogásolta, amikor a rendszer *túl sokat* (RBAC-belső
  konfigurációt) árult el — vagyis Kubernetesnél a probléma nem az volt, hogy nem rejt eleget,
  hanem hogy egy nem szándékolt csatornán (RBAC hibaszöveg) több szivárgott ki, mint amit a
  tervezők akartak.

**Nincs egy univerzálisan "helyes" válasz** — a két rendszer eltérő fenyegetési modellel
dolgozik: a GitHubnál a *repó létezése* önmagában érzékeny adat (pl. "cégük dolgozik egy még
be nem jelentett projekten" következtethető ki belőle), míg a Kubernetes API-nál a *kért
erőforrás neve* általában amúgy is ismert a hívó számára (mert ő maga adta meg a kérésben) —
tehát a "mit árulunk el" kérdés nem ugyanaz a két esetben. Ez fontos árnyalat: **a döntés
kontextusfüggő**, nem lehet egyetlen szabályt levezetni a megfigyelt gyakorlatokból.

## 3. Google Drive — belső following ellentmondás nélküli, de rétegzett viselkedés
Nem ellentmondás, de érdemes kiemelni: a Google Drive ugyanazon rendszeren belül **mindkét**
stratégiát alkalmazza, attól függően, hogy a hívó "már látott-e valamit": olvasási jog
hiányában rejt (404 `notFound`), írási jog hiányában (ha a fájl már ismert/olvasható) felfed
(403 `insufficientFilePermissions`). Ez nem a többi rendszerrel ellentmondó, hanem egy
harmadik, "fokozatos" modellt mutat be, amit sem a "mindig rejts" (GitHub), sem a "sose rejts"
(Kubernetes) tábor nem képvisel tisztán.

## 4. A biztonsági érvelés (CWE-203) és a használhatósági ellenérv (dev.to cikkek) nem
ütköznek közvetlenül, de különböző szinten mozognak
A CWE-203 Observable Discrepancy azt mondja: ha a válasz különbözik, az kiszivárogtatja a
létezést, ami *sebezhetőség*. A dev.to cikkek (7-8. pont) azt mondják: ha a válasz *nem*
különbözik (egyesített, rejtő válasz), az *használhatósági és hibakeresési* problémát okoz.
Ez a két állítás **nem zárja ki egymást** — mindkettő igaz lehet egyszerre, és pontosan ez a
tervezési feszültség, amit a tulajdonos eredeti kérdése (kell egy beállítható, alap
ajánlással ellátott mechanizmus) megpróbál feloldani. Fontos módszertani észrevétel: a
biztonsági oldal érvelését **szabvány (CWE) képviseli**, a használhatósági oldal érvelését
**csak gyakorlati blogok (T3)** — ez aszimmetria a bizonyíték minőségében, nem az érvelés
erejében.

## 5. Az MCP-spec (2026-07-28) hibatáblázata és a mi konkrét kérdésünk nem ugyanarról szól
Első ránézésre úgy tűnhet, hogy az MCP-spec "403 = insufficient permissions" előírása
közvetlenül megválaszolja a kérdésünket. **Ez félrevezető lenne** — a spec ezen szakasza az
OAuth-token/scope-validáció hibáiról szól (pl. a tokennek nincs `files:read` hatóköre), nem
arról, hogy egy *érvényes, megfelelő hatókörű* token birtokosa hozzáférhet-e egy *konkrét
rekordhoz* (a mi esetünkben: egy adott projekthez tartozó memória-dokumentumhoz). A kettőt
összekeverni módszertani hiba lenne — erre külön figyelmeztetek a `megallapitasok.md` 8.
pontjában és itt is, mert könnyen félreérthető "kész válaszként".

## 6. GitLab hivatalos dokumentációja vs. GitLab saját issue-trackere
A GitLab hivatalos dokumentációja (`docs.gitlab.com/api/rest/troubleshooting/`) semleges,
tényszerű hangnemben írja le a 404 egyesített jelentését, mintha ez lenne a természetes és
elfogadott állapot. Eközben a GitLab saját issue-trackerén **több éve nyitott jegyek**
kérdőjelezik meg pontosan ezt a döntést (pl. #65271, #20878), anélkül hogy a csapat hivatalos
választ adott volna bármelyikre (a fetch-elt tartalom szerint). Ez azt jelzi: a hivatalos
dokumentáció és a fejlesztői/felhasználói elégedettség **nincs szinkronban** — a dokumentált
viselkedés nem feltétlenül jelenti azt, hogy a viselkedés konszenzusos vagy vitán felüli
a gyakorlatban.


---

## SQ-03 — Mit kell megvalósítania egy szabványos MCP erőforrás-szervernek

# SQ-03 — Ellentmondások / belső feszültségek

## 1. OAuth 2.1 draft-verziószám következetlenség a hivatalos oldalon (kisebb, valószínűleg
   redakciós hiba)

A `specification/2026-07-28/basic/authorization/security-considerations.md` oldal a
dokumentum nagy részében `draft-ietf-oauth-v2-1-13`-ra hivatkozik (pl. "Communication
Security", "Authorization Code Protection", "Mix-Up Attacks" szakaszok mind ezt idézik), de
a "Token Theft" szakasz egyik mondata `draft-ietf-oauth-v2-1-14`-re mutat:

> "For public clients, authorization servers **MUST** rotate refresh tokens as described in
> [OAuth 2.1 Section 4.3.1 \"Token Endpoint Extension\"]
> (https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-14#section-4.3.1)."

Ez tartalmilag valószínűleg nem szándékos ellentmondás, hanem egy link-frissítési
elmaradás a hivatalos oldalon (a `-13` a domináns hivatkozási alap mindenhol máshol) — de
mivel a feladat kifejezetten kéri az ilyen following inkonzisztenciák jelzését, itt
rögzítve van. **Nem befolyásolja a MUST-tartalom lényegét** (refresh token rotáció publikus
kliensekre), csak a hivatkozott draft-verzió számát.

## 2. RFC 9728 saját szintje (MAY) vs. MCP spec szintje (MUST-válogatás) — nem valódi
   ellentmondás, hanem tudatos szigorítás

Nem ellentmondás, de fontos árnyalat, amit könnyű összekeverni ellentmondással: az alap-RFC-k
(RFC 8707 "resource" paraméter, RFC 9728 WWW-Authenticate-en keresztüli kiajánlás) számos
helyen **MAY**/OPTIONAL szinten fogalmaznak, miközben az MCP spec ugyanazt a mechanizmust
**MUST**-ra szigorítja MCP-kontextusban. Ez konzisztens réteg-modell (az RFC az általános
OAuth-ökoszisztémára ír elő minimumot, az MCP profil szigorúbb saját magára nézve), nem
tartalmi ütközés. Részletezve `megallapitasok.md` Q2.2 és Q4.1–4.2 alatt.

## 3. A `docs/2026-07-28/tutorials/security/authorization.md` tutorial és a fő spec közti
   DCR-hangsúly eltérés (részlegesen ellenőrzött)

A gyors `Grep`-ellenőrzés során (l. `gaps.md` 4. pont) a tutorial-oldal egy mondata még
DCR-t említ elsődleges regisztrációs útként ("Alternatively, the client can use **Dynamic
Client Registration** (DCR) to dynamically register itself...") anélkül, hogy a CIMD-et
elsődlegesként emelné ki ott, ahol ez a mondat áll. Ez **potenciálisan elmaradó frissítés**
a tutorial-szövegben a normatív spec-oldalak (`client-registration.md`) CIMD-elsőbbségi
állásfoglalásához képest. Mivel ezt a tutorial-oldalt nem dolgoztam fel teljes mélységben
(l. `gaps.md` 4. pont), **nem állítom biztosan**, hogy ez tényleges, teljes ellentmondás —
lehet, hogy a mondat egy másik, korábbi kontextusban (pl. régebbi AS-ekkel való
kompatibilitás bemutatásakor) szerepel, ahol a DCR-alternatíva említése helyénvaló. Jelzem
mint **nyitott, nem lezárt megfigyelést**, nem mint megerősített ellentmondást.

## Amiben nincs ellentmondás (explicit ellenőrizve)

- A `specification/2026-07-28/basic/authorization.md` és a
  `.../security-considerations.md` és a `docs/.../security_best_practices.md` mind
  egymást erősítve, azonos tartalommal mondják ki a token passthrough tilalmát —
  háromszorosan konzisztens, nincs eltérés a MUST-szintek között.
- A DCR deprecation állítása (client-registration.md figyelmeztetése, a fő authorization.md
  Overview 3. pontja, és a deprecated.md registry-bejegyzése) mindhárom helyen egybehangzó:
  `2026-07-28`-tól deprecated, CIMD a migrációs cél, 2027-07-28 utáni revízióig legalább
  megmarad.
