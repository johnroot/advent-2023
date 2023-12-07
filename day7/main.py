import os
from collections import Counter

part1 = '23456789TJQKA'
part2 = 'J23456789TQKA'
sorts = 'ABCDEFGHIJKLM'

def rank_hand(card, jokers_wild):
    freqs = Counter(card).most_common()
    most_freq = freqs[0]

    if jokers_wild and card != 'JJJJJ':
        jokers = next((f for f in freqs if f[0] == 'J'), None)
        if (jokers):
            freqs = [f for f in freqs if f[0] != 'J']
            most_freq = (freqs[0][0], freqs[0][1] + jokers[1])

    return (1.0/len(freqs), most_freq[1])

with open(os.path.join(os.path.dirname(__file__), 'input.txt'), 'r') as input_file:
    hands = [line.split() for line in input_file.readlines()]
    transform_to_sorted = lambda card, cards: ''.join([sorts[cards.index(c)] for c in card])

    hands.sort(key=lambda hand: (*rank_hand(hand[0], False), transform_to_sorted(hand[0], part1)))
    print(f"Part 1: {sum([int(hand[1]) * (i + 1) for i, hand in enumerate(hands)])}")

    hands.sort(key=lambda hand: (*rank_hand(hand[0], True), transform_to_sorted(hand[0], part2)))
    print(f"Part 2: {sum([int(hand[1]) * (i + 1) for i, hand in enumerate(hands)])}")
