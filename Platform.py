# gepetto-viewer-server
# hppcorbaserver
# -DCMAKE_INSTALL_PREFIX=/home/airobert/HPP/install

from HyQ import HyQ
from Agent import PR2
from Environment import BasicHouse
from Obstacle import Obstacle
from hpp.corbaserver import ProblemSolver
from hpp.gepetto import ViewerFactory
from hpp.gepetto import PathPlayer

class Platform ():
	main_agent = None
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
	# pp = PathPlayer (rbprmBuilder.client.basic,ls r)
	def __init__(self, mainAgentType):
		print 'creating a platform with an agent of type: ', mainAgentType
		if (mainAgentType == "hyq" or mainAgentType == "HyQ" or mainAgentType == "HYQ"):
			self.main_agent = HyQ(self, 1, "main")
		elif (mainAgentType == "pr2" or mainAgentType == "PR2"):
			self.main_agent = PR2(self, 1, "main")
		else:
			print 'this type of agent can not be defined yet'
		self.ps = ProblemSolver (self.main_agent)
		self.vf = ViewerFactory (self.ps)
		self.r = self.vf.createViewer()
		self.r(self.main_agent.getCurrentConfig ())
		self.agents.append (self.main_agent)
		
	def refreshDisplay(self):
		self.r = self.vf.createViewer()
		self.r.computeObjectPosition()

		#and finally, set the environment
	def setEnvironment(self, env):
		self.vf.loadObstacleModel(env.packageName, env.urdfName, env.name)
		self.env = env
		self.refreshDisplay()

	# this method looks useless so far.....
	def activatePlatform(self):
		self.main_agent.client.problem.selectProblem('0')
		for i in self.agents:
			i.refrechAgent()

	def loadAgentView (self, index):
		self.vf = ViewerFactory (self.agents[index -1].ps)
		self.refreshDisplay()
		self.r(self.agents[index - 1].init_config)

	def playAgentPath(self, cl):
		self.pp = PathPlayer (cl, self.r)
		self.pp(0)

	def addAgent(self, agt):
		self.agents.append(agt)