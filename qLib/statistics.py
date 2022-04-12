from collections import UserList
from typing import *
from .iterables import *
from .math import *

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

# visual analysis
def equiprobable_histogram(X: list[float], bins: int, **kwargs):
    g = PP(.5, bins + 1)
    for x in X:
        _ = g.next(x)
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    fig, ax = plt.subplots()
    for i in range(bins):
        x1 = g.q[i]
        x2 = g.q[i + 1]
        ax.add_patch(Rectangle((x1, 0), x2 - x1, 1 / bins, edgecolor='black'))
    # todo: use kwargs
    ax.set(xlim=(g.q[0], g.q[-1]), title='Equiprobable histogram\n(normal distribution)', xlabel='x', ylabel='probability')
    plt.show()

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
    Y_named = sorted(Y_named, key=lambda y: meanOrZero(y.data))

    X = None
    for i, y in enumerate(Y_named):
        X = [j / (len(y) - 1) for j in range(len(y))]
        ax.plot(X, sorted(y), linestyle=LINESTYLES[i % len(LINESTYLES)], linewidth=1.8, label=y.name)

    p05 = [_quantile(sorted(y.data), 0.05) for y in Y_named]
    p95 = [_quantile(sorted(y.data), 0.95) for y in Y_named]
    kwargs_default = {
        'title': 'Sorted plot',
        'xlabel': 'p-quantile',
        'ylabel': 'y',
        'xticks': [0.05, 0.95],
        'ylim': (min(p05), max(p95)),
    }
    for k, v in kwargs_default.items():
        if k not in kwargs: kwargs[k] = v
    ax.set(**kwargs)
    ax.grid()
    ax.legend(prop={'size': 12})
    plt.show()

if __name__ == '__main__':
    X = sorted([0, .24, .25, 1])
    print(modeOrZero(X), X)

    phi = (1 + 5**.5) / 2
    X = sorted([(0.5 + i * 1 / phi) % 1 for i in range(6)])
    print(modeOrZero(X), X)
    print(meanOrZero(X), stdevOrZero(X, meanOrZero(X)))

    #sortedplot([0.8, 1, 1.1], [0.75, 0.75, 0.75], X)
    Z = [0.02, 0.15, 0.74, 0.83, 3.39, 22.37, 10.15, 15.43, 38.62, 15.92, 34.60, 10.28, 1.47, 0.40, 0.05, 11.39, 0.27, 0.42, 0.09, 11.37]
    print(pQuantile(Z, 0.5)) # correct answer: 6.931, PP answer: 4.440634353260338, population median: 2.43

    class FractalRand:
        def __init__(self, seed: float):
            self.x = seed

        def next(self) -> float:
            self.x = (self.x**2 + 1)**2 / (4 * self.x * (self.x**2 - 1))
            y = self.x - sign(self.x)
            import math
            return y #/ (y + 1)

    r = FractalRand(2)

    X = []
    for i in range(100000):
        X.append(r.next())
    sortedplot(NamedList('fractal_rand() [not normalized]', X))
