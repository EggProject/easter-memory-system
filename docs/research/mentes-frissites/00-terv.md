# Kutatási terv — mentés, helyreállítás és verziófrissítés

**Kampány:** `mentes-frissites` · **Dátum:** 2026-09-12 · **Keresők:** 6 Sonnet subagent, párhuzamosan

## Miért indult

A dokumentum-átolvasás során kiderült, hogy a rendszernek **sehol nincs döntése a mentésről,
a helyreállításról és a verziófrissítésről**. A „mentés" szó a döntési naplóban addig kizárólag
azt jelentette, hogy valaki elment egy szerkesztést. Ez az egyetlen olyan hiány volt, aminek a
következménye adatvesztés lehet.

A kampány két körben indult. Az első négy egység a tartalmi kérdésre ment (mit, hogyan, milyen
gyakran, mivel ellenőrizve). Az ötödik és hatodik egység **a felhasználó kifejezett kérésére**
került be menet közben:

> „ne feleljtsd el hogy »mentés/helyreállítás és a verziófrissítés« -nel is figyelni kell a
> programozasi mintakra hogy ne a rendszerbe legyen minden beegetve"

Vagyis ugyanaz a szabály, ami a D-34-ben az adatbázisra vonatkozik, a mentésre és a frissítésre
is érvényes: cserélhető komponensként kell megtervezni, nem beégetve.

## Kutatási egységek

| Egység | Amire ment |
|---|---|
| `sq01` | Fájl-alapú tartalom mentése változás közben; markdown-rendszerek gyakorlata; 3-2-1 eredete; helyreállítás-próba; gyakoriság; a mentés jogosultsági kockázata |
| `sq02` | Futó SQLite biztonságos mentése: Backup API, `VACUUM INTO`, `.dump`, WAL-kölcsönhatás, Litestream, két adatbázis kereszt-konzisztenciája |
| `sq03` | Drizzle migrációs modell és a rollback kérdése; SQLite `ALTER TABLE` korlátai; FTS5 migrációban; expand–contract; mentés a migráció előtt; fájlformátum-verziózás; Docker-frissítés |
| `sq04` | Mit kell menteni: származtatott adat, beágyazások különleges esete; mentés-ellenőrzés; csendes adatromlás; titkok a mentésben; visszaállítás és a törléshez való jog |
| `sq05` | A mentés mint cserélhető komponens: hogyan absztrahálják a valódi eszközök a tárolási célt; melyik minta illik; mikor NEM éri meg absztrahálni; mit nem tud elrejteni egy interfész; ütemezés; helyreállítás |
| `sq06` | Séma- és formátum-migráció motorfüggetlenül: Liquibase vs. Flyway filozófia; Drizzle dialektusok; Django/Rails séma-absztrakció; képesség-jelzők; fájlformátum-migrációs minták; mikor NEM éri meg |

## Módszertani kikötések

- **A hivatalos dokumentációt nyers HTML-ként kellett lekérni** (`curl`), nem a WebFetch
  összefoglalóján keresztül. A pontos, szó szerinti technikai megfogalmazás számít, és a korábbi
  kampányokban a WebFetch már adott vissza hiányos tartalmat JS-sel töltődő oldalakról.
  GitHub-forrásfájloknál a `raw.githubusercontent.com` a járható út.
- **Minden fontos állítást további két, független linkkel megerősíteni**, ahol lehetséges.
- **Tier-jelölés minden állításnál**: T1 hivatalos/forráskód/lektorált, T2 megbízható másodlagos,
  T3 fórum/blog/anekdota.
- **Amire nincs adat, az hiány, nem becslés.** A „nincs rá forrás" értékes eredmény.
- **A mintanevek szerzőségét ellenőrizni kell** — egy korábbi kampányban már derült ki téves
  attribúció (a Repository minta nem Fowleré, hanem Hieatté és Mee-é).
