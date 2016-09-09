# hpp-manipulation-server
# gepetto-viewer-server

from ManiHyQ import HyQ as MetaHyQ
from HyQ import HyQ 
from math import cos, sin, asin, acos, atan2, pi
from hpp.gepetto.manipulation import ViewerFactory
from hpp.corbaserver.manipulation import ProblemSolver, ConstraintGraph
from time import sleep

import sys

meta = MetaHyQ('r0')
ps = ProblemSolver (meta)
fk = ViewerFactory (ps)
meta.setJointBounds ("r0/base_joint_xy", [-30,30,-30,30])

name_of_scene = "simple_boeing"


def loadOtherRobots(amount):
	print 'there are ', amount,  ' robots'
	for i in range(amount - 1):
		fk.loadObjectModel(HyQ, 'r' + str(i + 1))
		print 'loading', 'r' + str(i + 1)
		meta.setJointBounds ('r' + str(i + 1) + "/base_joint_xy", [-30,30,-30,30])
	print 'DOF: ', len(meta.getCurrentConfig())

def importTrajectory(filename):
	index = -1
	allT = {}
	f = open(filename, 'r')
	content = f.readlines()
	configs = []
	for l in content:
		if ('agent' in l):
			if index != -1:
				allT[index] = configs
			i = l.split(' ')
			index = int(i[1])
			configs = []
		else:
			ll = l.split(',')
			configs.append(map((float), ll))
	allT[index] = configs
	return allT

def convertConfig(config):
	x = config[0]
	y = config[1]
	th = 2 * atan2(config[6], config[3])
	c = cos (th)
	s = sin (th)
	con = [x, y, c, s] + config[7::]
	return con

def displayAnimation(filename):
	# graph = ConstraintGraph (meta, 'graph')
	# graph.createNode (['free'])
	# graph.createEdge ('free', 'free', 'move_free', 1, 'free')
	allT = importTrajectory(filename)
	loadOtherRobots(len(allT.keys()))

	r = fk.createViewer ()
	r.loadObstacleModel ('hpp-rbprm-corba', name_of_scene, "contact")
	r.client.gui.setColor('contact', [1,1,1,0.5])

	max_time = -1
	for a in allT.keys():
		if len(allT[a]) > max_time:
			max_time = len(allT[a])
	print 'max time : ', max_time

	x = raw_input('press the enter key to start the animation')
	for t in range(max_time):
		c = []
		for a in allT.keys():
			if len(allT[a]) <= t:
				c = c + convertConfig(allT[a][-1])
			else:
				c = c + convertConfig(allT[a][t])
		r(c)
		sleep(0.06)



def main():
	print sys.argv[1]
	displayAnimation(sys.argv[1])

if __name__ == "__main__":
    main()






# meta.setJointBounds ("myself/base_joint_xy", [-20,20,-20,20])
# meta.setJointBounds ("x/base_joint_xy", [-20,20,-20,20])
# meta.setJointBounds ("y/base_joint_xy", [-20,20,-20,20])

# q0 = meta.getCurrentConfig ()

# q0 [0] = -1
# q0 [1] = -1
# q0 [16] = -4
# q0 [17] = 4
# q0 [32] = 7
# q0 [33] = -2
# q0 [48] = 9
# q0 [49] = 10



# fk = ViewerFactory (ps)