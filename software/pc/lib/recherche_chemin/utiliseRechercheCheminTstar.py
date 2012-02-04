# -*- coding: utf-8 -*-

"""
exemple d'utilisation de la fonction rechercheChemin avec Theta*.

enregistreGraphe doit etre appelé pour stocker en dur le graphe de la table.

on peut ensuite appeler rechercheChemin autant de fois que voulu
rechercheChemin(a,b) où a et b sont des Points renvoi une liste de Points, du départ à l'arrivée

"""

import os,sys
# Ajout de ../.. au path python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from lib.recherche_chemin.rechercheCheminTstar import *
from lib.outils_math.point import Point


enregistreGraphe()

centresRobotsA = []
rechercheChemin(Point(0.,360.),Point(500.,1500.),centresRobotsA)
print "tracePDF -->"
tracePDF("chemin_0_robotsA.pdf")
"""
centresRobotsA = [Point(10.,30.)]
rechercheChemin(Point(-110.,40.),Point(120.,140.),centresRobotsA)
print "tracePDF -->"
tracePDF("chemin_1_robotsA.pdf")

centresRobotsA = [Point(10.,30.),Point(-100.,200.)]
rechercheChemin(Point(-110.,40.),Point(120.,140.),centresRobotsA)
print "tracePDF -->"
tracePDF("chemin_2_robotsA.pdf")
"""