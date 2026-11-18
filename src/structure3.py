import sys, math, itertools
sys.path.insert(0,'src')
from common import *
from sympy import factorint
Q = load_puzzles('data/practice_puzzles.csv')
for pid in sys.argv[1:]:
    p=Q[pid]; S=p['starting_values']; T=p['targets']
    print('=====',pid,p['family'],p['design_tier'],'S=',S,'lim=%.3e'%p['value_limit'])
    for i,t in enumerate(T):
        g=[(j,math.gcd(t,u)) for j,u in enumerate(T) if j!=i and math.gcd(t,u)>1000]
        print('  %20d'%t, dict(factorint(t)), 'bigg:',g[:4])
