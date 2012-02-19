# -*- coding: utf-8 -*-

import sys
import os
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

import log
import outils_math.point as point
import actionneur
import outils_math.point

sys.path.append('../')

import profils.develop.constantes

log = log.Log()

class Robot:
    
    #:TODO: A modifier pour la valeur réel (voir a passer en  attribut d'instance
    rayon = 350
    
    """
    Classe permettant de gérer le robot\n
    :Nota: Classement pouvant etre totalement refaite. Les attributs orientations et positions sont requis pour la visualisation de la table
    \n\n
    """
    
    def __init__(self):
        self.position = point.Point(1000,1500)
        self.orientation = 0
        self.rayon = 350
        self.actionneur = {"hd": actionneur.Actionneur("hd"),
        "hg": actionneur.Actionneur("hg"),
        "bd": actionneur.Actionneur("bd"),
        "bg": actionneur.Actionneur("bg")} # TODO gérer ça dans la détection
        # Pour avoir l'angle
        # self.actionneur["hg"].angle

        log.logger.info('Création du robot')

    def setPosition(self, position):
        """
        Défini la position du robot

        :param position: Position du robot
        :type position: Point
        """
        self.position = position
        
    def setOrientation(self, orientation):
        """
        Défini l'orientation du robot

        :param orientation: Orientation du robot
        :type orientation: float
        """
        self.orientation = orientation
        
    def calculerRayon(self):
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
        
        #TODO lien avec la consigne de l'angle des bras
        angle = 0.7
        
        #[]ouais, on pourrait le mettre dans constantes..
        diam_original = math.sqrt(longueur_robot ** 2 + largeur_robot ** 2)
        
        #projection du bras sur x et y
        
        #[]c'est quoi la convention pour l'angle des bras ?
        #faudrait mettre un schema à deux balles pour que tout le monde soit d'accord.
        #moi j'aurais pensé à mettre angle = 0 vers l'avant du robot, sur l'axe y.
        proj_x = -longueur_bras*math.cos(angle)
        proj_y = longueur_bras*math.sin(angle)
        
        #[]la longueur est sur x, largeur sur y
        sommet_bras = outils_math.point.Point(longueur_robot/2 + proj_x, largeur_robot/2 + proj_y)
        sommet_robot = outils_math.point.Point(-longueur_robot/2, -largeur_robot/2)
        
        #longueur du segment entre le centre du robot avec les bras fermés et le sommet du bras
        #segment_centre_bras = math.sqrt(math.pow(sommet_bras.x, 2) + math.pow(sommet_bras.y, 2))
        
        #[] le diamètre mesuré (segment le plus long) doit etre pris entre deux extremités du robot.
        #là tu considères que le milieu du diamètre est le centre_original
        #en gros faut raisonner sur les diamètres, par sur les rayons ^^
        diam_avec_bras = math.sqrt((sommet_bras.x - sommet_robot.x) ** 2 + (sommet_bras.y - sommet_robot.y) ** 2)
        
        if diam_avec_bras > diam_original:
            self.rayon = diam_avec_bras/2
            
            #[] donc c'est presque ca :
            #return outils_math.point.Point((sommet_bras.x+sommet_robot.x)/2, (sommet_bras.y+sommet_robot.y)/2)
            
            #[] sauf que comme on renvoit un (delta x, delta y) pour modifier la position du centre
            #il faut pas oublier que le vrai robot est orienté, et donc il faut encore projeter :P
            
            #TODO lien avec l'orientation absolue du robot sur la table
            orientation = 0.3
            
            delta_x = - math.cos(orientation)*(sommet_bras.x+sommet_robot.x)/2 - math.sin(orientation)*(sommet_bras.y+sommet_robot.y)/2
            delta_y = - math.sin(orientation)*(sommet_bras.x+sommet_robot.x)/2 + math.cos(orientation)*(sommet_bras.y+sommet_robot.y)/2
            return outils_math.point.Point(delta_x,delta_y)
            
            #trololololo..
            #comme personne n'aime les projection, une bonne série de tests serait appréciée xD
            
        else:
            self.rayon = diam_original/2
            return outils_math.point.Point(0., 0.)