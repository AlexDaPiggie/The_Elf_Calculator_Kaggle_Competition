# Experiment and submission log

Score = total instructions (lower is better). Local score is exact (no public/private split).
"Prac" = practice set (200 puzzles), used for quick A/B. "Scored" = the 1000 real puzzles.

## Submissions
| # | Date | File | Change | Local / LB | Delta vs prev best |
|---|---|---|---|---:|---:|
| 1 | 2026-11-18 | subs/v2.csv | own solver: cost<=2 dictionary + backward beam (w32) + product-approx reduction, alpha 0.25 | 187,524 | - |
| 2 | 2026-11-18 | best/best.csv | per-puzzle min over v1, v2, v3 (v3 = w128, x4) | 184,766 | -2,758 |
| 3 | 2026-11-18 | best/best.csv | + v5 (keep targets -k1, greedy order -o3, w32 x4; alone 184,012) | 182,242 | -2,524 |
| 4 | 2026-11-18 | best/best.csv | + public dataset konbu17 (163,413, 115 CPU-h portfolio), validated; ours wins 80 puzzles | 163,256 | -18,986 |
| 5 | 2026-11-18 | best/best.csv | + portfolio p1-p4 on scored (palette p1/p2, alpha 0.18/0.32; all w32 x4 k1 t1 o3) | 163,088 | -168 |
| 6 | 2026-11-18 | best/best.csv | + p5-p7 (w64, a0.18 w64, a0.12) | 163,081 | -7 |
| 7 | 2026-11-18 | best/best.csv | + virtual leaves V2 run (alone 181,117) | 162,958 | -123 |
| 8 | 2026-11-18 | best/best.csv | + public notebook outputs: elias best-of-public (161.8k), sacuscreed public-merge (142k); all validated per program | 142,313 | -20,645 |

## Experiments (practice set unless noted)
| Change | Prac score | Delta | Note |
|---|---:|---:|---|
| v1 baseline: dict + beam w8, alpha 0.18, ascending order | 39,565 | - | scored 193,433 |
| + product-approx reduction (x2) | 38,897 | -1.7% | approximating r by x*y and building the error helps |
| + beam w32 | 38,367 | -1.4% | |
| + alpha 0.25 | 38,220 | -0.4% | rank by cost + 0.25*log2(residual) |
| greedy cheapest-next order (w8) | 38,603 vs 38,897 | -0.75% | same beam; order matters a little |
| greedy + tie-break on larger target | 39,971 | +2.8% | worse: build small targets first |
| w64 x2 | 37,960 | -0.7% | |
| w32 x6 | 38,186 | ~0 | wider approx alone does little |
| w128 x4 | 37,857 | -1.0% vs w32 | scored 185,856 (3 min on 16 cores) |
| merge per-puzzle best of v1+v2+v3 | - | - | scored 184,766: different configs win on different puzzles |
| + additive approx r ~ x+y (sx1 / sx3), w32 x4 | 38,553 / 38,569 vs 38,308 | +0.6% | worse: extra candidates crowd the beam, and the residual-size rank misjudges them |
| register keep policy -k1 (evict scratch before targets/starts), w32 x4 | 37,864 vs 38,308 | -1.2% | pool content matters a lot |
| -k1 + greedy order -o3 | 37,594 | -0.7% more | gains stack; total -1.9% vs w32 x4 |
| three-term terminal r = A*B +/- C, all from dict (-t1, root full dict) | 37,643 vs 37,864 | -0.6% | |
| -t2 (three-term at every node) | 37,680 | ~0 | slower, no gain |
| full MITM at root (-D1, X op Y both up to cost 2) | same per-target costs | 0 | no cost-5 solutions exist for 40-bit targets from our pool |
| beam w1024 x8 d30 | ~same as w128 | ~0 | **search space is the limit, not width** |
| palette in registers (-p1 ladder 2,4,16,256,2^16,2^32 / -p2 + odd consts) | 37,843 / 38,280 vs 37,643 | +0.5% / +1.7% | upfront cost not repaid on average; may win on big-target puzzles (portfolio) |
| scored portfolio, single scores: p1 183,866 / p2 186,196 / a0.18 182,569 / a0.32 183,373 | - | - | merge gains vs 163,256 best: 28 / 2 / 132 / 6. alpha 0.18 best alone and most complementary |
| bug: X*f - a link built X*f above limit (w64 run, scored_0234) | - | - | fixed in solver4; merge_best validation caught it, file never broken |
| scored: w64 181,750 / a0.18 w64 181,746 / a0.12 183,548 | - | - | merge gains 3 / 1 / 3. best single setting now ~181.7k; portfolio of current solver is saturated |
| virtual leaves -V (consts 1-16 + powers of 2 as dict leaves, priced at real build cost, built only if used); base w32 x4 k1 t1 a0.25 o3 | V0 37,592 / V2 36,831 / V3 36,885 / V4 36,764 | -2.0% / -1.9% / -2.2% | time 242s / 627s / 1061s / 1349s. Biggest single gain so far. Unlike palette-in-registers (+0.5%), paying only on use wins |
| scored V2 (w32 x4 k1 t1 a0.25 o3 -V 2) | 181,117 | ~-0.8% vs same base | smaller gain on scored than practice (-2%); merge gain 123 |
| extra virtual sets with V2: -vs 2 (2^k+/-1) / -vs 3 (3*2^k) | 36,903 / 36,909 vs 36,831 | +0.2% | more helper values crowd the dict; consts 1-16 + powers of 2 is enough |
| dead-code elimination (src/dce.py) | - | - | palette runs p1/p2 shrink by 891/1322; others ~0. Needed for any palette-upfront approach |
| per-puzzle cap V6 on scored_0982 | 356 vs 378 (V0) / 429 (V2) | - | best cap varies a lot per puzzle; public best 308 |
| own-only portfolio (no public programs) | 176,782 | - | public 174k notebook gets 174,827 with 6 settings |

## Patterns so far
- **Pool/register content is a strong lever.** Keeping built targets and starts live beats LRU. Next: try smarter keep scores (small constants, frequently used hubs).
- Per-target cost scales ~5.3 bits/op: 40-bit targets cost ~7, 60-bit ~11-12; first target 15-43 (tiny pool).
- konbu17 (public 163k) used virtual palette leaves (built only when used) and up to 96-144 leaves with rebuild costs, plus exact MITM up to 3 instructions deep (tens of millions of values), plus a 50-setting portfolio. Their best single setting was ~167-174k, so the portfolio is worth ~3-6%.
- Beam width scales slowly: each 2x width gives ~0.5-0.7%. Compute alone will not reach the top.
- Small targets first is better than large first. The pool grows with built targets.
- Merging per-puzzle bests across configs gives free gains (~0.6%), so keep running varied configs.
- Hypotheses rejected:
  - targets are not reachable from the starts alone within 5 ops
  - targets are almost never 1-2 ops from other targets (0-2%)
  - so the hidden structure is weak, and generic search quality is the main lever
- Ops per target (practice v1): independent ~10.6, mixed ~8.4, shared ~6.4, multiplicative ~4.4. Independent and mixed (large 40-60 bit targets) carry most of the cost.
- Marginal portfolio gains are now small (~0.1%) because the public konbu17 set dominates most puzzles. New gains need a stronger solver, not more variants of the current one.
- **Pay-on-use beats pay-upfront.** Same helper values (powers of two) hurt when pre-built in registers but give -2% as priced virtual leaves.
- Leaderboard day 1 evening: #1 132,557, #10 137,544. Public merges reach 142.3k, so everyone starts there. Beating it needs improving existing best programs (LNS on suffixes), not standalone solves.
- Our gap vs public best is almost all on big targets (50-60 bits: 13-29% worse); small targets only ~2%.
