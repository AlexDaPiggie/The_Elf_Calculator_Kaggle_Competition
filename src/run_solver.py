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
    lines = [' '.join(map(str, (k, p['value_limit'], len(p['starting_values']), len(p['targets']), *p['starting_values'], *p['targets'], *((len(H[k]), *[x for ins in H[k] for x in ins]) if H else ())))) for k, p in batch]
    for attempt in range(3):
        r = subprocess.run([exe, *args], input='\n'.join(lines) + '\n', text=True, capture_output=True)
        if not r.returncode: return [l.split(' ', 1) for l in r.stdout.splitlines()]
        print('batch fail rc', r.returncode, [k for k, _ in batch], r.stderr[-300:], file=sys.stderr, flush=True)
    return []
H = None
if __import__('os').environ.get('HINT_CSV'): H = load_submission(__import__('os').environ['HINT_CSV'])
BS = int(__import__('os').environ.get('BATCH', 5))
progs = {}
import os
if os.environ.get('RESUME') and os.path.exists(out):  # continue from a checkpoint (partial output file)
    progs = {k: v for k, v in load_submission(out).items() if k in P}
    print('resumed', len(progs), 'puzzles from', out, flush=True)
todo = [it for it in items if it[0] not in progs]
with ThreadPoolExecutor(int(os.environ.get('THREADS', 16))) as ex:
    for n, rows in enumerate(ex.map(run, [todo[i:i+BS] for i in range(0, len(todo), BS)])):
        for k, v in rows: progs[k] = json.loads(v)
        if n % 5 == 0: write_submission(out, progs)  # checkpoint
print('solved', len(progs), 'of', len(P))
print('score', score(P, progs) if len(progs) == len(P) else 'partial')
write_submission(out, progs)
