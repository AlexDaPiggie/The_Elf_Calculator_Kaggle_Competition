# Merge carriers and baselines (one note for 8 low-novelty notebooks)

## tonylica/elf-calculator-with-register-reuse (30 votes) - 191,867
Root of nearly all lineages: backward beam (width 3) over a dictionary of values reachable in 0/1/2 instr from leaves (constants, starts, previous targets, recent intermediates); reduction T = q*f + r ("97 = 6*16 + 1"); rank by instr + alpha*log2(remaining); allocator evicts farthest next use and rebuilds if needed. Our solver is the same family.

## navneetprabhat/santa-2026-beam-dictionary-portfolio-135k - 135,912
Merge carrier (LLM-assistant written). Merge table: konbu 142,940 -> +avazaku helpers+chain resynthesis 908 wins 137,708 -> +hanif 95 wins 136,829 -> +IceFire 276 wins 135,912. Own solver wins 0 puzzles. Lesson: the 142.9k -> 137.7k step was avazaku's MILP helper method, not beam search.

## kmmmvs/analysis-santa-2026 + santa-2026-verified-best-of-merge - 135,763 at one point
Merge + per-puzzle analysis script (santa2026_analysis.py): live_len, dead_len, tail_len, robust z-score of length vs features (weak puzzle finder). Reusable idea: z-score of length residual to pick LNS targets.

## georgymamarin/santa-2026-why-the-first-target-costs-3x-more - merge 142,925
First target ~16 helper instr; 3/4 are small constants and almost all reused later (one-time toolkit). Puzzles with limits near 1e14 cheaper per target than 1e12. Figure (research/notebook_notes/santa-2026-why-the-first-target-costs-3x-more/fig01.jpg): banner trace "first target: 17 steps, the other 30: 4.8 steps each".

## rishabhbafnaiiitd/arithmetic-dag-synthesis-and-register-allocation - 137,866
Educational: counting bound log2(4608) ~ 12.17 bits per instr, 60-bit target >= 5 steps; DAG recombination + peephole + register scheduling over a 141,302 bank. No new technique.

## hidsaito/santa2026-a005 - 138,301 (-41 vs A004)
Japanese. Rebuild 1/2/3 outputs with backward beam, CP-SAT graph combination; best arms: 2-output joint intermediate back-solve (-11 over 16,316 rebuilds), free-order recombination (-7 on 642). ~50k rebuilds for -41. Notes leader 130,600 from a board screenshot (gap 7,701).

## santiagozazo bottleneck EDA (137,792 bank) / CP-SAT multi-bank fuser
Histogram + top-25 longest puzzles. No method beyond multi-bank CP-SAT (same as IceFire).

## sacuscreed public-merge, mizero merge-polish, nilanjan best-of-public, kozykappa, hanif, suka, elias
Pure merges (+ small window/suffix rebuilds, 0-7 instr per run). Nilanjan's suffix rebuilder: Asterios E11/E13 got 0 from it at the frontier.

## Already in our log?
All merged by the poller. Nothing to run.
