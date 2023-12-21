import click
import re
import inspect

class Rule:
    def __init__(self, descr):
        self.descr = descr
        r_ptrn = re.compile('^R$')
        a_ptrn = re.compile('^A$')
        name_ptrn = re.compile('^[a-z]+$')
        less_ptrn = re.compile('^([a-z]+)<([0-9]+):([a-zA-Z]+)$')
        more_ptrn = re.compile('^([a-z]+)>([0-9]+):([a-zA-Z]+)$')
        if r_ptrn.fullmatch(descr):
            self.rule = lambda _: 'R'
        elif a_ptrn.fullmatch(descr):
            self.rule = lambda _: 'A'
        elif name_ptrn.fullmatch(descr):
            self.rule = lambda _: descr
        elif less_ptrn.fullmatch(descr):
            split = less_ptrn.split(descr)
            self.rule = lambda part: split[3] if getattr(part, split[1]) < int(split[2]) else None
        elif more_ptrn.fullmatch(descr):
            split = more_ptrn.split(descr)
            self.rule = lambda part: split[3] if getattr(part, split[1]) > int(split[2]) else None      

    def check_part(self, part):
        return self.rule(part)

    def __repr__(self):
        return self.descr

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
    def __init__(self, descr):
        workflow_ptrn = re.compile('^([a-z]+){(.+)}$')
        split = workflow_ptrn.split(descr.strip())
        self.name = split[1]
        self.rules = [Rule(descr.strip()) for descr in split[2].split(',')]

    def check_part(self, part):
        for rule in self.rules:
            if rule.check_part(part) is not None:
                return rule.check_part(part)

    def __repr__(self):
        return f"{self.name}: {self.rules}"

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
    workflows = [Workflow(descr) for descr in input_rules]
    w_d = {}
    for workflow in workflows:
        w_d[workflow.name] = workflow
    result = 0
    for part in parts:
        current_workflow = w_d['in']
        while current_workflow.check_part(part) not in ['A', 'R']:
            print(part, current_workflow)
            current_workflow = w_d[w_d[current_workflow.name].check_part(part)]
        if current_workflow.check_part(part) == 'A':
            result += (part.x + part.m + part.a + part.s)
    print(result)

if __name__ == '__main__':
    main()
