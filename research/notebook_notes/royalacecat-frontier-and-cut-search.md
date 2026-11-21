# royalacecat (E-Max AI): public-frontier-score-135-761 + elf-calculator-residual-cut-search
Author: E-Max AI. Frontier notebook claims 135,761 (= best attached public bank; 3 LNS passes x 8 s/puzzle found 0 more on Kaggle). Residual cut search claimed 138,020 (1 instr over 138,021 inputs). ~20 "Public Frontier NNNNNN" versions in 24 h. Pulled: research/kernels/santa-2026-public-frontier-score-135-761, research/kernels/elf-calculator-residual-cut-search

## Method (plain words)
- Frontier notebook: pick the shortest fully replayed bank (IceFire, Asterios dataset), run goodpjw's LNS engine (elfopt.cpp, attributed, compiled inline) on puzzles with 60-180 instructions, 20 shards, fixed seeds, 2-3 passes, strict improvements only.
- Residual cut search (older): cut a value + its private cone; rebuild from retained values via 1-step bank (pair, f*q+-r) and optional 2-step bank (two-pointer sums/diffs/products); "shared cut": one new value rewires 1-2 consumers; CP-SAT recipe selection over values pooled from 2-3 banks; 48-reg list scheduler.

## Key numbers / findings
- "Reflexion" note: a cloud run was fed a stale 135,763 bank while 135,761 was public; local union of two independent LNS outputs + public bank gave 135,758. Lesson: always rebase on the freshest bank.
- Their survey: Roman IceFire and Asterios both 135,761; Ozer, Mizero, Wang Jakie 135,763 at that time.
- Residual cut search Kaggle run: 1 instr; earlier versions +13, +33 for our poller.

## Code worth knowing (read only)
- research/kernels/santa-2026-public-frontier-score-135-761 cell 5 = full elfopt.cpp (goodpjw design): HMap, Searcher (addS1/pairS1/find/find4/findWindow/oneStepCompletions/findPair/cost2), Dag (fromProgram/clean/pressure/listSchedule/fixPressure/emit), LNS (harvest/analyse/makePool/tryGroup/dominated/tryRemove/enumerateAlts/doKick/run), Constructor (greedy cheapest target + deepBuild split T = X*Y +- R). IO: "P id k starts m targets limit regs n" + n lines; output "R id n_old n_new".
- Cell 7: encode_puzzle / parse_engine_output / shard loop.

## Figures
Not extracted (frontier notebook is replay + engine log; no analysis plots of note).

## Reusable for us
- The elfopt block format and shard driver are a drop-in LNS lane if the user allows running public engines (STATE says engines were approved earlier; this task did not run anything).
- Puzzle-length filter 60-180.

## Failed
- 3 passes x 8 s per puzzle on Kaggle = 0 new instructions at 135,761 (short budgets are useless at the frontier).

## Already in our log?
- Residual cut search: in sota_2026-11-19 (not run). elfopt engine: not run. Merge of royalacecat outputs: yes (poller).
