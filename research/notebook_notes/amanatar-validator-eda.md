# amanatar/santa-2026-fast-validator-eda-sota-baseline (v12, #3 hottest)
Author: Aman Atar. Output 133,786 in the pulled run (merge of 17 attached csv files). In goodpjw's 132,950 merge this bank still holds the minimum on 567 puzzles (ties) and is strictly needed on 9. Pulled: research/kernels/santa-2026-fast-validator-eda-sota-baseline

## Method (plain words)
- Pure merge carrier: discovers every attached csv with id,program, validates, keeps the shortest per puzzle. No search.
- "EDA": a hand-made 5-family classifier (Fibonacci if starts == [1,2]; >1e14 and <=25 targets; >=32 targets; log10 limit >= 15; else) - not the organisers' families, not useful.
- Liveness heatmap of one program, opcode pie chart, table of algebraic identities (a*b + a*c = a*(b+c), difference of squares, ...).

## Insights with numbers
- None new. Note: its run_pure_python_dce function keeps every instruction (bug: it never drops anything), so its "DCE" claim is empty.
- Its validator uses regs = [0]*48 (reading an empty register gives 0, then rejected only if value <= 0): fine for scoring, not exact for edge cases.

## Figures
Plotly only (not rendered in CLI output). Figure 1 family scatter, Figure 2 register liveness heatmap, Figure 3 opcode share.

## Reusable code ideas
- None beyond what we have (merge + replay).

## What failed for them
- Not stated.

## Already tried by us?
- Poller merges its output. Nothing to run.
