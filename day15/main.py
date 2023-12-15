import os

def HASH(string: str):
    result = 0
    for c in string:
        result += ord(c)
        result *= 17
        result %= 256
    
    return result

find_lens = lambda box, label: next(filter(lambda lens: lens[0] == label, box), None)

with open(os.path.join(os.path.dirname(__file__), 'input.txt'), 'r') as input_file:
    initialization_sequence = input_file.read().strip().split(',')
    print(f"Part 1: {sum(HASH(input) for input in initialization_sequence)}")

    boxes = {i: [] for i in range(0, 256)}

    for input in initialization_sequence:
        if '-' in input:
            label = input[:-1]
            box = HASH(label)
            if existing_lens := find_lens(boxes[box], label):
                boxes[box].remove(existing_lens)
        
        if '=' in input:
            label = input[:-2]
            focal = int(input[-1])
            box = HASH(label)
            if existing_lens := find_lens(boxes[box], label):
                boxes[box] = [(label, focal) if old_label == label else (old_label, old_focal) for old_label, old_focal in boxes[box]]
            else:
                boxes[box].append((label, focal))

    focusing_power = 0
    for box_number, box in boxes.items():
        for i, lens in enumerate(box):
            focusing_power += (box_number + 1) * (i + 1) * lens[1]

    print(f"Part 2: {focusing_power}")
