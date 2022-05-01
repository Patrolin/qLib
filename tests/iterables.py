from qLib import *

@test
def testSet():
    set = Set()

    set.add("A")
    assert set.has("A")
    set.add("B")
    assert set.has("B")
    set.add("C")
    assert set.has("C")

    assert set.has("A")
    assert set.has("B")
    assert set.has("C")

    set.remove("A")
    assert not set.has("A")
    assert set.has("B")
    assert set.has("C")

    assert set["B"]
    assert set["C"]

@test
def testMap():
    map = Map()

    map["A"] = 1
    assert map["A"] == 1
    map["B"] = 2
    assert map["B"] == 2
    map["C"] = 3
    assert map["C"] == 3

    assert map.has("A")
    assert map.has("B")
    assert map.has("C")

    map.remove("A")
    assert not map.has("A")
    assert map.has("B")
    assert map.has("C")

    assert map["B"] == 2
    assert map["C"] == 3

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

@test
def testFuzzMap():
    for start in range(0, len(ALPHABET)):
        for end in range(1, len(ALPHABET) + 1):
            sliced_alphabet = ALPHABET[start:end]
            map = Map()
            for c in sliced_alphabet:
                map[c] = ord(c)
            for c in sliced_alphabet:
                if map[c] != ord(c):
                    for i, bucket in enumerate(map.buckets):
                        print(i, bucket)
                    print(c, hash(c) % map.bucket_count)
                assert map[c] == ord(c)

if __name__ == "__main__":
    run_tests()
