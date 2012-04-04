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
import threading



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
robotInstance = __builtin__.instance.robotInstance
capteurInstance = __builtin__.instance.capteurInstance
#__builtin__.instance.serieCaptInstance = serial.Serial("/dev/ttyUSB10" 57600, timeout=1)
"""
while 42:
    reponse = asser.capteurInstance.mesurer()
    print reponse
    """

#écriture du point de départ initial
"""
asser.avancer(300)
asser.tourner(-1.5)
asser.avancer(500)
asser.tourner(3.2)
asser.avancer(300)
asser.avancer(-300)
asser.tourner(-1.5)
asser.avancer(600)
asser.tourner(1.5)
"""
"""
while 42:
    __builtin__.instance.serieCaptInstance.write('ultrason\n')
    capteurInstance.mesurer()
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
    #print asser.capteursInstance.mesure()

    asser.goTo(arrivee)
    

"""
testThread= threading.Thread(target = asser.test)
testThread.start()
mutex = Lock()

while 42:
    mutex.acquire()
    time.sleep(0.1)
    print asser.var
    mutex.release()
"""