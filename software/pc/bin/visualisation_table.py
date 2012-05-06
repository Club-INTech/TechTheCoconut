# -*- coding: utf-8 -*-

import sys, os, threading
# Ajout de ../ au path python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import lib

print lib.visualisation

vTable = lib.visualisation.Visu_table()
vTable.start()