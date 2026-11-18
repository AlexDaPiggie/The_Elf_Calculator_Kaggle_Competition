# Santa 2026 - The Elf Calculator: strategy

Goal: top 10 on the final leaderboard (deadline 2027-01-28 23:59 UTC).

## Facts (from rules + data)
- Competition slug `santa-2026`. 1000 puzzles. Score = total instructions. Lower is better.
- **No public/private split.** The local score is exact, so the leaderboard only confirms what we already know.
- 100 submissions/day, 2 final picks. Submissions are cheap, but we only submit when the local score improves.
- One invalid program rejects the whole file. Always run `src/common.py` validation before submitting.
- Rudolph Prize ($10k) goes to whoever holds #1 the longest. That needs #1 early - not our goal.
- **Use only ONE Kaggle account** (`KAGGLE_API_TOKEN_1`, already entered). Other tokens in env look like other accounts - submitting from them = disqualification.
- No private code sharing outside the team. Teams up to 5, merge deadline 2027-01-21.

## Numbers
| Item | Value |
|---|---:|
| Sum of targets not in starts (trivial lower bound) | 26,898 |
| Rough counting floor if targets were random (~12 bits per op) | ~103,000 |
| sample_submission.csv | 1,490,379 |
| Best public notebook (Tony Li) | 191,867 |
| LB #1 on day 1 (2026-11-18) | 149,080 |
| **Ours v2** | **187,524** |

Practice set, v1 ops per target: tiny 1.5x LB, multiplicative 4.4x, shared 6.4x, mixed 8.4x, independent 10.6x.

## Puzzle families (practice labels; scored set has no labels)
- **independent**: targets look like uniform random numbers below the limit. Large starts (up to ~2000). No structure, so this is a pure search-quality problem.
- **shared**: clusters of nearly equal targets (e.g. 10973744, 10974352, 10974650). Build the cluster centre once, then each neighbour costs 1 op plus a small difference.
- **multiplicative / mixed**: hidden generator mixes * and +. Sometimes big gcds between targets.
- **tiny**: 1-4 small targets. Use exact search for provably optimal answers.
- To do: train a classifier on practice (family label) so we can apply family-specific solvers to the scored set.

## Engine plan (C++ in `src/solver.cpp`)
1. **Done (v1-v2):** for each target, build a dictionary from live registers (values at cost 0, 1, 2). Then run a backward beam search over residuals: `r = X*f +/- a`, `r = a - X`, `r = X + a`, `r = x*y +/- e` (approximate by product, then correct), with two-term meet-in-the-middle terminals. Registers use LRU eviction with pinning. Fallback adds small constants.
2. **Next, quick wins:**
   - target order search: cheapest-next greedy and random restarts. Keep the best per puzzle.
   - smarter register keep policy: keep targets and good "hub" values.
   - wider beam and alpha tuning, run in bulk on Modal CPUs.
3. **Per-puzzle best file:** store `best/<id>.json`, and merge after every run so improvements only ever add up. This is how past Santa winners worked.
4. **Structure exploits:**
   - shared: cluster detection, then build differences once (Bos-Coster approximation / delta-largest).
   - multiplicative: gcd / ratio links between targets, and factor reuse.
   - tiny: exact iterative deepening.
5. **Global improvement:** LNS + SA over the whole program. Remove 1-4 targets plus their helpers, rebuild with exact depth search, accept by SA. Finish with a dead-instruction prune.
6. **Compute:** local 16 cores, plus Modal for big CPU sweeps (the problem is CPU-bound, no GPU needed).

## Process rules
- Measure on all 1000 scored puzzles locally (exact score). Use the practice set for family-level diagnostics.
- Submit only when the local score improves. Write the score in the submission message.
- Track ops/target per family, and the gap to the counting floor, to decide where to spend compute.
