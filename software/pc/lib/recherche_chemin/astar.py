# -*- coding: utf-8 -*-

import graph

# Ajout de ../ au path python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Astar(graph.Graph):
    """
    Classe implémentant l'algorithme A* pour la recherche de chemin
    """
    def __init__(self):
        graph.Graph.__init__(self)