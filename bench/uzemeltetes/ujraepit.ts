// Index-újraépítés a fájlfából, ahogy a D-37 előírja (az index soha nem migrál, mindig újraépül).
// Fázisonként mér: bejárás, olvasás, fejléc-parse (Bun.YAML — a D-05 parsere), tartalom-lenyomat, beszúrás.
// Használat: bun ujraepit.ts <fa könyvtár> <index.sqlite>
import { Database } from "bun:sqlite";
import { readdirSync, readFileSync, rmSync, statSync } from "node:fs";
import { join } from "node:path";
const [fa, dbPath] = process.argv.slice(2);
for (const v of ["", "-wal", "-shm"]) { try { rmSync(dbPath + v); } catch {} }
const T: Record<string, number> = { bejaras: 0, olvasas: 0, parse: 0, lenyomat: 0, beszuras: 0, optimize: 0 };
const t0 = performance.now();

let t = performance.now();
const fajlok = (readdirSync(fa, { recursive: true }) as string[]).filter(f => f.endsWith(".md"));
T.bejaras = performance.now() - t;

const db = new Database(dbPath, { create: true });
db.exec("PRAGMA journal_mode = WAL; PRAGMA synchronous = NORMAL;");
db.exec(`CREATE TABLE bejegyzes (id INTEGER PRIMARY KEY, utvonal TEXT UNIQUE, modified TEXT,
           prompt_version INTEGER, format_version INTEGER, lenyomat TEXT);
         CREATE VIRTUAL TABLE bej_fts USING fts5(utvonal, tags, torzs, tokenize='unicode61 remove_diacritics 2');`);   // a bench/ lex lábának beállítása
const b1 = db.prepare("INSERT INTO bejegyzes (id, utvonal, modified, prompt_version, format_version, lenyomat) VALUES (?,?,?,?,?,?)");
const b2 = db.prepare("INSERT INTO bej_fts (rowid, utvonal, tags, torzs) VALUES (?,?,?,?)");

let bajt = 0, hibas = 0;
db.exec("BEGIN");
for (let i = 0; i < fajlok.length; i++) {
  const ut = fajlok[i];
  t = performance.now(); const s = readFileSync(join(fa, ut), "utf8"); T.olvasas += performance.now() - t;
  bajt += Buffer.byteLength(s);
  t = performance.now();
  const v = s.indexOf("\n---\n", 4);
  let fej: any = null, torzs = s;
  try { fej = Bun.YAML.parse(s.slice(4, v)); torzs = s.slice(v + 5); } catch { hibas++; }
  T.parse += performance.now() - t;
  t = performance.now(); const h = new Bun.CryptoHasher("sha256").update(torzs).digest("hex"); T.lenyomat += performance.now() - t;
  t = performance.now();
  b1.run(i, ut, fej?.modified ?? null, fej?.prompt_version ?? null, fej?.format_version ?? null, h);
  b2.run(i, ut, (fej?.tags ?? []).join(" "), torzs);
  if (i % 1000 === 999) { db.exec("COMMIT"); db.exec("BEGIN"); }
  T.beszuras += performance.now() - t;
}
t = performance.now(); db.exec("COMMIT"); T.beszuras += performance.now() - t;
t = performance.now(); db.exec("INSERT INTO bej_fts(bej_fts) VALUES('optimize')"); T.optimize = performance.now() - t;
db.exec("PRAGMA wal_checkpoint(TRUNCATE)");
const ok = (db.query("SELECT count(*) c FROM bej_fts WHERE bej_fts MATCH 'jogosultság'").get() as any).c;
db.close();
const ossz = performance.now() - t0;
const r = (x: number) => Math.round(x);
console.log(JSON.stringify({
  fajl: fajlok.length, szovegMB: +(bajt / 1048576).toFixed(1), hibasFejlec: hibas,
  osszMs: r(ossz), fazisMs: Object.fromEntries(Object.entries(T).map(([k, v]) => [k, r(v)])),
  fajlPerMp: r(fajlok.length / (ossz / 1000)), MBperMp: +((bajt / 1048576) / (ossz / 1000)).toFixed(1),
  indexMB: +(statSync(dbPath).size / 1048576).toFixed(1), probaTalalat: ok,
}));
