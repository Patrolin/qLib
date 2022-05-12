from enum import Enum
from typing import NamedTuple

# no nested groups, no backtracking

class RegexMatch(NamedTuple):
    groups: str
    starts: int

class RegexNodeType(Enum):
    GROUP = 0
    SET = 1
    OR = 2
    CHARACTER = 3

class Regex:
    def __init__(self, regexString: str):
        pass # TODO

    def match(self, string: str) -> list[RegexMatch] | None:
        return None # TODO

if __name__ == "__main__":
    print(Regex("(a)|(b)"))
