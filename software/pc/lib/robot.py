# -*- coding: utf-8 -*-

import sys
import os
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

import log
import outils_math.point as point
import actionneur
import outils_math.point
import lib.log
import asservissement

log = lib.log.Log(__name__)
sys.path.append('../')

#import profils.develop.constantes


class Robot:
    
    #:TODO: A modifier pour la valeur réel (voir a passer en  attribut d'instance
    #rayon = 350
    """
    Classe permettant de gérer le robot\n
    :Nota: Classement pouvant etre totalement refaite. Les attributs orientations et positions sont requis pour la visualisation de la table
    \n\n
    """
    
    def __init__(self):
        #TODO
        # Convertir en attributs de classe et les initialiser que si non reconnus (hasattr)
        self.position = point.Point(1000,1500)
        self.orientation = 0
        self.rayon = 279
        self.acquitemment = True
        self.translation = True
        self.rotation = True
        self.recalage = False
        
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
        
    def demarer(self):#TODO : protocole pour la languette (démarrage du robot)
        """
        Fonction utilisée pour initialiser le robot
        """
        asser.ecrire("recal\n")
        asser.reponse = self.file_attente.get(lu)
        
    def stop(self) :
        """
        Arrête entièrement le robot (par exemple après les 90 secondes)
        #TODO ELLE NE FAIT RIEN POUR L'INSTANT
        """
        pass