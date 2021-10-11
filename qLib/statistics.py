from collections import deque as LinkedList, UserList
from typing import *

# (sample mean, sample standard deviation)
def mean(X: List[float]) -> float:
  '''return the population mean = sample mean of X in O(n)'''
  acc = 0.0
  for x in X:
    acc += x
  return acc / len(X)

def stdev(X: List[float], u: float) -> float:
  '''return the sample standard deviation of X given the mean u in O(n)'''
  acc = 0.0
  for x in X:
    acc += (x - u)**2
  return (acc / (len(X) - 1))**0.5

# infinite streams
class EMA:
  def __init__(self, a=0.1):
    self.x_old = 0.0
    self.a = a
  
  def next(self, x: float) -> float:
    '''return the next EMA step in O(1)'''
    self.x_old = self.a * x + (1 - self.a) * self.x_old
    return self.x_old

def _quantile(X: list[float], p: float) -> float:
  '''return a linearly interpolated quantile of a sorted X in O(1)'''
  a = p * (len(X) - 1)
  i = int(a)
  j = -int(-a // 1)
  return ((i + 1) - a) * X[i] + (a - i) * X[j]

class pSquare:
  def __init__(self, p: float, bins=5):
    self.p = p
    self.bins = bins
    self.q: list[float] = []
    self.n = [i for i in range(self.bins)]
  
  def next(self, x: float) -> float:
    '''return the next P-Squared step in O(1)'''
    if len(self.q) < self.bins:
      self.q = sorted(self.q + [x])
      return _quantile(self.q, self.p)
    else:
      # add datapoint
      if x > self.q[-1]:
        self.q[-1] = x
      for i in range(1, self.bins):
        self.n[i] += (self.q[i] >= x)
      if x < self.q[0]:
        self.q[0] = x
      # interpolate if necessary
      for i in range(1, self.bins - 1):
        n_desired = i * self.n[-1] / (self.bins - 1)
        d = n_desired - self.n[i]
        if ((d >= 1) and ((self.n[i + 1] - self.n[i]) > 1)) or ((d <= -1) and ((self.n[i - 1] - self.n[i]) < -1)):
          d = (d > 0) - (d < 0)
          q_desired = self.q[i] + d / (self.n[i + 1] - self.n[i - 1]) * (
              (self.n[i] - self.n[i - 1] + d) * (self.q[i + 1] - self.q[i]) / (self.n[i + 1] - self.n[i]) +
              (self.n[i + 1] - self.n[i] - d) * (self.q[i] - self.q[i - 1]) / (self.n[i] - self.n[i - 1]))
          if (self.q[i - 1] < q_desired < self.q[i + 1]):
            self.q[i] = q_desired
          else:
            self.q[i] = self.q[i] + d * (self.q[i + d] - self.q[i]) / (self.n[i + d] - self.n[i])
          self.n[i] = self.n[i] + d
      return _quantile(self.q, self.p)

def pQuantile(X: list[float], p: float) -> float:
  '''return an estimated p-quantile of X in O(n) via P-Squared algorithm'''
  g = pSquare(p)
  for x in X:
    y = g.next(x)
  return y

def histogram(X: list[float], bins: int, **kwargs):
  g = pSquare(.5, bins + 1)
  for x in X:
    _ = g.next(x)
  print(g.n)
  print(g.q)

# histograms? https://www.cs.wustl.edu/~jain/papers/ftp/psqr.pdf

def mode(X: List[float]) -> float:
  '''return an estimated in-distribution mode of a sorted X in O(n)'''
  u = mean(X)
  A = LinkedList(X)
  for n in range(len(X) - 1, 0, -1):
    # remove farthest neighbor of the mean
    a, a_distance = A[0], abs(A[0] - u)
    b, b_distance = A[-1], abs(A[-1] - u)
    if a_distance >= b_distance:
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

def V(n: int, k: int, step: int = -1) -> int:
  # return variations = (n choose k) * k! in O(k)
  res = 1
  for i in range(k):
    res *= n
    n += step
  return res

def P(n: int, step: int = -1) -> int:
  # return permutations = n! in O(n)
  return V(n, n, step)

def C(n: int, k: int) -> int:
  # return combinations = (n choose k) in O(k)
  return V(n, k) // P(k)

class NamedList(UserList):
  def __init__(self, name: str, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.name = name

def sortedplot(*Y: Union[NamedList, list], **kwargs):
  '''plot the Y as a sorted plot in O(n log n)'''
  import matplotlib.pyplot as plt
  LINESTYLES = [
      (0, (3, 2, 3, 2, 3, 4)), # --- ---
      (0, (1, 1, 1, 1, 1, 3)), # *** ***
      (0, (3, 2, 1, 2, 3, 4)), # -*- -*-
      (0, (1, 2, 1, 2, 3, 4)), # **- **-
      (0, (1, 2, 3, 2, 1, 4)), # *-* *-*
  ]
  fig, ax = plt.subplots()
  Y_named = [NamedList(y.name if isinstance(y, NamedList) else f'{i}', y) for i, y in enumerate(Y)]
  Y_named = sorted(Y_named, key=lambda y: mean(y.data))
  X = None
  for i, y in enumerate(Y_named):
    X = [j / (len(y) - 1) for j in range(len(y))]
    ax.plot(X, sorted(y), linestyle=LINESTYLES[i % len(LINESTYLES)], linewidth=1.8, label=y.name)
  if 'title' not in kwargs: kwargs['title'] = 'Sorted plot'
  ax.set(xlabel='p-quantile', xticks=[0.05, 0.95], ylabel='y', **kwargs)
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
  print(pQuantile(Z, 0.5)) # correct answer: 6.931, pSquared answer: 4.440634353260338, population median: 2.43
  
  import numpy as np
  np.random.seed(19680801)
  x = np.random.normal(0, 1, 100000)
  histogram(x.tolist(), 5)
  print(len(x[x < -4.5]))
