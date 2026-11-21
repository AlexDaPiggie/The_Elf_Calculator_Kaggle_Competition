# evgendvorkin/santa-2026-inside-the-elf-s-calculator (32 votes)
Author: Evgeny Dvorkin. No score: EDA + exact-search lab on tiny puzzles, 16 chapters, reading list (Brauer 1939, Yao 1976, Bos-Coster 1989, Bergeron-Berstel-Brlek 1994, Clift 2011, Moody-Tall 2019, Sethi register allocation). Pulled: research/kernels/santa-2026-inside-the-elf-s-calculator. Kernel log (stdout numbers) in scratchpad only.

## Key numbers
- 1,000 scored puzzles, 26,902 targets (26,898 not in starts); median 30 targets, 3 starts; median largest target 47 bits, max 60.
- 4,683 adjacent target pairs within 1e6 (683 puzzles); relative 1e-6 closeness only 241 puzzles; only 22 pairs differ by a start value; 26 pairs t_j = t_i + s, 2 pairs t_j = t_i * s.
- Near-gap medians by family: independent 0, mixed 1, shared 4, multiplicative 13.5; for >= 28 targets: 0%, 3.6%, 12%, 49%.
- 174 scored puzzles: largest target >= 90% of value_limit (no overshoot room).
- 174 scored puzzles (and 46 practice): gcd of starts g > 1 and some target not divisible by g -> division provably required; 2,789 targets outside the divisibility class.
- practice lower_bound = |T \ S| exactly. Tiny puzzles: 32 exact optima, independent routes 165 vs shared 107 (-58); bound tight in only 10/32.
- Max reserved slots for starts+targets 38, so 10+ registers always free for helpers.
- Sample submission: 1,462,481 adds, 26,898 1x1 multiplies (resets), 1,000 divisions, 0 subtractions.

## Figures
Rendered output not pulled (many decorative charts). Key numbers above come from the kernel log.

## Reusable for us
- Divisibility check: in 174 puzzles a division is mandatory; seed helpers (start / g) early.
- Headroom flag (174 puzzles): overshoot-and-subtract recipes invalid near the limit.

## Failed
N/A (no optimisation).

## Already in our log?
- Family/targets-from-targets stats match our rejected hypotheses (targets rarely 1-2 ops from other targets). No action.
