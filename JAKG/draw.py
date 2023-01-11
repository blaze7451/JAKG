from JAKG.extraction import Preprocessing
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

class KG_graph():
    def __init__(self, text:str):
        self.text = text
        preprocess = Preprocessing()
        sentlist = preprocess.get_sentlist(self.text)
        self.rdf_pairs1 = []
        self.rdf_pairs2 = []
        for i in sentlist:
            j1, j2 = preprocess.get_rdf_tuples(i)
        for k1 in j1:
            self.rdf_pairs1.append(k1)
        for k2 in j2:
            self.rdf_pairs2.append(k2)
        self.all_pairs = preprocess.get_all_tuples(self.rdf_pairs1, self.rdf_pairs2)
        self.kg_dataset = preprocess.get_kg_dataset(self.all_pairs)

    def draw_kg(self):
        G = nx.from_pandas_edgelist(self.kg_dataset, "head", "tail", edge_attr=True, create_using=nx.MultiDiGraph())
        plt.figure(figsize=(12,12))
        node_sizes = [value*1000 for _, value in G.degree()]
        pos = nx.spring_layout(G)
        kg_graph = nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos = pos, node_size=node_sizes)
        plt.rcParams['font.sans-serif'] = 'MS Gothic'
        plt.show()

    def get_kg_info(self, G):
        print("The number of edges in knowledge graph is:", nx.number_of_edges(G))
        print("---------------------------------------------------------------------")
        print("The number of nodes in knowledge graph is:", nx.number_of_nodes(G))
        print("---------------------------------------------------------------------")
        print("The degree of graph:", G.degree())

    def get_degree_values(self, G):
        degree_values = [value for key, value in G.degree()]

        return degree_values 