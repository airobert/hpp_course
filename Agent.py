import sys

# from hpp.corbaserver.robot import Robot
from hpp.corbaserver import ProblemSolver
from hpp.corbaserver import Client
from hpp.gepetto import ViewerFactory
from hpp.corbaserver.pr2 import Robot as PR2Robot
from math import cos, sin, asin, acos, atan2, pi
from time import sleep
from Ghost import Ghost


class Agent (Client):
	robot = None
	platform = None
	index = 0
	ps = None
	ghosts = []
	ghost_urdf = ''
	ghost_package = ''
	# to avoid confusion, we use start and end instead of init and goal
	start_config = [] 
	end_config = []
	current_config = []
	repeat = 0

	def __init__ (self, robot, start, end):

		Client.__init__ (self)
		self.repeat = 0
		# print 'creating an agent of type ', robotType 
		self.robot = robot
		self.start_config = start
		self.end_config = end
		self.current_config = self.start_config
		self.__plan_proposed = []



	def registerPlatform(self, platform, index):
		self.platform = platform
		self.index = index

	def printInformation(self):
		print '-------------------------------------------'
		print 'name of the robot:\t', self.robot.name
		print 'configuration size:\t', self.robot.getConfigSize()
		print 'degree of freedom:\t', self.robot.getNumberDof()
		print 'mass of the robot:\t', self.robot.getMass()
		print 'the center of mass:\t', self.robot.getCenterOfMass()
		config = self.robot.getCurrentConfig()
		nm = self.robot.getJointNames()
		print 'there are ', len(nm), 'joint names in total. They are:'
		for i in range(len(nm)):
			lower = self.robot.getJointBounds(nm[i])[0]
			upper = self.robot.getJointBounds(nm[i])[1]
			print 'joint name: ', nm[i], '\trank in configuration:', self.robot.rankInConfiguration[nm[i]],
			print '\tlower bound: {0:.3f}'.format(lower), '\tupper bound: {0:.3f}'.format(upper) 

	def startDefaultSolver(self):
		name = self.robot.name
		self.problem.selectProblem(str(self.index)+' '+ str(self.repeat))
		self.robot = PR2Robot(name)
		self.ps = ProblemSolver(self.robot)
		self.ps.setInitialConfig(self.start_config)
		self.ps.addGoalConfig (self.end_config)
		self.ps.selectPathPlanner ("VisibilityPrmPlanner")
		self.ps.addPathOptimizer ("RandomShortcut")

	def solve(self):
		# try catch -------------------
		print 'solved: ', self.ps.solve()
		self.repeat += 1


	def storePath(self, choice = 0, segments = 2):
		# always store the first one for now
		for p in range(int(round(segments * self.ps.pathLength(choice)))):
			self.__plan_proposed.append(self.ps.configAtParam(choice, p* 1.0 / segments))
		
		# the last configuration is the goal configuration
		if self.ps.configAtParam(choice, self.ps.pathLength(choice)) == self.end_config:
			self.__plan_proposed.append(self.end_config)
		print 'stored; plan length: ', len(self.__plan_proposed)
	
	def setEnvironment(self):
		if self.platform.env != None:
			self.ps.loadObstacleFromUrdf(self.platform.env.packageName, self.platform.env.urdfName, self.platform.env.name)

	
	def loadOtherAgents(self):
		print 'There are ', len(self.platform.agents), 'agents'
		#load ghost agents
		for a in self.platform.agents:
			if (a.index != self.index):
				# if it is not itself then load a ghost agent
				g = Ghost()
				self.ps.loadObstacleFromUrdf(g.packageName, g.urdfName, a.robot.name) # it's the robot's name!!!
				# and then place it at the initial location of the agent
				print self.robot.name, ' is now loading ', a.robot.name, ' as a ghost'
				config = a.current_config
				spec = self.getMoveSpecification(config)
				self.obstacle.moveObstacle(a.robot.name + 'base_link_0', spec)

	def setBounds(self):
		# this is hard-coded for now
		self.robot.setJointBounds("base_joint_xy", [-10,10,-4,4])

	def getConfigOfProposedPlanAtTime(self, index):
		return self.__plan_proposed[index]

	def getProposedPlanLength(self):
		return len(self.__plan_proposed)

	def getMoveSpecification(self, config):
		x = config[0]
		y = config[1]
		th = atan2(config[3], config[2]) 
		# print 'sin = ', self.init_config[3], ' cos = ', self.init_config[2], ' th = ', th
		return [x, y, 0, cos(th / 2) , 0, 0, sin(th / 2)]