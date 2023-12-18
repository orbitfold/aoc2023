import click
import numpy as np
import sys

DIRECTIONS = {
    0: (0, 1),
    2: (0, -1),
    3: (-1, 0),
    1: (1, 0)
}

def execute_commands(puzzle):
    vertices = []
    position = (0, 0)
    for line in puzzle:
        direction = DIRECTIONS[int(line[2][-1])]
        distance = int(line[2][1:-1], 16)
        vertices.append(position)
        position = (position[0] + direction[0] * distance, position[1] + direction[1] * distance)
    a = min([v[0] for v in vertices])
    b = min([v[1] for v in vertices])
    return [(v[0] - a, v[1] - b) for v in vertices]

def path_length(vertices):
    vertices = vertices + [vertices[0]]
    length = 0
    for v1, v2 in zip(vertices[:-1], vertices[1:]):
        length += abs(v1[0] - v2[0]) + abs(v1[1] - v2[1])
    return length

def shoelace(vertices):
    vertices = vertices + [vertices[0]]
    result = 0
    for v1, v2 in zip(vertices[:-1], vertices[1:]):
        result += (v1[0] + v2[0]) * (v1[1] - v2[1])
    return result / 2

@click.command()
@click.option('-i', '--input-file', help='Input file')
def main(input_file):
    sys.setrecursionlimit(1000000)
    puzzle = []
    with open(input_file, 'r') as fd:
        raw_data = fd.read()
        for line in raw_data.splitlines():
            d, n, c = line.split()
            puzzle.append((d.strip(), int(n.strip()), c.strip()[1:-1]))
    result = execute_commands(puzzle)
    length = path_length(result)
    result = shoelace(result)
    print(result + length / 2 + 1)

if __name__ == '__main__':
    main()
