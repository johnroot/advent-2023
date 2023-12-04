import re
import os
import math
from collections import defaultdict

ticket_regex = re.compile('Card\s+\d+:\s+(?P<winning>(?:\d+\s+)+)\|\s+(?P<ticket>(?:\d+\s*)+)')

def get_winning_numbers(card: str) -> [str]:
    match = ticket_regex.match(card).groupdict()
    winning_numbers = [int(x) for x in re.findall(r'\d+', match['winning'])]
    ticket_numbers = [int(x) for x in re.findall(r'\d+', match['ticket'])]
    return list(filter(lambda i: i in winning_numbers, ticket_numbers))

def accumulate_points():
    points = 0
    with open(input, 'r') as input_file:
        for card in input_file:
            winning_numbers = get_winning_numbers(card)
            ticket_points = math.floor(2 ** (len(winning_numbers) - 1))
            points += ticket_points

    return points

def accumulate_tickets():
    cards = 0;
    copies = defaultdict(lambda: 1)
    with open(input, 'r') as input_file:
        for index, card in enumerate(input_file):
            while(copies[index] > 0):
                cards += 1
                for new_card in [index + i for i in range(1, len(get_winning_numbers(card)) + 1)]:
                    copies[new_card] += 1

                copies[index] -= 1

    return cards

input = os.path.join(os.path.dirname(__file__), 'input.txt')
if __name__ == '__main__':
    print(f"Part 1: {accumulate_points()}")
    print(f"Part 2: {accumulate_tickets()}")
