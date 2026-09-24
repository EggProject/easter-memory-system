# Nyers mérési kimenetek — második futás, 2026-09-22

Újraindított konténer, Bun 1.4.0, SQLite 3.53.2, Linux x86_64. A szkriptek: `bench/uzemeltetes/`.
Az első futás kimenetei a `nyers-meresek.md`-ben.

## Index-újraépítés (futtat-index.sh) — a bench lex lábának tokenizálójával (unicode61 remove_diacritics 2)
```
Bun 1.4.0 | Linux x86_64
=== 1000 fájl × 1 KB törzs ===
  hideg: {"fajl":1000,"szovegMB":1.3,"hibasFejlec":0,"osszMs":178,"fazisMs":{"bejaras":18,"olvasas":79,"parse":12,"lenyomat":9,"beszuras":42,"optimize":0},"fajlPerMp":5608,"MBperMp":7.1,"indexMB":1.8,"probaTalalat":972}
  meleg:  {"fajl":1000,"szovegMB":1.3,"hibasFejlec":0,"osszMs":66,"fazisMs":{"bejaras":2,"olvasas":7,"parse":6,"lenyomat":6,"beszuras":33,"optimize":0},"fajlPerMp":15064,"MBperMp":19.2,"indexMB":1.8,"probaTalalat":972}
  meleg:  {"fajl":1000,"szovegMB":1.3,"hibasFejlec":0,"osszMs":71,"fazisMs":{"bejaras":2,"olvasas":8,"parse":6,"lenyomat":7,"beszuras":34,"optimize":0},"fajlPerMp":14042,"MBperMp":17.9,"indexMB":1.8,"probaTalalat":972}
=== 10000 fájl × 1 KB törzs ===
  hideg: {"fajl":10000,"szovegMB":12.7,"hibasFejlec":0,"osszMs":1790,"fazisMs":{"bejaras":25,"olvasas":996,"parse":121,"lenyomat":82,"beszuras":502,"optimize":46},"fajlPerMp":5585,"MBperMp":7.1,"indexMB":21.1,"probaTalalat":9734}
  meleg:  {"fajl":10000,"szovegMB":12.7,"hibasFejlec":0,"osszMs":658,"fazisMs":{"bejaras":6,"olvasas":71,"parse":59,"lenyomat":61,"beszuras":404,"optimize":43},"fajlPerMp":15200,"MBperMp":19.3,"indexMB":21.1,"probaTalalat":9734}
  meleg:  {"fajl":10000,"szovegMB":12.7,"hibasFejlec":0,"osszMs":666,"fazisMs":{"bejaras":6,"olvasas":68,"parse":59,"lenyomat":64,"beszuras":413,"optimize":43},"fajlPerMp":15016,"MBperMp":19.1,"indexMB":21.1,"probaTalalat":9734}
=== 50000 fájl × 1 KB törzs ===
  hideg: {"fajl":50000,"szovegMB":63.7,"hibasFejlec":0,"osszMs":8106,"fazisMs":{"bejaras":52,"olvasas":4277,"parse":590,"lenyomat":382,"beszuras":2554,"optimize":194},"fajlPerMp":6168,"MBperMp":7.9,"indexMB":94.2,"probaTalalat":48580}
  meleg:  {"fajl":50000,"szovegMB":63.7,"hibasFejlec":0,"osszMs":3475,"fazisMs":{"bejaras":22,"olvasas":354,"parse":311,"lenyomat":310,"beszuras":2241,"optimize":195},"fajlPerMp":14387,"MBperMp":18.3,"indexMB":94.2,"probaTalalat":48580}
  meleg:  {"fajl":50000,"szovegMB":63.7,"hibasFejlec":0,"osszMs":3459,"fazisMs":{"bejaras":21,"olvasas":354,"parse":312,"lenyomat":311,"beszuras":2225,"optimize":192},"fajlPerMp":14455,"MBperMp":18.4,"indexMB":94.2,"probaTalalat":48580}
=== 1000 fájl × 4 KB törzs ===
  hideg: {"fajl":1000,"szovegMB":4.7,"hibasFejlec":0,"osszMs":302,"fazisMs":{"bejaras":17,"olvasas":107,"parse":13,"lenyomat":21,"beszuras":128,"optimize":0},"fajlPerMp":3312,"MBperMp":15.6,"indexMB":5.6,"probaTalalat":1000}
  meleg:  {"fajl":1000,"szovegMB":4.7,"hibasFejlec":0,"osszMs":170,"fazisMs":{"bejaras":2,"olvasas":14,"parse":8,"lenyomat":20,"beszuras":120,"optimize":0},"fajlPerMp":5874,"MBperMp":27.7,"indexMB":5.6,"probaTalalat":1000}
  meleg:  {"fajl":1000,"szovegMB":4.7,"hibasFejlec":0,"osszMs":166,"fazisMs":{"bejaras":2,"olvasas":13,"parse":7,"lenyomat":19,"beszuras":118,"optimize":0},"fajlPerMp":6042,"MBperMp":28.4,"indexMB":5.6,"probaTalalat":1000}
=== 10000 fájl × 4 KB törzs ===
  hideg: {"fajl":10000,"szovegMB":47.1,"hibasFejlec":0,"osszMs":2806,"fazisMs":{"bejaras":47,"olvasas":1052,"parse":128,"lenyomat":209,"beszuras":1277,"optimize":70},"fajlPerMp":3564,"MBperMp":16.8,"indexMB":59.7,"probaTalalat":10000}
  meleg:  {"fajl":10000,"szovegMB":47.1,"hibasFejlec":0,"osszMs":1636,"fazisMs":{"bejaras":10,"olvasas":119,"parse":68,"lenyomat":190,"beszuras":1165,"optimize":67},"fajlPerMp":6111,"MBperMp":28.8,"indexMB":59.7,"probaTalalat":10000}
  meleg:  {"fajl":10000,"szovegMB":47.1,"hibasFejlec":0,"osszMs":1619,"fazisMs":{"bejaras":10,"olvasas":117,"parse":70,"lenyomat":187,"beszuras":1147,"optimize":71},"fajlPerMp":6177,"MBperMp":29.1,"indexMB":59.7,"probaTalalat":10000}
=== 50000 fájl × 4 KB törzs ===
  hideg: {"fajl":50000,"szovegMB":235.5,"hibasFejlec":0,"osszMs":13756,"fazisMs":{"bejaras":65,"olvasas":5009,"parse":638,"lenyomat":1026,"beszuras":6626,"optimize":302},"fajlPerMp":3635,"MBperMp":17.1,"indexMB":285.5,"probaTalalat":50000}
  meleg:  {"fajl":50000,"szovegMB":235.5,"hibasFejlec":0,"osszMs":8720,"fazisMs":{"bejaras":22,"olvasas":612,"parse":405,"lenyomat":956,"beszuras":6244,"optimize":412},"fajlPerMp":5734,"MBperMp":27,"indexMB":285.5,"probaTalalat":50000}
  meleg:  {"fajl":50000,"szovegMB":235.5,"hibasFejlec":0,"osszMs":8906,"fazisMs":{"bejaras":22,"olvasas":607,"parse":416,"lenyomat":972,"beszuras":6502,"optimize":320},"fajlPerMp":5614,"MBperMp":26.4,"indexMB":285.5,"probaTalalat":50000}
```

## Index-újraépítés — kontrollfutás az alapértelmezett unicode61 tokenizálóval
```
Bun 1.4.0 | Linux x86_64
=== 1000 fájl × 1 KB törzs ===
  hideg: {"fajl":1000,"szovegMB":1.3,"hibasFejlec":0,"osszMs":211,"fazisMs":{"bejaras":21,"olvasas":93,"parse":15,"lenyomat":11,"beszuras":52,"optimize":0},"fajlPerMp":4732,"MBperMp":6,"indexMB":1.8,"probaTalalat":977}
  meleg:  {"fajl":1000,"szovegMB":1.3,"hibasFejlec":0,"osszMs":63,"fazisMs":{"bejaras":2,"olvasas":7,"parse":6,"lenyomat":6,"beszuras":32,"optimize":0},"fajlPerMp":15834,"MBperMp":20.1,"indexMB":1.8,"probaTalalat":977}
  meleg:  {"fajl":1000,"szovegMB":1.3,"hibasFejlec":0,"osszMs":64,"fazisMs":{"bejaras":2,"olvasas":6,"parse":6,"lenyomat":6,"beszuras":32,"optimize":0},"fajlPerMp":15666,"MBperMp":19.9,"indexMB":1.8,"probaTalalat":977}
=== 10000 fájl × 1 KB törzs ===
  hideg: {"fajl":10000,"szovegMB":12.7,"hibasFejlec":0,"osszMs":1720,"fazisMs":{"bejaras":20,"olvasas":946,"parse":122,"lenyomat":84,"beszuras":485,"optimize":40},"fajlPerMp":5814,"MBperMp":7.4,"indexMB":21.1,"probaTalalat":9715}
  meleg:  {"fajl":10000,"szovegMB":12.7,"hibasFejlec":0,"osszMs":633,"fazisMs":{"bejaras":6,"olvasas":68,"parse":55,"lenyomat":59,"beszuras":388,"optimize":46},"fajlPerMp":15800,"MBperMp":20.1,"indexMB":21.1,"probaTalalat":9715}
  meleg:  {"fajl":10000,"szovegMB":12.7,"hibasFejlec":0,"osszMs":663,"fazisMs":{"bejaras":6,"olvasas":70,"parse":60,"lenyomat":76,"beszuras":395,"optimize":45},"fajlPerMp":15081,"MBperMp":19.2,"indexMB":21.1,"probaTalalat":9715}
=== 50000 fájl × 1 KB törzs ===
  hideg: {"fajl":50000,"szovegMB":63.7,"hibasFejlec":0,"osszMs":8133,"fazisMs":{"bejaras":49,"olvasas":4237,"parse":592,"lenyomat":391,"beszuras":2602,"optimize":202},"fajlPerMp":6148,"MBperMp":7.8,"indexMB":94.2,"probaTalalat":48613}
  meleg:  {"fajl":50000,"szovegMB":63.7,"hibasFejlec":0,"osszMs":3523,"fazisMs":{"bejaras":22,"olvasas":368,"parse":298,"lenyomat":321,"beszuras":2272,"optimize":201},"fajlPerMp":14192,"MBperMp":18.1,"indexMB":94.2,"probaTalalat":48613}
  meleg:  {"fajl":50000,"szovegMB":63.7,"hibasFejlec":0,"osszMs":3466,"fazisMs":{"bejaras":25,"olvasas":339,"parse":298,"lenyomat":306,"beszuras":2250,"optimize":207},"fajlPerMp":14426,"MBperMp":18.4,"indexMB":94.2,"probaTalalat":48613}
=== 1000 fájl × 4 KB törzs ===
  hideg: {"fajl":1000,"szovegMB":4.7,"hibasFejlec":0,"osszMs":323,"fazisMs":{"bejaras":16,"olvasas":125,"parse":14,"lenyomat":23,"beszuras":132,"optimize":0},"fajlPerMp":3093,"MBperMp":14.6,"indexMB":5.6,"probaTalalat":1000}
  meleg:  {"fajl":1000,"szovegMB":4.7,"hibasFejlec":0,"osszMs":203,"fazisMs":{"bejaras":2,"olvasas":18,"parse":11,"lenyomat":23,"beszuras":143,"optimize":0},"fajlPerMp":4923,"MBperMp":23.2,"indexMB":5.6,"probaTalalat":1000}
  meleg:  {"fajl":1000,"szovegMB":4.7,"hibasFejlec":0,"osszMs":163,"fazisMs":{"bejaras":2,"olvasas":13,"parse":8,"lenyomat":19,"beszuras":116,"optimize":0},"fajlPerMp":6130,"MBperMp":28.9,"indexMB":5.6,"probaTalalat":1000}
=== 10000 fájl × 4 KB törzs ===
  hideg: {"fajl":10000,"szovegMB":47.1,"hibasFejlec":0,"osszMs":2771,"fazisMs":{"bejaras":26,"olvasas":1069,"parse":134,"lenyomat":218,"beszuras":1239,"optimize":60},"fajlPerMp":3609,"MBperMp":17,"indexMB":59.7,"probaTalalat":10000}
  meleg:  {"fajl":10000,"szovegMB":47.1,"hibasFejlec":0,"osszMs":1528,"fazisMs":{"bejaras":6,"olvasas":113,"parse":63,"lenyomat":179,"beszuras":1088,"optimize":63},"fajlPerMp":6544,"MBperMp":30.8,"indexMB":59.7,"probaTalalat":10000}
  meleg:  {"fajl":10000,"szovegMB":47.1,"hibasFejlec":0,"osszMs":1716,"fazisMs":{"bejaras":10,"olvasas":126,"parse":77,"lenyomat":205,"beszuras":1214,"optimize":65},"fajlPerMp":5829,"MBperMp":27.4,"indexMB":59.7,"probaTalalat":10000}
=== 50000 fájl × 4 KB törzs ===
  hideg: {"fajl":50000,"szovegMB":235.5,"hibasFejlec":0,"osszMs":13713,"fazisMs":{"bejaras":53,"olvasas":5084,"parse":623,"lenyomat":1014,"beszuras":6554,"optimize":306},"fajlPerMp":3646,"MBperMp":17.2,"indexMB":285.5,"probaTalalat":50000}
  meleg:  {"fajl":50000,"szovegMB":235.5,"hibasFejlec":0,"osszMs":8372,"fazisMs":{"bejaras":21,"olvasas":587,"parse":358,"lenyomat":939,"beszuras":6085,"optimize":320},"fajlPerMp":5972,"MBperMp":28.1,"indexMB":285.5,"probaTalalat":50000}
  meleg:  {"fajl":50000,"szovegMB":235.5,"hibasFejlec":0,"osszMs":8430,"fazisMs":{"bejaras":23,"olvasas":565,"parse":385,"lenyomat":932,"beszuras":6116,"optimize":342},"fajlPerMp":5931,"MBperMp":27.9,"indexMB":285.5,"probaTalalat":50000}
```

## VACUUM INTO / integritás méret szerint (futtat-meret.sh)
```
Bun 1.4.0 | Linux x86_64
=== 50 MB cél — {"bejegyzes":5600,"byte":46485504} ===
  olvas              hideg: {"mod":"olvas","ms":26,"byte":46489600}
  olvas              meleg: {"mod":"olvas","ms":25,"byte":46489600}
  olvas              meleg: {"mod":"olvas","ms":22,"byte":46489600}
  olvas              meleg: {"mod":"olvas","ms":21,"byte":46489600}
  copy               hideg: {"mod":"copy","ms":21,"kimenetByte":46489600}
  copy               meleg: {"mod":"copy","ms":13,"kimenetByte":46489600}
  copy               meleg: {"mod":"copy","ms":13,"kimenetByte":46489600}
  copy               meleg: {"mod":"copy","ms":13,"kimenetByte":46489600}
  vacuum             hideg: {"mod":"vacuum","ms":138,"kimenetByte":46460928}
  vacuum             meleg: {"mod":"vacuum","ms":114,"kimenetByte":46460928}
  vacuum             meleg: {"mod":"vacuum","ms":120,"kimenetByte":46460928}
  vacuum             meleg: {"mod":"vacuum","ms":122,"kimenetByte":46460928}
  quick_check        hideg: {"mod":"quick_check","ms":720,"sorok":1,"elso":"{\"quick_check\":\"ok\"}"}
  quick_check        meleg: {"mod":"quick_check","ms":27,"sorok":1,"elso":"{\"quick_check\":\"ok\"}"}
  quick_check        meleg: {"mod":"quick_check","ms":27,"sorok":1,"elso":"{\"quick_check\":\"ok\"}"}
  quick_check        meleg: {"mod":"quick_check","ms":26,"sorok":1,"elso":"{\"quick_check\":\"ok\"}"}
  integrity_check    hideg: {"mod":"integrity_check","ms":617,"sorok":1,"elso":"{\"integrity_check\":\"ok\"}"}
  integrity_check    meleg: {"mod":"integrity_check","ms":30,"sorok":1,"elso":"{\"integrity_check\":\"ok\"}"}
  integrity_check    meleg: {"mod":"integrity_check","ms":30,"sorok":1,"elso":"{\"integrity_check\":\"ok\"}"}
  integrity_check    meleg: {"mod":"integrity_check","ms":30,"sorok":1,"elso":"{\"integrity_check\":\"ok\"}"}
  foreign_key_check  hideg: {"mod":"foreign_key_check","ms":19,"sorok":0,"elso":"null"}
  foreign_key_check  meleg: {"mod":"foreign_key_check","ms":12,"sorok":0,"elso":"null"}
  foreign_key_check  meleg: {"mod":"foreign_key_check","ms":12,"sorok":0,"elso":"null"}
  foreign_key_check  meleg: {"mod":"foreign_key_check","ms":12,"sorok":0,"elso":"null"}
  -- fordított sorrend, hidegen --
  integrity_check hideg: {"mod":"integrity_check","ms":697,"sorok":1,"elso":"{\"integrity_check\":\"ok\"}"}
  quick_check     hideg: {"mod":"quick_check","ms":637,"sorok":1,"elso":"{\"quick_check\":\"ok\"}"}
=== 200 MB cél — {"bejegyzes":24800,"byte":205881344} ===
  olvas              hideg: {"mod":"olvas","ms":108,"byte":205885440}
  olvas              meleg: {"mod":"olvas","ms":99,"byte":205885440}
  olvas              meleg: {"mod":"olvas","ms":99,"byte":205885440}
  olvas              meleg: {"mod":"olvas","ms":105,"byte":205885440}
  copy               hideg: {"mod":"copy","ms":82,"kimenetByte":205885440}
  copy               meleg: {"mod":"copy","ms":66,"kimenetByte":205885440}
  copy               meleg: {"mod":"copy","ms":63,"kimenetByte":205885440}
  copy               meleg: {"mod":"copy","ms":65,"kimenetByte":205885440}
  vacuum             hideg: {"mod":"vacuum","ms":556,"kimenetByte":205737984}
  vacuum             meleg: {"mod":"vacuum","ms":471,"kimenetByte":205737984}
  vacuum             meleg: {"mod":"vacuum","ms":490,"kimenetByte":205737984}
  vacuum             meleg: {"mod":"vacuum","ms":543,"kimenetByte":205737984}
  quick_check        hideg: {"mod":"quick_check","ms":3006,"sorok":1,"elso":"{\"quick_check\":\"ok\"}"}
  quick_check        meleg: {"mod":"quick_check","ms":108,"sorok":1,"elso":"{\"quick_check\":\"ok\"}"}
  quick_check        meleg: {"mod":"quick_check","ms":103,"sorok":1,"elso":"{\"quick_check\":\"ok\"}"}
  quick_check        meleg: {"mod":"quick_check","ms":104,"sorok":1,"elso":"{\"quick_check\":\"ok\"}"}
  integrity_check    hideg: {"mod":"integrity_check","ms":2904,"sorok":1,"elso":"{\"integrity_check\":\"ok\"}"}
  integrity_check    meleg: {"mod":"integrity_check","ms":136,"sorok":1,"elso":"{\"integrity_check\":\"ok\"}"}
  integrity_check    meleg: {"mod":"integrity_check","ms":129,"sorok":1,"elso":"{\"integrity_check\":\"ok\"}"}
  integrity_check    meleg: {"mod":"integrity_check","ms":137,"sorok":1,"elso":"{\"integrity_check\":\"ok\"}"}
  foreign_key_check  hideg: {"mod":"foreign_key_check","ms":97,"sorok":0,"elso":"null"}
  foreign_key_check  meleg: {"mod":"foreign_key_check","ms":43,"sorok":0,"elso":"null"}
  foreign_key_check  meleg: {"mod":"foreign_key_check","ms":43,"sorok":0,"elso":"null"}
  foreign_key_check  meleg: {"mod":"foreign_key_check","ms":41,"sorok":0,"elso":"null"}
  -- fordított sorrend, hidegen --
  integrity_check hideg: {"mod":"integrity_check","ms":2938,"sorok":1,"elso":"{\"integrity_check\":\"ok\"}"}
  quick_check     hideg: {"mod":"quick_check","ms":2937,"sorok":1,"elso":"{\"quick_check\":\"ok\"}"}
=== 1000 MB cél — {"bejegyzes":125600,"byte":1043148800} ===
  olvas              hideg: {"mod":"olvas","ms":522,"byte":1043152896}
  olvas              meleg: {"mod":"olvas","ms":462,"byte":1043152896}
  olvas              meleg: {"mod":"olvas","ms":471,"byte":1043152896}
  olvas              meleg: {"mod":"olvas","ms":498,"byte":1043152896}
  copy               hideg: {"mod":"copy","ms":422,"kimenetByte":1043152896}
  copy               meleg: {"mod":"copy","ms":322,"kimenetByte":1043152896}
  copy               meleg: {"mod":"copy","ms":739,"kimenetByte":1043152896}
  copy               meleg: {"mod":"copy","ms":399,"kimenetByte":1043152896}
  vacuum             hideg: {"mod":"vacuum","ms":2245,"kimenetByte":1042354176}
  vacuum             meleg: {"mod":"vacuum","ms":2318,"kimenetByte":1042354176}
  vacuum             meleg: {"mod":"vacuum","ms":2185,"kimenetByte":1042354176}
  vacuum             meleg: {"mod":"vacuum","ms":1941,"kimenetByte":1042354176}
  quick_check        hideg: {"mod":"quick_check","ms":14442,"sorok":1,"elso":"{\"quick_check\":\"ok\"}"}
  quick_check        meleg: {"mod":"quick_check","ms":508,"sorok":1,"elso":"{\"quick_check\":\"ok\"}"}
  quick_check        meleg: {"mod":"quick_check","ms":506,"sorok":1,"elso":"{\"quick_check\":\"ok\"}"}
  quick_check        meleg: {"mod":"quick_check","ms":514,"sorok":1,"elso":"{\"quick_check\":\"ok\"}"}
  integrity_check    hideg: {"mod":"integrity_check","ms":14704,"sorok":1,"elso":"{\"integrity_check\":\"ok\"}"}
  integrity_check    meleg: {"mod":"integrity_check","ms":672,"sorok":1,"elso":"{\"integrity_check\":\"ok\"}"}
  integrity_check    meleg: {"mod":"integrity_check","ms":666,"sorok":1,"elso":"{\"integrity_check\":\"ok\"}"}
  integrity_check    meleg: {"mod":"integrity_check","ms":663,"sorok":1,"elso":"{\"integrity_check\":\"ok\"}"}
  foreign_key_check  hideg: {"mod":"foreign_key_check","ms":444,"sorok":0,"elso":"null"}
  foreign_key_check  meleg: {"mod":"foreign_key_check","ms":238,"sorok":0,"elso":"null"}
  foreign_key_check  meleg: {"mod":"foreign_key_check","ms":272,"sorok":0,"elso":"null"}
  foreign_key_check  meleg: {"mod":"foreign_key_check","ms":235,"sorok":0,"elso":"null"}
  -- fordított sorrend, hidegen --
  integrity_check hideg: {"mod":"integrity_check","ms":15083,"sorok":1,"elso":"{\"integrity_check\":\"ok\"}"}
  quick_check     hideg: {"mod":"quick_check","ms":14866,"sorok":1,"elso":"{\"quick_check\":\"ok\"}"}
```

## WAL kontrollos kísérlet (wal-kontroll.ts)
```
Bun 1.4.0
futás            ablak  | WAL előtte | WAL alatta | WAL utána | író aránya | író-hiba
KONTROLL #1   1300 ms |     4.0 MB |     4.0 MB |    4.0 MB |    105%    | 0
KONTROLL #2   1300 ms |     4.0 MB |     4.0 MB |    4.0 MB |    104%    | 0
KONTROLL #3   1300 ms |     4.0 MB |     4.0 MB |    4.0 MB |     81%    | 0
KÍSÉRLET #1    957 ms |     4.0 MB |   312.5 MB |  312.5 MB |    166%    | 0
KÍSÉRLET #2    943 ms |     4.0 MB |   360.7 MB |  360.7 MB |    172%    | 0
KÍSÉRLET #3   1075 ms |     4.0 MB |   392.5 MB |  392.5 MB |    144%    | 0
```

## WAL visszanyerése (wal-visszanyeres.ts)
```
Bun 1.4.0
WAL írás közben, mentés előtt:              4.1 MB
VACUUM INTO:                                741 ms
WAL közvetlenül a mentés után:              95.6 MB
WAL 2 mp tétlenség után (kapcsolat nyitva): 95.6 MB
wal_checkpoint(PASSIVE)  → [{"busy":0,"log":24330,"checkpointed":24330}]  WAL: 95.6 MB
wal_checkpoint(TRUNCATE) → [{"busy":0,"log":0,"checkpointed":0}]  WAL: 0.0 MB
WAL az író leállítása után:                 0.0 MB
```

## Pillanatkép-határ (pillanatkep.ts)
```
Bun 1.4.0
az író a VACUUM INTO indulásakor ~712825, a végén ~945975 sornál tartott (400 ms-os mintavétel)
a mentésben 757550 konkurens sor van → az INDULÁSI állapot
író-hiba: 0 · integrity_check a mentésen: [{"integrity_check":"ok"}]
```

## Ékezetek a unicode61 tokenizálóban (ekezet-teszt.ts)
```
SQLite 3.53.2 | Bun 1.4.0

== alapértelmezett ==
  őrző    → őrző kutya
  orzo    → őrző kutya
  örző    → őrző kutya
  kötő    → kötő tű
  koto    → kötő tű
  fűzfa   → fűzfa ág
  fuzfa   → fűzfa ág
  hűtő    → hűtő
  huto    → hűtő
  kör     → kör alakú | kor szerint
  kor     → kör alakú | kor szerint
  tör     → tör eszköz
  tor     → tör eszköz
  ház     → ház kulcs
  haz     → ház kulcs

== remove_diacritics 0 ==
  őrző    → őrző kutya
  orzo    → —
  örző    → —
  kötő    → kötő tű
  koto    → —
  fűzfa   → fűzfa ág
  fuzfa   → —
  hűtő    → hűtő
  huto    → —
  kör     → kör alakú
  kor     → kor szerint
  tör     → tör eszköz
  tor     → —
  ház     → ház kulcs
  haz     → —

== remove_diacritics 1 ==
  őrző    → őrző kutya
  orzo    → őrző kutya
  örző    → őrző kutya
  kötő    → kötő tű
  koto    → kötő tű
  fűzfa   → fűzfa ág
  fuzfa   → fűzfa ág
  hűtő    → hűtő
  huto    → hűtő
  kör     → kör alakú | kor szerint
  kor     → kör alakú | kor szerint
  tör     → tör eszköz
  tor     → tör eszköz
  ház     → ház kulcs
  haz     → ház kulcs

== remove_diacritics 2 ==
  őrző    → őrző kutya
  orzo    → őrző kutya
  örző    → őrző kutya
  kötő    → kötő tű
  koto    → kötő tű
  fűzfa   → fűzfa ág
  fuzfa   → fűzfa ág
  hűtő    → hűtő
  huto    → hűtő
  kör     → kör alakú | kor szerint
  kor     → kör alakú | kor szerint
  tör     → tör eszköz
  tor     → tör eszköz
  ház     → ház kulcs
  haz     → ház kulcs
```

## hibaesetek.ts · torolt-tartalom.ts · fts5-szerkezet.ts
```
Bun 1.4.0
létező célfájlra           HIBA — output file already exists
nem létező könyvtárba      HIBA — unable to open database: /home/claude/work/bench-uzem/adat/nincs/ilyen/x.sqlite
nyitott tranzakcióban      HIBA — cannot VACUUM from within a transaction
journal_mode    forrás: wal      mentés: delete   NEM öröklődik
page_size       forrás: 8192     mentés: 8192     öröklődik
auto_vacuum     forrás: 2        mentés: 2        öröklődik
user_version    forrás: 7        mentés: 7        öröklődik
application_id  forrás: 424242   mentés: 424242   öröklődik

Bun 1.4.0
forrás a törlés előtt:        MEGVAN
forrás a törlés után:         MEGVAN
nyers fájlmásolat (cp):       MEGVAN
VACUUM INTO kimenet:          NINCS

SQLite verzió: 3.53.2 | Bun 1.4.0
1) ALTER TABLE bej_fts ADD COLUMN cimke                       HIBA — virtual tables may not be altered
2) ALTER TABLE bej_fts DROP COLUMN torzs                      HIBA — cannot drop column from virtual table "bej_fts"
3) ALTER TABLE bej_fts RENAME COLUMN cim TO fejlec            HIBA — cannot rename columns of virtual table "bej_fts"
4) ALTER TABLE bej_fts RENAME TO bej_fts2                     SIKERÜLT
5) ALTER TABLE bej_fts SET tokenize='trigram'                 HIBA — near "SET": syntax error
6) INSERT INTO bej_fts(bej_fts) VALUES('rebuild')             SIKERÜLT
   INSERT INTO bej_fts(bej_fts) VALUES('integrity-check')     SIKERÜLT
7) CREATE VIRTUAL TABLE bej_fts USING fts5(cim, torzs, content='bejegyzes', content_rowid='id', tokenize='trigram') SIKERÜLT
   rebuild után részszó-találat ('szerz'): 100 sor
8) trigger után, rebuild ELŐTT: 0 találat
   rebuild UTÁN:                50 találat
```
