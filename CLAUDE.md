# The Elf Calculator (Kaggle)

@../_kaggle_shared/rules.md

## This competition
- Existing notes: STRATEGY.md and EXPERIMENTS.md (this is the experiment log). Read them first.
- Fill in when known: competition URL, metric, agreed CV scheme, per-run cost limit.
- To audit work already done here, follow ../_kaggle_shared/prompts/kaggle-audit-existing.md.

## Submission rules override (this competition only, set by user 2026-11-18)
- Replaces "Submission rules (hands-off)" in the shared rules.
- Up to 100 submissions per day. Submit any time it seems useful: no CV-margin gate, no skeptic review gate, no one-line justification needed.
- Still required: local validity check (exact local score, valid programs, same IDs, no NaN) so a bad file does not get rejected.
- Still log each submission in SUBMISSIONS.md and EXPERIMENTS.md (change, score, trend). Update STATE.md.
- Work autonomously: keep the experiment loop running, do not stop to ask. Stop only on "stop"/"handoff" or a usage limit.

## Research routine (user suggestion, 2026-11-20)
- Every research pass must include the top public notebooks by leaderboard score (and the most-voted ones). Read each carefully: markdown, code, outputs, and the figures (extract embedded PNGs from the .ipynb and view them). Write notes per notebook in research/notebook_notes/<name>.md (insights, numbers, figures, code ideas, what we can reuse) plus a synthesis. Do this for new frontier-moving notebooks too.
- Executing third-party code needs a code scan first (no network, file deletion, exec calls) and is only done on our own files.