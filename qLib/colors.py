from qLib import lerp, half_tau

def cerp(a: float, x: float, y: float) -> float:
  return lerp(3 / half_tau * x - 4 / half_tau**3 * x**3, x, y)

if __name__ == '__main__':
  print([lerp(a, 1, 2) for a in [0.2, 0.5, 0.8]])
  print()
  print([cerp(a, 1, 2) for a in [0.2, 0.5, 0.8]])
