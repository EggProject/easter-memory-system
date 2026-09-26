W = '/home/claude/work/audit/'

def rep(s, old, new, count=1):
    assert s.count(old) == count, (old[:90], s.count(old))
    return s.replace(old, new)

# ================================================================ 00
F0 = W + '00-dontesek.html'
s = open(F0, encoding='utf-8').read()

# D-01 fejléc + D-01/3
s = rep(s, '<p class="src">Kimondva: 2026-08-20 · Státusz: <span class="y">élő</span> · <b>Módosítva: 2026-09-22 (D-43)</b></p>',
        '<p class="src">Kimondva: 2026-08-20 · Státusz: <span class="y">élő</span> · <b>Módosítva: 2026-09-22 (D-43), 2026-09-25 (D-46)</b></p>')
s = rep(s, '''  <td><b>Minden nyelv, kiemelten a magyar</b></td>
  <td>A rendszernek nyelvfüggetlennek kell lennie. A <b>magyar kiemelt cél</b>, de nem az egyetlen.</td>''',
'''  <td><b>Angol elsődleges, magyar támogatott</b></td>
  <td><span class="src"><b>2026-09-25-én átírva — a D-46 következménye.</b> A te szavaiddal: „Angol nyelv a prior! magyar nyelvet is tamogatni kell tobbi nyelv most nem erdekes”.</span><br>Az <b>angol az elsődleges</b> nyelv, a <b>magyart támogatni kell</b>. A többi nyelv most nem szempont.<br><br><span class="src"><b>Korábban:</b> Minden nyelv, kiemelten a magyar — A rendszernek nyelvfüggetlennek kell lennie. A <b>magyar kiemelt cél</b>, de nem az egyetlen.</span></td>''')

# D-30 kockázati mondat
s = rep(s, '<p><b>A második nyelv csendben elavul.</b> Ha az angol katalógus lemarad, azt senki nem veszi észre, aki magyarul használja.',
        '<p><b>A második nyelv csendben elavul.</b> Ha az angol katalógus lemarad, azt senki nem veszi észre, aki magyarul használja. <span class="src"><b>2026-09-25 — a D-46 óta</b> az angol az elsődleges; a kockázat iránya megfordulhat (a magyar katalógus maradhat le). A néma visszaesés tilalma nyelvtől független, áll. Hogy melyik katalógus a forrás, nincs kimondva.</span>')

# D-43 CJK-megjegyzés
s = rep(s, 'a 30-as spec CJK-döntése azért nem hozott be tokenizálót, mert az FTS5-ben nincs ICU; a ParadeDB-ben van beépített CJK-tokenizáló.',
        'a 30-as spec CJK-döntése azért nem hozott be tokenizálót, mert az FTS5-ben nincs ICU; a ParadeDB-ben van beépített CJK-tokenizáló. <span class="src">2026-09-25 óta tárgytalan: a D-46 szerint a kínai, japán és koreai nyelv most nem cél.</span>')

D46 = '''<h2 id="s49"><span class="num">47</span>D-46 — Angol az elsődleges nyelv, a magyar támogatott</h2>

<p class="src">Kimondva: 2026-09-25 · Státusz: <span class="y">élő</span> · <b>Felülírja:</b> D-01/3 · Hatáselemzés: a döntés kimondása után, tételesen átnézve mind a hét dokumentum</p>

<div class="card">
<p><b>Az angol az elsődleges nyelv. A magyart támogatni kell. A többi nyelv most nem szempont.</b></p>
</div>

<p class="src"><b>A tulajdonos szavai szó szerint:</b> <i>„Angol nyelv a prior! magyar nyelvet is tamogatni kell tobbi nyelv most nem erdekes”</i>. A mondat arra a listára volt válasz, amelyben a nyitott pontok között a CJK-tokenizáló és a rendszerfájlok nevének nyelve szerepelt.</p>

<p class="src"><b>Az alábbi tábla az én hatáselemzésem, nem döntés.</b> Ami benne „tárgytalan”, az közvetlenül a mondatodból következik; ami „jelezve”, arról még dönteni kell — egyenként kérdezem.</p>

<div class="table-scroll">
<table>
<thead><tr><th>#</th><th>Mit érint</th><th>Mi történik vele</th></tr></thead>
<tbody>
<tr>
  <td><code>1</code></td>
  <td><b>D-01/3</b></td>
  <td><b>Átírva</b> — a régi szöveg „Korábban”-ként mellette áll.</td>
</tr>
<tr>
  <td><code>2</code></td>
  <td><b>Kínai, japán, koreai (CJK)</b> — Spec 30, 09. szakasz és a nyitott pont; a D-43 záró megjegyzése; mérések 13. szakasz</td>
  <td class="m"><b>Tárgytalan</b> — ezek a nyelvek most nem célok. A mérési számok történeti adatként maradnak.</td>
</tr>
<tr>
  <td><code>3</code></td>
  <td><b>D-02 — a kapuzott keresés</b></td>
  <td class="n"><b>Jelezve, nem újranyitva: az indok gyengül.</b> Az alátámasztó mérés kilencnyelvű; összesítve a kapuzott <b>0,855</b>, a vak fúzió <b>0,851</b>. Nyelvenként viszont <b>angolon a vak fúzió nyer, a táblázat legnagyobb különbségével (+0,088)</b>, magyaron a kapuzott (+0,074). A mérőkészletet a D-43 miatt amúgy is újra kell futtatni ParadeDB-n — ott kell kimérni angol és magyar korpuszon, és az döntsön.</td>
</tr>
<tr>
  <td><code>4</code></td>
  <td><b>A beágyazó modell</b></td>
  <td><b>Jelezve:</b> a dokumentumokban csak magyar külső mérés szól mellette. Angolra nincs külső alátámasztás; a saját futásunk angol értékei nem alkalmasak a nyelvek összevetésére (mérések, 06.). Mérni kell.</td>
</tr>
<tr>
  <td><code>5</code></td>
  <td><b>D-30 — a felület nyelve</b></td>
  <td>A felület továbbra is magyar és angol. <b>Jelezve:</b> melyik katalógus a forrás, és a kockázati mondat iránya (a D-30-nál dátumozott megjegyzés).</td>
</tr>
<tr>
  <td><code>6</code></td>
  <td><b>A rendszer saját fájl- és mappanevei</b></td>
  <td><b>Jelezve:</b> a D-08 szó szerint: <i>„Minden azonosító, amit a rendszer maga definiál és fájlba ír, angol.”</i> A Spec 20 ezt szűkebben olvasta (csak a markdown mezőnevekre), ezért áll ma magyar néven például a <code>memoria/</code> és a <code>naplo/</code>. Ez a D-46 előtti ellentmondás; hogy mi legyen angol (mappák, konténernevek, parancsok), azt külön kérdezem.</td>
</tr>
<tr>
  <td><code>7</code></td>
  <td><b>A mérések kilencnyelvű számai</b></td>
  <td>Maradnak, történeti adatként — a mérési dokumentum saját szabálya szerint nem törlünk.</td>
</tr>
</tbody>
</table>
</div>


'''
anchor = '<h2 id="s20"><span class="num">47</span>Feljegyzett követelmények'
s = rep(s, anchor, D46 + anchor)
s = rep(s, '<h2 id="s20"><span class="num">47</span>', '<h2 id="s20"><span class="num">48</span>')
s = rep(s, '<h2 id="s21"><span class="num">48</span>', '<h2 id="s21"><span class="num">49</span>')
s = rep(s, '<span class="chip">45 döntés, egy kivezetve</span>', '<span class="chip">46 döntés, egy kivezetve</span>')
open(F0, 'w', encoding='utf-8').write(s)

# ================================================================ 30
F3 = W + '30-kereses.html'
t = open(F3, encoding='utf-8').read()
t = rep(t, '''<h2 id="s9"><span class="num">09</span>Szóköz nélküli írásrendszerek</h2>

<div class="warn">''', '''<h2 id="s9"><span class="num">09</span>Szóköz nélküli írásrendszerek</h2>

<p class="src"><b>2026-09-25 óta tárgytalan (D-46):</b> a kínai, japán és koreai nyelv most nem cél. A szakasz történeti.</p>

<div class="warn">''')
t = rep(t, '''  <td><b>Kínai és más szóköz nélküli írásrendszerek.</b></td>
  <td class="m"><b>nyitva</b> — ''', '''  <td><b>Kínai és más szóköz nélküli írásrendszerek.</b></td>
  <td><b>tárgytalan 2026-09-25 óta (D-46)</b> — ezek a nyelvek most nem célok. <span class="src"><b>Korábban:</b> nyitva — ''')
t = rep(t, 'tehát a 06-os szakasz szerint egy beágyazó-kiesés ezeken a nyelveken teljes keresés-kiesést jelent.</td>',
        'tehát a 06-os szakasz szerint egy beágyazó-kiesés ezeken a nyelveken teljes keresés-kiesést jelent.</span></td>')
open(F3, 'w', encoding='utf-8').write(t)

# ================================================================ 20
F2 = W + '20-adatmodell.html'
u = open(F2, encoding='utf-8').read()
u = rep(u, 'a táblanevek még nincsenek kimondva.</span></td>',
        'a táblanevek még nincsenek kimondva.</span><br><span class="src"><b>2026-09-25 — a D-46 kapcsán jelezve:</b> a D-08 szó szerint „Minden azonosító, amit a rendszer maga definiál és fájlba ír, angol.” — tehát nem csak a markdown mezőnevekre szól. A <code>memoria/</code> és a <code>naplo/</code> ezzel ellentétes. Döntésre vár, egyenként kérdezve.</span></td>')
open(F2, 'w', encoding='utf-8').write(u)

# ================================================================ 90
F9 = W + '90-meresek.html'
v = open(F9, encoding='utf-8').read()
v = rep(v, 'A magyar — a fő cél szerint kiemelt nyelv — a legnagyobb különbséggel a kapuzott mellett szól, és ott a vak fúzió még a tiszta jelentés-keresésnél is rosszabb.</p>',
        'A magyar — a fő cél szerint kiemelt nyelv — a legnagyobb különbséggel a kapuzott mellett szól, és ott a vak fúzió még a tiszta jelentés-keresésnél is rosszabb.</p>\n\n<p class="src"><b>2026-09-25 — a D-46 óta az angol az elsődleges nyelv, a magyar támogatott.</b> A fenti mondat premisszája („a fő cél szerint kiemelt nyelv”) ezzel megváltozott. <b>Az angol sorban a vak fúzió nyer, a táblázat legnagyobb különbségével (+0,088).</b> A D-02 indoka ezzel gyengül; nem nyitom újra, de a ParadeDB-s újramérést angol és magyar korpuszon kell elvégezni, és az döntsön. A többi hét nyelv sora történeti adat.</p>')
v = rep(v, '<p><b>A tokenizáló-váltás ára a saját korpuszunkon.</b> Ha egyszer mégis kell CJK-támogatás,',
        '<p><b>A tokenizáló-váltás ára a saját korpuszunkon.</b> <span class="src">2026-09-25 óta tárgytalan (D-46: a CJK-nyelvek most nem célok).</span> Ha egyszer mégis kell CJK-támogatás,')
open(F9, 'w', encoding='utf-8').write(v)
print('ok')
