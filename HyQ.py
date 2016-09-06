from hpp.corbaserver.rbprm.rbprmbuilder import Builder

# class HyQ (Agent):
# 	def __init__(self, platform, agentIndex, agentName):
# 		print 'initialising a HyQ agent'
# 		self.robotType = "hyq"
# 		self.packageName = "hyq_description"
# 		self.meshPackageName = "hyq_description"
# 		self.rootJointType = "planar"
# 		self.urdfName = "hyq"
# 		self.urdfSuffix = ""
# 		self.srdfSuffix = ""
# 		Agent.__init__(self, platform, agentIndex, agentName, "hyq")
# 		# self.set_init(0, 0)

# 	def setInit(self, x, y):
# 		print 'the agent is now set to its initial configuration at (', x, ', ', y, ')'
# 		self.init_config = self.getCurrentConfig()
# 		self.init_config[0] = x
# 		self.init_config[1] = y
# 		self.init_config[6] = -0.5
# 		self.init_config[9] = 0.5
# 		self.init_config[12] = -0.5
# 		self.init_config[15] = 0.5
# 		self.setCurrentConfig(self.init_config)
# 		self.platform.r(self.init_config)
# 		# error message

	# def set_config(x, y): 


class HyQTrunk(Builder):
	def __init__(self, name):
		Builder.__init__(self)
		self.rootJointType = 'freeflyer'
		self.packageName = 'hpp-rbprm-corba'
		self.meshPackageName = 'hpp-rbprm-corba'
		self.urdfName = 'hyq_trunk'
		self.urdfNameRom = ['hyq_lhleg_rom','hyq_lfleg_rom','hyq_rfleg_rom','hyq_rhleg_rom']
		self.urdfSuffix = ""
		self.srdfSuffix = ""
		self.loadModel(self.urdfName, self.urdfNameRom, self.rootJointType, self.meshPackageName, self.packageName, self.urdfSuffix, self.srdfSuffix)
		self.setFilter(['hyq_rhleg_rom', 'hyq_lfleg_rom', 'hyq_rfleg_rom','hyq_lhleg_rom'])
		self.setNormalFilter('hyq_lhleg_rom', [0,0,1], 0.9)
		self.setNormalFilter('hyq_rfleg_rom', [0,0,1], 0.9)
		self.setNormalFilter('hyq_lfleg_rom', [0,0,1], 0.9)
		self.setNormalFilter('hyq_rhleg_rom', [0,0,1], 0.9)
		self.boundSO3([-0.1,0.1,-1,1,-1,1])
		self.name = name