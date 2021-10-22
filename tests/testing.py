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
  test(True, test, [True])
  test(False, test, [False])
  test(tests_failed() + 1, fail_test)

  test(tests_passed() == 15, tests_failed() == 0)

  tests_summary()

  exit(tests_failed() - 1)
