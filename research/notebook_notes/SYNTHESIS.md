# Notebook synthesis (2026-11-20). 17 notes in this folder; figures in subfolders (rendered __results__ PNGs).
Our best/best.csv now replays 135,596 (wangjakie 135,598 merged). LB #1 ~130.4k, #10 ~132.8k. Length bands of our best:
<60: 136 puzzles / 3.7k instr | 60-100: 116 / 10.4k | 100-140: 320 / 37.4k | 140-180: 171 / 27.6k | 180-230: 181 / 37.3k | 230+: 76 / 19.2k.

## Cross-notebook findings (with numbers)
1. The frontier is one lineage. 997/1000 merged programs come from one notebook line (Rudolph); every merge now ties at 135,761-135,763 (royalacecat). Merging alone is finished as a lever.
2. Half the cost is scaffolding. 48% of instructions serve 2+ targets (X-Ray); targets built alone cost 7.57 vs 4.76 (+59%, Asterios E10); first target 21.7 instr = 4.9x later ones; 16% of all instructions precede the first target.
3. Per-target cones are locally tight. Cone re-solve: 5 shorter of 26,898 (X-Ray); 13 of 17 Asterios ideas gave 0; full depth-5 MITM: 0 hits on 48-59 bit targets (goodpjw).
4. What still gains at the frontier is NON-LOCAL and NON-GREEDY: goodpjw LNS with plateau kicks + trajectory CP-SAT (-319 in 25 min from 136,829; -18 vs merge at 135.8k), wangjakie equal-length exchanges (-163 over 129 puzzles from 135,761), kindasomethin group-of-8 helper backbones (-6 to -23 per release).
5. Gains live in mid-size programs. goodpjw: 14 instr per 100 runs at 100-140 length, ~0 above 180; wangjakie wins at 107-188; konbu: recombination helps below ~150. Large independent puzzles (60-bit clusters, 8.6 instr/target, figs goodpjw 7_0 and rudolph 23_0) resist every public method.
6. Best public constructive solver = konbu planner: plan with 128 virtual registers + separate cost-aware re-allocator (evict min rebuild_cost^2/next_use_distance, search emission order): single run 150,714; + lookahead (own + 0.4 x remaining): 146,516. Our best single run is 169,483 (L3_full). 192 registers loses on large puzzles (~30 rebuilds).
7. Hidden structure exists but is hard to name: T = q*h + r with h ~18 bits, r ~10 bits (Rudolph); oracle hubs -20% on 16 puzzles, but detectors pick wrong hubs (+2.6%). 2x2 target grids T1*T4=T2*T3 in 151 puzzles do not beat the merge.

## Contradictions
- "Local rewrites find nothing" (Asterios 16/17 nulls, X-Ray) vs wangjakie -163 and goodpjw -319: both are true. Strict-descent local search is stuck; plateau moves (equal length, p=0.3, kicks of +2) open new optima. Our -S slack failure was inside the constructive solver, not plateau moves on a finished DAG.
- "Public LNS = 0 on the frontier" (goodpjw, our 6-instr run) vs goodpjw's own LNS gains: the difference is kicks, depth-5 near-miss T = X*Y +- R from sorted neighbours, helper-rooted destroy, and recombining the search trajectory.
- Toolkit: Georgy/konbu say "a cheaper first-target toolkit would help every puzzle" vs Rudolph (toolkit lock +3 to +15%) and our E1 (worse). The toolkit must be chosen jointly with later targets, not fixed.
- Depth: near-miss depth-5 helps (goodpjw) but exhaustive depth-5 MITM gives 0 (goodpjw, Asterios E05/E06). Use depth only as a guided shape, not brute force.

## Ranked ideas for us (gain per cost). Each test < 1 h on our 16 cores.
| # | Idea | Source | Expected | Test (< 1 h) | Stop rule |
|---|---|---|---|---|---|
| 1 | LNS lane with plateau + kicks on 60-180 band (goodpjw elfopt source is in research/kernels/santa-2026-public-frontier-score-135-761 cell 5; running it needs the user's OK for third-party code, else port Searcher/LNS ideas into our C++) | goodpjw, royalacecat | -50 to -300 per night | 100 puzzles of length 100-140 from best, --time 15 --kicks 1000 --kslack 2, 14 seeds/shards; count strict wins | < 5 instr per 100 puzzle-runs -> drop |
| 2 | Trajectory recombination: dump all accepted recipes during LNS (--dump/--hall), pool with best, free-order CP-SAT min-value model (IceFire cpsat_plan), re-allocate | goodpjw (-45/-28/-4 per pass) | -30 to -100 | 30 puzzles where idea 1 moved on the plateau; 30 s CP-SAT each | 0 wins on 30 -> drop |
| 3 | Equal-length diversification outer loop: N neutral recipe swaps (keep length), then strict repair; restart from champion every 3 rounds | wangjakie (-163) | -50 to -200 | 30 puzzles 100-190 length; compare eq 0.3 vs eq 0.6 + 3-11 neutral swaps per round, same CPU | no gain over plain idea 1 -> drop |
| 4 | Fresh-helper MILP on best: helper h = a op b (new value) with existing v = h op x; rank by freed private instructions (bitmask); scipy milp min values; 3 emit orders | avazaku (908 wins at 142.9k) | -10 to -60 (frontier absorbed most) | Python, 50 puzzles, 2 configs (500/w4/mode2, 600/w5/mode1) | 0 wins -> drop |
| 5 | Our solver: plan with 96-128 virtual registers, then post-hoc allocator (Belady + rebuild_cost^2/dist + emission-order search) | konbu (150.7k single vs portfolio 165k) | own single run 169k -> ~150k; only matters as LNS seed diversity | b20: rerun with R=128 in planning, measure planned length and peak live values (upper bound of gain) | planned length < -8% on b20 -> build allocator, else drop |
| 6 | Pollard-rho cofactor candidates: factor T +- r (small r) and add cheap factors as priced leaves / LNS repair shapes | ozertuu | unknown, small | offline scan on 20 large puzzles: fraction of targets with a factor in pool or 1 op away | < 5% of targets -> drop |
| 7 | Spend CPU where sources disagree: puzzles with several distinct same-length public programs or high length z-score | lightningv08, kmmmvs | efficiency only | rank puzzles; apply to idea 1 order | - |
Already done or failed (do not repeat): merge, DCE, suffix/tail re-solve on public best, depth<=5 cone re-solve, MITM A*B+-C, toolkit lock, base-power dictionary, hub detectors as forced targets, E3 hints, -S slack.

## Reframes
1. Objective reframe: stop "constructing a program", start "walking the plateau of the incumbent DAG". Accept equal-length moves; the value of a move is the new integers it leaves available (wangjakie, goodpjw).
2. Representation reframe: split value selection from register allocation. Plan as if registers were unlimited (128), compile into 48 later (konbu); our solver couples both inside the beam (-k 4 eviction).
3. Data reframe: the search trajectory is a recipe bank. Every visited same-length program adds recipes; CP-SAT over their union finds programs no single visit contains (goodpjw). Public merges recombine banks; recombine our own history instead, which nobody else has.
4. Budget reframe: CPU goes to the 60-180 band (607 of our puzzles, 75k instr), not to the largest independent puzzles.

## What the 130-131k teams might do differently (inference from notebook evidence only)
- Gap is a different construction, not a better merge: leader ~5,300 below the merge on 11-18 and ~8,000 later (Rudolph); screenshot leader 130,600 (a005). All public banks are one lineage, so the top teams likely own a separate lineage started from a much stronger planner (konbu-style 128-register planner + lookahead reaches 146.5k single run; Hansen's independent solver 146k per sota note).
- Compute: konbu used ~1,100 CPU-hours; goodpjw 20 cores for 8 h for -18 at the frontier. Top teams likely run LNS + recombination for hundreds of CPU-hours on their own lineage.
- Scaffolding is 48% of cost; the hub oracle gives -20%. A team that names hubs from targets (or plans helpers jointly per group of targets, kindasomethin group-of-8) would cut exactly the part public LNS cannot touch. Evidence is indirect: nobody public has done it.
