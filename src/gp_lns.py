"""Run goodpjw's LNS engine (ext/goodpjw/elfopt.exe, source scanned: stdin/stdout only) on our best programs in the 60-180 length band.
usage: gp_lns.py in.csv out.csv --seconds S --rounds R --shards N [--lo 60 --hi 180]
Writes only strictly improved, fully validated programs (per puzzle best) to out.csv after every round."""
import sys, subprocess, json, time, argparse
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, 'src')
from common import *
ap = argparse.ArgumentParser()
ap.add_argument('inp'); ap.add_argument('out')
ap.add_argument('--seconds', type=float, default=30); ap.add_argument('--rounds', type=int, default=1)
ap.add_argument('--shards', type=int, default=14); ap.add_argument('--lo', type=int, default=60); ap.add_argument('--hi', type=int, default=180)
ap.add_argument('--seed', type=int, default=20261120); ap.add_argument('--kicks', type=int, default=1000); ap.add_argument('--kslack', type=int, default=2)
a = ap.parse_args()
P = load_puzzles('data/puzzles.csv'); cur = load_submission(a.inp); base = sum(len(v) for v in cur.values())
def enc(k, prog):
    p = P[k]
    h = ['P', k, str(len(p['starting_values'])), *map(str, p['starting_values']), str(len(p['targets'])), *map(str, p['targets']), str(p['value_limit']), str(p.get('registers', 48)), str(len(prog))]
    return ' '.join(h) + chr(10) + chr(10).join(f'{op} {x} {y} {d}' for op, x, y, d in prog) + chr(10)
def parse(text):
    rows = text.splitlines(); i = 0; out = {}
    while i < len(rows):
        f = rows[i].split()
        if not f or f[0] != 'R': i += 1; continue
        n = int(f[3]); prog = []
        for l in rows[i+1:i+1+n]:
            op, x, y, d = l.split(); prog.append([op, int(x), int(y), int(d)])
        out[f[1]] = prog; i += n + 1
    return out
t0 = time.time()
for r in range(a.rounds):
    sel = sorted([k for k in cur if a.lo <= len(cur[k]) <= a.hi], key=lambda k: -len(cur[k]))
    shards = [sel[i::a.shards] for i in range(a.shards)]
    def run(i):
        payload = ''.join(enc(k, cur[k]) for k in shards[i])
        seed = a.seed + r * 1000003 + i * 7919
        for _ in range(2):
            res = subprocess.run([__import__('os').path.abspath('ext/goodpjw/elfopt.exe'), '--time', str(a.seconds), '--seed', str(seed), '--kicks', str(a.kicks), '--kslack', str(a.kslack)], input=payload, text=True, capture_output=True, timeout=7200)
            if res.returncode == 0: return parse(res.stdout)
            print('shard fail', i, res.returncode, flush=True)
        return {}
    gained = 0; n = 0
    with ThreadPoolExecutor(a.shards) as ex:
        for props in ex.map(run, range(a.shards)):
            for k, prog in props.items():
                if len(prog) < len(cur[k]) and check(P[k], prog) is None:
                    gained += len(cur[k]) - len(prog); n += 1; cur[k] = prog
    write_submission(a.out, cur)
    print(f'round {r+1}/{a.rounds}: selected {len(sel)}, improved {n}, saved {gained}, total {sum(len(v) for v in cur.values())}, {time.time()-t0:.0f}s', flush=True)
