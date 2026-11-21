# prvsiyan/santa-is-not-happy (new version 11-21; old note prvsiyan-santa-is-not-happy.md)
Author: prvsiyan. Embedded validated seed 133,835 (public 133,924 at run time). Kaggle run: 4 workers x 6 min, 84 attempts, 0 improved. Pulled: research/kernels/santa-is-not-happy.n1121; output sources (lns.cpp, poolc.cpp, sa1_joint.cpp, sa1_windows.cpp, relink*.py) in research/kernels/_out/santa-is-not-happy (binaries deleted unrun).

## What is NEW
- sa1_joint.cpp (~1,100 lines): their LNS plus SA1 "multi-output INTERNAL cuts": an internal node (not a target) whose siblings share an expensive ancestor and dominate many (> 4) targets is cut and rebuilt jointly; old target-subset neighbourhoods never select such nodes. Also "adjacent graph values" cuts (common ancestors 1-2 ops apart), deliberately choosing a 2-op derivation for one output to expose a new basis value, crossing a modest pressure barrier during search.
- Bounded REGISTER PEBBLING beam search over a fixed value DAG: a node may be recomputed after eviction (not only reordered); state = resident values + observed targets; missing-node closure as lower bound. This is a real re-allocator for DAGs that need > 48 live values - the konbu-style "plan wide, compile later" step.
- sa1_windows.cpp: joint live-output instruction-window synthesis (re-synthesise a window of instructions given what is live at its ends); 40-puzzle pilot: 0.
- Provenance of their 133,835 seed: bikram 516 puzzles, own lanes 219, mizero 81, IceFire 42, ozertuu 31, rudolph 19, own SA1 14, own lns_c 5, others small.

## Key numbers
- Internal-cut solver: validated 1-instruction reductions on scored_0944 and scored_0111 (mixed family). Window pilot and donor-graft pilot: 0.
- Kaggle run itself: 0 improved in 360 s.

## Figures
Rendered results chart (instructions by stage) exists on Kaggle only; CLI output has no PNG.

## Reusable code ideas
- Register pebbling with recomputation (sa1_joint.cpp bottom section) = the missing piece for our R=96/128 virtual-register plans (E5'): compile a wide DAG into 48 registers paying recomputes.
- Internal-cut selection rule: cut at non-target nodes that dominate many targets.

## What failed
- Window synthesis pilot (0/40), donor graft (0).

## Already tried by us?
- lns.cpp run (inconclusive, 6 instr). SA1, pebbling: not tried. Code was scanned only by reading comments here; any run needs a full scan + user OK.
