# load gmsh module
import gmsh
import sys

# init gmsh API
gmsh.initialize()

# instructions for building CAD shall be inserted here
gmsh.model.add("square")

Lc = 1e-1
Lx = Ly = 1

p1 = gmsh.model.occ.addPoint(-Lx, -Ly, 0, Lc)
p2 = gmsh.model.occ.addPoint(-0, -Ly, 0, Lc)
p3 = gmsh.model.occ.addPoint(-Lx, 0, 0, Lc)
p4 = gmsh.model.occ.addPoint(0, 0, 0, Lc)
# create lines
l1 = gmsh.model.occ.addLine(p1, p2)
l2 = gmsh.model.occ.addLine(p2, p4)
l3 = gmsh.model.occ.addLine(p4, p3)
l4 = gmsh.model.occ.addLine(p3, p1)

#add square
square = gmsh.model.occ.addCurveLoop([l1, l2, l3, l4], 1)
s = gmsh.model.occ.addPlaneSurface([square], 1)

#add circle
disk = gmsh.model.occ.addCircle(-Lx/2,-Ly/2,0,0.2)
l = gmsh.model.occ.addCurveLoop([disk])

d = gmsh.model.occ.addPlaneSurface([l])
gmsh.model.occ.cut([(2,s)],[(2,d)])

#gmsh.model.occ.remove([(2,2)])
# Force synchro
gmsh.model.occ.synchronize()

# view gmsh GUI
if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()