"""Dead-code elimination for Elf Calculator programs.

Removes instructions whose result is never read and that are not the first
producer of a target. Usage: python src/dce.py in.csv out.csv [puzzles.csv]
"""
import sys
from common import load_puzzles, load_submission, write_submission, check


def run_vals(p, prog):
    reg = [None] * p['registers']
    for i, v in enumerate(p['starting_values']):
        reg[i] = v
    out = []
    for op, a, b, d in prog:
        x, y = reg[a], reg[b]
        z = x + y if op == '+' else x - y if op == '-' else x * y if op == '*' else x // y
        reg[d] = z
        out.append(z)
    return out


def dce(p, prog):
    while True:
        vals = run_vals(p, prog)
        tg = set(p['targets']) - set(p['starting_values'])
        first = set()
        for k, z in enumerate(vals):
            if z in tg:
                first.add(k)
                tg.discard(z)
        live = set()
        keep = [False] * len(prog)
        for k in range(len(prog) - 1, -1, -1):
            op, a, b, d = prog[k]
            if d in live or k in first:
                keep[k] = True
                live.discard(d)
                live.add(a)
                live.add(b)
        new = [ins for k, ins in enumerate(prog) if keep[k]]
        if len(new) == len(prog):
            return prog
        prog = new


if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    P = load_puzzles(sys.argv[3] if len(sys.argv) > 3 else 'data/puzzles.csv')
    S = load_submission(src)
    before = after = 0
    for k, prog in S.items():
        new = dce(P[k], prog)
        if check(P[k], new) is None:
            S[k] = new
        before += len(prog)
        after += len(S[k])
    write_submission(dst, S)
    print(f'dce: {before} -> {after} (gain {before - after})')
