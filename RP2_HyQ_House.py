from  Platform import *
from HyQ import HyQ

pl = Platform("pr2")
pl.activatePlatform()

bc = BasicHouse("bc")
pl.setEnvironment(bc)


agt1 = pl.main_agent
agt1.activateAgent()
agt1.setJointBounds("base_joint_xy", [-10,10,-10,10])
agt1.setEnvironment(bc)

q_init = agt1.getCurrentConfig()
q_init[0] = -6
q_init[1] = -3
agt1.setInitConfig(q_init)

q_goal = q_init[::]
q_goal[0] = 3
q_goal[1] = 3
agt1.setGoalConfig(q_goal)
agt1.solve()
agt1.platform.loadAgentView(1) # --- works up to here
# pl.refreshDisplay()
# agt1.playPath()

















agt1.activateAgent()

agtx = PR2(pl, 1, "twin")
pl.addAgent(agtx)
agt1.loadOtherAgents()
pl.setEnvironment(bc)
agt1.setInitConfig(q_goal)
agt1.setGoalConfig(q_init)
agt1.setJointBounds("base_joint_xy", [-10,10,-10,10])

agt1.platform.loadAgentView(1)



# agt1.platform.loadAgentView(1)

# pl.refreshDisplay()
agt1.solve()

pl.refreshDisplay()
agt1.playPath()











agt2 = HyQ(pl, 2, "side")
pl.addAgent(agt2)

agt1.activateAgent()
agt1.setJointBounds("base_joint_xy", [-10,10,-10,10])
# agt1.setEnvironment(bc)

agt1.loadOtherAgents()
# vf.problemSolver.client.obstacle.getObstacleNames(False, 1000)
agt1.ps.moveObstacle("sidetrunk_0",[0, 0, 1, 1, 0, 0, 0])
agt1.platform.loadAgentView(2)

agt1.setInitConfig(q_init)
agt1.setGoalConfig(q_goal)

agt1.solve()


# pl.main_agent.loadModel('side', 'planar')

# pl.main_agent.client.robot.loadRobotModel("side", "planar", "hyq_description", "hyq", "", "")


