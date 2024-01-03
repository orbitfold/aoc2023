import click
import numpy as np
from sympy import symbols, solve

@click.command()
@click.option('-i', '--input-file', help='Input file')
def main(input_file):
    puzzle = []
    with open(input_file, 'r') as fd:
        for line in fd.readlines():
            pos, vel = line.split('@')
            pos = pos.strip()
            vel = vel.strip()
            pos = [int(val) for val in pos.split(',')]
            vel = [int(val) for val in vel.split(',')]
            puzzle.append((pos, vel))
    eqset = []
    x, y, z = symbols('x, y, z')
    dx, dy, dz = symbols('dx, dy, dz')
    for i, eq in enumerate(puzzle[:3]):
        ti = symbols(f"t{i}")
        eqset.append(x + dx * ti - eq[1][0] * ti - eq[0][0])
        eqset.append(y + dy * ti - eq[1][1] * ti - eq[0][1])
        eqset.append(z + dz * ti - eq[1][2] * ti - eq[0][2])
    print solve(eqset)
            
if __name__ == '__main__':
    main()
