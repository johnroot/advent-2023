import os
import re
from math import prod

MAX = 4000

def _invert(r):
    if r.start > 1:
        return range(1, r.start)
    return range(r.stop, MAX + 1)

def _intersect(r1, r2):
    return range(max(r1.start, r2.start), min(r1.stop, r2.stop))

def _replace(d, key, value):
    new = dict()
    for k, v in d.items():
        new[k] = value if k == key else v
    return new

with open(os.path.join(os.path.dirname(__file__), 'input.txt'), 'r') as input_file:
    workflows_and_parts = input_file.read().split('\n\n')
    workflows = {}

    for workflow_string in workflows_and_parts[0].split('\n'):
        i = workflow_string.index('{')
        name = workflow_string[:i]
        rules_list = workflow_string[i+1:len(workflow_string)-1]
        rules = []
        for rule_input in rules_list.split(','):
            rule_parts = rule_input.split(':')
            if len(rule_parts) == 1:
                exit = rule_input
            else:
                category, op, value = rule_parts[0][0], rule_parts[0][1], int(rule_parts[0][2:])
                if op == '<':
                    rules.append((category, range(1, value), rule_parts[1]))
                elif op == '>':
                    rules.append((category, range(value + 1, MAX + 1), rule_parts[1]))

        workflows[name] = (rules, exit)

    accepted_sum = 0
    for part_string in workflows_and_parts[1].split('\n'):
        pairs = re.findall(r'(\w+)=(\d+)', part_string)
        part = {key: int(value) for key, value in pairs}

        workflow_id = 'in'
        while workflow_id in workflows:
            rules, exit = workflows[workflow_id]
            for category, valid_range, workflow_id in rules:
                if part[category] in valid_range:
                    break
            else:
                workflow_id = exit

        if workflow_id == 'A':
            accepted_sum += sum(part.values())

    print(f"Part 1: {accepted_sum}")

    possibilities = 0
    queue = [("in", { category: range(1, 4001) for category in 'xmas'})]
    while queue:
        workflow_id, ranges = queue.pop()
        if workflow_id == 'A':
            possibilities += prod(len(r) for r in ranges.values())
        elif workflow_id in workflows:
            rules, exit = workflows[workflow_id]
            for category, valid_range, workflow_id in rules:
                new_range = _intersect(valid_range, ranges[category])
                if new_range:
                    queue.append((workflow_id, _replace(ranges, category, new_range)))
                old_range = _intersect(_invert(valid_range), ranges[category])
                if not old_range:
                    break
                ranges[category] = old_range
            else:
                queue.append((exit, ranges))

    print(f"Part 2: {possibilities}")