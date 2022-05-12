from qLib.tests import test, run_tests
from qLib.math_ import e, tau, tauOver2, tauOver4, phi1, phi2, phi3, phi4

@test
def testMathConstants():
    assert e == 2.718281828459045
    assert tau == 6.283185307179586
    assert tauOver2 == 3.141592653589793
    assert tauOver4 == 1.5707963267948966
    assert phi1 == 1.618033988749895
    assert phi2 == 1.3247179572447458
    assert phi3 == 1.2207440846057596
    assert phi4 == 1.1673039782614185

if __name__ == "__main__":
    run_tests()
