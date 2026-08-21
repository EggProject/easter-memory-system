# Easter — többnyelvű keresési mérőkészlet

Ez a készlet egyetlen kérdésre válaszol: **melyik keresési láb mit talál meg, és melyikre van tényleg szükség.**
Külső függőség nincs — `bun:sqlite` és `fetch`, semmi más.

## Mit mér

| rövidítés | mit csinál |
|---|---|
| `lex` | FTS5 szó-index, **pontos** szóalak (`unicode61 remove_diacritics 2`, tövező nélkül) |
| `lexs` | ugyanaz az index, **vágás nélküli** prefix: a teljes szó + `*` |
| `lexp` | ugyanaz az index, **vágott** prefix-illesztéssel: a szó első 6 karaktere + `*` |
| `tri` | külön FTS5 **trigram** tábla, részszó-kereséssel |
| `dense` | beágyazó modell, koszinusz-hasonlóság |
| `lex+dense`, `lexp+dense`, `lexp+tri+dense` | RRF-fúzió (k = 60) |
| `lexAnd` | ugyanaz az index, de a kérdés **minden szava együtt** kell hogy előforduljon egy dokumentumban |
| `kapuzott` | **embedding-elsődleges**: a szöveges láb csak akkor szólal meg, ha a `lexAnd` talál valamit. Egyébként tiszta `dense`. |

A `lexp` a trükk, ami tövező nélkül kezeli a toldalékolást: **a rag a szó végén van, tehát a szó eleje a tő.**
A vágás hossza a `EASTER_STEM` környezeti változóval állítható (alapértelmezés: 6).

A `lexs` azért van külön mérve, hogy látszódjon, **kell-e egyáltalán a vágás.** A `token*` alak
csak akkor talál, ha a keresett szó a dokumentumbeli szó ELEJE (`szerződés` → `szerződésekben`);
fordítva nem (`kiadásokról` nem találja meg a `kiadásához`-t). Mért különbség a ragozott
kérdéseken: `lex` 0,279 · **`lexs` 0,332** · `lexp` 0,721. Vagyis vágás nélkül a prefix
alig segít — a vágás nem díszítés.

## A korpusz

`corpus/<nyelv>.json`, nyelvenként 12 dokumentum és 12 kérdés, kilenc nyelven:
magyar, angol, német, lengyel, török, kínai, finn, orosz, spanyol. Összesen 108 + 108.

Mind a kilenc nyelv **ugyanazt a 12 témát** fedi le, természetes megfogalmazásban — nem fordításban.
A kérdések keresés közben a **teljes 108 dokumentumos korpuszon** futnak, tehát a többi nyelv zavaró tételként viselkedik.

`corpus/zz-tavolitok.json` — **22 zavaró dokumentum, kérdés nélkül.** Minden azonosítóhoz tartozik
egy hozzá nagyon hasonló, de MÁS azonosító, hasonló jelentésű mondatban: `PROJ-4413` / `PROJ-4421` /
`PROJ-4142`, `RATE_LIMIT_MAX` / `RATE_LIMITS_URL` / `REDIS_LIMIT_URL`, `ECONNRESET` / `ECONNABORTED` /
`ENOTFOUND`, `bun run prerelease` / `bun run release:dry` / `npm run release`, `TanStack Query` az
`TanStack Table` mellé. Az első mérésben minden azonosító egyedi volt, ezért **minden módszer 1,000-et
kapott — az a mérés túl könnyű volt.** Ez a fájl teszi valóságossá.

Három kérdéstípus, nyelvenként 4-4-4:

- **`ragozas`** — a kérdés a dokumentumban szereplő szó **más alakját** használja, azonos tővel.
- **`szinonima`** — a kérdésnek **egyetlen közös tartalmas szava sincs** a dokumentummal, csak a jelentés egyezik.
- **`azonosito`** — `PROJ-4412`, `RATE_LIMIT_URL`, `ECONNREFUSED`, `bun run release`. Ezek minden nyelvben azonosak (senki nem fordít le egy hibakódot), ezért **mind a kilenc nyelv megfelelő dokumentuma helyes találatnak számít** — nem a keresés dolga eldönteni, melyik ügyfél `PROJ-4412`-je kell, hanem a scope-szűrésé.

### A kapu

A `kapuzott` módszer kapuja nem regex és nem kulcsszólista, hanem egyetlen kérdés:
**előfordul-e a kérdés minden szava együtt egy dokumentumban?**

Ha igen, a kérdés pontos találatot vár — azonosítót, parancsnevet, hibakódot —, és ilyenkor
érdemes a szöveges lábra hallgatni. Ha nem, a kérdés átfogalmazás, és a szöveges láb csak zajt hoz.

Ez nyelvfüggetlen, és a mérőkorpuszon **108/108 kérdésnél pontosan a várt módon viselkedik**:
mind a 36 azonosítós kérdésnél nyit, a 72 másiknál nem. Egy korábbi, regex alapú kapu ugyanezen
a halmazon 9 kérdésnél elbukott — a `bun run release` három kisbetűs szó, semmilyen mintázat
nem különbözteti meg egy mondattól.

## Futtatás

Szöveges lábak, modell nélkül — bárhol fut:

```bash
bun bench.ts --no-dense
```

Teljes mérés a saját beágyazó végpontodon:

```bash
bun bench.ts \
  --endpoint http://192.168.50.48:8000/v1 \
  --model qwen3-embedding-8b-4bit-dwq \
  --out eredmeny-dwq.json
```

A query oldalára a szkript automatikusan rárakja a Qwen3 által elvárt instrukciós prefixet
(`Instruct: ...\nQuery:...`) — a dokumentumokra nem. A model card szerint ennek elhagyása
1–5% veszteséget okoz.

## A DWQ-veszteség mérése

Ez az a szám, amit sehol nem publikáltak: mennyit veszít a 4 bites kvantált változat
a nem kvantálthoz képest **magyaron és a többi nyelven**.

```bash
# 1. a kvantált modelleddel
bun bench.ts --model qwen3-embedding-8b-4bit-dwq --out fp4.json

# 2. ugyanaz a nem kvantálttal (vagy bármely másik modellel)
bun bench.ts --model qwen3-embedding-8b --out fp16.json

# 3. összehasonlítás
bun bench.ts --compare fp16.json fp4.json
```

A `--compare` módszerenként kiírja a két nDCG-t és a különbséget.

## További kapcsolók

| kapcsoló | jelentés |
|---|---|
| `--endpoint URL` | OpenAI-kompatibilis `/v1` gyökér (oMLX, LM Studio, Ollama, OpenAI) |
| `--model NÉV` | a modell neve a végponton |
| `--batch N` | hány szöveg megy egy kérésben (alapértelmezés: 16) |
| `--corpus ÚTVONAL` | másik korpuszmappa |
| `--out FÁJL` | az eredmény JSON-be mentése |
| `--no-dense` | csak a szöveges lábak, végpont nélkül |
| `EASTER_STEM=8` | a prefix-vágás hossza |

## Kimenet

Négy metrika, összesítve, nyelvenként és kérdéstípusonként:

- **R@1** — az első találat a helyes-e
- **R@5** — benne van-e az első ötben
- **MRR** — a helyes találat helyezésének reciproka
- **nDCG@10** — helyezés-súlyozott pontszám (egy releváns dokumentum, tehát `1 / log2(rank+2)`)

## Korlátok — ezeket tudni kell az eredmény olvasásához

- **Kínaira a szöveges lábak nem működnek.** A `unicode61` és a trigram is szóhatárra épül,
  a kínaiban viszont nincs szóköz — a mérésben minden kínai nyelvű kérdés elbukik, csak az
  azonosítós kérdések találnak. Ehhez CJK-tokenizáló kellene. Ez **valós korlát**, nem hiba a készletben.
- 12 dokumentum nyelvenként kevés a stabil százalékokhoz. A készlet arra jó, hogy a **módszerek
  közti sorrendet** megmutassa, nem arra, hogy abszolút értéket adjon.
- Egy kérdéshez egy helyes dokumentum tartozik (a `azonosito` típus kivételével). A valóságban
  több is lehet releváns.
