# -*- coding: utf-8 -*-

import pulp
import numpy as np
import networkx as nx
from itertools import product
from bipartite_wm import sample_graph

def weighted_b_matching_lp(G, Nl, Nr, capL, capR):
    prob = pulp.LpProblem('Bipartite Weighted b-Matching', pulp.LpMaximize)
    v_names = []
    for l, r in product(range(Nl), range(Nr)):
        v_names.append('{}{}'.format(l, r + Nl))
    vars = pulp.LpVariable.dicts('E', v_names, 0, 1, cat="Integer")
    obj = pulp.lpSum(G[l][Nl + r]['weight'] * vars['{}{}'.format(l, Nl + r)] for (l, r) in product(range(Nl), range(Nr)))
    prob.setObjective(obj)
    for l, r in product(range(Nl), range(Nr)):
        vn = "{}{}".format(l, Nl + r)
        # vn2 = "{}{}".format(v, u)
        prob += vars[vn] <= 1
        # prob += (vars[vn1] + vars[vn2] <= 1)

    # left
    for idl, vl in enumerate(range(Nl)):
        cand = [(u, vl) if u < vl else (vl, u) for u in G.neighbors(vl)]
        cons_v = pulp.lpSum([vars["{}{}".format(v, u)] for v, u in cand])
        prob += cons_v <= capL[idl]

    # right
    for idr, vr in enumerate(range(Nl + 1, Nl + Nr)):
        cand = [(u, vr) if u < vr else (vr, u) for u in G.neighbors(vr)]
        cons_v = pulp.lpSum([vars["{}{}".format(v, u)] for v, u in cand])
        prob += cons_v <= capR[idr]

    # print(prob)
    status = prob.solve()
    # print(pulp.LpStatus[status])
    ans = []
    for (u, v) in G.edges():
        vn = "{}{}".format(u, v)
        if vars[vn].value() > 0:
            ans.append((u, v))
    return ans

if __name__ == '__main__':
    Nl, Nr = 3, 4
    G = sample_graph(Nl, Nr)
    print(G.nodes())
    print(G.edges())
    capL = [2, 1, 1]
    capR = [1, 1, 1, 1]
    wm = weighted_b_matching_lp(G, Nl, Nr, capL, capR)
    print(wm)
