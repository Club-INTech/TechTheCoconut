# -*- coding: utf-8 -*-

import sys
import os
import termios
import tty
import select
import time
import threading

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

class Action(threading.Thread):
    def init(self, action, valeur):
        threading.Thread.__init__(self)
        
    def run(self):
        exec('strategieInstance.gestion'+action+'('+str(valeur)+')')

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
                            Action(Avancer, 500)
                            #strategieInstance.gestionAvancer(10)
                        elif c == "f": # bas
                            Action(Avancer, -500)
                            #strategieInstance.gestionAvancer(-10)
                        elif c == "g": # droite
                            Action(Tourner, 0)
                            #strategieInstance.gestionTourner(0)
                        elif c == "d": # gauche
                            Action(Tourner, math.pi)
                            #strategieInstance.gestionTourner(math.pi)
                        elif c == '\x1b':         # x1b is ESC
                                break
                        else:
                            strategieInstance.immobiliser()
                time.sleep(0.01)

finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
