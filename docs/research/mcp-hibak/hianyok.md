# Hiányok — amire nem találtunk választ

Kampány: `mcp-hibak` · 2026-09-12


---

## SQ-01 — A hibamodell adverzariális ellenőrzése

# SQ-01 — Rések, amiket nem sikerült teljesen lezárni

## 1. Éles, valós agent-kliensek forráskódja (5. ellenőrzési pont)

Nem volt hozzáférésem a legelterjedtebb, valóban LLM-et vezérlő MCP-kliensek zárt vagy
nehezen elérhető forráskódjához (Claude Desktop, Cursor, Cline, Claude Code maga, Windsurf
stb.), hogy közvetlenül lássam: a kapott JSON-RPC protokollhibát *ténylegesen* betolják-e
a modell kontextusába, vagy csak a felhasználói felületen jelenítik meg (ami NEM
egyenértékű azzal, hogy a modell "látja"). Amit találtam:

- **Strukturális bizonyíték** (T1, Python SDK): a kliens API-szinten a protokollhiba
  kivételként landol a hívó kódban, a tool-végrehajtási hiba pedig rendes visszatérési
  értékként — ez *lehetővé teszi*, hogy egy host figyelmen kívül hagyja vagy csak a
  felhasználónak mutassa a kivételt anélkül, hogy a modellnek átadná, de nem bizonyítja,
  hogy ez ténylegesen meg is történik bármelyik konkrét termékben.
- **Egyetlen, gyenge (T3) anekdota** (`modelcontextprotocol/servers#3122`), ami
  klienskénti eltérő viselkedést jelez, de karbantartói megerősítés vagy technikai
  magyarázat nélkül — nem tudni, hogy ez a MAY/SHOULD-mechanizmushoz kapcsolódik-e, vagy
  egy más okú (pl. session-kezelési) jelenség.

**Javaslat, ha ez a rés kritikus a döntéshez**: egy következő kutatási körben érdemes
konkrétan az Anthropic saját Claude Agent SDK-jának (`@anthropic-ai/claude-agent-sdk` /
`claude-agent-sdk` Python csomag) vagy a nyílt forráskódú MCP-kliens implementációknak
(pl. `mcp-cli`, a hivatalos `everything` teszt-kliens, vagy a Cline nyílt forráskódú
VS Code-kiterjesztés) a tényleges hiba-az-üzenetbe-fordítási logikáját megnézni.

## 2. LangChain MCP adapters forráskódja nem lett feldolgozva

A `langchain-mcp-adapters` csomag `tools.py` fájljának feltételezett elérési útja
(`libs/langchain-mcp-adapters/langchain_mcp_adapters/tools.py`) 404-et adott, és a
`jsdelivr` csomag-lista lekérdezés erre a repóra hibát dobott (`KeyError: 'versions'` —
valószínűleg más JSON-választ adott, mint a másik két repóra). Nem derítettem ki a
pontos okot vagy a helyes fájlnevet — időkorlát miatt nem folytattam. Ez egy közepesen
népszerű, valós agent-keretrendszer, ami közvetlen bizonyítékot adhatna arra, hogyan
kezeli egy tényleges, széles körben használt LLM-agent-réteg az `isError` mezőt és a
kivételeket.

## 3. `github.com`, `api.github.com`, `codeload.github.com` repó-szintű kapuzása

Ebben a szekcióban ezek a domainek "GitHub access to this repository is not enabled for
this session" hibát adtak (az `add_repo` eszköz nem volt elérhető az eszközkészletemben).
Ez nem tartalmi hozzáférés-megtagadás volt, hanem munkakörnyezeti korlátozás — a
`raw.githubusercontent.com` végpont viszont minden esetben elérhető volt, így a
forráskódot végül sikerült megszerezni, csak nem a natív GitHub-böngészőn/API-n
keresztül, hanem a `data.jsdelivr.com` csomag-API-jával kombinálva. Ha egy jövőbeli
kutatási kör GitHub Issues/PR-diszkussziókat (nem nyers fájltartalmat) akar feldolgozni
T1/T2 szinten, ehhez vagy az `add_repo` eszközt kell elérhetővé tenni, vagy kizárólag
`WebFetch`-re kell hagyatkozni (ami viszont kis modell összefoglalóját adja — pontossági
kockázat, amit a feladat kifejezetten óvott).

## 4. A TypeScript SDK pontos, kiadott (nem `main` ág) verziójának ellenőrzése

A `packages/server/src/server/mcp.ts` és társai a `typescript-sdk` `main` ágáról lettek
letöltve, mert a jsdelivr által jelzett legfrissebb csomag-tag (`2.0.0-beta.1`) git-tagként
nem oldódott fel közvetlenül a `raw.githubusercontent.com`-on (404). Nagy valószínűséggel
a monorepo csomagonkénti tag-elnevezési konvenciója miatt (pl. `server@2.0.0-beta.1`), de
ezt nem derítettem ki pontosan. A `main` ág tartalma (a `wire/rev2026-07-28/` mappa
megléte alapján) megbízhatóan az aktuális, 2026-07-28-cal párhuzamos fejlesztési állapotot
tükrözi, de ez nem 100%-ban azonos egy ténylegesen kiadott, verziószámozott csomaggal —
ha egy jövőbeli kör ragaszkodik egy pontos, npm-re publikált verzióhoz, érdemes lenne az
`unpkg.com` vagy `npmjs.com` becsomagolt forrását ellenőrizni.

## 5. Nem vizsgáltam részletesen a többi hivatalos SDK-t (C#, Rust, Java, Go, Kotlin, PHP, Ruby, Swift)

A SEP-2164 szövege (Motivation-táblázat) felsorolja, hogy ezen SDK-k hogyan kezelték a
resource-not-found hibát a SEP előtt (pl. Kotlin `-32603` INTERNAL_ERROR-t használt,
ami kifejezetten helytelen kategorizálás volt) — ez arra utal, hogy a nem-TS/Python
SDK-k között is lehetnek hasonló, kisebb inkonzisztenciák a `tools/call`
hibakezelésében is, de ezt nem ellenőriztem forráskód-szinten mindegyikre, mert a
feladat kifejezetten a "TypeScript és Python SDK"-t nevezte meg vizsgálandóként.


---

## SQ-02 — Jogosultság-elutasításkor mit szabad elárulni

# SQ-02 — Feltárt hiányosságok (gaps)

## 1. Nincs T1 forrás, amely explicit alapértéket ajánlana a 403-vs-404 kérdésre
Ezt a `megallapitasok.md` 3. pontja részletesen kifejti — itt csak megismétlem hiányként:
sem az RFC 9110, sem az OWASP Top10, sem az OWASP ASVS (V4 és V7 is átvizsgálva), sem az OWASP
Authorization Cheat Sheet, sem a CWE-200/203/209/210 nem mondja ki explicit módon: "alapból
X-et válaszd". Ez nem keresési hiba — mindegyik forrás teljes szövegét átnéztem (a legtöbbet
nyersben is), és a hiány konzisztens.

## 2. Nincs egységesen elfogadott név a "nem található vagy nem hozzáférhető" mintára
A jelenség mögötti *sebezhetőségnek* van neve (CWE-203 Observable Discrepancy), de magának a
*védekező tervezési mintának* nem találtam kanonikus elnevezését sem biztonsági, sem API-design
szakirodalomban (OWASP, NCC Group API authorization cikke, OpenID AuthZEN patterns oldal — egyik
sem nevezi meg). Lehet, hogy létezik egy iparági zsargon-kifejezés, amit nem sikerült
megtalálnom a rendelkezésre álló keresési idővel — ez nyitott maradt.

## 3. Microsoft Graph — hiányos lefedettség
A `security-error-codes.md` (microsoftgraph/microsoft-graph-docs-contrib GitHub repó) és a
`learn.microsoft.com/en-us/graph/resolve-auth-errors` hivatalos oldalak lekérése **nem hozta
vissza** az `itemNotFound` és `accessDenied` hibakódok közvetlen, egymás melletti hivatalos
definícióját, sem bármilyen szöveget arról, hogy a kettő között van-e tudatos elrejtési
stratégia. Ez azt jelenti, hogy a Microsoft Graph sorát a mellékelt táblázatban ("külön
kezelve") **részleges bizonyosággal** állítom — lehet, hogy létezik egy pontosabb hivatalos
oldal, amit a rendelkezésre álló idő alatt nem találtam meg.

## 4. Atlassian Jira — nincs hivatalos dokumentációs forrás
A `"Issue does not exist or you do not have permission to see it."` sztring léte gyakorlatilag
biztos (sok független közösségi jelentés reprodukálja szó szerint), de **egyetlen hivatalos
Atlassian dokumentációs oldalt sem találtam**, amely ezt a viselkedést és annak indoklását
dokumentálná. Ez lehet azért, mert nincs ilyen hivatalos dokumentáció, vagy azért, mert a
keresés nem talált rá — nem lehet biztosan megkülönböztetni "nincs ilyen dokumentum" és
"nem találtam meg" között ebben az esetben.

## 5. AWS S3 403-vs-404 indoklás — csak közösségi forrásból
Az AWS hivatalos `troubleshoot-403-errors.html` oldala **nem tartalmazza** a konkrét
"s3:ListBucket hiányában 403-at ad 404 helyett, hogy ne áruljon el semmit" indoklást. Ezt a
mondatot csak egy AWS re:Post cikkből (nem "AWS OFFICIAL" jelölésű, tehát community-szintű)
sikerült megszerezni. A viselkedés ténye jól dokumentált több független forrásban
(blog.kdgregory.com, gmcgregor.ca — ezeket nem fetch-eltem részletesen, csak a keresési
találatokból azonosítottam őket konzisztensként), de egyetlen hivatalos AWS-oldalt sem
találtam, amely a *miért*-et kimondaná.

## 6. Kubernetes hivatalos példamondat a "forbidden" hibaformátumra
A `kubernetes.io/docs/reference/access-authn-authz/authorization/` hivatalos oldal nagy
navigációs boilerplate-et tartalmazott, és a WebFetch/curl+regex kombinációval sem sikerült
elérnem a tényleges "is forbidden: User X cannot Y" példamondatot ezen a konkrét oldalon — ez
végül egy kubernetes/kubernetes GitHub Issue-ból (#124406) került elő, ami hivatalos projekt
repó, de nem "dokumentáció" a szó szoros értelmében. Ha van egy tisztább hivatalos oldal
(pl. kubectl referencia vagy egy külön RBAC-troubleshooting oldal) a pontos formátumra, azt
nem sikerült ez alatt a kutatás alatt beazonosítani.

## 7. Docker/OCI Distribution API spec — nem szerepel részletesen a fő anyagban
A specifikáció (`distribution.github.io/distribution/spec/api/`) explicit **nem** ad
iránymutatást arról, hogy 401-et vagy 404-et kell-e adni magánrepóra jogosultsághiány esetén —
ezt a "gap"-et a `megallapitasok.md`-ben csak érintőlegesen említettem (a `links.md`
"kevés hozadékú fetch-ek" részében), mert a fő öt kérdés (GitHub, GitLab, Google, Jira, MS
Graph, AWS, K8s) között nem szerepelt explicit módon, de a kutatás során felmerült, és
tanulságos negatív adat: egy releváns iparági specifikáció **is** nyitva hagyja ezt a kérdést.

## 8. WebFetch-hallucináció-gyanús esetek, amiket kizártam
Több esetben a WebFetch kis modellje vagy csonkolt választ adott (a dokumentum "túl hosszú
volt"), vagy egy kitalált korlátozásra hivatkozva (pl. "125 karakteres idézési limit" az RFC
9110 esetén) tagadta meg a pontos idézést. Ezeket **nem fogadtam el készpénznek** — minden
ilyen esetben közvetlen `curl`-letöltésre váltottam és magam kerestem a nyers szövegben. Az
összes kulcsidézet (RFC 9110, GitHub docs, GitLab docs, Google Drive docs, Discourse settings,
OWASP Top10/ASVS) ily módon nyers forrásból, nem AI-összefoglalóból lett ellenőrizve — ezek
tehát megbízhatók. Ahol ez NEM sikerült (Microsoft Graph, Kubernetes pontos példamondat, AWS
S3 indoklás), azt fent, külön pontokban jelöltem hiányként, nem állítottam be idézetként.

## 9. Nem vizsgáltam kifejezetten a hívó típusa szerinti (human vs machine) szabványt
A 8. pontra nem találtam olyan T1/T2 forrást, amely kifejezetten normatív módon foglalkozna
azzal, hogy gépi/ügynök hívónál más válasz szükséges, mint emberi hívónál. Ez lehet azért, mert
a téma túl új (LLM-ügynökök API-hívása még formálódó terület), és a szabványosítás még nem
érte utol a gyakorlatot — de nem zárható ki, hogy van releváns akadémiai vagy iparági anyag
(pl. egy frissebb OWASP "LLM Top 10" vagy "Agentic AI" iránymutatás), amit ez a kör nem
fedezett fel kifejezetten erre a szűk kérdésre optimalizálva.


---

## SQ-03 — Mit kell megvalósítania egy szabványos MCP erőforrás-szervernek

# SQ-03 — Hiányosságok / nyitott pontok

## 1. "aud/iss/exp/aláírás/scope" négyes-ötös lista nem szerepel tételesen a spec-ben

A kutatási kérdés (5. pont) feltételezte, hogy a spec egy konkrét, felsorolt listát ad a
token-validációhoz (`aud`, `iss`, `exp`, aláírás, scope). A ténylegesen fellelt szöveg
(OAuth 2.1 draft-13 5.2 szakasza, amit az MCP spec hivatkozással átvesz) ezt **nem
listaszerűen** mondja ki:

> "the resource server MUST check that the access token is not yet expired, is authorized to
> access the requested resource, was issued with the appropriate scope, and meets other
> policy requirements"

Ebből explicit: **exp** ("not yet expired"), **jogosultság az erőforráshoz** (ami az MCP
kontextusban az **aud**-ellenőrzésként jelenik meg, külön MCP-specifikus mondatban), és
**scope**. Az **iss** (kibocsátó) ellenőrzése a *tokenre* nézve nincs külön kimondva —
csak az *authorization response* `iss` paraméterére (RFC 9207), ami más réteg. Az
**aláírás-ellenőrzés** a spec szerint attól függ, hogy a szerver "reference token" (AS
introspection) vagy "self-encoded" (pl. JWT) tokent fogad-e el — ha JWT-t, az aláírás-
ellenőrzés szükségszerű, de ezt a specifikáció nem mondja ki külön MUST-ként, mert
formátum-agnosztikus akar maradni.

**Nyitott kérdés a döntéshozó felé**: ha a rendszer saját tokenformátumot választ (pl. JWT),
az `iss` és aláírás-ellenőrzést **implementációs döntésként**, nem spec-idézetként kell
előírni a D-35/D-11 dokumentumokban — ez nem hiányosság a kutatásban, hanem a spec valódi
nyitottsága, amit a szintézisnek jeleznie kell.

## 2. Nincs explicit "ha a PRM teljesen hiányzik" hibaág a szerver oldalán

L. `megallapitasok.md` Q2.3 — a kliens oldali "abort or use pre-configured values" csak egy
mermaid-diagram jegyzetében szerepel, nem a folyószöveg normatív részében. Nem találtam
olyan mondatot, ami azt mondaná ki, hogy egy PRM nélküli szerver *milyen konkrét hiba-
válasszal* kell hogy találkozzon — a spec egyszerűen "nem konformnak" tekinti az ilyen
szervert, explicit hibakezelési előírás nélkül erre a konkrét esetre.

## 3. CIMD alap-draft (draft-ietf-oauth-client-id-metadata-document-00) nem lett nyersen ellenőrizve

A CIMD-re vonatkozó MUST/SHOULD-listát (l. Q8.5) az MCP spec `client-registration.md`
oldaláról idéztem, amely maga hivatkozik a CIMD IETF draft 6. szakaszára (SSRF, biztonsági
megfontolások). Magát a CIMD draftot nem töltöttem le és nem ellenőriztem nyersen — ha a
szintézis szigorúan a CIMD draft *saját* normatív szövegét is idézni akarja (nem csak az
MCP spec róla szóló összefoglalóját), az egy külön lekérést igényelne
(`https://datatracker.ietf.org/doc/html/draft-ietf-oauth-client-id-metadata-document-00`).
Ez nem ellentmond semminek, csak a forrásmélység egy rétege, amit nem jártam be.

## 4. A `docs/2026-07-28/tutorials/security/authorization.md` tutorial-oldal nem lett részletesen idézve

Ez az 1161 soros oldal létezik és elérhető volt, de csak egy `Grep`-pel futottam át rajta
(a "co-locate"/"same entity" kérdés ellenőrzésére a Q1-hez), tartalmilag nem dolgoztam fel
mélyen. Lehet benne további, a fő spec-oldalakon nem szereplő magyarázó anyag — de mivel ez
egy *tutorial*, nem a normatív *specification* ág, a hiányosság kockázata alacsony (a
normatív MUST/SHOULD szövegek a `specification/2026-07-28/...` oldalakon vannak, amiket
teljeskörűen feldolgoztam).

## 5. Nincs SDK-forráskód-ellenőrzés

A feladat T1 definíciója tartalmazza az "SDK forráskód"-ot is, de ebben a körben kizárólag
a specifikáció-szöveget és az RFC-ket dolgoztam fel, egyetlen hivatalos MCP SDK (TypeScript,
Python stb.) forráskódját sem néztem meg annak ellenőrzésére, hogy a fenti MUST-
kötelezettségeket ténylegesen hogyan implementálják (pl. hogyan validál egy tokent a
hivatalos Python SDK). Ha a szintézisnek szüksége van "hogyan implementálják a
gyakorlatban" típusú megerősítésre, az egy külön, SDK-forráskód-fókuszú kutatási kört
igényelne.
