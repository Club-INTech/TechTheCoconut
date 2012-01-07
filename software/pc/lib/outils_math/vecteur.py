# -*- coding: utf-8 -*-

import point
import math

class Vecteur:
    """
    Classe permettant de définir un vecteur mathématique dans R^2 et les opérations usuelles sur les vecteurs dans R^2
    
    :param a: 1er point
    :type a: Point
    :param b: 2ème point
    :type b: Point
    """
    def __init__(self, a, b):
        self.dx = b.x - a.x
        self.dy = b.y - a.y
    
    def norme(self):
        """
        :rtype: float
        :return: norme euclidienne du vecteur
        """
        return math.sqrt(self.dx ** 2 + self.dy ** 2)
    
    def angle(self):
        """
        :rtype: float
        :return: angle orienté en radians entre le vecteur et l'axe des abscisses
        """
        return Math.atan2(self.dy, self.dx)