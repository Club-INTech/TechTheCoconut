# -*- coding: utf-8 -*-

import __builtin__
import instance
from outils_math.point import Point


asser = __builtin__.instance.asserInstance
sc = __builtin__.instance.scriptInstance

sc.gestionScripts(sc.recalage)

while True:
    com= raw_input("g , s ,p ?")
    if com == "g":
        xa = raw_input("x arrivée? ")
        ya = raw_input("y arrivée? ")
        asser.goTo(Point(float(xa),float(ya)))
    elif com == "s":
        xa = raw_input("x arrivée? ")
        ya = raw_input("y arrivée? ")
        asser.goToSegment(Point(float(xa),float(ya)))
    elif com == "q":
        break
    elif com == "p":
        print "pos : "+str(asser.getPosition())+", orient : "+str(asser.getOrientation())
    
    elif com == "d":
        asser.gestionAvancer(200)
    elif com == "f":
        asser.gestionAvancer(-200)
        
    elif com == "t":
        asser.gestionTourner(1.57)
    elif com == "y":
        asser.gestionTourner(3.1415)
    if com == "pos":
        xa = raw_input("x courant? ")
        ya = raw_input("y courant? ")
        asser.setPosition(Point(xa,ya))
    if com == "carre":
        while True:
            asser.goToSegment(Point(float(-500),float(-500)))
            asser.goToSegment(Point(float(500),float(-500)))
            asser.goToSegment(Point(float(500),float(0)))
            asser.goToSegment(Point(float(0),float(0)))
            
            