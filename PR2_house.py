from  Platform import *

pl = Platform("pr2")
bc = BasicHouse("bc")
pl.setEnvironment(bc)

agt = pl.main_agent
agt.activateAgent()
agt.setJointBounds("base_joint_xy", [-10,10,-10,10])
agt.setEnvironment(bc)

q_init = agt.getCurrentConfig()
q_init[0] = -6
q_init[1] = -3
agt.setInitConfig(q_init)

q_goal = q_init[::]
q_goal[0] = 3
q_goal[1] = 3
agt.setGoalConfig(q_goal)
agt.solve()
agt.playPath()
