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
        
        
####################################################################################################################
###########################################    GESTION DES SCRIPTS    ##############################################
####################################################################################################################
        
    def gestionScripts(self,script,chrono = False):
        
        """
        méthode de gestion des scripts : il s'occupe 
        - de la récupération des exceptions levées dans avancer, tourner, et recherche de chemin
        - du retour en cas de succes ou d'échec
        - permet de lancer les scripts en mode "chronomètre", pour évaluer leur durée
        """
        
        if chrono:
            #instance pour le calcul de durée
            asserv = self.asserInstanceDuree
            #initialisations
            if hasattr(__builtin__.instance, 'serieAsserInstance'):
                asserv.setPosition(self.asserInstance.getPosition())
                asserv.setOrientation(self.asserInstance.getOrientation())
            
            #début du calcul de durée du script
            asserv.lancerChrono()
        else:
            #instance pour les déplacements réels
            asserv = self.asserInstance
            
        #vitesses normales
        asserv.changerVitesse("rotation",2)
        asserv.changerVitesse("translation",2)
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
            
####################################################################################################################
###########################################     SCRIPTS SPECIAUX      ##############################################
####################################################################################################################


    def recalage(self, asserv):
        """
        Fonction permettant de recaller le robot dans un coin de la table
        """
        asserv.recalage()
        
    def homologation(self, asserv):
        #stocke le lingot et enfonce un poussoir
        asserv.changerVitesse("translation",1)
        asserv.changerVitesse("rotation",1)
        asserv.gestionAvancer(250)     # On sort de la zone départ
        asserv.gestionTourner(1.57)     # On se dirige vers le Nord
        asserv.gestionAvancer(600)     # On avance jusqu'au lingots
        asserv.gestionTourner(0.0)  
        asserv.gestionAvancer(300)     # On le rentre dans la calle
        asserv.gestionAvancer(-300)    # On ressort de la calle
        asserv.gestionTourner(1.57)     # On se tourne vers le boutton poussoir
        asserv.changerVitesse("translation",2)
        asserv.changerVitesse("rotation",2)
        asserv.gestionAvancer(200)     # On avance vers lui
        asserv.gestionTourner(-1.57)    # On lui montre nos fesses
        asserv.gestionAvancer(-480,"auStopNeRienFaire")    # On recule pour lui mettre sa dose
        asserv.changerVitesse("translation",3)
        asserv.gestionAvancer(-500.0,"auStopNeRienFaire")  # Pour l'enfoncer à fond
        asserv.changerVitesse("translation",2)
        asserv.gestionAvancer(200)
        asserv.gestionTourner(-1.57)    # réorientation du robot
        asserv.gestionAvancer(500)    # On se barre.
        
    def etalonnageAsserv(self, asserv):
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
                        asserv.serieAsserInstance.ecrire("d")
                        asserv.serieAsserInstance.ecrire("-1500.0")
                        
                    print "constantes rotation : p,d,i. q pour quitter."
                    cte = str(raw_input())
                    if cte == "q":
                        break
                    elif cte == "a":
                        asserv.serieAsserInstance.ecrire("d")
                        asserv.serieAsserInstance.ecrire("300.0")
                        pas+=1
                    else:
                        try:
                            val = str(float(raw_input()))
                            asserv.serieAsserInstance.ecrire("cr"+cte)
                            asserv.serieAsserInstance.ecrire(val)
                            asserv.serieAsserInstance.ecrire("d")
                            asserv.serieAsserInstance.ecrire("300.0")
                            pas+=1
                        except:
                            pass
                
            elif choix == "t":
                while True :
                    if (pas > 4):
                        pas = 0
                        asserv.serieAsserInstance.ecrire("d")
                        asserv.serieAsserInstance.ecrire("-1500.0")
                    
                    print "constantes translation : p,d,i. q pour quitter."
                    cte = str(raw_input())
                    if cte == "q":
                        break
                    elif cte == "a":
                        asserv.serieAsserInstance.ecrire("d")
                        asserv.serieAsserInstance.ecrire("300.0")
                        pas+=1
                    else:
                        try :
                            val = str(float(raw_input()))
                            asserv.serieAsserInstance.ecrire("ct"+cte)
                            asserv.serieAsserInstance.ecrire(val)
                            asserv.serieAsserInstance.ecrire("d")
                            asserv.serieAsserInstance.ecrire("300.0")
                            pas+=1
                        except :
                            pass
        
        
####################################################################################################################
###########################################      SCRIPTS DE TESTS     ##############################################
####################################################################################################################


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
        
    def allerRetour(self, asserv):
        while 42:
            asserv.gestionAvancer(400)
            asserv.gestionTourner(0)
            asserv.gestionAvancer(400)
            asserv.gestionTourner(math.pi)
            
    def testTourdeTable(self, asserv):
        #position initiale du robot
        asserv.setPosition(Point(0,400))
        while True:
            try:
                asserv.goToSegment(Point(710,680))
                asserv.goToSegment(Point(710,1290))
                asserv.goToSegment(Point(-710,1290))
                asserv.goToSegment(Point(-710,680))
            except:
                print "ca chie"

####################################################################################################################
####################################      Scripts de décision (marquent des points)       ##########################
####################################################################################################################

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
        
        
####################################################################################################################
####################################                        SYNTHAXE                      ##########################
####################################################################################################################
""" 
import __builtin__
import instance
sc = __builtin__.instance.scriptInstance
sc.gestionScripts(sc.test1)
sc.gestionScripts(sc.test1,True)

def scriptPipeauNewStrategie(self, asserv):
        #déplacements
        asserv.gestionAvancer(300)
        asserv.gestionAvancer(300,"forcer")
        asserv.changerVitesse("translation",1)
        
        asserv.gestionTourner(math.pi)
        asserv.changerVitesse("rotation",3)
        
        asserv.goTo(Point(800, 250))
        
        #exemples bras
        self.actionInstance.deplacer(90)                 # tous les bras
        self.actionInstance.deplacer(70, "hd")           # Bras Haud Droit (vu depuis le derrière du robot)
        self.actionInstance.deplacer(50, ["hg", "bg"])   # Tourner les bras gauches
        self.actionInstance.changer_vitesse(100)         # Entre 100 et 500 en gros mais on peut monter à 1000
"""