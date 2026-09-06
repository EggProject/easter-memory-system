# Korábbi kutatási körök — a projektmemóriából

Ezek a jegyzetek a 2026-08-20 és 2026-09-01 közötti körökből származnak, amikor még nem
készült strukturált kutatási tár. A projektmemóriában élnek; ez itt a másolatuk, hogy a
repóban is meglegyenek.

| Fájl | Mikor | Miről |
|---|---|---|
| `2026-08-20-eszkozok-es-magyar-meresek.md` | 2026-08-20 | Létező eszközök, keresési stack, **magyar beágyazás-mérések**, integrációs felületek, ACL-CVE-k |
| `2026-08-23-fa-lathatosag-kategoriak.md` | 2026-08-23 | A fa alakja, láthatóság, **kategóriák és darabszámuk**, írási útválasztás |
| `2026-09-01-adverzarialis-ellenorzes.md` | 2026-09-01 | **Mely korábbi állítások dőltek meg** — olvasd, mielőtt bármelyik régi számra hivatkoznál |

**A harmadikkal kezdd, ha régi számot akarsz használni.** Az első két kör több állítása
megdőlt vagy pontosításra szorult, és az ellenőrzés kiírja, mi a védhető megfogalmazásuk.

Ami ezekből a legfontosabb, és a mostani kérdésekhez kell:

- **Kategória-darabszám:** valós rendszerekben 3–15, **senki nem mond ki ideális számot**.
  Mérés (arXiv 2502.11830): GPT-4 zero-shot besorolás 3 / 18 / 60 kategóriánál nem romlik
  látványosan — **a kis nyílt modell viszont igen**.
- **Prompt-hossz:** nincs iparági sablon. A Claude skill-doksi max 1024 karaktert ajánl.
  arXiv 2603.25422: a kis kontextus-növelés hozza a legtöbbet, és *„increasing prompt context
  sometimes decreases accuracy"*.
- **Magyar beágyazás:** a korábbi „nincs magyar az MTEB-ben" állítás **téves volt** — 28 MTEB
  task tartalmaz magyart, és a BelebeleRetrieval `hun_Latn` taszkon 191 modellnek van pontszáma.
