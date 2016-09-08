

from hpp.corbaserver.rbprm.rbprmbuilder import Builder
from hpp.corbaserver.rbprm.rbprmfullbody import FullBody
from hpp.corbaserver.rbprm.problem_solver import ProblemSolver
from hpp.gepetto import Viewer
from time import sleep
import numpy as np



class Avatar ():


	packageName = "hyq_description"
	meshPackageName = "hyq_description"
	rootJointType = 'freeflyer'
	urdfName = "hyq"
	urdfSuffix = ""
	srdfSuffix = ""
	rootName = 'base_joint_xyz'
	name_of_scene = "simple_boeing"

	nbSamples = 10000
	lLegId = 'lhleg'
	lLeg = 'lh_haa_joint'
	lfoot = 'lh_foot_joint'
	lLegOffset = [0.,-0.021,0.]
	lLegNormal = [0,1,0]
	lLegx = 0.02; lLegy = 0.02


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
	rarmId = 'rhleg'
	rarm = 'rh_haa_joint'
	rHand = 'rh_foot_joint'
	rArmOffset = [0.,-0.021,0.]
	rArmNormal = [0,1,0]
	rArmx = 0.02; rArmy = 0.02
	larmId = 'lfleg'
	larm = 'lf_haa_joint'
	lHand = 'lf_foot_joint'
	lArmOffset = [0.,-0.021,0.]
	lArmNormal = [0,1,0]
	lArmx = 0.02; lArmy = 0.02


	def __init__ (self, robot, start, end):
		self.fullBody = FullBody () 
		self.fullBody.loadFullBodyModel(urdfName, rootJointType, meshPackageName, packageName, urdfSuffix, srdfSuffix)
		# remaining parameters are the chosen heuristic (here, manipulability), and the resolution of the octree (here, 10 cm).
		self.fullBody.addLimb(rLegId,rLeg,rfoot,rLegOffset,rLegNormal, rLegx, rLegy, nbSamples, "manipulability", 0.1, cType)
		self.fullBody.addLimb(lLegId,lLeg,lfoot,lLegOffset,rLegNormal, lLegx, lLegy, nbSamples, "manipulability", 0.05, cType)
		self.fullBody.addLimb(rarmId,rarm,rHand,rArmOffset,rArmNormal, rArmx, rArmy, nbSamples, "manipulability", 0.05, cType)
		self.fullBody.addLimb(larmId,larm,lHand,lArmOffset,lArmNormal, lArmx, lArmy, nbSamples, "forward", 0.05, cType)
		self.fullBody.client.basic.robot.setJointConfig('lf_hfe_joint',[-1.4])
		self.fullBody.client.basic.robot.setJointConfig('lh_hfe_joint',[-1.4])
		self.fullBody.client.basic.robot.setJointConfig('rf_hfe_joint',[-1.4])
		self.fullBody.client.basic.robot.setJointConfig('rh_hfe_joint',[-1.4])
		self.q_init = self.fullBody.getCurrentConfig(); q_init[0:7] = [4, 0, 0, 1,0,0,0]
		self.q_goal = self.fullBody.getCurrentConfig(); q_goal[0:7] = [-27, 0, 0, 1,0,0,0]
		self.fullBody.setCurrentConfig (self.q_init)
		self.q_init = self.fullBody.generateContacts(self.q_init, [0,0,1])
		self.fullBody.setCurrentConfig (self.q_goal)
		self.q_goal = self.fullBody.generateContacts(self.q_goal, [0,0,1])
		ps = ProblemSolver(fullBody)
		ps.loadObstacleFromUrdf('hpp-rbprm-corba', name_of_scene, "contact")
		

