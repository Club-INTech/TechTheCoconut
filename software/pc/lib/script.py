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
        if hasattr(__builtin__.instance, 'actionInstanceSimu'):
            self.actionInstanceSimu = __builtin__.instance.actionInstanceSimu
        else:
            log.logger.error("script : ne peut importer instance.actionInstanceSimu")
        self.couleur = __builtin__.constantes["couleur"]
        
#Scripts à tester :
#poussoirs côté ennemis et notre côté
#totem nord
#Faire chier ennemi
#Tour de table
#Défendre base
        
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
            asser = self.asserInstanceDuree
            action = self.actionInstanceSimu
            #initialisations
            if hasattr(__builtin__.instance, 'serieAsserInstance'):
                asser.setPosition(self.asserInstance.getPosition())
                asser.setOrientation(self.asserInstance.getOrientation())
            else :
                #NOTE : pour tests (sans série)
                asser.setPosition(Point(70,400))
                asser.setOrientation(0)
            #début du calcul de durée du script
            asser.lancerChrono()
        else:

            #instance pour les déplacements réels
            asser = self.asserInstance
            action = self.actionInstance
        #vitesses normales
        asser.changerVitesse("rotation",2)
        asser.changerVitesse("translation",2)
        try :
            #execution du script    
            script(asser,action)
            if chrono:
                #retour de la durée totale d'execution du script
                return asser.mesurerChrono()
            else:
                #bon déroulement du script (pour des déplacements réels)
                return True
        except :
            #spécifie un déroulement problématique
            return False
            
####################################################################################################################
###########################################     SCRIPTS SPECIAUX      ##############################################
####################################################################################################################


    def recalage(self, asser,action):
        """
        Fonction permettant de recaller le robot dans un coin de la table
        """
        asser.recalage()
    
    def secour(self, asser, action):
        #stocke le lingot et enfonce un poussoir
        #########################################
        asser.changerVitesse("translation",2)
        asser.changerVitesse("rotation",2)
        asser.gestionAvancer(340)     # On sort de la zone départ
        asser.gestionTourner(1.57)     # On se dirige vers le Nord
        asser.gestionAvancer(600)     # On avance jusqu'au lingots
        asser.gestionTourner(0.0)  
        asser.gestionAvancer(300)     # On le rentre dans la calle
        asser.gestionAvancer(-300)    # On ressort de la calle
        asser.gestionTourner(1.57)     # On se tourne vers le boutton poussoir
        #asser.changerVitesse("translation",2)
        #asser.changerVitesse("rotation",2)
        asser.gestionAvancer(500)     # On avance vers lui
        #actionInstance.deplacer(100, ["bd"])
        asser.gestionTourner(-1.57)    # On lui montre nos fesses
        #actionInstance.deplacer(10, ["bd"])
        asser.gestionAvancer(-480,"auStopNeRienFaire")    # On recule pour lui mettre sa dose
        asser.changerVitesse("translation",3)
        asser.gestionAvancer(-500.0,"auStopNeRienFaire")  # Pour l'enfoncer à fond
        asser.changerVitesse("translation",2)
        asser.gestionAvancer(200)
        ###########################################
        #totem nord
        ###########################################
        asser.gestionTourner(math.pi)
        asser.gestionAvancer(800)
        asser.gestionTourner(-math.pi/2)
        assr.gestionAvancer(500)
        asser.gestionTourner(0)
        print asser.getPosition()
        #asser.goTo(Point(-24, 1450))
        #début notre totem nord
        asserInstance.gestionTourner(0)
        actionInstance.deplacer(130)
        time.sleep(0.5)
        asserInstance.gestionAvancer(250,instruction = "auStopNeRienFaire")
        actionInstance.deplacer(120)
        time.sleep(0.5)
        asserInstance.gestionTourner(0,instruction = "auStopNeRienFaire")
        asserInstance.gestionAvancer(200,instruction = "auStopNeRienFaire")
        actionInstance.deplacer(110)
        time.sleep(0.5)
        actionInstance.deplacer(150)
        time.sleep(0.5)
        asserInstance.gestionTourner(0,instruction = "auStopNeRienFaire")
        asserInstance.gestionAvancer(350,instruction = "auStopNeRienFaire")
        
        # Rotation : vers le bas :
        actionInstance.deplacer(130)
        time.sleep(0.5)
        asserInstance.gestionTourner(-math.pi/3, instruction="auStopNeRienFaire")
        asserInstance.gestionAvancer(340, instruction="auStopNeRienFaire")
        asserInstance.gestionTourner(0, instruction="auStopNeRienFaire")
        asserInstance.gestionAvancer(250)
        actionInstance.deplacer(160)
        asserInstance.gestionAvancer(-50)
        actionInstance.deplacer(130)
        asserInstance.gestionAvancer(-50)
        actionInstance.deplacer(150)
        asserInstance.gestionAvancer(-50)
        actionInstance.deplacer(110)
        asserInstance.gestionAvancer(-150)
    
    def pipeau_cassiope(self,asser,action):
        #stocke le lingot et enfonce un poussoir
        asser.changerVitesse("translation",2)
        asser.changerVitesse("rotation",2)
        asser.gestionAvancer(800) 
        asser.gestionTourner(-1.57)
        asser.gestionAvancer(800) 
        asser.gestionTourner(3.14) 
        asser.gestionAvancer(800)

    def homologation(self, asser,action):
        #stocke le lingot et enfonce un poussoir
        asser.changerVitesse("translation",2)
        asser.changerVitesse("rotation",2)
        asser.gestionAvancer(340)     # On sort de la zone départ
        asser.gestionTourner(1.57)     # On se dirige vers le Nord
        asser.gestionAvancer(600)     # On avance jusqu'au lingots
        asser.gestionTourner(0.0)  
        asser.gestionAvancer(390)     # On le rentre dans la calle
        asser.gestionAvancer(-390)    # On ressort de la calle
        asser.gestionTourner(1.57)     # On se tourne vers le boutton poussoir
        #asser.changerVitesse("translation",2)
        #asser.changerVitesse("rotation",2)
        asser.gestionAvancer(500)     # On avance vers lui
        asser.gestionTourner(-1.57)    # On lui montre nos fesses
        asser.gestionAvancer(-480,"auStopNeRienFaire")    # On recule pour lui mettre sa dose
        asser.changerVitesse("translation",3)
        asser.gestionAvancer(-500.0,"auStopNeRienFaire")  # Pour l'enfoncer à fond
        asser.changerVitesse("translation",2)
        asser.gestionAvancer(200)
        asser.gestionTourner(-1.57)    # réorientation du robot
        asser.gestionAvancer(500)    # On se barre.
        
    def etalonnageAsserv(self, asser,action):
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
                        asser.serieAsserInstance.ecrire("d")
                        asser.serieAsserInstance.ecrire("-1500.0")
                        
                    print "constantes rotation : p,d,i. q pour quitter."
                    cte = str(raw_input())
                    if cte == "q":
                        break
                    elif cte == "a":
                        asser.serieAsserInstance.ecrire("d")
                        asser.serieAsserInstance.ecrire("300.0")
                        pas+=1
                    else:
                        try:
                            val = str(float(raw_input()))
                            asser.serieAsserInstance.ecrire("cr"+cte)
                            asser.serieAsserInstance.ecrire(val)
                            asser.serieAsserInstance.ecrire("d")
                            asser.serieAsserInstance.ecrire("300.0")
                            pas+=1
                        except:
                            pass
                
            elif choix == "t":
                while True :
                    if (pas > 4):
                        pas = 0
                        asser.serieAsserInstance.ecrire("d")
                        asser.serieAsserInstance.ecrire("-1500.0")
                    
                    print "constantes translation : p,d,i. q pour quitter."
                    cte = str(raw_input())
                    if cte == "q":
                        break
                    elif cte == "a":
                        asser.serieAsserInstance.ecrire("d")
                        asser.serieAsserInstance.ecrire("300.0")
                        pas+=1
                    else:
                        try :
                            val = str(float(raw_input()))
                            asser.serieAsserInstance.ecrire("ct"+cte)
                            asser.serieAsserInstance.ecrire(val)
                            asser.serieAsserInstance.ecrire("d")
                            asser.serieAsserInstance.ecrire("300.0")
                            pas+=1
                        except :
                            pass
        
        
####################################################################################################################
###########################################      SCRIPTS DE TESTS     ##############################################
####################################################################################################################

    def scriptTotem01(self,asser,action):
        asser.goTo(Point(-24, 1450))
        #début notre totem nord
        asserInstance.gestionTourner(0)
        actionInstance.deplacer(130)
        time.sleep(0.5)
        asserInstance.gestionAvancer(250,instruction = "auStopNeRienFaire")
        actionInstance.deplacer(120)
        time.sleep(0.5)
        asserInstance.gestionTourner(0,instruction = "auStopNeRienFaire")
        asserInstance.gestionAvancer(200,instruction = "auStopNeRienFaire")
        actionInstance.deplacer(110)
        time.sleep(0.5)
        actionInstance.deplacer(150)
        time.sleep(0.5)
        asserInstance.gestionTourner(0,instruction = "auStopNeRienFaire")
        asserInstance.gestionAvancer(350,instruction = "auStopNeRienFaire")
        
        # Rotation : vers le bas :
        actionInstance.deplacer(130)
        time.sleep(0.5)
        asserInstance.gestionTourner(-math.pi/3, instruction="auStopNeRienFaire")
        asserInstance.gestionAvancer(340, instruction="auStopNeRienFaire")
        asserInstance.gestionTourner(0, instruction="auStopNeRienFaire")
        asserInstance.gestionAvancer(250)
        actionInstance.deplacer(160)
        asserInstance.gestionAvancer(-50)
        actionInstance.deplacer(130)
        asserInstance.gestionAvancer(-50)
        actionInstance.deplacer(150)
        asserInstance.gestionAvancer(-50)
        actionInstance.deplacer(110)
        asserInstance.gestionAvancer(-150)
        
        # On récupère
        #actionInstance.deplacer(0, "bd")
        #asserInstance.gestionTourner(-math.pi/2)
        #asserInstance.gestionTourner(-math.pi)
        #actionInstance.deplacer(150)
        #time.sleep(0.5)
        #asserInstance.gestionAvancer(100)
        #actionInstance.deplacer(40)
        #asserInstance.gestionTourner(0)
        #actionInstance.deplacer(130)
        #asserInstance.gestionAvancer(300)
        #asserInstance.gestionAvancer(-200)
        
        # VERSION 2
        actionInstance.deplacer(0, ["bd", "hd"])
        time.sleep(0.2)
        asserInstance.gestionTourner(-math.pi/2)
        asserInstance.gestionTourner(-math.pi)
        asserInstance.gestionAvancer(70)
        actionInstance.deplacer(70, ["hg", "bg"])
        asserInstance.gestionTourner(math.pi/2)
        actionInstance.deplacer(50, ["hg", "bg"])
        asserInstance.gestionTourner(0)
        actionInstance.deplacer(130)
        time.sleep(0.2)
        asserInstance.gestionAvancer(300)
        asserInstance.gestionAvancer(-200)

    def scriptTotem10(self,asser,action):
        asser.goTo(Point(-820.,660.))
        #début leur totem sud
        asser.gestionTourner(0)
        action.deplacer(130)
        asser.attendre(0.5)
        asser.gestionAvancer(200,instruction = "auStopNeRienFaire")
        action.deplacer(120)
        asser.attendre(0.5)
        asser.gestionTourner(0,instruction = "auStopNeRienFaire")
        asser.gestionAvancer(200,instruction = "auStopNeRienFaire")
        action.deplacer(110)
        asser.attendre(0.5)
        action.deplacer(120)
        asser.attendre(0.5)
        asser.gestionTourner(0,instruction = "auStopNeRienFaire")
        asser.gestionAvancer(200,instruction = "auStopNeRienFaire")
        
        #mettre dans la cale
        asser.gestionAvancer(100,instruction = "auStopNeRienFaire")
        asser.gestionTourner(-math.pi/4,instruction = "auStopNeRienFaire")
        asser.gestionAvancer(300,instruction = "auStopNeRienFaire")
        asser.gestionTourner(0,instruction = "auStopNeRienFaire")
        asser.gestionAvancer(700,instruction = "auStopNeRienFaire")
        asser.gestionTourner(math.pi/4, instruction = "auStopNeRienFaire")
        asser.gestionAvancer(400,instruction = "auStopNeRienFaire")
        asser.gestionTourner(0,instruction = "auStopNeRienFaire")
        asser.gestionAvancer(300,instruction = "auStopNeRienFaire")
        asser.gestionAvancer(-50,instruction = "auStopNeRienFaire")
        action.deplacer(130)
        asser.attendre(0.2)
        action.deplacer(110)
        asser.attendre(0.2)
        action.deplacer(130)
        asser.changerVitesse("translation", 3)
        asser.gestionAvancer(-50,instruction = "auStopNeRienFaire")
        asser.changerVitesse("translation", 2)
        asser.gestionAvancer(-300,instruction = "auStopNeRienFaire")
        action.deplacer(0)
        asser.gestionTourner(math.pi/2,instruction = "auStopNeRienFaire")

    def test1(self,asser, action):
        xd = raw_input("x départ? ")
        yd = raw_input("y départ? ")
        asser.setPosition(Point(float(xd),float(yd)))
        asser.setOrientation(0)
        xa = raw_input("x arrivée? ")
        ya = raw_input("y arrivée? ")
        asser.goTo(Point(float(xa),float(ya)))
        
    def test2(self,asser,action):
        asser.setPosition(Point(812,872))
        asser.setOrientation(math.pi/2)
        asser.goTo(Point(float(850),float(1600)))
    
    def test3(self,asser,action):
        xa = raw_input("x robot adverse? ")
        ya = raw_input("y robot adverse? ")
        __builtin__.instance.ajouterRobotAdverse(Point(float(xa),float(ya)))
        
    def test4(self,asser,action):
        xd = raw_input("x départ? ")
        yd = raw_input("y départ? ")
        asser.setPosition(Point(float(xd),float(yd)))
        asser.setOrientation(0)
        xa = raw_input("x arrivée? ")
        ya = raw_input("y arrivée? ")
        asser.goTo(Point(float(xa),float(ya)))
        
    def test5(self,asser,action):
        action.deplacer(150)
        
    def test6(self,asser,action):
        action.deplacer(0)
        
    def allerRetour(self, asser,action):
        while 42:
            asser.gestionAvancer(400)
            asser.gestionTourner(0)
            asser.gestionAvancer(400)
            asser.gestionTourner(math.pi)
            
    def test_goto1(self, asser, action):
        print "OBJECTIF TOTEM SUD : (0,660)"
        asser.goTo(Point(0,660))
        
    def test_goto2(self, asser, action) :
        print "OBJECTIF TOTEM NORD : (0,1330)"
        asser.goTo(Point(0, 1330))
    def test_goto3(self, asser, action) :
        print "OBJECTIF _1 : (-800,1700)"
        asser.goTo(Point(-800,1700))
    def test_goto4(self, asser, action):
        print "OBJECTIF _2 : (800,1700)"

        asser.goTo(Point(800,1700))
        
    def testTourdeTable(self, asser,action):
        #position initiale du robot
        asser.setPosition(Point(0,400))
        while True:
            try:
                asser.goToSegment(Point(710,680))
                asser.goToSegment(Point(710,1290))
                asser.goToSegment(Point(-710,1290))
                asser.goToSegment(Point(-710,680))
            except:
                print "ca chie"
                
    def testGoTo(self):
        asser.setPosition(Point(0,400))
        asser.setOrientation(1.57)
        
        asser.goTo(Point(1002,703))
        asser.goTo(Point(0,400))
        

####################################################################################################################
####################################      Scripts de décision (marquent des points)       ##########################
####################################################################################################################

    #----------------------#
    #        TOTEMS        #
    #----------------------#
    
    def degager(self,asser,action):
        asser.gestionAvancer(600)
        asser.gestionTourner(2)
        asser.gestionAvancer(250)
    
    def totem00(self,asser,action):
        
        asser.gestionTourner(3.1)
        asser.gestionAvancer(1020)
        asser.gestionTourner(2.0)
        asser.gestionAvancer(415)
        #asser.goTo(Point(0.,663.))
        
        #début notre totem sud
        asser.gestionTourner(0)
        action.deplacer(130)
        time.sleep(0.5)
        asser.gestionAvancer(200,instruction = "finir")
        asser.gestionTourner(0,instruction = "finir")
        action.deplacer(120)
        time.sleep(0.3)
        action.deplacer(130)
        time.sleep(0.3)
        asser.gestionTourner(0,instruction = "finir")
        asser.gestionAvancer(200,instruction = "finir")
        action.deplacer(100)
        time.sleep(0.3)
        action.deplacer(120)
        time.sleep(0.3)
        asser.gestionTourner(0,instruction = "finir")
        asser.gestionAvancer(200,instruction = "finir")
        
        #mettre dans la cale
        asser.gestionAvancer(100,instruction = "auStopNeRienFaire")
        asser.gestionTourner(math.pi/4,instruction = "auStopNeRienFaire")
        asser.gestionAvancer(320,instruction = "auStopNeRienFaire")
        asser.gestionTourner(0,instruction = "auStopNeRienFaire")
        asser.gestionAvancer(280,instruction = "auStopNeRienFaire")
        asser.gestionAvancer(-50,instruction = "auStopNeRienFaire")
        action.deplacer(130)
        time.sleep(0.3)
        action.deplacer(110)
        time.sleep(0.3)
        action.deplacer(130)
        time.sleep(0.3)
        action.deplacer(110)
        time.sleep(0.3)
    
        action.deplacer(130)
        asser.changerVitesse("translation", 3)
        asser.gestionAvancer(-50,instruction = "auStopNeRienFaire")
        asser.changerVitesse("translation", 2)
        asser.gestionAvancer(-220,instruction = "auStopNeRienFaire")
        action.deplacer(0)
        
    def totem00_v2(self,asser,action):
        
        asser.goTo(Point(0, 660.))
        #asser.goTo(Point(0.,660.))
        
        #début notre totem sud
        asser.gestionTourner(0)
        action.deplacer(130)
        time.sleep(0.5)
        asser.gestionAvancer(200,instruction = "finir")
        asser.gestionTourner(0,instruction = "finir")
        action.deplacer(120)
        time.sleep(0.3)
        action.deplacer(130)
        time.sleep(0.3)
        asser.gestionTourner(0,instruction = "finir")
        asser.gestionAvancer(200,instruction = "finir")
        action.deplacer(100)
        time.sleep(0.3)
        action.deplacer(120)
        time.sleep(0.3)
        asser.gestionTourner(0,instruction = "finir")
        asser.gestionAvancer(200,instruction = "finir")
        
        #mettre dans la cale
        asser.gestionAvancer(100,instruction = "auStopNeRienFaire")
        asser.gestionTourner(math.pi/4,instruction = "auStopNeRienFaire")
        asser.gestionAvancer(320,instruction = "auStopNeRienFaire")
        asser.gestionTourner(0,instruction = "auStopNeRienFaire")
        asser.gestionAvancer(280,instruction = "auStopNeRienFaire")
        asser.gestionAvancer(-50,instruction = "auStopNeRienFaire")
        action.deplacer(130)
        time.sleep(0.3)
        action.deplacer(110)
        time.sleep(0.3)
        action.deplacer(130)
        time.sleep(0.3)
        action.deplacer(110)
        time.sleep(0.3)
    
        action.deplacer(130)
        asser.changerVitesse("translation", 3)
        asser.gestionAvancer(-50,instruction = "auStopNeRienFaire")
        asser.changerVitesse("translation", 2)
        asser.gestionAvancer(-220,instruction = "auStopNeRienFaire")
        action.deplacer(0)
        
    def totem00_v3(self,asser,action):
        
        asser.gestionTourner(3.1)
        asser.gestionAvancer(1020)
        asser.gestionTourner(2.0)
        asser.gestionAvancer(415)
        #asser.goTo(Point(0.,660.))
        
        #début notre totem sud
        asser.gestionTourner(0)
        action.deplacer(130)
        time.sleep(0.5)
        asser.gestionAvancer(200,instruction = "finir")
        asser.gestionTourner(0,instruction = "finir")
        action.deplacer(120)
        time.sleep(0.3)
        action.deplacer(130)
        time.sleep(0.3)
        asser.gestionTourner(0,instruction = "finir")
        asser.gestionAvancer(200,instruction = "finir")
        action.deplacer(100)
        time.sleep(0.3)
        action.deplacer(120)
        time.sleep(0.3)
        asser.gestionTourner(0,instruction = "finir")
        asser.gestionAvancer(200,instruction = "finir")
        
        #mettre dans la cale
        asser.gestionAvancer(100,instruction = "auStopNeRienFaire")
        asser.gestionTourner(math.pi/4,instruction = "auStopNeRienFaire")
        asser.gestionAvancer(320,instruction = "auStopNeRienFaire")
        asser.gestionTourner(0,instruction = "auStopNeRienFaire")
        asser.gestionAvancer(280,instruction = "auStopNeRienFaire")
        asser.gestionAvancer(-50,instruction = "auStopNeRienFaire")
        action.deplacer(130)
        time.sleep(0.3)
        action.deplacer(110)
        time.sleep(0.3)
        action.deplacer(130)
        time.sleep(0.3)
        action.deplacer(110)
        time.sleep(0.3)
    
        action.deplacer(130)
        asser.changerVitesse("translation", 3)
        asser.gestionAvancer(-50,instruction = "auStopNeRienFaire")
        asser.changerVitesse("translation", 2)
        asser.gestionAvancer(-220,instruction = "auStopNeRienFaire")
        action.deplacer(0)
        
    def poussoir1(self,asser,action):
        asser.gestionTourner(math.pi/2,instruction = "finir")
        asser.gestionAvancer(400,instruction = "auStopNeRienFaire")

        asser.gestionTourner(math.pi/2)
        action.deplacer(120, "bd")
        asser.attendre(0.3)
        asser.gestionAvancer(200,instruction = "auStopNeRienFaire")
        asser.gestionTourner(-math.pi)
        asser.gestionTourner(-math.pi/2)
        #asser.changerVitesse("translation", 3)
        asser.gestionAvancer(-1000, "auStopNeRienFaire")
        #asser.changerVitesse("translation", 2)
        asser.gestionAvancer(200,instruction = "auStopNeRienFaire")
        asser.gestionTourner(-math.pi/2)
        action.deplacer(0)
        asser.gestionAvancer(260)
        log.logger.debug("Enfonçage du poussoir à nous fini")
        
    def poussoir2(self,asser,action):
        log.logger.debug("Début d'enfonçage du poussoir 2")
        asser.gestionTourner(math.pi,instruction = "finir")
        action.deplacer(130,["bd","bg"])
        asser.gestionAvancer(1248,instruction = "auStopNeRienFaire")
        action.deplacer(50, ["bg", "bd"])
        asser.gestionTourner(-math.pi/2)
        asser.gestionAvancer(-200.0)
        #asser.changerVitesse("translation", 3)
        asser.gestionAvancer(-10000, "auStopNeRienFaire")
        #asser.changerVitesse("translation", 2)
        asser.gestionTourner(-math.pi/2)
        asser.gestionAvancer(300)
        log.logger.debug("Enfonçage du poussoir éloigné fini")
        
    def totem01(self, asser, action) :
        action.deplacer(50)
        asser.goTo(Point(0, 1500))
        asser.gestionTourner(1.712)
        asser.gestionAvancer(226.0)
        ##début notre totem nord
        asser.gestionTourner(0)
        action.deplacer(130)
        asser.attendre(0.5)
        asser.gestionAvancer(250,instruction = "auStopNeRienFaire")
        action.deplacer(120)
        asser.attendre(0.5)
        asser.gestionTourner(0,instruction = "auStopNeRienFaire")
        asser.gestionAvancer(200,instruction = "auStopNeRienFaire")
        action.deplacer(110)
        asser.attendre(0.5)
        action.deplacer(150)
        asser.attendre(0.5)
        asser.gestionTourner(0,instruction = "auStopNeRienFaire")
        asser.gestionAvancer(350,instruction = "auStopNeRienFaire")
        
        ## Rotation : vers le bas :
        action.deplacer(130)
        asser.attendre(0.5)
        asser.gestionTourner(-math.pi/3, instruction="auStopNeRienFaire")
        asser.gestionAvancer(340, instruction="auStopNeRienFaire")
        asser.gestionTourner(0, instruction="auStopNeRienFaire")
        asser.gestionAvancer(250)
        action.deplacer(160)
        asser.gestionAvancer(-50)
        action.deplacer(130)
        asser.gestionAvancer(-50)
        action.deplacer(150)
        asser.gestionAvancer(-50)
        action.deplacer(110)
        asser.gestionAvancer(-150)
    #_________________________________________________________________________________________________
    #_________________________________________________________________________________________________
        
    # Rafflage de notre totem côté sud (y petits)
    def rafflerTotem00(self,asser,action) :
        log.logger.debug("Rafflage de totem 0 0")
        action.deplacer(0)
        asser.goTo(Point(-90,655))
        
        #début notre totem sud
        asser.gestionTourner(0)
        action.deplacer(140)
        asser.attendre(0.1)
        
        asser.gestionAvancer(50)
        action.deplacer(90, "bg")
        asser.attendre(0.2)
        action.deplacer(130, "bg")
        #asser.attendre(0.1)
        
        #asser.gestionAvancer(200,instruction = "finir")
        #action.deplacer(130)
        ##asser.attendre(0.2)
        #asser.gestionTourner(0,instruction = "finir")
        #asser.gestionAvancer(200,instruction = "finir")
        #action.deplacer(110)
        #asser.attendre(0.1)
        #action.deplacer(130)
        #asser.attendre(0.1)
        #asser.gestionTourner(0,instruction = "finir")
        #asser.gestionAvancer(200,instruction = "finir")
        ##mettre dans la cale
        
        asser.gestionAvancer(400, instruction="finir")
        asser.gestionTourner(0)
        asser.gestionAvancer(300)
        
        #asser.gestionAvancer(100,instruction = "finir")
        asser.gestionTourner(math.pi/4)
        asser.gestionAvancer(300)
        asser.gestionTourner(0)
        asser.gestionAvancer(300, "auStopNeRienFaire")
        asser.gestionAvancer(-50)
        action.deplacer(130)
        asser.attendre(0.1)
        action.deplacer(110)
        asser.attendre(0.1)
        action.deplacer(150)
        asser.changerVitesse("translation", 3)
        asser.gestionAvancer(-50)
        asser.changerVitesse("translation", 2)
        asser.gestionAvancer(-250)
        action.deplacer(0)
        #asser.gestionTourner(math.pi/2)
        #asser.goTo(Point(850.,1600.))
    
    # Rafflage de notre totem côté nord (y grands)
    def rafflerTotem01(self,asser,action) :
        log.logger.debug("Rafflage de totem 0 1 en cours")
        action.deplacer(0)
        asser.goTo(Point(-80,1380))
        ##début notre totem nord
        action.deplacer(90, ["bd", "hd"])
        asser.attendre(0.1)
        action.deplacer(0, ["bd", "hd"])
        asser.attendre(0.1)
        asser.gestionTourner(0)
        #action.deplacer(120)
        ##début notre totem nord
        #action.deplacer(90, ["bd", "hd"])
        #asser.attendre(0.1)
        #asser.gestionTourner(0)
        action.deplacer(130)
        asser.attendre(0.2)
        
        asser.gestionAvancer(50)
        asser.gestionTourner(0,instruction = "finir")
        action.deplacer(70, "bd")
        asser.attendre(0.2)
        action.deplacer(120, "bd")
        asser.gestionAvancer(230,"finir")
        action.deplacer(110)
        #asser.attendre(0.1)
        asser.gestionTourner(0,instruction = "finir")
        asser.gestionAvancer(200,instruction = "finir")
        #action.deplacer(120)
        #asser.attendre(0.1)
        #action.deplacer(110)
        #asser.attendre(0.1)
        asser.gestionTourner(0,instruction = "finir")
        asser.gestionAvancer(300,instruction = "finir")
        
        ## Rotation : vers le bas :
        action.deplacer(110)
        #asser.attendre(0.2)
        asser.gestionTourner(-math.pi/2)
        asser.gestionAvancer(350)
        asser.gestionTourner(0)
        asser.gestionAvancer(400, "auStopNeRienFaire")
        action.deplacer(160)
        asser.gestionAvancer(-50)
        action.deplacer(130)
        asser.gestionAvancer(-50)
        action.deplacer(150)
        asser.gestionAvancer(-50)
        action.deplacer(110)
        asser.gestionAvancer(-150)
        action.deplacer(0)

        
    # Rafflage du totem ennemi côté sud (y petits)
    def rafflerTotem10(self,asser,action) :
        log.logger.debug("Rafflage de totem 1 0 en cours")
        action.deplacer(0)
        asser.goTo(Point(-920+ 70, 440+180))
        asser.gestionTourner(0)
        action.deplacer(150)
        asser.attendre(0.2)
        asser.gestionAvancer(100, "finir")
        action.deplacer(30, "bg")
        asser.attendre(0.2)
        action.deplacer(150, "bg")
        asser.attendre(0.2)
        asser.gestionAvancer(100, "finir")
        action.deplacer(130)
        asser.gestionAvancer(100, "finir")
        asser.gestionTourner(0)
        action.deplacer(110)
        asser.attendre(0.1)
        action.deplacer(120)
        asser.attendre(0.1)
        asser.gestionTourner(0)
        asser.gestionAvancer(200, "finir")
        asser.gestionTourner(0)
        action.deplacer(90)
        asser.attendre(0.3)
        
        #asser.gestionAvancer(200)
        #action.deplacer(40, "bg")
        
        #action.deplacer(0, ["hd", "hg"])
        #asser.gestionTourner(-1)
        #asser.gestionAvancer(300)
        #asser.gestionTourner(0)
        #asser.gestionAvancer(600)
        #asser.gestionTourner(1)
        #asser.gestionAvancer(500)
        #asser.gestionTourner(0)
        #asser.gestionAvancer(300, "auStopNeRienFaire")
        #asser.gestionAvancer(-300)
    
        asser.gestionAvancer(500, "finir")
        asser.gestionTourner(0)
        asser.gestionAvancer(400)
        
    # Rafflage du totem ennemi, côté Nord.
    def rafflerTotem11(self,asser,action) :
        action.deplacer(0)
        log.logger.debug("Rafflage de totem 1 1 en cours")
        asser.goTo(Point(-920+70, 1390))
        
        asser.gestionTourner(0)
        action.deplacer(130)
        asser.attendre(0.2)
        
        asser.gestionAvancer(20)
        action.deplacer(70, "bd")
        asser.attendre(0.2)
        action.deplacer(130, "bd")
        asser.gestionAvancer(230,"finir")
        action.deplacer(120)
        asser.attendre(0.2)
        asser.gestionTourner(0,instruction = "finir")
        asser.gestionAvancer(200,instruction = "finir")
        action.deplacer(110)
        asser.attendre(0.2)
        action.deplacer(150)
        asser.attendre(0.2)
        asser.gestionTourner(0,instruction = "finir")
        asser.gestionAvancer(350,instruction = "finir")
        
        asser.gestionTourner(-math.pi/4)
        asser.gestionAvancer(300)
        asser.gestionTourner(0)
        asser.gestionAvancer(300, "auStopNeRienFaire")
        asser.gestionAvancer(-50)
        action.deplacer(130)
        asser.attendre(0.1)
        action.deplacer(110)
        asser.attendre(0.1)
        action.deplacer(150)
        asser.changerVitesse("translation", 3)
        asser.gestionAvancer(-50)
        asser.changerVitesse("translation", 2)
        asser.gestionAvancer(-250)
        action.deplacer(0)
        asser.gestionTourner(math.pi/2)
    
    
    #----------------------#
    #   BOUTONS POUSSOIR   #
    #----------------------#
    
    # Poussoir côté chez nous.
    def enfoncerPoussoir0(self,asser,action) :
        action.deplacer(0)
        log.logger.debug("Enfonçage du poussoir côté nous en cours")
        asser.goTo(Point(860,1490))
        asser.gestionTourner(math.pi/2)
        action.deplacer(120, "bd")
        #asser.attendre(0.2)
        asser.gestionAvancer(20)
        asser.gestionTourner(math.pi)
        asser.gestionTourner(-math.pi/2)
        
        asser.gestionAvancer(-3000, "auStopNeRienFaire")
        asser.gestionTourner(-math.pi/2)

        asser.gestionAvancer(200)
        asser.gestionAvancer(200,"finir")
        asser.gestionTourner(-math.pi/2)
        #asser.gestionAvancer(-100)
        action.deplacer(0)
        log.logger.debug("Enfonçage du poussoir à nous fini")

        
    # Poussoir côté ennemi.
    def enfoncerPoussoir1(self,asser,action) :
        action.deplacer(0)
        log.logger.debug("Enfonçage du poussoir côté ennemi en cours")
        asser.goTo(Point(-390, 1510.))  
        asser.gestionTourner(math.pi/2)
        action.deplacer(150, "bd")
        asser.attendre(0.2)
        #asser.gestionAvancer(220)
        asser.gestionTourner(-math.pi)
        asser.gestionTourner(-math.pi/2)
        
        action.deplacer(20, "bd")
        
        asser.gestionAvancer(-3000, "auStopNeRienFaire")
        asser.gestionAvancer(200)
        asser.gestionAvancer(200)
        asser.gestionTourner(-math.pi/2)
        asser.gestionAvancer(-100)
        action.deplacer(0)
        log.logger.debug("Enfonçage du poussoir ennemi fini")
        
        
    #----------------------#
    #       ANNEXES        #
    #----------------------#

    def faireChierEnnemi(self,asser,action) :
        """
        On fait un tour de table bras fermés
        """
        log.logger.debug("C'est parti, on farme l'ennemi !")
        action.deplacer(0)
        asser.goTo(Point(-1500+960-70, 2000-260+160))
        asser.gestionTourner(-math.pi)
        action.deplacer(150, "bd")
        asser.attendre(0.5)
        asser.gestionAvancer(220)
        asser.gestionTourner(-math.pi/2)
        asser.gestionTourner(0)
        action.deplacer(0)
        asser.gestionAvancer(-3000, "auStopNeRienFaire")
        asser.gestionAvancer(130)
        asser.gestionTourner(-math.pi/2-0.02)
        asser.attendre(.5)
        asser.gestionAvancer(500)
        
        """
        asser.gestionTourner(-3*math.pi/4)
        asser.gestionAvancer(250)
        action.deplacer(150, "bg")
        asser.attendre(0.5)
        asser.gestionTourner(-math.pi/4)
        asser.gestionAvancer(350)
        """
        
        asser.gestionAvancer(150)
        asser.gestionTourner(-math.pi)
        asser.gestionAvancer(250)
        action.deplacer(160)
        asser.attendre(0.2)
        asser.changerVitesse("rotation", 3)
        asser.gestionTourner(-math.pi/2)
        asser.gestionTourner(math.pi)
        asser.gestionTourner(math.pi/2)
        asser.gestionTourner(math.pi)
        asser.changerVitesse("rotation", 2)
        asser.gestionAvancer(-300)
        action.deplacer(0)
        
    def debutRapide(self, asser, action) :
        asser.gestionTourner(2.9)
        asser.gestionAvancer(1000, "auStopNeRienFaire")
        asser.changerVitesse("translation", 2)
        
    def viderCaleEnnemi(self, asser, action) :
        log.logger.debug("Farmage d'ennemi")
        asser.goTo(Point(-690, 600))
        asser.gestionTourner(2.15)
        asser.gestionAvancer(239.0)
        action.deplacer(160, ["bg", "bd"])
        asser.attendre(.2)
        asser.gestionTourner(math.pi)
        asser.gestionAvancer(280.0)
        asser.changerVitesse("rotation", 3)
        asser.gestionTourner(-math.pi/2)
        asser.changerVitesse("rotation", 2)
        asser.gestionTourner(math.pi)
        asser.changerVitesse("rotation", 3)
        asser.gestionTourner(math.pi/2)
        asser.changerVitesse("rotation", 2)

        asser.gestionTourner(0)
        action.deplacer(20, ["bg", "bd"])
        asser.gestionAvancer(-270)
        asser.goTo(Point(779, 974))
        asser.gestionTourner(0)
        action.deplacer(160, ["bd", "bg"])
        asser.attendre(0.2)
        asser.gestionAvancer(270, "auStopNeRienFaire")
        asser.gestionAvancer(-270)
        action.deplacer(0)
        
    def viderCaleEnnemi2(self, asser, action) :
        log.logger.debug("On vide la cale de l'autre !")
        action.deplacer(0)
        asser.goTo(Point(-950, 1436))
        asser.gestionTourner(-math.pi/2-0.1)
        
        action.deplacer(180, "bd")
        asser.attendre(0.1)
        asser.gestionAvancer(200, "auStopNeRienFaire")
        action.deplacer(70, "bd")
        asser.attendre(0.2)
        action.deplacer(180, "bd")
        asser.attendre(0.2)
        asser.gestionAvancer(200)
        action.deplacer(70, "bd")
        asser.attendre(0.2)
        action.deplacer(180, "bd")
        asser.attendre(0.2)
        asser.gestionAvancer(200)
        action.gestionTourner(20)
        asser.gestionTourner(0)
        
        asser.goTo(Point(779, 974))
        asser.gestionTourner(0)
        action.deplacer(160, ["bd", "bg"])
        asser.attendre(0.2)
        asser.gestionAvancer(270, "auStopNeRienFaire")
        asser.gestionAvancer(-270)
        action.deplacer(0)
        
        
    # Tour de table avec les bras fermés.
    def tourDeTable0(self,asser,action) :
        """
        Tenter de passer à des pts clés pour ramasser des éventuels CDs perdus
        ET faire chier n'ennemi
        """
        asser.goTo(Point(0,1490))

        raw_input()
        asser.goTo(Point(590,290))
        asser.goTo(Point(-990,630))
        asser.goTo(Point(0,1490))

    # Tour de table avec les bras ouverts
    def tourDeTable1(self,asser,action) :
        """
        Tenter de passer à des pts clés pour ramasser des éventuels CDs perdus
        """
        log.logger.debug("Tour de table")
        action.deplacer(120) # On ouvre les bras
        asser.goTo(Point(860, 650)) # On va se placer à un de départ près de notre base
        asser.goTo(Point(395, 505))
        asser.goTo(Point(10, 580))
        asser.goTo(Point(-425, 480))
        asser.goTo(Point(-900, 970))
        asser.goTo(Point(410, 1480))
        asser.goTo(Point(0, 1400))
        asser.goTo(Point(405, 1480))
        asser.goTo(Point(900, 1000))
        asser.goTo(Point(890, 755))
        action.deplacer(80) # On ferme les bras avant de gestionTourner
        asser.gestionTourner(0.755)
        action.deplacer(120) # On ouvre les bras pour déposer
        asser.gestionAvancer(340) # On va dans la calle
        asser.gestionAvancer(-450) # On fait marche arrière pour se dégager
        action.deplacer(100)
        
    def defendreBase(self,asser,action):
        """
        Si l'ennemi est très bon, il faudra penser à défendre la base
        """
        action.deplacer(0)
        log.logger.debug("Défense de la base")
        asser.goTo(Point(960, 1260))
        asser.gestionTourner(math.pi/2)
        asser.gestionAvancer(1300)
        asser.gestionAvancer(-1300)
        log.logger.debug("Fin défense de la base")
        
    def bourrerCale(self, asser, action) :
        #action.deplacer(0)
        asser.goTo(Point(900, 1000))
        asser.gestionTourner(0)
        action.deplacer(0, "bd")
        asser.gestionTourner(-math.pi/2)
        asser.gestionTourner(-math.pi)
        action.deplacer(150)
        asser.attendre(0.2)
        asser.gestionAvancer(200, "auStopNeRienFaire")
        action.deplacer(30)
        asser.attendre(0.2)
        asser.gestionAvancer(-100)
        asser.gestionTourner(0)
        action.deplacer(150)
        asser.attendre(0.2)
        asser.gestionAvancer(300, "auStopNeRienFaire")
        asser.gestionAvancer(-230)
        action.deplacer(0)
        asser.gestionTourner(math.pi/2)
        
        
####################################################################################################################
###########################                P R É   ---   A C T I O N S                    ##########################
####################################################################################################################

    def preAction_1_2(self, asser, action) :
        action.deplacer(0)
        asser.goTo(Point(800, 700))
        asser.gestionTourner(math.pi/2)
        action.deplacer(110)
        asser.attendre(0.2)
        asser.gestionTourner(math.pi/2)
        asser.deplacer(700)
        
    def preAction_2_3(self, asser, action) :
        action.deplacer(0)
        asser.goTo(Point(430, 1585))
        action.deplacer(130)
        asser.attendre(0.2)
        asser.gestionTourner(path.pi)
        asser.gestionAvancer(400)
        
        

####################################################################################################################
###########################                       SCRIPT GÉNÉRIQUES                       ##########################
####################################################################################################################

    # Lance un script en fonction d'un tableau d'actions
    '''
      Syntaxe des actions : 
      ["avancer", mm, option]
      ["tourner", rad, option]
      ["actionneur", angle]
      ["goTo",    point]
      
      NOTE Normalement, cette fonction n'est pas utilisée.
    '''
    
    def scriptGenerique(self, asser, action,  suiteActions) :
        log.logger.debug("Script générique : " + str(suiteActions))
        for i in range(len(suiteActions)) :
            currentAction = suiteActions[i]
            
            if currentAction[0] == "avancer" :
                if len(currentAction) == 3 :
                    return asser.gestionAvancer(currentAction[1], currentAction[2])
                else :
                    return asser.gestionAvancer(currentAction[1])
                    
            elif currentAction[0] == "tourner" :
                if len(currentAction) == 3 :
                    return asser.gestionTourner(currentAction[1], currentAction[2])
                else : 
                    return asser.gestionTourner(currentAction[1])
            elif currentAction[0] == "actionneur" :
                return action.deplacer(currentAction[1])
                
            elif currentAction[0] == "goTo" :
                return asser.goTo(Point(currentAction[1][0], currentAction[1][1]))
                    
        
        
        
####################################################################################################################
####################################                        SYNTAXE                       ##########################
####################################################################################################################
""" 
import __builtin__
import instance
sc = __builtin__.instance.scriptInstance
sc.gestionScripts(sc.test1)
sc.gestionScripts(sc.test1,True)

def scriptPipeauNewStrategie(self, asser,action):
        #déplacements
        asser.gestionAvancer(300)
        asser.gestionAvancer(300,"forcer")
        asser.changerVitesse("translation",1)
        
        asser.gestionTourner(math.pi)
        asser.changerVitesse("rotation",3)
        
        asser.goTo(Point(800, 250))
        
        #exemples bras
        self.action.deplacer(90)                 # tous les bras
        self.action.deplacer(70, "hd")           # Bras Haud Droit (vu depuis le derrière du robot)
        self.action.deplacer(50, ["hg", "bg"])   # Tourner les bras gauches
        self.action.changer_vitesse(100)         # Entre 100 et 500 en gros mais on peut monter à 1000
"""
