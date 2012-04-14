# -*- coding: utf-8 -*-

import sys
from sys import argv
import os
import __builtin__
import lib.instance

import lib.outils_math.point as point

# Ajout de ../ au path python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import lib.chargement_lib
log = lib.log.Log(__name__)

couleur = __builtin__.constantes["couleur"]

# Import d'un timer et du jumper
timer       = lib.timer.Timer()
jumper      = lib.jumper.Jumper()
strategie   = lib.strategie.Strategie()
asserv      = __builtin__.instance.asserInstance
robot       = lib.robot.Robot()
script      = __builtin__.instance.scriptInstance
actionneur  = __builtin__.instance.actionInstance

# On attend la mise en position du Jumper pour lancer le recalage
log.logger.info("Robot en attente du jumper pour recalage")
jumper.demarrerRecalage()
log.logger.info("Lancement du recalage...")

#Lancement du recalage

try :
    asserv.recalage()
except :
    log.logger.error("Impossible de lancer le recalage")
    
    
# On attends le réenlèvement du jumper
log.logger.info("Le recalage a été effectué")
jumper.scruterDepart()
log.logger.info("Le Jumper a été retiré. Lancement de la stratégie")

# C'est parti
strategie.gestion_avancer(300)
actionneur.deplacer(110, ["bg, bd"])

strategie.gestion_goTo(point.Point(-50, 445))
strategie.gestion_tourner(0)
actionneur.deplacer(150, ["bg, bd"])
strategie.gestion_avancer(640)
actionneur.deplacer(80, ["bg", "bd"])
strategie.gestion_goTo(point.Point(915, 915))
strategie.gestion_tourner(0)
strategie.gestion_avancer(150)
actionneur.deplacer(150)
strategie.gestion_avancer(145)
strategie.gestion_avancer(-425)
actionneur.deplacer(20)

strategie.gestion_goTo(point.Point(860, 1590))
strategie.gestion_tourner(-1.571)
asserv.changerVitesse("translation",3)
strategie.gestion_avancer(-500.0)  # Pour l'enfoncer à fond
asserv.changerVitesse("translation",2)
strategie.gestion_avancer(1000)    # On se barre.





# ET BIM !


