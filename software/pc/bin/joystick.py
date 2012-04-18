# -*- coding: utf-8 -*-

import sys
import os
import termios
import tty
import select
import time

import asservissement
import outils_math
import robot
import recherche_chemin.thetastar
import script
import time
import serial
import instance
import __builtin__
import math


asserInstance = __builtin__.instance.asserInstance
strategieInstance = __builtin__.instance.strategieInstance
actionInstance = __builtin__.instance.actionInstance

# Ajout de ../ au path python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import lib.chargement_lib
log = lib.log.Log(__name__)

def isData():
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

old_settings = termios.tcgetattr(sys.stdin)
try:
        tty.setcbreak(sys.stdin.fileno())

        while 42:
                if isData():
                        c = sys.stdin.read(1)
                        print c
                        if c == "r": # haut
                            strategieInstance.gestionAvancer(10)
                        elif c == "f": # bas
                            strategieInstance.gestionAvancer(-10)
                        elif c == "g": # droite
                            strategieInstance.gestionTourner(0)
                        elif c == "d": # gauche
                            strategieInstance.gestionTourner(math.pi)
                        elif c == '\x1b':         # x1b is ESC
                                break
                time.sleep(0.01)

finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
