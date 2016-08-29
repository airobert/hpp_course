

from Agent import *
from Platform import *

# agent 1 
r1 = PR2Robot('myself')

q_init = r1.getCurrentConfig()
q_goal = q_init[::]
q_init[0] = -6
q_init[1] = -3
q_goal[0] = 3
q_goal[1] = 3

a1 = Agent(r1, q_init, q_goal)

# agent 2 
r2 = PR2Robot('sister')

q_init = r2.getCurrentConfig()
q_goal = q_init[::]
q_init[0] = 0
q_init[1] = 0
q_goal[0] = 0
q_goal[1] = 3

a2 = Agent(r2, q_init, q_goal)

# agent 3
r3 = PR2Robot('brother')

q_init = r3.getCurrentConfig()
q_goal = q_init[::]
q_init[0] = -2
q_init[1] = -3
q_goal[0] = 1.5
q_goal[1] = 3

a3 = Agent(r3, q_init, q_goal)

agents = [a1, a2, a3]

# platform
pl = Platform(agents)
bc = BasicHouse("bc")
pl.setEnvironment(bc)
pl.start()

a1.startDefaultSolver()
a1.setBounds()
a1.setEnvironment()
a1.loadOtherAgents()
a1.solve()
a1.storePath()

a2.startDefaultSolver()
a2.setBounds()
a2.setEnvironment()
a2.loadOtherAgents()
a2.solve()
a2.storePath()

a3.startDefaultSolver()
a3.setBounds()
a3.setEnvironment()
a3.loadOtherAgents()
a3.solve()
a3.storePath()


# pl.playAllPath()
pl.validateAllPath()
