from qLib import *
from contextlib import redirect_stdout

def fail_test():
  with redirect_stdout(None):
    test(False)
  return tests_failed()

if __name__ == '__main__':
  test(tests_passed() == 0, tests_failed() == 0)
  test(0, int)
  test(11, int, ['11'])
  test(3, int, ['11'], {'base': 2})
  test(ValueError, int, ['wtf'])

  test(TypeError, test)
  test(TypeError, test, [])
  test(TypeError, test, ['wtf'])
  test(TypeError, test, [0, 'wtf'])
  test(TypeError, test, [0, int, 'wtf'])

  test(TypeError, test, [0, int, ['0'], 'wtf'])
  test(True)
  test(tests_failed() + 1, fail_test)
  test(True, test, [True])
  test(False, test, [False])

  test(True, lambda: test({}, lambda: {}))
  test(True, lambda: test({}, lambda: {'a': 1}))
  test(False, lambda: test({}, lambda: {'a': 1}, exact=True))
  test(False, lambda: test({'a': 1}, lambda: {}))
  test(True, lambda: test({'a': 1}, lambda: {'a': 1}))

  test(True, lambda: test([], lambda: []))
  test(False, lambda: test([], lambda: [1]))
  test(False, lambda: test([1], lambda: []))
  test(True, lambda: test([1], lambda: [1]))

  test(tests_passed() == 24, tests_failed() == 0)

  tests_summary()

  exit(tests_failed() - 1)
