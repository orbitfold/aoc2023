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

def hand_type_b(hand):
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

def hand_type(hand):
    if 'J' in hand[0]:
        candidates = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', '1', 'J']
        candidates = [(hand[0].replace('J', c), hand[1]) for c in candidates]
        return hand_type_b(max(candidates, key=lambda h: hand_type_b(h)))
    else:
        return hand_type_b(hand)
        
def card_values(hand):
    mapping = {'A': 12, 'K': 11, 'Q': 10, 'T': 9, '9': 8, '8': 7, '7': 6, '6': 5, '5': 4, '4': 3, '3': 2, '2': 1, 'J': 0}
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
