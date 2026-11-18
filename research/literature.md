# Literature review - Santa 2026 "The Elf Calculator"

Scope: web research for multi-target straight-line programs (SLPs) over positive integers with + - * /,
48 registers, score = total instruction count. Items marked [recall] are from background knowledge,
not confirmed by a page fetched for this review.

---

## 1. Addition chains, addition sequences, vectorial chains, addition-subtraction chains

### Definitions and hardness
- Addition chain: 1 = a0 < a1 < ... < ar = n, each ai = aj + ak. Addition sequence: chain that contains
  every target in a set. Vectorial chain: build vectors in Z^k. (Gordon survey, https://dmgordon.org/papers/jalg.pdf)
- Downey, Leong, Sethi 1981, "Computing Sequences with Addition Chains", SIAM J. Comput. 10(3):638-646:
  the addition-SEQUENCE problem (many targets) is NP-complete. Single-target hardness is still open.
  (https://en.wikipedia.org/wiki/Addition_chain, https://en.wikipedia.org/wiki/Addition-subtraction_chain)
- Our problem is a harder superset (adds * and /, a register cap, several start values), so do not
  look for exact optima except on tiny instances.
- Duality (Olivos 1981) [recall]: vectorial chain for (n1..nk) <-> addition sequence for {n1..nk},
  with length l(seq) = l(vec) + k - 1. Multi-exponent tricks (Straus/Shamir, Pippenger) work by
  sharing a base set across targets. Gordon survey section 4 covers both.

### Bos-Coster heuristics (best practical method for long addition sequences)
- Bos, Coster, "Addition Chain Heuristics", CRYPTO '89. Coster's CWI report CS-R9024 lists 12 algorithms
  for chains, sequences and vector chains with worked examples: https://ir.cwi.nl/pub/5726/5726D.pdf
- It works top-down on a target multiset, always reducing the largest element f:
  - Approximation: find a, b in the set with a + b close to f; replace f by f - (a+b) (+ a, b).
  - Division: if f ~= c*g for small c, replace f by g (plus a chain for c).
  - Halving: if f >> next largest, push f/2^k (doublings).
  - Delta-largest (Lucas-like): add f - f2 (difference of the two largest).
  Repeat until the set is small, then finish exactly.
- mmcloughlin/addchain (Go) has a clean variant: approximation, then halving, then delta-largest, plus
  continued fractions, dictionary/sliding-window and "runs" methods, and an `opt` pass that drops
  redundant steps: https://github.com/mmcloughlin/addchain . Rust port: https://github.com/kwantam/addchain
- Our "shared" family (clusters like 10973744, 10974352, 10974650) is exactly what delta-largest and
  approximation are built for: compute one cluster centre, then each neighbour costs 1 op once the
  small difference (608, 298, ...) is in a register.

### Continued-fraction / division methods
- Bergeron, Berstel, Brlek, Duboc 1989 (J. Algorithms) "Addition chains using continued fractions":
  chain(n) = combine(chain(k), chain(n div k), chain(n mod k)), using strategies for picking k
  (binary, dichotomic, Fermat, sqrt, total). Tall-Sanghare ePrint 2013/466 extends this to
  addition-subtraction chains. (References listed in the addchain README.)
- With * available this becomes n = q*k + r, i.e. 2 instructions (mul, add/sub) plus the costs of q, k, r.
  This is the main building block for large independent targets (see section 2).

### Exact / near-exact methods
- Exact search by branch-and-bound / BFS for small addition sequences (multicore exact algorithm:
  https://www.academia.edu/86191300/A_Multicore_Exact_Algorithm_for_Addition_Sequence).
- ILP model of addition sequences (arXiv 2306.15002): https://arxiv.org/pdf/2306.15002
- Simulated annealing for addition sequences gives shorter results than older heuristics
  (AIMS Math 2024): https://aimspress.com/aimspress-data/math/2024/5/PDF/math-09-05-540.pdf
- Takeaway: exact methods only handle tiny sets. SA/LNS on top of a Bos-Coster-style constructor is
  the proven path.

### Addition-subtraction chains
- Subtraction helps only a little for chains (NAF, signed windows). Optimal hardness unknown.
  https://en.wikipedia.org/wiki/Addition-subtraction_chain . Otto's thesis (Brauer add-sub chains) and
  Kunihiro-Yamamoto (IEICE 2000) do dictionary and window methods with signed digits.

---

## 2. SLPs over integers with + - * / (integer complexity)

- tau(n) = shortest SLP from 1 using + - *. Bounds: log2 log2 n + 1 <= tau(n) <= 2 log2 n.
  Most n have tau(n) much larger than polylog(log n). (https://mathworld.wolfram.com/ArithmeticComplexity.html,
  OEIS A173419)
- Shub-Smale tau conjecture links tau(n!) and root counts to P vs NP over C. It is theory only; it says
  explicit large-scale exact tau is hopeless. (Buergisser, "On defining integers and proving arithmetic
  circuit lower bounds", https://eccc.weizmann.ac.il/report/2006/113/download)
- "Subtraction makes computing integers faster" (Kayal et al., arXiv 1212.2549,
  https://ar5iv.arxiv.org/html/1212.2549):
  - For almost all n-bit z, tau(z) = Theta(n / log n), with or without subtraction.
  - Upper bound: block-concatenation (base 2^k Horner). Precompute digits 1..2^k, then ~2 ops per
    k-bit block: z = (...(d1*B + d2)*B + d3...). This is base-B Horner.
  - Lower bound by counting: SLPs of length L give at most 2^(3 L log L) numbers.
- Markstroem, small factorials and primorials (arXiv 1306.3091): exact tau by exhaustive search works
  only for tiny programs (about 10 steps). It is a useful model for a depth-limited exact solver.
- Countdown numbers game solvers (https://incoherency.co.uk/countdown/pages/how-numbers-solver-works,
  Alliot "The (final) countdown" arXiv 1502.05450, https://arxiv.org/pdf/1502.05450.pdf):
  - Recursive combine over subsets, memoized by multiset of values, with canonical ordering (a >= b
    for commutative ops, skip x*1, x/1, results equal to inputs).
  - The BFS over set partitions is ~20x faster than naive DFS.
  - Same pruning rules apply to our depth-limited search.

### Constructive tricks for one big target t, given a pool P of available values
- Horner / mixed radix with pool elements as bases: t = q*b + r, where b is in the pool (or cheap) and
  q, r are recursed. Each mul+add removes ~log2(b) bits, so large pool values are worth more.
- "Approximate by product then correct": search a, b in pool (or 1-op-derived set) with
  |t - a*b| small; residual r = t - a*b is a new, much smaller target. Same idea as the Bos-Coster
  approximation step, with * instead of +.
- Meet-in-the-middle: build hash sets S1 (values from <= 1 op over pool, ~2|P|^2) and S2 (<= 2 ops,
  ~10^6-10^7). Test t = x op y for x in S_i, y in S_j by hashing t - x, t + x, t / x (when it divides),
  x / t. This gives exact optimal depth for small depths.
- Division is useful backwards: if t has a large factor in common with a pool value g, then
  t = (t/g)*g, which reduces to target t/g. Use gcd(t, pool values) and gcd between targets.
- Multiplicative family: factor the targets (trial division / Pollard rho; 1e18 is easy). Build shared
  prime powers / common factors once, then each target is a short product chain. This is a
  vectorial addition chain on exponent vectors (Straus / Pippenger style sharing).
- Lattice / CF idea: for two pool values a, b, the continued fraction of t/a or t/(a*b) gives good
  q with small t - q*a. LLL finds small (x1..xm) with sum xi*pi ~= t when m is small [recall].
  Probably overkill versus hashing.

---

## 3. Counting bounds (back-of-envelope, own derivation)

- One instruction on a pool of P live values gives at most ~2P^2 distinct results (+ and * on
  unordered pairs ~P^2/2 each, - and / on valid ordered pairs ~P^2/2 each, many / invalid).
  - P = 40: ~3200 (11.6 bits). P = 48 (all registers): ~4600 (12.2 bits).
- k new instructions reach at most ~ prod_{i<k} 2(P+i)^2 / k! values (k! for reordering independent
  steps). Bits reached, for P = 40:
  - k=1: 11.6 | k=2: 22.3 | k=3: 32.5 | k=4: 42.4 | k=5: 52 | k=6: 61.6
- So a target with no structure needs at least about:
  - 30-bit: 3 ops | 40-bit: 4 ops | 50-bit: 5 ops | 60-bit (~1e18): 6 ops
  - Early in a puzzle (P = 1-8 start values) the pool is small: about 7-8 bits per op for P=8, so the
    first big target costs more (~8 ops for 60 bits).
- This is an upper bound on reach (values collide), so real optima are slightly higher.
- Implication: leaderboard ~5.5 ops/target (149k / 26.9k) is already close to the counting limit for
  independent ~50-60-bit targets. Big gains must come from:
  (a) shared/multiplicative/mixed families where structure gives 1-2 ops per target,
  (b) tiny family (exact search, possibly provably optimal),
  (c) small search improvements on independent targets (~0.2-0.5 ops/target).
- Check per-family bits: compute log2(target) histograms. Targets well below value_limit are cheaper.
- Lower bound per puzzle >= number of targets not already in the start registers (one op each), plus
  counting bounds on the hardest targets. Use it to rank which puzzles have slack.

---

## 4. Register allocation under 48 registers

- Optimal register allocation for straight-line code is NP-complete (Sethi 1975, with or without
  recomputation; Bruno-Sethi JACM 1976). Trees are optimal in linear time (Sethi-Ullman / Nakata).
  (Checkmate rematerialization paper: https://arxiv.org/pdf/1910.02653)
- Belady MIN (evict the value whose next use is farthest) is a strong heuristic for long straight-line
  code (Guo, Garzaran, Padua, LCPC 2003:
  https://parasollab.web.illinois.edu/events/lcpc03/informal-proceedings/Papers/35.pdf).
- Rematerialization: recompute a cheap value instead of keeping it, at the cost of 1+ instructions.
  Here that adds to the score, so avoid it unless registers are truly short.
- Practical: ~30 targets + 8 starts < 48, so the cap rarely binds if dead values are freed. Plan the
  program as a DAG, then assign registers by linear scan with Belady eviction. Only when more than
  48 values are live, either reorder (pebbling) or add a rematerialization (+1 op). Targets only need
  to appear once, so a target with no later use frees its register right away.

---

## 5. Public discussion of santa-2026, and lessons from past Santa competitions

### Santa 2026 itself
- Searched Kaggle, GitHub, Reddit, X/Twitter, and blogs (Nov 2026). Nothing public outside Kaggle
  (searches for "Elf Calculator", "santa-2026"). The Kaggle page did not render through the fetcher.
  Re-check Kaggle discussions and Code tab often. Top public notebooks usually leak the current
  meta (e.g. a Bos-Coster/MITM baseline).

### Past Santa competitions - how top teams worked
- 2019 Workshop Tour Scheduling: top teams reached the proven optimum with MIP / LP min-cost flow
  (Gurobi, CPLEX). One participant got the optimum in ~37 h of LP min-cost flow and a 3% gap in ~5 h
  (https://www.godberit.de/2020/01/15/Kaggle-Christmas-Challenge-2019.html). Many ties at the optimum,
  so the winner came down to time of reaching it [recall].
- 2020 Candy Cane Contest: bandit agents (simulation), not relevant.
- 2021 Merry Movie Montage: permutation-cover strings. Top teams used TSP reductions + LKH, ILP for
  bounds, and C++ local search [recall]. LKH use for superpermutations: https://github.com/bwmetz/superperm
- 2022 Christmas Card Conundrum: TSP-like path on an image with arm configurations. LKH-3 +
  custom local search (https://github.com/sfujiwara/kaggle-santa-2022, https://zenn.dev/fixstars/articles/kaggle-santa-2022).
- 2023 Polytope Permutation Puzzle: winner 53,770 moves vs ~1.16M for the best public no-solver notebook
  (https://arxiv.org/pdf/2512.03549). Top teams used per-puzzle-type solvers (cube solvers, beam search,
  commutator/macro libraries, IDA* for small puzzles), many CPU-days, and kept the best per puzzle [recall].
- 2024 Perplexity Permutation Puzzle: SA / ILS over word orders with LLM (Gemma) scoring on GPUs.
  The winners mostly won on compute and good move sets (swap, shift, block moves)
  (https://awesome.ecosyste.ms/projects/github.com%2Fmbayraktar12%2Fsanta-2024) [recall for winner details].
- 2025 Christmas Tree Packing: SA + physics-style compaction in C++, long runs, per-N best-of merges [recall].
- Common patterns among top-10 teams:
  - Score is additive per instance, so optimize each puzzle on its own, run in parallel, and keep a
    per-puzzle best file. Merge candidates from all methods and all teammates.
  - Fast C++ (or Rust) core, Python for orchestration. Run 24/7 on many cores for weeks.
  - A family of specialized solvers per instance type, not one general method.
  - Exact solvers or proofs for small instances. Lower bounds show where to stop.
  - Late gains come from LNS (destroy part of a solution, rebuild optimally) on the worst-gap instances.
  - Team merging near the deadline adds a lot through per-instance best-of.

---

## 6. Recommendations by family

General engine (all families):
- Represent a solution as a DAG of operations, then add register assignment (Belady) at the end.
- Constructor: greedy target-by-target with a depth-limited exact search over the current pool
  (Countdown-style MITM, depths 1-3 exact, 4-5 via hashing), falling back to Horner / q*b+r
  decomposition. Targets join the pool once built, so sorted order and "nearest target first" matter.
- Improver: LNS. Remove the ops of 1-4 targets plus their exclusive helpers, then re-insert with
  exact depth search over the remaining pool. Accept with SA on op count (ties broken by more
  intermediate value reuse).
- Post-pass: dead-op elimination, and the addchain `opt` idea of dropping helpers that have an
  alternative derivation.
- Target-order search: try many permutations (SA over order). Cheap targets first grow the pool.

Independent (random ~40-60-bit targets) - small headroom (~0.2-0.5 op/target):
- Per target, search t = a*b +/- c, t = (a +/- b)*c +/- d, t = a*b +/- c*d over the pool and over
  1-op-derived values, using hash lookups for the residual. This is "approximate by product, then
  correct".
- Pick helper values that serve several targets at once, e.g. a base B such that all targets have
  cheap B-adic digits, or a shared big multiplier: t_i = q_i*B + r_i with B shared.
- Make sure the first big target uses the small start pool well (bootstrap a few medium "base" values
  ~2^10-2^20 early, since they boost bits/op for all later targets).

Shared (clusters with small differences) - biggest structured gains:
- Bos-Coster at heart: build one value per cluster (or the cluster median), then the differences.
- Differences between neighbours are small (~hundreds). Build a small addition sequence over the set
  of distinct differences (exact search is cheap for values < 2^12), then each target costs 1 op.
- Look for differences shared across clusters, and differences of differences.
- Aim ~1-1.5 ops per non-centre target, plus 4-6 per cluster centre.

Multiplicative:
- Factor all targets. Find common factors / gcds and ratios t_i / t_j that are small rationals.
- Build each target as t_j = t_i * c or t_i * c / d (1-2 ops), where c, d are cheap.
- Exponent-vector view: shared prime powers via vectorial addition chain (Straus/Pippenger-style).
- Use division: if t_i | t_j or gcd is large, one op derives a target from another.

Mixed:
- Detect structure per target. Compute the cost of each target from every other target via
  +-*/ with a small constant (graph of pairwise links). Solve a Steiner-tree / minimum branching over
  "target derived from target or pool" (Edmonds arborescence as a quick bound), then LNS.

Tiny:
- Small values: run an exact iterative-deepening search (Countdown-style, memoized on sorted pool
  multiset). Likely provably optimal, and must not lose a single op here.

Priority (expected gain per effort):
1. Exact/MITM depth search over the pool, plus target-from-target links (helps all families).
2. Shared-family difference handling (an addition sequence over differences).
3. Multiplicative factor/gcd/ratio links.
4. LNS + SA wrapper with per-puzzle best file, running in C++ on all cores.
5. Register allocation only as a final feasibility pass (rarely binding).
