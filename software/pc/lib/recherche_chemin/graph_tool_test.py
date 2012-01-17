# -*- coding: utf-8 -*-

import os
import sys
from graph_tool.all import *
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../outils_math"))
from collisionRectangles import Rectangle,collision


g = Graph(directed=False)
posX = g.new_vertex_property("int")
posY = g.new_vertex_property("int")
poids = g.new_edge_property("double")
poidsDirect = 1.
poidsDiag = 1.41
pas = 10 # pas en mm
largeur = int(40.001/pas)#TODO largeur = int(constantes["Coconut"]["largeur"]/pas)
longueur = int(64./pas)#TODO longueur = int(constantes["Coconut"]["longueur"]/pas)
#décalage des axes
axeX=0
axeY=0

objet=Rectangle(20.,15.,-0.7853,10.,20.)

def rechercheChemin(debut,fin):
    """
    fonction de recherche de chemin, utilisant le meilleur algorithme codé
    """
    return AStar(debut,fin)
        
def AStar(debut,fin):
    """
    algorithme A*, sur une table de jeu discrétisée "par cases"
    """
    
    discretiseTable()
    
    n=selectNoeudProche(objet.x,objet.y)
    
    #case=Rectangle(posX[n],posY[n],0,pas,pas)
    #print collision(case,objet)
    
    listeNoeuds=[(posX[n]+posY[n]*longueur)/pas]
    
    #itération sur les objets
    l=listerNoeuds(objet,[n],[n],listeNoeuds)
    l=sorted(l)
    print l
    #supprimerNoeuds(l)
    
    #TODO : algorithme A* sur le graphe obtenu
    #TODO : retour de la structure cheminObtenu
    graph_draw(g, vprops={"label": g.vertex_index}, output="map_suppr.pdf", splines='false',vsize=0.11, elen=1)
    
    
    
def supprimerNoeuds(listeNoeuds):
    for n in listeNoeuds:
        g.remove_vertex(n)
    
def NoeudsVoisins(noeud,registreVoisins):
    nouveaux=[]
    for v in noeud.out_neighbours():
        if not (v in registreVoisins):
            print (posX[v]+posY[v]*longueur)/pas
            nouveaux.append((posX[v]+posY[v]*longueur)/pas)
            #nouveaux.append(v)
    return nouveaux   
    
def listerNoeuds(objet,registreVoisins,aParcourir,listeNoeuds):
    while aParcourir!=[]:
        noeud=aParcourir.pop()
        case=Rectangle(posX[noeud],posY[noeud],0,pas,pas)
        if collision(case,objet):
            nouveaux = NoeudsVoisins(noeud,registreVoisins)
            listeNoeuds.extend(nouveaux)
            nouveaux = map(lambda v: g.vertex(v),nouveaux)
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
        
    """
    trace
    for i in range(1,largeur):
        for j in range(longueur):
            print str(longueur*i+j) + " :\t" + str(posX[g.vertex(longueur*i+j)]) + ',\t' + str(posY[g.vertex(longueur*i+j)]) + " :\t" + str(poids[g.edge(g.vertex(longueur*i+j),g.vertex(longueur*(i-1)+j))])
    """
    
    #g.remove_vertex(g.vertex(longueur*(largeur/2)-(longueur/2)))
    
    

rechercheChemin(0,0)
      
#g, pos = gt.triangulation(points, type="delaunay")
#dist, pred = gt.astar_search(g, g.vertex(0), weight, VisitorExample(touch_v, touch_e, target), heuristic=lambda v: h(v, target, pos))