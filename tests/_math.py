from qLib import *

@test
def testConstants():
    assert e == 2.718281828459045
    assert tau == 6.283185307179586
    assert half_tau == 3.141592653589793
    assert quarter_tau == 1.5707963267948966
    assert phi1 == 1.618033988749895
    assert phi2 == 1.3247179572447458
    assert phi3 == 1.2207440846057596
    assert phi4 == 1.1673039782614185

if __name__ == "__main__":
    run_tests()
