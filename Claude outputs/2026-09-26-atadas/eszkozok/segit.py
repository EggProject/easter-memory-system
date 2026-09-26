import re
F = '/home/claude/work/audit/00-dontesek.html'
DATUM = '2026-09-22'

def load():
    return open(F, encoding='utf-8').read()

def save(s):
    open(F, 'w', encoding='utf-8').write(s)

def sec_bounds(s, d):
    m = re.search(r'<h2 id="s\d+"><span class="num">\d+</span>%s — ' % re.escape(d), s)
    assert m, d
    nxt = s.find('<h2 ', m.end())
    return m.start(), (nxt if nxt > 0 else len(s))

def sub_in_sec(s, d, old, new, count=1):
    a, b = sec_bounds(s, d)
    sec = s[a:b]
    assert sec.count(old) == count, (d, old[:80], sec.count(old))
    return s[:a] + sec.replace(old, new) + s[b:]

ROW = r'(<tr>\s*<td><code>%s</code></td>\s*<td[^>]*>)(.*?)(</td>\s*<td>)(.*?)(</td>\s*</tr>)'

def row(s, d, n):
    a, b = sec_bounds(s, d)
    ms = list(re.finditer(ROW % n, s[a:b], re.S))
    assert len(ms) == 1, (d, n, len(ms))
    return a, ms[0]

def _put(s, a, m, title, body):
    return s[:a + m.start()] + m.group(1) + title + m.group(3) + body + m.group(5) + s[a + m.end():]

def modosit(s, d, n, miert, uj):
    """A tétel tartalma megváltozik: dátumozott ok, új szöveg, alatta a régi „Korábban:" jelöléssel."""
    a, m = row(s, d, n)
    body = ('<span class="src"><b>%s-én átírva — a D-43 következménye.</b> %s</span><br>%s'
            '<br><br><span class="src"><b>Korábban:</b> %s</span>') % (DATUM, miert, uj, m.group(4))
    return _put(s, a, m, m.group(2), body)

def targytalan(s, d, n, miert):
    """A tétel tárgya megszűnt: jelölés, ok, alatta a régi szöveg."""
    a, m = row(s, d, n)
    title = m.group(2) + ' <span class="m">— tárgytalan</span>'
    body = ('<span class="m">Tárgytalan %s óta (D-43).</span> %s'
            '<br><br><span class="src"><b>Korábban:</b> %s</span>') % (DATUM, miert, m.group(4))
    return _put(s, a, m, title, body)

def megjegyez(s, d, n, jegyzet):
    """A tétel áll, de egy része vagy az indoka megváltozott: dátumozott megjegyzés a végére."""
    a, m = row(s, d, n)
    body = m.group(4) + '<br><br><span class="src"><b>%s — a D-43 óta:</b> %s</span>' % (DATUM, jegyzet)
    return _put(s, a, m, m.group(2), body)

def statusz_modositva(s, d):
    a, b = sec_bounds(s, d)
    sec = s[a:b]
    old = 'Státusz: <span class="y">élő</span>'
    assert sec.count(old) == 1, d
    return s[:a] + sec.replace(old, old + ' · <b>Módosítva: %s (D-43)</b>' % DATUM) + s[b:]

def kartya_jegyzet(s, d, html):
    """Megjegyzés a döntés kártyájának végére."""
    a, b = sec_bounds(s, d)
    sec = s[a:b]
    i = sec.find('<div class="card">')
    j = sec.find('</div>', i)
    assert i > 0 and j > i, d
    sec = sec[:j] + '<p class="src"><b>%s — a D-43 óta:</b> %s</p>\n' % (DATUM, html) + sec[j:]
    return s[:a] + sec + s[b:]
