"""Exact check, Python standard library only. Run: python3 verify.py   (about a minute)
For each n it recomputes the union volume as an exact fraction and compares it with the stored
value and with the AlphaEvolve notebook value."""
import json, os
from fractions import Fraction
Q2 = 1 << 40
def breaks(X, n):
    cs = set()
    for i in range(n):
        for j in range(n):
            if i == j: continue
            d = X[i] - X[j]
            if i < j:
                num = n * d; den = Q2 * (j - i)
                if 0 < num < den: cs.add(Fraction(num, den))
            num = Q2 - n * d; den = Q2 * (i - j)
            if den < 0: num, den = -num, -den
            if 0 < num < den: cs.add(Fraction(num, den))
    return cs
def length(X, n, c):
    P, Q = c.numerator, c.denominator
    U = sorted(X[i] * n * Q + i * P * Q2 for i in range(n)); w = Q * Q2; tot = w
    for k in range(1, n):
        g = U[k] - U[k - 1]; tot += g if g < w else w
    return Fraction(tot, n * Q * Q2)
def exact_volume(X, Y, n):
    pts = sorted({Fraction(0), Fraction(1)} | breaks(X, n) | breaks(Y, n))
    f = lambda c: length(X, n, c) * length(Y, n, c)
    vol = Fraction(0); a = pts[0]; fa = f(a)
    for b in pts[1:]:
        fb = f(b); vol += (b - a) * (fa + 4 * f((a + b) / 2) + fb) / 6; a, fa = b, fb
    return vol
c = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'certificate.json'))); ok = True
for n in (8, 16, 32, 64):
    r = c['results'][str(n)]; new = exact_volume(r['x_times_2^40'], r['y_times_2^40'], n)
    assert new == Fraction(int(r['volume_numerator']), int(r['volume_denominator'])), 'stored volume does not match'
    assert all(0 <= v <= Q2 for v in r['x_times_2^40'] + r['y_times_2^40']), 'positions outside [0,1]'
    if 'alphaevolve_exact' in r:
        b = r['alphaevolve_exact']; bar = exact_volume(b['x_times_2^40'], b['y_times_2^40'], n); kind = 'exact'
        assert bar == Fraction(int(b['volume_numerator']), int(b['volume_denominator']))
    else:
        bar = Fraction(r['alphaevolve_stated_score']) * Fraction(25, 4); kind = 'stated Monte Carlo score x 6.25'
    ok = ok and new < bar
    print('n=%-3d new %.12f   AlphaEvolve %.12f (%s)   %.2f%% lower' % (n, float(new), float(bar), kind, float((bar - new) / bar) * 100), flush=True)
print('PASS' if ok else 'FAIL')
