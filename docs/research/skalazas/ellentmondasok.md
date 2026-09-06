# Ellentmondások

## 1. Thompson elve: folyamaton belül vagy azon túl is?

- **Az egyik kereső rögzítése**: a Single Writer Principle szálakra/végrehajtási kontextusokra
  vonatkozik, a nyereség folyamathatáron nem érhető el, mert memóriabarrierre épül.
- **Két verifikáló, élő ellenőrzéssel**: Thompson szövege explicit kiterjeszti — *„The same patterns
  apply if the processing node is a server and the communication system is a local network."*
- **Feloldás**: a szűkebb állítás **az LMAX Disruptor konkrét, lock-free, megosztott memóriás
  technikájára** igaz, nem magára az elvre. A kereső a kettőt összemosta.
- **Ránk nézve**: a szétvágásnak van elvi támogatása. A szűkebb olvasat ellene szólt volna.

## 2. WAL: az olvasók tényleg nem blokkolnak?

- **A dokumentáció fő állítása**: *„readers do not block writers and a writer does not block
  readers."*
- **Ugyanaz a dokumentáció, néhány bekezdéssel odébb**: *„This is mostly true. But there are some
  obscure cases…"*, és három dokumentált eset, amikor WAL módban mégis `SQLITE_BUSY` jön.
- **Feloldás**: nem ellentmondás, hanem elhallgatott feltétel. Tervezési alapelvnek jó, feltétel
  nélküli garanciának nem — 100 felhasználós konkurencia-tervnél `busy_timeout` és
  újrapróbálkozás kell mellé.

## 3. Azonnal látszódjon-e az írás?

- **Elasticsearch és Solr**: nem, és kifejezetten lebeszélnek róla — a per-írás frissítés ára
  háromszor jelentkezik (index-, keresés- és merge-időben).
- **A mi tervünk**: igen, azonnal.
- **Feloldás**: a figyelmeztetés **nagy írási forgalomra** szól. Nálunk az írás ritka, és az FTS5
  per-írás költsége egy kis b-fa, nem egy szegmens. A két helyzet nem ugyanaz — de a
  `crisismerge` blokkoló összeolvasztása marad valós kockázat, azt a karbantartónak kell kezelnie.

## 4. Szét kell-e vágni egy kis alkalmazást?

- **Fowler (MonolithFirst)**: ne — nem tudod még, megéri-e, és a jó határokat korán nem találod el.
- **Thompson és a valós SQLite-rendszerek (rqlite, dqlite, Litestream)**: az egy-írós szétválasztás
  bevett és működő minta.
- **Feloldás**: a kettő nem mond ellent. Thompson azt mondja, **hogyan** válaszd szét, ha
  szétválasztod; Fowler azt, **mikor**. A mért IPC-ár (a munka ezredrésze) Thompsonnak ad igazat
  teljesítményben, a hibamódok (idempotencia, amit még a dqlite sem fejezett be) Fowlernek
  időzítésben.
- **Megjegyzés a teljességért**: Fowler állításának is van dokumentált ellenérve — a verifikáló
  talált élő vitát róla. Nem egyhangú álláspont.

## 5. „A natív driver konténerben törik"

- **A projekt korábbi feljegyzése**: több független hibajegy, konténerben különösen.
- **Ez a kör**: a konténeres hibajegyet duplikátumként lezárták; a valódi ok CLI-félreértés
  (`bun bun` → `bun build`) a slim/distroless képek belépési pontja miatt, és **bármelyik**
  beépített importot elrontja, nem csak az SQLite-ot.
- **Feloldás**: a saját feljegyzésünk volt túl erős. Pontosítani kell.
