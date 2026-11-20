import json,collections,sys
good=collections.defaultdict(set);diff=collections.defaultdict(list)
for d in ['d_c180','d_c180b']:
    try: L=open(d+'/results.jsonl')
    except: continue
    for l in L:
        r=json.loads(l)
        if r.get('err'): continue
        good[r['fx']].add(r['cfg'])
        if r.get('n'): diff[r['fx']].append(r['cfg'])
for g in sys.argv[1:]:
    fx=[x.strip().split('/')[-1] for x in open(f'fx_{g}.txt') if x.strip()]
    nd=[f for f in fx if len(good[f])<10]
    print(g,len(fx),'left',len(nd),'with diffs',[(f,diff[f]) for f in fx if diff[f]])
