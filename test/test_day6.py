from aoc2023.day6_a import parse_input, calculate_winning_times
from aoc2023.day6_b import parse_input_b, calculate_winning_times_b

INPUT = """Time:      7  15   30
Distance:  9  40  200"""

def test_day6_a():
    distances = parse_input(INPUT)
    assert(distances == [[7, 15, 30], [9, 40, 200]])
    assert(calculate_winning_times([7, 9]) == [2, 3, 4, 5])


def test_day6_b():
    distances = parse_input_b(INPUT)
    assert(distances == [71530, 940200])
    times = calculate_winning_times_b(distances)
    import pdb; pdb.set_trace()
