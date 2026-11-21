# bikrambasnet1/santa-2026-arithmetic-graph-rewrites (58 votes, #3 by votes)
Author: Bikram Basnet. Claimed 138,485 (Kaggle submission 58552390): -4,455 over 857 puzzles vs konbu 142,940 start. Current version only replays packed replacements; v1 (scriptVersionId 371088174) ran the optimizers in full. Pulled: research/kernels/santa-2026-arithmetic-graph-rewrites

## Method (plain words)
- Multiple rebuild strategies per puzzle, keep shortest valid.
- Replace a recipe when an existing value or a shorter chain gives the same result.
- INVERSE CHAINS: for some dependency chains it is cheaper to build the downstream value first and recover its predecessor with an inverse op (e.g. build Y, then X = Y / k or Y - c) instead of X then Y.
- Recipe recombination across source programs (shared intermediates), 48-register allocation, replay.
- v12: full 1,000-puzzle randomized search + joint recipe selection over alternate programs: 75 shorter programs; IceFire supplied 14 more; -114 vs v11 (138,599).

## Key numbers
- 857/1000 puzzles shortened vs 142,940 (era of easy gains).

## Figures
None in current version.

## Reusable for us
- Inverse-chain reorder (build the later value first) as an LNS repair shape; not in our solver (we always build forward from leaves).

## Failed
Not documented.

## Already in our log?
- Merged outputs. Inverse chains: not tried.
