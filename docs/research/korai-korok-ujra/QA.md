# Önellenőrzés — `korai-korok-ujra` kampány

## Folyamat

| Amit a szabály előír | Betartva? |
|---|---|
| Webes keresést Sonnet subagent végzi | **igen** |
| Párhuzamos indítás | **igen** — három kereső egy üzenetben |
| `deep-web-research` skill | **igen**, mindhárom egységben |
| A szintézis és a döntés Opusé | **igen** — `SZINTEZIS.md` |
| **`linkek.md` + `allitasok.csv` minden egységnél** | **igen** — 160 forrásolt állítás, ez volt a kampány célja |

## Amit a kampány megdöntött vagy módosított

1. **A Claude Code 10 000 karakteres hook-limitje ma már dokumentált.** A 2026-09-01-i
   ellenőrzés helyesen mondta, hogy akkor nem volt az. Azóta a hivatalos dokumentáció **két
   helyen is** kimondja. **Nem a szám változott, hanem a világ.** A D-15 és a mérési dokumentum
   frissítve. <b>Ez a kampány legfontosabb tanulsága:</b> egy „nincs dokumentálva" megállapítás
   <b>lejár</b>, és ugyanúgy újra kell mérni, mint egy megerősítettet.

2. **A Spec 30 „a tövezés magyarra bizonyítottan ront" megfogalmazása túl erős volt.** A mérés
   azt mondja, hogy az angol tövező **nulla hasznot hoz**, a magyar tövező pedig **elrontja az
   alapalakot**. A kettő nem ugyanaz, mint hogy „ront". Javítva.

3. **A kategóriaszám kérdésére most van lektorált mérés is** — kis, eszközön futó modellekre:
   3 kategóriánál 83–84%, 13-nál 62,8%. Ez **nem mond ellent** a nagy modellen mért eredménynek
   (ott nincs látványos romlás 3 és 60 között); a kettő együtt azt mondja, hogy **a hatás
   modellmérettől függ**. A korlátot kiírtuk: a lektorált mérés kódoló modelleken készült, nem
   olyanokon, amilyen nálunk kategóriát választana.

4. **A „nincs magyar a nagy benchmarkban" tévedés ismét megerősítve megdőlt** — ezúttal nem
   másodkézből: a kereső letöltötte a nyers eredmény-adatbázist, és közvetlen lekérdezéssel
   igazolta a 28 taszkot és a 191 modellt.

5. **A YAML „Norway-probléma" körüli gyakori magyarázat téves.** Egy sokat idézett blog szerint
   a hiba „a YAML 1.2 specifikáció szerint szándékos" — a nyers specifikáció ezt cáfolja. A
   spec 1.2-ben megoldotta; **a két legelterjedtebb parser forráskódja viszont ma is az 1.1-es,
   tág szabályt használja.** A hiba tehát él, csak nem a spec hibája.

## Korlát: degradált mód

Mindhárom kereső jelezte, hogy nem tudott további alügynököt indítani. A párhuzamosság a
kampány szintjén megvolt; az idézetek nyers letöltésből származnak, és az `sq01` minden
forrás-linkjét élőnek is ellenőrizte.

## Ami nyitva maradt

- A 10 000 karakteres limit **dokumentálásának dátuma** nem állapítható meg (a webarchívum nem
  volt elérhető) — tehát nem tudjuk, mikor változott.
- A magyar Snowball-tövező mögötti tudományos mérés (CLEF 2005) **fizetőfal mögött** van; a
  saját mérésünk viszont megvan, és most már pontosabban is van megfogalmazva.
- Az `sq01` nem tudta szám-szám szinten összevetni a korábbi kör eltávolított állítását, mert
  annak szövege nem állt rendelkezésére — csak az irányt tudta megerősíteni.
