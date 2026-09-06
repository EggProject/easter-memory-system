<!-- forrás: projektmemória / easter-kutatas.md · másolat: 2026-09-05 -->

# Eszközök, keresési stack, magyar mérések — 2026-08-20

## ⚠️ JAVÍTÁS — a beágyazó modellek magyar képessége

**Az első kutatási kör ezt elrontotta.** A téves állítások: „nincs magyar az MTEB-ben", „nincs
magyar MTEB pontszám", „az embedding modellek gyengén kezelik a magyart". **Mind téves.**

A valóság: **28 MTEB task tartalmaz magyart**, és a magyar retrieval-feladatra **189 modellnek**
(2026-09-01-i ellenőrzés szerint már 191) van publikált pontszáma.

**BelebeleRetrieval `hun_Latn`, nDCG@10:**

| Modell | nDCG@10 |
|---|---|
| **Qwen/Qwen3-Embedding-8B** | **0,9799** — a 189-ből #3 |
| gemini-embedding-001 | 0,9588 |
| intfloat/multilingual-e5-large | 0,9504 |
| Qwen3-Embedding-4B | 0,9441 |
| BAAI/bge-m3 | 0,9436 |
| openai/text-embedding-3-large | 0,9232 |
| Qwen3-Embedding-0.6B | 0,8714 |
| openai/text-embedding-3-small | 0,8280 |
| mteb baseline BM25 | 0,6705 |

**A BM25-sorhoz kötelező fenntartás:** a baseline hardkódolt `stemmer_language="english"`-gel
futott magyar szövegen → **alulbecslés**.

**Antal Margit 2025** (Infocommunications Journal 17(4)) — 8 modell + BM25 baseline, MRR:
BGE-M3 0,90/0,98 · XLM-R 0,90/0,94 · gemini 0,87/0,99 · OpenAI-3-small 0,80/0,94 ·
**huBERT (magyar-specifikus) 0,78/0,82** · **BM25 0,77/0,82**.
Két tanulság: (1) a magyar-specifikus modell **alulmarad** a nagy multilingválisokkal szemben —
ne keressünk magyar modellt; (2) szűk, domén-specifikus korpuszon a BM25 meglepően közel van.

**MIRACL-ban NINCS magyar** → az OpenAI 54,9%-os MIRACL-száma **semmit nem mond a magyarról**.

**A „magyar embeddingek kiábrándítóak" blogposzt módszertanilag hibás:** HuRTE **entailment**-
párokon mért koszinusz-hasonlóságot — ez nem retrieval.

### Qwen3-Embedding-8B — implementációs tudnivalók

- **Instrukciós prefix KÖTELEZŐ a query oldalon.** A model card: *„not using an instruct on the
  query side can lead to a drop in retrieval performance by approximately 1% to 5%"*. **A
  dokumentumra NEM kell.**
- **4096 dimenzió** → 50 000 float32 = **819 MB**, ~5× lassabb brute force, mint 768d. Megoldás:
  MRL-csonkolás vagy bináris kvantálás. **Mérni kell.**
- **A 4bit-DWQ változat minősége magyarra SEHOL nincs mérve.**
- **LM Studio nem ismeri fel a Qwen3 MLX-változatot embeddingként** (nyitott hibajegy). GGUF-ban
  megy. **oMLX ad `/v1/embeddings`-et.**
- Apache 2.0, 32K kontextus, MRL támogatás.

## A legfontosabb eszköz-találat: itechmeat/open-second-brain

MIT, **Bun + TypeScript**, 314★, aktív. Majdnem pontosan a mi tervünk, megírva:
- markdown = igazságforrás; `brain.sqlite` = eldobható index
- SQLite **FTS5 + opcionális trigram shadow-tábla + opcionális sqlite-vec**; default tokenizer
  `unicode61 remove_diacritics 2`
- determinisztikus **dream** (`close → reconcile → synthesize → heal → log`), **LLM nélkül**,
  snapshot + rollback + `--dry-run` + idempotencia
- **fail-closed owner-scope**: „An unreadable ownership claim is still a claim"
- Claude Code 8 hook-esemény, ~82 MCP tool, 13 telepítési célpont

**Amije NINCS:** hierarchia, ACL, magyar. A szerző kimondja: „It is NOT a security boundary."
Döntés: **nem forkoljuk**, de a mintáit átvesszük.

**eugeniughelbur/obsidian-second-brain** — 4122★, Python. **Az egyetlen projekt dokumentált
Antigravity-úttal.** Mért: nem angol lekérdezéseknél recall@5 **13% → 63%** multilingual modellel.

## Keresés — saját mérés (Bun 1.3.13, Linux x64)

- `bun:sqlite` **tartalmazza az FTS5-öt** (SQLite 3.51.2). A Bun doksi ezt SEHOL nem említi —
  csak empirikus, macOS ARM-on nem tesztelve.
- **macOS-en a `bun:sqlite` az Apple rendszer-SQLite-ját használja** → **sqlite-vec nem tölthető
  be** `setCustomSQLite()` nélkül.
- **JS brute-force elég:** 50 000 × 768 = 97 ms / 147 MB. Bináris kvantálással 500 000 × 768 =
  108 ms / 46 MB. **Vector DB felesleges.**
- `bun:sqlite` BLOB-hoz **`Uint8Array` kell, nem `ArrayBuffer`**.
- **A Porter tövező magyarra pontosan nulla hasznot hoz.** A Snowball magyar tövező elrontja az
  alapalakot (`kutya→kuty`, `Budapest→Budapes`). **A `trigram` tokenizer nyelvfüggetlenül
  megoldja a ragozást.** `remove_diacritics 2` az `ő`/`ű`-t is kezeli.

## Integráció (hivatalos doksikból)

| Eszköz | Session-indulási injektálás | Limit |
|---|---|---|
| Claude Code | `SessionStart` → `additionalContext` | **nem dokumentált** (a 10 000 karakter téves volt) |
| Codex | `SessionStart` | **2500 token** (`additionalContextLimit`) |
| Gemini CLI | `SessionStart` | nem dokumentált |
| Cursor | `sessionStart` → `additional_context` (**snake_case!**) | nem dokumentált |
| **Antigravity** | **NINCS SessionStart** — `PreInvocation` + `injectSteps[]` | rules: 12 000 char |

**Két kemény korlát:** (1) az **MCP nem tud szerver→kliens kontextust betolni** — session-indulási
injektálás CSAK hookkal; (2) a **Codex hivatalos MCP feature-listáján a `resources` és `prompts`
nem szerepel** → a memória-API-t **tool**-ként kell kitenni.

## ACL — valódi CVE-k

- **CVE-2026-31245 / -31241 / -31240 (mem0)** — nincs authz a memória-API-n.
- **CVE-2025-53110** (MCP filesystem) — naiv prefix-illesztés. **Soha ne `startsWith()`.**
- **CVE-2026-25536** (MCP SDK) — cross-client szivárgás megosztott transport miatt.
- **OWASP Top 10 for Agentic Applications 2026** — ASI06 Memory & Context Poisoning.

**Kategorizálás prompt alapján:** Zep és mem0 is a LEÍRÁS alapján osztályoz, nem a név alapján.
Zep figyelmeztetése: *„Overlapping or ambiguous descriptions lead to inconsistent classification"*.
A Cursor és a Claude Code **kettéválasztja** a determinisztikus (glob/útvonal) és a
modell-döntéses (description) csatornát.

## Amit NEM sikerült megerősíteni

- A 4bit-DWQ minőségvesztése magyar retrievalen — sehol nincs mérve.
- Nincs korrektül stemmelt magyar BM25 vs. embedding összevetés.
- Nincs publikált mérés a mem0/Zep kategória-besorolás pontosságáról.
- Melyik Bun verziótól van FTS5 — a Bun doksi nem említi.
