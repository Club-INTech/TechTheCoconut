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
asser.serialInstance.write('cy\n' + str(float(500)))
asser.serialInstance.write('cx\n' + str(float(500)))



robotInstance=robot.Robot()
asser = asservissement.Asservissement(robotInstance)
#scriptInstance = script.Script(asser)
#scriptInstance.huit()

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



"""
while i+1 < len(chemin):
    centre_avr.append(asser.pythonToAvr(chemin[i],chemin[i+1]))
    i += 1
    
i = 0
for i in centre_avr:
    print "goto " + str(i.x) + ' ' + str(i.y) + '\n'
"""