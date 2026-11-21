# asteriospanoras/santa-2026-best-public-score-a-gift-per-run (new) + update of santa-2026-best-public-score-dataset-fails
Author: Asterios Panoras. Gift notebook claims 132,949 = dataset base 132,950 + one gift (scored_0137 54 -> 53). Pulled: research/kernels/santa-2026-best-public-score-a-gift-per-run; dataset-fails latest pulled to research/kernels/santa-2026-best-public-score-dataset-fails.

## Method (plain words)
- "Advent calendar": each version opens one door = one shorter program for one puzzle, found by their local search on the public program, replayed under strict rules (their replay also rejects a - b <= 0 explicitly).
- Base = dataset santa-2026-elf-programs-and-experiments best_programs.csv (with source column).
- WRITE_SUBMISSION = False by default: the output tab has NO submission.csv, so pollers that merge outputs never see the gift.

## Key numbers
- scored_0137: 54 -> 53. Our best/best.csv still has 54 for scored_0137, so merging this one program gives -1 (best 132,948 -> 132,947). The full 53-instruction program is in cell 7 (CHANGE dict).
- dataset-fails notebook: only the score text changed (135,761 -> 134,185; best single public file then 134,187 E-Max AI); the 17 E-cards and figures are unchanged (see asterios-best-public-fails.md).

## Figures
None in the gift notebook. dataset-fails figures unchanged.

## Reusable
- Hand-merge gift programs from notebooks that do not write output files (poller blind spot). Same check for any notebook with WRITE_SUBMISSION-style flags.

## Failed
- Nothing new.

## Already tried by us?
- No: scored_0137 at 53 is not in our best. Our poller only reads output csv files.
