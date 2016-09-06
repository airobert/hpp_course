from Obstacle import Obstacle


class Ghost (Obstacle):
	def __init__(self):
		self.name = 'ghost'
		self.packageName = 'hpp_tutorial'
		self.urdfName = 'bigbox'


class HyQGhost (Obstacle):
	def __init__(self):
		self.name = 'hyq_ghost'
		self.packageName = 'hpp-rbprm-corba'
		self.urdfName = 'hyq_trunk'