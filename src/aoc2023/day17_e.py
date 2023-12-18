import click
import numpy as np
import bisect
from dijkstar import Graph, find_path

INFINITY = 999999999

def check_neighbor(puzzle, neighbor):
    if neighbor[1][0] < 0:
        return False
    if neighbor[1][1] < 0:
        return False
    if neighbor[1][0] >= puzzle.shape[0]:
        return False
    if neighbor[1][1] >= puzzle.shape[1]:
        return False
    return True

def get_neighbors(puzzle, previous, current, straight):
    if previous == None:
        ns = [(current, (current[0] + 1, current[1]), 0),
              (current, (current[0] - 1, current[1]), 0),
              (current, (current[0], current[1] + 1), 0),
              (current, (current[0], current[1] - 1), 0)]
        return [n for n in ns if check_neighbor(puzzle, n)]
    elif straight < 3:
        if previous[0] == current[0]:
            ns = [(current, (current[0], current[1] + 1), straight + 1),
                  (current, (current[0], current[1] - 1), straight + 1)]
            return [n for n in ns if check_neighbor(puzzle, n) and n[1] != previous]
        elif previous[1] == current[1]:
            ns = [(current, (current[0] + 1, current[1]), straight + 1),
                  (current, (current[0] - 1, current[1]), straight + 1)]
            return [n for n in ns if check_neighbor(puzzle, n) and n[1] != previous]
    elif straight < 9:
        if previous[0] == current[0]:
            ns = [(current, (current[0] + 1, current[1]), 0),
                  (current, (current[0] - 1, current[1]), 0),
                  (current, (current[0], current[1] + 1), straight + 1),
                  (current, (current[0], current[1] - 1), straight + 1)]
            return [n for n in ns if check_neighbor(puzzle, n) and n[1] != previous]
        elif previous[1] == current[1]:
            ns = [(current, (current[0] + 1, current[1]), straight + 1),
                  (current, (current[0] - 1, current[1]), straight + 1),
                  (current, (current[0], current[1] + 1), 0),
                  (current, (current[0], current[1] - 1), 0)]
            return [n for n in ns if check_neighbor(puzzle, n) and n[1] != previous]
    else:
        if previous[0] == current[0]:
            ns = [(current, (current[0] + 1, current[1]), 0),
                  (current, (current[0] - 1, current[1]), 0)]
            return [n for n in ns if check_neighbor(puzzle, n)]
        elif previous[1] == current[1]:
            ns = [(current, (current[0], current[1] + 1), 0),
                  (current, (current[0], current[1] - 1), 0)]
            return [n for n in ns if check_neighbor(puzzle, n)]            


def get_dist(dist, node):
    try:
        return dist[node]
    except KeyError:
        return INFINITY

def get_prev(prev, node):
    try:
        return prev[node]
    except KeyError:
        return None

def backtrack(prev, start):
    back = start
    path = [back]
    while back != (None, None, (0, 0)):
        back = prev[back]
        path.append(back)
    return [p[2] for p in path]

def get_shortest(puzzle, dist, prev):
    last = []
    for node in prev:
        if node[2] == (puzzle.shape[0] - 1, puzzle.shape[1] - 1):
            last.append(node)
    return last

def print_path(puzzle, path):
    board = np.zeros(puzzle.shape)
    cost = 0
    for p in path:
        board[p[1][0]][p[1][1]] = 1
        cost += puzzle[p[1][0], p[1][1]]
    cost -= puzzle[0, 0]
    print(board)
    print(cost)

def heuristic(puzzle, node):
    node = node[1]
    return (puzzle.shape[0] - node[0]) + (puzzle.shape[1] - node[1])

def get_f_score(f_score, node):
    try:
        return f_score[node]
    except KeyError:
        return INFINITY

def get_g_score(g_score, node):
    try:
        return g_score[node]
    except KeyError:
        return INFINITY

def reconstruct_path(came_from, current):
    path = [current]
    while current[1] != (0, 0):
        current = came_from[current]
        path = [current] + path
    return path

def node_weight(puzzle, node):
    return puzzle[*node[1]]

def a_star(puzzle, start):
    open_set = []
    open_set.append(start)
    came_from = {}
    g_score = {}
    g_score[start] = 0
    f_score = {}
    f_score[start] = heuristic(puzzle, start)
    iteration = 0
    while len(open_set) > 0:
        iteration += 1
        current = min(open_set, key=lambda node: get_f_score(f_score, node))
        if current[1] == (puzzle.shape[0] - 1, puzzle.shape[1] - 1) and current[2] >= 3:
            print(iteration)
            return reconstruct_path(came_from, current)
        open_set.remove(current)
        for neighbor in get_neighbors(puzzle, *current):
            assert(current[1] == neighbor[0])
            tentative_g_score = get_g_score(g_score, current) + node_weight(puzzle, neighbor)
            if tentative_g_score < get_g_score(g_score, neighbor):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(puzzle, neighbor)
                if neighbor not in open_set:
                    #open_set.append(neighbor)
                    bisect.insort(open_set, neighbor, key=lambda node: get_f_score(f_score, neighbor))

@click.command()
@click.option('-i', '--input-file', help='Input file')
def main(input_file):
    with open(input_file, 'r') as fd:
        raw_data = fd.read()
        lines = [[int(x) for x in list(line.strip())] for line in raw_data.splitlines()]
    puzzle = np.array(lines)
    result = a_star(puzzle, (None, (0, 0), 0))
    import pdb; pdb.set_trace()

if __name__ == '__main__':
    main()
