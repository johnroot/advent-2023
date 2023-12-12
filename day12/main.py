import os
from functools import cache

normal = '.'
damaged = '#'
unknown = '?'

@cache
def solutions(springs: str, groups: tuple[int, ...], group_size=0):    
    if not springs:
        if ((len(groups) == 1 and groups[0] == group_size)) or \
            (len(groups) == 0 and group_size == 0):
            return 1
        return 0

    spring, *springs = springs
    springs = ''.join(springs)
    
    group, *new_groups = groups or [0]
    new_groups = tuple(new_groups)

    if spring == unknown:
        return solutions(normal + springs, groups, group_size) + \
            solutions(damaged + springs, groups, group_size)
    if spring == damaged:
        return 0 if group_size > group else solutions(springs, groups, group_size + 1)
    if spring == normal:
        if group_size == 0:
            return solutions(springs, groups, 0)
        if group_size == group:
            return solutions(springs, new_groups, 0)
        return 0
    
    return 0

with open(os.path.join(os.path.dirname(__file__), 'input.txt'), 'r') as input_file:
    records = [(line.split()[0], tuple(map(int, line.split()[1].split(',')))) for line in input_file.read().splitlines()]
    print(f"Part 1: {sum(solutions(record[0], record[1]) for record in records)}")

    unfolded_records = [(unknown.join([record[0]] * 5), record[1] * 5) for record in records]
    print(f"Part 2: {sum(solutions(*record) for record in unfolded_records)}")