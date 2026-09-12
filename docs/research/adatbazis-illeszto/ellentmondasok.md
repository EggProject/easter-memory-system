# Ellentmondások — ahol a források nem egyeznek

Kampány: `adatbazis-illeszto` · 2026-09-09


---

## SQ-01 — Melyik illesztési minta, és hol a varrat

# SQ-01 — Ellentmondások

## 1. "Kinek a mintája a Repository?" — elterjedt tévhit vs. a forrás saját állítása

**Sokan (a szakirodalomban és a köztudatban) "Fowler mintájaként" hivatkoznak a
Repository-ra.** A martinfowler.com katalógusoldal maga viszont expliciten Edward
Hieatt-et és Rob Mee-t nevezi meg szerzőként ("Edward Hieatt and Rob Mee, 05 March
2003"), míg a katalógus többi, itt vizsgált mintáját (Data Mapper, Gateway, Table Data
Gateway, Row Data Gateway) kifejezetten "Martin Fowler" névvel jegyzi. Ez nem
tartalmi ellentmondás két forrás között, hanem egy **gyakran félreidézett tényállás** —
rögzítjük, mert a kutatási kérdés kifejezetten "Martin Fowler a PoEAA-ban" megfogalmazást
használt, és ezt pontosítani kell: a Repository-fejezetet a könyvben Fowler szerkesztette/
adta ki, de a konkrét mintaleírás szerzősége Hieatt & Mee.

**Bizonyosság: Magas** (közvetlenül, szó szerint ellenőrzött a forrásoldalon).

---

## 2. Repository ORM-mel: hasznos vagy káros? — **Vitatott, valódi szakmai
véleménykülönbség, nem csak félreértés**

Ez a kutatási kör legélesebb, ténylegesen egymásnak ellentmondó véleménypárja.

**Kontra-oldal** (Comartin, Conery, Abraham, Bogard, Sapiens Works — mind gyakorló
mérnökök, nem a minta eredeti szerzői): a Repository ORM fölé építve tipikusan vagy (a)
leaky abstraction lesz, mert az `IQueryable`/`DbSet` kiszivárog, vagy (b) a Repository
csak egy felesleges, vékony burkolat az ORM már amúgy is elvonatkoztatott felülete
körül, ami nem ad valódi absztrakciós értéket, csak extra réteget.

**Pro-oldal / árnyalt oldal** (Jon P Smith, és részben Comartin saját kivétele az
aggregátum-gyökerekre): a Repository *jól megtervezve* — szűk felülettel, domain-
nyelvű metódusnevekkel, csak aggregátum-gyökérre alkalmazva — valódi értéket ad:
olvashatóbb szándékot fejez ki, egy helyre gyűjti az összetett lekérdezéseket, és
kontrollálja a tracked/untracked adat-hozzáférést.

**Fontos, hogy ez nem egyszerűen "két tábor", hanem egy közös nevező is kirajzolódik**:
mindkét oldal egyetért abban, hogy a **generikus, minden entitásra ráhúzott,
lekérdezés-visszaadó Repository (`IRepository<T>` `IQueryable`-lel)** problémás. A vita
lényegében arról szól, hogy (a) egyáltalán érdemes-e Repository-t használni ORM mellett,
vagy helyette use-case-enkénti query object-eket kell írni közvetlenül az ORM/DbContext
ellen — és ebben tényleg nincs egyetértés, mert az egyik oldal (Comartin) elveti a
lekérdezési Repository-t teljesen, a másik oldal (Jon P Smith) megtartja, csak
óvatosabban tervezve.

**Mi magyarázza az eltérést?** A megvizsgált szövegekből az látszik, hogy a vita
résztvevői **eltérő méretű/komplexitású rendszerekről** beszélnek: Comartin
"vertical slice"/CQRS-architektúrát favorizál, ahol amúgy is use case-enként szerveződik
a kód (ott a query object természetes illeszkedés); Jon P Smith egy nagyobb, réteges
("four-layer"), erősen összefüggő geodéziai adatmodellt ("Spatial Modeller") elemez, ahol
az aggregáció maga a fő érték, amit a Repository nyújt. **Ez tehát nem feltétlenül
egymást kizáró álláspont, hanem architektúra-stílustól függő ajánlás** — ezt a
`Vitatott` címke alá soroljuk, mindkét pozíciót és a valószínű magyarázó tényezőt
(architektúra-stílus, rendszerméret) megadva, győztes kikiáltása nélkül.

**Bizonyosság a vita létezésére: Magas** (több, egymástól független, névvel azonosítható
szerző dokumentáltan ellentétes álláspontot képvisel). **Bizonyosság az egyes idézetek
pontos szövegére: Kozepes** (a fentebb `gaps.md` 3. pontjában leírt AI-átfogalmazási
kockázat miatt).

---

## 3. "Hol vágjuk a varratot" — nincs tényleges ellentmondás, inkább kontextus-függés

A 3. kérdésre (aggregátumonként / táblánként / use case-enként) nem találtunk olyan
forráspárt, amely *ugyanarra a helyzetre* adna egymásnak ellentmondó ajánlást. Amit
találtunk, az inkább **különböző hagyományok, különböző alapfeltevésekkel**: a DDD-
hagyomány (Evans, aggregátum) eleve DDD-t feltételez a rendszerben; a DAO/Table Data
Gateway-hagyomány technikai, tábla-központú rendszereket feltételez; a query-object-
hagyomány CQRS/vertical-slice architektúrát feltételez. **Ez nem ellentmondás, hanem
a kontextus-függőség dokumentálása** — nem soroltuk a `Vitatott` kategóriába, mert egyik
forrás sem állítja, hogy a másik kettő téved *az ő kontextusában*.

---

## 4. Nincs ellentmondás a Cockburn-i Ports & Adapters alapelvben

Az összes forrás, amely Cockburnra hivatkozik vagy a hexagonal architecture-t
tárgyalja, konzisztens volt a "belső/külső" aszimmetria, a primary/secondary
megkülönböztetés, és a "cél szerint, nem technológia szerint particionálj" elvvel
kapcsolatban. Ezen a ponton nem találtunk vitatott vagy egymásnak ellentmondó
állítást.


---

## SQ-02 — Párhuzamosság és tranzakciók motorok között

# SQ-02 — Ellentmondások

## 1. "Elrejthető-e az egy-író korlát ingyen?" — nincs valódi forrás-ellentmondás, hanem
egy köztes, feltétel-függő igazság rajzolódik ki

Első pillantásra két, egymásnak ellentmondónak tűnő állítás található a korpuszban:

**A) "El lehet rejteni"-oldal**: a Prisma (3.2 pont) dokumentáltan, transzparensen mindig
`BEGIN IMMEDIATE`-et választ SQLite-on, az alkalmazáskód megváltoztatása nélkül; a
Doctrine SAVEPOINT-tal sikeresen emulálja a beágyazott tranzakciókat minden motoron; az
optimista zárolás (Rails, Prisma) motor-független felület-alak.

**B) "Nem lehet elrejteni ingyen"-oldal**: a Django-csapat évekig tartó vitája (ticket
#29280) végül egy SQLite-specifikus, opt-in konfigurációs kapcsolóban végződött, nem egy
transzparens, mindenkire ráerőltetett viselkedésváltoztatásban; a hivatalos Django-doksi
explicit "válts motort" tanácsot ad; az Ecto dokumentáltan kikapcsol egy konkrét funkciót
(async sandbox tesztelés) SQLite alatt.

**Ez NEM valódi ellentmondás, hanem ugyanannak a jelenségnek két különböző rétege**:
A) azokra az esetekre igaz, ahol a réteg **saját maga, egyszer, tervezési időben** dönthet
a motor-specifikus viselkedésről (pl. "mindig IMMEDIATE-tel induljon a tranzakció" —
ez egy globális, egyszeri döntés, aminek ára van, de nem igényel alkalmazáskód-
változtatást). B) azokra az esetekre igaz, ahol az **alkalmazás konkrét, futásidejű
logikája** (pl. egy adott "upsert" művelet konkrét versenyhelyzet-mintája) ütközik a
motor korlátjával — ott a réteg nem tud "okosan" dönteni helyettünk, mert a döntésnek
(sorosítás vagy sem) alkalmazás-specifikus teljesítmény/helyesség-kompromisszuma van,
amit csak az alkalmazásfejlesztő ismerhet.

**Bizonyosság: Magas** — ez a megkülönböztetés közvetlenül levezethető a Django-vita
szó szerinti szövegéből (Aymeric Augustin válasza kifejezetten ezt a feszültséget írja
le: "the performance hit... seems too high to implement this in Django" — vagyis ELVBEN
meg lehetett volna oldani globálisan, de a döntés ára motoronként eltérő lett volna).

---

## 2. Az izolációs szint "SERIALIZABLE" jelentése SQLite-ban vs a Berenson-kritika
fényében — látszólagos feszültség, ami valójában megerősítés

Az SQLite hivatalos doksija (`isolation.html`) magabiztosan, kertelés nélkül állítja:
"all transactions in SQLite show 'serializable' isolation." Eközben a Berenson et al.
cikk (4. pont) éppen azt bizonyítja, hogy az ANSI SQL izolációs szint-*nevek* (a
SERIALIZABLE-t is beleértve) kétértelműek, és a különböző motorok "standard locking
implementations" ugyanazon névvel eltérő tényleges garanciákat adhatnak.

**Ez nem ellentmondás, hanem éppen a Berenson-cikk tézisének konkrét illusztrációja**:
az SQLite-nál a "SERIALIZABLE" állítás szokatlanul **erős**, mert nem lock-alapú
konfliktus-detektálással éri el (mint sok más motor), hanem **fizikailag kizárja** a
konkurens írást — ez egy triviálisan igaz, "olcsó" SERIALIZABLE, ami más motorokon
(pl. Postgres SSI-je) egy sokkal bonyolultabb, drágább mechanizmussal valósul meg. A két
motor tehát **ugyanazt a nevet** ("SERIALIZABLE") **eltérő mechanizmussal és eltérő
teljesítmény-jellemzőkkel** éri el — pontosan az a jelenség, amire a Berenson-cikk
figyelmeztet egy hordozható felület tervezésénél: **a névazonosság nem garantálja a
mechanizmus- vagy teljesítmény-azonosságot**, csak (idealizált esetben) az eredmény-
garanciák azonosságát.

**Bizonyosság: Magas** a mindkét oldalt alátámasztó, közvetlenül idézett forrásokra
nézve; **Kozepes** a Berenson-idézetek pontos tördelésére nézve (ld. `gaps.md` 2. pont).

---

## 3. Nincs ellentmondás a "mit ígér egy portable réteg az izolációs szintekről" kérdésben

Mind a kilenc vizsgált adatréteg (3. pont) konzisztensen **NEM** állítja, hogy az
izolációs szint egyenértékű lenne minden motoron. Ezen a ponton — szemben az SQ-01 kör
"Repository ORM-mel" vitájával — **nem találtunk éles, valódi szakmai véleménykülönbséget**
a gyártók/karbantartók között; mindegyik forrás ugyanazt a stratégiát követi (dokumentálás
motoronkénti eltéréssel, nem hamis egységesítés), csak a *dokumentáció formája* tér el
(táblázat Prisma-nál, "csak alsó korlát" nyelvezet Doctrine-nál, funkció-tiltás Ecto-nál).

---

## 4. Egyetlen, gyenge jelzésű feszültség: a Kysely és a Knex eltérő explicitsége

A Knex hivatalos doksija nyíltan kimondja: "Not supported by oracle and sqlite" (az
izolációs szint paraméterről). A Kysely hivatalos API-doksija ezzel szemben egyszerűen
felsorolja az öt izolációs szint stringet, **anélkül**, hogy a fetchelt tartalomban
explicit motoronkénti támogatási mátrixot adna (ahogy Prisma vagy Knex teszi). Ez
**önmagában nem ellentmondás** két állítás között, csak **eltérő dokumentációs
alaposság** — de figyelmeztető jel arra, hogy a Kysely SQLite-felhasználóinak esetleg
*futásidőben*, hiba formájában kell szembesülniük egy nem támogatott izolációs szint
kéréssel, nem *dokumentáció-olvasáskor* előre. **Ezt ez a kör nem tudta megerősíteni vagy
cáfolni** (a Kysely SQLite-dialektus forráskódját nem vizsgáltuk) — nyitva hagyva,
`Alacsony` bizonyossággal, `gaps.md`-ben is jelezve related hiányként (4. pont, a #877-es
issue karbantartói válaszának hiánya).


---

## SQ-03 — Szöveges és vektoros keresés hordozható felület mögött

# SQ-03 — Ellentmondások és feszültségek a forrásanyagban

## 1. "Egyetlen abszolút módszer nincs" vs. "mindenki mégis BM25/BM25-szerű alapértelmezést
ad" — nem valódi ellentmondás, de érdemes élesen látni

A PostgreSQL dokumentációja explicit kimondja, hogy saját rangsoroló függvényei
("ts_rank"/"ts_rank_cd") **csak példák**, és a felhasználó szabadon írhat sajátot. Ezzel
szemben a SQLite FTS5, Elasticsearch, Solr/Lucene-család mind BM25-öt (vagy annak
variánsát) adja **beépített, nehezen lecserélhető alapértelmezésként** (SQLite FTS5-ben a
`bm25()` az egyetlen dokumentált beépített rangsoroló-függvény a `rank` oszlophoz, bár
technikailag írható egyéni auxiliary function). Ez nem logikai ellentmondás a forrásokban,
de a motorok **filozófiája** eltér abban, hogy a rangsorolást "cserélhető komponensnek"
(PostgreSQL retorikája) vagy "beépített, motorhoz kötött tulajdonságnak" (SQLite, ES,
Meilisearch, Typesense retorikája) tekintik-e. Ez nem forrprocesskonfliktus, hanem
tervezési filozófia különbsége — a `megallapitasok.md` 1.1 és 2.2 pontjaiban külön
jelölve.

## 2. RRF "nem igényel hangolást" (Elasticsearch, Cormack et al.) vs. a `rank_constant`
paraméter létezése

Az Elasticsearch RRF-dokumentációja azt állítja: "RRF requires no tuning" — ugyanakkor
ugyanaz a dokumentáció definiál egy `rank_constant` paramétert (alapértelmezett 60), amit
technikailag lehet állítani, és amelynek hatását is leírja ("A higher value indicates
that lower ranked documents have more influence"). Ez **enyhe feszültség, nem valódi
ellentmondás**: az eredeti Cormack-cikk is pontosan ugyanezt a mintát mutatja — a `k=60`
konstanst egy pilot-vizsgálatban rögzítették, és utána **nem hangolták tovább**
("fixed during a pilot investigation and not altered during subsequent validation"). Azaz
mindkét forrás konzisztensen azt állítja, hogy **létezik egy hangolható paraméter, de a
módszer szándéka szerint nem kell/nem érdemes ezen módszeresen (adatkészletre) hangolni**
— ez inkább árnyalás, mint ellentmondás, és mindkét fél (az eredeti kutatók és az
Elasticsearch dokumentáció) ugyanazt a mérnöki döntést támasztja alá.

## 3. Searchkick és Haystack/Scout eltérő "hordozhatóság"-fogalma

A négy vizsgált absztrakciós keretrendszer közül a Searchkick (kizárólag ES/OpenSearch)
és a Haystack/Scout/Hibernate Search (több, ténylegesen eltérő motorosztály) **nem
ugyanazt** érti "keresés-absztrakció" alatt — az egyik motorcsalád-belüli kényelmi
réteg, a másik motorosztályok közötti absztrakció. Ez nem a forrásaik közötti
ellentmondás (egyik sem állítja magáról a másik szerepét), hanem a kutatási kérdés
megválaszolásakor **fontos meg nem keverni** a két kategóriát — a `megallapitasok.md`
3.1 és 3.2 pontjai emiatt külön vannak tárgyalva.

## 4. "A pontszám nem összemérhető" állítás forráshelyzete motoronként eltérő erősségű

Nem a források mondanak egymásnak ellent, hanem **a bizonyíték erőssége motoronként
eltér**: Elasticsearch és PostgreSQL esetén T1, explicit, szó szerint idézhető
kijelentés áll rendelkezésre; SQLite FTS5 esetén csak közvetett, formulából levezetett
következtetés. Ha valaki csak a SQLite-dokumentációt olvasná, arra a következtetésre
juthatna, hogy a kérdés "nyitva marad" a hivatalos forrásban — miközben a matematikai
szerkezet (dokumentum- és korpuszfüggő IDF) ugyanazt a következtetést támasztja alá, mint
amit ES/PostgreSQL explicit kimond. Ez nem ellentmondás, hanem **eltérő dokumentálási
alaposság** a motorok között — fontos, mert egy jövőbeli olvasó tévesen azt hihetné, hogy
a SQLite BM25 valamiért kivétel ez alól, holott csak a dokumentáció nem tér ki rá
explicit.

## Amit NEM találtunk ellentmondásnak

A kutatás nem talált egyetlen olyan esetet sem, ahol két T1 forrás **tényszerűen**
egymásnak ellentmondó állítást tett volna ugyanarról a konkrét tényről (pl. hogy egy adott
motor pontos vagy közelítő legyen-e alapértelmezésben, vagy hogy egy adott függvény
milyen irányba rangsorol). A fenti pontok inkább hangsúly-, filozófia- és
dokumentálási-alaposság-beli különbségek, nem forrásütközések.


---

## SQ-04 — Hogyan tartható őszinte egy illesztő

# SQ-04 — Ellentmondások és feszültségek a forrásanyagban

## 1. A "szerződés-teszt" fogalmának hatóköre Fowlernél szűkebb, Rainsbergernél tágabb —
nem valódi ellentmondás, de fontos élesen látni

Fowler saját `ContractTest` bliki-oldala kifejezetten **külső, más csapat által
karbantartott szolgáltatás** és a hozzá tartozó test double viszonyára szabja a
definíciót — a szöveg explicit "external service"-t, "different team"-et, "supplier
team"-et emleget mindvégig.

Rainsberger ezzel szemben a szerződés-tesztet **bármely interfészre** alkalmazza, amit
több osztály implementálhat, kifejezetten beleértve a **saját kódbázison belüli**
Repository-mintát is (nem külső csapat szolgáltatása, hanem ugyanaz a csapat két
implementációja, pl. egy valódi és egy fake Repository).

**Ez nem logikai ellentmondás a két forrás között** — egyik sem állítja a másik
definíciójának tévedését —, hanem **a fogalom szűkebb és tágabb, egymást tartalmazó
olvasata**: Fowler eredeti, szűkebb esete (külső szolgáltatás) a Rainsberger-féle tágabb
definíció (bármely LSP-alapú interfész-szerződés) egy speciális esete. A D-34
kontextusában a **tágabb (Rainsberger-féle) olvasat a releváns**, mert az adatbázis-
illesztő nem külső, más csapat által karbantartott szolgáltatás, hanem saját kódbázison
belüli, két (jelenleg egy) implementációval rendelkező interfész.

## 2. "Subclass to Test" — nevesített minta, amit a szakma egy része antipatternnek
tart, más része (Rainsberger) védelmébe vesz

Ez a kör **nem tudta feltárni a vita tartalmát** (l. `gaps.md`), csak a **vita
létezését**: van egy c2-wiki oldal `SubclassToTestAntiPattern` néven, és van egy
Rainsberger-előadás kifejezetten **"Why I Don't Consider Subclass to Test An
Anti-Pattern"** címmel — a cím önmagában megerősíti, hogy létezik egy **álláspont,
amely szerint az öröklésen alapuló közös tesztkészlet (a `megallapitasok.md` 2.1/A
pontjában leírt "hagyományos" minta) antipattern**, és Rainsberger ez ellen érvel.

Ez összecseng azzal, hogy Rainsberger saját 2021-es visszatekintésében **explicit
áttért** a kompozíció-alapú (2.1/B) variánsra: "One Significant Change... favors
composition over inheritance." Ez **nem bizonyítottan** a "Subclass to Test antipattern"
kritikára adott közvetlen válasz (a cikk nem hivatkozik explicit erre a vitára), de a
két tény (a vita létezése + Rainsberger saját váltása öröklésről kompozícióra) **együtt
olvasva erősen sugallja**, hogy a szakmai konszenzus az öröklés-alapú változat felől a
kompozíció-alapú felé mozdult el 1999–2021 között. **Ez feszültség, amit a szintézisnek
Vitatott (Vitatott) címkével kell kezelnie, nem eldöntött kérdésként.**

## 3. A "gyártói blog vendégei" (Neon) és a "gyakorlói postmortem" (dev.to) közötti
tier-eltérés fontos, de a mögöttes tény nem áll ellentmondásban

A Neon-blog (T4) és a dev.to-poszt (T6) **ugyanarra a mögöttes jelenségre**
(SQLite/PostgreSQL viselkedés-eltérés miatti hamis biztonság) hoznak példákat, és a
konkrét technikai állításaik **nem mondanak ellent egymásnak** — sőt kiegészítik
egymást (a Neon a típuskényszert és a zárolási modellt emeli ki, a dev.to poszt az
idegenkulcs-kényszert, a sorrendezetlen lekérdezést és a migráció-lefedettséget).
**A feszültség nem tartalmi, hanem forrás-minőségi**: a Neon-blog végkövetkeztetése
("használj Neont") explicit termékajánlás, ezért a cikk teljes egészét **nem** szabad
semleges bizonyítékként kezelni — csak a benne található, önmagukban is ellenőrizhető,
jól ismert SQLite/PostgreSQL tulajdonságokra vonatkozó technikai állításokat használtuk
fel (l. `links.md` megjegyzése). A dev.to poszt ezzel szemben nem árul semmit, és
sokkal részletesebb, ellenőrizhető technikai indoklással szolgál — ezért annak ellenére,
hogy formálisan alacsonyabb tier-be esik (T6, egyetlen, nem azonosítható szerző), a
`megallapitasok.md` 5. pontjában **erősebb bizonyítékként** szerepel, mint a Neon-blog.
Ez tudatos, indokolt eltérés a nyers tier-sorrendtől, és itt explicit jelezve van.

## 4. YAGNI mint normatív állítás vs. Rainsberger tesztelhetőségi érve — nem
ellentmondás, hanem két külön kérdésre adott válasz, amit könnyű összekeverni

Fowler YAGNI-esszéje azt állítja, hogy **egy jövőbeli, bizonytalan igényre** épített
absztrakció általában rossz befektetés. Rainsberger azt állítja, hogy egy Repository-
mögötti szerződés-teszt **javítja a mai tesztelhetőséget**. **Ez a két állítás nem áll
ellentmondásban egymással**, mert két különböző kérdésre válaszolnak: Fowler a
*jövőbeli, még nem létező igény* kiszolgálásáról beszél ("piracy pricing" hat hónappal
később), Rainsberger a *jelenlegi* tesztelhetőségi igényről. A `megallapitasok.md` 6.3
pontja ezt explicit szétválasztja, mert a kutatási kérdés (D-34) szövege ("mert később
más adatbázis-típusokat is be akar vezetni") **a Fowler-féle, jövő-orientált érvelést**
idézi meg, miközben a forrásanyag legerősebb, létező, támogatható érve valójában **a
Rainsberger-féle, jelen-orientált tesztelhetőségi érv**. Ez nem a források közötti
ellentmondás, hanem annak kockázata, hogy a D-34 indoklása a gyengébb (empirikusan
alá nem támasztott, jövő-bizonytalan) érvre hivatkozik ahelyett, hogy az erősebb
(jelenlegi tesztelhetőség) érvre hivatkozna — ezt a szintézisnek érdemes explicit
kiemelnie.
