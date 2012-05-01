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
import recherche_chemin.thetastar
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
        theta = recherche_chemin.thetastar.Thetastar([])
        theta.enregistreGraphe()
        if hasattr(__builtin__.instance, 'robotInstance'):
            self.robotInstance = __builtin__.instance.robotInstance
        else:
            log.logger.error("asservissement : ne peut importer instance.robotInstance")
        if hasattr(__builtin__.instance, 'serieAsserInstance'):
            self.serieAsserInstance = __builtin__.instance.serieAsserInstance
        else:
            log.logger.error("asservissement : ne peut importer instance.serieAsserInstance")
            
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
        
        self.modeRotation = 2
        self.modeTranslation = 2
    
    def goTo(self, arrivee):
        log.logger.info("Calcul de la durée de déplacement")
        theta = recherche_chemin.thetastar.Thetastar(self.liste_robots_adv)
        chemin_python = theta.rechercheChemin(depart,arrivee)
        
        self.majVitesse(self.modeDeplacement)
        
        try :
            chemin_python.remove(chemin_python[0])
        except :
            return (depart)
        angleSauv = 1000
        for i in chemin_python:
            if angleSauv!= 1000:
                #DUREE ROTATION
                delta_x = (arrivee.x-depart.x)
                delta_y = (arrivee.y-depart.y)
                angle = math.atan2(delta_y,delta_x)
                dureeRotation = abs(angle - angleSauv)/self.vitesseRotation
                
                #DUREE TRANSLATION
                dureeTranslation = self.vitesseTranslation*math.sqrt(delta_x**2+delta_y**2)
                
                #MAJ des variables
                angleSauv = angle
                depart = i
                
            else:
                #DUREE DE ROTATION = constante
                delta_x = (arrivee.x-depart.x)
                delta_y = (arrivee.y-depart.y)
                angleSauv = math.atan2(delta_y,delta_x)
                dureeRotation = 0.5
                
                #TRANSLATION
                dureeTranslation = math.sqrt(delta_x**2+delta_y**2)/self.vitesseTranslation
                
                #MAJ des variables
                depart = i
            
            return dureeRotation + dureeTranslation
         
      
    def gestionTourner(self, angle):
        self.majVitesse(self.modeDeplacement)
        if orientation:
            return math.abs(orientation - angle)/self.vitesseRotation
        else:
            return 0.5
    
    def gestionAvancer(self, distance):
        self.majVitesse(self.modeDeplacement)
        return distance/self.vitesseTranslation
    
    def changerVitesse(self, modeDeplacement):
        if modeRotation == 1:
            self.vitesseRotation = 1.5
        elif modeRotation == 2:
            self.vitesseRotation = 0.4
        else:
            modeRotation = 0.2
            
        if modeTranslation == 1:
            self.vitesseTranslation = 148
        elif modeTranslation == 2:
            self.vitesseTranslation = 368
        else:
            self.vitesseTranslation = 573
    
    def getPosition(self):
        self.serieAsserInstance.ecrire("pos")
        reponse = str(self.serieAsserInstance.lire())
        try:
            if reponse[4]== "+":
                reponse = reponse.split("+")
                pos = point.Point(float(reponse[1]),float(reponse[0]))
            else:
                reponse = reponse.split("-")
                pos = point.Point(-float(reponse[1]),float(reponse[0]))
            return pos
        except:
            self.getPosition()
            
    def setPosition(self,position):
        self.serieAsserInstance.ecrire("cx")
        self.serieAsserInstance.ecrire(str(float(position.x)))
        self.serieAsserInstance.ecrire("cy")
        self.serieAsserInstance.ecrire(str(float(position.y)))
            
    def getOrientation(self):
        self.serieAsserInstance.ecrire("eo")
        reponse = str(self.serieAsserInstance.lire())
        if re.match("^[0-9]+$", reponse):
            orientation = float(reponse)/1000.0
            #self.robotInstance.setOrientation(orientation)
            return orientation
        else:
            return self.getOrientation()
            
    def setOrientation(self,orientation):
        self.serieAsserInstance.ecrire("co")
        self.serieAsserInstance.ecrire(str(float(orientation)))
        
    def recalage(self):
        self.serieAsserInstance.ecrire("recal")
        while not acquitement:
            self.serieAsserInstance.ecrire('acq')
            reponse = self.serieAsserInstance.lire()
            if reponse == "FIN_REC":
                print reponse
                acquitement = True
            #TODO : gestion stop ?
        
    def setUnsetAsser(self, asservissement, mode):
        pass
            
            
    def changerVitesse(self, typeAsservissement, valeur):
        if typeAsservissement == "rotation":
            self.modeRotation = valeur
        elif typeAsservissement == "translation":
            self.modeTranslation = valeur
        
    def immobiliser(self):
        pass
        