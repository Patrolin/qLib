from typing import *

def mean(X: List[float]) -> float:
  # return the mean of X in O(n)
  acc = 0.0
  for x in X:
    acc += x
  return acc / len(X)
  #res = 0.0
  #for i, x in enumerate(X, start=1):
  #  res += (x-u)/i
  #return res

def median(X: List[float]) -> float:
  # return the median of a sorted X in O(1)
  i = len(X)//2
  if len(X)%2 == 1:
    return X[i]
  elif len(X)%2 == 0:
    return (X[i]+X[i+1])/2

def mode(X: List[float]) -> float:
  # return an estimated in-distribution mode of X in O(n^2)
  A = list(X)
  u = mean(A)
  for n in range(len(X)-1, 1, -1):
    worstI, worstDistance = 0, 0.0
    for i, x in enumerate(A):
      distance = abs(u-x)
      if distance > worstDistance:
        worstI, worstDistance = i, distance
    u -= (A[worstI]-u) / n
    A.pop(worstI)
  return A[0]
  # is this better? https://www.sciencedirect.com/science/article/abs/pii/S016771520900354X

# quantiles? https://www.cs.wustl.edu/~jain/papers/ftp/psqr.pdf

if __name__ == '__main__':
  X = [0, .24, .25, 1]
  print(mode(X), X)

  phi = (1 + 5**.5)/2
  X = [(0.5 + i*1/phi) % 1 for i in range(5)]
  print(mode(X), X)
