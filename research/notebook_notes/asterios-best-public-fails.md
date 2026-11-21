# asteriospanoras/santa-2026-best-public-score-dataset-fails (83 votes, top by votes)
Author: Asterios Panoras. Claimed 135,761 (per-puzzle merge of 25 public sources + 2 instr from re-running Atakan's multiplier-frontier optimizer). Pulled: research/kernels/santa-2026-best-public-score-dataset-fails.v3

## Method (plain words)
- No search in the notebook: replay + merge + guide. Dataset santa-2026-elf-programs-and-experiments holds best_programs.csv (with per-program source), experiments.csv, elf_tools/ (dag4.py exact depth-4/5 numpy MITM, cone re-synthesis, joint-cut, extended suffix rebuilder in C++).
- 17 measured ideas on the frontier; only 1 gained (E16, -1 instr).

## Key numbers
- Instruction budget of 135,761: first targets 21,688 (16%), 10-19 bit 5,968 (4%), 20-29 bit 16,669 (12%), 30-39 bit 27,903 (21%), 40-49 bit 29,482 (22%), 50+ bit 34,051 (25%).
- First target 21.7 instr = 4.9x a later one; per-target cost falls from 6.6 (2nd) to ~3.3 (25th+).
- Cost per target by size: 1.2 (0-4 bit) ... 4.2 (35-40) ... 7.4 (55-60). Bits/instruction peaks ~10 at 40-45 bits.
- E10: targets built alone from live regs after 10th target cost 7.57 vs 4.76 in best programs (+59%). 43% of computed values are read 2+ times; ~20k instructions are never read again (pure target writes).
- E07: exact search rebuilds only 77/88 2-instr, 58/74 3-instr, 33/64 4-instr cones at original cost: cone leaves are overwritten mid-cone, so "local no gain" is not optimality.
- E17: 10,456 strong pair relations tj ~ (p/q) ti, 39% already used, unused ones give 0.
- E15: dictionary of base B powers: +44 to +168 worse on 10 puzzles.

## Figures (research/notebook_notes/asterios-best-public-fails/)
- __results___11_0.png: stacked bar of the 135,761 budget (numbers above).
- __results___18_0.png: near-duplicate targets only in "shared" (10% of neighbour pairs) and "mixed" (3%); targets within 4 instr of starts+smaller targets: independent 0%, shared 9%, multiplicative 26%, mixed 2%.
- __results___21_0.png: cost per target by size + first-target curve (21.7, 6.6, 5.6, 5.2, ...).
- __results___24_0.png: independent build 3.2 (20-29b) to 11.7 (60-69b) vs 4.76 shared; value reuse histogram.
- __results___28_0.png: frontier history 1.49M -> 191,867 -> 135,761 in 56 h, 199 merge steps.

## Failed (their E-cards)
E01 merge (already best file), E02 DCE (0 dead), E03 depth<=3 tree re-synthesis (0), E04 move leaf targets (0), E05/E06 depth 4/5 MITM (0), E08 greedy suffix re-plan (0), E11 wider suffix rebuilder beam 8-128 (0), E12 joint cut with depth-5 exact (0), E13 multi-start from 1,616 near-best alternatives (0), E14 joint target pairs rebuilt at end (0).
Gain: E16 helper-group joint rebuild at the cheapest original positions (all targets using one helper, re-inserted with reverse beam, live values pinned): -1 on 1000 puzzles.

## Reusable for us
- replay/merge_programs/compare_submissions (we already have equivalents).
- Per-target accounting loop (cell 10): cost between consecutive new targets + read counts per value; cheap diagnostic for our solver vs best.

## Already in our log?
- Suffix re-solve, DCE, merge, MITM A*B+-C: yes, all 0 for us too. Toolkit: E1 dropped. Nothing new to run from here; value is the negative list (do not repeat E03-E15).
