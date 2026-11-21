# evgendvorkin/santa-2026-inside-the-elf-s-calculator (new version, 152 cells vs 96; old note inside-the-elf-evgendvorkin.md)
Author: Evgeny Dvorkin. No score (education + EDA). New "Part IV: Anatomy of 1,200 envelopes", chapters 17-27, plus an atlas page. Pulled: research/kernels/santa-2026-inside-the-elf-s-calculator.n1121 (kernel output log empty).

## New numbers
- 850 of 1,000 scored puzzles have 28-32 targets. Starts: 4 values 246 puzzles, 3 -> 236, 2 -> 226.
- Practice families: shared 51, mixed 48, independent 45, multiplicative 40, tiny 16; tiers hard 170 / medium 14 / easy 16 (all tiny = easy).
- Multiplicative: median share of adjacent target gaps < 1e6 is 50%; independent 0%.
- Four measured signals on scored: close adjacent pair 683 puzzles; division required 174; max target >= 55 bits 250; max target >= 90% of limit 174. 167 puzzles have none, 11 have all four.
- Sample submission = exactly bit_length(x) + bit_count(x) - 1 per target + 1 division per puzzle (1,000/1,000 match): 981,641 doublings, 480,840 +1, 26,898 resets.
- Spearman with sample length: max target bits +0.83, close pairs -0.68, #starts +0.02 (properties of the sample, not of the optimum).
- 16.6% of sample instructions recompute an earlier value; 83.7% of those were evicted earlier although >= 38 registers were free.
- 32 exact optima of tiny puzzles fit in <= 5 registers.

## Figures
Many matplotlib charts about the SAMPLE program (not rendered via CLI). None about strong programs.

## Reusable
- Nothing for the frontier. Family/signal counts can label puzzles for budget routing.

## Already tried by us?
- N/A (no optimisation). Confirms nothing new for the 130k gap.
