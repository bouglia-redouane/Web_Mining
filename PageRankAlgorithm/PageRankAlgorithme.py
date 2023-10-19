import numpy as np
import networkx as nx
from lxml import etree
import matplotlib.pyplot as plt
import pandas as pd

def get_graph_from_file(path):
    tree = etree.parse(path)
    nodes = tree.xpath('//node')
    nodes_name = tree.xpath('//node/@name')
    edges = []
    for i, node in enumerate(nodes):
        links = node.xpath('link/text()')
        if links:
            origine = nodes_name[i]
            for link in links:
                edges.append((origine, link, {'weight': 1}))
    G = nx.DiGraph()
    G.add_nodes_from(nodes_name)
    G.add_edges_from(edges)
    return G
def calculate_p_matrix(a_matrix, N, d_factor):
    tmp = np.zeros((N, N))
    for i, row in enumerate(a_matrix):
        row_sum = sum(row)
        for j, val in enumerate(row):
            if row_sum == 0:
                tmp[i, j] = 1 / N
            else:
                tmp[i, j] = (d_factor * (val / row_sum)) + (1 - d_factor) * (1 / N)
    return tmp


def page_rank_algo(**kwargs):
    r_vects = []
    if 'path' in kwargs.keys():
        graph = get_graph_from_file(kwargs['path'])
        a_matrix, N = nx.adjacency_matrix(graph).toarray(), len(graph.nodes)
    else:
        graph = kwargs['graph']
        a_matrix, N = nx.adjacency_matrix(graph).toarray(), len(kwargs['graph'].nodes)
    p_matrix = calculate_p_matrix(a_matrix, N, kwargs['d_factor'])
    r_vects.append(np.ones((1, N)) / N)
    i = 0
    while True:
        r_vects.append(np.dot(r_vects[i], p_matrix))
        if np.abs(r_vects[i + 1] - r_vects[i]).all() <= kwargs['threshold']:
            break
        i += 1
    return pd.DataFrame(r_vects[-1]*100, columns=list(graph.nodes), index=['score']).round(1), graph

def draw_graph(G):
    pos = nx.circular_layout(G)
    scale_factor = 0.5
    pos = {node: (x * scale_factor, y * scale_factor) for node, (x, y) in pos.items()}
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1000, font_size=12, font_color='black')
    #plt.show(block=False)
    #plt.pause(10)
    plt.show()

def nx_pagerank(G):
    pagerank = nx.pagerank(G, alpha=0.85)
    return (pd.DataFrame(pagerank, index=['score'])*100).round(1)