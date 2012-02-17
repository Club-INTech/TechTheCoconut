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
        
    def calculerRayon(self): #TODO : calcul des coordonnées du nouveau centre
        """
        Modifie le rayon du cercle circonscrit au robot et retourne les coordonnées du nouveau centre par rapport au centre d'origine (bras rabattus).
        Le calcul ne se fait que sur un bras (inférieur droit dans le repère du robot) puisque le tout est symétrique.
        
        :param rayon_original:Rayon du robot avec les bras rabattu
        :type rayon_original: int
        :param longueur_bras: longueur des bras du robot
        :type longueur_bras: int
        :param largeur_robot: largueur du robot
        :type largeur_robot: int
        :param cote_robot: dimension du côté du robot
        :type cote_robot: int
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
        rayon_original = profils.develop.constantes.constantes["Coconut"]["rayon"]
        longueur_bras = profils.develop.constantes.constantes["Coconut"]["longueurBras"]
        largeur_robot = profils.develop.constantes.constantes["Coconut"]["largeur"]
        cote_robot = profils.develop.constantes.constantes["Coconut"]["coteRobot"]
        
        angle = raw_input("Donner l'angle entre bras et face avant du robot \n")
        
        #projection du bras sur x et y
        proj_x = -longueur_bras*math.cos(float(angle))
        proj_y = longueur_bras*math.sin(float(angle))
        
        sommet_bras = outils_math.point.Point(largeur_robot/2 + proj_x, cote_robot/2 + proj_y)
        
        #longueur du segment entre le centre du robot avec les bras fermés et le sommet du bras
        segment_centre_bras = math.sqrt(math.pow(sommet_bras.x, 2) + math.pow(sommet_bras.y, 2))
        
        if segment_centre_bras > rayon_original:
            self.rayon = (segment_centre_bras + rayon_original)/2
        
        else:
            self.rayon = rayon_original