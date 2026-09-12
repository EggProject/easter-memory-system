# Önellenőrzés — `mcp-hibak` kampány

Lezárva: 2026-09-12.

---

## Ez a kampány két tervezési hiba javítására indult

A tulajdonos kifogásolta a frissen megírt Spec 40 két pontját, és **mindkét kifogás jogos volt**:

1. **A jogosultság-hiányra adott üres válasz rossz volt.** A hívó modell nem tudja
   megkülönböztetni, hogy „nincs ilyen", „nem láthatod" vagy „hiba történt" — és a végtelen
   újrapróbálkozás ellen sem véd. Ezt nem gondoltam végig.
2. **Nem lett volna szabad nyitva hagyni.** A kérdés eldönthető volt, csak nem kerestem meg
   hozzá az anyagot.

Emellett **félreérthetően fogalmaztam** a hibamodellről: úgy hangzott, mintha nem adhatnánk
vissza saját hibát. Az ellenőrzés megerősítette, hogy adhatunk — csak az eredmény-objektumban.

---

## Amit az adverzariális ellenőrzés hozott

Az SQ-01 kifejezetten azzal a feladattal indult, hogy **döntse meg** a hibamodellről szóló
állítást. **Nem sikerült** — és az ellenőrzés közben találta meg a legerősebb bizonyítékot, a
Python SDK dokumentációjának mondatát, ami élesebb, mint az eredeti megállapítás volt.

**Ez az első kampány ebben a projektben, ahol adverzariális ellenőrzés futott.** A többi
kampány `QA.md`-je kiírja, hogy náluk nem.

Egy hatókör-pontosítás viszont kijött: a szabály a `tools/call`-ra vonatkozik, a
`resources/read`-re nem — ott nincs `isError` mező. Az eredeti állítás ezt nem mondta meg.

---

## Amit nem sikerült megerősíteni

1. **Nincs ajánlott alapérték a 403-vs-404 kérdésre egyetlen szabványban sem.** Sem RFC, sem
   OWASP Top 10, sem ASVS, sem a vonatkozó CWE-bejegyzések. **Ez nem hiány a kutatásban, hanem
   megállapítás** — és a döntésben ki kell írni, mert könnyű azt hinni, hogy van kánon.
2. **Az egyesített „nem található vagy nem hozzáférhető" üzenetnek nincs kanonikus neve.**
   Bevett gyakorlat, de névtelen.
3. **A beállíthatóságra egyetlen precedens van** (Discourse). A hét megvizsgált nagy rendszer
   közül egyik sem ad ilyen kapcsolót. Ez nem teszi rossz ötletté, de nincs mögötte iparági
   tömeg.
4. **A „csendes hiba" és a „gépi hívó" érvek** csak gyakorlói blogokban vannak kifejtve,
   szabványügyi háttér nélkül.
5. **Konkrét éles kliens forráskódja nem volt elérhető** annak ellenőrzésére, hogy a
   protokoll-hibákat a gyakorlatban továbbadják-e a modellnek. A „lehet, hogy nem jut el"
   állítás így strukturálisan bizonyított, empirikusan nem.
6. **A specifikáció nem ad tiszta ellenőrzőlistát** a token-validációhoz: csak a lejárat, a
   közönség és a hatókör explicit MUST; a kibocsátó és az aláírás ellenőrzése formátumfüggő.
7. **Egy elavult oktatóanyag** még mindig DCR-t említ CIMD nélkül a hivatalos oldalon —
   jelölve, de nem kemény ellentmondásként.

---

## Módszertani megjegyzés

Az SQ-03 ügynöke **szándékosan megkerülte a lekérő eszköz AI-összefoglalóját**: nyers Markdown
és nyers RFC-szöveg letöltésével dolgozott. Ez a korábbi kampányok visszatérő minőségi
problémájára adott válasz, és **működött** — minden idézet szó szerinti.

Az SQ-02 naplója jelöl egy esetet, ahol a lekérő eszköz **kitalált egy megkötést**. Az az
állítás nem került be.
