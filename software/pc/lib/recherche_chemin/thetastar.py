# -*- coding: utf-8 -*-

import graph

class Thetastar(graph.Graph):
    """
    Classe implémentant l'algorithme Theta* pour la recherche de chemin
    """
    def __init__(self):
        graph.Graph.__init__(self)