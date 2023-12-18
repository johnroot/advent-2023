import os
from enum import Enum

Direction = Enum('Direction', ['UP', 'DOWN', 'LEFT', 'RIGHT'])
traversed = set()

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


def traverse(x, y, direction, contraption, energized):
    while x >= 0 and y >= 0 and x < len(contraption) and y < len(contraption[0]):
        instruction = (x, y, direction)
        if (instruction in traversed):
            break
        traversed.add(instruction)

        energized[x][y] = '#'
        tile = contraption[x][y]
        
        match tile:
            case '.':
                x, y = go(x, y, direction)
            case '/':
                match direction:
                    case Direction.UP:
                        direction = Direction.RIGHT
                    case Direction.DOWN:
                        direction = Direction.LEFT
                    case Direction.LEFT:
                        direction = direction.DOWN
                    case Direction.RIGHT:
                        direction = direction.UP
                
                x, y = go(x, y, direction)
            case '\\':
                match direction:
                    case Direction.UP:
                        direction = Direction.LEFT
                    case Direction.DOWN:
                        direction = Direction.RIGHT
                    case Direction.LEFT:
                        direction = direction.UP
                    case Direction.RIGHT:
                        direction = direction.DOWN
                
                x, y = go(x, y, direction)
            case '-':
                if direction == direction.LEFT or direction == direction.RIGHT:
                    x, y = go(x, y, direction)
                else:
                    new_x, new_y = go(x, y, Direction.LEFT)
                    traverse(new_x, new_y, Direction.LEFT, contraption, energized)
                    direction = direction.RIGHT
                    x, y = go(x, y, direction)
            case '|':
                if direction == direction.UP or direction == direction.DOWN:
                    x, y = go(x, y, direction)
                else:
                    new_x, new_y = go(x, y, Direction.UP)
                    traverse(new_x, new_y, Direction.UP, contraption, energized)
                    direction = direction.DOWN
                    x, y = go(x, y, direction)

    return sum(1 if tile == '#' else 0 for row in energized for tile in row)

with open(os.path.join(os.path.dirname(__file__), 'input.txt'), 'r') as input_file:
    contraption = [list(line) for line in input_file.read().splitlines()]
    part_1 = traverse(0, 0, Direction.RIGHT, contraption, [['.' for _ in row] for row in contraption])
    print(f"Part 1: {part_1}")

    all_entries = []
    all_entries += [(x, 0, Direction.RIGHT) for x in range(0, len(contraption))]
    all_entries += ((x, len(contraption[0]) - 1, Direction.LEFT) for x in range(0, len(contraption)))
    all_entries += ((0, y, Direction.DOWN) for y in range(0, len(contraption[0])))
    all_entries += ((len(contraption) - 1, y, Direction.UP) for y in range(0, len(contraption[0])))

    traversed.clear()
    all_results = []
    for entry in all_entries:
        all_results.append(traverse(*entry, contraption, [['.' for _ in row] for row in contraption]))
        traversed.clear()
    
    print(f"Part 2: {max(all_results)}")