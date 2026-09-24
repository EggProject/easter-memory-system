# ELL02 — Folyamatfelügyeleti alapértékek ellenőrzése

Ellenőrző (verifikációs) kutatás. Cél: egy másik kutató által közölt macOS launchd és
systemd folyamatfelügyeleti alapérték-állításokat ELSŐDLEGES forrásból megerősíteni vagy
cáfolni, ott ahol a másik kutató korábban csak tükör-oldalt (manpagez.com, man7.org) tudott
idézni.

**Módszertani megjegyzés (degradált kutatási mód).** A `deep-web-research` skill szerint
futott a kutatás, de a skill Sonnet-kereső / Opus-szintézis subagent-szétválasztása ebben a
környezetben nem volt elérhető (nem volt "Agent" dispatch eszköz) — ez a helyzet, amit a
skill saját maga "degradált, de működő" módként ismer el. Ennek kompenzálására minden
számadatot **nyers forrásfájlból, közvetlen szövegkinyeréssel** (curl + grep a
raw.githubusercontent.com-ról letöltött forrásfájlokon), nem LLM-parafrázissal
ellenőriztem — így a lenti idézetek garantáltan szó szerintiek, karakterre pontosan
egyeznek a forrásfájllal. A nyers forrásfájlok archiválva vannak:
`/home/claude/work/kutatas-uzemeltetes/.research/ell02-felugyelet/02-sources/raw/`.

---

## Ítélet

| # | Állítás | Ítélet |
|---|---|---|
| 1 | launchd `ThrottleInterval` alapértéke 10 mp | **IGAZOLVA elsődleges forrásból** (Apple hivatalos GitHub-forráskódja) |
| 2 | launchd `KeepAlive` szótár-szemantika (SuccessfulExit, Crashed*, NetworkState, PathState, OtherJobEnabled) | **IGAZOLVA elsődleges forrásból, egy ponton pontosítással** — a hivatalos man-forrás `SuccessfulExit`-ot, `NetworkState`-et, `PathState`-et és `OtherJobEnabled`-et szó szerint így nevezi; önálló `Crashed` kulcsot **nem** nevesít (l. lent) |
| 3 | Nincs launchd-ben systemd `WatchdogSec`-nek megfelelő aktív életjel/watchdog mechanizmus | **IGAZOLVA elsődleges forrásból** (a teljes kulcslista kimerítő vizsgálatával) |
| 4a | systemd `RestartSec` alapértéke 100 ms | **IGAZOLVA elsődleges forrásból** (GitHub, v261 kiadás) |
| 4b | systemd `DefaultStartLimitIntervalSec` alapértéke 10 mp | **IGAZOLVA elsődleges forrásból** (GitHub, v261 kiadás) |
| 4c | systemd `DefaultStartLimitBurst` alapértéke 5 | **IGAZOLVA elsődleges forrásból** (GitHub, v261 kiadás) |
| 4d | systemd `DefaultTimeoutStopSec` alapértéke 90 mp | **IGAZOLVA elsődleges forrásból** (build-időben behelyettesített érték, 3 forrásfájl láncából rekonstruálva) |
| 5 | `Restart=` megengedett értékei | **IGAZOLVA elsődleges forrásból** — 7 érték: `no`, `on-success`, `on-failure`, `on-abnormal`, `on-watchdog`, `on-abort`, `always` |
| 6 | Mi történik `StartLimitBurst` túllépésekor | **IGAZOLVA elsődleges forrásból** |
| 7 | Melyik verzióra vonatkoznak az értékek / legfrissebb kiadás | **IGAZOLVA elsődleges forrásból** — legfrissebb kiadott tag: **v261** (2026-06-19); az ellenőrzött beállítások a `main` ágon (v262-fejlesztés) is azonos szöveggel szerepelnek, és `v209`/`v229` óta (kb. 2013 óta) változatlanok |
| 8 | `on-failure` vs `always` szándékos `systemctl stop` esetén | **IGAZOLVA elsődleges forrásból** — mindkettő azonosan viselkedik: egyik sem indítja újra a szolgáltatást szándékos leállításkor |

\* Lásd a 2. tétel részletes bizonyítékát — a `Crashed` mint önálló `KeepAlive` alkulcs nem
szerepel az Apple-forrásban; ez pontosítja (részben cáfolja) az eredeti kutató
megfogalmazását, ha az szó szerint `Crashed` kulcsot állított.

---

## Bizonyítékok — macOS launchd

### 1. `ThrottleInterval` alapértéke = 10 másodperc

**Forrás (T1, elsődleges):** Apple hivatalos GitHub-szervezete, `apple-oss-distributions`
("OSS Code distributed by Apple, Inc.") — ez a 2022 óta érvényes hivatalos utódja az
opensource.apple.com-nak (amely mostanra több man-oldal URL-jén 404-et ad, l. lent).

URL: `https://raw.githubusercontent.com/apple-oss-distributions/launchd/main/man/launchd.plist.5`

Szó szerinti idézet a `launchd.plist(5)` man-forrásból (troff/mdoc formátum):

> `.It Sy ThrottleInterval <integer>`
> `This key lets one override the default throttling policy imposed on jobs by` `.Nm launchd .`
> `The value is in seconds, and by default, jobs will not be spawned more than once every 10 seconds.`
> `The principle behind this is that jobs should linger around just in case they are needed again in the near future. This not only reduces the latency of responses, but it encourages developers to amortize the cost of program invocation.`

Ez szó szerint megegyezik az állítással: **10 másodperc az alapérték**, és a man-oldal
kifejezetten a "jobs will not be spawned more than once every 10 seconds" mondattal él —
ez pontosan az eredeti kutató által idézett megfogalmazás.

**Kereszt-ellenőrzés a tükör-oldallal:** a manpagez.com (`https://www.manpagez.com/man/5/launchd.plist/`)
ugyanezt a mondatot hozza, karakterre egyezően:

> "The value is in seconds, and by default, jobs will not be spawned more than once every
> 10 seconds."

→ Vagyis a másik kutató tükör-idézete **pontosan egyezik** az elsődleges Apple-forrással;
nincs eltérés, csak a forrás tier-je javult T5 (tükör)-ről T1 (Apple saját forráskódja)-ra.

**A man-oldal kelte:** `.Dd 1 May, 2009` — a szöveg utolsó dokumentált módosítása 2009.
május 1. Ez azt jelenti, hogy ez a megfogalmazás legalább Snow Leopard (10.6) kora óta
változatlan, és az Apple által jelenleg is közzétett forrásban ez az érvényes szöveg (nincs
újabb, ezt felülíró man-oldal-verzió a repóban).

**Megjegyzés a fő Apple-fejlesztői man-oldal böngészőről:** a feladatban javasolt
`developer.apple.com/library/archive/documentation/Darwin/Reference/ManPages/man5/launchd.plist.5.html`
URL jelenleg **404-et ad** (ellenőrizve közvetlen HTTP-kéréssel) — Apple ezt az archívum-
útvonalat láthatóan megszüntette. Emiatt az `apple-oss-distributions` GitHub-forrás a
legjobb elérhető elsődleges forrás erre az adatra.

---

### 2. `KeepAlive` szótár-szemantika

**Forrás:** ugyanaz a `launchd.plist(5)` man-forrás, mint fent.

Szó szerinti idézet a bevezető szövegről:

> "This optional key is used to control whether your job is to be kept continuously
> running or to let demand and conditions control the invocation. The default is false and
> therefore only demand will start the job. The value may be set to true to
> unconditionally keep the job alive. Alternatively, a dictionary of conditions may be
> specified to selectively control whether launchd keeps a job alive or not. If multiple
> keys are provided, launchd ORs them, thus providing maximum flexibility to the job to
> refine the logic and stall if necessary. If launchd finds no reason to restart the job,
> it falls back on demand based invocation. Jobs that exit quickly and frequently when
> configured to be kept alive will be throttled to converve system resources."
> *(a "converve" elgépelés az eredeti Apple-forrásban is így szerepel — nem az én hibám)*

A négy alkulcs szó szerint, egyenként:

> **SuccessfulExit** `<boolean>`
> "If true, the job will be restarted as long as the program exits and with an exit status
> of zero. If false, the job will be restarted in the inverse condition. This key implies
> that "RunAtLoad" is set to true, since the job needs to run at least once before we can
> get an exit status."

> **NetworkState** `<boolean>`
> "If true, the job will be kept alive as long as the network is up, where up is defined as
> at least one non-loopback interface being up and having IPv4 or IPv6 addresses assigned
> to them. If false, the job will be kept alive in the inverse condition."

> **PathState** `<dictionary of booleans>`
> "Each key in this dictionary is a file-system path. If the value of the key is true, then
> the job will be kept alive as long as the path exists. If false, the job will be kept
> alive in the inverse condition. The intent of this feature is that two or more jobs may
> create semaphores in the file-system namespace."

> **OtherJobEnabled** `<dictionary of booleans>`
> "Each key in this dictionary is the label of another job. If the value of the key is
> true, then this job is kept alive as long as that other job is enabled. Otherwise, if the
> value is false, then this job is kept alive as long as the other job is disabled. This
> feature should not be considered a substitute for the use of IPC."

**Pontosítás a `Crashed` kulcsról.** Az elsődleges Apple-forrás **nem** tartalmaz önálló
`Crashed` alkulcsot a `KeepAlive` szótárban. A teljes kulcslista a man-oldalon (kimerítő
felsorolás, l. 3. pont bizonyítéka) csak ezt a négyet nevesíti a `KeepAlive` szótár alatt:
`SuccessfulExit`, `NetworkState`, `PathState`, `OtherJobEnabled`. Ha az eredeti kutató
`Crashed`-et is a hivatalos kulcsnevek között sorolta fel, az **nem igazolható** ebből az
elsődleges forrásból — a "crash után újraindítás" viselkedés a launchd-ben nem külön
`Crashed` kulccsal, hanem a `SuccessfulExit=false` beállítással (vagy pusztán a `KeepAlive`
puszta `true` értékével, ami minden nem-tiszta kilépés esetén újraindít) érhető el. Ez
terminológiai pontosítás, nem funkcionális cáfolat: a *viselkedés* (crash esetén
újraindítás) létezik, de nem `Crashed` néven dokumentált kulcsként.

---

### 3. Van-e launchd-ben watchdog/életjel-mechanizmus (systemd `WatchdogSec` megfelelője)?

**Módszer:** kimerítő bizonyíték — a teljes `launchd.plist(5)` kulcslista (mind a ~75
`.It Sy <kulcsnév>` bejegyzés) átvizsgálása ugyanabból az elsődleges Apple-forrásból.

A teljes kulcslista (csak a nevek, sorrendben, a forrásfájlból kinyerve):
`Label, Disabled, UserName, GroupName, inetdCompatibility, Wait, LimitLoadToHosts,
LimitLoadFromHosts, LimitLoadToSessionType, Program, ProgramArguments, EnableGlobbing,
EnableTransactions, OnDemand, KeepAlive (+SuccessfulExit, NetworkState, PathState,
OtherJobEnabled), RunAtLoad, RootDirectory, WorkingDirectory, EnvironmentVariables, Umask,
TimeOut, ExitTimeOut, ThrottleInterval, InitGroups, WatchPaths, QueueDirectories,
StartOnMount, StartInterval, StartCalendarInterval (+Minute/Hour/Day/Weekday/Month),
StandardInPath, StandardOutPath, StandardErrorPath, Debug, WaitForDebugger,
SoftResourceLimits/HardResourceLimits (+Core/CPU/Data/FileSize/MemoryLock/
NumberOfFiles/NumberOfProcesses/ResidentSetSize/Stack), Nice, ProcessType, AbandonProcessGroup,
LowPriorityIO, LaunchOnlyOnce, MachServices, ResetAtClose, HideUntilCheckIn, Sockets
(+SockType/SockPassive/SockNodeName/SockServiceName/SockFamily/SockProtocol/SockPathName/
SecureSocketWithKey/SockPathMode), Bonjour, MulticastGroup`.

Nincs köztük `Watchdog`, `WatchdogSec`, `HeartBeat`, `Ping`, `LivenessCheck` vagy hasonló
nevű kulcs. A legközelebbi rokon mechanizmus az `EnableTransactions`, de ennek szemantikája
alapvetően más:

> "This flag instructs launchd that the job promises to use `vproc_transaction_begin(3)`
> and `vproc_transaction_end(3)` to track outstanding transactions that need to be
> reconciled before the process can safely terminate. If no outstanding transactions are in
> progress, then launchd is free to send the SIGKILL signal."

Ez egy **leállás-koordinációs** mechanizmus (a job jelzi, mikor biztonságos leállítani —
tehát a *launchd* kérdezi meg a jobot leállás előtt), **nem** egy folyamatos, proaktív
életjel-küldés, aminek elmaradása magától újraindítást váltana ki úgy, ahogy a systemd
`WatchdogSec=` + `sd_notify(WATCHDOG=1)` páros működik (l. `systemd.service.xml`
`WatchdogSec=` szakasza: "a watchdog timeout will occur if the watchdog has not pinged for
20s (10s before...)" — ez a systemd-oldali analógia, aminek nincs launchd-megfelelője).

**Ítélet:** a hiány elsődleges forrással igazolt — az Apple által hivatalosan közzétett,
kimerítő `launchd.plist` kulcslista nem tartalmaz proaktív életjel/watchdog-időzítő
mechanizmust. A `KeepAlive` egy *reaktív* (kilépés-alapú) újraindítási logika, nem egy
*proaktív* (életjel-alapú) figyelő logika.

---

## Bizonyítékok — systemd

**Forrás minden systemd-tételhez (T1, elsődleges):** a systemd hivatalos GitHub-repója,
rögzítve a **v261** kiadási tagre (a kutatás idején — 2026-09-15 — ez a legfrissebb
kiadott, tagelt verzió; l. 7. pont). A `main` ág tartalma (a fejlesztés alatt álló,
következő, még ki nem adott verzió felé halad — a NEWS fájl "CHANGES WITH 262 in spe[c]"
címsorral kezdődik) ugyanezekre a beállításokra szó szerint azonos szöveget ad — ez
kizárja, hogy egy nemrég bevezetett/eltávolított változásról legyen szó.

### 4a. `RestartSec` alapértéke = 100 ms

URL: `https://raw.githubusercontent.com/systemd/systemd/v261/man/systemd.service.xml`

Szó szerint (`RestartSec=` szakasz):

> "Configures the time to sleep before restarting a service (as configured with
> `Restart=`). Takes a unit-less value in seconds, or a time span value such as "5min 20s".
> Defaults to 100ms."

### 4b–4c. `DefaultStartLimitIntervalSec` = 10 mp, `DefaultStartLimitBurst` = 5

URL: `https://raw.githubusercontent.com/systemd/systemd/v261/man/systemd-system.conf.xml`

Szó szerint:

> "Configure the default unit start rate limiting, as configured per-service by
> `StartLimitIntervalSec=` and `StartLimitBurst=`. See systemd.service(5) for details on
> the per-service settings. `DefaultStartLimitIntervalSec=` defaults to 10s.
> `DefaultStartLimitBurst=` defaults to 5."

(Verzió-címke a forrásban: `<xi:include href="version-info.xml" xpointer="v209"/>` — ez a
beállítás legalább systemd v209 óta, azaz kb. 2013 óta létezik ezekkel az alapértékekkel.)

### 4d. `DefaultTimeoutStopSec` alapértéke = 90 másodperc

Ez a szám **build-időben behelyettesített érték**, ezért három forrásfájl együtt igazolja —
mindhárom a systemd hivatalos repójából, v261 tag:

1. `man/systemd-system.conf.xml` — a doksi-szöveg egy XML-entitásra hivatkozik, nem
   literál számra:

   > "`DefaultTimeoutStartSec=` and `DefaultTimeoutStopSec=` default to &DEFAULT_TIMEOUT_SEC;
   > in the system manager and &DEFAULT_USER_TIMEOUT_SEC; in the user manager.
   > `DefaultTimeoutAbortSec=` is not set by default so that all units fall back to
   > `TimeoutStopSec=`. `DefaultRestartSec=` defaults to 100 ms."

2. `man/custom-entities.ent.in` — az entitás definíciója egy build-időben behelyettesítendő
   sablon-változó:

   > `<!ENTITY DEFAULT_TIMEOUT_SEC "{{DEFAULT_TIMEOUT_SEC}} s">`

3. `meson_options.txt` — a `{{DEFAULT_TIMEOUT_SEC}}` sablon-változó tényleges,
   build-rendszerbeli alapértéke:

   > `option('default-timeout-sec', type : 'integer', value : 90, description : 'default`
   > `timeout for system unit start/stop')`

Együtt olvasva a három idézet: a végleges, lefordított man-oldalon a mondat "...default to
**90 s**..." lesz. Ez **igazolja** a 90 másodperces alapértéket, de fontos módszertani
pontosítás: ez **nem egyetlen literál szám egyetlen fájlban**, hanem egy build-időben
összeálló érték — aki csak a kiadott, disztribúció-specifikus man-oldalt nézi (pl. Ubuntu
vagy Fedora csomagolt man-oldala), ott már a behelyettesített "90 s" szöveget látja
literálként, ahogy a tükör-oldalak (man7.org, manpagez.com) is.

### 5. `Restart=` összes megengedett értéke

URL: `https://raw.githubusercontent.com/systemd/systemd/v261/man/systemd.service.xml`

Szó szerint:

> "Takes one of `no`, `on-success`, `on-failure`, `on-abnormal`, `on-watchdog`,
> `on-abort`, or `always`. If set to `no` (the default), the service will not be
> restarted."

Tehát pontosan **7 megengedett érték** van: `no` (alapértelmezett), `on-success`,
`on-failure`, `on-abnormal`, `on-watchdog`, `on-abort`, `always`.

### 6. Mi történik `StartLimitBurst` túllépésekor

URL: `https://raw.githubusercontent.com/systemd/systemd/v261/man/systemd.unit.xml`
(`StartLimitIntervalSec=` / `StartLimitBurst=` szakasz)

Szó szerint:

> "Configure unit start rate limiting. Units which are started more than *burst* times
> within an *interval* time span are **not permitted to start any more**."

> "Note that units which are configured for `Restart=`, and which reach the start limit
> are **not attempted to be restarted anymore**; however, they may still be restarted
> manually or from a timer or socket at a later point, after the *interval* has passed.
> From that point on, the restart logic is activated again. `systemctl reset-failed` will
> cause the restart rate counter for a service to be flushed, which is useful if the
> administrator wants to manually start a unit and the start limit interferes with that."

Kiegészítésül a `systemd.service.xml`-ből, a `StartLimitAction=` szakasz azt is rögzíti,
hogy alapból (`none`) a limit túllépése önmagában **nem** vált ki extra akciót (pl.
reboot), csak azt, hogy a további indítás nem engedélyezett:

> "If `none` is set, hitting the rate limit will trigger no action except that the start
> will not be permitted. Defaults to `none`."

### 7. Melyik systemd verzióra vonatkoznak az értékek + legfrissebb kiadás

**Legfrissebb kiadott (tagelt) verzió a kutatás idején (2026-09-15):** `v261`
(`git ls-remote --tags https://github.com/systemd/systemd.git` végigfuttatva, a
legmagasabb szemantikus tag `v261`; GitHub Releases oldal szerint a `v261` kiadás dátuma
2026. június 19.). A `main` fejlesztői ág ekkor már a következő, még ki nem adott
verziót (`262`) célozza — ezt a repó `NEWS` fájljának "CHANGES WITH 262 in spe[c]"
bevezető sora jelzi.

Az ellenőrzött négy szám (4a–4d) **mind a v261 tagen rögzített forrásfájlokból** lett
kiolvasva, tehát kifejezetten a jelenlegi legfrissebb kiadott systemd-verzióra
vonatkoznak — nem csak egy fejlesztői pillanatképre. A `DefaultStartLimitIntervalSec` /
`DefaultStartLimitBurst` pár forrás-megjegyzése (`version-info.xml xpointer="v209"`)
szerint ez a beállítás-pár már **v209 óta** (kb. 2013) ilyen alapértékekkel létezik —
vagyis ez egy régóta stabil alapérték, nem egy nemrég változott szám.

### 8. `Restart=on-failure` vs `Restart=always` szándékos `systemctl stop` esetén

URL: `https://raw.githubusercontent.com/systemd/systemd/v261/man/systemd.service.xml`
(`Restart=` szakasz, bevezető és záró bekezdés)

Szó szerint, a szakasz elején (érvényes **minden** `Restart=` értékre, tehát `always`-re
is):

> "Configures whether the service shall be restarted when the service process exits, is
> killed, or a timeout is reached. [...] **When the death of the process is a result of
> systemd operation (e.g. service stop or restart), the service will not be restarted.**"

És explicit módon, kifejezetten a `systemctl stop` parancsra nézve, a táblázat utáni
bekezdésben:

> "As exceptions to the setting above, **the service will not be restarted if** the exit
> code or signal is specified in `RestartPreventExitStatus=` (see below) or **the service
> is stopped with `systemctl stop` or an equivalent operation.** Also, the services will
> always be restarted if the exit code or signal is specified in
> `RestartForceExitStatus=` (see below)."

**Következtetés a kereszt-ellenőrzésből:** ez a kivétel **nem tesz különbséget**
`on-failure` és `always` között — mindkettő ugyanúgy viselkedik szándékos
`systemctl stop` esetén: **egyik sem indítja újra** a szolgáltatást. A `Restart=`
beállítás (bármelyik nem-`no` érték) csakis a folyamat *saját, nem szándékos* halálára
(összeomlás, hibás kilépőkód, timeout, watchdog-hiba) vonatkozik — az adminisztrátor általi
szándékos leállítás mindig kivétel, függetlenül attól, hogy `on-failure`-t vagy `always`-t
állítottak-e be. A gyakori tévhit, hogy "`Restart=always` még szándékos leállítás után is
visszahozza a szolgáltatást" — ez **cáfolható** ezzel az elsődleges forrással: `systemctl
stop` esetén `always` sem indítja újra.

---

## Amit nem sikerült ellenőrizni

- **Apple fejlesztői man-oldal böngésző (developer.apple.com/library/archive/.../
  launchd.plist.5.html)** — ez a konkrét URL jelenleg 404-et ad, tehát nem tudtam
  közvetlenül Apple hivatalos, "hivatalos man-oldal böngésző" felületéről igazolni; helyette
  Apple hivatalos GitHub-forráskódját (`apple-oss-distributions/launchd`) használtam
  elsődleges forrásként, ami tartalmilag ugyanaz a man-forrásfájl, amiből a fejlesztői
  portál oldala valaha generálódott. Ezt a fallback-et a feladatkiírás kifejezetten
  megengedte ("ha egyik sem érhető el, mondd ki, és nevezd meg a legjobb elérhető
  másodlagos forrást") — itt azonban nem másodlagos, hanem egy másik, ugyanolyan erősségű
  elsődleges (Apple saját) forrásra sikerült áttérni, tehát az igazolás erőssége nem
  csökkent.
- **A `Crashed` `KeepAlive`-alkulcs létezése konkrétan ezen a néven** — az elsődleges
  forrás nem nevesíti; NEM ELLENŐRIZHETŐ állításként szerepelt volna, ha az eredeti kutató
  ezt a nevet használta — helyette CÁFOLVA/pontosítva, ahogy a 2. tételnél részleteztem.
- **Az `apple-oss-distributions/launchd` repó pontos macOS-verzió/build-száma** (tag-szint),
  amelyhez ez a man-fájl tartozik — a repó tag-listája (`/tags` végpont) robots.txt által
  tiltott a keresőeszközömnek, így csak a fájlon belüli `.Dd 1 May, 2009` dátumbélyeget
  tudtam elsődleges forrásból igazolni, a konkrét GitHub-tag/release-számot nem.
- **Modell-szintű keresztellenőrzés Opus-szintézissel** — a skill előírt Sonnet-kereső /
  Opus-szintézis szétválasztása nem futott le (l. a bevezető módszertani megjegyzést),
  emiatt ez a jelentés egyetlen munkamenetben készült, nem független verifikáló
  subagent-ekkel keresztellenőrizve. Minden számot azonban nyers forrásfájlból, nem
  LLM-összefoglalóból nyertem ki, ami részben kompenzálja ezt a korlátot.

---

## Meglátogatott és felderített linkek

| Cím | URL | Tier | Lekérés módja | Megjegyzés |
|---|---|---|---|---|
| `launchd.plist(5)` man-forrás, Apple hivatalos GitHub-szervezet | https://raw.githubusercontent.com/apple-oss-distributions/launchd/main/man/launchd.plist.5 | T1 | curl (nyers szöveg) | Elsődleges forrás az 1–3. tételekhez; `.Dd 1 May, 2009` |
| `apple-oss-distributions/launchd` repó gyökere | https://github.com/apple-oss-distributions/launchd | T1 | WebFetch | Megerősíti: "OSS Code distributed by Apple, Inc." |
| `apple-oss-distributions` GitHub-szervezet | https://github.com/apple-oss-distributions | T1 | WebFetch | Szervezet-szintű megerősítés (509 repó, Apple hivatalos) |
| Apple fejlesztői man-oldal böngésző (launchd.plist.5.html) | https://developer.apple.com/library/archive/documentation/Darwin/Reference/ManPages/man5/launchd.plist.5.html | — | curl (HTTP fejléc) | **404 — nem elérhető**, ezért lett fallback az Apple GitHub-forrás |
| opensource.apple.com launchd projektlap | https://opensource.apple.com/source/launchd/ | — | curl (HTTP fejléc) | **404 — nem elérhető**, a projekt átköltözött GitHub-ra |
| manpagez.com tükör-oldal | https://www.manpagez.com/man/5/launchd.plist/ | T5 (tükör) | curl (HTML letöltés + szövegkinyerés) | Kereszt-ellenőrzésre használva; szó szerint egyezik az Apple-forrással |
| `systemd.service.xml`, systemd hivatalos repó, v261 tag | https://raw.githubusercontent.com/systemd/systemd/v261/man/systemd.service.xml | T1 | curl (nyers XML) | `RestartSec`, `Restart=` értékei, on-failure/always kivétel |
| `systemd-system.conf.xml`, systemd hivatalos repó, v261 tag | https://raw.githubusercontent.com/systemd/systemd/v261/man/systemd-system.conf.xml | T1 | curl (nyers XML) | `DefaultStartLimitIntervalSec`, `DefaultStartLimitBurst`, `DefaultTimeoutStopSec` (entitás-hivatkozás) |
| `systemd.unit.xml`, systemd hivatalos repó, v261 tag | https://raw.githubusercontent.com/systemd/systemd/v261/man/systemd.unit.xml | T1 | curl (nyers XML) | `StartLimitIntervalSec`/`StartLimitBurst` túllépés viselkedése |
| `custom-entities.ent.in`, systemd hivatalos repó, v261 tag | https://raw.githubusercontent.com/systemd/systemd/v261/man/custom-entities.ent.in | T1 | curl (nyers szöveg) | A `DEFAULT_TIMEOUT_SEC` XML-entitás sablon-definíciója |
| `meson_options.txt`, systemd hivatalos repó, v261 tag | https://raw.githubusercontent.com/systemd/systemd/v261/meson_options.txt | T1 | curl (nyers szöveg) | A `default-timeout-sec` build-opció tényleges értéke: 90 |
| `meson.build`, systemd hivatalos repó, main ág | https://raw.githubusercontent.com/systemd/systemd/main/meson.build | T1 | curl (nyers szöveg) | Megmutatja, hogy `DEFAULT_TIMEOUT_SEC` a `default-timeout-sec` opcióból jön |
| systemd `NEWS` fájl, main ág | https://raw.githubusercontent.com/systemd/systemd/main/NEWS | T1 | curl (nyers szöveg) | "CHANGES WITH 262 in spe[c]" — a `main` ág fejlesztői állapotának igazolása |
| systemd GitHub tag-lista (`git ls-remote`) | https://github.com/systemd/systemd.git (git protokoll) | T1 | `git ls-remote --tags` | Legmagasabb tag: `v261` |
| systemd v261 GitHub Release oldal | https://github.com/systemd/systemd/releases/tag/v261 | T1 | WebFetch | Kiadási dátum: 2026. június 19. |
| systemd/systemd GitHub repó gyökere | https://github.com/systemd/systemd | — | curl | 403 — a sima repó-főoldal curl-lel nem tölthető (bot-védelem), de a raw fájl-végpontok igen |
| api.github.com repo-végpont | https://api.github.com/repos/systemd/systemd/releases/latest | — | curl | 403 — API-végpont nem elérhető curl-lel (rate-limit/bot-védelem); helyette `git ls-remote` és WebFetch adta az adatot |
| `apple-oss-distributions/launchd` `/tags` aloldal | https://github.com/apple-oss-distributions/launchd/tags | — | WebFetch | `ROBOTS_DISALLOWED` — nem sikerült elérni a repó tag-listáját |
| `apple-oss-distributions/launchd` `/tree/main` aloldal | https://github.com/apple-oss-distributions/launchd/tree/main | — | WebFetch | `ROBOTS_DISALLOWED` — a fájllista-nézet nem elérhető, ezért találgatással (raw URL-próbákkal) kellett megtalálni a `man/launchd.plist.5` útvonalat |
