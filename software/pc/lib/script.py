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
        
    def homologation(self, asser,action):
        #stocke le lingot et enfonce un poussoir
        asser.changerVitesse("translation",1)
        asser.changerVitesse("rotation",1)
        asser.gestionAvancer(260)     # On sort de la zone départ
        asser.gestionTourner(1.57)     # On se dirige vers le Nord
        asser.gestionAvancer(600)     # On avance jusqu'au lingots
        asser.gestionTourner(0.0)  
        asser.gestionAvancer(300)     # On le rentre dans la calle
        asser.gestionAvancer(-300)    # On ressort de la calle
        asser.gestionTourner(1.57)     # On se tourne vers le boutton poussoir
        asser.changerVitesse("translation",2)
        asser.changerVitesse("rotation",2)
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
        asserInstance.goTo(Point(0.,1300.))
        #début notre totem nord
        asserInstance.gestionTourner(0)
        actionInstance.deplacer(130)
        time.sleep(0.5)
        asserInstance.gestionAvancer(200,instruction = "auStopNeRienFaire")
        actionInstance.deplacer(120)
        time.sleep(0.5)
        asserInstance.gestionTourner(0,instruction = "auStopNeRienFaire")
        asserInstance.gestionAvancer(200,instruction = "auStopNeRienFaire")
        actionInstance.deplacer(110)
        time.sleep(0.5)
        actionInstance.deplacer(120)
        time.sleep(0.5)
        asserInstance.gestionTourner(0,instruction = "auStopNeRienFaire")
        asserInstance.gestionAvancer(200,instruction = "auStopNeRienFaire")
        
        #mettre dans la cale
        asserInstance.gestionAvancer(100,instruction = "auStopNeRienFaire")
        asserInstance.gestionTourner(-math.pi/4,instruction = "auStopNeRienFaire")
        asserInstance.gestionAvancer(300,instruction = "auStopNeRienFaire")
        asserInstance.gestionTourner(0,instruction = "auStopNeRienFaire")
        asserInstance.gestionAvancer(300,instruction = "auStopNeRienFaire")
        asserInstance.gestionAvancer(-50,instruction = "auStopNeRienFaire")
        actionInstance.deplacer(130)
        time.sleep(0.2)
        actionInstance.deplacer(110)
        time.sleep(0.2)
        actionInstance.deplacer(130)
        asserInstance.changerVitesse("translation", 3)
        asserInstance.gestionAvancer(-50,instruction = "auStopNeRienFaire")
        asserInstance.changerVitesse("translation", 2)
        asserInstance.gestionAvancer(-300,instruction = "auStopNeRienFaire")
        actionInstance.deplacer(0)
        asserInstance.gestionTourner(math.pi/2,instruction = "auStopNeRienFaire")

    def scriptTotem10(self,asser,action):
        asserInstance.goTo(Point(-820.,660.))
        #début leur totem sud
        asserInstance.gestionTourner(0)
        actionInstance.deplacer(130)
        time.sleep(0.5)
        asserInstance.gestionAvancer(200,instruction = "auStopNeRienFaire")
        actionInstance.deplacer(120)
        time.sleep(0.5)
        asserInstance.gestionTourner(0,instruction = "auStopNeRienFaire")
        asserInstance.gestionAvancer(200,instruction = "auStopNeRienFaire")
        actionInstance.deplacer(110)
        time.sleep(0.5)
        actionInstance.deplacer(120)
        time.sleep(0.5)
        asserInstance.gestionTourner(0,instruction = "auStopNeRienFaire")
        asserInstance.gestionAvancer(200,instruction = "auStopNeRienFaire")
        
        #mettre dans la cale
        asserInstance.gestionAvancer(100,instruction = "auStopNeRienFaire")
        asserInstance.gestionTourner(-math.pi/4,instruction = "auStopNeRienFaire")
        asserInstance.gestionAvancer(300,instruction = "auStopNeRienFaire")
        asserInstance.gestionTourner(0,instruction = "auStopNeRienFaire")
        asserInstance.gestionAvancer(700,instruction = "auStopNeRienFaire")
        asserInstance.gestionTourner(math.pi/4, instruction = "auStopNeRienFaire")
        asserInstance.gestionAvancer(400,instruction = "auStopNeRienFaire")
        asserInstance.gestionTourner(0,instruction = "auStopNeRienFaire")
        asserInstance.gestionAvancer(300,instruction = "auStopNeRienFaire")
        asserInstance.gestionAvancer(-50,instruction = "auStopNeRienFaire")
        actionInstance.deplacer(130)
        time.sleep(0.2)
        actionInstance.deplacer(110)
        time.sleep(0.2)
        actionInstance.deplacer(130)
        asserInstance.changerVitesse("translation", 3)
        asserInstance.gestionAvancer(-50,instruction = "auStopNeRienFaire")
        asserInstance.changerVitesse("translation", 2)
        asserInstance.gestionAvancer(-300,instruction = "auStopNeRienFaire")
        actionInstance.deplacer(0)
        asserInstance.gestionTourner(math.pi/2,instruction = "auStopNeRienFaire")

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
        asser.changerVitesse("rotation",3)
        asser.gestionTourner(-math.pi/2)
        
    def test5(self,asser,action):
        asser.gestionAvancer(300)
        asser.gestionAvancer(300)
        asser.changerVitesse("rotation",3)
        asser.gestionTourner(0)
        
    def test6(self,asser,action):
        asser.goTo(Point(800, 250))
        
    def allerRetour(self, asser,action):
        while 42:
            asser.gestionAvancer(400)
            asser.gestionTourner(0)
            asser.gestionAvancer(400)
            asser.gestionTourner(math.pi)
            
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

####################################################################################################################
####################################      Scripts de décision (marquent des points)       ##########################
####################################################################################################################

    #----------------------#
    #        TOTEMS        #
    #----------------------#
    
    # Rafflage de notre totem côté sud (y petits)
    def rafflerTotem00(self,asser,action) :
        log.logger.debug("Rafflage de totem 0 0")
        asser.goTo(Point(0.,660.))
        #début notre totem sud
        asser.gestionTourner(0)
        action.deplacer(130)
        time.sleep(0.5)
        asser.gestionAvancer(200,instruction = "auStopNeRienFaire")
        action.deplacer(120)
        time.sleep(0.5)
        asser.gestionTourner(0,instruction = "auStopNeRienFaire")
        asser.gestionAvancer(200,instruction = "auStopNeRienFaire")
        action.deplacer(110)
        time.sleep(0.5)
        action.deplacer(120)
        time.sleep(0.5)
        asser.gestionTourner(0,instruction = "auStopNeRienFaire")
        asser.gestionAvancer(200,instruction = "auStopNeRienFaire")
        #mettre dans la cale
        asser.gestionAvancer(100,instruction = "auStopNeRienFaire")
        asser.gestionTourner(math.pi/4,instruction = "auStopNeRienFaire")
        asser.gestionAvancer(300,instruction = "auStopNeRienFaire")
        asser.gestionTourner(0,instruction = "auStopNeRienFaire")
        asser.gestionAvancer(300,instruction = "auStopNeRienFaire")
        asser.gestionAvancer(-50,instruction = "auStopNeRienFaire")
        action.deplacer(130)
        time.sleep(0.2)
        action.deplacer(110)
        time.sleep(0.2)
        action.deplacer(130)
        asser.changerVitesse("translation", 3)
        asser.gestionAvancer(-50,instruction = "auStopNeRienFaire")
        asser.changerVitesse("translation", 2)
        asser.gestionAvancer(-300,instruction = "auStopNeRienFaire")
        action.deplacer(0)
        asser.gestionTourner(math.pi/2,instruction = "auStopNeRienFaire")
        asser.goTo(Point(850.,1600.))
    
    # Rafflage de notre totem côté nord (y grands)
    def rafflerTotem01(self,asser,action) :
        log.logger.debug("Rafflage de totem 0 1 en cours")
        
        asser.goTo(Point(0.,1300.))
        #début notre totem sud
        asser.gestionTourner(0)
        action.deplacer(130)
        time.sleep(0.5)
        asser.gestionAvancer(200,instruction = "auStopNeRienFaire")
        action.deplacer(120)
        time.sleep(0.5)
        asser.gestionTourner(0,instruction = "auStopNeRienFaire")
        asser.gestionAvancer(200,instruction = "auStopNeRienFaire")
        action.deplacer(110)
        time.sleep(0.5)
        action.deplacer(120)
        time.sleep(0.5)
        asser.gestionTourner(0,instruction = "auStopNeRienFaire")
        asser.gestionAvancer(200,instruction = "auStopNeRienFaire")
        
        #mettre dans la cale
        asser.gestionAvancer(100,instruction = "auStopNeRienFaire")
        asser.gestionTourner(-math.pi/4,instruction = "auStopNeRienFaire")
        asser.gestionAvancer(300,instruction = "auStopNeRienFaire")
        asser.gestionTourner(0,instruction = "auStopNeRienFaire")
        asser.gestionAvancer(300,instruction = "auStopNeRienFaire")
        asser.gestionAvancer(-50,instruction = "auStopNeRienFaire")
        action.deplacer(130)
        time.sleep(0.2)
        action.deplacer(110)
        time.sleep(0.2)
        action.deplacer(130)
        asser.changerVitesse("translation", 3)
        asser.gestionAvancer(-50,instruction = "auStopNeRienFaire")
        asser.changerVitesse("translation", 2)
        asser.gestionAvancer(-300,instruction = "auStopNeRienFaire")
        action.deplacer(0)
        asser.gestionTourner(math.pi/2,instruction = "auStopNeRienFaire")
        
    # Rafflage du totem ennemi côté sud (y petits)
    def rafflerTotem10(self,asser,action) :
        log.logger.debug("Rafflage de totem 1 0 en cours")
        pass
    
    # Rafflage du totem ennemi, côté Nord.
    def rafflerTotem11(self,asser,action) :
        log.logger.debug("Rafflage de totem 1 1 en cours")
        pass
    
    
    #----------------------#
    #   BOUTONS POUSSOIR   #
    #----------------------#
    
    # Poussoir côté chez nous.
    def enfoncerPoussoir0(self,asser,action) :
        
        log.logger.debug("Enfonçage du poussoir côté nous en couuuuuuuurs")
        action.deplacer(0) # On met les bras à 110 pour arriver à la position
        #asser.goTo(Point(1500 - 640, 2000 - 500)) # On va se placer le long de la ligne
        log.logger.debug("hohohohoho")
        asser.gestionTourner(-math.pi/2) # on s'oriente vers les poussoir
        asser.gestionAvancer(290) # on avance au point de rotation
        asser.gestionTourner(-1.5)    # On lui montre nos fesses
        #asser.changerVitesse('translation', 3)   # .. Puis on l'enfonce en fonçant
        asser.gestionAvancer(-470.0)  # Pour l'enfoncer à fond
        #asser.changerVitesse('translation', 2)   # On remet le couple maxi à sa valeur d'origine.
        asser.gestionAvancer(450)    # On se barre.
        log.logger.debug("Enfonçage du poussoir à nous fini")
        
    # Poussoir côté ennemi.
    def enfoncerPoussoir1(self,asser,action) :
        
        log.logger.debug("Enfonçage du poussoir côté ennemi en cours")
        action.deplacer(0) # On met les bras à 110 pour arriver à la positionif idPoussoir == 0:
        #asser.goTo(Point(-1500 + 640 + 477, 2000 - 500)) # On va se placer le long de la ligne
        asser.gestionTourner(-math.pi/2) # on s'oriente vers les poussoir
        asser.gestionAvancer(290) # on avance au point de rotation
        asser.gestionTourner(-1.5)    # On lui montre nos fesses
        asser.changerVitesse('translation', 3)   # .. Puis on l'enfonce en fonçant
        asser.gestionAvancer(-470.0)  # Pour l'enfoncer à fond
        asser.changerVitesse('translation', 2)   # On remet le couple maxi à sa valeur d'origine.
        asser.gestionAvancer(450)    # On se barre.
        log.logger.debug("Enfonçage du poussoir ennemi fini")
        
        
    #----------------------#
    #       ANNEXES        #
    #----------------------#
    
        
    def faireChierEnnemi(self,asser,action) :
        """
        On fait un tour de table bras fermés
        """
        log.logger.debug("C'est parti, on farme l'ennemi !")
        self.tourDeTable(asser, action, False)
        
    def tourDeTable(self,asser,action, brasOuverts = True) :
        """
        Tenter de passer à des pts clés pour ramasser des éventuels CDs perdus
        """
        log.logger.debug("Tour de table")
        if brasOuverts:
            action.deplacer(120) # On ouvre les bras
        else:
            action.deplacer(0) #On garde les bras fermés
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
        if brasOuverts:
            action.deplacer(80) # On ferme les bras avant de gestionTourner
        else:
            pass
        asser.gestionTourner(0.755)
        action.deplacer(120) # On ouvre les bras pour déposer
        asser.gestionAvancer(340) # On va dans la calle
        asser.gestionAvancer(-450) # On fait marche arrière pour se dégager
        if brasOuverts:
            action.deplacer(100)
        else:
            pass
        log.logger.debug("Fin tour de table")
        
    def defendreBase(self,asser,action):
        """
        Si l'ennemi est très bon, il faudra penser à défendre la base
        """
        log.logger.debug("Défense de la base")
        asser.goTo(Point(960, 1260))
        asser.gestionTourner(math.pi/2)
        asser.gestionAvancer(1300)
        asser.gestionAvancer(-1300)
        log.logger.debug("Fin défense de la base")
        
        
        
        
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