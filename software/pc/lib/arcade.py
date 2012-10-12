# -*- coding: utf-8 -*-
import instance
import __builtin__

import pygame
from pygame.locals import *

if hasattr(__builtin__.instance, 'asserInstance'):
    asserInstance = __builtin__.instance.asserInstance
if hasattr(__builtin__.instance, 'actionInstance'):
    actionInstance = __builtin__.instance.actionInstance
#if hasattr(__builtin__.instance, 'capteurInstance'):
    #capteurInstance = __builtin__.instance.capteurInstance
    
def arcade():
    asserInstance.serieAsserInstance.ecrire("arcade")
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
                
            #avancer
            if event.type == KEYDOWN and event.key == K_r:
                print "avance gauche"
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
                print "ouvrir bras gauche"
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
            
        #capteur = capteurInstance.mesurer()
        capteur = 9000
        if capteur < maxCapt and (consigneGauche > 0 or consigneDroite > 0):
            asserInstance.moteurGauche(0)
            asserInstance.moteurDroit(0)
        else :
            asserInstance.moteurGauche(consigneGauche)
            asserInstance.moteurDroit(consigneDroite)
arcade()