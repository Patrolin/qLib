from enum import Enum

def _tokenize(string: str, tokens: str) -> list[str]:
    acc = []
    start = 0
    isEscaped = False
    for i, character in enumerate(string):
        if not isEscaped:
            for token in tokens:
                if character != token: continue
                if i > start:
                    acc.append(string[start:i])
                acc.append(string[i])
                start = i + 1
                break
        isEscaped = (not isEscaped if character == "\\" else False)
    if start != len(string):
        acc.append(string[start:])
    return acc

class RegexNodeType(Enum):
    GROUP = 0
    SET = 1
    OR = 2
    CHARACTER = 3

class HasNoParent(Exception):
    pass

class RegexNode: # TODO: polymorph from nodeType
    def __init__(self, nodeType: RegexNodeType):
        self.nodeType = nodeType
        self.parent: RegexNode | None = None
        self.children: list[RegexNode] = []

    def __repr__(self) -> str:
        if self.nodeType == RegexNodeType.GROUP:
            return f"({''.join(repr(v) for v in self.children)})"
        elif self.nodeType == RegexNodeType.GROUP:
            return f"[{''.join(repr(v) for v in self.children)}]"
        else:
            raise Exception()

    def add(self, newChild):
        newChild.parent = self
        self.children.append(newChild)
        return newChild

    def close(self):
        if self.parent == None: raise HasNoParent()
        return self.parent

def parseRegex(regex: str) -> RegexNode:
    tokens = _tokenize(regex, "()[]|")
    root = RegexNode(RegexNodeType.GROUP)
    current = root
    for token in tokens:
        if token == "(":
            current = current.add(RegexNode(RegexNodeType.GROUP))
        elif token == ")":
            current = current.close()
        elif token == "[":
            current = current.add(RegexNode(RegexNodeType.SET))
        elif token == "]":
            current = current.close()
        elif token == "|":
            current = current.close()
        else:
            current.add()
            print(token)
    return root

# TODO: construct (NFA ->)? DFA -> min-DFA at compile time in O(n^2)?
# or just prevent the creation or execution of Evil Regexes?

if __name__ == "__main__":
    print(parseRegex("(a)|(b)"))
