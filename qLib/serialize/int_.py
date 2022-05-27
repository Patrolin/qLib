from qLib.serialize import indexOrMinusOne

DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"

def parseInt(string: str, base=10) -> tuple[int, int]:
    acc = 0
    i = 0
    while i < len(string):
        if string[i] == "_":
            i += 1
            continue
        j = indexOrMinusOne(DIGITS[:base], string[i])
        if j < 0:
            break
        acc = acc * base + j # TODO: saturate on overflow
        i += 1
    return acc, i

def printInt(int_: int, base=10) -> str:
    if int_ == 0: return "0"
    acc_string = ""
    acc = abs(int_)
    while acc > 0:
        rem = acc % base
        acc_string += DIGITS[rem]
        acc = acc // base
    acc_string_reversed = ""
    for i in range(1, len(acc_string) + 1):
        acc_string_reversed += acc_string[len(acc_string) - i]
    sign = "" if (int_ > 0) else "-"
    return sign + acc_string_reversed

if __name__ == "__main__":
    print(parseInt("1234a")) # 1234
    print(parseInt("003456a")) # 3456
    print(printInt(1234)) # 1234
    print(printInt(-3456)) # 3456
    print(printInt(0)) # 0
