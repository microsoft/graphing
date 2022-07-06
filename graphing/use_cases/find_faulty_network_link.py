import queue
from collections import defaultdict


class Graph():
    def __init__(self, edges, excl_verts={}):
        self.white_verts = set()
        self.grey_verts = set()
        self.black_verts = set()
        self.adj = defaultdict(dict)
        # We'll need the reverse graph as well.
        self.adj_rev = defaultdict(dict)
        self.vert_wts = {}
        self.edges = edges
        for ed in edges:
            vert_0 = ed[0]
            vert_1 = ed[1]
            if vert_0 not in excl_verts and vert_1 not in excl_verts:
                self.white_verts.add(vert_0)
                self.white_verts.add(vert_1)
                # Save graph as an adjacency list.
                self.adj[vert_0][vert_1] = 0
                # We need both the regular graph and reversed graph.
                self.adj_rev[vert_1][vert_0] = 0
                self.vert_wts[vert_0] = 0
                self.vert_wts[vert_1] = 0

    def bfs_probs(self, s, rev=False):
        self.vert_wts[s] = 1
        self.grey_verts.add(s)
        q = queue.Queue()
        q.put(s)
        if not rev:
            e_lst = self.adj
        else:
            e_lst = self.adj_rev
        while q.qsize() > 0:
            u = q.get()
            for v in e_lst[u]:
                if v in self.white_verts and v not in self.grey_verts\
                 and v not in self.black_verts:
                    self.grey_verts.add(v)
                    q.put(v)
                e_lst[u][v] += self.vert_wts[u]/len(e_lst[u])
                self.vert_wts[v] += self.vert_wts[u]/len(e_lst[u])
            self.vert_wts[u] = 0
            self.black_verts.add(u)


def reachable_subgraph(edges, source='s1', dest='d1'):
    g3 = Graph(edges)
    # We don't care about the probabilities, just about BFS visits
    g3.bfs_probs(source)
    g4 = Graph(edges)
    # We don't care about the probabilities, just about BFS visits
    g4.bfs_probs(dest, rev=True)
    excl_verts = g3.vert_wts.keys() - \
        g4.black_verts.intersection(g3.black_verts)
    g5 = Graph(edges, excl_verts)
    return g5


def tst():
    # This kind of graph is not split neatly into layers.
    # So, one iteration of bfs is not enough.
    edges = [['s', 'a'],
             ['a', 'c'],
             ['s', 'e'],
             ['s', 'b'],
             ['b', 'd'],
             ['e', 'd'],
             ['c', 'd'],
             ['a', 'e']]
    g1 = Graph(edges)
    g1.bfs_probs('s')
    # This kind of graph is split neatly into layers
    # like a networking topology graph would. So,
    # one iteration of the bfs is enough.
    edges = [['s1', 'a'],
             ['s1', 'd'],
             ['a', 'b'],
             ['d', 'b'],
             ['b', 'c'],
             ['d', 'e'],
             ['e', 'c'],
             ['c', 'd1']]
    g2 = Graph(edges)
    g2.bfs_probs('s1')
    print("Here is the graph with probabilities of the error populated.")
    print(g2.adj)
    # Now, how to get rid of edges irrelevant to the network topology.
    edges = [['s1', 'a'],
             ['s1', 'd'],
             ['a', 'b'],
             ['d', 'b'],
             ['b', 'c'],
             ['d', 'e'],
             ['e', 'c'],
             ['c', 'd1'],
             ['s2', 'd'],
             ['d', 'e'],
             ['e', 'c'],
             ['e', 'f'],
             ['f', 'd2'],
             ['s3', 'g'],
             ['g', 'e'],
             ['e', 'f'],
             ['f', 'd2']]
    g3 = reachable_subgraph(edges, 's1', 'd1')
    g3.bfs_probs('s1')
