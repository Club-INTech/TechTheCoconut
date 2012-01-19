# -*- coding: utf-8 -*-

import os
import sys
from graph_tool.all import *
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
#from collisionRectangles import *
from outils_math.collisionRectangleCase import collisionRectangleCase
from outils_math.point import Point
from outils_math.rectangle import Rectangle

g = Graph(directed=False)
posX = g.new_vertex_property("int")
posY = g.new_vertex_property("int")
poids = g.new_edge_property("double")
poidsDirect = 1.
poidsDiag = 1.41
pas = 10 # pas en mm
largeur = int(200./pas)#TODO largeur = int(constantes["Coconut"]["largeur"]/pas)
longueur = int(300./pas)#TODO longueur = int(constantes["Coconut"]["longueur"]/pas)
#décalage des axes
axeX=0
axeY=0

listeObjets=[Rectangle(120.,120.,0.52,19.,100.),Rectangle(50.,150.,0.,50.,40.),Rectangle(150.,150.,-0.3,90.,20.)]

def rechercheChemin(debut,fin):
    """
    fonction de recherche de chemin, utilisant le meilleur algorithme codé
    """
    supprimerInaccessibles()
    return AStar(debut,fin)

def AStar(debut,fin):
    """
    algorithme A*, sur une table de jeu discrétisée "par cases"
    """
    
    #TODO : algorithme A* sur le graphe obtenu
    #TODO : retour de la structure cheminObtenu
    print "tracePDF -->"
    tracePDF()
    
def supprimerInaccessibles():
    """
    retire du graphe les noeuds entrant en collision avec les objets inaccessibles de la table de jeu
    """
    print "discretiseTable -->"
    discretiseTable()
    print "supprimerNoeuds -->"
    listeNoeuds=[]
    #itération sur les objets
    for objet in listeObjets:
        #trouve directement un noeud en collision avec l'objet en arrondissant les coordonnées de ce dernier
        n=g.vertex((objet.x+objet.y*longueur)/pas)
        listeNoeuds.extend(listerNoeuds(objet,[n],[n],[]))
    listeNoeuds=sorted(list(set(listeNoeuds)),reverse=True)
    supprimerNoeuds(listeNoeuds)
    
    
def supprimerNoeuds(listeNoeuds):
    listeNoeuds = map(lambda v: g.vertex(v),listeNoeuds)
    for n in listeNoeuds:
        g.remove_vertex(n)
    
def NoeudsVoisins(noeud,registreVoisins):
    nouveaux=[]
    for v in noeud.out_neighbours():
        if not (v in registreVoisins):
            nouveaux.append(v)
    return nouveaux   
    
def listerNoeuds(objet,registreVoisins,aParcourir,listeNoeuds):
    while aParcourir!=[]:
        noeud=aParcourir.pop()
        if collisionRectangleCase(objet,Point(posX[noeud],posY[noeud]),pas):
            listeNoeuds.append((posX[noeud]+posY[noeud]*longueur)/pas)
            nouveaux = NoeudsVoisins(noeud,registreVoisins)
            registreVoisins.extend(nouveaux)
            aParcourir.extend(nouveaux)
            
    return listeNoeuds
        
def discretiseTable():    
    """
    génération des noeuds, avec positions
    et des arêtes, avec poids
    """
    #premier noeud
    g.add_vertex()
    posX[g.vertex(0)] = 0+axeX
    posY[g.vertex(0)] = 0+axeY
    #première ligne
    for j in range(1,longueur):
        g.add_vertex()
        posX[g.vertex(longueur*0+j)] = j*pas+axeX
        posY[g.vertex(longueur*0+j)] = 0*pas+axeY
        #noeud à gauche
        g.add_edge(g.vertex(longueur*0+j-1),g.vertex(longueur*0+j))
        poids[g.edge(g.vertex(longueur*0+j-1),g.vertex(longueur*0+j))]=poidsDirect
    #autres lignes
    for i in range(1,largeur):
        #premier de la ligne
        g.add_vertex()
        posX[g.vertex(longueur*i)] = 0+axeX
        posY[g.vertex(longueur*i)] = i*pas+axeY
        #2 noeuds dessus
        g.add_edge(g.vertex(longueur*(i-1)),g.vertex(longueur*i))
        poids[g.edge(g.vertex(longueur*(i-1)),g.vertex(longueur*i))]=poidsDirect
        g.add_edge(g.vertex(longueur*(i-1)+1),g.vertex(longueur*i))
        poids[g.edge(g.vertex(longueur*(i-1)+1),g.vertex(longueur*i))]=poidsDiag
        #corps de la ligne
        for j in range(1,longueur-1):
            g.add_vertex()
            posX[g.vertex(longueur*i+j)] = j*pas+axeX
            posY[g.vertex(longueur*i+j)] = i*pas+axeY
            #noeud à gauche
            g.add_edge(g.vertex(longueur*i+j-1),g.vertex(longueur*i+j))
            poids[g.edge(g.vertex(longueur*i+j-1),g.vertex(longueur*i+j))]=poidsDirect
            #3 noeuds dessus
            g.add_edge(g.vertex(longueur*(i-1)+j-1),g.vertex(longueur*i+j))
            poids[g.edge(g.vertex(longueur*(i-1)+j-1),g.vertex(longueur*i+j))]=poidsDiag
            g.add_edge(g.vertex(longueur*(i-1)+j),g.vertex(longueur*i+j))
            poids[g.edge(g.vertex(longueur*(i-1)+j),g.vertex(longueur*i+j))]=poidsDirect
            g.add_edge(g.vertex(longueur*(i-1)+j+1),g.vertex(longueur*i+j))
            poids[g.edge(g.vertex(longueur*(i-1)+j+1),g.vertex(longueur*i+j))]=poidsDiag
        #dernier de la ligne
        g.add_vertex()
        posX[g.vertex(longueur*(i+1)-1)] = (longueur-1)*pas+axeX
        posY[g.vertex(longueur*(i+1)-1)] = i*pas+axeY
        #noeud à gauche
        g.add_edge(g.vertex(longueur*(i+1)-2),g.vertex(longueur*(i+1)-1))
        poids[g.edge(g.vertex(longueur*(i+1)-2),g.vertex(longueur*(i+1)-1))]=poidsDirect
        #2 noeuds dessus
        g.add_edge(g.vertex(longueur*i-1),g.vertex(longueur*(i+1)-1))
        poids[g.edge(g.vertex(longueur*i-1),g.vertex(longueur*(i+1)-1))]=poidsDirect
        g.add_edge(g.vertex(longueur*i-2),g.vertex(longueur*(i+1)-1))
        poids[g.edge(g.vertex(longueur*i-2),g.vertex(longueur*(i+1)-1))]=poidsDiag
        
    
def tracePDF():
    #tracé pdf
    #graph_draw(g, vprops={"label": g.vertex_index}, output="map_suppr.pdf", splines='false',vsize=0.11, elen=1)
    etiq = g.new_vertex_property("int")
    for v in g.vertices() :
        etiq[v]=(posX[v]+posY[v]*longueur)/pas
    graph_draw(g, vprops={"label": etiq}, output="map_rotation.pdf", pos=(posX,posY),vsize=5, pin=True,penwidth=20.,ecolor="#000000")

rechercheChemin(0,0)
      
#dist, pred = gt.astar_search(g, g.vertex(0), weight, VisitorExample(touch_v, touch_e, target), heuristic=lambda v: h(v, target, pos))