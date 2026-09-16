# Kivonat — tartalom-kapu



---

# sq01 — Titok- és kulcsfelismerés írás előtt

# sq01 — Titok- és kulcsfelismerés írás előtt: megállapítások

**Kampány:** tartalom-kapu · **Alkérdés:** sq01
**Kontextus:** `easter-memory-system` — fájl-alapú (nem git-alapú) agent-memória; a kérdés, hogy egy írás-előtti tartalomszűrő (titok/kulcs-felismerő) mennyire megbízhatóan tudná blokkolni vagy jelezni a titkot tartalmazó bejegyzéseket, és mi történik, ha egy titok mégis bekerül a verziózott történetbe.

## Módszertani megjegyzés (átláthatóság kedvéért)

Ez a kutatás egyetlen ügynök által, szekvenciálisan készült — a `deep-web-research` skillben leírt Sonnet-kereső / Opus-szintézis modell-szétválasztás **nem valósult meg**, mert ebben a végrehajtási környezetben nem állt rendelkezésre subagent-indító (Agent) eszköz. Ez a skill saját "degradált mód" ága szerint dokumentálandó hiányosság: a keresés és a szintézis ugyanabban a kontextusban, ugyanazzal a modellel történt. Ahol lehetett, ezt kompenzáltuk azzal, hogy elsődleges forrásokat (forráskód, hivatalos dokumentáció nyers HTML-je, lektorált tanulmány) kerestünk, nem összefoglalókat.

Tier-jelölés: **T1** = hivatalos dokumentáció / forráskód / lektorált tanulmány; **T2** = megbízható másodlagos vagy gyártói leírás (pl. gyártói blog, keretrendszer-ajánlás); **T3** = fórum/blog/anekdota.

---

## 1. Milyen mintázatokkal lehet titkot felismerni szövegben?

### 1.1 Gitleaks — regex + soronkénti Shannon-entrópia, kulcsszó-előszűréssel

A gitleaks alapból **regex-alapú**, minden szabály egy Go reguláris kifejezés, amelyhez opcionálisan hozzárendelhető egy entrópia-küszöb, amit **csak a regex által kifogott csoportra** (nem a teljes sorra) számol ki.

A hivatalos konfigurációs sablon (`config/gitleaks.toml` kommentje) szó szerint így írja le az entrópiamezőt:

> "Float representing the minimum shannon entropy a regex group must have to be considered a secret." — [gitleaks.toml, T1, raw.githubusercontent.com]

**Konkrét számok** a jelenlegi (2026-09-15-i letöltésű) alapértelmezett `config/gitleaks.toml` fájlból, közvetlen fájlszámlálással:

- **222** darab `[[rules]]` blokk (222 egyedi `id =` sor) — tehát **222 beépített minta**.
- Ebből **130** szabály rendelkezik explicit `entropy = ` mezővel, azaz kombinálja a regexet Shannon-entrópia-szűréssel; a maradék ~92 szabály tisztán regex-alapú.
- Az entrópia-küszöbök szabályonként eltérnek: a megfigyelt értékek 2, 3, 3.8, 3.5, 4 (lásd 3. pont).

Példa a `generic-api-key` szabályra (ez a "bármi, ami kulcsnak/tokennek néz ki" univerzális szabály), szó szerint a forrásból:

```
id = "generic-api-key"
regex = '''(?i)[\w.-]{0,50}?(?:access|auth|(?-i:[Aa]pi|API)|credential|creds|key|passw(?:or)?d|secret|token)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([\w.=-]{10,150}|[a-z0-9][a-z0-9+/]{11,}={0,3})(?:[\x60'"\s;]|\\[nr]|$)'''
entropy = 3.5
keywords = ["access","api","auth","key","credential","creds","passwd","password","secret","token"]
```

Ez a minta három technikát kombinál egyszerre: **kulcsszó-előszűrés** (a sorban szerepelnie kell egy "key/secret/token/..." szónak), **regex** (a kulcsszó utáni érték formátumát vizsgálja) és **entrópia** (a kinyert érték Shannon-entrópiájának 3.5 fölött kell lennie). A gitleaks készítője (Zachary Rice) ezt így foglalja össze a hivatalos README-ből is linkelt bejegyzésben:

> "How Gitleaks combines regex, entropy, and allowlists to find secrets" — [Regex is (almost) all you need, T2, gitleaks maintainer blog, a hivatalos README és a gitleaks.toml fejléce is erre hivatkozik mint magyarázatra]

### 1.2 TruffleHog — regex-alapú detektorok + élő API-ellenőrzés ("verified")

A TruffleHog elsődlegesen **regex-alapú detektorokra** épít, de a fő megkülönböztető jegye, hogy minden talált mintát megpróbál **élőben ellenőrizni** a szolgáltató API-ja ellen (lásd 4. pont). A hivatalos README szó szerint:

> "TruffleHog classifies over 800 secret types, mapping them back to the specific identity they belong to." — [T1, raw README]

> "We've **added over 700 credential detectors that support active verification against their respective APIs**." — [T1, raw README]

Entrópia-alapú szűrés a TruffleHogban **külön, opcionális réteg**, és a dokumentáció kifejezetten a **nem-ellenőrzött** találatokra ajánlja:

> "--filter-entropy=FILTER-ENTROPY  Filter unverified results with Shannon entropy. Start with 3.0." — [T1, raw README, CLI-kapcsoló leírás]

Vagyis a TruffleHogban az entrópia nem az elsődleges szűrő, hanem egy másodlagos zajszűrő azokra a találatokra, amelyeket nem sikerült (vagy nem is próbáltak) élőben ellenőrizni.

### 1.3 detect-secrets (Yelp) — plugin-rendszer: 27 beépített detektor, ebből 2 tisztán entrópia-alapú

A `detect-secrets scan --list-all-plugins` kimenete (hivatalos README-ből, szó szerint) **27 pluginet** sorol fel:

```
ArtifactoryDetector, AWSKeyDetector, AzureStorageKeyDetector, BasicAuthDetector,
CloudantDetector, DiscordBotTokenDetector, GitHubTokenDetector, GitLabTokenDetector,
Base64HighEntropyString, HexHighEntropyString, IbmCloudIamDetector, IbmCosHmacDetector,
IPPublicDetector, JwtTokenDetector, KeywordDetector, MailchimpDetector, NpmDetector,
OpenAIDetector, PrivateKeyDetector, PypiTokenDetector, SendGridDetector, SlackDetector,
SoftlayerDetector, SquareOAuthDetector, StripeDetector, TelegramBotTokenDetector,
TwilioKeyDetector
```
[T1, raw README]

Ebből **2 tisztán entrópia-alapú** (`Base64HighEntropyString`, `HexHighEntropyString`), a többi **regex/formátum-specifikus** az adott szolgáltatóra (AWS, Stripe, Slack stb.), plusz egy általános `KeywordDetector` (kulcsszó-heurisztika, pl. `password = "..."` minták).

### 1.4 GitHub secret scanning — 522 publikált szolgáltatói minta + 10 generikus + AI-alapú "generic" kategória

A hivatalos, élő "Supported secret scanning patterns" oldal (2026-09-15-i állapot, közvetlenül lekérve és tag-stripelve) a táblázat tetején explicit számot közöl:

> "Showing 522 of 522 patterns" — [T1, docs.github.com, nyers HTML lekérés]

Ezen felül **10 db "generic" (nem szolgáltatóhoz kötött) regex-mintát** sorol fel névvel és becsült precizitási szinttel (lásd 2. pont), pl. `rsa_private_key`, `openssh_private_key`, `postgres_connection_string`, `mongodb_connection_string` stb. — mindegyik "Regex-based" jelöléssel.

Emellett egy külön **AI-alapú kategória** is létezik, amely nem regex, hanem nyelvi modell:

> "AI-detected | Passwords and other unstructured secrets detected using AI models | AI-based | password" — [T1, docs.github.com, "Pattern categories" táblázat]

Vagyis a GitHub három rétegben dolgozik: (1) regex + partneri validáció "provider patterns" (522 minta), (2) regex-alapú "generic patterns" (10 minta, magas/közepes becsült precizitás), (3) AI/LLM-alapú "generic secret detection" a strukturálatlan jelszavakra (Copilot-modellel).

### Összegzés — módszertani spektrum

| Eszköz | Regex | Entrópia | Kulcsszó-előszűrés | Élő ellenőrzés | Publikált mintaszám |
|---|---|---|---|---|---|
| Gitleaks | igen, elsődleges | igen, 130/222 szabálynál | igen (generic-api-key) | nem beépített | **222** szabály |
| TruffleHog | igen, elsődleges | igen, csak nem-ellenőrzöttekre, opcionális | nem jellemző | igen, elsődleges erősség | **"over 800"** típus, **"over 700"** ellenőrizhető |
| detect-secrets | igen, 25/27 plugin | igen, 2/27 plugin | igen (KeywordDetector) | nem | **27** plugin |
| GitHub secret scanning | igen (provider+generic) | nincs dokumentált explicit entrópia-lépés a publikus doksiban | nem dokumentált explicit | igen ("validity checks") | **522** provider + **10** generic + AI-kategória |

---

## 2. Mennyire pontos ez — mért adattal

### 2.1 A kulcsforrás: ESEM 2023, lektorált tanulmány, névvel azonosítható korpusz

A legjobb — és gyakorlatilag egyetlen — **lektorált, nagymintás, független** (nem gyártói) mérés, amit találtunk: Setu Kumar Basak, Jamison Cox, Bradley Reaves, Laurie Williams: **"A Comparative Study of Software Secrets Reporting by Secret Detection Tools"**, elfogadva az **ESEM 2023** (International Symposium on Empirical Software Engineering and Measurement) technikai szekciójába, publikálva az IEEE Xplore-on (ieeexplore.org/document/10304853) és arXiv-on (2307.00714). [T1 — lektorált konferenciacikk]

**Korpusz és módszertan** (szó szerint):

> "Secrets: The dataset consists of 97,479 labeled plain-text secrets (labeled as true and false) extracted from 818 repositories. The secrets were manually labeled by the two authors of SecretBench. Among the 97,479 candidate secrets, 15,084 are true secrets. In addition, among the true secrets, 4,457 are unique." — [T1, ar5iv.labs.arxiv.org/html/2307.00714]

Tehát: **818 nyilvános GitHub-repó**, **97 479** kézzel címkézett jelölt-string, ebből **15 084 valódi** titok (4 457 egyedi). Kilenc eszközt hasonlítottak össze: 5 nyílt forráskódú (Gitleaks, TruffleHog, git-secrets, Repo-Supervisor, Whispers) és 4 kereskedelmi (GitHub Secret Scanner, SpectralOps, ggshield, "Commercial X" — a gyártó kérésére anonimizálva). A `detect-secrets`-et **kizárták** a vizsgálatból, mert nem tesz közzé sima szöveges titkot (5. kizárási kritérium: "Reports Plain Text Secret").

**Precizitás (precision) — a top három eszköz, szó szerint:**

> "The top three tools based on precision are: GitHub Secret Scanner (75%), Gitleaks (46%), and Commercial X (25%)... Among the nine tools, five tools have a precision score of less than 7%." — [T1]

**Visszahívás (recall) — a top három eszköz, szó szerint:**

> "Based on recall, we observe that Gitleaks is the top tool in both cases (Case 1: 86% and Case 2: 88%)... In addition, TruffleHog has the second-best recall in Case 1 (31%) and third-best in Case 2 (52%) though the precision is only 6%." — [T1]

**F1-pontszám:**

> "We observe that based on F1-score, the top three tools are Gitleaks (60%), GitHub Secret Scanner (48%), and Commercial X (32%)." — [T1]

**Fontos csapda a "GitHub Secret Scanner 75% precizitás" számban:** ugyanez az eszköz recall-ja mindössze **6%** —

> "Though GitHub Secret Scanner is the top tool based on precision, the recall score is low (6%), indicating the tool misses many secrets." — [T1]

Vagyis a magas precizitás nem technikai fölényt jelez, hanem azt, hogy a GitHub (ebben, 2023-as, tehát a jelenlegi 522-mintás katalógusnál szűkebb állapotában) csak jól ismert, szolgáltatóhoz kötött formátumokra keresett — kevesebb találat, kevesebb hibázási lehetőség is. (Lásd `ellentmondasok.md` — értelmezési csapda, nem forrásellentmondás.)

### 2.2 Fals pozitívok abszolút száma egy másodlagos, ugyanahhoz a laborhoz tartozó adathalmazból

A szerzők közzétették a nyers fals pozitív találatokat is egy külön adathalmazban, **FPSecretBench** néven (ugyanazon 818 repós korpuszon):

| Eszköz | Fals pozitív találatok száma (818 repó korpuszon) |
|---|---|
| git-secrets | 89 584 |
| **Gitleaks** | **24 885** |
| Repo-Supervisor | 177 658 |
| **TruffleHog** | **85 556** |
| Whispers | 414 068 |
| ggshield | 134 769 |
| SpectralOps | 1 543 217 |
| **GitHub-scanner** | **429** |
| Commercial X | 64 933 |

[T1 — github.com/setu1421/FPSecretBench README, ugyanazon kutatócsoport, ugyanazon ESEM 2023 tanulmány melléklete]

Ez konkrétan mutatja: egy naiv, teljes-repó regex+entrópia szkennelés (pl. SpectralOps, Whispers) **több százezer, akár 1,5 millió** fals pozitívot termelhet egyetlen 818 repós mintán; a szűkebb, csak ismert szolgáltatói formátumra szorítkozó GitHub-módszer 429-et.

### 2.3 A fals pozitívok és fals negatívok okai — kutatói minőségi elemzés (n=50 minta eszközönként)

A szerzők eszközönként **50 véletlen fals pozitívot** vizsgáltak kézzel:

> "Analysis of False Positives: Since we observed a high false positive rate by the tools, we inspected a random sample of 50 false positives from each tool to identify the types of false positive secrets." — [T1]

Az összefoglaló megállapítás szó szerint (ez a legfontosabb mondat a mi kérdésünk szempontjából):

> "Our manual analysis of reported secrets reveals that false positives are due to employing generic regular expressions and ineffective entropy calculation. In contrast, false negatives are due to faulty regular expressions, skipping specific file types, and insufficient rulesets." — [T1, absztrakt]

Konkrét, idézett fals pozitív példák:

> "the regex employed for the Stripe API key is `(?i)(sk|pk)_(test|live)_[0-9a-z]{10,32}`. However, the regex matches `sk_live_111111111111`, a dummy API key, and outputs as a Stripe API key." — [T1]

> "TruffleHog computes the entropy of `2b95710rD1e6287e69Z8f2E24373449d879b70c7601B3x9` and `ThisIsAReallyLongString` as 4.08 and 4.11 respectively, thus having higher entropy score for the latter... We also observed substantial instances of GitHub commit ids, such as `0e2b3d4e3dec5f38ae95f62519eb2736f73c0b`, outputted as secrets because of ineffective entropy calculation." — [T1]

**Ez a legerősebb bizonyíték arra, hogy az entrópia-alapú szűrés önmagában nem különbözteti meg megbízhatóan a valódi titkot egy ártalmatlan, de véletlenszerűnek tűnő stringtől (git-hash, camelCase változónév).**

### 2.4 Gyártói vs. mért pontossági állítások — külön kezelve

A GitHub saját blogján 2026-ban publikált egy fals pozitív csökkentésről szóló bejegyzést, LLM-alapú kontextuselemzéssel:

> "We evaluated this approach on hundreds of customer-confirmed false positive alerts. Our target was a 65% reduction. The result was 75.76%, exceeding that goal while maintaining strong detection performance." — [T2 — **gyártói blog, github.blog, NEM lektorált mérés**]

**Ezt explicit módon gyártói állításként kezeljük, nem mérésként**, mert: (a) a mintaszám csak "hundreds" (több száz), nincs pontos szám; (b) nincs közölve az abszolút fals pozitív *arány* sem előtte, sem utána — csak a relatív csökkenés; (c) "customer-confirmed" — nem világos, hogy ez reprezentatív mintavétel-e; (d) nincs független auditálás. A GitHub saját dokumentációja egyébként maga is elismeri, hogy az AI-alapú generikus felismerés megbízhatatlanabb, mint a szolgáltató-specifikus minták:

> "Since AI secret detection may generate more false positives than partner pattern detection, review the accuracy of each alert." — [T1, docs.github.com, "Responsible detection of generic secrets"]

A generikus (nem szolgáltatóhoz kötött) minták esetében a GitHub docs csak kvalitatív "Precision" címkéket ad (High/Medium), nem számot, és maga mondja ki, hogy ez becslés:

> "Precision levels are estimated based on the pattern type's typical false positive rates." — [T1, supported-secret-scanning-patterns]

---

## 3. Entrópia-alapú felismerés — küszöbök és viselkedésük

### 3.1 A három eszköz konkrét, forrásból igazolt küszöbei

| Eszköz | Karakterkészlet | Küszöb | Forrás |
|---|---|---|---|
| detect-secrets | Base64 | **4.5** | `--base64-limit`, "defaults to 4.5" [T1, forráskód: `detect_secrets/core/usage/plugins.py`] |
| detect-secrets | Hex | **3.0** | `--hex-limit`, "defaults to 3.0" [T1, ugyanott] |
| Gitleaks | `generic-api-key` szabály kifogott csoportja | **3.5** | `entropy = 3.5` [T1, `config/gitleaks.toml`] |
| Gitleaks | egyéb szabályok | **2 – 4** (szabályonként eltér) | [T1, `config/gitleaks.toml`, megfigyelt értékek] |
| TruffleHog | csak nem-ellenőrzött találatokra, opcionális | ajánlott kezdőérték **3.0** | "`--filter-entropy`... Start with 3.0." [T1, README] |

A `detect_secrets/plugins/high_entropy_strings.py` forrása azt is rögzíti, hogy az elméleti tartomány 0–8 bit/karakter:

> "if limit < 0 or limit > 8: raise ValueError('The limit set for HighEntropyStrings must be between 0.0 and 8.0')" — [T1, forráskód]

### 3.2 A küszöb eredete — nem statisztikai levezetés, hanem próba-szerencse

A gitleaks 3.5-ös küszöbének eredetét a készítő maga írja le, és ez fontos módszertani figyelmeztetés:

> "So what's a good value for the entropy threshold? First we should ask the questions, what are the theoretical maximum and minimum entropies? The theoretical maximum entropy for a secret captured by the generic rule's regular expression is 5.83... The theoretical minimum entropy is 0... After some trial and error and feedback from the Gitleaks community we landed on 3.5." — [T2, gitleaks maintainer blog, hivatalos README/config által linkelve mint magyarázat]

Vagyis a bevett küszöbérték **nem formális statisztikai vizsgálat eredménye**, hanem közösségi próbálgatásé. Ez összhangban van a 2.3 pontban idézett lektorált megállapítással ("ineffective entropy calculation").

### 3.3 Konkrét demonstráció: hétköznapi szöveg is átlépheti a küszöböt

A gitleaks készítőjének saját példája (szó szerint):

> "Entropy by itself isn't a very good heuristic for determining whether something is a secret or not. Consider this line of Go code: `if err := readUntilSafeBoundary(reader, n, maxPeekSize, peekBuf); err != nil`. Despite not containing anything that looks like a secret, this line has an entropy of **4.24** bits per character which is pretty high." — [T2, gitleaks maintainer blog]

> "myServiceToken = 'extremelySecret123' [entropy 3.3, a küszöb alatt, kiszűrve] ... myServiceToken = '8dyfuiRyq=vVc3RRr_edRk-fK__JItpZ' [entropy 4.11, a küszöb fölött, jelezve]" — [T2, ugyanott, saját összefoglalás a szerző számpéldáiból]

### 3.4 Magyar szöveg és base64-szerű azonosítók — **nincs publikált mérés**

**Ezt explicit hiányként rögzítjük** (lásd részletesen `hianyok.md` is): nem találtunk sem lektorált, sem gyártói publikációt, amely kifejezetten magyar nyelvű szöveg vagy magyar ékezetes azonosítók Shannon-entrópia-viselkedését vizsgálná secret-scanning kontextusban. A fenti eszközök dokumentációja és a lektorált tanulmány is kizárólag angol nyelvű/kódmintákkal illusztrál.

**Saját, illusztratív számítás** (nem forrás, nem mérés — csak azért közöljük, hogy megmutassuk a probléma irányát; módszer: Python `collections.Counter` alapú, egyetlen mintán számolt karakterenkénti Shannon-entrópia, `H = -Σ p(c)·log2(p(c))`, nem korpusz-alapú, n=1 mintánként):

| Minta | Hossz (karakter) | H (bit/karakter) |
|---|---|---|
| Magyar mondat, ékezet nélkül ("Az easter memory system markdown fájlokban...") | 103 | **4.11** |
| Ugyanaz, ékezetekkel, UTF-8 bájtszinten mérve | 106 kar / 119 bájt | **4.48** (bájt) |
| Magyar camelCase azonosító ("ÜgyfélAzonosítóKódja2026") | 24 | **4.34** |
| Valódi véletlen 32 bájtos base64 kulcs | 44 | 4.73 |
| Valódi véletlen 32 bájtos hex kulcs | 64 | 3.88 |
| Szintetikus "AWS-szerű" kulcs (AKIA+16 karakter) | 20 | 3.75 |
| A gitleaks-blog angol kódsora (idézve fent) | 76 | 4.35 (saját újraszámolással, illusztráció) |

**Ez a saját számítás azt sugallja** (hipotézisként, nem bizonyítékként), hogy egy átlagos magyar mondat vagy egy ékezetes magyar azonosító karakterenkénti Shannon-entrópiája **ugyanabban a 4.0–4.5 bit/karakter tartományban** mozoghat, mint a valódi, véletlen base64/hex kulcsoké — sőt, a szintetikus "AWS-szerű" kulcsnál (3.75) magasabb is lehet. Ez megerősítené (de nem bizonyítja korpusz-szinten) a 2.3 pontban idézett lektorált megfigyelést: a nyers Shannon-entrópia önmagában nem alkalmas nyelv-független megkülönböztetésre. **Hangsúlyozzuk: ez a táblázat a mi saját, egyetlen mintán végzett számításunk, nem publikált kutatás — kifejezetten azért szerepeltetjük, hogy jelöljük az adathiányt, nem azért, hogy pótoljuk azt.**

---

## 4. "Ellenőrzött titok" (verified secret) mint fogalom

### 4.1 GitHub — "validity checks", három állapot

> "Validity checks, a feature of secret scanning, verify whether a detected secret is still active and could be exploited. This helps you prioritize remediation by focusing first on secrets that are confirmed to be active." — [T1, docs.github.com/.../validity-checks]

> "GitHub displays the validation status of the secret in the alert view, so you can see if the secret is **active**, **inactive**, or if the validation status is **unknown**." — [T1, ugyanott]

> "Some secrets require more than the token itself to confirm whether they are active. For these secrets, GitHub will combine the token with additional contextual information, such as a host or URL, to check the secret's validity." — [T1, ugyanott]

### 4.2 TruffleHog — "verified / unverified / unknown", API-hívással

> "For every potential credential that is detected, we've painstakingly implemented programmatic verification against the API that we think it belongs to. Verification eliminates false positives and provides three result statuses: **verified**: Credential confirmed as valid and active by API testing; **unverified**: Credential detected but not confirmed valid (may be invalid, expired, or verification disabled); **unknown**: Verification attempted but failed due to errors, such as a network or API failure." — [T1, raw README]

Konkrét mechanizmus-példa:

> "For example, the AWS credential detector performs a `GetCallerIdentity` API call against the AWS API to verify if an AWS credential is active." — [T1, README, és megerősítve az ESEM 2023 tanulmányban is: "TruffleHog's AWS credential detector performs a 'GetCallerIdentity' API call against the AWS API to verify if the credential is active." — T1, második, független forrás]

Privát kulcsok esetén a TruffleHog más mechanizmust használ (nem API-hívást, hanem adatbázis-egyeztetést milliárdnyi ismert TLS/SSH nyilvános kulccsal):

> "A verified result means TruffleHog confirmed the credential is valid by testing it against the service's API. For private keys, we've confirmed the key can be used live for SSH or SSL authentication." — [T1, README FAQ]

> "We compiled a database of billions of TLS and SSH public keys that we know pair with sensitive private keys. Driftwood will take a given Private Key, extract its public key component, and then post the public key to our database to see whether it pairs with a known sensitive key." — [T2, trufflesecurity.com/blog/driftwood, a tool szerzőjének (Dylan Ayrey) blogja]

Anekdotikus (nem statisztikai) illusztráció ugyanebből a bejegyzésből a szűretlen módszer zajára:

> "Running TruffleHog on the Twitter GitHub organization returns about 25 Private Keys, and the Netflix Organization returns about 4811 Private Keys. Not only is this a tremendous amount of code to review, the surrounding context doesn't always give us the answer." — [T2, uo.]

### 4.3 Fals pozitív arány a két üzemmódban — **külön mérve**, lektorált forrásból

Ez a legfontosabb konkrét szám a teljes kutatáshoz, mert pontosan a "gyanús minta" vs. "ellenőrzött, élő kulcs" kettősséget méri, ugyanazon eszközön (TruffleHog), ugyanazon korpuszon (SecretBench, 818 repó):

> "Tool vendors should correctly employ secret verification by collaborating with API vendors. We find that tools verify the found secrets with the API endpoints (F4). As a result, tools show relatively higher precision by reducing false positives. **For example, before the verification option was enabled (`--only-verified`), TruffleHog's precision was 6%, outputting almost 100K alerts for our benchmark. In contrast, the precision changed to 90% when the verification was enabled and outputted only 611 secrets.** However, verification methods are not 100% correct as we observe **10% false positives**. For example, the tool tagged dummy server URLs such as 'http://dyn.example.com:password@dyn.dns.he.net' as secrets." — [T1, ESEM 2023, lektorált]

Összefoglalva, ugyanazon eszközön, ugyanazon 818 repós korpuszon:

| Üzemmód | Precizitás | Implikált fals pozitív arány | Riasztások száma |
|---|---|---|---|
| Nem ellenőrzött (`--regex --entropy`, minden találat) | **6%** | **~94%** | "almost 100K" (≈100 000) |
| Ellenőrzött (`--only-verified`, élő API-hívással) | **90%** | **~10%** | 611 |

Ez kb. **15-szörös precizitás-javulást** jelent az élő ellenőrzéssel, de a fals pozitív arány **nem nulla még ellenőrzött módban sem** (10%) — konkrét okot is adnak rá (a "verifikáció" néha csak azt igazolja, hogy egy URL/string szintaktikailag helyes, nem azt, hogy valódi, aktív hitelesítő adat).

A GitHub partnerprogram mérete (a tanulmány idején, 2023-ban) is dokumentált, ami kontextust ad a "provider patterns" lefedettségéhez:

> "We also find that GitHub has a secret scanning partner program where API vendors can join in scanning their API keys and tokens in GitHub repositories... However, only 66 API vendors have joined the program." — [T1, ESEM 2023 — **ez 2023-as állapot**; a jelenlegi (2026) hivatalos GitHub-oldal 522 mintát sorol fel, ami jóval szélesebb lefedettséget jelez, de a partnerek pontos száma a jelenlegi doksiban nincs egy helyen kimondva — lásd `hianyok.md`]

---

## 5. Blokkolás vagy jelzés? A valódi rendszerek gyakorlata

### 5.1 GitHub — két külön mechanizmus: utólagos jelzés vs. előzetes blokkolás

A GitHub **kétféle** választ ad ugyanarra a felismerésre, és ez maga is fontos tanulság:

**(a) "Secret scanning" (alap, jelzés-alapú):** utólag fut le, riasztást (alert) generál, **nem akadályozza meg** a push-t.

**(b) "Push protection" (opcionális, blokkolás-alapú):**

> "Push protection is a secret scanning feature designed to prevent hardcoded credentials, such as secrets or tokens, from ever being pushed to your repository. Rather than alerting you to credential leaks after the fact, push protection **blocks pushes that contain secrets before they reach your repository**." — [T1, docs.github.com/.../push-protection, concept oldal]

> "When push protection detects a potential secret during a push attempt, it will **block the push** and provide a detailed message explaining the reason for the block." — [T1, ugyanott]

### 5.2 A bypass (megkerülés) mechanizmus — miért engedik meg egyáltalán

Ez a kutatás egyik legfontosabb találata: a GitHub **explicit módon**, dokumentált indoklással engedi meg a blokkolás megkerülését, éppen a fals pozitívok miatt:

> "**Bypass functionality for flexibility**: For cases where **false positives occur** or when certain patterns are necessary, you can bypass push protection for users, and designated users can use the delegated bypass feature to bypass push protection for repositories... **This provides flexibility without compromising overall security.**" — [T1, docs.github.com/.../push-protection, "Benefits of push protection" szakasz — ez a hivatalos, kimondott indoklás]

A megkerülés **nem néma** — minden esetben nyomot hagy:

> "For push protection for repositories, by default, anyone with write access to the repository can bypass push protection by specifying a bypass reason. When a contributor bypasses a push protection block, GitHub: Creates an alert in the Security and quality tab...; Adds the bypass event to the audit log; Sends an email alert to personal account, organization, and enterprise owners, security managers, and repository administrators who are watching the repository, with a link to the secret and the reason it was allowed." — [T1, ugyanott]

A megkerülésnek **három, kényszerűen megnevezendő oka** lehet, mindegyikhez más riasztás-állapot tartozik:

> "Bypass reason → Alert behavior: 'It's used in tests' → GitHub creates a closed alert, resolved as 'used in tests'. 'It's a false positive' → GitHub creates a closed alert, resolved as 'false positive'. 'I'll fix it later' → GitHub creates an open alert." — [T1, ugyanott, táblázat]

> "You are required to specify a reason for bypassing push protection if the repository has secret scanning enabled." — [T1, push-protection-on-the-command-line]

Ezt egy másik hivatalos oldal (CLI-specifikus útmutató) is megerősíti, függetlenül a fenti concept-oldaltól:

> "If the secret is only used in tests and poses no threat, click **It's used in tests**. If the detected string is not a secret, click **It's a false positive**. If the secret is real but you intend to fix it later, click **I'll fix it later**." — [T1, docs.github.com/.../push-protection-on-the-command-line — második, független dokumentum-oldal, ugyanaz a tartalom más megfogalmazásban, tehát belső konzisztencia]

Nagyobb szervezetek szigoríthatnak: a "delegated bypass" funkcióval korlátozható, ki kaphat megkerülési jogot, illetve ki kérhet engedélyt eseti megkerülésre ("bypass requests" — a kérést jóváhagyás vagy elutasítás követi, e-mailes értesítéssel).

### 5.3 detect-secrets — pre-commit hook, blokkoló, de a fejlesztők maguk is relativizálják

A detect-secrets `--baseline` + pre-commit hook kombinációja **blokkol** (a commit nem megy át, ha új, a baseline-ban nem szereplő titok-gyanús string jelenik meg), de a saját dokumentáció explicit korlátozza a bizalmat ebbe:

> "This is not meant to be a sure-fire solution to prevent secrets from entering the codebase. Only proper developer education can truly do that. This pre-commit hook merely implements several heuristics to try and prevent obvious cases of committing secrets." — [T1, raw README]

Ismert, dokumentált vakfoltok:

> "Things That Won't Be Prevented: Multi-line secrets; Default passwords that don't trigger the `KeywordDetector` (e.g. `login = 'hunter2'`)" — [T1, ugyanott]

### 5.4 Gitleaks — nem tartalmaz beépített blokkoló/CI-kapu logikát a core eszközben

A gitleaks önmagában egy scanner (kimeneti riasztás/exit code), a blokkolás/kapu-logika a CI-integrációra van bízva (pl. a CI script bukik, ha nem-nulla exit code-ot ad vissza) — a hivatalos README ezt implicit módon a CI-integrációs mintákban mutatja be, nem önálló "push protection"-ként.

---

## 6. Mi a teendő, ha a titok már bekerült? Törlés vs. csere (rotate)

### 6.1 GitHub hivatalos állásfoglalása — kétszer, két különböző dokumentumban, egybehangzóan

**Első hely** ("About secret scanning" concept oldal):

> "When you receive an alert, **rotate the affected credential immediately** to prevent unauthorized access. While you can also remove secrets from your Git history, **this is time-intensive and often unnecessary if you've already revoked the credential**." — [T1, docs.github.com/en/code-security/concepts/secret-security/secret-scanning]

**Második, független hely** ("Removing sensitive data from a repository" — ez egy teljesen más szekció, authentication/account-biztonsági dokumentáció, nem a secret-scanning termékdoksi):

> "It is important to note that if the sensitive data you need to remove is a secret (e.g. password/token/credential), as is often the case, then as a first step you need to **revoke and/or rotate that secret**. Once the secret is revoked or rotated, it can no longer be used for access, and **that may be sufficient to solve your problem. Going through the extra steps to rewrite the history and remove the secret may not be warranted.**" — [T1, docs.github.com/en/authentication/.../removing-sensitive-data-from-a-repository]

Ugyanez a dokumentum azt is kimondja, hogy a GitHub támogatói csapata is a rotálást tekinti az elsődleges megoldásnak:

> "GitHub Support won't remove non-sensitive data, and will only assist in the removal of sensitive data in cases where **we determine that the risk can't be mitigated by rotating affected credentials**." — [T1, ugyanott]

**Ez két, tartalmilag és elhelyezkedésében is független GitHub-dokumentum, amely ugyanarra a következtetésre jut: a kulcscsere elsődleges és gyakran önmagában elégséges válasz; a történet-átírás másodlagos, opcionális lépés.**

### 6.2 Miért nem elég önmagában a törlés — technikai indoklás

A "Removing sensitive data" dokumentum részletesen leírja, hogy még egy sikeres history-átírás (git-filter-repo) esetén is:

> "If you only rewrite your history and force push it, the commits with sensitive data may still be accessible elsewhere" — [T1, ugyanott — pl. más fejlesztők helyi klónjaiban, forkjaiban, cache-elt nézetekben]

> "Leading others directly to the sensitive data: Git was designed with cryptographic checks built into commit identifiers... it means that expunging sensitive data is a very involved process of coordination; it further means that when you do modify history, clueful users with an existing clone will notice the history divergence and can use it to quickly and easily find the sensitive data still in their clone that you removed from the central repository." — [T1, ugyanott]

Ez különösen releváns a mi rendszerünk (`easter-memory-system`) szempontjából, mert ott **nincs git**, tehát nincs "más klónok" probléma — de a lényegi tanulság (a bekerült adat cseréje logikailag megelőzi/pótolja a törlést) ugyanúgy érvényes.

### 6.3 Független (nem GitHub) megerősítés: HashiCorp Well-Architected Framework, NIST-hivatkozással

> "Once you detect a leaked secret, immediate remediation is critical... The remediation process involves forming an incident response team, **following NIST guidelines**, and systematically removing secrets from all locations including version control, documentation, and backups." — [T2, developer.hashicorp.com, Well-Architected Framework]

> "**Rotate the compromised secret immediately**: Assume the secret is already compromised. Generate a new secret and update it... before modifying any code." — [T2, ugyanott]

> "Leaked secrets in source code require **immediate rotation followed by systematic removal** from version control history. **Simply deleting the file or line does not remove the secret.** It remains accessible in Git history until you explicitly purge it." — [T2, ugyanott]

Megjegyzendő: itt a sorrend és a hangsúly kicsit **más**, mint a GitHub-doksiban — lásd `ellentmondasok.md` — a HashiCorp mindkét lépést (rotate ÉS history-purge) szükségesnek tartja, míg a GitHub megengedőbb ("may not be warranted").

### 6.4 OWASP Secrets Management Cheat Sheet — általános rotációs elv

> "You should regularly rotate secrets so that any stolen credentials will only work for a short time. Regular rotation will also reduce the tendency for users to fall back to bad habits such as reusing credentials." — [T1, cheatsheetseries.owasp.org — hivatalos OWASP-dokumentum]

> "Deletion: Secrets revoked/rotated must be removed from the exposed system immediately, including secrets discovered in code or logs." — [T1, ugyanott — itt is a rotálás/visszavonás szerepel elsőként, a törlés másodikként]

### 6.5 Összefoglaló válasz Q6-ra

**Nem elég törölni — a kulcsot/jelszót minden hivatalos forrás szerint cserélni (rotálni) vagy visszavonni kell**, és ez az elsődleges, azonnali lépés. A history-ból való törlés/átírás **kiegészítő, másodlagos** védelem, amelynek szükségességét maga a GitHub is relativizálja ("often unnecessary if you've already revoked the credential"), míg más, NIST-alapú keretrendszerek (HashiCorp) mindkét lépést előírják defense-in-depth elvként. **Egyik forrás sem állítja, hogy a törlés önmagában, csere nélkül elegendő volna.**



---

# sq02 — Mit szűrnek a valódi agent-memória rendszerek íráskor

# sq02 — Mit szűrnek a valódi agent-memória rendszerek íráskor

**Kampány:** tartalom-kapu | **Alkérdés:** sq02
**Kontextus:** `easter-memory-system` — markdown-fájlokból álló agent-memória, külső agentek MCP-n írnak bele, nincs szöveggeneráló modell a rendszerben, csak beágyazó. A kérdés: van-e bárhol a piacon/gyakorlatban **tartalom-kapu íráskor**, és ha igen, milyen (LLM-alapú vagy determinisztikus)?

Tier-jelölés: **T1** = hivatalos dokumentáció / forráskód / preprint-akadémiai; **T2** = megbízható gyártói/másodlagos elemzés; **T3** = fórum, blog, egyéni anekdota, közösségi GitHub issue.

---

## 1. Rendszerenkénti áttekintés — van-e tartalom-kapu íráskor?

### 1.1 basic-memory (basicmachines-co)

A README.md-ben (fő projektdokumentáció) **egyetlen egyszer sem** szerepel a "security" szó — ezt közvetlenül ellenőriztük (`grep -i security` nulla találat a teljes fájlon). A projekt saját `SECURITY.md`-je (GitHub, T1) explicit módon **nem a tartalomról**, hanem a fájlrendszer-hozzáférésről szól:

> "Filesystem-touching tools validate paths against the configured project root with `validate_project_path()`... Path traversal attempts such as `../../etc/passwd` are blocked at this layer." — [SECURITY.md](https://raw.githubusercontent.com/basicmachines-co/basic-memory/main/SECURITY.md) (T1)

> "Basic Memory does not execute note content as code. Notes are returned as data to the LLM." — uo. (T1)

> "Basic Memory is designed for single-user local knowledge bases and does not implement access controls between operating-system users." — uo. (T1)

**Fontos pontosítás:** a kutatási feladat kiindulópontja szerint a basic-memory állítólag szó szerint kimondja magáról: *"It is NOT a security boundary."* Ezt a pontos szöveget **nem sikerült megtalálni** sem a README.md-ben, sem a SECURITY.md-ben, sem a docs.basicmemory.com technikai-információ oldalán (mindhármat közvetlenül ellenőriztük, curl-lal / nyers HTML-ként). A docs.basicmemory.com sitemapja is üresen jött vissza (JS-renderelt oldal). Lásd `hianyok.md` és `ellentmondasok.md` — a funkcionálisan azonos állítás (a helyi felhasználó megbízhatónak számít, a jegyzet-tartalom nem kerül osztályozásra) **igen** megvan, de a szó szerinti idézet nem igazolható.

**Következtetés:** basic-memory-ben nincs semmilyen tartalom-osztályozás, titokszűrés vagy tiltólista íráskor — csak elérési út-validáció. Ez egy dokumentáltan és tudatosan vállalt hiány (nem véletlen kihagyás), a projekt saját threat modelljében rögzítve.

### 1.2 mem0

A hivatalos dokumentáció (docs.mem0.ai, T1) egyetlen "mit írjunk be" mechanizmust kínál: a **Custom Instructions** (korábban `custom_fact_extraction_prompt`) funkciót. Ez explicit módon **LLM-közvetített**, nem determinisztikus:

> "Custom instructions let you decide exactly which facts Mem0 records from a conversation. Define a focused prompt, give a few examples, and Mem0 will add only the memories that match your use case." — [Custom Instructions docs](https://docs.mem0.ai/open-source/features/custom-fact-extraction-prompt) (T1)

Ez a mechanizmus egy háttér-LLM-nek ad egy kivonatoló promptot ("Please only extract entities containing..."), amely eldönti, mi kerüljön be — pontosan az a fajta megoldás, amit a feladatleírás kizár ("nincs szöveggeneráló modell... bármilyen megoldás, ami a rendszer eldönti/átfogalmazza, nálunk kivitelezhetetlen").

A mem0 saját blogja (2026.02.11., T2, gyártói forrás, a cégalapító Deshraj Yadav jegyzi) elismeri a problémát általánosan, és véd(elmi rétegeket ajánl: "input sanitization, memory isolation per user/session, cryptographic integrity checks, ... continuous monitoring" — de ezek fejlesztői feladatként, nem beépített, automatikus kapuként vannak leírva. [mem0.ai/blog/ai-memory-security-best-practices](https://mem0.ai/blog/ai-memory-security-best-practices) (T2)

**Következtetés:** mem0 egyetlen tartalomszűrő mechanizmusa LLM-alapú; nincs beépített, determinisztikus titok-/PII-szűrés az `add()` hívásnál. Nem található kifejezett "nem vagyunk biztonsági határ" nyilatkozat sem a dokumentációban, sem az adatvédelmi szabályzatban (kifejezetten kerestük).

### 1.3 Zep / Graphiti

A hivatalos overview-oldal (help.getzep.com/graphiti/getting-started/overview, T1) és a GitHub README (raw.githubusercontent.com/getzep/graphiti/main/README.md, T1) **egyszer sem** említ tartalom-validációt, szűrést, moderációt vagy rosszindulatú input elleni védelmet — közvetlenül kerestük ezeket a kulcsszavakat (`valid|filter|sanit|security|moderat|malicious`), nulla releváns találat a tartalom-kapu témában. Az egyetlen "security" említés egy funkció-összehasonlító táblázatban van, ami a **fizetős, zárt Zep platform** javára szól a nyílt forráskódú Graphiti-hoz képest:

> "Enterprise features: SLAs, support, security guarantees" (csak a Zep platformnál, nem a Graphiti-nál) — [GitHub README](https://raw.githubusercontent.com/getzep/graphiti/main/README.md) (T1)

A Graphiti saját `SECURITY.md`-je (T1) egy generikus sebezhetőség-bejelentési sablon, tartalom-kapuról nem szól.

**Következtetés:** a nyílt forráskódú Graphiti-ban nincs dokumentált tartalom-kapu íráskor. A kereskedelmi Zep platform "biztonsági garanciákat" ígér, de ezek tartalma nyilvánosan nincs specifikálva — ez inkább hiány, mint megerősített funkció.

### 1.4 Letta (MemGPT)

A hivatalos memory-blocks dokumentáció (docs.letta.com, T1) szerint az egyetlen íráskor érvényesített korlát egy **karakteres méretkorlát** (`limit` mező blokkonként, pl. 5000 karakter a példákban) — se PII-szűrés, se titok-detekció, se tartalom-osztályozás nincs dokumentálva.

Ezt megerősíti egy nyitott GitHub issue a hivatalos letta-ai/letta repóban (T3, közösségi forrás, de a fenntartói repóban):

> "Letta presently lacks built-in defenses against memory poisoning as defined by OWASP ASI06 standards" — [Issue #3342](https://github.com/letta-ai/letta/issues/3342), "Security: OWASP Agent Memory Guard for memory poisoning defense (ASI06)", állapot: nyitott.

Az issue kérése pontosan a hiányzó funkciókat sorolja fel: "Write validation — schema conformance, authorization checks, content scanning". Egy másik, lezárt issue (#3320, "Memory governance — policy enforcement for stateful agent memory", 2026.04.20.) ugyanezt a hiányt írja körül, Microsoft Agent Governance Toolkit integrációt javasolva.

**Következtetés:** Letta-ban nincs beépített, determinisztikus tartalom-kapu — ezt a projekt saját issue-trackere is megerősíti mint ismert, nyitott hiányt.

### 1.5 Anthropic memory tool (Claude API)

Ez a legpontosabban dokumentált eset. A hivatalos dokumentáció (platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool, T1) "Security considerations" szakasza **szó szerint** kimondja:

> "Your application executes every file operation Claude requests, so these safeguards are your responsibility: **Sensitive information** — Claude usually refuses to write sensitive information to memory files. For stronger guarantees, add validation that strips sensitive data before your handler writes the file." (T1)

Ez pontosan a feladat lényegét ragadja meg:
- A beépített "kapu" **modellítélet** ("Claude *usually* refuses") — tehát nem determinisztikus, hanem valószínűségi, és a modell megítélésén múlik.
- Anthropic explicit módon **a fejlesztőre hárítja** egy erősebb, determinisztikus szűrő hozzáadását.
- Ugyanez a szakasz további, kifejezetten a fejlesztő felelősségébe utalt tételeket sorol: fájlméret-korlátozás ("Track memory file sizes and cap how large a file can grow"), memória-lejárat ("Periodically delete memory files that haven't been accessed"), és — egyetlen **kötelezőként** megfogalmazott elemként — az útvonal-bejárás elleni védelem: "Your implementation **must** validate every path in every command to prevent directory traversal attacks."

**Következtetés:** Anthropic saját memory tool-ja explicit módon két rétegre bontja a védelmet: (a) puha, modell-alapú tartalomszűrés ("usually refuses"), amit ő biztosít; (b) kemény, determinisztikus védelem (útvonal, méret, lejárat, "erősebb garanciákhoz" tartalom-validáció), amit a hívó alkalmazásnak kell megvalósítania. Ez a legközvetlenebb bizonyíték arra, hogy egy vezető gyártó saját magától **nem** vár el (és nem is ígér) determinisztikus tartalom-kaput a memória-írásnál.

### 1.6 Claude Code saját memóriája (CLAUDE.md / auto-memory / MEMORY.md)

A hivatalos "How Claude remembers your project" dokumentáció (docs.claude.com/code.claude.com, T1) az auto-memory mechanikáját írja le, de a lekért szövegben **nem szerepel** semmilyen tartalom-moderációs, titok- vagy PII-szűrési utalás (kifejezetten kerestük: `sensitive|secur|filter|secret|PII|malicious|sanit` — a találatok mind szervezeti/rules-fájl kontextusban voltak, pl. "security.md" mint felhasználói szabályfájl neve, nem a rendszer saját tartalom-kapuja).

Ezt egy konkrét, dokumentált biztonsági kutatás (lásd 2. és a `megallapitasok.md` incidens-szakasza, Cisco "MemoryTrap") empirikusan igazolja: a vizsgált Claude Code verzióban a MEMORY.md fájlok első 200 sora **tartalom-vizsgálat nélkül** került be közvetlenül a rendszerpromptba, "magas tekintélyű" utasításként kezelve. Anthropic javítása (v2.1.50) nem tartalom-osztályozót adott hozzá, hanem **strukturálisan csökkentette a memória tekintélyét** (kivette a rendszerpromptból).

Egy független, nem-hivatalos blogbejegyzés (serendb.com, 2026.04.09., **T3**, egyetlen szerző, nem gyártói megerősítésű) azt állítja, hogy helyi Claude Code memória- és session-fájlokban talált visszamaradt titkokat (API-kulcs-nevek, tokenek) — ez konzisztens a mintázattal, de vendor által nem megerősített, egyedi megfigyelés.

**Következtetés:** Claude Code saját auto-memory rendszerében sem dokumentált, sem (a MemoryTrap-eset alapján) a gyakorlatban megvalósított tartalom-osztályozás nem volt jelen íráskor a vizsgált időpontban; a javítás architekturális (tekintély-csökkentés), nem tartalom-szűrő jellegű volt.

### 1.7 OpenAI / ChatGPT memória

Az OpenAI hivatalos bejelentő blogja (WebFetch-csel kérdezve le, mert a curl 403-at kapott Cloudflare-védelem miatt — lásd `linkek.md`) tartalmazza az egyetlen explicit tartalom-vezérlési nyilatkozatot:

> "We're taking steps to assess and mitigate biases, and steer ChatGPT away from proactively remembering sensitive information, like your health details - unless you explicitly ask it to." — [openai.com/index/memory-and-new-controls-for-chatgpt](https://openai.com/index/memory-and-new-controls-for-chatgpt/) (T1, WebFetch)

Ismét: "steer away" — tendencia, nem kemény szabály. A hivatalos Memory FAQ (help.openai.com, T1, WebFetch) megerősíti a puha jelleget:

> "Sensitive information may appear in memory if you share it with ChatGPT." (T1)

Az egyetlen **kemény, determinisztikus** szabály, amit találtunk, nem tartalom-szintű, hanem egész funkció ki/bekapcsolása szabályozott környezetekben:

> "This feature is not covered under your BAA. PHI should not be entered when using this feature" — és emiatt "improved memory is disabled by default" ChatGPT Healthcare / Enterprise Regulated Workspace esetén. (T1)

**Következtetés:** OpenAI-nál is a minta ismétlődik — a tartalom-szintű szűrés modell-alapú tendencia ("steer away"), a kemény szabály csak funkció-szintű kapcsoló, nem tartalom-osztályozó.

---

## 2. OWASP ASI06 — Memory & Context Poisoning

### 2.1 Hivatalos, szó szerinti idézetek (T1, genai.owasp.org)

A hivatalos bejelentő blogból (2025.12.09.):

> "Memory poisoning reshaped behaviour long after the initial interaction (ASI06 – Memory & Context Poisoning, e.g Gemini Memory Attack)." — [genai.owasp.org bejelentés](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/) (T1)

Az ASI06-tétel hivatalos felelősétől (Idan Habler, Cisco, "ASI Core Team and ASI06 Entry Lead"), a hivatalos OWASP GenAI Security Project blogon (2026.05.13.):

> "Agentic systems do not just respond in the moment. They retain context, reuse memory, and rely on persistent state to guide future reasoning and actions. That is what makes them useful. It is also what makes them vulnerable." — [genai.owasp.org: Memory Is a Feature. It Is Also an Attack Surface](https://genai.owasp.org/2026/05/13/memory-is-a-feature-it-is-also-an-attack-surface/) (T1)

> "The issue is not just that the model saw something malicious once. The issue is persistence. The corrupted context remains available, continues to circulate, and can shape future planning, tool use, and behavior." — uo. (T1)

### 2.2 Módszertani megjegyzés — amit NEM találtunk

A magát az ASI06-tételt formálisan felépítő (definíció / támadási vektorok / konkrét ajánlott kontrollok listája) hivatalos katalógus-oldalt **nem sikerült elérni** közvetlen, indexelhető HTML- vagy PDF-formában. A genai.owasp.org több valószínű URL-mintáját próbáltuk (`/asi06`, `/ASI06`, `/top10/asi06`, `/llmrisk/asi06-memory-context-poisoning`, `/asi06-memory-and-context-poisoning` — mind 404). Ez **"nem találtuk meg"**, nem **"nincs"**: a tétel léte és tartalma számos független forrásban (lásd lentebb) konzisztensen, egymást megerősítve szerepel, csak a hivatalos "törzsszöveg" közvetlen elérése nem sikerült ebben a kutatásban.

### 2.3 Háromszorosan megerősített, de csak másodkézből idézett ajánlott védekezés

Három egymástól független, az OWASP-taxonómiát felhasználó forrás (Modulos governance guide, DeepTeam red-teaming keretrendszer docs, Vectorize.io cikk) egymással konzisztens tartalmat ad vissza az ASI06-ra, de mindegyik **a saját szavaival parafrazálja**, nem szó szerint idézi az OWASP-szöveget:

- Modulos (T2): "persistent memory, retrieval stores, or session context an agent depends on is shaped by an adversary so that later steps in the plan ... execute under attacker-controlled assumptions... Governance should require provenance metadata on every memory write, tenancy separation, deliberate forgetting windows, and periodic evaluation against ground truth." [docs.modulos.ai](https://docs.modulos.ai/frameworks/owasp-top-10-agentic) (T2)
- DeepTeam (T2): "Memory & Context Poisoning involves injection or leakage of agent memory or contextual state that influences future reasoning or actions... Implement memory validation, integrity checks, and periodic memory audits." [trydeepteam.com](https://www.trydeepteam.com/docs/frameworks-owasp-top-10-for-agentic-applications) (T2)
- Vectorize (T2), az OWASP öt-rétegű kontroll-készletét összegezve: (1) Input Moderation with Trust Scoring — "Every retain operation passes through a policy that evaluates the content against detectors for prompt injection markers, credential and PII leakage, protected-key modifications, size anomalies, and encoded-payload smuggling"; (2) Memory Sanitization with Provenance Tracking; (3) Trust-Aware Retrieval (a visszakeresés forrás-megbízhatóság szerint súlyoz). [vectorize.io/articles/owasp-asi06](https://vectorize.io/articles/owasp-asi06) (T2)

Ez a hármas megerősítés (**T2 szinten**, nem T1) megbízhatóan körülírja az ASI06 tartalmát, de a `keresesek.md`-ben rögzített módon a szó szerinti hivatalos szöveghez nem jutottunk el.

### 2.4 Mért gyakorisági adatok — memória-mérgezésre specifikusan

**Elsődleges (T1) akadémiai eredmények:**

- **MINJA** (Dong et al., arXiv:2503.03704, "Memory Injection Attacks on LLM Agents via Query-Only Interaction") — az absztrakt (közvetlenül lekérve, T1) megerősíti a támadás mechanizmusát ("the attacker injects malicious records into the memory bank by only interacting with the agent via queries and output observations... enables any user to influence agent memory"), de konkrét számot az absztrakt maga nem közöl. A konkrét számokat egy másodlagos forrás (mem0 blog, T2) tulajdonítja a tanulmánynak: **"over 95% injection success rate and 70% attack success rate"** GPT-4o-mini, Gemini-2.0-Flash és Llama-3.1-8B agenseken. Ezt a konkrét százalékot **nem sikerült szó szerint visszaigazolni magában az arXiv-absztraktban** — egy szint áttételes idézet (T1 → T2 lánc).
- **AgentPoison** (Chen et al., NeurIPS 2024, arXiv:2407.12784) — az absztrakt (T1, közvetlenül lekérve) megerősíti a mechanizmust ("malicious demonstrations are retrieved from the poisoned memory or knowledge base with high probability... benign instructions... still maintain normal performance"), konkrét "80%+" számadatot ismét csak másodlagos forrás (mem0 blog) közöl: "average attack success rate above 80%" három ágens-típuson (önvezetés, tudásalapú QA, egészségügyi EHR).
- **Agent Security Bench**: "highest average attack success rate of 84.30% across 27 attack and defense methods" — **egyetlen forrásból** (Vectorize.io, T2), elsődleges tanulmányt nem azonosítottunk hozzá ebben a kutatásban.
- **A-MemGuard** (2025): "even advanced LLM-based detectors miss 66% of poisoned memory entries" — szintén **egyetlen forrásból** (mem0 blog, T2).

**Nem memória-specifikus, kapcsolódó (kontextusnak fontos, de nem közvetlen válasz) adatok**, mind egyetlen aggregátor-forrásból (Vectra.ai, T2/T3):
"Prompt injection now appears in over 73% of production AI deployments assessed during security audits, according to OWASP"; Pillar Security: "20% of jailbreak attempts succeed"; "90% of successful prompt injection attacks resulted in leakage of sensitive data"; Anthropic Opus 4.5 rendszerkártya-adat: 4,7% / 33,6% / 63,0% sikeres támadási arány 1/10/100 kísérletnél. **Ezek általános prompt injection-adatok, nem kifejezetten memória-mérgezésre vonatkoznak** — fontos megkülönböztetni.

---

## 3. Konkrét, dokumentált incidensek

### 3.1 Cisco "MemoryTrap" — Claude Code (2026.04.01., a legrelevánsabb eset)

Elsődleges forrás: Cisco hivatalos blog, Idan Habler és Amy Chang (Cisco AI Security Research), [blogs.cisco.com](https://blogs.cisco.com/ai/identifying-and-remediating-a-persistent-memory-compromise-in-claude-code) (T1/T2 — gyártói kutatói blog, névvel jegyzett szerzőkkel, technikai részletességgel). Független megerősítés: ugyanaz a szerző, az OWASP hivatalos blogján, az ASI06-tétel motiváló példájaként hivatkozva rá (lásd 2.1).

**Mi történt, szó szerint:**

> "We recently discovered a method to compromise Claude Code's memory and maintain persistence beyond our immediate session into every project, every session, and even after reboots." (T1)

> "AI coding agents such as Claude Code read from special files called MEMORY.md... In the version of Claude Code we evaluated, we found that first 200 lines of these files are loaded directly into the AI's system prompt... Memory files are treated as high-authority additions to this rulebook, and models assume they were written by the user and implicitly trust them and follow them." (T1)

A támadási lánc: (1) `npm postinstall` hook mint belépési pont (ismert supply-chain vektor); (2) a payload felülírja a projekt MEMORY.md-jét és a globális `~/.claude/settings.json` hook-konfigurációt; (3) perzisztencia — a payload egy shell-aliast ír a `.zshrc`/`.bashrc`-be, ami minden induláskor újra bekapcsolja az auto-memory funkciót, még akkor is, ha a felhasználó korábban kikapcsolta. Bemutatott hatás: a "megmérgezett" agent hamis biztonsági tanácsot adott (pl. API-kulcs commitolását javasolta .env helyett).

**Javítás:**

> "We are pleased to announce that, as of Claude Code v2.1.50, Anthropic has included a mitigation that removes user memories from the system prompt." (T1)

Ez **nevesített, dátumozott, gyártó által elismert és javított** sebezhetőség — nincs hozzá CVE-azonosító a talált forrásokban, de formális felelős közzététel (Cisco → Anthropic AppSec csapat → javított kiadás) történt.

### 3.2 Google Gemini hosszú távú memória — Johann Rehberger (2025.02.10-11.)

Elsődleges forrás: Johann Rehberger ("wunderwuzzi"), [Embrace The Red](https://embracethered.com/blog/posts/2025/gemini-memory-persistence-prompt-injection/) (T2 — elismert, önálló biztonsági kutató, nem gyártói forrás).

> "Existing Prompt Injection Mitigations: Generally, Gemini does not invoke certain sensitive tools when processing untrusted data... However, with some attack trickery... using delayed tool invocation, the memory tool can be invoked!" (T2)

A mechanizmus: egy feltöltött dokumentum rejtett utasítást csempész a Gemini összefoglalójába, ami egy későbbi felhasználói triggerszóra (pl. "igen") aktiválja a memória-írás eszközt, hamis adatot mentve a felhasználó tartós memóriájába.

**Fontos minősítési pontosítás:** az OECD.AI AI Incidents and Hazards Monitor (T2, kormányközi szervezet nyilvántartása) ezt **"AI Hazard"**-ként (bemutatott, valós fenyegetési útvonal), **nem** megerősített, valós áldozattal járó "aktív incidens"-ként sorolta be. Ez tehát egy kutatói proof-of-concept, nem dokumentált valós visszaélés.

### 3.3 Palo Alto Networks Unit 42 — Amazon Bedrock Agents Memory PoC (2025.10.09.)

Elsődleges forrás: [Unit 42, "When AI Remembers Too Much"](https://unit42.paloaltonetworks.com/indirect-prompt-injection-poisons-ai-longterm-memory/) (T2, gyártói fenyegetés-kutatás, névvel jegyzett szerzők: Royce Lu, Jay Chen).

> "This article presents a proof of concept (PoC) that demonstrates how adversaries can use indirect prompt injection to silently poison the long-term memory of an AI Agent. We use Amazon Bedrock Agent for this demonstration... Importantly, this is not a vulnerability in the Amazon Bedrock platform." (T2)

Amazon reakciója (Unit 42 tolmácsolásában): "Representatives from Amazon welcomed our research but emphasized that, in their view, these concerns are easy to mitigate by enabling Bedrock platform features... Specifically, they pointed out that applying Amazon Bedrock Guardrails with the prompt-attack policy provides effective protection." (T2)

Ez is **kifejezetten és önmeghatározóan PoC**, publikálás előtt a gyártóval egyeztetve — nem in-the-wild kihasználás.

### 3.4 Ami NEM memória-specifikus, de kapcsolódó — CVE-szintű esetek

A prompt injection tágabb kategóriájában valódi, aktívan kihasznált/patch-elt CVE-k léteznek (Vectra.ai összegzése, T2/T3, elsődleges forrásokkal átfedésben): CVE-2025-32711 ("EchoLeak", Microsoft 365 Copilot), **CVE-2025-53773** (GitHub Copilot / VS Code RCE — a payload a Copilot beállításait írta át, hogy automatikus jóváhagyással fusson kód; szintén Johann Rehberger fedezte fel és publikálta az Embrace The Red blogon), CVE-2026-21523/22708/26268 (Cursor IDE hármas CVE-lánc), CVE-2026-24307 ("Reprompt", Microsoft Copilot).

**Fontos:** ezek közül **egyik sem** kifejezetten "agent-memória tartalom-kapu megkerülése" címkével szerepel a CVE-adatbázisban — a CVE-2025-53773 egy beállítófájlra (nem memóriára) vonatkozik, ami szerkezetileg rokon jelenség (bizalmi felület tartalom-ellenőrzés nélküli írása), de nem ugyanaz a tárolási réteg. **Nem találtunk CVE-azonosítót, ami kifejezetten "memory poisoning"-ra lenne kiadva** — az itt tárgyalt memória-specifikus esetek (3.1–3.3) mind gyártói/kutatói blogbejegyzésen keresztül lettek nyilvánosságra hozva, nem a CVE-rendszeren keresztül.

---

## 4. Ki felel a tartalomért — hívó vagy tár?

Az összegyűjtött, szó szerinti nyilatkozatok egyöntetűen **a hívó/integrátor/felhasználó** felé tolják a felelősséget:

> **Anthropic memory tool (T1):** "Your application executes every file operation Claude requests, so these safeguards are your responsibility... For stronger guarantees, add validation that strips sensitive data before your handler writes the file." [platform.claude.com](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)

> **Anthropic álláspontja a Cisco MemoryTrap-jelentés szerint (T2, Cisco tolmácsolásában, nem szó szerinti Anthropic-idézet):** "Anthropic also clarified their position on security boundaries for agentic tools: first, that the user principal on the machine is considered fully trusted. Users (and by extension, scripts running as the user) are intentionally allowed to modify settings and memories. Second, the attack requires the user to interact with an untrusted repository and that users are ultimately responsible for vetting any dependencies introduced into their environments." [blogs.cisco.com](https://blogs.cisco.com/ai/identifying-and-remediating-a-persistent-memory-compromise-in-claude-code)

> **basic-memory (T1):** "Basic Memory is designed for single-user local knowledge bases and does not implement access controls between operating-system users." [SECURITY.md](https://raw.githubusercontent.com/basicmachines-co/basic-memory/main/SECURITY.md)

> **Microsoft Presidio (T1)** — egy réteggel lejjebb, a PII-detektálás szintjén, de ugyanaz a minta: "there is no guarantee that Presidio will find all sensitive information. Consequently, additional systems and protections should be employed." [faq.md](https://raw.githubusercontent.com/microsoft/presidio/main/docs/faq.md)

> **OpenAI (T1)** — jogi/tartalmi felelősség áthárítása szabályozott környezetben: "This feature is not covered under your BAA. PHI should not be entered when using this feature."

**A kutatási feladat feltételezése** (basic-memory szó szerint kimondja: *"It is NOT a security boundary"*) tartalmilag **pontosan illeszkedik** ehhez a mintázathoz, de a **pontos idézetet magában a basic-memory-ban nem sikerült igazolni** (lásd 1.1 és `ellentmondasok.md`). mem0-nál, Zep/Graphiti-nál és Letta-nál kifejezetten kerestünk hasonló nyilatkozatot, és **nem találtunk** ilyet a hivatalos dokumentációban.

**Összegzés:** minden vizsgált rendszernél, ahol egyáltalán van bármilyen nyilatkozat a témában, az nyilatkozat **a tartalom felelősségét a hívóra/integrátorra/felhasználóra hárítja**, sosem a tárra. Egyetlen vizsgált memória-szolgáltatás sem vállalja, hogy ő maga garantálja a beírt tartalom biztonságosságát.

---

## 5. Determinisztikus szűrés LLM nélkül — mi létezik a gyakorlatban

### 5.1 OWASP Agent Memory Guard — az egyetlen talált, kifejezetten erre épített, LLM-mentes megoldás

Hivatalos OWASP Incubator projekt (T1), [github.com/OWASP/www-project-agent-memory-guard](https://raw.githubusercontent.com/OWASP/www-project-agent-memory-guard/main/README.md), kifejezetten az ASI06-ra referencia-implementációként:

> "Agent Memory Guard sits between the agent and its memory store, screening every operation through a pipeline of detectors and a declarative policy." (T1)

> "No API keys. No external calls. Runs locally at 59 µs median latency." (T1)

**Architektúra:** `MemoryGuard.write()` → detektorok (prompt injection, titok/PII-szivárgás, védett kulcs módosítása, méret-anomália, önmegerősítő ciklusok) → YAML-alapú deklaratív policy, ami minden találat-típushoz akciót rendel: `allow` / `redact` / `quarantine` / `block`. Emellett SHA-256 integritás-alapvonal, forrás-eredet (`source_class`) minden íráson, és pillanatkép-alapú rollback.

Kész integrációk: LangChain, LangChain middleware, OpenAI Agents SDK, AutoGen, **mem0**, CrewAI — vagyis explicit módon azért létezik, mert a mögöttes memória-rendszerek (köztük a mem0, amit mi is vizsgáltunk) **maguk nem tartalmazzák** ezt a réteget.

**Saját, közzétett (T1, de önértékelt, kis mintás — 55 támadó payload, 4 kategória) benchmark:**

| Mutató | Érték |
|---|---|
| Detekciós arány (recall) | 92,5% |
| Precizitás | 100% |
| Fals pozitív arány | 0% |
| F1 | 0,961 |
| Medián latencia | 59 µs |

Kategóriánkénti bontás: prompt injection 100% (15/15), védett kulcs módosítása 100% (8/8), **érzékeny adat szivárgás 83% (10/12)**, **méret-anomália 80% (4/5)**. Fontos: **még a projekt saját, kedvező benchmarkja szerint is** a determinisztikus detektorok kb. 17-20%-ban elmulasztják az érzékeny-adat és méret-anomália eseteket — a "0% fals pozitív" állítás egy kis, saját összeállítású tesztkészletre vonatkozik, nem független, nagy méretű validációra.

A MITRE ATLAS "Memory Hardening" mitigációs kategória nyílt forráskódú referencia-implementációként hivatkozza (T1, projekt saját állítása, nem közvetlenül ellenőrzött MITRE-forrásból).

### 5.2 Microsoft Presidio — a determinisztikus (szabály+ML) PII-szűrés ipari mintapéldája és annak dokumentált korlátai

Hivatalos FAQ (T1, GitHub raw markdown):

> "Presidio can help identify sensitive/PII data in un/structured text. However, because it is using automated detection mechanisms, **there is no guarantee that Presidio will find all sensitive information**. Consequently, additional systems and protections should be employed." (T1)

> "Every PII identification logic would have its errors, and there is a **trade-off between false positives** (falsely detected text) **and false negatives** (PII entities which are not detected)." (T1)

A saját FAQ két külön szakaszt szentel a hamis negatívoknak és hamis pozitívoknak, alapvető, meg nem oldható kompromisszumként kezelve őket, nem szélsőséges esetként.

### 5.3 Általános DLP-gyakorlat (regex + szótár + strukturális mintaillesztés)

Cyberhaven 300 biztonsági vezetőt megkérdező felmérése (T2/T3, gyártói felmérés, de széles körben idézett):

> "According to Cyberhaven's survey of 300 security leaders, 51% of DLP alerts are false positives on average, and 65% of security teams say they are overwhelmed by benign alerts." — [cyberhaven.com](https://www.cyberhaven.com/infosec-essentials/dlp-false-positives) (T2/T3)

Az ok megnevezve: "the primary cause is content-inspection-only detection: rules that match patterns without knowing who moved the data, where it originated, or whether the transfer was approved." — vagyis a tisztán tartalom-alapú (kontextus nélküli) szabályillesztés strukturálisan hajlamos a hamis pozitívra.

### 5.4 A generáló modell nélküli rendszer korlátja a szabvány "guardrail" eszközökben is megjelenik

A Guardrails AI (T1, hivatalos dokumentáció) az `OnFailAction` szabványos válaszlehetőségei: `NOOP`, `EXCEPTION`, `REASK`, `FIX`, `FILTER`. Ebből kettő kifejezetten **LLM-hívást igényel**:

> "OnFailAction.REASK: Reask the LLM to generate an output that meets the correctness criteria..." / "OnFailAction.FIX: Programmatically fix the generated output... e.g. the formatter `provenance_llm` validator will remove any sentences that are estimated to be hallucinated." (T1)

Ez közvetlenül releváns az easter-memory-system megkötésére: a piaci "guardrail" eszközök tipikus, kényelmes hibakezelési útjai (újrakérdezés, automatikus javítás) **feltételezik egy generáló modell meglétét**. Generáló modell nélkül a ténylegesen elérhető válaszkészlet leszűkül `NOOP` (átenged, csak naplóz) / `EXCEPTION`-szerű `block` / durva `FILTER`-szerű elutasításra — pontosan az OWASP Agent Memory Guard `allow/redact/quarantine/block` négyese, ami nem véletlenül LLM-mentes.

---

## 6. A fals pozitív ára egy memória-rendszerben — specifikusan

**Kifejezetten kerestük**, hogy van-e mért vagy akár esettanulmány-szintű adat arról, mi történik egy agent/ügyfél viselkedésével, amikor egy memória-írási kapu blokkol (visszapróbálkozás, feladás, néma adatvesztés, támogatási jegyek stb.). **Ilyet nem találtunk.** Ez önmagában eredmény: kifejezetten kerestük ott, ahol lennie kellene (DLP-gyártói blogok, guardrail-keretrendszerek dokumentációja, OWASP Agent Memory Guard saját közlései), és nem volt.

Amit **egy szinttel távolabb** találtunk:

- Az általános DLP "alert fatigue" jelenség dokumentált mechanizmusa (Cyberhaven, T2/T3): a magas fals pozitív arány "erode[s] confidence in the DLP program itself, which can cause real exfiltration to be treated as noise" — ez a biztonsági kontroll saját hatékonyságának hosszú távú erózióját írja le, de **SOC-elemzői riasztás-kontextusban**, nem egy agent saját írási útvonalán.
- Az OWASP Agent Memory Guard saját, kis mintás benchmarkja szerinti "0% fals pozitív" (lásd 5.1) — ez azt sugallja, hogy egy jól hangolt, szűk körű determinisztikus kapu **elvben** elkerülheti a durva fals pozitív terhelést, de ez (a) önjelentett, (b) kis N, (c) nem méri az esetleges downstream viselkedési hatást.
- A Guardrails AI `NOOP` opciójának puszta létezése (5.4) hallgatólagos elismerése annak, hogy a blokkolás költsége néha elég nagy ahhoz, hogy a "csak naplózd, ne blokkold" legyen az elfogadott alapértelmezett néhány telepítésben.

**Következtetés:** a "blokkoló memória-kapu hogyan hat az agent/ügyfél viselkedésére" kérdésre a szakirodalomban és a gyártói anyagokban **nincs mért adat** — ez nyitott, nem lefedett terület.

---

## Összegző táblázat — tartalom-kapu íráskor rendszerenként

| Rendszer | Van-e beépített tartalom-kapu íráskor? | Típus | Forrás |
|---|---|---|---|
| basic-memory | Nincs (csak útvonal-validáció) | — | SECURITY.md (T1) |
| mem0 | Van, de LLM-alapú (Custom Instructions) | LLM-mediált | docs.mem0.ai (T1) |
| Zep / Graphiti | Nincs dokumentálva (OSS); "biztonsági garancia" csak a fizetős platformnál, specifikáció nélkül | — | README, docs (T1) |
| Letta | Nincs — csak karakteres méretkorlát; saját GitHub issue is megerősíti a hiányt | — | docs.letta.com (T1), Issue #3342 (T3) |
| Anthropic memory tool | Puha, modell-alapú ("usually refuses"); erősebb védelem explicit a hívó feladata | Modell-alapú + fejlesztői kiegészítés | platform.claude.com (T1) |
| Claude Code (auto-memory) | Nem dokumentált; a MemoryTrap-eset gyakorlatban is hiányt igazolt; a javítás architekturális, nem tartalom-szűrő | — | Cisco blog (T1/T2), OWASP blog (T1) |
| OpenAI / ChatGPT memória | Puha tendencia ("steer away"); kemény szabály csak funkció be/ki, nem tartalom-szint | Modell-alapú tendencia | openai.com, help.openai.com (T1) |

**A kutatás fő, egy mondatba sűríthető megállapítása:** a hat vizsgált rendszer közül **egyik sem** tartalmaz beépített, determinisztikus, LLM-mentes tartalom-kaput íráskor; ahol van bármilyen szűrés, az vagy modell-alapú/valószínűségi ("usually refuses", "steer away"), vagy kifejezetten a hívó fél feladatává van téve. Az egyetlen talált, kifejezetten erre a célra épített, LLM-mentes, determinisztikus megoldás (OWASP Agent Memory Guard) egy **harmadik féltől származó ráépülő eszköz**, nem a memória-rendszerek saját, beépített funkciója — és ez maga is bizonyítja a hiány valós, iparági elismertségét (MITRE ATLAS-referencia, mem0/LangChain/AutoGen/CrewAI integrációk).
