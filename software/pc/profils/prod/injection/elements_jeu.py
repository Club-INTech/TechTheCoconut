# -*- encoding:utf-8 -*-



"""
Ce module set à placer tous les élements de jeu


"""
# ../../../
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath("../"))))

import lib.elements_jeu as elements_jeu
import lib.math.point as point

point1 = point.Point(5,2)

totem1 = elements_jeu.Totem(point1)

