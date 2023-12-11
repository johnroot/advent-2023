import os
import sys

class MapNode:
    def __init__(self, char, north, west):
        self.char = char
        self.is_ground = char == '.'

        self.distance = None
        if (char == 'S'):
            self.distance = 0

        self.north = None
        self.east = None
        self.south = None
        self.west = None
        if north != None and self.goes_north() and north.goes_south():
            self.north = north
            north.set_south(self)
        
        if west != None and self.goes_west() and west.goes_east():
            self.west = west
            west.set_east(self)

    def goes_north(self):
        return self.char in ['S', '|', 'L', 'J']
    
    def goes_east(self):
        return self.char in ['S', '-', 'L', 'F']
    
    def goes_south(self):
        return self.char in ['S', '|', '7', 'F']
    
    def goes_west(self):
        return self.char in ['S', '-', 'J', '7']
    
    def set_south(self, other):
        self.south = other

    def set_east(self, other):
        self.east = other
    
    def get_neighboring_pipes(self):
        pipes = [self.north, self.east, self.south, self.west]
        return list(filter(None, pipes))

    def set_distance(self, distance) -> bool:
        if (self.distance == None or distance < self.distance):
            self.distance = distance
            return True
        
        return False


class Maze:
    def __init__(self, input: list[str]):
        self.map = [ [None]*len(input[0]) for _ in range(len(input)) ]
        self.distance = [ [sys.maxsize]*len(input[0]) for _ in range(len(input)) ]
        for x, line in enumerate(input):
            for y, char in enumerate(line):
                north = (self.map[x - 1][y] if x > 0 else None)
                west = (self.map[x][y - 1] if y > 0 else None)
                self.map[x][y] = MapNode(char, north, west)
                if char == 'S':
                    self.start = (x, y)

    def __repr__(self):
        self.__str()

    def __str__(self):
        string = ""
        for row in self.map:
            for node in row:
                if node.distance != None:
                    string += node.distance
                else:
                    string += " "
            
            string += '\n'
        
        return string

    def calculate_distances(self):
        start = self.map[self.start[0]][self.start[1]]
        nodes = start.get_neighboring_pipes()

        distance = 1
        while len(nodes) > 0:
            advance = [node for node in nodes if node.set_distance(distance)]
            connecting = [node.get_neighboring_pipes() for node in advance]
            nodes = [node for neighbors in connecting for node in neighbors]
            distance += 1

    def calculate_enclosure(self):
        enclosure = 0
        for x, row in enumerate(self.map):
            for y, node in enumerate(row):
                if node.distance == None:
                    crosses = 0
                    x2,y2 = x,y
                    while x2 < len(self.map) and y2 < len(self.map[0]):
                        node = self.map[x2][y2]
                        if (node.distance != None and node.char not in ['L', '7']):
                            crosses +=1
                        x2 += 1
                        y2 += 1
                    
                    if crosses % 2 == 1:
                        enclosure += 1

        return enclosure

with open(os.path.join(os.path.dirname(__file__), 'input.txt'), 'r') as input_file:
    lines = input_file.read().splitlines()
    maze = Maze(lines)

    maze.calculate_distances()
    # print(maze)
    distance = max(node.distance for row in maze.map for node in row if node.distance != None)
    print(f"Part 1: {distance}")
    
    print(f"Part 2: {maze.calculate_enclosure()}")
