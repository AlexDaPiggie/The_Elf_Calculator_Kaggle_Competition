"""Suffix re-solve: keep the best program up to the k-th target, let our solver
rebuild the rest from that register state, keep the shortest valid result.

usage: python src/lns.py exe in.csv out.csv [--ids N] [--step S] [--min-left M] -- [solver args]
Writes the per-puzzle best (input or improved) to out.csv.
"""
import sys, subprocess, json, argparse
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, 'src')
from common import load_puzzles, load_submission, write_submission, check
from dce import dce, run_vals

argv = sys.argv[1:]
sep = argv.index('--') if '--' in argv else len(argv)
ap = argparse.ArgumentParser()
ap.add_argument('exe'); ap.add_argument('inp'); ap.add_argument('out')
ap.add_argument('--ids', type=int, default=0, help='only first N puzzles (0 = all)')
ap.add_argument('--step', type=int, default=1, help='use every S-th cut point')
ap.add_argument('--min-left', type=int, default=1, help='min targets left after cut')
ap.add_argument('--puzzles', default='data/puzzles.csv')
ap.add_argument('--threads', type=int, default=16)
a = ap.parse_args(argv[:sep]); args = argv[sep + 1:]

P = load_puzzles(a.puzzles)
B = load_submission(a.inp)
keys = list(P)[:a.ids] if a.ids else list(P)


def cuts(p, prog):
    vals = run_vals(p, prog)
    tg = set(p['targets']) - set(p['starting_values'])
    idx = []
    for k, z in enumerate(vals):
        if z in tg:
            idx.append(k); tg.discard(z)
    n = len(idx)
    return [idx[j] + 1 for j in range(0, n - a.min_left, a.step)]


def line(k, prefix):
    p = P[k]
    head = [k, p['value_limit'], len(p['starting_values']), len(p['targets']), *p['starting_values'], *p['targets'], len(prefix)]
    return ' '.join(map(str, head)) + ' ' + ' '.join(f'{op} {x} {y} {d}' for op, x, y, d in prefix)


def work(k):
    prog = B[k]
    lines = [line(k, prog[:c]) for c in cuts(P[k], prog)]
    if not lines:
        return k, prog
    r = subprocess.run([a.exe, '-P', '1', *args], input='\n'.join(lines) + '\n', text=True, capture_output=True)
    best = prog
    for l in r.stdout.splitlines():
        try:
            cand = dce(P[k], json.loads(l.split(' ', 1)[1]))
        except Exception:
            continue
        if len(cand) < len(best) and check(P[k], cand) is None:
            best = cand
    return k, best


out = dict(B)
gain = 0
with ThreadPoolExecutor(a.threads) as ex:
    for i, (k, prog) in enumerate(ex.map(work, keys)):
        d = len(B[k]) - len(prog)
        if d > 0:
            out[k] = prog; gain += d
        if (i + 1) % 50 == 0:
            print(f'{i + 1}/{len(keys)} gain {gain}', flush=True)
write_submission(a.out, out)
print(f'total gain {gain} over {len(keys)} puzzles; new total {sum(len(v) for v in out.values())}')
