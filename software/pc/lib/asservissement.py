# -*- coding: utf-8 -*-

import sys
import os
import math
import time

#sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

import log
import outils_math.point as point
import actionneur
import robot
import outils_math.point
import recherche_chemin.thetastar
import peripherique
import lib.log
log =lib.log.Log(__name__)

sys.path.append('../')

import profils.develop.constantes

class Asservissement:
    """
    Classe pour gérer l'asservissement
    """
    def __init__(self, robotInstance):
        theta = recherche_chemin.thetastar.Thetastar([])
        theta.enregistreGraphe()
        capteursInstance = lib.capteur.Capteur
        capteursInstance.demarrer
        chemin = lib.peripherique.chemin_de_peripherique("asservissement")
        self.robotInstance = robotInstance
        if chemin:
            self.serieInstance = lib.serie.Serie(chemin, "asservissement", 9600, 10)
        else:
            log.logger.error("L'asservissement n'est pas chargé")
        self.serieInstance.start()
    
    def goToScript(self, script):
        """
        Fonction qui envoie une liste de coordonnées à la carte d'asservissement sans utiliser la recherche de chemin
        :param script: Script à lancer
        :type script: string
        """
        pass
    
    def goTo(self, depart, arrivee, centre_robotA = None):
        """
        Fonction qui appelle la recherche de chemin et envoie une liste de coordonnées à la carte asservissement
        :param depart: point de départ
        :type depart: Point
        :param arrivee: point d'arrivée
        :type arrivee: Point
        :param chemin: chemin renvoyé par la recherche de chemin
        :type chemin: liste de points
        """
        
        log.logger.info("Calcul du centre du robot en fonction de l'angle des bras")
        theta = recherche_chemin.thetastar.Thetastar([])
        log.logger.info("Appel de la recherche de chemin pour le point de départ : ("+str(depart.x)+","+str(depart.y)+") et d'arrivée : ("+str(arrivee.x)+","+str(arrivee.y)+")")
        chemin_python = theta.rechercheChemin(depart,arrivee)
        
        chemin_python.remove(chemin_python[0])
            
        for i in chemin_python:
            self.serieInstance.ecrire("goto\n" + str(float(i.x)) + '\n' + str(float(i.y)) + '\n')
            
            """
            while self.serieInstance.inWaiting():
                pass
            """
            #lu = self.serieInstance.readline()
            #lu = lu.split("\r\n")[0]
            acquittement = False
            while not acquittement:
                if not self.serieInstance.file_attente.empty():
                    reponse = self.serieInstance.file_attente.get()
                    if reponse != "FIN_GOTO":
                        log.logger.debug("Erreur asservissement (goto) : " + reponse)
                    else:
                        acquittement = True
                        """
                    mesure = capteursInstance.mesurer
                    x = 0
                    if mesure < x:
                        self.immobiliser
                        self.avancer(-150)
                        #TODO Calculer le centre du robot adverse nommé centre_robotA
                        goto(depart, arrivee, centre_robotA)
                        """
            lol = raw_input("suivant ?")
                        
    def tourner(self, angle):
        """
        Fonction de script pour faire tourner le robot sur lui même.
        :param angle: Angle à atteindre
        :type angle: Float
        """
        self.serieInstance.ecrire("t\n" + str(float(angle)))
        acquittement = False
        while not acquittement:
            while not self.serieInstance.file_attente.empty():
                reponse = self.serieInstance.file_attente.get()
                if reponse == "FIN_TOU":
                    acquittement = True
                elif reponse == 6 or reponse ==7:
                    pass
                else:
                    log.logger.debug("Erreur asservissement (tourner) : " + reponse)
    
    def avancer(self, distance):
        """
        Fonction de script pour faire avancer le robot en ligne droite. (distance <0 => reculer)c
        :param distance: Distance à parcourir
        :type angle: Float
        """
        self.serieInstance.ecrire("d\n" + str(float(distance)))
        acquittement = False
        while not acquittement:
            while not self.serieInstance.file_attente.empty():
                reponse = self.serieInstance.file_attente.get()
                if reponse == "FIN_TRA":
                    acquittement = True
                elif reponse == 6 or reponse ==7:
                    pass
                else:
                    log.logger.debug("Erreur asservissement (avancer) : " + reponse)

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
            mode = 's\n'
        else:
            mode = 'd\n'
            
        if asservissement == "rotation":
            asservissement = 'r\n'
        else:
            asservissement = 't\n'
        
        self.serieInstance.ecrire(mode + asservissement)


    def immobiliser(self):
        """
        Fonction pour demander l'immombilisation du robot
        """
        self.serieInstance.ecrire('stop\n')
        
    def calculRayon(self, angle):
        """
        Modifie le rayon du cercle circonscrit au robot et retourne les coordonnées du nouveau centre par rapport au centre d'origine (bras rabattus).
        Le calcul ne se fait que sur un bras (inférieur droit dans le repère du robot) puisque le tout est symétrique.
        
        
        :param longueur_bras: longueur des bras du robot
        :type longueur_bras: int
        :param largeur_robot: largueur du robot
        :type largeur_robot: int
        :param angle: angle entre la face avant du robot et les bras en bas du robot. Unité : la radian
        :type angle: float
        :param proj_x/proj_y: projection sur x et y d'un bras du robot
        :type proj_x/proj_y : float
        :param sommet_bras : coordonnées du sommet du bras droit
        :type sommet_bras: Point
        :param segment_centre_bras: distance entre le centre original du cercle circonscrit au robot et le sommet du bras.
        :type segment_centre_bras: float
        """
        
        #récupération des constantes nécessaires:
        log.logger.info('Calcul du rayon et du centre du robot')
        
        #[pierre] j'ai modifié des constantes...
        #désolé mais c'était nécessaire : ta "largeur" était en fait celle de la table
        #et toute facon constantes.py manquait de clarté
        
        longueur_bras = profils.develop.constantes.constantes["Coconut"]["longueurBras"]
        largeur_robot = profils.develop.constantes.constantes["Coconut"]["largeurRobot"]
        longueur_robot = profils.develop.constantes.constantes["Coconut"]["longueurRobot"]
        
        #Commenté pour les tests !
        #angle = robot.actionneur['bd'].angle
        
        #[]ouais, on pourrait le mettre dans constantes..
        diam_original = math.sqrt((longueur_robot/2) ** 2 + (largeur_robot/2) ** 2)
        print diam_original
        #projection du bras sur x et y
        
        #[]c'est quoi la convention pour l'angle des bras ?
        #moi j'aurais pensé à mettre angle = 0 vers l'avant du robot, sur l'axe y.
        proj_x = -longueur_bras*math.cos(float(angle))
        proj_y = longueur_bras*math.sin(float(angle))
        #[]la longueur est sur x, largeur sur y
        sommet_bras = outils_math.point.Point(longueur_robot/2 + proj_x, largeur_robot/2 + math.sqrt(proj_y ** 2))
        sommet_robot = outils_math.point.Point(-longueur_robot/2, -largeur_robot/2)
        #longueur du segment entre le centre du robot avec les bras fermés et le sommet du bras
        #segment_centre_bras = math.sqrt(math.pow(sommet_bras.x, 2) + math.pow(sommet_bras.y, 2))
        
        #[] le diamètre mesuré (segment le plus long) doit etre pris entre deux extremités du robot.
        #là tu considères que le milieu du diamètre est le centre_original
        #en gros faut raisonner sur les diamètres, par sur les rayons ^^
        diam_avec_bras = 2*math.sqrt((sommet_bras.x) ** 2 + (sommet_bras.y) ** 2)
        if diam_avec_bras > diam_original:
            self.robotInstance.rayon = diam_avec_bras/2
            
        else:
            self.robotInstance.rayon = diam_original/2
            
        print self.robotInstance.rayon
            
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
                self.serieInstance.ecrire(message)
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
                        self.serieInstance.ecrire(message)
                    
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
                        self.serieInstance.ecrire(message)
                    
                    else:
                        exit = True
                        self.afficherMenu()
            #Définir la position courante
            elif choix == '4':
                print "Ne pas rentrer de valeur pour une coordonée permet de laisser la valeur déjà enregistrée sur l'AVR\n"
                coordonneX = raw_input("Rentrer a coordonée en x : \n")
                if coordonneX:
                    message = 'cx' + str(coordonneX)
                    self.serieInstance.ecrire(message)
                
                coordonneY = raw_input("Rentrer a coordonée en y: \n")
                if coordonneY:
                    message = 'cy' + str(coordonneY)
                    self.serieInstance.ecrire(message)
                
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
                        self.serieInstance.ecrire(message)
                    elif constante == '2':
                        message = 'd\nr\n'
                        self.serieInstance.ecrire(message)
                    elif constante == '3':
                        message = 's\nt\n'
                        self.serieInstance.ecrire(message)
                    elif constante == '4':
                        message = 'd\nt\n'
                        self.serieInstance.ecrire(message)
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
                                self.serieInstance.ecrire(message)
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
                                self.serieInstance.ecrire(message)
                    elif choix == '4':
                        self.serieInstance.ecrire('e\ns')
                    elif choix =='5':
                        exit = False
                        while not exit:
                            self.serieInstance.ecrire('ex')
                            answer = False
                            while not answer:
                                while not self.serieInstance.file_attente.empty():
                                    print self.serieInstance.file_attente.get()
                                    answer = True
                                    self.afficherSousMenu()
                            self.serieInstance.ecrire('y\ne')
                            while not answer:
                                while not self.serieInstance.file_attente.empty():
                                    print self.serieInstance.file_attente.get()
                                    answer = True
                                    self.afficherSousMenu()
            elif choix == '7':
                exit = False
                while not exit:
                    self.serieInstance.ecrire('?\n')
                    
            else:
                print "Il faut choisir une valeur contenue dans le menu.\n"
