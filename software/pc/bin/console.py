# -*- coding: utf-8 -*-

import sys
from sys import argv
import os

# Ajout de ../ au path python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import lib.chargement_lib
log = lib.log.Log(__name__)

#try:

print "############################\n###########################\n"
print "#1"
from IPython.Shell import IPShellEmbed
print "#2"
ipshell = IPShellEmbed()
print "#3"
ipshell()
#except:
    #log.logger.error("La dépendance Ipython n'est pas installée. Taper sudo apt-get install ipython")

