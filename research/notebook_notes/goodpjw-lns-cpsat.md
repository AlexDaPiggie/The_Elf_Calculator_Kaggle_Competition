# goodpjw2008/santa-2026-lns-cp-sat-recombine-lb-135-787
Author: goodpjw2008. Claimed LB 135,787 (-18 vs best public merge 135,805 at the time; 13 puzzles strictly shorter than any public program). Pulled: research/kernels/santa-2026-lns-cp-sat-recombine-lb-135-787. Engine source (Apache 2.0) also inline in royalacecat 135,761 notebook (elfopt.cpp, ~860 lines).

## Method (plain words)
Own C++ re-implementation of prvsiyan's value-DAG LNS, plus 5 additions:
1. Depth-5 "near-miss" product: T = X*Y +- R with Y taken from sorted neighbours of T/X in (pool + one-step values); shapes X,Y,R <=1 step; Y=floor(T/X) in 2 steps; R in 2 steps.
2. Helper-rooted destroy: remove a shared helper + the subtree it dominates (all paths to targets go through it).
3. Multi-order repair + joint pair search (one new helper for 2-3 targets).
4. Plateau walk: equal-length moves p=0.3; after 200 plateau moves without progress, ILS kick = rebuild a random cone allowing +2 instr (--kicks 1000 --kslack 2). A/B 60 puzzles x 15 s: kicks 5 instr vs plain plateau 2.
5. CP-SAT recombination of the SEARCH TRAJECTORY: dump every accepted recipe v=a op b during LNS (--dump), pool with current program, add all cross recipes between pooled values, free-order model with integer levels, minimise #values. Passes gave -45, -28, -4 on top of LNS.
Repair searches all ~100-280 values of the DAG (not just 48 live regs), then re-schedules into 48 (list scheduling, linear scan).

## Key numbers
- Score over time (20 cores, 480 min): 136,829 -> 136,510 in 25 min (-319, 134 puzzles), then slow to 135,787.
- Public LNS re-run on frontier: 0 shorter on 100 puzzles x 15 s.
- Gains only in puzzles of 60-180 instructions: 14 instr per 100 runs at 100-140 length, ~0 above 180. Large independent puzzles (>=180) gain nothing from LNS or recombination.
- By family (their final -18): shared -10, mixed -3, multiplicative -3, independent -2.

## Figures (research/notebook_notes/goodpjw-lns-cpsat/)
- __results___0_0.png dashboard: bars of public files 135,805-135,936 vs 135,787; score-vs-time curve; puzzle map (13 cells -1..-3); example scored_0763 93 -> 92 (two targets re-routed via a new +2 helper 296,034,213,890).
- __results___7_0.png: instr/target vs mean target bits: independent in clusters 30b ~5, 40b ~5.8, 50b ~7.2, 60b ~8.6; shared flat ~4 at all sizes; mixed between. scored_0001: 107 instructions serve 1 target, 55 serve 8+. Length vs #targets: 28-32 target puzzles span 70-280.
- __results___11_0.png: rewrites 0286 128->127, 0617 92->91, 0814 122->121: each replaces 5-9 instructions with a different set of intermediates (not a 1-for-1 swap); targets reused as operands.

## What failed (their list)
- Greedy constructive with depth-5: scored_0001 271 vs 230 public, 70 live values (>48).
- Full depth-5 MITM over 10-19M two-step values: 0 hits on 9 targets of 48-59 bits (two-step values too sparse near 2^55).
- CP-SAT with fixed order: 0 on 8 puzzles (only free order with level vars gains). Adding bridge intermediates or all <=3-instr alternatives (300-900 values): model too big for 30 s.
- Hidden generator chains t_j = m*t_i + r: nothing cheaper.

## Reusable for us
- elfopt flags: --time --eq 0.3 --kicks N --kslack 2 --dump file --hall 1 --alts K --construct N. Driver: shard best file, fresh seeds per round, keep strictly shorter.
- Function names: Searcher::find/find4/findWindow (near-miss), LNS::tryRemove/dominated/doKick/harvest, Dag::fixPressure/listSchedule/emit.
- Pair with IceFire cpsat_plan (Python) for recombining the dumped trajectory.

## Already in our log?
- We ran prvsiyan lns.cpp (6 instr, INCONCLUSIVE per skeptic). Kicks, near-miss depth 5, trajectory recombination: NOT tried. Puzzle-size filter 60-180: NOT used (we ordered by worst ratio).
