# -*- coding: utf-8 -*-
import log
import lib.outils_math.point as point

log = log.Log()

class Robot:
    
    #:TODO: A modifier pour la valeur réel (voir a passer en  attribut d'instance
    rayon = 350
    
    """
    Classe permettant de gérer le robot
    :Nota: Classement pouvant etre totalement refaite. Les attributs orientations et positions sont requis pour la visualisation de la table
    """
    
    def __init__(self):
	self.position = point.Point(1000,1500)
	self.orientation = 0
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