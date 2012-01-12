# -*- coding: utf-8 -*-

import sys
import os

# Ajout de ../ au path python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import serie

class Visu_serie(serie.Serie):
    """
    Classe permettant de visualiser les messages passant par la liaison série
    """
    def __init__(self):
        pass