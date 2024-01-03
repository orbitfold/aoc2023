import click
import numpy as np

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
    count = 0
    #min_x = 7
    #max_x = 27
    #min_y = 7
    #max_y = 27
    min_x = 200000000000000
    max_x = 400000000000000
    min_y = 200000000000000
    max_y = 400000000000000
    for i, eq1 in enumerate(puzzle[:-1]):
        for j, eq2 in enumerate(puzzle[i + 1:]):
            x1, y1, z1 = eq1[0]
            dx1, dy1, dz1 = eq1[1]
            x2, y2, z2 = eq2[0]
            dx2, dy2, dz2 = eq2[1]
            a = np.array([[dx1, -dx2], [dy1, -dy2]])
            b = np.array([x2 - x1, y2 - y1])
            try:
                t1, t2 = np.linalg.solve(a, b)
                x_ = x1 + dx1 * t1
                y_ = y1 + dy1 * t1
                if (t1 >= 0.0) and (t2 >= 0.0) and (min_x <= x_ <= max_x) and (min_y <= y_ <= max_y):
                    #print(eq1, eq2, t1, t2, x1 + dx1 * t1, y1 + dx1 * t1, x2 + dx2 * t2, y2 + dy2 * t2)
                    count += 1
            except np.linalg.LinAlgError:
                pass
            
    print(count)
            
if __name__ == '__main__':
    main()
