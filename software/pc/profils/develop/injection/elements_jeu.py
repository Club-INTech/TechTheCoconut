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

:TODO: Disques, zones.

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
pointTotem1 = point.Point(400,1000)
pointTotem2 = point.Point(-400, 1000)

enemy = True    #TODO

carte.ajouter_totem(elements_jeu.Totem(pointTotem1, enemy))
carte.ajouter_totem(elements_jeu.Totem(pointTotem2, enemy))

"""
Règlettes en bois

"""

pointReglette1 = point.Point(1500 - 200, 500 + 6)
oriReglette1   = 0
longueurReglette1 = 400

pointReglette2 = point.Point(-1500 + 200, 500 + 6)
oriReglette2   = 0
longueurReglette2 = 400

pointReglette3 = point.Point(1500 - 345, 2000 - 375)
oriReglette3   = math.pi - math.atan((3000-500.)/(400-325.))
longueurReglette3 = 750

pointReglette4 = point.Point(-1500 + 345, 2000 - 375)
oriReglette4   = math.atan((3000-500.)/(400-325.))
longueurReglette4 = 750

carte.ajouter_regletteEnBois(elements_jeu.RegletteEnBois(pointReglette1, oriReglette1, longueurReglette1))
carte.ajouter_regletteEnBois(elements_jeu.RegletteEnBois(pointReglette2, oriReglette2, longueurReglette2))
carte.ajouter_regletteEnBois(elements_jeu.RegletteEnBois(pointReglette3, oriReglette3, longueurReglette3))
carte.ajouter_regletteEnBois(elements_jeu.RegletteEnBois(pointReglette4, oriReglette4, longueurReglette4))


"""
Boutons poussoir
:TODO: Gerer l'assignation de la variable enemy
"""

pointPoussoir1 = point.Point(150 - 640, 2000)
pointPoussoir2 = point.Point(1500 - 640 + 477, 2000)
pointPoussoir3 = point.Point(-1500 + 640 - 477, 2000)
pointPoussoir4 = point.Point(-1500 + 640, 2000)

enemy = False     # :TODO:

carte.ajouter_poussoir(elements_jeu.Poussoir(pointPoussoir1, enemy))
carte.ajouter_poussoir(elements_jeu.Poussoir(pointPoussoir2, enemy))
carte.ajouter_poussoir(elements_jeu.Poussoir(pointPoussoir3, enemy))
carte.ajouter_poussoir(elements_jeu.Poussoir(pointPoussoir4, enemy))


"""
Cartes au trésor

"""

pointCarte1 = point.Point(100,0)
pointCarte2 = point.Point(-100,0)

enemy = False   #TODO

carte.ajouter_carteAuTresor(elements_jeu.CarteAuTresor(pointCarte1))
carte.ajouter_carteAuTresor(elements_jeu.CarteAuTresor(pointCarte2)


"""
Lingots
TODO gerer l'assignation de la variable enemy
"""


pointLingot1 = point.Point(0, 3000-647) #en bas au milieu
pointLingot2 = point.Point(-1500 + 400, 518 + 280) #droite
pointLingot3 = point.Point(+1500 - 400, 518 + 280) #gauche

oriLingot1 = 0
oriLingot2 = math.pi/2    #WARNING Normalement, ce lingot est un petit peu penché...
oriLingot3 = math.pi/2    #WARNING Normalement, ce lingot est un petit peu penché...

                #TODO Les deux autres lingots dans les totems

enemy = False  #TODO

carte.ajouter_lingot(elements_jeu.Lingots(pointLingot1, oriLingot1))
carte.ajouter_lingot(elements_jeu.Lingots(pointLingot2, oriLingot2))
carte.ajouter_lingot(elements_jeu.Lingots(pointLingot3, oriLingot3))


"""
Palmier

"""

pointPalmier = point.Point(0,1000)

carte.ajouter_palmier(elements_jeu.Palmier(pointPalmier))


"""
Disques

"""

hauteur = 0
couleur = "BLANC"
enemy = False                # TODO

ptDisque1 = point.Point(500, 500)
ptDisque2 = point.Point(-500, 500)
ptDisque3 = point.Point(1500 - 450, 2000-300)
ptDisque4 = point.Point(-1500 + 450, 2000-300)

ptDisque5 = point.Point(400 - 170, 1000 - 170)
ptDisque6 = point.Point(400, 1000 - 230)
ptDisque7 = point.Point(400 + 170, 1000 - 170)
ptDisque8 = point.Point(400 + 230, 1000)
ptDisque9 = point.Point(400 + 170, 1000 + 170)
ptDisque10 = point.Point(400 - 170, 1000 + 230)

ptDisque11 = point.Point(-400 + 170, 1000 - 170)
ptDisque12 = point.Point(-400, 1000 - 230)
ptDisque13 = point.Point(-400 - 170, 1000 - 170)
ptDisque14 = point.Point(-400 - 230, 1000)
ptDisque15 = point.Point(-400 - 170, 1000 + 170)
ptDisque16 = point.Point(-400 + 170, 1000 + 230)

ptDisque17 = point.Point(0, 240+120+30)
ptDisque18 = point.Point(0, 240 - 30)

# On rentre les variables disques dans la Carte.
for i in range(1, 19) :
    exec("carte.ajouter_disque(elements_jeu.Disque(ptDisque"+str(i)+", 0, couleur, hauteur, enemy)")



couleur = "NOIR"

ptDisque19 = point.Point(400, 1000 + 230)
ptDisque20 = point.Point(-400, 1000 + 230)
ptDisque21 = point.Point(90, 2000 - 300)
ptDisque22 = point.Point(-90, 2000 - 300)

# On rentre les disques noirs dans la Carte
for i in range (19, 23):
    exec("carte.ajouter_disque(elements_jeu.Disque(ptDisque"+str(i)+", 0, couleur, hauteur, enemy)")


    
# TODO pas fini : Il reste les disques qui sont dans les totems



"""
Zones de jeu

"""

# Bureau du capitaine violet
angleSD = point.Point(1000, 500)
angleSG = point.Point(1500, 500)
angleID = point.Point(1000, 0  )
angleIG = point.Point(1500, 0  )

enemy = True
carte.ajouter_zone(elements_jeu.Zone("BUREAUCAPITAINE", angleSD, angleSG, angleID, angleIG, enemy))

# Bureau du capitaine rouge
angleSD = point.Point(-1500, 500)
angleSG = point.Point(-1000, 500)
angleID = point.Point(-1500, 0  )
angleIG = point.Point(-1000, 0  )

enemy = True
carte.ajouter_zone(elements_jeu.Zone("BUREAUCAPITAINE", angleSD, angleSG, angleID, angleIG, enemy))

# Zone du pont violet
angleSD = point.Point(1500 - 350, 2000 - 630)
angleSG = point.Point(1500, 2000 - 630)
angleID = point.Point(1500 - 400, 518)
angleIG = point.Point(1500, 518)

enemy = True
carte.ajouter_zone(elements_jeu.Zone("CALE", angleSD, angleSG, angleID, angleIG, enemy))

# Zone du pont rouge
angleSD = point.Point(-1500, 2000 - 630)
angleSG = point.Point(-1500 + 350, 2000 - 630)
angleID = point.Point(-1500, 518)
angleIG = point.Point(-1500 + 400, 518)

enemy = True
carte.ajouter_zone(elements_jeu.Zone("CALE", angleSD, angleSG, angleID, angleIG, enemy))

# Zone de la cale violette
angleSD = point.Point(1500 - 325, 2000)
angleSG = point.Point(1500, 2000)
angleID = point.Point(1500 - 325, 2000 - 630)
angleIG = point.Point(1500, 2000 - 630)

enemy = True
carte.ajouter_zone(elements_jeu.Zone("CALEPROTEGEE", angleSD, angleSG, angleID, angleIG, enemy))

# Zone de la cale violette
angleSD = point.Point(-1500, 2000)
angleSG = point.Point(-1500 + 325, 2000)
angleID = point.Point(-1500, 2000 - 630)
angleIG = point.Point(-1500 + 325, 2000 - 630)

enemy = True
carte.ajouter_zone(elements_jeu.Zone("CALEPROTEGEE", angleSD, angleSG, angleID, angleIG, enemy))