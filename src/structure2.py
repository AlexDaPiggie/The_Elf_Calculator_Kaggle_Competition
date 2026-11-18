import sys, math, itertools
sys.path.insert(0,'src')
from common import *
Q = load_puzzles('data/practice_puzzles.csv')
def small_expr(d, S):
    # express d as small combination of starts? just print d
    return d
for pid in sys.argv[1:]:
    p=Q[pid]; S=p['starting_values']; T=p['targets']
    print('=====',pid,p['family'],p['design_tier'],'S=',S,'lim=%.3e'%p['value_limit'], 'LB',p['lower_bound'])
    for i,t in enumerate(T):
        best=[]
        for u in T[:i]+T[i+1:]+S:
            if u==t: continue
            d=abs(t-u)
            if d < 100000: best.append(('diff',u,t-u))
            r=t/u
            if r>1.5:
                q=round(r);
                for qq in (t//u,):
                    rem=t-qq*u
                    if qq<=1000 and abs(rem)<2000: best.append(('mul',u,qq,rem))
        print('  %20d'%t, best[:4])
