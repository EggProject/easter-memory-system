# Szintézis — üzemeltetés (Spec 50 előkészítés)

Kampány: `uzemeltetes/` · 2026-09-15/16 · 6 kutatási egység (SQ01–SQ06) + 3 ellenőrző kör (ELL01–ELL03) + saját mérések.
A kutatást párhuzamos Sonnet alügynökök végezték, a szintézist és a döntési javaslatokat Opus írta.

---

## 1. A legfontosabb: három állítás, amit az ellenőrző kör megváltoztatott

**a) Az MCP `ping` LÉTEZETT, és 2026-07-28-án távolították el.**
Az SQ02 először azt állította, hogy „a protokollban soha nem volt health/heartbeat fogalom”. Ez **téves**.
Az ELL01 a nyers sémafájlokból igazolta: `PingRequest` benne volt a 2024-11-05, 2025-03-26, 2025-06-18 és
2025-11-25 verziókban, és a 2025-11-25-ös specifikáció szövege szó szerint ezt írta: az implementációk
„SHOULD periodically issue pings to **detect connection health**”. A 2026-07-28-as séma nyers tartalmában
nulla találat a `ping`/`Ping` szóra. Az eltávolítás hivatalos indoklása (SEP-2575) nem azt mondja, hogy
a kapcsolat-egészség nem kérdés, hanem hogy **a szállítási rétegre került** (HTTP keep-alive, SSE-komment,
STDIO folyamatállapot).

Következmény ránk nézve: az MCP nem ad nekünk kész állapotellenőrzést, és ami volt, azt elvitték.
Ha kell ilyesmi, azt nekünk kell megcsinálni — de **dátumozva**, mert ez a tény kétszer változott két év alatt.

**b) A launchd `KeepAlive` szótárban nincs `Crashed` kulcs.**
A kérdésem tartalmazta ezt a kulcsot; az ELL02 Apple saját forráskódjából (`apple-oss-distributions/launchd`)
ellenőrizte a teljes, ~75 kulcsos listát, és `Crashed` **nincs**. A négy hivatalos alkulcs: `SuccessfulExit`,
`NetworkState`, `PathState`, `OtherJobEnabled`. Összeomlás utáni újraindítást a `SuccessfulExit=false`
vagy a puszta `KeepAlive=true` ad.

**c) A `systemctl stop` egyik `Restart=` értéknél sem indít újra.**
Az `always` nem jelenti azt, hogy „mindig visszahozza”. Szándékos leállításnál sem az `on-failure`,
sem az `always` nem indít újra — ez az ELL02 elsődleges forrásból igazolt megállapítása, és egy
elterjedt tévhitet cáfol.

---

## 2. Amit a kutatás egyöntetűen mond

**A monitorozás nem ingyenes, és nekünk nincs, aki fizesse.** A Google SRE könyv saját szavaival írja le,
hogy a monitorozó rendszer maga törékeny és karbantartási teher, és hogy egy 10–12 fős SRE csapatból
1–2 ember kizárólag ezzel foglalkozik. Nálunk nulla ember van erre. A vizsgált egybináris, önüzemeltetett
projektek (Gitea, Forgejo, Miniflux, Jellyfin, Immich) **alapból kikapcsolva** szállítják a `/metrics`
végpontot, a Jellyfin explicit biztonsági indoklással; a Vaultwarden és a Paperless-ngx karbantartói
**elutasították** a natív metrika-végpont beépítését.

**Az audit napló és az üzemeltetési napló szétválasztására nincs kötelező szabvány, csak indok.**
Az OWASP Logging Cheat Sheet mondja ki, hogy más célra gyűjtik őket, „and this often means they should be
kept separate”. A NIST SP 800-92 forrás szerint kategorizál, nem cél szerint, és fizikai szétválasztást
nem ír elő. A négy megvizsgált önüzemeltetett projekt egyike sem vezet külön audit naplót.

**A naplószintek konvenciók, nem mérés.** Az RFC 5424 saját magáról mondja, hogy a nyolc súlyossági szint
nem normatív, „purely informational”. A vizsgált projektek 4–6 szintet használnak, nem nyolcat.

**A forgatás alapértékei csapdák.** A logrotate `rotate` paramétere alapból **0** (nincs megőrzés, amíg be
nem állítják); a journald `MaxRetentionSec` alapból **0** (kikapcsolva) — csak méret-alapú korlátok élnek.
Aki „majd az alapértelmezés megoldja” alapon tervez, az naplót veszít vagy lemezt tölt meg.

**A csendes meghibásodás ellen létezik bevált, dokumentált minta: a dead man's switch.**
Nem azt figyeljük, hogy történik-e hiba, hanem hogy **elmarad-e a várt jelzés** (healthchecks.io, Cronitor,
Prometheus `absent()`). A mentés pontosan ilyen: a NIST SP 800-34, a CIS Controls 11.5 és mindhárom vizsgált
mentőeszköz (restic, borg, Kopia) hivatalos dokumentációja a mentés **aktív ellenőrzését** írja elő, nem
csak az ütemezését.

**A riasztási fáradtságra van kemény szám — de nem a mi szakmánkból.** A Joint Commission Sentinel Event
Alert #50 (hivatalos, szabályozói) 85–99%-os hamis riasztási arányt dokumentál a klinikai gyakorlatban.
Informatikai kontextusban **nincs lektorált mérés**. Az érv átvihető, de ezt ki kell mondani.

---

## 3. Amire sehol nincs publikált válasz (és ezért mi mértük meg)

1. Nincs publikált szám a `VACUUM INTO` időigényére (ezt már a `mentes-frissites` kampány is megállapította).
2. Nincs publikált szám **semelyik** index-újraépítés sebességére: sem FTS5 `rebuild`, sem Elasticsearch,
   sem Meilisearch, sem Typesense.
3. Nincs hivatalos sqlite.org ajánlás arra, **milyen gyakran** fusson integritás-ellenőrzés.
4. Nincs számszerű hivatalos küszöb arra, mekkora WAL-fájl számít „túl nagynak” — a `wal.html` csak
   annyit mond, „grow without bound”.
5. Nincs hivatalos vagy mért összehasonlítás a `SELECT 1` és a `PRAGMA quick_check` között health-check célra.
6. Nincs keretrendszer-független szám arra, mennyivel lassít a szinkron naplóírás.
7. Nincs formális szakirodalom egyfelhasználós, ügyelet nélküli rendszerek riasztási stratégiájára.

A saját méréseink a 1., 3., 4. és 5. pontot részben lezárják — lásd `sajat-meresek.md`.

---

## 4. Amit a mérés hozott, és ami a kutatásból nem derült volna ki

**A `VACUUM INTO` a mentés alatt megakadályozza a WAL checkpointot.** Kontrollos méréssel (3+3 futás):
írás közben, mentés nélkül a WAL stabilan **4,0 MB** (= a dokumentált 1000 oldalas alapérték × 4096 bájt).
A `VACUUM INTO` alatt ugyanaz az író **451–523 MB**-ra fújja a WAL-t ~1,1 másodperc alatt. Ez pontosan
a dokumentált „checkpoint starvation”, működés közben megfigyelve. A dokumentáció leírja a jelenséget,
de számot nem ad hozzá — mi most adtunk.

**A felfújt WAL magától nem megy vissza, de újraindítás nélkül visszanyerhető.** Az írás leállítása után
2 másodperccel is 111 MB maradt; a `wal_checkpoint(PASSIVE)` visszamásolta mind a 28 281 keretet, de a
**fájlt nem zsugorította**; a `wal_checkpoint(TRUNCATE)` 0-ra vitte, futó szolgáltatás mellett.
Ebből közvetlen üzemeltetési szabály következik: **mentés után TRUNCATE checkpoint.**

**A `quick_check` és az `integrity_check` közti különbség a gyakorlatban elenyésző.** A hivatalos
dokumentáció O(N) kontra O(N log N)-t mond (ELL03 szó szerint igazolta). Mérve, meleg lapgyorsítótárral
az arány 1,2–1,3× (44 MB: 29 vs 36 ms; 994 MB: 526 vs 671 ms). **Hideg gyorsítótárral a különbség eltűnik**
(994 MB: 13,5 vs 14,0 s) — ott már nem a bonyolultság, hanem a lemezről olvasás dominál, 20–27-szeres
szorzóval. Health-check tervezésnél tehát nem a `quick_check` vs `integrity_check` választás számít,
hanem az, hogy az adatbázis benne van-e a lapgyorsítótárban.

---

## 5. Nyitott döntések, amelyek a felhasználóra várnak

1. Legyen-e egyáltalán metrika-végpont, és ha igen, alapból be- vagy kikapcsolva.
2. Legyen-e külön üzemeltetési napló az audit napló mellett, és ha igen, milyen formában.
3. Legyen-e állapotellenőrző végpont, és mit ellenőrizzen (az MCP `ping` eltűnése után).
4. Mi történjen induláskor, ha az index hiányzik vagy elavult: várjon, vagy csökkentett módban szolgáljon ki.
5. Milyen gyakran fusson integritás-ellenőrzés, és mi legyen a következménye.
6. Legyen-e dead man's switch a mentésre, és milyen csatornán szóljon.
