# Átadás — easter-memory-system · 2026-09-26

Ez a fájl arra való, hogy egy új munkamenet pontosan innen folytassa a munkát. Az előző munkamenetben ismétlődő API-hibák
voltak; semmi nem veszett el: minden dokumentum, kutatás és döntés a Mac-en van, md5-tel ellenőrizve.

---

## 1. Hogyan indítsd az új munkamenetet

1. **Ugyanabban a claude.ai Projectben** indítsd („easter-memory-system"). Ez számít: a projekt-memória
   (`/projects/01a0a5bc-1b9e-754b-9704-ff468e85ac54/…`) csak a projekten belül írható, a projekten kívülről nem is olvasható;
   a Project-utasítások (a célok listája) is csak ott töltődnek be.
2. **A Mac-mappát kösd hozzá**: `/Users/eggp/projects/eggproject/easter/easter-memory-system` (az asztali appban új feladat a
   géppel kiválasztva, vagy „Link to this computer"). Enélkül az új munkamenet nem látja a dokumentumokat.
3. **Első üzenetnek** ezt másold be:

   > Folytassuk az easter-memory-system munkát pontosan ott, ahol az előző munkamenet abbahagyta. Előbb olvasd el:
   > (1) a projekt-memóriából az `easter-spec-allapot.md` és az `easter-munkamodszer.md` fájlt; (2) a Mac-en a
   > `Claude outputs/2026-09-26-atadas/ATADAS.md` fájlt. Ellenőrizd md5-tel, hogy a `docs/` fájljai egyeznek az ATADAS.md-ben
   > leírtakkal. Utána tedd fel a 4. pontról a következő, egyetlen kérdést.

## 2. Az előző munkamenet azonosítói

| Mi | Érték |
|---|---|
| Helyi munkamenet-azonosító (`CLAUDE_CODE_SESSION_ID`) | `f781d964-b81e-5632-9fe5-5c6123fa9530` |
| Távoli munkamenet (`CLAUDE_CODE_REMOTE_SESSION_ID`) | `cse_01D1accJauceMuLUZQDDb4on` |
| Webes hivatkozás | https://claude.ai/code/session_01D1accJauceMuLUZQDDb4on |
| A napló másolata | ebben a mappában: `session-log-f781d964.tar.gz` — a fő `.jsonl`, 104 alügynök-napló (2026-09-22…25) és 41 eszköz-kimenet |

**A naplóról tudni kell (pontosan):**
- Az **alügynök-naplók teljesek**: minden kutató és ellenőrző ügynök munkája 2026-09-22-től benne van.
- A **fő beszélgetés naplója nem teljes.** A munkamenet 2026-09-24-én és 2026-09-26 00:03-kor (UTC) tömörítődött, és a
  fő `.jsonl` mindkétszer újraindult — a fájlban csak a második tömörítés utáni rész van, az elején az összefoglalóval.
- **A saját hibám:** a 2026-09-24 → 26 közötti fő naplót (D-44…D-48 és a 4. pont) egy korábbi másolat még tartalmazta;
  frissítéskor felülírtam, mielőtt észrevettem, hogy a fájl közben újraindult. Ez a rész helyben nem állítható vissza.
- Ami megvan belőle: a tömörítési összefoglaló (a `.jsonl` elején), a döntések és kutatások a `docs/`-ban, és a
  projekt-memória (`easter-spec-allapot.md`), amely lépésenként, szó szerinti idézetekkel vezeti a menetet. A
  beszélgetés maga az appban, a fenti webes hivatkozáson nyitható meg.
- A felhőkonténer (`/home/claude/…`) egy új munkamenetből nem érhető el, ezért van itt a másolat.

## 3. Hol tartunk — pontosan

**Az utolsó nyitott lépés: a fejlesztés előtti lista 4. pontja — mit adjon be a rendszer a hookokon át.**

- A kutatás kész (`docs/research/projekt-kontextus/SZINTEZIS.md`, 7–10. szakasz). Mérlegem: a munkamenet elején sablonból
  készült rövid szöveg + minden kérdésnél (Claude Code, Codex, Gemini CLI) küszöb fölötti, kevés találat beadása,
  „referencia, nem utasítás" jelöléssel; ahol a kliens nem tud beadni (Cursor, Antigravity, Copilot), ott az MCP marad.
  Ez a D-15/3 („a hook csak emlékeztet, elhagyható") átírása lenne.
- A kérdésre a felhasználó nem választott, hanem visszakérdezett, szó szerint: *„tetszik az ajanlasod, de webes kereses
  igazolta hogy szukseg van ra? nem eleg ha csak hagyjuk az agentnek hogy mint egy memory bank hasznalja a rendszert?"*
- A válaszom (elküldve): a bizonyíték **iránya** egyértelmű, de a legerősebb közvetlen mérés gyenge — arXiv:2607.20972
  (Saha, 2026): egyszerzős, nem lektorált, 12 futás, egy modell (Sonnet 5), egy kliens (Claude Code), egy feladat; a
  „memory bank" helyzetben 0 memória-hívás 114 lépésben. Mellette: MEMTRACK (NeurIPS 2025 workshop), egy memory-bank MCP
  karbantartója („one cannot enforce an MCP tool to be called"), a gyártók és a működő eszközök beadnak. Ellene: nincs
  több klienst és modellt összevető mérés; a noszogatás modellfüggő; a beadásnak zaja van.
  **Javaslatom: a felhasználó szabálya szerint („fejlesztés előtt mindent ki kell mérni") mérjük ki magunk** egy kis
  prototípus MCP-szerverrel, előre feltöltött memóriával, néhány valós feladaton, Claude Code-dal és Codexszel, három
  változatban (csak eszközök = memory bank; + indító sablon; + kérdésenkénti beadás): hányszor nyúl a memóriához, és jobban
  oldja-e meg a feladatot. Ára: a prototípus és az agent-futások a felhasználó fiókján, a gépén.
- **A következő lépés: EGY kérdés (AskUserQuestion), ajánlott első:**
  1. „Mérjük ki magunk, fejlesztés előtt (ez az ajánlott)"
  2. „Döntsünk most: beadás, ahol a kliens tudja"
  3. „Maradjon memory bank: csak MCP + indító sablon (D-15 marad)"

## 4. Ebben a munkamenetben hozott döntések (mind a `docs/00-dontesek.html`-ben)

| Döntés | Lényeg |
|---|---|
| **D-44** | Nincs dream; kikerült a célok közül (a projektleírásban is jelölve). |
| **D-45** | A Jev (TypeSafe AI) most nem kerül be; kutatás `docs/research/jev/`, számok: mérések 20. szakasz. |
| **D-46** | Az angol az elsődleges nyelv, a magyar támogatott, a többi most nem szempont (a D-01/3 átírva); CJK tárgytalan. **Jelezve:** a D-02 kapuzott keresésének indoka gyengül — angolon a vak fúzió nyer (+0,088), magyaron a kapuzott (+0,074); a ParadeDB-s újramérés angol+magyar korpuszon döntsön. |
| **D-47** | Minden rendszernév angol: `memory/`, `audit/`, `logs/`, `db/`; konténerek `app`, `embedder`, `db`; parancsok `serve`, `maintain`, `maintain admin-link`; sémák `derived`, `cache`, `core`. |
| **D-48** | A projektet a repóbeli MCP-beállítás fejléce adja (egy bejelentkezés; a modell nem nevezhet meg projektet); az írás szintje (projekt / közös / személyes) kötelező paraméter; a közös tudásba írás előbb visszaszól; agent-munkamenetben a keresés csak az aktuális projektet, a közös tudást és a saját személyes mappát látja. |

A felhasználó további kimondott szabálya (2026-09-25): *„fejlesztes elott mindent el kell donteni amit lehet es kimerni!
ne legyen olyan lehetoleg csak ami nagyon koltseges most merni hogy majd kozbe vagy utana!"*

## 5. A fejlesztés előtti lista (28 + 1 pont) állapota

| # | Pont | Állapot |
|---|---|---|
| 1 | Rendszernevek angolul | ✅ D-47 |
| 2 | A felületi katalógus forrása | ✅ már a D-30/1 eldöntötte (egyenrangú) — kérdés nélkül lezárva |
| 3 | A felület technológiája (framework, UI-könyvtár, téma) | nyitva — a felhasználó szerint „majd", kutatással |
| 4 | Mi kerüljön a hookon át az agent elé | **FOLYAMATBAN — lásd a 3. szakaszt** |
| 5 | Az index táblaszerkezete, táblanevek (angol) | nyitva — én teszem le javaslatként |
| 6 | `format_version` kezdőérték, mi emeli | nyitva |
| 7 | Postgres-driver Bun alatt | nyitva |
| 8 | Drizzle + ParadeDB (nyers `sql` vagy 1.0 RC; séma-feltolás) | nyitva |
| 9 | Olvashatatlan fejléc kezelése | nyitva |
| 10 | Napló formátuma: sorok vagy JSON | nyitva |
| 11 | MCP resource kell-e | nyitva |
| 12 | A formátum-átírás gombjának helye | nyitva |
| 13 | Gyengült indokú döntések újranyitása (D-02 a mérés után, D-21/12, D-41/4, kétlépcsős tartalom-hash, `remove_diacritics`, D-17/D-33 „+10,8 pp") | nyitva |
| 14 | Három belső ellentmondás a 00-ban (napló-menüpont; „egyetlen tiltás" vs D-42/2 és D-25/3) | nyitva |
| 15 | MCP SDK-k és a 2026-07-28-as protokoll | kutatandó |
| 16 | A beágyazó modell angolul | kutatandó |
| 17 | Mérőkészlet angol+magyar korpusszal ParadeDB-n (→ D-02) | mérendő |
| 18 | Duplikátum-küszöb saját korpuszon (D-20) | mérendő |
| 19 | ParadeDB-index felépítési ideje | mérendő |
| 20 | `pg_dump` → visszaállítás + index | mérendő |
| 21 | Tipikus bejegyzés-hossz → alapértelmezett találatszám | mérendő |
| 22 | `pg_amcheck` hidegen | mérendő |
| 23 | Beágyazások újraszámolásának ideje | mérendő |
| 24 | Szinkron naplóírás költsége | mérendő |
| 25 | Beágyazó késleltetése angol+magyar rövid kérdésekkel | mérendő |
| 26 | A drótvázak (`60-felulet.html`) újrarajzolása — 39 eltérés + 5 döntés nélküli elem | nyitva; jelentés: `docs/_ellenorzes/60-felulet-2026-09-25.md` |
| 27 | Naplószegmens mérethatára | javaslat: most becsült érték, valós kalibrálás használat közben — a felhasználó még nem hagyta jóvá |
| 28 | „Ennyi eltérésnél állj meg" küszöb | ugyanígy |
| 29 | Honnan a projekt, hová ír, mit lát a keresés | ✅ D-48 |

A nyelvi döntés hatáselemzése 20 nyitott kérdéssel: `docs/_ellenorzes/nyelv-hataselemzes-2026-09-25.md`.
Új, a 4. ponthoz tartozó méréseket (relevancia-küszöb és darabszám a beadáshoz) a döntés után kell a listához adni.

## 6. A dokumentumok mai állapota (md5, 2026-09-26)

```
e6b5c79db963d639245258cd27755617  docs/00-dontesek.html   (D-01…D-48, 51 szakasz)
58d3597797cf474b971cd0eee0f16dfb  docs/20-adatmodell.html
070054ac9b1cdfbf51b8a0e81be4ae60  docs/30-kereses.html
1c28985927dc9cffd620442e0395ed7d  docs/40-mcp.html
ed691cff7557e03665c7cb7c5476aed9  docs/50-uzemeltetes.html
4a294b80e360ff14084e4e2f746903e3  docs/60-felulet.html
6ee4dda470494430e0a933768280fc43  docs/90-meresek.html    (21 szakasz; 19 = dream, 20 = Jev)
a33706294546ec136183305b1a083ccc  docs/research/README.md
```
Kutatási kampányok ebben a munkamenetben: `docs/research/dream/`, `jev/`, `projekt-kontextus/` (két kör).

## 7. A munkamódszer (a felhasználó szabályai — a részletek a projekt-memóriában, `easter-munkamodszer.md`)

- Én csak koordinálok. Webes keresést kizárólag Sonnet alügynök végez, **Exa** eszközzel (ToolSearch:
  `select:mcp__Exa__web_search_exa,mcp__Exa__web_fetch_exa`), a `deep-web-research` skill elvei szerint, párhuzamosan.
  Minden találatot két további forrás erősítsen meg; utána adverzariális ellenőrző kör. A szintézist én (Opus) írom.
- Döntés csak AskUserQuestion-nel, **egyszerre egy kérdés**, az ajánlott az első „(ez az ajánlott)" címkével; a saját
  ötletemet külön, kimondva jelölöm.
- A döntési naplóba csak az kerül, amit a felhasználó kimondott; változásnál dátumozott megjegyzés + „Korábban:".
- Szám csak akkor kerülhet specbe, ha a `90-meresek.html`-ben is ott van; ismerten hibás szám nem maradhat.
- `docs/_legacy/` — semmit nem szabad tényként átvenni.
- Minden markdownba írt mezőnév és minden rendszernév angol (D-08, D-47).
- Minden kész lépés azonnal a Mac-re; minden döntés vagy kérdés előtt az állapot a projekt-memóriába — így egy API-hiba
  után sem vész el semmi.
- A köztes fájlokat a végén törölni kell.

## 8. A szerkesztés menete és az eszközök (`eszkozok/` ebben a mappában)

A Mac a mérvadó. Egy dokumentum szerkesztése: behozni (stage vagy a `device_bash`-sel olvasni) → a konténerben szerkeszteni
→ ellenőrizni → `SendUserFile` → `device_commit_files` **`fileUuid`-dal** és `expectedMtimeMs`-szel → md5-tel ellenőrizni.
(Ismert csapda: egy korábban `SendUserFile`-lal küldött útvonalnál a `stagedPath`-os commit a RÉGI tartalmat írta ki.)

| Fájl | Mire való |
|---|---|
| `ellenoriz.js` | Playwright-ellenőrzés mind a hét HTML-re: vízszintes túlcsordulás, horgonyok, duplikált id, táblázat-oszlopok, szakaszszámok, D-hivatkozások, fájlközi linkek, JS-hibák (`/opt/pw-browsers/chromium`, `playwright-core`) |
| `szamok.py` | Ellenőrzi, hogy minden új szám szerepel-e a `90-meresek.html`-ben (egy `eredeti/` alapváltozathoz képest) |
| `segit.py` | Segédfüggvények a 00 szerkesztéséhez (szakaszhatár, tétel módosítása „Korábban"-nal, tárgytalanná tétel) |
| `maradek.py`, `mutat.py` | SQLite-maradványok keresése; szakasz kiírása |
| `d45.py` … `d48.py` | A D-45…D-48 beírásának szkriptjei — mintának |
| `mtime.json` | A dokumentumok utolsó ismert mtime-ja a Mac-en (a commit `expectedMtimeMs`-éhez; commit előtt mindig frissen lekérni) |

A szkriptekben a `/home/claude/work/…` útvonalak a régi konténerre mutatnak — az új munkamenetben át kell írni.
