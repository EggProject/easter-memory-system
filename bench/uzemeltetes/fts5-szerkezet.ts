// Módosítható-e utólag egy FTS5 virtuális tábla szerkezete? (D-37/5)
// MEGJEGYZÉS: az eredeti, 2026-09-15-i szkript egy konténer-újraindításkor elveszett. Ez a változat a rögzített
// kimenet alapján készült újra (ugyanazok a lépések, ugyanazok a nevek), és a kimenetét össze kell vetni az eredetivel.
import { Database } from "bun:sqlite";
const db = new Database(":memory:");
console.log("SQLite verzió:", (db.query("select sqlite_version() v").get() as any).v, "| Bun", Bun.version);
db.exec("CREATE TABLE bejegyzes (id INTEGER PRIMARY KEY, cim TEXT, torzs TEXT)");
const be = db.prepare("INSERT INTO bejegyzes (cim, torzs) VALUES (?, ?)");
for (let i = 0; i < 100; i++) be.run(`Bejegyzés ${i}`, `A szerződés ${i}. pontja szerint a határidő módosul.`);
db.exec("CREATE VIRTUAL TABLE bej_fts USING fts5(cim, torzs, content='bejegyzes', content_rowid='id')");
db.exec("INSERT INTO bej_fts(bej_fts) VALUES('rebuild')");
const lepes = (n: string, sql: string, utana?: () => string) => {
  try { db.exec(sql); console.log(`${n} ${sql.padEnd(58)} SIKERÜLT${utana ? " — " + utana() : ""}`); }
  catch (e: any) { console.log(`${n} ${sql.padEnd(58)} HIBA — ${e.message}`); }
};
lepes("1)", "ALTER TABLE bej_fts ADD COLUMN cimke");
lepes("2)", "ALTER TABLE bej_fts DROP COLUMN torzs");
lepes("3)", "ALTER TABLE bej_fts RENAME COLUMN cim TO fejlec");
lepes("4)", "ALTER TABLE bej_fts RENAME TO bej_fts2");
db.exec("ALTER TABLE bej_fts2 RENAME TO bej_fts");
lepes("5)", "ALTER TABLE bej_fts SET tokenize='trigram'");
lepes("6)", "INSERT INTO bej_fts(bej_fts) VALUES('rebuild')");
lepes("  ", "INSERT INTO bej_fts(bej_fts) VALUES('integrity-check')");
db.exec("DROP TABLE bej_fts");
lepes("7)", "CREATE VIRTUAL TABLE bej_fts USING fts5(cim, torzs, content='bejegyzes', content_rowid='id', tokenize='trigram')");
db.exec("INSERT INTO bej_fts(bej_fts) VALUES('rebuild')");
console.log(`   rebuild után részszó-találat ('szerz'): ${(db.query("SELECT count(*) c FROM bej_fts WHERE bej_fts MATCH 'szerz'").get() as any).c} sor`);
// 8) a trigger nem tölt fel visszamenőleg
db.exec("CREATE TABLE b2 (id INTEGER PRIMARY KEY, torzs TEXT)");
const be2 = db.prepare("INSERT INTO b2 (torzs) VALUES (?)");
for (let i = 0; i < 50; i++) be2.run(`jogosultság ${i}`);
db.exec("CREATE VIRTUAL TABLE b2_fts USING fts5(torzs, content='b2', content_rowid='id')");
db.exec("CREATE TRIGGER b2_ai AFTER INSERT ON b2 BEGIN INSERT INTO b2_fts(rowid, torzs) VALUES (new.id, new.torzs); END");
const q = () => (db.query("SELECT count(*) c FROM b2_fts WHERE b2_fts MATCH 'jogosultság'").get() as any).c;
console.log(`8) trigger után, rebuild ELŐTT: ${q()} találat`);
db.exec("INSERT INTO b2_fts(b2_fts) VALUES('rebuild')");
console.log(`   rebuild UTÁN:                ${q()} találat`);
