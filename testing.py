from typing import *
import sys
import traceback

RED_COLOR = '\033[0;31m'
NO_COLOR = '\033[0m'

def tessert(condition: bool, exception: str):
  if not condition:
    raise TypeError(exception)

test_count = 0
passed_count = 0
def test(faw: Union[Tuple[Callable], Tuple[Callable, list], Tuple[Callable, list, dict]], expectedValue):
  global test_count, passed_count
  tessert(isinstance(faw, (list, tuple)), 'faw must be a list or tuple')
  tessert(1 <= len(faw) <= 3, 'faw must have len(faw) in [1, 3]')
  f = faw[0]
  if len(faw) >= 2:
    args = faw[1]
  else:
    args = []
  if len(faw) == 3:
    kwargs = faw[2]
  else:
    kwargs = dict()
  tessert(isinstance(f, Callable), 'f must be a function')
  tessert(isinstance(args, (list, tuple)), 'args must be a list or tuple')
  tessert(isinstance(kwargs, dict), 'kwargs must be a dict')

  passed = None
  value = None
  exception = None
  exception_info = None
  try:
    value = f(*args, **kwargs)
    passed = (value == expectedValue)
  except BaseException as e:
    exception = e
    exception_info = sys.exc_info()
    passed = isinstance(expectedValue, type) and isinstance(exception, expectedValue)

  test_count += 1
  if passed:
    passed_count += 1
    #print(f'{_describe_test(f, args, kwargs)} passed')
  else:
    print(f'{_describe_test(f, args, kwargs)} failed:')
    print(f'  value = {_repr(value or exception)}')
    print(f'  expectedValue = {_repr(expectedValue)}')
    if exception_info:
      print(f'{RED_COLOR}{"".join(traceback.format_exception(*exception_info)[1:-1])}{NO_COLOR}', end='')

def _repr(x: any) -> str:
  if not isinstance(x, type):
    return repr(x)
  else:
    return x.__name__

def _describe_test(f: Callable, args: list, kwargs: dict):
  global test_count
  tessert(isinstance(f, Callable), 'f must be a function')
  tessert(isinstance(args, (list, tuple)), 'args must be a list or tuple')
  tessert(isinstance(kwargs, dict), 'kwargs must be a dict')
  name_string = f.__name__
  args_string = ', '.join(_repr(x) for x in args)
  kwargs_string = (', ' if kwargs else '') + ', '.join(f'{_repr(key)}: {_repr(value)}' for (key, value) in kwargs)
  return f'#{test_count} {name_string}({args_string}{kwargs_string})'

def tests_done():
  global test_count, passed_count
  failed_count = test_count - passed_count
  print(f'{test_count} tests:')
  print(f'  {passed_count} passed {failed_count} failed')
  test_count = 0
  passed_count = 0

if __name__ == '__main__':
  test((int, []), 0)
  test((int, ['11']), 11)
  test((int, ['wtf']), ValueError)
  test((test, []), TypeError)
  test((test, [[], 0]), TypeError)
  test((test, [['wtf'], 0]), TypeError)
  test((test, [[int, 'wtf'], 0]), TypeError)
  test((test, [[int, [], 'wtf'], 0]), TypeError)
  test((test, [[int], 0]), None)
  tests_done()
