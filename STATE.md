# STATE (updated 2026-11-18)

Goal: top 10 (need about 137.5k; #1 132.6k). Metric: total instructions, lower is better, exact locally.

## Current best
- best/best.csv = 142,313 (submitted). Mostly public programs (konbu17 v10, public-merge) plus own solver wins on a few puzzles.
- Backup copy: subs/best_142313.csv

## What worked (see EXPERIMENTS.md)
- Keep targets/starts in registers, greedy order, three-term terminal, product approximation.
- Virtual helper leaves (-V 2): -2% practice, -0.8% scored.
- Reuse-aware eviction (-k 4 -uw 80): -4.2% on big-target benchmark (data/bench_big.csv).
- Per-puzzle min merge of everything (public + own).

## What failed
- Wider beams, additive approx, palette in registers, -k 2/3, bigger helper sets, suffix re-solve with our solver (0 gain).

## Key finding
- Our per-target search is as good as public; the gap is what we leave in registers for later targets (+40% on the rest of the program from public states).

## Running
- Background: full scored runs u_1 (-k 4 -uw 80) and u_2 (+ -H 128) via bin/solver9.exe; merges into best/best.csv automatically.

## Next 3 steps
1. Merge and submit u_1/u_2 results; run benchmark for -uw 80 -H 128 and tune.
2. Rollout/lookahead: choose among several plans for a target by cost of the next few targets.
3. Exact 3-instruction MITM finisher; consider Modal for wide portfolio sweeps.
