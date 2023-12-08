import click
import numpy as np

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
    locations = [l for l in dictionary if l[-1] == 'A']
    steps = 0
    print(locations)
    step_counts = []
    for l in locations:
        location = l
        steps = 0
        while location[-1] != 'Z':
            if directions[steps % len(directions)] == 'L':
                location = dictionary[location][0]
            else:
                location = dictionary[location][1]
            steps += 1
        print(steps)
        step_counts.append(steps)
    result = step_counts[0]
    for step_count in step_counts:
        result = np.lcm(result, step_count)
    print(result)

if __name__ == '__main__':
    main()
