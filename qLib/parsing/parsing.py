import struct
from time import sleep
from qLib.math_ import ilog10, log10, ceil

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

# packed struct f32 { u1 sign, u8 exponent, u23 mantissa }
# exponent (zero/subnormal = 0, normal = 1..254, inf/NaN = 255), stored with bias of 127
# packed struct f64 { u1 sign, u11 exponent, u52 mantissa }
# exponent (zero/subnormal = 0, normal = 1..2046, inf/NaN = 2047), stored with bias of 1023
def parseFloat(string: str, exponent_bits: int, mantissa_bits: int) -> tuple[float, int]:
    def UNPACK(acc: int) -> float:
        BYTES_COUNT = (1 + exponent_bits + mantissa_bits) // 8
        UNPACK_FORMAT = "f" if BYTES_COUNT == 4 else "d"
        return struct.unpack(UNPACK_FORMAT, acc.to_bytes(BYTES_COUNT, "little"))[0]

    MAX_EXPONENT = (1 << exponent_bits) - 1
    HALF_MAX_EXPONENT = MAX_EXPONENT // 2
    SIGNIFICANT_BASE10_DIGITS = 1 + ceil(mantissa_bits * log10(2))
    MANTISSA_MASK = ~(((0xff_ff_ff_ff_ff_ff_ff_ff << mantissa_bits) & 0xff_ff_ff_ff_ff_ff_ff_ff))

    acc = 0x00_00_00_00_00_00_00_00 # 64b
    i = 0
    # sign
    if i < len(string) and string[i] == "-":
        acc ^= 1 << (exponent_bits + mantissa_bits)
        i += 1

    # infinity
    if (i + 2 < len(string)) and string[i] == "i" and string[i + 1] == "n" and string[i + 2] == "f":
        i += 3
        acc = acc + (MAX_EXPONENT << mantissa_bits) # inf
        acc_float = UNPACK(acc)
        return acc_float, i

    # integer
    exponent = 0
    mantissa = 0
    base10_digits = 0
    while True:
        if i >= len(string):
            break
        j = indexOrMinusOne(DIGITS[:10], string[i])
        if j < 0:
            break
        if base10_digits < SIGNIFICANT_BASE10_DIGITS:
            mantissa = mantissa * 10 + j
            base10_digits += 1
        i += 1
    exponent_offset = max(mantissa.bit_length() - 1, 0)
    integer_offset = mantissa_bits - exponent_offset
    exponent += exponent_offset
    mantissa = mantissa << integer_offset
    #print("integer part:   ", string, f"{acc + ((exponent + HALF_MAX_EXPONENT) << mantissa_bits) + (mantissa & MANTISSA_MASK):032b}")

    # fraction
    fraction = 0
    if i < len(string) and string[i] == ".":
        i += 1
        while True:
            if i >= len(string):
                break
            j = indexOrMinusOne(DIGITS[:10], string[i])
            if j < 0:
                break
            if base10_digits < SIGNIFICANT_BASE10_DIGITS:
                fraction = fraction * 10 + j
                base10_digits += 1
            i += 1
    divisor = 10**ilog10(fraction)
    #print("fraction:", fraction, divisor)
    while integer_offset > 0 and fraction > 0:
        #print(j, integer_offset, fraction << 1, ((fraction << 1) >= divisor), mantissa)
        fraction = fraction << 1
        bit = (fraction >= divisor)
        fraction -= bit * divisor
        if mantissa == 0: # find first non-zero bit
            exponent -= 1
        else: # fill in remaining bits
            integer_offset -= 1
        mantissa += bit << integer_offset

    # zero
    if mantissa == 0:
        exponent = -HALF_MAX_EXPONENT

    # base10 exponent
    if (i == 0) or ((i == 1) and string[0] == "-"):
        exponent = 0
    acc = acc + ((exponent + HALF_MAX_EXPONENT) << mantissa_bits) + (mantissa & MANTISSA_MASK)
    acc_float = UNPACK(acc)
    #print("fractional part:", string, f"{exponent + HALF_MAX_EXPONENT:08b}", f"{mantissa & MANTISSA_MASK:023b}", f"{acc:032b}", acc_float)
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

def parseFloat32(string: str):
    return parseFloat(string, exponent_bits=8, mantissa_bits=23)

def parseFloat64(string: str):
    return parseFloat(string, exponent_bits=11, mantissa_bits=52)

if __name__ == "__main__":
    print(parseInt("1234a")) # 1234

    print(parseString("\"234.6\"")) # "234.6"
    print(parseString("\"234\\\"78.0\"")) # "234\"78.0"
    print(parseString("\"234.6\\u9012")) # "234.6递"
    print(parseString("\"234.6\\u901")) # "234.6"

    print(parseFloat32("inf")) # inf
    print(parseFloat32("-inf")) # -inf
    print(parseFloat32("1")) # 1.0
    print(parseFloat32("1.")) # 1.0
    print(parseFloat32("-1.0")) # -1.0
    print(parseFloat32("0")) # 0.0
    print(parseFloat32("0.")) # 0.0
    print(parseFloat32("-0.0")) # -0.0
    print(parseFloat32("e2")) # 100.0
    print(parseFloat32("-e-2")) # -0.01
    print(parseFloat32("1234")) # 1234.0
    print(parseFloat32("1.34")) # 1.3399999141693115
    print(parseFloat32("1.34e2")) # 133.99999141693115
    print(parseFloat32("0.3")) # 0.29999998211860657
    print(parseFloat32("-0.3")) # -0.29999998211860657

    print(parseFloat64("inf")) # inf
    print(parseFloat64("-inf")) # -inf
    print(parseFloat64("1")) # 1.0
    print(parseFloat64("1.")) # 1.0
    print(parseFloat64("-1.0")) # -1.0
    print(parseFloat64("0")) # 0.0
    print(parseFloat64("0.")) # 0.0
    print(parseFloat64("-0.0")) # -0.0
    print(parseFloat64("e2")) # 100.0
    print(parseFloat64("-e-2")) # -0.01
    print(parseFloat64("1234")) # 1234.0
    print(parseFloat64("1.34")) # 1.3399999999999999
    print(parseFloat64("1.34e2")) # 134
    print(parseFloat64("0.3")) # 0.3
    print(parseFloat64("-0.3")) # -0.3
