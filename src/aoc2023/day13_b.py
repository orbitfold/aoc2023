import click
import numpy as np

def find_smudge(arr):
    original_reflection = find_reflection(arr)
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            copy_arr = np.copy(arr)
            if arr[i][j] == '#':
                copy_arr[i][j] = '.'
            elif arr[i][j] == '.':
                copy_arr[i][j] = '#'
            else:
                raise RuntimeError("Invalid input!")
            new_reflection = find_reflection(copy_arr, old_reflection=original_reflection)
            if new_reflection != (None, None) and new_reflection != original_reflection:
                return new_reflection
    return original_reflection

def find_reflection(arr, old_reflection=None):
    vertical = None
    horizontal = None
    arr = np.copy(arr)
    for i in range(1, arr.shape[1]):
        a, b = np.hsplit(arr, [i])
        if a.shape[1] > b.shape[1]:
            _, a = np.hsplit(a, [a.shape[1] - b.shape[1]])
        elif a.shape[1] < b.shape[1]:
            b, _ = np.hsplit(b, [a.shape[1]])
        if np.all(a == np.fliplr(b)):
            if old_reflection is None:
                vertical = i
                break
            else:
                if old_reflection[0] is None:
                    vertical = i
                    return i, None
                else:
                    if old_reflection[0] != i:
                        return i, None
    for i in range(1, arr.shape[0]):
        a, b = np.vsplit(arr, [i])
        if a.shape[0] > b.shape[0]:
            _, a = np.vsplit(a, [a.shape[0] - b.shape[0]])
        elif a.shape[0] < b.shape[0]:
            b, _ = np.vsplit(b, [a.shape[0]])
        if np.all(a == np.flipud(b)):
            if old_reflection is None:
                horizontal = i
                break
            else:
                if old_reflection[1] is None:
                    horizontal = i
                    return None, i
                else:
                    if old_reflection[1] != i:
                        horizontal = i
                        return None, i
    return vertical, horizontal

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
    #print(find_smudge(puzzle_input[98]))
    for index, table in enumerate(puzzle_input):
        print(index)
        vertical, horizontal = find_smudge(table)
        #assert(vertical is None or horizontal is None)
        if vertical is not None:
            col_sum += vertical
        if horizontal is not None:
            row_sum += horizontal
    print(row_sum * 100 + col_sum)
    print(row_sum, col_sum)

if __name__ == '__main__':
    main()
