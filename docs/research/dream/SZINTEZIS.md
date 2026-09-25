# Szintézis — mi a „dream", és mi marad belőle LLM nélkül?

Kampány: `dream/` · 2026-09-24 · 4 kutatási egység (SQ01–SQ04) + 3 ellenőrző egység (ELL01–ELL03), 295 forrás, mind az
**Exa** keresővel. Keresés: párhuzamos Sonnet alügynökök. Szintézis: Opus.

A felhasználó kérdése szó szerint: „folytassuk de a dream furcsa, mert ugye nem használunk LLM-et + mintha az
rémlene hogy azt kutattad már le egyszer hogy nem kiszámítható az eredménye".

---

## 1. A korábbi kutatás — jól emlékszel, és most megerősítettük

Két korábbi kampányban volt ilyen találat:

- `router-rangsor/` (2026-09-01): az LLM egyedi ítélete gyenge; ütközés-feloldásnál a legjobb LLM-alapú
  rendszer 54%, egy determinisztikus sorszám-szabály 78–94,8%; többlépéses esetben a legjobb is legfeljebb 7%.
- `tartalom-kapu/` (2026-09-15): ahol a memória-rendszerekben van „kapu", az modell-alapú, valószínűségi,
  nem determinisztikus.

Most két külön kérdést választottunk szét, és mindkettőre ugyanaz a válasz:

**(a) Futásonként más kimenet.** Az Anthropic és az OpenAI hivatalos dokumentációja is kimondja, hogy
temperature 0 mellett sincs garantáltan azonos kimenet; a Claude 4.7-től a temperature nem is állítható.
Az ok a szerver terhelése (batch-invariancia hiánya), nem a prompt. (ELL02/5: igazolva.)

**(b) Rossz döntés, akkor is, ha reprodukálható lenne.**
- Egy 2026-os preprint (arXiv:2605.12978): a GPT-5.4 egy ARC-AGI feladatsoron memória nélkül 100%-ot ért el;
  miután a *helyes* megoldásokból konszolidált memóriát, ugyanezeken 54%-ra esett. A cikk maga szerint minden
  konszolidáció „lossy rewrite". *Két fenntartás: az ICML 2026-os elfogadás nem igazolható, és a cikk
  belül pontatlan (54% hibát vagy 54% pontosságot ír — a törzsszöveg szerint a pontosság esett 54%-ra).*
- A mem0 2026 áprilisában kivette az LLM kezéből a módosítás/törlés döntést („ADD-only"), mert a saját
  hibajegyei szerint az LLM helyes bejegyzést törölt, azonosítót hallucinált. Utána a csak-hozzáadás
  elavult tényeket halmozott fel, ezért külön „Supersede" mechanizmust építettek rá. (ELL02/4.)
- A Claude Code nem dokumentált „AutoDream" funkciója egy hivatalos hibajegy szerint (#47959, 2026-04-14)
  24 óra alatt 23 memóriafájlt törölt jóváhagyás és nyom nélkül. (ELL01/4.)

**Pontosítások a korábbi számokhoz** (ELL02/1–2):
- A „legfeljebb 7%" a MemoryAgentBench v2/v3 változatából van; a v4 (2026-06-28) és az ICLR 2026
  kiadvány ugyanerre „legfeljebb 28%"-ot ír.
- A 78–94,8% vs. 54% igaz, de a szerzők saját v2-je szerint a nyereség nagy része abból jön, hogy
  **szétválasztják** a jelöltek kinyerését és a döntést. Csak a döntő lépést LLM-ről szabályra cserélve
  átlagosan +2,0 pont, 262K-nál 0. Valós időbélyeggel (LongMemEval) nincs szignifikáns különbség
  (26/45 vs 29/45, p=0,45).

## 2. Mit jelent a „dream" ma

A szó agent-memóriára friss: egy 2025-12-i preprint, majd 2026 tavaszán több gyártó szinte egyszerre
(Claude Code 2026-04, Letta 2026-04-21, Anthropic Managed Agents 2026-04-29, open-second-brain 2026-05-15,
mem0 2026-08-04). Mindegyiknél ugyanaz a három művelet:

1. **duplikátumok összevonása**,
2. **elavult vagy ellentmondó bejegyzés cseréje** a frissebbre,
3. **új, összefoglaló bejegyzés írása** (szintézis).

A vizsgált rendszerek egy kivétellel mind **LLM-mel** csinálják: Letta, Anthropic Dreams, mem0 Dream,
Zep/Graphiti, LangMem, cognee, ChatGPT és a claude.ai memóriájának régi változata — a mostaniról nincs forrás
(a Claude Code AutoDream-nél ez csak nem hivatalos forrásból tudható). A kivétel az open-second-brain; a basic-memory-ban nincs ilyen funkció. Az 1. és a 3. pont
szövegírás — nálunk a D-01/2 miatt kizárt.

A biztonságos mintákat a gyártók maguk is keresik: az Anthropic Dreams alapból új tárba ír, a bemenetet nem
módosítja (egy korai hozzáférésű kapcsolóval mégis lehet); a mem0 platform semmit nem töröl, csak állapotot
jelöl; a mem0 saját „dream" skillje minden változást diffként mutat, és jóváhagyást kér; ellentmondást
automatikusan sosem old fel.

## 3. Ami LLM nélkül is létezik

| Rendszer | Mit csinál LLM nélkül | Ír-e magától |
|---|---|---|
| **open-second-brain** (v1.54.0, 2026-08-28) | számlálók és küszöbök: ismétlődő jelzésből szabály lesz, elavultat félretesz; ellentmondást csak **jelez** | igen, de pillanatkép + visszaállítás + próbafutás + idempotencia mellett; opcionálisan jóváhagyásra vár |
| **mimir-mem-core** | közel-duplikátum (koszinusz ≥ 0,92), ellentmondás-jelölés (hasonlóság + tagadás-eltérés), klaszter, lecsengés | csak visszafordíthatóan („none destructive"); az ellentmondást sosem oldja fel |
| **agentos**, **Unforget** | duplikátum, lecsengés, lejárat | igen; a „szintézis/előléptetés" lépéshez náluk is LLM kell |
| **wiki-lint család** (kb-lint, agent-wiki, …) | törött hivatkozás, árva oldal, régi dátum | nem, csak jelent |

A közös minta: **a felismerés determinisztikus és olcsó; az írás vagy csak javaslat, vagy visszafordítható.**
Az open-second-brain öt „fázisa" (close → reconcile → synthesize → heal → log) a fejlesztők saját
utólagos vizsgálata szerint csak naplócímke egyetlen algoritmus fölött; a „synthesize" náluk nem szövegírás,
hanem egy számláló átírása.

Minőségi mérés egyik LLM nélküli „dream"-re sincs — csak kódtesztek.

## 4. Hol a határ, ha csak beágyazónk van

- **Közel-duplikátum-jelölt: megy.** De a küszöb adat- és modellfüggő: egy mérésben a szokásos 0,9 a
  duplikátumok 42–78%-át kihagyta (T3), a Google RETSim-cikkében modellenként 0,82 és 0,96 között van a jó
  küszöb. **Saját korpuszon kell kalibrálni** — a D-20 küszöbe amúgy is mérésre vár.
- **Ellentmondás: nem megy megbízhatóan.** Négy független tanulmány szerint a koszinusz-hasonlóság nem
  választja szét az „X igaz" és az „X hamis" párt (egy példa: 0,993). A modern modellek (BGE, E5) jobbak,
  de korrekció nélkül náluk is fennáll. **A mi modellünkre (Qwen3-Embedding) nincs adat.**
- **Összevonás vagy felülírás?** Minden vizsgált éles rendszer szerint ehhez LLM vagy ember kell; a mem0-ban
  egy tisztán koszinusz-alapú javaslatot a kódellenőrzés azzal utasított el, hogy a hasonlóság rokonságot
  mutat, nem ellentmondást.
- **A beágyazás determinizmusa rendben van**, ha float32-ben, rögzített batch-mérettel számolunk; bfloat16-ban
  a hasonlósági értékek tömegesen egybeesnek.
- **Az emberi jóváhagyás** csak akkor ér valamit, ha kevés van belőle. Memóriára nincs mérés; a kódellenőrzési
  kutatás szerint a tételek számával meredeken esik a figyelem. (Ezt a `router-rangsor/` is jelezte.)

## 5. Ami nálunk már megvan — más néven

| Döntés | Amit csinál |
|---|---|
| D-20 | íráskor duplikátum-ellenőrzés, két lépésben: először nem ír, visszaadja a hasonlókat |
| D-33 | napi összefésülés: a fájlfa és az index eltéréseit keresi és javítja |
| D-17 | projektek között hasonlóságot mér és jelez, ember dönt |
| D-21/7 | a napi karbantartó jelzi a törött hivatkozásokat |
| D-07 | pillanatkép minden gépi tömeges művelet előtt |

Az LLM nélküli „dream" nagy része tehát már a tervben van. Ami hiányzik: **projekten belül, a teljes tárban**
utólag keresett közel-duplikátumok (a D-20 csak az írás pillanatában néz, és a második, szándékos hívás
után bekerülhet a hasonló is).

## 6. A mérlegem

Az LLM-alapú dream nálunk kizárt (D-01/2), és a kutatás szerint az eredménye valóban nem kiszámítható —
se futásonként, se minőségben. Az LLM nélküli változat létezik, és a biztonságos formája: **determinisztikus
felismerés, és vagy csak javaslat, vagy visszafordítható írás.** Nálunk ennek a nagy része már megvan. Új
darab legfeljebb egy éjszakai, projekten belüli közel-duplikátum-lista lehet. **Ellentmondás-felismerést
nem szabad ígérni**, mert beágyazással nem megbízható.

## 7. Amire nincs forrás

- A Qwen3-Embedding viselkedése tagadásra és ellentmondásra.
- Mért jóváhagyási fáradtság memória-karbantartási javaslatokra.
- Bármely LLM nélküli „dream" mért minősége (csak kódtesztek vannak).
- A mi korpuszunkra érvényes duplikátum-küszöb.
- Az arXiv:2605.12978 ICML-elfogadása és a 2606.01435 workshop-elfogadása független forrásból.

## 8. A döntés — 2026-09-24: D-44

**A dream kikerült a projekt céljai közül.** A felhasználó választása: „Kerüljön ki a célok közül"; az én ajánlásom
a halasztás volt (az első verzióban nincs, adat döntsön). Közben, ugyanazon a napon, a felhasználó saját javaslata
volt egy külön, éjszakai agent, amely csak a dream skillt és az MCP-t tölti be; az írásról a döntés „csak javasol"
lett; a külön dream-MCP-t én javasoltam. Mindhárom tárgytalan — a részletek a döntési napló D-44-ében.

**ELL03 (a döntés után):** a mérési dokumentum 5. szakaszában 2026-08-23 óta álló arXiv:2606.01435-számok valósak,
de a „+10,8 pp a determinisztikus szabálytól" félrevezető: a +10,8 pont a teljes átalakítás (jelöltkinyerés + szabály
az egylépéses LLM-válasz helyett) hatása; a szabály egyedül +2,0 pont, 262K-nál 0. A „71–82% 262K-nál" két
különböző metszetet fésült össze: 262K-nál a szám 82%. A mérési dokumentum sorai pontosítva, a D-17 és a D-33 áll.
