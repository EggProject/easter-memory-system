import re,html,sys
def text(fn):
    s=open(fn,encoding='utf-8').read()
    s=re.sub(r'<(style|script)[^>]*>.*?</\1>',' ',s,flags=re.S)
    s=re.sub(r'<[^>]+>',' ',s); s=html.unescape(s)
    return re.sub(r'\s+',' ',s)
NUM=re.compile(r'~?\d+(?:[  ]\d{3})*(?:[,.]\d+)?(?:\s?[–-]\s?\d+(?:[  ]\d{3})*(?:[,.]\d+)?)?(?:\s?(?:ms/MB|ms|s/GB|s|MB|GB|KB|%|×|-szeres\w*|-szoros\w*))?')
def nums(t):
    out=set()
    for m in NUM.finditer(t):
        v=m.group(0).strip()
        # zaj: dátumok, D-számok, verziók, szakaszszámok
        if re.fullmatch(r'\d{4}(-\d{2}(-\d{2})?)?',v): continue
        if re.fullmatch(r'\d{1,2}',v): continue
        out.add(v)
    return out
t90=text('90-meresek.html')
t90n=t90.replace(' ',' ')
for f in ['00-dontesek','20-adatmodell','30-kereses','40-mcp','50-uzemeltetes','60-felulet','90-meresek']:
    cur=text(f+'.html'); old=text('../eredeti/'+f+'.html')
    new=nums(cur)-nums(old)
    miss=[]
    for v in sorted(new):
        core=v.lstrip('~')
        if f=='90-meresek': continue
        if core.replace(' ',' ') not in t90n: miss.append(v)
    print(f, 'új számok:',len(new),'| nincs a 90-ben:',miss)
    if f=='90-meresek': print('   90 új számai:',sorted(new))
