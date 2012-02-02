# -*- coding: utf-8 -*-

"""
il faudra importer :
from lib.recherche_chemin.rechercheChemin import *

voir utiliseRechercheChemin pour exemple
"""

import marshal
import os,sys
# Ajout de ../.. au path python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
import lib.log
log = lib.log.Log()

from lib.outils_math.collisions import *
from lib.outils_math.point import Point
from lib.outils_math.rectangle import Rectangle
from lib.recherche_chemin.astar import *
from math import sqrt

#TODO lien avec constantes dans profil
tableLargeur = 200.
tableLongueur = 300.
coteRobot = 50.
rayonRobotsA = 50.

#TODO lien avec éléments de jeu
listeObjets=[Rectangle(100,70,0.,10.,10.),Rectangle(-50,100,0.7,10.,60.)]

""" synthaxe :
import lib.elements_jeu
from lib.carte import Carte
carte=Carte()
carte.reglettesEnBois[i].rectangle. #3
carte.totems[i].rectangle. #1
carte.palmiers[i].rectangle. #0
.x
.y
.t
.wx
.wy
"""

#déclaration du graphe, avec tables de propriétés : structure de données optimale pour les noeuds
g = Graph(directed=False)
posX = g.new_vertex_property("int")
posY = g.new_vertex_property("int")
poids = g.new_edge_property("double")

Nstruct = 2 #nb de noeuds de structure placés à la racine. il servent à pointer d'autres noeuds

pas = 10 # pas en mm
longueur = int(tableLongueur/pas)
largeur = int(tableLargeur/pas)
#centrage de l'axe des abscisses
axeX=-(tableLongueur)/2
axeY=0#-(0-pas)/2

#élargissement des objets : les noeuds concernent les zones accessibles par le centre du robot
largeurRobot=coteRobot*1.414#sqrt(2)
for o in listeObjets:
    o.wx += largeurRobot
    o.wy += largeurRobot

def rechercheChemin(depart,arrive,centresRobotsA):
    """
    fonction de recherche de chemin, utilisant le meilleur algorithme codé
    """
    print "recherche chemin"
    
    #réinitialisation des property map de couleurs
    global aCouleur
    global aLarg
    global nCouleur
    aCouleur = g.new_edge_property("string")
    aLarg = g.new_edge_property("double")
    nCouleur = g.new_vertex_property("string")
    
    
    #retrouve les noeuds arguments
    for v in find_vertex(g, posX, depart.x):
        if posY[v] == depart.y:
            Ndepart=v
    
    for v in find_vertex(g, posX, arrive.x):
        if posY[v] == arrive.y:
            Narrive=v
    
    #algorithme utilisé : A*
    #TODO : robot adverse fixé dans le graphe
    chemin=AStar(Ndepart,Narrive,centresRobotsA)
    
    #sortie
    print "chemin -->"
    for p in chemin:
        print "(" + str(p.x) + ", " + str(p.y) + ")"

def AStar(Ndepart,Narrive,centresRobotsA):
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
   
   
def chargeGraphe():
    print "chargement du graphe..."
    global g
    g=load_graph("sauv_g.xml")
    TposX=marshal.load(open("sauv_posX","rb"))
    TposY=marshal.load(open("sauv_posY","rb"))
    for k in range(len(TposX)):
        posX[g.vertex(k)]=TposX[k]
        posY[g.vertex(k)]=TposY[k]
    
def enregistreGraphe():    

    """
    génération des noeuds, avec positions
    et des arêtes, avec poids
    """
   
    print "création du graphe -->"

    #noeuds de structures, servant de pointeurs
    for k in range(Nstruct):
        g.add_vertex()
    k=Nstruct
    
    for objet in listeObjets:
        #ajoute 4 noeuds : les angles de l'objet rectangulaire
        for angle in RectangleToPoly(objet):
            g.add_vertex()
            posX[g.vertex(k)] = angle.x
            posY[g.vertex(k)] = angle.y
            for l in range(Nstruct,k):
                #teste les arêtes accessibles
                touche = False
                for rect in listeObjets:
                    if collisionSegmentPoly(angle,Point(posX[g.vertex(l)],posY[g.vertex(l)]),RectangleToPoly(rect)):
                        touche = True
                        break
                if not touche:
                    g.add_edge(g.vertex(k),g.vertex(l))
                    poids[g.edge(g.vertex(k),g.vertex(l))] = sqrt((posX[g.vertex(k)] - posX[g.vertex(l)]) ** 2 + (posY[g.vertex(k)] - posY[g.vertex(l)]) ** 2)
            k+=1
        
            
    
    print "enregistreGraphe -->"
    TposX=[]
    TposY=[]
    Tpoids=[]
    for v in g.vertices() :
        TposX.append(posX[v])
        TposY.append(posY[v])
        #Tpoids.append(poids[v])
    marshal.dump(TposX, open("sauv_posX", 'wb'))
    marshal.dump(TposY, open("sauv_posY", 'wb'))
    #marshal.dump(Tpoids, open("sauv_poids", 'wb'))
    g.save("sauv_g.xml")
    
def tracePDF(nom):
    #graph_draw(g, output=nom, pos=(posX,posY),vsize=5,vcolor=nCouleur, pin=True,penwidth=aLarg, eprops={"color": aCouleur})
    graph_draw(g, output=nom, pos=(posX,posY),vsize=5,pin=True)

enregistreGraphe()
for e in g.edges():
    print e
tracePDF("graphe_angles")