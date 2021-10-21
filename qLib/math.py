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
# log(x) = (x**epsilon - 1) / epsilon

def sign(x: float) -> int:
  return (x > 0) - (x < 0)

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

def nelder_mead_1D(f: Callable, x1: float, x2: float) -> float:
  '''return a local minimum of a 1D f(x) in O(1) via Nelder-Mead'''
  y1 = f(x1)
  y2 = f(x2)
  if y1 < y2:
    best_x, worst_x = x1, x2
    best_y, worst_y = y1, y2
  else:
    best_x, worst_x = x2, x1
    best_y, worst_y = y2, y1
  if abs(best_x - worst_x) > epsilon:
    for i in range(100):
      centroid = worst_x
      reflection_x = 2 * best_x - centroid
      expansion_x = 3 * best_x - 2 * centroid
      contraction_shrink_x = 0.5 * best_x + 0.5 * worst_x
      reflection_y = f(reflection_x)
      if reflection_y < best_y:
        expansion_y = f(expansion_x)
        if expansion_y < best_y:
          worst_x, worst_y = best_x, best_y
          best_x, best_y = expansion_x, expansion_y
        else:
          worst_x, worst_y = best_x, best_y
          best_x, best_y = reflection_x, reflection_y
      else:
        contraction_shrink_y = f(contraction_shrink_x)
        if contraction_shrink_y < best_y:
          worst_x, worst_y = best_x, best_y
          best_x, best_y = contraction_shrink_x, contraction_shrink_y
        else:
          worst_x, worst_y = contraction_shrink_x, contraction_shrink_y
      if abs(best_x - worst_x) <= epsilon:
        break
  if abs(best_x - worst_x) > epsilon:
    raise ValueError()
  return best_x

# TODO: globally optimize

phi1 = bisection_solve(1.0, 2.0, lambda x: x**2 - x - 1)
phi2 = bisection_solve(1.0, 2.0, lambda x: x**3 - x - 1)
phi3 = bisection_solve(1.0, 2.0, lambda x: x**4 - x - 1)
phi4 = bisection_solve(1.0, 2.0, lambda x: x**5 - x - 1)

f = lambda x: x**2 - x - 1
x1 = nelder_mead_1D(lambda x: (f(x) if x >= 1 else x - 2)**2, 1.0, 1 + 2 * epsilon)
print(x1, f(x1))
