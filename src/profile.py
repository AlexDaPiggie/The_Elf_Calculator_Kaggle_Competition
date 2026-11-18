"""Print per-target costs for some practice puzzles. usage: profile.py exe [args...]"""
import sys,subprocess,os; sys.path.insert(0,'src')
from common import *
Q=load_puzzles('data/practice_puzzles.csv')
for k in ['practice_0005','practice_0004','practice_0001','practice_0002','practice_0034']:
    p=Q[k]
    line=' '.join(map(str,(k,p['value_limit'],len(p['starting_values']),len(p['targets']),*p['starting_values'],*p['targets'])))
    r=subprocess.run(sys.argv[1:],input=line+'\n',text=True,capture_output=True,env={**os.environ,'ELF_DEBUG':'1'})
    c=[int(l.split()[-1]) for l in r.stderr.split('\n') if 'cost' in l]
    print(k,p['family'],p['starting_values'],'%.0e'%p['value_limit'],sum(c),c)
