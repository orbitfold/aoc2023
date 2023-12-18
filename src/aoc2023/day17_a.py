import click
import numpy as np

INFINITY = 999999

def check_neighbor(puzzle, p1, p2, p3, neighbor):
    if neighbor[0] < 0 or neighbor[1] < 0 or neighbor[0] >= puzzle.shape[0] or neighbor[1] >= puzzle.shape[1]:
        return False
    if neighbor == p2:
        return False
    if p1 is None:
        return True
    if p2 is None:
        return True
    if p1[0] == p2[0] == p3[0] == neighbor[0]:
        return False
    if p1[1] == p2[1] == p3[1] == neighbor[1]:
        return False
    return True

def get_neighbors(puzzle, node):
    p1, p2, p3 = node
    neighbors = [(p3[0] + 1, p3[1]), (p3[0] - 1, p3[1]),
                 (p3[0], p3[1] + 1), (p3[0], p3[1] - 1)]
    return [neighbor for neighbor in neighbors if check_neighbor(puzzle, p1, p2, p3, neighbor)]

def construct_queue(puzzle):
    queue = []
    for i in range(puzzle.shape[0]):
        for j in range(puzzle.shape[1]):
            queue.append((None, None, (i, j)))
            n1s = get_neighbors(puzzle, queue[-1])
            for n1 in n1s:
                queue.append((None, (i, j), n1))
                n2s = get_neighbors(puzzle, queue[-1])
                for n2 in n2s:
                    queue.append(((i, j), n1, n2))
    return queue

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

def get_node_weight(puzzle, node):
    w1 = puzzle[node[2][0]][node[2][1]]
    if node[0] == node[1] == None:
        return w1
    w2 = puzzle[node[1][0]][node[1][1]]
    if node[0] == None:
        return w1 + w2
    w3 = puzzle[node[0][0]][node[0][1]]
    return w1 + w2 + w3

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
    for p in path:
        board[p[0]][p[1]] = 1
    print(board)

def dijkstra(puzzle, start=(None, None, (0, 0))):
    queue = construct_queue(puzzle)
    dist = {}
    prev = {}
    dist[start] = 0
    while len(queue) > 0:
        node = min(queue, key=lambda p: get_dist(dist, p))
        queue.remove(node)
        for neighbor in get_neighbors(puzzle, node):
            if (node[1], node[2], neighbor) in queue:
                alt = get_dist(dist, node) + get_node_weight(puzzle, (node[1], node[2], neighbor))
                if alt < get_dist(dist, (node[1], node[2], neighbor)):
                    dist[(node[1], node[2], neighbor)] = alt
                    prev[(node[1], node[2], neighbor)] = node
    return dist, prev

@click.command()
@click.option('-i', '--input-file', help='Input file')
def main(input_file):
    with open(input_file, 'r') as fd:
        raw_data = fd.read()
        lines = [[int(x) for x in list(line.strip())] for line in raw_data.splitlines()]
    puzzle = np.array(lines)
    dist, prev = dijkstra(puzzle)
    shortest = get_shortest(puzzle, dist, prev)
    for s in shortest:
        path = backtrack(prev, s)
        print_path(puzzle, path)
        #print(sum([puzzle[p[0]][p[1]] for p in path]))
    import pdb; pdb.set_trace()

if __name__ == '__main__':
    main()
