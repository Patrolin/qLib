from types import LambdaType
from typing import *
import sys
import traceback
import inspect

RED_COLOR = '\033[0;31m'
NO_COLOR = '\033[0m'

test_count = 0
passed_count = 0

def test(faw: Union[bool, Tuple[Callable], Tuple[Callable, list], Tuple[Callable, list, dict]], expectedValue):
  global test_count, passed_count
  faw = cast(Union[Tuple[Callable], Tuple[Callable, list], Tuple[Callable, list, dict]], faw)
  if not (1 <= len(faw) <= 3): raise TypeError('faw must have len(faw) in [1, 3]')
  if len(faw) == 1:
    faw = cast(Tuple[Callable], faw)
    f, args, kwargs = faw[0], cast(List, []), cast(dict, dict())
  elif len(faw) == 2:
    faw = cast(Tuple[Callable, list], faw)
    f, args, kwargs = faw[0], faw[1], cast(dict, dict())
  else:
    faw = cast(Tuple[Callable, list, dict], faw)
    f, args, kwargs = faw[0], faw[1], faw[2]
  
  passed = None
  value = None
  exception = None
  exception_info = None
  test_count_old = test_count
  passed_count_old = passed_count
  try:
    value = f(*args, **kwargs)
    passed = (value == expectedValue)
  except BaseException as e:
    exception = e
    exception_info = sys.exc_info()
    passed = isinstance(expectedValue, type) and isinstance(exception, expectedValue)
  finally:
    test_count = test_count_old
    passed_count = passed_count_old
  
  test_count += 1
  if passed:
    passed_count += 1
  else:
    print(f'{_describe_test(f, args, kwargs)} failed:')
    print(f'  value = {_repr(value or exception)}')
    print(f'  expectedValue = {_repr(expectedValue)}')
    if exception_info:
      print(f'{RED_COLOR}{"".join(traceback.format_exception(*exception_info)[1:-1])}{NO_COLOR}', end='')

def _repr(x) -> str:
  if not isinstance(x, type):
    return repr(x)
  else:
    return x.__name__

def _describe_test(f: Callable, args: list, kwargs: dict):
  global test_count
  name_string = f.__name__
  args_string = ', '.join(_repr(x) for x in args)
  kwargs_string = (', ' if kwargs else '') + ', '.join(f'{_repr(key)}: {_repr(value)}' for (key, value) in kwargs)
  if isinstance(f, LambdaType):
    return f'#{test_count} {inspect.getsource(f).strip()}'
  else:
    return f'#{test_count} {name_string}({args_string}{kwargs_string})'

def test_stats() -> Tuple[int, int, int]:
  global test_count, passed_count
  failed_count = test_count - passed_count
  return failed_count, passed_count, test_count

def tests_done() -> int:
  failed_count, passed_count, test_count = test_stats()
  print(f'{test_count} tests:')
  print(f'  {passed_count} passed {failed_count} failed')
  tests_reset()
  return failed_count

def tests_reset():
  global test_count, passed_count
  test_count = 0
  passed_count = 0

def main():
  global test_count
  test((int, ), 0)
  test((int, ['11']), 11)
  test((int, ['wtf']), ValueError)
  test((test, ), TypeError)
  test((test, [[]]), TypeError)
  
  test((test, [[int], 0]), None)
  test((lambda: test_count == 6, ), True)
  test((lambda: test_count == 7, ), 1)

if __name__ == '__main__':
  main()
  exit(tests_done())
