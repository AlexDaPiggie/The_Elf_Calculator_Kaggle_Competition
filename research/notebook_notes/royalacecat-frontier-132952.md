# royalacecat/santa-2026-public-frontier-score-132-952 (new version of the frontier notebook; old note: royalacecat-frontier-and-cut-search.md)
Author: E-Max AI. Claimed 132,952: union of 4 public banks = 132,953, plus 1 from a replayed graph search (scored_0295 121 -> 120). Pulled: research/kernels/santa-2026-public-frontier-score-132-952 (output csv in research/kernels/_out/; the compiled binary was deleted unrun).

## Method (plain words) - NEW since the 135,761 note
- Inputs: their own v97 (133,772), kindasomethin 133,813, Asterios 132,996 snapshot (incl. scored_0549), goodpjw v26 bank 132,954; all checksum-pinned and replayed.
- Search = graph-based adaptation of Wang Jakie's recipe-pool search: convert valid programs to dependency graphs, RETAIN diverse historical graphs (archive of near-length programs, len <= best + 3, ranked), perturb candidate graphs, try recombination, compile back to registers. "Deeper incremental" arm: 3-18 changes per perturbation, keeps historical donor graphs during pruning (source incremental_retained.cpp / incremental_diverse_deep in public dataset royalacecat/santa-2026-retained-graph-search-source, not downloaded).
- Job input format: "limit regs rounds 0 seed / starts / sorted targets / number of programs / each program" -> one program per line.

## Key numbers
- The 134,190 -> 133,772 step (their v97 and the 133.8k wave) came from these seeded graph-search lanes run by several teams.
- Honest note: win was post-selected; in a fixed-seed 24-case comparison only the deeper arm found the 1 gain; in a later 32-case comparison all variants found 0.
- Credits Pardheev for suggestions on beam construction, annealing and CP-SAT recombination (see pardheev-132948.md).

## Figures
None (replay notebook). kaggle kernels output gives only log + csv now (no __results__ PNGs).

## Reusable for us
- Archive of near-length (<= +3) alternative programs per puzzle as crossover donors: a cheap way to keep diversity.
- encode_job wire format if we ever run their engine (needs user OK for third-party code).

## Failed
- 32-case comparison: 0 wins for all arms. Graph search lanes on the converged frontier now yield ~1 instr per release.

## Already tried by us?
- Poller merges their outputs. Seeded/retained graph search: not run. Our goodpjw-engine LNS (similar family) gave 13 instr in 2 rounds.
