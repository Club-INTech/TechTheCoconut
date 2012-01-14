# -*- encoding:utf-8 -*-



"""
Ce module set à placer tous les élements de jeu

:param totems: Tableau de totems, recensant les 2 totems du jeu
:type totem: list of Totem

:param reglettes: Tableau de reglettes, recensant les 4 reglettes du jeu
:type reglettes: list of RegletteEnBois

:param poussoirs: Tableau de poussoirs, recensant les 4 poussoirs du jeu
:type poussoir: list of Poussoir

:param Lingots

:TODO: Disques, Cartes aux trésor, Poussoir, zones.

"""

# ../../../
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

import lib.elements_jeu as elements_jeu
import lib.math.point as point
import lib.carte as mod_carte

import math

# Création de la carte
carte = mod_carte.Carte()



"""
Totems

"""
pointTotem1 = point.Point(-400,1000)
pointTotem2 = point.Point(400, 1000)

totem1 = carte.ajouter_totem(elements_jeu.Totem(point1))
totem2 = carte.ajouter_totem(elements_jeu.Totem(point2))

"""
Règlettes en bois

"""

pointReglette1 = point.Point(-1500 + 200, 500 + 6)
oriReglette1   = 0
longueurReglette1 = 400

pointReglette2 = point.Point(1500 - 200, 500 + 6)
oriReglette2   = 0
longueurReglette2 = 400

pointReglette3 = point.Point(-1500 + 345, 2000 - 375)
oriReglette3   = math.pi - math.atan((3000-500.)/(400-325.))
longueurReglette3 = 750

pointReglette4 = point.Point(1500 - 345, 2000 - 375)
oriReglette4   = math.atan((3000-500.)/(400-325.))
longueurReglette4 = 750

reglette1 = carte.ajouter_regletteEnBois(elements_jeu.RegletteEnBois(pointReglette1, oriReglette1, longueurReglette1))
reglette2 = carte.ajouter_regletteEnBois(elements_jeu.RegletteEnBois(pointReglette2, oriReglette2, longueurReglette2))
reglette3 = carte.ajouter_regletteEnBois(elements_jeu.RegletteEnBois(pointReglette3, oriReglette3, longueurReglette3))
reglette4 = carte.ajouter_regletteEnBois(elements_jeu.RegletteEnBois(pointReglette4, oriReglette4, longueurReglette4))


"""
Boutons poussoir
:TODO: Gerer l'assignation de la variable enemy
"""

pointPoussoir1 = point.Point(640, 2000)
pointPoussoir2 = point.Point(640 + 477, 2000)
pointPoussoir3 = point.Point(3000 - 640 - 477, 2000)
pointPoussoir4 = point.Point(3000 - 640, 2000)

enemy = False     # :TODO:

poussoir1 = carte.ajouter_poussoir(elements_jeu.Poussoir(pointPoussoir1, enemy))
poussoir2 = carte.ajouter_poussoir(elements_jeu.Poussoir(pointPoussoir2, enemy))
poussoir3 = carte.ajouter_poussoir(elements_jeu.Poussoir(pointPoussoir3, enemy))
poussoir4 = carte.ajouter_poussoir(elements_jeu.Poussoir(pointPoussoir4, enemy))


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

lingot1 = carte.ajouter_lingot(elements_jeu.Lingots(pointLingot1, oriLingot1))
lingot2 = carte.ajouter_lingot(elements_jeu.Lingots(pointLingot2, oriLingot2))
lingot3 = carte.ajouter_lingot(elements_jeu.Lingots(pointLingot3, oriLingot3))


"""
Palmier

"""

pointPalmier = point.Point(1500,1000)

palmier1 = carte.ajouter_palmier(elements_jeu.Palmier(pointPalmier))


"""
Disques

"""

hauteur = 0
couleur = "BLANC"

ptDisque1 = point.Point(500+500, 500)
ptDisque2 = point.Point(3000 - 1000, 500)
ptDisque3 = point.Point(450, 2000-300)
ptDisque4 = point.Point(3000 - 450, 2000-300)

ptDisque5 = point.Point(1100 + 170, 1000 - 170)
ptDisque6 = point.Point(1100, 1000 - 230)
ptDisque7 = point.Point(1100 - 170, 1000 - 170)
ptDisque8 = point.Point(1100 - 230, 1000)
ptDisque9 = point.Point(1100 - 170, 1000 + 170)
ptDisque10 =point.Point(1100, 1000 + 230)

# On crée les variables disque1, disque2, disque3....
for i in range(1, 10) :
    exec("carte.ajouter_disque(elements_jeu.Disque(ptDisque"+str(i)+", 0, couleur, hauteur)")

    
# TODO pas fini.

