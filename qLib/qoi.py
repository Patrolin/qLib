__all__ = ["decode_qoi"]

def u32(R: int, G: int, B: int, A: int) -> int:
    return (R << 24) + (G << 16) + (B << 8) + A

def RGBA(u32: int) -> tuple[int, int, int, int]:
    R = u32 >> 24
    G = (u32 >> 16) & 0xff
    B = (u32 >> 8) & 0xff
    A = u32 & 0xff
    return (R, G, B, A)

class QoiImage:
    MAGIC = b"qoif"

    def __init__(self, width: int, height: int, isLinear: bool):
        self.data = [0] * (width * height)
        self.width = width
        self.height = height
        self.isLinear = isLinear

    def print(self, x: int, y: int, n: int):
        print(f"-- {x} {y} --")
        for j in range(n):
            i = y * self.width + x + j
            print(RGBA(self.data[i]) if i < len(self.data) else None)

    def encode(self):
        pass # TODO

def decode_u32(v: bytes) -> int:
    return u32(v[0], v[1], v[2], v[3])

def decode_qoi(path: str) -> QoiImage:
    with open(path, "rb") as f:
        # header
        assert f.read(4) == QoiImage.MAGIC
        width = decode_u32(f.read(4))
        height = decode_u32(f.read(4))
        channels = f.read(1)[0]
        colorSpace = f.read(1)[0]
        print(width, height, channels, colorSpace)
        # data
        acc = QoiImage(width, height, colorSpace == 1)
        seen_pixels = [0] * 64
        R, G, B, A = 0, 0, 0, 255
        i = 0
        while i < len(acc.data):
            byte = f.read(1)[0]
            print(byte == 0xff, byte == 0xfe, byte >> 6)
            if byte == 0xff:
                R = f.read(1)[0]
                G = f.read(1)[0]
                B = f.read(1)[0]
                A = f.read(1)[0]
                #print(0xff, i, (R, G, B, A))
            elif byte == 0xfe:
                R = f.read(1)[0]
                G = f.read(1)[0]
                B = f.read(1)[0]
                #print(0xfe, i, (R, G, B, A))
            else:
                twoTag = byte >> 6
                if twoTag == 0b00:
                    R, G, B, A = RGBA(seen_pixels[byte & 0x3f])
                    #print(twoTag, i, byte, RGBA(pixel), (R, G, B, A))
                elif twoTag == 0b01:
                    dR = ((byte >> 4) & 0x03) - 2
                    dG = ((byte >> 2) & 0x03) - 2
                    dB = (byte & 0x03) - 2
                    R = (R + dR) & 0xff
                    G = (G + dG) & 0xff
                    B = (B + dB) & 0xff
                    #print(twoTag, i, byte, (dR, dG, dB), (R, G, B, A))
                elif twoTag == 0b10:
                    dG = (byte & 0x3f) - 32
                    byte = f.read(1)[0]
                    dRdG = (byte >> 4) - 8
                    dBdG = (byte & 0x0f) - 8
                    R = (R + dRdG + dG) & 0xff
                    G = (G + dG) & 0xff
                    B = (B + dBdG + dG) & 0xff
                    #print(twoTag, i, byte, (dG, dRdG, dBdG), (R, G, B, A))
                else:
                    n = (byte & 0x3f) + 1
                    for j in range(n):
                        acc.data[i + j] = u32(R, G, B, A)
                    #print(twoTag, f"{i}-{i+n-1}")
                    i += n
                    continue
            seen_pixels[(R * 3 + G * 5 + B * 7 + A * 11) & 0x3f] = u32(R, G, B, A)
            acc.data[i] = u32(R, G, B, A)
            i += 1
        #acc.print(0, 0, 16)
        #acc.print(0, 255, 256)
    return acc
