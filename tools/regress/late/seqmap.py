# python3 seqmap.py map.tsv oldlate newlate > map_new.tsv : перенумеровать строки карты по тексту блока
import sys
m,o,n=sys.argv[1:4];O=open(o).read().split('\n');N=open(n).read().split('\n')
for l in open(m):
    ln,t=l.split();ln=int(ln);key=O[ln-1:ln+3]
    hits=[i+1 for i in range(len(N)) if N[i:i+4]==key]
    assert len(hits)==1,(ln,hits);print(f'{hits[0]}\t{t}')
