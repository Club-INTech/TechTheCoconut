# -*- coding: utf-8 -*-

import sys
import os
import math
import time
import __builtin__
import lib.timer
#sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

import log
import outils_math.point as point
import actionneur
import robot
import outils_math.point
import recherche_chemin.thetastar
import peripherique
import lib.log
import outils_math
import capteur
log =lib.log.Log(__name__)

sys.path.append('../')

import profils.develop.constantes

import serial

class Asservissement:
    """
    Classe pour gérer l'asservissement
    """
    def __init__(self):
        theta = recherche_chemin.thetastar.Thetastar([])
        theta.enregistreGraphe()
        #self.capteursInstance = lib.capteur.Capteur('ultrason', 1)
        if hasattr(__builtin__.instance, 'capteurInstance'):
            self.capteurInstance = __builtin__.instance.capteurInstance
        else:
            log.logger.error("l'instance de instance.capteurInstance n'est pas chargée")
        if hasattr(__builtin__.instance, 'robotInstance'):
            self.robotInstance = __builtin__.instance.robotInstance
        else:
            log.logger.error("l'instance de instance.robotInstance n'est pas chargée")
        if hasattr(__builtin__.instance, 'serieAsserInstance'):
            self.serialInstance = __builtin__.instance.serieAsserInstance
        else:
            log.logger.error("l'instance de instance.serieAsserInstance n'est pas chargée")
        if hasattr(__builtin__.instance, 'serieCaptInstance'):
            self.CaptSerialInstance = __builtin__.instance.serieCaptInstance
        else:
            log.logger.error("l'instance de instance.serieCaptInstance n'est pas chargée")
        self.maxCapt = 600
            
    
    def goToScript(self, script):
        """
        Fonction qui envoie une liste de coordonnées à la carte d'asservissement sans utiliser la recherche de chemin
        :param script: Script à lancer
        :type script: string
        """
        pass
    
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
        position = self.MAJorientation()
        log.logger.info("Calcul du centre du robot en fonction de l'angle des bras")
        theta = recherche_chemin.thetastar.Thetastar([])
        log.logger.info("Appel de la recherche de chemin pour le point de départ : ("+str(depart.x)+","+str(depart.y)+") et d'arrivée : ("+str(arrivee.x)+","+str(arrivee.y)+")")
        chemin_python = theta.rechercheChemin(position,arrivee)
        
        try :
            chemin_python.remove(chemin_python[0])
        except :
            return (depart)
            
        for i in chemin_python:
             for pat in self.fins_ligne:
                self.serialInstance.write(pat)
             log.logger.info("écrit sur série : "+"goto\n" + str(float(i.x)) + '\n' + str(float(i.y)) + '\n')
             for pat in self.fins_ligne:
                self.serialInstance.write("goto" + pat + str(float(i.x)) + pat + str(float(i.y)) + pat)
             position = self.MAJorientation()
             
             debut_timer = self.strategieInstance.timerStrat.getTime()
             acquittement = False
             #debutTimer = lib.timer.getTime()
             while not acquittement:
                 for pat in self.fins_ligne:
                     self.serialInstance.write('acq'+pat)
                 reponse = str(self.serialInstance.readline()).replace("\n","").replace("\r","").replace("\0", "")
                 print reponse
                 if reponse == "FIN_MVT":
                     print 'FIN_MVT'
                     acquittement = True
                 capteur = self.capteurInstance.mesurer()
                 try:
                     if int(capteur) < self.maxCapt:
                         return "obstacle"
                 except:
                     pass
                 
                 if int(self.strategieInstance.timerStrat.getTime()) - int(debut_timer) > 8:
                     print "timeoout !"
                     return "timeout"
                     
        return "acquittement"
                    
                    
    def recalage(self):
        self.serialInstance.write("\n\r")
        self.serialInstance.write("recal\n\r")
        
        while not acquitement:
            self.serialInstance.write('acq\n\r')
            reponse = str(self.serialInstance.readline()).replace("\n","").replace("\r","").replace("\0", "")
            if reponse == "FIN_REC":
                print reponse
                acquitement = True
        
        
    def tourner(self, angle):
        """
        Fonction de script pour faire tourner le robot sur lui même.
        :param angle: Angle à atteindre
        :type angle: Float
        """
        self.serialInstance.write("\n\r")
        self.serialInstance.write('t\n\r' + str(float(angle))+'\n\r')
        log.logger.info("Ordre de tourner à " + str(float(angle)))
        acquitement = False
        #debutTimer = lib.timer.getTime()
        while not acquitement:
            self.serialInstance.write('acq\n')
            self.serialInstance.write('acq\r\n')
            self.serialInstance.write('acq\n\r')
            reponse = str(self.serialInstance.readline()).replace("\n","").replace("\r","").replace("\0", "")
            if reponse == "FIN_MVT":
                print reponse
                acquitement = True
            elif reponse == "STOPPE":
                return "stoppe"
                break
            #timerCourant = lib.timer.getTime()
            #if timerCourant - debutTimer == 8:
                #return "timeout"
        return "acquittement"
    
    def avancer(self, distance):
        """
        Fonction de script pour faire avancer le robot en ligne droite. (distance <0 => reculer)c
        :param distance: Distance à parcourir
        :type angle: Float
        """
        self.serialInstance.write("\n\r")
        self.serialInstance.write('d\n\r' + str(float(distance))+'\n\r')
        log.logger.info("Ordre d'avancer de " + str(float(distance)))
        acquitement = False
        #debutTimer = lib.timer.getTime()
        while not acquitement:
            self.serialInstance.write('acq\n')
            self.serialInstance.write('acq\r\n')
            self.serialInstance.write('acq\n\r')
            reponse = str(self.serialInstance.readline()).replace("\n","").replace("\r","").replace("\0", "")
            
            if reponse == "FIN_MVT":
                print reponse
                acquitement = True
            elif reponse == "STOPPE":
                return "stoppe"
        
            capteur = 5000
            self.CaptSerialInstance.write('ultrason\n')
            self.CaptSerialInstance.write('ultrason\r\n')
            self.CaptSerialInstance.write('ultrason\n\r')
            time.sleep(0.01)
            capteur = self.capteurInstance.mesurer()
            
            print capteur
            if int(capteur) < self.maxCapt:
                print 'CAPTEUR !'
                self.immobiliser()
                self.robotInstance.obstacle = True
                raise Exception
                #return "obstacle"
        return "acquittement"
        
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
        
        self.serialInstance.write(asservissement+mode+'\n')
        self.serialInstance.write(asservissement+mode+'\r\n')
        self.serialInstance.write(asservissement+mode+'\n\r')
        
    def changerPWM(self, typeAsservissement, valeur):
        if typeAsservissement == "rotation":
            self.serialInstance.write("crm\n"+str(float(valeur))+"\n")
        elif typeAsservissement == "translation":
            self.serialInstance.write("ctm\n"+str(float(valeur))+"\n")
            
    def changerVitesse(self, typeAsservissement, valeur):
        """
        spécifie une vitesse prédéfinie en translation ou rotation
        une valeur 1,2,3 est attendue
        1 : vitesse "prudente"
        2 : vitesse normale
        3 : vitesse pour forcer
        """
        
        if typeAsservissement == "rotation":
            self.serialInstance.write("crv"+str(int(valeur))+"\n")
        elif typeAsservissement == "translation":
            self.serialInstance.write("ctv"+str(int(valeur))+"\n")
        

    def MAJorientation(self):
        for pat in ["eo\n","eo\r\n","eo\n\r"]:
            self.serialInstance.write(pat)
            reponse = str(self.serialInstance.readline()).replace("\n","").replace("\r","").replace("\0", "")
            import re
            if re.match("^[0-9]+$", reponse):
                orientation = float(reponse)/1000.0
                self.robotInstance.setOrientation(orientation)
                return orientation
                break
        
    def MAJposition(self):
        for pat in ["pos\n","pos\r\n","pos\n\r"]:
            self.serialInstance.write(pat)
            reponse = str(self.serialInstance.readline()).replace("\n","").replace("\r","").replace("\0", "")
            try:
                if reponse[4]== "+":
                    reponse = reponse.split("+")
                    pos = outils_math.point.Point(float(reponse[1]),float(reponse[0]))
                else:
                    reponse = reponse.split("-")
                    pos = outils_math.point.Point(-float(reponse[1]),float(reponse[0]))
                self.robotInstance.setPosition(pos)
                return pos
                break
            except:
                pass
        
        
    def immobiliser(self):
        self.serialInstance.write('stop\n')
        self.serialInstance.write('stop\r\n')
        self.serialInstance.write('stop\n\r')
        
    def calculRayon(self, angle):
        """
        Modifie le rayon du cercle circonscrit au robot par rapport au centre d'origine (bras rabattus).
        Le calcul ne se fait que sur un bras (inférieur droit dans le repère du robot) puisque le tout est symétrique.
        
        
        :param angle: angle entre la face avant du robot et les bras en bas du robot. Unité :  radian
        :type angle: float
        """
        
        #récupération des constantes nécessaires:
        log.logger.info('Calcul du rayon et du centre du robot')
        
        longueur_bras = profils.develop.constantes.constantes["Coconut"]["longueurBras"]
        largeur_robot = profils.develop.constantes.constantes["Coconut"]["largeurRobot"]
        longueur_robot = profils.develop.constantes.constantes["Coconut"]["longueurRobot"]
        
        diam_original = math.sqrt((longueur_robot/2) ** 2 + (largeur_robot/2) ** 2)
        proj_x = -longueur_bras*math.cos(float(angle))
        proj_y = longueur_bras*math.sin(float(angle))
        
        
        #[]la longueur est sur x, largeur sur y
        #point à l'extremité du bras droit
        sommet_bras = outils_math.point.Point(longueur_robot/2 + proj_x, largeur_robot/2 + math.sqrt(proj_y ** 2))
        #point au sommet bas gauche du robot
        sommet_robot = outils_math.point.Point(-longueur_robot/2, -largeur_robot/2)
        
        diam_avec_bras = 2*math.sqrt((sommet_bras.x) ** 2 + (sommet_bras.y) ** 2)
        
        if diam_avec_bras > diam_original:
            self.robotInstance.rayon = diam_avec_bras/2
            
        else:
            self.robotInstance.rayon = diam_original/2
            
    def afficherMenu(self):
        print """
        Indiquer l'action à effectuer :
        Quitter-------------------------------[0]
        Zone de départ------------------------[1]
        Constante de rotation-----------------[2]
        Constante de translation--------------[3]
        Changer la osition courante-----------[4]
        Activer/Désactiver l'asservissement---[5]
        Afficher des valeurs------------------[6]
        Ping de la liaison série--------------[7]\n
        """

    def afficherSousMenu(self):
        print """
        Revenir au menu-----------------------[0]
        Changer la dérivée--------------------[1]
        Changer l'intégration-----------------[2]
        Changer le proportionnel--------------[3]
        Mettre le max du PWM------------------[4]\n
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
                couleur = raw_input("Indiquer la zone de départ (r/v)\n")
                message = 'c\nc\n' + str(couleur)
                self.serialInstance.write(message)
                self.afficherMenu()
            #Définir les constantes de rotation
            elif choix == '2':
                exit = False
                valeurs = {"1" : "d", "2" : "i", "3" : "p", "4" : "m"}
                while not exit:
                    self.afficherSousMenu()
                    choix = raw_input()
                    message = "c\nr\n"
                    
                    if choix != '0':
                        constante = raw_input("Indiquer la valeur de la constante :\n")
                        message += str(valeurs[choix]) + '\n' + str(constante)
                        self.serialInstance.write(message)
                    
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
                    message = "c\nt\n"
                    
                    if choix != '0':
                        constante = raw_input("Indiquer la valeur de la constante :\n")
                        message += valeurs[choix] + '\n' + str(constante)
                        self.serialInstance.write(message)
                    
                    else:
                        exit = True
                        self.afficherMenu()
            #Définir la position courante
            elif choix == '4':
                print "Ne pas rentrer de valeur pour une coordonée permet de laisser la valeur déjà enregistrée sur l'AVR\n"
                coordonneX = raw_input("Rentrer a coordonée en x : \n")
                if coordonneX:
                    message = 'cx' + str(coordonneX)
                    self.serialInstance.write(message)
                
                coordonneY = raw_input("Rentrer a coordonée en y: \n")
                if coordonneY:
                    message = 'cy' + str(coordonneY)
                    self.serialInstance.write(message)
                
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
                    Désactiver la translation-------------[4]\n
                    """
                    constante = raw_input()
                    if constante == '1':
                        message = 's\nr\n'
                        self.serialInstance.write(message)
                    elif constante == '2':
                        message = 'd\nr\n'
                        self.serialInstance.write(message)
                    elif constante == '3':
                        message = 's\nt\n'
                        self.serialInstance.write(message)
                    elif constante == '4':
                        message = 'd\nt\n'
                        self.serialInstance.write(message)
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
                    Afficher les coordonnées enregistrées--------------[5]\n
                    """
                    choix = raw_input()
                    if choix == '0':
                        exit = True
                        self.afficherMenu()
                        
                    elif choix == '1':
                        message = 'e\nc'
                        
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
                                message = 'e\nr\n' + valeurs[choix]
                                self.serialInstance.write(message)
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
                                message = 'e\nt\n' + valeurs[choix]
                                self.serialInstance.write(message)
                    elif choix == '4':
                        self.serialInstance.write('e\ns')
                    elif choix =='5':
                        exit = False
                        while not exit:
                            self.serialInstance.write('ex')
                            answer = False
                            while not answer:
                                while not self.serialInstance.file_attente.empty():
                                    print self.serialInstance.file_attente.get()
                                    answer = True
                                    self.afficherSousMenu()
                            self.serialInstance.write('y\ne')
                            while not answer:
                                while not self.serialInstance.file_attente.empty():
                                    print self.serialInstance.file_attente.get()
                                    answer = True
                                    self.afficherSousMenu()
            elif choix == '7':
                exit = False
                while not exit:
                    self.serialInstance.write('?\n')
                    
            else:
                print "Il faut choisir une valeur contenue dans le menu.\n"
                
    def test(self):
        print "test"
        self.serialInstance.write("?\n")
        time.sleep(1)
        print ">"+self.serialInstance.readline()+"<"