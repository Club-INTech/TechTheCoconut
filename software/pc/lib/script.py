# -*- coding: utf-8 -*-

import log
import sys
import __builtin__
import time
from outils_math.point import Point
import lib.log
import os
import math

log = lib.log.Log(__name__)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

class Script:
    
    def __init__(self):
        if hasattr(__builtin__.instance, 'asserInstance'):
            self.asserInstance = __builtin__.instance.asserInstance
        else:
            log.logger.error("script : ne peut importer instance.asserInstance")
            
        if hasattr(__builtin__.instance, 'asserInstanceDuree'):
            self.asserInstanceDuree = __builtin__.instance.asserInstanceDuree
        else:
            log.logger.error("script : ne peut importer instance.asserInstanceDuree")
        if hasattr(__builtin__.instance, 'robotInstance'):
            self.robotInstance = __builtin__.instance.robotInstance
        else:
            log.logger.error("script : ne peut importer instance.robotInstance")
        if hasattr(__builtin__.instance, 'actionInstance') :
            self.actionInstance = __builtin__.instance.actionInstance
        else:
            log.logger.error("script : ne peut importer instance.actionInstance")
    
        self.couleur = __builtin__.constantes["couleur"]
        
    def recalage(self):
        """
        Fonction permettant de recaller le robot dans un coin de la table
        """
        
        self.asserInstance.recalage()
        
    def homologation(self):
        
        #stocke le lingot et enfonce un poussoir
        
        try:
            print self.asserInstance.getPosition()
            self.asserInstance.changerVitesse("translation",1)
            self.asserInstance.changerVitesse("rotation",1)
            self.asserInstance.gestionAvancer(250)     # On sort de la zone départ
            self.asserInstance.gestionTourner(1.57)     # On se dirige vers le Nord
            self.asserInstance.gestionAvancer(600)     # On avance jusqu'au lingots
            print "couleur : " + self.couleur + "\n"
            self.asserInstance.gestionTourner(0.0)  
            
            self.asserInstance.gestionAvancer(300)     # On le rentre dans la calle
            self.asserInstance.gestionAvancer(-300)    # On ressort de la calle
            self.asserInstance.gestionTourner(1.57)     # On se tourne vers le boutton poussoir
            self.asserInstance.changerVitesse("translation",2)
            self.asserInstance.changerVitesse("rotation",2)
            self.asserInstance.gestionAvancer(70)     # On avance vers lui
            self.asserInstance.gestionTourner(-1.57)    # On lui montre nos fesses
            self.asserInstance.gestionAvancer(-480,"auStopNeRienFaire")    # On recule pour lui mettre sa dose
            self.asserInstance.changerVitesse("translation",3)
            self.asserInstance.gestionAvancer(-500.0,"auStopNeRienFaire")  # Pour l'enfoncer à fond
            self.asserInstance.gestionAvancer(200)
            self.asserInstance.gestionTourner(-1.57)    # réorientation du robot
            self.asserInstance.gestionAvancer(500)    # On se barre.
            
        except:
            print "detection capteur"
            reponse = "lulz"
            while not reponse == "STOPPE":
                self.asserInstance.serieAsserInstance.ecrire('stop')
                self.asserInstance.serieAsserInstance.ecrire('acq')
                reponse = self.asserInstance.serieAsserInstance.lire()

            print "robot stoppé, fin de l'homologation"
            while 42:
                time.sleep(0.1)
        
        
    def etalonnageAsserv(self):
        pas = 0
        while True :
            print "modifier ?"
            print "constantes de rotation.............r"
            print "constantes de translation..........t"
            print "sortez moi d'ici !.................q"
            choix = raw_input()
            if choix == "q":
                break
            elif choix == "r":
                while True :
                    if (pas > 4):
                        pas = 0
                        self.asserInstance.serieAsserInstance.ecrire("d")
                        self.asserInstance.serieAsserInstance.ecrire("-1500.0")
                        
                    print "constantes rotation : p,d,i. q pour quitter."
                    cte = str(raw_input())
                    if cte == "q":
                        break
                    elif cte == "a":
                        self.asserInstance.serieAsserInstance.ecrire("d")
                        self.asserInstance.serieAsserInstance.ecrire("300.0")
                        pas+=1
                    else:
                        try:
                            val = str(float(raw_input()))
                            self.asserInstance.serieAsserInstance.ecrire("cr"+cte)
                            self.asserInstance.serieAsserInstance.ecrire(val)
                            self.asserInstance.serieAsserInstance.ecrire("d")
                            self.asserInstance.serieAsserInstance.ecrire("300.0")
                            pas+=1
                        except:
                            pass
                
            elif choix == "t":
                while True :
                    if (pas > 4):
                        pas = 0
                        self.asserInstance.serieAsserInstance.ecrire("d")
                        self.asserInstance.serieAsserInstance.ecrire("-1500.0")
                    
                    print "constantes translation : p,d,i. q pour quitter."
                    cte = str(raw_input())
                    if cte == "q":
                        break
                    elif cte == "a":
                        self.asserInstance.serieAsserInstance.ecrire("d")
                        self.asserInstance.serieAsserInstance.ecrire("300.0")
                        pas+=1
                    else:
                        try :
                            val = str(float(raw_input()))
                            self.asserInstance.serieAsserInstance.ecrire("ct"+cte)
                            self.asserInstance.serieAsserInstance.ecrire(val)
                            self.asserInstance.serieAsserInstance.ecrire("d")
                            self.asserInstance.serieAsserInstance.ecrire("300.0")
                            pas+=1
                        except :
                            pass
        
    def test1(self,asserv):
        asserv.gestionAvancer(300,"forcer")
        
    def test2(self,asserv):
        asserv.changerVitesse("translation",1)
        asserv.gestionAvancer(300,"forcer")
    
    def test3(self,asserv):
        asserv.gestionTourner(math.pi/2)
        
    def test4(self,asserv):
        asserv.changerVitesse("rotation",3)
        asserv.gestionTourner(-math.pi/2)
        
    def test5(self,asserv):
        asserv.gestionAvancer(300)
        asserv.gestionAvancer(300)
        asserv.changerVitesse("rotation",3)
        asserv.gestionTourner(0)
        
    def test6(self,asserv):
        asserv.goTo(Point(800, 250))
        
    def gestionScripts(self,script,chrono = False):
        if chrono:
            #instance pour le calcul de durée
            asserv = self.asserInstanceDuree
            #initialisations
            if hasattr(__builtin__.instance, 'serieAsserInstance'):
                asserv.setPosition(self.asserInstance.getPosition())
                asserv.setOrientation(self.asserInstance.getOrientation())
            asserv.changerVitesse("rotation",2)
            asserv.changerVitesse("translation",2)
            
            #début du calcul de durée du script
            asserv.lancerChrono()
        else:
            #instance pour les déplacements réels
            asserv = self.asserInstance
            
        try :
            #execution du script
            script(asserv)
            if chrono:
                #retour de la durée totale d'execution du script
                return asserv.mesurerChrono()
            else:
                #bon déroulement du script (pour des déplacements réels)
                return True
        except :
            #spécifie un déroulement problématique
            return False
    def allerRetour(self):
        
        self.asserInstance.changerVitesse("translation", 2)
        while 42:
            self.asserInstance.gestionAvancer(400)
            self.asserInstance.gestionTourner(0)
            self.asserInstance.gestionAvancer(400)
            self.asserInstance.gestionTourner(math.pi)
            self.asserInstance.gestionAvancer(400)
            self.asserInstance.gestionTourner(0)
            self.asserInstance.gestionAvancer(400)
            self.asserInstance.gestionTourner(math.pi)
            self.asserInstance.gestionAvancer(400)
            self.asserInstance.gestionTourner(0)
            self.asserInstance.gestionAvancer(400)
            self.asserInstance.gestionTourner(math.pi)
            self.asserInstance.gestionAvancer(400)
            self.asserInstance.gestionTourner(0)
            self.asserInstance.gestionAvancer(400)
            self.asserInstance.gestionTourner(math.pi)
            
    def scriptPipeauNewStrategie(self,chrono = "false"):
        #déplacements
        asserv.gestionAvancer(300)
        asserv.gestionAvancer(300,"forcer")
        asserv.changerVitesse("translation",1)
        
        asserv.gestionTourner(math.pi)
        asserv.changerVitesse("rotation",3)
        
        asserv.goTo(Point(800, 250))
        
        #exemples bras
        self.actionInstance.deplacer(90)
        self.actionInstance.deplacer(160)
        self.actionInstance.deplacer(70, "hd")           # Bras Haud Droit (vu depuis le derrière du robot)
        self.actionInstance.deplacer(50, ["hg", "bg"])   # Tourner les bras gauches
        self.actionInstance.changer_vitesse(100)         # Entre 100 et 500 en gros mais on peut monter à 1000
                
    #TEST enchainement des scripts
    def scriptTestStruct0(self):
        try:
            #1ère action effectuée
            print "ca marche ! "
            #le script est validé
            return True
        except:
            return False
    def scriptTestStruct1(self):
        try:
            #1ère action effectuée
            print "yeeeees"
            #2ème action lève une exception
            print 4/0
            #3ème action ne sera pas effectuée
            print "yoyoyo"
            #le script ne sera pas validé
            return True
        except:
            return False
    
    
    def testRamasserTotem(self):
        angle_max = True
        self.actionInstance.deplacer(160)
        while True :
            print "a : avance, r : reculer, t : bouger angle, tt : spécifier angle, o : orientation"
            choix = raw_input("~Sopal\'INT~ ")
            if choix == "q":
                break
            elif choix == "a":
                self.asserInstance.gestionAvancer(100)
            elif choix == "r":
                self.asserInstance.gestionAvancer(-200)
            elif choix == "t":
                if angle_max :
                    self.actionInstance.deplacer(135)
                else :
                    self.actionInstance.deplacer(150)
                angle_max = not angle_max
            
            elif choix == "tt":
                angl = raw_input("angle ? ")
                self.actionInstance.deplacer(int(angl))
            elif choix == "o":
                orient = raw_input("orientation ? ")
                self.asserInstance.gestionTourner(float(orient))
            
            
    #-------------------------------------------------------------------#
    #               Fonctions de très haut niveau                       #
    #-------------------------------------------------------------------#
    def rafflerTotem(self, ennemi = False, nord = False, versLaCalle = True) :
        """
        (Thibaut)
        
        Le robot se déplace de façon à raffler un totem
        
        :param ennemi: A mettre à True si on veut raffler le totem ennemi
        :type ennemi: Bool
        
        :param nord: Partie Nord ou Sud du Totem qu'on veut raffler
        :type nord: Bool
        
        :param versLaCalle: A changer si on veut Parcourir le totem de D à G ou l'inverse
        :type versLaCalle: Bool        
        
        """
        log.logger.info("Rafflage de totem en cours")
        
        if not ennemi and not nord :
            self.actionInstance.deplacer(10)
            #self.asserInstance.goTo(Point(-50, 255))
            #self.asserInstance.gestionTourner(0)
            
            self.actionInstance.deplacer(150)
            #self.asserInstance.gestionAvancer(510)
            time.sleep(1)
            self.actionInstance.deplacer(75)
            #self.asserInstance.gestionTourner(0.535)
            #self.asserInstance.gestionAvancer(665)
            #self.asserInstance.gestionTourner(0)
            #self.asserInstance.gestionAvancer(-450)
            self.actionInstance.deplacer(10)
            
        #if not ennemi and nord :
            #self.actionInstance(
    
    
    def enfoncerPoussoir(self, idPoussoir) :
        """
        (Thibaut)
        Made by Anthony
        
        Le robot se déplace pour enfoncer le poussoir d'indice idPoussoir
        
        :param idPoussoir: Indice du poussoir, 0 = près de chez nous, 1 = loin de chez nous
        :type idPoussoir: int
        """
        log.logger.info("Enfonçage du poussoir "+str(idPoussoir)+" en cours")
        self.actionInstance.deplacer(110) # On met les bras à 110 pour arriver à la position
        if idPoussoir == 0:
            self.asserInstance.goTo(Point(1500 - 640, 2000 - 740)) # On va se placer le long de la ligne
        elif idPoussoir == 1:
            self.asserInstance.goTo(Point(-1500 + 640 + 477, 2000 - 740)) # On va se placer le long de la ligne
        self.asserInstance.gestionTourner(-math.pi/2) # on s'oriente vers les poussoir
        self.asserInstance.gestionAvancer(290) # on avance au point de rotation
        self.asserInstance.gestionTourner(-1.5)    # On lui montre nos fesses
        self.asserInstance.changerVitesse('translation', 3)   # .. Puis on l'enfonce en fonçant
        self.asserInstance.gestionAvancer(-470.0)  # Pour l'enfoncer à fond
        self.asserInstance.changerVitesse('translation', 2)   # On remet le couple maxi à sa valeur d'origine.
        self.asserInstance.gestionAvancer(450)    # On se barre.
        log.logger.info("Enfonçage du poussoir "+str(idPoussoir)+" fini")
        
        
    def faireChierEnnemi(self) :
        """
        Comment va-t-on bien faire chier l'ennemi ?
        """
        log.logger.info("C'est parti, on farme l'ennemi !")
        
    def tourDeTable(self) :
        """
        Tenter de passer à des pts clés pour ramasser des éventuels CDs perdus
        """
        log.logger.info("Tour de table")
        self.actionInstance.deplacer(120) # On ouvre les bras
        self.asserInstance.goTo(Point(860, 650)) # On va se placer à un de départ près de notre base
        self.asserInstance.goTo(Point(395, 505))
        self.asserInstance.goTo(Point(10, 580))
        self.asserInstance.goTo(Point(-425, 480))
        self.asserInstance.goTo(Point(-900, 970))
        self.asserInstance.goTo(Point(410, 1480))
        self.asserInstance.goTo(Point(0, 1400))
        self.asserInstance.goTo(Point(405, 1480))
        self.asserInstance.goTo(Point(900, 1000))
        self.asserInstance.goTo(Point(890, 755))
        self.actionInstance.deplacer(80) # On ferme les bras avant de gestionTourner
        self.asserInstance.gestionTourner(0.755)
        self.actionInstance.deplacer(120) # On ouvre les bras pour déposer
        self.asserInstance.gestionAvancer(340) # On va dans la calle
        self.asserInstance.gestionAvancer(-450) # On fait marche arrière pour se dégager
        self.actionInstance.deplacer(100)
        log.logger.info("Fin tour de table")
        
    def defendreBase(self):
        """
        Si l'ennemi est très bon, il faudra penser à défendre la base
        """
        log.logger.info("Défense de la base")
        
    def testTourdeTable(self):
        #position initiale du robot
        self.asserInstance.setPosition(Point(0,400))
        
        while True:
            try:
                self.asserInstance.goToSegment(Point(710,680))
                self.asserInstance.goToSegment(Point(710,1290))
                self.asserInstance.goToSegment(Point(-710,1290))
                self.asserInstance.goToSegment(Point(-710,680))
            except:
                print "ca chie"
                
        """
        while True:
            try:
                self.asserInstance.goToSegment(Point(0,400))
                self.asserInstance.gestionTourner(0.256)
                self.asserInstance.gestionAvancer(790.0)
                self.asserInstance.gestionTourner(1.147)
                self.asserInstance.gestionAvancer(449.0)
                self.asserInstance.gestionTourner(2.092)
                self.asserInstance.gestionAvancer(743.0)
                self.asserInstance.gestionTourner(3.123)
                self.asserInstance.gestionAvancer(1075.0)
                self.asserInstance.gestionTourner(-2.162)
                self.asserInstance.gestionAvancer(861.0)
                self.asserInstance.gestionTourner(-0.866)
                self.asserInstance.gestionAvancer(695.0)
            except:
                print "ca chie"
        """
        
        
"""
import __builtin__
import instance
sc = __builtin__.instance.scriptInstance
sc.gestionScripts(sc.test1)
sc.gestionScripts(sc.test1,True)
"""