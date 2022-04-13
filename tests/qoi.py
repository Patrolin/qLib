from qLib import *
from os import path

@test
def testDecodeQoi():
    read_qoi(relative_path(__file__, "/data/fishWater.qoi"), True)

@test
def testEncodeQoi():
    image = read_qoi(relative_path(__file__, "/data/fishWater.qoi"))
    write_qoi(relative_path(__file__, "/data/fishWaterCopy.qoi"), image)
    imageCopy = read_qoi(relative_path(__file__, "/data/fishWaterCopy.qoi"))
    for y in range(image.height):
        for x in range(image.width):
            i = y * image.width + x
            assert imageCopy.data[i] == image.data[i], f"{x} {y}"

if __name__ == "__main__":
    run_tests()
