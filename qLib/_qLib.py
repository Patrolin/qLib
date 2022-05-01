from .math import *

# bitwise (|, &, copysign)

def isqrt(x: float) -> None:
    pass

# floor, round, ceil, abs, trunc, modf

# frexp, ldexp, isfinite, isinf, isnan

# (cos, sin, tan) * ('', 'a-', '-h')

# exp, expm1, log1p

def qerp(x, x1, x2, x3, y1, y2, y3):
    return ((x - x2) * (x - x3) * (x2 - x3) * y1 - (x - x1) * (x - x3) * (x1 - x3) * y2 + (x - x1) * (x - x2) *
            (x1 - x2) * y3) / ((x1 - x2) * (x1 - x3) * (x2 - x3))

# Complex, # https://mathworld.wolfram.com/ComplexExponentiation.html

# Vector, Matrix

# gcd, erf, erfc

# gcd(a/b, c/d) = gcd(a, c) / lcm(b, d)

# https://en.wikipedia.org/wiki/Category:Numerical_integration_(quadrature)
#     [-1, 1] https://en.wikipedia.org/wiki/Gauss–Legendre_quadrature
#    [0, inf) https://en.wikipedia.org/wiki/Gauss–Laguerre_quadrature
# (-inf, inf) https://en.wikipedia.org/wiki/Gauss–Hermite_quadrature
#      (a, b) https://en.wikipedia.org/wiki/Newton–Cotes_formulas
#     (-1, 1) https://en.wikipedia.org/wiki/Tanh-sinh_quadrature
#     (-1, 1) https://en.wikipedia.org/wiki/Gauss–Jacobi_quadrature
#     (-1, 1) https://en.wikipedia.org/wiki/Chebyshev–Gauss_quadrature
