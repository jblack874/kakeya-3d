# 3D Kakeya problem (AlphaEvolve Problem 6.10): lower union volumes at n = 8, 16, 32, 64

Improved constructions for Problem 6.10 of Georgiev, Gomez-Serrano, Tao and Wagner, "Mathematical exploration and discovery at scale" (arXiv 2511.02864), scored as in the AlphaEvolve notebook `experiments/kakeya_needle_3d/kakeya_needle_3d.ipynb`.

## The problem

Fix n. Tube (i, j), for i, j = 0..n-1, has at height c in [0, 1] the square cross-section
[x + c i/n, x + c i/n + 1/n] x [y + c j/n, y + c j/n + 1/n]. Choose the n^2 positions (x, y) to minimise the volume of the union. The notebook's score is a Monte Carlo hit fraction in the box [0, 2.5]^2 x [0, 1], which equals volume / 6.25.

## Result (union volume; lower is better)

| n | AlphaEvolve notebook | This repository | Lower by |
| --- | --- | --- | --- |
| 8 | 0.132488398 | 0.124794467 | 5.81% |
| 16 | 0.098045244 | 0.080269564 | 18.13% |
| 32 | 0.092583854 | 0.056300425 | 39.19% |
| 64 | 0.090547412 | 0.039279736 | 56.62% |

AlphaEvolve values: for n = 8 and 16, the exact volume of the notebook's positions (their stated Monte Carlo scores, 0.021198256 and 0.015686817, agree with the exact scores 0.021198144 and 0.015687239 within sampling noise). For n = 32 and 64, the notebook's stated score times 6.25; those two constructions are commented out in the notebook.

## Files

| File | What it is |
| --- | --- |
| `certificate.json` | For each n: positions as integers over 2^40, the exact volume as a fraction, and the AlphaEvolve values used as the bar |
| `positions.json` | The same positions as `X_RAND`, `Y_RAND` float arrays in the notebook's order |
| `verify.py` | Exact check of every volume in rational arithmetic. Python standard library only |
| `check_montecarlo.py` | Monte Carlo check with the notebook scorer's logic. Needs numpy |
| `ISSUE.md` | Text of the claim as posted |

## How to check

```
python3 verify.py               # exact, about a minute
python3 check_montecarlo.py 16  # sampling check, n = 8, 16 or 32
```

## Method

The notebook's n = 8 and n = 16 constructions are products: tube (i, j) uses x_i and y_j. For a product, the union at height c is (union of n x-intervals) x (union of n y-intervals), so volume = integral of Lx(c) Ly(c) dc with Lx, Ly piecewise linear. Two optimizers on that objective in the 2n variables, started from the notebook's 3D positions (n = 8, 16) and from the notebook's 2D parallelogram constructions (n = 8 to 64): subgradient descent with random restarts, then a smoothed descent (min replaced by a soft-min whose temperature is annealed to 0, L-BFGS at each temperature) restarted from the best point with random kicks. About 15 minutes on 2 cores in total. Positions were rounded to multiples of 2^-40 so each volume is an exact rational.

## Status and caveats

- Unreviewed. Found with an AI assistant (Claude, Anthropic) on 2026-11-16.
- The bar was soft. The notebook values sit close to a simple arrangement where all tubes pass through one point at mid-height (0.134, 0.106, 0.094, 0.089 for n = 8, 16, 32, 64). At n = 32 and 64, products of simpler 2D constructions already beat the notebook values.
- All four constructions here are products. Freeing every tube at n = 8 found no further gain in a one-minute run; that is not evidence the product form is optimal.
- n = 8, 16 and 32 stopped improving under repeated restarts of the smoothed optimizer. n = 64 was still improving slowly (0.3% in its last five minutes).
- No later 3D value was found in a search on 2026-11-16.

## Sources

- AlphaEvolve repository of problems (Google DeepMind): https://github.com/google-deepmind/alphaevolve_repository_of_problems. Problem definition, scoring logic and the starting constructions come from its 3D and 2D Kakeya notebooks.
- Georgiev, Gomez-Serrano, Tao, Wagner, "Mathematical exploration and discovery at scale": https://arxiv.org/abs/2511.02864

## Update, 2026-11-24: n = 64 lowered to 0.03927973596640655

The n = 64 product construction was polished further: exact volume 8366110934600473457174170689853913361212944784150439434719 / 212987962591079374713220960336766622416732359118039285760000 = 0.03927973596640655, which is 1.2632e-8 below the value first posted (0.03927974859806375). It is still a product construction, and the change is a local refinement, not a new idea.

Method: local descent on the exact objective, started from the previous n = 64 certificate. The landscape is piecewise smooth with creases, so plain gradient descent stalls. The gains came from three kinds of moves, each accepted only when the exact volume fell. First, coordinate-wise compass (pattern) search with steps between 1e-7 and 1e-5. Second, line searches along exit directions measured from the current best, re-cast as the best moved. Third, small random nudges each followed by a 2-iteration L-BFGS polish. Every accepted point was checked by two independent exact evaluators.

Check it:

- `python3 verify.py` recomputes every n from `certificate.json`.
- `python3 checks/exactA.py checks/n64_positions_int.json` (verify.py's method) and `python3 checks/exactB.py checks/n64_positions_int.json` (an independent implementation) each print the same fraction. Their outputs are in `checks/n64_exactA.out` and `checks/n64_exactB.out`.
