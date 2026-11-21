"""Pebbling compiler: compile a program that uses many registers (indices may exceed 47) into 48 registers,
re-computing evicted values when they are needed again. Plan order is kept; eviction uses
min(rebuild_cost^P / next_use_distance) (konbu-style), dead values first, start values pinned.
usage: pebble.py wide.csv puzzles.csv out.csv"""
import sys, json
from concurrent.futures import ProcessPoolExecutor
sys.path.insert(0, 'src')
from common import *

def ssa_wide(p, prog):
    reg = {}
    for i, v in enumerate(p['starting_values']): reg[i] = v
    seq = []; seen = set(p['starting_values'])
    for op, a, b, d in prog:
        x, y = reg[a], reg[b]
        v = {'+': x + y, '-': x - y, '*': x * y, '/': x // y}[op]; reg[d] = v
        if v not in seen: seen.add(v); seq.append((v, op, x, y))
    return seq

def compile_(p, seq, P=2.0, lookw=1.0):
    starts = list(p['starting_values']); S = set(starts); T = set(p['targets'])
    recipe = {v: (op, x, y) for v, op, x, y in seq}
    uses = {}
    for j, (v, op, x, y) in enumerate(seq):
        uses.setdefault(x, []).append(j); uses.setdefault(y, []).append(j)
    reg = [None] * 48
    for i, v in enumerate(starts): reg[i] = v
    where = {v: i for i, v in enumerate(starts)}
    prog = []; cur = [0]
    INF = 10 ** 9
    def next_use(v):
        for j in uses.get(v, ()):
            if j >= cur[0]: return j
        return None
    def cost(v, depth=0):
        if v in where: return 0
        if v in S or v not in recipe: return INF
        if depth > 3: return 3
        op, x, y = recipe[v]
        return 1 + cost(x, depth + 1) + cost(y, depth + 1)
    def free_reg(protect):
        best = None; bk = None
        for r in range(48):
            u = reg[r]
            if u is None: return r
            if u in protect: continue
            nu = next_use(u)
            if u in S: key = 1e30  # start values cannot be rebuilt and may be needed by recomputation: pinned
            elif nu is None: key = -1.0  # dead
            else:
                if u in S: key = 1e30  # start values cannot be rebuilt: keep while still needed
                else:
                    c = 1 + cost(recipe[u][1]) + cost(recipe[u][2]) if u in recipe else INF
                    key = (min(c, 1e6) ** P) / (1 + (nu - cur[0])) ** lookw
            if bk is None or key < bk: bk = key; best = r
        return best
    def ensure(v, protect, depth=0):
        if v in where: return where[v]
        if v in S or v not in recipe or depth > 60: raise RuntimeError('unrecomputable')
        op, x, y = recipe[v]
        pr = protect | {v}
        rx = ensure(x, pr, depth + 1); ry = ensure(y, pr | {x}, depth + 1)
        if where.get(x) != rx: rx = where[x]
        pr2 = pr | {x, y}
        d = free_reg(pr2)
        if d is None: raise RuntimeError('no register')
        old = reg[d]
        if old is not None: del where[old]
        prog.append([op, where[x], where[y], d]); reg[d] = v; where[v] = d
        return d
    try:
        for j, (v, op, x, y) in enumerate(seq):
            cur[0] = j
            if v in where: continue
            ensure(v, frozenset())
        # all targets must have appeared at some time: they are in seq or starts
    except RuntimeError:
        return None
    return prog

def work(a):
    k, p, prog = a
    seq = ssa_wide(p, prog); best = None
    for P in (1.0, 2.0, 3.0):
        for lw in (1.0, 2.0):
            c = compile_(p, seq, P, lw)
            if c is not None and check(p, c) is None and (best is None or len(c) < len(best)): best = c
    return k, best, len(seq)

if __name__ == '__main__':
    wide, src, out = sys.argv[1:4]
    P = load_puzzles(src); W = json.load(open(wide)) if wide.endswith('.json') else {k: v for k, v in load_submission(wide).items()}
    res = {}; tw = tc = 0; fail = 0
    with ProcessPoolExecutor(6) as ex:
        for k, c, n in ex.map(work, [(k, P[k], W[k]) for k in P if k in W]):
            tw += n
            if c is None: fail += 1; print(k, 'FAIL wide', n, flush=True); continue
            res[k] = c; tc += len(c); print(k, 'wide', n, 'compiled', len(c), flush=True)
    print('puzzles', len(res), 'fail', fail, 'wide total', tw, 'compiled total', tc)
    write_submission(out, res)
