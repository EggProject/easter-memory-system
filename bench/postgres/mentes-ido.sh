#!/bin/bash
# E) Mennyi ideig tart a pg_dump, a pg_restore és a pg_amcheck három méreten (D-36, D-37, D-42)?
# Sima Postgres, bekapcsolt adatlap-ellenőrzőösszeggel (a D-43/5 javaslata). A ParadeDB-index a pg_dump-ba
# csak definícióként kerül, ezért a mentés ideje nem függ tőle; a visszaállításé igen — azt itt nem mérjük.
# Használat: PGBIN=/usr/lib/postgresql/16/bin ./mentes-ido.sh   (rootként: postgres userrel indít)
set -u
PGBIN=${PGBIN:-/usr/lib/postgresql/16/bin}
D=$(cd "$(dirname "$0")" && pwd)/adat-e; rm -rf "$D"; mkdir -p "$D"; chown postgres "$D" 2>/dev/null || true
PORT=5496
su postgres -c "$PGBIN/initdb -D $D/f -A trust -U postgres --data-checksums >/dev/null"
su postgres -c "$PGBIN/pg_ctl -D $D/f -o '-p $PORT -k /tmp' -l $D/f.log start >/dev/null"; sleep 2
P="psql -h /tmp -p $PORT -U postgres -q -tA"
ms() { echo $(( ($2-$1)/1000000 )); }
echo "Postgres $($P -d postgres -c 'show server_version') · data_checksums=$($P -d postgres -c 'show data_checksums')"
echo "Sor: azonosító + útvonal + ~4 KB szöveg (120 × md5, szóközzel). Minden mérés háromszor, melegen."
for N in 12000 50000 250000; do
  $P -d postgres -c "drop database if exists m" -c "create database m"
  $P -d m -c "create extension amcheck"
  $P -d m -c "create table e(id int primary key, ut text not null, torzs text not null)"
  $P -d m -c "insert into e select g, 'projekt/'||(g%20)||'/'||g||'.md', (select string_agg(md5(g::text||'-'||x::text),' ') from generate_series(1,120) x) from generate_series(1,$N) g"
  $P -d m -c "create index on e(ut)" -c "vacuum analyze e" -c "checkpoint"
  MB=$($P -d m -c "select round(pg_database_size('m')/1048576.0)")
  echo; echo "== $N sor · adatbázis $MB MB"
  D1=(); Z1=(); R1=(); A1=()
  for i in 1 2 3; do
    t0=$(date +%s%N); $PGBIN/pg_dump -h /tmp -p $PORT -U postgres -Fc -Z0 m > $D/m0.dump; t1=$(date +%s%N); Z1+=($(ms $t0 $t1))
    t0=$(date +%s%N); $PGBIN/pg_dump -h /tmp -p $PORT -U postgres -Fc m > $D/m.dump; rc=$?; t1=$(date +%s%N)
    [ $rc -ne 0 ] && echo "  pg_dump HIBA: $rc"; D1+=($(ms $t0 $t1))
    $P -d postgres -c "drop database if exists r" -c "create database r"
    t0=$(date +%s%N); $PGBIN/pg_restore -h /tmp -p $PORT -U postgres -d r $D/m.dump; rc=$?; t1=$(date +%s%N)
    [ $rc -ne 0 ] && echo "  pg_restore HIBA: $rc"; R1+=($(ms $t0 $t1))
    t0=$(date +%s%N); $PGBIN/pg_amcheck -h /tmp -p $PORT -U postgres -d m --heapallindexed >/dev/null 2>&1; rc=$?; t1=$(date +%s%N)
    [ $rc -ne 0 ] && echo "  pg_amcheck HIBA: $rc"; A1+=($(ms $t0 $t1))
  done
  DUMPMB=$(du -m $D/m.dump | cut -f1); DUMP0MB=$(du -m $D/m0.dump | cut -f1)
  SORR=$($P -d r -c "select count(*) from e")
  echo "  pg_dump -Fc:              ${D1[*]} ms   (a mentés $DUMPMB MB)"
  echo "  pg_dump -Fc -Z0 (tömörítés nélkül): ${Z1[*]} ms   (a mentés $DUMP0MB MB)"
  echo "  pg_restore (+ B-fa index): ${R1[*]} ms   (visszaállítva $SORR sor)"
  echo "  pg_amcheck --heapallindexed: ${A1[*]} ms"
done
su postgres -c "$PGBIN/pg_ctl -D $D/f stop -m fast >/dev/null"
rm -rf "$D"
