# hpp-manipulation-server
# gepetto-viewer-server

from ManiHyQ import HyQ as MetaHyQ
from HyQ import HyQ 

from hpp.gepetto.manipulation import ViewerFactory
from hpp.corbaserver.manipulation import ProblemSolver, ConstraintGraph


meta = MetaHyQ('myself')
ps = ProblemSolver (meta)
fk = ViewerFactory (ps)

# fk.loadObjectModel(HyQ, 'sister')
# fk.loadObjectModel(HyQ, 'brother')
meta.insertRobotModel('x', "planar", "hyq_description", "hyq", "","")
meta.insertRobotModel('y', "planar", "hyq_description", "hyq", "","")
meta.insertObjectModel('x', "planar", "hyq_description", "hyq", "","")

meta.setJointBounds ("myself/base_joint_xy", [-20,20,-20,20])
meta.setJointBounds ("x/base_joint_xy", [-20,20,-20,20])
meta.setJointBounds ("y/base_joint_xy", [-20,20,-20,20])

q0 = meta.getCurrentConfig ()

q0 [0] = -1
q0 [1] = -1
q0 [16] = -4
q0 [17] = 4
q0 [32] = 7
q0 [33] = -2
q0 [48] = 9
q0 [49] = 10



fk = ViewerFactory (ps)
r = fk.createViewer ()
r(q0)

graph = ConstraintGraph (meta, 'graph')
graph.createNode (['free'])
graph.createEdge ('free', 'free', 'move_free', 1, 'free')