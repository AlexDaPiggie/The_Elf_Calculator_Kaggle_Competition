# prvsiyan/santa-is-not-happy
Author: prvsiyan. Notebook merges Pratham Jain 138,441 output with its own warm start (public portfolios + own offline lanes); Kaggle run gives 4 workers 1 minute on 30 puzzles. Pulled: research/kernels/santa-is-not-happy (code read in sota_2026-11-19).

## Method (plain words)
"Hidden-program view": targets are sinks of an unknown arithmetic graph; a hub H has children m*H + r.
- lns.cpp: value-DAG LNS. Remove a set R (target exclusive cone), rebuild with exact depth <= 3 hash inversion + streamed depth-4 MITM over ALL DAG values, equal-cost moves with prob --eq 0.3, "helper move" = insert one shared helper h serving >= 2 targets; re-schedule into 48 registers. Puzzles ordered by (len - targets)/targets.
- poolc.cpp: planted-pool constructor. Grow pool K (starts first); each step add the hidden value h in F1 = K (+) K (one op over K) that brings the most uncovered targets to one op (t = h op k); targets one op away are taken at once; else two-helper construction t = f op g (f, g in F1), then a split encoder. Tested on a simulator with known hidden programs.
- relink.py / relink2.py: T = P*m +- r from an earlier hub; dominator-tree private sets.

## Key numbers
- Kaggle run: 36 s, 0 improved. Offline lane held 38 puzzles in the 137.9k era, 5 exclusive (6 instr).
- Our own run of lns.cpp on best (EXPERIMENTS 2026-11-19): run 1 6 instr (real merge gain 2), run 2 0 (possible silent crash). INCONCLUSIVE per skeptic.

## Figures
Result histogram "instructions saved" only (not extracted).

## Reusable for us
- poolc.cpp greedy hub-pool constructor is the only public CONSTRUCTIVE method built on the hidden-hub model; could seed our solver's virtual leaves with its pool instead of fixed constants.
- goodpjw rebuilt this LNS and added kicks + near-miss depth 5 + trajectory recombination, which is what made it productive (their note: plain public LNS = 0 on the frontier).

## Failed
- Short Kaggle budgets: 0.

## Already in our log?
- lns.cpp run (inconclusive), hub view = sota idea 3. poolc.cpp never run by us.
