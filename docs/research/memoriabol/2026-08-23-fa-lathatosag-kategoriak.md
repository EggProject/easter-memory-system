<!-- forrás: projektmemória / easter-kutatas-fa-kategoria.md · másolat: 2026-09-05 -->

# Fa, láthatóság, kategóriák — 2026-08-23

## 1. Fa és láthatóság

**A fő megállapítás:** a vizsgált hét markdown agent-memória közül **egyetlenegy sem** használja a
fájl útvonalát jogosultsági modellként — a láthatóságot mindenhol egy frontmatter-mező (`owner:`,
`visibility/`) vagy egy fán kívüli központi config hordozza, és két rendszer explicit kimondja, hogy
a saját láthatósági jelölőjük **nem** biztonsági határ.
**DE:** egyik sem multi-tenant → ez hiányzó precedens, nem cáfolat. Ahol van valódi többbérlős
izoláció (AWS S3 prefix, HashiCorp Vault namespace), ott **éppen az útvonal-prefix a modell**.

**Ortogonális gyökér — három független megerősítés:** obsidian-wiki (`projects/` mellett
`concepts/`, `entities/`, `skills/`, `references/`, `synthesis/`, `journal/`), basic-memory
(`projects/` mellett `decisions/`, `learning/`, `meetings/`, `archive/`), Claude Code
(`~/.claude/rules/` a repóbeli `.claude/rules/` mellett). Nincs egységes név rá; a leggyakoribb
szó: „global".

**Öröklődés: sehol nem szimmetrikus.** Claude Code: a gyerek automatikusan felfelé sétál, a szülő
csak lusta betöltéssel látja a gyereket. Cursor: csak lefelé. gitignore: mindkét irányban olvas, de
a mélyebb nyer.
**Deny-by-default fában:** a git kanonikus mondata — *„It is not possible to re-include a file if a
parent directory of that file is excluded."* A k8s RBAC tisztán additív, deny nincs. A Claude Code:
*„a deny rule can't carry allowlist exceptions."*

**Testvér-engedély: mindig a fán kívül.** Claude Code `permissions.additionalDirectories`,
open-second-brain `_brain.yaml`, Tailscale egyetlen policy fájl. **Nem találtunk olyan fájl-alapú
rendszert, ami a fában tárolna betartatott kétirányú testvér-engedélyt.**
Mért ok: SharePoint — 50 000 egyedi ACL a kemény korlát, **5 000 fölött romlik a teljesítmény**;
a Microsoft ajánlása: mappát ossz, ne elemet.

**Zanzibar fájlrendszeren:** a `parent` reláció ingyen van (`dirname()`), tehát
`check(user,rel,path) = direct(...) OR check(user,rel,dirname(path))` index nélkül működik.
**Minden nem-fa él (testvér, csoport, ortogonális gyökér) explicit tárolást igényel.**

**Hibaosztályok, amiket el kell kerülni:** CVE-2025-53110 (naiv `startsWith` — `/tmp/allow_dir`
engedélyezte `/tmp/allow_dir_sensitive`-t); CVE-2025-53109 (symlink: a catch-ág a szülőt
validálta); mcpvault (case-insensitive fájlrendszer megkerülte a `.git/**` blocklistet); setuptools
GHSA-h35f-9h28-mq5c (NFC/NFD eltérés miatt a kizárás csendben nem fogott); Claude Code #29471
(`/`, `-`, `_` mind `-`-ra képződik → két projekt memóriája összefolyt).
**Referencia-védelem:** `is_relative_to()` + `.resolve()`, nem `startswith`.

**Magyar ékezet — saját mérés:** az `ő` (U+0151) és az `ű` (U+0171) is dekomponálható, tehát
ugyanúgy érintett, mint az `ü`. A basic-memory `unidecode`-dal transzliterál: `ügyfelek/` és
`ugyfelek/` **ugyanarra a permalinkre esik**. Dokumentált eset: Syncthing NFC→NFD konverzió eltörte
a `Bürgergeld.md` hivatkozásait (1 forrás, blog).

**Átnevezés:** minden rendszer, ami komolyan vette, elválasztotta a stabil azonosítót a jelenlegi
útvonaltól (basic-memory `external_id`), vagy vállalta a vault-szintű link-átírást. **Az útvonal
mint egyedüli identitás átnevezéskor mindenhol tört.**

## 2. Kategóriák (4 Sonnet kutató-kör)

**Nincs közös mag.** ~12 rendszer, egyetlen kategórianév sem fordul elő a többségükben. A
leggyakoribbak: `projects` (4 rendszer), `archive` (3), `journal`/`skills`/`concepts`/`entities`/
`preferences` (2-2).

**Darabszám: 3–15.** Claude Code 4 (`user`, `feedback`, `project`, `reference` — a memóriafájl
frontmatterében `type` mező). obsidian-wiki 6 (`concepts,entities,skills,references,synthesis,
journal`). mem0 15 (életterület-alapú). **Senki nem mond ki ideális számot.**

**A 2026-os agentic rendszerek fele szándékosan NEM ír elő kategóriát:** basic-memory, Anthropic
memory tool, Google OKF, Karpathy-gist, CoMfUcIoS. Az OKF explicit nem-célja: *„Defining a fixed
taxonomy of concept types."*

**Technológia-nevű gyökérkategóriát (`react/`, `postgres/`) EGYIK rendszer sem használ.**

**Mért adatok:**
- **PaperRouter-Agent (arXiv 2607.11564, 2026)** — valós mappahierarchiákon mért LLM-útválasztás.
  Recall@1 szemantikailag egyértelmű mappaneveknél 0,62→0,72; rövidítéses neveknél 0,20→0,52;
  venue/év-alapúaknál 0,09→0,50; folyamat/státusz-alapúaknál 0,12→0,44. **A beszédes mappanév a
  legerősebb egyetlen tényező.** Csak 1 forrás, és a minta 5 felhasználó, kategóriánként 18–52 elem
  — formatív vizsgálat, nem nagymintás benchmark.
- **Whittaker et al., CHI 2011** — 345 felhasználó, 85 000+ visszakeresés. Mappaelérés 58,82 mp ·
  görgetés 25,77 mp · keresés 17,15 mp. **A sikerráta mindkét csoportban 88%** → a mappázás nem
  javította a megtalálást. (A csoportok: sok mappát használók vs. keveset — medián-osztás.)
- **Bergman et al. 2010** — visszakeresési idő = 4,956 + 2,236×mélység + 0,106×méret.
- **Hierarchikus vs lapos besorolás** (Payberah et al.) — lapos F1 0,9815 · hierarchikus 0,9653 /
  0,9564. A lapos pontosabb, a hierarchikus ~harmadára csökkenti a költséget.
- **Kategóriaszám és pontosság** (arXiv 2502.11830) — GPT-4 zero-shot: 3 kategória ~0,54-0,72 ·
  18 kategória ~0,59-0,67 · 60 kategória ~0,62-0,72. **A GPT-4 nem romlik látványosan**, a kis
  nyílt modell igen.
- **Konfliktus-feloldás** (arXiv 2606.01435) — determinisztikus `max(serial)` szabály +10,8 pp az
  LLM-ítélet fölött; 262K kontextusban az LLM 61%-ra esik, a determinisztikus 71-82% marad.
  **Karbantartó futásnál ne az LLM döntsön frissességről.**

**AMIT NEM TALÁLTUNK: nincs egyetlen publikált mérés arról, hogy a kategorizálás javítaná egy
agent-memória visszakeresését.** Négy benchmark (LongMemEval-V2, Mem2ActBench, MemoryAgentBench,
mem0 2026) mind a végső válasz pontosságát méri; egyik sem különíti el a rossz helyre írást a rossz
visszakereséstől.
**Következmény a D-10-re:** a kategória nálunk az ÍRÁSHOZ van, nem a kereséshez.

**Írási útválasztás — négy minta, egyik sem „válassz N kategória közül":**
1. szabad LLM-döntés laza keretben (Anthropic memory tool, Claude Code, mem0, obsidian-wiki)
2. explicit hívói paraméter (basic-memory `write_note(directory=...)`)
3. determinisztikus szabály/számláló, LLM nélkül (open-second-brain dream pass: *„Counters and
   atomic file moves — no LLM inside the algorithm"*)
4. keress előbb, aztán merge vagy új (obsidian-wiki `wiki-ingest`, mem0 ADD/UPDATE/DELETE/NOOP
   top-10 hasonlósági keresés után)

**Staging minta létezik:** obsidian-wiki `_raw/` → `wiki-ingest` promotálja; open-second-brain
`inbox/` → nightly dream pass, 3 ismétlődés után lesz belőle szabály.

**Kötegelt, utólagos besorolás:** a Letta „sleep-time agent" pontosan ez — háttér-LLM, ami utólag
konszolidál. Az open-second-brain ennek az ellenpéldája (tudatosan LLM-mentes). **Mindkettőre van
precedens.**

**A kategória-leírás (prompt) formája:** nincs iparági sablon. Két véglet: egysoros leírás (Cursor
`description`, OKF `description`, filesystem-memory `df`) vagy strukturált mezőlista (hermes-agent
page-típusok). **Egyik vizsgált rendszerben sem kötelező sablonelem a negatív példa** („ez NEM ide
tartozik"); a Claude skill-doksi kifejezetten a pozitív specifikusságot ajánlja, **max. 1024
karakterben**, „mit csinál + mikor használd" párossal.
Prompt-hossz mérés (arXiv 2603.25422): *„a minimal increase in prompt context yields the highest
increase in performance, while further increases only tend to yield marginal"* — és figyelmeztet:
*„Alarmingly, increasing prompt context sometimes decreases accuracy."*

## Amit NEM sikerült megerősíteni

- Nincs számszerű dokumentált eset kategória-elburjánzásra — csak minőségi leírások.
- Nincs olyan dokumentált rendszer, ami laposról VISSZATÉRT volna kategóriákhoz.
- A basic-memory `move_note` viselkedése wikilinkekkel és az indexszel átnevezéskor sehol nincs
  dokumentálva.
- Az open-second-brain `brain_note_lifecycle` eszköznevet a második kutató nem tudta megerősíteni
  — ellentmondás, ne hivatkozz rá bizonyítékként.
- A magyar ékezetes könyvtárnévhez kötött konkrét CVE: nincs.
