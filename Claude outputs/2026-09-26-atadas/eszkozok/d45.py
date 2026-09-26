W = '/home/claude/work/audit/'

def rep(s, old, new, count=1):
    assert s.count(old) == count, (old[:90], s.count(old))
    return s.replace(old, new)

# ---------------------------------------------------------------- 00
F0 = W + '00-dontesek.html'
s = open(F0, encoding='utf-8').read()

D45 = '''<h2 id="s48"><span class="num">46</span>D-45 — A Jev most nem kerül be</h2>

<p class="src">Kimondva: 2026-09-25 · Státusz: <span class="y">élő</span> · A számok: <a href="90-meresek.html#s21">mérések, 20. szakasz</a> · Kutatás: <code>docs/research/jev/</code></p>

<div class="card">
<p><b>A TypeSafe AI „Jev” nevű döntési modellje most egyik funkciónál sem kerül a rendszerbe. A kutatás és a kapcsolható beépítés mintája eltárolva marad arra az esetre, ha újranézzük.</b></p>
</div>

<p class="src"><b>A tulajdonos kérése szó szerint:</b> <i>„van egy uj "Jev" nevezetu dontest tamogato baromi gyors model, vegeztess deep research -t hogy megeri-e nekunk barmelyik funkcional hasznalni? peldaul akar kategoria dontes vagy ellenorzes uj jegyzet irasnal stb nem tudom, vizsgaljuk ki, de ne eroltessuk csak azert mert kerem, ha viszont erdemes lehet hasznalni akkor is ugy tervezzuk bele a rendeszerbe hogy kapcsoloval mukodjon, lehessen kezelni ha elfogy a balance es ha nem elerheto auto vissza allunk adott helyen a jelenlegi modszerre”</i>. A kutatás után a választott válasz: <i>„Most ne építsük be”</i> — ez volt az én ajánlásom is.</p>

<div class="table-scroll">
<table>
<thead><tr><th>#</th><th>Tétel</th><th>Amit jelent</th></tr></thead>
<tbody>
<tr>
  <td><code>1</code></td>
  <td><b>Mi a Jev</b></td>
  <td>A TypeSafe AI modellje, 2026-09-15-én jelent meg. <b>Nem ír szöveget:</b> egy helyzetleírásra és tipizált kérdésekre felel — választ egy listából, pontoz, vagy igent/nemet mond —, valószínűséggel. Csak felhős API, az USA-ban fut, a súlyai zártak. Nagyon olcsó, és a gyártó szerint nagyon gyors.</td>
</tr>
<tr>
  <td><code>2</code></td>
  <td><b>A fő ok: nálunk nincs mit kiváltania</b></td>
  <td>A Jev ott ad sokat, ahol egy rendszer maga hív nagy nyelvi modellt gyakori, egyszerű döntésekre. Nálunk ilyen hívás nincs: minden tartalmi döntést vagy a hívó ágens (Claude, Codex) hoz, vagy ember — a szerver szándékosan nem ítél (D-01/2). A Jev tehát csak egy <b>második döntéshozó</b> lehetne, és a független mérések szerint gyengébb a hívó ágensnél: egy 77 kategóriás osztályozási teszten <b>81,0%</b>, a Claude Opus 5 <b>84,4%</b>.</td>
</tr>
<tr>
  <td><code>3</code></td>
  <td><b>Funkciónként</b></td>
  <td><b>Kategória-döntés:</b> nem éri meg. Ma egy erősebb modell dönt; arra, hogy egy gyengébb utólagos ellenőrzése javítana, nincs számszerű forrás. A D-01/2 szó szerint kizárja: „se kategória-besorolást”.<br><br><b>Ellenőrzés íráskor</b> (ellentmond-e valaminek): gyenge. A hívó ágens a hasonló bejegyzéseket a D-20 válaszában amúgy is megkapja, és erősebb bíró. A gyártó saját dokumentációjában van példa arra, hogy ugyanarra a tényre két kérdésformában ellentétes választ ad.<br><br><b>Titokszűrés:</b> nem. Nincs tartalom-kapu (D-38), és az ellenőrzéshez éppen a védendő szöveget kellene kiküldeni.<br><br><b>Keresési találatok rangsorolása:</b> erre van a legtöbb bizonyíték, de minden keresés tartalma kimenne, minden keresés lassulna, és a hatást a saját mérőkészletünkön kellene kimérni.</td>
</tr>
<tr>
  <td><code>4</code></td>
  <td><b>Ami minden funkcióra áll</b></td>
  <td><b>Adat:</b> csak az USA-ban fut; fix megőrzési idő nincs; a „semmit nem őrzünk meg” (ZDR) vállalás a gyártó hivatalos dokumentumaiban nem szerepel, csak két közvetítő (OpenRouter, Vercel) adja.<br><b>Érettség:</b> tíznapos, „preview” termék, szolgáltatási garancia (SLA) nélkül; a korlátok előzetes értesítés nélkül változhatnak.<br><b>Nyelv:</b> magyarra semmilyen mérés nincs.<br><b>Saját döntéseink:</b> D-01/2 (csak beágyazó modell), D-01/8 (kevés külső függőség), D-17/4 (ember dönt).</td>
</tr>
<tr>
  <td><code>5</code></td>
  <td><b>Ha egyszer mégis: így kell beépíteni</b></td>
  <td>A te feltételeid: kapcsolóval működjön, kezelje az elfogyó keretet, és ha nem elérhető, az adott helyen automatikusan álljon vissza a mostani módszerre. A kutatás szerinti bevett minta hozzá: kapcsoló konfigurációból; áramkör-megszakító (circuit breaker); minden hívásra határidő; kétszintű költségkeret (előbb jelzés, aztán megállás); a visszaállás <b>soha nem néma</b> — naplóba és az állapot-nézetre kerül; és először <b>árnyék-mód</b>: a külső modell számol és naplóz, de a döntést a mostani módszer hozza, és a kettőt összevetjük.</td>
</tr>
<tr>
  <td><code>6</code></td>
  <td><b>Mikor nézzük újra</b></td>
  <td>Ha van EU-s futtatás vagy hivatalos ZDR; ha van magyar mérés; ha van SLA; és ha lesz a rendszerben olyan pont, ahol a szervernek ágens nélkül kell döntenie. <span class="src">A feltételeket én javasoltam; a választott válasz tartalmazta őket.</span></td>
</tr>
</tbody>
</table>
</div>


'''

anchor = '<h2 id="s20"><span class="num">46</span>Feljegyzett követelmények'
s = rep(s, anchor, D45 + anchor)
s = rep(s, '<h2 id="s20"><span class="num">46</span>', '<h2 id="s20"><span class="num">47</span>')
s = rep(s, '<h2 id="s21"><span class="num">47</span>', '<h2 id="s21"><span class="num">48</span>')
s = rep(s, '<span class="chip">frissítve: 2026-09-24</span>', '<span class="chip">frissítve: 2026-09-25</span>')
s = rep(s, '<span class="chip">44 döntés, egy kivezetve</span>', '<span class="chip">45 döntés, egy kivezetve</span>')
# D-44 nyitott pontja lezárva
s = rep(s, '<p><b>A projektleírásban még ott a „dream funkció”.</b> A claude.ai-os projekt céljai között szerepel; azt csak te tudod kivenni.</p>',
        '<p class="src"><b>A projektleírás — lezárva 2026-09-25-én.</b> A claude.ai-os projekt céljai között a „dream funkcio” mellé odaírtad: <i>„[nem kell implementalni, arra jutottunk hogy nem jo]”</i>.</p>')
open(F0, 'w', encoding='utf-8').write(s)

# ---------------------------------------------------------------- 90
F9 = W + '90-meresek.html'
t = open(F9, encoding='utf-8').read()

S21 = '''<h2 id="s21"><span class="num">20</span>Jev — amiért most nem építjük be</h2>

<p>Ez a szakasz a <b>D-45</b> mögötti számokat tartalmazza. A kampány: <b>egy azonosító kör, hat Sonnet kereső párhuzamosan, utána három ellenőrző</b>, mind az Exa keresővel — a kivonat a <code>docs/research/jev/</code> mappában. A döntés az lett, hogy <b>a Jev most nem kerül be</b>.</p>

<h3>Pontosság</h3>

<div class="table-scroll">
<table>
<thead><tr><th>Amit mértek</th><th>Érték</th><th>Forrás és feltétel</th></tr></thead>
<tbody>
<tr><td>Osztályozás 77 kategóriára (Banking77)</td><td>Jev <b>81,0%</b> · Claude Opus 5 <b>84,4%</b></td><td>OpenRouter blog, 2026-09-22: <i>„A paired bootstrap gives a 95% CI of 2.3 to 4.4 points, so Opus ahead by about three points is unlikely to be noise.”</i> <span class="src">T2 — a gateway üzemeltetője, nem a gyártó.</span></td></tr>
<tr><td>A gyártó saját mérése, négy munkafolyamaton</td><td>Jev <b>67,8%</b> · GPT-5.6 Sol <b>74,1%</b>; számlafeldolgozáson <b>61,8%</b> · <b>79,1%</b></td><td>TypeSafe, <code>evals.typesafe.ai</code>. <span class="src">Nem emberi igazsághoz mért pontosság, hanem egyezés két másik modell (GPT-6 Astra, Claude Fable 5.1) átlagolt válaszával.</span></td></tr>
<tr><td>Magyar nyelven</td><td class="n"><b>nincs mérés</b></td><td>Két külön kör célzottan kereste. <span class="src">Más nyelveken a szórt adatok nyelvváltáskor romlást mutatnak.</span></td></tr>
</tbody>
</table>
</div>

<p class="src">Független minősítés, szó szerint (AY Automate, 2026-09-20): <i>„Jev behaved like a good small model, not like a frontier model.”</i></p>

<h3>Működés és feltételek</h3>

<div class="table-scroll">
<table>
<thead><tr><th>Amit mértek vagy vállalnak</th><th>Érték</th><th>Forrás és feltétel</th></tr></thead>
<tbody>
<tr><td>Válaszidő</td><td><b>70–500 ms</b></td><td>Gyártói állítás. A gyártó maga írja: <i>„our published evals are generally run from our laptops on the West Coast”</i>. <span class="src">Független, kontrollált mérés nincs.</span></td></tr>
<tr><td>Ismételt futtatás szórása ugyanarra a kérdésre</td><td>átlagosan <b>~0,01</b>; egy kérdés <b>0,43–0,53</b> között ingadozott</td><td>TypeSafe cookbook: <i>„TypeSafe's mean per-question probability standard deviation is 0.0102 […] Its covered answers span 0.43 to 0.53, crossing a 0.5 decision threshold.”</i> <span class="src">Gyártói mérés. Nincs seed és nincs temperature.</span></td></tr>
<tr><td>Ár</td><td><b>0,042 dollár</b> millió bemeneti tokenenként; a kimenet ingyenes</td><td>TypeSafe blog; az OpenRouter ártáblája egyezik. <span class="src">Kredit-alapú elszámolás, a kredit nem visszatéríthető.</span></td></tr>
<tr><td>Korlátok</td><td><b>250 000</b> token/mp · <b>1 200</b> kérés/perc</td><td>TypeSafe, <code>docs.typesafe.ai/models</code>: <i>„the limits above can change without notice”</i>.</td></tr>
<tr><td>Elfogyott kredit</td><td>a gyártó API-ja nem dokumentál rá hibakódot · OpenRouter és Vercel: <b>402</b> · Cloudflare: <b>429</b></td><td>A három gateway hivatalos dokumentációja.</td></tr>
<tr><td>Felelősségkorlát</td><td>ingyenes használatnál <b>50 dollár</b>; fizetősnél a 12 havi díj vagy 50 dollár közül a nagyobb</td><td>TypeSafe Terms of Service és Master Customer Agreement 12.2.</td></tr>
<tr><td>Hol fut</td><td class="n"><b>csak az USA-ban</b></td><td>TypeSafe adatvédelmi szabályzat: <i>„The Services are hosted in the United States”</i>. <span class="src">„Zero data retention” egyik hivatalos dokumentumában sincs; az OpenRouter és a Vercel gateway-en át van.</span></td></tr>
</tbody>
</table>
</div>

<div class="danger">
<span class="kicker">Amire nincs adat</span>
<p><b>Magyar nyelvű mérés</b> — semmilyen.</p>
<p><b>Mennyit javít, ha egy frontier ágens döntése után egy gyors modell ellenőriz.</b> Ilyen munkafolyamat létezik, számszerű haszna nincs publikálva.</p>
<p><b>Kalibráció:</b> a gyakran idézett „CLINC150 0,02 / Banking77 0,05–0,09” számok forrása belsőleg ellentmondásos — nem igazolt, ezért nem is használjuk.</p>
</div>

'''
anchor9 = '<h2 id="s7"><span class="num">20</span>Amit nem mértünk — és lezártunk</h2>'
t = rep(t, anchor9, S21 + anchor9.replace('<span class="num">20</span>', '<span class="num">21</span>'))
t = rep(t, '<li><a href="#s7">Amit nem mértünk — és lezártunk</a></li>',
        '<li><a href="#s21">Jev — amiért most nem építjük be</a></li>\n<li><a href="#s7">Amit nem mértünk — és lezártunk</a></li>')
t = rep(t, '<span class="chip">frissítve: 2026-09-24</span>', '<span class="chip">frissítve: 2026-09-25</span>')
open(F9, 'w', encoding='utf-8').write(t)
print('ok')
