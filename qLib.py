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

def bisection_solve(a: float, b: float, f: Callable[[float], float]) -> float:
  # find the root x of f(x) in [a, b]
  sa = sign(f(a))
  if sa == 0: return a
  sb = sign(f(b))
  if sb == 0: return b
  if sa == sign(b):
    return ValueError("sign(f(a)) == sign(f(b))")
  while True:
    x = (a + b) / 2
    sx = sign(f(x))
    if x == a or x == b: return x
    if sx == sa:
      a = x
      sa = sx
    else:
      b = x

phi1 = bisection_solve(1.0, 2.0, lambda x: x**2 - x - 1)
phi2 = bisection_solve(1.0, 2.0, lambda x: x**3 - x - 1)
phi3 = bisection_solve(1.0, 2.0, lambda x: x**4 - x - 1)
phi4 = bisection_solve(1.0, 2.0, lambda x: x**5 - x - 1)
print(phi1, phi2, phi3, phi4) # 1.618033988749895 1.3247179572447458 1.2207440846057596 1.1673039782614185

def newtons_solve(x: float, f: Callable[[float], float]) -> float:
  # find a root x if f(x), given lim (x -> +-inf) d/dx f(x) != 0
  dx = 1.0
  while abs(dx) > epsilon:
    dy_dx = (f(x + epsilon) - f(x)) / epsilon
    if dy_dx != 0:
      dx = -f(x) / dy_dx
    x = x + dx
  return x

# m = 1/2 + (x1 - x2) / (x3 - 2*x2 + x1)

def minimize(x0: List[float], f: Callable[[List[float]], float], ro: float = 0.9) -> List[float]:
  # find a local minimum for a function with continuous gradient using fixed AdaDelta
  gradient = [0.0] * len(x0)
  mean_square_gradient = 0.0
  delta_x = [0.0] * len(x0)
  mean_square_delta_x = 0.0
  n = 0
  loop = 1.0
  while loop > epsilon**2:
    loop = 0
    n += 1
    x1 = list(x0)
    x1[0] += epsilon
    gradient[0] = (f(x1) - f(x0)) / epsilon
    for j in range(1, len(x0)):
      x1[j - 1] = x0[j - 1]
      x1[j] += epsilon
      gradient[j] = (f(x1) - f(x0)) / epsilon
    square_gradient = sum(g**2 for g in gradient)
    loop += square_gradient
    mean_square_gradient = ro * mean_square_gradient + (1 - ro) * square_gradient
    for j in range(len(x0)):
      #yee = math.tanh(n - 1)
      #yee = (n - 1) / n
      yee = 0.5
      k = ((mean_square_delta_x + epsilon) / (mean_square_gradient + epsilon))**.5
      delta_x[j] = -gradient[j] * (yee * k + (1 - yee) * 1)
      x0[j] += delta_x[j]
    square_delta_x = sum(dx**2 for dx in delta_x)
    mean_square_delta_x = ro * mean_square_delta_x + (1 - ro) * square_delta_x
    #print(x0, gradient)
    import time
    time.sleep(.02)
  print(n, x0, gradient)
  return x0

def newtons_minimize(x: float, f: Callable[[float], float], ro: float = 0.9) -> float:
  mean_dx = 0.0
  dx = 1.0
  while abs(dx) > epsilon:
    dy_dx = (f(x + epsilon) - f(x)) # / epsilon
    d2y_dx2 = (f(x + 2 * epsilon) - 2 * f(x + epsilon) + f(x)) / epsilon # / epsilon
    dx = -dy_dx / d2y_dx2
    mean_dx = (1 - ro) * mean_dx + ro * dx
    x = x + dx
  return x

def fixed_point(x: float, g: Callable[[float], float], ro: float = 1.0) -> float:
  mean_dx = 0.0
  dx = 1.0
  while abs(dx) > epsilon:
    x1 = g(x)
    dx = x1 - x
    mean_dx = (1 - ro) * mean_dx + ro * dx
    x = x + mean_dx
  return x

def wegsteins(x0: float, g: Callable[[float], float]) -> float:
  x1 = g(x0)
  x2 = g(x1)
  print(x0, x1, x2)
  while abs(x2 - x1) > epsilon:
    if x1 == x0:
      tmp = x2
      x2 = g(x1) + 2 * epsilon
      x0 = x1
      x1 = tmp
      continue
    a = (x2 - x1) / (x1 - x0)
    if a == 1:
      tmp = x2
      x2 = g(x1) + 2 * epsilon
      x0 = x1
      x1 = tmp
      continue
    q = a / (a - 1)
    tmp = x2
    x2 = q * x1 + (1 - q) * g(x1)
    x0 = x1
    x1 = tmp
    print(x0, x1, x2)
    import time
    time.sleep(.02)
  return x2

# exp, expm1, log1p

def log(x: float) -> float:
  return (x**epsilon - 1) / epsilon

def log2(x: float) -> float:
  return log(x) / log(2)

def log10(x: float) -> float:
  return log(x) / log(10)

#e = minimize([3.0], lambda x0: ((x0[0]**(1 + epsilon) - x0[0]) / epsilon - x0[0])**2)[0]
#print(e) # 2.7186029435049646

#print(log(2), log(1), log(e), log(10), log(16))

pi = 0
delta_x = 1
i = 0
while abs(delta_x) > 0:
  delta_x = 2 / 16**i * (4 / (8 * i + 1) - 2 / (8 * i + 4) - 1 / (8 * i + 5) - 1 / (8 * i + 6))
  pi += delta_x
  i += 1
#print(pi) # 6.283185307179586

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
      x = 0.0
      dx = 1.0
      while abs(dx) > epsilon:
        y, dy_dx = W.eval(x)
        if dy_dx != 0:
          dx = -y / dy_dx
        x = x + dx
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

def Legendre(n: int) -> List[float]:
  L = [0] * (n + 1)
  for i in range(n + 1):
    c = (n + i - 1) / 2
    L[i] = 2**n * C(n, i) * V(c, n) / P(n)
  return L

#p = Polynomial([1, 0, 1])
#p = Wilkinson(10)
p = Polynomial(Wilkinson(20))
print(p)
print(p.roots())
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
