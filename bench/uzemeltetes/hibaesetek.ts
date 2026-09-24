// A VACUUM INTO hibaesetei, és hogy mely beállítások öröklődnek a kimenetre.
import { Database } from "bun:sqlite";
import { rmSync, mkdirSync } from "node:fs";
import { join } from "node:path";
const D = join(import.meta.dir, "adat"); mkdirSync(D, { recursive: true });
const BUN = process.execPath, S = (f: string) => join(import.meta.dir, f);
const F = join(D, "h.sqlite"), C = join(D, "h-ki.sqlite");
const torol = () => { for (const f of [F, C]) for (const v of ["", "-wal", "-shm"]) { try { rmSync(f + v); } catch {} } };
torol(); Bun.spawnSync([BUN, S("epit.ts"), F, "10"]);
const proba = (nev: string, fn: () => void) => { try { fn(); console.log(`${nev.padEnd(26)} SIKERÜLT`); } catch (e: any) { console.log(`${nev.padEnd(26)} HIBA — ${e.message}`); } };
console.log(`Bun ${Bun.version}`);
const db = new Database(F);
db.exec(`VACUUM INTO '${C}'`);
proba("létező célfájlra", () => db.exec(`VACUUM INTO '${C}'`));
proba("nem létező könyvtárba", () => db.exec(`VACUUM INTO '${join(D, "nincs", "ilyen", "x.sqlite")}'`));
proba("nyitott tranzakcióban", () => { db.exec("BEGIN"); try { db.exec(`VACUUM INTO '${join(D, "h2.sqlite")}'`); } finally { db.exec("ROLLBACK"); } });
db.close();
// Öröklődés: NEM alapértelmezett értékekkel, különben a 0 → 0 egyezés semmit nem bizonyít.
const F2 = join(D, "h3.sqlite"), C2 = join(D, "h3-ki.sqlite");
for (const f of [F2, C2]) for (const v of ["", "-wal", "-shm"]) { try { rmSync(f + v); } catch {} }
const s = new Database(F2, { create: true });
s.exec("PRAGMA page_size = 8192; PRAGMA auto_vacuum = INCREMENTAL; PRAGMA user_version = 7; PRAGMA application_id = 424242;");
s.exec("CREATE TABLE t (x TEXT); INSERT INTO t VALUES ('a');");
s.exec("PRAGMA journal_mode = WAL;");
s.exec(`VACUUM INTO '${C2}'`);
const k = new Database(C2);
const g = (d: Database, p: string) => Object.values(d.query(`PRAGMA ${p}`).get() as any)[0];
for (const p of ["journal_mode", "page_size", "auto_vacuum", "user_version", "application_id"]) {
  const a = g(s, p), b = g(k, p);
  console.log(`${p.padEnd(15)} forrás: ${String(a).padEnd(8)} mentés: ${String(b).padEnd(8)} ${a == b ? "öröklődik" : "NEM öröklődik"}`);
}
k.close(); s.close();
for (const f of [F2, C2]) for (const v of ["", "-wal", "-shm"]) { try { rmSync(f + v); } catch {} }
torol(); try { rmSync(join(D, "h2.sqlite")); } catch {}
