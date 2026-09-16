# Keresések — tartalom-kapu



---

# sq01 — Titok- és kulcsfelismerés írás előtt

# sq01 — Lefuttatott keresések (szó szerint)

## Módszertani előzmény

A `deep-web-research` skill előírása szerint a keresésnek Sonnet-alapú, párhuzamos subagent-fan-outnak kellene lennie, Opus-szintézissel lezárva. Ebben a végrehajtási környezetben **nem állt rendelkezésre subagent-indító (Agent) eszköz**, ezért a kutatás egyetlen, szekvenciális menetben zajlott: WebSearch-lekérdezések + célzott `curl` (nyers HTML/raw fájl) letöltések, tag-stripeléssel. Ez a skill saját "degradált mód" ága szerint dokumentálandó korlátozás.

## WebSearch lekérdezések (szó szerinti query-string)

1. `SecretBench dataset software secrets false positive false negative gitleaks trufflehog detect-secrets`
   - Cél: lektorált vagy nagymintás mérés keresése a fals pozitív/negatív arányokról.
   - Eredmény: megtalálta a FPSecretBench GitHub repót és a hozzá tartozó ESEM 2023 tanulmányt (arXiv 2307.00714) — ez lett a kutatás kulcsforrása Q2/Q4-hez.

2. `peer-reviewed evaluation secret detection tools precision recall false positive rate gitleaks trufflehog`
   - Cél: megerősíteni, hogy az előző találat valóban lektorált, és nincs-e más, hasonló mérés.
   - Eredmény: ugyanazt a cikket hozta fel (IEEE Xplore + arXiv + ResearchGate linkekkel), plusz néhány nem lektorált gyártói/blog összehasonlítást (BlueOptima, Secrails, devsecops.ae) — ezeket forrásként elvetettük, csak `linkek.md`-ben regisztráltuk.

3. `Shannon entropy bits per character English text natural language redundancy 1.0 1.5`
   - Cél: általános nyelvi-entrópia bázisérték keresése összehasonlításképp (mivel magyar nyelvre nincs adat).
   - Eredmény: megtalálta Shannon 1951-es eredeti cikkét és egy 2009-es újraszámolást (arXiv 0911.2284); ezeket csak azonosítottuk, nem dolgoztuk fel részletesen, mert a kutatás fókusza a secret-scanning eszközök viselkedése, nem az általános nyelvi entrópia-elmélet — és magyar nyelvre úgysem tartalmaznának adatot.

4. `OWASP NIST guidance leaked credential rotate secret remove from git history`
   - Cél: Q6-hoz (mit kell tenni, ha már bekerült a titok) független, nem GitHub-forrású megerősítés keresése.
   - Eredmény: OWASP Secrets Management Cheat Sheet (hivatalos, T1) és HashiCorp Well-Architected Framework (T2, NIST-hivatkozással) — mindkettőt felhasználtuk.

5. `GitHub secret scanning validity checks false positive rate precision`
   - Cél: van-e publikált szám kifejezetten a "validity checks" (ellenőrzött titok) módra vonatkozóan.
   - Eredmény: nem talált külön számot a validity checks pontosságára; viszont felszínre hozta a GitHub 2026-os "Making secret scanning more trustworthy" blogbejegyzését (gyártói, relatív FP-csökkentési állítással) és a "Responsible detection of generic secrets" dokumentumot — mindkettőt felhasználtuk, explicit gyártói jelöléssel, ill. mint a magasabb-FP AI-mód beismerése.

## Célzott `curl` lekérések a proxyn keresztül (nyers HTML/raw fájl + tag-stripelés)

Minden lekérés `curl -sSL -A "Mozilla/5.0 ... research-agent"` paranccsal történt, a rendszer proxyján (`$HTTPS_PROXY`, port 38353) keresztül, majd egy Python-szkripttel: `<script>`/`<style>` blokkok eltávolítása, blokk-szintű tagek (`<br>`, `</p>`, `</li>`, `</tr>`, `</h1-6>`, `</div>`) sortörésre cserélése, majd az összes maradék tag eltávolítása és a whitespace normalizálása. Raw GitHub-fájloknál (`raw.githubusercontent.com`) nem volt szükség stripelésre, azok sima szöveg/kód fájlok.

Lekért URL-ek listája és eredménye — lásd részletesen `linkek.md` táblázatát (1–22. sor). Ide csak a technikai eseményeket rögzítjük:

- `curl -sS "$HTTPS_PROXY/__agentproxy/status"` — a kutatás elején, ellenőrzésképp: a proxy aktív, `enabled: true`, port 38353, `bundleCoversEveryHost: true`.
- `https://api.github.com/repos/Yelp/detect-secrets/contents/detect_secrets/plugins` — **hibát adott**: `{"message":"GitHub access to this repository is not enabled for this session. Use add_repo to request access..."}`. Ez a proxy/eszközkörnyezet saját GitHub API-korlátozása, nem a forrás elérhetetlensége. Nem próbáltuk megkerülni (pl. `add_repo` hívással), mert az írási/hozzáférési jogosultság kérése túlmutatna a kutatási feladat keretein.
- Két detect-secrets forrásfájl-útvonal (`base64_high_entropy_string.py`, `hex_high_entropy_string.py`) 404-et adott — ezek a fájlok időközben átszerveződtek a repóban; a keresett adatot (alapértelmezett entrópia-küszöbök: base64=4.5, hex=3.0) sikeresen megtaláltuk a `detect_secrets/core/usage/plugins.py` fájlban.
- Több `docs.github.com` rövid/régi URL 301-es átirányítást adott az új GitHub Docs URL-sémára; ezeket `-L` kapcsolóval követtük, minden esetben sikerrel (200-as végállapot).
- Három próbálkozás a "validity checks" oldal pontos URL-jének kitalálására: két útvonal 404-et adott, a harmadik (`/en/code-security/concepts/secret-security/validity-checks`) 200-at.

## Saját (nem publikált forrásból származó) számítás

A magyar nyelvű szöveg entrópia-viselkedésére vonatkozó adathiány (lásd `hianyok.md`) részleges illusztrálására egy önálló Python-szkriptet futtattunk (`collections.Counter`-alapú Shannon-entrópia-számítás, karakterenkénti és UTF-8 bájtszintű mérés egyaránt, kis, kézzel írt mintákon). Ez **nem keresés**, hanem saját számítás — a `megallapitasok.md` 3.4 pontjában és `hianyok.md`-ben explicit jelölve van, hogy nem publikált mérés, csak illusztráció.

## Elérhetetlen domainek összegzése

- `api.github.com` — a munkakörnyezet proxyja korlátozza (lásd fent), nem a forrás hibája.
- Minden más megcélzott domain (github.com raw fájlok, docs.github.com, github.blog, cheatsheetseries.owasp.org, developer.hashicorp.com, trufflesecurity.com, lookingatcomputer.substack.com, ar5iv.labs.arxiv.org, raw.githubusercontent.com) sikeresen elérhető volt, esetenként átirányítás után.



---

# sq02 — Mit szűrnek a valódi agent-memória rendszerek íráskor

# sq02 — Keresések naplója

Minden alábbi keresés szó szerint, futtatási sorrendben. A `[WebSearch]` jelölésű tételek a beépített keresőeszközzel futottak; a `[curl]` és `[WebFetch]` tételek konkrét URL-ek lekérését jelölik (ezek listája és a lekérés módja a `linkek.md`-ben van részletezve, itt csak a keresési lekérdezések szerepelnek).

1. `[WebSearch]` "basic-memory MCP "not a security boundary" write access control" — nem hozott releváns találatot a pontos idézetre, csak szabadalmi dokumentumokat és irreleváns blogokat.
2. `[WebSearch]` "mem0 content filtering PII redaction on add() guardrails" — vezetett a "Filtering what NOT to remember" (theneuralbase.com, harmadik fél oktatóanyag, nem hivatalos) és AWS Bedrock Guardrails találatokhoz; a hivatalos mem0-dokumentációhoz külön kereséssel jutottunk el.
3. `[WebSearch]` "OWASP Top 10 Agentic Applications ASI06 Memory Context Poisoning" — megtalálta a genai.owasp.org hivatalos bejelentést és a Vectorize/Zealynx/NEWORDER másodlagos elemzéseket.
4. `[WebSearch]` "Anthropic "memory tool" API context editing security content validation" — megtalálta a platform.claude.com hivatalos dokumentációt.
5. `[WebSearch]` "OWASP genai.owasp.org "Top 10 for Agentic Applications" GitHub repository ASI06" — nem talált közvetlen GitHub-repót a hivatalos katalógushoz.
6. `[WebSearch]` "basic-memory github readme "security" "not a security boundary"" — nem hozott találatot a konkrét idézetre; irreleváns eredmények (más "security" nevű repók).
7. `[WebSearch]` "Letta MemGPT archival memory insert content validation filter" — harmadik fél oktatóanyagokat hozott (theneuralbase.com), a hivatalos Letta-dokumentációt külön kereséssel találtuk meg.
8. `[WebSearch]` ""basic-memory" basicmachines github MCP knowledge base markdown" — megtalálta a hivatalos GitHub-repót (basicmachines-co/basic-memory) és a docs.basicmemory.com-ot.
9. `[WebSearch]` "Zep Graphiti ingestion content validation moderation knowledge graph poisoning" — nem hozott közvetlen találatot tartalom-validációról; a hivatalos Zep/Graphiti oldalakhoz vezetett.
10. `[WebSearch]` "ChatGPT memory feature content policy what gets saved moderation OpenAI" — megtalálta az openai.com bejelentést és a help.openai.com FAQ-ot (mindkettőt utólag WebFetch-csel kellett lekérni Cloudflare-blokk miatt).
11. `[WebSearch]` "Claude Code CLAUDE.md memory file security warning untrusted content" — megtalálta a code.claude.com/docs/en/security oldalt és több harmadik fél "Claude Code security risk" blogot (pl. serendb.com).
12. `[curl]` basic-memory README.md nyers lekérése és `grep -i security` — 0 találat.
13. `[curl]` genai.owasp.org hivatalos bejelentés nyers lekérése és `ASI06` kontextus kinyerése.
14. `[curl]` platform.claude.com/.../memory-tool nyers lekérése, "Security considerations" szakasz kinyerése.
15. `[curl]` code.claude.com/docs/en/security nyers lekérése, "memory" kulcsszóra keresés (0 releváns találat ezen az oldalon).
16. `[curl]` basic-memory SECURITY.md nyers lekérése (GitHub raw) — teljes threat model szöveg kinyerve.
17. `[curl]` docs.basicmemory.com/reference/technical-information nyers lekérése, "security boundary" kifejezésre keresés — 0 találat.
18. `[Bash]` OWASP announce szövegben "ASI06" második előfordulásának kontextusa — megtalálta a "Gemini Memory Attack" hivatkozást.
19. `[WebSearch]` "Gemini memory attack prompt injection persistent long-term memory researcher disclosure" — megtalálta az Embrace The Red elsődleges blogot és az OECD.AI incidens-bejegyzést.
20. `[WebSearch]` ""ASI06" site:genai.owasp.org OR site:owasp.org memory context poisoning mitigation" — megtalálta az OWASP Agent Memory Guard projektoldalt és a "Memory Is a Feature" blogot.
21. `[WebSearch]` "OWASP Agentic AI Top 10 github repository OWASP-org agentic-security" — vegyes, részben irreleváns (nem hivatalos fork-ok) találatok.
22. `[curl]` embracethered.com Gemini-cikk nyers lekérése.
23. `[curl]` owasp.org/www-project-agent-memory-guard/ nyers lekérése.
24. `[WebFetch]` oecd.ai/en/incidents/2025-02-11-0df5 — incidens-összefoglaló kinyerése.
25. `[WebSearch]` ""OWASP Top 10 for Agentic Applications" 2026 official document pdf download ASI01 ASI10 list" — nem talált közvetlenül elérhető PDF-et vagy hivatalos katalógusoldalt.
26. `[Bash]` github.com/OWASP/www-project-agentic-skills-top-10 próbalekérés — 0 byte (nem a keresett projekt, névhasonlóság csak).
27. `[curl]` vectorize.io/articles/owasp-asi06 nyers lekérése — az 5 rétegű kontroll-készlet és a mért adatok kinyerve.
28. `[WebSearch]` "MINJA memory injection attack LLM agent success rate paper" — megtalálta az arXiv:2503.03704-et és a mem0 biztonsági blogot.
29. `[WebSearch]` "mem0 official docs custom fact extraction prompt "add" filter what to remember" — megtalálta a docs.mem0.ai hivatalos Custom Instructions oldalt.
30. `[curl]` arxiv.org/abs/2503.03704 (MINJA) absztrakt nyers lekérése.
31. `[curl]` docs.mem0.ai Custom Instructions oldal nyers lekérése.
32. `[curl]` mem0.ai/blog/ai-memory-security-best-practices nyers lekérése (két részletben, a folytatást is beolvasva).
33. `[WebSearch]` "Palo Alto Unit 42 agent memory poisoning indirect prompt injection proof of concept" — megtalálta mindkét Unit 42 cikket.
34. `[WebSearch]` "mem0 "security boundary" OR "not responsible" OR "your responsibility" documentation disclaimer" — nem hozott releváns találatot mem0-specifikus nyilatkozatra (csak generikus jogi disclaimer-sablonokat).
35. `[curl]` unit42.paloaltonetworks.com/indirect-prompt-injection-poisons-ai-longterm-memory/ nyers lekérése.
36. `[curl]` unit42.paloaltonetworks.com/ai-agent-prompt-injection/ nyers lekérése + `grep -i memory` ellenőrzés (0 találat — megerősítve, hogy ez a cikk nem memória-specifikus).
37. `[Bash]` unit42-memory-poison.txt folytatásának kiolvasása "Amazon welcomed" kontextustól.
38. `[WebSearch]` "CVE agent memory poisoning MCP server vulnerability 2025 2026" — vegyes találatok, elvezetett a Vectra.ai CVE-összegzéshez.
39. `[curl]` vectra.ai/topics/prompt-injection nyers lekérése, CVE-azonosítók kinyerése (`grep -o "CVE-..."`).
40. `[Bash]` az egyes CVE-k kontextusának kinyerése a Vectra-szövegből (6 db CVE).
41. `[WebSearch]` ""CVE-2025-53773" GitHub Copilot memory RCE details prompt injection" — megerősítette, hogy ugyanaz a kutató (Johann Rehberger) publikálta.
42. `[Bash]` "Attack success rate benchmarks" szakasz kiolvasása a Vectra-szövegből.
43. `[curl]` help.openai.com/en/articles/8590148-memory-faq — Cloudflare-kihívás (403), tartalom nem elérhető curl-lal.
44. `[curl]` openai.com/index/memory-and-new-controls-for-chatgpt/ — ugyanaz a Cloudflare-blokk (403).
45. `[WebFetch]` help.openai.com/en/articles/8590148-memory-faq — sikeres, tartalom kinyerve.
46. `[WebFetch]` openai.com/index/memory-and-new-controls-for-chatgpt/ — sikeres, a kulcs "steer ChatGPT away" idézet kinyerve.
47. `[WebSearch]` "getzep.com OR help.getzep.com security "data" ingestion "prompt injection" OR "malicious" official" — nem hozott célzott találatot.
48. `[WebSearch]` "Letta security docs prompt injection memory "not a security boundary" OR "trust"" — megtalálta a PraisonAI GitHub issue-t és több általános "trust boundary" blogot.
49. `[curl]` docs.letta.com/guides/core-concepts/memory/memory-blocks nyers lekérése, `grep` a validáció/limit kulcsszavakra.
50. `[curl]` help.getzep.com/graphiti/getting-started/overview nyers lekérése, biztonsági kulcsszavakra keresés.
51. `[curl]` serendb.com/blog/claude-code-local-memory-security-risk nyers lekérése.
52. `[curl]` docs.claude.com/en/docs/claude-code/memory nyers lekérése.
53. `[Bash]` claude-code-memory-docs.txt kulcsszó-keresés (sensitive/secur/filter/secret/PII/malicious/sanit) — csak szervezeti szabályfájl-nevekben ("security.md" mint felhasználói fájl) találtunk egyezést, nem a rendszer saját tartalom-kapujában.
54. `[WebSearch]` "getzep graphiti github SECURITY.md OR security policy content validation" — megtalálta a Graphiti GitHub-repót.
55. `[curl]` api.github.com/repos/MervinPraison/PraisonAI/issues/5028 — sikertelen (session-szintű GitHub API-hozzáférés hiánya erre a repóra).
56. `[curl]` vectra.ai CVE-lista alapján további keresés.
57. `[WebSearch]` "CVE agent memory poisoning MCP server vulnerability 2025 2026" (ismételve, más találatokkal).
58. `[Bash]` raw.githubusercontent.com/OWASP/agent-memory-guard/main/README.md próbalekérés — 404 (rossz repónév).
59. `[Bash]` api.github.com/search/repositories?q=agent-memory-guard — nem adott releváns találatot közvetlenül (a helyes repónevet a projektoldalról nyertük ki).
60. `[WebSearch]` "DLP false positive rate regex pattern content filtering limitations enterprise" — megtalálta a Cyberhaven cikket.
61. `[WebSearch]` "Microsoft Presidio PII detection limitations false positive false negative regex" — megtalálta a Presidio FAQ-ot.
62. `[curl]` microsoft.github.io/presidio/faq/ — 404 (GitHub Pages migráció).
63. `[curl]` cyberhaven.com/infosec-essentials/dlp-false-positives nyers lekérése.
64. `[Bash]` api.github.com/search/repositories?q=org:OWASP+memory+guard — üres eredmény.
65. `[Bash]` owasp.org/www-project-agent-memory-guard/ HTML-ből GitHub-link kinyerése (`grep -o`) — megtalálta a helyes repót: OWASP/www-project-agent-memory-guard.
66. `[WebSearch]` "AgentPoison NeurIPS 2024 backdoor attack RAG agent memory success rate abstract" — megtalálta az arXiv:2407.12784-et.
67. `[curl]` arxiv.org/abs/2407.12784 (AgentPoison) absztrakt nyers lekérése.
68. `[curl]` raw.githubusercontent.com/OWASP/www-project-agent-memory-guard/main/README.md — teljes README nyers lekérése (2 részletben).
69. `[Bash]` microsoft/presidio/main/docs/faq.md raw markdown lekérése — sikeres, teljes FAQ-szöveg kinyerve.
70. `[WebSearch]` "Microsoft Presidio "not guarantee" OR "cannot guarantee" OR "false negative" accuracy documentation PII" — megerősítette a FAQ-forrást.
71. `[WebSearch]` "Palo Alto Unit 42 agent memory poisoning..." (lásd 33. tétel).
72. `[WebSearch]` "genai.owasp.org "ASI06" "Memory" "Context Poisoning" page description mitigation OR "Prevention"" — megtalálta a "docs(owasp-agentic): point ASI06 mitigation..." GitHub PR-t (confident-ai/deepteam), ami elvezetett a DeepTeam docs-hoz.
73. `[Bash]` genai.owasp.org több valószínű ASI06-útvonal próbája (`/asi06`, `/ASI06`, `/top10/asi06`, `/llmrisk/asi06-memory-context-poisoning`, `/asi06-memory-and-context-poisoning`) — mind 404, kivéve `/agentic-security-initiative` (301, de nem ASI06-specifikus tartalom).
74. `[curl]` docs.modulos.ai/frameworks/owasp-top-10-agentic nyers lekérése, ASI06-szakasz kinyerése (2 előfordulás: összefoglaló táblázat + részletes szakasz).
75. `[curl]` trydeepteam.com/docs/frameworks-owasp-top-10-for-agentic-applications nyers lekérése, ASI06-szakasz kinyerése.
76. `[Bash]` genai.owasp.org/2026/05/13/memory-is-a-feature-it-is-also-an-attack-surface/ nyers lekérése — a "MemoryTrap" hivatkozás felfedezése (Cisco/Claude Code eset).
77. `[WebSearch]` "Cisco "MemoryTrap" Claude Code persistent prompt injection memory hooks disclosure" — megtalálta a Cisco elsődleges blogot és a "thebreach.news" másodközlést.
78. `[WebSearch]` "Claude Code v2.1.50 changelog memory system prompt security fix" — megtalálta a Cisco blogot és a hivatalos Claude Code changelog-ot.
79. `[curl]` blogs.cisco.com/ai/identifying-and-remediating-a-persistent-memory-compromise-in-claude-code nyers lekérése (2 részletben: bevezető + "Step 2: The Poisoning" és a "Disclosure" szakasz).
80. `[curl]` code.claude.com/docs/en/changelog nyers lekérése, `grep` a "2.1.5X" verziószámokra.
81. `[WebSearch]` "DLP false positive rate regex pattern content filtering limitations enterprise" (lásd 60. tétel).
82. `[WebSearch]` ""basic memory" "NOT a security boundary" OR "not a security boundary" basicmachines OR basicmemory" — nem hozott találatot a pontos idézetre; csak a hivatalos repók listáját adta vissza.
83. `[WebSearch]` "Letta security.md github OR docs "prompt injection" OR "trust" official statement" — megtalálta a letta-ai/letta Issue #3342-t és #3320-at.
84. `[WebSearch]` "getzep graphiti github SECURITY.md OR security policy content validation" (lásd 54. tétel).
85. `[curl]` raw.githubusercontent.com/getzep/graphiti/main/README.md nyers lekérése, biztonsági kulcsszavakra `grep`.
86. `[curl]` raw.githubusercontent.com/getzep/graphiti/main/SECURITY.md nyers lekérése.
87. `[WebSearch]` "Letta.com trust security "prompt injection" OR "agent memory" official statement documentation" — megtalálta a két releváns GitHub issue-t.
88. `[Bash]` api.github.com/repos/letta-ai/letta/issues/3342 és /3320 — sikertelen ("GitHub access to this repository is not enabled for this session").
89. `[WebFetch]` github.com/letta-ai/letta/issues/3342 — sikeres, issue-tartalom kinyerve.
90. `[WebFetch]` github.com/letta-ai/letta/issues/3320 — sikeres, issue-tartalom kinyerve.
91. `[WebSearch]` "agent write blocked guardrail failure retry behavior workaround "silently fail" memory write rejected" — csak alacsony megbízhatóságú, gyanúsan generált GitHub-repókat (pl. "NousResearch/hermes-agent" ismétlődő issue-mintázattal) hozott; **szándékosan elvetve**, nem használtuk fel bizonyítékként.
92. `[WebSearch]` ""alert fatigue" OR "guardrail" agent gives up retries when blocked LLM tool call rejected behavior change" — megtalálta a Guardrails AI Error and Remediation dokumentációt és az Arthur AI guardrails blogot (utóbbi nem lett mélyen lekérve, idő/token-korlát miatt).
93. `[curl]` guardrailsai.com/guardrails/docs/concepts/error_remediation nyers lekérése.

## Nem elérhető domainek (összegzés — részletek a linkek.md-ben)

- `microsoft.github.io/presidio/faq/` — 404 (migrált dokumentáció, pótolva raw GitHub markdown-nal)
- `help.openai.com`, `openai.com` — Cloudflare JS-kihívás (403) curl-lal; WebFetch-csel megkerülve
- `api.github.com` — csak korlátozott repókra van engedélyezve ebben a sessionben (`letta-ai/letta`, `MervinPraison/PraisonAI` nem volt köztük); a nyilvános issue-oldalakat WebFetch-csel olvastuk el helyette
- `docs.basicmemory.com/sitemap.xml` — technikailag elérhető, de üres (JS-renderelt SPA, a sitemap generátor nem futott le build-time)
