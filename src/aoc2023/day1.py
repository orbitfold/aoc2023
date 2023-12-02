import click

def parse(inputs):
    result = []
    for line in inputs:
        for c in line:
            if c.isdigit():
                a = int(c)
                break
        for c in line[::-1]:
            if c.isdigit():
                b = int(c)
                break
        result.append(a * 10 + b)
    return result

def parse_adv(inputs):
    spelled = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    result = []
    for line in inputs:
        for i, c in enumerate(line):
            if c.isdigit():
                a = int(c)
                break
            found = False
            for j, sp in enumerate(spelled):
                if line[i:].startswith(sp):
                    a = j + 1
                    found = True
            if found:
                break
        for i, c in enumerate(line[::-1]):
            if c.isdigit():
                b = int(c)
                break
            found = False
            for j, sp in enumerate(spelled):
                if line[::-1][i:].startswith(sp[::-1]):
                    b = j + 1
                    found = True
            if found:
                break
        result.append(a * 10 + b)
    return result

@click.command()
@click.option('-i', '--input', help='Input file')
@click.option('-a', '--advanced', is_flag=True, default=False, help='Advanced mode')
def main(input, advanced):
    with open(input, 'r') as fd:
        lines = fd.readlines()
    if advanced:
        print("Advanced mode")
        print(sum(parse_adv(lines)))
    else:
        print(sum(parse(lines)))

if __name__ == '__main__':
    main()
