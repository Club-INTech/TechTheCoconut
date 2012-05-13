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
import __builtin__
import instance
import threading

log = lib.log.Log(__name__)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

#import profils.develop.constantes


class Robot:
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
        if not hasattr(self, 'position'):
            self.position = point.Point(0, 400)
        if not hasattr(self, 'orientation'):
            self.orientation = 0
        if not hasattr(self, 'rayon'):
            self.rayon = 279
        if not hasattr(self, 'acquittement'):
            self.acquitemment = False
        if not hasattr(self, 'fin_translation'):
            self.fin_translation = False
        if not hasattr(self, 'fin_rotation'):
            self.fin_rotation = False
        if not hasattr(self, 'fin_recalage'):
            self.fin_recalage = False
        if not hasattr(self, 'est_arrete'):
            self.est_arrete = False
        if not hasattr(self, 'message'):
            self.message = "huuk"
        if not hasattr(self, 'new_message'):
            self.new_message = False
        
        self.mutex = threading.Lock()
        #self.mutex = __builtin__.instance.mutex
        
        # Pour avoir l'angle
        # self.actionneur["hg"].angle

        log.logger.info('Création du robot')
    
    def changeRayon(self, rayon):
        self.rayon = rayon
        
    def donneRayon(self):
        return self.rayon
        
    def getPosition(self):
        """
        Défini la position du robot

        :param position: Position du robot
        :type position: Point
        """
        self.mutex.acquire()
        position = self.position
        self.mutex.release()
        return position
    
    def setPosition(self, position):
        """
        Défini la position du robot

        :param position: Position du robot
        :type position: Point
        """
        self.mutex.acquire()
        self.position = position
        self.mutex.release()
        
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