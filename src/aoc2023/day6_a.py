import click

def parse_input(input_):
    puzzle = input_.splitlines()
    time = [int(t.strip()) for t in puzzle[0].split(':')[1].strip().split()]
    distance = [int(d.strip()) for d in puzzle[1].split(':')[1].strip().split()]
    return [time, distance]

def calculate_winning_times(p):
    result = []
    for i in range(p[0]):
        if i * (p[0] - i) > p[1]:
            result.append(i)
    return result

@click.command()
@click.option('-i', '--input', help='Input file')
def main(input):
    with open(input, 'r') as fd:
        puzzle = parse_input(fd.read())
    result = 1
    for p in zip(puzzle[0], puzzle[1]):
        t = calculate_winning_times(p)
        result *= len(t)
    print(result)

if __name__ == '__main__':
    main()
