# pardheev/132-948-best-public-score-santa-2026 (was "santa-2026-132997-validated-programs")
Author: Pardheev Krishna. Claimed 132,948 (replay log: 0 invalid). Not in the top-10 vote/hot lists but the biggest frontier mover of 11-21: holds the per-puzzle minimum on 964-966 of 1,000 puzzles in goodpjw's and royalacecat's merges. Pulled: research/kernels/132-948-best-public-score-santa-2026; output in research/kernels/_out/pardheev/submission.csv.

## Method (plain words; only advice, search code is private)
Notebook = validator + replay of dataset pardheev/santa-2026-elf-calculator-132997. Their "what helped us most" list:
1. Good constructor first: beam search over value DAGs, targets derived one after another from a 1-2 instruction dictionary, many partial programs in parallel; narrow beams need a greedier weight on estimated remaining cost.
2. Simulated annealing on the WHOLE program: moves rewrite helper values and re-derive the targets that use them; register scheduler fits into 48.
3. Recombine, do not only re-run: all near-optimal programs of a puzzle in one recipe graph, CP-SAT picks the smallest value set.
4. Target structure: in several families many targets look like m * a_i * a_j + e for a few hidden "atoms"; build those products first and seed the search with them.
5. Fresh starts beat more polishing: after one polish, more SA rarely helps; new constructions (new beam sample, or re-planning part of a program on top of the rest) + one short polish keep finding gains.

## Our read-only analysis (src: scratchpad cmp.py / overlap.py / shape.py / atoms.py, our own code)
- vs our 134,190 file: -1,242 over 569 puzzles, 0 worse. Savings 1-8 per puzzle (199 x1, 156 x2, 153 x3, 42 x4, 19 x5+).
- By old length band (% saved): <60 2.77%, 60-100 1.63%, 100-140 1.58%, 140-180 0.48%, 180-230 0.48%, 230+ 0.41%. Small puzzles were NOT tight.
- vs kindasomethin 133,813: -865 over 449 puzzles (same band shape).
- Improved programs are NEW constructions, not edits: value-set Jaccard old vs new median 0.465 (p10 0.13, p90 0.81); helper-only Jaccard 0.33. Same-length changed programs: Jaccard 0.98.
- Shape of improved programs (old -> new means): instructions before the first target 21.6 -> 27.9 (more scaffolding up front), small constants (<2^16) 34.9 -> 32.7, targets used as operands 8.9 -> 7.7, hubs (>=2^14, read 3+) 11.7 -> 12.2, multiplications 44.6 -> 43.0.
- Atom check: with atoms = values before the first target, best bits(q)+bits(|e|) for T = q*x*y + e is 30.4 for real >=30-bit targets vs 33.9 for random numbers of the same size (60% of targets cheaper than null, 16% by >= 8 bits). Per puzzle (253 sampled, best file): 46 puzzles >= 4 bits of structure, 19 >= 8 bits, 8 >= 12 bits (top: scored_0705, 0942, 0307, 0227, 0053). Structure is real but concentrated in ~10-20% of puzzles.

## Figures
None in the notebook (prints a table of instr/target by #targets and digits: 28+ targets at 18 digits 6.37, 15 digits 5.76, 12 digits 4.95).

## Reusable for us
- Recipe: diverse fresh constructions -> pool per puzzle -> CP-SAT min value set -> compile -> one short SA polish.
- Scaffolding-first objective (pay more before the first target).

## Failed for them
Not stated beyond "more SA after one polish rarely helps".

## Already tried by us?
- Recombination of our own diverse runs with best: NOT tried (sota idea 6 proposed, never run). Atom seeding: NOT tried (hub detectors as forced targets failed for Rudolph; this is softer: priced leaves). Whole-program SA: NOT tried.
