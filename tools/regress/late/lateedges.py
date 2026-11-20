# python3 lateedges.py -> lateedges.json: пары правил внутри late.css, порядок которых нельзя менять (статически)
import sys,json,collections;sys.path.insert(0,'/workspace/rf')
from plan import *
late='overrides/late.css';L0=modstart[late];s=texts[late]
blocks=list(collections.OrderedDict((r['top'],None) for r in rules[L0:]).keys())
bid={t:k for k,t in enumerate(blocks)}
R=[r for r in rules[L0:] if r['decls']]
pairs=[];edges=set()
for a in range(len(R)):
    X=R[a]
    for b in range(a+1,len(R)):
        Y=R[b]
        if X['top']==Y['top']: continue
        if C.ctx_disjoint(X['ctx'],Y['ctx']): continue
        hit=None
        for (p,imp,v) in X['decls']:
            for (q,imp2,v2) in Y['decls']:
                if imp!=imp2 or not C.overlap(p,q): continue
                if C.norm(p)==C.norm(q) and C.vnorm(v)==C.vnorm(v2): continue
                for s1 in X['sels']:
                    sp=C.spec(s1)
                    for t in Y['sels']:
                        if C.spec(t)==sp and C.compatible(s1,t) and not C.page_disjoint(s1,t) and not C.class_disjoint(s1,t):
                            hit=hit or set();hit.add((s1,t))
        if hit:
            edges.add((bid[X['top']],bid[Y['top']]));pairs.append([sorted(hit),bid[X['top']],bid[Y['top']]])
json.dump(dict(blocks=[list(t) for t in blocks],pairs=pairs),open('lateedges.json','w'))
print('blocks',len(blocks),'rules',len(R),'edge pairs',len(pairs),'block edges',len(edges))
