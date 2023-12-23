import click
import functools
import deal
import numpy as np

class Brick:
    def __init__(self, start, end):
        self.update(start, end)
        self.safe = False

    def update(self, start, end):
        self.start = start
        self.end = end
        x_range = list(range(min(self.start[0], self.end[0]),
                             max(self.start[0], self.end[0]) + 1))
        y_range = list(range(min(self.start[1], self.end[1]),
                             max(self.start[1], self.end[1]) + 1))
        z_range = list(range(min(self.start[2], self.end[2]),
                             max(self.start[2], self.end[2]) + 1))
        r = max(len(x_range), len(y_range), len(z_range))
        if len(x_range) == 1:
            x_range = x_range * r
        if len(y_range) == 1:
            y_range = y_range * r
        if len(z_range) == 1:
            z_range = z_range * r
        self.supports = []
        self.supported_by = []
        self.points = [(x, y, z) for x, y, z in zip(x_range, y_range, z_range)]

    def l_x(self):
        return min(self.start[0], self.end[0])

    def u_x(self):
        return max(self.start[0], self.end[0])

    def l_y(self):
        return min(self.start[1], self.end[1])

    def u_y(self):
        return max(self.start[1], self.end[1])

    def l_z(self):
        return min(self.start[2], self.end[2])

    def u_z(self):
        return max(self.start[2], self.end[2])

    def move_z(self, d):
        new_start = (self.start[0], self.start[1], self.start[2] + d)
        new_end = (self.end[0], self.end[1], self.end[2] + d)
        self.update(new_start, new_end)

    def rests_on(self, other):
        if other.l_z() <= self.u_z():
            return False
        queue = [self]
        while len(queue) > 0:
            node = queue.pop(0)
            for supporting in self.supported_by:
                if supporting == other:
                    return True
                queue.append(supporting)
        return False

    def count_falling(self, bricks):
        if self.safe:
            return 0
        else:
            counter = 0
            for brick in bricks:
                if brick.rests_on(self):
                    counter += 1
            return counter

class BrickStack:
    def __init__(self, bricks):
        x_size = max(bricks, key=lambda b: b.u_x()).u_x()
        y_size = max(bricks, key=lambda b: b.u_y()).u_y()
        z_size = max(bricks, key=lambda b: b.u_z()).u_z()
        self.stack = np.full((x_size + 1, y_size + 1, z_size + 1), None)

    def overlapping(self, brick):
        return [self.stack[*p] for p in brick.points]

    def drop_brick(self, brick):
        if brick.l_z() == 1:
            for p in brick.points:
                self.stack[*p] = brick
        else:
            overlap = self.overlapping(brick)
            while all([b is None for b in overlap]):
                if brick.l_z() == 0:
                    break
                brick.move_z(-1)
                overlap = self.overlapping(brick)
            brick.move_z(1)
            for b in overlap:
                if b is not None:
                    if brick not in b.supports:
                        b.supports.append(brick)
                    if b not in brick.supported_by:
                        brick.supported_by.append(b)
            for p in brick.points:
                self.stack[*p] = brick

def mark_safe(bricks):
    for brick in bricks:
        brick.safe = False
    for brick in bricks:
        if all([len(supported.supported_by) > 1 for supported in brick.supports]):
            brick.safe = True
    
def parse_input(input_file):
    bricks = []
    with open(input_file, 'r') as fd:
        for line in fd.readlines():
            line = line.strip()
            start, end = line.split('~')
            start = tuple([int(elt) for elt in start.split(',')])
            end = tuple([int(elt) for elt in end.split(',')])
            bricks.append(Brick(start, end))
    return bricks

def will_fall(l_brick, u_brick):
    if l_brick.safe:
        return False
    elif l_brick.u_z() >= u_brick.l_z():
        return False
    elif u_brick.supported_by == [l_brick]:
        return True
    elif u_brick.supported_by == []:
        return False
    else:
        return all([will_fall(l_brick, b) for b in u_brick.supported_by])

@click.command()
@click.option('-i', '--input-file', help='Input file')
def main(input_file):
    bricks = parse_input(input_file)
    bricks = sorted(bricks, key=lambda b: b.l_z())
    x_size = max(bricks, key=lambda b: b.u_x()).u_x()
    y_size = max(bricks, key=lambda b: b.u_y()).u_y()
    z_size = max(bricks, key=lambda b: b.u_z()).u_z()
    stack = BrickStack(bricks)
    for brick in bricks:
        stack.drop_brick(brick)
    mark_safe(bricks)
    result = 0
    for brick in bricks:
        if brick.safe:
            result += 1
    print('safe:', result)
    result = []
    for brick1 in bricks:
        counter = 0
        for brick2 in bricks:
            if will_fall(brick1, brick2):
                counter += 1
        print(counter)
        result.append(counter)
    print('sum:', sum(result))
    #for brick in bricks:
    #    print(brick, brick.count_falling(bricks))
    #import pdb; pdb.set_trace()

if __name__ == '__main__':
    main()
