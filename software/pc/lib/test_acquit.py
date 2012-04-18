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
from outils_math.point import Point


asserInstance = __builtin__.instance.asserInstance
actionInstance = __builtin__.instance.actionInstance

a = Point(200.0,200.0)
b = Point(300.0,500.0) 

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
    print "### bienvenue dans la console $0p@l1z7 ###"
    print "exit ou ? pour sortir |     goto avec g     |   orienter avec z,q,s,d "
    print "avancer avec u -> p   | reculer avec j -> m | déplacer bras avec w -> n"
    
    #position initiale du robot
    asserInstance.setPosition(Point(0,400))
    
    while True:
        try:
            ordre = raw_input(">>")
            if ordre == "?" or ordre == "exit" :
                break
            elif ordre == "g":
                x = raw_input("x ?")
                y = raw_input("y ?")
                dest = Point(float(x),float(y)) 
                asserInstance.goTo(dest)
            elif ordre == "q":
                asserInstance.gestionTourner(3.14)
            elif ordre == "s":
                asserInstance.gestionTourner(-1.57)
            elif ordre == "d":
                asserInstance.gestionTourner(0)
            elif ordre == "z":
                asserInstance.gestionTourner(1.57)
                
            elif ordre == "u":
                asserInstance.gestionAvancer(100)
            elif ordre == "j":
                asserInstance.gestionAvancer(-100)
                
            elif ordre == "i":
                asserInstance.gestionAvancer(200)
            elif ordre == "k":
                asserInstance.gestionAvancer(-200)
                
            elif ordre == "o":
                asserInstance.gestionAvancer(300)
            elif ordre == "l":
                asserInstance.gestionAvancer(-300)
                
            elif ordre == "p":
                asserInstance.gestionAvancer(400)
            elif ordre == "m":
                asserInstance.gestionAvancer(-400)
                
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
asserInstance.gestionAvancer(100)
asserInstance.gestionAvancer(300)
raw_input("?")
asserInstance.gestionTourner(1.57)
raw_input("?")
asserInstance.gestionAvancer(400)
asserInstance.gestionTourner(0.0)
raw_input("?")
asserInstance.gestionTourner(math.pi)
raw_input("?")
asserInstance.gestionTourner(-1.57)
asserInstance.gestionAvancer(400)
raw_input("?")
asserInstance.gestionAvancer(200)
asserInstance.gestionAvancer(-200)
asserInstance.gestionAvancer(-200)
asserInstance.gestionAvancer(200)
raw_input("?")
asserInstance.gestionTourner(math.pi)
asserInstance.gestionTourner(0)
asserInstance.gestionTourner(1.57)
asserInstance.gestionTourner(0)
raw_input("?")
"""