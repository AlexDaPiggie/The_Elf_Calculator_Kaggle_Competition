# lucifer19/santa-2026-the-elf-calculator-x-ray (v2)
Author: Adaptive Agent Systems. Claimed <= 141,361 (merge + 5 re-solved cones). Value: measurements of where instructions go and how locally tight the frontier is. Pulled: research/kernels/santa-2026-the-elf-calculator-x-ray

## Method (plain words)
Merge public files; for every target cut its exclusive cone (instructions feeding only it); everything else is "shared scaffolding". Re-solve each cone with a meet-in-the-middle search (1- and 2-instruction hash tables, inverse ops, shapes up to 5 instr + 6-instr m*q +- z), splice, re-allocate.

## Key numbers
- 48% of all instructions are shared scaffolding (median 47% per puzzle, range 0.28-0.62).
- Cone re-solve over all 26,898 targets (5.3 CPU-h): 5 shorter (0.02%), 22,845 equal (84.9%), 4,048 deeper than search (15.0%). Re-run on 217 changed puzzles: 1 shorter.
- Counting floor with 48 regs ~12.8 bits/instr: 60-bit target >= 5 instr, 40-bit >= 4. All-in cost is 2-3 instr above the floor at 50-60 bits; the exclusive cone alone is below the floor (paid by scaffolding).

## Figures (research/notebook_notes/xray/)
- __results___22_1.png: avg program by value_limit bits: 1-19 (27 puzzles) ~12 instr, 20-29 (94) ~34, 30-39 (102) ~85, 40-49 (304) ~140, 50-55 (214) ~175, 56-60 (259) ~192; about half exclusive / half scaffolding in each. Histogram of scaffolding share, median 47%.
- __results___25_0.png: per target vs size: floor steps 1/2/3/4/5 at 12/25/38/51 bits; exclusive cone 1.2 -> 4.9; all-in 1.4 -> 8.1 (60+ bits). Gap all-in minus cone = scaffolding ~3 at 55-60 bits.
- __results___13_0/16_0/31_0.png: puzzle map, credit map, frontier ladder (not inspected in detail).

## Failed
- Segment re-solve (scored_0002: only 4/28 segments have no value reused later, none shorter).
- Ruin and recreate of one shared helper + dependants: 0 on 0001, 0002, 0100.
- Look-ahead re-solve (target may use values computed after it): 0 on 6 puzzles.

## Reusable for us
- anatomy(puzzle, program) (exclusive cones) and Workspace().solve(values, target, limit, max_cost).
- The scaffolding number: half the cost is helper planning, so improving per-target search can at best touch the other half.

## Already in our log?
- Matches our probe "per-target search is not the weak point" (one-target probe -4%). Scaffold planning is what our suffix probes showed (+36-40%).
