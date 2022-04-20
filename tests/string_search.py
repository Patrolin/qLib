from qLib import *

@test
def testStringSimilarity():
    assert string_similarity("app", "no") == 0.0
    assert string_similarity("app", "orange") == 0.10686629932510841
    assert string_similarity("app", "pineapple") == 0.26712224516570116
    assert string_similarity("app", "apole") == 0.31066746727980593
    assert string_similarity("app", "apple") == 0.682679419970128
    assert filter_options("y_", ["x", "x_index", "y", "y_index"]) == ["y", "y_index", "x_index"]

if __name__ == "__main__":
    run_tests()
