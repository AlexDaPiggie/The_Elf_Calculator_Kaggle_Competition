# romanrozen/santa-2026-icefire-strong-start (32 votes, #1 in score-ascending list)
Author: Roman Rozen. Output replays 135,761 (latest), strongest single public bank for most of 11-19/11-20; v117 used as reference by wangjakie. Pulled: research/kernels/santa-2026-icefire-strong-start (the .v3 pull is identical)

## Method (plain words)
1. Referee + read every attached id,program bank, best-of per puzzle.
2. IceFire optimizer per puzzle: pool the values of ALL equally short programs of a puzzle across banks; list every way one pooled value is a op b of two others (all_recipes); CP-SAT chooses a set of values containing all targets, one recipe per chosen value whose operands are chosen, levels for acyclicity; minimise #values, small secondary cost to keep original recipes and order (avoids stretched lifetimes).
3. Compile: emit values in original order; a value whose new recipe needs a later operand is delayed, or its operand pulled forward just in time (both tried). Full bank -> evict value with farthest next use (Belady) and rebuild from recipe if needed.
4. Keep only strictly shorter + replayed. Deterministic: 1 worker, fixed seed, deterministic time limit.

## Code (Python + ortools)
recipes_of(starts, prog), prune(starts, targets, rec), all_recipes(values, starts, cap), cpsat_plan(starts, targets, values, recipes, hint, det_time), first_appearances(puzzle, prog) for anatomy.

## Key numbers
- Section 4 anatomy: first targets expensive; bits per instruction rises with target index (same picture as Asterios).
- In sota pass 3: 4 puzzles / 6 instr in 189 s (4 CPU) on its own run; main value is being the merge carrier.

## Figures
Landscape + anatomy plots exist in the rendered notebook; not extracted (same content as Asterios figs 21/24).

## Reusable for us
- cpsat_plan is the cleanest public "recombine a value pool" model; input can be ANY set of programs for a puzzle, e.g. our own L8/E3 runs + best, or a dumped LNS trajectory (goodpjw idea).
- Two compile schedules (delay vs pull-forward) + Belady.

## Failed
- Not documented; equal-length pooling only gains when banks hold different same-length programs, which merges make rarer over time (diversity collapse).

## Already in our log?
- sota idea 6 (pooled CP-SAT with our alternative DAGs) proposed, not run. Merged IceFire outputs: yes (poller).
