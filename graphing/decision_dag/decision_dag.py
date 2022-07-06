import numpy as np
from collections import defaultdict
import networkx as nx
from pyvis.network import Network
import matplotlib.pyplot as plt
import re


class DAGNode(object):
	def __init__(self, key1='a', adj_lst=[]):
		self.nxt = None
		self.nxt_ix = 0
		self.adj_lst = adj_lst

	def get_nxt(self, icm_cand):
		return 0


class RgxLstNode(DAGNode):
	def __init__(self, regx_lst, prms, key1, adj_lst=[]):
		self.regx_lst = regx_lst
		self.prms = prms
		super().__init__(key1=key1, adj_lst=adj_lst)

	def get_nxt(self, icm_cand):
		ix = 0
		self.nxt = self.adj_lst[0]
		for rgx in self.regx_lst:
			if re.match(rgx, icm_cand.signal):
				self.taus = self.prms[ix]
				self.nxt_ix = 1
				self.nxt = self.adj_lst[1]
				ix += 1
				return self.taus


class IfEsclToNode(DAGNode):
	def get_nxt(self, icm_cand):
		if icm_cand.escl_to is None:
			icm_cand.assign_to = icm_cand.component
		else:
			icm_cand.assign_to = icm_cand.escl_to


class SevSubDAGNode(DAGNode):
	def __init__(self, key1="SevNode"):
		super().__init__(key1)

	def get_nxt(self, icm_cand, taus=None):
		if taus is not None:
			tau1, tau2, tau3 = taus
		else:
			tau1, tau2, tau3 = .01,1,4
		sev = 0
		# This logic can be replaced by a 3-node decision tree.
		if icm_cand.p_val < tau1:
			if icm_cand.ctrl_nodes < tau2:
				if icm_cand.trt_nodes > tau3:
					sev = 3
				else:
					sev = 4
			else:
				sev = 4
		else:
			sev = 5
		icm_cand.sev = sev
		self.nxt_ix = sev - 3
		if self.adj_lst is not None and self.nxt_ix < len(self.adj_lst):
			self.nxt = self.adj_lst[self.nxt_ix]


class DecisionDAG():
	def __init__(self, mapper, adj, strt_key='CmpDeny'):
		self.mapper = mapper
		self.adj = adj
		self.strt_key = strt_key

	def walk_dag(self, icm_cand):
		node = self.mapper[self.strt_key]
		node.get_nxt(icm_cand)
		taus = None
		while node.nxt is not None:
			node = node.nxt
			if taus is None:
				taus = node.get_nxt(icm_cand)
			else:
				taus = node.get_nxt(icm_cand, taus)
		# By now, the relevant properties
		# of the ICM are populated.
		self.icm = icm_cand


# regex for excluding xyzf but including xxx*bc: "^(?!.*xyzf).*xxx.*bc$"
# Instead of this, just match "xyzf" via deny list ".*xyzf"
# and then xxx*bc via allow list: ".*xxx.*bc"
# Further, if you wanted to allow ".*xxx.*bc1", ".*xxx.*bc2",
# you would have to append the exclusion ^(?!.*xyzf)" in both places.
def tst_walk():
	deny_lst = [".*a1", ".*n1"]
	deny_prms = [(.01, 1, 4), (.01, 1, 4)]
	allow_lst = [".*xyz.*xxx"]
	allow_prms = [(.01, 1, 4)]
	mapper = {
				'CmpDeny': RgxLstNode(deny_lst, deny_prms, 'CmpDeny'),
				'CmpAllow': RgxLstNode(allow_lst, allow_prms, 'CmpAllow'),
				'GlblDeny': RgxLstNode(deny_lst, deny_prms, 'GlblDeny'),
				'GlblAllow': RgxLstNode(allow_lst, allow_prms, 'GlblAllow'),
				'HasEsclTo': IfEsclToNode('HasEsclTo'),
				'SevDAG1': SevSubDAGNode('SevDAG1'),
				'SevDAG2': SevSubDAGNode('SevDAG2')
			 }
	adj = defaultdict(list)
	adj['CmpDeny'] = ['CmpAllow', 'SevDAG1']
	adj['CmpAllow'] = ['GlblDeny', 'SevDAG2']
	adj['GlblDeny'] = ['GlblAllow', 'SevDAG1']
	adj['GlblAllow'] = ['SevDAG2', 'SevDAG1']
	adj['SevDAG2'] = ['HasEsclTo']
	for k in adj:
		mapper[k].adj_lst = [mapper[kk] for kk in adj[k]]
	strt_key = 'CmpDeny'
	dd = DecisionDAG(mapper, adj, strt_key)
	icm_cand = ICMCandidate()
	#return icm_cand, mapper, adj, dd
	dd.walk_dag(icm_cand)
	return dd


class ICMCandidate():
	def __init__(self,
		         signal="fault__nn",
				 component="agent",
				 escl_to=None,
				 p_val=1e-5,
				 trt_nodes=5,
				 ctrl_nodes=0):
		self.signal = signal
		self.component = component
		self.escl_to = escl_to
		self.p_val=p_val
		self.trt_nodes = trt_nodes
		self.ctrl_nodes = ctrl_nodes


def tst_plot():
	g = nx.DiGraph()
	g.add_edge('CmpDeny', 'CmpAllow')
	g.add_edge('CmpDeny', 'SevDAG1')
	g.add_edge('CmpAllow', 'GlblDeny')
	g.add_edge('CmpAllow', 'SevDAG2')
	g.add_edge('GlblDeny', 'GlblAllow')
	g.add_edge('GlblDeny', 'SevDAG1')
	g.add_edge('GlblAllow', 'SevDAG2')
	g.add_edge('GlblAllow', 'SevDAG1')
	g.add_edge('SevDAG2', 'HasEsclTo')
	nx.draw(g, with_labels=True)
	net = Network(directed=True)
	net.from_nx(g)
	net.show("ex.html")
	#plt.show()
	return g


def tst_plot1():
	g = tst_plot()
	net = Network(directed =True)
	ix_2_key = {0: 'CmpDeny', 1: 'CmpAllow', 2: 'SevDAG1',
				3: 'GlblDeny', 4: 'SevDAG2',
				5: 'GlblAllow', 6: 'HasEsclTo'}
	key_2_ix = {}
	for k in ix_2_key.keys():
		key_2_ix[ix_2_key[k]] = k
		if k == 0:
			net.add_node(k, label=ix_2_key[k], color="green", pos="34,12!")
		elif ix_2_key[k] == 'HasEsclTo' or ix_2_key[k] == 'SevDAG1':
			net.add_node(k, label=ix_2_key[k], color="red")
		else:
			net.add_node(k, label=ix_2_key[k])
	for e in g.edges:
		net.add_edge(key_2_ix[e[0]],key_2_ix[e[1]], label="0")
	net.show('ex.html')

