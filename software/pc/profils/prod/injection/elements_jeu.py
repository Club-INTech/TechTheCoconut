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


"""

# ../../../
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

import lib.elements_jeu as elements_jeu
import lib.outils_math.point as point
import lib.carte as mod_carte

import math

# Création de la carte
carte = mod_carte.Carte()

# TODO gérer l'assignation de cette variable
# NOTE Soit 'R', soit 'V'
couleur_robot = constantes["couleur"]



"""
Totems

"""
pointTotem1 = point.Point(400,1000)
pointTotem2 = point.Point(-400, 1000)

carte.ajouter_totem(elements_jeu.Totem(pointTotem1, couleur_robot == 'R'))
carte.ajouter_totem(elements_jeu.Totem(pointTotem2, couleur_robot == 'V'))

"""
Règlettes en bois
"""

pointReglette1 = point.Point(1500. - 200, 500. + 6)
oriReglette1   = 0
longueurReglette1 = 400.

pointReglette2 = point.Point(-1500. + 200, 500 + 6)
oriReglette2   = 0
longueurReglette2 = 400.

pointReglette3 = point.Point(1500. - 345, 2000 - 375)
oriReglette3   = math.atan((3000.-500.)/(400-325.))
longueurReglette3 = 750.

pointReglette4 = point.Point(-1500 + 345., 2000. - 375)
oriReglette4   = 3.1415 - math.atan((3000-500.)/(400-325.))
longueurReglette4 = 750.

carte.ajouter_regletteEnBois(elements_jeu.RegletteEnBois(pointReglette1, oriReglette1, longueurReglette1))
carte.ajouter_regletteEnBois(elements_jeu.RegletteEnBois(pointReglette2, oriReglette2, longueurReglette2))
carte.ajouter_regletteEnBois(elements_jeu.RegletteEnBois(pointReglette3, oriReglette3, longueurReglette3))
carte.ajouter_regletteEnBois(elements_jeu.RegletteEnBois(pointReglette4, oriReglette4, longueurReglette4))


"""
Boutons poussoir
"""

pointPoussoir1 = point.Point(1500 - 640, 2000)
pointPoussoir2 = point.Point(1500 - 640 - 477, 2000)
pointPoussoir3 = point.Point(-1500 + 640 + 477, 2000)
pointPoussoir4 = point.Point(-1500 + 640, 2000)


carte.ajouter_poussoir(elements_jeu.Poussoir(pointPoussoir1, couleur_robot == 'R'))
carte.ajouter_poussoir(elements_jeu.Poussoir(pointPoussoir2, couleur_robot == 'V'))
carte.ajouter_poussoir(elements_jeu.Poussoir(pointPoussoir3, couleur_robot == 'R'))
carte.ajouter_poussoir(elements_jeu.Poussoir(pointPoussoir4, couleur_robot == 'V'))


"""
Cartes au trésor

"""

pointCarte1 = point.Point(100,0)
pointCarte2 = point.Point(-100,0)

carte.ajouter_carteAuTresor(elements_jeu.CarteAuTresor(pointCarte1, couleur_robot == 'R'))
carte.ajouter_carteAuTresor(elements_jeu.CarteAuTresor(pointCarte2, couleur_robot == 'V'))


"""
Lingots
"""

hauteur = 0

pointLingot1 = point.Point(0, 3000-647) #en bas au milieu
pointLingot2 = point.Point(-1500 + 400, 518 + 280) #droite
pointLingot3 = point.Point(+1500 - 400, 518 + 280) #gauche

oriLingot1 = 0
oriLingot2 = 3.1415/2    #WARNING Normalement, ce lingot est un petit peu penché... Mais OSEF.
oriLingot3 = 3.1415/2    #WARNING Normalement, ce lingot est un petit peu penché...


carte.ajouter_lingot(elements_jeu.Lingot(pointLingot1, oriLingot1, hauteur, True))
carte.ajouter_lingot(elements_jeu.Lingot(pointLingot2, oriLingot2, hauteur, couleur_robot == 'V'))
carte.ajouter_lingot(elements_jeu.Lingot(pointLingot3, oriLingot3, hauteur, couleur_robot == 'R'))

# Lingots des totems
oriLingotsTotem = 3.1415 /2
hauteur = 18 + 54.5

pointLingot4 = point.Point(400 + 125, 1000)
pointLingot5 = point.Point(400 - 125, 1000)
pointLingot6 = point.Point(-400 + 125, 1000)
pointLingot7 = point.Point(-400 - 125, 1000)

carte.ajouter_lingot(elements_jeu.Lingot(pointLingot4, oriLingotsTotem, hauteur, couleur_robot == 'R')) #NOTE Est-ce bien oriLingotsTotem ? (Anthony)
carte.ajouter_lingot(elements_jeu.Lingot(pointLingot5, oriLingotsTotem, hauteur, couleur_robot == 'R'))
carte.ajouter_lingot(elements_jeu.Lingot(pointLingot6, oriLingotsTotem, hauteur, couleur_robot == 'V'))
carte.ajouter_lingot(elements_jeu.Lingot(pointLingot7, oriLingotsTotem, hauteur, couleur_robot == 'V'))


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

ptDisque5 = point.Point(400 - 170, 1000 -170)
ptDisque6 = point.Point(400, 1000 - 230)
ptDisque7 = point.Point(400 + 170, 1000 - 170)
ptDisque8 = point.Point(400 + 230, 1000)
ptDisque9 = point.Point(400 + 170, 1000 + 170)
ptDisque10 = point.Point(400 - 170, 1000 + 170)

ptDisque11 = point.Point(-400 + 170, 1000 - 170)
ptDisque12 = point.Point(-400, 1000 - 230)
ptDisque13 = point.Point(-400 - 170, 1000 - 170)
ptDisque14 = point.Point(-400 - 230, 1000)
ptDisque15 = point.Point(-400 - 170, 1000 + 170)
ptDisque16 = point.Point(-400 + 170, 1000 + 170)

ptDisque17 = point.Point(0, 2000-(240+120+30))
ptDisque18 = point.Point(0, 2000-(240 - 30))

# On rentre les variables disques dans la Carte.
for i in range(1, 19) :
    exec("if (ptDisque" + str(i) + " == 0) :\n enemy = True\nelif (ptDisque" + str(i) +".x > 0) == (couleur_robot == 'R'):\n enemy = True\nelse:\n enemy = False\ncarte.ajouter_disque(elements_jeu.Disque(ptDisque"+str(i)+", 0, couleur, hauteur, enemy))")



couleur = "NOIR"

ptDisque19 = point.Point(400, 1000 + 230)
ptDisque20 = point.Point(-400, 1000 + 230)
ptDisque21 = point.Point(90, 2000 - 300)
ptDisque22 = point.Point(-90, 2000 - 300)

# On rentre les disques noirs dans la Carte
for i in range (19, 23):
    exec("if (ptDisque" + str(i) +".x > 0) == (couleur_robot == 'R'):\n enemy = True\nelse:\n enemy = False\ncarte.ajouter_disque(elements_jeu.Disque(ptDisque"+str(i)+", 0, couleur, hauteur, enemy))")  

# Niveau 1 des totems
hauteur = 18
couleur = "BLANC"
radius = 80
ptDisque23 = point.Point(400 - radius, 1000 - radius)
ptDisque24 = point.Point(400 + radius, 1000 - radius)
ptDisque25 = point.Point(400 + radius, 1000 + radius)
ptDisque26 = point.Point(400 - radius, 1000 + radius)
ptDisque27 = point.Point(-400 + radius, 1000 - radius)
ptDisque28 = point.Point(-400 - radius, 1000 - radius)
ptDisque29 = point.Point(-400 - radius, 1000 + radius)
ptDisque30 = point.Point(-400 + radius, 1000 + radius)

# On rentre les disques du niveau 1 dans la Carte
for i in range (23, 31):
    exec("if (ptDisque" + str(i) +".x > 0) == (couleur_robot == 'R'):\n enemy = True\nelse:\n enemy = False\ncarte.ajouter_disque(elements_jeu.Disque(ptDisque"+str(i)+", 0, couleur, hauteur, enemy))")

    
# Niveau 3 des totems :
hauteur = 18 + 18 + 18 + 2* 54.5

# On rentre les disques du niveau 3 dans la Carte
for i in range (23, 31):
    exec("if (ptDisque" + str(i) +".x > 0) == (couleur_robot == 'R'):\n enemy = True\nelse:\n enemy = False\ncarte.ajouter_disque(elements_jeu.Disque(ptDisque"+str(i)+", 0, couleur, hauteur, enemy))")

"""
Zones de jeu

"""

# Bureau du capitaine violet
angleSD = point.Point(1000, 500)
angleSG = point.Point(1500, 500)
angleID = point.Point(1000, 0  )
angleIG = point.Point(1500, 0  )

enemy = couleur_robot == 'R'
carte.ajouter_zone(elements_jeu.Zone("BUREAUCAPITAINE", angleSD, angleSG, angleID, angleIG, enemy))

# Bureau du capitaine rouge
angleSD = point.Point(-1500, 500)
angleSG = point.Point(-1000, 500)
angleID = point.Point(-1500, 0  )
angleIG = point.Point(-1000, 0  )

enemy = couleur_robot == 'V'
carte.ajouter_zone(elements_jeu.Zone("BUREAUCAPITAINE", angleSD, angleSG, angleID, angleIG, enemy))

# Zone du pont violet
angleSD = point.Point(1500 - 350, 2000 - 630)
angleSG = point.Point(1500, 2000 - 630)
angleID = point.Point(1500 - 400, 518)
angleIG = point.Point(1500, 518)

enemy = couleur_robot == 'R'
carte.ajouter_zone(elements_jeu.Zone("CALE", angleSD, angleSG, angleID, angleIG, enemy))

# Zone du pont rouge
angleSD = point.Point(-1500, 2000 - 630)
angleSG = point.Point(-1500 + 350, 2000 - 630)
angleID = point.Point(-1500, 518)
angleIG = point.Point(-1500 + 400, 518)

enemy = couleur_robot == 'V'
carte.ajouter_zone(elements_jeu.Zone("CALE", angleSD, angleSG, angleID, angleIG, enemy))

# Zone de la cale violette
angleSD = point.Point(1500 - 325, 2000)
angleSG = point.Point(1500, 2000)
angleID = point.Point(1500 - 325, 2000 - 630)
angleIG = point.Point(1500, 2000 - 630)

enemy = couleur_robot == 'R'
carte.ajouter_zone(elements_jeu.Zone("CALEPROTEGEE", angleSD, angleSG, angleID, angleIG, enemy))

# Zone de la cale violette
angleSD = point.Point(-1500, 2000)
angleSG = point.Point(-1500 + 325, 2000)
angleID = point.Point(-1500, 2000 - 630)
angleIG = point.Point(-1500 + 325, 2000 - 630)

enemy = couleur_robot == 'V'
carte.ajouter_zone(elements_jeu.Zone("CALEPROTEGEE", angleSD, angleSG, angleID, angleIG, enemy))