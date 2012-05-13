# -*- coding: utf-8 -*-

from outils_math.point import Point

class departInaccessible(Exception):
    def __init__(self, point):
        self.point = point
    def __repr__(self):
        return repr(self.point)

"""
try:
    raise departInaccessible(Point(2,5.0))
except departInaccessible as p:
    print 'le point de départ est inaccessible : ', p.point
"""