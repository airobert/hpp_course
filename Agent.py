import sys

from hpp.corbaserver.robot import Robot as Parent
from hpp.corbaserver import ProblemSolver
from hpp.gepetto import ViewerFactory
from hpp.corbaserver.pr2 import Robot as PR2Robot

class Agent (Parent):
	platform = None
	index = 0
	name = ""
	robotType = ""
	packageName = ""
	meshPackageName = ""
	rootJointType = "planar"
	urdfName = ""
	urdfSuffix = ""
	srdfSuffix = ""
	ps = None
	vf = None
	start_config = []
	end_config = []
	init_config = []
	goal_config = []
	# obs = [] # a list of other agents as obstacles
	# env = None # the environment


	def __init__ (self, platform, agentIndex, agentName, robotType, load = True):
		self.repeat = 0
		# print 'creating an agent of type ', robotType 
		self.platform = platform
		self.index = agentIndex
		self.name = agentName
		Parent.__init__ (self, agentName, self.rootJointType, load)
		self.ps = ProblemSolver (self)
		self.print_information()
		self.robotType = robotType
		

	
	def print_information(self):
		print '-------------------------------------------'
		print 'type of the robot:\t', self.robotType
		print 'name of the robot:\t', self.name
		print 'configuration size:\t', self.getConfigSize()
		print 'degree of freedom:\t', self.getNumberDof()
		print 'mass of the robot:\t', self.getMass()
		print 'the center of mass:\t', self.getCenterOfMass()
		config = self.getCurrentConfig()
		nm = self.getJointNames()
		print 'there are ', len(nm), 'joint names in total. They are:'
		for i in range(len(nm)):
			lower = self.getJointBounds(nm[i])[0]
			upper = self.getJointBounds(nm[i])[1]
			print 'joint name: ', nm[i], '\trank in configuration:', self.rankInConfiguration[nm[i]],
			print '\tlower bound: {0:.3f}'.format(lower), '\tupper bound: {0:.3f}'.format(upper) 

		# for i in range(len(nm)):
		# 	lower = self.getJointBounds(nm[i])[0]
		# 	upper = self.getJointBounds(nm[i])[1]
		# 	print nm[i], ' & ', self.rankInConfiguration[nm[i]],
		# 	print '& {0:.3f}'.format(lower), '& {0:.3f} & '.format(upper), '{0:.3f}\\\\ \\hline'.format(config[i]) 

		print 'by default, the root joint position is at:', self.getRootJointPosition()
		print 'the default configuration is: ', self.getCurrentConfig()
		if (self.isConfigValid(self.getCurrentConfig())[0]):
			print 'and the default configuration is valid'
		else:
			print 'but this default configuration is not valid because:'
			print self.isConfigValid(self.getCurrentConfig())[1]

	def refrechAgent(self):
		agt = PR2(self.platform, self.index, self.name)
		self = agt
		print 'the agent ', self.index, ' is now refreshed in this problem' 

	def activateAgent(self):
		self.platform.main_agent.client.problem.selectProblem(str(self.index)+' '+ str(self.repeat))
		self.refrechAgent()
		print 'the agent ', self.index , ' is now activated'

	def registerObstacle(self, obs):
		print 'load obstacle'
		self.client.obstacle.loadObstacleModel(obs.packageName, obs.urdfName, obs.name)

		# self.vf.loadObstacleModel ("hpp_tutorial", "bigbox", "bb")
		self.flatform.refreshDisplay()


	def setEnvironment(self, env):
		self.client.obstacle.loadObstacleModel(env.packageName, env.urdfName, env.name)

	def relocateObstacle(self, obs, config):
		obs.config = config
		self.client.obstacle.moveObstacle(obs.baseJointName, obs.config)
		self.flatform.refreshDisplay()

	def setInitConfig (self, config):
		self.ps.setInitialConfig(config)
		self.init_config = config

	def setGoalConfig (self, config):
		self.ps.addGoalConfig(config)
		self.goal_config = config

	def solve(self):
		self.ps.selectPathPlanner ("VisibilityPrmPlanner")
		self.ps.addPathOptimizer ("RandomShortcut")
		print self.ps.solve()
		self.repeat += 1

	def playPath(self):
		self.platform.playAgentPath(self.client)

	def loadOtherAgents(self): # load other agents as obstacles
		for a in self.platform.agents:
			if a.index != self.index:
				self.client.obstacle.loadObstacleModel(a.packageName, a.urdfName, a.name)

class PR2 (PR2Robot, Agent):
	def __init__(self, platform, agentIndex, agentName):
		print 'initialising a PR2 agent'
		Agent.__init__(self, platform, agentIndex, agentName, "pr2")

	def set_init(self, x, y):
		print 'the agent is now set to its initial configuration at (', x, ', ', y, ')'