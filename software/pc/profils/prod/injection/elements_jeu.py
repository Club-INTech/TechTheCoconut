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
import lib.carte as carte


"""
Totems

"""
pointTotem1 = point.Point(640+477,1000)
pointTotem2 = point.Point(3000 - (640+477), 1000)

totem1 = carte.ajouter_totem(point1)
totem2 = carte.ajouter_totem(point2)

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

reglette1 = carte.ajouter_regletteEnBois(pointReglette1SG, pointReglette1ID)
reglette2 = carte.ajouter_regletteEnBois(pointReglette2SG, pointReglette2ID)
reglette3 = carte.ajouter_regletteEnBois(pointReglette3SG, pointReglette3ID)
reglette4 = carte.ajouter_regletteEnBois(pointReglette4SG, pointReglette4ID)

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

poussoir1 = carte.ajouter_poussoir(pointPoussoir1, enemy)
poussoir2 = carte.ajouter_poussoir(pointPoussoir2, enemy)
poussoir3 = carte.ajouter_poussoir(pointPoussoir3, enemy)
poussoir4 = carte.ajouter_poussoir(pointPoussoir4, enemy)

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

lingot1 = carte.ajouter_lingot(pointLingot1, oriLingot1)
lingot2 = carte.ajouter_lingot(pointLingot2, oriLingot2)
lingot3 = carte.ajouter_lingot(pointLingot3, oriLingot3)

lingots = [lingot1, lingot2, lingot3]


"""
Palmier

"""

pointPalmier = point.Point(1500,1000)

palmier1 = carte.ajouter_palmier(pointPalmier)

palmier = [palmier1]

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
    exec("disque"+str(i)+" = carte.ajouter_disque(ptDisque"+str(i)+", 0, couleur, hauteur")
    
# On rempli le tableau disques[] :
disques = []
for i in range(1,10) :
    exec("disques.append(disque"+str(i)+")")
    
# TODO pas fini.

