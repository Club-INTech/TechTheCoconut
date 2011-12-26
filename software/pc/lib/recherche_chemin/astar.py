# -*- coding: utf-8 -*-

import graph

class Astar(graph.Graph):
    """
    Classe implémentant l'algorithme A* pour la recherche de chemin
    """
    def __init__(self):
        graph.Graph.__init__(self)