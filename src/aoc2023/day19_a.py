import click
import re

class Rule:
    def __init__(self, descr):
        self.always_accept = False
        self.always_reject = False
        

    def check_part(self, part):
        pass

class Part:
    def __init__(self, descr):
        props = descr[1:-1].split(',')
        self.x = int(props[0].split('=')[1].strip())
        self.m = int(props[1].split('=')[1].strip())
        self.a = int(props[2].split('=')[1].strip())
        self.s = int(props[3].split('=')[1].strip())

    def __repr__(self):
        return f"{{x={self.x}, m={self.m}, a={self.a}, s={self.s}}}"

class Workflow:
    def __init__(self):
        pass

@click.command()
@click.option('-i', '--input-file', help='Input file')
def main(input_file):
    input_rules = []
    input_parts = []
    with open(input_file, 'r') as fd:
        part_list = False
        for line in fd.readlines():
            line = line.strip()
            if line != '':
                if part_list:
                    input_parts.append(line)
                else:
                    input_rules.append(line)
            else:
                part_list = True
    parts = [Part(descr) for descr in input_parts]
    import pdb; pdb.set_trace()

if __name__ == '__main__':
    main()
