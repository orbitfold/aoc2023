from aoc2023.day3_a import parse_numbers
from aoc2023.day3_b import find_gears

INPUT = ["467..114..",
         "...*......",
         "..35..633.",
         "......#...",
         "617*......",
         ".....+.58.",
         "..592.....",
         "......755.",
         "...$.*....",
         ".664.598.."]

INPUT2 = ["467..114..",
         "...*......",
         "..35..633.",
         "......#...",
         "617.......",
         ".....+.58.",
         "..592.....",
         "......755.",
         "...$.*....",
         ".664.598.."]


def test_day3_a():
    result = parse_numbers(INPUT)
    assert(result == [467, 35, 633, 617, 592, 755, 664, 598])
    assert(sum(result) == 4361)

def test_day3_a_2():
    result = parse_numbers(INPUT2)
    assert(result == [467, 35, 633, 592, 755, 664, 598])

def test_day3_b():
    result = find_gears(INPUT)
    import pdb; pdb.set_trace()
    assert(result == {(1, 3): [467, 35], (4, 3): [617], (8, 5): [755, 598]})
