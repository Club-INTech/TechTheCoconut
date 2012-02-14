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

try:
    from graph_tool.all import *
except:
    log.logger.error("Vous devez installer graph-tool, plus d'informations sur le README")

from lib.outils_math.collisions import *
from lib.outils_math.point import Point
from lib.outils_math.rectangle import Rectangle
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

#déclaration du graphe, avec tables de propriétés : structure de données optimale pour les noeuds
g = Graph(directed=False)
posX = g.new_vertex_property("int")
posY = g.new_vertex_property("int")
pos = g.new_vertex_property("int")
poids = g.new_edge_property("double")

Nstruct = 2 #nb de noeuds de structure placés à la racine. il servent à pointer d'autres noeuds
"""
g.vertex(0) pointe sur le noeud de départ
g.vertex(1) pointe sur le noeud d'arrivé
"""

#poids des arêtes, tenant compte du déplacement en diagonale avec sqrt(2)
poidsDirect = 1.
poidsDiag = 1.41

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
    """
    #autre méthode, ne marche pas avec un graphe enregistré (?)
    for v in find_vertex(g, pos, (depart.x-axeX+(depart.y-axeY)*longueur)/pas ):
        Ndepart=v
    for v in find_vertex(g, pos, (arrive.x-axeX+(arrive.y-axeY)*longueur)/pas ):
        Narrive=v
    """
    
    #algorithme utilisé : A*
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
    
def supprimerInaccessibles():
    """
    retire du graphe les noeuds entrant en collision avec les objets inaccessibles de la table de jeu
    """
    
    print "supprimerNoeuds -->"
    listeNoeuds=[]
    #itération sur les objets
    for objet in listeObjets:
        #trouve directement un noeud en collision avec l'objet en arrondissant les coordonnées de ce dernier
        n=( int((objet.x-axeX)/pas)*pas + int((objet.y-axeY)/pas)*pas*longueur )/pas
        if(n > longueur*largeur):
            n -= longueur
        elif(n<0):
            n += longueur
        n=g.vertex(Nstruct+n)
        #recherche les autres noeuds en collision par récurrence sur les noeuds voisins. complexité proportionnelle à l'aire de l'objet.
        listeNoeuds.extend(listerNoeuds(RectangleToPoly(objet),[n],[n],[]))
    listeNoeuds=sorted(list(set(listeNoeuds)),reverse=True)
    supprimerNoeuds(listeNoeuds)

    
def supprimerNoeuds(listeNoeuds):
    #supprime les noeuds de la liste d'index, qui doit impérativement etre triée dans l'ordre décroissant
    listeNoeuds = map(lambda v: g.vertex(Nstruct+v),listeNoeuds)
    for n in listeNoeuds:
        g.remove_vertex(n)
    
def NoeudsVoisins(noeud,registreVoisins):
    #renvoi la liste des voisins du noeuds, si ils ne sont pas dans registreVoisins
    nouveaux=[]
    for v in noeud.out_neighbours():
        if not (v in registreVoisins):
            nouveaux.append(v)
    return nouveaux   
    
def listerNoeuds(poly,registreVoisins,aParcourir,listeNoeuds):
    """
    poly : polygone devant etre retiré du graphe (liste de Points représentant les sommets du poly)
    registreVoisins : évite de tester plusieurs fois un noeuds (et donc de créer des boucles incontrolées )
    aParcourir : pile des noeuds non évalués
    listeNoeuds : liste des noeuds effectivement en collision avec le polygone
    """
    while aParcourir!=[]:
        noeud=aParcourir.pop()
        #test de collision entre un polygone et une case carrée centré en Point, et de côté pas
        if collisionPolyCase(poly,Point(posX[noeud],posY[noeud]),pas):
            listeNoeuds.append((posX[noeud]-axeX+(posY[noeud]-axeY)*longueur)/pas)
            nouveaux = NoeudsVoisins(noeud,registreVoisins)
            registreVoisins.extend(nouveaux)
            aParcourir.extend(nouveaux)
    return listeNoeuds

def chargeGraphe():
    print "chargement du graphe..."
    global g
    g=load_graph("sauv_g.xml")
    TposX=marshal.load(open("sauv_posX","rb"))
    TposY=marshal.load(open("sauv_posY","rb"))
    Tpos=marshal.load(open("sauv_pos","rb"))
    for k in range(len(Tpos)):
        posX[g.vertex(k)]=TposX[k]
        posY[g.vertex(k)]=TposY[k]
        pos[g.vertex(k)]=Tpos[k]
    
def enregistreGraphe():    

    """
    génération des noeuds, avec positions
    et des arêtes, avec poids
    """
   
    print "discrétiseTable -->"

    #noeuds de structures, servant de pointeurs
    for k in range(Nstruct):
        g.add_vertex()
        
    #premier noeud
    g.add_vertex()
    posX[g.vertex(Nstruct+0)] = 0+axeX
    posY[g.vertex(Nstruct+0)] = 0+axeY
    #première ligne
    for j in range(1,longueur):
        g.add_vertex()
        posX[g.vertex(Nstruct+longueur*0+j)] = j*pas+axeX
        posY[g.vertex(Nstruct+longueur*0+j)] = 0*pas+axeY
        #noeud à gauche
        g.add_edge(g.vertex(Nstruct+longueur*0+j-1),g.vertex(Nstruct+longueur*0+j))
        poids[g.edge(g.vertex(Nstruct+longueur*0+j-1),g.vertex(Nstruct+longueur*0+j))]=poidsDirect
    #autres lignes
    for i in range(1,largeur):
        #premier de la ligne
        g.add_vertex()
        posX[g.vertex(Nstruct+longueur*i)] = 0+axeX
        posY[g.vertex(Nstruct+longueur*i)] = i*pas+axeY
        #2 noeuds dessus
        g.add_edge(g.vertex(Nstruct+longueur*(i-1)),g.vertex(Nstruct+longueur*i))
        poids[g.edge(g.vertex(Nstruct+longueur*(i-1)),g.vertex(Nstruct+longueur*i))]=poidsDirect
        g.add_edge(g.vertex(Nstruct+longueur*(i-1)+1),g.vertex(Nstruct+longueur*i))
        poids[g.edge(g.vertex(Nstruct+longueur*(i-1)+1),g.vertex(Nstruct+longueur*i))]=poidsDiag
        #corps de la ligne
        for j in range(1,longueur-1):
            g.add_vertex()
            posX[g.vertex(Nstruct+longueur*i+j)] = j*pas+axeX
            posY[g.vertex(Nstruct+longueur*i+j)] = i*pas+axeY
            #noeud à gauche
            g.add_edge(g.vertex(Nstruct+longueur*i+j-1),g.vertex(Nstruct+longueur*i+j))
            poids[g.edge(g.vertex(Nstruct+longueur*i+j-1),g.vertex(Nstruct+longueur*i+j))]=poidsDirect
            #3 noeuds dessus
            g.add_edge(g.vertex(Nstruct+longueur*(i-1)+j-1),g.vertex(Nstruct+longueur*i+j))
            poids[g.edge(g.vertex(Nstruct+longueur*(i-1)+j-1),g.vertex(Nstruct+longueur*i+j))]=poidsDiag
            g.add_edge(g.vertex(Nstruct+longueur*(i-1)+j),g.vertex(Nstruct+longueur*i+j))
            poids[g.edge(g.vertex(Nstruct+longueur*(i-1)+j),g.vertex(Nstruct+longueur*i+j))]=poidsDirect
            g.add_edge(g.vertex(Nstruct+longueur*(i-1)+j+1),g.vertex(Nstruct+longueur*i+j))
            poids[g.edge(g.vertex(Nstruct+longueur*(i-1)+j+1),g.vertex(Nstruct+longueur*i+j))]=poidsDiag
        #dernier de la ligne
        g.add_vertex()
        posX[g.vertex(Nstruct+longueur*(i+1)-1)] = (longueur-1)*pas+axeX
        posY[g.vertex(Nstruct+longueur*(i+1)-1)] = i*pas+axeY
        #noeud à gauche
        g.add_edge(g.vertex(Nstruct+longueur*(i+1)-2),g.vertex(Nstruct+longueur*(i+1)-1))
        poids[g.edge(g.vertex(Nstruct+longueur*(i+1)-2),g.vertex(Nstruct+longueur*(i+1)-1))]=poidsDirect
        #2 noeuds dessus
        g.add_edge(g.vertex(Nstruct+longueur*i-1),g.vertex(Nstruct+longueur*(i+1)-1))
        poids[g.edge(g.vertex(Nstruct+longueur*i-1),g.vertex(Nstruct+longueur*(i+1)-1))]=poidsDirect
        g.add_edge(g.vertex(Nstruct+longueur*i-2),g.vertex(Nstruct+longueur*(i+1)-1))
        poids[g.edge(g.vertex(Nstruct+longueur*i-2),g.vertex(Nstruct+longueur*(i+1)-1))]=poidsDiag
    for v in g.vertices() :
        pos[v]=(posX[v]-axeX+(posY[v]-axeY)*longueur)/pas
        
    supprimerInaccessibles()
    
    print "enregistreGraphe -->"
    TposX=[]
    TposY=[]
    Tpos=[]
    Tpoids=[]
    for v in g.vertices() :
        pos[v]=(posX[v]-axeX+(posY[v]-axeY)*longueur)/pas
        TposX.append(posX[v])
        TposY.append(posY[v])
        Tpos.append(posX[v])
        #Tpoids.append(poids[v])
    marshal.dump(TposX, open("sauv_posX", 'wb'))
    marshal.dump(TposY, open("sauv_posY", 'wb'))
    marshal.dump(Tpos, open("sauv_pos", 'wb'))
    #marshal.dump(Tpoids, open("sauv_poids", 'wb'))
    g.save("sauv_g.xml")
    
def tracePDF(nom):
    graph_draw(g, output=nom, pos=(posX,posY),vsize=5,vcolor=nCouleur, pin=True,penwidth=aLarg, eprops={"color": aCouleur})