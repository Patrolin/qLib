from qLib import *

@test
def testParseInt():
    assert parseInt("a")[1] == 0
    assert parseInt("0") == (0, 1)
    assert parseInt("000") == (0, 3)
    assert parseInt("123") == (123, 3)
    assert parseInt("123a") == (123, 3)
    assert parseInt("1012", base=2) == (5, 3)
    assert parseInt("1a", base=16) == (26, 2)

@test
def testPrintInt():
    assert printInt(0) == "0"
    assert printInt(123) == "123"
    assert printInt(-34) == "-34"

@test
def testParseString():
    assert parseString("")[1] == 0
    assert parseString("abc")[1] == 0
    assert parseString("\"")[1] == -1
    assert parseString("\"abc")[1] == -4
    assert parseString("\"abc\"") == ("abc", 5)
    assert parseString("\"hello world\"") == ("hello world", 13)

@test
def testPrintString():
    assert printString("") == "\"\""
    assert printString("hello world") == "\"hello world\""
