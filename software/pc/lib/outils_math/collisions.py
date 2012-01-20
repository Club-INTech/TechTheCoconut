# -*- coding: utf-8 -*-

from point import Point
from vecteur import Vecteur
from math import cos,sin

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
    
def RectangleToPoly(rect):
    p4=Point(rect.x+rect.wx/2*cos(rect.t)+rect.wy/2*sin(rect.t),rect.y+rect.wx/2*sin(rect.t)-rect.wy/2*cos(rect.t))
    p3=Point(rect.x+rect.wy/2*sin(rect.t)-rect.wx/2*cos(rect.t),rect.y-rect.wy/2*cos(rect.t)-rect.wx/2*sin(rect.t))
    p2=Point(rect.x-rect.wx/2*cos(rect.t)-rect.wy/2*sin(rect.t),rect.y-rect.wx/2*sin(rect.t)+rect.wy/2*cos(rect.t))
    p1=Point(rect.x-rect.wy/2*sin(rect.t)+rect.wx/2*cos(rect.t),rect.y+rect.wy/2*cos(rect.t)+rect.wx/2*sin(rect.t))
    return [p1,p2,p3,p4]
    
def collisionPolyCase(poly,ctr,pas):
    #test sur les 4 angles de la case
    c1 = collisionPolyPoint(poly,Point(ctr.x-pas/2,ctr.y-pas/2))
    c2 = collisionPolyPoint(poly,Point(ctr.x+pas/2,ctr.y-pas/2))
    c3 = collisionPolyPoint(poly,Point(ctr.x+pas/2,ctr.y+pas/2))
    c4 = collisionPolyPoint(poly,Point(ctr.x-pas/2,ctr.y+pas/2))
    c5 = collisionPolyPoint(poly,Point(ctr.x,ctr.y))
    return c1 or c2 or c3 or c4 or c5