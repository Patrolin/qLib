from qLib import *

@test
def testAssertTrue():
    assert True

if __name__ == "__main__":

    @test
    def testAssertFalse():
        assert False

    @test
    def testIntError():
        int("z")

    run_tests()
