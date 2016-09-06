#tests completed!

from Agent import *
from HyQ import HyQTrunk
from Platform import *
from Environment import Airplane

# agent 1 
r1 = HyQTrunk('myself')
q_init = [4, 0, 0.65, 1,0,0,0];
q_goal = [-27, 0, 0.65, 1,0,0,0];
r1.setJointBounds ("base_joint_xyz", [-35,10, -4, 4, -1, 1])

a1 = Agent(r1, q_init, q_goal)

# agent 2 
r2 = HyQTrunk('sister')
q_init = [-27, 2, 0.65, 1,0,0,0];
q_goal = [4, 2, 0.65, 1,0,0,0];
r2.setJointBounds ("base_joint_xyz", [-35,10, -4, 4, -1, 1])

a2 = Agent(r2, q_init, q_goal)



# platform
pl = Platform([a1, a2])

air = Airplane("air")
pl.setEnvironment(air)
pl.start()




print 'start the searching with ', pl.tree.getAgentsRemained(), ' remained'

(result, plans) = pl.construct_tree(100)


a1.setPermittedPlan(plans[0])
a2.setPermittedPlan(plans[1])
# a3.setPermittedPlan(plans[2])

pl.playAllPermittedPath()

# a1.startDefaultSolver()
# a1.setBounds()
# a1.setEnvironment()
# a1.loadOtherAgents()
# a1.solve()
# a1.storePath()

# a2.startDefaultSolver()
# a2.setBounds()
# a2.setEnvironment()
# a2.loadOtherAgents()
# a2.solve()
# a2.storePath()

# a3.startDefaultSolver()
# a3.setBounds()
# a3.setEnvironment()
# a3.loadOtherAgents()
# a3.solve()
# a3.storePath()


# pl.playAllPath()



