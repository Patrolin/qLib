from collections import deque as LinkedList, UserList
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
  # return the median of a sorted X
  i = len(X)//2
  if len(X)%2 == 1:
    return X[i]
  elif len(X)%2 == 0:
    return (X[i]+X[i+1])/2

def mode(X: List[float]) -> float:
  # return an estimated in-distribution mode of a sorted X in O(n)
  u = mean(X)
  A = LinkedList(X)
  for n in range(len(X)-1, 0, -1):
    # remove farthest neighbor relative to the mean
    a, aDistance = A[0], abs(A[0]-u)
    b, bDistance = A[-1], abs(A[-1]-u)
    if aDistance >= bDistance:
      u -= (a-u) / n
      A.popleft()
    else:
      u -= (b-u) / n
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
    acc += (x-u)**2
  return acc / (len(X)-1)

def stdev(X: List[float], u: float) -> float:
  # return the sample standard deviation of X given the mean u in O(n)
  return var(X, u)**.5

# quantiles? https://www.cs.wustl.edu/~jain/papers/ftp/psqr.pdf

class NamedList(UserList):
  def __init__(self, name, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.name = name

def sortedplot(*Y: Tuple[NamedList], **kwargs):
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
  for i, y in enumerate(Y):
    X = [j / (len(y)-1) for j in range(len(y))]
    ax.plot(X, sorted(y), linestyle=LINESTYLES[i%len(LINESTYLES)], linewidth=1.8, label=y.name)
  ax.set(xlabel='quantile', xticks=X, ylabel='y', title='Sorted plot', **kwargs)
  ax.grid()
  ax.legend(prop={'size': 12})
  plt.show()

if __name__ == '__main__':
  X = sorted([0, .24, .25, 1])
  print(mode(X), X)

  phi = (1 + 5**.5)/2
  X = sorted([(0.5 + i*1/phi) % 1 for i in range(6)])
  print(mode(X), X)
  print(mean(X), stdev(X, mean(X)))

  sortedplot([0.8, 1, 1.1], [0.75, 0.75, 0.75], X)
