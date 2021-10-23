from qLib import *

if __name__ == '__main__':
  root_test_suite = test_suites()[0]
  s_test = TestSuite('test()')

  with s_test:
    test(test(True, quiet=True) == True)
    test(root_test_suite.passed == 2, root_test_suite.failed == 0)
    test(test(False, quiet=True) == False)
    if test(root_test_suite.passed == 4, root_test_suite.failed == 1):
      for s in test_suites():
        s.passed += 1
        s.failed -= 1
  with TestSuite('int()'):
    with TestSuite('is_exact()'):
      test(is_exact(0, int()))
      test(is_exact(11, int('11')))
      test(is_exact(3, int('11', base=2)))
    with TestSuite('is_superset()'):
      test(is_superset(0, int()))
      test(is_superset(11, int('11')))
      test(is_superset(3, int('11', base=2)))
  with TestSuite('zig_maybe()'):
    with TestSuite('is_exact()'):
      test(is_exact(zig_maybe(int), 0))
      test(is_exact(zig_maybe(int, ['11']), 11))
      test(is_exact(zig_maybe(int, ['11'], {'base': 2}), 3))
      test(is_exact(zig_maybe(int, ['wtf']), ValueError))
      test(not is_exact(zig_maybe(int, ['wtf']), BaseException))
    with TestSuite('is_superset()'):
      test(is_superset(zig_maybe(int), 0))
      test(is_superset(zig_maybe(int, ['11']), 11))
      test(is_superset(zig_maybe(int, ['11'], {'base': 2}), 3))
      test(is_superset(zig_maybe(int, ['wtf']), ValueError))
      test(is_superset(zig_maybe(int, ['wtf']), BaseException))
  with TestSuite('list()'):
    with TestSuite('is_exact()'):
      test(is_exact([], []))
      test(is_exact([1], [1]))
      test(not is_exact([1], []))
      test(not is_exact([], [1]))
    with TestSuite('is_superset()'):
      test(is_superset([], []))
      test(is_superset([1], [1]))
      test(not is_superset([1], []))
      test(not is_superset([], [1]))
  with TestSuite('dict()'):
    with TestSuite('is_superset()'):
      test(is_superset({}, {}))
      test(is_superset({'a': 1}, {}))
      test(is_superset({'a': 1}, {'a': 1}))
      test(not is_superset({}, {'a': 1}))
    with TestSuite('is_exact()'):
      test(is_exact({}, {}))
      test(is_exact({'a': 1}, {'a': 1}))
      test(not is_exact({'a': 1}, {}))
      test(not is_exact({}, {'a': 1}))
  with s_test:
    test(root_test_suite.passed == 38, root_test_suite.failed == 0)

  tests_summary()

  if len(test_suites()) > 1: exit(-1)
  else: exit(root_test_suite.failed)
