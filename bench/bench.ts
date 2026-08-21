#!/usr/bin/env bun
/**
 * Easter — többnyelvű keresési mérőkészlet.
 *
 * Megméri ugyanazon a korpuszon:
 *   lex   — FTS5 szó-index (unicode61 remove_diacritics 2, tövező nélkül)
 *   tri   — FTS5 trigram-index (részszó)
 *   dense — beágyazó modell (koszinusz)
 *   lex+dense        — a javasolt két lábas hibrid (RRF)
 *   lex+tri+dense    — a három lábas hibrid (RRF)
 *
 * Külső függőség nincs: bun:sqlite + fetch.
 *
 *   bun bench.ts --endpoint http://192.168.50.48:8000/v1 --model qwen3-embedding-8b-4bit-dwq
 *   bun bench.ts ... --out eredmeny-dwq.json
 *   bun bench.ts --compare eredmeny-fp16.json eredmeny-dwq.json
 */

import { Database } from "bun:sqlite";
import { readdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

type Doc = { id: string; lang: string; text: string };
type Query = { id: string; lang: string; kind: string; query: string; expect: string };
type Ranked = string[]; // doc id-k rangsor szerint

const RRF_K = 60;
// Hány karakter után vágjuk a szót tőnek. Toldalékolt nyelveknél ez pótolja a tövezőt.
const STEM = Number(process.env.EASTER_STEM ?? 6);
const TOPK = 10;
// A Qwen3 model card szerint a query-oldali instrukció elhagyása 1-5% veszteséget okoz.
const INSTRUCT = "Given a search query, retrieve relevant passages that answer the query";

// ---------- argumentumok ----------
function arg(name: string, fallback?: string): string | undefined {
  const i = process.argv.indexOf(`--${name}`);
  return i >= 0 && process.argv[i + 1] ? process.argv[i + 1] : fallback;
}
const FLAG = (name: string) => process.argv.includes(`--${name}`);

// ---------- korpusz ----------
function loadCorpus(dir: string) {
  const docs: Doc[] = [];
  const queries: Query[] = [];
  for (const f of readdirSync(dir).filter((f) => f.endsWith(".json")).sort()) {
    const raw = JSON.parse(readFileSync(join(dir, f), "utf8"));
    const lang: string = raw.lang;
    for (const d of raw.docs) docs.push({ id: `${lang}:${d.id}`, lang, text: d.text });
    for (const q of raw.queries)
      queries.push({ id: `${lang}:${q.id}`, lang, kind: q.kind, query: q.query, expect: `${lang}:${q.expect}` });
  }
  const ids = new Set(docs.map((d) => d.id));
  for (const q of queries)
    if (!ids.has(q.expect)) throw new Error(`A(z) ${q.id} kérdés nem létező dokumentumra mutat: ${q.expect}`);
  return { docs, queries };
}

// ---------- FTS5 index ----------
function buildIndex(docs: Doc[]) {
  const db = new Database(":memory:");
  db.run(`CREATE TABLE docs(rowid INTEGER PRIMARY KEY, id TEXT UNIQUE, text TEXT)`);
  db.run(`CREATE VIRTUAL TABLE fts_word USING fts5(text, content='docs', content_rowid='rowid',
          tokenize='unicode61 remove_diacritics 2')`);
  db.run(`CREATE VIRTUAL TABLE fts_tri USING fts5(text, content='docs', content_rowid='rowid',
          tokenize='trigram')`);
  const ins = db.prepare(`INSERT INTO docs(rowid, id, text) VALUES (?, ?, ?)`);
  docs.forEach((d, i) => ins.run(i + 1, d.id, d.text));
  db.run(`INSERT INTO fts_word(fts_word) VALUES('rebuild')`);
  db.run(`INSERT INTO fts_tri(fts_tri) VALUES('rebuild')`);
  return db;
}

/**
 * FTS5 lekérdezéssé alakít úgy, hogy a metakarakterek elveszítsék a jelentésüket.
 *
 * mode = "exact"  — csak a pontos szóalak
 * mode = "prefix" — pontos szóalak VAGY a szó első STEM karakterének prefixe.
 *                   Ez a toldalékolt nyelvek (magyar, finn, török, lengyel) trükkje
 *                   tövező NÉLKÜL: a rag a szó VÉGÉN van, tehát az eleje a tő.
 * mode = "sub"    — trigram-táblához: a tő mint részszó, bárhol a szövegben.
 */
function ftsQuery(q: string, mode: "exact" | "and" | "star" | "prefix" | "sub", minLen: number): string | null {
  const raw = q.split(/[^\p{L}\p{N}_-]+/u).filter((t) => t.length >= minLen);
  const esc = (t: string) => `"${t.replace(/"/g, '""')}"`;
  const parts: string[] = [];
  for (const t of raw) {
    if (mode === "exact" || mode === "and") { parts.push(esc(t)); continue; }
    if (mode === "star") { parts.push(`${esc(t)}*`); continue; } // vágás NÉLKÜL
    const stem = t.length > STEM ? t.slice(0, STEM) : t;
    if (mode === "prefix") {
      parts.push(`${esc(t)}*`);
      if (stem !== t) parts.push(`${esc(stem)}*`);
    } else {
      parts.push(esc(stem));
    }
  }
  const uniq = [...new Set(parts)];
  return uniq.length ? uniq.join(mode === "and" ? " AND " : " OR ") : null;
}

function ftsSearch(db: Database, table: string, q: string, mode: "exact" | "and" | "star" | "prefix" | "sub", minLen: number): Ranked {
  const match = ftsQuery(q, mode, minLen);
  if (!match) return [];
  try {
    return db
      .prepare(
        `SELECT d.id FROM ${table} f JOIN docs d ON d.rowid = f.rowid
         WHERE ${table} MATCH ? ORDER BY bm25(${table}) LIMIT ${TOPK}`,
      )
      .all(match)
      .map((r: any) => r.id);
  } catch {
    return [];
  }
}

// ---------- beágyazás ----------
async function embed(endpoint: string, model: string, inputs: string[], batch: number): Promise<Float32Array[]> {
  const out: Float32Array[] = [];
  for (let i = 0; i < inputs.length; i += batch) {
    const slice = inputs.slice(i, i + batch);
    const res = await fetch(`${endpoint.replace(/\/$/, "")}/embeddings`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ model, input: slice }),
    });
    if (!res.ok) throw new Error(`${res.status} ${res.statusText} — ${(await res.text()).slice(0, 300)}`);
    const json: any = await res.json();
    if (!json?.data?.length) throw new Error(`A válaszban nincs 'data' mező: ${JSON.stringify(json).slice(0, 300)}`);
    for (const row of json.data) {
      const v = Float32Array.from(row.embedding);
      let n = 0;
      for (const x of v) n += x * x;
      n = Math.sqrt(n) || 1;
      for (let k = 0; k < v.length; k++) v[k] /= n;
      out.push(v);
    }
    process.stderr.write(`\r  beágyazás: ${Math.min(i + batch, inputs.length)}/${inputs.length}   `);
  }
  process.stderr.write("\n");
  return out;
}

function denseSearch(qv: Float32Array, docVecs: Float32Array[], ids: string[]): Ranked {
  const scored = docVecs.map((dv, i) => {
    let s = 0;
    for (let k = 0; k < qv.length; k++) s += qv[k] * dv[k];
    return { id: ids[i], s };
  });
  scored.sort((a, b) => b.s - a.s);
  return scored.slice(0, TOPK).map((x) => x.id);
}

// ---------- fúzió és metrikák ----------
function rrf(lists: Ranked[]): Ranked {
  const acc = new Map<string, number>();
  for (const list of lists)
    list.forEach((id, i) => acc.set(id, (acc.get(id) ?? 0) + 1 / (RRF_K + i + 1)));
  return [...acc.entries()].sort((a, b) => b[1] - a[1]).slice(0, TOPK).map((x) => x[0]);
}

/**
 * Az `azonosito` kérdések (PROJ-4412, ECONNREFUSED, ...) szándékosan azonosak
 * minden nyelvben, tehát mind a 9 nyelv megfelelő dokumentuma helyes találat.
 * Nem a keresés dolga eldönteni, melyik ügyfél PROJ-4412-je kell — az a scope-szűrésé.
 */
function metrics(ranked: Ranked, expect: string, relaxed = false) {
  const want = relaxed ? expect.split(":")[1] : expect;
  const rank = relaxed
    ? ranked.findIndex((id) => id.split(":")[1] === want)
    : ranked.indexOf(expect);
  return {
    r1: rank === 0 ? 1 : 0,
    r5: rank >= 0 && rank < 5 ? 1 : 0,
    mrr: rank >= 0 ? 1 / (rank + 1) : 0,
    ndcg: rank >= 0 ? 1 / Math.log2(rank + 2) : 0, // egyetlen releváns dokumentum, IDCG = 1
  };
}

type Agg = { n: number; r1: number; r5: number; mrr: number; ndcg: number };
const emptyAgg = (): Agg => ({ n: 0, r1: 0, r5: 0, mrr: 0, ndcg: 0 });
function add(a: Agg, m: ReturnType<typeof metrics>) {
  a.n++; a.r1 += m.r1; a.r5 += m.r5; a.mrr += m.mrr; a.ndcg += m.ndcg;
}
const pct = (x: number, n: number) => (n ? ((100 * x) / n).toFixed(1).padStart(5) : "    -");
const num = (x: number, n: number) => (n ? (x / n).toFixed(3) : "  -  ");

function table(title: string, rows: Map<string, Agg>, methods: string[]) {
  console.log(`\n${title}`);
  console.log("  módszer".padEnd(20) + "  n   R@1%   R@5%    MRR    nDCG");
  console.log("  " + "-".repeat(52));
  for (const m of methods) {
    const a = rows.get(m);
    if (!a) continue;
    console.log(
      `  ${m.padEnd(18)} ${String(a.n).padStart(3)} ${pct(a.r1, a.n)}  ${pct(a.r5, a.n)}  ${num(a.mrr, a.n)}  ${num(a.ndcg, a.n)}`,
    );
  }
}

// ---------- összehasonlító mód ----------
if (FLAG("compare")) {
  const i = process.argv.indexOf("--compare");
  const [aPath, bPath] = [process.argv[i + 1], process.argv[i + 2]];
  const A = JSON.parse(readFileSync(aPath, "utf8"));
  const B = JSON.parse(readFileSync(bPath, "utf8"));
  console.log(`\nA = ${A.model}  (${aPath})`);
  console.log(`B = ${B.model}  (${bPath})\n`);
  console.log("  módszer".padEnd(20) + "   A nDCG   B nDCG    különbség");
  console.log("  " + "-".repeat(52));
  for (const m of Object.keys(A.overall)) {
    const a = A.overall[m], b = B.overall[m];
    if (!a || !b) continue;
    const av = a.ndcg / a.n, bv = b.ndcg / b.n;
    const d = bv - av;
    const mark = Math.abs(d) < 0.005 ? "" : d < 0 ? "  ← B rosszabb" : "  ← B jobb";
    console.log(`  ${m.padEnd(18)}   ${av.toFixed(4)}  ${bv.toFixed(4)}   ${(d >= 0 ? "+" : "") + d.toFixed(4)}${mark}`);
  }
  console.log("");
  process.exit(0);
}

// ---------- futtatás ----------
const endpoint = arg("endpoint", "http://192.168.50.48:8000/v1")!;
const model = arg("model", "qwen3-embedding-8b-4bit-dwq")!;
const corpusDir = arg("corpus", join(import.meta.dir, "corpus"))!;
const batch = Number(arg("batch", "16"));
const outPath = arg("out");
const skipDense = FLAG("no-dense");

const { docs, queries } = loadCorpus(corpusDir);
const langs = [...new Set(docs.map((d) => d.lang))].sort();
const qLangs = [...new Set(queries.map((q) => q.lang))].sort();
const distractors = docs.filter((d) => !qLangs.includes(d.lang)).length;
console.log(`Korpusz: ${docs.length} dokumentum (ebből ${distractors} zavaró), ${queries.length} kérdés, ${qLangs.length} nyelv (${qLangs.join(", ")})`);

const db = buildIndex(docs);
const docIds = docs.map((d) => d.id);

let docVecs: Float32Array[] = [];
let qVecs: Float32Array[] = [];
if (!skipDense) {
  console.log(`Beágyazás: ${model} @ ${endpoint}`);
  const t0 = performance.now();
  docVecs = await embed(endpoint, model, docs.map((d) => d.text), batch);
  qVecs = await embed(endpoint, model, queries.map((q) => `Instruct: ${INSTRUCT}\nQuery:${q.query}`), batch);
  console.log(`  dimenzió: ${docVecs[0].length} · idő: ${((performance.now() - t0) / 1000).toFixed(1)} mp`);
}

const METHODS = skipDense
  ? ["lex", "lexAnd", "lexs", "lexp", "tri", "lexp+tri"]
  : ["lex", "lexs", "lexp", "tri", "dense", "lex+dense", "lexp+dense", "lexp+tri+dense", "kapuzott"];

const overall = new Map<string, Agg>();
const byLang = new Map<string, Map<string, Agg>>();
const byKind = new Map<string, Map<string, Agg>>();
const bucket = (m: Map<string, Map<string, Agg>>, key: string) => {
  if (!m.has(key)) m.set(key, new Map());
  return m.get(key)!;
};

const detail: any[] = [];

queries.forEach((q, qi) => {
  const lex = ftsSearch(db, "fts_word", q.query, "exact", 2);
  // A kapu: a kérdés MINDEN szava előfordul-e együtt egy dokumentumban.
  // Ha igen, a kérdés pontos találatot vár (azonosító, parancsnév) — ilyenkor beszél a szöveges láb.
  // Ha nem, a kérdés átfogalmazás — ilyenkor csak a jelentés-keresés dolgozik.
  const lexAnd = ftsSearch(db, "fts_word", q.query, "and", 2);
  const lexs = ftsSearch(db, "fts_word", q.query, "star", 2);
  const lexp = ftsSearch(db, "fts_word", q.query, "prefix", 2);
  const tri = ftsSearch(db, "fts_tri", q.query, "sub", 3);
  const dense = skipDense ? [] : denseSearch(qVecs[qi], docVecs, docIds);
  const results: Record<string, Ranked> = {
    lex, lexs, lexp, tri, dense,
    "lexs+dense": rrf([lexs, dense]),
    // embedding-elsődleges: a szöveges láb CSAK azonosítónak látszó kérdésnél kapcsol be
    lexAnd,
    "kapuzott": lexAnd.length ? rrf([lexAnd, dense]) : dense,
    "lexp+tri": rrf([lexp, tri]),
    "lex+dense": rrf([lex, dense]),
    "lexp+dense": rrf([lexp, dense]),
    "lexp+tri+dense": rrf([lexp, tri, dense]),
  };
  // diagnosztika: hol van a helyes találat, és mit adott vissza helyette
  const rankOf = (r: Ranked) => {
    const want = q.kind === "azonosito" ? q.expect.split(":")[1] : q.expect;
    return q.kind === "azonosito"
      ? r.findIndex((id) => id.split(":")[1] === want)
      : r.indexOf(q.expect);
  };
  detail.push({
    id: q.id, lang: q.lang, kind: q.kind, query: q.query, expect: q.expect,
    kapuNyit: lexAnd.length > 0,
    rank: Object.fromEntries(METHODS.map((m) => [m, rankOf(results[m])])),
    denseTop3: dense.slice(0, 3),
  });

  for (const m of METHODS) {
    const met = metrics(results[m], q.expect, q.kind === "azonosito");
    for (const map of [overall, bucket(byLang, q.lang), bucket(byKind, q.kind)]) {
      if (!map.has(m)) map.set(m, emptyAgg());
      add(map.get(m)!, met);
    }
  }
});

table("ÖSSZESÍTETT", overall, METHODS);
for (const lang of [...byLang.keys()].sort()) table(`NYELV: ${lang}`, byLang.get(lang)!, METHODS);
for (const kind of [...byKind.keys()].sort()) table(`KÉRDÉSTÍPUS: ${kind}`, byKind.get(kind)!, METHODS);

if (outPath) {
  const plain = (m: Map<string, Agg>) => Object.fromEntries(m);
  writeFileSync(
    outPath,
    JSON.stringify(
      {
        model, endpoint, dim: docVecs[0]?.length ?? null,
        docs: docs.length, queries: queries.length, langs,
        overall: plain(overall),
        byLang: Object.fromEntries([...byLang].map(([k, v]) => [k, plain(v)])),
        byKind: Object.fromEntries([...byKind].map(([k, v]) => [k, plain(v)])),
        detail,
      },
      null, 2,
    ),
  );
  console.log(`\nMentve: ${outPath}`);
}
