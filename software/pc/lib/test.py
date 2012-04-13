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
import math

"""
x = raw_input("Donner les coordonnées en x puis y du point de départ\n")
y = raw_input()
depart = outils_math.point.Point(x,y)

x = raw_input("Donner les coordonnées en x puis y du point de arrivee\n")
y = raw_input()
arrivee = outils_math.point.Point(x,y)
"""
"""
capteurInstance = __builtin__.instance.capteurInstance
while 42:
    print capteurInstance.mesurer()
    time.sleep(0.1)
"""
    

"""  
import robot
import asservissement
robotInstance=robot.Robot()
asser = Asservissement(robotInstance)
asser.test()
"""
scriptInstance = __builtin__.instance.scriptInstance

depart = outils_math.point.Point(0.0,0.0)
asser = __builtin__.instance.asserInstance
#écriture du point de départ initial

asser.serialInstance.write("\n")

asser.serialInstance.write("cx\n" + str(float(depart.x)) + "\ncy\n"+str(float(depart.y)))
#robotInstance.setPosition
#scriptInstance.homologation()
asser.avancer(500)
asser.avancer(-500)
"""
asser.avancer(500)
asser.avancer(-500)
asser.avancer(500)
asser.avancer(-500)
asser.avancer(500)
asser.avancer(-500)
asser.avancer(500)
asser.avancer(-500)
"""
"""
asser.avancer(800)
asser.tourner(0)
asser.avancer(800)
asser.tourner(math.pi)
asser.avancer(800)
asser.tourner(0)
asser.avancer(800)
asser.tourner(math.pi)
asser.avancer(800)
asser.tourner(0)
asser.avancer(800)
asser.tourner(math.pi)
asser.avancer(800)
asser.tourner(0)
asser.avancer(800)
asser.tourner(math.pi)
"""
"""
asser.avancer(300)
#time.sleep(0.5)
asser.tourner(1.5)
#time.sleep(0.5)
asser.avancer(500)
#time.sleep(0.5)
asser.tourner(0)
#time.sleep(0.5)
asser.avancer(300)
#time.sleep(0.5)
asser.avancer(-300)
#time.sleep(0.5)
asser.tourner(1.5)
#time.sleep(0.5)
asser.avancer(600)
#time.sleep(0.5)
asser.tourner(-1.5)
#time.sleep(0.5)
asser.avancer(-480)
#time.sleep(0.5)
asser.avancer(1500)
asser.tourner(math.pi)
asser.avancer(-300)
"""
"""
asser.serialInstance.write('\n')
asser.serialInstance.write('d\n' + str(float(-200))+'\n')
acquitement = False
while not acquitement:
    asser.serialInstance.write('acq\n')
    reponse = str(asser.serialInstance.readline()).replace("\n","").replace("\r","").replace("\0", "")
    print 'reponse :'
    print reponse
    if reponse == "FIN_MVT":
        acquitement = True
print 'FINI'
"""
#angle = 0.0
#angle = (float(angle)*3.14)/180
#asser.calculRayon(angle)
    
#scriptInstance = script.Script(asser)
#scriptInstance.huit()
while(True):
    x, y = '', ''
    while x=='':
        x = raw_input("x arrivé ?")
    while y=='':
        y = raw_input("y arrivé ?")
    arrivee = outils_math.point.Point(int(x),int(y))
    asser.goTo(depart, arrivee)
    asser.serialInstance.write("pos\n")
    depart = (asser.serialInstance.readline()).replace("\n","").replace("\r","").replace("\0", "")
    if depart[4]== "+":
        depart = depart.split("+")
    else:
        depart = depart.split("-")
    depart = outils_math.point.Point(depart[0],depart[1])
    