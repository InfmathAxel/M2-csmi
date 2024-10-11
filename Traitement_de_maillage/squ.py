# load gmsh module
import gmsh
import sys

# init gmsh API
gmsh.initialize()

# instructions for building CAD shall be inserted here

# view gmsh GUI
if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

    gmsh.model.add("square")

