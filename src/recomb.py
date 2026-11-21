"""E6: recombine several programs of the same puzzle by choosing a minimal value set over the union of their recipes
(plus one-op cross recipes among pooled values), via MILP with lazy acyclicity cuts, then compile to 48 registers (no recompute).
usage: recomb.py out.csv puzzles.csv prog1.csv [prog2.csv ...]   (first file = incumbent best)"""
import sys, json, random, time
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import coo_matrix
sys.path.insert(0, 'src')
from common import *

def ssa(p, prog):
    reg = [None] * 48
    for i, v in enumerate(p['starting_values']): reg[i] = v
    out = []
    for op, a, b, d in prog:
        x, y = reg[a], reg[b]
        v = {'+': x + y, '-': x - y, '*': x * y, '/': x // y if y else 0}[op]
        reg[d] = v; out.append((v, op, x, y))
    return out

def pool(p, progs):
    S = set(p['starting_values']); R = {}
    for prog in progs:
        for v, op, x, y in ssa(p, prog):
            if v not in S: R.setdefault(v, set()).add((op, x, y))
    U = set(R) | S
    L = p['value_limit']; Ul = sorted(U)
    for x in Ul:
        for y in Ul:
            for op in '+-*/':
                if op == '+': v = x + y
                elif op == '-': v = x - y
                elif op == '*': v = x * y
                else: v = x // y if y and x % y == 0 else 0
                if 0 < v <= L and v in R: R[v].add((op, x, y))
    return S, R


def solve_highs(c, A, lo, hi, lb, ub, integ, x0, tl):
    import highspy
    h = highspy.Highs(); h.setOptionValue('output_flag', False); h.setOptionValue('time_limit', float(tl)); h.setOptionValue('threads', 1)
    lp = highspy.HighsLp(); n = len(c); m = A.shape[0]
    lp.num_col_ = n; lp.num_row_ = m; lp.col_cost_ = list(c); lp.col_lower_ = list(lb); lp.col_upper_ = list(ub)
    lp.row_lower_ = [float(v) for v in lo]; lp.row_upper_ = [float(v) for v in hi]
    A = A.tocsr(); lp.a_matrix_.format_ = highspy.MatrixFormat.kRowwise
    lp.a_matrix_.start_ = list(A.indptr); lp.a_matrix_.index_ = list(A.indices); lp.a_matrix_.value_ = list(A.data.astype(float))
    lp.integrality_ = [highspy.HighsVarType.kInteger if i else highspy.HighsVarType.kContinuous for i in integ]
    h.passModel(lp)
    if x0 is not None:
        sol = highspy.HighsSolution(); sol.col_value = [float(v) for v in x0]; h.setSolution(sol)
    h.run()
    x = np.array(h.getSolution().col_value)
    st = h.getModelStatus()
    ok = len(x) == n and st in (highspy.HighsModelStatus.kOptimal, highspy.HighsModelStatus.kTimeLimit, highspy.HighsModelStatus.kInterrupt) and h.getInfo().primal_solution_status == 2
    return (x if ok else None), h.getInfo().objective_function_value

def select(p, S, R, tl=20, rounds=40, warm=None):
    T = set(p['targets']) - S
    vals = sorted(R); vi = {v: i for i, v in enumerate(vals)}
    recs = [(v, op, x, y) for v in vals for (op, x, y) in sorted(R[v])]
    nv, nr = len(vals), len(recs); n = nv + nr + nv; M = nv + 1  # last nv variables: ordering levels (acyclicity)
    rows, cols, dat = [], [], []; lo, hi = [], []; row = 0
    byv = {}
    for k, (v, op, x, y) in enumerate(recs): byv.setdefault(v, []).append(k)
    for v in vals:  # z_v <= sum r
        rows.append(row); cols.append(vi[v]); dat.append(1)
        for k in byv[v]: rows.append(row); cols.append(nv + k); dat.append(-1)
        lo.append(-np.inf); hi.append(0); row += 1
    for k, (v, op, x, y) in enumerate(recs):
        for z in {x, y}:
            if z in vi:
                rows += [row, row]; cols += [nv + k, vi[z]]; dat += [1, -1]; lo.append(-np.inf); hi.append(0); row += 1
            elif z not in S: break  # operand unavailable: forbid recipe
        else: continue
        rows.append(row); cols.append(nv + k); dat.append(1); lo.append(-np.inf); hi.append(0); row += 1
    for k, (v, op, x, y) in enumerate(recs):  # r_k = 1 -> level(v) >= level(operand) + 1
        for z in {x, y}:
            if z in vi:
                rows += [row, row, row]; cols += [nv + nr + vi[v], nv + nr + vi[z], nv + k]; dat += [1, -1, -M]; lo.append(1 - M); hi.append(np.inf); row += 1
    cuts = []
    lb = np.zeros(n); ub = np.ones(n); ub[nv + nr:] = nv
    for t in T:
        if t not in vi: return None
        lb[vi[t]] = 1
    c = np.concatenate([np.ones(nv), np.zeros(nr + nv)])
    integ = np.concatenate([np.ones(nv + nr), np.zeros(nv)])
    x0 = None
    if warm is not None:  # warm = ssa(best): feasible assignment from the incumbent program
        x0 = np.zeros(n); pos = {}
        for i, (v, op, x, y) in enumerate(warm):
            if v in vi and v not in pos: pos[v] = i + 1; x0[vi[v]] = 1; x0[nv + nr + vi[v]] = i + 1
        for k, (v, op, x, y) in enumerate(recs):
            if v in pos and any(w == v and o == op and a == x and b == y and True for (w, o, a, b) in warm[pos[v] - 1:pos[v]]): x0[nv + k] = 1
    for _ in range(rounds):
        A = coo_matrix((dat, (rows, cols)), shape=(row, n)).tocsr()
        cons = [LinearConstraint(A, lo, hi)]
        if cuts:
            rr, cc, dd = [], [], []
            for i, cut in enumerate(cuts):
                for k in cut: rr.append(i); cc.append(nv + k); dd.append(1)
            cons.append(LinearConstraint(coo_matrix((dd, (rr, cc)), shape=(len(cuts), n)).tocsr(), -np.inf, [len(c_) - 1 for c_ in cuts]))
        xs, fun = solve_highs(c, A_all(A, cons), None, None, lb, ub, integ, x0, tl) if False else (None, 0)
        res = milp(c, constraints=cons, integrality=integ, bounds=Bounds(lb, ub), options={'time_limit': tl}) if x0 is None else None
        if x0 is not None:
            Aall = A if not cuts else __import__('scipy.sparse', fromlist=['vstack']).vstack([A, cons[1].A])
            loall = list(lo) + ([-np.inf] * len(cuts)); hiall = list(hi) + [len(c_) - 1 for c_ in cuts]
            xs, fun = solve_highs(c, Aall, loall, hiall, lb, ub, integ, x0, tl)
            class _R: pass
            res = _R(); res.x = xs; res.fun = fun; res.status = 'highs'; res.message = 'highs fail'
        if res.x is None:
            print('milp fail', res.status, res.message[:80], file=sys.stderr, flush=True); return None
        x = res.x
        chosen = {}
        for v in vals:
            if x[vi[v]] > .5:
                ks = [k for k in byv[v] if x[nv + k] > .5]
                if ks: chosen[v] = recs[ks[0]]; chosen[('k', v)] = ks[0]
        # cycle check from targets
        state = {}; cyc = None
        def dfs(v, path):
            nonlocal cyc
            if cyc or v in S or v not in chosen: return
            if state.get(v) == 1: cyc = path[path.index(v):]; return
            if state.get(v) == 2: return
            state[v] = 1; _, op, a, b = chosen[v]
            for u in (a, b): dfs(u, path + [v] if u != v else path + [v])
            state[v] = 2
        for t in sorted(T): dfs(t, [])
        print('round', _, 'obj', res.fun, 'cyc', None if cyc is None else len(cyc), file=sys.stderr, flush=True) if __import__('os').environ.get('RCDBG') else None
        if cyc is None:
            return {v: chosen[v] for v in vals if v in chosen and not isinstance(v, tuple)}
        cuts.append([chosen[('k', v)] for v in cyc])
    return None

def compile48(p, S, ch):
    T = set(p['targets']) - S
    def build(order_t):
        seq, done = [], set(S)
        def go(v):
            if v in done: return
            done.add(v); _, op, a, b = ch[v]; go(a); go(b); seq.append(v)
        for t in order_t: go(t)
        return seq
    cands = [sorted(T), sorted(T, reverse=True)]
    rng = random.Random(1)
    for _ in range(30):
        o = sorted(T); rng.shuffle(o); cands.append(o)
    for order_t in cands:
        seq = build(order_t)
        # liveness
        use = {}
        for i, v in enumerate(seq):
            _, op, a, b = ch[v]; use[a] = i; use[b] = i
        reg = [None] * 48; prog = []
        starts = list(p['starting_values'])
        for i, v in enumerate(starts): reg[i] = v
        ok = True
        for i, v in enumerate(seq):
            _, op, a, b = ch[v]
            ra, rb = reg.index(a), reg.index(b)
            dst = None
            for r in range(48):
                u = reg[r]
                if u is None or (use.get(u, -1) <= i and u not in (None,) and not (u == a and use.get(a, -1) > i) and not (u == b and use.get(b, -1) > i)):
                    dst = r; break
            if dst is None: ok = False; break
            prog.append([op, ra, rb, dst]); reg[dst] = v
        if ok: return prog
    return None

def work(args):
    k, p, progs = args
    t0 = time.time(); S, R = pool(p, progs)
    ch = select(p, S, R, tl=int(__import__('os').environ.get('RC_TL', 20)), warm=ssa(p, progs[0]))
    if ch is None: return k, None, 0, len(R), time.time() - t0
    # reachable length
    reach = set(); st = [t for t in set(p['targets']) - S]
    while st:
        v = st.pop()
        if v in reach or v in S: continue
        reach.add(v); _, op, a, b = ch[v]; st += [a, b]
    ch = {v: ch[v] for v in reach}
    prog = compile48(p, S, ch)
    return k, prog, len(reach), len(R), time.time() - t0

if __name__ == '__main__':
    out, src = sys.argv[1], sys.argv[2]; files = sys.argv[3:]
    P = load_puzzles(src); banks = [load_submission(f) for f in files]
    jobs = [(k, P[k], [b[k] for b in banks if k in b]) for k in P]
    res = {}; wins = 0; gain = 0; milp_better = 0
    with ProcessPoolExecutor(6) as ex:
        for k, prog, mlen, npool, dt in ex.map(work, jobs):
            inc = len(banks[0][k]); ok = prog is not None and check(P[k], prog) is None
            tag = 'WIN' if ok and len(prog) < inc else ('lb<inc' if mlen and mlen < inc else '')
            print(k, 'best', inc, 'milp', mlen, 'compiled', len(prog) if ok else None, 'pool', npool, f'{dt:.0f}s', tag, flush=True)
            if ok and len(prog) < inc: res[k] = prog; wins += 1; gain += inc - len(prog)
            if mlen and mlen < inc: milp_better += 1
    print('wins', wins, 'gain', gain, 'milp_lb_better', milp_better, 'of', len(P))
    base = dict(banks[0]); base.update(res); write_submission(out, base)
