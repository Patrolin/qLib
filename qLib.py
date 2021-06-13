import math
from math import remainder as rem, modf, hypot as L2
from typing import *

# bitwise (|, &, copysign)

# add, sub, mul, div, pow, isqrt, exp, expm1, log, log2, log10, log1p

def mod(a: float, b: float) -> float:
  return a % b

def rem(a: float, b: float) -> float:
  return math.remainder(a, b)

# floor, round, ceil, abs

def trunc(x: float) -> float:
  return math.trunc(x)

def modf(x: float) -> Tuple[float, float]:
  return math.modf(x)

# frexp, ldexp, isfinite, isinf, isnan

# (cos, sin, tan) * ('', 'a-', '-h')

# Degrees, Radians

def V(n: int, k: int, step: int = -1) -> int:
  res = 1
  for i in range(k):
    res *= n
    n += step
  return res

def P(n: int, step: int = -1) -> int:
  return V(n, n, step)

def C(n: int, k: int) -> int:
  return V(n, k) // P(n)

epsilon = 1e-8

def optimize(x0: List[float], loss: Callable[[List[float]], float], ro: float = 0.9) -> List[float]:
  # optimize a loss function with continuous gradient using AdaDelta
  mean_square_delta = [0.0] * len(x0)
  mean_square_gradient = [0.0] * len(x0)
  gradient = 1.0
  while abs(gradient) > epsilon:
    for j in range(len(x0)):
      x1 = list(x0)
      x1[j] += epsilon
      gradient = (loss(x1) - loss(x0)) / epsilon
      mean_square_gradient[j] = ro * mean_square_gradient[j] + (1 - ro) * gradient**2
      delta_x = -((mean_square_delta[j] + epsilon) / (mean_square_gradient[j] + epsilon))**.5 * gradient
      x0[j] += delta_x
      mean_square_delta[j] = ro * mean_square_delta[j] + (1 - ro) * delta_x**2
  return x0

phi1 = optimize([1.0], lambda x0: (x0[0]**2 - x0[0] - 1)**2)[0]
phi2 = optimize([1.0], lambda x0: (x0[0]**3 - x0[0] - 1)**2)[0]
phi3 = optimize([1.0], lambda x0: (x0[0]**4 - x0[0] - 1)**2)[0]
phi4 = optimize([1.0], lambda x0: (x0[0]**5 - x0[0] - 1)**2)[0]
pi = optimize([3.0], lambda x0: (sum((1, -1)[((i - 1) // 2) % 2] * x0[0]**i / P(i) for i in range(1, 30, 2)))**2)[0]
print(phi1, phi2, phi3, phi4) # 1.618033983547484 1.3247179522114612 1.2207440795921793 1.1673039732520734
print(pi, math.pi)

# e, tau, halftau, quartertau

# Vector, Matrix

# gcd, erf, erfc

# gcd(a/b, c/d) = gcd(a, c) / lcm(b, d)

# gauss quadrature, lobatto, quadrature, chebyshev quadrature

def gamma(x):
  x -= 1
  #return (1 + 1 / (12 * x) + 1 / (288 * x**2) - 139 / (51840 * x**3)) * (x**x * (math.tau * x)**.5) / math.e**x
  return (x**2 + 1 / 24 * x + 293 / 8640) / (x**2 - 1 / 24 * x + 293 / 8640) * (math.tau * x)**.5 * (x / math.e)**x

def beta(x):
  pass

print(gamma(0), gamma(2), gamma(3), gamma(4), gamma(5), gamma(6), gamma(13))
