import traceback
from typing import Callable

__all__ = ["test", "run_tests"]

RED_COLOR = "\033[0;31m"
GREEN_COLOR = "\033[0;32m"
NO_COLOR = "\033[0m"

tests: list[Callable] = []

def test(f: Callable):
    tests.append(f)
    return f

def run_tests():
    passed = 0
    failed = 0
    for test in tests:
        name = f"#{passed + failed + 1} {test.__name__}"
        try:
            test()
            print(f"{GREEN_COLOR}{name} passed{NO_COLOR}")
            passed += 1
        except Exception:
            print(f"{RED_COLOR}{name} failed:")
            traceback.print_exc()
            print(f"{NO_COLOR}")
            failed += 1

    print(f"    {GREEN_COLOR if failed == 0 else RED_COLOR}tests: {passed} passed {failed} failed{NO_COLOR}")
    exit(failed)
