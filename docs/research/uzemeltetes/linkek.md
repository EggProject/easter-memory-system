# Linkek — üzemeltetés

Minden meglátogatott és felderített forrás, kutatási egységenként.

---



---

# SQ01 — Mit érdemes figyelni egy egyfelhasználós, önüzemeltetett szolgáltatásnál?
## Meglátogatott és felderített linkek

| Cím | URL | Tier | Lekérés módja | Megjegyzés |
|---|---|---|---|---|
| Monitoring Distributed Systems — Google SRE Book | https://sre.google/sre-book/monitoring-distributed-systems/ | T1 | curl letöltés + szöveg-kinyerés, majd grep | Fő forrás a négy arany jelzéshez és a monitorozás komplexitásához |
| Introduction — Google SRE Book | https://sre.google/sre-book/introduction/ | T1 | curl letöltés + grep | Kerestem explicit "kis csapat/startup" idézetet, nem találtam ilyet ebben a fejezetben |
| Storage — Prometheus hivatalos dokumentáció | https://prometheus.io/docs/prometheus/latest/storage/ | T1 | curl letöltés + szöveg-kinyerés | Fő forrás a bájt/minta és retenciós számokhoz |
| Scaling the Collector — OpenTelemetry | https://opentelemetry.io/docs/collector/scaling/ | T1 | WebFetch | Nincs benne konkrét memória/CPU szám — negatív eredmény forrása |
| Configuration Cheat Sheet — Gitea Documentation | https://docs.gitea.com/administration/config-cheat-sheet | T1 | curl (első próbálkozás 0 bájt, sikertelen; második próbálkozás más User-Agent stringgel sikeres) + grep | Metrics szakasz: ENABLED alapból false |
| Configuration Cheat Sheet — Forgejo | https://forgejo.org/docs/latest/admin/config-cheat-sheet/ | T1 | curl letöltés + grep | Azonos Metrics szakasz mint Giteánál |
| Configuration Parameters — Miniflux | https://miniflux.app/docs/configuration.html | T1 | WebFetch | METRICS_COLLECTOR alapból kikapcsolva |
| metric package — miniflux.app/metric (Go Packages) | https://pkg.go.dev/miniflux.app/metric | T1 | curl letöltés + szöveg-kinyerés | Forráskódból generált metrika-nevek |
| Prometheus-Style Metrics — Syncthing documentation | https://docs.syncthing.net/users/metrics.html | T1 | curl letöltés + teljes szöveg elolvasva | Teljes metrika-lista, nincs explicit ENABLED kapcsoló |
| Monitoring — Jellyfin | https://jellyfin.org/docs/general/post-install/networking/advanced/monitoring/ | T1 | curl letöltés + teljes szöveg elolvasva | EnableMetrics=false alapból, explicit biztonsági indoklás |
| Monitoring — Immich | https://docs.immich.app/features/monitoring/ | T1 | curl letöltés + teljes szöveg elolvasva | Opt-in telemetria, IMMICH_TELEMETRY_INCLUDE |
| Prometheus metrics · dani-garcia/vaultwarden PR #3634 | https://github.com/dani-garcia/vaultwarden/pull/3634 | T2 | WebFetch | Karbantartó elutasította a natív metrika-végpontot |
| Prometheus metrics · Issue #496 · dani-garcia/vaultwarden | https://github.com/dani-garcia/vaultwarden/issues/496 | T2 | WebSearch találat, nem nyitottam meg részletesen | Kapcsolódó, régebbi feature-kérés |
| Prometheus Metrics — Vaultwarden Forum | https://vaultwarden.discourse.group/t/prometheus-metrics/1571 | T3 | WebFetch | Nem hivatalos fórum; karbantartó megerősíti, hogy nincs metrika-végpont |
| Metrics endpoint for Prometheus — paperless-ngx Discussion #1541 | https://github.com/paperless-ngx/paperless-ngx/discussions/1541 | T3 | WebFetch | Nem hivatalos fórum jellegű GitHub Discussion; lezárva és zárolva, nincs natív támogatás |
| Monitoring Forgejo as a System Administrator — Codeberg discussion #399 | https://codeberg.org/forgejo/discussions/issues/399 | T3 | WebFetch | Nem hivatalos közösségi vita; megerősíti a natív /metrics létét és korlátozott gyakorlati használatát |
| Advisory GHSA-3qjf-qh38-x73v — Miniflux | https://github.com/miniflux/v2/security/advisories/GHSA-3qjf-qh38-x73v | T1 | WebSearch találat, cím és tartalom áttekintve | Biztonsági hiba a metrika-végpont hálózati szűrésében |
| The USE Method — Brendan Gregg | https://www.brendangregg.com/usemethod.html | T3 | WebFetch | Nem hivatalos személyes oldal, de a módszer egyetlen elsődleges forrása |
| USE Method Rosetta Stone — Brendan Gregg | https://www.brendangregg.com/USEmethod/use-rosetta.html | T3 | WebFetch | Nem tartalmazott explicit korlátozó kijelentést, ezért nem idéztem belőle |
| The RED Method: Key Metrics for Microservices Architecture — Weaveworks | https://www.weave.works/blog/the-red-method-key-metrics-for-microservices-architecture/ | T3 | WebFetch | Nem hivatalos vállalati blog, de a módszer megalkotójának (Tom Wilkie) saját, elsődleges cikke |
| Summary of the October 22, 2012 AWS Service Event | https://aws.amazon.com/message/680342/ | T1 | WebFetch | Hivatalos AWS incidens-összefoglaló; monitorozási hiányosság szerepe egy üzemzavarban |
| Healthchecks.io Documentation | https://healthchecks.io/docs/ | T1 | curl letöltés + teljes szöveg elolvasva | "Dead man's switch" fogalom hivatalos leírása |
| Metrics endpoint for prometheus · Issue #2751 · go-gitea/gitea | https://github.com/go-gitea/gitea/issues/2751 | T2 | WebSearch találat, nem nyitottam meg részletesen | Történeti kontextus a Gitea metrika-végpont bevezetéséhez |
| [WIP] Expose prometheus metrics with gitea · PR #678 · go-gitea/gitea | https://github.com/go-gitea/gitea/pull/678 | T2 | WebSearch találat, nem nyitottam meg részletesen | A metrika-végpont eredeti bevezető PR-je (2016) |
| jellyfin-prometheus-exporter (StefanAbl) | https://github.com/StefanAbl/jellyfin-prometheus-exporter | T3 | csak találat, nem nyitottam meg | Harmadik féltől származó, nem hivatalos exportáló |
| jellyfin_exporter (rebelcore) | https://github.com/rebelcore/jellyfin_exporter | T3 | csak találat, nem nyitottam meg | Harmadik féltől származó, nem hivatalos exportáló |
| prometheus-paperless-exporter (hansmi) | https://github.com/hansmi/prometheus-paperless-exporter | T3 | csak találat, nem nyitottam meg | Harmadik féltől származó, nem hivatalos exportáló; szuperfelhasználói API-hozzáférést igényel |
| vwmetrics (Tricked-dev) | https://github.com/Tricked-dev/vwmetrics | T3 | csak találat, nem nyitottam meg | Harmadik féltől származó, nem hivatalos Vaultwarden-exportáló |
| Cardinality Explosion: The Silent Killer of Your Observability Stack — Medium | https://medium.com/@PlanB./cardinality-explosion-the-silent-killer-of-your-observability-stack-and-how-to-defuse-it-9da667fb61bb | T3 | csak találat, nem nyitottam meg | Vélemény-jellegű gyártói/blog írás, mért adat nélkül — nem használtam fel állítás forrásaként |
| The Prometheus Cardinality Bomb — OpenObserve blog | https://openobserve.ai/blog/prometheus-data-cardinality/ | T3 | csak találat, nem nyitottam meg | Gyártói blog, mért adat nélkül — nem használtam fel |
| Amazon Web Services Outage Caused By Memory Leak — TechCrunch | https://techcrunch.com/2012/10/27/amazon-web-services-outage-caused-by-memory-leak-and-failure-in-monitoring-alarm | T3 | csak találat, nem nyitottam meg | Újságírói másodforrás az AWS-incidenshez; helyette a hivatalos AWS-összefoglalót (T1) idéztem |
| SREcon24 Americas Conference Program — USENIX | https://www.usenix.org/conference/srecon24americas/program | T2 | WebSearch találat, program áttekintve, egyedi előadás nem található a témában | Kerestem mért adatot tartalmazó előadást a metrika-számról, nem találtam ilyet |



---

# SQ02 — Állapotellenőrzés (health check) tervezése egyfelhasználós, egygépes szolgáltatáshoz
## Meglátogatott és felderített linkek

| Cím | URL | Tier | Lekérés módja | Megjegyzés |
|---|---|---|---|---|
| Liveness, Readiness, and Startup Probes (concept, probes.md) | https://kubernetes.io/docs/concepts/workloads/pods/probes/ | T1 | WebFetch (élő oldal csak navigációt adott vissza; a végleges idézetek a hivatalos GitHub forrásfájlból lettek megerősítve) | Sikeres, tartalmat a nyers forrásfájlból nyertem ki |
| Pod Lifecycle | https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/ | T1 | WebFetch (élő oldal csak navigációt adott vissza) + nyers forrás | Sikeres a nyers forrásfájlból |
| Configure Liveness, Readiness and Startup Probes (task) | https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/ | T1 | WebFetch (élő oldal csak navigációt adott) + nyers forrás | Sikeres a nyers forrásfájlból |
| kubernetes/website — probes.md (nyers forrás) | https://raw.githubusercontent.com/kubernetes/website/main/content/en/docs/concepts/workloads/pods/probes.md | T1 | WebFetch | Sikeres, ez a fő idézetforrás a probe-okhoz |
| kubernetes/website — pod-lifecycle.md (nyers forrás) | https://raw.githubusercontent.com/kubernetes/website/main/content/en/docs/concepts/workloads/pods/pod-lifecycle.md | T1 | WebFetch | Sikeres |
| kubernetes/website — configure-liveness-readiness-startup-probes.md (nyers forrás) | https://raw.githubusercontent.com/kubernetes/website/main/content/en/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes.md | T1 | WebFetch | Sikeres, Caution/Note blokkok innen |
| r.jina.ai proxy a k8s oldalakhoz | https://r.jina.ai/https://kubernetes.io/... | — | WebFetch | SIKERTELEN — a lekérő eszköz elutasította proxy/relay szolgáltatásként ("Domain is a known web proxy/relay service and is blocked for this use case") |
| draft-inadarei-api-health-check (index) | https://datatracker.ietf.org/doc/draft-inadarei-api-health-check/ | T1 | WebFetch | Első kísérlet timeoutolt; ld. lent a /06/ verziót, ami sikerült |
| draft-inadarei-api-health-check-06 (státuszoldal) | https://datatracker.ietf.org/doc/draft-inadarei-api-health-check/06/ | T1 | WebFetch | Sikeres — "Expired Internet-Draft" |
| draft-inadarei-api-health-check-06 (teljes szöveg) | https://datatracker.ietf.org/doc/html/draft-inadarei-api-health-check-06 | T1 | WebFetch (2×) | Sikeres — abstract, mezőkészlet, státuszkódok |
| Amazon Builders' Library — Implementing health checks (HTML) | https://aws.amazon.com/builders-library/implementing-health-checks/ | T2 | WebFetch | 302-es átirányítás történt egy JS-renderelt landing oldalra (builder.aws.com), amelyből csak metaadat volt kinyerhető |
| builder.aws.com — Implementing health checks (átirányított cél) | https://builder.aws.com/content/3Ev53O39izHCtWLzp4XU6t8PC1O/implementing-health-checks | T2 | WebFetch | SIKERTELEN érdemi tartalom szempontjából — csak meta tag-ek |
| Implementing health checks — hivatalos PDF | https://d1.awsstatic.com/builderslibrary/pdfs/implementing-health-checks.pdf | T2 | WebFetch (3×) | Sikeres — ez lett a fő idézetforrás a 3. szakaszhoz |
| Model Context Protocol — Versioning | https://modelcontextprotocol.io/specification/versioning | T1 | WebFetch | Sikeres — jelenlegi verzió: 2026-07-28 |
| MCP — Ping (2025-06-18 verzió) | https://modelcontextprotocol.io/specification/2025-06-18/basic/utilities/ping | T1 | WebFetch | Sikeres |
| MCP — Ping (2025-03-26 verzió, kereséskor talált link) | https://spec.modelcontextprotocol.io/specification/draft/basic/utilities/ping/ | T1 | csak keresési találat, nem lekérve | Nem lekérve, redundáns a 2025-06-18 verzióval |
| MCP — Discovery (server/discover, 2026-07-28) | https://modelcontextprotocol.io/specification/2026-07-28/server/discover | T1 | WebFetch | Sikeres |
| MCP — Ping (2026-07-28, ellenőrzésül) | https://modelcontextprotocol.io/specification/2026-07-28/basic/utilities/ping | T1 | WebFetch | Az oldal a Key Changes dokumentumra irányított át tartalmilag; a `ping` eltávolítását a changelog + a séma-fájl közvetlen vizsgálata erősítette meg |
| MCP — Key Changes / changelog (2026-07-28) | https://modelcontextprotocol.io/specification/2026-07-28/changelog | T1 | WebFetch | Sikeres — "Remove `ping`..." idézet innen |
| modelcontextprotocol/modelcontextprotocol — schema.ts (2025-06-18) | https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/2025-06-18/schema.ts | T1 | WebFetch | Sikeres — PingRequest definíció |
| modelcontextprotocol/modelcontextprotocol — schema.ts (2026-07-28) | https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/2026-07-28/schema.ts | T1 | WebFetch | Sikeres — PingRequest HIÁNYZIK, DiscoverRequest/Result jelen van |
| freedesktop.org — sd_notify(3) | https://www.freedesktop.org/software/systemd/man/latest/sd_notify.html | T1 | WebFetch | SIKERTELEN — 403 Client Error |
| freedesktop.org — systemd.service(5) | https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html | T1 | WebFetch | SIKERTELEN — 403 Client Error |
| Arch Linux man pages — systemd.service(5) tükör | https://man.archlinux.org/man/systemd.service.5.en | T2 | WebFetch | Sikeres — WatchdogSec=, Type=notify idézetek innen (a freedesktop.org 403 miatt ez a helyettesítő forrás) |
| Arch Linux man pages — sd_notify(3) tükör | https://man.archlinux.org/man/sd_notify.3.en | T2 | WebFetch | Sikeres — WATCHDOG=1, WATCHDOG=trigger idézetek innen |
| Apple Developer — Creating Launch Daemons and Agents | https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html | T1 | WebFetch | Sikeres — hivatalos Apple-dokumentum |
| launchd.plist(5) man-oldal tükör | https://keith.github.io/xcode-man-pages/launchd.plist.5.html | T2 | WebFetch | Sikeres — KeepAlive, ThrottleInterval kulcsok |
| SQLite — Pragma statements (quick_check) | https://sqlite.org/pragma.html#pragma_quick_check | T1 | WebFetch | Sikeres |
| SQLite — Pragma statements (integrity_check) | https://sqlite.org/pragma.html#pragma_integrity_check | T1 | WebFetch | Sikeres |
| SQLite hivatalos fórum — "PRAGMA INTEGRITY_CHECK takes very long" | https://sqlite.org/forum/info/631e8968e70b35bc | T2 | WebFetch | Sikeres — valós idő-adatok nagy (4,2 GB) adatbázison |
| doobidoo/mcp-memory-service — db_health_check.py | https://raw.githubusercontent.com/doobidoo/mcp-memory-service/main/scripts/database/db_health_check.py | T3 | WebFetch | Sikeres — valós MCP-memória-szolgáltatás health-check gyakorlata (funkcionális SELECT, nem PRAGMA) |

---

**Megjegyzés a kutatás módszertanáról:** ez a kutatás a `deep-web-research` skillt egyetlen, már pontosan definiált al-kérdésre (SQ02, hat konkrét részkérdéssel) alkalmazta. A skill teljes többágenses (Sonnet-kereső-hullámok + Opus-szintézis) csővezetéke ebben a futtatási környezetben nem volt elérhető (nem állt rendelkezésre subagent-indító eszköz), ezért a skill saját, erre az esetre megadott degradált módban futott: egyetlen ügynök (én) végezte sorban a keresést, a lekérést és az idézetek összeállítását, közvetlenül elsődleges/hivatalos forrásokból (kubernetes.io + GitHub-forrás, datatracker.ietf.org, modelcontextprotocol.io + GitHub-séma, sqlite.org, developer.apple.com, valamint a systemd esetében a blokkolt freedesktop.org helyett annak Arch Linux man-oldal-tükre). Minden idézet a ténylegesen lekért oldal/fájl szövegéből származik, nem generált vagy emlékezetből felidézett szöveg.



---

# SQ03 — Üzemeltetési napló az audit naplótól elkülönítve: mit mond a szabványirodalom és a gyakorlat
## Meglátogatott és felderített linkek

| Cím | URL | Tier | Lekérés módja | Megjegyzés |
|---|---|---|---|---|
| RFC 5424 — The Syslog Protocol (datatracker) | https://datatracker.ietf.org/doc/html/rfc5424 | T1 | WebFetch | Súlyossági táblázat első lekérése, tájékozódásra |
| RFC 5424 — The Syslog Protocol (rfc-editor, nyers szöveg) | https://www.rfc-editor.org/rfc/rfc5424.txt | T1 | WebFetch (2×) | Elsődleges, hivatalos szöveg; a "not normative but often used" idézet innen |
| RFC 3164 — The BSD syslog Protocol | https://www.rfc-editor.org/rfc/rfc3164.txt | T1 | WebFetch | Az elődszabvány, ugyanaz a 8 szint; nem tartalmazza a "szubjektív" megfogalmazást explicit módon |
| NIST SP 800-92 — Guide to Computer Security Log Management (hivatalos PDF) | https://nvlpubs.nist.gov/nistpubs/legacy/SP/nistspecialpublication800-92.Pdf | T1 | WebFetch (2×) | Log-forrás kategorizálás, audit rekord definíció, 3.1 szakasz idézet |
| OWASP Logging Cheat Sheet (renderelt oldal) | https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html | T1 | WebFetch | Purpose szakasz, Data to exclude lista |
| OWASP Logging Cheat Sheet (nyers Markdown forrás, GitHub) | https://raw.githubusercontent.com/OWASP/CheatSheetSeries/master/cheatsheets/Logging_Cheat_Sheet.md | T1 | WebFetch (2×) | Verbátim ellenőrzés a renderelt oldal ellen, egyezik |
| PCI DSS v4.0.1 hivatalos PDF (pcisecuritystandards.org) | https://docs-prv.pcisecuritystandards.org/PCI%20DSS/Standard/PCI-DSS-v4_0_1.pdf | T1 | WebFetch — **SIKERTELEN (403)** | A hivatalos domain elutasította a lekérést |
| PCI DSS v4.0.1 PDF, Wayback Machine tükör | https://web.archive.org/web/2024/https://docs-prv.pcisecuritystandards.org/PCI%20DSS/Standard/PCI-DSS-v4_0_1.pdf | T1 (elérhetetlen) | WebFetch — **SIKERTELEN (blokkolva)** | A rendszer blokkolta a lekérést |
| PCI DSS v4.0.1 PDF, egyetemi tükör (Middlebury) | https://www.middlebury.edu/sites/default/files/2025-01/PCI-DSS-v4_0_1.pdf | T2 | WebFetch — **RÉSZLEGES** | Csak 1-42. oldal jött le, a 10. követelmény (~236. o.) nem volt elérhető |
| PCI SSC — Summary of Changes v3.2.1→v4.0 | https://listings.pcisecuritystandards.org/documents/PCI-DSS-v3-2-1-to-v4-0-Summary-of-Changes-r1.pdf | T1 | WebFetch | Csak a 10.5.1 azonosító áthelyezését erősíti meg, konkrét számot nem tartalmaz |
| NXLog blog — PCI DSS 4.0 logging | https://nxlog.co/news-and-blog/posts/pci-dss-log-collection-compliance | T2 | WebFetch | 10.5.1 paraphrase, nem elsődleges idézet — a cikk maga is jelzi, hogy ez összefoglalás |
| RSI Security blog — PCI DSS Requirement 10 | https://blog.rsisecurity.com/tracking-and-monitoring-under-pci-dss-requirement-10/ | T3 | WebFetch | Paraphrase, nem elsődleges idézet |
| BasisTheory blog — PCI DSS Requirement 10 | https://blog.basistheory.com/pci-dss-requirement-10 | T2 | WebFetch | Paraphrase, a cikk explicit jelzi, hogy nem közvetlen idézet a szabványból |
| 12factor.net — XI. Logs | https://12factor.net/logs | T1 | WebFetch | Hivatalos Twelve-Factor App szöveg; a lekérés összefoglalva adta vissza, nem nyers HTML-ként |
| OpenTelemetry — Logs Data Model | https://opentelemetry.io/docs/specs/otel/logs/data-model/ | T1 | WebFetch | Stable állapot, mezőtáblázat |
| OpenTelemetry specifikáció forrás (GitHub, main ág) | https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/logs/data-model.md | T1 | WebFetch | SeverityNumber megfeleltetési táblázat |
| logrotate(8) man oldal (man7.org) | https://man7.org/linux/man-pages/man8/logrotate.8.html | T1 | WebFetch | `rotate` alapértéke 0, size/daily/weekly leírások |
| journald.conf(5) man oldal (freedesktop.org, legújabb) | https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html | T1 | WebFetch — **SIKERTELEN (403)** | A hivatalos systemd-domain elutasította a lekérést |
| journald.conf(5) man oldal (man7.org tükör) | https://www.man7.org/linux/man-pages/man5/journald.conf.5.html | T1 | WebFetch (2×) | Sikeres alternatíva; SystemMaxUse, SystemMaxFileSize, SystemMaxFiles, MaxFileSec, MaxRetentionSec alapértékek innen |
| Forgejo — Logging Configuration (hivatalos dokumentáció) | https://forgejo.org/docs/latest/admin/troubleshooting/logging/ | T1 | WebFetch | Szintek, alapértelmezett console mód, beépített forgatás alapértékei |
| Gitea — Logging Configuration (hivatalos dokumentáció) | https://docs.gitea.com/administration/logging-config/ | T1 | WebFetch | Megerősíti a Forgejo-val azonos rendszert |
| Miniflux — Configuration Parameters (hivatalos dokumentáció) | https://miniflux.app/docs/configuration.html | T1 | WebFetch | LOG_LEVEL/LOG_FILE/LOG_FORMAT alapértékek |
| Syncthing — Command Line Operation (hivatalos dokumentáció) | https://docs.syncthing.net/users/syncthing.html | T1 | WebFetch | --log-file, --log-level, --log-max-size, --log-max-old-files |
| Vaultwarden — Logging (hivatalos wiki) | https://github.com/dani-garcia/vaultwarden/wiki/Logging | T1 | WebFetch | Alapból stdout, LOG_FILE/LOG_LEVEL, nincs beépített forgatás |
| Apache Log4j2 — Performance (hivatalos projektoldal) | https://logging.apache.org/log4j/2.x/manual/performance.html | T1 | WebFetch | Csak minőségi állítások, konkrét szám nélkül |
| Logback — Performance (hivatalos projektoldal) | https://logback.qos.ch/performance.html | T1 | WebFetch | Szál-alapú áteresztőképesség-összehasonlítás, nem általános "hányszor lassabb" mutató |
| Nearform — The Cost of Logging in 2022 | https://nearform.com/insights/the-cost-of-logging-in-2022/ | T2 | WebFetch | Konkrét mért kérés/mp számok, Node.js/pino ökoszisztémára korlátozva |
| CNIL — recommandation relative aux mesures de journalisation | https://www.cnil.fr/fr/la-cnil-publie-une-recommandation-relative-aux-mesures-de-journalisation | T1 | WebFetch | Francia nemzeti felügyeleti hatóság hivatalos állásfoglalása, konkrét megőrzési tartományokkal |
| EDPB — site:edpb.europa.eu keresés naplózási megőrzésre | (keresés, nincs egyetlen releváns URL) | — | WebSearch | Nem hozott releváns EU-szintű naplómegőrzési iránymutatást |
| ICO — Records management and security (keresési találat, nem lekérve) | https://ico.org.uk/for-organisations/advice-and-services/audits/data-protection-audit-framework/toolkits/accountability/records-management-and-security/ | T1 (nem ellenőrzött) | Csak WebSearch találat, nem fetch-elve | Idő hiányában nem lett részletesen lekérve; potenciális további forrás egy jövőbeli körhöz |



---

# SQ04 — Indulás, újraindítás és összeomlás utáni helyreállás
## Meglátogatott és felderített linkek

| Cím | URL | Tier | Lekérés módja | Megjegyzés |
|---|---|---|---|---|
| SQLite: Write-Ahead Logging | https://sqlite.org/wal.html | T1 | curl (nyers HTML letöltve, grep-elve) | Sikeres; recovery, checkpoint, -shm, EXCLUSIVE mód |
| SQLite: Atomic Commit In SQLite | https://sqlite.org/atomiccommit.html | T1 | curl (nyers HTML) | Sikeres; hot journal teljes algoritmus |
| SQLite: Database File Format (fileformat2) | https://sqlite.org/fileformat2.html | T1 | curl (nyers HTML) | Sikeres; WAL frame checksum, wal-index tranziens jelleg |
| SQLite FTS5 Extension | https://sqlite.org/fts5.html | T1 | curl (nyers HTML) | Sikeres; 'rebuild' parancs, nincs sebességszám |
| SQLite C Interface: sqlite3_close/close_v2 | https://sqlite.org/c3ref/close.html | T1 | curl (nyers HTML) | Sikeres; zombie-állapot, tranzakció rollback zárásnál |
| systemd.service man-oldal forrása (upstream XML) | https://raw.githubusercontent.com/systemd/systemd/main/man/systemd.service.xml | T1 | curl (GitHub raw) | Sikeres; Restart=, RestartSec=, TimeoutStopSec= |
| systemd.unit man-oldal forrása (upstream XML) | https://raw.githubusercontent.com/systemd/systemd/main/man/systemd.unit.xml | T1 | curl (GitHub raw) | Sikeres; StartLimitIntervalSec=, StartLimitBurst=, Wants=/Requires=/After=/Before= |
| systemd-system.conf man-oldal forrása | https://raw.githubusercontent.com/systemd/systemd/main/man/systemd-system.conf.xml | T1 | curl (GitHub raw) | Sikeres; DefaultStartLimitIntervalSec=10s, DefaultStartLimitBurst=5, DEFAULT_TIMEOUT_SEC entitás |
| systemd meson_options.txt (build-alapértékek) | https://raw.githubusercontent.com/systemd/systemd/main/meson_options.txt | T1 | curl (GitHub raw) | Sikeres; default-timeout-sec = 90 |
| systemd.resource-control man-oldal forrása | https://raw.githubusercontent.com/systemd/systemd/main/man/systemd.resource-control.xml | T1 | curl (GitHub raw) | Sikeres; CPUQuota=, MemoryMax= (cgroup-alapú kvóta) |
| systemd custom-entities.ent.in | https://raw.githubusercontent.com/systemd/systemd/main/man/custom-entities.ent.in | T1 | curl (GitHub raw) | Sikeres; DEFAULT_TIMEOUT_SEC entitás definíciója (build-time template) |
| Debian manpages: systemd.service(5) | https://manpages.debian.org/testing/systemd/systemd.service.5.en.html | T2 | curl | Sikeres; keresztellenőrzés, systemd 260.1 (csomag 261.2-1) |
| Debian manpages: systemd.unit(5) | https://manpages.debian.org/testing/systemd/systemd.unit.5.en.html | T2 | curl | Sikeres; keresztellenőrzés |
| freedesktop.org systemd.service man (latest) | https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html | T1 (megcélzott) | curl | **Sikertelen** — bot-elhárítási kihívás ("Checking you are not a bot"), nem kerülve meg |
| freedesktop.org systemd.unit man (latest) | https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html | T1 (megcélzott) | curl | **Sikertelen** — ugyanaz a bot-elhárítás |
| launchd.plist(5) man-oldal | https://www.manpagez.com/man/5/launchd.plist/ | T2 | curl | Sikeres; KeepAlive, ThrottleInterval=10s, ExitTimeOut=20s, SoftResourceLimits/HardResourceLimits |
| ss64.com launchd.plist | https://ss64.com/mac/launchd.plist.html | T2 (megcélzott) | curl | **Sikertelen** — a válasz gyanúsan rövid (4,3 KB), feltehetően blokkolt/JS-védett |
| opensource.apple.com launchd forrás (találgatott útvonal) | https://opensource.apple.com/source/launchd/launchd-842.92.1/... | T1 (megcélzott) | curl | **Sikertelen** — 404, a pontos build-útvonal nem volt ismert |
| Elastic: Red or yellow cluster health status | https://www.elastic.co/guide/en/elasticsearch/reference/current/red-yellow-cluster-status.html | T1 | curl | Sikeres; degradált kiszolgálás piros/sárga állapotban, 1 perces allokációs késleltetés |
| OpenSearch: Cluster Health API | https://docs.opensearch.org/latest/api-reference/cluster-api/cluster-health/ | T1 | curl | Sikeres; green/yellow/red példaválaszok |
| OpenSearch: Recovery (Index APIs) | https://docs.opensearch.org/latest/api-reference/index-apis/recover/ | T1 | curl | Sikeres; INIT/INDEX/VERIFY_INDEX/TRANSLOG/FINALIZE/DONE állapotgép |
| Meilisearch: Tasks and asynchronous operations | https://www.meilisearch.com/docs/learn/async/asynchronous_operations | T1 | curl | Sikeres; enqueued/processing/succeeded/failed/canceled |
| Typesense API dokumentáció (Health szakasz) | https://typesense.org/docs/30.2/api/ | T1 | curl | Sikeres; nincs "importálás alatt" állapot a /health válaszban |
| Typesense: Cluster Operations | https://typesense.org/docs/30.2/api/cluster-operations.html | T1 | curl | Sikeres; snapshot/backup mechanizmus |
| GitHub: typesense/typesense Issue #665 | https://github.com/typesense/typesense/issues/665 | T2/T3 | WebFetch (curl blokkolva/üres volt) | Sikeres (WebFetch-en át); közösségi hibajelentés, nem hivatalos állásfoglalás |



---

# SQ05 — Mikor beteg egy SQLite adatbázis, és hogyan vesszük észre?
## Meglátogatott és felderített linkek

| Cím | URL | Tier | Lekérés módja | Megjegyzés |
|---|---|---|---|---|
| How To Corrupt An SQLite Database File | https://www.sqlite.org/howtocorrupt.html | T1 | WebFetch (sikeres, teljes tartalom) | Fő forrás az 1. szakaszhoz; 8 fő fejezet, ~25 alpont |
| Hints On Using SQLite On A Network Filesystem | https://www.sqlite.org/useovernet.html | T1 | WebFetch (két menetben, teljes szöveg ellenőrizve) | NFS/hálózati fájlrendszer kockázatok; nincs Dropbox/iCloud/OneDrive/SMB említés |
| Pragma statements supported by SQLite (integrity_check, quick_check, foreign_key_check) | https://www.sqlite.org/pragma.html#pragma_integrity_check | T1 | WebFetch (sikeres) | 2. szakasz fő forrása |
| Pragma statements — foreign_key_check | https://www.sqlite.org/pragma.html#pragma_foreign_key_check | T1 | WebFetch (sikeres, ugyanazon lekérésben) | Idegenkulcs-ellenőrzés leírása |
| Pragma statements — PRAGMA optimize | https://www.sqlite.org/pragma.html#pragma_optimize | T1 | WebFetch (sikeres) | 6. szakasz fő forrása, MASK-táblázattal |
| Pragma statements — PRAGMA busy_timeout | https://www.sqlite.org/pragma.html#pragma_busy_timeout | T1 | WebFetch (kétszer, sikeres, de nem tartalmaz konkrét alapértelmezett számot) | Nincs numerikus default a pragma-oldalon |
| Pragma statements — PRAGMA wal_autocheckpoint / wal_checkpoint | https://www.sqlite.org/pragma.html#pragma_wal_autocheckpoint | T1 | WebFetch (sikeres) | 1000 oldalas alapérték; PASSIVE/FULL/RESTART/TRUNCATE leírás |
| Pragma statements — teljes oldal (visszatérési oszlopok ellenőrzése) | https://www.sqlite.org/pragma.html | T1 | WebFetch — **sikertelen / nem meggyőző**, a válasz csonkolt volt, illetve egy korábbi lekérés ellentmondásos szöveget adott | wal_checkpoint visszatérési oszlopainak pontos leírását emiatt NEM használtuk fel |
| Query Language Understood by SQLite — ANALYZE | https://www.sqlite.org/lang_analyze.html | T1 | WebFetch (sikeres) | ANALYZE újrafuttatási ajánlás, PRAGMA optimize kapcsolat |
| Write-Ahead Logging | https://www.sqlite.org/wal.html | T1 | WebFetch (több menetben, sikeres) | wal_autocheckpoint default, checkpoint starvation, WAL-méret kérdések |
| c3ref: sqlite3_wal_checkpoint_v2 (checkpoint mode konstansok) | https://www.sqlite.org/c3ref/wal_checkpoint_v2.html | T1 | WebFetch (sikeres) | PASSIVE/FULL/RESTART/TRUNCATE C-szintű, részletesebb leírása |
| c3ref: sqlite3_busy_timeout | https://www.sqlite.org/c3ref/busy_timeout.html | T1 | WebFetch (sikeres) | Nem közöl numerikus defaultot |
| c3ref: sqlite3_busy_handler (Register A Callback To Handle SQLITE_BUSY Errors) | https://www.sqlite.org/c3ref/busy_handler.html | T1 | WebFetch (sikeres) | Kulcsforrás a holtpont-esethez és a NULL alapértelmezett callbackhez |
| Result and Error Codes (rescode.html) | https://www.sqlite.org/rescode.html | T1 | WebFetch (sikeres) | SQLITE_BUSY, SQLITE_BUSY_RECOVERY, SQLITE_BUSY_SNAPSHOT pontos szövege |
| File Locking And Concurrency In SQLite Version 3 | https://www.sqlite.org/lockingv3.html | T1 | WebFetch (sikeres, de nem tartalmazott releváns holtpont-/SQLITE_LOCKED szöveget) | Negatív találat — dokumentálva az „Amire nincs publikált válasz” szakaszban |
| Frequently Asked Questions (FAQ) | https://www.sqlite.org/faq.html | T1 | WebFetch (sikeres, de nem tartalmazott holtpont-/busy_timeout részletet) | Csak a Q5 SQLITE_BUSY alapmondatát tartalmazza |
| SQLite Procedures — Help: test-integrity (Fossil, sqlite.org saját Fossil-repója) | https://sqlite.org/mgmt/help?cmd=test-integrity | T1 | WebFetch (sikeres) | Fossil `test-integrity` parancs teljes súgója, `--db-only`/`--quick` kapcsolók |
| Fossil: Help: test-integrity (fossil-scm.org) | https://www.fossil-scm.org/home/help?cmd=test-integrity | T1 | WebFetch — **sikertelen, robots.txt tiltja** | Helyette a sqlite.org/mgmt tükörpéldányát használtuk (azonos szoftver, azonos tartalom) |
| Litestream — Tips & Caveats | https://litestream.io/tips/ | T1 | WebFetch (két menetben, sikeres) | Manuális `PRAGMA integrity_check` ajánlás helyreállítás után |
| Litestream — Troubleshooting | https://litestream.io/docs/troubleshooting/ | T1 | WebFetch (két menetben, sikeres) | „Corruption Detection” és „WAL Growth and Checkpoint Blocking” szakaszok |
| home-assistant/core PR #37949 (Automatically recover when the sqlite3 database is malformed or corrupted) | https://github.com/home-assistant/core/pull/37949 | T1 | WebFetch (két menetben, sikeres) | `validate_sqlite_database()`, `PRAGMA QUICK_CHECK`, indításkori automatikus helyreállítás |
| home-assistant/core — recorder/util.py (dev ág) | https://github.com/home-assistant/core/blob/dev/homeassistant/components/recorder/util.py | T1 | WebFetch (sikeres, de a PR-ben leírt explicit PRAGMA-hívást nem találtuk meg benne) | Aktualitási bizonytalanság — lásd „Amire nincs publikált válasz” |
| home-assistant.io — Recorder integráció dokumentációja | https://github.com/home-assistant/home-assistant.io/blob/12e29a81f6a75e909e2cc1e5e06644bd85c5e74c/source/_integrations/recorder.markdown | T2 | WebFetch (sikeres, negatív találat) | Nem tartalmaz integritás-ellenőrzési dokumentációt |
| datasette-verify (PyPI) | https://pypi.org/project/datasette-verify/ | T2 | WebFetch (sikeres) | Harmadik fél bővítmény, nem `integrity_check`-alapú |
| Datasette hivatalos dokumentáció (docs.datasette.io) | https://docs.datasette.io/ | T1 | WebSearch (csak találati lista, nincs releváns integritás-ellenőrzési oldal azonosítva) | Nem került elő natív integritás-ellenőrzési funkció |
| SQLite User Forum — „Why is PRAGMA busy_timeout per default 0?” | https://sqlite.org/forum/info/7e456bf5544ab128 | T3 | WebSearch (csak cím/link, nem olvastuk teljes egészében) | Közösségi megerősítés arra, hogy a gyakorlati alapérték 0; NEM használtuk elsődleges forrásként a jelentésben |
| SQLite User Forum — „database is locked”: detecting deadlock vs. busy timeout? | https://sqlite.org/forum/forumpost/4350638e78869137 | T3 | WebSearch (csak cím/link) | Kontextusigazolás, nem idézve a jelentésben |



---

# SQ06 — Riasztás egyszemélyes rendszerben és a csendes meghibásodás
## Meglátogatott és felderített linkek

| Cím | URL | Tier | Lekérés módja | Megjegyzés |
|---|---|---|---|---|
| My Philosophy on Alerting (Rob Ewaschuk, eredeti Google Doc) | https://docs.google.com/document/d/199PqyG3UsyXlwieHaqbGiWVa8eMWi8zzAn0YfcApr8Q/mobilebasic | T1 | curl (export=txt) teljes szöveg letöltve és ellenőrizve | A teljes, 172 soros dokumentumot letöltöttem és manuálisan ellenőriztem az idézeteket. |
| Google SRE Book — Monitoring Distributed Systems (6. fejezet) | https://sre.google/sre-book/monitoring-distributed-systems/ | T1 | curl + HTML→szöveg konverzió, grep-pel ellenőrizve | Ewaschuk saját fejezete a könyvben. |
| Google SRE Book — Being On-Call (11. fejezet) | https://sre.google/sre-book/being-on-call/ | T1 | curl + HTML→szöveg konverzió, grep-pel ellenőrizve | Konkrét óraszám (6 óra/incidens) és stresszhormon-idézet innen. |
| Google SRE Book — Practical Alerting (10. fejezet) | https://sre.google/sre-book/practical-alerting/ | T1 | curl + HTML→szöveg konverzió | Elsősorban a Borgmon technikai részleteiről szól; a "May the queries flow, and the pager stay silent" mottó innen. |
| Google SRE Book — Effective Troubleshooting | https://sre.google/sre-book/effective-troubleshooting/ | T1 | curl + grep (negatív találat) | Nem tartalmazza a stresszhormon-idézetet — az a Being On-Call fejezetben van, nem itt. |
| Google SRE Book — Table of Contents | https://sre.google/sre-book/table-of-contents/ | T1 | WebFetch | Fejezetsorrend azonosítására. |
| PubMed — Cvach 2012, "Monitor alarm fatigue: an integrative review" | https://pubmed.ncbi.nlm.nih.gov/22839984/ | T1 | WebFetch (csak metaadat jött vissza, absztrakt nem) | A cikk létezését és tárgyát megerősíti; a teljes absztraktot nem sikerült kinyerni. |
| AAMI Array — Cvach 2012 teljes cikk oldala | https://array.aami.org/doi/full/10.2345/0899-8205-46.4.268 | T1 | WebFetch — 403 hiba | Sikertelen lekérés (fizetős/hozzáférés-korlátozott). |
| AHRQ PSNet — Reducing the Safety Hazards of Monitor Alert and Alarm Fatigue | https://psnet.ahrq.gov/perspective/reducing-safety-hazards-monitor-alert-and-alarm-fatigue | T2 | WebFetch | Kormányzati szakmai testület, lektorált irodalmat szintetizál; a 80–99%-os szám forrása. |
| The Joint Commission — Sentinel Event Alert #50 (hivatalos PDF) | https://digitalassets.jointcommission.org/api/public/content/f65e5c9df2b94000a99445e0a7877007 | T1 | WebFetch | Szabályozói dokumentum; 85–99%-os szám és 98 eset/80 haláleset statisztika innen. |
| healthchecks.io — Documentation (főoldal) | https://healthchecks.io/docs/ | T1 | WebFetch | A dead man's switch modell alapleírása. |
| healthchecks.io — Monitoring Cron Jobs | https://healthchecks.io/docs/monitoring_cron_jobs/ | T1 | WebFetch | Konkrét cron-ping mechanizmus leírása. |
| healthchecks.io — Configuring Notifications | https://healthchecks.io/docs/configuring_notifications/ | T1 | WebFetch | Csatornalista (email, SMS, WhatsApp, telefon, Slack, Pushover, PagerDuty, Splunk On-Call, Opsgenie, PagerTree). |
| Cronitor — Heartbeat Monitoring (hivatalos docs) | https://cronitor.io/docs/heartbeat-monitoring | T1 | WebFetch | Hivatalos technikai dokumentáció. |
| Cronitor — Heartbeat Monitoring (marketing oldal) | https://cronitor.io/heartbeat-monitoring | T2 | WebFetch | Ugyanaz a tartalom tömörebben, marketing megfogalmazásban. |
| Prometheus — Query functions, `absent()` | https://prometheus.io/docs/prometheus/latest/querying/functions/#absent | T1 | WebFetch | Hivatalos PromQL-referencia. |
| Prometheus Operator / kube-prometheus runbooks — Watchdog | https://runbooks.prometheus-operator.dev/runbooks/general/watchdog/ | T1 | WebFetch | Közösségi (nem prometheus.io mag-) hivatalos runbook; a különbséget a jelentésben jeleztem. |
| GitHub — louislam/uptime-kuma, Issue #284 (Full List of Supported Notifications) | https://github.com/louislam/uptime-kuma/issues/284 | T2 | WebFetch | Karbantartó által kurátorolt, de issue-szálban lévő lista, nem formális docs-oldal. |
| GitHub — louislam/uptime-kuma wiki, Notification Methods | https://github.com/louislam/uptime-kuma/wiki/Notification-Methods | T1 | WebFetch | Hivatalos projekt-wiki, de a konkrét listát csak linkeli tovább. |
| GitHub — louislam/uptime-kuma, notification-providers könyvtár | https://github.com/louislam/uptime-kuma/tree/master/server/notification-providers | T1 | WebFetch — ROBOTS_DISALLOWED hiba | Sikertelen lekérés (robots.txt tiltás); a GitHub API is elutasította ebben a környezetben. |
| GitHub API — repos/louislam/uptime-kuma/contents/... | https://api.github.com/repos/louislam/uptime-kuma/contents/server/notification-providers | T1 | curl — hozzáférés-hiba ("not enabled for this session") | Sikertelen lekérés, a környezet nem engedélyezte a GitHub API elérést. |
| GitHub — caronc/apprise wiki, Notify_dbus | https://github.com/caronc/apprise/wiki/Notify_dbus | T1 | WebFetch | Hivatalos forrás az asztali (dbus/Gnome/KDE) értesítésről és annak "same system" korlátjáról. |
| docsmith.aigne.io — Uptime Kuma notification providers tükör | https://docsmith.aigne.io/docs/uptime-kuma/backend-notification-providers-4fed4a | T3 | WebFetch — üres/JS-igényes tartalom | Sikertelen tartalomkinyerés (JavaScript-alapú oldal). |
| NIST SP 800-34 Rev. 1 (Contingency Planning Guide) | https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-34r1.pdf | T1 | curl letöltés + pdftotext + grep, sorszám szerint ellenőrizve | Teljes PDF letöltve és feldolgozva; a backup-teszt idézetek pontos sorhelye rögzítve. |
| CSF Tools — CIS Control 11.5 (Test Data Recovery) | https://csf.tools/reference/critical-security-controls/v8-1/csc-11/csc-11-5/ | T2 | WebFetch | Másodlagos forrás a CIS Controls v8 szövegére (nem a hivatalos CIS PDF, de a szöveg konzisztens az ismert CIS-megfogalmazással). |
| AWS Well-Architected — REL09-BP04 | https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_backing_up_data_periodic_recovery_testing_data.html | T2 | WebFetch | Gyártói (AWS) hivatalos keretrendszer-dokumentáció. |
| restic — Working with repositories (check parancs) | https://restic.readthedocs.io/en/stable/045_working_with_repos.html | T1 | WebFetch | Hivatalos projekt-dokumentáció. |
| BorgBackup — borg check dokumentáció | https://borgbackup.readthedocs.io/en/stable/usage/check.html | T1 | WebFetch | Hivatalos projekt-dokumentáció. |
| Kopia — Verifying Validity of Snapshots/Repositories | https://kopia.io/docs/advanced/consistency/ | T1 | WebFetch | Hivatalos projekt-dokumentáció, konkrét napi/havi gyakorisági ajánlással. |
| pingfatigue.com/research | https://pingfatigue.com/research | T3 | WebFetch | Tematikus gyűjtőoldal; a lektorált IT-specifikus irodalom hiányának közvetett megerősítésére használva, nem elsődleges forrásként. |
| paulsprogrammingnotes.com — A dead man's switch for a single-host monitoring stack | https://www.paulsprogrammingnotes.com/2026/07/dead-mans-switch-single-host-monitoring.html | T3 | WebFetch | Egyetlen konkrét, releváns anekdota a 6. ponthoz. |
| MakeUseOf — I replaced all my server email alerts with push notifications | https://www.makeuseof.com/i-replaced-all-my-server-email-alerts-with-push-notifications-i-actually-read-them-now/ | T3 | Csak keresési találatként azonosítva, nem fetch-elve | Anekdota-szintű véleménycikk, csak a hiány dokumentálására hivatkozva. |
| Derdack — Push notifications are not reliable for critical alerting | https://www.derdack.com/push-notifications-are-not-reliable-for-critical-alerting/ | T2 (gyártói) | Csak keresési találatként azonosítva, nem fetch-elve | Riasztó-szoftver gyártó marketingérvelése, nem mérés. |
| PagerDuty — State of Digital Operations | https://www.pagerduty.com/state-of-digital-ops/ | T2 | Csak keresési találatként azonosítva | Iparági, önbevallásos felmérés, nem lektorált kutatás. |



---

# ELL01 — Az MCP `ping` eltávolításának ellenőrzése
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



---

# ELL02 — Folyamatfelügyeleti alapértékek ellenőrzése
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



---

# ELL03 — SQLite állítások ellenőrzése
## Meglátogatott és felderített linkek

| Cím | URL | Tier | Lekérés módja | Megjegyzés |
|---|---|---|---|---|
| SQLite PRAGMA Statements | https://www.sqlite.org/pragma.html | T0 | `curl` (nyers HTML) | quick_check, integrity_check, busy_timeout, wal_autocheckpoint, page_size, journal_mode, secure_delete szakaszok |
| Write-Ahead Logging | https://www.sqlite.org/wal.html | T0 | `curl` (nyers HTML) | 3.1 Automatic Checkpoint és 6. Avoiding Excessively Large WAL Files szakaszok |
| VACUUM | https://www.sqlite.org/lang_vacuum.html | T0 | `curl` (nyers HTML) | Teljes oldal grep-elve journal_mode/page_size/auto_vacuum/transaction/snapshot kulcsszavakra |
| The Online Backup API | https://www.sqlite.org/backup.html | T0 | `curl` (nyers HTML) | 3.1 File and Database Connection Locking szakasz |
| sqlite3_busy_timeout (C API) | https://www.sqlite.org/c3ref/busy_timeout.html | T0 | `curl` (nyers HTML) | Nincs numerikus alapérték megadva |
| sqlite3_busy_handler (C API) | https://www.sqlite.org/c3ref/busy_handler.html | T0 | `curl` (nyers HTML) | "The default busy callback is NULL." |
| Command Line Shell For SQLite | https://www.sqlite.org/cli.html | T0 | `curl` (nyers HTML) | `.timeout` parancs leírása, nincs alapérték megadva |
| SQLite forráskód: `src/vacuum.c` | https://github.com/sqlite/sqlite/blob/master/src/vacuum.c | T0 | `curl` (raw.githubusercontent.com, hivatalos csak-olvasható git tükör) | "output file already exists", tranzakció-ellenőrzés, aCopy meta-lista (page_size/auto_vacuum/user_version/application_id öröklődés) |
| SQLite forráskód: `src/shell.c.in` | https://github.com/sqlite/sqlite/blob/master/src/shell.c.in | T0 | `curl` (raw.githubusercontent.com, hivatalos csak-olvasható git tükör) | Az egyetlen `sqlite3_busy_timeout()` hívás a `.timeout` meta-parancsban van, `open_db()`-ben nincs |
| SQLite hivatalos Fossil forráskód-böngésző (`sqlite.org/src`) | https://sqlite.org/src/finfo?name=src/shell.c.in | T0 | `curl` — **sikertelen**, robot-elhárító JS-kihívás | Ezért a GitHub-tükröt használtam helyette a forráskód-ellenőrzéshez |
| SQLite PRAGMA page_size | https://www.sqlite.org/pragma.html#pragma_page_size | T0 | ugyanaz a `pragma.html` letöltés | 4096 bájtos alapértelmezett lapméret (3.12.0 óta) igazolásához |
| SQLite PRAGMA journal_mode | https://www.sqlite.org/pragma.html#pragma_journal_mode | T0 | ugyanaz a `pragma.html` letöltés | "The DELETE journaling mode is the default." — közvetett bizonyíték a 4. állításhoz |

*(StackOverflow vagy egyéb T3 forrás egyik állítás ellenőrzéséhez sem volt szükséges — minden kérdésre elsődleges forrásból található válasz vagy explicit dokumentációs csend.)*
