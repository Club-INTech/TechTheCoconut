# -*- coding: utf-8 -*-

import sys
import os

# Ajout de ../ au path python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import lib

from IPython.Shell import IPShellEmbed
ipshell = IPShellEmbed()
ipshell()

print constantes
