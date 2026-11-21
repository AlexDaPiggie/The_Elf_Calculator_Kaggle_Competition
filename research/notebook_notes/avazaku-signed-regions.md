# avazaku/elf-calc-signed-regions-and-register-scheduling (new notebook of the same author as avazaku-paired-helpers.md)
Author: Sargis Khachatryan. Input = royalacecat Public Frontier V76 (133,924). Result: 0 instructions saved; lower peak register demand in 800 puzzles (max -15 registers); 695 puzzles get a different intermediate value set at equal length. Pulled: research/kernels/elf-calc-signed-regions-and-register-scheduling

## Method (plain words), pure Python, ~250 lines
1. read_recipes: value -> (op, a, b). Collect connected REGIONS of + / - recipes (BFS over users/operands inside the add/sub set), plus sub-regions of radius 2 around each node for big regions.
2. For each region, write every exit value (target or used outside) as a signed multiset of region inputs ("signed sums"); cancel opposite terms.
3. Try expressing one exit through another exit (delta of signed forms, two orders: shortest-first and reversed).
4. Greedy pair merge: repeatedly pick the pairwise sum |a+b| shared by the most equations (rank prefers values already known), make it a new intermediate (check <= value_limit), until each equation is one term. Two tie policies (small/large value first).
5. Reject cycles (DFS), accept if fewer recipes; with reshape=True also keep an EQUAL-length rewrite that introduces the most new intermediate values.
6. Scheduling: low_pressure_order (ready list, prefer ops that release operands: priority new_live - released), pack_circuit (last-use register reuse), live_peak; pick (length, peak) lexicographically over original order and two tie orders.

## Insights with numbers
- On the 133.9k frontier, linear (+/-) regions are already optimal for instruction count (0 saved) but NOT for register pressure: 800/1000 puzzles can run with fewer live registers, up to 15 fewer.
- 695 puzzles get an equal-length program with different intermediates: a cheap plateau generator.

## Figures
None (prints only).

## Reusable code ideas
- signed-sum region resynthesis (optimize), low_pressure_order, live_peak, pack_circuit: small, readable; we can reimplement for (a) diversity input to recombination, (b) freeing registers so a later pass can keep more hubs alive.

## What failed for them
- No instruction gain at the frontier.

## Already tried by us?
- No. Our solver never minimises peak pressure at equal length.
