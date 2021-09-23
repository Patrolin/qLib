from collections import deque as LinkedList, UserList
from typing import *

def mean(X: List[float]) -> float:
  # return the population/sample mean of X in O(n)
  acc = 0.0
  for x in X:
    acc += x
  return acc / len(X)

def EMA(x: float, x_old: float, a=0.1):
  # return the next (exponential moving average) step in O(1)
  return a * x + (1 - a) * x_old

def median(X: List[float]) -> float:
  # return the population median of a sorted X in O(1)
  i = len(X) // 2
  if len(X) % 2 == 1:
    return X[i]
  elif len(X) % 2 == 0:
    return (X[i] + X[i + 1]) / 2

def pQuantile(X: list[float], p: float) -> float:
  # return an estimated p-quantile of X in O(n) via P-Square algorithm
  q = sorted(X[:5])
  if len(X) <= 5:
    return q[round(p * len(X))]
  n = [i for i in range(5)]
  n_desired = [0, 2 * p, 4 * p, 2 + 2 * p, 4]
  d_n_desired = [0, p / 2, p, (1 + p) / 2, 1]
  for x in X[5:]:
    k = 1
    if x < q[0]:
      q[0] = x
    k += (x >= q[1]) + (x >= q[2]) + (x >= q[3])
    if x >= q[4]:
      q[4] = x
    
    for i in range(k, 5):
      n[i] += 1
    for i in range(5):
      n_desired[i] += d_n_desired[i]
    for i in range(1, 4):
      d = n_desired[i] - n[i]
      if ((d >= 1) and ((n[i + 1] - n[i]) > 1)) or ((d <= -1) and ((n[i - 1] - n[i]) < -1)):
        d = (d > 0) - (d < 0)
        q_desired = q[i] + d / (n[i + 1] - n[i - 1]) * ((n[i] - n[i - 1] + d) * (q[i + 1] - q[i]) / (n[i + 1] - n[i]) +
                                                        (n[i + 1] - n[i] - d) * (q[i] - q[i - 1]) / (n[i] - n[i - 1]))
        if (q[i - 1] < q_desired < q[i + 1]):
          q[i] = q_desired
        else:
          q[i] = q[i] + d * (q[i + d] - q[i]) / (n[i + d] - n[i])
        n[i] = n[i] + d
  return q[2]

# histograms? https://www.cs.wustl.edu/~jain/papers/ftp/psqr.pdf

def mode(X: List[float]) -> float:
  # return an estimated in-distribution mode of a sorted X in O(n)
  u = mean(X)
  A = LinkedList(X)
  for n in range(len(X) - 1, 0, -1):
    # remove farthest neighbor relative to the mean
    a, aDistance = A[0], abs(A[0] - u)
    b, bDistance = A[-1], abs(A[-1] - u)
    if aDistance >= bDistance:
      u -= (a - u) / n
      A.popleft()
    else:
      u -= (b - u) / n
      A.pop()
  return A[0]
  # d > 1
  # https://stackoverflow.com/questions/59672100/how-to-find-farthest-neighbors-in-euclidean-space
  # http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.386.8193&rep=rep1&type=pdf
  # https://en.wikipedia.org/wiki/Priority_queue
  # https://en.wikipedia.org/wiki/R-tree
  # https://en.wikipedia.org/wiki/Ball_tree

def var(X: List[float], u: float) -> float:
  # return the sample variance of X given the mean u in O(n)
  acc = 0.0
  for x in X:
    acc += (x - u)**2
  return acc / (len(X) - 1)

def stdev(X: List[float], u: float) -> float:
  # return the sample standard deviation of X given the mean u in O(n)
  return var(X, u)**.5

def V(n: int, k: int, step: int = -1) -> int:
  # return (n choose k) * k! in O(k)
  res = 1
  for i in range(k):
    res *= n
    n += step
  return res

def P(n: int, step: int = -1) -> int:
  # return n! in O(n)
  return V(n, n, step)

def C(n: int, k: int) -> int:
  # return (n choose k) in O(k)
  return V(n, k) // P(k)

class NamedList(UserList):
  def __init__(self, name, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.name = name

def sortedplot(*Y: Tuple[NamedList], **kwargs):
  # plot the sorted Y values in O(n log n)
  import matplotlib.pyplot as plt
  LINESTYLES = [
      (0, (3, 2, 3, 2, 3, 4)), # --- ---
      (0, (1, 1, 1, 1, 1, 3)), # *** ***
      (0, (3, 2, 1, 2, 3, 4)), # -*- -*-
      (0, (1, 2, 1, 2, 3, 4)), # **- **-
      (0, (1, 2, 3, 2, 1, 4)), # *-* *-*
  ]
  fig, ax = plt.subplots()
  Y = [NamedList(i if 'name' not in y else y.name, y) for i, y in enumerate(Y)]
  Y = sorted(Y, key=lambda y: mean(y))
  X = None
  for i, y in enumerate(Y):
    X = [j / (len(y) - 1) for j in range(len(y))]
    ax.plot(X, sorted(y), linestyle=LINESTYLES[i % len(LINESTYLES)], linewidth=1.8, label=y.name)
  ax.set(xlabel='p-quantile', xticks=X, ylabel='y', title='Sorted plot', **kwargs)
  ax.grid()
  ax.legend(prop={'size': 12})
  plt.show()

if __name__ == '__main__':
  X = sorted([0, .24, .25, 1])
  print(mode(X), X)
  
  phi = (1 + 5**.5) / 2
  X = sorted([(0.5 + i * 1 / phi) % 1 for i in range(6)])
  print(mode(X), X)
  print(mean(X), stdev(X, mean(X)))
  
  #sortedplot([0.8, 1, 1.1], [0.75, 0.75, 0.75], X)
  Z = [
      0.02, 0.15, 0.74, 0.83, 3.39, 22.37, 10.15, 15.43, 38.62, 15.92, 34.60, 10.28, 1.47, 0.40, 0.05, 11.39, 0.27,
      0.42, 0.09, 11.37
  ]
  print(pQuantile(Z, 0.5)) # exact answer: 6.931
