# gepetto-viewer-server
# not hpp-manipulation-server
# hppcorbaserver
# -DCMAKE_INSTALL_PREFIX=/home/airobert/HPP/install


from Agent import *
from Platform import *
from Environment import *


# agent 1 
r1 = PR2Robot('myself')

q_init = r1.getCurrentConfig()
q_goal = q_init[::]
q_init[0] = -5
q_init[1] = -2
q_goal[0] = -1
q_goal[1] = -2

a1 = Agent(r1, q_init, q_goal)

# agent 2 
r2 = PR2Robot('sister')

q_init = r2.getCurrentConfig()
q_goal = q_init[::]
q_init[0] = -3
q_init[1] = -5
q_goal[0] = -3
q_goal[1] = 1

a2 = Agent(r2, q_init, q_goal)

# # agent 3
# r3 = PR2Robot('brother')

# q_init = r3.getCurrentConfig()
# q_goal = q_init[::]
# q_init[0] = 0 # instead of -2
# q_init[1] = 2 # instead of -3
# q_goal[0] = 1.5
# q_goal[1] = 3

# a3 = Agent(r3, q_init, q_goal)

# platform
pl = Platform([a1, a2])
kc = Kitchen("kc")
# pl.setEnvironment(kc)
pl.start()

print 'start the searching with ', pl.tree.getAgentsRemained(), ' remained'

(result, plans) = pl.construct_tree(100)


a1.setPermittedPlan(plans[0])
a2.setPermittedPlan(plans[1])
# a3.setPermittedPlan(plans[2])


pl.playAllPermittedPath()