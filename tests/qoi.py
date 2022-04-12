from qLib import *
from os import path

@test
def testDecodeQoi():
    decode_qoi(relative_path(__file__, "/data/fish_umbrella_stone.qoi"))

if __name__ == "__main__":
    run_tests()
