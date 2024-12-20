import salome
salome.salome_init()
 
from salome.geom import geomBuilder
geompy = geomBuilder.New()

O = geompy.MakeVertex(0, 0, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)

Box_1 = geompy.MakeBoxDXDYDZ(200, 200, 200)
Cylinder_1 = geompy.MakeCylinder(O, OZ, 80, 300)
geompy.TranslateDXDYDZ(Cylinder_1, 100, 100, -50)
Cut_1 = geompy.MakeCutList(Box_1, [Cylinder_1], True)

geompy.addToStudy( Box_1, 'Box_1' )
geompy.addToStudy( Cylinder_1, 'Cylinder_1' )
geompy.addToStudy( Cut_1, 'Cut_1' )