// Kontrollos kísérlet: ugyanaz az író, ugyanannyi ideig — mentés nélkül (kontroll) és VACUUM INTO alatt (kísérlet).
// Hipotézis: a VACUUM INTO nyitva tartott olvasó tranzakciója megakadályozza a WAL checkpointot.
import { rmSync, statSync, mkdirSync } from "node:fs";
import { join } from "node:path";
const D = join(import.meta.dir, "adat"); mkdirSync(D, { recursive: true });
const BUN = process.execPath, S = (f: string) => join(import.meta.dir, f);
const mb = (b: number) => (b / 1048576).toFixed(1);
const F = join(D, "w.sqlite"), KI = join(D, "w-ki.sqlite");
const torol = () => { for (const v of ["", "-wal", "-shm"]) { try { rmSync(F + v); } catch {} } try { rmSync(KI); } catch {} };

async function menet(vacuumot: boolean) {
  torol();
  Bun.spawnSync([BUN, S("epit.ts"), F, "200"]);
  const wal = () => { try { return statSync(F + "-wal").size; } catch { return 0; } };
  const minta: any[] = [];
  const iro = Bun.spawn([BUN, S("iro.ts"), F], { stdout: "pipe" });
  (async () => { const d = new TextDecoder(); for await (const c of iro.stdout as any) for (const s of d.decode(c).trim().split("\n")) if (s) minta.push(JSON.parse(s)); })();
  const ido: any[] = []; let fut = true;
  (async () => { while (fut) { ido.push({ t: Date.now(), wal: wal() }); await Bun.sleep(40); } })();
  await Bun.sleep(5000);
  const k = Date.now(); let vms: number;
  if (vacuumot) { const p = Bun.spawnSync([BUN, S("meres.ts"), "vacuum", F, KI]); vms = JSON.parse(new TextDecoder().decode(p.stdout).trim()).ms; }
  else { await Bun.sleep(1300); vms = 1300; }
  const v = Date.now();
  await Bun.sleep(2500);
  iro.kill("SIGTERM"); await iro.exited; fut = false;
  const abl = (a: number, b: number) => ido.filter(x => x.t >= a && x.t <= b).map(x => x.wal);
  const mx = (a: number[]) => a.length ? Math.max(...a) : 0;
  const rate = (a: number, b: number) => { const m = minta.filter(x => x.t >= a && x.t <= b); return m.length < 2 ? NaN : (m[m.length - 1].n - m[0].n) / ((m[m.length - 1].t - m[0].t) / 1000); };
  const hiba = minta.length ? minta[minta.length - 1].hiba : NaN;
  return { vms, e: mx(abl(k - 4000, k)), a: mx(abl(k, v)), u: mx(abl(v, v + 2500)), r: rate(k, v) / rate(k - 4000, k), hiba };
}
console.log(`Bun ${Bun.version}`);
console.log("futás            ablak  | WAL előtte | WAL alatta | WAL utána | író aránya | író-hiba");
for (const [nev, vac] of [["KONTROLL", false], ["KÍSÉRLET", true]] as [string, boolean][]) {
  for (let i = 1; i <= 3; i++) {
    const r = await menet(vac);
    console.log(`${nev} #${i} ${String(r.vms).padStart(6)} ms | ${mb(r.e).padStart(7)} MB | ${mb(r.a).padStart(7)} MB | ${mb(r.u).padStart(6)} MB | ${(r.r * 100).toFixed(0).padStart(6)}%    | ${r.hiba}`);
  }
}
torol();
