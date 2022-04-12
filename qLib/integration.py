from qLib import *
from typing import *

def wegsteins_fixed_point(x1: float, g: Callable[[float], float]) -> float:
    # find a root x of f(x)
    x2 = g(x1)
    dx = 1.0
    while True:
        b = (x1 + g(x2) - x2 - g(x1))
        if b != 0:
            x3 = (x1 * g(x2) - x2 * g(x1)) / b
            dx = x3 - x2
        else:
            x3 = x2 + dx
        if x3 == x2:
            return x3
        x1 = x2
        x2 = x3

from collections import UserList

class Polynomial(UserList):
    def eval(self, x: complex) -> Tuple[float, float]:
        # return P(x) and d/dx P(x) via Horner's method
        n = len(self.data)
        A = [[0.0] * n] * 2

        # P(x)
        A[0][n - 1] = self[n - 1]
        for i in range(n - 2, -1, -1):
            A[0][i] = self[i] + A[0][i + 1] * x

        # d/dx P(x)
        A[1][n - 1] = A[0][n - 1]
        for i in range(n - 2, 0, -1):
            A[1][i] = A[0][i] + A[1][i + 1] * x # type: ignore

        return A[0][0], A[1][1]

    def roots(self):
        W = Polynomial(self.data)
        X = [0.0] * (len(W) - 1)
        for i in range(len(W) - 1):
            x = wegsteins_fixed_point(0.0, lambda x0: W.eval(x0)[0] - x0)
            X[i] = x
            for j in range(len(W) - 2, -1, -1):
                W[j] += W[j + 1] * x
            W.data.pop(0)
        #X = sorted(X, key=lambda x: x.imag)
        #X = sorted(X, key=lambda x: x.real)
        return X

class Wilkinson(Polynomial):
    def __init__(self, N=20):
        W = [0] * (N + 1)
        W[0] = 1.0
        for i in range(1, N + 1):
            carry = 0.0
            for j in range(i + 1):
                w = W[j]
                W[j] = carry - w * i
                carry = w
        self.data = W

class WilkinsonStable(Polynomial):
    def __init__(self, N=20):
        W = [0] * (N + 1)
        W[0] = 1.0
        for i in range(1 - N // 2, N + 1 - N // 2):
            carry = 0.0
            for j in range(i + 1 + N // 2):
                w = W[j]
                W[j] = carry - w * (i / N)
                carry = w
        self.data = W

class Legendre(Polynomial):
    def __init__(self, N=20):
        W = [0] * (N + 1)
        for i in range(N + 1):
            c = (N + i - 1) / 2
            W[i] = 2**N * C(N, i) * V(c, N) / P(N)
        self.data = W

#p = Polynomial([1, 0, 1])
#p = Wilkinson(10)
#p = Polynomial(Legendre(20))
#print(p)
#print(p.roots())
#print(minimize([0.0], lambda x0: wilkinson.eval(x0[0])**2)[0])
#print(f'\n{p.roots()}')

#L5 = Legendre(5)
#print(L5.roots())
#print(minimize([0.0], lambda x0: evalPolynomial(L5, x0[0])**2))
#print(minimize([0.5], lambda x0: evalPolynomial(L5, x0[0])**2))
#print(minimize([0.0, 0.0], lambda x0: (x0[0] + 1)**2 + (x0[1] + 1)**2))
#print(minimize([1.0], lambda x0: evalPolynomial(L5, x0[0])**2))
#print([minimize([i / 10], lambda x0: evalPolynomial(L5, x0[0])**2) for i in range(-10, 11, 1)])

# pi = atan(1)
# zeta(2) = pi**2/6
# int from -1 to 1 of 1 / (1 - x**2)**.5 = pi
# int from -1 to 1 of (1 - x**2)**.5 = pi/2

# Gauss-Laguerre: f(x) * e**x *  # (x) / ((n + 1)**2 * L(x)**2)
# int from 0 to inf of t**(x-1) * e**(-t) dt gamma(1/2) = pi**.5

# Gauss-Hermite: f(x) * e**(x**2) # * (n!) / (n**2 * He(x)**2)
# int from -inf to inf of e**(-x**2) = pi**.5
# int from -inf to inf of 1 / (1 + x**2) = pi
# int from -inf to inf of (sin x) / x = pi

def integrate(f: Callable[[float], float], a: float, b: float) -> None:
    pass
