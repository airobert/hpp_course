

# this is a class to represent the searching tree

class Node ():
	configs = []
	children = []

	paths = []

	def __init__(self, configs):
		self.configs = configs

	def expand (self, configs):
		child = Node (configs)
		self.children.append(child)
		return child

	def terminates(self, end_node):
		if self.configs == end_node.configs:
			return true
		else:
			return false

	def recordPath(self, paths):
		self.paths = paths