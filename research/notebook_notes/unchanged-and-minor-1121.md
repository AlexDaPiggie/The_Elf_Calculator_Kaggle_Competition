# Top-voted / hottest notebooks re-pulled 11-21 with no or minor change
Each was pulled again (folders *.n1121 or base name) and diffed against the copy read for SYNTHESIS.md.

| notebook | change since last read | note file |
|---|---|---|
| konbu17/santa-2026-wider-dictionary-portfolio-163k | identical text | konbu17-wider-dictionary.md |
| romanrozen/santa-2026-icefire-strong-start | identical text | icefire.md |
| ozertuu/santa-2026-starter-notebook | identical (replay only) | ozertuu-starter.md |
| tonylica/elf-calculator-with-register-reuse | identical | merge-and-baseline-notebooks.md |
| atakanaldemir/santa-2026-joint-recipes-for-large-puzzles | identical (packed programs); goodpjw now runs its multiplier-frontier and interface-closure optimizers unchanged | atakan-joint-recipes.md |
| sacuscreed/public-merge | input list replaced by a glob over all attached notebooks | merge-and-baseline-notebooks.md |
| asteriospanoras/santa-2026-best-public-score-dataset-fails | score text 135,761 -> 134,185 only | asterios-gift-per-run.md |
| bikrambasnet1/santa-2026-arithmetic-graph-rewrites | v16: 134,119 (-11 over 10 puzzles vs v15 134,130): IceFire merge + CPU and CUDA graph rewrites; internal-cut pass (rebuild a shared intermediate, reuse its downstream); jointly rebuilding GROUPS OF THREE targets shortened scored_0269, 0690, 0729 by 1 each | bikram-graph-rewrites.md |

Takeaway: the most-voted list is stable and mostly historical; the new information sits in the hot list (royalacecat, goodpjw, kindasomethin, prvsiyan, rudolph) and in Pardheev's notebook outside both lists.
Figures: kaggle kernels output now returns only the log and csv files for these kernels (no __results__ PNGs); the pulled .ipynb files have no outputs, so no new figures could be extracted.
