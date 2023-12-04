import click
import numpy as np

def parse_card(card):
    card_id, numbers = card.split(':')
    card_id = card_id.strip()
    numbers = numbers.strip()
    winning_numbers, card_numbers = numbers.split('|')
    winning_numbers = winning_numbers.strip()
    card_numbers = card_numbers.strip()
    winning_numbers = winning_numbers.split(' ')
    card_numbers = card_numbers.split(' ')
    winning_numbers = [int(number.strip()) for number in winning_numbers if number != '']
    card_numbers = [int(number.strip()) for number in card_numbers if number != '']
    result = 0
    for winning_number in winning_numbers:
        if winning_number in card_numbers:
            result += 1
    return result

def count_cards(cards):
    card_numbers = [parse_card(card) for card in cards]
    copies = np.ones(len(card_numbers)).astype(int)
    for i, _ in enumerate(card_numbers):
        n = card_numbers[i]
        copies[i + 1:i + n + 1] += copies[i]
    return copies.sum()

@click.command()
@click.option('-i', '--input-file', help='Input file')
def main(input_file):
    with open(input_file, 'r') as fd:
        cards = fd.readlines()
        cards = [card.strip() for card in cards]
        results = count_cards(cards)
    print(results)

if __name__ == '__main__':
    main()
