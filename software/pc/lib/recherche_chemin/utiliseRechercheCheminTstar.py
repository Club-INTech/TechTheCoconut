# -*- coding: utf-8 -*-

"""
exemple d'utilisation de la fonction rechercheChemin avec Theta*.

il faudra importer :
from lib.recherche_chemin.rechercheChemin import *

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
rechercheChemin(Point(-270.,248.),Point(-350.,1200.),centresRobotsA)
tracePDF("chemin_dev1.pdf")
rechercheChemin(Point(-150.,248.),Point(-350.,1190.),centresRobotsA)
tracePDF("chemin_dev2.pdf")
rechercheChemin(Point(-150.,248.),Point(-350.,1180.),centresRobotsA)
tracePDF("chemin_dev3.pdf")