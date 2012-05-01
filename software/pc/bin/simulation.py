# -*- coding: utf-8 -*-

import sys
from sys import argv
import os
import __builtin__

# Ajout de ../ au path python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

__builtin__.simulation = True
import lib.chargement_lib
log = lib.log.Log(__name__)

try:
    from IPython.Shell import IPShellEmbed
    ipshell = IPShellEmbed()
    ipshell()
except:
    log.logger.error("La dépendance Ipython n'est pas installée. Taper sudo apt-get install ipython")

