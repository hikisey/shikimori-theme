# python3 reorg.py [--apply]  — раскладывает late.css по разделам (хозяин-модуль, причина),
# сохраняя относительный порядок всех пар правил, которые могут перебивать друг друга (lateedges.json + улики корпуса)
import sys,json,re,collections,heapq;sys.path.insert(0,'/workspace/rf')
import cascade as C
SRC=C.SRC;M=C.man()
s=open(SRC+'/overrides/late.css',encoding='utf-8').read()
E=json.load(open('lateedges.json'));blocks=[tuple(t) for t in E['blocks']]
EV={}
for f in os.environ.get('EVF','comatch5.json,comatch_late.json').split(','):
    for a,b,r in json.load(open(f)): EV[(a,b)]=r
def evid(a,b):
    r=EV.get((a,b))
    if r is not None and not r.get('err') and not r['co'] and r['a'] and r['b']: return True
    return C.class_disjoint2(a,b)
edges=collections.defaultdict(set);kept=0;dropped=0
for hits,i,j in E['pairs']:
    if all(evid(a,b) for a,b in hits): dropped+=1;continue
    edges[i].add(j);kept+=1
plan={tuple(b['top']):b for b in json.load(open('plan.json'))}
cls={}
for l in open(sys.argv[sys.argv.index('--cls')+1] if '--cls' in sys.argv else 'cls4.txt'):
    m=re.match(r"(\d+) (\d+) (\S+) (\{.*?\}) (.*)",l);k=eval(m.group(4))
    cls[int(m.group(1))]='real' if k.get('real') else 'rest'
COL=r'\.(orange|purple|green|blue|magenta|gray|powderblue|skyblue|yellow|red|pink|brown)'
def firstline(t):
    a=t[0]
    while a<t[1] and s[a] in ' \n\t': a+=1
    return a
def body(t): return re.sub(r'/\*.*?\*/','',s[t[0]:t[1]],flags=re.S)
def section(k,t):
    b=body(t);ln=s.count('\n',0,firstline(t))+1
    sels=[x for r in C.flatten(s[t[0]:t[1]],'x') for x in r['sels']]
    if 'prefers-reduced-motion' in b and '*' in [x.strip() for x in sels]: return ('zz_motion',None)
    if any(x.strip() in ('html',) or x.startswith('body[style') for x in sels): return ('zy_site',None)
    if any(re.search(r'block-rip|btn-rip|#toggle-players|players-loader|from_rip|shiki_sync',x) for x in sels): return ('zx_rip',None)
    if all(re.fullmatch(COL,x.strip()) for x in sels): return ('a_global','colors')
    if any(':-webkit-any-link' in x for x in sels): return ('a_global','links')
    if any(x.startswith('body * [class*=') for x in sels): return ('a_global','markers')
    tgt=plan[t]['tgt']
    if not tgt: return ('a_global','misc')
    return ('m_%02d'%M.index(tgt),tgt,cls.get(ln,'rest'))
sec=[section(k,t) for k,t in enumerate(blocks)]
def key(k):
    x=sec[k];sub={'colors':1,'markers':0,'misc':2,'real':0,'rest':1}
    return (x[0],sub.get(x[-1] if len(x)>2 else x[1],0),k)
indeg=collections.Counter()
for i in edges:
    for j in edges[i]: indeg[j]+=1
h=[key(k) for k in range(len(blocks)) if not indeg[k]];heapq.heapify(h);order=[]
while h:
    *_,k=heapq.heappop(h);order.append(k)
    for j in edges[k]:
        indeg[j]-=1
        if not indeg[j]: heapq.heappush(h,key(j))
assert len(order)==len(blocks),'cycle?'
# where blocks end up vs their section
runs=[];prev=None
for k in order:
    g=sec[k][:2] if sec[k][0].startswith('m_') else sec[k][:2]
    lab=sec[k]
    if runs and runs[-1][0]==lab: runs[-1][1].append(k)
    else: runs.append([lab,[k]])
labs=collections.Counter(tuple(r[0]) for r in runs)
frag={l:c for l,c in labs.items() if c>1}
print('edges kept',kept,'dropped by evidence',dropped,'runs',len(runs),'sections',len(labs),'fragmented',len(frag))
for l,c in sorted(frag.items()): print('  frag',l,c,[len(r[1]) for r in runs if tuple(r[0])==l])
json.dump(dict(order=order,sec=[list(x) for x in sec],runs=[[list(r[0]),r[1]] for r in runs]),open('reorg.json','w'))
