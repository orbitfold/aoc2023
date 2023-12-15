import click

def parse_statement(st):
    value = 0
    for c in list(st):
        value += ord(c)
        value *= 17
        value %= 256
    return value

@click.command()
@click.option('-i', '--input-file', help='Input file')
def main(input_file):
    with open(input_file, 'r') as fd:
        line = fd.read()
        puzzle_input = [x.strip() for x in line.split(',')]
    print(sum([parse_statement(st) for st in puzzle_input]))

if __name__ == '__main__':
    main()
