import click
import numpy as np
import sys

DIRECTIONS = {
    'R': (0, 1),
    'L': (0, -1),
    'U': (-1, 0),
    'D': (1, 0)
}

def execute_commands(puzzle):
    positions = []
    position = (0, 0)
    for line in puzzle:
        direction = DIRECTIONS[line[0]]
        for _ in range(line[1]):
            positions.append((position, line[2]))
            position = (position[0] + direction[0], position[1] + direction[1])
    a = min([p[0][0] for p in positions])
    b = min([p[0][1] for p in positions])
    return [((p[0][0] - a, p[0][1] - b), p[1]) for p in positions]

def positions_to_array(positions):
    a = max([p[0][0] for p in positions])
    b = max([p[0][1] for p in positions])
    arr = np.zeros((a + 1, b + 1))
    for p in positions:
        arr[*p[0]] = 1
    for i, p in enumerate(positions[1:]):
        prev = positions[i]
        d = (p[0][0] - prev[0][0], p[0][1] - prev[0][1])
        if d == (1, 0):
            left = (p[0][0], p[0][1] - 1)
        elif d == (-1, 0):
            left = (p[0][0], p[0][1] + 1)
        elif d == (0, 1):
            left = (p[0][0] + 1, p[0][1])
        elif d == (0, -1):
            left = (p[0][0] - 1, p[0][1])
        else:
            raise RuntimeError("Some bullshit!")
        flood_fill(arr, left, 1)
    return arr

def flood_fill(arr, start, value):
    if start[0] < 0 or start[1] < 0 or start[0] >= arr.shape[0] or start[1] >= arr.shape[1] or arr[*start] != 0:
        return
    arr[*start] = value
    flood_fill(arr, (start[0] + 1, start[1]), value)
    flood_fill(arr, (start[0] - 1, start[1]), value)
    flood_fill(arr, (start[0], start[1] + 1), value)
    flood_fill(arr, (start[0], start[1] - 1), value)

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
    result = positions_to_array(result)
    import pdb; pdb.set_trace()

if __name__ == '__main__':
    main()
