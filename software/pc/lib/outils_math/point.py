# -*- coding: utf-8 -*-

class Point:
    """
    Classe permettant de définir un point mathématique dans R^2 et les opérations usuelles sur les points dans R^2
    
    :param x: abscisse
    :type x: float
    :param y: ordonnée
    :type y: float
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        