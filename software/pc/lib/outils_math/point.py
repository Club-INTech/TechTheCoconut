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
    
    def __repr__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ')'
        
    def __add__(self,other):
        return Point(self.x + other.x, self.y + other.y)
        
    def __sub__(self,other):
        return Point(self.x - other.x, self.y - other.y)
    
    def __mul__(self,other):
        return Point(self.x*other, self.y*other)
    
    def __str__(self) :
        return "("+str(self.x)+"," + str(self.y) + ")"
        
    def to_list(self):
        return [self.x, self.y]