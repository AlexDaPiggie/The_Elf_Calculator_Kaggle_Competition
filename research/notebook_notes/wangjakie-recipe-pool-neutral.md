# wangjakie/santa-2026-arithmetic-recipe-pool-and-milp (#2 by score-ascending listing)
Author: wang Jakie. Claimed 135,598: -163 instr over 129 puzzles vs the 135,761 IceFire reference (plus 2 from IceFire on scored_0929). Largest single-author step on the 135.7k frontier. Pulled: research/kernels/santa-2026-arithmetic-recipe-pool-and-milp

## Method (plain words)
Core idea: two programs of the SAME length can leave different integers available; a later target may need one of them. So explore equal-length rewrites first, then look for a shorter one.
1. Find interchangeable values: temporarily forbid an intermediate; check if another number made by exact arithmetic from remaining values can replace it. Bit-mask reachability tests many exclusions at once ("knockout").
2. Combine compatible rewrites: pool recipes from several equal-length programs, remove optional numbers while targets stay reachable; extra pools by scaling, translating or regrouping expressions.
3. Compile into 48 registers, replay, accept only strictly shorter.
Recipes are keyed by numeric operands (op, a, b), not registers, so the same calculation is recognised across programs.

## Code (C++ embedded as NATIVE_FILES strings, cells 11-13)
- common.inc: Puzzle::graph_from, order_for, allocate, pressure_order, compile, inverses, live_only, search_group (joint repair with a step budget).
- neutral.inc: diversify(graph, cap, wanted) = equal-length random recipe swaps (all one-op makers over live numbers, keep if live size <= cap); knockout(); discover_options(); crossover(base, archives); perturb().
- Strategies: mask (default short pass), neutral, neutral_chain, exchange, population, neighbors, lift, basis, rotate, parents, barrier, quotient, union. search.cpp loop: every 3rd round reset trial to champion, shuffle targets, diversify 3-11 swaps, compile, then search_group.
- Python: recipes_from_tape, pool_from_tapes, topological_order, allocate (last-use counts).

## Key numbers
- Output: total 135,598, saved 163, improved 129 puzzles. Top: scored_0192 120->116, 0177 110->107, 0438 188->185, 0499 114->111, 0919 127->124. Gains sit in 107-188 instr puzzles.
- Default Kaggle run with recorded repairs only: "mask saved 0 additional instructions"; the gain is from offline runs (records of changed recipes are embedded, ~200 KB).

## Figures
None in the rendered output (checked __results__.html).

## Reusable for us
- Neutral-move diversification + strict-improvement repair as an outer loop around any LNS (ours or public).
- Recipe-by-value representation and bit-mask reachability under exclusions: cheap test whether value v is replaceable.

## Failed / limits
- Not stated in detail; the default replay-only path finds 0 new.
- royalacecat notes its latest output did not beat 135,761 when replayed at one point (stale versions matter).

## Already in our log?
- No. Equal-length (plateau) moves were never part of our pipeline; -S slack (keep near-best terminals) is a different thing (inside our constructive solver) and failed.
