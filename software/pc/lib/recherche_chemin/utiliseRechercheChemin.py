# -*- coding: utf-8 -*-

"""
exemple d'utilisation de la fonction rechercheChemin.

enregistreGraphe doit etre appelé pour stocker en dur le graphe de la table.
on peut donc le faire avant le jeu. ca prend quelques dizaines de secondes 
(si on met les bonnes valeurs de largeur et longueur dans rechercheChemin)

il faut faire un appel de chargeGraphe() au début du jeu, pour récupérer le graphe.
(on peut peut etre le faire avant et laisser tourner le programme jusqu'au top départ)
ca prend quand meme 5-6 sec (et pas sur un eeePC...)

on peut ensuite appeler rechercheChemin, qui devrait etre assez rapide
rechercheChemin(a,b) où a et b sont des Points renvoi une liste de Points, du départ à l'arrivée

nb : le tracé du pdf est refusé pour les vrais valeurs de longueur et largeur (~3000x1400) : out of memory...
"""

import os,sys
# Ajout de ../.. au path python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from lib.recherche_chemin.rechercheChemin import *
from lib.outils_math.point import Point

#enregistreGraphe()

chargeGraphe()

centresRobotsA = [Point(-20,0)]
rechercheChemin(Point(-120,40),Point(90,140),centresRobotsA)
print "tracePDF -->"
tracePDF("map_chemin_robot1.pdf")


centresRobotsA = [Point(30,0)]
rechercheChemin(Point(-120,40),Point(90,140),centresRobotsA)
print "tracePDF -->"
tracePDF("map_chemin_robot2.pdf")