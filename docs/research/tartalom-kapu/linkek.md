# Linkek — tartalom-kapu



---

# sq01 — Titok- és kulcsfelismerés írás előtt

# sq01 — Meglátogatott és felderített linkek

Lekérés módja oszlop: **curl+strip** = nyers HTML/raw fájl letöltve `curl`-lel a proxyn keresztül, majd Python-szkripttel tag-stripelve (script/style eltávolítva, blokk-tagek → sortörés, majd whitespace-normalizálás); **WebSearch** = csak keresőmotor-eredmény, tartalom nem lett közvetlenül lekérve ez alatt a link alatt (a linkelt oldalt esetleg külön, curl-lel is lekértük — akkor az a saját sorában szerepel).

| # | Cím | URL | Tier | Lekérés módja |
|---|---|---|---|---|
| 1 | Gitleaks — README | https://raw.githubusercontent.com/gitleaks/gitleaks/master/README.md | T1 | curl+strip (raw.githubusercontent.com) |
| 2 | Gitleaks — alapértelmezett szabálykészlet (config/gitleaks.toml) | https://raw.githubusercontent.com/gitleaks/gitleaks/master/config/gitleaks.toml | T1 | curl+strip (raw.githubusercontent.com, forráskód/konfiguráció) |
| 3 | TruffleHog — README | https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/README.md | T1 | curl+strip (raw.githubusercontent.com) |
| 4 | detect-secrets (Yelp) — README | https://raw.githubusercontent.com/Yelp/detect-secrets/master/README.md | T1 | curl+strip (raw.githubusercontent.com) |
| 5 | detect-secrets — high_entropy_strings.py forráskód | https://raw.githubusercontent.com/Yelp/detect-secrets/master/detect_secrets/plugins/high_entropy_strings.py | T1 | curl+strip (raw.githubusercontent.com, forráskód) |
| 6 | detect-secrets — core/usage/plugins.py (alapértelmezett entrópia-küszöbök forrása) | https://raw.githubusercontent.com/Yelp/detect-secrets/master/detect_secrets/core/usage/plugins.py | T1 | curl+strip (raw.githubusercontent.com, forráskód) |
| 7 | GitHub Docs — Supported secret scanning patterns | https://docs.github.com/en/code-security/reference/secret-security/supported-secret-scanning-patterns (301-redirect: /introduction/supported-secret-scanning-patterns) | T1 | curl -L + strip |
| 8 | GitHub Docs — Push protection on the command line | https://docs.github.com/en/code-security/how-tos/secure-your-secrets/work-with-leak-prevention/push-protection-on-the-command-line | T1 | curl -L + strip |
| 9 | GitHub Docs — Enable push protection (repository) | https://docs.github.com/en/code-security/how-tos/secure-your-secrets/prevent-future-leaks/enable-push-protection | T1 | curl -L + strip |
| 10 | GitHub Docs — Removing sensitive data from a repository | https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository | T1 | curl -L + strip |
| 11 | GitHub Docs — Secret scanning (concept, "About secret scanning") | https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning | T1 | curl -L + strip |
| 12 | GitHub Docs — Push protection (concept oldal, bypass-indoklás) | https://docs.github.com/en/code-security/concepts/secret-security/push-protection | T1 | curl -L + strip |
| 13 | GitHub Docs — Validity checks (concept) | https://docs.github.com/en/code-security/concepts/secret-security/validity-checks | T1 | curl -L + strip |
| 14 | GitHub Docs — Responsible detection of generic secrets / AI features (redirect céloldal) | https://docs.github.com/en/code-security/responsible-use/security-and-quality-ai-features (redirect innen: about-the-detection-of-generic-secrets-with-secret-scanning) | T1 | curl -L + strip |
| 15 | GitHub Docs — Secret scanning partner program | https://docs.github.com/en/code-security/tutorials/secret-scanning-partner-program (redirect innen: secret-scanning-partner-program) | T1 | curl -L + strip |
| 16 | GitHub Blog — Making secret scanning more trustworthy: Reducing false positives at scale | https://github.blog/security/making-secret-scanning-more-trustworthy-reducing-false-positives-at-scale/ | T2 (gyártói blog, önbevallott számok) | curl -L + strip |
| 17 | "Regex is (almost) all you need" — a gitleaks készítőjének (Zachary Rice) blogbejegyzése az entrópia-küszöb eredetéről | https://lookingatcomputer.substack.com/p/regex-is-almost-all-you-need | T2 (fejlesztői blog, de a hivatalos README és a gitleaks.toml fejléce is erre hivatkozik mint a működés magyarázatára) | curl -L + strip |
| 18 | OWASP Secrets Management Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html | T1 (hivatalos OWASP-dokumentum) | curl -L + strip |
| 19 | HashiCorp Well-Architected Framework — Remediate leaked secrets | https://developer.hashicorp.com/well-architected-framework/secure-systems/secrets/manage-leaked-secrets/remediate-leaked-secrets | T2 (gyártói, de NIST-hivatkozással, elismert keretrendszer) | curl -L + strip |
| 20 | TruffleHog — Driftwood bejelentő blogbejegyzés (privát kulcs ellenőrzés) | https://trufflesecurity.com/blog/driftwood-know-if-private-keys-are-sensitive/ (redirect: /blog/driftwood) | T2/T3 (gyártói/alapítói blog, anekdotikus adatokkal) | curl -L + strip |
| 21 | FPSecretBench — README (fals pozitív adatok táblázata eszközönként) | https://raw.githubusercontent.com/setu1421/FPSecretBench/main/README.md | T1 (lektorált kutatás melléklete, ugyanaz a kutatócsoport, ESEM 2023) | curl+strip (raw.githubusercontent.com) |
| 22 | Basak, Cox, Reaves, Williams — "A Comparative Study of Software Secrets Reporting by Secret Detection Tools" (ESEM 2023) | https://ar5iv.labs.arxiv.org/html/2307.00714 | T1 (lektorált konferenciacikk, IEEE Xplore: ieeexplore.ieee.org/document/10304853) | curl+strip (ar5iv HTML-render) |
| 23 | Ugyanez a cikk — IEEE Xplore bejegyzés (csak azonosításra, tartalom nem kérve le innen) | https://ieeexplore.ieee.org/document/10304853/ | T1 | WebSearch találat, nem lett külön lekérve (fizetőfal; a nyílt arXiv/ar5iv verzió tartalmilag azonos) |
| 24 | Ugyanez a cikk — arXiv PDF | https://arxiv.org/pdf/2307.00714 | T1 | WebSearch találat, nem lett külön lekérve (az ar5iv HTML-verzió tartalmilag azonos, könnyebben elemezhető szöveg) |

## WebSearch találatok, amelyeket regisztráltunk, de nem kértünk le közvetlenül (csak keresési kontextusként hasznosultak)

| Cím | URL | Megjegyzés |
|---|---|---|
| SecretBench dataset (ResearchGate PDF) | https://www.researchgate.net/publication/369184614_SecretBench_A_Dataset_of_Software_Secrets | Az alapul szolgáló (nem az összehasonlító) SecretBench-cikk; a fenti #22 forrás ezt idézi és épít rá — nem kértük le külön, mert az összehasonlító tanulmány (#22) tartalmazza a releváns számainkat |
| Secret Breach Detection in Source Code with LLMs | https://arxiv.org/pdf/2504.18784 | Kapcsolódó, de kérdésünk szempontjából (hagyományos regex/entrópia eszközök) másodlagos — nem elemeztük részletesen |
| Secret Leak Detection in Software Issue Reports using LLMs | https://arxiv.org/html/2410.23657v4 | Más felszín (issue reportok, nem forráskód) — nem releváns közvetlenül sq01-hez |
| A Comparison of Automated Secret Detection Tools (BlueOptima) | https://www.blueoptima.com/ai-access/a-comparison-of-automated-secret-detection-tools | Gyártói/kereskedelmi összehasonlító oldal — nem lektorált, nem használtuk fel számként |
| TruffleHog vs Gitleaks vs GitHub Secret Scanning (Secrails blog) | https://secrails.com/blog/trufflehog-vs-gitleaks-github-secret-scanning-guide | T3 blog — nem használtuk fel számként |
| Gitleaks vs TruffleHog 2026 (devsecops.ae) | https://devsecops.ae/secrets-scanners-comparison-2026/ | T3 blog — nem használtuk fel számként |
| GitHub's LLM Secret Scanning Cuts False Positives by 95% (webpronews.com) | https://www.webpronews.com/githubs-llm-secret-scanning-cuts-false-positives-by-95-with-100-accuracy | T3, másodkézből tálalt gyártói szám — az elsődleges forrást (GitHub Blog, #16) használtuk helyette |
| Shannon, "Prediction and Entropy of Printed English" (1951, eredeti cikk) | https://www.princeton.edu/~wbialek/rome/refs/shannon_51.pdf | Klasszikus, lektorált forrás az angol nyelv entrópiájáról — azonosítottuk, de a jelen kutatás fókusza (secret-scanning eszközök) miatt nem olvastuk el teljes terjedelemben; magyar nyelvre vonatkozó adatot úgysem tartalmazna |
| A New Look at the Classical Entropy of Written English (arXiv 0911.2284) | https://arxiv.org/pdf/0911.2284 | Ugyanaz a megfontolás, mint fent — nem angol/magyar összevetésről szól, nem olvastuk el részletesen |

## Elérhetetlen / blokkolt / átirányított domainek

- **api.github.com** — a proxy explicit hibaüzenetet adott: *"GitHub access to this repository is not enabled for this session. Use add_repo to request access."* Emiatt nem tudtunk GitHub API-n keresztül könyvtárlistázást végezni (pl. a TruffleHog `pkg/detectors/` mappájának pontos fájlszámát közvetlenül megszámolni) — helyette a README-ben közölt, szövegesen kimondott "over 800" / "over 700" számokra hagyatkoztunk.
- **raw.githubusercontent.com/.../detect_secrets/plugins/base64_high_entropy_string.py** és **hex_high_entropy_string.py** — 404, mert ezek a fájlok a jelenlegi repóban átszerveződtek (nem blokkolás, hanem elavult útvonal); a küszöbértékeket sikeresen megtaláltuk a `core/usage/plugins.py` fájlban.
- **docs.github.com** rövid (régi) URL-ek — több esetben 301-es átirányítást adtak az új GitHub Docs URL-sémára (pl. `/code-security/secret-scanning/introduction/...` → `/code-security/reference/secret-security/...`); ezt `curl -L`-lel követtük, nem számít elérhetetlenségnek.
- Nem volt olyan domain, amely tartósan (redirect-tel sem feloldható módon) elérhetetlen lett volna a kutatás során.



---

# sq02 — Mit szűrnek a valódi agent-memória rendszerek íráskor

# sq02 — Meglátogatott és felderített linkek

Lekérés módja: **curl** = nyers HTML/markdown, proxyn keresztül, tag-stripeléssel feldolgozva; **WebFetch** = amikor a curl 403/blokk miatt nem működött (jelölve, miért); **WebSearch** = csak keresési index-találat, nem lett mélyen lekérve (csak vezetéknek/felderítésnek használva).

## Elsődleges (T1) — hivatalos dokumentáció, forráskód, akadémiai preprint

| Cím | URL | Tier | Lekérés módja |
|---|---|---|---|
| basic-memory README.md | https://raw.githubusercontent.com/basicmachines-co/basic-memory/main/README.md | T1 | curl (raw) |
| basic-memory SECURITY.md | https://raw.githubusercontent.com/basicmachines-co/basic-memory/main/SECURITY.md | T1 | curl (raw) |
| basic-memory docs — Technical Information | https://docs.basicmemory.com/reference/technical-information | T1 | curl (nyers HTML, tag-stripelt) |
| basic-memory docs sitemap (üres, JS-renderelt) | https://docs.basicmemory.com/sitemap.xml | T1 | curl |
| OWASP GenAI Security Project — hivatalos bejelentés (2025.12.09.) | https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/ | T1 | curl (nyers HTML) |
| OWASP GenAI Security Project — "Memory Is a Feature. It Is Also an Attack Surface" (2026.05.13., ASI06 lead szerzőtől) | https://genai.owasp.org/2026/05/13/memory-is-a-feature-it-is-also-an-attack-surface/ | T1 | curl (nyers HTML) |
| OWASP Agent Memory Guard — projektoldal | https://owasp.org/www-project-agent-memory-guard/ | T1 | curl (nyers HTML) |
| OWASP Agent Memory Guard — README.md | https://raw.githubusercontent.com/OWASP/www-project-agent-memory-guard/main/README.md | T1 | curl (raw) |
| Anthropic — Memory tool hivatalos dokumentáció | https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool | T1 | curl (nyers HTML) |
| Claude Code — Security dokumentáció | https://code.claude.com/docs/en/security | T1 | curl (nyers HTML) |
| Claude Code — "How Claude remembers your project" (memória-dokumentáció) | https://docs.claude.com/en/docs/claude-code/memory | T1 | curl (nyers HTML) |
| Claude Code — Changelog | https://code.claude.com/docs/en/changelog | T1 | curl (nyers HTML) |
| MINJA — Memory Injection Attacks on LLM Agents via Query-Only Interaction (Dong et al.) | https://arxiv.org/abs/2503.03704 | T1 | curl (nyers HTML) |
| AgentPoison — Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases (Chen et al., NeurIPS 2024) | https://arxiv.org/abs/2407.12784 | T1 | curl (nyers HTML) |
| mem0 — Custom Instructions (Custom Fact Extraction Prompt) hivatalos dokumentáció | https://docs.mem0.ai/open-source/features/custom-fact-extraction-prompt | T1 | curl (nyers HTML) |
| Letta — Memory Blocks hivatalos dokumentáció | https://docs.letta.com/guides/core-concepts/memory/memory-blocks | T1 | curl (nyers HTML) |
| Zep/Graphiti — Getting Started Overview | https://help.getzep.com/graphiti/getting-started/overview | T1 | curl (nyers HTML) |
| Graphiti README.md | https://raw.githubusercontent.com/getzep/graphiti/main/README.md | T1 | curl (raw) |
| Graphiti SECURITY.md | https://raw.githubusercontent.com/getzep/graphiti/main/SECURITY.md | T1 | curl (raw) |
| Microsoft Presidio FAQ (markdown forrás) | https://raw.githubusercontent.com/microsoft/presidio/main/docs/faq.md | T1 | curl (raw; a microsoft.github.io/presidio/faq/ élő oldal 404-et adott, GitHub Pages migráció miatt) |
| Guardrails AI — Error and Remediation (OnFailAction) | https://guardrailsai.com/guardrails/docs/concepts/error_remediation | T1 | curl (nyers HTML) |
| OpenAI — Memory FAQ | https://help.openai.com/en/articles/8590148-memory-faq | T1 | **WebFetch** (curl Cloudflare-kihívást (403) kapott, JS-védelem) |
| OpenAI — "Memory and new controls for ChatGPT" bejelentés | https://openai.com/index/memory-and-new-controls-for-chatgpt/ | T1 | **WebFetch** (curl Cloudflare-kihívást (403) kapott) |

## Másodlagos (T2) — megbízható gyártói/elemzői anyag

| Cím | URL | Tier | Lekérés módja |
|---|---|---|---|
| Cisco Blogs — "Identifying and remediating a persistent memory compromise in Claude Code" (MemoryTrap) | https://blogs.cisco.com/ai/identifying-and-remediating-a-persistent-memory-compromise-in-claude-code | T1/T2 | curl (nyers HTML) |
| Embrace The Red — "Hacking Gemini's Memory with Prompt Injection and Delayed Tool Invocation" (Johann Rehberger) | https://embracethered.com/blog/posts/2025/gemini-memory-persistence-prompt-injection/ | T2 | curl (nyers HTML) |
| Unit 42 (Palo Alto Networks) — "When AI Remembers Too Much" (Amazon Bedrock PoC) | https://unit42.paloaltonetworks.com/indirect-prompt-injection-poisons-ai-longterm-memory/ | T2 | curl (nyers HTML) |
| Unit 42 — "Fooling AI Agents: Web-Based Indirect Prompt Injection Observed in the Wild" | https://unit42.paloaltonetworks.com/ai-agent-prompt-injection/ | T2 | curl (nyers HTML) — **megjegyzés:** ellenőrizve, hogy 0 "memory" említést tartalmaz; általános IDPI-ről szól, nem memória-mérgezésről, csak kontextusként idézve |
| OECD.AI — Gemini incidens-bejegyzés | https://oecd.ai/en/incidents/2025-02-11-0df5 | T2 | WebFetch |
| Vectorize.io — "OWASP ASI06: Memory and Context Poisoning Explained" | https://vectorize.io/articles/owasp-asi06 | T2 | curl (nyers HTML) |
| Modulos — "OWASP Top 10 for Agentic Applications (2026)" governance guide | https://docs.modulos.ai/frameworks/owasp-top-10-agentic | T2 | curl (nyers HTML) |
| DeepTeam — "OWASP Top 10 for Agents 2026" docs | https://www.trydeepteam.com/docs/frameworks-owasp-top-10-for-agentic-applications | T2 | curl (nyers HTML) |
| mem0 — "AI Memory Security: Best Practices and Implementation" blog | https://mem0.ai/blog/ai-memory-security-best-practices | T2 | curl (nyers HTML) |
| Vectra.ai — "Prompt injection: types, real-world CVEs, and enterprise defenses" | https://www.vectra.ai/topics/prompt-injection | T2 | curl (nyers HTML) |
| Cyberhaven — "DLP False Positives: What They Are and How to Reduce Them" | https://www.cyberhaven.com/infosec-essentials/dlp-false-positives | T2/T3 | curl (nyers HTML) |

## Harmadlagos (T3) — közösségi/blog/egyéni forrás

| Cím | URL | Tier | Lekérés módja |
|---|---|---|---|
| serendb.com — "Claude Code's Local Memory Is a Security Risk" | https://serendb.com/blog/claude-code-local-memory-security-risk | T3 | curl (nyers HTML) |
| GitHub Issue #3342 — letta-ai/letta, "Security: OWASP Agent Memory Guard for memory poisoning defense (ASI06)" | https://github.com/letta-ai/letta/issues/3342 | T3 | WebFetch (GitHub API nem volt elérhető ehhez a repóhoz ebben a sessionben) |
| GitHub Issue #3320 — letta-ai/letta, "[Feature] Memory governance — policy enforcement for stateful agent memory" | https://github.com/letta-ai/letta/issues/3320 | T3 | WebFetch |

## Csak keresési index-találat (WebSearch), mélyen nem lekérve — vezetéknek/felderítésnek használva

Ezek nem szolgálnak önálló bizonyítékként a jelentésben, csak arra kellettek, hogy megtaláljuk a fenti elsődleges forrásokat, vagy háttér-kontextust adjanak:

- wavect.io — "MCP Is Not a Security Boundary: Protect Agent Data" (blogcím-szintű felderítés, nem lekérve)
- neuraltrust.ai — "What is Memory & Context Poisoning?" (nem lekérve, tartalma feltehetően átfed a Vectorize-cikkel)
- willvelida.com — "Preventing Memory and Context Poisoning in AI Agents" (nem lekérve)
- zealynx.io — "OWASP ASI06 Explained: AI Memory & Context Poisoning" (nem lekérve, harmadik konvergáló parafrázis-forrás lett volna)
- github.com/MervinPraison/PraisonAI Issue #5028 — "Memory subsystem has no provenance/trust boundary..." (címe szerint releváns 3. keretrendszer-példa, de a mélyebb feldolgozás elmaradt idő/token-korlát miatt)
- Számos GitHub-repó ("NousResearch/hermes-agent" több issue-ja guardrail/memory-write témában) — ezek megbízhatósága kétséges volt (gyanúsan ismétlődő, esetleg automatikusan generált issue-minta), ezért **szándékosan nem használtuk fel** bizonyítékként; csak a keresési naplóban rögzítjük, hogy találkoztunk velük és elvetettük őket.

## Nem elérhető / blokkolt domainek

| Domain | Probléma |
|---|---|
| microsoft.github.io/presidio/faq/ | 404 — a Presidio dokumentáció időközben a `data-privacy-stack` szervezet alá és GitHub Pages-ről máshova migrált; a `raw.githubusercontent.com` forrásból sikerült pótolni |
| help.openai.com | curl: 403, Cloudflare "Enable JavaScript and cookies to continue" kihívás — WebFetch-csel megkerülve |
| openai.com | curl: 403, ugyanaz a Cloudflare-védelem — WebFetch-csel megkerülve |
| api.github.com (letta-ai/letta, MervinPraison/PraisonAI repókra) | "GitHub access to this repository is not enabled for this session" — a munkakörnyezet GitHub API-integrációja csak bizonyos repókra van engedélyezve; a nyilvános issue-oldalakat WebFetch-csel sikerült helyette olvasni |
| docs.basicmemory.com (sitemap) | Üresen tért vissza — a sitemap.xml JS-oldalgenerálás miatt nem tartalmazza a tényleges oldallistát; közvetlen útvonal-próbálkozások (`/security`, `/faq` stb.) mind 404-et adtak |
