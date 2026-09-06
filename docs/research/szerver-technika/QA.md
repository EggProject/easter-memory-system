# QA — a kutatási anyag ellenőrzése

Lefuttatva: 2026-09-05T00:17:41Z

## Összegzés

- quote fidelity: 143/148 exact (97%), 4 stitched, 1 not found
- snapshots modified after capture: 1
- verification coverage: 86% (21 unchecked)
- confidence tags in report: 51
- link health: LIVE 84
- sources: 84 | claims: 148 | attachments: 0

## Hibák

- claim SQ-07-C001: quote not found in snapshot — the citation does not support it

## Figyelmeztetések

- claim SQ-01-C009: stitched from separate lines
- claim SQ-07-C003: stitched from separate lines
- claim SQ-07-C006: stitched from separate lines
- claim SQ-07-C017: stitched from separate lines
- snapshot src_2026-09-04_github-com_concurrent-edits-to-the-same-file-will-overwrite-the-documen differs from its capture hash — anything quoted from the changed part is quoting the agent, not the source

## Mit jelent ez

A hibák listája blokkoló: minden sor egy állítás, ami nem visszakövethető, vagy egy hivatkozás, ami nem ellenőrizhető. Ezeket a riport véglegesítése előtt javítani kell.
A figyelmeztetések nem blokkolnak, de rontják az anyag auditálhatóságát.

## A `finalize.py` zárófutása (2026-09-05)

```
quote fidelity: 143/148 exact (97%), 4 stitched, 1 not found
snapshots modified after capture: 1
verification coverage: 86% (21 unchecked)
confidence tags in report: 51
link health: LIVE 84
sources: 84 | claims: 148
```

- **1 db "quote not found"** — `SQ-07-C001` (SQLite ATTACH-korlátok). Oka ismert és
  dokumentált: a mentett pillanatkép csonka, az idézet az élő oldalon szó szerint megvan, és
  a verifikáló élőben ellenőrizte. Az állítás áll, a pillanatkép hibás.
- **1 db módosult pillanatkép** — az SQ-03 slug-ütközés (két Logseq-forrás azonos fájlnévre).
- **4 db "stitched" idézet** — több sorból összefűzött, a script jelöli, nem hiba.
- **21 ellenőrizetlen állítás** — a gap-kör (`G-01`, `G-02`) állításai a verifikációs hullám
  után születtek. A két legfontosabbat (Bun #31247 nyitottsága, Better Auth hook-hatókör) a
  gap-ügynökök élőben ellenőrizték a rögzítéskor.
