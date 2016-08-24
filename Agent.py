import sys

from hpp.corbaserver.robot import Robot as Parent
from hpp.corbaserver import ProblemSolver
from hpp.gepetto import ViewerFactory
from hpp.corbaserver.pr2 import Robot as PR2Robot
import copy 
from math import cos, sin, asin, acos, atan2, pi

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
	jointBounds = {}

	plan_proposed = []
	# obs = [] # a list of other agents as obstacles
	# env = None # the environment


	def __init__ (self, platform, index, name, robotType, load = True):
		self.repeat = 0
		# print 'creating an agent of type ', robotType 
		self.platform = platform
		self.index = index
		self.name = name
		Parent.__init__ (self, name, self.rootJointType, load)
		self.ps = ProblemSolver (self)
		self.print_information()
		self.robotType = robotType
		

	def setBounds(self, name, spec):
		self.jointBounds[name] = spec
		self.setJointBounds(name, spec)

	def refreshAgent(self):
		agt = None
		if (self.robotType == 'pr2'):
			print 'create it again'
			agt = PR2(self.platform, self.index, self.name)
		# agt = Agent(self.platform, self.index, self.name, self.robotType)
		
		# agt.setEnvironment(self.platform.env)

		for k in self.jointBounds.keys():
			self.setBounds(k, self.jointBounds[k])
		# agt.registerObstacle(self.)
		print 'the agent ', self.index, ' is now recreated in this problem' 
		agt.ps = ProblemSolver(agt)
		agt.setEnvironment(self.platform.env)
		agt.loadOtherAgents()
		self = agt
		self.print_information()

	def activateAgent(self):
		self.platform.main_agent.client.problem.selectProblem(str(self.index)+' '+ str(self.repeat))
		self.refreshAgent()
		print 'the agent ', self.index , ' is now activated'
	
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


	def registerObstacle(self, obs):
		print 'load obstacle'
		self.client.obstacle.loadObstacleModel(obs.packageName, obs.urdfName, obs.name)

		# self.vf.loadObstacleModel ("hpp_tutorial", "bigbox", "bb")
		# self.flatform.refreshDisplay()


	def setEnvironment(self, env):
		self.client.obstacle.loadObstacleModel(env.packageName, env.urdfName, env.name)

	# def relocateObstacle(self, obs, config):
	# 	obs.config = config
	# 	self.client.obstacle.moveObstacle(obs.baseJointName, obs.config)
	# 	self.flatform.refreshDisplay()

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

	def playProposePath(self):
		self.platform.payProposePath()

	def storePath(self, choice = 0):
		# always store the first one for now
		for p in range(int(round(10 * self.ps.pathLength(choice)))):
			self.plan_proposed.append(self.ps.configAtParam(choice, p* 1.0 / 10))
		if self.ps.configAtParam(choice, self.ps.pathLength(choice)) == self.goal_config:
			self.plan_proposed.append(self.goal_config) 

	def loadOtherAgents(self): # load other agents as obstacles
		print 'load ', len(self.platform.agents) - 1, 'other agents'
		for a in self.platform.agents:
			if a.index != self.index:
				self.client.obstacle.loadObstacleModel(a.packageName, a.urdfName, a.name)
				# self.ps.loadObstacleFromUrdf(a.packageName, a.urdfName, a.name)
				# self.client.obstacle.moveObstacle()
				pst = a.getRootJointPosition3D()
				self.setRootJointPosition(pst)
				# names = self.getAllJointNames()
				names = a.client.obstacle.getObstacleNames(False, 10000)
				for n in names:
					if (n[0:len(a.name)] == a.name):
					# p = self.getJointPosition(n)
					# if (a.name + n) in a.jointNames:
						self.client.obstacle.moveObstacle(n, pst)
						print 'move', n
				# pstReverse = a.getRootJointPosition3DReverse()
				self.setRootJointPosition([0,0,0,1,0,0,0]) # set it back
				# print '-------------------another agent----------------------------'
				# # print a.client.obstacle.getObstacleNames(False, 10000)
				# print a.jointNames
				# print '==================== this agent ==========================='
				# print names



	def getRootJointPosition3D(self):
		x = self.init_config[0]
		y = self.init_config[1]
		th = atan2(self.init_config[3], self.init_config[2]) 
		# print 'sin = ', self.init_config[3], ' cos = ', self.init_config[2], ' th = ', th
		return [x, y, 0, cos(th / 2) , 0, 0, sin(th / 2)]

	def getRootJointPosition3DReverse(self):
		x = self.init_config[0]
		y = self.init_config[1]
		th = pi/2 + atan2(self.init_config[3], self.init_config[2]) 
		# print 'sin = ', self.init_config[3], ' cos = ', self.init_config[2], ' th = ', th
		return [x * -1, y * -1, 0, cos(th / 2) , 0, 0, sin(th / 2)]


class PR2 (PR2Robot, Agent):
	def __init__(self, platform, agentIndex, agentName):
		print 'initialising a PR2 agent'
		Agent.__init__(self, platform, agentIndex, agentName, "pr2")

	# def set_init(self, x, y):
	# 	print 'the agent is now set to its initial configuration at (', x, ', ', y, ')'