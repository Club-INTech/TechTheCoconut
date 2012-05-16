# -*- coding: utf-8 -*-

import sys
from sys import argv
import os
import __builtin__
import lib.instance
import time

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

# On attend la mise en position du Jumper pour lancer le recalage
log.logger.warning("Robot en attente du jumper pour recalage")
jumper.demarrerRecalage()
log.logger.info("Lancement du recalage...")

#Lancement du recalage

try :
    asserInstance.recalage()
except :
    log.logger.error("Impossible de lancer le recalage")
    
    
# On attends le réenlèvement du jumper
log.logger.info("Le recalage a été effectué")
jumper.scruterDepart()
log.logger.info("Le Jumper a été retiré. Lancement de la stratégie")


timer.lancer()

script.gestionScripts(script.totem00)
script.gestionScripts(script.bourrerCale)
script.gestionScripts(script.poussoir1)
script.gestionScripts(script.enfoncerPoussoir1)
"""
actionInstance.deplacer(0)
asserInstance.gestionAvancer(600)
asserInstance.gestionTourner(2)
asserInstance.gestionAvancer(250)


log.logger.debug("RAFFLER TOTEM 00")
script.gestionScripts(script.rafflerTotem00)
log.logger.debug("POUSSOIR 0")
script.gestionScripts(script.enfoncerPoussoir0)
log.logger.debug("POUSSOIR 1")
script.gestionScripts(script.enfoncerPoussoir0)
log.logger.debug("RAFFLER TOTEM 01")
script.gestionScripts(script.rafflerTotem01)
log.logger.debug("BOURRAGE CALE")
script.gestionScripts(script.bourrerCale)
"""




## C'est parti
#def debut() :
    ## NOTE DONE
    #if couleur == "v" :
        #asserInstance.avancer(300)
        #actionneur.deplacer(130, "bd")
        #actionneur.deplacer(100, "bg") # NOTE switch pour changer couleur
    #else :
        #asserInstance.avancer(300)
        #actionneur.deplacer(100, "bd")
        #actionneur.deplacer(130, "bg")
        
#def decharger() :
    ## NOTE DONE
    #if couleur == "v" :
        #actionneur.deplacer(80, ["bd", "bg"])
        #asserInstance.goTo(point.Point(830, 915))
        #asserInstance.tourner(0)
        #actionneur.deplacer(160, ["bg", "bd"])
        #asserInstance.avancer(270)
        #asserInstance.avancer(-270)
        #actionneur.deplacer(100, ["bg", "bd"])

    #else :
        #actionneur.deplacer(80, ["bd", "bg"])
        #asserInstance.goTo(point.Point(-830, 915))
        #asserInstance.tourner(3.14)
        #actionneur.deplacer(160, ["bg", "bd"])
        #asserInstance.avancer(270)
        #asserInstance.avancer(-270)
        #actionneur.deplacer(100, ["bg", "bd"])
        
#def farmerTotemHaut() :
    ## NOTE DONE
    #if couleur == "v" :
        #asserInstance.goTo(point.Point(-50, 445))
        #asserInstance.tourner(0)
        #actionneur.deplacer(150, ["bg, bd"])
        #asserInstance.avancer(640)
        #actionneur.deplacer(50, ["bg", "bd"])
        
    #else :
        #asserInstance.goTo(point.Point(50, 445))
        #asserInstance.tourner(3.14)
        #actionneur.deplacer(150, ["bg, bd"])
        #asserInstance.avancer(640)
        #actionneur.deplacer(50, ["bg", "bd"])
       
#def appuyerBouton(numero) :
    ## NOTE DONE 
    #if couleur == "v" and numero == 1 :
        #asserInstance.goTo(point.Point(880, 1590))
        #asserInstance.tourner(-1.571)
        #asserInstance.changerVitesse("translation",3)
        #asserInstance.avancer(-1000.0)
        #asserInstance.changerVitesse("translation",2)
        #asserInstance.avancer(200)
    
    #elif couleur == "v" and numero == 2 :
        #asserInstance.goTo(point.Point(-365, 1590))
        #asserInstance.tourner(-1.571)
        #asserInstance.changerVitesse("translation",3)
        #asserInstance.avancer(-1000.0)
        #asserInstance.changerVitesse("translation",2)
        #asserInstance.avancer(200)
        
    #elif couleur == "r" and numero == 1 :
        #asserInstance.goTo(point.Point(-880, 1590))
        #asserInstance.tourner(-1.571)
        #asserInstance.changerVitesse("translation",3)
        #asserInstance.avancer(-1000.0)
        #asserInstance.changerVitesse("translation",2)
        #asserInstance.avancer(200)

    #elif couleur == "r" and numero == 2 :
        #asserInstance.goTo(point.Point(365, 1590))
        #asserInstance.tourner(-1.571)
        #asserInstance.changerVitesse("translation",3)
        #asserInstance.avancer(-1000.0)
        #asserInstance.changerVitesse("translation",2)
        #asserInstance.avancer(200)
#def farmerTotemBas() :
    ##NOTE DONE
    #if couleur == "v" :
        #asserInstance.goTo(point.Point(-180,1470))
        #asserInstance.tourner(0)
        #actionneur.deplacer(160, ["bg", "bd"])
        #asserInstance.goTo(point.Point(545, 1490))
        #actionneur.deplacer(85, ["bg", "bd"])
    #else: 
        #asserInstance.goTo(point.Point(180,1470))
        #asserInstance.tourner(3.14)
        #actionneur.deplacer(160, ["bg", "bd"])
        #asserInstance.goTo(point.Point(-545, 1490))
        #actionneur.deplacer(85, ["bg", "bd"])
        
#def prendreDisquesCentre() :
    ##NOTE MAJ
    #if couleur == "v" :
        #actionneur.deplacer(90, ["bg", "bd"])
        #asserInstance.goTo(point.Point(705, 1345))
        #asserInstance.tourner(3.14)
        #asserInstance.avancer(1090)
        #asserInstance.tourner(1.921)
        #asserInstance.avancer(335.0)
        #asserInstance.tourner(0.00)
        #actionneur.deplacer(140, ["bg", "bd"])
        #asserInstance.avancer(1020.0)
        #actionneur.deplacer(80, ["bg", "bd"])
    #else :
        #actionneur.deplacer(90, ["bg", "bd"])
        #asserInstance.goTo(point.Point(-705, 1345))
        #asserInstance.tourner(0)
        #asserInstance.avancer(1090)
        #asserInstance.tourner(3.14-1.921)
        #asserInstance.avancer(335.0)
        #asserInstance.tourner(3.14)
        #actionneur.deplacer(140, ["bg", "bd"])
        #asserInstance.avancer(1020.0)
        #actionneur.deplacer(80, ["bg", "bd"])
        
##-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
##-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|

## Construction du script

#debut()
#farmerTotemHaut()

#decharger()

#appuyerBouton(1)
