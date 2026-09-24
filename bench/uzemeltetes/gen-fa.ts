// Szintetikus memória-fa: markdown fájlok a D-05/D-06 szerinti négymezős YAML fejléccel.
// Használat: bun gen-fa.ts <célkönyvtár> <fájlszám> <törzs KB>
import { mkdirSync, writeFileSync, rmSync } from "node:fs";
import { join } from "node:path";
const [cel, dbS, kbS] = process.argv.slice(2);
const db = Number(dbS), kb = Number(kbS);
rmSync(cel, { recursive: true, force: true });
const SZ = ("a rendszer memória bejegyzés keresés index beágyazás döntés dokumentum jegyzet projekt tudás " +
  "személyes címke változat formátum napló mentés visszaállítás kiszolgáló illesztő képesség zászló " +
  "őrző kötő fűzfa hűtő tűz örök ügyfél előszűrés jogosultság összefésülés újraépítés kör kor tör").split(" ");
const CIMKE = ["projekt/alfa", "projekt/béta", "döntés", "ügyfél/acme", "tudás/sqlite", "hiba", "mérés"];
function torzs(n: number) {
  const cel = n * 1024; let s = "";
  while (s.length < cel) {
    let m = ""; const h = 6 + Math.floor(Math.random() * 10);
    for (let i = 0; i < h; i++) m += SZ[Math.floor(Math.random() * SZ.length)] + " ";
    s += m.trim() + ". ";
    if (Math.random() < 0.04) s += "\n\n## Alcím\n\n";
  }
  return s.slice(0, cel);
}
for (let i = 0; i < db; i++) {
  const dir = join(cel, "projects", `p${i % 20}`, `m${(i >> 5) % 10}`);
  mkdirSync(dir, { recursive: true });
  const t = [CIMKE[i % CIMKE.length], CIMKE[(i * 7) % CIMKE.length]];
  const fej = `---\ntags: ["${t[0]}", "${t[1]}"]\nmodified: "2026-09-${String(1 + (i % 28)).padStart(2, "0")}T12:00:00Z"\nprompt_version: 3\nformat_version: 1\n---\n`;
  writeFileSync(join(dir, `e${i}.md`), fej + `# Bejegyzés ${i}\n\n` + torzs(kb) + "\n");
}
console.log(JSON.stringify({ fajl: db, torzsKB: kb }));
