import json,collections,heapq,sys,itertools
exec(open('reorg.py').read().split("sec=[section")[0])
sec=[section(k,t) for k,t in enumerate(blocks)]
lab=[tuple(x[:2]) if (len(x)>2 and "--nosub" in sys.argv) else tuple(x) for x in sec]
N=len(blocks)
pred=collections.defaultdict(set)
for i in edges:
    for j in edges[i]: pred[j].add(i)
def runs(order):
    r=0;p=None
    for k in order:
        if lab[k]!=p: r+=1;p=lab[k]
    return r
def kahn(rank):
    indeg={k:len(pred[k]) for k in range(N)};h=[(rank[lab[k]],k) for k in range(N) if not indeg[k]];heapq.heapify(h);o=[]
    while h:
        _,k=heapq.heappop(h);o.append(k)
        for j in edges[k]:
            indeg[j]-=1
            if not indeg[j]: heapq.heappush(h,(rank[lab[j]],j))
    return o
def rkahn(rank):
    outd={k:len(edges[k]) for k in range(N)};h=[(-rank[lab[k]],-k) for k in range(N) if not outd[k]];heapq.heapify(h);o=[]
    while h:
        _,k=heapq.heappop(h);k=-k;o.append(k)
        for j in pred[k]:
            outd[j]-=1
            if not outd[j]: heapq.heappush(h,(-rank[lab[j]],-j))
    return o[::-1]
def stick(rank):
    # emit by section; keep emitting from the current section while possible (sticky), else smallest rank
    indeg={k:len(pred[k]) for k in range(N)};avail=set(k for k in range(N) if not indeg[k]);o=[];cur=None
    while avail:
        c=[k for k in avail if lab[k]==cur]
        k=min(c) if c else min(avail,key=lambda k:(rank[lab[k]],k));cur=lab[k]
        avail.remove(k);o.append(k)
        for j in edges[k]:
            indeg[j]-=1
            if not indeg[j]: avail.add(j)
    return o
labs=sorted(set(lab),key=lambda x:(x[0],str(x[1:])))
r1={l:i for i,l in enumerate(labs)}
mean={l:sum(k for k in range(N) if lab[k]==l)/sum(1 for k in range(N) if lab[k]==l) for l in labs}
fixed=lambda l:(0 if l[0]=='a_global' else 2 if l[0].startswith('z') else 1)
r2={l:i for i,l in enumerate(sorted(labs,key=lambda l:(fixed(l),mean[l])))}
r3={l:i for i,l in enumerate(sorted(labs,key=lambda l:(fixed(l),l[0] if l[0].startswith('z') else '',mean[l])))}
print('orig',runs(list(range(N))))
for nm,r in [('manifest',r1),('mean',r2),('mean2',r3)]:
    for f in (kahn,rkahn,stick):
        o=f(r);print(nm,f.__name__,runs(o),len(o))
