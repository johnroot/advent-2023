import os
import math
from functools import reduce
    
if __name__ == '__main__':
    get_wins = lambda race: sum([i * (race[0] - i) > race[1] for i in range(1, race[0])])
    with open(os.path.join(os.path.dirname(__file__), 'input.txt'), 'r') as input_file:
        races = list(zip(*[[int(x) for x in line.split()[1::]] for line in input_file.read().splitlines()]))
        print(f"Part 1: {math.prod([get_wins(race) for race in races])}")
        print(f"Part 2: {get_wins(reduce(lambda x, y: (int(str(x[0]) + str(y[0])), int(str(x[1]) + str(y[1]))), races))}")
