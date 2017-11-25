import networkx as nx
import os

record_dict = {}
files = ["./tree/" + f for f in os.listdir('./tree/') ]
for file in files:
    name = "_".join(file.split('/')[-1][:-4].split('_')[:-1])
    if name not in record_dict.keys():
        record_dict[name] = []
    G = nx.DiGraph(nx.drawing.nx_pydot.read_dot(file))
    nodes = len([x for x in G.nodes_iter() ])
    leaves = len([x for x in G.nodes_iter() if G.out_degree(x)==0 and G.in_degree(x)==1])
    record_dict[name].append([nodes, leaves])
    print file, name, nodes, leaves, len(record_dict.keys())


import pickle
pickle.dump(record_dict, open('output.p', 'w'))

