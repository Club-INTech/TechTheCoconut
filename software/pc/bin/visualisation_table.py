# -*- coding: utf-8 -*-

import sys, os, threading
# Ajout de ../ au path python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import lib
from lib.visualisation.visu_table import Visu_table

vTable = Visu_table(False)
vTable.start()

