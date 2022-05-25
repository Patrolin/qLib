import struct

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
    while True:
        if i >= len(string):
            break
        if string[i] == "_":
            i += 1
            continue
        j = indexOrMinusOne(DIGITS[:base], string[i])
        if j < 0:
            break
        acc = acc * base + j
        i += 1
    return acc, i

def parseFloat32(string: str) -> tuple[float, int]:
    acc = 0x00_00_00_00
    exponent = 0 # exponent (zero/subnormal = 0, normal = 1..254, inf/NaN = 255), exponent_byte = exponent - 127
    integer = 0
    fraction = 0
    i = 0
    if i < len(string) and string[i] == "-":
        acc ^= 0x80_00_00_00
        i += 1
    base10_digits = 0
    while True:
        if i >= len(string):
            break
        j = indexOrMinusOne(DIGITS[:10], string[i])
        if j < 0:
            break
        if base10_digits < 7:
            integer = integer * 10 + j
            base10_digits += 1
        i += 1

    while integer < 2**23:
        integer = (integer << 1) # TODO: what
    if i < len(string) and string[i] == ".":
        i += 1
        while True:
            if i >= len(string):
                break
            j = indexOrMinusOne(DIGITS[:10], string[i])
            if j < 0:
                break
            if base10_digits < 7:
                fraction = fraction * 10 + j
                base10_digits += 1
            i += 1
    while integer < 2**23:
        bit = 0 # TODO: fractional bits
        fraction = (fraction << 1)
        integer = (integer << 1) + bit

    print(acc, exponent, integer)
    acc = acc + ((exponent + 127) << 23) + (integer & 0x7f_ff_ff)
    return struct.unpack("f", acc.to_bytes(4, "little"))[0], i

def parseString(string: str) -> tuple[str, int]:
    if len(string) == 0 or string[0] != "\"":
        return "", 0
    acc = ""
    i = 1
    while True:
        if i >= len(string):
            return acc, -i
        if string[i] == "\\":
            if i + 1 >= len(string):
                return acc, -i
            if string[i + 1] == "u":
                c, j = parseInt(string[i + 2:i + 6], base=16)
                if j != 4:
                    return acc, -i - j - 1
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

if __name__ == "__main__":
    print(parseInt("123a"))
    print(parseFloat32("1"))
    print(parseFloat32("1456"))
    print(parseFloat32("1.25"))
    print(parseString("\"12345.7\\u012"))
    print(parseString("\"12345.7\""))
    print(parseString("\"123\\\"45.7\""))
