def indexOrMinusOne(string: str, substring: str) -> int:
    try:
        return string.index(substring)
    except ValueError:
        return -1

from .int_ import *
