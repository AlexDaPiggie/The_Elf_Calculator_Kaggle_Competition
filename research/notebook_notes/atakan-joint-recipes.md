# atakanaldemir/santa-2026-joint-recipes-for-large-puzzles (24 votes)
Author: Atakan Aldemir. V30: 138,273 verified, -7 over 6 large puzzles vs V29; early version 142,979 -> 142,272 (46 from CP-SAT search on 37 puzzles, 13 from cleanup). Asterios credits him for the "scaffold exchange" and the "multiplier-frontier optimizer" (re-run on the 135,761 merge: -2). Pulled: research/kernels/santa-2026-joint-recipes-for-large-puzzles (+ .v3, which only holds packed programs)

## Method (plain words)
1. Decode live dependencies of several verified programs.
2. Generate extra candidate recipes from existing operands by inverse arithmetic (exact division only); add a helper if it could replace an exclusive chain or feed several goals.
3. CP-SAT: Boolean per value, one recipe per active non-seed value, targets forced, topological order (operands strictly earlier); minimise active values (candidate graph optimum, not puzzle optimum).
4. Multiple physical-register schedules; keep only strictly shorter replay.
5. Separate bounded cleanup on shared intermediates (counted separately).
Later versions (from V30 text): dependency-cut rebuilding + whole-program merge by numeric value (when old and new branches need the same integer, one shared computation replaces duplicate work); edits that do not shorten the local block may compete if the full program becomes strictly shorter.
"A cheaper graph is not necessarily a cheaper program": register compile is part of the objective.

## Key numbers
- Targets puzzles with >= 25 goals. 707 saved total in early version, of which 46 search + 13 cleanup, rest merge.
- V30 pilots that failed: joined-boundary, partial-completion, prepaid downstream-value.

## Figures
Not extracted (example of shared helper in early version).

## Reusable for us
- Inverse-arithmetic candidate generation + CP-SAT min-value model (same family as IceFire/avazaku). Offline sources (global_recipes.py, C++ compiler) are b85/zlib-packed in the old notebook appendix; not decoded here.

## Failed
- V30 pilots above (no gain on dev sample).

## Already in our log?
- Merged outputs via poller. Joint-recipe CP-SAT: not run by us.
