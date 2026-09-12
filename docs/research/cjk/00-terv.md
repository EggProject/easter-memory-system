# Kutatási terv — szóköz nélküli írásrendszerek (CJK) a szöveges keresésben

**Kampány:** `cjk` · **Dátum:** 2026-09-12 · **Keresők:** 1 Sonnet subagent (`sq01`)

## Miért indult

A dokumentum-átolvasás során felmerült, hogy a szöveges keresési láb (SQLite FTS5) a kínai,
japán és koreai szöveget nem tudja szavakra bontani, mert ezekben az írásrendszerekben nincs
szóköz. A kérdés eldöntése előtt tévesen abból indultam ki, hogy a rendszert csak magyarul
fogják használni — ezt a felhasználó visszautasította, és a kérdést rendes kutatással kellett
megválaszolni, nem feltevéssel.

**A döntendő kérdés:** építsünk-e CJK-tokenizálást, és ha igen, milyet?

## Al-kérdések (sq01)

1. Mit kínál az SQLite FTS5 tokenizálóként, és melyik alkalmas szóhatár nélküli szövegre?
   Szó szerinti dokumentáció kell, nem összefoglaló.
2. Elérhető-e ICU-alapú tokenizálás SQLite-ban, és mi az ára (függőség, méret, modul-váltás)?
3. Mennyivel nő az index a `trigram` tokenizálóval? Van-e hivatalos szám?
4. Hogyan oldják meg mások: PostgreSQL, Meilisearch, Typesense, Elasticsearch/OpenSearch?
   Egyetlen bevett megoldás van, vagy több, egymásnak ellentmondó?
5. Mennyit ér a lexikai (BM25) keresés CJK nyelveken egyáltalán, beágyazáshoz képest?
   Kell mért, lektorált adat.
6. Mit veszítenénk a magyar kereséssel, ha trigramra váltanánk?

## Módszertani kikötés

A `sqlite.org` és a többi hivatalos dokumentációs domain lapjait **nyers HTML-ként** kellett
lekérni (`curl`), nem a WebFetch összefoglalóján keresztül — a pontos, szó szerinti technikai
megfogalmazások számítanak, és egy kis modell összefoglalója ezeket elnyelheti. Ez a kikötés
menet közben igazolódott: az OpenSearch CJK-lapja és több GitHub README kliens-oldalon töltődik,
a WebFetch hiányos tartalmat adott vissza (ld. `hianyok.md`).
