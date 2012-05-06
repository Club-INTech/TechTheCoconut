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

class Asservissement:
    """
    Classe pour gérer l'asservissement
    """
    def __init__(self):
        theta = recherche_chemin.thetastar.Thetastar([])
        theta.enregistreGraphe()
        if hasattr(__builtin__.instance, 'capteurInstance'):
            self.capteurInstance = __builtin__.instance.capteurInstance
        else:
            log.logger.error("asservissement : ne peut importer instance.capteurInstance")
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
        
        self.vitesseTranslation = 2
        self.vitesseRotation = 2
            
    
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
        log.logger.info("Calcul du centre du robot en fonction de l'angle des bras")
        theta = recherche_chemin.thetastar.Thetastar(self.liste_robots_adv)
        log.logger.info("Appel de la recherche de chemin pour le point de départ : ("+str(depart.x)+","+str(depart.y)+") et d'arrivée : ("+str(arrivee.x)+","+str(arrivee.y)+")")
        chemin_python = theta.rechercheChemin(depart,arrivee)
        
        try :
            #NOTE on devrait peut etre laisser l'exception remonter dans le script...
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
        self.serieAsserInstance.ecrire("t")
        self.serieAsserInstance.ecrire(str(float(angle)))
        log.logger.info("Ordre de tourner à " + str(float(angle)))
        acquitement = False
        debut_timer = int(self.timerAsserv.getTime())
        while not acquitement:
            self.serieAsserInstance.ecrire('acq')
            reponse = str(self.serieAsserInstance.lire())
            if reponse == "FIN_MVT":
                acquitement = True
            elif reponse == "STOPPE":
                print "tourner : stoppé !"
                return "stoppe"
            elif int(self.timerAsserv.getTime()) - debut_timer > 8:
                print "tourner : timeout !"
                return "timeout"
                
        return "acquittement"
    
    def avancer(self, distance):
        """
        Fonction de script pour faire avancer le robot en ligne droite. (distance <0 => reculer)c
        :param distance: Distance à parcourir
        :type angle: Float
        """
        self.serieAsserInstance.ecrire("d")
        self.serieAsserInstance.ecrire(str(float(distance)))
        log.logger.info("Ordre d'avancer de " + str(float(distance)))
        acquitement = False
        debut_timer = int(self.timerAsserv.getTime())
        while not acquitement:
            self.serieAsserInstance.ecrire('acq')
            reponse = str(self.serieAsserInstance.lire())
            if reponse == "FIN_MVT":
                acquitement = True
            elif reponse == "STOPPE":
                print "avancer : stoppé !"
                return "stoppe"
            else:
                capteur = self.capteurInstance.mesurer()
                if capteur < self.maxCapt:
                    print 'avancer : capteur !'
                    return "obstacle"
                elif int(self.timerAsserv.getTime()) - debut_timer > 8:
                    print "avancer : timeout !"
                    return "timeout"
                
        return "acquittement"
        
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
        """
        Arrête ou remet l'asservissement en rotation
        :param asservissement: Définit l'asservissement ciblé (translation ou rotation)
        :type asservissement: string
        :param mode: permet de choisir entre marche et arrêt. 0 = arrêt; 1 = marche
        :type mode: int
        """
        if mode == 0:
            mode = '0'
        else:
            mode = '1'
            
        if asservissement == "rotation":
            asservissement = 'cr'
        else:
            asservissement = 'ct'
        
        self.serieAsserInstance.ecrire(asservissement+mode)
        
    def changerPWM(self, typeAsservissement, valeur):
        if typeAsservissement == "rotation":
            self.serieAsserInstance.ecrire("crm")
            self.serieAsserInstance.ecrire(str(float(valeur)))
        elif typeAsservissement == "translation":
            self.serieAsserInstance.ecrire("ctm")
            self.serieAsserInstance.ecrire(str(float(valeur)))
            
    def changerVitesse(self, typeAsservissement, valeur):
        """
        spécifie une vitesse prédéfinie en translation ou rotation
        une valeur 1,2,3 est attendue
        1 : vitesse "prudente"
        2 : vitesse normale
        3 : vitesse pour forcer
        """
        if typeAsservissement == "rotation":
            self.serieAsserInstance.ecrire("crv"+str(int(valeur)))
            self.vitesseRotation = int(valeur)
        elif typeAsservissement == "translation":
            self.serieAsserInstance.ecrire("ctv"+str(int(valeur)))
            self.vitesseTranslation = int(valeur)
            
    def getVitesse(self, typeAsservissement):
        if typeAsservissement == "rotation":
            return self.vitesseRotation
        elif typeAsservissement == "translation":
            return self.vitesseTranslation
        
    def immobiliser(self):
        self.serieAsserInstance.ecrire('stop')
        
    def gestionAvancer(self, distance, instruction = "", avecRechercheChemin = False):
        """
        méthode de haut niveau pour translater le robot
        prend en paramètre la distance à parcourir en mm
        et en facultatif une instruction "auStopNeRienFaire" ou "forcer"
        """
        
        print "#avancer à "+str(distance)+", "+instruction
        
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
                        print 'gestionAvancer : capteur !'
                    else :
                        print 'gestionAvancer : la voie est libre !'
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
        
        print "#tourner à "+str(angle)+", "+instruction
        
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
        
    def afficherMenu(self):
        print """
        Indiquer l'action à effectuer :
        Quitter-------------------------------[0]
        Zone de départ------------------------[1]
        Constante de rotation-----------------[2]
        Constante de translation--------------[3]
        Changer la position courante-----------[4]
        Activer/Désactiver l'asservissement---[5]
        Afficher des valeurs------------------[6]
        Ping de la liaison série--------------[7]
        """

    def afficherSousMenu(self):
        print """
        Revenir au menu-----------------------[0]
        Changer la dérivée--------------------[1]
        Changer l'intégration-----------------[2]
        Changer le proportionnel--------------[3]
        Mettre le max du PWM------------------[4]
        """
        
    def modifierConstantes(self):
        self.afficherMenu()
        main_exit = False
        while not main_exit:
            
            choix = raw_input()
            #Quitter
            if choix == '0':
                main_exit = True
                pass
            #Définir la zone de départ
            elif choix == '1':
                couleur = raw_input("Indiquer la zone de départ (r/v)")
                message = 'cc' + str(couleur)
                self.serieAsserInstance.ecrire(message)
                self.afficherMenu()
            #Définir les constantes de rotation
            elif choix == '2':
                exit = False
                valeurs = {"1" : "d", "2" : "i", "3" : "p", "4" : "m"}
                while not exit:
                    self.afficherSousMenu()
                    choix = raw_input()
                    message = "cr"
                    
                    if choix != '0':
                        constante = raw_input("Indiquer la valeur de la constante :")
                        message += str(valeurs[choix]) + '' + str(constante)
                        self.serieAsserInstance.ecrire(message)
                    
                    else:
                        exit = True
                        self.afficherMenu()
            #Définir les constantes de translation
            elif choix == '3':
                exit = False
                valeurs = {"1" : "d", "2" : "i", "3" : "p", "4" : "m"}
                while not exit:
                    self.afficherSousMenu()
                    choix = raw_input()
                    message = "ct"
                    
                    if choix != '0':
                        constante = raw_input("Indiquer la valeur de la constante :")
                        message += valeurs[choix] + '' + str(constante)
                        self.serieAsserInstance.ecrire(message)
                    
                    else:
                        exit = True
                        self.afficherMenu()
            #Définir la position courante
            elif choix == '4':
                print "Ne pas rentrer de valeur pour une coordonée permet de laisser la valeur déjà enregistrée sur l'AVR"
                coordonneX = raw_input("Rentrer a coordonée en x : ")
                if coordonneX:
                    message = 'cx' + str(coordonneX)
                    self.serieAsserInstance.ecrire(message)
                
                coordonneY = raw_input("Rentrer a coordonée en y: ")
                if coordonneY:
                    message = 'cy' + str(coordonneY)
                    self.serieAsserInstance.ecrire(message)
                
                self.afficherMenu()
            #Activer ou désactiver l'asservissement
            elif choix == '5':
                exit = False
                while not exit:
                    print """
                    Revenir au menu-----------------------[0]
                    Activer la rotation-------------------[1]
                    Désactiver la rotation----------------[2]
                    Activer la translation----------------[3]
                    Désactiver la translation-------------[4]
                    """
                    constante = raw_input()
                    if constante == '1':
                        message = 'sr'
                        self.serieAsserInstance.ecrire(message)
                    elif constante == '2':
                        message = 'dr'
                        self.serieAsserInstance.ecrire(message)
                    elif constante == '3':
                        message = 'st'
                        self.serieAsserInstance.ecrire(message)
                    elif constante == '4':
                        message = 'dt'
                        self.serieAsserInstance.ecrire(message)
                    elif constante == '0':
                        exit = True
                        self.afficherMenu()
            #Afficher les constantes enregistrées dans l'AVR
            elif choix == '6':
                exit = False
                while not exit:
                    print """
                    Revenir au menu------------------------------------[0]
                    Afficher la couleur--------------------------------[1]
                    Afficher la rotation-------------------------------[2]
                    Afficher la translation----------------------------[3]
                    Afficher le type d'asservissement------------------[4]
                    Afficher les coordonnées enregistrées--------------[5]
                    """
                    choix = raw_input()
                    if choix == '0':
                        exit = True
                        self.afficherMenu()
                        
                    elif choix == '1':
                        message = 'ec'
                        
                    elif choix == '2':
                        exit = False
                        valeurs = {"1" : "d", "2" : "i", "3" : "p", "4" : "m"}
                        while not exit:
                            self.afficherSousMenu()
                            choix = raw_input()
                            if choix == '0':
                                exit = True
                                self.afficherMenu()
                            else:
                                message = 'er' + valeurs[choix]
                                self.serieAsserInstance.ecrire(message)
                    elif choix == '3':
                        exit = False
                        valeurs = {"1" : "d", "2" : "i", "3" : "p", "4" : "m"}
                        while not exit:
                            self.afficherSousMenu()
                            choix = raw_input()
                            if choix == '0':
                                exit = True
                                self.afficherMenu()
                            else:
                                message = 'et' + valeurs[choix]
                                self.serieAsserInstance.ecrire(message)
                    elif choix == '4':
                        self.serieAsserInstance.ecrire('es')
                    elif choix =='5':
                        exit = False
                        while not exit:
                            self.serieAsserInstance.ecrire('ex')
                            answer = False
                            while not answer:
                                while not self.serieAsserInstance.file_attente.empty():
                                    print self.serieAsserInstance.file_attente.get()
                                    answer = True
                                    self.afficherSousMenu()
                            self.serieAsserInstance.ecrire('ye')
                            while not answer:
                                while not self.serieAsserInstance.file_attente.empty():
                                    print self.serieAsserInstance.file_attente.get()
                                    answer = True
                                    self.afficherSousMenu()
            elif choix == '7':
                exit = False
                while not exit:
                    self.serieAsserInstance.ecrire('?')
                    
            else:
                print "Il faut choisir une valeur contenue dans le menu."
                
