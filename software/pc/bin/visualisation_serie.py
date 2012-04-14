# -*- coding: utf-8 -*-

import sys, os
# Ajout de ../ au path python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import lib
from lib.visualisation.visu_serie import Visu_serie


vSerie = Visu_serie()
vSerie.start()