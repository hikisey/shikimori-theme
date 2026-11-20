import json,collections,sys
d=sys.argv[1];fxf=sys.argv[2]
good=collections.defaultdict(set);diff=collections.defaultdict(list);err=0
for l in open(d+'/results.jsonl'):
    r=json.loads(l)
    if r.get('err'): err+=1;continue
    good[r['fx']].add(r['cfg'])
    if r.get('n'): diff[r['fx']].append((r['cfg'],r['n']))
fx=[x.strip().split('/')[-1] for x in open(fxf) if x.strip()]
print('done',sum(len(good[f]) for f in fx),'/',len(fx)*10,'err',err)
print(dict(diff))
