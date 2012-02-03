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
    #un polygone doit etre défini par une liste de sommets (points), dans le sens inverse des aiguilles d'une montre
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
    return c1 or c2 or c3 or c4
    
def collisionSegmentPoly(a,b,poly):
    poly.append(poly[0])#pour boucler le polygone
    touche=False
    for i in range(len(poly)-1):
        c = poly[i]
        d = poly[i+1]
        
        if collisionSegmentSegment(a,b,c,d):
            touche=True
            break
    #pour ajouter un segment central, qui supprimera les arêtes interieures (simplifié pour un rectangle)
    c=Point(0.375*poly[0].x+0.375*poly[1].x+0.125*poly[2].x+0.125*poly[3].x,0.375*poly[0].y+0.375*poly[1].y+0.125*poly[2].y+0.125*poly[3].y)
    d=Point(0.125*poly[0].x+0.125*poly[1].x+0.375*poly[2].x+0.375*poly[3].x,0.125*poly[0].y+0.125*poly[1].y+0.375*poly[2].y+0.375*poly[3].y)
    if collisionSegmentSegment(a,b,c,d):
        touche=True
    return touche
    
def collisionSegmentSegment(a,b,c,d):
    if (a.x==c.x and a.y==c.y) or (a.x==d.x and a.y==d.y) or (b.x==c.x and b.y==c.y) or  (b.x==d.x and b.y==d.y):
        return False
    else:
        denom  = (d.y-c.y) * (b.x-a.x) - (d.x-c.x) * (b.y-a.y)
        numera = (d.x-c.x) * (a.y-c.y) - (d.y-c.y) * (a.x-c.x)
        numerb = (b.x-a.x) * (a.y-c.y) - (b.y-a.y) * (a.x-c.x)
        eps=0.000001

        if (abs(numera) < eps and abs(numerb) < eps and abs(denom) < eps):
            #droites coïncidentes
            return False
            """
            #test d'intersection des deux segments colinéraires
            if (((c.x+d.x)/2-(a.x+b.x)/2) > (abs(c.x-d.x)/2+abs(a.x-b.x)/2)) or (((c.y+d.y)/2-(a.y+b.y)/2) > (abs(c.y-d.y)/2+abs(a.y-b.y)/2)) :
                return False
            else:
                return True
            """
        elif (abs(denom) < eps):
            #droites parallèles
            return False
        else :
            #point d'intersection
            mua = numera / denom
            mub = numerb / denom
            #inclu dans les deux segments ?
            if (mua <= 0 or mua >= 1 or mub <= 0 or mub >= 1):
                return False
            else:
                return True
"""            
rect=Rectangle(-50.,100.,0.7,80.7,130.7)
poly=RectangleToPoly(rect)
a=Point(120.,140.)
hd=Point(rect.x-rect.wy/2*sin(rect.t)+rect.wx/2*cos(rect.t),rect.y+rect.wy/2*cos(rect.t)+rect.wx/2*sin(rect.t))
bd=Point(rect.x+rect.wx/2*cos(rect.t)+rect.wy/2*sin(rect.t),rect.y+rect.wx/2*sin(rect.t)-rect.wy/2*cos(rect.t))
hg=Point(rect.x-rect.wx/2*cos(rect.t)-rect.wy/2*sin(rect.t),rect.y-rect.wx/2*sin(rect.t)+rect.wy/2*cos(rect.t))
c=Point(0.375*poly[0].x+0.375*poly[1].x+0.125*poly[2].x+0.125*poly[3].x,0.375*poly[0].y+0.375*poly[1].y+0.125*poly[2].y+0.125*poly[3].y)
d=Point(0.125*poly[0].x+0.125*poly[1].x+0.375*poly[2].x+0.375*poly[3].x,0.125*poly[0].y+0.125*poly[1].y+0.375*poly[2].y+0.375*poly[3].y)
print collisionSegmentPoly(a,hd,RectangleToPoly(rect))
#print collisionSegmentSegment(a,hd,c,d)
print collisionSegmentSegment(a,hd,bd,hd)
#print "(" + str(bd.x) + ", " + str(bd.y) + ") | ("+ str(hd.x) + ", " + str(hd.y) + ")"
"""