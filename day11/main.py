import os
from itertools import combinations

def manhattan(galaxies):
    galaxy_pairs = list(combinations(galaxies, 2))
    print(f"{sum(abs(pair[0][0] - pair[1][0]) + abs(pair[0][1] - pair[1][1]) for pair in galaxy_pairs)}")

def part1():
    with open(os.path.join(os.path.dirname(__file__), 'input.txt'), 'r') as input_file:
        space = [[*line] for line in input_file.read().splitlines()]
        i = 0
        while i < len(space[0]):
            column = [row[i] for row in space]
            if (all(char == '.' for char in column)):
                for row in space:
                    row.insert(i, '.')
                
                i += 1
            
            i += 1

        expanded = []
        for row in space:
            expanded.append(row)
            if all(char == '.' for char in row):
                expanded.append(row)
                
        galaxies = []
        for x, row in enumerate(expanded):
            for y, char in enumerate(row):
                if char == '#':
                    galaxies.append((x, y))

        manhattan(galaxies)

def part2():
    with open(os.path.join(os.path.dirname(__file__), 'input.txt'), 'r') as input_file:
        space = [[*line] for line in input_file.read().splitlines()]
        empty_rows = []
        empty_columns = []

        for i in range(len(space[0])):
            column = [row[i] for row in space]
            if (all(char == '.' for char in column)):
                empty_columns.append(i)

        expanded = []
        for i, row in enumerate(space):
            expanded.append(row)
            if all(char == '.' for char in row):
                empty_rows.append(i)

        galaxies = []
        for x, row in enumerate(expanded):
            for y, char in enumerate(row):
                if char == '#':
                    galaxy_x = x + 999_999 * len([r for r in empty_rows if r < x])
                    galaxy_y = y + 999_999 * len([c for c in empty_columns if c < y])
                    galaxies.append((galaxy_x, galaxy_y))

        manhattan(galaxies)

part1()
part2()