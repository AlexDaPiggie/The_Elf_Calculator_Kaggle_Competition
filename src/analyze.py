import sys, statistics as st, math
sys.path.insert(0, 'src')
from common import *
P = load_puzzles('data/puzzles.csv'); Q = load_puzzles('data/practice_puzzles.csv')
S = load_submission('data/sample_submission.csv')
print('sample score', score(P, S))
lb = {k: len(set(p['targets'])-set(p['starting_values'])) for k,p in P.items()}
print('sum LB scored', sum(lb.values()))
print('sample per-puzzle len stats', st.mean(len(v) for v in S.values()), max(len(v) for v in S.values()))
ns = [len(p['starting_values']) for p in P.values()]; nt=[len(p['targets']) for p in P.values()]
print('n start dist', {i: ns.count(i) for i in sorted(set(ns))})
print('n targets dist min/mean/max', min(nt), st.mean(nt), max(nt))
print('log10 limit dist', sorted(set(round(math.log10(p['value_limit'])) for p in P.values())))
# practice families
from collections import Counter, defaultdict
c=Counter((p['family'],p['design_tier']) for p in Q.values()); print(c)
fam=defaultdict(list)
for p in Q.values(): fam[p['family']].append(p)
for f,ps in fam.items():
    print('==',f, len(ps), 'starts', Counter(len(p['starting_values']) for p in ps), 'targets mean', st.mean(len(p['targets']) for p in ps),
          'log10 lim', sorted(round(math.log10(p['value_limit']),1) for p in ps)[:3], '...', 'maxstart', max(max(p['starting_values']) for p in ps))
    for p in ps[:2]: print('   ', p['starting_values'], p['targets'][:8], p['value_limit'])
