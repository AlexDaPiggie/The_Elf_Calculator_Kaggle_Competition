# lightningv08/santa-2026-shared-intermediates-cuda-cofactors (17 votes)
Author: Vladislav Lavrentev ("Luna"). Old era: composite 141,399 -> 141,380 (-19 own arithmetic pass) -> -11 more by late merge. Pulled: research/kernels/santa-2026-shared-intermediates-cuda-cofactors

## Method (plain words)
- Per puzzle a "plan" (cut, hub, method, coefficient) chosen in 50 batches by an LLM ("gpt-6-luna" in the JSON), then verified; plan rationales hashed.
- CPU pass guided_exchanges(puzzle, program, root, hub, coefficient, method): local graph rewrite in the neighbourhood (radius 2) of a selected cut and a shared hub (top-4 most-used values).
- GPU CofactorSearch (cupy RawModule): common one-step and two-step dictionaries ("atoms"), per-cut leaf availability; branch_cuts(...) jobs with budget >= 3; NearestCofactors.lookup_nearest finds T ~ term op term with nearest-value search over the sorted 1-step dict + strided 2-step dict; optimize_cofactors accepts edits only if re-schedule shortens.
- Targets for GPU: CPU winners + up to 120 cases prioritised by source disagreement, earlier savings, size.

## Key numbers
- -19 instr over 1,000 puzzles from the arithmetic pass (141k era); portfolio merge part was 103.

## Figures
None extracted.

## Reusable for us
- Idea: target the LNS budget at puzzles where sources DISAGREE (several distinct same-length programs) - diversity predicts improvability.
- Nearest-term search over sorted dictionaries (same as goodpjw near-miss).

## Failed
Not documented; gains were small even in the 141k era.

## Already in our log?
- No. Low priority (GPU, small gains).
