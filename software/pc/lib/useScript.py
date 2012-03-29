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

asser = __builtin__.instance.asserInstance
robotInstance = __builtin__.instance.robotInstance
scriptInstance = __builtin__.instance.scriptInstance

scriptInstance.recalage()

#scriptInstance = script.Script(asser)
#scriptInstance.huit()


#depart = outils_math.point.Point(0.0,400.0)
##écriture du point de départ initial
#asser.serialInstance.write("cx\n" + str(float(depart.x)) + "\ncy\n"+str(float(depart.y)))
#robotInstance.setPosition(depart)
#while(True):    
    #x, y = '', ''
    #while x=='':
        #x = raw_input("x arrivé ?")
    #while y=='':
        #y = raw_input("y arrivé ?")
    #arrivee = outils_math.point.Point(int(x),int(y))
    ##print asser.capteursInstance.mesure()

    #asser.goTo(depart,arrivee)
    
    #depart.x = robotInstance.position.x
    #depart.y = robotInstance.position.y