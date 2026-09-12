# Kutatási terv — az MCP felület (a 40-mcp.html megírásához)

Dátum: 2026-09-12 · Vezető: Opus (a szintézist ő írja) · Keresők: Sonnet, párhuzamosan

## Miért ez a kör

Ez a rendszer valódi szerződése a külvilággal, és **teljesen hiányzik**. Több élő döntés már
úgy hivatkozik rá, mintha le lenne írva:

- **D-26/8** — a kategóriadefiníció pontosan egy helyen áll az MCP felületen
- **D-26/7** — az indoklás megelőzi a kategóriát a sémában
- **D-30/4** — az MCP felület mindenestül angol
- **D-21/3** — törlést MCP-n át is lehet kérni, kötelező indoklás-paraméterrel
- **D-20/1** — létrehozni CSAK MCP-n át lehet, a felületről nem
- **D-32/6** — a csonka keresési válasz a válasz tartalmában van megjelölve
- **D-33/1** — újraolvasás MCP-n át is kérhető
- **D-31/7** — jelszókezelés MCP-n át nincs

Eszközlista, paraméterek, válaszformátumok és hibakódok viszont sehol.

## A rendszer, amihez a felületet tervezzük

- Markdown fájlok három gyökér alatt (`projects/`, `knowledge/`, `personal/<email>/`).
- Öt szállított kategória, bővíthető; mindegyikhez prompt, ami a hívó agenthez kerül.
- Hibrid keresés: FTS5 + beágyazás, helyezés-alapú egyesítés, kapu.
- **Jogosultság projektenként, emberekhez rendelve** — és amihez nincs jog, az nem létezik.
- Három törlési állapot, kötelező indoklással minden átmenetnél.
- Egy gépen, két konténerben; egy szerverfolyamat.

## Négy al-kérdés

- **SQ-01 — Mit tud és mit nem tud kifejezni egy MCP eszközdefiníció.** A hivatalos
  specifikáció szó szerint: elnevezés, leírás, séma, strukturált kimenet, hibamodell,
  annotációk, lapozás, eszköz vs erőforrás vs prompt.
- **SQ-02 — Milyen eszközfelületet használnak jól a modellek.** Mit mondanak a mérések és a
  hivatalos útmutatók a leírásokról, a paraméterekről, az eszközök darabolásáról, és a
  modellnek szóló hibaüzenetekről.
- **SQ-03 — Mit csinálnak a létező memória-MCP szerverek.** Közvetlen előzmény: milyen
  eszközöket adnak, milyen paraméterekkel, és mit tanultak belőle.
- **SQ-04 — Ki hívja? Azonosítás és jogosultság MCP-ben.** A mi egész jogosultsági modellünk
  azon áll, hogy tudjuk, ki kérdez. Az MCP hitelesítési története viszont változott.

## Hatókörön kívül

- A keresés algoritmusa (D-02, D-32) és a tárolás (D-34) — csak a felület alakja érdekel.
- A felhasználói felület (60-felulet.html).
