# -*- coding: utf-8 -*-

import sys
from sys import argv
import os
import __builtin__
import lib.instance
import time

def afficherwelcome() :
    print "  *************************************************"
    print "  ***          R E - B I E N V E N U E          ***"
    print "  ***      D A N S    L A    C O N S O L E      ***"
    print "  ***     D U   C L U B   S O P A L ' I N T     ***"
    print "  *************************************************"
    
def afficheraide() :
    print "Un peu d'aide pour les n00bs....."
    print " Raffler totem :: 00 | 01 | 10"
    print " Boutons pouss ::  0 | 1"
    print " Bourrer Cale  :: bc"
    print " Vider Ennemi  :: e "
    
# Ajout de ../ au path python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import lib.chargement_lib
log = lib.log.Log(__name__)

# Import d'un timer et du jumper
timer       = lib.timer.Timer()
jumper      = __builtin__.instance.jumperInstance
strategie   = __builtin__.instance.strategieInstance
asserInstance      = __builtin__.instance.asserInstance
actionInstance     = __builtin__.instance.actionInstance
script      = __builtin__.instance.scriptInstance

#Lancement du recalage
try :
    asserInstance.recalage()
except :
    print 'Impossible de lancer le recalage'
    
afficherwelcome()
    
stop = False
while not stop :
    action = raw_input ("?> ")
    
    if action == "00" :
        action = "rafflerTotem00"
    elif action == "01" :
        action = "rafflerTotem01"
    elif action == "10" :
        action = "rafflerTotem10"
    elif action == "p0" :
        action = "enfoncerPoussoir0"
    elif action == "p1" :
        action = "enfoncerPoussoir1"
    elif action == "bc" :
        action = "bourrerCale"
    elif action == "e" :
        action = "viderCaleEnnemi"
        
    elif action == "g1" :
        action = "test_goto1"
    elif action == "g2" :
        action = "test_goto2"
    elif action == "g3" :
        action = "test_goto3"
    elif action == "g4" :
        action = "test_goto4"
        
    elif action == "!" :
        stop = True
        continue
    elif action == "" :
        continue
    elif action == "?" :
        afficheraide()
    
    try :
        exec("script.gestionScripts(script." + action + ")" )
    except :
        print "Erreur fatale lors du lancement de " + action + ". Arrêt."


