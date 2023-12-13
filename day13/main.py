import os

transpose = lambda pattern: [''.join(row) for row in zip(*pattern)]
get_diff = lambda pattern, x, y: sum(c1 != c2 for c1, c2 in zip(pattern[x], pattern[y]))

def find_symmetry(pattern, max_diff):
    adjacent = [i for i in zip(range(0, len(pattern) - 1), range(1, len(pattern))) if get_diff(pattern, i[0], i[1]) <= max_diff]
    
    for x, y in adjacent:
        diff = 0
        x2 = x
        y2 = y
        while x2 > -1 and y2 < len(pattern):
            diff += get_diff(pattern, x2, y2)
            if (diff > max_diff):
                break

            x2 -= 1
            y2 += 1

        if (x2 == -1 or y2 == len(pattern)) and diff == max_diff:
            return x + 1
    
    return None

def summarize_notes(patterns, smudges):
    total = 0
    for pattern in patterns:
        if reflection := find_symmetry(pattern, smudges):
            total += 100 * reflection
        elif reflection := find_symmetry(transpose(pattern), smudges):
            total += reflection

    return total

with open(os.path.join(os.path.dirname(__file__), 'input.txt'), 'r') as input_file:
    patterns = [input.split('\n') for input in input_file.read().split('\n\n')]
    
    print(f"Part 1: {summarize_notes(patterns, 0)}")
    print(f"Part 2: {summarize_notes(patterns, 1)}")
