# -*- coding: utf-8 -*-

import os,sys
# Ajout de ../.. au path python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
import lib.log
log = lib.log.Log()

try:
    from graph_tool.all import *
except:
    log.logger.error("Vous devez installer graph-tool, plus d'informations sur le README")

from lib.outils_math.point import Point
from math import sqrt


class VisitorExample(AStarVisitor):

    def __init__(self, touched_v, touched_e, target):
        self.touched_v = touched_v
        self.touched_e = touched_e
        self.target = target

    def discover_vertex(self, u):
        self.touched_v[u] = True

    def examine_edge(self, e):
        self.touched_e[e] = True

    def edge_relaxed(self, e):
        if e.target() == self.target:
            raise StopSearch()

def AStar(Ndepart,Narrive):
    """
    algorithme A*, sur une table de jeu discrétisée "par cases"
    """
    
    #fonction heuristique : renvoit la distance restante supposée
    def h(n, Narrive):
        #test sur les robots adverses détéctés
        for r in centresRobotsA:
            if sqrt((posX[n] - r.x) ** 2 + (posY[n] - r.y) ** 2) < rayonRobotsA:
                #ignorer les noeuds en leur attribuant une distance heuristique infinie
                nCouleur[n] = "blue"
                return float('Inf')
            else:
                return sqrt((posX[n] - posX[Narrive]) ** 2 + (posY[n] - posY[Narrive]) ** 2)
    
    #réinitialisation des tables des noeuds et arêtes parcourus par A*
    touch_v = g.new_vertex_property("bool")
    touch_e = g.new_edge_property("bool")
    #A* : liste 
    dist, pred = astar_search(g, Ndepart, poids, VisitorExample(touch_v, touch_e, Narrive), heuristic=lambda n: h(n, Narrive))
    
    #VISU : réinitialisation de la largeur des arêtes, couleur des noeuds
    aLarg.a = 20.
    for e in g.edges():
        aCouleur[e] = "blue" if touch_e[e] else "black"
    #tracé du chemin
    v = Narrive
    chemin=[]
    while v != Ndepart:
        chemin.insert(0, Point(posX[v],posY[v]))
        nCouleur[v] = "orange"#VISU noeuds du chemin
        p = g.vertex(pred[v])
        #VISU : arêtes du chemin épaisses en rouge
        for e in v.out_edges():
            if e.target() == p:
                aCouleur[e] = "red"
                aLarg[e] = 100.
        v = p
    nCouleur[v] = "red"#VISU départ en rouge
    chemin.insert(0, Point(posX[v],posY[v]))
    return chemin