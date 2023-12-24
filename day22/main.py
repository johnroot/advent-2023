from __future__ import annotations

import os
import sys


class Brick:
    def __init__(self, x: range, y: range, z: range):
        self.x = x
        self.y = y
        self.z = z
        self.supports = set()
        self.supported_by = set()

    def descend(self):
        self.z = range(self.z.start - 1, self.z.stop - 1)

    def add_supports(self, other: Brick):
        self.supports.add(other)

    def add_supported_by(self, bricks: list[Brick]):
        self.supported_by |= set(bricks)

    def can_be_disintegrated(self):
        if len(self.supports) == 0:
            return True
        
        return all(len(other.supported_by) > 1 for other in self.supports)



def intersect(x: range, y: range):
    return len(range(max(x.start, y.start), min(x.stop, y.stop))) > 0


def settle(bricks: set[Brick]) -> bool:
    for brick in sorted(bricks, key=lambda b: b.z.start):
        while brick.z.start > 1:
            supported_by = [other for other in bricks if other != brick and intersect(brick.x, other.x) and intersect(brick.y, other.y) and brick.z.start == other.z.stop]
            if len(supported_by) > 0:
                brick.add_supported_by(supported_by)
                for other in supported_by:
                    other.add_supports(brick)
                break
            
            brick.descend()


with open(os.path.join(os.path.dirname(__file__), 'input.txt'), 'r') as input_file:
    brick_descriptions = [tuple(line.split('~')) for line in input_file.read().splitlines()]
    bricks = set()

    for start, end in brick_descriptions:
        x1, y1, z1 = (int(i) for i in start.split(','))
        x2, y2, z2 = (int(i) for i in end.split(','))
        bricks.add(Brick(range(x1, x2 + 1), range(y1, y2 + 1), range(z1, z2 + 1)))

    print("Settling bricks...")
    settle(bricks)

    safe_bricks = len(list(filter(lambda b: b.can_be_disintegrated(), bricks)))

    print(f"Part 1: {safe_bricks}")

    chain_reactions = 0
    for brick in bricks:
        falling_bricks = set([brick])
        testing_bricks = set(brick.supports)
        while len(testing_bricks) > 0:
            test = testing_bricks.pop()
            if len(test.supported_by - falling_bricks) == 0:
                falling_bricks.add(test)
                testing_bricks.update(test.supports)

        chain_reactions += len(falling_bricks - set([brick]))

    print(f"Part 2: {chain_reactions}")