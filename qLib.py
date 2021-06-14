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
  return V(n, k) // P(k)

# def C(n: float, k: float) -> float:

epsilon = 1e-8

def minimize(x0: List[float], f: Callable[[List[float]], float], ro: float = 0.9) -> List[float]:
  # find a local minimum for a function with continuous gradient using AdaDelta
  mean_square_delta = [0.0] * len(x0)
  mean_square_gradient = [0.0] * len(x0)
  gradient = 1.0
  while abs(gradient) > epsilon:
    for j in range(len(x0)):
      x1 = list(x0)
      x1[j] += epsilon
      gradient = (f(x1) - f(x0)) / epsilon
      mean_square_gradient[j] = ro * mean_square_gradient[j] + (1 - ro) * gradient**2
      delta_x = -((mean_square_delta[j] + epsilon) / (mean_square_gradient[j] + epsilon))**.5 * gradient
      x0[j] += delta_x
      mean_square_delta[j] = ro * mean_square_delta[j] + (1 - ro) * delta_x**2
      #print(x1, gradient)
  return x0

#phi1 = minimize([1.0], lambda x0: (x0[0]**2 - x0[0] - 1)**2)[0]
#phi2 = minimize([1.0], lambda x0: (x0[0]**3 - x0[0] - 1)**2)[0]
#phi3 = minimize([1.0], lambda x0: (x0[0]**4 - x0[0] - 1)**2)[0]
#phi4 = minimize([1.0], lambda x0: (x0[0]**5 - x0[0] - 1)**2)[0]
#print(phi1, phi2, phi3, phi4) # 1.618033983547484 1.3247179522114612 1.2207440795921793 1.1673039732520734

#e = minimize([1.0], lambda x0: ((x0[0]**(1 + epsilon) - x0[0]) / epsilon - x0[0])**2)[0]
#print(e) # 2.7182818194466964

pi = 0
delta_x = 1
i = 0
while abs(delta_x) > 0:
  delta_x = 2 / 16**i * (4 / (8 * i + 1) - 2 / (8 * i + 4) - 1 / (8 * i + 5) - 1 / (8 * i + 6))
  pi += delta_x
  i += 1
#print(pi) # 6.283185307179586

def Legendre(n: int) -> List[float]:
  L = [0] * (n + 1)
  for i in range(n + 1):
    c = (n + i - 1) / 2
    L[i] = 2**n * C(n, i) * V(c, n) / P(n)
  return L

def evalPolynomial(W: List[float], x: float) -> float:
  total = 0.0
  for i in range(len(W)):
    total += W[i] * x**i
  return total

L5 = Legendre(5)
print(minimize([0], lambda x0: evalPolynomial(L5, x0[0])**2))
#print([minimize([i / 10], lambda x0: evalPolynomial(L5, x0[0])**2) for i in range(-10, 11, 1)])

# pi = atan(1)
# zeta(2) = pi**2/6
# int from -1 to 1 of 1 / (1 - x**2)**.5 = pi
# int from -1 to 1 of (1 - x**2)**.5 = pi/2

# Gauss-Laguerre: f(x) * e**x *  # (x) / ((n + 1)**2 * L(x)**2)
# int from 0 to inf of t**(x-1) * e**(-t) dt gamma(1/2) = pi**.5

# Gauss-Hermite: f(x) * e**(x**2) # * (n!) / (n**2 * He(x)**2)
# int from -inf to inf of e**(-x**2) = pi**.5
# int from -inf to inf of 1 / (1 + x**2) = pi
# int from -inf to inf of (sin x) / x = pi

def integrate(f: Callable[[float], float], a: float, b: float) -> float:
  return 0.0

quartertau = integrate(lambda x: (1 - x**2)**.5, -1, 1)
halftau = 2 * quartertau
tau = 2 * halftau
#print(tau, math.tau)

def sin(x: float) -> float:
  # sin(x) for x in (-halftau, halftau)
  y = 2 / quartertau * x - 1 / (quartertau**2) * x
  #return y
  return 0.775 * y + 0.225 * (y * abs(y))

def cos(x: float) -> float:
  x += quartertau
  if x > halftau: x -= tau
  return sin(x)

# Complex, # https://mathworld.wolfram.com/ComplexExponentiation.html

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

#print(gamma(0), gamma(2), gamma(3), gamma(4), gamma(5), gamma(6), gamma(13))
