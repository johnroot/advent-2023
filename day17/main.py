import os
import sys
import heapq
from itertools import product
from enum import IntEnum

Direction = IntEnum('Direction', ['UP', 'RIGHT', 'DOWN', 'LEFT'])

def go(x, y, direction) -> tuple[int, int]:
    match direction:
        case Direction.UP:
            return (x-1, y)
        case Direction.DOWN:
            return (x+1, y)
        case Direction.LEFT:
            return (x, y-1)
        case Direction.RIGHT:
            return (x, y+1)


def get_turns(direction):
    match direction:
        case Direction.UP:
            return [Direction.LEFT, Direction.RIGHT]
        case Direction.RIGHT:
            return [Direction.UP, Direction.DOWN]
        case Direction.DOWN:
            return [Direction.LEFT, Direction.RIGHT]
        case Direction.LEFT:
            return [Direction.UP, Direction.DOWN]
        case None:
            return list(Direction)

def generate_moves(x, y, previous, steps, directions, city):
    for direction in directions:
        new_steps = steps + 1 if direction == previous or previous == None else 1
        new_x, new_y = go(x, y, direction)
        if new_x >= 0 and new_y >= 0 and new_x < len(city) and new_y < len(city[0]):
            yield (new_x, new_y, direction, new_steps)

def move_crucible(x, y, previous, steps, city):
    directions = get_turns(previous)
    
    if steps < 3 and previous != None:
        directions.append(previous)

    return generate_moves(x, y, previous, steps, directions, city)


def move_ultra_crucible(x, y, previous, steps, city):
    directions = []
    if steps >= 4:
        directions += get_turns(previous)
    if steps < 10 and previous != None:
        directions.append(previous)
    if len(directions) == 0:
        directions = list(Direction)

    return generate_moves(x, y, previous, steps, directions, city)


with open(os.path.join(os.path.dirname(__file__), 'input.txt'), 'r') as input_file:
    city = [list(line) for line in input_file.read().splitlines()]
    get_heat = lambda coord: int(city[coord[0]][coord[1]])

    start = (0, 0, None, 0)
    end = (len(city) - 1, len(city[0]) - 1)
    
    heat = {}
    for x in range(0, len(city)):
        for y in range(0, len(city[0])):
            for previous_direction in Direction:
                for same_direction in range(0, 11):
                    heat[(x, y, previous_direction, same_direction)] = sys.maxsize
    heat[start] = 0

    queue = [(0, start)]

    while len(queue) > 0:
        curr_heat, status = heapq.heappop(queue)
        # neighbors = move_crucible(*status, city)
        neighbors = move_ultra_crucible(*status, city)
        for neighbor in neighbors:
            new_heat = curr_heat + get_heat(neighbor)
            if new_heat < heat[neighbor]:
                heat[neighbor] = new_heat
                heapq.heappush(queue, (new_heat, neighbor))


    result = min({ k: v for k, v in heat.items() if k[0] == end[0] and k[1] == end[1] and k[3] >= 4 }.values())
    print(f"Minimum Heat Loss: {result}")