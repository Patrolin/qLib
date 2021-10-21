from qLib.performance import *
import math

if __name__ == '__main__':
  N = 1000000
  A, B = Timer(2)
  for i in range(1, N + 1):
    with A:
      math.log(i)
    with B:
      math.log(i, 10)
  print(A < B)
  print(A == B)
  print(A > B)
