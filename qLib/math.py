from typing import *
from math import sin, remainder as rem, modf, hypot as L2

# units
e = 2.718281828459045
tau = 6.283185307179586
half_tau = tau / 2
quarter_tau = half_tau / 2

epsilon = 1e-6

def deg(radians: float) -> float:
  return radians * 360 / tau

def rad(degrees: float) -> float:
  return degrees * tau / 360

# functions
# a + b
# a - b
# a * b
# a / b
# a ^ b
# a mod b
# a rem b

def sign(x: float) -> int:
  return (x > 0) - (x < 0)

# log(x) = (x**epsilon - 1) / epsilon

def Gamma(x: int | float) -> float:
  '''return Gamma(x) in O(log n)'''
  y = (2 * x + 1 / 3)**.5 * half_tau**.5 * x**x * e**(-x)
  if x < 0:
    return half_tau / (sin(half_tau * x) * y)
  else:
    return y

def bisection_solve(a: float, b: float, f: Callable[[float], float]) -> float:
  # find a root x of f(x) on [min(a,b), max(a,b)] if sign(f(a)) != sign(f(b))
  sa = sign(f(a))
  if sa == sign(f(b)):
    raise ValueError("sign(f(a)) == sign(f(b))")
  while True:
    # shrink the interval towards some root
    x = (a + b) / 2
    if x == a or x == b: return x
    sx = sign(f(x))
    if sx == sa:
      a = x
    else:
      b = x

# TODO: Nelder-Mead for robust unbounded local optimization

# TODO: globally optimize

phi1 = bisection_solve(1.0, 2.0, lambda x: x**2 - x - 1)
phi2 = bisection_solve(1.0, 2.0, lambda x: x**3 - x - 1)
phi3 = bisection_solve(1.0, 2.0, lambda x: x**4 - x - 1)
phi4 = bisection_solve(1.0, 2.0, lambda x: x**5 - x - 1)
