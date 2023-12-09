import click

class Interval:
    def __init__(self, start, n):
        self.start = start
        if n < 0:
            self.n = 0
        else:
            self.n = n

    def __eq__(self, other):
        if self.n == 0 and other.n == 0:
            return True
        elif self.start == other.start and self.n == other.n:
            return True
        else:
            return False

    def __add__(self, x):
        return Interval(self.start + x, self.n)

    def __sub__(self, x):
        return Interval(self.start - x, self.n)

    def __and__(self, other):
        a1 = self.start
        b1 = self.start + self.n
        a2 = other.start
        b2 = other.start + other.n
        return Interval(max(a1, a2), min(b1, b2) - max(a1, a2))

    def __xor__(self, other):
        a1 = self.start
        b1 = self.start + self.n
        a2 = other.start
        b2 = other.start + other.n
        points = sorted([a1, b1, a2, b2])
        return Interval(points[0], points[1] - points[0]), Interval(points[2], points[3] - points[2])

    def __repr__(self):
        return f"Interval({self.start}, {self.n})"

class Mapping:
    def __init__(self, dst, src, n):
        self.dst = dst
        self.src = src
        self.n = n

    def __call__(self, interval):
        return (interval + (self.dst - self.src)) & Interval(self.dst, self.n)

    def __repr__(self):
        return f"Mapping({self.dst}, {self.src}, {self.n})"

def parse_almanac(almanac):
    result = []
    lines = almanac.splitlines()
    seeds = [int(seed.strip()) for seed in lines[0].split(':')[1].strip().split(' ')]
    seeds_ = []
    for i in range(0, len(seeds), 2):
        seeds_.append(Interval(seeds[i], seeds[i + 1]))
    seeds = seeds_
    result.append(seeds)
    maps = []
    for line in lines[3:]:
        line = line.strip()
        if len(line) > 0 and not line.strip().endswith('map:'):
            map_ = [int(val.strip()) for val in line.split(' ')]
            maps.append(Mapping(map_[0], map_[1], map_[2]))
        if line.strip().endswith('map:'):
            result.append(maps)
            maps = []
    result.append(maps)
    return result

def calculate_mapping(interval, mapping):
    r = mapping(interval)
    a, b = Interval(mapping.src, mapping.n) ^ interval
    return r, a & interval, b & interval

def remove_empty_intervals(lst):
    result = []
    for interval in lst:
        if interval != Interval(0, 0):
            result.append(interval)
    return result

def apply_maps(ranges, maps):
    mappings = []
    for map_ in maps:
        new_ranges = []
        for range_ in ranges:
            r, a, b = calculate_mapping(range_, map_)
            mappings += [r]
            new_ranges += [a, b]
        ranges = remove_empty_intervals(list(new_ranges))
    mappings = remove_empty_intervals(mappings)
    return mappings + ranges

def calculate_sequences_b(almanac):
    almanac = parse_almanac(almanac)
    result = almanac[0]
    for maps in almanac[1:]:
        print(result)
        result = apply_maps(result, maps)
    return min([r.start for r in result])

@click.command()
@click.option('-i', '--input', help='Input file')
def main(input):
    with open(input, 'r') as fd:
        data = fd.read()
    result = calculate_sequences_b(data)
    print(result)

if __name__ == '__main__':
    main()
