# konbu17/santa-2026-wider-dictionary-portfolio-163k (74 votes, #2 by votes)
Author: konbu17. Latest version claims 142,940 (title still says 163k), ~1,100 CPU-hours offline; dataset konbu17/santa-2026-elf-calculator-programs is the root of most public lineages. Pulled: research/kernels/santa-2026-wider-dictionary-portfolio-163k (old) and .v3 (new text).

## Method (plain words) - this is the best documented CONSTRUCTIVE solver in public
Base: Tony Li backward beam over a 0/1/2-instr dictionary + farthest-next-use allocator. Then, in order of impact:
1. More leaves: 72/88 leaves w10 174,184 vs original 52/56 191,867; past ~90 leaves worse (rebuilds 2% at 72/88, 10% at 64/112). 50 beam settings portfolio 165,055.
2. Register-aware planner, cheapest target first: keeps a simulated register file, uses only values really present, charges true rebuild price, runs the beam for EVERY missing target and builds the cheapest now.
3. PLAN WITH MORE REGISTERS THAN EXIST: run the planner as if 128 registers, then squeeze into 48 with a separate re-allocator. Over 1,000 puzzles the allocator needs < 100 extra instructions in total. Single run 150,714 (better than the whole 50-setting portfolio). 192 registers is shorter still but on the largest puzzles ~30 rebuilds eat the gain.
4. One-step lookahead: take 6-8 cheapest candidates, build each, score own + 0.4 x remaining cost; incremental dictionary update. Single run 146,516.
5. Re-allocator (930 final programs): evict smallest rebuild_cost^2 / distance_to_next_use (Mizero idea) + search over target emission order.
6. Tail re-solve (237 programs): keep first K targets, re-solve last 6-10 with lookahead and another tie-break seed; wins ~1 in 5. Middle windows do not work.
7. Recombination (438 programs): union of values of several programs, all single ops between candidates, CP-SAT min value set, acyclic, then allocator. Helps most below ~150 instructions; stalls after ~1 min on large puzzles.
8. Exact rewrite pass (41 programs): re-derive each value by a different single op on defined registers; delete instructions that become dead (6=3+3, 9=6+3 -> 9=3*3).
9. Exact MITM (18 puzzles): pool reachable in <=3 instr (tens of millions), test t = x op y up to cost 7 via hashing and two-pointer.

## Key numbers
first 5 targets ~8 instr each on large puzzles, later ~5. Beam width alone: w3 191,867 -> w100 184,072.

## Figures
None of note (tables only).

## Reusable for us
- The 128-virtual-register plan + separate cost-aware allocator is the most direct fix for OUR solver, which plans inside 48 registers with in-search eviction (-k 4 -uw 80). Their single run 150.7k / 146.5k vs our best single run 169.5k (L3_full).
- Lookahead weight 0.4 on remaining cost (we use -L K with -LW 0.5 state-value).

## Failed (their notes)
- >90 leaves worse; 192 regs loses on big puzzles; middle-window re-solve fails; CP-SAT stalls on big puzzles.

## Already in our log?
- Leaves/virtual leaves (-V), lookahead (-L, -LW), greedy order (-o 3), suffix re-solve (0 gain on public best), DCE: yes. Virtual 128-register planning + post-hoc re-allocation + order search: NOT tried. This is the most likely reason our standalone solver is 169k vs their 146k.
