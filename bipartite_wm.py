# -*- coding: utf-8 -*-

import pulp
import numpy as np
import networkx as nx
from itertools import product
from gen_wm import weighted_matching_lp

def sample_graph(Nl, Nr, debug_print=False):
    G = nx.Graph()
    Nl = 3
    Nr = 4
    for l in range(Nl):
        G.add_node(l)
    for r in range(Nr):
        G.add_node(r + Nl)
    for l, r in product(range(Nl), range(Nr)):
        wlr = np.random.randint(1, 10)
        if debug_print:
            print(l, r, wlr)
        G.add_edge(l, r, weight=wlr)
    return G


if __name__ == '__main__':
    Nl, Nr = 3, 4
    G = sample_graph(Nl, Nr)
    wm = weighted_matching_lp(G)
    print(wm)
