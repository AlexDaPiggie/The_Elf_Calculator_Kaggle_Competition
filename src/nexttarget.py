"""Search-quality probe: from the public program's state right after target j,
ask our solver to build only target j+1, and compare with the public segment cost.

usage: python src/nexttarget.py exe [puzzles.csv] -- [solver args]
"""
import sys, subprocess, json
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, 'src')
from common import load_puzzles, load_submission
from dce import run_vals

argv = sys.argv[1:]
sep = argv.index('--') if '--' in argv else len(argv)
pos, args = argv[:sep], argv[sep + 1:]
exe = pos[0]
P = load_puzzles(pos[1] if len(pos) > 1 else 'data/bench_big.csv')
B = load_submission('best/best.csv')


def work(k):
    p, prog = P[k], B[k]
    vals = run_vals(p, prog)
    tg = set(p['targets']) - set(p['starting_values'])
    idx, order = [], []
    for i, z in enumerate(vals):
        if z in tg:
            idx.append(i); order.append(z); tg.discard(z)
    res = []
    lines = []
    for j in range(2, len(idx) - 1, 3):  # sample cut points
        c = idx[j] + 1
        t = order[j + 1]
        pub = idx[j + 1] - idx[j]
        pre = prog[:c]
        head = [k, p['value_limit'], len(p['starting_values']), 1, *p['starting_values'], t, len(pre)]
        lines.append(' '.join(map(str, head)) + ' ' + ' '.join(f'{o} {x} {y} {d}' for o, x, y, d in pre))
        res.append((c, pub))
    r = subprocess.run([exe, '-P', '1', *args], input='\n'.join(lines) + '\n', text=True, capture_output=True)
    out = []
    for (c, pub), l in zip(res, r.stdout.splitlines()):
        ours = len(json.loads(l.split(' ', 1)[1])) - c
        out.append((pub, ours))
    return out


allr = []
with ThreadPoolExecutor(16) as ex:
    for o in ex.map(work, list(P)):
        allr += o
pub = sum(a for a, b in allr); ours = sum(b for a, b in allr)
better = sum(1 for a, b in allr if b < a); worse = sum(1 for a, b in allr if b > a)
print(f'n={len(allr)} public {pub} ours {ours} ({100*(ours-pub)/pub:+.1f}%) ours better {better} worse {worse}')
