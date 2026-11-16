# Issue text for google-deepmind/alphaevolve_repository_of_problems

## Title

3D Kakeya (Problem 6.10): lower union volumes at n = 8, 16, 32, 64 (5.8% to 56.6% below the notebook values)

## Body

Sharing improved constructions for the 3D Kakeya problem (Problem 6.10), scored as in `experiments/kakeya_needle_3d/kakeya_needle_3d.ipynb`.

| n | Notebook `union_volume_n` | New score (exact volume / 6.25) | Lower by | New volume |
| --- | --- | --- | --- | --- |
| 8 | 0.021198256 | 0.019967115 | 5.81% | 0.124794467 |
| 16 | 0.015686817 | 0.012843130 | 18.13% | 0.080269564 |
| 32 | 0.014813417 | 0.009008068 | 39.19% | 0.056300425 |
| 64 | 0.014487586 | 0.006284760 | 56.62% | 0.039279749 |

I read `get_score` as the Monte Carlo hit fraction in the box [0, 2.5]^2 x [0, 1], so volume = 6.25 x score. Please correct me if that is wrong. As a check on that reading, an exact evaluator applied to your n = 8 and n = 16 positions gives scores 0.021198144 and 0.015687239, against your stated 0.021198256 and 0.015686817.

**Files:** https://github.com/jblack874/kakeya-3d

**How to check**

- Notebook scorer: `positions.json` holds `X_RAND` and `Y_RAND` for each n, in the notebook's order, ready for `get_score`. All positions lie in [0, 1].
- Exact: `python3 verify.py` (standard library only) recomputes every volume as a fraction.
- Sampling: `python3 check_montecarlo.py 16` follows the notebook scorer's logic with numpy.

**Method:** your n = 8 and n = 16 constructions are products (tube (i, j) uses x_i and y_j). For a product, the union at height c is (union of x-intervals) x (union of y-intervals), so the volume is the integral of Lx(c) Ly(c), which is piecewise quadratic and can be computed exactly. I optimized the 2n parameters against that exact objective: subgradient descent with restarts, then a smoothed descent with an annealed soft-min. Starts were your 3D positions and your 2D parallelogram constructions. About 15 minutes on 2 cores. Positions were rounded to multiples of 2^-40.

**Caveats**

- The gain comes from optimizing an exact objective instead of a sampled one, not from a new idea. All four constructions are products.
- The n = 32 and n = 64 constructions in the notebook are commented out, so I compared against their stated scores.
- n = 64 was still improving slowly when I stopped.
- Found with an AI assistant (Claude) and not reviewed by a mathematician. I did not find a later 3D value to compare against; if one exists, please point me to it.
