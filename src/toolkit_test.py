"""E1: transplant best program's pre-first-target prefix (its toolkit) into our solver via -P prefix mode.
usage: toolkit_test.py exe out.csv puzzles.csv -- solver args"""
import sys, subprocess, json
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, 'src')
from common import *
from dce import run_vals
argv = sys.argv[1:]; sep = argv.index('--')
exe, out, src = argv[0], argv[1], argv[2]; args = argv[sep + 1:]
P = load_puzzles(src); B = load_submission('best/best.csv')
def line(k, prefix):
    p = P[k]
    head = [k, p['value_limit'], len(p['starting_values']), len(p['targets']), *p['starting_values'], *p['targets'], len(prefix)]
    return ' '.join(map(str, head)) + ' ' + ' '.join(f'{op} {x} {y} {d}' for op, x, y, d in prefix)
def work(k):
    p = P[k]; prog = B[k]; vals = run_vals(p, prog); tg = set(p['targets']) - set(p['starting_values'])
    first = next(i for i, z in enumerate(vals) if z in tg)
    r = subprocess.run([exe, '-P', '1', *args], input=line(k, prog[:first]) + '\n', text=True, capture_output=True)
    l = r.stdout.splitlines()[0]
    return k, json.loads(l.split(' ', 1)[1]), first
res = {}; fs = 0
with ThreadPoolExecutor(12) as ex:
    for k, pr, first in ex.map(work, list(P)):
        res[k] = pr; fs += first
print('toolkit instr total', fs, 'score', sum(len(v) for v in res.values()), 'valid', all(check(P[k], res[k]) is None for k in res))
write_submission(out, res)
