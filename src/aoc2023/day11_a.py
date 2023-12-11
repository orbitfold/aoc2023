import click
import numpy as np

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
    ones = np.insert(ones, add_row, np.zeros((len(add_row), ones.shape[1])), 0)
    ones = np.insert(ones, add_col, np.zeros((ones.shape[0], len(add_col))), 1)
    coords = np.where(ones == 1)
    result = 0.
    for i in range(coords[0].shape[0]):
        for j in range(coords[0].shape[0]):
            if i < j:
                result += np.abs(coords[0][i] - coords[0][j]) + np.abs(coords[1][i] - coords[1][j])
    print(result)
    import pdb; pdb.set_trace()

if __name__ == '__main__':
    main()
