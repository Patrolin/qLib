__all__ = ["test", "run_tests"]

from types import FrameType
from typing import Callable, NamedTuple, cast
from traceback import print_exc
from qLib.vtcodes import TextColor
from inspect import currentframe, getframeinfo
import inspect
from os.path import basename

class Test(NamedTuple):
    f: Callable
    file_name: str

tests: list[Test] = []

def test(callback: Callable) -> Callable:
    current_frame = cast(FrameType, currentframe())
    caller_frame = cast(FrameType, current_frame.f_back)
    file_path, *_ = getframeinfo(caller_frame)
    file_name = basename(file_path)
    tests.append(Test(callback, file_name))
    return callback

def run_tests():
    passed = 0
    failed = 0
    for test in tests:
        name = f"#{passed + failed + 1} {test.file_name}/{test.f.__name__}"
        try:
            test.f()
            print(f"{TextColor.GREEN}{name} passed{TextColor.RESET}")
            passed += 1
        except Exception:
            print(f"{TextColor.RED}{name} failed:")
            print_exc()
            print(f"{TextColor.RESET}")
            failed += 1

    print(f"    {TextColor.GREEN if failed == 0 else TextColor.RED}{passed} passed {failed} failed{TextColor.RESET}")
    exit(failed)
