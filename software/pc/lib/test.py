# -*- coding: utf-8 -*-

import asservissement
import outils_math
import robot
import recherche_chemin.thetastar
import script
import time
import serial
import instance
import __builtin__


"""
x = raw_input("Donner les coordonnées en x puis y du point de départ\n")
y = raw_input()
depart = outils_math.point.Point(x,y)

x = raw_input("Donner les coordonnées en x puis y du point de arrivee\n")
y = raw_input()
arrivee = outils_math.point.Point(x,y)
"""

"""  
import robot
import asservissement
robotInstance=robot.Robot()
asser = Asservissement(robotInstance)
asser.test()
"""
asser = __builtin__.instance.asserInstance
"""
while 42:
    reponse = asser.capteurInstance.mesurer()
    print reponse
    """
depart = outils_math.point.Point(0.0,400.0)



#écriture du point de départ initial
asser.serialInstance.write("cx\n" + str(float(depart.x)) + "\ncy\n"+str(float(depart.y)))

robotInstance.setPosition(depart)



#angle = 0.0
#angle = (float(angle)*3.14)/180
#asser.calculRayon(angle)
    
#scriptInstance = script.Script(asser)
#scriptInstance.huit()

while(True):
    print depart.x
    print depart.y
    print '-----------------------'
    asser.serialInstance.write('\ney\n')
    print asser.serialInstance.readline()
    time.sleep(0.1)
    asser.serialInstance.write('\nex\n')
    print asser.serialInstance.readline()
    
    x, y = '', ''
    while x=='':
        x = raw_input("x arrivé ?")
    while y=='':
        y = raw_input("y arrivé ?")
    arrivee = outils_math.point.Point(int(x),int(y))
    #print asser.capteursInstance.mesure()

    depart = asser.goTo(depart,arrivee)
    