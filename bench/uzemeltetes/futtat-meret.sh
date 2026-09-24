#!/bin/bash
# VACUUM INTO, fájlmásolás és integritás-ellenőrzés méret szerint, hidegen és melegen, külön folyamatokban.
# Hideg mérés csak Linuxon, rootként (drop_caches). Használat: BUN=bun ./futtat-meret.sh
cd "$(dirname "$0")"; BUN=${BUN:-bun}; unset BUN_OPTIONS; D=adat; mkdir -p $D
hideg() { if [ -w /proc/sys/vm/drop_caches ]; then sync; echo 3 > /proc/sys/vm/drop_caches; echo hideg; else echo "meleg*"; fi; }
echo "Bun $($BUN --version) | $(uname -sm)"
for MB in 50 200 1000; do
  F=$D/b$MB.sqlite
  echo "=== $MB MB cél — $($BUN epit.ts $F $MB) ==="
  for MOD in olvas copy vacuum quick_check integrity_check foreign_key_check; do
    printf "  %-18s %s: %s\n" "$MOD" "$(hideg)" "$($BUN meres.ts $MOD $F $D/ki.sqlite)"; rm -f $D/ki.sqlite
    for i in 1 2 3; do printf "  %-18s meleg: %s\n" "$MOD" "$($BUN meres.ts $MOD $F $D/ki.sqlite)"; rm -f $D/ki.sqlite; done
  done
  echo "  -- fordított sorrend, hidegen --"
  printf "  integrity_check %s: %s\n" "$(hideg)" "$($BUN meres.ts integrity_check $F)"
  printf "  quick_check     %s: %s\n" "$(hideg)" "$($BUN meres.ts quick_check $F)"
  rm -f $F $F-wal $F-shm
done
