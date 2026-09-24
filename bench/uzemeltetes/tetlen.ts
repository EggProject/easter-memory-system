// Író, ami SIGUSR1-re abbahagyja az írást, de NYITVA tartja a kapcsolatot.
import { Database } from "bun:sqlite";
const db = new Database(process.argv[2]);
db.exec("PRAGMA journal_mode = WAL; PRAGMA synchronous = NORMAL; PRAGMA busy_timeout = 10000;");
const be = db.prepare("INSERT INTO bejegyzes (utvonal,cim,torzs,modositva) VALUES (?,?,?,?)");
const t = "toltelek ".repeat(20); let n = 0, ir = true;
process.on("SIGUSR1", () => { ir = false; });
process.on("SIGTERM", () => process.exit(0));
setInterval(() => { if (!ir) return; db.exec("BEGIN"); for (let i = 0; i < 400; i++) { be.run(`k/${n}.md`, `K${n}`, t, Date.now()); n++; } db.exec("COMMIT"); }, 1);
