# alexchilton/rudolph-the-red-nosed-register-allocator (v3, 2026-11-20)
Author: alex chilton. Board 138,193 (merge of public + own, 11-19 16:30); own solver alone ~168.6k. Best negative-result table in the competition (18 measured ideas). Pulled: research/kernels/rudolph-the-red-nosed-register-allocator.v3

## Method (plain words)
Own C++ solver: backward reduction over a 2-step dictionary (small leaves first), farthest-next-use allocator, ruin and recreate accepted on compiled length. Analysis of the merge: hub structure, slack by target size.

## Key numbers
- 997/1000 shortest programs in every public merge come from ONE notebook lineage: all merges hold the same programs.
- Leader was ~5,300 below the merge on 11-18 and "about 8,000 below every public merge" later: a different construction, not a better merge (their claim).
- Slack (instructions above 1 per target) grows from ~38 per puzzle at 24-bit targets to ~167 at 56 bits; 300 puzzles hold half the slack.
- Hubs in 66 cracked puzzles (values >= 2^14, non-target, read 3+): T = q*h + r with h median 18 bits (p10 15, p90 20), q 23 bits (16/35), |r| 10 bits (3/14).
- Oracle: told the hubs of the best program, their solver cuts 16 cracked puzzles 2,900 -> 2,330 (-20%). Detectors (divisor near 3+ targets) pick wrong hubs: uncracked 4,718 -> 4,840.
- Merge anatomy: 12% of instructions before the first target; 27.6% make small constants < 2^16 at one instruction each.

## Figures (research/notebook_notes/rudolph/)
- __results___23_0.png: instr/target vs bits of largest target: two bands. Lower band ~3-4.5 flat (shared/multiplicative-like); upper band in vertical stacks at 30/40/50/60 bits (independent) reaching 5.5 / 6 / 7.5 / 8.8. Histogram multi-modal with peaks at 3.8, 5.8, 7.2, 8.7.
- __results___8_0.png: EDA by family (not inspected in detail).

## Failed (all measured, v3 adds last 3)
More leaves 72/88 (worse), small leaves to 2^24 (worse), ruin-recreate accepted by value count (worse; accept on compiled length), product link v = f*Y +- c (noise), residual-divisible-by-start bonus (worse), harder beam pruning (=), polish public merge with R&R 141,432 -> 141,431, pair ruin (=), prefix re-solve 30-85% (-3), MITM A*B+-C (-2), two-hub Euclid link (0), recombine targets across 76 files (cycles, 0), hub detectors as forced targets (worse), LLL (not built), DCE (0 dead), 2x2 target grid bases T1*T4=T2*T3 (8,655 quadruples in 151 puzzles; 55 puzzles 10,094 -> 9,973 own but merge 8,057), small-constant toolkit lock (6,173 -> 6,353-7,129 worse), joint recipe of two consecutive targets (32 of 507 pairs shorter on paper, 0 kept in full program: replaced instructions also feed 1-5 later values).

## Reusable for us
- Hub stats (h ~18 bits, r ~10 bits) to size any hub scan; oracle test design (give solver the true hubs) to bound the value of hub recovery.

## Already in our log?
- Most nulls match ours (suffix re-solve, MITM, toolkit E1, -S slack). Hub recovery = our sota idea 3 (not run; Rudolph's detector failure is a warning). 2x2 grid bases: new but already shown not to beat merge.
