from typing import overload, Optional
from .collections_ import *
from .math_ import *

# (sample mean, sample standard deviation)
@overload
def meanOrZero(X: list[int] | list[float]) -> float:
    ...

@overload
def meanOrZero(X: list[int] | list[float], weights: list[int] | list[float]) -> float:
    ...

def meanOrZero(X: list[int] | list[float], weights: Optional[list[int] | list[float]] = None):
    '''return the population mean = sample mean of X in O(n)'''
    if len(X) == 0: return 0
    if weights == None:
        acc = 0.0
        for x in X:
            acc += x
        return acc / len(X)
    else:
        acc = 0.0
        for i in range(len(X)):
            acc += X[i] * weights[i]
        return acc

def stdevOrZero(X: list[int] | list[float], u: float) -> float:
    '''return the sample standard deviation of X given the sample mean u in O(n)'''
    if len(X) == 1: return 0
    acc = 0.0
    for x in X:
        acc += (x - u)**2
    return (acc / (len(X) - 1))**0.5

# NTP stuff
def modeOrZero(X: list[int] | list[float]) -> float:
    '''return an estimated in-distribution mode of a sorted X in O(n)'''
    if len(X) == 0: return 0
    u = meanOrZero(X)
    A = LinkedList(X)
    for n in range(len(X) - 1, 0, -1):
        # remove farthest neighbor of the mean
        a, a_distance = A[0], abs(A[0] - u)
        b, b_distance = A[A.count - 1], abs(A[A.count - 1] - u)
        if a_distance >= b_distance:
            u -= (a - u) / n
            A.popLeft()
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

class PP:
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
                    d = sign(d)
                    q_desired = self.q[i] + d / (self.n[i + 1] - self.n[i - 1]) * (
                        (self.n[i] - self.n[i - 1] + d) * (self.q[i + 1] - self.q[i]) / (self.n[i + 1] - self.n[i]) +
                        (self.n[i + 1] - self.n[i] - d) * (self.q[i] - self.q[i - 1]) / (self.n[i] - self.n[i - 1]))
                    if (self.q[i - 1] < q_desired < self.q[i + 1]):
                        self.q[i] = q_desired
                    else:
                        self.q[i] = self.q[i] + d * (self.q[i + d] - self.q[i]) / (self.n[i + d] - self.n[i])
                    self.n[i] = self.n[i] + d
            return _quantile(self.q, self.p)

def pQuantile(X: list[float], p: float) -> Optional[float]:
    '''return an estimated p-quantile of X in O(n) via P-Squared algorithm'''
    g = PP(p)
    y = None
    for x in X:
        y = g.next(x)
    return y

if __name__ == '__main__':
    X = sorted([0, .24, .25, 1])
    print(modeOrZero(X), X)

    phi = (1 + 5**.5) / 2
    X = sorted([(0.5 + i * 1 / phi) % 1 for i in range(6)])
    print(modeOrZero(X), X)
    print(meanOrZero(X), stdevOrZero(X, meanOrZero(X)))

    Z = [0.02, 0.15, 0.74, 0.83, 3.39, 22.37, 10.15, 15.43, 38.62, 15.92, 34.60, 10.28, 1.47, 0.40, 0.05, 11.39, 0.27, 0.42, 0.09, 11.37]
    print(pQuantile(Z, 0.5)) # correct answer: 6.931, PP answer: 4.440634353260338, population median: 2.43
