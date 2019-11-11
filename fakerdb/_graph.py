import collections
import operator
import queue
from functools import reduce


class GraphTools:
	"""
	Utility for support schema graph structure (topological sorting), specifically for foreign keys
	"""

	@staticmethod
	def build_adj_list(dependencies, all_ids, add_inv=True):
		"""
		obj: build adj list from pair wise dependencies
		:param dependencies: list[list] - (A->B) dependencies list
		:param add_inv: bool - whether to include inverse as well
		:return: dict(dict()) - adjacency hash list
		"""
		# ensure all all keys form the complete graph, even if independent nodes
		# the flattened list of dependencies must exist as a subset of all the ids
		if dependencies:
			assert (set(reduce(operator.concat, dependencies)) <= set(all_ids))

		g = {id: set() for id in all_ids}
		for a, b in dependencies:
			g[a].add(b)
		if add_inv:
			g_inv = collections.defaultdict(set)
			for a, b in dependencies:
				g_inv[b].add(a)
			return g, g_inv
		else:
			return g

	@staticmethod
	def top_sort(dependencies, all_ids):
		"""
		obj: algorithm to provide topological ordering to dependencies
		:param dependencies: list[list] - (A->B) read "A depends on B"; dependencies list
		:param all_ids: list[str] - list of all table ids. this parameter was added
		because dependencies could have A->B, B->C but no identifier for D because
		it is independent and still necessary to represent the graph holistically
		:return: list[<value-type-dependencies>] - topological ordering
		"""
		# build graph and its inverse
		g, g_inv = GraphTools.build_adj_list(dependencies, all_ids)

		# find all empty dependencies
		q = queue.Queue()
		for course in g:
			if not g[course]:
				q.put(course)

		# begin topological sort algorithm
		topo_sort = []
		while not q.empty():
			# get next independent node
			front = q.get()
			topo_sort.append(front)

			# remove all associated edges
			for elm in g_inv[front]:
				g[elm].remove(front)
				# check if is empty
				if not g[elm]:
					q.put(elm)

		# make sure all elements are included
		# otherwise the graph does not have any topological ordering
		if len(topo_sort) == len(all_ids):
			return topo_sort
		else:
			raise RuntimeError('A cycle has been detected within the graph. No topological sort is possible.')
