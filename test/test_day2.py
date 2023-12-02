from aoc2023.day2_a import parse_game

INPUT = [
    "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
    "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
    "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red"
    "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red"
    "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"
]

def test_day2():
    result = parse_game(INPUT)
    assert(result[0] == [[4, 0, 3], [1, 2, 6], [0, 2, 0]])
    assert(result[1] == [[0, 2, 1], [1, 3, 4], [1, 1, 1]])
    assert(result[2] == [[20, 8, 6], [4, 13, 5], [1, 5, 0]])
    assert(result[3] == [[3, 1, 6], [6, 3, 0], [14, 3, 15]])
    assert(result[4] == [[6, 3, 1], [1, 2, 2]])
