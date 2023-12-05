import re
import os
from typing import Optional

class MapRange:
    def __init__(self, range: str):
        values = [int(x) for x in range.split(' ')]
        self.destination = values[0]
        self.source = values[1]
        self.length = values[2]

    def convert(self, input: int) -> Optional[int]:
        if input >= self.source and input <= self.source + self.length:
            return (input - self.source) + self.destination
        
        return None
    
    def deconvert(self, input: int) -> Optional[int]:
        if input >= self.destination and input <= self.destination + self.length:
            return (input - self.destination) + self.source
        
        return None


class AlmanacMap:
    def __init__(self, title: str, ranges: list[str]):
        self.__parseTitle(title)
        self.__ranges = [MapRange(range) for range in ranges]

    def __parseTitle(self, title: str):
        match = re.match(r'(?P<source>\w+)-to-(?P<destination>\w+) map:', title)
        self.source = str(match.group('source'))
        self.destination = str(match.group('destination'))

    def convert(self, input: int) -> int:
        return next(filter(None, map(lambda r: r.convert(input), self.__ranges)), input)
    
    def deconvert(self, input: int) -> int:
        return next(filter(None, map(lambda r: r.deconvert(input), self.__ranges)), input)


def initialize_maps() -> tuple[list[int], dict[str, AlmanacMap]]:
    seeds = []
    maps = {}

    map_title = None
    map_ranges = []

    input = os.path.join(os.path.dirname(__file__), 'input.txt')
    with open(input, 'r') as input_file:
        for line in input_file:
            if len(seeds) == 0:
                seeds = [int(x) for x in line.split(' ')[1:]]
                continue

            if len(line.strip()) == 0:
                if map_title != None and len(map_ranges) > 0:
                    map = AlmanacMap(map_title, map_ranges)
                    maps[map.source] = map
                            
                map_title = None
                map_ranges.clear()
                continue

            if (map_title == None):
                map_title = line
                continue

            map_ranges.append(line)
        
    if map_title != None and len(map_ranges) > 0:
        map = AlmanacMap(map_title, map_ranges)
        maps[map.source] = map

    return [seeds, maps]


def traverse_maps(value: int, data: str, maps: dict[str, AlmanacMap]):
    # print(f'{data} {value}', end = '')
    while (map := maps.get(data)) is not None:
        value = map.convert(value)
        data = map.destination
        # print(f', {data} {value}', end = '')
    
    # print('')
    return value


def reverse_maps(value: int, data: str, maps: dict[str, AlmanacMap]):
    # print(f'{data} {value}', end = '')
    while (map := maps.get(data)) is not None:
        value = map.deconvert(value)
        data = map.source
        # print(f', {data} {value}', end = '')
    
    # print('')
    return value


def main():
    seeds, maps = initialize_maps()

    part_one_locations = [traverse_maps(seed, 'seed', maps) for seed in seeds]
    print(f'Part 1: {min(part_one_locations)}')

    part_two_location = 0
    seed_ranges = list(zip(seeds[0::2], seeds[1::2]))
    is_valid_seed = lambda x: any([(x >= r[0] and x <= r[0] + r[1]) for r in seed_ranges])
    reversed_maps = { m.destination:m for m in maps.values() }
    while not is_valid_seed(reverse_maps(part_two_location, 'location', reversed_maps)):
        part_two_location += 1

    print(f'Part 2: {part_two_location}')

if __name__ == '__main__':
    main()
