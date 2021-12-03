from typing import *
from time import perf_counter_ns
'''
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
'''

# TODO: rdtsc

# https://docs.microsoft.com/en-gb/windows/win32/cimwin32prov/win32-processor
# https://github.com/workhorsy/py-cpuinfo
cpu_s = '''$colItems = Get-WmiObject "Win32_Processor"
foreach ($objItem in $colItems) {
  Write-Host "CPU Model: " -NoNewLine
  Write-Host $objItem.Name
  Write-Host "CPU Cores: " -NoNewLine
  Write-Host $objItem.NumberOfCores
  Write-Host "CPU Max Speed: " -NoNewLine
  Write-Host $objItem.MaxClockSpeed
  Write-Host "CPU Current Speed: " -NoNewLine
  Write-Host $objItem.CurrentClockSpeed
}'''

if __name__ == '__main__':
  import ctypes

  print(ctypes.windll.wmi)
