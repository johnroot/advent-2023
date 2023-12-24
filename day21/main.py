import os

def go(x, y, garden_map):
    max_x = len(garden_map)
    max_y = len(garden_map[0])
    possibilities = [((x + 1), y), ((x - 1), y), (x, (y + 1)), (x, (y - 1))]
    return [(x1, y1) for x1, y1 in possibilities if garden_map[x1 % max_x][y1 % max_y] in ['.', 'S']]

with open(os.path.join(os.path.dirname(__file__), 'input.txt'), 'r') as input_file:
    garden_map = [list(line) for line in input_file.read().splitlines()]
    possible_locations = set((x, y) for x, line in enumerate(garden_map) for y, char in enumerate(line) if char == 'S')
    
    x = [65, 65 + len(garden_map), 65 + (2 * len(garden_map))]
    y = []
    for i in range(1, 350):
        new_locations = []
        for location in possible_locations:
            new_locations += go(*location, garden_map)
        possible_locations = set(new_locations)
        if i in x:
            y.append(len(possible_locations))

    print(x, y)

    goal = 26501365
    def f(n):
        a0 = 3821
        a1 = 34234
        a2 = 94963

        b0 = a0
        b1 = a1-a0
        b2 = a2-a1
        return b0 + b1*n + (n*(n-1)//2)*(b2-b1)
    
    print(f(goal//len(garden_map)))