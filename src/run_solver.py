"""Run our stdin/stdout C++ solver over puzzles in parallel.
usage: run_solver.py exe out.csv [puzzles.csv] -- [solver args...]"""
import sys, subprocess, json
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, 'src')
from common import *
argv = sys.argv[1:]
sep = argv.index('--') if '--' in argv else len(argv)
pos, args = argv[:sep], argv[sep+1:]
exe, out = pos[0], pos[1]
src = pos[2] if len(pos) > 2 else 'data/puzzles.csv'
P = load_puzzles(src)
items = list(P.items())
def run(batch):
    lines = [' '.join(map(str, (k, p['value_limit'], len(p['starting_values']), len(p['targets']), *p['starting_values'], *p['targets']))) for k, p in batch]
    r = subprocess.run([exe, *args], input='\n'.join(lines) + '\n', text=True, capture_output=True)
    if r.returncode: raise RuntimeError(r.stderr[-2000:])
    return [l.split(' ', 1) for l in r.stdout.splitlines()]
progs = {}
with ThreadPoolExecutor(16) as ex:
    for rows in ex.map(run, [items[i:i+5] for i in range(0, len(items), 5)]):
        for k, v in rows: progs[k] = json.loads(v)
print('score', score(P, progs))
write_submission(out, progs)
