# Önellenőrzés — `tartalom-kapu` kampány

## Folyamat

| Amit a szabály előír | Betartva? |
|---|---|
| Webes keresést Sonnet subagent végzi | **igen** |
| Párhuzamos indítás | **igen** — két kereső egy üzenetben |
| `deep-web-research` skill | **igen**, mindkét egységben |
| A szintézis és a döntés Opusé | **igen** — `SZINTEZIS.md` |
| Minden szám a mérési dokumentumba kerül | **még nem** — ez a kampány döntés előtt áll |

## Korlát: degradált mód

Mindkét kereső jelezte, hogy **ő maga nem tudott további alügynököt indítani**, tehát a skill
belső munkamegosztása (külön kereső és külön szintetizáló modell) nem valósult meg. A
párhuzamosság a kampány szintjén megvolt. Az idézetek nyers letöltésből származnak.

## Amit a kutatás megdöntött a kiinduló feltevésemhez képest

1. **„Biztos van rá kész megoldás a memória-rendszerekben."** Nincs. Egyikben sem — és ahol
   van valami, az **modell-alapú, valószínűségi**, nem determinisztikus. Nálunk pont az nem
   használható.
2. **„A titokfelismerés megbízható technológia."** A mért precizitás ellenőrzés nélkül **6%**.
   Ez nem hiba a mérésben — ez a technológia állapota. Csak az élő kulcs-ellenőrzéssel megy
   90%-ra, és ott is marad 10% fals pozitív.
3. **„Az entrópia-küszöb elvi alapon áll."** Nem. A gitleaks készítője maga mondja, hogy
   „trial and error". És a magyar szöveg entrópiája ugyanabba a sávba esik, mint a kulcsoké —
   erre viszont **nincs publikált mérés**, csak a saját, illusztratív számításunk.

## Ami nyitva maradt

- Nincs független (nem gyártói) mérés a blokkoló üzemmód fals pozitív arányáról éles használatban.
- **Nincs semmilyen adat arra, hogyan hat egy blokkoló memória-kapu az agent viselkedésére.**
  Sem a memória-rendszerek, sem az általános DLP-irodalom nem méri.
- A magyar szöveg entrópia-viselkedése dokumentálatlan.
- Az OWASP ASI06 teljes katalógus-szövegét nem sikerült elérni, csak blogbejegyzéseken keresztül.
- A talált incidensek **kutatói bemutatók**, nem elkapott éles támadások — ezt a jelentés
  külön jelöli, és nem szabad elmosni.
