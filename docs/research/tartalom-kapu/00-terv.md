# Kutatási terv — tartalom-kapu

**Kampány:** `tartalom-kapu` · **Dátum:** 2026-09-15 · **Keresők:** 2 Sonnet subagent, párhuzamosan

## Miért indult

A régi mappák átnézésekor derült ki egy hiány, amit egyetlen döntés sem fed le: **a rendszer
pontosan szabályozza, KI írhat hova, de semmi nem szabályozza, MI kerülhet be.** Ha egy agent
beír egy API-kulcsot egy bejegyzésbe, azt ma semmi nem akadályozza meg.

Ez azért éles, mert a **D-07/6** fájl-alapú verziózása minden írásnál megőrzi a régi tartalmat is,
és a projekt kimondottan **azért nem gitet használ**, mert „ha egyszer bekerül egy jelszó vagy
kulcs, a gitből csak a teljes történet átírásával tüntethető el". A **bekerülés árát** tehát
végiggondoltuk — a **megelőzést** nem.

A „tartalom-szűrés", „titokszűrés", „tiltólista" szavak a hat élő dokumentumban **nulla**
alkalommal fordulnak elő.

## Al-kérdések

| Egység | Amire ment |
|---|---|
| `sq01` | Hogyan ismerhető fel titok szövegben: mintázat, entrópia, ellenőrzött kulcs; **fals pozitív és fals negatív arány mért adattal**; blokkolás vs. jelzés; mi a teendő, ha már bekerült |
| `sq02` | Van-e bármelyik létező agent-memória rendszerben tartalom-kapu íráskor; memory poisoning mint támadás; ki felel a tartalomért; determinisztikus (LLM nélküli) szűrés a gyakorlatban |

## Kikötések

- A rendszerben **nincs szöveggeneráló modell**, csak beágyazó — tehát csak mintázat- vagy
  szabály-alapú megoldás jöhet szóba. Bármi, ami „a rendszer megítéli", kivitelezhetetlen.
- A **fals pozitív ára** itt nem elméleti: ha a kapu blokkol, egy memória-írás hiúsul meg.
- Hivatalos dokumentációt nyers letöltéssel, gyártói pontossági állítást nem mérésként.
