from typing import Any, Callable, overload

__all__ = ['test', 'zig_maybe', 'is_exact', 'is_superset', 'tests_summary', 'TestSuite', 'test_suites']

RED_COLOR = '\033[0;31m'
NO_COLOR = '\033[0m'

class TestSuite:
  def __init__(self, name: str):
    self.name = name
    self.passed = 0
    self.failed = 0

  def __enter__(self):
    _test_suites.append(self)
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    if exc_value: raise exc_value
    _test_suites.pop()

_test_suites = [TestSuite('')]

def test_suites():
  return _test_suites

def test(*conditions: bool, quiet: bool = False) -> bool:
  value = conditions
  expected_value = (True, ) * len(value)
  passed = (value == expected_value)

  if passed:
    for s in _test_suites[::-1]:
      s.passed += 1
  else:
    for s in _test_suites[::-1]:
      s.failed += 1
    root_test_suite = _test_suites[0]
    tests_passed = root_test_suite.passed
    tests_failed = root_test_suite.failed
    if not quiet:
      print(f'{".".join(s.name for s in _test_suites[1:])}#{tests_passed + tests_failed} failed:')
      print(f'  value = {_repr(value)}')
      print(f'  expected_value = {_repr(expected_value)}')
  return passed

@overload
def zig_maybe(f: Callable[..., Any]) -> Any | BaseException:
  ...

@overload
def zig_maybe(f: Callable[..., Any], args: list[Any]) -> Any | BaseException:
  ...

@overload
def zig_maybe(f: Callable[..., Any], args: list[Any], kwargs: dict[str, Any]) -> Any | BaseException:
  ...

def zig_maybe(*args):
  if (len(args) > 3) \
    and isinstance(args[0], Callable) \
    and ((len(args) < 2) or isinstance(args[1], list)) \
    and ((len(args) < 3) or isinstance(args[2], dict)):
    raise TypeError()
  f: Callable = args[0]
  _args: list[Any] = args[1] if (len(args) >= 2) else []
  kwargs: dict = args[2] if (len(args) == 3) else dict()
  maybe_value = None
  try:
    maybe_value = f(*_args, **kwargs)
  except BaseException as e:
    maybe_value = e
  return maybe_value

def is_exact(a: Any, b: Any):
  return (a.__class__ == b) or (a == b)

def is_superset(a: Any, b: Any) -> bool:
  if isinstance(b, type):
    return isinstance(a, b) or (a == b)
  if type(a) != type(b): return False
  if isinstance(a, list):
    if len(a) != len(b): return False
    return all(is_superset(a[k], b[k]) for k in range(len(b)))
  elif isinstance(a, dict):
    return all((k in a) and is_superset(a[k], b[k]) for k in b.keys())
  else:
    return a == b

def _repr(obj: object) -> str:
  if isinstance(obj, list):
    return f'[{", ".join(_repr(x) for x in obj)}]'
  if isinstance(obj, Callable):
    return obj.__name__
  return repr(obj)

def tests_summary():
  last_test_suite = _test_suites[-1]
  name = last_test_suite.name if len(_test_suites) > 1 else ''
  tests_passed = last_test_suite.passed
  tests_failed = last_test_suite.failed
  NEWLINE = "\n"
  print(f'{NEWLINE if last_test_suite.failed > 0 else ""}{(name+" ") if name else ""}{tests_passed + tests_failed} tests:')
  print(f'  {tests_passed} passed {tests_failed} failed')
