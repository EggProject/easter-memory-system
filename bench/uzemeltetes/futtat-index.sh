#!/bin/bash
# Index-újraépítés mérése több méretben. Hideg mérés csak Linuxon, rootként (drop_caches).
# Használat: BUN=bun ./futtat-index.sh
cd "$(dirname "$0")"
BUN=${BUN:-bun}
unset BUN_OPTIONS
hideg() { if [ -w /proc/sys/vm/drop_caches ]; then sync; echo 3 > /proc/sys/vm/drop_caches; echo hideg; else echo "meleg(nincs drop_caches)"; fi; }
echo "Bun $($BUN --version) | $(uname -sm)"
for KB in 1 4; do
  for DB in 1000 10000 50000; do
    FA=adat/fa-$DB-$KB
    $BUN gen-fa.ts $FA $DB $KB >/dev/null
    echo "=== $DB fájl × $KB KB törzs ==="
    printf "  %s: %s\n" "$(hideg)" "$($BUN ujraepit.ts $FA adat/index.sqlite)"
    for i in 1 2; do printf "  meleg:  %s\n" "$($BUN ujraepit.ts $FA adat/index.sqlite)"; done
    rm -rf $FA adat/index.sqlite*
  done
done
