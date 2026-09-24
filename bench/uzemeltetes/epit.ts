// Szintetikus adatbázis a mentés-mérésekhez: bejegyzés-tábla (2-4 KB magyar törzs) + beágyazás-tábla
// (768 dimenziós float32 BLOB), két index és egy idegen kulcs. WAL mód.
// Használat: bun epit.ts <adatbázis> <cél MB> [jelölő-szöveg a 7-es sorba]
import { Database } from "bun:sqlite";
import { statSync, rmSync } from "node:fs";
const [u, celS, jelolo] = process.argv.slice(2);
const celMB = Number(celS);
for (const v of ["", "-wal", "-shm"]) { try { rmSync(u + v); } catch {} }
const meret = () => { let s = 0; for (const v of ["", "-wal", "-shm"]) { try { s += statSync(u + v).size; } catch {} } return s; };
const SZ = "a rendszer memoria bejegyzes kereses index beagyazas dontes dokumentum jegyzet projekt tudas szemelyes cimke modositva valtozat formatum naplo mentes".split(" ");
const torzs = (kb: number) => { const c = kb * 1024; let s = ""; while (s.length < c) { let m = ""; const h = 6 + Math.floor(Math.random() * 10); for (let i = 0; i < h; i++) m += SZ[Math.floor(Math.random() * SZ.length)] + " "; s += m.trim() + ". "; } return s.slice(0, c); };
const vek = (d: number) => { const f = new Float32Array(d); for (let i = 0; i < d; i++) f[i] = Math.random() * 2 - 1; return new Uint8Array(f.buffer); };
const db = new Database(u, { create: true });
db.exec("PRAGMA journal_mode = WAL; PRAGMA synchronous = NORMAL; PRAGMA foreign_keys = ON;");
db.exec(`CREATE TABLE bejegyzes (id INTEGER PRIMARY KEY, utvonal TEXT, cim TEXT, torzs TEXT, modositva INTEGER);
  CREATE TABLE beagyazas (id INTEGER PRIMARY KEY, bejegyzes_id INTEGER REFERENCES bejegyzes(id), vektor BLOB);
  CREATE INDEX i_ut ON bejegyzes(utvonal); CREATE INDEX i_mod ON bejegyzes(modositva); CREATE INDEX i_fk ON beagyazas(bejegyzes_id);`);
const b1 = db.prepare("INSERT INTO bejegyzes (id,utvonal,cim,torzs,modositva) VALUES (?,?,?,?,?)");
const b2 = db.prepare("INSERT INTO beagyazas (bejegyzes_id,vektor) VALUES (?,?)");
let n = 0;
while (meret() < celMB * 1048576) {
  db.exec("BEGIN");
  for (let i = 0; i < 400; i++) {
    const t = (n === 7 && jelolo) ? jelolo + " " + torzs(3) : torzs(2 + Math.floor(Math.random() * 3));
    b1.run(n, `projects/p/${n}.md`, `B ${n}`, t, Date.now()); b2.run(n, vek(768)); n++;
  }
  db.exec("COMMIT");
}
db.exec("PRAGMA wal_checkpoint(TRUNCATE); ANALYZE;");
db.close();
console.log(JSON.stringify({ bejegyzes: n, byte: statSync(u).size }));
