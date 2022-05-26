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
        acc = acc * base + j # TODO: saturate on overflow
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
    # sign
    if i < len(string) and string[i] == "-":
        acc ^= 0x80_00_00_00
        i += 1

    # integer
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

    # zero
    if integer == 0:
        exponent = -127
    if i == 0:
        exponent = 0
        integer = 0
    #print("integer part:   ", string, f"{acc + ((exponent + 127) << 23) + (integer & 0x7f_ff_ff):032b}")

    # fraction
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
    for j in range(1, integer_offset + 1):
        fraction = fraction << 1
        bit = (fraction >= divisor)
        fraction -= bit * divisor
        integer += bit << (integer_offset - j)
    acc = acc + ((exponent + 127) << 23) + (integer & 0x7f_ff_ff)
    acc_float = struct.unpack("f", acc.to_bytes(4, "little"))[0]
    #print("fractional part:", string, f"{acc:032b}", acc_float)

    # base10 exponent
    if i < len(string) and string[i] == "e":
        i += 1
        base10_exponent_sign = 1
        if i < len(string) and string[i] == "-":
            i += 1
            base10_exponent_sign = -1
        base10_exponent, j = parseInt(string[i:])
        if j > 0:
            i += j
            acc_float *= 10.0**(base10_exponent_sign * base10_exponent)
        else:
            return acc_float, -i

    return acc_float, i

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
    print(parseString("\"12345.7\"")) # "12345.7"
    print(parseString("\"123\\\"45.7\"")) # "123\"45.7"
    print(parseString("\"12345.7\\u0123")) # "12345.7ģ"
    print(parseString("\"12345.7\\u012")) # "12345.7"
    print(parseInt("1234a")) # 1234
    print(parseFloat32("1")) # 1.0
    print(parseFloat32("1.")) # 1.0
    print(parseFloat32("1.0")) # 1.0
    print(parseFloat32("0")) # 0.0
    print(parseFloat32("0.")) # 0.0
    print(parseFloat32("0.0")) # 0.0
    print(parseFloat32("e2")) # 100.0
    print(parseFloat32("1234")) # 1234.0
    print(parseFloat32("1.34")) # 1.3399999141693115
    print(parseFloat32("1.34e2")) # 133.99999141693115
