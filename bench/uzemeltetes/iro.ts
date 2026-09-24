// Konkurens író alfolyamat: maga méri az átbocsátását, 400 ms-onként kiírja. Korlát: 25 mp vagy +600 MB.
import { Database } from "bun:sqlite";
import { statSync } from "node:fs";
const u = process.argv[2];
const db = new Database(u);
db.exec("PRAGMA journal_mode = WAL; PRAGMA synchronous = NORMAL; PRAGMA busy_timeout = 10000;");
const be = db.prepare("INSERT INTO bejegyzes (utvonal,cim,torzs,modositva) VALUES (?,?,?,?)");
const t = "konkurens toltelek szoveg ".repeat(8);
const indulo = statSync(u).size, kezdet = Date.now();
let n = 0, hiba = 0, utolso = performance.now();
function veg(): never { console.log(JSON.stringify({ vege: true, n, hiba })); process.exit(0); }
process.on("SIGTERM", veg);
while (true) {
  try { db.exec("BEGIN"); for (let i = 0; i < 25; i++) { be.run(`konk/${n}.md`, `K${n}`, t, Date.now()); n++; } db.exec("COMMIT"); }
  catch { hiba++; try { db.exec("ROLLBACK"); } catch {} }
  const most = performance.now();
  if (most - utolso >= 400) {
    console.log(JSON.stringify({ t: Date.now(), n, hiba })); utolso = most;
    if (Date.now() - kezdet > 25000 || statSync(u).size - indulo > 600 * 1048576) veg();
  }
}
