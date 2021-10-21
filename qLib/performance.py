from typing import *
from time import perf_counter_ns

def Timer(n: int = 1):
  return [_Timer() for i in range(n)]

class _Timer:
  def __init__(self):
    self.times: list[float] = []

  def __enter__(self):
    self.start = perf_counter_ns()

  def __exit__(self, exc_type, exc_value, exc_traceback):
    self.end = perf_counter_ns()
    if exc_value: raise exc_value
    self.times.append(self.end - self.start)

  def __lt__(self, other) -> float:
    N = len(self.times)
    self_sorted = sorted(self.times)
    other_sorted: list[float] = sorted(other.times)
    return sum(self_sorted[i] < other_sorted[i] for i in range(N)) / N

  def __eq__(self, other) -> float:
    N = len(self.times)
    self_sorted = sorted(self.times)
    other_sorted: list[float] = sorted(other.times)
    return sum(self_sorted[i] == other_sorted[i] for i in range(N)) / N

  def __gt__(self, other) -> float:
    N = len(self.times)
    self_sorted = sorted(self.times)
    other_sorted: list[float] = sorted(other.times)
    return sum(self_sorted[i] > other_sorted[i] for i in range(N)) / N
