#!/usr/bin/env python

###
### This file is generated automatically by SALOME v9.13.0 with dump python functionality
###

import sys
import salome

salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()
sys.path.insert(0, r'/adhome/a/ad/a.demuth/a.demuth/a.demuth/Bureau/M2-GIT/M2-csmi/Traitement_de_maillage/salome')

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS


geompy = geomBuilder.New()

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
Box_1 = geompy.MakeBoxDXDYDZ(200, 200, 200)
Cylinder_1 = geompy.MakeCylinderRH(100, 300)
Translation_1 = geompy.MakeTranslation(Cylinder_1, 100, 100, 0)
Cut_1 = geompy.MakeCutList(Box_1, [Translation_1], True)
Torus_1 = geompy.MakeTorusRR(50, 13)
Torus_2 = geompy.MakeTorusRR(50, 13)
Cylinder_1.SetAutoColor(1)
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Cylinder_1, 'Cylinder_1' )
geompy.addToStudy( Box_1, 'Box_1' )
geompy.addToStudy( Translation_1, 'Translation_1' )
geompy.addToStudy( Cut_1, 'Cut_1' )
geompy.addToStudy( Torus_1, 'Torus_1' )
geompy.addToStudy( Torus_2, 'Torus_2' )


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()
