from aoc2023.day22_a import Brick, BrickStack, parse_input, count_safe

def test_brickstack():
    bricks = parse_input('data/day22_example.txt')
    bricks = sorted(bricks, key=lambda b: b.l_z())
    stack = BrickStack(bricks)
    for brick in bricks:
        stack.drop_brick(brick)
    assert(bricks[0].points == [(1, 0, 1), (1, 1, 1), (1, 2, 1)])
    assert(bricks[1].points == [(0, 0, 2), (1, 0, 2), (2, 0, 2)])
    assert(bricks[2].points == [(0, 2, 2), (1, 2, 2), (2, 2, 2)])
    assert(bricks[3].points == [(0, 0, 3), (0, 1, 3), (0, 2, 3)])
    assert(bricks[4].points == [(2, 0, 3), (2, 1, 3), (2, 2, 3)])
    assert(bricks[5].points == [(0, 1, 4), (1, 1, 4), (2, 1, 4)])
    assert(bricks[6].points == [(1, 1, 5), (1, 1, 6)])
    assert(count_safe(bricks) == 5)
    assert(bricks[1] in bricks[0].supports)
    assert(bricks[2] in bricks[0].supports)
    assert(bricks[1].supported_by == [bricks[0]])
    assert(bricks[2].supported_by == [bricks[0]])


