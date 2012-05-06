# -*- coding: utf-8 -*-

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
from outils_math.point import Point

import pygame
from pygame.locals import *


if hasattr(__builtin__.instance, 'asserInstance'):
    asserInstance = __builtin__.instance.asserInstance
if hasattr(__builtin__.instance, 'actionInstance'):
    actionInstance = __builtin__.instance.actionInstance

def arcade():
    print "echap ou ? pour sortir |  avancer gauche : r  | avancer droite : i"
    print "  vitesse : w -> n    |  reculer gauche : f  | reculer droite : j"
    
    #position initiale du robot
    asserInstance.setPosition(Point(0,400))
    pygame.init()
    screen = pygame.display.set_mode([100,100])
    
    vitesse = 80
    while True:
        pygame.time.Clock().tick(40)
        for event in pygame.event.get():
            
            
            if (event.type == KEYDOWN and (event.key == K_QUESTION or event.key == K_ESCAPE)) or event.type == QUIT:
                break
                
            """
            #pour pc
            if event.type == KEYDOWN and event.key == K_r:
                asserInstance.moteurGauche(vitesse)
            if event.type == KEYDOWN and event.key == K_f:
                asserInstance.moteurGauche(-vitesse)
            
            if event.type == KEYUP and (event.key == K_r or event.key == K_f):
                asserInstance.moteurGauche(0)
                
            if event.type == KEYDOWN and event.key == K_i:
                asserInstance.moteurDroit(vitesse)
            if event.type == KEYDOWN and event.key == K_j:
                asserInstance.moteurDroit(-vitesse)
                
            if event.type == KEYUP and (event.key == K_i or event.key == K_j):
                asserInstance.moteurDroit(0)
                
                
            if event.type == KEYDOWN and event.key == K_x:
                vitesse = 50
            if event.type == KEYDOWN and event.key == K_c:
                vitesse = 80
            if event.type == KEYDOWN and event.key == K_v:
                vitesse = 120
            if event.type == KEYDOWN and event.key == K_b:
                vitesse = 150
            if event.type == KEYDOWN and event.key == K_n:
                vitesse = 200
            """
            
            #pour bande arcade !
            
            if event.type == KEYDOWN and event.key == K_UP:
                asserInstance.moteurDroit(vitesse)
                
            if event.type == KEYDOWN and event.key == K_DOWN:
                asserInstance.moteurDroit(-vitesse)
                
            if event.type == KEYDOWN and event.key == K_r:
                asserInstance.moteurGauche(vitesse)
                
            if event.type == KEYDOWN and event.key == K_f:
                asserInstance.moteurGauche(-vitesse)
                
            if event.type == KEYUP and (event.key == K_r or event.key == K_f):
                asserInstance.moteurGauche(0)
                
            if event.type == KEYUP and (event.key == K_UP or event.key == K_DOWN):
                asserInstance.moteurDroit(0)
                
            if event.type == KEYDOWN and event.key == K_LCTRL:
                vitesse = 50 
            if event.type == KEYDOWN and event.key == K_LALT:
                vitesse = 80
            if event.type == KEYDOWN and event.key == K_SPACE:
                vitesse = 120
            if event.type == KEYDOWN and event.key == K_LSHIFT:
                vitesse = 150
            if event.type == KEYDOWN and event.key == K_z:
                vitesse = 200
            if event.type == KEYDOWN and event.key == K_x:
                vitesse = 250
                
arcade()