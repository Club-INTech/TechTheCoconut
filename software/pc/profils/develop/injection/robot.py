# -*- encoding:utf-8 -*-



"""
Ce module sert à initialiser le robot

"""

# ../../../
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

import lib.elements_jeu as elements_jeu
import lib.outils_math.point as point
import lib.robot as mod_robot

# Création du robot
robot = mod_robot.Robot()

robot.setPosition(point.Point(1000,1500))
robot.setOrientation(0)