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
raw_input()
print "position : ("+str(asser.robotInstance.position.x)+", "+str(asser.robotInstance.position.y)+")\n"
asser.serialInstance.write('cr1\n')
asser.serialInstance.write('ct1\n')
#raw_input()
asser.tourner(3.1415)
asser.avancer(600)
raw_input()
asser.tourner(1.57)
raw_input()
asser.goTo(outils_math.point.Point(100,1500))
raw_input()
asser.goTo(outils_math.point.Point(800,250))
raw_input()
asser.tourner(3.1415)
raw_input()
asser.avancer(-400)
raw_input()
print "position : ("+str(asser.robotInstance.position.x)+", "+str(asser.robotInstance.position.y)+")\n"
asser.serialInstance.write('cr0\n')
asser.serialInstance.write('ct0\n')
raw_input()
print "position : ("+str(asser.robotInstance.position.x)+", "+str(asser.robotInstance.position.y)+")\n"
raw_input()
print "position : ("+str(asser.robotInstance.position.x)+", "+str(asser.robotInstance.position.y)+")\n"
raw_input()
print "position : ("+str(asser.robotInstance.position.x)+", "+str(asser.robotInstance.position.y)+")\n"
raw_input()
print "position : ("+str(asser.robotInstance.position.x)+", "+str(asser.robotInstance.position.y)+")\n"
raw_input()
print "position : ("+str(asser.robotInstance.position.x)+", "+str(asser.robotInstance.position.y)+")\n"
raw_input()
print "position : ("+str(asser.robotInstance.position.x)+", "+str(asser.robotInstance.position.y)+")\n"
raw_input()
print "position : ("+str(asser.robotInstance.position.x)+", "+str(asser.robotInstance.position.y)+")\n"

#asser.serialInstance.write("cy\n400.0\n")