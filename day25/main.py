import networkx as nx
from itertools import combinations
import os

with open(os.path.join(os.path.dirname(__file__), 'input.txt'), 'r') as input_file:
    G = nx.Graph()
    for line in input_file.read().splitlines():
        nodes = line.split()
        origin = nodes[0][:-1]
        for destination in nodes[1:]:
            G.add_edge(origin, destination, capacity=1)

    node_combinations = combinations(G.nodes, r=2)
    for s, t in node_combinations:
        _, partition = nx.minimum_cut(G, s, t)
        reachable, non_reachable = partition
        cutset = set()
        for u, nbrs in ((n, G[n]) for n in reachable):
            cutset.update((u, v) for v in nbrs if v in non_reachable)

        if len(cutset) == 3:
            print(len(reachable) * len(non_reachable))
            break # I have no idea why this returns the same value for each combo, but I am not complaining.