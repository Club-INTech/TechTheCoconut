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


asserInstance = __builtin__.instance.asserInstance
strategieInstance = __builtin__.instance.strategieInstance
actionInstance = __builtin__.instance.actionInstance

a = outils_math.point.Point(200.0,200.0)
b = outils_math.point.Point(300.0,500.0) 

"""
while True:
    a.x = float(raw_input("x ?"))
    a.y = float(raw_input("y ?"))
    asserInstance.goToSegment(a)
"""
    

"""
raw_input("?")
asserInstance.avancer(100)
raw_input("?")
asserInstance.goToSegment(a)
raw_input("?")
asserInstance.goToSegment(b)
raw_input("?")
"""

def console():
    while True:
        try:
            ordre = raw_input("?")
            if ordre == "?":
                break
            elif ordre == "q":
                strategieInstance.gestionTourner(3.14)
            elif ordre == "s":
                strategieInstance.gestionTourner(-1.57)
            elif ordre == "d":
                strategieInstance.gestionTourner(0)
            elif ordre == "z":
                strategieInstance.gestionTourner(1.57)
                
            elif ordre == "u":
                strategieInstance.gestionAvancer(100)
            elif ordre == "j":
                strategieInstance.gestionAvancer(-100)
                
            elif ordre == "i":
                strategieInstance.gestionAvancer(200)
            elif ordre == "k":
                strategieInstance.gestionAvancer(-200)
                
            elif ordre == "o":
                strategieInstance.gestionAvancer(300)
            elif ordre == "l":
                strategieInstance.gestionAvancer(-300)
                
            elif ordre == "p":
                strategieInstance.gestionAvancer(400)
            elif ordre == "m":
                strategieInstance.gestionAvancer(-400)
                
            elif ordre == "n":
                actionInstance.deplacer(180)
            elif ordre == "b":
                actionInstance.deplacer(130)
            elif ordre == "v":
                actionInstance.deplacer(120)
            elif ordre == "c":
                actionInstance.deplacer(110)
            elif ordre == "x":
                actionInstance.deplacer(100)
            elif ordre == "w":
                actionInstance.deplacer(0)
            else:
                try:
                    actionInstance.deplacer(int(ordre))
                except:
                    pass
        except:
            print "--- exception levée ---"

console()
        
"""
strategieInstance.gestionAvancer(100)
strategieInstance.gestionAvancer(300)
raw_input("?")
strategieInstance.gestionTourner(1.57)
raw_input("?")
strategieInstance.gestionAvancer(400)
strategieInstance.gestionTourner(0.0)
raw_input("?")
strategieInstance.gestionTourner(math.pi)
raw_input("?")
strategieInstance.gestionTourner(-1.57)
strategieInstance.gestionAvancer(400)
raw_input("?")
strategieInstance.gestionAvancer(200)
strategieInstance.gestionAvancer(-200)
strategieInstance.gestionAvancer(-200)
strategieInstance.gestionAvancer(200)
raw_input("?")
strategieInstance.gestionTourner(math.pi)
strategieInstance.gestionTourner(0)
strategieInstance.gestionTourner(1.57)
strategieInstance.gestionTourner(0)
raw_input("?")
"""