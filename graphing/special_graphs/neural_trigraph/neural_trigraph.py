import numpy as np
import networkx as nx
from networkx.algorithms.flow import maximum_flow
from graphing.special_graphs.neural_trigraph.central_vert import NeuralTriGraphCentralVert
import re
import random
import collections


class NeuralTriGraph():
    """
    A neural tri-grpah is a special case of a tri-partite
    graph. In it, the vertices can be segregated into three
    layers. However unlike a tri-partite graph, connections
    exist only between successive layers (1 and 2; 2 and 3).
    Such graphs describe the layers of a neural network;
    hence the name.
    """
    def __init__(self, left_edges, right_edges):
        self.left_edges = left_edges
        self.right_edges = right_edges
        self.vertices = set(left_edges.flatten())\
                    .union(set(right_edges.flatten()))
        self.layer_1 = set(left_edges[:,0])
        self.layer_2 = set(left_edges[:,1])
        self.layer_3 = set(right_edges[:,1])
        self.layer_1_size = len(self.layer_1)
        self.layer_2_size = len(self.layer_2)
        self.layer_3_size = len(self.layer_3)
        self.layer_1_dict = {}
        for e in left_edges:
            if e[0] not in self.layer_1_dict:
                self.layer_1_dict[e[0]] = set([e[1]])
            else:
                self.layer_1_dict[e[0]].add(e[1])
        self.layer_3_dict = {}
        for e in right_edges:
            if e[1] not in self.layer_3_dict:
                self.layer_3_dict[e[1]] = set([e[0]])
            else:
                self.layer_3_dict[e[1]].add(e[0])
        self.central_vert_dict = create_central_vert_dict(left_edges,\
                                                        right_edges)

    def create_bipartite_graph(self):
        self.flow_graph = nx.DiGraph()
        for ed in self.left_edges:
            ## The vertices from which flow travels only out.
            v1 = "out_layer0_elem" + str(ed[0])
            v2 = "in_layer1_elem" + str(ed[1])
            self.flow_graph.add_edge(v1,v2,capacity=1,weight=1)
        for ed in self.right_edges:
            v1 = "out_layer1_elem" + str(ed[0])
            v2 = "in_layer2_elem" + str(ed[1])
            self.flow_graph.add_edge(v1,v2,capacity=1,weight=1)
        for k in self.central_vert_dict.keys():
            for l in self.central_vert_dict[k].l_edges:
                for r in self.central_vert_dict[k].r_edges:
                    v1 = "out_layer0_elem" + str(l)
                    v2 = "in_layer2_elem" + str(r)
                    self.flow_graph.add_edge(v1,v2,capacity=1,weight=1)
        v1="source"
        for e in self.layer_1:
            v2 = "out_layer0_elem" + str(e)
            self.flow_graph.add_edge(v1,v2,capacity=1,weight=1)
        for e in self.layer_2:
            v2 = "out_layer1_elem" + str(e)
            self.flow_graph.add_edge(v1,v2,capacity=1,weight=1)
        for e in self.layer_3:
            v2 = "out_layer2_elem" + str(e)
            self.flow_graph.add_edge(v1,v2,capacity=1,weight=1)
        v2="sink"
        for e in self.layer_1:
            v1 = "in_layer0_elem" + str(e)
            self.flow_graph.add_edge(v1,v2,capacity=1,weight=1)
        for e in self.layer_2:
            v1 = "in_layer1_elem" + str(e)
            self.flow_graph.add_edge(v1,v2,capacity=1,weight=1)
        for e in self.layer_3:
            v1 = "in_layer2_elem" + str(e)
            self.flow_graph.add_edge(v1,v2,capacity=1,weight=1)

    def determine_layer(self, ind):
        if ind < self.layer_1_size:
            return 0
        elif ind < self.layer_2_size:
            return 1
        else:
            return 2


def create_central_vert_dict(edges1, edges2):
    vert_set = {}
    for e in edges1:
        if e[1] not in vert_set:
            tg = NeuralTriGraphCentralVert(e)
            vert_set[e[1]] = tg
        else:
            vert_set[e[1]].add(e)
    for e in edges2:
        if e[0] not in vert_set:
            tg = NeuralTriGraphCentralVert(e)
            vert_set[e[0]] = tg
        else:
            vert_set[e[0]].add(e)
    return vert_set


def is_valid_3_neural(edges1, edges2):
    if min(edges2[::,1])-max(edges1[::,1])!=1:
        return False
    if min(edges1[::,1])-max(edges1[::,0])!=1:
        return False
    if min(edges2[::,1])-max(edges2[::,0])!=1:
        return False
    return True


def tst1():
    ## Test case-1
    edges1 = np.array([[1,4],[2,4],[2,5],[3,5]])
    edges2 = np.array([[4,6],[4,7],[5,8]])
    nu = NeuralTriGraph(edges1, edges2)
    nu.create_bipartite_graph()
    ##For debugging:
    [e for e in nu.flow_graph.edges]
    flow_val, flow_dict = nx.maximum_flow(nu.flow_graph, 'source', 'sink')
    #paths = max_matching_to_paths(flow_dict)

    ## Test case-2
    edges1 = np.array([[1,5],[2,5],[3,7],[4,6]])
    edges2 = np.array([[5,8],[5,9],[5,10],[7,11],[6,11]])

