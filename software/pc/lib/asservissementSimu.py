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
import robot
import lib.log
import outils_math
log =lib.log.Log(__name__)

sys.path.append('../')

import profils.develop.constantes

class Asservissement:
    """
    Classe pour gérer l'asservissement
    """
    def __init__(self):
        self.theta = __builtin__.instance.theta
        if hasattr(__builtin__.instance, 'robotInstance'):
            self.robotInstance = __builtin__.instance.robotInstance
        else:
            log.logger.error("[asservissement] ne peut importer instance.robotInstance")
            
        
        #liste des centres de robots adverses repérés (liste de points)
        
        self.liste_robots_adv = __builtin__.instance.liste_robots_adv
        
        #rayon moyen des robots adverses
        #TODO : à mettre dans constantes
        self.rayonRobotsAdverses = 200.0
        
        #timer pour les timeout
        self.timerAsserv = timer.Timer()
        
        #attributs de position et orientation
        self.couleur = __builtin__.constantes["couleur"]
        if self.couleur == "r":
            self.position = point.Point(float(-1200),float(250))
            self.orientation = 0.0
        else:
            self.position = point.Point(float(1200),float(250))
            self.position = point.Point(float(-1200),float(250))
            self.orientation = math.pi
            
    
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
        log.logger.info("[asservissement] Appel de la recherche de chemin pour le point de départ : ("+str(depart.x)+","+str(depart.y)+") et d'arrivée : ("+str(arrivee.x)+","+str(arrivee.y)+")")
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
    
            
        
    def tourner(self, angle):
        """
        Fonction de script pour faire tourner le robot sur lui même.
        :param angle: Angle à atteindre
        :type angle: Float
        """
        log.logger.info("[asservissement] Ordre de tourner à " + str(float(angle)))
        return "acquittement"
    
    def avancer(self, distance):
        """
        Fonction de script pour faire avancer le robot en ligne droite. (distance <0 => reculer)c
        :param distance: Distance à parcourir
        :type angle: Float
        """
        log.logger.info("[asservissement] Ordre d'avancer de " + str(float(distance)))
        return "acquittement"
        
    def getPosition(self):
        return self.position
            
    def setPosition(self,position):
        self.position = position
        log.logger.info("[asservissement] Changement de la position enregistrée dans le robot à la position : x = " + position.x + " y = " + position.y)
            
    def getOrientation(self):
        return self.orientation
            
    def setOrientation(self,orientation):
        self.orientation = orientation
        log.logger.info("[asservissement] Changement de l'orientation enregistrée dans le robot à l'angle : " + orientation
        
    def recalage(self):
        log.logger.info("[asservissement] Lancement du recalage")
        pass
        
    def setUnsetAsser(self, asservissement, mode):
        log.logger.info("[asservissement] L'asservissement " + asservissement + " passe en mode " + mode)
        pass
        
    def changerPWM(self, typeAsservissement, valeur):
        log.logger.info("[asservissement] Changement de la valeur du PWM de " + typeAsservissement + " à " + valeur)
        pass
            
            
    def changerVitesse(self, typeAsservissement, valeur):
        log.logger.info("[asservissement] Changement de la vitesse de " + typeAsservissement + " à " + valeur)
        pass
        
    def immobiliser(self):
        log.logger.info("[asservissement] Immobilisation du robot")
        pass
        
    def gestionAvancer(self, distance, instruction = "", avecRechercheChemin = False):
        """
        méthode de haut niveau pour translater le robot
        prend en paramètre la distance à parcourir en mm
        et en facultatif une instruction "auStopNeRienFaire" ou "forcer"
        """
        
        log.logger.info("[asservissement] avancer à "+str(distance)+", "+instruction)
        
        posAvant = self.getPosition()
        retour = self.avancer(distance)
        
        if retour == "timeout" or (retour == "stoppe" and not instruction):
            ##1
            #stopper le robot
            self.immobiliser()
            if instruction == "sansRecursion":
                ##4
                #mettre à jour l'attribut position du robot
                
                #stopper l'execution du script parent
                raise Exception
                
            else:
                #reculer de ce qui a été avancé
                posApres = self.getPosition()
                dist = math.sqrt((posApres.x - posAvant.x) ** 2 + (posApres.y - posAvant.y) ** 2)
                if distance != 0: 
                    signe = distance/abs(distance)
                else:
                    signe = 1
                self.gestionAvancer(-signe*dist,"sansRecursion")
                #recommencer le déplacement
                self.gestionAvancer(distance,"sansRecursion")
        
        if retour == "obstacle" :
            ##2 
            #ajoute un robot adverse sur la table, pour la recherche de chemin
            orientation = self.getOrientation()
            position = self.getPosition()
            
            adverse = point.Point(position.x + (self.maxCapt+self.rayonRobotsAdverses)*math.cos(orientation),position.y + (self.maxCapt+self.rayonRobotsAdverses)*math.sin(orientation))
            __builtin__.instance.ajouterRobotAdverse(adverse)
            
            
            if instruction == "sansRecursion" or avecRechercheChemin:
                ##4
                #stopper le robot
                self.immobiliser()
                #mettre à jour l'attribut position du robot
                
                #stopper l'execution du script parent
                raise Exception
            else:
                
                ##3
                #stopper le robot
                self.immobiliser()
                #attente que la voie se libère
                ennemi_en_vue = True
                debut_timer = int(timerStrat.getTime())
                while ennemi_en_vue and (int(timerStrat.getTime()) - debut_timer) < 4 :
                    capteur = self.capteurInstance.mesurer()
                    if capteur < self.maxCapt:
                        log.logger.info("[asservissement] gestionAvancer : capteur !")
                    else :
                        log.logger.info("[asservissement] gestionAvancer : la voie est libre !")
                        ennemi_en_vue = False
                    
                if not ennemi_en_vue:
                    #vider la liste des robots adverses repérés
                    __builtin__.instance.viderListeRobotsAdv()
                    
                    #baisser vitesse
                    self.changerVitesse("translation", 1)
                    
                    #finir le déplacement
                    posApres = self.getPosition()
                    dist = math.sqrt((posApres.x - posAvant.x) ** 2 + (posApres.y - posAvant.y) ** 2)
                    if distance != 0:
                        signe = distance/abs(distance)
                    else:
                        signe = 1
                    self.gestionAvancer(distance-signe*dist)
                    
                    #remettre vitesse
                    self.changerVitesse("translation", 2)
                    
                else:
                    #mettre à jour l'attribut position du robot
                    
                    #stopper l'execution du script parent
                    raise Exception
                
        if retour == "stoppe" and instruction == "sansRecursion":
            ##4
            #mettre à jour l'attribut position du robot
            
            #stopper l'execution du script parent
            
            raise Exception
            
        if retour == "stoppe" and instruction == "forcer":
            ##5
            
            #augmenter vitesse
            self.changerVitesse("translation", 3)
            
            #finir le déplacement
            posApres = self.getPosition()
            dist = math.sqrt((posApres.x - posAvant.x) ** 2 + (posApres.y - posAvant.y) ** 2)
            if distance != 0:
                signe = distance/abs(distance)
            else:
                signe = 1
            self.gestionAvancer(distance-signe*dist)
            
            #remettre vitesse
            self.changerVitesse("translation", 2)
            
            
    def gestionTourner(self, angle, instruction = ""):
        
        """
        méthode de haut niveau pour tourner le robot
        prend en paramètre l'angle à parcourir en radians
        et en facultatif une instruction "auStopNeRienFaire" ou "forcer"
        """
        
        #l'angle spécifié dans les scripts est valable pour un robot violet.
        if __builtin__.constantes['couleur'] == "r":
            angle = math.pi - angle
        if angle > math.pi:
            angle = angle - 2*math.pi
        if angle < -math.pi:
            angle = angle + 2*math.pi
        
        log.logger.info("[asservissement] tourner à "+str(angle)+", "+instruction)
        
        orientAvant = self.getOrientation()
        retour = self.tourner(angle)
        
        if retour == "timeout" or (retour == "stoppe" and not instruction):
            
            #stopper le robot
            self.immobiliser()
            if instruction == "sansRecursion":
                ##4
                #mettre à jour l'attribut position du robot
                
                #stopper l'execution du script parent
                raise Exception
                
            else:
                ##1
                #tourner inversement à ce qui a été tourné
                self.gestionTourner(orientAvant,"sansRecursion")
                #recommencer le déplacement
                self.gestionTourner(angle,"sansRecursion")
        
        if retour == "stoppe" and instruction == "sansRecursion":
            ##4
            #mettre à jour l'attribut orientation du robot
            
            #stopper l'execution du script parent
            raise Exception
            
        if retour == "stoppe" and instruction == "forcer":
            ##5
            #augmenter vitesse
            self.changerVitesse("rotation", 3)
            #finir le déplacement
            self.gestionTourner(angle)
            #remettre vitesse
            self.changerVitesse("rotation", 2)
        