# -*- coding: utf-8 -*-

import sys
from sys import argv
import os
import __builtin__

# Ajout de ../ au path python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import lib.chargement_lib
log = lib.log.Log(__name__)

# Création du robot
# WARNING robotInstance est une variable globale qui instancie la classe Robot
__builtin__.robotInstance = lib.robot.Robot()

robotInstance.setPosition(lib.outils_math.point.Point(1000,1500))
robotInstance.setOrientation(0)

try:
    from IPython.Shell import IPShellEmbed
    ipshell = IPShellEmbed()
    ipshell()
except:
    log.logger.error("La dépendance Ipython n'est pas installée. Taper sudo apt-get install ipython")

