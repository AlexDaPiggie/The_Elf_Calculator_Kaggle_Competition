# Notebook synthesis 2 (2026-11-21 pass; builds on SYNTHESIS.md)
Read: 10 most-voted + 10 hottest (17 unique) + Pardheev 132,948 (outside both lists, but it moved the frontier). New notes: pardheev-132948, royalacecat-frontier-132952, goodpjw-lns-cpsat-132950, kindasomethin-133813, asterios-gift-per-run, avazaku-signed-regions, prvsiyan-santa-is-not-happy-1121, rudolph-1121, amanatar-validator-eda, evgendvorkin-inside-1121, nevska-explorer, unchanged-and-minor-1121. Six top-voted notebooks are unchanged.
Figures: kaggle kernels output now returns only log + csv (no __results__ PNGs), and pulled .ipynb files have no outputs, so no new figures. The numbers below come from kernel logs and our own read-only replay of downloaded outputs (scratchpad scripts cmp.py, overlap.py, shape.py, atoms.py).

## What changed in the public frontier since SYNTHESIS.md
- 135,761 (11-20 am) -> 134,190 (11-20 pm): graph-search lanes. Wang Jakie's C++ strategies (anneal, incremental, compact_rotate, quartet) run at scale by goodpjw (first hour -23/-16/-11), royalacecat's "seeded/retained" variant (near-length historical programs as crossover donors; v97 = 133,772), kindasomethin cap-16 graph pools (-7 own).
- 133.8k -> 132,948: Pardheev Krishna (own private pipeline). Holds the minimum on 964-966/1000 puzzles. vs our 134,190: -1,242 over 569 puzzles, 0 worse.
- Then only merges: royalacecat 132,952 (+1 own), goodpjw 132,950 (+2 own, same 2 every release), Asterios gift 132,949. Our best.csv = 132,948 (public union). LB #1 ~130.4k: gap ~2,550 (1.9%).
- The Wang Jakie notebook now returns 404; our copy predates the anneal/incremental strategies.

## New cross-notebook insights (with numbers)
1. Plateau LNS is exhausted on the converged frontier. Rudolph S1 (plateau walk + kicks + CP-SAT over every rebuilt recipe): 134,404 -> 134,404 over all 1,000 puzzles in 6.8 CPU-h; it finds 6-106 equal-length moves per puzzle, never a shorter one. goodpjw live demo at 132.95k: 0/32 (up to 3,900 accepted plateau moves, strict 0). Free-order CP-SAT with 4,000 helpers on 611 puzzles: 0 (fixed point). Our elfopt runs: 13 instr in 2 rounds.
2. What worked was NEW CONSTRUCTIONS. Pardheev's improved programs share only 46% of their values with the old ones (median Jaccard; helpers 33%); same-length rewrites share 98%. Their advice: beam constructor -> one short whole-program SA -> CP-SAT recombination of all near-optimal programs -> fresh starts rather than more polish.
3. The new programs pay MORE up front: 21.6 -> 27.9 instructions before the first target, fewer small constants (34.9 -> 32.7), targets used less as operands (8.9 -> 7.7), slightly more hubs (11.7 -> 12.2).
4. Small puzzles were not tight. Saved share by old length: <60 2.77%, 60-100 1.63%, 100-140 1.58%, 140-180 0.48%, 180-230 0.48%, 230+ 0.41%.
5. Atom structure exists but is uneven. T = q*x*y + e with x, y from the best program's pre-first-target values: real targets 3.5 bits cheaper than random numbers of the same size; per puzzle, 46/253 show >= 4 bits, 19 >= 8 bits, 8 >= 12 bits (scored_0705, 0942, 0307, 0227, 0053).
6. Register pressure is slack at equal length: avazaku's signed (+/-) region resynthesis saves 0 instructions on 133.9k but lowers peak live registers in 800/1000 puzzles (up to -15) and gives 695 equal-length variants with new intermediates.
7. Compiling wide DAGs with recomputation now exists publicly: prvsiyan sa1_joint.cpp "bounded register pebbling" beam (evict + recompute, lower bound from missing-node closure). This is the konbu "plan with 128, compile into 48" step.
8. Joint-target moves give crumbs at the frontier: bikram groups of 3 targets (3 puzzles, -1 each), prvsiyan internal cuts at non-target nodes dominating > 4 targets (2 puzzles, -1), kindasomethin group-8 (absorbed).

## Contradictions with SYNTHESIS.md
- SYNTHESIS ideas 1-3 (plateau LNS + kicks + trajectory CP-SAT; equal-length outer loop) ranked first. Now contradicted on the frontier (insight 1). Their gains came from files that were not yet converged (136.8k-134.5k).
- "Gains live in 60-180; small puzzles tight" vs Pardheev's largest relative gains below 100 instructions.
- "Recombination is finished (diversity collapse)" vs Pardheev: recombination works again when the pool holds an independent lineage.
- "Cheaper first-target toolkit helps" (Georgy/konbu) vs insight 3: the winner spends more before the first target. Consistent with Rudolph's toolkit-lock failure and our E1: the scaffold must be planned for the later targets.
- Hubs: Rudolph's detectors pick wrong hubs (+2.6%) vs Pardheev "seeding atoms helps a lot". Our check: real structure, but only in ~10-20% of puzzles; it may help as soft seeds, not forced targets.

## Highest-value NEW ideas (gain per cost). No submission needed for any test; tests read best.csv only.
| # | Idea | Source | Expected | Test (< 1 h after build) | Stop rule |
|---|---|---|---|---|---|
| 1 | Hand-merge Asterios gift scored_0137 (54 -> 53; program in cell 7 of the gift notebook, no output csv so the poller cannot see it). Also scan notebooks with WRITE_SUBMISSION-style flags | asterios-gift | -1, 5 min | replay + merge | - |
| 2 | Own-lineage recombination: for each puzzle, K=8 diverse own programs (6 target orders, 2 seeds, R=48 and R=96 plans: recipes only, validity not needed) + best; pool recipes + all one-op cross recipes (cap ~2,000), free-order min-value model (scipy milp now, or pip install ortools CP-SAT), compile with low_pressure_order + Belady, replay | pardheev #3/#5, icefire cpsat_plan, avazaku exact_graph (reimplement, read only) | -200 to -800 if it reproduces Pardheev's effect | 30 puzzles of length 60-140, 30 s solve each, 16 cores | 0 strict wins on 30 -> drop; >= 3 wins -> scale to the <140 band (578 puzzles) |
| 3 | Short polish of OUR fresh programs before pooling (elfopt already scanned/approved, 10 s, kicks) | pardheev #2/#5 | makes idea 2 donors near-best | 20 puzzles: own -> elfopt 10 s; gap to best before/after | closes < 30% of the gap -> pool unpolished programs |
| 4 | Pebbling compiler for R=96 plans (evict + recompute beam, lower bound = missing closure) | prvsiyan sa1_joint, konbu | own single run -5 to -8% (E5' R=96 planned -10.3%) -> better donors | Python on b20 R=96 DAGs; compiled length vs R=48 5,134 | compiled >= 4,900 -> drop |
| 5 | Atom seeds as priced leaves (not forced): atoms = pre-first-target values of best (oracle) and q*x*y products; arm of idea 2 for diversity | pardheev #4, rudolph oracle -20% | -1 to -3 on the ~50 structured puzzles | top 20 puzzles by atoms2 score, own solver with seeds -> pool | no win over idea-2 baseline on those 20 -> drop |
| 6 | Signed-region equal-length variants (avazaku reimplemented) as extra pool members + register relief | avazaku signed regions | small; diversity | add variants to idea-2 pools on the same 30 puzzles | no extra wins -> drop |
| 7 | Budget routing: CPU first to the <140 band (Pardheev % gains 1.6-2.8% vs 0.4-0.5% above 140) | pardheev analysis | efficiency | order work by band | - |
Dropped now: more plateau LNS / kicks / trajectory CP-SAT on the frontier, plateau archives, re-running public graph-search engines (0-2 per release for their owners).

## Reframes
1. Diversity reframe: our weaker solver is an asset. Nobody else holds our lineage; recombining it with the frontier is the one move the public cannot copy. Stop polishing the frontier; generate independent programs.
2. Investment reframe: score a construction by what its scaffold enables later, not by first-target cost (winners pay +6 before the first target). Push lookahead weight (-LW) and early helper building rather than cheap toolkits.
3. Currency reframe: registers are a spendable budget. At equal length 800 puzzles have up to 15 spare registers; plan wide (R=96), then compile with recomputation (pebbling) only where pressure binds.
4. Compiler reframe: recombination fails mostly at compile time ("a cheaper graph is not a cheaper program": Atakan, Rudolph). One good 48-register compiler (pebbling + low-pressure order) unlocks ideas 2, 4 and 6 together.

## Focus areas asked for
- Konbu-style virtual registers: public tool now exists (pebbling); our E5' -10.3% says worth building (idea 4).
- Plateau / equal-length LNS: dead on the frontier (insight 1); keep only as a polish of fresh programs (idea 3).
- Joint helper planning: only crumbs publicly (insight 8); the effective form is joint value-set selection over a diverse pool (idea 2).
- Hub/structure detection: atoms are real in ~10-20% of puzzles (insight 5); use as soft seeds (idea 5), never forced.
