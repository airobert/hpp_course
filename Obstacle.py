

class Obstacle(object):
	name = ""
	packageName = ""
	urdfName = ""
	baseJointName = ""
	config  = []

	def __init__(self, name, packageName, urdfName, baseJointName):
		print 'create an obstacle/environment'
		self.name = name
		self.packageName = packageName
		self.urdfName = urdfName
		self.baseJointName = baseJointName

	def set_config(self, config):
		self.config = config

