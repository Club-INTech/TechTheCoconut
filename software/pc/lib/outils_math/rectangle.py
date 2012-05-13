# -*- coding: utf-8 -*-

class Rectangle:
    """
    Classe permettant de définir un rectangle orienté dans R^2
    
    :param x: abscisse du centre
    :type x: float
    :param y: ordonnée du centre
    :type y: float
    :param t: angle d'orientation en radian, dans le sens direct par rapport à l'axe des abscisses
    :type t: float
    :param wx: largeur sur x
    :type wx: float
    :param wy: largeur sur y
    :type wy: float
    """
    def __init__(self, x, y, t, wx, wy):
        #position
        self.x = x
        self.y = y
        #angle theta : orientation
        self.t = t
        #largeur sur x et y
        self.wx = wx
        self.wy = wy
        
    def __repr__(self):
        return '[centre:(' + str(self.x) + ',' + str(self.y) + ');orient:' + str(self.t) + ';larg:(' + str(self.wx) + ',' + str(self.wy) + ')]'