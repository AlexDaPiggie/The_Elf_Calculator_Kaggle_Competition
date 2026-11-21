# goodpjw2008/santa-2026-lns-cp-sat-recombine-lb-132-950 (v28; old note goodpjw-lns-cpsat.md covers v1 at 135,787)
Author: goodpjw2008. Claimed LB 132,950 = public frontier 132,952 - 2 own strictly shorter programs. Pulled: research/kernels/santa-2026-lns-cp-sat-recombine-lb-132-950 (log + csv in research/kernels/_out/; compiled elfopt deleted unrun).

## What is NEW vs the 135,787 note
- Version table v21-v28 (11-21 10:08-13:16 KST): every release = re-merge public frontier + the same 2 own programs. Frontier went 133,831 -> 132,952 in 3 hours of their table; own lane adds only -2 per release now.
- Item 6 "orchestrating public engines on 20 cores": they run Wang Jakie's C++ graph-search strategies unchanged (anneal, incremental, compact_rotate, quartet) with fresh seeds + more rounds; "*_seeded" variants put near-length historical programs into the crossover pool. First hour: anneal -23, incremental -16, compact_rotate -11. Since 11-21 also Atakan's multiplier-frontier and interface-closure optimizers and royalacecat's donor-retaining *_diverse pool.
- Own addition: PLATEAU ARCHIVE - every equal-length alternative any engine returns is kept and used as a later starting point, so searches stop restarting from the same converged program.
- Source table at 132,950: Pardheev bank holds the minimum on 964/1000, kindasomethin 134,091 on 16, amanatar 9, an old 135,931 bank 9, own 2.

## Key numbers (kernel log of this run)
- Live demo: elfopt --time 20 --kicks 1000 --kslack 2 on 32 shared/mixed/multiplicative puzzles: 0 saved. Per puzzle: 600-13,800 evaluations, 150-3,900 accepted plateau moves, strict 0, kicks 0-10. The engine walks the plateau a lot and never goes down on the current frontier.

## Figures
Dashboard and family plots exist in the rendered notebook only; CLI output has no PNGs. Plot code (cell 7) is unchanged: instr/target vs mean target bits by family; scored_0001 targets-per-instruction histogram; length vs #targets.

## Reusable for us
- Plateau archive idea: keep all equal-length variants as diversity for recombination (cheap).
- The wangjakie strategy names (anneal / incremental / compact_rotate / quartet) are in a NEWER wangjakie version; the wangjakie notebook now returns 404 (deleted or private), our pulled copy (research/kernels/santa-2026-arithmetic-recipe-pool-and-milp) predates these strategies.

## Failed (new)
- Demo 0/32 at the frontier. Their "what did not work" list is unchanged (full depth-5 MITM 0 hits, fixed-order CP-SAT 0, greedy depth-5 constructor 271 vs 230).

## Already tried by us?
- We ran elfopt via src/gp_lns.py: 7 + 6 instr in two 39-min rounds; 120 s test pending. Same verdict as their demo: plateau LNS is exhausted on the frontier.
