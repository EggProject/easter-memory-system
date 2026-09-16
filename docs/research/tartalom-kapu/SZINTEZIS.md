# Szintézis — tartalom-kapu

**Kampány:** `tartalom-kapu` · 2026-09-15 · 2 kereső, párhuzamosan
**Állapot: döntés előtt.** Ez a kampány feltárt egy hiányt; a döntés a tulajdonosé.

---

## A hiány, amiért a kampány indult

A rendszer szabályozza, **ki** írhat hova. Nem szabályozza, **mi** kerülhet be. Egy agent
beírhat egy API-kulcsot, és azt ma semmi nem állítja meg — sőt, a **D-07/6** verziózása miatt
a kulcs a történetben is megmarad, amíg valaki végleges törlést nem kér.

---

## Az öt megállapítás

### 1. Egyetlen agent-memória rendszerben sincs determinisztikus tartalom-kapu

Hét rendszert néztünk meg célzottan — basic-memory, mem0, Zep/Graphiti, Letta, az Anthropic
memory tool, a Claude Code saját memóriája, OpenAI memória. **Egyikben sincs.**

Ahol egyáltalán van valami, az **modell-alapú, valószínűségi ítélet**. Az Anthropic saját
dokumentációja így fogalmaz: *„Claude usually refuses to write sensitive information"* — az
„usually" itt nem véletlen szóválasztás.

**Nálunk ez az út eleve zárva van:** a rendszerben nincs szöveggeneráló modell.

### 2. A felelősség egyöntetűen a hívóé, sosem a táré

Az Anthropic dokumentációja kimondja: *„these safeguards are your responsibility… add
validation that strips sensitive data before your handler writes the file."*

**Ez ránk kétélű.** Egyfelől precedens arra, hogy a tár ne vállalja. Másfelől nálunk a
„hívó" egy **idegen agent**, akinek a viselkedését nem mi írjuk — tehát ha a felelősséget
kihelyezzük, azt a semmibe helyezzük ki.

### 3. A titokfelismerés pontossága sokkal rosszabb, mint hinnénk

Ez a kampány legfontosabb száma, és lektorált, nagymintás mérésből jön (ESEM 2023, 818 repó,
97 479 címkézett string):

| Üzemmód | Precizitás |
|---|---|
| Mintázat + entrópia, ellenőrzés nélkül | **6%** |
| Élő kulcs-ellenőrzéssel | **90%** |

Vagyis **ellenőrzés nélkül húsz riasztásból tizenkilenc téves.** A tanulmány az okot is
megnevezi: *„generic regular expressions and ineffective entropy calculation"*.

**Az entrópia-küszöbök nem elvi alapon állnak.** A gitleaks készítője maga mondja, hogy
„trial and error" eredménye. Egy ártalmatlan kódsor 4,24 bit/karakter — ugyanabban a sávban,
mint a valódi kulcsok. **Magyar szövegre nincs publikált mérés**, és a saját becslésünk szerint
az átlagos magyar mondat is ebbe a sávba esik.

### 4. Aki blokkol, az szándékosan megkerülhetővé teszi — a fals pozitívok miatt

A GitHub push protection dokumentációja kimondja, miért: *„Bypass functionality for
flexibility: For cases where false positives occur… This provides flexibility without
compromising overall security."*

De **a megkerülés sosem néma**: naplóba kerül, értesítés megy, és három megnevezett okkal
történhet. **Ez a minta közvetlenül átvehető** — és pontosan illeszkedik a projekt „jelzünk,
nem tiltunk" elvéhez, azzal a különbséggel, hogy itt a jelzés nyoma is marad.

### 5. Ha bekerült, a törlés önmagában sosem elég

A GitHub két független dokumentuma és a NIST-alapú ajánlás egybehangzóan: **a kulcsot cserélni
kell**, a törlés csak kiegészítő lépés.

**Ez nálunk fontos**, mert a D-21 végleges törlése tényleges — a fájl és minden verziója
eltűnik. Ez viszont **nem** teszi a kiszivárgott kulcsot érvénytelenné. Ha a rendszer valaha
titkot talál, a felületnek ezt kell mondania, nem azt, hogy „eltávolítva".

---

## Ami ebből következik — de amit nem én döntök el

A kutatás egy **valódi hiányt** igazolt, és azt is megmutatta, hogy **kész megoldás nincs rá**.
A tervezési tér három pontja között kell választani, és mindegyiknek más az ára:

1. **Nem építünk kaput.** A hiány marad, kimondva. Precedens van rá (minden vizsgált rendszer
   ezt csinálja), de nálunk a hívó egy idegen agent.
2. **Jelzünk, nem tiltunk.** Az írás átmegy, de a bejegyzés megjelölődik és naplóesemény lesz
   belőle. A 6%-os precizitás mellett ez **sok téves jelzést** jelent — viszont nem hiúsít meg
   írást, és illeszkedik a rendszer többi elvéhez.
3. **Blokkolunk, megkerülési úttal.** A GitHub mintája. A legerősebb védelem, de egy
   ismeretlen agent nem tud „megkerülési okot" megadni úgy, ahogy egy ember igen — a
   megkerülés nálunk emberi jóváhagyást jelentene, ami az MCP-úton nincs.

**Egy dolog a kutatásból egyértelmű:** bármelyiket választjuk, **élő kulcs-ellenőrzés nélkül a
mintázat-alapú felismerés önmagában használhatatlanul zajos** — élő ellenőrzés viszont azt
jelentené, hogy a rendszer kifelé hálózati hívást indít egy gyanús stringgel, ami maga is
kockázat. Ez a döntés magja.
