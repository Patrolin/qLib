__all__ = ["test", "run_tests"]

from typing import Callable
from traceback import print_exc
from qLib.vtcodes import TextColor

tests: list[Callable] = []

def test(callback: Callable) -> Callable:
    tests.append(callback)
    return callback

def run_tests():
    passed = 0
    failed = 0
    for test in tests:
        name = f"#{passed + failed + 1} {test.__name__}"
        try:
            test()
            print(f"{TextColor.GREEN}{name} passed{TextColor.RESET}")
            passed += 1
        except Exception:
            print(f"{TextColor.RED}{name} failed:")
            print_exc()
            print(f"{TextColor.RESET}")
            failed += 1

    print(f"    {TextColor.GREEN if failed == 0 else TextColor.RED}tests: {passed} passed {failed} failed{TextColor.RESET}")
    exit(failed)
