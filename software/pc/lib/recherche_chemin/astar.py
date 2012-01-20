# -*- coding: utf-8 -*-

import os
import sys
# Ajout de ../ au path python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../math"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../profils/develop/injection/"))

import lib.elements_jeu
#from carte import Carte

"""
carte=Carte()
carte.reglettesEnBois.rectangle. #3
carte.totems.rectangle. #1
carte.palmiers.rectangle. #0
.x
.y
.t
.wx
.wy

carte = elements_jeu.carte
carte.totems[0] 
carte.palmiers[0]
carte.reglettesEnBois[0] 

.position.x
.position.y
.orientation
.longueur
.largeur


"""