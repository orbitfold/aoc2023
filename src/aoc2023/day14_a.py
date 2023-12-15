import click
import numpy as np

def update_rocks(arr):
    result = []
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            if arr[i][j] == 'O':
                if i > 0 and arr[i - 1][j] == '.':
                    arr[i][j] = '.'
                    arr[i - 1][j] = 'O'
                    result.append((i, j))
            elif arr[i][j] == '.':
                pass
            elif arr[i][j] == '#':
                pass
            else:
                RuntimeError("Wrong input!")
    return result

def propagate(arr):
    while update_rocks(arr):
        pass
    return arr

def calculate_load(arr):
    result = 0
    for i, row in enumerate(arr):
        print(row, arr.shape[0] - i, np.count_nonzero(row == 'O'))
        result += (arr.shape[0] - i) * np.count_nonzero(row == 'O')
    return result

@click.command()
@click.option('-i', '--input-file', help='Input file')
def main(input_file):
    with open(input_file, 'r') as fd:
        table = [] 
        for line in fd:
            table.append(list(line.strip()))
        puzzle_input = np.array(table)
    propagate(puzzle_input)
    print(calculate_load(puzzle_input))

if __name__ == '__main__':
    main()
