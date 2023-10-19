from PageRankAlgorithme import page_rank_algo, draw_graph, nx_pagerank
import pandas as pd
pd.set_option('display.max_columns', None)

pagerank, graph = page_rank_algo(path='xml_files/graph.xml', d_factor=0.85, threshold=0.01)
nx_pagerank = nx_pagerank(graph)
print("******************************************")
print('using pagerank built in function in networkx: ')
print('---------------------------------------------')
print(nx_pagerank)
print("******************************************")
print("******************************************")
print('using simple iterative pagerank algorithm: ')
print('------------------------------------------')
print(pagerank)
print("******************************************")
draw_graph(graph)
