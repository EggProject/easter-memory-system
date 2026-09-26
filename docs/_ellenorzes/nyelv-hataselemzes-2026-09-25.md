# A nyelvi prioritás változásának hatása — 2026-09-25

Kiinduló mondat (a tulajdonos, 2026-09-25): „Angol nyelv a prior! magyar nyelvet is tamogatni kell tobbi nyelv most nem erdekes”. Ez a D-01/3-at írja felül.
Átnézve: `/home/claude/work/audit/` hét fájlja (00, 20, 30, 40, 50, 60, 90). Mind megvan, egyik sem üres. Hivatkozás: fájlszám · szakasz vagy tétel (pl. „00 · D-02/6”, „90 · §04”).

## Rövid válasz

A D-01/3 tartalma megváltozik: a „minden nyelv, kiemelten a magyar” helyett az angol az elsődleges, a magyar támogatott, a többi nyelv most nem cél. A döntési napló ma még a régi szöveget tartalmazza. A legnagyobb hatás a D-02 (kapuzott keresés) indoklását éri: a mérés kilencnyelvű, a kapuzott összesített előnye 0,004, a 90 §04 kifejezetten a magyarra mint „a fő cél szerint kiemelt nyelvre” hivatkozik, az angol sorban viszont a vak fúzió nyer, a táblázat legnagyobb különbségével (+0,088). A beágyazó modellt (Qwen3-Embedding) csak a 90 nevezi meg, D-tétel nem rögzíti; a dokumentumok magyar mérésekkel indokolják. Ez az indok áll, angolra viszont nincs benne külön alátámasztás. Tárgytalan lesz a CJK-kérdés (Spec 30 §09–§10, a D-43 zárómegjegyzése) és a hét másik nyelv mérési adata, ami történeti adatként marad. A felület nyelvkészlete (D-30: magyar és angol) és a gépi oldal angolsága nem változik. Az új prioritással csak a D-30 „egyenrangú” megfogalmazása és az a kockázati mondat kerül szembe, amelyik az angolt „második nyelvként” kezeli. A rendszerfájlok nevéről a mondat kifejezetten nem dönt. A Spec 20 §10 nyitott pontja csak a `naplo/`-t nevezi meg, pedig magyar a `memoria/` gyökér, két konténernév, két programüzemmód és a `karbantart admin-link` parancs is.

## Érintett helyek

83 vizsgált hely: 3 megváltozik, 9 tárgytalan, 11-nél gyengül az indok, 2-nél erősödik, 58-at nem érint.

| # | Fájl + szakasz/tétel | Pontos idézet | Hatás | Miért |
|---|---|---|---|---|
| 1 | 00 · D-01/3 | „Minden nyelv, kiemelten a magyar” · „A rendszernek nyelvfüggetlennek kell lennie. A magyar kiemelt cél, de nem az egyetlen.” | megváltozik | Ez maga a felülírt tétel; a napló fejléce „frissítve: 2026-09-25”, de a D-01/3 szövege ma még a régi. |
| 2 | 00 · D-01/7 | „a technikai tudás (nyelv, framework)” | nem érinti | Programozási nyelvről szól, nem természetes nyelvről. |
| 3 | 00 · D-02 (fejléc és törzs) | „Alátámasztás: 90-meresek.html (a mérések elfogadva)” · „A jelentés-keresés mindig fut. A szöveges láb csak akkor szólal meg, ha a kérdés minden szava együtt előfordul egy dokumentumban.” | indok gyengül | Az alátámasztó mérés kilencnyelvű összesítés (kapuzott 0,855, vak fúzió 0,851), az angol sorban a vak fúzió nyer +0,088-cal (#59); a döntés áll. |
| 4 | 00 · D-02/1 | „Egyetlen szó-index, pontos szóegyezéssel. Ékezet-hajtogatás van, tövező nincs.” | nem érinti | Az ékezet-hajtogatást a magyar indokolja, és a magyar támogatott marad; a tövező indokáról a #6 és a #38 szól. |
| 5 | 00 · D-02/3 | „Ez nem karaktermintázat és nem kulcsszólista — magát az indexet kérdezi meg, ezért nyelvfüggetlen.” | indok gyengül | A nyelvfüggetlenség a „minden nyelv” célt szolgálta; két nyelvnél a tulajdonság igaz marad, de előnyként kisebb a súlya. |
| 6 | 00 · D-02/6 | „Nincs „első N karakter" heurisztika és nincs nyelvenkénti hangolás. A kapu miatt a szöveges láb csak pontos kérdéseknél szólal meg, ahol a szótő hossza érdektelen.” | indok gyengül | A nyelvenkénti hangolás elkerülése kilenc nyelvnél nagyobb nyereség volt, mint kettőnél; a második mondat érve (a szótő hossza érdektelen) nyelvtől független, és áll. |
| 7 | 00 · D-02, „A vállalt következmény” | „A ragozott alakok kezelése teljes egészében a beágyazó modellen áll.” | nem érinti | A ragozás főleg a magyar (toldalékoló) tartalom kérdése, a magyar pedig támogatott marad. |
| 8 | 00 · D-04/5, példa | „kategoriak/technikai/typescript.md → mindenhol látszik” · „kategoriak/szemelyes/munkamodszer.md → mindenhol látszik” | nem érinti | A prioritástól független. A példa a 2026-09-05-i angol átnevezés előtti magyar rendszer-mappaneveket mutatja, és nincs átírva (lásd a névtáblázatot). |
| 9 | 00 · D-05/2 (2026-09-15) | „Egy magyar cím bőven tartalmazhat kettőspontot.” | nem érinti | A magyar tartalom támogatott marad; a kettőspont okozta parse-hiba nyelvtől független. |
| 10 | 00 · D-05/4 | „Lemérve: magyar ékezetes kulcs, érték és hierarchikus címke mind hibátlanul átment.” | nem érinti | A magyar támogatott marad. |
| 11 | 00 · D-08, a 2026-09-05-i elnevezési szabály | „Minden azonosító, amit a rendszer maga definiál és fájlba ír, angol. Magyar (vagy bármely más nyelvű) csak a tartalom lehet.” | nem érinti | Már most angol azonosítókat ír elő, összhangban az új prioritással. A „vagy bármely más nyelvű” a tartalomról szóló megengedő mondat, nem támogatási ígéret. |
| 12 | 00 · D-08/3–4 | „Nincs ékezet, nincs speciális karakter a mappanevekben” · „Kisbetű, kötőjel, ékezet nélkül: szerzodes-hatarido.md.” | nem érinti | Az indok bájtszintű (NFC/NFD-eltérés), nyelvtől független. |
| 13 | 00 · D-10/3 | „az „ebben a projektben mindig magyarul kommentelünk" nem döntés és nem is ismeret” | nem érinti | Csak példa. |
| 14 | 00 · D-10, kategória-táblázat | „decisions \| Mit döntöttünk el és miért. A döntés, mikor született, mi volt a másik lehetőség, és miért ezt választottuk.” | nem érinti | A gépi szöveg a D-22 és a D-30/4 óta angol. Az, hogy a táblázat „A promptja” oszlopa magyar szöveget mutat, már e döntés előtt is eltérés volt. |
| 15 | 00 · D-12, D-14, D-16, D-18, D-25, D-31 ábrái és parancsai; 20 · §02, §05, §06, §07, §09 | „naplo/*.jsonl NEM AZ audit napló — fájl, nem adatbázis (D-18)” · „memoria/ a fájlok — csak a szerver írja” · „beagyazo készen kapható szolgáltatás” · „adatbazis ParadeDB” · „szolgal folyamatosan fut” · „karbantart admin-link” | indok erősödik | Magyar nevű rendszer-azonosítók. Az angol prioritás mellett erősebb a Spec 20 §10 következetlenség-érve (angol fa, magyar rendszernév). A nevekről a mondat kifejezetten nem dönt (részletek a névtáblázatban). |
| 16 | 00 · D-22, 2026-09-08 | „A D-30 szerint minden gépnek szóló szöveg angol, és a kategória-prompt ilyen” | nem érinti | Már angol, összhangban az új prioritással. |
| 17 | 00 · D-26/5 | „itt korábban az is szerepelt, hogy a karakter-korlát a magyar tartalmat büntetné. A D-30 óta a kategória-promptok angolul íródnak, tehát ez az érv rájuk már nem áll” | nem érinti | Történeti megjegyzés. |
| 18 | 00 · D-26/6 | „Beépített BPE tokenizáló, ~ előtaggal” | nem érinti | Token-becslésről szól, nem nyelvi tokenizálásról. |
| 19 | 00 · D-26/8 | „A prompt nyelve angol, a felület nyelvétől függetlenül (D-30/4)” | nem érinti | Már angol. |
| 20 | 00 · D-29/8 | „a D-08 névszabályai (angol azonosítók, ékezet és speciális karakter nélküli mappanevek)” | nem érinti | A névszabály változatlan. |
| 21 | 00 · D-30, bevezető | „A felület magyarul és angolul is használható.” | nem érinti | Ez pontosan az a két nyelv, amelyet az új mondat támogatni kér. |
| 22 | 00 · D-30/1 | „Két nyelv, nem több.” · „a két nyelv egyenrangú fordítás a kulcsok alatt, nem egyik a másikból.” | nem érinti | A nyelvkészlet ugyanaz. Az „egyenrangú” és az „angol a prior” viszonyát egyik szöveg sem mondja ki (lásd a nyitott kérdéseket). |
| 23 | 00 · D-30/3 | „Ott a böngésző nyelve dönt: ha magyar, magyar — egyébként angol.” | nem érinti | A visszaesési alapérték már most az angol. |
| 24 | 00 · D-30/4 | „Angolul a legkisebb a kockázat mind a megértésben, mind a token-költségben — magyarul ugyanaz a tartalom kb. kétszer annyi tokenbe kerül (mérések, 10.).” | nem érinti | A gépi kommunikáció már angol, és az indok nem a támogatott nyelvek körén múlik. |
| 25 | 00 · D-30/5 | „A bejegyzések szövege, a projektnevek, a fájlnevek és a törlési indoklások (D-21/9) úgy maradnak, ahogy megírták őket.” | nem érinti | A tartalomra vonatkozik, bármilyen nyelvű. |
| 26 | 00 · D-30, „Amit ez a döntés máshol megváltoztat” | „kiterjeszti ugyanezt a logikát az MCP felületre és a naplózott eseménynevekre.” | nem érinti | Az eseménynevek angolok, az őket tartalmazó mappa (`naplo/`) neve viszont magyar (#15, #36). |
| 27 | 00 · D-30, „Ami könnyen elromlik” | „A második nyelv csendben elavul. Ha az angol katalógus lemarad, azt senki nem veszi észre, aki magyarul használja.” | megváltozik | A kockázatleírás az angolt tekinti lemaradó második nyelvnek; angol prioritás mellett más a szerepek iránya. A néma visszaesés tilalma nyelvtől független. |
| 28 | 00 · D-37/5 (történeti rész) | „a tokenizáló ALTER-rel nem állítható át (nincs ilyen szintaxis)” | nem érinti | FTS5-mérés, a D-43 óta történeti. |
| 29 | 00 · D-38/4 | „És a magyar szöveg entrópiája ugyanabba a sávba esik, mint a valódi kulcsoké; erre publikált mérés nincs.” | nem érinti | A magyar támogatott marad, és a döntés (nincs tartalom-kapu) nem nyelvi alapú. |
| 30 | 00 · D-43/2 és pontosítása | „Van magyar tövező és kapcsolható ékezet-lehagyás, oszloponként más tokenizálóval” · „Ami a ParadeDB-ből ténylegesen kell: a kapcsolható ékezet-lehagyás és az oszloponkénti tokenizáló.” | nem érinti | A magyarhoz kötött igény (ékezet-lehagyás) marad. Angol tövezőt angol szövegen egyik dokumentum sem mért. |
| 31 | 00 · D-43, nyitott pontok, utolsó bekezdés | „a 30-as spec CJK-döntése azért nem hozott be tokenizálót, mert az FTS5-ben nincs ICU; a ParadeDB-ben van beépített CJK-tokenizáló.” | tárgytalan | A kínai, japán és koreai tartalom a „tobbi nyelv most nem erdekes” mondattal kikerül a célok közül. |
| 32 | 00 · D-43, nyitott pontok | „A bench/ kapuzott stratégiája ParadeDB-n. Az elv átvihető, a számok nem. A mérőkészletet újra kell futtatni.” | nem érinti | A pont nyitva marad; új kérdés a korpusz nyelvi összetétele. |
| 33 | 00 · D-45/4 és /6 | „Nyelv: magyarra semmilyen mérés nincs.” · „ha van magyar mérés” | nem érinti | A magyar támogatandó marad, ezért a feltétel is áll. |
| 34 | 20 · §04 Névadás | „kisbetű, elválasztó kötőjel, nincs ékezet és nincs speciális karakter” · „Az ékezetes karakternek nincs egyetlen bájtsorozata.” | nem érinti | Nyelvtől független, bájtszintű indok. |
| 35 | 20 · §06, rendszertáblák | „felhasználói beállítások (nyelv)” | nem érinti | A felhasználónkénti nyelvbeállítás (D-30/2) változatlan. |
| 36 | 20 · §10 Ami nyitva van | „A rendszerfájlok nevei magyarok, a fáé angolok.” · „nyitva — a memória fa mappái angolul vannak (projects/, decisions/), a rendszer fájljai viszont nem (naplo/). A kimondott szabály a markdownba írt mezőnevekre vonatkozik, tehát ez nem szabálysértés — de következetlenség, és most még olcsó átnevezni.” | indok erősödik | A pont következetlenség-érve az angol prioritás mellett erősebb. A tulajdonos mondata erre a listára felelt, de neveket nem mond ki, ezért a pont formálisan nyitva van. |
| 37 | 30 · fejléc (2026-09-22) és §10 | „A bench/ mérőkészlet FTS5-ön mért. A kapuzott stratégia elve átvihető, a szöveges láb számai nem — ParadeDB-n újra kell futtatni” · „nyitva — a bench/ FTS5-ön mért; az elv átvihető, a szöveges láb számai nem (D-43).” | nem érinti | A mérőkészletet a D-43 miatt amúgy is újra kell futtatni; új kérdés a nyelvi összetétel. |
| 38 | 30 · §01 Az indexelés útja | „a saját mérésünk szerint az angol tövező magyarra pontosan semmit nem hoz, a magyar tövező pedig elrontja az alapalakot (kutya → kuty, Budapest → Budapes). Minden további nyelvhez ráadásul külön szabályrendszer kellene.” | indok gyengül | Elesik a „minden további nyelv” érv. Az angol tövező hatását angol szövegen egyik dokumentum sem mérte; a magyar érv áll. |
| 39 | 30 · §01, „Három dolog rögzítendő” | „Ékezet-hajtogatás van (hogy az árak és az arak ugyanaz legyen), tövezés nincs. Sem magyar, sem angol, sem semmilyen más nyelvre.” | indok gyengül | Az ékezet-hajtogatás magyar indoka áll. A „sem angol” tövezés-szabály indoka a #38 szerint gyengül. |
| 40 | 30 · §02 A keresés útja | „A használt beágyazó modell a kérdésre instrukciós előtagot vár (Instruct: {feladat}\nQuery:{kérdés}), a dokumentumokra nem.” | nem érinti | Modellhez kötött, nem nyelvhez; a Spec 30 a modellt nem nevezi meg. |
| 41 | 30 · §03 A kapu | „Ezért nyelvfüggetlen: ugyanúgy működik magyarra, törökre és kínaira, és nem kell hozzá szótárat vagy mintázatlistát karbantartani.” | indok gyengül | A példanyelvek (török, kínai) kikerülnek a célok közül. A karaktermintázat ellen szóló mérési érv (`bun run release`) nyelvtől független, és áll. |
| 42 | 30 · §09 Szóköz nélküli írásrendszerek | „A döntés: nem építünk CJK-tokenizálót.” · „2026-09-22 — az indoklás megszűnt, a döntés áll (D-43)” · „CJK tartalmon a beágyazó kiesése teljes keresés-kiesést jelent.” | tárgytalan | A szakasz tárgya (kínai, japán és koreai tartalom) kikerül a célok közül. |
| 43 | 30 · §10, „Kínai és más szóköz nélküli írásrendszerek” | „nyitva — a szöveges láb ezekre nem működik; a jelentés-láb viszi az egészet. Mérve; hogy kell-e CJK-tokenizáló, még nem dőlt el.” | tárgytalan | Csak a CJK-nyelvek miatt volt nyitott. Mellékesen ellentmond a §09 „A döntés: nem építünk CJK-tokenizálót” mondatának. |
| 44 | 30 · „Ami ebben a fájlban nincs” | „a D-30/4 szerint angolul” | nem érinti | Csak hivatkozás. |
| 45 | 40 · §02, „A leírások alakja” | „És mindez angolul (D-30/4) — a felület nyelvétől függetlenül.” | nem érinti | Gépi felület, már angol. |
| 46 | 60 · §02, D-30/2 megjegyzés | „Két nyelv van, magyar és angol, és a választás a felhasználó fiókjához tartozik, nem a böngészőhöz” | nem érinti | A nyelvkészlet változatlan. |
| 47 | 60 · §02, a Beállítások/Felület drótváza | „A felület nyelve” · „Magyar” · „English” · „A kategória-promptok nyelve NEM ez — azok mindig angolul íródnak.” | nem érinti | Változatlan. A választóban a „Magyar” áll elöl, és a drótvázak magyar felületet mutatnak (lásd a nyitott kérdéseket). |
| 48 | 60 · §08 Kategóriák és promptok | „A prompt angolul íródik — a hívó agent kapja meg, nem a felület nyelve számít.” · a diff-példa: „− ... és írd le, mi volt a másik lehetőség.” | nem érinti | A gépi szöveg angol. A diff-példa magyar szövege már eddig is eltért a D-30/4-től. |
| 49 | 60 · §10 Első indítás | „Maga a lap a böngésző nyelvén jelenik meg, mert itt még nincs kitől megkérdezni — ha az nem magyar, angolul (D-30/3).” | nem érinti | A visszaesés már angol. |
| 50 | 60 · §11 Import | „Elutasítva — ékezetes mappanév: projects/webshop/döntések/x.md” | nem érinti | Névszabály (D-08), nyelvtől független. |
| 51 | 60 · §14 Amit el kell dönteni | „A felület nyelve → D-30: magyar és angol, a Beállítások „Felület" lapján; a gépi kommunikáció mindig angol.” | nem érinti | Változatlan. |
| 52 | 90 · §02 A korpusz | „magyar, angol, német, lengyel, török, kínai, finn, orosz, spanyol. Mind a kilenc ugyanazt a 12 témát fedi le, természetes megfogalmazásban — nem fordításban.” · „A teljes korpuszon keresnek, tehát a többi nyelv zavaró tételként viselkedik.” | tárgytalan (részben) | Hét nyelv kikerül a célok közül; a korpusz leírása történeti adat. |
| 53 | 90 · §02, „azonosito” kérdéstípus | „ezért mind a kilenc nyelv megfelelő dokumentuma helyes találat” | nem érinti | Pontozási szabály, a történeti számok értelmezéséhez kell. |
| 54 | 90 · §03 Eredmények | „Futtatva: 2026-08-20, Qwen3-Embedding-8B-4bit-DWQ, 4096 dimenzió” · „130 DOKUMENTUM (22 ZAVARÓ), 108 KÉRDÉS, 9 NYELV” · „kapuzott \| 69,4% \| 96,3% \| 0,807 \| 0,855” | indok gyengül | Minden összesített szám mind a kilenc nyelvre szól. A kapuzott előnye 0,004, és a §06 éppen erről a nagyságról írja, hogy „nem jelent semmit”. |
| 55 | 90 · §03, 3. megállapítás | „Így a hatos szám, a nyelvenkénti hangolás és az egész heurisztika kiesik a tervből” | indok gyengül | A nyelvenkénti hangolás elkerülése kilenc nyelvnél nagyobb nyereség volt. |
| 56 | 90 · §03, „A vállalt következmény” | „A ragozás kezelése teljes egészében a beágyazó modellen áll. Mivel a modell konfigurálható, egy gyengébb modellel nincs mögötte tartalék.” | nem érinti | A ragozás főleg magyar kérdés, a magyar pedig marad. |
| 57 | 90 · §04 Nyelvenként, a hét másik nyelv sora | „török \| 0,871 \| 0,871 \| 0,901 \| kapuzott, +0,030” … „német \| 0,753 \| 0,797 \| 0,784 \| vak fúzió, +0,013” (és a lengyel, orosz, kínai, finn, spanyol sor) | tárgytalan | Ezek a nyelvek kikerülnek a célok közül; történeti adat. |
| 58 | 90 · §04, magyar sor | „magyar \| 0,897 \| 0,854 \| 0,928 \| kapuzott, +0,074” | nem érinti | A magyar támogatandó marad, és ez a sor továbbra is a kapuzott mellett szól. |
| 59 | 90 · §04, angol sor | „angol \| 0,746 \| 0,865 \| 0,777 \| vak fúzió, +0,088” | indok gyengül | A prioritásnyelven a vak fúzió nyer, a táblázat legnagyobb különbségével. A §06 mércéje szerint már „egy 0,074-es [különbség] igen” jelent valamit, ez pedig 0,088. A D-02 indoka ezzel gyengül. |
| 60 | 90 · §04, záró bekezdés | „a kapuzott a toldalékoló nyelveken nyer (magyar, török, lengyel), a vak fúzió az analitikusakon (angol, német, spanyol). A magyar — a fő cél szerint kiemelt nyelv — a legnagyobb különbséggel a kapuzott mellett szól” | megváltozik | A hivatkozott premissza („a fő cél szerint kiemelt nyelv”) a régi D-01/3; az új szöveg szerint az angol a prior. |
| 61 | 90 · §05 Külső, publikált mérések | „Azt támasztják alá, hogy a választott modellcsalád magyarul erős.” (MTEB BelebeleRetrieval hun_Latn; Antal Margit, 2025) | nem érinti | A magyar érv áll; angolra vonatkozó külső mérés a dokumentumban nincs. |
| 62 | 90 · §05 | „a magyar-specifikus huBERT alulmarad a nagy multilingvális modellekkel szemben — nem érdemes magyar modellt keresni.” | nem érinti | A magyar marad, és a többnyelvű modell két nyelvnél is kell. |
| 63 | 90 · §05, „Amit szándékosan kihagytunk” | „a baseline hardkódolt stemmer_language="english"-gel futott magyar szövegen” | nem érinti | Egy magyar adatra vonatkozó kizárás indoka. |
| 64 | 90 · §06 A mérés korlátai | „A nyelvenkénti számok nem alkalmasak a nyelvek összehasonlítására.” · „a jelentés-keresés a rossz találatok több mint felénél ugyanannak a ténynek a más nyelvű változatát adta vissza” · „Nyelvfüggetlen pontozással az összesített érték 0,824-ről 0,920-ra ugrik, de nyelvenként nagyon eltérő mértékben.” | nem érinti | Korlát, ami az angol és a magyar sor olvasásához kell: a párhuzamos, kilencnyelvű szerkezet a jelentés-keresés számait is lehúzta. |
| 65 | 90 · §06 | „11 magyar, 6 angol, 2 lengyel, 1 német, 1 spanyol, 0 a többinél.” | nem érinti | Történeti adat; a magyar és az angol sort eltérő számú zavaró mellett mérték. |
| 66 | 90 · §06 | „A szöveges lábak kínaira nem működnek.” · „Ha ez valaha kevés, CJK-tokenizáló kell.” | tárgytalan | A kínai kikerül a célok közül. |
| 67 | 90 · §06, „Egy tanulság, ami nem műtermék” | „A többnyelvű beágyazó modell nem garantálja, hogy a kérdés nyelvén adja vissza a találatot. Ha ugyanaz a tény két nyelven is szerepel a memóriában, bármelyiket hozhatja.” | nem érinti | Angol és magyar memóriára is áll. |
| 68 | 90 · §09 Skálázás | „A szóba jövő modellekre (multilingual-E5, MiniLM, BGE-M3) nincs egyesével mért CPU-késleltetés.” · „a saját gépünkön, magyar rövid lekérdezésekkel.” | indok gyengül | A tervezett késleltetés-mérés csak magyar lekérdezést nevez meg; a magyar kiemelése a régi D-01/3-hoz illett. |
| 69 | 90 · §10 Kategória-prompt | „A magyar szöveg token-többlete az azonos tartalmú angolhoz képest \| kb. 2×” | nem érinti | A D-30/4 indoka, változatlan. |
| 70 | 90 · §10, „Nyitott mérés” | „Hogy tipikusan mekkora az eltérés magyar és angol kategória-promptokon, azt a szállított öt kategórián kell kimérni.” | nem érinti | A promptok a D-30/4 óta angolok; a magyar fele már e döntés előtt tárgytalan volt. |
| 71 | 90 · §13, „Szóköz nélküli írásrendszerek (CJK)” | „kínai 56,1 · japán 31,2 · koreai 37,1” · „BGE-M3: zh 63,9 · ja 75,2 · ko 72,2” · „219 MB (mecab-ko-dic)” | tárgytalan | Csak a CJK-nyelvekre szól; történeti adat. |
| 72 | 90 · §13 és „Nyitott mérések” | „arra, hogy a trigram tokenizáló mennyivel rontaná a magyar BM25-relevanciát a unicode61-hez képest, nincs mérés.” · „Ha egyszer mégis kell CJK-támogatás, az indexméret-szorzót és a magyar relevancia-romlást a saját tartalmunkon kell kimérni” | tárgytalan | Elesik a mérés kiváltó oka, a CJK-támogatás. |
| 73 | 90 · §15, saját mérések | „Prefix-vágás haszna ragozott kérdéseken \| lex 0,279 · lexs 0,332 · lexp 0,721” | nem érinti | A kilencnyelvű korpuszon mért történeti adat; a prefix-láb nincs a tervben. |
| 74 | 90 · §15, külső mérések | „Nem angol lekérdezések recall@5-je többnyelvű beágyazóval \| 13% → 63%” · „ez a magyar tartalom szempontjából alapvető.” | nem érinti | A többnyelvű beágyazó a magyar miatt továbbra is szükséges. |
| 75 | 90 · §15, YAML-csapdák | „egy magyar cím vagy címke bőven tartalmazhat kettőspontot.” | nem érinti | Lásd a #9-et. |
| 76 | 90 · §16 Tartalom-kapu | „Magyar szövegre nincs publikált mérés; a kampány saját, illusztratív becslése szerint az átlagos magyar mondat is ide esik (~4,1–4,5).” | nem érinti | Lásd a #29-et. |
| 77 | 90 · §17 Üzemeltetés | „2–4 KB magyar törzs” · „unicode61 remove_diacritics 2” | nem érinti | FTS5-höz tartozó történeti mérés, a §17 maga is így jelöli. |
| 78 | 90 · §18, „Magyar nyelv” sor | „stemmer=hungarian (Snowball) és kapcsolható ascii_folding, oszloponként más tokenizáló. Az ő/ű betűt a ParadeDB saját Tantivy-forkja o/u-ra képezi. A tövezést nem használjuk” | nem érinti | A magyar marad; angol tövezőt nem mértek. |
| 79 | 90 · §18, „Szóköz nélküli írásrendszerek” sor | „chinese_compatible, lindera (kínai CC-CEDICT, japán IPADIC, koreai KoDic szótárral), icu, jieba” | tárgytalan | A CJK kikerül a célok közül. |
| 80 | 90 · §18, „Összevetési alap: sima Postgres” | „A beépített magyar Snowball-tövező egy független vizsgálatban (Endrédy, 2015) a leggyengébb volt a magyar tövezők között.” | nem érinti | A magyar marad. |
| 81 | 90 · §19 Dream | „A Qwen3-Embedding viselkedése tagadásra és ellentmondásra.” | nem érinti | Nem nyelvi kérdés. |
| 82 | 90 · §20 Jev | „Magyar nyelven \| nincs mérés \| Két külön kör célzottan kereste. Más nyelveken a szórt adatok nyelvváltáskor romlást mutatnak.” | nem érinti | Lásd a #33-at. |
| 83 | 90 · §21 Amit nem mértünk | „A használt modell abszolút értékei (magyaron 0,897–0,928) önmagukban elégségesek; a relatív veszteség nem befolyásol egyetlen tervezési döntést sem.” | indok gyengül | A lezárás csak magyar értékekre hivatkozik; ugyanennek a futásnak az angol értékei (0,746–0,865) nem szerepelnek benne. |

Megjegyzések a kereséshez:
- A 50-uzemeltetes.html-ben a teljes kulcsszólistára (nyelv, magyar, angol, CJK, tövező, ékezet, tokenizáló, Qwen és társaik) nincs nyelvi vonatkozású találat.
- Nem nyelvi prioritásról szól, ezért kimaradt: „Kilenc tételre bontva” (00 · D-01), „mind a kilenc megvizsgált több-motoros adatréteg” (00 · D-34/6), „a táblázat a kilenc mérés tartománya” (90 · §18/E), „a domén nyelvén” (00 · D-34), „nyelvtan-vezérelt” (40 · §02), „nagy nyelvi modellt” (00 · D-45/2), „granite-embedding … többnyelvű” (90 · §09, késleltetésmérés).

## A beágyazó modell és a keresési stratégia indoka

### Hol van „kimondva”

- **Kapuzott stratégia**: a D-02 rögzíti, és a 90 §03–§04-re hivatkozik („Alátámasztás: 90-meresek.html (a mérések elfogadva)”).
- **Beágyazó modell**: egyetlen D-tétel sem nevezi meg. A D-01/2 annyit mond, hogy „A rendszerben egyetlen modell fut: a beágyazó”, a D-01/4 pedig, hogy a modell konfigurációból jön. A konkrét modell csak a 90-ben szerepel:
  - §03: „Qwen3-Embedding-8B-4bit-DWQ, 4096 dimenzió, oMLX végponton”;
  - §05: „a választott modellcsalád”;
  - §19: „A Qwen3-Embedding viselkedése …”;
  - §21: „A használt modell”.

  A Spec 30 §02 modellhez kötött instrukciós előtagot ír elő (`Instruct: {feladat}\nQuery:{kérdés}`), de a modell nevét nem mondja ki. Jelöltként a 90 §09 a multilingual-E5-öt, a MiniLM-et és a BGE-M3-at nevezi meg; a jina-embeddings-v3 a licence miatt kiesett.

### Mit indokolt a kilenc nyelv

**A keresési stratégiánál** a kilenc nyelv kétféleképpen jelent meg.

1. **A mérés hatóköreként.** A 108 kérdés 9 × 12 kérdésből áll, a többi nyelv zavaróként szerepel. Összesítve a kapuzott 0,855, a vak fúzió 0,851, a különbség 0,004. A 90 §06 ugyanerről a nagyságról írja: „Egy 0,004-es különbség nem jelent semmit”. Kérdéstípusonként (kapuzott / vak fúzió):

   | Kérdéstípus | kapuzott | vak fúzió |
   |---|---|---|
   | azonosító | 1,000 | 1,000 |
   | rokon értelmű | 0,700 | 0,650 |
   | ragozott | 0,864 | 0,902 |

   Nyelvenként nyelvi bontás típusonként nincs a dokumentumban.
2. **Tervezési értékként:**
   - D-02/3: „ezért nyelvfüggetlen”;
   - D-02/6: „nincs nyelvenkénti hangolás”;
   - 90 §03/3: „a hatos szám, a nyelvenkénti hangolás és az egész heurisztika kiesik a tervből”;
   - Spec 30 §03: „ugyanúgy működik magyarra, törökre és kínaira”;
   - Spec 30 §01: „Minden további nyelvhez ráadásul külön szabályrendszer kellene.”

A konkrét, nyelvenkénti érv a magyaron keresztül született. A 90 §04 szerint: „A magyar — a fő cél szerint kiemelt nyelv — a legnagyobb különbséggel a kapuzott mellett szól, és ott a vak fúzió még a tiszta jelentés-keresésnél is rosszabb.”

A nyelvenkénti eredmény (90 §04):

| Melyik nyer | Nyelv és különbség |
|---|---|
| kapuzott | magyar (+0,074), lengyel (+0,061), török (+0,030) |
| döntetlen | orosz, kínai |
| vak fúzió | angol (+0,088), spanyol (+0,023), német (+0,013), finn (+0,005) |

Egy összefüggés a §03-ból: a §04 „vak fúzió” oszlopa a „vak fúzió (lexp+dense)” változat, 0,851 összesítve. Ez hat karakterre vágott prefixet használ, vagyis éppen azt a heurisztikát, amelynek elhagyását a §03/3 részben a „nyelvenkénti hangolás” elkerülésével indokolja.

**A beágyazó modellnél** a dokumentumok nem állítják, hogy a modellt a kilenc nyelv miatt választották. A felhozott indokok magyar-központúak:
- MTEB BelebeleRetrieval, hun_Latn: Qwen3-Embedding-8B 0,9799, a táblázatban az első, az élő rangsorban „a harmadik hely” (90 §05);
- Antal Margit (2025): a multilingvális modellek jobbak, mint a magyar-specifikus huBERT;
- a többnyelvű beágyazó szükségessége: „Nem angol lekérdezések recall@5-je … 13% → 63%” (90 §15);
- a saját magyar értékek: „magyaron 0,897–0,928” (90 §21).

A kilencnyelvű mérőkészlet a modell többnyelvűségét gyakorolta, de a modell mellett felhozott külső bizonyíték csak magyar.

### Mi marad az indokból angol + magyar mellett

Ami áll (nyelvtől független, vagy magyar):
- Az azonosító-probléma: a hasonló jegyszámoknál (PROJ-4412 / PROJ-4413) a jelentés-keresés 1,000-ről 0,908-ra esik. Ez indokolja a szöveges lábat, és nem nyelvfüggő.
- A kapu mechanizmusa (az indexet kérdezi) mindkét nyelven ugyanúgy működik. A karaktermintázatos változat bukása (`bun run release`) nyelvtől független.
- A magyar sor: kapuzott +0,074, a vak fúzió itt a tiszta jelentés-keresésnél (0,897) is rosszabb (0,854).
- A modell magyar alátámasztása (Belebele, Antal, 13% → 63%, 0,897–0,928) teljes egészében áll, mert a magyar támogatandó marad.
- A D-02 vállalt következménye („A ragozott alakok kezelése teljes egészében a beágyazó modellen áll.”) főleg a magyart érinti, és ugyanúgy áll.

Ami gyengül vagy ellene szól:
- Az angol sor: a vak fúzió +0,088-cal nyer, a táblázat legnagyobb különbségével. A tiszta jelentés-keresés angolon 0,746, a kapuzott 0,777, a vak fúzió 0,865.
- A két sor egyszerű átlaga (saját számolás, nem mérés): kapuzott 0,853, vak fúzió 0,860, csak jelentés 0,822. Fenntartások, mind a dokumentumokból:
  - nyelvenként csak 12 kérdés van (90 §06);
  - a többi hét nyelv zavaróként végig benne volt a korpuszban (90 §02);
  - a jelentés-keresés hibáinak több mint fele más nyelvű párhuzamos változat volt (90 §06);
  - a zavarók eloszlása egyenetlen, 11 magyar és 6 angol (90 §06);
  - a szöveges láb számai FTS5-ön készültek, és ParadeDB-n újra kell futtatni őket (D-43, 90 §18).
- A „nyelvfüggetlen” (D-02/3, Spec 30 §03) és a „nincs nyelvenkénti hangolás” érv (D-02/6, 90 §03/3, Spec 30 §01) súlya két nyelvnél kisebb, mint kilencnél.
- A 90 §04 záró mondatának premisszája („a fő cél szerint kiemelt nyelv”) megváltozott.
- A modellre: angolra vonatkozó külső mérés a dokumentumokban nincs. A saját futásban az angol jelentés-keresés értéke (0,746) a legalacsonyabb az oszlopban. A 90 §06 szerint viszont „A nyelvenkénti számok nem alkalmasak a nyelvek összehasonlítására”, ezért ebből a modell angol erősségére nem lehet következtetni.
- A 4 bites kvantálás lezárása (90 §21) csak a magyar értékekre hivatkozik.

## A mérések nyelvi adatai

A 90 saját szabályai a korábbi számok sorsáról:
- §15: „ha valami a kutatásban megvan, de itt nincs, akkor ide kell bemásolni, nem onnan kitörölni”;
- §18: „A korábbi kampányok szakaszai (8–16.) történeti feljegyzések … Nem írjuk át őket.”;
- §18: „A 2–7. szakasz keresési mérései (a bench/) is FTS5-ön készültek: a kapuzott stratégia elve átvihető, a szöveges láb számai nem”.

A kilenc nyelvre szóló számok tehát már az FTS5 miatt is részben történetiek. Nyelvi okból egyik sincs „történeti” jelöléssel ellátva.

| Szakasz | Mire szól nyelvileg | Állapot | Megjegyzés |
|---|---|---|---|
| §02 A mérőkészlet | 9 nyelv, 9 × 12 dokumentum, 9 × 12 kérdés, 22 zavaró | történeti adat | A §06 eloszlása („11 magyar, 6 angol, 2 lengyel, 1 német, 1 spanyol, 0 a többinél”) 21-et ad ki, a §02 és a §03 22 zavarót említ. Ezt a dokumentumok nem magyarázzák. |
| §03 Eredmények | a 9 nyelv összesítése, más nyelvre is szól | történeti adat (FTS5 és 9 nyelv) | Ez a D-02 hivatkozási alapja; angol + magyar részre a dokumentumból nem bontható. |
| §04 Nyelvenként | 7 sor más nyelvre szól, 2 sor angolra és magyarra | a 7 sor történeti, a magyar és az angol sor érvényes (FTS5-fenntartással) | Az angol és a magyar sor ellentétes irányba mutat (#58, #59). |
| §05 Külső mérések | csak magyar (hun_Latn; magyar céges Q&A, HuRTE) | érvényes | Angol külső mérés nincs. |
| §06 A mérés korlátai | kínai szöveges láb; zavarók nyelvenként; nyelvközi pontozás (0,824 → 0,920) | a kínai sor történeti; a többi az értelmezés kerete | A „két nyelven is szerepel” tanulság angol + magyarra is áll. |
| §09 Skálázás | késleltetés többnyelvű modellekkel; a tervezett saját mérés „magyar rövid lekérdezésekkel” | érvényes | A terv csak magyar lekérdezést nevez meg. |
| §10 Kategória-prompt | „A magyar szöveg token-többlete … kb. 2×”; nyitott mérés magyar és angol promptokon | érvényes; a nyitott mérés magyar fele a D-30/4 óta tárgytalan | — |
| §13 CJK | MIRACL zh/ja/ko; trigram-szorzó; koreai szótár 219 MB | történeti, csak más nyelvekre szól | A nyitott mérés („Ha egyszer mégis kell CJK-támogatás …”) tárgytalan. |
| §15 Pótolt számok | prefix-vágás (9 nyelvű korpusz); 13% → 63% (nem angol lekérdezés); magyar YAML-kettőspont | a prefix-szám történeti; a 13% → 63% és a YAML érvényes | — |
| §16 Tartalom-kapu | a magyar mondat entrópiája (becslés, nem mérés) | érvényes | — |
| §17 Üzemeltetés | magyar törzsű szintetikus korpusz, FTS5 `remove_diacritics 2` | történeti (az FTS5 miatt, nem nyelvi okból) | — |
| §18 ParadeDB | „Magyar nyelv” sor; CJK-tokenizálók sora; magyar Snowball (Endrédy 2015) | a magyar sorok érvényesek; a CJK-sor csak más nyelvekre szól | Angol tövezőről nincs adat. |
| §20 Jev | „Magyar nyelven \| nincs mérés”; „Más nyelveken … romlást mutatnak” | érvényes | — |
| §21 Amit nem mértünk | a 4 bites lezárás magyar értékekkel (0,897–0,928) | érvényes magyarra | Angolra nem mond semmit. |

Összefoglalva: más nyelvre szóló szám a §02-ben, a §03-ban (az összesítés részeként), a §04 hét sorában, a §06 kínai és zavaró-eloszlás sorában, a §13-ban és a §18 CJK-sorában van. Ezek a saját feltételeik között történeti adatként helyesek; a dokumentum szabályai szerint nem törlendők.

## Magyar nevű rendszerfájlok és -mappák

**Mit mond most a Spec 20 (§10, „Ami nyitva van”), szó szerint:**
„A rendszerfájlok nevei magyarok, a fáé angolok.” — „nyitva — a memória fa mappái angolul vannak (projects/, decisions/), a rendszer fájljai viszont nem (naplo/). A kimondott szabály a markdownba írt mezőnevekre vonatkozik, tehát ez nem szabálysértés — de következetlenség, és most még olcsó átnevezni. 2026-09-22: az adat.sqlite és a beagyazas.sqlite a D-43-mal megszűnt; a táblanevek még nincsenek kimondva.”

**A szabály szövege máshol, összevetésül:**
- **D-08 (2026-09-05):** „Minden azonosító, amit a rendszer maga definiál és fájlba ír, angol. […] Ez érinti a gyökereket (projects/, knowledge/, personal/), a kategóriákat (D-10) és a fejléc-mezőket (D-06: tags, modified, prompt_version).”
- **D-30:** „Az „amit a rendszer definiál és fájlba ír, az angol" szabály eddig a mappanevekre, kategóriákra és fejléc-mezőkre vonatkozott. Ez a döntés nem lazít rajta, hanem kiterjeszti ugyanezt a logikát az MCP felületre és a naplózott eseménynevekre.”

Ténymegállapítás: a Spec 20 §10 szűkebben írja le a szabályt („a markdownba írt mezőnevekre vonatkozik”), mint a D-08 és a D-30 saját szövege, amely a mappanevekre is kiterjed. A §10 egyetlen mai magyar példát nevez meg, a `naplo/`-t. A lenti nevek többségét nem említi.

A még ki nem mondott nevek nyelve sincs rögzítve:
- a Postgres-sémák: „A sémák neve még nincs kimondva.” (D-43/9);
- a táblák: „a táblanevek még nincsenek kimondva” (Spec 20 §10);
- a kategória-definíciók fájlja (D-22/1), a beállítófájl (D-16/3) és az üzemeltetési napló fájlja (D-40): ezeknek egyik dokumentum sem ad nevet.

**Futó rendszer, a mai terv szerint**

| Név | Hol szerepel | Mire való |
|---|---|---|
| `memoria/` | 00 · D-08 fa-ábra; D-14 szerver-ábra („memoria/ a fájlok — csak a szerver írja”); 20 · §02 fa-ábra, §05 verziók-ábra, §09 táblázat („memoria/**”) | A markdown tartalomfa gyökere, a `projects/`, `knowledge/` és `personal/` fölött. A Spec 20 §10 nem sorolja a magyar rendszernevek közé. |
| `naplo/` (benne `*.jsonl`) | 00 · D-12 ábra („naplo/*.jsonl NEM AZ audit napló”), D-18 ábra; 20 · §06 ábra és táblázat, §07 ábra, §09 táblázat, §10 | Az audit napló havi szegmenseinek mappája. A szegmensnevek (`2026-09.jsonl`, `2026-09.002.jsonl`) dátumok, nyelvsemlegesek. Ez a Spec 20 §10 egyetlen megnevezett példája. |
| `adatbázis/` | 00 · D-14 szerver-ábra („adatbázis/ ParadeDB, a szerver saját kötetén (D-43)”) | A ParadeDB kötete a szerveren. Az ábra ékezettel írja; hogy tényleges mappanév-e, az ábrából nem derül ki. |
| `szolgáltatás` | 00 · D-14 szerver-ábra („└── szolgáltatás felület + agent-hozzáférés”) | A fa harmadik eleme, perjel nélkül; nem egyértelmű, hogy mappa. |
| `beagyazo` (konténernév, nem fájl) | 00 · D-16 docker-compose ábra („beagyazo készen kapható szolgáltatás”; „Korábban két konténer volt: app és beagyazo.”) | A beágyazó szolgáltatás konténere. |
| `adatbazis` (konténernév, nem fájl) | 00 · D-16 docker-compose ábra („adatbazis ParadeDB — Postgres + pg_search + pgvector”) | A ParadeDB-konténer. |
| `szolgal` (üzemmód, nem fájl) | 00 · D-16 („A programon belül: szolgal folyamatosan fut”) | A program folyamatosan futó üzemmódja. |
| `karbantart`, `karbantart admin-link` (parancs, nem fájl) | 00 · D-16 ábra és D-16/4 („A kézi karbantart parancs”); D-25 ábra („szerveren: karbantart admin-link → új egyszeri link”) és D-25/4; D-31 („karbantart admin-link → új egyszeri beállító link”); 60 · §09 | Kézi karbantartó futás, illetve új egyszeri admin-beállító link kérése. |

**Megszűnt vagy elavult, de a szövegben szerepel**

| Név | Hol szerepel | Mire való |
|---|---|---|
| `adat.sqlite` | 00 · D-12 „Korábban” lista; 20 · §06 „Korábban”, §09 lábjegyzet, §10 | Felhasználók, projektek, jogok. Megszűnt 2026-09-22-én (D-43). |
| `beagyazas.sqlite` | 00 · D-12 „Korábban” lista; 20 · §06, §09, §10 | Beágyazás-gyorsítótár. Megszűnt 2026-09-22-én. |
| `naplo/index.sqlite` | 00 · D-18/5; 20 · §06, §07, §09 | A napló kísérő indexe; 2026-09-22 óta tábla a ParadeDB-ben. |
| `naplo/.index/` | 00 · D-18 ábra („2026-09-22 — a D-43 óta a .index/ nem mappa, hanem tábla”) | Ugyanez a kísérő index, mappaként. |
| `kategoriak/`, `technikai/`, `szemelyes/` | 00 · D-04/5 példája (ma is így áll) | A 2026-09-05-i angol átnevezés előtti kategória-mappák; a példa nincs átírva. |
| `projektek/`, `tudas/`, `sajat/`; `cimkek`, `modositva` | 00 · D-08 („Ami korábban itt állt”) | Régi gyökerek és fejlécmezők, 2026-09-05-én átnevezve. |
| `ugyfelek/` | 00 · D-08 („Mi változott 2026-09-01-én”) | Régi gyökér. |
| `cim`, `kategoria`, `verzio` | 90 · §15 (a YAML-próba kimenete: „{cim: Acme — szerződés,kategoria: ugyfel,verzio: 1.2,…}”) | Régi magyar fejlécmezők a próbaadatban. |

**Fejlesztői tár és dokumentáció (nem futásidejű)**

| Név | Hol szerepel | Mire való |
|---|---|---|
| `bench/yaml-teszt.ts` | 00 · D-05 megjegyzés; 90 · §15 | YAML-próbaszkript. |
| `bench/uzemeltetes/` és benne: `futtat-meret.sh`, `futtat-index.sh`, `wal-visszanyeres.ts`, `pillanatkep.ts`, `hibaesetek.ts`, `torolt-tartalom.ts`, `fts5-szerkezet.ts`, `wal-kontroll.ts` | 90 · §17 | Az SQLite-os üzemeltetési mérések szkriptjei. |
| `bench/postgres/probak.sh`, `mentes-ido.sh`, `kimenet-a/b/c.txt`, `kimenet-e1/e2/e3.txt` | 00 · D-43 fejléc („Próbák: bench/postgres/”); 90 · §18 | Postgres-próbák és kimeneteik. |
| `eredmeny.json` | 90 · §02, reprodukálás | A mérőkészlet kimeneti fájlja. |
| `bejegyzes`, `beagyazas` (táblák) | 90 · §17, „A mérés környezete” | A próba-adatbázis táblái. |
| `ragozas`, `szinonima`, `azonosito` | 90 · §02, kérdéstípusok | A mérőkészlet kérdéstípus-azonosítói. |
| `docs/research/adatbazis-illeszto/` | 00 · D-34 fejléc; 90 · §13 | Kutatási tár. |
| `docs/research/mcp-felulet/`, `mcp-hibak/` | 00 · D-35 fejléc; 40 · bevezető és zárósor (csak a `mcp-felulet/`); 90 · §13 | Kutatási tárak. |
| `docs/research/mentes-frissites/` | 00 · D-36, D-37 fejléc; 90 · §14 | Kutatási tár. |
| `docs/research/tartalom-kapu/` | 00 · D-38 fejléc, D-44/2; 90 · §16 | Kutatási tár. |
| `docs/research/uzemeltetes/` | 00 · D-39–D-42 fejléc; 50 · bevezető és zárósor; 90 · §17 | Kutatási tár. |
| `docs/research/kategoria-prompt/kivonat.md`, `import-export/kivonat.md`, `kereses-indexeles/kivonat.md` | 90 · §10, §11, §12 | Kampány-kivonatok. |
| `docs/research/memoriabol/` | 90 · §18 | Korábbi saját próba (tövező). |
| `router-rangsor/` | 00 · D-44/2 | Korábbi kutatási kampány. |
| `00-dontesek.html`, `20-adatmodell.html`, `30-kereses.html`, `50-uzemeltetes.html`, `60-felulet.html`, `90-meresek.html` | a spec-fájlok neve; hivatkozás pl. 00 · D-02 és D-03 („Alátámasztás: 90-meresek.html”) | A specifikáció dokumentumai. A `40-mcp.html` neve nyelvsemleges. |

Összevetésül a már angol vagy nyelvsemleges rendszernevek: `projects/`, `knowledge/`, `personal/`, `decisions/`, `mistakes/`, `procedures/`, `facts/`, `preferences/`, `versions/`, `.versions/`, `manifest.json`, `export-….zip`, `app` (konténer), `/setup/…`, a régi `index.sqlite` és `index/`, `QA.md`, valamint a `docs/research/cjk/`, `dream/`, `jev/` és `paradedb/`.
A tartalom példanevei (`szerzodes-hatarido.md`, `stripe-webhook-ujraprobalkozas.md`, `kodstilus.md`, `fizetesi-hibakodok.md`, `modulok/`, `fizetes/` stb.) a D-08 szerint a felhasználó tartalmához tartoznak, nem rendszernevek.

## Nyitott kérdések, amiket a döntés felvet

1. Mi a D-01/3 új, szó szerinti szövege, és a régi szöveg hogyan kerül mellé „Korábban”-ként, a napló szokása szerint?
2. Mit jelent a „prior” a gyakorlatban? Minőségi mércét (az angolon mért keresési minőség a döntő), alapértelmezést (felület, visszaesés), vagy sorrendet arra az esetre, ha a két nyelv érdeke ütközik?
3. Ha az angol és a magyar mérés ellentétes irányba mutat (90 §04: angolon a vak fúzió +0,088, magyaron a kapuzott +0,074), melyik dönt?
4. Érinti-e a D-02 státuszát, hogy az alátámasztó mérés prioritásnyelvén a másik stratégia nyert? A napló munkamódszere szerint („Egy lezárt döntést nem nyitok újra.”) ki és mi alapján dönt erről?
5. A mérőkészlet ParadeDB-n esedékes újrafuttatásánál (D-43, Spec 30 §10) milyen legyen a korpusz nyelvi összetétele: maradjon a kilenc nyelv, vagy legyen angol és magyar? És mennyiben műterméke az angol sor a párhuzamos, kilencnyelvű korpusznak (90 §06: a hibás jelentés-találatok több mint fele más nyelvű változat)?
6. Mi alapján ítélhető meg a beágyazó modell angol teljesítménye, ha a 90 csak magyar külső mérést tartalmaz? Kell-e ehhez külső vagy saját angol mérés?
7. Érvényes-e angolra a 4 bites kvantálás lezárása (90 §21), amely csak magyar értékekre hivatkozik?
8. A tervezett késleltetés-mérés (90 §09) továbbra is csak „magyar rövid lekérdezésekkel” készül?
9. A „tövezés nincs … sem angol” szabály (Spec 30 §01) mögött nincs mérés angol tövezőről angol szövegen. Számít-e ez a D-02/6 kapu-érve mellett, és mit jelent a ParadeDB oszloponkénti tokenizálója (D-43/2) ebből a szempontból?
10. Lezártnak tekinthető-e a Spec 30 CJK-pontja? A §09 szerint „A döntés: nem építünk CJK-tokenizálót”, a §10 szerint „még nem dőlt el”. És mit jelent a „most” a „tobbi nyelv most nem erdekes” mondatban: ideiglenes kizárást vagy tartós célt?
11. Mit vállal a rendszer, ha a tartalom mégis más nyelven íródik? A D-08 („vagy bármely más nyelvű”) és a D-30/5 ezt megengedi; ma egyedül a CJK-kockázat van kiírva (Spec 30 §09, „Amit ez a döntés kockáztat”).
12. Hogyan viszonyul a D-30/1 „a két nyelv egyenrangú fordítás a kulcsok alatt, nem egyik a másikból” az „angol a prior” mondathoz? Melyik katalógus a forrás?
13. Melyik irányba mutasson a D-30 kockázati mondata („Ha az angol katalógus lemarad …”), ha az angol az elsődleges?
14. Számít-e a prior szempontjából, hogy a nyelvválasztóban a „Magyar” áll elöl (60 · §02, §10), és hogy a drótvázak magyar felületet mutatnak?
15. Válasz-e a tulajdonos mondata a Spec 20 §10 nyitott pontjára, vagy az továbbra is nyitott? Ha érinti, csak a `naplo/`-ra vonatkozik, vagy a `memoria/`-ra, az `adatbázis/` kötetre, a konténernevekre (`beagyazo`, `adatbazis`), a parancsokra (`szolgal`, `karbantart`, `karbantart admin-link`) és a fejlesztői tár neveire is?
16. Melyik olvasat érvényes a D-08 hatályára? A Spec 20 §10 szerint csak a „markdownba írt mezőnevekre” vonatkozik, a D-08 és a D-30 szövege szerint a mappanevekre is.
17. Milyen nyelvűek legyenek a még ki nem mondott nevek: a Postgres-sémák (D-43/9), a táblák (Spec 20 §10), a kategória-definíciók fájlja, a beállítófájl és az üzemeltetési napló fájlja?
18. A 90 kilenc nyelvre szóló számai (§02–§04, §06, §13, §18 CJK-sor) ma csak az FTS5 miatt állnak részben „történeti” megjegyzés alatt. Kapjanak-e a nyelvi ok miatt is ilyen megjegyzést? És mit jelent a §02 (22 zavaró) és a §06 eloszlása (összesen 21) közti eltérés?
19. Hogyan viselkedik a D-20 duplikátum-ellenőrzése, ha ugyanaz a tény angolul és magyarul is bekerül? A 90 §06 tanulsága szerint a modell bármelyiket hozhatja; ezt a dokumentumok nem vizsgálják.
20. Változtat-e az angol prioritás a D-45 (Jev) mérlegelésén, amelynek nyelvi érve („magyarra semmilyen mérés nincs”) csak a magyarra szól?
