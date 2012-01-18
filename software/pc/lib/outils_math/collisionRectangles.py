# -*- coding: utf-8 -*-

"""
fonction de collision entre deux rectangles
implémentée d'après la source :
http://forum.games-creators.org/attachment.php?attachmentid=639&d=1274430280
"""

from math import cos,sin,tan,pi

class Rectangle:
   #classe de rectangles orientés pour le calcul de collision
    def __init__(self, x, y, t, wx, wy):
        #position
        self.x = x
        self.y = y
        #angle theta : orientation
        self.t = t
        #largeur sur x et y
        self.wx = wx
        self.wy = wy
        
def collisionNonOriente(r1,r2,o):
    return not (  (r2.x > r1.x + (r1.wx + r2.wx)/2) or (r1.x > r2.x + (r1.wx + r2.wx)/2) or (r2.y > r1.y + (r1.wy + r2.wy)/2) or (r1.y > r2.y + (r1.wy + r2.wy)/2)  )

"""   
def collisionNonOriente(r1,r2,o):
    #collision entre deux rectangles parallèles, dans un repère orienté selon o
    if o==0 :
        return not (  (r2.x > r1.x + (r1.wx + r2.wx)/2) or (r1.x > r2.x + (r1.wx + r2.wx)/2) or (r2.y > r1.y + (r1.wy + r2.wy)/2) or (r1.y > r2.y + (r1.wy + r2.wy)/2)  )
    else :
        return not (  (r1.y - r1.wx/2 > r2.y + r2.wx/2) or (r2.y - r2.wx/2 > r1.y + r1.wx/2) or (r1.y - r1.wx/2 > r2.y + r2.wx/2) or (r2.y - r2.wx/2 > r1.y + r1.wx/2) )
    #else if o > -pi/2 and o < 0 :
        #return not (  (r1.y - r1.wx/2 > r2.y + r2.wx/2) or (r2.y - r2.wx/2 > r1.y + r1.wx/2) ) #pas r1.wx, mais avec coeff
    
"""
    
def rectExt(r,o):
    #rectangle extérieur (ie exinscrit) au rectangle r, dans la base selon l'orientation o
    return Rectangle(r.x,r.y,o,r.wx*abs(cos(o))+r.wy*abs(sin(o)),r.wx*abs(sin(o))+r.wy*abs(cos(o)))

def collision(r1,r2):
    return (  collisionNonOriente(r1,rectExt(r2,r1.t),r1.t) and collisionNonOriente(r2,rectExt(r1,r2.t),r2.t) )