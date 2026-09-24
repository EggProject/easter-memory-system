// Hogyan kezeli az FTS5 unicode61 tokenizáló a magyar ékezeteket, a remove_diacritics beállítás szerint?
import { Database } from "bun:sqlite";
const db = new Database(":memory:");
const SZOVEG = ["őrző kutya", "kötő tű", "fűzfa ág", "hűtő", "kör alakú", "kor szerint", "tör eszköz", "ház kulcs"];
const KERES = ["őrző", "orzo", "örző", "kötő", "koto", "fűzfa", "fuzfa", "hűtő", "huto", "kör", "kor", "tör", "tor", "ház", "haz"];
const MODOK: [string, string][] = [["alapértelmezett", "unicode61"], ["remove_diacritics 0", "unicode61 remove_diacritics 0"],
  ["remove_diacritics 1", "unicode61 remove_diacritics 1"], ["remove_diacritics 2", "unicode61 remove_diacritics 2"]];
console.log("SQLite", (db.query("select sqlite_version() v").get() as any).v, "| Bun", Bun.version);
for (const [nev, tok] of MODOK) {
  db.exec("DROP TABLE IF EXISTS t");
  db.exec(`CREATE VIRTUAL TABLE t USING fts5(x, tokenize='${tok}')`);
  const be = db.prepare("INSERT INTO t(x) VALUES (?)"); for (const s of SZOVEG) be.run(s);
  const q = db.prepare("SELECT x FROM t WHERE t MATCH ?");
  console.log(`\n== ${nev} ==`);
  for (const k of KERES) console.log(`  ${k.padEnd(7)} → ${(q.all(`"${k}"`) as any[]).map(r => r.x).join(" | ") || "—"}`);
}
