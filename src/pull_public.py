"""Poll public santa-2026 kernels, download new outputs, merge shorter valid programs into best/best.csv,
submit if the total improved. Uses Kaggle account token 1 only.
usage: python src/pull_public.py [--loop MIN]"""
import sys, os, re, json, csv, subprocess, time, glob, shutil
sys.stdout.reconfigure(encoding='utf-8', errors='replace'); sys.stderr.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, 'src')
from common import *
csv.field_size_limit(1 << 30)
os.environ['KAGGLE_API_TOKEN'] = os.environ['KAGGLE_API_TOKEN_1']
for _v in ('KAGGLE_USERNAME', 'KAGGLE_KEY'): os.environ.pop(_v, None)  # never fall back to another account
import tempfile
os.environ['KAGGLE_CONFIG_DIR'] = tempfile.mkdtemp(prefix='kagglecfg_')  # empty dir: no kaggle.json fallback to another account
SEEN = 'ext/seen.json'
P = load_puzzles('data/puzzles.csv')

def sh(cmd, timeout=300):
    env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONUTF8='1')
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, encoding='utf-8', errors='replace', env=env)

def list_kernels():
    res = {}
    for sort in ('dateRun', 'voteCount', 'dateCreated', 'scoreAscending'):
        out = sh(['kaggle', 'kernels', 'list', '--competition', 'santa-2026', '--sort-by', sort, '--page-size', '60', '--csv']).stdout
        if 'ref,' not in out: continue
        for r in csv.DictReader(out[out.index('ref,'):].splitlines()):
            res[r['ref'].strip("b'\"")] = r.get('lastRunTime', '')
    return list(res.items())

def programs_in(path):
    """yield (id, program) from any csv with id and program columns"""
    try:
        rd = csv.DictReader(open(path, encoding='utf-8', newline=''))
        if not rd.fieldnames or 'id' not in rd.fieldnames or 'program' not in rd.fieldnames: return {}
        return {r['id']: json.loads(r['program']) for r in rd}
    except Exception:
        return {}

def once():
    seen = json.load(open(SEEN)) if os.path.exists(SEEN) else {}
    best = load_submission('best/best.csv'); total0 = sum(len(v) for v in best.values())
    new = [(r, t) for r, t in list_kernels() if seen.get(r) != t]
    newseen = {}
    print(time.strftime('%H:%M'), 'kernels', len(new), 'new/changed; best', total0, flush=True)
    for ref, t in new:
        d = 'ext/poll/' + ref.replace('/', '__'); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
        try:
            rr = sh(['kaggle', 'kernels', 'output', ref, '-p', d], 300)
            if rr.returncode: print('fail', ref, rr.stderr[-100:]); continue
        except Exception as e: print('fail', ref, e); continue
        newseen[ref] = t
        for f in glob.glob(d + '/**/*.csv', recursive=True):
            progs = programs_in(f)
            if not progs: continue
            ok = {}
            for k, v in progs.items():
                try:
                    if k in P and check(P[k], v) is None: ok[k] = v
                except Exception: pass
            gain = sum(len(best[k]) - len(v) for k, v in ok.items() if k in best and len(v) < len(best[k]))
            if gain > 0:
                for k, v in ok.items():
                    if k in best and len(v) < len(best[k]): best[k] = v
                print(' ', ref, f, 'gain', gain, flush=True)
    total1 = sum(len(v) for v in best.values())
    if total1 >= total0:
        seen.update(newseen); json.dump(seen, open(SEEN, 'w'))
    if total1 < total0:
        assert len(best) == len(P) and all(check(P[k], best[k]) is None for k in P)
        fn = f'subs/best_{total1}.csv'; write_submission(fn, best)
        r = sh(['kaggle', 'competitions', 'submit', 'santa-2026', '-f', fn, '-m', f'auto merge public: {total1}'], 300)
        okSub = r.returncode == 0 and 'Successfully' in (r.stdout + r.stderr)
        print('SUBMITTED' if okSub else 'SUBMIT FAILED', total1, (r.stdout + r.stderr)[-120:].replace('\n', ' '), flush=True)
        if not okSub: return  # seen not saved: same kernels are re-merged next poll
        seen.update(newseen); json.dump(seen, open(SEEN, 'w'))
        shutil.copy(fn, 'best/best.csv')
        with open('SUBMISSIONS.md', 'a') as f: f.write(f"| auto | {time.strftime('%Y-%m-%d')} | {fn} | {total1} | auto poll of public kernel outputs, all programs validated |\n")
        with open('EXPERIMENTS.md', 'a') as f: f.write(f"- Auto poll: merged public outputs, best {total0} -> {total1}, submitted {fn}.\n")

if __name__ == '__main__':
    mins = int(sys.argv[sys.argv.index('--loop') + 1]) if '--loop' in sys.argv else 0
    while True:
        try: once()
        except Exception as e: print('error', repr(e)[:300], flush=True)
        if not mins: break
        time.sleep(mins * 60)
