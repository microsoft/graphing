

class NeuralGraphVert():
    def __init__(self, key, layer, layer_ix=0):
        self.key = key
        self.layer = layer
        self.layer_ix = layer_ix


class ToyGraphs():
    @staticmethod
    def toy_graph_1():
        g = {}

        v4 = NeuralGraphVert(4, 2, 1)
        v5 = NeuralGraphVert(5, 2, 2)

        v6 = NeuralGraphVert(6, 3, 1)
        v7 = NeuralGraphVert(7, 3, 2)
        v8 = NeuralGraphVert(8, 3, 3)

        g[1] = [v4]
        g[2] = [v4, v5]
        g[3] = [v5]

        g[4] = [v6, v7]
        g[5] = [v8]

        g[6] = []
        g[7] = []
        g[8] = []

        return g

    @staticmethod
    def toy_graph_2():
        g = {}

        v2 = NeuralGraphVert(2, 2, 1)
        v3 = NeuralGraphVert(3, 2, 2)
        v4 = NeuralGraphVert(4, 2, 3)

        v5 = NeuralGraphVert(5, 3, 1)
        v6 = NeuralGraphVert(6, 3, 2)
        v7 = NeuralGraphVert(7, 3, 3)

        v8 = NeuralGraphVert(8, 4, 1)
        v9 = NeuralGraphVert(9, 4, 2)
        v10 = NeuralGraphVert(10, 4, 3)
        v11 = NeuralGraphVert(11, 4, 4)

        g[1] = [v2, v3, v4]
        g[2] = [v5]
        g[3] = [v6]
        g[4] = [v6, v7]

        g[5] = [v8]
        g[6] = [v9]
        g[7] = [v10, v11]

        return g
