W = '/home/claude/work/audit/'

def rep(s, old, new, count=1):
    assert s.count(old) == count, (old[:90], s.count(old))
    return s.replace(old, new)

# ================================================================ 00
F0 = W + '00-dontesek.html'
s = open(F0, encoding='utf-8').read()

# D-04/5 megjegyzés
s = rep(s, 'azt <b>két külön fájlba</b> kell írni, két külön helyre a fában.</td>',
        'azt <b>két külön fájlba</b> kell írni, két külön helyre a fában.<br><br><span class="src"><b>2026-09-25 — a D-48 óta</b> ezt az írás sémája is kikényszeríti: a szint (projekt, közös, személyes) kötelező paraméter, alapértelmezés nélkül.</span></td>')

# D-35/4 megjegyzés — a sor végére
i = s.find('<td><b>Hét eszköz, szándékonként külön</b></td>')
j = s.find('</td>\n</tr>', i + 60)
assert i > 0 and j > i
s = s[:j] + '<br><br><span class="src"><b>2026-09-25 — a D-48 óta:</b> a <code>write_memory</code> kötelező paraméterei között a szint is ott van; a projektet nem paraméter, hanem a kapcsolat fejléce adja; a keresés hatóköre a munkamenet projektjéből jön. Részletek: <a href="40-mcp.html">Spec 40</a>.</span>' + s[j:]

# D-32/1 megjegyzés — a sor végére
i = s.find('<td><b>Előszűrés mindkét lábban</b></td>')
j = s.find('</td>\n</tr>', i + 50)
assert i > 0 and j > i
s = s[:j] + '<br><br><span class="src"><b>2026-09-25 — a D-48 óta:</b> agent-munkamenetben a jogosult halmaz tovább szűkül — az aktuális projekt, a közös tudás és a saját személyes mappa; más projekt akkor sem, ha van hozzá jog. Projekt nélküli munkamenetben: a közös tudás és a személyes mappa. A kérdés az agent-munkamenetről szólt; a felület keresésére nem vonatkozik.</span>' + s[j:]

D48 = '''<h2 id="s51"><span class="num">49</span>D-48 — A projekt a kapcsolatból jön, az írás szintje kötelező, a keresés a projektre szűkül</h2>

<p class="src">Kimondva: 2026-09-25 · Státusz: <span class="y">élő</span> · Kutatás: <code>docs/research/projekt-kontextus/</code> · Részletek: <a href="40-mcp.html">Spec 40</a> · <b>Pontosítja:</b> D-04/5, D-32/1, D-35/4</p>

<div class="card">
<p><b>Hogy melyik projektben dolgozik az agent, azt a projekt repójában élő MCP-beállítás mondja meg egy fejlécben — nem a modell. Hogy egy új bejegyzés a projektbe, a közös tudásba vagy a személyes mappába kerül, azt az agent dönti el, de kötelezően, egy kimondott paraméterrel. A keresés egy projekt-munkamenetben csak az aktuális projektet, a közös tudást és a saját személyes mappát látja.</b></p>
</div>

<p class="src"><b>A kiváltó hiány:</b> a <code>write_memory</code> kötelező adatai között nem szerepelt, hová kerül az új bejegyzés, és sehol nem volt leírva, honnan tudja a rendszer, melyik projektben dolgozik a felhasználó — pedig ez a projektcél magja: <i>„meghatarozni milyen lepeseken megy keresztul a memoria reszlet - hogyan olvassuk a session-bol es mikor hogyan injectalunk?”</i> és <i>„project-ek szeparaltak legyen es csak kulon engedellyel lathassak a masik project memoriajat”</i>.</p>

<p class="src"><b>A te válaszaid, sorban:</b> <i>„A repó MCP-beállításából”</i> · <i>„Az agent, kötelező paraméterrel”</i> · <i>„Aktuális projekt + közös + személyes”</i> — mindhárom az én ajánlásom volt.</p>

<div class="table-scroll">
<table>
<thead><tr><th>#</th><th>Tétel</th><th>Amit jelent</th></tr></thead>
<tbody>
<tr>
  <td><code>1</code></td>
  <td><b>A projekt a kapcsolatból jön</b></td>
  <td>A projekt repójában élő MCP-beállítás egy HTTP-fejlécben megadja a projekt nevét; a szerver címe mindenhol ugyanaz. Így <b>egy bejelentkezés elég</b> minden projekthez — a kliensek többsége a bejelentkezést a szervercímhez köti.<br><br>A szerver <b>minden hívásnál</b> ellenőrzi, hogy a felhasználónak van-e joga ahhoz a projekthez (D-11); ha nincs, az egységes elutasítás jön (D-35/7). A modell nem tud másik projektet megnevezni.<br><br><b>Ahol nincs ilyen fejléc</b> — például egy általános beszélgetésben —, ott nincs aktuális projekt: projektbe írni nem lehet, csak a közös tudásba és a személyes mappába.<br><br><span class="src">Miért nem a modell dönt: az MCP-szabvány szerint ez eszköztervezési kérdés (a „roots” elavult, és több kliens nem is küldi); az OWASP és az AWS ajánlása szerint a hozzáférés hatókörét a környezet kényszerítse ki, ne a modell.</span></td>
</tr>
<tr>
  <td><code>2</code></td>
  <td><b>Az írás szintje kötelező paraméter</b></td>
  <td>A <code>write_memory</code>-nál kötelező megadni, hogy a bejegyzés <b>a projektbe, a közös tudásba vagy a személyes mappába</b> kerül — alapértelmezés nincs, tehát mindig kimondott döntés születik. A projekt nevét ehhez sem az agent adja, hanem a kapcsolat (1. pont).<br><br><span class="src">Miért kell kimondatni: egy 2026-os mérés (Meta, ICLR 2026) szerint a modellek a „ki láthatja ezt” típusú döntésben gyakran hibáznak, és ugyanarra a kérésre ingadozva válaszolnak. A kötelező paraméter nem teszi pontossá a döntést, de nem engedi, hogy egy csendes alapértelmezés döntsön helyette.</span></td>
</tr>
<tr>
  <td><code>3</code></td>
  <td><b>A közös tudásba írás előbb szól, csak aztán ír</b></td>
  <td>A D-20 mintájára: ha az agent a közös tudásba írna — amit az egész cég lát —, az első hívás <b>nem ír</b>, hanem visszaszól, hogy ez mindenkinek látszani fog. Az írás csak egy második, külön paraméterrel megismételt hívásra történik meg.<br><br><span class="src">Ez az én ötletem volt; a választott válasz tartalmazta.</span></td>
</tr>
<tr>
  <td><code>4</code></td>
  <td><b>A keresés a munkamenet projektjére szűkül</b></td>
  <td>Agent-munkamenetben a keresés alapból az <b>aktuális projektet, a közös tudást és a saját személyes mappát</b> látja. <b>Más projekt találatai akkor sem jelennek meg, ha a felhasználónak joga van hozzá.</b> Projekt nélküli munkamenetben: a közös tudás és a személyes mappa.<br><br><span class="src">Ez a D-32/1 jogosult halmazát szűkíti tovább; a felület keresésére nem vonatkozik.</span></td>
</tr>
</tbody>
</table>
</div>

<div class="q">
<h4>Nyitott pontok</h4>
<p><b>A fejléc és a visszaszóló paraméter pontos neve.</b> Angol lesz (D-47); a konkrét nevet a Spec 40 véglegesítésekor teszem le javaslatként.</p>
<p><b>Felülírja-e a projektszintű beállítás a felhasználói szintűt</b> minden kliensben? A kutatás szerint háromnál (Claude Code, Codex, Gemini CLI) dokumentált; a Cursornál, az Antigravitynél és a Copilotnál nem egyértelmű. Ki kell próbálni.</p>
<p><b>A munkamenet-indító hook</b> (D-15) ugyanezt a projektet kell, hogy lássa — ez a fejlesztés előtti lista 4. pontja.</p>
</div>


'''
anchor = '<h2 id="s20"><span class="num">49</span>Feljegyzett követelmények'
s = rep(s, anchor, D48 + anchor)
s = rep(s, '<h2 id="s20"><span class="num">49</span>', '<h2 id="s20"><span class="num">50</span>')
s = rep(s, '<h2 id="s21"><span class="num">50</span>', '<h2 id="s21"><span class="num">51</span>')
s = rep(s, '<span class="chip">47 döntés, egy kivezetve</span>', '<span class="chip">48 döntés, egy kivezetve</span>')
open(F0, 'w', encoding='utf-8').write(s)

# ================================================================ 40
F4 = W + '40-mcp.html'
t = open(F4, encoding='utf-8').read()
t = rep(t, '''<div class="note">
<span class="kicker">Amit ez a D-16-tól kér</span>''', '''<div class="card">
<h4>A projekt — a kapcsolatból (2026-09-25, D-48)</h4>
<p>A token megmondja, <b>ki</b> hív. Hogy <b>melyik projektben</b>, azt a projekt repójában élő MCP-beállítás mondja meg egy <b>HTTP-fejlécben</b>. A szerver címe minden projektben ugyanaz, így egy bejelentkezés elég.</p>
<ul>
<li>A szerver <b>minden hívásnál</b> ellenőrzi, hogy a felhasználónak van-e joga a fejlécben megnevezett projekthez (D-11). Ha nincs, az egységes elutasítás jön (D-35/7).</li>
<li>A projektet <b>egyetlen eszköz sem kéri paraméterben</b> — a modell nem tud másik projektet megnevezni.</li>
<li><b>Fejléc nélkül</b> nincs aktuális projekt: projektbe írni nem lehet, a keresés a közös tudást és a személyes mappát látja.</li>
</ul>
<p class="src">A fejléc pontos neve még nincs kimondva; angol lesz (D-47). Az MCP-szabvány szerint ez eszköztervezési kérdés — a „roots” elavult, és több kliens nem is küldi (<code>docs/research/projekt-kontextus/</code>).</p>
</div>

<div class="note">
<span class="kicker">Amit ez a D-16-tól kér</span>''')
t = rep(t, '''  <td>a lekérdezés</td>
  <td><b>Teljes tartalom</b>, találatonként a bejegyzés nevével és a helyezésével. Korlátozott találatszám, lapozással.</td>''',
        '''  <td>a lekérdezés</td>
  <td><b>Teljes tartalom</b>, találatonként a bejegyzés nevével és a helyezésével. Korlátozott találatszám, lapozással.<br><span class="src">2026-09-25 (D-48): a hatókör az aktuális projekt, a közös tudás és a saját személyes mappa — nem paraméter, a kapcsolatból jön.</span></td>''')
t = rep(t, '''  <td>a tartalom, a kategória, az <b>indoklás</b>, a <code>prompt_version</code></td>''',
        '''  <td>a tartalom, a kategória, az <b>indoklás</b>, a <code>prompt_version</code>, és <b>2026-09-25 óta a szint</b>: projekt, közös tudás vagy személyes mappa (D-48). A közös tudásba írás előbb visszaszól, és csak egy második, külön paraméterrel megismételt hívás ír.</td>''')
t = rep(t, '''<tr>
  <td><b>Kell-e erőforrásként (resource) is kiajánlani bármit?</b></td>''', '''<tr>
  <td><b>A projekt-fejléc és a visszaszóló paraméter neve</b> (D-48)</td>
  <td class="m"><b>nyitva</b> — angol lesz (D-47); javaslatként teszem le.</td>
</tr>
<tr>
  <td><b>Felülírja-e a projektszintű MCP-beállítás a felhasználói szintűt?</b></td>
  <td class="m"><b>nyitva, kipróbálandó</b> — a Claude Code-nál, a Codexnél és a Gemini CLI-nél dokumentált; a Cursornál, az Antigravitynél és a Copilotnál nem egyértelmű (<code>docs/research/projekt-kontextus/</code>).</td>
</tr>
<tr>
  <td><b>Kell-e erőforrásként (resource) is kiajánlani bármit?</b></td>''')
open(F4, 'w', encoding='utf-8').write(t)

# ================================================================ 30
F3 = W + '30-kereses.html'
u = open(F3, encoding='utf-8').read()
u = rep(u, '''<div class="card">
<p><b>A jogosult halmaz a keresés ELŐTT áll elő, és mindkét láb csak azon fut. Nem a rangsorolás után szűrünk.</b></p>
</div>''', '''<div class="card">
<p><b>A jogosult halmaz a keresés ELŐTT áll elő, és mindkét láb csak azon fut. Nem a rangsorolás után szűrünk.</b></p>
</div>

<p class="src"><b>2026-09-25 — a D-48 óta:</b> agent-munkamenetben a jogosult halmaz szűkebb: az aktuális projekt (a kapcsolat fejlécéből), a közös tudás és a saját személyes mappa. Más projekt akkor sem, ha van hozzá jog. Projekt nélküli munkamenetben: a közös tudás és a személyes mappa. A felület keresését ez nem érinti.</p>''')
open(F3, 'w', encoding='utf-8').write(u)
print('ok')
