# -*- coding: utf-8 -*-

"""
il faudra importer :
from lib.recherche_chemin.rechercheChemin import discretiseTable,rechercheChemin

et faire un seul appel de discretiseTable(), pour initialiser le graphe.
rechercheChemin(a,b) où a et b sont des Points renvoi une liste de Points, du départ à l'arrivée

voir utiliseRechercheChemin pour exemple
"""

try:
    from graph_tool.all import *
except:
    log.logger.error("Vous devez installer graph-tool, plus d'informations sur le README")
import os,sys
# Ajout de ../.. au path python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
import lib.log
log = lib.log.Log()

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
        

def rechercheChemin(depart,arrive,centresRobotsA):
    """
    fonction de recherche de chemin, utilisant le meilleur algorithme codé
    """
    
    #réinitialisation des property map de couleurs
    global aCouleur
    global aLarg
    global nCouleur
    aCouleur = g.new_edge_property("string")
    aLarg = g.new_edge_property("double")
    nCouleur = g.new_vertex_property("string")
    
    
    """
    besoin de sauvegarder le graphe ?
    g=load_graph("map_vierge.xml")
    g.save("map_vierge.xml")
    """
    
  
    #noeuds arguments 1è méthode
    """
    for v in find_vertex(g, posX, depart.x):
        if posY[v] == depart.y:
            Ndepart=v
    
    for v in find_vertex(g, posX, arrive.x):
        if posY[v] == arrive.y:
            Narrive=v
    """
    
    #noeuds arguments 2è méthode
    for v in find_vertex(g, pos, (depart.x-axeX+(depart.y-axeY)*longueur)/pas ):
        Ndepart=v
    for v in find_vertex(g, pos, (arrive.x-axeX+(arrive.y-axeY)*longueur)/pas ):
        Narrive=v
        
        
    
    #pointeurs sur départ et arrivé
    g.add_edge(g.vertex(0),Ndepart)
    g.add_edge(g.vertex(1),Narrive)
    
    supprimerInaccessibles()
    
    #on retrouve les noeuds départ et arrivé grace aux pointeurs
    for n in g.vertex(0).out_neighbours():
        Ndepart=n
    for n in g.vertex(1).out_neighbours():
        Narrive=n
        
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
        
def discretiseTable():    
    """
    génération des noeuds, avec positions
    et des arêtes, avec poids
    """
    
    print "discretiseTable -->"

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
        
    
def tracePDF(nom):
    graph_draw(g, output=nom, pos=(posX,posY),vsize=5,vcolor=nCouleur, pin=True,penwidth=aLarg, eprops={"color": aCouleur})
    