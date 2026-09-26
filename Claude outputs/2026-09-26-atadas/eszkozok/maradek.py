import re,html
PAT=re.compile(r'SQLite|sqlite|FTS5|\bWAL\b|VACUUM INTO|quick_check|wal_checkpoint|journal_mode|bun:sqlite|unicode61|árnyéktábl|foreign_key_check|integrity-check|\brebuild\b')
MARK=re.compile(r'Korábban|2026-09-22-ig|[Tt]árgytalan|[Kk]ivezetve|D-43|kiesett|korábbi|SQLite-tervhez|motorunkról|itt még|szólt|megszűnt|SQLite-specifikus|SQLite-os|2026-09-22 —|2026-09-22 óta|FTS5-ön|SQLite-eszköz')
def blocks(s):
    # a legkisebb blokk: td / p / li / pre / h2-h4 / figcaption / text
    for m in re.finditer(r'<(td|p|li|pre|h[1-4]|figcaption|text)\b[^>]*>(.*?)</\1>',s,re.S):
        yield m.start(), m.group(2)
for f in ['00-dontesek','20-adatmodell','30-kereses','40-mcp','50-uzemeltetes','60-felulet']:
    s=open(f+'.html',encoding='utf-8').read()
    s=re.sub(r'<(style|script)[^>]*>.*?</\1>','',s,flags=re.S)
    heads=[(m.start(),re.sub('<[^>]+>','',m.group(1))) for m in re.finditer(r'<h2 id="s\d+">(.*?)</h2>',s)]
    def sec(p):
        t=''
        for q,h in heads:
            if q<=p: t=h
        return t
    n=0
    for pos,b in blocks(s):
        txt=html.unescape(re.sub('<[^>]+>','',b))
        if not PAT.search(txt): continue
        if 'D-34 — ' in sec(pos): continue
        if MARK.search(txt): continue
        n+=1
        m=PAT.search(txt); i=m.start()
        print(f'{f} | {sec(pos)[:40]} | …{txt[max(0,i-120):i+120]}…')
    print('==',f,n)
