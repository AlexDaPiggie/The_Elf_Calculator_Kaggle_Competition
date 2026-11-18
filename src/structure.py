import sys, math
sys.path.insert(0,'src')
from common import *
Q = load_puzzles('data/practice_puzzles.csv')
from collections import Counter
def one_op(vals):
    vs=sorted(vals); out={}
    for i,a in enumerate(vs):
        for b in vs[:i+1]:
            for op,z in (('+',a+b),('-',a-b),('*',a*b),('/',a//b if a%b==0 else 0)):
                if z>0: out.setdefault(z,(op,a,b))
    return out
stats=Counter()
for fam in ['independent','shared','multiplicative','mixed']:
    ps=[p for p in Q.values() if p['family']==fam][:3]
    for p in ps:
        S=p['starting_values']; T=p['targets']
        print('=====',p['id'],fam,p['design_tier'],'S=',S,'n=',len(T),'lim=%.2e'%p['value_limit'])
        pool=set(S)|set(T)
        o=one_op(pool)
        for t in T:
            rel=o.get(t) if t not in S else None
            # also check t vs others via small multipliers
            note=''
            if rel is None:
                # gcd with other targets / factorization small
                f=[q for q in range(2,200) if t%q==0][:6]
                note='div:'+str(f)
            print('  %22d'%t, rel if rel else '', note)
