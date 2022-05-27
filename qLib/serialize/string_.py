from qLib.serialize.int_ import parseInt

def parseString(string: str) -> tuple[str, int]:
    if len(string) == 0 or string[0] != "\"":
        return "", 0
    acc = ""
    i = 1
    while i < len(string):
        if string[i] == "\\":
            i += 1
            if i >= len(string):
                break
            if string[i] == "u":
                i += 1
                c, j = parseInt(string[i:i + 4], base=16)
                if j != 4:
                    break
                acc += chr(c)
                i += j
            else:
                acc += string[i]
                i += 1
        elif string[i] == "\"":
            return acc, i + 1
        else:
            acc += string[i]
            i += 1
    return acc, -i

def printString(string: str) -> str:
    return f"\"{string}\""

if __name__ == "__main__":
    print(parseString("\"234.6\"")) # 234.6
    print(parseString("\"234\\\"78.0\"")) # 234"78.0
    print(parseString("\"234.6\\u9012")) # 234.6递
    print(parseString("\"234.6\\u901")) # 234.6
