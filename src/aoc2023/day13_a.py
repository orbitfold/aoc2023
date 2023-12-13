import click
import numpy as np

def find_smudge(arr):
    original_reflection = find_reflection(arr)
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            copy_arr = np.array(arr)
            if arr[i][j] == '#':
                copy_arr[i][j] = '.'
            elif arr[i][j] == '.':
                copy_arr[i][j] = '#'
            new_reflection = find_reflection(copy_arr)
            if new_reflection is not None and new_reflection != original_reflection:
                return new_reflection

def find_reflection(arr):
    for i in range(1, arr.shape[1]):
        a, b = np.hsplit(arr, [i])
        if a.shape[1] > b.shape[1]:
            _, a = np.hsplit(a, [a.shape[1] - b.shape[1]])
        elif a.shape[1] < b.shape[1]:
            b, _ = np.hsplit(b, [a.shape[1]])
        if np.all(a == np.fliplr(b)):
            return 1, i
    for i in range(1, arr.shape[0]):
        a, b = np.vsplit(arr, [i])
        if a.shape[0] > b.shape[0]:
            _, a = np.vsplit(a, [a.shape[0] - b.shape[0]])
        elif a.shape[0] < b.shape[0]:
            b, _ = np.vsplit(b, [a.shape[0]])
        if np.all(a == np.flipud(b)):
            return 0, i

@click.command()
@click.option('-i', '--input-file', help='Input file')
def main(input_file):
    puzzle_input = []
    with open(input_file, 'r') as fd:
        table = []
        for line in fd:
            if line.strip() == '':
                puzzle_input.append(np.array(table))
                table = []
            else:
                table.append(list(line.strip()))
        puzzle_input.append(np.array(table))
    row_sum = 0
    col_sum = 0
    for table in puzzle_input:
        axis, index = find_reflection(table)
        if axis == 0:
            row_sum += index
        elif axis == 1:
            col_sum += index
    print(row_sum * 100 + col_sum)
    print(row_sum, col_sum)

if __name__ == '__main__':
    main()
