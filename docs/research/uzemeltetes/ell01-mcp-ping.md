# ELL01 — Az MCP `ping` eltávolításának ellenőrzése

*Módszertani megjegyzés: ez az ellenőrzés egyetlen ügynök által, szekvenciális web-keresésekkel és nyers forrásfájl-lekérésekkel (curl/git) készült, a `deep-web-research` skill előírása szerint kötelezően meghívva — de a skill teljes, párhuzamos Sonnet-keresés + Opus-szintézis alügynök-pipeline-ja nélkül, mert ez a munkamenet nem fér hozzá alügynök-indító (`Agent`/`Task`) eszközhöz. Ez a skill saját szabálya szerint itt rögzítendő eltérés. A GitHub API-hozzáférés ebben a sandboxban korlátozott ("GitHub access to this repository is not enabled for this session") — ezért a repó tartalmát `raw.githubusercontent.com` közvetlen nyers-fájl-lekérésekkel és `git ls-remote --tags`-szel derítettem fel, API-listázás helyett.*

## Ítélet

**RÉSZBEN IGAZOLVA.**

Az állítás három külön, önállóan ellenőrizhető részből áll:

1. „A 2026-07-28 verzió TELJESEN ELTÁVOLÍTOTTA a `ping` kérést." → **IGAZOLVA.** A legújabb verzió (2026-07-28, ez a jelenlegi kiadott/„current" verzió) nyers `schema.ts` és `schema.json` fájljában **nulla találat** van a `ping`/`Ping` szavakra. A hivatalos changelog és az azt megvalósító SEP-2575 tervezési dokumentum kifejezetten és mindkét irányban (kliens→szerver, szerver→kliens) eltávolítottként dokumentálja.

2. „A protokollban SOHA nem volt health/heartbeat fogalom." → **CÁFOLVA.** Ez a rész ténybelileg hamis. A `ping` metódus 2024-11-05-től 2025-11-25-ig pontosan egy heartbeat/health-check mechanizmus volt — a séma saját szövege szerint arra szolgált, hogy „ellenőrizze, a másik fél még életben van-e" („to check that the other party is still alive"), a specifikáció szövege szerint pedig kifejezetten a „connection health" (kapcsolat-egészség) észlelésére. Egy külön, hivatalos, Final státuszú SEP (SEP-2260, 2026 februárja) szó szerint „keep-alive/health-check mechanizmusnak" és „MCP-szintű életjel-ellenőrzésnek" (liveness check) nevezi a ping-et.

3. „A jelenlegi verzióban ÉS NINCS most health/heartbeat fogalom." → **RÉSZBEN IGAZOLVA, pontosítással.** Protokoll-szintű (JSON-RPC metódusként megjelenő) health/liveness-ellenőrzés valóban nincs a 2026-07-28 verzióban — ez igaz. De az állítás megfogalmazása félrevezető, mert maga a hivatalos eltávolítási indoklás (SEP-2575) kifejezetten kimondja, hogy a „connection-health checks" (kapcsolat-egészség ellenőrzések) fogalma nem tűnt el, hanem a szállítási rétegbe (transport layer) költözött: „HTTP keep-alives, SSE comments, STDIO process status". Ennek nyoma a jelenlegi specifikációban ténylegesen megtalálható: a Streamable HTTP transport dokumentációja explicit `keep-alive` SSE-megjegyzéssort ír elő a `subscriptions/listen` hosszú életű streamhez, kifejezetten az inaktivitás miatti kapcsolat-bontás megelőzésére.

4. „A `server/discover` verzió- és képességegyeztetés, nem állapotellenőrzés." → **IGAZOLVA.** A `server/discover` RPC 2026-07-28-ban jelent meg elsőként (korábbi sémákban nulla találat), és kizárólag a szerver támogatott protokollverzióit, képességeit és azonosító adatait adja vissza — a hivatalos dokumentáció egyetlen szava sem köti health/liveness-ellenőrzéshez.

**Összefoglalva:** az állítás 1. és 3. (server/discover) tagmondata pontos; a „soha nem volt" tagmondat bizonyíthatóan hamis (a `ping` maga volt a heartbeat-mechanizmus, és a hivatalos dokumentáció ezt a szavaival is így nevezi); az „és most sincs" tagmondat a protokoll RPC-szintjén igaz, de a specifikáció szövege maga finomítja ezt azzal, hogy a health-check felelősséget explicit módon a szállítási rétegre hárítja, nem szünteti meg a fogalmat.

---

## Bizonyítékok

### 1. A legújabb kiadott verzió és a teljes verziótörténet

**Forrás:** `git ls-remote --tags` a `https://github.com/modelcontextprotocol/modelcontextprotocol.git` repóra (közvetlen git-protokoll lekérdezés, 2026-09-15).

Ténylegesen létező, a szerver által visszaadott tagek dátum szerinti sorrendben:

```
2024-10-07
2024-11-05
2024-11-05-final
2025-03-26
2025-06-18
2025-11-25-RC
2025-11-25
2026-07-28-RC
2026-07-28
```

**Forrás:** `https://modelcontextprotocol.io/docs/2026-07-28/learn/versioning` (WebFetch, 2026-09-15)

> "The **current** protocol version is [**2026-07-28**](/specification/2026-07-28/)."

A hivatalosan dokumentált, egymásra épülő verziólánc — minden verzió saját changelog-oldala explicit megnevezi az „előző revíziót" — a következő (mindegyik nyers `changelog.mdx` fájlból idézve, `raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/specification/<verzió>/changelog.mdx`):

- **2025-03-26** changelog: „…since the previous revision, [2024-11-05](/specification/2024-11-05)."
- **2025-06-18** changelog: „…since the previous revision, [2025-03-26](/specification/2025-03-26)."
- **2025-11-25** changelog: „…since the previous revision, [2025-06-18](/specification/2025-06-18)."
- **2026-07-28** changelog: „…since the previous revision, [2025-11-25](/specification/2025-11-25)."

Tehát a hivatalosan dokumentált specifikáció-verziólánc: **2024-11-05 → 2025-03-26 → 2025-06-18 → 2025-11-25 → 2026-07-28 (jelenlegi/„current")**. Ezt megelőzően release-candidate tagek is léteznek (`2025-11-25-RC`, `2026-07-28-RC`), valamint a `2026-07-28`-cal tartalmilag azonos `draft` ág (lásd lent, 3. pont).

A 2026-07-28-hoz vezető hivatalos blogbejegyzés-lánc (**Forrás:** `https://blog.modelcontextprotocol.io/tags/release/`, WebFetch):

- „The 2026-07-28 MCP Specification Release Candidate" — release candidate bejegyzés
- „Beta SDKs for the 2026-07-28 MCP Spec Release Candidate Are Here"
- „The 2026-07-28 Specification" — a végleges kiadás bejelentése, **2026. július 28.**

Ez megerősíti, hogy 2026-07-28 valódi, végleges kiadás, nem csak release candidate.

**A `2024-10-07` tag helyzete tisztázatlan / nem hivatalos specifikáció-verzió.** Ellenőriztem, hogy létezik-e hozzá séma vagy dokumentáció a jelenlegi repó-struktúrában:
- `https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/2024-10-07/schema.ts` → HTTP 404
- `https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/specification/2024-10-07/changelog.mdx` → HTTP 404

Mivel ehhez a taghez nem tartozik sem séma, sem specifikáció-dokumentum a jelenlegi könyvtárstruktúrában, és a hivatalos verziólánc (fent) `2024-11-05`-nél kezdődik, ezt a taget **nem tekintem hivatalosan számozott specifikáció-verziónak** — feltehetően egy korai, a mostani dokumentációs rendszer előtti commit-jelölés. Ezt nem tudtam megnyugtatóan tisztázni (lásd „Amit nem sikerült ellenőrizni").

### 2. Létezett-e valaha `ping` a specifikációban — igen, négy egymást követő verzióban

**Forrás (nyers séma, mind `raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/<verzió>/schema.ts`):**

| Verzió | `PingRequest` jelen van? | Idézet a nyers `schema.ts`-ből |
|---|---|---|
| 2024-11-05 | igen (258–263. sor) | „A ping, issued by either the server or the client, to check that the other party is still alive. The receiver must promptly respond, or else may be disconnected." |
| 2025-03-26 | igen (282–287. sor) | ugyanaz a szöveg |
| 2025-06-18 | igen (335–342. sor, `@category \`ping\`` címkével) | ugyanaz a szöveg |
| 2025-11-25 | igen (570–577. sor, `@category \`ping\`` címkével) | ugyanaz a szöveg |
| **2026-07-28** | **NEM** | (lásd 3. pont — nulla találat) |

A négy korábbi verzió mindegyikében pontosan ez a `PingRequest` definíció szerepelt:

```ts
export interface PingRequest extends Request {   // ill. JSONRPCRequest 2025-11-25-ben
  method: "ping";
  params?: RequestParams;
}
```

**Mit csinált a `ping` — a normatív specifikáció-szöveg (nem csak a séma) szerint.**
**Forrás:** `https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/ping` (WebFetch, 2026-09-15) — ez az oldal a 2026-07-28-ban már nem létezik (lásd 3. pont), így ez az utolsó élő verziója.

> "The Model Context Protocol includes an optional ping mechanism that allows either party to verify that their counterpart is still responsive and the connection is alive."

> "1. The receiver **MUST** respond promptly with an empty response… 2. If no response is received within a reasonable timeout period, the sender **MAY**: Consider the connection stale / Terminate the connection / Attempt reconnection procedures"

> "Implementation Considerations — Implementations **SHOULD** periodically issue pings to **detect connection health**. The frequency of pings **SHOULD** be configurable."

Ez a szövegrész szó szerint a „connection health" kifejezést használja — vagyis a hivatalos specifikáció saját maga nevezte a `ping`-et egészség-ellenőrzésnek, amíg létezett.

**Egy második, független hivatalos forrás ugyanerre:** a **SEP-2260** („Require Server requests to be associated with a Client request", Final státusz, létrehozva 2026-02-16, szponzor: Caitie McCaffrey / MCP Transports Working Group).
**Forrás:** `https://modelcontextprotocol.io/seps/2260-Require-Server-requests-to-be-associated-with-Client-requests` (WebFetch, 2026-09-15)

> "**Ping** has a special status as it is primarily intended as a **keep-alive/health-check mechanism**."

> "`ping` is an MCP-level **liveness check** and **MAY** be sent by either party at any time on an established session/connection."

Ez a dokumentum egy **másik**, a SEP-2575-től független, szintén Final státuszú hivatalos MCP-döntés — vagyis nem egyetlen elszigetelt megfogalmazásról van szó, hanem a protokoll kormányzási folyamata következetesen „health-check"-nek / „liveness check"-nek nevezte a ping-et, egészen a végső eltávolításáig.

**Ez közvetlenül cáfolja az állítás „soha nem volt health/heartbeat fogalom" részét.**

### 3. A legújabb verzió NYERS sémája — valóban nulla találat a `ping`-re

**Pontos lekért nyers URL-ek és eredmény (curl, 2026-09-15):**

- `https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/2026-07-28/schema.ts` — HTTP 200, 3197 sor.
  `grep -ni "ping"` → **nulla találat** (grep exit code 1).
- `https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/2026-07-28/schema.json` — HTTP 200, 181 474 bájt.
  Case-insensitive `"ping"` és `Ping` keresés → **nulla találat** mindkettőre.
- `https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/draft/schema.ts` — HTTP 200, 3197 sor (tartalmilag azonos a 2026-07-28-cal, azaz a folyamatban lévő „draft" ág jelenleg sem tartalmazza vissza a ping-et). **Nulla találat.**

A `basic/utilities/ping` dokumentációs oldal sorsa a 2026-07-28 kiadásban:
- `https://modelcontextprotocol.io/specification/2026-07-28/basic/utilities/ping` → HTTP **308** átirányítás, cél: `location: /specification/2026-07-28/changelog` (tehát a site maga a changelogra tereli az olvasót, ahol a törlés dokumentálva van).
- `https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/specification/2026-07-28/basic/utilities/ping.mdx` → HTTP **404** (a doksi-fájl fizikailag nem létezik ebben a verzióban).

**A teljes 2026-07-28 normatív specifikáció-szöveg átvizsgálása** (31 specifikációs oldal, a `https://modelcontextprotocol.io/llms-full.txt` hivatalos, teljes-szöveges exportján keresztül, curl, 2026-09-15): a `ping` szó a 31 oldal közül **kizárólag** a `changelog` oldalon fordul elő — pontosan azon a helyen, ahol az eltávolítást bejelentik. Az `index`, `schema`, `server/discover`, `basic/*`, `client/*`, `server/*` oldalak egyikén sem szerepel.

### 4. Hivatalos indoklás az eltávolításra

**Forrás:** `https://modelcontextprotocol.io/specification/2026-07-28/changelog` (WebFetch, 2026-09-15), „Major changes" 5. pont:

> "5. Remove `ping`, `logging/setLevel`, and `notifications/roots/list_changed`. Log level is now set per-request via `io.modelcontextprotocol/logLevel` in `_meta`; servers MUST NOT emit `notifications/message` for requests that did not include this field ([SEP-2575](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2575))."

A hivatkozott tervezési dokumentum, a **SEP-2575 „Make MCP Stateless"** (Final státusz, PR #2575, szerzők: Jonathan Hefner, Mark Roth, Shaun Smith, Harvey Tuch, Kurtis Van Gent).
**Forrás:** `https://modelcontextprotocol.io/seps/2575-stateless-mcp` (WebFetch) és a nyers `https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/seps/2575-stateless-mcp.md` (curl, 569–572. sor) — a két forrás szó szerint megegyezik:

> "`ping`: Removed in **both directions**. Server-to-client ping is removed because servers can no longer independently send requests. Client-to-server ping is also removed because any normal RPC call already proves server liveness, and transport-layer mechanisms (HTTP keep-alives, SSE comments, STDIO process status) handle **connection-health checks** more appropriately."

Ez a mondat maga is bizonyítja az „Ítélet" 3. pontjában leírt finomítást: az indoklás explicit megnevezi és elismeri a „connection-health checks" fogalmát — csak azt állítja, hogy ezt jobban kezelik a szállítási réteg mechanizmusai, nem hogy a fogalom megszűnt vagy soha nem is létezett volna.

**Az eltávolítás jogi/eljárási útja:** a `ping` **nem** a specifikáció formális elévülési (deprecation) folyamatán ment át — az eltávolítás egy nagyobb, kompatibilitást megtörő újratervezés (a stateless-átállás) része volt, direkt törléssel.
**Forrás:** `https://modelcontextprotocol.io/specification/2026-07-28/deprecated` (WebFetch) — a 2026-07-28-as „Deprecated features registry" táblázata **nem tartalmazza** a ping-et (a táblázatban Roots, Sampling, Logging, Dynamic Client Registration, `includeContext` értékek, HTTP+SSE transport szerepelnek), és a „Removed" szakasz szó szerint kimondja:

> "No features have been removed under this policy yet. When a Deprecated feature is removed, its row moves to this section with a link to the changelog entry recording the removal."

Ez azt jelenti, hogy a `ping` a formális elévülési szabályzat (SEP-2596, szintén 2026-07-28) hatálybalépése **előtt/azon kívül**, egy „major change"-ként, egy lépésben tűnt el — nem fokozatos deprecation→removal úton.

### 5. Van-e bármilyen más állapot-/életjel-fogalom a legújabb specifikációban?

Az alábbi kulcsszavakra kerestem rá (a) a nyers `schema.ts`/`schema.json` fájlban (2026-07-28) és (b) a teljes normatív specifikáció-szövegben (`llms-full.txt`, 31 db `/specification/2026-07-28/...` oldal, curl, 2026-09-15):

| Kulcsszó | Séma (schema.ts/json) | Specifikáció-szöveg (31 oldal) | Megjegyzés |
|---|---|---|---|
| `health` | nulla találat | nulla találat | Nincs `health`-koncepció a jelenlegi normatív szövegben. |
| `heartbeat` | nulla találat | nulla találat | Nincs. |
| `keepalive` / `keep-alive` | nulla találat a sémában | **1 találat**, a `basic/transports/streamable-http` oldalon | Lásd lent — nem RPC, csak SSE-konvenció. |
| `alive` | nulla találat | nulla találat (a `keep-alive` összetételen kívül) | A régi `PingRequest` „still alive" szövege eltűnt a sémából. |
| `status` | nulla RPC-szintű előfordulás a sémában, csak HTTP-státuszkód-hivatkozások (pl. „400 Bad Request" kontextusban) | csak HTTP-válaszkód-kontextusban | Nincs protokoll-szintű „állapot" objektum vagy `*/status` RPC. |
| `discover` | `DiscoverRequest`, `DiscoverResult`, `DiscoverResultResponse` (lásd 6. pont) | `server/discover` oldal | Kizárólag verzió/képesség-egyeztetés, lásd lent. |

**Az egyetlen valódi „életben tartás"-jellegű túlélő** a `basic/transports/streamable-http` oldalon található, a `subscriptions/listen` hosszú életű streamre vonatkozóan.
**Forrás:** `https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/specification/2026-07-28/basic/transports/streamable-http.mdx` (curl, 2026-09-15), 145–151. sor:

> "For long-lived streams — in particular the [`subscriptions/listen`][subscriptions-listen] response stream — servers are encouraged to periodically emit an SSE comment line (a line beginning with a colon, e.g. `:\r\n`) as a **keep-alive**. This keeps the connection from being closed by intermediaries or client idle timeouts during quiet periods when no notifications are flowing."

Ez **nem egy JSON-RPC metódus és nem egy állapot-lekérdezés** — ez egy SSE-protokoll-szintű, üres kommentsor-konvenció, amelynek célja kizárólag a köztes proxyk/idle-timeoutok általi lezárás megelőzése, nem a partner életjelének aktív ellenőrzése (a küldő nem vár és nem is kaphat rá választ). Funkcionálisan tehát jelentősen szűkebb, mint a korábbi kétirányú `ping`/`pong` RPC volt, de a „connection keep-alive" fogalom szó szerint benne maradt a szövegben — ahogy azt a SEP-2575 indoklása (4. pont) előre jelezte.

### 6. A `server/discover` — mi ez, mikor jelent meg, mit ad vissza

**Megjelenés verziója:** kizárólag 2026-07-28-ban. Ellenőriztem mind a négy korábbi nyers sémát (`2024-11-05`, `2025-03-26`, `2025-06-18`, `2025-11-25`) — mindegyikben **nulla találat** a `discover` szóra (case-insensitive grep, exit code 1 mindegyiknél).

**Mit ad vissza — a nyers `schema.ts` szerint** (`raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/2026-07-28/schema.ts`, 653–708. sor):

> "A request from the client asking the server to advertise its supported protocol versions, capabilities, and other metadata. Servers **MUST** implement `server/discover`. Clients **MAY** call it but are not required to — version negotiation can also happen inline via per-request `_meta`."

```ts
export interface DiscoverResult extends CacheableResult {
  supportedVersions: string[];        // "MCP Protocol Versions this server supports"
  capabilities: ServerCapabilities;   // "The capabilities of the server."
  instructions?: string;              // természetes nyelvű útmutatás LLM-eknek
}
```

**Mit ad vissza — a normatív dokumentáció-oldal szerint** (`raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/specification/2026-07-28/server/discover.mdx`, curl, 2026-09-15):

> "`server/discover` lets a client query a server's supported protocol versions, capabilities, and identity before sending any other requests. Servers **MUST** implement it."

> "**When to Call** — Calling `server/discover` is optional for clients… However, `server/discover` is useful in two scenarios: **Presenting server information** … **stdio backward-compatibility probe.**"

> "`serverInfo` is self-reported by the server and is not verified by the protocol. It is intended for display, logging, and debugging. Clients **SHOULD NOT** use it to change their behavior, and **SHOULD NOT** rely on it for security decisions."

**A tervezési dokumentum (SEP-2575) rationale-szakasza is ezt erősíti meg** — a „Separation of Concerns" alfejezetben:

> "**Discovery**: Handled exclusively by `server/discover`. **Capabilities**: Handled on a per-request basis via the `_meta` field or the `subscriptions/listen` RPC."

Sem a séma, sem a doksi-oldal, sem a SEP-szöveg egyetlen mondata sem társítja a `server/discover`-t health-, liveness- vagy állapot-ellenőrzéshez — kizárólag verzió- és képességfelfedezésről, valamint a stdio-n történő visszafelé-kompatibilitási próbáról van szó. **Ez a rész az állítás pontos, hű leírása.**

---

## Amit nem sikerült ellenőrizni

- **A `2024-10-07` git tag pontos jogállása.** Nem sikerült megnyugtatóan kideríteni, hogy ez a tag hivatalos, számozott specifikáció-verziónak minősül-e, vagy csak egy korai, a mostani `docs/specification/<dátum>/` struktúra előtti technikai jelölés — sem séma, sem specifikáció-dokumentum nem tartozik hozzá a jelenlegi fő ágban (mindkettő HTTP 404). Nem találgattam a dátumát vagy jelentőségét.
- **A SEP-2575 GitHub Pull Request (#2575) tényleges vitaszála/kommentjei.** A `github.com/.../pull/2575` oldal közvetlen lekérése ebben a sandboxban HTTP 403-at adott, a GitHub API pedig explicit hibaüzenetet: „GitHub access to this repository is not enabled for this session." Emiatt a PR-vitát magát nem tudtam elolvasni; helyette a SEP hivatalos, végleges (Final) szövegét használtam forrásként, amely ugyanazt az indoklást tartalmazza, mint amit a changelog a PR-re hivatkozva idéz.
- **A repó `docs/specification/` és `schema/` könyvtárainak teljes, API-alapú directory listázása.** A GitHub REST/Tree API ugyanezen 403-as korlátozás miatt nem volt elérhető; helyette célzott, verzió-specifikus nyers URL-eket próbáltam ki egyenként (`raw.githubusercontent.com/.../schema/<verzió>/schema.ts`), és `git ls-remote --tags`-szel kaptam meg a teljes, hiteles tag-listát. Ez lefedte a kért verziókat, de nem zárja ki teljes bizonyossággal, hogy létezik-e a fő ágban olyan köztes verzió-könyvtár, amelynek nevét nem próbáltam ki.
- **A 2024-11-05 előtti, „pre-spec" időszak pontos hivatalos bejelentési dátumai** (pl. az eredeti, 2024 novemberi Anthropic-bejelentés pontos kelte) — ezt nem kutattam külön, mivel a kérdés a *verzió-dátumokra*, nem a marketing-bejelentésekre vonatkozott, és a verzióazonosító (`2024-11-05`) maga a hivatalos „utolsó visszafelé nem kompatibilis változtatás dátuma" a versioning-oldal definíciója szerint.

---

## Meglátogatott és felderített linkek

| Cím | URL | Tier | Lekérés módja | Megjegyzés |
|---|---|---|---|---|
| Versioning (MCP docs, 2026-07-28) | https://modelcontextprotocol.io/docs/2026-07-28/learn/versioning | T1 | WebFetch | „Current" verzió = 2026-07-28; server/discover leírás |
| Key Changes / changelog (2026-07-28) | https://modelcontextprotocol.io/specification/2026-07-28/changelog | T1 | WebFetch | Ping eltávolítás bejelentése (5. pont), server/discover bevezetése (3. pont) |
| Deprecated features registry (2026-07-28) | https://modelcontextprotocol.io/specification/2026-07-28/deprecated | T1 | WebFetch | Ping NEM szerepel a deprecation-táblázatban; „Removed" szakasz üres |
| Ping utility spec (2025-11-25, utolsó élő verzió) | https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/ping | T1 | WebFetch | Teljes ping-leírás, „detect connection health" idézet |
| Ping utility URL a 2026-07-28-ban | https://modelcontextprotocol.io/specification/2026-07-28/basic/utilities/ping | T1 | curl -I | HTTP 308 → átirányítás a changelogra (oldal megszűnt) |
| SEP-2575: Make MCP Stateless | https://modelcontextprotocol.io/seps/2575-stateless-mcp | T1 | WebFetch | Teljes ping-eltávolítási indoklás, server/discover tervezési szövege |
| SEP-2575 nyers markdown | https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/seps/2575-stateless-mcp.md | T1 | curl | Ugyanaz mint fent, nyers fájlként megerősítve |
| SEP-2260: Require Server requests… (Ping health-check idézet) | https://modelcontextprotocol.io/seps/2260-Require-Server-requests-to-be-associated-with-Client-requests | T1 | WebFetch | „keep-alive/health-check mechanism", „MCP-level liveness check" idézetek |
| GitHub Releases lista | https://github.com/modelcontextprotocol/modelcontextprotocol/releases | T1 | WebFetch | Kiegészítő tájékozódás; a pontos dátumokat `git ls-remote`-dal kereszt-ellenőriztem |
| Git tag lista (hiteles) | https://github.com/modelcontextprotocol/modelcontextprotocol.git (git ls-remote --tags) | T1 | Bash / git protokoll | Hiteles, szerver által visszaadott tag-lista |
| Blog „release" címkéjű bejegyzések | https://blog.modelcontextprotocol.io/tags/release/ | T1 | WebFetch | 2026-07-28 végleges kiadás bejelentésének dátuma (2026. júl. 28.) |
| schema.ts — 2024-11-05 | https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/2024-11-05/schema.ts | T1 | curl | `PingRequest` jelen van |
| schema.ts — 2025-03-26 | https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/2025-03-26/schema.ts | T1 | curl | `PingRequest` jelen van |
| schema.ts — 2025-06-18 | https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/2025-06-18/schema.ts | T1 | curl | `PingRequest` jelen van, `discover` nulla találat |
| schema.ts — 2025-11-25 | https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/2025-11-25/schema.ts | T1 | curl | `PingRequest` jelen van, `discover` nulla találat |
| schema.ts — 2026-07-28 (LEGÚJABB) | https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/2026-07-28/schema.ts | T1 | curl | `ping` nulla találat; `DiscoverRequest`/`DiscoverResult` jelen van |
| schema.json — 2026-07-28 (LEGÚJABB) | https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/2026-07-28/schema.json | T1 | curl | `ping`/`Ping` nulla találat |
| schema.ts — draft ág | https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/draft/schema.ts | T1 | curl | Tartalmilag azonos a 2026-07-28-cal; `ping` nulla találat |
| server/discover doksi-oldal (nyers .mdx) | https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/specification/2026-07-28/server/discover.mdx | T1 | curl | Teljes leírás: verzió/képesség/identitás lekérdezés, stdio-kompat. próba |
| streamable-http transport doksi (nyers .mdx) | https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/specification/2026-07-28/basic/transports/streamable-http.mdx | T1 | curl | Az egyetlen `keep-alive` találat a 2026-07-28 specifikáció-szövegben (SSE-kommentsor) |
| ping.mdx elérési út a 2026-07-28-ban | https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/specification/2026-07-28/basic/utilities/ping.mdx | T1 | curl | HTTP 404 — a fájl fizikailag nem létezik ebben a verzióban |
| llms-full.txt (teljes doksi-korpusz) | https://modelcontextprotocol.io/llms-full.txt | T1 | curl | 31 db `/specification/2026-07-28/` oldal teljes szövegének átfésülése `ping/health/heartbeat/keepalive/alive` kulcsszavakra |
| llms.txt (oldal-index) | https://modelcontextprotocol.io/llms.txt | T1 | curl | A hivatalos oldaltérkép, a fenti korpusz-fájl eredetének ellenőrzésére |
| GitHub PR #2575 (nem sikerült elérni) | https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2575 | T1 | curl (403) | Blokkolva ebben a sandboxban; a SEP végleges szövege pótolta |
| GitHub Tree/Contents API (nem sikerült elérni) | https://api.github.com/repos/modelcontextprotocol/modelcontextprotocol/contents/docs/specification | T1 | curl (403) | „GitHub access to this repository is not enabled for this session" — API-hozzáférés blokkolva, nyers-fájl-lekérésekkel pótolva |
