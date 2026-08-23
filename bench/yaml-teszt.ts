// Mit csinál a Bun beépített YAML- és TOML-parsere a veszélyes mezőkkel?
const esetek: [string,string][] = [
  ["verzió, idézőjel nélkül",      'v: 1.20'],
  ["verzió, idézőjelben",          'v: "1.20"'],
  ["nem/no, idézőjel nélkül",      'v: no'],
  ["nem/no, idézőjelben",          'v: "no"'],
  ["igen/yes, idézőjel nélkül",    'v: yes'],
  ["off, idézőjel nélkül",         'v: off'],
  ["óra, idézőjel nélkül",         'v: 22:22'],
  ["óra, idézőjelben",             'v: "22:22"'],
  ["dátum, idézőjel nélkül",       'v: 2026-08-21'],
  ["dátum, idézőjelben",           'v: "2026-08-21"'],
  ["magyar ékezetes érték",        'v: "felhasználói preferenciák"'],
  ["magyar ékezetes idézőjel n.",  'v: felhasználói preferenciák'],
  ["hierarchikus címke",           'v: ["tech/typescript", "ügyfél/acme"]'],
  ["kettőspont a szövegben",       'v: "Ügyfél: preferenciák"'],
  ["kettőspont idézőjel nélkül",   'v: Ügyfél: preferenciák'],
];
console.log("BUN.YAML");
console.log("  eset".padEnd(34) + "típus      érték");
console.log("  " + "-".repeat(70));
for (const [nev, y] of esetek) {
  let t = "?", v: any = "?";
  try { const r: any = (Bun as any).YAML.parse(y); v = r.v; t = v === null ? "null" : Array.isArray(v) ? "array" : typeof v; }
  catch (e: any) { t = "HIBA"; v = String(e.message).slice(0, 30); }
  const eredeti = y.slice(3);
  const valt = String(v) !== eredeti.replace(/^"|"$/g, "");
  console.log(`  ${nev.padEnd(32)} ${t.padEnd(9)} ${JSON.stringify(v)}${valt && t!=="HIBA" ? "   <-- MEGVÁLTOZOTT" : ""}`);
}
