from aoc2023.day1 import parse, parse_adv

def test_day1():
    inputs = ["1abc2", "pqr3stu8vwx", "a1b2c3d4e5f", "treb7uchet"]
    result = parse(inputs)
    assert(result == [12, 38, 15, 77])
    result_adv = parse_adv(inputs)
    assert(result_adv == [29, 83, 13, 24, 42, 14, 76])
