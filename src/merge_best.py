"""Merge submission CSVs into best/best.csv, keeping the shortest valid program per puzzle.
usage: merge_best.py sub1.csv [sub2.csv ...]"""
import sys, os
sys.path.insert(0, 'src')
from common import *

P = load_puzzles('data/puzzles.csv')
BEST = 'best/best.csv'
os.makedirs('best', exist_ok=True)
best = load_submission(BEST) if os.path.exists(BEST) else {}
before = sum(len(v) for v in best.values()) if len(best) == len(P) else None
gains = 0
for path in sys.argv[1:]:
    for k, prog in load_submission(path).items():
        if k not in P or check(P[k], prog):
            continue
        if k not in best or len(prog) < len(best[k]):
            if k in best: gains += len(best[k]) - len(prog)
            best[k] = prog
total = score(P, best)
write_submission(BEST, best)
print(f'best: {before} -> {total} (gain {gains})')
