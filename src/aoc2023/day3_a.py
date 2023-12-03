import numpy as np
from itertools import product

def parse_numbers(input_):
    arr = np.array([list(line) for line in input_])
    in_number = False
    part_number = False
    number = []
    result = []
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            if arr[i][j].isnumeric():
                in_number = True
                number.append(arr[i][j])
                i0 = max(i - 1, 0)
                i1 = min(i + 1, arr.shape[0] - 1)
                j0 = max(j - 1, 0)
                j1 = min(j + 1, arr.shape[1] - 1)
                for i_, j_ in product([i0, i, i1], [j0, j, j1]):
                    if not arr[i_][j_].isnumeric() and arr[i_][j_] != '.':
                        part_number = True
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
    return result
                
                        
                
