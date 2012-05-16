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

def scriptTotem():
    asserInstance.goTo(Point(0.,660.))
    #début notre totem sud
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
    
    #mettre dans la cale
    asserInstance.gestionAvancer(100,instruction = "auStopNeRienFaire")
    asserInstance.gestionTourner(math.pi/4,instruction = "auStopNeRienFaire")
    asserInstance.gestionAvancer(320,instruction = "auStopNeRienFaire")
    asserInstance.gestionTourner(0,instruction = "auStopNeRienFaire")
    asserInstance.gestionAvancer(280,instruction = "auStopNeRienFaire")
    asserInstance.gestionAvancer(-50,instruction = "auStopNeRienFaire")
    actionInstance.deplacer(130)
    time.sleep(0.2)
    actionInstance.deplacer(110)
    time.sleep(0.2)
    actionInstance.deplacer(130)
    asserInstance.changerVitesse("translation", 3)
    asserInstance.gestionAvancer(-50,instruction = "auStopNeRienFaire")
    asserInstance.changerVitesse("translation", 2)
    asserInstance.gestionAvancer(-300,instruction = "auStopNeRienFaire")
    actionInstance.deplacer(0)
    #asserInstance.gestionTourner(math.pi/2,instruction = "auStopNeRienFaire")
    
    
def scriptTotemNordV0():
    #asserInstance.goTo(Point(820,1350.))
    #asserInstance.gestionTourner(math.pi)
    #actionInstance.deplacer(110)
    #time.sleep(0.5)
    #asserInstance.gestionAvancer(700)
    #actionInstance.deplacer(60)
    #time.sleep(0.5)
    
    #début notre totem sud
    asserInstance.gestionTourner(0)
    actionInstance.deplacer(130)
    time.sleep(0.5)
    asserInstance.gestionAvancer(250,instruction = "auStopNeRienFaire")
    actionInstance.deplacer(120)
    time.sleep(0.5)
    asserInstance.gestionTourner(0,instruction = "auStopNeRienFaire")
    asserInstance.gestionAvancer(200,instruction = "auStopNeRienFaire")
    actionInstance.deplacer(110)
    time.sleep(0.5)
    actionInstance.deplacer(150)
    time.sleep(0.5)
    asserInstance.gestionTourner(0,instruction = "auStopNeRienFaire")
    asserInstance.gestionAvancer(200,instruction = "auStopNeRienFaire")
    
    #mettre dans la cale
    asserInstance.gestionAvancer(100,instruction = "auStopNeRienFaire")
    asserInstance.gestionTourner(-math.pi/4,instruction = "auStopNeRienFaire")
    asserInstance.gestionAvancer(330,instruction = "auStopNeRienFaire")
    asserInstance.gestionTourner(0,instruction = "auStopNeRienFaire")
    asserInstance.gestionAvancer(320,instruction = "auStopNeRienFaire")
    asserInstance.gestionAvancer(-50,instruction = "auStopNeRienFaire")
    actionInstance.deplacer(140)
    time.sleep(0.2)
    actionInstance.deplacer(110)
    time.sleep(0.2)
    actionInstance.deplacer(130)
    asserInstance.changerVitesse("translation", 3)
    asserInstance.gestionAvancer(-50,instruction = "auStopNeRienFaire")
    asserInstance.changerVitesse("translation", 2)
    asserInstance.gestionAvancer(-230,instruction = "auStopNeRienFaire")
    actionInstance.deplacer(0)
    
def scriptTotemNord():
    #début notre totem nord
    asserInstance.gestionTourner(0)
    actionInstance.deplacer(130)
    time.sleep(0.5)
    asserInstance.gestionAvancer(250,instruction = "auStopNeRienFaire")
    actionInstance.deplacer(120)
    time.sleep(0.5)
    asserInstance.gestionTourner(0,instruction = "auStopNeRienFaire")
    asserInstance.gestionAvancer(200,instruction = "auStopNeRienFaire")
    actionInstance.deplacer(110)
    time.sleep(0.5)
    actionInstance.deplacer(150)
    time.sleep(0.5)
    asserInstance.gestionTourner(0,instruction = "auStopNeRienFaire")
    asserInstance.gestionAvancer(350,instruction = "auStopNeRienFaire")
    
    # Rotation : vers le bas :
    actionInstance.deplacer(130)
    time.sleep(0.5)
    asserInstance.gestionTourner(-math.pi/3, instruction="auStopNeRienFaire")
    asserInstance.gestionAvancer(340, instruction="auStopNeRienFaire")
    asserInstance.gestionTourner(0, instruction="auStopNeRienFaire")
    asserInstance.gestionAvancer(250)
    actionInstance.deplacer(160)
    asserInstance.gestionAvancer(-50)
    actionInstance.deplacer(130)
    asserInstance.gestionAvancer(-50)
    actionInstance.deplacer(150)
    asserInstance.gestionAvancer(-50)
    actionInstance.deplacer(110)
    asserInstance.gestionAvancer(-150)
    
    # On récupère
    #actionInstance.deplacer(0, "bd")
    #asserInstance.gestionTourner(-math.pi/2)
    #asserInstance.gestionTourner(-math.pi)
    #actionInstance.deplacer(150)
    #time.sleep(0.5)
    #asserInstance.gestionAvancer(100)
    #actionInstance.deplacer(40)
    #asserInstance.gestionTourner(0)
    #actionInstance.deplacer(130)
    #asserInstance.gestionAvancer(300)
    #asserInstance.gestionAvancer(-200)
    
    # VERSION 2
    actionInstance.deplacer(0, ["bd", "hd"])
    time.sleep(0.2)
    asserInstance.gestionTourner(-math.pi/2)
    asserInstance.gestionTourner(-math.pi)
    asserInstance.gestionAvancer(70)
    actionInstance.deplacer(70, ["hg", "bg"])
    asserInstance.gestionTourner(math.pi/2)
    actionInstance.deplacer(50, ["hg", "bg"])
    asserInstance.gestionTourner(0)
    actionInstance.deplacer(130)
    time.sleep(0.2)
    asserInstance.gestionAvancer(300)
    asserInstance.gestionAvancer(-200)
    
    
    #mettre dans la cale
    #asserInstance.gestionAvancer(100,instruction = "auStopNeRienFaire")
    #asserInstance.gestionTourner(-math.pi/4,instruction = "auStopNeRienFaire")
    #asserInstance.gestionAvancer(330,instruction = "auStopNeRienFaire")
    #asserInstance.gestionTourner(0,instruction = "auStopNeRienFaire")
    #asserInstance.gestionAvancer(320,instruction = "auStopNeRienFaire")
    #asserInstance.gestionAvancer(-50,instruction = "auStopNeRienFaire")
    #actionInstance.deplacer(140)
    #time.sleep(0.2)
    #actionInstance.deplacer(110)
    #time.sleep(0.2)
    #actionInstance.deplacer(130)
    #asserInstance.changerVitesse("translation", 3)
    #asserInstance.gestionAvancer(-50,instruction = "auStopNeRienFaire")
    #asserInstance.changerVitesse("translation", 2)
    #asserInstance.gestionAvancer(-230,instruction = "auStopNeRienFaire")
    #actionInstance.deplacer(0)
   
def scriptTotemEnnemiSud() :
    asserInstance.goTo(Point(-730, 660))
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
    asserInstance.goTo(Point(0, 500))
    asserInstance.gestionTourner(0.102)
    asserInstance.gestionAvancer(683.0)
    asserInstance.gestionTourner(0.845)
    asserInstance.gestionAvancer(447.0)

def scriptPoussoir0() :
    asserInstance.gestionTourner(math.pi/2)
    actionInstance.deplacer(150, "bd")
    asserInstance.attendre(0.5)
    asserInstance.gestionAvancer(220)
    asserInstance.gestionTourner(-math.pi)
    asserInstance.gestionTourner(-math.pi/2)
    
    asserInstance.gestionAvancer(-3000, "auStopNeRienFaire")
    asserInstance.gestionTourner(-math.pi/2)
    asserInstance.gestionAvancer(400)
    asserInstance.gestionAvancer(-100)
    actionInstance.deplacer(0)

    
def faireChier():
    asserInstance.gestionTourner(-math.pi)
    actionInstance.deplacer(150, "bd")
    asserInstance.attendre(0.5)
    asserInstance.gestionAvancer(220)
    asserInstance.gestionTourner(-math.pi/2)
    asserInstance.gestionTourner(0)
    actionInstance.deplacer(0)
    asserInstance.gestionAvancer(-3000, "auStopNeRienFaire")
    asserInstance.gestionAvancer(130)
    asserInstance.gestionTourner(-math.pi/2-0.02)
    asserInstance.attendre(.5)
    asserInstance.gestionAvancer(500)
    
    """
    asserInstance.gestionTourner(-3*math.pi/4)
    asserInstance.gestionAvancer(250)
    actionInstance.deplacer(150, "bg")
    asserInstance.attendre(0.5)
    asserInstance.gestionTourner(-math.pi/4)
    asserInstance.gestionAvancer(350)
    """
    
    asserInstance.gestionAvancer(150)
    asserInstance.gestionTourner(-math.pi)
    asserInstance.gestionAvancer(250)
    actionInstance.deplacer(160)
    asserInstance.attendre(0.2)
    asserInstance.changerVitesse("rotation", 3)
    asserInstance.gestionTourner(-math.pi/2)
    asserInstance.gestionTourner(math.pi)
    asserInstance.gestionTourner(math.pi/2)
    asserInstance.gestionTourner(math.pi)
    asserInstance.changerVitesse("rotation", 2)
    asserInstance.gestionAvancer(-300)
    
def farmerTotemEnnemiSud():
    asser.gestionTourner(0)
    action.deplacer(150)
    asser.attendre(0.5)
    asser.gestionAvancer(100)
    action.deplacer(30, "bg")
    asser.attendre(0.3)
    action.deplacer(150, "bg")
    asser.attendre(0.2)
    asser.gestionAvancer(100)
    action.deplacer(130)
    asser.gestionAvancer(100, "auStopNeRienFaire")
    asser.gestionTourner(0, "auStopNeRienFaire")
    action.deplacer(110)
    asser.attendre(0.2)
    action.deplacer(120)
    asser.attendre(0.2)
    asser.gestionTourner(0, "auStopNeRienFaire")
    asser.gestionAvancer(200, "auStopNeRienFaire")
    asser.gestionTourner(0, "auStopNeRienFaire")
    action.deplacer(90)
    asser.attendre(0.3)
    asser.gestionAvancer(200)
    action.deplacer(40, "bg")
    
    #asser.gestionAvancer(120)
    #action.deplacer(140, "hg")
    #action.deplacer(140 ,"bg")
    #asser.gestionTourner(0, "auStopNeRienFaire")
    #asser.gestionAvancer(50, "auStopNeRienFaire")
    #asser.gestionTourner(0, "auStopNeRienFaire")
    #action.deplacer(0, "hd")
    #action.deplacer(120, "bd")
    #action.deplacer(120, ["hg", "bg"])
    #asser.attendre(0.3)
    #asser.gestionTourner(0, "auStopNeRienFaire")
    #asser.gestionAvancer(200, "auStopNeRienFaire")
    #asser.gestionTourner(0, "auStopNeRienFaire")
    #action.deplacer(110, ["hg", "bg"])
    #asser.gestionTourner(0, "auStopNeRienFaire")
    #asser.gestionAvancer(200, "auStopNeRienFaire")
    #asser.gestionTourner(0, "auStopNeRienFaire")
    #asser.gestionTourner(0.5)
    #asser.gestionAvancer(300)
    
    action.deplacer(0, ["hd", "hg"])
    asser.gestionTourner(-1)
    asser.gestionAvancer(300)
    asser.gestionTourner(0)
    asser.gestionAvancer(600)
    asser.gestionTourner(1)
    asser.gestionAvancer(500)
    asser.gestionTourner(0)
    asser.gestionAvancer(400, "auStopNeRienFaire")
    asser.gestionAvancer(-400)
    """
    asserInstance.gestionAvancer(200,instruction = "auStopNeRienFaire")
    asserInstance.gestionTourner(math.pi/4,instruction = "auStopNeRienFaire")
    asserInstance.gestionAvancer(200,instruction = "auStopNeRienFaire")
    asserInstance.gestionTourner(0,instruction = "auStopNeRienFaire")
    asserInstance.gestionAvancer(400,instruction = "auStopNeRienFaire")
    actionInstance.deplacer(80)
    time.sleep(0.5)
    asserInstance.gestionAvancer(-400,instruction = "auStopNeRienFaire")
    actionInstance.deplacer(0)
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
    asserInstance.gestionAvancer(150,instruction = "auStopNeRienFaire")
    asserInstance.gestionAvancer(-150,instruction = "auStopNeRienFaire")
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
    """
    
    
    
def console():
    print "            ~~###~~ bienvenue dans la console $0p@1!z7 ~~###~~"
    print "exit ou ? pour sortir |  a : lancer script   | e : enregistrer derniere action  "
    print "avancer avec u -> p   | reculer avec j -> m  | ; : ! vitesses translation"
    print "             orienter avec z,q,s,d | r,t,y : vitesses rotation  "
    print "  g : goto position | déplacer bras avec w -> n | ² : position courante "             
    
    #position initiale du robot
    asserInstance.setPosition(Point(70,400))
    asserInstance.setOrientation(0)
    
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
                scriptTotem()
            elif ordre == "h":
                scriptTotemNord()
            
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