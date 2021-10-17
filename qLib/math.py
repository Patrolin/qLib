from math import sin

e = 2.718281828459045
tau = 6.283185307179586
half_tau = tau / 2 # 3.141592653589793
quarter_tau = half_tau / 2 # 1.5707963267948966

def Gamma(x: int | float) -> float:
  '''return Gamma(x) in O(log n)'''
  y = (2 * x + 1 / 3)**.5 * half_tau**.5 * x**x * e**(-x)
  if x < 0:
    return half_tau / (sin(half_tau * x) * y)
  else:
    return y
