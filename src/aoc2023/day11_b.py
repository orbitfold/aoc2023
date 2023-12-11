import click
import numpy as np

INCREASE = 999999

@click.command()
@click.option('-i', '--input-file', help='Input file')
def main(input_file):
    with open(input_file, 'r') as fd:
        raw_data = fd.read()
        raw_data = [list(line.strip()) for line in raw_data.splitlines()]
    data = np.array(raw_data)
    ones = np.zeros(data.shape)
    ones[data == '#'] = 1
    add_row = []
    add_col = []
    for i, row in enumerate(ones):
        if not any(row == 1):
            add_row.append(i)
    for j, col in enumerate(ones.transpose()):
        if not any(col == 1):
            add_col.append(j)
    coords = np.where(ones == 1)
    result = 0.
    for i in range(coords[0].shape[0]):
        for j in range(coords[0].shape[0]):
            if i < j:
                rows_between = len([r for r in add_row if min(coords[0][i], coords[0][j]) < r < max(coords[0][i], coords[0][j])])
                cols_between = len([c for c in add_col if min(coords[1][i], coords[1][j]) < c < max(coords[1][i], coords[1][j])])
                d_row = np.abs(coords[0][i] - coords[0][j]) + rows_between * INCREASE
                d_col = np.abs(coords[1][i] - coords[1][j]) + cols_between * INCREASE
                print(f"({coords[0][i]}, {coords[1][i]}) -> ({coords[0][j]}, {coords[1][j]}) {rows_between}, {cols_between}")
                result += d_row + d_col
    print(result)

if __name__ == '__main__':
    main()
