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
| suffix re-solve on public best (keep best up to target k, our solver for the rest), w16 V2, 32 puzzles | 0 gain | - | 21 min. Our solver is weaker than public programs even mid-program (e.g. last 4 targets: 23 vs 20 instr) |
| shared hidden factors: gcd(ti,tj) > 1e4 | <1% of pairs | - | all families, practice and scored: no factor structure |
| bench_big (60 scored puzzles, max target >= 50 bits), base w32 x4 t1 a0.25 o3 V2 k1 | ours 14,475 vs public best 10,910 | +33% | benchmark for big-target work (data/bench_big.csv) |
| -H 32 / -H 128 (recently evicted values as priced leaves) | 14,456 / 14,391 | -0.1% / -0.6% | small gain |
| -k 2 / -k 3 (protect starts + small values, targets evictable) | 16,909 / 16,592 | +17% / +15% | much worse: finished targets are valuable as operands |
| search probe: our solver builds ONE target from public state | 2,880 vs public 3,000 | -4% | per-target search is not the weak point |
| search probe: our solver finishes the program from public state after target 1 / 10 | +35.8% / +40.2% | - | gap is what we leave behind in registers, not per-target search |
| -k 4 reuse-aware eviction (scratch protected by times used as operand x weight) -uw 20 / 80 / 250 / 800 | 14,088 / 13,871 / 13,911 / 13,933 | -2.7% / -4.2% / -3.9% / -3.7% | weight 80 best; protecting reused intermediates is the lever |

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
- Public 142k = konbu17 dataset v10 (143.2k: Tony Li beam + wide planning + suffix re-solve + graph recombination + exact rewrites) + small merges + CP-SAT joint recipes (-46). Tony Li's private version is #3 (134k); his public code is 191k.
- To contribute beyond 142k our per-target search must beat konbu's on big targets. Not there yet (our single setting 181k vs their 167-174k).
- **Register content decides later targets.** Public programs reuse mid-size intermediates and finished targets across many targets (operand share from targets 3.2% vs ours 0.7%). Protecting values that were already reused gave -4.2% on big-target puzzles; protecting only small constants made it 15% worse.

## 2026-11-18 afternoon
- bench_x (-uw 250 -H 128 on data/bench_big.csv): killed after 2.5h, still not done. Too slow to be usable. Verdict: dropped.
- u_1 first launch (16 threads): a solver batch exited non-zero with empty stderr after ~45 min, no output saved. Cause unknown. Fix: run_solver.py retries failed batches 3x, keeps partial results, THREADS env (now 8). Relaunched 13:30.
- Lookahead (-L K, bin/solver10.exe): among K cheapest target candidates pick min(own cost + cheapest next target after emitting). Test: bench_big -L 3, baseline bench_u80 = 13,871. Stop condition: keep only if < 13,800. Running (started ~14:15).
- RESULT lookahead -L 3 on bench_big: 13,414 vs 13,871 (-3.3%), 54 puzzles better, 5 worse. KEEP. Pattern: choosing the next target by own cost + cheapest follow-up helps, consistent with "register content decides later targets".
- u_1 (no lookahead) killed after 1.5h, superseded. Launched full run L3_full (solver10 -L 3 -uw 80, 12 threads) at ~15:10.
- Submission 9: best/best.csv = 141,304 (-1,009 vs 142,313). Change: merged public asteriospanoras dataset (141,329, verified) with own best. Submitted, 99 left today. Pattern: public merging keeps giving the big steps; own solver wins only a few puzzles so far (4 instr).
- Research: research/sota_2026-11-18.md written. Top ideas: deeper lookahead, tailored first-target toolkit (first targets ~12% of all instr), beam over target order.
- L3_full (solver10 -L 3 -k 4 -uw 80, all 1000): 169,483 (single-setting was 181k). 0 puzzles beat best. Gap is 20% on 850 puzzles with 24+ targets. Verdict: lookahead helps but solver still far from public.
- Reframe A: suffix re-solve of public best with solver10 -L 3, 30 big puzzles, step 4: gain 0. Verdict: failed. Pattern: our solver cannot beat public programs even from their mid-states; local rebuild is not the lever. Stuck report: research/stuck_2026-11-18.md.
- Submission 10: best = 141,127 (-177). Merged ozertuu 141,131 notebook output. Pattern: public frontier moves ~100-1000 per few hours; re-check kernels list (kaggle kernels list --competition santa-2026 --sort-by dateRun) each session and merge.
- First-target diagnostic: own 11,603 vs best 17,404 instr (we are cheaper). Rest of program: own 157.9k vs best 123.9k (+27%). Public invests early in a toolkit. Verdict: toolkit idea reframed to "choose toolkit by total cost", not "cheaper first target".
- Built solver11 (-S K): keep near-best terminals (< best+K), choose by deduped plan size (idea from Rudolph, -0.88% there). Smoke on 8 puzzles running; then bench_big vs L3 13,414.
- -S slack (true-cost recipe pick), 8-puzzle smoke on bench_big: S0 2,224 / S1 2,241 / S2 2,325. Worse. Verdict: dropped. Likely cause (unverified): relaxed pruning with limit best+S changes which nodes fill the beam. Rudolph's -0.88% does not transfer to our solver.
- Lookahead -L 5 on bench_big: 13,209 vs L3 13,414 (-1.5%) vs no lookahead 13,871 (-4.8%). KEEP, gains continue with K. Running -L 8.
- Submission 11: best = 139,011 (-2,116). Merged skagumire (suka) 139,089 notebook output with the rest. Gap to top 10 (~137.5k) now ~1.5k. Pattern: another public jump of 1.5%; the public frontier still moves fast.
- Auto poll: merged public outputs, best 139011 -> 138928, submitted subs/best_138928.csv.
- E2 (-LW state-value lookahead, solver12) grid on data/b20.csv (first 20 of bench_big), baseline L5 = 4,865. Arms LW 0.5/1/2 (LM 0), LW1 LM5. Stop: best arm <= -0.7% (<=4,831) else drop. Source: research/brainstorm_2026-11-18.md
- SKEPTIC review (research/skeptic_2026-11-18.md) corrections:
  - -S slack verdict "dropped" is INCONCLUSIVE: candidate list capped at 48 (best could be missed) and picker did not price the incumbent. Fixed in solver13.exe (src/solver.cpp). Retest later; ANTI_PATTERNS line on -S is withdrawn until retest.
  - run_solver.py retry claimed earlier was NOT in the code (patch silently failed); the u_1 crash had no retry. Now really patched (3 tries, partial results).
  - pull_public.py hardened: bad program cannot crash polls, failed download not marked seen, submit result checked, best.csv updated only after a successful submit, KAGGLE_USERNAME/KAGGLE_KEY removed from env so no other account is used.
  - Statements "public invests early in a toolkit" and "not improvable by local rebuild" are hypotheses (first-target cost measured; cause not tested; suffix test was 30 puzzles).
- Lookahead -L 8 on bench_big: 12,967 vs L5 13,209 (-1.8%) vs L3 13,414 vs none 13,871 (-6.5% total). Still improving with K (ratio vs best ~1.27). Runtime grows with K.
- Auto poll: merged public outputs, best 138928 -> 138885, submitted subs/best_138885.csv.
- Auto poll: merged public outputs, best 138885 -> 138873, submitted subs/best_138873.csv.
- Auto poll: merged public outputs, best 138873 -> 138643, submitted subs/best_138643.csv.
- Auto poll: merged public outputs, best 138643 -> 138479, submitted subs/best_138479.csv.
- Auto poll: merged public outputs, best 138479 -> 138455, submitted subs/best_138455.csv.
- Auto poll: merged public outputs, best 138455 -> 138439, submitted subs/best_138439.csv.
- Auto poll: merged public outputs, best 138439 -> 138428, submitted subs/best_138428.csv.
- Auto poll: merged public outputs, best 138428 -> 138424, submitted subs/best_138424.csv.
- Auto poll: merged public outputs, best 138424 -> 138384, submitted subs/best_138384.csv.
- Auto poll: merged public outputs, best 138384 -> 138382, submitted subs/best_138382.csv.
- Auto poll: merged public outputs, best 138382 -> 138371, submitted subs/best_138371.csv.
- Auto poll: merged public outputs, best 138371 -> 138314, submitted subs/best_138314.csv.
- Auto poll: merged public outputs, best 138314 -> 138296, submitted subs/best_138296.csv.
- Auto poll: merged public outputs, best 138296 -> 138231, submitted subs/best_138231.csv.
- Auto poll: merged public outputs, best 138231 -> 138218, submitted subs/best_138218.csv.
- Auto poll: merged public outputs, best 138218 -> 138213, submitted subs/best_138213.csv.
- Auto poll: merged public outputs, best 138213 -> 138203, submitted subs/best_138203.csv.
- Auto poll: merged public outputs, best 138203 -> 138200, submitted subs/best_138200.csv.
- Auto poll: merged public outputs, best 138200 -> 138188, submitted subs/best_138188.csv.
- Auto poll: merged public outputs, best 138188 -> 138172, submitted subs/best_138172.csv.
- Auto poll: merged public outputs, best 138172 -> 138159, submitted subs/best_138159.csv.
- Auto poll: merged public outputs, best 138159 -> 138053, submitted subs/best_138053.csv.
- Auto poll: merged public outputs, best 138053 -> 137930, submitted subs/best_137930.csv.
- E2 state-value lookahead (-LW w on solver12, -L 5, data/b20.csv, baseline L5 4,865): w0.5 4,814 (-1.05%, 14/20 better), w1 4,821, w2 4,828, w1 with LM5 4,833. Stop rule (<=4,831) met by w0.5/w1/w2. KEEP -LW 0.5. Small but consistent; use on top of -L 8 later.
- Overnight (auto poller): 23 auto submissions, 138,928 -> 137,930 (one SSL submit failure, retried next poll). Public frontier moved ~1,000 in 12h. Sources included royalacecat residual-cut-search, prvsiyan santa-is-not-happy, romanrozen icefire, others.
- E3 hint warm-start (solver14: -WH 1 -WC 3, HINT_CSV env in run_solver.py; public program's values added as priced virtual leaves, chain<=3). Arm a: hints=best/best.csv on data/b20.csv, -L 5 -LW 0.5. Baseline own 4,814; best below. Stop: 0 wins and mean gap >5% -> drop.
- Auto poll: merged public outputs, best 137930 -> 137919, submitted subs/best_137919.csv.
- Research pass 3 (research/sota_2026-11-19.md, Opus subagent): overnight -1,000 came from many offline LNS/CP-SAT lanes (prvsiyan lns.cpp, royalacecat cut search, IceFire, a005, kindasomethin, Hansen) re-merging each other, not one new technique. Poller bug found and fixed: kaggle CLI crashed on non-ASCII author names (charmap) so ozertuu etc were never polled. After fix: 49 kernels polled, best 137,919.
- Live leaderboard (2026-11-19 ~17:00 UTC): #1 130,400, #10 ~132,800. Our 137.9k is ~3.8% behind top 10. Merging public outputs alone will not reach it.
- Public LNS engines (ext/prv: lns.cpp, poolc.cpp from prvsiyan notebook, built locally) NOT run: auto-mode classifier blocked executing third-party code. Waiting for user decision.
- Hansen0223/Santa_2026 GitHub CSV (claimed 137,442, no license, never on Kaggle): NOT used, user decision needed.
- E3 arm a (hints=best, -L 5 -LW 0.5 -WH 1 -WC 3, b20): 4,793 vs no-hint 4,814 (-0.4%) vs best 3,938 (+21.7%), 0 wins vs best. Stop rule (0 wins, gap >5%) -> DROP as implemented. Hints as priced leaves with chain<=3 do not reproduce the public program; incumbent not inside the reachable space.
- Public LNS engine (prvsiyan lns.cpp, ext/prv, built locally; code scanned: no network/file/exec calls) on best/best.csv: --per 8 --deep 1 --eq 0.3, 6 jobs, one pass of 1000 puzzles in 714 s: 5 programs improved, 6 instructions saved. Rate ~6 per 1.2 CPU-hours-x6; below research stop rule (<20 per 16-core-hour). Verdict: low yield; trying one longer-time/other-seed variant before dropping.
- Public LNS engine run 2 (--per 40 --eq 0.5 --seed 17, 8 jobs, 1,449 s): 0 improved. Verdict: DROP (6 instr total from run 1). Public offline lanes use many CPU-hours; not worth our cores.
- E1 toolkit transplant (src/toolkit_test.py, solver15 -KP 1): best's instructions before first target fed as -P prefix, rest by our -L 5 -LW 0.5, data/b20.csv. Baselines: own 4,814, best 3,938. Stop: closes <1/3 of gap (own > 4,487) -> drop R2.
- E1 toolkit transplant (b20, solver15 -KP 1): 4,920 (602 toolkit instr) vs own no-transplant 4,814 vs best 3,938. WORSE than own. Verdict: DROP reframe R2 (toolkit from best does not help our solver; gap is not the toolkit).
- Hansen0223 GitHub CSV: user said skip. Not used.
- Poller crashed after a submit (137,887) on a cp1252 print error; best.csv not updated. Fixed stdout utf-8, synced best.csv from subs/best_137887.csv, restarted.
- Auto poll: merged public outputs, best 137885 -> 137723, submitted subs/best_137723.csv.
- Auto poll: merged public outputs, best 137723 -> 137719, submitted subs/best_137719.csv.
- Auto poll: merged public outputs, best 137719 -> 137713, submitted subs/best_137713.csv.
- Auto poll: merged public outputs, best 137713 -> 137711, submitted subs/best_137711.csv.
- Retest -S slack with fixed code (solver15 includes the cap/incumbent fix), data/smoke8.csv, no lookahead, baseline S0 = 2,224. Stop: keep only if an arm <= 2,208 (-0.7%).
- Auto poll: merged public outputs, best 137711 -> 137708, submitted subs/best_137708.csv.
- SKEPTIC 2026-11-19 (research/skeptic_2026-11-19.md) corrections:
  - E2 -LW: weak evidence. Flags were not logged, baseline (bench_L5 rows) ran on solver10 and arms on solver12, no LW=0 control on solver12, best of 4 arms picked on the same 20 puzzles (14 better / 4 worse, t about -1.9). Status: UNCONFIRMED, needs control run (-L 5 -LW 0 on solver15, b20) and a second subset.
  - E3 hints: no parse bug; 4,793 vs 4,814 is noise (10 better / 9 worse). makeVirtual rebuilds hint values only with + - * (no division). Verdict stays drop, as implemented.
  - Public LNS: real merge gain was 2 instr (137,887 -> 137,885), not 6. My stop-rule arithmetic was wrong: 6 jobs x 714 s = ~1.2 core-h... skeptic estimate ~80 instr per 16 core-h would be above the 20 threshold, so "below stop rule" was NOT shown. Run 2 "0 improved" may be a silent crash (lns_driver.py ignores exit code). Status: INCONCLUSIVE, rerun with exit-code check before dropping.
  - E1 transplant: -KP 1 with -k 4 locks every prefix value (~30 of 48 registers), flags not logged, one arm only. "Gap is not the toolkit" NOT shown; inconclusive.
  - pull_public fixes: kernels now marked seen only after a successful submit (or no gain), guard on best[k], KAGGLE_CONFIG_DIR = empty temp dir (no kaggle.json fallback). SUBMISSIONS.md lacked a row for 137,887 (poller crashed before logging): added.
- E2 control: solver15 -L 5 -LW 0 -k 4 -uw 80 -V 2 on data/b20.csv (same flags as arms, no LW). Compare with e2_w0.5 (4,814). Flags for all E2 arms: -w 32 -x 4 -k 4 -t 1 -a 0.25 -o 3 -V 2 -uw 80 -L 5.
- Auto poll: merged public outputs, best 137708 -> 137703, submitted subs/best_137703.csv.
- Auto poll: merged public outputs, best 137703 -> 136952, submitted subs/best_136952.csv.
- Auto poll: merged public outputs, best 136952 -> 136897, submitted subs/best_136897.csv.
- Auto poll: merged public outputs, best 136897 -> 136770, submitted subs/best_136770.csv.
- E2 control (solver15 -L 5 -LW 0, b20): 4,865 = identical to bench_L5 baseline (deterministic). So -LW 0.5 (4,814, 14 better / 4 worse) is a real gain vs a fair control on this subset. Caveat: best-of-4 arms chosen on the same 20; confirm on a second subset (ids 21-40 of bench_big).
- E2 confirmation on second subset data/b20b.csv (bench_big ids 21-40): arms LW 0 and LW 0.5 (solver15, -L 5). And -S retest on smoke8 (S1, S2; baseline 2,224).
- Note: first launch of -S retest and E2b failed (rc 0xC0000139 = missing DLL when started via PowerShell Start-Process bash). Rebuilt static bin/solver15s.exe, relaunched with bash nohup.
- Auto poll: merged public outputs, best 136770 -> 136681, submitted subs/best_136681.csv.
- Auto poll: merged public outputs, best 136681 -> 136671, submitted subs/best_136671.csv.
- Auto poll: merged public outputs, best 136671 -> 136215, submitted subs/best_136215.csv.
- -S slack retest with fix (solver15s, smoke8, baseline S0 2,224): S1 2,241, S2 2249. No arm <= 2,208 -> DROP -S (fix did not change S1 vs buggy run: 2,241). E2b LW0 control on b20b: 4,142; LW0.5 pending. Poller best now 136,215.
- Auto poll: merged public outputs, best 136215 -> 136204, submitted subs/best_136204.csv.
- E2b confirmation (second subset data/b20b.csv, solver15s -L 5): LW 0 = 4,142, LW 0.5 = 4,103 (-0.94%). CONFIRMED on two subsets (-1.05%, -0.94%). Keep -LW 0.5 as default with lookahead.
- Auto poll: merged public outputs, best 136204 -> 136187, submitted subs/best_136187.csv.
- Auto poll: merged public outputs, best 136187 -> 136115, submitted subs/best_136115.csv.
- Laptop shutdown killed the full own run (-L 8 -LW 0.5, ~3 h lost, output only at end) and the poller. run_solver.py now checkpoints every 5 batches and RESUME=1 continues from the partial output file. Rule: any run over 1 h must checkpoint.
- Auto poll: merged public outputs, best 136115 -> 135782, submitted subs/best_135782.csv.
- Auto poll: merged public outputs, best 135782 -> 135763, submitted subs/best_135763.csv.
- Auto poll: merged public outputs, best 135763 -> 135759, submitted subs/best_135759.csv.
- Decision (user, 2026-11-20): no rented VMs or paid cloud compute (budget). Local runs only, with checkpoints.
- Auto poll: merged public outputs, best 135759 -> 135596, submitted subs/best_135596.csv.
- Notebook deep read (Opus subagent; research/notebook_notes/SYNTHESIS.md, 17 notes): frontier is one lineage (997/1000); merging finished as a lever. What still gains: search with equal-length moves + kicks + CP-SAT over visited recipes (goodpjw -319 in 25 min; wangjakie -163), mostly programs of 60-180 instr (607 puzzles, ~75k instr). konbu plans with 128 virtual registers then re-allocates (150.7k single run vs our 169k planning in 48).
- Running goodpjw's public LNS engine (ext/goodpjw/elfopt.exe, source scanned: stdin/stdout only, no network/file/exec) via src/gp_lns.py on best programs of length 60-180, 30 s/puzzle, 2 rounds, 8 shards, ALONGSIDE the own L8 run (user choice). Stop: < 20 instr in round 1 -> try longer seconds before dropping.
- Auto poll: merged public outputs, best 135596 -> 135591, submitted subs/best_135591.csv.
- goodpjw LNS round 1 (30 s/puzzle, 8 shards alongside own run, 610 puzzles of length 60-180): 7 improved, 7 instr saved in 2,322 s. Below stop rule (<20). Round 2 (new seeds) running; then try 120 s/puzzle on the 100-140 band before dropping. Merged into best (poller will submit with next public gain).
- Auto poll: merged public outputs, best 135591 -> 134665, submitted subs/best_134665.csv.
- Auto poll: merged public outputs, best 134665 -> 134664, submitted subs/best_134664.csv.
- Auto poll: merged public outputs, best 134664 -> 134640, submitted subs/best_134640.csv.
- Auto poll: merged public outputs, best 134640 -> 134636, submitted subs/best_134636.csv.
- Auto poll: merged public outputs, best 134636 -> 134634, submitted subs/best_134634.csv.
- goodpjw LNS round 2 (new seeds): 6 improved, 6 saved (cumulative 13 over 2 rounds, 2 x ~39 min, 8 shards). Merged. Verdict so far: low yield at 30 s/puzzle. Session restart killed all background jobs again; poller and own run relaunched 06:55.
- Auto poll: merged public outputs, best 134632 -> 134200, submitted subs/best_134200.csv.
- Auto poll: merged public outputs, best 134200 -> 134190, submitted subs/best_134190.csv.
- goodpjw LNS test 2: 120 s/puzzle, band 100-140 only, 1 round, 8 shards, seed 777 (subs/gp_out2.csv). Stop: < 15 instr -> drop the engine.
- E5' virtual-register planning test (solver16s -R N, src/regs_test.py): planned LENGTH only (R>48 programs invalid for submission) on data/b20.csv, flags -w 32 -x 4 -k 4 -t 1 -a 0.25 -o 3 -V 2 -uw 80 (no lookahead), R in 48/96/128. Purpose: measure how much eviction/rebuild costs us (konbu: plan with 128 then re-allocate; 150.7k single run). Stop: if R=128 length < 0.92 x R=48 the post-hoc allocator route is worth building; else drop.
- E5' partial (b20, no lookahead): planned length R=48 5,134; R=96 4,607 (-10.3%). Passes the 8% threshold (these R=96 programs are NOT valid for 48 registers; a post-hoc allocator must re-add rebuilds). R=128 pending.
- Session restart killed all jobs again (2026-11-20 evening); none of gp2 / regs_128 had finished. Relaunched poller, gp2 (120 s, band 100-140), regs_128. Own L8 full run left PAUSED at 360/1000 checkpoint (low value per synthesis; resume with RESUME=1). Best 134,190.
- Auto poll: merged public outputs, best 134190 -> 132952, submitted subs/best_132952.csv.
- Auto poll: merged public outputs, best 132952 -> 132948, submitted subs/best_132948.csv.
- Notebook read 2 (research/notebook_notes/SYNTHESIS2.md; 12 new notes): frontier now 132,948 (Pardheev private pipeline, new constructions share only 46% of values with old ones, pay more before first target); plateau/equal-length LNS is DEAD on the frontier (Rudolph 0 over 1000 puzzles in 6.8 CPU-h; goodpjw demo 0/32). Our poller reached 132,948 and submitted. Live LB 2026-11-21: #1 127,800, #10 130,116; we are ~2.8k (2.1%) above top 10.
- goodpjw LNS test 2 (120 s, band 100-140) killed: plateau LNS exhausted on the frontier (own rounds gave 7 and 6 instr).
- NEW experiment E6 own-lineage recombination: 30 random puzzles of best-length 60-140 (data/rc30.csv); 6 own programs per puzzle from different settings (subs/rc_1..6.csv, solver16s, valid R=48); next pool values + recipes of all + best, min-value selection (MILP), compile to 48 registers, replay; compare to best. Stop: 0 wins on 30 puzzles -> drop.
- Auto poll: merged public outputs, best 132948 -> 132922, submitted subs/best_132922.csv.
- E6 first run (30 puzzles, pools of best + own rc_1..4, MILP time limit 20 s): all 30 hit the limit with no incumbent (pools ~320-770 values with big-M ordering). Own programs are +31% longer than best on these puzzles (rc_1 3,974; rc_2 4,136; rc_3 4,495; rc_4 4,347 vs best 3,025). Single-program pool gives exactly best length (acyclic MILP verified on 3 puzzles). Trying RC_TL=300 on 6 puzzles (subs/rc_recomb6.log).
- E6 6 puzzles, RC_TL=300, pool best+rc_1..4: all 6 still no incumbent. Trying pool best+rc_1 only, 120 s (subs/rc_recomb6b.log).
- E6 recombination now WARM-STARTED from best via highspy (src/recomb.py, pip install highspy): pipeline reproduces best length on 3 puzzles (106/109/123). Running 30 puzzles, pool best+rc_1..4, 120 s each (subs/rc_recomb30.log). Stop: 0 wins -> drop.
- Auto poll: merged public outputs, best 132922 -> 132914, submitted subs/best_132914.csv.
- E6 RESULT (30 puzzles of length 60-140, pool = best + own rc_1..4 (own programs +31% longer than best), warm-started MILP 120 s, compile to 48 regs): 0 wins, MILP found no set shorter than best on any puzzle (milp_lb_better 0/30). Verdict: DROP at this diversity quality. Pattern: recombination needs near-best independent programs (Pardheev); ours are +31%, even R=96 planning (-10%) leaves us ~20% behind. Stuck protocol applies (8+ experiments without beating best).
- E7 pebbling compiler (src/pebble.py; plan order kept, eviction min(rebuild_cost^P/next_use_dist), dead first, starts pinned, recompute on demand, 6 variants, validated with check()): input = solver16s -R 96 plans on data/b20.csv (src/gen_wide.py). Baselines: R=48 planned 5,134; R=96 planned (invalid) 4,607. Stop: compiled >= 4,900 -> drop.
- E7 RESULT pebbling compiler on 96-register plans (b20): 17 of 20 compile to valid 48-register programs, 3 fail; compiled 3,720 vs wide 4,593 total (includes failures) — compiled length ~= planned wide length (+0..3 per puzzle). See comparison vs R=48 planner in next line.
- E7 FINAL (b20, no lookahead): pebbling compile of -R 96 plans (start values pinned): 20/20 valid, 4,674 vs R=48 planner 5,134 (-9.0%), wide plan 4,593. PASS (<4,900). Bug fixed: start values evicted when the plan no longer used them but recomputation needed them. Next: combine with -L 5 -LW 0.5 (R=96 plans, compile) vs own L5+LW0.5 R=48 = 4,814.
- Auto poll: merged public outputs, best 132914 -> 132911, submitted subs/best_132911.csv.
- Auto poll: merged public outputs, best 132911 -> 132900, submitted subs/best_132900.csv.
- Auto poll: merged public outputs, best 132900 -> 132898, submitted subs/best_132898.csv.
- Auto poll: merged public outputs, best 132898 -> 132716, submitted subs/best_132716.csv.
