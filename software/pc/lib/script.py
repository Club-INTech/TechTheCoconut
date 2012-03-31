# -*- coding: utf-8 -*-

import sys
import os
import __builtin__
import math
import time
import asservissement
import outils_math.point
import outils_math.point as point
import instance

sys.path.append('../')

import profils.develop.constantes

class Script:
    
    def __init__(self):
        self.asserInstance = __builtin__.instance.asserInstance
    
    
    def recalage(self):
        """
        Fonction permettant de recaller le robot dans un coin de la table
        """
        
        self.asserInstance.recalage()
        
        
        """
        couleur = profils.develop.constantes.constantes["couleur"]
        self.asser.avancer(-100.0)
        self.asser.setUnsetAsser('rotation', 0)
        self.asser.avancer(-100.0)
        if couleur == 'R':
            self.asser.robotInstance.position.x = 1460
            self.asser.serieInstance.ecrire("c\nx\n" + str(float(1460)))
        else:
            self.asser.robotInstance.position.x = -1460
            self.asser.serieInstance.ecrire("c\nx\n" + str(float(-1460)))
        self.asser.setUnsetAsser('rotation', 1)
        self.asser.avancer(200.0)
        self.asser.tourner(3*math.pi/2)
        self.asser.avancer(-150.0)
        self.asser.setUnsetAsser('rotation', 0)
        self.asser.avancer(-150)
        self.asser.robotInstance.position.y = 60
        self.asser.serieInstance.ecrire("c\ny\n" + str(float(60)))
        self.asser.setUnsetAsser('rotation', 1)
        self.asser.avancer(200.0)
        if couleur == 'R':
            self.asser.tourner(3*math.pi/2)
        else:
            self.asser.tourner(0)
        self.asser.avancer(-300.0)
        """
        
    def testPosition(self):
        self.recalage()
        raw_input()
        self.asserInstance.avancer(600)
        raw_input()
        self.asserInstance.tourner(1.57)
        raw_input()
        self.asserInstance.goTo(outils_math.point.Point(100,1500))
        raw_input()
        self.asserInstance.goTo(outils_math.point.Point(800,250))
        raw_input()
        self.asserInstance.tourner(3.1415)
        raw_input()
        self.asserInstance.avancer(-400)

    def evitement(self):
        print 'evitement'