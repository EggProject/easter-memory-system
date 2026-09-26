import re,sys,html
src=open('/home/claude/work/audit/00-dontesek.html',encoding='utf-8').read()
def section(dnum):
    m=re.search(r'<h2 id="(s\d+)"><span class="num">\d+</span>%s — '%re.escape(dnum),src)
    if not m: return None
    start=m.start()
    nxt=src.find('<h2 ',m.end())
    return src[start:nxt if nxt>0 else len(src)]
for d in sys.argv[1:]:
    s=section(d)
    print('=====',d, len(s) if s else None)
    if s: print(s)
