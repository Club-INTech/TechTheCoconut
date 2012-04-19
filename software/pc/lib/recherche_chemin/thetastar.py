# -*- coding: utf-8 -*-

#sauvegarde du graphe dans les fichiers "sauv_"
import marshal

# Ajout de ../.. au path python
import os,sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

#gestion des logs
import lib.log
log = lib.log.Log(__name__)

#importation de fonctions et classes de géométrie
from lib.outils_math.collisions import *
from lib.outils_math.point import Point
from lib.outils_math.rectangle import Rectangle
from lib.outils_math.polygone import polygone
from math import sqrt

#importation des éléments de jeu
import profils.develop.injection.elements_jeu
import profils.develop.constantes
from lib.carte import Carte
import __builtin__
import lib.instance

import lib.visualisation.visu_threads as visu_threads

#bibliothèque pour la gestion des graphes 
try:
    from graph_tool.all import *
except:
    log.logger.error("Vous devez installer graph-tool, plus d'informations sur le README")

class Thetastar:
    """
    Implémente l'algorithme de recherche de chemin sans discrétisation de la map (~Theta *). Pas de lissage nécessaire.\n\n
    
    Exemple d'utilisation :\n
    theta = Thetastar([])\n
    theta.enregistreGraphe() # On fait du cache\n
    theta.rechercheChemin(Point(-270.,248.),Point(-350.,1200.))
    
    :param liste_robots_adv: Liste des centres des robots adverses
    :type liste_robots_adv: list de Point
    """
    
    lastRayon = 0
    
    # Constantes du robot Coconut
    tableLargeur = constantes["Coconut"]["longueur"]
    tableLongueur = constantes["Coconut"]["largeur"]
    rayonRobotsA = constantes["Recherche_Chemin"]["rayonRobotsA"]
    nCotesRobotsA = constantes["Recherche_Chemin"]["nCotesRobotsA"]
    
    #TODO à remplacer 
    coteRobot = constantes["Coconut"]["coteRobot"]
    rayonRobot=coteRobot*sqrt(2)
    
    #par rayonRobot=lib.robot.Robot.rayon
    
    carte = Carte()
    
    # Reglettes
    r1 = carte.reglettesEnBois[0].rectangle
    r2 = carte.reglettesEnBois[1].rectangle
    r3 = carte.reglettesEnBois[2].rectangle
    r4 = carte.reglettesEnBois[3].rectangle
    
    # Palmier
    p = carte.palmiers[0].rectangle
    
    # Totems
    t1 = carte.totems[0].rectangle
    t2 = carte.totems[1].rectangle    
    
    listeRectangles = [r1,r2,r3,r4,p,t1,t2]

    #déclaration du graphe, avec tables de propriétés : structure de données optimale pour les noeuds
    g = Graph(directed=False)
    posX = g.new_vertex_property("double")
    posY = g.new_vertex_property("double")
    poids = g.new_edge_property("double")

    #centrage de l'axe des abscisses
    axeX=-(tableLongueur)/2
    axeY=0

    #pour activer les déviations automatiques en cas de départ/arrivée inaccessible
    effectuer_deviation_negligeable = True
    effectuer_deviation_segment = True

    listeObjets = []

    def __init__(self, liste_robots_adv):
        Thetastar.liste_robots_adv = liste_robots_adv
        
        if hasattr(__builtin__.instance, 'robotInstance'):
            self.rayonRobot = __builtin__.instance.robotInstance.rayon
        else:
            log.logger.error("thetastar : ne peut importer instance.robotInstance")
        
        if not Thetastar.lastRayon == self.rayonRobot:
            #élargissement des objets : les noeuds concernent les zones accessibles par le centre du robot
            for rect in Thetastar.listeRectangles:
                rect.wx += self.rayonRobot
                rect.wy += self.rayonRobot
                
            #conversion des rectangles en polygones de 4 sommets
            for rect in Thetastar.listeRectangles:
                #création d'une liste de polygones pour les zones inaccessibles    
                #les éléments de jeu ne doivent pas dépasser de l'aire de jeu
                listePoints = []
                for angle in RectangleToPoly(rect):
                    listePoints.append(Point(angle.x,angle.y))
                Thetastar.listeObjets.append(listePoints)
            Thetastar.lastRayon = self.rayonRobot

    def rechercheChemin(self, depart, arrive):
        """
        Méthode qui retourne la liste des points par lesquels passer pour aller du départ à l'arrivée en évitant les obstacles
        
        :param depart: Point de départ
        :type depart: Point
        :param arrive: Point d'arrivée
        :type arrive: Point
        """
        self.chargeGraphe()
        log.logger.info("Recherche de chemin entre ("+str(depart.x)+", "+str(depart.y)+") et ("+str(arrive.x)+", "+str(arrive.y)+")")

        if not (depart.x > -Thetastar.tableLongueur/2+self.rayonRobot/2 and depart.x < Thetastar.tableLongueur/2-self.rayonRobot/2 and depart.y < Thetastar.tableLargeur-self.rayonRobot/2 and depart.y > 0.+self.rayonRobot/2):
            log.logger.error("Le point de départ n'est pas dans l'aire de jeu")
        if not (arrive.x > -Thetastar.tableLongueur/2+self.rayonRobot/2 and arrive.x < Thetastar.tableLongueur/2-self.rayonRobot/2 and arrive.y < Thetastar.tableLargeur-self.rayonRobot/2 and arrive.y > 0.+self.rayonRobot/2):
            log.logger.critical("le point d'arrivée n'est pas dans l'aire de jeu !")

        
        #création des robots adverses
        robotsA=[]
        for centre in Thetastar.liste_robots_adv:
            robotsA.append(polygone(centre,self.rayonRobotsA,Thetastar.nCotesRobotsA))
            
        
        k=Thetastar.g.num_vertices()
        for robotA in robotsA:
            #ajoute les noeuds des sommets du polygone représentant le robot adverse
            for angle in robotA:
                Thetastar.g.add_vertex()
                Thetastar.posX[Thetastar.g.vertex(k)] = angle.x
                Thetastar.posY[Thetastar.g.vertex(k)] = angle.y
                for l in range(4,k):
                    #teste les arêtes accessibles
                    touche = False
                    for poly in Thetastar.listeObjets:
                        if collisionSegmentPoly(angle,Point(Thetastar.posX[Thetastar.g.vertex(l)],Thetastar.posY[Thetastar.g.vertex(l)]),poly):
                            touche = True
                            break
                    if not touche:
                        for robotA in Thetastar.liste_robots_adv:
                            if collisionSegmentPoly(angle,Point(Thetastar.posX[Thetastar.g.vertex(l)],Thetastar.posY[Thetastar.g.vertex(l)]),polygone(robotA,self.rayonRobotsA,Thetastar.nCotesRobotsA)):
                                touche = True
                                break
                    if not touche:
                        Thetastar.g.add_edge(Thetastar.g.vertex(k),Thetastar.g.vertex(l))
                        Thetastar.poids[Thetastar.g.edge(Thetastar.g.vertex(k),Thetastar.g.vertex(l))] = sqrt((Thetastar.posX[Thetastar.g.vertex(k)] - Thetastar.posX[Thetastar.g.vertex(l)]) ** 2 + (Thetastar.posY[Thetastar.g.vertex(k)] - Thetastar.posY[Thetastar.g.vertex(l)]) ** 2)
                k+=1
            
                
        #supprime les arêtes du graphe initial en collision avec les polygones des robots adverses
        for e in Thetastar.g.edges() :
            p1=Point(Thetastar.posX[e.source()],Thetastar.posY[e.source()])
            p2=Point(Thetastar.posX[e.target()],Thetastar.posY[e.target()])
            touche = False
            for poly in Thetastar.listeObjets:
                if collisionSegmentPoly(p1,p2,poly):
                    touche = True
                    break
            if not touche:
                for robotA in robotsA:
                    if collisionSegmentPoly(p1,p2,robotA):
                        touche = True
                        break
            if touche :
                Thetastar.g.remove_edge(e)
        
        
        
        #test de l'accessibilité des positions de départ et d'arrivée
        touche_td = False
        for poly in Thetastar.listeObjets:
            if collisionPolyPoint(poly,depart):
                touche_td = True
                break
            if not touche_td:
                for robotA in robotsA:
                    if collisionPolyPoint(robotA,depart):
                        touche_td = True
                        break
        if touche_td :
            log.logger.critical("la position de départ est inaccessible !")
            
            if Thetastar.effectuer_deviation_negligeable :
                #on retente depuis un point de départ voisin, sur un cercle (hexagone) de faible rayon
                for redir in polygone(depart,10.,6):
                    touche_tr = False
                    for poly in Thetastar.listeObjets:
                        if collisionPolyPoint(poly,redir):
                            touche_tr = True
                            break
                        if not touche_tr:
                            for robotA in robotsA:
                                if collisionPolyPoint(robotA,redir):
                                    touche_tr = True
                                    break
                    if not touche_tr :
                        log.logger.warning("deviation négligeable depuis ("+str(redir.x)+","+str(redir.y)+")")
                        return self.rechercheChemin(redir,arrive)
                        break
            
            
        else :
            touche_ta = False
            for poly in Thetastar.listeObjets:
                if collisionPolyPoint(poly,arrive):
                    touche_ta = True
                    break
                if not touche_ta:
                    for robotA in robotsA:
                        if collisionPolyPoint(robotA,arrive):
                            touche_ta = True
                            break
            if touche_ta :
                log.logger.critical("la position d'arrivée ("+str(arrive.x)+","+str(arrive.y)+") est inaccessible !")
                
                
                if Thetastar.effectuer_deviation_negligeable :
                    
                    #on retente une destination voisine de celle recherchée
                    
                    #d'abord sur un cercle (hexagone) de faible rayon autour du point d'arrivé initial
                    touche_cercle_A=True
                    for redir in polygone(arrive,10.,6):
                        touche_tr = False
                        for poly in Thetastar.listeObjets:
                            if collisionPolyPoint(poly,redir):
                                touche_tr = True
                                break
                            if not touche_tr:
                                for robotA in robotsA:
                                    if collisionPolyPoint(robotA,redir):
                                        touche_tr = True
                                        break
                        if not touche_tr :
                            touche_cercle_A=False
                            log.logger.warning("deviation négligeable vers --> ("+str(redir.x)+","+str(redir.y)+")")
                            return self.rechercheChemin(depart,redir)
                            break
                    
                    if Thetastar.effectuer_deviation_segment :
                        #puis sur le segment départ-arrivée initial, on choisit le point accessible le plus proche de l'arrivée
                        if touche_cercle_A:
                            pCollision=False
                            for robotA in robotsA:
                                pCollision=collisionSegmentPoly(depart,arrive,robotA)
                                if pCollision:
                                    break
                            if not pCollision:
                                for poly in Thetastar.listeObjets:
                                    pCollision=collisionSegmentPoly(depart,arrive,poly)
                                    if pCollision:
                                        break
                            log.logger.warning("deviation vers --> ("+str(pCollision[1].x)+","+str(pCollision[1].y)+")")
                            return self.rechercheChemin(depart,Point(0.99999999*pCollision[1].x+0.00000001*depart.x,0.99999999*pCollision[1].y+0.00000001*depart.y))
                
                
                
            else :
                #créations des noeuds arguments et de leurs arêtes
                Ndepart=Thetastar.g.add_vertex()
                Thetastar.posX[Ndepart] = depart.x
                Thetastar.posY[Ndepart] = depart.y
                Narrive=Thetastar.g.add_vertex()
                Thetastar.posX[Narrive] = arrive.x
                Thetastar.posY[Narrive] = arrive.y
                for l in range(4,Thetastar.g.num_vertices()-2):
                    #teste les arêtes accessibles
                    touche_d = False
                    for poly in Thetastar.listeObjets:
                        if collisionSegmentPoly(depart,Point(Thetastar.posX[Thetastar.g.vertex(l)],Thetastar.posY[Thetastar.g.vertex(l)]),poly):
                            touche_d = True
                            break
                        if not touche_d:
                            for robotA in robotsA:
                                if collisionSegmentPoly(depart,Point(Thetastar.posX[Thetastar.g.vertex(l)],Thetastar.posY[Thetastar.g.vertex(l)]),robotA):
                                    touche_d = True
                                    break
                    if not touche_d:
                        Thetastar.g.add_edge(Ndepart,Thetastar.g.vertex(l))
                        Thetastar.poids[Thetastar.g.edge(Ndepart,Thetastar.g.vertex(l))] = sqrt((depart.x - Thetastar.posX[Thetastar.g.vertex(l)]) ** 2 + (depart.y - Thetastar.posY[Thetastar.g.vertex(l)]) ** 2)
                
                for l in range(4,Thetastar.g.num_vertices()-1):
                    #teste les arêtes accessibles
                    touche_a = False
                    for poly in Thetastar.listeObjets:
                        if collisionSegmentPoly(arrive,Point(Thetastar.posX[Thetastar.g.vertex(l)],Thetastar.posY[Thetastar.g.vertex(l)]),poly):
                            touche_a = True
                            break
                        if not touche_a:
                            for robotA in robotsA:
                                if collisionSegmentPoly(arrive,Point(Thetastar.posX[Thetastar.g.vertex(l)],Thetastar.posY[Thetastar.g.vertex(l)]),robotA):
                                    touche_a = True
                                    break
                    if not touche_a:
                        Thetastar.g.add_edge(Narrive,Thetastar.g.vertex(l))
                        Thetastar.poids[Thetastar.g.edge(Narrive,Thetastar.g.vertex(l))] = sqrt((arrive.x - Thetastar.posX[Thetastar.g.vertex(l)]) ** 2 + (arrive.y - Thetastar.posY[Thetastar.g.vertex(l)]) ** 2)
                        
                        
                
                chemin=[]
                
                log.logger.info("Chemin trouvé :")
                #algorithme utilisé : A*
                for p in self.AStar(Ndepart,Narrive):
                    log.logger.info("(" + str(p.x) + ", " + str(p.y) + ")")
                    chemin.append(Point(int(p.x),int(p.y)))
                    
                visu_table = visu_threads.Visu_threads.rechercheThread('visu_table')
                if visu_table is not None:
                    visu_table.creerChemin(chemin)

                return chemin






    def AStar(self, Ndepart,Narrive):
        
        """
        Méthode qui implémente l'algorithme A*, sur un graphe de noeuds représentant des coins d'objets, 
        et des arêtes portant un poids équivalent à la distance euclidienne entre les noeuds
            
        :param Ndepart: Noeud de départ
        :type Ndepart: graph-tool Vertex
        :param Narrive: Noeud d'arrivée
        :type Narrive: graph-tool Vertex
        """
        
        
        #fonction heuristique : renvoit la distance restante supposée (équivalent continu de la distance de manhattan)
        def h(n, Narrive):
            return sqrt((Thetastar.posX[n] - Thetastar.posX[Narrive]) ** 2 + (Thetastar.posY[n] - Thetastar.posY[Narrive]) ** 2)
        
        #réinitialisation des tables des noeuds et arêtes parcourus par A*
        touch_v = Thetastar.g.new_vertex_property("bool")
        touch_e = Thetastar.g.new_edge_property("bool")
        #A* : liste 
        dist, pred = astar_search(Thetastar.g, Ndepart, Thetastar.poids, VisitorExample(touch_v, touch_e, Narrive), heuristic=lambda n: h(n, Narrive))
        
        #tracé du chemin
        v = Narrive
        chemin=[]
        while v != Ndepart:
            chemin.insert(0, Point(Thetastar.posX[v],Thetastar.posY[v]))
            p = Thetastar.g.vertex(pred[v])
            v = p
        chemin.insert(0, Point(Thetastar.posX[v],Thetastar.posY[v]))
        return chemin





    def chargeGraphe(self):
        """
        Méthode qui charge le graphe initial depuis les fichiers sauv_*
            
        """
        
        Thetastar.g=load_graph("sauv_g.xml")
        TposX=marshal.load(open("sauv_posX","rb"))
        TposY=marshal.load(open("sauv_posY","rb"))
        Tpoids=marshal.load(open("sauv_poids","rb"))
        for k in range(len(TposX)):
            Thetastar.posX[Thetastar.g.vertex(k)]=TposX[k]
            Thetastar.posY[Thetastar.g.vertex(k)]=TposY[k]
        k=0
        for e in Thetastar.g.edges():
            Thetastar.poids[e]=Tpoids[k]
            k+=1
            
    
    def enregistreGraphe(self):
        
        """
        Méthode qui enregistre le graphe contenant les éléments de jeu dans les fichiers sauv_*
            
        """
    
        k=0
        
        
        #éléments de jeu
        for objet in Thetastar.listeObjets:
            #ajoute 4 noeuds : les angles de l'objet rectangulaire
            for angle in objet:
                if (angle.x > -Thetastar.tableLongueur/2+self.rayonRobot/2 and angle.x < Thetastar.tableLongueur/2-self.rayonRobot/2 and angle.y < Thetastar.tableLargeur-self.rayonRobot/2 and angle.y > 0.+self.rayonRobot/2):
                    Thetastar.g.add_vertex()
                    Thetastar.posX[Thetastar.g.vertex(k)] = angle.x
                    Thetastar.posY[Thetastar.g.vertex(k)] = angle.y
                    for l in range(4,k):
                        #teste les arêtes accessibles
                        touche = False
                        for poly in Thetastar.listeObjets:
                            if collisionSegmentPoly(angle,Point(Thetastar.posX[Thetastar.g.vertex(l)],Thetastar.posY[Thetastar.g.vertex(l)]),poly):
                                touche = True
                                break
                                
                        
                        if not touche:
                            Thetastar.g.add_edge(Thetastar.g.vertex(k),Thetastar.g.vertex(l))
                            Thetastar.poids[Thetastar.g.edge(Thetastar.g.vertex(k),Thetastar.g.vertex(l))] = sqrt((Thetastar.posX[Thetastar.g.vertex(k)] - Thetastar.posX[Thetastar.g.vertex(l)]) ** 2 + (Thetastar.posY[Thetastar.g.vertex(k)] - Thetastar.posY[Thetastar.g.vertex(l)]) ** 2)
                    k+=1
        
        
        log.logger.info("création du graphe initial et enregistrement dans les fichiers sauv_*")
        TposX=[]
        TposY=[]
        Tpoids=[]
        for v in Thetastar.g.vertices() :
            TposX.append(Thetastar.posX[v])
            TposY.append(Thetastar.posY[v])
        for e in Thetastar.g.edges():
            Tpoids.append(Thetastar.poids[e])
        marshal.dump(TposX, open("sauv_posX", 'wb'))
        marshal.dump(TposY, open("sauv_posY", 'wb'))
        marshal.dump(Tpoids, open("sauv_poids", 'wb'))
        Thetastar.g.save("sauv_g.xml")





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