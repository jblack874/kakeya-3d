"""Monte Carlo check with the same logic as the AlphaEvolve notebook scorer (needs numpy).
Samples points in the box [0,2.5]^2 x [0,1] and tests each against every tube. Run: python3 check_montecarlo.py [n]"""
import json, os, sys
import numpy as np
n = int(sys.argv[1]) if len(sys.argv) > 1 else 16
here = os.path.dirname(os.path.abspath(__file__))
p = json.load(open(os.path.join(here, 'positions.json')))[str(n)]; X = np.array(p['X_RAND']); Y = np.array(p['Y_RAND'])
exact = json.load(open(os.path.join(here, 'certificate.json')))['results'][str(n)]['score_float']
I = np.repeat(np.arange(n), n) / n; J = np.tile(np.arange(n), n) / n; s = 1.0 / n
rng = np.random.default_rng(7); P = 4_000_000; ch = max(1000, int(3e7 // (n * n))); hits = 0
for k in range(0, P, ch):
    m = min(ch, P - k); a = rng.random(m) * 2.5; b = rng.random(m) * 2.5; c = rng.random(m)
    lx = X[None, :] + c[:, None] * I[None, :]; ly = Y[None, :] + c[:, None] * J[None, :]
    hits += ((lx <= a[:, None]) & (a[:, None] <= lx + s) & (ly <= b[:, None]) & (b[:, None] <= ly + s)).any(1).sum()
q = hits / P
print('n=%d Monte Carlo score %.6f +- %.6f   exact score %.6f' % (n, q, (q * (1 - q) / P) ** 0.5, exact))
