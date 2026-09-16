# Kivonat — korai-korok-ujra



---

# sq01 — A fa mint jogosultsági modell, és a kategóriák

# Megállapítások — sq01 újramérés
## A könyvtárfa mint jogosultsági modell, és a kategóriák

Ez a fájl a kutatási kör részletes megállapításait tartalmazza alkérdésenként, szó szerinti (eredeti nyelvű) idézetekkel és forrás-minősítéssel (tier). A megbízhatósági skála: **Magas** (több független, elsődleges forrásból konvergáló megállapítás) / **Közepes** (egyetlen T1-T2 forrás, szó szerint ellenőrzött idézettel) / **Alacsony** (egyetlen T4, nem lektorált forrás) / **Vitatott** (a forrás önmagával vagy más forrással ellentmond) / **Ellenőrizetlen** (nem sikerült mechanikusan visszaellenőrizni a forráshoz). Minden itt szereplő idézet a mögöttes snapshotban szó szerint (`add_claim.py` mechanikus ellenőrzésével) igazolt.

**Módszertani figyelmeztetés (degradált futási mód):** ebben a környezetben nem állt rendelkezésre Agent/szubágens-dispatch eszköz, ezért a keresés, a verifikáció és a szintézis egyetlen munkamenetben, szekvenciálisan zajlott — a skill saját dokumentált degradált módja szerint (lásd `00-plan.md`). Ez azt jelenti, hogy a modell-szintű elkülönítés (Sonnet keresés / Opus szintézis) nem valósult meg; kompenzációként minden számot tartalmazó vagy "Magas" jelölésre esélyes állítást élő URL-lel és — ahol lehetett — nyers HTML/PDF-ből való újbóli `grep`-es kereséssel ellenőriztünk.

---

## Vezetői összegzés — a három legfontosabb megállapítás

1. **A könyvtárfa/útvonal/névtér elhelyezkedése önmagában sehol nem biztonsági határ — sem az agent-memória rendszerekben, sem az általános infrastruktúrában.** Az Anthropic memory tool, a Claude Code memória és az Obsidian hivatalos dokumentációja explicit kimondja, hogy a láthatóság/útvonal nem kikényszerített konfiguráció (lásd SQ-01), és ugyanez az elv köszön vissza a valódi izolációt nyújtó rendszerekben is (Kubernetes, Vault, S3): ott is egy **külön, aktívan kikényszerített szabályzat-réteg** (RBAC, IAM policy, namespace-API) adja a tényleges határt, nem maga a fastruktúra (SQ-02). Ez a kör legmagasabban (10 forrásból konvergáló) alátámasztott, **Magas** megbízhatóságú megállapítása.
2. **A kategóriaszám növelése mérhetően rontja a besorolási pontosságot/F1-et, és ez a hatás modellméret-függő** — két egymástól független forrás (egy lektorált, kis modellekre; egy nem lektorált, nagy modellekre) mindkettő ugyanabba az irányba mutat: 3 kategóriánál 83-84%, 13 kategóriánál 62.8% balanced accuracy kis modelleknél; nagy modelleknél a kategóriatér szűkítése 3.3-7.0%-os átlagos F1-javulást hoz, de a hatás mérete fordítottan arányos a modell képességével (SQ-05). **Nincs egyetlen, modellmérettől független "ideális" kategóriaszám.**
3. **A fában való kizárás visszavonhatatlan lefelé, az öröklés iránya pedig kanonikusan szülőtől gyerek felé mutat, létrehozáskori (nem folyamatos) pillanatfelvétel formájában** — a git hivatalos dokumentációja szó szerint kimondja, hogy egy kizárt szülő könyvtár alatti fájl nem hozható vissza semmilyen mintával, a POSIX ACL és az NTFS-öröklés pedig egyaránt szülő→gyerek irányú, és a POSIX-nál kifejezetten csak létrehozáskor érvényesül, nem retroaktívan (SQ-03).

**Ellentmondás a korábbi (2026-08-23-i) körrel:** ennek az ügynöknek nem állt rendelkezésére a korábban eltávolított, forrás nélküli kategóriaszám/F1-állítás pontos tartalma, ezért nem végezhető közvetlen szám-összehasonlítás. Amit ez a kör ténylegesen, két független forrással megállapított — hogy TÖBB kategória MINDIG rontja a pontosságot/F1-et, és hogy ez a hatás kisebb/kevésbé képes modelleknél erősebb — összhangban van azzal, amit a megbízó már korábban, más úton felfedezett (hogy "a tényleges mérés éppen az ellenkezőjét mondta" a levett állításnak). Részletek: `ellentmondasok.md` 1. pont.

---

## SQ-01 — Használja-e bárki az útvonalat jogosultsági modellként markdown-alapú agent-memória rendszerekben?

**Alkérdés:** Hol él a láthatóság (fejléc-mező, központi config, vagy útvonal)? Kimondja-e bármelyik rendszer explicit, hogy a saját láthatósági jelölője NEM biztonsági határ?

**Vizsgált rendszerek:** Anthropic memory tool, Claude Code memória (CLAUDE.md/auto memory), Basic Memory, Letta memory blocks, mem0, Zep/Graphiti, Obsidian.

**Összefoglaló:** Hét vizsgált rendszer közül **egyik sem** valósít meg útvonal-alapú, kriptográfiailag vagy technikailag kikényszerített jogosultsági modellt. Az Anthropic memory tool és a Claude Code dokumentációja *explicit, szó szerint* kimondja, hogy a láthatósági jelölés (a `/memories` prefix, illetve a CLAUDE.md/auto memory) nem biztonsági határ, hanem kontextus vagy a hívó alkalmazás felelőssége (C001-C004). Az Obsidian ugyanezt mondja ki a pluginokra (C011-C012). A Letta és a Zep/Graphiti nem útvonalban, hanem explicit azonosítóban (block_id csatolás, illetve group_id névtér) tartja a láthatóságot — vagyis ott a "láthatóság" nem is az útvonalban, hanem egy külön mezőben/central configban él (C005-C006, C009-C010). A mem0 15 beépített, felülírható kategóriája (C007-C008) a kategória-oldal SQ-04/SQ-05 kérdéseihez kapcsolódik, nem a jogosultsághoz. A Basic Memory esetében **nem találtunk semmilyen hozzáférés-vezérlési nyilatkozatot** a vizsgált oldalon — ez hiányként, nem állításként szerepel (`hianyok.md`).

### Részletes állítások és idézetek

**[SQ-01-C001]** (T1, megbízhatóság: Közepes)
> Az Anthropic memory tool a /memories útvonalat csak prefixként kezeli, a tényleges biztonsági határt (path traversal elleni védelem) a kliens alkalmazásnak kell megvalósítania, nem a tool maga adja

Szó szerinti idézet: "*A malicious path such as /memories/../../secrets.env can reach files outside the /memories directory. Your implementation must validate every path in every command to prevent directory traversal attacks.*"

Forrás: https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool

**[SQ-01-C002]** (T1, megbízhatóság: Közepes)
> Az Anthropic memory tool dokumentációja kimondja, hogy a /memories prefix csak egy leképezés, amit a handler valósít meg, és a biztonság a handler felelőssége

Szó szerinti idézet: "*The /memories path is a prefix that your handler maps onto real storage, such as a per-user directory or keys in a database. Memory lives entirely in your application. A later conversation continues from the same memory when it sends the same tools entry and your handler serves the same store. For security, restrict all memory operations to the /memories directory (see Path traversal protection).*"

Forrás: https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool

**[SQ-01-C003]** (T1, megbízhatóság: Közepes)
> A Claude Code dokumentációja kimondja, hogy a CLAUDE.md és az auto memory nem kikényszerített konfiguráció, hanem kontextus, amit a modell figyelembe vehet vagy sem

Szó szerinti idézet: "*Claude treats them as context, not enforced configuration. To block an action regardless of what Claude decides, use a PreToolUse hook instead.*"

Forrás: https://code.claude.com/docs/en/memory

**[SQ-01-C004]** (T1, megbízhatóság: Közepes)
> A Claude Code dokumentációja explicit különbséget tesz a technikai kikényszerítés (settings/permissions.deny, sandbox.enabled) és a viselkedési útmutatás (CLAUDE.md) között, és kimondja, hogy a settings szabályok a kliens által kikényszerítettek, függetlenül attól, mit dönt Claude

Szó szerinti idézet: "*Settings rules are enforced by the client regardless of what Claude decides to do. CLAUDE.md instructions shape Claude's behavior but are not a hard enforcement layer.*"

Forrás: https://code.claude.com/docs/en/memory

**[SQ-01-C005]** (T1, megbízhatóság: Közepes)
> A Letta memory block hozzáférését nem útvonal, hanem explicit block_id csatolás (attach/detach) szabályozza: egy blokk azoknak az agenteknek látható, amelyekhez hozzá van csatolva

Szó szerinti idézet: "*Shareable - Multiple agents can access the same block; update once, visible everywhere*"

Forrás: https://docs.letta.com/guides/agents/memory-blocks/

**[SQ-01-C006]** (T1, megbízhatóság: Közepes)
> A Letta read-only jelölés blokkszinten egységes: nem lehet egy blokkot egyes agenteknek írhatóvá, másoknak írásvédetté tenni

Szó szerinti idézet: "*Read-only applies to the entire block, not per-agent. You cannot make a block read-only for some agents but writable for others.*"

Forrás: https://docs.letta.com/guides/agents/memory-blocks/

**[SQ-01-C007]** (T1, megbízhatóság: Közepes)
> A mem0 alapértelmezetten 15 beépített kategóriát használ a memóriák címkézésére

Szó szerinti idézet: "*Default list: Each project starts with 15 broad categories like travel, sports, and music.*"

Forrás: https://docs.mem0.ai/platform/features/custom-categories

**[SQ-01-C008]** (T1, megbízhatóság: Közepes)
> A mem0 dokumentáció felsorolja a 15 alapértelmezett kategórianevet

Szó szerinti idézet: "*personal_details, family, professional_details, sports, travel, food, music, health, technology, hobbies, fashion, entertainment, milestones, user_preferences, misc*"

Forrás: https://docs.mem0.ai/platform/features/custom-categories

**[SQ-01-C009]** (T1, megbízhatóság: Közepes)
> A Zep/Graphiti dokumentáció a group_id-t névtér-elválasztásra ajánlja többbérlős alkalmazásokhoz, az adatszivárgás megelőzése céljából

Szó szerinti idézet: "*Multi-tenant applications: Isolate data between different customers or organizations*"

Forrás: https://help.getzep.com/graphiti/core-concepts/graph-namespacing

**[SQ-01-C010]** (T1, megbízhatóság: Közepes)
> A Zep/Graphiti dokumentáció szerint a group_id-vel megcímkézett csomópontok/élek elkülönített, egymástól függetlenül lekérdezhető gráfot alkotnak

Szó szerinti idézet: "*Nodes and edges with the same group_id form a cohesive, isolated graph that can be queried and manipulated independently from other namespaces.*"

Forrás: https://help.getzep.com/graphiti/core-concepts/graph-namespacing

**[SQ-01-C011]** (T1, megbízhatóság: Közepes)
> Az Obsidian hivatalos dokumentációja kimondja, hogy technikai okokból nem lehet megbízhatóan korlátozni a community pluginokat konkrét jogosultságokra vagy hozzáférési szintekre - a plugin öröklődik Obsidian teljes hozzáférését, beleértve a fájlrendszert

Szó szerinti idézet: "*Due to technical limitations, Obsidian cannot reliably restrict plugins to specific permissions or access levels. This means that plugins will inherit Obsidian's access levels.*"

Forrás: https://obsidian.md/help/plugin-security

**[SQ-01-C012]** (T1, megbízhatóság: Közepes)
> Az Obsidian hivatalos dokumentációja szerint a community pluginok hozzáférhetnek a felhasználó számítógépén lévő fájlokhoz, csatlakozhatnak az internethez, és további programokat telepíthetnek

Szó szerinti idézet: "*Community plugins can access files on your computer. Community plugins can connect to internet. Community plugins can install additional programs.*"

Forrás: https://obsidian.md/help/plugin-security

---

## SQ-02 — Valódi többbérlős izolációs modellek (ellenpont)

**Alkérdés:** Ahol valódi izoláció létezik, mi a modell? Ez ellenpontja az SQ-01-nek: megmutatja, hogy a névtér/prefix mikor VÁLIK ténylegesen biztonsági határrá, és mi teszi azzá.

**Vizsgált rendszerek:** Kubernetes namespace+RBAC, HashiCorp Vault namespace, AWS S3 kulcs-prefix + IAM policy.

**Összefoglaló:** Mindhárom rendszer megerősíti, hogy a névtér/prefix **önmagában** csak szervezési eszköz — a Kubernetes explicit kimondja, hogy az objektumnevek névtereken átívelő átfedése "hasonló a mappákban lévő fájlokhoz" (C001), és a control planeon a "legfontosabb izolációs típus az authorization" (RBAC, C002). Az S3-nál még élesebb a megfogalmazás: "Amazon S3-nak nincs fizikai könyvtárhierarchiája" (C005), a hozzáférést az IAM `s3:prefix` feltétel és az explicit Deny kényszeríti ki (C006-C007). Egyedül a Vault namespace lép túl a puszta szervezésen: ott a namespace egy ténylegesen izolált "mini-Vault" példány saját login-útvonalakkal, amit a Vault motorja maga kényszerít ki (C003), és a szülő-gyerek öröklés is explicit, API-n konfigurálható (C004) — nem automatikus, hanem adminisztrátor által bekapcsolt viselkedés.

### Részletes állítások és idézetek

**[SQ-02-C001]** (T1, megbízhatóság: Közepes)
> A Kubernetes namespace elsősorban névtér-elkülönítést biztosít (az objektumnevek átfedhetnek névtereken átívelve, hasonlóan a mappákban lévő fájlokhoz), a tényleges biztonsági izolációt pedig a namespace-hez kötött RBAC és hálózati szabályzatok adják

Szó szerinti idézet: "*Object names within a namespace can overlap with names in other namespaces, similar to files in folders. This allows tenants to name their resources without having to consider what other tenants are doing.*"

Forrás: https://kubernetes.io/docs/concepts/security/multi-tenancy/

**[SQ-02-C002]** (T1, megbízhatóság: Közepes)
> A Kubernetes hivatalos dokumentációja szerint a control plane legfontosabb izolációs eleme az engedélyezés (authorization): az RBAC korlátozza a felhasználókat és service accountokat egy adott namespace-re

Szó szerinti idézet: "*The most important type of isolation for the control plane is authorization. If teams or their workloads can access or modify each others' API resources, they can change or disable all other types of policies thereby negating any protection those policies may offer.*"

Forrás: https://kubernetes.io/docs/concepts/security/multi-tenancy/

**[SQ-02-C003]** (T1, megbízhatóság: Közepes)
> A HashiCorp Vault namespace egy ténylegesen izolált 'mini-Vault' környezetet hoz létre saját login-útvonalakkal, szabályzatokkal, entitásokkal és tokenekkel, amit az adminisztrátorok API-n keresztül kényszerítenek ki (nem csak névtér, hanem a Vault motorja által kikényszerített határ)

Szó szerinti idézet: "*When you create a namespace, you establish an isolated environment with separate login paths that functions as a mini-Vault instance within your Vault installation.*"

Forrás: https://developer.hashicorp.com/vault/docs/enterprise/namespaces

**[SQ-02-C004]** (T1, megbízhatóság: Közepes)
> A Vault gyerek-névterei (child namespace, pl. A/B/C útvonal) örökölhetnek elemeket a szülő névtértől, és a szülő névtér szabályzatokat is kikényszeríthet (assert) a gyerek névtér identitásaira - ez explicit, API-n konfigurálható kétirányú kapcsolat, nem automatikus

Szó szerinti idézet: "*Children can inherit elements from their parent namespaces. For example, policies for a child namespace might reference entities or groups from the parent namespace. Parent namespaces can also assert policies on identities within a child namespace.*"

Forrás: https://developer.hashicorp.com/vault/docs/enterprise/namespaces

**[SQ-02-C005]** (T1, megbízhatóság: Közepes)
> Az Amazon S3 hivatalos dokumentációja kimondja, hogy az S3-nak nincs fizikai könyvtárhierarchiája, csak lapos kulcs-struktúrája van, és a 'mappa' csak az objektumkulcsok prefixéből következtetett logikai fogalom

Szó szerinti idézet: "*The console is using object keys to infer a logical hierarchy. Amazon S3 has no physical hierarchy. Amazon S3 only has buckets that contain objects in a flat file structure.*"

Forrás: https://docs.aws.amazon.com/AmazonS3/latest/userguide/walkthrough1.html

**[SQ-02-C006]** (T1, megbízhatóság: Közepes)
> Az AWS hivatalos S3 útmutatója szerint egy adott 'mappához' (prefixhez) való hozzáférést az IAM policy s3:prefix feltétele (Condition/StringLike) korlátozza, amit az AWS jogosultsági motor kényszerít ki minden egyes kérésnél, nem maga az útvonal

Szó szerinti idézet: "*For Alice to list the Development folder content, you must apply a policy to the user Alice that grants permission for the s3:ListBucket action on the companybucket bucket, provided the request includes the prefix Development/.*"

Forrás: https://docs.aws.amazon.com/AmazonS3/latest/userguide/walkthrough1.html

**[SQ-02-C007]** (T1, megbízhatóság: Közepes)
> Az AWS dokumentáció szerint egy explicit Deny szabályzat felülbírál minden más engedélyező szabályzatot (bucket policy vagy ACL), ezért a valódi elkülönítéshez explicit tiltó szabály kell, nem elég az, hogy egy felhasználó nem kapott engedélyt egy prefixre

Szó szerinti idézet: "*If you really want to tighten the access permissions, you could explicitly deny Alice access to any other folders in the bucket. If there is any other policy (bucket policy or ACL) that grants Alice access to any other folders in the bucket, this explicit deny overrides those permissions.*"

Forrás: https://docs.aws.amazon.com/AmazonS3/latest/userguide/walkthrough1.html

---

## SQ-03 — Öröklődés a fában: lefelé, felfelé, vagy mindkettő?

**Alkérdés:** Mit mondanak kanonikus források a kizárás visszavonhatatlanságáról egy fában?

**Vizsgált rendszerek:** git `.gitignore` (hivatalos forrás-dokumentáció), POSIX ACL (man7.org), NTFS öröklés (Microsoft Learn).

**Összefoglaló:** Mindhárom kanonikus forrás **lefelé irányuló** öröklődést ír le, és mindhárom explicit kimondja a visszavonhatatlanság valamilyen formáját. A git hivatalos dokumentációja szó szerint: "nem lehetséges egy fájlt visszaemelni, ha a fájl valamelyik szülő könyvtára ki van zárva" (C001) — ez pontosan megfelel a feladatban hivatkozott "git szabálya". A `.gitignore` feloldási sorrend explicit lefelé-öröklő: szülő mintákat a gyerek könyvtár mintái felülírhatják (C002). A POSIX ACL man oldala szerint az öröklés **csak létrehozáskor** történik (nem folyamatos, nem retroaktív, C003) — ez fontos különbség az NTFS-hez képest, ahol a szülő ACL módosítása a meglévő gyerek objektumokba is átterjed, amíg az öröklés be van kapcsolva (C004), de mozgatáskor NEM frissül automatikusan (C005) — vagyis az NTFS-öröklés esemény-vezérelt, nem folyamatosan újraszámolt kapcsolat.

### Részletes állítások és idézetek

**[SQ-03-C001]** (T1, megbízhatóság: Közepes)
> A git hivatalos dokumentációja kimondja, hogy egy fájl nem hozható vissza (negált mintával sem), ha a fájl valamelyik szülő könyvtára ki van zárva - a kizárás a fában lefelé visszavonhatatlan

Szó szerinti idézet: "*It is not possible to re-include a file if a parent directory of that file is excluded. Git doesn't list excluded directories for performance reasons, so any patterns on contained files have no effect, no matter where they are defined.*"

Forrás: https://raw.githubusercontent.com/git/git/master/Documentation/gitignore.adoc

**[SQ-03-C002]** (T1, megbízhatóság: Közepes)
> A git .gitignore feloldási sorrendje explicit lefelé irányuló öröklődést ír le: a magasabb szintű (szülő könyvtárbeli) .gitignore mintákat felülírhatják az alacsonyabb szintű (gyerek könyvtárbeli) minták, egészen a fájlt tartalmazó könyvtárig

Szó szerinti idézet: "*Patterns read from a .gitignore file in the same directory as the path, or in any parent directory (up to the top-level of the working tree), with patterns in the higher level files being overridden by those in lower level files down to the directory containing the file.*"

Forrás: https://raw.githubusercontent.com/git/git/master/Documentation/gitignore.adoc

**[SQ-03-C003]** (T1, megbízhatóság: Közepes)
> A POSIX ACL kanonikus man oldala szerint egy új fájl/könyvtár csak létrehozáskor örökli a szülő könyvtár default ACL-jét, mint saját access ACL-jét - ez lefelé irányuló, egyszeri (nem folyamatos, nem visszamenőleges) öröklődés

Szó szerinti idézet: "*If a default ACL is associated with a directory, the mode parameter to the functions creating file objects and the default ACL of the directory are used to determine the ACL of the new object: 1. The new object inherits the default ACL of the containing directory as its access ACL.*"

Forrás: https://man7.org/linux/man-pages/man5/acl.5.html

**[SQ-03-C004]** (T1, megbízhatóság: Közepes)
> A Microsoft hivatalos dokumentációja szerint az NTFS öröklődés iránya szülőtől a gyerek felé mutat: a szülő mappa ACL-jének módosítása a gyerek ACL-jébe kerül át, amíg az öröklés engedélyezett

Szó szerinti idézet: "*Any subsequent change to the parent folder's ACL causes the child's ACL to receive the inherited permissions.*"

Forrás: https://learn.microsoft.com/en-us/troubleshoot/windows-server/windows-security/inherited-permissions-not-automatically-update

**[SQ-03-C005]** (T1, megbízhatóság: Közepes)
> A Microsoft dokumentáció szerint mappa mozgatásakor az NTFS öröklött jogosultságok NEM frissülnek automatikusan, azaz az öröklődés nem folyamatosan újraszámolt kapcsolat, hanem eseményvezérelt (csak explicit ACL-módosításkor kényszerítődik ki)

Szó szerinti idézet: "*When you move a file or folder, the ACL is also moved and is not changed in any way. Even when inheritance is enabled for this folder, the inherited permissions are not automatically updated.*"

Forrás: https://learn.microsoft.com/en-us/troubleshoot/windows-server/windows-security/inherited-permissions-not-automatically-update

---

## SQ-04 — Kategóriák: hány kategóriát használnak valódi rendszerek, mond-e bárki ideális számot?

**Alkérdés:** Hány rendszer szándékosan NEM ír elő kategóriát, és miért?

**Vizsgált rendszerek:** PARA (Tiago Forte), Johnny.Decimal, Zettelkasten Method, (összevetésül: mem0 15 alapértelmezett kategóriája az SQ-01 alól).

**Összefoglaló:** A három szándékosan kategorizálási filozófiaként fellépő rendszer **egymásnak ellentmondó** számokat ír elő (lásd `ellentmondasok.md` 2. pont): a PARA pontosan 4 kategóriát (C001), a Johnny.Decimal explicit "legfeljebb 10 terület × legfeljebb 10 kategória" szabályt (C002), a Zettelkasten Method pedig kifejezetten **elutasítja** az előre definiált kategóriákat, azzal érvelve, hogy a kategorizálás felülről lefelé építkező, a jegyzeteket a struktúrához igazító folyamat (C003), és hogy egy rögzített kategória-rendszer nem nő szervesen, hanem egyszer megépül és utána mereven használatban marad (C004). **Egyik forrás sem állítja, hogy létezne tudományosan levezetett, univerzálisan helyes kategóriaszám** — mindhárom saját, nem empirikusan mért tervezési elvre hivatkozik.

### Részletes állítások és idézetek

**[SQ-04-C001]** (T1, megbízhatóság: Közepes)
> Tiago Forte a PARA módszerben pontosan négy kategóriát ír elő, azzal indokolva, hogy szerinte csak négy kategória fedi le az életünkben előforduló összes információt

Szó szerinti idézet: "*there are only four categories that encompass all the information in your life*"

Forrás: https://fortelabs.com/blog/para/

**[SQ-04-C002]** (T1, megbízhatóság: Közepes)
> A Johnny.Decimal hivatalos dokumentációja explicit numerikus korlátot ír elő: legfeljebb 10 terület (area) és területenként legfeljebb 10 kategória, ez a rendszer központi elve

Szó szerinti idézet: "*The 'no more than 10' concept is at the heart of Johnny.Decimal. When you start looking for something, there's no more than 10 area folders to choose from. Select one and ignore the rest. Now there's no more than 10 category folders to choose from.*"

Forrás: https://johnnydecimal.com/10-19-concepts/11-core/11.01-introduction/

**[SQ-04-C003]** (T2, megbízhatóság: Közepes)
> A Zettelkasten Method (zettelkasten.de) explicit azt tanácsolja, hogy ne hozzunk létre előre kategóriákat a jegyzetarchívumhoz, mert a kategorizálás felülről lefelé (top-down) építkező folyamat, ami arra kényszeríti a jegyzeteket, hogy illeszkedjenek a struktúrához

Szó szerinti idézet: "*Don't prepare. Don't invent categories. Just let it come. ... Creating categories is a top-down process. You start with the structure and then file the material away. Notes will have to fit the structure. If they don't, there'll have to be a compromise.*"

Forrás: https://zettelkasten.de/posts/no-categories/

**[SQ-04-C004]** (T2, megbízhatóság: Közepes)
> A Zettelkasten Method oldala azzal indokolja a kategóriák elutasítását, hogy egy rögzített kategóriarendszer nem nő szervesen, egyszer épül fel és utána mereven használatban marad, míg az agy folyamatosan asszimilálja az új információt

Szó szerinti idézet: "*Man-made structures, on the other hand, are not growing. They are built. A set of shared categories is something like that: it's built once and used forever. Rigid structures like this aren't likely to change.*"

Forrás: https://zettelkasten.de/posts/no-categories/

---

## SQ-05 — Kategóriaszám vs. besorolási pontosság, mért adatokkal (a legfontosabb alkérdés)

**Alkérdés:** Hogyan hat a választható kategóriák száma a modell besorolási pontosságára/F1-jére, nagy és kis modellekre külön, teljes mérési feltételekkel.

**Vizsgált forrás:** Scientific Reports (lektorált, kis/on-device LLM-ek), arXiv Haystack-to-Needle preprint (nem lektorált, nagy/frontier LLM-ek).

### Kis/on-device modellek (T2, lektorált — Scientific Reports, `s41598-024-63380-6`)

Mérési feltételek: on-device méretű LLM-ek (BERT, RoBERTa, ALBERT, XLNet családok, legfeljebb kb. 2GB méretig), intent-predikciós feladatokon, 3/4/6/13 kategóriás alfeladatokra bontva, epoch-onkénti balanced accuracy méréssel.

| Kategóriaszám (feladat) | Legjobb modell | Balanced accuracy | Epoch |
|---|---|---|---|
| 3 (query scope) | RoBERTa Large | 84% | 7 |
| 3 (query scope) | BERT Large | 83% | 4 |
| 13 (information feature) | RoBERTa Large | 62.8% | 15 |

### Nagy/frontier modellek (T4, nem lektorált — arXiv 2502.08436)

Mérési feltételek: 7 zero-shot klasszifikációs adathalmaz, 11-102 kategória között, négy modell (Llama-3.1-70B, Gemma-2-27B, Qwen2.5-72B, Claude-3.5-Sonnet), a kategóriatér (címketér) csökkentésének hatása macro-F1-re mérve.

| Modell | Átlagos macro-F1 javulás címketér-csökkentéskor |
|---|---|
| Llama-3.1-70B | 7.0% |
| Gemma-2-27B | 5.1% |
| Qwen2.5-72B | 4.9% |
| Claude-3.5-Sonnet | 3.3% |

A legkisebb (11 kategóriás) adathalmazon minden modell elérte vagy meghaladta a 95%-os pontosságot (ceiling/telítődés, C006).

**Kulcs-megállapítás mindkét méretkategóriára:** a kategóriaszám növekedése monoton rontja a pontosságot/F1-et, de a hatás mértéke fordítottan arányos a modell képességével — szó szerint: "more capable models can inherently handle larger label spaces more effectively" (C004). Ez azt jelenti, hogy **egyetlen, modellmérettől független "ideális" kategóriaszám megadása módszertanilag hibás lenne.**

### Részletes állítások és idézetek

**[SQ-05-C001]** (T2, megbízhatóság: Közepes)
> Egy lektorált (Scientific Reports) tanulmány kis, on-device LLM-eken (BERT, RoBERTa, ALBERT, XLNet családok, legfeljebb 2GB méretig) mérve egyértelmű összefüggést talált a kategóriák száma és a besorolási teljesítmény között: kevés kategóriánál a modellek gyorsan (néhány epoch alatt) telítődnek, sok kategóriánál a tanulási görbe ellaposodik és tovább tart az optimum elérése

Szó szerinti idézet: "*We have seen a clear and interesting relationship between the number of classes and classification performance of all the studied LLMs. First, for a small number of classes the trend resembles a logarithmic curve with models saturating after just a few epochs. Then, as the number of classes increases, the curve gets flatter and the models take longer to reach optimal performance.*"

Forrás: https://www.nature.com/articles/s41598-024-63380-6

**[SQ-05-C002]** (T2, megbízhatóság: Közepes)
> A tanulmány szerint minél több kategóriát kell megkülönböztetnie egy adott intent-feladatnak, annál fokozatosabb (lassabb) a tanulási görbe

Szó szerinti idézet: "*Overall, we observed that a larger number of classes per intent implies a more gradual learning curve.*"

Forrás: https://www.nature.com/articles/s41598-024-63380-6

**[SQ-05-C003]** (T2, megbízhatóság: Közepes)
> Konkrét mért adat: 3 kategóriás feladatnál (query scope) a RoBERTa Large 84%, a BERT Large 83% balanced accuracy-t ért el (7, illetve 4 epoch alatt); 13 kategóriás feladatnál (information feature) a legjobb modell (RoBERTa Large) csak 62.8% balanced accuracy-t ért el, 15 epoch alatt

Szó szerinti idézet: "*Overall, RoBERTa Large is the best performer, with a balanced accuracy of 84% that is reached after 7 epochs. Notably, BERT Large achieves only slightly worse performance (83%) in just 4 epochs. ... The best performing model for this task is RoBERTa Large with 62.8% Balanced Accuracy in 15 epochs*"

Forrás: https://www.nature.com/articles/s41598-024-63380-6

**[SQ-05-C004]** (T4, megbízhatóság: Alacsony)
> Egy 2025-ös arXiv preprint (nem lektorált) szerint nagyobb/képesebb LLM-ek (Qwen2.5-72B, Claude-3.5-Sonnet) eredendően jobban kezelik a nagy címke-/kategóriateret, mint a kevésbé képes modellek, amelyek nagyobb javulást mutatnak, ha a választható kategóriák számát csökkentik

Szó szerinti idézet: "*model capability plays a role, as we generally observe smaller performance improvements from more capable models like Qwen2.5-72B and Claude-3.5-Sonnet ... This leads us to hypothesize that more capable models can inherently handle larger label spaces more effectively. Conversely, less capable models show more substantial performance gains from LSR.*"

Forrás: https://arxiv.org/abs/2502.08436

**[SQ-05-C005]** (T4, megbízhatóság: Alacsony)
> Ugyanez a tanulmány konkrét számokkal méri a javulást négy modellen: Llama-3.1-70B átlagosan 7.0%, Gemma-2-27B 5.1%, Qwen2.5-72B 4.9%, Claude-3.5-Sonnet 3.3% macro-F1 javulást ér el a kategóriatér csökkentésétől hét, 11-102 kategóriát tartalmazó adathalmazon

Szó szerinti idézet: "*On average, Llama-3.1-70B gains 7.0%, Gemma-2-27b gains 5.1%, Qwen2.5-72B gains 4.9%, and Claude-3.5-Sonnet gains 3.3% across all datasets.*"

Forrás: https://arxiv.org/abs/2502.08436

**[SQ-05-C006]** (T4, megbízhatóság: Alacsony)
> A tanulmányban a legkisebb (11 kategóriás, Mtop Domain) adathalmazon minden tesztelt modell (Llama-3.1-70B, Gemma-2-27B, Qwen2.5-72B, Claude-3.5-Sonnet) elérte vagy meghaladta a 95%-os pontosságot, azaz a kategóriaszám csökkenésével a pontosság már telítődött (ceiling)

Szó szerinti idézet: "*all models score 95% or higher on Mtop Domain and already saturate the benchmark*"

Forrás: https://arxiv.org/abs/2502.08436

---

## SQ-06 — Mappanév/azonosítónév minősége és a találati pontosság

**Alkérdés:** Van-e mérés a leíró vs. rövidítéses vs. dátum-alapú nevek hatásáról a modell keresési pontosságára, feltételekkel és mintamérettel?

**Vizsgált forrás:** Lawrie, Feild & Binkley 2007 (ICPC, ember alanyok), "When Names Disappear" 2025 (arXiv, LLM-ek).

**Fontos korlát:** egyik talált forrás sem mér kifejezetten *mappaneveket* vagy LLM-alapú *fájlrendszer-navigációt* — mindkettő kódazonosítókra (változó-/függvénynevekre) vonatkozik. Az átvitel a mappanév-kérdésre analógiás, nem közvetlen (lásd `hianyok.md`).

**Lawrie et al. 2007 (T2, lektorált, n=128, ebből 80 fő fejezte be mind a 12 kérdést, 62.5%, C002):** a teljes szavas azonosítók szignifikánsan jobb leírási pontszámot adtak, mint az egybetűsek, mindhárom vizsgált esetben; a rövidített azonosítók két esetben szintén szignifikánsan jobbak voltak az egybetűsöknél, de **a teljes szavas és a rövidített azonosítók között sosem volt szignifikáns különbség** (C001). A tapasztalatlanabb programozókat jobban sújtja az uninformatív azonosító (p=0.0032, C003).

**"When Names Disappear" 2025 (T4, nem lektorált, frontier LLM-ek):** az azonosítónevek elhomályosítása még nagy, jól teljesítő modelleknél is jelentős romlást okoz: a ClassEval benchmarkon a GPT-4o 76.6%-ról 70.2%-ra, a DeepSeek V3 90.0%-ról 69.3%-ra esik (C004); a LiveCodeBench-en a romlás drámaibb, 20-30% feletti, pl. a Llama 4 Maverick 80.2%-ról 56.4%-ra esik (C005).

### Részletes állítások és idézetek

**[SQ-06-C001]** (T2, megbízhatóság: Közepes)
> Lawrie és szerzőtársai 2007-es, emberi alanyokon (n=128, ebből 80 fejezte be mind a 12 kérdést, 62.5%) végzett vizsgálatában a teljes szavas (full-word) azonosítók szignifikánsan jobb leírási pontszámot (description rating) eredményeztek, mint az egybetűs azonosítók, mindhárom szignifikáns esetben; az abbreviált azonosítók két esetben szintén szignifikánsan jobbak voltak az egybetűseknél, de a teljes szavas és a rövidített azonosítók között sosem volt szignifikáns különbség

Szó szerinti idézet: "*In all three cases, full-word identifiers lead to significantly better description ratings than single-letter identifiers. In two cases, abbreviated identifiers also lead to significantly better description ratings than the single letters. There is never a statistical difference between full words and abbreviations*"

Forrás: https://www.cs.kent.edu/~jmaletic/cs63902/Papers/Lawrie07.pdf

**[SQ-06-C002]** (T2, megbízhatóság: Közepes)
> A vizsgálat mintamérete: 192 fő kezdte el a kérdőívet, 128 válaszolt legalább egy kérdésre, 80 fő (62.5%) fejezte be mind a 12 kérdést

Szó szerinti idézet: "*In all, 192 people started the survey. Of these 64 filled in only the demographic information. Thus, 128 participants answered at least one question. Eighty of these completed all twelve questions.*"

Forrás: https://www.cs.kent.edu/~jmaletic/cs63902/Papers/Lawrie07.pdf

**[SQ-06-C003]** (T2, megbízhatóság: Közepes)
> A vizsgálat szerint a tapasztalatlanabb programozókat jobban sújtja az uninformatív azonosító, mint a tapasztaltakat (a variáns hatása szignifikánsan nagyobb az alacsonyabb szakértelmű csoportnál)

Szó szerinti idézet: "*uninformative identifiers hurt the inexperienced more than the experienced (p = 0.0032)*"

Forrás: https://www.cs.kent.edu/~jmaletic/cs63902/Papers/Lawrie07.pdf

**[SQ-06-C004]** (T4, megbízhatóság: Alacsony)
> Egy 2025-os arXiv preprint szerint az azonosítónevek eltávolítása/elhomályosítása (obfuscation) még a nagy, jól teljesítő modelleknél is jelentős pontosságcsökkenést okoz a ClassEval benchmarkon: a GPT-4o 76.6%-ról 70.2%-ra esik Pass@1-ben, a DeepSeek V3 90.0%-ról 69.3%-ra esik

Szó szerinti idézet: "*GPT-4o drops from 76.6% to 70.2% Pass@1 under Alpha, and DeepSeek V3 falls drastically from 90.0% to 69.3% under Ambiguity*"

Forrás: https://arxiv.org/html/2510.03178

**[SQ-06-C005]** (T4, megbízhatóság: Alacsony)
> Ugyanez a tanulmány a LiveCodeBench-en még drámaibb, 20-30% feletti pontosságesést mért az azonosítónevek elhomályosításakor; például a Llama 4 Maverick 80.2%-ról 56.4%-ra esett

Szó szerinti idézet: "*Nearly all models suffer double-digit drops, with reductions exceeding 20–30% in several obfuscation settings. For example, Llama 4 Maverick falls from 80.2% to just 56.4%.*"

Forrás: https://arxiv.org/html/2510.03178

---

## SQ-07 — Útvonal-biztonsági hibaosztályok: konkrét CVE-k

**Alkérdés:** Naiv prefix-illesztés, symlink, Unicode-normalizálási eltérés, névütközés — azonosítókkal.

**Vizsgált források:** MITRE CWE-22, NVD hivatalos CVE-leírások (Apache HTTPD, Android, unjs/ipx, node-tar család), Snyk Zip Slip.

**Összefoglaló négy hibaosztályonként:**

- **Naiv prefix-illesztés:** CVE-2025-54387 (unjs/ipx) — a megengedett könyvtár ellenőrzése "nyers string-prefix összehasonlítással" történt elválasztó karakter nélkül, így egy `public123` nevű könyvtár hozzáférhető volt, amikor csak `public` lett volna engedélyezve (C004). Rokon eset: CVE-2021-32804 (node-tar) — ismétlődő útvonal-gyökerek (`////home/user/.bashrc`) miatt a naiv abszolút-útvonal-tisztítás megkerülhető volt.
- **Symlink:** CVE-2021-32803 (node-tar) — könyvtár létrehozása, majd azonos nevű symlinkkel való felülírása megkerülte a symlink-ellenőrzést, mert az csak könyvtár-létrehozáskor futott le (C006).
- **Unicode-normalizálási eltérés:** CVE-2024-43093 (Android ExternalStorageProvider) — a fájlútvonal-szűrő hibás unicode-normalizálás miatt megkerülhető volt (C003). Rokon eset: CVE-2021-37712 (node-tar) — különböző karaktersorozatok, amelyek ugyanarra a normalizált Unicode-értékre oldódnak fel (C008).
- **Névütközés:** CVE-2021-37701 (node-tar) — egy `FOO` könyvtár és egy rá következő `foo` symlink case-insensitive fájlrendszeren összezavarta a belső könyvtár-cache-t (C007).

Emellett: CVE-2021-41773 (Apache HTTP Server 2.4.49, CVSS 9.8, élesben kihasznált, naiv útvonal-normalizáció, C002) és a Zip Slip sebezhetőségi osztály (Snyk, 2018.06.05, 10+ dokumentált CVE, C005) mint kiegészítő, széles hatókörű esetek. A CWE-22 hivatalos MITRE-definíciója (C001) adja a közös elméleti keretet mind a négy osztályhoz.

### Részletes állítások és idézetek

**[SQ-07-C001]** (T1, megbízhatóság: Közepes)
> A MITRE hivatalos CWE-22 definíciója szerint az útvonal-bejárás (path traversal) akkor jön létre, ha a program külső bemenetből épít fel egy útvonalat, ami egy korlátozott szülő könyvtár alatt kellene maradjon, de a speciális elemeket (pl. '../') nem semlegesíti megfelelően

Szó szerinti idézet: "*The product uses external input to construct a pathname that is intended to identify a file or directory that is located underneath a restricted parent directory, but the product does not properly neutralize special elements within the pathname that can cause the pathname to resolve to a location that is outside of the restricted directory.*"

Forrás: https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2021-41773

**[SQ-07-C002]** (T1, megbízhatóság: Közepes)
> A CVE-2021-41773 (Apache HTTP Server 2.4.49, kritikus, CVSS 9.8) egy naiv útvonal-normalizációs hiba volt, amivel URL-eket lehetett az Alias-szerű direktívák által konfigurált könyvtárakon kívüli fájlokra feloldani, és élesben ki is használták; a 2.4.50-es javítás hiányos volt (lásd CVE-2021-42013)

Szó szerinti idézet: "*A flaw was found in a change made to path normalization in Apache HTTP Server 2.4.49. An attacker could use a path traversal attack to map URLs to files outside the directories configured by Alias-like directives. ... This issue is known to be exploited in the wild. ... The fix in Apache HTTP Server 2.4.50 was found to be incomplete, see CVE-2021-42013.*"

Forrás: https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2021-41773

**[SQ-07-C003]** (T1, megbízhatóság: Közepes)
> A CVE-2024-43093 (Android ExternalStorageProvider) egy Unicode-normalizálási eltérésen alapuló megkerülés volt: a fájlútvonal-szűrő, ami érzékeny könyvtárakhoz való hozzáférést lett volna hivatott megakadályozni, hibás unicode-normalizálás miatt megkerülhető volt

Szó szerinti idézet: "*In shouldHideDocument of ExternalStorageProvider.java, there is a possible bypass of a file path filter designed to prevent access to sensitive directories due to incorrect unicode normalization.*"

Forrás: https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2021-41773

**[SQ-07-C004]** (T1, megbízhatóság: Közepes)
> A CVE-2025-54387 (ipx npm csomag) a naiv prefix-illesztés klasszikus hibáját mutatja: a megengedett könyvtár ellenőrzése nyers string-prefix összehasonlítással történt elválasztó karakter nélkül, ezért egy 'public123' nevű könyvtár hozzáférhető volt, amikor csak a 'public' lett volna engedélyezve

Szó szerinti idézet: "*the approach used to check whether a path is within allowed directories is vulnerable to path prefix bypass when the allowed directories do not end with a path separator. This occurs because the check relies on a raw string prefix comparison.*"

Forrás: https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2021-41773

**[SQ-07-C005]** (T1, megbízhatóság: Közepes)
> A Zip Slip nevű sebezhetőségi osztályt (tetszőleges fájlírás archívum-kicsomagoláskor, útvonal-bejárással preparált bejegyzésnevek, pl. '../../evil.sh' útján) a Snyk biztonsági csapata fedezte fel és hozta nyilvánosságra 2018. június 5-én, és ezrekre menő projektet érintett (HP, Amazon, Apache, Pivotal és mások), tíz+ konkrét CVE-vel dokumentálva (pl. CVE-2018-1002200 - CVE-2018-1002209, CVE-2018-1000544, CVE-2007-4559)

Szó szerinti idézet: "*Zip Slip is a widespread critical archive extraction vulnerability, allowing attackers to write arbitrary files on the system, typically resulting in remote command execution. It was discovered and responsibly disclosed by the Snyk Security team ahead of a public disclosure on 5th June 2018, and affects thousands of projects, including ones from HP, Amazon, Apache, Pivotal and many more.*"

Forrás: https://raw.githubusercontent.com/snyk/zip-slip-vulnerability/master/README.md

**[SQ-07-C006]** (T1, megbízhatóság: Közepes)
> A CVE-2021-32803 (node-tar) egy klasszikus symlink-alapú megkerülés: a program egy könyvtárat hozott létre és gyorsítótárazott, majd egy azonos nevű symlinkkel felülírva megkerülhető volt a symlink-ellenőrzés, mert az ellenőrzés csak könyvtár-létrehozáskor futott le, nem minden fájlműveletnél

Szó szerinti idézet: "*By first creating a directory, and then replacing that directory with a symlink, it was thus possible to bypass node-tar symlink checks on directories, essentially allowing an untrusted tar file to symlink into an arbitrary location and subsequently extracting arbitrary files into that location*"

Forrás: https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2021-37701

**[SQ-07-C007]** (T1, megbízhatóság: Közepes)
> A CVE-2021-37701 (node-tar) kimondottan a case-insensitive (kis-nagybetűt nem megkülönböztető) fájlrendszereken jelentkező névütközést dokumentálja: egy 'FOO' nevű könyvtár és egy rá következő 'foo' nevű symlink összezavarta a belső könyvtár-cache-t, mert a symlink létrehozása nem számított cache-találatnak, így egy azt követő fájlbejegyzés a symlink céljába került

Szó szerinti idézet: "*a similar confusion could arise on case-insensitive filesystems. If a tar archive contained a directory at FOO, followed by a symbolic link named foo, then on case-insensitive file systems, the creation of the symbolic link would remove the directory from the filesystem, but not from the internal directory cache, as it would not be treated as a cache hit.*"

Forrás: https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2021-37701

**[SQ-07-C008]** (T1, megbízhatóság: Közepes)
> A CVE-2021-37712 (node-tar) konkrétan Unicode-normalizálási eltérést dokumentál: két különböző karaktersorozat, amelyek ugyanarra a normalizált Unicode-értékre oldódnak fel (és Windows 8.3 rövid útvonalak esetén hasonlóan), lehetővé tették egy könyvtár symlinkkel való felülírását

Szó szerinti idézet: "*This logic was insufficient when extracting tar files that contained both a directory and a symlink with names containing unicode values that normalized to the same value. Additionally, on Windows systems, long path portions would resolve to the same file system entities as their 8.3 "short path" counterparts.*"

Forrás: https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2021-37701

---

## Kereszt-metszeti megállapítások (Magas megbízhatóság)

1. **A fastruktúra/névtér/útvonal elhelyezkedése önmagában sosem biztonsági határ.** 10 forrásból (SQ-01: 7 db agent-memória/jegyzetkezelő rendszer + SQ-02: 3 db általános infrastruktúra-rendszer) konvergáló megállapítás, két teljesen különböző területről. Mindenhol egy külön, aktívan kikényszerített szabályzat-réteg (kliens-oldali validáció, RBAC, IAM policy, namespace-API) adja a tényleges izolációt, nem a fa maga.
2. **A kizárás/exklúzió a fában lefelé visszavonhatatlan, az öröklés iránya szülő→gyerek.** 3 forrásból (git, POSIX ACL, NTFS) konvergáló megállapítás, három különböző technikai terület (verziókezelés, Unix fájlrendszer, Windows fájlrendszer) azonos elvi mintázattal.
3. **A kategóriaszám növekedése monoton rontja a besorolási pontosságot/F1-et, és a hatás mértéke fordítottan arányos a modell képességével.** 2 független forrásból (kis és nagy modellek, eltérő módszertan) konvergáló irány, de a nagyságrendi számok forrásonként eltérőek és csak az egyik lektorált — ezért az irány Magas, a konkrét számok Közepes/Alacsony megbízhatóságúak (ld. az egyes állításokat fent).



---

# sq02 — A markdown fájl mint memória-egység, és a fejléc

# Megállapítások — sq02: markdown fájl mint memória-egység, és a fejléc formátuma

**Kampány:** korai-korok-ujra · **Alkérdés:** sq02 · **Dátum:** 2026-09-15

**Módszertani megjegyzés a futtatásról:** ez a kutatási kör egyetlen agent-kontextusban futott, valódi párhuzamos Sonnet-al-agentek nélkül (a futtatókörnyezet nem biztosított subagent-indító eszközt). A `deep-web-research` skill degradált módját követtük: a keresés, majd az összegzés külön munkalépésként, de nem külön modell-példányban zajlott. Ez nem befolyásolja az idézetek és URL-ek pontosságát (minden idézet ellenőrzött, nyersen lekért forrásból származik), de a skill saját, modellek közötti elválasztásra épülő minőségbiztosítási rétege ezúttal hiányzott — ezt olvasóként érdemes figyelembe venni. Minden claim azonosítója (`Axx`) az `allitasok.csv` megfelelő sorára utal.

Minden alábbi állításnál a tier-jelölés: **T1** = hivatalos dokumentáció/spec/forráskód/lektorált; **T2** = megbízható másodlagos/lektorált; **T3** = blog/fórum/vélemény; **T4** = gyártói önjelentés/preprint.

---

## 1. Mi a tárolás egysége a valódi rendszerekben?

**Rövid válasz:** Vegyes kép, és **igen, van legalább egy éles, karbantartott rendszer, amely markdown fájlban tárol, és a fájlon belül tény-szintű egységeket is elkülönít** — de ez a rendszer (basic-memory) egy adatbázist is használ másodlagos indexként a tény-szintű granularitáshoz, nem tisztán a nyers fájlokra támaszkodik lekérdezéskor.

### basic-memory — fájl-elsődleges, adatbázis-másodlagos, tény-szintű belső indexeléssel

- **A fájl az elsődleges tároló, az adatbázis csak másodlagos index** (T1): *"The system follows a file-first architecture where all knowledge is represented in standard Markdown files and the database serves as a secondary index."* [A01]
- **A markdown a "single source of truth"** (T1): *"Plain Markdown files store all knowledge, making it accessible with any text editor and easy to version with git."* [A02]
- **Egy fájlon belül több tény-szintű "Observation" is él**, saját permalinkkel indexelve (T1): a dokumentáció "Entities / Observations / Relations / Tags" négyes felosztásban írja le a bennük rejlő szemantikus gráfot; az "Observations" definíciója: *"Categorized facts and information about entities"* [A03].
- **A tényleges tároló technológia: helyi SQLite index, opcionális vektoros kereséssel** (T1): *"Just files plus a local SQLite index. No servers required."* [A04] és *"Hybrid full-text + vector ranking with FastEmbed embeddings, on SQLite or Postgres."* [A05]

**Értékelés:** ez a legközelebbi ismert, éles analóg az `easter-memory-system` alapfeltevéséhez, de nem azonos vele — lásd `ellentmondasok.md` E2.

### mem0 — vektor-DB (alapértelmezetten Qdrant) + natív, beépített gráfréteg

- *"If no configuration is supplied, a default configuration will be applied, and Qdrant will be used as the vector database."* (T1) [A06]
- A gráf-réteg ma már **nem** külső gráf-adatbázisra épül: *"Graph Memory is built in . There is no Neo4j, Memgraph, or other graph store to deploy..."* (T1) [A07]. Korábban viszont igen: *"Earlier versions connected an external graph database (Neo4j and others) and exposed a relations field."* (T1) [A08]
- **Nem markdown fájl** a tárolás alapegysége; a "memory" objektumok a mem0 saját adatbázis-rétegében (vektor + gráf) élnek.

### Zep / Graphiti — valódi gráf-adatbázis, nem markdown

- A hosztolt Zep-termék saját, zárt forráskódú gráf-motort használ: *"Under the hood, Zep is powered by a proprietary graph database — the Context Graph Engine... so production deployments don't require a separate third-party graph database."* (T1, hivatalos repó) [A09]
- A nyílt forráskódú Graphiti könyvtár viszont **kötelezően** külső gráf-adatbázist igényel: Neo4j, FalkorDB, Amazon Neptune vagy Kuzu [A10].
- A Zep saját (nem független) mérése szerint 94.8% vs 93.4% a DMR benchmarkon (T4, gyártói önjelentés, arXiv preprint, **nem** lektorált) [A11] — ezt csak "a gyártó ezt állítja" jelleggel vesszük figyelembe.

### Letta — vektor-DB a tény-szintű ("archival") memóriához

- *"Archival memory is a general-purpose vector DB in the Letta API"* (T1) [A12]
- *"Archival memory is a semantically searchable database where agents can store facts, knowledge, and information for long-term retrieval."* (T1) [A13]

### Anthropic hivatalos memory tool — tisztán fájl-alapú, NINCS beépített indexelés

- *"The memory tool lets Claude store and retrieve information across conversations in a directory of memory files. Claude can create, read, update, and delete files that persist between sessions..."* (T1) [A14]
- A tool kliensoldalon fut, a fejlesztő dönt a tárolásról: *"The memory tool operates client-side: Claude requests file operations, and your application executes them. You control where and how the data is stored through your own infrastructure."* (T1) [A15]
- A hivatalos dokumentációban **egyszer sem** fordul elő a "markdown", "chunk" vagy "embed" szó — vagyis Anthropic saját memory tool-ja **nem** ír elő semmilyen fájlformátumot vagy indexelési sémát; ez egy tiszta, formátum-agnosztikus fájlrendszer-műveleti réteg.

### Claude Code saját memóriája — markdown fájl, egészben betöltve, méret szerint vágva (nem chunkolva)

- *"CLAUDE.md files are markdown files that give Claude persistent instructions for a project... Claude reads them at the start of every session."* (T1) [A16]
- Az automatikus memória (auto memory) betöltése **méretkorlátos, nem tény-szintű**: *"Loaded into Every session (first 200 lines or 25KB)"* (T1) [A17] — ez a truncation, nem retrieval: nincs kereső/rangsoroló lépés, egyszerűen az első N sor/KB kerül be.

### Obsidian — a jegyzet (fájl) az atomi egység; a frontmatter szándékosan kis, atomi adatokra való

- *"Properties are stored in YAML format at the top of the file."* (T1) [A18]
- *"Markdown in properties: This is an intentional limitation as properties are meant for small, atomic bits of information that are both human and machine readable."* (T1) [A19]
- (Nem elsődleges forrásból igazolt, de köztudott — lásd `hianyok.md` H5: az Obsidian beépített keresése és gráf nézete jegyzet/fájl-szinten dolgozik, nem tény-szinten; a tény-szintű kapcsolatokat a felhasználó saját maga fejezi ki wikilinkekkel és propertyk-kel, nem a rendszer extrahálja automatikusan.)

### Összefoglaló táblázat

| Rendszer | Tárolás egysége | Indexelés/visszakeresés tárolója | Markdown fájl az elsődleges tároló? |
|---|---|---|---|
| basic-memory | Markdown fájl (Entity) + fájlon belüli Observation/Relation | SQLite (FTS + vektor, FastEmbed) — **másodlagos** index | **Igen** |
| mem0 | "Memory" rekord (tény-szintű) | Vektor-DB (alapért. Qdrant) + natív gráfréteg | Nem |
| Zep (hosztolt) | Gráf-csomópont/-él | Proprietary "Context Graph Engine" (gráf-DB) | Nem |
| Graphiti (nyílt forráskódú) | Gráf-csomópont/-él | Neo4j / FalkorDB / Neptune / Kuzu (gráf-DB) | Nem |
| Letta (archival memory) | "Passage" (tény-szintű) | Vektor-DB | Nem |
| Anthropic memory tool | Fájl (formátum-agnosztikus) | Nincs beépített index | **Igen** (de nincs tény-szintű indexelés) |
| Claude Code (CLAUDE.md / auto memory) | Fájl, egészben (vagy méret-vágva) betöltve | Nincs — teljes betöltés vagy truncation | **Igen** (de nincs tény-szintű indexelés) |
| Obsidian | Jegyzet (fájl) | Beépített FTS jegyzet-szinten (nem elsődleges forrásból igazolva) | **Igen** (de nincs tény-szintű indexelés) |

**Válasz a kulcskérdésre:** a vizsgált rendszerek két csoportra oszlanak. (a) Amelyek **tény-szintű** egységet indexelnek, azok **mind gráf- vagy vektor-adatbázist** használnak erre (mem0, Zep/Graphiti, Letta) — **egyik sem markdown fájlt**. (b) Amelyek **markdown fájlt** használnak elsődleges tárolóként (Anthropic memory tool, Claude Code, Obsidian), azok **fájl-szinten** kezelik az adatot, tény-szintű automatikus indexelés nélkül. **Az egyetlen talált kivétel, amely mindkét tulajdonságot kombinálja, a basic-memory**: markdown fájl az igazság elsődleges forrása, DE a fájlon belüli tény-szintű egységeket (Observations) egy SQLite-alapú, újraépíthető másodlagos index tárolja külön-külön kereshető rekordokként.

---

## 2. Indexelés granularitása — mért adattal

**Egyetlen, valóban lektorált, feltételekkel dokumentált mérést találtunk erre a konkrét kérdésre:**

- **Forrás:** Chen, Lin et al., *"Dense X Retrieval: What Retrieval Granularity Should We Use?"*, EMNLP 2024 fő konferencia (ACL Anthology: 2024.emnlp-main.845) — **T2, lektorált**. [A23]
- **A mérés feltétele:** *"we conduct experiments on five different open-domain QA datasets and empirically compare the performance of six dual-encoder retrievers when Wikipedia is indexed by passage, sentence, and our proposed proposition."* [A21] — vagyis 5 nyílt-domain QA adathalmaz, 6 dual-encoder sűrű visszakereső modell, angol Wikipedia három granularitási szinten (100 szavas bekezdés, mondat, propozíció; a propozíció-alapú korpusz neve: FactoidWiki).
- **A szám:** *"The average improvement over passage-based retrieval of Recall@20 is +10.1 on unsupervised dense retrievers and +2.2 on supervised retrievers."* [A20]
- **A "propozíció" definíciója:** *"Propositions are defined as atomic expressions within text, each encapsulating a distinct factoid and presented in a concise, self-contained natural language format."* [A22]

**Marketing-torzítás jelzése:** a chunk-méret/granularitás témában rendkívül sok gyakorlati, nem-lektorált gyártói tartalom kering (Pinecone, LangChain, Weaviate stb. blogjai), amelyek gyakran hivatkoznak "jellemző" chunk-méret ökölszabályokra (pl. néhány száz token) kontrollált mérés megjelölése nélkül. Ebben a körben **csak a fenti egyetlen, lektorált mérést** sikerült szilárdan, feltételekkel dokumentálni; minden más talált szám (pl. konkrét "512 token" ajánlások) forrás nélkülinek bizonyult, ezért **nem** került be az `allitasok.csv`-be — lásd `hianyok.md` H6.

---

## 3. YAML frontmatter a gyakorlatban

- **Obsidian:** csak **három** beépített alapértelmezett mező van: `tags`, `aliases`, `cssclasses` [A24]; ezen felül van néhány Obsidian Publish-specifikus mező (`publish`, `permalink`, `description`, `image`, `cover`), de ezek nem "alap" mezők.
- **Jekyll:** a hivatalos referenciaoldal mindössze 6 mezőt sorol fel "predefined"-ként összesen (`layout`, `permalink`, `published` oldal-szinten; `date`, `category`/`categories`, `tags` poszt-szinten) [A25] — **a `title` nincs köztük**, csak illusztrációként szerepel a bevezető példában [A59] (lásd `ellentmondasok.md` E4).
- **Hugo:** *"The most common front matter fields are `date`, `draft`, `title`, and `weight`"* [A26] — itt a `title` hivatalosan, kifejezetten meg van nevezve.
- **Konkrét, számszerű ajánlás arra, hogy hány mező "sok"**: **nem található** egyik vizsgált hivatalos forrásban sem. Az egyetlen talált, ide vágó megfogalmazás minőségi jellegű, nem hivatalos style guide-ból: *"avoid non-standard practices like mixing data types or adding unnecessary complexity"* (T3) [A27]. Lásd `hianyok.md` H1.

---

## 4. YAML csapdái — elsődleges forrásból

### A YAML 1.1 spec maga is elismeri a többalakúságot

> *"YAML allows scalar content to be presented in several formats . For example, the boolean "true" might also be written as "yes"."*
> — YAML 1.1 spec, Final Draft 2005-01-18, https://yaml.org/spec/1.1/ (T1) [A28]

A pontos regex a YAML 1.1 Type Repository-ban van, nem magában a törzsspecifikációban:

> *"Regexp: y|Y|yes|Yes|YES|n|N|no|No|NO |true|True|TRUE|false|False|FALSE |on|On|ON|off|Off|OFF"*
> — https://yaml.org/type/bool.html (T1) [A29]

### A YAML 1.2.2 Core Schema kifejezetten megszünteti a kétértelműséget

> *"true | True | TRUE | false | False | FALSE tag:yaml.org,2002:bool"*
> (a Core Schema Tag Resolution táblázatból) — https://yaml.org/spec/1.2.2/, 10.3.2. szakasz (T1) [A30]

> *"The Core schema is an extension of the JSON schema... This is the recommended default schema that YAML processor should use unless instructed otherwise."*
> — ugyanott (T1) [A31]

**Tehát igen — a YAML 1.1 → 1.2 átmenet ténylegesen megváltoztatta ezt**: az 1.2-es Core Schema-ban a `yes/no/on/off/y/n` alakok kikerültek a logikai típus feloldásából. Fontos ugyanakkor, hogy maga a "Norway problem" kifejezés **nem szerepel** a spec szövegében egyik verzióban sem — ez közösségi/blog-eredetű elnevezés [A32], amelynek dokumentált, dátumozott népszerűsítése legkésőbb 2022 januárjára tehető [A33].

### A gyakorlatban a nagy parserek megosztottak

| Parser | Nyelv | Hivatalosan támogatott YAML verzió | Norway-hiba fennáll-e alapértelmezésben? |
|---|---|---|---|
| PyYAML | Python | **1.1** — *"PyYAML features a complete YAML 1.1 parser"* [A34] | **Igen** — forráskód: `re.compile(r'''^(?:yes\|Yes\|YES\|no\|No\|NO...\|on\|On\|ON\|off\|Off\|OFF)$'''...)` [A35] |
| SnakeYAML | Java | **1.1** — *"SnakeYAML is a YAML 1.1 processor for the Java Virtual Machine version 8+."* [A36] | **Igen** — forráskód: `BOOL = Pattern.compile("^(?:yes\|Yes\|YES\|no\|No\|NO\|true\|True\|TRUE\|false\|False\|FALSE\|on\|On\|ON\|off\|Off\|OFF)$")` [A37] |
| js-yaml (v4) | JavaScript | **1.2 alapértelmezett**, 1.1 is választható — *"Supports the YAML 1.2 and YAML 1.1 specifications."* [A39] | **Nem** — forráskód csak `true/True/TRUE/false/False/FALSE`-t ismer fel [A38] |
| ruamel.yaml | Python | **1.2 alapértelmezett**, 1.1 explicit kérésre — *"`ruamel.yaml` is a YAML 1.2 loader/dumper package for Python."* [A40] | **Nem** (alapértelmezésben) — a dokumentáció kifejezetten megnevezi az elhagyott alakokat: *"YAML 1.2 dropped support for several features unquoted Yes , No , On , Off"* [A41], [A42] |

**Egyéb, elsődleges forrással alátámasztott csapda:** idézőjel nélküli verziószám-szerű string ("9.3") lebegőpontossá alakul betöltéskor — *">>> load(versions) == [{"python": "3.5.3", "postgres": 9.3}]"* (T3, de technikailag reprodukálható viselkedés-bemutatás) [A43].

**Fontos, elsődleges forrásból cáfolt tévhit** (lásd `ellentmondasok.md` E1 részletesen): egy gyakran idézett blogbejegyzés szerint a Norway-hiba "a YAML 1.2 specifikáció szerint szándékos viselkedés" [A44] — ez **nem igaz** a spec 1.2.2-es szövege alapján, amely kifejezetten kizárja ezt a Core Schema szintjén.

---

## 5. TOML mint alternatíva

- **Tervezési cél, ami eleve kizárja a kétértelműséget:** *"TOML aims to be a minimal configuration file format that's easy to read due to obvious semantics. TOML is designed to map unambiguously to a hash table."* (T1) [A45]
- **A logikai típus szigorúan csak `true`/`false`, kisbetűvel, nincs alternatíva:** *"Booleans are just the tokens you're used to. Always lowercase."* (T1) [A46] — ez **szerkezetileg kizárja** a Norway-problémát: nincs `yes`/`no`/`on`/`off` alak, amit egy ISO-kód véletlenül eltalálhatna.
- **Explicit, elsőrangú dátum-idő típusok** (RFC 3339), nem implicit mintaillesztés: *"To unambiguously represent a specific instant in time, you may use an RFC 3339 formatted date-time with offset."* (T1) [A47]
- **A vezető nullák tiltása** csökkenti az egész szám / oktális kétértelműséget: *"Leading zeros are not allowed."* (T1) [A48]
- **Valós gyakorlati adaptáció:** a Hugo statikus oldal-generátor natívan elfogadja mindhárom formátumot (JSON/TOML/YAML) [A49], és kifejezetten megbízhatóbbnak kezeli a TOML dátumkezelését annyira, hogy idézőjel nélküli dátumértékeket is elfogad TOML-ban [A50].
- **Kimondott, idézhető állásfoglalás kifejezetten emberi szerkesztésre?** Nem találtunk egyetlen tiszta, egyértelmű "TOML jobb, mint YAML humán fejléchez" kinyilatkoztatást egy semleges, hivatalos forrásban. Találtunk viszont egy **ellentétes** véleményt: a PyTOML szerzője szerint *"TOML is a bad file format. It looks good at first glance... But once I started using it and the configuration schema became more complex, I found the syntax ugly and hard to read."* (T3, egyetlen fejlesztő véleménye) [A51]. **Ez a kritika kifejezetten összetett, mélyen ágyazott konfigurációkra vonatkozik** — egy egyszerű, lapos, 4 mezős fejléchez (mint amilyet az `easter-memory-system` használ: tags, modified, prompt_version, format_version) ez a konkrét kritikai pont valószínűleg nem érvényes, mivel ott nincs mélyen ágyazott struktúra.

**Összegzés:** a TOML nem elvi állásfoglalás, hanem **strukturális kényszer** útján zárja ki a Norway-problémát és a legtöbb implicit típuskonverziós csapdát — ára viszont a nagyobb verbozitás összetett, mélyen ágyazott adatoknál. Egy kis, fix mezőszámú, lapos fejléchez (mint a tárgyalt rendszeré) ez az ár alacsony, a haszon (kizárt kétértelműség) viszont közvetlenül releváns.

---

## 6. Beolvasás–visszaírás (round-trip) megőrzés

### YAML — ruamel.yaml

- Az alapértelmezett mód kifejezetten a round-trip: *"The major motivation for this fork is the round-trip capability for comments."* (T1) [A52]
- A cél kimondottan a humán-szerkeszthetőség + gépi feldolgozhatóság kombinálása: *"By extending the Python YAML parser to support round trip preservation of comments, it makes YAML a very good choice for configuration files that are human readable and editable while at the same time interpretable and modifiable by a program."* (T1) [A53]
- **Amit KIFEJEZETTEN NEM garantál** (a dokumentáció saját szavaival): a blokk-szekvencia elemek egyedi (soronkénti) behúzása nem marad meg (csak globális beállítás van rá), és a többsoros string blokkstílusa (`|`, `|+`, `|-`) elvész, ha a Python-oldalon újra hozzárendelik az értéket: *"Although ruamel.yaml doesn't preserve individual indentations of block sequence items... As this subclasses the string type the information is lost on reassignment."* (T1) [A54]
- A gyors, C-alapú (libyaml) betöltő **nem** használható round-trip szerkesztésre, mert nem generál komment-tokeneket: *"That library doesn't generate CommentTokens, so it cannot be used to do round trip editing on comments."* (T1) [A55]

### TOML — tomlkit

- *"TOML Kit is a 1.1.0-compliant TOML library. It includes a parser that preserves all comments, indentations, whitespace and internal element ordering, and makes them accessible and editable via an intuitive API."* (T1) [A56]
- **Egy explicit, dokumentált kivétel** a formátum-megőrzés alól: egy sorrenden kívül elhelyezett, táblatömböt kiterjesztő al-táblázat a visszaírás során a tömb utolsó eleméhez kerül, nem marad az eredeti pozíciójában (az adat megmarad, csak a fizikai elhelyezkedés változik) [A57].

**Összegzés:** mindkét ökoszisztémában (YAML: ruamel.yaml; TOML: tomlkit) létezik kifejezetten "style-preserving"/"round-trip" könyvtár, mindkettő **explicit dokumentálja a saját korlátait** is, nem csak a garanciáit — ez jó gyakorlat, amit érdemes követni az `easter-memory-system` saját olvasó/író rétegének dokumentálásakor is.

---

## 7. Cím a fejlécben vagy a törzsben?

Nincs egységes iparági konszenzus; a gyakorlat rendszerenként eltér:

| Rendszer | Cím elhelyezése | Forrás |
|---|---|---|
| Obsidian | **Nincs** `title` frontmatter mező az alapértelmezettek között; a cím a **fájlnévből** származik | T1, [A58] |
| Jekyll | `title` **nem** szerepel a hivatalos "predefined variables" listákon, csak konvencióként, a témák (theme-ek) `page.title`-ként használják | T1, [A59] (lásd `ellentmondasok.md` E4) |
| Hugo | `title` **hivatalosan, kifejezetten** az egyik leggyakoribb, definiált frontmatter mező, saját `Page.Title` metódussal | T1, [A60] |
| Notion export | Nem megállapítható a hivatalos dokumentációból | T1 (hiány), [A62] |

**Érdekesség:** a Hugo hivatalosan definiált mezői között szerepel egy `modified` nevű mező is, amely a `lastmod` aliasa — ugyanaz a mezőnév, mint amit az `easter-memory-system` fejléce használ (bár más rendszerben, esetleg más pontos szemantikával) [A61].

**Válasz:** nincs egyetlen "bevett gyakorlat" — a static site generátorok (Hugo) és a legtöbb blog-motor konvenciója a `title:` frontmatter mezőt preferálja, míg a jegyzetelő/tudásmenedzsment eszközök (Obsidian) a fájlnevet használják címként, és a frontmatterben szándékosan nem duplikálják. Az `easter-memory-system` saját döntése (cím a törzs `#` sorában) az **Obsidian-mintázathoz** áll közelebb, nem a Jekyll/Hugo-mintázathoz.



---

# sq03 — Beágyazás magyarra/többnyelvűre, és az integrációs felületek

# Megállapítások — sq03: beágyazás magyarra/többnyelvűre, integrációs felületek

**Kampány:** korai-korok-ujra · **Al-kérdés:** sq03 · **Kutatás dátuma:** 2026-09-15
**Módszer:** hivatalos dokumentáció nyers letöltése (`curl`, proxyn keresztül), GitHub-fájloknál `raw.githubusercontent.com`; ahol `WebFetch`-et használtunk, külön jelölve. Tier: T1 = hivatalos dok./forráskód/lektorált; T2 = megbízható másodlagos/gyártói; T3 = fórum/blog/anekdota.

**Fontos előzmény, amit ez a dokumentum folyamatosan figyelembe vesz:** a kampány saját belső dokumentumaiban (`/home/claude/work/audit/00-dontesek.html` és `90-meresek.html`) már léteznek konkrét, számszerű állítások ugyanezekről a témákról — ezek részben a 2026-08-20-i kutatásból, részben a 2026-09-01-i adverzariális ellenőrzésből származnak. Ahol lehetett, ezeket **függetlenül, nyers adatból újra levezettük** (nem csak elhittük), és minden esetben jelöljük, hogy megerősítettük vagy megdöntöttük őket.

---

## 1. Magyar és többnyelvű beágyazás — mért adattal

### 1.1 Van-e magyar retrieval taszk a nagy benchmarkban? Mennyi?

A **korábbi (2026-08-20-i) kör tévesen azt hitte, hogy "nincs magyar a nagy benchmarkban"**. Ez **megdőlt**, és ezt a mai kutatás **függetlenül, nyers adatból is megerősíti**.

- Az **MMTEB** (Massive Multilingual Text Embedding Benchmark) tanulmány (arXiv 2502.13595, elfogadva ICLR 2025-re) D függeléke, 8. táblázata szerint a magyar (`hun`, uráli nyelvcsalád) a benchmark 2025 eleji pillanatképében **12 taszkon** szerepelt összesen, ebből **2 Retrieval** típusú, 5 BitextMining, 3 Classification, 1 Clustering, 1 MultilabelClassification. [T1]
  > „hun Hungarian Uralic 5 3 1 0 1 0 0 2 0 0 0 12" — oszloprend: BitextMining, Classification, Clustering, InstructionRetrieval, MultilabelClassification, PairClassification, Reranking, **Retrieval**, STS, Speed, Summarization, Sum.
  Forrás: https://arxiv.org/html/2502.13595v3

- **Ez a szám azóta nőtt.** A ma élő (2026-09-15-i) hivatalos MTEB eredmény-adatbázisban (`mteb/results`, Hugging Face, `lastModified: 2026-09-14`) **pontosan 28 különböző taszk** hordoz `hun-Latn` nyelvű pontszámot — ezt egy saját, nyers parquet-adatokon futtatott SQL-lekérdezéssel állapítottuk meg (nem másodkézből vett szám). [T1]
  - Ez **szó szerint egyezik** a kampány saját `90-meresek.html` dokumentumának állításával ("Az MTEB összesen **28 taskban** tartalmaz magyart") — ez tehát egy **megerősített, nem megdöntött** korábbi állítás.
  - A magyarázat a 12→28 növekedésre: az MMTEB élő, folyamatosan bővülő benchmark; azóta új taszktípusok kerültek be (pl. `JinaVDR*` vizuális dokumentum-visszakeresés, `CommonVoice*` és `Fleurs*` hang-visszakeresés (T2A/A2T), `WebFAQ*`, `MKQARetrieval`). A 28 taszkból **15 névben "Retrieval"**, de ezek jelentős része **nem klasszikus szöveg-szöveg visszakeresés**, hanem kép/hang/dokumentum-QA jellegű.

- **Konkrét, klasszikus szöveges retrieval taszkok magyarra, amiket azonosítottunk:**
  - **BelebeleRetrieval** (`hun_Latn-hun_Latn` alkészlet): **191 modellnek** van pontszáma 2026-09-15-én. [T1, saját lekérdezés]
    - Legjobbak: Octen/Octen-Embedding-8B (0,98423), Mira190/Euler-Legal-Embedding-V1 (0,98415), **Qwen/Qwen3-Embedding-8B (0,97994, 3. hely)**, geevec-ai/geevec-embeddings-1.0 (0,97895), google/gemini-embedding-001 (0,95883), intfloat/multilingual-e5-large (0,9504), BAAI/bge-m3 (0,94364), openai/text-embedding-3-large (0,92318), Qwen/Qwen3-Embedding-0.6B (0,87139).
    - **Ez pontosan visszaigazolja** a kampány saját mérési dokumentumának 2026-09-01-i ellenőrzés utáni számait (0,97994 pontszám és 3. helyezés a Qwen3-Embedding-8B-nek, 191 modell) — a mai, két héttel későbbi állapot **stabil maradt**.
  - **HunSum2AbstractiveRetrieval** (monolingál magyar hírkorpusz, 1998 dokumentum/kérdés/qrels): **12 modellnek** van pontszáma. Legjobb: intfloat/multilingual-e5-large-instruct, `main_score=0,93544` (a hivatalos eredményfájl szerint ez a taszk fő metrikája — figyelem: **nem** egyezik az `ndcg_at_10=0,96366` értékkel, a két szám más metrikát jelöl). [T1]
    Forrás: https://huggingface.co/datasets/mteb/HunSum2AbstractiveRetrieval és a hivatalos eredmény-JSON.
  - **JinaVDRHungarianDocQARetrieval** (magyar dokumentum-vizuális-QA): **5 modellnek** van pontszáma. Legjobb: vidore/colqwen2.5-v0.2 (0,83932) — ez egy kép/dokumentum-látás alapú modell, nem klasszikus szöveges embedder. [T1]

**Mérési feltételek minden fenti számhoz:** a `mteb/results` Hugging Face dataset `score` mezője, amely a taszk hivatalos `main_score` metrikáját tükrözi (retrieval taszkoknál ez ált. — de nem mindig — `ndcg_at_10`; a HunSum2-nél kivételesen más). Split: `test`. Lekérés dátuma: **2026-09-15**, a dataset ezen a napon 1 napja frissült utoljára (élő, folyamatosan bővülő rangsor — a helyezések idővel változhatnak, ahogy azt a kampány saját dokumentuma is jelzi).

### 1.2 Mennyivel jobb a többnyelvű modell egynyelvűnél nem angol (magyar) lekérdezésen?

Két **lektorált, magyar nyelvű** tudományos forrást találtunk, amelyek közvetlenül mérik ezt:

1. **Antal Margit (Infocommunications Journal, 17(4), 2025. december, DOI: 10.36244/ICJ.2025.4.1)** — "Evaluation of Embedding Models for Hungarian Question-Answer Retrieval on Domain-Specific and Public Benchmarks". [T1, lektorált folyóirat]
   - Saját céges Q&A korpuszon (Clearservice), MRR metrikával: HUBERT (magyar-specifikus) = **0,78**; BGE-M3 és XLM-RoBERTa (többnyelvű) = **0,90** mindkettő. **A többnyelvű kb. 15%-kal jobb (relatív MRR).**
   - Nyilvános HuRTE benchmarkon (validáció): HUBERT = **0,82**; GEMINI (gemini-embedding) = **0,99**; BGE-M3 = **0,98**. **A többnyelvű kb. 20–21%-kal jobb.**
   - Szó szerint: „BGE-M3 and XLM-ROBERTA achieved the highest accuracy (MRR: 0.90) on the Clearservice dataset, while GEMINI demonstrated superior performance on HuRTE (MRR: 0.99)."
   - **Ez a tanulmány szerepel is a kampány saját `90-meresek.html` dokumentumában**, és a mai kutatás **teljes egyezéssel visszaigazolta** a benne idézett számokat (0,90/0,98/0,90/0,94/0,78/0,82 stb. mind pontosan stimmelnek a PDF-ben).

2. **Hatvani Péter & Yang Zijian Győző (IEEE CITDS 2024, Debrecen)** — "Training Embedding Models for Hungarian". [T1, lektorált konferencia] Ez egy **eltérő, árnyaltabb** képet ad: saját desztillált (nem eredeti, előtanított) modelleken mérve, a magyar STS-adathalmazon a többnyelvű gerincű (xlm-roberta) modell jobb (F1=0,068 vs. huBERT-gerincű 0,048), **de** egy saját, valós tesztkorpuszon a huBERT-gerincű modell kicsivel **jobb** (F1=0,490 vs. xlm-roberta 0,480).
   - **Tanulság:** a "többnyelvű mindig jobb magyaron" állítás **nem egyetemes** — adathalmaz-függő, és ez a tanulmány kis mintás (50 STS-pár), saját (nem publikusan elérhető, azonos körülmények közt tanított) modelleken mér, ezért óvatosan kezelendő.

**Hiány:** nem találtunk publikált mérést, amely kifejezetten egy mai, nagy kereskedelmi többnyelvű modellt (pl. `multilingual-e5-large`) egy **azonos méretű, kifejezetten csak magyarra tanított** modellel vetne össze standard benchmarkon, és kimondaná a pontos %-os javulást. A fenti két forrás a legjobb elérhető közelítés, mindkettő projekt-/kutatás-szintű, nem "hivatalos ajánlás".

---

## 2. Brute-force vs. közelítő vektorkeresés — hol a határ

**Nincs egyetlen hivatalos, számszerű "N vektorig ésszerű a brute-force" határ** egyetlen általunk vizsgált T1 forrásban sem. Ezt a hiányt maga a sqlite-vec dokumentáció is megerősíti: a hivatalos "Performance" útmutató oldala **jelenleg üres vázlat**, csak négy témapontot sorol fel tartalom nélkül:
> „- page_size\n- memory mapping\n- in-memory index\n- chunk_size (?)"
Forrás: https://raw.githubusercontent.com/asg017/sqlite-vec/main/site/guides/performance.md [T1]

A sqlite-vec dokumentáció ehelyett **minőségi** kijelentést tesz:
> „This is especially useful in `sqlite-vec`, which is (currently) brute-force only and meant to run on small devices."
Forrás: https://raw.githubusercontent.com/asg017/sqlite-vec/main/site/guides/binary-quant.md [T1]

**pgvector** (PostgreSQL) hivatalos README-je hasonlóan: alapból pontos (exact) keresést végez, "tökéletes recall"-lal, de **nem ad konkrét sorszám-küszöböt**:
> „By default, pgvector performs exact nearest neighbor search, which provides perfect recall."
Forrás: https://raw.githubusercontent.com/pgvector/pgvector/master/README.md [T1]

**FAISS** (Meta) hivatalos wiki-je a leginformatívabb, de itt sem egyetlen vektorszám a döntő tényező, hanem a **lekérdezésszám** és a **RAM-korlát**:
> „If you plan to perform only a few searches (say 1000-10000), the index building time will not be amortized by the search time. Then direct computation is the most efficient option. This is done via a \"Flat\" index."
> „If below 1M vectors: ...,IVF_K_,... Where K is 4*sqrt(N) to 16*sqrt(N)"
Forrás: https://raw.githubusercontent.com/wiki/facebookresearch/faiss/Guidelines-to-choose-an-index.md [T1]
Vagyis a hivatalos iránymutatás szerint **már 1 millió vektor alatt is** érdemes lehet elmozdulni a tiszta brute-force-tól, ha sok a lekérdezés vagy szűkös a memória — de ez nem egy kőbe vésett szám, hanem döntési fa.

**Egyetlen konkrét (memória+idő) mérési adatpontot** T3 forrásból találtunk: egy nem lektorált magánblog (Substack) kb. 14 millió darab 384-dimenziós vektoron (kb. 20 GB szintetikus adat, 24 GB RAM-os gépen) mérte a FAISS Flat indexet: 200 lekérdezésre 12,4 másodperc (≈62 ms/lekérdezés), 18,7 GB RAM, recall@10=1,000 (definíció szerint tökéletes). HNSW ugyanerre 0,95 mp (≈4,75 ms/lekérdezés), 13,2 GB, 0,962 recall. [T3 — a vektorszámot mi számoltuk ki a megadott GB/dimenzió alapján, a szerző nem közölte közvetlenül; **nem lektorált, egyetlen futtatás**.]
Forrás: https://datashot.substack.com/p/scaling-vector-search-flat-vs-hnsw

### Bináris kvantálás — mennyit spórol, mennyit ront

- **Térmegtakarítás (nyers vektorbájt szinten):** a sqlite-vec dokumentáció szerint pontosan **32×** (float32 → 1 bit): egy 8 dimenziós float32 vektor 32 bájt, bináris kvantálva 1 bájt; 1 millió vektornál 32 MB → 1 MB. [T1]
  > „For 1 million vectors, that would be `32MB`. On the other hand, the binary quantized 8-dimensional vector can be stored in a single byte... For 1 million vectors, that would be just `1MB`, a 32x reduction!"
- **Térmegtakarítás (teljes, működő index szintjén, ahol az eredeti vektorokat is meg kell tartani újra-pontozáshoz):** a Qdrant hivatalos technikai cikke szerint 100 ezer, 1536-dimenziós OpenAI-vektornál 900 MB helyett **128 MB** kell — ez **≈7×**, nem 32×. [T2] A különbség oka: egy valós rendszerben (Qdrant) az eredeti (nem kvantált) vektorokat is meg kell őrizni a re-scoring lépéshez, csak a HNSW-gráf és a kvantált index kerül RAM-ba.
  > „For 100K OpenAI Embedding (`ada-002`) vectors we would need 900 Megabytes of RAM and disk space... With binary quantization, those same 100K OpenAI vectors only require 128 MB of RAM."
  Forrás: https://qdrant.tech/articles/binary-quantization/index.md
- **Pontosságromlás:** a sqlite-vec dokumentáció csak minőségileg fogalmaz ("sokat veszítünk"), konkrét számot nem közöl:
  > „Though keep in mind, you're bound to lose a lot of quality when reducing 32 bits of information to 1 bit."
  A Qdrant viszont **konkrét, reprodukálható recall-számokat** ad, 3–4× túlmintavételezéssel (oversampling) és újra-pontozással (rescore): recall 0,9445 (Mistral Embed, 768d) és 0,9966 (OpenAI text-embedding-3-large, 3072d) között, modelltől és dimenziótól függően. [T2]

---

## 3. SQLite mint vektortár (`sqlite-vec`)

**Mire való:** a hivatalos README szerint "extrém kicsi, elég gyors" vektorkereső kiterjesztés, ami mindenhol fut, ahol az SQLite ("Linux/MacOS/Windows, WASM böngészőben, Raspberry Pi-n"). [T1]

**Mire nem való:** a projekt maga mondja ki, hogy **pre-v1.0** állapotú ("expect breaking changes"), és **jelenleg kizárólag brute-force** — nincs beépített ANN-index. [T1]

**Méret-ajánlás:** **nincs kimondott**. A hivatalos "Performance" oldal üres vázlat (l. fent). Ez egy dokumentált hiány magában a projektben, nem a mi kutatási hiányunk.

**Működik-e rendszer-SQLite-tal (bővítmény-betöltés)?**
- **macOS-en NEM automatikusan**, mert az Apple által szállított SQLite-könyvtár nem támogatja a bővítmény-betöltést, ezért a hozzá kötött Python `sqlite3` modul sem:
  > „The default SQLite library that is bundled with Mac operating systems do not include support for SQLite extensions. That means the default Python library that is bundled with MacOS also does not support SQLite extensions." Hibaüzenet: `AttributeError: 'sqlite3.Connection' object has no attribute 'enable_load_extension'`.
  Javasolt megoldás: Homebrew-s Python/SQLite használata. [T1] Forrás: https://raw.githubusercontent.com/asg017/sqlite-vec/main/site/using/python.md
- **Bun/Node esetén ugyanez a figyelmeztetés külön is szerepel**, közvetlenül releváns a kampány Node/Bun/Docker-alapú tervére:
  > „// MacOS *might* have to do this, as the builtin SQLite library on MacOS doesn't allow extensions\nDatabase.setCustomSQLite(\"/usr/local/opt/sqlite3/lib/libsqlite3.dylib\");"
  Forrás: https://raw.githubusercontent.com/asg017/sqlite-vec/main/site/using/js.md [T1]
- **Linuxon/Dockerben** (a kampány tényleges céltelepítése) ez a korlátozás jellemzően **nem** áll fenn — a hivatalos dokumentáció kifejezetten csak macOS-re ír figyelmeztetést, Linuxra nem.
- **Hivatalosan támogatott Node/Bun-kötések:** `node:sqlite` (Node 23.5.0+), `better-sqlite3`, `node-sqlite3`, `jsr:@db/sqlite` (Deno), `bun:sqlite`. [T1]
- **SQLite-verzió ajánlás:** 3.41 vagy újabb ajánlott, de nem kötelező; régebbivel is fut, csak "bizonyos funkciók és lekérdezések" nem helyesen. [T1]

**Kereszt-igazolás a kampány saját belső dokumentumával:** a kampány `90-meresek.html`-je szerint "az FTS5 elérhetősége a Bun beépített SQLite-jában nincs dokumentálva" — ezt a mai kutatás **nem tudta megdönteni sem megcáfolni** (nincs hivatalos Bun-FTS5 dokumentáció sehol), de a macOS-specifikus bővítmény-tiltásról szóló részét **közvetlenül alátámasztja** a fenti két sqlite-vec-idézet.

---

## 4. Magyar szótövezés és a szöveges keresés (FTS5)

**Az SQLite FTS5 hivatalos dokumentációja pontosan négy beépített tokenizálót sorol fel**: `unicode61`, `ascii`, `porter`, `trigram`. **Snowball NINCS köztük** — az egy különálló, harmadik féltől származó bővítmény (pl. `fts5-snowball` GitHub-projekt, `abiliojr/fts5-snowball`). [T1]
> „FTS5 features four built-in tokenizer modules... The unicode61 tokenizer... The ascii tokenizer... The porter tokenizer... The trigram tokenizer."
Forrás: https://sqlite.org/fts5.html

**A beépített `porter` tokenizáló kifejezetten csak angolra készült** — a dokumentáció ezt szó szerint kimondja:
> „The porter stemmer algorithm is designed for use with English language terms only - using it with other languages may or may not improve search utility."
[T1] Ugyanez a forrás azt is kimondja, hogy az **ICU-tokenizáló FTS5-ben nem elérhető**:
> „The ICU tokenizer is not available."
(Ez utóbbi pontosan megegyezik a kampány saját, korábban rögzített idézetével a Spec 30-ban.)

**Van-e mérés a Snowball-féle magyar tövezőről?** Részleges válasz:
- A magyar Snowball-algoritmust **Anna Tordai** készítette (2006 szeptember), és a hivatalos Snowball-projekt oldala egy konkrét tudományos hivatkozást ad meg mögé: **A. Tordai és M. de Rijke, "Four Stemmers and a Funeral: Stemming in Hungarian at CLEF 2005"** (DOI: 10.1007/11878773_20, megerősítve Semantic Scholaron is). [T1 a hivatkozás létezésére]
- **Ez tehát létező, lektorált IR-mérés** a magyar tövezésről (CLEF = Cross-Language Evaluation Forum, egy tényleges információ-visszakeresési benchmark-konferencia) — **de a tényleges tartalmát, számait ebben a kutatási körben NEM sikerült elérni**: a Springer-oldal fizetőfal mögött van, a ResearchGate 403-at adott, a szerzői (ILPS/UvA) forrásoldal halott link (DNS-hiba, ~20 éves egyetemi erőforrás), a Semantic Scholar API pedig "CLOSED" hozzáférésűnek jelzi az absztraktot is.
- **Mondjuk ki egyértelműen, ahogy a feladat kéri:** *ezen a kutatási körön belül nem sikerült számszerű mérést idézni arról, hogy a Snowball magyar tövező mit csinál a magyar szóalakokkal.* A hivatkozás létezik, de a tartalma nem ellenőrizhető innen.

**Fontos, konkrét belső ellentmondás, amit ez a kutatás tárt fel:** a kampány `Spec 30` dokumentuma (`/home/claude/work/audit/30-kereses.html`) kimondja:
> „A tövező szándékosan hiányzik — magyarra bizonyítottan ront, és minden további nyelvhez külön szabályrendszer kellene."
**Ehhez azonban sem ez a dokumentum, sem a mérési dokumentum (`90-meresek.html`) nem rendel konkrét forrást vagy mérést.** A mérési dokumentumban a legközelebbi kapcsolódó tétel egy **másik** jelenség: az MTEB publikál egy BM25-alapvonalat a magyar retrieval-taszkon, de az hibásan angol tövezővel (`stemmer_language="english"`) futott magyar szövegen — ezt a kampány maga is helyesen kizárta a specifikációból, mint tudottan hibás számot. Ez **nem** azonos azzal az állítással, hogy "a Snowball magyar tövező bizonyítottan ront" — ez utóbbihoz nem találtunk sem külső, sem belső forrást. **Ez pontosan az a fajta megalapozatlan, forrás nélküli állítás, amit a mostani kör kritériumai (URL + szó szerinti idézet minden számhoz) ki akarnak zárni.**

---

## 5. Integrációs felületek — kliensenkénti session-indulási hook méret-limit

**Ez a pont a kampány számára különösen kényes**, mert a feladatleírás szerint pont egy ilyen szám körül volt korábban hiba. A belső dokumentumok (`00-dontesek.html` D-15/5, `90-meresek.html` 07. szakasz) elmondják a teljes történetet:

1. A **2026-08-20-i** kutatás azt találta, hogy a Claude Code session-indulási hookja 10 000 karaktert fogad.
2. A **2026-09-01-i adverzariális ellenőrzés MEGDÖNTÖTTE** ezt: négy hivatalos oldalt átnézve (hook-referencia, útmutató, SDK-oldal, hibakeresés) egyikben sem találtak karakter- vagy tokenlimitet; a szám csak GitHub-hibajegyekben szerepelt, felhasználói állításként. A hivatalosan **dokumentált** állapot ekkor: Codex = 2500 token (dokumentált); **Claude Code, Gemini CLI, Cursor = nincs dokumentált limit**; Antigravitynek nincs is session-indulási hookja (helyette `PreInvocation`, 12 000 karakteres szabály-limittel).
3. **A mai (2026-09-15-i) kutatásunk során a hivatalos Claude Code hook-dokumentáció MÁR EXPLICIT MÓDON dokumentálja a 10 000 karakteres korlátot** — szó szerint, két helyen is. **Ez ellentmond a jelenleg érvényes D-15 döntésnek és a 2026-09-01-i ellenőrzés által rögzített állapotnak.** Részletek és a lehetséges magyarázat az `ellentmondasok.md`-ben.

### Kliensenkénti eredmény (2026-09-15, hivatalos dokumentáció, szó szerint idézve)

**Claude Code** — VAN dokumentált limit, **10 000 karakter**:
> „Hook output strings, including `additionalContext`, `systemMessage`, and plain stdout, are capped at 10,000 characters. Output that exceeds this limit is saved to a file and replaced with a preview and file path..."
> „If a value exceeds 10,000 characters, Claude Code writes the text to a file in the session directory and passes Claude the file path with a short preview instead."
[T1] Forrás: https://code.claude.com/docs/en/hooks

Kapcsolódó, **nem hivatalos** (GitHub-hibajegy, WebFetch-összefoglalón keresztül idézve, nem nyers letöltéssel) megfigyelés: a gyakorlatban a modellhez eljutó előnézet csak **2000 karakter (2KB)**, még ha a teljes szöveg a dokumentált 10 000-es küszöb alatt is fér el fájlba mentve:
> „The documentation says that hook output his truncated after 10,000 characters, but I observe that if you breach this limit, the output is truncated to 2000 characters." [T2, WebFetch-összefoglaló]
Forrás: https://github.com/anthropics/claude-code/issues/44086 (Claude Code v2.1.92)

**Codex CLI** — VAN dokumentált, konfigurálható alapértelmezett limit, **kb. 2500 token**:
> „By default, Codex limits each model-visible hook-output message to roughly 2,500 tokens. If a hook returns more, Codex saves the full text under `<temp_dir>/hook_outputs/<session_id>/<uuid>.txt`..."
> „Omit `additionalContextLimit` to use the default 2500-token threshold. Use a positive integer to select a different threshold, or 0 to pass the handler's complete additional context directly to the model."
[T1] Forrás: https://developers.openai.com/codex/hooks
(Megjegyzés: **token**-alapú mérték, nem karakter-alapú — más mértékegység, mint a Claude Code-nál.)

**Gemini CLI** — **NINCS dokumentált limit.** A teljes hivatalos hook-referencia (`reference.md`, `index.md`, `writing-hooks.md`) egyike sem tartalmaz karakter- vagy token-alapú korlátot a `SessionStart` hook `additionalContext` mezőjére; az egyetlen dokumentált korlát egy 60 másodperces (60000 ms) alapértelmezett **időkorlát**:
> „`hookSpecificOutput.additionalContext`: (`string`) - **Interactive**: Injected as the first turn in history."
> (méretkorlátra vonatkozó keresés: 0 találat a teljes dokumentáción)
[T1] Forrás: https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/hooks/reference.md

**Cursor** — **NINCS dokumentált limit.** A hivatalos `sessionStart` hook leírása szerint van `additional_context` kimeneti mező, de sem itt, sem az oldal "Execution type limits" szakaszában nincs karakter/token-korlát dokumentálva (az egyetlen numerikus korlát a `loop_limit`, ami a `stop`/`subagentStop` hook-okra vonatkozik, nem a kontextus méretére):
> „sessionStart ... Output Field Type Description ... `additional_context` string (optional) Additional context to add to the conversation's initial system context"
[T1] Forrás: https://cursor.com/docs/hooks

### Összefoglaló táblázat

| Kliens | Van session-indulási hook? | Dokumentált méretkorlát? | Érték |
|---|---|---|---|
| Claude Code | Igen (`SessionStart`) | **Igen** (2026-09-15-től, l. ellentmondasok.md) | 10 000 karakter |
| Codex CLI | Igen (`SessionStart`) | Igen | ~2500 token (állítható, `additionalContextLimit`) |
| Gemini CLI | Igen (`SessionStart`) | **Nincs** | — |
| Cursor | Igen (`sessionStart`) | **Nincs** | — |
| Antigravity | Nincs `SessionStart`-szerű hook; helyette `PreInvocation` (a kampány belső mérése szerint) | Igen (belső mérés szerint) | 12 000 karakter (nem ellenőriztük ma újra hivatalos forrásból, mert nem szerepelt a feladat listáján) |

---

## 6. Tud-e az MCP szerver oldalról kontextust betolni a kliensbe?

**Rövid válasz a hivatalos specifikáció (2025-06-18) alapján: nem egyoldalúan.** Az MCP három mechanizmust ad a szervernek kontextus/kompetencia felkínálására, mindegyik a kliens/host kontrollja alatt marad:

1. **Resources** — *"application-driven"* (alkalmazás-vezérelt): a szerver felkínálja az adatot, de a host dönt, mikor/hogyan illeszti be.
   > „Resources in MCP are designed to be application-driven, with host applications determining how to incorporate context based on their needs."
   [T1] https://modelcontextprotocol.io/specification/2025-06-18/server/resources
2. **Prompts** — *"user-controlled"* (felhasználó-vezérelt): a felhasználónak explicit ki kell választania.
   > „Prompts are designed to be user-controlled, meaning they are exposed from servers to clients with the intention of the user being able to explicitly select them for use."
   [T1] https://modelcontextprotocol.io/specification/2025-06-18/server/prompts
3. **Sampling** — a szerver **kérhet** egy LLM-completion-t a kliensen keresztül (akár más MCP-forrásokból vett kontextussal is), de a kliens tartja a kontrollt, és a specifikáció kifejezetten emberi felügyeletet ("human in the loop") ír elő:
   > „Servers can request text, audio, or image-based interactions and optionally include context from MCP servers in their prompts."
   > „For trust & safety and security, there SHOULD always be a human in the loop with the ability to deny sampling requests."
   [T1] https://modelcontextprotocol.io/specification/2025-06-18/client/sampling

A `list_changed` / `resources/updated` értesítések a legközelebb állnak a "push"-hoz, de ezek is csak **jelzik**, hogy érdemes újra lekérdezni — nem viszik át maguktól a tartalmat.

### Kliensek tényleges MCP-képesség-támogatása — hol hiányzik valami a hivatalos listáról

**Cursor** — a hivatalos "Protocol and extension support" táblázata **explicit módon felsorolja**: Tools, Prompts, Resources, Roots, Elicitation, Apps (mind "Supported"). **A Sampling EGYÁLTALÁN NEM szerepel** ezen a listán — a teljes oldalon nulla találat van a "sampling" szóra. [T1] Ez a **legerősebb** bizonyíték a hét kliens/forrás közül, mert itt egy explicit, kimerítőnek szánt táblázatból hiányzik a képesség, nem csak hallgatásról van szó.
> „Feature Support Description Tools Supported ... Prompts Supported ... Resources Supported ... Roots Supported ... Elicitation Supported ... Apps (extension) Supported"
Forrás: https://cursor.com/docs/mcp

**Claude Code** — a hivatalos, kb. 103 000 karakteres MCP-dokumentáció részletesen tárgyalja a Tools, Resources (`@` mention), Prompts (parancsként) és Elicitation (form/text mód) használatát — de a "sampling" szó **egyszer sem** fordul elő a teljes oldalon. Ez gyengébb bizonyíték, mint a Cursor esete, mert itt nincs explicit kizáró táblázat, csak hallgatás. [T1, közepes-magas erősségű következtetés]
Forrás: https://code.claude.com/docs/en/mcp

**Gemini CLI** — a hivatalos `mcp-server.md` tárgyalja a Tools, Resources és Prompts (mint "slash command") támogatását, de a "sampling", "elicit" és "roots" szavakra **egyaránt nulla találat** van a teljes dokumentumban. [T1, hallgatás alapú]
Forrás: https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/tools/mcp-server.md

**Codex CLI** — a hivatalos MCP-oldal "Supported MCP features" listája **kizárólag szállítási/hitelesítési képességeket** sorol fel (STDIO szerverek, Streamable HTTP szerverek, Server instructions) — Tools/Resources/Prompts/Sampling egyike sem szerepel explicit módon ezen a listán, bár a Tools-használat közvetve nyilvánvaló a szöveg többi részéből. [T1, gyengébb bizonyíték, mert a lista feltehetően csak a szállítási réteget célozza]
Forrás: https://developers.openai.com/codex/mcp

**Megjegyzés a kampány saját anyagához:** a `40-mcp.html` (Spec 40) belső dokumentum eddig nem vizsgálta a Sampling kérdést, és csak annyit rögzít, hogy a Resources kérdése ("kell-e erőforrásként is kiajánlani bármit?") még nyitott — ez a mostani sq03-kutatás tehát **új területet fed le**, nem ismétel meg korábbi állítást.
