import click
import itertools
import numpy as np
import functools

@functools.cache
def recursive_counter(spring_list, spec, broken=0):
    spring_list = list(spring_list)
    spec = list(spec)
    if len(spring_list) == 0 and len(spec) == 0:
        if broken > 0:
            return 0
        else:
            return 1
    elif len(spring_list) == 0 and len(spec) > 0:
        if broken > 0 and len(spec) == 1 and spec[0] == broken:
            return 1
        else:
            return 0
    elif spring_list[0] == '.' and broken == 0:
        return recursive_counter(tuple(spring_list[1:]), tuple(spec), broken=0)
    elif spring_list[0] == '.' and broken > 0:
        if len(spec) == 0:
            return 0
        if spec[0] == broken:
            return recursive_counter(tuple(spring_list[1:]), tuple(spec[1:]), broken=0)
        else:
            return 0
    elif spring_list[0] == '#':
        return recursive_counter(tuple(spring_list[1:]), tuple(spec), broken=broken + 1)
    elif spring_list[0] == '?':
        return (recursive_counter(tuple(['.'] + spring_list[1:]), tuple(spec), broken=broken) +
                recursive_counter(tuple(['#'] + spring_list[1:]), tuple(spec), broken=broken))    
                
@click.command()
@click.option('-i', '--input-file', help='Input file')
def main(input_file):
    puzzle_input = []
    with open(input_file, 'r') as fd:
        raw_data = fd.read()
        lines = raw_data.splitlines()
        for line in lines:
            springs, specs = line.split()
            specs = [int(nr) for nr in specs.split(',')]
            puzzle_input.append(("?".join([springs] * 5), specs * 5))
    result = 0
    run = 0
    values = []
    for pair in puzzle_input:
        run += 1
        comb = recursive_counter(tuple(list(pair[0])), tuple(pair[1]))
        values.append(comb)
        result += comb
        print(run, comb)
    print(sum(values))

if __name__ == '__main__':
    main()
