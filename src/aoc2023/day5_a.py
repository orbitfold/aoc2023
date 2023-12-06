import click

def parse_almanac(almanac):
    result = []
    lines = almanac.splitlines()
    seeds = [int(seed.strip()) for seed in lines[0].split(':')[1].strip().split(' ')]
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

def calculate_sequences(almanac):
    result = {}
    parsed_almanac = parse_almanac(almanac)
    for seed in parsed_almanac[0]:
        current_value = seed
        for maps in parsed_almanac[1:]:
            for map_ in maps:
                if map_[1] <= current_value < (map_[1] + map_[2]):
                    current_value = map_[0] + (current_value - map_[1])
                    break
            try:
                result[seed].append(current_value)
            except KeyError:
                result[seed] = [current_value]
    return result

@click.command()
@click.option('-i', '--input', help='Input file')
def main(input):
    with open(input, 'r') as fd:
        data = fd.read()
    sequences = calculate_sequences(data)
    print(min([sequences[key][-1] for key in sequences]))

if __name__ == '__main__':
    main()
