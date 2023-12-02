import click

def parse_game(line):
    game_id, game_input = line.split(':')
    game_id = int(game_id.strip().split(' ')[1])
    games = game_input.strip().split(';')
    result = []
    for game in games:
        game = game.strip()
        colors = game.split(',')
        color_counts = [0, 0, 0]
        for color in colors:
            color = color.strip()
            if color.endswith('red'):
                color_counts[0] += int(color.split(' ')[0].strip())
            elif color.endswith('green'):
                color_counts[1] += int(color.split(' ')[0].strip())
            elif color.endswith('blue'):
                color_counts[2] += int(color.split(' ')[0].strip())
            else:
                raise RuntimeError("Invalid input!")
        result.append(color_counts)
    return result
    
@click.command()
@click.option('-i', '--input', help='Input file')
def main(input):
    id_sum = 0
    with open(input, 'r') as fd:
        for i, line in enumerate(fd.readlines()):
            parsed = parse_game(line)
            if all([r <= 12 and g <= 13 and b <= 14 for r, g, b in parsed]):
                id_sum += (i + 1)
    print(id_sum)

if __name__ == '__main__':
    main()
