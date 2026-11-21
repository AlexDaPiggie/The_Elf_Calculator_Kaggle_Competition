"""Planned program LENGTH with R virtual registers (programs with R>48 are NOT valid for submission). usage: regs_test.py R puzzles.csv -- solver args"""
import sys, subprocess, json
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, 'src')
from common import *
R = sys.argv[1]; src = sys.argv[2]; args = sys.argv[sys.argv.index('--') + 1:]
P = load_puzzles(src)
def run(k):
    p = P[k]
    line = ' '.join(map(str, (k, p['value_limit'], len(p['starting_values']), len(p['targets']), *p['starting_values'], *p['targets'])))
    r = subprocess.run(['./bin/solver16s.exe', '-R', R, *args], input=line + '\n', text=True, capture_output=True)
    if r.returncode: return k, None
    return k, len(json.loads(r.stdout.split(' ', 1)[1]))
with ThreadPoolExecutor(6) as ex:
    res = dict(ex.map(run, list(P)))
print('R', R, 'total', sum(v for v in res.values() if v), 'failed', sum(v is None for v in res.values()), json.dumps(res))
