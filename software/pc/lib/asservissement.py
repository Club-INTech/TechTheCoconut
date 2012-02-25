# -*- coding: utf-8 -*-

import sys
import os
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

import log
import outils_math.point as point
import actionneur
import robot
import outils_math.point
import recherche_chemin.thetastar
import peripherique
import lib.log
log = lib.log.Log()

sys.path.append('../')

import profils.develop.constantes

class Asservissement:
    """
    Classe pour gérer l'asservissement
    """
    def __init__(self, robotInstance):
        theta = recherche_chemin.thetastar.Thetastar([])
        theta.enregistreGraphe()
        chemin = peripherique.chemin_de_peripherique("asservissement")
        self.robotInstance = robotInstance
        if chemin:
            serie.Serie.__init__(self, chemin, "asservissement", 9600, 3)
        else:
            log.logger.error("L'asservissement n'est pas chargé")
        #self.start()
    
    def goToScript(self, script):
        """
        Fonction qui envoie une liste de coordonnées à la carte d'asservissement sans utiliser la recherche de chemin
        :param script: Script à lancer
        :type script: string
        """
        pass
    
    def goTo(self, depart, arrivee):
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
        self.avrToPython()
        theta = thetastar.Thetastar([])
        
        #TODO : appeler avrToPython()
        log.logger.info("Appel de la recherche de chemin pour le point de départ : ("+depart.x+","+depart.y+") et d'arrivée : ("+arrivee.x+","+arrivee.y+")")
        chemin_python = theta.rechercheChemin(depart,arrivee)
        
        i = 0
        while i+1 < len(chemin_python):
            centre_avr[i] = pythonToAvr(chemin_python[i],chemin_python[i+1])
        
        i = 0
        for centre in centre_avr:
            
            #on peut tenter de concaténer après, sans doute avec des \0 entre les messages
            self.ecrire("goto")
            self.ecrire(str(float(centre.x)))
            self.ecrire(str(float(centre.y)))
            
            
            # TODO : gestion des erreurs
            
            #serie.Serie.lire()
            self.reponse = self.file_attente.get(lu)
            if reponse == "END":
                pass
            else:
                log.logger.debug("Erreur asservissement : " + reponse)
            
    
    def pythonToAvr(self, depart, arrivee):
        """
        La recherche de chemin renvoit une position du robot qui est le centre du cercle circonscrit au robot en prenant en compte ses bras. Il faut envoyer
        à l'AVR le centre du robot avec les bras rabattus. pythonToAvr() calcule l'orientation du robot et le centre à envoyer à l'AVR à partir du point 
        de départ et du point d'arrivée.
        
        :param orientation: Orientation du robot calculée avec es points de départ et d'arrivée envoyé par la recherche de chemin
        :type orientation: float
        :param depart: Point de départ envoyé par la recherche de chemin
        :type depart: Point
        :param arrivee: Point d'arrevée envoyé par la recherche de chemin
        :type arrivee: Point
        :param centre: centre du robot selon la recherche de chemin
        :type centre: Point
        :param rayon: Rayon du robot selon la recherche de chemin
        :type rayon: float
        :param largeur_robot/longueur_robot: Constantes respectives de largeur et longueur du robot
        :type largeur_robot/longueur_robot: int
        :param proj_x/proj_y: Projections sur x et y suivant le clacul (voir commentaire lié au calcul)
        :type proj_x/proj_y: float
        
        """
        centre = self.robotInstance.position
        rayon = self.robotInstance.rayon
        longueur_robot = profils.develop.constantes.constantes["Coconut"]["longueurRobot"]
        largeur_robot = profils.develop.constantes.constantes["Coconut"]["largeurRobot"]
        
        #calcul de l'orientation
        proj_x = arrivee.x - depart.x
        proj_y = arrivee.y - depart.y
        
        
        if (proj_x==0):
            if (proj_y > 0):
                orientation=pi/2
            else:
                orientation=-pi/2
        elif (proj_x > 0):
            orientation=math.atan(proj_y/proj_x)
        else:
            if (proj_y > 0):
                orientation=math.atan(proj_y/proj_x) + pi
            else:
                orientation=math.atan(proj_y/proj_x) - pi
        
        #distance entre le centre de la recherche de chemin et le milieu de la longueur du robot (pythagore)
        normale_Robot = math.sqrt(rayon ** 2 - (longueur_robot / 2) ** 2)
        
        #Distance sur l'axe de translation entre le centre de la recherche de chemin et le centre AVR
        distance_centres = normale_Robot - (largeur_robot / 2)
        
        #Projection de la distance pour calculer les coordonnées du centre AVR
        proj_x = distance_centres*math.cos(orientation)
        proj_y = distance_centres*math.sin(orientation)
        
        #Calcul des coordonnées du centre AVR
        return outils_math.point.Point(arrivee.x - proj_x, arrivee.y - proj_y)
        
    def avrToPython(self, angle):
        #récupération des constantes nécessaires:
        rayon = self.robotInstance.rayon
        longueur_bras = profils.develop.constantes.constantes["Coconut"]["longueurBras"]
        largeur_robot = profils.develop.constantes.constantes["Coconut"]["largeurRobot"]
        longueur_robot = profils.develop.constantes.constantes["Coconut"]["longueurRobot"]
        diam_original = math.sqrt((longueur_robot/2) ** 2 + (largeur_robot/2) ** 2)
        
        if rayon > diam_original:
            # TODO : vérifier convention pour l'angle des bras :  angle = 0 vers l'avant du robot, sur l'axe y.
            proj_x = -longueur_bras*math.cos(float(angle))
            proj_y = longueur_bras*math.sin(float(angle))
            
            #[]la longueur est sur x, largeur sur y
            sommet_bras = outils_math.point.Point(longueur_robot/2 + proj_x, largeur_robot/2 + proj_y)
            sommet_robot = outils_math.point.Point(-longueur_robot/2, -largeur_robot/2)
        
            delta_x = - math.cos(self.robotInstance.orientation)*(sommet_bras.x+sommet_robot.x)/2 - math.sin(self.robotInstance.orientation)*(sommet_bras.y+sommet_robot.y)/2
            delta_y = - math.sin(self.robotInstance.orientation)*(sommet_bras.x+sommet_robot.x)/2 + math.cos(self.robotInstance.orientation)*(sommet_bras.y+sommet_robot.y)/2
            return outils_math.point.Point(delta_x,delta_y)
            
        else:
            return outils_math.point.Point(0., 0.)
    
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
        
        longueur_bras = profils.develop.constantes.constantes["Coconut"]["longueurBras"]
        largeur_robot = profils.develop.constantes.constantes["Coconut"]["largeurRobot"]
        longueur_robot = profils.develop.constantes.constantes["Coconut"]["longueurRobot"]
        
        #Commenté pour les tests !
        #angle = robot.actionneur['bd'].angle
        
        diam_original = math.sqrt((longueur_robot/2) ** 2 + (largeur_robot/2) ** 2)
        
        #projection du bras sur x et y
        
        # TODO : vérifier convention pour l'angle des bras :  angle = 0 vers l'avant du robot, sur l'axe y.
        proj_x = -longueur_bras*math.cos(float(angle))
        proj_y = longueur_bras*math.sin(float(angle))
        
        #la longueur est sur x, largeur sur y
        sommet_bras = outils_math.point.Point(longueur_robot/2 + proj_x, largeur_robot/2 + proj_y)
        sommet_robot = outils_math.point.Point(-longueur_robot/2, -largeur_robot/2)
        
        #longueur du segment entre le sommet à l'arrière du robot et le sommet du bras opposé
        diam_avec_bras = math.sqrt((sommet_bras.x - sommet_robot.x) ** 2 + (sommet_bras.y - sommet_robot.y) ** 2)
        
        if diam_avec_bras > diam_original:
            self.robotInstance.rayon = diam_avec_bras/2
            
        else:
            self.robotInstance.rayon = diam_original/2
            
    def afficherMenu():
        print """
        Indiquer l'action à effectuer :
        Quitter-------------------------------[0]
        Zone de départ------------------------[1]
        Rotation------------------------------[2]
        Translation---------------------------[3]
        Position courante---------------------[4]
        Activer/Désactiver l'asservissement---[5]
        Afficher des valeurs------------------[6]
        Ping de la liaison série--------------[7]\n
        """

    def afficherSousMenu():
        print """
        Revenir au menu-----------------------[0]
        Changer la dérivée--------------------[1]
        Changer l'intégration-----------------[2]
        Changer le proportionnel--------------[3]
        Mettre le max du PWM------------------[4]\n
        """
        
    def modifierConstantes(self):
        afficherMenu()

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
                self.ecrire(message)
                afficherMenu()
            #Définir les constantes de rotation
            elif choix == '2':
                exit = False
                valeurs = {"1" : "d", "2" : "i", "3" : "p", "4" : "m"}
                while not exit:
                    afficherSousMenu()
                    choix = raw_input()
                    message = "c\nr\n"
                    
                    if choix != '0':
                        constante = raw_input("Indiquer la valeur de la constante :\n")
                        message += str(valeurs[choix]) + '\n' + str(constante)
                        self.ecrire(message)
                    
                    else:
                        exit = True
                        afficherMenu()
            #Définir les constantes de translation
            elif choix == '3':
                exit = False
                valeurs = {"1" : "d", "2" : "i", "3" : "p", "4" : "m"}
                while not exit:
                    afficherSousMenu()
                    choix = raw_input()
                    message = "c\nt\n"
                    
                    if choix != '0':
                        constante = raw_input("Indiquer la valeur de la constante :\n")
                        message += valeurs[choix] + '\n' + str(constante)
                        self.ecrire(message)
                    
                    else:
                        exit = True
                        afficherMenu()
            #Définir la position courante
            elif choix == '4':
                print "Ne pas rentrer de valeur pour une coordonée permet de laisser la valeur déjà enregistrée sur l'AVR\n"
                coordonneX = raw_input("Rentrer a coordonée en x : \n")
                if coordonneX:
                    message = 'x\nc\n' + str(coordonneX)
                    self.ecrire(message)
                
                coordonneY = raw_input("Rentrer a coordonée en y: \n")
                if coordonneY:
                    message = 'y\nc\n' + str(coordonneY)
                    self.ecrire(message)
                
                afficherMenu()
            #Activer ou désactiver l'asservissement
            elif choix == '5':
                exit = False
                while not exit:
                    print """
                    Revenir au menu-----------------------[0]
                    Activer/désactiver la rotation--------[1]
                    Activer/désactiver la translation-----[2]\n
                    """
                    constante = raw_input()
                    if constante == '1':
                        message = 's\nr\n'
                        self.ecrire(message)
                    elif constante == '2':
                        message = 's\nt\n'
                        self.ecrire(message)
                    elif constante == '0':
                        exit = True
                        afficherMenu()
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
                        afficherMenu()
                        
                    elif choix == '1':
                        message = 'e\nc'
                        
                    elif choix == '2':
                        exit = False
                        valeurs = {"1" : "d", "2" : "i", "3" : "p", "4" : "m"}
                        while not exit:
                            afficherSousMenu()
                            choix = raw_input()
                            if choix == '0':
                                exit = True
                                afficherMenu()
                            else:
                                message = 'e\nr\n' + valeurs[choix]
                                self.ecrire(message)
                    elif choix == '3':
                        exit = False
                        valeurs = {"1" : "d", "2" : "i", "3" : "p", "4" : "m"}
                        while not exit:
                            afficherSousMenu()
                            choix = raw_input()
                            if choix == '0':
                                exit = True
                                afficherMenu()
                            else:
                                message = 'e\nt\n' + valeurs[choix]
                                self.ecrire(message)
                    elif choix == '4':
                        self.ecrire('e\ns')
                    elif choix =='5':
                        self.ecrire('x\ne')
                        print self.file_attente.get(lu)
                        self.ecrire('y\ne')
                        print self.file_attente.get(lu)
            else:
                print "Il faut choisir une valeur contenue dans le menu.\n"
