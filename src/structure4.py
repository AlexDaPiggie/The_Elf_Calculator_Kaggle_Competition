import sys; sys.path.insert(0,'src')
from common import *
Q=load_puzzles('data/practice_puzzles.csv')
def ops(a,b,L):
    if a<b: a,b=b,a
    r=[a+b]
    if a>b: r.append(a-b)
    r.append(a*b)
    if b>1 and a%b==0: r.append(a//b)
    return [x for x in r if 0<x<=L]
from collections import defaultdict
res=defaultdict(lambda:[0,0,0])
for p in Q.values():
    if p['family']=='tiny': continue
    S=p['starting_values']; T=p['targets']; L=p['value_limit']
    for idx,t in enumerate(T):
        pool=sorted(set(S)|set(T)-{t})
        one=set()
        for i,a in enumerate(pool):
            for b in pool[:i+1]: one.update(ops(a,b,L))
        h1 = t in one
        h2=False
        if not h1:
            for c in pool:
                for u in (t-c, t+c, c-t, t//c if t%c==0 else 0, t*c):
                    if u>0 and u in one: h2=True;break
                if h2: break
        r=res[p['family']]; r[0]+=1; r[1]+=h1; r[2]+=h2
for f,(n,a,b) in res.items(): print(f, n, 'one-op %.2f'%(a/n), 'two-op %.2f'%(b/n))
