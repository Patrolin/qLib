from typing import *
import sys
import traceback
from contextlib import redirect_stdout

__all__ = ['test', 'tests_conclude', 'tests_passed', 'tests_failed']

RED_COLOR = '\033[0;31m'
NO_COLOR = '\033[0m'

_tests_passed = 0
_tests_failed = 0

def tests_failed() -> int:
  return _tests_failed

def tests_passed() -> int:
  return _tests_passed

@overload
def test(*conditions: bool) -> None:
  ...

@overload
def test(expected_value: Any, f: Callable) -> None:
  ...

@overload
def test(expected_value: Any, f: Callable, args: list[Any]) -> None:
  ...

@overload
def test(expected_value: Any, f: Callable, args: list[Any], kwargs: dict[str, Any]) -> None:
  ...

def test(*_args):
  global _tests_passed, _tests_failed
  passed = None
  value = None
  failed_msg = None
  exception_info = None

  if len(_args) >= 1 and all(isinstance(x, bool) for x in _args):
    value = _args

    expected_value = (True, ) * len(value)
    passed = (value == expected_value)
    failed_msg = f'#{_tests_passed + _tests_failed + 1} failed:'
  elif len(_args) >= 2 and \
      isinstance(_args[1], Callable) and \
      (len(_args) < 3 or isinstance(_args[2], list)) and \
      (len(_args) < 4 or isinstance(_args[3], dict)):
    expected_value = _args[0]
    f: Callable = _args[1]
    args: list[Any] = _args[2] if (len(_args) >= 3) else []
    kwargs: dict = _args[3] if (len(_args) == 4) else dict()

    _tests_passed_old = _tests_passed
    _tests_failed_old = _tests_failed
    with redirect_stdout(None):
      pass
      try:
        sys.stdout = None
        value = f(*args, **kwargs)
        passed = (value == expected_value)
      except BaseException as e:
        value = e
        exception_info = sys.exc_info()
        passed = isinstance(expected_value, type) and isinstance(value, expected_value)
    _tests_passed = _tests_passed_old
    _tests_failed = _tests_failed_old

    name_string = f.__name__
    args_string = ', '.join(_repr(x) for x in args)
    kwargs_string = (', ' if kwargs else '') + ', '.join(f'{_repr(key)}: {_repr(value)}'
                                                         for (key, value) in kwargs.items())
    failed_msg = f'#{_tests_passed + _tests_failed + 1} {name_string}({args_string}{kwargs_string}) failed:'
  else:
    raise TypeError()

  if passed:
    _tests_passed += 1
  else:
    _tests_failed += 1
    print(failed_msg)
    print(f'  value = {_repr(value)}')
    print(f'  expected_value = {_repr(expected_value)}')
    if exception_info:
      print(f'{RED_COLOR}{"".join(traceback.format_exception(*exception_info)[1:-1])}{NO_COLOR}', end='')
  return passed

def _repr(obj: object) -> str:
  if isinstance(obj, list):
    return f'[{", ".join(_repr(x) for x in obj)}]'
  if isinstance(obj, Callable):
    return obj.__name__
  return repr(obj)

def tests_conclude() -> int:
  global failed_count, test_count
  print(f'{_tests_passed + _tests_failed} tests:')
  print(f'  {_tests_passed} passed {_tests_failed} failed')
  return _tests_failed
