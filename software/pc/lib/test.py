# -*- coding: utf-8 -*-

#serieInstance = lib.serie.Serie("/dev/ttyUSB1","asservissement",9600,5)

#from asservissement import *
import asservissement
import outils_math
import robot
import recherche_chemin.thetastar
import script

"""
import time
import serie_simple as ss 
from time import sleep


serie1=ss.SerieSimple("/dev/ttyUSB1",9600,5)
serie0=ss.SerieSimple("/dev/ttyUSB0",9600,5)

global dest
dest = "rien"

def recevoir ():
    a=""
    b=""
    try:
            a=serie0.ss.lire()
    except:
        pass
    try:
            b=serie1.ss.lire()
    except:
        pass
    return str(a)+str(b)

def envoyer(arg):
    global dest
    try:
            serie0.ss.ecrire(arg)
    except:
        pass
    try:
            serie1.ss.ecrire(arg)
    except:
        pass
"""

#Tests fait en binome entre recherche de chemin et asservissement.
"""
x = raw_input("Donner les coordonnées en x puis y du point de départ\n")
y = raw_input()
depart = outils_math.point.Point(x,y)

x = raw_input("Donner les coordonnées en x puis y du point de arrivee\n")
y = raw_input()
arrivee = outils_math.point.Point(x,y)
"""
depart = outils_math.point.Point(500.0,500.0)
asser = asservissement.Asservissement(robotInstance)
asser.serieInstance.ecrire('cy\n' + str(float(500)))
asser.serieInstance.ecrire('cx\n' + str(float(500)))
"""
robotInstance=robot.Robot()
asser = asservissement.Asservissement(robotInstance)
scriptInstance = script.Script(asser)
scriptInstance.huit()
"""

while(True):
    x, y = '', ''
    while x=='':
        x = raw_input("x arrivé ?")
    while y=='':
        y = raw_input("y arrivé ?")
    arrivee = outils_math.point.Point(int(x),int(y))
    #print asser.capteursInstance.mesure()

    angle = 0.0
    angle = (float(angle)*3.14)/180
    asser.goTo(depart,arrivee)
"""
theta = recherche_chemin.thetastar.Thetastar([])
chemin_python = theta.rechercheChemin(depart,arrivee)

i = 0
for i
in chemin_python:
    print "goto : (" + str(i.x) + ", "+str(i.y)+")\n"
"""
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




"""
while i+1 < len(chemin):
    centre_avr.append(asser.pythonToAvr(chemin[i],chemin[i+1]))
    i += 1
    
i = 0
for i in centre_avr:
    print "goto " + str(i.x) + ' ' + str(i.y) + '\n'
"""