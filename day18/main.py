import os

def calculate_area(plans):
    hole = [(0, 0)]
    perimeter = 0
    for direction, meters in plans:
        x, y = hole[-1]
        perimeter += meters
        match direction:
            case 'U':
                hole.append((x + meters, y))
            case 'D':
                hole.append((x - meters, y))
            case 'L':
                hole.append((x, y - meters))
            case 'R':
                hole.append((x, y + meters))

    area = 0
    for i in range(len(hole)):
        x1, y1 = hole[i]
        x2, y2 = hole[(i + 1) % len(hole)]
        area += (x1 * y2 - x2 * y1)

    return (abs(area) / 2) + (perimeter / 2) + 1

with open(os.path.join(os.path.dirname(__file__), 'input.txt'), 'r') as input_file:
    plans = [line.split() for line in input_file.read().splitlines()]
    print(f"Part 1: {calculate_area([(direction, int(meters)) for direction, meters, _ in plans])}")

    directions = ['R', 'D', 'L', 'U']
    decoded_plans = [(directions[int(hex_code[7])], int(hex_code[2:7], 16)) for _, _, hex_code in plans]
    print(f"Part 2: {calculate_area(decoded_plans)}")
