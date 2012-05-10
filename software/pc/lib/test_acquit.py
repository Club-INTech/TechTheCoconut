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

if hasattr(__builtin__.instance, 'asserInstance'):
    asserInstance = __builtin__.instance.asserInstance
if hasattr(__builtin__.instance, 'actionInstance'):
    actionInstance = __builtin__.instance.actionInstance

def scriptTotem():
    asserInstance.goTo(Point(0.,660.))
    asserInstance.gestionTourner(0)
    actionInstance.deplacer(130)
    time.sleep(0.5)
    asserInstance.gestionAvancer(200,instruction = "auStopNeRienFaire")
    actionInstance.deplacer(120)
    time.sleep(0.5)
    asserInstance.gestionTourner(0,instruction = "auStopNeRienFaire")
    asserInstance.gestionAvancer(200,instruction = "auStopNeRienFaire")
    actionInstance.deplacer(110)
    time.sleep(0.5)
    actionInstance.deplacer(120)
    time.sleep(0.5)
    asserInstance.gestionTourner(0,instruction = "auStopNeRienFaire")
    asserInstance.gestionAvancer(200,instruction = "auStopNeRienFaire")
    asserInstance.gestionAvancer(600,instruction = "auStopNeRienFaire")
    actionInstance.deplacer(80)
    time.sleep(0.5)
    asserInstance.gestionAvancer(-300,instruction = "auStopNeRienFaire")
    asserInstance.gestionTourner(math.pi/2)
    actionInstance.deplacer(100)
    time.sleep(0.5)
    
    asserInstance.gestionAvancer(100,instruction = "auStopNeRienFaire")
    asserInstance.gestionTourner(0)
    asserInstance.gestionAvancer(100,instruction = "auStopNeRienFaire")
    asserInstance.gestionAvancer(-100,instruction = "auStopNeRienFaire")
    actionInstance.deplacer(130)
    time.sleep(0.5)
    asserInstance.gestionAvancer(500,instruction = "auStopNeRienFaire")
    asserInstance.gestionAvancer(-300)
    actionInstance.deplacer(0)
    time.sleep(0.5)
    asserInstance.gestionTourner(math.pi/2)
    asserInstance.gestionAvancer(100,instruction = "auStopNeRienFaire")
    actionInstance.deplacer(130)
    time.sleep(0.5)
    asserInstance.gestionAvancer(100,instruction = "auStopNeRienFaire")
    asserInstance.gestionTourner(0)
    actionInstance.deplacer(0)
    time.sleep(0.5)
    asserInstance.gestionTourner(math.pi/2)
    asserInstance.goTo(Point(850.,1600.))
    asserInstance.changerVitesse("translation", 3)
    asserInstance.gestionAvancer(-400,instruction = "auStopNeRienFaire")
    asserInstance.changerVitesse("translation", 2)
    asserInstance.gestionAvancer(500,instruction = "auStopNeRienFaire")
    
    
    #asserInstance.gestionAvancer(-50,instruction = "auStopNeRienFaire")
    #asserInstance.gestionAvancer(300,instruction = "auStopNeRienFaire")
    #actionInstance.deplacer(80)
    #time.sleep(0.5)
    
    #asserInstance.gestionAvancer(-400,instruction = "auStopNeRienFaire")
    #actionInstance.deplacer(0)
    #time.sleep(0.5)
    
    
    
    
    
def console():
    print "            ~~###~~ bienvenue dans la console $0p@l1z7 ~~###~~"
    print "exit ou ? pour sortir |         goto avec g         |   orienter avec z,q,s,d "
    print "avancer avec u -> p   |     reculer avec j -> m     | déplacer bras avec w -> n"
    print "   a : farmer totem   |  r,t,y : vitesses rotation  | ; : ! vitesses translation"
    
    #position initiale du robot
    asserInstance.setPosition(Point(70,400))
    asserInstance.setOrientation(0)
    
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
                asserInstance.gestionTourner(3.14,instruction = "auStopNeRienFaire")
            elif ordre == "s":
                asserInstance.gestionTourner(-1.57,instruction = "auStopNeRienFaire")
            elif ordre == "d":
                asserInstance.gestionTourner(0,instruction = "auStopNeRienFaire")
            elif ordre == "z":
                asserInstance.gestionTourner(1.57,instruction = "auStopNeRienFaire")
                
            elif ordre == "u":
                asserInstance.gestionAvancer(100,instruction = "auStopNeRienFaire")
            elif ordre == "j":
                asserInstance.gestionAvancer(-100,instruction = "auStopNeRienFaire")
                
            elif ordre == "i":
                asserInstance.gestionAvancer(200,instruction = "auStopNeRienFaire")
            elif ordre == "k":
                asserInstance.gestionAvancer(-200,instruction = "auStopNeRienFaire")
                
            elif ordre == "o":
                asserInstance.gestionAvancer(300,instruction = "auStopNeRienFaire")
            elif ordre == "l":
                asserInstance.gestionAvancer(-300,instruction = "auStopNeRienFaire")
                
            elif ordre == "p":
                asserInstance.gestionAvancer(400,instruction = "auStopNeRienFaire")
            elif ordre == "m":
                asserInstance.gestionAvancer(-400,instruction = "auStopNeRienFaire")
                
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
                
            #vitesses rotation
            elif ordre == "r":
                asserInstance.changerVitesse("rotation", 1)
            elif ordre == "t":
                asserInstance.changerVitesse("rotation", 2)
            elif ordre == "y":
                asserInstance.changerVitesse("rotation", 3)
                
            #vitesses translation
            elif ordre == ";":
                asserInstance.changerVitesse("translation", 1)
            elif ordre == ":":
                asserInstance.changerVitesse("translation", 2)
            elif ordre == "!":
                asserInstance.changerVitesse("translation", 3)
                
            elif ordre == "a":
                scriptTotem()
                
            else:
                try:
                    actionInstance.deplacer(int(ordre))
                except:
                    pass
        except:
            print "--- exception levée ---"

console()