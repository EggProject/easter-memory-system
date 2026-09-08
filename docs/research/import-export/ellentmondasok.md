# Ellentmondások — import és export kutatás (K-03)

Az `sq01..sq04/contradictions.md` egyesítve, mindkét oldal idézetével, és jelölve, hogy a
forrás-dokumentum feloldotta-e az ellentmondást, vagy nyitva marad.

---

## SQ-01 — Markdown-tudástárak export-formátumai

### 1. Joplin RAW formátum "lossless"-e valóban ugyanaz-e, mint a JEX?

**Egyik oldal** — a hivatalos doksi (joplinapp.org, T1):
> "A 'raw' format is also available. This is the same as the JEX format except that the data is
> saved to a directory and each item represented by a single file."

Ez implikálja, hogy a RAW is "lossless", mert csak a csomagolás módja tér el a JEX-től.

**Másik oldal** — a hivatalos fórum (discourse.joplinapp.org, T2) a RAW-ot és a JEX-et **külön**
tárgyalja: a RAW leírásánál az ID-alapú fájlneveket és a `/resources` mappát említi, a JEX-nél
csak "single file of everything in a profile" és "not human readable" — nem ismétli meg explicit a
"lossless" jelzőt a RAW-ra.

**Feloldás:** nem valódi ellentmondás, inkább hangsúly-eltérés — a T1 forrás explicit kimondja az
egyenértékűséget, a T2 forrás csak nem hangsúlyozza újra. A "RAW = lossless" állítás közvetlenül
csak a hivatalos oldal egyetlen mondatára támaszkodik, nem kettős, független megerősítésre.

### 2. Nincs más azonosított tartalmi ellentmondás a T1/T2 forrásaink között

A kutatás nem talált két T1 vagy T1/T2 forrást, amelyek egymásnak ellentmondó tényállítást tettek
volna ugyanarról a konkrét formátum-viselkedésről. A T3-as (content-farm, vélemény) oldalak közötti
esetleges ellentmondásokat szándékosan nem vizsgálták, mert ezeket eleve nem használták fel érdemi
állítás forrásaként.

### 3. Lehetséges látszólagos ellentmondás: "Obsidian frontmatter hordozható" vs. "Obsidian markdown nem sima markdown"

**Egyik oldal** — az `obsidian.md/help/properties` (T1) oldal azt sugallja, hogy a frontmatter YAML,
tehát más eszközökkel (VSCode, szkriptek) is olvasható/szerkeszthető — ez a "hordozhatóság"
benyomását kelti.

**Másik oldal** — a `github.com/zoni/obsidian-export` (T1, a tool önmagáról) létezése és célja
("export an Obsidian vault to regular Markdown", mert "obsidian-export supports most but not all of
Obsidian's Markdown flavor") azt mutatja, hogy a **teljes fájltartalom** (wikilinkek, embedek) NEM
sima markdown, csak a frontmatter YAML-blokk az.

**Feloldás:** nem valódi ellentmondás, hanem két különböző rétegre vonatkozó állítás — a frontmatter
(metaadat-réteg) valóban szabványos YAML, miközben a törzsszöveg (tartalom-réteg) Obsidian-specifikus
szintaxis-elemeket tartalmazhat.

### 4. Az OKF "nyíltsága" és a "Google alone" kontrollja között feszülő állítás

**Egyik oldal** — a cloud.google.com blogbejegyzés (T1) egyszerre állítja, hogy az OKF
"vendor-neutral" és "an open standard".

**Másik oldal** — ugyanabból a forrásból kiderül, hogy a specifikációt kizárólag Google-alkalmazottak
írták ("Authors: Sam McVeety..., Amir Hormati..."), a referencia-implementációk is mind
Google-termékek (BigQuery enrichment agent, Google Cloud Knowledge Catalog), és nincs dokumentált
harmadik feles hozzájárulás vagy elfogadás a publikáció idején.

**Feloldás:** nem forrás-ellentmondás (a forrás önmagával nem mond ellent), hanem egy gyártói
állítás ("vendor-neutral", "open standard") és a ténylegesen dokumentált állapot (egyetlen gyártó
által írt, egyetlen gyártó által implementált specifikáció) közötti feszültség. Kezelése: a
megfogalmazás leírja, hogy a formátum *célja* nyílt, de az *aktuális állapota* (2026 közepén)
egyetlen szereplőhöz kötött — **nyitva marad**, hogy a jövőben lesz-e harmadik feles elfogadás.

---

## SQ-02 — Ütközéskezelés importnál

Nem található éles, tényszerű ellentmondás két forrás között ugyanarra az állításra nézve. Az
alábbiak inkább látszólagos következetlenségek (ugyanaz a márkanév, más alrendszer) vagy
konvergáló, nem ellentmondó nézőpontok.

### 1. "Nextcloud" — két különböző alrendszer, két különböző alapértelmezett stratégia

**Egyik oldal** — a Nextcloud **szerver-oldali fájlművelet** (pl. UI-ból történő másolás azonos
nevű célra) a közösségi fórum szerint (2021, help.nextcloud.com) **blokkolja** a műveletet:
> "Could not copy [filename]; target exists."
A felhasználó explicit funkciókérést nyitott az automatikus átnevezésre.

**Másik oldal** — a Nextcloud **desktop szinkron-kliens** ezzel szemben — a hivatalos dokumentáció
(`user_manual/desktop/conflicts.rst`) szerint — **duplikál és átnevez**, nem blokkol:
> `"mydata (conflicted copy 2018-04-10 093612).txt"` tartalmazza *"local contents"*-t.

**Feloldás:** nem ellentmondás, hanem két különböző komponens két különböző tervezési döntése
ugyanazon termékcsaládon belül. A megállapítások mindkettőt külön, megnevezve idézik, nem
összemosva — mert egy olvasó, aki csak "Nextcloud"-ot lát, tévesen azt hihetné, hogy a termék
egyetlen konzisztens stratégiát követ.

### 2. Konvergencia (nem ellentmondás), de érdemes kiemelni

Három, egymástól független forrás **ugyanabba az irányba** mutat, jóllehet különböző bizonyítékkal
támasztja alá:
- **GNOME HIG** (tervezési irányelv, nem mért adat): az undo jobb, mint a megerősítő dialógus.
- **NNGroup/Nielsen** (szakértői ajánlás, a cikk maga is jelzi, hogy nem hivatkozik kutatásra):
  ugyanez az ajánlás.
- **Brindescu et al. 2020** (ténylegesen mért, lektorált adat, más területről — git merge-ütközés):
  a *kézi* döntést igénylő ütközésfeloldás mérhetően (26x) több hibával jár, mint az automatikusan
  feloldható eset.

**Feloldás:** ez a három forrás nem mond ellent egymásnak, de csak az egyikük (Brindescu et al.)
mért adat — a másik kettő bevett gyakorlat/szakértői vélemény. Nem kezelendő "három egybehangzó
bizonyítékként".

### 3. Anki — gyenge jelzés lehetséges belső feszültségre (nem megerősített)

A keresési találatok címei között több Anki-fórum-topik utal arra, hogy a "duplikátum = frissítés
az első mező alapján" alapértelmezett stratégia néha meglepi/összezavarja a felhasználókat (pl.
*"Anki import is misleading"*). Ezeket a szálakat nem kérték le, tartalmukat nem ismerik — **nyitva
marad**, gyenge (cím-szintű) jelzésként rögzítve, nem tényként.

---

## SQ-03 — Személyes adat exportja (GDPR)

### 1. Látszólagos, de feloldott ellentmondás: a WP242 rev.01 dátuma

Három különböző dátum jelenik meg három forrásban ugyanarra a dokumentumra:

- Az EC newsroom **listaoldala** (item_id=611233): "Date: 27/10/2017"
- Maga a **hivatalos PDF** (1. oldal): "Adopted on 13 December 2016 / As last Revised and adopted on
  5 April 2017."
- Az **EDPB oldala**: az EDPB az első plenáris ülésén (2018. május 25.) hagyta jóvá (endorsed) a
  dokumentumot GDPR-instrumentumként.

**Feloldás:** nem valódi ellentmondás, hanem négy különböző esemény dátuma ugyanahhoz a
dokumentumhoz: (1) eredeti WP29-elfogadás 2016.12.13., (2) felülvizsgált "rev.01" változat
elfogadása 2017.04.05., (3) az EC newsroom közzétételi/indexelési dátuma feltehetően 2017.10.27.,
(4) az EDPB általi utólagos jóváhagyás 2018.05.25. (mivel a GDPR csak akkor lépett hatályba, az EDPB
csak ekkor "örökölhette meg" a WP29 dokumentumait). A megállapítások mindkét releváns dátumot
(elfogadás: 2016.12.13./2017.04.05.; EDPB-jóváhagyás: 2018.05.25.) külön feltüntetik, hogy ne
keveredjenek. **Feloldva.**

### 2. Nem található valódi tartalmi ellentmondás

A hat vizsgált terület (GDPR 20. cikk, GDPR 15. cikk, WP29/EDPB iránymutatás, DTP/DTI, konkrét
termékek, törlés+export) között nem található egymásnak ellentmondó állítás a felhasznált T1-es
forrásokban. A "törlés előtt kötelező export" kérdésben a különböző források (GDPR szövege, ICO
guidance, WP242, GitHub doksi) egymást **erősítik**, nem mondanak ellent egymásnak: mindegyik vagy
hallgat a kérdésről, vagy csak tájékoztatási (nem technikai) kötelezettséget ír elő. Konzisztens
kép, nem vitatott pont.

---

## SQ-04 — Tömeges behozatal indexelt rendszerbe

### 1. "Mindent-vagy-semmit" vs. "megtartom, ami átment" — látszólagos ellentmondás, valójában architekturális különbség

**Egyik oldal** — PostgreSQL COPY: hiba esetén a korábban beírt sorok logikailag eltűnnek:
> "these rows are left in a deleted state; these rows will not be visible"
— gyakorlatilag teljes visszagörgetés. MySQL LOAD DATA `IGNORE` nélkül: "data-interpretation errors
terminate the operation" — a hiba megállítja a műveletet.

**Másik oldal** — Elasticsearch Bulk API: elemenkénti (`items` tömb) válasz, ami arra utal, hogy a
sikeres elemek a hibások mellett is bekerülnek az indexbe — vagyis "megtartom, ami átment".

**Feloldás:** nem valódi ellentmondás, hanem architektúrafüggő különbség — a COPY és a LOAD DATA
egyetlen adatbázis-tranzakcióba csomagolja az egész műveletet (ezért a hiba a tranzakciós szemantika
miatt mindent érint), míg az Elasticsearch Bulk API-nak nincs több-dokumentumos tranzakciós fogalma
— minden akció önálló egység, így a részleges siker az alapértelmezett viselkedés, nem egy külön
bekapcsolható opció. A tanulság: a döntés nem "melyik a helyes minta", hanem "milyen egységekben
(fájlonként? kötegenként? tranzakciónként?) definiáljuk a sikeres/hibás állapotot" — ez tervezési
döntés, nem egyértelműen "helyes" válasszal. **Feloldva (architekturális magyarázattal).**

### 2. MySQL `IGNORE` mint választható opció, nem alapértelmezés

Érdemes megjegyezni, hogy a MySQL LOAD DATA esetében a "megtartom, ami átment" viselkedés **nem az
alapértelmezés**, hanem egy explicit opt-in (`IGNORE` kulcsszó). Ez feszültségben áll az
Elasticsearch mintájával, ahol a részleges-siker viselkedés **nincs is kikapcsolható módon**
dokumentálva (nincs "all-or-nothing" bulk mód a lekért dokumentáció szerint). **Feloldás:** ez
megerősíti az 1. pont következtetését — a kérdés nem az, hogy melyik a "jó" minta általánosan, hanem
hogy a rendszer tervezője milyen alapértelmezést és milyen explicit vezérlőkapcsolót ad a
kezelőnek.

### 3. Nincs talált direkt, egymásnak ellentmondó számadat

A méretkorlátokra (GitHub, PyPI, Elasticsearch, S3) vonatkozó számok forrásonként különböznek
(50 MiB/100 MiB GitHub, 100 MB PyPI, 100 MB Elasticsearch HTTP-kérés), de ezek nem egymásnak
ellentmondó állítások ugyanarról a dologról, hanem különböző rendszerek különböző, egymástól
független korlátai. Nem található két forrás, amely ugyanarról a rendszerről/mezőről egymásnak
ellentmondó számot közölt volna.
