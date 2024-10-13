# load gmsh module
import gmsh
import sys

# init gmsh API
gmsh.initialize()

# instructions for building CAD shall be inserted here
gmsh.model.add("square")

Lc = 1e-1
Lx = Ly = 1

# define points
p1 = gmsh.model.geo.addPoint(-Lx, -Ly, 0, Lc)
p2 = gmsh.model.geo.addPoint(-0, -Ly, 0, Lc)
p3 = gmsh.model.geo.addPoint(-Lx, 0, 0, Lc)
p4 = gmsh.model.geo.addPoint(0, 0, 0, Lc)
# create lines
l1 = gmsh.model.geo.addLine(p1, p2)
l2 = gmsh.model.geo.addLine(p2, p4)
l3 = gmsh.model.geo.addLine(p4, p3)
l4 = gmsh.model.geo.addLine(p3, p1)

gmsh.model.geo.addCurveLoop([l1, l2, l3, l4], 1)
gmsh.model.geo.addPlaneSurface([1], 1)

# Force synchro
gmsh.model.geo.synchronize()

# view gmsh GUI
if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()