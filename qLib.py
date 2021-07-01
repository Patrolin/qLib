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

epsilon = 1e-6

def sign(x: float) -> int:
  return (x > 0) - (x < 0)

def bisection_solve(a: float, b: float, f: Callable[float, float]) -> float:
  # find a root x of f(x) on [min(a,b), max(a,b)] if sign(f(a)) != sign(f(b))
  sa = sign(f(a))
  if sign(f(b)) == sa:
    return ValueError("sign(f(a)) == sign(f(b))")
  while True:
    x = (a + b) / 2
    if x == a or x == b: return x
    sx = sign(f(x))
    if sx == sa:
      a = x
    else:
      b = x

def wegsteins_fixed_point(x1: float, g: Callable[float, float]) -> float:
  # find a root x of f(x)
  x2 = g(x1)
  dx = 1.0
  while True:
    b = (x1 + g(x2) - x2 - g(x1))
    if b != 0:
      x3 = (x1 * g(x2) - x2 * g(x1)) / b
      dx = x3 - x2
    else:
      x3 = x2 + dx
    if x3 == x2:
      return x3
    x1 = x2
    x2 = x3

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

from collections import UserList

class Polynomial(UserList):
  def eval(self, x: complex) -> complex:
    # return P(x) and d/dx P(x) via Horner's method
    n = len(self.data)
    A = [[0.0] * n] * 2
    
    # P(x)
    A[0][n - 1] = self[n - 1]
    for i in range(n - 2, -1, -1):
      A[0][i] = self[i] + A[0][i + 1] * x
    
    # d/dx P(x)
    A[1][n - 1] = A[0][n - 1]
    for i in range(n - 2, 0, -1):
      A[1][i] = A[0][i] + A[1][i + 1] * x
    
    return A[0][0], A[1][1]
  
  def roots(self):
    W = Polynomial(self.data)
    X = [0.0] * (len(W) - 1)
    for i in range(len(W) - 1):
      x = newtons_solve(0.0, lambda x0: W.eval(x0))
      X[i] = x
      for j in range(len(W) - 2, -1, -1):
        W[j] += W[j + 1] * x
      W.data.pop(0)
    #X = sorted(X, key=lambda x: x.imag)
    #X = sorted(X, key=lambda x: x.real)
    return X

class Wilkinson(Polynomial):
  def __init__(self, N=20):
    W = [0] * (N + 1)
    W[0] = 1.0
    for i in range(1, N + 1):
      carry = 0.0
      for j in range(i + 1):
        w = W[j]
        W[j] = carry - w * i
        carry = w
    self.data = W

class WilkinsonStable(Polynomial):
  def __init__(self, N=20):
    W = [0] * (N + 1)
    W[0] = 1.0
    for i in range(1 - N // 2, N + 1 - N // 2):
      carry = 0.0
      for j in range(i + 1 + N // 2):
        w = W[j]
        W[j] = carry - w * (i / N)
        carry = w
    self.data = W

class Legendre(Polynomial):
  def __init__(self, N=20):
    W = [0] * (N + 1)
    for i in range(N + 1):
      c = (N + i - 1) / 2
      W[i] = 2**N * C(N, i) * V(c, N) / P(N)
    self.data = W

#p = Polynomial([1, 0, 1])
#p = Wilkinson(10)
#p = Polynomial(Legendre(20))
#print(p)
#print(p.roots())
#print(minimize([0.0], lambda x0: wilkinson.eval(x0[0])**2)[0])
#print(f'\n{p.roots()}')

#L5 = Legendre(5)
#print(L5.roots())
#print(minimize([0.0], lambda x0: evalPolynomial(L5, x0[0])**2))
#print(minimize([0.5], lambda x0: evalPolynomial(L5, x0[0])**2))
#print(minimize([0.0, 0.0], lambda x0: (x0[0] + 1)**2 + (x0[1] + 1)**2))
#print(minimize([1.0], lambda x0: evalPolynomial(L5, x0[0])**2))
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
