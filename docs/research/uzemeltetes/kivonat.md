# Kivonat — üzemeltetés (monitorozás, állapotellenőrzés, naplózás, indulás, SQLite-egészség, riasztás)

Kutatási egységenként, szó szerinti idézetekkel. A linkek külön a `linkek.md`-ben.

---



---

# SQ01 — Mit érdemes figyelni egy egyfelhasználós, önüzemeltetett szolgáltatásnál?

Ez a kutatás egyetlen ügynök által, szekvenciális web-keresésekkel és forrás-lekérésekkel készült (nem a `deep-web-research` skill teljes, párhuzamos Sonnet-keresés + Opus-szintézis pipeline-jával, mert ez a munkamenet nem fér hozzá alügynök-indító eszközhöz) — ez a módszertani eltérés a skill saját szabálya szerint itt rögzítendő. A kanonikus monitorozási keretrendszerek (Google SRE „Four Golden Signals”, Brendan Gregg USE módszere, Tom Wilkie RED módszere) mindegyike explicit, saját szavaival korlátozza a hatókörét: a Google SRE könyv kifejezetten figyelmeztet, hogy a monitorozás bonyolultsága önmagában is hibaforrás és karbantartási teher lehet, és hogy egy 10-12 fős SRE csapatnak jellemzően 1-2 embere foglalkozik kizárólag a monitorozó rendszerrel. A vizsgált egybináris, önüzemeltetett projektek (Gitea, Forgejo, Miniflux, Jellyfin, Immich, Syncthing) többsége rendelkezik natív Prometheus `/metrics` végponttal, de ez — a Syncthing kivételével — mindenhol **alapból ki van kapcsolva**, és a Jellyfin dokumentációja ezt kifejezetten biztonsági okkal indokolja. Két projekt (Vaultwarden, Paperless-ngx) esetében a karbantartók **explicit elutasították** a natív metrika-végpont beépítését, biztonsági felület-növekedésre és karbantartási teherre hivatkozva. Mérésen alapuló, hiteles forrást arra, hogy „hány metrika után válik használhatatlanná” egy monitoring rendszer, **nem találtam** — ez a kutatás egyik legfontosabb negatív eredménye. A Prometheus hivatalos dokumentációja pontos számot ad a tárhelyigényről (1-2 bájt/minta, 15 napos alapértelmezett megőrzés), az OpenTelemetry Collector hivatalos dokumentációja viszont **nem** ad konkrét memória/CPU számot minimális telepítésre. A valós idejű riasztás helyettesítésére nincs formális szakirodalom kifejezetten egyfelhasználós rendszerekre, de a Google SRE könyv saját súlyossági hierarchiája (page/ticket/email alert) és a „dead man's switch” minta (pl. healthchecks.io) analóg, jól dokumentált gyakorlati mintát ad.

## 1. A kanonikus keretrendszerek és a saját érvényességi körük

### 1.1 Google SRE Book — „Monitoring Distributed Systems” (Négy arany jelzés)

Forrás: https://sre.google/sre-book/monitoring-distributed-systems/ (Tier: **T1** — Google hivatalos, publikált könyvfejezete)

A négy arany jelzés definíciója:

> "The four golden signals of monitoring are latency, traffic, errors, and saturation. If you can only measure four metrics of your user-facing system, focus on these four."

A négy jelzés egyenként:

> "Latency — The time it takes to service a request. It's important to distinguish between the latency of successful requests and the latency of failed requests."

> "Traffic — A measure of how much demand is being placed on your system, measured in a high-level system-specific metric."

> "Errors — The rate of requests that fail, either explicitly (e.g., HTTP 500s), implicitly (for example, an HTTP 200 success response, but coupled with the wrong content), or by policy."

> "Saturation — How 'full' your service is. A measure of your system fraction, emphasizing the resources that are most constrained (e.g., in a memory-constrained system, show memory; in an I/O-constrained system, show I/O)."

**A könyv saját maga mondja ki, mikor NEM éri meg a monitorozás komplexitása** — ez a „As Simple as Possible, No Simpler” szakasz lényege:

> "Piling all these requirements on top of each other can add up to a very complex monitoring system... The sources of potential complexity are never-ending. Like all software systems, monitoring can become so complex that it's fragile, complicated to change, and a maintenance burden."

> "Therefore, design your monitoring system with an eye toward simplicity."

> "Data collection, aggregation, and alerting configuration that is rarely exercised (e.g., less than once a quarter for some SRE teams) should be up for removal."

> "Signals that are collected, but not exposed in any prebaked dashboard nor used by any alert, are candidates for removal."

A könyv explicit kimondja azt is, hogy a monitorozás **méretezése** a csapat méretével arányos beruházás, és hogy még a Google SRE is kerüli a folyamatos képernyőfigyelést:

> "Monitoring a complex application is a significant engineering endeavor in and of itself. Even with substantial existing infrastructure for instrumentation, collection, display, and alerting in place, a Google SRE team with 10–12 members typically has one or sometimes two members whose primary assignment is to build and maintain monitoring systems for their service... (That being said, while it can be fun to have access to traffic graph dashboards and the like, SRE teams carefully avoid any situation that requires someone to 'stare at a screen to watch for problems.')"

> "In general, Google has trended toward simpler and faster monitoring systems, with better tools for post hoc analysis. We avoid 'magic' systems that try to learn thresholds or automatically detect causality."

Külön figyelmeztetés a monitorozás összemosásáról más rendszerekkel (releváns az „egy rendszer, sok funkció” tervezési kockázatra):

> "It can be tempting to combine monitoring with other aspects of inspecting complex systems, such as detailed system profiling, single-process debugging, tracking details about exceptions or crashes, load testing, log collection and analysis, or traffic inspection... blending together too many results in overly complex and fragile systems. As in many other aspects of software engineering, maintaining distinct systems with clear, simple, loosely coupled points of integration is a better strategy."

A könyv súlyossági hierarchiája (ticket / email alert / page) — ez a fogalmi alap az 5. kérdéshez is:

> "Alert — A notification intended to be read by a human and that is pushed to a system such as a bug or ticket queue, an email alias, or a pager. Respectively, these alerts are classified as tickets, email alerts, and pages."

> "Monitoring and alerting enables a system to tell us when it's broken, or perhaps to tell us what's about to break... Unless you're performing security auditing on very narrowly scoped components of a system, you should never trigger an alert simply because 'something seems a bit weird.'"

> "Paging a human is a quite expensive use of an employee's time... When pages occur too frequently, employees second-guess, skim, or even ignore incoming alerts, sometimes even ignoring a 'real' page that's masked by the noise."

A könyv zárógondolata a monitorozás egyszerűségéről és az email-riasztások korlátozott hasznáról:

> "A healthy monitoring and alerting pipeline is simple and easy to reason about. It focuses primarily on symptoms for paging, reserving cause-oriented heuristics to serve as aids to debugging problems... Email alerts are of very limited value and tend to easily become overrun with noise; instead, you should favor a dashboard that monitors all ongoing subcritical problems for the sort of information that typically ends up in email alerts."

**Érvényességi kör, amit a szöveg maga jelöl ki:** a fejezet kifejezetten *elosztott, felhasználó-kiszolgáló szolgáltatásokra* (user-facing distributed systems) készült, és a szerzők explicit kizárják a hatóköréből az üzleti analitikát és a biztonsági incidens-elemzést: "System monitoring is also helpful in supplying raw input into business analytics and in facilitating analysis of security breaches. Because this book focuses on the engineering domains in which SRE has particular expertise, we won't discuss these applications of monitoring here."

### 1.2 Brendan Gregg — USE módszer

Forrás: https://www.brendangregg.com/usemethod.html (Tier: **T3** — személyes weboldal/blog; **nem hivatalos szabvány**, de ez az egyetlen elsődleges forrás a módszerre, mivel a szerző maga publikálta itt és sehol máshol formális szabványként)

A módszer maga (Utilization, Saturation, Errors minden erőforrásra):

> "It will, however, only find certain types of issues – bottlenecks and errors – and should be considered as one tool in a larger toolbox."

Gregg saját maga mondja ki a módszer korlátait:

> "There are many problem types it doesn't solve, which will require other methods and longer time spans."

> "While the USE Method may find 80% of server issues, latency-based methodologies (eg, Method R) can approach finding 100% of all issues."

A célközönség is korlátozott a szerző szerint:

> a módszer "more suited for junior or senior system administrators", míg a latency-alapú megközelítések "may be more suited for database administrators or application developers", akik ismerik a szoftver belső működését.

Szoftver-erőforrásokra (pl. alkalmazás szintű queue-k) a szerző maga mondja, hogy a módszer csak akkor éri meg, ha könnyen elérhető a metrika:

> "Don't sweat this type. If the metrics work well, use them, otherwise software can be left to other methodologies (eg, latency)."

Explicit kizárt komponensek:

> "Some physical components have been left out, such as hardware caches (eg, MMU TLB/TSB, CPU)... Caches *improve* performance under high utilization" — vagyis a módszer alapfeltevése (magas kihasználtság = probléma jele) a gyorsítótáraknál nem érvényes, ezért ki vannak zárva.

### 1.3 Tom Wilkie — RED módszer

Forrás: https://www.weave.works/blog/the-red-method-key-metrics-for-microservices-architecture/ (Tier: **T3** — vállalati blogbejegyzés (Weaveworks); **nem hivatalos szabvány**, de ez a módszer megalkotójának, Tom Wilkie-nak saját, elsődleges publikációja, más hivatalos specifikáció nem létezik)

A módszer definíciója:

> "The RED Method defines the three key metrics you should measure for every microservice in your architecture." — (Rate, Errors, Duration)

**Wilkie saját maga mondja ki, mikor NEM alkalmazható:**

> "It is fair to say this method only works for request-driven services - it breaks down for batch-oriented or streaming services for instance."

> "It is also not all-encompassing. There are times you will need to monitoring other things - the USE Method is a great example when applied to resources like host CPU & Memory, or caches."

A RED és USE viszonyáról (Wilkie elismeri, hogy a USE absztrakciója szolgáltatásokra kevésbé illik):

> "However, I think the abstraction becomes a little strained when talking about services."

**Összegzés a három keretrendszer érvényességi köréről:** mindhárom explicit korlátozza magát: a Golden Signals felhasználó-kiszolgáló elosztott rendszerekre; a USE hardver-jellegű, kihasználtság-alapú erőforrásokra (és saját bevallása szerint csak ~80%-os lefedettségű); a RED kizárólag kérés-vezérelt (request-driven) szolgáltatásokra, kifejezetten *nem* batch- vagy stream-feldolgozásra. Egy egyfelhasználós, fájl alapú ágens-memória rendszer (markdown fájlok, SQLite index, batch-jellegű beágyazás-számítás) jellemzően nem "user-facing" elosztott szolgáltatás és nem tisztán kérés-vezérelt — ez a keretrendszerek saját deklarált hatókörén kívül esik, amit egyik szerző sem tagad, sőt maguk mondják ki a határokat.

## 2. Mit exportálnak ténylegesen az egybináris, önüzemeltetett projektek

### 2.1 Gitea

Forrás: https://docs.gitea.com/administration/config-cheat-sheet (Tier: **T1** — hivatalos dokumentáció)

Van `/metrics` végpont, **alapból ki van kapcsolva**:

> "Metrics (`metrics`) — `ENABLED`: **false**: Enables `/metrics` endpoint for prometheus."

> "`ENABLED_ISSUE_BY_LABEL`: false: Enable issue by label metrics with format `gitea_issues_by_label{label="bug"} 2`."

> "`ENABLED_ISSUE_BY_REPOSITORY`: false: Enable issue by repository metrics with format `gitea_issues_by_repository{repository="org/repo"} 5`."

> "`TOKEN`: empty: You need to specify the token, if you want to include in the authorization the metrics. The same token need to be used in prometheus parameters `bearer_token` or `bearer_token_file`."

### 2.2 Forgejo

Forrás: https://forgejo.org/docs/latest/admin/config-cheat-sheet/ (Tier: **T1** — hivatalos dokumentáció). Forgejo a Gitea kódbázisából ágazott le, és a konfiguráció szó szerint azonos:

> "Metrics (`metrics`) — `ENABLED`: false: Enables the `/metrics` endpoint for Prometheus."

Kiegészítő, közösségi kontextus (Tier: **T3**, nem hivatalos, Codeberg vitafórum, https://codeberg.org/forgejo/discussions/issues/399): egy adminisztrátor megerősíti, hogy bekapcsolta, de gyakorlatban alig használja:

> "I've enabled the `/metrics` endpoint and collect the metrics available, but effectively I do not use them in any way (alerts, dashboards)."

### 2.3 Miniflux

Forrás: https://miniflux.app/docs/configuration.html (Tier: **T1** — hivatalos dokumentáció)

Van `/metrics` végpont, **alapból ki van kapcsolva**:

> "`METRICS_COLLECTOR` — Set to 1 to enable metrics collector. Expose a `/metrics` endpoint for Prometheus." (alapértelmezett: kikapcsolva)

> "`METRICS_ALLOWED_NETWORKS` — List of networks (comma-separated values)" — alapértelmezett: `127.0.0.1/8`

> "`METRICS_REFRESH_INTERVAL` — Refresh interval in seconds to collect database metrics." (alapértelmezett: 60 másodperc)

Konkrét exportált metrikák a forráskódból (Tier: **T1** — Go modul dokumentáció, forráskódból generálva, https://pkg.go.dev/miniflux.app/metric):

> `miniflux_background_feed_refresh_duration` — "Processing time to refresh feeds from the background workers"
> `miniflux_scraper_request_duration` — "Web scraper request duration"
> `miniflux_archive_entries_duration` — "Archive entries duration"

(ezeken felül a `GatherStorageMetrics()` függvény adatbázis-szintű metrikákat is gyűjt, ezek pontos listáját a dokumentáció nem részletezi kimerítően.)

Biztonsági érzékenység, amit maga a projekt is jelez: 2023-ban biztonsági hibát jelentettek be, mert a `METRICS_ALLOWED_NETWORKS` hálózati szűrés megkerülhető volt (GHSA-3qjf-qh38-x73v, https://github.com/miniflux/v2/security/advisories/GHSA-3qjf-qh38-x73v, Tier: **T1** — hivatalos biztonsági közlemény), vagyis a metrika-végpont önmagában is támadási felület volt.

### 2.4 Syncthing

Forrás: https://docs.syncthing.net/users/metrics.html (Tier: **T1** — hivatalos dokumentáció)

Van natív, részletes Prometheus-stílusú metrika-végpont:

> "Syncthing provides an endpoint for Prometheus-style metrics. Metrics are served on the `/metrics` path on the GUI / API address. The metrics endpoint requires authentication when the GUI / API is configured to require authentication."

A dokumentáció **nem említ** külön ENABLED/DISABLED kapcsolót a metrikákhoz — a szöveg megfogalmazásából az következik, hogy a végpont mindig elérhető, amint a GUI/API fut, hitelesítést csak akkor követel, ha az API-hitelesítés maga be van kapcsolva. Ez eltér a többi vizsgált projekttől, ahol explicit `ENABLED=false` az alapértelmezés.

Exportált metrikák csomagonként (a dokumentáció teljes listája, T1 forrás):

- `build`: `syncthing_build_info` (verzióinformáció)
- `connections`: `syncthing_connections_active` ("Number of currently active connections, per device")
- `db`: `syncthing_db_files_updated_total`, `syncthing_db_operation_seconds_total`, `syncthing_db_operations_current`, `syncthing_db_operations_total`
- `events`: `syncthing_events_total` ("Total number of created/forwarded/dropped events")
- `fs`: `syncthing_fs_operation_bytes_total`, `syncthing_fs_operation_seconds_total`, `syncthing_fs_operations_total`
- `model`: `syncthing_model_folder_conflicts_total`, `syncthing_model_folder_processed_bytes_total`, `syncthing_model_folder_pull_seconds_total`, `syncthing_model_folder_pulls_total`, `syncthing_model_folder_scan_seconds_total`, `syncthing_model_folder_scans_total`, `syncthing_model_folder_state`, `syncthing_model_folder_summary`
- `protocol`: `syncthing_protocol_recv_bytes_total`, `syncthing_protocol_recv_decompressed_bytes_total`, `syncthing_protocol_recv_messages_total`, `syncthing_protocol_sent_bytes_total`, `syncthing_protocol_sent_messages_total`, `syncthing_protocol_sent_uncompressed_bytes_total`
- `scanner`: `syncthing_scanner_hashed_bytes_total`, `syncthing_scanner_scanned_items_total`

### 2.5 Vaultwarden — NINCS natív metrika-végpont

Forrás 1 (Tier: **T2** — hivatalos forráskód-tárban zajló, karbantartó által lezárt Pull Request, https://github.com/dani-garcia/vaultwarden/pull/3634): a `Prometheus metrics` végpontot hozzáadó PR-t a karbantartó **elutasította**, 2023.07.09-én lezárva, soha nem lett mergelve. A karbantartó indoklása biztonsági/felület-kockázatra hivatkozik:

> "I'm not really a fan of adding this built-in into Vaultwarden. Also, this implementation exposes those metrics to the rest of the world when enabled."

Forrás 2 (Tier: **T3** — nem hivatalos közösségi fórum, https://vaultwarden.discourse.group/t/prometheus-metrics/1571): egy karbantartó megerősíti, hogy jelenleg semmilyen metrika nincs exportálva:

> "None of these items are exposed via any metric endpoint. There is an /admin/users endpoint which provides some user info. But thats about it." és "For stuff like that i would suggest to use docker info or something."

Van egy kapcsolódó, régebbi GitHub issue is (https://github.com/dani-garcia/vaultwarden/issues/496, Tier: **T2**), amely szintén a feature-kérést dokumentálja, natív megoldás nélkül. Létezik nem-hivatalos, harmadik féltől származó exportáló (pl. `Tricked-dev/vwmetrics`, Tier: **T3**, nem a projekt része).

### 2.6 Paperless-ngx — NINCS natív metrika-végpont

Forrás (Tier: **T3** — GitHub Discussion, nem hivatalos, hivatalosan lezárva és zárolva, https://github.com/paperless-ngx/paperless-ngx/discussions/1541): a feature-kérést a karbantartó, `shamoon`, kifejezetten megkérdőjelezte:

> "I'm not really sure it's worth this being part of the paperless core...depends on how much new code the change introduces, or more specifically the maintenance burden"

A vitát 2025 augusztusában automatikusan lezárták, közösségi támogatás hiányában, majd zárolták. Egyetlen elérhető megoldás egy külső, nem hivatalos exportáló (`hansmi/prometheus-paperless-exporter`, Tier: **T3**), amelyről a felhasználók megjegyzik, hogy szuperfelhasználói API-hozzáférést igényel a teljes metrikakészlethez.

### 2.7 Jellyfin

Forrás: https://jellyfin.org/docs/general/post-install/networking/advanced/monitoring/ (Tier: **T1** — hivatalos dokumentáció)

Van natív `/metrics` végpont, **alapból ki van kapcsolva, explicit biztonsági indoklással**:

> "Jellyfin has two monitoring and metrics endpoints built-in: a basic health check endpoint and a Prometheus-compatible metrics endpoint."

> "Jellyfin can make Prometheus metrics available at /metrics, but this is turned off by default **to avoid unintentionally leaking this information on the public internet**. To enable it, you will need to edit `/etc/jellyfin/system.xml` and change this line from `false` to `true`: `<EnableMetrics>false</EnableMetrics>`."

A dokumentáció még reverse proxy szintű további hozzáférés-korlátozást is javasol: "If you have a reverse proxy configured, you can configure it to block access to the /metrics endpoint except for your internal network."

A dokumentáció nem sorolja fel tételesen az exportált metrikák nevét (ellentétben pl. a Syncthinggel) — csak azt állítja, hogy Prometheus-kompatibilis formátumban exportál.

### 2.8 Immich

Forrás: https://docs.immich.app/features/monitoring/ (Tier: **T1** — hivatalos dokumentáció)

Van natív Prometheus + OpenTelemetry alapú telemetria, **alapból ki van kapcsolva** (opt-in):

> "Immich provides a variety of performance metrics to allow for local monitoring and insights. This integration is primarily in the form of Prometheus metrics. However, exporting traces is also possible due to the use of OpenTelemetry instrumentation."

> "This is an opt-in feature intended for you to monitor immich's performance. This data isn't sent anywhere beyond what you've configured."

> "Immich will not expose an endpoint for metrics by default. To enable this endpoint, you can add the `IMMICH_TELEMETRY_INCLUDE=all` environmental variable to your `.env` file."

A metrikák csoportosítása:

> "The metrics in immich are grouped into API (endpoint calls and response times), host (memory and CPU utilization), and IO (internal database queries, image processing, and so on). Each group of metrics can be enabled or disabled independently."

A dokumentáció explicit megjegyzi, hogy Prometheus/Grafana **nem** része az alap telepítésnek, külön kell konfigurálni a Compose fájlban.

### 2.9 Összegzés — mit exportálnak ténylegesen?

| Projekt | Van `/metrics`? | Alapból bekapcsolva? | Forrás tier |
|---|---|---|---|
| Gitea | igen | **nem** (`ENABLED: false`) | T1 |
| Forgejo | igen (azonos Giteával) | **nem** (`ENABLED: false`) | T1 |
| Miniflux | igen | **nem** (`METRICS_COLLECTOR` alapból ki) | T1 |
| Syncthing | igen | dokumentáció szerint nincs külön kapcsoló — a GUI/API-val együtt elérhető | T1 |
| Vaultwarden | **nincs**, elutasított feature | n/a | T2 (PR) / T3 (fórum) |
| Paperless-ngx | **nincs**, elutasított feature | n/a | T3 (GitHub discussion) |
| Jellyfin | igen | **nem** (`<EnableMetrics>false</EnableMetrics>`, explicit biztonsági indoklással) | T1 |
| Immich | igen (Prometheus + OpenTelemetry trace) | **nem** (opt-in, `IMMICH_TELEMETRY_INCLUDE`) | T1 |

## 3. Az „over-engineering" ellenérve — van-e mérésen alapuló forrás?

**Amit találtam:**

Az AWS 2012. október 22-i hivatalos üzemzavar-összefoglalója (Tier: **T1** — AWS saját, hivatalos "post-event summary"-ja, https://aws.amazon.com/message/680342/) dokumentálja, hogy egy memóriaszivárgást okozó hiba azért maradt észrevétlen és súlyosbodott órákon át, mert a monitorozó rendszer maga nem volt elég finomszemcsés:

> "While we monitor aggregate memory consumption on each EBS Server, our monitoring failed to alarm on this memory leak."

> "Because of the design of the data collection service (which is tolerant to missing data), this did not cause any immediate issues or set off any alarms."

Ez egy dokumentált, hivatalos esetet ad arra, hogy a monitorozó/riasztó rendszer tervezési hibája (nem a metrikák száma, hanem a metrikák *granularitása* és a rendszer hibatűrő viselkedése) hozzájárulhat egy üzemzavar súlyosbodásához. **Fontos korlátozás:** ez egy hiperskálázott felhő-infrastruktúra esete, nem egy egyfelhasználós rendszeré, és nem azt bizonyítja, hogy „sok metrika” = „instabil rendszer”, hanem hogy a monitorozás *hiánya/pontatlansága* önmagában okozati tényező lehet egy incidensben.

A Vaultwarden karbantartójának indoklása (Tier: **T2**, ld. 2.5. pont) közvetlen, bár nem mért, hanem tapasztalati/döntési érvet ad arra, hogy egy metrika-végpont hozzáadása **önmagában is új támadási felületet és kockázatot** jelent egy önüzemeltetett, hitelesítő adatokat kezelő rendszerben:

> "this implementation exposes those metrics to the rest of the world when enabled."

**Amit NEM találtam (explicit negatív eredmény):** semmilyen hiteles, mérésen vagy szisztematikus tapasztalati adatgyűjtésen alapuló forrást (tudományos cikket, konferencia-előadást mért adatokkal, hivatalos incidens-statisztikát) arra, hogy **hány metrika, dashboard vagy riasztási szabály után válik egy monitorozó rendszer „használhatatlanná"** vagy kontraproduktívvá. A "cardinality explosion" témában talált cikkek (pl. openobserve.ai, Netdata Academy, Medium-bejegyzések) kizárólag gyártói blogok vagy vélemény-jellegű írások, mért adat vagy tanulmány nélkül — ezeket ezért **nem** vettem fel állítás forrásaként, csak a keresési nyomvonalban rögzítem őket (ld. link-táblázat). Az SREcon/USENIX konferencia-anyagok között sem található kifejezetten ilyen mért tanulmány.

## 4. Prometheus / OpenTelemetry erőforrásigénye minimális telepítésnél

### 4.1 Prometheus — hivatalos, pontos számok

Forrás: https://prometheus.io/docs/prometheus/latest/storage/ (Tier: **T1** — hivatalos dokumentáció)

> "Prometheus stores an average of only 1-2 bytes per sample."

Kapacitástervezési képlet, szó szerint:

> "needed_disk_space = retention_time_seconds * ingested_samples_per_second * bytes_per_sample"

Alapértelmezett megőrzési idő:

> "If neither this flag nor `storage.tsdb.retention.size` is set, the retention time defaults to `15d`."

Megőrzési méret ajánlás:

> "At present, we recommend setting the retention size to, at most, 80-85% of your allocated Prometheus disk space." — "The remaining 15-20% buffer covers the temporary extra space required by in-progress compactions."

WAL (write-ahead log) viselkedés:

> "High-traffic servers may retain more than three WAL files in order to keep at least two hours of raw data."

Kompaktálásra vonatkozó szabály:

> "Compaction will create larger blocks containing data spanning up to 10% of the retention time, or 31 days, whichever is smaller."

Ezek a számok pontosan idézettek a hivatalos dokumentációból; a konkrét memória- vagy lemezigényt egy adott, egyfelhasználós telepítésre (pl. "X MB RAM egy 1000 mintás/perc terhelésnél") a dokumentáció **nem** adja meg — csak a fenti képletet és a bájt/minta arányt, amiből a felhasználónak magának kell számolnia.

### 4.2 OpenTelemetry Collector — nincs hivatalos konkrét szám

Forrás: https://opentelemetry.io/docs/collector/scaling/ (Tier: **T1** — hivatalos dokumentáció)

A hivatalos "Scaling the Collector" oldal áttekinti a skálázási stratégiákat és megemlíti a `memory_limiter` processzort mint a memóriahasználat korlátozásának eszközét, de **nem közöl konkrét számot** (pl. "X MiB / 1000 span/mp") a minimális vagy tipikus erőforrásigényről. Kerestem az OpenTelemetry Collector és Collector-Contrib hivatalos README-jeit (`memorylimiterprocessor`) is konkrét "rule of thumb" szám után — ilyen hivatalos számot **nem találtam**. Ez explicit negatív eredmény: a Prometheus-szal ellentétben az OpenTelemetry hivatalos dokumentációja nem ad kvantitatív kapacitástervezési képletet vagy konkrét memória/lemez számot minimális telepítésre.

## 5. Mit jelent a „monitorozás", ha nincs 24/7 ügyelet?

Formális, kifejezetten **egyfelhasználós/otthoni önüzemeltetett rendszerekre** szabott szakirodalmat vagy hivatalos ajánlást **nem találtam**. Két releváns, dokumentált, analóg mintázatot azonosítottam:

**(a) A Google SRE könyv saját súlyossági hierarchiája** (Tier: **T1**, ld. 1.1. pont) különbséget tesz azonnali emberi beavatkozást igénylő "page" és alacsonyabb sürgősségű "ticket" / "email alert" között:

> "Alert — A notification intended to be read by a human and that is pushed to a system such as a bug or ticket queue, an email alias, or a pager. Respectively, these alerts are classified as tickets, email alerts, and pages."

Ez a hierarchia elvben átvihető úgy, hogy 24/7 ügyelet hiányában a rendszer sosem generál "page"-et (azonnali megszakítást), csak "ticket"-et vagy dashboardon megjelenő állapotot, amit a felhasználó a saját ütemezésében néz át — de a könyv ezt nem mondja ki explicit módon egyfelhasználós kontextusra, ez itt a szöveg saját kategóriáinak analóg alkalmazása, nem szó szerinti ajánlás.

**(b) A "dead man's switch" / periodikus check-in minta**, amit a healthchecks.io hivatalos dokumentációja ír le (Tier: **T1** — hivatalos termékdokumentáció, https://healthchecks.io/docs/):

> "Healthchecks.io listens for HTTP requests ('pings') from your cron jobs and scheduled tasks. It keeps silent as long as pings arrive on time. It raises an alert as soon as a ping does not arrive on time."

> "Healthchecks.io works as a dead man's switch for processes that need to run continuously or on a regular, known schedule."

Ez a minta strukturálisan más, mint a valós idejű riasztás: nem azt figyeli, hogy "történt-e hiba éppen most", hanem azt, hogy "jelentkezett-e a folyamat a várt időn belül" — vagyis a felügyelet aszinkron, és a riasztás (pl. e-mail) nem igényel azonnali emberi jelenlétet, csak időben belüli reakciót. Ez explicit tervezési minta, nem "valós idejű riasztás", és nyíltan dokumentált cél szerint pontosan olyan helyzetekre való, ahol nincs folyamatos emberi felügyelet.

**Amit nem találtam:** sem a Google SRE könyvben, sem a Prometheus/Grafana ökoszisztéma hivatalos dokumentációjában nincs olyan szakasz, ami kifejezetten "egyfelhasználós, ügyelet nélküli rendszer" esetére adna ajánlást a riasztási stratégiára. Amit találtam, azok analóg, más kontextusra írt alapelvek (SRE súlyossági hierarchia) és egy konkrét, más célú termék dokumentált tervezési mintája (healthchecks.io).

## Amire NINCS publikált válasz

- **Nincs mérésen alapuló forrás** arra, hogy hány metrika, dashboard vagy riasztási szabály után válik egy monitorozó rendszer "használhatatlanná" vagy kontraproduktívvá. Kerestem tudományos cikkeket, SREcon/USENIX konferencia-anyagokat, hivatalos incidens-statisztikákat — csak vélemény-jellegű gyártói blogokat találtam ("cardinality explosion" témában), amelyeket emiatt nem használtam fel állítás forrásaként.
- **Nincs hivatalos OpenTelemetry Collector szám** a minimális memória/CPU igényre (sem a fő dokumentációban, sem a `memory_limiter` processzor README-jében). A Prometheus-szal ellentétben itt nincs "bájt/minta"-szerű hivatalos képlet.
- **Nincs formális szakirodalom vagy hivatalos ajánlás** kifejezetten egyfelhasználós, önüzemeltetett, 24/7 ügyelet nélküli rendszerek riasztási stratégiájára. Amit találtam (SRE súlyossági hierarchia, healthchecks.io "dead man's switch" minta), az más kontextusra írt, analóg módon alkalmazható elv, nem közvetlen ajánlás erre a helyzetre.
- **Nem egyértelmű a Syncthing metrika-végpontjának alapértelmezett elérhetősége**: a hivatalos dokumentáció nem tartalmaz explicit ENABLED/DISABLED kapcsolót (ellentétben Gitea/Forgejo/Miniflux/Jellyfin/Immich rendszerekkel, ahol ez explicit dokumentált), így nem állítható biztosan, hogy a `/metrics` végpont "alapból ki van kapcsolva"-e, vagy mindig elérhető, amint a GUI/API fut.
- **Nincs a Google SRE könyvben (sem az általam megnyitott fejezetekben) külön, névvel jelölt szakasz kifejezetten "egyfős" vagy "hobbi méretű" rendszerekre** — a könyv explicit a Google méretű, csapat által üzemeltetett elosztott rendszerekre íródott, és ezt maga is jelzi ("This book focuses on the engineering domains in which SRE has particular expertise").
- **Miniflux teljes exportált metrika-listája nem található meg egyben** a hivatalos dokumentációban vagy egyetlen forráskód-fájlban; csak részleges listát sikerült rekonstruálni a `pkg.go.dev` generált Go-dokumentációból (3 Histogram metrika + nem részletezett "database metrics").
- **Jellyfin hivatalos dokumentációja nem sorolja fel tételesen** az exportált Prometheus-metrikák neveit (csak azt állítja, hogy "Prometheus-compatible" formátumú a végpont) — ellentétben pl. a Syncthinggel, ahol teljes, névvel ellátott lista van.



---

# SQ02 — Állapotellenőrzés (health check) tervezése egyfelhasználós, egygépes szolgáltatáshoz

Ez az anyag hat forrásterületet fed le a health check tervezéséhez egy egyfelhasználós, egygépes, markdown-fájl alapú ágens-memória rendszerhez (MCP-kiszolgáló, SQLite index, admin webfelület). A Kubernetes hivatalos dokumentációja élesen elválasztja a liveness/readiness/startup probe-ok célját és kimenetét, és kifejezetten figyelmeztet arra, hogy a liveness probe helytelen (pl. függő rendszert lekérdező) implementációja kaszkádhibát okozhat — ez lényegében megegyezik azzal, amit az AWS Builders' Library "Implementing health checks" cikke ("hard dependency", "cascading failure") ír le, bár az AWS cikk nem a "shallow/deep" szópárt, hanem "liveness / local / dependency health checks" hármas felosztást használ. Az IETF "Health Check Response Format for HTTP APIs" (draft-inadarei-api-health-check) szabványjavaslat lejárt, sosem lett RFC, utolsó verziója a -06 (2021-10-16, lejárt 2022-04-19), utódot nem találtam. Az MCP specifikáció jelenlegi (2026-07-28) verziója NEM tartalmaz health/heartbeat fogalmat, és a korábban létező `ping` metódust is eltávolította — ez fontos, idővel változó tény, amit dátumozva kell kezelni. Egyfelhasználós, egygépes környezetben a Linux systemd `Type=notify` + `WatchdogSec=` egy konkrét, kernelszintű "élő vagyok" mechanizmust ad (kimaradás esetén a watchdog egyszerűen ki van kapcsolva, nincs figyelés); a macOS launchd hivatalos dokumentációja ezzel szemben kifejezetten NEM ír le formális health-check/watchdog fogalmat, csak crash-alapú újraindítást. SQLite-specifikus, health-check-célú, hivatalos ajánlást (SELECT 1 vs PRAGMA quick_check) nem találtam; a hivatalos SQLite dokumentáció csak a quick_check és integrity_check egymáshoz viszonyított költségét (O(N) vs O(N log N)) írja le, és egy valós MCP-memória-szolgáltatás (mcp-memory-service) forráskódja funkcionális sématábla-lekérdezést használ, nem PRAGMA-t.

---

## 1. Kubernetes: liveness / readiness / startup probe megkülönböztetés

**Forrás:** https://kubernetes.io/docs/concepts/workloads/pods/probes/ és https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/ (a kubernetes/website hivatalos GitHub-repó forrásfájljaiból ellenőrizve: `content/en/docs/concepts/workloads/pods/probes.md` és `.../pod-lifecycle.md`)

**Definíciók (szó szerint):**

- Startup probe: "Startup probes verify whether the application within a container is started."
- Liveness probe: "Liveness probes determine when to restart a container."
- Readiness probe: "Readiness probes determine when a container is ready to accept traffic."

**Mi történik hibánál (szó szerint, `probes.md`):**

- Liveness és startup probe hibája esetén: "the kubelet kills the container, and the container is subjected to its restart policy."
- Readiness probe hibája esetén (nincs újraindítás, csak forgalom-leválasztás): "the kubelet marks the container as not ready, and the Pod stops receiving traffic from matching Services."
- Összefoglalva: "Kubernetes can restart unhealthy containers or stop sending traffic to containers that are not ready."
- A `pod-lifecycle.md` szerint readiness-hibánál konkrétan: "the EndpointSlice controller removes the Pod's IP address from the EndpointSlices of all Services that match the Pod."

**Mikor használjunk liveness probe-ot (és mikor NEM szükséges) — szó szerint:**

- "If the process in your container is able to crash on its own whenever it encounters an issue or becomes unhealthy, you do not necessarily need a liveness probe"
- "If you'd like your container to be killed and restarted if a probe fails, then specify a liveness probe, and specify a `restartPolicy` of `Always` or `OnFailure`."

**Mikor használjunk readiness probe-ot — szó szerint:**

- "To start sending traffic to a Pod only when a probe succeeds, specify a readiness probe."
- "You can also use a readiness probe to let a container take itself down for maintenance, by checking an endpoint specific to readiness that is different from the liveness probe."

**A liveness probe HELYTELEN használatának kifejezett veszélye (kaszkádhiba) — szó szerint, `probes.md`:**

> "Liveness probes can be a powerful way to recover from application failures, but they should be used with caution."

> "Incorrect implementation of liveness probes can lead to cascading failures. This results in restarting of container under high load; failed client requests as your application became less scalable; and increased workload on remaining pods due to some failed pods."

**A `configure-liveness-readiness-startup-probes` feladat-oldal figyelmeztetése (Caution/Note blokk, szó szerint, a hivatalos forrásfájlból):**

> "The readiness and liveness probes do not depend on each other to succeed. If you want to wait before executing a readiness probe, you should use `initialDelaySeconds` or a `startupProbe`."

> "Readiness probes run on the container during its whole lifecycle."

**Fontos negatív megállapítás:** a Kubernetes dokumentáció NEM tartalmaz egyetlen, explicit, önálló "mikor NE használj readiness probe-ot" mondatot vagy szakaszt. A dokumentum a readiness probe-ra kizárólag pozitív use-case-eket ("mikor HASZNÁLD") ad meg, míg a "helytelen használat veszélyes" jellegű, kifejezett figyelmeztetés kizárólag a liveness probe-ra vonatkozik (l. fent, kaszkádhiba). Ezt a "Amire nincs publikált válasz" szakaszban is rögzítem.

---

## 2. IETF draft-inadarei-api-health-check — státusz és mezőkészlet

**Forrás:** https://datatracker.ietf.org/doc/draft-inadarei-api-health-check/06/ és https://datatracker.ietf.org/doc/html/draft-inadarei-api-health-check-06

**Státusz (szó szerint a datatracker oldaláról):**

> "Expired Internet-Draft (individual) Expired & archived"

- Utolsó (és egyben utolsó publikált) verzió: **-06**, publikálva 2021-10-16, lejárt 2022-04-19.
- A datatracker verziólistája -00-tól -06-ig terjed; -06 után nincs újabb revízió, WG-draftra (draft-ietf-...) vagy RFC-re való átemelést nem találtam.
- A dokumentum oldala kifejezetten jelzi: "This Internet-Draft is no longer active. A copy of the expired Internet-Draft is available in these formats."

**Abstract (szó szerint, draft-06):**

> "This document proposes a service health check response format for HTTP APIs."

**Ajánlott media type (szó szerint):** `application/health+json`

**A `status` mező (kötelező) — szó szerint:**

> "status: (required) indicates whether the service status is acceptable or not."

Megengedett értékek: `pass` (egészséges; elfogadott aliasok: "ok" a Node Terminus, "up" a Java SpringBoot kompatibilitáshoz), `fail` (nem egészséges; aliasok: "error", "down"), `warn` (egészséges, de van aggály).

**HTTP státuszkód-követelmény — szó szerint:**

> "For 'pass' status, HTTP response code in the 2xx-3xx range MUST be used. For 'fail' status, HTTP response code in the 4xx-5xx range MUST be used. In case of the 'warn' status, endpoints MUST return HTTP status in the 2xx-3xx range."

**A teljes top-level mezőkészlet (mind opcionális, a `status` kivételével) — szó szerint az egyes definíciók:**

| Mező | Definíció (szó szerint) |
|---|---|
| version | "public version of the service" |
| releaseId | "separate 'release number' or 'releaseId' that is different from the public version" |
| notes | "array of notes relevant to current state of health" |
| output | "raw error output, in case of 'fail' or 'warn' states" |
| checks | "provides detailed health statuses of additional downstream systems and endpoints" |
| links | "object containing link relations and URIs for external links that MAY contain more information" |
| serviceId | "unique identifier of the service, in the application scope" |
| description | "human-friendly description of the service" |

**A `checks` objektum al-mezői (komponensenként) — szó szerint:**

- componentId: "unique identifier of an instance of a specific sub-component/dependency of a service"
- componentType: pl. "component", "datastore", "system"
- observedValue: "could be any valid JSON value, such as: string, number, object, array or literal"
- observedUnit: mértékegység (pl. "ms", "percent", "s")
- status: "has the exact same meaning as the top-level 'output' element, but for the sub-component" (a datatracker-kivonat így fogalmazott; ez a `status`/`output` közötti pontos viszonyt írja le a sub-component szintjén)
- time: "date-time, in ISO8601 format, at which the reading of the observedValue was recorded"
- output: "raw error output" nem-pass állapot esetén

**Konklúzió:** a draft LEJÁRT (expired), sosem vált RFC-vé, és semmilyen aktív IETF munkacsoporti utódját nem találtam a datatracker keresésével.

---

## 3. Az anti-minta: adatbázist lekérdező health check és a kaszkádhiba (AWS Builders' Library)

**Forrás:** https://d1.awsstatic.com/builderslibrary/pdfs/implementing-health-checks.pdf (az AWS Builders' Library "Implementing health checks" c. cikkének hivatalos PDF-je; a html verzió — https://aws.amazon.com/builders-library/implementing-health-checks/ — kliensoldalon renderelt tartalommal rendelkezik, a lekérő eszköz csak a landing oldal metaadatait tudta kinyerni belőle, l. a link-táblázatban)

**FONTOS PONTOSÍTÁS:** a cikk NEM a "shallow health check" / "deep health check" szópárt használja. Az általa használt hármas terminológia:

1. **Liveness checks** — szó szerint: "Liveness checks test the basic connectivity to a service and the presence of a server process. They are often performed by a load balancer or external monitoring agent, and they are unaware of the details about how an application works." Példák: "Tests that confirm that a server is listening on its expected port and accepting new TCP connections. Tests that perform a basic HTTP requests and make sure that the server responds with a 200 status code."

2. **Local health checks** — szó szerint: "Local health checks go further than liveness checks to verify that the application is likely to be able to function. These health checks test resources that are not shared with the server's peers. Therefore, they are unlikely to fail on many servers in the fleet simultaneously."

3. **Dependency health checks** — szó szerint: "Dependency health checks are a thorough inspection of the ability of an application to interact with its adjacent systems. These checks ideally catch problems local to the server, such as expired credentials, that are preventing it from interacting with a dependency. But they can also have false positives when there are problems with the dependency itself."

A "deep" szó egyetlen előfordulása a dokumentumban (nem kategórianévként, hanem melléknévi minősítésként) — szó szerint:

> "...the existing health check was deep enough to ensure that the rendering process was running and responding but not deep enough to ensure it was responding correctly."

**A kaszkádhiba veszélye — szó szerint, a "Balancing dependency health checks with the scope of impact" c. szakaszból:**

> "If a service only calls the dependency sometimes, we might consider the dependency to be a 'soft dependency,' since the service can still do some types of work even if it can't talk to the dependency. Without fail-open protection, implementing a health check that tests a dependency turns that dependency into a 'hard dependency.' If the dependency is down, the service also goes down, creating a cascading failure with increased scope of impact."

**A "Health checks without a circuit breaker" c. szakaszból — szó szerint:**

> "However, it is also the riskiest path if the server is wrong about its health or doesn't see the whole picture of what's happening across the fleet. When all servers across the fleet make the same wrong decision simultaneously, it can cause cascading failures throughout adjacent services."

**"Fail open" mechanizmus (védekezés a kaszkádhiba ellen) — szó szerint:**

> "When an individual server fails a health check, the load balancer stops sending it traffic. But when all servers fail health checks at the same time, the load balancer fails open, allowing traffic to all servers."

> "The AWS Network Load Balancer fails open if no servers are reporting as healthy."

---

## 4. Az MCP (Model Context Protocol) specifikáció és az állapotellenőrzés

**Forrás:** https://modelcontextprotocol.io/specification/versioning ; https://modelcontextprotocol.io/specification/2026-07-28/changelog ; a hivatalos séma-forrásfájlok: https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/2025-06-18/schema.ts és .../schema/2026-07-28/schema.ts

**A jelenlegi (2026-09-15-i állapot szerinti) hivatalos protokollverzió — szó szerint:**

> "The **current** protocol version is [**2026-07-28**]"

**Kritikus, IDŐFÜGGŐ megállapítás — a `ping` metódus státusza változott:**

A 2025-06-18-as (és korábbi, pl. 2024-11-05, 2025-03-26, 2025-11-25) specifikáció-verziókban létezett egy `ping` metódus. A 2025-06-18-as verzió Ping oldalán (https://modelcontextprotocol.io/specification/2025-06-18/basic/utilities/ping) szó szerint ez áll:

> "The Model Context Protocol includes an optional ping mechanism that allows either party to verify that their counterpart is still responsive and the connection is alive."

Kérés/válasz formátum (szó szerint idézve a specifikációból):

```json
{
  "jsonrpc": "2.0",
  "id": "123",
  "method": "ping"
}
```

> "1. The receiver **MUST** respond promptly with an empty response" — `{"jsonrpc": "2.0", "id": "123", "result": {}}`

> "2. If no response is received within a reasonable timeout period, the sender **MAY**: Consider the connection stale / Terminate the connection / Attempt reconnection procedures"

> "Implementations **SHOULD** periodically issue pings to detect connection health" — ez az egyetlen hely a régebbi specifikációban, ahol a "health" szó előfordul, és az is kifejezetten a kapcsolat (connection), nem a szolgáltatás egészségére vonatkozik.

A hivatalos séma (2025-06-18, `schema.ts`) ezt így definiálja:

> `export interface PingRequest extends Request { method: "ping"; }`

és a kommentje szerint a ping "issued by either the server or the client, to check that the other party is still alive. The receiver must promptly respond, or else may be disconnected."

**A JELENLEGI (2026-07-28) verzió a `ping`-et ELTÁVOLÍTOTTA.** A hivatalos changelog (https://modelcontextprotocol.io/specification/2026-07-28/changelog) szó szerint (5. pont a "Major changes" alatt):

> "Remove `ping`, `logging/setLevel`, and `notifications/roots/list_changed`. Log level is now set per-request via `io.modelcontextprotocol/logLevel` in `_meta`; servers MUST NOT emit `notifications/message` for requests that did not include this field ([SEP-2575])."

Ezt megerősíti a 2026-07-28-as hivatalos séma-forrásfájl közvetlen vizsgálata is: a `PingRequest` típus abból HIÁNYZIK. Amit a séma helyette tartalmaz, az a `server/discover` (`DiscoverRequest`/`DiscoverResult`), ami viszont — a hivatalos leírás szerint (https://modelcontextprotocol.io/specification/2026-07-28/server/discover) — kifejezetten verzió- és képesség-egyeztetésre, NEM élettartam-/health-ellenőrzésre szolgál. Szó szerint:

> "`server/discover` lets a client query a server's supported protocol versions, capabilities, and identity before sending any other requests. Servers **MUST** implement it."

A `server/discover` leírásában sem a "health", sem a "heartbeat", sem a "liveness"/"readiness" szó nem fordul elő.

**Explicit negatív megállapítás:** sem a korábbi (2025-ös), sem a jelenlegi (2026-07-28) MCP specifikáció nem definiál "health" vagy "heartbeat" fogalmat/mezőt/metódust. A `ping` a legközelebbi rokon fogalom volt (kapcsolat-életképesség, nem szolgáltatás-egészség), de ez a JELENLEGI verzióból már ki lett véve. A hivatalos séma-fájl teljes szövegében ("2026-07-28/schema.ts") sem a "health", sem a "heartbeat" szó nem szerepel.

---

## 5. Egyfelhasználós, egygépes szolgáltatás: systemd watchdog és macOS launchd

### systemd — `Type=notify` és `WatchdogSec=`

**Forrás (elsődleges, freedesktop.org 403-mal elutasította a lekérést — l. link-táblázat; az Arch Linux hivatalos man-oldal-tükrén keresztül lekért, a felstream systemd projektből származó szöveg):** https://man.archlinux.org/man/systemd.service.5.en és https://man.archlinux.org/man/sd_notify.3.en

**`WatchdogSec=` — szó szerint:**

> "Configures the watchdog timeout for a service. The watchdog is activated when the start-up is completed. The service must call sd_notify(3) regularly with 'WATCHDOG=1' (i.e. the 'keep-alive ping'). If the time between two such calls is larger than the configured time, then the service is placed in a failed state and it will be terminated with SIGABRT (or the signal specified by WatchdogSignal=). By setting Restart= to on-failure, on-watchdog, on-abnormal or always, the service will be automatically restarted."

**Mi történik, ha a `WatchdogSec=` KIMARAD (nincs beállítva)?** A funkció alapértelmezés szerint ki van kapcsolva — szó szerint: a beállítás "Defaults to 0" (azaz nincs watchdog-időtúllépés, a service manager nem várja a keep-alive pingeket, és nem indítja újra a szolgáltatást elakadás esetén ezen a csatornán). Ha `WatchdogSec=` nincs megadva, a `sd_notify(3)` `WATCHDOG=1` hívásainak elmaradása nem vált ki semmilyen systemd-oldali reakciót.

**`Type=notify` — szó szerint:**

> "Behavior of notify is similar to exec; however, it is expected that the service sends a 'READY=1' notification message via sd_notify(3) or an equivalent call when it has finished starting up. systemd will proceed with starting follow-up units after this notification message has been sent."

**A `WATCHDOG=1` üzenet (`sd_notify` man oldal) — szó szerint:**

> "Tells the service manager to update the watchdog timestamp. This is the keep-alive ping that services need to issue in regular intervals if *WatchdogSec=* is enabled for it."

**A `WATCHDOG=trigger` mechanizmus (a szolgáltatás önmaga jelezhet azonnali hibát) — szó szerint:**

> "the service detected an internal error that should be handled by the configured watchdog options. This will trigger the same behaviour as if *WatchdogSec=* is enabled and the service did not send 'WATCHDOG=1' in time."

### macOS launchd

**Forrás (hivatalos Apple fejlesztői dokumentáció):** https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html ; kiegészítésül a launchd.plist(5) man-oldal tükre: https://keith.github.io/xcode-man-pages/launchd.plist.5.html

**A `KeepAlive` kulcs — szó szerint:**

> "This optional key is used to control whether your job is to be kept continuously running or to let demand and conditions control the invocation. The default is false and therefore only demand will start the job."

Al-feltételek, pl.:
- `SuccessfulExit`: "If true, the job will be restarted as long as the program exits and with an exit status of zero."
- `Crashed`: "If true, the the job will be restarted as long as it exited due to a signal which is typically associated with a crash (SIGILL, SIGSEGV, etc.)."

**A `ThrottleInterval` kulcs — szó szerint:** "This key lets one override the default throttling policy imposed on jobs by launchd. The value is in seconds, and by default, jobs will not be spawned more than once every 10 seconds."

**Az Apple hivatalos "Creating Launch Daemons and Agents" útmutatójából — a crash-alapú újraindítási logika, szó szerint:**

> "Important: If your daemon shuts down too quickly after being launched, launchd may think it has crashed. Daemons that continue this behavior may be suspended and not launched again when future requests arrive. To avoid this behavior, do not shut down for at least 10 seconds after launch."

> "If you do, launchd thinks your process has died. Depending on your property list key settings, launchd will either keep trying to relaunch your process until it gives up (with a 'respawning too fast' error message) or will be unable to restart it if it really does die."

**Explicit negatív megállapítás:** az Apple hivatalos launchd-dokumentációja NEM ír le formális "health check" vagy "watchdog" (aktív keep-alive ping / timeout) mechanizmust a systemd `WatchdogSec=`/`sd_notify(3)` mintájára. A launchd kizárólag a folyamat kilépését/összeomlását (exit code, szignál) figyeli, és a `KeepAlive`/`ThrottleInterval` kulcsokkal szabályozza az újraindítást — proaktív, a szolgáltatás BELSEJÉBŐL jövő "élek és egészséges vagyok" jelzést (mint a systemd `WATCHDOG=1`) a felkutatott hivatalos dokumentáció nem említ.

---

## 6. SQLite-alapú szolgáltatás health checkje

**Forrás:** https://sqlite.org/pragma.html#pragma_quick_check , https://sqlite.org/pragma.html#pragma_integrity_check , https://sqlite.org/forum/info/631e8968e70b35bc

**`PRAGMA quick_check` vs `PRAGMA integrity_check` — a hivatalos SQLite dokumentáció szerint, szó szerint:**

> "The pragma is like integrity_check except that it does not verify UNIQUE constraints and does not verify that index content matches table content."

Komplexitás — szó szerint:

> "PRAGMA quick_check runs in O(N) time whereas PRAGMA integrity_check requires O(NlogN) time where N is the total number of rows in the database."

**Mit ellenőriz a teljes `integrity_check` — szó szerint:**

> "This pragma does a low-level formatting and consistency check of the database. The integrity_check pragma look for: Table or index entries that are out of sequence / Misformatted records / Missing pages / Missing or surplus index entries / UNIQUE, CHECK, and NOT NULL constraint errors / Integrity of the freelist / Sections of the database that are used more than once, or not at all"

> "PRAGMA integrity_check does not find FOREIGN KEY errors. Use the PRAGMA foreign_key_check command to find errors in FOREIGN KEY constraints."

**Valós költség nagy adatbázison — a hivatalos SQLite fórumból, szó szerint (Cecil, 2020-05-03, 4.2 GB-os adatbázisról):**

> "I have a very large DB (4,2 GB) and when I do a: PRAGMA INTEGRITY_CHECK on it, it takes more as twenty minutes."

Az SQLite-fórum egyik moderátorának (Simon Slavin) válasza — szó szerint:

> "Normal. It has to read every piece of data in the table and its indexes, and do a lot of cross-referencing."

Egy másik hozzászóló (Kees Nuyt) magyarázata a lemez-gyorsítótár hatásáról — szó szerint:

> "In the first run, the database is not in the OS filesystem cache (AKA disk cache), so a lot of time is spent waiting for I/O (read from disk). In all subsequent runs a significant part of the database will be in the cache, especially often used database pages."

**FONTOS HIÁNY:** nem találtam olyan HIVATALOS SQLite-dokumentumot vagy mért, hitelt érdemlő forrást, amely kifejezetten a **"SELECT 1" vs "PRAGMA quick_check" health-check kontextusú** költségét hasonlítaná össze. Amit találtam: (a) a `quick_check`/`integrity_check` egymáshoz viszonyított komplexitása (fent), és (b) hogy a teljes `integrity_check` percekig-tíz-percekig tarthat GB-os méretű adatbázison — ami gyakorlati érv amellett, hogy ezeket a PRAGMA-kat NEM cél gyakori (pl. minden N másodperces) health check ciklusban futtatni, de ezt maga a dokumentáció explicit módon nem mondja ki egy health-check ajánlás formájában.

**Valós MCP-memória-szolgáltatás gyakorlata (nem hivatalos, de közvetlenül releváns kódpélda):** a `doobidoo/mcp-memory-service` (https://github.com/doobidoo/mcp-memory-service) `db_health_check.py` szkriptje a repó fő ágának (`main`) vizsgálatakor NEM PRAGMA-t, hanem egy funkcionális séma-lekérdezést használ:

> `SELECT name FROM sqlite_master WHERE type='table'`

— ezzel ellenőrizve, hogy a várt táblák (`memories`, `memory_embeddings`) léteznek-e; a health-checker emellett funkcionális teszteket (mentés/lekérés/törlés) végez, nem alacsony szintű integritás-diagnosztikát.

---

## Amire NINCS publikált válasz

- **Kubernetes:** nem találtam olyan explicit, önálló mondatot vagy szakaszt a hivatalos dokumentációban, amely kifejezetten azt mondaná ki, hogy "mikor NE használj readiness probe-ot". A dokumentáció csak pozitív use-case-eket ad a readiness probe-hoz; a kifejezett "vigyázz, ez veszélyes" jellegű figyelmeztetés kizárólag a liveness probe-ra vonatkozik.
- **IETF draft:** nem találtam bizonyítékot arra, hogy a draft-inadarei-api-health-check bármikor IETF munkacsoporti (WG) draft-tá vagy RFC-vé vált volna a -06 után; nincs is jele folyamatban lévő utódmunkának a datatracker keresés alapján.
- **AWS Builders' Library:** a cikk nem használja a "shallow health check" kifejezést kategórianévként (csak "liveness checks" szerepel hasonló szerepben); a "deep" szó is csak egyszer, melléknévi minősítésként fordul elő, nem formális kategórianévként. Ha a felhasználói elvárás kifejezetten a "shallow vs deep" terminológia hivatalos forrásbeli megléte volt, ezt itt explicit módon cáfolom: NEM ez a cikk hivatalos terminológiája.
- **MCP:** nem találtam SEP-et (Specification Enhancement Proposal), GitHub issue-t vagy vitaanyagot, amely kifejezetten egy jövőbeli "health"/"heartbeat" metódus bevezetését tárgyalná a `ping` 2026-07-28-as eltávolítása után; nem tudom megmondani, hogy ez tervezett, ideiglenes hiány-e, vagy szándékos, végleges döntés.
- **macOS launchd:** nem találtam olyan hivatalos Apple-forrást, amely a systemd `WatchdogSec=`-hez hasonló, a szolgáltatás BELSEJÉBŐL érkező, aktív "élek és egészséges vagyok" keep-alive mechanizmust írna le. Ha ilyen létezik (pl. újabb launchd-verzióban), a nyilvánosan elérhető hivatalos dokumentáció ezt nem tárgyalja explicit módon.
- **SQLite health check:** nem találtam hivatalos vagy mért, hitelt érdemlő forrást, amely kifejezetten "SELECT 1" vs "PRAGMA quick_check" összehasonlítást tenne health-check kontextusban (költség, gyakoriság-ajánlás). Csak közvetett adatokat találtam (quick_check O(N) vs integrity_check O(NlogN); nagy DB-n percekig tartó integrity_check egy fórumbeszélgetésben).

---



---

# SQ03 — Üzemeltetési napló az audit naplótól elkülönítve: mit mond a szabványirodalom és a gyakorlat

Egyik vizsgált szabvány sem használ olyan éles, formális kettéválasztást, hogy "audit log" kontra "üzemeltetési/alkalmazásnapló" — de az OWASP Logging Cheat Sheet kifejezetten kimondja, hogy a kettőt **más célra gyűjtik, és emiatt gyakran külön kell tartani őket**. A NIST SP 800-92 nem célja szerint (biztonsági vs. üzemeltetési), hanem forrás szerint (biztonsági szoftver / OS / alkalmazás) kategorizálja a naplókat, és nem mond ki kötelező fizikai szétválasztást. A syslog RFC 5424 saját maga mondja ki, hogy a nyolc súlyossági szint **nem normatív**, tisztán informális jellegű — vagyis a szintek használata konvenció, nem mért/objektív skála. A Twelve-Factor App és az OpenTelemetry Logs specifikáció (ma: **Stable** állapot) egyaránt a strukturált, folyamként kezelt naplózás felé mutat, szemben a saját fájlkezeléssel. A logrotate és a systemd-journald.conf saját alapértelmezései meglepően szűkösek/agresszívek (a logrotate `rotate` paramétere alapból **0**, azaz nincs megőrzés, amíg be nem állítják; a journald `MaxRetentionSec` alapból **0**, azaz kikapcsolva). A megvizsgált négy önüzemeltetett, egybináris projekt (Forgejo/Gitea, Miniflux, Syncthing, Vaultwarden) egyike sem vezet külön "audit naplót" — mindegyik egyetlen üzemeltetési naplófolyamot ír, jellemzően stdout-ra alapból, néhány (4-6) szöveges szintnévvel, és a forgatást vagy az OS-re bízza, vagy egy egyszerű beépített forgatót ad hozzá. Hivatalos, publikált szám arra, hogy a szinkron fájlba írás mennyivel lassítja a kérésfeldolgozást, **nem található** — csak könyvtár-/eszközspecifikus, nagy szórású mért benchmarkok vannak (20%–100%+ különbség, implementációtól függően).

---

## 1. Van-e elismert megkülönböztetés az audit napló és az alkalmazás/üzemeltetési napló között?

### 1.1 OWASP Logging Cheat Sheet — a "Purpose" (cél) szakasz

A hivatalos OWASP Cheat Sheet Series oldala és a mögötte álló GitHub-forrás (kétszer, egymástól függetlenül lekérve, egyező szöveggel) ezt mondja ki:

> "Process monitoring, audit, and transaction logs/trails etc. are usually collected for different purposes than security event logging, and this often means they should be kept separate. The types of events and details collected will tend to be different."
> — https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html (heading: "Purpose"), megerősítve: https://raw.githubusercontent.com/OWASP/CheatSheetSeries/master/cheatsheets/Logging_Cheat_Sheet.md

Vagyis az OWASP kifejezetten **különbséget tesz** (a) folyamat-monitorozás / audit / tranzakciós napló, és (b) biztonsági esemény-napló (security event logging) között, és azt mondja, ez **gyakran** indokolja a különtartást — de nem ír elő kötelező technikai megoldást (pl. külön fájl, külön adatbázis) rá.

Ugyanakkor az OWASP "Which events to log" listája a gyakorlatban **összemossa** a biztonsági és az operatív eseményeket — köztük szerepel:

> "Application errors and system events" — a naplózandó kategóriák között, ugyanabban a listában, mint az "Authentication successes and failures" vagy az "Authorization failures".
> — https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html

Tehát az OWASP egyszerre mondja, hogy a *célok* szerint gyakran érdemes szétválasztani, és sorolja fel egy közös listában a biztonsági és az alkalmazáshiba-eseményeket — nincs éles, mindenre kiterjedő szabály.

### 1.2 NIST SP 800-92 (Guide to Computer Security Log Management)

A hivatalos NIST-dokumentum (https://nvlpubs.nist.gov/nistpubs/legacy/SP/nistspecialpublication800-92.Pdf) **nem célja szerint** (biztonsági/audit vs. üzemeltetési), hanem **forrás szerint** kategorizálja a naplókat, 3 fő típussal:

> Security Software Logs (2.1.1): "Most organizations use several types of network-based and host-based security software to detect malicious activity, protect systems and data, and support incident response efforts."
> Operating System Logs (2.1.2): "Operating systems (OS) for servers, workstations, and networking devices (e.g., routers, switches) usually log a variety of information related to security."
> Application Logs (2.1.3): "Most organizations rely on a variety of commercial off-the-shelf (COTS) applications, such as e-mail servers and clients, Web servers and browsers, file servers and file sharing clients, and database servers and clients."
> — https://nvlpubs.nist.gov/nistpubs/legacy/SP/nistspecialpublication800-92.Pdf

Az audit rekordokat a NIST az OS-naplók egyik **alkategóriájaként** definiálja, nem önálló, elkülönítve kezelendő naplótípusként:

> "Audit records contain security event information such as successful and failed authentication attempts, file accesses, security policy changes, account changes..." (2.1.2 szakasz)
> — ugyanaz a dokumentum.

A dokumentum nem mondja ki, hogy a biztonsági/audit naplókat fizikailag el kell választani az üzemeltetési/teljesítmény-naplóktól. Amit kimond, az a naplóinfrastruktúra **elosztottságáról** szól (3.1 szakasz), praktikus (nem biztonsági) indokokkal:

> "For most organizations, a single infrastructure is not feasible for any of several reasons, including limitations on the scalability of a single infrastructure, logging occurring on logically or physically separate networks, concern about robustness (e.g., having a single infrastructure means that a failure of that infrastructure affects logging throughout the organization), and interoperability issues among log generators and infrastructure components."
> — https://nvlpubs.nist.gov/nistpubs/legacy/SP/nistspecialpublication800-92.Pdf, 3.1 szakasz

**Következtetés (kutatási, nem döntési):** a NIST SP 800-92 nem ad normatív szabályt arra, hogy az audit/biztonsági naplót fizikailag külön kell-e tartani az üzemeltetési (hiba/indulás/teljesítmény) naplótól; a szétválasztást gyakorlati/skálázhatósági okokkal indokolja, nem biztonsági/jogi kötelezettségként.

### 1.3 PCI DSS — 10. követelmény (audit log történet megőrzése)

A PCI DSS v4.0.1 hivatalos PDF-jét (pcisecuritystandards.org és tükrei) **nem sikerült közvetlenül elérni** — a hivatalos domain 403-at adott a lekérő eszköznek, egy Wayback Machine-tükröt pedig blokkolt a rendszer, egy egyetemi (middlebury.edu) tükörből pedig csak az 1–42. oldal jött le (a 10. követelmény a ~236. oldalon kezdődik, ez nem volt elérhető). **Emiatt a 10.5.1 pontos, szó szerinti szövegét nem tudom hitelesen idézni.** Több független, nem hivatalos másodforrás (RSI Security, NXLog, BasisTheory) egybehangzóan **saját megfogalmazásként** (nem elsődleges idézetként) közli, hogy a PCI DSS 10.5.1 pontja szerint az audit log history-t legalább 12 hónapig kell megőrizni, ebből a legutóbbi 3 hónapnak azonnal elérhetőnek kell lennie elemzésre — de ezt a számot **másodforrásból, nem az elsődleges szövegből ellenőrizve** közlöm.

---

## 2. Mit nem szabad naplózni + GDPR megőrzési idő

### 2.1 OWASP Logging Cheat Sheet — "Data to exclude" (teljes lista)

A hivatalos szöveg (raw GitHub forrásból, verbátim):

> "Never log data unless it is legally sanctioned. The following should usually not be recorded directly in the logs, but instead should be removed, masked, sanitized, hashed, or encrypted: Application source code, Session identification values, Access tokens, Sensitive personal data and PII, Authentication passwords, Database connection strings, Encryption keys and other primary secrets, Bank account or payment card holder data, Data of a higher security classification, Commercially-sensitive information, Information it is illegal to collect, Information a user has opted out of collection."
> — https://raw.githubusercontent.com/OWASP/CheatSheetSeries/master/cheatsheets/Logging_Cheat_Sheet.md (heading: "Data to exclude"), megerősítve a renderelt oldalon is: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html

Emellett a cheat sheet külön megjegyzi, hogy bizonyos adatok **különleges bánásmódot** igényelhetnek (nem tiltottak, de óvatosan kezelendők): fájl elérési utak, adatbázis kapcsolati stringek (kétszer is szerepel), belső hálózati nevek/címek, nem-érzékeny személyes adatok (pl. név, telefonszám, e-mail cím).

### 2.2 GDPR — hivatalos (EDPB / felügyeleti hatósági) állásfoglalás a naplók megőrzési idejéről

**Az EDPB (European Data Protection Board) szintjén nem található olyan hivatalos, EU-szintű dokumentum, amely konkrét számot adna meg általános üzemeltetési/biztonsági naplók megőrzési idejére.** Az edpb.europa.eu domainen célzott keresés (`site:edpb.europa.eu logging retention guidelines`) kizárólag olyan EDPB-dokumentumokat hozott, amelyek más témákról szólnak (arcfelismerés, adatalanyi hozzáférési jog, EDPB saját belső iratkezelése) — **egyik sem naplómegőrzési iránymutatás**.

Nemzeti szintű felügyeleti hatóságtól viszont van konkrét, hivatalos szám: a **CNIL (francia adatvédelmi hatóság)** 2021-es, naplózási intézkedésekről szóló hivatalos ajánlásában ezt írja (francia eredetiben, verbátim):

> "une journalisation permettant d'assurer une traçabilité des accès et des actions des différents utilisateurs habilités à accéder aux systèmes d'information pour une durée comprise entre six mois et un an"
> — https://www.cnil.fr/fr/la-cnil-publie-une-recommandation-relative-aux-mesures-de-journalisation

(magyarul kb.: a rendszerhez hozzáférő felhasználók hozzáféréseinek és műveleteinek nyomon követhetőségét biztosító naplózást **hat hónap és egy év közötti** időtartamra kell tartani)

és kiterjesztett esetre (belső kontroll célú feldolgozás):

> "qu'il est possible de justifier la conservation de données de journalisation pour une durée supérieure à un an, avec dans les cas les plus courants une durée maximale de trois ans"
> — ugyanaz a CNIL-oldal

(magyarul kb.: egy évnél hosszabb megőrzés is indokolható, a leggyakoribb esetekben legfeljebb **három év** maximális időtartamig)

**Explicit megállapítás:** nincs egységes, EU-szintű (EDPB) szám a naplók megőrzési idejére; ahol van konkrét hivatalos szám, az egy **nemzeti** felügyeleti hatóságtól (CNIL, Franciaország) származik, és még ott is tartomány (6 hónap–1 év, kivételesen max. 3 év), nem egyetlen fix szám.

---

## 3. Naplószintek: van-e objektív alapja a besorolásnak?

### 3.1 RFC 5424 — a nyolc súlyossági szint verbátim definíciója

A hivatalos IETF-szöveg (https://www.rfc-editor.org/rfc/rfc5424.txt, 6.2.1 "PRI" szakasz, 2. táblázat) szerint:

> ```
>            Numerical         Severity
>              Code
>
>               0       Emergency: system is unusable
>               1       Alert: action must be taken immediately
>               2       Critical: critical conditions
>               3       Error: error conditions
>               4       Warning: warning conditions
>               5       Notice: normal but significant condition
>               6       Informational: informational messages
>               7       Debug: debug-level messages
>
>               Table 2. Syslog Message Severities
> ```
> — https://www.rfc-editor.org/rfc/rfc5424.txt, 6.2.1 szakasz

**Kulcsfontosságú, magának az RFC-nek a saját nyilatkozata a normativitásról** (ugyanazon 6.2.1 szakasz, a Facility- és Severity-táblázatokra egyaránt vonatkozóan):

> "Facility and Severity values are not normative but often used. They are described in the following tables for purely informational purposes."
> — https://www.rfc-editor.org/rfc/rfc5424.txt, 6.2.1 szakasz

Tehát maga a szabvány mondja ki, hogy a súlyossági szintek **nem normatívak**, csak "gyakran használt", "tisztán informális célú" konvenciók.

Az elődje, az RFC 3164 (informational BSD syslog) ugyanezt a 8 szintet sorolja fel (azonos szöveggel), de nem tartalmaz kifejezett nyilatkozatot arról, hogy a súlyosság hozzárendelése implementátoronként "szubjektív" lenne — ez a pontos megfogalmazás a lekérésben nem volt fellelhető, ezért ezt az állítást **nem** idézem verbátimként.

### 3.2 Van-e bárhol mérés vagy elismert útmutató arról, melyik szintet mikor kell használni?

**Nem található ilyen.** Az RFC 5424 saját maga jelenti ki nem-normatívnak a szinteket (ld. fent). Az OpenTelemetry Logs specifikáció ad egy **keresztirányú megfeleltetési táblázatot** a gyakori elnevezési konvenciók (TRACE/DEBUG/INFO/WARN/ERROR/FATAL) és egy numerikus `SeverityNumber` tartomány között:

> | SeverityNumber tartomány | Név | Jelentés |
> |---|---|---|
> | 1-4 | TRACE | "A fine-grained debugging event. Typically disabled in default configurations." |
> | 5-8 | DEBUG | "A debugging event." |
> | 9-12 | INFO | "An informational event. Indicates that an event happened." |
> | 13-16 | WARN | "A warning event. Not an error but is likely more important than an informational event." |
> | 17-20 | ERROR | "An error event. Something went wrong." |
> | 21-24 | FATAL | "A fatal error such as application or system crash." |
> — https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/logs/data-model.md, "Field: SeverityNumber" szakasz

Ez azonban **megfeleltetési konvenció** (hogy különböző rendszerek szintnevei összevethetők legyenek), **nem mért vagy empirikusan levezetett** iránymutatás arra, hogy egy adott hibatípust melyik szinten kell naplózni. Explicit megállapítás: **nem található mért adat vagy hivatalos szabvány arra, hogy "mikor melyik szintet kell használni" — ez tisztán konvenció**, amit maga az RFC 5424 is kimond a saját szintjeire nézve.

---

## 4. Strukturált vs. sima szöveges napló

### 4.1 Twelve-Factor App — XI. Logs

A hivatalos szöveg (https://12factor.net/logs) verbátim (a lekérés angol nyelvű összefoglalása, a kulcsmondatok szó szerint idézve):

> "the stream of aggregated, time-ordered events collected from the output streams of all running processes and backing services"
> — https://12factor.net/logs (a logok definíciója)

> egy twelve-factor alkalmazás "never concern[s] itself with routing or storage of its output stream. It should not attempt to write to or manage logfiles. Instead, each running process writes its event stream, unbuffered, to stdout."
> — https://12factor.net/logs (a mag-elv; a lekérés parafrazált visszaadásában szerepel az "unbuffered... to stdout" kulcskifejezés, ez a Twelve-Factor App közismert, gyakran szó szerint idézett mondata)

**Megjegyzés a forrás pontosságáról:** a fenti második idézet a lekérő eszköz összefoglalójából származik, amely nagyrészt parafrazált; a "never concern itself with routing or storage of its output stream" és az "unbuffered to stdout" fordulatok a 12factor.net/logs oldal jól ismert, széles körben idézett eredeti mondatai, de ezt a kutatás nem tudta karakterre pontosan, nyers szövegként megerősíteni (a lekérés összefoglalva, nem nyers HTML-ként adta vissza a tartalmat).

### 4.2 OpenTelemetry Logs specifikáció — mezők és stabilitási státusz

A hivatalos specifikáció (https://opentelemetry.io/docs/specs/otel/logs/data-model/) tetején álló állapotjelzés:

> "**Status**: [Stable](https://opentelemetry.io/docs/specs/otel/document-status/)"
> — https://opentelemetry.io/docs/specs/otel/logs/data-model/

**A Log Data Model MA (2026-09-15-i állapot szerint, a lekérés idején) Stable.** A napló-rekord mezői (a stabil specifikáció szerint):

| Mező | Leírás (verbátim) |
|---|---|
| Timestamp | "Time when the event occurred." |
| ObservedTimestamp | "Time when the event was observed." |
| TraceId | "Request trace ID." |
| SpanId | "Request span ID." |
| TraceFlags | "W3C trace flag." |
| SeverityText | "The severity text (also known as log level)." |
| SeverityNumber | "Numerical value of the severity." |
| Body | "The body of the log record." |
| Resource | "Describes the observed entity that generated the log." |
| InstrumentationScope | "Describes the scope that emitted the log." |
| Attributes | "Additional information about the event." |
| EventName | "Name that identifies the class / type of event." |
| — https://opentelemetry.io/docs/specs/otel/logs/data-model/ |||

Fontos: az `EventName` mező és az "Event" fogalom (napló-rekord, aminek van neve) **külön, később hozzáadott** koncepció; a kutatás során nem sikerült igazolni, hogy ez a stabil specifikáció mely pontos verziójától stabil (a fő "Log Data Model" dokumentum egésze Stable, de ez nem jelenti azt, hogy annak minden almezője az elejétől fogva ott volt — ez explicit rés, ld. lentebb).

---

## 5. Forgatás és megőrzés egyetlen gépen

### 5.1 logrotate(8) man oldal

A hivatalos man oldal (https://man7.org/linux/man-pages/man8/logrotate.8.html) verbátim:

**A `rotate count` opció és alapértelmezése:**

> "Log files are rotated count times before being removed or mailed to the address specified in a mail directive. If count is 0, old versions are removed rather than rotated. If count is -1, old logs are not removed at all, except they are affected by maxage (use with caution, may waste performance and disk space). Default is 0."
> — https://man7.org/linux/man-pages/man8/logrotate.8.html

Vagyis a logrotate **eszköz saját alapértelmezése a `rotate` paraméterre 0** — azaz explicit konfiguráció nélkül a régi naplóváltozatokat **eltávolítja, nem archiválja**. Bármilyen ténylegesen használt megőrzési szám (pl. a legtöbb Linux-disztribúció `/etc/logrotate.conf`-jában megszokott `rotate 4`) **a disztribúció döntése**, nem a logrotate beépített viselkedése.

**Nincs beépített méret- vagy időküszöb sem** — a `size`, `daily`, `weekly`, `monthly` mind explicit konfigurációs direktívák, alapértelmezett érték/küszöb nélkül:

> "size: Log files are rotated only if they grow bigger than size bytes. If size is followed by k, the size is assumed to be in kilobytes. If M is used, the size is in megabytes, and if G is used, the size is in gigabytes."
> — https://man7.org/linux/man-pages/man8/logrotate.8.html

> "logrotate is designed to ease administration of systems that generate large numbers of log files. It allows automatic rotation, compression, removal, and mailing of log files. Each log file may be handled daily, weekly, monthly, or when it grows too large. Normally, logrotate is run as a daily cron job (or by logrotate.timer when using systemd(1))."
> — https://man7.org/linux/man-pages/man8/logrotate.8.html (DESCRIPTION szakasz)

**Explicit megállapítás:** a logrotate önmagában nem forgat semmit — külső ütemezőtől (cron/`logrotate.timer`) és explicit konfigurációtól függ; a beépített egyetlen numerikus alapértelmezés (`rotate`=0) is a "ne őrizz meg semmit" irányba mutat.

### 5.2 systemd-journald.conf(5) man oldal

A hivatalos man oldal (https://www.man7.org/linux/man-pages/man5/journald.conf.5.html) verbátim, a méretkorlátokról:

> "SystemMaxUse= and RuntimeMaxUse= control how much disk space the journal may use up at most... The first pair defaults to 10% and the second to 15% of the size of the respective file system, but each of the calculated default values is capped to 4G."
> — https://www.man7.org/linux/man-pages/man5/journald.conf.5.html

> "SystemKeepFree= and RuntimeKeepFree= control how much disk space systemd-journald shall leave free for other uses... The first pair defaults to 10% and the second to 15% of the size of the respective file system, but each of the calculated default values is capped to 4G."
> — ugyanaz a man oldal

> "SystemMaxFileSize= and RuntimeMaxFileSize= control how large individual journal files may grow at most... Defaults to one eighth of the values configured with SystemMaxUse= and RuntimeMaxUse= capped to 128M, so that usually seven rotated journal files are kept as history."
> — ugyanaz a man oldal

> "SystemMaxFiles= and RuntimeMaxFiles= control how many individual journal files to keep at most... This setting defaults to 100."
> — ugyanaz a man oldal

Az időalapú korlátokról:

> MaxFileSec=: "The maximum time to store entries in a single journal file before rotating to the next one." — alapértelmezés: **"one month"**.
> — https://www.man7.org/linux/man-pages/man5/journald.conf.5.html

> MaxRetentionSec=: "The maximum time to store journal entries. This controls whether journal files containing entries older than the specified time span are deleted." — alapértelmezés: **"0 (which turns off this feature)"**.
> — https://www.man7.org/linux/man-pages/man5/journald.conf.5.html

**Explicit megállapítás:** a journald alapból **méret alapján** (10% lemez, max 4G, max 100 fájl, fájlonként max 1/8 rész / 128M) korlátoz és forgat, **idő alapján viszont alapból NEM töröl** (`MaxRetentionSec=0` = kikapcsolva) — csak a fájlonkénti forgatási időköz (`MaxFileSec`) van alapból beállítva, egy hónapra.

---

## 6. Mit tesznek ténylegesen az önüzemeltetett, egybináris projektek?

### 6.1 Forgejo / Gitea (közös eredetű, gyakorlatilag azonos naplózási rendszer)

Forgejo hivatalos dokumentáció (https://forgejo.org/docs/latest/admin/troubleshooting/logging/):

> "Possible values, sorted by increasing severity, are: `Trace`, `Debug`, `Info`, `Warn`, `Error`, `Fatal`."
> — https://forgejo.org/docs/latest/admin/troubleshooting/logging/

> "There is a fully functional log output by default, so it is not necessary to define one." (alapból konzolra megy a log)
> — ugyanaz az oldal

> "Forgejo includes built-in log rotation, which should be enough for most deployments."
> — ugyanaz az oldal

Beépített forgatási alapértékek (fájl módban):

> "MAX_SIZE_SHIFT: 28: Maximum size shift of a single file. 28 represents 256Mb." / "LOG_ROTATE true: Whether to rotate the log files." / "DAILY_ROTATE: true: Whether to rotate logs daily." / "MAX_DAYS: 7: Delete rotated log files after this number of days." / "COMPRESS: true: Whether to compress old log files by default with gzip."
> — ugyanaz az oldal

Gitea hivatalos dokumentációja (https://docs.gitea.com/administration/logging-config/) **szó szerint ugyanezt** a szintnevet és rotációs alapértéket adja meg (`MODE` alapból **console**), ami megerősíti, hogy a Forgejo ezen a ponton öröklte a Gitea rendszerét.

Egyik projekt sem beszél külön "audit" naplóról — egyetlen, szintezett üzemeltetési naplófolyam van, aminek a legrészletesebb szintje (`Trace`) tartalmazhat biztonsági jellegű eseményeket is, de ez nincs elkülönítve.

### 6.2 Miniflux

Hivatalos dokumentáció (https://miniflux.app/docs/configuration.html):

> LOG_LEVEL: "Supported values are `debug`, `info`, `warning`, or `error`." — alapértelmezés: `info`
> LOG_FILE: "Supported values are `stderr`, `stdout`, or a file name." — alapértelmezés: `stderr`
> LOG_FORMAT: "Supported log formats are `text` or `json`." — alapértelmezés: `text`
> — https://miniflux.app/docs/configuration.html

Csak **4 szint**, alapból **stderr**-re ír (nem fájlba!), formátuma választható szöveg vagy JSON. Nincs beépített forgatás említve — fájlba írás esetén ez explicit módon a rendszergazda/OS feladata.

### 6.3 Syncthing

Hivatalos dokumentáció (https://docs.syncthing.net/users/syncthing.html):

> `--log-file=<filename>` ($STLOGFILE): "Set destination filename for logging (use "-" for stdout, which is the default option)."
> `--log-level=<level>` ($STLOGLEVEL): "Set the log level for all packages. Valid levels are DEBUG, INFO, WARN, and ERROR."
> `--log-max-size=<num>` ($STLOGMAXSIZE): "Maximum size in bytes of any log file (zero to disable log rotation)."
> `--log-max-old-files=<num>` ($STLOGMAXOLDFILES): "Number of old files to keep (zero to keep only current). Applies only when log rotation is enabled through --log-max-size."
> — https://docs.syncthing.net/users/syncthing.html

Csak **4 szint** (DEBUG/INFO/WARN/ERROR), alapból **stdout**-ra ír, és a forgatás **explicit ki van kapcsolva alapból** (`zero to disable log rotation` — a log-max-size alapértéke 0).

### 6.4 Vaultwarden

Hivatalos wiki (https://github.com/dani-garcia/vaultwarden/wiki/Logging):

> "vaultwarden logs only to standard output (stdout) by default."
> "You can specify the path to the log file with the LOG_FILE environment variable" — és ha be van állítva: "When this environment variable is set, log messages will be logged to both stdout and the log file."
> LOG_LEVEL lehetséges értékek: "trace", "debug", "info", "warn", "error" or "off" (`EXTENDED_LOGGING=true` szükséges hozzá)
> — https://github.com/dani-garcia/vaultwarden/wiki/Logging

Log-forgatásra a Vaultwarden nem ad beépített funkciót — a wiki egy **külön oldalt** ("Logrotate example") tart fenn, ami kifejezetten az OS `logrotate` eszközére támaszkodó példakonfigurációt ad, azaz a szétválasztás explicit: **a naplózás a projekt dolga, a forgatás a rendszeré**.

### 6.5 Összegzés a 4 projektről

Egyik vizsgált projekt sem tart fenn külön, elkülönített "audit naplót" a hibaüzenetektől — egyetlen, szintezett üzemeltetési naplófolyamuk van. A szintek száma **4-6 között mozog** (Miniflux/Syncthing: 4; Vaultwarden: 5-6; Forgejo/Gitea: 6) — jóval kevesebb, mint az RFC 5424 8 szintje; egyik projekt sem használja az "Emergency", "Alert", "Critical" vagy "Notice" elnevezéseket. Az alapértelmezett célpont vegyes: van, ami konzolra/stdoutra ír alapból (Gitea/Forgejo, Miniflux, Syncthing, Vaultwarden mind ezt teszi), és csak explicit bekapcsolásra ír fájlba is. A forgatás kezelése megoszlik: Forgejo/Gitea **saját beépített** forgatót ad (méret- és napalapú, alapból be van kapcsolva), míg Miniflux, Syncthing és Vaultwarden **nem** ad ilyet (Syncthing-nél explicit ki is van kapcsolva alapból), és a rendszergazdára / OS logrotate-re bízzák.

---

## 7. Naplózás mint teljesítménykockázat

### 7.1 Van-e hivatalos, publikált szám?

**A vizsgált hivatalos projektoldalakon (Apache Log4j2, Logback) nem található konkrét, számszerű, "szinkron írás X%-kal lassabb" jellegű hivatalos állítás.** A Log4j2 hivatalos teljesítmény-oldala (https://logging.apache.org/log4j/2.x/manual/performance.html) csak minőségi kijelentéseket tesz ("Higher peak throughput", "Lower logging latency" az aszinkron naplózás mellett), konkrét szám nélkül. A Logback hivatalos oldala (https://logback.qos.ch/performance.html) áteresztőképesség-összehasonlítást ad több szálra, de nem egy általános "hányszor lassabb a szinkron fájlírás" mutatót.

### 7.2 Van-e mért adat egyáltalán?

Igen, de **implementáció-specifikus, nem hivatalos/szabványos** mérésekről van szó. A Nearform (Node.js `pino` naplózókönyvtár egyik fő fejlesztőjének cége) 2022-es, publikált benchmarkja (https://nearform.com/insights/the-cost-of-logging-in-2022/) konkrét számokat közöl:

> Alap (naplózás nélkül): kb. 11 000+ kérés/mp
> "Running a server using bunyan for logging will reduce throughput by almost 70%" (kb. 3300 kérés/mp-re esik vissza)
> "Running a server using Winston (version 2) for logging will slow you down by almost 50%" (kb. 5500 kérés/mp)
> — https://nearform.com/insights/the-cost-of-logging-in-2022/

Szinkron vs. aszinkron írás (ugyanazon a `pino` könyvtáron belül):

> "We get around 20% more throughput when using Asynchronous logging" — szinkron kb. 9000+ kérés/mp, aszinkron kb. 10 800+ kérés/mp.
> — https://nearform.com/insights/the-cost-of-logging-in-2022/

**Explicit megállapítás:** ez **egyetlen ökoszisztéma (Node.js), egyetlen gyártó saját mérése**, nem független/hivatalos benchmark, és a szórás óriási (20%–70% közötti throughput-csökkenés, kizárólag a választott naplózókönyvtártól függően). **Nincs olyan hivatalos, általánosan elismert, nyelv-/keretrendszer-független szám, ami megmondaná, hogy egy szinkron fájlba írás mennyivel lassítja a kérésfeldolgozást** egy tetszőleges (pl. Python/Node/Go, egyetlen felhasználós, egyetlen gépes) rendszerben. A hatás nagyságrendje kimutathatóan a konkrét implementáción (pufferelt vs. pufferelés nélküli írás, szinkron `fsync` megléte, stb.) múlik, nem egy általánosítható konstans.

---

## Amire NINCS publikált válasz

- **Nincs olyan szabvány vagy hivatalos útmutató, amely kötelezővé tenné, hogy az "audit napló" és az "üzemeltetési napló" fizikailag/technikailag külön fájlban/rendszerben legyen.** Az OWASP csak azt mondja, hogy céljuk miatt "gyakran" indokolt a szétválasztás, konkrét technikai előírás nélkül. A NIST SP 800-92 forrás szerint kategorizál, nem cél szerint, és nem ír elő fizikai szétválasztást.
- **Nincs EU-szintű (EDPB) hivatalos állásfoglalás konkrét számmal az üzemeltetési/biztonsági naplók megőrzési idejéről.** Célzott edpb.europa.eu keresés nem hozott releváns találatot. Ahol van konkrét szám, az egy nemzeti hatóságtól (CNIL, Franciaország) származik, és az is tartomány (6 hónap–1 év, kivételesen legfeljebb 3 év), nem egyetlen kötelező érték.
- **Nincs igazolt, verbátim hozzáférésű PCI DSS 10.5.1 szöveg** — a hivatalos PCI SSC domain és tükrei (Wayback Machine, egyetemi tükör) mind elérhetetlenek voltak a kutatás eszközei számára; a széles körben terjedő "12 hónap / 3 hónap azonnal elérhető" szám kizárólag másodforrásokból (nem elsődleges szövegből) igazolt.
- **Nincs mért vagy hivatalos útmutató arra, hogy az RFC 5424 nyolc szintje közül melyiket mikor kell használni** — maga az RFC mondja ki, hogy a szintek nem normatívak, "tisztán informális célúak". Az OpenTelemetry `SeverityNumber` táblázata csak elnevezés-megfeleltetés, nem "mikor melyiket használd" iránymutatás.
- **Nincs hivatalos, keretrendszer-független szám arra, hogy a szinkron fájlba írás mennyivel lassítja a kérésfeldolgozást.** Csak egyetlen ökoszisztémára (Node.js) vonatkozó, gyártói (Nearform/pino) benchmark van, 20%–70% közötti, könyvtárfüggő szórással; ez nem általánosítható egy tetszőleges, egyetlen felhasználós, markdown-fájl-alapú rendszerre.
- **A Twelve-Factor App XI. Logs fejezetének nyers, szó szerinti szövegét nem sikerült karakterre pontosan, nyers HTML-ként megerősíteni** — a lekért tartalom parafrazált összefoglaló volt, bár a kulcskifejezések ("unbuffered... to stdout", "never concern itself with routing or storage") a széles körben ismert eredeti szöveggel egyeznek.
- **Nem világos, hogy az OpenTelemetry Logs Data Model teljes mezőkészlete (pl. `EventName`) mikortól számít a "Stable" besorolás részének** — maga a dokumentum összességében Stable, de a kutatás nem tudta megállapítani, hogy ez a konkrét mező is a kezdetektől stabil volt-e, vagy később, esetleg még kísérleti státuszból került át.

---



---

# SQ04 — Indulás, újraindítás és összeomlás utáni helyreállás

**Módszertani megjegyzés:** ez a jegyzet a `deep-web-research` skill elvei szerint készült (elsődleges/hivatalos forrás előnyben, szó szerinti idézetek, minden állítás nyomon követhető forrásig), de a skill teljes, több-ügynökös (Sonnet-keresés + Opus-szintézis + külön verifikációs kör) gépezete nélkül, mert ez a munkamenet egyetlen kutató-alügynökként, Agent/subagent-dispatch eszköz nélkül fut. A lenti minden idézetet én magam olvastam ki a nyers forrásból (letöltött HTML/XML, `grep`-pel ellenőrizve), nem csak egy összefoglaló-eszköz kimenetéből — de a szokásos többkörös keresztellenőrzés (külön Sonnet-verifikátorok) elmaradt. A pontos alapértékeket (RestartSec, StartLimitBurst/IntervalSec, TimeoutStopSec, ThrottleInterval) kizárólag hivatalos man-oldal / hivatalos forráskód alapján közlöm, verzióval együtt; ahol nincs hivatalos szám, azt explicit kimondom.

## Összefoglaló

SQLite WAL módban a hivatalos dokumentáció szerint összeomlás után a következő megnyitás automatikusan "recovery process"-t indít, kizárólagos zárral; ez a rollback-journal módban jól dokumentált "hot journal" fogalom WAL-ra is kiterjed ("hot WAL file"), a wal-index (`-shm` fájl) pedig kifejezetten **tranziens**, és a dokumentáció szerint "After a crash, the wal-index is reconstructed from the original WAL file" — ez a legközelebbi hivatalos válasz arra, mi történik ha a `-shm` hiányzik. Sérült/csonka WAL-keretek kezelését csak a fájlformátum-specifikáció checksum-lánca írja le közvetetten, nincs külön "korrupt WAL" fejezet. systemd oldalon a `Restart=` opció mind a hét dokumentált értékét (no, on-success, on-failure, on-abnormal, on-watchdog, on-abort, always) szó szerint idézem, a `RestartSec=` alapértéke **100ms**, a `DefaultStartLimitIntervalSec=` **10s**, a `DefaultStartLimitBurst=` **5**, a `DefaultTimeoutStopSec=` (build-alapértelmezés) **90s** — mindegyik a systemd hivatalos forráskódjából/man-oldalából, systemd 260–261 környéki állapot szerint. macOS launchd oldalon a `ThrottleInterval` hivatalos man-oldali szövege kimondja: "by default, jobs will not be spawned more than once every 10 seconds" — ez a keresett 10 másodperces alapérték pontos forrása. Index-újraépítés sebességére (sor/mp, MB/mp) **sehol nem találtam hivatalosan publikált számot** — sem a SQLite FTS5 `rebuild` parancsnál, sem Elasticsearch/OpenSearch/Meilisearch/Typesense dokumentációjában; ezek a rendszerek helyette minőségi állapotgépeket dokumentálnak (pl. OpenSearch `INIT/INDEX/VERIFY_INDEX/TRANSLOG/FINALIZE/DONE` recovery-fázisok, Elasticsearch piros/sárga klaszter-állapot, Meilisearch `enqueued/processing/succeeded/failed/canceled` feladatállapotok). Az Elasticsearch hivatalos dokumentációja kifejezetten leírja a degradált kiszolgálás mintáját: sárga/piros állapotban "it will continue to process searches and indexing where possible". Tiszta leállásnál a SQLite dokumentáció szerint az utolsó kapcsolat lezárásakor a könyvtár automatikusan checkpointol, az alkalmazásnak csak a `sqlite3_close()`/`sqlite3_close_v2()` hívást kell helyesen elvégeznie; systemd oldalon a `TimeoutStopSec=` lejártakor a szolgáltatás `SIGKILL`-t kap.

---

## 1. SQLite WAL mód összeomlás utáni viselkedése

### 1.1 Mi történik a következő megnyitáskor (recovery process)

A `sqlite.org/wal.html` 9. szakasza ("Sometimes Queries Return SQLITE_BUSY In WAL Mode") kifejezetten leírja a recovery-folyamatot:

> "If the last connection to a database crashed, then the first new connection to open the database will start a recovery process. An exclusive lock is held during recovery."
> — [sqlite.org/wal.html](https://sqlite.org/wal.html), 9. szakasz

A wal-index (a `-shm` fájl tartalma) tranziens jellegét és a helyreállítás mechanizmusát a fájlformátum-specifikáció írja le explicit módon:

> "The wal-index is transient. After a crash, the wal-index is reconstructed from the original WAL file. The VFS is required to either truncate or zero the header of the wal-index when the last connection to it closes."
> — [sqlite.org/fileformat2.html](https://sqlite.org/fileformat2.html), 4.6. WAL-Index Format

Ez az egyetlen explicit hivatalos állítás arra a kérdésre, hogy "mit garantál a recovery" — magára a wal-index szerkezetére vonatkozik (mindig újraépíthető a WAL-ból), nem egy külön, "WAL crash recovery guarantees" című fejezetből.

### 1.2 Garanciák és nem-garanciák

Az atomicitásra vonatkozó általános garanciát az `atomiccommit.html` mondja ki (ez rollback-journal módra íródott, de a bevezetőben explicit kiterjeszti WAL-ra is):

> "SQLite has the important property that transactions appear to be atomic even if the transaction is interrupted by an operating system crash or power failure."
> — [sqlite.org/atomiccommit.html](https://sqlite.org/atomiccommit.html), 1. szakasz

> "The information in this article applies only when SQLite is operating in 'rollback mode', or in other words when SQLite is not using a write-ahead log. SQLite still supports atomic commit when write-ahead logging is enabled, but it accomplishes atomic commit by a different mechanism from the one described in this article."
> — [sqlite.org/atomiccommit.html](https://sqlite.org/atomiccommit.html), 1. szakasz

Amit a `wal.html` **nem** garantál — a `-wal` fájl és az adatbázisfájl szétválasztása esetére kifejezett figyelmeztetés van:

> "The WAL file is part of the persistent state of the database and should be kept with the database if the database is copied or moved. If a database file is separated from its WAL file, then transactions that were previously committed to the database might be lost, or the database file might become corrupted."
> — [sqlite.org/wal.html](https://sqlite.org/wal.html), 4. szakasz ("The WAL File")

A tartósság (durability) feladása NORMAL szinkronizálási móddal szintén explicit dokumentált nem-garancia:

> "…transactions are no longer durable and might rollback following a power failure or hard reset."
> — [sqlite.org/wal.html](https://sqlite.org/wal.html), 2.1. Checkpointing

### 1.3 Mi történik, ha a `-wal` megvan, de a `-shm` hiányzik

Erre a pontos forgatókönyvre **nincs külön, névvel megcímzett** hivatalos szakasz. A legközelebbi hivatalos válasz a fent (1.1) idézett "the wal-index is reconstructed from the original WAL file" mondat — mivel a `-shm` fájl éppen a wal-index háttértárolója, ebből következik (de a dokumentáció ezt nem mondja ki ilyen konkrét megfogalmazásban), hogy egy hiányzó `-shm` mellett történő megnyitás új `-shm`-et hoz létre és a wal-indexet a `-wal` tartalmából építi újra recovery közben. Emellett a 7. szakasz megerősíti, hogy a wal-index fájl önmagában sosem tekinthető a séma tartós részének:

> "the wal-index backing file is deleted when the last database connection disconnects, which often prevents any real disk I/O from ever happening."
> — [sqlite.org/wal.html](https://sqlite.org/wal.html), 7. szakasz

A 8. szakasz ("Use of WAL Without Shared-Memory") azt is dokumentálja, hogy létezik egy üzemmód, amiben eleve **nincs** `-shm` fájl (EXCLUSIVE locking mode, egyetlen folyamat esetén):

> "If EXCLUSIVE locking mode is set prior to the first WAL-mode database access, then SQLite never attempts to call any of the shared-memory methods and hence no shared-memory wal-index is ever created."
> — [sqlite.org/wal.html](https://sqlite.org/wal.html), 8. szakasz

### 1.4 Mi történik, ha a WAL fájl sérült

Nincs a sqlite.org dokumentációban külön "corrupted WAL" című fejezet. A tényleges védelmi mechanizmust a `fileformat2.html` írja le: minden WAL-keret ("frame") csak akkor érvényes, ha a saltok és a checksum-lánc egyezik:

> "A frame is considered valid if and only if the following conditions are true: The salt-1 and salt-2 values in the frame-header match salt values in the wal-header. The checksum values in the final 8 bytes of the frame-header exactly match the checksum computed consecutively on the first 24 bytes of the WAL header and the first 8 bytes and the content of all frames up to and including the current frame."
> — [sqlite.org/fileformat2.html](https://sqlite.org/fileformat2.html), 4.1/4.5 (Reader Algorithm előtti definíció)

Ebből a leírásból következik (de a dokumentáció ezt nem mondja ki külön "sérülés esetén ez történik" formában), hogy egy csonka vagy sérült WAL-ban az első érvénytelen checksumú kerettől kezdve a tartalom nem kerül visszajátszásra — a rendszer úgy viselkedik, mintha az a tranzakció soha nem történt volna meg. Ez implicit, nem explicit dokumentált viselkedés.

### 1.5 "Hot journal" és a dokumentált recovery-folyamat

A "hot journal" fogalom **igen, hivatalosan dokumentált**, mégpedig két helyen. A fájlformátum-dokumentum explicit kiterjeszti a fogalmat WAL-ra is:

> "When a rollback journal or write-ahead log contains information necessary for recovering the state of the database, they are called a 'hot journal' or 'hot WAL file'. Hot journals and WAL files are only a factor during error recovery scenarios and so are uncommon, but they are part of the state of an SQLite database and so cannot be ignored."
> — [sqlite.org/fileformat2.html](https://sqlite.org/fileformat2.html), bevezető (2. szakasz környéke)

Az `atomiccommit.html` (rollback-journal módra) tételesen leírja a teljes recovery-algoritmust, pontos feltételekkel, mikor számít egy journal "hot"-nak:

> "SQLite then checks to see if the rollback journal is a 'hot journal'. A hot journal is a rollback journal that needs to be played back in order to restore the database to a sane state. A hot journal only exists when an earlier process was in the middle of committing a transaction when it crashed or lost power."
> — [sqlite.org/atomiccommit.html](https://sqlite.org/atomiccommit.html), 4.2. Determining If A Journal is Hot

> "A rollback journal is a 'hot' journal if all of the following are true: The rollback journal exists. The rollback journal is not an empty file. There is no reserved lock on the main database file. The header of the rollback journal is well-formed and in particular has not been zeroed out. The rollback journal does not contain the name of a super-journal file… or if [it] does…, then that super-journal file exists."
> — [sqlite.org/atomiccommit.html](https://sqlite.org/atomiccommit.html), 4.2.

> "The first step toward dealing with a hot journal is to obtain an exclusive lock on the database file. This prevents two or more processes from trying to rollback the same hot journal at the same time."
> — [sqlite.org/atomiccommit.html](https://sqlite.org/atomiccommit.html), 4.3.

> "Once a process obtains an exclusive lock, it is permitted to write to the database file. It then proceeds to read the original content of pages out of the rollback journal and write that content back to where it came from in the database file. […] At the end of this step, the database should be the same size and contain the same information as it did before the start of the aborted transaction."
> — [sqlite.org/atomiccommit.html](https://sqlite.org/atomiccommit.html), 4.4.

WAL módban a formális algoritmus lépéseit (4.2–4.5 pontok) a `wal.html`/`fileformat2.html` nem írja le ilyen tételes formában — csak azt, hogy "recovery process" indul, kizárólagos zárral (l. 1.1), és hogy a wal-index a WAL-ból újraépül.

---

## 2. Folyamatfelügyelet egy gépen

### 2.1 systemd `Restart=` — összes érték szó szerint

Forrás: a systemd hivatalos man-oldalának forrása (`systemd.service.xml`, upstream `main` ág), amit a Debian testing csomagolt man-oldala (systemd 260.1, csomag: 261.2-1) tartalmilag megerősít.

> "Takes one of **no**, **on-success**, **on-failure**, **on-abnormal**, **on-watchdog**, **on-abort**, or **always**. If set to **no** (the default), the service will not be restarted. If set to **on-success**, it will be restarted only when the service process exits cleanly. […] If set to **on-failure**, the service will be restarted when the process exits with a non-zero exit code, is terminated by a signal (including on core dump, but excluding the aforementioned four signals), when an operation (such as service reload) times out, and when the configured watchdog timeout is triggered. If set to **on-abnormal**, the service will be restarted when the process is terminated by a signal (including on core dump, excluding the aforementioned four signals), when an operation times out, or when the watchdog timeout is triggered. If set to **on-abort**, the service will be restarted only if the service process exits due to an uncaught signal not specified as a clean exit status. If set to **on-watchdog**, the service will be restarted only if the watchdog timeout for the service expires. If set to **always**, the service will be restarted regardless of whether it exited cleanly or not, got terminated abnormally by a signal, or hit a timeout."
> — [systemd.service man-oldal forrása (GitHub, upstream)](https://raw.githubusercontent.com/systemd/systemd/main/man/systemd.service.xml), `Restart=` szakasz

("Clean exit" pontos definíciója ugyanitt: exit code 0; vagy — Type=oneshot kivételével — a SIGHUP, SIGINT, SIGTERM, SIGPIPE jelek egyike; vagy a `SuccessExitStatus=`-ban felsorolt kódok/jelek.)

### 2.2 `RestartSec=`, `StartLimitBurst=`, `StartLimitIntervalSec=` — pontos alapértékek

> "Configures the time to sleep before restarting a service (as configured with Restart=). Takes a unit-less value in seconds, or a time span value such as '5min 20s'. **Defaults to 100ms.**"
> — [systemd.service.xml](https://raw.githubusercontent.com/systemd/systemd/main/man/systemd.service.xml), `RestartSec=`

> "Configure unit start rate limiting. Units which are started more than *burst* times within an *interval* time span are not permitted to start any more. […] Defaults to DefaultStartLimitIntervalSec= in manager configuration file, and may be set to 0 to disable any kind of rate limiting. *burst* is a number and defaults to DefaultStartLimitBurst= in manager configuration file."
> — [systemd.unit.xml](https://raw.githubusercontent.com/systemd/systemd/main/man/systemd.unit.xml), `StartLimitIntervalSec=` / `StartLimitBurst=`

A tényleges alapszámokat a `systemd-system.conf` man-oldal mondja ki:

> "DefaultStartLimitIntervalSec= defaults to 10s. DefaultStartLimitBurst= defaults to 5."
> — [systemd-system.conf.xml](https://raw.githubusercontent.com/systemd/systemd/main/man/systemd-system.conf.xml), `DefaultStartLimitIntervalSec=`/`DefaultStartLimitBurst=` (bevezetve: v209)

**Tehát: `RestartSec=100ms`, `StartLimitIntervalSec=10s`, `StartLimitBurst=5`** — mind a systemd upstream forráskódjából (jelenlegi `main` ág, amit a Debian 260.1/261.2-1 man-oldala szó szerint megerősít).

### 2.3 Mi történik, ha a szolgáltatás gyorsabban hal meg, mint a limit

A `StartLimitIntervalSec=`/`StartLimitBurst=` leírás explicit kimondja a rate-limit hatását ("not permitted to start any more"), a `StartLimitAction=` opció pedig a rálépés utáni további cselekvést szabályozza:

> "Configure an additional action to take if the rate limit configured with StartLimitIntervalSec= and StartLimitBurst= is hit. Takes the same values as the FailureAction=/SuccessAction= settings. If **none** is set, hitting the rate limit will trigger no action except that the start will not be permitted. Defaults to **none**."
> — [systemd.unit.xml](https://raw.githubusercontent.com/systemd/systemd/main/man/systemd.unit.xml), `StartLimitAction=`

Vagyis alapértelmezésben a szolgáltatás egyszerűen nem indul újra tovább (a unit "failed" állapotban marad), semmilyen extra akció (pl. reboot) nem történik, hacsak a `StartLimitAction=` explicit be nincs állítva.

### 2.4 macOS launchd — `KeepAlive` és `ThrottleInterval`

Forrás: a `launchd.plist(5)` man-oldal (a manpagez.com tükrözésében; ez a Darwin nyílt forráskódú man-oldal tartalma, dátuma "1 May, 2009", Mac OS X 10.9-hez generált tükrözés — ugyanez a szöveg jelenik meg lényegében változatlanul a mai macOS-eken futtatott `man launchd.plist` paranccsal is, de ezt ebben a munkamenetben közvetlenül Apple-forrásból nem tudtam újra letölteni, l. a link-táblázatot).

> "**KeepAlive** \<boolean or dictionary of stuff\> This optional key is used to control whether your job is to be kept continuously running or to let demand and conditions control the invocation. **The default is false** and therefore only demand will start the job. The value may be set to true to unconditionally keep the job alive. Alternatively, a dictionary of conditions may be specified to selectively control whether launchd keeps a job alive or not. If multiple keys are provided, launchd ORs them… Jobs that exit quickly and frequently when configured to be kept alive will be throttled to converve system resources."
> — [launchd.plist(5), manpagez.com tükrözés](https://www.manpagez.com/man/5/launchd.plist/), `KeepAlive` kulcs

> "**ThrottleInterval** \<integer\> This key lets one override the default throttling policy imposed on jobs by launchd. The value is in seconds, and **by default, jobs will not be spawned more than once every 10 seconds.** The principle behind this is that jobs should linger around just in case they are needed again in the near future."
> — [launchd.plist(5), manpagez.com tükrözés](https://www.manpagez.com/man/5/launchd.plist/), `ThrottleInterval` kulcs

Ez a pontos, hivatalos forrása a 10 másodperces alapértéknek. Fontos: ez egy **fix cooldown**, nincs hozzá dokumentált "burst counter" vagy "adott időn belül N-szer" jellegű számláló, és nincs dokumentált "trvalefailed"/tartósan meghibásodott állapot — a man-oldal egyetlen ilyen mechanizmust ír le (l. 3. szakasz).

Leállításhoz kapcsolódó launchd-alapérték is van a man-oldalon:

> "**ExitTimeOut** \<integer\> The amount of time launchd waits before sending a SIGKILL signal. **The default value is 20 seconds.** The value zero is interpreted as infinity."
> — [launchd.plist(5), manpagez.com tükrözés](https://www.manpagez.com/man/5/launchd.plist/), `ExitTimeOut` kulcs

---

## 3. Eltérés systemd és launchd között

Ez a szakasz mindkét projekt saját hivatalos dokumentációjának összevetése — nincs egyetlen hivatalos "systemd vs launchd" összehasonlító dokumentum, ezért az alábbi pontok az én saját összevetésem a két elsődleges forrás alapján, nem egy harmadik fél állítása.

**Amit a systemd dokumentál, és a launchd.plist man-oldalán nincs megfelelője:**

- **cgroup-alapú erőforrás-kvóta.** systemd: "This setting controls the cpu controller in the unified hierarchy. Assign the specified CPU time quota to the processes executed. Takes a percentage value…" ([systemd.resource-control.xml](https://raw.githubusercontent.com/systemd/systemd/main/man/systemd.resource-control.xml), `CPUQuota=`) — és hasonlóan `MemoryMax=`, `IOWeight=` stb. A launchd.plist man-oldal ezzel szemben csak POSIX `setrlimit(2)`-alapú korlátokat ismer: "Resource limits to be imposed on the job. These adjust variables set with setrlimit(2)." ([launchd.plist(5)](https://www.manpagez.com/man/5/launchd.plist/), `SoftResourceLimits`/`HardResourceLimits`) — ez lényegesen durvább eszköz (pl. `ResidentSetSize`, `NumberOfFiles`, `CPU` másodpercben), nincs benne arányos CPU-kvóta vagy I/O-súlyozás fogalma.
- **Explicit rate-limit számláló tartós hibaállapottal.** systemd: `StartLimitIntervalSec=`/`StartLimitBurst=` + `StartLimitAction=` (l. 2.2–2.3). A launchd.plist man-oldalon ennek nincs dokumentált megfelelője — csak a `ThrottleInterval` fix cooldown létezik, "tartósan failed" unit-állapot fogalma nélkül.
- **Deklaratív unit-függőségi gráf tetszőleges egységtípusok között.** systemd: "Configures (weak) requirement dependencies on other units… Wants=" és "Requires=… declares a stronger requirement dependency" és "Before=/After=… These two settings expect a space-separated list of unit names" ([systemd.unit.xml](https://raw.githubusercontent.com/systemd/systemd/main/man/systemd.unit.xml)). A launchd.plist man-oldalon a legközelebbi eszköz az `OtherJobEnabled` kulcs ("Each key in this dictionary is the label of another job… kept alive as long as that other job is enabled/disabled"), ami jóval korlátozottabb — csak boolean "él-e a másik job" reláció, nincs explicit indítási sorrend (`Before=`/`After=`) fogalom.
- **Readiness-jelzés protokoll (`sd_notify`/`Type=notify`).** systemd: "it is expected that the service sends a READY=1 notification message via sd_notify… systemd will proceed with starting follow-up units after this notification message has been sent." ([systemd.service.xml](https://raw.githubusercontent.com/systemd/systemd/main/man/systemd.service.xml), `Type=notify`). A launchd.plist man-oldalon nincs dokumentált megfelelő "jelezd, hogy kész vagy" mechanizmus a folyamat felől launchd felé (a `TimeOut` kulcs csak egy időtúllépési javaslatot ad át a jobnak, nem egy készenlét-visszajelzés).

**Amit a launchd man-oldala dokumentál, és nem esik egybe semmilyen systemd-fogalommal (nem feltétlenül hiányzik systemd-ből, csak máshogy van megoldva):**

- Session-típushoz kötött betöltés: `LimitLoadToSessionType` — a macOS Aqua GUI-munkamenet fogalmához kötött, aminek nincs 1:1 megfelelője a systemd unit-modelljében.
- `WatchPaths`/`QueueDirectories` közvetlenül a plist-ben, mint natív kulcsok — systemd-ben ugyanez külön `.path` egységtípuson keresztül van megoldva, tehát nem hiányzik a képességből, csak máshol van a konfiguráció (ez tehát nem tekinthető systemd-hiányosságnak).

Ez utóbbi pont miatt fontos hangsúlyozni: sok "launchd tud X-et, amit systemd nem" jellegű állítás valójában csak eltérő konfigurációs helyre vonatkozik (pl. path-alapú aktiválás), nem tényleges képességhiányra — ezeket itt nem sorolom fel hiányosságként.

---

## 4. Index-újraépítés induláskor — idő és gyakorlat valós rendszerekben

### 4.1 Elasticsearch

A hivatalos Elastic-dokumentáció kifejezetten leírja, hogy sárga/piros (azaz nem teljesen kész/helyreállt) klaszterállapotban a rendszer **tovább szolgál ki kéréseket**:

> "A red or yellow cluster health status indicates one or more shards are not assigned to a node. Red health status: The cluster has some unassigned primary shards, which means that some operations such as searches and indexing may fail. Yellow health status: The cluster has no unassigned primary shards but some unassigned replica shards. […] When your cluster has a red or yellow health status, it will continue to process searches and indexing where possible, but may delay certain management and cleanup activities until the cluster returns to green health status."
> — [elastic.co — Red or yellow cluster health status](https://www.elastic.co/guide/en/elasticsearch/reference/current/red-yellow-cluster-status.html)

Egy kapcsolódó, hivatalosan dokumentált **szám** is van, bár ez nem index-újraépítési sebesség, hanem az újraelosztás késleltetése node-kiesés után:

> "To avoid wasting resources on temporary issues, Elasticsearch delays allocation by one minute by default."
> — [elastic.co — Red or yellow cluster health status](https://www.elastic.co/guide/en/elasticsearch/reference/current/red-yellow-cluster-status.html)

### 4.2 OpenSearch

Az OpenSearch hivatalos Recovery API-dokumentációja egy explicit, névvel ellátott állapotgépet ír le a shard-helyreállításra induláskor/node-csatlakozáskor:

> "STAGE String The recovery stage. Returned values can include: - INIT: Recovery has not started. - INDEX: Reading index metadata and copying bytes from the source to the destination. - VERIFY_INDEX: Verifying the integrity of the index. - TRANSLOG: Replaying the transaction log. - FINALIZE: Cleanup. - DONE: Complete."
> — [docs.opensearch.org — Recovery (Index APIs)](https://docs.opensearch.org/latest/api-reference/index-apis/recover/)

> "type String The recovery source for the shard. Returned values include: - EMPTY_STORE: An empty store… - EXISTING_STORE: The store of an existing primary shard. Indicates that the recovery is related to node startup or the allocation of an existing primary shard. […] - SNAPSHOT: A snapshot. Indicates that the recovery is related to a snapshot restore operation."
> — [docs.opensearch.org — Recovery (Index APIs)](https://docs.opensearch.org/latest/api-reference/index-apis/recover/)

Ez tehát egy explicit, hivatalosan dokumentált mintája annak, hogy egy elosztott keresőrendszer indulás/helyreállítás közben nevesített, kívülről lekérdezhető köztes állapotokon megy át — de itt sincs sebességszám (sor/mp, MB/mp) dokumentálva, csak `total_time_in_millis`, ami egy adott futás mért ideje, nem publikált elvárt/tervezési szám.

### 4.3 Meilisearch

A Meilisearch hivatalos dokumentációja explicit, névvel ellátott feladat-állapotokat definiál, és kimondja, hogy a keresés nem blokkolódik az indexelési munkák miatt:

> "Processing operations asynchronously allows Meilisearch to handle resource-intensive tasks without impacting search performance."
> — [meilisearch.com/docs — Tasks and asynchronous operations](https://www.meilisearch.com/docs/learn/async/asynchronous_operations)

> "enqueued: the task has been received and will be processed soon. processing: the task is being processed. succeeded: the task has been successfully processed. failed: a failure occurred when processing the task. No changes were made to the database. canceled: the task was canceled."
> — [meilisearch.com/docs — Tasks and asynchronous operations](https://www.meilisearch.com/docs/learn/async/asynchronous_operations)

Publikált sebességszám itt sincs.

### 4.4 Typesense

A hivatalos `/health` végpont dokumentációja **nem** ismer külön "importálás/újraépítés alatt" állapotot — csak alap ok/hiba jelzést:

> "Get health information about a Typesense node. […] When a node is running out of memory / disk, the API response will have an additional resource_error field that's set to either OUT_OF_DISK or OUT_OF_MEMORY."
> — [typesense.org/docs/30.2/api](https://typesense.org/docs/30.2/api/), Health szakasz

Ezt megerősíti egy, a Typesense saját GitHub-problémakövetőjén nyitott hibajegy (ez **nem** hivatalos dokumentáció, csak a projekt saját repója — T2/T3 jellegű, közösségi jelentés), amely szerint a `/health` túl korán "ok"-ot jelez, mielőtt a belső adatbetöltés befejeződne:

> "Typesense appears to respond {ok:true} too early, before changing its mind and actually loading the data."
> — [github.com/typesense/typesense, Issue #665](https://github.com/typesense/typesense/issues/665) (bejelentői megfogalmazás, nem hivatalos Typesense-válasz)

### 4.5 SQLite FTS5 `rebuild` parancs

A hivatalos FTS5-dokumentáció szerint a `rebuild` parancs teljes törlést és újraépítést végez, de **semmilyen költség-, idő- vagy sebességbecslést nem közöl**:

> "This command first deletes the entire full-text index, then rebuilds it based on the contents of the table or content table. It is not available with contentless tables."
> — [sqlite.org/fts5.html](https://sqlite.org/fts5.html), 6.12. The 'rebuild' Command

> "In this, and any other situation where the FTS index and its content table have become inconsistent, the 'rebuild' command may be used to completely discard the contents of the FTS index and rebuild it based on the current contents of the content table."
> — [sqlite.org/fts5.html](https://sqlite.org/fts5.html), 4.4.4 környéke

### 4.6 Van-e bárhol publikált szám (sor/mp, MB/mp)?

**Nem.** Egyik átvizsgált hivatalos dokumentációban sem található publikált átviteli sebesség vagy elfogadható időkeret index-újraépítésre — sem a SQLite FTS5, sem Elasticsearch, sem OpenSearch, sem Meilisearch, sem Typesense hivatalos dokumentációjában. Ezt itt explicit ki kell mondani, mert e nélkül a hiány könnyen összetéveszthető azzal, mintha nem kerestem volna meg.

---

## 5. Lusta (lazy) vs mohó (eager) újraépítés — degradált üzemmód mintája

Nincs egyetlen olyan hivatalos dokumentum sem, amely a "lazy vs eager index rebuild" kifejezést vagy pontosan ezt a tervezési mintát névvel megnevezve tárgyalná. A legközelebbi, **hivatalos** (nem blog) leírás a degradált kiszolgálásra az Elasticsearch klaszter-állapot dokumentációja (l. 4.1):

> "When your cluster has a red or yellow health status, it will continue to process searches and indexing where possible, but may delay certain management and cleanup activities until the cluster returns to green health status."
> — [elastic.co — Red or yellow cluster health status](https://www.elastic.co/guide/en/elasticsearch/reference/current/red-yellow-cluster-status.html)

Ehhez kapcsolódó, szintén hivatalos mintázat a systemd `Type=notify` readiness-protokollja (l. 3. szakasz vége) — ez formálisan lehetővé teszi, hogy egy szolgáltatás a folyamat elindulása után még ne jelentse magát késznek (`READY=1`) amíg pl. egy index felépül, és eközben systemd nem indítja el a rá váró (`After=`) egységeket:

> "systemd will proceed with starting follow-up units after this notification message has been sent."
> — [systemd.service.xml](https://raw.githubusercontent.com/systemd/systemd/main/man/systemd.service.xml), `Type=notify`

Ez azonban egy **indításvezérlési** mechanizmus (mikor tekintse systemd "elindultnak" az egységet), nem magának az alkalmazásnak egy dokumentált "degraded mode, amíg az index épül" mintája. Ilyen, kifejezetten "degraded mode" címkével ellátott hivatalos leírást egyik vizsgált rendszernél sem találtam — az Elasticsearch a legközelebbi, de ott is a "piros/sárga állapot melletti folyamatos kiszolgálás" a dokumentált tény, nem egy általános, elnevezett tervezési minta.

---

## 6. Tiszta leállás

### 6.1 SQLite oldali helyes sorrend

A hivatalos C-API dokumentáció szerint az ajánlott sorrend: minden prepared statement finalize-olása, minden BLOB-handle lezárása, minden backup befejezése, **utána** `sqlite3_close()`/`sqlite3_close_v2()`:

> "Ideally, applications should finalize all prepared statements, close all BLOB handles, and finish all sqlite3_backup objects associated with the sqlite3 object prior to attempting to close the object. If the database connection is associated with unfinalized prepared statements, BLOB handlers, and/or unfinished sqlite3_backup objects then sqlite3_close() will leave the database connection open and return SQLITE_BUSY. If sqlite3_close_v2() is called with unfinalized prepared statements, unclosed BLOB handlers, and/or unfinished sqlite3_backups, it returns SQLITE_OK regardless, but instead of deallocating the database connection immediately, it marks the database connection as an unusable 'zombie' and makes arrangements to automatically deallocate the database connection after all prepared statements are finalized, all BLOB handles are closed, and all backups have finished."
> — [sqlite.org/c3ref/close.html](https://sqlite.org/c3ref/close.html)

> "If an sqlite3 object is destroyed while a transaction is open, the transaction is automatically rolled back."
> — [sqlite.org/c3ref/close.html](https://sqlite.org/c3ref/close.html)

Explicit checkpoint-hívás **nem kötelező** az alkalmazás részéről — a WAL-dokumentáció szerint az utolsó kapcsolat lezárásakor a könyvtár automatikusan elvégzi ezt:

> "By default, SQLite will automatically checkpoint whenever a COMMIT occurs that causes the WAL file to be 1000 pages or more in size, or when the last database connection on a database file closes. The default configuration is intended to work well for most applications."
> — [sqlite.org/wal.html](https://sqlite.org/wal.html), 3.1. Automatic Checkpoint

> "When the last connection to a database closes, that connection does one last checkpoint and then deletes the WAL and its associated shared-memory file, to clean up the disk."
> — [sqlite.org/wal.html](https://sqlite.org/wal.html), 6. szakasz

Vagyis a helyes sorrend a hivatalos dokumentáció szerint: (1) minden nyitott statement/BLOB/backup lezárása, (2) `sqlite3_close()` (vagy `_close_v2()`) meghívása minden kapcsolaton — a checkpointot és a `-wal`/`-shm` takarítást ez automatikusan kiváltja, application-oldali explicit `wal_checkpoint` hívás csak akkor szükséges, ha az automatikus checkpoint le van tiltva vagy application-specifikus okból korábban akarjuk lefuttatni.

### 6.2 systemd `TimeoutStopSec=` alapértéke és lejárat esetén történő esemény

> "This option serves two purposes. First, it configures the time to wait for each ExecStop= command. If any of them times out, subsequent ExecStop= commands are skipped and the service will be terminated by SIGTERM. If no ExecStop= commands are specified, the service gets the SIGTERM immediately. […] Second, it configures the time to wait for the service itself to stop. If it does not terminate in the specified time, it will be forcibly terminated by SIGKILL (see KillMode= in systemd.kill(5)). Takes a unit-less value in seconds… Defaults to DefaultTimeoutStopSec= from the manager configuration file."
> — [systemd.service.xml](https://raw.githubusercontent.com/systemd/systemd/main/man/systemd.service.xml), `TimeoutStopSec=`

A tényleges alapszámot a build-rendszer (meson) alapértelmezése rögzíti, amit a `systemd-system.conf` man-oldal is megerősít szövegesen:

> "option('default-timeout-sec', type : 'integer', value : 90, description : 'default timeout for system unit start/stop')"
> — [systemd forráskód, meson_options.txt](https://raw.githubusercontent.com/systemd/systemd/main/meson_options.txt)

> "DefaultTimeoutStartSec= and DefaultTimeoutStopSec= default to &DEFAULT_TIMEOUT_SEC; in the system manager…"
> — [systemd-system.conf.xml](https://raw.githubusercontent.com/systemd/systemd/main/man/systemd-system.conf.xml) (a `&DEFAULT_TIMEOUT_SEC;` entitás a fenti meson-alapértékből, azaz **90s**, épül be a végleges man-oldalba)

**Tehát: `TimeoutStopSec=` build-alapértelmezése 90 másodperc**, és lejáratkor a folyamat `SIGKILL`-t kap (a `KillMode=` beállítástól függő pontos hatókörrel — l. `systemd.kill(5)`, amit ez a kutatás nem töltött le külön).

---

## Amire NINCS publikált válasz

1. **Nincs hivatalosan publikált sebességszám** (sor/másodperc vagy MB/másodperc) semelyik vizsgált index-újraépítési mechanizmusra: sem a SQLite FTS5 `rebuild` parancsra, sem Elasticsearch/OpenSearch shard-recovery-re, sem Meilisearch task-feldolgozásra, sem Typesense-re. Ezt kifejezetten kimondom, nem hallgatom el.
2. **Nincs név szerint megcímzett hivatalos szakasz** arra a pontos forgatókönyvre, hogy "`-wal` megvan, `-shm` hiányzik" — csak a wal-index általános tranziens/újraépíthető jellegének leírásából (fileformat2.html) lehet erre következtetni, nem egy erre a konkrét esetre írt mondatból.
3. **Nincs külön, "korrupt WAL fájl" címkéjű hivatalos fejezet** — csak a checksum-lánc formátumleírásából következtethető ki, mi történik sérült/csonka keretek esetén.
4. **Nincs hivatalos, egységes "systemd vs launchd" összehasonlító dokumentum** — a 3. szakasz saját összevetésem a két projekt külön-külön dokumentációja alapján, nem egy harmadik fél állítása.
5. **Nincs a launchd man-oldalán explicit kimondva, hogy "nincs StartLimitBurst-szerű mechanizmusunk"** — ezt a man-oldal teljes kulcslistájának átvizsgálásával, hiány alapján állapítottam meg, nem egy Apple-nyilatkozatból.
6. **A launchd.plist man-oldalt ebben a munkamenetben nem sikerült közvetlenül Apple-forrásból (developer.apple.com / opensource.apple.com) letölteni** — csak egy megbízható, de harmadik fél általi tükrözésből (manpagez.com, 2009-es dátumozású, Mac OS X 10.9-hez generált). Ez a tartalom közismerten (saját tudásból, nem ebből a kutatásból) lényegében változatlanul szerepel a jelenlegi macOS-ek `man launchd.plist` kimenetében is, de ezt ebben a kutatásban nem tudtam frissen, hivatalos Apple-forrásból megerősíteni.
7. **Nincs egyetlen hivatalos dokumentum sem, amely a "lazy vs eager index rebuild" tervezési mintát ezen a néven tárgyalná** — az 5. szakaszban bemutatott Elasticsearch- és systemd-minták csak analóg, nem azonos nevű jelenségek.
8. **A `www.freedesktop.org/software/systemd/man/latest/...` hivatalos oldalakat bot-elhárítási kihívás védte** ("Checking you are not a bot" meta-refresh), ezért ezeket nem sikerült közvetlenül lekérni; helyettük a systemd upstream GitHub-forrást (a man-oldalak tényleges forrása) és a Debian testing man-oldal-tükrözését használtam, amelyek tartalmilag megegyeznek.

---



---

# SQ05 — Mikor beteg egy SQLite adatbázis, és hogyan vesszük észre?

Ez az összefoglaló egygépes, egyfolyamatos, WAL-módú SQLite-használatra (az „easter-memory-system” mintájára: eldobható FTS5-index, drágán újraépíthető embedding-cache, pótolhatatlan adatfájl) vonatkozó hivatalos sqlite.org dokumentációt és forráskódot gyűjti össze. A hivatalos „How To Corrupt An SQLite Database File” oldal okainak túlnyomó többsége több gépet, több eltérő zárolási protokollt, hálózati fájlrendszert vagy hardveres/oprendszeri hibát tételez fel; egygépes, egyfolyamatos WAL-használatra ezekből lényegében a `fsync`-hazugság (lemez/vezérlő hazudik a szinkronról), a fájlrendszer-hiba, a memóriasérülés az alkalmazásban, valamint a „meleg” napló (`-wal`/`-journal`) fájl leválasztása/másolása futás közben marad releváns. A `PRAGMA integrity_check`, `quick_check` és `foreign_key_check` három, jól elhatárolt, hivatalosan dokumentált ellenőrzést végez — nincs azonban hivatalos ajánlás arra, milyen gyakran fussanak. A WAL napló alapértelmezett automatikus checkpoint-küszöbe dokumentáltan 1000 oldal, és a dokumentáció név szerint ismeri és leírja a „checkpoint starvation” jelenséget, amikor egy tartósan nyitva hagyott olvasó tranzakció miatt a WAL korlátlanul nőhet. A `busy_timeout` alapértelmezett viselkedése hivatalosan az, hogy nincs busy-handler (NULL), így zárolás esetén a hívás azonnal `SQLITE_BUSY`-val tér vissza; a hivatalos dokumentáció emellett kifejezetten leírja azt a holtpont-esetet, amikor a timeout hiába van beállítva, mert a válasz kikényszerítése maga okozna holtpontot. A `SQLITE_BUSY_SNAPSHOT` kifejezetten WAL-módra jellemző hibakód, amikor egy olvasási tranzakciót író tranzakcióvá akarnak léptetni, de közben más kapcsolat már írt az adatbázisba. Nincs olyan hivatalos sqlite.org-i ajánlás, amely rendszeres, ütemezett integritás-ellenőrzést írna elő; a gyakorlatban vizsgált harmadik fél projektek (Litestream, Fossil, Home Assistant) mindegyike a saját eszközkészletében old meg valamilyen integritás-ellenőrzést, de eltérő mélységben és eltérő időzítéssel. A `PRAGMA optimize` hivatalos ajánlása kifejezetten kimondja, hogy rövid életű kapcsolatok esetén a kapcsolat lezárása előtt közvetlenül kell lefuttatni.

## 1. Sérülés okai — sqlite.org/howtocorrupt.html

Forrás minden idézethez: https://www.sqlite.org/howtocorrupt.html

A teljes ok-lista nyolc fő fejezetre oszlik: (1) Fájl felülírása egy „rossz” szál/folyamat által, (2) Fájlzárolási problémák, (3) Sync-hiba, (4) Lemez-/flash-meghibásodás, (5) Memóriasérülés, (6) Egyéb operációsrendszer-problémák, (7) SQLite konfigurációs hibák, (8) SQLite-hibák (történeti lista). Alább a teljes lista, kiemelve, mi az, ami **egygépes, egyfolyamatos, WAL-módú** használatnál egyáltalán relevánsan előfordulhat.

### 1.1 Teljes okcsoport-lista (rövid felsorolás, minden alpont a hivatalos oldalról)

1. Fájl felülírása rossz szál/folyamat által
   1.1 Lezárt fájlleíró további használata
   1.2 Biztonsági mentés/visszaállítás tranzakció közben
   1.3 „Meleg” napló törlése
   1.4 Adatbázisfájl és meleg napló összekeverése
2. Fájlzárolási problémák
   2.1 Hibás/hiányos zárolás-implementációjú fájlrendszerek (NFS)
   2.2 POSIX advisory lock törlődik más szál `close()`-jától
   2.3 Több SQLite-példány linkelve ugyanabba az alkalmazásba
   2.4 Két folyamat eltérő zárolási protokollal
   2.5 Adatbázisfájl unlink/rename közben használatban
   2.6 Több link ugyanarra a fájlra
   2.7 Nyitott adatbázis-kapcsolat átvitele `fork()`-on át
3. Sync-hiba (fsync nem működik)
   3.1 Lemezmeghajtók, amelyek nem tartják be a sync-kéréseket
   3.2 Sync letiltása PRAGMA-val
4. Lemez- és flash-memória-hibák
   4.1 Nem power-safe flash vezérlők
   4.2 Hamis kapacitású USB-eszközök
5. Memóriasérülés (az alkalmazás oldalán)
6. Egyéb operációsrendszer-problémák
   6.1 Linux Threads
   6.2 `mmap()` hibák QNX-en
   6.3 Fájlrendszer-sérülés
7. SQLite konfigurációs hibák (pl. `synchronous=OFF`, `journal_mode=OFF/MEMORY` + összeomlás, `writable_schema=ON`)
8. Történeti SQLite-hibák (2009–2022 közötti, azóta javított hibák, pl. WAL race condition, boundary-hiba a nested tranzakciók naplóiban)

### 1.2 Egygépes, egyfolyamatos, WAL-módú használatra ténylegesen releváns okok — szó szerinti idézetek

**a) Fájlrendszer-hiba / meghibásodás (4. és 6.3 pont)**

> "An SQLite database can become corrupt if the file content changes due to a disk drive or flash memory failure. It is very rare, but disks will occasionally flip a bit in the middle of a sector."

> "Since SQLite databases are ordinary disk files, any malfunction in the filesystem can corrupt the database. Filesystems in modern operating systems are very reliable, but errors do still occur. For example, on 2013-10-01 the SQLite database that holds the Wiki for Tcl/Tk went corrupt a few days after the host computer was moved to a dodgy build of the (linux) kernel that had issues in the filesystem layer."

**b) `fsync` hazudik / a lemez nem tartja be a sync-kérést (egygépes, egyfolyamatos esetben is releváns, mert nem folyamatszámtól, hanem a hardvertől függ)**

> "Unfortunately, most consumer-grade mass storage devices lie about syncing. Disk drives will report that content is safely on persistent media as soon as it reaches the track buffer and before actually being written to oxide. […] But if a power loss or hard reset does occur, and if that results in content that was written after a sync reaching oxide while content written before the sync is still in a track buffer, then database corruption can occur."

A dokumentáció kifejezetten kiemeli, hogy **WAL módban ez a hiba korlátozottabb hatású**, mint rollback-journal módban:

> "However, SQLite in WAL mode is far more forgiving of out-of-order writes than in the default rollback journal modes. In WAL mode, the only time that a failed sync operation can cause database corruption is during a checkpoint operation. A sync failure during a COMMIT might result in loss of durability but not in a corrupt database file. Hence, one line of defense against database corruption due to failed sync operations is to use SQLite in WAL mode and to checkpoint as infrequently as possible."

**c) `PRAGMA synchronous=OFF` (konfigurációs hiba, egyfolyamatos rendszeren is előfordulhat, ha valaki tudatosan kikapcsolja)**

> "By setting PRAGMA synchronous=OFF, all sync operations are omitted. This makes SQLite seem to run faster, but it also allows the operating system to freely reorder writes, which could result in database corruption if a power failure or hard reset occurs prior to all content reaching persistent storage. For maximum reliability and for robustness against database corruption, SQLite should always be run with its default synchronous setting of FULL."

**d) „Meleg” napló (hot journal / `-wal` fájl) törlése vagy leválasztása összeomlás után**

> "SQLite must see the journal files in order to recover from a crash or power failure. If the hot journal files are moved, deleted, or renamed after a crash or power failure, then automatic recovery will not work and the database may go corrupt."

**e) Biztonsági mentés / fájlmásolás futó tranzakció közben (ez egygépes, egyfolyamatos rendszeren is előfordulhat, ha egy külső backup-szkript másolja a fájlt)**

> "Systems that run automatic backups in the background might try to make a backup copy of an SQLite database file while it is in the middle of a transaction. The backup copy then might contain some old and some new content, and thus be corrupt."

> "It is also safe to make a copy of an SQLite database file as long as there are no transactions in progress while the copy is taking place. If the previous write transaction failed, then it is important that any rollback journal (the *-journal file) or write-ahead log (the *-wal file) be copied together with the database file itself."

A biztonságos másolási módszerek, amiket a dokumentáció hivatalosan ajánl: `sqlite3_rsync`, `VACUUM INTO filename`, illetve a C-szintű backup API.

**f) Memóriasérülés az alkalmazásban (egyfolyamatos rendszeren is a leggyakoribb valódi kockázat, főleg `mmap` I/O mellett)**

> "SQLite is a C-library that runs in the same address space as the application that it serves. That means that stray pointers, buffer overruns, heap corruption, or other malfunctions in the application can corrupt internal SQLite data structure and ultimately result in a corrupt database file. […] The memory corruption problem becomes more acute when using memory-mapped I/O. When all or part of the database file is mapped into the application's address space, then a stray pointer that overwrites any part of that mapped space will immediately corrupt the database file, without requiring the application to do a subsequent write() system call."

**g) Nyitott kapcsolat átvitele `fork()`-on keresztül (releváns, ha az egyfolyamatos rendszer valaha elágaztat gyermekfolyamatot)**

> "Do not open an SQLite database connection, then fork(), then try to use that database connection in the child process. All kinds of locking problems will result and you can easily end up with a corrupt database."

### 1.3 Ami TÖBBGÉPES / TÖBBFOLYAMATOS forgatókönyvhöz kötött (egygépes/egyfolyamatos esetben NEM releváns, de a kérdés kifejezetten kérte a hálózati fájlrendszeres részt)

**Hálózati fájlrendszerek (NFS) — sqlite.org/howtocorrupt.html:**

> "SQLite depends on the underlying filesystem to do locking as the documentation says it will. But some filesystems contain bugs in their locking logic such that the locks do not always behave as advertised. This is especially true of network filesystems and NFS in particular. If SQLite is used on a filesystem where the locking primitives contain bugs, and if two or more threads or processes try to access the same database at the same time, then database corruption might result."

**Kiegészítő hivatalos oldal a témában — https://www.sqlite.org/useovernet.html ("Hints On Using SQLite On A Network Filesystem"):**

> "This simple, 'remote database' approach is usually not the best way to use a single SQLite database from multiple systems, (even if it appears to 'work'), as it often leads to various kinds of trouble and grief."

> "A similar hazard arises with file locking in network filesystems. SQLite relies on exclusive locks for write operations, and those have been known to operate incorrectly for some network filesystems. This has led to database corruption."

> "The bottom line is that network filesystem sync and locking reliability vary among implementations and installations. The design assumptions upon which it relies may hold more true where an application is tested than where it is relied upon. **Rely upon it at your (and your customers') peril.**"

Ez az oldal a záró ajánlásában kifejezetten client/server adatbázist (pl. PostgreSQL) javasol, ha az adat és az alkalmazás nem ugyanazon a gépen van:

> "Generally, if your data is separated from the application by a network, you want to use a client/server database."

**SMB, illetve felhő-szinkronizáló mappák (Dropbox, iCloud, OneDrive):** sem a `howtocorrupt.html`, sem a `useovernet.html` oldal **nem említi név szerint** az SMB-t, a Dropboxot, az iCloudot vagy a OneDrive-ot. Az `useovernet.html` oldal kifejezetten csak „network filesystem” általánosságban beszél, konkrét márkanevek nélkül. (Lásd az „Amire nincs publikált válasz” szakaszt.)

## 2. `integrity_check` vs `quick_check` vs `foreign_key_check` — sqlite.org/pragma.html

**`PRAGMA integrity_check`** (https://www.sqlite.org/pragma.html#pragma_integrity_check):

> "This pragma does a low-level formatting and consistency check of the database. The integrity_check pragma look for:
> - Table or index entries that are out of sequence
> - Misformatted records
> - Missing pages
> - Missing or surplus index entries
> - UNIQUE, CHECK, and NOT NULL constraint errors
> - Integrity of the freelist
> - Sections of the database that are used more than once, or not at all"

> "If the integrity_check pragma finds problems, strings are returned (as multiple rows with a single column per row) which describe the problems. Pragma integrity_check will return at most N errors before the analysis quits, with N defaulting to 100. If pragma integrity_check finds no errors, a single row with the value 'ok' is returned."

Részleges (tábla szintű) ellenőrzés is lehetséges, de korlátozottan:

> "The usual case is that the entire database file is checked. However, if the argument is TABLENAME, then checking is only performed for the the table named and its associated indexes. This is called a 'partial integrity check'. Because only a subset of the database is checked, errors such as unused sections of the file or duplication use of the same section of the file by two or more tables cannot be detected."

Amit KIFEJEZETTEN NEM ellenőriz:

> "PRAGMA integrity_check does not find FOREIGN KEY errors. Use the PRAGMA foreign_key_check command to find errors in FOREIGN KEY constraints."

**`PRAGMA quick_check`** (https://www.sqlite.org/pragma.html#pragma_quick_check):

> "The pragma is like integrity_check except that it does not verify UNIQUE constraints and does not verify that index content matches table content. By skipping UNIQUE and index consistency checks, quick_check is able to run faster. PRAGMA quick_check runs in O(N) time whereas PRAGMA integrity_check requires O(NlogN) time where N is the total number of rows in the database. Otherwise the two pragmas are the same."

Tehát a `quick_check` hivatalosan dokumentáltan **kihagyja**: (1) a UNIQUE megszorítások ellenőrzését, (2) annak ellenőrzését, hogy az index tartalma megegyezik-e a tábla tartalmával. Mindent mást (rossz sorrendű bejegyzések, hibás rekordformátum, hiányzó lapok, CHECK/NOT NULL megszorítások, freelist, kettős/felhasználatlan szakaszok) a dokumentáció szerint ugyanúgy ellenőriz, mint az `integrity_check`.

Futásidőről az egyetlen hivatalos, konkrét állítás a fenti O(N) vs O(NlogN) komplexitás-összehasonlítás; **konkrét ajánlott gyakoriságról vagy arról, hogy melyiket kell rutinszerű ellenőrzésre használni, a pragma.html oldal nem tesz kijelentést** (lásd „Amire nincs publikált válasz”).

**`PRAGMA foreign_key_check`** (https://www.sqlite.org/pragma.html#pragma_foreign_key_check):

> "The foreign_key_check pragma checks the database, or the table called 'table-name', for foreign key constraints that are violated. The foreign_key_check pragma returns one row output for each foreign key violation. There are four columns in each result row. The first column is the name of the table that contains the REFERENCES clause. The second column is the rowid of the row that contains the invalid REFERENCES clause, or NULL if the child table is a WITHOUT ROWID table. The third column is the name of the table that is referred to. The fourth column is the index of the specific foreign key constraint that failed."

Ez a pragma kizárólag a deklarált idegenkulcs-megszorítások (REFERENCES-záradékok) sértéseit deríti fel — sem az `integrity_check`, sem a `quick_check` nem terjed ki erre, ahogy azt az `integrity_check` szakasz kifejezetten kimondja.

## 3. WAL növekedés és checkpoint-éhezés — sqlite.org/wal.html

**`wal_autocheckpoint` alapértelmezett értéke** (https://www.sqlite.org/pragma.html#pragma_wal_autocheckpoint):

> "The wal_autocheckpoint setting is the number of pages that have to be written to the WAL file before an automatic checkpoint occurs. The default value for wal_autocheckpoint is 1000. (This means that an automatic checkpoint occurs after every 1000 pages are written to the WAL file.) Setting the wal_autocheckpoint value to zero disables automatic checkpoints entirely."

Ugyanez a wal.html dokumentumban:

> "By default, SQLite does a checkpoint automatically when the WAL file reaches a threshold size of 1000 pages."

**Pontos érték és mértékegység: 1000 (oldal), nem MB vagy más mértékegység.**

**Checkpoint-éhezés („checkpoint starvation”)** — https://www.sqlite.org/wal.html, „Avoiding Excessively Large WAL Files" szakasz:

> "**Checkpoint starvation.** A checkpoint is only able to run to completion, and reset the WAL file, if there are no other database connections using the WAL file. If another connection has a read transaction open, then the checkpoint cannot reset the WAL file because doing so might delete content out from under the reader. The checkpoint will do as much work as it can without upsetting the reader, but it cannot run to completion. The checkpoint will start up again where it left off after the next write transaction. This repeats until some checkpoint is able to complete.
>
> However, if a database has many concurrent overlapping readers and there is always at least one active reader, then no checkpoints will be able to complete and hence the WAL file will grow without bound."

**Nagyon nagy írási tranzakciók hatása a WAL-fájl méretére** (ugyanazon szakasz):

> "A checkpoint can only complete when no other transactions are running, which means the WAL file cannot be reset in the middle of a write transaction. So a large change to a large database might result in a large WAL file. The WAL file will be checkpointed once the write transaction completes (assuming there are no other readers blocking it) but in the meantime, the file can grow very big."

> "As of SQLite version 3.11.0 (2016-02-15), the WAL file for a single transaction should be proportional in size to the transaction itself. Pages that are changed by the transaction should only be written into the WAL file once. However, with older versions of SQLite, the same page might be written into the WAL file multiple times if the transaction grows larger than the page cache."

**Olvasási teljesítmény romlása nagy WAL mellett** (wal.html, 2.3 szakasz):

> "On the other hand, read performance deteriorates as the WAL file grows in size since each reader must check the WAL file for the content and the time needed to check the WAL file is proportional to the size of the WAL file."

**`PRAGMA wal_checkpoint(PASSIVE|FULL|RESTART|TRUNCATE)` — pontos különbségek** (https://www.sqlite.org/pragma.html#pragma_wal_checkpoint):

> "The checkpoint mode can be one of PASSIVE, FULL, RESTART, or TRUNCATE. The default checkpoint mode is PASSIVE."
>
> "**PASSIVE**: This checkpoint mode blocks (waits for) readers, but not writers. A PASSIVE checkpoint will cause all frames in the WAL file to be transferred to the database file via the xFileControl method of the VFS interface. But a PASSIVE checkpoint does not stall transactions or touch the wal-index."
>
> "**FULL**: A FULL checkpoint goes one step further. After transferring all frames from the WAL file to the database, it also reinitializes the WAL file (deletes the file or truncates it to an empty state) and syncs the changes to stable storage. A FULL checkpoint may only run after all readers have finished using the database, however. So a FULL checkpoint might not complete if there are open read transactions. A FULL checkpoint blocks writers as it runs."
>
> "**RESTART**: A RESTART checkpoint works the same as FULL, but also resets the wal-index back to the beginning so that the next reader will see a clear wal-index."
>
> "**TRUNCATE**: This is like RESTART but also truncates the wal file to zero bytes."

Ugyanez a C-szintű interfészen (https://www.sqlite.org/c3ref/wal_checkpoint_v2.html), az `SQLITE_CHECKPOINT_*` konstansokra, még részletesebben a busy-handler viselkedésével együtt:

> "SQLITE_CHECKPOINT_PASSIVE: Checkpoint as many frames as possible without waiting for any database readers or writers to finish, then sync the database file if all frames in the log were checkpointed. The busy-handler callback is never invoked in the SQLITE_CHECKPOINT_PASSIVE mode. On the other hand, passive mode might leave the checkpoint unfinished if there are concurrent readers or writers."

> "SQLITE_CHECKPOINT_FULL: This mode blocks (it invokes the busy-handler callback) until there is no database writer and all readers are reading from the most recent database snapshot. It then checkpoints all frames in the log file and syncs the database file. This mode blocks new database writers while it is pending, but new database readers are allowed to continue unimpeded."

> "SQLITE_CHECKPOINT_RESTART: This mode works the same way as SQLITE_CHECKPOINT_FULL with the addition that after checkpointing the log file it blocks (calls the busy-handler callback) until all readers are reading from the database file only. This ensures that the next writer will restart the log file from the beginning. Like SQLITE_CHECKPOINT_FULL, this mode blocks new database writer attempts while it is pending, but does not impede readers."

> "SQLITE_CHECKPOINT_TRUNCATE: This mode works the same way as SQLITE_CHECKPOINT_RESTART with the addition that it also truncates the log file to zero bytes just prior to a successful return."

**WAL méret és mikor baj ez** — összefoglaló mondat a wal.html 6. szakaszából:

> "So in the vast majority of cases, applications need not worry about the WAL file at all. SQLite will automatically take care of it. But it is possible to get SQLite into a state where the WAL file will grow without bound, causing excess disk space usage and slow query speeds."

A dokumentáció **nem ad meg konkrét GB-ban vagy MB-ban kifejezett felső korlátot** vagy küszöböt, aminél a WAL mérete önmagában „bajnak” minősül — csak azt írja le kvalitatívan, hogy korlátlan (unbounded) növekedés és az ebből fakadó lemezterület-fogyás, illetve olvasási lassulás jelenti a problémát.

## 4. `busy_timeout` és `SQLITE_BUSY`

**`PRAGMA busy_timeout`** (https://www.sqlite.org/pragma.html#pragma_busy_timeout):

> "Query or change the setting of the busy timeout. This pragma is an alternative to the sqlite3_busy_timeout() C-language interface which is made available as a pragma for use with language bindings that do not provide direct access to sqlite3_busy_timeout()."
>
> "Each database connection can only have a single busy handler. This PRAGMA sets the busy handler for the process, possibly overwriting any previously set busy handler."

Ez a hivatalos PRAGMA-oldal **nem ad meg konkrét számot** az alapértelmezett várakozási időre.

**Alapértelmezett busy-handler viselkedés — a C-API hivatalos dokumentációjából** (https://www.sqlite.org/c3ref/busy_handler.html, „Register A Callback To Handle SQLITE_BUSY Errors"):

> "The default busy callback is NULL."

> "If the busy callback is NULL, then SQLITE_BUSY is returned immediately upon encountering the lock."

Tehát a hivatalosan dokumentált alapállapot az, hogy **nincs busy-handler**, és emiatt egy zárolásba ütköző hívás **azonnal** `SQLITE_BUSY` hibával tér vissza — ez funkcionálisan egyenértékű egy 0 ezredmásodperces timeout-tal, de a dokumentáció ezt sehol nem fejezi ki puszta „0” számként; ehelyett a „NULL callback → azonnali SQLITE_BUSY” viselkedést írja le.

**Mikor NEM segít a `busy_timeout` — a hivatalos holtpont-eset** (ugyanaz az oldal, https://www.sqlite.org/c3ref/busy_handler.html):

> "The presence of a busy handler does not guarantee that it will be invoked when there is lock contention. If SQLite determines that invoking the busy handler could result in a deadlock, it will go ahead and return SQLITE_BUSY to the application instead of invoking the busy handler. Consider a scenario where one process is holding a read lock that it is trying to promote to a reserved lock and a second process is holding a reserved lock that it is trying to promote to an exclusive lock. The first process cannot proceed because it is blocked by the second and the second process cannot proceed because it is blocked by the first. If both processes invoke the busy handlers, neither will make any progress. Therefore, SQLite returns SQLITE_BUSY for the first process, hoping that this will induce the first process to release its read lock and allow the second process to proceed."

Ez a hivatalos szöveg egyértelműen kimondja: ilyen kölcsönös zárolási helyzetben (két kapcsolat egymást várná) a `busy_timeout`/busy-handler **nem kerül meghívásra**, SQLite azonnal `SQLITE_BUSY`-t ad vissza, mert a várakozás maga okozná a holtpontot.

**Az `SQLITE_BUSY` általános definíciója és a `SQLITE_LOCKED`-től való elhatárolás** (https://www.sqlite.org/rescode.html):

> "The SQLITE_BUSY result code indicates that the database file could not be written (or in some cases read) because of concurrent activity by some other database connection, usually a database connection in a separate process."

> "An SQLITE_BUSY error can occur at any point in a transaction: when the transaction is first started, during any write or update operations, or when the transaction commits. To avoid encountering SQLITE_BUSY errors in the middle of a transaction, the application can use BEGIN IMMEDIATE instead of just BEGIN to start a transaction. The BEGIN IMMEDIATE command might itself return SQLITE_BUSY, but if it succeeds, then SQLite guarantees that no subsequent operations on the same database through the next COMMIT will return SQLITE_BUSY."

> "The SQLITE_BUSY result code differs from SQLITE_LOCKED in that SQLITE_BUSY indicates a conflict with a separate database connection, probably in a separate process, whereas SQLITE_LOCKED indicates a conflict within the same database connection (or sometimes a database connection with a shared cache)."

**`SQLITE_BUSY_SNAPSHOT`** (https://www.sqlite.org/rescode.html):

> "The SQLITE_BUSY_SNAPSHOT error code is an extended error code for SQLITE_BUSY that occurs on WAL mode databases when a database connection tries to promote a read transaction into a write transaction but finds that another database connection has already written to the database and thus invalidated prior reads."
>
> "The following scenario illustrates how an SQLITE_BUSY_SNAPSHOT error might arise:
> 1. Process A starts a read transaction on the database and does one or more SELECT statements. Process A keeps the transaction open.
> 2. Process B updates the database, changing values previous read by process A.
> 3. Process A now tries to write to the database. But process A's view of the database content is now obsolete because process B has modified the database file after process A read from it. Hence process A gets an SQLITE_BUSY_SNAPSHOT error."

A dokumentáció külön kiemeli, hogy ez a kód **kifejezetten WAL-módú adatbázisokra jellemző** ("occurs on WAL mode databases"). Rokon kód: `SQLITE_BUSY_RECOVERY`:

> "The SQLITE_BUSY_RECOVERY error code is an extended error code for SQLITE_BUSY that indicates that an operation could not continue because another process is busy recovering a WAL mode database file following a crash. The SQLITE_BUSY_RECOVERY error code only occurs on WAL mode databases."

## 5. Mit érdemes rendszeresen megnézni — hivatalos ajánlás és gyakorlati példák

**Hivatalos sqlite.org ajánlás rendszeres integritás-ellenőrzésre: NINCS.** Sem a `pragma.html`, sem a `wal.html`, sem a `howtocorrupt.html` oldal nem tartalmaz olyan mondatot, amely előírná vagy javasolná az `integrity_check`/`quick_check` időszakos (pl. napi/heti) lefuttatását éles rendszeren. A `pragma.html` az `integrity_check` és `quick_check` leírásánál kizárólag azt mondja ki, hogy a `quick_check` gyorsabb (lásd 2. szakasz), de nem ajánl konkrét ütemezést vagy gyakoriságot. Ezt kifejezetten dokumentáljuk hiányként (lásd „Amire nincs publikált válasz”).

**Litestream** (https://litestream.io/) — nincs beépített, automatikus integritás-ellenőrzés a replikáció folyamatában; a hivatalos dokumentáció manuális lépésként ajánlja a `PRAGMA integrity_check` futtatását helyreállítás UTÁN:

Tips oldal (https://litestream.io/tips/):

> "Once you have a restored copy, it's a good idea to perform an integrity check on the database using `sqlite3`"

(a hozzá tartozó példa: `sqlite3 /path/to/db` → `PRAGMA integrity_check;` → `ok`)

Troubleshooting oldal (https://litestream.io/docs/troubleshooting/), „Corruption Detection" szakasz — a leírt lépéssor: replikáció leállítása → `sqlite3 /path/to/db.sqlite "PRAGMA integrity_check;"` futtatása → sérülés esetén visszaállítás a legutóbbi mentésből (`litestream restore -o ...`). Ugyanez a lap külön szakaszban („WAL Growth and Checkpoint Blocking") kezeli a hosszú élettartamú olvasási tranzakciók által okozott checkpoint-blokkolást is, összhangban a wal.html „checkpoint starvation" leírásával.

**Fossil SCM** — a `test-integrity` parancs hivatalos súgója (https://sqlite.org/mgmt/help?cmd=test-integrity — ez maga a sqlite.org saját, Fossillal futtatott repója, tehát elsődleges forrásnak tekinthető a Fossil-parancsra nézve):

> "Verify that all content can be extracted from the BLOB table correctly. If the BLOB table is correct, then the repository can always be successfully reconstructed using 'fossil rebuild'."

Kapcsolók:

> "-d|--db-only: Run 'PRAGMA integrity_check' on the database only. No other validation is performed."

> "--quick: Run 'PRAGMA quick_check' on the database only. No other validation is performed."

Tehát a Fossil kifejezetten és nyíltan a hivatalos SQLite `integrity_check`/`quick_check` pragmákra épít, alapértelmezésben viszont saját, tartalom-szintű (BLOB-kinyerési) ellenőrzést végez, és a puszta SQLite-szintű ellenőrzés csak kapcsolóval kérhető.

**Home Assistant** — az `home-assistant/core` hivatalos repó #37949 számú PR-je („Automatically recover when the sqlite3 database is malformed or corrupted”, https://github.com/home-assistant/core/pull/37949) egy `validate_sqlite_database()` nevű függvényt vezetett be, amely a recorder-komponens indulásakor fut le SQLite-adatbázis esetén, és a `PRAGMA QUICK_CHECK` paranccsal ellenőrzi az adatbázist; sérülés észlelése esetén a hibás fájlt (a hozzá tartozó `-wal`/`-shm` fájlokkal együtt) átnevezi `*.corrupt.{ISOTIME}` végződéssel, és a rendszer egy friss adatbázissal indul tovább. **Megjegyzés a forrás aktualitásához:** a jelen kutatás során a `dev` ág aktuális `homeassistant/components/recorder/util.py` fájljában egy `validate_sqlite_database()`/`basic_sanity_check()` nevű, SELECT-alapú (nem explicit `PRAGMA quick_check`-et hívó) ellenőrzést találtunk; nem sikerült megnyugtatóan tisztázni, hogy ez a 2020-as PR-ben bevezetett `PRAGMA QUICK_CHECK`-alapú logika időközbeni átalakítása-e, vagy egy másik, kiegészítő ellenőrzési réteg. Ezt bizonytalanságként jelöljük (lásd „Amire nincs publikált válasz”).

**Datasette** — nincs beépített, natív SQLite-integritásellenőrzés. Létezik egy harmadik fél (Simon Willison) által készített `datasette-verify` bővítmény (https://pypi.org/project/datasette-verify/), de ez kifejezetten **nem** a `PRAGMA integrity_check`-et futtatja, hanem csak azt teszteli, hogy a fájl egyáltalán megnyitható-e Datasette-tel:

> "Verify that SQLite files can be opened using Datasette"

## 6. `PRAGMA optimize` és `ANALYZE`

**`PRAGMA optimize` hivatalos ajánlott használati minta** (https://www.sqlite.org/pragma.html#pragma_optimize):

> "In most applications, using PRAGMA optimize as follows will help SQLite to achieve the best possible query performance:
> 1. Applications with short-lived database connections should run 'PRAGMA optimize;' once, just prior to closing each database connection.
> 2. Applications that use long-lived database connections should run 'PRAGMA optimize=0x10002;' when the connection is first opened, and then also run 'PRAGMA optimize;' periodically, perhaps once per day or once per hour.
> 3. All applications should run 'PRAGMA optimize;' after a schema change, especially after one or more CREATE INDEX statements."

Ez kifejezetten és szó szerint tartalmazza a kért javaslatot: **kapcsolat lezárása ELŐTT kell lefuttatni**, rövid életű kapcsolatoknál.

A pragma teljesítmény-jellemzőjéről:

> "This pragma is usually a no-op or nearly so and is very fast. On the occasions where it does need to run ANALYZE on one or more tables, it sets a temporary analysis limit, valid for the duration of this pragma only, that prevents the ANALYZE invocations from running for too long."

A MASK argumentum alapértelmezett értéke:

> "The default MASK is 0xfffe."

Az `ANALYZE` külön futtatásának hivatalos ajánlása (https://www.sqlite.org/lang_analyze.html):

> "Statistics gathered by ANALYZE are not updated as the content of the database changes. If the content of the database changes significantly, or if the database schema changes, then one should consider rerunning the ANALYZE command in order to update the statistics."

Az `ANALYZE` és a `PRAGMA optimize` viszonyáról, illetve az ajánlott ütemezésről (ugyanaz az oldal):

> "The PRAGMA optimize command looks at those records and runs ANALYZE on only those tables for which new or updated ANALYZE data seems likely to be useful. In most cases PRAGMA optimize will not run ANALYZE, but it will occasionally do so either for tables that have never before been analyzed, or for tables that have grown significantly since they were last analyzed."

> "it is recommended that PRAGMA optimize be deferred until the database connection is closing and has thus had an opportunity to accumulate as much usage information as possible. It is also reasonable to set a timer to run PRAGMA optimize every few hours, or every few days, for database connections that stay open for a long time."

## Amire NINCS publikált válasz

- **Nincs hivatalos sqlite.org ajánlás rendszeres/ütemezett integritás-ellenőrzésre.** Sem a `pragma.html`, sem a `wal.html`, sem a `howtocorrupt.html` nem mondja ki, hogy „futtasd az `integrity_check`-et naponta/hetente” vagy hasonlót. Ez kifejezett hiány, nem a kutatás mulasztása.
- **Nincs hivatalos, bárhol kimondott konkrét szám (pl. „0 ms”) a `busy_timeout`/`sqlite3_busy_timeout()` alapértelmezett értékére.** A hivatalos oldalak (`pragma.html#pragma_busy_timeout`, `c3ref/busy_timeout.html`) nem közölnek numerikus alapértéket; csak a `c3ref/busy_handler.html` írja le szövegesen, hogy az alapértelmezett busy-callback `NULL`, és emiatt zárolás esetén azonnal `SQLITE_BUSY` érkezik. A „0 ezredmásodperc” tehát levezetett, nem szó szerint dokumentált szám.
- **Nincs konkrét, GB-ban vagy MB-ban kifejezett hivatalos küszöbérték arra, mekkora WAL-fájl számít „túl nagynak”.** A `wal.html` csak kvalitatív leírást ad („grow without bound”, „excess disk space usage and slow query speeds”), számszerű határt nem közöl.
- **A `lockingv3.html` (File Locking And Concurrency In SQLite Version 3) oldalon nem található kifejezett, általános `SQLITE_BUSY` vs. `SQLITE_LOCKED` fogalmi meghatározás vagy holtpont-tárgyalás** — ezt a `rescode.html`, illetve a `c3ref/busy_handler.html` oldalak tartalmazzák, nem a `lockingv3.html`.
- **A `PRAGMA wal_checkpoint` pontos visszatérési sor/oszlopleírását** (hány oszlopot ad vissza és mit jelentenek) a kutatás során nem sikerült megbízhatóan, ellentmondásmentesen verifikálni a `pragma.html` live lekérésével (a lekért tartalom vagy csonkolt volt, vagy egy korábbi lekérésben egymásnak ellentmondó, valószínűleg pontatlan szöveget adott vissza) — ezért ezt az adatot **szándékosan nem** szerepeltetjük állításként a fenti szakaszokban.
- **Home Assistant recorder jelenlegi (2026-os) forráskódjában** nem sikerült egyértelműen, megbízhatóan azonosítani, hogy a 2020-as #37949 PR-ben bevezetett, explicit `PRAGMA QUICK_CHECK`-alapú indítási ellenőrzés változatlanul megvan-e, vagy azt egy más nevű/logikájú (`basic_sanity_check`, SELECT-alapú) ellenőrzés váltotta-e fel. Ez nyitott kérdés marad.
- **Sem a `howtocorrupt.html`, sem a `useovernet.html` oldal nem nevesíti az SMB protokollt vagy bármelyik felhő-szinkronizáló szolgáltatást (Dropbox, iCloud, OneDrive, Google Drive).** Csak általánosságban beszélnek „network filesystem”-ről és NFS-ről; konkrét cloud-sync termékre vonatkozó hivatalos sqlite.org-i figyelmeztetés nem található.
- **Datasette hivatalos dokumentációjában (docs.datasette.io) nem található natív integritás-ellenőrzési funkció** — ezt a kutatás negatív eredményként rögzíti, nem mulasztásként.



---

# SQ06 — Riasztás egyszemélyes rendszerben és a csendes meghibásodás

Ez az összefoglaló azt vizsgálja, mit mond a szakirodalom és a hivatalos dokumentáció a riasztásról olyan helyzetben, ahol nincs ügyeletes csapat, csak egyetlen ember, aki egyszerre üzemeltető és "felhasználó" is. A kanonikus riasztási filozófia (Rob Ewaschuk, Google SRE könyv) forrásszövegei szó szerint kimondják, hogy a riasztás emberi erőforrást éget, minden riasztásnak cselekvést kell kiváltania, és a zajos riasztást inkább el kell hagyni, mint fenntartani — ez egyszemélyes rendszerre még inkább igaz, mert nincs kire szétosztani a terhelést. Az orvosi szakirodalomban (klinikai "alarm fatigue") van kemény, lektorált és szabályozói (Joint Commission) szám a hamis riasztások arányára (85–99%), de informatikai/SRE kontextusban ilyen lektorált mérés nem található — ezt a hiányt a kutatás explicit módon dokumentálja. A "csendes meghibásodás" ellenszereként a dead man's switch / heartbeat minta (healthchecks.io, Cronitor, Prometheus Watchdog/`absent()`) hivatalosan is dokumentált, jól definiált mechanizmus: nem az van megfigyelve, hogy történik-e valami, hanem az, hogy ELMARAD-e a várt jelzés. Az önüzemeltetett eszközök (Uptime Kuma, healthchecks.io) sokféle csatornát támogatnak, köztük asztali (desktop) értesítést is, de ennek van egy dokumentált, kritikus korlátja egyszemélyes/headless szerver esetén. A mentés mint tipikus csendes hiba ellen NIST, CIS és minden vizsgált backup-eszköz (restic, borg, Kopia) hivatalos dokumentációja egyöntetűen a rendszeres, aktív ellenőrzést (nem csak az ütemezést) írja elő, konkrét gyakorisági ajánlásokkal. Az ellenérvre — hogy a riasztási infrastruktúra maga is elromolhat — nem található lektorált vagy szabványforrás, csak гyakorlati blogbejegyzés-szintű anekdota, ezt a kutatás egyértelműen jelzi.

---

## 1. A kanonikus riasztási filozófia és a saját korlátai

### 1.1 Rob Ewaschuk: "My Philosophy on Alerting" (eredeti dokumentum)

Az eredeti, nyilvánosan elérhető Google Doc (szerző: Rob Ewaschuk, korábbi Google SRE) a Google SRE könyv "Monitoring Distributed Systems" fejezetének alapja. Szó szerinti idézetek:

- **Mikor NE riasszunk / zajcsökkentés:** "Err on the side of removing noisy alerts – over-monitoring is a harder problem to solve than under-monitoring." (Összefoglaló szakasz)
- **A riasztás négy kritériuma:** "Pages should be urgent, important, actionable, and real." és "They should represent either ongoing or imminent problems with your service."
- **Az akcióképesség elve:** "Every page should be actionable; simply noting 'this paged again' is not an action." és "Every page should require intelligence to deal with: no robotic, scriptable responses."
- **A riasztás emberi költsége, szó szerint:** "Every time my pager goes off, I should be able to react with a sense of urgency. I can only do this a few times a day before I get fatigued."
- **Pontossági küszöb konkrét számmal:** "Alerts that are less than 50% accurate are broken; even those that are false positives 10% of the time merit more consideration."
- **Az emberi ár összefoglalva:** "The underlying point is to create a system that still has accountability for responsiveness, but doesn't have the high cost of waking someone up, interrupting their dinner, or preventing snuggling with a significant other."
- **Záró mondat (a dokumentum "áldása"):** "May the queries flow, and your pagers be quiet."

Forrás: [My Philosophy on Alerting (Google Docs, Rob Ewaschuk)](https://docs.google.com/document/d/199PqyG3UsyXlwieHaqbGiWVa8eMWi8zzAn0YfcApr8Q/mobilebasic)

### 1.2 Google SRE könyv — "Monitoring Distributed Systems" (6. fejezet, Ewaschuk átdolgozott változata)

A fejezetet maga Ewaschuk írta (szerkesztő: Betsy Beyer), és ez a könyvbeli, "hivatalos" verziója az 1.1 pont filozófiájának:

- **Mikor NE riasszunk, explicit szabály:** "Unless you're performing security auditing on very narrowly scoped components of a system, you should never trigger an alert simply because 'something seems a bit weird.'"
- **A pager-célú szabályok legyenek egyszerűek:** "Similarly, to keep noise low and signal high, the elements of your monitoring system that direct to a pager need to be very simple and robust. Rules that generate alerts for humans should be simple to understand and represent a clear failure."
- **A pager-filozófia három tétele, szó szerint:** "Every time the pager goes off, I should be able to react with a sense of urgency. I can only react with a sense of urgency a few times a day before I become fatigued." / "Every page should be actionable." / "Every page response should require intelligence. If a page merely merits a robotic response, it shouldn't be a page." / "Pages should be about a novel problem or an event that hasn't been seen before."
- **A riasztás mint erőforrás-elvonás:** "Every page that happens today distracts a human from improving the system for tomorrow, so there is often a case for taking a short-term hit to availability or performance in order to improve the long-term outlook for the system."
- **Konkrét esettanulmány a túlriasztásról (Bigtable):** "we also disabled email alerts, as there were so many that spending time diagnosing them was infeasible. […] On-call engineers could actually accomplish work when they weren't being kept up by pages at all hours."

Forrás: [Google SRE Book — Monitoring Distributed Systems (ch. 6)](https://sre.google/sre-book/monitoring-distributed-systems/)

### 1.3 Google SRE könyv — "Being On-Call" (11. fejezet) — a riasztás emberi költsége, számszerűsítve

Ez a fejezet expliciten megadja a riasztás/incidens-kezelés emberi költségét óraszámban:

- **Konkrét óraszám egy riasztásra:** "We've found that on average, dealing with the tasks involved in an on-call incident — root-cause analysis, remediation, and follow-up activities like writing a postmortem and fixing bugs — takes 6 hours. It follows that the maximum number of incidents per day is 2 per 12-hour on-call shift."
- **A zajos riasztás rontja a komoly riasztásra adott reakciót — explicit állítás:** "Misconfigured monitoring is a common cause of operational overload. Paging alerts should be aligned with the symptoms that threaten a service's SLOs. All paging alerts should also be actionable. Low-priority alerts that bother the on-call engineer every hour (or more frequently) disrupt productivity, and the fatigue such alerts induce can also cause serious alerts to be treated with less attention than necessary."
- **Élettani/kognitív hatás, konkrét mechanizmussal:** "Stress hormones like cortisol and corticotropin-releasing hormone (CRH) are known to cause behavioral consequences—including fear—that can impair cognitive functions and cause suboptimal decision making [Chr09]." és "Under the influence of these stress hormones, the more deliberate cognitive approach is typically subsumed by unreflective and unconsidered (but immediate) action, leading to potential abuse of heuristics."
- **Az éjszakai műszak egészségkárosító hatása (a fejezet ezért ajánl multi-site rotációt):** a fejezet expliciten hivatkozik arra, hogy az éjszakai ügyelet egészségre gyakorolt hatása indokolja a több telephelyes elosztást.

Forrás: [Google SRE Book — Being On-Call (ch. 11)](https://sre.google/sre-book/being-on-call/)

**Értelmezési megjegyzés (nem állítás, csak kontextus):** a fenti szabályok mind több fős ügyeleti rotációra lettek kitalálva, de a bennük megfogalmazott alapelv — "csak akkor riassz, ha van tennivaló, és a zajos riasztás rosszabb, mint a hiányzó" — tartalmilag pontosan arra a problémára válaszol, amit egy egyszemélyes rendszer felvet: az egyetlen ember "fatigue budget"-je (naponta "csak néhányszor" tud sürgősen reagálni) ugyanúgy véges, mint egy csapaté, csak nincs kire osztani.

---

## 2. Riasztási fáradtság — van-e mérés?

### 2.1 Orvosi/klinikai terület: IGEN, van lektorált és szabályozói mérés

- **Cvach M. (2012), "Monitor Alarm Fatigue: An Integrative Review"**, *Biomedical Instrumentation & Technology* — a klinikai "alarm fatigue" témakör alapcikke, lektorált folyóiratban. (A teljes szöveg fizetős, a PubMed-bejegyzés és az AAMI-adatbázis megerősíti a cikk létét és tárgyát.)
  Forrás: [PubMed 22839984](https://pubmed.ncbi.nlm.nih.gov/22839984/), [AAMI Array — teljes cikk oldala](https://array.aami.org/doi/full/10.2345/0899-8205-46.4.268)

- **AHRQ PSNet (Agency for Healthcare Research and Quality, kormányzati szakmai testület) szintézise a lektorált irodalomból, konkrét számmal és forrásmegjelöléssel:**
  "Research has shown that 80%–99% of ECG monitor alarms are false or clinically insignificant." — a cikk ezt a Atzema és mtsai. (2006), Lawless (1994), Siebig és mtsai. (2010), valamint Tsien & Fackler (1997) lektorált tanulmányoknak tulajdonítja.
  Forrás: [AHRQ PSNet — Reducing the Safety Hazards of Monitor Alert and Alarm Fatigue](https://psnet.ahrq.gov/perspective/reducing-safety-hazards-monitor-alert-and-alarm-fatigue)

- **The Joint Commission — Sentinel Event Alert #50 (2013), hivatalos szabályozói dokumentum, T1 forrás:**
  "Between 85 and 99 percent of alarm signals do not require clinical intervention."
  A dokumentum azt is kimondja, hogy 2009 január és 2012 június között 98 riasztással kapcsolatos sentinel eseményt regisztráltak, ebből 80 haláleset és 13 tartós funkcióvesztés lett — vagyis a riasztási fáradtságnak közvetlenül mérhető, dokumentált emberi ára van ezen a területen: "In response to this constant barrage of noise, clinicians may turn down the volume of the alarm, turn it off, or adjust the alarm settings outside the limits that are safe and appropriate for the patient – all of which can have serious, often fatal, consequences." A dokumentum a "leggyakoribb hozzájáruló tényezőnek" ("the most common contributing factor") nevezi az alarm fatigue-ot a riasztással kapcsolatos sentinel eseményeknél.
  Forrás: [Joint Commission Sentinel Event Alert #50 (hivatalos PDF)](https://digitalassets.jointcommission.org/api/public/content/f65e5c9df2b94000a99445e0a7877007)

**Az átvihető érv:** ez a mérés azt igazolja, hogy egy magas hamis-riasztási arányú rendszerben (itt: 85–99%) a kezelő fél ténylegesen deszenzitizálódik, és a valódi, kritikus jelzést is figyelmen kívül hagyja vagy késve reagál rá — ez pontosan az a mechanizmus, amit Ewaschuk (1. pont) informálisan ("I can only do this a few times a day before I get fatigued") ír le, csak itt lektorált, számszerűsített formában.

### 2.2 Informatikai/DevOps/SRE terület: NINCS talált lektorált mérés

A kutatás során nem került elő olyan lektorált (peer-reviewed) tanulmány, amely az informatikai/SRE riasztási fáradtságot ugyanolyan módszertannal (pl. a hamis riasztások arányának és a reakcióidő/pontosság romlásának összefüggését) mérné, mint a klinikai szakirodalom. A talált anyagok mind az alábbi kategóriákba esnek:
- iparági/gyártói felmérések (pl. PagerDuty "State of Digital Operations" riportok — ezek önbevalláson alapuló céges felmérések, nem lektorált kutatás),
- blog- és marketingtartalmak (pl. incident.io, Panther, Vectra, oneuptime.com blogjai),
- egy tematikus gyűjtőoldal (pingfatigue.com/research), amely maga is csak iparági riportokra és az orvosi szakirodalomra hivatkozik IT-kontextusban, lektorált IT-specifikus tanulmányt nem idéz.

**Explicit megállapítás:** az informatikai/DevOps/SRE riasztási fáradtságra vonatkozóan nem található lektorált, mért (nem önbevallásos ipari felmérésen alapuló) publikáció, amely számszerűsítené a hamis riasztás aránya és a reakció-minőség romlása közötti összefüggést. Ez tudatos rés (l. "Amire nincs publikált válasz" szakasz).

Forrás (a hiány dokumentálásához): [pingfatigue.com/research](https://pingfatigue.com/research) (T3, tematikus gyűjtőoldal — a saját hivatkozásai alapján erősíti meg a lektorált IT-specifikus irodalom hiányát), [PagerDuty State of Digital Operations](https://www.pagerduty.com/state-of-digital-ops/) (T2, gyártói felmérés, nem lektorált).

---

## 3. A csendes meghibásodás mintája: dead man's switch / heartbeat

### 3.1 A minta elismert neve

A "dead man's switch" kifejezést maguk a szolgáltatók is ezen a néven, expliciten használják a mintára (eredetileg vasúti/ipari biztonságtechnikai fogalom, ld. Wikipedia-hivatkozás mindkét szolgáltató dokumentációjában). A healthchecks.io emellett a "heartbeat monitoring" elnevezést is használja szinonimaként.

### 3.2 healthchecks.io — hivatalos dokumentáció, szó szerint

- **A modell lényege:** "Healthchecks.io listens for HTTP requests ('pings') from your cron jobs and scheduled tasks." / "It keeps silent as long as pings arrive on time." / "It raises an alert as soon as a ping does not arrive on time."
- **A pontos működés cron-feladatra alkalmazva:** "your cron job sends an HTTP request ('ping') to Healthchecks.io every time it completes. When Healthchecks.io does not receive the HTTP request at the expected time, it notifies you."
- **A minta elnevezése, hivatalos forrásból:** "This monitoring technique, sometimes called 'heartbeat monitoring', is a type of [dead man's switch](https://en.wikipedia.org/wiki/Dead_man%27s_switch)."

Forrás: [healthchecks.io/docs/](https://healthchecks.io/docs/), [healthchecks.io/docs/monitoring_cron_jobs/](https://healthchecks.io/docs/monitoring_cron_jobs/)

### 3.3 Cronitor — hivatalos dokumentáció, szó szerint

- "Heartbeat monitoring tracks system health using periodic HTTP requests sent to Cronitor. When heartbeats stop arriving or report failures an alert is sent to the monitor's alert recipients."
- A három komponens: "Heartbeat Event — Simple HTTP request sent from your system to Cronitor" / "Expected Interval — How often Cronitor expects to receive the heartbeat" / "Alert Trigger — Notification sent when heartbeats are missed or are sent with a fail state."
- A marketing oldalon ugyanez tömörebben: "Cronitor expects the next heartbeat and alerts you when it never arrives" — "Alerts fire on absence — no exit code and no error required."

Forrás: [cronitor.io/docs/heartbeat-monitoring](https://cronitor.io/docs/heartbeat-monitoring), [cronitor.io/heartbeat-monitoring](https://cronitor.io/heartbeat-monitoring)

### 3.4 Prometheus — "Watchdog" alert minta (kube-prometheus / Prometheus Operator közösségi konvenció)

**Pontosítás:** a Prometheus mag-projekt hivatalos dokumentációja (prometheus.io) nem definiál külön "Dead Man's Switch" nevű beépített funkciót vagy ajánlott mintát; a "Watchdog" elnevezésű riasztási szabály a **Prometheus Operator / kube-prometheus** hivatalos runbook-gyűjteményéből származik, amely a Prometheus-ökoszisztéma elismert, széles körben használt referenciaimplementációja:

- "This is an alert meant to ensure that the entire alerting pipeline is functional. This alert is always firing, therefore it should always be firing in Alertmanager and always fire against a receiver."
- Az elv: a riasztás folyamatosan tüzel; ha valaha ELTŰNIK a befutó riasztások közül, az önmagában jelzi, hogy a teljes riasztási csővezeték (Prometheus → Alertmanager → értesítési csatorna) elromlott valahol — tipikusan PagerDuty "Dead Man's Snitch" jellegű külső szolgáltatással párosítva, amely a Watchdog HIÁNYÁRA riaszt.

Forrás: [runbooks.prometheus-operator.dev/runbooks/general/watchdog/](https://runbooks.prometheus-operator.dev/runbooks/general/watchdog/)

### 3.5 Az `absent()` függvény — hivatalos Prometheus dokumentáció

**Pontosítás:** az `absent()` egy Prometheus PromQL lekérdezési függvény (nem az Alertmanager funkciója); az Alertmanager csak az ebből épített riasztási szabályt routolja/csillapítja. Hivatalos, szó szerinti dokumentáció:

- "`absent(v instant-vector)` returns an empty vector if the vector passed to it has any elements (float samples or histogram samples) and a 1-element vector with the value 1 if the vector passed to it has no elements."
- Célja: "This is useful for alerting on when no time series exist for a given metric name and label combination."

Forrás: [prometheus.io — Query functions, `absent()`](https://prometheus.io/docs/prometheus/latest/querying/functions/#absent)

**Összegzés a 3. ponthoz:** mindhárom eszköz (healthchecks.io, Cronitor, Prometheus Watchdog+`absent()`) ugyanazt az elvet valósítja meg hivatalosan dokumentált módon: nem azt figyelik, hogy TÖRTÉNIK-e hiba, hanem azt, hogy ELMARAD-e egy várt, pozitív jelzés — ez pontosan az "észrevétlen meghibásodás" (a mentés hónapok óta nem fut, az index elavult) elleni architekturális védekezés kanonikus mintája.

---

## 4. Riasztási csatorna ügyeletes nélkül

### 4.1 Uptime Kuma — hivatalosan dokumentált csatornák

Az Uptime Kuma saját, natívan beépített értesítési szolgáltatói (a projekt hivatalos forráskód-könyvtára és a GitHub-issue #284, amelyben a karbantartók összesítik a támogatott listát) között szerepel: Telegram, Webhook, SMTP (e-mail), Discord, Signal, Gotify, Slack, Rocket.chat, Pushover, Pushy, Octopush, LunaSea, Pushbullet, Line Messenger, Mattermost. Emellett az **Apprise** integráción keresztül még kb. 65 további szolgáltatás érhető el (pl. AWS SNS, Microsoft Teams, Twilio, Google Firebase Cloud Messaging stb.).

Forrás: [GitHub — louislam/uptime-kuma, Issue #284 "Full List of Supported Notifications"](https://github.com/louislam/uptime-kuma/issues/284), [GitHub — louislam/uptime-kuma wiki, Notification Methods](https://github.com/louislam/uptime-kuma/wiki/Notification-Methods)

**Van-e asztali (desktop) értesítés?** Igen, az Apprise integráción keresztül, amelyet Uptime Kuma hivatalosan támogat. Az Apprise saját, hivatalos wiki-dokumentációja szerint (`Notify_dbus` szolgáltatás):

- "Display notifications right on your Gnome or KDE desktop. This only works if you're sending the notification to the same system you're currently accessing."
- Támogatott URL-sémák: `dbus://`, `qt://` (KDE), `kde://`, `glib://` (Gnome/Unity). Emellett külön szolgáltatásként létezik macOS X és Windows natív asztali értesítés is.

Forrás: [GitHub — caronc/apprise wiki, Notify_dbus](https://github.com/caronc/apprise/wiki/Notify_dbus)

**Kritikus, dokumentált korlát egyszemélyes/szerver-kontextusra:** a hivatalos szöveg explicit módon kimondja, hogy az asztali értesítés **csak akkor működik, ha ugyanarra a gépre küldi a szolgáltatás az üzenetet, amelyiket éppen használod** ("the same system you're currently accessing") — vagyis egy headless/távoli szerveren futó Uptime Kuma esetén az asztali csatorna csak akkor él, ha a monitorozó szoftver és az aktív desktop-munkamenet (D-Bus session) ugyanazon a gépen fut, amelyiket a felhasználó ténylegesen néz. Ez direkt releváns egy egygépes rendszerre, ahol ez adott lehet, de a helyi grafikus munkamenet (bejelentkezett desktop, D-Bus) meglétéhez van kötve, nem egy szerver szolgáltatáshoz általában.

### 4.2 healthchecks.io — hivatalosan dokumentált csatornák

A hivatalos dokumentáció (Configuring Notifications) alapján támogatott csatornák: e-mail, SMS, WhatsApp, telefonhívás (mindhárom havi kvótával), Slack, Pushover (ezen belül "Emergency" prioritási szint ismételt értesítéssel), valamint incidenskezelő rendszerek: PagerDuty, Splunk On-Call, Opsgenie, PagerTree.

Forrás: [healthchecks.io/docs/configuring_notifications/](https://healthchecks.io/docs/configuring_notifications/)

### 4.3 Van-e adat arról, melyik csatornát veszik ténylegesen észre?

Nem található megbízható, mért (nem marketing-) forrás erre a kérdésre. A talált anyagok kizárólag anekdotikus/marketing jellegűek (pl. egy MakeUseOf véleménycikk "I replaced all my server email alerts with push notifications — I actually read them now" címmel, illetve a Derdack nevű riasztó-szoftver gyártó saját blogbejegyzése a push-értesítések megbízhatósági korlátairól). Ezek T3 (illetve gyártói T2) szintű, nem mérési, hanem véleményforrások — konkrét szám vagy módszertan nélkül, ezért itt nem idézünk belőlük számot. Ez explicit rés (l. lent).

Forrás (csak az anekdota létezésének dokumentálására, NEM mérésként idézve): [MakeUseOf — I replaced all my server email alerts with push notifications](https://www.makeuseof.com/i-replaced-all-my-server-email-alerts-with-push-notifications-i-actually-read-them-now/), [Derdack — Push notifications are not reliable for critical alerting](https://www.derdack.com/push-notifications-are-not-reliable-for-critical-alerting/)

Egy releváns, jó minőségű Pushover-specifikus adalék viszont hivatalos forrásból (healthchecks.io dokumentáció) van: a Pushover "Emergency" prioritási szintje kifejezetten azért létezik, mert az alap push-értesítés elnémítható/kihagyható, és az "Emergency" mód ismételten küldi az értesítést, amíg nyugtázzák — ez implicit elismerése annak, hogy egyetlen push-értesítés nem garantáltan kerül észlelésre.

---

## 5. A mentés mint tipikus csendes meghibásodás

### 5.1 NIST SP 800-34 Rev. 1 (Contingency Planning Guide for Federal Information Systems) — hivatalos szövetségi ajánlás

- **Explicit előírás a rendszeres teszt-ellenőrzésre:** "Backup tapes should be tested regularly to ensure that data are being stored correctly and that the files may be retrieved without errors or lost data." (3. fejezet, lábjegyzet)
- **Kontrollkövetelmény-táblázat (CP-9, System Backup):** "Test backup information to verify media reliability and information integrity." — közepes és magas hatású rendszerekre kötelezőként megjelölve ("Mod. Impact = Yes, High Impact = Yes").
- **A kapcsolódó biztonsági kontroll (CP-9) bővítése:** "(1) The organization tests backup information [Assignment: organization-defined frequency] to verify media reliability and information integrity." — vagyis a gyakoriságot a szervezetnek kell rögzítenie, de a TESZTELÉS KÖTELEZŐ, nem csak az ütemezés.

Forrás: [NIST SP 800-34 Rev. 1 (hivatalos PDF)](https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-34r1.pdf)

### 5.2 CIS Controls v8 — 11.5 Test Data Recovery

- Kontroll-szöveg, szó szerint: "Test backup recovery quarterly, or more frequently, for a sampling of in-scope enterprise assets."

Forrás: [CSF Tools — CIS Control 11.5](https://csf.tools/reference/critical-security-controls/v8-1/csc-11/csc-11-5/)

### 5.3 AWS Well-Architected Framework — REL09-BP04 (gyártói, de széles körben idézett iparági ajánlás, T2)

- **A kívánt állapot:** "Data from backups is periodically recovered using well-defined mechanisms to verify that recovery is possible within the established recovery time objective (RTO) for the workload."
- **A tipikus hibás minta, amit expliciten anti-patternnek nevez:** "Assuming that a backup exists." / "Assuming that the backup of a system is fully operational and that data can be recovered from it." / "Restoring a backup, but not querying or retrieving any data to check that the restoration is usable."

Forrás: [AWS Well-Architected — REL09-BP04](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_backing_up_data_periodic_recovery_testing_data.html)

### 5.4 restic — hivatalos dokumentáció

- "it's a good idea to regularly use the `check` command to test whether your repository is healthy and consistent, and that your precious backup data is unharmed."
- Ha a `check` hibát jelez: "If check reports an error in the repository, then you must repair the repository. As long as a repository is damaged, restoring some files or directories will fail."
- Konkrét gyakoriságot a hivatalos dokumentáció nem ad meg számszerűen (nem mondja ki pl. "hetente"), csak azt, hogy "regularly", és hogy a teljes adat-integritás-ellenőrzés (`--read-data`) drágább/lassabb, ezért részleges mintavétellel (`--read-data-subset=x%`) is végezhető, tipikusan minden mentés után automatizálva.

Forrás: [restic.readthedocs.io — Checking integrity and consistency](https://restic.readthedocs.io/en/stable/045_working_with_repos.html)

### 5.5 BorgBackup — hivatalos dokumentáció

- "The check command verifies the consistency of a repository and its archives."
- Konkrét gyakorlati ajánlás időkorláttal particionált ellenőrzésre: "Assuming a complete check would take 7 hours, then running a daily check with `--max-duration=3600` (1 hour) would result in one full repository check per week." — vagyis a hivatalos dokumentáció explicit módon egy heti teljes ellenőrzési ciklust javasol napi részleges futtatásokból összerakva.
- Figyelmeztetés a javító módra: "`--repair` is a POTENTIALLY DANGEROUS FEATURE and might lead to data loss!"

Forrás: [borgbackup.readthedocs.io — borg check](https://borgbackup.readthedocs.io/en/stable/usage/check.html)

### 5.6 Kopia — hivatalos dokumentáció

- **Automatikus, beépített ellenőrzés:** "Both Kopia CLI and KopiaUI automatically run `kopia snapshot verify` during every daily full maintenance, so you do not need to run the command yourself."
- **Mit ellenőriz alapból, és mit NEM:** "it verifies that the content manager index structures are correct and that every index entry is backed by an existing file" — de "does not test whether blobs have been corrupted after they have been uploaded by Kopia, due to bit rot, bit flip, etc."
- **Konkrét, számszerű gyakorisági ajánlás a mélyebb ellenőrzésre:** "it is recommended to at least run `kopia snapshot verify --verify-files-percent=1 --file-parallelism=10` daily. If you run this command daily, statistically over the course of a year you have a roughly 98% likelihood to have tested 100% of your backed up data." Alternatívaként havi vagy ritkább teljes (`--verify-files-percent=100`) ellenőrzést javasol.

Forrás: [kopia.io — Verifying Validity of Snapshots/Repositories](https://kopia.io/docs/advanced/consistency/)

**Összegzés az 5. ponthoz:** minden vizsgált hivatalos forrás (két szabvány/kormányzati ajánlás, egy gyártói keretrendszer, három nyílt forráskódú backup-eszköz dokumentációja) egybehangzóan állítja, hogy a mentés ÜTEMEZÉSE önmagában nem elég — a mentés SIKERESSÉGÉT/HELYREÁLLÍTHATÓSÁGÁT külön, rendszeresen, aktívan ellenőrizni kell. A gyakoriságra van konkrét szám (CIS: negyedévente vagy gyakrabban; Kopia: napi 1%-os minta ~98%-os éves lefedettséggel, vagy havi teljes ellenőrzés; Borg: heti egy teljes ciklus napi részletekben), de NIST és restic esetén a gyakoriság szervezet/felhasználó-függő ("organization-defined frequency", illetve "regularly").

---

## 6. Az ellenérv: mikor rosszabb a riasztás, mint a semmi — a riasztási infrastruktúra maga is elromolhat

**Ehhez a kérdéshez nem található lektorált tanulmány, szabvány vagy hivatalos gyártói állásfoglalás.** A kutatás során talált egyetlen konkrét, tartalmilag releváns forrás egy személyes blogbejegyzés, amely kifejezetten a témára (egygépes megfigyelő-verem önmeghibásodása) reflektál:

- "if that box goes down, nothing can alert me, because the thing that sends alerts is the thing that's down."
- Konkrét, megtörtént eset leírásaként: "Prometheus once sat dead for two days before I noticed, and only because a dashboard had gone blank."

Forrás (T3, anekdota — NEM mérés vagy szabvány): [paulsprogrammingnotes.com — A dead man's switch for a single-host monitoring stack](https://www.paulsprogrammingnotes.com/2026/07/dead-mans-switch-single-host-monitoring.html)

Ezen kívül több hasonló témájú blogbejegyzés (pl. "Monitor Prometheus So Its Failure Cannot Silence Host-Down Alerts", "Your Uptime Monitoring Is Broken By Design") tárgyalja ugyanezt a mintát ("ki figyeli a figyelőt" probléma), de ezek is mind T3 iparági blogtartalmak, gyártói vagy magánszemélyi vélemény, nem lektorált vagy szabványforrás.

**Explicit megállapítás:** ez a pont — hogy egy egyszemélyes/hobbi rendszernél a riasztási infrastruktúra maga is karbantartandó és el tud romlani, ezáltal hamis biztonságérzetet adva — jelenleg **kizárólag anekdota szintjén dokumentált**, komoly (lektorált, szabványügyi vagy elismert szakkönyvi) forrás nem támasztja alá számszerűen vagy normatívan. A Google SRE könyv sem tér ki explicit módon erre (a könyv feltételezi, hogy a monitoring-infrastruktúrát maga is egy külön SRE-csapat tartja fenn, tehát a "ki figyeli a megfigyelőt" kérdés ott szervezeti válasz, nem architekturális).

---

## Amire NINCS publikált válasz

1. **Nincs lektorált, mért tanulmány** az informatikai/DevOps/SRE riasztási fáradtságról, amely számszerűsítené a hamis riasztás aránya és a reakcióminőség (pl. válaszidő, hibás triázs) romlása közötti összefüggést — szemben az orvosi területtel, ahol ez (Cvach 2012, Joint Commission Sentinel Event Alert #50) létezik.
2. **Nincs mért/lektorált adat arról, hogy egyszemélyes/önüzemeltetett kontextusban melyik értesítési csatornát (e-mail, push, asztali, SMS) veszik ténylegesen észre nagyobb valószínűséggel.** Csak anekdotikus véleménycikkek és egy gyártói (Derdack) marketingérvelés található.
3. **Nincs szabvány, lektorált forrás vagy elismert szakkönyvi állásfoglalás arról, hogy egy egyszemélyes/hobbi rendszernél a riasztási infrastruktúra saját meghibásodása mikor rosszabb, mint riasztás nélkül üzemelni** — ez jelenleg kizárólag blogszintű anekdota (l. 6. pont).
4. **A restic és a NIST SP 800-34 dokumentáció nem ad számszerű ellenőrzési gyakoriságot** (csak "regularly", illetve "organization-defined frequency") — ezzel szemben a Kopia és a CIS Controls igen (napi minta / negyedévente).
5. **Nem található hivatalos Prometheus mag-projekt dokumentáció**, amely saját néven "Dead Man's Switch" mintát definiálna; ez a Prometheus Operator/kube-prometheus közösségi konvenciója ("Watchdog" alert), nem a prometheus.io hivatalos referenciája — ezt a különbséget a 3.4 pontban külön jeleztük, nehogy tévesen "Prometheus hivatalos ajánlásaként" kerüljön be a specifikációba.

---



---

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



---

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



---

# ELL03 — SQLite állítások ellenőrzése

**Módszertani megjegyzés.** Ez az ellenőrzés a `deep-web-research` skill **degradált** módjában készült: a futtató munkamenet nem ért el Agent/subagent-dispatch eszközt, ezért nem volt külön Sonnet-kereső hullám és külön Opus-szintézis — ezt a skill saját szabálya szerint itt rögzítem. Kompenzálásul minden állítást **közvetlenül letöltött, nyers HTML-ből** (`curl` a sqlite.org domainről) és a **hivatalos, csak-olvasható SQLite forráskód-tükörből** (`github.com/sqlite/sqlite`, amelyre maga a sqlite.org is hivatkozik forráskód-elérésként) ellenőriztem szövegkereséssel (`grep`/Python), nem összefoglaló-eszköz (pl. LLM-alapú lapfeldolgozó) kimenetéből. Ez kizárja az LLM-parafrázisból eredő idézet-pontatlanságot. Két állításnál (2c és 4b) a hivatalos próza-dokumentáció hallgat vagy csak közvetett, ezért a hivatalos SQLite forráskódot is bevontam (a `sqlite.org/src` fossil-webfelület robot-elhárítása miatt az `src/vacuum.c` és `src/shell.c.in` fájlokat a hivatalos GitHub-tükörről töltöttem le).

A teljes bizonyíték-vault (9 archivált forrás, 15 rögzített idézet, 100%-os idézet-egyezés) itt található: `/home/claude/work/kutatas-uzemeltetes/.research/ell03-sqlite/`.

---

## Ítélet

| # | Állítás | Ítélet |
|---|---|---|
| 1 | `quick_check` O(N), `integrity_check` O(N log N) | **IGAZOLVA** — szó szerint így áll a dokumentációban |
| 1b | A `quick_check` kihagyja a UNIQUE-ellenőrzést és az index/tábla-tartalom egyezés-ellenőrzést | **IGAZOLVA** |
| 2a | A `busy_timeout`-nak nincs számszerű hivatalos alapértéke | **IGAZOLVA** |
| 2b | Alapból nincs busy handler (NULL), ezért azonnal `SQLITE_BUSY` jön | **IGAZOLVA** |
| 2c | A `sqlite3` CLI-nek saját (nullától eltérő) alapértelmezett busy timeoutja van | **CÁFOLVA** — a forráskód szerint nincs ilyen |
| 3 | `wal_autocheckpoint` alapértéke 1000 oldal | **IGAZOLVA** — pragma.html és wal.html is megerősíti |
| 3b | 1000 oldal ≈ 4 MB (4096 bájtos lapmérettel) | **IGAZOLVA** — a dokumentáció maga mondja ki a "~4MB"-ot |
| 4 | A `VACUUM INTO` kimenete nem őrzi meg a forrás `journal_mode`-ját (delete módban jön létre) | **RÉSZBEN** — a dokumentáció explicit **hallgat** a `journal_mode`-ról; a forráskód és egy általános pragma-mondat közvetve alátámasztja a mérést |
| 4b | `page_size`, `auto_vacuum`, `user_version`, `application_id` öröklődik a VACUUM(INTO) kimenetére | **IGAZOLVA** — forráskód szerint (a dokumentáció csak a `page_size`/`auto_vacuum`-ot említi kifejezetten) |
| 5a | `VACUUM INTO` nem futtatható nyitott tranzakción belül | **IGAZOLVA** — forráskód + doksi együtt |
| 5b | Létező célfájlra hiba: *"output file already exists"* | **IGAZOLVA** — szó szerint ez a forráskódi hibaüzenet |
| 5c | Dokumentált-e, mi történik félbeszakadt `VACUUM INTO`-nál | **RÉSZBEN** — a "korrupt/hiányos" kimenet dokumentált, de a félkész fájl sorsáról (megmarad-e a lemezen) nincs explicit mondat |
| 6 | `VACUUM INTO` pillanatkép-szemantikája dokumentált | **IGAZOLVA** (röviden) |
| 6b | A dokumentáció a `VACUUM INTO`-nál éppúgy tárgyalja a párhuzamos írást, mint a `sqlite3_backup` API-nál | **CÁFOLVA** — a `backup.html` sokkal részletesebb, a `lang_vacuum.html` **hallgat** a párhuzamos írásról |
| 7 | `VACUUM INTO` kimenete nem tartalmazza a törölt tartalmat | **IGAZOLVA** — szó szerint "no forensic traces" |

---

## 1. `quick_check` vs `integrity_check` — O(N) vs O(N log N)

**URL:** https://www.sqlite.org/pragma.html#pragma_quick_check

**Szó szerinti idézet:**

> "The pragma is like integrity_check except that it does not verify UNIQUE constraints and does not verify that index content matches table content. By skipping UNIQUE and index consistency checks, quick_check is able to run faster. PRAGMA quick_check runs in O(N) time whereas PRAGMA integrity_check requires O(NlogN) time where N is the total number of rows in the database. Otherwise the two pragmas are the same."

**Ítélet: IGAZOLVA, szó szerint.** A vizsgált állítás pontosan megfelel a hivatalos szövegnek — nem kellett parafrazálni vagy közelítő megfogalmazást keresni.

**Mit hagy ki pontosan a `quick_check`?** A dokumentáció szerinti teljes felsorolás (két elem):
1. "it does not verify UNIQUE constraints"
2. "does not verify that index content matches table content"

Minden más tekintetben ("Otherwise the two pragmas are the same") a két PRAGMA azonos ellenőrzéseket végez.

---

## 2. `busy_timeout` alapértéke és a CLI saját alapértéke

### 2a–2b. C API és PRAGMA szintje

**URL:** https://www.sqlite.org/c3ref/busy_handler.html

**Szó szerinti idézet:**

> "If the busy callback is NULL, then SQLITE_BUSY is returned immediately upon encountering the lock. If the busy callback is not NULL, then the callback might be invoked with two arguments." […] "The default busy callback is NULL."

**URL:** https://www.sqlite.org/c3ref/busy_timeout.html

**Szó szerinti idézet:**

> "This routine sets a busy handler that sleeps for a specified amount of time when a table is locked. […] Calling this routine with an argument less than or equal to zero turns off all busy handlers."

Ez az oldal **nem** ad meg semmilyen numerikus alapértéket a busy timeout-hoz — csak a mechanizmust írja le.

**URL:** https://www.sqlite.org/pragma.html#pragma_busy_timeout

**Szó szerinti idézet (a teljes szakasz):**

> "Query or change the setting of the busy timeout. This pragma is an alternative to the sqlite3_busy_timeout() C-language interface which is made available as a pragma for use with language bindings that do not provide direct access to sqlite3_busy_timeout(). Each database connection can only have a single busy handler. This PRAGMA sets the busy handler for the process, possibly overwriting any previously set busy handler."

Ez a szakasz — más pragmákkal ellentétben (pl. `wal_autocheckpoint`, ahol kifejezetten szerepel "enabled by default with an interval of 1000") — **nem tartalmaz egyetlen számot sem** alapértékként. Ez pontosan alátámasztja az ellenőrizendő állítást: nincs számszerű hivatalos alapérték kimondva erre a pragmára, csak a viselkedés van leírva (NULL handler → azonnali `SQLITE_BUSY`).

A `busy_handler.html` külön dokumentálja a holtpont-elkerülési esetet is:

> "The presence of a busy handler does not guarantee that it will be invoked when there is lock contention. If SQLite determines that invoking the busy handler could result in a deadlock, it will go ahead and return SQLITE_BUSY to the application instead of invoking the busy handler."

**Ítélet: IGAZOLVA.** A `busy_timeout`-nak nincs dokumentált számszerű alapértéke; a busy handler alapból NULL, ezért zárolás esetén a hívás azonnal `SQLITE_BUSY`-t ad vissza — ez szó szerint így szerepel a hivatalos C API dokumentációban.

### 2c. Van-e a `sqlite3` CLI-nek saját alapértelmezett busy timeoutja?

A `cli.html` (https://www.sqlite.org/cli.html) csak ennyit mond a `.timeout` parancsról:

> ".timeout MS              Try opening locked tables for MS milliseconds"

— **nem ad meg semmilyen alapértéket**, és a dokumentáció egyáltalán nem tér ki arra, hogy a shell indításkor beállít-e valamilyen busy timeout-ot.

Mivel a hivatalos dokumentáció itt **hallgat**, a kérdést a hivatalos forráskódból (`github.com/sqlite/sqlite`, `src/shell.c.in`) ellenőriztem. A `sqlite3_busy_timeout()` C-függvénynek **egyetlen** hívása van a teljes shell forrásában, a `.timeout` meta-parancs kezelőjében:

```c
if( c=='t' && n>4 && cli_strncmp(azArg[0], "timeout", n)==0 ){
    open_db(p, 0);
    sqlite3_busy_timeout(p->db, nArg>=2 ? (int)integerValue(azArg[1]) : 0);
}else
```
— (`src/shell.c.in`, github.com/sqlite/sqlite, `master` ág, 13003–13005. sor)

A kapcsolatot megnyitó `open_db()` függvényben (5065. sortól) **nincs** `sqlite3_busy_timeout()` vagy `sqlite3_busy_handler()` hívás. Vagyis a shell indításkor, `.timeout` parancs nélkül, **nem** állít be saját busy timeout-ot — a könyvtár sima alapértéke (NULL handler, azonnali `SQLITE_BUSY`) érvényesül. Ha a felhasználó `.timeout` argumentum nélkül futtatja, az `0`-t ad át, ami — a `busy_timeout.html` szerint — "turns off all busy handlers", azaz kifejezetten kikapcsolja azt.

**Ítélet: CÁFOLVA (a gyakori félreértéssel szemben).** A hivatalos dokumentáció nem állít semmit erről explicit módon (sem "van", sem "nincs" — ezt ki kell mondani: **a dokumentáció hallgat róla**), de a hivatalos forráskód egyértelműen mutatja, hogy a `sqlite3` parancssori eszköznek **nincs** saját, nullától eltérő alapértelmezett busy timeoutja.

---

## 3. `wal_autocheckpoint` alapértéke — 1000 oldal / ~4 MB

**URL:** https://www.sqlite.org/wal.html#automatic_checkpoint (és a 6. "Avoiding Excessively Large WAL Files" szakasz)

**Szó szerinti idézetek:**

> "By default, SQLite will automatically checkpoint whenever a COMMIT occurs that causes the WAL file to be 1000 pages or more in size, or when the last database connection on a database file closes."

> "In normal cases, new content is appended to the WAL file until the WAL file accumulates about 1000 pages (and is thus about 4MB in size) at which point a checkpoint is automatically run and the WAL file is recycled."

**URL:** https://www.sqlite.org/pragma.html#pragma_wal_autocheckpoint

**Szó szerinti idézet:**

> "Autocheckpointing is enabled by default with an interval of 1000 or SQLITE_DEFAULT_WAL_AUTOCHECKPOINT."

**Bájtban, 4096 bájtos lapmérettel:** 1000 × 4096 bájt = 4 096 000 bájt (≈ 3,91 MiB). A `pragma.html#pragma_page_size` megerősíti, hogy 4096 bájt a lapméret alapértéke SQLite 3.12.0 (2016-03-29) óta:

> "beginning with SQLite version 3.12.0 (2016-03-29), the default page size increased to 4096."

A `wal.html` **saját maga mondja ki a konkrét MB-számot**: "about 1000 pages (and is thus about 4MB in size)" — tehát a dokumentáció nem hallgat erről, hanem kifejezetten megadja a kerekített 4 MB-os értéket (nem a pontos 4 096 000 bájtot, hanem "about 4MB"-ot).

**Ítélet: IGAZOLVA**, mind a wal.html, mind a pragma.html oldalon, szó szerint.

---

## 4. `VACUUM INTO` és a `journal_mode` öröklődése

**URL:** https://www.sqlite.org/lang_vacuum.html

A teljes oldalon (`grep`-pel ellenőrizve) a `journal_mode` kifejezés **egyszer sem fordul elő**. A dokumentáció **kifejezetten hallgat** arról, hogy a `VACUUM INTO` kimenete milyen naplózási módban jön létre.

Amit a dokumentáció **igen** kimond az öröklődő tulajdonságokról:

> "Normally, the database page_size and whether or not the database supports auto_vacuum must be configured before the database file is actually created. However, when not in write-ahead log mode, the page_size and/or auto_vacuum properties of an existing database may be changed by using the page_size and/or pragma auto_vacuum pragmas and then immediately VACUUMing the database."

Ez a mondat a `page_size`/`auto_vacuum` **beállítási mechanizmusáról** szól, nem kifejezetten a `VACUUM INTO` öröklődéséről. A pontos öröklődési listát a **forráskód** (`src/vacuum.c`, `sqlite3RunVacuum()`) adja meg egyértelműen:

```c
sqlite3BtreeSetPageSize(pTemp, sqlite3BtreeGetPageSize(pMain), nRes, 0)   /* page_size öröklődik */
...
sqlite3BtreeSetAutoVacuum(pTemp, db->nextAutovac>=0 ? db->nextAutovac :
                                         sqlite3BtreeGetAutoVacuum(pMain));  /* auto_vacuum öröklődik */
...
static const unsigned char aCopy[] = {
   BTREE_SCHEMA_VERSION,     1,  /* Add one to the old schema cookie */
   BTREE_DEFAULT_CACHE_SIZE, 0,  /* Preserve the default page cache size */
   BTREE_TEXT_ENCODING,      0,  /* Preserve the text encoding */
   BTREE_USER_VERSION,       0,  /* Preserve the user version */
   BTREE_APPLICATION_ID,     0,  /* Preserve the application id */
};
```
— (`src/vacuum.c`, github.com/sqlite/sqlite, kb. 281., 290. és 358–363. sor)

Vagyis a forráskód szerint **explicit módon öröklődik**: `page_size`, `auto_vacuum`, `user_version`, `application_id` (és a séma-verzió +1-gyel, valamint a szövegkódolás). A `journal_mode` **nem szerepel** ebben a listában, és sehol máshol a fájlban nincs olyan hívás, amely a `VACUUM INTO` célfájljának naplózási módját a forrás `journal_mode`-jára állítaná.

Ezt közvetve alátámasztja egy általános (nem VACUUM-specifikus) pragma-mondat is:

**URL:** https://www.sqlite.org/pragma.html#pragma_journal_mode

> "The DELETE journaling mode is the default."

Mivel a `VACUUM INTO` egy vadonatúj fájlt hoz létre (`ATTACH`-csal), és a forráskód nem állítja be rajta a `journal_mode`-ot a forrás alapján, az új fájl az általános SQLite-alapértelmezésen (DELETE) marad — ez **magyarázza**, de nem **mondja ki explicit módon** a mért jelenséget ("a mentés delete módban jön létre, nem WAL-ban").

**Ítélet: RÉSZBEN.** A `lang_vacuum.html` és a `pragma.html` egyaránt **hallgat** arról, hogy a `VACUUM INTO` kimenete milyen `journal_mode`-ban jön létre — ezt itt ki kell mondani, nem szabad logikával pótolni a hivatalos-forrás-idézetek helyén. A mért jelenség (delete mód, nem WAL) a forráskód elemzésével **magyarázható és konzisztens** (a `journal_mode` nincs az öröklődő tulajdonságok listáján, és az általános alapértelmezés DELETE), de ez forráskód-szintű következtetés, nem dokumentációs kijelentés.

---

## 5. `VACUUM INTO` tranzakció-tilalom, "output file already exists", félbeszakadás

### 5a. Nyitott tranzakción belüli tilalom

**URL:** https://www.sqlite.org/lang_vacuum.html

**Szó szerinti idézet:**

> "A VACUUM will fail if there is an open transaction on the database connection that is attempting to run the VACUUM. Unfinalized SQL statements typically hold a read transaction open, so the VACUUM might fail if there are unfinalized SQL statements on the same connection. VACUUM (but not VACUUM INTO) is a write operation and so if another database connection is holding a lock that prevents writes, then the VACUUM will fail."

Ez a bekezdés a `VACUUM`/`VACUUM INTO` közös leírásán belül van, közvetlenül azután, hogy a szöveg kifejezetten megkülönbözteti a kettőt ("VACUUM (but not VACUUM INTO) is a write operation…") — vagyis a nyitott tranzakcióra vonatkozó tiltás **nem** kap kivételt a `VACUUM INTO` számára, csak a másik kapcsolat write-lockjára vonatkozó rész.

Ezt a **forráskód egyértelműen megerősíti**: a tranzakció-ellenőrzés a `VACUUM INTO`-ági elágazás (`pOut`) **előtt** fut le, tehát mindkét formára vonatkozik:

```c
if( !db->autoCommit ){
    sqlite3SetString(pzErrMsg, db, "cannot VACUUM from within a transaction");
    return SQLITE_ERROR; /* IMP: R-12218-18073 */
}
```
— (`src/vacuum.c`, github.com/sqlite/sqlite, 169–171. sor, a `pOut` néven megkülönböztetett `VACUUM INTO`-ág előtt)

**Ítélet: IGAZOLVA**, dokumentáció + forráskód együtt.

### 5b. "output file already exists"

**URL:** https://www.sqlite.org/lang_vacuum.html

**Szó szerinti idézet (dokumentáció):**

> "The file named by the INTO clause must not previously exist, or else it must be an empty file, or the VACUUM INTO command will fail with an error."

A dokumentáció nem idézi szó szerint a hibaüzenet szövegét, csak a szabályt írja le. A **pontos hibaüzenet-string** a forráskódban van:

```c
if( id->pMethods!=0 && (sqlite3OsFileSize(id, &sz)!=SQLITE_OK || sz>0) ){
    rc = SQLITE_ERROR;
    sqlite3SetString(pzErrMsg, db, "output file already exists");
    goto end_of_vacuum;
}
```
— (`src/vacuum.c`, github.com/sqlite/sqlite, 236–241. sor)

**Ítélet: IGAZOLVA, szó szerint egyezik** ("output file already exists") — de a pontos szöveg forrása a **forráskód**, nem a lang_vacuum.html próza (az csak a szabályt írja le, az üzenetet nem idézi).

### 5c. Félbeszakadt `VACUUM INTO`

**URL:** https://www.sqlite.org/lang_vacuum.html

**Szó szerinti idézet:**

> "The VACUUM INTO command is transactional in the sense that the generated output database is a consistent snapshot of the original database. However, if the VACUUM INTO command is interrupted by an unplanned shutdown or power loss, then the generated output database might be incomplete and corrupt."

> "However, if the PRAGMA synchronous setting of the original database is NORMAL or FULL, then SQLite invokes fsync() or FileFlushBuffers() to sync the output database to disk after it has been written. This means that in these cases, a power failure or unplanned shutdown that occurs after the VACUUM INTO command has completed should not corrupt the database."

**Ítélet: RÉSZBEN.** A dokumentáció **nem hallgat teljesen** erről — kifejezetten kimondja, hogy megszakítás (áramkimaradás, tervezetlen leállás) esetén a kimeneti adatbázis **"incomplete and corrupt"** lehet. Amiről viszont **explicit módon hallgat**: hogy a félkész célfájl a lemezen **marad-e** (nincs törlés/cleanup lépés említve), vagy hogy a fájlrendszer szintjén milyen méretű/állapotú fájl marad vissza. Ez utóbbi kérdésre nincs szó szerinti válasz a dokumentációban — ezt itt ki kell mondani, nem szabad kikövetkeztetni.

---

## 6. `VACUUM INTO` pillanatkép-szemantikája vs. `sqlite3_backup` API

**URL:** https://www.sqlite.org/lang_vacuum.html

**Szó szerinti idézet (a `VACUUM INTO` teljes vonatkozó szövege):**

> "The VACUUM INTO command is transactional in the sense that the generated output database is a consistent snapshot of the original database."

Ez az **egyetlen** mondat a `lang_vacuum.html`-en, amely a pillanatkép-jelleget tárgyalja. A párhuzamos írásokról **semmi mást nem mond** ez az oldal — nincs benne olyan bekezdés, amely arról szólna, mi történik, ha egy másik kapcsolat a `VACUUM INTO` futása közben ír az adatbázisba.

**URL:** https://www.sqlite.org/backup.html (3.1. "File and Database Connection Locking")

**Szó szerinti idézet:**

> "During the 250 ms sleep in step 3 above, no read-lock is held on the database file and the mutex associated with pDb is not held. This allows other threads to use database connection pDb and other connections to write to the underlying database file."

> "If another thread or process writes to the source database while this function is sleeping, then SQLite detects this and usually restarts the backup process when sqlite3_backup_step() is next called. There is one exception to this rule: If the source database is not an in-memory database, and the write is performed from within the same process as the backup operation and uses the same database handle (pDb), then the destination database […] is automatically updated along with the source."

> "Whether or not the backup process is restarted as a result of writes to the source database mid-backup, the user can be sure that when the backup operation is completed the backup database contains a consistent and up-to-date snapshot of the original."

**Összehasonlítás:** A `backup.html` egy teljes alfejezetet (3.1.) szentel annak, hogy pontosan mi történik, ha másik kapcsolat ír a forrásba a mentés közben (újraindítás, kivétel ugyanazon kapcsolatra, teljesítmény-következmények, végtelen újraindítás kockázata). Ezzel szemben a `lang_vacuum.html` a `VACUUM INTO`-ra vonatkozóan **egyetlen, tömör mondatban** intézi el a pillanatkép-kérdést, és **nem tér ki** arra, mi történik párhuzamos írás esetén (újraindul-e a másolás, hibázik-e, vagy egyszerűen a `BEGIN`-kor rögzített olvasási pillanatképet másolja tovább — ez utóbbi a forráskódból [`sqlite3BtreeBeginTrans(pMain, pOut==0 ? 2 : 0, 0)`, azaz `VACUUM INTO`-nál sima olvasási tranzakció] következtethető ki, de a dokumentáció ezt nem mondja ki).

**Ítélet: IGAZOLVA a pillanatkép-állítás (röviden dokumentált), CÁFOLVA az az elvárás, hogy a két oldal hasonló mélységben tárgyalná a témát** — a `backup.html` explicit és részletes, a `lang_vacuum.html` erről a részről **hallgat**.

---

## 7. `VACUUM INTO` és a törölt tartalom / `secure_delete`

**URL:** https://www.sqlite.org/lang_vacuum.html

**Szó szerinti idézet:**

> "The advantage of using VACUUM INTO is that the resulting backup database is minimal in size and hence the amount of filesystem I/O may be reduced. Also, all deleted content is purged from the backup, leaving behind no forensic traces."

Ugyanez a lap, a `VACUUM` általános indoklásánál, még korábban:

> "Running VACUUM will clean the database of all traces of deleted content, thus preventing an adversary from recovering deleted content. Using VACUUM in this way is an alternative to setting PRAGMA secure_delete=ON."

**URL:** https://www.sqlite.org/pragma.html#pragma_secure_delete

**Szó szerinti idézet:**

> "When secure_delete is on, SQLite overwrites deleted content with zeros. […] Applications that wish to avoid leaving forensic traces after content is deleted or updated should enable the secure_delete pragma prior to performing the delete or update, or else run VACUUM after the delete or update."

**Ítélet: IGAZOLVA, szó szerint.** A hivatalos dokumentáció kifejezetten kimondja, hogy a `VACUUM INTO` kimenete **nem tartalmazza** a törölt tartalom maradványait ("no forensic traces"), és ezt egyenrangú alternatívaként állítja a `PRAGMA secure_delete=ON` mellé.

---

## Amit nem sikerült ellenőrizni

- **A "félkész célfájl megmarad-e a lemezen" kérdés (5c)** — a hivatalos dokumentáció nem tér ki erre explicit módon, és a forráskód gyors átvizsgálása sem talált egyértelmű "cleanup on error" lépést a `VACUUM INTO` hibaágán (a `goto end_of_vacuum` egy közös hibakezelő útra ugrik, amely nem törli explicit a részlegesen írt kimeneti fájlt) — ez utóbbi állítást azonban **nem tekintem véglegesen igazoltnak**, mert nem futtattam le a teljes hibakezelő ág lépésről lépésre történő nyomkövetését (pl. nem ellenőriztem, hogy az `ATTACH`-hoz tartozó `DETACH`/`sqlite3BtreeClose` valamilyen implicit törlést végez-e sikertelen `VACUUM INTO` esetén). Ez egy tisztán forráskód-alapú, nem dokumentált kérdés — a hivatalos próza-dokumentáció erről **hallgat**.
- **A `VACUUM INTO` konkrét viselkedése párhuzamos író esetén** (újraindul-e, hibázik-e, vagy csendben a régi pillanatképet másolja) — ezt a forráskód (`sqlite3BtreeBeginTrans` olvasási tranzakcióként) valószínűsíti, de **nincs hivatalos próza-dokumentáció**, amely ezt kimondaná; méréssel (pl. tényleges konkurens írás közbeni `VACUUM INTO` futtatásával) lehetett volna közvetlenül tesztelni, de ez az ellenőrzés a dokumentáció/forráskód-szintre korlátozódott, élő adatbázis-teszt nélkül.
- **`SQLITE_DEFAULT_WAL_AUTOCHECKPOINT` fordítás-idejű módosításának tényleges elterjedtsége** disztribúciónként (pl. Debian/Ubuntu csomagolt SQLite-ja módosítja-e) — ezt nem vizsgáltam, mert az eredeti állítás csak a hivatalos alapértékre kérdezett rá.
- Nem volt szükség T3 (StackOverflow stb.) forrásra egyik állításnál sem — minden kérdés megválaszolható volt elsődleges forrásból (sqlite.org dokumentáció vagy a hivatalos forráskód-tükör).

---
