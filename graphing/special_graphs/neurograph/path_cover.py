import networkx as nx
from networkx.algorithms import bipartite
from graphing.special_graphs.neural_trigraph.path_cover \
            import min_cover_trigraph, min_cover_trigraph_heuristic1
from graphing.special_graphs.neural_trigraph.rand_graph import neur_trig_edges, rep_graph
from graphing.special_graphs.directed_graph.transitive_closure import transitive_closure
from graphing.special_graphs.neural_trigraph.neural_trigraph import is_valid_3_neural
import random
import time


def create_path_cover(g):
    '''
    idea:
        1. create the bipartite graph. split each node v into two nodes v_top
        and v_bottom, where v_top connects with all outgoing edges of v, and
        v_bottom connects with all incoming edges of v.
        2. use max matching in networkx to generate the matching
        3. recover the path in the transitive closure graph using the
        bipartite graph matching
        4. reference: https://towardsdatascience.com/solving-minimum-path-cover-on-a-dag-21b16ca11ac0
    Parameter: g (dict), the transitive closure of the DAG
    Return: the paths in the transitive closure (list of list)
    '''
    # generate bipartite
    b = nx.Graph()
    top_nodes = []
    bottom_nodes = []
    # generate nodes
    for v in g:
        v_top = str(v) + "t"
        v_bottom = str(v) + "b"
        top_nodes.append(v_top)
        bottom_nodes.append(v_bottom)
    # generate edges
    edges = []
    for v in g:
        nbrs = g[v]
        for u in nbrs:
            v_top = str(v) + "t"
            u_bottom = str(u) + "b"
            edges.append([v_top, u_bottom])

    b.add_nodes_from(top_nodes, bipartite=0)
    b.add_nodes_from(bottom_nodes, bipartite=1)
    b.add_edges_from(edges)

    # calculate maximum cardinality matching
    # matching: a dict maps node to node (both ways, represent edges)
    matching = bipartite.matching.hopcroft_karp_matching(b, top_nodes)

    # generate paths from matching
    paths = []
    visited_nodes = set()
    for v in sorted(g.keys()):
        path = []
        if v not in visited_nodes:
            visited_nodes.add(v)
            path.append(v)
            v_top = str(v) + "t"
            while v_top in matching:
                u_bottom = matching[v_top]
                u = int(u_bottom[:-1])
                path.append(u)
                visited_nodes.add(u)
                v_top = u_bottom[:-1] + "t"
        if len(path) > 0:
            paths.append(path)
    return paths


def recover_path(g):
    '''
    Recover the path in the original graph from the path in the transitive
    graph, using the "trans_path" dict

    Parameter: g, the original graph
    Return: the recovered path
    '''
    original_paths = []
    trans_path, trans_dict = transitive_closure(g)
    ret_paths = create_path_cover(trans_dict)
    for path in ret_paths:
        original_path = []
        for i in range(len(path)-1):
            v = path[i]
            u = path[i+1]
            v_u_path = trans_path[v][u]
            original_path.extend(v_u_path[:-1])
        original_path.append(path[-1])
        original_paths.append(original_path)
    return original_paths


def parent_dict(g):
    '''
    Construct parent_dict: maps node v to node v's parent;
    if a node has no parent, maps to None
    Parameter: the original graph g
    Return: the parent dict
    '''
    parent_dict = {}
    for v in g:
        nbrs = g[v]
        for u in nbrs:
            parent_dict[u] = v
    for v in g:
        if v not in parent_dict:
            parent_dict[v] = None
    return parent_dict


def construct_complete_path(g, paths):
    '''
    some of the original_paths may be incomplete. We want to construct the
    complete paths from the first layer to the last layer
    Parameters:
        g(dict), DAG
        paths (list of list): the incomplete paths returned from 'recover_path'
    Return:
        the complete paths (list of list)
    '''
    # recover the head part
    parent = parent_dict(g)
    for i in range(len(paths)):
        path = paths[i]
        while parent[path[0]] is not None:
            path = [parent[path[0]]] + path
        paths[i] = path
    # recover the tail part
    for path in paths:
        while len(g[path[-1]]) > 0:
            path.append(g[path[-1]][0])
    return paths


def min_path_cover(g):
    '''
    the main function; combines all previous functions
    parameter: g(dict), DAG
    return: the completed, recovered path of g
    '''
    original_paths = recover_path(g)
    return construct_complete_path(g, original_paths)


def graph_converter(edges1, edges2):
    '''
    Parameters: edges1, edges2 (list of list), generated
    from the neur_trig_edges
    return: an adjacent list representation of the graph
    '''
    g = {}
    vertices = set()
    for e in edges1:
        vertices.add(e[0])
    for e in edges2:
        vertices.add(e[0])
        vertices.add(e[1])
    for v in vertices:
        g[v] = []
    for e in edges1:
        g[e[0]].append(e[1])
    for e in edges2:
        g[e[0]].append(e[1])
    return g


def check_path_cover(g, paths):
    '''
    check if the generated paths have covered all vertices, and if the paths
    are valid paths
    Parameters:
        g (adjacent list), DAG
        paths (list of list), the result we obtained
    '''
    parent = parent_dict(g)
    ret_vertices = set()
    for path in paths:
        for v in path:
            ret_vertices.add(v)
    assert len(ret_vertices) == len(g), "not all vertices are covered"
    flag = True
    for path in paths:
        for i in range(len(path)-1):
            current = path[i]
            next = path[i+1]
            if next not in g[current]:
                flag = False
                break
        last = path[-1]
        assert len(g[last]) == 0, "this is not a complete path " + str(path)
        assert parent[path[0]] is None, "this is not a complete path " + str(path)
    assert flag is True, "this is not a correct set of path" + paths


# test case 7
def neuro_trigraph_stack_test(left, center, right, rep):
    '''
    Create test cases by stacking small neurotrigraphs together, repeating
    rep number of times
    Parameters:
        left (int): number of vertices on the left layer
        center (int): number of vertices in the middle layer
        right (int): number of vertices on the right layer
        rep (int): the number of times neurotrigraphs repeating
    '''
    print("left: " + str(left*rep) + ", center:" + str(center*rep) + ", right:" + str(right*rep))
    edges1, edges2 = rep_graph(left, right, center, rep)
    print("Generated the graph.")
    if not is_valid_3_neural(edges1, edges2):
        print("Invalid graph this time")
        return
    start = time.time()
    ans = min_cover_trigraph(edges1,  edges2)
    end = time.time()
    print("Original took: " + str(end-start) + " secs")
    g = graph_converter(edges1, edges2)
    start = time.time()
    paths = min_path_cover(g)
    end = time.time()
    print("New method took: " + str(end-start) + " secs")
    check_path_cover(g, paths)
    print("Original method shows: " + str(len(ans)) + " paths.")
    print("New method shows: " + str(len(paths)) + " paths.")
    assert len(paths) == len(ans), "Number of paths incorrect. Correct number of paths is " + str(len(ans)) +\
        "returned number of path is " + str(len(paths))\
        + "\n edges1" + str(edges1) + "\n edge2" + str(edges2)\
        + "\n g" + str(g) + "\n ans" + str(ans) + "\n paths" + str(paths)


def tst_stack():
    for i in range(100):
        left = int(random.uniform(5, 25))
        center = int(random.uniform(2, 10))
        right = int(random.uniform(5, 25))
        rep = int(random.uniform(10, 100))
        neuro_trigraph_stack_test(left, center, right, rep)
        print("Passed:" + str(i))
        print("#######################\n")


if __name__ == "__main__":
    # test case 1
    g1 = {1: [4], 2: [4, 5], 3: [5], 4: [6, 7], 5: [8], 6: [], 7: [], 8: []}
    paths = min_path_cover(g1)
    check_path_cover(g1, paths)
    assert len(paths) == 3, ("Number of paths incorrect. Correct number" +
                             "of paths is 3, and returned number of path is " + str(len(paths)))

    # test case 2
    g2 = {1: [4], 2: [4, 5], 3: [5], 4: [6], 5: [6], 6: []}
    paths = min_path_cover(g2)
    check_path_cover(g2, paths)
    assert len(paths) == 3, ("Number of paths incorrect. Correct number" +
                             "of paths is 3, and returned number of path is " + str(len(paths)))

    # test case 3
    g3 = {1: [4], 2: [5], 3: [6, 7], 4: [8], 5: [8, 9, 10], 6: [10], 7: [9],
          8: [11, 12], 9: [12], 10: [12, 13], 11: [], 12: [], 13: []}
    paths = min_path_cover(g3)
    check_path_cover(g3, paths)
    assert len(paths) == 4, ("Number of paths incorrect. Correct number" +
                             "of paths is 4, and returned number of path is " + str(len(paths)))

    # test case 4
    g4 = {1: [4], 2: [5], 3: [6, 7], 4: [8], 5: [8], 6: [8, 9], 7: [10], 
          8: [11], 9: [11], 10: [12, 13, 14], 11: [], 12: [], 13: [], 14: []}
    paths = min_path_cover(g4)
    check_path_cover(g4, paths)
    assert len(paths) == 6, ("Number of paths incorrect. Correct number" +
                             "of paths is 6, and returned number of path is " + str(len(paths)))

    # test case 6
    def neuro_trigraph_test(left, center, right, p=1.0):
        '''
        Create three layer (neuro trigraph) test cases
        Parameters:
            left (int): number of vertices on the left layer
            center (int): number of vertices in the middle layer
            right (int): number of vertices on the right layer
            p (float between 0 and 1): shuffle_p
        '''
        edges1, edges2 = neur_trig_edges(left, right, center, shuffle_p=p)
        ans = min_cover_trigraph(edges1, edges2)
        g = graph_converter(edges1, edges2)
        paths = min_path_cover(g)
        check_path_cover(g, paths)
        assert len(paths) == len(ans), "Number of paths incorrect. Correct number of paths is " + str(len(ans)) + ",\
        and returned number of path is " + str(len(paths))

    for i in range(100):
        left = int(random.uniform(2, 100))
        center = int(random.uniform(2, 100))
        right = int(random.uniform(2, 100))
        p = random.random()
        neuro_trigraph_test(left, center, right, p)
    tst_stack()
