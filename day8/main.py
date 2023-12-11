import os
import re
import math

regex = re.compile(r"(\w{3}) = \((\w{3}), (\w{3})\)")

def findSteps(position, isEnd):
    step = 0
    while not isEnd(position):
        direction = directions[step % len(directions)]
        position = (map[position][0] if direction == 'L' else map[position][1])
        step += 1

    return step

with open(os.path.join(os.path.dirname(__file__), 'input.txt'), 'r') as input_file:
    directions = input_file.readline().strip()
    input_file.readline() # empty
    
    map = {}
    for line in input_file.readlines():
        match = regex.match(line)
        map[match.group(1)] = (match.group(2), match.group(3))

    print(f"Part 1: {findSteps('AAA', lambda x: x == 'ZZZ')}")

    positions = [key for key in map.keys() if key.endswith('A')]
    steps = [findSteps(position, lambda x: x.endswith('Z')) for position in positions]
    print(f"Part 2: {math.lcm(*steps)}")
