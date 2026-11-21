# ozertuu/santa-2026-starter-notebook (32 votes, top 3 by score)
Author: Ertugrul Ozer. Output replays ~135,761-135,763 on 11-20 (one of the frontier banks). Notebook = replay of dataset ozertuu/santa-2026-verified-programs + any attached submission.csv. Pulled: research/kernels/santa-2026-starter-notebook.v3 (same text as .v2)

## Method (described, code not public in the notebook)
"Deep Cone Pollard-Rho & Joint Scaffold Optimizer" (opt_deep_cone.cpp, attached to dataset):
- Deep sub-DAG / cone re-synthesis.
- 64-bit Miller-Rabin + Brent Pollard-rho factorisation of T +- r for small r: find cofactor splits T = a*b +- r where a or b is cheap.
- Large D2 meet-in-the-middle: 2^21-2^22 flat hash index of 2-step values.
- Congruence backward beam search.
- Belady / register-pressure scheduling.
Asterios also credits him (with Atakan) for the joint scaffold exchange: cut a shared helper with all its consumers and re-price jointly.

## Key numbers
- 24 new per-puzzle bests in mizero's merge (11-19); goodpjw lists his outputs among the 1,000/1,000 frontier holders.

## Figures
None (2 cells).

## Reusable for us
- Factor-based split idea: for each expensive target, factor T +- r (|r| small) with Pollard-rho and check whether a factor is already in the pool or 1-2 ops away. Our solver uses quotient/residual reduction only from pool values, not factorisation of nearby integers.

## Failed
Not documented.

## Already in our log?
- Poller bug (charmap) caused his kernels to be missed until 11-19; fixed. Pollard-rho cofactors: not tried by us.
