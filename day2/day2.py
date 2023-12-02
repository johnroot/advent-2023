import re
import os

class Cubes:
    def __init__(self, red, blue, green):
        self.red = self.parseInt(red)
        self.blue = self.parseInt(blue)
        self.green = self.parseInt(green)

    def parseInt(self, val) -> int:
        return int(val) if val != None else 0

    def isValid(self) -> bool:
        return self.red <= 12 and self.blue <= 14 and self.green <= 13
    
    def power(self) -> int:
        return self.red * self.blue * self.green
    
    def condense(self, other):
        self.red = max(self.red, other.red)
        self.blue = max(self.blue, other.blue)
        self.green = max(self.green, other.green)
    
    def __str__(self):
        return f'{self.red} red, {self.blue} blue, {self.green} green'


game_regex = re.compile(r'Game (\d+): .+')
cube_regex = re.compile(r'(?:(?:(?:(\d+) red(?:, )?)|(?:(\d+) green(?:, )?)|(?:(\d+) blue(?:, )?))+;?)+')

def get_game_id(game) -> int:
    return int(game_regex.match(game).group(1))


def test_possibility(game) -> bool:
    for reveal in cube_regex.finditer(game):
        cubes = Cubes(red = reveal[1], green = reveal[2], blue = reveal[3])
        # print(f'Input: {reveal}; Output: {cubes}, Possible: {cubes.isValid()}')
        if not cubes.isValid():
            return False
        
    return True


def find_power_of_minimum_cubes(game) -> int:
    minimum_cubes = Cubes(0, 0, 0)
    for reveal in cube_regex.finditer(game):
        cubes = Cubes(red = reveal[1], green = reveal[2], blue = reveal[3])
        minimum_cubes.condense(cubes)

    return minimum_cubes.power()

part_one_result = 0
part_two_result = 0
input = os.path.join(os.path.dirname(__file__), 'input.txt')
if __name__ == '__main__':
    with open(input, 'r') as input_file:
        for game in input_file:
            game_id = get_game_id(game)
            if test_possibility(game):
                part_one_result += game_id
            
            part_two_result += find_power_of_minimum_cubes(game)

    print(f'Part 1: {part_one_result}')
    print(f'Part 2: {part_two_result}')
