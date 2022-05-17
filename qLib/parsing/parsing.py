# you only really need top-level groups without backtracking in regex anyway, so you might as well just write the code yourself

def indexOrMinusOne(string: str, substring: str) -> int:
    try:
        return string.index(substring)
    except ValueError:
        return -1

DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"

def parseInt(string: str, base=10) -> tuple[int, int]:
    acc = 0
    i = 0
    for c in string:
        j = indexOrMinusOne(DIGITS[:base], c)
        if j == -1:
            break
        acc = acc * base + j
        i += 1
    return acc, i

def parseString(string: str) -> tuple[str, int]:
    i = 0
    acc = ""
    if i < len(string) and string[i] == "\"":
        i += 1
    else:
        return "", 0
    while i < len(string):
        if string[i] == "\\":
            if i + 1 >= len(string):
                return "", 0
            if string[i + 1] == "u":
                c, j = parseInt(string[i + 2:i + 6], base=16)
                if j != 4:
                    return "", 0
                acc += chr(c)
                i += 6
            else:
                acc += string[i + 1]
                i += 2
        elif string[i] == "\"":
            return acc, i + 1
        else:
            acc += string[i]
            i += 1
    return "", 0 # make compiler happy

def parse_qex(string: str):
    start = 0
    CHARS = "()|+*?"
    while True:
        if start >= len(string):
            break
        i = indexOrMinusOne(CHARS, string[start])
        if i != -1:
            yield i, string[start]
            start += 1
        else:
            j = 1
            while start + j < len(string) and indexOrMinusOne(CHARS, string[start + j]) == -1:
                j += 1
            yield i, string[start:start + j]
            start += j

if __name__ == "__main__":
    print(parseString("\"12345.4\""))
    print(parseString("\"123\\\"45.4\""))
    print(list(parse_qex("(ab)ba|b+?")))
