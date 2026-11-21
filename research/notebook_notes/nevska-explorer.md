# nevska/santa-2026-explorer (new, #10 hottest, 1 vote)
Author: Nevska. Output = baseline submission 1,276,696 instructions (valid). Tool notebook: an in-browser "workshop" to replay, inspect and hand-edit programs, plus verifier and baseline solver. Code lives in dataset santa-2026-explorer-files (elf_tools.py, santa_explorer.py; not downloaded). Pulled: research/kernels/santa-2026-explorer

## Method
- E.verify (strict replay), E.solve_baseline / E.solve_naive (simple constructions), X.classifier_check: simple rules recover practice design_tier exactly (200/200) and family on 136/200 (independent and tiny exact; a cross-validated tree ~69% on the other three).
- Scored labels from its classifier: multiplicative 307, independent 242, mixed 240, shared 195, tiny 16; tiers hard 850, medium 134, easy 16.

## Insights
- Only the family estimate is useful: ~31% multiplicative, ~24% independent among scored puzzles (68% accuracy on mixed/shared/multiplicative).

## Figures
HTML widget only.

## Reusable
- Family labels for budget routing (cheap; we can build our own from practice labels).

## Failed / already tried
- Nothing to run. Not relevant to the frontier.
