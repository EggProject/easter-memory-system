# Önellenőrzés — `mentes-frissites` kampány

## Folyamat

| Amit a szabály előír | Betartva? |
|---|---|
| Webes keresést Sonnet subagent végzi | **igen** |
| **Párhuzamos indítás** | **igen** — négy kereső egy üzenetben, majd a bővítés után további kettő szintén egyszerre |
| `deep-web-research` skill használata | **igen**, mind a hat egységben |
| A szintézis és a döntés Opusé | **igen** — `SZINTEZIS.md`, D-36, D-37 |
| Minden szám a mérési dokumentumba kerül | **igen** — 90-meresek, 14. szakasz |
| Kérdés minden döntésnél, ajánlással | **igen** — két körben, nyolc kérdés |

## A legfontosabb korlát: a keresők degradált módban futottak

**Mind a hat kereső jelezte, hogy ő maga nem tudott további alügynököt indítani**, tehát a
`deep-web-research` skill belső munkamegosztása (Sonnet-keresők + külön Opus-szintetizáló,
egymástól izolált kontextusban) **nem valósult meg**. Mindegyik egység egyetlen, folytonos
munkamenetben keresett, idézetet ellenőrzött és szintetizált.

**Mit jelent ez, és mit nem:**

- **Nem érinti az idézetek pontosságát.** Minden egység nyers `curl`-lel töltötte le a hivatalos
  oldalakat és forráskódokat, és több egység automatikus idézet-egyezés-ellenőrzést is futtatott
  (az sq05 37 forrásból 75 állítást, az sq06 21 állítást ellenőrzött szó szerinti egyezésre,
  mindkettő 100%-os eredménnyel; mindkettő linkellenőrzést is futtatott, minden forrás élt).
- **Érinti viszont az ellentmondás-keresés mélységét.** Az egységeken belül nem volt független
  második olvasat. Az egységek **között** viszont volt átfedés (az sq03 és az sq06 is nézte a
  migrációt, az sq01 és az sq04 is a mentés-ellenőrzést), és ezek nem mondtak egymásnak ellent —
  ez gyenge, de nem nulla kereszt-ellenőrzés.
- **A párhuzamosság az én szintemen megvolt:** hat egyidejű kereső. A hiány a keresőkön *belül*
  van, nem a kampány szerkezetében.

Ezt a korlátot az egységek maguk írták ki a saját anyagukban is — nem én vettem észre utólag.

## Amit a kutatás megdöntött vagy módosított a kiinduló feltevéseimhez képest

1. **„A mentés a napi karbantartó dolga."** Ezt javasoltam, de a felhasználó a külön, felületről
   állítható ütemezőt választotta. A kutatás valójában őt támasztja alá: a Bacula szó szerint
   négy külön erőforrásra bontja a kérdést (*„What, Where, How, and When"*), a Kopia a „mit +
   mikor" párost külön objektumba teszi a céltól. **Egyik vizsgált rendszer sem köti a mentést
   egy általános karbantartó feladatai közé.**

2. **„A Backup API a hivatalos út."** Első olvasatra ez tűnt a fő mechanizmusnak. A dokumentáció
   viszont rangsor nélkül sorolja a hármat (*„In no particular order"*), és a `VACUUM INTO`
   mellett szól két olyan tulajdonság, amit előre nem láttam: a törölt tartalom kipucolása
   (D-21-illeszkedés) és hogy nem tud „soha be nem fejeződni".

3. **„A két adatbázis konzisztens mentése megoldandó feladat."** Nem az — mert csak egyet
   mentünk. A probléma a D-03 miatt meg sem jelenik. Ezt a kutatás derítette ki, nem a tervezés:
   azért kérdeztem rá, mert azt hittem, meg kell oldani.

4. **„A 3-2-1 szabály szabvány."** Nem az. Egy 2005-ös fényképész-könyvből ered, és a NIST
   vonatkozó szabványa egyszer sem említi. Ha a specifikációban szabványként hivatkoztam volna
   rá, az hiba lett volna.

5. **„A trigram… "** — nem ide tartozik, de ugyanez a mintázat: a kézenfekvőnek tűnő válasz
   ritkán az, amit a valódi rendszerek csinálnak.

## Szerzőség-ellenőrzés

A megbízás külön kérte, mert egy korábbi kampányban derült ki téves attribúció (a Repository
minta **Hieatté és Mee-é**, nem Fowleré). Ebben a körben:

- **YAGNI** — a kifejezés **Kent Becktől és Chet Hendricksontól** ered, Fowler csak dokumentálja.
  Ezt Fowler maga írja le.
- **Speculative generality** — a nevet **Brian Foote** javasolta; a könyv Fowleré és Becké.
- **Rule of three** — **Don Roberts** fogalmazta meg Fowlernek; a gyökere 1988-ig nyúlik vissza.
- **Parallel change / expand–contract** — **Danilo Sato** írta le, 2014-ben, Fowler oldalán.
- **Tolerant Reader** — **valóban Fowleré** (2011). *Itt nem volt téves attribúció.* A valódi
  tévesztési kockázat a szomszédos **Consumer-Driven Contracts**, ami ugyanazon az oldalon van,
  de **Ian Robinson** írta (2006).
- **Ports and Adapters** — **Alistair Cockburn**, 2005.

## Ami nyitva maradt

- **Nincs mért idő** a `VACUUM INTO`-ra és a Backup API-ra méret szerint. Egy talált 2 ms-os
  szám **nem ide tartozik** (fájlrendszer-szintű, blokk-megosztásos másolás) — az sq02 ezt külön
  ki is emelte, nehogy tévesen általánosítsuk.
- **Nincs mért idő** a beágyazások újraszámítására. Csak ár van rá.
- **Nincs a méretünkre szabott ajánlás** sem mentési gyakoriságra, sem visszaállítás-próbára.
- **A visszaállított jogosultságok kérdésére** egyetlen hatósági forrás sem tér ki.
- **Az FTS5 szerkezeti módosíthatósága dokumentációs rés** — a hivatalos oldal nem mondja ki,
  hogy nem lehet, csak nem tárgyalja. A D-37/5 ezért levezetés, nem idézet, és gyakorlati próbával
  kell lezárni.
- Az `sq05` nem tudta a GoF Bridge-fejezetét kinyerni, tehát nincs GoF-szintű Strategy–Bridge
  megkülönböztetés; a *Refactoring* 58. oldala csak két független másodlagos forráson át
  megerősített.

## Forráshűség

Minden egység nyers `curl`-lel dolgozott a hivatalos domaineken (`sqlite.org`, `postgresql.org`,
`orm.drizzle.team`, `docs.liquibase.com`, `documentation.red-gate.com`, `docs.djangoproject.com`,
`litestream.io`, `borgbackup.readthedocs.io`, `restic.readthedocs.io`), forráskódot pedig
`raw.githubusercontent.com`-ról. Ahol WebFetch-et kellett használni (Akamai-blokk, JS-renderelés,
403), azt az egységek jelölik a `linkek.md`-ben és a `hianyok.md`-ben.

Az sq02 egy **forráskód-szintű megállapítást** is tett, amit semelyik dokumentációs oldal nem
mond ki: a SQLite CLI `.backup` parancsa **nem próbálkozik újra** zárolási hiba esetén — a
ciklusa kizárólag `SQLITE_OK`-ra fut tovább. Ez a fajta lelet csak nyers forrásolvasásból jön elő.
