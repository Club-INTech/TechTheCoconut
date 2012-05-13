# -*- coding: utf-8 -*-

import sys
import os
import math
import time
import __builtin__
import timer
import re
import log
import outils_math.point as point
import actionneur
import robot
import lib.log
import outils_math
import capteur
log =lib.log.Log(__name__)

sys.path.append('../')

import profils.develop.constantes

class Asservissement_duree:
    """
    Classe pour gérer l'asservissement
    """
    def __init__(self):
        self.theta = __builtin__.instance.theta
        if hasattr(__builtin__.instance, 'robotInstance'):
            self.robotInstance = __builtin__.instance.robotInstance
        else:
            log.logger.error("asservissement : ne peut importer instance.robotInstance")
            
        #distance seuil de detection pour les ultrasons
        #self.maxCapt = 400
        self.maxCapt = 0
        
        #liste des centres de robots adverses repérés (liste de points)
        
        self.liste_robots_adv = __builtin__.instance.liste_robots_adv
        
        #rayon moyen des robots adverses
        #TODO : à mettre dans constantes
        self.rayonRobotsAdverses = 200.0
        
        #timer pour les timeout
        self.timerAsserv = timer.Timer()
        
        self.vitesseRotation = 0.4
        self.vitesseTranslation = 368.
        self.modeRotation = 2
        self.modeTranslation = 2
        self.orientation = 0
        self.position = point.Point(0,400)
        self.duree = 0
    
    def lancerChrono(self):
        self.duree = 0
        
    def mesurerChrono(self):
        return self.duree
        
    def goToSegment(self, arrivee, avecRechercheChemin = False):
        """
        Fonction qui envoie un point d'arrivé au robot sans utiliser la recherche de chemin (segment direct départ-arrivée)
        :param script: point d'arrivé
        :type script: point
        :param avecRechercheChemin: si le segment a été trouvé par la recherche de chemin
        :type avecRechercheChemin: booléen
        """
        depart = self.getPosition()
        delta_x = (arrivee.x-depart.x)
        delta_y = (arrivee.y-depart.y)
        angle = math.atan2(delta_y,delta_x)
        self.gestionTourner(angle)
        
        """
        appel d'une translation de la distance euclidienne depart->arrivée
        sans instruction particulière
        avec un booléen codant l'utilisation de la recherche de chemin
        """
        self.gestionAvancer(math.sqrt(delta_x**2+delta_y**2),"",avecRechercheChemin)
    
    def goTo(self, arrivee):
        """
        Fonction qui appelle la recherche de chemin et envoie une liste de coordonnées à la carte asservissement
        :param depart: point de départ
        :type depart: Point
        :param arrivee: point d'arrivée
        :type arrivee: Point
        :param chemin: chemin renvoyé par la recherche de chemin
        :type chemin: liste de points
        """
        depart = self.getPosition()
        log.logger.info("Appel de la recherche de chemin pour le point de départ : ("+str(depart.x)+","+str(depart.y)+") et d'arrivée : ("+str(arrivee.x)+","+str(arrivee.y)+")")
        chemin_python = self.theta.rechercheChemin(depart,arrivee)
        
        try :
            chemin_python.remove(chemin_python[0])
        except :
            return (depart)
            
        for i in chemin_python:
            log.logger.info("goto (" + str(float(i.x)) + ', ' + str(float(i.y)) + ')')
            
            #effectue un segment du chemin trouvé, en indiquant que la recherche de chemin a été utilisée
            self.goToSegment(i,True)
        return "chemin_termine"
        
    def gestionAvancer(self, distance, instruction = "", avecRechercheChemin = False):
        self.position.x += distance*math.cos(self.orientation)
        self.position.y += distance*math.sin(self.orientation)
        self.duree +=  distance/self.vitesseTranslation
        print "temps de translation\tde "+str(int(distance*10)/10.)+",   \tvitesse "+str(self.modeTranslation)+":\t"+str(distance/self.vitesseTranslation)
    
    def gestionTourner(self, angle, instruction = ""):
        if __builtin__.constantes['couleur'] == "r":
            angle = math.pi - angle
        
        deltaAngle = abs(self.orientation - angle)
        while deltaAngle >= 2*math.pi:
            deltaAngle -= 2*math.pi
        while deltaAngle > math.pi:
            deltaAngle = 2*math.pi - deltaAngle
        self.orientation = angle
        self.duree += deltaAngle/self.vitesseRotation
        print "temps de rotation\tà "+str(int(angle*1000)/1000.)+",   \tvitesse "+str(self.modeRotation)+":\t"+str(deltaAngle/self.vitesseRotation)
        
    def getPosition(self):
        return point.Point(self.position.x,self.position.y)
    
    def setPosition(self,position):
        self.position.x = position.x
        self.position.y = position.y
            
    def getOrientation(self):
        return self.orientation
            
    def setOrientation(self,orientation):
        self.orientation = orientation
     
    def changerVitesse(self, typeAsservissement, valeur):
        
        if typeAsservissement == "rotation":
            self.modeRotation = valeur
            if self.modeRotation == 1:
                self.vitesseRotation = 0.2
            elif self.modeRotation == 2:
                self.vitesseRotation = 0.4
            else:
                self.vitesseRotation = 1.5
                
        elif typeAsservissement == "translation":
            self.modeTranslation = valeur
            if self.modeTranslation == 1:
                self.vitesseTranslation = 148.
            elif self.modeTranslation == 2:
                self.vitesseTranslation = 368.
            else:
                self.vitesseTranslation = 573.
                
    def immobiliser(self):
        pass
       
    def recalage(self):
        pass
        
    def setUnsetAsser(self, asservissement, mode):
        pass
        
    def attendre(self, temps):
        self.duree += temps