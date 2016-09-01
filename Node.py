

# this is a class to represent the searching tree

class Node ():
	# configs = []
	agent_remained = []
	paths = []
	children = []

	def __init__(self, configs):
		self.agent_remained = range (len(configs)) # all the agents
		self.paths = map ((lambda x: [x]), configs)

	def cloneNode (self):
		node = Node ([])
		node.paths = self.paths
		node.agent_remained = self.agent_remained
		return node

	def expand (self, indexes_and_paths, reached_agents):
		print '\n \n \n  these agents are removed!!!!!!!!!', reached_agents
		child = self.cloneNode()
		for (index, path) in indexes_and_paths:
			child.paths[index] = child.paths[index] + path[1::]
		child.agent_remained = self.agent_remained
		for a in reached_agents:
			child.agent_remained.remove(a)
		return child

	def terminates(self):
		return (self.agent_remained == [])

	def getAgentCurrentConfig(self, agent):
		return self.paths[agent][-1]

	def getAgentsRemained(self):
		return self.agent_remained

	def printInformation(self):
		print 'the agents remained', self.agent_remained
		for i in range (len(self.agent_remained)):
			print 'for agent ', i, ' it moved like: '
			for p in self.paths[i]:
				print '\t', p[0], p[1]
		print '---------------------------'

	def getAgentPlan (self, agent):
		return self.paths[agent]
