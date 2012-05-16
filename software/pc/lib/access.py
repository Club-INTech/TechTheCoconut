# -*- coding: utf-8 -*-

import __builtin__
import instance
from lib.outils_math.point import Point

t = __builtin__.instance.theta

def test():
    px = raw_input("x ?")
    py = raw_input("y ?")
    t.estAccessible(Point(float(px),float(py)))
    
test()