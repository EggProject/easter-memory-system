# Router és keresési rangsor — validáció

2026-09-01 · 47 forrás · 69 állítás · minden hivatkozott link él

---

## A rövid válasz

**A router úgy, ahogy felmerült — LLM ítéli meg, hogy „hasznos-e", és emberi jóváhagyás nélkül beírja a másik projektbe — nem támogatható.** Nem azért, mert senki nem csinálja (bár tényleg senki), hanem mert a három szükséges feltétel közül kettő mérhetően nem teljesül: az LLM egyedi relevancia-ítélete gyenge és felfelé torzít, a hiba pedig ebben a rendszerben nem marad ott, ahol keletkezett.

**A keresési rangsor ötlete — „B találatai kötelezően A után" — szintén nem támogatható**, és itt a megérzésed volt jó: „lehet hülyeséget mondok". Egyetlen keresőmotor és egyetlen termék sem csinál merev forrás-sorrendet, és van mérés arra, hogy a forrás szerinti keverés rontja az eredményt.

Mindkettőre van használható alternatíva, és mindkettő olyan mechanizmusból jön, ami már a rendszer része.

---

## 1. A router

### 1.1 Amit senki nem csinál — és ez itt bizonyíték, nem hiány

Hat rendszert néztünk át célzottan arra, hogy van-e bennük hatókörök közötti, gépi ítéleten alapuló tartalom-propagáció. **Egyikben sincs.** Ez nem „nem találtuk", hanem „megnéztük ott, ahol lennie kellene":

| Rendszer | Mit csinál helyette |
|---|---|
| **basic-memory** | Szigorú izoláció. *„Notes in one project do not appear in another."* A projektek közti másolás kizárólag kézi, kérésre indított művelet: *„There is no built-in cross-workspace 'Move to…' action yet."* |
| **mem0** | A hatókör célja kifejezetten az elkülönítés — *„prevent data from mixing between them"*. |
| **mem0 cross-repo demó** | **Húzó (pull) modell.** A projekt rögzíti a változást, a másik oldal csak akkor jut hozzá, ha ő maga rákérdez. Semmi nem íródik át. |
| **Letta megosztott memóriablokkok** | Nem másolás: **ugyanaz az objektum**, több ágens hivatkozik rá. *„When one agent updates the block, all others see the change immediately."* Nincs mit eldönteni, mert nincs második példány. |
| **Letta kontextus-tárak** | Van automatikus, jóváhagyás nélküli visszaolvasztás — de **egyetlen ágens saját memóriáján belül**, nem két független projekt között. |
| **Zep / Graphiti** | Automatikusan épített gráf, de felhasználónként elkülönítve. |

Egyetlen friss preprint (arXiv 2606.24535) használja a „propagation" szót, de ott is **láthatósági szabályról** van szó egy hatókör-hierarchiában, nem tartalom átmásolásáról. Gyártó-közeli, önértékelt forrás.

**Az egyetlen valódi precedens az ellenkező irányba mutat:** a Letta „sleep-time" ágense tényleg gépi ítélet alapján ír memóriát emberi jóváhagyás nélkül, és a dokumentáció ezt ki is mondja — *„does not ask you for approval"*. De ez saját memórián belüli konszolidáció, nem átvitel egy másik hatókörbe.

### 1.2 Amiért ez nem véletlen — az ítélet minősége

A router működése azon áll, hogy egy LLM megbízhatóan eldönti: „ez a tudásdarab máshol is hasznos". Erre van mérés, és rossz.

**A relevancia-ítélet egyedi szinten gyenge.** GPT-4o egyetértése emberi annotátorokkal Cohen kappában: bináris döntésnél **0,434**, négyfokú skálán **0,215**. Kisebb modelleknél a négyfokú kappa gyakorlatilag nulla. A Bing-stílusú UMBRELA értékelőnél kappa **0,31–0,37** — a szakirodalom ezt „fair agreement"-ként minősíti.

**Ugyanezek a rendszerek agregáltan viszont kiválóak:** az UMBRELA rendszer-szintű rangsor-korrelációja **0,97–0,99**. Ez a legfontosabb megkülönböztetés az egész kutatásban. Az LLM jól rangsorol sok elemet együtt, és rosszul dönt egyetlen elemről. **A router pont az utóbbi üzemmódban használná** — minden egyes bejegyzésre külön, igen/nem.

**És a torzítás iránya a rosszabbik.** A nagy TREC-vizsgálat szerint az UMBRELA **rendszeresen magasabbra értékel, mint az emberi értékelő**. Egy hamis pozitív irányba torzított bíró egy routerben azt jelenti: inkább átvisz, mint nem.

**Az átvihetőség még ennél is rosszabb.** Amikor egy finomhangolt bírót nem látott kérdésekre kell alkalmazni, a pontosság **8–9 százalékponttal esik**. Az agent-memória benchmarkokban a „ez az új információ érvényteleníti-e a régit" feladatra a legjobb módszerek is legfeljebb **7%**-ot érnek el többlépéses esetben. Konfliktus-feloldásnál a legjobb LLM-alapú rendszer **54%**, egy determinisztikus sorszám-szabály **78–94,8%**.

> A tanulság: nem az architektúra a szűk keresztmetszet, hanem maga az ítélet.

### 1.3 Amiért a hiba nem marad ott, ahol keletkezik

Ha a router téved, a hibás bejegyzés nem egy helyen van, hanem kettőn — és a másodikban semmi nem jelzi, hogy származtatott. Erre van mért adat, és aránytalan:

| Mérés | Mérgezett arány | Hatás |
|---|---|---|
| **PoisonedRAG** (USENIX Security 2025) | 5 szöveg egymillió szövegű tudásbázisban | **90%** támadási sikerráta |
| **AgentPoison** (NeurIPS 2024) | a tudásbázis **kevesebb mint 0,1%-a** | **>80%** siker, **<1%** teljesítményromlás |
| **MINJA** (arXiv 2503.03704) | csak lekérdezéseken át, közvetlen hozzáférés nélkül | **90%+** injekciós siker, elhanyagolható minőségromlás |

A közös mintázat mindháromban ugyanaz: **nagyon kevés rossz bejegyzés aránytalanul nagy hatást ér el, miközben a rendszer jóindulatú működése szinte változatlan marad.** Vagyis nem lehet észrevenni abból, hogy „valami rosszabb lett".

Valós eset is van: a Cisco által 2026 áprilisában dokumentált „MemoryTrap" egy telepítési horgon keresztül írta felül minden projekt memóriafájlját és a globális beállításokat, majd minden további promptba beinjektálódott — **projekteken, munkameneteken és újraindításokon átívelve, emberi jóváhagyás nélkül**. Az Anthropic válaszul kivette a felhasználói memóriákat a rendszerpromptból.

Ez a kockázat a mi rendszerünkben súlyosabb, mint másutt, mert **nálunk minden írás egyetlen kapun megy át**, és nincs kézi lemez-hozzáférés, amivel valaki véletlenül észrevenné a bekerült szemetet.

### 1.4 Amit helyette ajánlok

A kutatás három működő alternatívát mutat, és **kettő közülük már benne van a rendszerünkben**.

**(a) A linkelés jelentsen kereshetőséget, ne átírást.** Ez a mem0 húzó modellje: B nem kap semmit, de amikor B-ben dolgozom, a keresés belenéz A-ba is. Egy példány marad, nincs divergencia, nincs mit visszavonni.

**(b) Ami tényleg két projektnek hasznos, azt emeljük fölfelé, ne másoljuk oldalra.** Erre már van helyünk: a `tudas/` gyökér. Ez pontosan a Letta megosztott memóriablokk mintája — **egy objektum, mindenki ugyanazt látja**. A „hasznos-e máshol is" kérdés így nem másolási döntés lesz, hanem egy áthelyezési javaslat, amit ember hagy jóvá.

**(c) Ha mégis kell gépi kezdeményezés, az javaslat legyen, ne írás.** A rendszer felajánlja: „ez a bejegyzés a B projektben is hasznos lehet — emeljük a közös tudásba?" Ember dönt.

Egy figyelmeztetés a jóváhagyáshoz: a jóváhagyás csak akkor ér valamit, ha ritka. A vizsgált irodalom szerint sok jóváhagyáskérés után az emberek vakon rábólintanak — erre kemény szám nincs (a gyártók nem publikálnak ilyet), de a minta a biztonsági riasztások irodalmából jól ismert. Ha a rendszer naponta húsz javaslatot tesz, a huszonegyedik már nem kap valódi elbírálást.

---

## 2. A keresési rangsor

### 2.1 A merev sorrend nem bevett minta

Öt keresőmotort és hat terméket néztünk át. **Egyikben sincs beépített „saját hatókör mindig előre" szabály.**

- **Elasticsearch** klaszterek közti keresésnél a helyi és távoli találatok **globálisan, pontszám szerint** fésülődnek össze — a hivatalos példa ezt mutatja. Az `indices_boost` létezik, de az **opt-in súlyozás**, nem sorrend.
- **Azure AI Search** pontozási profiljai egyetlen indexen belül működnek; több index találatának forrás-súlyozott egyesítésére nincs primitív.
- **Vespa** federációnál az egyesítés az alkalmazás dolga, és a hivatalos példa **nem sorrendet, hanem küszöböt** mutat: a másodlagos forrásból csak egy pontszám fölötti találat kerül be.
- **A klasszikus federált keresés irodalma** (CORI, ReDDE) pont azt akarja **eltüntetni**, hogy a forrás számítson: a pontszámokat forrásfüggetlenné normalizálja.
- **Confluence** minden térben keres, és a hivatalos rangsorolási képlet **nem tartalmaz tér-alapú súlyt**. Egy 2006 óta nyitott, 162 szavazatos kérés pont azt kéri, hogy alapból szűküljön a jelenlegi térre — vagyis a kevert lista a bevett (és vitatott) alapértelmezés.
- **Slack** egyetlen kevert listát ad, típus szerinti fülekkel. **GitHub** explicit hatókört kér a kereséstől. **Notion** a teljes munkatéren keres, a hatókör utólagos szűrő.

### 2.2 És van mérés arra, hogy a forrás szerinti keverés ront

A FeB4RAG-vizsgálat a forrásonként váltakozó egyesítést hasonlította a tisztán relevancia szerintihez: **a relevancia-rendezés minden vizsgált adathalmazon jobb választ adott**.

Arra viszont **nincs szám**, hogy pontosan mennyibe kerül a merev „saját előre" sorrend — mert senki nem csinálja, tehát senki nem is mérte. Ez maga a válasz.

### 2.3 Amit helyette ajánlok

**Ne sorrend, hanem küszöb és jelölés.** A Vespa mintája: a kapcsolt projektből csak az kerül be, ami egy relevancia-küszöböt átlép — de ha átlépi, akkor a helyén szerepel, nem hátrasorolva. És minden találat vigye magával, honnan jött, mert a hatókör a felhasználó számára információ, nem rangsor.

Ez megőrzi, amit a rangsor-ötlet védeni akart — hogy a saját projekt ne fulladjon bele az idegen zajba —, de nem ront a relevancián.

---

## 3. Bizonyossági szintek

| Állítás | Szint |
|---|---|
| Nincs precedens gépi ítéletű, hatókörök közötti automatikus propagációra | **Magas** — hat rendszer célzott átnézése, mind negatív |
| Az LLM egyedi relevancia-ítélete gyenge (kappa 0,2–0,43) és felfelé torzít | **Magas** — több független, lektorált mérés |
| Kevés mérgezett bejegyzés aránytalan kárt okoz, észrevétlenül | **Magas** — három független mérés, egy valós eset |
| Egyetlen keresőmotor sem csinál merev forrás-sorrendet | **Magas** — öt motor hivatalos dokumentációja |
| A forrás szerinti keverés mérhetően ront a relevancián | **Közepes** — egy mérés (FeB4RAG) |
| A jóváhagyási fáradtság rontja a jóváhagyás értékét | **Alacsony** — a minta ismert, de kemény szám nincs rá |

---

## 4. A vizsgálat korlátai

- **A verifikációs fázis rövidített.** A linkek gépi ellenőrzése lefutott (mind a 47 él), és az idézeteket a rögzítő szkript ellenőrizte a mentett szöveg ellen. Külön ellenőrző ügynökök nem futottak, és a szintézist nem különálló ügynök írta, hanem a vezető szál — a modell-szétválasztás tehát nem teljes.
- **Több forrás összefoglalva jött le**, nem szó szerint (különösen a tudományos cikkeknél). A számok valószínűleg helyesek, de teljes szövegű ellenőrzés nélkül.
- **Két domain nem volt elérhető:** a Wikipédia bot-szabályzata és egy ACM-cikk.
- **A jóváhagyási fáradtság mérése hiányzik.** Az eredeti hivatkozások (Franklin 2025, Goddard 2012, Bainbridge 1983) valódiak, de csak másodkézből idézve szerepelnek.
- A mem0 memóriabiztonsági CVE-számokat nem sikerült megerősíteni — lehet, hogy tévesek.
