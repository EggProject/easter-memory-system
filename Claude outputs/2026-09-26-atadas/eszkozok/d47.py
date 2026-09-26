W = '/home/claude/work/audit/'

def rep(s, old, new, count=1):
    assert s.count(old) == count, (old[:90], s.count(old))
    return s.replace(old, new)

# ================================================================ 00
F0 = W + '00-dontesek.html'
s = open(F0, encoding='utf-8').read()

# D-04 példa: dátumozott megjegyzés, a példa marad
s = rep(s, '''kategoriak/szemelyes/munkamodszer.md    → mindenhol látszik</code></pre>''',
        '''kategoriak/szemelyes/munkamodszer.md    → mindenhol látszik</code></pre>

<p class="src"><b>2026-09-25 — megjegyzés:</b> a példa a 2026-09-05-i átnevezés előtti mappaneveket mutatja. A mai gyökerek: <code>projects/</code>, <code>knowledge/</code>, <code>personal/</code> (D-08).</p>''')

# D-08 fa
s = rep(s, '<pre><code>memoria/\n', '<pre><code>memory/\n')
# D-12 ábrák
s = rep(s, 'naplo/*.jsonl                     NEM AZ       audit napló — fájl, nem adatbázis (D-18)</code></pre>',
        'audit/*.jsonl                     NEM AZ       audit napló — fájl, nem adatbázis (D-18)</code></pre>')
s = rep(s, 'naplo/*.jsonl      NEM AZ       audit napló — fájl, nem adatbázis (D-18)</code></pre>',
        'audit/*.jsonl      NEM AZ       audit napló — fájl, nem adatbázis (D-18)</code></pre>')
# D-14 szerver-ábra
s = rep(s, '├── memoria/         a fájlok — csak a szerver írja', '├── memory/          a fájlok — csak a szerver írja')
s = rep(s, '├── adatbázis/       ParadeDB, a szerver saját kötetén (D-43)', '├── db/              ParadeDB, a szerver saját kötetén (D-43)')
# D-16 compose és parancsok
s = rep(s, '  beagyazo   készen kapható szolgáltatás — csak számol,', '  embedder   készen kapható szolgáltatás — csak számol,')
s = rep(s, '  adatbazis  ParadeDB — Postgres + pg_search + pgvector,', '  db         ParadeDB — Postgres + pg_search + pgvector,')
s = rep(s, '  szolgal        folyamatosan fut', '  serve          folyamatosan fut')
s = rep(s, '  karbantart     kézi indítás — ugyanaz a kód, egyszer lefut</code></pre>', '  maintain       kézi indítás — ugyanaz a kód, egyszer lefut</code></pre>')
s = rep(s, 'A kézi <code>karbantart</code> parancs ugyanezt a kört futtatja le egyszer, majd kilép.',
        'A kézi <code>maintain</code> parancs ugyanezt a kört futtatja le egyszer, majd kilép.')
# D-18 ábra
s = rep(s, '<pre><code>naplo/\n', '<pre><code>audit/\n')
# D-25, D-31
s = rep(s, '  • szerveren:  <b>karbantart admin-link</b>  → új egyszeri link</code></pre>',
        '  • szerveren:  <b>maintain admin-link</b>  → új egyszeri link</code></pre>')
s = rep(s, 'Erre a D-25 parancssori útja marad: <b><code>karbantart admin-link</code></b> → új egyszeri beállító link.',
        'Erre a D-25 parancssori útja marad: <b><code>maintain admin-link</code></b> → új egyszeri beállító link.')
# D-43/9 sémanevek
s = rep(s, '<br><br><span class="src">A sémák neve még nincs kimondva.</span></td>',
        '<br><br><span class="src"><b>2026-09-25: a nevek kimondva (D-47)</b> — <code>derived</code> (eldobható), <code>cache</code> (drágán eldobható), <code>core</code> (pótolhatatlan). <b>Korábban:</b> A sémák neve még nincs kimondva.</span></td>')
# D-46/6 lezárva
s = rep(s, 'Ez a D-46 előtti ellentmondás; hogy mi legyen angol (mappák, konténernevek, parancsok), azt külön kérdezem.</td>',
        'Ez a D-46 előtti ellentmondás; hogy mi legyen angol (mappák, konténernevek, parancsok), azt külön kérdezem. <span class="src"><b>Lezárva 2026-09-25-én: D-47</b> — minden rendszernév angol.</span></td>')

D47 = '''<h2 id="s50"><span class="num">48</span>D-47 — A rendszer minden saját neve angol</h2>

<p class="src">Kimondva: 2026-09-25 · Státusz: <span class="y">élő</span> · <b>Pontosítja:</b> a D-08-at — a Spec 20 azt csak a markdown mezőnevekre olvasta · Kiváltója: D-46</p>

<div class="card">
<p><b>A rendszer minden saját neve angol: a mappák, a konténerek, a parancsok, az adatbázis-sémák és a táblák. A projekt dokumentumainak (<code>docs/</code>) és mérőszkriptjeinek (<code>bench/</code>) nevét ez nem érinti.</b></p>
</div>

<p class="src"><b>A te válaszaid:</b> az elvre <i>„Minden rendszernév angol”</i>, a konkrét nevekre <i>„Rövid nevek”</i> — mindkettő az én ajánlásom volt, és a neveket is én javasoltam. A D-08 szövege már eddig is ezt mondta: <i>„Minden azonosító, amit a rendszer maga definiál és fájlba ír, angol.”</i></p>

<div class="table-scroll">
<table>
<thead><tr><th>Mi</th><th>Korábban</th><th>Mostantól</th></tr></thead>
<tbody>
<tr><td>A markdown fa gyökere</td><td><code>memoria/</code></td><td><code>memory/</code></td></tr>
<tr><td>Az audit napló mappája (D-18)</td><td><code>naplo/</code></td><td><code>audit/</code></td></tr>
<tr><td>Az üzemeltetési napló mappája (D-40)</td><td>nem volt neve</td><td><code>logs/</code></td></tr>
<tr><td>A ParadeDB kötete</td><td><code>adatbázis/</code></td><td><code>db/</code></td></tr>
<tr><td>A program konténere</td><td><code>app</code></td><td><code>app</code> — marad</td></tr>
<tr><td>A beágyazó konténere</td><td><code>beagyazo</code></td><td><code>embedder</code></td></tr>
<tr><td>Az adatbázis konténere</td><td><code>adatbazis</code></td><td><code>db</code></td></tr>
<tr><td>A folyamatosan futó üzemmód</td><td><code>szolgal</code></td><td><code>serve</code></td></tr>
<tr><td>A kézi karbantartó futás</td><td><code>karbantart</code></td><td><code>maintain</code></td></tr>
<tr><td>Új egyszeri admin-link</td><td><code>karbantart admin-link</code></td><td><code>maintain admin-link</code></td></tr>
<tr><td>Az eldobható séma (D-43/9)</td><td>nem volt neve</td><td><code>derived</code></td></tr>
<tr><td>A drágán eldobható séma</td><td>nem volt neve</td><td><code>cache</code></td></tr>
<tr><td>A pótolhatatlan séma</td><td>nem volt neve</td><td><code>core</code></td></tr>
</tbody>
</table>
</div>

<p class="src"><b>Ami még hátravan:</b> a táblák neve a táblaszerkezettel együtt kerül elő (a fejlesztés előtti lista 5. pontja), szintén angolul. A „Korábban” megjegyzésekben a régi nevek történetként maradnak.</p>


'''
anchor = '<h2 id="s20"><span class="num">48</span>Feljegyzett követelmények'
s = rep(s, anchor, D47 + anchor)
s = rep(s, '<h2 id="s20"><span class="num">48</span>', '<h2 id="s20"><span class="num">49</span>')
s = rep(s, '<h2 id="s21"><span class="num">49</span>', '<h2 id="s21"><span class="num">50</span>')
s = rep(s, '<span class="chip">46 döntés, egy kivezetve</span>', '<span class="chip">47 döntés, egy kivezetve</span>')
open(F0, 'w', encoding='utf-8').write(s)

# ================================================================ 20
F2 = W + '20-adatmodell.html'
u = open(F2, encoding='utf-8').read()
u = rep(u, '<pre><code>memoria/\n', '<pre><code>memory/\n', count=2)
u = rep(u, 'naplo/*.jsonl                     NEM AZ       audit napló — fájl, nem adatbázis</code></pre>',
        'audit/*.jsonl                     NEM AZ       audit napló — fájl, nem adatbázis</code></pre>')
u = rep(u, 'naplo/*.jsonl      NEM AZ       audit napló — fájl, nem adatbázis</code></pre>',
        'audit/*.jsonl      NEM AZ       audit napló — fájl, nem adatbázis</code></pre>')
u = rep(u, '<td><code>naplo/*.jsonl</code></td>', '<td><code>audit/*.jsonl</code></td>', count=2)
u = rep(u, '<pre><code>naplo/\n', '<pre><code>audit/\n')
u = rep(u, '<td><code>memoria/**</code></td>', '<td><code>memory/**</code></td>')
u = rep(u, '''  <td><b>A rendszerfájlok nevei magyarok, a fáé angolok.</b></td>
  <td class="m"><b>nyitva</b> — ''', '''  <td><b>A rendszerfájlok nevei magyarok, a fáé angolok.</b></td>
  <td class="y"><b>lezárva 2026-09-25-én (D-47)</b> — minden rendszernév angol: <code>memory/</code>, <code>audit/</code>, <code>logs/</code>, <code>db/</code>; a sémák <code>derived</code>, <code>cache</code>, <code>core</code>. A táblanevek a táblaszerkezettel együtt jönnek. <span class="src"><b>Korábban:</b> nyitva — ''')
u = rep(u, 'A <code>memoria/</code> és a <code>naplo/</code> ezzel ellentétes. Döntésre vár, egyenként kérdezve.</span></td>',
        'A <code>memoria/</code> és a <code>naplo/</code> ezzel ellentétes. Döntésre vár, egyenként kérdezve.</span></span></td>')
u = rep(u, '— külön Postgres-sémával (D-43/9). A sémák neve még nincs kimondva.</td>',
        '— külön Postgres-sémával (D-43/9). <b>2026-09-25: a nevek</b> <code>derived</code>, <code>cache</code>, <code>core</code> (D-47). <span class="src"><b>Korábban:</b> A sémák neve még nincs kimondva.</span></td>')
open(F2, 'w', encoding='utf-8').write(u)

# ================================================================ 60
F6 = W + '60-felulet.html'
v = open(F6, encoding='utf-8').read()
v = rep(v, 'karbantart admin-link', 'maintain admin-link')
open(F6, 'w', encoding='utf-8').write(v)
print('ok')
