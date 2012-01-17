# -*- coding: utf-8 -*-

from graph_tool.all import *

g = Graph(directed=False)
posX = g.new_vertex_property("int")
posY = g.new_vertex_property("int")
poids = g.new_edge_property("double")
poidsDirect = 1.
poidsDiag = 1.41
pas = 10 # pas en mm
largeur = int(20.001/pas)#TODO largeur = int(constantes["Coconut"]["largeur"]/pas)
longueur = int(54./pas)#TODO longueur = int(constantes["Coconut"]["longueur"]/pas)
#décalage des axes
axeX=0
axeY=0


#génération des noeuds, avec positions
#et des arêtes, avec poids

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
    
    
for i in range(1,largeur):
    for j in range(longueur):
      print str(longueur*i+j) + " :\t" + str(posX[g.vertex(longueur*i+j)]) + ',\t' + str(posY[g.vertex(longueur*i+j)]) + " :\t" + str(poids[g.edge(g.vertex(longueur*i+j),g.vertex(longueur*(i-1)+j))])
      
      
#TODO : suppression des noeuds inaccessibles (triangulation de Delaunay)


#g, pos = gt.triangulation(points, type="delaunay")

#for e in g.edges():
 # touch_v = g.new_vertex_property("bool")
 # touch_e = g.new_edge_property("bool")
 # target = g.vertex(1)
 # dist, pred = gt.astar_search(g, g.vertex(0), weight, VisitorExample(touch_v, touch_e, target), heuristic=lambda v: h(v, target, pos))