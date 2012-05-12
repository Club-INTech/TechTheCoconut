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
            action = self.actionInstanceSimu
            #initialisations
            if hasattr(__builtin__.instance, 'serieAsserInstance'):
                asserv.setPosition(self.asserInstance.getPosition())
                asserv.setOrientation(self.asserInstance.getOrientation())
            else :
                #NOTE : pour tests (sans série)
                asserv.setPosition(Point(70,400))
                asserv.setOrientation(0)
                
            #début du calcul de durée du script
            asserv.lancerChrono()
        else:
            #instance pour les déplacements réels
            asserv = self.asserInstance
            action = self.actionInstance
            
        #vitesses normales
        asserv.changerVitesse("rotation",2)
        asserv.changerVitesse("translation",2)
        #try :
        #execution du script
        script(asserv,action)
        if chrono:
            #retour de la durée totale d'execution du script
            return asserv.mesurerChrono()
        else:
            #bon déroulement du script (pour des déplacements réels)
            return True
        #except :
            #spécifie un déroulement problématique
        return False
            
####################################################################################################################
###########################################     SCRIPTS SPECIAUX      ##############################################
####################################################################################################################


    def recalage(self, asserv,action):
        """
        Fonction permettant de recaller le robot dans un coin de la table
        """
        asserv.recalage()
        
    def homologation(self, asserv,action):
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
        asserv.gestionAvancer(500)     # On avance vers lui
        asserv.gestionTourner(-1.57)    # On lui montre nos fesses
        asserv.gestionAvancer(-480,"auStopNeRienFaire")    # On recule pour lui mettre sa dose
        asserv.changerVitesse("translation",3)
        asserv.gestionAvancer(-500.0,"auStopNeRienFaire")  # Pour l'enfoncer à fond
        asserv.changerVitesse("translation",2)
        asserv.gestionAvancer(200)
        asserv.gestionTourner(-1.57)    # réorientation du robot
        asserv.gestionAvancer(500)    # On se barre.
        
    def etalonnageAsserv(self, asserv,action):
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

    def scriptTotem(self,asser,action):
        #asser.setPosition(Point(70,400))
        #asser.setOrientation(math.pi/2)
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
    

    def test1(self,asserv, action):
        xd = raw_input("x départ? ")
        yd = raw_input("y départ? ")
        asserv.setPosition(Point(float(xd),float(yd)))
        asserv.setOrientation(math.pi/2)
        xa = raw_input("x arrivée? ")
        ya = raw_input("y arrivée? ")
        asserv.goTo(Point(float(xa),float(ya)))
        
    def test2(self,asserv,action):
        asserv.setPosition(Point(812,872))
        asserv.setOrientation(math.pi/2)
        asserv.goTo(Point(float(850),float(1600)))
    
    def test3(self,asserv,action):
        xa = raw_input("x robot adverse? ")
        ya = raw_input("y robot adverse? ")
        __builtin__.instance.ajouterRobotAdverse(Point(float(xa),float(ya)))
        
    def test4(self,asserv,action):
        asserv.changerVitesse("rotation",3)
        asserv.gestionTourner(-math.pi/2)
        
    def test5(self,asserv,action):
        asserv.gestionAvancer(300)
        asserv.gestionAvancer(300)
        asserv.changerVitesse("rotation",3)
        asserv.gestionTourner(0)
        
    def test6(self,asserv,action):
        asserv.goTo(Point(800, 250))
        
    def allerRetour(self, asserv,action):
        while 42:
            asserv.gestionAvancer(400)
            asserv.gestionTourner(0)
            asserv.gestionAvancer(400)
            asserv.gestionTourner(math.pi)
            
    def testTourdeTable(self, asserv,action):
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

    #----------------------#
    #        TOTEMS        #
    #----------------------#
    
    # Rafflage de notre totem côté sud (y petits)
    def rafflerTotem00(self,asserv,action) :
        log.logger.info("Rafflage de totem en cours")
        asserv.goTo(Point(0.,660.))
        #début notre totem sud
        asserv.gestionTourner(0)
        action.deplacer(130)
        time.sleep(0.5)
        asserv.gestionAvancer(200,instruction = "auStopNeRienFaire")
        action.deplacer(120)
        time.sleep(0.5)
        asserv.gestionTourner(0,instruction = "auStopNeRienFaire")
        asserv.gestionAvancer(200,instruction = "auStopNeRienFaire")
        action.deplacer(110)
        time.sleep(0.5)
        action.deplacer(120)
        time.sleep(0.5)
        asserv.gestionTourner(0,instruction = "auStopNeRienFaire")
        asserv.gestionAvancer(200,instruction = "auStopNeRienFaire")
        
        #mettre dans la cale
        asserv.gestionAvancer(100,instruction = "auStopNeRienFaire")
        asserv.gestionTourner(math.pi/4,instruction = "auStopNeRienFaire")
        asserv.gestionAvancer(300,instruction = "auStopNeRienFaire")
        asserv.gestionTourner(0,instruction = "auStopNeRienFaire")
        asserv.gestionAvancer(300,instruction = "auStopNeRienFaire")
        asserv.gestionAvancer(-50,instruction = "auStopNeRienFaire")
        action.deplacer(130)
        time.sleep(0.2)
        action.deplacer(110)
        time.sleep(0.2)
        action.deplacer(130)
        asserv.changerVitesse("translation", 3)
        asserv.gestionAvancer(-50,instruction = "auStopNeRienFaire")
        asserv.changerVitesse("translation", 2)
        asserv.gestionAvancer(-300,instruction = "auStopNeRienFaire")
        action.deplacer(0)
        asserv.gestionTourner(math.pi/2,instruction = "auStopNeRienFaire")
    
    # Rafflage de notre totem côté nord (y grands)
    def rafflerTotem01(self,asserv,action) :
        log.logger.info("Rafflage de totem en cours")
        pass
        
    # Rafflage du totem ennemi côté sud (y petits)
    def rafflerTotem10(self,asserv,action) :
        log.logger.info("Rafflage de totem en cours")
        pass
    
    # Rafflage du totem ennemi, côté Nord.
    def rafflerTotem11(self,asserv,action) :
        log.logger.info("Rafflage de totem en cours")
        pass
    
    
    #----------------------#
    #   BOUTONS POUSSOIR   #
    #----------------------#
    
    # Poussoir côté chez nous.
    def enfoncerPoussoir0(self,asserv,action) :
        
        log.logger.info("Enfonçage du poussoir à nous en cours")
        action.deplacer(110) # On met les bras à 110 pour arriver à la position
        asserv.goTo(Point(1500 - 640, 2000 - 740)) # On va se placer le long de la ligne
        asserv.gestionTourner(-math.pi/2) # on s'oriente vers les poussoir
        asserv.gestionAvancer(290) # on avance au point de rotation
        asserv.gestionTourner(-1.5)    # On lui montre nos fesses
        asserv.changerVitesse('translation', 3)   # .. Puis on l'enfonce en fonçant
        asserv.gestionAvancer(-470.0)  # Pour l'enfoncer à fond
        asserv.changerVitesse('translation', 2)   # On remet le couple maxi à sa valeur d'origine.
        asserv.gestionAvancer(450)    # On se barre.
        log.logger.info("Enfonçage du poussoir à nous fini")
        
    # Poussoir côté ennemi.
    def enfoncerPoussoir1(self,asserv,action) :
        
        log.logger.info("Enfonçage du poussoir ennemi en cours")
        action.deplacer(110) # On met les bras à 110 pour arriver à la positionif idPoussoir == 0:
        asserv.goTo(Point(-1500 + 640 + 477, 2000 - 740)) # On va se placer le long de la ligne
        asserv.gestionTourner(-math.pi/2) # on s'oriente vers les poussoir
        asserv.gestionAvancer(290) # on avance au point de rotation
        asserv.gestionTourner(-1.5)    # On lui montre nos fesses
        asserv.changerVitesse('translation', 3)   # .. Puis on l'enfonce en fonçant
        asserv.gestionAvancer(-470.0)  # Pour l'enfoncer à fond
        asserv.changerVitesse('translation', 2)   # On remet le couple maxi à sa valeur d'origine.
        asserv.gestionAvancer(450)    # On se barre.
        log.logger.info("Enfonçage du poussoir ennemi fini")
        
        
    #----------------------#
    #       ANNEXES        #
    #----------------------#
    
        
    def faireChierEnnemi(self,asserv,action) :
        """
        Comment va-t-on bien faire chier l'ennemi ?
        """
        log.logger.info("C'est parti, on farme l'ennemi !")
        pass
        
    def tourDeTable(self,asserv,action) :
        """
        Tenter de passer à des pts clés pour ramasser des éventuels CDs perdus
        """
        log.logger.info("Tour de table")
        action.deplacer(120) # On ouvre les bras
        asserv.goTo(Point(860, 650)) # On va se placer à un de départ près de notre base
        asserv.goTo(Point(395, 505))
        asserv.goTo(Point(10, 580))
        asserv.goTo(Point(-425, 480))
        asserv.goTo(Point(-900, 970))
        asserv.goTo(Point(410, 1480))
        asserv.goTo(Point(0, 1400))
        asserv.goTo(Point(405, 1480))
        asserv.goTo(Point(900, 1000))
        asserv.goTo(Point(890, 755))
        action.deplacer(80) # On ferme les bras avant de gestionTourner
        asserv.gestionTourner(0.755)
        action.deplacer(120) # On ouvre les bras pour déposer
        asserv.gestionAvancer(340) # On va dans la calle
        asserv.gestionAvancer(-450) # On fait marche arrière pour se dégager
        action.deplacer(100)
        log.logger.info("Fin tour de table")
        
    def defendreBase(self,asserv,action):
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

def scriptPipeauNewStrategie(self, asserv,action):
        #déplacements
        asserv.gestionAvancer(300)
        asserv.gestionAvancer(300,"forcer")
        asserv.changerVitesse("translation",1)
        
        asserv.gestionTourner(math.pi)
        asserv.changerVitesse("rotation",3)
        
        asserv.goTo(Point(800, 250))
        
        #exemples bras
        self.action.deplacer(90)                 # tous les bras
        self.action.deplacer(70, "hd")           # Bras Haud Droit (vu depuis le derrière du robot)
        self.action.deplacer(50, ["hg", "bg"])   # Tourner les bras gauches
        self.action.changer_vitesse(100)         # Entre 100 et 500 en gros mais on peut monter à 1000
"""