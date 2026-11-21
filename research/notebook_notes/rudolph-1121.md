# alexchilton/rudolph-the-red-nosed-register-allocator (version pulled 11-21; old note rudolph.md covers v3)
Author: alex chilton. Pulled: research/kernels/rudolph-the-red-nosed-register-allocator.n1121. Kaggle output download was empty (0 files).

## What is NEW (two rows added to the failure table)
1. "Re-choose recipes jointly by integer program (CP-SAT)" (avazaku / royalacecat style: charge each intermediate once): 134,664 -> 134,664 over all 1,000 puzzles in free order; 611 puzzles with 4,000 candidate helpers each. Reason: the best programs are a FIXED POINT over their own values; goodpjw gains only by pooling recipes from a whole search run.
2. "Plateau walk with kicks, then CP-SAT over every rebuilt recipe" (their S1 = goodpjw method): -7 on the 134,475 file; then 134,404 -> 134,404 over all 1,000 puzzles (30 s walk + 60 s CP-SAT per puzzle, 6.8 h on Kaggle). After the cron merged the newest public programs, the walk finds 6-106 equal-length moves per puzzle but never a shorter one.
- Odd: this pulled version drops section 5b (slack table, hub stats) that v3 had; facts in rudolph.md still stand. The dataset list now attaches 20 public kernels incl. pardheev 132,948 and goodpjw 132,950 (merge carrier role).

## Insights with numbers
- Strongest public evidence that plateau LNS + recombination of its own trajectory is EXHAUSTED on a converged frontier: 0 over 1,000 puzzles, 6.8 CPU-hours (Kaggle 4 cores).
- Equal-length neighbours are plentiful (6-106 per puzzle) but none leads down: the plateau is wide and flat.

## Figures
Unchanged (__results___23_0 instr/target bands; see rudolph.md). No PNGs via CLI.

## Reusable
- The negative result itself: do not spend CPU on plateau+kicks+CP-SAT over the frontier.

## Already tried by us?
- Our goodpjw-engine runs (13 instr over 2 rounds) agree. Our idea list in SYNTHESIS.md ranked plateau LNS #1: now downgraded (see SYNTHESIS2.md).
