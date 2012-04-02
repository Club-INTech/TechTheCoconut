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
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

#import profils.develop.constantes


class Robot:
    
    #:TODO: A modifier pour la valeur réel (voir a passer en  attribut d'instance
    #rayon = 350
    """
    Classe permettant de gérer le robot\n
    :Nota: Classement pouvant etre totalement refaite. Les attributs orientations et positions sont requis pour la visualisation de la table
    :param acq*: Permet de vérifier les acquitements qui arrivent en boucle
    :type acq*: Booleen
    :param position: Position du robot mise à jour en permanance via la série
    :type position: math.Point
    :param acquitement, fin_*: Permet de surveiller les acquitements. Mis à jour par serie_acquisition.py et asservissement.py
    :type cquitement, fin_*: Booleen
    :param message: Reçois tous les autres messages non filtrer par serie_acquisition.py
    :type message: string
    :param new_message: Permet de savoir quand la variable message est mise à jour
    ;type new_message: Booleen
    \n\n
    """
    
    def __init__(self):
        #TODO
        # Convertir en attributs de classe et les initialiser que si non reconnus (hasattr)
        self.position = point.Point(0,400)
        self.orientation = 0
        self.rayon = 279
        self.acquitemment = False
        self.fin_translation = False
        self.fin_rotation = False
        self.fin_recalage = False
        self.est_arrete=False
        self.message = "huuk"
        self.new_message = False
        self.acqA = False
        self.acqB = False
        
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
        
    def demarrer(self):#TODO : protocole pour la languette (démarrage du robot)
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