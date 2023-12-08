import click

@click.command()
@click.option('-i', '--input-file', help='Input file')
def main(input_file):
    with open(input_file, 'r') as fd:
        raw_data = fd.read()
        lines = raw_data.splitlines()
    directions = list(lines[0].strip())
    dictionary = {}
    for line in lines[2:]:
        command = line.split('=')
        pair = command[1].strip().split(',')
        p1 = pair[0].strip()[1:]
        p2 = pair[1].strip()[:-1]
        dictionary[command[0].strip()] = (p1, p2)
    location = 'AAA'
    steps = 0
    while location != 'ZZZ':
        if directions[steps % len(directions)] == 'L':
            location = dictionary[location][0]
        else:
            location = dictionary[location][1]
        print(location, directions[steps % len(directions)])
        steps += 1
    print(steps)
    import pdb; pdb.set_trace()

if __name__ == '__main__':
    main()
