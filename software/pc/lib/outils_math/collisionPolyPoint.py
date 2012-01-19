# -*- coding: utf-8 -*-

from point import Point
from vecteur import Vecteur

def collisionPolyPoint(poly,p):
    poly.append(poly[0])
    for i in range(len(poly)-1):
        a = poly[i]
        b = poly[i+1]
        d=Vecteur(a,b)
        t=Vecteur(a,p)
        if (d.dx*t.dy - d.dy*t.dx < 0):
            return False
    return True