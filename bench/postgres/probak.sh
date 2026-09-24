#!/bin/bash
# Postgres-próbák a ParadeDB-re váltáshoz (D-43). Sima Postgres + pgvector kell hozzá (a ParadeDB-specifikus
# részek itt nem próbálhatók ki). Használat: PGBIN=/usr/lib/postgresql/16/bin ./probak.sh   (rootként: postgres userrel indít)
set -u
PGBIN=${PGBIN:-/usr/lib/postgresql/16/bin}
D=$(cd "$(dirname "$0")" && pwd)/adat; rm -rf "$D"; mkdir -p "$D"; chown postgres "$D" 2>/dev/null || true
PORT=5497; JEL="TITKOS-JELSZO-QX7R2M-EZ-TOROLVE-LESZ"
start() { su postgres -c "$PGBIN/initdb -D $D/$1 -A trust -U postgres $2 >/dev/null" && su postgres -c "$PGBIN/pg_ctl -D $D/$1 -o '-p $PORT -k /tmp' -l $D/$1.log start >/dev/null"; sleep 2; }
stop()  { su postgres -c "$PGBIN/pg_ctl -D $D/$1 stop -m fast >/dev/null"; }
P="psql -h /tmp -p $PORT -U postgres -q -tA"

start f1 ""
echo "Postgres $($P -d postgres -c 'show server_version') · data_checksums=$($P -d postgres -c 'show data_checksums')"
echo "autovacuum=$($P -d postgres -c 'show autovacuum') · beépített alapérték: $($P -d postgres -c "select boot_val from pg_settings where name='autovacuum'")"
echo; echo "== A) Törölt tartalom: hol marad meg?"
$P -d postgres -c "create database nyom"
$P -d nyom -c "create table b(id int primary key, torzs text); insert into b select g, repeat('szoveg ',200) from generate_series(1,2000) g; insert into b values (7777,'$JEL');"
$P -d nyom -c "checkpoint"; F=$($P -d nyom -c "select pg_relation_filepath('b')")
van() { grep -q "$JEL" "$1" && echo MEGVAN || echo NINCS; }
echo "  adatfájl a törlés előtt:           $(van $D/f1/$F)"
$P -d nyom -c "delete from b where id=7777"; $P -d nyom -c "checkpoint"
echo "  adatfájl a törlés után:            $(van $D/f1/$F)"
echo "  WAL-szegmensek:                    $(grep -lqr "$JEL" $D/f1/pg_wal && echo MEGVAN || echo NINCS)"
$PGBIN/pg_dump -h /tmp -p $PORT -U postgres -Fp nyom > $D/d.sql; $PGBIN/pg_dump -h /tmp -p $PORT -U postgres -Fc nyom > $D/d.bin
echo "  pg_dump (plain):                   $(van $D/d.sql)"
echo "  pg_dump (custom):                  $(van $D/d.bin)"
cp $D/f1/$F $D/masolat; echo "  nyers fájlmásolat:                 $(van $D/masolat)"
$P -d nyom -c "vacuum b"; $P -d nyom -c "checkpoint"; echo "  sima VACUUM után, adatfájl:        $(van $D/f1/$F)"
$P -d nyom -c "vacuum full b"; $P -d nyom -c "checkpoint"; F2=$($P -d nyom -c "select pg_relation_filepath('b')"); echo "  VACUUM FULL után, új adatfájl:     $(van $D/f1/$F2)"

echo; echo "== B) Tranzakciós DDL: félúton elhasaló migráció"
$P -d postgres -c "create database mig"
printf "BEGIN;\nCREATE TABLE f(id int primary key, email text);\nINSERT INTO f VALUES (1,'a@b.hu');\nALTER TABLE f ADD COLUMN szerep text DEFAULT 'olvaso';\nCREATE INDEX i_e ON f(email);\nALTER TABLE f ADD COLUMN hibas nemletezo_tipus;\nCOMMIT;\n" > $D/mig.sql
psql -h /tmp -p $PORT -U postgres -d mig -q -v ON_ERROR_STOP=1 -f $D/mig.sql >/dev/null 2>&1
echo "  táblák a hiba után:  [$($P -d mig -c "select string_agg(tablename,',') from pg_tables where schemaname='public'")]"
echo "  indexek a hiba után: [$($P -d mig -c "select string_agg(indexname,',') from pg_indexes where schemaname='public'")]"
echo "  CREATE INDEX CONCURRENTLY tranzakcióban: $($P -d mig -c "create table g(x int)"; $P -d mig -c "begin; create index concurrently ig on g(x); commit;" 2>&1 | head -1)"

echo; echo "== C) Pontos vektorkeresés jogosultsági előszűréssel (50 000 × 768)"
$P -d postgres -c "create database vek"; $P -d vek -c "create extension vector"
$P -d vek -c "create table v(id int primary key, project_id int not null, e vector(768))"
python3 - "$D" <<'PY'
import random, sys
random.seed(42); d=sys.argv[1]
with open(f"{d}/vek.tsv","w") as f:
    for i in range(50000):
        f.write(f"{i}\t{i%20}\t[{','.join(f'{random.uniform(-1,1):.5f}' for _ in range(768))}]\n")
PY
$P -d vek -c "\copy v from '$D/vek.tsv'"; $P -d vek -c "create index on v(project_id)"; $P -d vek -c "analyze v"
echo "  pgvector $($P -d vek -c "select extversion from pg_extension where extname='vector'")"
python3 - "$D" "$PORT" <<'PY'
import random, subprocess, time, math, sys
d,port=sys.argv[1],sys.argv[2]
P=["psql","-h","/tmp","-p",port,"-U","postgres","-q","-tA","-d","vek"]
q=lambda s: subprocess.run(P+["-c",s],capture_output=True,text=True).stdout.strip()
random.seed(7); qv=[random.uniform(-1,1) for _ in range(768)]; qs="["+",".join(f"{x:.5f}" for x in qv)+"]"
rows=[l.split("\t") for l in open(f"{d}/vek.tsv")]
def cos(a,b): return 1-sum(x*y for x,y in zip(a,b))/(math.sqrt(sum(x*x for x in a))*math.sqrt(sum(y*y for y in b)))
ref=[i for _,i in sorted((cos(qv,[float(x) for x in r[2].strip()[1:-1].split(",")]),int(r[0])) for r in rows if int(r[1]) in (3,11))[:10]]
got=[int(x) for x in q(f"select id from v where project_id in (3,11) order by e <=> '{qs}' limit 10").split()]
print(f"  a top-10 azonos a teljes átnézéssel (Python referencia): {got==ref}")
plan=q(f"explain select id from v where project_id in (3,11) order by e <=> '{qs}' limit 10")
print("  terv: " + " → ".join(l.strip().split('(')[0].strip('-> ').strip() for l in plan.splitlines() if l.strip().startswith(('Limit','->'))))
for nev,w in [("jogosult: 10% (5 000 sor)","where project_id in (3,11)"),("jogosult: 5% (2 500 sor)","where project_id = 3"),("mind (50 000 sor)","")]:
    ts=[]
    for _ in range(5):
        t=time.perf_counter(); q(f"select id from v {w} order by e <=> '{qs}' limit 10"); ts.append((time.perf_counter()-t)*1000)
    print(f"  {nev:28} medián {sorted(ts)[2]:.0f} ms (psql-indítással együtt)")
ts=[]
for _ in range(5):
    t=time.perf_counter(); q("select 1"); ts.append((time.perf_counter()-t)*1000)
print(f"  üres psql-hívás                medián {sorted(ts)[2]:.0f} ms")
PY
$P -d vek -c "create extension amcheck"
t0=$(date +%s%N); $PGBIN/pg_amcheck -h /tmp -p $PORT -U postgres -d vek --heapallindexed >/dev/null 2>&1; rc=$?; t1=$(date +%s%N)
echo "  pg_amcheck (heap + B-tree, --heapallindexed), $($P -d vek -c "select pg_size_pretty(pg_database_size('vek'))"): $(( (t1-t0)/1000000 )) ms, kilépés: $rc"
stop f1

for MOD in "" "--data-checksums"; do
  N=f2$([ -n "$MOD" ] && echo k || echo n); start $N "$MOD"
  echo; echo "== D) Elrontott táblatartalom — data_checksums=$($P -d postgres -c 'show data_checksums')"
  $P -d postgres -c "create database kar"; $P -d kar -c "create extension amcheck"; $P -d kar -c "create table t(id int primary key, x text); insert into t select g, repeat('abc',50) from generate_series(1,5000) g;"; $P -d kar -c "checkpoint"
  F=$($P -d kar -c "select pg_relation_filepath('t')"); stop $N
  python3 -c "f='$D/$N/$F'; b=bytearray(open(f,'rb').read()); b[8192*3+2000]^=0xFF; b[8192*3+2001]^=0xFF; open(f,'wb').write(b)"
  su postgres -c "$PGBIN/pg_ctl -D $D/$N -o '-p $PORT -k /tmp' -l $D/$N.log start >/dev/null"; sleep 2
  $PGBIN/pg_amcheck -h /tmp -p $PORT -U postgres -d kar >/dev/null 2>&1; echo "  pg_amcheck kilépés: $?  (0 = nem talált hibát; 2 = sérülést talált)"
  $PGBIN/pg_dump -h /tmp -p $PORT -U postgres -Fp kar >$D/kar.sql 2>$D/kar.err; rc=$?
  echo "  pg_dump kilépés:    $rc  (0 = lefutott)$(grep -o 'invalid page in block [0-9]*' $D/kar.err | head -1 | sed 's/^/ — hibaüzenet: /')"
  if [ $rc -eq 0 ]; then
    echo "  sérült sor a mentésben: $(python3 -c "
import sys
ok='abc'*50; n=0; bent=False
for l in open('$D/kar.sql',encoding='utf-8',errors='replace'):
    if l.startswith('COPY public.t '): bent=True; continue
    if bent and l.startswith('\\.'): break
    if bent and l.rstrip('\n').split('\t')[1]!=ok: n+=1
print(f'{n} sor tér el az eredetitől')")"
  fi
  $P -d kar -c "select count(*) from t" >/dev/null 2>&1; echo "  SELECT kilépés:     $?  (0 = lefutott)"
  stop $N
done
rm -rf "$D"
