import os

def generate_edges(trails):
    edges = {}
    for x, row in enumerate(trails):
        for y, char in enumerate(row):
            if char == '.':
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ax, ay = x + dx, y + dy
                    if not 0 <= ax < len(trails) and 0 <= ay < len(row):
                        continue
                    if trails[ax][ay] == '.':
                        edges.setdefault((ax, ay), set()).add((x, y, 1))
                        edges.setdefault((x, y), set()).add((ax, ay, 1))
            elif char == '>':
                edges.setdefault((x, y), set()).add((x, y + 1, 1))
                edges.setdefault((x, y - 1), set()).add((x, y, 1))
            elif char == 'v':
                edges.setdefault((x, y), set()).add((x + 1, y, 1))
                edges.setdefault((x - 1, y), set()).add((x, y, 1))

    return edges

def merge_edges(edges):
    while True:
        for key, connections in edges.items():
            if len(connections) == 2:
                forward, backward = connections
                edges[forward[:2]].remove(key + (forward[2],))
                edges[backward[:2]].remove(key + (backward[2],))
                edges[forward[:2]].add((backward[0], backward[1], forward[2] + backward[2]))
                edges[backward[:2]].add((forward[0], forward[1], forward[2] + backward[2]))
                del edges[key]
                break
        else:
            break

def find_longest_hike(edges, destination):
    stack = [(0, 0, 1)]
    visited = set()
    farthest_distance = 0
    while stack:
        dist, x, y = stack.pop()
        if dist == -1:
            visited.remove((x, y))
            continue
        if (x, y) == destination:
            farthest_distance = max(farthest_distance, dist)
            continue
        if (x, y) in visited:
            continue
        visited.add((x, y))
        stack.append((-1, x, y))
        for ax, ay, ddist in edges[(x, y)]:
            stack.append((dist + ddist, ax, ay))

    return farthest_distance

with open(os.path.join(os.path.dirname(__file__), 'input.txt'), 'r') as input_file:
    trails = [list(line) for line in input_file.read().splitlines()]
    
    edges = generate_edges(trails)
    destination = (len(trails) - 1, len(trails[0]) - 2)

    print(f"Part 1: {find_longest_hike(edges, destination)}")

    trails = [[char.replace('v', '.').replace('>', '.') for char in line] for line in trails]
    edges = generate_edges(trails)
    merge_edges(edges)
    print(f"Part 2: {find_longest_hike(edges, destination)}")
