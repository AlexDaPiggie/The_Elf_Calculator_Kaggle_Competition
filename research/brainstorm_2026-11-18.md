# Brainstorm 2026-11-18 (stuck protocol steps 2-6) - next 5 experiments

Inputs read: STATE, EXPERIMENTS, STRATEGY, sota/stuck notes, ANTI_PATTERNS, ext/asterios/experiments.csv (E01-E17),
research/kernels (suka, joint recipes, shared helpers, Bos-Coster, first-target, sqrt-lattice), src/solver.cpp.
New numbers below come from quick read-only DAG scripts (seconds, no solver runs) on best/best.csv,
subs/bench_L5.csv, subs/best_141127.csv, subs/best_139011.csv.

## 2. Error analysis (bench_big, 60 puzzles, 1,809 targets: best 10,493 vs own L5 13,209)
| per puzzle set | best | own L5 |
|---|---:|---:|
| non-target values used once (per target) | 4,476 (2.5) | 8,089 (4.5) |
| non-target values used >= 2 (per target) | 4,208 (2.3) | 3,298 (1.8) |
| mid values (17-40 bit) used once | 2,611 | 5,169 |
| small values (<= 16 bit) used once | 425 | 1,487 |
| big values (> 40 bit) used >= 2 | 157 | 72 |
| targets used as operands | 116 | 41 |
| registers at half program: small / mid / big / target | 23.7 / 17.0 / 2.4 / 3.9 | 22.7 / 21.6 / 2.4 / 1.4 |
- The gap is throwaway intermediates: we build ~2 extra single-use values per target (1.4 mid, 0.6 small).
  Best spends ~0.5 more per target on shared values and saves ~2 on private ones.
- Register mix by size is the same. So the problem is WHICH values we hold, not how many of each size.
- Overlap: best's mid/big values appear in ANY of our 5 bench runs only 1-3% (small hubs 25%). They appear
  73-89% in the old public 142k file. Public frontier = one lineage. Recombining our DAGs with public: dead.
- Suka diff (383 puzzles where 139,011 < 141,127, total -2,116, median -2/puzzle):
  common instruction prefix median 0%, target order different in 383/383, first target LATER
  (median position 14 -> 23, bigger toolkit), yet 40% of new mid/big values (53% small) exist in the old program.
  => suka is a whole-program re-solve (not a suffix edit) that reuses many old intermediates and buys a bigger toolkit.
- Fix for worst 10%: not per-target search (probe: ours -4% on one target from public state). It is making
  intermediates that later targets reuse, plus a larger, puzzle-specific toolkit.

## 3. Re-read: what public does that we do not
- Their search always contains the incumbent (suffix re-solve / recombination edit their own lineage). Our suffix
  re-solve (Reframe A, 0 gain) could not even reproduce the public suffix: their intermediates were not in our dict.
- Atakan CP-SAT joint recipes: candidates only from existing public DAGs (46 instr). Nobody feeds a beam's
  alternative plans into a joint selection.
- Toolkit: public invests 14-23 instr before the first target; suka grows it further and wins.
- E16 (asterios): rebuilding at original positions gains, rebuilding at the end never does.

## 4. Three reframes
R1. State value, not next-target cost (sequential, better objective).
- Represent a partial program by its register state; value = own cost so far + estimated cost of ALL remaining
  targets from that state. Lookahead L3 -> L5 kept paying (-3.3%, -1.5%) using only the cheapest next target.
- Key fact: Solver::nextBest already runs searchT on every remaining target and keeps only the min. Sum/mean is free.
- Cheapest test = E2 (-LW). Stop: no subset gain <= -0.7% vs L5 at any weight -> drop R1 (and E4).

R2. Two-level: toolkit first, targets second (choose toolkit by total cost).
- Phase 1 picks ~20-30 small/mid hub values per puzzle; phase 2 runs our solver with hubs live.
  Past failures were FIXED palettes (p1/p2 +0.5%, asterios E15 base powers +44..+168). Untested: puzzle-specific
  toolkit chosen by the real total. Suka's later first target says it matters.
- Cheapest test = E1 (transplant best's toolkit through existing -P prefix mode). Stop: gap closes < 1/3 -> drop R2.

R3. Order-free joint selection (whole program as a DAG).
- For each target, generate top-M plans (incl. equal-cost alternatives) from a fixed state; choose one plan per
  target minimizing |union of new values| (set cover / CP-SAT); add chosen values as free leaves and regenerate
  plans (column generation); then topological order + register allocation. Attacks "private 4.5 vs 2.5" directly.
- Cheapest test = E5 on 10 puzzles. Stop: scheduled total > own L5 on those 10 -> drop.
- Guide variant (learned beam guide, cheaper): score each equal-cost plan by shareability = number of remaining
  targets whose near-best plans contain its new values; pick max. Offline check first: from public states, does the
  plan public chose rank top on shareability among our equal-cost alternatives in > 50% of targets?

## Suka guess and test (E3)
Guess: fresh greedy re-solve of the whole puzzle where the public program's values are offered as priced leaves
(warm start / value bank), with a different target order and larger toolkit. Fits all 4 facts above:
no common prefix, new order, 40% value reuse, more toolkit. Key property: the incumbent is INSIDE the search
space (every public value is rebuildable via its public recipe), which our suffix re-solve lacked.
Test: see E3. Alternative guess (same lineage solver + more settings, overlap by determinism) is ruled out for us
anyway: we do not have their solver, so the hint route is the one we can run.

## 5. Diversity (from-scratch, different family) = E5 column-generation joint solver
Optimization family (set cover + column generation + scheduler), not greedy-sequential beam.
Components: solver plan-dump flag (-PD M: print top-M plans per target as JSON, needs alternative terminals kept
in Search at cost == best, NOT relaxed pruning - ANTI_PATTERNS -S); Python driver src/colgen.py: greedy weighted
set cover first (ortools not installed; pip install ortools in global env if greedy shows promise); scheduler =
cheapest-first topological order + linear-scan allocation, evicted-and-needed values rebuilt and counted; validate
with common.check.

## 6. Ranked next 5 (all on the "what stays in registers / which values to build" lever)
| # | Exp | Cost | Expected gain | Why this rank |
|---|---|---|---|---|
| 1 | E2 -LW state-value lookahead | 30 lines, ~1h on 20 bench puzzles | own bench -1 to -3% (13,209 -> 12.8-13.1k); LB 0 direct, feeds E3 | nearly free: data already computed |
| 2 | E1 toolkit transplant | ~40 lines Python, 0-1 line C++, 30 min run | diagnostic; own gap 26% -> 15-20% predicted; LB 0-50 | decides R2; zero risk |
| 3 | E3 hint warm-start (suka guess) | ~80 lines C++, 30 min test, 4-5h full | LB -300 to -1,000 (P ~40%) | only one aimed at beating best now |
| 4 | E4 order beam -B 4 with LW score | ~60 lines, ~2h on 20 puzzles | own -2 to -4% beyond E2 | proven lever, 4x CPU |
| 5 | E5 column-generation joint solver | ~1 day | P ~20%; if it works own -5 to -10% | new family, attacks private-value gap |
Run order: E2 and E1 in parallel now, E3 next with the best engine, E4 if E2 keeps, E5 when CPU is busy.

### E2 details
- In Solver::nextBest return min AND mean of remaining costs (skip unreachable). In runGreedy lookahead (the
  `LA > 1` block): tot = pl.size() + min + LW * mean. New flags -LW w, -LM m (mean of cheapest m only; far targets noisy).
- Grid on first 20 ids of data/bench_big.csv, -L 5 -k 4 -uw 80 -V 2: LW 0.5 / 1 / 2, LM 0 / 5. Baseline = bench_L5
  rows for the same 20 ids. Same runtime as -L 5. Stop: best arm <= -0.7% -> full bench; else drop.
- Add-on (R3 guide, cheap): -A M = among equal-cost terminals of the chosen target, pick the one with best LW score.

### E1 details
- src/toolkit_prefix.py: SSA of best program; toolkit = non-target values <= 16 bits used >= 3 times + ancestor
  closure, in original order, each in its own register 4..47; arm b = best's instructions before first target (DCE).
- Feed via lns.line(k, prefix) to bin/solver10.exe -P 1 -o 3 -L 5 -k 4 -uw 80 -V 2 on the 20 ids.
  1-line C++: keep.insert(v) for replayed prefix values in Solver::run (else -k 4 may evict them; uses=0).
- Read: own+toolkit vs own L5 vs best. Gap closes > 2/3 -> build toolkit search (SA over hub sets scored by fast
  -L 0 solve). < 1/3 -> drop R2. Any puzzle < best -> merge_best.py + submit.

### E3 details
- Input: after targets (and prefix), `nh` + hint instructions (same format as -P). Solver replays them on scratch
  registers -> (value, Recipe). In Solver::makeVirtual add hint values to S with their PUBLIC recipe: cost computed
  in program order (0 if live, else 1 + cost(x) + cost(y)), chains via the existing `chain` lambda; cap -WC 3.
- Arms on 20 ids, -o 3 -L 5: (a) hints = best; (b) (a) + E1 toolkit prefix; (c) hints = union of best,
  ext/suka/submission.csv, ext/konbu17/submission.csv, subs/best_142313.csv (multi-lineage recombination);
  (d) sanity: hints = best + public target order (new -o 4 = input order); should land near best.
- Read: wins (< best) count, total vs best. Stop: 0 wins in all arms and mean gap > 5% -> drop.
  Wins -> 1000-puzzle run (-L 3 locally ~4h, or Modal), merge per puzzle, submit.

### E4 details
- Solver::runBeam: B states; expand top K=3 candidates each (own cost), child score = prog.size() + LW score;
  dedupe children by hash of sorted register values; return min final prog. Stop: < -1% vs E2 on same 20 ids -> keep.

## Do not repeat
Recombination of our DAGs with public (1-3% overlap), suffix re-solve without hints, -S slack, fixed palettes,
wider beams, more portfolio variants of the current solver.
