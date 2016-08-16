from Agent import Agent

class HyQ (Agent):
	def __init__(self, platform, agentIndex, agentName):
		print 'initialising a HyQ agent'
		self.robotType = "hyq"
		self.packageName = "hyq_description"
		self.meshPackageName = "hyq_description"
		self.rootJointType = "planar"
		self.urdfName = "hyq"
		self.urdfSuffix = ""
		self.srdfSuffix = ""
		Agent.__init__(self, platform, agentIndex, agentName, "hyq")
		# self.set_init(0, 0)

	def set_init(self, x, y):
		print 'the agent is now set to its initial configuration at (', x, ', ', y, ')'
		self.init_config = self.getCurrentConfig()
		self.init_config[0] = x
		self.init_config[1] = y
		self.init_config[6] = -0.5
		self.init_config[9] = 0.5
		self.init_config[12] = -0.5
		self.init_config[15] = 0.5
		self.setCurrentConfig(self.init_config)
		self.platform.r(self.init_config)
		# error message

	# def set_config(x, y): 


