// EGY mérés, saját folyamatban (hogy ne legyen folyamaton belüli gyorsítótár-átszivárgás).
// Használat: bun meres.ts <vacuum|copy|olvas|quick_check|integrity_check|foreign_key_check> <forrás> [cél]
import { Database } from "bun:sqlite";
import { rmSync, statSync, copyFileSync } from "node:fs";
const [mod, forras, cel] = process.argv.slice(2);
let t0: number, t: number, extra: any = {};
if (mod === "vacuum") {
  try { rmSync(cel!); } catch {}
  const db = new Database(forras); t0 = performance.now(); db.exec(`VACUUM INTO '${cel}'`); t = performance.now() - t0; db.close();
  extra.kimenetByte = statSync(cel!).size;
} else if (mod === "copy") {
  try { rmSync(cel!); } catch {}
  t0 = performance.now(); copyFileSync(forras, cel!); t = performance.now() - t0; extra.kimenetByte = statSync(cel!).size;
} else if (mod === "olvas") {
  t0 = performance.now(); const b = await Bun.file(forras).arrayBuffer(); t = performance.now() - t0; extra.byte = b.byteLength;
} else if (["quick_check", "integrity_check", "foreign_key_check"].includes(mod)) {
  const db = new Database(forras); t0 = performance.now(); const r = db.query(`PRAGMA ${mod}`).all(); t = performance.now() - t0; db.close();
  extra.sorok = r.length; extra.elso = JSON.stringify(r[0] ?? null).slice(0, 80);
} else throw new Error("ismeretlen mód: " + mod);
console.log(JSON.stringify({ mod, ms: Math.round(t!), ...extra }));
