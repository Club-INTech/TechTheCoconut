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
import capteur

import pygame
from pygame.locals import *

import lolilol

if hasattr(__builtin__.instance, 'asserInstance'):
    asserInstance = __builtin__.instance.asserInstance
if hasattr(__builtin__.instance, 'actionInstance'):
    actionInstance = __builtin__.instance.actionInstance
if hasattr(__builtin__.instance, 'capteurInstance'):
    capteurInstance = __builtin__.instance.capteurInstance
    
def arcade():
    maxCapt = 600
    consigneGauche = 0
    consigneDroite = 0
    correction = 0
    print "echap ou ? pour sortir |  avancer gauche : r  | avancer droite : i"
    print "   vitesse : w -> n    |  reculer gauche : f  | reculer droite : j"
    print "ouvrir/fermer bras gauche : q/z  |  ouvrir/fermer bras droit : m/o"
    
    pygame.init()
    screen = pygame.display.set_mode([100,100])
    vitesse = 100
    while True:
        pygame.time.Clock().tick(40)
        for event in pygame.event.get():
            
            if (event.type == KEYDOWN and (event.key == K_QUESTION or event.key == K_ESCAPE)) or event.type == QUIT:
                break
                
            #pour pc
            
            #avancer
            if event.type == KEYDOWN and event.key == K_r:
                consigneGauche = vitesse + correction
            if event.type == KEYDOWN and event.key == K_i:
                consigneDroite = vitesse
                    
            #reculer
            if event.type == KEYDOWN and event.key == K_f:
                consigneGauche = -vitesse - correction
            if event.type == KEYDOWN and event.key == K_j:
                consigneDroite = -vitesse
                
            #stopper
            if event.type == KEYUP and (event.key == K_r or event.key == K_f):
                consigneGauche = 0
            if event.type == KEYUP and (event.key == K_i or event.key == K_j):
                consigneDroite = 0
                
            #vitesses
            if event.type == KEYDOWN and event.key == K_w:
                vitesse = 50
            if event.type == KEYDOWN and event.key == K_x:
                vitesse = 80
            if event.type == KEYDOWN and event.key == K_c:
                vitesse = 100
            if event.type == KEYDOWN and event.key == K_v:
                vitesse = 120
            if event.type == KEYDOWN and event.key == K_b:
                vitesse = 150
            if event.type == KEYDOWN and event.key == K_n:
                vitesse = 200
                
            #bras
            if event.type == KEYDOWN and event.key == K_m:
                actionInstance.deplacer(160, ["hd","bd"])
            if event.type == KEYDOWN and event.key == K_o:
                actionInstance.deplacer(0, ["hd","bd"])
            if event.type == KEYDOWN and event.key == K_q:
                actionInstance.deplacer(160, ["hg","bg"])
            if event.type == KEYDOWN and event.key == K_z:
                actionInstance.deplacer(0, ["hg","bg"])
            if event.type == KEYUP:
                if event.key == K_q or event.key == K_z:
                    actionInstance.stop(["hg","bg"])
                if event.key == K_o or event.key == K_m:
                    actionInstance.stop(["hd","bd"])
            
            if event.type == KEYDOWN and event.key == K_g:
                correction = int(raw_input("correction ?"))
            
            """
            #pour bande arcade !
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    lolilol.son("bruitages/vroom.mp3")
                    asserInstance.moteurDroit(vitesse)
                if event.key == K_DOWN:
                    lolilol.son("bruitages/klaxon_tour_de_france.mp3")
                    asserInstance.moteurDroit(-vitesse)
                if event.key == K_r:
                    lolilol.son("bruitages/vroom.mp3")
                    asserInstance.moteurGauche(vitesse)
                if event.key == K_f:
                    lolilol.son("bruitages/klaxon_tour_de_france.mp3")
                    asserInstance.moteurGauche(-vitesse)
                if event.key == K_LCTRL:
                    lolilol.son("bruitages/freiner.MP3")
                    vitesse = 50 
                if event.key == K_LALT:
                    vitesse = 80
                if event.key == K_SPACE:
                    vitesse = 120
                if event.key == K_LSHIFT:
                    vitesse = 150
                if event.key == K_z:
                    vitesse = 200
                if event.key == K_x:
                    lolilol.son("bruitages/klaxon_tour_de_france.mp3")
                    vitesse = 250
                
                if event.key == K_RIGHT:
                    lolilol.son("bruitages/klaxon_fun.mp3")
                    actionInstance.deplacer(160, ["hd","bd"])
                if event.key == K_LEFT:
                    lolilol.son("bruitages/klaxon_fun.mp3")
                    actionInstance.deplacer(0, ["hd","bd"])
                if event.key == K_d:
                    lolilol.son("bruitages/klaxon_camion.mp3")
                    actionInstance.deplacer(160, ["hg","bg"])
                if event.key == K_g:
                    lolilol.son("bruitages/klaxon_camion.mp3")
                    actionInstance.deplacer(0, ["hg","bg"])
                
            if event.type == KEYUP:
                if (event.key == K_r or event.key == K_f):
                    asserInstance.moteurGauche(0)
                if(event.key == K_UP or event.key == K_DOWN):
                    asserInstance.moteurDroit(0)
                    
                if event.key == K_d or event.key == K_g:
                    actionInstance.stop(["hg","bg"])
                if event.key == K_LEFT or event.key == K_RIGHT:
                    actionInstance.stop(["hd","bd"])
            """
             
        capteur = capteurInstance.mesurer()    
        if capteur < maxCapt and (consigneGauche > 0 or consigneDroite > 0):
            asserInstance.moteurGauche(0)
            asserInstance.moteurDroit(0)
        else :
            asserInstance.moteurGauche(consigneGauche)
            asserInstance.moteurDroit(consigneDroite)
arcade()