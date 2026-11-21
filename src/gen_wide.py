"""Run solver16s with -R N and save the (possibly >48-register) programs. usage: gen_wide.py R puzzles.csv out.csv -- solver args"""
import sys, subprocess, json
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, 'src')
from common import *
R, src, out = sys.argv[1:4]; args = sys.argv[sys.argv.index('--') + 1:]
P = load_puzzles(src)
def run(k):
    p = P[k]
    line = ' '.join(map(str, (k, p['value_limit'], len(p['starting_values']), len(p['targets']), *p['starting_values'], *p['targets'])))
    r = subprocess.run(['./bin/solver16s.exe', '-R', R, *args], input=line + '\n', text=True, capture_output=True)
    return k, (json.loads(r.stdout.split(' ', 1)[1]) if r.returncode == 0 and r.stdout.strip() else None)
with ThreadPoolExecutor(8) as ex: res = dict(ex.map(run, list(P)))
res = {k: v for k, v in res.items() if v}
write_submission(out, res); print('saved', len(res), 'total', sum(len(v) for v in res.values()))
