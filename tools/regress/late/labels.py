# python3 labels.py [--apply] — подписывает подряд идущие блоки late.css: модуль-хозяин и почему правило здесь.
# Порядок правил не меняется, меняются только комментарии (в сборку не попадают).
import sys,os,json,re,collections;sys.path.insert(0,'/workspace/rf')
exec(open('/workspace/rf/reorg.py').read().split("edges=collections")[0])
plan={tuple(b['top']):b for b in json.load(open('plan.json'))}
cls={}
for l in open(os.environ.get('CLS','cls4.txt')):
    m=re.match(r"(\d+) (\d+) (\S+) (\{.*?\}) (.*)",l);k=eval(m.group(4));cls[int(m.group(1))]='real' if k.get('real') else 'rest'
exec(open('/workspace/rf/reorg.py').read().split("COL=")[1].join(["COL=",""]).split("sec=[section")[0]) if False else None
src=open('/workspace/rf/reorg.py').read()
exec('COL='+src.split('COL=')[1].split('sec=[section')[0])
def losers(t):
    out=collections.Counter()
    for c in plan[t]['conf']:
        r=EV.get((c[2],c[3]))
        if r and not r.get('err') and r['co']: out[c[1].split('/')[-1]]+=1
    return [f for f,_ in out.most_common()]
def label(k,t):
    x=section(k,t)
    if x[0]=='zz_motion': return 'весь сайт: «Уменьшение движения», должно остаться последним'
    if x[0]=='zy_site': return 'весь сайт: корень html и просмотр картинок'
    if x[0]=='zx_rip': return 'только shikimori.rip'
    if x[1]=='colors': return 'общее: цвета-классы'
    if x[1]=='markers': return 'общее: метки и теги body * [class*="_marker"], [class*="_status_tag"]'
    if x[1]=='links': return 'общее: ссылки'
    if x[1]=='misc': return 'общее: страница без своего модуля'
    if x[2]=='real':
        L=[('правило выше в этом файле' if f=='late.css' else f) for f in losers(t)]
        return 'дом %s · перебивает %s'%(x[1],', '.join(L) or '?')
    return 'дом %s · без доказательства'%x[1]
labs=[label(k,t) for k,t in enumerate(blocks)]
ins=[];prev=None
for k,t in enumerate(blocks):
    if labs[k]!=prev:
        a=firstline(t)
        if k==0 and s.startswith('/*',a): a=s.index('*/',a)+2;a=a+len(s[a:])-len(s[a:].lstrip('\n'))
        ins.append((a,labs[k]))
    prev=labs[k]
print('blocks',len(blocks),'labels',len(ins))
cnt=collections.Counter(re.sub(r' ·.*','',l) for l in labs);print(cnt.most_common())
if '--apply' in sys.argv:
    out=[];pos=0
    for a,l in ins:
        out.append(s[pos:a]);out.append('/* ── %s ── */\n'%l);pos=a
    out.append(s[pos:]);open(SRC+'/overrides/late.css','w',encoding='utf-8').write(''.join(out));print('applied')
else:
    for a,l in ins[:400]: print(s.count('\n',0,a)+1,l)
