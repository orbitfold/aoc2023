import click

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
            if result == 0:
                result = 1
            else:
                result *= 2
    return result

def parse_cards(cards):
    return [parse_card(card) for card in cards]

@click.command()
@click.option('-i', '--input-file', help='Input file')
def main(input_file):
    with open(input_file, 'r') as fd:
        cards = fd.readlines()
        cards = [card.strip() for card in cards]
        results = parse_cards(cards)
    print(sum(results))

if __name__ == '__main__':
    main()
