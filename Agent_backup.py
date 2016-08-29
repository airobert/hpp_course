import sys

from hpp.corbaserver.robot import Robot
from hpp.corbaserver import ProblemSolver
from hpp.corbaserver import Client
from hpp.gepetto import ViewerFactory
from hpp.corbaserver.pr2 import Robot as PR2Robot
import copy 
from math import cos, sin, asin, acos, atan2, pi
from time import sleep

class Agent (Client):
	robot = None
	platform = None
	index = 0
	name = ""
	# packageName = ""
	# meshPackageName = ""
	# rootJointType = "planar"
	# urdfName = ""
	# urdfSuffix = ""
	# srdfSuffix = ""
	ps = None
	# vf = None
	start_config = []
	end_config = []
	current_config = []
	init_config = []
	goal_config = []
	jointBounds = {}
	proposed_plan_length = 0

	
	# obs = [] # a list of other agents as obstacles
	# env = None # the environment


	def __init__ (self, platform, index, name, robot, load = True):
		self.repeat = 0
		# print 'creating an agent of type ', robotType 
		self.platform = platform
		self.index = index
		self.name = name
		Parent.__init__ (self, name, self.rootJointType, load)
		self.ps = ProblemSolver (self)
		self.print_information()
		self.robotType = robotType
		self.__plan_proposed = []
		

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
		# agt.platform.agents[self.index-1] = agt
		for k in self.jointBounds.keys():
			self.setBounds(k, self.jointBounds[k])
		# agt.registerObstacle(self.)
		print 'the agent ', self.index, ' is now recreated in this problem' 
		agt.client.obstacle.getObstacleNames(True, 10000)
		agt.ps = ProblemSolver(agt)
		agt.setEnvironment(self.platform.env)
		agt.loadOtherAgents()
		agt.init_config = self.init_config
		agt.goal_config = self.goal_config
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

		# ------------------- for latex use only ------------------------------------------------
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

	def solve(self, choice = 0):
		self.ps.selectPathPlanner ("VisibilityPrmPlanner")
		self.ps.addPathOptimizer ("RandomShortcut")
		print self.ps.solve()
		self.repeat += 1

	def playPath(self):
		self.platform.playAgentPath(self.client)

	def playProposedPath(self):
		self.platform.playProposedPath(self.index)

	def storePath(self, choice = 0):
		# always store the first one for now
		for p in range(int(round(10 * self.ps.pathLength(choice)))):
			print 'this is agent: ', self.index
			self.platform.agents[self.index - 1].__plan_proposed.append(self.ps.configAtParam(choice, p* 1.0 / 10))
			# self.platform.r(self.__plan_proposed[-1])
			# sleep(0.02)
			for a in self.platform.agents:
				print 'agt', a.index, ': ', len(a.__plan_proposed)

		if self.ps.configAtParam(choice, self.ps.pathLength(choice)) == self.goal_config:
			self.__plan_proposed.append(self.goal_config) 
		print 'plan length: ', len(self.__plan_proposed)
		self.proposed_plan_length = len(self.__plan_proposed)

	# def proposed_plan_length(self):
		# return len(self.__plan_proposed)

	def configOfProposedPlanAtTime(self, index):
		return self.__plan_proposed[index]

	def loadOtherAgents(self): # load other agents as obstacles
		print 'load ', len(self.platform.agents) - 1, 'other agents'
		for a in self.platform.agents:
			if a.index != self.index:
				self.client.obstacle.loadObstacleModel(a.packageName, a.urdfName, a.name)
				# self.platform.vf.loadObstacleModel(a.packageName, a.urdfName, a.name)
				# self.ps.loadObstacleFromUrdf(a.packageName, a.urdfName, a.name)
				# self.client.obstacle.moveObstacle()
				# *************************
				# this two lines are wrong. becasue of this would only change the location of the robot. 
				# introducing ghost robots
				pst = a.getRootJointPosition3D()
				self.setRootJointPosition(pst)
				# *************************************
				# names = self.getAllJointNames()
				names = a.client.obstacle.getObstacleNames(False, 10000)
				for n in names:
					if (n[0:len(a.name)] == a.name):
					# p = self.getJointPosition(n)
					# if (a.name + n) in a.jointNames:
						self.client.obstacle.moveObstacle(n, pst)
						print 'move', n
				# pstReverse = a.getRootJointPosition3DReverse()
				self.setRootJointPosition(a.default_config) # set it back
				# print '-------------------another agent----------------------------'
				# # print a.client.obstacle.getObstacleNames(False, 10000)
				# print a.jointNames
				# print '==================== this agent ==========================='
	# 			# print names


	def checkAlongPath(self):
		# self.refreshAgent()
		self.platform.loadAgentView(self.index)

		for t in range(self.proposed_plan_length):
			self.platform.r(self.configOfProposedPlanAtTime(t))
			# print 'there are ', len(self.platform.agents), ' agents'
			for i in range(len(self.platform.agents)):

				a = self.platform.agents[i]
				# print '===== this agent has index: ', a.index, '========= I am agent', self.index
				if a.index != self.index: 
					if  a.proposed_plan_length > t:
						# move the other robot to it's expected location
						pst  = a.getRootJointPosition3DVectorAtTime(t)
						names = self.client.obstacle.getObstacleNames(True, 10000)
						# print names
						for n in names:
							# print a.name, '|-------->', n[0:len(a.name)] 
							if (n[0:len(a.name)] == a.name):
							# p = self.getJointPosition(n)
							# if (a.name + n) in a.jointNames:
								self.client.obstacle.moveObstacle(n, pst)
								print 'agent ', i, ' is at ', '(', self.getCurrentConfig()[0], ' ', self.getCurrentConfig()[1], ')'   
								print 'move', n, 'to ', pst[0], ', ', pst[1]
						# and then set the agent to its current configuration
			# self.platform.refreshDisplay()
			# check --------------------------------
			self.setRootJointPosition(self.getRootJointPosition3DVectorAtTime(t))
			if not self.isConfigValid(self.getCurrentConfig()):
				return t

			# name = input("go on next?")
			if not self.isConfigValid(self.configOfProposedPlanAtTime(t)):
				return t
			# ---------------------------------------
			# after checking, we must also move it back !!!!!!!! no need to move back!
			# getRootJointPosition3DVectorAtTimeReverse(self, t)
			# for i in range(len(self.platform.agents)):
			# 	a = self.platform.agents[i]
			# 	if a.index != self.index:
			# 		if  a.proposed_plan_length > t:
			# 			# move the other robot to it's expected location
			# 			pst  = a.getRootJointPosition3DVectorAtTimeReverse(t)
			# 			names = a.client.obstacle.getObstacleNames(False, 10000)
			# 			for n in names:
			# 				if (n[0:len(a.name)] == a.name):
			# 				# p = self.getJointPosition(n)
			# 				# if (a.name + n) in a.jointNames:
			# 					self.client.obstacle.moveObstacle(n, pst)
			# 					print 'for agent ', i, 'move back', n, 'back towards ', pst[0], ', ', pst[1]
			self.setRootJointPosition(self.default_config)
		return -1

	def getMoveVectorFromConfig(self, config):
		x = config[0]
		y = config[1]
		th = atan2(config[3], config[2]) 
		# print 'sin = ', self.init_config[3], ' cos = ', self.init_config[2], ' th = ', th
		return [x, y, 0, cos(th / 2) , 0, 0, sin(th / 2)]

	def getMoveVectorFromConfigReverse(self, config):
		x = self.init_config[0]
		y = self.init_config[1]
		th = pi/2 + atan2(self.init_config[3], self.init_config[2]) 
		# print 'sin = ', self.init_config[3], ' cos = ', self.init_config[2], ' th = ', th
		return [x * -1, y * -1, 0, cos(th / 2) , 0, 0, sin(th / 2)]


	def getRootJointPosition3DVectorAtTime(self, t):
		config = self.configOfProposedPlanAtTime(t)
		return self.getMoveVectorFromConfig(config)
		# x = config[0]
		# y = config[1]
		# th = atan2(config[3], config[2]) 
		# print 'sin = ', self.init_config[3], ' cos = ', self.init_config[2], ' th = ', th
		# return [x, y, 0, cos(th / 2) , 0, 0, sin(th / 2)]

	def getRootJointPosition3DVectorAtTimeReverse(self, t):
		config = self.configOfProposedPlanAtTime(t)
		return self.getMoveVectorFromConfigReverse(config)
		# x = config[0]
		# y = config[1]
		# th = pi/2 + atan2(self.init_config[3], self.init_config[2]) 
		# print 'sin = ', self.init_config[3], ' cos = ', self.init_config[2], ' th = ', th
		# return [x * -1, y * -1, 0, cos(th / 2) , 0, 0, sin(th / 2)]


	def getRootJointPosition3D(self): # at time 0
		return self.getMoveVectorFromConfig(self.init_config)
		# x = self.init_config[0]
		# y = self.init_config[1]
		# th = atan2(self.init_config[3], self.init_config[2]) 
		# # print 'sin = ', self.init_config[3], ' cos = ', self.init_config[2], ' th = ', th
		# return [x, y, 0, cos(th / 2) , 0, 0, sin(th / 2)]

	def getRootJointPosition3DReverse(self):
		return self.getMoveVectorFromConfigReverse(self.init_config)
		# x = self.init_config[0]
		# y = self.init_config[1]
		# th = pi/2 + atan2(self.init_config[3], self.init_config[2]) 
		# # print 'sin = ', self.init_config[3], ' cos = ', self.init_config[2], ' th = ', th
		# return [x * -1, y * -1, 0, cos(th / 2) , 0, 0, sin(th / 2)]


class PR2 (PR2Robot, Agent):
	default_config = [0,0,0,1,0,0,0]
	def __init__(self, platform, agentIndex, agentName):
		print 'initialising a PR2 agent'
		Agent.__init__(self, platform, agentIndex, agentName, "pr2")

	# def set_init(self, x, y):
	# 	print 'the agent is now set to its initial configuration at (', x, ', ', y, ')'