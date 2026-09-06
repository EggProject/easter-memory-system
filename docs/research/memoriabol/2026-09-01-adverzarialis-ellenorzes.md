<!-- forrás: projektmemória / easter-kutatas-ellenorzes.md · másolat: 2026-09-05 -->

# Adverzariális ellenőrzés — 2026-09-01

**Olvasd, MIELŐTT bármelyik korábbi kutatási számra hivatkoznál.**

## MEGDŐLT VAGY TÚL ERŐS ÁLLÍTÁSOK

**1. „Egyíró szerver-elrendezésnél az SQLite egyidejűségi problémái eltűnnek." — HAMIS, túlzó.**
Az SQLite `wal.html` maga mondja: *„this is mostly true"*. Marad `SQLITE_BUSY` és **checkpoint
starvation**: ha mindig van aktív olvasó, a WAL-fájl korlátlanul nő. Védhető: „a klasszikus
író-író verseny megszűnik, de a WAL mód önmagában nem konfliktusmentes."

**2. „A szerverre költözés megszünteti a korrupciós kockázatot." — TÚL ERŐS.**
A `howtocorrupt.html` **8 fő kategóriában ~29 okot** nevez meg; ebből a hálózati fájlrendszer csak
**1-2**. A többi (fd-hibák, backup közbeni írás, sync letiltása, flash-hardver, memóriakorrupció,
`fork()` utáni nyitott kapcsolat) helyi lemezen, egyíró elrendezésben is fennáll.

**3. „A Claude Code `additionalContext` limitje 10 000 karakter." — NEM DOKUMENTÁLT.**
Négy hivatalos oldal átkeresve: **nincs benne semmilyen karakter- vagy tokenlimit**. A szám csak
GitHub issue-kban bukkan fel, felhasználói állításként. A tényleges viselkedés (#70460, nyitott):
~10 KB fölött a modell **2 KB előnézetet** kap. **Ez a szám NEM kerülhet a specifikációba.**

**4. „Minden mai kliens mohón kapcsolódik minden MCP-szerverhez." — CÁFOLT.**
A Claude Code **v2.1.221-től** discovery cache-t használ. Cursor/Gemini/Antigravity: **nem
dokumentált**, nem állítható egyik irányban sem.

**5. „16 órás beragadás egy MCP-szerver miatt." — PONTOSÍTANDÓ.**
`stale` címkével zárt issue, valószínűleg botzárás. **Azóta orvosolva:** `MCP_TOOL_TIMEOUT_MS`
(alap 600000 ms) és `MCP_TOOL_IDLE_TIMEOUT_MS` hivatalosan dokumentált.

**6. „Egyetlen vizsgált rendszerben sem lát a mélyebb szint fölfelé." — HAMIS univerzálisként.**
A **tagsági** öröklés valóban csak lefelé megy. DE a GitLabban ma is nyitott hibák szerint
alcsoport-tagok **látják a szülő csoport** Labeleit, Iterations-ét, Epicseit, CI-változóit
(gitlab#358615, #358611, gitlab-foss#42518). A fölfelé szivárgás létezik — **hibaként, nem
tervezett funkcióként.**

## PONTOSÍTÁSOK (az állítás áll, de a feltétel hiányzott)

**7. WAL hálózati fájlrendszeren.** A kivétel: **`PRAGMA locking_mode=EXCLUSIVE` az első
hozzáférés ELŐTT + garantáltan egyetlen kapcsolat**. NEM a `SQLITE_OPEN_NOMUTEX` és NEM a `nolock`
URI-paraméter.

**8. Vec2Text 92% — a feltételek nélkül túl erős.** GTR-base embeddingen, Wikipedia-adaton,
**50 korrekciós lépéssel + sequence-level beam search-csel**. Egy lépéssel **0% exact match**. És
**iteratív black-box hozzáférés kell magához az embedder-modellhez**.

**9. PaperRouter-Agent.** A cikk létezik, a számok pontosak. De a harmadik kategória **„venue/year"**,
nem „dátum/hely". A minta **5 felhasználó** — formatív vizsgálat.

**10. Whittaker CHI 2011.** Minden szám stimmel. De a csoportok **„sok mappát használók vs.
keveset használók"**, nem „rendszerezők vs. keresők". A konklúzió árnyaltabb: a mappázás
visszakeresésre nem ér semmit, **de feladatkezelési célt jól szolgál**.

**11. Windows rename — „egyáltalán nem megbízható" túl erős.** A `MoveFileEx` doksi **nem
garantálja** az atomicitást. NFS: a `rename(2)` BUGS szakasza nem az atomicitást vonja kétségbe,
hanem hogy **crash esetén a hibajelzés megbízhatatlan**.

**12. „Adatbázis nem tartható szinkronizált mappában" — nincs szolgáltatói forrás.** A
figyelmeztetés az **SQLite** és a **Zotero** dokumentációjából jön. A Zotero-forrás ERŐSEBB, mint
hittük: hivatalos KB-cikk, nem fórumbejegyzés.

**13. MTEB Belebele `hun_Latn`.** 0,97994 és a 3. hely **pontos**, nyers parquet-ből ellenőrizve.
De ma **191 modell** van a taszkon, nem 189 — élő, bővülő leaderboard.

**14. `additionalContextLimit` Codexben — LÉTEZIK.** Alapérték **2500 token**. A 2026-08-20-i
kutatásnak igaza volt, a 09-01-inek nem.

**15. Antigravity `injectSteps[]` — PreInvocation ÉS PostInvocation.** A 12 000 karakteres
rules-limit igazolt. Timeout alapból 30 mp.

**16. Cursor `sessionStart`** — `additional_context` snake_case igazolt; cloud agentben nem fut;
a background agent kizárása **NEM igazolható**.

## NEM DOKUMENTÁLT, DE NEM IS CÁFOLT

**17. FTS5 a `bun:sqlite`-ban.** A Bun doksi **sehol nem említi**. A saját mérés (Bun 1.3.13,
Linux x64, SQLite 3.51.2) áll, de ez viselkedés-megfigyelés, nem garancia, és **platformfüggő**.
**A specifikációban „lemért", nem „dokumentált" jelzővel szerepelhet.**
