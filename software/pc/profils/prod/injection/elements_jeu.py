# -*- encoding:utf-8 -*-



"""
Ce module set à placer tous les élements de jeu

:param totems: Tableau de totems, recensant les 2 totems du jeu
:type totem: list of Totem

:param reglettes: Tableau de reglettes, recensant les 4 reglettes du jeu
:type reglettes: list of RegletteEnBois

:TODO: Disques, Lingots, Cartes aux trésor, Poussoir, zones.

"""

# ../../../
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

import lib.elements_jeu as elements_jeu
import lib.math.point as point


"""
Totems

"""
pointTotem1 = point.Point(640+477,1000)
pointTotem2 = point.Point(3000 - (640+477), 1000)

totem1 = elements_jeu.Totem(point1)
totem2 = elements_jeu.Totem(point2)


totems = [totem1, totem2]

"""
Règlettes en bois

"""

pointReglette1SG = point.Point(0,500)
pointReglette1ID = point.Point(400, 500+18)

pointReglette2SG = point.Point(3000-400, 500)
pointReglette2ID = point.Point(3000, 500+18)

pointReglette3SG = point.Point(337,2000-740)
pointReglette3ID = point.Point(337+18, 2000)

pointReglette4SG = point.Point(3000 - 337, 2000 - 740)
pointReglette4ID = point.Point(3000 - 337 - 18, 2000)

reglette1 = elements_jeu.RegletteEnBois(pointReglette1SG, pointReglette1ID)
reglette2 = elements_jeu.RegletteEnBois(pointReglette2SG, pointReglette2ID)
reglette3 = elements_jeu.RegletteEnBois(pointReglette3SG, pointReglette3ID)
reglette4 = elements_jeu.RegletteEnBois(pointReglette4SG, pointReglette4ID)

reglettes = [reglette1, reglette2, reglette3, reglette4]

"""
Boutons poussoir
:TODO: Gerer l'assignation de la variable enemy
"""

pointPoussoir1 = point.Point(640, 2000)
pointPoussoir2 = point.Point(640 + 477, 2000)
pointPoussoir3 = point.Point(3000 - 640 - 477, 2000)
pointPoussoir4 = point.Point(3000 - 640, 2000)

enemy = False     # :TODO:

poussoir1 = elements_jeu.Poussoir(pointPoussoir1, enemy)
poussoir2 = elements_jeu.Poussoir(pointPoussoir2, enemy)
poussoir3 = elements_jeu.Poussoir(pointPoussoir3, enemy)
poussoir4 = elements_jeu.Poussoir(pointPoussoir4, enemy)

poussoirs = [poussoir1, poussoir2, poussoir3, poussoir4]

"""
Lingots
TODO gerer l'assignation de la variable enemy
"""


pointLingot1 = point.Point(1500, 3000-647) #en bas au milieu
pointLingot2 = point.Point(3000 - 450, 518 + 280) #droite
pointLingot3 = point.Point(450, 518 + 280) #gauche

oriLingot1 = 0
oriLingot2 = 3.1415/2    #TODO + un petit truc
oriLingot3 = 3.1415/2    #TODO - un petit truc

#TODO Les deux autres lingots dans les totems

enemy = False  #TODO

lingot1 = elements_jeu.Lingot(pointLingot1, oriLingot1)
lingot2 = elements_jeu.Lingot(pointLingot2, oriLingot2)
lingot3 = elements_jeu.Lingot(pointLingot3, oriLingot3)

Lingots = [lingot1, lingot2, lingot3]
