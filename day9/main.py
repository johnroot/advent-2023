import os

def predict(history, index, operation) -> int:
    differences = [j-i for i, j in zip(history[:-1], history[1:])]
    if all(diff == 0 for diff in differences):
        return history[index]
    
    return operation(history[index], predict(differences, index, operation))

with open(os.path.join(os.path.dirname(__file__), 'input.txt'), 'r') as input_file:
    lines = input_file.readlines()
    print(f"Part 1: {sum([predict([int(x) for x in line.split()], -1, lambda x, y: x + y) for line in lines])}")
    print(f"Part 2: {sum([predict([int(x) for x in line.split()], 0, lambda x, y: x - y) for line in lines])}")