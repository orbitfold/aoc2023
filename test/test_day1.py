from aoc2023.day1 import parse

def test_day1():
    inputs = ["1abc2", "pqr3stu8vwx", "a1b2c3d4e5f", "treb7uchet"]
    result = parse(inputs)
    assert(result == [12, 38, 15, 77])
    
