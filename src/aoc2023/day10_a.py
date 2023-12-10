import click
import numpy as np
import sys
import functools

MAX_DISTANCE = 9999999

class Maze:
    def __init__(self, input_file):
        with open(input_file, 'r') as fd:
            raw_data = fd.read()
            puzzle_input = []
            for line in raw_data.splitlines():
                puzzle_input.append(list(line.strip()))
        self.maze = np.array(puzzle_input)
        self.distances = np.ones(self.maze.shape) * MAX_DISTANCE
        self.outline = np.zeros(self.maze.shape)
        self.inside = np.zeros(self.maze.shape)

    def find_start(self):
        start = np.where(self.maze == 'S')
        return start[0][0], start[1][0]

    def one_step(self, flood=False):
        current_distance = self.distances[self.position]
        self.outline[self.position] = 1
        self.position = (self.position[0] + self.direction[0],
                         self.position[1] + self.direction[1])
        if flood:
            arr = np.array(self.outline)
            if self.direction == (-1, 0):
                self.flood_fill(arr, (self.position[0], self.position[1] + 1))
            elif self.direction == (1, 0):
                self.flood_fill(arr, (self.position[0], self.position[1] - 1))
            elif self.direction == (0, -1):
                self.flood_fill(arr, (self.position[0] - 1, self.position[1]))
            elif self.direction == (0, 1):
                self.flood_fill(arr, (self.position[0] + 1, self.position[1]))
            arr[np.where(arr != -1)] = 0
            arr[np.where(arr == -1)] = 1
            self.floods.append(arr)
        if self.maze[self.position] == 'S':
            return False
        self.distances[self.position] = min(self.distances[self.position], current_distance + 1)
        if self.direction == (1, 0):
            if self.maze[self.position] == '|':
                self.direction = (1, 0)
            elif self.maze[self.position] == 'J':
                self.direction = (0, -1)
            elif self.maze[self.position] == 'L':
                self.direction = (0, 1)
            else:
                raise RuntimeError('Wrong input!')
        elif self.direction == (-1, 0):
            if self.maze[self.position] == '|':
                self.direction = (-1, 0)
            elif self.maze[self.position] == '7':
                self.direction = (0, -1)
            elif self.maze[self.position] == 'F':
                self.direction = (0, 1)
            else:
                raise RuntimeError('Wrong input!')
        elif self.direction == (0, 1):
            if self.maze[self.position] == '-':
                self.direction = (0, 1)
            elif self.maze[self.position] == 'J':
                self.direction = (-1, 0)
            elif self.maze[self.position] == '7':
                self.direction = (1, 0)
            else:
                raise RuntimeError('Wrong input!')
        elif self.direction == (0, -1):
            if self.maze[self.position] == '-':
                self.direction = (0, -1)
            elif self.maze[self.position] == 'L':
                self.direction = (-1, 0)
            elif self.maze[self.position] == 'F':
                self.direction = (1, 0)
            else:
                raise RuntimeError('Wrong input!')
        else:
            raise RuntimeError('Wrong position!')
        return True

    def possible_directions(self, position):
        n1 = self.maze[(position[0] - 1, position[1])]
        n2 = self.maze[(position[0] + 1, position[1])]
        n3 = self.maze[(position[0], position[1] - 1)]
        n4 = self.maze[(position[0], position[1] + 1)]
        directions = []
        if n1 in ['|', '7', 'F']:
            directions.append((-1, 0))
        if n2 in ['|', 'L', 'J']:
            directions.append((1, 0))
        if n3 in ['-', 'F', 'L']:
            directions.append((0, -1))
        if n4 in ['-', '7', 'J']:
            directions.append((0, 1))
        return directions

    def follow_path(self, start_position, start_direction, flood=False):
        self.position = start_position
        self.direction = start_direction
        finished = False
        while not finished:
            finished = not self.one_step(flood=flood)

    def follow_paths(self, flood=False):
        start_position = self.find_start()
        start_direction = self.possible_directions(start_position)[0]
        self.distances[start_position] = 0
        self.follow_path(start_position, start_direction, flood=flood)
        #for start_direction in self.possible_directions(start_position):
        #    self.distances[start_position] = 0
        #    self.follow_path(start_position, start_direction)

    def flood_fill(self, arr, node):
        try:
            if arr[node] != 0:
                return
            else:
                arr[node] = -1
        except IndexError:
            return
        self.flood_fill(arr, (node[0] - 1, node[1]))
        self.flood_fill(arr, (node[0] + 1, node[1]))
        self.flood_fill(arr, (node[0], node[1] - 1))
        self.flood_fill(arr, (node[0], node[1] + 1))
            

@click.command()
@click.option('-i', '--input-file', help='Input file')
def main(input_file):
    sys.setrecursionlimit(1000000)
    maze = Maze(input_file)
    maze.follow_paths()
    #print(maze.outline)
    maze.floods = []
    maze.follow_paths(flood=True)
    inside = functools.reduce(lambda a, b: np.logical_or(a, b).astype(int), maze.floods)
    print(inside.sum())
    #maze.flood_fill((0, 0))
    #print(maze.outline)
    #print(maze.outline[maze.outline == 0].shape[0])
    #import pdb; pdb.set_trace()
    #print(max(maze.distances[maze.distances != MAX_DISTANCE]))

if __name__ == '__main__':
    main()
