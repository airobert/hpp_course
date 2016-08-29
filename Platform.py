# gepetto-viewer-server
# not hpp-manipulation-server
# hppcorbaserver
# -DCMAKE_INSTALL_PREFIX=/home/airobert/HPP/install

from Environment import BasicHouse
from Obstacle import Obstacle
from hpp.corbaserver import ProblemSolver
# from hpp.corbaserver.manipulation import ProblemSolver as MProblemSolver, ConstraintGraph
from hpp.gepetto import PathPlayer
from hpp.gepetto import ViewerFactory
# from hpp.gepetto.manipulation import ViewerFactory as MViewerFactory
# from hpp.corbaserver.manipulation.pr2 import Robot
# from hpp.corbaserver.manipulation import robot as METARobot
# from hpp.corbaserver.manipulation import ProblemSolver, ConstraintGraph

from time import sleep

class Platform ():
	# main_agent = None
	agents = []
	# problem solver
	ps = None
	# path player
	pp = None
	# view factory
	vf = None
	# viewer
	r = None
	env = None
	# a dictionary to get the agent's index
	index_dic = {}

	# pp = PathPlayer (rbprmBuilder.client.basic,ls r)
	def __init__(self, agents):
		self.agents = agents
		for i in range (len(agents)):
			self.index_dic[agents[i].robot.name] = i
			self.agents[i].registerPlatform(self, i)
			print 'the agent ', agents[i].robot.name, ' is now registered with the index ', self.getInidex(agents[i].robot.name) 
	
	def start(self):
		# self.problem.selectProblem(0)
		self.ps = ProblemSolver(self.agents[0].robot)
		self.vf = ViewerFactory(self.ps)
		self.vf.loadObstacleModel(self.env.packageName, self.env.urdfName, self.env.name)
		self.r = self.vf.createViewer()
		# self.pp = PathPlayer (self.agents[0], self.r)


	def loadAgentView (self, index, default = False): #default position or not
		self.ps = self.agents[index -1].ps
		self.vf = ViewerFactory (self.ps)
		# self.vf.loadObstacleModel(self.env.packageName, self.env.urdfName, self.env.name)
		self.r = self.vf.createViewer()
		# print '---------------->', len(self.agents[index - 1].init_config)
		if default:
			self.r(self.agents[index - 1].current_config)
		# self.r.computeObjectPosition()

	def getInidex(self, robot_name):
		return self.index_dic[robot_name]


	def setEnvironment(self, env):
		self.env = env
		# self.r = self.vf.createViewer()

	# def startViewer(self):
	# 	self.r = vf.createViewer()

	def updateViewAtTime(self, t):
		config = []
		for a in self.agents:
			config.append (a.getConfigOfProposedPlanAtTime(t))
		self.r(config)


	def playAllPath(self):
		max_time = 0
		for a in self.agents:
			l = a.getProposedPlanLength()
			if l > max_time:
				max_time = l
		
		for t in range(max_time):
			# print 'time is ', t
			for i in range(len(self.agents)):
				a = self.agents[i]
				if  a.getProposedPlanLength() > t:
					# print 'agent ', a.index, 
					self.loadAgentView(i+1)
					# and then set the agent to its current configuration
					self.r(a.getConfigOfProposedPlanAtTime(t))
			# sleep(0.003)

	def validateAllPath(self):
		max_time = 0
		for a in self.agents:
			a.startDefaultSolver()
			a.setBounds()
			a.setEnvironment()
			a.loadOtherAgents()

			l = a.getProposedPlanLength()
			if l > max_time:
				max_time = l

		for t in range (max_time):
			print '\n\n\nthis is time ', t
			for i in range (len(self.agents)):
				a = self.agents[i]
				a.startDefaultSolver()

				print 'this is robot ', a.robot.name
				# a1.obstacle.getObstacleNames(False, 1000)
				if a.getProposedPlanLength() > t:
					myconfig = a.getConfigOfProposedPlanAtTime(t)
					myspec = a.getMoveSpecification(myconfig)
					print 'the agent is at ', myspec[0], myspec[1]
					# first of all, move all the obstacles
					for oa in self.agents: # other agents
						if a.index != oa.index:
							# print '\t and moving the ghost of ', oa.robot.name
							if oa.getProposedPlanLength() > t:
								config = oa.getConfigOfProposedPlanAtTime(t)
							else:
								config = oa.end_config
							spec = oa.getMoveSpecification(config)
							a.obstacle.moveObstacle(oa.robot.name + 'base_link_0', spec)
							print '\tmove ghost', oa.robot.name, ' to ', spec[0], spec[1] 

					# secondly, test if the configuration is valid 
					(result, _) = a.robot.isConfigValid(a.getConfigOfProposedPlanAtTime(t))
					if not result:
						return t
		# if everything is fine at each time slot, return -1 
		return -1 



