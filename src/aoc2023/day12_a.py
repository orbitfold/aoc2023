import click
import itertools

def spring_list_to_spec(spring_list):
    inside_broken = False
    counter = 0
    result = []
    for i, c in enumerate(spring_list):
        if c == '#' and inside_broken:
            counter += 1
        elif c == '#' and not inside_broken:
            counter += 1
            inside_broken = True
        elif c != '#' and inside_broken:
            result.append(counter)
            counter = 0
            inside_broken = False
    if counter != 0:
        result.append(counter)
    return result

def check_spec(spring_list, spec):
    return spring_list_to_spec(spring_list) == spec

def replace_question_marks(spring_list, replacements):
    spring_list = list(spring_list)
    for i, c in enumerate(spring_list):
        if c == '?':
            spring_list[i] = replacements[0]
            replacements = replacements[1:]
    return "".join(spring_list)

def count_question_marks(spring_list):
    spring_list = list(spring_list)
    counter = 0
    for c in spring_list:
        if c == '?':
            counter += 1
    return counter

def all_combinations(spring_list, spec):
    iterables = [['#', '.']] * count_question_marks(spring_list)
    count = 0
    for c in itertools.product(*iterables):
        replaced = replace_question_marks(spring_list, c)
        if check_spec(replaced, spec):
            #print(replaced)
            count += 1
    return count

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
            puzzle_input.append((springs, specs))
    result = 0
    run = 0
    for pair in puzzle_input:
        print(run)
        run += 1
        result += all_combinations(pair[0], pair[1])
    print(result)

if __name__ == '__main__':
    main()
