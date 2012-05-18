# -*- coding: utf-8 -*-

import sys
import os
import math
import time
import __builtin__
import timer
import re
import log
from outils_math.point import Point
import actionneur
import robot
import lib.log
import outils_math
import capteur
log =lib.log.Log(__name__)

sys.path.append('../')

import profils.develop.constantes

class Asservissement_duree:
    """
    Classe pour gérer l'asservissement
    """
    def __init__(self):
        if hasattr(__builtin__.instance, 'robotInstance'):
            self.robotInstance = __builtin__.instance.robotInstance
        else:
            log.logger.error("asservissement : ne peut importer instance.robotInstance")
            
        #distance seuil de detection pour les ultrasons
        #self.maxCapt = 400
        self.maxCapt = 0
        
        #liste des centres de robots adverses repérés (liste de points)
        self.liste_robots_adv = __builtin__.instance.liste_robots_adv
        
        #vitesse moyenne (translation et rotations)
        self.vitesse_moyenne_segment = 1
        
        #rayon moyen des robots adverses
        #TODO : à mettre dans constantes
        self.rayonRobotsAdverses = 200.0
        
        #timer pour les timeout
        self.timerAsserv = timer.Timer()
        
        self.vitesseRotation = 0.4
        self.vitesseTranslation = 368.
        self.modeRotation = 2
        self.modeTranslation = 2
        self.orientation = 0
        self.position = Point(0,400)
        self.duree = 0
        
        self.hotSpotsOriginaux = [Point(0, 1440), Point(860, 1440), Point(875, 970), Point(590, 290), Point(0, 560), Point(-590, 290), Point(-875, 970), Point(-860, 1440)]
        self.hotSpots = self.hotSpotsOriginaux[:]
        
    #############
    def test(self):
        raw_input("?")
        debut_timer = int(self.timerAsserv.getTime())
        raw_input("?")
        print int(self.timerAsserv.getTime()) - debut_timer
    #############
    def lancerChrono(self):
        self.duree = 0
        
    def mesurerChrono(self):
        return self.duree
        
    def goToSegment(self, arrivee, avecRechercheChemin = False):
        """
        Fonction qui envoie un point d'arrivé au robot sans utiliser la recherche de chemin (segment direct départ-arrivée)
        :param script: point d'arrivé
        :type script: point
        :param avecRechercheChemin: si le segment a été trouvé par la recherche de chemin
        :type avecRechercheChemin: booléen
        """
        depart = self.getPosition()
        log.logger.info("effectue le segment de départ : ("+str(depart.x)+","+str(depart.y)+") et d'arrivée : ("+str(arrivee.x)+","+str(arrivee.y)+")")
        
        
        delta_x = (arrivee.x-depart.x)
        delta_y = (arrivee.y-depart.y)
        angle = math.atan2(delta_y,delta_x)
        angle = int(angle*10000)/10000.
        
        self.gestionTourner(angle)
        
        """
        appel d'une translation de la distance euclidienne depart->arrivée
        sans instruction particulière
        avec un booléen codant l'utilisation de la recherche de chemin
        """
        distance = math.sqrt(delta_x**2+delta_y**2)
        distance = int(distance*10)/10.
        self.gestionAvancer(distance,"",avecRechercheChemin)
    
    
    
    ############################## <HACK>
    
    def goTo(self, arrivee):
        depart = self.getPosition()
        
        ##éventuelle symétrie sur la position d'arrivée
        if __builtin__.constantes['couleur'] == "r":
            arrivee.x *= -1
        
        #appel de la recherche de chemin : liste de points
        chemin = self.rechercheChemin(depart, arrivee)[0]
        for point in chemin:
            self.goToSegment(point, avecRechercheChemin = True)
        
        #on réinitialise la mémoire des (du) robot ennemi
        self.oublierAdverses()
        
    def getTimeTo(self,depart, arrivee):
        #appel de la recherche de chemin : distance parcourue
        return self.rechercheChemin(depart, arrivee)[1]/self.vitesse_moyenne_segment
        
    def rechercheChemin(self, depart, arrivee):
        """
        méthode de recherche de chemin basique
        renvoi un tuple dont 
        le premier element est la liste des points à parcourir, du deuxième point à l'arrivée
        le second est la distance totale parcourue
        """
        
        log.logger.info("Appel de la recherche de chemin basique pour le point de départ : ("+str(depart.x)+","+str(depart.y)+") et d'arrivée : ("+str(arrivee.x)+","+str(arrivee.y)+")")
        
        HSdepart = self.hotSpot(depart)
        HSarrivee = self.hotSpot(arrivee)
        
        #couper l'anneau si robot adverse
        for adverse in self.liste_robots_adv:
            self.supprimerHotspot(self.hotSpot(adverse))
        
        if HSdepart == HSarrivee :
            chemin = [HSdepart]
            dist = 0.
        else:
            #établissement de listes représentant le parcourt des hotspots dans les 2 sens
            listeSens1 = self.hotSpots[self.hotSpots.index(HSdepart):]+self.hotSpots[:self.hotSpots.index(HSdepart)]
            listeSens2 = listeSens1[:]
            listeSens2.reverse()
            listeSens2.insert(0,listeSens2.pop())
            
            #calcul de la distance du trajet, dans les 2 sens
            dist1 = 0.
            cheminSens1 = []
            for k in range(1,len(listeSens1)):
                if not listeSens1[k]:
                    dist1 = float('inf')
                    break
                else:
                    dist1 += math.sqrt( (listeSens1[k].x - listeSens1[k-1].x)**2 + (listeSens1[k].y - listeSens1[k-1].y)**2 )
                    cheminSens1.append(listeSens1[k])
                if listeSens1[k] == HSarrivee:
                    break
            
            dist2 = 0.  
            cheminSens2 = []
            for k in range(1,len(listeSens2)):
                if not listeSens2[k]:
                    dist2 = float('inf')
                    break
                else:
                    dist2 += math.sqrt( (listeSens2[k].x - listeSens2[k-1].x)**2 + (listeSens2[k].y - listeSens2[k-1].y)**2 )
                    cheminSens2.append(listeSens2[k])
                if listeSens2[k] == HSarrivee:
                    break
                
            if dist1 <= dist2:
                chemin = cheminSens1
                dist = dist1
            else:
                chemin = cheminSens2
                dist = dist2
            chemin.insert(0,HSdepart)
        
        #ajouter le point d'arrivée, si ce n'est pas un hotspot
        if not (arrivee.x == chemin[-1].x and arrivee.y == chemin[-1].y):
            chemin.append(arrivee)
            
        #ne pas créer de doublon si le point de départ était un hotspot
        try : chemin.remove(depart)
        except : pass
        
        
        #ajoute les distances des points départ et arrivée à celles calculées entre les hotspots
        dist += math.sqrt( (depart.x - HSdepart.x)**2 + (depart.y - HSdepart.y)**2 )
        dist += math.sqrt( (arrivee.x - HSarrivee.x)**2 + (arrivee.y - HSarrivee.y)**2 )
        
        log.logger.info("chemin trouvé : ("+str(chemin))
        return (chemin, dist)
            
            
    def hotSpot(self, point):
        #détermine le hotspot le plus proche à partir d'un point de la carte
        
        #zone sur le coté du totem
        if self.estDansZone(point,Point(-592,1180),Point(-401,810)):
            return self.hotSpots[7]
        elif self.estDansZone(point,Point(401,1180),Point(592,810)):
            return self.hotSpots[2]
            
        #zone sur le dessus du totem
        elif self.estDansZone(point,Point(-448,1213),Point(-167,1000)):
            return self.hotSpots[0]
        elif self.estDansZone(point,Point(167,1213),Point(448,1000)):
            return self.hotSpots[0]
            
        #zone sur le dessous du totem
        elif self.estDansZone(point,Point(-448,1000),Point(-167,810)):
            return self.hotSpots[4]
        elif self.estDansZone(point,Point(167,1000),Point(448,810)):
            return self.hotSpots[4]
            
        else:
            dest = self.hotSpots[0]
            for hs in self.hotSpots:
                if hs :
                    if ((hs.x - point.x)**2 + (hs.y - point.y)**2) < ((dest.x - point.x)**2 + (dest.y - point.y)**2) :
                        dest = hs
            return dest
        
    def estDansZone(self,point,hg,bd):
        if (point.x > hg.x and point.x < bd.x and point.y < hg.y and point.y > bd.y):
            return True
        else:
            return False
            
    def supprimerHotspot(self,hotspot):
        try:
            pos = self.hotSpots.index(hotspot)
            self.hotSpots.pop(pos)
            self.hotSpots.insert(pos,"")
        except: pass
    
    def oublierAdverses(self):
        __builtin__.instance.viderListeRobotsAdv()
        self.hotSpots = self.hotSpotsOriginaux[:]
    
    ############################## </HACK>
    
    
    
    #def goTo(self, arrivee):
        #"""
        #Fonction qui appelle la recherche de chemin et envoie une liste de coordonnées à la carte asservissement
        #:param depart: point de départ
        #:type depart: Point
        #:param arrivee: point d'arrivée
        #:type arrivee: Point
        #:param chemin: chemin renvoyé par la recherche de chemin
        #:type chemin: liste de points
        #"""
        #depart = self.getPosition()
        #log.logger.info("Appel de la recherche de chemin pour le point de départ : ("+str(depart.x)+","+str(depart.y)+") et d'arrivée : ("+str(arrivee.x)+","+str(arrivee.y)+")")
        #chemin_python = self.theta.rechercheChemin(depart,arrivee)
        
        #try :
            #chemin_python.remove(chemin_python[0])
        #except :
            #return (depart)
            
        #for i in chemin_python:
            #log.logger.info("goto (" + str(float(i.x)) + ', ' + str(float(i.y)) + ')')
            
            ##effectue un segment du chemin trouvé, en indiquant que la recherche de chemin a été utilisée
            #self.goToSegment(i,True)
        #return "chemin_termine"
        
    def gestionAvancer(self, distance, instruction = "", avecRechercheChemin = False):
        self.position.x += distance*math.cos(self.orientation)
        self.position.y += distance*math.sin(self.orientation)
        self.duree +=  distance/self.vitesseTranslation
        print "temps de translation\tde "+str(int(distance*10)/10.)+",   \tvitesse "+str(self.modeTranslation)+":\t"+str(distance/self.vitesseTranslation)
    
    def gestionTourner(self, angle, instruction = ""):
        if __builtin__.constantes['couleur'] == "r":
            angle = math.pi - angle
        
        deltaAngle = abs(self.orientation - angle)
        while deltaAngle >= 2*math.pi:
            deltaAngle -= 2*math.pi
        while deltaAngle > math.pi:
            deltaAngle = 2*math.pi - deltaAngle
        self.orientation = angle
        self.duree += deltaAngle/self.vitesseRotation
        print "temps de rotation\tà "+str(int(angle*1000)/1000.)+",   \tvitesse "+str(self.modeRotation)+":\t"+str(deltaAngle/self.vitesseRotation)
        
    def getPosition(self):
        return Point(self.position.x,self.position.y)
    
    def setPosition(self,position):
        self.position.x = position.x
        self.position.y = position.y
            
    def getOrientation(self):
        return self.orientation
            
    def setOrientation(self,orientation):
        self.orientation = orientation
     
    def changerVitesse(self, typeAsservissement, valeur):
        
        if typeAsservissement == "rotation":
            self.modeRotation = valeur
            if self.modeRotation == 1:
                self.vitesseRotation = 0.2
            elif self.modeRotation == 2:
                self.vitesseRotation = 0.4
            else:
                self.vitesseRotation = 1.5
                
        elif typeAsservissement == "translation":
            self.modeTranslation = valeur
            if self.modeTranslation == 1:
                self.vitesseTranslation = 148.
            elif self.modeTranslation == 2:
                self.vitesseTranslation = 368.
            else:
                self.vitesseTranslation = 573.
                
    def immobiliser(self):
        pass
       
    def recalage(self):
        pass
        
    def setUnsetAsser(self, asservissement, mode):
        pass
        
    def attendre(self, temps):
        print "temps d'attente    \t          \t         \t"+str(temps)
        self.duree += temps
        
    def degager(self,retry = False):
        orientation = self.getOrientation()
        if not retry :
            if orientation > -3*math.pi/4 and orientation <= -math.pi/4:
                consigne = -math.pi/2
            elif orientation > -math.pi/4 and orientation <= math.pi/4:
                consigne = 0.
            elif orientation > math.pi/4 and orientation <= 3*math.pi/4:
                consigne = math.pi/2
            else:
                consigne = math.pi
        else :
            if orientation <= -math.pi/2:
                consigne = -3*math.pi/4
            elif orientation > -math.pi/2 and orientation <= 0:
                consigne = -math.pi/4
            elif orientation > 0 and orientation <= math.pi/2:
                consigne = math.pi/4
            else:
                consigne = 3*math.pi/4
                
        self.gestionTourner(consigne,instruction = "finir",avecSymetrie = False)

        if hasattr(__builtin__.instance, 'actionInstance'):
            actionInstance = __builtin__.instance.actionInstance
            actionInstance.deplacer(40)
            time.sleep(0.3)
            actionInstance.deplacer(70)
            time.sleep(0.3)
            actionInstance.deplacer(0)
            time.sleep(0.3)
            
        self.gestionAvancer(150,instruction = "auStopNeRienFaire")
        self.gestionAvancer(150,instruction = "auStopNeRienFaire")

        position = self.getPosition()
        if self.estInaccessible(position):
            self.gestionAvancer(-150,instruction = "auStopNeRienFaire")
            self.gestionAvancer(-150,instruction = "auStopNeRienFaire")
            
            position = self.getPosition()
            if self.estInaccessible(position) and not retry:
                self.degager(retry = True)
                    
        
    def estInaccessible(self,point):
        point.x = abs(point.x)
        
        dansTable = self.estDansZone(point,Point(-1300,1800),Point(1300,200))
        
        dansTotem = self.estDansZone(point,Point(72,1341),Point(750,660))
        dansPalmier = self.estDansZone(point,Point(-240,1240),Point(250,750))
        danscalle = self.estDansZone(point,Point(970,2000),Point(1700,1130))
        dansbarette = self.estDansZone(point,Point(770,720),Point(1700,280))
        
        return not ( dansTable and not (dansTotem or dansPalmier or danscalle or dansbarette) )