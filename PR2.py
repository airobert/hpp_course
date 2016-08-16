from Agent import Agent
from hpp.corbaserver.pr2 import Robot as PR2Robot

class PR2 (PR2Robot, Agent):
	def __init__(self, platform, agentIndex, agentName):
		print 'initialising a PR2 agent'
		Agent.__init__(self, platform, agentIndex, agentName, "pr2")
		# self.set_init(0, 0)

	# def set_init(self, x, y):
	# 	print 'the agent is now set to its initial configuration at (', x, ', ', y, ')'
	# 	self.init_config = self.getCurrentConfig()
	# 	self.init_config[0] = x
	# 	self.init_config[1] = y
	# 	self.init_config[6] = -0.5
	# 	self.init_config[9] = 0.5
	# 	self.init_config[12] = -0.5
	# 	self.init_config[15] = 0.5
	# 	self.setCurrentConfig(self.init_config)
	# 	self.platform.r(self.init_config)