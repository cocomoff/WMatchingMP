# -*- coding: utf-8 -*-

import pulp
import numpy as np
import networkx as nx
from itertools import product
from gen_wm import weighted_matching_lp

if __name__ == '__main__':
    G = nx.Graph()
    Nl = 3
    Nr = 4
    for l in range(Nl):
        G.add_node(l)
    for r in range(Nr):
        G.add_node(r + Nl)
    for l, r in product(range(Nl), range(Nr)):
        wlr = np.random.randint(1, 10)
        print(l, r, wlr)
        G.add_edge(l, r, weight=wlr)
    wm = weighted_matching_lp(G)
    print(wm)
