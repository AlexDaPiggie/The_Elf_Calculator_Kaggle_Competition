# kindasomethin/santa-2026-exact-portfolio-frontier-133813 (new version; old note kindasomethin-exact-portfolio.md at 135,812)
Author: Pratham Jain. Claimed official 133,813 (submission 58644349), max tape 277. Pulled: research/kernels/santa-2026-exact-portfolio-frontier-133813

## What is NEW
- Score path: previous 133,990 -> disjoint 192-job "cap-16 graph-pool" batch 133,983 (-7) -> strict complementary union with RoyalAce 133,825 = 133,814 (-169) -> Asterios 133,824 exact complement 133,813.
- Pipeline now: (1) replay all banks, take strictly shorter rows; (2) union RoyalAce frontier with GoodPJW and Hansen banks; (3) replay fixed-seed RoyalAce graph-pool candidates; (4) diversify the same GCC graph search locally (cap-16 = pool cap per job); (5) keep earlier whole-value-DAG and paired-network search; (6) multi-bank CP-SAT with fresh two-step shared helpers; (7) keep a small set of exact EQUAL-LENGTH variants because the public search bank uses them for diversity.
- vs the 138,441 provenance base: 4,628 instructions over 795 puzzles (stage table lives in their dataset checkpoint_stage_deltas.csv, not downloaded).

## Insights
- Own search share is tiny (-7 from 192 jobs); the release is mostly unions. Same message as goodpjw: graph search lanes are near-exhausted on the converged frontier.
- They deliberately publish equal-length variants so others' crossover pools get diversity: the community treats same-length alternatives as a resource.

## Figures
Tables only; no PNGs in CLI output.

## Reusable
- Equal-length variant publishing / archiving as diversity for recombination.

## Failed
- Not documented.

## Already tried by us?
- Poller merges; vs our current best this file is 865 worse (Pardheev wave came after).
