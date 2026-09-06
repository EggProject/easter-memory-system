# Kutatási terv — router és keresési rangsor

Dátum: 2026-09-01 · Vezető: Opus (fő szál) · Keresők: Sonnet

## A kutatási kérdés

Egy markdown-alapú, projekt-szintű agent-memóriarendszert tervezünk. Egy cég egy telepített
szervert használ; a projektek alapból nem látják egymást, de **összeköthetők**. Két
tervezési ötletet kell validálni:

**(1) ROUTER.** Ha A és B projekt össze van kötve, és A-ba új tudás kerül, amiből "valami
hasznos", akkor a rendszer azt **automatikusan** írja bele B-be is. A hasznosság megítélése
egy LLM-re hárulna, emberi jóváhagyás nélkül.

**(2) KERESÉSI RANGSOR.** Ha A projektből keresek, az összekötött B projekt találatai
**kötelezően A találatai után** jöjjenek-e, vagy relevancia szerint keveredhetnek.

A megrendelő maga jelezte a második pontnál: "de lehet hülyeséget mondok, deep-research-vel
validálni kell".

## Explicit hatókörön kívül

- Autentikáció, jogosultság-kikényszerítés, titkosítás. A rendszerben szándékosan nincs
  autentikáció; ez lezárt kérdés, NEM kutatandó.
- Vektoradatbázisok termékösszehasonlítása. A tárolás eldöntött (markdown + SQLite index).
- A beágyazó modell megválasztása.
- Bármi, ami a felület kinézetére vonatkozik.
- Több-bérlős (multi-tenant) izoláció: egy szerver egy céget szolgál, ez nem kérdés.

## Al-kérdések — mind az 1. hullámban, függetlenek

### SQ-01 — Automatikus tudás-propagáció hatókörök között
objective:      Megállapítani, létezik-e működő rendszer, ami LLM ítélete alapján
                automatikusan másol vagy tükröz tudást egyik hatókörből (projekt, munkatér,
                namespace) a másikba; ha igen, pontosan mi a kiváltó feltétel és ki hagyja jóvá.
output_format:  Rendszerenként: a mechanizmus neve, a kiváltó feltétel, van-e jóváhagyás,
                szó szerinti idézet a dokumentációból.
source_hints:   itechmeat/open-second-brain (shared_namespace, mirroring), mem0 multi-scope,
                Zep, Letta sleep-time agents, basic-memory, Notion/Confluence automatizálás,
                Glean, agent-memória arXiv 2025-2026.
boundaries:     Ne a szinkronizálást kutasd (fájlmásolás gépek között), hanem a
                TARTALMI propagációt hatókörök között.

### SQ-02 — A memóriamérgezés és keresztkontamináció dokumentált kárai
objective:      Konkrét, dokumentált eseteket és méréseket találni arra, hogy automatikusan
                továbbterjesztett vagy megmérgezett memória mekkora kárt okoz agent-rendszerekben.
output_format:  Esetenként: mi történt, milyen mechanizmuson át, mekkora hatás számokkal.
source_hints:   OWASP Top 10 for Agentic Applications 2026 (ASI06), arXiv memory poisoning /
                RAG poisoning 2025-2026, CVE-adatbázisok, biztonsági kutatók blogjai
                (Varonis, Wiz, Cymulate), MINJA / AgentPoison típusú támadások.
boundaries:     Ne prompt injectiont általában, hanem kifejezetten a PERZISZTENS memóriába
                jutó és onnan továbbterjedő tartalom kárát.

### SQ-03 — Emberi jóváhagyás a propagációban
objective:      Kideríteni, milyen jóváhagyási mintákat használnak, amikor gépi döntés
                írna egy másik hatókörbe; van-e mérés a jóváhagyás költségéről és hasznáról.
output_format:  Mintánként: mikor kér jóváhagyást, mit lát a jóváhagyó, mi történik, ha nem válaszol.
source_hints:   Letta sleep-time agent review, Anthropic memory tool, GitHub PR-alapú
                automatizálás, Wikipédia bot approval, Dependabot/Renovate, human-in-the-loop
                irodalom (arXiv), Airflow/dbt promóciós minták.
boundaries:     Ne az UI-t kutasd, hanem a folyamat-mintát és a méréseket.

### SQ-04 — Mennyire megbízható egy LLM "ez máshol is hasznos" ítélete
objective:      Mért adatot találni arról, milyen pontosan tud egy LLM eldönteni, hogy egy
                tudásdarab általánosítható-e vagy releváns-e egy másik kontextusban.
output_format:  Mérésenként: feladat, modell, metrika, szám, és hogy mihez képest.
source_hints:   arXiv 2024-2026: relevance judgment with LLMs, LLM-as-a-judge kalibráció,
                cross-domain transfer, knowledge generalization, memory consolidation
                benchmarkok (LongMemEval, LoCoMo, MemoryAgentBench).
boundaries:     Ne az általános LLM-képességet, hanem kifejezetten a RELEVANCIA- és
                ÁTVIHETŐSÉG-ítélet pontosságát.

### SQ-05 — Több forrásból érkező találatok rangsorolása
objective:      Megállapítani, mit csinálnak a valós rendszerek, amikor több hatókörből
                jönnek találatok: merev forrás-sorrend, súlyozás, vagy tiszta relevancia.
                Van-e mérés arról, hogy a merev sorrend mennyit ront a relevancián.
output_format:  Rendszerenként vagy tanulmányonként: a rangsorolási szabály, és ha van, a
                mért hatás számokkal.
source_hints:   federated search irodalom, Elasticsearch cross-cluster search és index boosting,
                Azure AI Search scoring profiles, Vespa rank profiles, Solr, arXiv federated
                / distributed IR, source credibility weighting.
boundaries:     Ne a fúziós algoritmusokat általában (RRF-et már ismerjük), hanem kifejezetten
                a FORRÁS-HATÓKÖR szerinti előnyben részesítést.

### SQ-06 — "Saját + kapcsolt hatókör" keresés a gyakorlatban
objective:      Kideríteni, hogyan mutatja a felhasználónak a saját hatókörén kívülről
                érkező találatokat egy valós termék, és milyen sorrendben.
output_format:  Termékenként: mi a hatókör-fogalom, hogyan jelöli a más hatókörből jövő
                találatot, van-e külön szekció vagy kevert lista.
source_hints:   GitHub cross-repo és org search, Slack cross-channel, Notion teamspaces,
                Linear, Jira cross-project, Confluence cross-space, Glean, Obsidian
                multi-vault, VS Code multi-root workspace search.
boundaries:     Ne a jogosultsági szűrést (azt már kikutattuk), hanem a MEGJELENÍTÉST és
                a SORRENDET.
