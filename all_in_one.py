


from hpp.corbaserver.rbprm.rbprmbuilder import Builder
from hpp.corbaserver.rbprm.rbprmfullbody import FullBody
from hpp.corbaserver.rbprm.problem_solver import ProblemSolver
from hpp.gepetto import Viewer
from time import sleep
import numpy as np
import sys


# gepetto-viewer-server 
# not hppcorbaserver 
# but hpp-rbprm-server

# rootJointType = 'freeflyer'
# packageName = 'hpp-rbprm-corba'
# meshPackageName = 'hpp-rbprm-corba'
# urdfName = 'hyq_trunk'
# urdfNameRom = ['hyq_lhleg_rom','hyq_lfleg_rom','hyq_rfleg_rom','hyq_rhleg_rom']
# urdfNameroms = ['hyq_lhleg_rom','hyq_lfleg_rom','hyq_rfleg_rom','hyq_rhleg_rom']
# urdfSuffix = ""
# srdfSuffix = ""
# # name_of_scene = "groundcrouch"
# name_of_scene = "simple_boeing"

# #------------------------------------------
# rbprmBuilder = Builder ()

# rbprmBuilder.loadModel(urdfName, urdfNameRom, rootJointType, meshPackageName, packageName, urdfSuffix, srdfSuffix)
# # rbprmBuilder.setJointBounds ("base_joint_xyz", [-6,5, -4, 4, 0.6, 2])
# rbprmBuilder.setFilter(['hyq_rhleg_rom', 'hyq_lfleg_rom', 'hyq_rfleg_rom','hyq_lhleg_rom'])
# rbprmBuilder.setNormalFilter('hyq_lhleg_rom', [0,0,1], 0.9)
# rbprmBuilder.setNormalFilter('hyq_rfleg_rom', [0,0,1], 0.9)
# rbprmBuilder.setNormalFilter('hyq_lfleg_rom', [0,0,1], 0.9)
# rbprmBuilder.setNormalFilter('hyq_rhleg_rom', [0,0,1], 0.9)
# rbprmBuilder.boundSO3([-0.1,0.1,-1,1,-1,1])

# # ~ from hpp.corbaserver.rbprm. import ProblemSolver


# ps = ProblemSolver( rbprmBuilder )

# r = Viewer (ps)

# rbprmBuilder.setJointBounds ("base_joint_xyz", [-35,10, -4, 4, -1, 1])
# #q_init = [0, 4, 0.65, 0.7071,0,0,0.7071];
# #q_goal = [0, -27, 0.65, 0.7071,0,0,0.7071];
# q_init = [4, 0, 0.65, 1,0,0,0];
# q_goal = [-27, 0, 0.65, 1,0,0,0];
# # rbprmBuilder.setCurrentConfig (q_init); r (q_init)

# # q_init = rbprmBuilder.getCurrentConfig ();
# # q_init = [-6,-3,0.8,1,0,0,0]; 

# # q_goal = [4, 4, 0.8, 1, 0, 0, 0]; r (q_goal)

# ps.addPathOptimizer("RandomShortcut")
# ps.setInitialConfig (q_init)
# ps.addGoalConfig (q_goal)


# r.loadObstacleModel (packageName, name_of_scene, "planning")
# r.loadObstacleModel (packageName, 'hyq_trunk', "hyq_ghost")
# # r.loadObstacleModel (packageName, "box", "box")


# # r.client.gui.setColor('planning', [1,1,1,0.3])
# ps.client.problem.selectConFigurationShooter("RbprmShooter")
# ps.client.problem.selectPathValidation("RbprmPathValidation",0.05)
# r(q_init)
# t = ps.solve () ; #what if I don't have this?
# # if isinstance(t, list):
# # 	t = t[0]* 3600000 + t[1] * 60000 + t[2] * 1000 + t[3]
# # ****************************************************************************



packageName = "hyq_description"
meshPackageName = "hyq_description"
rootJointType = 'freeflyer'
urdfName = "hyq"
urdfSuffix = ""
srdfSuffix = ""
rootName = 'base_joint_xyz'
name_of_scene = "simple_boeing"

fullBody = FullBody () 
fullBody.loadFullBodyModel(urdfName, rootJointType, meshPackageName, packageName, urdfSuffix, srdfSuffix)

#  Setting a number of sample configurations used
nbSamples = 10000

# RW: update the problem solver and viewer
# ps = ProblemSolver(fullBody)
# r = Viewer (ps)




#  Creating limbs
# cType is "_3_DOF": positional constraint, but no rotation (contacts are punctual)
cType = "_3_DOF"
# string identifying the limb
rLegId = 'rfleg'
# First joint of the limb, as in urdf file
rLeg = 'rf_haa_joint'
# Last joint of the limb, as in urdf file
rfoot = 'rf_foot_joint'
# Specifying the distance between last joint and contact surface
rLegOffset = [0.,-0.021,0.]
# Specifying the contact surface direction when the limb is in rest pose
rLegNormal = [0,1,0]
# Specifying the rectangular contact surface length
rLegx = 0.02; rLegy = 0.02
# remaining parameters are the chosen heuristic (here, manipulability), and the resolution of the octree (here, 10 cm).
fullBody.addLimb(rLegId,rLeg,rfoot,rLegOffset,rLegNormal, rLegx, rLegy, nbSamples, "manipulability", 0.1, cType)

lLegId = 'lhleg'
lLeg = 'lh_haa_joint'
lfoot = 'lh_foot_joint'
lLegOffset = [0.,-0.021,0.]
lLegNormal = [0,1,0]
lLegx = 0.02; lLegy = 0.02
fullBody.addLimb(lLegId,lLeg,lfoot,lLegOffset,rLegNormal, lLegx, lLegy, nbSamples, "manipulability", 0.05, cType)

rarmId = 'rhleg'
rarm = 'rh_haa_joint'
rHand = 'rh_foot_joint'
rArmOffset = [0.,-0.021,0.]
rArmNormal = [0,1,0]
rArmx = 0.02; rArmy = 0.02
fullBody.addLimb(rarmId,rarm,rHand,rArmOffset,rArmNormal, rArmx, rArmy, nbSamples, "manipulability", 0.05, cType)

larmId = 'lfleg'
larm = 'lf_haa_joint'
lHand = 'lf_foot_joint'
lArmOffset = [0.,-0.021,0.]
lArmNormal = [0,1,0]
lArmx = 0.02; lArmy = 0.02
fullBody.addLimb(larmId,larm,lHand,lArmOffset,lArmNormal, lArmx, lArmy, nbSamples, "forward", 0.05, cType)
# RB: this line is never used?
q_0 = fullBody.getCurrentConfig(); 

fullBody.client.basic.robot.setJointConfig('lf_hfe_joint',[-1.4])
fullBody.client.basic.robot.setJointConfig('lh_hfe_joint',[-1.4])
fullBody.client.basic.robot.setJointConfig('rf_hfe_joint',[-1.4])
fullBody.client.basic.robot.setJointConfig('rh_hfe_joint',[-1.4])

# q_init = [4, 0, 0.65, 1,0,0,0];
# q_goal = [-27, 0, 0.65, 1,0,0,0];

# q_init = fullBody.getCurrentConfig(); q_init[0:7] = [4, 0, 0.65, 1,0,0,0]
# q_goal = fullBody.getCurrentConfig(); q_goal[0:7] = [-27, 0, 0.65, 1,0,0,0]

# fullBody.setCurrentConfig (q_init)
# q_init = fullBody.generateContacts(q_init, [0,0,1])

# # Randomly generating a contact configuration at q_end
# fullBody.setCurrentConfig (q_goal)
# q_goal = fullBody.generateContacts(q_goal, [0,0,1])



# RW: update the problem solver and viewer
ps = ProblemSolver(fullBody)
r = Viewer (ps)




# fullBody.setStartState(q_init,[])
# fullBody.setEndState(q_goal,[rLegId,lLegId,rarmId,larmId])

r.loadObstacleModel ('hpp-rbprm-corba', name_of_scene, "contact")
r.client.gui.setColor('contact', [1,1,1,0.5])


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


# allT = importTrajectory(filename)

# take agent 0 for example
# tra = allT[0]

# q_all = []
# for t in tra:
# 	config = fullBody.getCurrentConfig()
# 	config[0:7] = [t[0], t[1], 0, 1, 0, 0, 0]
# 	print config[0], config[1]
# 	configx = fullBody.generateContacts(config, [0,0,1])
# 	q_all.append(configx)

# fullBody.setStartState(q_all[0],[])
# fullBody.setEndState(q_all[-1],[rLegId,lLegId,rarmId,larmId])



def exportContacts(agent_index, configs, filename):
	f = open(filename, 'a+')
	f.write('agent ' + str(agent_index) + '\n')
	for p in configs:
		f.write(str(p)[1:-1] + '\n')
	f.close()



def computeContacts(filename):
	allT = importTrajectory(filename)
	for a in allT:
		tra = allT[0]
		q_all = []
		for t in tra:
			config = fullBody.getCurrentConfig()
			config[0:7] = [t[0], t[1], 0, 1, 0, 0, 0]
			print a, ' - ', config[0], config[1]
			configx = fullBody.generateContacts(config, [0,0,1])
			q_all.append(configx)
		fullBody.setStartState(q_all[0],[])
		fullBody.setEndState(q_all[-1],[rLegId,lLegId,rarmId,larmId])
		configs = fullBody.interpolateConfigs(q_all, 0)
		filename = filename.split('.')[0] + '.contact'
		exportContacts(a, configs, filename)



def main():
	print sys.argv[1]
	computeContacts(sys.argv[1])

if __name__ == "__main__":
    main()



# filename = 'allPath'


#*******************************************************
# l = np.arange(-27,4.5,0.5)
# l = l.tolist()
# l.reverse()

# q_all = []
# for i in range(len(l)):
# 	config = fullBody.getCurrentConfig()
# 	config[0:7] = [l[i], 0, 0.65,1,0,0,0]
# 	config = fullBody.generateContacts(config, [0,0,1])
# 	q_all.append(config)

# fullBody.setStartState(q_all[0],[])
# fullBody.setEndState(q_all[-1],[rLegId,lLegId,rarmId,larmId])



# configs = fullBody.interpolateConfigs(q_all, 0)


# def playpath(fullBody, configs):
# 	i = 0;
# 	#~ # fullBody.draw(configs[i],r); i=i+1; i-1
# 	#~ 
# 	while (i < len(configs)):
# 		fullBody.draw(configs[i],r)
# 		sleep(0.1)
# 		i = i + 1




# playpath(fullBody, configs)
# playpath(fullBody, q_all)





# ****************************************************************************
# Randomly generating a contact configuration at q_init
# fullBody.setCurrentConfig (q_init)
# q_init = fullBody.generateContacts(q_init, [0,0,1])

# # Randomly generating a contact configuration at q_end
# fullBody.setCurrentConfig (q_goal)
# q_goal = fullBody.generateContacts(q_goal, [0,0,1])

# # specifying the full body configurations as start and goal state of the problem
# fullBody.setStartState(q_init,[])
# fullBody.setEndState(q_goal,[rLegId,lLegId,rarmId,larmId])


# r(q_init)
# # computing the contact sequence
# configs = fullBody.interpolate(0.2, 1, 0)
# # RB: Is this line redundent?
# # r.loadObstacleModel ('hpp-rbprm-corba', name_of_scene, "contact")
# r.client.gui.setColor('contact', [1,1,1,0.3])

# i = 0;
# #~ # fullBody.draw(configs[i],r); i=i+1; i-1
# #~ 
# while (i < len(configs)):
# 	fullBody.draw(configs[i],r)
# 	sleep(0.05)
# 	i = i + 1

# print "Animation finished!"
