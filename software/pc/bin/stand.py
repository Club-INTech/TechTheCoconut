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

while "Sopal'INT":
    #Lancement du recalage
    asserInstance.recalage()
    script.gestionScripts(script.torine00)
    script.gestionScripts(script.torine01)