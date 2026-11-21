# avazaku: elf-calc-paired-helpers-and-target-scheduling (20 votes) + shared-helpers-chain-resynthesis + cross-trace-milp
Author: Sargis Khachatryan. No score in the title; in navneetprabhat's merge table this lineage was the biggest single contributor (908 puzzle wins, 142,940 -> 137,708). Pulled: research/kernels/elf-calc-paired-helpers-and-target-scheduling (+ chain-resynthesis, cross-trace-milp)

## Method (plain words) - pure Python + scipy.optimize.milp, readable, ~300 lines
extended_pool(starts, targets, programs, max_helpers, reverse, witness_limit, schedule_mode):
1. Read each program as value -> recipe (read_recipes). Union all values.
2. All one-op recipes between existing values that give another existing value (choices[z]).
3. FRESH HELPER h: forward(a,b) gives a new value h (not in program, <= max value); backward(v, x) checks whether an existing value v = h op x for some earlier x. If yes, h is a candidate shared helper for v.
4. Rank helpers by private instructions they could free: bitmask footprint/private sets per value (private = values used once); saving = popcount(private[v] & ~(needed by x, a, b)) - 1, summed over consumers.
5. Keep top 500-1200 helpers; add pair rules where two helpers combine (balanced expressions, first 64 helpers).
6. merged_order: topological interleave so every recipe uses operands earlier (no cycles).
7. exact_graph: MILP, one binary per value, cost 1 each, fixed = targets + forced common operands; each value needs one recipe with present operands (aux binaries for 2-operand recipes). node_limit 200.
8. allocate_graph in 3 emit orders x each source graph; keep shortest replay.
shorten() runs two configs: (500 helpers, witness 4, schedule_mode 2) and (600, witness 5, mode 1).
Chain-resynthesis notebook adds square_chain_cuts (cut one result + private chain, try short combos incl. squaring and exact division) and pack_circuit.

## Key numbers
- Inputs: IceFire V60 programs. Two dependency orders expose different candidate recipes.
- In the 142.9k era: 908 wins / -5,232 in one merge step (navneet table). Gains shrink as the frontier absorbs it.

## Figures
- Notebook plots a bar chart "instructions saved per puzzle" (not extracted; no rendered output pulled).

## Reusable for us
- extended_pool + exact_graph are self-contained Python (scipy milp, no ortools). Could be run on our best/best.csv per puzzle; helper scoring via bitmask private sets is a good pattern for our own solver ("which new value frees most private instructions").

## Failed
- Not documented in markdown.

## Already in our log?
- No. Our E3 hints / -V virtual leaves price helpers inside the constructive solver; the backward check "existing value = new helper op earlier value" + joint MILP over the whole program is new for us.
