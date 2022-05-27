from math import remainder
import struct
from qLib.math_ import ilog10, log10, ceil
from qLib.serialize import indexOrMinusOne, DIGITS
from qLib.serialize.int_ import parseInt, printInt

# packed struct f32 { u1 sign, u8 exponent, u23 mantissa }
# exponent (zero/subnormal = 0, normal = 1..254, inf/NaN = 255), stored with bias of 127
# packed struct f64 { u1 sign, u11 exponent, u52 mantissa }
# exponent (zero/subnormal = 0, normal = 1..2046, inf/NaN = 2047), stored with bias of 1023

def significant_base10_digits(mantissa_bits: int) -> int:
    return 1 + ceil(mantissa_bits * log10(2))

def parseFloat(string: str, exponent_bits: int, mantissa_bits: int) -> tuple[float, int]:
    def UNPACK(acc: int) -> float:
        BYTES_COUNT = (1 + exponent_bits + mantissa_bits) // 8
        UNPACK_FORMAT = "f" if BYTES_COUNT == 4 else "d"
        return struct.unpack(UNPACK_FORMAT, acc.to_bytes(BYTES_COUNT, "little"))[0]

    MAX_EXPONENT = (1 << exponent_bits) - 1
    HALF_MAX_EXPONENT = MAX_EXPONENT // 2
    SIGNIFICANT_BASE10_DIGITS = significant_base10_digits(mantissa_bits)
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
        i += 1
        if base10_digits < SIGNIFICANT_BASE10_DIGITS:
            mantissa = mantissa * 10 + j
            base10_digits += 1
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
            i += 1
            if base10_digits < SIGNIFICANT_BASE10_DIGITS:
                fraction = fraction * 10 + j
                base10_digits += 1
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
        exponent = -HALF_MAX_EXPONENT # 0.0

    # base10 exponent
    if (i == 0) or ((i == 1) and string[0] == "-"):
        exponent = 0 # 1.0 by default
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

def printFloat(float_: float, mantissa_bits: int) -> str:
    def PACK(float__: float):
        PACK_FORMAT = "f" if (mantissa_bits == 23) else "d"
        return struct.pack(PACK_FORMAT, float__)

    BYTES_COUNT = 4 if (mantissa_bits == 23) else 8

    # TODO: handle large exponents
    int_ = int(float_)
    negative = PACK(float_)[BYTES_COUNT - 1] >> 7
    sign_string = "-" if negative else ""
    acc_string = sign_string + printInt(abs(int_)) + "."
    acc = -float_ if negative else float_
    while len(acc_string) < negative + (int_ == 0) + 1 + significant_base10_digits(mantissa_bits):
        acc = (acc % 1) * 10
        acc_string += DIGITS[abs(int(acc))]
    # TODO: shift mantissa +- 1?
    return acc_string

def printFloat32(float_: float) -> str:
    return printFloat(float_, 23)

def printFloat64(float_: float) -> str:
    return printFloat(float_, 52)

if __name__ == "__main__":
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
    print()

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
    print()

    print(printFloat32(1.0)) # 1.0000000
    print(printFloat32(-0.0)) # 1.0000000
    print(printFloat32(123.4)) # 123.40000
    print(printFloat32(0.375)) # 0.37500000
    print()

    print(printFloat64(0.0)) # 1.0000000000000000
    print(printFloat64(-0.0)) # 1.0000000000000000
    print(printFloat64(1.0)) # 1.0000000000000000
    print(printFloat64(123.4)) # 123.40000000000000
    print(printFloat64(0.375)) # 0.3750000000000000
    print(printFloat64(0.12345678901234566)) # 0.1234567890123456
    print(printFloat64(-0.12345678901234566)) # -0.1234567890123456
