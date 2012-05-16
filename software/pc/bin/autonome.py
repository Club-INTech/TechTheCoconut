# -*- coding: utf-8 -*-

import sys
from sys import argv
import os
import __builtin__
import lib.instance

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
time.sleep(5)
#jumper.demarrerRecalage()
log.logger.info("Lancement du recalage...")

#Lancement du recalage

try :
    asserInstance.recalage()
except :
    log.logger.error("Impossible de lancer le recalage")
    
    
# On attends le réenlèvement du jumper
log.logger.warning("Le recalage a été effectué")
#jumper.scruterDepart()
log.logger.warning("Le Jumper a été retiré. Lancement de la stratégie")

farmage_ennemi = False

if not farmage_ennemi :
    actionInstance.deplacer(0)
    asserInstance.gestionAvancer(300)
    asserInstance.gestionTourner(2)
    asserInstance.gestionAvancer(200)
else :
    asserInstance.changerVitesse("translation", 3)
    success = asserInstance.gestionAvancer("1900", "auStopNeRienFaire")
    if success :
        script.gestionScripts(script.rafflerTotem10)


# Lancement de la stratégie.
strategie.lancer()
    
    
#script.gestionScripts(script.rafflerTotem00)
#script.gestionScripts(script.rafflerTotem01)
#script.gestionScripts(script.enfoncerPoussoir0)
#script.gestionScripts(script.enfoncerPoussoir1)
#script.gestionScripts(script.homologation)


# ET BIM !


