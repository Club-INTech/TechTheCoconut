# -*- coding: utf-8 -*-

import os
import sys

# Ajout de ../../.. au path python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

import lib.log
log = lib.log.Log()
try:
    from graph_tool.all import *
except:
    log.logger.error("Vous devez installer graph-tool, plus d'informations sur le README")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../outils_math"))
#from collisionRectangles import Rectangle,collision
from collisionRectangles import *


g = Graph(directed=False)
posX = g.new_vertex_property("int")
posY = g.new_vertex_property("int")
poids = g.new_edge_property("double")
poidsDirect = 1.
poidsDiag = 1.41
pas = 10 # pas en mm
largeur = int(400./pas)#TODO largeur = int(constantes["Coconut"]["largeur"]/pas)
longueur = int(600./pas)#TODO longueur = int(constantes["Coconut"]["longueur"]/pas)
#décalage des axes
axeX=0
axeY=0

#objet=Rectangle(20.,15.,0,19.,4.)
objet=Rectangle(100.,300.,0.785398163,19.,100.)

def rechercheChemin(debut,fin):
    """
    fonction de recherche de chemin, utilisant le meilleur algorithme codé
    """
    return AStar(debut,fin)
        
def AStar(debut,fin):
    """
    algorithme A*, sur une table de jeu discrétisée "par cases"
    """
    print "discretiseTable -->"
    discretiseTable()
    
    print "listeNoeuds -->"
    
    n=selectNoeudProche(objet.x,objet.y) #TODO élire directement le noeud en arrondissant les coordonnées de l'objet
    
    listeNoeuds=[]
    
    #itération sur les objets
    l=listerNoeuds(objet,[n],[n],listeNoeuds)
    l=sorted(l,reverse=True)
    print l
    print "supprimerNoeuds -->"
    supprimerNoeuds(l)
    
    #TODO : algorithme A* sur le graphe obtenu
    #TODO : retour de la structure cheminObtenu
    print "tracePDF -->"
    tracePDF()

    
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
        case=Rectangle(posX[noeud],posY[noeud],0.,pas,pas)
        if collision(case,objet):
            listeNoeuds.append((posX[noeud]+posY[noeud]*longueur)/pas)
            nouveaux = NoeudsVoisins(noeud,registreVoisins)
            registreVoisins.extend(nouveaux)
            aParcourir.extend(nouveaux)
            
    return listeNoeuds
        
def selectNoeudProche(x,y):
    """
    à partir des coordonnée d'un objet inaccessible, renvoi un noeud du graphe contenant ces coordonnées.
    ce sera un premier noeud eliminé, et des tests de collision seront effectués par récurrence sur ses voisins.
    """
    for v in g.vertices() :
        if (abs(posX[v]-x) <= pas/2) and (abs(posY[v]-y) <= pas/2) :
            return v
            break
            
    
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
    graph_draw(g, vprops={"label": etiq}, output="map_inclinéPis4.pdf", pos=(posX,posY),vsize=5, pin=True,penwidth=20.,ecolor="#000000")

rechercheChemin(0,0)
      
#g, pos = gt.triangulation(points, type="delaunay")
#dist, pred = gt.astar_search(g, g.vertex(0), weight, VisitorExample(touch_v, touch_e, target), heuristic=lambda v: h(v, target, pos))