# -*- coding: utf-8 -*-

import networkx as nx
import pulp

def weighted_matching_lp(G):
    prob = pulp.LpProblem('WM', pulp.LpMaximize)
    v_names = []
    for (u, v) in G.edges():
        v_names.append('{}{}'.format(u, v))
    vars = pulp.LpVariable.dicts('E', v_names, 0, 1, cat="Integer")
    obj = pulp.lpSum(G[u][v]['weight'] * vars['{}{}'.format(u, v)] for (u, v) in G.edges())
    prob.setObjective(obj)
    for (u, v) in G.edges():
        vn = "{}{}".format(u, v)
        # vn2 = "{}{}".format(v, u)
        prob += vars[vn] <= 1
        # prob += (vars[vn1] + vars[vn2] <= 1)
    for v in G.nodes():
        # prob += pulp.lpSum([vars["{}{}".format(v, u)] for u in G.neighbors(v)]) <= 1
        cand = []
        for u in G.neighbors(v):
            if v < u:
                cand.append((v, u))
            else:
                cand.append((u, v))
        cons_v = pulp.lpSum([vars["{}{}".format(v, u)] for v, u in cand])
        prob += cons_v <= 1

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
    G = nx.Graph()
    G.add_nodes_from(['a', 'b', 'c', 'd', 'e', 'f'])
    G.add_edge('a', 'b', weight=2)
    G.add_edge('a', 'c', weight=6)
    G.add_edge('a', 'd', weight=5)
    G.add_edge('b', 'c', weight=3)
    G.add_edge('b', 'd', weight=4)
    G.add_edge('c', 'e', weight=7)
    G.add_edge('d', 'e', weight=3)
    G.add_edge('d', 'f', weight=2)
    G.add_edge('e', 'f', weight=7)
    wm = weighted_matching_lp(G)
    print(wm)
