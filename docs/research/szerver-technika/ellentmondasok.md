# Ellentmondások és feszültségek

## 1. WAL: gyorsít vagy lassít?

- **Az egyik oldal**: az SQLite WAL-dokumentációja és a széles körben ismételt tanács szerint
  a WAL "általában gyorsabb".
- **A másik oldal**: mért benchmark (megnevezett hardver) szerint 1 írónál 43%-kal, 2 írónál
  17%-kal LASSABB, és csak 4+ egyidejű írótól nyer. Az SQLite saját fórumán egy hozzászóló
  ugyanezt mondja tapasztalatból.
- **Feloldás**: nincs valódi ellentmondás, csak elhallgatott feltétel. A WAL a konkurrenciát
  javítja, nem a nyers írási sebességet. Egy írónál nincs mit javítani rajta.
- **Ránk nézve**: egy írónk van → nem kell WAL. Ez egybevág a hálózati fájlrendszeres
  korláttal is.

## 2. Működik-e az FTS5 a Bunban?

- **Amellett**: két külön GitHub-hibajegy reprodukciós kódja sikeresen futtat
  `CREATE VIRTUAL TABLE ... USING fts5(...)`-t — tehát be van fordítva.
- **Ellene**: nyitott hibajegy szerint macOS arm64-en az FTS5 UPDATE/DELETE korrupciót okoz
  a régi (3.43.2-es) SQLite miatt.
- **Semleges**: a Bun dokumentációja SEHOL nem említi az FTS5-öt.
- **Feloldás**: nem ellentmondás, hanem platformkérdés. macOS-en a Bun az Apple
  rendszer-SQLite-ját használja, Linuxon a sajátját. A "működik" és a "korrumpál" két
  különböző gépen igaz.
- **Ránk nézve**: Linux szerver + induláskori önteszt. A dokumentációs csend nem oldható fel
  további kereséssel, csak méréssel.

## 3. Hova való a jogosultság-ellenőrzés Better Auth mellett?

- **Az első kör állítása**: a `before` hook az objektum-szintű ellenőrzés primitívje.
- **A gap-kör állítása**: a hookok csak a Better Auth saját végpontjain futnak, tehát a mi
  végpontjainkra rá sem futnak.
- **Feloldás**: az első állítást a verifikáció is megjelölte mint a kutató saját
  következtetését, a gap-kör pedig idézettel cáfolta. A gap-kör áll.

## 4. "Nincs beépített sync" — SilverBullet

- **Az eredeti állítás**: a SilverBullet dokumentációja szerint egy space csak egy mappa,
  nincs beépített sync- vagy konfliktuskezelés.
- **Az ellenőrzés**: van beépített sync-motor és CLI `sync` parancs, külön doksioldalon.
- **Feloldás**: a gyengébb állítás igaz — **konfliktuskezelésről** nem ír semmit. A hiány
  bizonyítása rossz oldalon lett elvégezve.

## 5. A megőrzési idő számai

- Több másodlagos forrás magabiztosan mond 12 vagy 18 hónapot ISO 27001 / NIS2 kapcsán.
- Az élő ellenőrzés kimutatta, hogy egyik szabvány szövege sem tartalmaz számot; a számok a
  tanácsadó cégek saját ajánlásai.
- **Feloldás**: ez nem források közti nézeteltérés, hanem körkörös ismétlés. Öt oldal, amely
  ugyanazt a "12 hónap" hüvelykujjszabályt mondja, egy forrás.
