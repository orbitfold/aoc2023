import click

def read_puzzle(filename):
    with open(filename, 'r') as fd:
        raw_data = fd.read()
    lines = raw_data.splitlines()
    result = []
    for line in lines:
        hand, value = line.strip().split()
        result.append((hand, int(value)))
    return result

def hand_type(hand):
    count = {}
    for c in hand[0]:
        try:
            count[c] += 1
        except KeyError:
            count[c] = 1
    if sorted(count.values()) == [5]:
        return 6
    elif sorted(count.values()) == [1, 4]:
        return 5
    elif sorted(count.values()) == [2, 3]:
        return 4
    elif sorted(count.values()) == [1, 1, 3]:
        return 3
    elif sorted(count.values()) == [1, 2, 2]:
        return 2
    elif sorted(count.values()) == [1, 1, 1, 2]:
        return 1
    elif sorted(count.values()) == [1, 1, 1, 1, 1]:
        return 0

def card_values(hand):
    mapping = {'A': 12, 'K': 11, 'Q': 10, 'J': 9, 'T': 8, '9': 7, '8': 6, '7': 5, '6': 4, '5': 3, '4': 2, '3': 1, '2': 0}
    result = []
    for c in hand[0]:
        result.append(mapping[c])
    return result

def compare_hands(hand1, hand2):
    pass
        

@click.command()
@click.option('-i', '--input-file')
def main(input_file):
    puzzle = read_puzzle(input_file)
    sorted_by_hand = {}
    for hand in puzzle:
        try:
            sorted_by_hand[hand_type(hand)].append(hand)
        except KeyError:
            sorted_by_hand[hand_type(hand)] = [hand]
    for key in sorted_by_hand:
        sorted_by_hand[key] = sorted(sorted_by_hand[key], key=card_values)
    result = 0
    final_hands = []
    for i in range(7):
        try:
            final_hands += sorted_by_hand[i]
        except KeyError:
            pass
    result = 0
    for i, hand in enumerate(final_hands):
        result += (i + 1) * hand[1]
    print(result)

if __name__ == '__main__':
    main()
