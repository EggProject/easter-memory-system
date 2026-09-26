// Egy menetben: vízszintes túlcsordulás (1280/420), horgonyok, duplikált id, táblázat-oszlopok,
// szakaszszámok, D-hivatkozások, fájlközi linkek, JS-hibák.
const {chromium}=require('/home/claude/work/tools/node_modules/playwright-core');
const fs=require('fs');
const DIR='/home/claude/work/audit/';
const F=['00-dontesek','20-adatmodell','30-kereses','40-mcp','50-uzemeltetes','60-felulet','90-meresek'];
(async()=>{
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const ids={}, terkep={};
let hibak=0;
for(const f of F){
  const p=await b.newPage({viewport:{width:1280,height:900}});
  const js=[]; p.on('pageerror',e=>js.push(String(e)));
  await p.goto('file://'+DIR+f+'.html'); await p.waitForTimeout(150);
  const r=await p.evaluate(()=>{
    const idl=[...document.querySelectorAll('[id]')].map(e=>e.id);
    const ids=new Set(idl);
    const torott=[...new Set([...document.querySelectorAll('a[href^="#"]')].map(a=>a.getAttribute('href').slice(1)).filter(h=>h&&!ids.has(h)))];
    const dup=[...new Set(idl.filter((x,i)=>idl.indexOf(x)!==i))];
    const nums=[...document.querySelectorAll('h2 .num')].map(e=>+e.textContent.trim());
    const tbl=[...document.querySelectorAll('table')].map((t,i)=>{const h=t.querySelector('thead tr');const hc=h?h.children.length:0;const bad=[...t.querySelectorAll('tbody tr')].filter(r=>r.children.length!==hc).length;return bad?`tábla#${i}: ${bad} sor ≠ ${hc} oszlop`:null}).filter(Boolean);
    const d={};
    document.querySelectorAll('h2').forEach(h=>{const m=h.textContent.match(/D-(\d+)/);if(!m)return;const k='D-'+m[1];d[k]=new Set();let n=h.nextElementSibling;while(n&&n.tagName!=='H2'){n.querySelectorAll('tbody tr > td:first-child > code').forEach(c=>{if(/^\d+$/.test(c.textContent.trim()))d[k].add(c.textContent.trim())});n=n.nextElementSibling}d[k]=[...d[k]]});
    const refs=[...new Set(document.body.innerText.match(/D-\d+(?:\/\d+)?/g)||[])];
    const links=[...new Set([...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href')).filter(h=>h&&!h.startsWith('#')&&!h.startsWith('http')))];
    return {idl:[...ids],torott,dup,nums,tbl,d,refs,links};
  });
  ids[f+'.html']=new Set(r.idl); if(f==='00-dontesek') Object.assign(terkep,r.d);
  const w={}; for(const vw of [1280,420]){ await p.setViewportSize({width:vw,height:900}); await p.waitForTimeout(80); w[vw]=await p.evaluate(v=>document.documentElement.scrollWidth>v+1?document.documentElement.scrollWidth:0,vw); }
  const szam=r.nums.map((v,i)=>v!==i+1?`${i+1}. helyen ${v}`:null).filter(Boolean);
  const gond=[];
  if(r.torott.length) gond.push('TÖRÖTT HORGONY: '+r.torott.join(', '));
  if(r.dup.length) gond.push('DUPLIKÁLT ID: '+r.dup.join(', '));
  if(r.tbl.length) gond.push('TÁBLA: '+r.tbl.join(' | '));
  if(szam.length) gond.push('SZAKASZSZÁM: '+szam.join(', '));
  if(w[1280]||w[420]) gond.push(`TÚLCSORDULÁS: 1280→${w[1280]} 420→${w[420]}`);
  if(js.length) gond.push('JS: '+js.join(' | '));
  r.f=f; r.gond=gond; (global.R=global.R||[]).push(r);
  await p.close();
}
for(const r of global.R){
  const rossz=[];
  for(const x of r.refs){const [d,i]=x.split('/');if(!terkep[d])rossz.push(x+' (nincs ilyen döntés)');else if(i&&!terkep[d].includes(i))rossz.push(x+' (nincs ilyen tétel)');}
  for(const h of r.links){const [file,a]=h.split('#');if(!fs.existsSync(DIR+file))rossz.push(h+' (nincs fájl)');else if(a&&!ids[file]?.has(a))rossz.push(h+' (nincs horgony)');}
  if(rossz.length) r.gond.push('HIVATKOZÁS: '+rossz.join(', '));
  console.log(`## ${r.f.padEnd(15)} ${r.gond.length?'HIBA\n   '+r.gond.join('\n   '):'rendben — '+r.nums.length+' szakasz, '+r.refs.length+' D-hivatkozás, '+r.links.length+' fájlközi link'}`);
  hibak+=r.gond.length;
}
console.log(hibak?`\n${hibak} hiba`:'\nminden ellenőrzés rendben');
await b.close();
})();
