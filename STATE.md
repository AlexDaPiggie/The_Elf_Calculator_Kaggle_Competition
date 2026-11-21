# STATE (updated 2026-11-19 23:10)

Goal: top 10 (LB top 10 about 132.8k on 2026-11-19; #1 130.4k). Metric: total instructions, lower is better, exact locally.

## Current best
- best/best.csv = 134,190 (submitted by poller, still dropping). LB top 10 ~132.8k, #1 130.4k.
- Backup copy: subs/best_142313.csv

## What worked (see EXPERIMENTS.md)
- Keep targets/starts in registers, greedy order, three-term terminal, product approximation.
- Virtual helper leaves (-V 2): -2% practice, -0.8% scored.
- Reuse-aware eviction (-k 4 -uw 80): -4.2% on big-target benchmark (data/bench_big.csv).
- Per-puzzle min merge of everything (public + own).

## What failed
- Wider beams, additive approx, palette in registers, -k 2/3, bigger helper sets, suffix re-solve with our solver (0 gain).

## Key finding
- Hypothesis (not proven): gap to public is mostly what stays in registers for later targets.

## Running (relaunch after any shutdown; all die when the session restarts)
- Poller: PYTHONIOENCODING=utf-8 python src/pull_public.py --loop 20 > subs/poll.log (auto merge + submit)
- gp2: python src/gp_lns.py subs/gp_in2.csv subs/gp_out2.csv --seconds 120 --rounds 1 --shards 8 --lo 100 --hi 140 --seed 777 (goodpjw engine, ext/goodpjw)
- regs_128: python src/regs_test.py 128 data/b20.csv -- -w 32 -x 4 -k 4 -t 1 -a 0.25 -o 3 -V 2 -uw 80 > subs/regs_128.log (R=48 5,134; R=96 4,607 = -10.3%)
- Own L8 full run PAUSED (360/1000 in subs/own_L8_full.csv): RESUME=1 THREADS=14 python src/run_solver.py ./bin/solver15s.exe subs/own_L8_full.csv -- -w 32 -x 4 -k 4 -t 1 -a 0.25 -o 3 -V 2 -uw 80 -L 8 -LW 0.5
- Launch with Bash nohup (not PowerShell Start-Process bash).

## Done / failed today
- E6 own-lineage recombination: 0 wins on 30 puzzles (own programs +31% longer than best). Dropped.
- goodpjw plateau LNS: 13 instr in 2 rounds; plateau search exhausted on the frontier (Rudolph 0 over 1000 puzzles).
- Best 132,922 (poller). LB 2026-11-21: #1 127,800, #10 130,116.
- E2 -LW 0.5 keep (-1.05%). E3 hints drop. E1 toolkit transplant drop (worse). Public LNS engine (prvsiyan lns.cpp) 6 instr total, drop. -S slack inconclusive (retest with solver13+).

## Blocked / needs user
- (resolved: user approved public engines; they gave only 6 instr.)
- Use Hansen0223/Santa_2026 GitHub CSV (137,442 claimed, no license)? Not used.

## Next 3 steps (see brainstorm file for flags and stop rules)
1. E2 result -> E1 toolkit transplant (-P prefix mode, 20 ids).
2. E3 hint warm-start (public values as priced leaves in makeVirtual), the only idea aimed at beating best.
3. Every 5 experiments: Opus skeptic subagent. Retest -S with solver13.
