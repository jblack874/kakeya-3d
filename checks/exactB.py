# Checker B (independent): Lx, Ly as exact piecewise-linear functions sampled at each axis's own breakpoints
# (union length by merging Fraction intervals), merged grid, closed-form integral of a product of two linear functions.
import sys, json
from fractions import Fraction as F
d=json.load(open(sys.argv[1])); n=64; S=2**40
X=[F(v,S) for v in d['x_times_2^40']]; Y=[F(v,S) for v in d['y_times_2^40']]; w=F(1,n)
def union_len(starts):
    iv=sorted(starts); tot=F(0); cs,ce=iv[0],iv[0]+w
    for s in iv[1:]:
        if s>ce: tot+=ce-cs; cs,ce=s,s+w
        else: ce=max(ce,s+w)
    return tot+ce-cs
def L(Z,c): return union_len([Z[i]+c*i/n for i in range(n)])
def kinks(Z):
    ks={F(0),F(1)}
    for i in range(n):
        for j in range(n):
            if i==j: continue
            # start_i(c) - start_j(c) in {0, w}: (Z_i-Z_j) + c (i-j)/n = t
            for t in (F(0),w):
                c=(t-(Z[i]-Z[j]))*n/(i-j)
                if 0<c<1: ks.add(c)
    return ks
pts=sorted(kinks(X)|kinks(Y))
Lx={c:L(X,c) for c in pts}; Ly={c:L(Y,c) for c in pts}
vol=F(0)
for a,b in zip(pts,pts[1:]):
    h=b-a; p0,p1=Lx[a],Lx[b]; q0,q1=Ly[a],Ly[b]
    vol+=h*(2*p0*q0+p0*q1+p1*q0+2*p1*q1)/6   # exact integral of (linear)(linear)
print('B', vol.numerator, vol.denominator); print('B float', float(vol))
