const Y: any = (Bun as any).YAML;
console.log("Bun.YAML API:", Object.keys(Y).join(", "));

const eredeti = `cim: "Acme — szerződés"
kategoria: ugyfel
verzio: 1.20
cimkek: ["tech/typescript", "ügyfél/acme"]
letrehozva: "2026-08-21"
`;
console.log("\n--- EREDETI ---\n" + eredeti);

if (typeof Y.stringify === "function") {
  const vissza = Y.stringify(Y.parse(eredeti));
  console.log("--- PARSE + STRINGIFY UTÁN ---\n" + vissza);
  console.log("azonos?", vissza.trim() === eredeti.trim() ? "IGEN" : "NEM — a forrás megváltozott");
} else {
  console.log("Bun.YAML.stringify NINCS — vagyis a Bun magától nem is tud visszaírni YAML-t.");
  console.log("Ez önmagában védelem: nincs mivel elrontani a fájlt egy naiv oda-vissza körrel.");
}

console.log("\n=== TOML ===");
const T: any = (Bun as any).TOML;
if (T) {
  console.log("Bun.TOML API:", Object.keys(T).join(", "));
  const toml = `cim = "Acme — szerződés"
kategoria = "ugyfel"
verzio = "1.20"
cimkek = ["tech/typescript", "ügyfél/acme"]
letrehozva = "2026-08-21"
`;
  const r = T.parse(toml);
  for (const [k, v] of Object.entries(r)) console.log(`  ${k.padEnd(12)} ${Array.isArray(v)?"array":typeof v} ${JSON.stringify(v)}`);
  try { T.parse('verzio = 1.20'); console.log("  idézőjel nélküli 1.20 ->", JSON.stringify(T.parse('verzio = 1.20').verzio), "(szám)"); } catch(e:any){ console.log("  1.20 hiba:", e.message.slice(0,40)); }
  try { T.parse('a = no'); } catch(e:any){ console.log("  idézőjel nélküli 'no' -> HIBA (a TOML kötelezővé teszi az idézőjelet):", e.message.slice(0,50)); }
}
