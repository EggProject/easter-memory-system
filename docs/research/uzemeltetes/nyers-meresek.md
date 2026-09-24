# Nyers mérési kimenetek — uzemeltetes kampány

Bun 1.4.0 / SQLite 3.53.2 / Linux 6.18 konténer.

## FTS5 szerkezeti teszt (fts5-teszt.ts)
```
SQLite verzio: 3.53.2
Bun: 1.4.0

=== 1) VACUUM INTO idoigeny meret szerint (toredezetlen adatbazis) ===
meret(MB) | bejegyzes | VACUUM INTO (ms) | fajlmasolas (ms) | kimenet(MB) | MB/s
      6.4 |       800 |               18 |               28 |         6.4 | 358
     44.4 |      5600 |              111 |              129 |        44.3 | 399
    196.4 |     24800 |              569 |              184 |       196.0 | 345
    995.1 |    125600 |             2306 |              346 |       993.0 | 431

=== 2) Toredezettseg hatasa (200 MB, 30% torles utan) ===
  forras torles ELOTT:        196.4 MB
  forras torles UTAN:         196.4 MB   (a fajl nem zsugorodik)
  VACUUM INTO kimenet:        137.2 MB   (30.1%-kal kisebb)
  VACUUM INTO ido:            473 ms

=== 3) Torolt tartalom a mentesben — nyomolvashatosag ===
  a jelolo a forrasban a torles elott: MEGVAN
  a jelolo a forrasban a torles UTAN: MEGVAN (a lap nincs felulirva)
  fajlmasolat (cp):                   MEGVAN — a torolt tartalom atkerult
  VACUUM INTO kimenet:                NINCS — a torolt tartalom nem kerult at

=== 4) VACUUM INTO konkurens iro mellett (200 MB) ===
  VACUUM INTO iro NELKUL:     739 ms
  VACUUM INTO iro KOZBEN:     669 ms   (0.91x)
  a mentes merete:            215.3 MB
  sorok a mentesben:          34480 (ebbol konkurensen beszurt: 9680)
  integrity_check a mentesen: [{"integrity_check":"ok"}]

kesz.
```

## VACUUM INTO / integritás-ellenőrzés méret szerint (futtat.sh)
```
Lapgyorsitotar: 483304 kB -> urites -> 155508 kB

=== 50 MB cel — {"bejegyzes":5600,"byte":46473216} ===
  olvas              hideg: {"mod":"olvas","ms":35,"byte":46477312}
  olvas              meleg: {"mod":"olvas","ms":24,"byte":46477312}
  olvas              meleg: {"mod":"olvas","ms":30,"byte":46477312}
  olvas              meleg: {"mod":"olvas","ms":27,"byte":46477312}
  copy               hideg: {"mod":"copy","ms":29,"kimenetByte":46477312}
  copy               meleg: {"mod":"copy","ms":16,"kimenetByte":46477312}
  copy               meleg: {"mod":"copy","ms":14,"kimenetByte":46477312}
  copy               meleg: {"mod":"copy","ms":14,"kimenetByte":46477312}
  vacuum             hideg: {"mod":"vacuum","ms":124,"kimenetByte":46448640}
  vacuum             meleg: {"mod":"vacuum","ms":108,"kimenetByte":46448640}
  vacuum             meleg: {"mod":"vacuum","ms":106,"kimenetByte":46448640}
  vacuum             meleg: {"mod":"vacuum","ms":111,"kimenetByte":46448640}
  quick_check        hideg: {"mod":"quick_check","ms":704,"sorok":1,"elso":"{\"quick_check\":\"ok\"}"}
  quick_check        meleg: {"mod":"quick_check","ms":29,"sorok":1,"elso":"{\"quick_check\":\"ok\"}"}
  quick_check        meleg: {"mod":"quick_check","ms":29,"sorok":1,"elso":"{\"quick_check\":\"ok\"}"}
  quick_check        meleg: {"mod":"quick_check","ms":29,"sorok":1,"elso":"{\"quick_check\":\"ok\"}"}
  integrity_check    hideg: {"mod":"integrity_check","ms":681,"sorok":1,"elso":"{\"integrity_check\":\"ok\"}"}
  integrity_check    meleg: {"mod":"integrity_check","ms":36,"sorok":1,"elso":"{\"integrity_check\":\"ok\"}"}
  integrity_check    meleg: {"mod":"integrity_check","ms":35,"sorok":1,"elso":"{\"integrity_check\":\"ok\"}"}
  integrity_check    meleg: {"mod":"integrity_check","ms":36,"sorok":1,"elso":"{\"integrity_check\":\"ok\"}"}
  foreign_key_check  hideg: {"mod":"foreign_key_check","ms":20,"sorok":0,"elso":"null"}
  foreign_key_check  meleg: {"mod":"foreign_key_check","ms":11,"sorok":0,"elso":"null"}
  foreign_key_check  meleg: {"mod":"foreign_key_check","ms":11,"sorok":0,"elso":"null"}
  foreign_key_check  meleg: {"mod":"foreign_key_check","ms":11,"sorok":0,"elso":"null"}
  -- forditott sorrend, hidegen (sorrendhatas kizarasa) --
  integrity_check    hideg: {"mod":"integrity_check","ms":710,"sorok":1,"elso":"{\"integrity_check\":\"ok\"}"}
  quick_check        hideg: {"mod":"quick_check","ms":665,"sorok":1,"elso":"{\"quick_check\":\"ok\"}"}

=== 200 MB cel — {"bejegyzes":24800,"byte":205807616} ===
  olvas              hideg: {"mod":"olvas","ms":94,"byte":205811712}
  olvas              meleg: {"mod":"olvas","ms":86,"byte":205811712}
  olvas              meleg: {"mod":"olvas","ms":91,"byte":205811712}
  olvas              meleg: {"mod":"olvas","ms":101,"byte":205811712}
  copy               hideg: {"mod":"copy","ms":104,"kimenetByte":205811712}
  copy               meleg: {"mod":"copy","ms":67,"kimenetByte":205811712}
  copy               meleg: {"mod":"copy","ms":55,"kimenetByte":205811712}
  copy               meleg: {"mod":"copy","ms":54,"kimenetByte":205811712}
  vacuum             hideg: {"mod":"vacuum","ms":464,"kimenetByte":205664256}
  vacuum             meleg: {"mod":"vacuum","ms":443,"kimenetByte":205664256}
  vacuum             meleg: {"mod":"vacuum","ms":446,"kimenetByte":205664256}
  vacuum             meleg: {"mod":"vacuum","ms":481,"kimenetByte":205664256}
  quick_check        hideg: {"mod":"quick_check","ms":2891,"sorok":1,"elso":"{\"quick_check\":\"ok\"}"}
  quick_check        meleg: {"mod":"quick_check","ms":114,"sorok":1,"elso":"{\"quick_check\":\"ok\"}"}
  quick_check        meleg: {"mod":"quick_check","ms":104,"sorok":1,"elso":"{\"quick_check\":\"ok\"}"}
  quick_check        meleg: {"mod":"quick_check","ms":104,"sorok":1,"elso":"{\"quick_check\":\"ok\"}"}
  integrity_check    hideg: {"mod":"integrity_check","ms":3039,"sorok":1,"elso":"{\"integrity_check\":\"ok\"}"}
  integrity_check    meleg: {"mod":"integrity_check","ms":140,"sorok":1,"elso":"{\"integrity_check\":\"ok\"}"}
  integrity_check    meleg: {"mod":"integrity_check","ms":135,"sorok":1,"elso":"{\"integrity_check\":\"ok\"}"}
  integrity_check    meleg: {"mod":"integrity_check","ms":133,"sorok":1,"elso":"{\"integrity_check\":\"ok\"}"}
  foreign_key_check  hideg: {"mod":"foreign_key_check","ms":103,"sorok":0,"elso":"null"}
  foreign_key_check  meleg: {"mod":"foreign_key_check","ms":46,"sorok":0,"elso":"null"}
  foreign_key_check  meleg: {"mod":"foreign_key_check","ms":50,"sorok":0,"elso":"null"}
  foreign_key_check  meleg: {"mod":"foreign_key_check","ms":43,"sorok":0,"elso":"null"}
  -- forditott sorrend, hidegen (sorrendhatas kizarasa) --
  integrity_check    hideg: {"mod":"integrity_check","ms":2934,"sorok":1,"elso":"{\"integrity_check\":\"ok\"}"}
  quick_check        hideg: {"mod":"quick_check","ms":2758,"sorok":1,"elso":"{\"quick_check\":\"ok\"}"}

=== 1000 MB cel — {"bejegyzes":125600,"byte":1043062784} ===
  olvas              hideg: {"mod":"olvas","ms":733,"byte":1043066880}
  olvas              meleg: {"mod":"olvas","ms":436,"byte":1043066880}
  olvas              meleg: {"mod":"olvas","ms":426,"byte":1043066880}
  olvas              meleg: {"mod":"olvas","ms":496,"byte":1043066880}
  copy               hideg: {"mod":"copy","ms":658,"kimenetByte":1043066880}
  copy               meleg: {"mod":"copy","ms":362,"kimenetByte":1043066880}
  copy               meleg: {"mod":"copy","ms":361,"kimenetByte":1043066880}
  copy               meleg: {"mod":"copy","ms":366,"kimenetByte":1043066880}
  vacuum             hideg: {"mod":"vacuum","ms":2342,"kimenetByte":1042268160}
  vacuum             meleg: {"mod":"vacuum","ms":2538,"kimenetByte":1042268160}
  vacuum             meleg: {"mod":"vacuum","ms":2319,"kimenetByte":1042268160}
  vacuum             meleg: {"mod":"vacuum","ms":2393,"kimenetByte":1042268160}
  quick_check        hideg: {"mod":"quick_check","ms":14540,"sorok":1,"elso":"{\"quick_check\":\"ok\"}"}
  quick_check        meleg: {"mod":"quick_check","ms":526,"sorok":1,"elso":"{\"quick_check\":\"ok\"}"}
  quick_check        meleg: {"mod":"quick_check","ms":509,"sorok":1,"elso":"{\"quick_check\":\"ok\"}"}
  quick_check        meleg: {"mod":"quick_check","ms":593,"sorok":1,"elso":"{\"quick_check\":\"ok\"}"}
  integrity_check    hideg: {"mod":"integrity_check","ms":14031,"sorok":1,"elso":"{\"integrity_check\":\"ok\"}"}
  integrity_check    meleg: {"mod":"integrity_check","ms":671,"sorok":1,"elso":"{\"integrity_check\":\"ok\"}"}
  integrity_check    meleg: {"mod":"integrity_check","ms":677,"sorok":1,"elso":"{\"integrity_check\":\"ok\"}"}
  integrity_check    meleg: {"mod":"integrity_check","ms":665,"sorok":1,"elso":"{\"integrity_check\":\"ok\"}"}
  foreign_key_check  hideg: {"mod":"foreign_key_check","ms":618,"sorok":0,"elso":"null"}
  foreign_key_check  meleg: {"mod":"foreign_key_check","ms":205,"sorok":0,"elso":"null"}
  foreign_key_check  meleg: {"mod":"foreign_key_check","ms":228,"sorok":0,"elso":"null"}
  foreign_key_check  meleg: {"mod":"foreign_key_check","ms":222,"sorok":0,"elso":"null"}
  -- forditott sorrend, hidegen (sorrendhatas kizarasa) --
  integrity_check    hideg: {"mod":"integrity_check","ms":15103,"sorok":1,"elso":"{\"integrity_check\":\"ok\"}"}
  quick_check        hideg: {"mod":"quick_check","ms":13476,"sorok":1,"elso":"{\"quick_check\":\"ok\"}"}

kesz.
```

## Konkurencia és pillanatkép-határ (konkurens.ts)
```
alap: 196.2 MB
VACUUM INTO: 1346 ms, kimenet 425.5 MB
iro atbocsatas ELOTTE:  137717 sor/mp
iro atbocsatas KOZBEN:  219604 sor/mp  (159%)
iro atbocsatas UTANA:   142475 sor/mp
SQLITE_BUSY / egyeb iro-hiba: 0

pillanatkep: a VACUUM inditasakor az iro ~767750 sornal tartott, a vegen ~1085375-nel.
             a mentesben 816250 konkurens sor van.
             -> az INDULASI allapot kerult a mentesbe
integrity_check a mentesen: [{"integrity_check":"ok"}]
```
