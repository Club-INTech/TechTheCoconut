# -*- coding: utf-8 -*-

import sys
import os
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
import pygame
import threading

asserInstance = __builtin__.instance.asserInstance
strategieInstance = __builtin__.instance.strategieInstance
actionInstance = __builtin__.instance.actionInstance

#Ajout de ../ au path python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import lib.chargement_lib
log = lib.log.Log(__name__)

pygame.init()
screen = pygame.display.set_mode([100,100])
asserInstance.changerVitesse('translation', 1)
asserInstance.changerVitesse('rotation', 1)
actionInstance.changerVitesse(100)

while 42:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                print "Avance !"
                asserInstance.serieAsserInstance.ecrire("d")
                asserInstance.serieAsserInstance.ecrire(str(float(1000)))
            elif event.key == pygame.K_s:
                print "Recule !"
                asserInstance.serieAsserInstance.ecrire("d")
                asserInstance.serieAsserInstance.ecrire(str(float(-1000)))
            elif event.key == pygame.K_q:
                print "Tourne à gauche !"
                asserInstance.serieAsserInstance.ecrire("t")
                asserInstance.serieAsserInstance.ecrire(str(float(0)))
            elif event.key == pygame.K_d:
                print "Tourne à droite !"
                asserInstance.serieAsserInstance.ecrire("t")
                asserInstance.serieAsserInstance.ecrire(str(float(math.pi)))
            elif event.key == pygame.K_o:
                print "Actionneur hg vers l'extérieur"
                actionInstance.deplacer(160, ["hg"])
            elif event.key == pygame.K_p:
                print "Actionneur hg vers l'intérieur"
                actionInstance.deplacer(0, ["hg"])
            elif event.key == pygame.K_l:
                print "Actionneur bg vers l'extérieur"
                actionInstance.deplacer(160, ["bg"])
            elif event.key == pygame.K_m:
                print "Actionneur bg vers l'intérieur"
                actionInstance.deplacer(0, ["bg"])
            elif event.key == pygame.K_KP3:
                print "Actionneur hd vers l'extérieur"
                actionInstance.deplacer(160, ["hd"])
            elif event.key == pygame.K_KP1:
                print "Actionneur hg vers l'intérieur"
                actionInstance.deplacer(0, ["hd"])
            elif event.key == pygame.K_KP9:
                print "Actionneur bg vers l'extérieur"
                actionInstance.deplacer(160, ["bd"])
            elif event.key == pygame.K_KP7:
                print "Actionneur bg vers l'intérieur"
                actionInstance.deplacer(0, ["bd"])
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_z:
                print "N'avance plus"
                asserInstance.immobiliser()
            elif event.key == pygame.K_s:
                print "Ne recule plus"
                asserInstance.immobiliser()
            elif event.key == pygame.K_q:
                print "Ne tourne plus à gauche"
                asserInstance.immobiliser()
            elif event.key == pygame.K_d:
                print "Ne tourne plus à droite"
                asserInstance.immobiliser()
            elif event.key == pygame.K_o or event.key == pygame.K_p:
                print "Actionneur hg stop"
                actionInstance.stop()
            elif event.key == pygame.K_l or event.key == pygame.K_m:
                print "Actionneur bg stop"
                actionInstance.stop()
            elif event.key == pygame.K_KP3 or event.key == pygame.K_KP1:
                print "Actionneur hd stop"
                actionInstance.stop()
            elif event.key == pygame.K_KP9 or event.key == pygame.K_KP7:
                print "Actionneur bg stop"
                actionInstance.stop()