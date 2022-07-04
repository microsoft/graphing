import numpy as np
import graphing.special_graphs.neural_trigraph.toy_graphs as tg
from copy import deepcopy


class FlowGraph1(object):
	"""
	The purpose of this class is to convert
	a flow dictionary to a list of paths.
	"""
	def __init__(self, g):
		"""
		Initialize a flow graph dictionary so we
		can convert to a list of paths.
		args:
			g: A flow dictionary.
		"""
		self.g = g
		self.dest = max(list(g.keys()))+1
		self.paths = []

	def dfs(self, u):
		if u == self.dest:
			self.paths.append(self.path)
			self.path = []
			return
		self.path.append(u)
		# This is typically where the loop comes in
		# for traditional DFS.
		v = next(iter(self.g[u]))
		self.g[u][v] -= 1
		self.dfs(v)
		# Now remove redundant keys.
		if self.g[u][v] == 0:
			del self.g[u][v]

	def dfs_init(self):
		while len(self.g[0].keys()) > 0:
			for v in self.g[0].keys():
				self.path = []
				self.g[0][v] -= 1
				self.dfs(v)
			# Need to store a seperate array for keys
			# since dictionary can't be modified while
			# iterating on it.
			keyss = list(self.g[0].keys())
			for v in keyss:
				if self.g[0][v] == 0:
					del self.g[0][v]


def tst(gr_no=1):
	if gr_no == 1:
		g = deepcopy(tg.ToyGraph1.res)
	else:
		g = deepcopy(tg.ToyGraph2.res)
	fg = FlowGraph1(g)
	fg.dfs_init()
	return fg
