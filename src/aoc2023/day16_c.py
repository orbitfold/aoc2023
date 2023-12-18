import click
import numpy as np

def find_loop(p):
    visited = set()
    for position, direction in zip(p[0], p[1]):
        if (position, direction) in visited:
            return True
        else:
            visited.add((position, direction))
    return False

def check_pair(puzzle, p):
    if p[0][-1][0] < 0:
        return False
    if p[0][-1][1] < 0:
        return False
    if p[0][-1][0] >= puzzle.shape[0]:
        return False
    if p[0][-1][1] >= puzzle.shape[1]:
        return False
    if find_loop(p):
        return False
    return True

def unique_visited(visited):
    positions = [p[0] for p in visited]
    return list(set(positions))

def bfs(puzzle):
    visited = set()
    queue = []
    queue.append(((0, 0), (0, 1)))
    while len(queue) > 0:
        position, direction = queue.pop(0)
        if position[0] < 0 or position[1] < 0 or position[0] >= puzzle.shape[0] or position[1] >= puzzle.shape[1]:
            continue
        if (position, direction) not in visited:
            visited.add((position, direction))
        else:
            continue
        if puzzle[*position] == '.':
            new_direction = direction
            new_position = (position[0] + new_direction[0], position[1] + new_direction[1])
            queue.append((new_position, new_direction))
        elif puzzle[*position] == '/':
            new_direction = (-direction[1], -direction[0])
            new_position = (position[0] + new_direction[0], position[1] + new_direction[1])
            queue.append((new_position, new_direction))
        elif puzzle[*position] == '\\':
            new_direction = (direction[1], direction[0])
            new_position = (position[0] + new_direction[0], position[1] + new_direction[1])
            queue.append((new_position, new_direction))            
        elif puzzle[*position] == '|':
            new_direction_1 = (-1, 0)
            new_direction_2 = (1, 0)
            new_position_1 = (position[0] + new_direction_1[0], position[1] + new_direction_1[1])
            new_position_2 = (position[0] + new_direction_2[0], position[1] + new_direction_2[1])
            queue.append((new_position_1, new_direction_1))
            queue.append((new_position_2, new_direction_2))
        elif puzzle[*position] == '-':
            new_direction_1 = (0, -1)
            new_direction_2 = (0, 1)
            new_position_1 = (position[0] + new_direction_1[0], position[1] + new_direction_1[1])
            new_position_2 = (position[0] + new_direction_2[0], position[1] + new_direction_2[1])
            queue.append((new_position_1, new_direction_1))
            queue.append((new_position_2, new_direction_2))
        else:
            raise RuntimeError("Wrong input!")
    return visited

@click.command()
@click.option('-i', '--input-file', help='Input file')
def main(input_file):
    with open(input_file, 'r') as fd:
        raw_data = fd.read()
        raw_data = [list(line.strip()) for line in raw_data.splitlines()]
    puzzle = np.array(raw_data)
    visited = bfs(puzzle)
    print(len(unique_visited(visited)))

if __name__ == '__main__':
    main()
