# -*- coding: utf-8 -*-

import os,sys
# Ajout de ../.. au path python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from lib.recherche_chemin.rechercheChemin import *
from lib.outils_math.point import Point

discretiseTable()

centresRobotsA = [Point(-20,0)]
rechercheChemin(Point(-120,40),Point(90,140),centresRobotsA)
print "tracePDF -->"
tracePDF("map_chemin_robot1.pdf")


centresRobotsA = [Point(30,0)]
rechercheChemin(Point(-120,40),Point(90,140),centresRobotsA)
print "tracePDF -->"
tracePDF("map_chemin_robot2.pdf")