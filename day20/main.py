from __future__ import annotations

import os
from enum import Enum
from collections import deque
from abc import ABC, abstractmethod
from math import lcm

Pulse = Enum('Pulse', ['HI', 'LO'])
PulseQueue = deque()

class Module(ABC):
    HI_PULSES = 0
    LO_PULSES = 0

    def __init__(self, name):
        self.name = name

    def add_destinations(self, destinations: list[Module]):
        self.destinations = destinations

    def process_pulse(self, origin: Module, pulse: Pulse):
        if (pulse == Pulse.HI):
            Module.HI_PULSES += 1
        else:
            Module.LO_PULSES += 1
        return
    
    def __repr__(self):
        return f"{self.name} -> {[dest.name for dest in self.destinations]}"
    
class Broadcaster(Module):
    def process_pulse(self, origin: Module, pulse: Pulse):
        super().process_pulse(origin, pulse)
        for module in self.destinations:
            PulseQueue.append((module, self, pulse))

class FlipFlop(Module):
    def __init__(self, name):
        super().__init__(name)
        self.is_on = False

    def process_pulse(self, origin: Module, pulse: Pulse):
        super().process_pulse(origin, pulse)
        if pulse == Pulse.LO:
            output = Pulse.LO if self.is_on else Pulse.HI
            self.is_on = not self.is_on
            for module in self.destinations:
                PulseQueue.append((module, self, output))

class Conjunction(Module):
    def __init__(self, name):
        super().__init__(name)
        self.last_input = {}

    def add_input(self, input):
        self.last_input[input] = Pulse.LO

    def process_pulse(self, origin, pulse: Pulse):
        super().process_pulse(origin, pulse)
        self.last_input[origin] = pulse
        output = Pulse.LO if all(p == Pulse.HI for p in self.last_input.values()) else Pulse.HI
        for module in self.destinations:
            PulseQueue.append((module, self, output))

class Dummy(Module):
    def process_pulse(self, origin: Module, pulse: Pulse):
        return super().process_pulse(origin, pulse)

def parse_modules():
    with open(os.path.join(os.path.dirname(__file__), 'input.txt'), 'r') as input_file:
        modules = {}
        configs = input_file.read().splitlines()
        module_names = [config.split(' -> ')[0] for config in configs]
        for module in module_names:
            if module == 'broadcaster':
                modules[module] = Broadcaster(module)
            elif module[0] == '%':
                name = module[1:]
                modules[name] = FlipFlop(name)
            elif module[0] == '&':
                name = module[1:]
                modules[name] = Conjunction(name)

        configs = [(config.split(' -> ')[0][1:], config.split(' -> ')[1].split(', ')) for config in configs]
        for source, destinations in configs:
            destinations = [modules[name] if name in modules else Dummy(name) for name in destinations]
            if source == 'roadcaster':
                source = 'broadcaster'
            modules[source].add_destinations(destinations)
            for destination in destinations:
                if isinstance(destination, Conjunction):
                    destination.add_input(modules[source])

    return modules

def part_one():
    modules = parse_modules()
    for _ in range(0, 1000):
        PulseQueue.append((modules['broadcaster'], Dummy("button"), Pulse.LO))
        while len(PulseQueue) > 0:
            module, origin, pulse = PulseQueue.popleft()
            module.process_pulse(origin, pulse)

    print(f"Part 1: {Module.LO_PULSES * Module.HI_PULSES}")

def part_two():
    modules = parse_modules()
    cl_inputs = {name: None for name in ['js', 'qs', 'dt', 'ts']}
    button_presses = 0
    while True:
        button_presses += 1
        
        PulseQueue.append((modules['broadcaster'], Dummy("button"), Pulse.LO))
        while len(PulseQueue) > 0:
            module, origin, pulse = PulseQueue.popleft()
            if (origin.name in cl_inputs and pulse == Pulse.HI):
                cl_inputs[origin.name] = button_presses

            module.process_pulse(origin, pulse)
        
        if all(value != None for value in cl_inputs.values()):
            break

    print(f"Part 2: {lcm(*cl_inputs.values())}")

part_one()
part_two()