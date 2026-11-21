"""Rebuild local_leaderboard.md: top 10 full submission files by exact local score."""
import sys, glob; sys.path.insert(0, 'src')
from common import *
P = load_puzzles('data/puzzles.csv'); rows = []
for f in glob.glob('subs/*.csv') + ['best/best.csv']:
    try: S = load_submission(f)
    except Exception: continue
    if set(S) != set(P): continue
    if any(check(P[k], S[k]) for k in P): continue
    rows.append((sum(len(v) for v in S.values()), f))
rows.sort()
with open('local_leaderboard.md', 'w') as o:
    o.write('# Local leaderboard (top 10 valid full files, exact score, lower is better)\n\n| rank | score | file |\n|---:|---:|---|\n')
    for i, (s, f) in enumerate(rows[:10], 1): o.write(f'| {i} | {s:,} | {f} |\n')
print(open('local_leaderboard.md').read())
