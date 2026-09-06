# Hiányok — mit nem tudunk, és melyik fajta hiány

## Bizonyított hiány (evidence of absence) — ne keressük tovább

1. **A Bun dokumentációja nem mondja ki, hogy az FTS5 be van fordítva.** Átnézve: a renderelt
   `bun.com/docs/runtime/sqlite` és a nyers `docs/runtime/sqlite.mdx` forrás, célzott
   kereséssel. Nulla találat. → Zárás módja: induláskori önteszt, nem további keresés.
2. **Egyetlen vizsgált markdown-alapú rendszer sem használ tartalom-lenyomatos írási
   előfeltételt.** Hét rendszer dokumentációja átnézve. → Ez a D-07 melletti érv, nem hiány.
3. **A Better Auth sehol nem mondja ki, hogy az authorizáció nem az ő felelőssége.** Kerestük
   a hooks, plugins, security és FAQ oldalakon. A csend maga a válasz: a dokumentált minta
   (`auth.api.getSession` a saját route-ban) elárulja a határt anélkül, hogy kimondaná.
4. **Nincs dedikált "Protecting Resources" doksioldal Better Authtól.** A mintát a
   framework-integrációs guide-okból kell összerakni.

## Hiányzó bizonyíték (absence of evidence) — lehetne még keresni

| Hiány | Mennyire fontos | Milyen kérdés zárná |
|---|---|---|
| Tartalmazza-e a stabil Bun 1.4 a 2026-08-06-i FTS5-segfault javítást | közepes | Bun 1.4 changelog / a PR merge-célja és a release dátuma |
| macOS Intelen reprodukálható-e az FTS5-korrupció | alacsony | nem érdemes — Linuxra megyünk |
| Mért többletköltség hash-láncolt auditnaplóra | alacsony | akadémiai irodalom (Schneier–Kelsey), vagy saját mérés |
| Bájt/sor becslés valós audit-sémára indexekkel | közepes | nem keresés kérdése: számoljuk ki magunk a rekordformátumból |
| Kemény OFFSET vs keyset benchmark SQLite-on | alacsony | a mechanizmus dokumentált, a szám nem kell a döntéshez |
| TiddlyWiki MultiWikiServer ETag / If-Match írási előfeltétel | **közepes-magas** | ha létezik, ez az EGYETLEN precedens a D-07-re — `mws.tiddlywiki.com` API-doksi |
| Dendron, Zettlr, Foam konkurenciakezelése | alacsony | egy kör; valószínűleg ugyanaz a kép, mint a többinél |
| Kulcsos mutex-map memórianövekedése nagy könyvtárakban | alacsony | a minta dokumentált egy kis csomagban; a nagyok nem adnak kulcsos wrappert |

## Vault-hibák, amiket egy jövőbeli ügynöknek tudnia kell

1. **Két rögzítés AI-összefoglaló, nem oldalmentés** volt (GitHub issue-k). A hibás mintát
   fel lehet ismerni: `## Issue Summary`, `## Critical Impact`, harmadik személyű elbeszélés.
   A Bun-osat újrarögzítettük (`G-01` könyvtár), a Better Auth-osat elejtettük.
2. **Az `sqlite.org/limits.html` pillanatképe csonka** — hiányzik belőle az ATTACH-korlátokról
   szóló szakasz. Az élő oldalon megvan.
3. **Slug-ütközés az SQ-03 könyvtárban**: két hasonló című Logseq-forrás azonos fájlnevet
   kapott, az egyik felülírta a másikat. A manifest egyik sora félrevezető URL/tartalom párt
   mutat.
4. **Rendszeres tier-felminősítés**: a hivatalos domainen lévő fórumbejegyzések és a
   megerősítetlen GitHub-hibajegyek T1-et kaptak. A `04-citations/verdicts.jsonl` tartalmazza
   a javított értékeket `tier_confirmed` mezőben — azt kell nézni, nem a manifestet.
