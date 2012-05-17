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
        self.theta = __builtin__.instance.theta
        
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
        self.maxCapt = 400
        
        #couleur du robot
        if __builtin__.constantes['couleur'] == "r":
            self.serieAsserInstance.ecrire('ccr')
        
        
        #liste des centres de robots adverses repérés (liste de points)
        self.liste_robots_adv = __builtin__.instance.liste_robots_adv
        
        #rayon moyen des robots adverses
        self.rayonRobotsAdverses = constantes["Recherche_Chemin"]["rayonRobotsA"]
        
        #timer pour les timeout
        self.timerAsserv = timer.Timer()
        
        self.vitesseTranslation = 2
        self.vitesseRotation = 2
        
        self.hotSpots = [Point(-900,1000),Point(-800,1420),Point(-360,1660),Point(360,1660),Point(800,1420),Point(900,1000),Point(540,290),Point(-540,290)]
            
    
    def goToSegment(self, arrivee, avecRechercheChemin = []):
        """
        Fonction qui envoie un point d'arrivé au robot sans utiliser la recherche de chemin (segment direct départ-arrivée)
        :param script: point d'arrivé
        :type script: point
        :param avecRechercheChemin: si le segment a été trouvé par la recherche de chemin : contient de quoi créer une recursion.
        :type avecRechercheChemin: list
        """
        depart = self.getPosition()
        log.logger.info("effectue le segment de départ : ("+str(depart.x)+","+str(depart.y)+") et d'arrivée : ("+str(arrivee.x)+","+str(arrivee.y)+")")
        
        delta_x = (arrivee.x-depart.x)
        delta_y = (arrivee.y-depart.y)
        angle = math.atan2(delta_y,delta_x)
        
        log.logger.info("effectue un segment de départ : ("+str(depart.x)+","+str(depart.y)+") et d'arrivée : ("+str(arrivee.x)+","+str(arrivee.y)+")")
        
        """
        oriente le robot pour le segment à parcourir
        sans instruction particulière
        avec un booléen spécifiant que la rotation ne doit pas effectuer de symétrie
        """
        self.gestionTourner(angle,"",avecSymetrie = False)
        
        """
        appel d'une translation de la distance euclidienne depart->arrivée
        sans instruction particulière
        avec un booléen codant l'utilisation de la recherche de chemin
        """
        self.gestionAvancer(math.sqrt(delta_x**2+delta_y**2),instruction = "",avecRechercheChemin = avecRechercheChemin)
    
    
    ############################## <HACK>
    
    
    
    def goToScript(self, arrivee):
        depart = self.getPosition()
        log.logger.info("Appel de la recherche de chemin basique pour le point de départ : ("+str(depart.x)+","+str(depart.y)+") et d'arrivée : ("+str(arrivee.x)+","+str(arrivee.y)+")")
        
        HSdepart = self.hotSpot(depart)
        HSarrivee = self.hotSpot(arrivee)
        
        repere = HSdepart
        while not repere == HSarrivee:
            self.goToSegment(repere)
            repere = self.HotSpotSuivant(repere,HSarrivee)
        self.goToSegment(HSarrivee)
        self.goToSegment(arrivee)
        
    def HotSpotSuivant(self,HSdepart,HSarrivee):
         #retourne le hotspot suivant pour effectuer le trajet
        
        if HSdepart == HSarrivee :
            return HSdepart
        else:
        
            for k in range(len(self.hotSpots)):
                
                if self.hotSpots[k] == HSdepart:
                    dep = k
                if self.hotSpots[k] == HSarrivee:
                    arr = k
                    
            if (dep - arr)%len(self.hotSpots) < len(self.hotSpots)/2.:
                sens = -1
            else:
                sens = 1
            return self.hotSpots[dep+sens]
        
    def hotSpot(self, point):
        #détermine le hotspot le plus proche à partir d'un point de la carte
        
        #zone sur le coté du totem
        if self.estDansZone(point,Point(-592,1180),Point(-401,810)):
            return self.hotSpots[0]
        elif self.estDansZone(point,Point(401,1180),Point(592,810)):
            return self.hotSpots[5]
            
        #zone sur le dessus du totem
        elif self.estDansZone(point,Point(-448,1213),Point(-167,1000)):
            return self.hotSpots[2]
        elif self.estDansZone(point,Point(167,1213),Point(448,1000)):
            return self.hotSpots[3]
            
        #zone sur le dessous du totem
        elif self.estDansZone(point,Point(-448,1000),Point(-167,810)):
            return self.hotSpots[7]
        elif self.estDansZone(point,Point(167,1000),Point(448,810)):
            return self.hotSpots[6]
            
        else:
        
            dest = self.hotSpots[0]
            for hs in self.hotSpots:
                if ((hs.x - point.x)**2 + (hs.y - point.y)**2) < ((dest.x - point.x)**2 + (dest.y - point.y)**2) :
                    dest = hs
            return dest
        
    def estDansZone(self,point,hg,bd):
        if (point.x > hg.x and point.x < bd.x and point.y < hg.y and point.y > bd.y):
            return True
        else:
            return False
    
    
    ############################## </HACK>
    
    
    def goTo(self, arrivee, numTentatives = 1):
        """
        Fonction qui appelle la recherche de chemin et envoie une liste de coordonnées à la carte asservissement
        :param depart: point de départ
        :type depart: Point
        :param arrivee: point d'arrivée
        :type arrivee: Point
        :param chemin: chemin renvoyé par la recherche de chemin
        :type chemin: liste de points
        """
        
        if numTentatives > 4:
            #plusieurs recherches de chemin ne suffisent pas à contourner le robot ennemi (il tente sans doute également de nous contourner)
            raise Exception
        
        #récupération de la position de départ
        depart = self.getPosition()
        
        #éventuelle symétrie sur la position d'arrivée
        if __builtin__.constantes['couleur'] == "r":
            arrivee.x *= -1
            
        log.logger.info("Appel de la recherche de chemin pour le point de départ : ("+str(depart.x)+","+str(depart.y)+") et d'arrivée : ("+str(arrivee.x)+","+str(arrivee.y)+")")
        chemin_python = self.theta.rechercheChemin(depart,arrivee)
        
        #supprime le point de départ du chemin.
        #une exception est levée ici en cas de chemin non trouvé
        chemin_python.remove(chemin_python[0])
        
        #on oublie les robots adverses, puisqu'on est censé les éviter
        __builtin__.instance.viderListeRobotsAdv()
            
        for i in chemin_python:
            log.logger.info("goto (" + str(float(i.x)) + ', ' + str(float(i.y)) + ')')
            
            #effectue un segment du chemin trouvé, en indiquant que la recherche de chemin a été utilisée
            self.goToSegment(i,avecRechercheChemin = [arrivee, numTentatives])
        return "chemin_termine"

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
                return "stoppe"
            elif int(self.timerAsserv.getTime()) - debut_timer > 8:
                print "tourner : timeout !"
                return "timeout"
            #time.sleep(0.05)
            
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
            print "             >"+reponse+"<"
            if reponse == "FIN_MVT":
                print "avancer : FIN_MVT"
                acquittement = True
            elif reponse == "STOPPE":
                print "avancer : stoppé !"
                return "stoppe"
            else:
                if (int(self.timerAsserv.getTime()) - debut_timer) > 8:
                    print "avancer : timeout !"
                    return "timeout"
                elif distance > 0 :
                    capteur = self.capteurInstance.mesurer()
                    if capteur < self.maxCapt:
                        print 'avancer : capteur !'
                        return "obstacle"
                
            #time.sleep(0.05)
                
        return "acquittement"
            
    def getPosition(self):
        while 42:
            try:
                reponseX = ""
                reponseY = ""
                while not (re.match("^(-[0-9]+|[0-9]+)$", reponseX) and re.match("^(-[0-9]+|[0-9]+)$", reponseY)):
                    self.serieAsserInstance.ecrire("pos")
                    reponseX = self.serieAsserInstance.lire()
                    reponseY = self.serieAsserInstance.lire()
                pos = Point(float(reponseX),float(reponseY))
                return pos
            except:
                pass
            
    def setPosition(self,position):
        self.serieAsserInstance.ecrire("cx")
        self.serieAsserInstance.ecrire(str(float(position.x)))
        self.serieAsserInstance.ecrire("cy")
        self.serieAsserInstance.ecrire(str(float(position.y)))
    
    def getOrientation(self):
        while 42:
            try:
                reponse = ""
                while not re.match("^(-[0-9]+|[0-9]+)$", reponse):
                    self.serieAsserInstance.ecrire("eo")
                    reponse = self.serieAsserInstance.lire()
                orientation = float(reponse)/1000.0
                #self.robotInstance.setOrientation(orientation)
                return orientation
            except:
                pass
            
    def setOrientation(self,orientation):
        self.serieAsserInstance.ecrire("co")
        self.serieAsserInstance.ecrire(str(float(orientation)))
        
            
    def recalage(self):
        self.serieAsserInstance.ecrire("recal")
        log.logger.info("début du recalage")
        acquitement = False
        while not acquitement:
            reponse = self.serieAsserInstance.lire()
            if reponse == "FIN_REC":
                log.logger.info("fin du recalage")
                acquitement = True
            #time.sleep(0.05)
        
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
        
    def gestionAvancer(self, distance, instruction = "", avecRechercheChemin = [], numTentatives = 1):
        """
        méthode de haut niveau pour translater le robot
        prend en paramètre la distance à parcourir en mm
        et en facultatif une instruction "auStopNeRienFaire" ou "finir"
        """
        
        print "#avancer à "+str(distance)+", "+instruction
        
        posAvant = self.getPosition()
        retour = self.avancer(distance)
        
        if retour == "timeout" or (retour == "stoppe" and not instruction):
            ##1
            #stopper le robot
            self.immobiliser()
            if instruction == "sansRecursion":
                ##4
                #mettre à jour l'attribut position du robot
                
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
        
        if retour == "obstacle" :
            ##2 
            #ajoute un robot adverse sur la table, pour la recherche de chemin
            #stopper le robot
                
            orientation = self.getOrientation()
            position = self.getPosition()
            largeur_robot = profils.develop.constantes.constantes["Coconut"]["largeurRobot"]
            tableLargeur = constantes["Coconut"]["longueur"]
            tableLongueur = constantes["Coconut"]["largeur"]
            adverse = Point(position.x + (self.maxCapt+self.rayonRobotsAdverses+largeur_robot/2)*math.cos(orientation),position.y + (self.maxCapt+self.rayonRobotsAdverses+largeur_robot/2)*math.sin(orientation))
            
            if (adverse.x > -tableLongueur/2+100 and adverse.x < tableLongueur/2-100 and adverse.y < tableLargeur-100 and adverse.y > 100):
                #le point détecté est bien dans l'aire de jeu, c'est sans doute un robot adverse
                
                print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
                print "ennemi en vue à "+str(adverse)
                print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
                self.immobiliser()
            
                if avecRechercheChemin :
                    #robot adverse
                    __builtin__.instance.viderListeRobotsAdv(recalculer = False)
                    __builtin__.instance.ajouterRobotAdverse(adverse)
                    
                    #est-il rentable de relancer une recherche de chemin ?
                    self.asserInstanceDuree.setPosition(position)
                    self.asserInstanceDuree.lancerChrono()
                    self.asserInstanceDuree.goTo(destination)
                    if self.asserInstanceDuree.mesurerChrono() < __builtin__.instance.timeout:
                        #le contretemps est quand meme plus profitable que de changer de script
                        
                        #avecRechercheChemin est une liste dont les éléments permettent de lancer un appel récursif
                        destination = avecRechercheChemin[0]
                        new_numTentatives = avecRechercheChemin[1] + 1
                        self.goTo(destination, new_numTentatives)
                    else:
                        #la stratégie connait un script plus avantageux que de retenter un goTo pour le script courant
                        raise Exception
                    
                elif instruction == "sansRecursion":
                    ##4
                    #robot adverse
                    __builtin__.instance.ajouterRobotAdverse(adverse)
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
                        else :
                            print 'gestionAvancer : la voie est libre !'
                            ennemi_en_vue = False
                        
                    if not ennemi_en_vue:
                        #vider la liste des robots adverses repérés
                        if not __builtin__.instance.liste_robots_adv == []:
                            __builtin__.instance.viderListeRobotsAdv()
                        
                        #baisser vitesse
                        #self.changerVitesse("translation", 1)
                        
                        #finir le déplacement
                        posApres = self.getPosition()
                        dist = math.sqrt((posApres.x - posAvant.x) ** 2 + (posApres.y - posAvant.y) ** 2)
                        if distance != 0:
                            signe = distance/abs(distance)
                        else:
                            signe = 1
                        self.gestionAvancer(distance-signe*dist, "sansRecursion")
                        
                        #remettre vitesse
                        #self.changerVitesse("translation", 2)
                        
                    else:
                        #robot adverse
                        __builtin__.instance.ajouterRobotAdverse(adverse)
                        #stopper l'execution du script parent
                        raise Exception
                        
            else:
                #fausse alerte : on termine tranquil'
                print "fausse alerte. pos à "+str(position)+", adverse à "+str(adverse)+"."
                if instruction == "sansRecursion":
                    #stopper l'execution du script parent
                    raise Exception
                else:
                    dist = math.sqrt((position.x - posAvant.x) ** 2 + (position.y - posAvant.y) ** 2)
                    if distance != 0:
                        signe = distance/abs(distance)
                    else:
                        signe = 1
                    self.gestionAvancer(distance-signe*dist,"sansRecursion")
                    
        if retour == "stoppe" and instruction == "sansRecursion":
            #stopper l'execution du script parent
            raise Exception
            
        if retour == "stoppe" and instruction == "finir":
            
            if numTentatives <= 2:
                #finir le déplacement
                posApres = self.getPosition()
                dist = math.sqrt((posApres.x - posAvant.x) ** 2 + (posApres.y - posAvant.y) ** 2)
                if distance != 0:
                    signe = distance/abs(distance)
                else:
                    signe = 1
                self.gestionAvancer(distance-signe*dist,instruction = "finir",numTentatives = numTentatives+1)
                
            elif numTentatives == 3:
                
                #replier un peu les bras
                if hasattr(__builtin__.instance, 'actionInstance'):
                    actionInstance = __builtin__.instance.actionInstance
                    actionInstance.deplacer(100)
                    time.sleep(0.3)
                    actionInstance.deplacer(130)
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
                
                
            elif numTentatives == 4:
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
                    actionInstance.deplacer(135)
                    time.sleep(0.3)
                    actionInstance.deplacer(120)
                    time.sleep(0.3)
                #finir le déplacement
                posApres = self.getPosition()
                dist = math.sqrt((posApres.x - posAvant.x) ** 2 + (posApres.y - posAvant.y) ** 2)
                self.gestionAvancer(distance-signe*dist,instruction = "finir",numTentatives = numTentatives+1)
            
            elif numTentatives == 5:
                #reculer et tourner un peu
                self.changerVitesse("translation", 3)
                self.gestionAvancer(-signe*50,"auStopNeRienFaire")
                self.changerVitesse("translation", 2)
                
                self.changerVitesse("rotation", 3)
                orientation = self.getOrientation()
                self.gestionTourner(orientation+0.08,instruction = "auStopNeRienFaire", avecSymetrie = False)
                self.gestionTourner(orientation-0.08,instruction = "auStopNeRienFaire", avecSymetrie = False)
                self.gestionTourner(orientation, avecSymetrie = False)
                self.changerVitesse("rotation", 2)
                
                #finir le déplacement
                posApres = self.getPosition()
                dist = math.sqrt((posApres.x - posAvant.x) ** 2 + (posApres.y - posAvant.y) ** 2)
                if distance != 0:
                    signe = distance/abs(distance)
                else:
                    signe = 1
                self.gestionAvancer(distance-signe*dist,instruction = "finir",numTentatives = numTentatives+1)
            
            elif numTentatives >= 6:
                #soucis
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
        
        orientAvant = self.getOrientation()
        retour = self.tourner(angle)
        
        if retour == "timeout" or (retour == "stoppe" and not instruction):
            
            #stopper le robot
            self.immobiliser()
            if instruction == "sansRecursion":
                ##4
                #mettre à jour l'attribut position du robot
                
                #stopper l'execution du script parent
                raise Exception
                
            else:
                ##1
                #tourner inversement à ce qui a été tourné
                self.gestionTourner(orientAvant,"sansRecursion",avecSymetrie = False)
                #recommencer le déplacement
                self.gestionTourner(angle,"sansRecursion",avecSymetrie = False)
        
        if retour == "stoppe" and instruction == "sansRecursion":
            ##4
            #mettre à jour l'attribut orientation du robot
            
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
        
    def afficherMenu(self):
        print """
        Indiquer l'action à effectuer :
        Quitter-------------------------------[0]
        Zone de départ------------------------[1]
        Constante de rotation-----------------[2]
        Constante de translation--------------[3]
        Changer la position courante-----------[4]
        Activer/Désactiver l'asservissement---[5]
        Afficher des valeurs------------------[6]
        Ping de la liaison série--------------[7]
        """

    def afficherSousMenu(self):
        print """
        Revenir au menu-----------------------[0]
        Changer la dérivée--------------------[1]
        Changer l'intégration-----------------[2]
        Changer le proportionnel--------------[3]
        Mettre le max du PWM------------------[4]
        """
        
    def modifierConstantes(self):
        self.afficherMenu()
        main_exit = False
        while not main_exit:
            
            choix = raw_input()
            #Quitter
            if choix == '0':
                main_exit = True
                pass
            #Définir la zone de départ
            elif choix == '1':
                couleur = raw_input("Indiquer la zone de départ (r/v)")
                message = 'cc' + str(couleur)
                self.serieAsserInstance.ecrire(message)
                self.afficherMenu()
            #Définir les constantes de rotation
            elif choix == '2':
                exit = False
                valeurs = {"1" : "d", "2" : "i", "3" : "p", "4" : "m"}
                while not exit:
                    self.afficherSousMenu()
                    choix = raw_input()
                    message = "cr"
                    
                    if choix != '0':
                        constante = raw_input("Indiquer la valeur de la constante :")
                        message += str(valeurs[choix]) + '' + str(constante)
                        self.serieAsserInstance.ecrire(message)
                    
                    else:
                        exit = True
                        self.afficherMenu()
            #Définir les constantes de translation
            elif choix == '3':
                exit = False
                valeurs = {"1" : "d", "2" : "i", "3" : "p", "4" : "m"}
                while not exit:
                    self.afficherSousMenu()
                    choix = raw_input()
                    message = "ct"
                    
                    if choix != '0':
                        constante = raw_input("Indiquer la valeur de la constante :")
                        message += valeurs[choix] + '' + str(constante)
                        self.serieAsserInstance.ecrire(message)
                    
                    else:
                        exit = True
                        self.afficherMenu()
            #Définir la position courante
            elif choix == '4':
                print "Ne pas rentrer de valeur pour une coordonée permet de laisser la valeur déjà enregistrée sur l'AVR"
                coordonneX = raw_input("Rentrer a coordonée en x : ")
                if coordonneX:
                    message = 'cx' + str(coordonneX)
                    self.serieAsserInstance.ecrire(message)
                
                coordonneY = raw_input("Rentrer a coordonée en y: ")
                if coordonneY:
                    message = 'cy' + str(coordonneY)
                    self.serieAsserInstance.ecrire(message)
                
                self.afficherMenu()
            #Activer ou désactiver l'asservissement
            elif choix == '5':
                exit = False
                while not exit:
                    print """
                    Revenir au menu-----------------------[0]
                    Activer la rotation-------------------[1]
                    Désactiver la rotation----------------[2]
                    Activer la translation----------------[3]
                    Désactiver la translation-------------[4]
                    """
                    constante = raw_input()
                    if constante == '1':
                        message = 'sr'
                        self.serieAsserInstance.ecrire(message)
                    elif constante == '2':
                        message = 'dr'
                        self.serieAsserInstance.ecrire(message)
                    elif constante == '3':
                        message = 'st'
                        self.serieAsserInstance.ecrire(message)
                    elif constante == '4':
                        message = 'dt'
                        self.serieAsserInstance.ecrire(message)
                    elif constante == '0':
                        exit = True
                        self.afficherMenu()
            #Afficher les constantes enregistrées dans l'AVR
            elif choix == '6':
                exit = False
                while not exit:
                    print """
                    Revenir au menu------------------------------------[0]
                    Afficher la couleur--------------------------------[1]
                    Afficher la rotation-------------------------------[2]
                    Afficher la translation----------------------------[3]
                    Afficher le type d'asservissement------------------[4]
                    Afficher les coordonnées enregistrées--------------[5]
                    """
                    choix = raw_input()
                    if choix == '0':
                        exit = True
                        self.afficherMenu()
                        
                    elif choix == '1':
                        message = 'ec'
                        
                    elif choix == '2':
                        exit = False
                        valeurs = {"1" : "d", "2" : "i", "3" : "p", "4" : "m"}
                        while not exit:
                            self.afficherSousMenu()
                            choix = raw_input()
                            if choix == '0':
                                exit = True
                                self.afficherMenu()
                            else:
                                message = 'er' + valeurs[choix]
                                self.serieAsserInstance.ecrire(message)
                    elif choix == '3':
                        exit = False
                        valeurs = {"1" : "d", "2" : "i", "3" : "p", "4" : "m"}
                        while not exit:
                            self.afficherSousMenu()
                            choix = raw_input()
                            if choix == '0':
                                exit = True
                                self.afficherMenu()
                            else:
                                message = 'et' + valeurs[choix]
                                self.serieAsserInstance.ecrire(message)
                    elif choix == '4':
                        self.serieAsserInstance.ecrire('es')
                    elif choix =='5':
                        exit = False
                        while not exit:
                            self.serieAsserInstance.ecrire('ex')
                            answer = False
                            while not answer:
                                while not self.serieAsserInstance.file_attente.empty():
                                    print self.serieAsserInstance.file_attente.get()
                                    answer = True
                                    self.afficherSousMenu()
                            self.serieAsserInstance.ecrire('ye')
                            while not answer:
                                while not self.serieAsserInstance.file_attente.empty():
                                    print self.serieAsserInstance.file_attente.get()
                                    answer = True
                                    self.afficherSousMenu()
            elif choix == '7':
                exit = False
                while not exit:
                    self.serieAsserInstance.ecrire('?')
                    
            else:
                print "Il faut choisir une valeur contenue dans le menu."
                
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
        
    def getZone(self) :
        
        couleur = __builtin__.constantes["couleur"]
        
        if couleur == "v" :
            if self.getPosition().x >= 0 and self.getPosition().y <= 1500:
                return 1
            elif self.getPosition().x >= 0 and self.getPosition().y > 1500 :
                return 2
            elif self.getPosition().x < 0 and self.getPosition().y <= 1500 :
                return 4
            elif self.getPosition().x < 0 and self.getPosition().y > 1500 :
                return 3
                
        else :
            if self.getPosition().x < 0 and self.getPosition().y <= 1500:
                return 1
            elif self.getPosition().x < 0 and self.getPosition().y > 1500 :
                return 2
            elif self.getPosition().x >= 0 and self.getPosition().y <= 1500 :
                return 4
            elif self.getPosition().x >= 0 and self.getPosition().y > 1500 :
                return 3