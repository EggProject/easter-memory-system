# Kutatási terv — a kategória-választó prompt mérete

Dátum: 2026-09-05 · Vezető: Opus (a szintézist ő írja) · Keresők: Sonnet

## A kérdés, ahogy a tulajdonos feltette

A kategóriák promptjait **nem mi dolgozzuk fel** — azokat a memóriát író külső agent (Claude,
Codex, bármelyik) kapja meg, hogy el tudja dönteni, melyik kategóriába sorolja a bejegyzést.
Ezért nem lehet túl hosszú. Kell egy **token-alapú ajánlott felső határ**, és ha a felhasználó
átlépi, **nem tiltunk, csak erősen jelzünk**. A kategória-darabszám ajánlásánál pedig a prompt
méretét is figyelembe kell venni.

## A vezető felismerése, amit a kutatásnak igazolnia vagy cáfolnia kell

A modell **nem egy kategória promptját kapja, hanem az összesét egyszerre**, mert azok közül
választ. Tehát a korlátnak nem a darabszámra és nem a prompt hosszára külön kell vonatkoznia,
hanem **a kettő szorzatára** — arra az egy utasítás-blokkra, ami ténylegesen az agenthez kerül.

## Amit már tudunk (2026-08-23-i kör, NE kutassátok újra)

- Valós rendszerekben 3–15 kategória; senki nem mond ki ideális számot.
- arXiv 2502.11830: GPT-4 zero-shot besorolás 3 / 18 / 60 kategóriánál ~0,54-0,72 / 0,59-0,67 /
  0,62-0,72 — erős modell nem romlik látványosan, kis nyílt modell igen.
- Claude skill-doksi: max 1024 karakteres leírás, „mit csinál + mikor használd".
- arXiv 2603.25422: a kis kontextus-növelés hozza a legtöbbet, a további alig; és
  „increasing prompt context sometimes decreases accuracy".
- Nincs dokumentált eset kategória-elburjánzásra.

## Öt al-kérdés

- **SQ-01** Mennyibe kerül tokenben egy eszköz/kategória-leírás, és hol a gyakorlati plafon.
- **SQ-02** Hogyan romlik a választás pontossága, ahogy nő a választható elemek SZÁMA.
- **SQ-03** Hogyan romlik, ahogy nő az egy elemre jutó LEÍRÁS hossza.
- **SQ-04** Mit írnak elő a valós rendszerek saját maguknak (karakter/token limitek).
- **SQ-05** Hogyan jelezzük a felhasználónak — mérés a figyelmeztetés küszöbéről.

## Hatókörön kívül

- Modellválasztás, beágyazó modellek, keresési minőség.
- A prompt SZÖVEGE (mit írjunk bele) — ez a méretéről szól.
- Fine-tuning, RAG-architektúra.
