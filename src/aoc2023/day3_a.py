import numpy as np
from itertools import product
import click

def parse_numbers(input_):
    arr = np.array([list(line.strip()) for line in input_])
    result = []
    for i in range(arr.shape[0]):
        in_number = False
        part_number = False
        number = []
        for j in range(arr.shape[1]):
            if arr[i][j].isnumeric():
                in_number = True
                number.append(arr[i][j])
                i0 = i - 1
                i1 = i + 1
                j0 = j - 1
                j1 = j + 1
                for i_, j_ in product([i0, i, i1], [j0, j, j1]):
                    try:
                        if (not arr[i_][j_].isnumeric()) and (arr[i_][j_] != '.'):
                            part_number = True
                    except:
                        continue
            elif not arr[i][j].isnumeric() and in_number:
                power = 0
                number_numeric = 0
                while len(number) != 0:
                    digit = number.pop()
                    number_numeric += int(digit) * 10 ** power
                    power += 1
                if part_number:
                    result.append(number_numeric)
                in_number = False
                part_number = False
        if in_number:
            power = 0
            number_numeric = 0
            while len(number) != 0:
                digit = number.pop()
                number_numeric += int(digit) * 10 ** power
                power += 1
            if part_number:
                result.append(number_numeric)
            in_number = False
            part_number = False            
    return result

@click.command()
@click.option('-i', '--input-file', help='Input file')
def main(input_file):
    with open(input_file, 'r') as fd:
        lines = fd.readlines()
    result = parse_numbers(lines)
    print(result)
    print(sum(result))

if __name__ == '__main__':
    main()
