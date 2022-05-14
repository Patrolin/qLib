from enum import Enum
from typing import NamedTuple

# only top-level groups, no backtracking

class QexMatch(NamedTuple):
    groups: str
    starts: int

class QexNodeType(Enum):
    AND = 0
    OR = 1
    SET = 2
    STRING = 3

class QexNode:
    min: int = 1
    max: int = 1
    nodeType: QexNodeType
    #values: # union

class Qex:
    def __init__(self, qexString: str):
        pass # TODO

    def match(self, string: str) -> list[QexMatch] | None:
        return None # TODO

if __name__ == "__main__":
    print(Qex("a|b"))
