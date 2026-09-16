# Linkek — korai-korok-ujra



---

# sq01 — A fa mint jogosultsági modell, és a kategóriák

# Linkek — minden meglátogatott és felderített link (sq01 újramérés)

Ez a fájl a kör egyik fő terméke. Célja: minden URL, amit ez a kutatási kör
meglátogatott (lekért, tartalmát elolvasta) vagy csak felfedezett (egy elsődleges
oldalon linkként felbukkant, de nem lett külön feldolgozva), nyomon követhető
legyen — retrospektív ellenőrizhetőség céljából, mert az előző (2026-08-23-i) kör
pontosan ennek a hiányában okozott problémát.

Módszertani jelölések:
- **WebFetch** = a Claude WebFetch eszközével lekért és összefoglalt tartalom
- **curl (nyers HTML/JSON)** = `curl` a proxy-n keresztül, a nyers választ egy saját
  Python szkript tisztította markdown/szöveggé (lásd 00-plan.md módszertani megjegyzés)
- **PDF+pdftotext** = `curl` a PDF-re, majd `pdftotext -layout`
- **NVD REST API** = `curl https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=...`
  (a hivatalos NVD JSON API; a nvd.nist.gov HTML felülete Cloudflare mögött van,
  sima curl-lal nem elérhető, ezért az API-ra váltottunk)

---

## A) Elsődlegesen feldolgozott, idézetek forrásaként használt oldalak (23 forrás)

| # | Cím | URL | Tier | Alkérdés | Lekérési mód | Megjegyzés |
|---|---|---|---|---|---|---|
| 1 | Memory tool - Claude Platform Docs | https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool | T1 | SQ-01 | WebFetch | Eredetileg docs.claude.com/... címen indult a keresés, az átirányított célt (platform.claude.com) rögzítettük |
| 2 | How Claude remembers your project - Claude Code Docs | https://code.claude.com/docs/en/memory | T1 | SQ-01 | WebFetch | |
| 3 | MCP Tools Reference - Basic Memory | https://docs.basicmemory.com/reference/mcp-tools-reference | T1 | SQ-01 | WebFetch | |
| 4 | Memory blocks (core memory) - Letta Docs | https://docs.letta.com/guides/agents/memory-blocks/ | T1 | SQ-01 | WebFetch | |
| 5 | Custom Categories - Mem0 | https://docs.mem0.ai/platform/features/custom-categories | T1 | SQ-01 | WebFetch | |
| 6 | Graph Namespacing - Zep/Graphiti Documentation | https://help.getzep.com/graphiti/core-concepts/graph-namespacing | T1 | SQ-01 | WebFetch | |
| 7 | Plugin security - Obsidian Help | https://obsidian.md/help/plugin-security | T1 | SQ-01 | WebFetch | |
| 8 | Multi-tenancy - Kubernetes | https://kubernetes.io/docs/concepts/security/multi-tenancy/ | T1 | SQ-02 | curl (nyers HTML) | WebFetch csonkolt kivonatot adott ("Content truncated due to length"), ezért nyers curl + saját HTML→markdown tisztító szkript |
| 9 | Namespace and Secure Multi-Tenancy (SMT) Support in Vault | https://developer.hashicorp.com/vault/docs/enterprise/namespaces | T1 | SQ-02 | WebFetch | |
| 10 | Controlling access to a bucket with user policies - Amazon S3 | https://docs.aws.amazon.com/AmazonS3/latest/userguide/walkthrough1.html | T1 | SQ-02 | WebFetch | |
| 11 | gitignore(5) - Git hivatalos forrás-dokumentáció | https://raw.githubusercontent.com/git/git/master/Documentation/gitignore.adoc | T1 | SQ-03 | curl (raw.githubusercontent.com) | Szándékosan a git/git forráskód-repó raw fájlja, nem a git-scm.com másodlagos renderelt verzió |
| 12 | acl(5) - Linux manual page | https://man7.org/linux/man-pages/man5/acl.5.html | T1 | SQ-03 | curl (nyers HTML) | |
| 13 | Inherited permissions are not automatically updated when you move folders | https://learn.microsoft.com/en-us/troubleshoot/windows-server/windows-security/inherited-permissions-not-automatically-update | T1 | SQ-03 | WebFetch | |
| 14 | The PARA Method - Forte Labs (Tiago Forte) | https://fortelabs.com/blog/para/ | T1 | SQ-04 | WebFetch | A módszer saját eredeti forrása |
| 15 | Introduction - Documentation - Johnny.Decimal | https://johnnydecimal.com/10-19-concepts/11-core/11.01-introduction/ | T1 | SQ-04 | WebFetch | |
| 16 | Why Categories for Your Note Archive are a Bad Idea - Zettelkasten Method | https://zettelkasten.de/posts/no-categories/ | T2 | SQ-04 | WebFetch | Modern Zettelkasten-gyakorlói oldal, nem Luhmann elsődleges írása |
| 17 | On-device query intent prediction with lightweight LLMs... - Scientific Reports | https://www.nature.com/articles/s41598-024-63380-6 | T2 | SQ-05 | WebFetch + curl (ellenőrzés) | Lektorált (Nature Portfolio/Scientific Reports) mérés; a számokat nyers HTML-ből is visszaellenőriztük |
| 18 | From Haystack to Needle: Label Space Reduction for Zero-shot Classification | https://arxiv.org/abs/2502.08436 | T4 | SQ-05 | WebFetch (csak absztrakt) → curl arxiv.org/html/2502.08436v2 (teljes szöveg) | Nem lektorált arXiv preprint |
| 19 | Effective Identifier Names for Comprehension and Memory (Lawrie, Feild, Binkley, ICPC 2007) | https://www.cs.kent.edu/~jmaletic/cs63902/Papers/Lawrie07.pdf | T2 | SQ-06 | curl + pdftotext -layout | Klasszikus, nem LLM-specifikus, lektorált szoftvertechnikai kísérlet |
| 20 | When Names Disappear: Revealing What LLMs Actually Understand About Code | https://arxiv.org/html/2510.03178 | T4 | SQ-06 | curl (nyers HTML, teljes szöveg) | Nem lektorált 2025-ös arXiv preprint |
| 21 | NVD/MITRE CVE adatlapok — CWE-22, CVE-2021-41773, CVE-2024-43093, CVE-2025-54387 | https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2021-41773 (+ cveId=CVE-2024-43093, cveId=CVE-2025-54387) és https://cwe.mitre.org/data/definitions/22.html | T1 | SQ-07 | NVD REST API (curl, JSON) + curl (CWE, nyers HTML) | Egy forrás-azonosító alá gyűjtött köteg; a nvd.nist.gov HTML UI Cloudflare mögött van, ezért REST API-t használtunk |
| 22 | Zip Slip - Snyk canonical vulnerability repository | https://raw.githubusercontent.com/snyk/zip-slip-vulnerability/master/README.md | T1 | SQ-07 | curl (raw.githubusercontent.com) | A sebezhetőségi osztály elsődleges (felfedező) forrása |
| 23 | node-tar (npm tar) CVE-család — NVD hivatalos leírások (CVE-2021-32803/32804/37701/37712/37713) | https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2021-37701 (+ cveId=CVE-2021-32803, cveId=CVE-2021-32804, cveId=CVE-2021-37712, cveId=CVE-2021-37713) | T1 | SQ-07 | NVD REST API (curl, JSON ×5) | Egyetlen npm csomag 5 összefüggő CVE-je, mind a 4 kért hibaosztályt lefedi |

**Tier-eloszlás:** 17× T1, 4× T2, 2× T4. Minden URL élőnek (LIVE, HTTP 200) lett
minősítve a `check_links.py` szkripttel 2026-09-15-én (lásd `04-citations/link-health.jsonl`).

---

## B) Meglátogatott, de idézetként végül fel nem használt oldalak

Ezeket ténylegesen lekértük (WebFetch vagy curl), de a tartalmuk nem került be
állításba — vagy mert redirect/duplikátum volt, vagy mert a keresett konkrét adatot
nem tartalmazták.

| URL | Alkérdés | Miért nem lett önálló forrás |
|---|---|---|
| https://docs.letta.com/guides/agents/multi-agent-shared-memory/ | SQ-01 | A megosztott memória mechanizmusát írja le, de nem ad hozzá új információt az útvonal/jogosultsági modellhez a memory-blocks oldalhoz képest |
| https://docs.aws.amazon.com/AmazonS3/latest/userguide/amazon-s3-policy-keys.html | SQ-02 | A `${aws:username}` policy-változó konkrét példáját kerestük ezen az oldalon, nem találtuk meg ilyen formában — ld. `hianyok.md` |
| https://johnnydecimal.com/documentation/areas-and-categories | SQ-04 | Régi/átirányított URL; a tartalom a végül idézett `11.01-introduction` oldalon található meg |
| https://zettelkasten.de/posts/luhmann-folgezettel-truth/ | SQ-04 | Luhmann Folgezettel-rendszeréről szól, nem a kategória-kérdésről; nem releváns az SQ-04-hez |
| https://github.com/unjs/ipx/security/advisories/GHSA-mm3p-j368-7jcr | SQ-07 | A CVE-2025-54387-hez kiegészítő technikai részletet (a "public123" PoC-ot) adta, ezt a `cve-path-security.md` munkafájlban rögzítettük leíró jelleggel, de a mechanikusan ellenőrzött `allitasok.csv` idézet a hivatalos NVD-szövegből származik, nem erről az oldalról |

---

## C) Felfedezett, de meg nem nyitott linkek

Ezek az elsődleges (A) forrásokban szereplő kimenő linkek, amelyeket a
`log_link.py` regisztrált, de a kutatás nem nyitott meg és nem dolgozott fel
(mert a linkszöveg vagy kontextus alapján nem tűntek relevánsnak a 7
alkérdés egyikéhez sem, vagy másodlagos/adminisztratív tartalomra mutattak).

| URL | Honnan (forrás) | Horgonyszöveg | Alkérdés |
|---|---|---|---|
| https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | Anthropic memory tool docs | "Effective context engineering" | SQ-01 |
| https://forms.gle/YXC2EKGMhjN1c4L88 | Anthropic memory tool docs | "feedback form" | SQ-01 |
| https://platform.claude.com/docs/en/manage-claude/api-and-data-retention | Anthropic memory tool docs | "API and data retention" | SQ-01 |
| https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls | Anthropic memory tool docs | "Handle tool calls" | SQ-01 |
| https://platform.claude.com/docs/en/agents-and-tools/tool-use/text-editor-tool#handle-errors | Anthropic memory tool docs | "text editor tool" | SQ-01 |
| https://platform.claude.com/docs/en/build-with-claude/context-editing | Anthropic memory tool docs | "Context editing" | SQ-01 |
| https://docs.letta.com/v1-sdk/memory/shared-memory | Letta memory-blocks docs | "shared memory blocks" | SQ-01 |
| https://docs.letta.com/api/resources/blocks/methods/retrieve | Letta memory-blocks docs | "blocks retrieve" | SQ-01 |
| https://docs.letta.com/v1-sdk/memory/memory-blocks | Letta memory-blocks docs | "memory blocks" | SQ-01 |
| https://docs.obsidian.md/Developer+policies | Obsidian plugin security docs | "Obsidian Developer Policies" | SQ-01 |
| https://community.obsidian.md | Obsidian plugin security docs | "plugin directory" | SQ-01 |
| https://github.com/kubernetes/website/issues/new?title=Issue%20with%20k8s.io | Kubernetes multi-tenancy docs | "report a problem" | SQ-02 |
| https://github.com/kubernetes/website/issues/new?title=Improvement%20for%20k8s.io | Kubernetes multi-tenancy docs | "suggest an improvement" | SQ-02 |
| https://git-scm.com/docs/gitignore | git gitignore.adoc (raw) | (másodlagos renderelt verzió) | SQ-03 |
| https://arxiv.org/html/2502.08436v2 | Haystack-to-Needle arXiv absztrakt | (a teljes szöveg saját maga — végül ezt is felhasználtuk, ld. A) táblázat) | SQ-05 |
| https://cwe.mitre.org/data/definitions/22.html | NVD CVE-bundle forrás | (a CWE-22 definíció — végül ezt is felhasználtuk, ld. A) táblázat) | SQ-07 |

Megjegyzés: az utolsó két sor (arxiv html v2, cwe.mitre.org) technikailag már
"meg lett nyitva" és fel is lett használva — a `log_link.py` `not_opened`
állapotban rögzítette őket, mert a linket egy másik oldalon fedeztük fel, de
a tényleges feldolgozás egy külön `curl` hívással történt. Az A) táblázat ezt a
tényleges felhasználást mutatja.



---

# sq02 — A markdown fájl mint memória-egység, és a fejléc

# Linkek — sq02

Minden meglétező, meglátogatott és felderített link. A "Lekérés módja" oszlop jelöli, hogy a tartalmat **curl (nyers, a proxyn keresztül)**, **WebFetch** (kis modellel feldolgozott összefoglaló/rendered szöveg) vagy **WebSearch** (csak találati lista, nem nyitva) útján szereztük-e meg. A specifikációk és a hivatalos parser-dokumentációk esetén — a feladat kikötése szerint — mindenütt **curl nyerset** használtunk, WebFetch-et sehol nem vetettünk be ténylegesen erre a körre (a WebFetch tool elérhető volt, de minden ténylegesen felhasznált fő forrást curl-lel kérdeztünk le, ahol ez technikailag lehetséges volt; ahol curl nem hozott érdemi tartalmat — pl. JS-rendered oldalak —, ott a GitHub-alapú nyers markdown/forráskód-változatot kerestük meg helyette, nem WebFetch-et).

## 1. Elsődleges specifikációk és forráskód (T1, curl nyers)

| Cím | URL | Tier | Lekérés módja | Státusz |
|---|---|---|---|---|
| YAML Ain't Markup Language (YAML™) Version 1.1 (Final Draft, 2005-01-18) | https://yaml.org/spec/1.1/ | T1 | curl nyers | 200 |
| YAML 1.1 Type Repository — Boolean | https://yaml.org/type/bool.html | T1 | curl nyers | 200 |
| YAML Ain't Markup Language (YAML™) Version 1.2.2 | https://yaml.org/spec/1.2.2/ | T1 | curl nyers | 200 |
| TOML spec, main branch | https://raw.githubusercontent.com/toml-lang/toml/main/toml.md | T1 | curl nyers (raw.githubusercontent.com) | 200 |
| TOML spec, v1.0.0 tag (elsődlegesen ezt idéztük) | https://raw.githubusercontent.com/toml-lang/toml/1.0.0/toml.md | T1 | curl nyers | 200 |
| PyYAML `resolver.py` forráskód (main ág) | https://raw.githubusercontent.com/yaml/pyyaml/main/lib/yaml/resolver.py | T1 | curl nyers | 200 |
| PyYAML `README.md` | https://raw.githubusercontent.com/yaml/pyyaml/main/README.md | T1 | curl nyers | 200 |
| PyYAML `CHANGES` | https://raw.githubusercontent.com/yaml/pyyaml/main/CHANGES | T1 | curl nyers | 200 |
| PyYAML hivatalos wiki-dokumentáció | https://pyyaml.org/wiki/PyYAMLDocumentation | T1 | curl nyers | 200 (nem tartalmazott releváns verzió-állítást) |
| PyYAML csomagleírás (PyPI JSON API) | https://pypi.org/pypi/PyYAML/json | T1 | curl nyers (JSON API) | 200 |
| SnakeYAML `Resolver.java` forráskód | https://raw.githubusercontent.com/snakeyaml/snakeyaml/master/src/main/java/org/yaml/snakeyaml/resolver/Resolver.java | T1 | curl nyers | 200 |
| SnakeYAML `README.md` | https://raw.githubusercontent.com/snakeyaml/snakeyaml/master/README.md | T1 | curl nyers | 200 |
| js-yaml `README.md` | https://raw.githubusercontent.com/nodeca/js-yaml/master/README.md | T1 | curl nyers | 200 |
| js-yaml `lib/type/bool.js` (v4.3.2, unpkg tükrözi az npm csomagot) | https://unpkg.com/js-yaml@4.3.2/lib/type/bool.js | T1 | curl nyers (-L, unpkg CDN) | 200 |
| js-yaml `lib/schema/core.js` (v4.3.2) | https://unpkg.com/js-yaml@4.3.2/lib/schema/core.js | T1 | curl nyers (-L) | 200 |
| js-yaml `lib/schema/default.js` (v4.3.2) | https://unpkg.com/js-yaml@4.3.2/lib/schema/default.js | T1 | curl nyers (-L) | 200 |
| ruamel.yaml csomagleírás (PyPI JSON API, = README) | https://pypi.org/pypi/ruamel.yaml/json | T1 | curl nyers (JSON API) | 200 |
| ruamel.yaml hivatalos dokumentáció — Overview | https://yaml.dev/doc/ruamel.yaml/ | T1 | curl nyers | 200 |
| ruamel.yaml hivatalos dokumentáció — Basic Usage | https://yaml.dev/doc/ruamel.yaml/basicuse/ | T1 | curl nyers | 200 |
| ruamel.yaml hivatalos dokumentáció — Details (round-trip) | https://yaml.dev/doc/ruamel.yaml/detail/ | T1 | curl nyers | 200 |
| ruamel.yaml hivatalos dokumentáció — Differences with PyYAML | https://yaml.dev/doc/ruamel.yaml/pyyaml/ | T1 | curl nyers | 200 |
| tomlkit `README.md` | https://raw.githubusercontent.com/python-poetry/tomlkit/master/README.md | T1 | curl nyers | 200 |
| tomlkit `README.rst` (elavult elérési út, próba) | https://raw.githubusercontent.com/python-poetry/tomlkit/master/README.rst | T1 | curl nyers | 404 |

## 2. Memória-rendszerek hivatalos dokumentációja / forráskódja (T1)

| Cím | URL | Tier | Lekérés módja | Státusz |
|---|---|---|---|---|
| Basic Memory — Technical Information | https://docs.basicmemory.com/reference/technical-information | T1 | curl nyers (SSR-elt Mintlify oldal) | 200 |
| Basic Memory `README.md` | https://raw.githubusercontent.com/basicmachines-co/basic-memory/main/README.md | T1 | curl nyers | 200 |
| Mem0 — Graph Memory doksi | https://docs.mem0.ai/platform/features/graph-memory | T1 | curl nyers | 200 |
| Mem0 — Vector Databases Overview | https://docs.mem0.ai/components/vectordbs/overview | T1 | curl nyers | 200 |
| Mem0 `README.md` | https://raw.githubusercontent.com/mem0ai/mem0/main/README.md | T1 | curl nyers | 200 |
| Mem0 — "How Mem0 Works" (rossz URL-találgatás) | https://docs.mem0.ai/core-concepts/how-mem0-works | T1 | curl nyers | 404 |
| Graphiti `README.md` (getzep/graphiti) | https://raw.githubusercontent.com/getzep/graphiti/main/README.md | T1 | curl nyers | 200 |
| Zep — arXiv absztrakt oldal (2501.13956) | https://arxiv.org/abs/2501.13956 | T4 (preprint, gyártói önjelentés) | curl nyers | 200 |
| Letta — Archival memory doksi | https://docs.letta.com/guides/core-concepts/memory/archival-memory | T1 | curl nyers (-L, redirect követve) | 200 (redirect: 308→200) |
| Anthropic — Memory tool hivatalos doksi | https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool | T1 | curl nyers (-L) | 200 (redirect: 302→200) |
| Anthropic — Memory tool (alternatív domain, nem nyitva külön) | https://docs.claude.com/en/docs/agents-and-tools/tool-use/memory-tool | T1 | — | 302 (ugyanoda mutat, mint fent) |
| Claude Code — "How Claude remembers your project" | https://code.claude.com/docs/en/memory | T1 | curl nyers | 200 |
| Obsidian súgó — Properties (help.obsidian.md, JS-app-shell, tartalom nélkül) | https://help.obsidian.md/Editing+and+formatting/Properties | T1 | curl nyers | 200 (üres app-shell, nem használható) |
| Obsidian súgó forrása — Properties.md (GitHub, ez a ténylegesen idézett verzió) | https://raw.githubusercontent.com/obsidianmd/obsidian-help/master/en/Editing%20and%20formatting/Properties.md | T1 | curl nyers | 200 |
| Obsidian súgó forrása — Property types.md (próba) | https://raw.githubusercontent.com/obsidianmd/obsidian-help/master/en/Editing%20and%20formatting/Property%20types.md | T1 | curl nyers | 404 |
| Obsidian súgó forrása — Plugins/Bases.md (próba) | https://raw.githubusercontent.com/obsidianmd/obsidian-help/master/en/Plugins/Bases.md | T1 | curl nyers | 404 |
| Obsidian súgó forrása — Search.md (próba) | https://raw.githubusercontent.com/obsidianmd/obsidian-help/master/en/Plugins/Core%20plugins/Search.md | T1 | curl nyers | 404 |
| Obsidian súgó forrása — Graph view.md (próba) | https://raw.githubusercontent.com/obsidianmd/obsidian-help/master/en/Plugins/Core%20plugins/Graph%20view.md | T1 | curl nyers | 404 |
| Jekyll — Front Matter hivatalos doksi | https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/front-matter.md | T1 | curl nyers | 200 |
| Hugo — Front matter hivatalos doksi | https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/content-management/front-matter.md | T1 | curl nyers | 200 |
| Notion — Export your content (hivatalos súgó) | https://www.notion.com/help/export-your-content | T1 | curl nyers (-L) | 200 (nem részletezi a cím elhelyezését) |

## 3. Tudományos / lektorált forrás (T2)

| Cím | URL | Tier | Lekérés módja | Státusz |
|---|---|---|---|---|
| Dense X Retrieval — arXiv absztrakt | https://arxiv.org/abs/2312.06648 | T2 (lektorált, ld. ACL Anthology) | curl nyers | 200 |
| Dense X Retrieval — teljes szöveg (arXiv HTML, v2) | https://arxiv.org/html/2312.06648v2 | T2 | curl nyers | 200 |
| Dense X Retrieval — ACL Anthology hivatalos bejegyzés (EMNLP 2024 main, 2024.emnlp-main.845) | https://aclanthology.org/2024.emnlp-main.845/ | T1/T2 | curl nyers | 200 |

## 4. Másodlagos / blog / közösségi (T3)

| Cím | URL | Tier | Lekérés módja | Státusz |
|---|---|---|---|---|
| Bram.us — "YAML: The Norway Problem" (2022-01-11) | https://www.bram.us/2022/01/11/yaml-the-norway-problem/ | T3 | curl nyers | 200 |
| HitchDev / StrictYAML — "The Norway Problem - why StrictYAML refuses to do implicit typing" | https://hitchdev.com/strictyaml/why/implicit-typing-removed/ | T3 | curl nyers | 200 |
| HitchDev / StrictYAML — "What is wrong with TOML?" | https://hitchdev.com/strictyaml/why-not/toml/ | T3 | curl nyers | 200 |
| SSW.com.au — "Best practices for Frontmatter in markdown" | https://www.ssw.com.au/rules/best-practices-for-frontmatter-in-markdown | T3 | curl nyers | 200 |

## 5. Felderített, de nem (vagy csak találati listaként) megnyitott linkek — leadek további körhöz

Ezek a WebSearch találati listáiban jelentek meg; relevánsnak tűntek, de idő/keret hiányában nem nyitottuk meg elsődleges forrásként ebben a körben. További kutatáshoz ajánlott kiindulópontok.

| Cím | URL | Miért releváns | Alkérdés |
|---|---|---|---|
| StrictYAML GitHub issue #186 — "Website fails to acknowledge that the Norway problem was fixed in YAML 1.2" | https://github.com/crdoconnor/strictyaml/issues/186 | közvetlen vita a spec-változásról | SQ-04 |
| noyaml.com / yamltokyaml.com — "What is the Norway Bug?" | https://yamltokyaml.com/en/docs/norway-bug | további népszerűsítő anyag, esetleg korábbi datálás | SQ-04 |
| Posit Open Source — "In Defense of YAML" | https://opensource.posit.co/blog/2026-05-21_in-defense-of-yaml/ | ellenvélemény a YAML-kritikákkal szemben | SQ-04 / SQ-05 |
| Neo4j blog — "Graphiti: Knowledge graph memory for an agentic world" | https://neo4j.com/blog/developer/graphiti-knowledge-graph-memory/ | Neo4j saját (T4) leírása a Graphiti-integrációról | SQ-01 |
| EmergentMind — Zep topic-összefoglaló | https://www.emergentmind.com/topics/zep-a-temporal-knowledge-graph-architecture | másodlagos összefoglaló, nem elsődleges | SQ-01 |
| TheMoonlight.io — Zep irodalmi áttekintés | https://www.themoonlight.io/en/review/zep-a-temporal-knowledge-graph-architecture-for-agent-memory | független(nek tűnő) értékelés a Zep-papírról | SQ-01 |
| Weaviate — "Dense X Retrieval" paper-összefoglaló | https://weaviate.io/papers/paper10 | gyártói összefoglaló egy független, lektorált papírról (maga a szám T2, az összefoglaló T4) | SQ-02 |
| chentong0.github.io/factoid-wiki | https://chentong0.github.io/factoid-wiki/ | a Dense X Retrieval szerzőjének projektoldala, adatkészlet | SQ-02 |
| Zettlr — YAML Front Matter hivatalos doksi | https://docs.zettlr.com/en/editor/yaml-frontmatter.html | Zettlr saját frontmatter-mezői — nem dolgoztuk fel elsődleges forrásból | SQ-03 |
| Dendron — Frontmatter wiki-oldal | https://wiki.dendron.so/notes/ffec2853-c0e0-4165-a368-339db12c8e4b/ | Dendron saját frontmatter-mezői — nem dolgoztuk fel elsődleges forrásból | SQ-03 |
| Zettelkasten fórum — "on the use of YAML and its relation to wikilinks" | https://forum.zettelkasten.de/discussion/3255/ | gyakorlati vélemények YAML-ról jegyzetelésben | SQ-03/SQ-04 |
| GitHub dendronhq/dendron issue #160 — "Store metadata without using frontmatter" | https://github.com/dendronhq/dendron/issues/160 | vita a frontmatter alternatíváiról | SQ-03 |
| MyST Markdown — "Content frontmatter options" | https://mystmd.org/guide/frontmatter | egy további frontmatter-séma-referencia | SQ-03 |
| Milvus blog — "Claude Code Memory System Explained" | https://milvus.io/blog/claude-code-memory-memsearch.md | harmadik fél (vektor-DB gyártó) értelmezése a Claude Code memóriájáról — vektoros/kereshető réteget javasol hozzáadni, de ez NEM a hivatalos Claude Code viselkedés | SQ-01 |

## Módszertani megjegyzés a `<pre>`/kódblokk idézetekről

Néhány T1 forrás (pl. `yaml.org/type/bool.html` regex-blokkja) a HTML-ben sortöréssel tördelt `<pre>` blokkban van. Az `allitasok.csv`-ben ezeknél a sortöréseket szóközzé normalizáltuk az olvashatóság kedvéért; a pontos, sortörésekkel együtt látható eredeti az URL-en közvetlenül ellenőrizhető. Ahol ez történt, a `allitasok.csv` megfelelő sorában jelöltük.



---

# sq03 — Beágyazás magyarra/többnyelvűre, és az integrációs felületek

# Linkek — sq03 (beágyazás, vektorkeresés, SQLite, integrációs felületek)

Minden meglátogatott/felderített link. **Lekérés módja**: `curl` = nyers HTML/Markdown/JSON letöltés a proxyn keresztül; `WebFetch` = összefoglaló kis modellen keresztül (jelölve, mert ez az utasítás szerint gyengébb bizonyíték); `WebSearch` = csak találati lista, nem tartalom; `API` = strukturált API-hívás (pl. Hugging Face API, Semantic Scholar API); `belső` = a kampány saját, korábbi munkájából származó fájl, nem web.

Lekérés dátuma (minden `curl`/`WebFetch`/`API` sorra): **2026-09-15**.

## SQ1 — Magyar/többnyelvű embedding benchmarkok

| Cím | URL | Tier | Lekérés módja |
|---|---|---|---|
| MMTEB: Massive Multilingual Text Embedding Benchmark (arXiv HTML, v3) | https://arxiv.org/html/2502.13595v3 | T1 | curl |
| MMTEB arXiv absztrakt oldal | https://arxiv.org/abs/2502.13595 | T1 | WebSearch (csak találat) |
| MTEB Leaderboard (Hugging Face Space) | https://huggingface.co/spaces/mteb/leaderboard | T1 | WebSearch (csak találat) |
| mteb/leaderboard Space fájlfa (main) | https://huggingface.co/api/spaces/mteb/leaderboard/tree/main | T1 | API (curl) |
| mteb GitHub repó | https://github.com/embeddings-benchmark/mteb/ | T1 | WebSearch (csak találat, nem nyitva) |
| HunSum2AbstractiveRetrieval dataset README | https://huggingface.co/datasets/mteb/HunSum2AbstractiveRetrieval/raw/main/README.md | T1 | curl |
| Hugging Face dataset-keresés API (mteb + "Hun") | https://huggingface.co/api/datasets?search=Hun&author=mteb&limit=100 | T1 | API (curl) |
| WikipediaRetrievalMultilingual dataset API-metaadat | https://huggingface.co/api/datasets/mteb/WikipediaRetrievalMultilingual | T1 | API (curl) |
| mteb/results dataset API-metaadat | https://huggingface.co/api/datasets/mteb/results | T1 | API (curl) |
| mteb/results dataset README | https://huggingface.co/datasets/mteb/results/raw/main/README.md | T1 | curl |
| mteb/results parquet adatfájlok (4 shard, ~299 MB) | https://huggingface.co/datasets/mteb/results/resolve/main/data/train-0000{0..3}-of-00004.parquet | T1 | curl (letöltés + saját DuckDB-lekérdezés) |
| Egyedi eredményfájl: multilingual-e5-large-instruct / HunSum2AbstractiveRetrieval | https://raw.githubusercontent.com/embeddings-benchmark/results/main/results/intfloat__multilingual-e5-large-instruct/baa7be480a7de1539afce709c8f13f833a510e0a/HunSum2AbstractiveRetrieval.json | T1 | curl |
| Training Embedding Models for Hungarian (Hatvani & Yang, IEEE CITDS 2024) | https://real.mtak.hu/207276/1/86-91.pdf | T1 | curl (PDF letöltés + szövegkinyerés) |

## SQ2 — Többnyelvű vs egynyelvű mérés

| Cím | URL | Tier | Lekérés módja |
|---|---|---|---|
| Evaluation of Embedding Models for Hungarian QA Retrieval (Antal Margit, Infocommunications Journal 2025/4) — repó oldal | https://real.mtak.hu/232825/ | T1 | curl |
| Ugyanaz, teljes PDF | https://real.mtak.hu/232825/1/InfocomJournal_2025_4_1.pdf | T1 | curl (PDF letöltés + szövegkinyerés) |
| Multilingual E5 Text Embeddings: A Technical Report (arXiv, v1) — ellenőrizve, nem tartalmaz monolingual-összevetést | https://arxiv.org/html/2402.05672v1 | T1 | curl |
| Training Embedding Models for Hungarian (ld. fent, kettős felhasználás SQ1+SQ2) | https://real.mtak.hu/207276/1/86-91.pdf | T1 | curl |

## SQ3 — Brute-force vs. közelítő vektorkeresés, bináris kvantálás

| Cím | URL | Tier | Lekérés módja |
|---|---|---|---|
| sqlite-vec — Binary Quantization guide (nyers md) | https://raw.githubusercontent.com/asg017/sqlite-vec/main/site/guides/binary-quant.md | T1 | curl |
| sqlite-vec — Scalar Quantization guide (nyers md) | https://raw.githubusercontent.com/asg017/sqlite-vec/main/site/guides/scalar-quant.md | T1 | curl |
| sqlite-vec — Performance guide (nyers md, üres vázlat) | https://raw.githubusercontent.com/asg017/sqlite-vec/main/site/guides/performance.md | T1 | curl |
| pgvector README (GitHub raw) | https://raw.githubusercontent.com/pgvector/pgvector/master/README.md | T1 | curl |
| FAISS wiki — Guidelines to choose an index | https://raw.githubusercontent.com/wiki/facebookresearch/faiss/Guidelines-to-choose-an-index.md | T1 | curl |
| Qdrant — Optimizing High-Dimensional Vectors with Binary Quantization (hivatalos technikai cikk) | https://qdrant.tech/articles/binary-quantization/index.md | T2 | curl |
| Scaling Vector Search: Flat vs HNSW vs HNSW+PQ (Substack blog) | https://datashot.substack.com/p/scaling-vector-search-flat-vs-hnsw | T3 | curl |
| "500000 vectors in under 500ms in sqlite (brute force)" (YouTube Short, nem nyitva, csak találat) | https://www.youtube.com/shorts/Xs7uZ60xBmM | T3 | WebSearch (nem nyitva, tartalom nem ellenőrzött) |

## SQ4 — SQLite mint vektortár (sqlite-vec)

| Cím | URL | Tier | Lekérés módja |
|---|---|---|---|
| sqlite-vec főoldal | https://alexgarcia.xyz/sqlite-vec/ | T1 | curl |
| sqlite-vec — vec0 Virtual Tables (features) | https://alexgarcia.xyz/sqlite-vec/features/vec0.html | T1 | curl |
| sqlite-vec README (GitHub raw) | https://raw.githubusercontent.com/asg017/sqlite-vec/main/README.md | T1 | curl |
| sqlite-vec — Installation guide (nyers md) | https://raw.githubusercontent.com/asg017/sqlite-vec/main/site/getting-started/installation.md | T1 | curl |
| sqlite-vec — Python integráció (nyers md) | https://raw.githubusercontent.com/asg017/sqlite-vec/main/site/using/python.md | T1 | curl |
| sqlite-vec — Node/Deno/Bun integráció (nyers md) | https://raw.githubusercontent.com/asg017/sqlite-vec/main/site/using/js.md | T1 | curl |
| SQLite hivatalos — Runtime Loadable Extensions | https://www.sqlite.org/loadext.html | T1 | curl |

## SQ5 — FTS5 és magyar tövezés

| Cím | URL | Tier | Lekérés módja |
|---|---|---|---|
| SQLite hivatalos FTS5 dokumentáció | https://sqlite.org/fts5.html | T1 | curl |
| fts5-snowball (harmadik féltől, GitHub) | https://github.com/abiliojr/fts5-snowball | T2 | WebSearch (nem nyitva) |
| Snowball projekt főoldal | https://snowballstem.org/ | T1 | curl |
| Snowball — magyar tövező algoritmus oldala | https://snowballstem.org/algorithms/hungarian/stemmer.html | T1 | curl |
| "Four Stemmers and a Funeral: Stemming in Hungarian at CLEF 2005" — Springer oldal (fizetőfal) | https://link.springer.com/chapter/10.1007/11878773_20 | T1 | WebSearch (csak találat, tartalom fizetőfal mögött) |
| Ugyanaz — ResearchGate (403, blokkolva) | https://www.researchgate.net/publication/221160352_Four_Stemmers_and_a_Funeral_Stemming_in_Hungarian_at_CLEF_2005 | T1 | curl (403 Temporarily Unavailable) |
| Ugyanaz — szerzői forrásoldal (ILPS, UvA) — halott link | http://ilps.science.uva.nl/resources/snowball-hun/ | T1 | curl (DNS-hiba, nem elérhető) |
| Semantic Scholar API — a tanulmány metaadata (absztrakt nélkül) | https://api.semanticscholar.org/graph/v1/paper/search?query=Four+Stemmers+and+a+Funeral+Hungarian | T1 | API (curl) |

## SQ6 — Kliensenkénti hook méret-limit

| Cím | URL | Tier | Lekérés módja |
|---|---|---|---|
| Claude Code — Hooks reference (hivatalos, élő) | https://code.claude.com/docs/en/hooks | T1 | curl |
| Claude Code CHANGELOG.md (GitHub raw) | https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md | T1 | curl |
| GitHub issue anthropics/claude-code #44086 (SessionStart hook truncation) | https://github.com/anthropics/claude-code/issues/44086 | T2 | **WebFetch (összefoglaló, nem nyers)** — a nyers `curl` a proxy github.com-specifikus API-korlátozásába ütközött |
| Gemini CLI — hooks/reference.md (GitHub raw) | https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/hooks/reference.md | T1 | curl |
| Gemini CLI — hooks/index.md (GitHub raw) | https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/hooks/index.md | T1 | curl |
| Gemini CLI — hooks/writing-hooks.md (GitHub raw) | https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/hooks/writing-hooks.md | T1 | curl |
| Cursor — Hooks (hivatalos) | https://cursor.com/docs/hooks | T1 | curl |
| Cursor — Rules (hivatalos, ellenőrizve, nincs releváns méret-limit) | https://cursor.com/docs/rules | T1 | curl |
| Cursor — CLI Using (hivatalos, ellenőrizve) | https://cursor.com/docs/cli/using | T1 | curl |
| Codex — Hooks (hivatalos, developers.openai.com) | https://developers.openai.com/codex/hooks | T1 | curl |
| Codex — Advanced Config (hivatalos) | https://developers.openai.com/codex/config-advanced | T1 | curl |
| Codex — Config Reference (hivatalos, ellenőrizve) | https://developers.openai.com/codex/config-reference | T1 | curl |
| Codex CLI repo — docs/config.md (GitHub raw) | https://raw.githubusercontent.com/openai/codex/main/docs/config.md | T1 | curl |

## SQ7 — MCP protokoll és kliens-támogatás

| Cím | URL | Tier | Lekérés módja |
|---|---|---|---|
| MCP specifikáció — Client Features: Sampling | https://modelcontextprotocol.io/specification/2025-06-18/client/sampling | T1 | curl |
| MCP specifikáció — Server Features: Resources | https://modelcontextprotocol.io/specification/2025-06-18/server/resources | T1 | curl |
| MCP specifikáció — Server Features: Prompts | https://modelcontextprotocol.io/specification/2025-06-18/server/prompts | T1 | curl |
| MCP specifikáció — főoldal (2025-06-18) | https://modelcontextprotocol.io/specification/2025-06-18 | T1 | curl |
| Claude Code — Connect to tools via MCP (hivatalos) | https://code.claude.com/docs/en/mcp | T1 | curl |
| Cursor — Model Context Protocol (MCP) (hivatalos) | https://cursor.com/docs/mcp | T1 | curl |
| Gemini CLI — docs/tools/mcp-server.md (GitHub raw) | https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/tools/mcp-server.md | T1 | curl |
| Codex — Model Context Protocol (hivatalos) | https://developers.openai.com/codex/mcp | T1 | curl |
| MCPJam — Claude MCP client oldal (harmadik fél, gyártói/aggregátor) | https://www.mcpjam.com/clients/claude | T2/T3 | curl |
| MCPJam — Cursor MCP client oldal | https://www.mcpjam.com/clients/cursor | T2/T3 | curl |
| caniuse.dev (MCP kliens-mátrix, JS-renderelt SPA, tartalom nem volt kinyerhető) | https://caniuse.dev/ | T3 | curl (üres shell, JS-only) |

## Blokkolt / elérhetetlen források (dokumentálva, nem megkerülve)

| Forrás | Probléma |
|---|---|
| `api.github.com` (bármely repó) | A proxy egy Claude Code GitHub Actions-specifikus hibaüzenetet ad vissza ("sessions are bound to their configured repositories"), nyers GitHub API-hívás nem lehetséges ebben a környezetben. |
| `github.com/search` | Ugyanaz a proxy-korlátozás. |
| `grep.app` | Vercel biztonsági ellenőrző oldal (429/checkpoint), nem adott vissza tartalmat. |
| `web.archive.org`, `archive.org` | A `curl` kapcsolat rendszeresen megszakadt ("Connection reset by peer"), a `WebFetch` pedig `SITE_BLOCKED` hibát adott. Emiatt nem sikerült történeti (2026-09-01 körüli) pillanatképet ellenőrizni a Claude Code hook-dokumentációról — lásd `hianyok.md` és `ellentmondasok.md`. |
| `ilps.science.uva.nl` | DNS-feloldási hiba, a domain valószínűleg megszűnt (kb. 20 éves egyetemi erőforrás-oldal). |
| `researchgate.net` | 403 "Temporarily Unavailable" — bot-védelem. |

## Belső (nem web) források, amelyekre a kutatás hivatkozik

| Fájl | Szerep |
|---|---|
| `/home/claude/work/audit/00-dontesek.html` | A kampány döntési naplója (D-02, D-15, D-16 stb.) — ebből derült ki a D-15/5 pontos szövege és a 2026-09-15-i belső jegyzet. |
| `/home/claude/work/audit/90-meresek.html` | A kampány mérési dokumentuma — ebből derült ki a 05. és 07. szakasz (külső embedding-mérések, illetve a 2026-09-01-i adverzariális ellenőrzés eredménye a hook-limitekről). |
| `/home/claude/work/audit/30-kereses.html` | Spec 30 (keresés és indexelés) — ebből derült ki a "tövező szándékosan hiányzik — magyarra bizonyítottan ront" állítás, aminek nem található alátámasztása. |
| `/home/claude/work/audit/40-mcp.html` | Spec 40 (MCP felület) — megerősíti, hogy a "resource" kiajánlás kérdése még nyitott, és nem tárgyalja a sampling-kérdést (tehát a mostani kutatás új területet fed le). |
