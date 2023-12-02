import click
from aoc2023.day2_a import parse_game

def check_validity(game):
    return [max([cubes[0] for cubes in game]),
            max([cubes[1] for cubes in game]),
            max([cubes[2] for cubes in game])]
    
@click.command()
@click.option('-i', '--input', help='Input file')
def main(input):
    result = 0
    with open(input, 'r') as fd:
        for i, line in enumerate(fd.readlines()):
            parsed = parse_game(line)
            minimum_set = check_validity(parsed)
            power = minimum_set[0] * minimum_set[1] * minimum_set[2]
            result += power
            #if all([r <= 12 and g <= 13 and b <= 14 for r, g, b in parsed]):
            #    id_sum += (i + 1)
    print(result)

if __name__ == '__main__':
    main()
