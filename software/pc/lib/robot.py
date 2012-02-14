# -*- coding: utf-8 -*-

class Robot:
    
    rayon = 25 
    """
    Classe permettant de gérer le robot
    :TODO: Refaire  l'initialisation du robot; Basiquement la déclaration de position et d'orientation pourrait etre fait ailleurs (idée a développer)
    
    :param position: Position du robot
    :type position: Point
    
    :param orientation: Orientation du robot
    :type orientation: float
    """
    def __init__(self, position, orientation):
        self.position = position
        self.orientation = orientation