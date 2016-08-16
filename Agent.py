import sys

from hpp.corbaserver.robot import Robot as Parent
from hpp.corbaserver import ProblemSolver
from hpp.gepetto import ViewerFactory


class Agent (Parent):
	platform = None
	index = 0
	name = ""
	robotType = ""
	packageName = ""
	meshPackageName = ""
	rootJointType = ""
	urdfName = ""
	urdfSuffix = ""
	srdfSuffix = ""
	ps = None
	# vf = None
	init_config = []
	goal_config = []
	obs = []


	def __init__ (self, platform, agentIndex, agentName, robotType, load = True):
		# print 'creating an agent of type ', robotType 
		self.platform = platform
		self.index = agentIndex
		self.name = agentName
		Parent.__init__ (self, agentName, self.rootJointType, load)
		self.ps = ProblemSolver (self)
		self.print_information()
	
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

		for i in range(len(nm)):
			lower = self.getJointBounds(nm[i])[0]
			upper = self.getJointBounds(nm[i])[1]
			print nm[i], ' & ', self.rankInConfiguration[nm[i]],
			print '& {0:.3f}'.format(lower), '& {0:.3f} & '.format(upper), '{0:.3f}\\\\ \\hline'.format(config[i]) 

		print 'by default, the root joint position is at:', self.getRootJointPosition()
		print 'the default configuration is: ', self.getCurrentConfig()
		if (self.isConfigValid(self.getCurrentConfig())[0]):
			print 'and the default configuration is valid'
		else:
			print 'but this default configuration is not valid because:'
			print self.isConfigValid(self.getCurrentConfig())[1]

	
	def activate_agent():
		self.platform.main_agent.client.problem.selectProblem(self.index)
		print 'the agent ', self.index , ' is now activated'

	def registerObstacle(obs):
		print 'load obstacle'
		self.client.obstacle.loadObstacleModel(obs.packageName, obs.urdfName, obs.name)

		# self.vf.loadObstacleModel ("hpp_tutorial", "bigbox", "bb")
		self.flatform.refresh_display()

	def moveObstacle(obs, config):
		obs.config = config
		self.client.obstacle.moveObstacle(obs.baseJointName, obs.config)
		self.flatform.refresh_display()
