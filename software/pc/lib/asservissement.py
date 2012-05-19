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

class Asservissement:
    """
    Classe pour gérer l'asservissement
    """
    def __init__(self):
        
        if hasattr(__builtin__.instance, 'capteurInstance'):
            self.capteurInstance = __builtin__.instance.capteurInstance
        else:
            log.logger.error("asservissement : ne peut importer instance.capteurInstance")
        if hasattr(__builtin__.instance, 'robotInstance'):
            self.robotInstance = __builtin__.instance.robotInstance
        else:
            log.logger.error("asservissement : ne peut importer instance.robotInstance")
        if hasattr(__builtin__.instance, 'serieAsserInstance'):
            self.serieAsserInstance = __builtin__.instance.serieAsserInstance
        else:
            log.logger.error("asservissement : ne peut importer instance.serieAsserInstance")
        if hasattr(__builtin__.instance, 'asserInstanceDuree'):
            self.asserInstanceDuree = __builtin__.instance.asserInstanceDuree
        else:
            log.logger.error("asservissement : ne peut importer instance.asserInstanceDuree")
            
        #distance seuil de detection pour les ultrasons
        self.maxCapt = 600
        
        #couleur du robot
        if __builtin__.constantes['couleur'] == "r":
            self.serieAsserInstance.ecrire('ccr')
        
        #vitesse moyenne (translation et rotations)
        self.vitesse_moyenne_segment = 700
        
        #liste des centres de robots adverses repérés (liste de points)
        self.liste_robots_adv = []
        
        #rayon moyen des robots adverses
        self.rayonRobotsAdverses = constantes["Recherche_Chemin"]["rayonRobotsA"]
        
        #timer pour les timeout
        self.timerAsserv = timer.Timer()
        
        self.vitesseTranslation = 2
        self.vitesseRotation = 2
        
        self.hotSpotsOriginaux = [Point(0, 1490), Point(860, 1490), Point(875, 970), Point(590, 290), Point(0, 560), Point(-590, 290), Point(-875, 970), Point(-860, 1490)]
        self.hotSpots = self.hotSpotsOriginaux[:]
    
    def goToSegment(self, arrivee, avecRechercheChemin = False):
        """
        Fonction qui envoie un point d'arrivé au robot sans utiliser la recherche de chemin (segment direct départ-arrivée)
        :param script: point d'arrivé
        :type script: point
        :param avecRechercheChemin: si le segment a été trouvé par la recherche de chemin
        """
        depart = self.getPosition()
        log.logger.info("effectue le segment de départ : ("+str(depart.x)+","+str(depart.y)+") et d'arrivée : ("+str(arrivee.x)+","+str(arrivee.y)+")")
        
        
        delta_x = (arrivee.x-depart.x)
        delta_y = (arrivee.y-depart.y)
        
        """
        oriente le robot pour le segment à parcourir
        sans instruction particulière
        avec un booléen spécifiant que la rotation ne doit pas effectuer de symétrie
        """
        angle = math.atan2(delta_y,delta_x)
        self.gestionTourner(angle,"",avecSymetrie = False)
        
        """
        appel d'une translation de la distance euclidienne depart->arrivée
        sans instruction particulière
        avec un booléen codant l'utilisation de la recherche de chemin
        """
        distance = math.sqrt(delta_x**2+delta_y**2)
        self.gestionAvancer(distance,instruction = "",avecRechercheChemin = avecRechercheChemin)
        
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
        
        ##éventuelle symétrie sur la position d'arrivée
        if __builtin__.constantes['couleur'] == "r":
            arrivee.x *= -1
            
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
        self.hotSpots = self.hotSpotsOriginaux[:]
        print "liste robots adverses : "+str(self.liste_robots_adv)
        for adverse in self.liste_robots_adv:
            log.logger.debug("le noeud "+str(self.hotSpot(adverse))+" a été retiré à cause de l'adverse "+str(adverse))
            print "le noeud "+str(self.hotSpot(adverse))+" a été retiré à cause de l'adverse "+str(adverse)
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
        if self.estDansZone(point,Point(-592,1180),Point(-401,810)) and self.hotSpots[6]:
            return self.hotSpots[6]
        elif self.estDansZone(point,Point(401,1180),Point(592,810)) and self.hotSpots[2]:
            return self.hotSpots[2]
            
        #zone sur le dessus du totem
        elif self.estDansZone(point,Point(-448,1213),Point(-167,1000)) and self.hotSpots[0]:
            return self.hotSpots[0]
        elif self.estDansZone(point,Point(167,1213),Point(448,1000)) and self.hotSpots[0]:
            return self.hotSpots[0]
            
        #zone sur le dessous du totem
        elif self.estDansZone(point,Point(-448,1000),Point(-167,810)) and self.hotSpots[4]:
            return self.hotSpots[4]
        elif self.estDansZone(point,Point(167,1000),Point(448,810)) and self.hotSpots[4]:
            return self.hotSpots[4]
            
        else:
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
        log.logger.debug("suppression du point : "+str(hotspot))
        print "suppression du point : "+str(hotspot)
        print "avant = "+str(self.hotSpots)
        try:
            pos = self.hotSpots.index(hotspot)
            self.hotSpots.pop(pos)
            self.hotSpots.insert(pos,"")
        except: pass
        print "après = "+str(self.hotSpots)
        
    
    def oublierAdverses(self):
        print "on oublie les adverses"
        self.liste_robots_adv = []
        self.hotSpots = self.hotSpotsOriginaux[:]
    
    ############################## </HACK>
    
    
    #def goTo(self, arrivee, numTentatives = 1):
        #"""
        #Fonction qui appelle la recherche de chemin et envoie une liste de coordonnées à la carte asservissement
        #:param depart: point de départ
        #:type depart: Point
        #:param arrivee: point d'arrivée
        #:type arrivee: Point
        #:param chemin: chemin renvoyé par la recherche de chemin
        #:type chemin: liste de points
        #"""
        
        #if numTentatives > 4:
            ##plusieurs recherches de chemin ne suffisent pas à contourner le robot ennemi (il tente sans doute également de nous contourner)
            #raise Exception
        
        ##récupération de la position de départ
        #depart = self.getPosition()
        
        ##éventuelle symétrie sur la position d'arrivée
        #if __builtin__.constantes['couleur'] == "r":
            #arrivee.x *= -1
            
        #log.logger.info("Appel de la recherche de chemin pour le point de départ : ("+str(depart.x)+","+str(depart.y)+") et d'arrivée : ("+str(arrivee.x)+","+str(arrivee.y)+")")
        #chemin_python = self.theta.rechercheChemin(depart,arrivee)
        
        ##supprime le point de départ du chemin.
        ##une exception est levée ici en cas de chemin non trouvé
        #chemin_python.remove(chemin_python[0])
        
        ##on oublie les robots adverses, puisqu'on est censé les éviter
        #self.oublierAdverses()
            
        #for i in chemin_python:
            #log.logger.info("goto (" + str(float(i.x)) + ', ' + str(float(i.y)) + ')')
            
            ##effectue un segment du chemin trouvé, en indiquant que la recherche de chemin a été utilisée
            #self.goToSegment(i,avecRechercheChemin = [arrivee, numTentatives])
        #return "chemin_termine"

    def tourner(self, angle):
        """
        Fonction de script pour faire tourner le robot sur lui même.
        :param angle: Angle à atteindre
        :type angle: Float
        """
        self.serieAsserInstance.ecrire("t")
        self.serieAsserInstance.ecrire(str(float(angle)))
        #log.logger.info("Ordre de tourner à " + str(float(angle)))
        acquittement = False
        debut_timer = int(self.timerAsserv.getTime())
        while not acquittement:
            self.serieAsserInstance.ecrire('acq')
            reponse = str(self.serieAsserInstance.lire())
            if reponse == "FIN_MVT":
                acquittement = True
            elif reponse == "STOPPE":
                print "tourner : stoppé !"
                log.logger.debug("tourner : stoppé !")
                return "stoppe"
            elif int(self.timerAsserv.getTime()) - debut_timer > 8:
                print "tourner : timeout !"
                log.logger.debug("tourner : timeout !")
                return "timeout"
            time.sleep(0.1)
            
        return "acquittement"
    
    def avancer(self, distance):
        """
        Fonction de script pour faire avancer le robot en ligne droite. (distance <0 => reculer)c
        :param distance: Distance à parcourir
        :type angle: Float
        """
        self.serieAsserInstance.ecrire("d")
        self.serieAsserInstance.ecrire(str(float(distance)))
        #log.logger.info("Ordre d'avancer de " + str(float(distance)))
        acquittement = False
        debut_timer = int(self.timerAsserv.getTime())
        while not acquittement:
            self.serieAsserInstance.ecrire('acq')
            reponse = str(self.serieAsserInstance.lire())
            #print "             >"+reponse+"<"
            #print str(reponse)
            if reponse == "FIN_MVT":
                print "avancer : FIN_MVT"
                log.logger.debug("avancer : FIN_MVT")
                acquittement = True
            elif reponse == "STOPPE":
                print "avancer : stoppé !"
                log.logger.debug("avancer : stoppé !")
                return "stoppe"
            else:
                if (int(self.timerAsserv.getTime()) - debut_timer) > 8:
                    print "avancer : timeout !"
                    log.logger.debug("avancer : timeout !")
                    return "timeout"
                elif distance > 0 :
                    capteur = self.capteurInstance.mesurer()
                    if capteur < self.maxCapt:
                        print 'avancer : capteur !'
                        log.logger.debug('avancer : capteur !')
                        return "obstacle"
                
            time.sleep(0.1)
                
        return "acquittement"
            
    def getPosition(self):
        reponseX = ""
        reponseY = ""
        while not (re.match("^(-[0-9]+|[0-9]+)$", reponseX) and re.match("^(-[0-9]+|[0-9]+)$", reponseY)):
            try:
                self.serieAsserInstance.ecrire("pos")
                time.sleep(0.1)
                reponseX = self.serieAsserInstance.lire()
                reponseY = self.serieAsserInstance.lire()
            except:
                pass
        return Point(float(reponseX),float(reponseY))
            
    def setPosition(self,position):
        self.serieAsserInstance.ecrire("cx")
        self.serieAsserInstance.ecrire(str(float(position.x)))
        self.serieAsserInstance.ecrire("cy")
        self.serieAsserInstance.ecrire(str(float(position.y)))
    
    def getOrientation(self):
        reponse = ""
        while not re.match("^(-[0-9]+|[0-9]+)$", reponse):
            try:
                self.serieAsserInstance.ecrire("eo")
                time.sleep(0.1)
                reponse = self.serieAsserInstance.lire()
            except:
                pass
        return float(reponse)/1000.0
            
    def setOrientation(self,orientation):
        self.serieAsserInstance.ecrire("co")
        self.serieAsserInstance.ecrire(str(float(orientation)))
        
            
    def recalage(self):
        self.serieAsserInstance.ecrire("recal")
        log.logger.info("début du recalage")
        acquitement = False
        while not acquitement:
            reponse = self.serieAsserInstance.lire(timeout = False)
            if reponse == "FIN_REC":
                log.logger.info("fin du recalage")
                acquitement = True
            time.sleep(0.1)
        
    def setUnsetAsser(self, asservissement, mode):
        pass
        """
        Arrête ou remet l'asservissement en rotation
        :param asservissement: Définit l'asservissement ciblé (translation ou rotation)
        :type asservissement: string
        :param mode: permet de choisir entre marche et arrêt. 0 = arrêt; 1 = marche
        :type mode: int
        """
        if mode == 0:
            mode = '0'
        else:
            mode = '1'
            
        if asservissement == "rotation":
            asservissement = 'cr'
        else:
            asservissement = 'ct'
        
        self.serieAsserInstance.ecrire(asservissement+mode)
        
    def changerPWM(self, typeAsservissement, valeur):
        if typeAsservissement == "rotation":
            self.serieAsserInstance.ecrire("crm")
            self.serieAsserInstance.ecrire(str(float(valeur)))
        elif typeAsservissement == "translation":
            self.serieAsserInstance.ecrire("ctm")
            self.serieAsserInstance.ecrire(str(float(valeur)))
            
    def changerVitesse(self, typeAsservissement, valeur):
        """
        spécifie une vitesse prédéfinie en translation ou rotation
        une valeur 1,2,3 est attendue
        1 : vitesse "prudente"
        2 : vitesse normale
        3 : vitesse pour forcer
        """
        if typeAsservissement == "rotation":
            self.serieAsserInstance.ecrire("crv"+str(int(valeur)))
            self.vitesseRotation = int(valeur)
        elif typeAsservissement == "translation":
            self.serieAsserInstance.ecrire("ctv"+str(int(valeur)))
            self.vitesseTranslation = int(valeur)
            
    def getVitesse(self, typeAsservissement):
        if typeAsservissement == "rotation":
            return self.vitesseRotation
        elif typeAsservissement == "translation":
            return self.vitesseTranslation
        
    def immobiliser(self):
        self.serieAsserInstance.ecrire('stop')
        
    def gestionAvancer(self, distance, instruction = "", avecRechercheChemin = False, numTentatives = 1):
        """
        méthode de haut niveau pour translater le robot
        prend en paramètre la distance à parcourir en mm
        et en facultatif une instruction "auStopNeRienFaire" ou "finir"
        """
        
        print "#avancer à "+str(distance)+", "+instruction
        log.logger.debug("#avancer à "+str(distance)+", "+instruction)
        
        posAvant = self.getPosition()
        retour = self.avancer(distance)
        
        if retour == "timeout" or (retour == "stoppe" and not instruction):
            ##1
            #stopper le robot
            self.immobiliser()
            if instruction == "sansRecursion":
                if self.estInaccessible(self.getPosition()):
                    self.degager()
                #stopper l'execution du script parent
                raise Exception
                
            else:
                #reculer de ce qui a été avancé
                posApres = self.getPosition()
                dist = math.sqrt((posApres.x - posAvant.x) ** 2 + (posApres.y - posAvant.y) ** 2)
                if distance != 0: 
                    signe = distance/abs(distance)
                else:
                    signe = 1
                self.gestionAvancer(-signe*dist,"sansRecursion")
                #recommencer le déplacement
                self.gestionAvancer(distance,"sansRecursion")
        
        if retour == "obstacle" and not instruction == "oublierCapteur":
            orientation = self.getOrientation()
            position = self.getPosition()
            largeur_robot = profils.develop.constantes.constantes["Coconut"]["largeurRobot"]
            tableLargeur = constantes["Coconut"]["longueur"]
            tableLongueur = constantes["Coconut"]["largeur"]
            adverse = Point(position.x + (self.maxCapt/2+self.rayonRobotsAdverses+largeur_robot/2)*math.cos(orientation),position.y + (self.maxCapt/2+self.rayonRobotsAdverses+largeur_robot/2)*math.sin(orientation))
            
            if (adverse.x > -tableLongueur/2+100 and adverse.x < tableLongueur/2-100 and adverse.y < tableLargeur-100 and adverse.y > 100):
                #le point détecté est bien dans l'aire de jeu, c'est sans doute un robot adverse
                
                print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
                print "ennemi en vue à "+str(adverse)
                print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
                log.logger.debug("ennemi en vue à "+str(adverse))
                self.immobiliser()
            
                if avecRechercheChemin or instruction == "sansRecursion":
                    #robot adverse
                    self.oublierAdverses()
                    self.liste_robots_adv.append(adverse)
                    #stopper l'execution du script parent
                    raise Exception
                else:
                    #attente que la voie se libère
                    ennemi_en_vue = True
                    debut_timer = int(self.timerAsserv.getTime())
                    while ennemi_en_vue and (int(self.timerAsserv.getTime()) - debut_timer) < 4 :
                        capteur = self.capteurInstance.mesurer()
                        if capteur < self.maxCapt:
                            print 'gestionAvancer : capteur !'
                            log.logger.debug('gestionAvancer : capteur !')
                        else :
                            print 'gestionAvancer : la voie est libre !'
                            log.logger.debug('gestionAvancer : la voie est libre !')
                            ennemi_en_vue = False
                        time.sleep(0.05)
                        
                    if not ennemi_en_vue:
                        #vider la liste des robots adverses repérés
                        self.oublierAdverses()
                        
                        #finir le déplacement
                        posApres = self.getPosition()
                        dist = math.sqrt((posApres.x - posAvant.x) ** 2 + (posApres.y - posAvant.y) ** 2)
                        if distance != 0:
                            signe = distance/abs(distance)
                        else:
                            signe = 1
                        self.gestionAvancer(distance-signe*dist)
                        
                    else:
                        #robot adverse
                        self.oublierAdverses()
                        self.liste_robots_adv.append(adverse)
                        #stopper l'execution du script parent
                        raise Exception
                        
            else:
                #fausse alerte : on termine tranquil'
                print "fausse alerte. pos à "+str(position)+", adverse à "+str(adverse)+"."
                log.logger.debug("fausse alerte. pos à "+str(position)+", adverse à "+str(adverse)+".")
                
                dist = math.sqrt((position.x - posAvant.x) ** 2 + (position.y - posAvant.y) ** 2)
                if distance != 0:
                    signe = distance/abs(distance)
                else:
                    signe = 1
                self.gestionAvancer(distance-signe*dist,"oublierCapteur")
                    
        if retour == "stoppe" and instruction == "sansRecursion":
            if self.estInaccessible(self.getPosition()):
                self.degager()
            #stopper l'execution du script parent
            raise Exception
            
        if retour == "stoppe" and instruction == "finir":
            
            if numTentatives == 1:
                #finir le déplacement
                self.sauvOrient = self.getOrientation()
                posApres = self.getPosition()
                dist = math.sqrt((posApres.x - posAvant.x) ** 2 + (posApres.y - posAvant.y) ** 2)
                if distance != 0:
                    signe = distance/abs(distance)
                else:
                    signe = 1
                self.gestionAvancer(distance-signe*dist,instruction = "finir",numTentatives = numTentatives+1)
                
            elif numTentatives == 2:
                if distance != 0:
                    signe = distance/abs(distance)
                else:
                    signe = 1
                #reculer
                self.changerVitesse("translation", 3)
                self.gestionAvancer(-signe*20,"auStopNeRienFaire")
                self.changerVitesse("translation", 2)
                
                #se réasservir en rotation
                self.changerVitesse("rotation", 3)
                self.gestionTourner(self.sauvOrient, avecSymetrie = False)
                self.changerVitesse("rotation", 2)
                
                #replier un peu les bras
                if hasattr(__builtin__.instance, 'actionInstance'):
                    actionInstance = __builtin__.instance.actionInstance
                    actionInstance.deplacer(100)
                    time.sleep(0.3)
                    actionInstance.deplacer(120)
                    time.sleep(0.3)
                #finir le déplacement
                posApres = self.getPosition()
                dist = math.sqrt((posApres.x - posAvant.x) ** 2 + (posApres.y - posAvant.y) ** 2)
                if distance != 0:
                    signe = distance/abs(distance)
                else:
                    signe = 1
                self.gestionAvancer(distance-signe*dist,instruction = "finir",numTentatives = numTentatives+1)
                
                
            elif numTentatives == 3:
                
                #se réasservir en rotation
                self.changerVitesse("rotation", 3)
                self.gestionTourner(self.sauvOrient, avecSymetrie = False)
                self.changerVitesse("rotation", 2)
                
                if distance != 0:
                    signe = distance/abs(distance)
                else:
                    signe = 1
                #forcer
                self.changerVitesse("translation", 3)
                self.gestionAvancer(signe*20,"auStopNeRienFaire")
                self.changerVitesse("translation", 2)
                
                #replier un peu les bras
                if hasattr(__builtin__.instance, 'actionInstance'):
                    actionInstance = __builtin__.instance.actionInstance
                    actionInstance.deplacer(70)
                    time.sleep(0.3)
                    actionInstance.deplacer(130)
                    time.sleep(0.3)
                    actionInstance.deplacer(120)
                    time.sleep(0.3)
                #finir le déplacement
                posApres = self.getPosition()
                dist = math.sqrt((posApres.x - posAvant.x) ** 2 + (posApres.y - posAvant.y) ** 2)
                self.gestionAvancer(distance-signe*dist,instruction = "finir",numTentatives = numTentatives+1)
            
            elif numTentatives == 4:
                #reculer et tourner un peu
                self.changerVitesse("translation", 3)
                self.gestionAvancer(-signe*50,"auStopNeRienFaire")
                self.changerVitesse("translation", 2)
                
                self.changerVitesse("rotation", 3)
                self.gestionTourner(self.sauvOrient+0.08,instruction = "auStopNeRienFaire", avecSymetrie = False)
                self.gestionTourner(self.sauvOrient-0.08,instruction = "auStopNeRienFaire", avecSymetrie = False)
                self.gestionTourner(self.sauvOrient, avecSymetrie = False)
                self.changerVitesse("rotation", 2)
                
                #finir le déplacement
                posApres = self.getPosition()
                dist = math.sqrt((posApres.x - posAvant.x) ** 2 + (posApres.y - posAvant.y) ** 2)
                if distance != 0:
                    signe = distance/abs(distance)
                else:
                    signe = 1
                self.gestionAvancer(distance-signe*dist,instruction = "finir",numTentatives = numTentatives+1)
            
            elif numTentatives >= 5:
                #soucis
                if self.estInaccessible(self.getPosition()):
                    self.degager()
                raise Exception
            
    def gestionTourner(self, angle, instruction = "", avecSymetrie = True):
        
        """
        méthode de haut niveau pour tourner le robot
        prend en paramètre l'angle à parcourir en radians
        et en facultatif une instruction "auStopNeRienFaire" ou "finir"
        ainsi qu'un booléen indiquant si la rotation doit effectuer une symétrie selon la couleur
        """
        
        if avecSymetrie:
            #l'angle spécifié dans les scripts est valable pour un robot violet.
            if __builtin__.constantes['couleur'] == "r":
                angle = math.pi - angle

        #angle dans ]-pi,pi]
        while angle > math.pi:
            angle -= 2*math.pi
        while angle < -math.pi:
            angle += 2*math.pi
        
        print "#tourner à "+str(angle)+", "+instruction
        log.logger.debug("#tourner à "+str(angle)+", "+instruction)
        
        orientAvant = self.getOrientation()
        retour = self.tourner(angle)
        
        if retour == "timeout" or (retour == "stoppe" and not instruction):
            
            #stopper le robot
            self.immobiliser()
            if instruction == "sansRecursion":
                if self.estInaccessible(self.getPosition()):
                    self.degager()
                #stopper l'execution du script parent
                raise Exception
                
            else:
                ##1
                #tourner inversement à ce qui a été tourné
                self.gestionTourner(orientAvant,"sansRecursion",avecSymetrie = False)
                #recommencer le déplacement
                self.gestionTourner(angle,"sansRecursion",avecSymetrie = False)
        
        if retour == "stoppe" and instruction == "sansRecursion":
            if self.estInaccessible(self.getPosition()):
                self.degager()
            #stopper l'execution du script parent
            raise Exception
            
        if retour == "stoppe" and instruction == "finir":
            ##5
            #augmenter vitesse
            self.changerVitesse("rotation", 3)
            #finir le déplacement
            self.gestionTourner(angle,avecSymetrie = False)
            #remettre vitesse
            self.changerVitesse("rotation", 2)
        
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
        
        
    """
    accesseurs direct au PWM pour la borne d'arcade
    (nécessite un flash spécial)
    """
    def moteurGauche(self, vitesse):
        self.serieAsserInstance.ecrire("pwmG")
        self.serieAsserInstance.ecrire(str(vitesse))
        
    def moteurDroit(self, vitesse):
        self.serieAsserInstance.ecrire("pwmD")
        self.serieAsserInstance.ecrire(str(vitesse))                

    def attendre(self, temps):
        time.sleep(temps)