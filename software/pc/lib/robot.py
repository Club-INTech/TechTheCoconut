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

#import profils.develop.constantes

#log = log.Log()

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
        
    