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

@click.command()
@click.option('-i', '--input', help='Input file')
def main(input):
    with open(input, 'r') as fd:
        lines = fd.readlines()
    print(sum(parse(lines)))

if __name__ == '__main__':
    main()
