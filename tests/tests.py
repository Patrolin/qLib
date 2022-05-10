from qLib import *

@test
def testPassTest():
    assert True

if __name__ == "__main__":

    @test
    def testFailTest():
        assert False

    @test
    def testIntError():
        int("z")

    run_tests()
