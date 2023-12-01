from aoc import day1_parse

def test_day1:
    inputs = ["1abc2", "pqr3stu8vwx", "a1b2c3d4e5f", "treb7uchet"]
    result = day1_parse(inputs)
    assert(result == [12, 38, 15, 77])
    
