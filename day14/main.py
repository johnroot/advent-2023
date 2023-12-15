import os
from enum import Enum

transpose = lambda platform: [''.join(row) for row in zip(*platform)]
Direction = Enum('Direction', ['NORTH', 'EAST', 'SOUTH', 'WEST'])

def tilt(platform: str, direction: Direction):
    reversed = True if direction == Direction.NORTH or direction == Direction.WEST else False
    transposed = True if direction == Direction.NORTH or direction == direction.SOUTH else False

    split_platform = platform.splitlines()

    if transposed:
        split_platform = transpose(split_platform)

    for i, column in enumerate(split_platform):
        split_platform[i] = '#'.join([''.join(sorted(section, reverse=reversed)) for section in column.split('#')])

    return '\n'.join(transpose(split_platform) if transposed else split_platform)

def load(platform: str):
    split_platform = platform.splitlines()
    return sum(row.count('O') * (len(split_platform) - i) for i, row in enumerate(split_platform))
    

spin_cycle = lambda platform: tilt(tilt(tilt(tilt(platform, Direction.NORTH), Direction.WEST), Direction.SOUTH), Direction.EAST)

with open(os.path.join(os.path.dirname(__file__), 'input.txt'), 'r') as input_file:
    platform = input_file.read()
    print(f"Part 1: {load(tilt(platform, Direction.NORTH))}")

    num_cycles = 1000000000
    cycled = platform
    results = [cycled]
    seen = set(results)
    repeat_len = 1

    for i in range(1, num_cycles):
        cycled = spin_cycle(cycled)
        if cycled in seen:
            previous = results.index(cycled)
            repeat_len = i - previous
            break
        seen.add(cycled)
        results.append(cycled)

    remaining_cycles = num_cycles - i
    additional_cycles = remaining_cycles % repeat_len
    for i in range(additional_cycles):
        cycled = spin_cycle(cycled)

    print(f"Part 2: {load(cycled)}")
