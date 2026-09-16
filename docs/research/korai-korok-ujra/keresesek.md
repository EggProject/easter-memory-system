# Keresések — korai-korok-ujra



---

# sq01 — A fa mint jogosultsági modell, és a kategóriák

# Keresések — minden lefuttatott keresés és lekérés szó szerint (sq01 újramérés)

Ez a fájl a `01-search-log/queries.jsonl` tartalmát rendereli emberi olvasásra.
Összesen **66** rögzített keresési/lekérési művelet, 7 alkérdésre bontva.
A `tool` oszlop jelzi a módszert: `WebSearch` (kulcsszavas keresés), `WebFetch`
(Claude-összefoglalós lekérés) vagy `Bash-curl` (nyers HTML/JSON lekérés a proxy-n
keresztül, saját tisztító szkripttel feldolgozva — ez a módszertan explicit
követelménye volt ennek a körnek).

## SQ-01 — Útvonal mint jogosultsági modell markdown-alapú agent-memória rendszerekben

(17 művelet)

| # | Eszköz | Keresés / URL | Találatok |
|---|---|---|---|
| 1 | WebSearch | basic-memory MCP markdown permissions folder | 7 |
| 2 | WebSearch | Anthropic memory tool context management documentation | 10 |
| 3 | WebSearch | Claude Code memory CLAUDE.md project memory documentation | 8 |
| 4 | WebSearch | Letta memory blocks agent scoped access | 8 |
| 5 | WebSearch | mem0 user_id namespace isolation documentation | 10 |
| 6 | WebSearch | Zep memory graph group_id user isolation docs | 8 |
| 7 | WebSearch | mem0 docs.mem0.ai multi-tenancy categories custom_categories | 8 |
| 8 | WebSearch | obsidian vault security file access permissions plugin sandbox | 10 |
| 9 | WebFetch | https://docs.claude.com/en/docs/agents-and-tools/tool-use/memory-tool -> redirect -> https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool | 1 |
| 10 | WebFetch | https://code.claude.com/docs/en/memory | 1 |
| 11 | WebFetch | https://docs.basicmemory.com/reference/mcp-tools-reference | 1 |
| 12 | WebFetch | https://docs.letta.com/guides/agents/memory-blocks/ | 1 |
| 13 | WebFetch | https://docs.letta.com/guides/agents/multi-agent-shared-memory/ | 1 |
| 14 | WebFetch | https://docs.mem0.ai/platform/features/custom-categories | 1 |
| 15 | WebFetch | https://help.getzep.com/graphiti/core-concepts/graph-namespacing | 1 |
| 16 | WebFetch | https://obsidian.md/help/plugin-security | 1 |
| 17 | WebSearch | mem0 official docs "access control" OR "security" user_id filter enforce application | 7 |

## SQ-02 — Valódi többbérlős izolációs modellek (ellenpont)

(7 művelet)

| # | Eszköz | Keresés / URL | Találatok |
|---|---|---|---|
| 1 | WebSearch | AWS IAM policy S3 prefix condition s3:prefix path-based access control documentation | 9 |
| 2 | WebSearch | Kubernetes namespace RBAC isolation documentation security boundary | 8 |
| 3 | WebSearch | HashiCorp Vault namespaces multi-tenant isolation documentation | 10 |
| 4 | Bash-curl | curl -sS -L https://kubernetes.io/docs/concepts/security/multi-tenancy/ (raw HTML, proxy) | 1 |
| 5 | WebFetch | https://developer.hashicorp.com/vault/docs/enterprise/namespaces | 1 |
| 6 | WebFetch | https://docs.aws.amazon.com/AmazonS3/latest/userguide/walkthrough1.html | 1 |
| 7 | WebFetch | https://docs.aws.amazon.com/AmazonS3/latest/userguide/amazon-s3-policy-keys.html | 1 |

## SQ-03 — Öröklődés a fában (lefelé/felfelé, visszavonhatatlanság)

(5 művelet)

| # | Eszköz | Keresés / URL | Találatok |
|---|---|---|---|
| 1 | Bash-curl | curl raw.githubusercontent.com/git/git/master/Documentation/gitignore.adoc | 1 |
| 2 | WebSearch | Microsoft Learn NTFS inherited permissions parent object propagate documentation | 8 |
| 3 | WebSearch | POSIX ACL default ACL directory inheritance man page setfacl | 10 |
| 4 | Bash-curl | curl man7.org/linux/man-pages/man5/acl.5.html | 1 |
| 5 | WebFetch | https://learn.microsoft.com/en-us/troubleshoot/windows-server/windows-security/inherited-permissions-not-automatically-update | 1 |

## SQ-04 — Kategóriák száma valódi rendszerekben

(9 művelet)

| # | Eszköz | Keresés / URL | Találatok |
|---|---|---|---|
| 1 | WebSearch | PARA method Tiago Forte four categories Projects Areas Resources Archives | 10 |
| 2 | WebSearch | Johnny Decimal ten categories areas official system | 10 |
| 3 | WebSearch | Zettelkasten no categories no hierarchy tags links Luhmann | 9 |
| 4 | WebFetch | https://fortelabs.com/blog/para/ | 1 |
| 5 | WebFetch | https://johnnydecimal.com/documentation/areas-and-categories | 1 |
| 6 | WebFetch | https://zettelkasten.de/posts/luhmann-folgezettel-truth/ | 1 |
| 7 | WebFetch | https://zettelkasten.de/posts/no-categories/ | 1 |
| 8 | WebFetch | https://johnnydecimal.com/10-19-concepts/11-core/11.01-introduction/ | 1 |
| 9 | WebSearch | Obsidian official folders vs tags philosophy "don't need folders" | 8 |

## SQ-05 — Kategóriaszám és besorolási pontosság (lektorált mérések)

(9 művelet)

| # | Eszköz | Keresés / URL | Találatok |
|---|---|---|---|
| 1 | WebSearch | effect of number of classes on LLM classification accuracy label space size | 8 |
| 2 | WebSearch | number of answer choices multiple choice accuracy large language model study | 7 |
| 3 | WebSearch | extreme multi-label classification accuracy degrades number of labels increases | 10 |
| 4 | WebFetch | https://arxiv.org/abs/2502.08436 | 1 |
| 5 | Bash-curl | curl arxiv.org/html/2502.08436v2 (raw HTML full text) | 1 |
| 6 | WebSearch | "number of classes" accuracy small model large model comparison in-context learning study arxiv | 7 |
| 7 | WebSearch | intent classification accuracy decreases as number of intent classes increases small model study | 10 |
| 8 | WebFetch | https://www.nature.com/articles/s41598-024-63380-6 | 1 |
| 9 | Bash-curl | curl nature.com/articles/s41598-024-63380-6 (raw HTML, quote verification) | 1 |

## SQ-06 — Mappanév/azonosítónév minősége és találati pontosság

(7 művelet)

| # | Eszköz | Keresés / URL | Találatok |
|---|---|---|---|
| 1 | WebSearch | identifier naming quality code comprehension study Lawrie abbreviation full word | 10 |
| 2 | WebSearch | file naming convention retrieval accuracy RAG semantic search study | 9 |
| 3 | WebSearch | LLM agent file navigation naming descriptive vs abbreviated study benchmark | 8 |
| 4 | Bash-curl | curl cs.kent.edu Lawrie07.pdf + pdftotext | 1 |
| 5 | WebSearch | LLM code search bug localization file path naming quality benchmark study 2024 2025 | 8 |
| 6 | WebSearch | variable name obfuscation LLM code understanding accuracy study identifier | 8 |
| 7 | Bash-curl | curl arxiv.org/html/2510.03178 (raw HTML full text) | 1 |

## SQ-07 — Útvonal-biztonsági hibaosztályok (CVE-k)

(12 művelet)

| # | Eszköz | Keresés / URL | Találatok |
|---|---|---|---|
| 1 | WebSearch | CVE path traversal prefix matching bypass vulnerability example | 7 |
| 2 | WebSearch | Zip Slip vulnerability CVE symlink archive extraction | 8 |
| 3 | WebSearch | Unicode normalization path traversal vulnerability CVE bypass | 10 |
| 4 | WebFetch | https://github.com/unjs/ipx/security/advisories/GHSA-mm3p-j368-7jcr | 1 |
| 5 | Bash-curl | curl services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2021-41773 (NVD REST API) | 1 |
| 6 | Bash-curl | curl services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2024-43093 | 1 |
| 7 | Bash-curl | curl services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2025-54387 | 1 |
| 8 | Bash-curl | curl cwe.mitre.org/data/definitions/22.html | 1 |
| 9 | Bash-curl | curl raw.githubusercontent.com/snyk/zip-slip-vulnerability/master/README.md | 1 |
| 10 | WebSearch | CVE symlink race container escape volume mount path validation bypass | 10 |
| 11 | WebSearch | CVE case-insensitive filesystem filename collision security bypass npm package | 10 |
| 12 | Bash-curl | curl services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2021-32803/32804/37701/37712/37713 (node-tar family) | 5 |

## Összegzés

| Alkérdés | Keresés/lekérés darabszám |
|---|---|
| SQ-01 | 17 |
| SQ-02 | 7 |
| SQ-03 | 5 |
| SQ-04 | 9 |
| SQ-05 | 9 |
| SQ-06 | 7 |
| SQ-07 | 12 |
| **Összesen** | **66** |

Lásd még: `01-search-log/prisma-flow.md` (a keresés-forrás-állítás tölcsér
számszerű összegzése) és `01-search-log/blocked.jsonl` (üres — egyetlen domain
sem utasította el a lekérést ebben a körben).



---

# sq02 — A markdown fájl mint memória-egység, és a fejléc

# Keresések — sq02

Minden lefuttatott keresés szó szerint, a PRISMA-S elv szerint (a keresőkifejezés pontosan úgy, ahogy lefutott). A táblázat két eszköztípust különböztet meg: **WebSearch** (kulcsszavas keresőmotor-lekérdezés) és **közvetlen URL-lekérés** (curl a proxyn keresztül, illetve néhány esetben WebFetch/curl -L átirányítás-követéssel). A közvetlen lekérések listája a `linkek.md`-ben van részletezve; itt csak a tényleges *kereséseket* soroljuk fel.

## WebSearch lekérdezések

| # | Eszköz | Keresőkifejezés (szó szerint) | Cél / alkérdés | Megjegyzés |
|---|---|---|---|---|
| 1 | WebSearch | `YAML Norway problem "no" boolean specification 1.1 1.2` | SQ-04 | tájékozódó, széles kör |
| 2 | WebSearch | `basic-memory MCP markdown knowledge graph architecture` | SQ-01 | |
| 3 | WebSearch | `mem0 architecture vector store graph store facts extraction` | SQ-01 | |
| 4 | WebSearch | `Zep Graphiti temporal knowledge graph memory architecture` | SQ-01 | |
| 5 | WebSearch | `Letta memory blocks architecture core memory archival` | SQ-01 | |
| 6 | WebSearch | `Anthropic memory tool documentation context management` | SQ-01 | |
| 7 | WebSearch | `Claude Code memory CLAUDE.md how it works documentation` | SQ-01 | |
| 8 | WebSearch | `proposition-based chunking retrieval accuracy paper dense X-Retrieval` | SQ-02 | |
| 9 | WebSearch | `"frontmatter" too many fields keep minimal recommendation markdown notes` | SQ-03 | nem hozott számszerű ajánlást (lásd hianyok.md) |
| 10 | WebSearch | `Zettlr Dendron frontmatter fields YAML metadata note-taking` | SQ-03 | találatok azonosítva, de idő hiányában nem dolgoztuk fel elsődleges forrásból (lásd hianyok.md) |
| 11 | WebSearch | `tomlkit round-trip preserving comments python TOML library documentation` | SQ-06 | |
| 12 | WebSearch | `"Norway problem" origin blog post noyaml country code parsed as false` | SQ-04 | a kifejezés eredetének/népszerűsítésének datálásához |
| 13 | WebSearch | `"Dense X Retrieval" propositions NAACL 2024 accepted paper` | SQ-02 | a lektoráltság ellenőrzéséhez (kiderült: EMNLP 2024, nem NAACL) |
| 14 | WebSearch | `Zep temporal knowledge graph 2501.13956 accepted conference OR workshop` | SQ-01 | a Zep-papír lektoráltsági státuszának ellenőrzéséhez — eredmény: nincs bizonyíték lektorált konferencia-megjelenésre, marad T4 preprint |
| 15 | WebSearch | `Notion export markdown format title H1 frontmatter properties csv` | SQ-07 | nem hozott döntő választ, hivatalos Notion-doksi lekérve, de nem részletez (lásd hianyok.md) |

## Célzott ellenőrző keresés (nem WebSearch, hanem elsődleges forrás közvetlen URL-találgatással)

Több esetben (pl. js-yaml `lib/type/bool.js` elérési útja, Obsidian súgó egyes almappái, mem0 `how-mem0-works` oldal) próbálkoztunk közvetlen `raw.githubusercontent.com` vagy dokumentációs URL-ekkel, amelyek 404-et adtak; ezeket a `linkek.md` "Nem elérhető / 404" szakasza sorolja fel. Ezek nem keresőmotor-lekérdezések, hanem URL-találgatások az elsődleges forrás megtalálásához.

## Módszertani megjegyzés

A kutatás jelentős részét **nem** kulcsszavas keresés, hanem **közvetlen, elsődleges forráshoz navigálás** tette ki (pl. `yaml.org/spec/1.2.2/`, `raw.githubusercontent.com/toml-lang/toml/...`, hivatalos GitHub README-k) — ez szándékos, mert a feladat kifejezetten megkövetelte a specifikációk és hivatalos dokumentációk nyers lekérését keresőmotor helyett. Lásd `linkek.md` a teljes lekérési listáért és a lekérés módjáért.



---

# sq03 — Beágyazás magyarra/többnyelvűre, és az integrációs felületek

# Keresések — sq03

Minden lefuttatott keresés szó szerint, időrendben, azzal a megjegyzéssel, hogy a `WebSearch` csak találati listát ad (nem tartalmat), a `curl` és az `API` nyers tartalmat/adatot. Dátum: 2026-09-15.

## WebSearch lekérdezések (szó szerint, ahogy futtatva lettek)

1. `MTEB Hungarian retrieval task leaderboard 2026`
2. `MMTEB Massive Multilingual Text Embedding Benchmark Hungarian tasks paper`
3. `sqlite-vec documentation "how many vectors" brute force performance`
4. `SQLite FTS5 documentation snowball tokenizer stemmer languages`
5. `MTEB "BelebeleRetrieval" Hungarian "hun" task languages`
6. `mteb tasks Retrieval hun_Latn Hungarian dataset github embeddings-benchmark`
7. `"MTEB(Multilingual" leaderboard Hungarian retrieval score nDCG`
8. `multilingual-e5 technical report monolingual vs multilingual embedding non-English retrieval comparison benchmark`
9. `brute force vector search vs ANN index "how many vectors" latency memory benchmark million`
10. `Claude Code hook SessionStart output character limit documentation`
11. `Codex CLI AGENTS.md context injection size limit documentation`
12. `Gemini CLI hooks documentation SessionStart context size limit`
13. `Cursor rules AGENTS.md .cursor/rules size limit documentation context injection`
14. `Model Context Protocol specification sampling server request client LLM completion`
15. `MCP client feature support matrix tools resources prompts sampling Claude Code Cursor 2026`
16. `binary quantization embeddings recall loss percent rescoring oversampling measured benchmark Cohere OR Weaviate OR Qdrant`
17. `pgvector "exact search" vs HNSW "how many rows" recommendation flat index brute force threshold`
18. `Tordai de Rijke "Four Stemmers and a Funeral" Hungarian CLEF 2005 stemming`
19. `"Four Stemmers and a Funeral" Tordai pdf CLEF 2005 lecture notes computer science`
20. `faiss wiki "guidelines to choose an index" IndexFlat "if exact results" dataset size`
21. `embeddings-benchmark mteb "HunSum2AbstractiveRetrieval" site:github.com`
22. `mteb "eval_langs" "hun-Latn" retrieval task python github`

## WebFetch hívások (kis modell összefoglalója, nem nyers tartalom — külön jelölve minden felhasználásnál)

1. `https://github.com/anthropics/claude-code/issues/44086` — prompt: "Idézd szó szerint a bug report teljes szövegét: mi a dokumentált SessionStart hook méret/karakter-korlát (10000 karakter?), és mire csonkolja ténylegesen (2000 karakter?)."
2. `https://web.archive.org/web/20260901000000*/code.claude.com/docs/en/hooks` — prompt: "Van-e archivált változata... 2026-09-01 körül..." → eredmény: `SITE_BLOCKED` hiba, nem sikerült.

## Nyers letöltések (`curl`) — a proxyn keresztül, közvetlen HTML/Markdown/PDF/JSON tartalom

A teljes lista a `linkek.md`-ben van URL-enként felsorolva. Kiemelt technikai lépések:

- **SQLite FTS5 hivatalos dokumentáció** nyers letöltése és grep-elése tokenizáló-nevekre (`porter`, `snowball`, `unicode61`, `trigram`, `ICU`).
- **sqlite-vec dokumentáció**: a renderelt HTML (VitePress SPA) helyett a tényleges Markdown-forrást kerestük meg a `raw.githubusercontent.com`-on — a helyes elérési utat az `alexgarcia.xyz/sqlite-vec/*.html` oldalak "Edit this page" linkjeiből (`edit/main/site/...`) fejtettük vissza, mert a naiv `site/<oldal>.md` útvonal több esetben 404-et adott (pl. a Python-oldal valójában `site/using/python.md`, az Installation `site/getting-started/installation.md`).
- **MTEB nyers eredmény-adatbázis**: a `mteb/results` Hugging Face dataset 4 parquet-fájlját (össz. ~299 MB) helyben letöltöttük, majd DuckDB-vel közvetlenül lekérdeztük (`SELECT DISTINCT task_name ... WHERE list_contains(language,'hun-Latn')` stb.) — ez nem másodkézből vett szám, hanem a saját, nyers adatból származtatott eredmény.
- **PDF-ek** (Hatvani&Yang IEEE CITDS 2024; Antal Margit, Infocommunications Journal 2025/4): letöltve és `pypdf`-fel szövegre bontva, majd grep-elve a releváns táblázatokért.
- **GitHub API (`api.github.com`) és `github.com/search`**: mindkettő a proxy egy Claude Code-specifikus hibaüzenetét adta vissza ("GitHub access to this repository is not enabled for this session... Use repository-scoped endpoints"), ezért ezekhez az útvonalakhoz nem fértünk hozzá; a `raw.githubusercontent.com` viszont minden esetben működött.
- **`grep.app`**: Vercel biztonsági checkpoint (429), nem adott kódot vissza.
- **`web.archive.org` / `archive.org`**: minden kísérlet (CDX API, `available` API, `WebFetch`) meghiúsult (connection reset, illetve `SITE_BLOCKED`) — ez korlátozta a történeti (2026-09-01 körüli) dokumentáció-állapot ellenőrzését, lásd `hianyok.md`.

## Hugging Face API hívások

- `GET https://huggingface.co/api/datasets?search=Hun&author=mteb&limit=100` — 1 találat: `mteb/HunSum2AbstractiveRetrieval`.
- `GET https://huggingface.co/api/datasets?author=mteb&language=hu&limit=200` és `...language=hun...` — **nem szűrt** ténylegesen (a `language` paraméter figyelmen kívül lett hagyva a végponton, ugyanazt a generikus listát adta vissza mindkét hívásnál) — ez zsákutcának bizonyult, a tényleges "melyik taszkban van magyar" kérdést végül a parquet-adaton közvetlen SQL-lekérdezéssel oldottuk meg.
- `GET https://huggingface.co/api/datasets/mteb/results` — metaadat (utolsó módosítás: 2026-09-14T20:47:21Z).

## Semantic Scholar API

- `GET https://api.semanticscholar.org/graph/v1/paper/search?query=Four Stemmers and a Funeral Hungarian` — első kísérlet 429 (rate limit), második (10 mp várakozás után) sikeres: megerősítette a Tordai & de Rijke (2005) tanulmány létezését (DOI 10.1007/11878773_20), de az absztraktot "CLOSED" hozzáférésűnek jelezte.
