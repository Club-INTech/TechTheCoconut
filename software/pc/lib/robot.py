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
    
    :angle : dictionnaire recessant les positions des quatres bras (hd, hg, bd, bg (h : haut, g : gauche, d : droite, g : gauche))
    """
    
    def __init__(self):
	self.position = point.Point(1000,1500)
	self.orientation = 0
	self.angle = {'hd' : 0, 'hg' : 0, 'bd' : 0, 'bg' : 0}
	self.angle['hd'] = actionneur.Actionneur.getAngle('hd')
    self.angle['hg'] = actionneur.Actionneur.getAngle('hg')
    self.angle['bd'] = actionneur.Actionneur.getAngle('bd')
    self.angle['bg'] = actionneur.Actionneur.getAngle('bg')
	
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
        
    def getAngle(self, actionneur):
    """
    Récupère l'angle actuel de l'actionneur passé en paramètre
    :actionneur: actionneur dont on récupère l'angle
    """
        self.angle['hd'] = actionneur.Actionneur.getAngle('hd')
        self.angle['hg'] = actionneur.Actionneur.getAngle('hg')
        self.angle['bd'] = actionneur.Actionneur.getAngle('bd')
        self.angle['bg'] = actionneur.Actionneur.getAngle('bg')
        
    def calculerRayon(self):
        