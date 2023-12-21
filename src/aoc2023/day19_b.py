import click
import re
import inspect
import itertools
from interval import interval
import numpy as np

class Rule:
    def __init__(self, descr):
        self.descr = descr
        name_ptrn = re.compile('^[a-zA-Z]+$')
        less_ptrn = re.compile('^([a-z]+)<([0-9]+):([a-zA-Z]+)$')
        more_ptrn = re.compile('^([a-z]+)>([0-9]+):([a-zA-Z]+)$')
        if name_ptrn.fullmatch(descr):
            self.rule = lambda part: (descr, Part(part.x, part.m, part.a, part.s), None)
        elif less_ptrn.fullmatch(descr):
            split = less_ptrn.split(descr)
            label = split[3]
            attr = split[1]
            value = int(split[2])
            def checker_1(part):
                new_part_1, new_part_2 = part.split(attr, value)
                assert(new_part_1 is not None)
                assert(new_part_2 is not None)
                return label, new_part_1, new_part_2
            self.rule = checker_1
        elif more_ptrn.fullmatch(descr):
            split = more_ptrn.split(descr)
            label = split[3]
            attr = split[1]
            value = int(split[2])
            def checker_2(part):
                new_part_1, new_part_2 = part.split(attr, value + 1)
                assert(new_part_1 is not None)
                assert(new_part_2 is not None)
                return label, new_part_2, new_part_1
            self.rule = checker_2
        else:
            raise RuntimeError("some bullshit")

    def check_part(self, part):
        return self.rule(part)

    def __repr__(self):
        return self.descr

class Part:
    def __init__(self, x=(1, 4000), m=(1, 4000), a=(1, 4000), s=(1, 4000)):
        self.x = x
        self.m = m
        self.a = a
        self.s = s

    def __repr__(self):
        return f"{{x={self.x}, m={self.m}, a={self.a}, s={self.s}}}"

    def split(self, attribute, value):
        a = getattr(self, attribute)[0]
        b = getattr(self, attribute)[1]
        if value >= b:
            return self, None
        if value <= a:
            return None, self
        else:
            new_part_1 = Part(self.x, self.m, self.a, self.s)
            new_part_2 = Part(self.x, self.m, self.a, self.s)
            new_range_1 = (a, value - 1)
            new_range_2 = (value, b)
            setattr(new_part_1, attribute, new_range_1)
            setattr(new_part_2, attribute, new_range_2)
            return new_part_1, new_part_2

    def combinations(self):
        return ((self.x[1] - self.x[0] + 1) *
                (self.m[1] - self.m[0] + 1) *
                (self.a[1] - self.a[0] + 1) *
                (self.s[1] - self.s[0] + 1))

    def __eq__(self, other):
        return self.x == other.x and self.m == other.m and self.a == other.a and self.s == other.s

class Workflow:
    def __init__(self, descr):
        workflow_ptrn = re.compile('^([a-z]+){(.+)}$')
        split = workflow_ptrn.split(descr.strip())
        self.name = split[1]
        self.rules = [Rule(descr.strip()) for descr in split[2].split(',')]

    def check_part(self, part):
        processed = {}
        for rule in self.rules:
            label, a, r = rule.check_part(part)
            if a is not None:
                try:
                    processed[label].append(a)
                except KeyError:
                    processed[label] = [a]
            part = r
        return processed

    def __repr__(self):
        return f"{self.name}: {self.rules}"

def montecarlo(parts, iterations=10000):
    accepted = 0
    for _ in range(iterations):
        x = np.random.randint(1, 4001)
        m = np.random.randint(1, 4001)
        a = np.random.randint(1, 4001)
        s = np.random.randint(1, 4001)
        if any([part.x[0] <= x <= part.x[1] and part.m[0] <= m <= part.m[1] and part.a[0] <= a <= part.a[1] and part.s[0] <= s <= part.s[1] for part in parts]):
            accepted += 1
    return (accepted / iterations) * 4000 * 4000 * 4000 * 4000

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
    part = Part()
    workflows = [Workflow(descr) for descr in input_rules]
    ws = {}
    for workflow in workflows:
        ws[workflow.name] = workflow
    current = ws['in'].check_part(Part())
    partitions = [current]
    accepted = []
    rejected = []
    while len(partitions) > 0:
        new_partitions = []
        print([[workflow for workflow in current] for current in partitions])
        print(partitions)
        print()
        for current in partitions:
            for workflow in current:
                if workflow == 'A':
                    accepted += current[workflow]
                elif workflow == 'R':
                    rejected += current[workflow]
                else:
                    new_result = [ws[workflow].check_part(part) for part in current[workflow]]
                    new_partitions += new_result
        partitions = new_partitions
    result = 0
    for part in accepted:
        result += part.combinations()
    import pdb; pdb.set_trace()
    # w_d = {}
    # for workflow in workflows:
    #     w_d[workflow.name] = workflow
    # result = 0
    # for part in parts:
    #     current_workflow = w_d['in']
    #     while current_workflow.check_part(part) not in ['A', 'R']:
    #         print(part, current_workflow)
    #         current_workflow = w_d[w_d[current_workflow.name].check_part(part)]
    #     if current_workflow.check_part(part) == 'A':
    #         result += (part.x + part.m + part.a + part.s)
    #print(result)

if __name__ == '__main__':
    main()
