from Obstacle import Obstacle

class Environment(Obstacle):

	def __init__(self, name, packageName, urdfName, baseJointName):
		Obstacle.__init__ (self, name, packageName, urdfName, baseJointName)

#this is too complicated!!!
class Kitchen(Environment):

	def __init__(self, name):
		# vf.loadObstacleModel ("iai_maps", "kitchen_area", "kitchen")
		self.name = name
		self.packageName = "iai_maps"
		self.urdfName = "kitchen_area"
		Environment.__init__(self, self.name, self.packageName, self.urdfName, "kitchen_base_joint")

#a basic environment
class BasicHouse(Environment):
	def __init__(self, name):
		# vf.loadObstacleModel ("iai_maps", "kitchen_area", "kitchen")
		self.name = name
		self.packageName = "hpp-rbprm-corba"
		self.urdfName = "basic"
		Environment.__init__(self, self.name, self.packageName, self.urdfName, "basic")