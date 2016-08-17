from Agent import Agent
from hpp.corbaserver.pr2 import Robot as PR2Robot

class PR2 (PR2Robot, Agent):
	def __init__(self, platform, agentIndex, agentName):
		print 'initialising a PR2 agent'
		Agent.__init__(self, platform, agentIndex, agentName, "pr2")

	def set_init(self, x, y):
		print 'the agent is now set to its initial configuration at (', x, ', ', y, ')'