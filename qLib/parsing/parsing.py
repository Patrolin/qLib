import struct
from qLib.math_ import ilog10

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

# struct float32 { u1 sign, u8 exponent, u23 mantissa }
# exponent (zero/subnormal = 0, normal = 1..254, inf/NaN = 255), stored with bias of 127
def parseFloat32(string: str) -> tuple[float, int]:
    # TODO: zero/subnormal, inf/NaN, 1e10 scientific notation
    acc = 0x00_00_00_00
    exponent = 0
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
    exponent_offset = integer.bit_length() - 1
    integer_offset = 23 - exponent_offset
    exponent += exponent_offset
    integer = integer << integer_offset
    #print("integer part:   ", string, f"{acc + ((exponent + 127) << 23) + (integer & 0x7f_ff_ff):032b}")

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
    divisor = 10**ilog10(fraction)
    #print("integer_offset:", integer_offset, divisor)
    for j in range(1, integer_offset + 1):
        #print("fraction:", fraction, fraction << 1, int(fraction >= divisor), (fraction << 1) - (fraction >= divisor) * divisor)
        fraction = fraction << 1
        bit = (fraction >= divisor)
        fraction -= bit * divisor
        integer += bit << (integer_offset - j)
    #print("fractional part:", string, f"{acc + ((exponent + 127) << 23) + (integer & 0x7f_ff_ff):032b}")

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
