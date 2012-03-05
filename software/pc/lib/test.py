# -*- coding: utf-8 -*-

from asservissement import *

#Tests fait en binome entre recherche de chemin et asservissement.

"""
x = raw_input("Donner les coordonnées en x puis y du point de départ\n")
y = raw_input()
depart = outils_math.point.Point(x,y)
x = raw_input("Donner les coordonnées en x puis y du point de arrivee\n")
y = raw_input()
arrivee = outils_math.point.Point(x,y)
"""

x = -500
y = 500
depart = outils_math.point.Point(x,y)
x = 2000
y = 800
arrivee = outils_math.point.Point(x,y)

robotInstance = lib.robot.Robot()
angle = raw_input("Donner l'angle des bras\n")
angle = (float(angle)*3.14)/180
lib.robot.orientation = 0.79 #en rad
asser = Asservissement(robotInstance)
robotInstance.rayon = 350

#Ici le centre et le rayon du robot sont initialisés, tu y accèdes avec robot.centre et robot.rayon

"""
mec, ya un problème avec ta méthode centrepython().
elle doit renvoyer le point de centre de périmètre en fonction d'un point de centre avr, et pas modifier l'attribut de classe.
puisqu'on en a besoin pour le départ et l'arrivée. 
-->le calcul doit pouvoir etre appelé pour n'importe quel point

tu crées après une autre méthode qui s'occupe de mettre à jour le rayon du du robot (appelée seulement lors de la modification de l'angle des bras)

l'attribut centre robot doit plutot contenir les coordonnées du centre pour l'avr.

et pis faudrait tester centrepython() et centreAvr() indépendemment, avec des listes de points, avant d'implémenter un joli test de goto.

"""
print angle
theta = recherche_chemin.thetastar.Thetastar([])
print "Appel de la recherche de chemin pour le point de départ : ("+str(depart.x)+","+str(depart.y)+") et d'arrivée : ("+str(arrivee.x)+","+str(arrivee.y)+")"
chemin = theta.rechercheChemin(depart,arrivee)
for i in chemin:
    print "goto " + str(i.x) + ' ' + str(i.y) + '\n'

asser.calculRayon(angle)

"""
while i+1 < len(chemin):
    centre_avr.append(asser.pythonToAvr(chemin[i],chemin[i+1]))
    i += 1
    
i = 0
for i in centre_avr:
    print "goto " + str(i.x) + ' ' + str(i.y) + '\n'
"""