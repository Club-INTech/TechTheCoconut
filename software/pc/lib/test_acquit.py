# -*- coding: utf-8 -*-

import asservissement
import outils_math
import robot
import script
import time
import serial
import instance
import __builtin__
import math
from outils_math.point import Point
import lib.log
log =lib.log.Log(__name__)

if hasattr(__builtin__.instance, 'asserInstance'):
    asserInstance = __builtin__.instance.asserInstance
    asser = asserInstance
else:
    log.logger.error("console $0p@l1z7 : ne peut importer instance.asserInstance")
if hasattr(__builtin__.instance, 'actionInstance'):
    actionInstance = __builtin__.instance.actionInstance
    action = actionInstance
    
else:
    log.logger.error("console $0p@l1z7 : ne peut importer instance.actionInstance")

    
def torine00():
    #totem 00
    asserInstance.goTo(Point(-70.0, 470.0))
    asserInstance.gestionTourner(0,instruction = "finir")
    actionInstance.deplacer(130)
    time.sleep(0.3)
    asserInstance.gestionAvancer(400,instruction = "finir")
    asserInstance.gestionAvancer(300,instruction = "finir")
    asserInstance.gestionTourner(0.74,instruction = "auStopNeRienFaire")
    asserInstance.gestionAvancer(400,instruction = "auStopNeRienFaire")
    asserInstance.gestionTourner(0,instruction = "auStopNeRienFaire")
    asserInstance.gestionAvancer(200,instruction = "auStopNeRienFaire")
    actionInstance.deplacer(130)
    time.sleep(0.3)
    actionInstance.deplacer(180)
    time.sleep(0.3)
    asserInstance.gestionAvancer(-350,instruction = "auStopNeRienFaire")
    actionInstance.deplacer(0)
    time.sleep(0.3)
    asserInstance.gestionTourner(1.57,instruction = "auStopNeRienFaire")
    #poussoir0
    asserInstance.gestionAvancer(500,instruction = "auStopNeRienFaire")
    asserInstance.gestionTourner(-1.57,instruction = "auStopNeRienFaire")
    asserInstance.gestionAvancer(-300,instruction = "auStopNeRienFaire")
    asserInstance.gestionAvancer(-200,instruction = "auStopNeRienFaire")
    asserInstance.gestionAvancer(200,instruction = "auStopNeRienFaire")
    
def torine01():
    #totem01
    asserInstance.goTo(Point(-50.0, 1200.0))
    asserInstance.gestionTourner(0,instruction = "finir")
    actionInstance.deplacer(140)
    time.sleep(0.3)
    asserInstance.gestionAvancer(300,instruction = "finir")
    asserInstance.gestionTourner(0,instruction = "auStopNeRienFaire")
    asserInstance.gestionAvancer(400,instruction = "finir")
    asserInstance.gestionTourner(-0.74,instruction = "auStopNeRienFaire")
    asserInstance.gestionAvancer(300,instruction = "auStopNeRienFaire")
    asserInstance.gestionTourner(0,instruction = "auStopNeRienFaire")
    asserInstance.gestionAvancer(300,instruction = "auStopNeRienFaire")
    actionInstance.deplacer(180)
    time.sleep(0.3)
    asserInstance.gestionAvancer(-300,instruction = "auStopNeRienFaire")
    actionInstance.deplacer(0)
    time.sleep(0.3)
    #rentrer dans la cale
    asserInstance.gestionTourner(1.57,instruction = "auStopNeRienFaire")
    asserInstance.gestionAvancer(-600,instruction = "auStopNeRienFaire")
    asserInstance.gestionTourner(3.14,instruction = "auStopNeRienFaire")
    asserInstance.gestionAvancer(-400,instruction = "auStopNeRienFaire")
    
    
def console():
    print "            ~~###~~ bienvenue dans la console $0p@1!z7 ~~###~~"
    print "exit ou ? pour sortir |  a : lancer script   | e : enregistrer derniere action  "
    print "avancer avec u -> p   | reculer avec j -> m  | ; : ! vitesses translation"
    print "             orienter avec z,q,s,d | r,t,y : vitesses rotation  "
    print "  g : goto position | déplacer bras avec w -> n | ² : position courante "             
    
    #position initiale du robot
    #asserInstance.setPosition(Point(70,400))
    #asserInstance.setOrientation(0)
    
    #enregistrement du script
    macro = ""
    
    while True:
        try:
            ordre = raw_input(">>")
            if ordre == "?" or ordre == "exit" :
                print "script enregistré : \n\n"+macro+"\n"
                break
            elif ordre == "g":
                x = raw_input("x ?")
                y = raw_input("y ?")
                dest = Point(float(x),float(y)) 
                asserInstance.goTo(dest)
                current = "asserInstance.goTo(Point("+str(float(dest.x))+", "+str(float(dest.y))+"))\n"
            elif ordre == "q":
                asserInstance.gestionTourner(3.14,instruction = "auStopNeRienFaire")
                current = "asserInstance.gestionTourner(3.14,instruction = \"auStopNeRienFaire\")\n"
            elif ordre == "s":
                asserInstance.gestionTourner(-1.57,instruction = "auStopNeRienFaire")
                current = "asserInstance.gestionTourner(-1.57,instruction = \"auStopNeRienFaire\")\n"
            elif ordre == "d":
                asserInstance.gestionTourner(0,instruction = "auStopNeRienFaire")
                current = "asserInstance.gestionTourner(0,instruction = \"auStopNeRienFaire\")\n"
            elif ordre == "z":
                asserInstance.gestionTourner(1.57,instruction = "auStopNeRienFaire")
                current = "asserInstance.gestionTourner(1.57,instruction = \"auStopNeRienFaire\")\n"
                
            elif ordre == "u":
                asserInstance.gestionAvancer(100,instruction = "auStopNeRienFaire")
                current = "asserInstance.gestionAvancer(100,instruction = \"auStopNeRienFaire\")\n"
            elif ordre == "j":
                asserInstance.gestionAvancer(-100,instruction = "auStopNeRienFaire")
                current = "asserInstance.gestionAvancer(-100,instruction = \"auStopNeRienFaire\")\n"
            elif ordre == "i":
                asserInstance.gestionAvancer(200,instruction = "auStopNeRienFaire")
                current = "asserInstance.gestionAvancer(200,instruction = \"auStopNeRienFaire\")\n"
            elif ordre == "k":
                asserInstance.gestionAvancer(-200,instruction = "auStopNeRienFaire")
                current = "asserInstance.gestionAvancer(-200,instruction = \"auStopNeRienFaire\")\n"
            elif ordre == "o":
                asserInstance.gestionAvancer(300,instruction = "auStopNeRienFaire")
                current = "asserInstance.gestionAvancer(300,instruction = \"auStopNeRienFaire\")\n"
            elif ordre == "l":
                asserInstance.gestionAvancer(-300,instruction = "auStopNeRienFaire")
                current = "asserInstance.gestionAvancer(-300,instruction = \"auStopNeRienFaire\")\n"
            elif ordre == "p":
                asserInstance.gestionAvancer(400,instruction = "auStopNeRienFaire")
                current = "asserInstance.gestionAvancer(400,instruction = \"auStopNeRienFaire\")\n"
            elif ordre == "m":
                asserInstance.gestionAvancer(-400,instruction = "auStopNeRienFaire")
                current = "asserInstance.gestionAvancer(-400,instruction = \"auStopNeRienFaire\")\n"
                
            elif ordre == "n":
                actionInstance.deplacer(180)
                current = "actionInstance.deplacer(180)\n"
            elif ordre == "b":
                actionInstance.deplacer(130)
                current = "actionInstance.deplacer(130)\n"
            elif ordre == "v":
                actionInstance.deplacer(120)
                current = "actionInstance.deplacer(120)\n"
            elif ordre == "c":
                actionInstance.deplacer(110)
                current = "actionInstance.deplacer(110)\n"
            elif ordre == "x":
                actionInstance.deplacer(100)
                current = "actionInstance.deplacer(100)\n"
            elif ordre == "w":
                actionInstance.deplacer(0)
                current = "actionInstance.deplacer(0)\n"
                
            #vitesses rotation
            elif ordre == "r":
                asserInstance.changerVitesse("rotation", 1)
                current = "asserInstance.changerVitesse(\"rotation\", 1)\n"
            elif ordre == "t":
                asserInstance.changerVitesse("rotation", 2)
                current = "asserInstance.changerVitesse(\"rotation\", 2)\n"
            elif ordre == "y":
                asserInstance.changerVitesse("rotation", 3)
                current = "asserInstance.changerVitesse(\"rotation\", 3)\n"
                
            #vitesses translation
            elif ordre == ";":
                asserInstance.changerVitesse("translation", 1)
                current = "asserInstance.changerVitesse(\"translation\", 1)\n"
            elif ordre == ":":
                asserInstance.changerVitesse("translation", 2)
                current = "asserInstance.changerVitesse(\"translation\", 2)\n"
            elif ordre == "!":
                asserInstance.changerVitesse("translation", 3)
                current = "asserInstance.changerVitesse(\"translation\", 3)\n"
                
            elif ordre == "a":
                torine00()
            elif ordre == "h":
                torine01()
                
            elif ordre == "f":
                asserInstance.recalage()
            
            elif ordre == "e":
                macro += current
                current = ""
                
            elif ordre == "sop" :
                scriptPoussoir0()
            elif ordre == "sop1": 
                faireChier()
            elif ordre == "sop2":
                farmerTotemEnnemiSud()
            elif ordre == "²":
                print "pos : "+str(asserInstance.getPosition())+", orient : "+str(asserInstance.getOrientation())
                
            else:
                try:
                    actionInstance.deplacer(int(ordre))
                    current = "actionInstance.deplacer("+str(int(ordre))+")\n"
                except:
                    pass
                
        except:
            print "--- exception levée ---"

console()