import sys

# from hpp.corbaserver.robot import Robot
from hpp.corbaserver import ProblemSolver
from hpp.corbaserver import Client
from hpp import Error
from hpp.gepetto import ViewerFactory
# from hpp.corbaserver.pr2 import Robot as PR2Robot
from math import cos, sin, asin, acos, atan2, pi
from time import sleep
from Ghost import Ghost
import copy
from  threading import Timer
from HyQ import HyQ

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
	permitted_plan = []

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
		self.repeat += 1
		name = self.robot.name
		self.problem.selectProblem(str(self.index)+' '+ str(self.repeat))
		self.robot = HyQ(name)
		self.ps = ProblemSolver(self.robot)
		self.ps.setInitialConfig(self.start_config)
		self.ps.addGoalConfig (self.end_config)
		self.ps.selectPathPlanner ("VisibilityPrmPlanner")
		self.ps.addPathOptimizer ("RandomShortcut")

	def startNodeSolver(self, node):
		self.repeat += 1
		name = self.robot.name
		self.problem.selectProblem(str(self.index)+' '+ str(self.repeat))
		self.robot = HyQ(name)
		self.ps = ProblemSolver(self.robot)
		cfg = node.getAgentCurrentConfig(self.index)
		print 'this iteration, the agent', name, 'starts from ', cfg[0], cfg[1]
		self.ps.setInitialConfig(cfg)
		self.ps.addGoalConfig (self.end_config)
		self.ps.selectPathPlanner ("VisibilityPrmPlanner")
		self.ps.addPathOptimizer ("RandomShortcut")

	def terminate_solving(self):
		self.problem.interruptPathPlanning ()

	def solve(self):
		# try catch -------------------
		try: 
			t = Timer (30.0, self.terminate_solving)
			t.start()
			print 'solved: ', self.ps.solve()
			t.cancel()
		except Error as e:
			print e.msg
			print '***************\nfailed to plan within limited time\n**************'
			return -1

		# self.repeat += 1


	def storePath(self, choice = 0, segments = 8):
		# always store the first one for now
		self.__plan_proposed = []
		for p in range(int(round(segments * self.ps.pathLength(choice)))):
			self.__plan_proposed.append(self.ps.configAtParam(choice, p* 1.0 / segments))
		
		# the last configuration is the goal configuration
		if self.ps.configAtParam(choice, self.ps.pathLength(choice)) == self.end_config:
			self.__plan_proposed.append(self.end_config)
		print 'stored; plan length: ', len(self.__plan_proposed)

	# def playProposed
	
	def setEnvironment(self):
		if self.platform.env != None:
			self.ps.loadObstacleFromUrdf(self.platform.env.packageName, self.platform.env.urdfName, self.platform.env.name)
			# self.ps.moveObstacle('airbase_link_0', [0,0, -3, 1,0,0,0])
	
	def loadOtherAgents(self):
		# print 'There are ', len(self.platform.agents), 'agents'
		#load ghost agents
		for a in self.platform.agents:
			if (a.index != self.index):
				# if it is not itself then load a ghost agent
				g = Ghost()
				self.ps.loadObstacleFromUrdf(g.packageName, g.urdfName, a.robot.name) # it's the robot's name!!!
				# and then place it at the initial location of the agent
				# print self.robot.name, ' is now loading ', a.robot.name, ' as a ghost'
				config = a.current_config
				spec = self.getMoveSpecification(config)
				spec [2] = 0.3 
				self.obstacle.moveObstacle(a.robot.name + 'base_link_0', spec)
	
	def loadOtherAgentsFromNode(self, node):
		print 'There are ', len(self.platform.agents), 'agents'
		#load ghost agents
		for a in self.platform.agents:
			if (a.index != self.index):
				# if it is not itself then load a ghost agent
				g = Ghost()
				self.ps.loadObstacleFromUrdf(g.packageName, g.urdfName, a.robot.name) # it's the robot's name!!!
				# and then place it at the initial location of the agent
				config = node.getAgentCurrentConfig(a.index)
				spec = self.getMoveSpecification(config)
				self.obstacle.moveObstacle(a.robot.name + 'base_link_0', spec)
				print self.robot.name, ' is now loading ', a.robot.name, ' as a ghost', 'it is at ', spec [0], spec [1]

	def setBounds(self):
		self.robot.setJointBounds ("base_joint_xy", [-35,10, -2.6, 4.3])

		# if self.platform.env != None:
		# 	if ('Environment.Kitchen' in str(type(self.platform.env))):
		# 		self.robot.setJointBounds("base_joint_xy", [-5,0,-10,2])
		# 	else:
		# 		self.robot.setJointBounds("base_joint_xy", [-10,10,-4,4])
		# else:
		# 	self.robot.setJointBounds("base_joint_xy", [-10,10,-10,10])
		# # this is hard-coded for now
		# if (env == 'house')
		# else:

	def getConfigOfProposedPlanAtTime(self, index):
		return self.__plan_proposed[index]

	def getConfigOfPermittedPlanAtTime(self, index):
		return self.permitted_plan[index]

	def getProposedPlanLength(self):
		return len(self.__plan_proposed)

	def setPermittedPlan(self, plan):
		self.permitted_plan = plan

	def getPermittedPlanLength(self):
		return len(self.permitted_plan)

	def exportPermittedPlan(self, filename):
		f = open(filename, 'a+')
		f.write('agent ' + str(self.index) + '\n')
		for p in self.permitted_plan:
			f.write(str(p)[1:-1] + '\n')
		f.close()



	def obtainPermittedPlan(self):
		return copy.copy(self.permitted_plan)

		# we will get only a copy of it, not the original one 
		# to remind the difference, we use 'obtain' instead of 'get'
	def obtainProposedPlan(self):
		return copy.copy(self.__plan_proposed)

	def getMoveSpecification(self, config):
		x = config[0]
		y = config[1]
		th = atan2(config[3], config[2]) 
		# print 'sin = ', self.init_config[3], ' cos = ', self.init_config[2], ' th = ', th
		return [x, y, 0, cos(th / 2) , 0, 0, sin(th / 2)]

	def computePlan(self, node):
		self.startNodeSolver(node)
		self.setBounds()
		self.setEnvironment()
		self.loadOtherAgentsFromNode(node)
		if self.solve() != -1:
			self.storePath()
		else:
			self.__plan_proposed = self.__plan_proposed[node.progress_time::]
			[node.getAgentCurrentConfig(self.index)]
			print 'take the previous one and continue the searching'
			return -1


		


