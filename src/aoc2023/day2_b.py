import click
from aoc2023.day2_a import parse_game

def check_validity(game):
    pass
    
@click.command()
@click.option('-i', '--input', help='Input file')
def main(input):
    id_sum = 0
    with open(input, 'r') as fd:
        for i, line in enumerate(fd.readlines()):
            parsed = parse_game(line)
            if all([r <= 12 and g <= 13 and b <= 14 for r, g, b in parsed]):
                id_sum += (i + 1)
    print(id_sum)

if __name__ == '__main__':
    main()
