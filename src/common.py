"""Load puzzles, validate and score programs."""
import csv, json, sys
csv.field_size_limit(10**9)
OPS = {'+', '-', '*', '/'}

def load_puzzles(path):
    out = {}
    with open(path, newline='') as f:
        for r in csv.DictReader(f):
            r['starting_values'] = json.loads(r['starting_values'])
            r['targets'] = json.loads(r['targets'])
            r['value_limit'] = int(r['value_limit'])
            r['registers'] = int(r['registers'])
            out[r['id']] = r
    return out

def load_submission(path):
    with open(path, newline='') as f:
        return {r['id']: json.loads(r['program']) for r in csv.DictReader(f)}

def write_submission(path, progs):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['id', 'program'])
        for k in sorted(progs):
            w.writerow([k, json.dumps(progs[k], separators=(',', ':'))])

def check(p, prog):
    """Return None if valid else error string."""
    if len(prog) > 4096: return 'too long'
    if len(json.dumps(prog).encode()) > 131072: return 'too many bytes'
    R = p['registers']; L = p['value_limit']
    reg = [None] * R
    for i, v in enumerate(p['starting_values']): reg[i] = v
    need = set(p['targets']) - set(p['starting_values'])
    for k, ins in enumerate(prog):
        op, a, b, d = ins
        if op not in OPS: return f'{k}: bad op'
        for x in (a, b, d):
            if not (isinstance(x, int) and 0 <= x < R): return f'{k}: bad reg'
        x, y = reg[a], reg[b]
        if x is None or y is None: return f'{k}: undefined src'
        if op == '+': z = x + y
        elif op == '-':
            if x <= y: return f'{k}: nonpositive sub'
            z = x - y
        elif op == '*': z = x * y
        else:
            if x % y: return f'{k}: inexact div'
            z = x // y
        if z > L: return f'{k}: over limit'
        reg[d] = z
        need.discard(z)
    if need: return f'missing {len(need)} targets'
    return None

def score(puzzles, progs, verbose=True):
    tot = 0
    for k, p in puzzles.items():
        if k not in progs: raise ValueError(f'missing {k}')
        e = check(p, progs[k])
        if e: raise ValueError(f'{k}: {e}')
        tot += len(progs[k])
    return tot
