import click
import numpy as np

def parse_input_b(input_):
    puzzle = input_.splitlines()
    time = int("".join([t.strip() for t in puzzle[0].split(':')[1].strip().split()]))
    distance = int("".join([d.strip() for d in puzzle[1].split(':')[1].strip().split()]))
    return [time, distance]

def calculate_winning_times_b(p):
    return [np.ceil((-p[0] + np.sqrt(p[0] ** 2 - 4 * p[1])) / -2.),
            np.floor((-p[0] - np.sqrt(p[0] ** 2 - 4 * p[1])) / -2.)]

@click.command()
@click.option('-i', '--input', help='Input file')
def main(input):
    with open(input, 'r') as fd:
        puzzle = parse_input_b(fd.read())
    result = calculate_winning_times_b(puzzle)
    print(result)
    print(int(result[1] - result[0]))

if __name__ == '__main__':
    main()
