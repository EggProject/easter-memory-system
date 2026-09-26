# Szintézis — megéri-e a Jevet használni az easter-memory-systemben?

Kampány: `jev/` · 2026-09-25 · 1 azonosító kör (SQ00) + 6 kutatási egység (SQ01–SQ06) + 3 ellenőrző egység
(ELL01–ELL03), 380 egyedi link, mind az **Exa** keresővel, párhuzamos Sonnet alügynökökkel. Szintézis: Opus.

A felhasználó kérdése szó szerint: „van egy új »Jev« nevezetű döntést támogató baromi gyors model, végeztess deep
research-t, hogy megéri-e nekünk bármelyik funkciónál használni? például akár kategória döntés vagy ellenőrzés új jegyzet
írásnál stb nem tudom, vizsgáljuk ki, de ne erőltessük csak azért mert kérem, ha viszont érdemes lehet használni akkor is
úgy tervezzük bele a rendszerbe hogy kapcsolóval működjön, lehessen kezelni ha elfogy a balance és ha nem elérhető auto
visszaállunk adott helyen a jelenlegi módszerre".

---

## 1. Mi a Jev — ellenőrzött tények

- A **TypeSafe AI** (San Francisco, alapítva 2024, ~40 millió dolláros seed, DCVC) modellje, bejelentve 2026-09-15-én
  (a cég saját blogja 09-14-et mutat). Név: `jev-1.13.0`. 2026-09-20 óta várólista nélkül elérhető. (ELL01/1, /5, /11)
- **Nem ír szöveget.** Bemenet: egy „state" (szöveg vagy JSON) és tipizált kérdések — **Choice** (legfeljebb 255 opció),
  **Score** (2–10 szint), **Noul** (igen/nem). Kimenet: valószínűség és konfidencia. Egy hívásban több kérdés. (ELL01/1)
- **Csak felhős API**, zárt súlyok, nincs helyben futtatható változat. OpenRouter, Vercel és Cloudflare gateway-en is.
- **Ár:** 0,042 dollár millió bemeneti tokenenként, a kimenet ingyenes. Kredit-alapú, a kredit nem visszatéríthető. (ELL01/7–8)
- **Nem determinisztikus:** nincs seed vagy temperature; a gyártó saját mérése szerint kb. 0,01-es szórás. (ELL01/2)
- **Késleltetés:** a gyártó szerint 70–500 ms, „nyugati parti laptopról" mérve; független, kontrollált mérés nincs. (SQ01)
- **Nincs SLA.** Van státuszoldal. A felelősségkorlát ingyenes használatnál 50 dollár, fizetősnél a 12 havi díj vagy
  50 dollár közül a nagyobb. (ELL01/6, /10)

## 2. A mi rendszerünkben ma ki dönt?

Ez a kérdés kulcsa. A rendszerünkben **minden tartalmi döntést vagy egy frontier LLM hoz — a hívó ágens (Claude, Codex) —,
vagy ember.** A szerver szándékosan nem ítél (D-01/2).

| Döntési pont | Ki dönt ma |
|---|---|
| Melyik kategóriába kerül egy új bejegyzés | a hívó ágens, a kategória-promptok alapján (D-22) |
| Duplikátum-e | a szerver beágyazással jelzi, a hívó ágens dönt, látja a hasonlók teljes tartalmát (D-20) |
| Ellentmond-e egy meglévőnek | a hívó ágens, ugyanabból a D-20-válaszból; a szerver nem vizsgálja |
| Van-e benne titok | senki — nincs kapu (D-38) |
| Melyik keresési találat releváns | a szerver sorrendet ad (hibrid keresés + kapu), a hívó ágens válogat |

Vagyis a Jev nálunk **nem váltana ki egyetlen lassú vagy drága LLM-hívást sem** — mert a szerver nem hív LLM-et. Csak egy
**új, második döntéshozó** lehetne a hívó ágens mellett. A független mérés szerint pedig gyengébb nála: az AY Automate
2026-09-20-i mérése szerint *„Jev behaved like a good small model, not like a frontier model"*; az OpenRouter
Banking77-mérésén 81,0% a Claude Opus 5 84,4%-ával szemben. (SQ05, ELL02/3)

## 3. Funkciónként

**Kategória-döntés — nem éri meg.** A kategóriát ma egy erősebb modell választja. Arra, hogy egy gyengébb modell utólagos
ellenőrzése javítana a frontier döntésén, **nincs számszerű forrás**; egy 2026-os cikk (arXiv:2609.01345, „Cheap Verifiers,
Large Blind Spots") szerint az olcsó ellenőrző vakfoltja épp az erősebb modell hibáinál nő. Ráadásul a D-01/2 szó szerint
kizárja: „se kategória-besorolást".

**Ellenőrzés új jegyzet írásánál — gyenge.** Az egyetlen hely, ahol a beágyazás nem elég: az ellentmondás (D-44 kutatása).
A Jevnek van erre bevett mintája (egy „contradicts" Noul-kérdés). De: a gyártó saját dokumentációja mutat példát arra, hogy
ugyanaz a tény Noul-ként és Choice-ként kérdezve **ellentétes választ** ad; magyarra nincs mérés; és a hívó ágens ugyanazt a
két bejegyzést amúgy is látja a D-20 válaszában, és erősebb bíró. A többlet legfeljebb egy jelzés lenne.

**Titokszűrés — nem.** A D-38 szerint nincs kapu. És egy titok-ellenőrzéshez a bejegyzést egy amerikai szolgáltatóhoz
kellene küldeni — pont azt a tartalmat, amit védeni akarnánk.

**Keresési találatok rangsorolása — itt van a legtöbb bizonyíték, de a legnagyobb adatkiáramlással.** Rangsorolásra van
gyártói és független adat (pl. egy nyílt csomag szerint az NFCorpus-on kb. kétszeres precizitás, némi recall árán). Viszont
**minden keresés** kérdése és a jelöltek tartalma kimenne, minden keresés lassulna, és a hatást a saját mérőkészletünkön
(angol + magyar) kellene kimérni.

## 4. Ami minden funkcióra áll

- **Adat:** csak USA-ban fut („The Services are hosted in the United States."); fix megőrzési idő nincs; a „zero data
  retention" egyik hivatalos TypeSafe-dokumentumban sem szerepel — csak az OpenRouter és a Vercel gateway-en át van ZDR.
  A DPA-ban van EU SCC; a DPF-listán szereplés nem ellenőrizhető; a SOC 2 vitatott. (ELL03)
- **Érettség:** tíznapos, „preview" termék; a korlátok előzetes értesítés nélkül változhatnak; a hivatalos API nem
  dokumentál hibakódot az elfogyott kreditre (a gateway-ek igen: OpenRouter és Vercel 402, Cloudflare 429). (ELL01/8–9)
- **Magyar:** semmilyen mérés nincs. (ELL02/4)
- **Saját döntéseink:** D-01/2 (csak beágyazó; „se kategória-besorolást"), D-01/8 (kevés külső függőség), D-17/4 (ember dönt).

## 5. Ha egyszer mégis — a bevett minta (SQ06, ELL03/6)

Kapcsoló (kill switch) konfigurációból; circuit breaker (Node-ban az `opossum`, futásidejű függőség nélkül); minden hívásra
határidő; kétszintű költségkeret (figyelmeztetés, majd megállás); a visszaállás **soha nem néma** — naplóba és az
állapot-nézetre kerül (Google SRE, Azure, Polly; a LiteLLM „silently rerouted" megoldása ennek ellentmond); és először
**árnyék-mód**: a külső modell számol és naplóz, de a döntést a mostani módszer hozza, és összevetjük.

## 6. A mérlegem

**Ma egyik funkciónál sem éri meg.** A Jev ott ad sokat, ahol egy rendszer maga hív LLM-et gyakori, egyszerű döntésekre —
nálunk ilyen hívás nincs, mert a döntést a hívó ágens hozza. Ahol mégis hozzáadna valamit (rangsorolás, ellentmondás-jelzés),
ott ügyféladatot küldenénk egy tíznapos, amerikai, SLA nélküli szolgáltatónak, magyar mérés nélkül.

Amikor érdemes újranézni: ha van EU-s futtatás vagy hivatalos ZDR; ha van magyar mérés; ha van SLA; és ha lesz olyan pont a
rendszerben, ahol a szervernek ágens nélkül kell döntenie.

## 7. Amire nincs forrás

- Magyar nyelvű Jev-mérés — semmilyen.
- Számszerű haszon arra, ha egy frontier ágens döntése után egy gyors modell ellenőriz.
- Független, kontrollált késleltetés-mérés.
- A Jev-Mem memória-cikk (arXiv:2609.23986) eredményeinek független megismétlése.
- A TypeSafe DPF-státusza és SOC 2-je elsődleges forrásból.
- Kalibráció: a gyártó nem közölt mérőszámot; a gyakran idézett független kalibrációs számhármas egy belsőleg
  ellentmondásos oldalról jön — nem igazolt, ezért nem vesszük át (ELL02/2).

## 8. A döntés — 2026-09-25: D-45

A felhasználó választása: „Most ne építsük be" — ez volt az ajánlásom is. A kutatás és a kapcsolható beépítés mintája
eltárolva; az újranézés feltételei a 6. pontban. A számok a mérési dokumentum 20. szakaszában.
