import click

def parse_almanac(almanac):
    result = []
    lines = almanac.splitlines()
    seeds = [int(seed.strip()) for seed in lines[0].split(':')[1].strip().split(' ')]
    seeds_ = []
    for i in range(0, len(seeds), 2):
        seeds_.append([seeds[i], seeds[i + 1]])
    seeds = seeds_
    result.append(seeds)
    maps = []
    for line in lines[3:]:
        line = line.strip()
        if len(line) > 0 and not line.strip().endswith('map:'):
            map_ = [int(val.strip()) for val in line.split(' ')]
            maps.append(map_)
        if line.strip().endswith('map:'):
            result.append(maps)
            maps = []
    result.append(maps)
    return result

def calculate_mapping(range_, map_):
    if range_[0] + range_[1] < map_[1]:
        # range fully below map range
        return [], [range_]
    elif range_[0] < map_[1] and range_[0] + range_[1] <= map_[1] + map_[2]:
        # range starts below map range and ends in the middle of map range
        return [[map_[0], range_[0] + range_[1] - map_[1]]], [[range_[0], map_[1] - range_[0]]]
    elif range_[0] <= map_[1] and range_[0] + range_[1] >= map_[1] + map_[2]:
        # range covers map range
        return [[map_[0], map_[2]]], [[range_[0], map_[1] - range_[0]], [map_[1] + map_[2], (range_[0] + range_[1]) - (map_[1] + map_[2])]]
    elif range_[0] >= map_[1] and range_[0] + range_[1] <= map_[1] + map_[2]:
        # range is inside map range
        return [[map_[0] + (range_[0] - map_[1]), range_[1]]], []
    elif range_[0] > map_[1] and range_[0] + range_[1] >= map_[1] + map_[2] and range_[0] < map_[1] + map_[2]:
        # range starts inside map range and ends outside
        return [[map_[0] + (range_[0] - map_[1]), map_[1] + map_[2] - range_[0]]], [[map_[1] + map_[2], range_[0] + range_[1] - (map_[1] + map_[2])]]
    elif range_[0] > map_[1] + map_[2]:
        # range starts above map range
        return [], [range_]

def apply_maps(ranges, maps):
    mappings = []
    for map_ in maps:
        new_ranges = []
        for range_ in ranges:
            m, s = calculate_mapping(range_, map_)
            mappings += m
            new_ranges += s
        ranges = list(new_ranges)
    return mappings + ranges

def calculate_sequences_b(almanac):
    almanac = parse_almanac(almanac)
    result = almanac[0]
    for maps in almanac[1:]:
        result = apply_maps(result, maps)
    return min([r[0] for r in result])

@click.command()
@click.option('-i', '--input', help='Input file')
def main(input):
    with open(input, 'r') as fd:
        data = fd.read()
    result = calculate_sequences_b(data)
    print(result)

if __name__ == '__main__':
    main()
