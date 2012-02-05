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

#importation des éléments de jeu
import profils.develop.injection.elements_jeu
from lib.carte import Carte
import profils.develop.constantes


#lien avec constantes dans profil

#TODO à mettre dans constantes
coteRobot = 350.
rayonRobotsA = 350.

#approximation hexagonale des robots adverses
nCotesRobotsA = 6
#diamètre maximal du robot (cf élargissement des objets)
largeurRobot=coteRobot*sqrt(2)

#sur y
tableLargeur = constantes["Coconut"]["longueur"]
#sur x
tableLongueur = constantes["Coconut"]["largeur"]

#enlever
#4 points = angles de l'aire de jeu
bordsCarte=[Point(-tableLongueur/2+largeurRobot/2,0.+largeurRobot/2),Point(tableLongueur/2-largeurRobot/2,0.+largeurRobot/2),Point(-tableLongueur/2+largeurRobot/2,tableLargeur-largeurRobot/2),Point(tableLongueur/2-largeurRobot/2,tableLargeur-largeurRobot/2)]



#lien avec éléments de jeu

carte=Carte()
#4 reglettes, 2 totems, 1 palmier
r1=carte.reglettesEnBois[0].rectangle
r2=carte.reglettesEnBois[1].rectangle
r3=carte.reglettesEnBois[2].rectangle
r4=carte.reglettesEnBois[3].rectangle
p=carte.palmiers[0].rectangle
t1=carte.totems[0].rectangle
t2=carte.totems[1].rectangle

listeRectangles=[r1,r2,r3,r4,p,t1,t2]

#élargissement des objets : les noeuds concernent les zones accessibles par le centre du robot
for rect in listeRectangles:
    rect.wx += largeurRobot
    rect.wy += largeurRobot

#4 rectangles pour supprimer des arêtes sur les bords
listeDebug=[]
listeDebug.append(Rectangle(-tableLongueur/2+334,tableLargeur-largeurRobot/2,0.,10.,30.))#a_haut_gauche
listeDebug.append(Rectangle(tableLongueur/2-334,tableLargeur-largeurRobot/2,0.,10.,30.))#a_haut_droit
listeDebug.append(Rectangle(-tableLongueur/2+largeurRobot/2,509.,0.,30.,10.))#a_gauche
listeDebug.append(Rectangle(tableLongueur/2-largeurRobot/2,509.,0.,30.,10.))#a_droit


#déclaration du graphe, avec tables de propriétés : structure de données optimale pour les noeuds
g = Graph(directed=False)
posX = g.new_vertex_property("double")
posY = g.new_vertex_property("double")
poids = g.new_edge_property("double")

#centrage de l'axe des abscisses
axeX=-(tableLongueur)/2
axeY=0

#conversion des rectangles en polygones de 4 sommets
listeObjets=[]
for rect in listeRectangles:
    #création d'une liste de polygones pour les zones inaccessibles    
    #les éléments de jeu ne doivent pas dépasser de l'aire de jeu
    listePoints=[]
    for angle in RectangleToPoly(rect):
        if (angle.x > -tableLongueur/2+largeurRobot/2 and angle.x < tableLongueur/2-largeurRobot/2):
            px = angle.x
        elif (angle.x <= -tableLongueur/2+largeurRobot/2):
            px = -tableLongueur/2+largeurRobot/2
        else :
            px = tableLongueur/2-largeurRobot/2
            
        if (angle.y < tableLargeur-largeurRobot/2 and angle.y > 0.+largeurRobot/2):
            py = angle.y
        elif (angle.y >= tableLargeur-largeurRobot/2):
            py = tableLargeur-largeurRobot/2
        else :
            py = 0.+largeurRobot/2
        listePoints.append(Point(px,py))
    listeObjets.append(listePoints)

    
def rechercheChemin(depart,arrive,centresRobotsA):
    """
    fonction de recherche de chemin, utilisant le meilleur algorithme codé
    """
    
    chargeGraphe()
    
    if not (depart.x > -tableLongueur/2+largeurRobot/2 and depart.x < tableLongueur/2-largeurRobot/2 and depart.y < tableLargeur-largeurRobot/2 and depart.y > 0.+largeurRobot/2):
        print "+---------------------------------------------------+"
        print "| le point de départ n'est pas dans l'aire de jeu ! |"
        print "+---------------------------------------------------+"
    if not (arrive.x > -tableLongueur/2+largeurRobot/2 and arrive.x < tableLongueur/2-largeurRobot/2 and arrive.y < tableLargeur-largeurRobot/2 and arrive.y > 0.+largeurRobot/2):
        print "+---------------------------------------------------+"
        print "| le point d'arrivée n'est pas dans l'aire de jeu ! |"
        print "+---------------------------------------------------+"
        
    print "recherche chemin -->"
    
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
                for poly in listeObjets:
                    if collisionSegmentPoly(angle,Point(posX[g.vertex(l)],posY[g.vertex(l)]),poly):
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
        for poly in listeObjets:
            if collisionSegmentPoly(p1,p2,poly):
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
    for poly in listeObjets:
        if collisionPolyPoint(poly,depart):
            touche_td = True
            break
        if not touche_td:
            for robotA in robotsA:
                if collisionPolyPoint(robotA,depart):
                    touche_td = True
                    break
    if touche_td :
        print "+------------------------------------------+"
        print "| la position de départ est inaccessible ! |"
        print "+------------------------------------------+"
    else :
        touche_ta = False
        for poly in listeObjets:
            if collisionPolyPoint(poly,arrive):
                touche_ta = True
                break
            if not touche_ta:
                for robotA in robotsA:
                    if collisionPolyPoint(robotA,arrive):
                        touche_ta = True
                        break
        if touche_ta :
            print "+------------------------------------------+"
            print "| la position d'arrivée est inaccessible ! |"
            print "+------------------------------------------+"
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
                for poly in listeObjets:
                    if collisionSegmentPoly(depart,Point(posX[g.vertex(l)],posY[g.vertex(l)]),poly):
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
                for poly in listeObjets:
                    if collisionSegmentPoly(arrive,Point(posX[g.vertex(l)],posY[g.vertex(l)]),poly):
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
    algorithme A*, sur un graphe de noeuds représentant des coins d'objets, 
    et des arêtes portant un poids équivalent à la distance euclidienne entre les noeuds
    """
    
    #fonction heuristique : renvoit la distance restante supposée (équivalent continu de la distance de manhattan)
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
    
    #4 angles de l'aire de jeu
    for angle in bordsCarte:
        g.add_vertex()
        posX[g.vertex(k)] = angle.x
        posY[g.vertex(k)] = angle.y
        for l in range(k):
            #teste les arêtes accessibles
            touche = False
            for poly in listeObjets:
                if collisionSegmentPoly(angle,Point(posX[g.vertex(l)],posY[g.vertex(l)]),poly):
                    touche = True
                    break
            if not touche:
                for rect in listeDebug:
                    if collisionSegmentPoly(angle,Point(posX[g.vertex(l)],posY[g.vertex(l)]),RectangleToPoly(rect)):
                        touche = True
                        break
            if not touche:
                g.add_edge(g.vertex(k),g.vertex(l))
                poids[g.edge(g.vertex(k),g.vertex(l))] = sqrt((posX[g.vertex(k)] - posX[g.vertex(l)]) ** 2 + (posY[g.vertex(k)] - posY[g.vertex(l)]) ** 2)
        k+=1
        
    #éléments de jeu
    for objet in listeObjets:
        #ajoute 4 noeuds : les angles de l'objet rectangulaire
        for angle in objet:
            g.add_vertex()
            posX[g.vertex(k)] = angle.x
            posY[g.vertex(k)] = angle.y
            for l in range(k):
                #teste les arêtes accessibles
                touche = False
                for poly in listeObjets:
                    if collisionSegmentPoly(angle,Point(posX[g.vertex(l)],posY[g.vertex(l)]),poly):
                        touche = True
                        break
                if not touche:
                    for rect in listeDebug:
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