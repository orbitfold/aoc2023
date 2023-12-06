from aoc2023.day5_a import parse_almanac, calculate_sequences
from aoc2023.day5_b import calculate_mapping, calculate_sequences_b, apply_maps


ALMANAC = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

def test_mappings():
    ranges = [[79, 14], [55, 13]]
    maps = [[50, 98, 2], [52, 50, 48]]
    result = apply_maps(ranges, maps)
    assert(result == [[81, 14], [57, 13]])
    maps = [[0, 15, 37], [37, 52, 2], [39, 0, 15]]
    result = apply_maps(result, maps)
    assert(result == [[81, 14], [57, 13]])
    maps = [[49, 53, 8], [0, 11, 42], [42, 0, 7], [57, 7, 4]]
    result = apply_maps(result, maps)
    assert(result == [[53, 4], [81, 14], [61, 9]])
    maps = [[88, 18, 7], [18, 25, 70]]
    result = apply_maps(result, maps)
    assert(result == [[46, 4], [74, 14], [54, 9]])
    maps = [[45, 77, 23], [81, 45, 19], [68, 64, 13]]
    result = apply_maps(result, maps)
    assert(result == [[45, 11], [82, 4], [90, 9], [78, 3]])
    maps = [[0, 69, 1], [1, 0, 69]]
    result = apply_maps(result, maps)
    assert(result == [[46, 11], [82, 4], [90, 9], [78, 3]])
    maps = [[60, 56, 37], [56, 93, 4]]
    result = apply_maps(result, maps)
    assert(result == [[60, 1], [86, 4], [94, 3], [82, 3], [56, 4], [46, 10], [93, 0], [97, 2]])
    #import pdb; pdb.set_trace()
    #assert(result == [[82, 4], []])
    #import pdb; pdb.set_trace()

def test_day5_a():
    result = parse_almanac(ALMANAC)
    assert(result[0] == [79, 14, 55, 13])
    assert(result[1] == [[50, 98, 2], [52, 50, 48]])
    assert(result[2] == [[0, 15, 37], [37, 52, 2], [39, 0, 15]])
    assert(result[3] == [[49, 53, 8], [0, 11, 42], [42, 0, 7], [57, 7, 4]])
    assert(result[4] == [[88, 18, 7], [18, 25, 70]])
    assert(result[5] == [[45, 77, 23], [81, 45, 19], [68, 64, 13]])
    assert(result[6] == [[0, 69, 1], [1, 0, 69]])
    assert(result[7] == [[60, 56, 37], [56, 93, 4]])
    sequences = calculate_sequences(ALMANAC)
    assert(sequences[79] == [81, 81, 81, 74, 78, 78, 82])
    assert(sequences[14] == [14, 53, 49, 42, 42, 43, 43])
    assert(sequences[55] == [57, 57, 53, 46, 82, 82, 86])
    assert(sequences[13] == [13, 52, 41, 34, 34, 35, 35])

def test_day5_b():
    result = calculate_mapping([0, 10], [2, 5, 10])
    assert(list(result) == [[[2, 5]], [[0, 5]]])
    result = calculate_mapping([0, 10], [2, 5, 4])
    assert(list(result) == [[[2, 4]], [[0, 5], [9, 1]]])
    result = calculate_mapping([5, 3], [2, 0, 10])
    assert(list(result) == [[[7, 3]], []])
    result = calculate_mapping([5, 10], [2, 0, 10])
    assert(list(result) == [[[7, 5]], [[10, 5]]])
    result = calculate_mapping([0, 5], [2, 10, 10])
    assert(list(result) == [[], [[0, 5]]])
    result = calculate_mapping([15, 5], [2, 0, 10])
    assert(list(result) == [[], [[15, 5]]])
    result = calculate_mapping([79, 14], [52, 50, 48])
    assert(list(result) == [[[81, 14]], []])
    result = calculate_mapping([55, 13], [52, 50, 48])
    assert(list(result) == [[[57, 13]], []])
    result = calculate_mapping([57, 13], [49, 53, 8])
    assert(list(result) == [[[53, 4]], [[61, 9]]])
