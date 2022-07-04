import numpy as np
from collections import defaultdict
from graphing.special_graphs.neural_trigraph.rand_graph import neur_trig_edges, rep_graph
from graphing.special_graphs.neurograph.toy_graph import NeuralGraphVert, ToyGraphs
from functools import cmp_to_key
import time


def dfs_search(g, v, t, visited_dict=set()):
    if v.key not in visited_dict:
        visited_dict.add(v.key)
    if v.key == t.key:
        return []
    elif v.layer < t.layer:
        for u in g[v.key]:
            if u.key not in visited_dict:
                res = dfs_search(g, u, t, visited_dict)
                if res is not None:
                    res.append(u.key)
                    return res


def dfs_targeted(g, v, t, path=[], visited_dict=set()):
    if v.key not in visited_dict:
        visited_dict.add(v.key)
    if v.key == t.key:
        return []
    elif v.layer < t.layer:

        # Comparator for preferring vertices close in index to target.
        def compare(x, y):
            return abs(x.layer_ix - t.layer_ix)\
                        - abs(y.layer_ix - t.layer_ix)
        for u in sorted(g[v.key], key=cmp_to_key(compare)):
            if u.key not in visited_dict:
                res = dfs_targeted(g, u, t, path, visited_dict)
                if res is not None:
                    res.append(u.key)
                    return res


def tst():
    g = ToyGraphs.toy_graph_1()
    v1 = NeuralGraphVert(1, 1, 1)
    v7 = NeuralGraphVert(7, 3, 2)
    visited_dict = set()
    path = dfs_targeted(g, v1, v7, visited_dict=visited_dict)
    path.append(v1.key)
    path.reverse()
    print(path)
    print(visited_dict)


def tst_dfs_vanilla():
    g = ToyGraphs.toy_graph_2()
    v1 = NeuralGraphVert(1, 1, 1)
    v11 = NeuralGraphVert(11, 4, 4)
    visited_dict = set()
    path = dfs_search(g, v1, v11, visited_dict=visited_dict)
    path.append(v1.key)
    path.reverse()
    print(path)
    print(visited_dict)


def tst_dfs_targeted():
    g = ToyGraphs.toy_graph_2()
    v1 = NeuralGraphVert(1, 1, 1)
    v11 = NeuralGraphVert(11, 4, 4)
    visited_dict = set()
    path = dfs_targeted(g, v1, v11, visited_dict=visited_dict)
    path.append(v1.key)
    path.reverse()
    print(path)
    print(visited_dict)


if __name__ == "__main__":
    start = time.time()
    tst_dfs_vanilla()
    end = time.time()
    print("Naive DFS took: " + str(end-start) + " secs")
    start = time.time()
    tst_dfs_targeted()
    end = time.time()
    print("Targeted DFS took: " + str(end-start) + " secs")



# Demonstration of call-stack behavior and how None is returned
# if nothing found.
def fn1(a):
    if a == 1:
        return a
    else:
        return fn2(a)


def fn2(a):
    if a == 1:
        return a


def tst_call_stack():
    a = fn1(2)
    print(a is None)


# [1] https://stackoverflow.com/questions/29863851/python-stop-recursion-once-solution-is-found
