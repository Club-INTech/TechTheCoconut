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
from lib.outils_math.polygone import polygone
from lib.recherche_chemin.astar import *
from math import sqrt

#TODO lien avec constantes dans profil
tableLargeur = 200.
tableLongueur = 300.
coteRobot = 50.
rayonRobotsA = 50.
nCotesRobotsA = 6#approximation hexagonale

#TODO lien avec éléments de jeu
listeObjets=[Rectangle(100.,70.,0.,10.,10.),Rectangle(-50.,100.,0.7,10.,60.),Rectangle(120.,230.,0.4,60.,10.)]

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
posX = g.new_vertex_property("double")
posY = g.new_vertex_property("double")
poids = g.new_edge_property("double")

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
    
    
    #création des robots adverses
    robotsA=[]
    for centre in centresRobotsA:
        robotsA.append(polygone(centre,rayonRobotsA,nCotesRobotsA))
        
    
    k=g.num_vertices()
    for robotA in robotsA:
        #ajoute les noeuds des sommets du polygone représentant le robot adverse
        for angle in robotA:
            g.add_vertex()
            posX[g.vertex(k)] = angle.x
            posY[g.vertex(k)] = angle.y
            for l in range(k):
                #teste les arêtes accessibles
                touche = False
                for rect in listeObjets:
                    if collisionSegmentPoly(angle,Point(posX[g.vertex(l)],posY[g.vertex(l)]),RectangleToPoly(rect)):
                        touche = True
                        break
                if not touche:
                    for robotA in centresRobotsA:
                        if collisionSegmentPoly(angle,Point(posX[g.vertex(l)],posY[g.vertex(l)]),polygone(robotA,rayonRobotsA,nCotesRobotsA)):
                            touche = True
                            break
                if not touche:
                    g.add_edge(g.vertex(k),g.vertex(l))
                    poids[g.edge(g.vertex(k),g.vertex(l))] = sqrt((posX[g.vertex(k)] - posX[g.vertex(l)]) ** 2 + (posY[g.vertex(k)] - posY[g.vertex(l)]) ** 2)
            k+=1
        
            
    #supprime les arêtes du graphe initial en collision avec les polygones des robots adverses
    for e in g.edges() :
        p1=Point(posX[e.source()],posY[e.source()])
        p2=Point(posX[e.target()],posY[e.target()])
        touche = False
        for rect in listeObjets:
            if collisionSegmentPoly(p1,p2,RectangleToPoly(rect)):
                touche = True
                break
        if not touche:
            for robotA in robotsA:
                if collisionSegmentPoly(p1,p2,robotA):
                    touche = True
                    break
        if touche :
            g.remove_edge(e)
    
    
    
    
    #test de l'accessibilité des positions de départ et d'arrivée
    touche_td = False
    for objet in listeObjets:
        if collisionPolyPoint(RectangleToPoly(objet),depart):
            touche_td = True
            break
        if not touche_td:
            for robotA in robotsA:
                if collisionPolyPoint(robotA,depart):
                    touche_td = True
                    break
    if touche_td :
        print "la position de départ est inaccessible !"
    else :
        touche_ta = False
        for objet in listeObjets:
            if collisionPolyPoint(RectangleToPoly(objet),arrive):
                touche_ta = True
                break
            if not touche_ta:
                for robotA in robotsA:
                    if collisionPolyPoint(robotA,arrive):
                        touche_ta = True
                        break
        if touche_ta :
            print "la position d'arrivée est inaccessible !"
        else :
            #créations des noeuds arguments et de leurs arêtes
            Ndepart=g.add_vertex()
            posX[Ndepart] = depart.x
            posY[Ndepart] = depart.y
            Narrive=g.add_vertex()
            posX[Narrive] = arrive.x
            posY[Narrive] = arrive.y
            for l in range(g.num_vertices()-2):
                #teste les arêtes accessibles
                touche_d = False
                for rect in listeObjets:
                    if collisionSegmentPoly(depart,Point(posX[g.vertex(l)],posY[g.vertex(l)]),RectangleToPoly(rect)):
                        touche_d = True
                        break
                    if not touche_d:
                        for robotA in robotsA:
                            if collisionSegmentPoly(depart,Point(posX[g.vertex(l)],posY[g.vertex(l)]),robotA):
                                touche_d = True
                                break
                if not touche_d:
                    g.add_edge(Ndepart,g.vertex(l))
                    poids[g.edge(Ndepart,g.vertex(l))] = sqrt((depart.x - posX[g.vertex(l)]) ** 2 + (depart.y - posY[g.vertex(l)]) ** 2)
            
            for l in range(g.num_vertices()-1):
                #teste les arêtes accessibles
                touche_a = False
                for rect in listeObjets:
                    if collisionSegmentPoly(arrive,Point(posX[g.vertex(l)],posY[g.vertex(l)]),RectangleToPoly(rect)):
                        touche_a = True
                        break
                    if not touche_a:
                        for robotA in robotsA:
                            if collisionSegmentPoly(arrive,Point(posX[g.vertex(l)],posY[g.vertex(l)]),robotA):
                                touche_a = True
                                break
                if not touche_a:
                    g.add_edge(Narrive,g.vertex(l))
                    poids[g.edge(Narrive,g.vertex(l))] = sqrt((arrive.x - posX[g.vertex(l)]) ** 2 + (arrive.y - posY[g.vertex(l)]) ** 2)
                    
                    
            #algorithme utilisé : A*
            chemin=AStar(Ndepart,Narrive)
            
            #sortie
            print "chemin -->"
            for p in chemin:
                print "(" + str(p.x) + ", " + str(p.y) + ")"


def AStar(Ndepart,Narrive):
    """
    algorithme A*, sur une table de jeu discrétisée "par cases"
    """
    
    #fonction heuristique : renvoit la distance restante supposée
    def h(n, Narrive):
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
    Tpoids=marshal.load(open("sauv_poids","rb"))
    for k in range(len(TposX)):
        posX[g.vertex(k)]=TposX[k]
        posY[g.vertex(k)]=TposY[k]
    k=0
    for e in g.edges():
        poids[e]=Tpoids[k]
        k+=1
        
    
def enregistreGraphe():    

    """
    génération des noeuds, avec positions
    et des arêtes, avec poids
    """
   
    print "création du graphe -->"
    k=0
    for objet in listeObjets:
        #ajoute 4 noeuds : les angles de l'objet rectangulaire
        for angle in RectangleToPoly(objet):
            g.add_vertex()
            posX[g.vertex(k)] = angle.x
            posY[g.vertex(k)] = angle.y
            for l in range(k):
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
    for e in g.edges():
        Tpoids.append(poids[e])
    marshal.dump(TposX, open("sauv_posX", 'wb'))
    marshal.dump(TposY, open("sauv_posY", 'wb'))
    marshal.dump(Tpoids, open("sauv_poids", 'wb'))
    g.save("sauv_g.xml")
    
def tracePDF(nom):
    graph_draw(g, output=nom, pos=(posX,posY),vsize=5,vcolor=nCouleur, pin=True,penwidth=aLarg, eprops={"color": aCouleur})
    #graph_draw(g, output=nom, pos=(posX,posY),vsize=5,pin=True,penwidth=100)


enregistreGraphe()
centresRobotsA = []
rechercheChemin(Point(-110.,40.),Point(120.,140.),centresRobotsA)
print "tracePDF -->"
tracePDF("chemin_0_robotsA.pdf")

chargeGraphe()
centresRobotsA = [Point(10.,30.)]
rechercheChemin(Point(-110.,40.),Point(120.,140.),centresRobotsA)
print "tracePDF -->"
tracePDF("chemin_1_robotsA.pdf")

chargeGraphe()
centresRobotsA = [Point(10.,30.),Point(-100.,200.)]
rechercheChemin(Point(-110.,40.),Point(120.,140.),centresRobotsA)
print "tracePDF -->"
tracePDF("chemin_2_robotsA.pdf")