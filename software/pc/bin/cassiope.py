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
script      = __builtin__.instance.scriptInstance

# On attend la mise en position du Jumper pour lancer le recalage
jumper.demarrerRecalage()
log.logger.info("Attente du jumper...")
jumper.scruterDepart()
log.logger.warning("Le Jumper a été retiré. Lancement de script cassiope")

# On lance le script d'homologation
script.gestionScripts(script.pipeau_cassiope)

# ET BIM !


