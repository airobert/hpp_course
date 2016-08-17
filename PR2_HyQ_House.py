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
agt1.playPath()



agt2 = HyQ(pl, 2, "side")
pl.addAgent(agt2)

pl.main_agent.loadModel('side', 'planar')

pl.main_agent.client.robot.loadRobotModel("side", "planar", "hyq_description", "hyq", "", "")


