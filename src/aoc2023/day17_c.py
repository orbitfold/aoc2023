import click
import numpy as np

INFINITY = 999999

def check_neighbor(puzzle, prev, node, neighbor):
    if neighbor[0] < 0 or neighbor[1] < 0 or neighbor[0] >= puzzle.shape[0] or neighbor[1] >= puzzle.shape[1]:
        return False
    p1 = get_prev(prev, node)
    p2 = get_prev(prev, p1)
    p3 = get_prev(prev, p2)
    if p1 is None:
        return True
    if p1 == neighbor:
        return False
    if p2 is None or p3 is None:
        return True
    if p2[0] == p1[0] == node[0] == neighbor[0]:
        return False
    if p2[1] == p1[1] == node[1] == neighbor[1]:
        return False
    return True

def get_neighbors(puzzle, prev, node):
    neighbors = [(node[0] + 1, node[1]), (node[0] - 1, node[1]),
                 (node[0], node[1] + 1), (node[0], node[1] - 1)]
    return [neighbor for neighbor in neighbors if check_neighbor(puzzle, prev, node, neighbor)]

def shortest_path(puzzle, prev):
    pos = (puzzle.shape[0] - 1, puzzle.shape[1] - 1)
    path = [pos]
    while pos != (0, 0):
        pos = prev[*pos]
        path.append(pos)
    return path

def print_path(puzzle, path):
    board = np.zeros(puzzle.shape)
    for p in path:
        board[p[0]][p[1]] = 1
    print(board)

def get_prev(prev, node):
    try:
        return prev[node]
    except KeyError:
        return None

def dijkstra(puzzle, start=(0, 0)):
    queue = []
    dist = np.ones(puzzle.shape) * INFINITY
    prev = {}
    dist[*start] = 0
    for i in range(puzzle.shape[0]):
        for j in range(puzzle.shape[1]):
            queue.append((i, j))
    while len(queue) > 0:
        node = min(queue, key=lambda p: dist[*p])
        queue.remove(node)
        neighbors = get_neighbors(puzzle, prev, node)
        for neighbor in neighbors:
            if neighbor in queue:
                alt = dist[*node] + puzzle[*neighbor]
                if alt < dist[*neighbor]:
                    dist[*neighbor] = alt
                    prev[*neighbor] = node
    return dist, prev

def path_cost(puzzle, path):
    result = 0
    for p in path[:-1]:
        result += puzzle[*p]
    return result

@click.command()
@click.option('-i', '--input-file', help='Input file')
def main(input_file):
    with open(input_file, 'r') as fd:
        raw_data = fd.read()
        lines = [[int(x) for x in list(line.strip())] for line in raw_data.splitlines()]
    puzzle = np.array(lines)
    dist, prev = dijkstra(puzzle)
    #print_path(puzzle, shortest_path(puzzle, prev))
    path = shortest_path(puzzle, prev)
    print(path_cost(puzzle, path))
    #shortest = get_shortest(puzzle, dist, prev)
    #for s in shortest:
        #path = backtrack(prev, s)
        #print_path(puzzle, path)
        #print(sum([puzzle[p[0]][p[1]] for p in path]))
    import pdb; pdb.set_trace()

if __name__ == '__main__':
    main()
