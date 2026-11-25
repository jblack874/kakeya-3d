# Checker A: verify.py's exact method (integer sweep + per-piece Simpson), on a positions file of integers over 2^40.
import sys, json
from fractions import Fraction
src=open('verify.py').read().split('c = json.load')[0]; exec(src)
d=json.load(open(sys.argv[1])); X,Y=d['x_times_2^40'],d['y_times_2^40']; n=64
assert all(0<=v<=Q2 for v in X+Y)
v=exact_volume(X,Y,n); print('A', v.numerator, v.denominator); print('A float', float(v))
