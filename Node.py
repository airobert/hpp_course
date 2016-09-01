import copy

# this is a class to represent the searching tree

class Node ():
	# configs = []
	agent_remained = []
	paths = []
	children = []
	absolute_time = 0
	progress_time = 0

	def __init__(self, configs):
		self.agent_remained = range (len(configs)) # all the agents
		self.paths = map ((lambda x: [x]), configs)

	def cloneNode (self):
		node = Node ([])
		node.paths = copy.copy(self.paths)
		node.agent_remained = copy.copy(self.agent_remained)
		self.absolute_time = copy.copy(self.absolute_time)
		self.progress_time = copy.copy(self.progress_time)
		return node

	def expand (self, indexes_and_paths, reached_agents):
		# print '\n \n \n  these agents are removed!!!!!!!!!', reached_agents
		child = self.cloneNode()
		for (index, path) in indexes_and_paths:
			if child.paths[index][-1] == path[0]:
			# if True:
				child.paths[index] = child.paths[index] + path[1::]
				print '\n\n\n WE CAN continue from here\n\n\n\n' 
			else:
				print index, ' --- ',reached_agents
				print '\n\n\n\may not continue from here\n\n\n\n'
				print 'should be: ', child.paths[index][-1][0], child.paths[index][-1][1]
				print 'but is it', path[0][0], path[0][1]

		child.progress_time = len (indexes_and_paths[0]) -1
		child.absolute_time = self.absolute_time + child.progress_time
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

		print 'absolute time: ', self.absolute_time
		print 'progress_time: ', self.progress_time
		# print 'the agents remained', self.agent_remained
		# for i in range (len(self.agent_remained)):
		# 	print 'for agent ', i, ' it moved like: '
		# 	for p in self.paths[i]:
		# 		print '\t', p[0], p[1]
		print '---------------------------'

	def getAgentPlan (self, agent):
		return self.paths[agent]
