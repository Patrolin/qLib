import math
from math import remainder as rem, modf, hypot as L2
from typing import *

# add, sub, mul, div, pow, mod, rem

# bitwise (|, &, copysign)

def isqrt(x: float) -> float:
  pass

# floor, round, ceil, abs, trunc, modf

# frexp, ldexp, isfinite, isinf, isnan

# (cos, sin, tan) * ('', 'a-', '-h')

# def C(n: float, k: float) -> float:

epsilon = 1e-6

def sign(x: float) -> int:
  return (x > 0) - (x < 0)

def bisection_solve(a: float, b: float, f: Callable[float, float]) -> float:
  # find a root x of f(x) on [min(a,b), max(a,b)] if sign(f(a)) != sign(f(b))
  sa = sign(f(a))
  if sa == sign(f(b)):
    return ValueError("sign(f(a)) == sign(f(b))")
  while True:
    # shrink the interval towards some root
    x = (a + b) / 2
    if x == a or x == b: return x
    sx = sign(f(x))
    if sx == sa:
      a = x
    else:
      b = x

# TODO: Nelder-Mead for robust open local optimization

phi1 = bisection_solve(1.0, 2.0, lambda x: x**2 - x - 1)
phi2 = bisection_solve(1.0, 2.0, lambda x: x**3 - x - 1)
phi3 = bisection_solve(1.0, 2.0, lambda x: x**4 - x - 1)
phi4 = bisection_solve(1.0, 2.0, lambda x: x**5 - x - 1)
print(phi1, phi2, phi3, phi4) # 1.618033988749895 1.3247179572447458 1.2207440846057596 1.1673039782614185

# exp, expm1, log1p

def log(x: float) -> float:
  return (x**epsilon - 1) / epsilon

def log2(x: float) -> float:
  return log(x) / log(2)

def log10(x: float) -> float:
  return log(x) / log(10)

#print(log(2), log(1), log(e), log(10), log(16))

e = 2.718281828459045
tau = 6.283185307179586
halftau = tau / 2 # 3.141592653589793
quartertau = halftau / 2 # 1.5707963267948966
print(e, tau, halftau, quartertau)

def deg(radians: float) -> float:
  return rad * 360 / tau

def rad(degrees: float) -> float:
  return degrees * tau / 360

print(rad(360), deg(tau))

# TODO: globally optimize

def sin(x: float) -> float:
  # return sin(x) for x on (-halftau, halftau)
  y = 2 / quartertau * x - 1 / (quartertau**2) * x
  #return y
  return 0.775 * y + 0.225 * (y * abs(y))

def cos(x: float) -> float:
  x += quartertau
  if x > halftau: x -= tau
  return sin(x)

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

def gamma(x):
  x -= 1
  #return (1 + 1 / (12 * x) + 1 / (288 * x**2) - 139 / (51840 * x**3)) * (x**x * (math.tau * x)**.5) / math.e**x
  return (x**2 + 1 / 24 * x + 293 / 8640) / (x**2 - 1 / 24 * x + 293 / 8640) * (math.tau * x)**.5 * (x / math.e)**x

def beta(x):
  pass

#print(gamma(0), gamma(2), gamma(3), gamma(4), gamma(5), gamma(6), gamma(13))
